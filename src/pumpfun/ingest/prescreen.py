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
STRATA = ("candidate", "unlikely_active", "unlikely_quiet", "unknown", "hist_candidate", "hist_rest")


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
                   count(distinct case when m.at >= u.after_ms then m.real_sol_reserves end),
                   max(case when m.at < u.after_ms then m.reply_count end),
                   max(case when m.at < u.after_ms then m.is_currently_live end)
              from u left join (
                select mint, at, real_sol_reserves, complete, reply_count, is_currently_live from early_marks
                union all
                select mint, at, real_sol_reserves, complete, reply_count, is_currently_live from attention_marks
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
            "replies_at_entry": [None if r[5] is None else int(r[5]) for r in rows],
            "live_at_entry": [None if r[6] is None else bool(r[6]) for r in rows],
        },
        schema={
            "mint": pl.String,
            "max_real_sol": pl.Float64,
            "n_marks": pl.Int64,
            "completed": pl.Boolean,
            "distinct_after": pl.Int64,
            "replies_at_entry": pl.Int64,
            "live_at_entry": pl.Boolean,
        },
    )
    need = needed_sol(cfg)
    screen_path = cfg.interim_dir / "bitquery_screen.parquet"
    if screen_path.exists():
        bq = pl.read_parquet(screen_path).select(
            "mint", bq_fdv=pl.col("fdv_max"), bq_r=pl.col("r"), bq_pre=pl.col("pre_sampled"), bq_w=pl.col("pre_weight")
        )
    else:
        bq = pl.DataFrame(
            schema={"mint": pl.String, "bq_fdv": pl.Float64, "bq_r": pl.Float64, "bq_pre": pl.Boolean, "bq_w": pl.Float64}
        )
    rates = {
        "candidate": 1.0,
        "unlikely_active": 1.0,
        "unlikely_quiet": cfg.prescreen.sample_rate_unlikely_quiet,
        "unknown": cfg.prescreen.sample_rate_unknown,
        "hist_candidate": cfg.prescreen.sample_rate_hist_candidate,
        "hist_rest": cfg.prescreen.sample_rate_hist,
    }
    df = (
        tokens.join(marks, on="mint", how="left")
        .join(bq, on="mint", how="left")
        .with_columns(
            stratum=pl.when(pl.col("source") == "bitquery")
            .then(
                pl.when((pl.col("bq_fdv") >= cfg.prescreen.fdv_candidate_usd) & (pl.col("bq_r") >= 1 + cfg.tp))
                .then(pl.lit("hist_candidate"))
                .otherwise(pl.lit("hist_rest"))
            )
            .when(pl.col("mayhem").fill_null(False))
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
    )
    df = df.with_columns(
        rate=pl.col("stratum").replace_strict(rates, default=0.0),
    ).with_columns(
        selected=(pl.col("u") < pl.col("rate")),
        weight=pl.when(pl.col("rate") > 0).then(1.0 / pl.col("rate")).otherwise(0.0),
    )
    # Pre-sampled historical sources (Dune) already applied the hist_rest sampling server-side:
    # every present row is selected, with the measured weight it arrived with.
    df = df.with_columns(
        selected=pl.when(pl.col("stratum") == "hist_rest")
        .then(pl.col("bq_pre").fill_null(False) | pl.col("selected"))
        .otherwise(pl.col("selected")),
        weight=pl.when((pl.col("stratum") == "hist_rest") & pl.col("bq_pre").fill_null(False))
        .then(pl.col("bq_w"))
        .otherwise(pl.col("weight")),
    )
    strata = df.select(
        "mint", "launch_day", "stratum", "max_real_sol", "n_marks", "selected", "weight", "replies_at_entry", "live_at_entry"
    )
    cfg.interim_dir.mkdir(parents=True, exist_ok=True)
    strata.write_parquet(cfg.interim_dir / "strata.parquet")

    until = cfg.tape_until_seconds * 1000
    hour_slack = 3_600_000  # bitquery launch times are hour-floored; walk one extra hour of tape
    queue = (
        df.filter(pl.col("selected"))
        .select(
            "mint",
            "launch_time_ms",
            "launch_day",
            "stratum",
            "weight",
            until_ms=pl.col("launch_time_ms")
            + until
            + pl.when(pl.col("stratum").str.starts_with("hist_")).then(hour_slack).otherwise(0),
        )
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
