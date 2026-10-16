# split-questions

Status: single-run
Control: refine-passes r1's `design_refine` pass (bd4f3bf), one open "what do you need, decide,
update" pass on the same seed and model.

## Purpose

refine-passes closed inconclusive, but its passes showed a pattern. A context that both asks
and answers asks what it can already answer. The visual and sound refines spent hundreds of
lines on contrast ratios and dBFS, which the model can measure. They missed what a player
feels: r1's hold-to-pivot lands on a facing that reads as random, and its rhythm feedback
"felt inconsistent". No pass asked a game-design question at all; every one refined for
correctness. Every design pass also wrote code nobody asked for, and r0's whole stack came out
of a figure script.

The smallhours design that Nick rated "much much better than chathub" came from the same loop
with the roles split: a fresh context only asked questions, and a different party answered
them. Nick will not be the answerer (the pipeline runs without a human), so here the answerer
is the model, given the original request as the only source of intent.

## Hypothesis

Split refinement into separate fresh contexts:

1. `ask_need`: what do you need to know to build this? Questions only, to QUESTIONS_NEED.md.
2. `ask_better`: what would make this a better game? Questions only, to QUESTIONS_BETTER.md.
3. `answer`: given ASK.md, DESIGN.md and both question files, answer every question in
   ANSWERS.md, then update DESIGN.md. Design only, no code.

An asker that will never answer is free to ask the hard questions. An answerer handed a list
must commit to each one, instead of choosing what to work on. The "better" asker asks the
game-design questions no refine pass asked.

Measured against the hole list in `holes.md`, holes the seed is known to have, each scored
0/1/2 (missed / asked / settled):

- K and L, the holes that only building and playing found: one round of the split should
  score above r1's design_refine, which left both unsettled.
- A-J, the holes r1's design_refine already settled: the split should not lose them.
- Secondary: whether the asker passes leave DESIGN.md alone and write no code (the runner stops
  if an asker edits DESIGN.md), and what the "better" questions are. Nick reads those, because
  the hole list cannot score taste.

Idea failure: the split scores no higher than r1 on K and L, or the "better" questions are generic
(add more enemies, add a story) rather than about this game's feel.

Only if it clearly wins: build once and play it, then try it on the prod design chain over the
usual battery. The hole list exists only because this seed was built and played twice, so it
is a one-game check, not a general metric.

## Setup

Model: basalt, Flash-Next IQ3 local on the 5090, via llama-swap on :5001. Harness: Nick's
`coding-agent` CLI with file tools only, no `--shell`. That differs from refine-passes, which
ran with a shell. A design pass has no use for one, and it is the "no code" ask enforced by the
harness rather than by the prompt. `drive.py` is refine-passes' driver with that flag dropped.
It keeps the judge and continue loop, and refine-passes raised coding-agent's round cap to 2000.

Seed: `refine-passes/r0/DESIGN.md` at d0ee945, the same seed both refine-passes arms started
from. `ASK.md` is `prompts/design.txt`, the request the seed was designed from.

Run: `./run.sh <arm> [rounds] [first pass]`, e.g. `./run.sh s1 1`. One fresh coding-agent per
pass, and one commit per pass titled `split-questions <arm>: round <n> <pass>`. The question
files are overwritten each round, so `git log -p -- <arm>/` holds every round's questions and
answers.

## Log

## Outcome
