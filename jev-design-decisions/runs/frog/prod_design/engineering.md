# engineering.md

## 1. Purpose and Handoff Contract

This document is the engineering source of truth for **FROG: POND TO PEAK**.

It implements the gameplay described in `gameplay.md` using vanilla HTML, CSS, and JavaScript only.

The integration agent should implement the game using only this document. If a decision is not explicitly made here, the implementation should choose the smallest deterministic option that satisfies the gameplay rules.

Important handoff constraints:

- No Node.
- No npm.
- No build step.
- No test runner.
- No external libraries.
- No modules required.
- Tests run inside a headless page as plain JavaScript.
- Tests drive the game through `window.__game`.
- Tests check state returned by `window.__game.getState()`.
- The game must be playable in a normal browser from `index.html`.
- The game must be testable from `test.html`.

This document owns:

- file layout
- runtime architecture
- deterministic update model
- level data format
- level validation
- physics and collision rules
- water, lily pad, moving platform, enemy, and boss logic
- save system
- HUD/UI state model
- audio event implementation
- debug API
- in-page test harness
- required test suite

This document does not own:

- level design decisions
- audio asset design
- visual asset design

The visual designer may replace placeholder visuals and provide final CSS/audio assets. The engineering implementation must make those assets work without changing gameplay logic.

---

## 2. Engineering Decisions and Why They Were Made

### 2.1 Use classic scripts instead of ES modules

Decision:

- Use classic `<script>` files.
- Use one global namespace: `window.FrogGame`.
- Expose debug API on `window.__game`.
- Expose test harness on `window.__test` in `test.html`.

Why:

- The project has no build step.
- ES modules can fail or behave differently when opened directly from `file://`.
- Classic scripts are easiest to syntax-check and load in a headless page.
- A single namespace keeps the code scalable without requiring a bundler.

Rule:

- Do not use `import` or `export`.
- Do not rely on module scope.
- Wrap each file in an IIFE.
- Attach only to `window.FrogGame`.
- Avoid creating extra globals.

Allowed globals:

```js
window.FrogGame
window.__game
window.__test          // test.html only
window.__testsDone     // test.html only
window.__testResults   // test.html only
```

---

### 2.2 Fixed logical timestep

Decision:

- Logic always updates in fixed steps of `dt = 1 / 60`.
- Rendering may happen at display refresh rate.
- Debug tests call `window.__game.step()` to advance logic deterministically.

Why:

- The gameplay document defines all movement in seconds and pixels per second.
- Tests must be deterministic.
- Real-time `requestAnimationFrame` timing must not affect gameplay assertions.
- A fixed timestep prevents physics behavior from changing between 60 Hz, 120 Hz, and 144 Hz displays.

Rule:

- All gameplay timers use seconds.
- All movement uses `dt = 1 / 60`.
- The browser loop may run multiple fixed updates after a slow frame.
- Clamp accumulated frame time to avoid a spiral of death.
- Debug `step()` does not use real time.

---

### 2.3 No procedural level generator in the shipped game

Decision:

- Do not generate levels procedurally.
- Levels are authored data.
- Provide a deterministic test-level factory for tests only.

Why:

- The gameplay designer has already authored six levels.
- Random level generation would make tests non-deterministic.
- A short linear platformer does not need procedural content.
- Data-driven levels are easier to validate and easier to hand off.

Rule:

- `js/levels.js` contains the six authored levels.
- `FrogGame.LevelData.testLevel()` creates deterministic test levels for tests.
- No seeded random generator is required.
- No runtime level generation is allowed in the shipped game.

---

### 2.4 DOM HUD and menus, canvas game world

Decision:

- Game world renders to a 1280 x 720 canvas.
- HUD and menus are DOM elements.
- CSS scales the game container while preserving aspect ratio.

Why:

- Text menus are easier to make readable and styleable with DOM.
- Canvas is better for the game world.
- The visual designer can style HUD/menus with CSS without touching game logic.
- Tests should not need to inspect canvas pixels.

Rule:

- Do not render HUD text on canvas.
- Do not render menu text on canvas.
- Game world rendering may use placeholder shapes if visual assets are missing.
- Logic must not depend on DOM measurements.

---

### 2.5 Debug API is required for tests

Decision:

- Expose `window.__game`.
- Tests may only interact with the game through `window.__game`.
- `window.__game.getState()` returns a serializable state object.

Why:

- There is no test runner.
- Headless tests need deterministic control.
- The game must be validatable without real keyboard events or real time.
- A debug API also helps humans test in the browser console.

Rule:

- The debug API must always exist after scripts load.
- The debug API must not be visible in the player UI.
- Tests must not access internal `FrogGame` objects directly.
- `getState()` must return plain objects/arrays only.
- `getState()` must not contain functions, DOM nodes, or canvas contexts.

---

### 2.6 Tests are integration tests, not unit tests

Decision:

- Tests drive the full game through `window.__game`.
- Tests check game state, not isolated functions.
- Tests do not require Node, npm, or a test runner.

Why:

- The goal is to prove the game is finished and playable.
- Unit tests would not prove that the systems integrate.
- The headless environment can only execute browser JavaScript.
- A small in-page harness is simpler and more portable.

Rule:

- `test.html` loads the game and test files.
- `test/test-harness.js` provides a minimal test runner.
- `test/tests.js` registers and runs tests.
- Tests must not use real timers.
- Tests must not require audio files.
- Tests must not require image files.
- Tests must not require network access.
- Tests must not require user interaction.

---

## 3. Required Files

The repository should contain these files:

```text
index.html
test.html
css/style.css

js/constants.js
js/utils.js
js/save.js
js/input.js
js/audio.js
js/assets.js
js/levels.js
js/level.js
js/collision.js
js/player.js
js/enemies.js
js/camera.js
js/hud.js
js/ui.js
js/game.js
js/debug.js
js/main.js

test/test-harness.js
test/tests.js

assets/audio/jump.ogg
assets/audio/water_splash.ogg
assets/audio/lily_pad_bounce.ogg
assets/audio/stomp.ogg
assets/audio/damage.ogg
assets/audio/checkpoint.ogg
assets/audio/level_complete.ogg
assets/audio/boss_hit.ogg
assets/audio/boss_death.ogg
assets/audio/game_complete.ogg

assets/images/optional visual assets
```

Notes:

- Audio files may be `.mp3` instead of `.ogg`. The audio manager should try `.ogg` first, then `.mp3`.
- Image assets are optional for logic and tests.
- If visual assets are missing, the game must still run with placeholders.
- If audio assets are missing, the game must still run silently.
- `test.html` is required for headless validation.
- `index.html` is required for normal play.

---

## 4. Script Order

`index.html` must load scripts in this order:

```html
<script src="js/constants.js"></script>
<script src="js/utils.js"></script>
<script src="js/save.js"></script>
<script src="js/input.js"></script>
<script src="js/audio.js"></script>
<script src="js/assets.js"></script>
<script src="js/levels.js"></script>
<script src="js/level.js"></script>
<script src="js/collision.js"></script>
<script src="js/player.js"></script>
<script src="js/enemies.js"></script>
<script src="js/camera.js"></script>
<script src="js/hud.js"></script>
<script src="js/ui.js"></script>
<script src="js/game.js"></script>
<script src="js/debug.js"></script>
<script src="js/main.js"></script>
```

`test.html` must load the same game scripts, then:

```html
<script src="test/test-harness.js"></script>
<script src="test/tests.js"></script>
```

`test.html` should also include a visible result container:

```html
<pre id="test-results"></pre>
```

---

## 5. Global Namespace Layout

Each JS file should follow this pattern:

```js
window.FrogGame = window.FrogGame || {};

window.FrogGame.Constants = (function () {
  "use strict";

  // file contents

  return {
    // public API
  };
})();
```

Required namespace members:

```js
FrogGame.Constants
FrogGame.Utils
FrogGame.Save
FrogGame.Input
FrogGame.Audio
FrogGame.Assets
FrogGame.LevelData
FrogGame.Level
FrogGame.Collision
FrogGame.Player
FrogGame.Enemies
FrogGame.Camera
FrogGame.HUD
FrogGame.UI
FrogGame.Game
FrogGame.Debug
FrogGame.main
```

`window.__game` is created by `js/debug.js`.

`window.__test` is created by `test/test-harness.js`.

---

## 6. HTML Structure

### 6.1 `index.html`

Required structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>FROG: POND TO PEAK</title>
  <link rel="stylesheet" href="css/style.css" />
</head>
<body>
  <div id="game">
    <canvas id="canvas" width="1280" height="720"></canvas>

    <div id="hud" class="hidden">
      <div id="hearts" class="hud-section hearts"></div>
      <div id="dewdrops" class="hud-section dewdrops"></div>
      <div id="message" class="hud-section message"></div>
    </div>

    <div id="ui">
      <div id="screen-title" class="screen hidden"></div>
      <div id="screen-controls" class="screen hidden"></div>
      <div id="screen-pause" class="screen hidden"></div>
      <div id="screen-level-complete" class="screen hidden"></div>
      <div id="screen-game-complete" class="screen hidden"></div>
    </div>
  </div>

  <!-- scripts -->
</body>
</html>
```

### 6.2 `test.html`

`test.html` should use the same `#game` structure and add:

```html
<pre id="test-results"></pre>
```

The test page may hide `#game` visually, but the DOM structure should exist because the game code may reference it.

---

## 7. CSS Contract

The visual designer owns final styling, but engineering requires these IDs/classes to exist:

```css
#game
#canvas
#hud
#hearts
#dewdrops
#message
#ui
.screen
.hidden
.menu-item
.menu-item.selected
.confirm
.heart
.heart.full
.heart.empty
.dewdrop-icon
```

Required layout behavior:

- `#game` maintains a 16:9 aspect ratio.
- `#canvas` is 1280 x 720 logical pixels.
- `#hud` is absolutely positioned over the canvas.
- `#ui` screens are absolutely positioned over the canvas.
- Hidden screens use `.hidden`.
- The game should be centered in the browser viewport.
- The game should scale to fit the window without changing logical resolution.

Required HUD placement:

- Hearts: top-left, 16 px from left and top.
- Heart icons: 32 x 32 px.
- Heart spacing: 8 px.
- Dewdrop count: top-right, 16 px from right and top.
- Dewdrop icon: 24 x 24 px.
- Dewdrop text: 18 px.
- Message: top-center, 48 px below top edge.
- Message max width: 600 px.

The visual designer may change colors, fonts, and decorative styling, but must preserve these functional anchors.

---

## 8. Logical Resolution and Units

Constants:

```js
VIEW_W = 1280
VIEW_H = 720
TILE = 32
DT = 1 / 60
```

Coordinate system:

- X increases to the right.
- Y increases downward.
- Origin is top-left.
- All gameplay coordinates are logical pixels.

Player hitbox:

```js
PLAYER_W = 20
PLAYER_H = 28
```

Entity sizes:

```js
DEWDROP_W = 16
DEWDROP_H = 16

CHECKPOINT_W = 32
CHECKPOINT_H = 32

EXIT_W = 48
EXIT_H = 64

MOSQUITO_W = 24
MOSQUITO_H = 20

DRAGONFLY_W = 28
DRAGONFLY_H = 16

HERON_W = 56
HERON_H = 80
```

Rectangles for solids, one-way platforms, lily pads, water, currents, and thorns use top-left coordinates:

```js
{ x, y, w, h }
```

Center-based entities use center coordinates:

- player spawn
- dewdrops
- checkpoints
- exits
- enemies
- boss

Conversion:

```js
rectFromCenter(cx, cy, w, h) => {
  x: cx - w / 2,
  y: cy - h / 2,
  w: w,
  h: h
}
```

---

## 9. `js/constants.js`

This file contains all gameplay numbers.

Required constants:

```js
{
  VIEW_W: 1280,
  VIEW_H: 720,
  TILE: 32,
  DT: 1 / 60,

  PLAYER_W: 20,
  PLAYER_H: 28,

  RUN_MAX_SPEED: 240,
  GROUND_ACCEL: 1800,
  AIR_ACCEL: 1200,
  GROUND_FRICTION: 1600,
  AIR_FRICTION: 200,
  GRAVITY: 1400,
  MAX_FALL_SPEED: 900,
  JUMP_VY: -520,
  COYOTE_TIME: 0.08,
  JUMP_BUFFER_TIME: 0.12,
  JUMP_CUT_FACTOR: 0.45,

  WATER_GRAVITY: 350,
  WATER_MAX_FALL_SPEED: 220,
  WATER_MAX_SPEED: 160,
  WATER_ACCEL: 700,
  WATER_FRICTION: 900,
  SURFACE_JUMP_VY: -460,
  SWIM_UP_ACCEL: 900,
  SWIM_UP_MAX_VY: -220,
  WATER_SURFACE_TOLERANCE: 6,

  LILY_BOUNCE_VY: -620,
  LILY_BOUNCE_JUMP_VY: -680,

  STOMP_BOUNCE_VY: -380,
  BOSS_STOMP_BOUNCE_VY: -420,
  STOMP_TOLERANCE: 4,
  BOSS_STOMP_ZONE: 12,

  MAX_HEARTS: 3,
  INVULN_TIME: 1.2,
  KNOCKBACK_X: 260,
  KNOCKBACK_Y: -220,
  DEATH_TIME: 0.6,

  CURRENT_FORCE: 120,

  CAMERA_DEADZONE_X: 200,
  CAMERA_DEADZONE_Y: 120,
  CAMERA_LOOKAHEAD: 40,
  CAMERA_SMOOTHING: 10,

  SAVE_KEY: "frog-pond-to-peak-save",

  ENEMY_SIZES: {
    mosquito: { w: 24, h: 20 },
    dragonfly: { w: 28, h: 16 },
    heron: { w: 56, h: 80 }
  },

  BOSS: {
    HP: 6,
    PHASE1: {
      idle: 1.2,
      lunge: 0.4,
      recover: 0.8,
      lungeSpeed: 320
    },
    PHASE2: {
      idle: 0.8,
      lunge: 0.4,
      recover: 0.6,
      lungeSpeed: 380
    }
  }
}
```

All gameplay code must read these constants instead of hard-coding numbers.

---

## 10. `js/utils.js`

Required utility functions:

```js
clamp(value, min, max)
lerp(a, b, t)
rectFromCenter(cx, cy, w, h)
rectsOverlap(a, b)
applyFriction(v, friction, dt)
deepCopy(value)
```

`applyFriction` rules:

```js
if v > 0:
  v -= friction * dt
  if v < 0: v = 0

if v < 0:
  v += friction * dt
  if v > 0: v = 0
```

`rectsOverlap` uses strict AABB overlap:

```js
a.x < b.x + b.w &&
a.x + a.w > b.x &&
a.y < b.y + b.h &&
a.y + a.h > b.y
```

---

## 11. Game States

The game has these states:

```js
"title"
"controls"
"playing"
"paused"
"levelComplete"
"gameComplete"
```

State rules:

### Title

- Shown at boot.
- Options depend on save.
- Enter/Space confirms selected option.
- Esc does nothing.

### Controls

- Shows control list.
- Esc returns to previous menu.
- If opened from title, returns to title.
- If opened from pause, returns to pause.

### Playing

- Normal gameplay.
- Esc opens pause.
- Esc is ignored during death animation.
- Esc is ignored during level complete or game complete.

### Paused

- Shown only from Playing.
- Options:
  - Resume
  - Restart Level
  - Controls
  - Quit to Title
- Esc resumes.
- If Controls is opened from pause, Esc returns to pause.

### Level Complete

- Shown after levels 1 through 5.
- Enter/Space continues to next level.
- Esc is ignored.
- Pause is disabled.

### Game Complete

- Shown after level 6.
- Enter/Space returns to title.
- Esc is ignored.
- Pause is disabled.

---

## 12. Save System

File:

```js
js/save.js
```

Storage:

- Use `localStorage` when available.
- Fall back to in-memory storage if `localStorage` is unavailable or throws.
- Save key: `frog-pond-to-peak-save`.

Save shape:

```js
{
  unlocked_level: 1,
  completed: false
}
```

Rules:

- `unlocked_level` is always clamped to 1 through 6.
- `completed` is boolean.
- No in-level progress is saved.
- No dewdrops are saved.
- No boss HP is saved.
- No checkpoint is saved.
- Invalid save data is treated as no save.

API:

```js
FrogGame.Save.load()
FrogGame.Save.save(data)
FrogGame.Save.clear()
FrogGame.Save.exists()
```

`load()` return shape:

```js
{
  exists: false,
  unlocked_level: 1,
  completed: false
}
```

Save timing:

- Save on level complete.
- Save on quit to title.
- Save on game complete.
- Clear on New Game.
- Clear on Play Again.

---

## 13. Input System

File:

```js
js/input.js
```

Keyboard mapping:

### Gameplay

- Left: `A` or `ArrowLeft`
- Right: `D` or `ArrowRight`
- Jump/Swim: `Space`, `W`, or `ArrowUp`
- Pause: `Escape`

### Menus

- Move: `W`, `S`, `ArrowUp`, `ArrowDown`
- Confirm: `Enter` or `Space`
- Back: `Escape`

Required behavior:

- Prevent default browser behavior for game keys.
- Track held keys.
- Track press edges.
- Ignore key repeat for edge-based actions.
- Input must work even when the canvas is not focused, as long as the page has focus.

Internal state:

```js
{
  left: false,
  right: false,
  jumpHeld: false,
  jumpPressed: false,
  menuUp: false,
  menuDown: false,
  menuLeft: false,
  menuRight: false,
  enterPressed: false,
  spacePressed: false,
  escPressed: false
}
```

Edge handling:

- `jumpPressed` is true for the frame after a new jump keydown.
- `jumpPressed` is cleared at the end of each logic update.
- If keydown and keyup happen in the same frame, the jump press should still register.

Debug input:

- `window.__game.input` can override or simulate input.
- Debug input uses the same internal state as real keyboard input.

---

## 14. Main Game Loop

File:

```js
js/game.js
```

The game object owns:

- current state
- current level
- player
- camera
- HUD state
- UI state
- save state
- message system
- audio event recording

Main loop:

```js
let lastTime = 0
let accumulator = 0
const MAX_FRAME_TIME = 0.25

function frame(timestamp) {
  if (lastTime === 0) lastTime = timestamp

  let frameTime = (timestamp - lastTime) / 1000
  lastTime = timestamp

  if (frameTime > MAX_FRAME_TIME) frameTime = MAX_FRAME_TIME
  accumulator += frameTime

  while (accumulator >= DT) {
    game.update(DT)
    accumulator -= DT
  }

  game.render()
  requestAnimationFrame(frame)
}
```

Rules:

- `game.update(dt)` is the only place gameplay logic changes.
- `game.render()` only draws.
- Rendering must not modify gameplay state.
- If `requestAnimationFrame` is unavailable, the game should still boot and allow debug stepping.
- If canvas is unavailable, rendering should be a no-op.
- The loop should not throw if DOM elements are missing.

---

## 15. Level Data Format

File:

```js
js/levels.js
```

Levels are plain data.

Rect-based entries use top-left coordinates.

Center-based entries use center coordinates.

Level schema:

```js
{
  id: Number,
  name: String,
  width: Number,
  height: Number,

  spawn: { x, y },

  solids: [ [x, y, w, h] ],
  oneWays: [ [x, y, w, h] ],
  lilyPads: [ [x, y, w, h] ],
  waters: [ [x, y, w, h] ],
  currents: [ [x, y, w, h, force] ],
  thorns: [ [x, y, w, h] ],

  enemies: [
    {
      type: "mosquito" | "dragonfly",
      x: Number,
      y: Number,
      minX: Number,
      maxX: Number,
      baseY: Number
    }
  ],

  dewdrops: [ [x, y] ],

  checkpoint: { x, y } | null,
  exit: { x, y, locked },

  movingPlatforms: [
    {
      x,
      y,
      w,
      h,
      axis: "x" | "y",
      amplitude: Number,
      period: Number
    }
  ],

  boss: {
    type: "heron",
    x,
    y,
    hp,
    minX,
    maxX
  } | null
}
```

Notes:

- `spawn.x/y` is player center.
- `dewdrops` entries are center coordinates.
- `checkpoint.x/y` is center coordinate.
- `exit.x/y` is center coordinate.
- Enemy `x/y` is center coordinate.
- Enemy `baseY` is used by mosquitoes. For dragonflies, `y` is fixed.
- `currents.force` is positive for right, negative for left.
- `exit.locked` is only true for level 6 before boss death.
- `movingPlatforms` are one-way platforms that move on a sine path.
- `boss` exists only in level 6.

---

## 16. Authored Level Data

The following data must be implemented in `js/levels.js`.

