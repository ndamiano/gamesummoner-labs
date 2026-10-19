#!/usr/bin/env bash
# Serve decide, image, mesh and video from the 5090 (local_gpu.auto minus llm) under the 45G cap.
set -euo pipefail
REPO=$(cd "$(dirname "$0")/../.." && pwd)
LOGS=${MAESTRO_LOCAL_LOGS:-/tmp/maestro-local}
cd "$REPO"
exec labs/rig-lab/safe -m 45G venv/bin/python -c '
import sys; sys.path.insert(0, "scripts")
import local_gpu
local_gpu.QUEUES.remove("llm")
local_gpu.auto(None, 600)' >> "$LOGS/frontier-auto.log" 2>&1
