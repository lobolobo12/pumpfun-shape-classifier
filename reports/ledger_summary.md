# Model ledger — held-out days averaged

Latest evaluation per (mode, model, test day); lift = PR-AUC / base rate.


## age mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape+holders | 1 | 20 | 0.336 | 3.76× | 3.76× | 0.32 | +1.60 | -0.64 |
| cnn_trades+side+pre | 1 | 20 | 0.309 | 3.47× | 3.47× | 0.32 | +2.04 | -0.20 |
| ensemble:xgb_holders+cnn_trades+side | 1 | 20 | 0.283 | 3.17× | 3.17× | 0.27 | +1.39 | -0.89 |
| cnn_trades | 2 | 97 | 0.288 | 3.03× | 2.63× | 0.25 | +0.03 | -3.99 |
| xgb_all | 1 | 20 | 0.262 | 2.93× | 2.93× | 0.32 | +1.03 | -0.56 |
| xgb_shape | 1 | 20 | 0.257 | 2.88× | 2.88× | 0.27 | +1.12 | -1.11 |
| xgb_holders | 1 | 20 | 0.254 | 2.85× | 2.85× | 0.32 | +1.10 | -1.16 |
| xgb_all+wallets | 1 | 20 | 0.254 | 2.85× | 2.85× | 0.36 | +2.40 | +0.12 |
| cnn_trades+side | 1 | 20 | 0.249 | 2.79× | 2.79× | 0.27 | +1.39 | -0.89 |
| xgb_holders+wallets | 1 | 20 | 0.244 | 2.73× | 2.73× | 0.27 | +0.85 | -1.41 |
| logistic_repo_recipe | 1 | 20 | 0.186 | 2.08× | 2.08× | 0.14 | -1.96 | -3.63 |
| xgb_context | 1 | 20 | 0.156 | 1.74× | 1.74× | 0.18 | +0.08 | -1.46 |
| xgb_wallets | 1 | 20 | 0.134 | 1.50× | 1.50× | 0.14 | -0.81 | -2.33 |

Test days: 2026-08-31, 2026-09-02


## cross mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_holders | 1 | 18 | 0.473 | 2.71× | 2.71× | 0.60 | +12.73 | +0.72 |
| ensemble:xgb_holders+cnn_trades+side | 1 | 18 | 0.411 | 2.35× | 2.35× | 0.50 | +12.13 | +0.05 |
| xgb_holders+wallets | 1 | 18 | 0.393 | 2.25× | 2.25× | 0.40 | +11.31 | -0.77 |
| xgb_shape+holders | 1 | 18 | 0.391 | 2.24× | 2.24× | 0.60 | +12.82 | +0.74 |
| xgb_all | 1 | 18 | 0.355 | 2.03× | 2.03× | 0.40 | +11.61 | -0.47 |
| xgb_shape | 1 | 18 | 0.335 | 1.92× | 1.92× | 0.40 | +1.34 | -0.42 |
| xgb_all+wallets | 1 | 18 | 0.324 | 1.85× | 1.85× | 0.40 | +11.54 | -0.55 |
| cnn_trades+side+pre | 1 | 18 | 0.322 | 1.84× | 1.84× | 0.40 | +11.35 | -0.73 |
| logistic_repo_recipe | 1 | 18 | 0.262 | 1.50× | 1.50× | 0.30 | +0.51 | -1.41 |
| cnn_trades+side | 1 | 18 | 0.257 | 1.47× | 1.47× | 0.30 | +10.57 | -1.51 |
| cnn_trades | 1 | 18 | 0.231 | 1.32× | 1.32× | 0.30 | +0.60 | -1.49 |
| xgb_context | 1 | 18 | 0.184 | 1.05× | 1.05× | 0.20 | -0.05 | -1.41 |
| xgb_wallets | 1 | 18 | 0.179 | 1.02× | 1.02× | 0.10 | -1.04 | -1.46 |

Test days: 2026-09-02

