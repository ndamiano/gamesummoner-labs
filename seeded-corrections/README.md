# seeded-corrections

Status: done
Control: the direct-call rates in Purpose, measured 2026-10-20 over every python-only build in
`~/output/runs`; a same-position control arm at battery stage.

## Purpose

Two small, repeated ways a Qwen build turn does nothing:

- **Direct calls.** The model calls a game function (`read_file`, `edit_file`, `play`, `done` …) as
  a native tool call instead of inside a `python` program. The schema has only `python`. The harness
  answers "That call carried no `code`, so nothing ran", and the step is lost. Run 8fc1191a0c54:
  2 in build 1's 200 turns, 27 in its ghost fix tail.
- **Refused programs.** The program uses `open()` or is not valid Python, and nothing runs. Run
  8fc1191a0c54 turns 13–14 (`open('/tmp/maps.json','w')` to keep maps for later; a tuple sort key
  missing its parentheses). Flash-Next control 524b1c3efa1c: 1 `open()` + 8 syntax in 200 turns.
  Opus 5.5 hit neither in 200.

Direct calls across all python-only builds (fix tail of 8fc1191a0c54 excluded):

| | turns | rate |
|---|---|---|
| fresh build, all turns | 13,416 | 0.71% |
| fresh build, first turn after a compaction | 467 | 2.36% |
| fresh build, 1–5 turns after a compaction | 2,032 | ~1.0% |
| fix/change, turns 0–5 | 284 | ~2.1% |
| fix/change, turns 11–50 | 1,063 | ~0.55% |

The rate is highest where the context holds few or no earlier `python` calls: the start of a fix
(one user message) and just after a compaction (history trimmed). Same system prompt (`build.txt`)
and same tool list for build, fix and change.

## Hypothesis

Put three harness-written rounds at the front of every build's transcript, as if the model had sent
them:

1. a direct `read_file` call → the harness's real no-`code` reply
2. a `python` program using `open()` → the harness's real `open()` refusal
3. a `python` program that works (`print([f["path"] for f in list_files()])`) → its real output

Kept through every compaction. The model then always sees what fails, how it is corrected, and what a
working call looks like, at exactly the points where it now drifts.

Measured over 5-turn branches:

- direct calls per turn at a **fix start**: ~2.1% → ≤0.7%
- direct calls per turn in the **5 turns after a compaction**: ~1.2% → ≤0.6%
- guards: files read and written per branch not lower than control; "no tool call" turns not
  higher

`open()` and syntax refusals happen when the model writes large programs, mid-build, not in the
first 5 turns. They are not measured here. Nick, 2026-10-20: acceptable if the prefix is shown
working on the 5-turn branches; the refusal rate is read from later full builds.

Idea failure: the direct-call rate does not drop, or rises (the failed examples prime the failure),
or the model spends branch turns on the prefix (re-listing files, asking about the failures) and the
guards fall.

## Setup

**The change**, applied in the branch's `install()` only (nothing in `src/`):

- after the request (`history[0]`), insert the three rounds above. Every tool reply is produced by
  the real code path: rounds 1–2 through `build_steps._apply` / `runner.run` on the real input,
  round 3 by running it, so the strings match the harness exactly.
- pin those rounds through compaction: `rounds()` treats everything after `history[0]` as
  trimmable, so `compact` must skip the first three rounds.
- the rounds are not steps: they do not count against `max_steps`, and the arm's transcript marks
  them as harness-written.

**Positions.** `lib.replay.branch.run(source_run, position, 5, build=…, install=…, restore=…)` with
`direct.install()` first, so turns go straight to the local engine instead of through the queue,
which is the only deviation from the prod build path.

- fix starts (position 0 of each fix build): 1629ea1ae380/8a22202c1e36,
  632bb49dbb5b/74264d3cf4bb, 8fc1191a0c54/414e264d4630, d0dc7c41c2d0/{c23286be4361, fd5333028570,
  4ef086d16a56, 0ad97e3d3c8b}
- post-compaction (first compaction of each build, `before_compaction=True` so the arm's own
  compaction runs): 1629ea1ae380@47, 22263c0d3c8b@26, 3170a8a2b4c3@45, 524b1c3efa1c@23,
  632bb49dbb5b@41, 8fc1191a0c54@33, d0dc7c41c2d0@40

Check each source is a Flash-Next build before the first run; the "basalt" served name also covers
the frontier-ceiling runs.

**Model.** Flash-Next IQ3_S on the 5090 (Basalt), served at the port `direct.install()` points to.
Stop llama-swap (:5001) first.

**Runs.**

1. single run: one branch per state with the prefix. Check the three rounds are in turn 0's prompt,
   still there after the arm's compaction, and not counted as steps.
