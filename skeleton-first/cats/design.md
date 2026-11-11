# 0. CONCEPT

A tower defense where cats defend a fish market. The fish display is at the bottom of the screen; the shop's exterior, ocean and docks, is to the right; a path comes down to the fish, walled by crates and barrels that the cats sit on top of; mice and other vermin come down the path. The cats: a sleepy cat that wakes up every once in a while and does a lot of single-target damage to something on the path; one that pounces from afar; one that swipes from up close.

# 1. DECISIONS

Prod's decide step (JEV) on the ask, as the control was decided:

dimension: 2d
camera: top-down
time model: real-time with pause
movement model: no movement, cursor only
session shape: a sequence of levels
failure: restart the level
tone: silly
size: a handful of levels, under 30 minutes
win/lose: none
core mechanics: combat, building, waves, economy
supporting mechanics: abilities, scoring
extra mechanics: none
art style: flat vector: clean flat shapes, solid colours, crisp edges
palette: saturated: bright, strong colours
typography: hand-lettered: drawn, irregular letters
music: chiptune: retro console bleeps
sound effects style: retro bleeps: synthesized chip sounds
screens: title, pause, settings, level select, high scores
hud: health, score, wave number, currency
effects: particles, hit flash
accessibility: colour-blind safe palette, reduced motion, difficulty options

# 2. HOW IT IS BUILT

The way a person would build it with an AI: a crappy framework first, with placeholder shapes, until it plays; then the concept's things replace the placeholders one at a time; then the UI. A thing from the concept only ever replaces a placeholder. It never adds a rule, a system or a screen that the framework did not already have. A tower defense is a path, things that walk it, things placed beside it that hit them, health, death, gold and lives; nothing in the concept changes what a tower defense is. Pick the numbers yourself and keep them plain.
