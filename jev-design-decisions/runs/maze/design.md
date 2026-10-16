# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Make a game about solving mazes | Core loop in §4: enter a pastel top-down maze, move freely, solve keys/switches/doors, reach the exit. |
| 2D | Canvas rendering, tile grid, top-down orthographic view. |
| Camera: top-down | Static top-down view of the full level, centered in a 960×600 logical canvas. |
| Players: single player | One local player controlled by remappable keyboard input. |
| Time model: real-time | Fixed-step 60 Hz simulation with real-time movement. |
| Movement model: free movement | 8-directional vector movement at 112 px/s, not tile-by-tile. |
| Session shape: a sequence of levels | Six hand-authored levels, unlocked sequentially. |
| Failure: restart the level | No death or timer failure; restart is the recovery action via `R` or pause. |
| Tone: cozy | Pastel garden mazes, no enemies, no traps, no timer, soft acoustic audio. |
| Size: a handful of levels, under 30 minutes | Six levels with target total play time of 15–24 minutes. |
| Win/lose: `['reach the exit']` | Win occurs only when the player enters the exit tile. There is no lose state. |
| Systems: exploration: secrets, keys and locked doors, landmarks | §4 systems: Secret Blossoms, Petal Keys and Locked Doors, Garden Landmarks. |
| Systems: puzzles: puzzle types, hints, switches and doors | §4 systems: exactly two puzzle types, Hint Arrows, Bloom Switches and Switch Doors. |
| Art style: hand-drawn / painterly | Brush/watercolor tile recipe, ink outlines, static paper texture, irregular hand-lettered UI. |
| Palette: pastel | Pastel, colour-blind-safe palette in §3 and §4. |
| Typography: hand-lettered | Handwriting font stack with deterministic irregular rotation and ink underlines. |
| Music: acoustic | Synthesized plucked guitar/folk-style loops and soft piano-like tones. |
| Sound effects style: minimal | Soft clicks and short tones only, no loud or complex SFX. |
| Screens: title, pause, settings, win, level select | §7 state machine includes exactly these UI screens plus the in-level play state. |
| HUD: none | No persistent in-level HUD. All information is in-world or on a screen. |
| Effects: none | No particles, no screen shake, no hit flashes, no post-processing effects. |
| Accessibility: colour-blind safe palette, reduced motion, remappable keys | Shape-based icons, `reducedMotion` setting, settings-screen key remapping. |

## 0.2 Decisions

| Decision | Value | Why |
| --- | --- | --- |
| Game title | `Petal Path` | Cozy, matches maze/path theme and pastel tone. |
| Player identity | `Pip`, a small paper sprout | Non-threatening, fits hand-drawn garden world, easy to animate simply. |
| Setting | The Meadow Maze, a sequence of six pastel garden mazes | Cozy tone, supports landmarks without adding lore systems. |
| Level count | 6 | “A handful” and fits under 30 minutes. |
| Level target times | L1 1–2 min, L2 2–3 min, L3 2–3 min, L4 3–5 min, L5 3–5 min, L6 4–6 min | Total 15–24 minutes, under 30. |
| No enemies | Exactly zero enemies | Systems list does not include enemies; cozy tone. |
| No traps | Exactly zero traps | Systems list does not include traps; failure is restart only. |
| No score | No score, no stars, no timer | Win/lose is only reaching exit; HUD is none. |
| No lose state | Player cannot fail except by choosing restart | `win/lose` only includes `reach the exit`; cozy tone. |
| Camera behaviour | Full level always visible, static top-down | All levels are small enough, supports accessibility, removes camera complexity. |
| Canvas size | 960×600 logical pixels, CSS-scaled preserving aspect ratio | Fits largest level, common browser size, simple scaling. |
| Tile size | 32 px per tile | Largest level is 15×13 = 480×416 px, comfortably centered. |
| Player speed | 112 px/s = 3.5 tiles/s | Smooth maze movement without feeling floaty. |
| Player collision radius | 10 px | Small enough for tight corridors, large enough to feel solid. |
| Movement model | Instant normalized velocity, no acceleration | Predictable, accessible, easy to test. |
| Facing | 4 facings: up, down, left, right | Enough for hand-drawn sprites and simple animation. |
| Key model | Keys are not consumed; carrying a key pattern opens any matching locked door permanently | Cozy, prevents soft-lock, simplifies rules. |
| Key patterns | Exactly two: circle and triangle | Shape-based, colour-blind safe, enough variety for six levels. |
| Door model | Doors are 1×1 tiles; closed doors block movement; opened doors become floor | Clear maze interaction, no extra door states. |
| Switch model | A switch blooms once and permanently opens its linked switch door | Cozy, no requiring simultaneous pressure plates. |
| Switch-door marker | `D` in level maps | Distinct from keyed doors `o` and `a`. |
| Secret model | Touch a secret blossom to bloom it and add one leaf to Pip for the rest of the level | Gives secrets feedback without HUD, scoring, or progression effects. |
| Secret limit | 0–3 per level | Keeps optional content light. |
| Landmark model | Static walkable visual anchors only | Wayfinding aid without adding gameplay systems. |
| Hint model | Press `H` to show a 3-second ink arrow; 5-second cooldown | Minimal, non-intrusive, supports puzzles. |
| Hint target priority | 1) unactivated switch door, 2) missing keyed door/key, 3) openable keyed door, 4) exit | Deterministic and easy to test. |
| Progression | Levels unlock sequentially; completion saved locally | Sequence of levels, no extra meta systems. |
| Persistence | `localStorage` key `petal-path-v1` | Simple browser persistence for completion and settings. |
| Fixed timestep | 60 Hz simulation, `1/60` second step | Deterministic movement and collision. |
| Random source | Deterministic `mulberry32` seeded per level | Any hand-drawn jitter must be stable and testable. |
| Accessibility palette | Pastel colours plus mandatory shape icons | Colour-blind safe; no red/green-only identification. |
| Reduced motion | Disables idle sway, hint wiggle, win hop, CSS transitions | Meets accessibility requirement. |
| Remappable keys | All actions remappable in settings | Meets accessibility requirement. |
| Typography | Local handwriting font stack, no external font dependency | Browser-safe, hand-lettered feel. |
| Audio implementation | Web Audio synthesis only | No asset files required; matches acoustic tone with plucks/tones. |
| Music count | 2 loops: title, level | Enough variety without large asset burden. |
| SFX count | 10 UI/gameplay SFX | Minimal soft clicks and tones. |