```js
const FROG_LEVELS = [
  {
    id: 1,
    name: "Pond Edge",
    width: 2000,
    height: 720,
    spawn: { x: 100, y: 626 },
    solids: [
      [0, 640, 900, 80],
      [1020, 640, 480, 80],
      [1660, 640, 340, 80]
    ],
    oneWays: [
      [1100, 552, 128, 16]
    ],
    lilyPads: [],
    waters: [],
    currents: [],
    thorns: [
      [1350, 624, 48, 16]
    ],
    enemies: [
      {
        type: "mosquito",
        x: 1450,
        y: 570,
        minX: 1380,
        maxX: 1520,
        baseY: 570
      }
    ],
    dewdrops: [
      [200, 600],
      [400, 560],
      [700, 560],
      [1160, 508],
      [1700, 560]
    ],
    checkpoint: { x: 1700, y: 624 },
    exit: { x: 1900, y: 608, locked: false },
    movingPlatforms: [],
    boss: null
  },

  {
    id: 2,
    name: "Lily Rush",
    width: 2400,
    height: 720,
    spawn: { x: 100, y: 626 },
    solids: [
      [0, 640, 400, 80],
      [900, 640, 300, 80],
      [1800, 640, 600, 80]
    ],
    oneWays: [],
    lilyPads: [
      [520, 560, 64, 16],
      [680, 520, 64, 16],
      [840, 560, 64, 16],
      [1280, 560, 64, 16],
      [1440, 500, 64, 16],
      [1600, 560, 64, 16]
    ],
    waters: [
      [400, 560, 500, 160],
      [1200, 560, 600, 160]
    ],
    currents: [],
    thorns: [
      [1000, 624, 48, 16]
    ],
    enemies: [
      {
        type: "dragonfly",
        x: 1500,
        y: 460,
        minX: 1300,
        maxX: 1700
      }
    ],
    dewdrops: [
      [200, 600],
      [600, 520],
      [760, 480],
      [1000, 560],
      [1350, 520],
      [1550, 460],
      [2100, 600]
    ],
    checkpoint: { x: 1850, y: 624 },
    exit: { x: 2300, y: 608, locked: false },
    movingPlatforms: [],
    boss: null
  },

  {
    id: 3,
    name: "Reed Hollow",
    width: 1600,
    height: 1280,
    spawn: { x: 100, y: 1202 },
    solids: [
      [0, 1216, 1600, 64]
    ],
    oneWays: [
      [300, 1128, 128, 16],
      [500, 1040, 128, 16],
      [700, 952, 128, 16],
      [900, 864, 128, 16],
      [1250, 688, 128, 16],
      [1050, 600, 128, 16],
      [850, 512, 128, 16],
      [650, 424, 128, 16],
      [450, 336, 128, 16],
      [1200, 248, 128, 16]
    ],
    lilyPads: [
      [1100, 776, 64, 16]
    ],
    waters: [],
    currents: [],
    thorns: [
      [200, 1200, 48, 16]
    ],
    enemies: [
      {
        type: "mosquito",
        x: 800,
        y: 820,
        minX: 700,
        maxX: 1000,
        baseY: 820
      }
    ],
    dewdrops: [
      [200, 1180],
      [350, 1090],
      [550, 1000],
      [750, 910],
      [950, 820],
      [1150, 730],
      [1314, 650],
      [1100, 560],
      [900, 470],
      [700, 380],
      [500, 290],
      [800, 210]
    ],
    checkpoint: { x: 1314, y: 672 },
    exit: { x: 1264, y: 216, locked: false },
    movingPlatforms: [
      {
        x: 800,
        y: 248,
        w: 128,
        h: 16,
        axis: "x",
        amplitude: 240,
        period: 4
      }
    ],
    boss: null
  },

  {
    id: 4,
    name: "Stormy Creek",
    width: 2800,
    height: 720,
    spawn: { x: 100, y: 626 },
    solids: [
      [0, 640, 300, 80],
      [700, 640, 200, 80],
      [1400, 640, 300, 80],
      [2200, 640, 600, 80]
    ],
    oneWays: [],
    lilyPads: [
      [400, 560, 64, 16],
      [550, 520, 64, 16],
      [1000, 560, 64, 16],
      [1150, 500, 64, 16],
      [1300, 560, 64, 16],
      [1800, 560, 64, 16],
      [1950, 520, 64, 16],
      [2100, 560, 64, 16]
    ],
    waters: [
      [300, 560, 400, 160],
      [900, 560, 500, 160],
      [1700, 560, 500, 160]
    ],
    currents: [
      [300, 560, 400, 160, 120],
      [900, 560, 500, 160, -120],
      [1700, 560, 500, 160, 120]
    ],
    thorns: [
      [800, 624, 48, 16],
      [1600, 624, 48, 16],
      [2300, 624, 48, 16]
    ],
    enemies: [
      {
        type: "dragonfly",
        x: 1100,
        y: 460,
        minX: 950,
        maxX: 1350
      },
      {
        type: "dragonfly",
        x: 1900,
        y: 460,
        minX: 1750,
        maxX: 2150
      }
    ],
    dewdrops: [
      [200, 600],
      [450, 520],
      [600, 480],
      [850, 600],
      [1050, 520],
      [1200, 460],
      [1450, 600],
      [1850, 520],
      [2000, 480],
      [2400, 600],
      [2600, 560]
    ],
    checkpoint: { x: 1500, y: 624 },
    exit: { x: 2700, y: 608, locked: false },
    movingPlatforms: [],
    boss: null
  },

  {
    id: 5,
    name: "Cliffside Ponds",
    width: 2000,
    height: 1280,
    spawn: { x: 100, y: 1202 },
    solids: [
      [0, 1216, 2000, 64]
    ],
    oneWays: [
      [200, 1128, 128, 16],
      [400, 1040, 128, 16],
      [600, 952, 128, 16],
      [800, 864, 128, 16],
      [1500, 512, 128, 16],
      [1300, 424, 128, 16],
      [1100, 336, 128, 16],
      [900, 248, 128, 16],
      [1600, 248, 128, 16]
    ],
    lilyPads: [
      [1000, 776, 64, 16],
      [1150, 688, 64, 16],
      [1300, 600, 64, 16]
    ],
    waters: [],
    currents: [],
    thorns: [
      [500, 1200, 48, 16],
      [1400, 1200, 48, 16]
    ],
    enemies: [
      {
        type: "mosquito",
        x: 700,
        y: 820,
        minX: 600,
        maxX: 900,
        baseY: 820
      },
      {
        type: "dragonfly",
        x: 1200,
        y: 300,
        minX: 1000,
        maxX: 1400
      }
    ],
    dewdrops: [
      [250, 1090],
      [450, 1000],
      [650, 910],
      [850, 820],
      [1032, 740],
      [1182, 650],
      [1332, 560],
      [1564, 484],
      [1364, 380],
      [1164, 290],
      [964, 210],
      [1300, 250]
    ],
    checkpoint: { x: 1564, y: 496 },
    exit: { x: 1664, y: 216, locked: false },
    movingPlatforms: [
      {
        x: 1200,
        y: 288,
        w: 128,
        h: 16,
        axis: "x",
        amplitude: 160,
        period: 4
      }
    ],
    boss: null
  },

  {
    id: 6,
    name: "Great Waterfall",
    width: 1280,
    height: 720,
    spawn: { x: 100, y: 626 },
    solids: [
      [0, 640, 1280, 80]
    ],
    oneWays: [],
    lilyPads: [],
    waters: [],
    currents: [],
    thorns: [],
    enemies: [],
    dewdrops: [
      [200, 600],
      [640, 500],
      [1080, 600]
    ],
    checkpoint: null,
    exit: { x: 1200, y: 608, locked: true },
    movingPlatforms: [],
    boss: {
      type: "heron",
      x: 640,
      y: 600,
      hp: 6,
      minX: 100,
      maxX: 1180
    }
  }
];
```

Expected dewdrop totals:

```js
[5, 7, 12, 11, 12, 3]
```

---

## 17. Level Validation

File:

```js
js/levels.js
```

Required API:

```js
FrogGame.LevelData.validate(levelData)
```

Return:

```js
[ "error string", ... ]
```

An empty array means valid.

Validation rules:

- `id` is a number from 1 through 6.
- `name` is a non-empty string.
- `width` and `height` are positive numbers.
- `spawn` exists.
- `spawn.x` is within `[0, width]`.
- `spawn.y` is within `[0, height]`.
- `solids` is an array.
- `oneWays` is an array.
- `lilyPads` is an array.
- `waters` is an array.
- `currents` is an array.
- `thorns` is an array.
- `enemies` is an array.
- `dewdrops` is an array.
- `exit` exists.
- `exit.x/y` are within level bounds.
- Enemy `type` is `"mosquito"` or `"dragonfly"`.
- Enemy `minX < maxX`.
- Enemy `x` is within `[minX, maxX]`.
- Current `force` is either `120` or `-120`.
- Moving platform `axis` is `"x"` or `"y"`.
- Moving platform `amplitude > 0`.
- Moving platform `period > 0`.
- Boss exists only when `id === 6`.
- If boss exists:
  - `type === "heron"`
  - `hp === 6`
  - `minX < maxX`
  - `x` is within `[minX, maxX]`

Validation is structural only.

It does not verify:

- platforming spacing
- solvability
- difficulty
- enemy fairness

Why:

- The gameplay designer owns level design.
- Engineering must make the authored levels function.
- A solvability checker would be large, brittle, and outside scope.

---

## 18. Test Level Factory

File:

```js
js/levels.js
```

Required API:

```js
FrogGame.LevelData.testLevel(overrides)
```

This creates a deterministic level for tests only.

Default test level:

```js
{
  id: 0,
  name: "Test",
  width: 1280,
  height: 720,
  spawn: { x: 100, y: 626 },
  solids: [
    [0, 640, 1280, 80]
  ],
  oneWays: [],
  lilyPads: [],
  waters: [],
  currents: [],
  thorns: [],
  enemies: [],
  dewdrops: [],
  checkpoint: null,
  exit: { x: 1100, y: 608, locked: false },
  movingPlatforms: [],
  boss: null
}
```

`overrides` are shallow/deep merged into the default.

Also provide:

```js
FrogGame.LevelData.generateSmokeLevel()
```

Smoke level:

```js
{
  id: 0,
  name: "Smoke",
  width: 1600,
  height: 720,
  spawn: { x: 100, y: 626 },
  solids: [
    [0, 640, 1600, 80]
  ],
  oneWays: [],
  lilyPads: [],
  waters: [],
  currents: [],
  thorns: [],
  enemies: [
    {
      type: "mosquito",
      x: 500,
      y: 570,
      minX: 450,
      maxX: 550,
      baseY: 570
    }
  ],
  dewdrops: [
    [300, 600],
    [700, 600]
  ],
  checkpoint: { x: 900, y: 624 },
  exit: { x: 1400, y: 608, locked: false },
  movingPlatforms: [],
  boss: null
}
```

The smoke level is used by the synthetic full-loop test.

---

## 19. Runtime Level Object

File:

```js
js/level.js
```

`FrogGame.Level.fromData(data)` creates a runtime level.

Runtime level should contain:

```js
{
  id,
  name,
  width,
  height,
  spawn,
  solids: [ { id, x, y, w, h } ],
  oneWays: [ { id, x, y, w, h, movingId } ],
  lilyPads: [ { id, x, y, w, h } ],
  waters: [ { id, x, y, w, h } ],
  currents: [ { id, x, y, w, h, force } ],
  thorns: [ { id, x, y, w, h } ],
  enemies: [ { id, type, x, y, w, h, minX, maxX, baseY, direction, alive } ],
  dewdrops: [ { id, x, y, w, h, collected } ],
  checkpoint: { id, x, y, w, h, activated } | null,
  exit: { id, x, y, w, h, locked, active },
  movingPlatforms: [ { id, start, current, previous, axis, amplitude, period } ],
  boss: runtimeBoss | null,
  time: 0,
  respawn: { x, y },
  events: tutorialEventFlags
}
```

IDs:

```text
solid-0
oneway-0
lily-0
water-0
current-0
thorn-0
enemy-0
dewdrop-0
checkpoint-0
exit-0
moving-0
boss-0
```

Rules:

- Level data must be deep-copied when creating runtime level.
- Runtime level must not mutate the original data.
- `level.time` is level time in seconds.
- `level.time` advances only while:
  - state is `"playing"`
  - player is not dead
- `level.time` resets to 0 on:
  - level load
  - level restart
  - player respawn
- `level.time` does not advance during:
  - pause
  - death animation
  - level complete
  - game complete
  - title
  - controls

Enemy initial direction:

- Default direction is right: `1`.
- If initial `x >= maxX`, direction is left: `-1`.
- If initial `x <= minX`, direction is right: `1`.

Boss initial state:

```js
{
  id: "boss-0",
  type: "heron",
  x,
  y,
  w: 56,
  h: 80,
  hp: 6,
  state: "idle",
  timer: 1.2,
  direction: 1,
  alive: true
}
```

---

## 20. Collision System

File:

```js
js/collision.js
```

Collision is axis-separated.

Update order:

1. Apply moving platform carry delta to player.
2. Apply horizontal input.
3. Apply water/current horizontal forces.
4. Apply vertical gravity/swimming.
5. Move player horizontally.
6. Resolve horizontal solid collisions and level bounds.
7. Move player vertically.
8. Resolve vertical solid collisions and level bounds.
9. Resolve one-way platforms and lily pads.
10. Update enemies.
11. Check player-enemy collisions.
12. Check dewdrops.
13. Check checkpoint.
14. Check exit.
15. Update timers and HUD.

Stomp checks must use the player's bottom position from before vertical movement.

### 20.1 Player Rect

Player position is stored as center:

```js
player.x
player.y
player.vx
player.vy
```

Player rect:

```js
{
  x: player.x - PLAYER_W / 2,
  y: player.y - PLAYER_H / 2,
  w: PLAYER_W,
  h: PLAYER_H
}
```

Player bottom:

```js
player.y + PLAYER_H / 2
```

Player feet:

```js
player.y + PLAYER_H / 2
```

### 20.2 Level Bounds

Level bounds act as solid walls on left, right, and top.

Rules:

- Player cannot move left of `x = 0`.
- Player cannot move right of `x = level.width`.
- Player cannot move above `y = 0`.
- Player may move below `level.height`.
- If player center `y > level.height + 100`, player dies.

Implementation:

```js
if player.x < PLAYER_W / 2:
  player.x = PLAYER_W / 2
  player.vx = 0

if player.x > level.width - PLAYER_W / 2:
  player.x = level.width - PLAYER_W / 2
  player.vx = 0

if player.y < PLAYER_H / 2:
  player.y = PLAYER_H / 2
  player.vy = 0
```

