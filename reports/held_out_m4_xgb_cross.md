# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 103 | 0.274 | 0.628 | 0.00 | 0.40 | 0.30 | 0.26 | -1.42 |
| xgb_holders | 103 | 0.361 | 0.660 | 1.00 | 0.60 | 0.40 | 11.16 | -0.80 |
| xgb_shape+holders | 103 | 0.337 | 0.693 | 1.00 | 0.20 | 0.40 | 0.97 | -0.78 |
| xgb_all | 103 | 0.306 | 0.681 | 1.00 | 0.20 | 0.20 | 10.09 | -1.44 |
| xgb_context | 103 | 0.182 | 0.526 | 0.00 | 0.20 | 0.20 | -0.46 | -1.43 |
| logistic_repo_recipe | 103 | 0.295 | 0.577 | 0.00 | 0.60 | 0.30 | 10.55 | -1.42 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- last_trade_t: 12.369
- lows: 11.658
- sol_last60: 11.428
- n_slots: 11.189
- bundle_slots: 11.013
- n_buyers: 10.996
- max_drawdown: 10.887
- sell_share_sol: 10.782
- step_gini: 10.336
- gini_buy_size: 10.108
- buy_size_cv: 9.868
- iti_median: 9.849
- buy_ratio_sol: 9.765
- buy_ratio_count: 9.709
- price_slope: 9.679

## xgb_holders: top gain features

- dev_share: 24.471
- dev_sold: 15.0
- holders_n: 12.144
- launch_bundle_share: 11.949
- top3_share: 10.143
- top1_share: 10.036
- top10_share: 9.562
- first_slot_share: 9.483
- tokens_out_pct: 9.47
- buyers_n: 8.824
- exited_share: 8.406
- gini_hold: 8.148
- same_size_share: 7.649

## xgb_shape+holders: top gain features

- dev_share: 34.452
- sell_share_sol: 25.175
- dev_sold: 21.966
- last_trade_t: 19.282
- sol_last60: 17.0
- iti_median: 16.92
- holders_n: 15.925
- run_from_low: 15.537
- buy_ratio_count: 15.171
- top3_share: 14.914
- first_trade_t: 14.913
- launch_bundle_share: 14.732
- top1_share: 14.488
- first_slot_share: 14.01
- buy_size_cv: 13.957

## xgb_all: top gain features

- is_native_launch: 51.551
- replies_at_entry: 35.696
- creator_prior_resolved: 31.041
- live_at_entry: 19.844
- last_trade_t: 18.616
- creator_prior_launches: 16.151
- sol_last60: 16.032
- launch_bundle_share: 15.866
- exited_share: 15.478
- bundle_slots: 14.608
- dev_share: 13.561
- top3_share: 13.237
- iti_median: 13.151
- top1_share: 12.974
- holders_n: 12.348

## xgb_context: top gain features

- is_native_launch: 20.385
- replies_at_entry: 9.875
- live_at_entry: 4.88
- hour_cos: 3.142
- hour_sin: 2.995
