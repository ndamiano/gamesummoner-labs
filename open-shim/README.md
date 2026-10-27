# open-shim

Status: done
Control: `labs/seeded-corrections` fix-start batteries (ctrl `seeded-battery-1792475606`, read arm
`seeded-battery-1792511226` + its remainder), same positions and engine.

## Purpose

Flash-Next writes `open(path).read()` inside `python` programs. The static check refuses the whole
program ("open() is not available here. Nothing ran."), so the turn is lost.

- Real Flash-Next fix builds, turns 0–5: 4 of 53 turns (7.5%) refused for `open()`; 0.3% later in
  a build; 27B 0.5%.
- `labs/seeded-corrections` fix-start control: 95 `open()` refusals in 1000 turns (9.5%/turn), 95 of
  200 branches. Every refusal at fix starts was `open()`, none were syntax.
- Seeding a `list_files()` round there pushed it to 174 of 200 branches; list → read left 50, all
  `open('design/design.md')` to search the whole design.

The model's intent is plain: read that file. The tools already do it.

## Hypothesis

Give programs an `open()` whose file object reads through `read_file` and writes through
`write_file` on close. Every path still goes through the tools' own checks; seccomp is untouched.
Paths the tools reject raise ordinary Python errors (`FileNotFoundError`, `PermissionError`) that
the program can catch or the model reads in the traceback.

Measured over 5-turn fix-start branches, 200 per arm:

- `open()` refusals: ~9.5%/turn → 0 (by construction); the number that matters is lost turns per
  branch, 0.74 → ≤ the direct-call share alone (~0.27)
- guards: reads per branch not lower; programs that raise from the shim (outside paths, binary
  mode) counted and read by hand; no rise in direct calls
- stacked with the `seeded-corrections` read seed: lost turns ≈ 0

Idea failure: the shim's errors turn into a new loop (the model keeps opening `/tmp/...` or binary
files), or it writes through `open(..., 'w')` in ways that clobber files `write_file` calls would
not have.

## Setup

**The change**, lab-only (`openshim.py`, nothing in `src/`): `install()` drops `open` from
`runner.BANNED_CALLS`, puts a file-object class named `open` in front of each program, checks only
the model's own code, and shifts traceback line numbers back so the model sees its own lines. In
prod the class would sit in `pyexec/child.py` beside the tool stubs, with no shift.

**Positions, model, metric**: as `labs/seeded-corrections` fix starts (Flash-Next IQ3_S on the 5090
via llama-swap :5001, 4 fix starts, 5 turns, temperature as the build). Arms: shim, shim + read
seed. Controls reused.

