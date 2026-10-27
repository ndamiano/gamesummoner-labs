# qev-decide

Status: done (idea failure)
Control: JEV-27B-VL's decisions on the current prod chain (`src/maestro/codegen/prompts/design/decisions.json`,
unchanged since 76040ca) for "A game about frogs eating bugs": runs 632bb49dbb5b, 3170a8a2b4c3, 33db73007732 in
`~/output/runs/<id>/design/decisions.json`. Three runs of one ask, so JEV's own run-to-run spread is the yardstick.

## Purpose

The decide step is JEV-27B-VL: a 27B model on its own box (a PRO 6000 or a g7e), serial at ~68 ms per read, about
16 s per chain, and a cold boot of ~120 s per game on prod because the box is almost never warm
(`labs/decide-image-cotenancy`, `labs/jev-on-flash-next`). The decide chain is text only (`contract/decide.py`
builds a string state). qev-0.8b (labqoat, Apache-2.0, a full fine-tune of Qwen3.5-0.8B-Base, 1.7 GB bf16) is a
System One model with no text generation: choice / noul / score in one forward pass, 3.5 ms p50 on an L40S per its
card, first of 27 ~1B decision models on its Benchmark Heaven (77.1%), JevBench 85.1, ECE 0.063 (JEV-27B-VL: 0.019
on a different board; no shared benchmark). At 1.7 GB it could sit beside the llm engine on the llm box, or on CPU,
and decide would stop needing a box of its own.

## Hypothesis

qev-0.8b, through the prod chain executor (`run_chain`, the >16-option tournament included), makes design
decisions that read as plausibly as JEV-27B-VL's for the same ask: the frame calls (dimension, camera, time model,
movement, session shape, failure, tone, size, win/lose) mostly land on one of JEV's answers, and the kept mechanics
overlap JEV's about as much as JEV's three runs overlap each other.

Measured: frame calls equal to any JEV run; mechanics kept and overlap with each JEV run; first-playable top five;
chain wall time on CPU.

Idea failure: frame calls that read wrong for the ask (the 9B's "eerie fridge" class), or a mechanics keep set that is
near-empty or near-everything (calibration does not transfer to these questions, so `keep_over 0.6` means nothing).
Its card warns: no reasoning, weaker on long inputs, and the chain's state grows with every answer.

Fit beside Flash-Next: the local 5090 has Basalt at 29.4 GB with `--vram-elastic --vram-reserve-mib 1200`; ~1.5 GB is
free and it is Basalt's reserve. qev on GPU needs Basalt to lend VRAM (`POST /v1/vram {"reserve_mib": N}`, between
requests, shrinking the expert cache) which costs Flash-Next tok/s. Measured separately, only while no build runs.

## Setup

No prod change. qev is wrapped as `read(kind, state, questions)` for the prod `run_chain`; each read is one qev call
with every question in it, `per_question=True` (one row per question, each with its own state copy, as JEV reads).
Choice questions pass their options as criteria with no descriptions.

- Model: `/var/lib/models/qev/qev-0.8b` (`hf download labqoat/qev-0.8b`; weights and code match its SHA256SUMS,
  README and header.jpg do not, edited after). Venv `/var/lib/models/qev/venv`: torch 2.13.0 cu130, transformers
  5.17.0, decider-ai 1.9.0, flash-linear-attention 0.5.2.
- Chain payload: `chain_frogs.json`, made by the prod `maestro.codegen.design.chain(ask)`.
- CPU run (fla hidden, GPU hidden):

```
CUDA_VISIBLE_DEVICES= ../rig-lab/safe -m 8G /var/lib/models/qev/venv/bin/python -I run.py chain_frogs.json \
  runs/frogs_cpu.json ~/output/runs/{632bb49dbb5b,3170a8a2b4c3,33db73007732}/design/decisions.json
```

## Log

2026-10-20, run 1, CPU (`runs/frogs_cpu.txt`, `runs/frogs_cpu.json`). Load 3.3 s, chain 56.4 s, 201 questions in
20 reads (bf16, transformers backend, no fla). Frame calls: 6/9 equal to all three JEV runs (dimension, camera, time
model, movement, tone, size); misses read wrong for the ask: session shape open world (JEV endless), failure "no
failure", music none. JEV's three runs agree with each other on every frame call. Keep lists: qev kept 1 of 157
mechanics (jump; JEV 20-21 each run), and 0 screens, hud, effects, accessibility (JEV 5 / 3 / 3 / 4). Its noul
probabilities sit low (mechanics median 0.04 vs JEV 0.22; screens 0.03 vs 0.78) and rank wrong, not just low:
correlation with JEV 0.49 on mechanics, 0.32-0.47 on screens / hud / effects, -0.06 on accessibility; top mechanics
jump, dodge, dash, hunger, plot, where JEV leads with score, chase and catch, high scores.

