"""xgb — milestone 4: gradient-boosted trees on the tabular features, three feature groups, taken seriously.

Variants: shape only (the spec's chart hypothesis in isolation), holders only, shape + holders (+ creator).
Also the trading repo's logistic recipe (analyse.ts MODEL_FEATURES, translated) for continuity.
Early stopping on the validation split; the test split is touched once per variant.
"""

from __future__ import annotations

import json
import logging
from datetime import date
from pathlib import Path

import numpy as np
import polars as pl
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from pumpfun.config import Config
from pumpfun.features.tabular import BOTLIVE, CONTEXT, CREATOR, HOLDERS, SHAPE
from pumpfun.features.wallets import WALLETS
from pumpfun.models import metrics
from pumpfun.reports import append_history, write_json

log = logging.getLogger(__name__)

VARIANTS = {
    "xgb_shape": SHAPE,
    "xgb_holders": HOLDERS,
    "xgb_shape+holders": SHAPE + HOLDERS,
    "xgb_all": SHAPE + HOLDERS + CREATOR + CONTEXT,
    "xgb_context": CONTEXT,
    "xgb_wallets": WALLETS,
    "xgb_holders+wallets": HOLDERS + WALLETS,
    "xgb_all+wallets": SHAPE + HOLDERS + CREATOR + CONTEXT + WALLETS,
    "xgb_botlive": BOTLIVE,
    "xgb_botlive+context": BOTLIVE + CONTEXT,
}
# Trained for money rather than for the label: regress the realized log exit multiple (fees included),
# then rank by the prediction. Same features as the strongest tabular models.
PNL_VARIANTS = {
    "xgb_pnl:all+wallets": SHAPE + HOLDERS + CREATOR + CONTEXT + WALLETS,
    "xgb_pnl:botlive+context": BOTLIVE + CONTEXT,
}
PNL_CLIP = (-1.5, 1.5)
RECENT_SOURCES = ["sweep", "pumpportal", "curve", "graduated", "tracked"]
# analyse.ts MODEL_FEATURES, translated to our names (sameSlotShare and ageS have no counterpart here).
LOGISTIC_FEATURES = [
    "top10_share",
    "dev_share",
    "launch_bundle_share",
    "same_size_share",
    "exited_share",
    "gini_hold",
    "holders_n",
    "sell_share_sol",
    "max_drawdown",
    "lows_per_min",
    "step_gini",
    "buy_size_cv",
    "iti_cv",
    "sol_last60",
    "buyers_last60",
    "biggest_buy_vs_curve",
    "from_peak",
]


def _xy(df: pl.DataFrame, cols: list[str]) -> tuple[np.ndarray, np.ndarray]:
    x = df.select(cols).to_numpy().astype(np.float32)
    return x, df["label"].to_numpy().astype(int)


def recency_weights(cfg: Config, df: pl.DataFrame) -> np.ndarray | None:
    """0.5 ** (age_days / half_life), age measured back from split_train_end. None when disabled."""
    hl = float(cfg.train.get("recency_half_life_days", 0) or 0)
    if hl <= 0:
        return None
    anchor = date.fromisoformat(cfg.split_train_end).toordinal()
    days = np.array([anchor - date.fromisoformat(d).toordinal() for d in df["launch_day"]], dtype=float)
    return (0.5 ** (np.clip(days, 0, None) / hl)).astype(np.float32)


def fit_xgb(cfg: Config, train: pl.DataFrame, val: pl.DataFrame, cols: list[str]) -> xgb.XGBClassifier:
    xt, yt = _xy(train, cols)
    xv, yv = _xy(val, cols)
    p = cfg.xgb
    spw = float((yt == 0).sum() / max(1, (yt == 1).sum()))
    model = xgb.XGBClassifier(
        n_estimators=p["n_estimators"],
        max_depth=p["max_depth"],
        learning_rate=p["learning_rate"],
        subsample=p["subsample"],
        colsample_bytree=p["colsample_bytree"],
        scale_pos_weight=spw,
        eval_metric="aucpr",
        early_stopping_rounds=p["early_stopping_rounds"],
        random_state=cfg.seed,
        n_jobs=4,
    )
    w = recency_weights(cfg, train)
    model.fit(xt, yt, sample_weight=w, eval_set=[(xv, yv)], verbose=False)
    return model


