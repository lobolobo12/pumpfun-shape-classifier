# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 1472 | 0.240 | 0.828 | 0.33 | 0.35 | 0.26 | -0.32 | -2.02 |
| xgb_holders | 1472 | 0.240 | 0.807 | 0.47 | 0.28 | 0.20 | -6.82 | -8.49 |
| xgb_shape+holders | 1472 | 0.253 | 0.821 | 0.47 | 0.27 | 0.21 | -5.47 | -7.18 |
| xgb_all | 1472 | 0.245 | 0.822 | 0.47 | 0.30 | 0.22 | -5.21 | -6.92 |
| xgb_context | 1472 | 0.079 | 0.557 | 0.13 | 0.09 | 0.08 | -8.04 | -9.66 |
| xgb_wallets | 1472 | 0.164 | 0.679 | 0.33 | 0.15 | 0.14 | -4.24 | -5.89 |
| xgb_holders+wallets | 1472 | 0.188 | 0.786 | 0.27 | 0.18 | 0.18 | -7.74 | -9.58 |
| xgb_all+wallets | 1472 | 0.260 | 0.827 | 0.40 | 0.31 | 0.24 | -3.44 | -5.14 |
| xgb_botlive | 1472 | 0.252 | 0.832 | 0.33 | 0.34 | 0.27 | 1.51 | -0.19 |
| xgb_botlive+context | 1472 | 0.235 | 0.829 | 0.40 | 0.27 | 0.24 | -1.63 | -3.38 |
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

- run_from_low: 95.727
- sol_per_s_window: 57.894
- curve_sol_in: 50.397
- replies_at_entry: 14.96
- dev_share: 14.913
- sell_share_sol: 14.055
- max_drawdown: 13.904
- buyers_last60: 13.279
- from_peak: 12.124
- launch_bundle_share: 11.957
- creator_prior_tp_rate: 11.574
- iti_median: 11.312
- n_sellers: 10.303
- first_slot_share: 10.245
- buy_ratio_count: 10.218

## xgb_context: top gain features

- is_native_launch: 20.864
- replies_at_entry: 17.408
- has_twitter: 10.218
- live_at_entry: 7.098
- market_recent_n: 6.568
- has_telegram: 5.801
- name_dup_24h: 5.755
- description_len: 5.743
- market_launch_rate: 5.565
- market_candidate_rate: 5.414
- hour_sin: 5.207
- image_dup_24h: 5.056
- has_website: 5.054
- hour_cos: 4.988
- market_recent_tp_rate: 4.853

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

- run_from_low: 77.817
- curve_sol_in: 65.12
- sol_per_s_window: 51.632
- dev_share: 13.312
- replies_at_entry: 13.251
- sell_share_sol: 13.063
- buyers_n: 12.39
- launch_bundle_share: 11.279
- max_drawdown: 11.248
- creator_prior_tp_rate: 11.203
- iti_median: 11.03
- buyers_last60: 10.656
- volume_slope: 10.577
- dev_sold: 10.534
- twitter_is_status: 10.362

## xgb_botlive: top gain features

- run_from_low: 77.249
- curve_sol_in: 45.86
- sol_per_s_window: 42.068
- max_drawdown: 13.004
- from_peak: 9.976
- dev_buy_sol: 9.78
- log_ret_window: 9.658
- lows_per_min: 9.186
- lows: 8.274
- inflow_accel: 7.381
- trades_last60: 6.464
- sol_last60: 6.324
- top10_share: 6.296
- price_slope: 4.732

## xgb_botlive+context: top gain features

- run_from_low: 90.229
- sol_per_s_window: 47.47
- curve_sol_in: 42.927
- log_ret_window: 31.31
- twitter_is_status: 22.927
- live_at_entry: 17.153
- max_drawdown: 13.747
- lows_per_min: 13.144
- has_telegram: 12.285
- has_twitter: 11.827
- lows: 11.506
- from_peak: 11.441
- dev_buy_sol: 11.23
- replies_at_entry: 10.953
- market_candidate_rate: 8.817
