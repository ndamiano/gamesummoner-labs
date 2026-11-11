# bible-first — the game we want, then the minimum that is a game, then the skeleton-first build

Status: done
Control: the bakery ghost ask on the staged chain, `docs/experiments.md` 2026-10-30 (Flash-Next
e30b96b10489 = 4, "I can get a single cookie, but do nothing with it"; DeepSeek 6.6–7; Opus 8) and
`labs/template-ask` 2997d5c16447 (a 99-word shape-plus-nouns paragraph, naked, DeepSeek: 6,
"mechanically it works ... it doesn't feel like a bakery. They enter with the bread"). Shape of the
run: `labs/skeleton-first` 816d5ac86674 (cats TD, Nick's concept + process plan on Flash-Next,
"the best version of this game that we've got. By like a lot").

## Purpose

Nick's two-day read of the week's builds (2026-11-07/08): every path mixes "make it functional"
with "add content" in one pass, and the one run that separated them (skeleton-first) is the one he
called the game he wanted. Both control designs on the bakery ghost were read for a why: 13,448
and 10,136 words, zero story; JEV's mechanics picks turned into contracts. The design stage has
never written a premise. The template-ask paragraph kept every noun and still produced customers
who walk into a bakery carrying bread, because the shape (Pac-Man) was chosen first and the fiction
bent to it.

What Nick asked for: a "holy bible" of the game we want (the story: why Pip steals pastries, why
he cannot buy them, what he needs tonight, how it resolves; the world; all the intended content,
procedural bakeries included) that is never cut because the builder cannot finish it; then,
separately, the minimum that turns it into a game (one bakery by hand, Pip in it, the one loop);
then the skeleton-first process (framework → the concept's things replace placeholders → UI →
game-ify); then content, as more stages, long horizon.

## Hypothesis

**What changes.** The design stage becomes, on the prod path with JEV's decisions kept: (1)
`bible.txt`: the model writes the game we want under Story / World / Content / A Session /
Resolution, 600–1,200 words, nothing about how; (2) `minimum.txt`: from the bible, the model
writes `# 0. CONCEPT` (≤150 words, one hand-built place, the player, the people acting on their
own, the one verb, two or three kinds of each thing) and `# 2. HOW IT IS BUILT` (skeleton-first's
paragraph, with the shape named as "a <shape> is <its parts>"); (3) `design.md` = concept +
decisions + how it is built + the bible; (4) skeleton-first's `plan_process.txt` cuts the stages;
(5) the staged build as prod runs it. Private run, so every seat is Flash-Next on the local 5090,
the builder that got a 4 on this ask and built the cats TD.

**Measured.** The bible (does it answer why), the concept (does the shape follow the fiction, or
the fiction bend to a shape), the stage list, stage checks, and Nick's play against the floor he
named: "the floor needs to be a playable game" of the subway-FPS class, and is it the thing asked
for. Bucket, not a 1–10: slop / toy / thin clone / the game asked for.

**Expected.** A playable bakery-ghost game whose loop comes from the fiction (customers buy,
pastries cross the counter, a scare opens a window), on the model that produced a 4 on this ask
through the mechanics design. Cost local; ~1–1.5 h like the cats TD.

**Idea failure.** The bible reads as a why and the game still plays as the template-ask
Pac-Man (fiction in the names only), or the loop does not close as in e30b96b10489. A bible with
no why, or a concept that is a scene with no verb, is an implementation failure: prompt fix and
rerun from `plan`.

## Setup

From the repo root, with `venv/bin/python run.py` up:

    venv/bin/python labs/bible-first/build.py plan bakery   # JEV, bible, minimum, stages; stops
    venv/bin/python labs/bible-first/build.py build bakery  # the staged build on bakery/run.txt
    venv/bin/python labs/bible-first/build.py battery cats wizardcat zombie alienfarm

`plan` writes `decisions.txt`, `bible.md`, `minimum.md`, `design.md`, `stages.json` here and lands
design.md and stages.json in the run; `build` writes `build.json`. Both start the GPU runner and
stop it after.

## Log

