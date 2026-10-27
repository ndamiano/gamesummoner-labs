# model-owned-audio

Status: single-run
Control: labs/frontier-ceiling battery (2026-10-18): every game's audio judged bad by Nick, across
Opus, DeepSeek V4.1 Flash, Gemini 4 Argon and local Flash-Next.

## Purpose

Nick, playing the battery: "Our sound thing kinda sucks, the audio in our games are bad, and I
think we need to fix it. Let the models do it themselves." The build prompt
(src/maestro/codegen/prompts/build.txt) fixes the sound path: line 64, "The game's sound is
lib/audio.js; the game makes no AudioContext of its own", with lib/audio.js described at line 53.
Every game is therefore limited to what lib/audio.js offers, whatever the spec's audio table
asks for.

## Hypothesis

Only build.txt changes: the lib/audio.js entry in the "already in the project directory" list and
the rule "The game's sound is lib/audio.js; the game makes no AudioContext of its own" are
removed. lib/audio.js is still seeded into the game folder; the builder may use it or not.
Expected: the builder writes its own WebAudio (oscillators, envelopes, noise, filters, a
sequencer) and the game sounds closer to what the spec's audio table asks for. Measured: whether
it imports lib/audio.js, how much audio code it writes, whether the game still runs (prod gates),
cost, and Nick's ear against the control. Idea failure: Nick hears no better sound, or the
audio code breaks the game (AudioContext errors, autoplay-blocked silence, gates fail on it).

## Setup

Control: 57cbb0ef882d (labs/opus-design-deepseek-build): the Opus wizard-cat spec from
d086d499669b, DeepSeek V4.1 Flash builder, stock build.txt, 200 turns, gates clean. This run
changes only build.txt. The Opus spec's §6 AUDIO is a full table of synthesised SFX and five music
tracks with tempo and voicing, and never names lib/audio.js, so the spec does not steer the choice.
DeepSeek because it builds best per dollar (frontier-ceiling: 6.25 average at ~$0.65 a game).

`prompts/` is a copy of src/maestro/codegen/prompts with the two lines removed; `build.sh` points
`build_steps._PROMPTS` at it for the kickoff, which is when the system prompt is read into the
build cursor. Gate fix builds start their own cursors in the control plane and read the stock
build.txt (known difference, logged if a fix build runs).

From the repo root, with `venv/bin/python run.py` up and no other llm worker:

    labs/model-owned-audio/serve.sh               # BUDGET=4 by default
    labs/model-owned-audio/build.sh d086d499669b model-owned-audio

## Log

**2026-10-22 22:40 EDT, run ee4f696fca48.** Opus spec from d086d499669b, DeepSeek V4.1 Flash
builder, lab `build.txt` (no lib/audio.js line, no "makes no AudioContext of its own" rule),
200-step cap. Capped at 200 like the control. The game wrote its own `src/audio.js` (236 lines,
`new AudioContext`, oscillator `tone()` and filtered `noise()` voices, an `sfx(name)` table and a
step-sequenced music player with title/floor/win/over tracks) and never imports `lib/audio.js`,
which still sits in the folder. The control 57cbb0ef882d's `src/audio.js` wraps `lib/audio.js`
(`import { sound, seq, setVolume } from '../lib/audio.js'`). 20 source files, 4479 lines. Gates:
error gate 0 rounds; play gate 1 round, one fix build of 40 steps that added the missing canvas
click-to-target for raised cards, then archived with nothing broken. Cost $0.68 for 264 calls,
every one at peak price (the control ran off-peak at $0.35). Served on http://127.0.0.1:8944.
Awaiting Nick's listen.

## Outcome
