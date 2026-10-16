# `gameplay.md`

## 1. Game Overview

**Working title:** *Fading Labyrinth*

A 2D top-down maze-solving puzzle game. The player moves through a series of mazes with limited visibility and a fading trail. The goal is to explore, remember the layout, collect optional orbs when present, and reach the exit.

The game is a complete campaign of **12 levels**, from a small tutorial maze to a large final maze. There is no fail state. Progression is unlocked by completing levels. Stars are optional performance goals.

**Core fantasy:**  
You are exploring a maze that erases your memory. Only your recent footprints remain, and only a small area around you is visible. You must solve the maze through observation, memory, and route planning.

**Core loop:**

1. Enter a maze.
2. Move through the maze.
3. See only a small area around the player.
4. Leave a trail that fades after a few seconds.
5. Explore branches, remember important paths, and collect orbs if present.
6. Reach the exit.
7. Earn stars based on time.
8. Unlock the next maze.

---

## 2. Dimensionality

**Decision: 2D top-down.**

The game is played entirely on a flat 2D grid from a top-down view.

**Why 2D top-down:**

- Maze solving depends on clear spatial relationships.
- Top-down 2D makes walls, corridors, branches, and dead ends easy to read.
- The player can plan turns and remember routes without perspective distortion.
- 2.5D or 3D would add visual depth, but that depth would obscure the exact path structure and make the puzzle less fair.
- A fixed top-down camera keeps the focus on the maze itself.

The visual designer may use subtle 2.5D wall shading for presentation, but the gameplay space must remain logically 2D and fully readable.

---

## 3. Space and Layout

The game space is a single maze per level.

### 3.1 Maze Structure

Each maze is a rectangular grid of cells.

- Walls exist between adjacent cells.
- The outer boundary is always solid wall.
- The player occupies one cell at a time.
- Movement is cell-to-cell, not freeform.
- There are no rooms, platforms, elevators, traps, enemies, or moving walls.

**Why no extra geometry:**  
The maze itself is the puzzle. Extra structures would distract from route planning and memory.

### 3.2 Level Components

Each level contains:

- A start cell.
- An exit cell.
- Zero or more orbs.
- A set of walls generated from a seeded algorithm.

### 3.3 Start and Exit Placement

- The start cell is placed in one of the four corners, chosen by the level seed.
- The exit cell is the farthest reachable cell from the start based on maze path distance.
- This ensures the player usually begins with a clear directional goal: move away from the start and into the maze.

**Why corner start:**  
A corner start gives the player a simple initial orientation. It also reduces the chance that the first few moves feel arbitrary.

**Why farthest exit:**  
A far exit increases the chance that the maze requires real exploration rather than a short direct route.

### 3.4 Orbs

Orbs are collectible objective items.

- Orbs are placed in reachable cells.
- Orbs are never placed on the start or exit cell.
- If a level has orbs, the exit is locked until all orbs are collected.
- If a level has no orbs, the exit is open from the beginning.

**Why orbs instead of keys and doors:**  
Keys and doors require careful placement to avoid unfair or confusing layouts. Orbs are simpler: they force exploration without creating hidden dependency problems. They also give the HUD a clear objective.

### 3.5 Level Size Progression

Levels increase in size gradually.

- Early levels are small enough to be solved quickly.
- Mid levels introduce more loops and orbs.
- Late levels are larger and require stronger memory.

The full level table is in section 8.

---

## 4. Core Gameplay Systems

The game uses the following systems:

1. Level generation and validation
2. Player movement
3. Visibility and trail
4. Objective system
5. Progression and scoring
6. HUD and UI
7. Save and settings

---

## 5. Level Generation and Validation

Levels are procedurally generated but deterministic.

Each level uses a fixed seed:

```text
seed = 1000 + level_id
```

This means the same level always generates the same maze, which is important for fair star thresholds and replayability.

### 5.1 Generation Algorithm

Use a **recursive backtracker** / iterative DFS maze generator.

**Why recursive backtracker:**

- It produces organic mazes with many dead ends.
- It creates natural branches that encourage memory-based solving.
- It is simple to validate.
- It avoids the overly structured feel of recursive division or perfect grid patterns.

#### Generation Steps

