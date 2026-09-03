"""bitquery_history — the 30-day historical universe from Bitquery's trade index.

Speaks MCP JSON-RPC directly to mcp.bitquery.io with BITQUERY_TOKEN (from .env) and runs
bounded per-day SQL over trading_rt.tokens_by_interval_start: every `...pump` token that
traded on a given UTC day, its first interval, day-high/low, volume. Results go straight
to data/raw/bitquery/<day>.parquet — never through a conversation.

Universe semantics: processed oldest-first with a rolling seen-set, a token is NEW on the
first day it appears; the first two processed days only seed the seen-set (left-censored)
and never enter the universe. Creator and mayhem flags are unknown for historical coins
(creator features stay null; mayhem-mode coins are caught later by the curve-residual check).
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import httpx
import polars as pl

from pumpfun.config import Config

log = logging.getLogger(__name__)

MCP_URL = "https://mcp.bitquery.io/mcp"
CHUNKS = ["123", "456", "789", "ABCDE", "FGHJKL", "MNPQRS", "TUVWXY", "Zabcde", "fghijk", "mnopqrs", "tuvwxyz"]


def _token() -> str:
    for line in Path(".env").read_text().splitlines():
        if line.startswith("BITQUERY_TOKEN="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("BITQUERY_TOKEN missing from .env")


class BitqueryMcp:
    def __init__(self) -> None:
        self._http = httpx.Client(
            headers={
                "Authorization": f"Bearer {_token()}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
            timeout=120,
        )
        self._id = 0
        self._rpc(
            "initialize",
            {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "pumpfun-shape-classifier", "version": "0.1"},
            },
        )

    def _rpc(self, method: str, params: dict) -> dict:
        self._id += 1
        r = self._http.post(MCP_URL, json={"jsonrpc": "2.0", "id": self._id, "method": method, "params": params})
        r.raise_for_status()
        body = r.json()
        if "error" in body:
            raise RuntimeError(f"MCP {method}: {body['error']}")
        return body.get("result", {})

    def sql(self, query: str, retries: int = 4) -> list[dict]:
        for attempt in range(retries):
            try:
                res = self._rpc("tools/call", {"name": "execute_sql", "arguments": {"sql": query}})
            except (httpx.HTTPError, RuntimeError) as e:
                log.warning("sql attempt %d failed: %s", attempt, str(e)[:200])
                time.sleep(5 * (attempt + 1))
                continue
            if res.get("isError"):
                raise RuntimeError(f"SQL error: {json.dumps(res)[:400]}")
            rows: list[dict] = []
            for item in res.get("content", []):
                if item.get("type") != "text":
                    continue
                for line in item["text"].splitlines():
                    line = line.strip()
                    if line.startswith("{"):
                        rows.append(json.loads(line))
            return rows
        raise RuntimeError("sql: retries exhausted")


DAY_SQL = """
SELECT
  Token_Address AS mint,
  min(Interval_Time_Start) AS first_iv,
  argMin(Price_Ohlc_Open, Interval_Time_Start) AS px_first_open,
  max(Price_Ohlc_High) AS px_high,
  min(Price_Ohlc_Low) AS px_low,
  argMax(Price_Ohlc_High, Price_Ohlc_High) AS _ph,
  sum(Volume_Usd) AS vol_usd,
  count() AS n_intervals,
  max(Supply_FullyDilutedValuationUsd) AS fdv_max
FROM trading_rt.tokens_by_interval_start
WHERE Token_Network = 'Solana' AND Block_Date = '{day}'
  AND endsWith(Token_Address, 'pump') AND substring(Token_Address, 1, 1) IN ({chars})
