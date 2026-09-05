# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 129 | 0.272 | 0.621 | 1.00 | 0.33 | 0.23 | -0.51 | -2.04 |
| xgb_holders | 129 | 0.293 | 0.585 | 1.00 | 0.33 | 0.38 | 0.58 | -1.02 |
| xgb_shape+holders | 129 | 0.253 | 0.567 | 1.00 | 0.33 | 0.15 | -1.38 | -2.38 |
| xgb_all | 129 | 0.237 | 0.579 | 0.00 | 0.33 | 0.23 | -0.60 | -2.21 |
| xgb_context | 129 | 0.164 | 0.462 | 0.00 | 0.00 | 0.08 | -1.51 | -2.05 |
| xgb_wallets | 129 | 0.222 | 0.507 | 0.00 | 0.17 | 0.38 | 1.35 | -0.25 |
| xgb_holders+wallets | 129 | 0.296 | 0.658 | 0.00 | 0.17 | 0.31 | -0.06 | -1.69 |
| xgb_all+wallets | 129 | 0.234 | 0.619 | 0.00 | 0.33 | 0.23 | -0.58 | -2.19 |
| xgb_botlive | 129 | 0.295 | 0.589 | 1.00 | 0.33 | 0.38 | 0.96 | -0.67 |
| xgb_botlive+context | 129 | 0.239 | 0.559 | 0.00 | 0.33 | 0.31 | 0.21 | -1.42 |
| xgb_pnl:all+wallets | 129 | 0.221 | 0.606 | 0.00 | 0.00 | 0.23 | 0.20 | -1.39 |
| xgb_pnl:botlive+context | 129 | 0.271 | 0.604 | 0.00 | 0.33 | 0.31 | 0.42 | -1.20 |
| logistic_repo_recipe | 129 | 0.317 | 0.663 | 0.00 | 0.50 | 0.31 | 0.09 | -1.49 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- dev_buy_sol: 20.661
- sell_share_sol: 10.346
- trades_last60: 8.829
- sol_last60: 8.799
- lows: 8.275
- max_drawdown: 7.797
- buyers_last60: 7.017
- n_trades: 6.963
- buy_ratio_count: 6.747
- buy_size_cv: 6.702
- n_slots: 6.612
- run_from_low: 6.561
- flipper_share: 6.243
- last_trade_t: 6.143
- n_buyers: 6.005

## xgb_holders: top gain features

- dev_sold: 8.195
- dev_share: 7.495
- top3_share: 4.664
- top1_share: 4.398
- launch_bundle_share: 4.125
- holders_n: 3.906
- exited_share: 3.871
- tokens_out_pct: 3.643
- same_size_share: 3.591
- first_slot_share: 3.563
- gini_hold: 3.549
- buyers_n: 3.522
- top10_share: 3.479

## xgb_shape+holders: top gain features

- dev_sold: 10.43
- dev_buy_sol: 8.128
- dev_share: 7.597
- top3_share: 6.636
- sol_last60: 5.814
- launch_bundle_share: 5.644
- buy_size_cv: 5.486
- top1_share: 5.412
- lows_per_min: 5.011
- sell_share_sol: 4.918
- max_drawdown: 4.766
- exited_share: 4.734
- gini_hold: 4.614
- first_trade_t: 4.565
- lows: 4.55

## xgb_all: top gain features

- creator_prior_resolved: 19.256
- is_native_launch: 13.394
- sol_last60: 8.046
- creator_prior_launches: 6.825
- holders_n: 6.767
- dev_share: 6.585
- replies_at_entry: 6.276
- top3_share: 6.208
- live_at_entry: 6.067
- launch_bundle_share: 6.057
- exited_share: 6.048
- sell_share_sol: 5.909
- buy_ratio_count: 5.826
- lows: 5.823
- buy_size_cv: 5.757

## xgb_context: top gain features

