# vision-ux

Status: single-run
Control: each source game's own build before the loop.

## Purpose

Nick (2026-10-24): "a bunch of big swings (vision in the pipeline, not just the player but look
at the UX)". The gates detect broken. The playtest player (labs/playtest-refine) finds what
blocks play. Neither looks at whether the screens read and look right: text contrast, overlap,
the HUD saying what matters, one consistent style, the design's art direction, nothing left
looking unfinished. Project memory "verification gap": the gates prove a game runs, never that
it is good.

A test review on four frames of the refined wizard cat (playtest-refine pr-cat after) returned
five concrete issues:
- the bottom status line in faint grey over bright yellow tiles, with the objective banner
  covering it;
- no targeting highlight in aim mode;
- affordable cards drawn as if disabled;
- a stray outlined box fixed at top-centre, like debug leftovers;
- a title backdrop whose desaturated palette does not match the play screens.

## Hypothesis

A loop of tour, review, direct and build makes the screens read and look better, with no new
breakage:
1. a vision agent tours every screen and plays a few turns (24 turns);
2. a single vision call looks at the last frame of each screen (up to 8) against the design's
   `# 3. VISUAL SPEC` and `# 7. UX` and lists at most five issues;
3. a director turns them into at most three changes, each with what the screen should look like
   and how to reach it, never a guessed cause;
4. one 40-step change build makes them, with the prod gates after.

A comparison call keeps the round or drops it.

Measured:
- the issues per round;
- whether the same issues recur;
- the comparison verdicts;
- gate rounds;
- Nick's eye on before against after.

Idea failure: the reviewer reports nothing real, the changes do not land, or the screens look
no better or worse to Nick.

## Setup

`ux.py <run id> <label> <rounds>`, with prompts in `prompts/`. It reuses playtest-refine's
`refine.py` (request, copy, note) and `loop.py` (copy of a non-stage run). Runs through
labs/runner. Frames and issues under /var/tmp/vision-ux/<label>/round<n>/; rows in
`results.jsonl`.

## Log

