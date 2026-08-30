"""cnn — milestone 5: a small dilated residual 1-D CNN over the 6-channel window, plus a side vector.

About 200k parameters, no pretrained weights, class-weighted BCE, early stopping on the
validation split, several seeds averaged. The side vector is the standardised tabular
feature set (shape + holders + creator); a `--set cnn.side=false` run isolates the sequence.
"""

from __future__ import annotations

import logging
import math

import numpy as np
import polars as pl
import torch
from torch import nn

from pumpfun.config import Config
from pumpfun.features.tabular import CREATOR, HOLDERS, SHAPE
from pumpfun.models import metrics
from pumpfun.reports import write_json

log = logging.getLogger(__name__)

SIDE_COLS = SHAPE + HOLDERS + CREATOR


class Block(nn.Module):
    def __init__(self, ch: int, k: int, dilation: int, dropout: float):
        super().__init__()
        pad = (k - 1) * dilation // 2
        self.net = nn.Sequential(
            nn.Conv1d(ch, ch, k, padding=pad, dilation=dilation),
            nn.BatchNorm1d(ch),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Conv1d(ch, ch, k, padding=pad, dilation=dilation),
            nn.BatchNorm1d(ch),
        )
        self.act = nn.GELU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.act(x + self.net(x))


class ShapeNet(nn.Module):
    def __init__(self, in_ch: int, side_dim: int, ch: int, blocks: int, k: int, dropout: float):
        super().__init__()
        self.stem = nn.Conv1d(in_ch, ch, 1)
        self.blocks = nn.Sequential(*[Block(ch, k, 2**i, dropout) for i in range(blocks)])
        self.side = nn.Sequential(nn.Linear(side_dim, ch), nn.GELU(), nn.Dropout(dropout)) if side_dim else None
        self.head = nn.Sequential(
            nn.Linear(2 * ch + (ch if side_dim else 0), ch), nn.GELU(), nn.Dropout(dropout), nn.Linear(ch, 1)
        )

    def forward(self, x: torch.Tensor, side: torch.Tensor | None) -> torch.Tensor:
        h = self.blocks(self.stem(x))
        pooled = torch.cat([h.mean(dim=2), h.amax(dim=2)], dim=1)
        if self.side is not None and side is not None:
            pooled = torch.cat([pooled, self.side(side)], dim=1)
        return self.head(pooled).squeeze(1)


def _device() -> torch.device:
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _prep_seq(x: np.ndarray, encoding: str) -> np.ndarray:
    """Per-channel scaling that keeps the shape: counts -> log1p; trade encoding is already scaled."""
    x = x.copy()
    if encoding == "steps":
        x[:, :, 2] = np.log1p(x[:, :, 2])
        x[:, :, 3] = np.log1p(x[:, :, 3])
    return x.transpose(0, 2, 1).astype(np.float32)  # [N, C, T]


def _load(cfg: Config, enc: str) -> tuple[pl.DataFrame, np.ndarray]:
    feats = pl.read_parquet(cfg.processed_dir / "features.parquet")
    labels = pl.read_parquet(cfg.interim_dir / "labels.parquet").select("mint", "entry_cost_sol", "exit_net_sol")
    feats = feats.join(labels, on="mint", how="left")
    seq = np.load(cfg.processed_dir / ("sequences.npy" if enc == "steps" else "sequences_trades.npy"))
    idx = pl.read_parquet(cfg.processed_dir / "sequence_index.parquet").with_row_index("row")
    feats = feats.join(idx, on="mint", how="inner")
    return feats, seq


