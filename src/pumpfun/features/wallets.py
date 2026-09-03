"""wallets — what the early buyers' own histories say, from every tape in the archive.

For each (wallet, coin) the archive gives one event: the wallet's first buy on that coin, and whether the
coin's tape later reached `cross_level_sol` ("ran"). A coin's outcome is only known once its tape is
complete, `window + horizon` seconds after launch, so a decision at absolute time e may use:
  n_prior     events with first-buy time < e            (how many coins this wallet has been early in)
  n_resolved  events with resolution time < e           (how many of those have a known outcome)
  n_ran       resolved events whose coin ran
Per decision, those per-wallet counts are aggregated over the visible window's buyers. Every count is
strictly before e, and the coin being decided is removed from its own buyers' histories.

The archive is the stratified fetch, so wallet histories cover a weighted sample of launches, not all of
them; the features are ratios and log-counts, which survive that.
"""

from __future__ import annotations

import logging

import numpy as np
import polars as pl

from pumpfun.config import Config
from pumpfun.ingest.to_parquet import read_trades

log = logging.getLogger(__name__)

WALLETS = [
    "w_repeat_share",  # share of visible buyers seen early on >= 1 prior coin
    "w_serial_share",  # share of visible buyers seen early on >= 20 prior coins
    "w_log_prior_mean",  # mean log1p(prior coins) over visible buyers
    "w_hit_rate_mean",  # mean of (ran / resolved) over buyers with >= 3 resolved coins
    "w_hit_rate_max",  # best such buyer
    "w_hit_rate_sol",  # SOL-weighted hit rate over the same buyers
    "w_scored_share",  # share of visible buyers with >= 3 resolved coins (coverage of the read)
]
MIN_RESOLVED = 3
SERIAL_MIN = 20


def wallet_events(cfg: Config, tokens: pl.DataFrame) -> pl.DataFrame:
    """One row per (trader, mint): first buy time, and the coin's outcome with its resolution time."""
    level = float(cfg.raw.get("cross_level_sol", 0.0) or 0.0)
    resolve_after = float(cfg.window_seconds + cfg.horizon_seconds)
    t = read_trades(cfg)
    peaks = t.group_by("mint").agg(peak=pl.col("curve_sol_after").max())
    first = t.filter(pl.col("is_buy")).group_by("trader", "mint").agg(first_t=pl.col("block_time").min())
    ev = (
        first.join(peaks, on="mint", how="left")
        .join(tokens.select("mint", "launch_time").lazy(), on="mint", how="inner")
        .with_columns(
            ran=(pl.col("peak") >= level).fill_null(False).cast(pl.Float64),
            resolve_t=(pl.col("launch_time") + resolve_after).cast(pl.Float64),
            first_t=pl.col("first_t").cast(pl.Float64),
        )
        .select("trader", "mint", "first_t", "resolve_t", "ran")
        .collect()
    )
    log.info("wallet events: %d (trader, mint) first buys over %d wallets", ev.height, ev["trader"].n_unique())
    return ev


def _cum_by_time(ev: pl.DataFrame, time_col: str, value_cols: dict[str, pl.Expr]) -> pl.DataFrame:
    """Per trader, cumulative sums ordered by `time_col` (ties included), for as-of lookups."""
    return (
        ev.sort("trader", time_col)
        .with_columns([expr.cum_sum().over("trader").alias(name) for name, expr in value_cols.items()])
        .select("trader", time_col, *value_cols.keys())
    )


def wallet_features(cfg: Config, wt: pl.DataFrame, labels: pl.DataFrame, tokens: pl.DataFrame) -> pl.DataFrame:
    ev = wallet_events(cfg, tokens)
    one = pl.col("ran").is_not_null().cast(pl.Float64)  # a literal would collapse to a scalar under cum_sum
    by_first = _cum_by_time(ev, "first_t", {"n_prior": one})
    by_resolve = _cum_by_time(ev, "resolve_t", {"n_resolved": one, "n_ran": pl.col("ran")})

    entry_abs = labels.select("mint", "entry_t").join(tokens.select("mint", "launch_time"), on="mint", how="left")
    entry_abs = entry_abs.with_columns(e=(pl.col("launch_time") + pl.col("entry_t")).cast(pl.Float64)).select("mint", "e")
    buyers = (
        wt.filter(pl.col("is_buy"))
        .group_by("mint", "trader")
        .agg(sol=pl.col("sol_amount").sum())
        .join(entry_abs, on="mint", how="inner")
        # strictly before the decision: as-of joins look up the last row with time <= key
        .with_columns(key=pl.col("e") - 0.5)
        .sort("key")
    )
    # as-of by trader on the two cumulative tables
    p = buyers.join_asof(by_first.sort("first_t"), left_on="key", right_on="first_t", by="trader", strategy="backward")
    p = p.join_asof(by_resolve.sort("resolve_t"), left_on="key", right_on="resolve_t", by="trader", strategy="backward")
    p = p.with_columns(
        # the coin being decided is one of this wallet's prior first-buys (it is a visible buyer); remove it
        n_prior=(pl.col("n_prior").fill_null(0.0) - 1.0).clip(0.0, None),
        n_resolved=pl.col("n_resolved").fill_null(0.0),
        n_ran=pl.col("n_ran").fill_null(0.0),
    ).with_columns(
        scored=(pl.col("n_resolved") >= MIN_RESOLVED),
        hit=pl.when(pl.col("n_resolved") > 0).then(pl.col("n_ran") / pl.col("n_resolved")).otherwise(None),
    )
    agg = p.group_by("mint").agg(
        w_repeat_share=(pl.col("n_prior") >= 1).cast(pl.Float64).mean(),
        w_serial_share=(pl.col("n_prior") >= SERIAL_MIN).cast(pl.Float64).mean(),
        w_log_prior_mean=(pl.col("n_prior") + 1.0).log().mean(),
        w_hit_rate_mean=pl.col("hit").filter(pl.col("scored")).mean(),
        w_hit_rate_max=pl.col("hit").filter(pl.col("scored")).max(),
        w_hit_rate_sol=(
            (pl.col("hit") * pl.col("sol")).filter(pl.col("scored")).sum() / pl.col("sol").filter(pl.col("scored")).sum()
        ),
        w_scored_share=pl.col("scored").cast(pl.Float64).mean(),
    )
    out = labels.select("mint").join(agg, on="mint", how="left")
    cov = float(np.mean(out["w_scored_share"].fill_null(0.0).to_numpy() > 0)) if out.height else 0.0
    log.info("wallet features: %d decisions, %.0f%% with at least one scored buyer", out.height, 100 * cov)
    return out
