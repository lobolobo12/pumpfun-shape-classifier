"""xgb — milestone 4: gradient-boosted trees on the tabular features, three feature groups, taken seriously.

Variants: shape only (the spec's chart hypothesis in isolation), holders only, shape + holders (+ creator).
Also the trading repo's logistic recipe (analyse.ts MODEL_FEATURES, translated) for continuity.
Early stopping on the validation split; the test split is touched once per variant.
"""

from __future__ import annotations

import logging

import numpy as np
import polars as pl
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from pumpfun.config import Config
from pumpfun.features.tabular import CONTEXT, CREATOR, HOLDERS, SHAPE
from pumpfun.models import metrics
from pumpfun.reports import append_history, write_json

log = logging.getLogger(__name__)

VARIANTS = {
    "xgb_shape": SHAPE,
    "xgb_holders": HOLDERS,
    "xgb_shape+holders": SHAPE + HOLDERS,
    "xgb_all": SHAPE + HOLDERS + CREATOR + CONTEXT,
    "xgb_context": CONTEXT,
}
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
    model.fit(xt, yt, eval_set=[(xv, yv)], verbose=False)
    return model


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
    for name, cols in VARIANTS.items():
        model = fit_xgb(cfg, train, val, cols)
        p = model.predict_proba(_xy(test, cols)[0])[:, 1]
        results[name] = metrics.evaluate(cfg, test, p)
        results[name]["best_iteration"] = int(model.best_iteration)
        results[name]["val_pr_auc"] = metrics.evaluate(cfg, val, model.predict_proba(_xy(val, cols)[0])[:, 1])["pr_auc"]
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
