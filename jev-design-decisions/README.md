# jev-design-decisions

Status: done
Control: the LLM design chain as it ships; the 95 real prompts built locally under `~/output/runs`
and the designs (`spec.json` `request`) it wrote for 50 of them.

## Purpose

Design is one LLM pass that makes every call at once, and its calls lean: Flash-Next picks 2D
24/24 when the ask leaves the dimension open (experiments.md, design 2D/3D tilt). JEV-27B-VL
(`/var/lib/models/jev/JEV-27B-VL`, Apache-2.0, a LoRA plus decision head on Qwen3.8-27B) answers
typed choices with calibrated probabilities in one forward pass. If a design's discrete calls
(dimension, art style, camera, ...) go to JEV and the LLM writes the design around them, the
design may come out better than one where the LLM makes those calls itself.

Probe 1 (2026-10-14), dimension: "Should a game described by '{prompt}' be 2d or 3d?" asked of
JEV for every built local game, compared to what the build shipped (three.js
`PerspectiveCamera` in the game's own code = 3d). 87/95 real prompts agree; all 19 that name a
dimension agree; all 8 misses are JEV 3d where we built 2d, on asks that leave it open (fridge
escape, museum heist, open-world collector, amnesia RPG, lap racer, derelict station, rally,
island survival).

## Hypothesis

Draft. The goal is less friction from prompt to start of build, and the question is whether a
JEV-driven design can be good; no game is built in this lab. A design whose discrete calls come
from JEV reads, to Nick, as at least as good as the shipping chain's on the same ask. An idea
failure: JEV's picks are a different lean rather than a better read (e.g. pixel art for every
2d game), or Nick prefers the LLM's calls where they differ.

## Setup

`survey.py` collects built runs, their prompt and built dimension into `rows.json`;
`dim_results.json` adds JEV's dimension answer. `style.py` asks, per prompt, "Given a {dim}
game with the prompt '{prompt}', what art style would you choose?" with dim = JEV's own answer,
over nine styles with one-line descriptions, and classifies each LLM design's written style
over the same nine. JEV served by llama-swap (:5001) + `decide.py` (:8101) on the local 5090.

    ~/Documents/decision-model-test/.venv/bin/python style.py

## Log

2026-10-14, style probe 1. 95 prompts, 50 with an LLM design. JEV's pick matches the design's
style on 23/50. JEV picks: pixel art 40, painterly 12, low-poly 10, neon 10, realistic 7,
voxel 6, flat vector 6, anime 3, minimalist 1. Designs: pixel art 37, neon 15, flat vector 14,
voxel 8, low-poly 7, anime 5, realistic 5, painterly 3, minimalist 2. Median top probability
0.64. 5 of 28 prompts designed more than once got different styles across designs. Read:
JEV leans painterly where the LLM leans flat vector, and reads cozy/story asks (fishing,
noodle shop, village mystery, squirrel) as painterly; agreement alone says nothing about which
is better. Verdict: works as a probe; quality needs a build and Nick's judgment.

2026-10-14, style probe 1 baseline fix. Runs from the team-design era keep only a pointer in
`spec.json` `request`; the design is `game/design/design.md`. `style.py` now reads that (or
`design.md` in the run root). Local JEV serves 32K context, so 4 designs over it are recorded as
skipped, not truncated. Rerun: agree 21/48. Designs: pixel art 36, flat vector 21, neon 12,
voxel 8, low-poly 5, anime 3, realistic 3, painterly 2, minimalist 2. JEV unchanged. Verdict:
implementation fix; the first entry's design numbers are void.

2026-10-14, style probe 2: the nine plus "something not listed: none of the styles above fits
this game" (`style.py --other`). Choosing from a prompt, JEV never takes it: median P 0.003,
max 0.044 (the sentient fridge); 3 picks shift between neighbouring styles. Classifying designs,
it takes it on 4, and every one is a design with no style in it: Ember Duel's ART section lists
sprites and names no style, and the warehouse stealth run has only the bare prompt. Agree 21/48.
Read: "not listed" means "the text states no style", not "this list is wrong for the game";
from a one-line prompt any listed style is plausible, so a per-game list cannot rely on JEV to
reject it, and the list has to come from somewhere upstream. Verdict: works as a probe.

