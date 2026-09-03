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
from pumpfun.features.wallets import WALLETS
from pumpfun.models import metrics
from pumpfun.reports import append_history, write_json

log = logging.getLogger(__name__)

SIDE_COLS = SHAPE + HOLDERS + CREATOR + WALLETS


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


def _recent(cfg: Config, tr: pl.DataFrame) -> pl.DataFrame:
    from datetime import date, timedelta

    days = int(cfg.cnn.get("finetune_days", 0) or 0)
    if days <= 0:
        return tr.head(0)
    cut = (date.fromisoformat(cfg.split_train_end) - timedelta(days=days)).isoformat()
    return tr.filter(pl.col("launch_day") >= cut)


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
    ss = (
        torch.tensor(((tr.select(SIDE_COLS).fill_null(0).fill_nan(0).to_numpy() - mean) / std).astype(np.float32))
        if use_side
        else None
    )
    sv = (
        torch.tensor(((va.select(SIDE_COLS).fill_null(0).fill_nan(0).to_numpy() - mean) / std).astype(np.float32))
        if use_side
        else None
    )
    model = ShapeNet(xs.shape[1], len(SIDE_COLS) if use_side else 0, c["channels"], c["blocks"], c["kernel"], c["dropout"]).to(
        dev
    )
    n_params = sum(p.numel() for p in model.parameters())
    pre = pretrained_path(cfg)
    if pre is not None:
        state = torch.load(pre, map_location=dev)
        missing, unexpected = model.load_state_dict(state, strict=False)
        loaded = [k for k in state if k not in unexpected]
        log.info("loaded %d pretrained tensors from %s (head left random)", len(loaded), pre.name)
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
    # Fine-tune on the most recent slice at a low learning rate; keep only if validation improves.
    ft = _recent(cfg, tr)
    if ft.height > 50 and ft.height < tr.height:
        idx = pl.Series(range(tr.height)).filter(tr["launch_day"].is_in(ft["launch_day"].implode()))
        xf = xs[idx.to_list()]
        yf = ys[idx.to_list()]
        sf = None if ss is None else ss[idx.to_list()]
        opt = torch.optim.AdamW(model.parameters(), lr=c["lr"] / 5, weight_decay=1e-4)
        pre_best = best
        for _ in range(5):
            model.train()
            perm = torch.randperm(len(yf))
            for i in range(0, len(yf), bs):
                b = perm[i : i + bs]
                opt.zero_grad()
                out = model(xf[b].to(dev), None if sf is None else sf[b].to(dev))
                loss_fn(out, yf[b].to(dev)).backward()
                opt.step()
            model.eval()
            with torch.no_grad():
                pv = torch.sigmoid(model(xv.to(dev), None if sv is None else sv.to(dev))).cpu().numpy()
            from sklearn.metrics import average_precision_score

            ap = average_precision_score(yv.numpy(), pv)
            if ap > best:
                best = ap
                best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        model.load_state_dict(best_state)
        log.info("seed %d fine-tune: val %.4f -> %.4f", seed, pre_best, best)
    return model, best, n_params


PRETRAIN_FILE = "cnn_pretrained_{enc}.pt"


def pretrained_path(cfg: Config):
    """The pretrained trunk for the current encoding, when `cnn.pretrained: true` and the file exists."""
    if not bool(cfg.cnn.get("pretrained", False)):
        return None
    p = cfg.processed_dir / PRETRAIN_FILE.format(enc=str(cfg.cnn.get("encoding", "steps")))
    return p if p.exists() else None


