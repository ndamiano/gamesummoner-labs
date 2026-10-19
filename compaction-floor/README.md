# the post-compaction floor

Status: planned
Control: frontier-ceiling Opus 5.5 build d086d499669b (compactions at 15/25/31/60/79, then every 8–21
turns to 190), spec-skeleton collector c6b51ec35d89 (compactions at 43/83/144/186, 39 design
re-reads after 83), the 2026-09-06 re-read-cycle fix (built, unmeasured)

## Purpose

After a compaction a build resumes at ~60K tokens on a 131K window: `_COMPACT_KEEP` 0.33 keeps
the newest body of every game file, and the game is 130–150K chars by then. Each compaction is
followed by re-reads of the spec and the files, and the collector run spent turns 96–199 that
way. Bigger games compact more often and re-read more.

The Opus 5.5 wizard-cat build (labs/frontier-ceiling, scored 9) is the sharpest case. Tier 1 was
done by turn 75. Turns 1–79: 5 compactions, 63 read_file calls, 47 writes/edits. Turns 80–200: 10
compactions, 175 read_file calls, 2 writes/edits, ~$12 of its ~$22. Each compaction resumed at
42–84K prompt tokens (mean ~62K) on the 131K window, with 158 KB of game JavaScript and a 54 KB
spec on disk, so re-reading what it needed refilled the window in ~10 turns and compacted again.
The same cycle caps every model whose files outgrow the window; it is the cost lever between the
Opus game and a sellable price.

## Hypothesis

A lower keep ratio, or bodies replaced by a file listing plus per-file line counts, drops the
floor and the re-read count without costing the builder what it needs. Measured: turns between
compactions, re-reads per compaction, turns to done, on the collector and platformer specs. Idea
failure: the builder re-reads everything it lost anyway, and the total is the same or worse.

## Setup

Test locally on Flash-Next (basalt on the 5090, $0 API; it hits the same cycle and so does prod),
then confirm the best arm once on a hosted model.

## Log

## Outcome
