# stage-planner

Status: single-run
Control: labs/section-budget arm B chains on the Opus wizard-cat spec (hand-written stages, Nick's
blind scores: chain C 8, E 7, D 6, A 4; the one-conversation build of the same spec 2). For the
battery: the open-shim battery's seeded-head one-conversation builds of the same four Flash-Next
designs on the same local Basalt Flash-Next (34bfd0509e59 hiragana, 61376284936b frog
platformer, 7143e3953cfe frogs eating bugs, 4d1ac4cae527 wizard cat), three of four capped at 200.

## Purpose

Nick (2026-10-23): "we're moving to staged." Every staged chain in labs/section-budget beat the
one-conversation build of the same design (8/7/6/4 against 2), but the stages were cut by hand,
for one spec, written by Opus. Prod needs the cut made by the machine, for whatever design the
prod design chain writes. That is section-budget's Part 2 ("figure out how to make those
decomps").

The design's own `# 10. BUILD ORDER` is not that cut. Opus wrote 11 tier-1 steps naming their
sections; prod Flash-Next designs write 18–23 one-line steps over every tier ("Implement input
system and remappable bindings.") with no sections and no done line.

## Hypothesis

One more model call before the build, a stage planner (`prompts/plan.txt`), turns any design into
9 playable stages in arm B's shape: each stage starts and ends on a game that runs, world first,
then the player, then the core loop one system at a time, screens and audio last. Each stage names
its design headings for the pre-read and a done line. The planner states the cut rules arm B was
cut by, nothing about any one game.

Everything after the plan is arm B as chain C ran it: a fresh build per stage on the same files,
25 turns, turns-left lines, the stage's sections plus §2/§8/§9 and the game's files pre-read (100 KB
cap), our check after each stage, retries from the snapshot before it. Two implementation changes
from section-budget, both from the dsA25 findings:
- the chain keeps the best attempt (boots, then fewest page errors, then latest), not the last;
- the broken rule is generic (does not boot or throws on the page), since the Mittens and E-key
  checks only fit the wizard-cat spec.
One harness fix: the section pre-read is packed into programs under the runner's 20,000-char
stdout cap (`planned.py`), since a Flash-Next design's §2 alone is 8–11 KB and stage sections stack
on it.

Measured per game:
- the plan: stage count, reads that match a heading;
- per stage: boots, page errors, turns, `done()`, retries;
- the chain: total turns and minutes;
- prod gates on the final: rounds, fix builds, broken inputs left;
- Nick's blind play against the one-conversation control of the same design, later.

Single run first: the Opus spec (d086d499669b), the one design with hand-cut chains to compare the
machine cut against. Then the battery: the four Flash-Next designs.

Expected: the planned chain on the Opus spec lands with the hand-cut chains (6–8). On the
Flash-Next designs, finals boot and pass the gates more often than the one-conversation controls
reach `done()`, and play better by Nick's blind scores.

Idea failure:
- plans that don't make playable stages (a stage 1 with no screen, stages that each need the next
  to run), or chains that break and stay broken through retries;
- or, by Nick's play, staged games no better than the one-conversation controls of the same
  designs.

## Setup

Local Flash-Next IQ3_S on Basalt through llama-swap (:5001), `scripts/local_gpu.py auto`, this
lab's `serve.py` in place of run.py. Basalt `conversation-cache-mib` 1536 and
`resident-budget-gib` 36 as for the section-budget chains (backup
/var/tmp/stage-planner/basalt-iq3s.json.bak, restored at the end).

From the repo root:

    venv/bin/python labs/stage-planner/serve.py          # in place of run.py
    venv/bin/python scripts/local_gpu.py auto
    venv/bin/python labs/stage-planner/chain.py <source run> <label>

