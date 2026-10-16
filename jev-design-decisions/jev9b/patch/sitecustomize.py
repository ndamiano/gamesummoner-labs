"""Give sglang's text-only Qwen3_5ForCausalLM the LoRA hidden-dim lookup its multimodal sibling has."""
try:
    from sglang.srt.models import qwen3_5, qwen3_5_text
    qwen3_5_text.Qwen3_5ForCausalLM.get_hidden_dim = qwen3_5.Qwen3_5ForCausalLM.get_hidden_dim
except ImportError:
    pass
