"""leakage — fail the build if any feature can see past the entry, or reads outcome through the back door.

Two passes over the processed features:
  1. Causality: every feature is recomputed after every trade at/after the window is deleted and the
     remaining post-window tape replaced by noise. The recomputed table must be identical.
  2. Window permutation (spec §9): each token's window is swapped for a random other token's window and
     the window-derived features recomputed; |corr(feature, label)| must be below `threshold` for all of
     them — a feature that still correlates is reading something other than the window.
Creator-history features are exempt from pass 2 (they are not window-derived) and are instead checked
by construction in tests/test_features.py.
"""

from __future__ import annotations

import logging

import numpy as np
import polars as pl

from pumpfun.config import Config
from pumpfun.features import sequence, tabular
from pumpfun.ingest.to_parquet import read_trades
from pumpfun.reports import write_json

log = logging.getLogger(__name__)

THRESHOLD = 0.05


def _corr(a: np.ndarray, b: np.ndarray) -> float:
    a = a.astype(float)
    b = b.astype(float)
    ok = np.isfinite(a)
    if ok.sum() < 10 or a[ok].std() == 0 or b[ok].std() == 0:
        return 0.0
    return float(np.corrcoef(a[ok], b[ok])[0, 1])


def run(cfg: Config) -> dict:
    feats = pl.read_parquet(cfg.processed_dir / "features.parquet")
    labels = pl.read_parquet(cfg.interim_dir / "labels.parquet").filter(pl.col("mint").is_in(feats["mint"].implode()))
    tokens = pl.read_parquet(cfg.tokens_path)
    trades = read_trades(cfg).filter(pl.col("mint").is_in(feats["mint"].implode()))
    wt = sequence.window_trades(cfg, trades, labels)
    window_cols = tabular.SHAPE + tabular.HOLDERS

    # --- pass 1: mutate everything after the window; features must not move
    rng = np.random.default_rng(cfg.seed)
    ranked = (
        trades.sort("mint", "slot", "slot_index")
        .with_columns(rank=pl.int_range(pl.len()).over("mint"))
        .join(labels.select("mint", "n_visible").lazy(), on="mint", how="inner")
        .collect()
    )
    post = ranked.filter(pl.col("rank") >= pl.col("n_visible")).drop("rank", "n_visible")
    noise = post.with_columns(
        sol_amount=pl.Series(rng.random(post.height) * 10),
        is_buy=pl.Series(rng.random(post.height) > 0.5),
        price_sol=pl.Series(rng.random(post.height) * 1e-6),
    )
    pre = ranked.filter(pl.col("rank") < pl.col("n_visible")).drop("rank", "n_visible")
    mutated = pl.concat([pre, noise]).lazy()
    wt2 = sequence.window_trades(cfg, mutated, labels)
    base = tabular.build(cfg, wt, labels, tokens).sort("mint")
    again = tabular.build(cfg, wt2, labels, tokens).sort("mint")
    diff = [c for c in window_cols if not np.allclose(base[c].to_numpy(), again[c].to_numpy(), equal_nan=True)]
    if diff:
        raise SystemExit(f"leakage: features changed when post-window trades were mutated: {diff}")

    # --- pass 2: swap windows between tokens
    mints = labels["mint"].to_list()
    perm = rng.permutation(len(mints))
    remap = dict(zip(mints, [mints[i] for i in perm], strict=True))
    swapped = wt.with_columns(pl.col("mint").replace_strict(remap))
    # entry_price / curve_sol_at_entry belong to the window, so they travel with it
    lab_sw = labels.with_columns(pl.col("mint").replace_strict(remap)).select(
        "mint", "entry_t", "entry_price", "n_visible", "curve_sol_at_entry", "in_zone", "launch_day", "label"
    )
    lab_sw = lab_sw.join(labels.select("mint", "label").rename({"label": "true_label"}), on="mint")
    perm_feats = tabular.build(cfg, swapped, lab_sw.drop("label").rename({"true_label": "label"}), tokens)
    y = perm_feats["label"].to_numpy()
    corrs = {c: _corr(perm_feats[c].to_numpy(), y) for c in window_cols}
    bad = {c: v for c, v in corrs.items() if abs(v) > THRESHOLD}
    report = {"threshold": THRESHOLD, "n": len(y), "permuted_window_corr": corrs, "violations": bad}
    write_json(cfg.reports_dir / "leakage_check.json", report)
    if bad:
        raise SystemExit(f"leakage: window-derived features correlate with the label after window permutation: {bad}")
    log.info("leakage check passed on %d tokens (max |corr| %.3f)", len(y), max(abs(v) for v in corrs.values()))
    return report