def _pnl_target(df: pl.DataFrame) -> np.ndarray:
    m = (df["exit_net_sol"] / df["entry_cost_sol"]).to_numpy().astype(np.float64)
    return np.clip(np.log(np.clip(m, 1e-3, None)), *PNL_CLIP).astype(np.float32)


def fit_xgb_reg(cfg: Config, train: pl.DataFrame, val: pl.DataFrame, cols: list[str]) -> xgb.XGBRegressor:
    xt, _ = _xy(train, cols)
    xv, _ = _xy(val, cols)
    p = cfg.xgb
    model = xgb.XGBRegressor(
        n_estimators=p["n_estimators"],
        max_depth=p["max_depth"],
        learning_rate=p["learning_rate"],
        subsample=p["subsample"],
        colsample_bytree=p["colsample_bytree"],
        objective="reg:squarederror",
        eval_metric="rmse",
        early_stopping_rounds=p["early_stopping_rounds"],
        random_state=cfg.seed,
        n_jobs=4,
    )
    model.fit(xt, _pnl_target(train), sample_weight=recency_weights(cfg, train), eval_set=[(xv, _pnl_target(val))], verbose=False)
    return model


def model_dir(cfg: Config) -> Path:
    return cfg.processed_dir / "models" / cfg.decision_mode


def replace_seed(cfg: Config, seed: int) -> Config:
    import dataclasses

    return dataclasses.replace(cfg, seed=seed)


def save_model(
    cfg: Config, name: str, bag: list, cols: list[str], test_scores: np.ndarray, test_pnl: np.ndarray | None = None
) -> None:
    """Boosters (one file per seed) + feature list + the held-out score distribution (for live percentiles)."""
    d = model_dir(cfg)
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob(f"{name}.*.ubj"):
        old.unlink()
    for k, m in enumerate(bag):
        m.get_booster().save_model(str(d / (f"{name}.ubj" if k == 0 else f"{name}.{k}.ubj")))
    (d / f"{name}.json").write_text(
        json.dumps(
            {
                "model": name,
                "mode": cfg.decision_mode,
                "features": cols,
                "bag": len(bag),
                "splits": {"train_end": cfg.split_train_end, "val_end": cfg.split_val_end},
                "test_scores": [float(s) for s in np.sort(test_scores)],
                # realized PnL (SOL, fees included) of each held-out row, in the same order: the EV gate's table
                "test_pnl": None if test_pnl is None else [float(v) for v in test_pnl[np.argsort(test_scores)]],
            }
        )
    )


def fit_logistic(train: pl.DataFrame, cols: list[str]) -> tuple[StandardScaler, LogisticRegression]:
    xt, yt = _xy(train, cols)
    xt = np.log1p(np.clip(xt, 0, None))
    sc = StandardScaler().fit(xt)
    lr = LogisticRegression(C=100.0, max_iter=3000, class_weight="balanced").fit(sc.transform(xt), yt)
    return sc, lr


