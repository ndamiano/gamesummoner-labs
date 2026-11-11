#!/bin/bash
# after the battery exits, rerun the label whose plan did not parse
cd "$(dirname "$0")/../.."
while pgrep -fx '/bin/bash labs/bible-first/overnight.sh' >/dev/null; do sleep 60; done
venv/bin/python labs/bible-first/build.py all wizardcat > labs/bible-first/wizardcat/all.log 2>&1
