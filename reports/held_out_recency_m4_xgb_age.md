# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 224 | 0.260 | 0.764 | 0.50 | 0.18 | 0.23 | -0.10 | -1.67 |
| xgb_holders | 224 | 0.325 | 0.792 | 1.00 | 0.36 | 0.27 | 0.36 | -1.86 |
| xgb_shape+holders | 224 | 0.324 | 0.800 | 0.50 | 0.36 | 0.36 | 2.57 | 0.33 |
| xgb_all | 224 | 0.287 | 0.798 | 0.50 | 0.36 | 0.27 | 0.52 | -1.01 |
| xgb_context | 224 | 0.113 | 0.589 | 0.00 | 0.09 | 0.09 | -0.73 | -1.88 |
| logistic_repo_recipe | 224 | 0.193 | 0.745 | 0.00 | 0.09 | 0.09 | -2.49 | -3.63 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- run_from_low: 77.439
- buyers_last60: 26.665
- log_ret_window: 18.88
- biggest_buy_vs_curve: 13.718
- iti_median: 12.28
- lows: 11.589
- sell_share_sol: 11.129
- n_buyers: 11.029
- trades_last60: 10.511
- lows_per_min: 10.081
- n_sellers: 9.411
- volume_slope: 9.06
- max_drawdown: 8.391
- last_trade_t: 8.352
- buy_ratio_count: 8.321

## xgb_holders: top gain features

- tokens_out_pct: 31.793
- holders_n: 20.308
- launch_bundle_share: 14.44
- top10_share: 11.058
- top3_share: 8.833
- gini_hold: 8.608
- first_slot_share: 8.46
- exited_share: 7.556
- buyers_n: 6.039
- dev_share: 5.747
- top1_share: 5.428
- dev_sold: 5.163
- same_size_share: 4.89

## xgb_shape+holders: top gain features

- run_from_low: 78.662
- buyers_last60: 19.507
- tokens_out_pct: 16.322
- holders_n: 13.574
- biggest_buy_vs_curve: 10.743
- buyers_n: 10.454
- iti_median: 9.925
- log_ret_window: 9.91
- lows_per_min: 9.788
- sell_share_sol: 9.735
- lows: 9.43
- trades_last60: 9.123
- top3_share: 8.62
- dev_sold: 8.454
- exited_share: 8.165

## xgb_all: top gain features

- run_from_low: 102.183
- buyers_last60: 30.174
- tokens_out_pct: 21.285
- holders_n: 20.112
- biggest_buy_vs_curve: 15.795
- iti_median: 13.977
- top1_share: 12.554
- launch_bundle_share: 12.275
- top3_share: 11.831
- dev_sold: 11.816
- lows_per_min: 11.306
- creator_prior_tp_rate: 11.235
- n_buyers: 11.215
- top10_share: 11.169
- trades_last60: 10.834

## xgb_context: top gain features

- hour_cos: 2.737
- hour_sin: 2.504
- is_native_launch: 1.741
- replies_at_entry: 1.527
- live_at_entry: 1.245