1. Choose maze width and height from the level table.
2. Choose a start corner using the seeded RNG.
3. Generate a perfect maze using recursive backtracker.
4. Choose the exit as the farthest cell from the start using BFS distance.
5. Add the level’s loop count by removing interior walls.
6. Place orbs according to the level’s orb count.
7. Validate the maze.
8. If validation fails, regenerate up to 10 times.
9. If all attempts fail, use a hand-designed fallback layout for that level.

### 5.2 Loop Addition

A perfect maze has exactly one path between any two cells. Loops are added by removing extra interior walls.

Loop count is a level parameter.

**Why loops:**

- A perfect maze can sometimes be solved by blindly filling dead ends.
- Loops create ambiguity and require the player to remember which branches matter.
- Loops increase difficulty without adding new mechanics.

Loop placement rules:

- Only remove interior walls.
- Do not remove boundary walls.
- Avoid removing walls directly adjacent to the start or exit.
- If removing a wall makes the start-to-exit path too short, reject that wall.
- If the maze fails validation, regenerate.

### 5.3 Orb Placement

Orbs are placed after the maze and exit are determined.

Placement rules:

- Orbs must be in reachable cells.
- Orbs cannot be placed on the start or exit.
- Each orb must be at least `35%` of the maximum start-to-exit BFS distance away from the start.
- Each orb should be reasonably far from the exit, at least `20%` of the maximum distance.
- Orbs should be spaced apart from each other.
  - Minimum separation: `max(3, floor(min(width, height) / 4))` Manhattan distance.
- If placement fails, relax the separation rule once. If it still fails, regenerate the maze.

**Why orb distance rules:**  
Orbs should force exploration, not just sit near the start or exit. Placing them in distant branches makes the player choose which areas to search.

### 5.4 Validation

A generated maze is valid only if:

- All cells are reachable from the start.
- The exit is reachable from the start.
- Every orb is reachable from the start.
- The start-to-exit BFS distance is at least the level’s minimum path length.
- No orb is on the start or exit.
- No straight corridor is longer than 8 tiles.
- The maze does not contain isolated cells.

**Why corridor length limit:**  
Very long straight corridors feel boring and reduce maze complexity. Limiting corridor length keeps the player making frequent decisions.

### 5.5 Fallback Layouts

Each level must have one hand-designed fallback layout.

The fallback must match:

- Level size.
- Orb count.
- Loop count, or a similar loop density.
- Minimum path length.
- Start and exit constraints.

Fallbacks are only used if procedural generation fails validation after 10 attempts.

---

## 6. Player Movement

The player moves one tile at a time on the grid.

### 6.1 Movement Rules

- The player can move up, down, left, and right.
- Diagonal movement is not allowed.
- The player cannot move through walls.
- The player cannot leave the maze boundary.
- The exit cell is passable.
- Orbs are collected automatically when the player enters their cell.

### 6.2 Input

Supported input:

- Keyboard: Arrow keys or WASD.
- Gamepad: Left stick or D-pad.
- Touch: Swipe in a direction to move one tile. Repeated swipes continue movement.

Keyboard and gamepad support holding a direction to keep moving. Touch uses discrete swipes.

**Why grid movement:**

- Grid movement makes maze solving fair and precise.
- It removes ambiguity about wall collisions.
- It is easier to make accessible.
- It makes path planning clearer.
- It simplifies trail and visibility logic.

### 6.3 Movement Feel

- Move time per tile: `140 ms`
- Movement speed: approximately `7.1 tiles per second`
- Input buffer: `1 direction`
- When a move completes, if a buffered direction is valid, the next move begins immediately.
- If multiple directions are pressed, use the most recent one.
- If the player is moving and presses a new direction, the new direction is applied after the current tile move completes.

**Why 140 ms per tile:**  
This feels responsive but not frantic. It gives the player time to observe the maze while still allowing smooth continuous movement when holding a direction.

### 6.4 Movement Edge Cases

- Moving into a wall: no movement.
- Moving out of bounds: no movement.
- Moving onto an orb: collect orb.
- Moving onto a locked exit: player can stand on the exit, but level does not complete.
- Moving onto an unlocked exit: level completes at the end of the move animation.
- Pausing while moving: movement pauses.
- Restarting while moving: movement state resets.

---

## 7. Visibility and Trail

The player cannot see the whole maze.

### 7.1 Light Radius

