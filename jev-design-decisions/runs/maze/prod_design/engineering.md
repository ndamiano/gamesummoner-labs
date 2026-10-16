# `engineering.md`

## 1. Purpose and scope

This document defines the engineering implementation for *Fading Labyrinth*, a complete 12-level HTML/CSS/JS maze-solving game.

The implementation must be:

- Vanilla HTML, CSS, and JavaScript only.
- No Node, npm, bundler, framework, test runner, or external library.
- Syntax-checkable as plain browser scripts.
- Testable in a headless page through a deterministic debug API exposed on `window.__game`.
- Deterministic in all gameplay-affecting logic.
- Scalable to the 12 fixed levels without per-level hand-tuned code.

This document is the source of truth for another agent integrating the engineering side of the game.

If a design choice is important, this document states the choice and the reason.

---

## 2. Engineering decisions and rationale

### 2.1 Use plain scripts, not modules

**Decision:** Use classic browser scripts loaded in a fixed order.

**Why:**

- No build step.
- No module resolution issues in headless file-based tests.
- Simpler syntax check.
- All code can share one global namespace.

---

### 2.2 Use a single global namespace

**Decision:** All game code attaches to:

```js
window.FL = window.FL || {};
```

The debug API is exposed as:

```js
window.__game = { ... };
```

**Why:**

- Plain scripts need an explicit namespace.
- Tests only need `window.__game`.
- Integration is predictable.

---

### 2.3 Use a deterministic debug clock

**Decision:** The game logic is driven by an `update(dtMs)` function.

In normal play, `requestAnimationFrame` calls `update(dtMs)`.

In tests, `window.__game.tick(ms)` calls the same `update` logic deterministically.

**Why:**

- Headless tests cannot rely on real time.
- Trail fade, timer, and movement must be testable.
- One update path avoids divergence between real and debug behavior.

The debug API also includes `setAutoUpdate(false)` so tests can disable the rAF-driven update path and avoid double updates.

---

### 2.4 Use stored 3-star times from the level table

**Decision:** Star thresholds use the explicit `threeStarMs` values from the gameplay level table.

The gameplay document says 3-star time is `70%` of par, but the level table contains a few values that do not exactly match that formula.

**Why:**

- The level table is the gameplay designer’s explicit content.
- Star fairness depends on consistent thresholds.
- Engineering should not silently change designer-authored thresholds.

If a future level omits `threeStarMs`, engineering will compute:

```js
threeStarMs = Math.floor(parMs * 0.7 / 1000) * 1000;
```

---

### 2.5 Replace hand-designed fallback maze data with a deterministic fallback builder

**Decision:** The gameplay document asks for one hand-designed fallback layout per level. Engineering replaces per-level hand data with a deterministic fallback builder.

**Why:**

- Hand-designed maze data for 12 levels is brittle and hard to maintain.
- A deterministic builder is easier to test.
- The builder can guarantee the same constraints: size, orb count, loop count, minimum path length, start/exit constraints, and corridor limit.
- The fallback is still deterministic per level seed.

The fallback builder is the engineering fallback layout. It is not random and does not require external data.

---

### 2.6 Visibility state is logical, not interpolated

**Decision:** Logical visibility uses the player’s current grid cell, not the interpolated visual position.

Rendering may use interpolated position for smooth visuals, but `getState().visibleTiles` and debug visibility queries use the logical cell.

**Why:**

- Tests must be deterministic.
- Gameplay rules are cell-based.
- Avoids subtle differences between visual smoothing and rule state.

---

### 2.7 Cut features

The following are intentionally not implemented:

- Mouse-based maze interaction.
- Minimap.
- Persistent seen-map.
- Arrow to exit.
- Trail lifetime meter.
- Light radius meter.
- Mid-level save.
- Audio mute setting.
- Difficulty settings that affect light radius, trail lifetime, or star fairness.
- High-DPI-specific gameplay logic.
- Procedural narrative.
- Endless mode.

**Why:**

The core fantasy is memory-based maze solving. Extra systems would obscure the core loop or create unfair star times.

---

## 3. Files that must exist

```text
index.html
test.html
css/styles.css
js/config.js
js/rng.js
js/levels.js
js/maze.js
js/save.js
js/audio.js
js/input.js
js/render.js
js/game.js
js/ui.js
js/debug.js
js/tests.js
```

Optional but recommended:

```text
audio/step.wav
audio/orb.wav
audio/exitUnlocked.wav
audio/lockedExit.wav
audio/levelComplete.wav
audio/star.wav
audio/uiSelect.wav
audio/uiBack.wav
```

Audio files are non-essential. The game must not crash if audio files are missing.

---

## 4. Load order

`index.html` loads:

```html
<link rel="stylesheet" href="css/styles.css">

<script src="js/config.js"></script>
<script src="js/rng.js"></script>
<script src="js/levels.js"></script>
<script src="js/maze.js"></script>
<script src="js/save.js"></script>
<script src="js/audio.js"></script>
<script src="js/input.js"></script>
<script src="js/render.js"></script>
<script src="js/game.js"></script>
<script src="js/ui.js"></script>
<script src="js/debug.js"></script>
```

`test.html` loads the same files, then:

```html
<script src="js/tests.js"></script>
```

`test.html` must set:

```js
window.__runTests = true;
```

before `js/tests.js` runs.

---

## 5. Global namespace

Each script should use:

```js
window.FL = window.FL || {};
```

Expected namespaces:

```js
FL.config
FL.rng
FL.levels
FL.maze
FL.save
FL.audio
FL.input
FL.render
FL.game
FL.ui
FL.debug
```

`window.__game` is the public debug API defined in `js/debug.js`.

---

## 6. Configuration constants

`js/config.js` must define:

```js
FL.config = {
  MOVE_MS: 140,
  LIGHT_RADIUS: 2.5,
  LIGHT_RADIUS_SQUARED: 6.25,
  TRAIL_LIFETIME_MS: 10000,
  TRAIL_FADE_MS: 2000,
  TOAST_MS: 1500,
  VIEWPORT_TILES: 15,
  MAX_CORRIDOR_TILES: 8,
  GENERATION_ATTEMPTS: 10,
  TOTAL_LEVELS: 12,
  TOTAL_STARS: 36
};
```

---

## 7. Level data

`js/levels.js` must define the 12 levels.

Level IDs are `1` through `12`.

