#!/usr/bin/env bash
# The weekend GPU queue: runs labs/runner/jobs.txt one line at a time, from the repo root. A line
# is a shell command. Lines are claimed by moving them to done.txt with start/end stamps and exit
# code, so jobs can be appended while it runs. With nothing pending it waits for more.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
JOBS=$HERE/jobs.txt; DONE=$HERE/done.txt; LOG=/var/tmp/runner
mkdir -p $LOG; touch $JOBS $DONE
while true; do
  line=$(grep -v '^\s*\(#\|$\)' $JOBS | head -1)
  if [ -z "$line" ]; then sleep 60; continue; fi
  python3 - "$JOBS" "$line" <<'PY'
import sys
path, line = sys.argv[1], sys.argv[2]
rows = open(path).read().splitlines()
rows.remove(line)
open(path, "w").write("\n".join(rows) + ("\n" if rows else ""))
PY
  n=$(( $(wc -l < $DONE) + 1 ))
  start=$(date -Is)
  echo "[$start] start #$n: $line" | tee -a $LOG/runner.log
  bash -c "$line" < /dev/null > $LOG/job$n.log 2>&1
  code=$?
  echo "$start $(date -Is) exit=$code | $line" >> $DONE
  echo "[$(date -Is)] end #$n exit=$code" | tee -a $LOG/runner.log
done
