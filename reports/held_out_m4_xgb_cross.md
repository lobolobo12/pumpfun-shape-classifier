# Milestone 4 — XGBoost baseline

| model | n | PR-AUC | ROC-AUC | P@1% | P@5% | P@10% | PnL@10% (SOL) | ex-top-3 |
|---|---|---|---|---|---|---|---|---|
| xgb_shape | 103 | 0.327 | 0.690 | 0.00 | 0.40 | 0.40 | 10.96 | -0.78 |
| xgb_holders | 103 | 0.415 | 0.734 | 1.00 | 0.60 | 0.50 | 12.13 | 0.05 |
| xgb_shape+holders | 103 | 0.392 | 0.763 | 0.00 | 0.40 | 0.50 | 2.02 | -0.03 |
| xgb_all | 103 | 0.301 | 0.652 | 0.00 | 0.40 | 0.40 | 11.57 | -0.18 |
| xgb_context | 103 | 0.225 | 0.583 | 0.00 | 0.20 | 0.20 | -0.61 | -1.44 |
| logistic_repo_recipe | 103 | 0.312 | 0.648 | 0.00 | 0.60 | 0.30 | 10.28 | -1.48 |
| human (M0) | — | not yet recorded: run `pf bench label` | | | | | | |


## xgb_shape: top gain features

- sol_last60: 16.681
- bundle_slots: 14.641
- buy_ratio_count: 14.004
- iti_cv: 12.823
- lows: 12.814
- sell_share_sol: 12.72
- step_gini: 12.412
- time_to_10_trades: 12.343
- sellers_last60: 12.197
- buy_size_cv: 11.634
- run_from_low: 11.614
- volume_slope: 11.555
- n_buyers: 11.49
- first_trade_t: 11.4
- n_sellers: 11.369

## xgb_holders: top gain features

- launch_bundle_share: 12.84
- top10_share: 12.651
- exited_share: 12.644
- top3_share: 12.579
- dev_share: 12.537
- top1_share: 12.347
- gini_hold: 11.981
- first_slot_share: 10.983
- holders_n: 10.821
- tokens_out_pct: 9.926
- buyers_n: 9.169
- same_size_share: 8.54
- dev_sold: 7.241

## xgb_shape+holders: top gain features

- buyers_n: 15.119
- sellers_last60: 15.062
- exited_share: 15.049
- sol_last60: 14.987
- top3_share: 13.64
- n_slots: 13.507
- top10_share: 13.391
- step_gini: 13.236
- n_trades: 13.06
- dev_share: 12.995
- top1_share: 12.859
- first_slot_share: 12.767
- launch_bundle_share: 12.698
- buy_ratio_count: 12.587
- gini_hold: 12.394

## xgb_all: top gain features

- sol_last60: 12.184
- exited_share: 10.313
- launch_bundle_share: 10.305
- top3_share: 10.015
- first_slot_share: 9.553
- dev_share: 9.473
- replies_at_entry: 9.442
- top1_share: 9.377
- creator_prior_launches: 9.375
- buyers_n: 9.271
- gini_hold: 9.23
- n_slots: 9.206
- step_gini: 8.978
- iti_cv: 8.858
- time_to_10_trades: 8.811

## xgb_context: top gain features

- is_native_launch: 4.154
- hour_cos: 3.873
- live_at_entry: 3.743
- hour_sin: 3.636
- replies_at_entry: 3.313
