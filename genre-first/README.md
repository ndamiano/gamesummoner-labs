# genre-first

Status: done
Control: `labs/skeleton-first` 816d5ac86674 (cats TD from Nick's concept, the best cats build);
`labs/bible-first` 14229225094c (cats TD from a bible, "an actual game from an amateur": 3
towers, 5 levels, no upgrades, towers unexplained).

## Purpose

Nick's read of bible-first (2026-11-09), two of five at the floor: "we're sacrificing in both
places, gameplay and aesthetic, to make 'any game the user types'." Every chain to date has the
ask's theme in every stage: the design, the plan, the stage requests ("A user asked for: …"),
and the builder spends its turns on cats and fish while the towers go unexplained and
un-upgradable. The bible-first zombie bible read JEV's fifty mechanics back as prose; the bakery
minimum dropped the fiction's loop. Function and content compete at every step.

What Nick does himself: "Build me a generic Tower Defense game, where there's a path, towers,
you can upgrade towers, and a goal. Then add an aesthetic on top of it of cats defending the
fish stall." Two phases, the second never touching a rule.

## Hypothesis

Phase 1 builds the generic game of the ask's genre with no theme at all: the model names the
genre and lists what every game of it has (`genre.txt`), the plan is framework → every listed
feature, one per step → levels, both ends, balance (`plan_process.txt`), and the run's ask is
"a generic game of this genre" so no stage request carries the theme. Phase 2 is one `change`
build on the prod path: the model writes the rename/redraw/retitle note (`skin.txt`, with
JEV's look decisions only) and the builder applies it, "add no rule, remove no rule, change no
number."

Measured: Nick plays the generic game (kept in `<label>/generic/`) and the skinned one. The
floor question for the generic game is "is this a complete TD a player would recognise:
upgrades, tooltips, several towers, several levels, title → play → quit." For the skinned one:
"is it still that game, and is it now cats defending a fish market." Moves against
14229225094c if the generic game has the features that one lacked (upgrades, explanation, more
than 3 towers) and the skin keeps them.

Idea failure: the generic game is no more complete than 14229225094c (the model's genre list is
as thin as its design was), or the skin pass breaks rules while renaming (a `change` build
cannot hold the line), or the skinned game reads as "a TD with cat pictures" and not as the
thing asked for.

## Setup

One ask, `cats/ask.txt`: "a tower defense game where cats defend a fish market". Private run,
every seat `qwen-flash-next` on the local 5090. From the repo root, run.py up:

    venv/bin/python labs/genre-first/build.py all cats

or `plan`, `build`, `skin` separately. `build.py` starts and stops the GPU runner. Outputs in
`cats/`: `decisions.txt`, `genre.md`, `design.md`, `stages.json`, `plan-raw-*.txt`,
`build.json`, `generic/` (the game before the skin), `skin.md`, `skin.json`.

## Log

**2026-11-09 14:42, run `1730d01639bc`, cats, local Flash-Next.** Genre call (2.5 min): "It is
tower defense", 16 features (3–8 tower kinds × 3–5 levels, upgrade/sell, range preview,
pause/speed/restart, 10–30 waves, win/loss end screen); no word of the ask, no title screen in
the list (the plan prompt adds it). Plan parsed first try, 24 stages: framework 1–7 (path,
walker, lives, waves, tower, range, currency), features 8–19 (title, pause/speed, wave HUD,
placement preview, 3 kinds × 3 levels, select/upgrade/sell, upgrade paths, effects, health bars,
counters, end screen, quit → title), game 20–24 (14 waves, scaling, win screen, loss screen,
balance).

**15:55, generic build done: 69 min, 24/24 stages, 24 attempts (zero retries), 624 jobs, 0
failed.** Kept in `cats/generic/`, served at :8960 (`generic_title.png`, `generic_play3.png`).
Title "TOWER DEFENSE / Title Screen / one map, 14 waves"; play screen has every listed feature as
labelled grey boxes: lives 20, wave 1/14 pips, currency with +10/kill +25/wave, tower menu "3
kinds, 3 levels", tower-in-hand panel with range/dmg/rate and three level tabs with costs and
damage, pause/1x-2x-3x/restart/quit, four live counters, grey path with "Walker" squares with
100/100 bars and a speed number. HUD takes the top third. Headless: no console errors. It is a
complete generic TD; the first build on this ask with upgrades and tower stats on screen.

**15:56, skin note** (`cats/skin.md`): "FISH MARKET FELINES — The fish are moving. The cats are
not amused." 66-row table; towers Tuna Splat Tabby / Sardine Spray Calico / Anchor Paw Whiskers,
levels Paper Collar / Tin Badge / Captain's Hat, lives = Fresh Fish Crates. The table names
things the generic game does not have (armored walker, additional tower kind): a `change` build
could read those as rules to add. `change` build started 15:56.

**16:12, skin `change` build done: 16 min, 153 llm turns, 0 image jobs, 0 failed, +356 lines
in game.js.** Served at :8961 (`skin_title.png`, `skin_play.png`). Title screen: vector stall
awning, three flat cats, "FISH MARKET FELINES / The fish are moving. The cats are not amused. /
OPEN THE STALL". Every HUD label renamed per the table (Fresh Fish Crates, Market Rush 1/14,
Fish Coins +10/bop +25/shift pay, Cat Crew Shelf, Tuna Splat Tabby, Break Bell / Broom 1x /
Reset Stall), sand floor, teal path with paw prints, Back Dock. The note held: every numeric
constant in game.js is identical between `generic/` and the skinned game, no walker or tower
kind added. Shortfall: walkers are still boxes labelled "Fish Thief"; the redraw reached the HUD,
title and map, not the sprites, and neither phase called generate_media. Nick plays both.

