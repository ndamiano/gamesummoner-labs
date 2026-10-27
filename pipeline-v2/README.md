# pipeline-v2

Status: single-run
Control: none (Nick, 2026-10-24: no controls until some format makes at least a really solid
game). The games are the base for the vision swings in labs/vision-ux and the ones after it.

## Purpose

The night of 2026-10-23 turned up three mechanical wins:
- the stage planner (labs/stage-planner);
- B6, back-loaded stage budgets: 8 retries to 2 across seven designs;
- B7, repair first.

Playtest-refine (labs/playtest-refine) also fixed real problems the gates passed. This lab runs
them end to end on fresh asks, so the vision swings have fresh games to work on and so we see
what the stack makes.

## Hypothesis

Per ask:
1. prod design (local Flash-Next);
2. staged chain (planner, budgets 20,20,20,25,25,30,30,35,35, repair first; prod gates on a copy);
3. three playtest-refine rounds (director v3, keep-best progress judge).

Measured: whether each step completes, retries, gate rounds, the player's progress per round.
Nick plays the results. Idea failure: the stack breaks end to end, or the refined games are no
better than the staged ones by Nick's play.

## Setup

`run_ask.sh <label> "<ask>"`, queued through labs/runner (`jobs.txt`, `runner.sh`), which runs
one job at a time and takes appended jobs. Lab control plane (labs/vision-build/serve_v.py) and
local_gpu auto as for stage-planner. Logs in /var/tmp/pipeline-v2/<label>/; one row per ask in
`results.jsonl`.

## Log

**2026-10-24 10:09–12:38 EDT, farm** ("a cozy farming game on a floating island").
- **Design:** f0ba5f239694, 12,627 words; the game is "Skyfarmer".
- **Staged chain:** final 5baaf3f15dbe.
  - Stage 4's vision look caught gathering doing nothing on E; its retry was shown.
  - Stage 5 (planting) ended unclear after three tries.
  - Stage 8's look caught a dead Settings button; its retry passed.
  - Every stage 9 try failed to boot or erred; the kept best boots.
- **Gates** (copy ed92ae3ee08f): 2 error rounds and 1 play round, nothing broken.
- **Our screenshot:** isometric meadow, compass minimap, garden and satchel panels, tilled beds.
  Plain coloured circles stand in for plants, and text overlaps bottom right.
- **Served** on :8992.

Two harness bugs on the way:
- **The refine player crashed** on a chord key "click" (`Keyboard.down: Unknown key`).
  `stage_look._act_watching` now skips keys the browser does not know.
- **Refine ran on the pre-gate build.** 5baaf3f15dbe throws `resetNodes is not defined` at
  start, so its Start button does nothing, and both player sessions spent 30 turns on the
  title. The gates had fixed it in ed92ae3ee08f. `run_ask.sh` now refines the gated copy, and
  the farm refine was killed and re-run on ed92ae3ee08f as pv2-farm-g.

**12:38–14:05 EDT, farm refine on the gated copy (pv2-farm-g), three rounds:**
- **Round 0:** gathered stone and planted 2 Sunleaf.
- **Round 1** (7f29ff26e42d): could not find or stand on beds. Judged worse, dropped.
- **Round 2** (22f19e8b91ee, 56 steps): the full core loop, plant, grow, harvest into the
  satchel, forage. Judged further, kept.
- **Round 3** (db5ea5a5ff6f): ripened crops but no confirmed pick, and a new silent
  material-loss. Judged worse, dropped.
- **Final:** 22f19e8b91ee. Keep-best caught both regressions.

**14:00–15:00 EDT, farm UX polish** (pv2-farm-ux, two paired rounds on 22f19e8b91ee): no
visible change in either round. The builder sank its turns into generating a hand-lettered font
the game has no asset for, and round 2 left a `window.__game` stub in `index.html`. See
labs/vision-ux. **Farm final: 22f19e8b91ee.**

**15:00 EDT on, catdefense** ("a tower defense game where cats defend a fish market").
- **Design:** c7cc78647588, 11,075 words; the game is "Whisker Market".
- **Staged chain:** final c44a54983131; 1 retry in 9 stages.
  - Stage 5 looked shown: the market health bar drops as a Fish Thief reaches the stall.
  - Stage 6 looked shown: a placed Alley Cat draws targets and fires.
  - Stages 7 and 8 were unclear, since the looks ran out at wave 3.
  - Stage 9 was missing, then shown on its retry.