The player has a small visible area around them.

- Light radius: `2.5 tiles`
- Visibility is measured using Euclidean distance from the player’s cell center to tile centers.
- Tiles within the light radius are visible.
- Walls are visible if at least one adjacent tile is visible.

**Why 2.5 tiles:**

- It is large enough to see immediate turns and short branches.
- It is small enough that the player cannot see the whole route.
- It creates the core tension: the player must remember what they saw.

### 7.2 Trail

When the player moves into a tile, that tile receives a trail marker.

Trail rules:

- Trail lifetime: `10 seconds`
- Trail fade time: last `2 seconds`
- Trail alpha:
  - `1.0` from `0` to `8 seconds`
  - Linear fade from `1.0` to `0.0` from `8` to `10 seconds`
- Trail tiles remain visible even if they are outside the current light radius.
- Trail is shown on the floor.
- Walls adjacent to a trail tile remain visible while that trail tile is visible.
- Old trail tiles are removed when their lifetime expires.

**Why 10 seconds:**

- 10 seconds is long enough to retrace a short branch or return to a decision point.
- It is short enough that the player cannot rely on the trail for the entire maze.
- It creates a clear memory pressure: the player must remember important routes before the trail disappears.

### 7.3 Visibility Edge Cases

- The current tile is always visible.
- The player’s light does not reveal the exit if the exit is outside the light radius.
- Orbs are only visible when in the light radius or on a visible trail tile.
- The exit is only visible when in the light radius or on a visible trail tile.
- No persistent memory map is provided.

**Why no persistent memory map:**  
A persistent map would reduce the memory challenge. The fading trail is the memory system.

---

## 8. Level Content

The game contains 12 levels.

Each level has:

- A name.
- A size.
- A loop count.
- An orb count.
- A minimum start-to-exit path length.
- A par time.
- A 3-star time.
- A design focus.

### 8.1 Level Table

| Level | Name | Size | Loops | Orbs | Min Path | Par | 3-Star | Focus |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | First Steps | 7x7 | 0 | 0 | 14 | 0:40 | 0:28 | Teach movement, light, and trail |
| 2 | Winding Path | 9x9 | 2 | 0 | 20 | 1:00 | 0:42 | Larger basic maze |
| 3 | Forks | 9x9 | 5 | 1 | 22 | 1:15 | 0:53 | Introduce loops and first orb |
| 4 | Gathering Light | 11x11 | 8 | 1 | 28 | 1:35 | 1:07 | Orbs required to unlock exit |
| 5 | Crossroads | 11x11 | 12 | 2 | 30 | 1:55 | 1:21 | More loops and route choice |
| 6 | Deep Hall | 13x13 | 16 | 2 | 36 | 2:20 | 1:38 | Size increase |
| 7 | Tangle | 13x13 | 22 | 2 | 40 | 2:40 | 1:52 | Dense loop structure |
| 8 | Long Way | 15x15 | 28 | 3 | 46 | 3:10 | 2:11 | Longer required exploration |
| 9 | Labyrinth | 15x15 | 36 | 3 | 50 | 3:40 | 2:34 | More orbs and ambiguity |
| 10 | Echo Chamber | 17x17 | 44 | 3 | 56 | 4:10 | 2:53 | Larger memory challenge |
| 11 | Winding End | 19x19 | 55 | 4 | 66 | 4:50 | 3:23 | Four orbs, high route complexity |
| 12 | Final Maze | 21x21 | 68 | 4 | 76 | 5:40 | 3:58 | Full-size final challenge |

### 8.2 Level Design Notes

#### Level 1: First Steps

- No orbs.
- No loops.
- Small enough that the trail remains useful for much of the maze.
- Teaches movement, light radius, and trail fade.

#### Level 2: Winding Path

- Slightly larger.
- A couple of loops are introduced, but the maze is still simple.
- The player learns that not every branch is correct.

#### Level 3: Forks

- First orb.
- More loops.
- The player learns that the exit may be locked.
- Teaches orb collection and exit unlocking.

#### Levels 4-5: Gathering Light / Crossroads

- Orbs become a normal part of the objective.
- Loop density increases.
- The player must decide which branches are worth exploring.

#### Levels 6-7: Deep Hall / Tangle

