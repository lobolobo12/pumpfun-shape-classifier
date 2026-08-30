"""prescreen — which coins are worth a trade-tape fetch, and with what weight.

The 20 s curve polls (early_marks / attention_marks) cannot label a coin, but
they bound it. Price on the curve is virtual_sol / virtual_token, so reaching
(1 + tp)x the entry price from ANY entry requires the curve to hold at least
    needed = (sqrt(1 + tp) - 1) * initial_virtual_sol
real SOL at some point in the horizon (12.4 SOL for tp = 1). Strata:

  mayhem      is_mayhem_mode in the create frame -> a curve v1 cannot simulate; dropped, counted
  no_inflow   polls exist and never show SOL in the curve -> cannot have min_trades; dropped, counted
  candidate        max real SOL >= needed, or graduated -> fetched in full
  unlikely_active  never reached `needed`, but the curve's SOL changed after the window (so the coin
                   was alive at the entry; validated 26/26 on probe tapes) -> fetched in full
  unlikely_quiet   never reached `needed`, no change after the window (mostly dead) -> sampled
  unknown          no polls (coins the collector never saw) -> sampled

Sampling is by mint hash, so it is stable as the universe grows. Every token
gets a `weight` = 1 / its stratum's rate, and the "unlikely" stratum's
positives are reported as a check on the bound. Nothing looks at outcomes.
"""

from __future__ import annotations

import math
import sqlite3
import zlib

import polars as pl

from pumpfun.config import Config
from pumpfun.ingest.universe import SNAPSHOT_NAME
from pumpfun.reports import update_counts

POLL_SLACK_MS = 20_000
STRATA = ("candidate", "unlikely_active", "unlikely_quiet", "unknown")


def needed_sol(cfg: Config) -> float:
    """Real SOL the curve must reach for a (1 + tp)x price move from any entry — a necessary condition."""
    return (math.sqrt(1 + cfg.tp) - 1) * cfg.curve_expected.initial_virtual_sol_lamports / 1e9


def unit_hash(mint: str) -> float:
    return zlib.crc32(mint.encode()) / 2**32


def run(cfg: Config) -> pl.DataFrame:
    tokens = pl.read_parquet(cfg.tokens_path)
    snap = cfg.raw_dir / SNAPSHOT_NAME
    con = sqlite3.connect(f"file:{snap}?mode=ro", uri=True)
    try:
        con.execute("create temp table u(mint text primary key, after_ms integer, cutoff_ms integer)")
        cutoff = cfg.tape_until_seconds * 1000 + POLL_SLACK_MS
        after = cfg.window_seconds * 1000 - POLL_SLACK_MS
        con.executemany(
            "insert into u values (?, ?, ?)",
            [(m, int(ms) + after, int(ms) + cutoff) for m, ms in tokens.select("mint", "launch_time_ms").iter_rows()],
        )
        rows = con.execute(
            """
            select u.mint, max(m.real_sol_reserves), count(m.at), max(m.complete),
                   count(distinct case when m.at >= u.after_ms then m.real_sol_reserves end)
              from u left join (
                select mint, at, real_sol_reserves, complete from early_marks
                union all
                select mint, at, real_sol_reserves, complete from attention_marks
              ) m on m.mint = u.mint and m.at <= u.cutoff_ms
             group by u.mint
            """
        ).fetchall()
    finally:
        con.close()
    marks = pl.DataFrame(
        {
            "mint": [r[0] for r in rows],
            "max_real_sol": [(r[1] or 0) / 1e9 for r in rows],
            "n_marks": [int(r[2]) for r in rows],
            "completed": [bool(r[3]) for r in rows],
            "distinct_after": [int(r[4]) for r in rows],
        },
        schema={
            "mint": pl.String,
            "max_real_sol": pl.Float64,
            "n_marks": pl.Int64,
            "completed": pl.Boolean,
            "distinct_after": pl.Int64,
        },
    )
    need = needed_sol(cfg)
    rates = {
        "candidate": 1.0,
        "unlikely_active": 1.0,
        "unlikely_quiet": cfg.prescreen.sample_rate_unlikely_quiet,
        "unknown": cfg.prescreen.sample_rate_unknown,
    }
    df = tokens.join(marks, on="mint", how="left").with_columns(
        stratum=pl.when(pl.col("mayhem").fill_null(False))
        .then(pl.lit("mayhem"))
        .when(pl.col("n_marks") == 0)
        .then(pl.lit("unknown"))
        .when(pl.col("max_real_sol") <= 0)
        .then(pl.lit("no_inflow"))
        .when(pl.col("completed") | (pl.col("max_real_sol") >= need))
        .then(pl.lit("candidate"))
        .when(pl.col("distinct_after") >= 2)
        .then(pl.lit("unlikely_active"))
        .otherwise(pl.lit("unlikely_quiet")),
        u=pl.col("mint").map_elements(unit_hash, return_dtype=pl.Float64),
    )
    df = df.with_columns(
        rate=pl.col("stratum").replace_strict(rates, default=0.0),
    ).with_columns(
        selected=(pl.col("u") < pl.col("rate")),
        weight=pl.when(pl.col("rate") > 0).then(1.0 / pl.col("rate")).otherwise(0.0),
    )
    strata = df.select("mint", "launch_day", "stratum", "max_real_sol", "n_marks", "selected", "weight")
    cfg.interim_dir.mkdir(parents=True, exist_ok=True)
    strata.write_parquet(cfg.interim_dir / "strata.parquet")

    until = cfg.tape_until_seconds * 1000
    queue = (
        df.filter(pl.col("selected"))
        .select("mint", "launch_time_ms", "launch_day", "stratum", "weight", until_ms=pl.col("launch_time_ms") + until)
        .sort("launch_time_ms")
    )
    queue.write_parquet(cfg.interim_dir / "fetch_queue.parquet")
    # A committed copy for the GitHub Actions fetcher (small; the runners have no attention.db).
    committed = cfg.data_dir / "queue" / "fetch_queue.parquet"
    committed.parent.mkdir(parents=True, exist_ok=True)
    queue.write_parquet(committed)

    sizes = {s: int(df.filter(pl.col("stratum") == s).height) for s in (*STRATA, "no_inflow", "mayhem")}
    picked = {s: int(queue.filter(pl.col("stratum") == s).height) for s in STRATA}
    counts = {
        "universe_tokens": tokens.height,
        "needed_sol_for_tp": round(need, 3),
        "strata": sizes,
        "queued": picked,
        "prescreen_no_inflow_dropped": sizes["no_inflow"],
        "prescreen_mayhem_dropped": sizes["mayhem"],
        "fetch_queue": queue.height,
        "sample_rates": rates,
    }
    update_counts(cfg.reports_dir, "prescreen", counts)
    print(f"prescreen: {tokens.height} tokens; need >= {need:.2f} SOL for a {1 + cfg.tp:.1f}x; strata {sizes}")
    print(f"  queue {queue.height}: {picked}")
    return queue
