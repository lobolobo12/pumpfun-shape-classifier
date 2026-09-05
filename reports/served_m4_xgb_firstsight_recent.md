# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape+recent | 138 | 0.211 | 0.554 | 0.00 | 0.14 | 0.21 | -0.89 | -2.44 |
| xgb_holders+recent | 138 | 0.238 | 0.563 | 0.00 | 0.29 | 0.21 | -1.04 | -2.65 |
| xgb_shape+holders+recent | 138 | 0.210 | 0.553 | 0.00 | 0.14 | 0.14 | -1.61 | -2.61 |
| xgb_all+recent | 138 | 0.202 | 0.568 | 0.00 | 0.00 | 0.07 | -2.07 | -2.65 |
| xgb_context+recent | 138 | 0.229 | 0.522 | 1.00 | 0.29 | 0.14 | -0.81 | -1.88 |
| xgb_wallets+recent | 138 | 0.233 | 0.544 | 0.00 | 0.29 | 0.21 | -0.40 | -1.96 |
| xgb_holders+wallets+recent | 138 | 0.240 | 0.575 | 0.00 | 0.29 | 0.21 | -0.78 | -2.32 |
| xgb_all+wallets+recent | 138 | 0.200 | 0.547 | 0.00 | 0.00 | 0.14 | -1.30 | -2.43 |
| xgb_botlive+recent | 138 | 0.269 | 0.502 | 1.00 | 0.29 | 0.29 | -0.03 | -1.61 |
| xgb_botlive+context+recent | 138 | 0.269 | 0.534 | 1.00 | 0.29 | 0.36 | 0.72 | -0.91 |
| xgb_pnl:all+wallets+recent | 138 | 0.191 | 0.526 | 0.00 | 0.00 | 0.14 | -0.59 | -1.78 |
| xgb_pnl:botlive+context+recent | 138 | 0.271 | 0.593 | 0.00 | 0.29 | 0.36 | 1.08 | -0.50 |
| logistic_repo_recipe | 138 | 0.269 | 0.651 | 0.00 | 0.14 | 0.29 | -0.41 | -1.98 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape+recent: top gain features

- buyers_last60: 10.45
- sol_last60: 10.199
- max_drawdown: 9.535
- buy_ratio_count: 8.802
- iti_cv: 8.799
- trades_last60: 8.795
- bundle_slots: 8.781
- lows_per_min: 8.737
- n_trades: 8.607
- sell_share_sol: 8.462
- buy_ratio_sol: 8.337
- iti_std: 8.293
- flipper_share: 8.201
- curve_sol_in: 8.109
- n_slots: 8.043

## xgb_holders+recent: top gain features

- holders_n: 11.268
- dev_share: 10.107
- launch_bundle_share: 9.987
- exited_share: 8.612
- top10_share: 8.497
- top3_share: 8.474
- top1_share: 8.279
- first_slot_share: 8.174
- same_size_share: 7.631
- buyers_n: 7.604
- gini_hold: 6.625
- tokens_out_pct: 6.134
- dev_sold: 3.842

## xgb_shape+holders+recent: top gain features

- holders_n: 13.207
- top3_share: 12.921
- launch_bundle_share: 12.241
- n_trades: 11.63
- sol_last60: 11.602
- buyers_last60: 11.174
- iti_median: 11.103
- decision_age_s: 10.949
- exited_share: 10.725
- first_slot_share: 10.708
- max_drawdown: 10.701
- dev_share: 10.453
- lows: 10.349
- tokens_out_pct: 10.201
- top1_share: 10.199

## xgb_all+recent: top gain features

- has_website: 21.322
- holders_n: 17.302
- iti_median: 15.728
- max_drawdown: 14.978
- buyers_last60: 14.823
- sol_last60: 14.494
- n_trades: 14.246
- sellers_last60: 13.612
- description_len: 13.457
- top3_share: 13.226
- has_twitter: 12.958
- launch_bundle_share: 12.9
- exited_share: 12.863
- buy_ratio_count: 12.375
- flipper_share: 12.359

## xgb_context+recent: top gain features

