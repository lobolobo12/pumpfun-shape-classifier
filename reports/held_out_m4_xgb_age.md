# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 1086 | 0.236 | 0.823 | 0.36 | 0.33 | 0.28 | 1.19 | -0.42 |
| xgb_holders | 1086 | 0.255 | 0.809 | 0.55 | 0.33 | 0.28 | 1.19 | -0.49 |
| xgb_shape+holders | 1086 | 0.276 | 0.827 | 0.55 | 0.37 | 0.28 | 0.35 | -1.42 |
| xgb_all | 1086 | 0.247 | 0.823 | 0.36 | 0.35 | 0.28 | 0.84 | -0.88 |
| xgb_context | 1086 | 0.092 | 0.559 | 0.09 | 0.13 | 0.11 | -4.77 | -6.36 |
| xgb_wallets | 1086 | 0.203 | 0.697 | 0.55 | 0.20 | 0.17 | -1.97 | -3.58 |
| xgb_holders+wallets | 1086 | 0.176 | 0.775 | 0.09 | 0.31 | 0.21 | -3.97 | -5.76 |
| xgb_all+wallets | 1086 | 0.271 | 0.824 | 0.55 | 0.30 | 0.26 | -0.53 | -2.20 |
| logistic_repo_recipe | 1086 | 0.222 | 0.800 | 0.27 | 0.28 | 0.27 | 0.02 | -1.87 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- curve_sol_in: 102.921
- run_from_low: 101.167
- sol_per_s_window: 70.723
- max_drawdown: 17.608
- buyers_last60: 16.525
- n_buyers: 16.152
- largest_buy_share: 14.649
- iti_median: 13.736
- buy_ratio_count: 13.57
- buy_ratio_sol: 11.948
- round_size_share: 11.012
- lows: 10.929
- trades_last60: 10.601
- from_peak: 10.475
- price_slope: 10.466

## xgb_holders: top gain features

- tokens_out_pct: 39.505
- holders_n: 16.451
- launch_bundle_share: 16.024
- top10_share: 13.792
- top3_share: 10.836
- gini_hold: 8.908
- exited_share: 8.568
- dev_share: 7.998
- first_slot_share: 7.907
- dev_sold: 7.834
- buyers_n: 6.708
- top1_share: 5.888
- same_size_share: 5.454

## xgb_shape+holders: top gain features

- run_from_low: 108.307
- curve_sol_in: 78.591
- sol_per_s_window: 65.544
- log_ret_window: 24.494
- launch_bundle_share: 19.785
- holders_n: 19.702
- sell_share_sol: 13.023
- dev_share: 12.681
- n_sellers: 12.219
- buy_ratio_count: 11.921
- buyers_last60: 11.895
- iti_median: 11.855
- iti_cv: 11.401
- n_buyers: 11.217
- lows_per_min: 11.005

## xgb_all: top gain features

- run_from_low: 123.295
- curve_sol_in: 83.098
- sol_per_s_window: 73.75
- launch_bundle_share: 26.71
- largest_buy_share: 19.391
- iti_median: 19.16
- buy_ratio_count: 16.38
- holders_n: 16.024
- dev_share: 15.548
- round_size_share: 14.541
- buyers_last60: 14.324
- is_native_launch: 14.109
- creator_prior_resolved: 13.942
- max_drawdown: 13.7
- creator_prior_tp_rate: 13.401

## xgb_context: top gain features

- replies_at_entry: 24.682
- is_native_launch: 14.726
- has_twitter: 8.281
- has_telegram: 5.855
- has_website: 5.656
- market_recent_n: 5.496
- description_len: 5.345
- market_recent_tp_rate: 5.024
- hour_sin: 4.975
- market_launch_rate: 4.957
- hour_cos: 4.908
- twitter_is_status: 4.819
- image_dup_24h: 4.756
- market_candidate_rate: 4.729
- name_dup_24h: 4.707

## xgb_wallets: top gain features

- w_repeat_share: 17.673
- w_hit_rate_mean: 9.865
- w_hit_rate_sol: 8.748
- w_scored_share: 7.171
- w_serial_share: 6.009
- w_hit_rate_max: 5.355
- w_log_prior_mean: 4.804

## xgb_holders+wallets: top gain features

- tokens_out_pct: 55.994
- top10_share: 41.986
- launch_bundle_share: 26.29
- holders_n: 21.488
- top3_share: 18.081
- gini_hold: 14.093
- dev_sold: 10.772
- exited_share: 9.744
- dev_share: 9.109
- first_slot_share: 9.077
- buyers_n: 8.996
- w_log_prior_mean: 8.449
- top1_share: 8.377
- w_scored_share: 7.951
- w_hit_rate_sol: 7.858

## xgb_all+wallets: top gain features

- run_from_low: 110.215
- curve_sol_in: 77.136
- sol_per_s_window: 69.609
- buyers_n: 23.302
- launch_bundle_share: 20.415
- holders_n: 15.831
- dev_share: 15.17
- replies_at_entry: 14.779
- iti_median: 14.46
- top3_share: 14.115
- buy_ratio_count: 13.534
- n_sellers: 13.178
- buyers_last60: 13.065
- creator_prior_tp_rate: 12.873
- buy_ratio_sol: 12.713
