# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 316 | 0.129 | 0.791 | 0.00 | 0.06 | 0.12 | -2.93 | -4.51 |
| xgb_holders | 316 | 0.198 | 0.780 | 0.33 | 0.06 | 0.16 | -3.05 | -4.67 |
| xgb_shape+holders | 316 | 0.153 | 0.781 | 0.33 | 0.12 | 0.12 | -2.87 | -4.45 |
| xgb_all | 316 | 0.140 | 0.781 | 0.00 | 0.12 | 0.16 | -2.20 | -3.82 |
| xgb_context | 316 | 0.049 | 0.459 | 0.00 | 0.06 | 0.03 | -2.72 | -3.24 |
| xgb_wallets | 316 | 0.085 | 0.588 | 0.00 | 0.12 | 0.09 | -1.28 | -2.88 |
| xgb_holders+wallets | 316 | 0.181 | 0.788 | 0.00 | 0.25 | 0.22 | -1.61 | -3.24 |
| xgb_all+wallets | 316 | 0.166 | 0.789 | 0.33 | 0.12 | 0.16 | -2.77 | -4.39 |
| xgb_botlive | 316 | 0.154 | 0.833 | 0.00 | 0.06 | 0.16 | -2.67 | -4.30 |
| xgb_botlive+context | 316 | 0.152 | 0.822 | 0.00 | 0.12 | 0.16 | -2.76 | -4.39 |
| xgb_pnl:all+wallets | 316 | 0.111 | 0.612 | 0.33 | 0.12 | 0.09 | -2.67 | -4.26 |
| xgb_pnl:botlive+context | 316 | 0.116 | 0.569 | 0.33 | 0.19 | 0.12 | -2.52 | -4.14 |
| logistic_repo_recipe | 316 | 0.124 | 0.755 | 0.00 | 0.12 | 0.12 | -3.18 | -4.75 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- run_from_low: 65.646
- sol_per_s_window: 49.092
- curve_sol_in: 39.545
- lows_per_min: 14.247
- max_drawdown: 13.783
- buyers_last60: 12.954
- sell_share_sol: 10.702
- buy_ratio_count: 8.224
- n_buyers: 8.202
- dev_buy_sol: 7.586
- n_sellers: 7.429
- biggest_buy_vs_curve: 7.375
- volume_slope: 7.236
- from_peak: 7.204
- gini_buy_size: 7.097

## xgb_holders: top gain features

- tokens_out_pct: 24.386
- top10_share: 9.012
- launch_bundle_share: 8.828
- top3_share: 7.953
- first_slot_share: 6.356
- holders_n: 6.338
- dev_sold: 5.553
- exited_share: 5.476
- buyers_n: 5.467
- gini_hold: 5.438
- dev_share: 5.096
- same_size_share: 4.924
- top1_share: 4.847

## xgb_shape+holders: top gain features

- run_from_low: 103.899
- curve_sol_in: 44.367
- sol_per_s_window: 39.547
- buyers_last60: 13.251
- lows_per_min: 12.103
- launch_bundle_share: 11.723
- tokens_out_pct: 11.493
- dev_share: 11.447
- sell_share_sol: 10.828
- volume_slope: 8.774
- trades_last60: 8.457
- lows: 8.423
- buyers_n: 8.329
- holders_n: 8.155
- buy_ratio_count: 8.154

## xgb_all: top gain features

- run_from_low: 214.256
- curve_sol_in: 67.787
- sol_per_s_window: 65.224
- buyers_last60: 27.186
- launch_bundle_share: 26.021
- holders_n: 17.246
- sell_share_sol: 16.836
- dev_share: 16.555
- max_drawdown: 15.771
- trades_last60: 15.766
- lows_per_min: 15.555
- volume_slope: 13.868
- tokens_out_pct: 13.501
- is_native_launch: 12.548
- buy_ratio_count: 12.119

## xgb_context: top gain features