## 0.3 Tiers

| Tier | Name | Scope | Why this tier |
| --- | --- | --- | --- |
| Tier 1 | Core Cozy Maze | Title, level select, settings, pause, win; L1–L2; movement, collision, exit win, restart; one key/door; one switch-free level; basic landmarks/secrets; minimal audio; reduced motion; remappable keys; progress save. | Minimal viable game: the player can understand mazes, solve a door, and finish a short sequence. |
| Tier 2 | Full Puzzle Content | Add L3–L6; switch doors; multiple keys; all level maps; all secrets and landmarks; sequential unlock for six levels. | Turns the core loop into the full “handful of levels” session. |
| Tier 3 | Hints and Polish | Hint arrows, full audio table, hand-drawn visual recipe, win-screen blossom feedback, debug API, full tests. | Improves usability and feel without adding new gameplay systems. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Quantity | Unit | Value / rule |
| --- | --- | --- |
| Logical canvas size | CSS pixels | 960 × 600 |
| Tile size | CSS pixels | 32 × 32 |
| Coordinates | CSS pixels | `(x, y)` in canvas space. |
| Tile coordinates | tiles | Code uses 0-based `(x, y)` where `(0, 0)` is top-left. |
| Design map coordinates | tiles | Human-facing tables use 1-based `(col, row)`; convert by `x = col - 1`, `y = row - 1`. |
| Time | seconds | Simulation delta `dt` in seconds. |
| Simulation rate | steps/second | 60 fixed steps per second. |
| Fixed step | seconds | `dt = 1/60`. |
| Player speed | px/second | 112. |
| Player speed in tiles | tiles/second | 3.5. |
| Player collision radius | px | 10. |
| Hint duration | seconds | 3.0. |
| Hint cooldown | seconds | 5.0. |
| Win delay | seconds | 0.35 before win screen. |
| Audio gain units | linear 0–1 | Defaults: music 0.6, SFX 0.8. |
| Level count | levels | 6. |

## 1.2 Important conventions

- The game uses a fixed-step loop: `requestAnimationFrame` accumulates elapsed time, clamps max frame delta to `0.25` seconds, and runs integer numbers of `1/60` second simulation steps before rendering.
- `Math.random` is forbidden. All deterministic irregularity uses `mulberry32`. The global seed is `0x9E3779B9`. Level visual jitter uses seed `levelIndex * 101 + 7`.
- Tile types are derived from level map characters:
  - `#` wall
  - `.` floor
  - `@` player start
  - `E` exit
  - `O` circle key
  - `A` triangle key
  - `o` circle keyed door
  - `a` triangle keyed door
  - `D` switch door
  - `*` bloom switch
  - `?` secret blossom
  - `L` lantern landmark
  - `F` flower landmark
  - `R` stone landmark
- Closed doors are collision blocks. Open doors are floor.
- Keys, switches, secrets, landmarks, and the exit are walkable.
- There are no enemies, traps, hazards, timers, score, inventory count UI, or persistent damage state.
- Restart resets the current level: player position, carried keys, doors, switches, secrets, hint state, win state.
- Completion and settings persist in `localStorage` under `petal-path-v1`.
- All UI screens are HTML/CSS. The in-level world is canvas.
- No in-level HUD. The only transient in-level visual feedback is the optional Tier 3 hint arrow.
- “Effects: none” means no particles, no screen shake, no flash, no post-processing. State changes such as a door opening or a secret blooming are allowed.
- Colour identification is never colour-only. Every interactive or informational tile has a shape icon:
  - circle key/door: dot/circle
  - triangle key/door: small leaf/triangle
  - switch: flower plate
  - secret: blossom
  - exit: gate
  - landmarks: lantern, flower, stone
- Reduced motion must disable:
  - idle sway
  - hint arrow wiggle
  - win hop
  - CSS button transition animation
  - any decorative motion not required for state clarity
- Remapped keys use `KeyboardEvent.code`, not visible key labels.

# 2. CONTRACTS

## 2.1 Module layout

| File | Responsibility |
| --- | --- |
| `index.html` | Canvas, HTML screens, settings forms, button wiring. |
| `styles.css` | Pastel hand-drawn CSS, screen layout, reduced-motion class, typography. |
| `js/main.js` | Boot, module imports, initial state, UI binding. |
| `js/loop.js` | Fixed-step loop, accumulator, update/render dispatch. |
| `js/input.js` | Keyboard events, held/pressed sets, remapping, action queries. |
| `js/audio.js` | Web Audio context, synthesized SFX, music loops, volume. |
| `js/state.js` | Global context, screen transitions, save/load, restart. |
| `js/levels.js` | Level maps, parser, level factory, level roster. |
| `js/entities.js` | Entity creation helpers for keys, doors, switches, secrets, landmarks. |
| `js/movement.js` | Player input vector, velocity, facing, position update. |
| `js/collision.js` | Tile lookup, circle-vs-tile collision, blocked checks. |
| `js/puzzles.js` | Key/door/switch/secret rules. |
| `js/hint.js` | Hint target selection, timer, cooldown, drawing data. |
| `js/progression.js` | Unlock/complete logic. |
| `js/render.js` | Canvas drawing, hand-drawn recipes, entity/player rendering. |
| `js/ui.js` | Screen state machine, button handlers, settings UI. |
| `js/debug.js` | `window.debug` API. |
| `js/tests.js` | High-level tier validation tests. |

## 2.2 Global context