2026-10-14, read of probe 1 on the 69 prompts JEV calls 2d (no new run). Clear picks (top P
≥0.9) on 17: pixel art for dungeon crawlers, platformers, top-down RPG/village/farming;
neon/synthwave for rhythm, bullet-hell, arena shooter, glowing-mushroom snake. Most of the 17
are long "Build this ..." system prompts or name a cue ("Neon Beat", "glowing", "dark
starfield"); few are short user asks. Neon averages P 0.89 when picked, pixel art 0.74,
painterly 0.55, flat vector 0.47, anime 0.39. 3d styles on 2d: one (voxel, tetris-like, 0.42).

2026-10-14, escape-hatch probe (`remove_one.py`). Neon Beat ("A four-lane rhythm game called
Neon Beat..."), JEV 100.0% neon with the nine. Neon removed, "something else: a style not
listed above" added: flat vector 69.4%, minimalist 14.9%, pixel art 10.0%, something else 1.9%.
Read: with its near-certain answer gone, JEV moves to the nearest listed style rather than the
escape option. A missing style cannot be detected from JEV's pick, so the list must contain the
right answer before JEV is asked. Verdict: works as a probe.

2026-10-14, escape-hatch control: "2+2=" over 1/2/3/4 → 4 at 100.0%; over 1/2/3/something
else → something else 80.9%, 2 18.4%, 3 0.5%, 1 0.2%. Read: the escape works when every listed
option is plainly wrong, and still leaks 18% to a wrong answer. Neon Beat's fallback styles are
worse fits, not wrong answers, so JEV took one. Taste calls need a list that holds the answer.

2026-10-14, escape wording: "something not listed" in place of "something else". 2+2 over
1/2/3/something not listed → 79.4% (2: 20.2%). Neon Beat, neon removed, "something not listed:
none of the styles above fits this game" → 0.6% (flat vector 67.5%, minimalist 19.0%, pixel
art 9.6%). Read: the wording changes nothing; same result as "something else".

2026-10-14, question wording: "which art style is the correct one?" in place of "what art style
would you choose?", Neon Beat. Nine: neon 100.0%. Neon removed + "something else": 3.0% (flat
vector 69.4%, minimalist 19.6%). + "something not listed": 1.5% (flat vector 67.6%, minimalist
22.2%). Read: framing it as a right answer does not move the escape; within noise of before.

2026-10-14, sufficiency probe (`sufficiency.py`). JEV served at 131072 context, KV pool ~80K
tokens (mem fraction 0.91; 0.94 OOMs in warmup). "Is this design sufficient?" (noul), state =
the whole design, on the 18 local finished designs: P(yes) 0.618-0.795, no separation.
Controls on the cozy fishing design: empty 0.067, bare prompt 0.356, first 5% 0.489, full 0.787.
Read: the question tracks how much design there is, not whether it is good; every real design
lands in the same band. Verdict: works as a probe; as asked it does not judge quality.

2026-10-14, three more yes/no questions (`sufficiency.py "<question>"`), same 18 designs + controls.
| question | designs P(yes) | empty / prompt / 5% / full |
| ready to be built? | 0.78-0.93 | 0.02 / 0.33 / 0.60 / 0.92 |
| enough information for all the visuals? | 0.61-0.88 | 0.04 / 0.17 / 0.38 / 0.79 |
| everything needed for all the mechanics? | 0.62-0.89 | 0.09 / 0.25 / 0.50 / 0.86 |
The four questions (with "sufficient?") rank the designs alike, Spearman 0.63-0.89, and not by
length (-0.24 to +0.12). Snake and cozy fishing sit on top everywhere; one derelict-station
design, the amnesia RPG and the learning tower defense at the bottom. Two byte-identical
derelict designs scored identically on all four. Read: the questions share one signal that is
neither length nor the question asked, possibly game complexity; without a human rating of
the designs there is no way to tell whether it tracks quality. Verdict: inconclusive.

2026-10-14, full-design run 1, frame section (`frame.py`, `frame_result.json`). Prompt: "A
roguelike with one button. What you do is decided by how fast you press it." Each answer is
carried into the next question's state. 2d 0.90, top-down 0.69, single player 0.97, real-time
0.81, free movement 0.36 (on rails 0.32), endless 0.51, permadeath 0.95, tense 0.76, one screen
a few minutes 0.72; ends by surviving as long as possible 0.88 (all others under 0.6).

2026-10-14, full-design run 1, gameplay mechanics (`gameplay.py`, `prompts/mechanics.txt`,
`gameplay_result.json`). Generation moved to ninfer `qwen3.8-27b-quasar` (sglang JEV decodes
~40 tok/s; first try spent 7 min). "List every mechanic... cast wide" made the model draft ~222
mechanics in its reasoning and hit 16K tokens with no answer; bounded to 25-40 it answered in
72 s (10.8K reasoning tokens), 30 mechanics. JEV triage with the full list in state: core 9,
nice-to-have 21, cut 0. Core loop: "Tempo signal input" 0.92. Read: core reads right (tempo
input, steering, waves, permadeath, tempo-banded attack/dash/dodge); JEV never cuts, the same
"no escape from a plausible list" pattern; nice-to-have below ~0.6 are the effective cut line.

2026-10-14, full-design run 1, systems level 1 (`systems.md`, `systems.py`,
`systems_result.json`). Yes/no "Does this game contain {system}?" over 24 system names, bare
names, frame decisions as state. Kept (>0.6): survival 0.96, hazards 0.93, score and records
0.77, creatures 0.76, waves and spawning 0.70, combat 0.69. Next: characters and NPCs 0.57,
exploration 0.35, progression 0.29; everything else under 0.21. Read: the cut side looks right
(farming, cards, racing, sports, dialogue all under 0.1). Survival likely matched "survive as
long as possible" in the frame, not hunger/thirst; creatures likely read as enemies, not
collecting. Progression at 0.29 is low for a roguelike. Names alone are ambiguous.

