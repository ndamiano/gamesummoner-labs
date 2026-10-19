# decide-openai-shape

Status: single-run
Control: the decide jobs already run through `contract/decide.py` (SGLang `/generate` with
`return_hidden_states`, the decision head applied in the contract): local game 3170a8a2b4c3 (frog,
llama-swap SGLang, 2026-10-19) and e9's wizard-cat chain on the RunPod decide box (game 628f9b02f79c).

## Purpose

Nick's requirement (2026-10-19): every engine call goes through standard OpenAI-compatible shapes, so
`GameSummoner summon` runs on any llama-swap. The decide queue is the one that doesn't: it needs
SGLang's native `/generate` with hidden states, a prep step that splits JEV's adapter, and a 1.1 MB
readout the contract multiplies itself. JEV's README documents an OpenAI path instead: model
`jev-decision` through `/v1/completions` or `/v1/chat/completions` with `max_tokens: 1`, logprobs
over the option tokens (`allowed_token_ids`), then the bundled bias and per-kind temperature
client-side. The decision head is an `lm_head` LoRA, so the server's logprobs already carry it.

## Hypothesis

vLLM serving the NVFP4 base (`JEV-27B-VL-NVFP4`) with JEV's stock `adapter_vllm` on the local 5090,
read through `/v1/completions` + logprobs, gives the same decisions as the current contract: every
chain answer equal, and probabilities within the ±0.05 the current path already moves between
engine configs (max-running-requests 1 vs 2).

Idea failure: vLLM cannot apply the `lm_head` LoRA over the NVFP4 base's FP8 `lm_head` (garbage or
uniform probabilities), the model does not load on the 5090, or answers flip.

## Setup

- `vllm/vllm-openai:latest` in Docker, `--enable-lora --max-lora-rank 32
  --lora-modules jev-decision=/jev/adapter_vllm --max-logprobs 32 --logprobs-mode processed_logprobs`.
- `run.py`: `contract.decide.run_chain` from gamesummoner-images with a `read` that posts to
  `/v1/completions`; head files from `JEV-27B-VL/adapter_vllm/decision_head.json` and
  `calibration.json`. Compares each step's probabilities and the final answers with the control.
- 5090, local; llama-swap's models unloaded first (one card).

## Log

### 2026-10-19 run 1: wizard-cat and frog chains, vLLM 0.32.0, NVFP4 base, 5090

vLLM loaded `JEV-27B-VL-NVFP4` (absolute symlinks into `/var/lib/models/llm`, so the container
mounts `/var/lib/models` at the same path) with the stock `adapter_vllm` in about 2 minutes. The
only LoRA warnings are for the vision tower; the `lm_head` LoRA applies.

| chain | control | compared | mean abs diff | p95 | max | answers |
|---|---|---|---|---|---|---|
| wizard cat (628f9b02f79c) | RunPod / local decide box, SGLang max-running 1 | 307 | 0.013 | 0.036 | 0.059 | 21/22 equal |
| frog (3170a8a2b4c3) | llama-swap SGLang, max-running 2 | 264 | | | 0.077 | 21/22 equal |

Mean signed difference -0.0025 (139 up, 168 down): no lean. Both flips are the `mechanics` step,
whose ~60 items sit on `keep_over 0.6`; on wizard cat the three extra items moved 0.569-0.593 to
0.602-0.635. A whole chain takes 18 s.

`logit_bias` +100 in place of `allowed_token_ids` moved a two-option answer by 0.008: the bias
lands in bf16 logits, which resolve ~0.5 at that magnitude. `allowed_token_ids` (vLLM's OpenAI
extension, the one JEV documents) masks instead and is exact.

Read: works. Equivalent within the noise the current path already shows between engine configs.

## Outcome
