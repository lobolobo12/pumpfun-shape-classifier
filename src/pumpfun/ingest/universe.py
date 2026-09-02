"""universe — every coin born in the date range, from the create capture.

Source: the trading repo's attention collector (attention.db). Its sweep reads
the 50 newest coins every 20 s (50 coins span ~47 s of creates), so a coin
captured at age <= max_first_seen_age_seconds was seen at birth regardless of
what it did next. Coins first seen LATER reached the collector through an
outcome-conditioned path (curve band, graduation) and are excluded: keeping
them would be the survivorship bias spec §5 warns about. Their count is logged.

Completeness is measured, not assumed: pump.fun's on-chain `create` frames
recorded by the same repo (data/raw/pumpportal) are cross-checked against the
sweep for the hours both were up -> reports/universe_coverage.json.
"""

from __future__ import annotations

import bisect
import gzip
import json
import logging
import sqlite3
import zlib
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

import polars as pl

from pumpfun.checks.schema import TOKENS_SCHEMA, conform
from pumpfun.config import Config
from pumpfun.reports import update_counts, write_json

log = logging.getLogger(__name__)

SNAPSHOT_NAME = "attention_snapshot.sqlite"


def snapshot_attention_db(src: Path, dst: Path) -> Path:
    """Copy the live WAL database with the SQLite backup API (consistent, non-blocking for the writer)."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(f"file:{src}?mode=ro", uri=True) as s, sqlite3.connect(dst) as d:
        s.backup(d)
    return dst


def _day_expr(ms_col: str, tz: str) -> pl.Expr:
    ts = pl.from_epoch(pl.col(ms_col), time_unit="ms").dt.replace_time_zone("UTC")
    return ts.dt.convert_time_zone(tz).dt.strftime("%Y-%m-%d")


def _graduations(con: sqlite3.Connection) -> pl.DataFrame:
    rows = con.execute(
        """
        select mint, min(at) as graduation_ms from (
          select mint, at from early_marks where complete = 1
          union all
          select mint, at from attention_marks where complete = 1
        ) group by mint
        """
    ).fetchall()
    return pl.DataFrame(
        {"mint": [r[0] for r in rows], "graduation_ms": [int(r[1]) for r in rows]},
        schema={"mint": pl.String, "graduation_ms": pl.Int64},
    )


def build_tokens(cfg: Config, snapshot: Path) -> tuple[pl.DataFrame, dict[str, int]]:
    con = sqlite3.connect(f"file:{snapshot}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "select mint, creator, created_timestamp, source, first_seen_age_s, first_seen_at"
            " from attention_meta where created_timestamp is not null"
        ).fetchall()
        grads = _graduations(con)
    finally:
        con.close()
    meta = pl.DataFrame(
        {
            "mint": [r[0] for r in rows],
            "creator": [r[1] for r in rows],
            "launch_time_ms": [int(r[2]) for r in rows],
            "source": [r[3] for r in rows],
            "first_seen_age_s": [None if r[4] is None else float(r[4]) for r in rows],
            "first_seen_at": [int(r[5]) for r in rows],
        },
        schema={
            "mint": pl.String,
            "creator": pl.String,
            "launch_time_ms": pl.Int64,
            "source": pl.String,
            "first_seen_age_s": pl.Float64,
            "first_seen_at": pl.Int64,
        },
    )
    meta = meta.with_columns(launch_day=_day_expr("launch_time_ms", cfg.split_timezone))
    in_range = meta.filter((pl.col("launch_day") >= cfg.date_start) & (pl.col("launch_day") < cfg.date_end))
    counts = {"attention_meta_total": meta.height, "in_date_range": in_range.height}

    seen_at_birth = in_range.filter(
        pl.col("first_seen_age_s").is_not_null() & (pl.col("first_seen_age_s") <= cfg.universe.max_first_seen_age_seconds)
    )
    counts["universe_seen_late_dropped"] = in_range.height - seen_at_birth.height
    counts["universe_no_creator"] = int(seen_at_birth["creator"].is_null().sum())
    seen_at_birth = seen_at_birth.filter(pl.col("creator").is_not_null())

    days = _utc_days_around(seen_at_birth["launch_day"].unique().to_list())
    frames = frame_tokens(cfg, days).filter((pl.col("launch_day") >= cfg.date_start) & (pl.col("launch_day") < cfg.date_end))
    extra = frames.filter(~pl.col("mint").is_in(seen_at_birth["mint"].implode()))
    counts["pumpportal_frames_in_range"] = frames.height
    counts["universe_added_from_frames"] = extra.height
    cols = ["mint", "creator", "launch_time_ms", "source", "first_seen_age_s", "launch_day", "mayhem", "meta_host"]
    # The sweep does not know about mayhem mode or the metadata host; take both from the frame when one exists.
    seen_at_birth = seen_at_birth.join(frames.select("mint", "mayhem", "meta_host"), on="mint", how="left")
    union = pl.concat([seen_at_birth.select(cols), extra.select(cols)])
    counts["universe_mayhem_flagged"] = int(union["mayhem"].fill_null(False).sum())
    counts["universe_mayhem_unknown"] = int(union["mayhem"].is_null().sum())
    tokens = (
        union.join(grads, on="mint", how="left")
        .with_columns(
            launch_time=(pl.col("launch_time_ms") // 1000),
            graduated=pl.col("graduation_ms").is_not_null(),
            graduation_time=(pl.col("graduation_ms") // 1000),
        )
        .sort("launch_time_ms", "mint")
    )
    tokens = conform(tokens, TOKENS_SCHEMA, "tokens")
    counts["universe_tokens"] = tokens.height
    return tokens, counts


# ------------------------------------------------------------ coverage check


def _iter_create_frames(raw_dir: Path, days: set[str]):
    for day in sorted(days):
        d = raw_dir / day
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.ndjson.gz")):
            # The hour being recorded is a partial gzip stream: keep every frame up to the truncation.
            try:
                with gzip.open(f, "rt") as fh:
                    for line in fh:
                        try:
                            fr = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        p = fr.get("payload") or {}
                        if p.get("txType") == "create" and isinstance(p.get("mint"), str):
                            uri = str(p.get("uri") or "")
                            host = uri.split("/")[2].lower() if uri.startswith("http") and uri.count("/") >= 2 else None
                            yield (
                                p["mint"],
                                int(fr["receivedAt"]),
                                str(p.get("traderPublicKey") or ""),
                                bool(p.get("is_mayhem_mode", False)),
                                host,
                            )
            except (EOFError, zlib.error, OSError) as e:
                log.warning("%s: stopped at a truncated block (%s)", f.name, e.__class__.__name__)


def frame_tokens(cfg: Config, days: set[str]) -> pl.DataFrame:
    """On-chain create frames as token rows (source = pumpportal); creator = the create tx signer."""
    rows: dict[str, tuple[int, str, bool, str | None]] = {}
    for mint, at, creator, mayhem, host in _iter_create_frames(cfg.sources.pumpportal_raw, days):
        if creator and mint not in rows:
            rows[mint] = (at, creator, mayhem, host)
    df = pl.DataFrame(
        {
            "mint": list(rows),
            "launch_time_ms": [v[0] for v in rows.values()],
            "creator": [v[1] for v in rows.values()],
            "mayhem": [v[2] for v in rows.values()],
            "meta_host": [v[3] for v in rows.values()],
        },
        schema={
            "mint": pl.String,
            "launch_time_ms": pl.Int64,
            "creator": pl.String,
            "mayhem": pl.Boolean,
            "meta_host": pl.String,
        },
    )
    return df.with_columns(
        source=pl.lit("pumpportal"),
        first_seen_age_s=pl.lit(0.0),
        launch_day=_day_expr("launch_time_ms", cfg.split_timezone),
    )


def _utc_days_around(local_days: list[str]) -> set[str]:
    days: set[str] = set()
    for d in local_days:
        dt = datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=UTC)
        for off in (-1, 0, 1):
            days.add(datetime.fromtimestamp(dt.timestamp() + off * 86400, UTC).strftime("%Y-%m-%d"))
    return days


def coverage_check(cfg: Config, snapshot: Path, tokens: pl.DataFrame) -> dict:
    """Share of on-chain create frames present in the sweep universe, counted only while the collector was polling."""
    con = sqlite3.connect(f"file:{snapshot}?mode=ro", uri=True)
    try:
        polls = sorted(int(r[0]) for r in con.execute("select at from attention_polls").fetchall())
        meta_mints = {r[0] for r in con.execute("select mint from attention_meta").fetchall()}
    finally:
        con.close()
    universe = set(tokens.filter(pl.col("source") != "pumpportal")["mint"].to_list())
    days = _utc_days_around(tokens["launch_day"].unique().to_list())

    def collector_up(ms: int, slack_ms: int = 60_000) -> bool:
        i = bisect.bisect_left(polls, ms - slack_ms)
        return i < len(polls) and polls[i] <= ms + slack_ms

    per_day: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for mint, at, _creator, _mayhem, _host in _iter_create_frames(cfg.sources.pumpportal_raw, days):
        day = datetime.fromtimestamp(at / 1000, UTC).strftime("%Y-%m-%d")
        c = per_day[day]
        c["frames"] += 1
        up = collector_up(at)
        if up:
            c["frames_while_polling"] += 1
            if mint in universe:
                c["in_universe_while_polling"] += 1
            elif mint in meta_mints:
                c["in_meta_but_seen_late"] += 1
        elif mint in universe:
            c["in_universe_while_not_polling"] += 1
    tot_up = sum(c["frames_while_polling"] for c in per_day.values())
    tot_hit = sum(c["in_universe_while_polling"] for c in per_day.values())
    return {
        "coverage_while_polling": (tot_hit / tot_up) if tot_up else None,
        "frames_while_polling": tot_up,
        "in_universe_while_polling": tot_hit,
        "per_day": {d: dict(c) for d, c in sorted(per_day.items())},
        "coverage_min": cfg.universe.coverage_min,
    }


def run(cfg: Config, strict: bool = True) -> pl.DataFrame:
    snap = snapshot_attention_db(cfg.sources.attention_db, cfg.raw_dir / SNAPSHOT_NAME)
    tokens, counts = build_tokens(cfg, snap)
    cfg.tokens_path.parent.mkdir(parents=True, exist_ok=True)
    tokens.write_parquet(cfg.tokens_path)
    # Historical (Bitquery) tokens live outside the collector's range; re-append them on every rebuild.
    if any((cfg.raw_dir / "bitquery").glob("*.parquet")):
        from pumpfun.ingest.bitquery_history import merge_into_tokens

        merge_into_tokens(cfg)
        tokens = pl.read_parquet(cfg.tokens_path)
        counts["universe_bitquery_appended"] = tokens.height - counts["universe_tokens"]
    cov = coverage_check(cfg, snap, tokens)
    write_json(cfg.reports_dir / "universe_coverage.json", cov)
    update_counts(cfg.reports_dir, "universe", counts)
    per_day = tokens.group_by("launch_day").len().sort("launch_day")
    print(f"universe: {tokens.height} tokens -> {cfg.tokens_path}")
    for d, n in per_day.iter_rows():
        print(f"  {d}: {n}")
    print(
        f"dropped seen-late: {counts['universe_seen_late_dropped']}  "
        f"added from on-chain frames: {counts['universe_added_from_frames']}"
    )
    c = cov["coverage_while_polling"]
    shown = "n/a" if c is None else f"{c:.4f}"
    print(f"sweep coverage vs on-chain create frames (collector up): {shown} over {cov['frames_while_polling']} frames")
    if strict and c is not None and c < cfg.universe.coverage_min:
        raise SystemExit(f"sweep coverage {c:.4f} < {cfg.universe.coverage_min}; see reports/universe_coverage.json")
    return tokens
