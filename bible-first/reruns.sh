#!/bin/bash
# the two labels whose plans were cut at the token cap, with the cap raised
cd "$(dirname "$0")/../.."
venv/bin/python labs/bible-first/build.py all wizardcat > labs/bible-first/wizardcat/all.log 2>&1
venv/bin/python labs/bible-first/build.py all alienfarm > labs/bible-first/alienfarm/all.log 2>&1
