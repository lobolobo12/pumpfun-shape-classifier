# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 138 | 0.197 | 0.516 | 0.00 | 0.14 | 0.21 | -1.02 | -2.57 |
| xgb_holders | 138 | 0.260 | 0.568 | 0.00 | 0.43 | 0.29 | -0.35 | -1.96 |
| xgb_shape+holders | 138 | 0.194 | 0.516 | 0.00 | 0.14 | 0.14 | -1.47 | -2.49 |
| xgb_all | 138 | 0.203 | 0.561 | 0.00 | 0.00 | 0.07 | -2.37 | -2.65 |
| xgb_context | 138 | 0.202 | 0.512 | 0.00 | 0.14 | 0.21 | -0.07 | -1.67 |
| xgb_wallets | 138 | 0.231 | 0.509 | 0.00 | 0.29 | 0.36 | 0.68 | -0.92 |
| xgb_holders+wallets | 138 | 0.244 | 0.552 | 0.00 | 0.14 | 0.21 | -1.07 | -2.61 |
| xgb_all+wallets | 138 | 0.206 | 0.557 | 0.00 | 0.00 | 0.14 | -1.64 | -2.63 |
| xgb_botlive | 138 | 0.272 | 0.558 | 0.00 | 0.43 | 0.36 | 0.39 | -1.20 |
| xgb_botlive+context | 138 | 0.250 | 0.532 | 0.00 | 0.29 | 0.29 | -0.15 | -1.78 |
| xgb_pnl:all+wallets | 138 | 0.206 | 0.546 | 0.00 | 0.14 | 0.21 | -0.81 | -2.35 |
| xgb_pnl:botlive+context | 138 | 0.287 | 0.589 | 0.00 | 0.29 | 0.43 | 1.74 | 0.16 |
| logistic_repo_recipe | 138 | 0.227 | 0.601 | 0.00 | 0.00 | 0.21 | -0.42 | -2.00 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- bundle_slots: 8.192
- buyers_last60: 6.778
- sol_last60: 6.59
- n_trades: 5.994
- iti_median: 5.817
- trades_last60: 5.681
- decision_age_s: 5.562
- n_slots: 5.463
- iti_cv: 5.416
- max_drawdown: 5.297
- last_trade_t: 5.295
- price_slope: 5.261
- inflow_accel: 5.213
- flipper_share: 5.115
- sell_share_sol: 5.048

## xgb_holders: top gain features

- holders_n: 6.109
- launch_bundle_share: 5.655
- dev_share: 5.382
- top10_share: 4.925
- first_slot_share: 4.858
- dev_sold: 4.528
- top3_share: 4.391
- gini_hold: 4.391
- same_size_share: 4.381
- top1_share: 4.269
- tokens_out_pct: 4.183
- exited_share: 3.773
- buyers_n: 3.525

## xgb_shape+holders: top gain features

- holders_n: 8.739
- bundle_slots: 7.663
- top10_share: 7.185
- iti_median: 7.027
- sol_last60: 6.932
- launch_bundle_share: 6.74
- last_trade_t: 6.625
- decision_age_s: 6.148
- n_trades: 6.091
- top3_share: 6.055
- buyers_last60: 6.05
- top1_share: 6.037
- iti_cv: 5.972
- sellers_last60: 5.948
- first_slot_share: 5.916

## xgb_all: top gain features

- creator_prior_resolved: 26.602
- is_native_launch: 15.05
- creator_prior_launches: 13.09
- replies_at_entry: 11.92
- buyers_last60: 11.885
- holders_n: 11.634
- sol_last60: 10.258
- top10_share: 9.051
- iti_median: 8.973
- launch_bundle_share: 8.528
- dev_share: 8.483
- first_slot_share: 8.412
- has_telegram: 8.283
- has_twitter: 8.234
- twitter_is_status: 8.124

## xgb_context: top gain features

