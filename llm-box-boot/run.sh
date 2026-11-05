#!/usr/bin/env bash
# Launch one lab box from the region's prod llm AMI with boot.sh as user-data; print where its logs land.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
images=${GS_IMAGES:-$HOME/Documents/gamesummoner-images}
. "$images/aws/common.sh"
market=spot
[ "${2:-}" = --on-demand ] && market=on-demand
ami=${1:?usage: AWS_REGION=<region> run.sh <prod llm ami for the region> [--on-demand]}
instance=$(run_instance "gs-lab-llm-box-boot-$(basename "${USERDATA:-boot.sh}" .sh)-$(date -u +%Y%m%dT%H%M%S)" "$ami" "$here/${USERDATA:-boot.sh}" "$market")
echo "$instance $(date -u +%FT%TZ) $REGION $ami $market" | tee -a "$here/launches.txt"
echo "logs: s3://$BUCKET/lab/llm-box-boot/$instance/"
