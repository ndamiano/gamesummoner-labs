# pitch-interrogate

Status: single-run

Control: `labs/mechanics-curation`. Its decide chain (50 system rows kept over 0.7, definitions
handed to the designer) and its two frog platformer builds, 100f46b508a3 and fb0aa5866ea8, both
built to the end. Nick on the first: "the first game platformer that was actually completable".

## Purpose

mechanics-curation found that the designer writes a section for nearly every word it is handed
and that a short list gives a design the builder finishes. It also found what the list cannot
do. A hundred games fit "a zombie survival game" and nothing in the chain chooses one: JEV can
only say yes or no to rows put in front of it.

On 2026-11-05 and 06 Nick and Claude designed that ask by hand. Nick pitched a game, Claude
asked questions with a guess attached to each, Nick answered, and four rounds settled it
(`zombie/pitch.md`, `zombie/interview.md`). Nick: "I don't know how we get a better design for
this than what we're talking through. I don't think JEV buys us anything at this point. It is
for automated design, but I'm not convinced that it does anything positive given what we have."

Set against the 50 rows, nine of the game's thirteen parts have a row and four do not (luring
people to you, things that work without the player, heat, storage). None of what makes it that
game is a row: you are the zombie, the humans are dumb, the banana stand, the free puppies.

## Hypothesis

Draft, in Nick's words, not yet ruled on as a hypothesis: "a pitcher and an interrogator, and
the interrogator builds the design the pitcher pitches. Effectively, you'd be the interrogator
here, and I'm pitching my idea. We can probably throw JEV in to say something like is this a
good idea, but that'd be for future versions."

What changes: two model roles take the place of the decide step. The pitcher reads the ask and
commits to one game. The interrogator questions the pitcher until the game is concrete, then
writes the design.

The rest of this section is Claude's draft, written 2026-11-06 before the first automated run,
for Nick to reword.

What is measured, on the control ask "a platformer where you play as a frog":

1. The pitch chooses a game. It states who the player is, what they do and what they are after,
   none of which the ask gives, and the game is still plainly the ask.
2. The pitcher rules. Of the interrogator's guesses, how many the pitcher redirects or adds to.
   By hand Nick gave a plain yes to about a third of them.
3. The design carries the game. Every part and every piece of content settled in the interview is
   in the design, and the design has no system the interview did not settle.
4. The build finishes as the control did: fb0aa5866ea8 passed nine stages on the first attempt
   with both gates clean.
5. The number that should move: parts of the built game that are particular to its ask. Claude's
   read of the control design was "Nothing in the platformer is particular to a frog beyond its
   look." Nick's play verdict against 100f46b508a3 and fb0aa5866ea8 is the final measure.

Why it should move: the decide step can only keep or drop rows written before the ask existed, so
it cannot name anything particular to the ask. A pitcher can.

Idea failures:

- The pitcher restates the ask instead of choosing a game, or pitches a game the person did not
  ask for.
- The pitcher agrees with every guess. Then the interview is one model designing alone.
- The interview adds parts round after round until the design is the 44-section kind
  mechanics-curation started from, and the builder does not finish tier 1.
- The design drops or overrides what the interview settled.

Second arm, Claude's draft, written 2026-11-06 before its run. The first run's pitcher overturned
none of 15 guesses. Nick: "the concern is the pitcher is a rubber stamp. They aren't working
together, the interrogator is actually pitching things, and the pitcher is saying 'yes!'"
Claude's reading of the cause: by hand the pitcher held a whole game in his head and a guess
could miss it; the model pitcher held nothing past its three sentences. What changes: the pitcher
first writes a page for itself, pitches from it and answers from it, and the interrogator never
sees the page (`--page`). Measured: guesses overturned out of guesses made, and how much of the
page reaches the design. Idea failures: still none overturned; the page is a feature list and
the game grows to the 44-section kind; what makes the page particular never reaches the design
because no question touched it.

Third arm, written 2026-11-06 before its run. Nick: "what about giving the interrogator the
page, and letting it ask questions to the pitcher. I mean, if we think the page is good, let's
design based on the page, and let the interrogator question it and the pitcher be the creative
that answers." What changes: the interrogator is handed the pitcher's page in place of the short
pitch (`--shown`); the run reuses the second arm's page (`--from frog-page`) so nothing else
differs. Measured (Claude's draft): how much of the page reaches the design, counted on the
things the second arm lost; whether the questions land on what the page leaves open; the number
of parts (second arm: eight). Guesses overturned is expected to fall, since the interrogator
has now read the game, and is not a failure by itself. Idea failures: every noun on the page
becomes a system and tier 1 stops being a small core; the interview only reads the page back
and the pitcher only confirms it, which would make the interview dead weight; the design
overrides the page.

Nick, 2026-11-06, while the third arm ran, on what the lab is for: "overturned isn't super
useful as a metric. the goal of this is to get a more creative free flowing stream of
consciousness type design. Then the interrogator takes that and pokes at the little cracks /
issues, and turns it into a full fledged buildable design". This replaces measure 2 of the first
draft above. The page is the creative part; the interview is judged by whether its questions
land on the page's cracks and whether the design that comes out is buildable and still the page.

Fourth arm, Claude's draft, written 2026-11-06 before its run. The third arm's interrogator read
the page and asked nothing. Its prompt was written for an interviewer who had seen only a pitch:
"Stop when you could write the rules of every part without guessing at what the pitcher wants."
What changes: the interrogator's prompt is rewritten for the job Nick named
(`interrogator_cracks.txt`): list the cracks in the page, ask about them, most serious first,
with no guess offered; the pitcher's prompt says the answers are its own to make up
(`pitcher_cracks.txt`). Same page again (`--cracks --from frog-page`). Measured: whether the
questions land on the cracks Claude listed to Nick before the third arm's result came in (the
cat resets the frog to a perch while the heron coughs it up nearby; whether the wasp's sideways
hop is a mechanic or a joke; how much movement is too much for the cat; wind against a hop that
cannot be corrected; what starts a sprinkler); whether the answers and the page both reach the
design; the number of parts (third arm: eleven). Idea failures: the interview still ends at
once; the questions ask for numbers or for what the page makes plain; each answer brings a new
system and the game balloons; the design keeps the answers and drops the page.