```js
window.game = {
  screen: 'title',
  prevScreen: null,

  levelIndex: 0,
  level: null,

  player: null,
  carrying: new Set(),
  secretLeaves: 0,

  hint: {
    active: false,
    timer: 0,
    cooldown: 0,
    target: null
  },

  win: {
    active: false,
    timer: 0
  },

  progress: {
    completed: [false, false, false, false, false, false],
    unlocked: [true, false, false, false, false, false]
  },

  settings: {
    reducedMotion: false,
    musicVolume: 0.6,
    sfxVolume: 0.8,
    keyMap: {
      up: ['KeyW', 'ArrowUp'],
      down: ['KeyS', 'ArrowDown'],
      left: ['KeyA', 'ArrowLeft'],
      right: ['KeyD', 'ArrowRight'],
      hint: ['KeyH'],
      restart: ['KeyR'],
      pause: ['Escape'],
      confirm: ['Enter'],
      cancel: ['Escape']
    }
  },

  input: {
    held: new Set(),
    pressed: new Set()
  },

  audio: {
    ready: false,
    ctx: null,
    masterGain: null,
    musicGain: null,
    sfxGain: null,
    music: 'title',
    musicTimer: null
  },

  time: 0,
  dt: 1 / 60,
  rng: mulberry32(0x9E3779B9)
};
```

Level record:

```js
game.level = {
  id: 1,
  name: 'First Sprout',
  rows: 9,
  cols: 11,
  grid: [
    '###########',
    '#@.......E#'
  ],
  start: { x: 1, y: 1 },
  exit: { x: 9, y: 1 },
  keys: [
    {
      id: 'L2-key-circle-1',
      x: 3,
      y: 6,
      pattern: 'circle',
      collected: false
    }
  ],
  doors: [
    {
      id: 'L2-door-circle-1',
      x: 5,
      y: 4,
      type: 'keyed',
      pattern: 'circle',
      open: false
    }
  ],
  switches: [
    {
      id: 'L3-switch-1',
      x: 4,
      y: 2,
      on: false,
      doorId: 'L3-door-switch-1'
    }
  ],
  secrets: [
    {
      id: 'L2-secret-1',
      x: 9,
      y: 7,
      found: false
    }
  ],
  landmarks: [
    {
      id: 'L1-landmark-1',
      x: 4,
      y: 7,
      type: 'lantern'
    }
  ]
};
```

Player record:

```js
game.player = {
  x: 48,
  y: 48,
  vx: 0,
  vy: 0,
  radius: 10,
  facing: 'down',
  state: 'idle',
  animTime: 0,
  stateTimer: 0
};
```

Hint target record:

```js
// target is one of:
{ type: 'switch', id: 'L3-switch-1' }
{ type: 'key', id: 'L2-key-circle-1' }
{ type: 'door', id: 'L2-door-circle-1' }
{ type: 'exit' }
```

## 2.3 Module specifics

| Module | Required functions |
| --- | --- |
| `loop.js` | `startLoop()`, `tick(now)`, `step(dt)`, `render()` |
| `input.js` | `init()`, `onKeyDown(e)`, `onKeyUp(e)`, `actionHeld(action)`, `actionPressed(action)`, `clearPressed()`, `bindRemapListener(callback)`, `actionLabel(action, code)` |
| `audio.js` | `init()`, `ensureContext()`, `playSfx(name)`, `setMusic(name)`, `stopMusic()`, `setVolumes()`, `resume()` |
| `state.js` | `setScreen(screen)`, `goTitle()`, `goLevelSelect()`, `startLevel(index)`, `restartLevel()`, `completeLevel()`, `loadProgress()`, `saveProgress()`, `applySettingsClass()` |
| `levels.js` | `getLevelRaw(index)`, `parseLevel(index, raw)`, `createLevel(index)`, `resetLevelEntities(index)` |
| `entities.js` | `makeKey(levelIndex, x, y, pattern)`, `makeDoor(levelIndex, x, y, type, pattern)`, `makeSwitch(levelIndex, x, y, doorId)`, `makeSecret(levelIndex, x, y)`, `makeLandmark(levelIndex, x, y, type)` |
| `movement.js` | `updatePlayer(dt)`, `getMoveVector()`, `setFacingFromVector(dx, dy)` |
| `collision.js` | `tileAtPx(x, y)`, `tileTypeAt(x, y)`, `isBlockedTile(x, y)`, `moveCircle(x, y, radius, dx, dy)` |
| `puzzles.js` | `updatePuzzles(dt)`, `collectKey(key)`, `tryOpenDoors()`, `activateSwitch(sw)`, `triggerSecret(sec)`, `doorIsOpen(door)`, `keyMatchesDoor(key, door)` |
| `hint.js` | `updateHint(dt)`, `requestHint()`, `getHintTarget()`, `hintTargetPosition(target)` |
| `progression.js` | `isUnlocked(index)`, `markCompleted(index)`, `unlockNext(index)` |
| `render.js` | `renderLevel()`, `renderPlayer()`, `renderEntities()`, `renderHint()`, `drawHandText(text, x, y, size, align)` |
| `ui.js` | `showScreen(name)`, `bindUI()`, `updateLevelSelectButtons()`, `updateSettingsUI()`, `handleSettingsChange()`, `startRebind(action)` |

# 3. VISUAL SPEC

`Petal Path` looks like a soft watercolour garden notebook page seen from directly above. The maze is a small hand-painted garden plot: pale cream paper floor, washed pastel walls, thin ink lines, and little drawn landmarks. The player is a tiny sprout with a round body and one leaf. All interactive objects are readable by shape as well as colour. The visual language is calm, rounded, and slightly irregular, as if drawn with brush pen and watercolour. There is no perspective, no depth of field, no shadow casting, and no dynamic lighting.

Lighting and atmosphere are simulated, not rendered: the world feels like daytime under a soft overcast sky. Colours are low-contrast pastels on warm paper. Walls are the darkest large surfaces, while the floor is the lightest surface. Ink lines provide readability. There are no animated light sources, no glow, no bloom, no particles, and no post-processing. The atmosphere comes from palette, rounded shapes, and static hand-drawn texture.

The space is top-down and fully visible. Each level is centered in the 960×600 logical canvas. The background outside the level is plain paper with a faint static speckle. Level borders are wall tiles. The player, keys, doors, switches, secrets, and landmarks all occupy one tile and are drawn with a consistent 32 px tile recipe.

