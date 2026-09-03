# Model ledger — held-out days averaged

Latest evaluation per (mode, model, test day); lift = PR-AUC / base rate.


## age mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape+holders | 1 | 62 | 0.346 | 3.67× | 3.67× | 0.35 | +3.67 | +1.91 |
| xgb_all | 1 | 62 | 0.341 | 3.61× | 3.61× | 0.33 | +3.14 | +1.37 |
| xgb_holders | 1 | 62 | 0.327 | 3.47× | 3.47× | 0.30 | +2.12 | -0.23 |
| xgb_all+wallets | 1 | 62 | 0.324 | 3.43× | 3.43× | 0.32 | +2.06 | +0.29 |
| cnn_trades+side+pre | 1 | 62 | 0.311 | 3.30× | 3.30× | 0.32 | +2.88 | +0.58 |
| ensemble:xgb_holders+cnn_trades+side | 1 | 62 | 0.289 | 3.07× | 3.07× | 0.32 | +3.00 | +0.65 |
| xgb_shape | 1 | 62 | 0.284 | 3.01× | 3.01× | 0.32 | +2.31 | +0.61 |
| xgb_holders+wallets | 1 | 62 | 0.283 | 3.00× | 3.00× | 0.23 | -1.20 | -3.61 |
| cnn_trades | 2 | 139 | 0.286 | 2.92× | 2.63× | 0.28 | +1.68 | -2.32 |
| cnn_trades+side | 1 | 62 | 0.275 | 2.92× | 2.92× | 0.27 | +0.81 | -1.52 |
| logistic_repo_recipe | 1 | 62 | 0.264 | 2.80× | 2.80× | 0.26 | -0.46 | -2.38 |
| xgb_wallets | 1 | 62 | 0.174 | 1.84× | 1.84× | 0.20 | -1.06 | -2.70 |
| xgb_context | 1 | 62 | 0.101 | 1.07× | 1.07× | 0.06 | -4.07 | -5.62 |

Test days: 2026-08-31, 2026-09-02


## cross mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_all+wallets | 1 | 58 | 0.358 | 1.84× | 1.84× | 0.37 | +13.42 | +1.12 |
| xgb_shape+holders | 1 | 58 | 0.329 | 1.69× | 1.69× | 0.40 | +13.52 | +1.22 |
| xgb_all | 1 | 58 | 0.323 | 1.66× | 1.66× | 0.37 | +13.10 | +0.80 |
| xgb_shape | 1 | 58 | 0.317 | 1.63× | 1.63× | 0.43 | +13.90 | +1.81 |
| ensemble:xgb_holders+cnn_trades+side | 1 | 58 | 0.305 | 1.57× | 1.57× | 0.40 | +13.61 | +1.52 |
| xgb_holders+wallets | 1 | 58 | 0.297 | 1.53× | 1.53× | 0.33 | +2.33 | +0.04 |
| cnn_trades+side | 1 | 58 | 0.297 | 1.53× | 1.53× | 0.33 | +12.32 | +0.23 |
| cnn_trades | 1 | 58 | 0.290 | 1.49× | 1.49× | 0.33 | +12.00 | +0.27 |
| xgb_wallets | 1 | 58 | 0.287 | 1.47× | 1.47× | 0.33 | +12.80 | +1.17 |
| logistic_repo_recipe | 1 | 58 | 0.272 | 1.40× | 1.40× | 0.27 | +0.39 | -1.53 |
| xgb_holders | 1 | 58 | 0.269 | 1.38× | 1.38× | 0.17 | +7.93 | -4.03 |
| cnn_trades+side+pre | 1 | 58 | 0.259 | 1.33× | 1.33× | 0.23 | +10.36 | -1.40 |
| xgb_context | 1 | 58 | 0.248 | 1.27× | 1.27× | 0.27 | +0.73 | -1.07 |

Test days: 2026-09-02

