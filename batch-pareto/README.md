# batch-pareto — how far does one llm box batch?

Status: planned
Requires: >1000 paying customers per day. Batching only pays when the box is full; below that,
cards that scale one at a time and DeepSeek's API (~$0.65/game, labs/frontier-ceiling) are cheaper.
Control: labs/conc-replay (2026-09-13, Pennyroyal on one Pro 6000 at ~104K context: 1 stream 128
tok/s, 2 streams 114 each, 4 streams 79–88 each)

## Purpose

DeepSeek open-sourced DeepInfer (2026-10-20, github.com/deepseek-ai/DeepInfer), the engine behind
its API. Its decode chart (`doc/images/decode_pareto.png`, DeepSeek V4.1 Flash, 64 SM100 GPUs,
experts sharded 64 ways, 131K context, MTP acceptance fixed at 75%) holds 325 tok/s per user at 8
streams per GPU and 246 at 64: 8× the streams for −24% per user. Ours falls off far faster: 1 → 4
streams costs each user ~35% for 2.3× aggregate, and prod runs Basalt at 1 slot because it reuses
a slot only on an exact prefix match.

The question is whether the same shape exists at our scale: one box of 8× Pro 6000 serving ~160
concurrent builds instead of ~160 single-build cards. DeepSeek's curve stays flat because expert
parallelism gives each expert a large batch, so its GEMMs are compute-bound rather than
weight-read-bound. The Pro 6000 has no NVLink, so expert dispatch rides PCIe every layer of every
decode step — the biggest unknown. The July DeepSeek V4 run on 2× Pro 6000 sat at 47–49% util on a
layer split.

What would block it on our stack, from what is already measured:

- KV space per card: Flash-Next takes ~73 GiB of 96; Pennyroyal's pool was ~900K tokens, ~8 builds
  at 100K. Sharding experts 8 ways frees ~60 GiB per card for KV.
- Host RAM: each Flash-Next replica pins ~48 GiB for the PLE table; 8 replicas need ~384 GiB.
- Prefill: turns that start together serialize (5.5 → 18 s on Pennyroyal), and compaction voids
  the prefix cache. DeepInfer leaves prefill/decode disaggregation, the KV cache system and load
  balancing out of its release; deepseek-recipe is the request/chat codec, not serving.
- Speculative decoding feeds on the same idle bandwidth batching does (2026-08-01), so Basalt's
  spec 7 gain shrinks as the batch grows.

## Hypothesis

Two runs, in order, the second only if the first says one card is not the ceiling.

1. One Pro 6000, SGLang with the largest KV pool that fits, real build transcripts replayed at real
   context, sweep 1/2/4/8/16 streams. Plot per-user tok/s against tok/s per GPU, the same axes as
   DeepSeek's chart. Expected: KV capacity, not decode, ends the curve around 8 streams at ~100K.
2. Two Pro 6000s over PCIe: experts sharded across both (EP2) against two independent replicas
   (DP2), same sweep. Expected if the idea lives: EP2 holds per-user speed at higher stream counts
   than DP2 because it has more KV room and larger per-expert batches. Idea failure: EP2's PCIe
   all-to-all costs more per step than the batching buys, so EP2 ≤ DP2 at every point.

## Setup

## Log

## Outcome