2. battery: 200 branches × 5 turns per arm per state, spread evenly over the positions. Prefix arm
   and control arm on the same positions. Temperature 0.7, as in the build.

**Metric.** Per turn, from the arm's transcript: a tool reply containing "carried no `code`" is a
direct call. Files read and written come from `TurnRecord.reads` and the ledger.

Commands: TBD with the branch script, run from this folder with `PYTHONPATH=..`.

## Log

**2026-10-20, setup.** Positions no longer replay with real tools: a fix start checks out the
`built` commit taken just before the fix from `game.git` (0.0 s); a post-compaction world replays
with play/check_syntax stubbed (`positions.py`). Stubbed replay of all of 8fc1191a0c54's build 1:
5 s, game folder byte-identical to its `built` snapshot 0937a2a. `lib/replay` seeds neither
`design/` nor `docs/`; patched here only (`_seed_with_design`). Engine: llama-swap :5001,
`qwen3.8-flash-next-basalt`, reasoning xhigh. Compaction pinning not built yet; fix-start branches
never compact in 5 turns.

**2026-10-20, timing (control, 1 branch each).** Fix start 8fc1191a0c54/414e264d4630: 5 turns 5 s,
matching the real fix build's own turns 0–5 (52–173 tokens, 0.6–1.8 s). Post-compaction
524b1c3efa1c@23: 33 s, of which one 6K-token write took 29 s; 1 direct call at turn 27.

**2026-10-20, single run (seeded, 1 branch).** 1629ea1ae380/8a22202c1e36. The three rounds land
after the request as written, every reply the harness's real string; prompt 2407 vs 1888 tokens.
First real turn copied the seeded `open()`: `t = open("design/design.md").read() if False else
None`, refused; it used `read_file` from the next turn on. 0 direct calls. Works mechanically; the
priming risk is visible at n=1, so the battery counts refused programs per arm beside direct calls.

**2026-10-20, history check.** `open()` refusals on real Flash-Next fix builds, turns 0–5: 4 of 53
turns (7.5%), against 0.3% from turn 6 on and 0% on fresh-build turns 0–5. 27B: 0.5%. So a fix
start loses ~7.5% of its early turns to `open()` and ~2% to direct calls in production; the
whole-build averages in Purpose hid it.

**2026-10-20, fix-start battery.** 4 fix starts (1629ea1ae380/8a22202c1e36,
632bb49dbb5b/74264d3cf4bb, 8fc1191a0c54/414e264d4630, d0dc7c41c2d0/c23286be4361), 50 branches per
position per arm, 5 turns, arms alternating. `seeded-battery-1792475606/results.jsonl`.

| arm | branches | direct calls | branches with one | `open()` refused | branches with one | reads/branch |
|---|---|---|---|---|---|---|
| ctrl | 200 | 53 (5.3%/turn) | 37 | 95 (9.5%/turn) | 95 | 2.44 |
| seeded | 200 | 35 (3.5%/turn) | 33 | 83 (8.3%/turn) | 81 | 3.87 |

Branches with a direct call: Fisher p=0.69. With a refusal: p=0.19. Lost turns (direct + refused)
per branch 0.74 → 0.59, permutation p=0.06. Reads per branch +1.42, p<0.0001, up at every
position.

Per position the arm trades one failure for the other rather than removing both: d0dc7c41c2d0
direct 34 → 9 but refused 5 → 33; 632bb49dbb5b direct 5 → 10, refused 37 → 17; 8fc1191a0c54
refused 17 → 4, direct 12 → 11; 1629ea1ae380 refused 36 → 29, direct 2 → 5. Every refusal in both
arms was `open()`; no syntax errors at fix starts.

Read: the hypothesis (direct calls ~2.1% → ≤0.7%) is not met — 5.3% → 3.5%, not significant by
branch. The seeded rounds lower total lost turns about 20% (borderline) and the model reads more of
the code in its first 5 turns, the one clear effect. `open()` at a fix start is the larger target
(9.5%/turn here, 7.5% in prod) and the seeded `open()` example does not stop it. Verdict pending
the post-compaction battery.

