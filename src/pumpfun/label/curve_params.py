"""curve_params — derive the curve constants from the tapes; never trust a blog post.

For every coin the API's spot after each curve trade must satisfy
    price_k * (vT0 - sum_tokens_k) = vQ0 + sum_sol_k
which is linear in the unknown initial virtual reserves (vT0, vQ0). A least-squares
fit over a coin's first trades gives that coin's constants; the per-month median
is the month's constant. The graduation threshold is the real SOL in the curve
at the completing trade. Both are compared with `curve_expected` in config and
asserted stable month to month; per-coin residuals above `curve_param_tolerance`
mark the coin non-standard (mayhem mode, custom curves) and it is dropped downstream.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
import polars as pl

from pumpfun.config import Config
from pumpfun.ingest.to_parquet import CURVE_PROGRAM, read_trades
from pumpfun.reports import write_json

log = logging.getLogger(__name__)

FIT_TRADES = 40
SAMPLE_PER_MONTH = 400


@dataclass(frozen=True)
class CoinFit:
    mint: str
    month: str
    v_token0: float
    v_sol0: float
    residual: float  # median |spot_model / spot_api - 1| over the fitted trades
    n: int


def fit_coin(
    sol: np.ndarray, tokens: np.ndarray, is_buy: np.ndarray, price: np.ndarray, raw_per_token: int
) -> tuple[float, float, float]:
    """Least squares for (vT0, vQ0) in raw tokens / lamports from cumulative flows and the API spot."""
    sign = np.where(is_buy, 1.0, -1.0)
    cum_sol = np.cumsum(sign * sol) * 1e9
    cum_tok = np.cumsum(sign * tokens) * raw_per_token
    p = price * 1e9 / raw_per_token  # lamports per raw token
    # p*vT0 - vQ0 = p*cum_tok + cum_sol
    a = np.stack([p, -np.ones_like(p)], axis=1)
    b = p * cum_tok + cum_sol
    (vt0, vq0), *_ = np.linalg.lstsq(a, b, rcond=None)
    model = (vq0 + cum_sol) / (vt0 - cum_tok)
    resid = float(np.median(np.abs(model / p - 1)))
    return float(vt0), float(vq0), resid


def fit_all(cfg: Config, sample_per_month: int = SAMPLE_PER_MONTH) -> list[CoinFit]:
    raw_per = 10**cfg.curve_expected.token_decimals
    lf = read_trades(cfg).filter(pl.col("program") == CURVE_PROGRAM)
    first = (
        lf.sort("mint", "slot", "slot_index")
        .with_columns(k=pl.int_range(pl.len()).over("mint"))
        .filter(pl.col("k") < FIT_TRADES)
        .select("mint", "block_time", "sol_amount", "token_amount", "is_buy", "price_sol")
        .collect()
    )
    first = first.with_columns(month=pl.from_epoch("block_time").dt.strftime("%Y-%m"))
    out: list[CoinFit] = []
    rng = np.random.default_rng(cfg.seed)
    for (month,), g in first.group_by("month", maintain_order=True):
        mints = g["mint"].unique().to_list()
        if len(mints) > sample_per_month:
            mints = list(rng.choice(mints, sample_per_month, replace=False))
        for (mint,), t in g.filter(pl.col("mint").is_in(mints)).group_by("mint", maintain_order=True):
            if t.height < 3:
                continue
            vt0, vq0, r = fit_coin(
                t["sol_amount"].to_numpy(),
                t["token_amount"].to_numpy(),
                t["is_buy"].to_numpy(),
                t["price_sol"].to_numpy(),
                raw_per,
            )
            out.append(CoinFit(mint, str(month), vt0, vq0, r, t.height))
    return out


def graduation_sol(cfg: Config) -> pl.DataFrame:
    lf = read_trades(cfg).filter((pl.col("program") == CURVE_PROGRAM) & (pl.col("curve_token_after") <= 0))
    return (
        lf.sort("mint", "slot", "slot_index")
        .group_by("mint", maintain_order=True)
        .agg(pl.col("curve_sol_after").first().alias("graduation_sol"), pl.col("block_time").first())
        .with_columns(month=pl.from_epoch("block_time").dt.strftime("%Y-%m"))
        .group_by("month")
        .agg(
            pl.col("graduation_sol").median().alias("median"),
            pl.col("graduation_sol").min().alias("min"),
            pl.col("graduation_sol").max().alias("max"),
            pl.len().alias("n"),
        )
        .sort("month")
        .collect()
    )


def run(cfg: Config) -> dict:
    e = cfg.curve_expected
    fits = fit_all(cfg)
    if not fits:
        raise SystemExit("no curve trades on disk yet — run fetch / to-parquet first")
    tol = cfg.curve_param_tolerance
    months: dict[str, dict] = {}
    for m in sorted({f.month for f in fits}):
        fs = [f for f in fits if f.month == m]
        std = [f for f in fs if f.residual <= tol]
        vt = float(np.median([f.v_token0 for f in std])) if std else float("nan")
        vq = float(np.median([f.v_sol0 for f in std])) if std else float("nan")
        months[m] = {
            "coins_fitted": len(fs),
            "coins_standard": len(std),
            "share_non_standard": round(1 - len(std) / len(fs), 4),
            "virtual_token0_raw": vt,
            "virtual_sol0_lamports": vq,
            "rel_diff_vs_expected": {
                "virtual_token": abs(vt / e.initial_virtual_token_raw - 1),
                "virtual_sol": abs(vq / e.initial_virtual_sol_lamports - 1),
            },
        }
    grad = graduation_sol(cfg)
    report = {
        "months": months,
        "graduation_sol_by_month": grad.to_dicts(),
        "expected": {
            "virtual_token0_raw": e.initial_virtual_token_raw,
            "virtual_sol0_lamports": e.initial_virtual_sol_lamports,
        },
        "tolerance": tol,
    }
    write_json(cfg.reports_dir / "curve_params.json", report)
    for m, r in months.items():
        log.info(
            "%s: vT0=%.4g vQ0=%.4g (diff %.2e / %.2e), non-standard %.1f%% of %d",
            m,
            r["virtual_token0_raw"],
            r["virtual_sol0_lamports"],
            r["rel_diff_vs_expected"]["virtual_token"],
            r["rel_diff_vs_expected"]["virtual_sol"],
            100 * r["share_non_standard"],
            r["coins_fitted"],
        )
    bad = [m for m, r in months.items() if max(r["rel_diff_vs_expected"].values()) > tol]
    if bad:
        raise SystemExit(
            f"curve constants differ from config in {bad}; update curve_expected only after reading reports/curve_params.json"
        )
    return report
