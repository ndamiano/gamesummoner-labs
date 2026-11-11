# template-ask — the design stage is one paragraph that names the template

Status: done
Control: `docs/experiments.md` 2026-10-30 (bakery ghost through the shipped staged chain: DeepSeek
V4.1 Flash 6382ea1e857f = 6.6–7 at $0.37, Opus 4d1aa7d6046c = 8, Flash-Next = 4) and 2026-11-07
(`labs/subway-fps`: the naked path on the same model, 31-word ask "pretty solid" at $0.21; the
chain on that ask 6.5 at $0.98; the naked 11-word wizard cat ~7 as a Slay the Spire copy).

## Purpose

`labs/subway-fps` showed the naked build path on DeepSeek V4.1 Flash does well on an ask that
resolves to a canonical game shape with its stock feature tags ("fps controls, zombie enemies,
tracers, recoil, muzzle flash, high details") and that the 17K-word design chain on the same ask
costs 4.6× and loses the ask's own words. The naked path on a vague ask reproduces the genre's
default game (wizard cat → Slay the Spire). So the design stage's work may be one translation: the
user's ask → the nearest shape, its on-screen systems as tags, and the user's nouns as the thing
that replaces the shape's placeholders. ~150 words, not 13,000.

The bakery ghost ask is the test because it has no strong attractor (Haunt the House in fiction,
top-down stealth-collect in code) and controls on this exact model.

## Hypothesis

**What changes.** The design stage (JEV decide, design write, stage plan) is replaced by one llm
call on the design seat with `concrete_ask.txt`: name the shape and the view, list the core systems
as on-screen things, carry every noun and verb of the ask, keep the quality words, ≤150 words. The
paragraph is the build's request and the whole of `design/design.md`; the build is single-shot
(`designed=True`, no `stages.json`), everything else the prod path on `deepseek-4.1`.

**Measured.** The paragraph itself (which shape it picked, whether the ask's nouns survived);
build steps and done-vs-capped; cost; Nick playing it against the 6382ea1e857f 6.6–7.

**Expected.** ≥7 with the bakery ghost's identity (ghost, bakery, customers, scaring, pastries,
sunrise) at ~$0.3 and ~20 min, against the chain's 6.6–7 at $0.37 and 42 min. If so the design
stage shrinks to this call and the staged plan (`labs/skeleton-first`) slots under it.

**Idea failure.** A generic stealth or collect template with a bakery coat of paint, or ≤6.5. A bad
paragraph (wrong shape, dropped nouns, systems a player cannot see) is an implementation failure:
the prompt gets fixed and the run repeats.

## Setup

`build.py` from this folder, with `venv/bin/python run.py` up (it runs the api worker):

    venv/bin/python labs/template-ask/build.py

`ask.txt` is the ask, `concrete_ask.txt` the prompt. The script creates a public run, makes the one
llm call under a design build row (so it is billed to the run), writes the paragraph to
`concrete.txt`, lands it as request and `design.md`, kicks the build off, starts the GPU runner for
the art queues, waits with tier-chain's stall handling, and writes `build.json`.

## Log

**2026-11-08 01:05 EST, run 2997d5c16447.** Paragraph in one call, 99 words, $0.002
(`concrete.txt`): top-down single-screen Pac-Man-style collect-and-chase, float + scare verbs,
counters as obstacles, customers on patrol, scare radius with cooldown, dropped pastries, quota,
sunrise clock; every noun of the ask kept, "High detail" kept. Took Pac-Man's collect-and-maze and
dropped its chase: nothing opposes the ghost but the clock, because the ask names no antagonist
and the prompt asks for "the win and the loss", which a clock satisfies. Left alone to measure.

**01:25, done.** 58 steps to `done`, 0 fix rounds, 20 min, $0.28, 73 jobs (71 llm, 2 comfy)
none failed. "MIDNIGHT CRUMBS": title with controls and the 20-pastry quota; play screen
(`shot_play.png`) is a lit bakery, display cases, ovens, string lights, six customers on patrol,
scare radius with a "gathering nerve" cooldown bar, pastry quota, sunrise bar. Procedural art
plus two stills. Boots with no console errors. Against the chain on the same ask (6382ea1e857f):
58 steps vs 9 stages, 20 vs 42 min, $0.28 vs $0.37. Served at :8954. Nick plays next.

**2026-11-08, Nick played it: 6/10 on his relative scale** (the DeepSeek chain's 6382ea1e857f was
6.6–7, Opus 4d1aa7d6046c 8, Flash-Next e30b96b10489 4). "Honestly, this one was kinda clean…
The 'game' is not really good, but mechanically it works, the aesthetic works decently well,
there's a bit of personality to it, but it feels... not good? The gameplay itself is off. people
walk into the bakery with bread, then you spook them and collect the bread. It doesn't feel like
a bakery. They enter with the bread lol." What he imagined: 3D, customers order at the counter,
you slam an oven door while the pastry crosses the counter and take it while they look. "I think
the issue is lack of depth for *all of this*." And on a scene-only rewrite: "Why is the ghost
stealing pastries?… what's the situation? Why is this happening?… This ask isn't an 'only
gameplay' ask." Verdict: works as a build (cleanest Flash-Next-cheap build on this ask, 0 fix
rounds), idea failure as a quality step: naming the nearest shape bends the fiction to the shape
(Pac-Man pickups) and the shape has no room for the why.

## Outcome

Clean and shallow. The concrete paragraph makes the build reliable (58 steps, 0 fix rounds, 20
min, $0.28) and puts a template's loop where the ask's loop should be; it scored 6 where the
chain scored 7 and Opus 8, and it produced nothing of what the ask is about. Not adopted. Led to
`labs/bible-first` (the why first) and then `labs/genre-first` (the generic genre game first,
theme applied after). Section: `docs/experiments.md`
2026-11-08, "the design stage as one paragraph".
