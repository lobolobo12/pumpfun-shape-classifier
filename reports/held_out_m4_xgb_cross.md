# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 460 | 0.300 | 0.638 | 0.60 | 0.35 | 0.33 | 2.67 | 0.50 |
| xgb_holders | 460 | 0.257 | 0.599 | 0.60 | 0.26 | 0.28 | 0.85 | -1.27 |
| xgb_shape+holders | 460 | 0.279 | 0.597 | 0.40 | 0.39 | 0.33 | 2.59 | 0.42 |
| xgb_all | 460 | 0.303 | 0.616 | 0.60 | 0.48 | 0.39 | 5.03 | 2.86 |
| xgb_context | 460 | 0.241 | 0.578 | 0.60 | 0.22 | 0.26 | -0.13 | -1.96 |
| xgb_wallets | 460 | 0.204 | 0.553 | 0.00 | 0.26 | 0.22 | -0.82 | -2.55 |
| xgb_holders+wallets | 460 | 0.260 | 0.614 | 0.40 | 0.26 | 0.30 | 1.99 | -0.13 |
| xgb_all+wallets | 460 | 0.342 | 0.632 | 0.80 | 0.52 | 0.46 | 7.03 | 4.86 |
| xgb_botlive | 460 | 0.261 | 0.577 | 0.60 | 0.26 | 0.30 | 2.00 | -0.17 |
| logistic_repo_recipe | 460 | 0.233 | 0.548 | 0.60 | 0.22 | 0.22 | -2.09 | -3.78 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- dev_buy_sol: 10.514
- bundle_slots: 6.916
- lows: 6.786
- sol_last60: 6.042
- flipper_share: 5.9
- max_drawdown: 5.722
- n_sellers: 5.601
- trades_last60: 5.463
- buyers_last60: 5.393
- buy_ratio_count: 5.196
- gini_buy_size: 5.169
- iti_cv: 5.034
- n_trades: 4.91
- first_trade_t: 4.907
- price_slope: 4.877

## xgb_holders: top gain features

- dev_sold: 10.1
- dev_share: 9.152
- top1_share: 5.15
- top3_share: 4.899
- holders_n: 4.862
- launch_bundle_share: 4.756
- first_slot_share: 4.424
- top10_share: 4.375
- exited_share: 4.006
- gini_hold: 3.983
- tokens_out_pct: 3.964
- same_size_share: 3.794
- buyers_n: 3.704

## xgb_shape+holders: top gain features

- dev_sold: 16.94
- dev_buy_sol: 11.933
- dev_share: 10.538
- top3_share: 7.811
- holders_n: 7.811
- sol_last60: 7.275
- bundle_slots: 7.248
- top1_share: 7.178
- buy_size_cv: 6.63
- buy_ratio_count: 6.058
- launch_bundle_share: 5.999
- buy_ratio_sol: 5.844
- n_slots: 5.78
- max_drawdown: 5.677
- exited_share: 5.677

## xgb_all: top gain features

- is_native_launch: 27.929
- creator_prior_resolved: 17.601
- creator_prior_launches: 16.388
- sol_last60: 11.147
- gini_buy_size: 10.112
- holders_n: 9.723
- dow_cos: 9.69
- launch_bundle_share: 9.657
- max_drawdown: 9.075
- top3_share: 8.933
- top1_share: 8.774
- n_buyers: 8.293
- buy_size_cv: 8.171
- first_trade_t: 8.089
- exited_share: 7.905

## xgb_context: top gain features

- replies_at_entry: 25.776
- is_native_launch: 16.242
- live_at_entry: 12.945
- has_twitter: 4.744
- market_recent_n: 4.743
- dow_cos: 4.724
- name_dup_24h: 4.382
- market_candidate_rate: 4.192
- description_len: 4.119
- market_recent_tp_rate: 3.93
- hour_sin: 3.89
- twitter_is_status: 3.886
- image_dup_24h: 3.741
- hour_cos: 3.354
- dow_sin: 3.295

## xgb_wallets: top gain features

- w_repeat_share: 3.159
- w_scored_share: 3.027
- w_hit_rate_sol: 2.994
- w_hit_rate_max: 2.976
- w_log_prior_mean: 2.975
- w_serial_share: 2.957
- w_hit_rate_mean: 2.867

## xgb_holders+wallets: top gain features

- dev_sold: 13.188
- dev_share: 12.357
- top3_share: 7.648
- launch_bundle_share: 6.68
- gini_hold: 6.628
- holders_n: 6.364
- top1_share: 6.159
- tokens_out_pct: 5.713
- w_repeat_share: 5.465
- w_serial_share: 5.347
- same_size_share: 5.247
- first_slot_share: 5.212
- w_hit_rate_sol: 5.195
- exited_share: 5.144
- w_scored_share: 5.102

## xgb_all+wallets: top gain features

- is_native_launch: 18.261
- creator_prior_launches: 5.63
- bundle_slots: 5.562
- top3_share: 5.37
- dev_share: 5.247
- launch_bundle_share: 5.191
- top1_share: 5.168
- sol_last60: 4.898
- buy_size_cv: 4.819
- live_at_entry: 4.623
- twitter_is_status: 4.597
- sell_share_sol: 4.526
- iti_std: 4.456
- exited_share: 4.431
- dev_buy_sol: 4.43

## xgb_botlive: top gain features

- dev_share: 10.943
- holders_n: 6.502
- sol_last60: 5.935
- max_drawdown: 4.805
- run_from_low: 4.759
- log_ret_window: 4.661
- price_slope: 4.573
- lows_per_min: 4.563
- decision_age_s: 4.554
- curve_sol_in: 4.283
- top10_share: 4.226
- trades_last60: 4.051
- inflow_accel: 3.997
- sol_per_s_window: 3.991
- lows: 3.74