```js
FL.levels = {
  LEVELS: [
    {
      id: 1,
      name: "First Steps",
      width: 7,
      height: 7,
      loops: 0,
      orbs: 0,
      minPath: 14,
      parMs: 40000,
      threeStarMs: 28000
    },
    {
      id: 2,
      name: "Winding Path",
      width: 9,
      height: 9,
      loops: 2,
      orbs: 0,
      minPath: 20,
      parMs: 60000,
      threeStarMs: 42000
    },
    {
      id: 3,
      name: "Forks",
      width: 9,
      height: 9,
      loops: 5,
      orbs: 1,
      minPath: 22,
      parMs: 75000,
      threeStarMs: 53000
    },
    {
      id: 4,
      name: "Gathering Light",
      width: 11,
      height: 11,
      loops: 8,
      orbs: 1,
      minPath: 28,
      parMs: 95000,
      threeStarMs: 67000
    },
    {
      id: 5,
      name: "Crossroads",
      width: 11,
      height: 11,
      loops: 12,
      orbs: 2,
      minPath: 30,
      parMs: 115000,
      threeStarMs: 81000
    },
    {
      id: 6,
      name: "Deep Hall",
      width: 13,
      height: 13,
      loops: 16,
      orbs: 2,
      minPath: 36,
      parMs: 140000,
      threeStarMs: 98000
    },
    {
      id: 7,
      name: "Tangle",
      width: 13,
      height: 13,
      loops: 22,
      orbs: 2,
      minPath: 40,
      parMs: 160000,
      threeStarMs: 112000
    },
    {
      id: 8,
      name: "Long Way",
      width: 15,
      height: 15,
      loops: 28,
      orbs: 3,
      minPath: 46,
      parMs: 190000,
      threeStarMs: 131000
    },
    {
      id: 9,
      name: "Labyrinth",
      width: 15,
      height: 15,
      loops: 36,
      orbs: 3,
      minPath: 50,
      parMs: 220000,
      threeStarMs: 154000
    },
    {
      id: 10,
      name: "Echo Chamber",
      width: 17,
      height: 17,
      loops: 44,
      orbs: 3,
      minPath: 56,
      parMs: 250000,
      threeStarMs: 173000
    },
    {
      id: 11,
      name: "Winding End",
      width: 19,
      height: 19,
      loops: 55,
      orbs: 4,
      minPath: 66,
      parMs: 290000,
      threeStarMs: 203000
    },
    {
      id: 12,
      name: "Final Maze",
      width: 21,
      height: 21,
      loops: 68,
      orbs: 4,
      minPath: 76,
      parMs: 340000,
      threeStarMs: 238000
    }
  ],

  getLevel: function (id) {
    for (let i = 0; i < this.LEVELS.length; i++) {
      if (this.LEVELS[i].id === id) {
        return this.LEVELS[i];
      }
    }
    return null;
  },

  totalStars: function (save) {
    let total = 0;
    const stars = save && save.stars ? save.stars : {};
    for (let i = 0; i < this.LEVELS.length; i++) {
      const id = this.LEVELS[i].id;
      total += stars[id] || 0;
    }
    return total;
  }
};
```

Level seed:

```js
seed = 1000 + levelId
```

---

## 8. Seeded RNG

`js/rng.js` must provide a deterministic PRNG.

Use `mulberry32`.

```js
FL.rng = {
  mulberry32: function (seed) {
    let a = seed >>> 0;

    return function () {
      a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  },

  levelSeed: function (levelId) {
    return (1000 + levelId) >>> 0;
  },

  attemptSeed: function (levelId, attempt) {
    const base = this.levelSeed(levelId);
    return (base ^ Math.imul((attempt + 1) * 0x9E3779B9, 0x85EBCA6B)) >>> 0;
  },

  fallbackSeed: function (levelId) {
    return this.attemptSeed(levelId, 999);
  },

  randomInt: function (rng, n) {
    return Math.floor(rng() * n);
  },

  shuffle: function (arr, rng) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = this.randomInt(rng, i + 1);
      const tmp = arr[i];
      arr[i] = arr[j];
      arr[j] = tmp;
    }
    return arr;
  }
};
```

Rules:

- No `Math.random()` in gameplay, generation, save, star, or level logic.
- UI animation may use non-critical randomness only if it does not affect state.
- For simplicity, avoid randomness in UI animation too.

---

## 9. Maze representation

A maze is a rectangular grid of cells.

Each cell stores wall bits.

Wall bits:

```js
N = 1
E = 2
S = 4
W = 8
```

Internal maze object:

```js
{
  width: number,
  height: number,
  walls: Uint8Array,
  start: { x, y },
  exit: { x, y },
  orbs: [{ x, y, collected: false }],
  loopCount: number,
  seed: number,
  fallbackUsed: boolean
}
```

`walls` is indexed:

```js
index = y * width + x
```

A wall bit set means there is a wall on that side.

Initial maze:

```js
walls[i] = 15;
```

Boundary walls must never be removed.

---

### 9.1 Direction constants

```js
FL.maze.DIRS = {
  up:    { dx: 0,  dy: -1, bit: 1, opp: 4 },
  right: { dx: 1,  dy: 0,  bit: 2, opp: 8 },
  down:  { dx: 0,  dy: 1,  bit: 4, opp: 1 },
  left:  { dx: -1, dy: 0,  bit: 8, opp: 2 }
};
```

---

### 9.2 Required maze helpers

`FL.maze` must implement:

```js
createMaze(width, height)
cellIndex(maze, x, y)
inBounds(maze, x, y)
hasWall(maze, x, y, dir)
isOpen(maze, x, y, dir)
removeWall(maze, x, y, dir)
reAddWall(maze, x, y, dir)
isBoundaryWall(maze, x, y, dir)
neighbor(maze, x, y, dir)
```

`removeWall` must clear the wall bit on both cells.

`reAddWall` must set the wall bit on both cells.

Boundary walls must be protected.

---

## 10. BFS and path distance

`FL.maze.bfs(maze, from)` returns:

```js
{
  dist: Int16Array or Array,
  parent: Array
}
```

Distance rules:

- Unreachable cells are `-1`.
- Start distance is `0`.
- Movement is 4-directional.
- Walls block movement.

`FL.maze.farthestCell(maze, start)` returns the farthest reachable cell from `start`.

Tie-break rule:

1. Largest distance.
2. Largest `x`.
3. Largest `y`.

This gives a deterministic exit choice.

---

## 11. Straight corridor validation

A straight corridor is a maximal sequence of cells in one cardinal direction such that:

- The wall between each consecutive pair is open.
- Interior cells in the sequence have no open perpendicular walls.
- The sequence stops when the next wall is closed or out of bounds.

`FL.maze.maxStraightCorridor(maze)` returns the maximum corridor length in tiles.

Validation fails if:

```js
maxStraightCorridor > 8
```

Example of a valid corridor:

```text
Cell A has a side opening.
Cell B has no side opening.
Cell C has no side opening.
```

The straight run is counted from cells with no perpendicular openings. Side openings break the run.

This definition intentionally makes open areas with many side openings valid, and long featureless tunnels invalid.

---

## 12. Level generation

### 12.1 Public generation API

`FL.maze.generateLevel(level, options)` generates a maze.

Options:

