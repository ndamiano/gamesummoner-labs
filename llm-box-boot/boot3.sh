#!/usr/bin/env bash
# User-data for lab run 3: the ceilings under the pack pull. Raw instance-store write and read with
# O_DIRECT, the S3 → /dev/null rate with no disk, then the prod pull for a baseline.
set -uo pipefail
exec > >(python3 -u -c 'import sys,time
for l in sys.stdin: print(f"{time.time():.2f} {l}", end="", flush=True)' > /var/log/lab-boot.log) 2>&1

NVME=/opt/dlami/nvme
PACK=Qwen3.8-FN-UD-Q4_K_XL-bf16key-mtptuned.basalt
LAB=/var/log/lab
mkdir -p "$LAB"
mark() { echo "[lab +$(awk '{printf "%d", $1}' /proc/uptime)s uptime] $*"; }
rate() { python3 -c "import sys; print(f'{int(sys.argv[1]) / max(float(sys.argv[2]), 0.01) / 1e9:.2f} GB/s')" "$1" "$2"; }

token=$(curl -sf -m 2 -X PUT -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600' http://169.254.169.254/latest/api/token)
md() { curl -sf -H "X-aws-ec2-metadata-token: $token" "http://169.254.169.254/latest/meta-data/$1"; }
region=$(md placement/region); instance=$(md instance-id)
bucket=gamesummoner-models-$region-$(cat /opt/gamesummoner/account)
src="s3://$bucket/basalt/$PACK"
s5="s5cmd --log error --endpoint-url http://s3.$region.amazonaws.com"
finish() {
    mark "finishing"
    kill "${sampler:-0}" 2>/dev/null
    cp /var/log/lab-boot.log "$LAB/"
    s5cmd --log error cp "$LAB/*" "s3://$bucket/lab/llm-box-boot/$instance/" || true
    systemctl poweroff
}
trap finish EXIT
trap 'exit 1' TERM
( sleep 900; mark "watchdog: 15 min, giving up"; kill $$ ) &

( while :; do
    printf '%s %s %s %s\n' "$(date +%s.%N | cut -c1-14)" \
      "$(awk '/^(Cached|Dirty|Writeback):/{printf "%s%s ",$1,$2}' /proc/meminfo)" \
      "$(awk '$3=="nvme1n1"{printf "nvme1n1 rs=%s ws=%s busy_ms=%s ",$6,$10,$13}' /proc/diskstats)" \
      "$(awk -F'[: ]+' '$2 ~ /^(ens|eth)/{printf "%s rx=%s ",$2,$3}' /proc/net/dev)"
    sleep 1
  done > "$LAB/samples.txt" ) &
sampler=$!

for _ in $(seq 1 60); do mountpoint -q "$NVME" && break; sleep 1; done
mark "instance store: $(lsblk -dno NAME,SIZE,MODEL | grep -i 'instance storage' | tr '\n' ';')"
size=$($s5 ls "$src" | awk '{print $3}')
mark "pack is $size bytes; s5cmd $(s5cmd version 2>&1 | head -1); $(nproc) cpus"

t=$(date +%s.%N)
dd if=/dev/zero of="$NVME/ddtest" bs=64M count=480 oflag=direct status=none
el=$(python3 -c "import time; print(time.time() - $t)")
mark "raw write, 30 GiB O_DIRECT: ${el%.*}s, $(rate $((30 * 1073741824)) "$el")"
t=$(date +%s.%N)
dd if="$NVME/ddtest" of=/dev/null bs=64M iflag=direct status=none
el=$(python3 -c "import time; print(time.time() - $t)")
mark "raw read, 30 GiB O_DIRECT: ${el%.*}s, $(rate $((30 * 1073741824)) "$el")"
rm -f "$NVME/ddtest"

for cfg in "64 64" "128 64" "256 128"; do
    set -- $cfg
    t=$(date +%s.%N)
    $s5 cat --concurrency "$1" --part-size "$2" "$src" | head -c 64424509440 > /dev/null
    el=$(python3 -c "import time; print(time.time() - $t)")
    mark "network only, first 60 GiB to /dev/null, concurrency $1 part $2: ${el%.*}s, $(rate 64424509440 "$el")"
done

sync; echo 3 > /proc/sys/vm/drop_caches
t=$(date +%s.%N)
$s5 cp --concurrency 64 --part-size 64 "$src" "$NVME/$PACK"
el=$(python3 -c "import time; print(time.time() - $t)")
mark "prod pull to the instance store: ${el%.*}s, $(rate "$size" "$el")"
