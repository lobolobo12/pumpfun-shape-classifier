# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 281 | 0.295 | 0.843 | 0.33 | 0.29 | 0.29 | -0.06 | -1.64 |
| xgb_holders | 281 | 0.331 | 0.807 | 1.00 | 0.36 | 0.25 | -0.53 | -2.08 |
| xgb_shape+holders | 281 | 0.383 | 0.835 | 0.67 | 0.36 | 0.36 | 1.20 | -0.36 |
| xgb_all | 281 | 0.377 | 0.844 | 0.67 | 0.29 | 0.36 | 1.32 | -0.34 |
| xgb_context | 281 | 0.088 | 0.527 | 0.00 | 0.07 | 0.07 | -1.92 | -2.97 |
| xgb_wallets | 281 | 0.184 | 0.690 | 0.33 | 0.21 | 0.25 | 0.77 | -0.81 |
| xgb_holders+wallets | 281 | 0.308 | 0.790 | 0.67 | 0.36 | 0.29 | 0.21 | -1.43 |
| xgb_all+wallets | 281 | 0.338 | 0.843 | 0.33 | 0.36 | 0.36 | 1.26 | -0.32 |
| logistic_repo_recipe | 281 | 0.329 | 0.797 | 0.67 | 0.36 | 0.29 | 0.05 | -1.60 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- sol_per_s_window: 66.192
- run_from_low: 65.947
- curve_sol_in: 41.046
- buyers_last60: 14.182
- lows_per_min: 13.862
- max_drawdown: 12.319
- iti_median: 11.544
- round_size_share: 10.282
- trades_last60: 9.881
- buy_ratio_count: 9.571
- log_ret_window: 9.017
- flipper_share: 8.998
- n_buyers: 8.955
- flip_latency_med: 8.687
- from_peak: 8.669

## xgb_holders: top gain features

- tokens_out_pct: 39.735
- launch_bundle_share: 18.502
- top10_share: 16.56
- holders_n: 14.74
- top3_share: 13.23
- first_slot_share: 9.737
- gini_hold: 9.245
- exited_share: 8.62
- dev_share: 7.023
- buyers_n: 6.565
- top1_share: 6.517
- dev_sold: 6.375
- same_size_share: 5.47

## xgb_shape+holders: top gain features

- run_from_low: 69.478
- sol_per_s_window: 61.031
- curve_sol_in: 42.845
- buyers_last60: 18.635
- launch_bundle_share: 13.123
- iti_median: 11.402
- tokens_out_pct: 10.365
- sell_share_sol: 10.093
- lows_per_min: 9.744
- holders_n: 9.128
- trades_last60: 9.099
- lows: 8.938
- buy_ratio_count: 8.809
- round_size_share: 8.768
- buyers_n: 8.559

## xgb_all: top gain features

- run_from_low: 78.814
- sol_per_s_window: 67.692
- curve_sol_in: 53.066
- buyers_last60: 18.823
- launch_bundle_share: 16.002
- dev_share: 12.137
- iti_median: 11.556
- tokens_out_pct: 10.764
- buy_ratio_count: 10.652
- n_buyers: 10.646
- trades_last60: 10.624
- creator_prior_tp_rate: 10.624
- dev_sold: 9.861
- creator_prior_launches: 9.845
- biggest_buy_vs_curve: 9.751

## xgb_context: top gain features

- is_native_launch: 18.353
- has_twitter: 11.653
- replies_at_entry: 7.374
- image_dup_24h: 6.773
- description_len: 6.372
- market_recent_tp_rate: 5.882
- market_launch_rate: 5.779
- market_recent_n: 5.604
- market_candidate_rate: 5.361
- name_dup_24h: 5.254
- dow_sin: 5.246
- has_website: 5.217
- hour_cos: 4.991
- hour_sin: 4.877
- live_at_entry: 4.793

## xgb_wallets: top gain features

- w_repeat_share: 13.853
- w_hit_rate_mean: 11.486
- w_hit_rate_sol: 8.394
- w_hit_rate_max: 7.743
- w_scored_share: 6.938
- w_serial_share: 6.594
- w_log_prior_mean: 5.072

## xgb_holders+wallets: top gain features

- top10_share: 45.087
- tokens_out_pct: 44.462
- launch_bundle_share: 20.424
- holders_n: 15.817
- top3_share: 15.699
- gini_hold: 11.01
- exited_share: 10.563
- dev_sold: 9.724
- dev_share: 8.625
- buyers_n: 8.563
- first_slot_share: 8.428
- w_hit_rate_sol: 7.424
- w_log_prior_mean: 7.233
- top1_share: 6.998
- w_scored_share: 6.53

## xgb_all+wallets: top gain features

- run_from_low: 77.771
- sol_per_s_window: 61.336
- curve_sol_in: 46.704
- buyers_last60: 14.419
- launch_bundle_share: 14.277
- iti_median: 11.11
- dev_share: 10.778
- creator_prior_tp_rate: 10.678
- has_twitter: 10.041
- gini_buy_size: 10.004
- biggest_buy_vs_curve: 9.94
- buy_ratio_count: 9.806
- lows_per_min: 9.513
- tokens_out_pct: 9.49
- log_ret_window: 9.418