**2026-11-08 13:19 EST, `plan bakery`, run 2546d62858f8 (private, Flash-Next local).** JEV's
decisions match the 2026-10-30 controls (2D side-on, single screen, lose a life, silly, pixel art,
10 core / 15 supporting / 10 extra mechanics). Bible 1,008 words (`bakery/bible.md`): has a why —
Pim, a former mascot, ate the Head Baker's Moonberry Proof and is bound to the bakery; sunrise
erases any ghost that has not paid it back, so waiting is not open — and a World whose cast acts
on its own (customers browse and buy, a baker patrols with a rolling pin, an inspector, a cat in
the oven). Defect: Content and A Session narrate JEV's 35 mechanics one by one (matches, medals,
ranks, decoration, leaderboard, combos, transform, traps, hints); the catalogue leaks into the
fiction because the prompt hands it the mechanics bands as decisions. Candidate fix for the next
iteration: give `bible.txt` only the look-and-kind decisions. Minimum (`bakery/minimum.md`) is
clean: one hand-built side-on bakery, tiny ghost, one verb (scare), three people (sleepy customer,
suspicious customer, baker guard), two pastries, three hiding spots, detection meter, sunrise
timer, moon gate; shape named from the fiction ("a timed one-screen stealth heist is 1 room, 1
player, 1 scare verb, 3 people, 2 pastries, 3 hiding spots, 1 detection meter, 1 timer"). Carried
defect from template-ask: customers still drop pastries when scared rather than buying at the
counter, though the bible said "browse and buy". Plan: 24 stages in the four parts (room shell →
player dot → moving dots → static boxes → collectible dots → scare state → detection value →
caught check → life counter → plain timer → score counter → screen states | tiny ghost → customer
actors → hiding spots → pastry items → scare verb → detection meter → sunrise timer | top hud →
bottom menu → menu button | night escalation → balance pass). 8 minutes for the whole plan phase.

**13:28, `overnight.sh`:** `build bakery`, then `battery cats wizardcat zombie alienfarm` (asks
in each folder; cats is the 816d5ac86674 ask with the model's concept in place of Nick's). Nick
afk; results below as they land.

**14:51, bakery 2546d62858f8 done.** 84 min, 24 stage builds (15–35 steps each), 625 jobs none
failed, every stage booted clean first try, no fix round. "PIM'S NIGHT SHIFT — Tiny Ghost Bakery
Heist": pixel side-on bakery (street window, register, flour sacks, display case, cold oven, moon
gate), the ghost, a customer, a baker and a guard walking their routes, scare on Q/E with a
cooldown bar, a "quiet" detection meter, sunrise bar, lives with a caught counter, moon gate at
score 20, title/settings/high-scores menu. Boots with no console errors; headless flailing got
caught once in five seconds, so detection works. Defects seen: the HUD is drawn twice (the
framework's thin placeholder strip HEALTH/SCORE/TIME/COMBO was never removed when the hud stage
replaced it with panels); a 2:30 night with 2 pastries is a very small session. Against the
Flash-Next control e30b96b10489 (4, "get a single cookie, but do nothing with it") the loop
closes on the same model. Served at :8955 (`shot_title.png`, `shot_play1.png`). Nick plays.

**14:51–14:59, a stall between labels.** The battery's first cats run (bff306578499) died at
start: tier-chain's `Services.stop()` sent SIGTERM and returned, the next `ensure()` started a
runner while the old one was tearing down, the new runner saw the old decide engine "ready in
0s" and then lost it ("stopping, held=('decide', None)"); the Basalt llm engine (29.5 GB) also
outlived its runner and had to be killed by pid. Fixed `stop()` to wait for the runner (90 s,
then kill); battery relaunched from cats. Open: why the runner's SIGTERM left Basalt up.

