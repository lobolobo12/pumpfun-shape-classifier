# Model ledger — held-out days averaged

Latest evaluation per (mode, model, test day); lift = PR-AUC / base rate.


## age mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape+holders | 2 | 86 | 0.364 | 4.08× | 3.67× | 0.35 | +4.87 | +1.55 |
| xgb_all | 2 | 86 | 0.359 | 4.02× | 3.61× | 0.35 | +4.46 | +1.03 |
| xgb_all+wallets | 2 | 86 | 0.331 | 3.69× | 3.43× | 0.34 | +3.31 | -0.03 |
| xgb_holders | 2 | 86 | 0.329 | 3.67× | 3.47× | 0.28 | +1.60 | -2.31 |
| logistic_repo_recipe | 2 | 86 | 0.297 | 3.33× | 2.80× | 0.27 | -0.41 | -3.98 |
| xgb_holders+wallets | 2 | 86 | 0.295 | 3.30× | 3.00× | 0.26 | -0.98 | -5.04 |
| ensemble:xgb_holders+cnn_trades+side | 2 | 86 | 0.294 | 3.28× | 3.07× | 0.34 | +4.26 | +0.34 |
| cnn_trades+side+pre | 2 | 86 | 0.294 | 3.28× | 3.25× | 0.28 | +1.97 | -1.88 |
| xgb_shape | 2 | 86 | 0.289 | 3.23× | 3.01× | 0.30 | +2.25 | -1.03 |
| cnn_trades+side | 2 | 86 | 0.287 | 3.21× | 2.92× | 0.31 | +2.08 | -1.91 |
| cnn_trades | 3 | 163 | 0.285 | 3.05× | 2.63× | 0.27 | +0.96 | -4.70 |
| xgb_wallets | 2 | 86 | 0.179 | 2.00× | 1.84× | 0.22 | -0.29 | -3.51 |
| xgb_context | 2 | 86 | 0.095 | 1.05× | 1.04× | 0.07 | -5.99 | -8.59 |

Test days: 2026-08-31, 2026-09-02, 2026-09-03


## cross mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_all+wallets | 2 | 85 | 0.383 | 1.88× | 1.84× | 0.38 | +14.93 | +0.67 |
| ensemble:xgb_holders+cnn_trades+side | 2 | 85 | 0.382 | 1.86× | 1.57× | 0.51 | +17.05 | +3.01 |
| xgb_all | 2 | 85 | 0.370 | 1.81× | 1.66× | 0.38 | +14.54 | +0.29 |
| xgb_holders+wallets | 2 | 85 | 0.361 | 1.76× | 1.53× | 0.40 | +4.38 | +0.14 |
| cnn_trades+side+pre | 2 | 85 | 0.348 | 1.69× | 1.33× | 0.35 | +12.36 | -1.33 |
| cnn_trades+side | 2 | 85 | 0.335 | 1.64× | 1.53× | 0.40 | +14.00 | +0.31 |
| xgb_shape+holders | 2 | 85 | 0.332 | 1.63× | 1.58× | 0.39 | +14.78 | +0.56 |
| xgb_shape | 2 | 85 | 0.329 | 1.62× | 1.60× | 0.41 | +15.21 | +1.20 |
| cnn_trades | 2 | 85 | 0.330 | 1.61× | 1.49× | 0.36 | +13.10 | -0.37 |
| xgb_wallets | 2 | 85 | 0.321 | 1.57× | 1.47× | 0.32 | +13.31 | +0.12 |
| logistic_repo_recipe | 2 | 85 | 0.319 | 1.56× | 1.40× | 0.29 | +0.59 | -2.87 |
| xgb_holders | 2 | 85 | 0.317 | 1.55× | 1.38× | 0.28 | +9.24 | -4.65 |
| xgb_context | 2 | 85 | 0.301 | 1.47× | 1.27× | 0.33 | +1.69 | -1.68 |

Test days: 2026-09-02, 2026-09-03