- Larger mazes.
- More loops.
- The trail becomes less reliable for long routes.
- Memory becomes more important.

#### Levels 8-9: Long Way / Labyrinth

- 15x15 mazes.
- Three orbs.
- The player must manage exploration across a larger space.
- Par times increase significantly.

#### Levels 10-12: Echo Chamber / Winding End / Final Maze

- Largest mazes.
- Highest loop density.
- Four orbs in the final levels.
- The player must maintain a strong mental map of the maze.

---

## 9. Objective System

### 9.1 Win Condition

The player wins a level by entering the exit cell while the exit is unlocked.

### 9.2 Exit Lock

If the level has orbs:

- Exit starts locked.
- Exit becomes unlocked when all orbs are collected.
- The player can stand on the locked exit, but the level does not complete.
- The player must move to the exit again after collecting all orbs.

If the level has no orbs:

- Exit is unlocked from the start.

### 9.3 Orb Collection

- Orbs are collected automatically.
- Collecting an orb removes it from the maze.
- The HUD updates immediately.
- A toast message appears:
  - If orbs remain: `Orb collected`
  - If this was the final orb: `Exit unlocked`

### 9.4 Objective Edge Cases

- Player reaches exit before collecting orbs: exit remains locked.
- Player collects final orb elsewhere: exit unlocks immediately.
- Player collects all orbs and then reaches exit: level completes.
- Player restarts level: orbs reset and exit locks again if orbs exist.
- Player pauses: objective state pauses with the level.

---

## 10. Progression and Scoring

### 10.1 Level Unlocking

- Level 1 is unlocked at start.
- Each level unlocks the next level after completion.
- Completed levels can be replayed at any time from level select.

### 10.2 No Fail State

There is no fail state.

**Why no fail state:**

- Maze solving is already a cognitive challenge.
- Punishing the player with failure would make the game feel unfair.
- The player can always restart if they become lost.
- Stars provide optional challenge without blocking progression.

### 10.3 Timer

- The timer starts on the player’s first successful move.
- The timer pauses when the game is paused.
- The timer resets when the level is restarted.
- The timer is not a fail condition.

**Why timer starts on first move:**  
This prevents the player from losing time while reading the level or thinking about how to start.

### 10.4 Stars

Stars are optional.

Star rules:

- 1 star: Complete the level.
- 2 stars: Complete the level at or under par time.
- 3 stars: Complete the level at or under 3-star time.

3-star time is `70%` of par, rounded down to the nearest second.

**Why stars instead of score:**

- Time is the clearest performance metric for maze solving.
- Stars are easy to understand.
- They encourage replay without forcing difficulty.
- They do not require complex scoring for wrong turns, backtracking, or exploration.

### 10.5 Best Time

- The game stores the best time for each level.
- Replaying a level can improve best time and stars.
- Stars are stored as the highest earned star count.

### 10.6 Progression Edge Cases

- Player completes level with no stars: level still unlocks.
- Player replays a completed level: stars and best time can improve.
- Player quits mid-level: current attempt is lost, but previous progress remains.
- Player restarts: timer and level state reset, but saved progress remains.
- Player completes final level: game complete screen appears.

---

## 11. HUD

The HUD should be minimal.

### 11.1 Persistent HUD Elements

#### Top Left

- Level number and name.
- Objective.

Objective display:

- If no orbs: `Exit`
- If orbs remain: `Orbs 1/3`
- If all orbs collected: `Exit Open`
- If exit is locked and player is standing on it: `Exit Locked`

#### Top Right

- Timer: `M:SS`
- Best time, if one exists, displayed smaller under the timer.

#### Bottom Right

- Pause button.

#### Bottom Left

- Control hint, only during tutorial hints or first-time play.

### 11.2 Toast Messages

Small non-blocking messages appear briefly in the center or upper center.

Toast rules:

- Duration: `1.5 seconds`
- Do not block movement.
- Do not stack more than one at a time.

Toasts:

- `Orb collected`
- `Exit unlocked`
- `Exit locked` — only when the player steps onto a locked exit, once per level attempt.

### 11.3 What Is Not in the HUD

There is no:

- Minimap.
- Arrow to exit.
- Health bar.
- Resource bar.
- Compass.
- Path hint.
- Trail lifetime meter.
- Light radius meter.