def train_one(
    cfg: Config, seed: int, tr: pl.DataFrame, va: pl.DataFrame, seq: np.ndarray, side_stats, use_side: bool, dev: torch.device
):
    torch.manual_seed(seed)
    np.random.seed(seed)
    c = cfg.cnn
    xs = torch.tensor(_prep_seq(seq[tr["row"].to_numpy()], str(cfg.cnn.get("encoding", "steps"))))
    xv = torch.tensor(_prep_seq(seq[va["row"].to_numpy()], str(cfg.cnn.get("encoding", "steps"))))
    ys = torch.tensor(tr["label"].to_numpy(), dtype=torch.float32)
    yv = torch.tensor(va["label"].to_numpy(), dtype=torch.float32)
    mean, std = side_stats
    ss = torch.tensor(((tr.select(SIDE_COLS).fill_null(0).to_numpy() - mean) / std).astype(np.float32)) if use_side else None
    sv = torch.tensor(((va.select(SIDE_COLS).fill_null(0).to_numpy() - mean) / std).astype(np.float32)) if use_side else None
    model = ShapeNet(xs.shape[1], len(SIDE_COLS) if use_side else 0, c["channels"], c["blocks"], c["kernel"], c["dropout"]).to(
        dev
    )
    n_params = sum(p.numel() for p in model.parameters())
    pos_w = torch.tensor([(ys == 0).sum() / max(1.0, (ys == 1).sum())], device=dev)
    loss_fn = nn.BCEWithLogitsLoss(pos_weight=pos_w)
    opt = torch.optim.AdamW(model.parameters(), lr=c["lr"], weight_decay=1e-4)
    best, best_state, bad = -math.inf, None, 0
    bs = c["batch_size"]
    for epoch in range(c["epochs"]):
        model.train()
        perm = torch.randperm(len(ys))
        for i in range(0, len(ys), bs):
            b = perm[i : i + bs]
            opt.zero_grad()
            out = model(xs[b].to(dev), None if ss is None else ss[b].to(dev))
            loss = loss_fn(out, ys[b].to(dev))
            loss.backward()
            opt.step()
        model.eval()
        with torch.no_grad():
            pv = torch.sigmoid(model(xv.to(dev), None if sv is None else sv.to(dev))).cpu().numpy()
        from sklearn.metrics import average_precision_score

        ap = average_precision_score(yv.numpy(), pv)
        if ap > best:
            best, bad = ap, 0
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        else:
            bad += 1
            if bad >= c["patience"]:
                break
        log.info("seed %d epoch %d val PR-AUC %.4f (best %.4f)", seed, epoch, ap, best)
    model.load_state_dict(best_state)
    return model, best, n_params


def predict(model, seq_rows: np.ndarray, side: np.ndarray | None, dev: torch.device, encoding: str = "steps") -> np.ndarray:
    model.eval()
    with torch.no_grad():
        x = torch.tensor(_prep_seq(seq_rows, encoding)).to(dev)
        s = None if side is None else torch.tensor(side.astype(np.float32)).to(dev)
        return torch.sigmoid(model(x, s)).cpu().numpy()


def run(cfg: Config) -> dict:
    enc = str(cfg.cnn.get("encoding", "steps"))
    feats, seq = _load(cfg, enc)
    use_side = bool(cfg.cnn.get("side", True))
    tr = feats.filter(pl.col("split") == "train")
    va = feats.filter(pl.col("split") == "val")
    te = feats.filter(pl.col("split") == "test")
    if min(tr.height, va.height, te.height) == 0:
        raise SystemExit("empty split")
    side_tr = tr.select(SIDE_COLS).fill_null(0).to_numpy()
    side_stats = (side_tr.mean(axis=0), side_tr.std(axis=0) + 1e-6)
    dev = _device()
    log.info("device %s, train %d val %d test %d, side=%s", dev, tr.height, va.height, te.height, use_side)
    preds = []
    vals = []
    n_params = 0
    for s in range(int(cfg.cnn["seeds"])):
        model, best_val, n_params = train_one(cfg, cfg.seed + s, tr, va, seq, side_stats, use_side, dev)
        side_te = ((te.select(SIDE_COLS).fill_null(0).to_numpy() - side_stats[0]) / side_stats[1]) if use_side else None
        preds.append(predict(model, seq[te["row"].to_numpy()], side_te, dev, enc))
        vals.append(best_val)
    p = np.mean(preds, axis=0)
    name = f"cnn_{enc}" + ("+side" if use_side else "")
    result = metrics.evaluate(cfg, te, p)
    result["val_pr_auc_per_seed"] = [float(v) for v in vals]
    result["n_params"] = int(n_params)
    report = {"results": {name: result}, "config": cfg.cnn, "preset": cfg.preset}
    write_json(cfg.reports_dir / f"m5_{name}.json", report)
    md = [f"# Milestone 5 — {name} ({n_params:,} params)\n", metrics.comparison_table(cfg, {name: result}), ""]
    (cfg.reports_dir / f"m5_{name}.md").write_text("\n".join(md) + "\n")
    log.info(
        "%s: test PR-AUC %.3f (base %.3f) -> %s", name, result["pr_auc"], result["base_rate"], cfg.reports_dir / f"m5_{name}.md"
    )
    return report