Fifth arm, written 2026-11-06 before its run. Nick chose two of the three fixes Claude offered
for the fourth arm's spiral: "Sure, let's try 1/2". What changes, both in place in the two
cracks prompts (the fourth arm's wording is kept in its raw files): the interrogator is told
that cracks are in the page, that an answer is a ruling that closes its crack, and to come back
to an answer only when it cannot be true together with the page; the pitcher is told to answer
only what was asked and to close a crack with what is already on its page where it can. No
round limit beyond the script's six. Same page (`--cracks --from frog-page`). Measured
(Claude's draft): the round in which the interrogator ends the interview (fourth arm: never);
questions about things not on the page (fourth arm: about 13 of 27); parts in the design that
are not on the page (fourth arm: 3); whether the answers still rule in the page's voice as
round 1 of the fourth arm did. Idea failures: the interview still does not end; the answers go
thin and leave the design writer to rule alone again; a crack that needs something new, such as
what ends a place, is left unasked or unanswered.

Sixth arm, written 2026-11-06 before its run. Nick: "I'm also curious if the limit of 3-5
questions is valid. No reason we should limit it, I think". The limit was Claude's, copied from
the by-hand session, where a person answered a few questions at a time. What changes, in place
in `interrogator_cracks.txt`: the crack list is every crack, not "a short list", and there is
one question for each crack in place of "three to five". Same page. Measured (Claude's draft):
the round in which the interrogator ends the interview (fifth arm: never in six); whether what
a builder cannot start without (how the frog moves on the ground, what a reset restores, what
ends a place) is asked in round 1 (fifth arm: rounds 5, 6 and 2); words per answer (fifth arm:
about 90); questions off the page (fifth arm: 0). Idea failures: handed a long list the pitcher
answers thinly or skips questions; the interview still does not end; the list is padded with
what the page makes plain.

Seventh arm, Claude's draft, written 2026-11-07 at 01:10 before its run, on Nick's "You've got
the GPU for 8-10 hours, go for whatever". Nick's play verdict split the two labs cleanly: the
mechanics-curation control plays and has no character; the two cracks builds have "WAY more
character" and are "mechanically a giant mess". Claude's read of the mess, in order of weight: the
page invented a hard, non-standard verb (committed arcs, no air steering, no running, charge by
hold, three aim angles) that Flash-Next cannot tune on improvised geometry, where the control's
standard run-and-jump forgives bad geometry; tier 1 is fat; nobody authors geometry. Nick did not
say which kind of mess (feel or bugs) before handing over the card, so this arm tests the first
cause and the others wait on the result.

What changes: the pitcher's page is written with the mechanics-curation list in hand
(`systems-tight.json`, the 50 rows the control was decided from), and the page's verbs must be
systems from that list working the way they work in every game that has them; the page is free
in its world, its things, what happens and how it feels. The interrogator, the sheet and the
design writer are as in the sixth arm. In the sheet, a part named by a list name carries the
list's definition, as the control's decided state did (`designs-tight2`). Everything else on the
prod path is unchanged.

Measured: the systems the page names and any sentence that changes how a listed system works
(the sixth arm's page: a locomotion model of its own); how many of the page's particulars reach
the design (grep, as in the earlier arms); the plan's stages and places built; headless, whether
a scripted player completes the first place and whether there is a dead spot; and Nick playing
it against 100f46b508a3 (plays, no character) and a60ed53b9a82 (character, mess). Prediction:
completable like the control, and still plainly the frog game of the page. Idea failures: the
page reads like the control's design (the character was in the invented verbs); or it still does
not play (the mess was not the verbs).

Second ask in the same arm, if the first builds: "a tower defense game where cats defend a fish
market" (control ask 4257407d866e, a different genre where the list's systems are standard and
the character has to come from the world). Its control is the mechanics-curation chain on the
same ask, tight rows with definitions, built the same way (no build of it exists yet), so that
Nick has a pair to play for that ask too.

Eighth arm, planned the same night, if time: the sixth arm's fat tier 1 (ten places, every verb
and the cat all "first day"). After INTERVIEW OVER the pitcher is asked one fixed question, which
parts must be in the game on its first day for it to still be their game, and the answer goes to
the interrogator before the sheet, whose rule for the core band already reads "the parts the
pitcher said must work on the first day". Same page as the seventh arm's frog run. Measured: the
size of tier 1, and the plan and build as above.

Ninth arm, Nick's, written 2026-11-07 at 01:40 before its run, while the seventh arm's frog build
ran: "What if we give the verbs from JEV to the pitcher?" The seventh arm hands the pitcher the
whole 50-row list and lets it pick (it picked five for the frog; JEV, deciding the control, kept
four: platforming and hazards core, collectibles and scoring supporting). This arm runs prod's
decide step on the list first, as the mechanics-curation control was decided (`write.decide`,
JEV), and the pitcher's page is written with only those systems in hand, each with its band and
its definition (`page_decided.txt`); the interrogator cracks the page as before; and the sheet is
told JEV's bands and bands every part of the page under the system it belongs to
(`decided_said.txt`). So the verbs and the tiers are the control's, and the page, the interview
and the content are the pitcher's. Measured as the seventh arm, plus: the sheet's core band
against JEV's (the fat tier 1 of the sixth and seventh arms is the thing this should fix), and
whether the page's world survives having its verbs fixed before it is written. Prediction: the
control's frog with the page's garden. Idea failure: the page is a description of the control's
design (no character left), or the sheet ignores the bands. Run tonight ahead of the cats ask;
the cats ask then runs in this arm and the seventh, with its control. The eighth arm (first day)
is dropped for the night: JEV's bands do its job.

Tenth arm, planned, the decided systems stay the designer's: the ninth arm with three changes,
all in the prompt files. One, the interrogator is told what the pitcher was told
(`interrogator_decided.txt`, prefixed to `interrogator_cracks.txt` under `--decided`): the
systems are decided and each plays as it plays in every game that has it; the designer writes
that; a crack is in the world, the things, the order they arrive in and what happens to them,
never how a system works or what the player does to make it happen. Two, the sheet's mechanic
lines carry what each system is made of in this world and the rulings about those things, not
how the system plays (`sheet.txt`, the `core mechanics` line). Three, `decided_said.txt` gives
the sheet JEV's whole decided state, and the sheet keeps every line of it that is not a band
verbatim, above its own lines (view, look and sound, time and a run's shape come from JEV, not
the pitcher). Measured on the cats ask, one run: the design has a path with a base at its end
and build slots beside it made of the page's objects, more than one level, JEV's art style and
HUD; and the screen, played by Nick. Prediction: the control's tower defense in the page's
market. Idea failure: the sheet still carries rulings on how systems play, or the design ignores
the carried lines. Not in this arm, a candidate after it: the page prompt asks for the place
("where it happens and what is where"), since the cats page named things and never a geography.

## Setup

`interview.py <label> <ask>` runs both roles on the local Flash-Next with the request prod's
design write sends, and writes everything into `<label>/`:

- `pitcher.txt` is the pitcher's system prompt and `ask.txt` its first turn. One call gives the
  pitch (`pitch.md`).
- `interrogator.txt` is the interrogator's system prompt and `pitched.txt` its first turn (the ask
  and the pitch). Each round it reads the game back, lists what is settled and asks three to five
  questions with a guess each; the pitcher answers; the interrogator ends the interview itself
  with the line INTERVIEW OVER. The script stops asking after six rounds (`interview.md`).
- `sheet.txt` is the interrogator's last turn: the decisions sheet, in the shape of the decided
  state with its three mechanics bands (`state.txt`).
- Prod's write prompt, unchanged, writes the design with that sheet in the place of the decided
  state (`design.md`). JEV is not called.
- `--page`: the pitcher's system prompt is `pitcher_page.txt`, its first turn `page.txt` (the page,
  kept as `page.md`) and its second `pitch_from_page.txt`. Everything after the pitch is the same.
- `--shown`: as `--page`, and the interrogator's first turn is `paged.txt` (the ask and the page)
  and the pitcher answers under `pitcher_shown.txt`. `--from <label>` takes the page and pitch that
  label already wrote instead of writing new ones.
- `--cracks`: as `--shown`, with `interrogator_cracks.txt` and `pitcher_cracks.txt` as the two
  system prompts.
- `--verbs`: the page's first turn is `page_verbs.txt`, which carries the 50 rows of
  `labs/mechanics-curation/systems-tight.json`; a band line of the sheet that names one of them
  gets the row's definition before the page's own words (`state.txt`).
- `--firstday`: after the interview the pitcher is asked `firstday.txt` (which parts must be in on
  the first day); the answer, under `firstday_said.txt`, opens the interrogator's sheet turn.
- `--decided`: prod's decide step on the same 50 rows (`labs/mechanics-curation/write.decide`, JEV)
  runs first (`decisions.json`, `decided.txt`); the page's first turn is `page_decided.txt` with
  only the kept systems, each with its band and definition; `decided_said.txt`, with JEV's bands,
  opens the sheet turn; band lines get the definitions as with `--verbs`.

`build.py <label>` makes prod's stage plan for the label's design if it has none (the first run's
plan came from `plan.py` in `labs/mechanics-curation`, the same prompt and parse), lands design
and plan on a new private run and builds it on prod's staged chain, with the GPU runner and
stall watch of `labs/tier-chain`.

    ../../venv/bin/python interview.py frog a platformer where you play as a frog
    ../../venv/bin/python build.py frog-cracks3
    ../../venv/bin/python interview.py --cracks --verbs frog-verbs a platformer where you play as a frog
    ../../venv/bin/python interview.py --cracks --verbs --firstday --from frog-verbs frog-firstday a platformer where you play as a frog
    ../../venv/bin/python interview.py --cracks --decided frog-jev a platformer where you play as a frog

The by-hand session is the worked example of both roles. What the interrogator did in it:

- Asked a few questions a round, each with its own guess, so the pitcher could say yes or
  redirect.
- Asked for the reason behind a part (why traps, if the zombie can chase).
- Kept a list of what was settled and read the game back in a paragraph each round.
- Asked for the day-one core, and tiered the rest instead of cutting it. Nick: "A good design
  doesn't limit itself because the build can't do it. That's a build problem."
