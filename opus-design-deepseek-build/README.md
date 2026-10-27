# opus-design-deepseek-build

Status: single-run
Control: labs/frontier-ceiling (Opus spec + Opus build d086d499669b: "kinda insanely good", 9,
~$22; DeepSeek V4.1 Flash spec + build 01a723c0555a: "6.5, messy", $0.78). Same Opus spec built
by local Flash-Next in one conversation: labs/opus-design-flashnext-build 8fc1191a0c54 (2 in the
section-budget blind play, "a far cry from opus").

## Purpose

Opus's spec cost $1.27; its build cost ~$20. DeepSeek V4.1 Flash builds for well under a dollar.
If most of the Opus game's quality comes from the spec, an Opus spec handed to a DeepSeek builder
could land near the Opus game at roughly $2, a price GameSummoner can sell at. The 2026-08-28
design transplant arm (a stronger designer lifting a weaker builder) is the precedent. Flash-Next
on the same spec did not get there (8fc1191a0c54), but DeepSeek on its own spec already beat
Flash-Next on its own spec by a wide margin (6.5 vs awful), so the builder seat is where the two
differ.

## Hypothesis

Only the builder changes from d086d499669b: the Opus spec (`design/spec.md`, 54 KB) and the ask
are copied verbatim into a new run with no designer call (the spec already exists, so the
router's tool-less Claude rule is not needed), and DeepSeek V4.1 Flash builds it on the production
build path, 200-step cap, real build.txt, prod gates after.

Measured: done vs capped, the step "Tier completed: 1" prints at (Opus ~75), read/play/edit/write
mix, compactions, API cost, prod gate result, and Nick's blind play score against the Opus game,
the DeepSeek-spec game and 8fc1191a0c54.

Expected: a game above DeepSeek on its own spec (6.5) and below Opus (9), for under $1 of build
on top of the $1.27 spec.

Idea failure: about the DeepSeek-spec game's 6.5 or below. Then the builder carries the ceiling
and a frontier designer alone does not buy the Opus game.

## Setup

Engine: `labs/frontier-ceiling/openai_engine.py` (DeepSeek pass-through, effort xhigh → high,
peak hours doubled) with its own ledger `calls.jsonl` in this folder, behind the stock llm
contract server and the stock worker (`serve.sh`). No GPU queues: the Opus spec rules "No
external assets", and no design stage runs, so decide is never asked.

From the repo root, with `venv/bin/python run.py` up and no other llm worker:

    labs/opus-design-deepseek-build/serve.sh              # BUDGET=4 by default
    labs/opus-design-deepseek-build/build.sh d086d499669b opus-design-deepseek-build

`build.sh` is `labs/tests-in-files/build.sh` plus `designed=True` at kickoff (new runs start in
"designing" today, and kickoff refuses a build on them without it).

## Log

**2026-10-22 19:20 EDT, run 15fc2e8a0d48, implementation fix and rerun.** The kickoff's seeded
pyexec rounds died in `build.sh`'s process ("No module named 'maestro'"): pyexec builds the child's
PYTHONPATH from `sys.path`, and a `python3 -` heredoc has only `''` for the cwd, which it drops.
Paused at step 3, marked failed. `build.sh` now puts `src` on `sys.path` first, as
`labs/section-budget/run_stage.sh` does. ~$0.01.

**2026-10-22 19:23 EDT, run 57cbb0ef882d.** Opus spec from d086d499669b, DeepSeek V4.1 Flash
builder, off-peak prices, 200-step cap, stock control plane (`run.py`). Build log `build.log`.
Capped at 200 in 31 min (1833 s), never called `done()`, no "Tier completed" printed (Opus: tier 1
by ~75). 8 compactions (turns 29, 31, 45, 54, 91, 112, 123, 170). Turns by what the code did
(write beats play beats read): 58 write/edit, 51 play, 35 read, 56 other (syntax checks, listings,
python-only work). Unlike the Opus build's second half (114 reads, 3 writes), it kept writing to the
end; the last 10 turns were plays and syntax checks. 26 source files, 5065 lines, 228 KB. No media
jobs. Prod gates: error gate 0 rounds, play gate 0 rounds, nothing broken, archived. Play gate:
"Every input I tried behaved as documented": menu, a four-beat intro, arrow moves spending the
MOVE counter, a +25 fish-bone pickup, E ending the turn with a fresh hand; it never resolved a card.
Title "WHISKER WIZARD: TOWER OF YARN". Cost: $0.35 for 219 calls and 310K output tokens,
including the ~$0.01 false start. With the $1.27 spec, $1.62 a game.
Our screenshots (/var/tmp/odd/b1_*.png): clean title, floor 1 is the spec's side-on floor with
ladders, pickups, a hand of five cards (Pounce, Zap, Scramble) and an End Turn button. Served on
http://127.0.0.1:8935. Awaiting Nick's play verdict.

**2026-10-22 19:50 EDT, second arm, chain dsA25.** Deliberate addition beyond one run, picked
while Nick was away: the same Opus spec and DeepSeek builder through labs/section-budget's arm A
chain (the spec's 11 build-order steps, one fresh 25-turn agent each, our check after each stage,
a broken stage rerun from the snapshot before it up to 2 times, then the prod gates on a copy).
Same STAGE_OPTS as the Flash-Next armA25 chain; `serve.py` in place of run.py, this lab's
`serve.sh` behind it. Rows in `labs/section-budget/chains.jsonl` (label dsA25), log
`/var/tmp/section-budget/dsA25.log`.
- Stages 1–5 passed first try (stage 1 called `done()` at 19 turns; stage 3 moved, ended turns
  and took fall damage). Stage 4's main.js rewrite (snapshot bfe5a11) dropped the
  `requestAnimationFrame(frame)` at the end of `frame()`, so the page ran exactly one frame:
  `G.tick` stayed 0, arrows and E queued input nothing ever drained. The builder never saw it:
  its plays step the game through the debug API. Our check flags it only from stage 6
  (`turns_from` 6), so stages 6–11 all failed it and each burned both retries.
- `chain.py` keeps the last attempt when all three fail, even when it is worse. Stage 8's third
  attempt did not boot ("grid is not defined"), so stages 9–11 built on a game that never loaded
  (errors drifted between "grid is not defined", duplicate `CFG` and `rewardSignature`
  declarations). Stage 11's second attempt (fa871983fc53) booted clean and was dropped for the
  third, which did not. Chain lever, not a builder one: keep the best attempt (boots, fewest
  check failures), not the last.
- Totals: 23 stage runs (11 stages, 12 retries), 569 turns, 73 min, $0.75. Final cfd042e82160.
- Prod gates on copy a979f204cf09: error gate fixed the boot in 1 round (27 steps); play gate
  reported 11 broken inputs, first "press e (documented END TURN key)", the stage 4 bug; three
  more fix builds (25, 51, 41 steps); the last play gate left 3 broken inputs (first: backtick,
  a debug key) and handed it to a human. 4 fix builds, 144 steps, $0.19. After the fixes the loop
  runs (our probe: arrow moves Mittens, E ends turn 1 → 2, a card plays, no page errors). 22 source
  files, 6474 lines.
- Whole arm: $0.94 build + gates, $2.21 with the spec.
Read: the staged chain did not protect a DeepSeek build the way it protected Flash-Next (armA25: 1
retry, gates clean with 0 rounds). One silent loop break early, invisible to a builder that
tests through the debug API, plus a keep-the-last retry rule, turned 6 of 11 stages into
retries. The prod gates rescued it, which the one-conversation build did not need.

**To play, blind:** http://127.0.0.1:8941 … 8943: the one-conversation DeepSeek game
(57cbb0ef882d), the gated dsA25 game (a979f204cf09) and the Opus game (d086d499669b, Nick 9),
shuffled. Key: /var/tmp/odd/blind_key.txt.

## Outcome