```js
{
  forceFallback: false,
  seedOverride: null
}
```

Behavior:

1. If `forceFallback` is true, use the fallback builder.
2. Otherwise, try normal generation up to `FL.config.GENERATION_ATTEMPTS` times.
3. If all normal attempts fail, use the fallback builder.
4. If fallback fails, throw an error.

The returned maze must pass validation.

---

### 12.2 Normal generation attempt

For each attempt:

1. Create an RNG from:

```js
FL.rng.attemptSeed(level.id, attempt)
```

2. Create a maze of the level’s width and height.
3. Choose a start corner using the RNG.
4. Generate a perfect maze using iterative recursive backtracker.
5. Compute BFS distances from start.
6. Choose exit as farthest cell from start.
7. Add the level’s loop count.
8. Place orbs.
9. Validate.

If validation fails, try the next attempt.

---

### 12.3 Start corner selection

Corners:

```js
[
  { x: 0, y: 0 },
  { x: width - 1, y: 0 },
  { x: width - 1, y: height - 1 },
  { x: 0, y: height - 1 }
]
```

Choose:

```js
cornerIndex = FL.rng.randomInt(rng, 4)
```

---

### 12.4 Recursive backtracker

Use iterative DFS.

Algorithm:

1. Mark start visited.
2. Push start onto stack.
3. While stack is not empty:
   - Let `cell` be top of stack.
   - Collect unvisited 4-neighbors.
   - If none, pop.
   - If any, choose one with RNG.
   - Remove wall between `cell` and chosen neighbor.
   - Mark neighbor visited.
   - Push neighbor.

This produces a perfect maze.

---

### 12.5 Loop addition

Loops are added by removing interior walls.

A candidate wall is:

- Interior, not boundary.
- Currently closed.
- Not directly adjacent to start or exit.

“Directly adjacent” means:

- One of the wall’s two cells is the start or exit, or
- One of the wall’s two cells is a 4-neighbor of start or exit.

This prevents loops from trivially shortening the first or last part of the route.

Loop addition must add exactly `level.loops` walls.

Algorithm:

1. Compute current start-to-exit distance.
2. Collect candidate walls.
3. For each candidate:
   - Temporarily remove the wall.
   - Compute new start-to-exit distance.
   - Compute max straight corridor.
   - Temporarily restore the wall.
   - If new distance is at least `level.minPath` and corridor limit is valid, keep the candidate.
   - Store impact:

```js
impact = max(0, currentDistance - newDistance)
```

4. Sort valid candidates by:
   - Lowest impact.
   - Deterministic wall key.

Wall key:

```js
"x,y,dir"
```

5. Iterate sorted candidates.
6. For each candidate:
   - Remove the wall.
   - Revalidate distance and corridor.
   - If valid, keep it and increment loop count.
   - If invalid, restore it.
7. Stop when `level.loops` walls are added.
8. If fewer than `level.loops` can be added safely, the attempt fails.

**Why sort by impact:**  
This maximizes the chance of adding the required number of loops without breaking the minimum path length requirement.

---

### 12.6 Orb placement

Orbs are placed after loops.

Let:

```js
distStart = BFS distance from start
distExit = BFS distance from exit
maxDist = distStart[exit]
```

Orb candidate rules:

- Cell is reachable.
- Cell is not start.
- Cell is not exit.
- `distStart[cell] >= ceil(0.35 * maxDist)`
- `distExit[cell] >= ceil(0.20 * maxDist)`

Separation:

```js
minSeparation = max(3, floor(min(width, height) / 4))
```

Separation is Manhattan distance between orbs.

Placement algorithm:

1. Build candidate list.
2. Shuffle candidates with RNG.
3. Use backtracking to place `level.orbs` orbs.
4. If placement fails, relax separation once:

```js
relaxedSeparation = max(2, floor(minSeparation / 2))
```

5. Retry.
6. If still fails, the generation attempt fails.

Orbs in the final maze state must be sorted by:

1. `y`
2. `x`

This makes state serialization deterministic.

---

### 12.7 Maze validation

`FL.maze.validateMaze(maze, level, options)` returns:

```js
{
  valid: boolean,
  reasons: string[]
}
```

Options:

```js
{
  exactLoops: true
}
```

Validation checks:

- Maze width and height match level.
- Start is in bounds.
- Exit is in bounds.
- Start and exit are different cells.
- All cells are reachable from start.
- Exit is reachable from start.
- Start-to-exit distance is at least `level.minPath`.
- Orb count matches level.
- No orb is on start.
- No orb is on exit.
- Every orb is reachable from start.
- Max straight corridor is at most 8.
- If `exactLoops` is true, `maze.loopCount === level.loops`.

---

### 12.8 Fallback builder

The fallback builder creates a deterministic maze that satisfies the level constraints.

It is used only if normal generation fails.

It must support the shipped level table and should also work for reasonable rectangular sizes.

#### Fallback structure

The fallback uses a serpentine spine with short side branches.

Local coordinates are generated with start at:

```js
{ x: 0, y: 0 }
```

Then the maze is transformed to the chosen start corner.

Main columns:

```js
x = 0, 2, 4, ...
```

Branch columns:

```js
x = 1, 3, 5, ...
```

For each main column, open vertical walls for the full height.

For each branch column, open a horizontal wall to the main column immediately to its left.

This makes every branch cell a dead end attached to the main spine.

Then connect main columns in a serpentine path:

- From main column `i` to main column `i+1`:
  - If `i` is even, connect at bottom row.
  - If `i` is odd, connect at top row.
  - Open the wall between the branch cell and the next main column at that row.

This creates a long main path from the top-left corner through the maze.

#### Fallback loops

Safe loops are added by opening vertical walls inside branch columns.

For each branch column `x`:

```js
for y = 0 to height - 2:
  candidate wall between (x, y) and (x, y + 1)
```

These loops create small cycles in side branches. They do not shorten the main start-to-exit path because the main spine already provides a shorter direct route between the two main-spine cells.

Loop candidates must still exclude walls directly adjacent to start or exit.

Shuffle candidates with the fallback RNG and open exactly `level.loops` of them.

The shipped level table has enough safe loop candidates for every level.

#### Fallback start corner

After building the local maze:

1. Compute local start as `{ x: 0, y: 0 }`.
2. Compute local exit as farthest cell from local start.
3. Choose a corner index with the fallback RNG.
4. Transform the local maze so local start maps to the chosen corner.

Transform rules:

- Top-left: identity.
- Top-right: mirror `x`.
- Bottom-right: mirror `x` and `y`.
- Bottom-left: mirror `y`.

Direction bits must transform accordingly.

#### Fallback orbs

Use the same orb placement algorithm as normal generation.

The fallback maze has a long main path and many reachable branch cells, so orb placement should succeed.

If orb placement fails even after relaxing separation, the fallback attempt fails.

