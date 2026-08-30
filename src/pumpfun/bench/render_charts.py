"""render_charts — the milestone-0 images: line and bars only, nothing else.

Balanced seeded sample of labeled tokens; each chart shows the price line and
volume bars over [0, window_seconds) with no axes, ticks, text, colour cues or
identifying marks. File names are shuffled indices; the mint/label mapping
lives only in the manifest.
"""

from __future__ import annotations

import json
import logging
import random

import matplotlib
import numpy as np
import polars as pl

from pumpfun.config import Config
from pumpfun.features import sequence
from pumpfun.ingest.to_parquet import read_trades

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

log = logging.getLogger(__name__)

BG = "#e9e9e9"
LINE = "#222222"
BAR = "#8a8a8a"


def sample(cfg: Config, labels: pl.DataFrame) -> pl.DataFrame:
    n = cfg.bench.n_per_class
    pos = labels.filter(pl.col("label") == 1)
    neg = labels.filter(pl.col("label") == 0)
    if pos.height < n or neg.height < n:
        raise SystemExit(f"need {n} per class, have {pos.height} positives / {neg.height} negatives — fetch more first")
    picked = pl.concat([pos.sample(n=n, seed=cfg.seed), neg.sample(n=n, seed=cfg.seed + 1)])
    rng = random.Random(cfg.seed)
    order = list(range(picked.height))
    rng.shuffle(order)
    return picked[order].with_columns(chart_id=pl.int_range(pl.len()))


def render(cfg: Config, x: np.ndarray, path) -> None:
    w, h = cfg.bench.image_px
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100, facecolor=BG)
    ax1 = fig.add_axes([0.02, 0.32, 0.96, 0.66], facecolor=BG)
    ax2 = fig.add_axes([0.02, 0.02, 0.96, 0.27], facecolor=BG)
    price = np.exp(x[:, 0])  # relative price, shape only
    ax1.plot(np.arange(len(price)), price, color=LINE, linewidth=1.4)
    ax2.bar(np.arange(len(price)), x[:, 1], color=BAR, width=1.0)
    for ax in (ax1, ax2):
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        ax.margins(x=0)
    fig.savefig(path, dpi=100, facecolor=BG)
    plt.close(fig)


def run(cfg: Config) -> None:
    labels = pl.read_parquet(cfg.interim_dir / "labels.parquet")
    picked = sample(cfg, labels).sort("chart_id")
    trades = read_trades(cfg).filter(pl.col("mint").is_in(picked["mint"].implode()))
    wt = sequence.window_trades(cfg, trades, picked)
    x, mints = sequence.encode(cfg, wt, picked)
    out = cfg.reports_dir / "charts"
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.png"):
        f.unlink()
    pos = {m: i for i, m in enumerate(mints)}
    manifest = []
    for mint, label, cid, zone in picked.select("mint", "label", "chart_id", "in_zone").iter_rows():
        render(cfg, x[pos[mint]], out / f"{cid:03d}.png")
        manifest.append({"chart_id": cid, "mint": mint, "label": int(label), "in_zone": bool(zone)})
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))
    log.info("rendered %d charts -> %s", len(manifest), out)
