# Model ledger — held-out days averaged

Latest evaluation per (mode, model, test day); lift = PR-AUC / base rate.


## age mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_holders | 3 | 175 | 0.255 | 3.68× | 3.47× | 0.23 | -6.34 | -12.00 |
| ensemble:xgb_botlive+context+cnn_trades+side+pre+xgb_all+wallets | 2 | 113 | 0.211 | 3.59× | 3.38× | 0.18 | -6.75 | -10.20 |
| xgb_botlive | 2 | 113 | 0.211 | 3.55× | 3.03× | 0.20 | -4.04 | -7.42 |
| xgb_shape+holders | 3 | 175 | 0.251 | 3.52× | 3.02× | 0.23 | -3.60 | -8.65 |
| xgb_all+wallets | 3 | 175 | 0.246 | 3.50× | 3.27× | 0.24 | -3.04 | -8.14 |
| ensemble:xgb_holders+cnn_trades+side | 2 | 159 | 0.273 | 3.48× | 3.07× | 0.27 | -3.55 | -7.58 |
| xgb_holders+wallets | 3 | 175 | 0.236 | 3.42× | 3.00× | 0.23 | -4.10 | -9.84 |
| xgb_all | 3 | 175 | 0.245 | 3.42× | 2.77× | 0.24 | -2.75 | -7.85 |
| cnn_trades+side+pre | 3 | 175 | 0.238 | 3.41× | 3.30× | 0.21 | -6.00 | -11.59 |
| xgb_botlive+context | 2 | 113 | 0.199 | 3.37× | 3.01× | 0.20 | -4.86 | -8.24 |
| xgb_shape | 3 | 175 | 0.220 | 3.11× | 2.55× | 0.23 | -1.61 | -6.59 |
| cnn_trades+side | 3 | 175 | 0.216 | 3.06× | 2.53× | 0.20 | -5.79 | -11.27 |
| cnn_trades | 4 | 252 | 0.231 | 2.96× | 2.63× | 0.22 | -5.78 | -13.10 |
| logistic_repo_recipe | 3 | 175 | 0.193 | 2.71× | 2.44× | 0.20 | -7.88 | -13.25 |
| xgb_pnl:all+wallets | 2 | 113 | 0.157 | 2.64× | 2.18× | 0.17 | -4.47 | -7.77 |
| xgb_pnl:botlive+context | 2 | 113 | 0.146 | 2.48× | 2.29× | 0.17 | -4.05 | -7.40 |
| xgb_wallets | 3 | 175 | 0.144 | 2.06× | 1.69× | 0.15 | -4.91 | -9.89 |
| xgb_context | 3 | 175 | 0.085 | 1.21× | 0.97× | 0.06 | -15.22 | -18.95 |

Test days: 2026-08-31, 2026-09-02, 2026-09-03, 2026-09-04


## cross mode

| model | days | positives | mean PR-AUC | mean lift | min lift | mean P@10% | Σ PnL@10% | Σ PnL ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| cnn_trades+side | 3 | 191 | 0.320 | 1.74× | 1.53× | 0.39 | +18.12 | +2.34 |
| cnn_trades+side+pre | 3 | 191 | 0.314 | 1.71× | 1.33× | 0.34 | +17.04 | +1.60 |
| ensemble:xgb_botlive+context+cnn_trades+side+pre+xgb_all+wallets | 2 | 133 | 0.299 | 1.67× | 1.43× | 0.33 | +6.59 | +2.87 |
| cnn_trades | 3 | 191 | 0.300 | 1.63× | 1.49× | 0.34 | +14.89 | -0.30 |
| ensemble:xgb_holders+cnn_trades+side | 2 | 168 | 0.302 | 1.62× | 1.57× | 0.41 | +20.27 | +6.07 |
| xgb_all+wallets | 3 | 194 | 0.289 | 1.55× | 1.33× | 0.31 | +15.44 | -0.27 |
| xgb_pnl:botlive+context+recent | 1 | 26 | 0.271 | 1.44× | 1.44× | 0.36 | +1.08 | -0.50 |
| xgb_botlive+context | 2 | 136 | 0.258 | 1.43× | 1.43× | 0.32 | +2.88 | -0.66 |
| xgb_botlive+context+recent | 1 | 26 | 0.269 | 1.43× | 1.43× | 0.36 | +0.72 | -0.91 |
| xgb_botlive+recent | 1 | 26 | 0.269 | 1.43× | 1.43× | 0.29 | -0.03 | -1.61 |
| xgb_all | 3 | 194 | 0.265 | 1.42× | 1.20× | 0.28 | +11.11 | -4.67 |
| xgb_holders+wallets | 3 | 194 | 0.264 | 1.42× | 1.30× | 0.28 | -0.40 | -6.00 |
| xgb_botlive | 2 | 136 | 0.256 | 1.42× | 1.30× | 0.30 | +0.76 | -2.72 |
| xgb_shape+holders | 3 | 194 | 0.263 | 1.41× | 1.14× | 0.27 | +9.75 | -5.24 |
| xgb_shape | 3 | 194 | 0.262 | 1.41× | 1.23× | 0.28 | +11.67 | -3.10 |
| xgb_pnl:botlive+context | 2 | 136 | 0.242 | 1.34× | 1.21× | 0.24 | +0.03 | -3.43 |
| xgb_wallets | 3 | 194 | 0.239 | 1.29× | 1.04× | 0.31 | +12.33 | -2.68 |
| xgb_holders | 3 | 194 | 0.238 | 1.28× | 1.21× | 0.19 | +6.03 | -8.75 |
| logistic_repo_recipe | 3 | 194 | 0.237 | 1.27× | 1.19× | 0.23 | -1.86 | -6.59 |
| xgb_holders+wallets+recent | 1 | 26 | 0.240 | 1.27× | 1.27× | 0.21 | -0.78 | -2.32 |
| xgb_holders+recent | 1 | 26 | 0.238 | 1.26× | 1.26× | 0.21 | -1.04 | -2.65 |
| xgb_pnl:all+wallets | 2 | 136 | 0.227 | 1.25× | 1.18× | 0.27 | +3.75 | +0.41 |
| xgb_wallets+recent | 1 | 26 | 0.233 | 1.24× | 1.24× | 0.21 | -0.40 | -1.96 |
| cnn_botlive+side | 1 | 26 | 0.231 | 1.23× | 1.23× | 0.29 | -0.05 | -1.68 |
| xgb_context+recent | 1 | 26 | 0.229 | 1.22× | 1.22× | 0.14 | -0.81 | -1.88 |
| xgb_shape+recent | 1 | 26 | 0.211 | 1.12× | 1.12× | 0.21 | -0.89 | -2.44 |
| xgb_shape+holders+recent | 1 | 26 | 0.210 | 1.12× | 1.12× | 0.14 | -1.61 | -2.61 |
| xgb_all+recent | 1 | 26 | 0.202 | 1.07× | 1.07× | 0.07 | -2.07 | -2.65 |
| xgb_context | 3 | 194 | 0.198 | 1.06× | 0.87× | 0.15 | -5.01 | -8.53 |
| xgb_all+wallets+recent | 1 | 26 | 0.200 | 1.06× | 1.06× | 0.14 | -1.30 | -2.43 |
| xgb_pnl:all+wallets+recent | 1 | 26 | 0.191 | 1.01× | 1.01× | 0.14 | -0.59 | -1.78 |

Test days: 2026-09-02, 2026-09-03, 2026-09-04

