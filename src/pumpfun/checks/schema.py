"""schema — the Parquet schemas of the raw layer, and the causality assertion.

Spec §6 columns are kept verbatim; additive columns are marked. A frame that
does not match is rejected at write time, never silently coerced.
"""

from __future__ import annotations

import polars as pl

# data/raw/trades/{yyyy-mm}/*.parquet
TRADES_SCHEMA: dict[str, pl.DataType] = {
    "mint": pl.String,
    "signature": pl.String,  # dedupe key
    "slot": pl.Int64,
    "slot_index": pl.Int64,  # additive: position inside the slot (from slotIndexId); ordering key with slot
    "block_time": pl.Int64,  # unix seconds
    "seconds_since_launch": pl.Float64,
    "is_buy": pl.Boolean,
    "sol_amount": pl.Float64,  # curve-side SOL (fee-exclusive)
    "token_amount": pl.Float64,  # whole tokens
    "trader": pl.String,
    "program": pl.String,  # additive: pump | pump_amm | other
    "curve_sol_after": pl.Float64,  # real SOL in the curve after this trade (pool: real quote)
    "curve_token_after": pl.Float64,  # additive: real tokens left in the curve (pool: base reserve)
    "price_sol": pl.Float64,  # marginal price after this trade (API priceSol)
    "fill_price_sol": pl.Float64,  # additive: realized average fill of THIS trade (API fillPriceSol)
}

# data/raw/tokens.parquet
TOKENS_SCHEMA: dict[str, pl.DataType] = {
    "mint": pl.String,
    "creator": pl.String,
    "launch_time": pl.Int64,  # unix seconds
    "launch_time_ms": pl.Int64,  # additive: creation ms, needed for sub-second ordering vs trades
    "graduated": pl.Boolean,
    "graduation_time": pl.Int64,  # nullable
    "source": pl.String,  # additive: how the universe saw it (sweep | pumpportal | ...)
    "first_seen_age_s": pl.Float64,  # additive
    "launch_day": pl.String,  # additive: YYYY-MM-DD in split_timezone
    "mayhem": pl.Boolean,  # additive: is_mayhem_mode from the on-chain create frame; null when no frame was recorded
    "meta_host": pl.String,  # additive: host of the metadata URI from the create frame (launch-origin fingerprint)
}


class SchemaError(ValueError):
    pass


def assert_schema(df: pl.DataFrame, schema: dict[str, pl.DataType], name: str) -> None:
    missing = [c for c in schema if c not in df.columns]
    extra = [c for c in df.columns if c not in schema]
    if missing or extra:
        raise SchemaError(f"{name}: missing={missing} extra={extra}")
    for c, t in schema.items():
        if df.schema[c] != t:
            raise SchemaError(f"{name}.{c}: expected {t}, got {df.schema[c]}")


def conform(df: pl.DataFrame, schema: dict[str, pl.DataType], name: str) -> pl.DataFrame:
    """Select + cast into the schema's column order; raises on missing columns."""
    missing = [c for c in schema if c not in df.columns]
    if missing:
        raise SchemaError(f"{name}: missing={missing}")
    out = df.select([pl.col(c).cast(t) for c, t in schema.items()])
    assert_schema(out, schema, name)
    return out


def assert_causal(trades: pl.DataFrame, entry_time: int, mint: str) -> None:
    """Every row a feature may see must be strictly before the entry timestamp."""
    if trades.height == 0:
        return
    mx = int(trades["block_time"].max())  # type: ignore[arg-type]
    if mx >= entry_time:
        raise AssertionError(f"{mint}: feature input contains block_time {mx} >= entry_time {entry_time}")