**16:20, cats 14229225094c done.** Plan phase 5 min: bible 1,040 words with a why (Captain
Whiskers inherited a debt and the night shift of the Sashimi Bazaar; humans are banned at feeding
hour because they say "cute" instead of buying); minimum = a crate path from two spawns to the
Fish Stall, paw cursor, three towers (Slingshot Cat, Spray Bottle Turret, Yarn Cannon), three
enemies (seagulls, armored raccoons, crabs), shop between waves; 21 stages. Build 76 min, 21/21
booted clean first try, no fix round. "SASHIMI BAZAAR": flat-vector market, the path, seagulls
walking it, placed cats firing, waves, coins, build bar with prices, menu; no console errors.
Against 816d5ac86674 (Nick's concept): the model's cats operate weapons where Nick's cats were
the towers with cat behaviours (sleepy, pounce, swipe) and the enemies were vermin; a reskin of
a TD where Nick's was a TD grown from the fiction. Served at :8956 (`cats/shot_play1.png`).

**16:26, wizardcat 72ec79d16285 plan did not parse.** Bible 964 words (Whiskerwick vs Big Hat,
"who wants to wear you"; teleport jammed because the spell words were shuffled into cards); JEV
decided side-on, turn-based, grid-based with jump and falling as core, so the minimum is a side-on
grid floor with Move / Jump / Attack cards and two enemies stepping each turn, not Slay the Spire.
The planner's JSON had a syntax slip (`Expecting ',' delimiter`, char 5347) and `stages.parse`
threw; the battery moved on. Fix: the plan call retries up to three times and saves each raw
reply (`plan-raw-N.txt`); `followup.sh` reruns `all wizardcat` after the battery.

**17:36, zombie a637487dd875 done.** Bible 1,189 words (Gulp, a candy-coloured risen zombie, is
the only hero left because the quest board still says "save the valley from the zombie menace");
JEV: first-person 3D. Minimum: one churchyard, a bonk verb, townsfolk and animals that flee,
combo and score, **no win and no loss**, and the planner wrote that into the plan as a stage
named "no failure". Build 66 min, 23/23 clean, no fix round. The game: a real three.js
churchyard (candy houses, gravestones, well, picket fence, a baker and a guard on their paths),
Gulp's enormous blocky arms over the bottom third with the help text printed across them, and a
HUD that says "NOTHING LOST · NOBODY IS OUT · KEEP GOING … THERE IS NO LIFE COUNT AND NO GAME
OVER"; twenty bonks unlock the next corner. A toy with a world. Second minimum of four without an
end (the template-ask paragraph was the first): `minimum.txt` needs "the win and the loss, on
screen" for the next iteration. Served at :8957 (`zombie/shot_play2.png`).

**17:41, alienfarm e5e39e48b7ad plan did not parse** (same JSON slip, char 7543): two of four
Flash-Next plans failed to parse on the first try. Its bible (1,094 words) and minimum landed:
JEV said cozy, no failure, no ending, so "no end" is by design here; the minimum is one crater
plot, a tend verb (plant / water / harvest), three crops with growth stages, a merchant who buys,
a pet; the ask's "weird alien" survives as names only (star-onion, violet wheat, moon-pumpkin),
not as behaviour. Battery exited; `followup.sh` runs `all wizardcat` with the retry, then
`followup2.sh` runs `all alienfarm`.

**17:47, the parse failures were truncation.** The wizardcat rerun's first plan reply also
"failed to parse"; the raw text ends mid-array with no closing fence, and the job row says
`finish_reason: length`, 20,000 completion tokens: Flash-Next at reasoning xhigh spent ~19K
tokens thinking and the plan was cut at ~1,100. My cap (`MAX_TOKENS = 20000`) against design.py's
100K. The bible and the minimum fit because they think less. Cap set to `design.MAX_TOKENS`;
reruns relaunched as `reruns.sh` (wizardcat then alienfarm). Second time the Basalt engine
outlived its runner on teardown (29 GB left on the card, killed by pid): the llama-swap hookproxy
seems to put the engine in its own process group, out of the runner's killpg. Open.

**18:04, and the orphan was mine.** tiers launches the runner with the absolute venv python, so
every `pgrep -fx 'venv/bin/python scripts/local_gpu.py …'` in my watchers never matched: the
"runner down" readings were wrong, the 17:47 `pkill` of build.py left its runner alive (SIGTERM
kills Python without `finally`), and two runners started decide on the card at 17:48:55 and both
stopped. Killed everything by pid, relaunched `reruns.sh`; wizardcat is now 3359cb575c68.

**19:30, wizardcat 3359cb575c68 done.** With the 100K cap the plan parsed first try (24
stages), so both "parse failures" were my cap. Build 79 min, 24/24 clean, no fix round. "TOWER
CLIMB": a side-on grid card-tactics game, not Slay the Spire — a pixel library floor (1 of 4),
Pip the cat, enemy books with health bars, pot hazards, a bell as the exit, a hand of three
(Feather Key / Heal, Dash, Wand-Sword) with costs, draw and discard piles, HUD with health, coins,
score, combo, floor. Coherent and its own shape, which JEV chose (turn-based, grid-based, jump and
falling as core). Defect: the page title is still "Tower Climb (stage 12)". Served at :8958
(`wizardcat/shot_play1.png`). Alienfarm 1a6ed3d9ea7a started.

**21:08, alienfarm 1a6ed3d9ea7a done.** Plan 24 stages first try. Build 93 min, 24/24 stages
clean, then the only gate fix round of the five (22 steps), 657 jobs none failed. "HOLLOW VALE":
top-down pastel valley, cottage, three soil beds with sprouts, a well, a merchant stall, a hotbar
(hoe / watering can / seed), minimap; no console errors. Defect: every HUD label renders as
glyph boxes — the pixel font never loaded, so coins, day and counters are unreadable, and the
gate cannot see it. Served at :8959 (`alienfarm/shot_play1.png`).

**Correction on the "orphaned" Basalt.** The runner logs say `[llm-qwen-flash-next] using the
server already at http://localhost:5001`: Basalt runs under Nick's llama-swap hookproxy as a
persistent service, not as the runner's child. It is supposed to outlive the runner; the two
kills by pid (14:51, 17:47) were of that service, which came back on demand. Not a bug.

| | bakery `2546d62858f8` | cats `14229225094c` | zombie `a637487dd875` | wizardcat `3359cb575c68` | alienfarm `1a6ed3d9ea7a` |
|---|---|---|---|---|---|
| JEV shape | 2D side-on, lose a life | 2D top-down TD | first-person 3D, no failure | 2D side-on, turn-based grid | 2D top-down, cozy, no failure, no ending |
| bible words | 1,008 | 1,040 | 1,189 | 1,062 | 1,058 |
| has a why | yes (Moonberry Proof) | yes (inherited debt) | yes (last hero in town) | yes (Big Hat wants to wear you) | yes |
| minimum has win + loss | yes | yes | **no** (planner wrote a "no failure" stage) | yes | no, by JEV's ruling |
| stages / fix | 24 / 0 | 21 / 0 | 23 / 0 | 24 / 0 | 24 / 1 (22 steps) |
| wall | 84 min | 76 | 66 | 79 | 93 |
| boots clean, no console errors | yes | yes | yes | yes | yes |
| screenshot read | stealth heist in a bakery; HUD drawn twice | working TD, weapons-cats reskin | world with no game | grid card-tactics, own shape | cozy plot; HUD font missing |
| Nick (2026-11-09) | a game, barely: one level, pastries on the ground, scaring has no point, die while hidden, "weird platformer" | **a game**, "an actual game from an amateur": progressive levels, 3 towers, 5 levels, no upgrades, towers unexplained, cluttered; reads as cats defending a fish market | not a game: unreadable font, click fucked-up people 20× to bonk them, gate opens, nothing changes; 40% of screen covered by player parts | not a game: no menu, dumps into play, cards unexplained, level 1 uncompletable, 4 lava pots on a grid, Quit does nothing; "undercooked by a LOT" | not a game: unreadable font; plant, water, collect plants; shop does "something" |

Every one of the five booted and plays something; four of five needed no fix round. The 2026-10-30
Flash-Next control on the bakery ask (4, loop did not close) is the only prior Flash-Next data on
these asks; the cats control is Nick's own concept (816d5ac86674). Nick plays next; bucket each
(slop / toy / thin clone / the game asked for), the floor question is "is it a playable game and
is it the thing asked for", not a 1–10.

2026-11-09, Nick played all five: first read "the only one that came out with a working game is
cats", then on detail bakery is "a game, I was too harsh" and the other three are not. Two of
five clear the floor; the full verdicts are in the table. "Boots clean, no console errors, every
stage check green" said yes on all five; the gates proved the games run, not that they are games
(the verification gap again).

What the three misses share is not the bible: zombie and alienfarm have an unreadable HUD font
(the same "font missing" the screenshots showed; a font loader that never resolves, text drawn
anyway), wizardcat has no title screen and a dead Quit, zombie has a loop the planner wrote as
"no failure" and so no end. Those are framework defects, part one of the process plan, and the
build's stage checks never ask "can a person read the HUD" or "does Quit quit". The two hits are
the two asks whose shape the model has a template for (platformer, TD); the bible gave all five
a why and none of the three misses a loop a player can see. Bakery's bible loop (scare → steal)
is on the page and absent from the game: pastries lie on the ground and scaring does nothing,
the fiction's causal loop was not carried into the minimum's one verb.

## Outcome

Two of five at the floor. Every ask got a bible with a why, every build booted clean with every
stage check green, and Nick found cats "an actual game from an amateur", bakery "a game" barely,
and zombie, wizardcat and alienfarm not games. The misses are framework defects the gates cannot
see (an HUD font that never loaded, no title screen, a dead Quit, a loop planned with no end),
and the bakery bible's own loop did not reach the game. Led to `labs/genre-first`.
Section: `docs/experiments.md` 2026-11-08, "a story bible, then the minimum that is a game".
