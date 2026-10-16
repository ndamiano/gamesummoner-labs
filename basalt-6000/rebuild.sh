#!/bin/bash
# On the box: pull the IQ3_S pack, and rebuild the UD-Q4_K_XL pack with the PLE key in BF16 (Q8_0 dropped from the
# converter's native-key list), so the batch path's PLE window kernels can run.
W=/opt/dlami/nvme/w
cd $W
export HF_HUB_ENABLE_HF_TRANSFER=1
mark() { echo "[$(date +%s)] $*"; }
( venv/bin/hf download jesdga/Qwen3.8-Flash-Next-Basalt Qwen3.8-FN-GSQ-RCO-IQ3_S.basalt --local-dir model > dl-iq3s.log 2>&1; mark "iq3s download exit $?" ) &
venv/bin/hf download jesdga/Qwen3.8-Flash-Next-Basalt --include "convert/*" --local-dir src > dl-convert.log 2>&1
mark "convert inputs exit $?"
venv/bin/hf download unsloth/Qwen3.8-Flash-Next-GGUF --include "UD-Q4_K_XL/*" --local-dir src > dl-gguf.log 2>&1
mark "gguf download exit $?"
(cd src && tar -xf convert/gguf-sources.tar)
ls -la src/convert src/convert/mtp | head -30
rm -rf basalt-conv && git clone -q basalt basalt-conv
sed -i 's/^NATIVE_PLE_KEY = {"Q2_0", "Q8_0"}/NATIVE_PLE_KEY = {"Q2_0"}/' basalt-conv/tools/convert/model_sections.py
grep -n "^NATIVE_PLE_KEY" basalt-conv/tools/convert/model_sections.py
/usr/bin/time -v venv/bin/python basalt-conv/tools/convert/convert.py \
  --gguf src/UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf \
  --out model/Qwen3.8-FN-UD-Q4_K_XL-bf16key.basalt --compat-bf16 \
  --mmproj src/convert/mmproj-Qwen3.8-Flash-Next-BF16.gguf --mtp-source src/convert/mtp \
  --profile src/convert/profile.bin --draft-vocab src/convert/draft_vocab.bin \
  --name "Qwen3.8-Flash-Next UD-Q4_K_XL (BF16 PLE key)" > convert.log 2>&1
mark "convert exit $?"
wait
venv/bin/python packmeta.py model/Qwen3.8-FN-UD-Q4_K_XL-bf16key.basalt
mark REBUILD_DONE
