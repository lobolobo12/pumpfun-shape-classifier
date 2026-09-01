# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 277 | 0.331 | 0.578 | 0.67 | 0.36 | 0.32 | 0.75 | -0.88 |
| xgb_holders | 277 | 0.290 | 0.526 | 0.67 | 0.29 | 0.21 | -0.31 | -2.51 |
| xgb_shape+holders | 277 | 0.348 | 0.553 | 0.67 | 0.43 | 0.46 | 4.27 | 2.07 |
| xgb_all | 277 | 0.339 | 0.575 | 0.33 | 0.36 | 0.39 | 2.81 | 0.60 |
| xgb_context | 277 | 0.247 | 0.433 | 0.33 | 0.29 | 0.25 | -0.11 | -1.75 |
| logistic_repo_recipe | 277 | 0.357 | 0.578 | 0.67 | 0.50 | 0.39 | 2.79 | 0.56 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- gini_buy_size: 19.49
- lows: 16.282
- n_sellers: 14.846
- step_gini: 13.462
- largest_buy_share: 12.634
- sol_last60: 12.578
- log_ret_window: 12.47
- max_drawdown: 12.167
- price_slope: 12.074
- biggest_buy_vs_curve: 11.993
- run_from_low: 11.968
- n_trades: 11.218
- last_trade_t: 10.771
- sell_share_sol: 10.377
- lows_per_min: 10.231

## xgb_holders: top gain features

- top3_share: 10.744
- gini_hold: 10.03
- tokens_out_pct: 10.018
- launch_bundle_share: 9.908
- top1_share: 9.454
- exited_share: 8.878
- holders_n: 8.481
- first_slot_share: 8.428
- dev_share: 8.394
- top10_share: 7.47
- buyers_n: 7.432
- same_size_share: 6.223

## xgb_shape+holders: top gain features

- gini_buy_size: 11.212
- top1_share: 9.57
- step_gini: 9.305
- top3_share: 9.258
- exited_share: 8.844
- holders_n: 8.697
- sol_last60: 8.651
- sell_share_sol: 8.354
- lows: 8.06
- buyers_last60: 7.928
- lows_per_min: 7.846
- buy_size_cv: 7.844
- launch_bundle_share: 7.82
- dev_share: 7.776
- first_slot_share: 7.751

## xgb_all: top gain features

- creator_prior_tp_rate: 15.01
- gini_buy_size: 14.677
- top1_share: 14.111
- creator_prior_launches: 12.264
- step_gini: 12.01
- buy_size_cv: 11.518
- sol_last60: 11.386
- n_sellers: 11.116
- launch_bundle_share: 10.594
- tokens_out_pct: 10.543
- exited_share: 10.366
- holders_n: 10.239
- top3_share: 10.141
- max_drawdown: 10.002
- first_slot_share: 9.901

## xgb_context: top gain features

- hour_sin: 3.939
- hour_cos: 3.431
- live_at_entry: 2.639
- is_native_launch: 2.568
- replies_at_entry: 1.613
