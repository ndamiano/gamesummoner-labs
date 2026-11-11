#!/bin/bash
# after the wizardcat rerun exits, rerun alienfarm (its plan did not parse either)
cd "$(dirname "$0")/../.."
while pgrep -fx '/bin/bash labs/bible-first/followup.sh' >/dev/null; do sleep 60; done
venv/bin/python labs/bible-first/build.py all alienfarm > labs/bible-first/alienfarm/all.log 2>&1