2026-10-14, full-design run 1, systems level 2 (`systems2.py`, `systems2_result.json`). Yes/no
"Does this game's {system} include {part}?" for the parts of the six kept systems; kept
systems added to the state. Survival: every part under 0.22 (hunger 0.22). Creatures: every
part under 0.34 (evolution 0.34). Combat: enemies 0.97, player health 0.92; weapons 0.55,
abilities 0.51, bosses 0.39, allies 0.09. Hazards: traps 0.66, environmental damage 0.62.
Score: high scores 0.93, score 0.92, combos 0.66, leaderboard 0.61. Waves: difficulty ramp
0.88, waves 0.82, spawn points 0.71. Read: level 2 empties the two word-match systems on its
own, so a level-1 false positive costs a few questions and drops out. A level-1 false negative
(progression 0.29) is never asked again.

2026-10-14, systems level 1, LLM comparison (`systems_llm.py`, `prompts/systems_llm.txt`,
`systems_llm_result.json`). Same state and 24 systems, one prompt to ninfer
`qwen3.8-27b-quasar`, thinking on, true/false per system. 11 s, 1,638 completion tokens (swap
not counted). Agrees with JEV on 24/24, including survival and creatures. Its reasoning shows
the same readings: survival from "survive as long as possible", creatures as enemies;
progression considered and rejected for a few-minute endless game. Timing for JEV: ~70 ms per
yes/no on the ~150-token state (30 questions in 2.1 s), warm-up 17 s.

2026-10-14, full-design run 1, look and sound (`look_sound.md`, `look_sound.py`,
`look_sound_result.json`). Options carry one-line descriptions; frame, kept systems and their
parts in state; each answer chained. Art pixel art 0.36 (minimalist geometric 0.355, neon
0.21), palette dark 0.83, pixel font 1.00, chiptune 0.56 (synth loop 0.41), retro bleeps 1.00.
Screens: title, game over, high scores (pause 0.51, settings 0.50, win 0.10). HUD: health,
score, timer, combo counter, wave number (minimap, ammo, currency ~0.11). Effects: screen
shake, particles, hit flash, trails (slow-mo 0.56, bloom 0.31). Accessibility: colour-blind
palette, reduced motion (remappable keys 0.59). Read: coherent for an endless arcade roguelike;
art style is a near tie.

2026-10-14, full-design run 1, write-up (`write.py`, `prompts/write.txt`, `write_raw.json`,
`design.md`). Writer prompt = integrator's section list with a new intro: the JEV decisions are
final, the LLM writes content, rules, input, structure, look within the style, contracts. One
ninfer `qwen3.8-27b-quasar` call, thinking on: 317 s, 49.4K completion tokens (29.9K
reasoning), finish stop, 61K-char design with every section 0-11 and A. Stays inside the
decisions: no pickups, no healing, no upgrades, pixel/dark/chiptune carried through. Input
became press interval bands (<150 ms frenzy, 150-350 dash, 350-750 strike, >=750 step).
Survival and creatures show up as section names (the state still listed all six level-1
systems; only the parts line dropped the empty ones), but their content is health/failure and
the enemy roster. Read: the JEV-decided chain reaches a complete design. Quality not judged.

2026-10-14, control: current design chain on the same prompt (`prod_design.py`,
`prod_design/`). The four prompts from `src/maestro/codegen/design.py` with its messages,
reasoning `xhigh`, temperature 0.7, 100K cap, posted straight to llama-swap (no job queue).
gameplay 418 s / 60.4K tokens, visual 234 s / 36.9K, engineering 447 s / 64.0K, integrate
344 s / 46.4K: 1,442 s and 207.7K completion tokens, 85K-char spec, all sections, one
integrate call. The JEV chain: ~5 s of decisions + 317 s / 49.4K tokens, 61K chars. Different
games: the chain wrote a side-view roguelike, 5 floors of generated rooms, 5 bosses, 10 relics,
a shard economy and meta upgrades, input as a decaying tempo meter (move / attack / parry /
flick). JEV's frame (one screen, a few minutes, endless, no progression system) produced a
one-screen endless arena with no bosses, relics or upgrades: closer to an arcade survival game
than a roguelike. Read: JEV's frame decisions set the scope; the size and session-shape answers
pulled it small.

2026-10-14, my read of both designs (Claude, one reader, not Nick). Neither is broken; both
are fully specified with numbers a builder can implement. JEV design: tighter and smaller
Tier 1 (step + strike + one enemy), internally consistent; but not much of a roguelike (no
items, rooms or meta, variety only from spawns), and it aims with the pointer: the whole
playfield is the button and the press location steers. That follows from JEV's top-down + free
movement (0.36 vs on rails 0.32): one button cannot steer in 2D without a pointer. Current
chain: answers the prompt better (pure one button, single lane solves direction, rooms,
relics, bosses, meta) but Tier 1 is heavy (relics, shards, upgrades, save, boss), the tempo
meter cannot hold Attack (+30/tap against 30/s decay only balances at exactly 1 tap/s, so the
"1.5-2.5 taps/s" attack rate in its own feel table climbs into Parry within ~3 taps), and room
4 vs room 5 as the boss room is ambiguous. Verdict: not way worse at the craft level; worse at
fitting the prompt, and both misses trace to frame decisions (size, session, camera/movement,
progression left out).

