#!/usr/bin/env bash
# Daily top-up: refresh the universe from the collector, extend the queue, commit it, dispatch the fetch,
# and fold any finished runs into the local cache. Safe to run any time; everything is resumable.
set -euo pipefail
cd "$(dirname "$0")/.."
uv run pf gh-pull --limit 20 2>&1 | grep -E "merged|no successful" || true
uv run pf universe --no-strict | tail -4
# after the universe: the rebuild re-merges history with hour-floored launch times, so correct them afterwards
uv run pf fix-launch-times 2>&1 | tail -1 || true
uv run pf prescreen | tail -2
if ! git diff --quiet -- data/queue/ || [ -n "$(git status --porcelain data/queue/)" ]; then
  git add data/queue/
  git -c commit.gpgsign=false commit -q -m "queue: $(date -u +%F) top-up"
  git push -q origin main
fi
if gh run list --workflow fetch.yml --status in_progress --limit 1 --json databaseId -q '.[0].databaseId' | grep -q .; then
  echo "a fetch run is already in progress; not dispatching another"
else
  gh workflow run fetch.yml -f shards="${SHARDS:-20}" -f rps="${RPS:-0.28}" -f probe=0 -f max_minutes="${MAX_MINUTES:-300}"
  echo "dispatched fetch (${SHARDS:-20} shards)"
fi
# Served bot-live models: retrain on the bot's task (entry at first sight) with yesterday as the held-out day, restart the scorer.
TODAY=$(date +%F); YDAY=$(date -v-1d +%F 2>/dev/null || date -d "yesterday" +%F)
scripts/serve_refresh.sh "$YDAY" "$TODAY" 2>&1 | tail -3 || echo "serve refresh failed"
