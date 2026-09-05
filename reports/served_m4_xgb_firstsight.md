# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 138 | 0.197 | 0.527 | 0.00 | 0.00 | 0.21 | -0.74 | -2.29 |
| xgb_holders | 138 | 0.235 | 0.539 | 0.00 | 0.29 | 0.21 | -1.13 | -2.67 |
| xgb_shape+holders | 138 | 0.197 | 0.509 | 0.00 | 0.14 | 0.21 | -0.90 | -2.45 |
| xgb_all | 138 | 0.205 | 0.571 | 0.00 | 0.00 | 0.07 | -2.37 | -2.65 |
| xgb_context | 138 | 0.184 | 0.498 | 0.00 | 0.00 | 0.00 | -2.09 | -2.25 |
| xgb_wallets | 138 | 0.246 | 0.494 | 0.00 | 0.43 | 0.29 | 0.02 | -1.56 |
| xgb_holders+wallets | 138 | 0.251 | 0.561 | 0.00 | 0.14 | 0.36 | 0.37 | -1.20 |
| xgb_all+wallets | 138 | 0.198 | 0.529 | 0.00 | 0.00 | 0.00 | -2.42 | -2.65 |
| xgb_botlive | 138 | 0.289 | 0.557 | 1.00 | 0.43 | 0.36 | 0.58 | -1.01 |
| xgb_botlive+context | 138 | 0.272 | 0.538 | 1.00 | 0.29 | 0.29 | -0.16 | -1.78 |
| xgb_pnl:all+wallets | 138 | 0.202 | 0.545 | 0.00 | 0.00 | 0.21 | -0.40 | -1.94 |
| xgb_pnl:botlive+context | 138 | 0.274 | 0.585 | 0.00 | 0.29 | 0.43 | 1.89 | 0.31 |
| logistic_repo_recipe | 138 | 0.251 | 0.615 | 0.00 | 0.14 | 0.29 | 0.29 | -1.32 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- bundle_slots: 10.299
- buyers_last60: 8.741
- sol_last60: 8.375
- iti_median: 7.229
- decision_age_s: 6.648
- n_trades: 6.611
- max_drawdown: 6.467
- n_slots: 6.455
- trades_last60: 6.436
- iti_std: 6.043
- iti_cv: 6.04
- price_slope: 6.015
- lows: 5.955
- lows_per_min: 5.932
- run_from_low: 5.895

## xgb_holders: top gain features

- holders_n: 6.659
- dev_share: 6.224
- dev_sold: 6.063
- top10_share: 5.872
- first_slot_share: 5.46
- launch_bundle_share: 5.446
- top3_share: 5.312
- tokens_out_pct: 5.281
- gini_hold: 5.009
- top1_share: 4.415
- same_size_share: 4.341
- exited_share: 4.055
- buyers_n: 3.568

## xgb_shape+holders: top gain features

- bundle_slots: 13.86
- top10_share: 10.146
- sol_last60: 9.911
- launch_bundle_share: 9.874
- holders_n: 9.369
- top3_share: 9.218
- buyers_last60: 8.226
- n_trades: 7.943
- iti_median: 7.851
- last_trade_t: 7.774
- decision_age_s: 7.686
- exited_share: 7.666
- tokens_out_pct: 7.562
- run_from_low: 7.258
- price_slope: 6.93

## xgb_all: top gain features

- creator_prior_resolved: 25.115
- iti_median: 13.312
- is_native_launch: 12.716
- creator_prior_launches: 12.634
- max_drawdown: 10.571
- buyers_last60: 10.331
- holders_n: 10.255
- sol_last60: 9.569
- replies_at_entry: 9.344
- dow_cos: 8.864
- top3_share: 8.675
- last_trade_t: 8.459
- top10_share: 8.394
- exited_share: 8.29
- market_recent_n: 8.071

## xgb_context: top gain features

