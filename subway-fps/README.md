# subway-fps — the Reddit subway FPS prompt, naked, on the model that made it

Status: done
Control: `labs/ashworth-street` (a 274 KB Fable 5.1 spec for the same video's prompt, built by the
local 27B in ~12 h, 11M tokens read, 3.2M written; never judged in `docs/experiments.md`), and the
2026-10-30 mainline run (`docs/experiments.md`: Flash-Next 4, DeepSeek V4.1 Flash 6.6–7, Opus 8 on
the bakery-ghost ask).

## Purpose

A Reddit post (2026-11, "inspired by Bijan Bowen's video - Subway FPS test") shows a detailed
three.js subway-station FPS with zombies, tracers, recoil and muzzle flash from one prompt,
180K generated tokens, run locally on a 5090 + 256 GB RAM box with "Deepseek v4.1 1017 UD-IQ3_S"
(Unsloth) behind the Maya backend and the OMP harness. A commenter on the same quant got two
unplayable zero-feedback runs (inverted look after a turn, zombies walking backwards, tracer from
the screen corner, too slow) that became playable after one feedback round each.

"V4.1 1017" is DeepSeek V4.1 Flash 1017 (763B; `labs/deepseek-flash-41`): the only V4.1 that fits
288 GB at IQ3_S, and the model prod's `deepseek-4.1` entry already calls through DeepSeek's API.
So the question "why do their games look better than ours" is answerable on our own harness with
the same model: hand it the same prompt, with no design chain in front, and play what comes out.

## Hypothesis

**What changes.** The ask is the Reddit prompt verbatim, and it is also the build's whole user
message and the whole of `design/design.md`: no design write, no JEV decisions, no stage plan.
Everything else is the prod build path (`build.txt`, tools, gates, 200-step cap) on the
`deepseek-4.1` entry (DeepSeek V4.1 Flash, effort high, public run so the API seat is allowed).

**Measured.** Steps and done-vs-capped, API cost, generated tokens against the post's 180K, and
Nick playing it blind on the post's own list: station detail, FPS controls (look inverts?
jump?), zombies (facing, pathing), tracers from the barrel, recoil, muzzle flash, frame rate.

**Expected.** A playable FPS of the commenter's quality (works after a fix round, not before), at
~$0.5–1. If it lands near the video's quality, the gap in our games is the prompt class (an
expert's concrete ask vs the user's garbage through a design) and not the harness; if it lands at
the bakery run's 6.6–7 with the commenter's defects, the video is a curated best-of-N and our
measurements already describe this model.

**Idea failure.** The build caps or breaks the way Flash-Next builds do (dead render loop,
nothing on screen), which would say the naked prompt needs the design chain even on this model.

## Setup

`build.py` from this folder, with `venv/bin/python run.py` up (it runs the api worker):

    venv/bin/python labs/subway-fps/build.py

It creates a public run, stores the prompt as ask, request and `design.md`, kicks the build off
with `designed=True`, starts the GPU runner for the decide and comfy queues (tier-chain's
`Services`), waits with its stall handling, and writes `build.json` here.

Prompt (`prompt.txt`), from the post:

    I want you to create a single html file with a detailed subway station 3d scene, fps controls,
    zombie enemies, tracers, recoil, muzzle flash, high details. build it with three.js

## Log

**2026-11-07 17:30 EST, run 05a120cf7a0c.** Launched as above; build seat resolved to
`deepseek-4.1` (public run). Turn 0 listed the seed; turn 1 read `docs/compose_world.md` and the
seed's `world.js`; turn 2 ruled compose_world out ("outdoor landscapes", the station is indoor)
and planned a procedural station in a 19K-token turn (15K reasoning). No art calls yet.

**17:47, done.** 52 steps, 17 min, $0.21, 64 jobs none failed; gates passed with no fix round.
Steps: 36 `play`, 5 reads, one `check_off` (its own eight rows, all from the prompt), `done`.
Output 114K tokens (48K reasoning) against the post's 180K. No `generate_media` call: one
`index.html` of 121 KB / 2,519 lines, everything procedural (canvas textures, 804 meshes,
instanced sleepers and litter, a stopped Line 7 train, 8 point lights, a carbine viewmodel,
WebAudio), plus the seed's `lib/audio.js`. Boots clean headless (no console errors); the
title screen lists WASD / sprint / jump / fire / aim / reload / flashlight; the first frame on
the platform (`shot_play2.png`) reads as the video's class: tiled walls with the green band,
columns, posters, signage, the train across the track, HUD with wave and ammo. Served for play
at `python3 -m http.server 8951` in `runtime/games/05a120cf7a0c`. Nick plays next.

