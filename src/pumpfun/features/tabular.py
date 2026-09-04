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
from pumpfun.features.wallets import WALLETS, wallet_features
from pumpfun.ingest.to_parquet import curve_params
from pumpfun.label import curve_sim as cs
from pumpfun.label.first_sight import first_seen_level

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
    # v1.6: speed, composition and the decision moment itself
    "decision_age_s",  # seconds from launch to the decision (cross mode: how fast the level was reached)
    "curve_sol_in",  # real SOL in the curve at the decision, as a model input
    "sol_per_s_window",  # net SOL inflow per second over the whole visible window
    "inflow_accel",  # net inflow rate over the last 30 s divided by the window rate
    "round_size_share",  # share of buys at a preset size (0.05/0.1/0.2/0.25/0.5/1/2 SOL): bots and buttons
    "flip_latency_med",  # median seconds from a wallet's first buy to its first sell (window cap if none)
    "flipper_share",  # share of buyers that sold anything inside the window
    "dev_buy_sol",  # the creator's total buy size in SOL
]
ROUND_SIZES = {50, 100, 200, 250, 500, 1000, 2000}  # in thousandths of a SOL
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
CONTEXT = [
    "is_native_launch",
    "hour_sin",
    "hour_cos",
    "replies_at_entry",
    "live_at_entry",
    "market_recent_tp_rate",
    "market_recent_n",
    "market_launch_rate",
    "market_candidate_rate",
    # create metadata, non-semantic (null for historical tokens without a sweep record)
    "has_twitter",
    "has_telegram",
    "has_website",
    "twitter_is_status",
    "description_len",
    "name_dup_24h",
    "image_dup_24h",
    "dow_sin",
    "dow_cos",
]
META_COLS = [
    "has_twitter",
    "has_telegram",
    "has_website",
    "twitter_is_status",
    "description_len",
    "name_dup_24h",
    "image_dup_24h",
]
# What the paper bot can compute live at a crossing without a per-trade tape: reserve-series shape,
# speed, the decision moment, and its own holder pull. Served as model "xgb_botlive" (v0 book).
# The bot first sees a curve where its scanner ranks it (3-6 SOL raised) and anchors the series at the
# launch state, so its path features see only [launch anchor] + [first sight .. decision]. Training
# renders the same truncation ("bl_" columns) from a first-sight level sampled per coin; the bot sends
# its actual level as first_seen_sol.
BOTLIVE_NAMES = [
    "price_slope",
    "max_drawdown",
    "lows",
    "lows_per_min",
    "run_from_low",
    "from_peak",
    "log_ret_window",
    "sol_per_s_window",
    "inflow_accel",
    "sol_last60",
    "trades_last60",
    "decision_age_s",
    "curve_sol_in",
    "top10_share",
    "dev_buy_sol",  # creator's launch buy in SOL: exact live and in the tape; dev_share is pre-dump here, post-dump live
    "first_seen_sol",  # real SOL in the curve when the bot first sighted it (its own key)
]
BOTLIVE = [f"bl_{n}" for n in BOTLIVE_NAMES]


def botlive_series(rows: list[tuple], curve_sol: list[float], level: float, p0: float) -> list[tuple[float, float, float]]:
    """The bot's view of a tape as (t, price, real_sol) samples: one per slot-write of the curve account
    (the last state in each slot), starting at the first slot after which the curve held >= level, plus
    the launch anchor (t=0, start price, 0 SOL). Below-level history before first sight is invisible."""
    by_slot: dict[int, tuple[float, float, float]] = {}
    order: list[int] = []
    for r, c in zip(rows, curve_sol, strict=True):
        slot = int(r[1])
        if slot not in by_slot:
            order.append(slot)
        by_slot[slot] = (float(r[0]), float(r[6]), float(c) if c is not None else 0.0)
    samples = [by_slot[sl] for sl in order]
    k = next((i for i, smp in enumerate(samples) if smp[2] >= level), None)
    tail = samples if k is None else samples[k:]
    return [(0.0, p0, 0.0), *tail]