**Arm 2, real files (planned, after arm 1's battery).** Nick, 2026-10-20: the goal is a model free
to use what it already knows, and result quality outranks our tooling — a tool-stack rewrite is
fine if games get better. So the second arm is real Python file access, not a shim: the child
process confined by Landlock to the game folder (kernel-enforced at path resolution, symlinks and
`..` included; this box's kernel has it, prod's kernel and Docker profile unchecked), cwd = the game
folder, `open`, `os`, `pathlib`, `glob` allowed, `os` process/network calls still blocked by
seccomp. What it gives up and must be rebuilt if it wins: the read record `edit_file`'s freshness
check uses, the reads the compaction re-read cycle uses, the "what the program called" ledger.
Measured on lost turns at the same fix starts, then on full builds, since 5-turn branches cannot
show game quality: one full build per arm first, then a battery Nick judges by playing.

Commands, from this folder: `PYTHONPATH=.. python3 check_shim.py` (offline, no GPU);
`PYTHONPATH=.. python3 run_battery.py <per_arm> [shim,shim+read]`.

## Log

**2026-10-20, offline check (`check_shim.py`, no GPU).** Real tools on 1629ea1ae380's fix-start
world, 12 programs. `open(p).read()`, `with` + iteration, `readlines()`, write without close,
append: all right, each showing up in the ledger as the `read_file`/`write_file` it made. Missing
file raises `FileNotFoundError` (catchable); binary mode raises `PermissionError`; the model's own
traceback lines come out unshifted; `eval` and dunders still refused. First version had one bug: a
write to an outside path with no close failed silently, because `__del__` swallowed the error.
Fixed by checking the path through `read_file` on open: `open("/tmp/maps.json", "w")` now raises
`PermissionError: ValueError: path escapes the project directory`. Side effect: opening a new file
for writing shows a failed `read_file` in the ledger. Works; single GPU run next.

**2026-10-20, real-files arm built, offline check (`check_realfs.py`, no GPU).** `realchild.py`:
pyexec's child with Landlock (ABI 6 here) granting the game folder read/write/make/remove and
Python's library read-only, cwd = game folder, seccomp's deny list minus the path calls Landlock
now governs (open*, unlink*, rename*, mkdir*, rmdir, creat, truncate); link, symlink, chmod,
process, network and mount calls still denied. `realfs.py` routes the lab's programs to it and adds
os, pathlib, glob, shutil, io, fnmatch to the importable modules; `open` unbanned. Prompt
unchanged. 9 allowed programs all ran (`open`, `pathlib` glob, `os.walk`, `glob`, `json.load`,
mkdir + write + rmtree, binary read, tool calls, lazy stdlib import). 13 escapes all failed:
`/etc/passwd`, `../build_state.json`, `~/.anthropic_key`, `os.listdir("/")`, symlink and hard
link out, write to `/tmp`, `os.system` (no process: clone denied), fork, subprocess/socket
imports, `/proc/self/environ`, repo source. Local trap: `/home` is eCryptfs, where Landlock denies
every directory listing (readdir goes through the encrypted lower tree); file reads still work.
Prod disks are not eCryptfs; the lab's real-arm worlds live on ext4 under `/var/tmp/open-shim`.
Single GPU run next, then 200 × 5 turns at the fix starts to look for new failure modes before any
full build.

**2026-10-20, single run (real, 1 branch).** 1629ea1ae380/8a22202c1e36: 0 direct, 0 refused, 9 s.
The model used the tools only (`list_files`, `read_file` + `re`); no `open`, `os` or `pathlib`,
which build.txt never mentions. Works; battery next.

**2026-10-20, shim fix-start battery.** 200 branches per arm, 50 per fix start, alternating.
`open-shim-1792516467/results.jsonl`. Reads recounted from transcripts with `open(` included.

| arm | branches | direct | branches with one | refused | branches with one | lost/branch | reads/branch |
|---|---|---|---|---|---|---|---|
| ctrl (seeded-corrections) | 200 | 53 | 37 | 95 | 95 | 0.74 | 2.44 |
| read seed (seeded-corrections) | 200 | 0 | 0 | 2 | 2 | 0.01 | 3.82 |
| shim | 200 | 43 | 33 | 2 | 2 | 0.23 | 3.17 |
| shim + read seed | 200 | 0 | 0 | 0 | 0 | 0.00 | 3.90 |

Shim vs ctrl: refused branches 95 → 2 (p<1e-31), lost turns 0.74 → 0.23 and reads 2.44 → 3.17 per
branch (both p<0.0001); direct calls unchanged (37 → 33 branches, p=0.69). Given a working `open`,
the model used it in 100 of 200 branches (358 calls): half of all fix-start branches want it.
Program errors match ctrl (NameError 25 vs 25): the shim's own were 8 `FileNotFoundError` on
guessed paths (`js/game.js`), each followed by a listing, and 4 `PermissionError` carrying
read_file's vendored-renderer note. No loops, no writes outside. Shim + read seed vs read seed
alone: identical (0/0 vs 0/2; p≥0.5 on every metric); with the read seed in context the model
opened files in only 8 branches. Works: the shim removes the `open()` refusals and nothing else;
the read seed removes both failures and makes the shim nearly unused at fix starts.

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

**2026-10-20, real-files fix-start battery.** 200 branches, 50 per fix start.
`/var/tmp/open-shim/open-shim-1792518903/results.jsonl` (ext4, see the eCryptfs note). Recounted
as in the correction above: 0.23 lost turns per branch (ctrl 0.84, shim 0.39; real vs shim
p<0.0001 on branches with a loss), 34 of 200 branches with any loss. Direct calls 35 (34 at
d0dc7c41c2d0, as ctrl's 34 there), import refusals 9 (`subprocess` 7, `pickle` 2), syntax 1.
What the model reached for: `open` in 98 branches, `os` 15, `glob` 4, `pathlib` 2. No program hit
Landlock (no PermissionError, no OSError), no escape attempt, one write via `open(…, 'w')` (to a
guessed wrong path, FileNotFoundError on the read before it). Errors otherwise as ctrl (NameError
33 vs 25, FileNotFoundError 5, TypeError 2). No new failure mode at 5 turns: the
real-files arm is the lowest-loss arm measured. Full builds next.

**2026-10-20, arm real + list/read in one program (single run).** Nick: real files plus one seeded
program that does both `print(list_files())` and `print(read_file("design/design.md", lines=100))`
(`run_battery.py` arm `real+listread1`). 1629ea1ae380/8a22202c1e36: prompt 5724 tokens; turns 1–5
all `read_file` + `re`. 0 lost turns, 6 s. Works; battery next, 200 at the fix starts, lost turns
counted with `lost.py`'s full set of refusal kinds.

**2026-10-20, arm real + list/read + nudge (single run).** Nick: after the seeded program, a user
message "Good, continue, and please do not use the subprocess module." (arm
`real+listread1+nudge`), aimed at the dead `import subprocess` that is real+listread1's only loss
so far (17 of 63 branches). 1629ea1ae380/8a22202c1e36: message lands after the seeded tool reply;
turns 1–5 `read_file` + `re`, no subprocess. 0 lost turns, 13 s. Works; battery after
real+listread1's.

**2026-10-20, real + list/read in one program, fix-start battery.** 200 branches,
`/var/tmp/open-shim/open-shim-1792520789`. Lost turns 0.29 per branch, 58 of 200 branches (ctrl
0.84 / 125; real alone 0.23 / 34). Kinds: `import subprocess` 57, syntax 1; direct calls 0. vs
real alone: lost turns p=0.25, branches with a loss 34 → 58 (p=0.006). The seed trades real's 35
direct calls for 57 dead `subprocess` imports, the same trade as the read seed without real files
(77). Not better than real alone; the nudge arm targets exactly the remaining loss.

**2026-10-20, real + list/read + nudge, fix-start battery.** 200 branches, 50 per position,
`/var/tmp/open-shim/open-shim-1792522320`.

| arm | lost/branch | branches with a loss | kinds |
|---|---|---|---|
| ctrl | 0.85 | 125 | direct 53, `open()` 92, import 21, syntax 3 |
| real | 0.23 | 34 | direct 35, import 9, syntax 1 |
| real + list/read | 0.29 | 58 | `import subprocess` 57, syntax 1 |
| real + list/read + nudge | 0.07 | 13 | `import subprocess` 13 |

Nudge vs real alone: lost turns 0.23 → 0.07 (p=0.0003), branches with a loss 34 → 13 (p=0.002);
vs ctrl p<1e-34. Reads 6.3 per branch (`read_file` + `open`). Errors otherwise NameError 17 (ctrl
25) and 2 PermissionError, both `open('/dev/null')` from a model probing whether `open` exists
(it said so in its reasoning: "suggesting there IS an open() but restricted"), followed straight by
`read_file`. No mention of the subprocess message backfiring: 13 of 200 branches still import it,
down from 57. Works at fix starts: lowest loss of every arm, ~92% fewer lost turns than ctrl. Not
measured: post-compaction, and whether any of it changes the game.

**2026-10-20, reads and writes per branch, all fix-start arms** (`rw.py`, programs that ran only).
Reads per branch: ctrl 2.77, read 4.27, shim 3.33, real 3.62, real + list/read 6.17, + nudge 6.21.
Writes in 5 turns are near zero everywhere (ctrl 2 branches / 5 calls, real 6 / 23, seeded arms
0–1): a fix start spends its first 5 turns reading. Whether the seeded arms' extra reading is good
needs full builds.

**2026-10-20, arm real + list/read + failed subprocess + nudge (single run).** Nick: also seed the
failure the nudge answers. Second seeded program `import re, subprocess` +
`print(read_file("index.html", lines=20))`, answered by the real refusal under the real-files
check (module list includes os, pathlib, glob …), then the nudge (arm
`real+listread1+subfail+nudge`). Risk known from arm 1 of seeded-corrections: a seeded failure got
copied. 1629ea1ae380/8a22202c1e36: turns 1–5 `read_file` + `re`, 0 lost, 6 s. Works; battery next.

**2026-10-20, real + list/read + failed subprocess + nudge, fix-start battery.** 200 branches,
`/var/tmp/open-shim/open-shim-1792524136`. Lost turns 0.03 per branch, 6 of 200 branches (nudge
arm 0.065 / 13, real 0.23 / 34, ctrl 0.85 / 125). vs nudge arm: p=0.15 lost turns, p=0.16
branches, so not separable at n=200; vs real and ctrl p<1e-5. Kinds: `import subprocess` 0 (13
in the nudge arm), `__import__('re')` refused 4, syntax 1, direct 1. The `__import__` refusals are
new (0 in every other arm): an inline import inside a search loop, as if the model now avoids
`import` lines. The seeded failure was not copied. Reads 6.42 per branch, writes 2 branches.
Errors NameError 28 (ctrl 25), IndexError 1. Works: lowest loss measured; `__import__` is the next
removable refusal (it is banned as a call, though `re` itself is allowed).

**2026-10-20, full-build setup.** Nick: take real + list/read + failed subprocess + nudge into a full
build; control is an existing game, 1629ea1ae380 (hiragana, local Basalt Flash-Next IQ3_S,
2026-10-19: build 1 hit the 200-step cap, fix build 8a22202c1e36 passed in 93, both gates clean).
A full control-vs-arm pair only once this build holds up against it. `arm.py` installs the arm in
the control plane process (turns run there): real files for every program, the two seeded programs
and the nudge at every build start (build and fix), pinned right after the request through every
compaction. `serve.py` runs `run.py` with it installed; `fullbuild.sh` is tests-in-files' build.sh
with the run directory moved to ext4 (`/var/tmp/open-shim/runs/<id>`, symlinked back into runs).
Offline check (`check_arm.py`, 1629ea1ae380@47): seeded head lands after the request; after a
real compaction all 5 arm messages are still at [1:6], the note at 6. Known differences from the
control: d05a659 (failed tool calls carry their fields, so play() errors now reach the model) and
9e1dc40 (reaper fix) landed after it ran.

**2026-10-20 15:56 EDT, full build 1, two false starts.** Old control plane (pid 2500252, started
10-19 22:26, before 9e1dc40) stopped with Nick's OK; `serve.py` + `local_gpu.py auto` (llama-swap
:5001 Basalt) in its place. Run a64de75966c0: no seed, because `build_chain.kickoff` runs the
first step in fullbuild.sh's own process, which did not have the arm; stopped at step 7. Run
7cdbb5ac64ed: arm installed in the script, but its `sys.path` held `src` only as `''`, which the
runner drops from the child's PYTHONPATH, so the first seeded program showed "the session could
not be started"; stopped at step 6. Both implementation failures, fixed in fullbuild.sh.
Run 42427fef48dd: seed, failed-subprocess refusal and nudge land after the request, no child
errors. Building. Unrelated: the reaper re-advances game 33b7c5a6bb6d every tick (status building
in the db, no run directory); harmless, pre-existing.

**2026-10-20, full build 1 result: run 42427fef48dd.** One build, 9686cec4a20d, to the 200-step cap
(as ctrl's build 1), 6 compactions, seeded head pinned through all of them. Lost turns 3 of 200
(`import pickle`, `import builtins`, `exec()`) vs ctrl build 1's 10 (6 direct, 3 syntax, 1
`exec()`). Error gate and play gate both passed on round 0, so no fix build; ctrl needed fix build
8a22202c1e36 (93 turns) for a dead room-card click before its gates passed. Totals: arm 200 turns,
22.2 inference-min, 265K generated tokens, 2010 s wall; ctrl 293 turns, 22.4 min, 272K tokens.
Play gate's read: every exercised input worked (title → room 1, WASD/arrows/on-screen D-pad, Space
on a seal opens a four-choice kana quiz, correct answer opens the screen and scores); "unusually
legible" as a teaching game. n=1, same design: holds at least ~= ctrl, the bar for a full
ctrl-vs-arm pair. Nick to play both.

