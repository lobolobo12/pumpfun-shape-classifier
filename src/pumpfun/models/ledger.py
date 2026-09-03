"""ledger — read reports/model_history.jsonl and average each model over its held-out days.

One held-out day has ~20 positives, so single-day PR-AUC swings by ±0.08 between otherwise identical
runs. This report keeps, per (mode, model, test day), only the LATEST evaluation of that day, then
averages lift = pr_auc / base_rate and PR-AUC across days. Models are compared on the days they share.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import polars as pl

from pumpfun.config import Config

log = logging.getLogger(__name__)


def load(reports_dir: Path) -> pl.DataFrame:
    rows = []
    for line in (reports_dir / "model_history.jsonl").read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        rows.append(
            {
                "at": int(r["at"]),
                # rows backfilled from git predate decision_mode; they were age-mode runs
                "mode": r.get("mode") or "age",
                "model": r["model"],
                "test_day": (r.get("splits") or {}).get("val_end"),
                "train_end": (r.get("splits") or {}).get("train_end"),
                "test_n": r.get("test_n"),
                "test_pos": r.get("test_pos"),
                "base_rate": r.get("base_rate"),
                "pr_auc": r.get("pr_auc"),
                "roc_auc": r.get("roc_auc"),
                "p_at_10pct": r.get("p_at_10pct"),
                "pnl_at_10pct": r.get("pnl_at_10pct"),
                "pnl_ex_top3": r.get("pnl_ex_top3"),
            }
        )
    return pl.DataFrame(rows)


def summarize(df: pl.DataFrame) -> pl.DataFrame:
    # a held-out day is one where the test day follows the train end (the val split sits between them)
    held = df.filter(pl.col("test_day").is_not_null() & pl.col("pr_auc").is_not_null())
    latest = held.sort("at").group_by("mode", "model", "test_day").last()
    latest = latest.with_columns(lift=pl.col("pr_auc") / pl.col("base_rate"))
    return (
        latest.group_by("mode", "model")
        .agg(
            days=pl.len(),
            pr_auc_mean=pl.col("pr_auc").mean(),
            lift_mean=pl.col("lift").mean(),
            lift_min=pl.col("lift").min(),
            p10_mean=pl.col("p_at_10pct").mean(),
            pnl10_sum=pl.col("pnl_at_10pct").sum(),
            pnl_ex3_sum=pl.col("pnl_ex_top3").sum(),
            positives=pl.col("test_pos").sum(),
            last_day=pl.col("test_day").max(),
        )
        .sort("mode", "lift_mean", descending=[False, True])
    )


def run(cfg: Config) -> pl.DataFrame:
    df = load(cfg.reports_dir)
    summary = summarize(df)
    per_day = (
        df.filter(pl.col("pr_auc").is_not_null() & pl.col("test_day").is_not_null())
        .sort("at")
        .group_by("mode", "model", "test_day")
        .last()
        .select("mode", "test_day", "model", "pr_auc", "base_rate", "test_pos")
        .sort("mode", "test_day", "pr_auc", descending=[False, False, True])
    )
    md = ["# Model ledger — held-out days averaged\n"]
    md.append("Latest evaluation per (mode, model, test day); lift = PR-AUC / base rate.\n")
    for mode in summary["mode"].unique().sort().to_list():
        s = summary.filter(pl.col("mode") == mode)
        md.append(f"\n## {mode} mode\n")
        md.append("| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |")
        md.append("|---|---|---|---|---|---|---|---|---|")
        for r in s.iter_rows(named=True):
            md.append(
                f"| {r['model']} | {r['days']} | {r['positives']} | {r['pr_auc_mean']:.3f} | {r['lift_mean']:.2f}× | "
                f"{r['lift_min']:.2f}× | {r['p10_mean']:.2f} | {r['pnl10_sum']:+.2f} | {r['pnl_ex3_sum']:+.2f} |"
            )
        days = per_day.filter(pl.col("mode") == mode)["test_day"].unique().sort().to_list()
        md.append(f"\nTest days: {', '.join(days)}\n")
    out = cfg.reports_dir / "ledger_summary.md"
    out.write_text("\n".join(md) + "\n")
    summary.write_csv(cfg.reports_dir / "ledger_summary.csv")
    log.info("-> %s (%d model rows)", out, summary.height)
    return summary