#### Fallback validation

The fallback must pass:

```js
FL.maze.validateMaze(maze, level, { exactLoops: true })
```

If it does not, `generateLevel` throws an error.

**Why this fallback works:**

- It guarantees reachability.
- It guarantees a long minimum path.
- It guarantees corridor limit because main and branch cells have frequent side openings.
- It guarantees exact loop count using safe side-branch loops.
- It is deterministic.
- It avoids storing 12 hand-designed maze layouts.

---

## 13. Save data

`js/save.js` handles persistence.

Storage:

- Use `localStorage` if available.
- If `localStorage` is unavailable or throws, use an in-memory fallback.

Storage key:

```js
"fadingLabyrinth.save.v1"
```

Save shape:

```js
{
  version: 1,
  completed: {
    1: true,
    2: false
  },
  stars: {
    1: 3,
    2: 1
  },
  bestMs: {
    1: 25000,
    2: 61000
  },
  settings: {
    input: "keyboard",
    colorblind: false,
    reducedMotion: false,
    textSize: "normal"
  },
  hintsShown: {
    level1Move: false,
    level1Trail: false,
    level3Orb: false
  }
}
```

Normalization rules:

- Missing save returns default save.
- Corrupted JSON returns default save.
- Wrong version returns default save.
- Missing level fields default to:
  - `completed[id] = false`
  - `stars[id] = 0`
  - `bestMs[id] = null`
- Settings are normalized to valid values.

Default settings:

```js
{
  input: "keyboard",
  colorblind: false,
  reducedMotion: false,
  textSize: "normal"
}
```

Save timing:

- After level complete.
- After settings change.
- After hint flags change.
- Do not save mid-level attempt state.

Level unlock rule:

```js
level 1 is unlocked
level N > 1 is unlocked if level N-1 is completed
```

`Play` behavior:

- Find the smallest unlocked level that is not completed.
- If all levels are completed, start level 1.

---

## 14. Game state

`FL.game.state` is the runtime state.

`window.__game.getState()` returns a plain JSON-safe copy.

State shape:

```js
{
  version: 1,
  screen: "title" | "howToPlay" | "levelSelect" | "gameplay" | "pause" | "settings" | "levelComplete" | "gameComplete",
  levelId: number | null,
  selectedLevelId: number | null,
  settingsReturnTo: "title" | "pause" | null,

  level: object | null,
  maze: object | null,

  player: {
    x: number,
    y: number,
    moving: boolean,
    target: { x, y } | null,
    progressMs: number,
    bufferedDirection: string | null,
    facing: string | null
  },

  timerMs: number,
  timerStarted: boolean,
  exitUnlocked: boolean,
  orbsCollected: number,
  lockedExitToastShown: boolean,

  trail: [{
    x: number,
    y: number,
    ageMs: number,
    alpha: number
  }],

  visibleTiles: [{ x, y }],
  toasts: [{
    text: string,
    remainingMs: number
  }],

  hint: {
    levelId: number | null,
    text: string | null
  },

  levelComplete: {
    levelId: number,
    timeMs: number,
    starsEarned: number,
    bestMs: number,
    newStars: number
  } | null,

  gameComplete: {
    totalStars: number
  } | null,

  save: object,
  settings: object,
  totalStars: number,

  audioLog: string[],
  eventLog: object[]
}
```

`visibleTiles` must be sorted by:

1. `y`
2. `x`

`trail` must be sorted by:

1. `y`
2. `x`

`toasts` should contain at most one active toast.

---

## 15. Screens and state machine

Screens:

```text
title
howToPlay
levelSelect
gameplay
pause
settings
levelComplete
gameComplete
```

Transitions:

```text
title -> gameplay
title -> levelSelect
title -> howToPlay
title -> settings
howToPlay -> title
levelSelect -> gameplay
levelSelect -> title
gameplay -> pause
pause -> gameplay
pause -> levelSelect
pause -> settings
pause -> title
settings -> settingsReturnTo
gameplay -> levelComplete
gameplay -> gameComplete
levelComplete -> gameplay
levelComplete -> levelSelect
levelComplete -> gameplay next level
gameComplete -> title
gameComplete -> levelSelect
```

Settings return behavior:

- If opened from title, back returns to title.
- If opened from pause, back returns to pause.

Pause behavior:

- Timer stops.
- Trail aging stops.
- Movement stops.
- Toast timing stops.
- Maze state does not change.

Restart behavior:

- Same generated maze is reused.
- Player returns to start.
- Timer resets.
- Trail clears.
- Orbs reset.
- Exit locks if orbs exist.
- `lockedExitToastShown` resets.
- `timerStarted` resets.

Quit behavior:

- Current attempt is lost.
- Previous save remains.

---

## 16. Movement

### 16.1 Movement constants

```js
MOVE_MS = 140
```

Movement is grid-based.

The player occupies one logical cell.

While moving:

```js
player.moving = true
player.target = { x, y }
player.progressMs = 0 to 140
```

When `progressMs` reaches `140`, the move completes.

---

### 16.2 Movement rules

The player can move:

- Up
- Down
- Left
- Right

Diagonal movement is not allowed.

The player cannot move through walls.

The player cannot leave bounds.

The exit cell is passable.

Orbs are collected when the move completes onto their cell.

Level completion happens when the move completes onto an unlocked exit.

If the exit is locked, the player may stand on it, but the level does not complete.

---

### 16.3 Input buffer

The player has one buffered direction.

Rules:

- If a direction is pressed while not moving, try to move immediately if valid.
- If a direction is pressed while moving, store it as the buffer.
- If multiple directions are pressed, use the most recent one.
- When a move completes:
  - If the buffered direction is valid, start the next move immediately.
  - If the buffered direction is invalid, remain still.
- If the buffered direction is released, choose the most recent remaining held direction, if any.

Direction values:

```js
"up"
"down"
"left"
"right"
```

---

### 16.4 Movement edge cases

- Moving into wall: no movement.
- Moving out of bounds: no movement.
- Moving onto orb: collect orb.
- Moving onto locked exit: stand on exit, no completion.
- Moving onto unlocked exit: complete level at end of move.
- Pausing while moving: preserve `progressMs`.
- Restarting while moving: reset movement.

---

## 17. Input implementation

`js/input.js` must support:

- Keyboard.
- Gamepad.
- Touch swipe.

All inputs feed the same game input buffer.

### 17.1 Keyboard

Supported keys:

```text
ArrowUp
ArrowDown
ArrowLeft
ArrowRight
W
A
S
D
```

Rules:

- `keydown` presses a direction.
- `keyup` releases a direction.
- Prevent default for arrow keys.
- Holding a key keeps that direction active.
- Most recent key press wins.

---

### 17.2 Gamepad

Poll `navigator.getGamepads()` during update.

Supported:

- Left stick.
- D-pad.