| Visual element | Recipe |
| --- | --- |
| Paper background | Fill `#fbf6ec`. Add 120 static 1 px speckles using level seed, colour `#f0e8d8`, alpha 0.35. |
| Floor tile | Fill `#fdfaf3`. Draw a 1 px ink corner dot at each tile corner with 50% probability from level seed, colour `#e6dcc8`. |
| Wall tile | Rounded rectangle inset 2 px. Fill wash `#d9e4f3`. Inner highlight `#e8f0fa`. Ink outline `#5b5b66`, 2 px, with ±0.5 px deterministic jitter. |
| Player Pip | 20 px body ellipse `#f7e3a5`, 12 px leaf `#a8c9a0`, ink outline `#5b5b66`, 2 px. |
| Circle key/door | 10 px filled circle `#7bb3d0`, ink outline, centre dot `#fbf6ec`. |
| Triangle key/door | 12 px rounded triangle/leaf `#f2b6a3`, ink outline, small stem line. |
| Circle keyed door | Closed: wall tile with circle cutout. Open: floor tile with faint circle stamp. |
| Triangle keyed door | Closed: wall tile with triangle cutout. Open: floor tile with faint triangle stamp. |
| Switch door | Closed: wall tile with flower cutout. Open: floor tile with faint flower stamp. |
| Bloom switch | 14 px flower plate `#a7c2a0`, ink outline. Off: closed bud. On: four petals visible. |
| Secret blossom | 12 px lavender blossom `#c8b8e5`, ink outline. Found: 16 px open blossom. |
| Exit gate | 24 px rounded gate `#f5d98b`, ink outline, two vertical bars. |
| Lantern landmark | 16 px lantern `#f5d98b`, ink outline, soft yellow inner circle. |
| Flower landmark | 14 px flower `#f2b6a3`, green centre `#a8c9a0`. |
| Stone landmark | 16 px rounded stone `#b7c4c2`, ink outline, small moss dot. |
| Hint arrow | 64 px hand-drawn arrow, ink `#5b5b66`, 4 px stroke, slight deterministic wiggle unless reduced motion. |
| Typography | Font stack `"Segoe Print", "Bradley Hand", "Comic Neue", cursive`. Button text 18 px, headings 32 px. Each UI element gets deterministic rotation from -0.6° to 0.6° and a 2 px ink underline with rounded ends. |

# 4. GAMEPLAY SPEC

You play Pip, a small sprout moving through six pastel garden mazes. The only goal is to reach the hand-drawn exit gate. Some mazes contain petal keys that open matching locked doors, and some contain bloom switches that open switch doors. Optional secret blossoms can be touched to add a leaf to Pip, but they never block or unblock the path. Landmarks help you find your way. There are no enemies, traps, timers, score, or inventory screens. If Pip gets stuck, the player can restart the level.

## 4.1 Level roster

| Level | Name | Size rows×cols | Focus | Target time | Map |
| --- | --- | ---: | --- | ---: | --- |
| 1 | First Sprout | 9×11 | Plain maze, exit only | 1–2 min | See below |
| 2 | Petal Gate | 9×11 | Circle key and circle door | 2–3 min | See below |
| 3 | Lantern Switch | 9×11 | Bloom switch and switch door | 2–3 min | See below |
| 4 | Twin Gates | 11×13 | Two keyed doors, two keys | 3–5 min | See below |
| 5 | Echo Garden | 11×13 | Switch door plus keyed door | 3–5 min | See below |
| 6 | Meadow Heart | 13×15 | Switch door plus two keyed doors | 4–6 min | See below |

Level 1 map:

```text
###########
#@.......E#
#.#####.#.#
#.#...#.#.#
#.#####.#.#
#.#...#...#
#.#####.###
#...L...#.#
###########
```

Level 2 map:

```text
###########
#@...#...E#
#.#..#.#..#
#.#..#.#..#
#.#..o.#..#
#.#..#.#..#
#.#O.#.#..#
#L#..#.#.?#
###########
```

Level 3 map:

```text
###########
#@...#...E#
#.#.*#.#..#
#.#..#.#..#
#.#..#.#..#
#.#..D.#..#
#.#..#.#..#
#.#..#.#..#
#L#..#.#.?#
###########
```

Level 4 map:

```text
#############
#@..#...#..E#
#...#...#...#
#...#...#...#
#.O.#.A.#...#
#...o...a...#
#...#...#...#
#...#...#...#
#L..#?..#F..#
#...#...#...#
#############
```

Level 5 map:

```text
#############
#@..#...#..E#
#...#...#...#
#...#...#...#
#.*..#.O.#...#
#...D...o...#
#...#...#...#
#...#...#...#
#L..#?..#F..#
#...#...#...#
#############
```

Level 6 map:

```text
###############
#@..#...#...#E#
#...#...#...#.#
#...#...#...#.#
#.*..#.O.#.A.#.#
#...D...o...a.#
#...#...#...#.#
#...#...#...#.#
#L..#F..#?..#R#
#...#...#...#.#
#...#...#...#.#
#...#...#...#.#
###############
```

## 4.2 Object counts

| Level | Circle keys | Triangle keys | Circle doors | Triangle doors | Switch doors | Switches | Secrets | Landmarks |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 2 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 1 |
| 3 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 |
| 4 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 2 |
| 5 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 2 |
| 6 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 3 |

Switch-door links use 1-based map coordinates:

| Level | Switch position | Linked switch door position |
| ---: | --- | --- |
| 3 | col 5, row 3 | col 6, row 5 |
| 5 | col 3, row 5 | col 5, row 6 |
| 6 | col 3, row 5 | col 5, row 6 |

## 4.3 Player movement — Tier 1

Rules:

- Movement input is continuous real-time.
- Each simulation step, input actions produce a vector:
  - up: `(0, -1)`
  - down: `(0, 1)`
  - left: `(-1, 0)`
  - right: `(1, 0)`
- If multiple movement keys are held, sum the vectors and normalize.
- Velocity is instant: `vx = normalizedX * 112`, `vy = normalizedY * 112`.
- No acceleration and no friction.
- Player position updates in pixels: `x += vx * dt`, `y += vy * dt`.
- Collision is resolved axis-by-axis using the player’s 10 px radius circle against wall and closed door tiles.
- Facing updates while moving:
  - if `abs(dx) > abs(dy)`, facing is `left` or `right`;
  - otherwise facing is `up` or `down`;
  - if `dx == 0` and `dy == 0`, facing does not change.
- The player cannot leave the level border.
- The player state is `idle` when velocity is zero and `move` otherwise.
- Restart sets player position to start tile centre:
  - `x = startX * 32 + 16`
  - `y = startY * 32 + 16`

