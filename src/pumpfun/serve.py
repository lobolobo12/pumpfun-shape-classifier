"""serve — a local scoring endpoint for the paper bot.

POST /score  {mint, creator, launch_time_ms, trades: [swap-api v2 rows, oldest first, through the crossing]}
             or {mint, features: {name: value}} when the caller computed the features itself (xgb_botlive)
          -> {score, pct, model, decision: {...}}  or  {"skip": reason}
GET  /health -> model name, split it was trained on, feature count.

The tape is replayed through the same curve simulator and feature code as training; the decision moment
is the first trade after which the curve holds >= cross_level_sol real SOL with the coin at least
cross_min_age_seconds old. `pct` is the score's percentile against the model's held-out test scores, so
the bot can act on "top 5 %" without knowing the score scale. Stdlib HTTP server: one process, no deps.
"""

from __future__ import annotations

import os

# xgboost and torch each bundle their own OpenMP runtime; loading both in one process segfaults on macOS
# inside the first convolution unless the duplicate is tolerated. Must be set before either import.
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import json  # noqa: E402
import logging
import time
from bisect import bisect_left
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import numpy as np

from pumpfun.config import Config
from pumpfun.features.tabular import botlive_features, shape_and_holders
from pumpfun.ingest.swap_api import TradeFile, parse_trade
from pumpfun.ingest.to_parquet import tape_rows

log = logging.getLogger(__name__)

DEFAULT_MODEL = "xgb_shape+holders"


class Scorer:
    def __init__(self, cfg: Config, name: str = DEFAULT_MODEL):
        import xgboost as xgb

        self.xgb = xgb
        d = cfg.processed_dir / "models" / cfg.decision_mode
        meta = json.loads((d / f"{name}.json").read_text())
        self.cfg = cfg
        self.name = name
        self.features: list[str] = meta["features"]
        # bot-facing names: the truncated training columns are "bl_<name>", the bot sends "<name>"
        self.request_names: list[str] = [c[3:] if c.startswith("bl_") else c for c in self.features]
        self.truncated = any(c.startswith("bl_") for c in self.features)
        self.splits = meta["splits"]
        self.test_scores: list[float] = meta["test_scores"]
        self.test_pnl: list[float] | None = meta.get("test_pnl")
        self.boosters: list[xgb.Booster] = []
        for path in [d / f"{name}.ubj", *sorted(d.glob(f"{name}.*.ubj"))]:
            b = self.xgb.Booster()
            b.load_model(str(path))
            self.boosters.append(b)
        self.level = float(cfg.raw.get("cross_level_sol", 0.0) or 0.0)
        self.min_age = float(cfg.raw.get("cross_min_age_seconds", 0) or 0)
        self.silence = float(cfg.metrics["active_silence_max"])
        log.info("loaded %s (%d features, trained to %s)", name, len(self.features), self.splits["train_end"])
        self.stats = {"requests": 0, "scored": 0, "skipped": 0, "errors": 0, "fired_pct95": 0, "last_request_at": None}

    def score(self, req: dict) -> dict:
        t0 = time.perf_counter()
        if isinstance(req.get("features"), dict):
            # bot-live path: the caller computed the features itself (model xgb_botlive)
            f = req["features"]
            # the launch bundle crosses the level inside the first seconds; training never sees those coins
            cross_age = f.get("cross_age_s")
            if cross_age is not None and float(cross_age) < self.min_age:
                return {"skip": "crossed_too_young", "cross_age_s": float(cross_age)}
            share = f.get("top10_share")
            if share is not None and float(share) > 1.0:
                return {"skip": "top10_share_out_of_range", "top10_share": float(share)}
            return self._score_features(f, t0, {"source": "features"})
        mint = str(req["mint"])
        creator = str(req.get("creator") or "")
        launch_ms = int(req["launch_time_ms"])
        raw = req.get("trades") or []
        if not raw:
            return {"skip": "no trades"}
        trades = sorted((parse_trade(r) if "slotIndexId" in r else _from_internal(r) for r in raw), key=lambda t: (t.slot, t.idx))
        tf = TradeFile(
            mint=mint, fetched_at_ms=int(time.time() * 1000), start_cursor=None, complete=False, pages=0, trades=trades
        )
        rows = tape_rows(self.cfg, tf, launch_ms)
        # decision: first row after which the curve holds the level, coin old enough
        cut = None
        for i, r in enumerate(rows):
            sol = r["curve_sol_after"]
            if sol is not None and sol >= self.level and r["seconds_since_launch"] >= self.min_age:
                cut = i
                break
        if cut is None:
            return {"skip": "level not reached", "n_trades": len(rows)}
        visible = rows[: cut + 1]
        entry_t = float(visible[-1]["seconds_since_launch"])
        if len(visible) < int(self.cfg.min_trades_in_window):
            return {"skip": "too few trades", "n_trades": len(visible)}
        if visible[-1]["program"] != "pump":
            return {"skip": "not on the curve"}
        tup = [
            (r["seconds_since_launch"], r["slot"], r["is_buy"], r["sol_amount"], r["token_amount"], r["trader"], r["price_sol"])
            for r in visible
        ]
        sol_at = float(visible[-1]["curve_sol_after"])
        px = float(visible[-1]["price_sol"])
        feats = shape_and_holders(self.cfg, tup, creator, sol_at, px, entry_t)
        if self.truncated:
            level = float(req.get("first_seen_sol", 4.5))
            feats.update(
                botlive_features(
                    self.cfg, tup, [r["curve_sol_after"] for r in visible], creator, entry_t, level, feats["top10_share"]
                )
            )
        decision = {
            "entry_t": entry_t,
            "curve_sol": float(visible[-1]["curve_sol_after"]),
            "n_visible": len(visible),
            "slot": int(visible[-1]["slot"]),
        }
        return self._score_features(feats, t0, decision)

    def _ev_at(self, s: float, min_rows: int = 8) -> float | None:
        if not self.test_pnl:
            return None
        i = bisect_left(self.test_scores, s)
        tail = self.test_pnl[i:]
        if len(tail) < min_rows:
            tail = self.test_pnl[-min_rows:]
        return round(float(np.mean(tail)), 4) if tail else None

    def _score_features(self, feats: dict, t0: float, decision: dict) -> dict:
        # accept either the training column names or the bot-facing names
        vals = [feats.get(c, feats.get(r)) for c, r in zip(self.features, self.request_names, strict=True)]
        missing = [r for r, v in zip(self.request_names, vals, strict=True) if v is None]
        x = np.array([[float(v) if v is not None else np.nan for v in vals]], dtype=np.float32)
        dm = self.xgb.DMatrix(x)
        s = float(np.mean([b.predict(dm)[0] for b in self.boosters]))
        pct = 100.0 * bisect_left(self.test_scores, s) / max(1, len(self.test_scores))
        out = {
            "score": s,
            "pct": round(pct, 1),
            # expected PnL per 0.5 SOL trade if every held-out coin scoring at least this high had been bought
            "ev_sol": self._ev_at(s),
            "model": self.name,
            "decision": decision,
            "latency_ms": round(1000 * (time.perf_counter() - t0), 1),
        }
        if missing:
            out["missing_features"] = missing
        return out


