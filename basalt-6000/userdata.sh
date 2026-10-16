#!/bin/bash
shutdown -h +180
exec > /var/log/basalt-boot.log 2>&1
mark() { echo "[$(date +%s)] $*"; }
mark start
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
free -g
mkdir -p /opt/dlami/nvme/w
W=/opt/dlami/nvme/w
CUDA=$(ls -d /usr/local/cuda-13* 2>/dev/null | sort -V | tail -1)
mark "cuda $CUDA"
export PATH=$CUDA/bin:$PATH
apt-get update -q && apt-get install -y -q cmake build-essential git python3-venv
python3 -m venv $W/venv
$W/venv/bin/pip install -q -U "huggingface_hub[hf_transfer]"
mark "deps done"
cd $W
( HF_HUB_ENABLE_HF_TRANSFER=1 $W/venv/bin/hf download jesdga/Qwen3.8-Flash-Next-Basalt Qwen3.8-FN-UD-Q4_K_XL.basalt --local-dir $W/model > $W/dl.log 2>&1; mark "download exit $?" ) &
git clone https://github.com/jesdga95/basalt.git $W/basalt
cd $W/basalt
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_CUDA_COMPILER=$CUDA/bin/nvcc > $W/cmake.log 2>&1
cmake --build build -j8 > $W/build.log 2>&1
mark "build exit $? $(ls bin)"
$W/venv/bin/pip install -q -r requirements.txt
mark "server reqs done"
wait
mark "boot done"