- replies_at_entry: 31.01
- live_at_entry: 25.287
- is_native_launch: 6.634
- market_recent_n: 4.419
- name_dup_24h: 4.344
- market_candidate_rate: 4.276
- description_len: 4.239
- has_website: 4.2
- has_twitter: 4.016
- dow_cos: 3.878
- has_telegram: 3.808
- hour_sin: 3.78
- dow_sin: 3.716
- market_launch_rate: 3.649
- hour_cos: 3.602

## xgb_wallets: top gain features

- w_repeat_share: 4.641
- w_hit_rate_sol: 4.297
- w_hit_rate_max: 4.023
- w_scored_share: 4.007
- w_hit_rate_mean: 3.925
- w_serial_share: 3.822
- w_log_prior_mean: 3.7

## xgb_holders+wallets: top gain features

- holders_n: 9.688
- top10_share: 6.918
- w_repeat_share: 6.689
- launch_bundle_share: 6.656
- gini_hold: 6.376
- dev_share: 6.331
- first_slot_share: 5.99
- w_hit_rate_mean: 5.984
- top3_share: 5.836
- exited_share: 5.819
- w_log_prior_mean: 5.582
- w_scored_share: 5.564
- w_hit_rate_max: 5.474
- same_size_share: 5.454
- w_serial_share: 5.333

## xgb_all+wallets: top gain features

- creator_prior_resolved: 31.937
- replies_at_entry: 20.453
- creator_prior_launches: 17.791
- is_native_launch: 16.868
- buyers_last60: 13.468
- holders_n: 12.002
- has_twitter: 11.15
- exited_share: 10.887
- market_recent_n: 10.129
- iti_median: 9.712
- max_drawdown: 9.656
- sol_last60: 9.534
- top10_share: 9.453
- flipper_share: 9.392
- round_size_share: 9.382

## xgb_botlive: top gain features

- bl_top10_share: 4.523
- bl_sol_last60: 4.301
- bl_sol_per_s_window: 4.071
- bl_dev_buy_sol: 3.82
- bl_price_slope: 3.775
- bl_decision_age_s: 3.75
- bl_curve_sol_in: 3.707
- bl_first_seen_sol: 3.572
- bl_inflow_accel: 3.508
- bl_run_from_low: 3.172
- bl_lows_per_min: 2.894
- bl_log_ret_window: 2.833
- bl_max_drawdown: 2.064
- bl_trades_last60: 1.707

## xgb_botlive+context: top gain features

- replies_at_entry: 31.22
- live_at_entry: 15.27
- is_native_launch: 11.697
- market_candidate_rate: 6.3
- bl_top10_share: 5.939
- bl_curve_sol_in: 5.861
- bl_price_slope: 5.739
- bl_sol_last60: 5.718
- bl_max_drawdown: 5.667
- bl_sol_per_s_window: 5.434
- bl_log_ret_window: 5.431
- name_dup_24h: 5.422
- dow_cos: 5.371
- market_recent_n: 5.322
- bl_first_seen_sol: 5.32

## xgb_pnl:all+wallets: top gain features

- creator_prior_resolved: 4.151
- is_native_launch: 2.845
- replies_at_entry: 2.813
- creator_prior_launches: 1.827
- top3_share: 1.717
- holders_n: 1.554
- launch_bundle_share: 1.528
- name_dup_24h: 1.407
- dev_buy_sol: 1.373
- top1_share: 1.35
- last_trade_t: 1.343
- top10_share: 1.302
- twitter_is_status: 1.276
- tokens_out_pct: 1.27
- decision_age_s: 1.245

## xgb_pnl:botlive+context: top gain features

- replies_at_entry: 7.049
- live_at_entry: 4.601
- is_native_launch: 2.261
- bl_decision_age_s: 1.231
- market_candidate_rate: 1.165
- has_twitter: 1.154
- bl_dev_buy_sol: 1.145
- bl_top10_share: 1.123
- name_dup_24h: 1.118
- has_website: 1.11
- market_recent_n: 1.095
- has_telegram: 1.077
- bl_lows: 1.06
- bl_trades_last60: 1.039
- bl_first_seen_sol: 1.032
