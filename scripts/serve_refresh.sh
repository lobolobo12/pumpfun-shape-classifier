#!/usr/bin/env bash
# serve_refresh.sh <train_end> <val_end> — retrain the SERVED bot-live models on the bot's actual task
# (entry at first sight, empirical first-sight mixture), persist them, restart `pf serve` on 8791.
set -euo pipefail
cd "$(dirname "$0")/.."
TRAIN_END="${1:?train_end}"; VAL_END="${2:?val_end}"
PF=(uv run pf --set decision_mode=cross --set "split_train_end=$TRAIN_END" --set "split_val_end=$VAL_END" --set botlive.entry_at_first_sight=true)
"${PF[@]}" label 2>&1 | tail -1
"${PF[@]}" features 2>&1 | tail -1
"${PF[@]}" xgb 2>&1 | grep -E "botlive"
mv -f reports/m4_xgb.json "reports/served_m4_xgb_firstsight.json"
mv -f reports/m4_xgb.md "reports/served_m4_xgb_firstsight.md"
"${PF[@]}" --set cnn.encoding=botlive cnn 2>&1 | grep -E "test PR-AUC|bag ->"
mv -f "reports/m5_cnn_botlive+side.json" "reports/served_m5_cnn_botlive.json" 2>/dev/null || true
mv -f "reports/m5_cnn_botlive+side.md" "reports/served_m5_cnn_botlive.md" 2>/dev/null || true
pkill -f "pumpfun.*serve --port" || true
sleep 1
mkdir -p logs
# the bot-view CNN in its own process (torch and xgboost cannot share one), then the primary that forwards to it
nohup uv run pf --set decision_mode=cross serve --port 8792 --model "cnn_botlive+side" > logs/serve_cnn.log 2>&1 &
sleep 20
nohup uv run pf --set decision_mode=cross serve --port 8791 --model "${SERVE_MODEL:-xgb_botlive}" > logs/serve.log 2>&1 &
sleep 12
curl -s http://127.0.0.1:8791/health | head -c 400; echo
