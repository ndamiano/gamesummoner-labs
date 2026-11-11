# tier-chain

Status: single-run

Control: `labs/pitch-interrogate` run 26d2aeb66c16. The by-hand zombie design (51 KB, four
tiers, 15 buildables) on prod's staged chain: nine stages, all tier 1, all passed first time;
tiers 2 to 4 were never planned.

## Purpose

Nick, 2026-11-06: "A good design doesn't limit itself because the build can't do it. That's a
build problem, which we should solve." The first build-side limit met was the planner: its
prompt asks for exactly nine stages (`STAGES = 9`, `src/maestro/codegen/stages.py`), and on a
four-tier design all nine went to tier 1. The chain itself runs a plan of any length. Three more
limits were read off the code and that run, not yet measured past tier 1:

- A stage's developer is handed every file up front only while the game's own code is under
  100 KB (`FILES_CAP`). The zombie game passed that after stage 7 (110 KB) and ended at 171 KB;
  stages 8 and 9 ran from the code map alone and passed.
- A stage passes when the page boots without errors. Nothing checks that an earlier stage's
  feature still works.
- The end gates play for a short session. On tier 1 the play judge never caught a human.

## Hypothesis

Plan one tier at a time, with the code map of what is already built in the planner's hands, and
run prod's chain on each plan in turn, on the same game folder. One prompt changes:
`plan_tier.txt` in place of `prompts/stage/plan.txt`. It tells the planner tiers below are
built, asks for 3 to 9 stages for this tier only, and asks each stage to name the existing files
it touches. Everything else is prod: stage prompts, build prompt, stage check, gates.

Measured: how many of the design's tiers end up built and playing, by `probe.py`, which drives
the game through the design's own debug API (seven tier 1 checks verified by hand on the
control, then best-effort checks for tiers 2 to 4), and by Nick playing it. Also whether tier 1
keeps passing as tiers land on it, which is the regression the boot check cannot see.

Expected: tier 2 is planned and built. Unknown how far the chain gets with every stage starting
from the code map alone.

Idea failure: the planner cannot cut a tier it has only a code map for (stages that restate
tier 1, or name files that do not exist), or a tier's stages break tier 1 faster than they add
to it.

Two settings differ from the control besides the prompt, both chosen so that a finished game is
likelier by morning, as Nick asked: every stage of tiers 2 to 4 gets 35 turns (prod gives 20 to
35 by position), and when a tier 1 check breaks after a tier, the driver asks for one prod fix
build of at most 60 steps with the failed checks as the playtest note.

## Setup

From the repo root, with `venv/bin/python run.py` up:

    venv/bin/python -u labs/tier-chain/tiers.py 26d2aeb66c16 2 4 > labs/tier-chain/tiers.log 2>&1

- `tiers.py` forks the source run into a new private run (design, game folder and its snapshot
  history), so the control stays playable as tier 1. For each tier it makes the plan call
  straight to the local Flash-Next with the request prod sends, lands the plan as prod does,
  starts prod's chain at stage 1, waits through the stages and gates, runs the probe, and keeps
  a copy of the game under `~/output/tier-chain/<run>/tier<N>`. It starts the GPU runner and
  restarts it when it dies or no job has finished for 20 minutes.
- `probe.py <game dir> <tier>` prints one JSON line of checks.
- Model and card: Flash-Next (Basalt IQ3_S) on the local 5090 through llama-swap.

## Log

**2026-11-06, 01:29 to 02:53, one run: tiers 2, 3 and 4 of the zombie design on a copy of the
tier 1 build. Run ac23f047b078, forked from 26d2aeb66c16 at snapshot 03d2580.** Flash-Next on
the local card, prod chain, 35 turns a stage. `tiers.log` has the driver's account and
`ac23f047b078/results.json` the probe reports.

| tier | plan call | stages | stage checks | gates | minutes | probe after the tier |
|---|---|---|---|---|---:|---|
| 2 | 141 s | 6: free wifi lure · fridge harvest bank · banana pit lure · brain rot station · free puppies drag · tier 2 polish tests | all first attempt | play gate 1 round, fix build of 81 steps | 30 | tier 1 7 of 7, tier 2 5 of 5 |
| 3 | 106 s | 7 after a split by hand, see below | all first attempt | clean | 27 | tier 1 7 of 7, tier 2 5 of 5, tier 3 2 of 2 |
| 4 | 91 s | 4: place walls and doors · use walls as cover · decor and home score · finish tier 4 tests | stage 3 retried once (did not boot), the rest first attempt | clean | 21 | tier 1 7 of 7, tier 2 5 of 5, tier 3 2 of 2, tier 4 2 of 2 |

