#!/usr/bin/env bash
# train.sh <mode> <split_train_end> <split_val_end> [tag] — label + features + leakage + xgb + cnn for one
# decision mode, stamping the reports with mode and tag. Leaves that mode's artifacts on disk.
set -euo pipefail
cd "$(dirname "$0")/.."
MODE="${1:?mode}"; TRAIN_END="${2:?train_end}"; VAL_END="${3:?val_end}"; TAG="${4:-preliminary}"
PF=(uv run pf --set "decision_mode=$MODE" --set "split_train_end=$TRAIN_END" --set "split_val_end=$VAL_END")
"${PF[@]}" label 2>&1 | tail -1
"${PF[@]}" features 2>&1 | tail -1
"${PF[@]}" check leakage 2>&1 | tail -1
"${PF[@]}" xgb 2>&1 | grep -E "train |test PR-AUC"
mv -f reports/m4_xgb.json "reports/${TAG}_m4_xgb_${MODE}.json"
mv -f reports/m4_xgb.md "reports/${TAG}_m4_xgb_${MODE}.md"
"${PF[@]}" --set cnn.encoding=trades cnn 2>&1 | grep -E "test PR-AUC"
mv -f "reports/m5_cnn_trades+side.json" "reports/${TAG}_m5_cnn_trades_${MODE}.json"
mv -f "reports/m5_cnn_trades+side.md" "reports/${TAG}_m5_cnn_trades_${MODE}.md"
"${PF[@]}" --set cnn.encoding=trades --set cnn.side=false cnn 2>&1 | grep -E "test PR-AUC"
mv -f "reports/m5_cnn_trades.json" "reports/${TAG}_m5_cnn_trades_seqonly_${MODE}.json"
mv -f "reports/m5_cnn_trades.md" "reports/${TAG}_m5_cnn_trades_seqonly_${MODE}.md"