### 20.3 Solid Collision

Solids block from all sides.

Horizontal resolution:

```js
player.x += player.vx * dt

for each solid:
  if player rect overlaps solid:
    if player.vx > 0:
      player.x = solid.x - PLAYER_W / 2
      player.vx = 0
    else if player.vx < 0:
      player.x = solid.x + solid.w + PLAYER_W / 2
      player.vx = 0
```

Vertical resolution:

```js
player.y += player.vy * dt

for each solid:
  if player rect overlaps solid:
    if player.vy > 0:
      player.y = solid.y - PLAYER_H / 2
      player.vy = 0
      player.onGround = true
    else if player.vy < 0:
      player.y = solid.y + solid.h + PLAYER_H / 2
      player.vy = 0
```

### 20.4 One-Way Platforms

One-way platforms block only from below.

The player can pass through from below.

The player cannot drop through.

Landing condition:

```js
if player.vy >= 0:
  if previousBottom <= platform.y + EPS:
    if newBottom >= platform.y:
      if horizontal overlap:
        land on platform
```

`EPS` is `1`.

Landing:

```js
player.y = platform.y - PLAYER_H / 2
player.vy = 0
player.onGround = true
player.standingPlatformId = platform.id
```

### 20.5 Lily Pads

Lily pads are bouncy one-way platforms.

The player cannot stand on them.

Bounce condition:

```js
if player.vy >= 0:
  if previousBottom <= pad.y + EPS:
    if newBottom >= pad.y:
      if horizontal overlap:
        bounce
```

Bounce:

```js
if jumpHeld:
  player.vy = -680
else:
  player.vy = -620

player.onGround = false
player.standingPlatformId = null
player.jumpCutApplied = false
```

Lily pad bounce triggers:

- audio event `lily_pad_bounce`
- tutorial event `firstLilyBounce`

### 20.6 Moving Platforms

Moving platforms are one-way platforms.

Position:

```js
offset = amplitude * sin(2 * PI * level.time / period)

if axis === "x":
  current.x = start.x + offset
  current.y = start.y

if axis === "y":
  current.x = start.x
  current.y = start.y + offset
```

Each update:

1. Store `previous = current`.
2. Compute new `current` from `level.time`.
3. Compute `delta = current - previous`.
4. If player `standingPlatformId` matches this platform:
   - `player.x += delta.x`
   - `player.y += delta.y`

Moving platform ride sets tutorial event:

```js
firstMovingPlatformRide = true
```

Rules:

- Moving platforms carry the player before input is applied.
- If the player is not standing on the platform, no carry is applied.
- If the platform moves away, the player falls normally.
- If the player dies, moving platforms reset to initial phase by resetting `level.time = 0`.

---

## 21. Player System

File:

```js
js/player.js
```

Player state:

```js
{
  x,
  y,
  vx,
  vy,
  facing: 1,
  onGround: false,
  inWater: false,
  onSurface: false,
  hearts: 3,
  invulnTimer: 0,
  coyoteTimer: 0,
  jumpBufferTimer: 0,
  jumpCutApplied: false,
  dead: false,
  deathTimer: 0,
  deaths: 0,
  standingPlatformId: null,
  wasInWater: false
}
```

### 21.1 Horizontal Movement

Input:

```js
input = 0
if right: input += 1
if left: input -= 1
```

Context:

- on ground:
  - acceleration `1800`
  - max speed `240`
  - friction `1600`
- in air:
  - acceleration `1200`
  - max speed `240`
  - friction `200`
- in water:
  - acceleration `700`
  - max speed `160`
  - friction `900`

Algorithm:

```js
if input != 0:
  player.facing = input
  player.vx += input * accel * dt
  clamp player.vx to [-maxSpeed, maxSpeed]
else:
  applyFriction(player.vx, friction, dt)
```

### 21.2 Water State

Water detection:

```js
player.inWater = player center is inside any water rectangle
```

Surface detection:

```js
player.onSurface =
  !player.inWater
  and player feet are within 6 px above water top
  and player horizontally overlaps water rectangle
```

Feet:

```js
feetY = player.y + PLAYER_H / 2
```

Surface condition for a water rect:

```js
feetY >= water.y - 6
feetY <= water.y
horizontal overlap between player rect and water rect
```

Entering water:

```js
if !wasInWater and inWater and player.vy > 220:
  player.vy = 220
```

While in water:

- vertical velocity is clamped to `[-220, 220]`.
- horizontal velocity is clamped to `[-160, 160]`.
- water splash audio triggers when entering water.

### 21.3 Currents

Current detection:

```js
player center is inside current rectangle
```

Current force:

```js
player.vx += force * dt
```

Clamp:

```js
clamp player.vx to [-160, 160]
```

Current force sets tutorial event:

```js
firstCurrentForce = true
```

### 21.4 Jumping

Jump press:

```js
if jumpPressed:
  player.jumpBufferTimer = 0.12
```

Ground/coyote jump:

```js
if player.onGround or player.coyoteTimer > 0:
  if player.jumpBufferTimer > 0:
    if !player.inWater:
      player.vy = -520
      player.onGround = false
      player.coyoteTimer = 0
      player.jumpBufferTimer = 0
      player.jumpCutApplied = false
      audio.play("jump")
      tutorial.firstJump = true
```

Coyote time:

```js
if player.onGround:
  player.coyoteTimer = 0.08
else:
  player.coyoteTimer -= dt
```

Jump buffer:

```js
player.jumpBufferTimer -= dt
if player.jumpBufferTimer < 0:
  player.jumpBufferTimer = 0
```

Variable jump cut:

```js
if jumpReleased:
  if player.vy < 0:
    if !player.jumpCutApplied:
      player.vy *= 0.45
      player.jumpCutApplied = true
```

Jump cut applies only to land jumps, not water swimming.

### 21.5 Surface Jump

Surface jump:

```js
if player.onSurface and jumpPressed:
  player.vy = -460
  audio.play("water_splash")
  tutorial.firstWaterJumpOrSwim = true
```

Surface jump does not set `jumpCutApplied`.

### 21.6 Vertical Movement

If in water:

```js
if jumpHeld:
  player.vy -= 900 * dt
  if player.vy < -220:
    player.vy = -220
    tutorial.firstWaterJumpOrSwim = true
else:
  player.vy += 350 * dt
  if player.vy > 220:
    player.vy = 220
```

If not in water:

```js
player.vy += 1400 * dt
if player.vy > 900:
  player.vy = 900
```

### 21.7 Death

Death causes:

- hearts reach 0
- player center `y > level.height + 100`

Death behavior:

```js
player.dead = true
player.deathTimer = 0.6
player.deaths += 1
player.vx = 0
player.vy = 0
```

During death:

- input is ignored.
- level updates are frozen.
- only `deathTimer` decreases.
- pause is disabled.

Respawn:

```js
player.x = level.respawn.x
player.y = level.respawn.y
player.vx = 0
player.vy = 0
player.hearts = 3
player.invulnTimer = 0
player.coyoteTimer = 0
player.jumpBufferTimer = 0
player.jumpCutApplied = false
player.onGround = false
player.inWater = false
player.onSurface = false
player.standingPlatformId = null
player.dead = false
player.deathTimer = 0
```

Respawn also:

- resets enemies to initial positions
- resets moving platforms to initial phase
- keeps collected dewdrops
- keeps boss dead if boss was dead
- refills hearts

---

## 22. Damage System

Damage function:

```js
player.damage(sourceX)
```

Rules:

- If `player.invulnTimer > 0`, ignore damage.
- If `player.dead`, ignore damage.
- Decrement hearts by 1.
- Set `invulnTimer = 1.2`.
- Apply knockback away from source.
- Play audio `damage`.
- If hearts reach 0, start death.

Knockback:

```js
if sourceX <= player.x:
  player.vx = 260
else:
  player.vx = -260

player.vy = -220
```

Invulnerability:

- Player cannot take damage while invulnerable.
- Stomp checks still work while invulnerable.
- Dewdrop collection still works while invulnerable.
- Checkpoint activation still works while invulnerable.

---

## 23. Enemy System

File:

```js
js/enemies.js
```

Enemy types:

- mosquito
- dragonfly
- thorn
- heron boss

Normal enemies are not solid.

Thorns are not solid.

Boss is not solid except for stomp/damage logic.

### 23.1 Mosquito

Hitbox:

```js
24 x 20
```

Movement:

```js
speed = 80
verticalAmplitude = 24
verticalPeriod = 1.6
```

Update:

```js
if enemy.x < enemy.minX:
  enemy.direction = -1
if enemy.x > enemy.maxX:
  enemy.direction = 1

enemy.x += enemy.direction * 80 * dt
enemy.y = enemy.baseY + 24 * sin(2 * PI * level.time / 1.6)
```

Bounds:

- `minX` and `maxX` are center X bounds.
- Clamp `enemy.x` to `[minX, maxX]`.

Behavior:

- stompable
- side/bottom contact damages player

### 23.2 Dragonfly

Hitbox:

```js
28 x 16
```

Movement:

```js
speed = 180
fixed y
```

Update:

```js
if enemy.x < enemy.minX:
  enemy.direction = -1
if enemy.x > enemy.maxX:
  enemy.direction = 1

enemy.x += enemy.direction * 180 * dt
```

Behavior:

- stompable
- side/bottom contact damages player

### 23.3 Thorn

Thorns are static hazards.

- Not stompable.
- Touching damages player.
- No movement.
- No AI.

### 23.4 Stomp Detection

Stomp check uses:

- player `vy > 0`
- previous player bottom from before vertical movement
- current enemy top
- horizontal overlap

Normal enemy:

```js
if player.vy > 0:
  if previousPlayerBottom <= enemy.top + 4:
    if horizontal overlap:
      stomp enemy
```

Stomp result:

```js
enemy.alive = false
player.vy = -380
player.onGround = false
player.jumpCutApplied = false
audio.play("stomp")
tutorial.firstStomp = true
```

### 23.5 Player-Enemy Collision Order

Each frame:

1. Update enemies.
2. Find all living enemies overlapping player.
3. Process stomps first.
4. If any stomp applies:
   - apply stomp bounce
   - do not apply damage
5. If no stomp applies:
   - apply exactly one damage instance from the first damaging enemy or thorn.

Multiple enemies:

- If player overlaps multiple enemies and at least one stomp applies, no damage is applied.
- If no stomp applies, only one damage instance is applied.

Thorn + enemy:

- Stomp checks happen first.
- If no stomp applies, only one damage instance is applied.

---

## 24. Boss System: Heron

Boss exists only in level 6.

Boss hitbox:

```js
56 x 80
```

Boss states:

```js
"idle"
"lunge"
"recover"
"dead"
```

Boss phase:

- Phase 1: HP 6, 5, or 4.
- Phase 2: HP 3, 2, or 1.

Phase timings:

```js
Phase 1:
  idle: 1.2
  lunge: 0.4
  recover: 0.8
  lungeSpeed: 320

Phase 2:
  idle: 0.8
  lunge: 0.4
  recover: 0.6
  lungeSpeed: 380
```

Boss update:

```js
if boss.state === "idle":
  boss.direction = sign(player.x - boss.x)
  boss.timer -= dt
  if boss.timer <= 0:
    boss.state = "lunge"
    boss.timer = 0.4

if boss.state === "lunge":
  boss.x += boss.direction * lungeSpeed * dt
  boss.timer -= dt
  if boss.timer <= 0:
    boss.state = "recover"
    boss.timer = recoverTime

if boss.state === "recover":
  boss.timer -= dt
  if boss.timer <= 0:
    boss.state = "idle"
    boss.timer = idleTime

clamp boss.x to [boss.minX, boss.maxX]
boss.y = groundTop - boss.h / 2
```

For level 6:

- ground top is `640`
- boss center Y is `600`

Boss stomp:

Stomp zone:

```js
top 12 px of boss hitbox
```

