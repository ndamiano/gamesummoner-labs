# jev-on-flash-next

Status: planned
Control: prod decide today: JEV-27B-VL (a LoRA plus a decision head on Qwen3.8-27B NVFP4) on stock
SGLang 0.5.21, EC2 g7e in us-east-1 with a RunPod 5090 fallback; first prod job 2026-10-19 took
~141 s from enqueue to answer (123 s of it boot, 16.6 s exec).

## Purpose

Decide and llm run on separate GPU pools with separate engines. On 2026-10-19 a ~200 s decide box
took the one us-east-1 spot slot ($2.58/hr) while the 30-minute llm box behind it paid on-demand
($3.36/hr): the short job got the cheap rung. Prod llm now runs Basalt, which serves only
Qwen3.8-Flash-Next. If JEV's decisions came from Flash-Next on Basalt, decide could run on the llm
boxes themselves: one engine, one image, one warm card for both queues, and no second pool to
misallocate.

## Hypothesis

## Setup

Two pieces, either of which can fail the idea:
- A JEV decision head (and adapter, if needed) trained against Flash-Next's hidden states from
  JEV's training data, scored against JEV-27B-VL on the same decide chains.
- Basalt returning the hidden states the head reads (it serves completions only today).

## Log

## Outcome
