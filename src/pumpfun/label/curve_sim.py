"""curve_sim — integer-exact Pump.fun bonding-curve maths.

A faithful port of the three legs the program executes (verified against real
TradeEvents by the trading repo, and against tests/fixtures/curve-trades.json
here):

  buy(tokens_out)                 exact tokens out, quote in = t*vQ/(vT-t) + 1
  buy_exact_sol_in(quote_in)      quote to curve = (quote_in-1)*1e4/(1e4+bps), tokens = (q-1)*vT/(vQ+q-1),
                                  capped at the real token reserves (that cap IS graduation)
  sell(tokens_in)                 gross = t*vQ/(vT+t), fees come out of the proceeds

Fees are ceil(amount * bps / 1e4), each of protocol and creator separately.
All amounts are integers: lamports and raw token units. Floats only appear in
the convenience converters at the bottom.

Everything downstream (labels, PnL, features) depends on this file being right;
if it is wrong nothing will look obviously broken. Keep the tests green.
"""

from __future__ import annotations

from dataclasses import dataclass

BPS = 10_000
LAMPORTS_PER_SOL = 1_000_000_000


def ceil_div(a: int, b: int) -> int:
    if b == 0:
        raise ZeroDivisionError("ceil_div by zero")
    return -(-a // b)


def fee_of(amount: int, bps: int) -> int:
    return ceil_div(amount * bps, BPS)


@dataclass(frozen=True)
class CurveParams:
    """Initial state of a standard curve; derived/asserted by curve_params.py, never hardcoded in callers."""

    initial_virtual_sol: int
    initial_virtual_token: int
    initial_real_token: int
    token_decimals: int

    @property
    def raw_per_token(self) -> int:
        return 10**self.token_decimals


@dataclass(frozen=True)
class CurveFees:
    protocol_bps: int
    creator_bps: int

    @property
    def total_bps(self) -> int:
        return self.protocol_bps + self.creator_bps


@dataclass(frozen=True)
class CurveReserves:
    virtual_token: int
    virtual_sol: int
    real_token: int
    real_sol: int

    @property
    def complete(self) -> bool:
        return self.real_token <= 0

    def spot_lamports_per_raw(self) -> float:
        return self.virtual_sol / self.virtual_token

    def spot_sol_per_token(self, raw_per_token: int) -> float:
        """Marginal price in SOL per whole token (what the API reports as priceSol)."""
        return self.virtual_sol / self.virtual_token * raw_per_token / LAMPORTS_PER_SOL


def initial_reserves(p: CurveParams) -> CurveReserves:
    return CurveReserves(
        virtual_token=p.initial_virtual_token,
        virtual_sol=p.initial_virtual_sol,
        real_token=p.initial_real_token,
        real_sol=0,
    )


# ----------------------------------------------------------------------- buys


def buy_tokens_out(c: CurveReserves, quote_to_curve: int) -> int:
    """Tokens for `quote_to_curve` lamports AFTER fees were taken off; capped at the real reserves."""
    inp = quote_to_curve - 1
    if inp <= 0 or c.virtual_token <= 0:
        return 0
    out = (inp * c.virtual_token) // (c.virtual_sol + inp)
    return min(out, c.real_token)


def buy_quote_in(c: CurveReserves, tokens_out: int) -> int:
    """Quote the curve must receive for exactly `tokens_out` (the `buy` leg), before fees."""
    t = min(tokens_out, c.real_token)
    if t <= 0:
        return 0
    left = c.virtual_token - t
    if left <= 0:
        return 0
    return (t * c.virtual_sol) // left + 1


@dataclass(frozen=True)
class BuyResult:
    tokens_out: int
    quote_to_curve: int
    protocol_fee: int
    creator_fee: int
    total_paid: int
    completed: bool
    after: CurveReserves


def _after_buy(c: CurveReserves, tokens_out: int, quote_to_curve: int) -> CurveReserves:
    return CurveReserves(
        virtual_token=c.virtual_token - tokens_out,
        virtual_sol=c.virtual_sol + quote_to_curve,
        real_token=c.real_token - tokens_out,
        real_sol=c.real_sol + quote_to_curve,
    )


def buy_exact_sol_in(c: CurveReserves, quote_in: int, fees: CurveFees) -> BuyResult:
    """`buy_exact_sol_in(spendable)`: spend up to `quote_in` lamports including fees.

    When the tokens would exceed the real reserves the trade is capped at the
    remainder and repriced as an exact-tokens-out buy — the graduating trade.
    """
    zero = BuyResult(0, 0, 0, 0, 0, False, c)
    if quote_in <= 0 or c.virtual_token <= 0 or c.real_token <= 0:
        return zero
    quote_to_curve = ((quote_in - 1) * BPS) // (BPS + fees.total_bps)
    tokens_out = buy_tokens_out(c, quote_to_curve)
    completed = tokens_out >= c.real_token
    if completed:
        tokens_out = c.real_token
        quote_to_curve = buy_quote_in(c, tokens_out)
    if tokens_out <= 0:
        return zero
    pf = fee_of(quote_to_curve, fees.protocol_bps)
    cf = fee_of(quote_to_curve, fees.creator_bps)
    return BuyResult(
        tokens_out=tokens_out,
        quote_to_curve=quote_to_curve,
        protocol_fee=pf,
        creator_fee=cf,
        total_paid=quote_to_curve + pf + cf,
        completed=completed,
        after=_after_buy(c, tokens_out, quote_to_curve),
    )


def buy_exact_tokens_out(c: CurveReserves, tokens_out: int, fees: CurveFees) -> BuyResult:
    """`buy(amount)`: receive exactly `tokens_out` (capped at real reserves); pay quote + fees."""
    t = min(tokens_out, c.real_token)
    q = buy_quote_in(c, t)
    if t <= 0 or q <= 0:
        return BuyResult(0, 0, 0, 0, 0, False, c)
    pf = fee_of(q, fees.protocol_bps)
    cf = fee_of(q, fees.creator_bps)
    return BuyResult(t, q, pf, cf, q + pf + cf, t >= c.real_token, _after_buy(c, t, q))


# ---------------------------------------------------------------------- sells


def sell_quote_out(c: CurveReserves, tokens_in: int) -> int:
    """Gross lamports off the curve for `tokens_in` (fees applied by the caller)."""
    if tokens_in <= 0 or c.virtual_token + tokens_in <= 0:
        return 0
    return (tokens_in * c.virtual_sol) // (c.virtual_token + tokens_in)


@dataclass(frozen=True)
class SellResult:
    quote_out_gross: int
    protocol_fee: int
    creator_fee: int
    quote_out_net: int
    real_reserves_ok: bool
    after: CurveReserves


def sell_exact_tokens_in(c: CurveReserves, tokens_in: int, fees: CurveFees) -> SellResult:
    """`sell(amount)`: fees come out of the proceeds."""
    gross = sell_quote_out(c, tokens_in)
    pf = fee_of(gross, fees.protocol_bps)
    cf = fee_of(gross, fees.creator_bps)
    net = gross - pf - cf
    return SellResult(
        quote_out_gross=gross,
        protocol_fee=pf,
        creator_fee=cf,
        quote_out_net=max(net, 0),
        real_reserves_ok=c.real_sol >= gross,
        after=CurveReserves(
            virtual_token=c.virtual_token + tokens_in,
            virtual_sol=c.virtual_sol - gross,
            real_token=c.real_token + tokens_in,
            real_sol=c.real_sol - gross,
        ),
    )


# --------------------------------------------------------------------- replay


def apply_tape_trade(c: CurveReserves, is_buy: bool, sol_lamports: int, token_raw: int) -> CurveReserves:
    """Advance the reserves by a trade as the tape reports it.

    The API's `amountSol` is the curve-side quote (fee-exclusive), so it moves the
    reserves one-for-one. Real reserves are clamped at zero like the program does.
    """
    if is_buy:
        return CurveReserves(
            virtual_token=c.virtual_token - token_raw,
            virtual_sol=c.virtual_sol + sol_lamports,
            real_token=max(c.real_token - token_raw, 0),
            real_sol=c.real_sol + sol_lamports,
        )
    return CurveReserves(
        virtual_token=c.virtual_token + token_raw,
        virtual_sol=c.virtual_sol - sol_lamports,
        real_token=c.real_token + token_raw,
        real_sol=max(c.real_sol - sol_lamports, 0),
    )


# ----------------------------------------------------------------- converters


def sol_to_lamports(sol: float) -> int:
    return round(sol * LAMPORTS_PER_SOL)


def tokens_to_raw(tokens: float, raw_per_token: int) -> int:
    return round(tokens * raw_per_token)


def lamports_to_sol(lamports: int) -> float:
    return lamports / LAMPORTS_PER_SOL