2026-10-14, full-design run 2: "make me a game about solving mazes" (`runs/maze/`). Scripts now
take a run directory; run 1 moved to `runs/one-button/`. Systems with no kept parts are now
dropped from the state before look and sound. Frame: 2d 0.88, top-down 0.98, real-time 0.47,
free movement 0.51 (grid 0.48), sequence of levels 0.94, restart the level 0.78, cozy 0.46
(tense 0.44), a handful of levels 0.81, reach the exit 0.96. Level 1: progression 0.87,
exploration 0.82, puzzles 0.75, the rest <= 0.26 (combat 0.006). Level 2: exploration ->
landmarks, secrets, keys and locked doors; puzzles -> puzzle types, switches and doors, hints;
progression -> nothing over 0.6, so it dropped out. Look: painterly 0.41, pastel, hand-lettered,
acoustic, minimal SFX; no HUD, no effects. JEV write-up: 358 s, 52.7K tokens, 47K chars, all
sections: six hand-drawn ASCII garden mazes with keys, switch doors, cosmetic secrets, hint
arrow. Level 1 is a straight corridor to the exit; levels 4-6 are three rooms joined by doors,
not mazes; the level 5 and 6 maps have one row a character too wide.

Control on the same prompt: gameplay 167 s, visual 259 s, engineering 622 s with an EMPTY reply
(91K tokens, all reasoning, finish stop), integrate started without it. `prod_design.py` had
no retry where `design._call` retries once; stopped it, added the retry and resume, reran:
engineering 527 s, integrate 276 s. 1,851 s of compute with the failed call, 1,229 s without,
vs JEV ~6.5 min. Control design: 12 seeded generated mazes with validation, BFS and a fallback
builder, limited visibility and a fading 10 s trail, orbs, time stars, no fail state.

2026-10-14, builds (`build.sh`, `build_all.sh`, `builds.tsv`): new run with the ask, the design as
spec, the real request line, the real build chain at its default cap, local quasar, art left
queued. maze-jev 75dd2004bb39: ok, 67 steps, 975 s; the builder BFS-checked the six maps and
fixed three transcription errors. Nick played it: "pretty bad". maze-chain 1dc92b675b70: hit the
200-step cap (ok False) at 2,342 s, its last turns reporting 35/35 tests and 63/63 DoD items;
5 compactions. One-button builds paused at Nick's ask until the maze pair is compared.

2026-10-14, Nick's verdict on the maze pair: maze-chain has "actual mazes, but unplayable because
it is impossible to read"; Petal Path "pretty bad". "Overall, I think the current pipeline
probably produces a better game." The JEV pipeline is worth improving; how is open.

2026-10-15, Nick corrects the maze verdict after playing both: Petal Path worked, all 6 levels
playable, only "next level" was broken; the weak part was the mazes themselves, not keys and
doors. "I think jevs game was very alright." maze-chain was the larger failure: the tiles were
unreadable (not the fog) and he could not work out how to move, though its idea would likely
have been the more interesting game. Next: run 3, JEV on "a game where you play as a cat trying
to catch mice".

2026-10-15, run 3 "a game where you play as a cat trying to catch mice" (`runs/cat/`), JEV steps
only: 2d 0.73, top-down 0.63 (side-on 0.36), free movement 0.98, sequence of levels 0.39,
restart 0.49 vs lose a life 0.48, silly 0.77, reach the exit 0.60 (beat a score 0.515). Level 1
kept creatures 0.96, progression 0.85, characters 0.80; level 2 dropped every part (creatures'
parts are pet-sim: pets 0.46), so the state had no systems. The tree has no home for chase and
catch. Throughput: 67 ms per yes/no serial, 33 ms at 8-32 concurrent (2000 systems ~1 min).

Level-1 phrasing probes on cat, maze, one-button. (a) "Does this game contain {system}, which
includes any of: {parts}?" killed the word matches (one-button survival 0.96 -> 0.29, creatures
0.76 -> 0.16) but dragged everything down: maze lost exploration 0.48 and puzzles 0.39, cat kept
only progression. (b) Nick's unlabelled form, "Do any of these mechanics make sense for this game:
{parts}?", then "Does this mechanic make sense for this game: {part}?" per part of kept groups:
cat -> stealth (hiding spots, noise), exploration (map, secrets, collectibles), waves (spawn
points, difficulty ramp), puzzles kept but no parts; score 0.594 and hazards 0.576 just under.
Maze -> exploration (map, secrets, collectibles, keys and doors, landmarks), puzzles (hints,
switches and doors), waves (spawn points, difficulty ramp). One-button -> score, waves, combat
(enemies, player health), hazards (traps); survival and creatures gone.

