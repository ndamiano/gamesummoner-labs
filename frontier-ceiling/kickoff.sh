#!/usr/bin/env bash
# Post one ask through the API as the e2e account, the way the front door does; prints the game id.
set -euo pipefail
ask=${1:?usage: kickoff.sh "<ask>"}
REPO=$(cd "$(dirname "$0")/../.." && pwd)
cd "$REPO/src"
user=c9a667820e8b
../venv/bin/python -m auth.cli grant e2e 100 >/dev/null
token=$(../venv/bin/python -c "from auth import store; print(store.issue_token('$user'))")
body=$(python3 -c 'import json,sys; print(json.dumps({"prompt": sys.argv[1]}))' "$ask")
curl -sf -X POST localhost:8000/api/games -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json" -d "$body"
echo
