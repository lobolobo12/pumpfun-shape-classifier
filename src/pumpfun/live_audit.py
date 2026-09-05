"""live_audit — the bot's posted feature dicts vs the training distribution of the same columns.

Catches what a unit test cannot: a units bug, a cohort the model never saw, a renamed key. Reads the
bot's nn_scores table (ops.db), takes decisions since `--since` (default: last 24 h), compares each
bot-view feature's live median / p90 with the held-out training columns, and flags drift. Written to
reports/live_audit.json and printed; exit code 1 when anything is flagged, so the daily cycle notices.
"""

from __future__ import annotations

import json
import logging
import sqlite3
import time

import numpy as np
import polars as pl

from pumpfun.config import Config
from pumpfun.features.tabular import BOTLIVE_NAMES
from pumpfun.reports import write_json

log = logging.getLogger(__name__)

# a feature is flagged when its live median is outside [lo, hi] x the training median (after a floor)
RATIO_LO, RATIO_HI, FLOOR = 0.4, 2.5, 0.05
MIN_ROWS = 20


def run(cfg: Config, since_ms: int | None = None) -> dict:
    ops = cfg.raw.get("sources", {}).get("ops_db") or "/Users/lovrobor/axiom-holy-sol/data/ops.db"
    since_ms = since_ms or int((time.time() - 86_400) * 1000)
    con = sqlite3.connect(f"file:{ops}?mode=ro", uri=True)
    rows = con.execute(
        "select score, pct, missing, features from nn_scores where decided_at >= ? order by decided_at", (since_ms,)
    ).fetchall()
    con.close()
    scored = [r for r in rows if r[0] is not None and r[3]]
    skips: dict[str, int] = {}
    for r in rows:
        if r[0] is None:
            try:
                k = ",".join(json.loads(r[2]) or []) or "unknown"
            except Exception:  # noqa: BLE001
                k = str(r[2])
            skips[k] = skips.get(k, 0) + 1
    out: dict = {
        "since_ms": since_ms,
        "crossings": len(rows),
        "scored": len(scored),
        "skipped": skips,
        "features": {},
        "flags": [],
    }
    if len(scored) < MIN_ROWS:
        out["flags"].append(f"only {len(scored)} scored rows (< {MIN_ROWS}); nothing compared")
        write_json(cfg.reports_dir / "live_audit.json", out)
        print(json.dumps(out, indent=1))
        return out
    live = [json.loads(r[3]) for r in scored]
    te = pl.read_parquet(cfg.processed_dir / "features.parquet")
    te = te.filter(pl.col("split") == "test") if te.filter(pl.col("split") == "test").height >= MIN_ROWS else te
    for n in BOTLIVE_NAMES:
        lv = np.array([float(f[n]) for f in live if f.get(n) is not None], dtype=float)
        col = f"bl_{n}"
        if col not in te.columns:
            continue
        tv = te[col].drop_nulls().to_numpy().astype(float)
        if len(lv) == 0:
            out["flags"].append(f"{n}: missing in every live dict")
            continue
        lm, tm = float(np.median(lv)), float(np.median(tv))
        entry = {
            "live_median": lm,
            "train_median": tm,
            "live_p90": float(np.quantile(lv, 0.9)),
            "train_p90": float(np.quantile(tv, 0.9)),
            "n_live": int(len(lv)),
        }
        out["features"][n] = entry
        if n == "top10_share" and (lv.max() > 1.0 or lv.min() < 0.0):
            out["flags"].append(f"{n}: live values outside [0, 1]")
        ratio = (abs(lm) + FLOOR) / (abs(tm) + FLOOR)
        if ratio < RATIO_LO or ratio > RATIO_HI:
            out["flags"].append(f"{n}: live median {lm:.3f} vs training {tm:.3f}")
    sc = np.array([r[0] for r in scored])
    pc = np.array([r[1] for r in scored])
    out["score"] = {"live_median": float(np.median(sc)), "share_pct95": float((pc >= 95).mean())}
    if (pc >= 95).mean() > 0.2:
        out["flags"].append(f"{(pc >= 95).mean():.0%} of live decisions in the top 5 % bucket")
    write_json(cfg.reports_dir / "live_audit.json", out)
    print(f"live audit: {len(rows)} crossings, {len(scored)} scored, skips {skips}")
    for n, e in out["features"].items():
        med = f"live {e['live_median']:9.3f} / train {e['train_median']:9.3f}"
        p90 = f"p90 {e['live_p90']:9.3f} / {e['train_p90']:9.3f}"
        print(f"  {n:18s} {med}   {p90}")
    print("  flags:", out["flags"] or "none")
    return out
