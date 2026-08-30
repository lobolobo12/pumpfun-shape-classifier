# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 191 | 0.216 | 0.851 | 0.00 | 0.20 | 0.21 | -0.45 | -1.98 |
| xgb_holders | 191 | 0.134 | 0.828 | 0.00 | 0.10 | 0.16 | -1.19 | -2.70 |
| xgb_shape+holders | 191 | 0.190 | 0.882 | 0.00 | 0.20 | 0.21 | -0.14 | -1.68 |
| xgb_all | 191 | 0.163 | 0.865 | 0.00 | 0.10 | 0.16 | -1.40 | -2.91 |
| logistic_repo_recipe | 191 | 0.113 | 0.757 | 0.00 | 0.10 | 0.11 | -2.03 | -3.17 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- log_ret_window: 24.529
- run_from_low: 18.54
- biggest_buy_vs_curve: 10.247
- iti_median: 6.564
- price_slope: 6.516
- lows_per_min: 5.819
- last_trade_t: 5.482
- step_gini: 5.262
- n_trades: 5.26
- n_slots: 5.157
- buy_ratio_sol: 5.079
- iti_std: 4.822
- sell_share_sol: 4.781
- gini_buy_size: 4.72
- lows: 4.578

## xgb_holders: top gain features

- top10_share: 21.765
- top3_share: 14.186
- top1_share: 12.111
- dev_sold: 11.654
- tokens_out_pct: 11.649
- gini_hold: 7.714
- exited_share: 7.708
- buyers_n: 7.552
- first_slot_share: 6.362
- holders_n: 5.843
- dev_share: 5.384
- launch_bundle_share: 5.218
- same_size_share: 4.698

## xgb_shape+holders: top gain features

- run_from_low: 47.734
- log_ret_window: 39.135
- biggest_buy_vs_curve: 17.559
- top3_share: 15.899
- buyers_n: 15.854
- holders_n: 12.851
- tokens_out_pct: 12.743
- lows: 12.365
- lows_per_min: 11.43
- n_buyers: 11.185
- last_trade_t: 11.033
- sell_share_sol: 10.716
- top10_share: 10.209
- exited_share: 9.945
- gini_hold: 9.838

## xgb_all: top gain features

- run_from_low: 42.744
- log_ret_window: 36.803
- top10_share: 16.373
- biggest_buy_vs_curve: 16.105
- n_buyers: 14.846
- top3_share: 14.28
- lows: 13.5
- buyers_last60: 13.247
- tokens_out_pct: 12.519
- last_trade_t: 11.178
- price_slope: 10.538
- exited_share: 10.366
- volume_slope: 9.756
- gini_hold: 9.716
- buy_size_cv: 9.62
