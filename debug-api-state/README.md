# debug-api-state

Status: planned
Control: tr-gta6 and tr-skatemall (labs/vision-build, 2026-10-25), the same chain with relook and
trace, on the current design prompt.

## Purpose

labs/vision-build's `trace` gives a retry the looker's last inputs with what `window.__game`'s
state did after each. It is only as good as that state.
- **tr-skatemall:** `state()` carried player position, hp and state. The trace showed `hold w:
  player.pos.x -> 29.4` and `e: nothing changed` at a locked exit, and the next retry fixed it.
- **tr-gta6:** `state()` carried static fields only. Every input, walking included, read
  "nothing in window.__game's state changed". Across rl-gta6, v23-gta6 and tr-gta6 the
  quest-dialogue miss was reported eight times and the enemies-never-die miss six, and neither
  was fixed.

labs/vision-build's `teleport` hit the same wall. tl-carts at stage 5 exposed only `hud`,
`keymap`, `drive`, `release`, `render` and `resize`, with nothing to travel or set time with,
though B6's finished carts carried about 100 debug functions. In staged builds the API grows
stage by stage, so the deep stages that most need travel run on the thinnest API.

The design prompt's section 8 (`src/maestro/codegen/prompts/design/write.txt`) asks for "One
function per gameplay system that reaches its state directly, and the player's inputs as
functions". It never asks for one live snapshot of what is happening.

## Hypothesis

Section 8 also asks for travel and setup functions (start a level, warp to a place, set the clock, grant score), built with the stage that adds each system, and for a `state()` that returns the live state a player would see: the player
(position, health, lives), every enemy and interactable (position, health, alive), score and
resources, and the current screen. With that, traces carry the cause of a dead input (`e:
nothing changed` beside `npc.talking: false`, `enemies[0].hp` stuck), and retries fix named
misses more often.

Measured, on gta6 (the worst diagnosis-gap design) and one more:
- the share of trace steps with a state change;
- named misses fixed on the traced retry, against tr-gta6's 0 of the dialogue and enemy-death
  misses;
- the chain's retries and time.

Idea failure: richer traces and the same unfixed misses.

## Setup

One sentence added to section 8 of the design prompt, written as a general law with no game in
it (per prompt-generality). A new gta6 design from the same ask, then chain.py with `relook` and
`trace` as tr-gta6 ran. One run first.

## Log

## Outcome
