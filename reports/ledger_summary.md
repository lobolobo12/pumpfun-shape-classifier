# Model ledger — held-out days averaged

Latest evaluation per (mode, model, test day); lift = PR-AUC / base rate.


## age mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_holders | 3 | 175 | 0.265 | 3.87× | 3.47× | 0.23 | -6.31 | -11.98 |
| xgb_botlive+context | 2 | 113 | 0.214 | 3.66× | 3.59× | 0.20 | -5.03 | -8.41 |
| xgb_botlive | 2 | 113 | 0.210 | 3.53× | 2.99× | 0.20 | -3.52 | -6.86 |
| xgb_holders+wallets | 3 | 175 | 0.239 | 3.50× | 3.00× | 0.25 | -3.42 | -9.16 |
| ensemble:xgb_holders+cnn_trades+side | 2 | 159 | 0.273 | 3.48× | 3.07× | 0.27 | -3.55 | -7.58 |
| cnn_trades+side+pre | 3 | 175 | 0.241 | 3.47× | 3.30× | 0.23 | -5.48 | -11.13 |
| xgb_shape+holders | 3 | 175 | 0.248 | 3.45× | 2.81× | 0.24 | -2.95 | -8.00 |
| xgb_all+wallets | 3 | 175 | 0.243 | 3.44× | 3.09× | 0.24 | -2.37 | -7.47 |
| xgb_all | 3 | 175 | 0.245 | 3.41× | 2.75× | 0.24 | -2.63 | -7.73 |
| ensemble:xgb_botlive+context+cnn_trades+side+pre+xgb_all+wallets | 2 | 113 | 0.200 | 3.38× | 2.96× | 0.18 | -6.15 | -9.59 |
| xgb_shape | 3 | 175 | 0.223 | 3.17× | 2.73× | 0.22 | -2.27 | -7.23 |
| cnn_trades | 4 | 252 | 0.238 | 3.09× | 2.63× | 0.25 | -4.44 | -11.83 |
| cnn_trades+side | 3 | 175 | 0.216 | 3.06× | 2.54× | 0.20 | -5.75 | -11.23 |
| logistic_repo_recipe | 3 | 175 | 0.194 | 2.74× | 2.53× | 0.21 | -7.38 | -12.76 |
| xgb_pnl:all+wallets | 2 | 113 | 0.153 | 2.56× | 2.03× | 0.17 | -4.78 | -8.07 |
| xgb_pnl:botlive+context | 2 | 113 | 0.148 | 2.51× | 2.36× | 0.19 | -3.23 | -6.58 |
| xgb_wallets | 3 | 175 | 0.146 | 2.10× | 1.81× | 0.15 | -4.67 | -9.66 |
| xgb_context | 3 | 175 | 0.086 | 1.23× | 1.02× | 0.06 | -15.34 | -19.22 |

Test days: 2026-08-31, 2026-09-02, 2026-09-03, 2026-09-04


## cross mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| cnn_trades+side | 3 | 191 | 0.316 | 1.72× | 1.53× | 0.39 | +18.07 | +2.30 |
| ensemble:xgb_botlive+context+cnn_trades+side+pre+xgb_all+wallets | 2 | 133 | 0.301 | 1.68× | 1.44× | 0.37 | +7.32 | +3.54 |
| cnn_trades+side+pre | 3 | 191 | 0.306 | 1.67× | 1.33× | 0.37 | +18.04 | +2.59 |
| cnn_trades | 3 | 191 | 0.299 | 1.63× | 1.49× | 0.32 | +13.79 | -1.40 |
| ensemble:xgb_holders+cnn_trades+side | 2 | 168 | 0.302 | 1.62× | 1.57× | 0.41 | +20.27 | +6.07 |
| xgb_all+wallets | 3 | 194 | 0.289 | 1.55× | 1.31× | 0.31 | +15.44 | -0.27 |
| xgb_shape | 3 | 194 | 0.280 | 1.51× | 1.37× | 0.31 | +12.34 | -2.95 |
| xgb_shape+holders | 3 | 194 | 0.279 | 1.50× | 1.40× | 0.27 | +9.60 | -5.38 |
| xgb_holders+wallets | 3 | 194 | 0.277 | 1.50× | 1.30× | 0.28 | -0.60 | -6.21 |
| xgb_botlive | 2 | 136 | 0.266 | 1.48× | 1.30× | 0.34 | +1.59 | -1.89 |
| xgb_all | 3 | 194 | 0.273 | 1.47× | 1.33× | 0.28 | +11.09 | -4.70 |
| logistic_repo_recipe | 3 | 194 | 0.269 | 1.45× | 1.19× | 0.28 | -0.33 | -5.67 |
| xgb_holders | 3 | 194 | 0.264 | 1.43× | 1.25× | 0.27 | +7.99 | -7.32 |
| xgb_botlive+context | 2 | 136 | 0.251 | 1.39× | 1.34× | 0.32 | +2.82 | -0.72 |
| xgb_pnl:botlive+context | 2 | 136 | 0.246 | 1.36× | 1.21× | 0.28 | +0.58 | -2.91 |
| xgb_pnl:all+wallets | 2 | 136 | 0.232 | 1.28× | 1.24× | 0.23 | +2.98 | -0.30 |
| xgb_wallets | 3 | 194 | 0.233 | 1.25× | 1.04× | 0.31 | +12.57 | -2.43 |
| xgb_context | 3 | 194 | 0.201 | 1.08× | 0.92× | 0.17 | -4.28 | -8.52 |

Test days: 2026-09-02, 2026-09-03, 2026-09-04