2026-10-15, grouping probe (`runs/grouping_probe.json`): all 109 distinct level-2 parts, asked
three ways with the unlabelled questions. Flat: every part on its own, kept over 0.6 (cat 15,
maze 15, one-button 13). Gated: a group question first, then only parts of kept groups. Recall of
the flat set: logical groups 33% / 60% / 62% (cat / maze / one-button); random groups of 4-16,
three shuffles each, 0-54% per shuffle, mean 9-51%, no size reliably better, swings of 0% to 47%
on the same size between shuffles. A group question is not "any of": a mixed group reads as no
even when one part fits, so gating mostly loses parts. Flat cat keeps: difficulty ramp, rooms /
structures, collectibles, hiding spots, traps, spawn points, map / world, objectives, boosts,
score, secrets, abilities / special moves, rules, rewards, noise. Generic parts pass everywhere
(rules, objectives, rewards; needs and collectible creatures on maze; choices, opponents on
one-button).

2026-10-15, neighbour probe (`runs/neighbor_probe.json`). A: the per-part question with a
three-part context list in front ("chosen from a list that includes: ...") vs alone, 7 parts x 5
contexts x 3 runs. Neighbours move a part by up to ~0.25 and often across 0.6, but not in a
consistent meaning direction: cat abilities rose with combat neighbours (0.65 -> 0.74), cat enemies
rose with farming (0.54 -> 0.73), cat keys fell with stealth (0.51 -> 0.26), score fell with
stealth or farming on cat and one-button. B: 180 groups per run (24 logical + random 4/8/12 x 3
shuffles): group score correlates 0.79-0.82 with the mean of its parts' solo scores and 0.77-0.79
with the best part's. Of groups holding at least one part JEV says yes to alone, the group got yes
21/99 (cat), 14/96 (maze), 33/89 (one-button). The group question reads as "does this set fit on
average", not "any of"; that is most of what the gate loses.

2026-10-15, flat coverage, 5 random real asks (`flat.py`, `runs/cov_sample.tsv`, `runs/cov/`): frame
then all 109 parts yes/no, 63 s for all five. One sample is a run label, not an ask ("island —
skeleton v2 design"). F1 racing: core covered (laps, tracks, vehicles, opponents, leaderboard,
medals), tyre and fuel landed on consumables 0.72 and temperature 0.72, "placement" 0.89 likely
read as race position. Card battler: fully covered (hand, cards, draw / discard, player health,
field). Sentient fridge escaping a house: rooms, switches and doors, hiding spots, detection,
physics objects; no part for how the fridge moves, as the list does not do movement. Space
salvage: crafting and economy covered, but the core verb, towing wrecks, has no part (physics
objects 0.71 nearest). Keeps run 18-32 parts, and generic parts pass on all of them (rules,
objectives, difficulty ramp; needs on two).

2026-10-15, flat list v2 (`mechanics.md`): every part now carries a one-line description, plus 48
verbs with descriptions; 157 mechanics, asked one by one (`flat.py`). Cat now keeps chase and catch
0.89, F1 steer 0.98, salvage carry and tow 0.96, fridge push and pull / sneak / flee. "Rules" no
longer passes everywhere. Coverage (`coverage.py`, `runs/cov/`): 113 of 116 distinct built prompts
under 4,000 chars (3 crashed JEV; see below; ~25 of the 113 are run labels, not asks). The core
verb lands on nearly every real ask: platformers jump, shooters shoot / aim, rhythm hit on the beat,
tower defense place / defend a point, Tetris place / swap and rotate, solitaire pick up / sort,
mysteries guess and deduce, fishing fish, noodle shop cook, incremental wait and collect / tap,
fish-eats-fish chase and catch, minecraft dig / place. Misses: catch falling apples in a basket (no
verb; chase and catch is pursuit), card battlers keep no verb (the card nouns carry them). Broad
verbs pass widely: dash 62/113, flee 50, dodge 48, jump 47, memorize 41, push and pull 37, throw
34. Keeps per prompt: median 22, max 97. Never kept: bet and bluff, roll dice, spell words, type
(no such asks in the set).

JEV serving: any prompt over ~3,000 chars CUDA-OOMs sglang (0.91 mem fraction, ~0.15 GB headroom)
and kills the server; and decide calls bypass llama-swap, so its 300 s ttl unloads JEV mid-run
unless something pings it through llama-swap.

2026-10-15 overnight (`overnight.sh`, `stack.py`): three asks through both pipelines, then six
builds on local quasar, art left queued. JEV side: frame + flat mechanics + look and sound + write.
The write cap was 64K and cut the first cat write at 7 sections (finish length); raised to 100K to
match the chain, rewritten: cat 65K chars, salvage 62K, fridge 80K, all sections, 331-392 s each.
Chain: cat 1,071 s, salvage 1,872 s (engineering empty twice at the 100K cap, so integrate ran on
gameplay and visual only, as prod does), fridge 1,109 s; all sections.

| Build | Run | Result | Steps | Time |
|---|---|---|---|---|
| cat-jev "Whisker Panic" | fcf8552fba2a | ok | 171 | 1,779 s |
| cat-chain "Cat & Mice Hunt" | 0ba62d405f5f | cap | 200 | 1,770 s |
| salvage-jev "Cold Current" | b3a569feb805 | cap | 200 | 2,360 s |
| salvage-chain "Deep Salvage" | b402ddfd4343 | ok | 127 | 1,565 s |
| fridge-jev "Fridge Escape" | 4711fba111df | cap | 200 | 1,627 s |
| fridge-chain "Defrosted" | c0a49155e79d | cap | 200 | 1,765 s |

