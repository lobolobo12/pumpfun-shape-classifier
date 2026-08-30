"""pool_sim — PumpSwap constant-product maths, for the leg after graduation.

Exact integer port of @pump-fun/pump-swap-sdk (buy.ts / sell.ts / fees.ts) as
verified by the trading repo (src/domain/pumpswap/quote.ts). Price basis is
always the EFFECTIVE quote = real quote vault + the pool's virtual quote
reserves; the LP fee stays in the pool. Sells are capped by real reserves.

Fee tiers by market cap exist for canonical pools; v1 uses the GlobalConfig
flat fees from config and validates against fillPriceSol on pump_amm trades.
"""

from __future__ import annotations

from dataclasses import dataclass

from pumpfun.label.curve_sim import BPS, ceil_div, fee_of


@dataclass(frozen=True)
class PoolFees:
    lp_bps: int
    protocol_bps: int
    creator_bps: int

    @property
    def total_bps(self) -> int:
        return self.lp_bps + self.protocol_bps + self.creator_bps


@dataclass(frozen=True)
class PoolReserves:
    base: int  # raw tokens in the pool
    quote: int  # real quote vault, lamports
    virtual_quote: int  # Pool.virtual_quote_reserves, lamports

    @property
    def effective_quote(self) -> int:
        return self.quote + self.virtual_quote

    def spot_sol_per_token(self, raw_per_token: int) -> float:
        return self.effective_quote / self.base * raw_per_token / 1_000_000_000


def migration_reserves(base_tokens_raw: int, quote_lamports: int, virtual_quote_lamports: int) -> PoolReserves:
    """The deterministic pool state a standard migration leaves behind, before its first trade."""
    return PoolReserves(base=base_tokens_raw, quote=quote_lamports, virtual_quote=virtual_quote_lamports)


@dataclass(frozen=True)
class PoolBuyResult:
    base_out: int
    quote_to_curve: int
    lp_fee: int
    protocol_fee: int
    creator_fee: int
    total_paid: int
    after: PoolReserves


def buy_quote_input(quote: int, r: PoolReserves, fees: PoolFees) -> PoolBuyResult:
    """`buy_exact_quote_in(spendable_quote_in)` — spend exactly `quote`, receive `base_out`."""
    if r.base <= 0 or r.quote <= 0:
        raise ValueError("empty pool reserves")
    eff = r.effective_quote
    quote_to_curve = (quote * BPS) // (BPS + fees.total_bps)
    lp = fee_of(quote_to_curve, fees.lp_bps)
    pf = fee_of(quote_to_curve, fees.protocol_bps)
    cf = fee_of(quote_to_curve, fees.creator_bps)
    total = quote_to_curve + lp + pf + cf
    if total > quote:
        quote_to_curve -= total - quote
    inp = quote_to_curve - 1
    denom = eff + inp
    if denom <= 0:
        raise ValueError("pool depleted")
    base_out = (r.base * inp) // denom
    return PoolBuyResult(
        base_out=base_out,
        quote_to_curve=quote_to_curve,
        lp_fee=lp,
        protocol_fee=pf,
        creator_fee=cf,
        total_paid=quote,
        after=PoolReserves(base=r.base - base_out, quote=r.quote + quote_to_curve + lp, virtual_quote=r.virtual_quote),
    )


@dataclass(frozen=True)
class PoolSellResult:
    quote_out_gross: int
    lp_fee: int
    protocol_fee: int
    creator_fee: int
    quote_out_net: int
    real_reserves_ok: bool
    after: PoolReserves


def sell_base_input(base: int, r: PoolReserves, fees: PoolFees) -> PoolSellResult:
    """`sell(base_amount_in, min_quote_amount_out)`."""
    if r.base <= 0 or r.quote <= 0:
        raise ValueError("empty pool reserves")
    eff = r.effective_quote
    gross = (eff * base) // (r.base + base)
    lp = fee_of(gross, fees.lp_bps)
    pf = fee_of(gross, fees.protocol_bps)
    cf = fee_of(gross, fees.creator_bps)
    net = gross - lp - pf - cf
    return PoolSellResult(
        quote_out_gross=gross,
        lp_fee=lp,
        protocol_fee=pf,
        creator_fee=cf,
        quote_out_net=max(net, 0),
        real_reserves_ok=r.quote >= gross - lp,
        after=PoolReserves(base=r.base + base, quote=r.quote - (gross - lp), virtual_quote=r.virtual_quote),
    )


def apply_tape_trade(r: PoolReserves, is_buy: bool, sol_lamports: int, token_raw: int) -> PoolReserves:
    """Advance the pool by a tape trade (amountSol taken as the quote leg, like the trading repo's replay)."""
    if is_buy:
        return PoolReserves(base=max(r.base - token_raw, 1), quote=r.quote + sol_lamports, virtual_quote=r.virtual_quote)
    return PoolReserves(base=r.base + token_raw, quote=max(r.quote - sol_lamports, 0), virtual_quote=r.virtual_quote)


def buy_base_input_quote(base: int, r: PoolReserves) -> int:
    """Quote to curve for exactly `base` tokens out (before fees) — used by validation only."""
    if base >= r.base:
        raise ValueError("more base than pool reserves")
    return ceil_div(r.effective_quote * base, r.base - base)
