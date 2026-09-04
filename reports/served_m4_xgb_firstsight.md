# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 617 | 0.251 | 0.639 | 0.00 | 0.29 | 0.26 | -1.04 | -2.72 |
| xgb_holders | 617 | 0.229 | 0.585 | 0.33 | 0.16 | 0.26 | -0.53 | -2.26 |
| xgb_shape+holders | 617 | 0.257 | 0.636 | 0.17 | 0.23 | 0.24 | -2.54 | -4.23 |
| xgb_all | 617 | 0.257 | 0.632 | 0.50 | 0.23 | 0.24 | -1.42 | -3.29 |
| xgb_context | 617 | 0.191 | 0.506 | 0.17 | 0.19 | 0.18 | -3.49 | -5.40 |
| xgb_wallets | 617 | 0.190 | 0.499 | 0.17 | 0.23 | 0.21 | -1.58 | -3.36 |
| xgb_holders+wallets | 617 | 0.239 | 0.581 | 0.33 | 0.23 | 0.19 | -2.87 | -4.56 |
| xgb_all+wallets | 617 | 0.274 | 0.625 | 0.50 | 0.32 | 0.32 | 2.60 | 0.80 |
| xgb_botlive | 617 | 0.238 | 0.593 | 0.00 | 0.26 | 0.29 | 0.63 | -1.22 |
| xgb_botlive+context | 617 | 0.262 | 0.550 | 0.50 | 0.39 | 0.34 | 2.61 | 0.70 |
| xgb_pnl:all+wallets | 617 | 0.243 | 0.586 | 0.50 | 0.26 | 0.23 | 2.78 | 1.09 |
| xgb_pnl:botlive+context | 617 | 0.222 | 0.536 | 0.33 | 0.26 | 0.26 | 0.16 | -1.70 |
| logistic_repo_recipe | 617 | 0.218 | 0.533 | 0.33 | 0.29 | 0.26 | -0.80 | -2.65 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- dev_buy_sol: 12.117
- max_drawdown: 9.976
- sell_share_sol: 9.3
- iti_median: 8.722
- sellers_last60: 8.17
- run_from_low: 8.038
- n_buyers: 7.853
- n_trades: 7.852
- trades_last60: 7.751
- sol_last60: 7.697
- flipper_share: 7.651
- buy_ratio_count: 7.235
- iti_std: 7.22
- decision_age_s: 7.038
- bundle_slots: 6.997

## xgb_holders: top gain features

- dev_share: 10.842
- dev_sold: 9.84
- top3_share: 9.412
- launch_bundle_share: 8.07
- top10_share: 7.971
- top1_share: 7.415
- first_slot_share: 6.307
- tokens_out_pct: 6.131
- exited_share: 5.721
- holders_n: 5.7
- gini_hold: 5.69
- same_size_share: 5.339
- buyers_n: 4.986

## xgb_shape+holders: top gain features

- dev_buy_sol: 16.779
- dev_sold: 15.132
- sell_share_sol: 14.912
- launch_bundle_share: 13.882
- dev_share: 13.154
- first_slot_share: 13.099
- top3_share: 12.624
- exited_share: 12.174
- run_from_low: 11.103
- iti_std: 10.925
- holders_n: 10.756
- decision_age_s: 10.406
- sol_last60: 9.978
- lows_per_min: 9.865
- top10_share: 9.642

## xgb_all: top gain features

- replies_at_entry: 48.536
- creator_prior_launches: 16.341
- is_native_launch: 15.635
- buyers_n: 14.176
- decision_age_s: 12.141
- lows: 10.58
- launch_bundle_share: 10.567
- sol_last60: 10.242
- exited_share: 9.926
- top3_share: 9.798
- creator_prior_tp_rate: 9.618
- top10_share: 9.281
- last_trade_t: 9.056
- trades_last60: 9.03
- lows_per_min: 8.654

## xgb_context: top gain features