- Totals: 17 stages, 629 build steps and 81 fix steps, 758 jobs, none failed, 84 minutes
  including the three plan calls. The game's own code went from 171 KB to 413 KB, 14 modules to
  22 (lures, fridge, station, puppies, heat, law, weapons, home added). Every stage started over
  the 100 KB pre-read cap, from the code map and the files its stage text named.
- No tier 1 check broke after any tier, so the fix-on-regression build never ran.
- Hand intervention on tier 3 (Claude, 02:06:51, while stage 1 was running). The planner
  returned four stages: heat and witnesses · law patrol and freeing · weapons and donuts · tier
  three polish tests. The second held all of §4.12 (three kinds of law, patrols, investigating,
  freeing, shooting, bullets, eating the law) and the third both weapons, stun and the donut
  lure, against the prompt's "one system per stage". Those two were replaced by five: law
  patrols · shooting and bullets · investigating and eating law · weapons and stun · free
  donuts. The planner's own plan is kept in `ac23f047b078/tier3-stages-as-planned.json`. So
  tier 3 does not measure the planner's cut.
- Probe correction. The first tier 2 report read 1 of 5. Both causes were in the probe: it
  tapped E where the game wants the key held, and it tested lures on humans spawned through the
  debug API, who stand still and cannot walk to a lure. Checked by hand on the kept tier 2 copy
  (fridge stores and feeds; the banana stand pitted a passer-by in 10 s), the checks were
  rewritten to use the game's own passers-by, and the rerun on that copy read 5 of 5.
- Look at the finished game with one of every building placed and heat set to 16: all fifteen
  buildables place and draw, a police pair arrives, one officer walked into a box trap and is
  held yelling, the other investigates with a "?", flyers are on the lamp posts, the HUD shows
  heat badges with "Police" and two carried brains. No page errors. Two HUD labels overlap
  ("CARRIED BRAINS" with its count, the junk names with each other).
- Not covered by the probe: weapons and stun, the donut lure, investigating and freeing, guard
  squads, bullets stopping at walls, the home score, any balance. Tier 2 to 4 checks were
  written the same night and are best effort.

Read: planned a tier at a time, all four tiers of the design were scheduled and built on prod's
chain, and the earlier tiers kept working as the later ones landed. The planner cut tiers 2 and
4 well and under-cut tier 3. Blind stages and the boot-only check did not stop the build on
this game; whether they cost quality is not measured. Verdict: works, on one run with one hand
intervention; Nick has not played it.

**2026-11-06, change note "can you make the art a bit better?" on `ac23f047b078` (Nick's words, the site's change path, `change.py`).** One `change` build, 60 steps, 5.6 min, succeeded; probe still passes every check of tiers 1 to 4. It touched `src/render.js` (+445, −16) and `src/main.js` (+3). All of it went on the ground and on lighting: grain, mow stripes, litter, leaf drift, kerb grit, contact shadows under buildings, a dusk vignette. No character, building or junk spot was redrawn and the two HUD label overlaps are unchanged. Side by side in the same staged yard the two versions read as nearly the same picture. The builder cannot see the screen (`play` returns data, not a picture), so it had no way to tell what looked bad. Before: snapshot `67e1365` and `~/output/tier-chain/ac23f047b078/tier4`; after: snapshot `518b380` and `~/output/tier-chain/ac23f047b078/art1`. Earlier the same morning I rendered 11 sample sprites through the image path on scratch run `0a4c8b293f05` (`samples.py`): every render was refused locally with "no safety verdict — classifier unavailable: No module named 'timm'", so no generated art can land on this box as it stands. `plan_art.txt` is a staged art plan prompt that was written and never run.

**2026-11-06, Nick's verdict on `ac23f047b078` after the art change.** "Overall, I lean towards this being a solid 7/10 for a first draft." "It seems to work properly, which is a good thing!" What he named as wrong: "we have a zombie that looks... not zombie... and the traps and what not don't really show off what they are"; "the build menu has a bunch of \"undefined\" in it"; "free donuts extending past the sign". On the art change: "the improvements they're fine, but they missed all the actual issues". On the builder not seeing the screen: "The fact that it's blind is definitely part of the problems." On a refine pass: "It desperately needs a refine pass, not just for graphics", and of an art refine pass, "I'm not sold on it right this moment". Checked after: the "undefined" is the three tab labels of the build menu. `panelLayout` in `src/render.js` builds each tab rectangle as `{id, x, y, w, h}` without the name, and `drawBuildPanel` prints `tab.name`. The same menu stacks each row's cost letters into the name above it and runs long names and the hint line off the right edge of the screen. None of this throws, fails the boot check or fails a probe check: every defect he named can only be found by looking. Cost, corrected for him the same day: the 84 minutes was tiers 2 to 4; the whole game was about 118 minutes of wall time and 95.5 minutes of GPU job time over 1,061 llm jobs, roughly $3 to $4 at the 6000 Pro rates on record against a $5 game (an estimate from local minutes, not measured on prod).

## Outcome