def botlive_features(
    cfg: Config, rows: list[tuple], curve_sol: list[float], creator: str, entry_t: float, level: float, top10_share: float
) -> dict:
    """Branch 2's exact live semantics over the bot-view series; holder read and launch buy from their own sources."""
    p = curve_params(cfg)
    p0 = cs.initial_reserves(p).spot_sol_per_token(p.raw_per_token)
    ser = botlive_series(rows, curve_sol, level, p0)
    T = max(float(entry_t), 1.0)
    ts = [x[0] for x in ser]
    ps = [x[1] for x in ser]
    ss = [x[2] for x in ser]
    s_now = ss[-1]

    def sol_at_or_before(t_cut: float) -> float:
        v = 0.0
        for t_, _, sol in ser:
            if t_ <= t_cut:
                v = sol
            else:
                break
        return v

    rate_w = s_now / T
    net_30 = s_now - sol_at_or_before(T - 30.0)
    # lows / drawdown / run / peak on the sampled price path
    peak, max_dd, lows = 0.0, 0.0, 0
    state, local_high, local_low = "up", 0.0, math.inf
    for px in ps:
        peak = max(peak, px)
        max_dd = max(max_dd, 1 - px / peak if peak > 0 else 0.0)
        if state == "up":
            local_high = max(local_high, px)
            if px <= local_high * 0.95:
                state, local_low = "down", px
        else:
            local_low = min(local_low, px)
            if px >= local_low * 1.05:
                lows += 1
                state, local_high = "up", px
    dev_first_buy = next((float(r[3]) for r in rows if r[2] and r[5] == creator), 0.0)
    return {
        "bl_price_slope": slope([math.log(x) for x in ps if x > 0], [t_ for t_, x in zip(ts, ps, strict=True) if x > 0]),
        "bl_max_drawdown": max_dd,
        "bl_lows": lows,
        "bl_lows_per_min": lows / T * 60,
        "bl_run_from_low": ps[-1] / min(ps) if min(ps) > 0 else 1.0,
        "bl_from_peak": ps[-1] / max(ps) if max(ps) > 0 else 1.0,
        "bl_log_ret_window": math.log(ps[-1] / ps[0]) if ps[0] > 0 and ps[-1] > 0 else 0.0,
        "bl_sol_per_s_window": rate_w,
        "bl_inflow_accel": max(-20.0, min(20.0, (net_30 / 30.0) / max(rate_w, 0.005))),
        "bl_sol_last60": s_now - sol_at_or_before(T - 60.0),
        "bl_trades_last60": sum(1 for t_ in ts if T - 60.0 < t_ <= T),
        "bl_decision_age_s": T,
        "bl_curve_sol_in": s_now,
        "bl_top10_share": top10_share,
        "bl_dev_buy_sol": dev_first_buy,
        "bl_first_seen_sol": level,
    }


SIDE = ["curve_sol_at_entry", "in_zone", "active_at_entry"]
GROUPS = {"shape": SHAPE, "holders": HOLDERS, "creator": CREATOR, "context": CONTEXT, "wallets": WALLETS}
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
    # --- speed, composition, decision moment
    net_window = buy_sol - sell_sol
    last30 = [r for r in rows if w - r[0] <= 30]
    net_30 = sum(r[3] if r[2] else -r[3] for r in last30)
    rate_w = net_window / w
    first_buy_t: dict[str, float] = {}
    first_sell_t: dict[str, float] = {}
    for r in rows:
        if r[2]:
            first_buy_t.setdefault(r[5], r[0])
        elif r[5] in first_buy_t:
            first_sell_t.setdefault(r[5], r[0])
    flips = [first_sell_t[tr] - first_buy_t[tr] for tr in first_sell_t]
    shape.update(
        {
            "decision_age_s": float(w),
            "curve_sol_in": float(curve_sol_at_entry),
            "sol_per_s_window": rate_w,
            # bounded: quiet windows explode the ratio
            "inflow_accel": max(-20.0, min(20.0, (net_30 / 30.0) / max(rate_w, 0.005))),
            "round_size_share": (sum(1 for r in buys if round(r[3] * 1000) in ROUND_SIZES) / len(buys)) if buys else 0.0,
            "flip_latency_med": float(np.median(flips)) if flips else float(w),
            "flipper_share": len(first_sell_t) / len(first_buy_t) if first_buy_t else 0.0,
            "dev_buy_sol": sum(r[3] for r in buys if r[5] == creator),
        }
    )
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
        c = creator if isinstance(creator, str) else (creator[0] if creator else None)
        if c is None:
            # Historical sources carry no creator: history is unknown, not zero.
            out.append(
                {
                    "mint": mint,
                    "creator_prior_launches": None,
                    "creator_prior_resolved": None,
                    "creator_prior_tp_rate": None,
                }
            )
            continue
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
    meta_path = cfg.raw_dir / "token_meta.parquet"
    meta = (
        pl.read_parquet(meta_path).select("mint", *META_COLS)
        if meta_path.exists()
        else pl.DataFrame(schema={"mint": pl.String, **{c: pl.Float64 for c in META_COLS}})
    )
    two_pi = 2 * math.pi
    local = pl.from_epoch("launch_time").dt.replace_time_zone("UTC").dt.convert_time_zone(cfg.split_timezone)
    return (
        tokens.select("mint", "launch_time", "meta_host")
        .with_columns(
            is_native_launch=pl.col("meta_host").is_in(sorted(NATIVE_HOSTS)).cast(pl.Float64),
            hour=local.dt.hour(),
            dow=local.dt.weekday(),
        )
        .with_columns(
            hour_sin=(pl.col("hour") * two_pi / 24).sin(),
            hour_cos=(pl.col("hour") * two_pi / 24).cos(),
            dow_sin=(pl.col("dow") * two_pi / 7).sin(),
            dow_cos=(pl.col("dow") * two_pi / 7).cos(),
        )
        .join(att, on="mint", how="left")
        .join(meta, on="mint", how="left")
        .with_columns(live_at_entry=pl.col("live_at_entry").cast(pl.Float64))
        .select(
            "mint",
            "is_native_launch",
            "hour_sin",
            "hour_cos",
            "dow_sin",
            "dow_cos",
            "replies_at_entry",
            "live_at_entry",
            *META_COLS,
        )
    )


