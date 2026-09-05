# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 138 | 0.197 | 0.516 | 0.00 | 0.14 | 0.21 | -1.02 | -2.57 |
| xgb_holders | 138 | 0.260 | 0.568 | 0.00 | 0.43 | 0.29 | -0.35 | -1.96 |
| xgb_shape+holders | 138 | 0.194 | 0.516 | 0.00 | 0.14 | 0.14 | -1.47 | -2.49 |
| xgb_all | 138 | 0.200 | 0.553 | 0.00 | 0.00 | 0.07 | -2.36 | -2.65 |
| xgb_context | 138 | 0.202 | 0.512 | 0.00 | 0.14 | 0.21 | -0.07 | -1.67 |
| xgb_wallets | 138 | 0.231 | 0.509 | 0.00 | 0.29 | 0.36 | 0.68 | -0.92 |
| xgb_holders+wallets | 138 | 0.244 | 0.552 | 0.00 | 0.14 | 0.21 | -1.07 | -2.61 |
| xgb_all+wallets | 138 | 0.200 | 0.545 | 0.00 | 0.14 | 0.07 | -2.36 | -2.64 |
| xgb_botlive | 138 | 0.272 | 0.558 | 0.00 | 0.43 | 0.36 | 0.39 | -1.20 |
| xgb_botlive+context | 138 | 0.250 | 0.533 | 0.00 | 0.29 | 0.29 | -0.15 | -1.78 |
| xgb_pnl:all+wallets | 138 | 0.208 | 0.559 | 0.00 | 0.14 | 0.21 | -0.81 | -2.35 |
| xgb_pnl:botlive+context | 138 | 0.296 | 0.588 | 0.00 | 0.29 | 0.43 | 1.87 | 0.29 |
| logistic_repo_recipe | 138 | 0.227 | 0.601 | 0.00 | 0.00 | 0.21 | -0.42 | -2.00 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- bundle_slots: 8.192
- buyers_last60: 6.778
- sol_last60: 6.59
- n_trades: 5.994
- iti_median: 5.817
- trades_last60: 5.681
- decision_age_s: 5.562
- n_slots: 5.463
- iti_cv: 5.416
- max_drawdown: 5.297
- last_trade_t: 5.295
- price_slope: 5.261
- inflow_accel: 5.213
- flipper_share: 5.115
- sell_share_sol: 5.048

## xgb_holders: top gain features

- holders_n: 6.109
- launch_bundle_share: 5.655
- dev_share: 5.382
- top10_share: 4.925
- first_slot_share: 4.858
- dev_sold: 4.528
- top3_share: 4.391
- gini_hold: 4.391
- same_size_share: 4.381
- top1_share: 4.269
- tokens_out_pct: 4.183
- exited_share: 3.773
- buyers_n: 3.525

## xgb_shape+holders: top gain features

- holders_n: 8.739
- bundle_slots: 7.663
- top10_share: 7.185
- iti_median: 7.027
- sol_last60: 6.932
- launch_bundle_share: 6.74
- last_trade_t: 6.625
- decision_age_s: 6.148
- n_trades: 6.091
- top3_share: 6.055
- buyers_last60: 6.05
- top1_share: 6.037
- iti_cv: 5.972
- sellers_last60: 5.948
- first_slot_share: 5.916

## xgb_all: top gain features

- creator_prior_resolved: 26.648
- is_native_launch: 15.071
- creator_prior_launches: 12.986
- replies_at_entry: 11.948
- buyers_last60: 11.885
- holders_n: 11.862
- sol_last60: 10.61
- decision_age_s: 10.076
- iti_median: 8.992
- top10_share: 8.625
- launch_bundle_share: 8.53
- dev_share: 8.406
- first_slot_share: 8.391
- name_dup_24h: 8.274
- has_twitter: 8.242

## xgb_context: top gain features

