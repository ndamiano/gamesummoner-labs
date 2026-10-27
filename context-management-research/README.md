# low-impact compaction: fewer throwaway turns between the cut and the next change

Status: planned
Control: unchanged-harness branches, run to first change, from the same compaction positions the
arms use (see Setup). The 2026-09-08 replay nulls (docs/experiments.md:2093-2117, labs/replay). The Opus
re-read cycle in frontier-ceiling d086d499669b. Overlaps labs/compaction-floor (planned, keep ratio
and floor). This lab is about what survives the cut and what a read costs, not the ratio.

Research report: [reports/Low impact context compaction.md](reports/Low%20impact%20context%20compaction.md)

## Purpose

Quality is the goal. This lab serves a secondary one: build faster by wasting fewer turns, so that
quality work later iterates on quicker builds. It is the compaction half of that push; the other
half (labs/seeded-corrections, labs/open-shim) cuts harness errors. The bar: compaction should cost
the build less, ideally while raising quality, and never by lowering it. A lever that costs quality
goes.

The post-compaction re-read cycle is the largest measured waste in a build. In Opus build
d086d499669b, steps 76-200 were 114 reads, 3 writes and 15 compactions, about $12 of ~$22. On prod
Flash-Next, reading is 52% of generated tokens, and 77% of reads are of files already read
(labs/replay/README.md).

Five note-content attacks were null on the local 27B, and a sixth backfired:

- the fact block
- a rule
- no map
- the map alone
- bodies pasted into the note
- bodies as a synthetic `read_file` round (19 reads against a baseline of 16, the backfire)

A model-written summary (dsh arm) still re-read on 72 of 94 turns.

Seeding is a technique this lab can borrow, not a baseline it builds on. labs/seeded-corrections
showed that a harness-written round in the model's own format ("this is how to handle a read")
changes what the model does next. Its numbers measure harness errors at fix starts, not compaction,
and its quality verdict is still open.

Three facts about the current harness are levers no arm has touched:

1. `drop_read_only_rounds` deletes every read-only round at compaction, including the newest. The
   files the model was just looking at leave context the moment it resumes. Claude Code, qwen-code
   and OpenHands all keep or restore the recent working set.
2. The file-state block says a re-read "returns exactly what you were shown", but by then those
   bytes are no longer in context. There is no stub that fires when the bytes are still in context.
3. prompts/build.txt:34-36 tells the model "you will need to re-read".

The engineer's prefetch idea needs settling. JEV would pick the files the model is about to read and
read them for it. Inject-all already lost (on the 27B). Inject-only-what-it-will-read was never
tried.

## Hypothesis

The goal is not fewer reads. A read the model needs for its next change is fine. The goal is fewer
throwaway turns: turns after the cut that change nothing (re-reads of what it already had, listings,
syntax checks, plays, lost turns) before the model writes or edits a file.

The harness causes some of those turns. It deletes the working set at the cut, tells the model
nothing changed when the bytes are gone, and its prompt predicts a re-read. Fixing that, and making a
re-read of bytes still in context cost a line, should shorten the gap from the cut to the first
change. Prefetch beyond recency pays only if an oracle injection (exactly the files ctrl reads
before its first change) shortens that gap. If the oracle doesn't, no predictor can, and the JEV arm
does not run.

Measured per branch, against ctrl at the same positions:

- **non-changing turns before the first change.** Primary. A change is a turn whose program writes
  or edits a file. Every turn before it counts, including needed reads, because which reads were
  needed is only knowable from what the change used. Branches run until the first change, capped at
  25 turns; a branch that hits the cap counts as 25 and is reported separately. Fixed-length
  5-turn branches cannot measure this: writes within 5 turns are ~0.
- **needed vs throwaway reads, diagnostic.** A pre-change read is needed if the first change edits
  that file or the read's span is one the change depends on (judged by hand on the single first
  runs). This says whether an arm cut waste or cut needed reads that the change then got wrong.
- **lost turns** (direct calls, refusals), counted with open-shim's `lost.py`.
- **the first change itself.** Does the write apply, and does it touch the file ctrl's first change
  touched? An arm that reaches a change sooner by changing the wrong thing has failed.
- **read tokens brought in before the first change.** Secondary, for floor and next-compaction
  pressure.

Idea failure, written now:

- **Oracle arm.** Non-changing turns before the first change are not lower than ctrl's. Prefetch is
  dead, and so are the JEV arm and the restore half of the working-set arm.
- **Stub arm.** The model routes around the stub (`open()`, slicing, `list_files` sweeps) and the gap
  to the first change does not shrink.
- **Working-set arm.** The gap does not shrink, or the larger floor makes the next compaction come
  enough sooner to eat the saving. Turns to the next compaction is read off the same branches when
  they run past the first change.
