# jev-play-probe

Status: done
Control: the owner's hand verdicts on the 2026-08-22 lib experiment builds (`runs.txt`); the
play gate (`src/maestro/codegen/play_gate.py`) as it ships, on the same builds, if run 1 works.

## Purpose

The games that fail people pass every gate, and they fail in ways you only see while playing
(experiments.md, the critic rubric entry): "an unreachable state, and a control scheme that is
wrong only once a body is attached to it." The lib experiment's hand play lists six more: a
blank page, a title overlay that never leaves, a Begin button nothing can reach, inverted
camera yaw, every direction walking into the screen, and a spawn on an unwalkable tile.

The play gate already presses inputs, but through a VLM writing free-text JSON turns: about
ten presses, no confidence, and the 2026-09-06 ruling closed feeding its judgment back "until
the player can play." JEV-27B-VL (`/var/lib/models/jev/JEV-27B-VL`, Apache-2.0, a LoRA plus
decision head on Qwen3.8-27B) answers typed questions over images with calibrated probabilities
in ~250 ms. Its own card says that inside a control loop it works on small visual questions and
fails when asked to pick motor commands directly. That is the shape of a broken-input probe:
the harness presses, and the model only judges what changed between two screenshots.

## Hypothesis

On the 14 builds in `runs.txt`, the probe's answers match the owner's verdict on the defects it
can reach: did the game start, did each movement key move the player or view the way its name
says, can you see anything. Reachable defects are the dead arcade, npcs and rhythm lib builds,
both indoor3d builds and the npcs rebuild. The placement bug in lib cards is out of reach and
doesn't count.

Works: every reachable defect flagged at p ≥ 0.7, and no false "broken" on the five builds the
owner says play (control arcade, control platformer, lib platformer, lib-fix arcade, control
npcs).
Idea failure: it misses the stuck-title builds (the start question can't tell a title screen
from gameplay), or it calls the playing games broken. The second is the critic's "6/5 every
time" failure turned around, and it's the one to watch for.

Run 1 is a single build: `085e8b97077f` (lib rhythm, title never leaves). The probe has to say
"never started" with all three start inputs tried.

## Setup

No change to the build. The probe reuses the error gate's server, browser and page
(`error_gate._serve/_browser/_open`), so it sees the page the gates see. Steps:

1. Screenshot. JEV picks which input starts the game, from the visible buttons' text plus
   Enter, Space and a centre click (`questions/start.txt`). Up to three are tried, best first.
   After each one, a before/after pair goes to `questions/started.txt` (yes/no).
2. Each of W A S D and the arrows is held 500 ms. The before/after pair goes to
   `questions/moved.txt` (choice of 10).
3. The last screen goes to `questions/visible.txt` (yes/no).

The questions are text files so they can be climbed. Clicks land at screen coordinates, so a
canvas covering a button absorbs the click the way it absorbs a person's.

Model: JEV-27B-VL System 1 on the local 5090. bf16 is 54 GB and doesn't fit, so it needs the
`JEV-27B-VL-NVFP4` backbone with `adapter_vllm`. Serving is open (see Log). Nothing else may
hold the card (`scripts/local_gpu.py`).

    ../../venv/bin/python probe.py 085e8b97077f --jev http://127.0.0.1:8101

Screens and `report.json` go to `~/output/jev-play-probe/<run_id>/`.

## Log

2026-10-13 — Lab set up. Ground-truth run ids recovered from `~/output/runs` by request text,
lib imports and bug signatures: lib rhythm has `#title .hidden`, the dead lib arcade and npcs
still carry the old `canvas.js` with `position:fixed` plus `appendChild`, and lib cards has the
`handleClick` without placement. Control indoor3d is either `5cfe6c7b94c0` or `8b294a0daa68`
(same ask, both done, 21 vs 41 steps); the owner has to confirm which one was played.
`~/Documents/decision-model-test` (sglang + `decide.py`) was emptied today, so how JEV gets
served for run 1 is still to be decided.

