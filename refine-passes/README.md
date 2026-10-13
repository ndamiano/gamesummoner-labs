# refine-passes

Status: single-run
Control: arm r0 (zero refine passes) of this lab; same seed design, same model, same build prompt.

## Purpose

The 2026-09-14 design-team entry in `docs/experiments.md` names what a spec still leaves to the
builder: levels, maps, a first minute. The builder improvises those and they come out thin. A
model in a fresh context, asked what it needs to build the game, has no memory of the intent
behind the doc, so it can only work from what is written. The holes it finds are the holes the
builder would hit. This lab tests whether making it close those holes before the build makes a
better game.

## Hypothesis

A design pipeline of stages (design → add visuals → add sound), each optionally followed by N
fresh-context refine passes, then a build. Arms differ only in N.

- **r0**: N = 0. Stage, stage, stage, build.
- **r1**: N = 1 after every stage.
- **r2**: N = 2, run only if r1 beats r0.

Measured: Nick plays each build and ranks the arms. Secondary, read off the git history:
DESIGN.md growth per pass, and whether a refine pass's questions repeat or turn trivial (that
means it has converged) or keep inventing detail (bloat). Also any decision a later pass quietly
reverses.

Idea failure: r1 plays no better than r0, or its passes only add length (padding, restated
rules) without closing gaps a player would notice.

## Setup

Model: basalt, Flash-Next IQ3 local on the 5090. Every pass is a fresh context with the arm's
folder as working directory and exactly one prompt from `prompts/`, sent verbatim. Minimal
tools: read, write, edit and shell in the arm folder. No GameSummoner library, tools, or build
path. Tooling is the next version's lever.

Seed: `r0/DESIGN.md` is the output of `prompts/design.txt`, already run. Every arm starts from
that commit, so the design stage itself is shared.

Pass order per arm (refine after each stage, repeated N times):

1. `design.txt` (shared seed), then `design_refine.txt` × N
2. `visuals.txt`, then `visuals_refine.txt` × N
3. `sound.txt`, then `sound_refine.txt` × N
4. `build.txt`

Run: `./run_arm.sh <arm> <N>`, e.g. `./run_arm.sh r0 0`. Each pass pipes one prompt file into a
fresh `coding-agent` process (default flags: basalt via llama-swap on :5001, reasoning xhigh, file
tools plus `--shell`: bash in bubblewrap, no network). The seed came from the same harness without `--shell`. Transcripts land in `<arm>/logs/`.

One commit per pass, titled `refine-passes <arm>: <prompt file>`, so `git log -p -- <arm>/DESIGN.md`
is the whole design history of an arm. A new arm starts with `cp r0/DESIGN.md` from the seed
commit. Only authored text is tracked (see `labs/.gitignore`); the built game stays local.

## Log

## Outcome