def market_heat(cfg: Config, labels: pl.DataFrame, tokens: pl.DataFrame) -> pl.DataFrame:
    """The trenches dial: weighted TP rate of decisions whose outcome RESOLVED inside the window
    ending at this coin's entry moment. Deployment-causal: those outcomes are known by then."""
    strata_path = cfg.interim_dir / "strata.parquet"
    w = (
        pl.read_parquet(strata_path).select("mint", "weight")
        if strata_path.exists()
        else labels.select("mint").with_columns(weight=pl.lit(1.0))
    )
    df = (
        labels.select("mint", "entry_t", "exit_t", "label")
        .join(tokens.select("mint", "launch_time"), on="mint", how="left")
        .join(w, on="mint", how="left")
        .with_columns(
            entry_abs=pl.col("launch_time") + pl.col("entry_t"),
            resolved_abs=pl.col("launch_time") + pl.col("exit_t"),
            wgt=pl.col("weight").fill_null(1.0),
        )
    )
    win = cfg.market_heat_window_hours * 3600
    resolved = df.sort("resolved_abs")
    r_abs = resolved["resolved_abs"].to_numpy()
    r_w = resolved["wgt"].to_numpy()
    r_wy = (resolved["wgt"] * resolved["label"]).to_numpy()
    import numpy as np

    cw = np.concatenate([[0.0], np.cumsum(r_w)])
    cwy = np.concatenate([[0.0], np.cumsum(r_wy)])
    out_rate, out_n = [], []
    for e in df["entry_abs"].to_numpy():
        hi = np.searchsorted(r_abs, e, side="left")
        lo = np.searchsorted(r_abs, e - win, side="left")
        wsum = cw[hi] - cw[lo]
        out_rate.append(float((cwy[hi] - cwy[lo]) / wsum) if wsum > 0 else None)
        out_n.append(float(hi - lo))
    return df.select("mint").with_columns(
        market_recent_tp_rate=pl.Series(out_rate, dtype=pl.Float64),
        market_recent_n=pl.Series(out_n, dtype=pl.Float64),
    )


UNQUEUED_STRATA = {"no_inflow", "mayhem"}


