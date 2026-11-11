#!/bin/bash
# the battery, one card, each step logged to its folder
cd "$(dirname "$0")/../.."
venv/bin/python labs/bible-first/build.py battery cats wizardcat zombie alienfarm > labs/bible-first/battery.log 2>&1
