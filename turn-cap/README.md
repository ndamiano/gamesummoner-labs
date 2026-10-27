# turn-cap: builds spend the 200 turns and stop mid-design

Status: planned
Control: labs/open-shim full-build battery pairs 1–4 (2026-10-20), ctrl and arm builds below.

## Purpose

Most builds end at the 200-turn cap, not at `done()`. In the open-shim battery, first builds of
pairs 1, 2 and 4 capped on both sides (6 of 8); none of the six called `done()`. At the cap they
had reported tiers 1–2 of the design's tiers, except pair 2's arm (every tier and every definition
of done box, still no `done()`). Only pair 3 finished (ctrl 107 turns, arm 73). A capped game is
whatever the first tier or two came to, so the cap sets how much of the design reaches the player.
Nick: "the other thing that is a big problem, which is that it takes a ton of steps and then hits
the limit."

First build only, turns classified by what the program did (write beats play beats read):

| run | turns | read | write | play | reads | re-reads |
|---|---|---|---|---|---|---|
| 5870978265fe p1 ctrl | 200 | 38% | 34% | 21% | 189 | 82% |
| 34bfd0509e59 p1 arm | 200 | 38% | 30% | 23% | 174 | 80% |
| 33a565da9ca8 p2 ctrl | 204 | 36% | 30% | 28% | 91 | 79% |
| 61376284936b p2 arm | 204 | 43% | 36% | 16% | 195 | 86% |
| d188fbe6b5c2 p4 ctrl | 200 | 49% | 34% | 7% | 161 | 73% |
| 4d1ac4cae527 p4 arm | 200 | 41% | 38% | 15% | 131 | 70% |
| 9c4ac408da27 p3 ctrl (done) | 107 | 25% | 33% | 33% | 30 | 86% |
| 7143e3953cfe p3 arm (done) | 73 | 23% | 30% | 42% | 18 | 72% |

Re-reads are reads of a path already read in that build. `design/design.md` is the most read file
in every capped build (29–32 reads; the designs are 63–72 KB, definition of done lists 35–67
rows), then the game's biggest source files and, in p1 ctrl, `tests/helpers.js` (45). Capped
builds compacted 5–7 times, the finishers 1–2. The first 8 turns after a compaction are ~70%
no-write against ~65% elsewhere, so the reading is steady through the build, not a burst after
each cut.

Related: labs/compaction-floor and labs/context-management-research (planned) attack re-reads
after compaction; labs/tests-in-files (done) found one-probe-per-play() turns; labs/dod-checkoff
(done) found row-by-row definition of done walks at the cap.

## Hypothesis

Not written yet. First lever taken: labs/section-budget (one build-order step per fresh agent,
25 turns each). Nick passed on a raised cap: "it might finish, but I'm not sold about that being
super relevant."

## Setup

## Log

## Outcome
