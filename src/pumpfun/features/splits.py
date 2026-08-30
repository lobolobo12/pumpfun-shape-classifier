"""splits — time-based, creator-grouped (spec §9).

train: launch_day <  split_train_end
val:   split_train_end <= launch_day < split_val_end
test:  launch_day >= split_val_end
A creator appearing in an earlier split has all tokens removed from every later split
(creator-history features would otherwise leak across the boundary). Negatives are
downsampled to `neg_pos_ratio` per positive in TRAIN only; the base rate is persisted elsewhere.
"""

from __future__ import annotations

import polars as pl

from pumpfun.config import Config


def assign(cfg: Config, df: pl.DataFrame) -> tuple[pl.DataFrame, dict[str, int]]:
    df = df.with_columns(
        split=pl.when(pl.col("launch_day") < cfg.split_train_end)
        .then(pl.lit("train"))
        .when(pl.col("launch_day") < cfg.split_val_end)
        .then(pl.lit("val"))
        .otherwise(pl.lit("test"))
    )
    counts: dict[str, int] = {}
    train_creators = set(df.filter(pl.col("split") == "train")["creator"].to_list())
    val_creators = set(df.filter(pl.col("split") == "val")["creator"].to_list())
    before = df.height
    df = df.filter(~((pl.col("split") == "val") & pl.col("creator").is_in(list(train_creators))))
    df = df.filter(~((pl.col("split") == "test") & pl.col("creator").is_in(list(train_creators | val_creators))))
    counts["creator_straddle_dropped"] = before - df.height

    train = df.filter(pl.col("split") == "train")
    pos = train.filter(pl.col("label") == 1)
    neg = train.filter(pl.col("label") == 0)
    keep_neg = min(neg.height, int(round(pos.height * cfg.neg_pos_ratio)))
    neg = neg.sample(n=keep_neg, seed=cfg.seed) if keep_neg < neg.height else neg
    counts["train_negatives_dropped"] = train.height - pos.height - neg.height
    df = pl.concat([pos, neg, df.filter(pl.col("split") != "train")])
    for s in ("train", "val", "test"):
        part = df.filter(pl.col("split") == s)
        counts[f"{s}_n"] = part.height
        counts[f"{s}_pos"] = int(part["label"].sum())
    return df, counts