- **Gates** (copy 0bf97699dcd0): 0 / 0, nothing broken.
- **Our screenshots:**
  - level select: five named levels, Opening Day through Festival Fiasco;
  - play: a winding path from a crate to the fish stall, paw build tiles, crab thieves carrying
    fish, a HUD (MARKET 100/100, WAVE 1/3, COINS 180) and a shop (Alley Cat 50).
- **Served** on :8997.
- **Refine:**
  - **Round 0:** cleared waves 1 and 2, lost on wave 3. "Map clicks did not register as
    placements" most of the time; the pause button does nothing; no lose screen.
  - **Round 1** (31787bf9944e): placement still sporadic. Judged worse, dropped.
- **Our probe of the gated copy:** the cause of the dead clicks.
  - `js/input.js` sets `leftJustPressed` on pointerdown.
  - `renderFrame()` calls `clearFrameInput()` every render frame.
  - `shop.update` reads the flag only inside the fixed-step `step()`, which runs on frames where
    the accumulator holds a full STEP. A click on a frame with no step is cleared before any
    step sees it.
  - Intermittent at 60 Hz, and worse on fast displays. No gate can see it; the vision player
    did.

- **Round 2** (1230270af93f): placement still failing silently, and the level select now
  ignores clicks (likely the same dropped edge). Judged worse, dropped.
- **Round 3** (faedce8786c0): won Level 0 and reached Level 1 wave 2. Judged further, kept.
  Final faedce8786c0.
  - The clear-every-render-frame code is unchanged in every round, so the dropped-click bug is
    still there.
  - The win came from the round's other changes and a luckier session, not a fix.

- **UX polish** (pv2-catdefense-ux): both rounds dropped. Replay drift from the dropped clicks
  read as regressions; see labs/vision-ux. **Catdefense final: faedce8786c0, served on :8998.**

  A general law candidate for the build prompt (a lab, per prompt-lines-are-labs): input edges
  are consumed where they are cleared. Either clear them after the sim steps that read them, or
  queue them until a step consumes them.

**17:10 EDT on, skatemall** ("a skateboarding game in a haunted mall").
- **Design:** 04f519d4f02f, 16,866 words; the game is "Neon Hollow".
- **Staged chain:** final b60a38f818bc; 3 retries in 9 stages.
  - Stage 2's look caught no visible skater; its retry was shown, with a centred cyan skater.
  - Stage 3 shown: a held-Space ollie lands on platforms.
  - Stage 4 missing (no gaps, the floor continuous), then unclear on its retry.
  - Stages 5 and 6 unclear: the looker never touched a mannequin or got inside the exit door.
  - Stage 7 failed to boot, then shown on its retry: HUD and a live minimap.
  - Stage 8 missing (Settings dead), then shown on its retry: difficulty, colour-blind, reduced
    motion and keys, and Easy applies.
  - Stage 9 unclear: no win or loss reached.
- **Gates** (copy bd5ed8523fe3): 0 / 0, nothing broken.
- **Our screenshot:** a top-down neon mall, very dark and blurred, with the neon reading as
  smudges; HUD and minimap readable.
- **Served** on :8999.
- **Refine** (on bd5ed8523fe3): no round reached the exit.
  - **Round 0:** explored, lost all three lives once.
  - **Round 1** (ff2340f0be3a): circled the wrong way. Judged same, so kept.
  - **Round 2** (e67baf5c2d99): "no win trigger even when the exit marker was overlapped".
    Judged worse.
  - **Round 3** (ebbc5b2ff2d2): a navigation stall. Judged worse.
  - **Final:** ff2340f0be3a.
- **Our probe of the gated copy** (debug `__game.state()`):
  - spawn (0, 0, 0), exit (28, 0, −18), 33 m apart;
  - tank controls (A/D turn, W forward, camera behind);
  - a heading-steering script reached 17.6 m and then stuck with no movement, on screen a dark,
    blurred scene with no skater visible.

  Whether the exit can be reached at all is unproven. The level is at least very hard to
  navigate, and every player, looker and our script failed. The stage looks' "unclear" on
  stages 4, 5, 6 and 9 was hiding a game nobody could finish. Keep-best treated "unclear" as
  good enough.

- **Skatemall UX:** two rounds kept, both for the settings screen. The dark, unreadable game view
  is unchanged; see labs/vision-ux. **Skatemall final: 22bb93190cea.**

**2026-10-25 22:00 EDT on, rhythm** ("a rhythm game where you are a DJ for a ghost party"; relook
on, fast settle).
- **Stages 1 to 3:** shown. Stage 2's first try had no lane feedback; the retry added white ring
  pulses on D/F/J/K.