- Asked the pitcher for content in the pitcher's voice (the gags) and filled in around it.
- Wrote the numbers, layouts and rules itself once the game was settled.

## Log

**2026-11-06, by hand, one ask ("a zombie survival game", Claude's guess at what a user
types).** Nick pitched, Claude interrogated over four rounds, then wrote the design in the
pipeline's spec format (`zombie/design.md`). The rulings Claude made without asking are marked
C in the design's decisions table. Verdict: works by hand; nothing automated has run.

**2026-11-06, the by-hand design planned and handed to the builder, run 26d2aeb66c16.** The
design is 51 KB, four tiers, 15 buildables. Prod's plan prompt unchanged, Flash-Next, one call,
99 s, parsed first time (`zombie/stages.json`, `plans.md`; scripts are the ones in
`labs/mechanics-curation`, pointed at this folder). All nine stages are tier 1: draw the lot ·
move and sneak · starve and score · spawn the humans · sense and flee · grab and eat · search
for junk · build a box trap · title and polish. Nothing of tier 2 (lures, fridge, banana stand,
station, puppies), tier 3 (heat, law, weapons) or tier 4 (mansion, decor) is in the plan. Build:
prod staged chain, private run, Flash-Next on the local card. Result to follow.

**2026-11-06, build result, run 26d2aeb66c16.** All nine stages passed their check on the first
attempt: 239 build steps, then one fix round of 40 steps, 303 jobs, none failed, about 35
minutes. Error gate 0 rounds. Play gate 1 round: pressing E on a junk spot gave nothing. The
cause was a rule in the design, "any movement key pressed after the first 0.2 s of a search
cancels the search", which the build applied to a key still held from walking up; the fix round
changed it and the gate passed. Headless check by Claude through the design's debug API: the
run starts, the meter drains, a jogger spawns on the road and a local on the sidewalk, a human
facing the zombie turns `alarmed`, a grab from behind eats (brains 69 to 100, one Cardboard
dropped), a search at Trash Can A gives one Scrap and the spot refills in 25 s, a box placed at
(10, 6) holds a human who shows "HELP!". No page errors. The screen reads clearly: road,
sidewalk, yard, foundation, six junk spots, sight cones, the brains bar and the junk panel.
What exists is tier 1 only, as planned; the game folder has no module for lures, fridge, heat,
law, weapons or home. The play judge never caught anyone: it walked at humans from the front
and nothing on screen says to come from behind.

Read: a design from a pitch and an interview built cleanly as far as the plan reached, and the
plan reached tier 1 of 4. The ceiling is the nine fixed stages, set before the builder starts.
Verdict: works for tier 1; Nick has not played it.

**2026-11-06, the rest of the design built.** `labs/tier-chain` planned and built tiers 2, 3
and 4 on a copy of this run's game, run ac23f047b078: 17 more stages in 84 minutes, and its
probe passes every check it has for all four tiers. Detail and caveats in that lab's log.

**2026-11-06, 15:00 to 15:09, first automated run: `interview.py frog a platformer where you
play as a frog`, then `plan.py`.** Flash-Next in both roles. Pitch 35 s; three rounds of five
questions and the interrogator ended the interview itself in round 4, about 2 minutes; sheet
36 s; one design write, 225 s, 62 KB, no section missing. About six and a half minutes from the
ask to the design (`frog/pitch.md`, `interview.md`, `state.txt`, `design.md`).

- The pitch chose a game. "You play as Mire, a mud-stained tree frog trying to get home to the
  hidden marsh after the town drains the ponds. You run, leap, and cling through backyards,
  rooftops, and flooded gutters, using your tongue to swing from wires, snag keys, and pull
  loose planks aside. This isn't a frog that fights or collects shiny things; it's a small
  animal moving through a human-sized world, and every crossing is about how to get across
  without being caught."
- The pitcher overturned none of the 15 guesses. Twelve answers open with "Yes" or "Exactly";
  the five of round 2 agree without the word. What it added was content: the ways of being
  caught (a hand, a dog herding her into a bucket, a drain, a sprinkler, a mower), each
  hazard's tell (the cat crouches, the drain gurgles), weak anchors that slip, three named safe
  perches, and "without the tongue, the game is just a frog with a costume on". The rules came
  from the interrogator's guesses: no meter on the tongue, a failed crossing resets its puzzle,
  no timer, a straight route with no hub, the tongue cannot touch a hazard.
- The sheet carried it: six core parts (run, leap, cling, tongue, hazards and being caught,
  crossing), three supporting (keys, loose planks, intermediate safe perches), no extras, 35
  content lines, and a left-out line of 20 things.
- The design has those parts and no others: player, tongue, hazards and crossing in tier 1;
  keys, planks and intermediate perches in tier 2; tier 3 empty. Its own rulings are the
  numbers, 12 crossings (4 in tier 1), 9 kinds of hazard with counts, no HUD, and the art style.
  It restates the left-out list as rulings. The control design from the tight rows had run and
  jump, three hazards that differ in size, an exit, flies and a score.
- Plan: nine stages, all tier 1. The whole tongue (aim, grab, swing, pull, weak slip) is one
  30-turn stage, and crossings 2 to 4 with five kinds of hazard are one 35-turn stage.

Against the tests written before the run: the pitch chooses (1 holds); the design carries the
game and adds no system (3 holds); the pitcher agreeing with every guess is the second idea
failure as written, and it happened. The interview still produced the rules, but the
interrogator wrote them and the pitcher signed. The game is larger than the control's in what
the builder must make work: a rope swing, pulled objects and nine behaving hazards against run,
jump and spikes.

Claude started the build without asking (run 64b38dcc8621) and Nick stopped it: "don't build it
immediately". Paused after two jobs, runner stopped; nothing of it is kept as a result.
Verdict: works as far as the design; the pitcher's part in the interview is open; not built.

**2026-11-06, 15:23 to 15:28, second arm, one run: `interview.py --page frog-page a platformer
where you play as a frog`.** Nick: "number 2 is the most interesting", then "Sure, let's try it".
Page 39 s (about 1,450 words), pitch 2 s, two rounds of five questions and the
interrogator ended the interview in round 3, about a minute; sheet 36 s; one design write,
157 s, 61 KB, no section missing. About five minutes from the ask to the design
(`frog-page/page.md`, `pitch.md`, `interview.md`, `state.txt`, `design.md`). Not planned, not
built.

- A different game from the first run's: a small frog climbing to a moonlit rooftop pond where
  the other frogs are calling. It cannot run. It crouches to coil, aims and commits to an arc
  with no steering in the air, sticks to wet walls, slides off dry ones, and swings from what
  its tongue can catch, some of which breaks.
- Guesses overturned: 3 of 10, one more bounded, six plain yes (first run: 0 of 15). The three:
  the tongue "Mostly, but not only" anchors, it also pulls small things that change the scene;
  "Not exactly as a run that ends at the next pond", the pond stays the distant goal; crouch
  "Not as a stealth posture", it is the coil for the leap, and hiding is stillness and timing.
  Each correction is on the page.
- The design has the sheet's eight parts and no others: six core (crouch and committed leap,
  tongue, surface state, breakable supports, watching dangers, failure and reset), two
  supporting (disturbing things with the tongue, the legs of the journey). Three legs, four
  dangers (cat, heron, fish, sprinkler); tier 1 is one leg with one cat. Air control is 0.
- What was on the page and reached nothing after it (count in page / interview / sheet /
  design): wasp 3/0/0/0 with its hiccup hop, flies to eat 6/1/0/1, swimming 2/0/0/0, wind on
  the rooftops 2/0/0/1, greenhouse 3/0/0/0, lily pads 2/0/0/0, the leaf in the rain barrel
  4/0/0/1, the heron that swallows the frog and coughs it up, the cat that bats it away, the
  throat that swells. The interrogator saw only the pitch and asked about the pitch's phrases;
  the pitcher answered what was asked in a sentence or two and volunteered nothing.

Against the tests written before the run: guesses are overturned now, and from the page (the
first idea failure did not happen). The page is play described, not a feature list, and the
game is no larger than the first run's (the second did not happen). The third happened in part:
the rules that make the page particular arrived (no running, committed arcs, grip by wetness,
stillness), and its particular things mostly did not. Verdict: works; the pitcher pushes back
when it holds a page; what the page holds beyond the pitch is lost unless a question lands on
it.

