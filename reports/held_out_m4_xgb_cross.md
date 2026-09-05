# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 129 | 0.219 | 0.573 | 0.00 | 0.17 | 0.15 | -1.19 | -2.19 |
| xgb_holders | 129 | 0.216 | 0.556 | 0.00 | 0.17 | 0.15 | -1.37 | -2.45 |
| xgb_shape+holders | 129 | 0.203 | 0.553 | 0.00 | 0.17 | 0.15 | -1.24 | -2.24 |
| xgb_all | 129 | 0.215 | 0.581 | 0.00 | 0.17 | 0.23 | -0.58 | -2.19 |
| xgb_context | 129 | 0.155 | 0.438 | 0.00 | 0.00 | 0.00 | -2.24 | -2.05 |
| xgb_wallets | 129 | 0.241 | 0.519 | 0.00 | 0.17 | 0.38 | 1.10 | -0.49 |
| xgb_holders+wallets | 129 | 0.256 | 0.594 | 0.00 | 0.17 | 0.31 | 0.14 | -1.48 |
| xgb_all+wallets | 129 | 0.236 | 0.614 | 0.00 | 0.33 | 0.23 | -0.58 | -2.19 |
| xgb_botlive | 129 | 0.275 | 0.578 | 1.00 | 0.33 | 0.31 | 0.13 | -1.50 |
| xgb_botlive+context | 129 | 0.254 | 0.564 | 0.00 | 0.50 | 0.31 | 0.27 | -1.36 |
| xgb_pnl:all+wallets | 129 | 0.211 | 0.586 | 0.00 | 0.00 | 0.31 | 0.97 | -0.68 |
| xgb_pnl:botlive+context | 129 | 0.263 | 0.600 | 0.00 | 0.33 | 0.23 | -0.12 | -1.73 |
| logistic_repo_recipe | 129 | 0.220 | 0.565 | 0.00 | 0.33 | 0.15 | -1.44 | -2.41 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- sol_last60: 10.52
- bundle_slots: 8.307
- sell_share_sol: 7.089
- max_drawdown: 7.03
- iti_cv: 6.756
- curve_sol_in: 6.719
- buyers_last60: 6.717
- dev_buy_sol: 6.65
- last_trade_t: 6.579
- step_gini: 6.52
- lows: 6.426
- first_trade_t: 6.279
- biggest_buy_vs_curve: 6.147
- buy_size_cv: 6.146
- buy_ratio_sol: 6.134

## xgb_holders: top gain features

- holders_n: 6.918
- launch_bundle_share: 6.54
- dev_share: 6.28
- top3_share: 6.027
- first_slot_share: 5.718
- top10_share: 5.685
- top1_share: 5.655
- dev_sold: 5.635
- exited_share: 5.185
- gini_hold: 5.124
- tokens_out_pct: 4.968
- buyers_n: 4.578
- same_size_share: 4.157

## xgb_shape+holders: top gain features

- bundle_slots: 12.606
- buyers_last60: 11.796
- sol_last60: 10.553
- launch_bundle_share: 8.678
- decision_age_s: 8.569
- holders_n: 8.467
- biggest_buy_vs_curve: 8.183
- sell_share_sol: 8.022
- top1_share: 7.743
- max_drawdown: 7.743
- iti_cv: 7.562
- lows_per_min: 7.516
- buy_size_cv: 7.481
- exited_share: 7.368
- largest_buy_share: 7.305

## xgb_all: top gain features

- creator_prior_resolved: 15.283
- replies_at_entry: 15.017
- is_native_launch: 15.006
- creator_prior_launches: 10.25
- sol_last60: 9.765
- holders_n: 7.681
- exited_share: 7.651
- buy_size_cv: 7.233
- top3_share: 7.118
- top1_share: 7.111
- launch_bundle_share: 6.971
- buy_ratio_count: 6.757
- n_trades: 6.575
- max_drawdown: 6.515
- sellers_last60: 6.424

## xgb_context: top gain features

