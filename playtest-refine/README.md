# playtest-refine

Status: single-run
Control: each game's own unrefined build: the staged penguin (eedc7205ebd3, gated copy
c50414b074cc) and the staged wizard cat (32fa91f2477a, gated copy 543cb30da1fa) from
labs/stage-planner.

## Purpose

The gates only find what is broken. A game can pass both and still be hard to play. The staged
penguin passed with nothing broken, yet its camera starts behind a stone step with Pip out of
view. The play gate's own impressions already name real feel problems: on the wizard cat, "the
wizard barely appears to move… the MOVE counter is the only real feedback", and "HP changed
between turns with no animation or popup". Nick (2026-10-23): "maybe we can" be a judge of
quality.

Prior evidence against (2026-08-08, project memory "grades are aggregate"): Nick's grade,
transcribed as a fix note, did not make a better game. The fix found the real bug, but
legibility went down. A grade names symptoms, not remedies. Notes that carry design direction do
improve games.

## Hypothesis

Three steps turn what a player runs into into a better game:
1. **Player:** a vision-model player plays it for real, 30 turns of trying to get through the
   loop, not testing each input, and reports concrete observations, never scores.
2. **Director:** one call with the design turns those symptoms into at most three remedies tied
   to design sections. This is the step the 08-08 note lacked.
3. **Refine:** one change build (40 steps, prod path, prod gates after) makes them.

Measured:
- whether the player catches known problems (the penguin camera);
- the director's changes;
- the change build's steps and gate rounds;
- the same player session on the result: are the same problems still reported, and does it get
  further;
- Nick's blind play of before against after, the only verdict on quality.

Idea failure: the player reports nothing real, or reports what the gates already catch, or the
refine fixes the listed things but the game plays no better or worse by Nick's play, as on 08-08.

## Setup

`refine.py <stage run> <label>` reuses the play gate's machinery (`_serve`, `_act`, `_ask`,
action parsing) with this lab's prompts:
- `prompts/player_turn.txt`: free play;
- `prompts/player_report.txt`: observations;
- `prompts/director.txt`: remedies.

The player is shown the ask and the design's `# 7. UX` section. The copy is made with
section-budget's `branch.py`, with stage.json removed so the change build and the gates take the
stock path. Sessions with screenshots are under /var/tmp/playtest-refine/<label>/{before,after};
rows go to `results.jsonl`.

Local Flash-Next (Basalt), under labs/stage-planner's serve.py and local_gpu auto. `queue.sh`
runs it after the stage-planner bets.

## Log