- replies_at_entry: 31.532
- live_at_entry: 19.821
- is_native_launch: 10.698
- market_recent_n: 6.415
- has_telegram: 5.779
- market_candidate_rate: 5.322
- dow_cos: 5.181
- name_dup_24h: 4.904
- has_twitter: 4.893
- description_len: 4.725
- image_dup_24h: 4.352
- market_recent_tp_rate: 4.023
- has_website: 4.018
- dow_sin: 3.986
- hour_cos: 3.933

## xgb_wallets: top gain features

- w_repeat_share: 5.102
- w_hit_rate_sol: 4.483
- w_scored_share: 4.23
- w_hit_rate_max: 4.065
- w_hit_rate_mean: 4.031
- w_serial_share: 3.813
- w_log_prior_mean: 3.623

## xgb_holders+wallets: top gain features

- holders_n: 7.094
- top10_share: 6.424
- launch_bundle_share: 5.785
- dev_share: 5.451
- first_slot_share: 5.284
- w_repeat_share: 5.283
- tokens_out_pct: 5.061
- w_hit_rate_mean: 4.969
- w_hit_rate_sol: 4.932
- exited_share: 4.917
- w_log_prior_mean: 4.856
- w_serial_share: 4.84
- same_size_share: 4.833
- top1_share: 4.754
- w_scored_share: 4.747

## xgb_all+wallets: top gain features

- creator_prior_resolved: 21.562
- is_native_launch: 13.444
- replies_at_entry: 11.239
- holders_n: 10.4
- buyers_last60: 8.955
- dev_sold: 8.563
- has_telegram: 8.186
- sol_last60: 8.077
- launch_bundle_share: 7.511
- exited_share: 6.737
- top1_share: 6.73
- top10_share: 6.687
- n_trades: 6.66
- iti_median: 6.658
- flipper_share: 6.611

## xgb_botlive: top gain features

- bl_top10_share: 6.065
- bl_first_seen_sol: 4.644
- bl_price_slope: 4.585
- bl_sol_last60: 4.542
- bl_decision_age_s: 4.45
- bl_dev_buy_sol: 4.416
- bl_sol_per_s_window: 4.249
- bl_curve_sol_in: 4.059
- bl_log_ret_window: 3.751
- bl_inflow_accel: 3.656
- bl_run_from_low: 3.604
- bl_trades_last60: 3.473
- bl_lows: 2.24
- bl_max_drawdown: 2.238
- bl_lows_per_min: 1.631

## xgb_botlive+context: top gain features

- replies_at_entry: 25.082
- live_at_entry: 16.376
- is_native_launch: 12.963
- bl_curve_sol_in: 7.948
- market_recent_n: 6.918
- bl_sol_last60: 6.837
- bl_decision_age_s: 6.672
- bl_top10_share: 6.411
- market_candidate_rate: 6.397
- has_twitter: 6.382
- image_dup_24h: 6.358
- has_website: 6.258
- name_dup_24h: 5.956
- description_len: 5.794
- bl_sol_per_s_window: 5.655

## xgb_pnl:all+wallets: top gain features

- creator_prior_resolved: 5.429
- replies_at_entry: 4.362
- is_native_launch: 3.094
- holders_n: 2.073
- top3_share: 1.993
- launch_bundle_share: 1.938
- creator_prior_launches: 1.911
- has_twitter: 1.817
- dev_buy_sol: 1.735
- top1_share: 1.717
- w_hit_rate_max: 1.714
- iti_median: 1.674
- last_trade_t: 1.642
- n_slots: 1.597
- price_slope: 1.537

## xgb_pnl:botlive+context: top gain features

- replies_at_entry: 6.467
- live_at_entry: 3.475
- is_native_launch: 2.928
- bl_trades_last60: 1.507
- bl_dev_buy_sol: 1.398
- market_recent_n: 1.361
- has_twitter: 1.311
- bl_decision_age_s: 1.291
- market_candidate_rate: 1.287
- bl_sol_per_s_window: 1.242
- bl_top10_share: 1.239
- name_dup_24h: 1.232
- bl_curve_sol_in: 1.177
- bl_run_from_low: 1.15
- bl_first_seen_sol: 1.141