- **Prompt-line arm.** The gap is within noise of ctrl.
- **Ranged-read seed.** The gap does not shrink, or the seed's shape degrades into failures.
- **JEV.** Precision@3 on pre-change reads not above the recency baseline by enough to pay for a
  warm card.
- **Any arm.** The first change applies less often, or lands on a different file than ctrl's.

## Setup

Model and card: local Flash-Next IQ3_S on the 5090, served by basalt, prod build path.

Positions are built in this lab from any previous run that compacted; where it came from does not
matter, since arm and ctrl branch from the same position and a compaction fix should help from
anywhere. Each one is a run's `turns.jsonl` cut at a real compaction: the history exactly as `compact()` returned
it, plus that run's on-disk game files at that turn. Real transcripts, real prompts, real design
chain, only the lever changed. Branch-world mechanics (restoring files, replaying from a turn) may be
copied from labs/seeded-corrections or labs/replay. Their arms and controls are not reused. The first
position should be one that compacted and then spent turns re-reading before its next write.
Candidate: 524b1c3efa1c at its first compaction (turn 23).

Seeded or injected rounds follow the pattern that worked in seeded-corrections:

- native tool-call format
- the program written the way the model writes it
- the reply produced by `build_steps._apply` on the real files
- well-formed ids
- pinned through compaction
- never a failure in the seed

Any wording the model sees (stub text, note text, prompt line) is itself the thing under test.

No full builds. Every arm is measured from frozen compaction positions taken from previous runs:
the transcript as it stood right after a real cut, branched forward with only the lever changed.

Arms, in run order. Each new arm runs ONCE first: one branch to first change at one position, to
prove it functions. Ctrl gets the same single run-to-change at that position first. Then a battery
over a handful of positions from different runs. There is no further new ctrl unless the
engine or the head moved.

1. **Oracle prefetch.** Single first run: the first position (see above).
   - Oracle set: the paths ctrl's run-to-change branches at that position read before their first
     change, kept if at least half the branches read them.
   - Delivery: one appended `print(read_file(p))` round per path with its real reply, after the
     compaction note.
   - Settles prefetch, and "telling the model it did it" with real bytes, on Flash-Next.
2. **Keep the working set.** No fabrication: the model's own rounds.
   - `compact()` stops dropping the newest read-only rounds.
   - It keeps them, newest first, up to a ~30K-token budget. That is the qwen-code 5 files / 5K /
     50K budget scaled to a 131K window, an extrapolation.
   - Variant: carry the last round's `reasoning_content` through the cut (thinking-on caveat,
     Complexity Trap).
   - If arm 1 passed, a restore variant re-reads the 5 most recent files fresh from disk, as Claude
     Code and qwen-code do.
3. **In-context read stub.**
   - `read_file` of a path whose current on-disk bytes (content hash, not our own write log) are
     already in the live transcript returns a one-line pointer instead of the body.
   - Any change on disk, or any compaction that removed those bytes, returns the real body.
   - Appended reply, so the prefix cost is zero.
4. **build.txt:34-36 line.**
   - (a) The re-read sentence removed, keeping "only print exactly what you need".
   - (b) Optional reword pointing at the code map's line ranges.
   - Prompt wording is its own experiment.
5. **Ranged-read precedent.** One seeded post-compaction round that reads a single declaration by
   the code map's line range (`read_file(p, offset=a, lines=n)`), with its real reply. Tests whether
   a narrow-read precedent gets the model to its first change in fewer turns.
6. **JEV next-read predictor.** Runs only if arm 1 passed.
   - (a) Offline, no build: label every post-compaction read in existing `turns.jsonl` /
     `reads.json`. Score JEV noul per file on the compacted state against three baselines:
     recency (last 5 read or edited), last written, and import neighbours from the code map.
     Report precision@3, recall@3, bytes covered, and JEV latency on a 40-60K-token state.
   - (b) If JEV beats recency, arm 1's delivery with JEV's top-k in place of the oracle.
   - JEV and Flash-Next do not share the 5090. Run one GPU queue at a time.
   - In prod this needs a warm decide card per build, or labs/jev-on-flash-next. That cost is part
     of the verdict.

Commands: not written yet. Arms live in this folder as `arms_<name>.py`, each an `install()` over
`build_steps` in the style of labs/seeded-corrections/prefix.py. The driver builds positions from
previous runs and runs each branch until its first write or edit (cap 25 turns), as
`python run_branches.py <arm> <per_position> [check]` from this folder. Results go to
`/var/tmp/context-management-research/<arm>-<ts>/results.jsonl`. Nothing goes in src/ until a
battery says so.

## Log

## Outcome