**2026-10-24 05:13 EDT, ux-cat round 1: the reviewer works, and the blind builder cannot act on
it.** Source 49faeca8b1f1 (playtest-refine loop-cat's best).
- **Round 0** (24 tour turns): three issues.
  - The objective is not clear: a tiny "REACH THE EXIT", a clipped green rectangle at the right
    edge and a hollow yellow box in the sky.
  - HUD and status text too small and low-contrast over the yellow floor.
  - The settings key map stops at `playCard2` and uses internal action names.
- **Director:**
  1. the exit as the design's glowing 48 px green door, pulsing at 1 Hz;
  2. HUD text in the HTML overlay at 16 px or more;
  3. a full key map with player-facing labels.
- **Change build:** 6bf88b0e7d63, 40 steps.
- **Round 1:** the same three issues, plus unreadable hand cards and a clipped remap table.
  Judged worse and dropped. Our side-by-side at tour turn 12 shows the HUD and play screen
  nearly pixel-identical before and after.

Read: the change build edited toward visual goals it could never check, which is labs/vision-build's
premise. Queued: the same loop with `UX_LOOK=1`, where each change build sees its page after
every play() (look.py on a `look.flag` in the run directory, under serve_v.py).

- **ux-cat round 2:** worse again; the final stays 49faeca8b1f1.
- **2026-10-24 08:22–08:43 EDT, ux-cat-look** (change builds with pictures): both rounds judged
  worse.
  - Round 1 (ac37ad9d8e92) added "malformed debug HUD bars" over the player and board.
  - Round 2 (2144c5b56985): unreadable card text, UI over the lower level and exit, a wrong tiny
    player sprite, a contradictory health bar.

  Why the pictures did not help: they arrived only 3 times in round 1's 40 steps. A change build
  mostly reads and edits and seldom calls play(), so it made HUD changes it never looked at.

**09:43 EDT on, ux-cat-autolook.**
- **Round 0:** four issues.
- **Round 1** (6ff05d2ca6a2): 16 pictures in 40 steps (9 auto after edits, 6 after its own
  plays), against 3 in ux-cat-look's round 1. The hand readability and font issues were fixed;
  a new one appeared (affordable Hop cards drawn disabled); the key map clip and low-contrast
  HUD stayed. Judged worse, since the new issue was "as serious as" those fixed.
- **The judge reworded:** from round 2's comparison on, `ux_compare.txt` weighs net, fixed
  against newly broken, with issues in both builds counting for neither.

- **Round 2** (b9f21bffa9b7), under the net judge: fixed the HUD/status contrast and wrong-font
  issues; "introduced" an unclear exit marker and no targeting feedback. Round 0's own review had
  already called the objective unclear. Judged worse; the final stays 49faeca8b1f1.

Read: the change builds now see their work, and fixes land. The comparison is the weak link:
each round's review comes from a fresh tour that visits different screens at different moments,
so "new" issues are partly reviewer noise.

Next (queued, ux-cat-paired, 3 rounds): `UX_PAIRED=1`.
- Every round replays round 0's tour inputs on the new build (`replay`).
- One vision call sees before/after pairs of each distinct screen and gives the verdict and the
  new build's issues (`paired`, `prompts/ux_paired.txt`).
- The tour is a fixed probe across rounds.

**11:57 EDT on, ux-cat-paired.**
- **Round 0:** five issues.
- **Round 1** (00b6f660977a, 40 steps): judged better, and kept, the first round this lab has
  kept. Judge: "boxing the HUD, clarifying cards with icons, and making the exit goal visible";
  against it, live game UI bleeding into the menu and pause screens, and some clipped,
  low-contrast HUD text left.
- **Our side-by-side** at tour turn 12 (same inputs) agrees:
  - before: translucent overlapping cards, a faint HUD line under them, and no exit on screen;
  - after: a boxed HUD bar (FLOOR 1/6, OBJECTIVE: REACH THE EXIT, DRAW, DISCARD, HAND, HINTS),
    opaque cards with icons, and a glowing green exit door with an arrow.

- **Round 2** (818a1d3eb6a3, 40 steps): judged better, and kept.
  - Fixed: the faint SCORE/COMBO/YARN line is now boxed, large chips ("SCORE 0 LOCKED", "COMBO 0
    LOCKED", "PAW COINS 0 LOCKED"), and the clipped key map is fixed.
  - Against it: HUD strips over the play field, and a clipped key map header and title config
    line.
- **Our frame** (turn 12): the chips read well. The hand and the new chips both sit over the
  blobs' row, so enemies are half hidden. The hand did that in round 1 too.

- **Round 3** (9afc08d0940e, 40 steps, 12:28 EDT): judged better, and kept. Final 9afc08d0940e.
- **Our side-by-sides**, round 0 against round 3:
  - **Play:** the board now sits in its own panel above the hand, so the blobs, the exit and the
    cat are all visible together, with the HUD chips on top. The hiding from round 2 is solved.
    The cost: smaller board sprites.
  - **Title:** larger text; the settings summary wraps "COLOUR-BLIND / ON".
- **Served:** before 49faeca8b1f1 on :8993, after on :8994. Nick's eye and play are the verdict.

Read: with a fixed probe the judge sees the same screen before and after, and its verdict
matches what a person sees. Three rounds of polish compound. The judge weighs "covers the enemies"
as one issue among readability gains; a gameplay cost like that may need more weight than a
font.

**14:00 EDT on, pv2-farm-ux** (source 22f19e8b91ee, farm refine's best).
- **Round 0:** five issues; the first is "every UI string in a book serif, not the spec's
  hand-lettered type".
- **Round 1** (7db3f37e299f, 81 steps with the gate repair): judged same, "pixel-identical but
  for timers".
  - The director passed the font issue on as change 1. The game has no hand-lettered font
    asset, so the builder spent its turns writing `tools/fontgen.py`, a procedural TTF
    generator, and never reached the clipped settings panel or the overlapping hint panels.
  - The only code diff is a reach fix from the gate's repair round.

- **Round 2** (fa4468df126a, 188 steps with the gate repair): judged same again, "pixel-identical
  in layout, typography and colour".
  - The director again wrote hand-lettered type into every goal, so the builder again wrote a
    font generator (`_gen_font_src.py`).
  - It also left a stub in `index.html`: `window.__game = { ready: true, stage: 'stub', ... }`.
  - Since "same" counted as keep, fa4468df126a became the final. The farm's real final stays
    22f19e8b91ee.
- **Fix:** ux.py now keeps a round only on "better".

Read: a style mismatch that needs an asset the game lacks is a sink. Director lesson: order the
changes by what blocks a player reading the screen (clipping, overlap, contrast) before style
fidelity.
`ux_director.txt` now says so (14:50 EDT): readability first; a style change needing a missing
asset last or not at all. It applies from the next director call.

**16:50–17:10 EDT, pv2-catdefense-ux** (source faedce8786c0, the first run with the reordered
director and the better-only keep).
- **Rounds 1 and 2** (ca4e7bab1b3d, b697cf948fff): both judged worse, on "the title and
  level-select captures are not those screens", "pause modal instead of title".
- **Our check:** the replays' turn 1 and turn 3 title frames are identical before and after.
  The game drops clicks at random (pipeline-v2 catdefense: an edge flag cleared every render
  frame), so the same inputs reach different screens later in the replay, and the judge scored
  the drift as regression.
- **Final** stays faedce8786c0.
- **Fix:** `ux_paired.txt` now tells the judge to skip pairs that show different screens or
  states and judge only like with like.

**19:40–19:57 EDT, pv2-skatemall-ux** (source ff2340f0be3a).
- **Round 0:** five issues, the first "the playable view is unreadable… near-black
  out-of-focus smears". The director put it first, as change 1.
- **Rounds 1 and 2** (d2c243f3b386, 22bb93190cea): both judged better and kept, for the
  settings screen: the header unclipped, a contained panel, no collision with the help bar.
- **The game view is unchanged:** our turn-20 pair is the same dark blur before and after.
  Round 2's judge listed one issue and none for gameplay. The likely cause is the drift rule
  added at 17:10: two 3D gameplay frames always differ in camera and player position, so "skip
  pairs that show different game states" skipped every gameplay pair.
- **Fix** (20:00 EDT): the rule now skips only pairs on different screens, and says that
  gameplay frames with things in different places are the same screen.
- **Final:** 22bb93190cea.

Earlier (queued): `UX_LOOK=auto`. look.py's auto mode runs the build's last play() script again after
any turn that edits files without playing, and shows that picture, so every visual change is seen.

## Outcome