- replies_at_entry: 31.52
- live_at_entry: 19.816
- is_native_launch: 10.687
- market_recent_n: 6.554
- has_telegram: 5.787
- market_candidate_rate: 5.278
- dow_cos: 5.184
- name_dup_24h: 5.079
- has_twitter: 4.952
- description_len: 4.696
- image_dup_24h: 4.257
- has_website: 4.212
- market_recent_tp_rate: 3.979
- hour_cos: 3.941
- market_launch_rate: 3.85

## xgb_wallets: top gain features

- w_repeat_share: 5.102
- w_hit_rate_sol: 4.483
- w_scored_share: 4.23
- w_hit_rate_max: 4.065
- w_hit_rate_mean: 4.031
- w_serial_share: 3.813
- w_log_prior_mean: 3.623

## xgb_holders+wallets: top gain features

- holders_n: 7.094
- top10_share: 6.424
- launch_bundle_share: 5.785
- dev_share: 5.451
- first_slot_share: 5.284
- w_repeat_share: 5.283
- tokens_out_pct: 5.061
- w_hit_rate_mean: 4.969
- w_hit_rate_sol: 4.932
- exited_share: 4.917
- w_log_prior_mean: 4.856
- w_serial_share: 4.84
- same_size_share: 4.833
- top1_share: 4.754
- w_scored_share: 4.747

## xgb_all+wallets: top gain features

- creator_prior_resolved: 22.532
- is_native_launch: 14.224
- replies_at_entry: 12.791
- holders_n: 11.752
- sol_last60: 9.027
- buyers_last60: 8.398
- launch_bundle_share: 7.83
- flipper_share: 7.617
- has_telegram: 7.598
- sol_per_s_window: 7.55
- top1_share: 7.474
- top10_share: 7.309
- top3_share: 7.242
- dow_cos: 7.162
- iti_median: 7.108

## xgb_botlive: top gain features

- bl_top10_share: 6.065
- bl_first_seen_sol: 4.644
- bl_price_slope: 4.585
- bl_sol_last60: 4.542
- bl_decision_age_s: 4.45
- bl_dev_buy_sol: 4.416
- bl_sol_per_s_window: 4.249
- bl_curve_sol_in: 4.059
- bl_log_ret_window: 3.751
- bl_inflow_accel: 3.656
- bl_run_from_low: 3.604
- bl_trades_last60: 3.473
- bl_lows: 2.24
- bl_max_drawdown: 2.238
- bl_lows_per_min: 1.631

## xgb_botlive+context: top gain features

- replies_at_entry: 25.93
- live_at_entry: 16.403
- is_native_launch: 13.09
- bl_curve_sol_in: 7.344
- market_recent_n: 7.08
- bl_sol_last60: 6.943
- bl_decision_age_s: 6.512
- bl_top10_share: 6.385
- market_candidate_rate: 6.381
- has_website: 6.237
- has_twitter: 6.209
- image_dup_24h: 6.14
- name_dup_24h: 6.076
- bl_sol_per_s_window: 5.783
- description_len: 5.674

## xgb_pnl:all+wallets: top gain features

- creator_prior_resolved: 5.537
- replies_at_entry: 4.365
- is_native_launch: 3.287
- holders_n: 2.388
- launch_bundle_share: 2.012
- creator_prior_launches: 1.955
- top3_share: 1.922
- dev_buy_sol: 1.722
- iti_median: 1.679
- price_slope: 1.662
- top1_share: 1.655
- has_twitter: 1.626
- last_trade_t: 1.619
- n_slots: 1.599
- w_hit_rate_max: 1.512

## xgb_pnl:botlive+context: top gain features

- replies_at_entry: 5.945
- live_at_entry: 3.487
- is_native_launch: 2.898
- bl_dev_buy_sol: 1.405
- market_recent_n: 1.365
- bl_trades_last60: 1.301
- bl_decision_age_s: 1.272
- bl_top10_share: 1.256
- market_candidate_rate: 1.252
- name_dup_24h: 1.24
- has_twitter: 1.229
- bl_sol_per_s_window: 1.203
- has_telegram: 1.167
- bl_run_from_low: 1.167
- bl_curve_sol_in: 1.161