All six boot headless with no console errors. Not yet played.

2026-10-15, design-stage cost. JEV decisions (frame, mechanics, look and sound) were not timed
directly; file mtimes put frame + mechanics for salvage and fridge in the same second and look and
sound for all three within 7 s, so seconds per game. JEV load and swap time was not measured.

| Game | JEV write | Chain gameplay / visual / engineering / integrate | Chain total |
|---|---|---|---|
| cat | 331 s, 55K tok | 176 / 208 / 339 / 349 s | 1,071 s, 179K tok |
| salvage | 341 s, 56K tok | 223 / 202 / 577 + 602 (both empty) / 267 s | 1,872 s, 319K tok |
| fridge | 334 s, 56K tok | 214 / 233 / 314 / 348 s | 1,109 s, 185K tok |

Design + build: JEV 2,114 / 2,705 / 1,965 s, chain 2,841 / 3,437 / 2,874 s; 6,784 s vs 9,152 s
total, ~26% less. Build time does not differ (four of six hit the 200-step cap): both arms feed the
builder a design of the same kind, so the saving is the design stage only, ~3x fewer tokens.

2026-10-15, design read, first pass by Claude (scope, decisions and core gameplay of all six; not
played). Chain designs better on all three, by a wide margin. Each chain design is built around
one idea from the ask: cat = mice leave holes and run back to escape, the cat blocks holes, escapes
cost lives; salvage = spring-damper tow with stress and line snap, upgrades make heavier wrecks
towable, 15-25 min; fridge = unplug to move, power drains, recharge only while plugged and still,
slow waddle and turn through doorways, loud slide, movers arrive at 120 s. JEV designs are a
generic adventure with a new skin: cat = 7 scrolling levels of catch N then exit, plus shape keys,
switches, levers, secrets, medals, ranks; salvage = 12 sectors over 2.5-3.5 h, crafting, trading,
quests, skill tree, cutscenes, and the tow is a fixed follow 96 px behind the ship; fridge =
first-person stealth with keys and pressure plates, and the fridge moves like a person.

Read causes: (1) the writer treats the kept list as a checklist; the JEV "Why" column is mostly
"Given final decision" / "Uses listed X", and 26-44 kept mechanics fill the design; (2) the generic
parts (keys, switches, secrets, hints, medals, unlocks) pass everywhere and are what makes the
three alike; (3) frame calls push scope the wrong way (salvage open world + a few hours; fridge 3D
first-person + sequence of levels), where the chain chose one screen or one short run on its own;
(4) the writer's thinking leaks into the fridge design ("pushed by a fan boost? No, ...").
For JEV: its designs are simpler to build (cat-jev finished; maze-jev worked), consistent with
Nick's maze verdict that JEV's game worked and the chain's was more interesting.

Options raised, not decided: (a) the writer treats kept mechanics as a menu: choose the core loop
first, then use only what serves it; (b) JEV ranks how central each kept mechanic is and only the
top few are required; (c) fix the generic parts first; (d) hybrid, JEV for frame and art and sound,
chain gameplay draft for the game.

2026-10-15, Nick played the six. Cat: JEV 5, chain 2. Both are valid readings of the ask; JEV has
more mechanics and would be solid with better graphics and working doors (the Roomba does not act
as expected, the red-rectangle-with-X traps are unreadable, the layouts are a bit odd). Chain is
three circles on a big square, mice run randomly and you run into them; unforgiving, and blocking a
hole does nothing because the mice go to another hole. Salvage: both 4, both glaringly broken with
big camera faults (JEV: only the top-left corner of the screen behaves, the rest drags everything
around); JEV has more mechanics and several do not work, likely from the step cap; both look a
little refinement away from fine games. Fridge: chain 5, works but is not very good or
interesting; Nick is far more interested in the JEV 3D version but its camera only turned left and
right, inverted. My first-pass design read had cat backwards: the chain's one idea built as three
circles on a square, while JEV's extra mechanics made the better game.

Hand fix to fridge-jev to judge it with a working camera (`~/output/runs/4711fba111df/game`,
original in `game.orig`): mouse-x yaw sign flipped in `player.js`, pitch added (clamped to ±1.2
rad) and applied to the camera in `main.js`. Checked headless: mouse right turns right, mouse up
looks up, no console errors.

