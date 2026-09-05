# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 138 | 0.219 | 0.565 | 0.00 | 0.14 | 0.21 | -0.87 | -2.43 |
| xgb_holders | 138 | 0.305 | 0.607 | 1.00 | 0.43 | 0.36 | 0.43 | -1.19 |
| xgb_shape+holders | 138 | 0.253 | 0.543 | 1.00 | 0.29 | 0.21 | -0.89 | -2.45 |
| xgb_all | 138 | 0.201 | 0.557 | 0.00 | 0.00 | 0.07 | -2.36 | -2.65 |
| xgb_context | 138 | 0.272 | 0.535 | 1.00 | 0.43 | 0.29 | 0.58 | -1.01 |
| xgb_wallets | 138 | 0.263 | 0.496 | 1.00 | 0.43 | 0.36 | 0.66 | -0.94 |
| xgb_holders+wallets | 138 | 0.293 | 0.624 | 0.00 | 0.29 | 0.36 | 0.39 | -1.20 |
| xgb_all+wallets | 138 | 0.204 | 0.552 | 0.00 | 0.00 | 0.14 | -1.64 | -2.64 |
| xgb_botlive | 138 | 0.326 | 0.570 | 1.00 | 0.43 | 0.36 | 0.64 | -0.94 |
| xgb_botlive+context | 138 | 0.293 | 0.549 | 1.00 | 0.29 | 0.29 | -0.19 | -1.81 |
| xgb_pnl:all+wallets | 138 | 0.200 | 0.545 | 0.00 | 0.00 | 0.14 | -1.14 | -2.35 |
| xgb_pnl:botlive+context | 138 | 0.268 | 0.576 | 0.00 | 0.29 | 0.36 | 0.98 | -0.58 |
| logistic_repo_recipe | 138 | 0.377 | 0.694 | 0.00 | 0.43 | 0.43 | 1.54 | -0.07 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- dev_buy_sol: 7.78
- sol_last60: 5.922
- buyers_last60: 5.921
- decision_age_s: 5.281
- n_trades: 5.021
- first_trade_t: 4.981
- n_buyers: 4.968
- max_drawdown: 4.925
- n_slots: 4.912
- run_from_low: 4.85
- flipper_share: 4.691
- inflow_accel: 4.644
- bundle_slots: 4.613
- price_slope: 4.564
- buy_size_cv: 4.537

## xgb_holders: top gain features

- dev_sold: 11.909
- dev_share: 11.024
- top3_share: 6.693
- holders_n: 5.902
- top10_share: 5.465
- launch_bundle_share: 5.314
- top1_share: 5.297
- first_slot_share: 5.221
- tokens_out_pct: 5.206
- buyers_n: 5.049
- same_size_share: 4.797
- gini_hold: 4.438
- exited_share: 4.072

## xgb_shape+holders: top gain features

- dev_sold: 6.117
- dev_share: 4.854
- dev_buy_sol: 4.499
- decision_age_s: 4.453
- top3_share: 4.4
- launch_bundle_share: 4.369
- holders_n: 4.209
- lows: 4.099
- top1_share: 3.975
- sol_last60: 3.956
- first_trade_t: 3.948
- iti_median: 3.872
- last_trade_t: 3.818
- n_buyers: 3.677
- buyers_last60: 3.63

## xgb_all: top gain features

- creator_prior_resolved: 14.477
- is_native_launch: 12.969
- creator_prior_launches: 11.444
- replies_at_entry: 10.642
- buyers_last60: 10.403
- sol_last60: 8.802
- holders_n: 8.287
- decision_age_s: 7.848
- top10_share: 7.1
- top3_share: 6.583
- last_trade_t: 6.507
- buyers_n: 6.37
- top1_share: 6.351
- buy_ratio_count: 6.339
- market_recent_n: 6.262

## xgb_context: top gain features

