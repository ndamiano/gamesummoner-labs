# CADENCE

A one-button game about rhythm. See `DESIGN.md` for the spec this implements; this file is
only how to run it and what state the build is in.

## Run

Open `index.html` in a browser (any static server, e.g. `python3 -m http.server`).
One input: **Space**, **Enter**, **J**, **F** or a **click**. That is the whole control set.

* one tap — Step (walk)
* two taps — Strike (hit)
* three — Lunge
* four — Guard
* five — Sprint
* hold — Pivot (turn); keep holding past 2 s and the game pauses
* nothing for 1.5 s — Brace (set your guard, give one enemy a free move)

`npm test` runs the whole suite (node ≥ 18, no dependencies). `npm run shots` regenerates
headless screenshots of the real renderer into `tools/out/`.

## Layout

| file | what it is |
|---|---|
| `src/cfg.js` | every tunable: constants, the grammar, the palette, the light model, the cue table, the measured audio/contrast fixtures |
| `src/recogniser.js` | the input grammar — pure `(event, t, state, cfg) -> (state, verb, fx)` |
| `src/sim.js` | the world — pure `(state, verb, ctx) -> (state, events)`, RNG and clock injected |
| `src/rooms.js` | the floor as ASCII strings (14.5) |
| `src/light.js`, `src/color.js` | the light model and colour derivation (15.3, 15.11-v2/v3) |
| `src/audio.js` | the cue synth (a port of `mockups/sound.py`), the mix planner, the Web Audio shell |
| `src/render.js` | the canvas renderer (section 15) |
| `src/game.js` | the shell: moves events between the three, owns no rules |
| `src/storage.js` | save / settings / burst log (section 11) |
| `src/main.js` | the browser entry — the only impure file |
| `test/*.test.js` | 14.6, 15.11 and 16.11 as executable checks |
| `tools/canvas.js`, `tools/shot.py` | a headless screenshot of the real renderer |

The three pure modules take the clock and the RNG as arguments, so the entire game can be
driven headlessly: `test/spec.test.js` plays floors and menus with no browser, no canvas and
no AudioContext.

## What is built

The M1 vertical slice, plus most of M2: the grammar and its two axes (count → verb, rate →
tier), the light model, one floor of 8 rooms (tutorial 1–3 verbatim from 5.1, then corridor,
bottleneck, fork, vault, exit), four verbs beyond Step plus Brace/Rest/Pivot, the metronome
as the face of the input pipeline, the intent ghost, the end screen, Assist mode, Calm mode
with undo, the settings menu (reached by holding, driven by the same grammar), the two
grammar-modifying relics, and cold-start resume.

Section 16's audio spec is implemented as measurements, not intentions: cue lengths, rendered
attacks, bus levels, band exclusivity, the metronome masking matrix and the worst-case mix
are all asserted by `test/audio.test.js`, which prints the table it is checking.

## Where this build departs from the spec, deliberately

* **Room size.** 14.5 shows a 24×24 map and 15.2 gives a 960×600 field at a 30 px tile;
  those do not fit together once the 1 px inter-tile gap and the letterbox frame (15.11-v4)
  are honoured. Rooms are 24×19, which fits both layout presets, and `test/spec.test.js`
  asserts that against `LAYOUT` rather than a magic number.
* **The light ramp.** 15.3's formula is kept verbatim in `light.js` (`specFloor`) and its
  measured failure is asserted in a test, exactly as 15.11-v3 describes it. The ramp the game
  draws adds 15.11-v3's exponent and a low ceiling, because 16.11 measured that cues on
  terrain get weaker as the light model gets brighter.
* **The audio plate.** Ducking the masker and the victim by the same amount changes no
  masking margin (measured). The plate therefore ducks per bus: the metronome deepest, the
  verb cues slightly, the world not at all. `MASK_TABLE` in `cfg.js` is this repo's own
  measurement, not `mockups/sound.py`'s, and the test fails if the two drift.
* **The mix ceiling.** 16.2's levels are peak levels, and the worst legal mix (two hits plus
  a kill plus a Strike) sums past −3 dBFS whatever the phases do — 16.9 predicted this. The
  fix applied is 16.9's own: a consequence cue fires once per commit, not once per event. A
  derived safety gain then covers the remainder; it is idle for ordinary mixes and the test
  prints both numbers.
* **The menu.** 7 describes one tap as both moving and committing, which cannot both be true.
  The menu runs through the same recogniser as the game: one tap moves, two taps commit, more
  taps move back, a hold adjusts the value under the cursor, a long hold closes it.
* **`<` in the room format** is both a west-facing spawn and the stairs in 14.5. It is the
  stairs here; spawn facing is a field. Noted in `src/rooms.js`.
* **Room 6's fork** is entered by facing plus verb, not by a three-way branch whose branches
  are verb-selected — that is M3 geometry. The room makes the choice visible; it does not
  implement the fork mechanic.

## Not built

Section 5.5's hazards (pits, pressure plates, gates, chimes), 5.6's light-as-puzzle, the
floor generator, Hard mode, live mode, gamepad/touch, and the third audio band. `C.MODES`
carries only Calm and Standard, with Hard left as a flag in the data model (D10). Two of the
five room briefs in 5.2 are unused because the rooms that need them are not built.