`chain.py` plans (`plan.py`, writes `plans/<label>/`), runs the stages with `run_stage.sh`
(section-budget's, plus `planned.py`), records each stage in `chains.jsonl`, and runs the prod
gates on a copy of the final (section-budget's `gates.py`). Stage logs are in `logs/<label>/`.

## Log

**2026-10-23 04:45–05:25 EDT, single run sp-opus: works.** Source d086d499669b (Opus spec, 54 KB).
- **Plan:** 155 s, 17.6K prompt and 25.9K completion tokens. Nine stages:
  1. draw tower floor
  2. move Professor Mittens
  3. place enemy targets (stomp)
  4. draw hand and energy
  5. play cards and Nova
  6. enemy phase loop
  7. floor reward loop
  8. Grand Vacuum boss
  9. finish screens and feel

  Reads: 53 of 54 matched a heading (stage 1 lost one). The cut is close to the hand cut of arm B,
  in a slightly different order: stomp before the turn loop, cards before enemy turns.
- **Chain:**
  - 11 stage runs over 9 stages, 275 turns, 40 min, 17 lost turns.
  - Every stage ran its full 25 turns; no `done()` anywhere.
  - Two retries, each saved by its first rerun: stage 5's first attempt did not boot ("Invalid or
    unexpected token"), and neither did stage 9's ("CFG is not defined").
  - Stage 9 (every screen, settings, audio and feel) first wrote at turn 19 on its first attempt
    and 13 on its rerun. It is the planner's biggest stage.
- **Final:** 9bf96c1cfd4a, 19 source files, 5070 lines.
- **Prod gates** on copy 6b70b774d455: error gate 0 rounds, play gate 0 rounds, nothing broken.
  The play gate drove title → NEW RUN (full HUD, a 5-card hand, End Turn, floor with ladders and
  enemies), the ESC pause with deck view, settings (reduced motion toggled), abandon, end screens
  with run stats, and high scores.
- Served on http://127.0.0.1:8951 for Nick's blind play against chain C (8) and the
  one-conversation baseline (2).

Read: the planner turns a design into a playable stage cut, and the chain holds together with the
keep-best rule. The battery runs next.

**2026-10-23 05:28–07:55 EDT, battery: four prod Flash-Next designs, all four gated clean.** The
penguin design that was to come first fell back to the bare ask: the decide model (JEV on vLLM,
via llama-swap) failed to start ("upstream command exited prematurely"). Not this lab's fault; it
is retried after the battery (queue2.sh).

The stage lists (9 stages each, 78–80 reads, all matched to headings):
- **hiragana:** paper study board · turn-based movement · gate question overlay · fail restart
  policy · exit win objective · level select boards · accessibility settings · unlock kana
  progress · title hud audio
- **frog platformer:** static lily lesson · frog movement controls · exit win state · pit fail
  retry · side scroll camera · hud pause shell · level select start · settings high scores ·
  title end polish
- **frogs eating bugs:** static pond scene · frog steering · spawn points and bugs · tongue catch
  · score counter · wasp life loss · health hud · pause and settings · title audio feel
- **wizard cat:** render static level one · basic grid movement · cards and hand · enemy turns
  and attacks · falling resolution · exit and reward · deckbuilding rewards · tower progression
  bosses · final screens feel

| game | stage runs | retries (stage: first error) | turns | `done()` | lost | minutes | final | gates (copy) |
|---|---|---|---|---|---|---|---|---|
| sp-opus | 11 | 2 (5: syntax, 9: CFG undefined) | 275 | 0 | 17 | 40 | 9bf96c1cfd4a | 0 / 0 (6b70b774d455) |
| sp-hira | 10 | 1 (6: undefined property) | 248 | 3 | 9 | 32 | 89ff46a6da2d | 0 / 1 round (6239197320f9) |
| sp-frog | 10 | 1 (7: stray `export`) | 249 | 2 | 10 | 36 | d973c0a94daa | 1 round / 0 (33e9ec0510bb) |
| sp-bugs | 10 | 1 (8: null property) | 238 | 5 | 14 | 26 | 9e4bd842fc25 | 0 / 0 (76a41629a0cd) |
| sp-cat | 9 | 0 | 225 | 1 | 7 | 29 | 32fa91f2477a | 0 / 0 (543cb30da1fa) |

Gates are error gate / play gate rounds; every play gate ended with nothing broken. Every retry
was won on its first rerun, so no chain ever went on from a broken game.

Against the one-conversation controls of the same four designs (same model, same card): three of
four capped at 200 without `done()` (hiragana, frog platformer, wizard cat). Frogs eating bugs
finished at 73. The staged chains spend 225–249 turns and end on a gated game every time.

Read, for the mechanics: the planner makes playable cuts on prod designs, not just on the Opus
spec. Every stage list follows the cut rules (world, then player, then loop, then screens), and
every chain finished on a booting, gate-clean game in about half an hour. Whether the games are
better is Nick's call by play.

**2026-10-23 07:58–08:48 EDT, sp-penguin: "A game about a penguin climbing a pyramid" (Nick's
ask).**
- **Decide fix:** the decide container OOMed in vLLM's fp4 autotune at
  `--gpu-memory-utilization 0.90`. That share is 29.6 of 32 GB (20.9 GB weights, 6.7 GB KV); the
  desktop holds about 1.6 GB, which left ~200 MB. Set to 0.85 in
  ~/Documents/llama-swap-config/llama-swap.yaml (uncommitted), and llama-swap was restarted while
  idle. Tested: KV 5.1 GiB, startup complete.
- **Design:** f254f7d986a9, 10,996 words, 3D.
- **Plan:** static dune steps · pip movement camera · add penguin jump · climb grip walls · fall
  fail restart · exit win score · unlock switch steps · switch door puzzles · finish game feel.
- **Chain:** 9 stages, 0 retries, final eedc7205ebd3.
- **Gates** on copy c50414b074cc: 0 / 0, nothing broken. Title, level select, Dune Steps
  gameplay with the score HUD, pause, settings.
- **Our screenshot:** a hand-drawn title card ("Penguin Pyramid, a small penguin, a very large
  pyramid"). After Enter, Enter, the gameplay camera sits against a wall with Pip out of view; to
  check by play.
- Served on http://127.0.0.1:8952.

**2026-10-23 08:48–09:46 EDT, penguin control: f254f7d986a9 built the stock way.** One
conversation on the prod build path, the same design.
- **Build:** capped at 200 in 58 min without `done()`.
- **Gates:** 0 / 0, nothing broken.
- **Title:** "PIP CLIMBS THE PYRAMID".
- **Our screenshot after Enter:** Pip (red scarf) on the spawn pad facing the pyramid steps,
  with a signpost, a star and the sun counter, the camera behind him. The staged game's camera
  sat inside a wall at the same point.

On first look the control is the better game, the opposite of the Opus-spec result. One pair
only, and a screenshot is not play. Served on http://127.0.0.1:8953 (not blind: I named both
to Nick).

**2026-10-23 09:46–11:37 EDT, fresh ask sp-carts: "shopping cart racing through a grocery store".**

| | design | run | retries | gates (error / play) | left broken |
|---|---|---|---|---|---|
| staged | a81bbbcec618 (13,128 words) | bc93cf2bf76e | 4 | 0 / 2 rounds (copy 7a315a6089ba) | "Back to title" from level select, no real title screen |
| one conversation | same | a81bbbcec618 | n/a | 0 / 0 | nothing |

- **Staged chain:** stages 1–7 clean. Stage 8 took three attempts (`renderCount` used before it
  was defined, then `loaderList is not defined`). Stage 9 took three (a stray comma, then `api`
  used before it was defined).
- **Control:** capped at 200 in 38 min.

Read: the roughest staged chain of the night, and the first where the control's gates come out
cleaner than the staged game's.

**2026-10-23 11:37–13:33 EDT, fresh asks sp-gears and sp-blorp.**
- **Gears**, "a puzzle game about rotating gears to power a lighthouse": design 06992a5bc1fc,
  6,969 words.
  - Staged: 9 stages in 27 min, 0 retries, `done()` in 6 of 9, gates 0 / 0 (copy 865d0ba7c731).
  - Control: `done()` at step 51 in 9 min, gates 0 / 0.
  - A small design does not need staging to finish.
- **Blorp**, "blorp the zingle 3000", the gibberish ask: the design read it as a silly 3D
  third-person open-world platformer (cf58d637677e, 14,321 words).
  - Staged: 0 retries, gates 0 / 1 round, nothing broken (copy 6ead78a968af).
  - Control: capped at 200, gates 0 / 1 round, nothing broken.

Fresh pairs so far, by gates: carts favours the control, gears and blorp tie, penguin favours
the control on our screenshots. Nobody has played any of them yet.

**2026-10-23 13:33–14:31 EDT, sp-gta6: "make gta6" (Nick's ask).**
- **Design:** 815570b85c6d, 11,670 words. 3D third-person open world, realistic, golden hour,
  final boss.
- **Plan:** dusk city canvas · rico movement camera · health lives respawn · weapons aim shoot ·
  enemies detection ai · quest objectives rewards · landmarks spawns unlocks · archon sol boss ·
  screens audio polish.
- **Chain:** 1 retry (stage 7). Late stages wrote late: stage 7 first wrote at turn 21, stage 8
  at turn 22 of 25.
- **Gates:** 0 / 1 round, nothing broken (copy dd83c3bcbccc).
- **Our screenshot:** opens straight into a dusk city of lit-window towers, with Rico in a red
  jacket on a spawn pad, a minimap, SunCoins, health and pistol ammo. Served on
  http://127.0.0.1:8954.
- **Control** (one conversation, same design, 815570b85c6d): capped at 200, "VICE DUSK: Solano
  Bay, a dusk that never ends".
  - Gates: 0 / 2 rounds. The play gate fixed undefined `wireSkills` and `wireFastTravel` in the
    pause panel, then left three core inputs broken: hold W, Space, mouse aim/fire.
  - Our headless Enter did not leave the title.
  - Served on http://127.0.0.1:8955.

The first fresh pair where the staged game is clearly ahead on mechanics.

**2026-10-23, bets queued (Nick: "we need a lot of bets").** Each runs once on the carts design
(a81bbbcec618), the roughest staged chain of the night, against sp-carts and its control:

| bet | what changes | evidence | how |
|---|---|---|---|
| B1 | the planner picks 3–12 stages by design size | gears: the control finished in 51 steps, staged spent ~220 | `--prompt plan_adaptive.txt` |
| B4 | screens get their own stage, then audio and feel | Opus stage 9 first wrote at 13–19; carts stage 9 took 3 tries | `--prompt plan_split_end.txt` |
| B6 | turn budget 20,20,20,25,25,30,30,35,35 | late stages write late and break more | `--budgets`, sp-carts' plan |
| B3 | one conversation: each stage after the first opens on the previous stage's whole history, with no pre-read (retries fall back to the pre-read) | first writes at turns 9–22 in late stages | `--opts '{"carry": true}'`, sp-carts' plan |
| B5 | `done()` refused (at most twice a stage) until the game was played after its last edit | stages end without proving their done line | `--opts '{"play_before_done": true}'`, sp-carts' plan |

Not built yet: B2, the prod play gate after every stage, with what it finds fed into the stage's
retry.

`queue5.sh` runs B1, B4 and B6. `queue6.sh` restarts the lab control plane while idle, so
planned.py's B5 patch is loaded where the turns run, then runs B3 and B5. Stage runs use
`run_stage_b.sh`, which adds a per-stage budget.

**2026-10-23 15:02–16:54 EDT, B1 (adaptive stage count) on carts: idea failure here.**
- **Plan:** the planner took the maximum, 12 stages.
- **Breakage:** stage 8 (three new levels, unlocks, level select, four collectible kinds and side
  quests) broke on all three attempts, each on a different error: `rand.range` not a function,
  `decorGroup` declared twice, `data.traps` not iterable. Every later stage started from that
  broken game, and none of its 12 runs repaired it.
- **Cost:** 22 stage runs, 550 turns, 93 min.
- **Gates** (copy f6d4ddabaf1c): the error gate fixed the boot in 1 round; play gate 2 rounds;
  left broken: the `r` key.
- **Against sp-carts** (9 stages, 4 retries, 1 broken input left): more turns and more time for a
  game with the same kind of leftover.

Read: given room, the planner does not cut smaller; it adds stages and still packs one. And a
chain whose base breaks never recovers, because no stage is told the game it starts from is
broken. That is B7, queued.

**2026-10-23 16:54–17:37 EDT, B4 (split final stage) on carts: promising.**
- **Plan:** static grocery diorama · wobble cart controls · cart jump system · physics object
  bodies · scoring bins and plates · objectives and round end · l2 progression flow · menus and hud
  gaps · audio and juice.
- **Chain:** 9 stage runs, 0 retries, 225 turns, 38 min. 16 lost turns, 10 of them in stage 3: a
  late loop of empty `code` calls and one invalid program sent four times, the local model's
  known tool-call failure, not the bet.
- **Gates** (copy 82df77167a6e): 0 / 0, nothing broken.
- **Against sp-carts** (same design, plan.txt): 4 retries, play gate 2 rounds, 1 input left
  broken.

One run, and the plan differs beyond the split (the planner is not deterministic), so this is a
lead, not a result. Worth a battery.

**2026-10-23 17:37–18:19 EDT, B6 (back-loaded budget) on carts: promising, cleanest comparison.**
Same plan as sp-carts (copied), budgets 20,20,20,25,25,30,30,35,35.
- **Chain:** 10 stage runs, 1 retry (stage 2, at 20 turns), 260 turns, 40 min, `done()` in
  stages 6 and 7 (30 turns each).
- **Late stages:** stages 8 and 9, which took sp-carts three attempts each at 25 turns, passed
  first time at 35.
- **Gates** (copy be8fe3cdb7a3): 0 / 0, nothing broken.
- **Against sp-carts** (same plan): 4 retries, play gate 2 rounds, 1 input left broken.

Read: only the budget changed, and the late breakage went away; the one retry moved to a 20-turn
early stage. One run. Worth a battery, along with B4.

**2026-10-23 18:19–19:33 EDT, B3 (one conversation across stages) on carts: no clear gain.**
Same plan as sp-carts. Stages 2+ opened on the previous stage's whole history (checked: stage 2's
build began with stage 1's 60 messages); retries are branched runs and fell back to a fresh agent.
- **Chain:** 13 stage runs, 4 retries (stage 4 once, stage 8 twice, stage 9 once), 323 turns,
  66 min.
- **First writes:** carried stages 2–3 wrote by turn 2–3. Stages 5–9 still first wrote at 8–14,
  because compaction had cut the history by then.
- **Stage 8:** failed all three attempts again. It also broke under sp-carts and B1, but not
  under B6 at 35 turns. Stage 9's retry repaired it: the first time a later stage fixed an
  earlier break on its own.
- **Gates** (copy c19bdb77d868): 0 / 1 round, nothing broken.
- **Against sp-carts:** the same 4 retries, slightly cleaner gates, about 50% more time.

Read: carrying the conversation saves orientation only until the first compaction. The stage 8
breakage tracks the budget, not the agent.

**2026-10-23 19:33–20:28 EDT, B5 (play before done) on carts: the lever never moved.**
Same plan as sp-carts.
- **The lever:** across 11 stage runs the builder called `done()` once (stage 7), after it had
  already played, so the refusal never fired. Every other stage ran out its 25 turns.
- **Chain:** 2 retries (stage 8 twice; stage 8 again), 274 turns, 43 min.
- **Gates** (copy c2838ea6e246): 0 / 2 rounds. Left broken: Escape and "back" in the settings
  panel, a click outside it, and Escape in the level loader.
- **Against sp-carts:** fewer retries, more left broken. All of that is noise from runs this bet
  did not touch.

Read: a rule on `done()` cannot help a builder that almost never calls it. Not a lever on this
model.

**2026-10-23 20:28–21:54 EDT, B7 (repair first) on carts: works.**
B1's 12-stage plan again. A stage whose starting game does not load opens with "The game in this
folder does not load right now. The page throws: <errors>. Make it load first, then build this
stage." (`run_stage_c.sh`, `--opts '{"repair_first": true}'`).
- **Stage 8 broke on all three attempts again,** as in B1.
- **Stage 9** was told "Identifier 'save' has already been declared". All three attempts fixed
  it in their first writes (turn 3: `save()` renamed `persist()` in highscore.js), then stalled
  on `updateCollectibles is not defined`. That error was already in stage 8's game, masked
  because the page stops at the first throw.
- **Stage 10** was told that one, fixed it, and booted.
- **Stages 11–12** booted.
- **Chain:** 16 stage runs, 399 turns, 72 min. Final c910585023ec boots.
- **Gates** (copy 065ad27ae852): 0 / 2 rounds, nothing broken.
- **Against B1** (same plan, no repair line): broken from stage 8 to the end; the error gate
  rescued the boot; 22 runs, 550 turns, 93 min, the `r` key left broken.

Read: telling a stage the game it starts from is broken makes the builder fix it; B1's twelve
later runs never did. A sharper line would ask for the page to be checked after each fix, since
stacked errors surface one per stage. Cheap, and worth keeping whatever else wins.

**2026-10-23 22:21–23:20 EDT, B4+B6+B7 combined on carts: clean gates, gains did not stack.**
- **Setup:** `plan_split_end.txt` (a new plan, 9 stages), budgets
  20,20,20,25,25,30,30,35,35, repair first.
- **Chain:** 12 stage runs, 3 retries (stage 6 twice at 30 turns, stage 8, the menus stage, once
  at 35), 335 turns, 57 min. Repair-first never fired: every retry recovered within its stage.
- **Gates** (copy 78554851e06c): 0 / 0, nothing broken.

| carts run | retries | gates (error / play) | left broken | turns | minutes |
|---|---|---|---|---|---|
| sp-carts (baseline) | 4 | 0 / 2 | 1 | 225 | ~45 |
| B4 split end | 0 | 0 / 0 | 0 | 225 | 38 |
| B6 back-loaded | 1 | 0 / 0 | 0 | 260 | 40 |
| B7 repair (B1 plan) | 6 | 0 / 2 | 0 | 399 | 72 |
| B4+B6+B7 | 3 | 0 / 0 | 0 | 335 | 57 |

Read: every bet ends gate-clean where the baseline did not, but retries swing with each new plan
(B4 and the combined run each drew their own). One design and one run each cannot rank them.
The battery is next: B6 alone, which kept sp-carts' plan, over the six designs with existing
staged baselines.

**2026-10-23 23:36 – 2026-10-24 03:34 EDT, B6 battery: fewer retries, same cost, gates even.**
Each design's own sp- plan copied, only the budget changed to 20,20,20,25,25,30,30,35,35.

| design | baseline retries | B6 retries | baseline gates | B6 gates | baseline turns / min | B6 turns / min |
|---|---|---|---|---|---|---|
| hiragana | 1 | 0 | 0 / 1 | 0 / 0 | 248 / 32 | 238 / 29 |
| frog platformer | 1 | 0 | 1 / 0 | 0 / 1 | 249 / 36 | 237 / 34 |
| frogs eating bugs | 1 | 0 | 0 / 0 | 0 / 0 | 238 / 26 | 228 / 25 |
| wizard cat (Flash-Next) | 0 | 0 | 0 / 0 | 0 / 0 | 225 / 29 | 240 / 34 |
| penguin | 0 | 0 | 0 / 0 | 0 / 0 | 225 / 40 | 240 / 45 |
| gta6 | 1 | 1 (stage 2, at 20 turns) | 0 / 1 | 0 / 2 | 249 / 40 | 260 / 43 |
| carts (earlier) | 4 | 1 | 0 / 2, 1 left broken | 0 / 0 | 225 / ~45 | 260 / 40 |

Every final boots and gates with nothing broken except baseline carts.

Read: across seven designs, back-loading the budget cut retries from 8 to 2 at about the same
turns and minutes. The two B6 retries both came on early 20-turn stages; the late-stage breakage
the baselines had is gone. Gate rounds are a wash. A mechanical win; whether the games are
better is Nick's to play. The B6 penguin (:8959) frames Pip at the bottom edge instead of behind
a wall.

**To play, blind, fresh pairs:** http://127.0.0.1:8971/8972 carts, 8973/8974 gears, 8975/8976
blorp. Key: /var/tmp/stage-planner/blind_key_fresh.txt. Penguin, not blind: 8952 staged, 8953
control.

**To play, blind, by design:** http://127.0.0.1:8961/8962 hiragana, 8963/8964 frog platformer,
8965/8966 frogs eating bugs, 8967/8968 wizard cat. In each pair, one is the staged game and one
the one-conversation control, shuffled. Key: /var/tmp/stage-planner/blind_key_battery.txt. The
Opus-spec staged game is on 8951. Queued after this run, at Nick's ask: a fresh prod design
of "A game about a penguin climbing a pyramid" (local Flash-Next), then its chain.

## Outcome