**2026-10-20, Nick on full build 1.** "They are approximately even, yeah. Interesting that the arm
didn't need a fix, as it was actually working." The control used generated assets, the arm did
not. Verdict: holds ~= ctrl, so the full pair runs.

**2026-10-20 17:00 EDT, full-build battery started.** 6 designs, one ctrl build and one arm build
each, the pair side by side, next pair after both settle (fix builds included):
1629ea1ae380 hiragana, 22263c0d3c8b frog platformer, 3170a8a2b4c3 frogs eating bugs, 524b1c3efa1c
wizard-cat deckbuilder, d0dc7c41c2d0 monster collecting, c93a1320cbd3 3D kart racing (632bb49dbb5b
dropped as a second "frogs eating bugs"). `arm.py` now switches per run: a run directory under
`/var/tmp/open-shim/runs` gets the arm, any other the stock path, with the per-program switch
thread-local (checked offline: both at once on two threads, arm `open` + `os` ran, ctrl got the
stock `os` refusal). One `serve.py` control plane for both arms; ctrl via tests-in-files/build.sh,
arm via fullbuild.sh; driver `battery_full.py`, index `/var/tmp/open-shim/battery/pairs.jsonl`.
Pair 1: ctrl 5870978265fe (stock head), arm 34bfd0509e59 (seeded head).