## 4.4 Exploration: Secrets — Tier 1 basic, Tier 2 complete

Secrets are optional hidden blossoms marked `?`.

Rules:

- A secret is a walkable tile.
- When the player’s circle overlaps the secret tile centre by at least 50% of the secret’s 12 px diameter, the secret triggers immediately.
- Triggering a secret:
  - sets `found = true`
  - increments `game.secretLeaves` by 1
  - plays `secret_bloom`
  - visually blooms the secret from 12 px to 16 px
  - adds one decorative leaf to Pip for the rest of the level
- Secrets do not open doors, unlock levels, change hints, affect the exit, or create failure.
- Maximum secrets per level is 3.
- Restart resets all secrets in the level to `found = false` and sets `game.secretLeaves = 0`.

## 4.5 Exploration: Keys and locked doors — Tier 1 basic, Tier 2 complete

Petal keys are walkable pickups. Locked doors are closed by default.

Key rules:

- Key patterns are exactly:
  - `circle`
  - `triangle`
- Touching a key tile collects it immediately.
- Collecting a key:
  - adds its pattern to `game.carrying`
  - sets `collected = true`
  - plays `key_collect`
  - changes the key visual to a faint spent petal stamp on the floor
- Keys are not consumed.
- Carried keys persist for the rest of the current level only.
- Restart clears `game.carrying`.

Keyed door rules:

- Keyed door types are exactly:
  - circle door `o`, pattern `circle`
  - triangle door `a`, pattern `triangle`
- A keyed door is closed unless `open = true`.
- A closed keyed door blocks movement.
- An opened keyed door behaves as floor.
- When the player overlaps a closed keyed door tile:
  - if the door’s pattern is in `game.carrying`, the door opens immediately;
  - otherwise nothing happens.
- Door opening:
  - sets `open = true`
  - plays `door_open`
  - sets the door visual to floor with a faint pattern stamp
- Doors do not close again during the level.
- Restart closes all doors.

## 4.6 Exploration: Landmarks — Tier 1 basic, Tier 2 complete

Landmarks are static visual anchors.

Landmark types:

| Map char | Type | Visual |
| --- | --- | --- |
| `L` | lantern | small glowing-looking lantern, no dynamic glow |
| `F` | flower | pastel flower |
| `R` | stone | rounded mossy stone |

Rules:

- Landmarks are walkable.
- Landmarks have no gameplay effect.
- Landmarks do not interact with keys, switches, secrets, hints, or the exit.
- Landmarks persist through the level and restart.
- Their only purpose is wayfinding and cozy visual variety.

## 4.7 Puzzles: Puzzle types — Tier 2

The game has exactly two puzzle types:

1. Keyed Door puzzle: find the matching petal key, then touch the matching locked door.
2. Switch Door puzzle: touch the bloom switch, then touch the linked switch door.

No other puzzle types exist.

## 4.8 Puzzles: Hints — Tier 3

Hints are requested by the remappable `hint` key, default `KeyH`.

Rules:

- A hint can be requested only in the `level` screen.
- A hint cannot be requested if:
  - the win delay is active, or
  - a hint is already active, or
  - `game.hint.cooldown > 0`.
- On successful request:
  - `game.hint.active = true`
  - `game.hint.timer = 3.0`
  - `game.hint.cooldown = 5.0`
  - `game.hint.target` is set by `getHintTarget()`
  - `hint` SFX plays.
- The hint arrow is drawn from the player’s centre toward the target’s tile centre.
- Arrow length is 64 px.
- Arrow width is 4 px.
- Arrow colour is ink `#5b5b66`.
- If reduced motion is off, the arrow has a ±1 px deterministic wiggle at 1 Hz.
- If reduced motion is on, the arrow is static.
- After 3.0 seconds, `active = false` and `timer = 0`.
- Cooldown decrements by `dt` every simulation step.

Hint target selection, in priority order:

1. If any switch door is closed and its linked switch is off:
   - choose the nearest such switch.
   - target type: `switch`.
2. Else if any keyed door is closed:
   - For each closed keyed door:
     - if its pattern is not in `game.carrying`, candidate is the nearest key with that pattern;
     - if its pattern is in `game.carrying`, candidate is that door.
   - choose the nearest candidate by Euclidean distance from the player.
   - target type: `key` or `door`.
3. Else:
   - target is the exit tile.
   - target type: `exit`.

## 4.9 Puzzles: Switches and doors — Tier 2

Bloom switches are floor plates marked `*`. Switch doors are marked `D`.

Switch rules:

- A switch is a walkable tile.
- When the player’s circle overlaps the switch tile centre by at least 50% of the switch’s 14 px diameter, the switch activates immediately.
- Activating a switch:
  - sets `on = true`
  - opens its linked switch door immediately
  - plays `switch_bloom`
  - changes the switch visual from closed bud to four-petal bloom
- Switches do not toggle off.
- A switch remains on for the rest of the level.
- Restart resets switches to `on = false` and closes linked switch doors.

Switch door rules:

- A switch door is closed unless its linked switch is on.
- A closed switch door blocks movement.
- An opened switch door behaves as floor.
- When a switch activates, its linked door:
  - sets `open = true`
  - plays `door_open` if the door was closed
  - changes visual to floor with a faint flower stamp.
- Switch doors do not close again during the level.

## 4.10 Progression and difficulty — Tier 1 basic, Tier 2 complete

Progression is a linear sequence of six levels.

Rules:

- Level 1 is unlocked at start.
- Completing level `n` sets:
  - `progress.completed[n] = true`
  - `progress.unlocked[n + 1] = true`, if `n + 1 < 6`.
- Level select shows all six level buttons.
- Locked buttons are disabled and show a small ink cross.
- Completed buttons show a small blossom icon.
- Replaying a completed level does not change completion.
- There is no difficulty selection, no score, no par time, and no penalty for restarting.

Difficulty increases only by:

- larger grid
- more required keys
- more required switches
- longer route to exit
- more secret/landmark visual variety

## 4.11 Feel