2026-10-15, fridge screenshots (`labs/scratch/`). Nick: fridge-jev is almost certainly the best of
the six once its faults are fixed. The main weakness across all six is lack of depth; JEV's extra
mechanics, right ones or not, are what give depth, and the problem is that many of them do not
work. Screenshot read (Claude): the JEV frame reads as a place to explore: a lit hallway to a
doorway with a goal arrow, pickups and a plate on the floor, lit rooms. The chain frame reads as a
floor plan: three empty rooms, boxes, two resident circles, outlet rings. JEV faults visible: a
large green block (likely the fridge's view model) covers about a quarter of the view, every
object is a bare box (no art pass ran), and the pink pickups are unreadable. Across all three
pairs the JEV faults Nick hit were build faults (camera, doors, mechanics not working, 200-step
cap), not design faults, so the next lever is making the extra mechanics work rather than cutting
them.

Nick's stance: last night he expected JEV had not worked out; the morning results moved him to
"this is a good approach, push it more". Not fully sold: the generator here is the local 27B, not
prod's Flash-Next. Next design work: how JEV joins the queue; Nick leans to one call carrying all
the questions, for the least added latency.

2026-10-15, JEV-9B vs JEV-27B on the same decisions. JEV-9B (autotrust, Apache-2.0, Qwen3.5-9B base,
18 GB bf16) at /var/lib/models/jev/JEV-9B, served by sglang + the decide.py readout (`jev9b/`:
prep.py splits the adapter as for the 27B; sglang's text-only Qwen3_5ForCausalLM lacks the LoRA
hidden-dim lookup, patched through `jev9b/patch/sitecustomize.py`). Same frame.py, flat.py and
look_sound.py on the three overnight asks (`jev9b/compare.sh`, `runs9b/`), compared with the 27B
results in `runs/`, which were made on the same code. Time per game ~6-9 s on the 9B (frame 1.5-4.7,
mechanics 2.7, look and sound 2.1).

| | cat | salvage | fridge |
|---|---|---|---|
| frame calls the same | 5/10 | 6/10 | 8/10 |
| mechanics kept 27B / 9B / both | 26 / 16 / 11 | 44 / 27 / 21 | 29 / 25 / 19 |
| mechanic probability correlation | 0.80 | 0.80 | 0.86 |
| look and sound the same | 4/9 | 2/9 | 1/10 |

Frame splits are mostly near-ties in one model or the other (cat players 0.495 vs 0.484 on the 9B;
cat failure 0.488 vs 0.479 on the 27B; session shape tops at 0.29-0.39 in both), and they cascade:
session shape and size move together and then the mechanics and look follow. The 9B leans small:
single screen for cat and salvage, a few minutes or under 30 minutes, fewer mechanics kept (it drops
the keys / switches / secrets / hints / medals generics the 27B keeps). Some 9B calls read wrong for
the ask: fridge tone eerie (0.51) with realistic art and ambient music for a sentient-fridge escape,
cat "single player against an AI opponent". Some read plausible: cat keeps sneak, hiding spots and
detection (stalking mice). Nick's play verdicts favoured the 27B's extra mechanics, so the 9B's
smaller keeps may cost depth; unbuilt, not judged.

2026-10-15, players question removed from frame.py (Nick). "Single player against an AI opponent"
is multiplayer with a bot, and a chase game like cat already is single player against AI; the
answer changes nothing the writer does (a card duel gets its opponent from the ask either way), and
local two-player only ever passed on run labels reading "p2" (pass 2). Runs before this line carry
a players line in their state; later runs do not.

2026-10-15, Decision 3.0 (vLLM Semantic Router, Apache-2.0) d3-mini (4B, Qwen3.5-4B, 9.1 GB) and d3-flash (9B,
Qwen3.5-9B, 16.8 GB) on the same three asks, through `d3/shim.py` (JEV's /v1/decide over the model's system_one,
one question per call) and `d3/compare.sh` into `runs-d3-mini/`, `runs-d3-flash/`. Venv /var/lib/models/d3/venv
(transformers 5.17, torch 2.13 cu130). 5-7 s per game.

Frame: both d3 models lean large where the 27B does not: "many levels, a few hours" on all three asks, open world
for cat and fridge, cat as 3D third-person, fridge third-person with "no failure". Look and sound are close to the
27B on cat and fridge (silly, stylized, hand-lettered; cartoony effects rather than retro bleeps). Mechanics kept
(27B / mini / flash): cat 26 / 42 / 46, salvage 44 / 36 / 33, fridge 29 / 35 / 35; correlation with the 27B
0.73-0.87; mini keeps hunger, skill tree and day / night for the cat. d3-mini and d3-flash mostly agree with each
other. Read: neither is a drop-in for the 27B on the frame; scope calls are the weak part.

2026-10-16, two mainstream asks for a prompt-to-game demo: frog "a platformer where you play as a frog", shooter
"a space shooter where you fight waves of aliens". Frames: frog 2d side-on, levels, restart the level, silly,
handful of levels, reach the exit; shooter 2d top-down, levels, lose a life, tense, handful, defeat a final boss.
Flat mechanics kept 36 (frog) and 34 (shooter), shooter including leaderboard, cutscenes, plot, evolution.

Tuning, decided while Nick was AFK. `centrality.py` asks JEV three centrality questions on the kept mechanics;
"Must the first playable version of this game have this mechanic" separates cleanly (shooter: 13 at >= 0.6, the
four oddities <= 0.11; frog: jump, objectives, falling, map / world, bounce). `tiers.py` bands the kept mechanics
on it (core >= 0.6, supporting >= 0.3, extra below) and replaces the state's mechanics line with the three bands;
`prompts/write_tiered.txt` makes tier 1 exactly the core, tier 2 supporting, tier 3+ extra, every mechanic a
concrete on-screen thing with a named input. Nothing is cut: depth stays, order changes.

Frog v1 (`runs/frog/design_v1.md`, 330 s, 63K chars): tiers as intended, concrete numbers (coyote 0.09 s, jump
buffer 0.10 s, 7-level roster), but art, music, SFX and effects landed in tier 5, which a 200-step build never
reaches. Added to the tiered prompt: tiers band mechanics, not polish; tier 1 already looks and sounds like the
game. Shooter v1 write was stopped mid-run for the same reason; both rewritten.

2026-10-16, results. Designs from `prompts/write_tiered.txt` with the polish rule: frog 391 s / 69K chars, shooter
405 s / 78K chars; both put art, sound and effects in tier 1's definition of done, both tier the mechanics as banded.
Builds on local quasar (`demo/build_two.sh`), worker with the long-poll fix (pickup median 0.022 s):

| Game | Run | Build | After | Total, prompt to playable |
|---|---|---|---|---|
| frog "Brib the Gummy Frog" | 68e135291424 | 200 steps (cap), 1,793 s | fix pass 75 s on a player-style report: canvas double-scaled, the view cropped to its top-left so the frog stood below the screen | 37:58 |
| shooter "Neon Swarm" | ac747c82b0b9 | done at 139 steps, 1,056 s | play gate found a dead documented input (title screen never shown), auto fix 50 steps; gate + fix 451 s | 32:11 |

Totals are JEV decisions (19 s per game warm, `runs/_t_*`) + write + build + fix. Not counted: JEV load 28 s, model
swaps between JEV, the writer and the build engine, and the stack boot. The rerun decisions differ near the band
thresholds (frog: unlocks supporting -> extra, the game over screen dropped), so JEV is not bit-for-bit repeatable
at these margins.

Shooter is the better demo: neon title with the controls, sector intro text (the cutscenes mechanic working), waves,
score and combo, hit flash, no page errors. Frog after its fix: title, level 1 clearable (score 750, bronze medal),
level 2 with water, traps and a scrolling camera; flat pixel art, small sprites. Gameplay in both videos is driven
by script (`demo/shooter_plan.json`, `demo/frog_bot.js`, which reads the level tiles and uses the air bounce), not a
person. Videos: `demo/{frog,shooter}.{mp4,gif}`, copied to `~/Videos/gamesummoner/jev-*.{mp4,gif}`. Not yet watched or
played by Nick.

2026-10-16, frog on the current design chain, same ask, same local quasar, same build path (`prod_design.py`, the
chain pinned in `chain/` as it shipped before the JEV stage replaced it; `demo/frog_chain.sh`). Design: gameplay
256 s, visual 255 s, engineering 519 s, integrate 462 s; 1,237 s wall as prod runs it (visual and engineering in
parallel), 1,492 s of compute, 228.8K completion tokens, 115K chars, all sections. JEV design on the same ask: 19 s
decisions + 391 s write = 410 s, 60.5K tokens, 70K chars, so 3.0x faster by wall and 3.8x fewer tokens. Build
40184d98560d hit the 200-step cap at 2,001 s; the frog was never drawn (camera ahead of it), the same class of
defect the JEV frog had. Fix pass on a player-style report: 705 s, hit the fix cap, frog drawn after. Total 65:43
against JEV's 37:58. The game: "Frog: Pond to Peak", six levels to a heron boss by the spec; level 1 clears under a
bot (`demo/chain_bot.js`), level 2's lily pads beat the bot. Video `demo/frog_chain.mp4`, copied to
`~/Videos/gamesummoner/chain-frog.mp4`. One run each, not judged by Nick. My own run crash (I removed the chain
prompts from src/ while this was running) cost ~7 min, not counted.

2026-10-16, demo capture: Playwright's recorder writes VP8 at 0.2-0.9 Mbps, which blocked the dark UI gradients.
`demo/capture.py` records CDP screencast PNG frames with their timestamps and encodes at 30 fps, crf 10; the clock
card shortened to 2.0 s count + 1.8 s hold, "on one local GPU" removed.

2026-10-16, JEV design stage in src/ end to end (uncommitted): `design.py` sends one `decide` job with the whole
chain (`prompts/design/decisions.json` + `mechanics.md`), bands on the first-playable probabilities, one write call
(`prompts/design/write.txt`). Decide box from gamesummoner-images (`local/decide`, SGLang + JEV readout, max running
requests 1 after the peer found batched reads shift probabilities up to 0.05). Frog ask through the web API, served
by `scripts/local_gpu.py auto`: game a896dc2202bd. Decide job: pending -> done at 83 s (box cold boot 51 s), 16.1 s
of exec; write done at 337 s (239 s exec, 53.6K chars); build hit the 200-step cap, last job at 2,230 s (37:10 from
the click, cold boot and auto's model swaps included). Frame and look decisions match the lab run; the bands moved
(core jump, falling, objectives, map / world; bounce to supporting; a larger supporting band) because the
first-playable question now sees the mechanics line, plus the engine config change. The game "Bip the Frog" boots to
a pixel-font title, level select (6 levels), plays, and a blind run falls into the pond to a game over screen.
`local_gpu auto` released the llm card whenever a play step left the queue empty past 6 s and reloaded it 7 s later,
several times a build: a local cost only.

## Outcome

Closed 2026-10-18 without a write-up here: stale. Any result it reached is in docs/experiments.md.
