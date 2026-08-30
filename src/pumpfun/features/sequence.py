"""sequence — the window as a fixed-length, scale-free 6-channel tensor (spec §7).

Channels per step (window resampled to `resample_steps` bins, 1 s at defaults):
  0  log(price / entry_price)        last spot in the bin, forward-filled from the launch price
  1  volume share                    SOL traded in the bin / SOL traded in the whole window
  2  trade count
  3  unique buyers
  4  buy/sell imbalance by SOL       (buy - sell) / (buy + sell), 0 when the bin is empty
  5  curve fill fraction             real SOL in the curve / graduation SOL, forward-filled

Only trades with seconds_since_launch < window_seconds enter; that is asserted
against the entry time of every token (features are strictly causal).
"""

from __future__ import annotations

import numpy as np
import polars as pl

from pumpfun.config import Config
from pumpfun.ingest.to_parquet import curve_params
from pumpfun.label import curve_sim as cs

CHANNELS = ["log_price", "volume_share", "trade_count", "unique_buyers", "imbalance", "curve_fill"]


def launch_price(cfg: Config) -> float:
    p = curve_params(cfg)
    return cs.initial_reserves(p).spot_sol_per_token(p.raw_per_token)


def graduation_sol(cfg: Config) -> float:
    """Real SOL in the curve when the last real token is sold, from the curve maths (not a hardcoded 85)."""
    p = curve_params(cfg)
    c0 = cs.initial_reserves(p)
    return cs.buy_quote_in(c0, p.initial_real_token) / cs.LAMPORTS_PER_SOL


def window_trades(cfg: Config, trades: pl.LazyFrame, labels: pl.DataFrame) -> pl.DataFrame:
    """Trades strictly inside the feature window, joined to the entry so causality can be asserted."""
    w = cfg.window_seconds
    lab = labels.select("mint", "entry_t", "entry_price").lazy()
    df = (
        trades.join(lab, on="mint", how="inner")
        .filter(pl.col("seconds_since_launch") < w)
        .sort("mint", "slot", "slot_index")
        .collect()
    )
    late = df.filter(pl.col("seconds_since_launch") >= pl.col("entry_t"))
    if late.height:
        raise AssertionError(f"{late['mint'].n_unique()} tokens have window trades at/after their entry — not causal")
    return df


def encode(cfg: Config, wt: pl.DataFrame, labels: pl.DataFrame) -> tuple[np.ndarray, list[str]]:
    """Dense [N, steps, 6] float32 in the order of `labels.mint`."""
    steps = cfg.resample_steps
    w = cfg.window_seconds
    mints = labels["mint"].to_list()
    pos = {m: i for i, m in enumerate(mints)}
    entry_price = dict(labels.select("mint", "entry_price").iter_rows())
    p0 = launch_price(cfg)
    grad = graduation_sol(cfg)

    x = np.zeros((len(mints), steps, len(CHANNELS)), dtype=np.float32)
    # Channel 0/5 need forward fill; start from the launch state.
    for m, ep in entry_price.items():
        x[pos[m], :, 0] = np.log(p0 / ep)

    binned = (
        wt.with_columns(b=(pl.col("seconds_since_launch") * steps / w).floor().cast(pl.Int32).clip(0, steps - 1))
        .group_by("mint", "b")
        .agg(
            last_price=pl.col("price_sol").last(),
            last_fill=pl.col("curve_sol_after").last(),
            vol=pl.col("sol_amount").sum(),
            n=pl.len(),
            buyers=pl.col("trader").filter(pl.col("is_buy")).n_unique(),
            buy_sol=pl.col("sol_amount").filter(pl.col("is_buy")).sum(),
            sell_sol=pl.col("sol_amount").filter(~pl.col("is_buy")).sum(),
        )
        .join(wt.group_by("mint").agg(total=pl.col("sol_amount").sum()), on="mint")
        .sort("mint", "b")
    )
    for m, b, lp, lf, vol, n, buyers, bs, ss, total in binned.iter_rows():
        i = pos[m]
        x[i, b, 0] = np.log(lp / entry_price[m]) if lp > 0 else x[i, b, 0]
        x[i, b, 1] = vol / total if total > 0 else 0.0
        x[i, b, 2] = n
        x[i, b, 3] = buyers
        x[i, b, 4] = (bs - ss) / (bs + ss) if (bs + ss) > 0 else 0.0
        x[i, b, 5] = (lf / grad) if lf is not None else 0.0
    # forward-fill channels 0 and 5 across empty bins
    for ch in (0, 5):
        has = np.zeros((len(mints), steps), dtype=bool)
        for m, b, *_ in binned.select("mint", "b").iter_rows():
            has[pos[m], b] = True
        idx = np.where(has, np.arange(steps)[None, :], -1)
        idx = np.maximum.accumulate(idx, axis=1)
        filled = np.take_along_axis(x[:, :, ch], np.clip(idx, 0, None), axis=1)
        x[:, :, ch] = np.where(idx >= 0, filled, x[:, :, ch])
    return x, mints