- replies_at_entry: 28.17
- live_at_entry: 20.031
- is_native_launch: 8.522
- market_recent_n: 5.632
- has_twitter: 4.976
- name_dup_24h: 4.77
- dow_cos: 4.768
- market_candidate_rate: 4.512
- has_telegram: 4.26
- market_launch_rate: 3.974
- description_len: 3.876
- twitter_is_status: 3.637
- image_dup_24h: 3.458
- hour_cos: 3.432
- has_website: 3.26

## xgb_wallets: top gain features

- w_repeat_share: 4.204
- w_scored_share: 3.61
- w_hit_rate_max: 3.608
- w_serial_share: 3.543
- w_hit_rate_sol: 3.498
- w_hit_rate_mean: 3.37
- w_log_prior_mean: 3.287

## xgb_holders+wallets: top gain features

- dev_sold: 12.306
- dev_share: 11.74
- top3_share: 8.041
- top10_share: 6.758
- gini_hold: 6.582
- holders_n: 6.47
- w_repeat_share: 6.432
- launch_bundle_share: 6.186
- top1_share: 5.822
- exited_share: 5.749
- buyers_n: 5.618
- w_hit_rate_max: 5.616
- tokens_out_pct: 5.592
- first_slot_share: 5.493
- w_serial_share: 5.434

## xgb_all+wallets: top gain features

- is_native_launch: 12.628
- creator_prior_resolved: 12.154
- replies_at_entry: 9.449
- creator_prior_launches: 7.888
- buyers_last60: 7.373
- live_at_entry: 7.069
- holders_n: 7.056
- top10_share: 6.286
- sol_last60: 6.227
- inflow_accel: 5.992
- last_trade_t: 5.962
- has_telegram: 5.943
- launch_bundle_share: 5.642
- market_recent_n: 5.627
- top3_share: 5.607

## xgb_botlive: top gain features

- bl_dev_buy_sol: 13.17
- bl_top10_share: 4.673
- bl_first_seen_sol: 4.061
- bl_price_slope: 3.972
- bl_sol_last60: 3.8
- bl_decision_age_s: 3.782
- bl_sol_per_s_window: 3.483
- bl_inflow_accel: 3.106
- bl_log_ret_window: 2.511
- bl_run_from_low: 2.387
- bl_trades_last60: 2.147
- bl_curve_sol_in: 1.886
- bl_max_drawdown: 1.287
- bl_lows_per_min: 0.839

## xgb_botlive+context: top gain features

- replies_at_entry: 28.595
- live_at_entry: 19.504
- is_native_launch: 14.376
- bl_dev_buy_sol: 6.731
- market_recent_n: 6.665
- bl_sol_last60: 6.382
- bl_top10_share: 5.743
- bl_curve_sol_in: 5.667
- bl_decision_age_s: 5.663
- market_candidate_rate: 5.575
- dow_cos: 5.499
- bl_run_from_low: 5.377
- bl_price_slope: 5.31
- bl_first_seen_sol: 5.263
- bl_trades_last60: 5.253

## xgb_pnl:all+wallets: top gain features

- replies_at_entry: 3.953
- creator_prior_resolved: 3.898
- is_native_launch: 2.849
- creator_prior_launches: 2.078
- twitter_is_status: 2.065
- holders_n: 1.934
- live_at_entry: 1.738
- dev_buy_sol: 1.586
- top3_share: 1.553
- launch_bundle_share: 1.521
- n_slots: 1.492
- last_trade_t: 1.472
- top1_share: 1.432
- buy_size_cv: 1.419
- biggest_buy_vs_curve: 1.338

## xgb_pnl:botlive+context: top gain features

- replies_at_entry: 7.599
- live_at_entry: 6.113
- is_native_launch: 2.75
- bl_trades_last60: 1.675
- bl_dev_buy_sol: 1.386
- market_candidate_rate: 1.378
- has_twitter: 1.346
- market_recent_n: 1.303
- bl_decision_age_s: 1.297
- dow_sin: 1.281
- has_website: 1.274
- name_dup_24h: 1.216
- bl_first_seen_sol: 1.198
- bl_top10_share: 1.197
- bl_curve_sol_in: 1.174
