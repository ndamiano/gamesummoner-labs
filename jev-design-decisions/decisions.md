# Where JEV could decide

Working list of the decisions it takes to make a game, to mark up together. Nothing here is ruled
in or out yet. The starting point is what our three design prompts
(`src/maestro/codegen/prompts/design/{gameplay,visual,engineering}.txt`) already make the
designers decide, plus additions from the 2026-10-14 conversation. Checked for gaps against the
integrator's required sections (`integrate.txt`) and the section headings of the 35 local designs
under `~/output/runs`.

## What the probes showed

- A closed list works: 2D/3D agreed with what we built on 87/95 real prompts, and every miss was
  JEV choosing 3D where we built 2D on a prompt that left the dimension open.
- JEV cannot tell when the right answer is missing from the list. With neon removed for Neon Beat,
  "something else" / "something not listed" got 0.6-3%, whatever the wording. It only escapes when
  every listed option is plainly wrong (2+2 over 1/2/3: ~80%, still 18-20% on "2").
- So every decision below needs a list that already holds the right answer.

## Question shapes

- **one**: `choice`, pick one. Probabilities sum to 100%, so only one option can clear 60%.
- **many**: yes/no (`noul`) per item, for picking several (enemies, mechanics). "Use any above
  60%" works in this shape.
- **score**: 0-5 per item, for ranking or bucketing.

Option sources: **fixed** (hard-coded list, a text file), **tools** (our own capability list,
complete by definition), **LLM** (generated per game, then JEV decides).

## Frame of the game

| Decision | Example options | Shape | Options from |
|---|---|---|---|
| Dimension | 2D / 2.5D / 3D | one | fixed |
| Camera | top-down, side-on, isometric, first-person, third-person | one | fixed per dimension |
| Genre / reference games | platformer, roguelike, tower defense, ... | one or many | fixed |
| Input | keyboard, mouse, one-button, gamepad | one | fixed |
| Players | single player, vs AI opponent, local two-player | one | fixed |
| Time model | real-time, turn-based, real-time with pause | one | fixed |
| Movement model | free, grid, lanes, on rails, none (cursor only) | one | fixed |
| Core loop | the one verb the game is about: jump, shoot, match, build, talk, ... | one | LLM |
| Failure consequence | restart level, lose a life, checkpoint, permadeath, none | one | fixed |
| Session shape | single screen, levels, endless, open world, rooms | one | fixed |
| Win / lose | survive, reach the exit, score, defeat a boss, no failure | one or many | fixed |
| Tone | cozy, tense, silly, epic, eerie | one | fixed |
| Size | how many levels, rooms or minutes | one | fixed bands |

## Gameplay

| Decision | Example options | Shape | Options from |
|---|---|---|---|
| Mechanics: which to include | jump, dash, craft, trade, ... | many | LLM |
| Mechanics: how important | core / nice-to-have / cut | one per mechanic | fixed |
| Tiers | which tier each system lands in (integrator's 0.3 Tiers) | one or score per system | fixed |
| Cut | whether to keep any piece: a screen, a system, a level, an effect | many | the design's own pieces |
| Systems | health, inventory, economy, dialogue, AI | many | fixed or LLM |
| Progression | upgrades, unlocks, levels, story beats, none | one or many | fixed |
| Map contents: enemies | skeletons, bats, ogres, trolls, goblins, rabbits, birds | many per level | LLM or fixed per theme |
| Map contents: pickups, hazards, NPCs, props | per level, as above | many | LLM |
| Bosses | none, one final boss, one per level or act | one | fixed |
| Story | none, intro text, acts with story beats, dialogue trees, branching | one | fixed |
| Number of acts / levels | 1, 3, 5, ... | one | fixed bands |
| Player character | who or what the player is | one | LLM |
| Tutorial | none, controls on the title screen, on-screen prompts, guided first level | one | fixed |
| Per-level theme | forest, dungeon, ice, city | one per level | LLM or fixed |
| Difficulty curve | flat, ramp, spikes, adaptive | one | fixed |
| HUD contents | health, score, timer, minimap, ammo | many | fixed |
| Feel numbers | slow / medium / fast speed, floaty / snappy jump | one per number | fixed bands |

## Visual and audio

| Decision | Example options | Shape | Options from |
|---|---|---|---|
| Art style | pixel, painterly, neon, ... | one | fixed per dimension (probed: the list must hold the answer) |
| Art source per asset, 2D | drawn in code, ComfyUI model, sprite sheet | one | tools |
| Art source per asset, 3D | primitives, TRELLIS, compose_world, Blender? | one | tools |
| Image model per asset | Qwen-2512, NetaYume, pixel model | one | tools (routing table) |
| Palette / mood | warm, cold, dark, pastel, saturated | one | fixed |
| Lighting and atmosphere (3D) | time of day, fog, indoor / outdoor light | one per setting | fixed |
| Animations per character | idle, walk, run, jump, attack, hurt, death | many | fixed |
| Typography | pixel font, clean sans, serif, hand-lettered | one | fixed |
| Accessibility | colour-blind safe palette, remappable keys, difficulty options, reduced motion | many | fixed |
| Music | none, ambient, chiptune, synth loop, orchestral | one | fixed |
| Which events get a sound | jump, hit, pickup, death | many | LLM |
| Screens | title, pause, settings, game over, win | many | fixed |

## Engineering

| Decision | Example options | Shape | Options from |
|---|---|---|---|
| Rendering | canvas 2D / three.js / DOM | one | fixed |
| Level source | hand-authored / seeded generator / mixed | one | fixed |
| Physics | none, simple AABB, custom | one | fixed |
| Lib modules | the `lib/` files (input, audio, canvas, ...) | many | tools |
| Save state | none, local, per run | one | fixed |
| Tests: which states to verify | from the systems list | many | LLM |

## Design sufficiency

| Decision | Example options | Shape | Options from |
|---|---|---|---|
| Is this design sufficient? | yes / no | yes/no | fixed |

Asked of the finished design. Local JEV serves a 32K context, and 4 of the 35 local designs are
over it (up to 38.6K tokens), so either the serving context grows (the card supports 256K) or the
question is asked per section.

## Outside the design step

- **Build-time tool** (`decide_between` / `pick_options`): the build model calls JEV when it is
  choosing, e.g. which of two fixes, or whether a placeholder is acceptable.
- **Checking work**: yes/no over screenshots ("did the player move?"), as in `labs/jev-play-probe`.
- **Asking the user**: a decision JEV is unsure of could go to the user as a one-click choice.

## Open questions

- Is genre a decision, or just a summary of camera + mechanics + win condition?
- How fine do map contents go: per level, per room, per wave?
- A fixed order where each answer narrows the next list, or independent decisions the LLM writes
  the design around?
- Is map layout (where things go) out, or does it come back as JEV choosing between generated
  layouts?