- Movement should feel smooth and immediate.
- Door opening is instant on contact.
- Switch activation is instant on contact.
- Key collection is instant on contact.
- Secret triggering is instant on contact.
- The win sequence is short: 0.35 second pause, then win screen.
- Audio is soft and sparse.
- Visual feedback is state change, not particles.
- Restart is forgiving and immediate.

# 5. CHARACTERS

There is one character: Pip the sprout.

Silhouette:

- Small vertical sprout.
- Round bottom body.
- One leaf on top.
- Soft pastel fill with a thin ink outline.
- 20 px tall inside a 32 px tile.
- Easy to read against floor and walls.

Facings:

| Facing | Visual change |
| --- | --- |
| up | leaf slightly higher, body rounded |
| down | leaf slightly forward, body rounded |
| left | leaf tilted left |
| right | leaf tilted right |

States:

| State | Trigger | Motion rule | Reduced motion |
| --- | --- | --- | --- |
| `idle` | velocity zero | 0.5 px vertical sway at 0.5 Hz unless reduced motion | no sway |
| `move` | velocity nonzero | leaf bob 3 px over 0.36 s cycle; facing snaps to dominant axis | no bob |
| `collect` | key collected | scale to 1.10 for 0.10 s, then 1.00 for 0.05 s | instant scale only |
| `open` | door opens by contact | lean 4 px toward door for 0.10 s | no lean |
| `switch` | switch activates | lean 3 px toward switch for 0.10 s | no lean |
| `secret` | secret triggers | add one leaf visual to Pip for rest of level | instant leaf |
| `win` | exit entered | hop 6 px up twice over 0.60 s before win screen | no hop |

# 6. AUDIO

All audio is synthesized. No audio files are required.

| Sound | Recipe | When it plays |
| --- | --- | --- |
| `ui_click` | Sine 660 Hz, 60 ms, gain 0.12, 5 ms attack, 30 ms release, lowpass 2205 Hz | Any confirm/click on title, level select, pause, settings, win. |
| `ui_back` | Sine 440 Hz, 60 ms, gain 0.10, 5 ms attack, 30 ms release, lowpass 1800 Hz | Back button, cancel action, closing settings. |
| `level_start` | Sine 392 Hz, 80 ms, gain 0.14, 5 ms attack, 40 ms release, lowpass 2400 Hz | Starting or restarting a level. |
| `key_collect` | Triangle 523 Hz to 784 Hz over 90 ms, gain 0.18, lowpass 3000 Hz | Pip touches a petal key. |
| `door_open` | Sine 330 Hz to 392 Hz over 140 ms, gain 0.18, lowpass 2600 Hz | Any locked door opens. |
| `switch_bloom` | Sine 262 Hz to 330 Hz over 120 ms, gain 0.16, lowpass 2200 Hz | Bloom switch activates. |
| `secret_bloom` | Triangle 587 Hz, 100 ms, gain 0.14, 5 ms attack, 50 ms release, lowpass 2800 Hz | Secret blossom triggers. |
| `hint` | Sine 440 Hz, 200 ms, gain 0.10, 10 ms attack, 100 ms release, lowpass 1800 Hz | Hint arrow appears. |
| `restart` | Sine 330 Hz to 262 Hz over 100 ms, gain 0.12, lowpass 2200 Hz | Player restarts level. |
| `win` | Triangle notes 262, 330, 392, 523 Hz, 100 ms each, 20 ms gaps, gain 0.18, lowpass 3200 Hz | Win screen appears. |
| `music_title` | Plucked triangle arpeggio C4-E4-G4-B4-C5, 70 BPM, 8th notes, gain 0.18, lowpass 2500 Hz, soft sine piano pad C4 at 0.10 gain | Title screen, after first user gesture. |
| `music_level` | Plucked triangle pattern C4-D4-E4-G4-E4-D4-C4-D4, 82 BPM, gain 0.16, lowpass 2200 Hz, soft sine bass C3 at 0.08 gain | In-level play, pause keeps music low but continues. |

# 7. UX

The UX uses HTML and CSS only for screens. The in-level canvas has no HUD.

## 7.1 Screen state machine

| Current screen | Event | Next screen | Notes |
| --- | --- | --- | --- |
| `title` | Confirm / “Begin” | `levelSelect` | Plays `ui_click`. |
| `title` | “Settings” | `settings` | `prevScreen = 'title'`. |
| `levelSelect` | Click unlocked level | `level` | Starts selected level. |
| `levelSelect` | “Back” | `title` | Plays `ui_back`. |
| `level` | `pause` key or pause button equivalent | `pause` | Simulation stops. |
| `pause` | “Resume” | `level` | Simulation resumes. |
| `pause` | “Restart” | `level` | Resets current level. |
| `pause` | “Settings” | `settings` | `prevScreen = 'pause'`. |
| `pause` | “Level Select” | `levelSelect` | Abandons current level without saving completion. |
| `settings` | “Back” | `prevScreen` | Applies settings. |
| `level` | Player enters exit | `win` | After 0.35 s win delay. |
| `win` | “Next” | `level` or `levelSelect` | If next level exists, start it; if final, go to level select. |
| `win` | “Replay” | `level` | Restarts current level. |
| `win` | “Level Select” | `levelSelect` | Returns to selection. |

## 7.2 HUD table

| Element | Record field | When visible |
| --- | --- | --- |
| No in-level HUD | none | never |
| No timer | none | never |
| No key count | none | never |
| No hint counter | none | never |
| No secret counter | none | never |

## 7.3 Screen content

| Screen | Required elements |
| --- | --- |
| Title | Game title `Petal Path`, “Begin”, “Settings”, soft paper background. |
| Level Select | Six level buttons in a 3×2 grid, each showing level number and name. Locked buttons disabled. Completed buttons show a small blossom icon. “Back” button. |
| Pause | “Resume”, “Restart”, “Settings”, “Level Select”. |
| Settings | Reduced motion toggle, music volume slider, SFX volume slider, key remap list, “Back”. |
| Win | “Reached the Garden Gate”, optional row of blossom icons representing secrets found in that level, “Next”, “Replay”, “Level Select”. |

Key remap UI:

- List actions: `up`, `down`, `left`, `right`, `hint`, `restart`, `pause`.
- Clicking an action enters rebind mode.
- The next `KeyboardEvent.code` becomes the new key for that action.
- `Escape` cancels rebind without changing the binding.
- Remapping persists immediately.