- dow_cos: 8.74
- is_native_launch: 8.272
- live_at_entry: 8.141
- description_len: 8.059
- dow_sin: 7.579
- has_twitter: 7.495
- market_recent_n: 7.349
- name_dup_24h: 7.223
- market_candidate_rate: 7.061
- twitter_is_status: 6.676
- replies_at_entry: 6.663
- has_website: 6.59
- image_dup_24h: 6.464
- market_launch_rate: 6.458
- hour_cos: 6.447

## xgb_wallets+recent: top gain features

- w_scored_share: 6.689
- w_log_prior_mean: 6.451
- w_repeat_share: 6.216
- w_hit_rate_mean: 6.206
- w_serial_share: 6.201
- w_hit_rate_max: 5.883
- w_hit_rate_sol: 5.586

## xgb_holders+wallets+recent: top gain features

- holders_n: 9.444
- dev_share: 8.767
- launch_bundle_share: 8.755
- top10_share: 8.382
- top3_share: 7.906
- w_repeat_share: 7.895
- first_slot_share: 7.687
- top1_share: 7.68
- same_size_share: 7.638
- exited_share: 7.462
- buyers_n: 7.385
- w_scored_share: 7.304
- w_hit_rate_max: 7.147
- tokens_out_pct: 7.138
- w_serial_share: 7.062

## xgb_all+wallets+recent: top gain features

- has_telegram: 15.155
- holders_n: 14.142
- sol_last60: 13.194
- launch_bundle_share: 12.118
- top3_share: 12.052
- iti_median: 11.617
- bundle_slots: 11.177
- first_slot_share: 10.822
- buy_ratio_count: 10.352
- flipper_share: 10.284
- buyers_last60: 10.049
- sell_share_sol: 10.037
- last_trade_t: 10.018
- dev_share: 9.989
- has_website: 9.93

## xgb_botlive+recent: top gain features

- bl_top10_share: 6.935
- bl_curve_sol_in: 6.636
- bl_decision_age_s: 6.569
- bl_sol_per_s_window: 6.469
- bl_price_slope: 6.305
- bl_sol_last60: 6.247
- bl_first_seen_sol: 5.976
- bl_dev_buy_sol: 5.777
- bl_inflow_accel: 5.663
- bl_run_from_low: 5.502
- bl_log_ret_window: 5.012
- bl_trades_last60: 4.948
- bl_max_drawdown: 4.245
- bl_lows_per_min: 2.301

## xgb_botlive+context+recent: top gain features

- bl_curve_sol_in: 8.799
- replies_at_entry: 8.784
- bl_top10_share: 8.696
- description_len: 8.657
- bl_sol_per_s_window: 8.477
- market_candidate_rate: 8.435
- bl_decision_age_s: 8.334
- bl_sol_last60: 7.942
- is_native_launch: 7.926
- bl_first_seen_sol: 7.844
- market_launch_rate: 7.744
- has_twitter: 7.741
- bl_price_slope: 7.598
- bl_run_from_low: 7.496
- has_telegram: 7.328

## xgb_pnl:all+wallets+recent: top gain features

- holders_n: 2.494
- top3_share: 2.072
- iti_median: 1.929
- dev_buy_sol: 1.854
- launch_bundle_share: 1.794
- n_slots: 1.742
- buy_size_cv: 1.528
- w_repeat_share: 1.51
- inflow_accel: 1.491
- last_trade_t: 1.442
- w_hit_rate_mean: 1.426
- name_dup_24h: 1.42
- creator_prior_launches: 1.413
- top1_share: 1.401
- sell_share_sol: 1.392

## xgb_pnl:botlive+context+recent: top gain features

- bl_dev_buy_sol: 1.367
- bl_first_seen_sol: 1.267
- bl_decision_age_s: 1.249
- bl_sol_per_s_window: 1.208
- bl_curve_sol_in: 1.198
- bl_trades_last60: 1.177
- bl_sol_last60: 1.165
- name_dup_24h: 1.141
- is_native_launch: 1.139
- bl_top10_share: 1.123
- market_launch_rate: 1.107
- market_candidate_rate: 1.067
- market_recent_n: 1.05
- image_dup_24h: 1.047
- dow_cos: 1.036
