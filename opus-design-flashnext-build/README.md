# opus-design-flashnext-build

Status: single-run
Control: labs/frontier-ceiling. Opus spec + Opus build d086d499669b (Nick: 9, "kinda insanely
good"). Flash-Next spec + Flash-Next build 524b1c3efa1c, same ask, local 5090 (Nick: "awful").

## Purpose

frontier-ceiling found the model is the gap, but it swapped the model in both seats at once, so
it cannot say whether the gap is in the spec or in the build. The 2026-08-28 transplant arm
(Flash-Next designs built by the local 27B, 10/10 gated) showed a stronger designer can lift a
weaker builder. Opus's spec cost $1.27 and its build ~$20. If most of the Opus game's quality
lives in the spec, a frontier spec plus our own builder is a price we can sell at.

## Hypothesis

Only the builder changes from d086d499669b: the Opus spec (`design/spec.md`, 54 KB) and request
line are copied verbatim into a new run, with no designer call, and local Flash-Next builds it on
the production build path.

Measured: done vs capped, the step "Tier completed: 1" prints at (Opus ~75, Flash-Next control
~155), read/play/edit/write mix, and Nick's play score against both controls.

Expected: a game clearly above the Flash-Next control (awful) and below the Opus game (9). The
Opus spec is tighter than Flash-Next's (gameplay ~175 lines vs ~925), so the builder has less
to carry. It should reach tier 1 earlier than ~155.

Idea failure: about as bad as the Flash-Next control. Then the builder carries the ceiling, the
spec does not, and a frontier designer alone is not the lever.

## Setup

No API spend: the spec already exists. Local 5090, basalt Flash-Next IQ3_S (settings.json llm
alias `qwen3.8-flash-next-basalt`), stock `scripts/local_gpu.py auto`, real build.txt.

Known difference from the controls: build.txt changed after both ran (b5d0788 retired anims, 5
lines). The Opus spec rules "no external assets", so the anim lines should not come into play.

From the repo root, with `venv/bin/python run.py` and
`venv/bin/python scripts/local_gpu.py auto --idle-exit 300 --ready-timeout 600` up:

    labs/tests-in-files/build.sh d086d499669b opus-design-flashnext-build

## Log

**2026-10-19 22:26 EDT, run 8fc1191a0c54.** Opus spec from d086d499669b, local Basalt IQ3_S
(served through llama-swap :5001, `start-basalt.sh` with `basalt-iq3s.json`; same weights as the
control), 200-step cap. Control plane restarted onto e3f72fa first. Build log in `build.log`.
Build: capped at 200 in ~28 min, never called done, no "Tier completed" printed, 5 compactions
(Opus: tier 1 by ~75; Flash-Next control: ~155). No media jobs. After finalize the reaper logged
"re-advancing stuck build … its driver was lost mid-turn" 7 times, bumping steps to 207 (harness
bug, likely `build.sh` driving the build outside the control plane; not chased). Play gate: 3
broken inputs → fix round. The fix round thrashed: 82 edits, 63 plays, failed edits on
`src/cards.js`, then ~30 steps of re-reads and empty calls after a 6th compaction. Stopped by
hand at fix step 126 (23:04). Awaiting Nick's play verdict.
Correction on the fix round: the play gate went clean ("inputs clean after 1 fix round") and the
game archived around fix step 7, twice back to back; the ~115 thrashing steps after that look like
a second driver left by the reaper's re-advances, not real fix work. Main build timing: 22:26:23
to ~22:50:40, ~24 min, ~7 s/step. Not thrashing: per 25-step bucket, writes/edits never fell below
2 (64 total), plays 49, read-only 93, failed/empty calls 25; compactions at steps 34, 55, 99, 119,
170 with read bursts after each. It ran out of steps with tier 1 unfinished.
Nick, playing it: "quite a bit better" than the Flash-Next control, "a far cry from opus",
"clearly not finished"; UX "seemingly better than opus"; "needs more time to cook".
Failure forensics (replayed every write/edit from turns.jsonl into a scratch copy; the replay
reproduced all 12 failed edits on the same turns). Edits: 1 identical old/new, 1 old_text found
twice, 10 old_text not in the file and never in any earlier version of it. The model typed what it
remembered the code saying (renamed locals, reordered imports, `src=` vs `./src=`, a function that
never existed, code that lives in another file), several right after a compaction and two one
turn after reading the file. Plays: 2 broken test scripts (redeclared `ex`, `import` inside the
play script); 2 real game bugs the tests caught (`e.def.resists` undefined in `elementMod`, null
target in `cards.js` apply); 7 from one boot break, steps ~120–129. A rewrite of `enemies.js`
dropped the `actBoss` export that `debug.js` imports, so the module graph failed to load and
play() reported only "window.__game never appeared within 10 s"; 4 of the 7 are Python
TypeErrors from indexing that error string as a dict. The model found the cause only after
editing an error catcher into index.html. Harness lever, out of scope here: when `__game` never
appears, play() should return the page's load errors.

**2026-10-19 23:21 EDT, build 5f5b08e81510 on the same run.** Nick: "needs more time to cook".
A second 200-step build over the build-1 files, through `build_chain.kickoff(rid, kind="build")`
(no `fresh`, so files kept; same request line and spec; fresh context). Build-1 game snapshotted
to `~/output/snapshots/8fc1191a0c54-build1`.
Capped at 200 at ~23:40 (~19 min), no "Tier completed", compactions at 34, 89, 129, 161, 185.
Mostly reading: 34 write/edit steps (build 1: 64), 16 clean plays, 5 failed edits, 6 failed
plays, 1 empty, 1 refused; src 312 → 336 KB, 16 files differ from build 1.
The reaper fired again after the cap (8 re-advances, 15 total on this run), so the ghost driver
is not from `build.sh`: this build was kicked by a one-shot `kickoff()` and driven by the control
plane. Each re-advance re-finalized the build, and each finalize ran its own play gate: the log
shows concurrent gates ("inputs clean after 2 fix round(s)" ×3, then "still failing inputs after
2 rounds — leaving it to a human") and tools=False gate LLM jobs under the finished build's id
(92 in 10 min) beside the fix build 06cb24ab0a7f. `POST /stop` ended the fix build but not those
jobs; they drained on their own by 23:44. Final state: fix build done at step 10, game archived.
Root cause (session ai-agent-test-bc, read-only): a capped build sits in phase "checking" while
gates run; `games.stuck_builds` counts only stage='build' jobs, and gate LLM jobs carry no stage,
so after 60 s the build looks dead; the reaper's `build_chain.advance` bails only on phase
"done", steps past the cap, re-finalizes, and starts another gate thread. Fix proposed there,
awaiting Nick.

## Outcome
