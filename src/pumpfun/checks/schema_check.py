"""schema_check — every raw Parquet on disk matches the spec's schema; duplicates by signature are zero."""

from __future__ import annotations

import logging

import polars as pl

from pumpfun.checks.schema import TOKENS_SCHEMA, TRADES_SCHEMA, assert_schema
from pumpfun.config import Config

log = logging.getLogger(__name__)


def run(cfg: Config) -> None:
    tokens = pl.read_parquet(cfg.tokens_path)
    assert_schema(tokens, TOKENS_SCHEMA, "tokens")
    if tokens["mint"].n_unique() != tokens.height:
        raise SystemExit("tokens.parquet has duplicate mints")
    n_files = 0
    for f in sorted(cfg.trades_dir.glob("*/*.parquet")):
        df = pl.read_parquet(f)
        assert_schema(df, TRADES_SCHEMA, f.name)
        dup = df.height - df["signature"].n_unique()
        if dup:
            raise SystemExit(f"{f}: {dup} duplicate signatures")
        unknown = df.filter(~pl.col("mint").is_in(tokens["mint"].implode())).height
        if unknown:
            raise SystemExit(f"{f}: {unknown} rows for mints not in tokens.parquet")
        n_files += 1
    log.info("schema ok: tokens %d rows, %d trade files", tokens.height, n_files)