**2026-10-20 18:41, battery pair 1 (1629ea1ae380 hiragana) settled.** Both one build, 200 turns,
error and play gates round 0, no fix build. Lost turns: ctrl 5870978265fe 10 (direct 5, `open()`
2, imports 2, `exec` 1); arm 34bfd0509e59 7 (direct 3, other refusals 2, import 1, syntax 1). The
pair lost ~25 min to the basalt-batch pauses. Pair 2 (22263c0d3c8b frog platformer): ctrl
33a565da9ca8, arm 61376284936b.

**2026-10-20 ~19:35, battery pair 2 lost to host RAM; battery paused.** Both pair-2 builds
(ctrl 33a565da9ca8 at step 166, arm 61376284936b at 193) ended "stalled: 4 turns the server could
not read": Basalt refused every turn with `RAM low (2941 MiB free < 3192 MiB guard): request
stopped; lower --resident-budget-gib`. Infrastructure, both arms alike; pair 2 does not count and
is continued (below). Then paused for Nick (games for a couple of hours): local_gpu auto stopped, llama-swap
models unloaded (RAM 51 GB available after), driver stopped before pair 3 started. serve.py
control plane left up. Resume: local_gpu auto, then
`battery_full.py 22263c0d3c8b 3170a8a2b4c3 524b1c3efa1c d0dc7c41c2d0 c93a1320cbd3`.

**2026-10-20, pair 2 continued instead of rerun (Nick).** `continue_build.py`: drops each build's
trailing "inference server could not read" messages (4 each), gives the 4 steps back, sets the
cursor to phase build, the builds row to running and the game to building, then
`build_chain.resume`. Both arms treated alike; the refused turns stay in turns.jsonl. To run on
resume, before the driver goes on with pairs 3–6.

**2026-10-20 20:17, battery pair 2 (22263c0d3c8b frog platformer) settled, after continuing.**
Both continued cleanly (ctrl back at 162, arm at 189). Both failed the play gate once and passed
after one fix build. Ctrl 33a565da9ca8: Space did not make the frog hop; fix 60 turns; 264 turns
in all, 9 lost (direct 4, syntax 2, `open()` 2, `import subprocess` 1). Arm 61376284936b: no frog
sprite drawn (player simulated, invisible); fix 33 turns; 237 turns in all, 2 lost (direct 2).
Paused again after it for Nick (local_gpu stopped, models unloaded). Pairs 3–6 left.

**2026-10-20 22:17, battery pair 3 (3170a8a2b4c3 frogs eating bugs) settled.** Resumed 21:41 on
the paused battery (`battery_full.py 3170a8a2b4c3 524b1c3efa1c d0dc7c41c2d0 c93a1320cbd3`).
Ctrl 9c4ac408da27: 2 builds, 135 turns, 5 lost (direct 5); play gate failed once (Space before
Enter did nothing, no start prompt), fixed in 25 turns. Arm 7143e3953cfe: 1 build, 73 turns, 1 lost
(direct 1); passed both gates round 0. Both built. Running total after 3 pairs: arm 10 lost, ctrl
24; fix builds arm 1, ctrl 2.

**2026-10-20 23:30, battery pair 4 (524b1c3efa1c wizard-cat deckbuilder) settled.** Both one
build, 200 turns (cap), passed both gates round 0, built. Ctrl d188fbe6b5c2: 8 lost (direct 2,
syntax 1, imports struct/pickle/posixpath/subprocess/os 1 each). Arm 4d1ac4cae527: 5 lost (direct
1, `exec()` refused 2, imports struct/fontTools 1 each). The arm's `exec()` refusal still says
"Files are reached only through read_file, write_file and edit_file", which is false under the
arm. Running total after 4 pairs: arm 15 lost, ctrl 32; arm fewer in all 4.

**2026-10-20, cap check (Nick: worried about quality change).** First builds of pairs 1, 2 and 4
all ran to the 200-turn cap on both sides; none called `done()`. Only pair 3 finished under it
(ctrl 107, arm 73). At the cap, tiers reported done were 1–2 of the design's tiers on every
capped build except pair 2's arm (all, every definition-of-done box ticked, still no `done()`).
About two thirds of turns write nothing (read, play, check syntax), spread through the build: the
first 8 turns after a compaction are ~70% no-write against ~65% elsewhere. Capped builds compacted
5–7 times, pair 3 1–2. So in capped pairs the arms compare progress at equal budget, not finished
games; why pair 3 finishes and the rest do not is open, outside this lab.

**2026-10-20, Nick played pairs 1–4 blind** (A/B shuffled per pair, served on 127.0.0.1:88N1/88N2).
Hiragana: "B is definitely superior" (B = ctrl 5870978265fe). Frog platformer: prefers A,
"approximately equal" (A = ctrl 33a565da9ca8). Frogs eating bugs: "both about the same", leans A
(A = ctrl 9c4ac408da27; the arm stopped at 73 turns to its 107). Wizard-cat deckbuilder: "both are
borked, but B seems a bit better" (B = arm 4d1ac4cae527). Preference ctrl 3, arm 1; one clear
(ctrl), three near-ties. The arm's fewer lost turns (15 vs 32) bought no visible quality.

**2026-10-20 ~23:55, battery stopped after pair 5 (Nick).** On hiragana: "I probably graded the
arm a little too harshly... The graphics in B were much much better, which immediately caused it to
rank higher." On the rest: possibly "luck of the draw"; with identical designs the content is near
identical, so quality is hard to tell apart. Driver killed during pair 5 (d0dc7c41c2d0, ctrl
c5dbc1a1da07, arm f6be70fbc824); its builds run out on serve.py, then plain run.py goes back. Pair
6 (c93a1320cbd3 3D kart) not run. Next problem taken up in labs/turn-cap.

**2026-10-21, Nick on adoption.** "Unless the last build is significantly worse on open-shim, we're
pushing it." The call waits on his blind play of pair 5; labs/section-budget then runs on the
prod harness with open-shim in it.

**2026-10-21 ~00:50, battery pair 5 (d0dc7c41c2d0 monster collecting) settled; battery done at 5
pairs.** Both first builds capped at 200. Ctrl c5dbc1a1da07: 3 builds, 276 turns, 16 lost (direct
10, `import subprocess` 3, syntax 2, `open()` 1); play gate failed twice (Enter on the title did
not start a run; then an Escape/map report), fixes 38 + 38 turns. Arm f6be70fbc824: 2 builds, 253
turns, 7 lost (direct 4, syntax 3); play gate failed once (Tab opened the region map, not the
GLOOPDEX), fix 53 turns. Both built; both passed the error gate round 0. Totals over 5 pairs: lost
arm 22, ctrl 48, fewer on the arm in all 5; fix builds arm 2, ctrl 4. serve.py stopped, plain
run.py back. Served blind for Nick on 127.0.0.1:8861/8862.

**2026-10-21, Nick played pair 5 blind.** "A works better than B, both are borked" (A = arm
f6be70fbc824). Blind preference over 5 pairs: ctrl 3 (hiragana clear, frog platformer and frogs
eating bugs near ties), arm 2 (wizard-cat and monster collecting, both games broken on both sides).
Not significantly worse, so by Nick's rule open-shim goes to prod.

## Outcome

**2026-10-20, single run (shim, 1 branch).** 1629ea1ae380/8a22202c1e36. Turns 1–2 `list_files()`,
turns 3–5 `open('design/design.md').read()` (whole design, then regex over it) and
`open('js/ui.js').read()`: all ran, 0 refused, 0 direct, 5 s. The branch metrics count reads by
regex over `read_file(` in the program, so a shim turn shows no tools; reads per branch for these
arms are recounted from the transcripts with `open(` included. Works; battery next, 200 per arm,
fix starts only.

**Verdict (wrap-up 2026-10-21).** Works: lost turns 22 vs 48 over 5 full-build pairs, fewer in
every pair, quality a wash on blind play (3–2 ctrl). Shipped as tested, real-files child + `open()`
+ seeded opening + nudge, into src/ (uncommitted at wrap-up). docs/experiments.md, "real files in
the sandbox".
