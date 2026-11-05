#!/usr/bin/env bash
# User-data for one lab boot of the prod llm AMI: the entrypoint's boot with every line stamped,
# a startup-file pre-read under the pack pull, memory/disk sampling, then logs to S3 and power off.
set -uo pipefail
exec > >(python3 -u -c 'import sys,time
for l in sys.stdin: print(f"{time.time():.2f} {l}", end="", flush=True)' > /var/log/lab-boot.log) 2>&1

NVME=/opt/dlami/nvme
BASALT=/opt/basalt
PACK=Qwen3.8-FN-UD-Q4_K_XL-bf16key-mtptuned.basalt
PORT=8001
LAB=/var/log/lab
mkdir -p "$LAB"
mark() { echo "[lab +$(awk '{printf "%d", $1}' /proc/uptime)s uptime] $*"; }
stamp() { python3 -u -c 'import sys,time
for l in sys.stdin: print(f"{time.time():.2f} {l}", end="", flush=True)'; }

token=$(curl -sf -m 2 -X PUT -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600' http://169.254.169.254/latest/api/token)
md() { curl -sf -H "X-aws-ec2-metadata-token: $token" "http://169.254.169.254/latest/meta-data/$1"; }
region=$(md placement/region); instance=$(md instance-id)
bucket=gamesummoner-models-$region-$(cat /opt/gamesummoner/account)
mark "entrypoint start, $instance in $region"
systemd-analyze > "$LAB/systemd-analyze.txt" 2>&1
systemd-analyze blame 2>&1 | head -25 >> "$LAB/systemd-analyze.txt"

finish() {
    mark "finishing"
    kill "${sampler:-0}" "${engine:-0}" "${tail_pid:-0}" 2>/dev/null
    cp /var/log/lab-boot.log "$LAB/"
    s5cmd --log error cp "$LAB/*" "s3://$bucket/lab/llm-box-boot/$instance/" || true
    systemctl poweroff
}
trap finish EXIT
trap 'exit 1' TERM
( sleep 900; mark "watchdog: 15 min, giving up"; kill $$ ) &

( while :; do
    printf '%s %s %s\n' "$(date +%s.%N | cut -c1-14)" \
      "$(awk '/^(MemFree|Cached|Dirty|Writeback):/{printf "%s%s ",$1,$2}' /proc/meminfo)" \
      "$(awk '$3=="nvme0n1"||$3=="nvme1n1"{printf "%s rs=%s ws=%s busy_ms=%s ",$3,$6,$10,$13}' /proc/diskstats)"
    sleep 1
  done > "$LAB/samples.txt" ) &
sampler=$!

for _ in $(seq 1 60); do mountpoint -q "$NVME" && break; sleep 1; done
mark "instance store mounted"
( t=$(date +%s); nvidia-smi -pm 1 > /dev/null 2>&1; mark "gpu persistence on, $(( $(date +%s) - t ))s" ) &

( t=$(date +%s)
  { find /root/.cache/basalt /opt/basalt /opt/gamesummoner /usr/lib/python3.12 -type f
    ls /usr/local/cuda-13.3/targets/x86_64-linux/lib/libcublas.so.* \
       /usr/local/cuda-13.3/targets/x86_64-linux/lib/libcublasLt.so.* \
       /usr/local/cuda-13.3/targets/x86_64-linux/lib/libcudart.so.* \
       /usr/lib/x86_64-linux-gnu/libcuda.so.* /usr/lib/x86_64-linux-gnu/libnvidia-*.so.* ; } \
    2>/dev/null | sort -u > "$LAB/prewarm.list"
  bytes=$(xargs -a "$LAB/prewarm.list" -d '\n' du -cb 2>/dev/null | tail -1 | cut -f1)
  xargs -a "$LAB/prewarm.list" -d '\n' -P 32 -n 16 cat > /dev/null 2>&1
  mark "pre-read $(wc -l < "$LAB/prewarm.list") files, $(( bytes / 1048576 )) MiB, in $(( $(date +%s) - t ))s" ) &

t=$(date +%s)
s5cmd --log error --endpoint-url "http://s3.$region.amazonaws.com" cp --concurrency 64 --part-size 64 \
    "s3://$bucket/basalt/$PACK" "$NVME/$PACK"
mark "pack on the instance store in $(( $(date +%s) - t ))s"
wait_prewarm=$(pgrep -f "xargs -a $LAB/prewarm.list" | head -1)
[ -n "$wait_prewarm" ] && mark "pre-read still running at pack-done"

config=$NVME/basalt.json
python3 - "$config" "$NVME/$PACK" <<'CONFIG'
import json, sys
json.dump({"server": {"model": sys.argv[2], "vision": "dynamic", "fit-max-tokens": True},
           "engine": {"expert-cache": "auto", "prefill": "auto", "spec": 7, "spec-min-p": 0.5,
                      "kv": "int8", "vram-reserve-mib": 700, "resident-experts": True,
                      "max-context": 262144, "conversation-cache-mib": 32000,
                      "conversation-cache-slots": 16}}, open(sys.argv[1], "w"))
CONFIG
engine_log=$(ls -d /root/.cache/basalt/*/ | head -1)engine.log
tail -n0 -F "$engine_log" 2>/dev/null | stamp > "$LAB/engine.log" &
tail_pid=$!
mark "starting engine"
setsid "$BASALT/bin/basalt" serve --config "$config" --alias qwen3.8-flash-next-basalt \
    --host 127.0.0.1 --port $PORT --parallel 1 2>&1 | stamp > "$LAB/server.log" &
engine=$!

until curl -sf -m 2 "http://127.0.0.1:$PORT/v1/models" > /dev/null; do sleep 0.5; done
mark "engine answers /v1/models"
t=$(date +%s.%N)
curl -sf -m 120 "http://127.0.0.1:$PORT/v1/chat/completions" -H 'content-type: application/json' \
    -d '{"model":"qwen3.8-flash-next-basalt","max_tokens":32,"messages":[{"role":"user","content":"Say hi."}]}' \
    > "$LAB/first-reply.json"
mark "first reply in $(python3 -c "import time; print(round(time.time() - $t, 2))")s"
sleep 3
