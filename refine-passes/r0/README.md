# CADENCE

A game about **rhythm as language**: one button, and the *frequency* of your
presses is the verb set. The design is [DESIGN.md](DESIGN.md); this is the
build of it.

```
python3 main.py                 # play (needs a display)
python3 main.py --resume        # resume the saved run
python3 main.py --assist        # dwell wheel: the same one button, no timing
python3 main.py --live          # Live mode: enemies also move on a clock
python3 main.py --seed 7        # a repeatable run
python3 main.py --reduced-motion --grey --quiet    # the accessibility settings
python3 main.py --no-audio
```

Nothing to install beyond PIL and tkinter. The whole game is drawn with
`polygon + ellipse + line` - no bitmaps, no licensed fonts, no asset pipeline.

## The one button

| input | verb | turns |
|---|---|---|
| 1 tap | STEP | 1 |
| 2 taps | STRIKE | 1 |
| 3 taps | LUNGE | 1 |
| 4 taps | GUARD | 1 |
| 5 taps | SPRINT | 3 |
| hold | PIVOT - free while held, one detent per 200 ms | 0 |
| hold 2 s | REST - the pause menu | 0 |
| no input 1.5 s | BRACE - +1 Guard on the tile you face | free |

The **gap between presses** is the tier: over 700 ms is CAREFUL (-25% damage,
+1 Guard, silent), under 260 ms is FRANTIC (+30% damage, everything hears
you), between them is NORMAL. Those numbers are not hidden: they are the four
sliders in the pause menu, and the recogniser runs on them live (1-4 to pick a
slider, `[` / `]` to tune it).

Other keys: `space` / `enter` / click are the button, `h` help, `u` undo (once
per room), `s` save, `r` new run, `p` audio, `esc` quit.

## Running it without a screen

The engine has no clock and no device of its own - the app feeds it
`time.monotonic()` in milliseconds. So the same game can be driven by a
scripted key track, with no keyboard, window or sound card:

```
python3 main.py --headless --seed 4 --script '500:1:400;1500:2:150;2600:1:400' --record out/demo
python3 -m cadence.soundcheck        # renders every source/tier to out/sound/*.wav
python3 tests/smoke.py               # the input grammar, tiers, verbs, undo, save/resume
python3 tests/maps.py                # every authored room: size, reachability, exits
python3 tests/play.py                # a bot plays whole runs; the run must be beatable
```

`--script 'start_ms:taps:gap;...'` is the virtual key. `--record out/demo`
writes `out/demo.png` (a frame) and `out/demo.wav` (the audio the run made).
`App.capture(...)` renders the pause menu, the help card and the dwell wheel
for the same reason.

## Layout

```
cadence/
  config.py       every tunable number (2.3 thresholds, the accessibility dials)
  ladder.py       the six rungs, the tier rule, the grammar relics (6)
  recognizer.py   the input state machine: press / release / tick -> events
  game.py         verbs, half-turns, rooms, the run, save/resume, run profile
  entities.py     the player and the seven enemy archetypes (7)
  world.py        the authored rooms as ASCII, and the run structure (8)
  effects.py      the 14.6 effect timings; "input outranks presentation" (14.8)
  render.py       the renderer: the shape law, one light, the meter (14)
  theme.py        the palette and the primitives - figures/make_figures.py grown up
  audio.py        the 15.9 parameter table and its four primitives
  sound.py        event -> diegetic cue, and an output device if there is one
  app.py          tkinter: the clock, the key, the frames
  soundcheck.py   renders the whole sound table and prints the mix budget
tests/            smoke / maps / play
figures/          the design's figures (unchanged; the renderer started here)
```

## What is in, and what is not

In: the verb ladder and the tier rule, the pivot, graceful degradation with one
undo per room, Live mode as a dial, the dwell-wheel assist mode, seven enemy
archetypes (five keyed to your cadence), nine grammar relics that edit the
ladder instead of adding verbs, three floors of ~33 authored rooms (corridors,
bottlenecks, forks with a lit path / dark branch / safe alcove, locked doors
and switches, shops that price relics in turns, a period-keeping boss), the run
profile as the death screen, save/resume, the synthesised sound design, and the
accessibility settings the document asks for (reduced motion, greyscale, quiet
mode, assist mode, tunable thresholds).

Not built: the physical single-button device and the calibration screen (that
needs hardware), and the in-run threshold sliders - they live in the pause
menu, which is where the design puts them.
