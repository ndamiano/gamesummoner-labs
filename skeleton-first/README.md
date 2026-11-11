# skeleton-first — the genre's crappy framework first, the concept's things replace its placeholders

Status: single-run
Control: the cats ask's two builds of 2026-11-07 in `labs/pitch-interrogate`: the mechanics-curation
control `d2321b3512ff` (Nick: "functions, and is fine. It's not good, it's not bad") and the ninth
arm `b8351a8361eb` (Nick: "I have no fucking clue what's going on. The screen is a huge fucking
mess").

## Purpose

Both cats builds of the pitch-interrogate night fail the same way from opposite sides. The control
has the tower-defense skeleton (a path, a base at its end, crate cells beside it, towers that hit
the enemy furthest along) and no world: a paw-tile grid. The ninth arm has the world (a dawn fish
market, five cats, four thieves, stalls, crates, ice, awnings, a bell) and no skeleton: the design
ruled every stall a target and there is no path at all; the plan's stage 1 drew the whole market
static, with every node of the design's graph labelled, before anything walked. Nick's read of the
night: "something is wrong with our approach ... too much liberty?", and then how he would build
it with an AI: get the concept (a fish display, a bunch of cats, the shop's exterior with ocean and
docks to the right, mice and other vermin); then "a crappy framework to play it": a procedural path
top to bottom, circles that walk it, a menu to put colored circles off the path, range and attack
speed, a minor attack animation, health bars, removal on death; then replace the dots with mice,
the towers with cats, the tower animations with cat animations; then gold and lives at the top, a
build menu at the bottom, a hamburger menu.

Three things in that sequence the pipeline does the other way round. The skeleton plays with
placeholders before any content is drawn; prod's planner is told the opposite ("Stage 1 puts the
world on the screen ... drawn in the design's look. Nothing moves yet.", `prompts/stage/plan.txt`).
Content only ever replaces a placeholder, so it can never redefine the skeleton; in the ninth arm
the page's "the market is the target" became twelve targets and no path. And every step's done is
something you see ("circles walk from top to bottom"), where the plan's stage 1 done was "all nodes
and pads visible". Liberty is in the wrong place: the design step has all of it (every number,
rule and layout "left open", so it invents), the build has none; in Nick's sequence the skeleton
has none (it is what a tower defense is) and the concept's things have it, one placeholder at a
time.

## Hypothesis

**What changes.** For one ask, the design and the stage plan are replaced by hand: `cats/design.md`
is the concept in Nick's words plus one paragraph on how it is built; `cats/stages.json` is his
sequence as fourteen stages, each with its done line. The builder, the stage framing, the gates
and the model are prod's. Nothing else changes. (One stage is mine, not his: "the place", which
replaces the background with the market and docks; his list named them in the concept and never
placed them. Cut it if it is wrong.)

