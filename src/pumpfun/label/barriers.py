"""barriers — triple-barrier labels on REALIZED exit value.

For every coin that passes the filters (spec §7) a hypothetical position of
`position_sol` is bought with `buy_exact_sol_in` at the first trade at/after
launch + window (+ lag), on the curve state just before that trade. The
position's own reserve delta is carried forward, and at every later trade the
exact proceeds of selling the whole position — curve or PumpSwap pool, fees,
tx fee, router fee — are computed. The barriers run against THAT series:

    label = 1 if net proceeds >= cost * (1 + tp) first
            0 if net proceeds <= cost * (1 - sl) first (or <= peak * (1 - sl) when trailing)
            0 at entry + horizon

Every drop is counted by rule in reports/filter_counts.json.
"""

from __future__ import annotations

import logging
from collections import Counter
from dataclasses import asdict, dataclass

import polars as pl

from pumpfun.config import Config
from pumpfun.ingest.to_parquet import CURVE_PROGRAM, POOL_PROGRAMS, curve_params, read_trades
from pumpfun.label import curve_sim as cs
from pumpfun.label import pool_sim as ps
from pumpfun.reports import update_counts, write_json

log = logging.getLogger(__name__)

RESIDUAL_CHECK_TRADES = 30


@dataclass(frozen=True)
class TapeTrade:
    idx: int
    t_s: float  # seconds since launch
    is_buy: bool
    sol: float
    tokens: float
    program: str
    price_sol: float


@dataclass(frozen=True)
class LabelRow:
    mint: str
    label: int
    entry_t: float
    entry_idx: int
    n_visible: int  # trades the features may see (age: strictly before entry time; cross: incl. the crossing trade)
    entry_price: float  # marginal price just before the entry (sequence normaliser)
    entry_fill_price: float  # cost / tokens
    entry_cost_sol: float
    tokens_held: float
    exit_t: float
    exit_net_sol: float
    exit_reason: str
    ratio_at_exit: float
    peak_ratio: float
    curve_sol_at_entry: float
    in_zone: bool
    n_trades_window: int
    n_trades_horizon: int
    graduated_in_horizon: bool
    residual: float


class Drop(Exception):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def _router_fee(lamports: int, pct: float) -> int:
    return round(lamports * pct)