class CnnScorer:
    """Bot-view series CNN (cnn_botlive+side): the sampled reserve series + the 16 bot-live features."""

    def __init__(self, cfg: Config, name: str = "cnn_botlive+side"):
        import torch  # only in the CNN process; never next to xgboost

        from pumpfun.models.cnn import ShapeNet

        d = cfg.processed_dir / "models" / cfg.decision_mode
        blob = self.torch.load(d / f"{name}.pt", map_location="cpu")
        self.cfg, self.name, self.torch = cfg, name, torch
        a = blob["arch"]
        self.models = []
        for sd in blob["state_dicts"]:
            m = ShapeNet(a["in_ch"], len(blob["side_cols"]), a["channels"], a["blocks"], a["kernel"], a["dropout"])
            m.load_state_dict(sd)
            m.eval()
            self.models.append(m)
        self.side_cols: list[str] = blob["side_cols"]
        self.request_names = [c[3:] if c.startswith("bl_") else c for c in self.side_cols]
        self.side_mean = np.array(blob["side_mean"], dtype=np.float32)
        self.side_std = np.array(blob["side_std"], dtype=np.float32)
        self.steps = int(blob["steps"])
        self.splits = blob["splits"]
        self.test_scores: list[float] = blob["test_scores"]
        self.test_pnl: list[float] | None = blob.get("test_pnl")
        self.features = self.request_names
        self.truncated = True
        self.boosters = self.models
        self.stats = {"requests": 0, "scored": 0, "skipped": 0, "errors": 0, "fired_pct95": 0, "last_request_at": None}
        self.level = float(cfg.raw.get("cross_level_sol", 0.0) or 0.0)
        self.min_age = float(cfg.raw.get("cross_min_age_seconds", 0) or 0)
        log.info("loaded %s (%d seeds, %d steps, %d side features)", name, len(self.models), self.steps, len(self.side_cols))

    _ev_at = Scorer._ev_at

    def _encode(self, series: list) -> np.ndarray:
        from pumpfun.features.sequence import graduation_sol
        from pumpfun.ingest.to_parquet import curve_params
        from pumpfun.label import curve_sim as cs

        p = curve_params(self.cfg)
        grad = graduation_sol(self.cfg)
        ser = [(float(t), float(px), float(sol)) for t, px, sol in series]
        # the bot sends price as virtual SOL lamports per raw token unit; training used SOL per token. Both
        # are the same curve constant times a fixed factor, so pick the launch price in whichever unit the
        # first sample is closest to (a coin's first sample is within a few x of the start price).
        p0_sol = cs.initial_reserves(p).spot_sol_per_token(p.raw_per_token)
        p0_raw = p.initial_virtual_sol / p.initial_virtual_token
        first = ser[0][1] if ser else p0_sol
        p0 = min((p0_sol, p0_raw), key=lambda c: abs(np.log(max(first, 1e-30) / c)))
        ser = ser[-self.steps :]
        x = np.zeros((1, self.steps, 4), dtype=np.float32)
        off = self.steps - len(ser)
        prev = 0.0
        for k, (t, px, sol) in enumerate(ser):
            x[0, off + k] = (np.log(px / p0) if px > 0 else 0.0, np.log1p(max(0.0, t - prev)), sol / grad, 1.0 if k == 0 else 0.0)
            prev = t
        return x.transpose(0, 2, 1)

    def score(self, req: dict) -> dict:
        t0 = time.perf_counter()
        feats = req.get("features") or {}
        series = req.get("series")
        if not series:
            return {"skip": "no series"}
        cross_age = feats.get("cross_age_s")
        if cross_age is not None and float(cross_age) < self.min_age:
            return {"skip": "crossed_too_young", "cross_age_s": float(cross_age)}
        vals = [feats.get(c, feats.get(r)) for c, r in zip(self.side_cols, self.request_names, strict=True)]
        missing = [r for r, v in zip(self.request_names, vals, strict=True) if v is None]
        side = np.array([[float(v) if v is not None else 0.0 for v in vals]], dtype=np.float32)
        side = (side - self.side_mean) / self.side_std
        x = self.torch.tensor(self._encode(series))
        sd = self.torch.tensor(side) if self.side_cols else None
        with self.torch.no_grad():
            s = float(np.mean([self.torch.sigmoid(m(x, sd)).item() for m in self.models]))
        pct = 100.0 * bisect_left(self.test_scores, s) / max(1, len(self.test_scores))
        out = {
            "score": s,
            "pct": round(pct, 1),
            "ev_sol": self._ev_at(s),
            "model": self.name,
            "decision": {"source": "series", "n_samples": len(series)},
            "latency_ms": round(1000 * (time.perf_counter() - t0), 1),
        }
        if missing:
            out["missing_features"] = missing
        return out


