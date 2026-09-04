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

import json
import logging
import time
from bisect import bisect_left
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import numpy as np
import xgboost as xgb

from pumpfun.config import Config
from pumpfun.features.tabular import shape_and_holders
from pumpfun.ingest.swap_api import TradeFile, parse_trade
from pumpfun.ingest.to_parquet import tape_rows

log = logging.getLogger(__name__)

DEFAULT_MODEL = "xgb_shape+holders"


class Scorer:
    def __init__(self, cfg: Config, name: str = DEFAULT_MODEL):
        d = cfg.processed_dir / "models" / cfg.decision_mode
        meta = json.loads((d / f"{name}.json").read_text())
        self.cfg = cfg
        self.name = name
        self.features: list[str] = meta["features"]
        self.splits = meta["splits"]
        self.test_scores: list[float] = meta["test_scores"]
        self.boosters: list[xgb.Booster] = []
        for path in [d / f"{name}.ubj", *sorted(d.glob(f"{name}.*.ubj"))]:
            b = xgb.Booster()
            b.load_model(str(path))
            self.boosters.append(b)
        self.level = float(cfg.raw.get("cross_level_sol", 0.0) or 0.0)
        self.min_age = float(cfg.raw.get("cross_min_age_seconds", 0) or 0)
        self.silence = float(cfg.metrics["active_silence_max"])
        log.info("loaded %s (%d features, trained to %s)", name, len(self.features), self.splits["train_end"])
        self.n_bag = 0

    def score(self, req: dict) -> dict:
        t0 = time.perf_counter()
        if isinstance(req.get("features"), dict):
            # bot-live path: the caller computed the features itself (model xgb_botlive)
            return self._score_features(req["features"], t0, {"source": "features"})
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
        feats = shape_and_holders(
            self.cfg, tup, creator, float(visible[-1]["curve_sol_after"]), float(visible[-1]["price_sol"]), entry_t
        )
        decision = {
            "entry_t": entry_t,
            "curve_sol": float(visible[-1]["curve_sol_after"]),
            "n_visible": len(visible),
            "slot": int(visible[-1]["slot"]),
        }
        return self._score_features(feats, t0, decision)

    def _score_features(self, feats: dict, t0: float, decision: dict) -> dict:
        missing = [c for c in self.features if c not in feats]
        x = np.array([[float(feats.get(c) if feats.get(c) is not None else np.nan) for c in self.features]], dtype=np.float32)
        dm = xgb.DMatrix(x)
        s = float(np.mean([b.predict(dm)[0] for b in self.boosters]))
        pct = 100.0 * bisect_left(self.test_scores, s) / max(1, len(self.test_scores))
        out = {
            "score": s,
            "pct": round(pct, 1),
            "model": self.name,
            "decision": decision,
            "latency_ms": round(1000 * (time.perf_counter() - t0), 1),
        }
        if missing:
            out["missing_features"] = missing
        return out


def _from_internal(r: dict):
    from pumpfun.ingest.swap_api import Trade

    return Trade.from_json(r)


def serve(cfg: Config, host: str, port: int, name: str = DEFAULT_MODEL) -> None:
    scorer = Scorer(cfg, name)

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
                        "features": scorer.features,
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
            try:
                req = json.loads(self.rfile.read(n) or b"{}")
                self._send(200, scorer.score(req))
            except Exception as e:  # noqa: BLE001 — report, keep serving
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
