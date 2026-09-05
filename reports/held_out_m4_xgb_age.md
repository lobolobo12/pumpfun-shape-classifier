# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 316 | 0.129 | 0.790 | 0.00 | 0.06 | 0.09 | -3.58 | -5.16 |
| xgb_holders | 316 | 0.199 | 0.791 | 0.33 | 0.06 | 0.12 | -3.65 | -5.27 |
| xgb_shape+holders | 316 | 0.128 | 0.773 | 0.00 | 0.12 | 0.09 | -3.46 | -5.03 |
| xgb_all | 316 | 0.134 | 0.781 | 0.00 | 0.12 | 0.16 | -2.00 | -3.63 |
| xgb_context | 316 | 0.052 | 0.473 | 0.00 | 0.06 | 0.03 | -2.54 | -3.19 |
| xgb_wallets | 316 | 0.092 | 0.582 | 0.00 | 0.12 | 0.09 | -1.05 | -2.65 |
| xgb_holders+wallets | 316 | 0.201 | 0.790 | 0.00 | 0.25 | 0.25 | -0.65 | -2.31 |
| xgb_all+wallets | 316 | 0.184 | 0.789 | 0.00 | 0.25 | 0.16 | -2.44 | -4.07 |
| xgb_botlive | 316 | 0.153 | 0.836 | 0.00 | 0.12 | 0.12 | -3.52 | -5.10 |
| xgb_botlive+context | 316 | 0.154 | 0.822 | 0.33 | 0.12 | 0.16 | -2.76 | -4.39 |
| xgb_pnl:all+wallets | 316 | 0.112 | 0.645 | 0.33 | 0.12 | 0.06 | -3.82 | -4.87 |
| xgb_pnl:botlive+context | 316 | 0.116 | 0.603 | 0.33 | 0.12 | 0.12 | -2.78 | -4.39 |
| logistic_repo_recipe | 316 | 0.141 | 0.759 | 0.00 | 0.19 | 0.19 | -1.93 | -3.55 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- run_from_low: 91.845
- sol_per_s_window: 63.36
- curve_sol_in: 28.053
- max_drawdown: 15.148
- buyers_last60: 13.776
- lows_per_min: 12.688
- sell_share_sol: 11.697
- volume_slope: 9.543
- from_peak: 9.049
- iti_median: 8.433
- buy_ratio_sol: 8.354
- iti_cv: 8.143
- buy_ratio_count: 8.068
- time_to_10_trades: 7.93
- n_sellers: 7.803

## xgb_holders: top gain features

- tokens_out_pct: 42.94
- top10_share: 16.932
- launch_bundle_share: 16.853
- top3_share: 12.195
- first_slot_share: 11.347
- holders_n: 9.537
- exited_share: 8.691
- gini_hold: 8.34
- dev_sold: 6.678
- buyers_n: 6.602
- dev_share: 5.884
- same_size_share: 5.451
- top1_share: 5.252

## xgb_shape+holders: top gain features

- run_from_low: 142.636
- sol_per_s_window: 56.895
- curve_sol_in: 41.161
- buyers_last60: 20.501
- launch_bundle_share: 18.511
- holders_n: 13.769
- tokens_out_pct: 13.722
- buy_ratio_sol: 13.512
- first_slot_share: 12.759
- sell_share_sol: 12.67
- max_drawdown: 11.877
- volume_slope: 11.139
- dev_share: 10.74
- lows_per_min: 10.24
- n_buyers: 9.664

## xgb_all: top gain features

- run_from_low: 163.617
- sol_per_s_window: 58.076
- curve_sol_in: 38.209
- buyers_last60: 17.783
- launch_bundle_share: 17.665
- sell_share_sol: 17.413
- holders_n: 13.512
- max_drawdown: 12.599
- trades_last60: 12.507
- dev_share: 12.114
- lows_per_min: 11.496
- tokens_out_pct: 11.43
- dev_buy_sol: 11.302
- buy_ratio_count: 10.768
- is_native_launch: 10.526

## xgb_context: top gain features

