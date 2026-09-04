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
pkill -f "pf.*serve" || true
sleep 1
mkdir -p logs
nohup uv run pf --set decision_mode=cross serve --port 8791 --model "${SERVE_MODEL:-xgb_botlive}" > logs/serve.log 2>&1 &
sleep 6
curl -s http://127.0.0.1:8791/health | head -c 400; echo
