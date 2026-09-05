# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 316 | 0.138 | 0.799 | 0.00 | 0.12 | 0.09 | -3.59 | -5.15 |
| xgb_holders | 316 | 0.228 | 0.799 | 0.33 | 0.25 | 0.16 | -3.03 | -4.65 |
| xgb_shape+holders | 316 | 0.142 | 0.796 | 0.00 | 0.12 | 0.16 | -2.21 | -3.80 |
| xgb_all | 316 | 0.139 | 0.789 | 0.00 | 0.19 | 0.16 | -2.07 | -3.70 |
| xgb_context | 316 | 0.052 | 0.479 | 0.00 | 0.06 | 0.03 | -2.84 | -3.51 |
| xgb_wallets | 316 | 0.092 | 0.582 | 0.00 | 0.12 | 0.09 | -1.05 | -2.65 |
| xgb_holders+wallets | 316 | 0.192 | 0.801 | 0.00 | 0.25 | 0.25 | -0.94 | -2.56 |
| xgb_all+wallets | 316 | 0.157 | 0.790 | 0.00 | 0.25 | 0.16 | -2.09 | -3.72 |
| xgb_botlive | 316 | 0.151 | 0.832 | 0.00 | 0.06 | 0.16 | -2.16 | -3.74 |
| xgb_botlive+context | 316 | 0.182 | 0.830 | 0.33 | 0.19 | 0.16 | -2.94 | -4.57 |
| xgb_pnl:all+wallets | 316 | 0.103 | 0.587 | 0.33 | 0.12 | 0.09 | -2.98 | -4.57 |
| xgb_pnl:botlive+context | 316 | 0.120 | 0.628 | 0.33 | 0.12 | 0.16 | -1.70 | -3.32 |
| logistic_repo_recipe | 316 | 0.128 | 0.750 | 0.00 | 0.12 | 0.16 | -2.68 | -4.25 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- run_from_low: 104.301
- sol_per_s_window: 55.863
- curve_sol_in: 36.85
- max_drawdown: 15.711
- lows_per_min: 14.886
- buyers_last60: 14.396
- sell_share_sol: 11.624
- from_peak: 9.304
- volume_slope: 9.126
- time_to_10_trades: 8.993
- buy_ratio_count: 8.902
- dev_buy_sol: 8.561
- n_buyers: 8.557
- buy_ratio_sol: 8.534
- n_sellers: 8.385

## xgb_holders: top gain features

- tokens_out_pct: 41.624
- top10_share: 17.384
- launch_bundle_share: 16.155
- top3_share: 11.712
- first_slot_share: 10.007
- holders_n: 9.837
- exited_share: 8.784
- dev_share: 7.771
- gini_hold: 7.749
- dev_sold: 7.369
- buyers_n: 6.985
- top1_share: 5.398
- same_size_share: 4.819

## xgb_shape+holders: top gain features

- run_from_low: 150.58
- sol_per_s_window: 57.44
- curve_sol_in: 40.343
- buyers_last60: 22.498
- launch_bundle_share: 18.201
- tokens_out_pct: 13.456
- dev_share: 12.705
- lows_per_min: 12.621
- sell_share_sol: 12.116
- holders_n: 11.731
- max_drawdown: 11.1
- dev_sold: 10.629
- volume_slope: 10.577
- buy_ratio_count: 10.074
- n_buyers: 9.642

## xgb_all: top gain features

- run_from_low: 227.619
- sol_per_s_window: 63.456
- curve_sol_in: 44.334
- launch_bundle_share: 23.328
- buyers_last60: 19.777
- dev_share: 17.583
- holders_n: 16.036
- sell_share_sol: 15.089
- max_drawdown: 14.862
- lows_per_min: 13.749
- buy_ratio_sol: 13.681
- first_slot_share: 13.675
- has_twitter: 13.211
- volume_slope: 12.7
- image_dup_24h: 12.475

## xgb_context: top gain features

