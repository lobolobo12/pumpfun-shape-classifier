# Model ledger — held-out days averaged

Latest evaluation per (mode, model, test day); lift = PR-AUC / base rate.


## age mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape+holders | 1 | 20 | 0.328 | 3.68× | 3.68× | 0.32 | +1.93 | -0.30 |
| ensemble:xgb_holders+cnn_trades+side | 1 | 20 | 0.285 | 3.20× | 3.20× | 0.23 | +0.60 | -1.64 |
| cnn_trades | 2 | 97 | 0.288 | 3.03× | 2.63× | 0.25 | +0.03 | -3.99 |
| cnn_trades+side+pre | 1 | 20 | 0.266 | 2.98× | 2.98× | 0.27 | +0.53 | -1.05 |
| xgb_shape | 1 | 20 | 0.255 | 2.85× | 2.85× | 0.36 | +2.53 | +0.12 |
| xgb_holders | 1 | 20 | 0.254 | 2.85× | 2.85× | 0.32 | +1.10 | -1.16 |
| cnn_trades+side | 1 | 20 | 0.251 | 2.81× | 2.81× | 0.23 | +0.60 | -1.63 |
| xgb_holders+wallets | 1 | 20 | 0.244 | 2.73× | 2.73× | 0.27 | +0.85 | -1.41 |
| xgb_all | 1 | 20 | 0.240 | 2.69× | 2.69× | 0.32 | +1.33 | -0.37 |
| xgb_all+wallets | 1 | 20 | 0.236 | 2.65× | 2.65× | 0.32 | +1.36 | -0.19 |
| logistic_repo_recipe | 1 | 20 | 0.186 | 2.08× | 2.08× | 0.14 | -1.96 | -3.63 |
| xgb_wallets | 1 | 20 | 0.134 | 1.50× | 1.50× | 0.14 | -0.81 | -2.33 |
| xgb_context | 1 | 20 | 0.095 | 1.06× | 1.06× | 0.09 | -0.82 | -2.09 |

Test days: 2026-08-31, 2026-09-02


## cross mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_holders | 1 | 18 | 0.473 | 2.71× | 2.71× | 0.60 | +12.73 | +0.72 |
| ensemble:xgb_holders+cnn_trades+side | 1 | 18 | 0.457 | 2.62× | 2.62× | 0.60 | +12.87 | +0.78 |
| xgb_all+wallets | 1 | 18 | 0.424 | 2.43× | 2.43× | 0.50 | +11.73 | -0.02 |
| xgb_holders+wallets | 1 | 18 | 0.393 | 2.25× | 2.25× | 0.40 | +11.31 | -0.77 |
| xgb_all | 1 | 18 | 0.370 | 2.12× | 2.12× | 0.40 | +1.59 | -0.46 |
| cnn_trades+side | 1 | 18 | 0.351 | 2.01× | 2.01× | 0.50 | +12.12 | +0.04 |
| cnn_trades+side+pre | 1 | 18 | 0.276 | 1.58× | 1.58× | 0.20 | +9.74 | -1.53 |
| xgb_shape | 1 | 18 | 0.268 | 1.53× | 1.53× | 0.20 | -0.04 | -1.50 |
| xgb_shape+holders | 1 | 18 | 0.268 | 1.53× | 1.53× | 0.40 | +1.36 | -0.68 |
| logistic_repo_recipe | 1 | 18 | 0.262 | 1.50× | 1.50× | 0.30 | +0.51 | -1.41 |
| cnn_trades | 1 | 18 | 0.231 | 1.32× | 1.32× | 0.30 | +0.60 | -1.49 |
| xgb_wallets | 1 | 18 | 0.179 | 1.02× | 1.02× | 0.10 | -1.04 | -1.46 |
| xgb_context | 1 | 18 | 0.154 | 0.88× | 0.88× | 0.20 | +0.07 | -1.39 |

Test days: 2026-09-02

