# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 298 | 0.317 | 0.690 | 0.00 | 0.27 | 0.43 | 13.90 | 1.81 |
| xgb_holders | 298 | 0.269 | 0.586 | 0.67 | 0.20 | 0.17 | 7.93 | -4.03 |
| xgb_shape+holders | 298 | 0.329 | 0.672 | 0.33 | 0.33 | 0.40 | 13.52 | 1.22 |
| xgb_all | 298 | 0.323 | 0.622 | 0.67 | 0.53 | 0.37 | 13.10 | 0.80 |
| xgb_context | 298 | 0.248 | 0.575 | 0.00 | 0.40 | 0.27 | 0.73 | -1.07 |
| xgb_wallets | 298 | 0.287 | 0.597 | 0.67 | 0.47 | 0.33 | 12.80 | 1.17 |
| xgb_holders+wallets | 298 | 0.297 | 0.635 | 0.33 | 0.33 | 0.33 | 2.33 | 0.04 |
| xgb_all+wallets | 298 | 0.358 | 0.654 | 1.00 | 0.47 | 0.37 | 13.42 | 1.12 |
| logistic_repo_recipe | 298 | 0.272 | 0.565 | 0.67 | 0.40 | 0.27 | 0.39 | -1.53 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- sol_last60: 8.361
- flipper_share: 7.939
- dev_buy_sol: 7.69
- lows: 7.619
- n_sellers: 6.929
- max_drawdown: 6.653
- first_trade_t: 6.513
- iti_cv: 6.385
- n_buyers: 6.255
- buy_ratio_count: 6.118
- decision_age_s: 6.105
- sell_share_sol: 6.088
- n_trades: 6.084
- buy_size_cv: 5.898
- last_trade_t: 5.864

## xgb_holders: top gain features

- dev_share: 8.219
- dev_sold: 6.838
- holders_n: 6.675
- launch_bundle_share: 6.511
- top3_share: 6.483
- exited_share: 5.72
- first_slot_share: 5.635
- top1_share: 5.524
- gini_hold: 5.196
- tokens_out_pct: 5.129
- top10_share: 5.116
- buyers_n: 4.787
- same_size_share: 4.501

## xgb_shape+holders: top gain features

- bundle_slots: 10.575
- dev_sold: 10.024
- dev_share: 9.937
- sol_last60: 9.601
- exited_share: 9.142
- dev_buy_sol: 9.03
- buyers_last60: 8.859
- holders_n: 8.678
- flipper_share: 8.492
- top3_share: 8.453
- launch_bundle_share: 8.11
- max_drawdown: 7.667
- last_trade_t: 7.431
- gini_buy_size: 7.392
- buy_size_cv: 7.25

## xgb_all: top gain features

- is_native_launch: 17.87
- replies_at_entry: 13.481
- exited_share: 11.999
- sol_last60: 11.685
- creator_prior_resolved: 11.563
- creator_prior_launches: 10.938
- top3_share: 10.494
- dev_share: 10.314
- holders_n: 10.239
- market_recent_n: 10.22
- bundle_slots: 9.699
- buyers_n: 9.687
- gini_buy_size: 9.624
- launch_bundle_share: 9.391
- market_candidate_rate: 9.385

## xgb_context: top gain features

- is_native_launch: 10.358
- replies_at_entry: 9.521
- live_at_entry: 5.996
- twitter_is_status: 5.545
- market_recent_n: 5.395
- market_candidate_rate: 4.974
- name_dup_24h: 4.591
- has_twitter: 4.577
- image_dup_24h: 4.494
- market_recent_tp_rate: 4.305
- description_len: 3.927
- hour_cos: 3.791
- market_launch_rate: 3.734
- hour_sin: 3.711
- has_website: 3.391

## xgb_wallets: top gain features

- w_repeat_share: 4.844
- w_scored_share: 4.185
- w_hit_rate_sol: 4.066
- w_serial_share: 4.0
- w_hit_rate_mean: 3.853
- w_log_prior_mean: 3.731
- w_hit_rate_max: 3.659

## xgb_holders+wallets: top gain features

- dev_share: 9.787
- dev_sold: 8.579
- holders_n: 7.75
- top3_share: 7.645
- launch_bundle_share: 7.595
- exited_share: 7.162
- top1_share: 7.012
- w_repeat_share: 6.851
- w_hit_rate_max: 6.83
- w_scored_share: 6.684
- w_serial_share: 6.632
- top10_share: 6.499
- buyers_n: 6.334
- w_hit_rate_mean: 6.265
- gini_hold: 6.209

## xgb_all+wallets: top gain features

- is_native_launch: 16.162
- twitter_is_status: 10.711
- creator_prior_resolved: 10.7
- bundle_slots: 10.428
- exited_share: 10.424
- replies_at_entry: 10.223
- holders_n: 10.074
- market_candidate_rate: 9.916
- sol_last60: 9.897
- buyers_n: 9.691
- n_sellers: 9.446
- dev_share: 9.361
- launch_bundle_share: 9.242
- top3_share: 8.771
- decision_age_s: 8.507
