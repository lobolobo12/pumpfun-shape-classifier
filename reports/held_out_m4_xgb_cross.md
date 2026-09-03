# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 103 | 0.335 | 0.704 | 0.00 | 0.40 | 0.40 | 1.34 | -0.42 |
| xgb_holders | 103 | 0.473 | 0.771 | 1.00 | 0.40 | 0.60 | 12.73 | 0.72 |
| xgb_shape+holders | 103 | 0.391 | 0.724 | 0.00 | 0.60 | 0.60 | 12.82 | 0.74 |
| xgb_all | 103 | 0.342 | 0.637 | 1.00 | 0.40 | 0.40 | 11.54 | -0.22 |
| xgb_context | 103 | 0.283 | 0.574 | 1.00 | 0.60 | 0.30 | 0.52 | -1.14 |
| logistic_repo_recipe | 103 | 0.262 | 0.560 | 0.00 | 0.40 | 0.30 | 0.51 | -1.41 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- sol_last60: 5.728
- buy_ratio_count: 5.397
- max_drawdown: 5.061
- sellers_last60: 4.897
- iti_cv: 4.882
- bundle_slots: 4.831
- n_trades: 4.831
- sell_share_sol: 4.818
- price_slope: 4.656
- n_sellers: 4.513
- lows: 4.5
- trades_last60: 4.476
- lows_per_min: 4.466
- volume_slope: 4.434
- run_from_low: 4.418

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

- sol_last60: 7.232
- exited_share: 7.097
- launch_bundle_share: 6.363
- dev_share: 6.115
- holders_n: 5.995
- sell_share_sol: 5.946
- buy_ratio_count: 5.916
- top1_share: 5.844
- top3_share: 5.803
- gini_buy_size: 5.791
- buy_size_cv: 5.784
- top10_share: 5.671
- max_drawdown: 5.652
- gini_hold: 5.544
- n_trades: 5.496

## xgb_all: top gain features

- sol_last60: 7.858
- dev_share: 6.988
- launch_bundle_share: 6.737
- is_native_launch: 6.611
- exited_share: 6.589
- top3_share: 6.223
- replies_at_entry: 6.156
- first_slot_share: 6.108
- top1_share: 6.091
- bundle_slots: 6.008
- n_trades: 5.841
- max_drawdown: 5.794
- creator_prior_tp_rate: 5.786
- creator_prior_launches: 5.669
- gini_buy_size: 5.649

## xgb_context: top gain features

- is_native_launch: 3.955
- market_recent_n: 3.642
- market_recent_tp_rate: 3.602
- hour_sin: 3.367
- hour_cos: 3.204
- replies_at_entry: 2.955
- live_at_entry: 2.826