- replies_at_entry: 29.125
- live_at_entry: 18.679
- is_native_launch: 16.747
- has_twitter: 5.709
- market_recent_n: 5.693
- dow_cos: 5.267
- market_candidate_rate: 5.176
- name_dup_24h: 4.848
- hour_cos: 4.685
- description_len: 4.523
- market_recent_tp_rate: 4.507
- market_launch_rate: 4.419
- image_dup_24h: 4.34
- twitter_is_status: 4.231
- hour_sin: 4.197

## xgb_wallets: top gain features

- w_scored_share: 3.68
- w_hit_rate_mean: 3.613
- w_log_prior_mean: 3.589
- w_hit_rate_sol: 3.583
- w_hit_rate_max: 3.567
- w_repeat_share: 3.454
- w_serial_share: 3.349

## xgb_holders+wallets: top gain features

- launch_bundle_share: 5.044
- dev_sold: 4.882
- holders_n: 4.626
- top3_share: 4.592
- dev_share: 4.456
- top1_share: 4.294
- exited_share: 4.284
- w_scored_share: 4.171
- tokens_out_pct: 4.073
- w_hit_rate_mean: 4.071
- first_slot_share: 3.916
- top10_share: 3.908
- gini_hold: 3.901
- w_repeat_share: 3.871
- w_serial_share: 3.862

## xgb_all+wallets: top gain features

- creator_prior_resolved: 21.977
- is_native_launch: 19.143
- creator_prior_launches: 13.135
- replies_at_entry: 11.282
- sol_last60: 9.728
- live_at_entry: 9.234
- decision_age_s: 8.684
- launch_bundle_share: 8.394
- twitter_is_status: 8.078
- buy_ratio_count: 7.992
- has_twitter: 7.961
- buy_size_cv: 7.758
- holders_n: 7.753
- exited_share: 7.659
- top1_share: 7.597

## xgb_botlive: top gain features

- bl_sol_last60: 5.935
- bl_top10_share: 5.895
- bl_lows_per_min: 4.874
- bl_price_slope: 4.847
- bl_trades_last60: 4.834
- bl_log_ret_window: 4.674
- bl_dev_buy_sol: 4.464
- bl_run_from_low: 4.445
- bl_decision_age_s: 4.329
- bl_curve_sol_in: 4.275
- bl_inflow_accel: 4.238
- bl_max_drawdown: 4.209
- bl_first_seen_sol: 4.201
- bl_sol_per_s_window: 3.951

## xgb_botlive+context: top gain features

- replies_at_entry: 30.724
- is_native_launch: 23.007
- live_at_entry: 12.414
- bl_sol_last60: 9.077
- market_recent_n: 7.341
- image_dup_24h: 7.299
- market_candidate_rate: 6.996
- bl_top10_share: 6.978
- bl_lows_per_min: 6.947
- bl_log_ret_window: 6.892
- bl_run_from_low: 6.79
- has_telegram: 6.592
- bl_curve_sol_in: 6.572
- bl_first_seen_sol: 6.369
- twitter_is_status: 6.225

## xgb_pnl:all+wallets: top gain features

- creator_prior_resolved: 5.005
- replies_at_entry: 4.29
- is_native_launch: 3.43
- creator_prior_launches: 3.231
- iti_median: 1.815
- sell_share_sol: 1.751
- holders_n: 1.704
- top1_share: 1.675
- exited_share: 1.652
- launch_bundle_share: 1.634
- buy_size_cv: 1.603
- lows: 1.567
- buy_ratio_sol: 1.497
- bundle_slots: 1.496
- top3_share: 1.496

## xgb_pnl:botlive+context: top gain features

- replies_at_entry: 5.125
- is_native_launch: 3.859
- live_at_entry: 2.312
- twitter_is_status: 1.707
- bl_trades_last60: 1.532
- bl_lows: 1.27
- has_twitter: 1.264
- market_candidate_rate: 1.222
- bl_decision_age_s: 1.222
- market_recent_n: 1.217
- name_dup_24h: 1.193
- bl_top10_share: 1.176
- hour_cos: 1.164
- bl_sol_per_s_window: 1.152
- bl_curve_sol_in: 1.132
