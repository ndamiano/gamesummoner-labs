#!/usr/bin/env bash
# User-data for the one prep boot: tar the llm box's startup folders and libraries into the
# region's bucket as lab/llm-box-boot/hot.tar, the stand-in for a bake-time step, then power off.
set -uo pipefail
exec > >(python3 -u -c 'import sys,time
for l in sys.stdin: print(f"{time.time():.2f} {l}", end="", flush=True)' > /var/log/lab-pack.log) 2>&1
token=$(curl -sf -m 2 -X PUT -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600' http://169.254.169.254/latest/api/token)
md() { curl -sf -H "X-aws-ec2-metadata-token: $token" "http://169.254.169.254/latest/meta-data/$1"; }
region=$(md placement/region); instance=$(md instance-id)
bucket=gamesummoner-models-$region-$(cat /opt/gamesummoner/account)
finish() {
    s5cmd --log error cp /var/log/lab-pack.log "s3://$bucket/lab/llm-box-boot/pack-$instance.log" || true
    systemctl poweroff
}
trap finish EXIT
trap 'exit 1' TERM
( sleep 1200; kill $$ ) &

for _ in $(seq 1 60); do mountpoint -q /opt/dlami/nvme && break; sleep 1; done
LIST=/opt/dlami/nvme/hot.list
{ printf '%s\n' /root/.cache/basalt /opt/basalt /opt/gamesummoner /usr/lib/python3.12
  find /usr/local/cuda-13.3/targets/x86_64-linux/lib /usr/lib/x86_64-linux-gnu -maxdepth 1 -type f \
    \( -name 'libcublas.so.*' -o -name 'libcublasLt.so.*' -o -name 'libcudart.so.*' \
       -o -name 'libcuda.so.*' -o -name 'libnvidia-*.so.*' \) ; } > "$LIST"
echo "packing $(cat "$LIST" | tr '\n' ' ')"
t=$(date +%s)
tar -cf /opt/dlami/nvme/hot.tar -T "$LIST"
echo "tar $(du -h /opt/dlami/nvme/hot.tar | cut -f1) in $(( $(date +%s) - t ))s"
s5cmd --log error cp /opt/dlami/nvme/hot.tar "s3://$bucket/lab/llm-box-boot/hot.tar"
s5cmd --log error cp "$LIST" "s3://$bucket/lab/llm-box-boot/hot.list"
echo "uploaded"
