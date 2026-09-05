# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 129 | 0.215 | 0.559 | 0.00 | 0.17 | 0.15 | -1.21 | -2.21 |
| xgb_holders | 129 | 0.217 | 0.556 | 0.00 | 0.17 | 0.23 | -0.66 | -2.27 |
| xgb_shape+holders | 129 | 0.211 | 0.545 | 0.00 | 0.17 | 0.08 | -1.94 | -2.36 |
| xgb_all | 129 | 0.236 | 0.602 | 0.00 | 0.33 | 0.31 | 0.29 | -1.34 |
| xgb_context | 129 | 0.164 | 0.460 | 0.00 | 0.00 | 0.08 | -1.51 | -2.05 |
| xgb_wallets | 129 | 0.222 | 0.507 | 0.00 | 0.17 | 0.38 | 1.35 | -0.25 |
| xgb_holders+wallets | 129 | 0.259 | 0.622 | 0.00 | 0.17 | 0.23 | -0.62 | -2.24 |
| xgb_all+wallets | 129 | 0.236 | 0.609 | 0.00 | 0.33 | 0.23 | -0.59 | -2.20 |
| xgb_botlive | 129 | 0.269 | 0.581 | 1.00 | 0.33 | 0.23 | -0.57 | -2.13 |
| xgb_botlive+context | 129 | 0.259 | 0.556 | 0.00 | 0.33 | 0.38 | 1.01 | -0.62 |
| xgb_pnl:all+wallets | 129 | 0.220 | 0.606 | 0.00 | 0.17 | 0.08 | -1.12 | -1.87 |
| xgb_pnl:botlive+context | 129 | 0.256 | 0.580 | 0.00 | 0.33 | 0.31 | 0.53 | -1.09 |
| logistic_repo_recipe | 129 | 0.208 | 0.547 | 0.00 | 0.17 | 0.15 | -1.37 | -2.23 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- sol_last60: 5.943
- sell_share_sol: 4.889
- bundle_slots: 4.858
- lows: 4.827
- iti_cv: 4.642
- dev_buy_sol: 4.598
- first_trade_t: 4.516
- max_drawdown: 4.491
- biggest_buy_vs_curve: 4.484
- buyers_last60: 4.383
- flipper_share: 4.383
- decision_age_s: 4.378
- n_slots: 4.344
- n_trades: 4.303
- gini_buy_size: 4.294

## xgb_holders: top gain features

- holders_n: 5.718
- top3_share: 5.402
- launch_bundle_share: 5.25
- dev_share: 5.203
- top1_share: 4.672
- first_slot_share: 4.558
- exited_share: 4.479
- top10_share: 4.344
- gini_hold: 4.107
- tokens_out_pct: 4.087
- same_size_share: 4.064
- buyers_n: 3.738
- dev_sold: 3.352

## xgb_shape+holders: top gain features

- sol_last60: 7.059
- top3_share: 5.623
- launch_bundle_share: 5.593
- top1_share: 5.472
- holders_n: 5.458
- lows_per_min: 5.095
- buyers_n: 5.0
- iti_cv: 4.91
- exited_share: 4.909
- buy_size_cv: 4.792
- bundle_slots: 4.766
- step_gini: 4.754
- decision_age_s: 4.72
- dev_share: 4.718
- buy_ratio_sol: 4.652

## xgb_all: top gain features

- creator_prior_resolved: 22.326
- is_native_launch: 16.05
- replies_at_entry: 13.559
- sol_last60: 9.462
- creator_prior_launches: 9.337
- lows: 9.232
- sell_share_sol: 8.131
- launch_bundle_share: 7.671
- top3_share: 7.455
- holders_n: 7.192
- exited_share: 6.894
- n_buyers: 6.789
- buy_size_cv: 6.755
- buyers_n: 6.704
- twitter_is_status: 6.699

## xgb_context: top gain features

