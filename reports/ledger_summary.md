# Model ledger — held-out days averaged

Latest evaluation per (mode, model, test day); lift = PR-AUC / base rate.


## age mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_holders | 3 | 175 | 0.256 | 3.68× | 3.47× | 0.22 | -6.93 | -12.60 |
| xgb_all+wallets | 3 | 175 | 0.253 | 3.62× | 3.43× | 0.24 | -2.72 | -7.82 |
| xgb_holders+wallets | 3 | 175 | 0.242 | 3.56× | 3.00× | 0.25 | -3.13 | -8.91 |
| xgb_botlive | 2 | 113 | 0.210 | 3.54× | 3.02× | 0.18 | -4.89 | -8.22 |
| ensemble:xgb_holders+cnn_trades+side | 2 | 159 | 0.273 | 3.48× | 3.07× | 0.27 | -3.55 | -7.58 |
| ensemble:xgb_botlive+context+cnn_trades+side+pre+xgb_all+wallets | 2 | 113 | 0.201 | 3.40× | 2.99× | 0.18 | -7.00 | -10.44 |
| xgb_botlive+context | 2 | 113 | 0.200 | 3.39× | 3.04× | 0.20 | -4.86 | -8.23 |
| xgb_all | 3 | 175 | 0.243 | 3.37× | 2.64× | 0.24 | -2.56 | -7.66 |
| cnn_trades+side+pre | 3 | 175 | 0.236 | 3.37× | 3.30× | 0.21 | -7.04 | -12.64 |
| xgb_shape+holders | 3 | 175 | 0.243 | 3.36× | 2.53× | 0.22 | -4.20 | -9.23 |
| xgb_shape | 3 | 175 | 0.220 | 3.11× | 2.54× | 0.22 | -2.26 | -7.24 |
| cnn_trades+side | 3 | 175 | 0.218 | 3.09× | 2.62× | 0.21 | -5.03 | -10.51 |
| cnn_trades | 4 | 252 | 0.238 | 3.09× | 2.63× | 0.25 | -4.44 | -11.83 |
| logistic_repo_recipe | 3 | 175 | 0.199 | 2.83× | 2.79× | 0.22 | -6.63 | -12.06 |
| xgb_pnl:all+wallets | 2 | 113 | 0.158 | 2.65× | 2.21× | 0.15 | -5.62 | -8.37 |
| xgb_pnl:botlive+context | 2 | 113 | 0.146 | 2.48× | 2.30× | 0.17 | -4.30 | -7.66 |
| xgb_wallets | 3 | 175 | 0.146 | 2.10× | 1.81× | 0.15 | -4.67 | -9.66 |
| xgb_context | 3 | 175 | 0.086 | 1.23× | 1.03× | 0.06 | -15.04 | -18.89 |

Test days: 2026-08-31, 2026-09-02, 2026-09-03, 2026-09-04


## cross mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| ensemble:xgb_botlive+context+cnn_trades+side+pre+xgb_all+wallets | 2 | 133 | 0.338 | 1.89× | 1.86× | 0.37 | +7.36 | +3.58 |
| cnn_trades+side | 3 | 191 | 0.324 | 1.77× | 1.53× | 0.39 | +18.09 | +2.32 |
| cnn_trades+side+pre | 3 | 191 | 0.322 | 1.76× | 1.33× | 0.37 | +18.20 | +2.75 |
| cnn_trades | 3 | 191 | 0.299 | 1.63× | 1.49× | 0.32 | +13.79 | -1.40 |
| ensemble:xgb_holders+cnn_trades+side | 2 | 168 | 0.302 | 1.62× | 1.57× | 0.41 | +20.27 | +6.07 |
| xgb_all+wallets | 3 | 194 | 0.289 | 1.55× | 1.32× | 0.31 | +15.44 | -0.27 |
| xgb_all | 3 | 194 | 0.272 | 1.46× | 1.32× | 0.31 | +11.98 | -3.82 |
| xgb_botlive+context | 2 | 136 | 0.260 | 1.44× | 1.43× | 0.36 | +3.62 | +0.09 |
| xgb_holders+wallets | 3 | 194 | 0.265 | 1.43× | 1.30× | 0.25 | -1.16 | -6.76 |
| xgb_shape+holders | 3 | 194 | 0.265 | 1.42× | 1.18× | 0.24 | +9.05 | -5.36 |
| xgb_botlive | 2 | 136 | 0.253 | 1.40× | 1.30× | 0.26 | +0.06 | -3.35 |
| xgb_shape | 3 | 194 | 0.261 | 1.40× | 1.20× | 0.28 | +11.65 | -3.12 |
| cnn_botlive+side | 1 | 26 | 0.257 | 1.36× | 1.36× | 0.21 | -0.73 | -2.32 |
| xgb_pnl:botlive+context | 2 | 136 | 0.239 | 1.32× | 1.21× | 0.28 | +0.69 | -2.80 |
| xgb_holders | 3 | 194 | 0.238 | 1.28× | 1.22× | 0.22 | +6.74 | -8.56 |
| xgb_pnl:all+wallets | 2 | 136 | 0.231 | 1.28× | 1.23× | 0.15 | +1.67 | -0.78 |
| logistic_repo_recipe | 3 | 194 | 0.233 | 1.25× | 1.17× | 0.23 | -1.78 | -6.41 |
| xgb_wallets | 3 | 194 | 0.233 | 1.25× | 1.04× | 0.31 | +12.57 | -2.43 |
| xgb_context | 3 | 194 | 0.201 | 1.08× | 0.92× | 0.17 | -4.28 | -8.52 |

Test days: 2026-09-02, 2026-09-03, 2026-09-04

