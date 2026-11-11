# hosted-decider: the design's decisions from a per-token API instead of our decide box

Status: planned
Control: the decide chains prod already ran on our box (JEV-27B-VL, SGLang, max-running-requests 1),
saved as `decisions.json` in each game's run dir: 26b16c2ea111 and fe87fce4707a (both 2026-11-05,
Quality); the OpenAI-shape equivalence numbers in `labs/decide-openai-shape` (mean abs diff 0.013,
max 0.077, 21/22 answers equal between our own engine configs).

## Purpose

Quality games now run every llm call on DeepSeek's API, at ~$0.27–0.63 a game. The one job still on
our hardware is decide: one JEV chain of 22 decisions per game, ~16–68 s of work. The box around it
is paid out of pocket. Prod, the 5 decide boxes of the last 30 days (all g7e.2xlarge):

| | per box |
|---|---|
| launch → registered | 122–165 s |
| busy | 16–68 s |
| paid (lifetime × hourly rate) | $0.08–0.20 |
| billed to the game (busy seconds) | ~$0.013 |

That is 6–15× what the game is billed, ~13% on top of the last game's $0.63, and 2–3 min of boot in
front of the design write on every cold start. Hosted per-token decision models exist: TypeSafe's
Jev ($0.042 per million input tokens, output free) and Perplexity's `pplx-decider-v1-27b` ($0.02 per
million input, open weights), per third-party comparisons, not the providers' own pages. A chain is
22 prompts of a few thousand tokens, so either is a fraction of a cent per game.

## Hypothesis

A hosted decider makes the same calls our JEV box makes on the same chain, so Quality games can drop
the decide box with no change to the design: no boot, no out-of-pocket idle.

Measured per chain against the control's saved `decisions.json`: answers equal out of 22, and over
every option probability, mean abs diff, p95 and max (the `decide-openai-shape` comparison).

- Works, TypeSafe Jev: ≥ 20/22 answers equal and mean abs diff ≤ 0.03, i.e. inside the drift our own
  engine configs already show. Then the hosted model is JEV for our purposes.
- Works, pplx-decider: a different model, so its probabilities will not match JEV's calibration.
  ≥ 18/22 answers equal is a pass for run 1; disagreements go to Nick as design reads, the
  `jev-design-decisions` way, before any switch.
- Idea failure: the API cannot give a distribution over our options (no logprobs over chosen tokens,
  no `allowed_token_ids` or equivalent, no native decision endpoint), or answers flip on the
  structural steps (dimension, camera, movement model, win/lose).
- Watch: a shared server batches requests, which moved JEV up to 0.077 on our own engine. The
  `mechanics` step (~60 items on `keep_over 0.6`) is where that shows first.

## Setup

To do before the run:

1. Keys: Perplexity (Nick, 2026-11-06) and TypeSafe in `~/api_keys/`. Read neither into logs.
2. From each provider's docs: is TypeSafe's Jev the same weights as JEV-27B-VL (autotrust, LoRA plus
   `lm_head` decision head on Qwen3.8-27B)? How does each return a distribution over our options:
   logprobs with `allowed_token_ids` (JEV's documented OpenAI path), top logprobs, or a native
   decision call? Does either take images (JEV-27B-VL is VL; the chain is text-only today)?
3. Pull the two control games' `decisions.json` from prod (read-only).
4. `run.py`: replay each control chain's prompts in order, carrying the control's answers into each
   next step's state so every step is compared on identical input, apply JEV's bias and per-kind
   temperature only where the provider returns raw logprobs, and write per-step answers and
   probabilities plus the comparison table to `run1/`.

```
venv/bin/python run.py --provider typesafe --games 26b16c2ea111 fe87fce4707a
venv/bin/python run.py --provider perplexity --games 26b16c2ea111 fe87fce4707a
```

Cost: cents.

## Log

## Outcome
