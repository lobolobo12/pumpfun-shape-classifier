# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 1472 | 0.248 | 0.829 | 0.40 | 0.31 | 0.25 | -0.99 | -2.69 |
| xgb_holders | 1472 | 0.240 | 0.807 | 0.47 | 0.27 | 0.22 | -5.41 | -7.11 |
| xgb_shape+holders | 1472 | 0.256 | 0.822 | 0.40 | 0.32 | 0.22 | -4.41 | -6.11 |
| xgb_all | 1472 | 0.255 | 0.825 | 0.53 | 0.28 | 0.23 | -3.69 | -5.40 |
| xgb_context | 1472 | 0.105 | 0.557 | 0.20 | 0.12 | 0.09 | -8.43 | -10.08 |
| xgb_wallets | 1472 | 0.174 | 0.684 | 0.33 | 0.20 | 0.16 | -2.56 | -4.31 |
| xgb_holders+wallets | 1472 | 0.243 | 0.810 | 0.47 | 0.27 | 0.26 | -1.29 | -2.99 |
| xgb_all+wallets | 1472 | 0.250 | 0.829 | 0.33 | 0.32 | 0.25 | -2.33 | -4.04 |
| xgb_botlive | 1472 | 0.268 | 0.840 | 0.40 | 0.36 | 0.24 | -1.37 | -3.12 |
| xgb_botlive+context | 1472 | 0.246 | 0.834 | 0.40 | 0.32 | 0.25 | -2.10 | -3.85 |
| xgb_pnl:all+wallets | 1472 | 0.203 | 0.659 | 0.53 | 0.28 | 0.24 | -1.80 | -3.50 |
| xgb_pnl:botlive+context | 1472 | 0.176 | 0.611 | 0.40 | 0.27 | 0.22 | -1.53 | -3.27 |
| logistic_repo_recipe | 1472 | 0.191 | 0.792 | 0.20 | 0.19 | 0.22 | -4.23 | -6.12 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- run_from_low: 89.33
- sol_per_s_window: 74.382
- curve_sol_in: 54.233
- max_drawdown: 17.609
- iti_median: 15.185
- lows_per_min: 15.091
- buyers_last60: 14.989
- from_peak: 14.598
- buy_ratio_count: 14.513
- log_ret_window: 13.298
- n_buyers: 11.688
- dev_buy_sol: 11.208
- n_sellers: 9.77
- sol_last60: 9.735
- volume_slope: 9.044

## xgb_holders: top gain features

- tokens_out_pct: 31.48
- top10_share: 11.88
- holders_n: 11.644
- launch_bundle_share: 11.553
- dev_share: 8.048
- gini_hold: 7.704
- top3_share: 7.669
- exited_share: 7.46
- first_slot_share: 7.005
- dev_sold: 6.427
- buyers_n: 6.368
- top1_share: 5.635
- same_size_share: 5.61

## xgb_shape+holders: top gain features

- run_from_low: 88.149
- sol_per_s_window: 64.437
- curve_sol_in: 52.459
- log_ret_window: 18.194
- dev_share: 15.234
- launch_bundle_share: 13.272
- from_peak: 12.086
- max_drawdown: 11.955
- iti_median: 11.847
- volume_slope: 11.484
- first_slot_share: 11.422
- buy_ratio_count: 11.265
- n_buyers: 10.707
- buyers_last60: 10.688
- iti_cv: 10.144

## xgb_all: top gain features

- run_from_low: 97.425
- sol_per_s_window: 57.357
- curve_sol_in: 53.044
- dev_share: 15.036
- replies_at_entry: 14.956
- sell_share_sol: 14.071
- max_drawdown: 13.935
- buyers_last60: 13.496
- from_peak: 12.443
- launch_bundle_share: 11.975
- iti_median: 11.582
- creator_prior_tp_rate: 11.513
- first_slot_share: 10.615
- n_buyers: 10.205
- volume_slope: 9.906

## xgb_context: top gain features