2026-10-14 — Serving: JEV-27B-VL now lives in `~/Documents/AI-Launcher/jev/` (sglang :8100 with the
`jev-decision` LoRA, `decide.py` on :8101 applying the decision head), started by llama-swap model
`jev-27b-vl` through gpuswap (CRIU restore ~11 s). `--jev` now defaults to :8101. Load it first
with any request for `jev-27b-vl` on :5001; `decide.py` calls bypass llama-swap, so its 300 s TTL
can unload JEV mid-run. sglang's own `/v1/systemone` is not a substitute: it reads the base
lm_head without JEV's head or calibration, and disagrees with `decide.py` on 2 of 5 text checks.

Run 1, `085e8b97077f` (lib rhythm, title never leaves): works. Start pick "press Enter" 0.99; all
three start tries (Enter, centre click, Space) answered started ≤ 0.005, and the screens confirm
the "PRESS ENTER TO START" title stayed up every time. Moves: "nothing changed" or "something
changed, but not the player's position or the view" on all eight keys (p 0.64–0.96); every pair
differs in bytes (the title glow animates), so neither answer is wrong. visible 0.54, an honest
coin flip on a title screen. Not covered: the game's own keys are D F J K, which the move set
never presses. Timing on the 5090: 0.27 s for the start pick (one screen plus the design), 0.33–0.40 s
per before/after pair, 0.15 s for one screen; 24.5 s for the run including an 11.6 s JEV restore.

2026-10-14 — Battery, the other 13 builds (5 min 5 s, ~23 s a build). Control indoor3d run as
`5cfe6c7b94c0`, still unconfirmed. Against the hypothesis, mixed.

Reachable defects, 2 of 6 caught at p ≥ 0.7, 1 partly:
- `085e8b97077f` rhythm, title stuck: caught (run 1).
- `9c789de05052` npcs, Begin unreachable: caught through the moves, all eight "nothing changed"
  at 0.93; the start question said started 0.74 after Enter.
- `54ae8aa9a571` npcs rebuild, unwalkable spawn: partly, "nothing changed" on 7 of 8 keys but
  only 4 of them at ≥ 0.7.
- `0b0b2ac24e99` dead arcade: missed. Headless, Enter starts it (Score, Wave 1, hearts appear):
  the defect was the covered LAUNCH button, which a key press walks around. No ship is visible
  afterwards, yet JEV answered "the player moved" at 0.83–0.91 for w, a, s and ArrowUp; it read
  the drifting starfield as the player. A false pass, not just a miss.
- `5cfe6c7b94c0` and `3a1c40a05150` indoor3d (walks into the screen; yaw inverted): missed.
  Forward, backward and turn answers scatter at p 0.19–0.56 with no pattern across keys. Two
  frames half a second apart of a first-person scene don't carry camera motion JEV can read.

The five builds that play: no false "broken". All started at ≥ 0.99, and none got the all-keys
"nothing changed" pattern. Platformers' left/right matched at 0.95–1.00 (`1b57ae46e6cb`,
`f78fd2e54349`), top-down arcade and npcs mostly matched (`89b96c6bedf4`, `88bb1e96e07c`), the
control arcade had two wrong moves (w and ArrowUp "moved left", 0.49 and 0.88; `2a72e5ad505c`).

Out of scope as expected: both cards builds "nothing changed" at 1.00 on every key, control
rhythm started 0.78 with "something changed" on every key.

`visible` separates nothing: 0.40–0.88 on playing builds, 0.48–0.60 on the dead ones.

Reading: on 2D games JEV is a reliable "did the game start" and "does any key do anything"
check, fast and without false alarms on these five. It does not judge first-person camera
motion, and it will invent player movement in a scene with no player when something else
moves. Fix candidates: the start step should try the visible button with the mouse before
keys, as a person would; the moves question needs a "no player visible" option; 3D likely needs
more frames or a different question, or is out of reach.

## Outcome

Closed 2026-10-18 without a write-up here: stale. Any result it reached is in docs/experiments.md.
