# model-owned-audio

Status: planned
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

## Setup

The change under test: drop the lib/audio.js rule from build.txt and let the builder write its own
WebAudio. Everything else is the prod harness. One ask first, on the model that currently builds
best per dollar.

## Log

## Outcome
