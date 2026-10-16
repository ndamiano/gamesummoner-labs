#!/bin/bash
shutdown -h +300
exec > /var/log/basalt-boot.log 2>&1
mark() { echo "[$(date +%s)] $*"; }
mark start
W=/opt/dlami/nvme/w
B=s3://gamesummoner-models-385588571625/basalt-test
mkdir -p $W && cd $W
CUDA=$(ls -d /usr/local/cuda-13* | sort -V | tail -1)
export PATH=$CUDA/bin:$PATH
apt-get update -q && apt-get install -y -q cmake build-essential git python3-venv
python3 -m venv venv && venv/bin/pip install -q -U "huggingface_hub[hf_transfer]"
export HF_HUB_ENABLE_HF_TRANSFER=1
aws s3 cp $B/ . --recursive --exclude "*" --include "*.py" --include "*.sh" --include "longctx.json" --quiet
mark "deps done"
( venv/bin/hf download jesdga/Qwen3.8-Flash-Next-Basalt --include "convert/*" --local-dir src > dl-convert.log 2>&1
  venv/bin/hf download unsloth/Qwen3.8-Flash-Next-GGUF --include "UD-Q4_K_XL/*" --local-dir src > dl-gguf.log 2>&1
  (cd src && tar -xf convert/gguf-sources.tar); mark "sources done" ) &
git clone -q https://github.com/jesdga95/basalt.git basalt
git -C basalt log -1 --format=%h
venv/bin/pip install -q -r basalt/requirements.txt
venv/bin/python patch_batch_ar.py basalt
cmake -S basalt -B basalt/build -DCMAKE_BUILD_TYPE=Release > cmake.log 2>&1 && cmake --build basalt/build -j8 > build.log 2>&1
mark "build exit $?"
ln -sfn basalt basalt-patch
rm -rf basalt-conv && git clone -q basalt basalt-conv
sed -i 's/^NATIVE_PLE_KEY = {"Q2_0", "Q8_0"}/NATIVE_PLE_KEY = {"Q2_0"}/' basalt-conv/tools/convert/model_sections.py
wait
mkdir -p model
conv() {
  venv/bin/python basalt-conv/tools/convert/convert.py \
    --gguf src/UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf --compat-bf16 \
    --mmproj src/convert/mmproj-Qwen3.8-Flash-Next-BF16.gguf --mtp-source src/convert/mtp \
    --profile src/convert/profile.bin --draft-vocab src/convert/draft_vocab.bin "$@"
}
conv --out model/Qwen3.8-FN-UD-Q4_K_XL-bf16key.basalt --name "Qwen3.8-Flash-Next UD-Q4_K_XL (BF16 PLE key)" > convert1.log 2>&1
mark "convert1 exit $?"
aws s3 cp model/Qwen3.8-FN-UD-Q4_K_XL-bf16key.basalt $B/packs/ --quiet
mark "upload1 exit $?"
conv --mtp-dense src/convert/mtp/rt/dense.bin --out model/Qwen3.8-FN-UD-Q4_K_XL-bf16key-mtptuned.basalt \
  --name "Qwen3.8-Flash-Next UD-Q4_K_XL (BF16 PLE key, tuned MTP)" > convert2.log 2>&1
mark "convert2 exit $?"
aws s3 cp model/Qwen3.8-FN-UD-Q4_K_XL-bf16key-mtptuned.basalt $B/packs/ --quiet
mark "upload2 exit $?"
mark BOOT_DONE