**Why no minimap:**  
The fading trail is the memory system. A minimap would make the maze too easy and remove the core tension.

**Why no arrow to exit:**  
An arrow would turn the game into navigation rather than maze solving.

**Why no trail meter:**  
The trail is visible directly. A meter would add clutter without improving understanding.

---

## 12. UI Screens and Content by Section

### 12.1 Title Screen

Content:

- Game title.
- Total stars: `X / 36`
- Buttons:
  - `Play`
  - `Level Select`
  - `How to Play`
  - `Settings`

`Play` behavior:

- If no progress: start Level 1.
- If progress exists: start the next incomplete unlocked level.

**Why total stars on title:**  
It gives the player a clear long-term goal without forcing them to track it manually.

---

### 12.2 How to Play Screen

Content: Three short cards.

#### Card 1: Move

- Use Arrow Keys, WASD, Left Stick, D-Pad, or Touch Swipe.
- Holding a direction keeps moving.
- Swiping moves one tile at a time.

#### Card 2: Light and Trail

- You only see a small area around your character.
- Your trail remains for 10 seconds.
- The trail fades after 8 seconds.

#### Card 3: Objective

- Find the exit.
- If orbs are present, collect all of them to unlock the exit.
- There is no fail state.
- Stars are based on time.

**Why How to Play is separate:**  
Level 1 teaches the basics, but a player may want to understand the rules before starting.

---

### 12.3 Level Select Screen

Content:

- A path or grid of 12 level nodes.
- Each node shows:
  - Level number.
  - Level name.
  - Star count, if completed.
  - Lock icon if locked.
  - Highlight if currently selected.

Buttons:

- `Back`
- `Play Level`, if selected level is unlocked.

Locked level behavior:

- Cannot be selected for play.
- Shows lock icon.
- Tooltip or label: `Complete previous level to unlock`.

**Why level select is visible:**  
The game is short enough that players should be able to replay levels for stars.

---

### 12.4 Gameplay Screen

Content:

- Maze.
- Player.
- Exit.
- Orbs.
- Trail.
- HUD.
- Tutorial hints, if active.

Tutorial hints:

Level 1:

- On load: `Move to explore.`
- After first move: `Your trail fades after 10 seconds.`

Level 3, first time:

- When first orb is visible: `Collect orbs to unlock the exit.`

If player steps onto locked exit:

- Toast: `Exit locked`

**Why tutorial hints are sparse:**  
The game should teach through play. Too many messages would clutter the HUD and reduce immersion.

---

### 12.5 Pause Screen

Content:

- `Paused`
- Buttons:
  - `Resume`
  - `Restart Level`
  - `Level Select`
  - `Settings`
  - `Quit to Title`

Pause behavior:

- Timer stops.
- Trail fade stops.
- Player movement stops.
- Maze state does not change.

**Why restart is in pause:**  
If the player becomes lost, restarting is the natural recovery action.

---

### 12.6 Level Complete Screen

Content:

- `Level Complete`
- Level name.
- Stars earned: 1 to 3.
- Time.
- Best time.
- Buttons:
  - `Next Level`, if not the final level.
  - `Replay`
  - `Level Select`

If the player earned new stars:

- Show a brief star animation.
- If reduced motion is enabled, use a simple non-animated star display.

**Why next level button is present:**  
It makes the campaign flow smooth.

---

### 12.7 Game Complete Screen

Appears after completing Level 12.

Content:

- `The Labyrinth Is Complete`
- Total stars: `X / 36`
- Buttons:
  - `Level Select`
  - `Title`

**Why no automatic reset:**  
The player may want to replay levels for stars. Resetting progress would be frustrating.

---

### 12.8 Settings Screen

Settings do not affect star fairness.

Content:

- Input:
  - Keyboard
  - Gamepad
  - Touch
- Colorblind mode:
  - On / Off
- Reduced motion:
  - On / Off
- Text size:
  - Normal
  - Large

**Why no gameplay-affecting difficulty settings:**  
Changing light radius or trail lifetime would make star times unfair. Accessibility settings should improve clarity without changing the core challenge.

---

## 13. Numbers and Feel

### 13.1 Movement

| Value | Number |
|---|---:|
| Move time per tile | `140 ms` |
| Movement speed | `~7.1 tiles/sec` |
| Input buffer | `1 direction` |
| Diagonal movement | No |
| Acceleration | None |
| Friction | None |

