# builder-eyes

Status: single-run

Control: `labs/tier-chain` run ac23f047b078, the four-tier zombie game. Its change build "can you
make the art a bit better?" (60 steps, 2026-11-06) and Nick's review of the result the same day.

## Purpose

Nothing in the build ever looks at the game and asks whether it looks right. The builder's `play`
tool returns data and no picture, a stage is checked by booting, and the play gate reads screenshots
only to see whether a pressed input changed the screen. Run ac23f047b078 shows what that costs. The
game works (every probe check of tiers 1 to 4 passes) and Nick scored it "a solid 7/10 for a first
draft", yet everything he named as wrong can only be found by looking: "a zombie that looks... not
zombie", traps that "don't really show off what they are", a build menu with "a bunch of
\"undefined\" in it", "free donuts extending past the sign". The blind change build spent 60 steps on
"can you make the art a bit better?" and touched none of them. Nick: "The fact that it's blind is
definitely part of the problems." and, on this lab, "I want to see what it detects".

## Hypothesis

Draft, mine, for Nick to reword. Shown screenshots of its own game and asked an open question,
Flash-Next names the defects that only show on the screen.

What is measured: how many of the ten defects below it names, and how many of the problems it lists
are not real when checked against the screenshot. The list was written before the run. Rows 1 to 4
are Nick's, 5 to 10 are mine.

| # | Defect | Shot |
|---|---|---|
| 1 | Build menu tab labels read "undefined" | menu |
| 2 | "FREE DONUTS" text runs past its sign | yard, menu |
| 3 | The zombie does not look like a zombie | start, yard |
| 4 | Traps and other buildings do not show what they are | yard |
| 5 | HUD: the "CARRIED" label collides with the count and "BRAINS" | yard |
| 6 | HUD: junk names run into each other ("CARDBOARD" into "ROPE") | start, yard, menu |
| 7 | Build menu rows: cost letters drawn over the name above; long names and the hint line cut off at the right edge | menu |
| 8 | "POCKETS FULL" is hidden behind the build menu | menu |
| 9 | Sight cones cover much of the yard and wash out what is under them | yard |
| 10 | Text on signs in the yard is too small to read | yard |

Why it should work: the play gate already has Flash-Next read screenshots of these games well enough
to press inputs and say whether the screen changed.

An idea failure: it names two or fewer of the ten, or more of what it lists is invented than real.
A partial result worth knowing either way is which kind it sees: plain mistakes in text and layout
(rows 1, 2, 5 to 8) or things that do not look like what they are meant to be (rows 3, 4, 9, 10).

Second half, added 2026-11-06 before the fix run. Handed the list as one fix note, a builder that
still cannot see fixes what is on it. What is measured: of the 20 real problems in the first look,
how many are gone from the same four screenshots, by a second look and by my own eye, and whether
every probe check of tiers 1 to 4 still passes. An idea failure: fewer than half are gone, or the
fixes break a check. The two wrong findings stay in the note, because a loop with nobody in it would
not have filtered them; what the builder does with them is part of the result.

## Setup

`look.py <run id>` takes four screenshots of the built game through its debug API at the gates'
1280 by 720 viewport (title, one second into a run, a staged yard with every building, passer-by and
lawman on it, the build menu open), and sends each to Flash-Next in its own call: `look.txt` as the
system prompt, then one user turn holding a line on the state of the game and the screenshot, in the
message shape the play gate uses. The request body is the builder's (`qwen-flash-next`, its own
reasoning setting), posted straight to the local llama-swap. Detection only: nothing is fixed.

From this folder: `../../venv/bin/python look.py ac23f047b078`. Screenshots land in
`~/output/builder-eyes/<run id>/`, the raw replies and `found.json` in `<run id>/` here.

`fix.py <run id> <label>` turns `<run id>/found.json` into one note with `fix_note.txt` (every
problem of every screenshot, unfiltered, under the state line of its screenshot) and starts a `fix`
build with it, the kind the play gate starts with its own findings, at the default 200 steps. It
then runs the tier-chain probe and keeps a copy of the game in `~/output/tier-chain/<run id>/<label>`.
`look.py <run id> <label>` looks again and writes to `<run id>/<label>/`.

## Log

**2026-11-06, one run: `look.py ac23f047b078`, the game as it stands after the art change.** Four
calls, 9 to 25 s each, 70 s in all. A 1280 by 720 screenshot costs about 1,000 prompt tokens. It
listed 22 problems: title 1, start 4, yard 11, menu 6 (`ac23f047b078/found.json`).

Against the list written before the run:

| # | Defect | Named? | Its words |
|---|---|---|---|
| 1 | "undefined" tab labels | yes | "shows the placeholder text \"undefinedundefinedundefined\"" (it took the tabs for the first entry) |
| 2 | "FREE DONUTS" past its sign | partly | right place, wrong cause: "The \"FREE DONUTS\" sign is overlapped by a pink character/heart, making the prop messy and hard to read" |
| 3 | Zombie does not look like a zombie | yes | "only a tiny green head is visible with no clear body"; "a disembodied green head ... rather than a recognizable zombie survivor" |
| 4 | Buildings do not show what they are | yes | "\"Free Puppies\", \"Brain Rot Cleaning Station\", \"Box on a Stick\", \"Banana Stand\", \"Garden Gnome\", and \"Dead Flamingo\" cannot be identified"; "The row of Walls with a Door looks like stacked wooden benches" |
| 5 | "CARRIED" label collision | yes | "reads \"CARRIED 1/3AINS\"" |
| 6 | Junk names collide | yes | in three shots, "mashed together as \"CARDBOARDROPE\"" |
| 7 | Menu rows: letters over names, text cut off at the edge | partly | the cut-off names, cost line and hint, each quoted exactly; not the cost letters drawn over the names |
| 8 | "POCKETS FULL" behind the menu | yes | found as broken text, misread as "BOCKETS FULL" and blamed on a typo |
| 9 | Sight cones wash out the yard | no | |
| 10 | Sign text too small to read | no | |