def label_tape(cfg: Config, mint: str, trades: list[TapeTrade]) -> LabelRow:
    p = curve_params(cfg)
    raw_per = p.raw_per_token
    fees = cs.CurveFees(cfg.fee_protocol_bps, cfg.fee_creator_bps)
    pfees = ps.PoolFees(cfg.pool_fee_bps.lp, cfg.pool_fee_bps.protocol, cfg.pool_fee_bps.creator)

    def replay_check(upto: int) -> tuple[cs.CurveReserves, float]:
        """Replay trades[:upto] on the curve, tracking the tape-vs-maths residual."""
        c = cs.initial_reserves(p)
        resid: list[float] = []
        for t in trades[:upto]:
            if t.program != CURVE_PROGRAM:
                raise Drop("graduated_before_entry")
            c = cs.apply_tape_trade(c, t.is_buy, cs.sol_to_lamports(t.sol), cs.tokens_to_raw(t.tokens, raw_per))
            if len(resid) < RESIDUAL_CHECK_TRADES and t.price_sol > 0 and c.virtual_token > 0:
                resid.append(abs(c.spot_sol_per_token(raw_per) / t.price_sol - 1))
        return c, (sorted(resid)[len(resid) // 2] if resid else 0.0)

    if cfg.decision_mode == "age":
        w = cfg.window_seconds
        t_entry = float(cfg.entry_offset_seconds)
        if not trades or trades[-1].t_s < w:
            raise Drop("lifetime_lt_window")
        # The curve fills at any moment: the entry is the state after the last trade before t_entry.
        entry_idx = next((t.idx for t in trades if t.t_s >= t_entry), len(trades))
        n_visible = entry_idx
        if sum(1 for t in trades[:n_visible] if t.t_s < w) < cfg.min_trades_in_window:
            raise Drop("lt_min_trades")
        curve, residual = replay_check(entry_idx)
    elif cfg.decision_mode == "cross":
        level = cs.sol_to_lamports(cfg.cross_level_sol)
        c = cs.initial_reserves(p)
        cross_i: int | None = None
        for i, t in enumerate(trades):
            if t.program != CURVE_PROGRAM:
                break
            c = cs.apply_tape_trade(c, t.is_buy, cs.sol_to_lamports(t.sol), cs.tokens_to_raw(t.tokens, raw_per))
            if c.real_sol >= level:
                cross_i = i
                break
        if cross_i is None:
            raise Drop("never_crossed_level")
        if trades[cross_i].t_s < cfg.cross_min_age_seconds:
            raise Drop("crossed_too_young")
        entry_idx = cross_i + 1  # the crossing trade is visible; we buy right after it
        n_visible = entry_idx
        t_entry = trades[cross_i].t_s
        if n_visible < cfg.min_trades_in_window:
            raise Drop("lt_min_trades")
        curve, residual = replay_check(entry_idx)
    else:
        raise SystemExit(f"unknown decision_mode {cfg.decision_mode!r}")

    if residual > cfg.curve_param_tolerance:
        raise Drop("non_standard_curve")
    if curve.complete:
        raise Drop("graduated_before_entry")

    entry_price = curve.spot_sol_per_token(raw_per)
    buy = cs.buy_exact_sol_in(curve, cfg.position_lamports, fees)
    if buy.tokens_out <= 0:
        raise Drop("entry_zero_tokens")
    if buy.completed:
        raise Drop("entry_completes_curve")
    cost = buy.total_paid + cfg.tx_fee_lamports + _router_fee(cfg.position_lamports, cfg.router_fee_pct)
    held = buy.tokens_out
    delta_sol, delta_tok = buy.quote_to_curve, buy.tokens_out
    curve_sol_at_entry = curve.real_sol / cs.LAMPORTS_PER_SOL

    def net_curve(c: cs.CurveReserves) -> int:
        shifted = cs.CurveReserves(
            c.virtual_token - delta_tok, c.virtual_sol + delta_sol, c.real_token - delta_tok, c.real_sol + delta_sol
        )
        s = cs.sell_exact_tokens_in(shifted, held, fees)
        gross_net = s.quote_out_net if s.real_reserves_ok else min(s.quote_out_net, shifted.real_sol)
        return gross_net - _router_fee(gross_net, cfg.router_fee_pct) - cfg.tx_fee_lamports

    def net_pool(r: ps.PoolReserves) -> int:
        s = ps.sell_base_input(held, r, pfees)
        gross_net = s.quote_out_net if s.real_reserves_ok else min(s.quote_out_net, r.quote)
        return gross_net - _router_fee(gross_net, cfg.router_fee_pct) - cfg.tx_fee_lamports

    # --- every later trade is a state we could sell into
    horizon_end = t_entry + cfg.horizon_seconds
    pool: ps.PoolReserves | None = None
    graduated = False
    peak_net = 0
    peak_ratio = 0.0
    label, reason, exit_t, exit_net = 0, "vertical_no_trades", t_entry, net_curve(curve)
    n_horizon = 0
    for t in trades[entry_idx:]:
        if t.t_s > horizon_end:
            break
        n_horizon += 1
        lam, raw = cs.sol_to_lamports(t.sol), cs.tokens_to_raw(t.tokens, raw_per)
        if t.program == CURVE_PROGRAM and pool is None:
            curve = cs.apply_tape_trade(curve, t.is_buy, lam, raw)
            net = net_curve(curve)
        elif t.program in POOL_PROGRAMS:
            if pool is None:
                m = cfg.migration
                pool = ps.migration_reserves(m.base_tokens_raw, m.quote_lamports, m.virtual_quote_lamports)
                graduated = True
            pool = ps.apply_tape_trade(pool, t.is_buy, lam, raw)
            net = net_pool(pool)
        else:
            continue
        ratio = net / cost
        exit_t, exit_net = t.t_s, net
        peak_ratio = max(peak_ratio, ratio)
        peak_net = max(peak_net, net)
        if ratio >= 1 + cfg.tp:
            label, reason = 1, "tp"
            break
        stop = (net <= peak_net * (1 - cfg.sl)) if cfg.trailing_stop else (ratio <= 1 - cfg.sl)
        if stop:
            label, reason = 0, "sl"
            break
        reason = "vertical"
    return LabelRow(
        mint=mint,
        label=label,
        entry_t=t_entry,
        entry_idx=entry_idx,
        n_visible=n_visible,
        entry_price=entry_price,
        entry_fill_price=cost / cs.LAMPORTS_PER_SOL / (held / raw_per),
        entry_cost_sol=cost / cs.LAMPORTS_PER_SOL,
        tokens_held=held / raw_per,
        exit_t=exit_t,
        exit_net_sol=exit_net / cs.LAMPORTS_PER_SOL,
        exit_reason=reason,
        ratio_at_exit=exit_net / cost,
        peak_ratio=peak_ratio,
        curve_sol_at_entry=curve_sol_at_entry,
        in_zone=cfg.zone_sol[0] <= curve_sol_at_entry <= cfg.zone_sol[1],
        n_trades_window=n_visible,
        n_trades_horizon=n_horizon,
        graduated_in_horizon=graduated,
        residual=residual,
    )


def tape_from_frame(df: pl.DataFrame) -> list[TapeTrade]:
    return [
        TapeTrade(i, float(t), bool(b), float(s), float(k), str(pr), float(px))
        for i, (t, b, s, k, pr, px) in enumerate(
            df.select("seconds_since_launch", "is_buy", "sol_amount", "token_amount", "program", "price_sol").iter_rows()
        )
    ]


def run(cfg: Config) -> pl.DataFrame:
    tokens = pl.read_parquet(cfg.tokens_path).select("mint", "launch_day", "creator", "mayhem")
    mayhem = set(tokens.filter(pl.col("mayhem").fill_null(False))["mint"].to_list())
    tokens = tokens.drop("mayhem")
    trades = read_trades(cfg).sort("mint", "slot", "slot_index").collect()
    rows: list[dict] = []
    drops: Counter[str] = Counter()
    for (mint,), df in trades.group_by("mint", maintain_order=True):
        if mint in mayhem:
            drops["mayhem_mode"] += 1
            continue
        try:
            rows.append(asdict(label_tape(cfg, str(mint), tape_from_frame(df))))
        except Drop as d:
            drops[d.reason] += 1
    labels = pl.DataFrame(rows).join(tokens, on="mint", how="left")
    cfg.interim_dir.mkdir(parents=True, exist_ok=True)
    labels.write_parquet(cfg.interim_dir / "labels.parquet")

    fetched = trades["mint"].n_unique()
    counts = {"tokens_with_tape": fetched, "labeled": labels.height, **{f"dropped_{k}": v for k, v in sorted(drops.items())}}
    update_counts(cfg.reports_dir, "label", counts)
    summary = _summary(cfg, labels, tokens, trades["mint"].unique())
    write_json(cfg.reports_dir / "labels_summary.json", summary)
    write_json(cfg.data_dir / "base_rate.json", summary["base_rate"])
    log.info(
        "labels: %d labeled of %d tapes; positives %.3f; drops %s",
        labels.height,
        fetched,
        summary["positive_rate_labeled"],
        dict(drops),
    )
    return labels


def _summary(cfg: Config, labels: pl.DataFrame, tokens: pl.DataFrame, fetched: pl.Series) -> dict:
    strata_path = cfg.interim_dir / "strata.parquet"
    strata = pl.read_parquet(strata_path) if strata_path.exists() else None
    per_day = (
        labels.group_by("launch_day")
        .agg(pl.len().alias("labeled"), pl.col("label").sum().alias("positives"), pl.col("in_zone").sum().alias("in_zone"))
        .join(tokens.group_by("launch_day").len().rename({"len": "universe"}), on="launch_day", how="full", coalesce=True)
        .sort("launch_day")
    )
    zone = labels.filter(pl.col("in_zone"))
    base: dict = {
        "note": (
            "positives per universe token. With strata: sum over strata of size * (positives / fetched) — "
            "unfetched coins are represented by their stratum's sampled rate"
        ),
        "per_day": per_day.to_dicts(),
    }
    if strata is not None:
        f = pl.DataFrame({"mint": fetched}).join(strata, on="mint", how="left")
        lab = labels.join(strata.select("mint", "stratum"), on="mint", how="left")
        rows = []
        est = 0.0
        for st in ("candidate", "unlikely_active", "unlikely_quiet", "unknown", "no_inflow", "mayhem"):
            size = strata.filter(pl.col("stratum") == st).height
            n_f = f.filter(pl.col("stratum") == st).height
            n_l = lab.filter(pl.col("stratum") == st).height
            pos = int(lab.filter(pl.col("stratum") == st)["label"].sum())
            rate = pos / n_f if n_f else 0.0
            est += size * rate
            rows.append(
                {"stratum": st, "size": size, "fetched": n_f, "labeled": n_l, "positives": pos, "positive_rate_per_fetched": rate}
            )
        base["per_stratum"] = rows
        base["estimated_overall"] = est / tokens.height if tokens.height else None
        base["estimated_positives"] = est
        base["bound_check_unlikely_positives"] = sum(r["positives"] for r in rows if r["stratum"].startswith("unlikely"))
    else:
        base["overall"] = (float(labels["label"].sum()) / tokens.height) if tokens.height else None
    return {
        "labeled": labels.height,
        "positive_rate_labeled": float(labels["label"].mean()) if labels.height else None,
        "positive_rate_zone": float(zone["label"].mean()) if zone.height else None,
        "zone_n": zone.height,
        "exit_reasons": labels.group_by("exit_reason").len().sort("exit_reason").to_dicts(),
        "median_entry_slippage": float((labels["entry_fill_price"] / labels["entry_price"] - 1).median())
        if labels.height
        else None,
        "base_rate": base,
        "config": {
            k: cfg.raw[k]
            for k in (
                "window_seconds",
                "horizon_seconds",
                "tp",
                "sl",
                "trailing_stop",
                "position_sol",
                "entry_lag_seconds",
                "min_trades_in_window",
            )
        },
        "preset": cfg.preset,
    }