Condition:

```js
if player.vy > 0:
  if previousPlayerBottom <= boss.top + 12:
    if horizontal overlap:
      stomp boss
```

Stomp result:

```js
boss.hp -= 1
player.vy = -420
player.onGround = false
player.jumpCutApplied = false
tutorial.firstBossStomp = true

if boss.hp > 0:
  audio.play("boss_hit")
else:
  boss.state = "dead"
  boss.alive = false
  audio.play("boss_death")
  level.exit.active = true
```

Boss side/bottom contact:

- If player overlaps boss and no stomp applies, player takes damage.
- If boss is dead, it does not damage the player.

Boss death persistence:

- If boss is dead and player dies, boss remains dead.
- If boss is dead and player restarts level, boss resets to alive.
- If boss is dead, exit remains unlocked until level restart.

---

## 25. Dewdrops

Dewdrop hitbox:

```js
16 x 16
```

Dewdrop data uses center coordinates.

Runtime:

```js
{
  id,
  x,
  y,
  w: 16,
  h: 16,
  collected: false
}
```

Collection:

```js
if player rect overlaps dewdrop rect:
  if !dewdrop.collected:
    dewdrop.collected = true
```

Rules:

- Dewdrops are optional.
- Collected dewdrops persist after respawn.
- Collected dewdrops reset on level restart.
- Dewdrop collection works while invulnerable.
- Dewdrop collection does not affect progression.

HUD:

- Shows current level collected count.
- Shows current level total count.
- Format: `x / y`.

---

## 26. Checkpoints

Checkpoint hitbox:

```js
32 x 32
```

Checkpoint data uses center coordinates.

Runtime:

```js
{
  id,
  x,
  y,
  w: 32,
  h: 32,
  activated: false
}
```

Activation:

```js
if player rect overlaps checkpoint rect:
  if !checkpoint.activated:
    checkpoint.activated = true
    level.respawn.x = checkpoint.x
    level.respawn.y = checkpoint.y
    player.hearts = 3
    show message "Checkpoint"
    audio.play("checkpoint")
  else:
    if player.hearts < 3:
      player.hearts = 3
```

Rules:

- Checkpoint sets respawn point.
- Checkpoint refills hearts.
- Checkpoint works while invulnerable.
- Checkpoint does not reset enemies.
- Checkpoint does not reset moving platforms.
- Checkpoint does not reset dewdrops.

---

## 27. Exits

Exit hitbox:

```js
48 x 64
```

Exit data uses center coordinates.

Runtime:

```js
{
  id,
  x,
  y,
  w: 48,
  h: 64,
  locked: boolean,
  active: boolean
}
```

Active rule:

```js
exit.active = exit.locked ? bossDead : true
```

Completion:

```js
if player rect overlaps exit rect:
  if exit.active:
    complete level
```

Level 6:

- Exit is locked until boss is dead.
- If boss is alive, touching exit does nothing.
- If boss is dead, touching exit completes level 6.

---

## 28. Level Complete and Game Complete

### 28.1 Levels 1 through 5

When active exit is touched:

- state becomes `"levelComplete"`.
- save `unlocked_level` becomes current level + 1.
- show level complete screen.
- play audio `level_complete`.

Level complete screen shows:

```text
LEVEL COMPLETE

[Level Name]

Dewdrops: x / y

Press Enter or Space to continue
```

If `x == y`, also show:

```text
Perfect!
```

Continuing:

- loads next level.
- state becomes `"playing"`.

### 28.2 Level 6

When active exit is touched:

- state becomes `"gameComplete"`.
- save `completed = true`.
- save `unlocked_level = 6`.
- show game complete screen.
- play audio `game_complete`.

Game complete screen shows:

```text
THE FROG REACHED THE GREAT WATERFALL.

The pond is now a small dot in a big sky.

Press Enter or Space to return to title
```

Returning to title:

- state becomes `"title"`.
- title shows completed-save options.

---

## 29. Title Screen

Title content:

```text
FROG: POND TO PEAK

A small jump to the waterfall
```

Options depend on save.

No save:

```text
New Game
Controls
```

Save exists and not completed:

```text
Continue
New Game
Controls
```

Save completed:

```text
Play Again
New Game
Controls
```

Actions:

### Continue

- Starts `save.unlocked_level`.
- Only shown when save exists and `completed === false`.

### New Game

- If no save:
  - resets save.
  - starts level 1.
- If save exists:
  - shows confirmation:

```text
Start over?

Yes
No
```

- Yes:
  - clears save.
  - starts level 1.
- No:
  - returns to title options.

### Play Again

- Only shown when `completed === true`.
- Clears save.
- Starts level 1.
- No confirmation.

### Controls

- Shows controls screen.
- Esc returns to title.

---

## 30. Controls Screen

Controls screen content:

```text
CONTROLS

Move: A / D or Left / Right
Jump / Swim: Space / W / Up
Pause: Esc

Menus:
Move: W / S or Up / Down
Confirm: Enter or Space
Back: Esc

Press Esc to go back
```

Behavior:

- No gameplay updates.
- Esc returns to previous menu.
- If opened from title, returns to title.
- If opened from pause, returns to pause.

---

## 31. Pause Menu

Pause menu content:

```text
PAUSED

Resume
Restart Level
Controls
Quit to Title
```

Behavior:

### Resume

- Returns to playing.
- Level state is unchanged.

### Restart Level

- Resets current level completely.
- Dewdrops reset.
- Enemies reset.
- Moving platforms reset.
- Boss resets if present.
- Player respawns at level spawn.
- Hearts refill to 3.
- State becomes playing.

### Controls

- Opens controls screen.
- Esc returns to pause.

### Quit to Title

- Saves current unlocked level.
- Does not save in-level progress.
- Does not save dewdrops.
- Does not save boss HP.
- Returns to title.

Pause is disabled during:

- death animation
- level complete
- game complete
- title
- controls

---

## 32. HUD

File:

```js
js/hud.js
```

HUD is DOM-based.

HUD updates immediately when state changes.

### 32.1 Hearts

Location:

- top-left
- 16 px from left
- 16 px from top

Content:

- 3 heart icons.
- Each icon is 32 x 32.
- 8 px spacing.

Display:

- Full heart for current health.
- Empty heart for lost health.

Update:

- On damage.
- On checkpoint.
- On respawn.

### 32.2 Dewdrops

Location:

- top-right
- 16 px from right
- 16 px from top

Content:

- Dewdrop icon.
- Count text.

Format:

```text
x / y
```

Where:

- `x` = collected in current level.
- `y` = total in current level.

Update:

- On collection.
- On level load.
- On level restart.

Persistence:

- Persists through respawn.
- Resets on level restart.

### 32.3 Message

Location:

- top-center
- 48 px below top edge
- max width 600 px

Message priority:

1. Level Complete
2. Checkpoint
3. Tutorial prompt
4. Level name

Because Level Complete is a screen, HUD message priority effectively is:

1. Checkpoint
2. Tutorial prompt
3. Level name

Message timers:

- Level name: 2.5 seconds.
- Checkpoint: 1.5 seconds.
- Tutorial prompt: 5 seconds after shown, or until hidden by condition.

Messages do not affect gameplay.

---

## 33. Tutorial Prompts

Tutorial prompts appear in the message section.

They are per-level.

They do not affect gameplay.

They are hidden when their condition is met.

They expire 5 seconds after first shown if not hidden.

Required event flags per level:

```js
{
  firstHorizontalInput: false,
  firstJump: false,
  firstStomp: false,
  firstWaterJumpOrSwim: false,
  firstLilyBounce: false,
  firstOneWayLanding: false,
  firstMovingPlatformRide: false,
  firstCurrentForce: false,
  firstBossStomp: false
}
```

Prompt table:

### Level 1

```text
id: "move"
text: "Move with A/D or Left/Right"
show: at spawn
hide: firstHorizontalInput
```

```text
id: "jump"
text: "Jump with Space"
show: player.x >= 300
hide: firstJump
```

```text
id: "stomp"
text: "Land on enemies to stomp them"
show: player.x >= 1350
hide: firstStomp or player.x >= 1500
```

```text
id: "waterfall"
text: "Reach the waterfall"
show: player.x >= 1750
hide: after 5 seconds
```

### Level 2

```text
id: "swim"
text: "Hold Jump to swim"
show: player.x >= 350
hide: firstWaterJumpOrSwim
```

```text
id: "lily"
text: "Lily pads bounce"
show: player.x >= 500
hide: firstLilyBounce
```

### Level 3

```text
id: "oneway"
text: "Leaves are one-way platforms"
show: player.x >= 250
hide: firstOneWayLanding
```

```text
id: "moving"
text: "Moving leaves carry you"
show: player.x >= 750 and player.y <= 400
hide: firstMovingPlatformRide
```

### Level 4

```text
id: "current"
text: "Currents push you"
show: player.x >= 280
hide: firstCurrentForce
```

### Level 5

```text
id: "chain"
text: "Chain lily pads to climb"
show: player.x >= 950
hide: firstLilyBounce
```

### Level 6

```text
id: "boss"
text: "Stomp the heron’s head"
show: at level start
hide: firstBossStomp
```

---

## 34. Camera

File:

```js
js/camera.js
```

Camera follows player.

Camera is clamped to level bounds.

Camera uses:

- deadzone X: 200 px
- deadzone Y: 120 px
- lookahead: 40 px in facing direction
- smoothing factor: 10

Algorithm:

```js
halfW = 640
halfH = 360

playerLookX = player.x + (player.facing > 0 ? 40 : -40)
playerLookY = player.y

cameraCenterX = camera.x + halfW
cameraCenterY = camera.y + halfH

desiredX = camera.x
desiredY = camera.y

if playerLookX > cameraCenterX + 200:
  desiredX = playerLookX - (halfW - 200)
else if playerLookX < cameraCenterX - 200:
  desiredX = playerLookX + (halfW - 200)

if playerLookY > cameraCenterY + 120:
  desiredY = playerLookY - (halfH - 120)
else if playerLookY < cameraCenterY - 120:
  desiredY = playerLookY + (halfH - 120)

camera.x += (desiredX - camera.x) * min(1, dt * 10)
camera.y += (desiredY - camera.y) * min(1, dt * 10)

clamp camera.x to [0, level.width - 1280]
clamp camera.y to [0, level.height - 720]
```

If level is smaller than viewport:

- clamp camera to `0` on that axis.

Camera is visual only.

Logic must not depend on camera.

---

## 35. Rendering

File:

```js
js/game.js
```

Rendering uses canvas 2D.

Logical canvas size:

```js
1280 x 720
```

Render order:

1. Clear canvas.
2. Apply camera transform.
3. Draw background.
4. Draw water.
5. Draw currents.
6. Draw solids.
7. Draw one-way platforms.
8. Draw lily pads.
9. Draw moving platforms.
10. Draw thorns.
11. Draw dewdrops.
12. Draw checkpoint.
13. Draw exit.
14. Draw enemies.
15. Draw boss.
16. Draw player.

Rendering rules:

- If visual assets exist, draw assets.
- If visual assets are missing, draw simple placeholder rectangles.
- Player facing is visible.
- Player invulnerability is visible by blinking.
- Player death state is visible.
- Boss head/stomp zone should be visually distinguishable.
- Locked exit should look different from active exit.
- Currents should be visible.
- Water should be visible.
- Lily pads should look different from normal one-way platforms.

No gameplay logic may depend on rendered pixels.

---

## 36. Audio Implementation

File:

```js
js/audio.js
```

Required audio events:

```text
jump
water_splash
lily_pad_bounce
stomp
damage
checkpoint
level_complete
boss_hit
boss_death
game_complete
```

Expected asset files:

```text
assets/audio/jump.ogg
assets/audio/water_splash.ogg
assets/audio/lily_pad_bounce.ogg
assets/audio/stomp.ogg
assets/audio/damage.ogg
assets/audio/checkpoint.ogg
assets/audio/level_complete.ogg
assets/audio/boss_hit.ogg
assets/audio/boss_death.ogg
assets/audio/game_complete.ogg
```

