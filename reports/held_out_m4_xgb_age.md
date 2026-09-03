# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 224 | 0.257 | 0.780 | 0.00 | 0.27 | 0.27 | 1.12 | -1.11 |
| xgb_holders | 224 | 0.254 | 0.770 | 0.50 | 0.18 | 0.32 | 1.10 | -1.16 |
| xgb_shape+holders | 224 | 0.336 | 0.800 | 0.50 | 0.36 | 0.32 | 1.60 | -0.64 |
| xgb_all | 224 | 0.262 | 0.792 | 0.00 | 0.18 | 0.32 | 1.03 | -0.56 |
| xgb_context | 224 | 0.156 | 0.487 | 0.00 | 0.36 | 0.18 | 0.08 | -1.46 |
| xgb_wallets | 224 | 0.134 | 0.631 | 0.00 | 0.09 | 0.14 | -0.81 | -2.33 |
| xgb_holders+wallets | 224 | 0.244 | 0.797 | 0.00 | 0.27 | 0.27 | 0.85 | -1.41 |
| xgb_all+wallets | 224 | 0.254 | 0.785 | 0.00 | 0.18 | 0.36 | 2.40 | 0.12 |
| logistic_repo_recipe | 224 | 0.186 | 0.739 | 0.00 | 0.09 | 0.14 | -1.96 | -3.63 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- run_from_low: 33.982
- buyers_last60: 12.791
- log_ret_window: 8.584
- biggest_buy_vs_curve: 8.241
- iti_median: 7.261
- lows_per_min: 7.0
- lows: 6.877
- sell_share_sol: 6.362
- max_drawdown: 5.992
- step_gini: 5.72
- n_buyers: 5.665
- iti_cv: 5.546
- gini_buy_size: 5.452
- buy_ratio_sol: 5.4
- volume_slope: 5.395

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

- run_from_low: 57.9
- buyers_last60: 20.119
- tokens_out_pct: 12.868
- top10_share: 11.744
- holders_n: 11.565
- biggest_buy_vs_curve: 9.697
- sell_share_sol: 9.592
- lows_per_min: 9.425
- buy_ratio_sol: 7.968
- exited_share: 7.858
- lows: 7.812
- iti_median: 7.435
- log_ret_window: 7.329
- top3_share: 6.917
- buy_ratio_count: 6.889

## xgb_all: top gain features

- run_from_low: 107.932
- top10_share: 52.252
- holders_n: 41.122
- buyers_last60: 32.882
- tokens_out_pct: 20.693
- lows_per_min: 16.567
- biggest_buy_vs_curve: 15.608
- buy_ratio_sol: 15.043
- sell_share_sol: 14.422
- iti_median: 13.822
- lows: 13.702
- top3_share: 13.491
- launch_bundle_share: 12.282
- creator_prior_launches: 11.83
- top1_share: 10.925

## xgb_context: top gain features

- market_recent_n: 5.268
- market_candidate_rate: 5.028
- hour_cos: 4.951
- market_launch_rate: 4.53
- hour_sin: 4.517
- market_recent_tp_rate: 4.29
- is_native_launch: 3.808
- live_at_entry: 3.615

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

- run_from_low: 92.984
- buyers_last60: 34.441
- bundle_slots: 32.189
- tokens_out_pct: 23.941
- launch_bundle_share: 17.785
- lows_per_min: 17.406
- holders_n: 16.967
- lows: 16.373
- biggest_buy_vs_curve: 15.89
- sell_share_sol: 15.573
- top3_share: 14.495
- iti_median: 14.027
- buy_ratio_count: 13.11
- top1_share: 12.314
- exited_share: 12.249
