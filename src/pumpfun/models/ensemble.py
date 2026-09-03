"""ensemble — rank-average the saved test scores of several models (no refitting).

Members come from `ensemble.members` in config.yaml and must have been trained in this run, so their
prediction files under data/processed/preds/ belong to the same split and mode. Ranks rather than raw
probabilities, since XGBoost and the CNN are calibrated differently.
"""

from __future__ import annotations

import logging

import numpy as np
import polars as pl

from pumpfun.config import Config
from pumpfun.models import metrics
from pumpfun.reports import append_history, write_json

log = logging.getLogger(__name__)


def rank_average(cols: list[np.ndarray]) -> np.ndarray:
    from scipy.stats import rankdata

    return np.mean([rankdata(c) / len(c) for c in cols], axis=0)


def run(cfg: Config) -> dict:
    members = list((cfg.raw.get("ensemble") or {}).get("members") or [])
    if len(members) < 2:
        raise SystemExit("ensemble.members needs at least two model names")
    feats = pl.read_parquet(cfg.processed_dir / "features.parquet")
    labels = pl.read_parquet(cfg.interim_dir / "labels.parquet").select("mint", "entry_cost_sol", "exit_net_sol")
    te = feats.join(labels, on="mint", how="left").filter(pl.col("split") == "test")
    if str(cfg.raw.get("population", "all")) == "active":
        te = te.filter(pl.col("active_at_entry").fill_null(False))
    scores = []
    for m in members:
        path = cfg.processed_dir / "preds" / f"{m}.parquet"
        if not path.exists():
            raise SystemExit(f"no saved predictions for {m}: train it first ({path})")
        pr = pl.read_parquet(path)
        joined = te.select("mint").join(pr, on="mint", how="left")
        if joined["p"].null_count():
            raise SystemExit(f"{m}: predictions do not cover the current test split — retrain it in this run")
        scores.append(joined["p"].to_numpy())
    p = rank_average(scores)
    name = "ensemble:" + "+".join(members)
    result = metrics.evaluate(cfg, te, p)
    metrics.save_predictions(cfg, "ensemble", te, p)
    report = {"results": {name: result}, "members": members}
    write_json(cfg.reports_dir / "m6_ensemble.json", report)
    append_history(
        cfg.reports_dir,
        {
            "model": name,
            "mode": cfg.decision_mode,
            "splits": {"train_end": cfg.split_train_end, "val_end": cfg.split_val_end},
            "test_n": result["n"],
            "test_pos": result["positives"],
            "base_rate": result["base_rate"],
            "pr_auc": result["pr_auc"],
            "roc_auc": result["roc_auc"],
            "p_at_10pct": result["precision_at"]["0.1"]["precision"],
            "pnl_at_10pct": result["pnl_at"]["0.1"]["pnl_sol"],
            "pnl_ex_top3": result["pnl_at"]["0.1"]["pnl_ex_top3_sol"],
            "weighted_pr_auc": (result.get("weighted") or {}).get("pr_auc"),
            "weighted_base_rate": (result.get("weighted") or {}).get("base_rate"),
            "serial_launcher": result.get("slice_serial_launcher", {}).get("pr_auc"),
            "train_n": None,
        },
    )
    md = [f"# Milestone 6 — {name}\n", metrics.comparison_table(cfg, {name: result}), ""]
    (cfg.reports_dir / "m6_ensemble.md").write_text("\n".join(md) + "\n")
    log.info("%s: test PR-AUC %.3f (base %.3f)", name, result["pr_auc"], result["base_rate"])
    return report
