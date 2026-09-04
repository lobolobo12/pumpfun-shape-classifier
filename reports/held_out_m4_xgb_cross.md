# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 127 | 0.341 | 0.680 | 0.00 | 0.50 | 0.38 | 1.32 | -0.60 |
| xgb_holders | 127 | 0.365 | 0.636 | 1.00 | 0.50 | 0.38 | 1.31 | -0.62 |
| xgb_shape+holders | 127 | 0.335 | 0.631 | 0.00 | 0.50 | 0.38 | 1.26 | -0.66 |
| xgb_all | 127 | 0.417 | 0.636 | 1.00 | 0.83 | 0.38 | 1.44 | -0.51 |
| xgb_context | 127 | 0.353 | 0.612 | 1.00 | 0.83 | 0.38 | 0.96 | -0.61 |
| xgb_wallets | 127 | 0.356 | 0.587 | 1.00 | 0.50 | 0.31 | 0.50 | -1.05 |
| xgb_holders+wallets | 127 | 0.424 | 0.679 | 1.00 | 0.67 | 0.46 | 2.05 | 0.10 |
| xgb_all+wallets | 127 | 0.408 | 0.648 | 1.00 | 0.83 | 0.38 | 1.50 | -0.45 |
| logistic_repo_recipe | 127 | 0.365 | 0.572 | 1.00 | 0.50 | 0.31 | 0.20 | -1.34 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- dev_buy_sol: 7.384
- sol_last60: 6.13
- lows: 5.878
- bundle_slots: 5.531
- flipper_share: 5.37
- max_drawdown: 5.171
- decision_age_s: 5.17
- buy_size_cv: 5.038
- n_trades: 5.003
- buyers_last60: 5.001
- buy_ratio_count: 4.892
- buy_ratio_sol: 4.874
- sell_share_sol: 4.732
- iti_cv: 4.665
- first_trade_t: 4.554

## xgb_holders: top gain features

- dev_share: 8.377
- dev_sold: 7.735
- top3_share: 5.872
- top1_share: 5.258
- launch_bundle_share: 5.14
- holders_n: 5.013
- top10_share: 4.724
- first_slot_share: 4.643
- tokens_out_pct: 4.179
- gini_hold: 4.176
- exited_share: 4.113
- buyers_n: 3.721
- same_size_share: 3.6

## xgb_shape+holders: top gain features

- dev_sold: 13.964
- dev_share: 10.465
- dev_buy_sol: 9.64
- top3_share: 8.397
- bundle_slots: 8.088
- top1_share: 7.601
- buy_size_cv: 7.534
- holders_n: 7.52
- decision_age_s: 7.249
- exited_share: 7.168
- launch_bundle_share: 7.014
- max_drawdown: 6.865
- lows: 6.843
- sol_last60: 6.826
- top10_share: 6.679

## xgb_all: top gain features

- is_native_launch: 16.219
- creator_prior_resolved: 9.895
- creator_prior_launches: 9.446
- sol_last60: 9.191
- dev_share: 8.934
- buy_size_cv: 8.674
- exited_share: 8.128
- top3_share: 8.081
- launch_bundle_share: 7.868
- top1_share: 7.771
- max_drawdown: 7.745
- market_recent_n: 7.642
- round_size_share: 7.388
- sell_share_sol: 7.225
- bundle_slots: 7.17

## xgb_context: top gain features

- is_native_launch: 13.069
- replies_at_entry: 8.688
- live_at_entry: 6.129
- market_recent_n: 5.746
- has_twitter: 5.199
- name_dup_24h: 4.79
- image_dup_24h: 4.43
- description_len: 4.331
- market_candidate_rate: 4.141
- hour_cos: 4.091
- market_launch_rate: 3.99
- market_recent_tp_rate: 3.967
- dow_sin: 3.89
- hour_sin: 3.871
- twitter_is_status: 3.495

## xgb_wallets: top gain features

- w_hit_rate_sol: 4.0
- w_log_prior_mean: 3.698
- w_repeat_share: 3.665
- w_scored_share: 3.364
- w_hit_rate_max: 3.345
- w_serial_share: 3.313
- w_hit_rate_mean: 3.305

## xgb_holders+wallets: top gain features

- dev_sold: 9.003
- dev_share: 8.478
- top3_share: 6.547
- top1_share: 6.299
- holders_n: 5.621
- launch_bundle_share: 5.594
- w_repeat_share: 5.313
- first_slot_share: 5.209
- top10_share: 5.101
- exited_share: 5.09
- gini_hold: 5.039
- tokens_out_pct: 4.987
- w_hit_rate_sol: 4.94
- w_serial_share: 4.928
- w_hit_rate_max: 4.91

## xgb_all+wallets: top gain features

- is_native_launch: 20.335
- creator_prior_launches: 12.538
- creator_prior_resolved: 12.243
- n_slots: 12.062
- buy_size_cv: 11.087
- dev_share: 11.004
- top3_share: 10.259
- exited_share: 10.188
- buy_ratio_count: 9.975
- replies_at_entry: 9.593
- sol_last60: 9.311
- max_drawdown: 9.126
- dow_cos: 9.104
- bundle_slots: 8.972
- live_at_entry: 8.902