**2026-11-09 16:30, Nick on both.** Generic: "this feels fine for a TD, it's a bit easy, but
overall it's fine." Skin: "The redraw portion was awful. I don't want to spend time on that."
Verdict on the chain: phase 1 works (a complete generic TD, zero retries, first build on this ask
with upgrades and stats on screen); phase 2 as one `change` note is an idea failure for the look,
not for the names (every rename landed, every number held).

Nick's question: would concept art help, with a generated UX? Facts found: the gate seat already
takes screenshots as `image_url`, so Flash-Next can see pictures; the builder's two ways to make
pixels are canvas code and `generate_media`, and it called the latter zero times in 777 jobs.
Nick's ruling: **the person at the ceiling writes the art direction and renders the assets; the
local model only wires them in.** "This is a test of what's possible at the current ceiling."
That is `art.py`: `art.json` (16 assets, one prompt each, one style line, by me), rendered through
prod's own `request_media` (same routing, matte and files the builder would get), then `wire.txt`
(how each asset is used, and a HUD layout: one 56 px top bar, one 96 px bottom bar, the map gets
the screen, counters move to the end screens) applied by one `change` build that may change no
number. `art` started 17:05.

**17:05–17:30, prod image path: 32 renders, 0 landed.** Every render (19 s each, Qwen-Image 2512)
came back `"safety": {"error": "classifier unavailable: No module named 'timm'"}` and the
completion handler refused and deleted it ("no safety verdict" is a refusal by policy). The
worker runs on `~/.gamesummoner/venv-gpu` under llama-swap, which has neither timm nor torch;
installing timm into the comfy env changed nothing. Same failure `labs/tier-chain` logged on
2026-11-06. Nick: not interested, generate_media is never called anyway; "just use comfy".

**17:30, `comfy_direct.py`: prod's own workflow graphs posted straight to ComfyUI** (llama-swap
upstream `comfyui_auto`), files written by hand: 16 assets in 4 min, `contact_baseline.png`.
Consistent sticker-outline style, clean mattes; `tile_path` quilt shows seams and doubled fish,
`gate_alley` kept its background. Nick: "we also don't need to use the prod workflow graphs…
what could exist", so:

**17:37, `art_ceiling.py`: Qwen-Image 2512 key art (1344×768, 30 steps) → Qwen-Image-Edit 2511
per asset with the key art as style reference** (white 1024² canvas seeds the latent, key art is
image2; worldclaw's `ImageModel` client), BiRefNet cutout, quilted tiles. 17 min, 63 s/asset,
`contact_ceiling.png`. Verdict: **lost to the baseline** for sprites: style more unified but
`cat_white` washed out (white on white, the matte ate the lines), `coin_fish` a blob,
`badge_paper` a belt, outlines too soft to read at 48 px. Won for the tiles (seamless, flat) and
the two top-down props (`gate_alley`, `dock_boat`). Reference-conditioned Edit trades punch for
conformity. **Hybrid installed** (`assets_hybrid/`): baseline sprites and title, ceiling tiles and
props. `wire` (`change` build with `wire.txt`) started 17:54.

**18:00, stopped and realigned.** Nick: "what you made is not what I want." The wire build
(`d4d105a6d4a6`, 18 turns) paused and abandoned; game snapshot `before-change` 64a5a4e intact.
His goal, in his words: "make a mock up screenshot in the beginning, and use that as the
'goal'… not to use assets… not generate_media… a way to guide the LLM. It does not matter to me
if we use generated assets from comfyui or trellis or if everything is built in code. What
matters is that we generate a reasonably user friendly game that functions… to see if using
images in our *inputs* is beneficial to the game creation process." The asset work above
(`art.py`, `comfy_direct.py`, `art_ceiling.py`, `assets*/`) answered a question he did not ask;
kept as a record of what the box can render.

Checked: Flash-Next on Basalt reads an image in a chat message (it named "FRESH FISH CRATES",
"CAT CREW SHELF", "Tuna Splat Tabby" off `skin_play.png`), so the builder can be shown a picture.

**18:05, `mockup.py`:** four mockup screenshots of the finished game, Qwen-Image 2512 at
1280×720 from `cats/mockup_prompt.txt` (the play screen, HUD and names described in prose), 2
min (`mockups/contact.png`). All four are plausible finished TDs; `mockup_0` picked (cleanest
HUD, legible path, cats on pedestals, dock) → `cats/mockup.png`.

**18:09, `image_change.py`, the arm:** generic game restored into the run (snapshot "generic
restored for the image arm"), one `change` build whose first user message is the **same
`skin.md` text the control got** plus "Here is a screenshot of what the finished game looks like;
make the game look like this" and the mockup as an `image_url` (JPEG ≤1024, patched into
`build_steps._seed`, which runs in this process for the first turn). Control = the 15:56 text-only
skin pass (:8961). Same base, same model, same kind of pass, same text; the only difference is
the picture.

**18:35, image arm done: 26 min, ~200 turns, 0 failed jobs, 0 console errors; `art.js` (910
lines) written new.** :8961 (`image_title.png`, `image_play.png`); control at :8962 from
`cats/skinned/`. The picture steered the build hard and visibly: top bar with crates / coins /
title / rush / pause 1x reset quit, bottom shelf of cat portrait buttons with prices, selected-cat
panel with range · dmg · rate and badge tiers, teal fish-scale cobble path, plank floor, water
corner with the dock, seagull thieves with sacks drawn in code with health bars. Composition,
bars, portraits and the water corner match `mockup_0`. All code-drawn, no assets.

It broke the note's rule: the mockup shows three cats, it built **four cats (40/55/90/30) and
four levels (collar/badge/hat/crown 40/65/100/150)**, added `hp`, retuned ranges (95/115/250
vs 120–230); the text-only control held every number. Also: text overlap in the selected-cat
panel, a second cluttered HUD row (the counters the control also kept). Read: an image in the
input moves look and layout a long way on the same model and budget; it also moves the model
off the rules it was told to hold. Nick plays both.

**19:44, arm 2: same mockup, short note** (`cats/image_note.md`, ~290 words: "the picture is the
whole inventory of the screen… every other counter, panel, label or line… moves into the win
and loss screens or goes away"; the names in three sentences; "keep every rule and every number
exactly as it is: three kinds, three levels…"). Arm 1 kept at `cats/image_arm1/` (:8963).

**20:15, arm 2 done: 31 min, 149 llm turns, 12 comfy jobs, 0 failed, 0 console errors.**
:8961 (`arm2_title.png`, `arm2_play.png`). Every number identical to the generic (costs,
damage, ranges, waves), three kinds, three levels. On screen exactly the mockup's inventory: one
top bar (crates, coins, title, RUSH 1 / 14, Pause 1x Restart Quit), one bottom bar (three cat
portrait buttons with prices, the selected cat's panel with level name and range · dmg · rate,
Upgrade, Sell), fence and hedge, gate, cobbled path, plank floor, water corner with dock and
rowboat. The second HUD row is gone.

**It called `generate_media` twelve times, unasked** — the first time on this run (777+ jobs
before it) and the first time I have seen Flash-Next reach for it. It wrote its own style line
("cartoon storybook style, bold dark outlines, bright warm palette, flat colour with soft
shading"), ordered three cats as actors, gull and crab thieves, a fish shot, plank / cobble /
water tiles, crate and coin icons, a rowboat; all twelve rendered, passed the classifier (the
venv-gpu `timm` install pulled torch, so renders land now) and were wired in: portraits on the
buttons and panel, sprites walking the path, tiled floor and path. It also split game.js into
game / hud / layout / screens / world / art, unasked.

Read: the picture carries where and how; the text carries what exists. Arm 1's 66-row table
told it 66 things exist and it drew them all; arm 2's "the picture is the inventory" let the
picture rule. The picture also, for the first time, made the model want art it could not draw
in code, which is the only thing that has ever made it call the art tool.

**2026-11-09 evening, Nick on arm 2:** "It looks so much better." Played it: "It works properly…
probably a bit unbalanced being a bit too easy, but it works properly." Kept at
`cats/image_arm2/`.

## Outcome

Two results, one run each, cats only. (1) A theme-free generic game of the ask's genre builds
clean on Flash-Next and is the functional floor Nick asked for: 24/24 stages, zero retries,
upgrades and stats on screen, "fine for a TD". (2) A mockup screenshot of the finished game in
the builder's input is the largest single-input improvement in look and layout measured here,
provided the text beside it is short and says the picture is the inventory; a long table beside
it clutters the screen and the rules slip, and the same table with no picture is "awful". The
picture also got the builder to use the art tool unprompted. Rendering assets by hand and having
the model wire them in was a detour from Nick's question and was stopped. Continued as
`labs/mockup-first` (the chain with nobody in it, on the bakery ghost ask). Section:
`docs/experiments.md` 2026-11-09.
