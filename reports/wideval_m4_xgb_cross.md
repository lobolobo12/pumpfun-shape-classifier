# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 612 | 0.296 | 0.641 | 0.50 | 0.32 | 0.39 | 5.82 | 3.65 |
| xgb_holders | 612 | 0.254 | 0.576 | 0.50 | 0.29 | 0.28 | 0.18 | -1.87 |
| xgb_shape+holders | 612 | 0.260 | 0.587 | 0.17 | 0.35 | 0.33 | 2.79 | 0.65 |
| xgb_all | 612 | 0.291 | 0.595 | 0.50 | 0.48 | 0.36 | 5.31 | 3.15 |
| xgb_context | 612 | 0.223 | 0.549 | 0.17 | 0.29 | 0.28 | 1.09 | -0.58 |
| xgb_wallets | 612 | 0.233 | 0.541 | 0.33 | 0.32 | 0.30 | 2.66 | 0.75 |
| xgb_holders+wallets | 612 | 0.273 | 0.598 | 0.33 | 0.35 | 0.34 | 3.63 | 1.54 |
| xgb_all+wallets | 612 | 0.292 | 0.597 | 0.67 | 0.48 | 0.34 | 4.48 | 2.33 |
| xgb_botlive | 612 | 0.234 | 0.539 | 0.33 | 0.23 | 0.34 | 3.57 | 1.34 |
| xgb_botlive+context | 612 | 0.241 | 0.557 | 0.33 | 0.32 | 0.25 | -0.56 | -2.28 |
| xgb_pnl:all+wallets | 612 | 0.249 | 0.591 | 0.33 | 0.39 | 0.31 | 3.70 | 1.57 |
| xgb_pnl:botlive+context | 612 | 0.199 | 0.536 | 0.33 | 0.16 | 0.13 | -3.88 | -5.67 |
| logistic_repo_recipe | 612 | 0.256 | 0.586 | 0.67 | 0.29 | 0.25 | -1.14 | -2.85 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- dev_buy_sol: 24.693
- max_drawdown: 9.922
- decision_age_s: 6.933
- sol_last60: 6.846
- buyers_last60: 6.372
- n_sellers: 6.273
- flipper_share: 6.198
- iti_median: 6.165
- trades_last60: 6.08
- first_trade_t: 5.973
- gini_buy_size: 5.86
- lows: 5.792
- n_trades: 5.731
- inflow_accel: 5.426
- biggest_buy_vs_curve: 5.387

## xgb_holders: top gain features

- dev_sold: 12.429
- dev_share: 11.352
- holders_n: 5.174
- tokens_out_pct: 4.595
- launch_bundle_share: 4.572
- top1_share: 4.568
- first_slot_share: 4.566
- top3_share: 4.448
- exited_share: 3.964
- gini_hold: 3.813
- top10_share: 3.641
- buyers_n: 3.63
- same_size_share: 3.323

## xgb_shape+holders: top gain features

- dev_buy_sol: 18.819
- dev_sold: 15.656
- dev_share: 11.947
- max_drawdown: 9.338
- holders_n: 9.307
- buy_size_cv: 7.936
- top3_share: 7.479
- n_sellers: 6.893
- sol_last60: 6.84
- trades_last60: 6.787
- bundle_slots: 6.739
- buy_ratio_count: 6.699
- step_gini: 6.56
- exited_share: 6.399
- first_slot_share: 5.97

## xgb_all: top gain features

- creator_prior_resolved: 31.387
- is_native_launch: 30.633
- replies_at_entry: 25.361
- creator_prior_launches: 14.99
- max_drawdown: 10.413
- twitter_is_status: 10.246
- dev_share: 8.871
- sell_share_sol: 8.626
- holders_n: 7.862
- sol_last60: 7.376
- first_slot_share: 7.036
- top1_share: 6.895
- exited_share: 6.818
- top3_share: 6.601
- iti_median: 6.582

## xgb_context: top gain features