**2026-11-06, 15:33 to 15:39, third arm, one run: `interview.py --shown --from frog-page
frog-shown a platformer where you play as a frog`.** The second arm's page, now handed to the
interrogator. The interrogator asked nothing: its first round read the page back, listed 113
settled lines and ended with INTERVIEW OVER (26 s). Sheet 65 s, 62 lines, the page's own
sentences sorted into bands. One design write, 262 s, 65 KB, no section missing
(`frog-shown/`). Not planned, not built.

- The page reaches the design. Count in the page / in this design / in the second arm's
  design: wasp 3/13/0, hiccup 1/9/0, sneeze 1/10/0, swim 2/14/0, wind 2/43/1, leaf 4/34/1,
  lily 2/22/0, greenhouse 3/14/0, caterpillar 1/8/0, koi 1/7/0. The opening on a leaf in a
  rain barrel is the start of level 1; the heron's "dark swallow, coughed up nearby" is a
  row of the failure table.
- Eleven parts against eight: six core (crouch-hop, tongue, sticky climbing and sliding, wet
  surfaces and water, avoidance and stillness, forgiving failure), four supporting (combined
  traversal, hazard escalation and distraction, environmental consequences, route variety),
  one extra (eating reactions). Five levels, three of them in tier 1.
- With no interview, the design writer ruled on every crack alone, and nothing records that a
  ruling was made. The sprinkler is started by holding E at a valve, on a page that says the
  world "is not made of locked doors or switches". The wasp's hop, "weird but useful" on the
  page, is a random push left or right and "Eating cannot unlock routes". The cat's "moving too
  much" became an attention number; the wind became zones with streaks.

Against the tests written before the run: the page reaches the design (holds). The second idea
failure happened in its plainest form, the interview is dead weight: no question was asked.
The cause is the interrogator's prompt, which stops "when you could write the rules of every
part without guessing at what the pitcher wants" and was written for an interviewer who had
only a pitch. Verdict: the page-to-design half works; the interview needs its own prompt for
this job; implementation fix and rerun.

**2026-11-06, 15:40 to 15:56, fourth arm, one run: `interview.py --cracks --from frog-page
frog-cracks a platformer where you play as a frog`.** The same page, the interrogator's prompt
rewritten to list cracks and ask about them without guesses. Six rounds, 27 questions, and the
interrogator never ended the interview; the script's six-round stop ended it, about ten
minutes. Sheet 93 s, 31 KB. One design write, 219 s, 63 KB, no section missing
(`frog-cracks/`). Not planned, not built.

- The first two rounds are the job Nick described. Eight of their nine questions quote the
  page and ask about a real gap, and all five cracks Claude had listed beforehand were asked
  (the wind in round 5). The answers are rulings in the page's voice. The tongue has "two
  registers: a light grab and a committed anchor", and "A quick tongue flick is a probe; it
  does not commit the body." The cat has four states and the heron three. The wasp, which the
  page called both "useful" and "flavor": the frog is "Buzzed", "the next jump gets a sideways
  kick and less control", and "the game never asks the frog to eat in order to move forward."
  The sprinkler "without warning": "No hazard begins with no physical tell."
- Then the interview fed on itself. At the end of round 1 the pitcher offered "the unasked
  seam", that a place is completed when the frog's call is answered. About twelve of the
  eighteen questions in rounds 3 to 6 are about things only the answers had introduced: the
  Answering Goal, Thresholds, the held croak as a noise that draws the cat, "stable return
  routes", coming back to finished places, rain. Each answer was new text with new cracks, and
  the interrogator treated it as it treated the page.
- Twelve parts (third arm eleven, second eight): seven core, three supporting, two extra, in
  four tiers. Three were never on the page: Answer Call and Place Completion, which is in tier
  1, Rain and Weather with six states, and Soft Ladder and Revisitation. Words in the design
  that are not in the page: answering 16, return route 16, croak 17, rest node 15.
- The page still reaches the design: wasp 15, swim 10, wind 22, leaf 17, lily 17, greenhouse 8.

Against the tests written before the run: the questions land on the page's cracks, and the
page and the answers both reach the design (hold). The third idea failure happened: answers
brought new systems, the game grew past the page, and the interview did not end. Read: two
rounds on the page gave what was wanted; the rounds after that were spent on the answers.
Nothing in the prompt says an answer closes a crack. Verdict: works for the first two rounds;
implementation fix (what counts as a crack once the pitcher has answered) and rerun.

**2026-11-06, 15:59 to 16:14, fifth arm, one run: `interview.py --cracks --from frog-page
frog-cracks2 a platformer where you play as a frog`.** The same page; the two cracks prompts
with the lines Nick chose (an answer is a ruling and closes its crack; the pitcher answers only
what was asked). Six rounds, 27 questions, about ten minutes, and again the script's stop ended
the interview, not the interrogator. Sheet 71 s, 24 KB. One design write, 177 s, 68 KB, no
section missing (`frog-cracks2/`). Not planned, not built.

- All 27 questions quote the page. None is about a thing only an answer introduced (fourth
  arm: about 13 of 27). The pitcher offered nothing unasked; its answers run 317 to 511 words a
  round.
- Two questions use the one way back the prompt allows, an answer against the page, "Which of
  these is the game?". The pitcher ruled against its own page both times: "The page line
  'Releasing lets the frog swing' is not the game", and insects "are never anchors". Earlier it
  had ruled "The page's 'slide upward' is not the game."
- Rulings a builder needs came out of it: on the ground the frog has "only standing,
  aiming/facing, crouch-charging, and launching", a tap is a short hop; in the air it is
  "ballistic"; a quick snap eats and a held tongue anchors; a reset restores the place to the
  state stored at the last safe perch, which "prevents soft lock"; every verb is there from the
  start; a place ends when the frog reaches its endpoint. The last three were asked in rounds
  5 and 6, so the order was not most serious first.