- **Stage 4 (hit judging): missing on the first two tries.** "A note sat exactly on the receptor
  … no Perfect/Good grade text".
- **Our probe of 414fb5c84ee2:** a script polling `__game.notes.nearest(lane)` and pressing
  through `debug.input.press` within 25 ms of the hit time scored **9 Perfect, 0 miss** in 25
  s. Judging works; the misses are false.
- **Cause:** the looker takes about 10 s per turn against ±60/±120 ms windows. It cannot hit a
  note. Any real-time timing game is a blind spot for single-input looks (and the refine player).
- **Chain** (final aecce7860391): stages 4, 7, 8 and 9 burned retries on timing false misses.
  Stage 5's game-over, stage 6's hit effects and stage 8's retry (one lucky held-key hit, score
  100, combo 1) were shown.
- **Gates** (copy f7479164677d): 0 error rounds, 1 play round.
- **Our probe of the gated copy:** `debug.input.tapAt(lane, ms)` scheduled at each approaching
  note's hit time scored **10 Perfect, 0 miss, combo 10, ×1.1 multiplier**. The game plays; the
  scoring misses were all the looker.
- **Refine stopped by hand after round 0** (00:17 EDT): the player "never scored a single hit;
  every attempt ended at the miss-cap game-over".
  - The keep-best judge ranks builds by player progress, so the only builds it could prefer are
    ones that stop being timing games (windows wide enough for 10 s turns).
  - Killed before any change build started. UX ran on the gated copy f7479164677d.
- **Options:**
  - teleport mode letting the looker call the game's own timing aid (`debug.input.tapAt` exists
    here);
  - a look action that runs a short scripted input sequence keyed to the debug state.

**2026-10-26 00:36–03:55 EDT, dungeon** ("a zelda-like dungeon crawler starring a frog knight";
relook on, fast settle).
- **Design:** 6dd8f6ab6921, 10,872 words.
- **Staged chain:** final 5aae8fff6e11.
  - Stages 1 to 5 shown first time: the toon Lily Courtyard, WASD and camera, jump with air
    control, a hearts HUD with respawn, fly slimes and charging beetles.
  - Stage 6 (combat) missing: the attacks did not land.
  - Stage 7: broken, then missing (blocked by pillars in room 2), then broken.
  - Stage 8: the Toad Emperor found but not felled.
  - Stage 9: title, HUD, pause and settings added on the retries; the end screens out of reach.
- **Refine:**
  - round 0 never left room 1 ("fighting the camera and drowning");
  - **round 1** (4f9345ab2787) cleared room 1 and entered room 2: kept;
  - rounds 2 and 3 regressed to room 1 and were dropped.
- **UX polish:** two rounds kept (c105c9dcfb9a): a larger title, unclipped settings. The judge
  noted the costs: an oversized portal effect, a low-contrast health HUD, and room and controls
  guidance removed.
- **Both 4f9345ab2787 (pre-UX) and c105c9dcfb9a are in the grading list,** to test whether UX
  polish helps or hurts.

**2026-10-26 03:52–06:45 EDT, turtlecity** ("a city builder on the back of a giant sea turtle").
- **Design:** f1c38fce8e91, 13,376 words.
- **Chain:** final 1a230625183b.
  - Stages 1 to 3 shown: an 11×11 pastel shell board, the glove cursor, resource bars with
    caps.
  - Stage 4 (build and place): missing (no Build menu), then missing (placement clicks filtered
    as UI; see below), then shown.
  - Stages 5 and 6 shown: gathering spots grow and fill; a click harvests "+1 Algae".
  - Stage 7 missing ×3: no growth-post piece, and Storage Room gated on pearls never gathered.
  - Stage 8 shown: pick up, drag, drop.
  - Stage 9: dead Settings, then shown.
- **Gates** (copy 287bd67059f5): 0 / 0.
- **Refine:** round 0 learned the loop and stalled at 0 algae (an economy dead end). Rounds 1
  to 3 each regressed (a dead Algae card, no committed action, fewer spots) and were dropped.
  The refine result is the gated copy.
- **UX:** round 1 "same", with no visible change despite edits to main/scene/screens.
  **Round 2** (806b477ffbf9) kept: a closable, complete Settings, and the Build panel off the
  board; a "more settings below" hint now overlaps a row.
- Both the pre-UX build and 806b477ffbf9 are in the grading list.

