# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 658 | 0.284 | 0.826 | 0.29 | 0.30 | 0.32 | 2.31 | 0.61 |
| xgb_holders | 658 | 0.327 | 0.813 | 0.71 | 0.36 | 0.30 | 2.12 | -0.23 |
| xgb_shape+holders | 658 | 0.346 | 0.816 | 0.86 | 0.36 | 0.35 | 3.67 | 1.91 |
| xgb_all | 658 | 0.341 | 0.829 | 0.43 | 0.39 | 0.33 | 3.14 | 1.37 |
| xgb_context | 658 | 0.101 | 0.536 | 0.00 | 0.09 | 0.06 | -4.07 | -5.62 |
| xgb_wallets | 658 | 0.174 | 0.667 | 0.29 | 0.15 | 0.20 | -1.06 | -2.70 |
| xgb_holders+wallets | 658 | 0.283 | 0.806 | 0.57 | 0.24 | 0.23 | -1.20 | -3.61 |
| xgb_all+wallets | 658 | 0.324 | 0.821 | 0.57 | 0.30 | 0.32 | 2.06 | 0.29 |
| logistic_repo_recipe | 658 | 0.264 | 0.786 | 0.43 | 0.30 | 0.26 | -0.46 | -2.38 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- sol_per_s_window: 91.796
- curve_sol_in: 81.627
- run_from_low: 25.437
- lows_per_min: 22.586
- max_drawdown: 20.475
- iti_median: 14.265
- n_buyers: 13.632
- from_peak: 11.591
- largest_buy_share: 10.692
- buy_ratio_sol: 10.306
- buy_ratio_count: 10.241
- flipper_share: 9.731
- buyers_last60: 9.655
- biggest_buy_vs_curve: 8.999
- trades_last60: 8.989

## xgb_holders: top gain features

- tokens_out_pct: 27.986
- launch_bundle_share: 12.626
- top3_share: 11.919
- holders_n: 11.63
- exited_share: 7.973
- gini_hold: 7.572
- first_slot_share: 7.427
- top10_share: 6.782
- dev_share: 6.759
- buyers_n: 6.3
- dev_sold: 5.992
- top1_share: 5.655
- same_size_share: 5.168

## xgb_shape+holders: top gain features

- sol_per_s_window: 95.548
- curve_sol_in: 89.525
- run_from_low: 27.98
- log_ret_window: 25.369
- max_drawdown: 25.049
- launch_bundle_share: 23.271
- lows_per_min: 19.359
- iti_median: 17.667
- dev_share: 14.009
- n_buyers: 13.106
- from_peak: 11.837
- largest_buy_share: 11.567
- exited_share: 11.345
- tokens_out_pct: 11.02
- iti_cv: 10.872

## xgb_all: top gain features

- sol_per_s_window: 86.425
- curve_sol_in: 81.391
- run_from_low: 43.682
- max_drawdown: 20.111
- launch_bundle_share: 18.146
- iti_median: 17.611
- sell_share_sol: 16.4
- bundle_slots: 15.764
- lows_per_min: 14.656
- n_buyers: 13.737
- log_ret_window: 13.498
- dev_share: 12.714
- replies_at_entry: 12.704
- tokens_out_pct: 12.472
- buyers_last60: 12.45

## xgb_context: top gain features

- has_twitter: 10.71
- is_native_launch: 9.982
- description_len: 9.557
- has_website: 9.333
- replies_at_entry: 8.226
- live_at_entry: 8.103
- market_recent_n: 7.874
- name_dup_24h: 6.907
- market_candidate_rate: 6.343
- hour_sin: 6.096
- dow_sin: 5.929
- hour_cos: 5.889
- image_dup_24h: 5.848
- market_recent_tp_rate: 5.683
- market_launch_rate: 5.665

## xgb_wallets: top gain features

- w_repeat_share: 16.899
- w_hit_rate_sol: 10.06
- w_hit_rate_mean: 7.773
- w_hit_rate_max: 7.4
- w_scored_share: 6.82
- w_serial_share: 6.606
- w_log_prior_mean: 5.005

## xgb_holders+wallets: top gain features

- tokens_out_pct: 35.628
- top10_share: 26.193
- holders_n: 21.219
- launch_bundle_share: 16.436
- top3_share: 11.843
- exited_share: 9.865
- gini_hold: 9.119
- dev_share: 7.801
- buyers_n: 7.734
- dev_sold: 7.66
- w_scored_share: 7.254
- first_slot_share: 6.443
- top1_share: 6.327
- w_log_prior_mean: 6.207
- w_repeat_share: 6.106

## xgb_all+wallets: top gain features

- curve_sol_in: 94.86
- sol_per_s_window: 79.467
- run_from_low: 30.62
- max_drawdown: 16.921
- launch_bundle_share: 15.392
- iti_median: 14.573
- sell_share_sol: 12.891
- buyers_last60: 12.733
- replies_at_entry: 12.573
- dev_share: 12.464
- lows_per_min: 11.763
- lows: 11.63
- buy_ratio_count: 10.235
- exited_share: 9.774
- from_peak: 9.763