- The design has 21 named parts in four tiers: eight core, ten supporting, three extra, and
  eight places, four of them in tier 1. Every part is a thing on the page with its ruling
  (drainpipes, lily pads, hollow landmarks, wind, the wasp). None was invented in the
  interview: answering, croak and return route are 0 in this design (16, 17 and 16 in the
  fourth arm's). The count is high because each thing the interview ruled on became a part of
  its own in the sheet.

Against the tests written before the run: questions off the page 0, parts not on the page 0,
answers still rulings in the page's voice (all hold). The interview still does not end, the
first idea failure as written, though for another reason than in the fourth arm: after six
rounds it was still finding real gaps in a 1,450-word page. Read: this is the shape Nick
described, a loose page and an interview that pokes it into rules. Open: how long the
interview runs if left alone, and whether a builder can finish a tier 1 of seven systems and
four places. Verdict: works as a design chain; not built.

**2026-11-06, 16:51 to 17:00, sixth arm, one run: `interview.py --cracks --from frog-page
frog-cracks3 a platformer where you play as a frog`.** The same page; the interrogator's limit
of three to five questions a round removed. One round: 15 cracks listed, 15 questions, all
quoting the page; the pitcher answered all 15 in 1,139 words (about 76 each); the interrogator
ended the interview itself in round 2. Interview about four minutes (fifth arm about ten),
sheet 76 s, one design write 229 s, 68 KB, no section missing; nine and a half minutes from
the page to the design (`frog-cracks3/`). Not planned, not built.

- The questions are broader than the fifth arm's ("What rules decide when the cat notices the
  frog, how it approaches, when it swats..."), several things to a question.
- Asked in round 1: what completes the game and what ends a place (questions 1 and 2), what a
  safe perch is and how the frog gets back (14). Not asked at all, and asked in the fifth arm:
  what the frog can do on the ground, what happens to changed objects when the frog is reset,
  how eating differs from anchoring as an input. The design writer ruled the first alone
  ("A/D never move the frog on land", launch angle held between 20 and 78 degrees, aim by
  mouse; its numbers agree: 10.5 u/s at gravity 38 is 1.4 u high and 2.9 u far) and left the
  second out: a reset moves the frog and says nothing of the world.
- New from the page: its "bulging eyes that follow threats" and "throat that swells when it
  is nervous" became the pitcher's "danger language", how the player reads a cat's attention
  without a meter. The safe perch is marked by "a faint wet ring".
- 16 parts in two tiers: eight core, eight supporting, none extra. A table of ten places, each
  with a wake perch, an exit perch, a direct path and a longer safer one, in the page's order
  (leaf in the rain barrel, barrel rim, drainpipe mouth, crate, branch, greenhouse). No
  coordinates, as in every design here and in the control.
- Tiering differs from the fifth arm's on the same page: tier 1 here is all ten places with
  the cat only watching (its swat is tier 2); there it was four places with the swat. Nobody
  asks the pitcher what comes first in the cracks arms; the interrogator bands the parts alone
  when it writes the sheet.
- Rulings differ between the two runs (climb by holding up here, by timed hops there; a fly's
  sneeze is a back-hop here, cosmetic there). Each run the pitcher rules afresh.

Against the tests written before the run: the interview ends itself, in round 2; nothing off
the page; the answers are not thin and none was skipped (all hold). Of the three things a
builder cannot start without, one and a half were asked in round 1. Read: with no limit the
interview is one pass and stops, two and a half times faster, and covers the page broadly; it
no longer digs into the main verb, which the page describes well enough to look closed.
Verdict: works; the chain's shape is the page, one round of cracks, the sheet, the design.

**2026-11-06, 17:05 to 18:19, build of the sixth arm's design: `build.py frog-cracks3`, run
a60ed53b9a82.** Prod plan (124 s) then the prod staged chain, nothing changed but the design.
Nine stages: static place one · frog crouch hop · tongue anchor catch · tongue rope swing · sticky
pad wall · water haul out · wake exit reset · cat stillness danger · title end feel. Every stage
booted on its first attempt, 462 jobs, none failed; the play gate then ran two fix builds (100 and
86 steps). 72 minutes in all, against the control's one-shot build of the same ask.

The plan is one stage per verb and names one place. The plan's own words for stage 7: "hold the
exit perch to slide to the next-place placeholder". So the game has two places of the design's
ten: Place 1 (the leaf in the rain barrel, under the dripping gutter, with the rim cat) and Place
10 (the roof-edge pond with the lily ring), the second flagged `placeholder: true` in
`src/places.js`. Places 2 to 9 are not built. The design's hole, that nobody authors level
geometry, lands here as eight missing places rather than as bad ones.

Headless look (Playwright at the gates' viewport, the game's own `window.__game` debug API):

- It boots clean, no page errors. Title reads "Frog · a wet night, the roof tops, and the pond at
  the end of them", with the controls under it ("hold Space or the left mouse to crouch, release
  to hop · hold E or the right mouse for the tongue", "A and D never run").
- It looks like the page: night rain, a moon, the barrel with the leaf on the water, a dripping
  gutter, a branch with a hanging wire, a stack of tiles, the cat crouched along the barrel rim.
  By my eye the best-looking frog build of the day by a wide margin; the control is flat tiles.
- The verbs work through the debug API: crouch-charge-release hops (speed from hold time), the
  tongue flicks out and retracts on a miss, the anchors carry material cues (pear branch, wet
  copper wire "no hook and no fibre to bite", cracked tile edge), the cat notices a hop, walks to
  the rim exit and blocks it, loses interest after 2.2 s of stillness and climbs down to the
  ground, the safe-perch ring records after a rest, the lily-ring hold completes after 4 s still
  (chorus stops, rain fades, one call).
- Played through by script: Place 1 completes the way the design means it (hop, get seen, hold
  still until the cat leaves, hop onto the rim, hold 0.6 s, slide to Place 10). In Place 10 my
  scripted hop from the first pad landed in the pond and paddling did not haul out, so the pond
  crossing is not proven headless; the ring itself works when the frog is put on it.

Not measured: whether a person finishes it. Nick plays it.

**2026-11-06, 18:19 to 19:12, build of the fifth arm's design: `build.py frog-cracks2`, run
7bbc07a6171b.** Prod plan (102 s) then the prod staged chain. Nine stages: static rain barrel
world · frog crouch-hop controls · tongue eating anchors · water paddle haul · sticky wall grip ·
safe perch reset · cat stillness awareness · place chain completion · title complete polish. Every
stage booted on its first attempt, 328 jobs, none failed, one play-gate fix build (64 steps). 52
minutes.

This plan has a place stage, "place chain completion: traverse barrel, damp wall, branch/cat, and
final pond", and the game has four places of the design's eight, each its own screen:
`rain_barrel_leaf`, `damp_wall_puddle`, `branch_cat`, `rooftop_pond` (`level.js`). Four of eight
against two of ten in the other build; the planner budgets by verb in both, and how many places
survive is whatever the plan happens to name.

Headless look, same method (its debug API takes physical key codes: S or Shift crouches, W/A/D
aim at three angles, Space is the tongue):

- Boots clean, no page errors. Title, then Enter starts. Four distinct scenes: the barrel under a
  dripping gutter with a leaf on the water and a cat by the greenhouse; a tall soaked concrete
  face with anchor rings, a puddle and a tile shelf; mossy stone steps, two branches with anchor
  rings, the cat and a roofline plank; the pond with lily pads and a hanging wire. Flatter and
  smaller-scale than the cracks3 build (a small frog in a big screen), more world.
- Hops work and the three keyboard aims do what the design says (W is 90°, D+W 45°, D flat). A
  flat hop right from the leaf lands on the barrel rim, which is Place 1's endpoint, so Place 1 is
  one hop long and completes at once. Place 2 starts on the rim; a 90° hop reaches the tile shelf.
- A likely dead spot: a 45° hop right from the rim lands at the foot of the brick wall
  (`ground_court`, x 2.85), and from there no crouch-hop at any aim moves the frog at all, by
  scripted and by real key presses. The design has a dead-end reset; I did not wait long enough
  to see whether it fires there.
- Places 2 to 4 not played through headless; `places.finish()` reaches the completed screen.

Not measured: whether a person finishes it. Nick plays both.

**2026-11-06, Nick's play verdict on both builds.** "Frustrating. Cracks2/3 have *WAY* fucking
more character. They feel like a game about a frog. However, they're both mechanically a giant
mess. I was unable to play them effectively unfortunately." Against his bar for the near term, "a
bland game that reads well, plays well, and is very clearly what's in the prompt": both are very
clearly the game on the page and read well; neither plays well. The control (100f46b508a3) was the
reverse: playable and completable, no character.

**2026-11-07, 01:04 to 01:17, seventh arm, false start: `interview.py --cracks --verbs frog-verbs
a platformer where you play as a frog`, build stopped before its plan call returned.** The page
(756 words) named platforming, hazards, collectibles, stealth and time cycle and said "the controls
are ordinary platforming controls under gravity", but also "the path across is a chain of small
committed hops". The interrogator took that phrase as a crack (question 11 of round 1: what rule
makes the player "move in bursts"), the pitcher ruled "each gap is placed so it requires one
deliberate jump with no extra movement option to rescue a bad takeoff", the sheet carried it, and
the design wrote "Air control 0 while airborne. Horizontal velocity is locked at takeoff. Enforces
committed hops." The verb the arm exists to remove came back through one phrase on the page. Five
rounds, 36 questions; design 52.8 KB in one write; 6 core parts, 2 supporting. Kept in
`frog-verbs/` as evidence; no run was created. Implementation failure: the page prompt let the
page describe how a system is operated. Fix: `page_verbs.txt` now says "say nothing about how any
of them is controlled or how it works: each is played the way it is played in every game that has
it, and the designer writes that". Rerun as `frog-verbs2`; its page (490 words, "Moon Pool", a
tree frog crossing a rooftop garden before dawn: rain barrel, gutter, awning, heron, cat, drains,
lamps, rain lily bulbs) has no line about controls.

**2026-11-07, 01:17 to 02:07, seventh arm: `interview.py --cracks --verbs frog-verbs2 a
platformer where you play as a frog`, then `build.py frog-verbs2`, run 01eeafdb6f7c.** Page 113 s,
pitch, three rounds (34 questions, all quoting the page, INTERVIEW OVER in round 3), sheet 63 s,
design 221 s in one write (60.8 KB); 9 minutes page to design. Prod plan 9 stages: draw static
rooftop · control frog · land and camera · attempt start reset · fixed danger schedules · heron
lamp attention · moon pool goal · bulbs tile cat · title end feel. Build 38 minutes, 275 jobs,
none failed, stage 7 retried once (one error, then clean), no play-gate fix build. The same 38
minutes as the control's second build; the cracks builds took 52 and 72.

