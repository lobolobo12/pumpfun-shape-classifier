# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 224 | 0.257 | 0.780 | 0.00 | 0.27 | 0.27 | 1.12 | -1.11 |
| xgb_holders | 224 | 0.254 | 0.770 | 0.50 | 0.18 | 0.32 | 1.10 | -1.16 |
| xgb_shape+holders | 224 | 0.336 | 0.800 | 0.50 | 0.36 | 0.32 | 1.60 | -0.64 |
| xgb_all | 224 | 0.277 | 0.787 | 0.00 | 0.36 | 0.23 | 0.63 | -1.61 |
| xgb_context | 224 | 0.138 | 0.478 | 0.50 | 0.27 | 0.14 | -0.28 | -1.82 |
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

- run_from_low: 65.856
- holders_n: 19.438
- tokens_out_pct: 18.494
- buyers_last60: 17.404
- lows: 11.512
- lows_per_min: 11.471
- sell_share_sol: 10.743
- biggest_buy_vs_curve: 10.451
- launch_bundle_share: 9.856
- log_ret_window: 9.69
- buy_ratio_sol: 8.796
- top1_share: 8.772
- iti_median: 8.164
- creator_prior_tp_rate: 7.778
- top10_share: 7.683

## xgb_context: top gain features

- market_recent_tp_rate: 4.058
- hour_sin: 4.005
- market_recent_n: 3.993
- hour_cos: 3.813
- is_native_launch: 3.42
- live_at_entry: 2.95
- replies_at_entry: 2.684
