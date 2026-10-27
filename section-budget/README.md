# section-budget: build in units, a fresh agent and 25 turns each

Status: planned
Control: 8fc1191a0c54 (Flash-Next building the Opus wizard-cat spec in one conversation); Opus 5.5
building it, d086d499669b, as the upper bound.

## Purpose

Most builds end at the 200-turn cap with the design's first tier or two done (labs/turn-cap). A
capped build reads 91–195 files, 70–86% of them already read, `design/design.md` (63–72 KB) 29–32
times, and writes in only 30–38% of its turns. One conversation carries the whole game: it
compacts 5–7 times and keeps re-finding its place in a design too big to hold.

Nick's idea (2026-10-21): split the design into section files and give an agent one section and a
small fixed budget: "You have 25 turns left, and your task is to complete Section 1." Lead-in is
`list_files()` and a read of the whole section. It is told how many turns it has left and can
still say done early. "Let's swing big."

## Hypothesis

Three parts, in order; each starts only once the one before it has an answer (Nick, 2026-10-21:
"the first step is figure out which decomposition is good, then we figure out how to make those
decomps, then we test everything all together").

**Part 1: which decomposition.** Hand-written decompositions of one good design, under the same
budget rules, so only the cut differs and the ceiling of each cut is what is measured.

- Design: the Opus 5.5 wizard-cat spec (`~/output/runs/d086d499669b/design.md`, 54 KB). It is
  the design ceiling we have: tight tier 1, hand-laid maps, winnable numbers. The design is not the
  limit here: Flash-Next building it in one conversation capped twice without tier 1
  (labs/opus-design-flashnext-build, 8fc1191a0c54, Nick: "a far cry from opus", "clearly not
  finished"); Opus building it reached tier 1 by ~75 (Nick: 9).
- Arm A, build-order steps: the spec's 11 tier-1 `# 10. BUILD ORDER` steps, each unit holding
  its step and the design subsections it names. The game first plays around step 6.
- Arm B, playable stages (Nick's cut): each stage ends on a game that runs and adds one system to
  it. Draft: 1 the 16×10 side-on floor from the ASCII map in pixel art; 2 Mittens, arrows, ladders,
  gravity, fall damage; 3 turns with Move points and End Turn, one Dust Bunny that walks and hits;
  4 starter deck, hand, draw/discard, Energy, Zap and Yarnball with Tab targeting; 5 intents and
  step-out whiffs, all four enemies, stomp; 6 exit, objectives, reward screen, all 5 floors; 7 the
  Grand Vacuum; 8 screens, HUD, audio, juice.
- Both arms: stage 1 is a build whose request is that unit; each later unit is a fresh build on
  the same files (`kind="change"`), the full design on disk, 25 turns, turns left shown,
  `done()` ends it early.
- Measured: does the game play after each unit; total turns; tier 1 reached; Nick's blind play
  against each other and against 8fc1191a0c54 (one conversation, same design, same builder).
  Prior evidence for arm B: staged construction (2026-08-02, the duel built alone first, then
  grown) beat single-shot.
- Idea failure: neither arm reaches a better game than 8fc1191a0c54; or later units break what
  earlier ones built.

**Part 2: making the winning decomposition.** A design-model pass or a design section that
writes the units, judged against the hand-written ones from part 1.

**Part 3: all together.** Generated units on the prod path, a battery against today's builds.

## Setup

Decided with Nick (2026-10-21): fresh agent per unit, 25 turns each, turns left shown, `done()`
early, unused turns forfeited; prod harness underneath (open-shim, in src/ 2026-10-21, not yet
committed); gates run once after the last unit. Part 1 runs keep their run dirs off eCryptfs `/home` until the output
move lands (README-UNFINISHED-OUTPUT-MOVE.md in the repo root).

Open: wording of the unit message and the turns-left line, and where the line goes.

## Overnight summary (2026-10-21, for Nick)

Arm B (playable stages) ran end to end, five times. Every chain that finished ended on a game
that boots to a title screen, starts a run, and plays: Mittens, turns, cards, four enemy types
with intents, ten valid maps, floor objectives, rewards, the Grand Vacuum. None is the finished
§11 tier 1 (sounds and every screen were never checked; floor 5 in E has two bosses).

| chain | turns/stage | stage builds | retries | `done()` | final | prod gates |
| --- | --- | --- | --- | --- | --- | --- |
| A | 25 | 12 | 3 (stages 5, 6, 9) | 2 | 9fc66fc08616 | error clean; play gate never ran clean (RAM guard, then a timeout, then a hang) |
| B | 25 | 2 | – | 1 | abandoned: stage 1 layout off-screen | – |
| C | 25 | 14 | 5 (stage 1 by eye; 5, 8, 9 ×2) | 1 | 99316c80aa3f | clean, but it tested title and settings only |
| D | 35 | 10 | 1 (stage 8) | 2 | f6376409311e | clean; 10 turns through title, run, pause, settings |
| E | 35 | 9 | 0 | 4 | ae0c184f084a (eb38d4246f16 + prod fix) | play gate round 1: pause-menu SETTINGS dead → prod fix build (116 turns) → round 2 clean |

What it says, on small numbers:

- Pre-reading the game's own files plus §2, §8, §9 is the orientation lever: stage 2's first
  write moved from ~13 to ~8 turns, first play ~22 → ~15, and only that arm gave three clean
  games of three (battery, 9 runs). A design-only pre-read did nothing.
- 25 turns is too few for the heavy stages. At 25, stage 5 broke both first tries and stage 9
  three of five tries; at 35, stage 5 passed both first tries and the two 35 chains needed 1 retry
  between them against 8.
- The turns-left lines are what make a stage stop early: without them stage 1 never called
  `done()` (0/3); with them it did 3 times of 5.
- Most stages still run their full budget (`done()` in 10 of 47 chain stage builds).
- Our checks miss things the eye does not: a blank floor with no error, a title that hides a
  dead game, an off-screen layout, two bosses. Each was caught by looking at the screenshot.

Things I did to your machine: Basalt `conversation-cache-mib` 4096 → 1536 and
`resident-budget-gib` 36 (it was refusing turns at the RAM guard); the original is restored at
wrap-up from /var/tmp/section-budget/basalt-iq3s.json.bak. The lab control plane
(`labs/section-budget/serve.py`) replaced run.py overnight; plain run.py comes back at wrap-up.

To play: five games served blind on http://127.0.0.1:8921 … 8925 (A–E): the finals of chains A, C,
D and E, and 8fc1191a0c54 (Flash-Next building the same Opus design in one 200-turn
conversation). Key: /var/tmp/section-budget/blind_key.txt. Screenshots of every stage:
/var/tmp/section-budget/shots/.

Still open from yesterday: open-shim is in src/ uncommitted and local runs on eCryptfs `/home`
cannot list directories under it (README-UNFINISHED-OUTPUT-MOVE.md in the repo root). Plain
run.py is back on that code, so a local build started now has that problem.

## Log

**2026-10-21 01:52, arm B stage 1, run 82b5825bb92f (stopped at turn 14).** Opus spec
from d086d499669b, local Flash-Next via Basalt, prod harness with open-shim in src/, stage patch
`stage.py` on `serve.py`, 25 turns. Turns 0–6 read the design, 7–9 wrote map data and a Python
BFS to validate it; no game file by turn 10. Implementation fix: stage 1 said "load all 10 maps",
but the spec gives one example map (1a) and rules, so the stage silently became "design ten
levels". Second fix: the system prompt was prod build.txt, which asks for the whole game by tier;
Nick: drop it. `stages/1.txt` now names map 1a only (the other floors come in stage 6), and
`stage.system()` swaps build.txt's opening paragraph for a stage one. Stopped by hand (Nick: "not
relevant"); rerun.

**2026-10-21 02:00, arm B stage 1 rerun, run e38cd3e57611.** Both fixes in. Done at turn 25 of
25, 299 s (`done()` in the last program, after the 3-left line). Turns 0–4 read, 5–12 wrote 10
files (index.html, style.css, data/maps.js, src/ grid, rng, state, render, pixfont, debug,
palette), 13–23 check_syntax and 7 plays with 3 edits, 24 check + done. 2 lost turns (1 direct,
1 refused). Its summary: floor 1 on a 256×160 backbuffer, integer-scaled (scale 4 at 1280×720,
smoothing off), map 1a plus validateMaps() checking the §4.1 rules. Works: the stage fits in 25,
just. Served on 127.0.0.1:8871 for Nick. The 8 plays: 3 read the canvas back as ASCII (one refused,
`__str__`), 2 broke copies of the map to test `validateMaps()` (caught all but row width, then
fixed), 2 checked crisp integer scaling (one Python slip on the result). Most of the testing went
to the validator, not the picture.

**2026-10-21 ~02:25, arm B stage 2 (Mittens), same run e38cd3e57611, build d3fe77535633.** A
build on stage 1's files (`kind="build"`, not fresh; a change build would frame it as "a person
played it and asked for this change"). Capped at 25 without `done()`, 220 s. Turns 0–11 read
(stage 1's files, design §2/§5/§7, lib/input.js, lib/audio.js, via `open()` and regex), 12–16
sprite work, 17–20 wrote/edited 4 new files and 7 old ones, 21 lost (direct), 22–24 checked and
played. Its last plays: walk, ladder up to the top, fall 7 → HP 30 → 25 (§4.4 right), short fall
no damage; but the HUD still read "HP 30/30" after the hit. Our check (Playwright, 4 × ArrowRight
on the served page): no page errors, Mittens moved 1 tile, not 4. Half the budget went to
re-learning the code: a fresh agent per stage pays ~12 turns of orientation.

**2026-10-21 ~02:45, arm B stage 2 rerun with a design pre-read, run 1b798e3a77db.** Branched
from stage 1's snapshot (e38cd3e57611 @ 5ba46f0, `branch.py`), so only the pre-read differs. One
more seeded round before the nudge prints the sections in `stages/2.reads` (§1.1, §4.4, §5, the
HUD table; 5.6 KB). Capped at 25 again, 262 s, no `done()` (turn 23's done program was a syntax
error, turn 24 empty). Orientation did not shrink: turns 0–9 still read, 10 vs 12. Turn 0 copied
the seeded `section()` helper to fetch more of the design (a name that is not a heading, so
ValueError); then the heading list, §2.2 global context, §4.6, §7, §3, index.html, render.js,
lib/input.js, lib/audio.js, fx.js, pixfont.js, maps.js. What it went looking for was the contract
(§2) and the code, not the stage's sections. Writing 11–18 (sprites.js, turn/combat/ui/input.js,
edits), 19 lost (direct), 20–21 checked and played: hold-right walks 4 tiles, death works, but the
HUD again reads "HP 30/30" at hp 0, the same bug as the first stage 2. Read: a design pre-read is
not the orientation lever; the code is.

**2026-10-21 ~02:30, arm B stage 2 again with a code-map pre-read, run 1970f7001765.** Same
stage 1 snapshot. The pre-read program now also prints §2 CONTRACTS, and its result is followed
by `code_map.render()` of the game (every file, its imports, each declaration with line ranges)
under `stages/codemap_head.txt`; the round is 17 KB, pinned. Called `done()` at turn 24 of 25,
323 s. Orientation still ~9 turns (0–8: the design twice, then index.html, style.css,
config/main/state/grid/render/debug.js, lib/input.js, lib/audio.js, maps.js, fx.js, whole files
despite the map's line ranges), sprites 10–13, writing 14–19, check and play 20–22, done 23. Our
check (Playwright, served on 127.0.0.1:8872): `DBG.setPlayer(9,3)` drops Mittens 5 tiles, HP
30 → 27 (§4.4: max(0, 5−2)), and the HUD reads "HP 27/30": the HUD bug of both earlier tries is
gone; hold-right walks; no page errors. Better stage, same orientation: the map tells it where
things are, and it still reads them whole.

**2026-10-21 ~02:40, stage 2 with the files pre-read (Nick: "I wanted prereads like that from the
get go").** First try e538e2e739a3: implementation failure, stopped at turn 5. One program printed
the sections and every file, and the runner cuts stdout at 20,000 chars (`MAX_STDOUT`), so the
pre-read stopped inside src/config.js. Fixed: the sections are one seeded program and the files
(every text file the game wrote itself, by `is_vendored`, plus `stages/2.files`: lib/input.js)
are packed as slices into programs of ≤18 KB (`stage.pieces`); the code map follows the last.
Checked in the real sandbox: 14 files, 39.6 KB in, all printed. Rerun a2c5bc7f2de9, same stage 1
snapshot: 4 pre-read rounds (11, 17.6, 17.4, 11.4 KB) after the two prod seeds, before the nudge.

**2026-10-21 ~02:45, result of a2c5bc7f2de9 (files pre-read).** Capped at 25, 324 s; its last
turn was a direct call (lost), so no `done()`. Orientation 6 turns, and targeted: 0–3 the design
parts not pre-read, by line range from the code map (§8 debug API, §9 tests, §11 done list, §4.9,
§6 audio, §7), 4–5 lib/audio.js (not pre-read; it wanted step/climb/fall sounds); no source file
re-read whole. Writing from 6, first play at 7 (earlier tries: 20+), then 17 turns of edit and
play. Our check (served 127.0.0.1:8873): 4 taps → 4 tiles, one tile per press (holding moves
one), drop from row 3 → HP 27/30 on the HUD, no page errors.

| stage 2 try | orientation | ended | HUD |
| --- | --- | --- | --- |
| none (e38cd3e57611) | 12 | cap | broken |
| design sections (1b798e3a77db) | 10 | cap (done() a syntax error) | broken |
| + §2 + code map (1970f7001765) | 9 | done() at 24 | works |
| + every source file (a2c5bc7f2de9) | 6 | cap (last turn a direct call) | works |

Single runs each. For the next stages: §8 and §9 are what it fetches for testing, and audio is
pulled in even when the stage does not name it.

**2026-10-21 ~02:50, correction on a2c5bc7f2de9.** Mittens is a solid yellow blob in that build
(no outline, no hat, no orange), idle and long after any hit, so not the 4-frame white hit flash:
the sprite renders in one colour. 1970f7001765 drew him right (orange, purple hat). My check
looked at position, HP and the HUD, never the sprite; from here every check compares a screenshot
of the sprite with §3/§5 colours. So the files pre-read saved turns, and that run's game came out
worse; one run each, so not yet a verdict on either.

**2026-10-21 ~02:55, overnight plan (Nick asleep, GPU ~8–9 h: "try as many things as you'd like").**
1. Stage 2 ×3 per arm from the stage 1 snapshot: A code map + §2, B + every source file, C = B +
   §8 + §9. My check per run includes the sprite. 2. Stages 3–8 written; two full chains from
   scratch on the winner, a check and screenshot between stages, a broken stage rerun from the
   previous snapshot (≤2), prod gates after stage 8. 3. If time: 35 turns per stage; stage 1
   without turns-left lines ×3. 4. Morning: games served blind, against 8fc1191a0c54.

**2026-10-21 03:00–03:50, stage 2 pre-read battery: 9 runs, 3 per arm, interleaved, all from the
stage 1 snapshot (e38cd3e57611 @ 5ba46f0)** (`battery.py`, rows in `results.jsonl`, our check
`check.py`: boots, page errors, design colours in the player tile, 3 taps right, a drop from row 3
with the HUD). Arms: codemap = stage sections + §2 + code map; files = + every source file the
game wrote; files89 = files + §8 DEBUG API + §9 TESTS.

| arm | turns to first write | first play | done() | game |
| --- | --- | --- | --- | --- |
| codemap | 11, 12, 17 | 22, 21, 23 | 0/3 | ok; sprite gone (white box); does not boot (`grid.js` has no `enemyAt` export) |
| files | 6, 11, 13 | 15, 20, 22 | 1/3 | outline missing; ok; ok but 3 taps moved 0 |
| files89 | 4, 7, 12 | 14, 17, 14 | 1/3 | ok; ok; ok |

Lost turns 1–2 per run everywhere. Two drops showed no fall damage (codemap 1, files89 3): either
the rule or `setPlayer` differs per build; unconfirmed. Read: pre-reading the code and §8/§9 moves
the first write from ~13 to ~8 and the first play from ~22 to ~15, and the three files89 games are
the only clean set; codemap breaks the game most. Every run but two hit the cap, so 25 turns is
tight even for stage 2. Fix on the way: battery.py imported check.py before its player lookup
learnt `G.player`, so two rows were rechecked by hand. Next: full chains on files89 (+ §2 every
stage, a 100 KB cap on the files pre-read past which only the stage's named files go in).

**2026-10-21 03:30–04:20, chain A (files89 + §2, files cap 100 KB), stages 1–6.** `chain.py`, rows
in `chains.jsonl`, screenshots in /var/tmp/section-budget/shots. Stage 1 7f41f966e4e4: done at
25. 2: capped, Mittens right, 3 taps 3 tiles. 3: capped; Dust Bunny on the top ledge, MOVE pips,
TURN counter, [E] END TURN, 3 taps → 2 tiles (2 Move points: right); HUD bar covers the exit door.
4: capped, 17 files / +832 lines; a hand of 5 HTML cards (Scramble, Zap, Yarnball, Zap, Pounce),
NRGY gems, DRAW/DISC counts, hint bar. 5: first try did not boot (`Cannot read properties of
undefined (reading '................')`, a map row); retry d0168e73eeaa from the stage 4 snapshot:
boots, bunny, pigeon, spray bottle and a fourth enemy (half under the END TURN button), intent
icons. 6: capped; a blank floor (no tiles, no Mittens, empty objective, player at 0,0) with no page
error, so the chain's broken rule (no boot or a page error) passed it and stage 7 started on it.
Implementation fixes: chain stopped; broken now also means no Mittens colours from stage 2 on;
`branch.py` snapshots a branched run (the chain reads its HEAD); `check.py` probes are guarded
(stage 1 has no DBG) and count `write_text` as a write. Stage 6 rerun from the stage 5 snapshot
(bac96cd27c60 @ 7fab84e). Every stage after 1 hit the 25-turn cap.

**2026-10-21 04:15–04:35, chain A stages 6–9.** Stage 6 rerun bac96cd27c60: boots; a new floor 1
map with two Dust Bunnies, "REACH THE EXIT (OPEN)"; the "HP 30/30" text wraps onto the energy bar.
7: `done()`; the reward screen ("FLOOR n CLEARED!", 3 offers from the 11 reward cards, rare slots
at 0.25, a met bonus forces slot 3 rare). 8: capped; our test of its snapshot (window.DBG, per
§8): `validateMaps()` → [] on all ten maps; floor 5 holds the Grand Vacuum (2×2, a face), "! SUCK"
intents, a minion, "BEAT THE GRAND VACUUM", Nova meter, score and coins; arrows move, a Zap
plays to discard, E ends the turn. 9: capped; a title screen ("WHISKER WIZARD / TOWER OF YARN",
New Run, Difficulty ◀ CAT ▶, High Scores, Settings), but Enter starts a run that throws `row[0].push
is not a function` and nothing answers after. Our check never pressed Enter, so it saw a clean
title and passed it. Fixed: the check presses Enter off a non-play screen, then plays (arrows, E)
and records the turn before and after; broken now also means E does not end the turn (stage 3
on). It catches this game (`end_turn` [1, 1], the page error). Stage 9 retried from the stage 8
snapshot (9fc66fc08616 @ a1c9729), beside chain B (from scratch, 04:30), sharing the GPU.

**2026-10-21 04:55, chain A finished: 9fc66fc08616 (stage 9 retry from the stage 8 snapshot).**
Capped at 25. Our play of it: a title screen → Enter → floor 1; arrows walk (2 Move points), cards
play to discard, E ends the turn, Esc opens a pause menu (Resume, Deck View, Settings, Abandon
Run) over the dimmed game with a stats line; combo ×2 and Nova charge on the HUD; no page errors.
Chain A in all: 9 stages, 12 stage builds (stages 5, 6 and 9 each needed one retry), 300 turns
spent, 225 on the final game's line; `done()` on stages 1 and 7 only. Prod gates not run yet.

**2026-10-21 04:45, chain B (8943165f783c) abandoned at stage 3.** Its stage 1 drew floor 1 at
the wrong scale and offset (only the top-left quarter of the map shows, pushed to the lower right of
a 1280×720 page), and stage 2's Mittens stands at x=15, off screen; our check cannot see a stage 1
layout fault (no Mittens yet) and its stage 2 sprite scan found no orange. Also an implementation
fault of ours: chain B had started on the check before it pressed Enter, so it was stopped after
stage 1 and resumed from stage 3 by a waiter (`/var/tmp/section-budget/resumeB.sh`). Restarted as
chain C from scratch; I look at each stage 1 screenshot before the chain goes on.

**2026-10-21 05:05, chain C stage 1 try 1 (df564c5e3714) rejected by eye:** platforms of map 1a, but
the two ladders are missing (a stub top left) and an orange placeholder square stands on `P`.
Rerun. Stage 1 without turns-left lines, run 1 (32540fd0ebd0): 25 turns, no `done()`, 450 s; floor
drawn whole and crisp.

**2026-10-21 05:25, stage 1 without the turns-left lines, 3 runs** (32540fd0ebd0, 92c45de6847a,
e22cfab588c1; `stage.json` countdown false, the stage message still says "You have 25 turns"):
0/3 called `done()`, 450–603 s each. With the lines, stage 1 called `done()` in 3 of 5 (e38cd3e57611,
chain A, chain B yes; chain C's two tries no). Read: the countdown is what makes a stage end early
when it does, and without it the model works to the cap; small numbers.

**2026-10-21 05:15–05:40, chain C stages 1–2, prod gates on chain A, and two mistakes of mine.**
Chain C stage 1 try 2 (22bdc4cfdb53): accepted by eye (whole-screen floor, both ladders, torches;
the model wrote maps 1a and 1b, `validateMaps()` → []). Stage 2: Mittens right, HUD panel, hint
bar. Our check missed the player there (this build's `window.__game` is the debug API itself, no
`G`), so the chain called stage 2 broken and branched a needless retry; fixed (the check tries
`__game.DBG`, `window.DBG` and `__game` for player/state), chain C resumed from stage 3 on the
good stage 2 (retry 00aa12470f11 discarded). Prod gates on chain A's final game, on a copy
without stage.json (`gates.py`, af68d3edf3ce): error gate clean (0 rounds); play gate found one
broken input on the title screen ("ArrowRight: the CAT selector should change… pixel-identical"),
then its session ended when Basalt refused a turn (`RAM low (3057 MiB free < 3192 MiB guard)`).
The fix build it started was then stopped by me by mistake at turn 9 (I took the newest run dir
for chain C's retry; it was the gate copy). So: gates not yet a clean read. Host RAM is ~3.7 GB
free against the 3.2 GB guard (Basalt 45 GB, page cache, desktop apps); I stopped my 17 game http
servers; builds run one at a time from here.

**2026-10-21 05:20, Basalt RAM settings lowered (lab infra, restore in the morning).** Eight more
`RAM low` refusals tonight (MemAvailable dips to ~3.1 GB during decode against the 3,192 MiB guard;
Basalt RSS 45 GB = 39.5 GB resident experts + up to 4 GB parked-conversation cache). Paused chain C's
build, waited for the queue to drain, set `conversation-cache-mib` 4096 → 1536 and
`resident-budget-gib` 36 in /var/lib/models/basalt/basalt-iq3s.json (original backed up at
/var/tmp/section-budget/basalt-iq3s.json.bak, identical to /var/tmp/open-shim/basalt-iq3s.json.bak),
unloaded via llama-swap `/unload`, reloaded: RSS 35 GB, MemAvailable 13.3 GB. Resumed. Decode may be
slower from here; turn counts, not seconds, are what this lab compares.

**2026-10-21 05:25–06:20, chain C stages 3–9 (22bdc4cfdb53 → fb4ce9c93673 → 1aa0902e45f2 →
99316c80aa3f).** 3: capped; End Turn advances, fall 30 → 27 on the HUD. 4: capped; a tidy HUD
panel top left (HP, Energy, Move, [E] End Turn, objective, turn), map 1a with both ladders, five
compact cards with effect text, DRAW/DISCARD; the Dust Bunny stands next to Mittens. 5: first try
threw `drawText is not defined`; retry fb4ce9c93673: all four enemy types on floor 1 (spray
bottle, pigeon, Roomba Knight, Dust Bunny) with intent arrows. 6: capped; 10 maps,
`validateMaps()` → []; floor 4 is a new layout with "DEFEAT ALL ENEMIES (5 LEFT) – THE DOOR IS
LOCKED", the bonus line and exactly the §4.1 floor 4 roster. 7: `done()`. 8: first try did not
boot (`Identifier 'shake' has already been declared`); retry 1aa0902e45f2: the Grand Vacuum (a grey
vacuum creature with a hose, "! SUCK" banner, "DEFEAT THE GRAND VACUUM (60/60 HP)"), Nova meter,
score, coins, a minion; it stands on the floor, not the `V` slot on top. 9: first try `G is not
defined` (title, Enter does nothing), retry 1 did not boot (`./audio.js` has no export `setMix`),
retry 2 99316c80aa3f works (title → Enter → play, moves, End Turn). Across chains A and C, stage
9 broke on 3 of 4 tries and stage 5 on 2 of 2 first tries: the two heaviest stages.

**2026-10-21 06:20, next:** prod gates on both finals (chain C 99316c80aa3f, then chain A again,
since the first run lost its play gate to the RAM guard and its fix build to my stop), and chain D:
the same setup at 35 turns per stage.

**2026-10-21 06:06, prod gates on chain C's final (copy 986c6adc62b1 of 99316c80aa3f): both clean,
no fix build.** Error gate 0 rounds; play gate 0 rounds, no broken input. Its playtest went title
→ SETTINGS and worked the panel: SFX volume 7 → 8, reduced motion on, colour-blind palette off
("an immediate, unmistakable visual change… the wizard cat's hat shifting from purple to red"),
difficulty CAT/HP 30 → LION/HP 25, key-remap rows, "SAVED TO THIS BROWSER". It never started a
run before the session ended ("I did not get to open HIGH SCORES, start a run…"), so play itself
is not what the gate checked. gates.py waited forever when no fix build started (nothing clears
"building"); fixed, then rerun on chain A's final.

**2026-10-21 06:50, gates on chain A's final again (copy b278dd3b9f19):** error gate clean; play
gate "session could not run (Page.screenshot: Timeout 30000ms exceeded) — build stands". The first
run on the same game took screenshots, so this looks like the headless browser competing with
chain D's own plays; rerun when the GPU is quiet.

**2026-10-21 05:55–07:00, chain D: the same setup at 35 turns per stage (87e2accafced →
f6376409311e).** 1: map 1a whole (accepted by eye), capped at 35. 2: capped; Mittens right. 3:
`done()`. 4: capped. 5: passed first try (the only first-try stage 5 of three chains): map 1b,
spray bottle and Roomba Knight with intents (not all four types in view), HP hearts drawn as dots.
6: capped. 7: `done()`. 8: first try did not boot (`Unexpected token 'export'`, first write at
turn 24 of 35); retry f6376409311e boots (first write 19). 9: passed first try: a title screen
(moonlit sky, the tower with yarn banners, New Run / Difficulty ◀ CAT ▶ with its stats / High
Scores / Settings) → Enter → play. Our look at the final: `validateMaps()` → []; floor 5 holds the
Grand Vacuum on the top platform (the `V` slot), "! SUCK 4", a minion, a locked door. Retries:
chain A 3 (stages 5, 6, 9), chain C 4 (5, 8, 9 ×2), chain D 1 (8). One chain at 35, so not yet a
verdict on the budget.

**2026-10-21 07:35, gates on chain A's final, third try (f5935bdd6a1c): error gate clean; play gate
hung** (its last LLM job 28 min old, headless browser still open); killed. Not reproduced by hand:
Enter, four turns of moves, cards and End Turn, pause, menu: no stall, no page error. Unresolved
(the second try's screenshot timeout may be the same thing). Gates on chain D's final next.

**2026-10-21 07:50, gates on chain D's final (copy 22b5c3115062 of f6376409311e): both clean, no
fix build.** Error gate 0 rounds; play gate 0 rounds, nothing broken, ten turns: "every input I
tried produced the documented visible change": title → NEW RUN → floor 1 (HUD, 5-card hand, two
enemies, ladders, exit), Escape → PAUSED (Resume, Settings, Deck View, Abandon Run), a full settings
panel (music and SFX volume, reduced motion, colour-blind palette, hints, difficulty with its
numbers, a complete key-remap table). The deepest gate pass of the three finals. Chain E started:
a second chain at 35 turns per stage.

**2026-10-21 07:20–08:25, chain E: a second chain at 35 turns (eb38d4246f16, no retries).** 1:
map 1a with yarn bunting along the top and a "FLOOR 1/5 · Reach the exit · TURN 1" strip,
`done()` at 33. 2: capped; End Turn already advances (a stage early). 3, 4 and 5: `done()` (the
first stage 4 to finish early in four chains); stage 5 shows all four enemy types with intent
arrows; the hand is drawn semi-transparent over the bottom of the playfield. 6: capped, 7 lost
turns. 7: capped. 8 and 9: passed first try. Our look at the final: `validateMaps()` → []; the
title (menu top left over the bunting tower, difficulty with its numbers); floor 5 holds TWO Grand
Vacuums, both 60/60, both "SUCK 4" (the design has one plus a Dust Bunny): a bug no check of ours
or the model's caught. Stage builds per chain: A 12 (3 retries), C 14 (5 incl. a rejected stage
1), D 10 (1), E 9 (0); `done()` calls A 2, C 1, D 2, E 4.

**2026-10-21 08:30–10:00, prod gates on chain E's final (copy ae0c184f084a of eb38d4246f16): the
full prod cycle.** Error gate clean. Play gate round 1: "click on SETTINGS (in pause menu)" did
nothing → a prod fix build (116 turns, `done()`): "each menu row carried its click handler only
on the <li>… a click landing on a child of the row… never reached that listener"; round 2 clean:
title → run → HUD, pause, deck view (POUNCE×2, PURR, SCRAMBLE×2, ZAP×4, YARNBALL with pile counts),
menu navigation. Chain E's final is the fixed copy ae0c184f084a. Correction to the 06:20 entry:
at 25 turns stage 9 broke on 3 of 5 tries (A 1 of 2, C 2 of 3), not 3 of 4. Chain F (35 turns)
started 08:44 beside the fix build: stage 1 7e1a2bfd6410 good (map 1a, torches, "FLOOR 1"),
capped; stopped at wrap-up partway.

**2026-10-21 10:05, wrap-up.** Chain F stopped after stage 2 (good: Mittens right, End Turn
works). Basalt config restored from /var/tmp/section-budget/basalt-iq3s.json.bak (identical to
the original), model unloaded; the lab control plane stopped and plain run.py restarted. The five
games served blind on 127.0.0.1:8921–8925, key in /var/tmp/section-budget/blind_key.txt.

**To check (Nick):** run stage 1 without the turns-left lines. It called `done()` only on the last
turn, right after the 3-left warning, so the budget lines may be what decides when a stage ends;
Nick expects every stage to run its full 25 (200, or ~192, for the chain).

### 2026-10-21 ~10:30: Nick's blind play, key revealed

Nick played the five served games blind (8921-8925) and scored them out of 10:

| Port | Score | Game | Nick |
|---|---|---|---|
| 8922 (B) | 8 | chain C, 25/stage, 99316c80aa3f | best |
| 8923 (C) | 7 | chain E, 35/stage + prod fix, ae0c184f084a | "not far behind B, but not great either" |
| 8925 (E) | 6 | chain D, 35/stage, f6376409311e | "the worst of the working ones, but still pretty good" |
| 8921 (A) | 4 | chain A, 25/stage, 9fc66fc08616 | fine until "some sort of seemingly infinite thing happened", which blew up Firefox |
| 8924 (D) | 2 | baseline, one 200-turn conversation, 8fc1191a0c54 | "Missing graphics makes it unplayable" |

Every stage chain beat the one-conversation baseline, three of four by 4+ points. The per-stage
budget did not order the chains: the best (8) and the worst chain (4) were both 25-turn, and the
35-turn chains sit between them. Chain A's hang is likely the same one that kept its prod play gate
from ever finishing (the hang I could not reproduce by hand), so the gate saw a real defect our
check never did. Chain C, the best by Nick's play, had the most retries (5) and its prod gates only
reached the title and settings.
**2026-10-22, arm A: build-order steps (Nick AFK a few hours, "go").** `stages_a/`: the spec's 11
tier-1 §10 BUILD ORDER steps, each step's text verbatim plus the §-sections it names as the
pre-read (`<n>.reads`, platform files in `<n>.files`), and a done line from §11. The frame differs
from arm B only in the cut ("each stage is one step of the design's §10 build order", the stage
list) and the carry line ("already has stages 1 to {prev}", since arm A's game does not play until
step 6). Everything else as chain C: files pre-read, §2/§8/§9 every stage, 100 KB cap, turns-left
lines, no gates between stages, retries ≤2 from the previous snapshot. `stage.py`, `run_stage.sh`,
`branch.py` and `chain.py` now take the stage set from `"stages"` in STAGE_OPTS (default arm B), and
the chain's broken rule takes `mittens_from` 3 and `turns_from` 6 for arm A, `last` 11. Chain
armA25 (25 turns/stage) first, then armA35 if time. Basalt `conversation-cache-mib` 1536 and
`resident-budget-gib` 36 again (backup /var/tmp/section-budget/basalt-iq3s.json.bak); serve.py in
place of run.py; local_gpu auto up.

**2026-10-22 ~02:00, implementation fix, armA25 restarted.** First stage 1 (3282d42ef059) never
queued a turn: a new run starts at running/designing, and `kickoff` without `designed=True` refuses
it, so `_await_build` waited on a build that never began. `run_stage.sh` now passes
`designed=True` when the run is still in designing (stage 1 and branched retries). Old run marked
failed; chain restarted, stage 1 a3f0d4ece00d.

**2026-10-22 ~02:30, two more implementation fixes; armA25 stage 1 recorded by hand.** Stage 1
a3f0d4ece00d ended cleanly (25 turns, `done()` on the last, first write 8, first play 19, 3 lost),
then the lab's finalize hook threw (`_settle()` now takes the build id) and the run sat at
running/checking for 20 min until the watcher flagged it. `stage.py` passes `build_id`; serve.py
restarted, which re-ran the hook and settled the run. Then `battery.shape` read
`build_state.json`, which no longer exists (the cursor is in the DB); it now uses
`build_state.load`. Stage 1's row was recorded by hand, its `seconds` an estimate. Our check: boots
clean to a title card in the §3 palette with the pixel font, the alphabet and a palette strip.
Chain resumed from stage 2.

**2026-10-22 02:00–03:10, chain armA25: arm A, 25 turns per stage, 11 stages, final
ae5a1fbe3146.** ~4 min a stage. 1: scaffold, title card in the §3 palette, `done()` at 25. 2 (grid,
all 10 maps): first try does not boot (`Unexpected identifier 's'`); retry ae5a1fbe3146 from the
stage 1 snapshot, `done()`. 3–11 all passed first try (1 retry in the chain against A 3, C 5, D 1,
E 0); `done()` at stages 1, 2 (retry) and 4 only. By stage 7 the screen is a playing floor:
Mittens in his colours, two enemies, ladders, the exit, HUD (hearts, HP, score, Energy, Move, Nova),
objective strip with a bonus objective, 5-card hand, END TURN. Final check: boots to title, Enter
→ play, E ends the turn, a drop from row 3 takes HP 30 → 24 on the HUD, no page errors. Lost turns
per stage 0–3. `gates.py` was stale the same way (`games.set_status`, `build_state.json`): it now
gives the copy a build row and a finished cursor, moves it to running/checking and calls the prod
`_post_finalize`. Gates on armA25's final (copy 17356dcadebf) and chain armA35 started side by side,
03:10.

**2026-10-22 ~03:25, prod gates on armA25's final (copy 17356dcadebf of ae5a1fbe3146): both clean,
no fix build.** Error gate 0 rounds; play gate 0 rounds, nothing broken: title → Enter → floor 1
with the full HUD, number keys arm and fire cards (Zap's range painted with "NO TARGET IN RANGE",
Purr self-cast, Pounce leaps the cat), combo badge, E ends the turn (counter, Energy refill, fresh
hand, discard grows, enemies move), Escape pause menu (Resume, Settings, Deck View, Abandon) and
back. Its impressions: "a tight, readable tactics puzzle". The first chain final to pass both gates
with no fix build on the first try besides chain D.

**2026-10-22 03:10–04:00, chain armA35: arm A, 35 turns per stage, final c64de1578709, no retries.**
`done()` at stages 1 (23), 2 (31) and 6 (35); every other stage ran its 35. Stage 2, the one that
broke at 25, passed first try. Final check: boots to title, Enter → play, 3 taps → 2 tiles (2 Move
points), E ends the turn, no page errors. The title screen has debug leftovers armA25's does not: a
palette strip top left, a "HP 30 ENEMY DMG 0 ENEMY HP X1 SCORE X1" line, and a big "F1 DIORAMA T150
EV 5 … TITLE" strip along the bottom; armA25's title is clean (castle, moon, Mittens, menu). Gates on
it next.

**2026-10-22 ~04:15, prod gates on armA35's final (copy 89d68c1b1a7c of c64de1578709): both clean,
no fix build.** Error gate 0 rounds, play gate 0 rounds, nothing broken: title → NEW RUN, arrows
walk and fall off edges, Up climbs, cards give range feedback, E ends the turn (1 → 2 → 3, bonus
line updates, hand reshuffles, a gained FIREBALL), bunnies climb ladders toward the cat. It read the
debug footer as "the stage-11 debug surface"; it never reached the boss or the win/lose screens.

**2026-10-22 04:20, wrap-up and arm A summary (for Nick).**

| chain | turns/stage | stage builds | retries | `done()` | final | prod gates |
| --- | --- | --- | --- | --- | --- | --- |
| armA25 | 25 | 12 | 1 (stage 2, did not boot) | 3 | ae5a1fbe3146 | both clean, 0 rounds |
| armA35 | 35 | 11 | 0 | 3 | c64de1578709 | both clean, 0 rounds |

Against arm B (A 3 retries, C 5, D 1, E 0; gates clean without a fix on C, which only reached the
title and settings, and D): arm A broke less
and both finals passed the gates untouched, on two chains. Arm A spends more turns (275 and 385 vs
225 and 315), since it has 11 stages to B's 9. armA35's title screen carries debug leftovers
(palette strip, a stats line, a big "F1 DIORAMA … TITLE" footer); armA25's is clean. Whether either
plays better than chain C is Nick's call.

Served blind on 127.0.0.1:8931–8934: armA25, armA35, chain C (99316c80aa3f, Nick's 8) and the
one-conversation baseline (8fc1191a0c54, Nick's 2), shuffled; key in
/var/tmp/section-budget/blind_key_armA.txt. Basalt config restored from the backup and the model
unloaded; serve.py and local_gpu auto stopped; plain run.py restarted.

**2026-10-22 19:50–21:40 EDT, arm A with a DeepSeek V4.1 Flash builder (chain dsA25).** Logged
in full in labs/opus-design-deepseek-build. Two findings for this lab: (1) `chain.py` keeps the
last attempt when every retry fails, even one that no longer boots; stage 8's third attempt broke
the boot, and stage 11 dropped a booting second attempt for a broken third. Keep the best attempt.
(2) A builder that plays through the debug API cannot see a dead `requestAnimationFrame` loop;
stage 4 lost it, our check caught it from stage 6, the prod play gate caught it at the end.

## Outcome
