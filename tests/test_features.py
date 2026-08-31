"""Feature layer: causality of the window, encoder shape, holder/creator features by construction."""

import numpy as np
import polars as pl
import pytest

from pumpfun.config import load_config
from pumpfun.features import sequence, tabular

CFG = load_config()


def _trades(mint: str, rows: list[tuple[float, bool, float, float, str, float]]) -> pl.DataFrame:
    """rows: (t_s, is_buy, sol, tokens, trader, price_sol)."""
    return pl.DataFrame(
        {
            "mint": [mint] * len(rows),
            "signature": [f"{mint}-{i}" for i in range(len(rows))],
            "slot": [1000 + int(r[0]) for r in rows],
            "slot_index": list(range(len(rows))),
            "block_time": [int(r[0]) for r in rows],
            "seconds_since_launch": [r[0] for r in rows],
            "is_buy": [r[1] for r in rows],
            "sol_amount": [r[2] for r in rows],
            "token_amount": [r[3] for r in rows],
            "trader": [r[4] for r in rows],
            "program": ["pump"] * len(rows),
            "curve_sol_after": [float(i + 1) for i in range(len(rows))],
            "curve_token_after": [1.0] * len(rows),
            "price_sol": [r[5] for r in rows],
            "fill_price_sol": [None] * len(rows),
        }
    )


def _labels(mint: str, entry_t: float = 300.0, label: int = 1) -> pl.DataFrame:
    return pl.DataFrame(
        {
            "mint": [mint],
            "entry_t": [entry_t],
            "n_visible": [10**6],
            "entry_price": [2e-8],
            "curve_sol_at_entry": [5.0],
            "in_zone": [True],
            "launch_day": ["2026-08-29"],
            "label": [label],
        }
    )


def test_window_trades_slices_by_rank_and_asserts_causality():
    tr = _trades("A", [(1, True, 1.0, 1e7, "w1", 1e-8), (299, True, 1.0, 1e7, "w2", 2e-8), (300, True, 1.0, 1e7, "w3", 3e-8)])
    lab = _labels("A").with_columns(n_visible=pl.lit(2))
    wt = sequence.window_trades(CFG, tr.lazy(), lab)
    assert wt.height == 2
    with pytest.raises(AssertionError):
        sequence.window_trades(CFG, tr.lazy(), lab.with_columns(entry_t=pl.lit(250.0), n_visible=pl.lit(3)))


def test_encoder_shape_and_forward_fill():
    tr = _trades("A", [(10, True, 1.0, 1e7, "w1", 1e-8), (200, False, 0.5, 5e6, "w1", 4e-8)])
    lab = _labels("A")
    x, mints = sequence.encode(CFG, sequence.window_trades(CFG, tr.lazy(), lab), lab)
    assert x.shape == (1, CFG.resample_steps, 6) and mints == ["A"]
    assert x[0, 0, 0] == pytest.approx(np.log(sequence.launch_price(CFG) / 2e-8))  # pre-trade: launch price
    assert x[0, 10, 0] == pytest.approx(np.log(1e-8 / 2e-8))
    assert x[0, 150, 0] == x[0, 10, 0]  # forward-filled
    assert x[0, 200, 0] == pytest.approx(np.log(4e-8 / 2e-8))
    assert x[0, :, 1].sum() == pytest.approx(1.0)  # volume shares sum to 1
    assert x[0, 10, 4] == 1.0 and x[0, 200, 4] == -1.0


def test_holder_features_by_construction():
    rows = [
        (0.0, 1000, True, 1.0, 100.0, "dev", 1e-8),
        (0.0, 1000, True, 1.0, 100.0, "b1", 1e-8),
        (5.0, 1010, True, 1.0, 100.0, "b2", 1e-8),
        (6.0, 1012, False, 0.5, 60.0, "dev", 1e-8),
    ]
    f = tabular.shape_and_holders(CFG, rows, creator="dev", curve_sol_at_entry=2.5, entry_price=1e-8, window_s=300.0)
    assert f["holders_n"] == 3 and f["buyers_n"] == 3
    assert f["dev_share"] == pytest.approx(40 / 240)
    assert f["dev_sold"] == 1.0
    assert f["first_slot_share"] == pytest.approx(140 / 240)
    assert f["launch_bundle_share"] == pytest.approx(140 / 240)
    assert f["top1_share"] == pytest.approx(100 / 240)
    assert f["same_size_share"] == pytest.approx(1.0)  # all three first buys are exactly 1.000 SOL
    assert f["bundle_slots"] == 1 and f["n_trades"] == 4


def test_creator_history_uses_only_prior_resolved_outcomes():
    tokens = pl.DataFrame(
        {
            "mint": ["t1", "t2", "t3"],
            "creator": ["c", "c", "c"],
            "launch_time": [1_000_000, 1_000_000 + 10_000, 1_000_000 + 20_000],
        }
    )
    # t1 resolved (entry 300 + horizon 3600 = 3900 s) before t2 launches (10_000 s later): counts for t2 and t3.
    # t2 resolves 3900 s after its launch -> after t3's launch? t3 launches 10_000 s after t2, so t2 counts for t3.
    labels = pl.DataFrame({"mint": ["t1", "t2", "t3"], "label": [1, 0, 1], "entry_t": [300.0, 300.0, 300.0]})
    h = tabular.creator_history(CFG, tokens, labels).sort("mint")
    assert h["creator_prior_launches"].to_list() == [0, 1, 2]
    assert h["creator_prior_resolved"].to_list() == [0, 1, 2]
    assert h["creator_prior_tp_rate"].to_list()[0] is None
    assert h["creator_prior_tp_rate"].to_list()[1] == 1.0
    assert h["creator_prior_tp_rate"].to_list()[2] == 0.5
    # A token launched 1 s after t1 must NOT see t1's outcome (unresolved at launch).
    tokens2 = tokens.with_columns(launch_time=pl.Series([1_000_000, 1_000_001, 1_000_002]))
    h2 = tabular.creator_history(CFG, tokens2, labels).sort("mint")
    assert h2["creator_prior_launches"].to_list() == [0, 1, 2]
    assert h2["creator_prior_resolved"].to_list() == [0, 0, 0]


def test_prescreen_threshold_is_derived_from_tp():
    from pumpfun.ingest.prescreen import needed_sol

    assert needed_sol(CFG) == pytest.approx((2**0.5 - 1) * 30, rel=1e-6)
    assert needed_sol(load_config(overrides=["tp=3.0"])) == pytest.approx(30.0, rel=1e-6)


def test_trade_encoding_right_aligned_with_dt():
    tr = _trades(
        "A",
        [(10, True, 1.0, 1e7, "w1", 1e-8), (40, True, 2.0, 1e7, "w2", 3e-8), (41, False, 0.5, 5e6, "w1", 2.5e-8)],
    )
    lab = _labels("A")
    x, mints = sequence.encode_trades(CFG, sequence.window_trades(CFG, tr.lazy(), lab), lab, steps=8)
    assert x.shape == (1, 8, 6)
    assert (x[0, :5] == 0).all()  # left padding
    assert x[0, 5, 2] == 1.0 and x[0, 7, 2] == -1.0  # sides
    assert x[0, 6, 1] == pytest.approx(np.log1p(30.0))  # dt 10 -> 40
    assert x[0, 7, 1] == pytest.approx(np.log1p(1.0))
    assert x[0, 5, 4] == 1.0 and x[0, 7, 4] == 0.0  # w1 new at first trade, not at its second
    assert x[0, 7, 0] == pytest.approx(np.log(2.5e-8 / 2e-8))