If `.ogg` is missing, try `.mp3`.

Audio manager API:

```js
FrogGame.Audio.play(event)
FrogGame.Audio.setEnabled(enabled)
FrogGame.Audio.getLastEvent()
FrogGame.Audio.unlock()
```

Rules:

- Audio must not block boot.
- Missing audio files must fail silently.
- Audio should unlock on first user gesture.
- In tests, audio may be disabled.
- `play(event)` should record `lastEvent` even if audio is disabled or missing.
- No music is required.
- No mute UI is required.
- No volume UI is required.

Event triggers:

| Event | Trigger |
|---|---|
| `jump` | Ground jump |
| `water_splash` | Entering water or surface jump |
| `lily_pad_bounce` | Lily pad bounce |
| `stomp` | Normal enemy stomp |
| `damage` | Player takes damage |
| `checkpoint` | Checkpoint first activation |
| `level_complete` | Levels 1 through 5 complete |
| `boss_hit` | Boss HP decreases but remains above 0 |
| `boss_death` | Boss HP reaches 0 |
| `game_complete` | Level 6 complete |

---

## 37. Assets

File:

```js
js/assets.js
```

Assets are optional at runtime.

Required behavior:

- Images load asynchronously.
- Audio loads asynchronously.
- Missing assets do not throw.
- Missing images use placeholder rectangles.
- Missing audio plays silently.

The visual designer may provide:

- player sprite
- enemy sprites
- boss sprite
- background assets
- HUD icon assets
- audio files

Engineering does not require a specific image format beyond what the browser supports.

Recommended image formats:

- PNG
- WebP

Recommended audio formats:

- OGG
- MP3 fallback

---

## 38. Debug API

File:

```js
js/debug.js
```

`window.__game` must be created after the game boots.

Required shape:

```js
window.__game = {
  version: "1.0.0",

  start: function (opts) {},
  reset: function (opts) {},
  step: function (frames, opts) {},
  until: function (predicate, maxFrames) {},
  getState: function () {},

  input: {
    setLeft: function (down) {},
    setRight: function (down) {},
    setJump: function (down) {},
    pressJump: function (holdFrames) {},
    setMenu: function (key, down) {},
    pressMenu: function (key) {}
  },

  actions: {
    startNewGame: function () {},
    continueGame: function () {},
    playAgain: function () {},
    selectTitleOption: function (index) {},
    moveMenu: function (dir) {},
    pressEnter: function () {},
    pressEsc: function () {},

    pause: function () {},
    resume: function () {},
    restartLevel: function () {},
    quitToTitle: function () {},

    loadLevel: function (index) {},
    loadTestLevel: function (spec) {},
    validateLevel: function (data) {},
    setSave: function (save) {},

    collectDewdrop: function (index) {},
    killEnemy: function (idOrIndex) {},
    setEnemyPosition: function (idOrIndex, x, y) {},
    setBossHp: function (hp) {},
    setBossState: function (state) {},
    unlockExit: function (active) {},

    damagePlayer: function (sourceX) {},
    setHearts: function (hearts) {},
    setInvulnerable: function (seconds) {},
    teleport: function (x, y) {},
    setPlayerVelocity: function (vx, vy) {},
    setLevelTime: function (seconds) {},
    setAudioEnabled: function (enabled) {}
  }
}
```

### 38.1 `start(opts)`

Boots the game.

Optional:

```js
{
  level: 1
}
```

If `level` is provided, the game may start directly in that level for debugging. Normal boot starts at title.

### 38.2 `reset(opts)`

Resets game to title.

Optional:

```js
{
  save: false
}
```

If `save` is `false`, clear save data.

If `save` is `true`, preserve save data.

### 38.3 `step(frames, opts)`

Advances gameplay by a number of fixed frames.

Default:

```js
frames = 1
```

Optional:

```js
{
  render: false
}
```

Rules:

- Each frame is `dt = 1 / 60`.
- Does not use real time.
- Returns final state.
- If state is not playing, step may still update allowed non-gameplay timers, but tests should use actions to change state.

### 38.4 `until(predicate, maxFrames)`

Returns a Promise.

Steps the game until `predicate(state)` returns true.

Default:

```js
maxFrames = 120
```

If timeout occurs, reject with an error.

This is for tests only.

### 38.5 `getState()`

Returns a serializable state object.

Required shape:

```js
{
  gameState: "title" | "controls" | "playing" | "paused" | "levelComplete" | "gameComplete",

  version: "1.0.0",

  save: {
    exists: boolean,
    unlocked_level: number,
    completed: boolean
  },

  title: {
    options: [string],
    selectedIndex: number,
    confirm: null | {
      prompt: string,
      options: [string],
      selectedIndex: number
    }
  },

  level: {
    index: number,
    id: number,
    name: string,
    width: number,
    height: number,
    time: number
  },

  player: {
    x: number,
    y: number,
    vx: number,
    vy: number,
    facing: number,
    onGround: boolean,
    inWater: boolean,
    onSurface: boolean,
    hearts: number,
    invulnTimer: number,
    dead: boolean,
    deathTimer: number,
    deaths: number,
    respawnX: number,
    respawnY: number
  },

  input: {
    left: boolean,
    right: boolean,
    jumpHeld: boolean
  },

  dewdrops: {
    collected: number,
    total: number,
    collectedIds: [number]
  },

  enemies: [
    {
      id: string,
      type: string,
      alive: boolean,
      x: number,
      y: number,
      w: number,
      h: number
    }
  ],

  boss: {
    exists: boolean,
    alive: boolean,
    hp: number,
    state: string,
    x: number,
    y: number
  },

  exit: {
    x: number,
    y: number,
    active: boolean,
    locked: boolean
  },

  checkpoint: {
    x: number,
    y: number,
    activated: boolean
  } | null,

  message: {
    text: string,
    remaining: number
  },

  tutorial: {
    activeId: string | null,
    flags: {
      firstHorizontalInput: boolean,
      firstJump: boolean,
      firstStomp: boolean,
      firstWaterJumpOrSwim: boolean,
      firstLilyBounce: boolean,
      firstOneWayLanding: boolean,
      firstMovingPlatformRide: boolean,
      firstCurrentForce: boolean,
      firstBossStomp: boolean
    }
  },

  levelComplete: {
    levelName: string,
    dewdropsCollected: number,
    dewdropsTotal: number,
    perfect: boolean,
    nextLevel: number
  } | null,

  gameComplete: {
    completed: boolean
  } | null,

  camera: {
    x: number,
    y: number
  },

  audio: {
    enabled: boolean,
    lastEvent: string | null
  }
}
```

Rules:

- State must be JSON-serializable.
- State must not contain functions.
- State must not contain DOM nodes.
- State must not contain canvas contexts.
- State must not contain internal objects with circular references.

---

## 39. Debug Action Details

### 39.1 `actions.startNewGame()`

- Clears save.
- Starts level 1.
- State becomes playing.

### 39.2 `actions.continueGame()`

- Starts `save.unlocked_level`.
- If no save, starts level 1.
- State becomes playing.

### 39.3 `actions.playAgain()`

- Clears save.
- Starts level 1.
- State becomes playing.

### 39.4 `actions.selectTitleOption(index)`

Selects title option by index.

If option is New Game and save exists, enters confirmation state.

If confirmation is active, selects confirmation option.

### 39.5 `actions.moveMenu(dir)`

Moves menu selection.

`dir`:

```js
"up"
"down"
```

Selection wraps around.

### 39.6 `actions.pressEnter()`

Confirms current menu/screen action.

### 39.7 `actions.pressEsc()`

Triggers Esc behavior for current state.

### 39.8 `actions.pause()`

Pauses only if state is playing and player is not dead.

### 39.9 `actions.resume()`

Resumes only if state is paused.

### 39.10 `actions.restartLevel()`

Restarts current level.

### 39.11 `actions.quitToTitle()`

Quits to title and saves current unlocked level.

### 39.12 `actions.loadLevel(index)`

Loads authored level by 1-based index.

- Resets level.
- Sets state to playing.
- Does not require save unlock.
- Does not modify save unless explicitly part of normal game flow.

### 39.13 `actions.loadTestLevel(spec)`

Loads a test level.

- Uses `FrogGame.LevelData.testLevel(spec)`.
- Sets state to playing.
- Does not modify save.

### 39.14 `actions.validateLevel(data)`

Returns validation errors.

### 39.15 `actions.setSave(save)`

Sets save state for tests.

Expected:

```js
{
  exists: boolean,
  unlocked_level: number,
  completed: boolean
}
```

### 39.16 `actions.collectDewdrop(index)`

Collects dewdrop by index.

If index is omitted, collect first uncollected dewdrop.

### 39.17 `actions.killEnemy(idOrIndex)`

Kills enemy by ID or index.

### 39.18 `actions.setEnemyPosition(idOrIndex, x, y)`

Sets enemy center position.

### 39.19 `actions.setBossHp(hp)`

Sets boss HP.

If `hp <= 0`:

- boss state becomes dead.
- boss alive becomes false.
- exit becomes active.

### 39.20 `actions.setBossState(state)`

Sets boss state.

Valid states:

```js
"idle"
"lunge"
"recover"
"dead"
```

### 39.21 `actions.unlockExit(active)`

Overrides exit active state for tests.

### 39.22 `actions.damagePlayer(sourceX)`

Applies damage to player.

If `sourceX` omitted, use player.x.

### 39.23 `actions.setHearts(hearts)`

Sets player hearts.

Clamp to 0 through 3.

If hearts reach 0, start death.

### 39.24 `actions.setInvulnerable(seconds)`

Sets player invulnerability timer.

### 39.25 `actions.teleport(x, y)`

Teleports player center.

- Resets velocity.
- Resets onGround.
- Does not reset hearts.
- Does not reset dewdrops.
- Does not reset enemies.

### 39.26 `actions.setPlayerVelocity(vx, vy)`

Sets player velocity.

### 39.27 `actions.setLevelTime(seconds)`

Sets level time.

Used for moving platform and sine enemy tests.

### 39.28 `actions.setAudioEnabled(enabled)`

Enables/disables audio.

`lastEvent` should still be recorded when disabled.

---

## 40. Debug Input Details

### 40.1 `input.setLeft(down)`

Sets left input.

### 40.2 `input.setRight(down)`

Sets right input.

### 40.3 `input.setJump(down)`

Sets jump held state.

If transitioning from false to true, set jump pressed edge.

### 40.4 `input.pressJump(holdFrames)`

Simulates a jump press held for a number of frames.

Default:

```js
holdFrames = 12
```

Behavior:

- Sets jump held true.
- Sets jump pressed edge.
- Schedules jump release after `holdFrames` updates.

This is important for full jumps in tests.

### 40.5 `input.setMenu(key, down)`

Sets menu key.

Valid keys:

```js
"up"
"down"
"left"
"right"
"enter"
"space"
"esc"
```

### 40.6 `input.pressMenu(key)`

Presses and releases menu key within one update.

---

## 41. Test Harness

File:

```js
test/test-harness.js
```

The harness is minimal and dependency-free.

Required API:

```js
window.__test = {
  test: function (name, fn) {},
  assert: function (condition, message) {},
  assertClose: function (actual, expected, epsilon, message) {},
  run: function () {},
  results: {
    passed: 0,
    failed: 0,
    assertions: 0,
    failures: []
  }
}
```

`test(name, fn)`:

- Registers a test.
- `fn` may be synchronous or async.
- Tests run sequentially.

`assert(condition, message)`:

- Increments assertion count.
- Throws if condition is false.

`assertClose(actual, expected, epsilon, message)`:

- Passes if `Math.abs(actual - expected) <= epsilon`.
- Default epsilon is `0.001`.

`run()`:

