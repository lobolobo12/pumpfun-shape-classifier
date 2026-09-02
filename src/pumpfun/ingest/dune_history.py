"""dune_history — the deep historical universe (pre-Aug-5) from Dune's decoded pump.fun trades.

Free-tier reality shapes the design: we may create PUBLIC queries and execute them, and result
volume is limited — so the screening runs server-side in DuneSQL and only candidate mints plus a
hash-sampled slice of the rest come back, with per-day totals for the weights. Day files land in
data/raw/bitquery/<day>.parquet in the exact shape of the Bitquery pulls (px in USD, fdv = px * 1e9),
plus `pre_sampled` / `pre_weight` so the prescreen knows the sampling already happened.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

import httpx
import polars as pl

from pumpfun.config import Config

log = logging.getLogger(__name__)

API = "https://api.dune.com/api/v1"
STATE = Path(".dune_query_id")

DAY_SQL = """
WITH legs AS (
  SELECT token_bought_mint_address AS mint, block_time,
         amount_usd / NULLIF(token_bought_amount, 0) AS px
  FROM dex_solana.trades
  WHERE project = 'pumpdotfun' AND block_date = DATE '{day}'
    AND token_bought_mint_address LIKE '%pump' AND amount_usd > 0
  UNION ALL
  SELECT token_sold_mint_address, block_time,
         amount_usd / NULLIF(token_sold_amount, 0)
  FROM dex_solana.trades
  WHERE project = 'pumpdotfun' AND block_date = DATE '{day}'
    AND token_sold_mint_address LIKE '%pump' AND amount_usd > 0
),
agg AS (
  SELECT mint,
         min(block_time) AS first_iv,
         min_by(px, block_time) AS px_first_open,
         max(px) AS px_high,
         min(px) AS px_low,
         count(*) AS n_trades
  FROM legs
  WHERE px IS NOT NULL AND px > 0
  GROUP BY mint
),
flagged AS (
  SELECT *,
         (px_high * 1e9 >= {fdv_usd} AND px_high / px_low >= {ratio}) AS is_cand,
         (mod(abs(from_big_endian_64(xxhash64(to_utf8(mint)))), 10000) < {rate_bp}) AS in_sample
  FROM agg
)
SELECT mint, cast(first_iv AS varchar) AS first_iv, px_first_open, px_high, px_low,
       n_trades, is_cand,
       (SELECT count(*) FROM flagged WHERE NOT is_cand) AS day_noncand,
       (SELECT count(*) FROM flagged WHERE NOT is_cand AND in_sample) AS day_noncand_sampled
FROM flagged
WHERE is_cand OR in_sample
"""


class DuneClient:
    def __init__(self) -> None:
        key = None
        for line in Path(".env").read_text().splitlines():
            if line.startswith("DUNE_API_KEY="):
                key = line.split("=", 1)[1].strip()
        if not key:
            raise SystemExit("DUNE_API_KEY missing from .env")
        self._http = httpx.Client(headers={"X-Dune-API-Key": key}, timeout=120)
        self.query_id = self._ensure_query()

    def _ensure_query(self) -> int:
        if STATE.exists():
            return int(STATE.read_text().strip())
        r = self._http.post(f"{API}/query", json={"name": "pumpfun-shape-history", "query_sql": "SELECT 1", "is_private": False})
        r.raise_for_status()
        qid = int(r.json()["query_id"])
        STATE.write_text(str(qid))
        return qid

    def run(self, sql: str, poll_s: float = 5.0, max_wait_s: float = 900.0) -> list[dict]:
        r = self._http.patch(f"{API}/query/{self.query_id}", json={"query_sql": sql})
        r.raise_for_status()
        r = self._http.post(f"{API}/query/{self.query_id}/execute", json={})
        r.raise_for_status()
        ex = r.json()["execution_id"]
        t0 = time.monotonic()
        while True:
            time.sleep(poll_s)
            rows: list[dict] = []
            offset = 0
            r = self._http.get(f"{API}/execution/{ex}/results?limit=30000&offset=0")
            j = r.json()
            state = j.get("state")
            if state == "QUERY_STATE_FAILED":
                raise RuntimeError(f"dune query failed: {str(j.get('error'))[:300]}")
            if state == "QUERY_STATE_COMPLETED":
                rows.extend(j["result"]["rows"])
                total = j["result"]["metadata"]["total_row_count"]
                while len(rows) < total:
                    offset += 30000
                    rr = self._http.get(f"{API}/execution/{ex}/results?limit=30000&offset={offset}")
                    rows.extend(rr.json()["result"]["rows"])
                return rows
            if time.monotonic() - t0 > max_wait_s:
                raise TimeoutError("dune query timed out")


def pull_day(cfg: Config, dune: DuneClient, day: str) -> Path:
    out = cfg.raw_dir / "bitquery" / f"{day}.parquet"
    if out.exists():
        return out
    rate_bp = int(round(cfg.prescreen.sample_rate_hist * 10000))
    sql = DAY_SQL.format(day=day, fdv_usd=cfg.prescreen.fdv_candidate_usd, ratio=1 + cfg.tp, rate_bp=rate_bp)
    rows = dune.run(sql)
    if not rows:
        raise RuntimeError(f"{day}: empty result")
    noncand = rows[0]["day_noncand"]
    sampled = rows[0]["day_noncand_sampled"]
    df = (
        pl.DataFrame(rows)
        .with_columns(
            first_iv=pl.col("first_iv").str.slice(0, 19).str.replace(" ", "T") + "Z",
            vol_usd=pl.lit(None, dtype=pl.Float64),
            n_intervals=pl.col("n_trades"),
            fdv_max=pl.col("px_high") * 1e9,
            block_date=pl.lit(day),
            pre_sampled=~pl.col("is_cand"),
            pre_weight=pl.when(pl.col("is_cand")).then(1.0).otherwise(noncand / max(sampled, 1)),
        )
        .drop("is_cand", "n_trades", "day_noncand", "day_noncand_sampled")
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(out)
    log.info("%s: %d rows (%d non-cand of which %d sampled) -> %s", day, df.height, noncand, sampled, out)
    return out