GROUP BY Token_Address
"""


def pull_day(cfg: Config, mcp: BitqueryMcp, day: str) -> Path:
    out = cfg.raw_dir / "bitquery" / f"{day}.parquet"
    if out.exists():
        return out
    rows: list[dict] = []
    for chunk in CHUNKS:
        chars = ",".join(f"'{c}'" for c in chunk)
        rows.extend(mcp.sql(DAY_SQL.format(day=day, chars=chars)))
    df = pl.DataFrame(rows).with_columns(pl.lit(day).alias("block_date"))
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(out)
    log.info("%s: %d pump tokens -> %s", day, df.height, out)
    return out


def screen_calibration(mcp: BitqueryMcp, day: str) -> list[dict]:
    """Distribution of day high/low ratios, to pick the candidate screen empirically."""
    q = f"""
    SELECT quantilesExact(0.5, 0.75, 0.9, 0.95, 0.99)(r) AS q, count() AS n,
           countIf(r >= 2) AS ge2, countIf(r >= 3) AS ge3, countIf(r >= 5) AS ge5
    FROM (
      SELECT Token_Address, max(Price_Ohlc_High) / nullIf(min(Price_Ohlc_Low), 0) AS r
      FROM trading_rt.tokens_by_interval_start
      WHERE Token_Network = 'Solana' AND Block_Date = '{day}' AND endsWith(Token_Address, 'pump')
      GROUP BY Token_Address
    )
    """
    return mcp.sql(q)


# ------------------------------------------------------------ universe merge

WARMUP_DAYS = 2  # first processed days only seed the seen-set: their "new" tokens are left-censored


def universe_extension(cfg: Config) -> pl.DataFrame:
    """Historical tokens (source=bitquery): first day each mint appears, with its screen fields.

    Screen fields aggregate the token's first two calendar days: max FDV and max high/low ratio.
    """
    files = sorted((cfg.raw_dir / "bitquery").glob("*.parquet"))
    if len(files) <= WARMUP_DAYS:
        raise SystemExit("not enough bitquery day files; run the history pull first")
    cols = ["mint", "first_iv", "px_high", "px_low", "fdv_max", "pre_sampled", "pre_weight"]
    frames = []
    for f in files:
        df = pl.read_parquet(f)
        if "pre_sampled" not in df.columns:
            df = df.with_columns(pre_sampled=pl.lit(False), pre_weight=pl.lit(1.0))
        frames.append(
            df.select(cols).with_columns(
                r=pl.col("px_high") / pl.when(pl.col("px_low") > 0).then(pl.col("px_low")).otherwise(None)
            )
        )
    from datetime import date

    days = [date.fromisoformat(f.stem) for f in files]
    # A day is warm-up when it is among the first WARMUP_DAYS of a contiguous block (gap > 1 day starts a block).
    warm: set[int] = set()
    block_start = 0
    for i in range(len(days)):
        if i > 0 and (days[i] - days[i - 1]).days > 1:
            block_start = i
        if i - block_start < WARMUP_DAYS:
            warm.add(i)
    seen: set[str] = set()
    out = []
    for i in range(len(frames)):
        df = frames[i]
        if i in warm:
            seen.update(df["mint"].to_list())
            continue
        new = df.filter(~pl.col("mint").is_in(sorted(seen)))
        seen.update(df["mint"].to_list())
        nxt = frames[i + 1] if i + 1 < len(frames) else None
        agg2 = new.select("mint", "first_iv", "fdv_max", "r", "pre_sampled", "pre_weight")
        if nxt is not None:
            n2 = nxt.select("mint", fdv2=pl.col("fdv_max"), r2=pl.col("r"))
            agg2 = (
                agg2.join(n2, on="mint", how="left")
                .with_columns(fdv_max=pl.max_horizontal("fdv_max", "fdv2"), r=pl.max_horizontal("r", "r2"))
                .drop("fdv2", "r2")
            )
        out.append(agg2)
    ext = pl.concat(out)
    ext = ext.with_columns(
        launch_time_ms=pl.col("first_iv").str.to_datetime("%Y-%m-%dT%H:%M:%SZ", time_zone="UTC").dt.epoch("ms"),
    )
    return ext


def merge_into_tokens(cfg: Config) -> None:
    from pumpfun.checks.schema import TOKENS_SCHEMA, conform
    from pumpfun.ingest.universe import _day_expr

    tokens = pl.read_parquet(cfg.tokens_path)
    ext = universe_extension(cfg).filter(~pl.col("mint").is_in(tokens["mint"].implode()))
    rows = ext.with_columns(
        creator=pl.lit(None, dtype=pl.String),
        launch_time=(pl.col("launch_time_ms") // 1000),
        graduated=pl.lit(False),
        graduation_time=pl.lit(None, dtype=pl.Int64),
        source=pl.lit("bitquery"),
        first_seen_age_s=pl.lit(None, dtype=pl.Float64),
        launch_day=_day_expr("launch_time_ms", cfg.split_timezone),
        mayhem=pl.lit(None, dtype=pl.Boolean),
        meta_host=pl.lit(None, dtype=pl.String),
    )
    merged = pl.concat([tokens, conform(rows, TOKENS_SCHEMA, "tokens-ext")]).sort("launch_time_ms", "mint")
    merged.write_parquet(cfg.tokens_path)
    # screen fields for the prescreen, kept separately
    ext.select("mint", "fdv_max", "r", "pre_sampled", "pre_weight").write_parquet(cfg.interim_dir / "bitquery_screen.parquet")
    log.info("universe extension: +%d historical tokens (now %d)", rows.height, merged.height)


def fix_launch_times(cfg: Config) -> int:
    """After fetching, replace the hour-floor launch times of bitquery tokens with the tape's first trade."""
    from pumpfun.ingest.fetch_trades import Ledger, load_cached
    from pumpfun.ingest.universe import _day_expr

    tokens = pl.read_parquet(cfg.tokens_path)
    hist = tokens.filter(pl.col("source") == "bitquery")["mint"].to_list()
    if not hist:
        return 0
    led = Ledger(cfg.ledger_path)
    ok = set(led.ok_mints())
    led.close()
    fixes = {}
    for m in hist:
        if m not in ok:
            continue
        tf = load_cached(cfg, m)
        if tf and tf.complete and tf.trades:
            fixes[m] = min(t.at_ms for t in tf.trades)
    if not fixes:
        return 0
    fixed = tokens.with_columns(
        launch_time_ms=pl.col("mint").replace_strict(fixes, default=None).fill_null(pl.col("launch_time_ms"))
    ).with_columns(
        launch_time=(pl.col("launch_time_ms") // 1000),
        launch_day=_day_expr("launch_time_ms", cfg.split_timezone),
    )
    fixed.write_parquet(cfg.tokens_path)
    log.info("launch times corrected from tapes: %d of %d historical tokens", len(fixes), len(hist))
    return len(fixes)
