"""tabular — what a pair of eyes (and a holder scanner) sees at the decision moment, as numbers.

Three groups, kept separate so each can be evaluated alone (spec §10 + handoff §0):
  shape     the chart's texture from the window's trades (spec list + the trading repo's shape features)
  holders   the holder graph at the decision moment, from per-wallet net balances (features.ts::holderFeatures)
  creator   the creator's history using ONLY launches strictly before this launch, and only outcomes
            that were resolved before it (spec §9)
Side columns (curve_sol_at_entry, in_zone) travel along for slicing, not as model input by default.
"""

from __future__ import annotations

import math
from collections import defaultdict

import numpy as np
import polars as pl

from pumpfun.config import Config
from pumpfun.ingest.to_parquet import curve_params

SHAPE = [
    "n_trades",
    "n_buyers",
    "n_sellers",
    "buy_ratio_count",
    "buy_ratio_sol",
    "largest_buy_share",
    "gini_buy_size",
    "price_slope",
    "volume_slope",
    "time_to_10_trades",
    "iti_median",
    "iti_std",
    "iti_cv",
    "bundle_slots",
    "max_drawdown",
    "lows",
    "lows_per_min",
    "step_gini",
    "buy_size_cv",
    "sol_last60",
    "trades_last60",
    "buyers_last60",
    "sellers_last60",
    "biggest_buy_vs_curve",
    "run_from_low",
    "from_peak",
    "log_ret_window",
    "sell_share_sol",
    "n_slots",
    "first_trade_t",
    "last_trade_t",
]
HOLDERS = [
    "holders_n",
    "buyers_n",
    "top1_share",
    "top3_share",
    "top10_share",
    "dev_share",
    "dev_sold",
    "gini_hold",
    "first_slot_share",
    "launch_bundle_share",
    "same_size_share",
    "exited_share",
    "tokens_out_pct",
]
CREATOR = ["creator_prior_launches", "creator_prior_resolved", "creator_prior_tp_rate"]
# v1.5: causal context that is not the meme itself (spec §7 keeps name/image out of v1).
CONTEXT = ["is_native_launch", "hour_sin", "hour_cos", "replies_at_entry", "live_at_entry"]
SIDE = ["curve_sol_at_entry", "in_zone", "active_at_entry"]
GROUPS = {"shape": SHAPE, "holders": HOLDERS, "creator": CREATOR, "context": CONTEXT}
NATIVE_HOSTS = {"ipfs.io", "pump.mypinata.cloud"}


def gini(xs: list[float]) -> float:
    s = sorted(x for x in xs if x > 0)
    n = len(s)
    if n < 2:
        return 0.0
    cum = 0.0
    acc = 0.0
    for v in s:
        cum += v
        acc += cum
    return (n + 1 - 2 * acc / cum) / n if cum > 0 else 0.0


