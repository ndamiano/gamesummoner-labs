# Known holes in the CADENCE seed

The seed is `refine-passes/r0/DESIGN.md` at d0ee945. Every hole below is one that a build or a
refine pass on that seed actually hit. Score each one per arm, reading the questions files,
ANSWERS.md and the updated DESIGN.md:

- 0: no question touches it
- 1: a question surfaces it, but DESIGN.md does not settle it
- 2: DESIGN.md settles it with a decision a builder could implement without guessing

## Found by r1's design_refine (bd4f3bf, §14.2 and §14.1)

| # | Hole |
|---|---|
| A | Rate tiers unreachable: COMMIT_WINDOW 260 ms ends every burst before Normal (260-700 ms) or Careful (>700 ms) can be measured |
| B | Hold → Pivot and hold 2 s → Rest are the same gesture |
| C | Idle Brace re-fires forever: idling farms Guard and hands enemies free moves |
| D | Stepping into a monster, and Strike into a wall, are undefined |
| E | Guard is used three ways and never defined |
| F | "Costs 3 turns" is undefined where a turn is a commit |
| G | What presses past the top of the ladder do |
| H | Facing snaps to 45° in one place and to 4 directions in another |
| I | What happens to a press that arrives while a verb animates |
| J | Nothing says what a room is, or what platform and stack the game runs on |

## Found only by building and playing

| # | Hole | Where it showed |
|---|---|---|
| K | Hold "rotates facing continuously" at no stated rate, and nothing says what the player sees of the facing before release | r1 play: pivot lands on a facing that reads as random |
| L | Nothing requires every room's exit and enemies to be reachable from its entry | r0 build: stairs unreachable in four rooms, could not pass level 3 |

A-J are what r1's single refine pass already found, so they are r1's own score by
construction and only show whether the split loses ground. K and L are the test: no design
pass in refine-passes settled them.

Not scored: r1's rhythm "felt inconsistent". The seed already specifies a cadence meter tinted by
tier (§5, item 2). The likelier cause is r1's own fix for A, which takes the tier across bursts, so
one gesture can read differently depending on the one before it. Note whether an arm's fix for
A has the same effect.