Wrapper check, same day: obvious nouls answer right (frog eats bugs 0.96-0.98, tank 0.00), so the read is wired
correctly. Given the state the mechanics step saw, with qev's frame or JEV's own frame (~280 chars, not a long input),
the answers are the same: title screen 0.85 on the bare prompt drops to 0.06-0.12 once the frame lines are in the
state, chase and catch 0.32, score 0.29-0.34. The cascade is not the cause; the model's design judgment is.

Verdict: idea failure on this chain. A lower keep_over would not fix it, since the ranking is wrong as well as the
level. GPU fit beside Basalt not measured: a build was live on Basalt (100% util) and the quality result makes it moot.

2026-10-20, run 2, flymy-ai/decision-2b-preview (`runs/frogs_d2b.txt`, `runs/frogs_d2b.json`), same chain and
control, `run.py --engine d2b --device cuda`. A LoRA plus pointer head on openbmb/MiniCPM5-2B (base fetched at the
pinned revision to `/var/lib/models/decision-2b/base`, hash matches); venv `/var/lib/models/decision-2b/venv`
(torch 2.8.0 cu128, the card's pins). qev's board lists it ahead of qev on ECE (0.042) and JevBench (86.0). Licence:
code and weights Apache-2.0, but `provenance-review.json` is BENCHMARK_PREVIEW_AUTHORIZED_WITH_UNRESOLVED_PROVENANCE
(no commercial clearance claimed; unresolved Gigaword-derived records, and 543 synthetic records authored by
claude-fable-5-1 under an unestablished provider contract). Evaluation is expressly permitted; prod use is not
cleared.

Beside Flash-Next on the local 5090: Basalt idle since 15:46, `POST /v1/vram {"reserve_mib": 6500}` shrank its expert
cache 19,555 -> 13,824 MiB (10,067 -> 7,117 slots), 6.4 GB free. decision-2b loaded in 11.1 s and ran the whole chain
in 4.8 s (202 questions, ~24 ms each; JEV ~16 s on its own box). Flash-Next decode with the cache lent, same 600-token
prompt twice: 151 then 193 tok/s (hit rate 77% then 88%, the adaptive tier refilling); restored: 255 and 254 tok/s
(94%). Restore came back to 9,753 of 10,067 slots: free VRAM 1,352 MiB against the 1,200 reserve, one 512 MiB segment
short; decode is at baseline anyway.

Quality: frame 4/9 equal to JEV (dimension, camera, tone, size); misses read wrong for the ask (turn-based,
grid-based, single screen, restart the level, no music). Keep lists collapse as with qev: mechanics hunger and waves
(JEV 20-21), first playable waves 0.90, 0 screens / hud / effects / accessibility, 0 of JEV's 3 win/lose. Noul
medians 0.09-0.42 against JEV's 0.22-0.79, correlation with JEV -0.42 to 0.84 (hud negative, screens 0.06).

Verdict: idea failure for the chain as written, same shape as qev. Two ~1-2B decision models from different bases
both reject nearly every design item; the questions are calibrated to JEV, and these models were trained on business
and benchmark decisions, not game design. Cotenancy works mechanically: a 2B decision model fits beside Flash-Next
on a 32 GB card by lending ~6 GB, at ~25% decode cost while lent on the 5090.

## Outcome

Idea failure. Neither small decision model can stand in for JEV-27B-VL on the design chain: qev-0.8b
kept 1 of 157 mechanics and decision-2b kept 2, against JEV's 20-21, with frame misses that read
wrong for the ask, and probabilities that rank the items wrong as well as sit low. The questions
are calibrated to JEV, and both models were trained on business and benchmark decisions, not game
design. Nothing shipped. What carries over: a ~2B decision model fits beside Flash-Next on the 5090
by lending Basalt ~6 GB, at ~25% decode while lent and back to baseline on restore, so cotenancy is
open to a model whose judgment holds (labs/jev-on-flash-next, labs/decide-image-cotenancy).
decision-2b is cleared for evaluation only. experiments.md: 2026-10-20, small decision models in the
decide seat.