**Feel goal:**  
Crisp, responsive, and readable. The player should feel in control without the movement becoming a reflex challenge.

---

### 13.2 Visibility

| Value | Number |
|---|---:|
| Light radius | `2.5 tiles` |
| Trail lifetime | `10 seconds` |
| Trail fade duration | `2 seconds` |
| Persistent memory | None |

**Feel goal:**  
The player can always see enough to make the next decision, but not enough to solve the whole maze at once.

---

### 13.3 Camera and Viewport

- Camera follows the player.
- Camera is centered on the player.
- Camera is clamped to maze bounds.
- If the maze is smaller than the viewport, center the maze.
- Reference viewport: `15x15 tiles` visible at reference resolution.
- Logical tile size: `1 unit`.
- Player visual size: approximately `0.6 tile`.

**Why 15x15 viewport:**  
It is large enough to see the light radius and nearby context, but small enough that larger mazes still require movement and memory.

---

### 13.4 Difficulty Curve

Difficulty increases through:

1. Maze size.
2. Loop density.
3. Orb count.
4. Required path length.
5. Memory load.

The player never faces a new mechanic in the final level. By Level 12, all mechanics are already understood.

**Why no late-game mechanic surprise:**  
The final level should test mastery of the existing systems, not introduce something new that could feel unfair.

---

## 14. Audio Cues

Audio is not the gameplay responsibility, but these events should have sound cues.

Required sound events:

- Player step.
- Orb collected.
- Exit unlocked.
- Locked exit interaction.
- Level complete.
- Star earned.
- UI select.
- UI back.

All audio should be non-essential. Every gameplay-critical event must also have a visual cue.

---

## 15. Functional Visual Requirements

The visual designer is responsible for art, but the gameplay requires these visual distinctions:

- Player must be clearly distinct from floor, walls, orbs, and exit.
- Walls and floor must be clearly distinguishable.
- Visible area and fog must be clearly distinguishable.
- Trail must be readable on the floor.
- Orbs must be distinct from the player and exit.
- Exit must be distinct from orbs and player.
- Locked exit and unlocked exit must be visually distinct.
- HUD icons must be understandable without color alone.
- Colorblind mode must not rely on color-only cues.

---

## 16. Accessibility

### 16.1 Input

Supported:

- Keyboard.
- Gamepad.
- Touch.

No mouse-only requirements.

### 16.2 Colorblind Support

- Use shapes and icons, not color alone.
- Exit should have a distinct shape.
- Orbs should have a distinct shape.
- Player should have a distinct shape.
- Locked and unlocked exit should differ by shape or icon, not just color.

### 16.3 Reduced Motion

When enabled:

- Disable pulsing exit animation.
- Disable star animation effects.
- Use simple fade instead of complex trail fade effects.
- Remove any screen shake or camera bounce.

### 16.4 Text

- Text size setting affects HUD and menus.
- Text should remain readable at the smallest supported display size.

---

## 17. Save Data

The game saves locally.

Save data should include:

- Completed levels.
- Stars per level.
- Best time per level.
- Settings.
- Total stars.

Save timing:

- Save after level complete.
- Save after settings change.
- Do not save mid-level progress.

**Why no mid-level save:**  
Levels are short enough that mid-level save complexity is not worth it. Restarting a level is simple and fair.

Save edge cases:

- If save file is missing, start with no progress.
- If save file is corrupted, reset to default progress.
- If a level is completed out of order through level select, update save normally.

---

## 18. State Machine

The game uses these main states:

1. `Title`
2. `HowToPlay`
3. `LevelSelect`
4. `Gameplay`
5. `Pause`
6. `Settings`
7. `LevelComplete`
8. `GameComplete`

Transitions:

- Title -> Play -> Gameplay
- Title -> Level Select -> Gameplay
- Title -> How to Play -> Title
- Title -> Settings -> Title
- Gameplay -> Pause -> Resume
- Pause -> Restart -> Gameplay
- Pause -> Level Select -> Level Select
- Pause -> Quit -> Title
- Gameplay -> Level Complete -> Next Level or Level Select
- Level 12 Complete -> Game Complete -> Level Select or Title

---

## 19. All Cases and Edge Cases