- Runs all registered tests.
- Catches errors.
- Returns results object.
- Sets `window.__testResults`.
- Sets `window.__testsDone` promise.

Result shape:

```js
{
  passed: number,
  failed: number,
  assertions: number,
  failures: [
    {
      name: string,
      message: string
    }
  ]
}
```

`test.html` should expose:

```js
window.__testsDone
window.__testResults
```

Headless validation can do:

```js
await window.__testsDone
window.__testResults.failed === 0
```

---

## 42. Test File

File:

```js
test/tests.js
```

Tests should:

- Use only `window.__game`.
- Use `window.__test`.
- Not use real timers.
- Not require audio files.
- Not require image files.
- Not require network.
- Not require user interaction.
- Reset game state at the start of each test when needed.
- Use tolerances for numeric assertions.

Recommended helper in `tests.js`:

```js
function freshGame() {
  const g = window.__game;
  g.actions.setAudioEnabled(false);
  g.reset({ save: false });
  return g;
}

function groundLevel(g) {
  g.actions.loadTestLevel({});
}

function smokeLevel(g) {
  g.actions.loadTestLevel(window.FrogGame.LevelData.generateSmokeLevel());
}
```

Recommended numeric tolerances:

- Position: `1` px.
- Velocity: `5` px/s.
- Timer: `0.05` seconds.
- Angle/phase: not used.

---

## 43. Required Test Suite

The following tests are required.

They are grouped by system.

A passing `test.html` must run all of these.

### 43.1 Boot and Debug

#### Test: `boot.debug-api-exists`

Setup:

- Load `test.html`.

Assertions:

- `window.__game` exists.
- `window.__game.getState` is a function.
- `window.__game.input` exists.
- `window.__game.actions` exists.

#### Test: `boot.starts-at-title`

Setup:

- `freshGame()`.

Assertions:

- `state.gameState === "title"`.
- `state.save.exists === false`.
- `state.title.options` includes `"New Game"`.
- `state.title.options` includes `"Controls"`.

---

### 43.2 Save and Title Flow

#### Test: `save.no-save-title-options`

Setup:

- `freshGame()`.

Assertions:

- Title options are exactly:

```js
["New Game", "Controls"]
```

#### Test: `save.new-game-starts-level-1`

Setup:

- `freshGame()`.
- Select New Game.

Assertions:

- `state.gameState === "playing"`.
- `state.level.index === 1`.
- `state.level.name === "Pond Edge"`.
- `state.save.unlocked_level === 1`.
- `state.save.completed === false`.

#### Test: `save.new-game-confirmation-when-save-exists`

Setup:

- `freshGame()`.
- `actions.setSave({ exists: true, unlocked_level: 3, completed: false })`.
- Return to title.
- Select New Game.

Assertions:

- `state.title.confirm` is not null.
- Confirm options are:

```js
["Yes", "No"]
```

#### Test: `save.new-game-confirmation-yes`

Setup:

- Same as above.
- Select Yes.

Assertions:

- `state.gameState === "playing"`.
- `state.level.index === 1`.
- `state.save.exists === false`.
- `state.save.completed === false`.

#### Test: `save.new-game-confirmation-no`

Setup:

- Same as confirmation test.
- Select No.

Assertions:

- `state.gameState === "title"`.
- `state.title.confirm` is null.
- Save remains unchanged.

#### Test: `save.completed-title-options`

Setup:

- `freshGame()`.
- `actions.setSave({ exists: true, unlocked_level: 6, completed: true })`.
- Return to title.

Assertions:

- Title options are exactly:

```js
["Play Again", "New Game", "Controls"]
```

#### Test: `save.play-again-resets-and-starts-level-1`

Setup:

- `freshGame()`.
- `actions.setSave({ exists: true, unlocked_level: 6, completed: true })`.
- Return to title.
- Select Play Again.

Assertions:

- `state.gameState === "playing"`.
- `state.level.index === 1`.
- `state.save.exists === false`.
- `state.save.completed === false`.

#### Test: `save.continue-starts-unlocked-level`

Setup:

- `freshGame()`.
- `actions.setSave({ exists: true, unlocked_level: 4, completed: false })`.
- Return to title.
- Select Continue.

Assertions:

- `state.gameState === "playing"`.
- `state.level.index === 4`.
- `state.level.name === "Stormy Creek"`.

#### Test: `save.quit-to-title-saves-unlocked-level`

Setup:

- `freshGame()`.
- `actions.loadLevel(3)`.
- `actions.pause()`.
- `actions.quitToTitle()`.

Assertions:

- `state.gameState === "title"`.
- `state.save.exists === true`.
- `state.save.unlocked_level === 3`.
- `state.save.completed === false`.

---

### 43.3 Level Data

#### Test: `levels.all-six-load`

Setup:

- For each level index 1 through 6:
  - `actions.loadLevel(index)`.

Assertions for each level:

- `state.gameState === "playing"`.
- `state.level.index === index`.
- `state.level.name` is non-empty.
- `state.level.width > 0`.
- `state.level.height > 0`.
- Player position matches spawn.
- Exit exists.
- Dewdrop total matches expected total.

#### Test: `levels.dewdrop-totals`

Setup:

- Load each level.

Assertions:

- Dewdrop totals are:

```js
[5, 7, 12, 11, 12, 3]
```

#### Test: `levels.level-6-has-locked-exit`

Setup:

- `actions.loadLevel(6)`.

Assertions:

- `state.boss.exists === true`.
- `state.boss.hp === 6`.
- `state.boss.alive === true`.
- `state.exit.locked === true`.
- `state.exit.active === false`.

#### Test: `levels.level-6-exit-unlocks-after-boss`

Setup:

- `actions.loadLevel(6)`.
- `actions.setBossHp(0)`.

Assertions:

- `state.boss.alive === false`.
- `state.exit.active === true`.

#### Test: `levels.validator-rejects-invalid-data`

Setup:

- Create invalid level data:
  - missing exit
  - spawn outside bounds
  - invalid enemy type
  - boss on non-level-6

Assertions:

- `actions.validateLevel(data)` returns non-empty errors for each invalid case.

---

### 43.4 Player Movement

Use a default test level with ground.

#### Test: `physics.run-right`

Setup:

- `groundLevel(g)`.
- `input.setRight(true)`.
- Step 60 frames.

Assertions:

- `player.vx` is close to `240`.
- `player.x > initialX`.

#### Test: `physics.run-left`

Setup:

- `groundLevel(g)`.
- Teleport player to middle.
- `input.setLeft(true)`.
- Step 60 frames.

Assertions:

- `player.vx` is close to `-240`.
- `player.x < initialX`.

#### Test: `physics.friction-stops-player`

Setup:

- `groundLevel(g)`.
- Run right for 60 frames.
- Release right.
- Step 60 frames.

Assertions:

- `player.vx === 0`.

#### Test: `physics.full-jump-height`

Setup:

- `groundLevel(g)`.
- Press jump held for at least 60 frames.
- Step until `player.vy >= 0`.

Assertions:

- Max jump height is at least `90` px.
- Max jump height is no more than `100` px.

#### Test: `physics.variable-jump-cut`

Setup:

- `groundLevel(g)`.
- Press jump held for 1 frame.
- Step until `player.vy >= 0`.

Assertions:

- Max jump height is less than `50` px.

#### Test: `physics.coyote-time`

Setup:

- Create test level with ground ending at x = 400.
- Teleport player to x = 380, on ground.
- Move right until player walks off edge.
- Step 4 frames.
- Press jump.

Assertions:

- Player jumps.

Then:

- Reset.
- Walk off edge.
- Step 8 frames.
- Press jump.

Assertions:

- Player does not jump.

#### Test: `physics.jump-buffer`

Setup:

- Create test level with a gap.
- Teleport player above gap.
- Press jump 8 frames before landing.
- Step until player lands.

Assertions:

- Player jumps immediately after landing.
- `player.vy < 0` shortly after landing.

#### Test: `physics.max-fall-speed`

Setup:

- `groundLevel(g)`.
- Teleport player high above ground.
- Step until `player.vy > 800`.

Assertions:

- `player.vy <= 900`.

---

### 43.5 Water

#### Test: `water.entering-caps-vy`

Setup:

- Test level with water.
- Teleport player above water.
- Set `player.vy = 900`.
- Step until `player.inWater === true`.

Assertions:

- `player.vy <= 220`.

#### Test: `water.swim-upward`

Setup:

- Test level with water.
- Teleport player into water.
- `input.setJump(true)`.
- Step 60 frames.

Assertions:

- `player.vy <= -200`.
- `player.inWater === true`.

#### Test: `water.surface-jump`

Setup:

- Test level with water.
- Teleport player on water surface.
- Press jump.

Assertions:

- `player.vy` is close to `-460`.
- `player.onSurface` was true before jump.

#### Test: `water.current-pushes-player`

Setup:

- Test level with water and current force `+120`.
- Teleport player into current.
- Step 30 frames.

Assertions:

- `player.vx` increases.

Then:

- Use current force `-120`.
- Step 30 frames.

Assertions:

- `player.vx` decreases.

---

### 43.6 Platforms

#### Test: `platform.one-way-landing`

Setup:

- Test level with one-way platform.
- Teleport player above platform.
- Step until player lands.

Assertions:

- `player.onGround === true`.
- `player.vy === 0`.
- Player bottom equals platform top within 1 px.

#### Test: `platform.one-way-pass-through`

Setup:

- Test level with one-way platform.
- Teleport player below platform.
- Press jump.

Assertions:

- Player passes through platform while rising.
- Player `y` decreases through platform top.

#### Test: `platform.lily-bounce`

Setup:

- Test level with lily pad.
- Teleport player above pad.
- Do not hold jump.
- Step until bounce occurs.

Assertions:

- `player.vy` is close to `-620`.
- `player.onGround === false`.

#### Test: `platform.lily-bounce-held`

Setup:

- Test level with lily pad.
- Teleport player above pad.
- Hold jump.
- Step until bounce occurs.

Assertions:

- `player.vy` is close to `-680`.

#### Test: `platform.moving-platform-carries-player`

Setup:

- Test level with horizontal moving platform.
- Place player on platform.
- Record player X.
- Step 30 frames.

Assertions:

- Player X changes in same direction as platform X.
- Player remains on platform.

#### Test: `platform.moving-platform-resets-on-respawn`

Setup:

- Test level with moving platform.
- `actions.setLevelTime(1)`.
- Kill player.
- Wait for respawn.

Assertions:

- `state.level.time === 0`.

---

### 43.7 Enemies and Damage

#### Test: `enemy.mosquito-patrols`

Setup:

- Test level with mosquito.
- Step 120 frames.

Assertions:

- Mosquito X stays within `minX` and `maxX`.
- Mosquito X changes over time.
- Mosquito eventually reverses direction if bounds are reached.

#### Test: `enemy.dragonfly-patrols`

Setup:

- Test level with dragonfly.
- Step 120 frames.

Assertions:

- Dragonfly X stays within `minX` and `maxX`.
- Dragonfly X changes over time.

#### Test: `enemy.stomp-kills-enemy`

Setup:

- Test level with enemy.
- Place enemy under player.
- Set player `vy = 100`.
- Step until collision.

Assertions:

- Enemy `alive === false`.
- Player `vy` is close to `-380`.

#### Test: `enemy.side-contact-damages`

Setup:

- Test level with enemy.
- Place enemy beside player.
- Step until collision.

Assertions:

- Player hearts decrease by 1.
- Player `invulnTimer > 0`.
- Player knockback direction is away from enemy.

#### Test: `enemy.invuln-ignores-damage`

Setup:

- Place enemy beside player.
- `actions.setInvulnerable(1)`.
- Step until collision.

Assertions:

- Player hearts unchanged.

#### Test: `enemy.invuln-stomp-works`

Setup:

- Place enemy under player.
- `actions.setInvulnerable(1)`.
- Set player `vy = 100`.
- Step until collision.