The verbs are the list's and the design wrote them the ordinary way: `maxSpeed=170, jumpVel=520,
coyote=0.08, jumpBuffer=0.08`, variable jump, no committed-hop rule anywhere (`design.md` line
59). The world is the page's: "Rooftop Crossing", a tree frog from a rain barrel across gutters,
wires, awnings and windowsills to the Moon Pool behind the greenhouse before first light, a heron
with a sight cone, lamps that light ledges, a cat that appears on the awning after the first bulb,
drains and fans on schedules, broken glass, five rain lily bulbs. One authored level of 27
platforms laid out in `src/gameplay/level.js` (x 120 to 2980), which no earlier build had: the
builder laid the geometry because run-and-jump needs only a ledge list. Sheet bands: 8 core, 3
supporting, 0 extra; `described()` matched 2 of the 5 named systems (hazards, time cycle), the
other three were renamed by the sheet ("Platforming and route viability", "Shadow, cover, and
being seen").

Headless: boots clean, title card "Rooftop Crossing", wake, then play; HUD "RAIN LILY ○○○○○ 0/5"
and "→ and ↑ to cross". A waypoint bot that walks right, jumps at platform edges and never hides
reaches x 1351 of 2980 (45%) on six attempts out of six, past the heron, and is taken each time by
the broken glass on a ledge (a hazard a person jumps), with a clean "Taken / the broken glass"
card and a reset to the barrel. Deterministic and traversable as far as tried; the pool not
reached by bot. Look: readable night rooftop, rain, moon, a plain small frog; less lush than the
cracks3 build (`a60ed53b9a82`), more world than the control.

Against the tests written before the run: the controls are standard (holds); the page's
particulars reach the design (heron, cat, bulbs, Moon Pool, greenhouse, gutters, awnings, drains,
fans, lamps, loose tile all in the plan's stage lines); the bot's 45% with no hiding says it plays
as a platformer. Not an idea failure on either count at this stage. Nick's play is the measure.

**2026-11-07, 02:07 to 03:04, ninth arm (Nick's), one run: `interview.py --cracks --decided
frog-jev a platformer where you play as a frog`, then `build.py frog-jev`, run `e0c46862c2cf`.**
JEV on the 50 rows first (`decisions.json`, `decided.txt`): core platforming and hazards,
supporting collectibles, extra scoring, side-on, real-time, a sequence of levels, reach the
exit, silly, pixel art. The page (`page.md`, 510 words, 50 s) was written with those four rows
and their definitions in hand: "Bullfrog Crossing", a frog that belongs in the swamp displaced
into a rain-swollen greenhouse after closing, moonlit glass, overturned pots, flooded clay pots,
lily pads in a basin, glass shelves, broken glass, black moss, a snapped mousetrap in a leaf,
still oil, pale moths behind pots, five rooms (opening greenhouse, flooded potting bench, broken
fountain, root-choked greenhouse, abandoned children's pond), "the game does not fight back. It
takes the rhythm away", and under "what it is not": no new verbs. Interview: one round of four
cracks (what a crossing is and what makes it clean; how moths are found; what the last safe edge
is and what persists; what opens the next room), the pitcher answered all four in rules, round 2
INTERVIEW OVER. Sheet 76 s (`state.txt`, 1.4K words). Design 227 s in one write (66.9 KB), 10
minutes page to design.

The measure this arm was written for: the sheet's bands are JEV's exactly, core platforming and
hazards, supporting collectibles, extra scoring, nothing added, nothing renamed; `described()`
matched 4 of 4 and each band line carries the list definition followed by "In this game, …". The
sixth and seventh arms' sheets had 8 to 10 core; this one has 2. The page's world survived the
fixed verbs: every particular above is in the sheet's content list and in the plan.

Prod plan 9 stages: static greenhouse room · frog platforming controls · hazard reset rhythm ·
exit and room transition · five greenhouse rooms · final run summary state · pale moth
collectibles · clean crossing scoring · title end screens polish. Build 45 minutes, 338 jobs,
none failed, every stage check clean first time, then two play-gate fix builds (22 and 41 steps;
the play gate's judgment had nothing broken, it could not see the jump in a screenshot). Design
rulings: gravity 1800, jump -650, run 240, coyote 0.08, buffer 0.12, cut 0.45, "horizontal jump
distance ~173 px, matching level gaps"; the rooms are authored rosters in
`js/levels/room_data.js` with a validator (`validateAll` ok, 5 rooms, 9 to 15 surfaces, 4 to 12
hazards, 1 to 5 moths, widths 1700 to 2500), gaps 30 to 70 px, drops under 80, hazards sitting on
the ends of landing platforms (glass, moss, mousetrap, oil pools, a bad edge) and water basins
under the gaps.

Headless (`scratchpad/jev4.py`, `jev5.py`): boots clean, title "A quiet, rainy place / Bullfrog
Crossing" with a controls card (← → / A D move, space / W / ↑ hop, R restart, Esc pause, Enter
confirm), Enter starts room 1. A platform-to-platform bot (run to the edge or to 22 px before a
hazard, hop, hold right until over the next surface) crossed room 2 clean by play (0 resets,
score 110 with a moth) and room 5 by play (0 resets, `run_complete`), and stalled in rooms 1, 3
and 4 at the same spot each time: a 50 px landing zone with a hazard on its right end, then a hop
that must clear it; bot precision, the geometry is consistent. Exits chain by teleport too, and
the end card "The frog walks out of the glass. Rain on the pond, and no one tending it" lists all
five rooms with moths and best scores, continue / cross a room again / title. Look: dark moonlit
greenhouse, glass panes, pot silhouettes on shelves, rain, a small plain frog; the mousetrap on a
pot, glass shards, a moss slick, a lily pad, all readable in one frame.

Against the predictions: "the control's frog with the page's garden" is what came out. Not the
idea failures: the page is not a description of the control's design (it has a title, a frame, a
voice and particular things), and the sheet did not ignore the bands. Nick's play is the measure.

**2026-11-07, 03:04 to 03:55, ninth arm on the second ask: `interview.py --cracks --decided
cats-jev a tower defense game where cats defend a fish market`, then `build.py cats-jev`, run
`b8351a8361eb`.** JEV: core combat, building, waves, economy; supporting abilities, scoring;
extra none; top-down, cursor only, a sequence of levels, defeat a final boss, silly, flat vector
(the same decisions as the mechanics-curation control's for this ask, `cats-control/state.txt`).
Page 70 s, 625 words: "The Fish Market Cats", the player is the Forecat of a wet dawn market,
Mackerel Mousers on crates, Calico Counter Cats, Alley Cats under awnings, Ragdoll Rattlers by
the ice tubs; seagulls from open sky, rats through gaps, raccoons that carry off whole crates;
failure shown in the market's own objects (crates knocked open, ice melting, signs tilting, cat
beds abandoned); "not a generic tower defense with cats pasted onto human towers". Interview:
one round of 14 cracks and 14 questions (66 s to ask, 48 s to answer, every answer a rule),
round 2 INTERVIEW OVER. Sheet 76 s, 2.3K words, bands JEV's exactly: combat, building, waves,
economy / abilities, scoring / none; `described()` matched 6 of 6. Design 221 s, 62.1 KB. Prod
plan 9 stages: static market layout · start build cats · bell ground waves · cat combat overwhelm
· customers sales close · market state repairs · real enemy progression · abilities score jokes
· title end feel. Build 38 minutes, 335 jobs, none failed, one play-gate fix build (36 steps;
the gate's judgment: every control and screen responded as documented, nothing broken).

Headless (`scratchpad/catsjev.py`): "Pale Harbor Fish Market / Dawn Watch · The Forecat", three
aisles of four stalls each with chalk pads, a Market Scale, gates, customer doors, a cat roster
of five (Mackerel 10c, Alley 12c, Calico 25c anti-air, Ragdoll 35c, Tabby 50c; hotkeys 1 to 5),
four tricks (Yarn Ball, Catnip Nap, Hairball, Awning Drop; Q W E F, wave only), a bell that
calls the wave (refuses in the first 5 s of prep, as designed), 30 coins and 100 stock to start.
Lifting the sign, placing cats by hotkey + pad click, tolling, the HUD, warnings ("gap in cover
· spread too thin · aisle A sign tilting"), the CLOSED card with a scored breakdown of the day
(stock held, coins earned, customers served, thieves turned away, stalls unbroken, high-value
stalls protected, aisles covered, perfect waves; customers lost, darkened stalls, crates carried
off, ice melted, beds abandoned, market closed) all work. Look: a readable dark-dawn market with
wooden stalls, blue fish crates, striped barriers, lanterns; the page's objects are on screen.

It cannot be won. 30 coins buys three Mackerels, one per aisle. Wave 1 is three rats (hp 14) at
one per aisle; each reaches a row-one stall in under 3 s; a Mackerel does 6 damage every 1.5 s;
so each cat lands one hit (`catStates` hits 1) and then the overwhelm rule fires: a thief that
reaches a target while standing permanently overwhelms the nearest covering cat and abandons its
bed (8 coins to repair, which the player does not have). By t=3 s all three cats are
`overwhelmed`, the rats never drop below 14 hp, stock goes 100 to 0 in 35 s, CLOSED. Two cats on
one aisle, same end at 50 s. Provenance: the page said "If the player spreads too thin, the cats
are overwhelmed and the market loses stock"; the interrogator cracked it (question 11); the
pitcher ruled "cats are overwhelmed when an enemy enters a placed cat's defense and the cat
cannot turn it away before the enemy reaches a crate"; the sheet carried it; the design wrote
the rule faithfully (§ Overwhelm rule) and chose the numbers (rat hp 14, cat damage 6 at 1.5/s,
rats reaching the first row in 3 s, no recovery) that make it one strike and permanent. Build
followed the design. The gate saw working controls, not a losing game, as gates do.

So on this ask the arm did what it was written for (JEV's bands, the page's market), and the
build is the most complete tower defense of the lab, and the first rule the player meets ends
the game. The failure is the design's numbers, not the pitch, the sheet or the builder.

**2026-11-07, 03:55 to 04:40, the cats ask's control: mechanics-curation chain (`write.py
--systems systems-tight.json --described --out designs-tight2 4257407d866e`, JEV decides on the
50 rows, prod write prompt with definitions), copied to `cats-control/`, then `build.py
cats-control`, run `d2321b3512ff`.** Same JEV decisions as cats-jev (`state.txt`): core combat,
building, economy, waves; supporting abilities; extra scoring; top-down, cursor only, defeat a
final boss. Design 223 s, 56.6 KB. Prod plan 9 stages: draw market floor · paw cursor input ·
cat build palette · thieves walk aisles · cats fight back · market open loop · all market stalls
· special cat powers · finish the game. Build 38 minutes, 382 jobs, none failed, two play-gate
fix builds (48 and 62 steps; the gate found two placement clicks that landed on the aisle or
removed a cat, then passed).

Headless (`scratchpad/catsctl.py`): "Catfish Market · cats defend the fish stalls", five market
days (Market Open 3 waves rats; Fish Flies gulls; Raccoon Racket; Crab Caper; a Gull King boss),
four cats (Alley 50, Fishmonger 120, Laser Pointer 175, yarn trap 60), three abilities unlocked
by days, settings (sound, Easy/Normal/Hard, reduced motion), high scores. 150 fish to start.
Three Alley Cats on crate cells beside the first aisle leg, waves driven by the fixed-step sim:
wave 1 five rats, wave 2 eight, wave 3 twelve, all 25 killed, stall 100/100, "MARKET DEFENDED",
score 3125 with a breakdown (kills 250, waves 600, stall 2000, fish 275), day 2 unlocked, Catnip
Frenzy unlocked. Cats placed in the far corner instead: 0 kills, stall 100 to 0 over three waves,
"The stall is wrecked — market closed", restart or quit. So it plays as a tower defense and is
winnable by the obvious opening. Look: a grid of paw-print tiles, a dashed aisle, three cat
circles, one fish-crate stall with a health bar, a flat HUD; nothing of a fish market in it
beyond the names. The bland game that works.

**2026-11-07, 04:40 to 05:40, seventh arm on the cats ask: `interview.py --cracks --verbs
cats-verbs a tower defense game where cats defend a fish market`, then `build.py cats-verbs`,
run `201866832990`.** Page 40 s, 768 words (the whole 50-row list in hand, the pitcher picks).
Interview 5 rounds (18 cracks; the interrogator kept finding more), sheet 61 s, 4.6K words: 6
core ("market survival and night state", "customers", "stock and fish supply", "enemy raids and
hazards", "basic market defenses and object durability", "bell and emergency response"), 7
supporting ("advanced cat roles and patrol", "bad fish detection and removal", "flung trout
events", "advanced market objects", "progression and strange raids", "cascading failure and
forced sacrifice", "joke behavior rules"), 1 extra; `described()` matched 0 of 14, every band
line is a name the sheet made up. Design 263 s, 80.5 KB, the largest of the lab. Prod plan 9
stages: draw market world · select and open stalls · run timer and phases · stock and dock cart ·
customers and sales · resources and market defenses · cats obey and act · enemy raids and bell ·
finish loop and feel. Build 46 minutes, 252 jobs, none failed, no fix build (the play gate's
judgment: every documented control responded).

Headless (`scratchpad/catsverbs.py`): "Tide & Tackle · The Night Watch", and the title card says
what it is: "You keep this market. You do not fight anything yourself — you choose what stays
open, what you let fail, and who you set to guard it." Seven stalls under awnings, a night clock
00:00 to 12:00, stores of coins 30 / fresh fish 62 / ice 40 / scraps 20, six market objects to
carry (netted awning, ice box, barricade, hook, rope, little trap), three cats asleep in lamp
pools with condition, energy, obedience, hunger and fear, aisle posts, a bell, a gate, a dock
cart, customers with patience, fish freshness per unit. Rules: open four of seven stalls before
01:00 or the market is lost at the opening; survive to the dawn bell. Idle: LOSS at 01:00 ("7
stalls are shut, ruined or occupied"). Four stalls opened, cats fed awake and posted, bell rung
at each raid: the market opens at 01:00, three gulls raid and leave with a fish each, fish spoils
with no ice boxes placed (16 spoiled, 2 sold), two stalls run out of sellable stock and shut, 5 of
7 non-functional, LOSS at 01:58 of 12:00, "The market did not hold", restart from the same seed.
Look: the best of the three cats builds by a distance, a real wet night market with lamp pools on
wet stone, red-and-white awnings, crates, cats curled in corners, a bell by the gate.

Against the ask: not a tower defense. The pitcher, free to pick from the list, built a night-watch
management sim out of it (stock, spoilage, upkeep, obedience, customers) and the sheet banded all
of it core; the interrogator's five rounds of cracks made the rules deeper, not fewer. The same
arm on the frog ask kept to the verbs; on this ask the page's world grew its own systems and the
list did not hold it. Compare cats-jev, where JEV's four verbs held the page to a tower defense
and the pitcher's market went into objects and failure states instead of systems.

**2026-11-07, morning, Nick's play verdicts and where the cats-jev screen came from.** Nick
played all four: `e0c46862c2cf` "almost exactly what I expect. It's a bit bland, but it feels
right"; `b8351a8361eb` "I have no fucking clue what's going on. The screen is a huge fucking
mess"; `d2321b3512ff` "functions, and is fine. It's not good, it's not bad"; `201866832990` "I
have no idea what's going on. It's like a market?" and a loss after a minute of looking (stalls
not opened before 01:00). His call: the control won the cats ask heavily, the ninth arm won the
frog ask handily. His frame for the next look: stuff is not the problem, what stuff is; eight
towers and four maps with variance would be fine; the stuff here manifests as junk. So, by
layer, what put each thing on the cats-jev screen (`cats-jev/`, screenshot at wave 1 in the
scratchpad's `catsjev/wave1.png`):

- Thirty-odd text labels on the market floor (`EN_A`, `S_A1` to `S_C4`, `J_A`, `J_B · MARKET
  SCALE`, `CUST_A`, `EX_A`, plus `GATE A`, `CUSTOMERS`, `EXIT`): not on the page, not in the
  sheet. The design ruled "market layout was left open" and wrote a node graph table with those
  ids (`design.md` 4.2). The prod planner's stage 1 done criterion reads "the page loads as a
  static wet dawn market with all nodes and pads visible" (`stages.json` stage 0); the builder
  obeyed it literally, `index.html` line 156: "node markers: every graph node is visible as a
  chalk mark", each with its id as a tag. Design ids → planner "visible" → builder labels. The
  design's own visual spec only ever says build pads are visible, as faint chalk outlines.
- Twelve identical stalls in a 3×4 grid, each with crate and ice tub, three candy-striped awning
  poles: design ("12 stall nodes", "one pole per lane at station 2"); the page said stalls,
  crates, ice tubs, awning poles with no count; the sheet carried the list without a count. The
  pole look is the builder's.
- The OPEN board hanging in the middle of the floor all game: the design says the Closed sign
  shows before start and at game over only; the builder flipped it to OPEN and left it hung
  ("lifting it turns the board over to the OPEN face for the day", `index.html` comment). Builder.
- The warnings strip (GAP IN COVER · SPREAD TOO THIN · AISLE A SIGN TILTING · AISLE B SIGN
  TILTING · AISLE C SIGN TILTING, three lines by the end), the repair bench, the fifteen-line
  score card, the ice/sign/bed states: this is the page's flavor turned into rules. The page's
  "what happens when it goes wrong" paragraph is one sentence of texture: "a stolen fish becomes
  a darkened stall, a missing customer, a thinner market, and a hungrier wave ... crates knocked
  open, ice melting, signs tilting, cat beds abandoned." The interrogator's q10 asked "what
  mechanical effects do [those eight nouns] have", q8 asked "what does each named object do"
  (seven objects), q11 asked what spread too thin, overwhelmed and loses stock do, q13 what
  economy buys. The pitcher answered every noun with a rule; the sheet's content list has 37
  entries, twelve of them failure states (darkened stall, tilting sign, missing customer, thinner
  market, hungrier wave, knocked-open crate, melting ice, abandoned cat bed, weak point, gap,
  spread too thin, high-value stall); the design gave each a field, a warning, a repair target, a
  penalty line and a visual state (98 lines matching warning/repair/melt/tilt against 1 in the
  control's design). Page texture → interrogator cracks → pitcher rules → sheet content → design
  systems; every layer did its job, and the texture became a HUD.
- The 5-card cat roster, the bell, the coin/wave/customer counters: page → sheet → design, and
  fine; this is the "eight towers" kind of stuff.
- One arithmetic defect on top: the only way a run ends is the market closing, and "Closed
  market" is a −1000 penalty, so every run scores 0 (the CLOSED card reads "0 best 0", penalties
  −1095).

So the junk has two sources, neither the page's nouns. One is the pipeline's own: a node graph
in the design became "all nodes visible" in the plan became id labels on the floor. The other is
the interview's shape: the interrogator treats texture as unruled mechanics, the pitcher rules
it, and nothing downstream can tell a rule that came from a sentence of feel from one that came
from the ask. The control had no page, so no texture, so no warnings strip; it also had no node
graph. The frog ask survived the same interview because a platformer has one screen with a frog
on it and the rules (coyote time, hazards on ledge ends, moths) all live in that frog; the cats
ask's rules each wanted a place on the HUD.

**2026-11-07, morning, second look at the cats-jev screen: the clutter under the labels.** Nick:
even without the labels there is a ton of visual clutter, "holes in the wall, holes in existence,
holes at the bottom, 4 desks in 3 columns, each desk has a basket with eggs and a register, carts
and barrels, rectangles with symbols, random things that look like nails, a gong". Mapped to
`index.html`: the wall holes are the three enemy arches, the bottom holes the three customer
gates, the holes in existence the two exits, the desks the twelve stall counters (design: "twelve
stalls, four per lane, each with a counter, fish crate, ice tub, and customer cart point"), the
egg basket the fish crate ("small brown box with fish-scale pattern, silver-blue fish shapes"),
the register the ice tub ("rounded basin, cyan gradient"), the rectangles with symbols the sixteen
chalk pads, the nails the awning poles, the gong the Market Scale ("brass polygon shape, pan,
needle, gauge glow"), the carts the customer carts; the barrels, bucket and rope coil are in no
document, the builder's props. Every one of them is a CSS gradient rectangle from the design's
23-row recipe table, and no build of the night called `generate_media` (0 of 4, the open
design-tiers-skip-art finding).

Why this design drew that way, and the control's did not: JEV's decided state is 23 lines, and
the ninth arm threads only the three band lines through. `decided.txt` for the cats ask says
`camera: top-down`, `art style: flat vector: clean flat shapes, solid colours, crisp edges`,
`palette: saturated`, `hud: health, score, wave number, currency`, `screens: title, pause,
settings, level select, high scores`, `session shape: a sequence of levels`, `failure: restart
the level`, `size: a handful of levels, under 30 minutes`, `typography`, `music`, `sound effects
style`, `effects`, `accessibility`, `time model`, `movement model`, `win/lose`. The sheet's shape
(`sheet.txt`) has no line for any of these; it has `view` and `look and sound` as prose, so the
sheet wrote "fixed oblique overhead view" and "wet dawn fish-market stalls, crates, awnings..."
and the other fifteen decisions vanished. The design then ruled each of them "left open" (0.2:
rendering, HUD, wave table, run end, best scores) and invented: DOM/CSS faux-oblique, a 16-row
HUD, one endless run that ends only when the market closes, a 15-term score with a −1000 closing
penalty every run pays. The control carried all 23 lines into the same write prompt and got a
flat-vector saturated top-down grid with a four-row HUD, levels and a restart: "fine".

This is an implementation gap in the arm, not an idea failure: the pitcher adds the world, and
the sheet should carry JEV's look and shape lines verbatim beside it. Fix: give the sheet (and
the page) the whole decided state, with the systems banded as now and the other lines kept as
written; rerun the cats ask once in the ninth arm.

**2026-11-07, morning, third look: the map.** Nick, on what the content should have been: "4-5
curated maps that are top to bottom with a fish market at the bottom, ocean / docks on the right,
and a path created by crates and barrels that you can put cats on top of"; the cat roster "feels
like it has that (mackerel vs alley, etc), but the map is awful." The control's design has the
tower-defense skeleton: "the path is a visible walkway", "build cells are shown as crate outlines
with paw marks", "the base is always at the right side", level records with a `path` each,
towers target "the enemy furthest along the path". It is bland because it has no world. The
ninth arm's design has no path at all: enemies "move down the aisles toward the nearest
unguarded stall, crate, or the Market Scale", twelve targets on three lanes, so the map is a grid
of stalls and the world is there but nothing to walk through it. Where the path went: the page
said "the market is the target, the economy, and the stage"; the interrogator's q1 asked what is
defended, q3 how enemies move, q4 what a gap is; the pitcher ruled every crate a target; the
sheet made it final; the design obeyed. Ten of the fourteen questions ask how a decided system
works (target, wave start and end, enemy movement, gaps, what each cat does, what each enemy
does, abilities, scoring, overwhelm, wave patterns, what economy buys), which the page was told
not to say ("each is played the way it is played in every game that has it, and the designer
writes that") and which `interrogator_cracks.txt` calls a crack ("a thing the page names without
saying how it works"). The two prompts contradict, the interrogator wins, and the designer, who
knows what a tower defense is, never gets to write one. The missing maps are the same drop as
the look: JEV said `session shape: a sequence of levels`, `size: a handful of levels`; the sheet
has no line for it, and the design wrote one endless run on one graph.

## Outcome

Character, at the cost of play. A pitcher's page questioned once for its cracks gives a design
that is plainly its own game, and the two cracks builds were "mechanically a giant mess". With
JEV deciding the systems first (the ninth arm) the frog ask came out "almost exactly what I
expect. It's a bit bland, but it feels right"; on the cats ask the same arm was "a huge fucking
mess" that cannot be won and the mechanics-curation control "functions, and is fine". Nick's
call: the control won the cats ask heavily, the ninth arm won the frog ask handily. The tenth
arm, written to carry JEV's whole decided state through the sheet, has no run. Led to
`labs/skeleton-first`. Section: `docs/experiments.md` 2026-11-06 to 11-07.