- live_at_entry: 31.658
- replies_at_entry: 25.456
- is_native_launch: 21.417
- has_telegram: 6.018
- twitter_is_status: 5.378
- has_twitter: 4.619
- market_candidate_rate: 4.386
- hour_sin: 4.114
- market_recent_n: 4.025
- market_recent_tp_rate: 3.842
- name_dup_24h: 3.661
- market_launch_rate: 3.65
- image_dup_24h: 3.555
- description_len: 3.376
- dow_sin: 2.773

## xgb_wallets: top gain features

- w_repeat_share: 4.568
- w_scored_share: 3.927
- w_hit_rate_sol: 3.922
- w_hit_rate_mean: 3.563
- w_log_prior_mean: 3.45
- w_serial_share: 3.437
- w_hit_rate_max: 3.207

## xgb_holders+wallets: top gain features

- dev_sold: 11.615
- dev_share: 9.987
- holders_n: 5.842
- launch_bundle_share: 5.016
- top3_share: 4.855
- tokens_out_pct: 4.741
- w_serial_share: 4.657
- exited_share: 4.654
- w_scored_share: 4.638
- top1_share: 4.576
- w_log_prior_mean: 4.514
- w_repeat_share: 4.469
- w_hit_rate_mean: 4.398
- top10_share: 4.375
- first_slot_share: 4.217

## xgb_all+wallets: top gain features

- creator_prior_resolved: 38.973
- is_native_launch: 30.181
- replies_at_entry: 20.043
- creator_prior_launches: 19.328
- max_drawdown: 9.486
- live_at_entry: 9.202
- top3_share: 9.117
- dev_share: 8.826
- twitter_is_status: 8.427
- w_repeat_share: 8.085
- creator_prior_tp_rate: 8.011
- dev_buy_sol: 7.689
- sellers_last60: 7.382
- has_twitter: 7.376
- decision_age_s: 7.262

## xgb_botlive: top gain features

- bl_dev_buy_sol: 11.779
- bl_first_seen_sol: 3.467
- bl_sol_last60: 3.452
- bl_max_drawdown: 3.428
- bl_decision_age_s: 3.421
- bl_curve_sol_in: 3.269
- bl_price_slope: 3.265
- bl_trades_last60: 3.251
- bl_run_from_low: 3.074
- bl_top10_share: 3.019
- bl_log_ret_window: 3.011
- bl_inflow_accel: 2.812
- bl_sol_per_s_window: 2.552
- bl_lows_per_min: 2.311

## xgb_botlive+context: top gain features

- is_native_launch: 28.126
- replies_at_entry: 20.65
- bl_dev_buy_sol: 6.213
- has_twitter: 5.985
- twitter_is_status: 5.779
- market_candidate_rate: 5.35
- name_dup_24h: 5.118
- hour_sin: 4.939
- bl_lows_per_min: 4.839
- market_launch_rate: 4.8
- market_recent_n: 4.787
- bl_run_from_low: 4.775
- bl_sol_per_s_window: 4.711
- bl_inflow_accel: 4.667
- market_recent_tp_rate: 4.665

## xgb_pnl:all+wallets: top gain features

- creator_prior_resolved: 10.45
- is_native_launch: 5.28
- creator_prior_launches: 4.816
- first_trade_t: 2.231
- has_twitter: 2.145
- price_slope: 2.085
- w_repeat_share: 2.054
- creator_prior_tp_rate: 2.017
- max_drawdown: 1.946
- dev_share: 1.74
- gini_hold: 1.719
- flipper_share: 1.667
- lows_per_min: 1.637
- w_hit_rate_max: 1.634
- w_serial_share: 1.633

## xgb_pnl:botlive+context: top gain features

- is_native_launch: 8.901
- replies_at_entry: 5.144
- market_recent_n: 2.07
- has_twitter: 1.721
- market_candidate_rate: 1.719
- bl_dev_buy_sol: 1.684
- name_dup_24h: 1.585
- bl_lows: 1.504
- bl_decision_age_s: 1.421
- description_len: 1.387
- twitter_is_status: 1.321
- dow_sin: 1.308
- bl_sol_per_s_window: 1.28
- bl_price_slope: 1.265
- bl_first_seen_sol: 1.265