**2026-10-23 ~20:00 EDT, smoke test (2 turns, penguin):** the player read the title ("Penguin
Pyramid… Play highlighted") and the level select ("Dune Steps, par 3:00, Switch Steps locked")
correctly and picked its moves. The session machinery works.

**2026-10-23 21:55–22:08 EDT, pr-penguin: the player works; the refine did not fix the real
problem.** Source eedc7205ebd3 (staged penguin; prod gates had passed it clean).
- **Before** (30 turns). The player's first observation: "The penguin I am supposed to control
  was never visible on screen at any point". It also found:
  - arrows and WASD seemed to pan the camera;
  - nothing ever climbed or scored;
  - the first play state froze until a restart;
  - nothing told it which structure is the climb path.

  These are the real problems; the gates saw none of them.
- **Director:** three changes tied to the design.
  1. Pip visible and controllable on the first play frame: reset at spawn, camera target at
     spawn, render in the design's colours.
  2. Controls on Pip (WASD move, mouse orbit, Space jump, C climb).
  3. A readable climb route (pulsing grip dots, a "Hold C on grip dots" hint board) and a
     sun-arch exit that scores and shows WIN.
- **Change build:** ffa755605dfc, 40 steps. Gates 0 / 0, nothing broken.
- **After** (30 turns): Pip still never visible; still no climb; and the dots panel against the
  stepped tiers still confusing. Frames no longer froze at the start.
- **Our probe of the refined game** (debug API + a raycast): the camera sits at the same spot
  (6, 2.5, 22.5), aimed at Pip at (6, 0.6, 16.5). A `solid_stone` mesh is still 2.69 m from it,
  between it and Pip. The camera's occlusion pull-in never sees that mesh.

Read: the player is the best detector we have, since it caught what the gates passed. The chain
broke at diagnosis. A player can only report "I can't see my character", the director guessed
"not rendered", and the builder made the guessed fix. The cause is camera occlusion, which no
one in the loop could see. The next try gives the builder evidence instead of a guess:
- the player's screenshots;
- a probe of the debug API's camera and player state at the moment of the observation.

**2026-10-23 22:08–22:20 EDT, pr-cat: progress.** Source 32fa91f2477a (staged wizard cat on the
Flash-Next design).
- **Before:** reached the Floor 1 exit and stood on it, but the floor never completed. It found:
  - nothing hinted where the exit was;
  - `w` dropped the cat into a gap instead of climbing;
  - fall damage was unpredictable;
  - the Hop aim prompt did not show where it would land.
- **Director:**
  1. a "Press E to exit" prompt on the exit tile, with E completing the floor into the reward
     screen;
  2. a Hop targeting preview (green landing tile, red first blocked tile, "Cannot hop there" and
     no cost when invalid);
  3. Move Up into an unsupported tile rejected with "No place to climb, use Hop or Climb"
     instead of a fall.
- **Change build:** e1863bc2f88b, 40 steps. Gates 0 / 0, nothing broken.
- **After:** beat both tutorial blobs and reached the exit; the session ended on the exit
  tile. The before-complaints about up-into-a-gap and the Hop prompt are gone; Hop now shows
  a dashed path. New, deeper observations:
  - a card's number key gives no aim prompt (clicking the card does);
  - blobs show no damage until an HP bar appears late;
  - the Hop preview does not say the landing is over a gap;
  - no way down except walking off a ledge.

Read: here the loop worked as meant. The fixes landed, the player got further, and its
complaints moved one layer deeper into the game. The difference from the penguin is that these
symptoms named their own causes (a prompt that does not show where it lands); the penguin's did
not. Served for Nick: before (gated copy 543cb30da1fa, :8967 or :8968 in the battery pair) and
after on http://127.0.0.1:8957.

**2026-10-23 23:22–23:36 EDT, pr-penguin-v2: the real cause found and fixed.** Same source as
pr-penguin.

v2 changes two things:
- `director_v2.txt`: for each problem, a goal in the design's names, what the player saw, and the
  inputs that reproduce it, never a guessed cause.
- The note asks the builder to reproduce each problem and find its cause in the code before
  changing anything.

Results:
- **Before** (a new session on the same game, which went further than v1's): walked Pip to the
  base of the grip wall. It found:
  - no climb key it could find;
  - the settings key map stops at "Move forward";
  - the penguin barely visible, "a tiny beige block";
  - arrows pan the camera, too slowly;
  - W sometimes does nothing.
- **Director v2:**
  1. climb on C within 0.6 of a climbable surface, with the design's speeds;
  2. the camera targets Pip and keeps him in frame (repro: Enter, Enter, w);
  3. WASD and arrows move Pip, and the mouse orbits the camera.
- **Change build:** 00caa301b90e, 40 steps. Gates 0 / 0.
- **Our probe:** the camera now sits at (6, 0.66, 18.08), 1.6 m behind Pip, and the first thing
  its ray meets is Pip's own mesh, where before it met a stone mesh 2.69 m away. The screenshot
  after Enter, Enter shows Pip from behind, facing the dotted grip panel.
- **After:** the next layer down:
  - each W swings the camera up and Pip leaves the frame;
  - the player never pressed C, since nothing on screen names it, so it never climbed;
  - it read Pip's orange feet as footholds.

Read: v2 fixed the cause v1 could not see. v1 guessed "not rendered"; v2's reproduction let the
builder find the occlusion. The after-session shows the next problems, as with the cat, so a
second round of the same loop is the natural next step. Served on http://127.0.0.1:8958.

**2026-10-24 03:35–05:00 EDT, loop-penguin: three v2 rounds; stuck on a design gap.**
- **Round 0:** in play but never climbed.
- **Round 1** (699a3f0b0dae, 30 steps): the player still never found the climb key. It tried
  Space, E, F, Q, G, R, Shift, Up and clicks, never C. The settings key map does not scroll past
  "Move forward", and a red reticle on Pip's back misled.
- **Round 2** (76984ef153c9, 40 steps): the director asked for C to climb as designed, the
  settings list to scroll to the climb row, and the reticle removed. Same outcome. Two new
  observations: the hold grid is offset brick-wise, and a/d rotate Pip around the corners.
- **Round 3** (2c272a1e92fe, 40 steps): same again. The settings list still does not scroll, and
  the play screen shows no control hint.

Read: the loop is bounded by its own rule. The design names C but never puts it on screen, and
`director_v2.txt` forbids features the design does not have, so the one fix a person would make
first, an on-screen "Hold C" at the wall, was never asked for. The builder also failed the
scroll fix twice. Next: a director that may add the smallest thing that makes the design's own
controls discoverable.

**2026-10-24 04:00–04:30 EDT, loop-cat: three v2 rounds; the player finished floor 1.**
- **Round 0:** fought one enemy, never found the exit.
- **Round 1** (fbfb4ba3cda4, 18 steps): killed two enemies and walked to within a tile of the
  exit, but could not drop onto its lower platform.
- **Round 2** (f53fd8e1265d) regressed: stuck on the starting ledge, every move "blocked". The
  round asked Hop to stop before solids and refuse invalid targets; movement came out too strict.
  This run had no judge yet, so round 3 built on it.
- **Round 3** (49faeca8b1f1): cleared Floor 1, killing both enemies and reaching the exit. What
  was left:
  - range messages that do not say why;
  - no cue before a drop;
  - enemy HP hidden behind the hand.

Read: three rounds took the player from mid-floor to the exit, through a regression the loop
could not see. That is what the keep-best judge (`prompts/progress.txt`, in loop.py since) is
for.

**2026-10-24 05:13–06:15 EDT, loop3-penguin: director v3, two rounds, both judged worse and
dropped.** Source 2c272a1e92fe (loop-penguin's last build).
- **Round 1** (792a773bd1d5): v3 asked for a "Hold C on grip dots" hint card within 3 m of the
  first climbable wall, and `js/ui/hints.js` has it. The player never saw it and still never
  climbed. It also reported strafing that overshoots and a start under a column with no
  reachable hold. Judged worse.
- **Round 2** (8b31d6e890fb): the same, plus A/D orbiting the camera. Judged worse.
- **Final:** 2c272a1e92fe kept.

Read: the guard did its job. Two sessions on one build can end very differently, though, so
one session is thin evidence for keep or drop. loop.py now plays each build twice
(`SESSIONS = 2`) and the furthest session stands for it. The penguin climb has resisted six
rounds of three loop versions. The next lever for it is the builder seeing its game
(labs/vision-build), not more notes.

**2026-10-24 08:25 EDT, the player was half blind: fixed.** labs/vision-build found that a
look which screenshots 1.5 s after a 0.2 s tap never sees a jump, and that the player could not
hold two keys at once. The penguin's climb needs C held with W. Every penguin session in this lab
(nine rounds) played that way, so "never climbed" there is at least partly the player's limit,
not the game's.

`session` now:
- shows a three-frame strip per action (during, just after, settled), via
  labs/vision-build/stage_look.py's `_act_watching`;
- takes a `chord` action; `prompts/player_turn.txt` says so.

The earlier penguin loop verdicts should be read with that in mind.

## Outcome