**2026-10-20, post-compaction battery.** 7 positions (first compaction of each build, replayed
with stubbed play/check_syntax, `before_compaction=True` so the arm's own compaction runs first),
28–29 branches per position per arm, 5 turns. Seeded rounds pinned through the compaction
(`prefix.pin`; checked offline on all 7: rounds at [1:7], note at 7).
`seeded-pc-1792478004/results.jsonl`.

| arm | branches | direct calls | branches with one | refused | branches with one | reads/branch | write turns/branch |
|---|---|---|---|---|---|---|---|
| ctrl | 200 | 21 (2.1%/turn) | 18 | 42 (4.2%/turn) | 35 | 2.22 | 2.25 |
| seeded | 200 | 45 (4.5%/turn) | 36 | 31 (3.1%/turn) | 31 | 2.44 | 2.08 |

Branches with a direct call 18 → 36, Fisher p=0.012. Refused p=0.69. Lost turns per branch 0.32 →
0.38 (p=0.42); reads and writes unchanged (p=0.23, 0.30). Direct calls rose at 6 of 7 positions.
524b1c3efa1c@23 carries most of both arms' failures (ctrl 15 direct / 29 refused of 63 total).

Read: after a compaction the seeded rounds double direct calls. The rounds open with a direct
`read_file` call; mid-build, with the transcript trimmed, the model copies it. Same shape as the
single run's copied `open()`: failed examples in context get imitated.

**Verdict: idea failure for this arm.** Fix starts: −20% lost turns (p=0.06), +1.4 reads/branch
(p<0.0001), the failure kinds trading places by position. Post-compaction: direct calls doubled
(p=0.012). Across both states the seeded rounds remove no lost turns: 148+63 = 211 control vs
118+76 = 194 seeded in 2000 turns each.

Directions the data points at, none run: drop the two failing rounds and keep only the working
`python` round (the reads gain at fix starts may come from it, and it has no failure to copy);
target `open()` at fix starts directly (9.5%/turn here, the largest single loss), e.g. a fix
request that names `read_file`. Both are prompt changes, so each is its own arm.

**2026-10-20, correction: refusals were undercounted in every battery.** The per-branch counter
matched "Nothing ran", so it missed the import refusal ("…nothing in the program ran"). Recounted
from the transcripts, every lost-turn kind, fix starts, 200 branches each:

| arm | lost/branch | branches with a loss | direct | `open()` | import | syntax |
|---|---|---|---|---|---|---|
| ctrl | 0.84 | 125 | 53 | 92 | 21 | 3 |
| 3-round seed | 0.76 | 105 | 35 | 82 | 33 | 1 |
| list | 1.21 | 190 | 20 | 182 | 37 | 1 |
| list → read | 0.47 | 90 | 0 | 49 | 43 | 0 |
| read | 0.42 | 81 | 0 | 2 | 83 | 0 |
| open-shim: shim | 0.39 | 57 | 43 | 0 | 33 | 0 |
| open-shim: shim + read | 0.39 | 76 | 0 | 0 | 77 | 0 |
| open-shim: real files | 0.23 | 34 | 35 | 0 | 9 | 1 |

The read seed's "0.01 lost turns" was wrong: it is 0.42. It removes direct calls and `open()`, but
77 of its 83 import refusals are `import subprocess`, a dead import on line 1 of a program that
never uses it (`import re, subprocess` then `read_file` + `re` only). The static check refuses the
whole program for it. Still the best seed (0.84 → 0.42, p<0.0001), half of what was reported.
The post-compaction battery has the same undercount and is not recounted yet.

## Outcome

**2026-10-20, arm 2: one successful read (single run).** Nick: seed something that works instead. One
round after the request: `print(read_file("design/design.md", lines=100))`, answered by the real
turn machine, pinned through compaction like arm 1 (`prefix.seed_read`). First try was an
implementation failure: the seed indexed `["content"]`, but inside a program `read_file` returns
the text itself, so the seeded round showed a TypeError. Fixed. Rerun at 1629ea1ae380/8a22202c1e36:
the round shows design lines 1–100; prompt 4264 vs ctrl 1888 tokens. Turn 1 `list_files()`, turns
2–5 `read_file` over the code searching for the input's handler. 0 direct, 0 refused, 6 s.
Battery: read arm only, same positions and per-position counts as arm 1; control rows reused from
`seeded-battery-1792475606` and `seeded-pc-1792478004` (same engine, same worlds).

**2026-10-20, arm 3: one successful `list_files()` (single run).** Nick swapped arm 2 for this: a
listing is what a model would do first anyway, and costs less context than 100 design lines. Arm 2's
battery stopped at 53 fix-start branches (`seeded-battery-1792511226`, kept, not analysed). One
round after the request, `print(list_files())`, real reply, pinned through compaction
(`prefix.seed_list`). 1629ea1ae380/8a22202c1e36: prompt 3187 vs ctrl 1888 tokens. Turn 1 searched
the design with `open()`, refused; turns 2–5 `read_file`. 0 direct, 1 refused, 6 s. Battery: list
arm only, controls reused as for arm 2.

**2026-10-20, arm 3 fix-start battery.** 200 branches, same 4 fix starts, 50 each.
`seeded-battery-1792511566/results.jsonl`. Post-compaction leg not run (Nick: later).

| arm | branches | direct | branches with one | `open()` refused | branches with one | lost/branch | reads/branch |
|---|---|---|---|---|---|---|---|
| ctrl | 200 | 53 | 37 | 95 | 95 | 0.74 | 2.44 |
| list | 200 | 20 | 19 | 185 | 174 | 1.02 | 4.21 |
| read (arm 2, partial) | 53 | 0 | 0 | 0 | 0 | 0.00 | 3.58 |

List vs ctrl: branches with a direct call 37 → 19 (Fisher p=0.014), but branches with a refusal
95 → 174 (p<0.0001); lost turns per branch +0.28 (p=0.0002). Refusals rose at every position
(36→48, 37→48, 17→55, 5→34). The refused programs `open()` the very paths the listing showed
(`src/input.js` 62, `design/design.md` 57, `src/cards.js` 49): a file list with no read beside it
reads as a filesystem to open. Idea failure for arm 3.

Arm 2's 53 stopped branches (13–14 per position): 0 direct, 0 refused in 265 turns, against ctrl
37/200 and 95/200 branches (Fisher p=0.0001 and p<1e-12); reads/branch 3.58. The one seeded round
that shows `read_file` working removes both failures at fix starts. n=53 from a stopped run, so it
is a lead, not a result; arm 2 needs its full 200 and the post-compaction leg.

**2026-10-20, arm 4: `list_files()` then the 100-line design read (single run).** Nick: list →
read, the order a model would take. Two seeded rounds, arm 3's then arm 2's (`prefix.seed_list_read`).
1629ea1ae380/8a22202c1e36: prompt 5773 tokens; turns 1–5 all `read_file`, first one searching the
design with `read_file` + `re`. 0 direct, 0 refused, 6 s. Battery: fix starts only, 200 branches,
controls reused.

**2026-10-20, arm 4 fix-start battery.** 200 branches, 50 per fix start.
`seeded-battery-1792513050/results.jsonl`.

| arm | branches | direct | branches with one | refused | branches with one | lost/branch | reads/branch |
|---|---|---|---|---|---|---|---|
| ctrl | 200 | 53 | 37 | 95 | 95 | 0.74 | 2.44 |
| list (arm 3) | 200 | 20 | 19 | 185 | 174 | 1.02 | 4.21 |
| read (arm 2, partial) | 53 | 0 | 0 | 0 | 0 | 0.00 | 3.58 |
| list → read | 200 | 0 | 0 | 50 | 50 | 0.25 | 4.92 |

List → read vs ctrl: direct calls gone at every position (37 → 0 branches, p<1e-11); refused
branches 95 → 50 (p<0.0001); lost turns per branch 0.74 → 0.25, reads 2.44 → 4.92 (both p<0.0001).
Every refusal is `open('design/design.md')`, 46 of 50 on the first real turn, to search the whole
design after the seeded 100-line read. Arm 2's 53 branches had none (0/53 vs 50/200, p<0.0001), so
the read alone may beat list → read; that comparison waits on arm 2's full 200.

**2026-10-20, arm 2 fix-start battery, complete.** The stopped 53 (`seeded-battery-1792511226`)
plus the remaining 147 (`seeded-battery-1792515466`, started at index 53 so every position has 50).

| arm | branches | direct | branches with one | refused | branches with one | lost/branch | reads/branch |
|---|---|---|---|---|---|---|---|
| ctrl | 200 | 53 | 37 | 95 | 95 | 0.74 | 2.44 |
| list → read (arm 4) | 200 | 0 | 0 | 50 | 50 | 0.25 | 4.92 |
| read (arm 2) | 200 | 0 | 0 | 2 | 2 | 0.01 | 3.82 |

Read vs ctrl: branches with a direct call 37 → 0 (p<1e-11), with a refusal 95 → 2 (p<1e-31), lost
turns 0.74 → 0.01 and reads 2.44 → 3.82 per branch (both p<0.0001). Every position: direct 0,
refused ≤1 of 50. Read vs list → read: refusals 50 → 2 (p<1e-13); reads lower (4.92 → 3.82,
p<0.0001), because list → read's first turns search the whole design and the code tree.
Works at fix starts: one seeded `read_file` round removes ~99% of the lost turns. Post-compaction
leg not run yet (Nick: later).

**Verdict (wrap-up 2026-10-21).** Seeding works at fix starts; the best arm here (one design read)
cut lost turns 0.84 → 0.42 per branch, its residue a refused `import subprocess`. Carried into
labs/open-shim, where seeds plus real files plus a nudge shipped. docs/experiments.md, "seeded
opening rounds".
