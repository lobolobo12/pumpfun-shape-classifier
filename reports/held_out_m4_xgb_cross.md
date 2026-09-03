# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 103 | 0.335 | 0.704 | 0.00 | 0.40 | 0.40 | 1.34 | -0.42 |
| xgb_holders | 103 | 0.473 | 0.771 | 1.00 | 0.40 | 0.60 | 12.73 | 0.72 |
| xgb_shape+holders | 103 | 0.391 | 0.724 | 0.00 | 0.60 | 0.60 | 12.82 | 0.74 |
| xgb_all | 103 | 0.355 | 0.742 | 0.00 | 0.20 | 0.40 | 11.61 | -0.47 |
| xgb_context | 103 | 0.184 | 0.505 | 0.00 | 0.20 | 0.20 | -0.05 | -1.41 |
| xgb_wallets | 103 | 0.179 | 0.504 | 0.00 | 0.00 | 0.10 | -1.04 | -1.46 |
| xgb_holders+wallets | 103 | 0.393 | 0.727 | 0.00 | 0.80 | 0.40 | 11.31 | -0.77 |
| xgb_all+wallets | 103 | 0.324 | 0.629 | 1.00 | 0.40 | 0.40 | 11.54 | -0.55 |
| logistic_repo_recipe | 103 | 0.262 | 0.560 | 0.00 | 0.40 | 0.30 | 0.51 | -1.41 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- sol_last60: 5.728
- buy_ratio_count: 5.397
- max_drawdown: 5.061
- sellers_last60: 4.897
- iti_cv: 4.882
- bundle_slots: 4.831
- n_trades: 4.831
- sell_share_sol: 4.818
- price_slope: 4.656
- n_sellers: 4.513
- lows: 4.5
- trades_last60: 4.476
- lows_per_min: 4.466
- volume_slope: 4.434
- run_from_low: 4.418

## xgb_holders: top gain features

- exited_share: 6.553
- launch_bundle_share: 6.356
- dev_share: 6.151
- holders_n: 6.012
- top3_share: 5.88
- top10_share: 5.81
- first_slot_share: 5.693
- top1_share: 5.447
- tokens_out_pct: 5.214
- buyers_n: 5.0
- gini_hold: 4.858
- dev_sold: 4.706
- same_size_share: 4.226

## xgb_shape+holders: top gain features

- sol_last60: 7.232
- exited_share: 7.097
- launch_bundle_share: 6.363
- dev_share: 6.115
- holders_n: 5.995
- sell_share_sol: 5.946
- buy_ratio_count: 5.916
- top1_share: 5.844
- top3_share: 5.803
- gini_buy_size: 5.791
- buy_size_cv: 5.784
- top10_share: 5.671
- max_drawdown: 5.652
- gini_hold: 5.544
- n_trades: 5.496

## xgb_all: top gain features

- replies_at_entry: 11.395
- exited_share: 10.446
- sol_last60: 10.345
- bundle_slots: 10.26
- lows: 8.895
- holders_n: 8.588
- top3_share: 8.502
- buy_ratio_count: 8.389
- top1_share: 8.223
- is_native_launch: 8.215
- dev_share: 7.936
- launch_bundle_share: 7.75
- buyers_n: 7.645
- market_candidate_rate: 7.508
- creator_prior_launches: 7.41

## xgb_context: top gain features

- market_candidate_rate: 4.631
- is_native_launch: 4.389
- market_recent_tp_rate: 4.337
- market_launch_rate: 4.313
- market_recent_n: 4.132
- replies_at_entry: 3.953
- hour_sin: 3.716
- hour_cos: 3.227
- live_at_entry: 2.93

## xgb_wallets: top gain features

- w_repeat_share: 5.356
- w_hit_rate_mean: 5.196
- w_serial_share: 4.623
- w_hit_rate_sol: 4.346
- w_scored_share: 4.19
- w_hit_rate_max: 4.112
- w_log_prior_mean: 4.095

## xgb_holders+wallets: top gain features

- exited_share: 7.679
- launch_bundle_share: 6.933
- top3_share: 6.802
- dev_share: 6.754
- dev_sold: 6.7
- holders_n: 6.618
- top1_share: 6.6
- w_repeat_share: 6.371
- w_serial_share: 6.218
- w_log_prior_mean: 6.176
- w_hit_rate_mean: 6.138
- w_hit_rate_max: 6.128
- buyers_n: 6.118
- gini_hold: 6.082
- first_slot_share: 5.808

## xgb_all+wallets: top gain features

- holders_n: 12.775
- sol_last60: 12.081
- bundle_slots: 11.719
- buy_ratio_count: 11.156
- w_repeat_share: 10.575
- exited_share: 10.311
- top1_share: 10.201
- top3_share: 10.167
- creator_prior_resolved: 10.028
- max_drawdown: 9.968
- dev_share: 9.506
- first_slot_share: 9.28
- n_trades: 9.13
- launch_bundle_share: 9.01
- is_native_launch: 8.941