def pretrain(cfg: Config) -> dict:
    """Self-supervised pretraining of the trunk on every tape, labels never touched.

    Each tape gets `cnn.pretrain.cuts_per_tape` random cuts in [cross_min_age, window] seconds; the trunk
    sees the trades before a cut (same encoding as the classifier) and regresses, for every horizon in
    `cnn.pretrain.horizons_s`, the log change of curve SOL from the cut to cut+horizon. Tapes launched on
    or after split_train_end are excluded, so nothing from a validation or test day is ever seen. Saves
    stem + blocks only; the classifier head always starts random.
    """
    from pumpfun.features import sequence
    from pumpfun.ingest.to_parquet import read_trades

    pc = cfg.cnn.get("pretrain", {}) or {}
    enc = str(cfg.cnn.get("encoding", "steps"))
    if enc != "trades":
        raise SystemExit("pretraining is implemented for cnn.encoding=trades")
    horizons = [float(h) for h in (pc.get("horizons_s") or [pc.get("horizon_s", 60)])]
    max_mints = int(pc.get("max_mints", 60000))
    cuts_per = max(1, int(pc.get("cuts_per_tape", 1)))
    rng = np.random.default_rng(cfg.seed)
    tokens = pl.read_parquet(cfg.tokens_path).select("mint", "launch_day", "mayhem")
    trades = read_trades(cfg)
    mints = (
        trades.select("mint")
        .unique()
        .collect()
        .join(tokens, on="mint", how="inner")
        .filter((pl.col("launch_day") < cfg.split_train_end) & ~pl.col("mayhem").fill_null(False))
    )
    if mints.height > max_mints:
        mints = mints.sample(max_mints, seed=cfg.seed)
    lo, hi = float(cfg.raw.get("cross_min_age_seconds", 10)), float(cfg.window_seconds)
    # one pseudo-coin per (tape, cut): "mint#k" so the shared window/encoder code keys on it unchanged
    cuts = pl.concat(
        [
            mints.select(pl.col("mint").alias("src")).with_columns(
                entry_t=pl.Series(rng.uniform(lo, hi, mints.height)), k=pl.lit(k)
            )
            for k in range(cuts_per)
        ]
    ).with_columns(mint=pl.col("src") + "#" + pl.col("k").cast(pl.String))
    t = (
        trades.rename({"mint": "src"})
        .join(cuts.lazy(), on="src", how="inner")
        .sort("mint", "slot", "slot_index")
        .with_columns(rank=pl.int_range(pl.len()).over("mint"))
    )
    before = t.filter(pl.col("seconds_since_launch") < pl.col("entry_t"))
    last_before = before.group_by("mint").agg(
        n_visible=pl.len(), entry_price=pl.col("price_sol").last(), sol_at=pl.col("curve_sol_after").last()
    )
    pseudo = cuts.lazy().join(last_before, on="mint", how="inner")
    tcols = []
    for h in horizons:
        col = f"target_{int(h)}"
        after = (
            t.filter(pl.col("seconds_since_launch") < pl.col("entry_t") + h)
            .group_by("mint")
            .agg(pl.col("curve_sol_after").last().alias(f"sol_after_{int(h)}"))
        )
        pseudo = pseudo.join(after, on="mint", how="inner").with_columns(
            (pl.col(f"sol_after_{int(h)}") / pl.col("sol_at")).log().clip(-1.0, 2.0).alias(col)
        )
        tcols.append(col)
    pseudo = pseudo.filter((pl.col("n_visible") >= 5) & (pl.col("entry_price") > 0) & (pl.col("sol_at") > 0)).collect()
    log.info(
        "pretrain set: %d cuts over %d tapes; %s",
        pseudo.height,
        pseudo["src"].n_unique(),
        ", ".join(f"{c}: mean {pseudo[c].mean():.3f} std {pseudo[c].std():.3f}" for c in tcols),
    )
    wt = sequence.window_trades(cfg, t.drop("src", "k").select(trades.collect_schema().names()), pseudo)
    x, order = sequence.encode_trades(cfg, wt, pseudo, int(cfg.cnn["trade_steps"]))
    y = pl.DataFrame({"mint": order}).join(pseudo.select("mint", *tcols), on="mint", how="left").select(tcols).to_numpy()
    xs = torch.tensor(_prep_seq(x, enc))
    ys = torch.tensor(y.astype(np.float32))
    ys = (ys - ys.mean(dim=0)) / (ys.std(dim=0) + 1e-6)
    dev = _device()
    c = cfg.cnn
    torch.manual_seed(cfg.seed)
    model = ShapeNet(xs.shape[1], 0, c["channels"], c["blocks"], c["kernel"], c["dropout"]).to(dev)
    model.head[-1] = nn.Linear(c["channels"], len(tcols)).to(dev)  # one output per horizon
    opt = torch.optim.AdamW(model.parameters(), lr=c["lr"], weight_decay=1e-4)
    n_val = max(500, int(0.05 * len(ys)))
    perm = torch.randperm(len(ys))
    va_idx, tr_idx = perm[:n_val], perm[n_val:]
    bs = int(c["batch_size"])
    best, best_state, bad = math.inf, None, 0
    for epoch in range(int(pc.get("epochs", 15))):
        model.train()
        p2 = tr_idx[torch.randperm(len(tr_idx))]
        for i in range(0, len(p2), bs):
            b = p2[i : i + bs]
            opt.zero_grad()
            loss = nn.functional.mse_loss(model(xs[b].to(dev), None), ys[b].to(dev))
            loss.backward()
            opt.step()
        model.eval()
        with torch.no_grad():
            vl = float(nn.functional.mse_loss(model(xs[va_idx].to(dev), None), ys[va_idx].to(dev)))
        log.info("pretrain epoch %d val mse %.4f (best %.4f)", epoch, vl, best)
        if vl < best - 1e-4:
            best, bad = vl, 0
            best_state = {k: v.detach().clone().cpu() for k, v in model.state_dict().items() if not k.startswith("head.")}
        else:
            bad += 1
            if bad >= int(c["patience"]):
                break
    out = cfg.processed_dir / PRETRAIN_FILE.format(enc=enc)
    torch.save(best_state, out)
    summary = {
        "n_cuts": int(len(ys)),
        "n_tapes": int(pseudo["src"].n_unique()),
        "val_mse": best,
        "horizons_s": horizons,
        "cuts_per_tape": cuts_per,
        "path": str(out),
    }
    write_json(cfg.reports_dir / "cnn_pretrain.json", summary)
    log.info("pretrained trunk -> %s (val mse %.4f, unit-variance targets)", out, best)
    return summary


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
    if str(cfg.raw.get("population", "all")) == "active":
        feats = feats.filter(pl.col("active_at_entry").fill_null(False))
    tr = feats.filter(pl.col("split") == "train")
    va = feats.filter(pl.col("split") == "val")
    te = feats.filter(pl.col("split") == "test")
    if min(tr.height, va.height, te.height) == 0:
        raise SystemExit("empty split")
    side_tr = tr.select(SIDE_COLS).fill_null(0).fill_nan(0).to_numpy()
    side_stats = (side_tr.mean(axis=0), side_tr.std(axis=0) + 1e-6)
    dev = _device()
    log.info("device %s, train %d val %d test %d, side=%s", dev, tr.height, va.height, te.height, use_side)
    preds = []
    vals = []
    n_params = 0
    for s in range(int(cfg.cnn["seeds"])):
        model, best_val, n_params = train_one(cfg, cfg.seed + s, tr, va, seq, side_stats, use_side, dev)
        side_te = (
            ((te.select(SIDE_COLS).fill_null(0).fill_nan(0).to_numpy() - side_stats[0]) / side_stats[1]) if use_side else None
        )
        preds.append(predict(model, seq[te["row"].to_numpy()], side_te, dev, enc))
        vals.append(best_val)
    p = np.mean(preds, axis=0)
    name = f"cnn_{enc}" + ("+side" if use_side else "") + ("+pre" if pretrained_path(cfg) is not None else "")
    result = metrics.evaluate(cfg, te, p)
    metrics.save_predictions(cfg, name, te, p)
    result["val_pr_auc_per_seed"] = [float(v) for v in vals]
    result["n_params"] = int(n_params)
    report = {"results": {name: result}, "config": cfg.cnn, "preset": cfg.preset}
    write_json(cfg.reports_dir / f"m5_{name}.json", report)
    append_history(
        cfg.reports_dir,
        {
            "model": name,
            "mode": cfg.decision_mode,
            "splits": {"train_end": cfg.split_train_end, "val_end": cfg.split_val_end},
            "test_n": result["n"],
            "test_pos": result["positives"],
            "base_rate": result["base_rate"],
            "pr_auc": result["pr_auc"],
            "roc_auc": result["roc_auc"],
            "p_at_10pct": result["precision_at"]["0.1"]["precision"],
            "pnl_at_10pct": result["pnl_at"]["0.1"]["pnl_sol"],
            "pnl_ex_top3": result["pnl_at"]["0.1"]["pnl_ex_top3_sol"],
            "weighted_pr_auc": (result.get("weighted") or {}).get("pr_auc"),
            "weighted_base_rate": (result.get("weighted") or {}).get("base_rate"),
            "serial_launcher": result.get("slice_serial_launcher", {}).get("pr_auc"),
            "train_n": tr.height,
        },
    )
    md = [f"# Milestone 5 — {name} ({n_params:,} params)\n", metrics.comparison_table(cfg, {name: result}), ""]
    (cfg.reports_dir / f"m5_{name}.md").write_text("\n".join(md) + "\n")
    log.info(
        "%s: test PR-AUC %.3f (base %.3f) -> %s", name, result["pr_auc"], result["base_rate"], cfg.reports_dir / f"m5_{name}.md"
    )
    return report
