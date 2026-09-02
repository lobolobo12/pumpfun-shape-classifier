"""to_parquet — the cached tapes as the spec's raw Parquet layer.

One file per launch day under data/raw/trades/{yyyy-mm}/, rebuilt from the cache
(idempotent). `curve_sol_after` / `curve_token_after` / `price_sol` come from
replaying the curve (and, after graduation, the PumpSwap pool) trade by trade;
the API's own spot and realized fill are kept alongside for validation.
"""

from __future__ import annotations

import logging
from collections import defaultdict

import polars as pl

from pumpfun.checks.schema import TRADES_SCHEMA, conform
from pumpfun.config import Config
from pumpfun.ingest.fetch_trades import Ledger, load_cached
from pumpfun.ingest.swap_api import TradeFile
from pumpfun.label import curve_sim as cs
from pumpfun.label import pool_sim as ps
from pumpfun.reports import write_json

log = logging.getLogger(__name__)

CURVE_PROGRAM = "pump"
POOL_PROGRAMS = {"pump_amm", "pumpswap"}


def curve_params(cfg: Config) -> cs.CurveParams:
    e = cfg.curve_expected
    return cs.CurveParams(
        initial_virtual_sol=e.initial_virtual_sol_lamports,
        initial_virtual_token=e.initial_virtual_token_raw,
        initial_real_token=e.initial_real_token_raw,
        token_decimals=e.token_decimals,
    )


def tape_rows(cfg: Config, tf: TradeFile, launch_ms: int) -> list[dict]:
    p = curve_params(cfg)
    raw_per = p.raw_per_token
    curve = cs.initial_reserves(p)
    pool: ps.PoolReserves | None = None
    rows: list[dict] = []
    for t in tf.trades:
        lam = cs.sol_to_lamports(t.sol)
        raw = cs.tokens_to_raw(t.tokens, raw_per)
        if t.program == CURVE_PROGRAM:
            curve = cs.apply_tape_trade(curve, t.is_buy, lam, raw)
            sol_after, tok_after = curve.real_sol / cs.LAMPORTS_PER_SOL, curve.real_token / raw_per
        elif t.program in POOL_PROGRAMS:
            if pool is None:
                m = cfg.migration
                pool = ps.migration_reserves(m.base_tokens_raw, m.quote_lamports, m.virtual_quote_lamports)
            pool = ps.apply_tape_trade(pool, t.is_buy, lam, raw)
            sol_after, tok_after = pool.quote / cs.LAMPORTS_PER_SOL, pool.base / raw_per
        else:
            sol_after, tok_after = None, None
        rows.append(
            {
                "mint": tf.mint,
                "signature": t.tx,
                "slot": t.slot,
                "slot_index": t.idx,
                "block_time": t.at_ms // 1000,
                "seconds_since_launch": (t.at_ms - launch_ms) / 1000.0,
                "is_buy": t.is_buy,
                "sol_amount": t.sol,
                "token_amount": t.tokens,
                "trader": t.user,
                "program": t.program,
                "curve_sol_after": sol_after,
                "curve_token_after": tok_after,
                "price_sol": t.price_sol,
                "fill_price_sol": t.fill_price_sol,
            }
        )
    return rows


def run(cfg: Config) -> dict[str, dict[str, int]]:
    tokens = pl.read_parquet(cfg.tokens_path)
    meta = {m: (int(ms), day) for m, ms, day in tokens.select("mint", "launch_time_ms", "launch_day").iter_rows()}
    ledger = Ledger(cfg.ledger_path)
    mints = ledger.ok_mints()
    ledger.close()
    by_day: dict[str, list[dict]] = defaultdict(list)
    missing = 0
    for mint in mints:
        if mint not in meta:
            continue
        tf = load_cached(cfg, mint)
        if tf is None:
            missing += 1
            continue
        launch_ms, day = meta[mint]
        by_day[day].extend(tape_rows(cfg, tf, launch_ms))
    counts: dict[str, dict[str, int]] = {}
    for day, rows in sorted(by_day.items()):
        df = pl.DataFrame(rows, schema=TRADES_SCHEMA).unique(subset=["signature"], keep="first")
        df = conform(df.sort("mint", "slot", "slot_index"), TRADES_SCHEMA, "trades")
        out = cfg.trades_dir / day[:7] / f"{day}.parquet"
        out.parent.mkdir(parents=True, exist_ok=True)
        df.write_parquet(out)
        counts[day] = {"rows": df.height, "mints": df["mint"].n_unique()}
        log.info("%s: %d rows, %d mints -> %s", day, df.height, counts[day]["mints"], out)
    write_json(cfg.reports_dir / "trades_row_counts.json", {"per_day": counts, "ledger_ok": len(mints), "cache_missing": missing})
    return counts


def read_trades(cfg: Config) -> pl.LazyFrame:
    return pl.scan_parquet(str(cfg.trades_dir / "*" / "*.parquet"))
