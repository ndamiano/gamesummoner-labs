# mockup-first

Status: single-run
Control: `labs/genre-first` 1730d01639bc arm 2 (cats; my mockup prompt, my note, my pick of four);
`labs/bible-first` bakery 2546d62858f8 ("a game, barely: one level, pastries on the ground,
scaring has no point, die while hidden") and the 2026-10-30 bakery builds in `docs/experiments.md`
(Flash-Next 4, DeepSeek 6.6–7, Opus 8).

## Purpose

`labs/genre-first` on cats, 2026-11-09: a generic theme-free game of the genre built clean (24
stages, zero retries), and one `change` pass shown a mockup screenshot of the finished game plus
a short note ("the picture is the whole inventory of the screen… keep every rule and number")
turned it into the best-looking build Flash-Next has made here; Nick: "It looks so much better",
"It works properly… probably a bit unbalanced being a bit too easy." The same pass with a
66-row text table and no picture was "awful"; with the picture and the 66 rows it was cluttered
and broke the rules. The picture carries where and how; the text carries what exists. The picture
also made the model call `generate_media` twelve times unasked, the first time in 777 jobs.

Two hands were mine in that run: I wrote the mockup prompt knowing the game and picked one of
four, and I wrote the note. And cats is the ask where everything already works.

## Hypothesis

The whole chain with nobody in it: genre → generic build → the model writes the naming note and
the mockup description (`look.txt`) → Qwen-Image paints it, seed 0 → `picture` pass (`note.txt`
+ the mockup) → `compare` pass (`compare.txt` + the mockup beside screenshots of the game as
built; the builder has never before been shown its own screen). Run on the ask that has beaten
every chain: the bakery ghost.

Two changes to `genre.txt` against genre-first, both for asks that are not a template: the ask's
own actions are kept as plain mechanics ("scare" must survive as "a startle that makes a walker
look away", or the game is a platformer with pastries on the floor again), and title / how to
play / win / loss screens are always lines of the list.

Measured: Nick plays `generic/`, `picture/` and `compare/`. Floor: is the generic game a working
game in which the ask's verbs do something. Then: does the picture pass make it the bakery ghost
game without breaking it, and does the compare pass move it closer to the mockup or just churn.

Idea failure: the generic game has no working scare-then-take loop (genre-first does not reach
template-miss asks); or the model's own mockup description paints a picture the game cannot be
(wrong counts, wrong view); or compare makes it worse.

## Setup

One ask, `bakery/ask.txt`. Private run, every seat `qwen-flash-next` on the local 5090; the
mockup is Qwen-Image 2512 through the llama-swap ComfyUI. From the repo root, run.py up:

    venv/bin/python labs/mockup-first/build.py all bakery

or `plan`, `build`, `look`, `picture`, `compare` one at a time. The pictures are attached to the
first message of a prod `change` build by a lab-side patch of `build_steps._seed`.

## Log

**2026-11-09 21:14, run `97cdc61d2da5`, bakery ghost, local Flash-Next.** Genre call: "Stealth
game", fixed 2D side view; the ask's verbs survived as mechanics: "presses a scare action to
startle nearby people so they stop watching or move away; this creates a window to press a grab
action and take an object", with a scare cooldown or 1–3 uses per level, countdown, detection
meter, 22 feature lines including title, how-to-play, level-start, win and loss screens. No noun
of the ask in it. Plan parsed, 24 stages: room, player, object + person with sight cone, **core
loop at stage 4 (scare → person stops watching → grab → counter)**, title, how to play, level
start, detection feedback, scare uses, grab + counter, countdown, detection penalty, routes,
progression, cues, pause, win, loss, quit → title, 3 levels, harder rounds, balance. Build
started 21:20.

**21:45, Nick, before the picture phases ran:** "Wouldn't the path shape on the TD have been
bad? It's meant to be an example screen. What if you show it a shop screen in an RPG and it
decides everything should look like that?" Right: my two-image test's first named difference was
the path shape, a level-layout change, and `compare.txt` as written asked for exactly that.
`note.txt` and `compare.txt` rewritten before either was used: the picture is one example moment
of the main play screen; it decides style, how each kind of thing is drawn, and the HUD; it does
not decide level layout, positions, counts or the contents of other screens, which take its style
only.

## Outcome

**2026-11-09 22:47, generic build ended.** 24/24 stages, 89 min, one retry (stage 8), 688 jobs, 0 failed, no console errors. Level card shows the loop: take 2 of 5, 3 scares, 60 s, detection meter, 5-level track. Look: grey boxes and a wall of text, as expected. Kept in `bakery/generic/`.

**22:49, look.** One call, about a minute; paint 62 s, seed 100, no picking. The model named it "Midnight Ghost Bakery", chose pixel art, dark palette, cyan ghost, yellow sight cones; HUD in the description is the generic game's own three counters plus scare uses and the grab key, nothing invented. The painted mockup misspells two labels: "PASTIES" and "FLIGHT" (for FRIGHT). The names note carries filler lines that name no thing ("The level is the Bakery level").

**23:40, picture pass ended.** One change build, 50 min, 0 failed jobs. The model asked for 11 images unprompted (ghost, customer, pastry, counter, oven, shelf, sack, lamps, door, table). Play screen now: pixel-art bakery, ghost and customer sprites, cupcakes, sight cones, the mockup's HUD exactly (three boxes top, fright bar and grab key bottom), all the generic clutter gone. Level layout is still the generic level's (platform, stairs, two rooms), not the mockup's room: the example-screen wording held. Defects: it copied the painter's misspellings into the HUD ("PASTIES", "FLIGHT") although the note says Pastries and Fright pulse, so the picture beat the text on labels; the two customers stand on top of each other; the title and level cards kept the generic text wall with new colours. Kept in `bakery/picture/`, real play shot `picture_play_real.png`.

**23:42, compare restarted.** The shot helper pressed Enter once and clicked, which stopped on the level card, so the first compare start (23:40) was handed the level card as the play screen. Stopped it a minute in, restored `picture/` into the run, made the helper press Enter three times, started compare again with a real play shot.

**2026-11-10 00:11, compare pass ended.** One change build, 29 min, 0 failed jobs, no new images. Changes on the play screen: a plank floor strip under the level, wall shelves full of pastries and counters behind the platform, the whole level drawn a little higher. Closer to the mockup's density; the background pastries now look like the ones to grab, so the screen reads worse for play. Not fixed: the misspelled labels (the mockup has them, so compare sees no difference), the stacked customers, the title and level cards' text wall. Kept in `bakery/compare/`. On this run the compare pass bought little and may have cost readability; Nick's play decides.
