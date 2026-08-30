# pumpfun-shape-classifier

Does the first 300 s of a Pump.fun token's tape predict whether a 0.5 SOL buy at t = 300 s hits
+100 % before −40 % within an hour? The spec and the trading-repo handoff live locally next to this README and are not part of the repository.

## Setup

```bash
make sync                      # uv, Python 3.12, all extras
make check                     # ruff + pytest (curve maths vs 14 mainnet trades, barriers, features)
```

All knobs live in `config.yaml`; `--preset <name>` overlays `presets/<name>.yaml` (local); `--set tp=1.5` overrides one key.

## Pipeline

```bash
pf universe                    # attention.db sweep ∪ on-chain create frames -> data/raw/tokens.parquet (+ coverage report)
pf prescreen                   # drop coins with zero curve inflow -> fetch queue (also committed to data/queue/ for the runners)
# fetch tapes — on GitHub Actions (own IPs), never on the Mac while the live collector runs:
gh workflow run fetch.yml -f shards=4 -f rps=2.0 -f max_minutes=330
pf gh-pull                     # merge the runs' artifacts into data/raw/cache + the ledger
pf to-parquet                  # cache -> data/raw/trades/{yyyy-mm}/*.parquet
pf curve-params                # derive curve constants, assert stable, flag non-standard coins
pf label                       # triple-barrier labels on realized exits -> data/interim/labels.parquet
pf bench render && pf bench label   # milestone 0: 200 stripped charts, g/b in the terminal
pf features && pf check leakage     # tabular + 6-channel sequences, day/creator splits, leakage assertions
pf xgb                         # milestone 4 -> reports/m4_xgb.md
pf cnn                         # milestone 5 -> reports/m5_*.md
```

Every stage writes its drop counts to `reports/filter_counts.json`.

## Why it is built this way

- Universe from create events only (sweep + on-chain frames), never from a chart site — survivorship bias.
- Labels use the realized proceeds of selling the whole position on the curve (or PumpSwap after graduation),
  with the verified 125 bps/side curve fee, not the quoted price.
- Time-based, creator-grouped splits; creator features use only outcomes resolved before the launch.
- The fetcher is sharded and resumable; the Mac's IP is shared with a live collector and stays untouched.
