# build-prompt-laws

Status: single-run done 2026-10-28, awaiting Nick's play and grade
Control: pipeline-v2's farm3 (design c1dad551e950; gated 3f28dc497d54, polished 33cb8b33fc46),
same design, chain, opts and refine loop, with the prod build prompt. Nick graded both 7.

## Purpose

The weekend's looks, refine players and Nick's blind grades (labs/grade, 2026-10-27) keep finding
the same three classes of defect, each one a game that runs and passes the gates but cannot be
played through:
- **Dropped input.** A one-frame flag cleared before the code that reads it runs: catdefense's
  `leftJustPressed` cleared every render frame, turtlecity's `overUi`, gta6's `rawTick()` clearing
  raw flags in `frame()` before the fixed-step `sample()`. Clicks and taps are lost at random.
- **A goal with no trigger, or a trigger that leads nowhere.** Nick's grades: frog ("Go in
  appears, and then it just kinda... breaks"), penguin relook (the door freezes the game), penguin
  v23b (level 2's switches can't be used), farm3 ("I don't seem to have the ability to plant the
  seeds I found"), gta6 across rl, v23 and tr (quest dialogue never starts, reported eight times).
- **Dead buttons.** Menu and settings items that do nothing: skatemall ("only movement and jumping
  of the keybinds work"), carts and gta6 overlays that cannot be closed.

`build.txt`'s `# Rules` say nothing about any of them.

## Hypothesis

Three general laws in `# Rules` (no game named, per prompt-generality), each with the play() test
that proves it:
1. An input is kept until the update that handles it has run, and cleared only after.
2. Everything the player is meant to reach or use has the code that fires when they do, and what it
   leads to loads and runs; a play() test reaches each one as a player would.
3. Every button and menu item does what it says; a play() test clicks each one.

Measured, against farm3:
- stage looks: shown, missing and unclear per stage, and misses in the three classes;
- refine: how far the player gets (the judge's reach line) and the defects it names;
- Nick's play and grade, with the farm3 builds beside it.

Idea failure: the same classes of miss at the same rate, or the laws spend the stage budgets on
tests and the stages finish less.

## Setup

- `prompts/build.txt`: the prod prompt plus the three bullets at the top of `# Rules`.
  `prompts/build_seed` links to the prod one.
- `serve_laws.py`: serve_v.py with `build_steps._PROMPTS` pointed at `prompts/`.
- `run.sh <label> <design> [HH:MM]`: waits until HH:MM, swaps the control plane to serve_laws.py
  (only with no game building), runs the staged chain as pipeline-v2 did, then three refine rounds
  on the gated copy, no UX rounds (Nick's grades could not tell UX before from after). Swaps back
  to serve_v.py.
- Queued in labs/runner: `LAB_SETTLE=fast labs/build-prompt-laws/run.sh farm3l c1dad551e950 01:00`.

Differences from the control besides the laws: prod `play_gate.py` now settles fast (f9ad520)
and the llm entries are named (BYOK), which routes the same calls to the same model.

## Log

**2026-10-28 01:00–03:05 EDT, farm3l** (design c1dad551e950, laws prompt).
- **Plan:** 9 stages, re-planned this run, so the order differs from farm3: jump is stage 3 (farm3:
  7), and day/night is gone in favour of "Finish Screens Audio".
- **Staged chain:** 83 min, final 4f9bcbaaf95f (farm3: 87 min).
  - 16 attempts across the 9 stages, against farm3's 12. The model said done on 9 of the 16;
    farm3 said done on 1 of 12, so the laws did not spend the budgets on tests.
  - Looks: 8 of 16 attempts missing (farm3: 3 of 12, all on stage 8). After retries, stages 1–6, 8
    and 9 ended shown, and stage 7 (grow and harvest) ended missing after three tries.
  - The misses are the classes the laws target: P pause dead (stage 2), Space hop never fires
    (3), E pickup removes the stack but the satchel never updates (5, twice), planting does
    nothing on E and sown beds never draw growth (7, three times), and E gathers nothing from
    bushes and rocks (8).
- **Gates** (copy e71d428f9275): 0 error rounds, 0 play rounds, nothing broken.
- **Refine**, 3 rounds of 40 steps, about 40 min:
  - Round 0, on the gated copy: the player gathered fiber and wood but never planted. farm3's
    round 0 collected 50 crops.
  - Round 1 (3eb753f38aac), judged further: planting works through B, then E, which contradicts
    the on-screen hint. Kept.
  - Rounds 2 (ba7fb0c670d9) and 3 (be7294a335c1), judged worse: the arch/gate into the next zone
    never triggers, crops never grow, and there is no goal shown.
  - Final: 3eb753f38aac. farm3's final was its gated copy, after three rounds all judged worse.
- **Served:** refined 3eb753f38aac on :9024, gated e71d428f9275 on :9025, farm3 gated
  3f28dc497d54 on :9021.

Read so far: the laws did not cut these misses. Same classes, more of them, though the stage
plans differ, so the counts are not like-for-like. Nick's play decides.

## Outcome