# 8. DEBUG API

`window.debug` is available in all tiers after boot.

| Namespace | Function | Effect |
| --- | --- | --- |
| `screen` | `debug.screen.set(name)` | Force screen: `title`, `levelSelect`, `pause`, `settings`, `win`, `level`. |
| `level` | `debug.level.load(index)` | Load level 0–5 immediately. |
| `level` | `debug.level.reset()` | Restart current level. |
| `player` | `debug.player.setPosition(x, y)` | Set player pixel position. |
| `player` | `debug.player.setVelocity(vx, vy)` | Set player velocity for one step. |
| `player` | `debug.player.setFacing(facing)` | Set facing: `up`, `down`, `left`, `right`. |
| `player` | `debug.player.addKey(pattern)` | Add `circle` or `triangle` to carrying. |
| `player` | `debug.player.setSecretLeaves(n)` | Set decorative leaf count 0–3. |
| `input` | `debug.input.press(action)` | Add action to held and pressed sets. |
| `input` | `debug.input.release(action)` | Remove action from held set. |
| `input` | `debug.input.simulateMove(dx, dy, seconds)` | Apply direct player movement over `seconds` of fixed steps. |
| `keys` | `debug.keys.collectAll()` | Collect all uncollected keys in current level. |
| `keys` | `debug.keys.spawn(pattern, x, y)` | Spawn a key at tile coordinates. |
| `doors` | `debug.doors.setOpen(id, open)` | Set door open state. |
| `doors` | `debug.doors.setAllOpen(open)` | Set all doors in current level. |
| `switches` | `debug.switches.set(id, on)` | Set switch state and linked door accordingly. |
| `switches` | `debug.switches.setAll(on)` | Set all switches and linked doors. |
| `secrets` | `debug.secrets.set(id, found)` | Set secret found state. |
| `secrets` | `debug.secrets.setAll(found)` | Set all secrets. |
| `landmarks` | `debug.landmarks.set(id, type)` | Change landmark type: `lantern`, `flower`, `stone`. |
| `hint` | `debug.hint.show(target)` | Force hint target and activate for 3 seconds. |
| `hint` | `debug.hint.setCooldown(seconds)` | Set hint cooldown. |
| `progress` | `debug.progress.setCompleted(index, value)` | Set completion for level 0–5. |
| `progress` | `debug.progress.setUnlocked(index, value)` | Set unlock for level 0–5. |
| `audio` | `debug.audio.play(name)` | Play an SFX from the audio table. |
| `audio` | `debug.audio.setMusic(name)` | Play `title` or `level` music. |
| `settings` | `debug.settings.setReducedMotion(value)` | Toggle reduced motion. |
| `settings` | `debug.settings.remap(action, code)` | Remap an action to a key code. |
| `time` | `debug.time.set(seconds)` | Set `game.time`. |

# 9. TESTS

## Tier 1 tests

- Boot test: page loads, title screen visible, canvas present, no JS errors.
- Input test: default WASD and arrow keys produce expected movement vectors.
- Movement test: holding one direction for 1.0 simulated seconds moves the player approximately 112 px on an open floor.
- Collision test: player cannot enter wall tiles or closed door tiles.
- Facing test: moving left/right/up/down sets facing correctly.
- Level 1 test: start at `@`, exit reachable, entering `E` triggers win delay and win screen.
- Level 2 key test: circle door blocks exit until circle key is collected; after collecting key, touching door opens it.
- Restart test: pressing default `KeyR` in level returns player to start, clears carried key, closes doors, resets secrets.
- Pause test: pressing default `Escape` pauses, resume continues same level state.
- Settings test: toggling reduced motion adds/removes `reduced-motion` CSS class; remapping a movement key changes input response.
- Persistence test: completing Level 1 unlocks Level 2 after page reload using `localStorage`.
- Screen test: exactly title, level select, pause, settings, win, and level states are reachable from the state machine.
- HUD test: no DOM elements with `data-hud` are visible while `screen === 'level'`.
- Audio test: first user gesture initializes audio; `ui_click`, `key_collect`, `door_open`, and `win` SFX are callable.

## Tier 2 tests

- Level 3 switch test: switch door blocks path; touching switch opens linked switch door permanently.
- Level 4 test: both circle and triangle keys are required; opening one door does not open the other; order can be either.
- Level 5 test: switch door must open before exit route is clear; circle key must open circle door.
- Level 6 test: switch door, circle door, and triangle door can all be opened; level completes only after all required doors are open.
- Secrets test: triggering each secret sets `found = true`, increments `secretLeaves`, and does not affect exit reachability.
- Landmarks test: all landmark tiles are walkable and do not alter doors, keys, switches, secrets, or hints.
- Progression test: Level Select locks later levels until previous levels are completed; completed levels show blossom icon.
- Restart test: restart Level 6 resets three doors, one switch, two keys, one secret, and player carrying.
- Colour-blind test: circle and triangle keys/doors are distinguishable by shape icons in DOM/canvas snapshot or unit assertion of icon type.

## Tier 3 tests

- Hint cooldown test: pressing hint twice within 5 seconds does not create a second hint.
- Hint duration test: hint arrow disappears after 3.0 simulated seconds.
- Hint target test:
  - Level 3 with switch off points to switch.
  - Level 2 before key points to circle key.
  - Level 2 after key but before door points to circle door.
  - Level 4 with both keys missing points to nearest missing key.
  - Level 6 with switch on and both keys missing points to nearest missing key.
- Reduced motion test: with reduced motion enabled, idle sway, hint wiggle, and win hop are disabled.
- Full audio test: every SFX in §6 plays without error; volume sliders change gain values.
- Visual recipe test: wall, floor, key, door, switch, secret, exit, and landmark draw calls use the palette values in §3.
- Debug API test: every `window.debug` function listed in §8 runs without error and changes the expected state.

# 10. BUILD ORDER

