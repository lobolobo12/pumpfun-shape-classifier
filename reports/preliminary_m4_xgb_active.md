# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 1290 | 0.179 | 0.786 | 0.08 | 0.16 | 0.22 | -4.94 | -7.27 |
| xgb_holders | 1290 | 0.191 | 0.777 | 0.08 | 0.20 | 0.22 | -3.49 | -5.96 |
| xgb_shape+holders | 1290 | 0.204 | 0.801 | 0.23 | 0.25 | 0.22 | -4.59 | -7.06 |
| xgb_all | 1290 | 0.192 | 0.791 | 0.15 | 0.19 | 0.24 | -2.45 | -4.81 |
| xgb_context | 1290 | 0.069 | 0.496 | 0.00 | 0.05 | 0.06 | -4.21 | -6.05 |
| logistic_repo_recipe | 1290 | 0.163 | 0.745 | 0.15 | 0.19 | 0.19 | -6.87 | -8.74 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- buyers_last60: 13.302
- log_ret_window: 11.82
- run_from_low: 11.734
- trades_last60: 9.785
- biggest_buy_vs_curve: 9.611
- n_buyers: 6.563
- n_trades: 6.328
- sellers_last60: 6.309
- last_trade_t: 5.624
- step_gini: 5.128
- price_slope: 4.943
- from_peak: 4.917
- max_drawdown: 4.697
- n_sellers: 4.645
- iti_std: 4.554

## xgb_holders: top gain features

- tokens_out_pct: 9.58
- top10_share: 6.685
- holders_n: 5.969
- top1_share: 5.192
- top3_share: 5.152
- launch_bundle_share: 4.04
- buyers_n: 3.948
- gini_hold: 3.911
- exited_share: 3.473
- dev_share: 2.94
- first_slot_share: 2.796
- same_size_share: 2.563
- dev_sold: 0.591

## xgb_shape+holders: top gain features

- run_from_low: 17.444
- buyers_last60: 15.077
- tokens_out_pct: 13.687
- top3_share: 11.675
- log_ret_window: 8.996
- biggest_buy_vs_curve: 8.567
- trades_last60: 6.702
- sellers_last60: 6.124
- holders_n: 6.014
- top10_share: 5.992
- max_drawdown: 5.599
- n_buyers: 5.311
- sell_share_sol: 4.986
- from_peak: 4.984
- buy_ratio_sol: 4.906

## xgb_all: top gain features

- tokens_out_pct: 14.73
- buyers_last60: 14.615
- run_from_low: 13.328
- is_native_launch: 11.962
- top3_share: 11.265
- top10_share: 10.358
- biggest_buy_vs_curve: 8.71
- log_ret_window: 8.153
- n_buyers: 6.877
- max_drawdown: 6.623
- holders_n: 6.084
- n_trades: 6.0
- price_slope: 5.654
- top1_share: 5.628
- trades_last60: 5.489

## xgb_context: top gain features

- hour_cos: 2.345
- live_at_entry: 1.685
- hour_sin: 1.515
- replies_at_entry: 1.225
- is_native_launch: 1.124