### 19.1 First Launch

- Player sees title screen.
- Total stars is `0 / 36`.
- `Play` starts Level 1.
- Level 1 is unlocked.
- All other levels are locked.

### 19.2 Returning Player

- `Play` starts the next incomplete unlocked level.
- Completed levels show stars in level select.
- Best times are available.

### 19.3 Player Is Lost

- Player can pause.
- Player can restart level.
- No penalty.
- Timer resets.
- Trail resets.
- Orbs reset.

### 19.4 Player Reaches Locked Exit

- Player can stand on the exit.
- Level does not complete.
- Toast shows `Exit locked` once.
- HUD shows remaining orbs.

### 19.5 Player Collects Final Orb

- Exit unlocks immediately.
- Toast shows `Exit unlocked`.
- HUD changes to `Exit Open`.

### 19.6 Player Completes Level

- Level complete screen appears.
- Stars are calculated.
- Best time is updated.
- Next level unlocks.
- Save file updates.

### 19.7 Player Completes Final Level

- Game complete screen appears.
- Total stars are shown.
- Player can return to level select or title.

### 19.8 Player Wants Stars

- Player can replay any completed level.
- Better times can improve stars and best time.
- Progress is not lost.

### 19.9 Level Generation Fails

- The generator attempts up to 10 valid layouts.
- If all fail, use the hand-designed fallback layout.
- The fallback must still satisfy the level’s size, orb count, and minimum path length.

### 19.10 Input Device Changes

- If keyboard is used, arrows/WASD work.
- If gamepad is used, left stick/D-pad work.
- If touch is used, swipes work.
- The game should not require a specific input device.

### 19.11 Multiple Inputs

- If multiple directions are active, use the most recent input.
- If no valid input is active, player remains still.

### 19.12 Pause While Moving

- Movement stops.
- Timer stops.
- Trail fade stops.
- Resuming continues from the same state.

### 19.13 Restart While Paused

- Level resets to start.
- Timer resets.
- Trail resets.
- Orbs reset.
- Exit locks if orbs exist.

### 19.14 Quit Mid-Level

- Current attempt is lost.
- Previously completed levels remain saved.
- Returning to the level starts it fresh.

---

## 20. Cut Features and Why They Were Cut

These features were considered but removed.

### 20.1 No Enemies or Traps

**Cut because:**  
The core fantasy is maze solving, not survival. Hazards would distract from memory and route planning.

### 20.2 No Minimap

**Cut because:**  
The fading trail is the core memory mechanic. A minimap would make the maze too easy.

### 20.3 No Arrow to Exit

**Cut because:**  
An arrow would reduce the game to simple navigation. The player should infer direction from memory.

### 20.4 No Keys and Doors

**Cut because:**  
Orbs are simpler and less likely to create unfair layouts. Keys and doors would require more validation and could feel more like a puzzle lock than a maze.

### 20.5 No Moving Walls

**Cut because:**  
Moving walls would add chaos and reduce the fairness of memory-based solving.

### 20.6 No Fail State

**Cut because:**  
Maze solving is already challenging. Failure would make the game feel punitive. Restarting is enough.

### 20.7 No Health or Lives

**Cut because:**  
They are irrelevant to the core maze-solving loop.

### 20.8 No Upgrades

**Cut because:**  
Upgrades would make star times unfair and complicate progression. The player’s skill and memory are the only progression.

### 20.9 No Endless Mode

**Cut because:**  
The game is designed as a complete 12-level campaign. An endless mode would dilute the focused experience.

### 20.10 No Narrative

**Cut because:**  
A short puzzle game does not need story. The maze and the fading trail are enough.

---

## 21. Final Design Summary

*Fading Labyrinth* is a complete 2D top-down maze-solving puzzle game.

The player moves through 12 generated mazes with limited visibility and a fading 10-second trail. Some levels require collecting orbs to unlock the exit. There is no fail state. Progression is linear, and stars are based on time.

The design is intentionally minimal:

- 2D top-down for clarity.
- Grid movement for fairness.
- Small light radius for tension.
- Fading trail for memory.
- Orbs for exploration.
- Stars for optional challenge.
- No minimap, arrow, enemies, traps, or fail state.

The result is a compact, complete maze game that progresses smoothly from a simple tutorial maze to a large final challenge.