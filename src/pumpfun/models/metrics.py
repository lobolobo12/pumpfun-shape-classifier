"""metrics — what every model is judged on (spec §11), always next to the human number.

PR-AUC (primary), precision at the top 1 / 5 / 10 % of predicted probability,
simulated PnL on the test set from the labels' realized exits (fees included),
ex-top-3 PnL (handoff §5.6), and the same on the friends' zone slice.
"""

from __future__ import annotations

import numpy as np
import polars as pl
from sklearn.metrics import average_precision_score, roc_auc_score

from pumpfun.config import Config
from pumpfun.reports import read_json


def precision_at(y: np.ndarray, p: np.ndarray, frac: float) -> dict:
    k = max(1, int(round(len(y) * frac)))
    idx = np.argsort(-p)[:k]
    return {"k": k, "precision": float(y[idx].mean())}


def pnl_at(frac: float, p: np.ndarray, cost: np.ndarray, net: np.ndarray) -> dict:
    k = max(1, int(round(len(p) * frac)))
    idx = np.argsort(-p)[:k]
    pnl = net[idx] - cost[idx]
    top3 = np.sort(pnl)[-3:].sum() if len(pnl) >= 3 else pnl.sum()
    return {
        "k": k,
        "pnl_sol": float(pnl.sum()),
        "pnl_ex_top3_sol": float(pnl.sum() - top3),
        "mean_per_trade_sol": float(pnl.mean()),
        "win_rate": float((pnl > 0).mean()),
    }


def weighted_precision_at(y: np.ndarray, p: np.ndarray, w: np.ndarray, frac: float) -> dict:
    """Precision among the highest-scored coins that make up `frac` of the total weight (the real population)."""
    order = np.argsort(-p)
    cw = np.cumsum(w[order])
    k = int(np.searchsorted(cw, frac * cw[-1])) + 1
    idx = order[:k]
    return {"k": k, "precision": float((w[idx] * y[idx]).sum() / w[idx].sum())}


def save_predictions(cfg: Config, name: str, df: pl.DataFrame, p: np.ndarray) -> None:
    """Test-set scores per model, so an ensemble can be evaluated without refitting anything."""
    out = cfg.processed_dir / "preds"
    out.mkdir(parents=True, exist_ok=True)
    df.select("mint").with_columns(p=pl.Series(np.asarray(p, dtype=np.float64))).write_parquet(out / f"{name}.parquet")


def evaluate(cfg: Config, df: pl.DataFrame, p: np.ndarray) -> dict:
    """df must carry label, entry_cost_sol, exit_net_sol (and in_zone for the slice, sample_weight for strata)."""
    y = df["label"].to_numpy().astype(int)
    cost = df["entry_cost_sol"].to_numpy()
    net = df["exit_net_sol"].to_numpy()
    out: dict = {
        "n": int(len(y)),
        "positives": int(y.sum()),
        "base_rate": float(y.mean()) if len(y) else None,
        "pr_auc": float(average_precision_score(y, p)) if y.sum() and (1 - y).sum() else None,
        "roc_auc": float(roc_auc_score(y, p)) if y.sum() and (1 - y).sum() else None,
        "precision_at": {str(f): precision_at(y, p, f) for f in cfg.metrics["top_fractions"]},
        "pnl_at": {str(f): pnl_at(f, p, cost, net) for f in cfg.metrics["top_fractions"]},
        "pnl_all_sol": float((net - cost).sum()),
    }
    if "sample_weight" in df.columns:
        w = df["sample_weight"].fill_null(1.0).to_numpy().astype(float)
        out["weighted"] = {
            "base_rate": float((w * y).sum() / w.sum()),
            "pr_auc": float(average_precision_score(y, p, sample_weight=w)) if y.sum() and (1 - y).sum() else None,
            "precision_at": {str(f): weighted_precision_at(y, p, w, f) for f in cfg.metrics["top_fractions"]},
        }
    slices = {c: df[c].fill_null(False).to_numpy().astype(bool) for c in ("in_zone", "active_at_entry") if c in df.columns}
    if "creator_prior_launches" in df.columns:
        slices["serial_launcher"] = df["creator_prior_launches"].fill_null(0).to_numpy() >= 3
    for slice_name, z in slices.items():
        if z.sum() >= 10 and y[z].sum() and (1 - y[z]).sum():
            drop = [c for c in ("in_zone", "active_at_entry", "creator_prior_launches") if c in df.columns]
            out[f"slice_{slice_name}"] = evaluate(cfg, df.filter(pl.Series(z)).drop(drop), p[z])
    return out


def human_row(cfg: Config) -> dict | None:
    h = read_json(cfg.reports_dir / "human_benchmark.json")
    return None if h is None else h.get("all")


def comparison_table(cfg: Config, results: dict[str, dict]) -> str:
    lines = [
        "| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for name, r in results.items():
        pa = r["precision_at"]
        pn = r["pnl_at"]
        lines.append(
            f"| {name} | {r['n']} | {r['pr_auc']:.3f} | {r['roc_auc']:.3f} | {pa['0.01']['precision']:.2f} | "
            f"{pa['0.05']['precision']:.2f} | {pa['0.1']['precision']:.2f} | "
            f"{pn['0.1']['pnl_sol']:.2f} | {pn['0.1']['pnl_ex_top3_sol']:.2f} |"
        )
    h = human_row(cfg)
    if h:
        lines.append(
            f"| human (M0, balanced 50/50) | {h['n']} | — | — | acc {h['accuracy']:.2f} | "
            f"prec {h['precision']:.2f} | rec {h['recall']:.2f} | — | — |"
        )
    else:
        lines.append("| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |")
    return "\n".join(lines)
