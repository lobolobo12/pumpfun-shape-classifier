# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 224 | 0.285 | 0.790 | 0.50 | 0.36 | 0.32 | 1.81 | -0.46 |
| xgb_holders | 224 | 0.285 | 0.795 | 0.00 | 0.09 | 0.36 | 1.64 | 0.04 |
| xgb_shape+holders | 224 | 0.260 | 0.790 | 0.00 | 0.36 | 0.32 | 1.33 | -0.41 |
| xgb_all | 224 | 0.270 | 0.785 | 0.00 | 0.27 | 0.32 | 1.33 | -0.41 |
| xgb_context | 224 | 0.086 | 0.446 | 0.00 | 0.09 | 0.09 | -1.27 | -2.56 |
| logistic_repo_recipe | 224 | 0.244 | 0.788 | 0.00 | 0.09 | 0.32 | 1.77 | -0.64 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- run_from_low: 58.253
- log_ret_window: 14.719
- buyers_last60: 13.588
- biggest_buy_vs_curve: 13.442
- lows_per_min: 13.338
- lows: 11.479
- buy_ratio_sol: 9.107
- iti_median: 8.885
- volume_slope: 8.548
- last_trade_t: 8.4
- sell_share_sol: 8.298
- iti_cv: 8.191
- n_buyers: 7.958
- buy_ratio_count: 7.936
- iti_std: 7.845

## xgb_holders: top gain features

- tokens_out_pct: 40.743
- holders_n: 30.652
- launch_bundle_share: 17.855
- top10_share: 13.479
- gini_hold: 11.176
- first_slot_share: 10.187
- exited_share: 9.829
- top3_share: 9.372
- dev_sold: 9.075
- top1_share: 7.888
- buyers_n: 7.536
- dev_share: 7.127
- same_size_share: 6.761

## xgb_shape+holders: top gain features

- run_from_low: 105.428
- tokens_out_pct: 46.634
- log_ret_window: 36.266
- holders_n: 35.889
- lows_per_min: 30.064
- trades_last60: 24.893
- buyers_n: 23.381
- launch_bundle_share: 22.474
- lows: 22.308
- top10_share: 20.002
- biggest_buy_vs_curve: 18.174
- top1_share: 16.843
- n_trades: 15.507
- top3_share: 15.481
- buyers_last60: 14.985

## xgb_all: top gain features

- run_from_low: 107.177
- tokens_out_pct: 49.504
- holders_n: 44.006
- lows: 29.657
- top10_share: 28.295
- lows_per_min: 23.299
- launch_bundle_share: 20.495
- buyers_last60: 20.194
- biggest_buy_vs_curve: 20.056
- buy_ratio_sol: 16.206
- trades_last60: 15.127
- top1_share: 14.78
- same_size_share: 13.946
- buy_ratio_count: 13.36
- dev_sold: 12.996

## xgb_context: top gain features

- hour_cos: 3.537
- hour_sin: 3.115
- is_native_launch: 2.473
- live_at_entry: 2.132
- replies_at_entry: 1.716