Assertions:

- Enemy dies.
- Player hearts unchanged.
- Player bounce occurs.

#### Test: `hazard.thorn-damages`

Setup:

- Test level with thorn.
- Teleport player into thorn.
- Step.

Assertions:

- Player hearts decrease by 1.

#### Test: `hazard.multiple-hazards-apply-one-damage`

Setup:

- Test level with enemy and thorn.
- Place player overlapping both.
- Step.

Assertions:

- Player hearts decrease by exactly 1.

#### Test: `player.death-respawn`

Setup:

- `actions.setHearts(1)`.
- `actions.damagePlayer(player.x)`.

Assertions:

- `player.dead === true`.

Step 36 frames.

Assertions:

- `player.dead === false`.
- `player.hearts === 3`.
- Player position is respawn point.

#### Test: `player.fall-below-level-kills`

Setup:

- `groundLevel(g)`.
- Teleport player to `y = level.height + 200`.
- Step.

Assertions:

- Player dies.
- After 36 frames, player respawns.

---

### 43.8 Dewdrops, Checkpoints, Exits

#### Test: `dewdrop.collect`

Setup:

- Test level with dewdrop.
- Teleport player to dewdrop.
- Step.

Assertions:

- `dewdrops.collected === 1`.

#### Test: `dewdrop.persist-after-respawn`

Setup:

- Collect dewdrop.
- Kill player.
- Wait for respawn.

Assertions:

- `dewdrops.collected === 1`.

#### Test: `dewdrop.reset-on-restart`

Setup:

- Collect dewdrop.
- `actions.restartLevel()`.

Assertions:

- `dewdrops.collected === 0`.

#### Test: `checkpoint.sets-respawn`

Setup:

- Test level with checkpoint.
- Teleport player to checkpoint.
- Step.
- Kill player.
- Wait for respawn.

Assertions:

- Respawn position equals checkpoint position.

#### Test: `checkpoint.refills-hearts`

Setup:

- `actions.setHearts(1)`.
- Teleport player to checkpoint.
- Step.

Assertions:

- `player.hearts === 3`.

#### Test: `exit.completes-level`

Setup:

- Test level with active exit.
- Teleport player to exit.
- Step.

Assertions:

- `state.gameState === "levelComplete"`.
- Level complete data shows correct dewdrop count.

#### Test: `exit.level-6-locked`

Setup:

- `actions.loadLevel(6)`.
- Teleport player to exit.
- Step.

Assertions:

- `state.gameState === "playing"`.

Then:

- `actions.setBossHp(0)`.
- Teleport player to exit.
- Step.

Assertions:

- `state.gameState === "gameComplete"`.

---

### 43.9 Boss

#### Test: `boss.idle-lunge-cycle`

Setup:

- `actions.loadLevel(6)`.
- Step 72 frames.

Assertions:

- Boss state changes from idle to lunge.
- During lunge, boss X moves toward player.

#### Test: `boss.phase-2-timing`

Setup:

- `actions.loadLevel(6)`.
- `actions.setBossHp(3)`.
- `actions.setBossState("idle")`.
- Step 48 frames.

Assertions:

- Boss enters lunge after approximately 0.8 seconds.
- Lunge speed is approximately `380` px/s.

#### Test: `boss.stomp-reduces-hp`

Setup:

- `actions.loadLevel(6)`.
- Place player above boss head.
- Set player `vy = 100`.
- Step until stomp.

Assertions:

- Boss HP decreases by 1.
- Player `vy` is close to `-420`.

#### Test: `boss.death-unlocks-exit`

Setup:

- `actions.loadLevel(6)`.
- `actions.setBossHp(1)`.
- Stomp boss.

Assertions:

- Boss `alive === false`.
- Boss state is `"dead"`.
- Exit active is true.

#### Test: `boss.dead-persists-after-respawn`

Setup:

- Kill boss.
- Kill player.
- Wait for respawn.

Assertions:

- Boss remains dead.
- Exit remains active.

---

### 43.10 HUD, UI, Messages

#### Test: `ui.level-name-message`

Setup:

- `groundLevel(g)`.
- Step 1 frame.

Assertions:

- Message text is level name.

Step 150 frames.

Assertions:

- Level name message has expired.

#### Test: `ui.tutorial-movement-hides`

Setup:

- `actions.loadLevel(1)`.

Assertions:

- `state.tutorial.activeId === "move"`.

Setup:

- `input.setRight(true)`.
- Step 1 frame.

Assertions:

- `state.tutorial.flags.firstHorizontalInput === true`.
- `state.tutorial.activeId !== "move"`.

#### Test: `ui.checkpoint-message`

Setup:

- Test level with checkpoint.
- Teleport player to checkpoint.
- Step 1 frame.

Assertions:

- Message text is `"Checkpoint"`.

Step 90 frames.

Assertions:

- Checkpoint message has expired.

#### Test: `ui.pause-resume`

Setup:

- `groundLevel(g)`.
- `actions.pause()`.

Assertions:

- `state.gameState === "paused"`.

Then:

- `actions.resume()`.

Assertions:

- `state.gameState === "playing"`.

#### Test: `ui.pause-restart-level`

Setup:

- `groundLevel(g)`.
- Collect a dewdrop if present or use test level with dewdrop.
- `actions.pause()`.
- `actions.restartLevel()`.

Assertions:

- `state.gameState === "playing"`.
- Player at spawn.
- Dewdrops collected is 0.

#### Test: `ui.pause-quit-to-title`

Setup:

- `actions.loadLevel(3)`.
- `actions.pause()`.
- `actions.quitToTitle()`.

Assertions:

- `state.gameState === "title"`.
- Save unlocked level is 3.

#### Test: `ui.pause-disabled-during-death`

Setup:

- `groundLevel(g)`.
- `actions.setHearts(1)`.
- `actions.damagePlayer(player.x)`.

Assertions:

- Player is dead.

Then:

- `actions.pause()`.

Assertions:

- `state.gameState !== "paused"`.

---

### 43.11 Full Game Flow

#### Test: `flow.synthetic-full-loop`

Setup:

- `smokeLevel(g)`.

Bot:

- Hold right.
- Step until level complete.
- Allow up to 3000 frames.

Assertions:

- `state.gameState === "levelComplete"`.
- Dewdrop count is at least 1.
- Checkpoint activated if player reached it.
- No exceptions.

This test proves the core loop works on a deterministic level.

#### Test: `flow.level-1-scripted-completion`

Setup:

- `freshGame()`.
- `actions.startNewGame()`.

Bot:

- Hold right.
- Use jump windows:
  - first gap: `x > 820 && x < 890`
  - thorn: `x > 1290 && x < 1340`
  - second gap: `x > 1460 && x < 1500`
- Press jump with hold frames `14` when:
  - player is on ground
  - player is in jump window
  - jump is not already held
- Step until level complete.
- Allow up to 9000 frames.
- If player dies, wait for respawn and continue.

Assertions:

- `state.gameState === "levelComplete"`.
- `state.save.unlocked_level === 2`.
- No exceptions.

This test is a regression smoke test for the authored first level.

If level 1 data changes, this bot must be updated.

#### Test: `flow.all-levels-complete-via-exit`

Setup:

- For each level 1 through 6:
  - `actions.loadLevel(index)`.
  - If level 6, `actions.setBossHp(0)`.
  - Teleport player to exit.
  - Step 1 frame.

Assertions:

- Levels 1 through 5:
  - `state.gameState === "levelComplete"`.
- Level 6:
  - `state.gameState === "gameComplete"`.

This test validates exit/state flow for all authored levels.

It uses teleport intentionally because platforming mechanics are tested separately.

#### Test: `flow.game-complete-after-level-6`

Setup:

- `actions.loadLevel(6)`.
- `actions.setBossHp(0)`.
- Teleport player to exit.
- Step 1 frame.

Assertions:

- `state.gameState === "gameComplete"`.
- `state.save.completed === true`.
- `state.save.unlocked_level === 6`.

Then:

- Press Enter/Space.

Assertions:

- `state.gameState === "title"`.
- Title options include `"Play Again"`.

---

## 44. Test Success Criteria

`test.html` is successful when:

```js
window.__testResults.failed === 0
window.__testResults.assertions > 100
```

The headless page may also verify:

```js
await window.__testsDone
```

A passing test suite proves:

- The game boots.
- Save/title flow works.
- All six levels load.
- Player movement works.
- Jumping works.
- Water works.
- Lily pads work.
- One-way platforms work.
- Moving platforms work.
- Enemies work.
- Stomping works.
- Damage/invulnerability works.
- Death/respawn works.
- Dewdrops work.
- Checkpoints work.
- Exits work.
- Boss works.
- HUD/messages work.
- Pause works.
- Level complete works.
- Game complete works.
- A scripted Level 1 playtest completes.

Human playability is still a final manual acceptance step, but the automated suite must pass before handoff.

---

## 45. Integration Contract with Visual Designer

The visual designer may provide:

- CSS
- canvas sprites
- HUD icons
- background art
- audio files

Engineering requirements for visual handoff:

1. Keep required DOM IDs.
2. Keep required CSS classes.
3. Do not move gameplay logic into CSS.
4. Do not change logical resolution.
5. Do not change hitboxes through visual styling.
6. Audio files must match required event names.
7. Missing visual assets must not break the game.
8. Placeholder rendering is acceptable during development.

The visual designer may change:

- colors
- fonts
- sprite art
- background art
- decorative HUD styling
- audio files

The visual designer must not change:

- player hitbox
- enemy hitbox
- level dimensions
- collision behavior
- state machine
- debug API
- test API

---

## 46. Integration Contract with Audio Designer

Required audio event names are fixed:

```text
jump
water_splash
lily_pad_bounce
stomp
damage
checkpoint
level_complete
boss_hit
boss_death
game_complete
```

The audio designer may choose:

- waveform
- length
- volume
- timbre
- file format

Engineering requirements:

- Files must be local.
- Files must use required names.
- Missing files must fail silently.
- Audio must not block gameplay.
- Audio must not require network.
- Audio must not require user interaction before first event, but browsers may delay playback until first gesture.

---

## 47. Engineering Cuts

The following are intentionally cut:

- procedural level generator
- level select
- score
- timer
- star ratings
- lives
- health pickups
- power-ups
- upgrades
- controller support
- remappable controls
- mobile touch controls
- music
- mute UI
- volume UI
- settings menu
- minimap
- objective arrow
- screen shake
- particle effects
- damage numbers
- floating text
- hitbox debug draw
- FPS counter
- console debug UI
- network features
- cloud save
- analytics
- error reporting
- service worker
- PWA
- WebGL
- external libraries
- build step
- TypeScript
- ES modules
- Node-based tests
- npm
- test runner
- unit test framework
- automated solvability checker
- random enemy spawns
- dynamic difficulty
- secret levels
- hidden required paths
- multiple frogs
- companion characters
- inventory
- weapons
- difficulty modes

Why:

- The game is short and focused.
- Each cut reduces integration risk.
- The core fantasy is a small frog making a big journey.
- The gameplay document already defines a complete scope.
- Tests must remain deterministic.
- The handoff agent must be able to implement and validate the game without external tooling.

---

## 48. Final Acceptance Criteria

The engineering handoff is complete when:

1. `index.html` opens in a browser and shows the title screen.
2. The player can start New Game and play Level 1.
3. All six levels load from authored data.
4. The player can complete Level 6 and see the game complete screen.
5. Save data persists unlocked level and completion state.
6. Pause, restart, controls, and quit all work.
7. HUD displays hearts, dewdrop count, and messages.
8. Required audio events are wired to named assets.
9. Missing assets do not break the game.
10. `test.html` loads and runs all required tests.
11. `window.__testResults.failed` is `0`.
12. No console errors occur during normal play or tests.
13. `window.__game` debug API works in the browser console.
14. The game uses only vanilla HTML, CSS, and JavaScript.
15. No build step is required.