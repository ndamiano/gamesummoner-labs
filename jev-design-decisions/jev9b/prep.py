"""Split the JEV-9B System 1 adapter for sglang (copy of AI-Launcher/jev/prep_adapter.py on the bf16 9B).

sglang's lm_head LoRA runs F.linear on the raw lm_head weight, which is FP8 in the local NVFP4 base, so the lm_head
part of the adapter is not loaded into sglang. Instead:
  adapter_sglang/     backbone LoRA only (every target module except lm_head) -> sglang --lora-paths
  readout.safetensors the decision head's readout: lm_head rows for the verbalizer tokens (dequantized) and the
                      lm_head LoRA rows for those tokens -> logits = h @ (W + s * B @ A)^T, computed by decide.py
"""
import json
import shutil
import sys
from pathlib import Path

import torch
from safetensors import safe_open
from safetensors.torch import save_file

JEV = Path("/var/lib/models/jev/JEV-9B")
BASE = JEV
SRC = JEV / "adapter_vllm"
OUT = JEV / "adapter_sglang"


def split_in_proj_qkv(weights):
    """HF/vLLM layout has in_proj_qkv (q|k|v rows) + in_proj_z; sglang loads in_proj_q/k/v/z and stacks them into
    in_proj_qkvz. Exact: each slice keeps the shared lora_A and takes its rows of lora_B."""
    config = json.loads((BASE / "config.json").read_text())
    text = config.get("text_config", config)
    key_dim = text["linear_key_head_dim"] * text["linear_num_key_heads"]
    value_dim = text["linear_value_head_dim"] * text["linear_num_value_heads"]
    sizes = {"q": key_dim, "k": key_dim, "v": value_dim}
    out = {}
    for k, t in weights.items():
        if ".in_proj_qkv." not in k:
            out[k] = t
            continue
        if "lora_A" in k:
            for s in sizes:
                out[k.replace(".in_proj_qkv.", f".in_proj_{s}.")] = t.clone()
        else:
            assert t.shape[0] == sum(sizes.values()), (k, t.shape)
            for s, part in zip(sizes, torch.split(t, list(sizes.values()), dim=0)):
                out[k.replace(".in_proj_qkv.", f".in_proj_{s}.")] = part.contiguous()
    return out


def main():
    cfg = json.loads((SRC / "adapter_config.json").read_text())
    head = json.loads((SRC / "decision_head.json").read_text())
    ids = head["verbalizer_ids"]
    scaling = cfg["lora_alpha"] / cfg["r"]

    backbone, lm_a, lm_b = {}, None, None
    with safe_open(SRC / "adapter_model.safetensors", "pt") as f:
        for k in f.keys():
            if ".lm_head." in k:
                if "lora_A" in k:
                    lm_a = f.get_tensor(k)
                else:
                    lm_b = f.get_tensor(k)
            else:
                backbone[k] = f.get_tensor(k)
    assert lm_a is not None and lm_b is not None, "adapter has no lm_head LoRA"

    backbone = split_in_proj_qkv(backbone)

    OUT.mkdir(exist_ok=True)
    save_file(backbone, OUT / "adapter_model.safetensors", metadata={"format": "pt"})
    # sglang fuses the linear-attention input projections into in_proj_qkvz
    targets = [m for m in cfg["target_modules"] if m not in ("lm_head", "in_proj_qkv", "in_proj_z")]
    cfg["target_modules"] = targets + ["in_proj_qkvz"]
    (OUT / "adapter_config.json").write_text(json.dumps(cfg, indent=2))

    index = json.loads((BASE / "model.safetensors.index.json").read_text())["weight_map"]
    with safe_open(BASE / index["lm_head.weight"], "pt") as f:
        w = f.get_slice("lm_head.weight")[ids]          # only the verbalizer rows
        scale = f.get_slice("lm_head.weight_scale")[ids] if "lm_head.weight_scale" in index else None
    w = w.float() * (scale.float() if scale is not None else 1.0)

    save_file({
        "ids": torch.tensor(ids, dtype=torch.int64),
        "weight": w.contiguous(),                        # (n_ids, hidden)
        "lora_a": lm_a.float().contiguous(),             # (r, hidden)
        "lora_b": (lm_b[ids].float() * scaling).contiguous(),  # (n_ids, r), LoRA scaling folded in
    }, JEV / "readout.safetensors", metadata={"base": str(BASE), "adapter": str(SRC)})
    print(f"backbone tensors: {len(backbone)}, readout rows: {len(ids)}, lora scaling: {scaling}")


if __name__ == "__main__":
    sys.exit(main())