- replies_at_entry: 21.724
- is_native_launch: 13.196
- live_at_entry: 13.064
- image_dup_24h: 5.937
- hour_sin: 5.467
- name_dup_24h: 5.422
- market_candidate_rate: 5.347
- market_recent_n: 5.233
- has_twitter: 4.985
- market_recent_tp_rate: 4.742
- description_len: 4.535
- dow_sin: 4.438
- market_launch_rate: 4.402
- has_website: 4.176
- hour_cos: 4.135

## xgb_wallets: top gain features

- w_repeat_share: 3.398
- w_log_prior_mean: 3.288
- w_scored_share: 3.06
- w_hit_rate_sol: 3.036
- w_hit_rate_mean: 3.012
- w_serial_share: 2.898
- w_hit_rate_max: 2.699

## xgb_holders+wallets: top gain features

- dev_share: 8.194
- top3_share: 7.823
- launch_bundle_share: 6.842
- dev_sold: 6.633
- top10_share: 6.021
- w_log_prior_mean: 5.865
- top1_share: 5.78
- holders_n: 5.686
- tokens_out_pct: 5.485
- w_repeat_share: 5.44
- w_scored_share: 5.363
- first_slot_share: 5.295
- exited_share: 5.276
- w_hit_rate_sol: 5.052
- same_size_share: 4.866

## xgb_all+wallets: top gain features

- replies_at_entry: 16.091
- is_native_launch: 11.598
- launch_bundle_share: 8.965
- creator_prior_launches: 8.806
- buyers_n: 8.274
- iti_median: 7.983
- exited_share: 7.563
- top10_share: 7.086
- lows: 7.08
- dev_share: 7.027
- last_trade_t: 6.965
- trades_last60: 6.828
- decision_age_s: 6.403
- creator_prior_tp_rate: 6.301
- top1_share: 6.265

## xgb_botlive: top gain features

- bl_dev_buy_sol: 10.857
- bl_top10_share: 5.658
- bl_sol_last60: 5.307
- bl_curve_sol_in: 4.591
- bl_log_ret_window: 4.586
- bl_run_from_low: 4.584
- bl_inflow_accel: 4.234
- bl_sol_per_s_window: 3.841
- bl_decision_age_s: 3.75
- bl_first_seen_sol: 3.443
- bl_price_slope: 2.918
- bl_trades_last60: 2.818

## xgb_botlive+context: top gain features

- replies_at_entry: 25.286
- is_native_launch: 14.874
- twitter_is_status: 11.231
- bl_sol_last60: 9.569
- live_at_entry: 9.239
- dow_cos: 8.793
- bl_dev_buy_sol: 8.634
- has_telegram: 8.398
- bl_curve_sol_in: 8.018
- bl_first_seen_sol: 7.67
- bl_top10_share: 7.201
- hour_sin: 7.198
- market_candidate_rate: 7.176
- market_recent_n: 7.024
- bl_log_ret_window: 6.855

## xgb_pnl:all+wallets: top gain features

- dev_share: 3.767
- launch_bundle_share: 2.825
- is_native_launch: 2.731
- dev_buy_sol: 2.484
- replies_at_entry: 2.355
- creator_prior_launches: 2.174
- top10_share: 1.931
- lows: 1.803
- tokens_out_pct: 1.777
- gini_hold: 1.609
- holders_n: 1.593
- buy_size_cv: 1.576
- iti_median: 1.547
- trades_last60: 1.537
- sellers_last60: 1.534

## xgb_pnl:botlive+context: top gain features

- replies_at_entry: 4.4
- bl_dev_buy_sol: 2.713
- bl_sol_last60: 2.578
- live_at_entry: 2.486
- is_native_launch: 2.204
- twitter_is_status: 2.002
- bl_top10_share: 1.582
- has_telegram: 1.535
- bl_first_seen_sol: 1.509
- bl_curve_sol_in: 1.498
- bl_log_ret_window: 1.493
- image_dup_24h: 1.388
- name_dup_24h: 1.355
- description_len: 1.351
- bl_sol_per_s_window: 1.344
