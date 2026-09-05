"""build — labels + tapes -> data/processed/{features.parquet, sequences.npy, sequence_index.parquet}."""

from __future__ import annotations

import logging

import numpy as np
import polars as pl

from pumpfun.checks.schema import assert_causal
from pumpfun.config import Config
from pumpfun.features import sequence, splits, tabular
from pumpfun.ingest.to_parquet import read_trades
from pumpfun.reports import update_counts, write_json

log = logging.getLogger(__name__)


def run(cfg: Config) -> None:
    labels = pl.read_parquet(cfg.interim_dir / "labels.parquet")
    tokens = pl.read_parquet(cfg.tokens_path)
    trades = read_trades(cfg)
    wt = sequence.window_trades(cfg, trades, labels)
    # Belt and braces: the schema-level causality assertion per token.
    entry = dict(labels.select("mint", "entry_t").iter_rows())
    for (mint,), g in wt.group_by("mint"):
        assert_causal(g.with_columns(block_time=pl.col("seconds_since_launch")), int(entry[mint]), str(mint))

    labels = labels.filter(pl.col("mint").is_in(wt["mint"].unique().implode()))
    tab = tabular.build(cfg, wt, labels, tokens).join(tokens.select("mint", "creator", "source"), on="mint", how="left")
    strata_path = cfg.interim_dir / "strata.parquet"
    if strata_path.exists():
        tab = tab.join(
            pl.read_parquet(strata_path).select("mint", "stratum", pl.col("weight").alias("sample_weight")), on="mint", how="left"
        )
    else:
        tab = tab.with_columns(stratum=pl.lit("all"), sample_weight=pl.lit(1.0))
    tab, counts = splits.assign(cfg, tab)
    tab = tab.sort("launch_day", "mint")
    cfg.processed_dir.mkdir(parents=True, exist_ok=True)
    tab.write_parquet(cfg.processed_dir / "features.parquet")

    ordered = labels.join(tab.select("mint"), on="mint", how="inner").sort("mint")
    wt_ord = wt.filter(pl.col("mint").is_in(ordered["mint"].implode()))
    x, mints = sequence.encode(cfg, wt_ord, ordered)
    np.save(cfg.processed_dir / "sequences.npy", x)
    xt, _ = sequence.encode_trades(cfg, wt_ord, ordered, int(cfg.cnn["trade_steps"]))
    np.save(cfg.processed_dir / "sequences_trades.npy", xt)
    xb, _ = sequence.encode_botlive(cfg, wt_ord, ordered, int(cfg.cnn.get("botlive_steps", 128)))
    np.save(cfg.processed_dir / "sequences_botlive.npy", xb)
    pl.DataFrame({"mint": mints}).write_parquet(cfg.processed_dir / "sequence_index.parquet")

    update_counts(cfg.reports_dir, "features", {"labeled_in": labels.height, "features_out": tab.height, **counts})
    write_json(
        cfg.reports_dir / "features_summary.json",
        {
            "groups": tabular.GROUPS,
            "side": tabular.SIDE,
            "sequence_channels": sequence.CHANNELS,
            "sequence_shape": list(x.shape),
            "trade_channels": sequence.TRADE_CHANNELS,
            "trade_shape": list(xt.shape),
            "splits": counts,
        },
    )
    log.info("features: %d rows, sequences %s, splits %s", tab.height, x.shape, counts)
