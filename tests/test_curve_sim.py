"""The curve simulator against 14 real mainnet trades (fixture from the trading repo).

Every leg is checked to the lamport / raw-token unit: fees, exact-tokens buys,
exact-SOL buys (including the graduating cap), and a sell.
"""

import json
from pathlib import Path

import pytest

from pumpfun.label import curve_sim as cs

FIX = json.loads((Path(__file__).parent / "fixtures" / "curve-trades.json").read_text())
FEES = cs.CurveFees(protocol_bps=95, creator_bps=30)
PARAMS = cs.CurveParams(
    initial_virtual_sol=30_000_000_000,
    initial_virtual_token=1_073_000_000_000_000,
    initial_real_token=793_100_000_000_000,
    token_decimals=6,
)


def _after(t: dict) -> cs.CurveReserves:
    return cs.CurveReserves(
        virtual_token=int(t["virtualTokenReserves"]),
        virtual_sol=int(t["virtualSolReserves"]),
        real_token=int(t["realTokenReserves"]),
        real_sol=int(t["realSolReserves"]),
    )


def _before(t: dict) -> cs.CurveReserves:
    a = _after(t)
    sol, tok = int(t["solAmount"]), int(t["tokenAmount"])
    if t["isBuy"]:
        return cs.CurveReserves(a.virtual_token + tok, a.virtual_sol - sol, a.real_token + tok, a.real_sol - sol)
    return cs.CurveReserves(a.virtual_token - tok, a.virtual_sol + sol, a.real_token - tok, a.real_sol + sol)


@pytest.mark.parametrize("t", FIX, ids=[f"{x['ix']}-{i}" for i, x in enumerate(FIX)])
def test_fees_are_ceil_of_bps(t):
    sol = int(t["solAmount"])
    assert cs.fee_of(sol, FEES.protocol_bps) == int(t["fee"])
    assert cs.fee_of(sol, FEES.creator_bps) == int(t["creatorFee"])


@pytest.mark.parametrize("t", [x for x in FIX if x["ix"] == "Buy"], ids=lambda x: x["signature"][:8])
def test_buy_exact_tokens_out(t):
    pre = _before(t)
    r = cs.buy_exact_tokens_out(pre, int(t["tokenAmount"]), FEES)
    assert r.quote_to_curve == int(t["solAmount"])
    assert r.tokens_out == int(t["tokenAmount"])
    assert r.protocol_fee == int(t["fee"]) and r.creator_fee == int(t["creatorFee"])
    assert r.after == _after(t)
    assert r.completed == (int(t["realTokenReserves"]) == 0)


@pytest.mark.parametrize(
    "t", [x for x in FIX if x["ix"] in ("BuyExactSolIn", "BuyExactQuoteInV2")], ids=lambda x: x["signature"][:8]
)
def test_buy_exact_sol_in(t):
    pre = _before(t)
    total = int(t["solAmount"]) + int(t["fee"]) + int(t["creatorFee"])
    # The user offered at least `total`; the program derives the curve leg from the offer and the bps.
    # Search the offer that reproduces this trade: it must exist within a few lamports of `total`.
    hits = [q for q in range(total - 3, total + 4) if cs.buy_exact_sol_in(pre, q, FEES).quote_to_curve == int(t["solAmount"])]
    assert hits, "no offer reproduces the curve leg"
    r = cs.buy_exact_sol_in(pre, hits[0], FEES)
    assert r.tokens_out == int(t["tokenAmount"])
    assert r.after == _after(t)
    assert r.total_paid == total


@pytest.mark.parametrize("t", [x for x in FIX if not x["isBuy"]], ids=lambda x: x["signature"][:8])
def test_sell(t):
    pre = _before(t)
    r = cs.sell_exact_tokens_in(pre, int(t["tokenAmount"]), FEES)
    assert r.quote_out_gross == int(t["solAmount"])
    assert r.protocol_fee == int(t["fee"]) and r.creator_fee == int(t["creatorFee"])
    assert r.quote_out_net == int(t["solAmount"]) - int(t["fee"]) - int(t["creatorFee"])
    assert r.after == _after(t)


def test_graduating_buy_from_fresh_curve_matches_fixture():
    grad = next(x for x in FIX if int(x["realTokenReserves"]) == 0 and int(x["tokenAmount"]) == PARAMS.initial_real_token)
    c0 = cs.initial_reserves(PARAMS)
    # Offer far more than needed: the cap must reprice to the exact graduating quote.
    r = cs.buy_exact_sol_in(c0, 200 * cs.LAMPORTS_PER_SOL, FEES)
    assert r.completed
    assert r.tokens_out == PARAMS.initial_real_token
    assert r.quote_to_curve == int(grad["solAmount"])
    assert r.after.complete and r.after == _after(grad)


def test_round_trip_costs_only_fees_and_slippage():
    c0 = cs.initial_reserves(PARAMS)
    spend = cs.sol_to_lamports(0.5)
    b = cs.buy_exact_sol_in(c0, spend, FEES)
    s = cs.sell_exact_tokens_in(b.after, b.tokens_out, FEES)
    assert s.quote_out_net < b.total_paid
    # 125 bps each way plus tiny slippage on a fresh curve: well under 3 %.
    assert s.quote_out_net > b.total_paid * 0.97
    # Integer rounding leaves at most a lamport of dust in the curve; tokens come back exactly.
    assert 0 <= s.after.real_sol <= 1 and s.after.real_token == PARAMS.initial_real_token


def test_spot_price_matches_reserve_ratio():
    c0 = cs.initial_reserves(PARAMS)
    # 30 SOL / 1.073e9 tokens ≈ 2.796e-8 SOL per token — the well-known launch price.
    assert c0.spot_sol_per_token(PARAMS.raw_per_token) == pytest.approx(2.7959e-8, rel=1e-4)


def test_tape_replay_reproduces_fixture_after_states():
    for t in FIX:
        pre = _before(t)
        assert cs.apply_tape_trade(pre, t["isBuy"], int(t["solAmount"]), int(t["tokenAmount"])) == _after(t)
