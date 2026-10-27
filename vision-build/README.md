# vision-build

Status: single-run
Control: labs/stage-planner b6-penguin (12e6e6388be4, gated copy be961707c1d3). Same design
(f254f7d986a9), same plan (sp-penguin's, copied), same budgets 20,20,20,25,25,30,30,35,35; the
only change is the picture. Also sp-penguin (eedc7205ebd3), whose camera started inside a stone
step.

## Purpose

The builder is blind. `play(js)` runs the page headless and returns only what the script returns,
plus page errors and the console. Every visual defect the builder made, it could not see:
- dsA25 stage 4's dead `requestAnimationFrame` loop: the game ran one frame and the builder,
  stepping it through the debug API, never knew;
- the staged penguin's camera behind a stone step, with Pip never on screen (labs/playtest-refine
  needed a raycast to find it);
- the B6 penguin's Pip clipped at the bottom edge;
- every art and layout choice in the vision-ux review: grey text on yellow, overlaps, a stray
  box.

Nick (2026-10-24): big swings with vision in the pipeline.

## Hypothesis

After every `play()`, the builder sees a 640x360 picture of the page as its script left it,
added to the conversation as the next user message ("The page as it looked when your last
play() ended:"). One picture at a time; earlier ones become a one-line placeholder. Seeing what
it made, the builder catches visual breakage while building: a missing character, a camera in a
wall, unreadable text.

Measured, against b6-penguin:
- retries;
- gate rounds;
- our camera probe and screenshot after Enter, Enter;
- the playtest player's first observations on both games (labs/playtest-refine `session`);
- how often the builder's next program reacts to what the picture shows;
- token cost: an image is a few hundred prompt tokens (tested, 639 for a short conversation with
  one), but the harness's size estimate counts its base64 (~35K chars), so compaction may fire
  earlier.

Idea failure: the builder ignores the pictures, or the games are no better on these measures and
in Nick's play.

## Setup

- `look_play.py`: `maestro.codegen.play.run` plus a final screenshot, downscaled with Pillow.
- `look.py`: for a stage whose stage.json has `"look"`, swaps the build's `play` tool for one
  that runs look_play, and wraps `build_steps._apply` (outermost, after `stage.install()`) to add
  the picture after the tool result and retire the previous one.
- `serve_v.py`: the lab control plane with look installed. `run_stage_v.sh` is the stage runner
  with look installed.
- `swap_serve.sh` swaps the running control plane over between jobs.
- `chain.py` (labs/stage-planner) uses `run_stage_v.sh` when `--opts` has `"look": true`.

Tested: look_play's picture of the refined cat game (26 KB JPEG), and a tool-calling
conversation with the picture as a user message, which the local Flash-Next read and answered
("Let me look at the screenshot carefully…").

**V3, a look per stage** (added 2026-10-24, same lab, same control):
- **The look:** after a stage boots clean, `stage_look.py` gives a vision player 10 turns to
  reach and see what the stage's done line promises, then a verdict: shown, missing or unclear
  (`prompts/stage_look_*.txt`).
- **On "missing":** the stage counts as failed and is retried. The retry's request opens with
  the looker's report ("In an earlier try at this stage, a player who went looking for what it
  should show reported: …"). This is `seen_missing` in stage.json, read by `run_stage_v.sh`.
- **Keep-best:** the rule now ranks an attempt by boots, then fewest errors, then not missing.
- **Switch:** `chain.py --opts '{"vision_check": true}'`.
- **Smoke test** on the refined cat with a made-up done line: it moved the cat and reported the
  counter it was told to watch did not drop. Precise. A literal reading of a done line can cost a
  false retry.

Queued in labs/runner, on the penguin with sp-penguin's plan and B6 budgets:
- v2-look-penguin (pictures);
- v3-check-penguin (looks);
- v23-penguin (both).

## Log

**2026-10-24 05:36 EDT, v2-look-penguin stage 1 (ae7109fed36a), first look: the builder uses
the pictures.** The pictures arrive: 5 JPEGs in `looks/`, each followed by "The page as it looked
when your last play() ended" in turns.jsonl. From its reasoning:
- **Turn 13:** "There's no screenshot tool, but I can check state… read pixel data from the
  canvas".
- **Turn 14:** "The screenshot shows only the sky-horizon background color… no 3D content
  visible… WebGL context was lost". It went after the context loss.
- **Turn 18:** "Now it renders: a stepped sand pyramid with the sun-shaped exit at the summit… the
  final screenshot shows the full level. Observations from the image: the sand looks quite
  dark/saturated orange".

A blank 3D scene, found and fixed inside the stage, and then a critique of its own art. A blind
builder ships the blank scene unless our boot check or the gates happen to catch it.

**2026-10-24 05:36–06:19 EDT, v2-look-penguin done: same mechanics as the blind control, a
visibly better game.**
- **Chain:** 9 stage runs, 0 retries, 240 turns, 40 min. The control b6-penguin had 0 retries,
  240 turns, 45 min.
- **First writes come later:** 4, 4, 4, 3, 11, 12, 12, 15, 11, against 3, 4, 3, 2, 8, 11, 7, 8, 9.
  Turns go to looking.
- **Gates** (copy 941bb9ae819e): 0 / 0, nothing broken, the same as the control.
- **Our screenshots:**
  - title: a "Penguin Climb" card over the live level;
  - play, after Enter, Enter: the whole stepped pyramid in frame with the sun exit at the top,
    two grip-dot panels, side walls, sand ground, and Pip in view at the bottom centre, half
    behind the near ledge.
- **The control at the same point:** a low camera against the first step, the pyramid as flat
  bands, and Pip's head clipped at the bottom edge.

Read: what the gates and retries cannot tell apart, the pictures can. Served on
http://127.0.0.1:8960 for Nick; control on :8959.

**2026-10-24 06:19 EDT on, v3-check-penguin (V3).**
- **Stage 1:** shown. It saw the stepped pyramid and the glowing exit, static under every input.
- **Stage 2:** the first attempt did not boot. The retry's look was unclear: WASD moves, but it
  never saw Pip climb the ramp.
- **Stage 3** (jump):
  - attempt 0 missing: "pressed/held the documented jump key many times, yet Pip never left the
    ground". It boots clean, so only the look catches this.
  - attempt 1, with that report in its request: the jump fires now, but still called missing,
    for no squash deformation and no dust on landing.

The verdict was too strict: polish in a done line was costing retries. From the next look on
(stage 3 attempt 2), `stage_look_verdict.txt` says "missing" is for the main thing only, and an
absent smaller touch is "shown" with a note.

The rest of the chain, up to 07:44:
- **Stage 3, attempt 2:** shown. "Pressing Space reliably made Pip jump and each takeoff/landing
  spawned visible dust puffs"; only the squash, which stills cannot catch, went unseen.
- **Stage 4** (climb on C):
  - missing twice: holding C at the panel never attached Pip;
  - unclear on attempt 2: the panel sits behind a ledge and the looker never got adjacent.

  The code grabs only within 0.6 m (`GRAB_RANGE`, from the design), and the looker steers from
  screenshots. The playtest player failed the same climb on the earlier penguin.
- **Stage 5** (fall, fail, restart):
  - missing: the "SPLAT!" fail banner appears but the level never restarts, across eight
    different inputs;
  - the retry was unclear: it never found the gully.

  Keep-best took the unclear one over the confirmed bug. "Unclear" outranks "missing" even when
  the missing attempt only lacks the last step.
- **Stages 6–7:** unclear. The looker could not climb, so it never reached what these stages
  built.
- **Stage 8** (levers and door): missing ("the counter stayed at 0… no linked door"), then
  unclear for the same climb.
- **Stage 9:** unclear. Title, level select and pause are fine, the deeper screens unreached.
- **Totals:** 16 stage runs, 7 retries (1 boot, 6 from looks), 410 turns, 69 min. The control
  b6-penguin had 0 retries, 240 turns and 45 min.
- **Gates** (copy 5b86198503f9): 0 / 0, nothing broken. The play gate called the shell "a real,
  finished game shell rather than a stub".

Read: the look catches real defects that boot clean (a dead jump, a missing restart, dead levers,
a climb that never attaches), and its reports fixed the jump within two retries. But one core
mechanic left broken (the climb, stage 4) blinds every look after it, and with retries capped
the chain moves on anyway. Two changes worth a try:
- a core mechanic's "missing" should block the chain, or carry into the next stages' requests as
  a repair, the way B7 carries a boot error;
- keep-best should not prefer "unclear" over a "missing" whose report is specific.

Cost: +170 turns and +24 min.

**08:20 EDT, the looks were blind to anything quick: a harness flaw, fixed.** v23-penguin
stage 3 called the jump missing on all three attempts. I checked directly on 5295e3cf94b7 with
Playwright and the debug API: Space lifts Pip to y 1.74 with state "jump" and the squash timer
running. The jump works.

The look acted the way the play gate does: a 0.2 s tap, then 1.5 s settle, then the screenshot.
A jump is over in ~0.8 s, so every frame showed Pip back on the ground. The looker also could not
hold two keys at once, and the climb wants C held with W.

So V3's earlier "missing" on the jump (v3-check-penguin stage 3, attempts 0–1) was false. Its
stage 4 climb verdicts are suspect, and so is every "missing" the old v23 run carried forward.

Fix, in `stage_look.py`:
- each action returns a strip of three frames: during the action, ~0.25 s after, and settled;
- a new `chord` action holds up to three keys together.

The same build now gets "Every Space press made Pip jump into the air, with a tan dust puff…
the body visibly squashing". The v23 run (#7) was stopped and its build paused (65f8c2731b03), and
it is re-queued as v23b-penguin with the fixed looker.

The playtest player (labs/playtest-refine `refine.session`) had the same blind spot, and that is
the likeliest reason no penguin loop ever climbed. It uses the strip and chords from now on.

**2026-10-24 08:43–09:43 EDT, v23b-penguin: pictures, looks with the fixed looker, and the carry.
The best penguin of the weekend.** Same design, plan and budgets as b6-penguin.
- **Stage looks:**
  - 1 shown;
  - 2 shown;
  - 3 shown, first try ("clearly airborne in the middle frames… squashed and stretched…
    dust");
  - 4 unclear (10 turns spent walking to the panels);
  - 5 unclear (never found an edge to fall from);
  - 6 shown: the looker reached the exit, "SUMMIT! Level 1 Dune Steps complete… Reach the exit
    +1000";
  - 7 shown: "Unlocked: Level 2 Switch Steps!", then climbed Switch Steps to its summit;
  - 8 shown: held E at a lever, the handle flipped, score 0 → 100;
  - 9 missing: the win overlay's Next / Level select / Title buttons ignored every input. Its
    one retry was shown, through title, level select, pause and settings.
- **Chain:** 10 stage runs, 1 retry, 275 turns, 43 min. The control b6-penguin had 0 retries,
  240 turns and 45 min.
- **Gates** (copy 3f1e39700084): 0 / 1 round, nothing broken.
- **Our screenshots:**
  - title: "PIP'S PYRAMID, Five pyramid levels to climb", a Level 1 Dune Steps badge, and a
    "How to waddle" card naming every control (hold C to climb, hold E for levers);
  - play: Pip on the central ramp of the pyramid with dotted grip panels, the score, and the
    control card still on screen.
- Served on http://127.0.0.1:8991.

Read: on the same plan, every earlier penguin (sp-, b6-, v2-, v3-; nine refine rounds) never
had a session climb. This build had a looker climb two levels and pull a lever inside the stage
checks, and it shows its controls. Both vision swings are on, plus the fixed looker; which
carried most needs the separate runs again with the fixed looker. The stage looks need more
than 10 turns for later stages, and TURNS is 16 from the next run.

**07:45 EDT, carry the miss forward, and v23-penguin restarted.**
- **The change:** when a stage's attempts include a "missing" and the kept one is not "shown",
  the next stage's first attempt opens with "A player who looked at the game after the last
  stage found this still not working: <report>. Fix that first, then build this stage."
  (`carry_missing` in stage.json, chain.py and run_stage_v.sh.)
- **The restart:** the first v23 start (#6) was stopped at its first stage and its build paused
  (e05457691df1). run_stage_v.sh had been edited while that stage's bash was reading it, so its
  next lines would have been read from shifted offsets.
- **What this run tests:** the rerun (#7) has pictures, looks and the carried miss. It is V2 + V3
  + carry, not V2 + V3 alone.

**2026-10-24 19:57–21:12 EDT, battery leg 1, v23-carts (V2+V3 on carts): a clear loss to the
blind B6.**
- **Setup:** same plan and budgets as b6-backload-carts (copy be8fe3cdb7a3).
- **Chain:** 11 stage runs, 2 retries, 290 turns, 54 min, against B6's 1 retry, 260 turns and
  40 min.
- **Stage looks:**
  - 1, 2 and 7 shown;
  - stage 4 (push a crate onto the plate): missing, then missing, then unclear on the last try,
    where the cart sat wedged against a shelf. Keep-best took the unclear one.
  - stages 3, 5, 6, 8 and 9 unclear.
- **Gates** (copy 988fca82a0c3): 0 / 0, nothing broken.
- **Our probe:**
  - B6: Enter, Enter, Enter starts the level. A polished toy-grocery diorama, the googly-eyed
    cart, a full HUD (score, keycards, coupons, exit gate, clock), and W drives.
  - v23: the same keys land on a "LOAD A LEVEL" panel with a "BACK TO TITLE" box laid over the
    level list. The level cannot start, as the stage 9 looker reported. W changes nothing.
  - The v23 debug API has 6 members against B6's ~100.
- **Served:** B6 on :9002, v23 on :9003.

Read: on carts the vision stack lost. The looks found real defects (the crate push) but the
retries did not fix them. Keep-best then chose an unclear but worse build, and the later stages
built on that. The vision loop is only as good as its ranking: "unclear" must not beat a
specific miss, which the relook bet (queued) addresses. The penguin win and the carts loss
together say the stack helps when misses get fixed and hurts when they get papered over.

**21:12–22:13 EDT, battery leg 2, v23-cat: close to even with the blind B6.**
- **Chain:** 11 stage runs, 2 retries, 299 turns, 46 min, against b6-cat's 0 retries, 240 turns
  and 34 min.
- **Stage looks:**
  - 1 to 3 shown (board, WASD moves, the card hand spends PAW);
  - 4 missing (combat dealt no damage), then unclear on the retry, where Zap now targets and
    damages;
  - 5 to 8 unclear (the looks never cleared level 1);
  - 9 failed to boot, then unclear on its retry, with title, pause and settings confirmed.
- **Gates** (copy 85990ab2a717): 0 / 0, nothing broken.
- **Our screenshots after Enter ×3 and d**, against b6-cat (gated copy d1973b3a36b2):
  - both play;
  - v23 has bigger sprites and a closer camera, "OBJECTIVE: REACH THE EXIT / ENEMIES 2 – THEY
    CHASE AND BITE", and a smaller hand clear of the board, but its title overlaps the HUD;
  - B6 shows the whole level, with the hand over it.
- **Served:** B6 on :9004, v23 on :9005. Nick's play decides.

**22:13–23:51 EDT, battery leg 3, v23-gta6: a loss to the staged blind build.**
- **Chain:** 5 retries in 9 stages.
- **Stage looks:**
  - 1 failed to boot, then shown on its retry: the golden-hour street grid.
  - 2 shown: walk, Shift-run, the over-the-shoulder camera.
  - 3 unclear: a flat world, no ledge, no life counter.
  - 4 missing twice (F fired a pose but no ammo was spent), then shown on the third try: ammo
    12→0, reload, combo on hit. The fire bug the one-conversation control 8955 shipped with was
    caught and fixed.
  - 5 missing, then failed to boot, then missing: enemies chase and damage, shots register, but
    no enemy dies.
  - 6 failed to boot, then missing (E TALK opens no dialogue), then unclear: the player is
    trapped in an instant-death loop. Keep-best took the unclear one.
  - 7 and 8 unclear: a constant health drain at the spawn ends every run in GAME OVER.
  - 9 shown: title, difficulty, game over.
- **Gates** (copy 7deaf6a5c1b3): 0 error rounds, 1 play round, nothing broken.
- **Our screenshots after Enter, Enter and W**, against sp's staged gta6 (:8954):
  - sp: a clean golden-hour city, Rico in view, HUD at health 100;
  - v23: health already 50/100 from the drain, a dimmed "SHAPES:" legend box over the view, a
    faded HUD.
- **Served** on :9006.

**Battery read, after three legs plus v23b-penguin:**
- penguin: a vision win;
- cat: even;
- carts: a loss;
- gta6: a loss.

The looks find real defects every time: a dead crate push, no damage, no fire, no kill, a dead
talk prompt, a missing skater, dead Settings buttons. Retries fix some of them (fire, Settings,
skater, the penguin's win menu). The losses come from the ranking: an attempt that left the game
worse but confused the looker ("unclear") beat a specific miss, and every later stage built on
it. gta6's stage 6 and carts' stage 4 are the cases. The relook bet (running now on skatemall)
is the direct test.

**2026-10-24 23:51 – 10-25 01:24 EDT, rl-skatemall: relook's first run. Every stage resolved and
the game can be won.** Same design (04f519d4f02f), plan and budgets as pv2-skatemall.
- **Chain:** 14 stage runs, 5 retries, 350 turns, 55 min, against pv2's 4 retries, 350 turns and
  59 min.
- **Relook fired 3 times:** two second looks resolved, and one stayed unclear and became missing
  (stage 4).
- **Stage looks:**
  - 1 missing (no exit door), then shown.
  - 2 shown.
  - 3 missing twice (a tap gives only a small hop), then shown: a held Space ollies onto a
    platform.
  - 4 missing three times: walking off into the void lands on an unseen floor with no damage.
    The kill plane is never fixed; the builder could not reach the cause from the account.
  - 5 shown: enemy contact −12 HP with a cooldown.
  - 6 shown: "EXIT REACHED… L1 – Food Court Atrium cleared", reached twice.
  - 7 to 9 shown: HUD and minimap; pause and settings; title, level select, pause and win.
- **Against pv2:** five unclear stages, and an exit no player, looker or our steering script
  ever reached.
- **Gates** (copy 1fe79e407cbe): 0 / 0, nothing broken.
- **Our screenshot after Enter, Enter and W:** crisp neon, the skater visible, the EXIT sign
  and arrow ahead, a minimap. pv2's was a dark blur.
- **Served** on :9007.

Read: one run against one run, and the plans match but the build is stochastic, so part of
this is run-to-run variance. Still, the shape is what relook was for: no stage was left
"unclear", and the final can be won. The remaining miss is the diagnosis gap, not the looker.
rl-gta6 and rl-carts (running) test relook on the two battery losses.

**2026-10-25 02:30 EDT, `trace` built: the diagnosis-gap bet.** A chain.py opt, off by default.
- Each look action records how `window.__game`'s state (`state()` or `getState()`) changed:
  scalar leaves, with time, frame and log noise dropped.
- A missing verdict carries the last 10 (input, change) pairs to the retry as `seen_trace`.
  `run_stage_vt.sh` puts them in the request and asks the builder to replay them with play()
  and read the state before changing code.
- Smoke look on catdefense faedce8786c0 (4 turns):
  - turn 1: click on Start, `ctx.state: "title" -> "level_select"`;
  - turns 2 to 4: clicks on the Level 0 card, "nothing in window.__game's state changed".

  That pins the dropped-click bug the refine builder never found.
- Queued after rl-carts with relook:
  - tr-catdefense (design c7cc78647588, pv2's plan): the dropped clicks;
  - tr-skatemall (04f519d4f02f): the kill plane, which three precise reports never got fixed.

**2026-10-25 03:00–04:00 EDT, settle audit (Nick: "how valuable is the settling time?").**
- Every look, refine and UX action waited a fixed 1.5 s before its screenshot:
  - ~330 look actions per staged game, ~8 min;
  - refine ~6 min per ask;
  - prod `play_gate.py` ~15–30 s per gate run.
- The GPU idles through all of it: 20–32% of each run's wall time is idle gaps between LLM jobs,
  mostly 2–10 s each.
- `settle_probe.py` replayed the first 20 inputs of each recorded refine session (12 builds,
  186 actions) in a CPU-only browser. After each input it measured when the frame stopped
  changing (160×90 grey mean difference < 1.0 between 100 ms polls) and how far that frame
  was from the 1.5 s frame.
  - Debug-state stillness is useless as a signal: enemy positions and item ages tick forever,
    even with an ambient baseline.
  - Frame-only results:

    | Game | Median stop | p90 | Mean wait |
    |---|---|---|---|
    | Catdefense | 214 ms | 245 ms | 233 ms |
    | Skatemall | 440 ms | 662 ms | 440 ms |
    | Farm (constant shimmer) | never stops | — | 1.5 s cap |

  - The largest gap from the stopped frame to the 1.5 s frame was 1.56/255, invisible.
- **Built:** `stage_look.settle()` with `LAB_SETTLE=fast`: a 200 ms floor, running on to 600 ms
  only while the frame is still changing.
  - Used by watched actions (just-after frame at 100 ms), the refine player (through
    `_act_watching`) and ux.py's tour and replay.
  - A watched click went from ~2.0 s to 0.75 s.
  - Default off, so the relook and trace battery keep 1.5 s and stay comparable.
  - On for the 8 queued pipeline asks.
- Prod `play_gate.py` is unchanged and needs Nick's signoff.

**04:30 EDT, `teleport` built.** A chain.py opt.
- The look prompt (`stage_look_turn_teleport.txt`) lists `window.__game`'s functions and allows
  `{"debug": {"call", "args"}}` to travel or set the game up. The promise must still be judged
  on screen.
- Why: relook turns a deep stage the looker cannot reach into a false missing. rl-gta6 stage 8:
  the boss sat behind locked waypoints and the whole look went on the opening objective.
- Smoke on v23-gta6's copy (boss stage, 6 turns, with trace):
  - the debug call ran, but that build's API has no travel function (only `sample`), so the
    look stayed unclear;
  - the trace alone surfaced the spawn health drain: `player.health 0 -> 100, lives 0 -> 3` on
    a restart.
- Queued as tl-carts (relook + teleport). Carts' designs carry `warp`, `startLevel`, `setTime`,
  `expireTimer` and `winLevel`, so the stage 5, 6, 8 and 9 content the v23 looks never reached
  becomes reachable.

**2026-10-25 01:24–04:18 EDT, rl-gta6 (relook on the gta6 loss): no rescue, and the most
expensive run yet.**
- **Chain:** 23 stage runs, 14 retries, 640 turns, 174 min, against v23-gta6's 5 retries and
  99 min. Relook fired 6 times.
- **No stage after 2 resolved:**
  - 3 (falling): missing ×3; no ledge anywhere.
  - 4: broken ×3.
  - 5 (enemies): missing ×3; enemies chase and damage but never die.
  - 6 (quest giver): missing ×3; E/F never open a dialogue. With v23 that is five precise
    reports, never fixed.
  - 7 and 8: broken or missing. Stage 8's relook turned "the boss is behind locked waypoints"
    into a missing.
  - 9: missing ×2 and broken.
- **The kept final** (copy ed28dc0e1259, gates 0 / 0) is stage 9's last attempt, where "holding
  W produced no perceptible movement".
- **Two lessons:**
  - When every attempt misses, keep-best falls back to the latest, which here was the worst.
    It should prefer the attempt with the narrowest miss, or the earlier stage's state.
  - Relook cannot help when the builder cannot fix what the looker names. gta6 is the
    diagnosis gap at its worst; tr-gta6 (queued) is its test.

**04:18–06:37 EDT, rl-carts (relook on the carts loss): rescued.**
- **Chain:** 16 stage runs, 7 retries, 445 turns, 139 min, against v23-carts' 2
  retries and 75 min.
- **Stage looks:**
  - 1 to 3 shown. Stage 3 (jump gating): the cart clears the 0.8 m barrier but not the 1.6 m
    shelf. v23 had stage 3 unclear, with the cart frozen.
  - 4 missing, then shown: a can into the bin scores "+50 CAN SCORED". v23 never fixed this.
  - 5 missing ×3: the cart froze after a restart, then the 1500-point win was out of reach in
    one look.
  - 6 missing ×3, all false: the 5:00 timer works and every look ended at 0:14–0:24. About 30
    min of retries were spent on a working stage.
  - 7 shown: a live HUD at 400/1500 with a keycard.
  - 8 missing ×2: frozen after a restart, and L2 only appears after winning L1.
  - 9 shown.
- **Gates** (copy 5029f6197211): 0 / 0.
- **Our probe:**
  - Enter ×3 opens a clean LEVEL LOADER (L1 unlocked, L2 to L4 locked with their goals).
  - Pressing 1, then W for 2 s: 400/1500, keycard 1/3, 11 tokens, "+50 CAN scored" popups, a
    rules panel and a control bar. A fuller game than v23's stuck loader.
- **Served** on :9008. Against B6 (:9002), Nick's blind grade decides.
- **Remaining real bug:** after R the cart can spawn frozen. It was reported at stages 5 and 8
  and never fixed, a diagnosis-gap case for trace.

**Relook so far:**
- skatemall rescued;
- carts rescued;
- gta6 not rescued (the builder cannot fix what is named).

Its cost: about 1.5–2× the chain time, much of it false misses on deep or timed content.
Teleport (tl-carts, queued) targets those.

**06:37–08:13 EDT, tr-catdefense (relook + trace on catdefense's design and plan).**
- **Chain:** 15 stage runs, 6 retries, 96 min.
- **Stage looks:** [(1, 0, 'shown'), (2, 0, 'shown'), (3, 0, 'shown'), (4, 0, 'shown'), (5, 0, 'missing'), (5, 1, 'shown'), (6, 0, 'shown'), (7, 0, 'missing'), (7, 1, 'shown'), (8, 0, 'missing'), (8, 1, 'missing'), (8, 2, 'shown'), (9, 0, 'missing'), (9, 1, 'BROKEN'), (9, 2, 'missing')]
- **Placement worked first time** (stage 3: placement mode, a range ghost, −50 coins). In this
  build `leftClick` places inside the per-frame input update, so no click can drop. The bug
  pv2-catdefense had did not arise, so trace was not what fixed it.
- **Trace fired on two misses**, at stages 5 and 8. Both were deep content (the market not yet
  fallen, the level select not reached), and both retries were shown.
- **The delivered trace** carried input → state lines, e.g. `click (640,280): ctx.enemies.length
  null -> 1`. Noise: the state exposes the same objects twice (`ctx.enemies…` and
  `enemies…`), and enemy motion fills the six-change cap.
- **Stage 9:** a blank Settings panel, then a boot break, then Settings working with one part
  still missing.
- **Gates** (copy 9180cb5ef0bd): 0 / 0. Served on :9009.

Read: no stuck bug arose here to test trace against. tr-skatemall (the kill plane) and tr-gta6
(dialogue, enemy death) are the real tests.

**08:13 EDT on, tr-skatemall: the first trace-carried fix of a specific bug.**
- **Stages 1 to 5:** stages 3 and 4 needed one retry each (a miss, then a boot break). Stage 4's
  kill plane worked first time, which rl-skatemall never achieved. Trace was not involved, so
  that is run variance.
- **Stage 6, missing:** "the exit door … a yellow lock icon and acted as a solid collider;
  pressing/holding 'e' never unlocked it".
- **The retry's request carried the trace** (stage.json's `seen_*` keys are cleared once read; the
  text is in the build's first user turn):
  - `hold w 2s: player.pos.x … -> 29.4`, the player stopped against the door;
  - `e` and `hold e`: "nothing in window.__game's state changed".
- **The retry (aaf1fa6b21f3) was shown:** walking into the portal now gives "EXITED — LEVEL
  COMPLETE".
- **The builder did not replay with play()** as asked. It read main.js, props.js, the level's
  exit, collision.js, then rewrote `js/objectives.js`.

One case; a text-only retry might also have fixed it. tr-gta6's dialogue and enemy-death bugs
(five and six text reports never fixed) are the sharper test.

**10:40 EDT, tr-gta6 so far: the trace can mislead.**
- Stage 3 (falling): missing, then missing (the retry with the trace rebuilt flat terrain), then
  broken.
- Stage 4 (shooting): missing all three times. The combo stuck at 1, then at 4, and the ammo
  never fell.
- The stage 4 trace read "nothing in window.__game's state changed" for all ten F presses, while
  the looker saw a hit and a combo counter. gta6's debug `state()` does not carry combat
  fields, so "nothing changed" was wrong.
- **Fix** (applies from the next trace run): each step also records whether the screen changed,
  as 160×90 grey mean diff ≥ 1.0 against the frame before the input. The text now
  distinguishes:
  - state lines;
  - "the screen changed but nothing in window.__game's state did (the debug state does not
    expose it)";
  - "neither the screen nor window.__game's state changed".

**11:15 EDT, tr-gta6 stage 6 (dialogue): eighth precise report, still unfixed.** Its trace read
"nothing in window.__game's state changed" for every input, walking included. gta6's
`state()` exposes nothing that moves during play.

Read: trace is only as good as the game's debug API.
- skatemall exposes player position, hp and state, and its trace pinned the exit (`pos.x ->
  29.4`).
- gta6 exposes static fields, and its trace carries no information.

The screen-change signal (10:40) turns that into "the screen changed but the debug state does
not expose it". The deeper lever is upstream: the design's `# 8. DEBUG API` section asking for
live state (player, enemies, interactables, UI screen) in `state()`. That is a design-prompt
change, so a lab.

**09:24–14:24 EDT, tr-gta6 done: the diagnosis gap held.**
- **Chain:** 22 stage runs, 13 retries, 609 turns, 300 min.
- **Shown:** stages 1, 2 and 7 (spawn points).
- **Missing at every attempt:** 3 (fall damage), 4 (ammo and combo), 5 (enemy death), 6
  (dialogue), 8 (the boss, out of reach) and 9 (the end screens, out of reach).
- **Trace was useless here:** gta6's `state()` changes for nothing during play.
- **Final:** 52cfb6b38325 (copy 9d879ffae627, gates 0 / 0). Title, settings, the loop, and
  death/respawn work; combat and dialogue do not.
- gta6 cost about 3× the other designs across v23, rl and tr. labs/debug-api-state (planned)
  is the next lever.

**Relook battery read (8 designs, 2026-10-25 to 10-26).**
- **Rescued:**
  - skatemall: no unclear stages, winnable, where pv2 was unwinnable;
  - carts: drives, scores, keycards, where v23 was stuck on its loader;
  - wizard cat: falls, the L1 clear and the reward screen.
- **No gain:** gta6 (the diagnosis gap, 5 h) and penguin (about 2.6× v23b's cost for the same
  game).
- **New designs:**
  - hira: gates inconsistent from stage 5;
  - frog: a dead exit;
  - bugs: collisions dead from stage 5 to 7, recovered by stage 9.
- **The shape:** relook turns "unclear" into a retry. That helps where the looker can reach the
  defect and the builder can fix what it names. It costs 1.5–3× the chain time.
- **Waste comes from three blind spots:**
  - deep content one look cannot reach (bosses, level 2, long timers);
  - real-time skill (timing, precise jumps);
  - the builder unable to fix a precisely named defect.
- **Next levers:**
  - labs/debug-api-state (planned): travel and setup functions plus a live `state()`, which
    would make teleport and trace useful;
  - a general build-prompt law for the recurring defect classes: dropped clicks, a goal present
    with no trigger, dead menu buttons.

**13:48–15:28 EDT, rl-bugs (frog-tongue bug catcher).**
- **Chain:** 16 stage runs, 7 retries, 398 turns, 100 min.
- **Stage looks:**
  - stage 1: missing (a yellow border, no HUD strip), then shown;
  - stages 2 to 4 shown first time: clamped movement and facing, spawn rings and wandering bugs,
    the X tongue catching flies with a sparkle;
  - stage 5 (score) missing ×3: tongue catches never scored, and on the last try stopped
    connecting;
  - stage 6 (wasp game over) missing ×3: wasp contact did nothing;
  - stage 7 (HUD updates) missing ×3: the HUD was stable and never changed;
  - stages 8 and 9 shown first time: pause, settings, Easy applies; a reached GAME OVER with
    "NEW HIGH SCORE", stats and a ranked high-score table. Deaths worked again by stage 9.
- **Gates** (copy 45c969380cdb): 0 / 0.

**12:15–13:48 EDT, rl-frog ("Froggy Fen" platformer).**
- **Chain:** 14 stage runs, 5 retries, 373 turns.
- **Stage looks:**
  - stages 1, 2, 4, 5 and 6 shown first time: the swamp level, run and jump, pit −1 heart with a
    respawn, camera clamp, HUD and pause;
  - stage 3 (the exit) missing ×3: walking into the archway triggers no win;
  - stage 7: missing ×3. Pip frozen, then the goal dead, then an invisible wall at x≈530.
  - stage 8: broken, then shown (settings, high scores);
  - stage 9 shown (title, "THE FEN HOLDS ITS BREATH" pause, game over).
- **The defect that held:** the exit never completes a level, the same "goal present, no
  trigger" class as skatemall's locked exit and hira's gates.
- **Gates** (copy c59864a6d24b): 0 / 0.

**2026-10-26 10:08–12:15 EDT, rl-hira ("Sumi's Study", a hiragana gate maze). The first chain on
the hardened look loop.**
- **Chain:** 18 stage runs, 9 retries, 507 turns, 127 min.
- **Stage looks:**
  - stages 1 and 2 shown;
  - stage 3: missing (no quiz at the あ gate), then shown (a 4-option "Recognition gate", the
    correct answer opens it);
  - stage 4 shown ("The page smudged", Try again);
  - stage 5 missing ×3: the gate stopped opening its quiz;
  - stage 6: missing ×2 ("choose a page · L" advertised, L dead), then shown (a 5-board list,
    3 loads L3);
  - stage 7 shown (difficulty and settings);
  - stage 8 missing ×3: one gate opens and another never triggers beside it;
  - stage 9: missing ×2, then shown (title, the calm pause, a score-only HUD).
- **The defect that held** from stage 5 on: gate triggering is inconsistent, so L1 can never be
  cleared.
- **Gates** (copy 972bb001b49b): 0 / 0.

**19:33–22:00 EDT, rl-cat (relook on cat's design and plan).**
- **Chain:** 16 stage runs, 7 retries, 464 turns, 147 min, against v23-cat's 2
  retries and 61 min.
- **Stage looks:**
  - stages 1 to 3 shown;
  - stage 4 (combat): missing (Zap never fired), then shown (the enemy chases and damages, a new
    hand on Space);
  - stage 5 (falls): shown first time, "YOU FELL 5 TILES - 4 DAMAGE"; v23 was unclear;
  - stage 6 (the level-clear reward): shown first time, "LEVEL 1 CLEARED… CHOOSE ONE REWARD"
    with three choices; v23 never cleared L1;
  - stage 7 missing ×3: the looks did not clear L1 again;
  - stage 8 missing ×3: "PICK A TARGET" swallowed tile clicks (a real softlock, possibly the
    catdefense dropped-click class); the last try cleared L1 and reached L2, with the bosses
    beyond reach;
  - stage 9: broken, then missing ×2 (title and settings work; L1 targeting stuck).
- **Gates** (copy 0ca1e2e104b2): 0 error rounds, 1 play round.

**16:55–19:33 EDT, rl-penguin (relook on v23b's design and plan).**
- **Chain:** 17 stage runs, 8 retries, 158 min, against v23b's 1 retry and 60 min.
- **Stage looks:**
  - stages 1 to 4 shown, including the climb on Shift+W / Shift+S;
  - stage 5 (fall): missing, then shown ("PIP FELL!", a respawn);
  - stage 6 (the win) missing ×3: the looker kept getting blocked at the wall's base;
  - stage 7: missing ×2, then shown ("SUN DOOR! next up: Switch Steps");
  - stage 8 (levers) missing ×3. The last look searched L1 for levers that live on L2, so at
    least partly a false miss.
  - stage 9: missing, then shown (title, level select, pause, full settings).
- **Gates** (copy fc95aa85b42c): 0 / 0.
- **Read:** on the penguin, where v23b already did well, relook mostly bought retries on deep
  content (win, levers) that one look cannot reach. It nearly tripled the cost. A design with a
  ladder of levels is relook's worst case until looks can travel.

**14:24–16:55 EDT, tl-carts done (relook + teleport).**
- **Chain:** 17 stage runs, 8 retries, 151 min.
- **Stage looks:**
  - stages 1 to 3 shown;
  - stage 4 (scoring) missing ×3;
  - stage 5 (win) missing ×3;
  - stage 6 (timer) shown first time: the look saw 04:59 to 00:00 and the TIME UP overlay,
    where rl-carts had three false misses;
  - stage 7 shown, with scoring and keycards working by then (250/1500, 1/3);
  - stage 8: missing, then broken, then shown (the L2 loader card with 70x45, 3000, 05:30);
  - stage 9: broken, then missing ×2. One attempt saw "L1 cleared → L2 unlocked".
- **Teleport:** the looker did call the API (`drive`, `release`, `hud`, to free a wedged cart),
  but no travel function existed. Its value waits on labs/debug-api-state.
- **Gates** (copy 52c78fe2c60c): 0 / 0.
- **Our probe** (Enter ×3, 1, W for 2 s): drives; 250 points and 5 coupons from a keycard, and
  a full HUD.
- **Served** on :9012 and in the grading list.

**15:30 EDT, tl-carts so far: teleport has nothing to call.**
- Stage 4 (scoring) was missing ×3: the score flashed to 6 in the during-action frame and reset
  to 0; the crate never moved.
- Stage 5 (win) missing.
- The build's `window.__game` at stage 5: `hud`, `keymap`, `drive`, `release`, `render`,
  `resize`. No travel or setup function exists to call.
- Folded into labs/debug-api-state (planned): section 8 asking for travel and setup functions
  per system as well as a live `state()`.
- The new tie-break picked stage 4's attempt 1 (responsive 1.0) over attempt 2 (0.84).

**12:45 EDT, keep-best tie-break changed** (from the next chain job).
- When every attempt at a stage misses, keep-best used to fall back to the latest attempt.
  Three times that kept the worst one:
  - rl-gta6 stage 9: W no longer moved;
  - rl-carts stage 5;
  - tr-gta6 stage 8: the game hung from turn 19, "frames byte-identical".
- Every look now records `responsive`: the share of its inputs after which the screen changed
  (160×90 grey mean diff ≥ 1.0).
- `chain.rank` puts it after "not missing" and before the attempt number. A hung or frozen
  build ranks below one that answers its inputs.
- Rows from before have no value and tie at 0, so their order is unchanged.

**2026-10-26 10:00 EDT, looks and player sessions were ending early.**
- 77 of 376 stage looks (20%) stopped before their turn budget.
- 6 of 52 refine sessions stopped too. Five were timeloop's rounds 1 to 3, after 1 to 3 turns,
  so the keep-best judge weighed builds on a few seconds of play.
- **Cause:** the turn loop breaks when the model's answer fails to parse twice (refine) or once
  (looks). With thinking on, a 1500- or 2500-token cap can run out inside reasoning and return
  no answer.
- **Fix** (from the next job): looks and the player now ask up to three times with
  `max_tokens=4000` before giving up.
- Earlier "unclear" and "missing" verdicts partly rest on truncated looks; read the weekend's
  numbers with that in mind.
- **20:20 EDT, the same defect in two more calls:**
  - the stage-look verdict (`max_tokens=1500`, one try). An empty answer defaults the verdict
    to "unclear", which relook then turns into "missing".
  - the refine player's report (3000, one try). pv2-farm3 round 1's s0 came back with no
    observations.
- **Fix:** both now ask up to three times at 6000; the UX tour turn goes 2000 → 4000. Some of
  the weekend's "unclear" verdicts were empty answers, not judgments.

**Trace so far:**
- tr-skatemall: 1 for 1 (the locked exit fixed on the first traced retry);
- tr-gta6: 0 for 2;
- tr-catdefense: only deep-content misses, no test.

**Ideas from the pipeline-v2 asks, unbuilt.**
- **Deep stages run out of turns.** On skatemall, stages 4 to 6 (gaps, enemies, exit) all came
  back unclear: the looker walked the level but never reached a gap, touched an enemy, or got
  inside the door in 16 turns. Catdefense stages 7 and 8 ended at wave 3. Options:
  - turns that grow with the stage index;
  - a start at the stage's own content through the game's debug API (the "teleport").
- **Keep-best ranks "unclear" above a specific "missing".** A retry that only makes the looker
  lose its way beats one that names the defect.

Held until the V2+V3 battery (carts, cat, gta6) has run with TURNS=16, so it compares with
v23b-penguin.

**Built and queued (20:15 EDT), `relook`** (chain.py opt, off by default so the battery is
untouched).
- An unclear stage look gets a second look with twice the turns (32).
- If that is unclear too, the stage counts as missing and is retried, carrying the look's
  account.
- Queued after the battery as rl-skatemall: the same design and plan as pv2-skatemall, where
  stages 4, 5, 6 and 9 were unclear and no one could reach the exit.
- Measured: whether the relooks resolve, the retries, and whether the final can be won.


## Outcome
