from pumpfun.label import pool_sim as ps

FEES = ps.PoolFees(lp_bps=20, protocol_bps=5, creator_bps=5)
MIG = ps.migration_reserves(206_900_000_000_000, 84_990_360_349, 17_584_505_556)


def test_migration_spot_is_continuous_with_graduated_curve():
    # A graduated curve quotes 115.005 SOL virtual / 279.9e12 raw; the pool's effective quote / base must be close.
    curve_spot = 115_005_359_057 / 279_900_000_000_000
    assert abs(MIG.effective_quote / MIG.base / curve_spot - 1) < 0.25


def test_buy_then_sell_loses_fees_and_slippage_only():
    b = ps.buy_quote_input(500_000_000, MIG, FEES)
    assert b.total_paid == 500_000_000
    assert b.quote_to_curve + b.lp_fee + b.protocol_fee + b.creator_fee <= 500_000_000
    s = ps.sell_base_input(b.base_out, b.after, FEES)
    assert s.real_reserves_ok
    assert s.quote_out_net < 500_000_000
    assert s.quote_out_net > 500_000_000 * 0.99


def test_sell_caps_on_real_reserves():
    thin = ps.PoolReserves(base=MIG.base, quote=1_000_000, virtual_quote=MIG.virtual_quote)
    s = ps.sell_base_input(MIG.base // 2, thin, FEES)
    assert not s.real_reserves_ok
