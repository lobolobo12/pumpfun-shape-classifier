# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 612 | 0.302 | 0.644 | 0.50 | 0.35 | 0.36 | 4.13 | 1.98 |
| xgb_holders | 612 | 0.271 | 0.593 | 0.33 | 0.42 | 0.33 | 2.47 | 0.44 |
| xgb_shape+holders | 612 | 0.282 | 0.624 | 0.50 | 0.35 | 0.36 | 4.30 | 2.14 |
| xgb_all | 612 | 0.319 | 0.632 | 0.83 | 0.45 | 0.41 | 6.55 | 4.39 |
| xgb_context | 612 | 0.228 | 0.538 | 0.17 | 0.35 | 0.26 | -0.03 | -1.78 |
| xgb_wallets | 612 | 0.208 | 0.538 | 0.17 | 0.29 | 0.26 | 0.79 | -0.99 |
| xgb_holders+wallets | 612 | 0.275 | 0.597 | 0.33 | 0.32 | 0.41 | 6.26 | 4.14 |
| xgb_all+wallets | 612 | 0.317 | 0.642 | 0.67 | 0.45 | 0.41 | 6.77 | 4.61 |
| xgb_botlive | 612 | 0.240 | 0.559 | 0.33 | 0.23 | 0.26 | 0.13 | -2.07 |
| xgb_botlive+context | 612 | 0.298 | 0.609 | 0.67 | 0.48 | 0.38 | 5.54 | 3.38 |
| xgb_pnl:all+wallets | 612 | 0.266 | 0.625 | 0.50 | 0.29 | 0.31 | 3.83 | 1.80 |
| xgb_pnl:botlive+context | 612 | 0.238 | 0.594 | 0.33 | 0.19 | 0.21 | 1.36 | -0.76 |
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

- creator_prior_resolved: 36.042
- is_native_launch: 29.11
- replies_at_entry: 24.972
- creator_prior_launches: 16.576
- holders_n: 11.909
- sol_last60: 11.451
- bundle_slots: 10.592
- max_drawdown: 10.2
- launch_bundle_share: 9.67
- dev_share: 9.293
- buy_size_cv: 9.291
- first_trade_t: 9.204
- top1_share: 8.551
- time_to_10_trades: 7.906
- exited_share: 7.878

## xgb_context: top gain features

- replies_at_entry: 19.674
- is_native_launch: 16.929
- live_at_entry: 9.569
- market_recent_n: 4.566
- market_candidate_rate: 4.463
- has_twitter: 4.368
- twitter_is_status: 4.04
- description_len: 3.868
- name_dup_24h: 3.858
- image_dup_24h: 3.648
- hour_sin: 3.642
- has_telegram: 3.588
- market_recent_tp_rate: 3.511
- hour_cos: 3.384
- dow_cos: 3.151

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

- is_native_launch: 29.209
- creator_prior_launches: 21.918
- creator_prior_resolved: 18.674
- replies_at_entry: 12.317
- dev_share: 11.617
- sol_last60: 10.93
- sell_share_sol: 10.287
- bundle_slots: 10.175
- holders_n: 9.924
- dow_cos: 9.824
- buy_ratio_count: 9.549
- time_to_10_trades: 9.48
- market_recent_n: 9.141
- exited_share: 9.087
- twitter_is_status: 8.882

## xgb_botlive: top gain features

- bl_dev_buy_sol: 17.22
- bl_sol_last60: 5.107
- bl_top10_share: 4.642
- bl_inflow_accel: 4.208
- bl_log_ret_window: 3.704
- bl_decision_age_s: 3.37
- bl_price_slope: 3.361
- bl_lows_per_min: 3.315
- bl_run_from_low: 3.273
- bl_trades_last60: 3.254
- bl_first_seen_sol: 3.205
- bl_sol_per_s_window: 3.072
- bl_curve_sol_in: 2.489
- bl_max_drawdown: 2.272
- bl_lows: 1.122

## xgb_botlive+context: top gain features

- is_native_launch: 25.15
- replies_at_entry: 12.817
- bl_sol_last60: 7.396
- bl_dev_buy_sol: 7.197
- market_recent_n: 6.821
- dow_cos: 6.54
- twitter_is_status: 5.913
- name_dup_24h: 5.512
- description_len: 5.364
- market_candidate_rate: 5.266
- bl_run_from_low: 5.165
- bl_top10_share: 5.161
- bl_log_ret_window: 5.132
- hour_sin: 4.855
- has_twitter: 4.83

## xgb_pnl:all+wallets: top gain features

- is_native_launch: 4.449
- creator_prior_resolved: 3.537
- creator_prior_launches: 2.821
- replies_at_entry: 2.403
- top3_share: 1.538
- has_twitter: 1.527
- first_trade_t: 1.462
- launch_bundle_share: 1.375
- exited_share: 1.279
- dev_buy_sol: 1.272
- creator_prior_tp_rate: 1.241
- iti_cv: 1.232
- lows: 1.218
- top1_share: 1.209
- largest_buy_share: 1.203

## xgb_pnl:botlive+context: top gain features

- is_native_launch: 5.51
- replies_at_entry: 4.744
- has_twitter: 1.694
- bl_dev_buy_sol: 1.619
- market_recent_n: 1.406
- market_candidate_rate: 1.388
- twitter_is_status: 1.351
- has_telegram: 1.347
- bl_decision_age_s: 1.334
- has_website: 1.327
- bl_sol_per_s_window: 1.319
- image_dup_24h: 1.282
- description_len: 1.256
- bl_sol_last60: 1.249
- market_launch_rate: 1.227
