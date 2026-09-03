# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 103 | 0.268 | 0.625 | 0.00 | 0.20 | 0.20 | -0.04 | -1.50 |
| xgb_holders | 103 | 0.473 | 0.771 | 1.00 | 0.40 | 0.60 | 12.73 | 0.72 |
| xgb_shape+holders | 103 | 0.268 | 0.618 | 0.00 | 0.20 | 0.40 | 1.36 | -0.68 |
| xgb_all | 103 | 0.370 | 0.720 | 1.00 | 0.40 | 0.40 | 1.59 | -0.46 |
| xgb_context | 103 | 0.154 | 0.392 | 0.00 | 0.00 | 0.20 | 0.07 | -1.39 |
| xgb_wallets | 103 | 0.179 | 0.504 | 0.00 | 0.00 | 0.10 | -1.04 | -1.46 |
| xgb_holders+wallets | 103 | 0.393 | 0.727 | 0.00 | 0.80 | 0.40 | 11.31 | -0.77 |
| xgb_all+wallets | 103 | 0.424 | 0.741 | 0.00 | 0.80 | 0.50 | 11.73 | -0.02 |
| logistic_repo_recipe | 103 | 0.262 | 0.560 | 0.00 | 0.40 | 0.30 | 0.51 | -1.41 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- sol_last60: 11.379
- buy_ratio_count: 8.823
- flipper_share: 8.768
- iti_median: 8.667
- bundle_slots: 8.433
- buyers_last60: 7.974
- n_trades: 7.831
- max_drawdown: 7.83
- trades_last60: 7.708
- sell_share_sol: 7.667
- iti_cv: 7.595
- inflow_accel: 7.502
- iti_std: 7.384
- n_sellers: 7.303
- price_slope: 7.289

## xgb_holders: top gain features

- exited_share: 6.553
- launch_bundle_share: 6.356
- dev_share: 6.151
- holders_n: 6.012
- top3_share: 5.88
- top10_share: 5.81
- first_slot_share: 5.693
- top1_share: 5.447
- tokens_out_pct: 5.214
- buyers_n: 5.0
- gini_hold: 4.858
- dev_sold: 4.706
- same_size_share: 4.226

## xgb_shape+holders: top gain features

- bundle_slots: 14.011
- sol_last60: 11.145
- dev_share: 9.924
- flipper_share: 9.83
- top3_share: 9.717
- exited_share: 9.66
- launch_bundle_share: 8.773
- n_sellers: 8.736
- buy_ratio_count: 8.392
- same_size_share: 8.351
- top1_share: 8.264
- n_slots: 8.227
- gini_buy_size: 8.199
- first_slot_share: 8.179
- max_drawdown: 7.975

## xgb_all: top gain features

- sol_last60: 11.256
- replies_at_entry: 11.186
- exited_share: 11.095
- dev_sold: 10.77
- top3_share: 10.29
- sell_share_sol: 10.049
- bundle_slots: 9.837
- is_native_launch: 9.827
- dev_share: 9.82
- iti_std: 9.627
- top1_share: 9.376
- launch_bundle_share: 9.283
- has_website: 9.263
- holders_n: 9.083
- flipper_share: 8.994

## xgb_context: top gain features

- has_twitter: 6.49
- dow_cos: 5.759
- has_telegram: 5.583
- description_len: 5.547
- image_dup_24h: 5.365
- market_candidate_rate: 5.238
- live_at_entry: 5.054
- market_recent_n: 5.024
- name_dup_24h: 4.975
- twitter_is_status: 4.97
- hour_sin: 4.879
- hour_cos: 4.766
- market_launch_rate: 4.711
- dow_sin: 4.567
- market_recent_tp_rate: 4.487

## xgb_wallets: top gain features

- w_repeat_share: 5.356
- w_hit_rate_mean: 5.196
- w_serial_share: 4.623
- w_hit_rate_sol: 4.346
- w_scored_share: 4.19
- w_hit_rate_max: 4.112
- w_log_prior_mean: 4.095

## xgb_holders+wallets: top gain features

- exited_share: 7.679
- launch_bundle_share: 6.933
- top3_share: 6.802
- dev_share: 6.754
- dev_sold: 6.7
- holders_n: 6.618
- top1_share: 6.6
- w_repeat_share: 6.371
- w_serial_share: 6.218
- w_log_prior_mean: 6.176
- w_hit_rate_mean: 6.138
- w_hit_rate_max: 6.128
- buyers_n: 6.118
- gini_hold: 6.082
- first_slot_share: 5.808

## xgb_all+wallets: top gain features

- bundle_slots: 10.615
- sol_last60: 10.428
- dev_share: 10.242
- top3_share: 10.234
- holders_n: 9.882
- launch_bundle_share: 9.859
- exited_share: 9.721
- image_dup_24h: 9.269
- w_repeat_share: 8.995
- flipper_share: 8.887
- first_slot_share: 8.702
- top1_share: 8.607
- w_hit_rate_max: 8.596
- buy_ratio_count: 8.383
- n_trades: 8.194
