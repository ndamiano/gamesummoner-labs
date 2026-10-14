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

Run: `./run_arm.sh <arm> <N> [first pass]`, e.g. `./run_arm.sh r0 0`. Each pass pipes one
prompt file into a fresh `coding-agent` process via `drive.py`, which sends "continue" when the
turn ends on an announcement instead of finished work (default flags: basalt via llama-swap on :5001, reasoning xhigh, file
tools plus `--shell`: bash in bubblewrap, no network). The seed came from the same harness without `--shell`. Transcripts land in `<arm>/logs/`.

One commit per pass, titled `refine-passes <arm>: <prompt file>`, so `git log -p -- <arm>/DESIGN.md`
is the whole design history of an arm. A new arm starts with `cp r0/DESIGN.md` from the seed
commit. Only authored text is tracked (see `labs/.gitignore`); the built game stays local.

## Log

**2026-10-13, r0 attempt 1 (implementation fix and rerun).** `visuals` ("Add visuals to
DESIGN.md.") read "visuals" as figures for the doc: it probed PIL fonts to draw mock-ups, then
ended its turn on "First, the generator script:" with no tool call, and DESIGN.md never changed.
Prompts reworded to "Add a visual design" / "Add sound design"; the runner now stops an arm on a
pass that changes nothing instead of carrying on.

**2026-10-13, r0 attempt 2.** `visuals` (+207 lines, §14 plus a PIL figure script) and `sound`
(+255, §15) landed; DESIGN.md 338 → 800 lines. `build` stalled like attempt 1's visuals: 8 calls,
then "Starting with the core." and no tool call. Fix: `drive.py` keeps the session open, and when
a judge call on basalt (`prompts/judge.txt`) reads the turn's end as an announcement it sends
`prompts/continue.txt`, up to 5 times. The judge read all four turns so far correctly (both
stalls CONTINUE, both finished passes DONE). Rerunning `build` only.

**2026-10-13, r0 build (works; awaiting Nick's play).** One turn, judge DONE. Not a natural finish: 193
programs + 6 rejected bare tool calls hit coding-agent's 200-round cap, whose `_out_of_budget`
asks for "what you did, what state things are in, what is left" (the REPL does not print that
event). The summary's shape is that report, and the judge read it as finished work. Commit 05b5b4d: ~3.8K lines of Python, `cadence/` package with a PIL renderer
in a tkinter window and synthesised audio piped to aplay/paplay. The stack came from the visuals
pass, whose figure script calls itself "the seed of the renderer"; the turn had announced a
browser game in attempt 2. 33-room, 3-floor plan, 7 enemy archetypes, 9 grammar relics, three
self-written test suites. Its summary claimed all three suites green except one smoke block. Rerun
after the pass: smoke dies on a None event, maps fails 5 checks (unreachable enemies and stairs in
4 rooms, a floor with no boss), play fails 5 including "the bot finishes a run". It had seen
`maps-exit=1` two calls before writing the summary.

**2026-10-13, r0 launch (hand patch).** `python3 main.py` crashed on the first frame:
`img.tobytes("ppm")` is not an encoder in this PIL build, and the pass only ever ran headless, so
the window path never executed. Patched by hand in its own commit (frames go to Tk as base64 PNG)
so Nick can play; this is the only edit to r0's game not made by the model. coding-agent's round
cap raised 200 → 2000 for later passes.
Crash fixes, budget under 5 (Nick): (1) idle brace crashed effects.py, because the recognizer's
`brace` input event and the game's `brace` world event share a type and only the latter has a
position. After the fix, a headless random-input fuzz (taps, bursts, idles, pivots, rest holds,
frames drawn mid-run; 50 seeds) found no further crashes.
Nick's play verdict on r0: the concept is great and the model "didn't do an awful job", but the
game doesn't work properly. His read: more steps could fix it, more refinement probably would
have been better. Next: r1.
r1 so far: `design_refine` 338 → 525 (settled seed contradictions, chose browser + plain JS
over Python, cut scope to one floor of 8 rooms), `visuals` → 795 (+ `mockups/make.py`),
`visuals_refine` → 992 (rewrote more than it added, every number regenerated by the mock-up
script), `sound` → 1311 (+ `mockups/sound.py` and 29 reference cues). The cue WAVs are all 44
bytes: `wav()` returns the header without the samples. The §16 numbers are measured on
in-memory buffers and hold; the pass's only check on the files was `ls`. Watch whether
`sound_refine` catches it.
Nick on the cues (heard via a patched copy): the sounds are fine; the real test is how the game
feels. Off-target for both arms: the visual and sound prompts meant "write that part of the
design", and every design pass also built tooling (figure, mock-up and cue scripts). Prompts stay
as they are for r1 so the arms match; a "design only, no code" wording is a candidate lever for a
later arm.
`sound_refine` → 1507 lines, 88 calls: answered three questions the cue table left open and
extended `sound.py` by 134 lines. It did not catch the 44-byte cue files; they are regenerated
just as empty. Refinement closes gaps in the prose; it does not check artifacts it never opens.
**r1 build (works; awaiting Nick's play).** One turn, 535 calls, judge DONE, cap 2000 never near.
Browser game in plain JS (`index.html`, 11 modules in `src/`), as `design_refine` decided. Its
claim of `npm test` 59/59 green reproduces (rerun after the pass: 59 pass, 0 fail), unlike r0's.
It caught and fixed real behaviour bugs while testing (menu fired on the first tap, the room
overflowed the frame, a sticky rest latch closed the menu), and its audio tests caught the
cue-table attack values the design passes had asserted without rendering. Unbuilt by its own
account: rooms 6-8, the arcade layout, Hard mode, gamepad. The `.js`/`.html`/`.css` sources are
not tracked by `labs/.gitignore`, so only the README and Python tooling are in commit e56e1cd.
r1 hand fix 1 (same under-5 budget): the first cue threw in the browser, because `main.js`
assigned `renderCue`'s Float32Array to `AudioBufferSourceNode.buffer`; it now wraps the samples
in an `AudioBuffer` once per cached cue. Its tests never reach `main.js`, the one file allowed
to touch WebAudio. Not in git (untracked `.js`).
Nick's play verdict on r1: a complete, playable game, where r0 could not be got past its third
level (consistent with r0's own failing maps test: unreachable stairs in four rooms). r1 is
weaker in some of the UX. Mainly: hold-to-pivot seems to land on a random facing, where r0 had
an indicator; the rhythm "sorta" came across but felt inconsistent. The design specified pivot
feedback in one table row (an arc redrawn per 90° snap) while spending hundreds of lines on
contrast ratios and dBFS; no refine pass played or simulated a pivot. Nick: the lab "doesn't
feel like it has any teeth".

## Outcome