def cv(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    if m <= 0:
        return 0.0
    v = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return math.sqrt(v) / m


def slope(y: list[float], t: list[float]) -> float:
    if len(y) < 2:
        return 0.0
    a = np.asarray(t, dtype=float)
    b = np.asarray(y, dtype=float)
    a = a - a.mean()
    den = float((a * a).sum())
    return float((a * (b - b.mean())).sum() / den) if den > 0 else 0.0


def shape_and_holders(
    cfg: Config, rows: list[tuple], creator: str, curve_sol_at_entry: float, entry_price: float, window_s: float
) -> dict:
    """One token's visible tape: rows = (t_s, slot, is_buy, sol, tokens, trader, price_sol) in order."""
    p = curve_params(cfg)
    w = max(window_s, 1.0)
    n = len(rows)
    buys = [r for r in rows if r[2]]
    sells = [r for r in rows if not r[2]]
    buy_sol = sum(r[3] for r in buys)
    sell_sol = sum(r[3] for r in sells)
    total_sol = buy_sol + sell_sol
    t_end = rows[-1][0]
    # --- shape
    times = [r[0] for r in rows]
    prices = [r[6] for r in rows]
    itis = [max(0.0, times[i] - times[i - 1]) for i in range(1, n)]
    peak = 0.0
    max_dd = 0.0
    lows = 0
    state = "up"
    local_high, local_low = 0.0, math.inf
    ups: list[float] = []
    min_p, max_p = math.inf, 0.0
    for i, s in enumerate(prices):
        if i > 0 and prices[i - 1] > 0 and s > 0:
            lr = math.log(s / prices[i - 1])
            if lr > 0:
                ups.append(lr)
        peak = max(peak, s)
        max_dd = max(max_dd, 1 - s / peak if peak > 0 else 0.0)
        min_p, max_p = min(min_p, s), max(max_p, s)
        if state == "up":
            local_high = max(local_high, s)
            if s <= local_high * 0.95:
                state, local_low = "down", s
        else:
            local_low = min(local_low, s)
            if s >= local_low * 1.05:
                lows += 1
                state, local_high = "up", s
    last60 = [r for r in rows if t_end - r[0] <= 60]
    slots = defaultdict(set)
    for r in buys:
        slots[r[1]].add(r[5])
    # coarse volume slope over 10 bins
    nb = 10
    vol_bins = [0.0] * nb
    for r in rows:
        vol_bins[max(0, min(nb - 1, int(r[0] * nb / w)))] += r[3]
    shape = {
        "n_trades": n,
        "n_buyers": len({r[5] for r in buys}),
        "n_sellers": len({r[5] for r in sells}),
        "buy_ratio_count": len(buys) / n,
        "buy_ratio_sol": buy_sol / total_sol if total_sol > 0 else 0.0,
        "largest_buy_share": (max((r[3] for r in buys), default=0.0) / total_sol) if total_sol > 0 else 0.0,
        "gini_buy_size": gini([r[3] for r in buys]),
        "price_slope": slope([math.log(x) for x in prices if x > 0], [t for t, x in zip(times, prices, strict=True) if x > 0]),
        "volume_slope": slope(vol_bins, list(range(nb))),
        "time_to_10_trades": rows[9][0] if n >= 10 else float(w),
        "iti_median": float(np.median(itis)) if itis else float(w),
        "iti_std": float(np.std(itis)) if itis else 0.0,
        "iti_cv": cv(itis),
        "bundle_slots": sum(1 for s in slots.values() if len(s) >= 2),
        "max_drawdown": max_dd,
        "lows": lows,
        "lows_per_min": lows / max(t_end, 1.0) * 60,
        "step_gini": gini(ups),
        "buy_size_cv": cv([r[3] for r in buys]),
        "sol_last60": sum(r[3] if r[2] else -r[3] for r in last60),
        "trades_last60": len(last60),
        "buyers_last60": len({r[5] for r in last60 if r[2]}),
        "sellers_last60": len({r[5] for r in last60 if not r[2]}),
        "biggest_buy_vs_curve": (max((r[3] for r in buys), default=0.0) / curve_sol_at_entry) if curve_sol_at_entry > 0 else 0.0,
        "run_from_low": prices[-1] / min_p if min_p > 0 else 1.0,
        "from_peak": prices[-1] / max_p if max_p > 0 else 1.0,
        "log_ret_window": math.log(prices[-1] / prices[0]) if prices[0] > 0 and prices[-1] > 0 else 0.0,
        "sell_share_sol": sell_sol / total_sol if total_sol > 0 else 0.0,
        "n_slots": len({r[1] for r in rows}),
        "first_trade_t": rows[0][0],
        "last_trade_t": t_end,
    }
    # --- holders (per-wallet net balances inside the window)
    bal: dict[str, float] = defaultdict(float)
    peak_bal: dict[str, float] = defaultdict(float)
    first_slot: dict[str, int] = {}
    first_sol: dict[str, float] = {}
    size_count: dict[int, int] = defaultdict(int)
    slot0 = rows[0][1]
    for _t_s, slot, is_buy, sol, tokens, trader, _px in rows:
        if trader not in first_slot:
            first_slot[trader] = slot
            first_sol[trader] = sol if is_buy else 0.0
            if is_buy:
                size_count[round(sol * 1000)] += 1
        if is_buy:
            bal[trader] += tokens
            peak_bal[trader] = max(peak_bal[trader], bal[trader])
        else:
            bal[trader] = max(0.0, bal[trader] - tokens)
    tokens_out = sum(bal.values())
    bals = sorted((b for b in bal.values() if b >= 1), reverse=True)
    buyers_n = sum(1 for tr in peak_bal if peak_bal[tr] > 0)
    exited = sum(1 for tr in peak_bal if peak_bal[tr] > 0 and bal[tr] < 0.1 * peak_bal[tr])

    def share(pred) -> float:
        return sum(b for tr, b in bal.items() if pred(tr)) / tokens_out if tokens_out > 0 else 0.0

    holders = {
        "holders_n": len(bals),
        "buyers_n": buyers_n,
        "top1_share": sum(bals[:1]) / tokens_out if tokens_out > 0 else 0.0,
        "top3_share": sum(bals[:3]) / tokens_out if tokens_out > 0 else 0.0,
        "top10_share": sum(bals[:10]) / tokens_out if tokens_out > 0 else 0.0,
        "dev_share": bal.get(creator, 0.0) / tokens_out if tokens_out > 0 else 0.0,
        "dev_sold": 1.0 if peak_bal.get(creator, 0.0) > 0 and bal.get(creator, 0.0) < 0.5 * peak_bal[creator] else 0.0,
        "gini_hold": gini(bals),
        "first_slot_share": share(lambda tr: first_slot[tr] == slot0),
        "launch_bundle_share": share(lambda tr: first_slot[tr] <= slot0 + 1),
        "same_size_share": share(lambda tr: size_count.get(round(first_sol[tr] * 1000), 0) >= 3),
        "exited_share": exited / buyers_n if buyers_n else 0.0,
        "tokens_out_pct": tokens_out / (p.initial_real_token / p.raw_per_token),
    }
    return {**shape, **holders}


def creator_history(cfg: Config, tokens: pl.DataFrame, labels: pl.DataFrame) -> pl.DataFrame:
    """Per labeled token: the creator's launches strictly before it, and the TP rate of those already resolved."""
    horizon = cfg.horizon_seconds
    t = tokens.select("mint", "creator", "launch_time").sort("creator", "launch_time")
    lab = labels.select("mint", "label", "entry_t").join(t, on="mint", how="left")
    lab = lab.with_columns(resolved_at=pl.col("launch_time") + pl.col("entry_t").cast(pl.Int64) + horizon)
    out = []
    by_creator_launch = {c: g["launch_time"].to_list() for c, g in t.group_by("creator", maintain_order=True)}  # noqa: B905
    by_creator_res = {
        c: sorted(zip(g["resolved_at"].to_list(), g["label"].to_list(), strict=True))
        for c, g in lab.group_by("creator", maintain_order=True)
    }
    import bisect

    for mint, creator, launch in lab.select("mint", "creator", "launch_time").iter_rows():
        c = creator if isinstance(creator, str) else creator[0]
        launches = by_creator_launch.get(c) or by_creator_launch.get((c,)) or []
        prior = bisect.bisect_left(launches, launch)
        res = by_creator_res.get(c) or by_creator_res.get((c,)) or []
        k = bisect.bisect_left(res, (launch, -1))
        resolved = res[:k]
        out.append(
            {
                "mint": mint,
                "creator_prior_launches": prior,
                "creator_prior_resolved": len(resolved),
                "creator_prior_tp_rate": (sum(lbl for _, lbl in resolved) / len(resolved)) if resolved else None,
            }
        )
    return pl.DataFrame(out)


def context_features(cfg: Config, tokens: pl.DataFrame) -> pl.DataFrame:
    """Launch origin, launch hour (periodic), platform attention frozen strictly before the entry."""
    strata_path = cfg.interim_dir / "strata.parquet"
    att = (
        pl.read_parquet(strata_path).select("mint", "replies_at_entry", "live_at_entry")
        if strata_path.exists() and "replies_at_entry" in pl.read_parquet_schema(strata_path)
        else pl.DataFrame(schema={"mint": pl.String, "replies_at_entry": pl.Int64, "live_at_entry": pl.Boolean})
    )
    two_pi = 2 * math.pi
    return (
        tokens.select("mint", "launch_time", "meta_host")
        .with_columns(
            is_native_launch=pl.col("meta_host").is_in(sorted(NATIVE_HOSTS)).cast(pl.Float64),
            hour=(pl.from_epoch("launch_time").dt.replace_time_zone("UTC").dt.convert_time_zone(cfg.split_timezone).dt.hour()),
        )
        .with_columns(
            hour_sin=(pl.col("hour") * two_pi / 24).sin(),
            hour_cos=(pl.col("hour") * two_pi / 24).cos(),
        )
        .join(att, on="mint", how="left")
        .with_columns(live_at_entry=pl.col("live_at_entry").cast(pl.Float64))
        .select("mint", "is_native_launch", "hour_sin", "hour_cos", "replies_at_entry", "live_at_entry")
    )


def build(cfg: Config, wt: pl.DataFrame, labels: pl.DataFrame, tokens: pl.DataFrame) -> pl.DataFrame:
    meta = {
        m: (c, s, e, t)
        for m, c, s, e, t in labels.join(tokens.select("mint", "creator"), on="mint", how="left")
        .select("mint", "creator", "curve_sol_at_entry", "entry_price", "entry_t")
        .iter_rows()
    }
    rows = []
    cols = ["seconds_since_launch", "slot", "is_buy", "sol_amount", "token_amount", "trader", "price_sol"]
    for (mint,), g in wt.group_by("mint", maintain_order=True):
        creator, sol_at_entry, entry_price, entry_t = meta[mint]
        feats = shape_and_holders(cfg, list(g.select(cols).iter_rows()), creator, sol_at_entry, entry_price, entry_t)
        rows.append({"mint": mint, "entry_t_": entry_t, **feats})
    df = (
        pl.DataFrame(rows)
        .join(creator_history(cfg, tokens, labels), on="mint", how="left")
        .join(context_features(cfg, tokens), on="mint", how="left")
    )
    df = df.with_columns(
        active_at_entry=(pl.col("last_trade_t") >= pl.col("entry_t_") - float(cfg.metrics["active_silence_max"]))
    ).drop("entry_t_")
    side = labels.select("mint", "label", "launch_day", "curve_sol_at_entry", pl.col("in_zone").cast(pl.Float64))
    return side.join(df, on="mint", how="inner")