def _from_internal(r: dict):
    from pumpfun.ingest.swap_api import Trade

    return Trade.from_json(r)


def serve(cfg: Config, host: str, port: int, name: str = DEFAULT_MODEL) -> None:
    scorer = CnnScorer(cfg, name) if name.startswith("cnn_") else Scorer(cfg, name)
    # xgboost and torch cannot share a process (two OpenMP runtimes: a booster call after a torch op, or
    # the reverse, segfaults on macOS), so the bot-view CNN runs as its own `pf serve --model cnn_botlive+side`
    # on the companion port and the primary forwards the request to it over loopback.
    companion_url = None if name.startswith("cnn_") else f"http://127.0.0.1:{port + 1}/score"
    companion_name = None
    if companion_url:
        try:
            import urllib.request

            with urllib.request.urlopen(companion_url.replace("/score", "/health"), timeout=1) as r:
                companion_name = json.loads(r.read()).get("model")
        except Exception:  # noqa: BLE001
            companion_url = None

    class H(BaseHTTPRequestHandler):
        def _send(self, code: int, body: dict) -> None:
            data = json.dumps(body).encode()
            self.send_response(code)
            self.send_header("content-type", "application/json")
            self.send_header("content-length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):  # noqa: N802
            if self.path == "/health":
                self._send(
                    200,
                    {
                        "ok": True,
                        "model": scorer.name,
                        "splits": scorer.splits,
                        "n_features": len(scorer.features),
                        "features": scorer.request_names,
                        "truncated_training": scorer.truncated,
                        "stats": scorer.stats,
                        "ev_available": scorer.test_pnl is not None,
                        "companion": companion_name,
                        "bag": len(scorer.boosters),
                    },
                )
            else:
                self._send(404, {"error": "unknown path"})

        def do_POST(self):  # noqa: N802
            if self.path != "/score":
                self._send(404, {"error": "unknown path"})
                return
            n = int(self.headers.get("content-length") or 0)
            st = scorer.stats
            st["requests"] += 1
            st["last_request_at"] = int(time.time())
            try:
                req = json.loads(self.rfile.read(n) or b"{}")
                out = scorer.score(req)
                if companion_url and req.get("series") and "score" in out:
                    try:
                        import urllib.request

                        creq = urllib.request.Request(
                            companion_url, data=json.dumps(req).encode(), headers={"content-type": "application/json"}
                        )
                        with urllib.request.urlopen(creq, timeout=0.5) as r:
                            out["cnn"] = json.loads(r.read())
                    except Exception as e:  # noqa: BLE001 — the companion never blocks the primary answer
                        out["cnn"] = {"error": f"{e.__class__.__name__}: {e}"}
                st["scored" if "score" in out else "skipped"] += 1
                if out.get("pct", 0) >= 95:
                    st["fired_pct95"] += 1
                self._send(200, out)
            except Exception as e:  # noqa: BLE001 — report, keep serving
                st["errors"] += 1
                log.exception("score failed")
                self._send(400, {"error": f"{e.__class__.__name__}: {e}"})

        def log_message(self, fmt, *args):  # quiet
            return

    srv = ThreadingHTTPServer((host, port), H)
    log.info("pf serve: http://%s:%d  (POST /score, GET /health)", host, port)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