- replies_at_entry: 27.317
- live_at_entry: 25.472
- is_native_launch: 12.578
- twitter_is_status: 4.722
- market_recent_n: 4.475
- has_twitter: 4.16
- description_len: 4.146
- dow_cos: 4.051
- market_candidate_rate: 4.034
- name_dup_24h: 3.876
- market_recent_tp_rate: 3.724
- hour_cos: 3.669
- image_dup_24h: 3.612
- hour_sin: 3.592
- has_telegram: 3.455

## xgb_wallets: top gain features

- w_log_prior_mean: 3.597
- w_hit_rate_mean: 3.56
- w_serial_share: 3.518
- w_hit_rate_max: 3.502
- w_hit_rate_sol: 3.429
- w_scored_share: 3.403
- w_repeat_share: 3.252

## xgb_holders+wallets: top gain features

- dev_sold: 5.943
- holders_n: 5.209
- launch_bundle_share: 4.886
- w_scored_share: 4.601
- first_slot_share: 4.539
- top1_share: 4.487
- dev_share: 4.479
- gini_hold: 4.461
- top3_share: 4.434
- w_hit_rate_mean: 4.372
- same_size_share: 4.316
- tokens_out_pct: 4.288
- w_serial_share: 4.276
- w_repeat_share: 4.056
- buyers_n: 4.02

## xgb_all+wallets: top gain features

- creator_prior_resolved: 17.444
- is_native_launch: 13.73
- replies_at_entry: 13.256
- creator_prior_launches: 9.499
- sol_last60: 8.003
- lows: 7.265
- decision_age_s: 7.257
- launch_bundle_share: 6.852
- exited_share: 6.847
- buy_size_cv: 6.801
- twitter_is_status: 6.693
- top3_share: 6.681
- dev_share: 6.551
- buyers_n: 6.415
- holders_n: 6.243

## xgb_botlive: top gain features

- bl_sol_last60: 5.433
- bl_top10_share: 4.806
- bl_price_slope: 4.262
- bl_trades_last60: 4.167
- bl_max_drawdown: 4.164
- bl_first_seen_sol: 4.162
- bl_dev_buy_sol: 3.918
- bl_curve_sol_in: 3.838
- bl_run_from_low: 3.744
- bl_lows_per_min: 3.667
- bl_log_ret_window: 3.621
- bl_decision_age_s: 3.542
- bl_sol_per_s_window: 3.349
- bl_inflow_accel: 3.235

## xgb_botlive+context: top gain features

- replies_at_entry: 26.188
- is_native_launch: 18.053
- bl_sol_last60: 7.519
- bl_run_from_low: 6.98
- bl_decision_age_s: 6.203
- market_candidate_rate: 6.103
- twitter_is_status: 6.008
- bl_first_seen_sol: 5.988
- market_recent_n: 5.984
- bl_top10_share: 5.92
- hour_cos: 5.914
- dow_cos: 5.522
- hour_sin: 5.504
- description_len: 5.459
- bl_log_ret_window: 5.191

## xgb_pnl:all+wallets: top gain features

- creator_prior_resolved: 4.131
- is_native_launch: 3.447
- replies_at_entry: 2.343
- creator_prior_launches: 2.219
- launch_bundle_share: 1.48
- iti_median: 1.414
- top3_share: 1.399
- holders_n: 1.304
- has_twitter: 1.278
- exited_share: 1.237
- sell_share_sol: 1.171
- gini_hold: 1.16
- buyers_last60: 1.148
- iti_std: 1.142
- iti_cv: 1.127

## xgb_pnl:botlive+context: top gain features

- replies_at_entry: 6.217
- is_native_launch: 3.446
- bl_decision_age_s: 1.316
- market_candidate_rate: 1.305
- has_twitter: 1.284
- bl_trades_last60: 1.265
- twitter_is_status: 1.204
- market_launch_rate: 1.174
- bl_top10_share: 1.168
- bl_run_from_low: 1.164
- market_recent_n: 1.162
- has_telegram: 1.134
- bl_first_seen_sol: 1.126
- description_len: 1.124
- image_dup_24h: 1.102