- is_native_launch: 26.841
- replies_at_entry: 20.297
- has_twitter: 12.014
- live_at_entry: 8.547
- market_recent_n: 7.072
- has_telegram: 6.959
- description_len: 6.345
- name_dup_24h: 6.175
- market_launch_rate: 6.093
- market_candidate_rate: 5.909
- hour_sin: 5.85
- hour_cos: 5.541
- image_dup_24h: 5.516
- market_recent_tp_rate: 5.508
- dow_sin: 5.434

## xgb_wallets: top gain features

- w_repeat_share: 16.091
- w_hit_rate_mean: 10.047
- w_hit_rate_sol: 8.972
- w_scored_share: 6.84
- w_serial_share: 6.095
- w_hit_rate_max: 5.59
- w_log_prior_mean: 5.45

## xgb_holders+wallets: top gain features

- top10_share: 60.598
- tokens_out_pct: 57.497
- holders_n: 22.371
- launch_bundle_share: 20.669
- dev_share: 14.945
- exited_share: 13.183
- top3_share: 12.146
- gini_hold: 11.276
- dev_sold: 9.987
- first_slot_share: 9.983
- w_hit_rate_sol: 9.923
- buyers_n: 9.062
- w_log_prior_mean: 8.532
- top1_share: 7.553
- w_hit_rate_mean: 7.54

## xgb_all+wallets: top gain features

- run_from_low: 94.289
- curve_sol_in: 79.673
- sol_per_s_window: 56.621
- dev_share: 18.15
- launch_bundle_share: 15.517
- buyers_last60: 15.332
- buyers_n: 14.772
- sell_share_sol: 13.734
- max_drawdown: 13.233
- replies_at_entry: 13.203
- creator_prior_tp_rate: 12.946
- volume_slope: 12.184
- from_peak: 12.045
- iti_median: 11.939
- n_buyers: 11.786

## xgb_botlive: top gain features

- bl_log_ret_window: 46.176
- bl_run_from_low: 44.428
- bl_sol_per_s_window: 10.47
- bl_curve_sol_in: 9.621
- bl_max_drawdown: 9.133
- bl_lows_per_min: 8.763
- bl_top10_share: 8.11
- bl_dev_buy_sol: 7.989
- bl_price_slope: 6.706
- bl_from_peak: 6.151
- bl_sol_last60: 5.948
- bl_trades_last60: 5.433
- bl_inflow_accel: 5.068
- bl_lows: 4.58
- bl_first_seen_sol: 4.516

## xgb_botlive+context: top gain features

- bl_log_ret_window: 57.26
- bl_run_from_low: 31.174
- replies_at_entry: 12.806
- bl_sol_per_s_window: 11.908
- has_twitter: 9.825
- bl_curve_sol_in: 9.742
- bl_top10_share: 9.208
- bl_max_drawdown: 8.21
- bl_lows: 8.11
- live_at_entry: 7.896
- bl_dev_buy_sol: 7.698
- bl_price_slope: 7.275
- is_native_launch: 6.928
- bl_from_peak: 6.925
- description_len: 6.66

## xgb_pnl:all+wallets: top gain features

- largest_buy_share: 5.927
- sell_share_sol: 3.679
- buy_size_cv: 3.094
- dev_buy_sol: 3.013
- buy_ratio_count: 2.773
- buy_ratio_sol: 2.653
- volume_slope: 2.5
- creator_prior_tp_rate: 2.242
- gini_hold: 2.212
- dev_share: 1.978
- tokens_out_pct: 1.828
- time_to_10_trades: 1.729
- creator_prior_launches: 1.665
- log_ret_window: 1.614
- exited_share: 1.585

## xgb_pnl:botlive+context: top gain features

- bl_dev_buy_sol: 3.28
- bl_max_drawdown: 2.775
- bl_from_peak: 2.549
- twitter_is_status: 1.677
- replies_at_entry: 1.515
- bl_log_ret_window: 1.371
- is_native_launch: 1.316
- has_telegram: 1.3
- live_at_entry: 1.3
- bl_run_from_low: 1.274
- bl_top10_share: 1.251
- bl_sol_per_s_window: 1.241
- name_dup_24h: 1.237
- bl_curve_sol_in: 1.23
- bl_sol_last60: 1.196
