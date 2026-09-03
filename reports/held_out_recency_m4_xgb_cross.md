# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 103 | 0.338 | 0.693 | 0.00 | 0.40 | 0.30 | 10.27 | -1.46 |
| xgb_holders | 103 | 0.385 | 0.643 | 1.00 | 0.60 | 0.40 | 11.07 | -0.72 |
| xgb_shape+holders | 103 | 0.347 | 0.671 | 0.00 | 0.40 | 0.40 | 10.83 | -0.79 |
| xgb_all | 103 | 0.360 | 0.682 | 1.00 | 0.20 | 0.40 | 11.00 | -0.74 |
| xgb_context | 103 | 0.181 | 0.525 | 0.00 | 0.00 | 0.00 | -2.04 | -1.45 |
| logistic_repo_recipe | 103 | 0.273 | 0.581 | 0.00 | 0.40 | 0.40 | 11.20 | -0.77 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- sol_last60: 8.052
- bundle_slots: 7.527
- buy_ratio_count: 6.513
- lows: 6.172
- iti_cv: 6.161
- sellers_last60: 6.095
- max_drawdown: 5.987
- run_from_low: 5.866
- sell_share_sol: 5.708
- n_trades: 5.615
- gini_buy_size: 5.615
- price_slope: 5.595
- trades_last60: 5.58
- time_to_10_trades: 5.488
- step_gini: 5.476

## xgb_holders: top gain features

- dev_share: 8.206
- exited_share: 7.885
- top3_share: 7.537
- launch_bundle_share: 7.194
- top1_share: 6.927
- holders_n: 6.806
- gini_hold: 6.6
- first_slot_share: 6.412
- top10_share: 6.243
- tokens_out_pct: 6.175
- same_size_share: 5.97
- buyers_n: 5.718
- dev_sold: 5.418

## xgb_shape+holders: top gain features

- sol_last60: 11.495
- dev_share: 10.633
- launch_bundle_share: 10.222
- exited_share: 10.213
- top1_share: 10.17
- holders_n: 9.964
- same_size_share: 9.654
- top3_share: 9.387
- gini_hold: 9.339
- buy_ratio_sol: 8.66
- buy_ratio_count: 8.64
- buy_size_cv: 8.578
- gini_buy_size: 8.563
- trades_last60: 8.436
- n_sellers: 8.328

## xgb_all: top gain features

- sol_last60: 7.751
- launch_bundle_share: 7.707
- bundle_slots: 7.614
- exited_share: 6.984
- top3_share: 6.881
- lows: 6.551
- holders_n: 6.446
- top1_share: 6.399
- dev_share: 6.36
- creator_prior_launches: 6.108
- dev_sold: 6.027
- last_trade_t: 6.007
- buy_ratio_count: 6.002
- buy_size_cv: 5.987
- gini_hold: 5.916

## xgb_context: top gain features

- is_native_launch: 2.447
- replies_at_entry: 2.184
- hour_sin: 2.18
- hour_cos: 2.15
- live_at_entry: 1.815