1. Scaffold `index.html`, canvas, CSS screens, and hand-lettered typography.
2. Implement global context, fixed-step loop, and screen state machine.
3. Implement input system with held/pressed sets and default key map.
4. Implement settings, persistence, reduced motion, and remappable keys.
5. Implement level parser and Level 1–Level 2 data.
6. Implement movement, collision, player facing, and restart.
7. Implement exit win, win screen, completion, and level select unlock.
8. Implement minimal audio: context, UI click, level music, win SFX.
9. Implement keys, keyed doors, landmarks, and secrets for Level 1–Level 2.
10. Add Level 3–Level 6 maps and entity data.
11. Implement switches and switch doors.
12. Implement hint target selection, hint timer, and hint arrow.
13. Implement full audio table and volume settings.
14. Implement visual recipe for all tiles, player states, landmarks, secrets, and doors.
15. Implement debug API and high-level tier tests.
16. Run tier tests and polish hand-drawn irregularity.

# 11. DEFINITION OF DONE

## Tier 1 done

High-level: A player can start from the title screen, enter Level 1 or Level 2, move freely, solve at least one locked door, reach the exit, and restart if needed, with accessibility settings working and no HUD visible.

- [ ] Title screen loads and “Begin” goes to level select.
- [ ] Level select shows Level 1 unlocked and Level 2 locked.
- [ ] Level 1 loads with correct start and exit.
- [ ] Player moves with default WASD and arrow keys.
- [ ] Player collides correctly with walls.
- [ ] Reaching exit in Level 1 shows win screen and completes Level 1.
- [ ] Level 2 unlocks after Level 1 completion.
- [ ] Level 2 circle key opens circle door.
- [ ] Restart returns player to start and resets level state.
- [ ] Pause screen opens and closes correctly.
- [ ] Settings screen toggles reduced motion and remaps keys.
- [ ] Settings persist after reload.
- [ ] No in-level HUD elements are visible.
- [ ] Minimal audio plays after first user gesture.
- [ ] No enemies, traps, timers, score, or extra systems are present.

## Tier 2 done

High-level: All six levels are playable, all listed keys, doors, switches, secrets, and landmarks work, and sequential progression is complete.

- [ ] All six level maps parse correctly.
- [ ] Level 3 switch door opens after touching switch.
- [ ] Level 4 requires both circle and triangle keys.
- [ ] Level 5 requires switch door and circle door.
- [ ] Level 6 requires switch door, circle door, and triangle door.
- [ ] All switch-door links match §4.2.
- [ ] All secrets trigger and add leaves without affecting exit.
- [ ] All landmarks are walkable and purely visual.
- [ ] Restart resets all doors, switches, keys, secrets, and carrying.
- [ ] Level select unlock/completion icons update correctly.
- [ ] Total designed session remains under 30 minutes.
- [ ] No systems beyond listed systems are present.

## Tier 3 done

High-level: Hints, full audio, visual recipe, accessibility polish, debug API, and tests are complete.

- [ ] Hint key shows arrow for 3.0 seconds.
- [ ] Hint cooldown is 5.0 seconds.
- [ ] Hint target priority matches §4.8.
- [ ] Hint arrow points to switch, key, door, or exit correctly.
- [ ] Reduced motion disables idle sway, hint wiggle, and win hop.
- [ ] All SFX in §6 are implemented and callable.
- [ ] Music title and level music are synthesized and switch correctly.
- [ ] Volume sliders affect music and SFX gain.
- [ ] All visual elements use the palette and shape icons in §3.
- [ ] Player animations match §5.
- [ ] `window.debug` implements every function in §8.
- [ ] Tier 1, Tier 2, and Tier 3 tests pass.
- [ ] No particles, screen shake, flashes, or post-processing effects exist.

# A. SANITY

| Check | Result | Notes / fix |
| --- | --- | --- |
| User request satisfied | Valid | The game is a single-player real-time top-down maze-solving game. |
| Only listed systems present | Valid | No enemies, traps, hazards, score, timer, inventory, or meta progression beyond level unlock. |
| Screens exact | Valid | UI screens are title, level select, pause, settings, win, plus in-level play state. |
| HUD none | Valid | §7.2 explicitly states no in-level HUD. |
| Win/lose only reach exit | Valid | No lose state exists; win only occurs on exit tile. |
| Failure restart only | Valid | Restart is voluntary; no death or forced failure. |
| Effects none | Valid | No particles, screen shake, flashes, or post-processing. State changes are not effect systems. |
| Colour-blind safe | Valid | All interactive tiles have shape icons; palette avoids red/green-only identification. |
| Reduced motion | Valid | Setting disables idle sway, hint wiggle, win hop, and CSS transitions. |
| Remappable keys | Valid | Settings screen rebinds all gameplay actions using `KeyboardEvent.code`. |
| Palette pastel | Valid | Palette uses soft light colours with low-contrast pastels and ink lines. |
| Art style hand-drawn/painterly | Valid | Watercolor washes, ink outlines, paper speckles, irregular UI underlines. |
| Typography hand-lettered | Valid | Handwriting font stack plus deterministic rotation and ink underline. |
| Music acoustic | Valid | Synthesized plucked guitar/folk-like loops and soft piano-like tones. |
| SFX minimal | Valid | Only short soft clicks and tones. |
| Levels under 30 minutes | Valid | Target total time is 15–24 minutes. |
| Level maps solvable | Valid | Maps were checked for border walls, start/exit, key/door/switch access, and required paths. |
| Door/switch links correct | Valid | Switch links listed in §4.2 match maps in §4.1. |
| No extra pickups | Valid | Only petal keys and secret blossoms exist; landmarks are not pickups. |
| Fixed step loop specified | Valid | 60 Hz fixed step with accumulator and max frame clamp. |
| Random source specified | Valid | `mulberry32` seeded, no `Math.random`. |
| Debug API complete | Valid | §8 lists direct state access per system and player input functions. |
| Tests tied to tiers | Valid | §9 gives high-level tests for Tier 1, Tier 2, and Tier 3. |
| Definition of done workable | Valid | §11 gives tier-level high-level done plus checkbox details. |
| Potential contradiction: hint arrow vs effects none | Resolved | Hint arrow is a required puzzle aid and is treated as a transient UI glyph, not a particle/effect system. |
| Potential contradiction: static camera vs camera top-down | Resolved | Static top-down is a valid camera choice and is explicitly documented. |
| Potential contradiction: no HUD vs win screen blossom icons | Resolved | Win screen is a screen, not in-level HUD; blossom icons are optional feedback for the secret system. |