- is_native_launch: 20.472
- has_twitter: 8.839
- has_website: 8.712
- market_recent_n: 7.142
- market_candidate_rate: 6.13
- description_len: 6.02
- dow_sin: 5.999
- dow_cos: 5.922
- market_recent_tp_rate: 5.558
- name_dup_24h: 5.481
- replies_at_entry: 5.481
- market_launch_rate: 5.446
- hour_sin: 5.288
- image_dup_24h: 5.163
- twitter_is_status: 5.119

## xgb_wallets: top gain features

- w_hit_rate_mean: 12.756
- w_repeat_share: 12.112
- w_hit_rate_sol: 9.445
- w_hit_rate_max: 6.183
- w_scored_share: 6.006
- w_log_prior_mean: 5.787
- w_serial_share: 5.626

## xgb_holders+wallets: top gain features

- top10_share: 55.186
- tokens_out_pct: 49.44
- launch_bundle_share: 21.441
- holders_n: 19.375
- top3_share: 11.179
- gini_hold: 9.332
- exited_share: 9.251
- first_slot_share: 9.061
- w_log_prior_mean: 9.054
- buyers_n: 8.261
- w_hit_rate_sol: 7.349
- dev_share: 7.273
- w_scored_share: 7.049
- w_serial_share: 6.97
- w_repeat_share: 6.597

## xgb_all+wallets: top gain features

- run_from_low: 157.752
- curve_sol_in: 75.558
- sol_per_s_window: 47.01
- launch_bundle_share: 18.889
- buyers_last60: 18.253
- buyers_n: 17.888
- dev_share: 14.275
- max_drawdown: 14.094
- lows_per_min: 14.024
- tokens_out_pct: 13.201
- sell_share_sol: 12.711
- dev_buy_sol: 12.08
- iti_median: 11.89
- holders_n: 11.73
- from_peak: 11.67

## xgb_botlive: top gain features

- bl_log_ret_window: 56.599
- bl_run_from_low: 46.605
- bl_lows_per_min: 10.432
- bl_top10_share: 9.465
- bl_curve_sol_in: 9.255
- bl_sol_per_s_window: 8.683
- bl_max_drawdown: 8.253
- bl_lows: 7.74
- bl_dev_buy_sol: 6.916
- bl_from_peak: 5.83
- bl_price_slope: 5.542
- bl_sol_last60: 5.417
- bl_inflow_accel: 5.058
- bl_first_seen_sol: 4.859
- bl_trades_last60: 3.814

## xgb_botlive+context: top gain features

- bl_log_ret_window: 64.748
- bl_run_from_low: 59.137
- bl_sol_per_s_window: 11.974
- bl_top10_share: 11.591
- bl_curve_sol_in: 11.053
- bl_lows: 10.493
- has_twitter: 9.899
- bl_max_drawdown: 9.346
- bl_from_peak: 7.967
- is_native_launch: 7.756
- market_recent_n: 7.58
- market_candidate_rate: 7.394
- description_len: 7.366
- bl_dev_buy_sol: 7.257
- has_telegram: 7.017

## xgb_pnl:all+wallets: top gain features

- dev_share: 7.947
- largest_buy_share: 4.89
- buy_ratio_sol: 3.04
- curve_sol_in: 2.54
- dev_buy_sol: 2.295
- sell_share_sol: 2.293
- is_native_launch: 2.178
- gini_hold: 2.149
- buy_ratio_count: 1.998
- log_ret_window: 1.92
- exited_share: 1.845
- buy_size_cv: 1.826
- volume_slope: 1.685
- tokens_out_pct: 1.671
- gini_buy_size: 1.62

## xgb_pnl:botlive+context: top gain features

- bl_dev_buy_sol: 3.058
- bl_max_drawdown: 2.638
- bl_from_peak: 2.412
- twitter_is_status: 1.731
- is_native_launch: 1.677
- bl_top10_share: 1.303
- bl_log_ret_window: 1.232
- bl_run_from_low: 1.199
- description_len: 1.127
- live_at_entry: 1.081
- has_twitter: 1.057
- bl_sol_per_s_window: 1.057
- replies_at_entry: 1.044
- bl_curve_sol_in: 1.018
- has_telegram: 1.015
