# opus-design-deepseek-build

Status: planned
Control: labs/frontier-ceiling (Opus spec + Opus build: "kinda insanely good", ~$22; DeepSeek
V4.1 Flash spec + build: "6.5, messy", $0.78).

## Purpose

Opus's spec cost $1.27; its build cost ~$20. DeepSeek V4.1 Flash builds for well under a dollar.
If most of the Opus game's quality comes from the spec, an Opus spec handed to a DeepSeek builder
could land near the Opus game at roughly $2, a price GameSummoner can sell at. The 2026-08-28
design transplant arm (a stronger designer lifting a weaker builder) is the precedent.

## Hypothesis

## Setup

`labs/frontier-ceiling/router_engine.py` already routes per call type: a rule with
`"tools": false` sends the tool-less design write to the Claude engine (agentic write + task
budget) and a `"tools": true` rule sends build turns to the DeepSeek engine, for the same ask.

## Log

## Outcome