Six named outright, two partly, two missed. Of Nick's four: three outright, one partly. The two
misses are both mine and both matters of degree, not mistakes.

What it listed that was not on the list, checked by me against the screenshots. Real: Free Puppies
shows "Need junk" with 5 of every junk in hand (it costs a brain, "1B", which nothing explains);
passers-by and lawmen are "near-identical colored circles, so their roles are not distinguishable";
the "Police" banner covers the middle of the yard; a threshold tick runs through the "S" of
"BRAINS"; the "Donut!" pop-up is drawn over by its own icon; the litter the art change scattered
"does not read as searchable junk spots", so decoration and junk spots now look alike; the "Mouse"
keycap on the title screen (true, trivial). Wrong, 2 of 22: it called the Dumpster at the left edge
"the gray object meant to be a Fridge", and said "Quiet street" floats over the road when it sits
inside the heat panel.

Read: with eyes and one open question it finds the plain mistakes in text and layout nearly
completely, quotes small text exactly, and also says when a thing does not look like what it is. Its
weak spot is knowing which drawn thing is which: given names without positions it matched one name to
the wrong object. Verdict: works, on one game. Not yet tried: whether a builder handed this list
fixes what is on it.

**2026-11-06, 13:07 to 13:37, one run: `fix.py ac23f047b078 eyes1`, then `look.py ac23f047b078 eyes1`.**
The whole first list went in as one fix note (4,628 characters, 22 problems, the two wrong ones
included; `ac23f047b078/eyes1-note.txt`). The fix build ran to the 200-turn cap in 24.5 minutes
without calling done, compacting nine times, and left the game dead: it was part way through
redrawing the zombie and `src/render.js` used a tuning name it had not imported, so the draw loop
threw on the first frame. The play gate caught that as eight inputs doing nothing and a 22-step fix
build repaired it. After that every probe check of tiers 1 to 4 passes and the play gate is clean.
It changed six files, `src/render.js` most (+580, −175 over all six).

Of the 20 real problems in the first look, counted as listed: 13 gone, 2 papered over, 1 moved,
4 not fixed.

- Gone: the junk name collision (three listings), the tick through "BRAINS", "CARRIED 1/3AINS",
  the "Mouse" keycap, the "Donut!" pop-up, walls that looked like benches (redrawn as a plank
  fence), litter against junk spots (junk spots now have a dashed frame), "POCKETS FULL" (moved
  into the junk panel), menu rows and the hint cut off at the edge, and Free Puppies' "Need junk"
  (now "2C 1R 1 Brain" with a letter legend). The cost letters drawn over names, row 7 of my list
  which the look had missed, went with them.
- Papered over: "cannot be identified" and "near-identical colored circles". The builder left
  those drawings as they were and put a text name tag under every building and every person
  ("Box on a Stick", "phone guy", "cop").
- Moved: the "Police" banner, from the middle of the yard to the top of it, where the second look
  flags it again.
- Not fixed: the zombie (two listings; it was redrawn, and still reads as "a tiny floating green
  head"), the Free Donuts sign, and the "undefined" tab labels. The first look had placed
  "undefined" on "the first build entry", and the builder reworked the entries and left the tabs.

So none of Nick's four is fixed: three untouched in effect and one covered with labels.

The one wrong finding that named a real thing cost a redraw: told the grey thing at the left edge
"meant to be a Fridge" looked like a couch, the builder redrew the real Fridge, which now looks
like a washing machine. The Dumpster it had actually seen is unchanged.

Second look: 16 problems (title 0, start 4, yard 9, menu 3) against 22. Seven of them the fix
made: name tags that overlap each other ("Banana Stan" under "cop"), run together ("Tombstone
Mailbox"), are cut by the screen edge ("opper", "phone g") or show through the build menu, and
"B Brain in hand" beside the menu's own "B" key. Four persist from the first look (zombie twice,
"undefinedundefined", the banner). Two are false alarms: the bare foundation slab called "an
unexplained structure", and two Locals on screen at once called a duplicate.

Read: the loop of look, blind fix, look again works for mistakes in text and layout, which is most
of what the look finds. It does not make a thing look like what it is. A builder that cannot see
answers "cannot be identified" with a label, and its redraw of the zombie changed nothing a viewer
could tell. Three costs showed: 22 findings in one note took the full 200 turns and did not finish;
the build ended on a broken game that only the play gate rescued; and a finding that is right about
the text but wrong about the place leaves the bug where it is. By the test written before the run
this is not an idea failure (13 of 20 gone, checks pass at the end), but the half Nick cares about,
looks, did not move. Verdict: works for layout and text; idea failure for looks while the fixer is
blind.

**2026-11-06, Nick's verdict on the fix run.** "I would lean towards it improved, but still not
great. Okay, this has gone on long enough." No further run is planned here; the work moves to
`labs/pitch-interrogate`. The game is left as the fix run ended it (snapshot `35ecb1a`), with the
"undefined" tabs, the zombie and the Free Donuts sign as they were.

## Outcome