def market_state(cfg: Config, labels: pl.DataFrame, tokens: pl.DataFrame) -> pl.DataFrame:
    """Two more dials on the trenches, measured the same way in every era:
    market_launch_rate     launches per hour in the window ending at this coin's entry moment, over the
                           whole universe; Dune days were sampled server-side, so those rows carry their
                           pre-sampling weight (bitquery_screen.pre_weight), everything else weight 1
    market_candidate_rate  weighted share of fetched launches whose tape reached cross_level_sol, over
                           launches old enough (window + horizon before the entry) for the whole tape to
                           be in the past; weights are the pre-screen selection weights (strata.weight)
    """
    import numpy as np

    from pumpfun.ingest.to_parquet import read_trades

    screen_path = cfg.interim_dir / "bitquery_screen.parquet"
    pre = (
        pl.read_parquet(screen_path).filter(pl.col("pre_sampled").fill_null(False)).select("mint", pre_w=pl.col("pre_weight"))
        if screen_path.exists()
        else pl.DataFrame(schema={"mint": pl.String, "pre_w": pl.Float64})
    )
    uni = (
        tokens.select("mint", "launch_time")
        .join(pre, on="mint", how="left")
        .with_columns(wgt=pl.col("pre_w").fill_null(1.0))
        .sort("launch_time")
    )
    l_abs = uni["launch_time"].to_numpy().astype(np.float64)
    cw = np.concatenate([[0.0], np.cumsum(uni["wgt"].to_numpy())])

    strata_path = cfg.interim_dir / "strata.parquet"
    # Fetched, pre-screen-selected launches carry their selection weight; launches in strata that are never
    # queued (no inflow, mayhem) count as "never reached" with weight 1. Selected-but-not-yet-fetched
    # launches are left out of both numerator and denominator, so fetch progress cannot bias the rate.
    if strata_path.exists():
        st = pl.read_parquet(strata_path).select("mint", "stratum", "selected", "weight")
        sel = st.filter(pl.col("selected")).select("mint", "weight")
        unqueued = st.filter(~pl.col("selected") & pl.col("stratum").is_in(sorted(UNQUEUED_STRATA))).select("mint")
    else:
        sel = tokens.select("mint").with_columns(weight=pl.lit(1.0))
        unqueued = tokens.head(0).select("mint")
    level = float(cfg.raw.get("cross_level_sol", 0.0) or 0.0)
    peaks = read_trades(cfg).group_by("mint").agg(peak=pl.col("curve_sol_after").max()).collect()
    fetched = (
        pl.concat(
            [
                peaks.join(sel, on="mint", how="inner")
                .with_columns(
                    reached=(pl.col("peak") >= level).fill_null(False).cast(pl.Float64),
                    weight=pl.col("weight").fill_null(1.0).fill_nan(1.0),
                )
                .select("mint", "weight", "reached"),
                unqueued.with_columns(weight=pl.lit(1.0), reached=pl.lit(0.0)),
            ]
        )
        .join(tokens.select("mint", "launch_time"), on="mint", how="left")
        .sort("launch_time")
    )
    f_abs = fetched["launch_time"].to_numpy().astype(np.float64)
    fw = np.concatenate([[0.0], np.cumsum(fetched["weight"].to_numpy())])
    fwr = np.concatenate([[0.0], np.cumsum((fetched["weight"] * fetched["reached"]).to_numpy())])

    win = cfg.market_heat_window_hours * 3600
    known_lag = float(cfg.window_seconds + cfg.horizon_seconds)
    df = labels.select("mint", "entry_t").join(tokens.select("mint", "launch_time"), on="mint", how="left")
    rate, cand = [], []
    for e in (df["launch_time"] + df["entry_t"]).to_numpy():
        hi = np.searchsorted(l_abs, e, side="left")
        lo = np.searchsorted(l_abs, e - win, side="left")
        rate.append(float((cw[hi] - cw[lo]) / cfg.market_heat_window_hours))
        khi = np.searchsorted(f_abs, e - known_lag, side="left")
        klo = np.searchsorted(f_abs, e - known_lag - win, side="left")
        n = fw[khi] - fw[klo]
        cand.append(float((fwr[khi] - fwr[klo]) / n) if n > 0 else None)
    return df.select("mint").with_columns(
        market_launch_rate=pl.Series(rate, dtype=pl.Float64),
        market_candidate_rate=pl.Series(cand, dtype=pl.Float64),
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
        tup = list(g.select(cols).iter_rows())
        feats = shape_and_holders(cfg, tup, creator, sol_at_entry, entry_price, entry_t)
        level = first_seen_level(cfg, mint)
        bl = botlive_features(cfg, tup, g["curve_sol_after"].to_list(), creator, entry_t, level, feats["top10_share"])
        rows.append({"mint": mint, "entry_t_": entry_t, **feats, **bl})
    df = (
        pl.DataFrame(rows)
        .join(creator_history(cfg, tokens, labels), on="mint", how="left")
        .join(context_features(cfg, tokens), on="mint", how="left")
        .join(market_heat(cfg, labels, tokens), on="mint", how="left")
        .join(market_state(cfg, labels, tokens), on="mint", how="left")
        .join(wallet_features(cfg, wt, labels, tokens), on="mint", how="left")
    )
    df = df.with_columns(
        active_at_entry=(pl.col("last_trade_t") >= pl.col("entry_t_") - float(cfg.metrics["active_silence_max"]))
    ).drop("entry_t_")
    side = labels.select("mint", "label", "launch_day", "curve_sol_at_entry", pl.col("in_zone").cast(pl.Float64))
    return side.join(df, on="mint", how="inner")