- is_native_launch: 23.176
- replies_at_entry: 12.191
- has_twitter: 8.966
- market_recent_n: 7.589
- has_website: 7.45
- dow_cos: 7.05
- market_candidate_rate: 6.266
- description_len: 6.246
- image_dup_24h: 6.172
- market_launch_rate: 5.967
- name_dup_24h: 5.446
- market_recent_tp_rate: 5.222
- live_at_entry: 5.18
- hour_sin: 4.782
- hour_cos: 4.519

## xgb_wallets: top gain features

- w_hit_rate_mean: 10.996
- w_repeat_share: 10.536
- w_hit_rate_sol: 7.555
- w_hit_rate_max: 5.845
- w_scored_share: 5.635
- w_log_prior_mean: 5.451
- w_serial_share: 4.898

## xgb_holders+wallets: top gain features

- tokens_out_pct: 46.796
- top10_share: 35.539
- launch_bundle_share: 21.101
- holders_n: 20.14
- top3_share: 13.72
- dev_sold: 9.424
- first_slot_share: 9.315
- exited_share: 9.082
- dev_share: 8.793
- w_log_prior_mean: 8.439
- gini_hold: 8.35
- buyers_n: 8.182
- w_hit_rate_sol: 7.799
- w_scored_share: 7.11
- w_repeat_share: 6.772

## xgb_all+wallets: top gain features

- run_from_low: 163.901
- sol_per_s_window: 63.936
- curve_sol_in: 48.571
- launch_bundle_share: 26.212
- buyers_last60: 21.726
- holders_n: 15.857
- max_drawdown: 15.586
- replies_at_entry: 14.951
- trades_last60: 13.918
- dev_share: 13.003
- lows_per_min: 12.969
- first_slot_share: 12.561
- is_native_launch: 12.083
- tokens_out_pct: 12.011
- buy_ratio_sol: 11.859

## xgb_botlive: top gain features

- bl_log_ret_window: 53.57
- bl_run_from_low: 47.234
- bl_lows_per_min: 10.124
- bl_curve_sol_in: 9.601
- bl_top10_share: 9.37
- bl_max_drawdown: 8.825
- bl_dev_buy_sol: 8.695
- bl_sol_per_s_window: 8.062
- bl_lows: 7.206
- bl_inflow_accel: 5.737
- bl_sol_last60: 5.705
- bl_price_slope: 5.625
- bl_from_peak: 5.049
- bl_first_seen_sol: 5.048
- bl_trades_last60: 3.771

## xgb_botlive+context: top gain features

- bl_log_ret_window: 68.65
- bl_run_from_low: 56.272
- has_telegram: 18.643
- bl_top10_share: 13.432
- bl_sol_per_s_window: 12.591
- bl_max_drawdown: 10.877
- market_recent_n: 10.389
- bl_lows_per_min: 10.244
- bl_dev_buy_sol: 9.741
- bl_lows: 8.956
- has_twitter: 8.635
- bl_curve_sol_in: 8.408
- bl_from_peak: 7.757
- hour_sin: 7.633
- market_candidate_rate: 7.571

## xgb_pnl:all+wallets: top gain features

- largest_buy_share: 6.444
- dev_share: 5.778
- buy_ratio_sol: 2.544
- sell_share_sol: 2.465
- iti_median: 2.441
- curve_sol_in: 2.356
- dev_buy_sol: 2.339
- gini_hold: 2.262
- max_drawdown: 2.167
- is_native_launch: 2.036
- sol_per_s_window: 2.019
- flipper_share: 1.943
- buy_ratio_count: 1.849
- exited_share: 1.805
- volume_slope: 1.76

## xgb_pnl:botlive+context: top gain features

- bl_dev_buy_sol: 2.742
- bl_max_drawdown: 2.335
- bl_from_peak: 2.133
- twitter_is_status: 1.284
- has_twitter: 1.158
- replies_at_entry: 1.135
- bl_lows_per_min: 1.125
- bl_top10_share: 1.107
- bl_log_ret_window: 1.062
- bl_curve_sol_in: 1.057
- bl_sol_per_s_window: 1.055
- is_native_launch: 1.054
- bl_run_from_low: 1.041
- description_len: 0.996
- bl_price_slope: 0.945