Stick threshold:

```js
0.5
```

D-pad buttons:

- Button 12: up
- Button 13: down
- Button 14: left
- Button 15: right

If gamepad direction changes, release old gamepad direction and press new one.

Gamepad input must not require the keyboard.

---

### 17.3 Touch

Swipe on the maze canvas.

Swipe threshold:

```js
24 pixels
```

Direction is the larger axis.

If both axes are below threshold, ignore.

A swipe moves exactly one tile.

Repeated swipes continue movement.

Touch swipes use a one-shot press:

- Swipe presses a direction.
- After one move completes, that touch direction is released automatically.

---

### 17.4 Input priority

All inputs are active.

The most recent input timestamp wins.

If timestamps tie, use `settings.input` as a tie-breaker:

```text
keyboard
gamepad
touch
```

This setting does not disable other inputs.

---

## 18. Timer

Timer rules:

- Starts on the first successful move start.
- Does not start on invalid input.
- Pauses when game is paused.
- Resets on restart.
- Is not a fail condition.

Timer format:

```js
M:SS
```

Example:

```js
95000 -> "1:35"
```

Use floor seconds.

---

## 19. Stars and best time

On level complete:

```js
timeMs = state.timerMs
```

Star calculation:

```js
stars = 1
if (timeMs <= level.parMs) stars = 2
if (timeMs <= level.threeStarMs) stars = 3
```

Save updates:

```js
completed[levelId] = true
stars[levelId] = max(oldStars, stars)
bestMs[levelId] = min(oldBestMs, timeMs)
```

`newStars` is the number of stars earned above the previously saved star count.

If no new stars are earned, `newStars` is `0`.

---

## 20. Visibility and trail

### 20.1 Light radius

Light radius:

```js
2.5 tiles
```

A tile is visible by light if the Euclidean distance between tile centers is at most `2.5`.

Use squared distance:

```js
dx * dx + dy * dy <= 6.25
```

The player’s current logical cell is always visible.

---

### 20.2 Trail

When a move completes into a tile:

- Add or refresh a trail marker on that tile.
- Trail age starts at `0`.
- Revisiting a tile resets its trail age to `0`.

Trail lifetime:

```js
10000 ms
```

Trail fade:

- Age `0` to `8000`: alpha `1.0`
- Age `8000` to `10000`: linear fade from `1.0` to `0.0`
- Age `>= 10000`: remove trail marker

Trail tiles remain visible even if outside the current light radius.

Walls adjacent to a visible trail tile remain visible.

No persistent memory map is stored.

---

### 20.3 Revealed tile rule

A tile is revealed if:

```js
visibleByLight(tile) || activeTrail(tile)
```

A wall is visible if at least one of its adjacent tiles is revealed.

Orbs are visible only if their tile is revealed.

The exit is visible only if its tile is revealed.

---

### 20.4 Visibility edge cases

- Current tile is always visible.
- Exit outside light radius is not visible.
- Orb outside light radius is not visible.
- Trail tile outside light radius is visible.
- Walls adjacent to trail tile are visible.
- After trail expires, the tile is no longer visible unless in light radius.

---

## 21. Objectives

### 21.1 Exit lock

If level has no orbs:

```js
exitUnlocked = true
```

If level has orbs:

```js
exitUnlocked = false
```

When all orbs are collected:

```js
exitUnlocked = true
```

---

### 21.2 Orb collection

When player completes a move onto an orb:

- Mark orb collected.
- Increment `orbsCollected`.
- Show toast:
  - If orbs remain: `"Orb collected"`
  - If this was final orb: `"Exit unlocked"`
- Play audio:
  - `"orb"`
  - If final orb, also play `"exitUnlocked"`.

---

### 21.3 Locked exit interaction

When player completes a move onto a locked exit:

- Level does not complete.
- If `lockedExitToastShown` is false:
  - Show toast `"Exit locked"`.
  - Set `lockedExitToastShown = true`.
- Play audio `"lockedExit"`.

The toast appears once per level attempt.

---

### 21.4 HUD objective text

Top-left objective display:

- No orbs:

```text
Exit
```

- Orbs remain:

```text
Orbs 1/3
```

- All orbs collected:

```text
Exit Open
```

- Exit locked and player standing on exit:

```text
Exit Locked
```

---

## 22. Toasts

Toast rules:

- Duration: `1500 ms`.
- One toast at a time.
- New toast replaces current toast.
- Toasts do not block movement.
- Toasts pause when game is paused.

Toast state:

```js
{
  text: string,
  remainingMs: number
}
```

---

## 23. Tutorial hints

Hints are sparse.

Level 1:

- On load, if `hintsShown.level1Move` is false:

```text
Move to explore.
```

- After first move, if `hintsShown.level1Trail` is false:

```text
Your trail fades after 10 seconds.
```

Level 3:

- When the first orb is visible for the first time in a level attempt, if `hintsShown.level3Orb` is false:

```text
Collect orbs to unlock the exit.
```

Hint flags are saved so hints do not repeat on replay.

---

## 24. UI screens

### 24.1 DOM structure

`index.html` must contain these screen sections:

```html
<section id="screen-title" class="screen">
<section id="screen-how-to-play" class="screen">
<section id="screen-level-select" class="screen">
<section id="screen-gameplay" class="screen">
<section id="screen-pause" class="screen overlay">
<section id="screen-settings" class="screen overlay">
<section id="screen-level-complete" class="screen overlay">
<section id="screen-game-complete" class="screen overlay">
```

Only one screen is active at a time.

Overlays may visually sit over gameplay, but state machine treats them as separate screens.

---

### 24.2 Title screen

Content:

- Game title.
- Total stars:

```text
X / 36
```

Buttons:

```html
<button data-action="play">Play</button>
<button data-action="level-select">Level Select</button>
<button data-action="how-to-play">How to Play</button>
<button data-action="settings">Settings</button>
```

`Play` starts the next incomplete unlocked level.

---

### 24.3 How to Play screen

Three cards:

1. Move
2. Light and Trail
3. Objective

Button:

```html
<button data-action="back">Back</button>
```

---

### 24.4 Level Select screen

Content:

- Grid or path of 12 level nodes.
- Each node shows:
  - Level number.
  - Level name.
  - Stars if completed.
  - Lock state if locked.
- Buttons:
  - `Back`
  - `Play Level`

Level node states:

```text
locked
unlocked
completed
selected
```

Locked nodes cannot be selected for play.

Locked node label:

```text
Complete previous level to unlock
```

---

### 24.5 Gameplay screen

Contains:

```html
<canvas id="maze-canvas"></canvas>
<div id="hud">
  <div id="hud-level"></div>
  <div id="hud-objective"></div>
  <div id="hud-timer"></div>
  <div id="hud-best"></div>
  <button id="hud-pause" data-action="pause"></button>
  <div id="hud-hint"></div>
</div>
<div id="toast" role="status"></div>
```