**What is measured.** Nick plays it against `d2321b3512ff` and `b8351a8361eb`: is it a tower
defense, is it clearly cats at a fish market, is the map a map. Also: which stage each thing
arrived in and whether a skin stage changed a rule (the diff of each skin stage against the
skeleton's numbers), the build's steps and minutes, the gates.

**Why it should move.** The game is a known thing built in the known order; the concept has
nowhere to put a rule, so it can only change what things look like and which kinds there are.

**Idea failure looks like.** The builder cannot land the skeleton in its tiny stages (a path that
does not draw, walkers that do not walk), or the skin stages make the same junk from the same
builder (the concept's nouns become labels and props), or Nick finds it a worse game than the
control. If it works at the human ceiling, the next lab is the model writing the skeleton from
the genre and the skin from the concept, instead of a 60 KB design.

## Setup

Model: Flash-Next on the local card through llama-swap :5001, started by `tiers.Services`. Control
plane `venv/bin/python run.py` up on :8000.

    venv/bin/python labs/skeleton-first/build.py cats

`cats/stages.json` is the plan as prod stores it (`stages.json` in the run's design folder), with
budgets from `stages.budgets(14)`; `cats/design.md` is pinned as the run's design; the build runs
through `build_chain.kickoff(run, kind="build", designed=True)` as every lab build does. Run id in
`cats/build.txt`, result in `cats/build.json`, game at
`/var/lib/gamesummoner/output/runs/<run>/game`.

## Log

**2026-11-07, 10:47 to 10:50, the process planner once: `venv/bin/python labs/skeleton-first/plan.py
cats`.** One Flash-Next call on `cats/design.md` (Nick's concept paragraph, JEV's 23 decided lines for
the ask, one paragraph on how it is built) with `plan_process.txt`: 172 s, 1.1K prompt tokens, 34K
completion (reasoning), 23 steps in `cats/stages.json`. The steps follow the four parts in order:
1–9 the framework in placeholder shapes (path, circles walk it, click beside it places a square,
range and a 1 s cooldown, a line and a flash per hit, health bars, removal at zero, a wave timer, a
pause toggle from JEV's "real-time with pause"); 10–13 the replacements (circles to mice with a leg
wiggle, the square to the sleepy, pounce and swipe cats with right-click cycling the kind, the line
to a blink, an arc and a swipe trail, the background to the fish display, docks and crates and
barrels the cats sit on); 14–17 the UI (JEV's four HUD counters, the bottom build menu replacing
the right-click cycle, JEV's five screens, the accessibility settings); 18–23 the game (costs with
bounty and starting gold, waves scaling by number and difficulty, lives on the fish display with a
fail screen and restart, level definitions with different wave sets, score and high scores, a last
balance step that tunes numbers only until early rounds are losable empty and winnable with a few
cats placed well). Nick's thirteen are there near verbatim, and the crappy-then-real shape repeats
on its own (step 11's right-click cycle is replaced by step 15's menu). Every done line is a thing
seen. Noted, not changed: towers pick the nearest enemy (Nick: nearest and furthest along are both
valid, many games let you swap); levels are one map with different wave sets (Nick: less exciting,
fine if meaningfully different). Nick: "Let's do this." Build launched.

**2026-11-07, 10:53 to 11:58, the build: `venv/bin/python labs/skeleton-first/build.py cats`, run
`816d5ac86674`.** 64 minutes, 23 stage builds, 606 jobs, none failed, every stage checked once
with 0 errors, no fix build; play gate 0 rounds, nothing broken; gate impression "a compact,
well-organized tower defense: the fish-market theme is charming, the economy and wave HUD are
legible at a glance ... depth is modest but coherent for a single market", its rough edge
"clicking a tile that holds a cat gives a tooltip rather than an info panel, and clicking empty
floor does not cleanly cancel a pending placement". Per-stage commits in the run's `game.git`:
stage 1 is the vendored libs plus `level.js` 69 lines, `render.js` 92, `game.js` 160 (a fixed
six-leg waypoint path, 48 px, with `pointAtDistance` and `onPath` for later stages, a spawn
portal and a red bullseye labelled THE FISH); stages 2 to 9 are 48 to 237 lines each; the four
replacement stages 237, 479, 351 and 691 lines; the UI stages 239, 193, 689, 153; the game
stages 109, 137, 301, 391, 202; the balance stage 21 lines in and 20 out, every one a number
(first countdown 5 to 8 s, vermin hp 30 to 32, per-wave hp step 12% to 15%, purse per kill 6 to
7, sleepy cat 45 to 55 coins and 18 to 20 damage, pounce 30 to 35, swipe 18 to 20, level purses
and lives up). The replacements changed no rule: `level.js` is untouched from stage 9 to 13, and
what left `game.js` in those stages is the placeholder constants (`WALK_SPEED`, `TOWER_RANGE`,
`FIRE_COOLDOWN`, `TOWER_DAMAGE`, the yellow line) replaced by the three kinds' table and their
motions. Final game: `game.js` 2092 lines, `render.js` 1948, `market.js` 670, `level.js` 171.

Screens at stages 7, 10 and 13 and at the end are in the session scratchpad under `skel/`. After
stage 7: a gray path, SPAWN, THE FISH, black circles with yellow bars, a dashed placement cursor;
Nick's crappy framework to the letter. After stage 10: the circles are pink mice with tails,
nothing else moved. After stage 13: the fish display under a striped awning at the bottom, docks
with boats, gulls, rope coils and barrels on the right, crates along the path with the cats
sitting on them, a mouse hole at the spawn, a FRESH FISH sign, sleepy cats with Zs; the concept
near literally, and the path, placement and waves as they were. Headless on the finished game
(`skel.py` in the scratchpad): three levels (THE FISH MARKET 4 waves, THE LATE DELIVERY 7, THE
WHOLE MARKET 10; same map, harder mixes of mouse, beetle, rat), three cats (sleepy 55 coins reach
165 dmg 20 every 2.5 s; pounce 35, 130, 9, 1.2 s; swipe 20, 80, 3, 0.4 s), purse 100, lives 10.
Level 1 with nothing placed: wave 1 takes 4 lives, wave 2 four more, failed in wave 3 at 0/10. Level
1 with a sleepy and a pounce cat beside the first leg and nothing else bought: LEVEL CLEAR at wave
4 with 3/10 lives, score 450, level 2 unlocked. The balance stage's own done line holds. 0 page
errors. Defects seen: the bottom status strip draws two strings over each other (from stage 10 on,
never fixed); the game opens on the prep countdown with no title screen (the title is an item in
the M menu); the placement mode is sticky, as the gate said.

**2026-11-07, Nick's play of `816d5ac86674`.** "Damn, this is probably the best version of this game
that we've got. By like a lot. It's *actually* the game I wanted, and while it's still got issues,
it actually looks good." Verdict: works. Against the same ask's control `d2321b3512ff` ("fine")
and the ninth arm `b8351a8361eb` ("a huge mess"), the same builder, model and gates; the only
change was the concept plus the process plan in place of the 60 KB design and prod's plan. The
concept was Nick's own paragraph; the next run has the model write it from the ask and JEV's
decisions, since prod has no Nick.

## Outcome
