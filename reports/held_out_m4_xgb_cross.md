# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 612 | 0.293 | 0.642 | 0.67 | 0.39 | 0.36 | 4.32 | 2.17 |
| xgb_holders | 612 | 0.273 | 0.596 | 0.33 | 0.45 | 0.33 | 2.77 | 0.69 |
| xgb_shape+holders | 612 | 0.232 | 0.566 | 0.33 | 0.26 | 0.30 | 1.11 | -0.99 |
| xgb_all | 612 | 0.245 | 0.610 | 0.33 | 0.29 | 0.25 | -0.42 | -2.59 |
| xgb_context | 612 | 0.209 | 0.546 | 0.00 | 0.19 | 0.23 | -1.43 | -3.15 |
| xgb_wallets | 612 | 0.213 | 0.525 | 0.17 | 0.26 | 0.26 | 0.53 | -1.09 |
| xgb_holders+wallets | 612 | 0.282 | 0.609 | 0.67 | 0.35 | 0.39 | 5.65 | 3.53 |
| xgb_all+wallets | 612 | 0.249 | 0.605 | 0.33 | 0.32 | 0.33 | 3.25 | 1.09 |
| xgb_botlive | 612 | 0.280 | 0.620 | 0.67 | 0.29 | 0.34 | 3.72 | 1.52 |
| xgb_botlive+context | 612 | 0.298 | 0.613 | 0.50 | 0.35 | 0.38 | 5.77 | 3.61 |
| logistic_repo_recipe | 612 | 0.264 | 0.590 | 0.67 | 0.39 | 0.28 | 0.21 | -1.50 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- dev_buy_sol: 9.66
- bundle_slots: 6.452
- sol_last60: 5.515
- max_drawdown: 5.141
- flipper_share: 5.07
- n_trades: 4.964
- buy_ratio_sol: 4.678
- first_trade_t: 4.677
- buy_size_cv: 4.608
- lows: 4.579
- trades_last60: 4.512
- sell_share_sol: 4.419
- sellers_last60: 4.344
- n_buyers: 4.291
- buy_ratio_count: 4.249

## xgb_holders: top gain features

- dev_sold: 8.923
- dev_share: 7.873
- top3_share: 4.698
- top1_share: 4.477
- first_slot_share: 4.131
- launch_bundle_share: 4.042
- holders_n: 3.873
- gini_hold: 3.692
- top10_share: 3.677
- tokens_out_pct: 3.53
- exited_share: 3.372
- buyers_n: 3.332
- same_size_share: 2.993

## xgb_shape+holders: top gain features

- dev_buy_sol: 21.214
- dev_sold: 19.029
- dev_share: 14.624
- top3_share: 9.004
- top1_share: 8.32
- bundle_slots: 7.832
- n_buyers: 7.546
- buy_size_cv: 7.428
- buy_ratio_count: 7.333
- holders_n: 7.312
- round_size_share: 7.021
- n_trades: 7.0
- sol_last60: 6.832
- max_drawdown: 6.799
- n_sellers: 6.554

## xgb_all: top gain features

- creator_prior_resolved: 36.058
- is_native_launch: 27.627
- replies_at_entry: 24.966
- creator_prior_launches: 16.985
- sol_last60: 11.543
- holders_n: 11.328
- bundle_slots: 10.592
- max_drawdown: 9.579
- launch_bundle_share: 9.535
- dev_share: 9.278
- buy_size_cv: 9.252
- first_trade_t: 9.232
- top1_share: 8.672
- time_to_10_trades: 8.035
- exited_share: 7.926

## xgb_context: top gain features

- replies_at_entry: 19.725
- is_native_launch: 17.385
- live_at_entry: 9.754
- market_recent_n: 4.636
- has_twitter: 4.383
- market_candidate_rate: 4.38
- twitter_is_status: 4.06
- name_dup_24h: 3.865
- description_len: 3.785
- hour_sin: 3.704
- image_dup_24h: 3.65
- market_recent_tp_rate: 3.514
- dow_cos: 3.349
- hour_cos: 3.329
- has_telegram: 3.139

## xgb_wallets: top gain features

- w_hit_rate_sol: 3.799
- w_scored_share: 3.716
- w_serial_share: 3.61
- w_hit_rate_mean: 3.532
- w_log_prior_mean: 3.522
- w_repeat_share: 3.497
- w_hit_rate_max: 3.452

## xgb_holders+wallets: top gain features

- dev_sold: 10.328
- dev_share: 8.572
- top3_share: 5.282
- launch_bundle_share: 4.906
- holders_n: 4.849
- gini_hold: 4.78
- top1_share: 4.776
- w_serial_share: 4.489
- buyers_n: 4.45
- w_hit_rate_max: 4.399
- w_scored_share: 4.359
- first_slot_share: 4.329
- w_repeat_share: 4.145
- exited_share: 4.142
- tokens_out_pct: 4.054

## xgb_all+wallets: top gain features

- is_native_launch: 29.147
- creator_prior_launches: 22.546
- creator_prior_resolved: 17.593
- replies_at_entry: 12.218
- dev_share: 11.672
- bundle_slots: 11.55
- sol_last60: 11.24
- holders_n: 10.735
- dow_cos: 9.824
- time_to_10_trades: 9.421
- exited_share: 9.158
- top1_share: 9.081
- market_recent_n: 8.868
- buy_ratio_count: 8.858
- gini_buy_size: 8.789

## xgb_botlive: top gain features

- dev_buy_sol: 13.6
- sol_last60: 5.668
- max_drawdown: 4.797
- top10_share: 4.485
- lows: 4.48
- trades_last60: 4.47
- run_from_low: 4.238
- decision_age_s: 4.164
- log_ret_window: 4.021
- lows_per_min: 3.939
- inflow_accel: 3.8
- curve_sol_in: 3.713
- sol_per_s_window: 3.705
- price_slope: 3.359

## xgb_botlive+context: top gain features

- is_native_launch: 28.219
- replies_at_entry: 18.185
- dev_buy_sol: 8.119
- sol_last60: 8.047
- market_recent_n: 7.862
- max_drawdown: 7.55
- trades_last60: 7.085
- name_dup_24h: 5.803
- market_candidate_rate: 5.713
- log_ret_window: 5.687
- top10_share: 5.598
- curve_sol_in: 5.473
- price_slope: 5.419
- has_twitter: 5.32
- run_from_low: 5.226