- is_native_launch: 22.777
- replies_at_entry: 12.177
- has_twitter: 9.097
- market_recent_n: 7.779
- has_website: 7.778
- dow_cos: 7.069
- description_len: 6.416
- market_candidate_rate: 6.278
- market_launch_rate: 6.184
- image_dup_24h: 6.165
- live_at_entry: 5.617
- name_dup_24h: 5.484
- market_recent_tp_rate: 5.437
- hour_sin: 4.666
- hour_cos: 4.508

## xgb_wallets: top gain features

- w_hit_rate_mean: 10.996
- w_repeat_share: 10.536
- w_hit_rate_sol: 7.555
- w_hit_rate_max: 5.845
- w_scored_share: 5.635
- w_log_prior_mean: 5.451
- w_serial_share: 4.898

## xgb_holders+wallets: top gain features

- tokens_out_pct: 46.212
- top10_share: 34.321
- holders_n: 19.869
- launch_bundle_share: 19.81
- top3_share: 12.741
- first_slot_share: 9.346
- exited_share: 8.535
- gini_hold: 8.471
- w_hit_rate_sol: 8.231
- w_log_prior_mean: 8.181
- buyers_n: 7.807
- dev_share: 7.459
- top1_share: 6.725
- w_scored_share: 6.692
- dev_sold: 6.69

## xgb_all+wallets: top gain features

- run_from_low: 125.557
- sol_per_s_window: 50.205
- curve_sol_in: 45.795
- buyers_last60: 18.609
- launch_bundle_share: 13.043
- holders_n: 12.85
- max_drawdown: 12.224
- sell_share_sol: 11.202
- is_native_launch: 10.377
- dev_share: 10.288
- tokens_out_pct: 10.171
- lows_per_min: 9.813
- buy_ratio_sol: 9.632
- creator_prior_tp_rate: 9.461
- trades_last60: 9.394

## xgb_botlive: top gain features

- bl_run_from_low: 80.087
- bl_log_ret_window: 73.749
- bl_lows_per_min: 13.869
- bl_top10_share: 12.584
- bl_curve_sol_in: 11.132
- bl_max_drawdown: 10.837
- bl_sol_per_s_window: 9.855
- bl_dev_buy_sol: 8.678
- bl_from_peak: 7.884
- bl_lows: 7.698
- bl_price_slope: 7.028
- bl_inflow_accel: 6.777
- bl_sol_last60: 6.675
- bl_first_seen_sol: 5.308
- bl_trades_last60: 4.384

## xgb_botlive+context: top gain features

- bl_log_ret_window: 65.109
- bl_run_from_low: 57.488
- bl_lows_per_min: 16.269
- bl_top10_share: 13.147
- bl_sol_per_s_window: 12.916
- bl_max_drawdown: 11.211
- bl_lows: 10.262
- has_twitter: 9.273
- has_telegram: 8.927
- is_native_launch: 8.786
- market_recent_n: 8.752
- bl_dev_buy_sol: 8.661
- bl_curve_sol_in: 8.298
- replies_at_entry: 8.23
- bl_price_slope: 7.814

## xgb_pnl:all+wallets: top gain features

- dev_share: 7.306
- largest_buy_share: 6.427
- curve_sol_in: 2.912
- sell_share_sol: 2.78
- buy_ratio_sol: 2.417
- dev_buy_sol: 2.293
- iti_median: 2.236
- is_native_launch: 2.235
- gini_hold: 2.108
- max_drawdown: 2.007
- sol_per_s_window: 1.966
- buy_ratio_count: 1.865
- flipper_share: 1.707
- tokens_out_pct: 1.685
- volume_slope: 1.633

## xgb_pnl:botlive+context: top gain features

- bl_dev_buy_sol: 2.715
- bl_max_drawdown: 2.222
- bl_from_peak: 2.167
- is_native_launch: 1.409
- bl_top10_share: 1.214
- twitter_is_status: 1.135
- bl_sol_per_s_window: 1.126
- bl_run_from_low: 1.047
- image_dup_24h: 1.046
- has_telegram: 1.043
- description_len: 1.018
- has_twitter: 1.013
- bl_log_ret_window: 0.986
- bl_price_slope: 0.985
- bl_lows_per_min: 0.956