**2026-10-26 06:34–09:08 EDT, timeloop** ("a puzzle platformer about a time loop in a clock
tower"): "THE 11:59 LOOP".
- **Premise:** the ledges are shown once at the start of each loop, then stay solid but
  invisible.
- **Design:** 8d6e474f972d, 9,932 words.
- **Chain:** final cb275fb57f3c.
  - Stages 1 to 3 shown: the Windup Yard room, walk with wall stops, variable jump height.
  - Stage 4 missing ×3: the ledges flashed and vanished, but the looker fell through them, a
    real collision gap or a memory challenge it failed.
  - Stage 5 missing ×3: never reached a working exit arch.
  - Stage 6 shown: "LOOP BROKEN — THE TOWER WINDS BACK TO THE START", and Retry resets.
  - Stage 7 missing ×3: one input every ~10 s cannot make the jumps to the high exit, a
    platforming blind spot like rhythm's timing.
  - Stage 8: broken, then missing (P pauses, no menu), then shown (pause, settings, difficulty,
    accessibility).
  - Stage 9: broken ×2, then shown (title, HUD timer, game over).
- **Gates** (copy 5f691020d0fa): 0 / 0.
- **Refine:**
  - round 0 reached the right platform and the wall below the exit, falling into the pink hazard;
  - rounds 1 to 3 were judged worse on sessions that ended after 1 to 3 turns (a harness defect,
    fixed 10:00; see labs/vision-build).
  - Result: the gated copy.
- **UX:** two rounds kept (411a86a2d054): real key bindings and volume controls in a readable
  settings screen, clearer health, a cyan "usable" ledge. Faint world outlines now show behind
  the pause menu.
- Both builds are in the grading list.

**2026-10-26 15:28–18:06 EDT, penguin3** ("A game about a penguin climbing a pyramid", the
weekend's hardest ask): "Penguin Pyramid Dash". The best penguin of the weekend.
- **Design:** b7e616b2afda, 11,654 words.
- **Chain:** final c1fdac922e26.
  - Stages 1 to 5 shown first time: the cold flat-vector L1, movement and gravity, variable
    jump, grip-wall climb and wall jump, a pit reset with a burst.
  - Stage 6 missing ×3 on the looker's jump precision (the objective fish on a high platform).
  - Stage 7: missing ×3. Attempt 1 showed L1 complete with L2 unlocked and playable; L3 out of
    reach.
  - Stages 8 and 9 shown: HUD and pause hint; the "L1 COMPLETE" card with Continue to L2.
- **Gates** (copy 89d175c253dc): 0 / 0. A clean three-level select with fish counts, par times
  and locks.
- **Refine on the gated copy:**
  - round 0: L1 fish collected, stuck at the exit pillar;
  - **round 1** (20c5abc51075): L1 complete, climbing L2's summit. Kept.
  - round 2: a climb-control regression. Dropped.
  - **round 3** (e5a661b16f28): **L1 and L2 completed, L3 started**. Kept. The player's own
    frame shows "L2 COMPLETE · fish 1/1 · 1:23 / par 1:30 · 0 deaths · L3 Falling Ice
    unlocked".
- **Served** on :9019.

**2026-10-26 18:24–21:15 EDT, farm3** (a repeat of "a cozy farming game on a floating island"):
"Sky Garden Caretaker". The cleanest staged chain of the weekend.
- **Design:** c1dad551e950, 11,453 words.
- **Chain:** final d5fed94d6dbf.
  - Stages 1 to 7 and 9 shown first time: the Hollowroot meadow, walking and cloud-edge bounce,
    the satchel (Tab, Q drops), gathering with 5-use counters, build mode and planting, four
    growth stages, hops over water gaps, the title and HUD.
  - Stage 8 missing ×3: pause works; the dusk→night shift sits ~537 s away, beyond any look.
- **Gates** (copy 3f28dc497d54): 1 error round, 0 play rounds.
- **Refine:** round 0 collected 50 crops (past the 30 goal) but never found the Sky Market
  delivery. Rounds 1 to 3 each broke interaction and were dropped. The refine result is the
  gated copy.
- **UX:** two rounds kept (33cb8b33fc46): settings unclipped into two columns, and the minimap
  and map rendering the island instead of blank boxes. Still faint.
- Both builds are in the grading list.

**2026-10-26 21:09–23:46 EDT, catdefense3** (a repeat of "a tower defense game where cats defend a
fish market").
- **Design:** 4257407d866e, 13,702 words.
- **Chain:** final 75793e39fb6f.
  - Stages 1 to 7 shown first time: the board, placement mode with a ghost and range ring
    (−40), placement, gull snatchers walking the path, waves 1/3→3/3, cats auto-firing, the
    "Market Flopped! Restarting…" loss.
  - Stage 8 missing ×3: a deep L2 unlock. The last try cleared L1 and saw "2 of 5 markets open".
  - Stage 9: dead pause, then shown.
  - No dropped clicks this time.
- **Gates** (copy c3631de7dbc2): 0 error rounds, 1 play round.
- **Refine:**
  - round 0 cleared market 1 and was midway through market 2 wave 1;
  - rounds 1 and 2 were dropped (palette and HUD confusion; a 3-column level select that sent
    the player back to L1);
  - round 3 "same" was kept (0861810a6846).
- **UX:** two rounds kept (9fdb9b39f73b):
  - the Settings Back button unclipped;
  - debug labels and level IDs removed;
  - placement affordances (gold grid, range circle, HELD badge, greyed unaffordable cats);
  - compact settings.
- Both builds are in the grading list.

**2026-10-26 23:46 – 10-27 03:50 EDT, gta6b ("make gta6").**
- **Design:** c6a6b17831ac, 18,039 words, the largest of the weekend.
- **Chain:** final 449cfa6cd080.
  - Stages 1 and 2 shown: a sunset dockside with a lighthouse; WASD, orbit camera, jump.
  - Stage 3 missing ×3: a cone hazard did damage (100→80) but death and respawn never fired.
  - Stage 4 missing ×3: the Odessa Pike quest marker and E prompt present, the talk dead.
  - Stage 5 missing ×3: the streetbike appeared on the last try; E to enter dead.
  - Stage 6: a thug killed (100→0, the first enemy death in any gta6), no reward; then broken
    ×2.
  - Stages 7 to 9 broken or missing: M1 blocked, the boss out of reach, no Game Over, then
    Settings dead.
- **Gates** (copy bc3088e3198e): 0 / 0.
- **Our screenshot:** a striking red-gold sunset harbour, Mara, the full HUD (score, SolCoins,
  hearts, health, Dusk Pistol ammo), a minimap with the M1 marker.
- **Refine:**
  - round 0 stuck at M1 and died to the hostile;
  - round 1 was dropped;
  - **round 2** (8086412d643d) **completed the M1 dialogue**, the first working NPC talk in any
    gta6 this weekend: kept;
  - round 3 got the dialogue, a streetbike handed over, then stuck on "Follow Odessa", with
    camera and darkness regressions: dropped.
- **UX:** round 1 worse, round 2 same. Nothing kept; the final is 8086412d643d.

**Refine across the pipeline asks:**
- **helped:** penguin3 (L2 cleared), dungeon (room 2), farm (the core loop);
- **dropped every round:** turtlecity, timeloop, farm3, where change builds broke basic
  interaction;
- **stopped by hand:** rhythm.

**Dropped clicks, a recurring generated-code defect (three games so far):**
- **catdefense pv2:** an edge flag (`leftJustPressed`) was cleared every render frame but read
  only in the fixed-step update.
- **turtlecity stage 4, attempt 1** (b1f41bcef2bf): `input.js` added `overUi(e)`, which skips
  any pointerdown whose target sits inside `[data-ui]`. Board clicks were classed as UI and the
  ghost never placed. Attempt 2 removed the check and was shown.
- **rl-cat stages 8 and 9:** "PICK A TARGET" swallowed tile clicks; cause not probed.

- **gta6b (1a9e8965f7e1), likely the root of gta6's never-working E prompts** (dialogue, spawn
  set, bike, in every gta6 build this weekend):
  - `engine/input.js` `sample()` runs at the top of each fixed step and falls back to
    `rawJustPressed(code)` for taps between steps;
  - but `rawTick()`, which clears those raw flags, runs in `frame()` once per render frame
    after the steps;
  - so a render frame with no fixed step clears the tap unseen.

  The code's own comment says "this is why a short E press used to do nothing". The builder
  patched the symptom and left the clear in the wrong place. A looker's E is a short tap, so
  it is dropped. Same class as catdefense's `leftJustPressed`.
  - **Correction (03:20 EDT):** gta6b refine round 2 (8086412d643d) completed the M1 dialogue
    with `engine/input.js` unchanged. The frame-cleared tap is real in the code, but it was not
    what blocked talking here; the fix landed elsewhere (offers or range). Root cause
    unconfirmed.

Both causes have the same shape: the press reaches the game but is consumed or filtered before
the system that should act on it. A general build-prompt law candidate (a lab): consume an
input edge where it is read, and test any "over UI" filter against a click on the play area.

From catdefense on, `run_ask.sh` adds step 4: two paired vision-ux rounds (labs/vision-ux,
`UX_PAIRED=1`, `UX_LOOK=auto`) on the refined game. The farm gets the same as its own job.

## Outcome
