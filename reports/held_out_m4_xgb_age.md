# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 224 | 0.255 | 0.785 | 0.00 | 0.45 | 0.36 | 2.53 | 0.12 |
| xgb_holders | 224 | 0.254 | 0.770 | 0.50 | 0.18 | 0.32 | 1.10 | -1.16 |
| xgb_shape+holders | 224 | 0.328 | 0.810 | 0.50 | 0.36 | 0.32 | 1.93 | -0.30 |
| xgb_all | 224 | 0.240 | 0.795 | 0.00 | 0.27 | 0.32 | 1.33 | -0.37 |
| xgb_context | 224 | 0.095 | 0.471 | 0.00 | 0.18 | 0.09 | -0.82 | -2.09 |
| xgb_wallets | 224 | 0.134 | 0.631 | 0.00 | 0.09 | 0.14 | -0.81 | -2.33 |
| xgb_holders+wallets | 224 | 0.244 | 0.797 | 0.00 | 0.27 | 0.27 | 0.85 | -1.41 |
| xgb_all+wallets | 224 | 0.236 | 0.782 | 0.00 | 0.27 | 0.32 | 1.36 | -0.19 |
| logistic_repo_recipe | 224 | 0.186 | 0.739 | 0.00 | 0.09 | 0.14 | -1.96 | -3.63 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- run_from_low: 77.426
- sol_per_s_window: 71.611
- curve_sol_in: 67.119
- lows: 39.307
- lows_per_min: 21.394
- max_drawdown: 15.937
- buyers_last60: 15.326
- iti_median: 14.269
- volume_slope: 13.578
- n_sellers: 13.406
- sell_share_sol: 10.901
- log_ret_window: 10.663
- flipper_share: 10.627
- iti_cv: 10.529
- step_gini: 10.404

## xgb_holders: top gain features

- tokens_out_pct: 35.273
- top10_share: 27.117
- holders_n: 23.132
- launch_bundle_share: 16.389
- exited_share: 9.225
- gini_hold: 8.378
- first_slot_share: 7.917
- top3_share: 7.754
- dev_share: 7.138
- top1_share: 7.106
- dev_sold: 6.25
- same_size_share: 5.601
- buyers_n: 5.508

## xgb_shape+holders: top gain features

- sol_per_s_window: 52.22
- curve_sol_in: 48.312
- run_from_low: 36.146
- lows: 11.257
- tokens_out_pct: 10.947
- iti_median: 10.87
- lows_per_min: 10.135
- holders_n: 8.862
- top10_share: 8.714
- launch_bundle_share: 8.246
- max_drawdown: 8.187
- sell_share_sol: 8.109
- flipper_share: 8.103
- buyers_last60: 8.102
- buy_ratio_sol: 7.399

## xgb_all: top gain features

- run_from_low: 122.097
- sol_per_s_window: 75.384
- curve_sol_in: 67.515
- lows_per_min: 27.041
- max_drawdown: 25.166
- lows: 22.226
- top10_share: 20.487
- buyers_last60: 19.505
- launch_bundle_share: 18.695
- sell_share_sol: 17.461
- iti_median: 17.175
- buyers_n: 15.922
- creator_prior_launches: 14.892
- buy_ratio_count: 14.678
- volume_slope: 13.925

## xgb_context: top gain features

- has_twitter: 11.028
- dow_cos: 6.776
- name_dup_24h: 6.279
- market_candidate_rate: 6.07
- market_launch_rate: 6.035
- has_telegram: 5.968
- dow_sin: 5.945
- description_len: 5.859
- hour_sin: 5.673
- market_recent_n: 5.616
- market_recent_tp_rate: 5.543
- has_website: 5.472
- is_native_launch: 4.987
- image_dup_24h: 4.289
- hour_cos: 4.286

## xgb_wallets: top gain features

- w_repeat_share: 11.414
- w_hit_rate_sol: 6.918
- w_scored_share: 6.183
- w_hit_rate_mean: 5.991
- w_hit_rate_max: 5.959
- w_serial_share: 5.014
- w_log_prior_mean: 4.336

## xgb_holders+wallets: top gain features

- holders_n: 41.098
- top10_share: 35.454
- tokens_out_pct: 34.107
- launch_bundle_share: 18.526
- exited_share: 11.41
- dev_sold: 10.974
- gini_hold: 10.499
- dev_share: 8.358
- first_slot_share: 7.989
- w_hit_rate_sol: 7.782
- top1_share: 7.569
- w_scored_share: 7.47
- buyers_n: 7.406
- top3_share: 7.396
- w_repeat_share: 7.288

## xgb_all+wallets: top gain features

- run_from_low: 106.622
- curve_sol_in: 88.147
- sol_per_s_window: 68.538
- lows: 38.781
- buyers_last60: 22.418
- launch_bundle_share: 22.078
- sell_share_sol: 21.456
- lows_per_min: 21.15
- iti_median: 17.87
- max_drawdown: 16.889
- creator_prior_launches: 16.145
- log_ret_window: 15.817
- dev_sold: 14.606
- holders_n: 14.491
- volume_slope: 14.42
