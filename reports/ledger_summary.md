# Model ledger — held-out days averaged

Latest evaluation per (mode, model, test day); lift = PR-AUC / base rate.


## age mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_botlive | 1 | 97 | 0.268 | 4.07× | 4.07× | 0.24 | -1.37 | -3.12 |
| ensemble:xgb_botlive+context+cnn_trades+side+pre+xgb_all+wallets | 1 | 97 | 0.251 | 3.81× | 3.81× | 0.24 | -3.28 | -5.12 |
| xgb_shape+holders | 2 | 159 | 0.301 | 3.77× | 3.67× | 0.29 | -0.74 | -4.20 |
| xgb_all | 2 | 159 | 0.298 | 3.74× | 3.61× | 0.28 | -0.56 | -4.03 |
| xgb_botlive+context | 1 | 97 | 0.246 | 3.73× | 3.73× | 0.25 | -2.10 | -3.85 |
| xgb_all+wallets | 2 | 159 | 0.287 | 3.62× | 3.43× | 0.28 | -0.28 | -3.75 |
| xgb_holders | 2 | 159 | 0.284 | 3.56× | 3.47× | 0.26 | -3.28 | -7.33 |
| ensemble:xgb_holders+cnn_trades+side | 2 | 159 | 0.273 | 3.48× | 3.07× | 0.27 | -3.55 | -7.58 |
| xgb_shape | 2 | 159 | 0.266 | 3.39× | 3.01× | 0.28 | +1.32 | -2.08 |
| xgb_holders+wallets | 2 | 159 | 0.263 | 3.35× | 3.00× | 0.24 | -2.48 | -6.60 |
| cnn_trades+side+pre | 2 | 159 | 0.267 | 3.34× | 3.30× | 0.26 | -2.28 | -6.32 |
| cnn_trades+side | 2 | 159 | 0.260 | 3.32× | 2.92× | 0.26 | -2.05 | -5.97 |
| xgb_pnl:all+wallets | 1 | 97 | 0.203 | 3.09× | 3.09× | 0.24 | -1.80 | -3.50 |
| cnn_trades | 3 | 236 | 0.263 | 3.05× | 2.63× | 0.27 | -2.25 | -8.03 |
| logistic_repo_recipe | 2 | 159 | 0.227 | 2.85× | 2.80× | 0.24 | -4.69 | -8.50 |
| xgb_pnl:botlive+context | 1 | 97 | 0.176 | 2.67× | 2.67× | 0.22 | -1.53 | -3.27 |
| xgb_wallets | 2 | 159 | 0.174 | 2.24× | 1.84× | 0.18 | -3.62 | -7.01 |
| xgb_context | 2 | 159 | 0.103 | 1.33× | 1.07× | 0.07 | -12.50 | -15.71 |

Test days: 2026-08-31, 2026-09-02, 2026-09-03


## cross mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| ensemble:xgb_botlive+context+cnn_trades+side+pre+xgb_all+wallets | 1 | 110 | 0.344 | 1.92× | 1.92× | 0.43 | +7.07 | +4.90 |
| xgb_botlive+context | 1 | 110 | 0.335 | 1.87× | 1.87× | 0.41 | +7.10 | +4.87 |
| xgb_all+wallets | 2 | 168 | 0.338 | 1.80× | 1.76× | 0.39 | +20.20 | +5.73 |
| xgb_all | 2 | 168 | 0.321 | 1.72× | 1.66× | 0.39 | +19.65 | +5.19 |
| xgb_shape | 2 | 168 | 0.310 | 1.65× | 1.63× | 0.40 | +18.02 | +3.79 |
| xgb_shape+holders | 2 | 168 | 0.305 | 1.63× | 1.57× | 0.38 | +17.82 | +3.36 |
| ensemble:xgb_holders+cnn_trades+side | 2 | 168 | 0.302 | 1.62× | 1.57× | 0.41 | +20.27 | +6.07 |
| cnn_trades | 2 | 168 | 0.296 | 1.58× | 1.49× | 0.32 | +13.93 | +0.34 |
| cnn_trades+side | 2 | 168 | 0.295 | 1.58× | 1.53× | 0.35 | +16.44 | +2.26 |
| cnn_trades+side+pre | 2 | 168 | 0.292 | 1.57× | 1.33× | 0.32 | +16.23 | +2.37 |
| xgb_holders+wallets | 2 | 168 | 0.286 | 1.53× | 1.53× | 0.37 | +8.59 | +4.19 |
| xgb_pnl:all+wallets | 1 | 110 | 0.266 | 1.48× | 1.48× | 0.31 | +3.83 | +1.80 |
| xgb_holders | 2 | 168 | 0.270 | 1.44× | 1.38× | 0.25 | +10.41 | -3.60 |
| logistic_repo_recipe | 2 | 168 | 0.268 | 1.43× | 1.40× | 0.27 | +0.60 | -3.03 |
| xgb_pnl:botlive+context | 1 | 110 | 0.246 | 1.37× | 1.37× | 0.25 | +2.58 | +0.43 |
| xgb_botlive | 1 | 110 | 0.242 | 1.35× | 1.35× | 0.31 | +1.59 | -0.41 |
| xgb_wallets | 2 | 168 | 0.247 | 1.32× | 1.16× | 0.30 | +13.59 | +0.19 |
| xgb_context | 2 | 168 | 0.238 | 1.27× | 1.27× | 0.26 | +0.70 | -2.85 |

Test days: 2026-09-02, 2026-09-03

