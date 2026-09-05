# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 138 | 0.198 | 0.531 | 0.00 | 0.00 | 0.21 | -1.03 | -2.58 |
| xgb_holders | 138 | 0.229 | 0.531 | 0.00 | 0.14 | 0.29 | -0.15 | -1.76 |
| xgb_shape+holders | 138 | 0.207 | 0.513 | 0.00 | 0.14 | 0.21 | -0.88 | -2.43 |
| xgb_all | 138 | 0.199 | 0.558 | 0.00 | 0.00 | 0.07 | -2.36 | -2.65 |
| xgb_context | 138 | 0.272 | 0.535 | 1.00 | 0.43 | 0.29 | 0.58 | -1.01 |
| xgb_wallets | 138 | 0.263 | 0.496 | 1.00 | 0.43 | 0.36 | 0.66 | -0.94 |
| xgb_holders+wallets | 138 | 0.232 | 0.544 | 0.00 | 0.14 | 0.29 | -0.36 | -1.97 |
| xgb_all+wallets | 138 | 0.203 | 0.555 | 0.00 | 0.00 | 0.14 | -1.64 | -2.64 |
| xgb_botlive | 138 | 0.262 | 0.555 | 0.00 | 0.43 | 0.21 | -0.95 | -2.52 |
| xgb_botlive+context | 138 | 0.265 | 0.525 | 1.00 | 0.29 | 0.29 | 0.02 | -1.61 |
| xgb_pnl:all+wallets | 138 | 0.191 | 0.525 | 0.00 | 0.00 | 0.14 | -1.16 | -2.35 |
| xgb_pnl:botlive+context | 138 | 0.274 | 0.582 | 0.00 | 0.29 | 0.50 | 2.59 | 1.01 |
| logistic_repo_recipe | 138 | 0.245 | 0.594 | 0.00 | 0.29 | 0.29 | 0.26 | -1.35 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- bundle_slots: 6.479
- buyers_last60: 5.925
- sol_last60: 5.554
- n_trades: 5.158
- decision_age_s: 5.136
- n_slots: 5.093
- max_drawdown: 4.669
- iti_cv: 4.636
- sellers_last60: 4.523
- price_slope: 4.487
- sell_share_sol: 4.399
- trades_last60: 4.332
- buy_ratio_count: 4.33
- lows_per_min: 4.24
- buy_ratio_sol: 4.221

## xgb_holders: top gain features

- holders_n: 5.041
- top10_share: 4.724
- launch_bundle_share: 4.55
- first_slot_share: 4.238
- dev_share: 4.025
- gini_hold: 3.934
- top3_share: 3.919
- top1_share: 3.847
- tokens_out_pct: 3.744
- same_size_share: 3.629
- exited_share: 3.481
- buyers_n: 3.159
- dev_sold: 2.72

## xgb_shape+holders: top gain features

- bundle_slots: 10.709
- holders_n: 10.561
- iti_median: 9.191
- buyers_last60: 8.584
- sol_last60: 8.266
- sol_per_s_window: 8.029
- max_drawdown: 7.926
- launch_bundle_share: 7.625
- top10_share: 7.194
- top3_share: 6.995
- same_size_share: 6.899
- buy_size_cv: 6.891
- inflow_accel: 6.688
- buy_ratio_sol: 6.608
- trades_last60: 6.601

## xgb_all: top gain features

- creator_prior_resolved: 13.451
- is_native_launch: 12.345
- buyers_last60: 9.848
- creator_prior_launches: 9.288
- replies_at_entry: 9.144
- decision_age_s: 7.827
- sol_last60: 7.6
- holders_n: 7.1
- top10_share: 6.961
- launch_bundle_share: 6.46
- last_trade_t: 6.324
- top1_share: 5.984
- top3_share: 5.976
- buy_ratio_count: 5.824
- inflow_accel: 5.781

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

- holders_n: 7.572
- w_repeat_share: 6.637
- top10_share: 6.223
- dev_share: 5.89
- launch_bundle_share: 5.84
- w_serial_share: 5.832
- first_slot_share: 5.831
- top1_share: 5.573
- w_hit_rate_max: 5.439
- w_hit_rate_mean: 5.227
- exited_share: 5.166
- same_size_share: 5.158
- gini_hold: 5.085
- top3_share: 4.865
- w_scored_share: 4.825

## xgb_all+wallets: top gain features

- creator_prior_resolved: 12.117
- is_native_launch: 11.557
- creator_prior_launches: 7.847
- holders_n: 7.625
- buyers_last60: 7.02
- sol_last60: 6.896
- replies_at_entry: 6.816
- live_at_entry: 6.739
- top10_share: 6.224
- inflow_accel: 6.15
- top1_share: 5.872
- last_trade_t: 5.829
- top3_share: 5.727
- launch_bundle_share: 5.685
- has_telegram: 5.676

## xgb_botlive: top gain features

- bl_trades_last60: 4.923
- bl_top10_share: 4.9
- bl_sol_last60: 4.357
- bl_decision_age_s: 4.352
- bl_price_slope: 4.282
- bl_dev_buy_sol: 4.03
- bl_first_seen_sol: 3.843
- bl_sol_per_s_window: 3.67
- bl_inflow_accel: 3.226
- bl_run_from_low: 3.224
- bl_log_ret_window: 3.026
- bl_curve_sol_in: 2.997
- bl_max_drawdown: 2.725
- bl_lows_per_min: 2.412

## xgb_botlive+context: top gain features

- replies_at_entry: 28.478
- live_at_entry: 26.0
- is_native_launch: 13.944
- market_recent_n: 6.959
- twitter_is_status: 6.667
- bl_sol_last60: 6.446
- market_candidate_rate: 6.091
- has_website: 5.91
- bl_decision_age_s: 5.855
- bl_top10_share: 5.854
- bl_log_ret_window: 5.608
- bl_curve_sol_in: 5.435
- bl_first_seen_sol: 5.408
- name_dup_24h: 5.333
- dow_cos: 5.268

## xgb_pnl:all+wallets: top gain features

- creator_prior_resolved: 4.599
- replies_at_entry: 2.982
- is_native_launch: 2.318
- iti_median: 2.134
- creator_prior_launches: 2.066
- n_slots: 1.858
- holders_n: 1.782
- live_at_entry: 1.699
- top3_share: 1.641
- has_twitter: 1.575
- launch_bundle_share: 1.542
- dev_buy_sol: 1.485
- top1_share: 1.445
- last_trade_t: 1.416
- market_candidate_rate: 1.41

## xgb_pnl:botlive+context: top gain features

- replies_at_entry: 7.502
- live_at_entry: 7.412
- is_native_launch: 2.757
- has_telegram: 1.355
- bl_dev_buy_sol: 1.316
- market_candidate_rate: 1.307
- market_recent_n: 1.275
- bl_decision_age_s: 1.247
- has_twitter: 1.243
- bl_top10_share: 1.241
- bl_trades_last60: 1.222
- bl_first_seen_sol: 1.169
- market_launch_rate: 1.154
- bl_curve_sol_in: 1.154
- dow_cos: 1.142