HUD layout:

- Top left: level and objective.
- Top right: timer and best time.
- Bottom right: pause button.
- Bottom left: control hint when active.

---

### 24.6 Pause screen

Buttons:

```html
<button data-action="resume">Resume</button>
<button data-action="restart">Restart Level</button>
<button data-action="level-select">Level Select</button>
<button data-action="settings">Settings</button>
<button data-action="quit">Quit to Title</button>
```

---

### 24.7 Settings screen

Settings:

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

Button:

```html
<button data-action="back">Back</button>
```

Settings changes save immediately.

---

### 24.8 Level Complete screen

Content:

- `Level Complete`
- Level name.
- Stars earned: 1 to 3.
- Time.
- Best time.

Buttons:

```html
<button data-action="next-level">Next Level</button>
<button data-action="replay">Replay</button>
<button data-action="level-select">Level Select</button>
```

`Next Level` is hidden on level 12 because level 12 completion goes to game complete.

If new stars were earned:

- Show star animation.
- If reduced motion is enabled, use a simple non-animated star display.

---

### 24.9 Game Complete screen

Content:

- `The Labyrinth Is Complete`
- Total stars:

```text
X / 36
```

Buttons:

```html
<button data-action="level-select">Level Select</button>
<button data-action="title">Title</button>
```

---

## 25. Rendering

Rendering uses one canvas:

```html
<canvas id="maze-canvas"></canvas>
```

The canvas is the maze viewport.

HUD is DOM.

### 25.1 Canvas sizing

Reference viewport:

```js
15x15 tiles
```

Canvas should be square.

Size:

```js
size = min(containerWidth, containerHeight)
```

Use device pixel ratio:

```js
canvas.width = size * dpr
canvas.height = size * dpr
canvas.style.width = size + "px"
canvas.style.height = size + "px"
ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
```

Tile size:

```js
tileSize = size / 15
```

---

### 25.2 Camera

Camera follows the player.

Logical camera is in tile units.

If maze is smaller than viewport:

```js
cameraX = (mazeWidth - 15) / 2
cameraY = (mazeHeight - 15) / 2
```

If maze is larger than viewport:

```js
cameraX = clamp(playerX - 7.5, 0, mazeWidth - 15)
cameraY = clamp(playerY - 7.5, 0, mazeHeight - 15)
```

For visual smoothness, the camera may use the interpolated player position.

Reduced motion disables camera easing and bounce.

---

### 25.3 Draw order

1. Fill background/fog.
2. Draw revealed floor tiles.
3. Draw trail on floor.
4. Draw visible walls.
5. Draw exit if visible.
6. Draw orbs if visible.
7. Draw player.

---

### 25.4 Visual shapes

The visual designer owns final art, but engineering must enforce accessible shapes.

Required shape distinctions:

- Player: circle with directional notch.
- Orb: diamond.
- Exit: square.
- Locked exit: square with lock glyph.
- Unlocked exit: square with open-door glyph or open gap.

These shapes must remain distinguishable without color.

---

### 25.5 CSS variables

The renderer should read CSS custom properties from the canvas element where possible.

Expected variables:

```css
--fl-floor
--fl-wall
--fl-fog
--fl-trail
--fl-player
--fl-orb
--fl-exit
--fl-exit-locked
```

Default values may be defined in CSS.

The visual designer can change these without changing game logic.

---

### 25.6 Reduced motion

When reduced motion is enabled:

- No pulsing exit.
- No player bobbing.
- No star animation effects.
- No camera bounce.
- Toast uses simple fade or no fade.
- Trail alpha still fades linearly.

---

### 25.7 Colorblind mode

Colorblind mode must not rely on color alone.

Engineering ensures:

- Shapes differ.
- Locked/unlocked exit differ by glyph.
- Orbs differ from player and exit by shape.
- HUD icons use shape or text.

The visual designer can adjust palettes, but shape logic is engineering-owned.

---

## 26. Audio

`js/audio.js` implements a non-essential audio manager.

Expected audio files:

```text
audio/step.wav
audio/orb.wav
audio/exitUnlocked.wav
audio/lockedExit.wav
audio/levelComplete.wav
audio/star.wav
audio/uiSelect.wav
audio/uiBack.wav
```

Audio events:

```js
"step"
"orb"
"exitUnlocked"
"lockedExit"
"levelComplete"
"star"
"uiSelect"
"uiBack"
```

Rules:

- Audio must never block gameplay.
- Missing audio files must not throw.
- Audio may be disabled in tests.
- Debug audio logging must still work when audio is disabled.

Audio manager behavior:

```js
FL.audio.play(eventName)
```

This:

1. Appends event name to debug audio log if logging is enabled.
2. Attempts to play the audio file.
3. Ignores playback errors.

Star audio:

- Play `"star"` once per new star earned.
- If 3 new stars are earned, play 3 times.

UI audio:

- Primary buttons play `"uiSelect"`.
- Back buttons play `"uiBack"`.

---

## 27. Debug API

`window.__game` is the debug API.

It must be available after `js/debug.js` loads.

### 27.1 API shape

```js
window.__game = {
  version: "1.0.0",

  // State
  getState: function () {},

  // Lifecycle
  reset: function () {},
  startLevel: function (levelId, options) {},
  restartLevel: function () {},
  pause: function () {},
  resume: function () {},
  quitToTitle: function () {},
  openHowToPlay: function () {},
  openLevelSelect: function () {},
  openSettings: function () {},
  nextLevel: function () {},
  replayLevel: function () {},

  // Settings
  setSetting: function (key, value) {},

  // Input
  press: function (direction) {},
  release: function (direction) {},
  swipe: function (direction) {},

  // Time
  tick: function (ms) {},
  setAutoUpdate: function (enabled) {},

  // Save
  setSave: function (saveObject) {},
  loadSave: function (jsonString) {},
  clearSave: function () {},

  // Level generation
  generateLevel: function (levelId, options) {},
  validateMaze: function (maze, levelId, options) {},
  pathfind: function (from, to) {},

  // Gameplay debug
  setTimer: function (ms) {},
  teleport: function (x, y) {},
  collectOrb: function (index) {},
  forceComplete: function (timeMs) {},
  solveLevel: function () {},

  // Visibility debug
  isTileVisible: function (x, y) {},
  isWallVisible: function (x, y, dir) {},
  getTrailAge: function (x, y) {},

  // Logs
  audioLog: [],
  eventLog: [],
  clearAudioLog: function () {},
  clearEventLog: function () {},
  setAudioLogging: function (enabled) {},
  setAudioEnabled: function (enabled) {}
};
```

---

### 27.2 `getState()`

Returns a JSON-safe plain object.

It must not return internal `Uint8Array` directly.

Maze walls in state should be a normal array:

```js
maze.walls = Array.from(internalWalls)
```

---

### 27.3 `reset()`

Resets the game to first launch:

- Save cleared to default.
- Settings default.
- Screen title.
- No current level.
- Timer zero.
- Trail empty.
- Input cleared.
- Audio log cleared.
- Event log cleared.
- Maze cache cleared.
- Auto-update disabled if called from tests.

---

### 27.4 `startLevel(levelId, options)`

Options:

```js
{
  force: false
}
```

Behavior:

- If `force` is false, level must be unlocked.
- If locked and not forced, return `false`.
- Generate or fetch deterministic maze.
- Reset level attempt state.
- Set screen to `gameplay`.
- Return `true` on success.

---

### 27.5 `tick(ms)`

Advances game logic by `ms` milliseconds.

Rules:

- `ms` must be a non-negative number.
- If screen is not `gameplay`, no gameplay state changes.
- If paused, no gameplay state changes.
- If level complete, no gameplay state changes.
- Processes movement, timer, trail, toasts deterministically.
- May complete multiple tile moves if `ms` is large.

---

### 27.6 `solveLevel()`

Returns a Promise.

Behavior:

- Only valid when screen is `gameplay`.
- Repeatedly:
  - If orbs remain, target the first uncollected orb by sorted orb order.
  - Else target exit.
  - Compute BFS path from player to target.
  - For each direction in path:
    - Call `swipe(direction)`.
    - Call `tick(FL.config.MOVE_MS)`.
    - If screen changes, stop.
- Resolves `true` if level completes.
- Resolves `false` if no path is found or state becomes invalid.

This is used for high-level playability tests.

---

### 27.7 `forceComplete(timeMs)`

Debug-only.

If screen is `gameplay`:

- Set timer to `timeMs`.
- Complete the level immediately.

Used to test star calculation without manually driving the maze.

---

### 27.8 `teleport(x, y)`

Debug-only.

Sets player logical cell to `x,y`.

Does not trigger:

- Orb collection.
- Exit completion.
- Trail creation.

Used for visibility and trail tests.

---

### 27.9 `collectOrb(index)`

Debug-only.

Marks the orb at the given sorted index as collected.

Updates objective and exit lock state.

---

### 27.10 Visibility debug helpers

`isTileVisible(x, y)` returns:

```js
visibleByLight(x, y) || activeTrail(x, y)
```

`isWallVisible(x, y, dir)` returns whether the wall segment is visible.

`getTrailAge(x, y)` returns:

```js
number | null
```

---

## 28. Event log

`window.__game.eventLog` records high-level events.

Events:

```js
{ type: "move", from: {x,y}, to: {x,y}, dir: "up" }
{ type: "orb", x, y, remaining }
{ type: "exitUnlocked" }
{ type: "lockedExit" }
{ type: "levelComplete", levelId, timeMs, stars }
{ type: "ui", action: "play" }
```

Event log is for tests and debugging.

It should not affect gameplay.

---

## 29. Test harness

Tests run in a headless page.

There is no test runner.

`js/tests.js` defines:

```js
window.__tests = {
  results: null,
  run: async function () {}
};
```

If:

```js
window.__runTests === true
```

then `js/tests.js` runs tests on `DOMContentLoaded`.

When finished, it sets:

```js
window.__testResults = {
  passed: number,
  failed: number,
  total: number,
  durationMs: number,
  failures: [
    {
      name: string,
      message: string,
      stack: string
    }
  ]
}
```

Headless validation can wait until:

```js
window.__testResults !== null
```

and then assert:

```js
window.__testResults.failed === 0
```

---

### 29.1 Test helpers

`js/tests.js` must include minimal helpers:

```js
function assert(condition, message) {}
function assertEqual(actual, expected, message) {}
function assertDeepEqual(actual, expected, message) {}
```

`assertDeepEqual` may use `JSON.stringify` because state is JSON-safe.

Each test must:

1. Call `__game.reset()`.
2. Use `__game.tick()` instead of real timers.
3. Use debug API for state changes.
4. Avoid relying on real `requestAnimationFrame`.

At test start:

```js
__game.reset();
__game.setAutoUpdate(false);
__game.setAudioLogging(true);
__game.setAudioEnabled(false);
```

---

## 30. Required tests

The test suite must include the following tests.

### 30.1 Level table integrity

Assert:

- 12 levels exist.
- IDs are `1` through `12`.
- Names are non-empty.
- Width and height are positive.
- `parMs > threeStarMs > 0`.
- `minPath > 0`.
- `orbs >= 0`.
- `loops >= 0`.

---

### 30.2 RNG determinism

Assert:

- Same seed produces same sequence.
- Different seeds produce different sequences.
- `randomInt` stays in range.
- `shuffle` is deterministic for same seed.

---

### 30.3 Normal level generation is valid

For every level `1` through `12`:

- Call `__game.generateLevel(levelId)`.
- Call `__game.validateMaze(maze, levelId, { exactLoops: true })`.
- Assert valid.
- Assert maze width/height match level.
- Assert orb count matches level.
- Assert loop count matches level.
- Assert start is a corner.
- Assert exit is not start.
- Assert exit is farthest cell from start using BFS.
- Generate twice and assert walls, orbs, start, and exit are identical.

---

### 30.4 Fallback generation is valid

For every level:

- Call `__game.generateLevel(levelId, { forceFallback: true })`.
- Assert `fallbackUsed === true`.
- Assert validation passes with `exactLoops: true`.
- Assert start is a corner.
- Assert exit is farthest cell from start.
- Assert orb count matches level.
- Assert loop count matches level.
- Assert deterministic: generate twice and compare.

---

### 30.5 Movement is blocked by walls

Start level 1.

For each direction from start:

- If wall exists or out of bounds:
  - Press direction.
  - Tick `MOVE_MS`.
  - Assert player position unchanged.

---

### 30.6 Valid movement works

Start level 1.

Find a valid direction from start using maze walls.

- Press direction.
- Tick `MOVE_MS`.
- Assert player moved to target cell.
- Assert trail exists at new cell.
- Assert timer started.

---

### 30.7 Input buffer works

Start a level.

- Press valid direction A.
- Tick halfway through move.
- Press valid direction B.
- Tick remaining time.
- Assert first move completed in direction A.
- Tick `MOVE_MS`.
- Assert second move completed in direction B.

---

### 30.8 Holding direction continues movement

Start a level.

Find a straight valid path of at least 3 tiles.

- Press direction.
- Tick `MOVE_MS * 3`.
- Assert player moved 3 tiles if path is clear.

If path is not clear, use a generated level or debug maze where a straight path exists.

---

### 30.9 Orb collection works

Start level 3 or any level with orbs.

Use `__game.solveLevel()` or manual pathfinding.

After collecting each orb:

- Assert orb `collected === true`.
- Assert `orbsCollected` increments.
- Assert HUD objective updates.
- Assert toast text is correct.
- Assert audio log contains `"orb"`.

After final orb:

- Assert `exitUnlocked === true`.
- Assert toast is `"Exit unlocked"`.
- Assert audio log contains `"exitUnlocked"`.

---

### 30.10 Locked exit does not complete level

Start a level with orbs.

- Path player to exit before collecting orbs.
- Assert player is on exit.
- Assert screen remains `gameplay`.
- Assert toast is `"Exit locked"`.
- Assert audio log contains `"lockedExit"`.
- Assert `lockedExitToastShown === true`.
- Move away and back onto locked exit.
- Assert no second `"Exit locked"` toast.

Then collect orbs and complete level.

---

### 30.11 Level completion works

Start a level without orbs or solve orbs first.

- Move onto unlocked exit.
- Assert screen becomes `levelComplete` or `gameComplete` for level 12.
- Assert save completed level.
- Assert stars at least 1.
- Assert best time set.
- Assert audio log contains `"levelComplete"`.

---

### 30.12 Star calculation

Use `__game.forceComplete(timeMs)`.

For a level:

- Complete with time `<= threeStarMs`:
  - Assert 3 stars.
- Complete with time `> threeStarMs` but `<= parMs`:
  - Assert 2 stars.
- Complete with time `> parMs`:
  - Assert 1 star.

Also test:

- Replaying with a better time increases stars.
- Replaying with a worse time does not reduce saved stars.
- Best time improves only when new time is lower.

---

### 30.13 Timer starts on first move

Start level.

- Assert timer is `0`.
- Press invalid direction.
- Tick.
- Assert timer still `0`.
- Press valid direction.
- Tick small amount.
- Assert `timerStarted === true`.
- Assert timer > `0`.

---

### 30.14 Timer pauses and resumes

Start level and begin timer.

- Record timer.
- Pause.
- Tick `1000`.
- Assert timer unchanged.
- Resume.
- Tick `1000`.
- Assert timer increased.

---

### 30.15 Trail lifetime and fade

Start level.

- Move to a tile.
- Assert trail age is `0`.
- Assert alpha is `1`.
- Tick `8000`.
- Assert alpha is `1`.
- Tick `1000`.
- Assert alpha is approximately `0.5`.
- Tick `1000`.
- Assert trail removed.

---

### 30.16 Trail remains visible outside light radius

Start level.

- Move to a tile.
- Teleport player far away.
- Assert original trail tile is still visible while trail age < `10000`.
- Tick until trail expires.
- Assert original tile is no longer visible unless in light radius.

---

### 30.17 Light radius visibility

Start level.

For a set of cells around start:

- Cells within Euclidean distance `2.5` are visible.
- Cells outside are not visible.
- Current cell is visible.
- Walls adjacent to visible tiles are visible.
- Walls not adjacent to visible or trail tiles are not visible.

---

### 30.18 No persistent memory

Start level.

- Move to a tile.
- Teleport away.
- Wait for trail to expire.
- Assert tile is not visible.

There must be no hidden `seen` map in state.

---

### 30.19 Save persistence and progression

Fresh save:

- Level 1 unlocked.
- Levels 2-12 locked.
- Total stars `0 / 36`.

Complete level 1:

- Level 1 completed.
- Level 2 unlocked.
- Stars saved.
- Best time saved.

Complete level 2:

- Level 3 unlocked.

Complete out of order through level select:

- Start an unlocked completed level.
- Complete it.
- Assert save updates normally.

Corrupted save:

- Call `__game.loadSave("not-json")`.
- Assert save resets to default.

---

### 30.20 Level select behavior

From title:

- Open level select.
- Assert level 1 selectable.
- Assert level 2 locked.
- Select level 1.
- Press play level.
- Assert screen is gameplay.

Select locked level:

- Assert it cannot be played.

---

### 30.21 Settings affect UI and save

For each setting:

- Change setting.
- Assert save updated.
- Assert DOM class or attribute updated.

Settings:

- `colorblind`:
  - Root or app element has `colorblind` class when true.
- `reducedMotion`:
  - Root or app element has `reduced-motion` class when true.
- `textSize`:
  - Root or app element has `text-large` class when large.
- `input`:
  - Save stores value.
  - Hint text or input priority uses value.

---

### 30.22 Audio events are logged

Clear audio log.

Perform:

- Move:
  - Expect `"step"`.
- Orb:
  - Expect `"orb"`.
- Final orb:
  - Expect `"exitUnlocked"`.
- Locked exit:
  - Expect `"lockedExit"`.
- Level complete:
  - Expect `"levelComplete"`.
- Star earned:
  - Expect `"star"` once per new star.
- UI select:
  - Expect `"uiSelect"`.
- UI back:
  - Expect `"uiBack"`.

Audio must be disabled during tests, but logging must still work.

---

### 30.23 Input device simulation

Keyboard:

- `press("up")`
- `tick(MOVE_MS)`
- `release("up")`
- Assert movement.

Gamepad:

- Use debug input simulation if exposed, or simulate through input manager.
- Assert movement.

Touch:

- `swipe("up")`
- `tick(MOVE_MS)`
- Assert one tile movement.
- Assert touch direction is released after move.

Most recent input:

- Press left.
- Press right.
- Assert buffered direction is right.

---

### 30.24 Full campaign playability

This is the final required test.

Steps:

1. `__game.reset()`.
2. For level `1` through `12`:
   - Start level normally, not forced.
   - Assert level is unlocked.
   - Call `await __game.solveLevel()`.
   - Assert it resolves `true`.
   - Assert screen is:
     - `levelComplete` for levels 1-11.
     - `gameComplete` for level 12.
   - Assert save completed level.
   - Assert stars at least 1.
   - If level < 12:
     - Call `__game.nextLevel()` or start next level.

This test proves the full game is playable from first launch to completion.

---

### 30.25 Debug state is serializable

Call:

```js
JSON.stringify(__game.getState())
```

Assert it does not throw.

Assert result contains:

- `screen`
- `levelId`
- `player`
- `timerMs`
- `save`
- `settings`

---

## 31. Definition of done

The engineering implementation is done when:

1. All required files exist.
2. All JS files pass syntax check.
3. `index.html` loads and shows the title screen.
4. `test.html` runs the test suite.
5. `window.__testResults.failed === 0`.
6. The full campaign test passes.
7. All 12 levels generate valid deterministic mazes.
8. Fallback generation passes for all 12 levels.
9. Save persistence works.
10. Keyboard, gamepad, and touch input all work.
11. Audio events are logged and non-essential.
12. Accessibility settings change UI state.
13. No minimap, arrow, persistent memory map, fail state, or gameplay-affecting difficulty setting exists.
14. The game can be completed from title to game complete without manual save editing.