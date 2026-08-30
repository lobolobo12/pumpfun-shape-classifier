"""Synthetic tapes with known outcomes for the triple-barrier labeller."""

import pytest

from pumpfun.config import load_config
from pumpfun.label import curve_sim as cs
from pumpfun.label.barriers import Drop, TapeTrade, label_tape

CFG = load_config(overrides=["min_trades_in_window=3"])
P = cs.CurveParams(
    CFG.curve_expected.initial_virtual_sol_lamports,
    CFG.curve_expected.initial_virtual_token_raw,
    CFG.curve_expected.initial_real_token_raw,
    CFG.curve_expected.token_decimals,
)
FEES = cs.CurveFees(CFG.fee_protocol_bps, CFG.fee_creator_bps)


def _tape(buys_sol: list[tuple[float, float]], sells: list[tuple[float, float]] = ()) -> list[TapeTrade]:
    """Build a consistent tape by simulating real buys/sells on a fresh curve. Items are (t_s, sol)."""
    events = sorted([(t, s, True) for t, s in buys_sol] + [(t, s, False) for t, s in sells])
    c = cs.initial_reserves(P)
    out: list[TapeTrade] = []
    held = 0
    for i, (t, sol, is_buy) in enumerate(events):
        if is_buy:
            r = cs.buy_exact_sol_in(c, cs.sol_to_lamports(sol), FEES)
            c = r.after
            held += r.tokens_out
            out.append(
                TapeTrade(
                    i,
                    t,
                    True,
                    r.quote_to_curve / 1e9,
                    r.tokens_out / P.raw_per_token,
                    "pump",
                    c.spot_sol_per_token(P.raw_per_token),
                )
            )
        else:
            tok = min(held, int(sol))  # for sells, `sol` carries raw tokens to sell
            r = cs.sell_exact_tokens_in(c, tok, FEES)
            c = r.after
            held -= tok
            out.append(
                TapeTrade(
                    i, t, False, r.quote_out_gross / 1e9, tok / P.raw_per_token, "pump", c.spot_sol_per_token(P.raw_per_token)
                )
            )
    return out


def test_pump_after_entry_hits_tp():
    # 5 small buys in the window, entry at 300 s, then 20 SOL of buying -> price far above 2x.
    tape = _tape(
        [(10, 0.5), (20, 0.5), (30, 0.5), (40, 0.5), (50, 0.5), (300, 0.1)] + [(300 + 30 * k, 2.0) for k in range(1, 11)]
    )
    row = label_tape(CFG, "m", tape)
    assert row.label == 1 and row.exit_reason == "tp"
    assert row.ratio_at_exit >= 1 + CFG.tp
    assert row.entry_t == 300 and row.n_trades_window == 5


def test_dump_after_entry_hits_sl():
    # ~340M tokens were bought for 12 SOL; dumping 250M of them walks the curve well below the -40 % stop.
    tape = _tape([(10, 3.0), (20, 3.0), (30, 3.0), (40, 3.0), (300, 0.1)], sells=[(400, 250_000_000 * 10**6)])
    row = label_tape(CFG, "m", tape)
    assert row.label == 0 and row.exit_reason == "sl"
    assert row.ratio_at_exit <= 1 - CFG.sl


def test_flat_tape_is_vertical_and_costs_fees():
    tape = _tape([(10, 1.0), (20, 1.0), (30, 1.0), (300, 0.05), (900, 0.05), (2000, 0.05)])
    row = label_tape(CFG, "m", tape)
    assert row.label == 0 and row.exit_reason == "vertical"
    # Round trip on a quiet curve loses fees + slippage only: well inside the stop.
    assert 0.9 < row.ratio_at_exit < 1.0


def test_filters():
    with pytest.raises(Drop, match="lifetime_lt_window"):
        label_tape(CFG, "m", _tape([(10, 1.0), (20, 1.0), (30, 1.0)]))
    with pytest.raises(Drop, match="lt_min_trades"):
        label_tape(CFG, "m", _tape([(10, 1.0), (300, 1.0), (400, 1.0)]))
    # Alive but quiet at t = 300: the curve still fills; the later trade is the first exit state.
    row = label_tape(CFG, "m", _tape([(10, 1.0), (20, 1.0), (30, 1.0), (400, 1.0)]))
    assert row.entry_t == 300 and row.exit_reason == "vertical" and row.n_trades_horizon == 1


def test_entry_price_is_pre_entry_marginal_and_fill_is_worse():
    tape = _tape([(10, 1.0), (20, 1.0), (30, 1.0), (300, 0.1), (600, 0.1)])
    row = label_tape(CFG, "m", tape)
    assert row.entry_fill_price > row.entry_price
    assert row.curve_sol_at_entry == pytest.approx(3.0 * 10_000 / (10_000 + FEES.total_bps), rel=1e-3)
    assert 0 < row.entry_cost_sol - CFG.position_sol < 0.01