**~19:00, Nick played it:** "pretty solid all things considered." So the post is real, and the
same model on our harness gets there in 17 min and $0.21 from the same prompt. Works.

**19:08, two arms to separate the ask class from the design chain** (`arms.py`, one GPU
runner, both public on `deepseek-4.1`): `ac59959e6874` = the launch-battery wizard-cat ask
("roguelike deckbuilder where you're a wizard cat climbing a tower") naked, exactly as the subway
run; `11b51c904e1b` = the subway prompt through the full prod chain (design write, JEV, stage
plan, staged build). Nick's question that motivates them: "it's not in the training data, so it
should nail any game?" — the naked wizard cat answers whether the naked path holds on an ask
with thin canonical code and real design decisions; the chained subway answers whether the design
chain costs a concrete ask its quality.

**~20:10, naked wizard cat `ac59959e6874` done.** 144 steps to `done` (68 plays, 30 edits, 25
reads, 13 writes, one `generate_media`), one gate fix round of 23 steps, $0.48, 202 jobs none
failed, 198K output tokens. "NINE LIVES": canvas title with a drawn wizard cat, a 12-floor
tower map with room choices, deck of 10, HP/gold HUD. Served at :8952. Nick plays next, against
the 2026-10-19 design-chain DeepSeek wizard cat (01a723c0555a, 6.5, "it feels so messy").

**20:12, chain subway `11b51c904e1b` done.** Design 17,395 words; 10 stages at 20–35 steps
(265 build steps), one gate fix round of 51 steps, 64 min, $0.98, 343 jobs none failed, 11
image jobs. "DEAD LINE — NIGHT SHIFT · LINE 4": title with difficulty tiers, a leaderboard,
three weapons, crowbar, dash, dodge, sneak, interact, a minimap, score. First frame on the
platform (`shot_chain_play.png`) against the naked run's (`shot_play2.png`): near-black station,
bare walls, a blocky pistol, one lit sign; the naked run's tiled walls, columns, posters and
train are gone. The design spent the prompt's "high details" on systems. Served at :8953.

| | naked subway `05a120cf7a0c` | chain subway `11b51c904e1b` | naked wizard cat `ac59959e6874` |
|---|---|---|---|
| design | the prompt (31 words) | 17,395 words | the prompt (11 words) |
| steps | 52, 0 fix rounds | 265 + 51 fix | 144 + 23 fix |
| wall / cost | 17 min / $0.21 | 64 min / $0.98 | 39 min / $0.48 |
| Nick | "pretty solid all things considered" | — | ~7, "a near 1 for 1 copy of Slay the Spire, with a worse map and probably fewer options … works fine. It's not amazing. It's just kinda fine … I'd be annoyed if I got this out, but it's probably just fine" |

**~21:30, Nick played the naked wizard cat.** ~7 (above). Against the 2026-10-19 design-chain
DeepSeek wizard cat (6.5, "so messy"): the naked build is coherent and derivative, the chained one
original and messy. The naked path reproduces the genre's canonical game: the three.js FPS demo
for the subway, Slay the Spire for the deckbuilder. Side note: Nick's Firefox profile (not a
private window either, so a pref rather than an extension) stalls this 2D-canvas game after its
first frame with no console error; the WebGL subway runs. Playwright's Firefox (fresh profile,
headed, same display) and headless Chromium play it fully.

**~21:50, Nick played the chain subway.** 6.5: "better than the plain one in many ways, and
worse in many ways."

## Outcome

Works, and the three plays settle the question that started it. The post is real: the same model
(DeepSeek V4.1 Flash 1017) on our harness builds the Reddit prompt naked in 17 min and $0.21 with
no feedback round, to a game Nick calls solid. Not memorised: what the naked path reproduces is
the genre's canonical game, the three.js FPS demo here and Slay the Spire for the wizard cat, so
"it should nail any game" is false in the way that matters — it nails any game the field has
already written a thousand times, as well as that template is written, when the ask names its
systems concretely. The design chain on the same prompt cost 4.6× and traded the ask's "high
details" for systems the ask never named (6.5); on the vague ask the chain (2026-10-19, 6.5,
messy) and the naked build (~7, derivative) are half a point apart with opposite defects.
Nothing on this model reaches Opus's 8 by either path. Section: `docs/experiments.md`
2026-11-07. Nothing shipped; what follows is the ask-class question (how a vague ask becomes a
concrete one without a 17K-word design), not a prompt line.
