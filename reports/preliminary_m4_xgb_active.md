# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 118 | 0.168 | 0.759 | 0.00 | 0.17 | 0.17 | -1.15 | -1.96 |
| xgb_holders | 118 | 0.196 | 0.734 | 1.00 | 0.17 | 0.17 | -0.80 | -1.94 |
| xgb_shape+holders | 118 | 0.192 | 0.801 | 0.00 | 0.17 | 0.17 | -1.15 | -1.96 |
| xgb_all | 118 | 0.178 | 0.782 | 0.00 | 0.00 | 0.17 | -1.10 | -1.93 |
| logistic_repo_recipe | 118 | 0.206 | 0.773 | 0.00 | 0.33 | 0.25 | -0.62 | -2.13 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- log_ret_window: 8.509
- run_from_low: 7.003
- sell_share_sol: 6.728
- biggest_buy_vs_curve: 4.271
- n_slots: 3.886
- iti_std: 3.824
- n_buyers: 3.747
- iti_median: 3.654
- buyers_last60: 3.572
- bundle_slots: 3.508
- n_trades: 3.452
- last_trade_t: 3.41
- price_slope: 2.91
- lows: 2.837
- max_drawdown: 2.767

## xgb_holders: top gain features

- holders_n: 7.599
- tokens_out_pct: 6.956
- top10_share: 6.928
- buyers_n: 4.811
- top3_share: 4.428
- gini_hold: 4.24
- exited_share: 3.972
- dev_share: 3.911
- top1_share: 3.85
- launch_bundle_share: 3.695
- first_slot_share: 3.657
- same_size_share: 2.721
- dev_sold: 2.447

## xgb_shape+holders: top gain features

- log_ret_window: 11.929
- run_from_low: 9.008
- buyers_n: 6.455
- biggest_buy_vs_curve: 5.787
- iti_median: 5.625
- iti_std: 5.308
- bundle_slots: 4.672
- last_trade_t: 4.533
- max_drawdown: 4.515
- n_slots: 4.462
- buyers_last60: 4.152
- price_slope: 4.105
- gini_hold: 3.945
- lows: 3.908
- holders_n: 3.892

## xgb_all: top gain features

- run_from_low: 13.278
- log_ret_window: 13.209
- biggest_buy_vs_curve: 8.955
- n_slots: 8.037
- iti_std: 7.295
- lows_per_min: 7.283
- iti_median: 6.802
- buyers_last60: 6.783
- from_peak: 6.404
- max_drawdown: 6.241
- lows: 6.234
- bundle_slots: 6.114
- last_trade_t: 6.091
- gini_hold: 6.081
- n_sellers: 6.017