- replies_at_entry: 27.303
- live_at_entry: 25.459
- is_native_launch: 12.56
- twitter_is_status: 4.738
- market_recent_n: 4.426
- has_twitter: 4.396
- description_len: 4.134
- dow_cos: 4.055
- market_candidate_rate: 4.001
- name_dup_24h: 3.827
- market_recent_tp_rate: 3.754
- hour_cos: 3.741
- hour_sin: 3.592
- image_dup_24h: 3.544
- has_telegram: 3.46

## xgb_wallets: top gain features

- w_log_prior_mean: 3.597
- w_hit_rate_mean: 3.56
- w_serial_share: 3.518
- w_hit_rate_max: 3.502
- w_hit_rate_sol: 3.429
- w_scored_share: 3.403
- w_repeat_share: 3.252

## xgb_holders+wallets: top gain features

- dev_share: 14.354
- dev_sold: 12.941
- top3_share: 7.545
- launch_bundle_share: 6.488
- gini_hold: 6.394
- w_scored_share: 6.201
- top1_share: 6.045
- holders_n: 5.976
- w_hit_rate_mean: 5.956
- exited_share: 5.663
- tokens_out_pct: 5.464
- buyers_n: 5.296
- w_serial_share: 5.082
- first_slot_share: 4.955
- w_log_prior_mean: 4.737

## xgb_all+wallets: top gain features

- creator_prior_resolved: 22.887
- is_native_launch: 14.583
- creator_prior_launches: 12.901
- sol_last60: 9.732
- buyers_n: 9.049
- twitter_is_status: 8.969
- dev_buy_sol: 8.414
- holders_n: 8.288
- decision_age_s: 8.014
- launch_bundle_share: 7.956
- dev_share: 7.82
- exited_share: 7.76
- buy_size_cv: 7.684
- top3_share: 7.443
- lows: 7.29

## xgb_botlive: top gain features

- bl_dev_buy_sol: 14.755
- bl_sol_last60: 5.533
- bl_top10_share: 4.721
- bl_first_seen_sol: 4.538
- bl_trades_last60: 4.311
- bl_decision_age_s: 3.781
- bl_run_from_low: 3.59
- bl_price_slope: 3.459
- bl_sol_per_s_window: 3.418
- bl_curve_sol_in: 3.221
- bl_lows_per_min: 3.01
- bl_max_drawdown: 2.699
- bl_log_ret_window: 2.689
- bl_inflow_accel: 2.169

## xgb_botlive+context: top gain features

- replies_at_entry: 25.736
- is_native_launch: 18.548
- live_at_entry: 10.004
- bl_sol_last60: 8.579
- bl_dev_buy_sol: 7.719
- bl_run_from_low: 6.859
- market_candidate_rate: 6.218
- market_recent_n: 6.113
- bl_top10_share: 6.066
- bl_first_seen_sol: 5.978
- hour_sin: 5.693
- twitter_is_status: 5.413
- name_dup_24h: 5.373
- hour_cos: 5.297
- description_len: 5.284

## xgb_pnl:all+wallets: top gain features

- creator_prior_resolved: 7.244
- is_native_launch: 4.02
- replies_at_entry: 3.19
- creator_prior_launches: 3.028
- iti_median: 2.214
- top3_share: 1.989
- holders_n: 1.853
- launch_bundle_share: 1.805
- gini_hold: 1.659
- exited_share: 1.657
- time_to_10_trades: 1.638
- dow_cos: 1.578
- w_hit_rate_sol: 1.576
- largest_buy_share: 1.558
- sell_share_sol: 1.558

## xgb_pnl:botlive+context: top gain features

- replies_at_entry: 6.696
- is_native_launch: 3.219
- twitter_is_status: 1.29
- has_twitter: 1.287
- bl_dev_buy_sol: 1.238
- dow_cos: 1.214
- market_candidate_rate: 1.2
- bl_decision_age_s: 1.192
- market_recent_n: 1.188
- bl_top10_share: 1.184
- name_dup_24h: 1.152
- image_dup_24h: 1.113
- description_len: 1.085
- bl_run_from_low: 1.079
- bl_first_seen_sol: 1.077
