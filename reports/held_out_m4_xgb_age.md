# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 224 | 0.252 | 0.754 | 0.50 | 0.27 | 0.18 | -0.43 | -2.65 |
| xgb_holders | 224 | 0.228 | 0.746 | 0.50 | 0.18 | 0.14 | -0.98 | -3.20 |
| xgb_shape+holders | 224 | 0.238 | 0.782 | 0.50 | 0.18 | 0.23 | 0.46 | -1.91 |
| xgb_all | 224 | 0.207 | 0.781 | 0.00 | 0.18 | 0.23 | -0.43 | -2.12 |
| xgb_context | 224 | 0.187 | 0.613 | 0.50 | 0.18 | 0.18 | 0.47 | -1.13 |
| logistic_repo_recipe | 224 | 0.213 | 0.769 | 0.00 | 0.09 | 0.18 | -1.12 | -2.81 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- run_from_low: 87.82
- log_ret_window: 36.451
- buyers_last60: 23.933
- sell_share_sol: 18.27
- biggest_buy_vs_curve: 14.181
- buy_ratio_sol: 13.98
- buy_ratio_count: 10.801
- n_buyers: 10.683
- n_sellers: 10.327
- last_trade_t: 10.286
- max_drawdown: 10.242
- buy_size_cv: 10.214
- lows_per_min: 9.977
- iti_cv: 9.29
- price_slope: 9.225

## xgb_holders: top gain features

- tokens_out_pct: 44.64
- top3_share: 15.625
- launch_bundle_share: 15.393
- holders_n: 15.389
- top10_share: 14.299
- exited_share: 12.36
- first_slot_share: 11.44
- buyers_n: 9.566
- dev_share: 8.579
- dev_sold: 8.475
- same_size_share: 8.452
- gini_hold: 7.973
- top1_share: 7.755

## xgb_shape+holders: top gain features

- run_from_low: 146.982
- log_ret_window: 95.866
- tokens_out_pct: 39.595
- buyers_last60: 37.874
- sell_share_sol: 34.67
- buy_ratio_sol: 22.204
- biggest_buy_vs_curve: 22.004
- launch_bundle_share: 21.656
- n_buyers: 17.854
- dev_share: 17.162
- buy_ratio_count: 16.686
- holders_n: 16.553
- exited_share: 16.194
- from_peak: 15.471
- last_trade_t: 14.702

## xgb_all: top gain features

- run_from_low: 154.366
- log_ret_window: 138.509
- tokens_out_pct: 44.203
- sell_share_sol: 42.648
- top3_share: 33.553
- biggest_buy_vs_curve: 31.515
- buy_ratio_sol: 26.766
- buyers_last60: 24.654
- launch_bundle_share: 21.21
- dev_share: 20.905
- n_buyers: 20.284
- holders_n: 19.487
- exited_share: 19.162
- n_sellers: 18.033
- from_peak: 17.231

## xgb_context: top gain features

- is_native_launch: 5.976
- replies_at_entry: 3.058
- hour_cos: 2.847
- hour_sin: 2.124
- live_at_entry: 1.802
