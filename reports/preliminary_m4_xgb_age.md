# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 753 | 0.293 | 0.785 | 0.62 | 0.37 | 0.29 | 1.92 | -0.71 |
| xgb_holders | 753 | 0.257 | 0.757 | 0.38 | 0.34 | 0.28 | 0.61 | -1.06 |
| xgb_shape+holders | 753 | 0.284 | 0.787 | 0.38 | 0.34 | 0.32 | 2.90 | 0.27 |
| xgb_all | 753 | 0.279 | 0.787 | 0.38 | 0.39 | 0.33 | 4.38 | 1.75 |
| xgb_context | 753 | 0.115 | 0.516 | 0.00 | 0.16 | 0.16 | 0.91 | -0.75 |
| logistic_repo_recipe | 753 | 0.241 | 0.757 | 0.25 | 0.26 | 0.28 | -0.08 | -1.77 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- run_from_low: 43.566
- buyers_last60: 15.656
- log_ret_window: 13.691
- sell_share_sol: 12.742
- trades_last60: 10.511
- iti_median: 9.648
- biggest_buy_vs_curve: 8.881
- last_trade_t: 8.391
- from_peak: 7.7
- n_sellers: 7.669
- iti_std: 7.563
- lows_per_min: 7.302
- buy_size_cv: 7.298
- sellers_last60: 7.265
- gini_buy_size: 7.209

## xgb_holders: top gain features

- tokens_out_pct: 18.396
- holders_n: 15.055
- top3_share: 8.556
- launch_bundle_share: 8.53
- exited_share: 7.993
- first_slot_share: 7.468
- top10_share: 6.296
- dev_sold: 5.955
- top1_share: 5.89
- buyers_n: 5.664
- dev_share: 5.495
- gini_hold: 5.196
- same_size_share: 4.978

## xgb_shape+holders: top gain features

- run_from_low: 41.243
- holders_n: 15.091
- tokens_out_pct: 14.252
- iti_median: 11.716
- sell_share_sol: 11.219
- trades_last60: 11.18
- biggest_buy_vs_curve: 9.704
- top3_share: 8.885
- last_trade_t: 8.882
- max_drawdown: 8.821
- buyers_last60: 8.461
- lows_per_min: 8.295
- log_ret_window: 8.234
- exited_share: 8.232
- n_sellers: 8.214

## xgb_all: top gain features

- run_from_low: 47.906
- log_ret_window: 18.51
- tokens_out_pct: 17.26
- sell_share_sol: 15.605
- buyers_n: 14.824
- iti_median: 11.86
- biggest_buy_vs_curve: 11.206
- holders_n: 10.976
- launch_bundle_share: 10.731
- top3_share: 10.113
- last_trade_t: 9.768
- live_at_entry: 9.352
- trades_last60: 9.221
- buy_ratio_sol: 8.891
- lows_per_min: 8.605

## xgb_context: top gain features

- hour_cos: 2.151
- live_at_entry: 1.949
- hour_sin: 1.918
- is_native_launch: 1.698
- replies_at_entry: 1.49
