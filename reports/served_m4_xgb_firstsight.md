# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 138 | 0.219 | 0.565 | 0.00 | 0.14 | 0.21 | -0.87 | -2.43 |
| xgb_holders | 138 | 0.305 | 0.607 | 1.00 | 0.43 | 0.36 | 0.43 | -1.19 |
| xgb_shape+holders | 138 | 0.253 | 0.543 | 1.00 | 0.29 | 0.21 | -0.89 | -2.45 |
| xgb_all | 138 | 0.200 | 0.556 | 0.00 | 0.00 | 0.00 | -3.08 | -2.65 |
| xgb_context | 138 | 0.272 | 0.535 | 1.00 | 0.43 | 0.29 | 0.58 | -1.01 |
| xgb_wallets | 138 | 0.263 | 0.496 | 1.00 | 0.43 | 0.36 | 0.66 | -0.94 |
| xgb_holders+wallets | 138 | 0.293 | 0.624 | 0.00 | 0.29 | 0.36 | 0.39 | -1.20 |
| xgb_all+wallets | 138 | 0.204 | 0.549 | 0.00 | 0.00 | 0.14 | -1.64 | -2.64 |
| xgb_botlive | 138 | 0.326 | 0.570 | 1.00 | 0.43 | 0.36 | 0.64 | -0.94 |
| xgb_botlive+context | 138 | 0.291 | 0.552 | 1.00 | 0.29 | 0.14 | -1.66 | -2.55 |
| xgb_pnl:all+wallets | 138 | 0.202 | 0.548 | 0.00 | 0.00 | 0.21 | -0.61 | -2.17 |
| xgb_pnl:botlive+context | 138 | 0.257 | 0.568 | 0.00 | 0.14 | 0.36 | 1.11 | -0.47 |
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

- creator_prior_resolved: 18.476
- replies_at_entry: 15.05
- is_native_launch: 14.107
- creator_prior_launches: 13.681
- buyers_last60: 12.107
- sol_last60: 9.171
- holders_n: 8.862
- top10_share: 8.056
- decision_age_s: 7.851
- sol_per_s_window: 7.752
- last_trade_t: 7.518
- twitter_is_status: 7.379
- top3_share: 7.362
- largest_buy_share: 7.12
- launch_bundle_share: 6.924

## xgb_context: top gain features

- replies_at_entry: 28.17
- live_at_entry: 20.032
- is_native_launch: 8.522
- market_recent_n: 5.631
- has_twitter: 4.976
- dow_cos: 4.773
- name_dup_24h: 4.768
- market_candidate_rate: 4.517
- has_telegram: 4.267
- market_launch_rate: 3.971
- description_len: 3.872
- twitter_is_status: 3.632
- image_dup_24h: 3.461
- hour_cos: 3.429
- has_website: 3.261

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

- creator_prior_resolved: 13.013
- is_native_launch: 12.624
- replies_at_entry: 9.45
- creator_prior_launches: 7.906
- holders_n: 7.872
- live_at_entry: 7.63
- buyers_last60: 7.292
- first_trade_t: 6.444
- sol_last60: 6.426
- top10_share: 6.419
- last_trade_t: 6.139
- inflow_accel: 6.072
- has_telegram: 5.943
- sol_per_s_window: 5.861
- top1_share: 5.845

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

- replies_at_entry: 30.225
- live_at_entry: 22.457
- is_native_launch: 14.576
- market_recent_n: 6.71
- bl_dev_buy_sol: 6.558
- bl_sol_last60: 6.421
- bl_top10_share: 5.767
- bl_curve_sol_in: 5.714
- bl_decision_age_s: 5.714
- market_candidate_rate: 5.536
- has_website: 5.495
- dow_cos: 5.468
- bl_price_slope: 5.465
- bl_trades_last60: 5.218
- bl_first_seen_sol: 5.162

## xgb_pnl:all+wallets: top gain features

- replies_at_entry: 4.859
- creator_prior_resolved: 4.036
- is_native_launch: 2.577
- creator_prior_launches: 2.125
- twitter_is_status: 2.066
- holders_n: 1.96
- live_at_entry: 1.606
- dev_buy_sol: 1.597
- launch_bundle_share: 1.555
- top3_share: 1.547
- last_trade_t: 1.513
- top1_share: 1.475
- buy_size_cv: 1.437
- dev_share: 1.435
- biggest_buy_vs_curve: 1.404

## xgb_pnl:botlive+context: top gain features

- replies_at_entry: 7.573
- live_at_entry: 4.596
- is_native_launch: 2.764
- bl_dev_buy_sol: 1.389
- has_twitter: 1.373
- market_candidate_rate: 1.351
- bl_decision_age_s: 1.299
- market_recent_n: 1.277
- dow_sin: 1.252
- bl_trades_last60: 1.227
- name_dup_24h: 1.219
- has_website: 1.198
- bl_curve_sol_in: 1.181
- bl_top10_share: 1.175
- bl_first_seen_sol: 1.161