def run(cfg: Config) -> dict:
    feats = pl.read_parquet(cfg.processed_dir / "features.parquet")
    labels = pl.read_parquet(cfg.interim_dir / "labels.parquet").select("mint", "entry_cost_sol", "exit_net_sol")
    feats = feats.join(labels, on="mint", how="left")
    if str(cfg.raw.get("population", "all")) == "active":
        feats = feats.filter(pl.col("active_at_entry").fill_null(False))
    train = feats.filter(pl.col("split") == "train")
    val = feats.filter(pl.col("split") == "val")
    test = feats.filter(pl.col("split") == "test")
    suffix = ""
    min_day = str(cfg.train.get("min_launch_day") or "")
    if min_day:
        # regime cut: the May-July 2026 hot market (crossing win rate ~50 % vs ~20 % since August) misleads a
        # model trading now; cut chosen with Lovro on 5 Sep
        train = train.filter(pl.col("launch_day") >= min_day)
    if bool(cfg.train.get("recent_only", False)) and "source" in train.columns:
        # the live collector's eras only (no Bitquery/Dune history): regime-matched but small
        train = train.filter(pl.col("source").is_in(RECENT_SOURCES))
        suffix = "+recent"
    log.info(
        "train %d (%d pos) val %d (%d pos) test %d (%d pos)",
        train.height,
        train["label"].sum(),
        val.height,
        val["label"].sum(),
        test.height,
        test["label"].sum(),
    )
    if min(train.height, val.height, test.height) == 0:
        raise SystemExit("empty split — check split dates in config.yaml against the labeled days")

    results: dict[str, dict] = {}
    importances: dict[str, dict[str, float]] = {}
    n_bag = int(cfg.xgb.get("bag_seeds", 1) or 1)
    for base_name, cols in {**VARIANTS, **PNL_VARIANTS}.items():
        name = base_name + suffix
        is_pnl = base_name in PNL_VARIANTS
        fit = fit_xgb_reg if is_pnl else fit_xgb
        # bag of seeds: early stopping on one small validation day is noisy; served models always >= 5
        k_bag = max(n_bag, 5) if base_name.startswith("xgb_botlive") else n_bag
        bag = [fit(replace_seed(cfg, cfg.seed + k), train, val, cols) for k in range(k_bag)]
        model = bag[0]

        def score(df: pl.DataFrame, cols=cols, is_pnl=is_pnl, bag=bag) -> np.ndarray:
            x = _xy(df, cols)[0]
            return np.mean([m.predict(x) if is_pnl else m.predict_proba(x)[:, 1] for m in bag], axis=0)

        p = score(test)
        results[name] = metrics.evaluate(cfg, test, p)
        metrics.save_predictions(cfg, name, test, p)
        save_model(cfg, name, bag, cols, p, (test["exit_net_sol"] - test["entry_cost_sol"]).to_numpy())
        results[name]["best_iteration"] = int(model.best_iteration)
        results[name]["bag"] = k_bag
        results[name]["val_pr_auc"] = metrics.evaluate(cfg, val, score(val))["pr_auc"]
        gain = model.get_booster().get_score(importance_type="gain")
        importances[name] = {cols[int(k[1:])]: round(v, 3) for k, v in sorted(gain.items(), key=lambda kv: -kv[1])[:15]}
        log.info("%s: test PR-AUC %.3f (base %.3f)", name, results[name]["pr_auc"], results[name]["base_rate"])
    sc, lr = fit_logistic(train, LOGISTIC_FEATURES)
    p = lr.predict_proba(sc.transform(np.log1p(np.clip(_xy(test, LOGISTIC_FEATURES)[0], 0, None))))[:, 1]
    results["logistic_repo_recipe"] = metrics.evaluate(cfg, test, p)

    report = {
        "results": results,
        "importances_gain_top15": importances,
        "splits": {s: {"n": d.height, "pos": int(d["label"].sum())} for s, d in (("train", train), ("val", val), ("test", test))},
        "config": {k: cfg.raw[k] for k in ("window_seconds", "horizon_seconds", "tp", "sl", "position_sol", "neg_pos_ratio")},
        "preset": cfg.preset,
    }
    write_json(cfg.reports_dir / "m4_xgb.json", report)
    for name, r in results.items():
        append_history(
            cfg.reports_dir,
            {
                "model": name,
                "mode": cfg.decision_mode,
                "splits": {"train_end": cfg.split_train_end, "val_end": cfg.split_val_end},
                "test_n": r["n"],
                "test_pos": r["positives"],
                "base_rate": r["base_rate"],
                "pr_auc": r["pr_auc"],
                "roc_auc": r["roc_auc"],
                "p_at_10pct": r["precision_at"]["0.1"]["precision"],
                "pnl_at_10pct": r["pnl_at"]["0.1"]["pnl_sol"],
                "pnl_ex_top3": r["pnl_at"]["0.1"]["pnl_ex_top3_sol"],
                "weighted_pr_auc": (r.get("weighted") or {}).get("pr_auc"),
                "weighted_base_rate": (r.get("weighted") or {}).get("base_rate"),
                "serial_launcher": r.get("slice_serial_launcher", {}).get("pr_auc"),
                "train_n": train.height,
            },
        )
    md = ["# Milestone 4 — XGBoost baseline\n", metrics.comparison_table(cfg, results), ""]
    for name, imp in importances.items():
        md.append(f"\n## {name}: top gain features\n")
        md += [f"- {k}: {v}" for k, v in imp.items()]
    (cfg.reports_dir / "m4_xgb.md").write_text("\n".join(md) + "\n")
    log.info("-> %s", cfg.reports_dir / "m4_xgb.md")
    return report
