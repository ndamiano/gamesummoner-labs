# engineering.md

## 1. Purpose

This document defines the engineering implementation for **Fridge Escape** in vanilla HTML, CSS, and JavaScript.

It is written so that another agent can implement the game without needing the original conversation. It defines:

- the files that should exist
- the runtime architecture
- the level compiler / level “generator” logic
- the core simulation loop
- the debug API used by tests
- the test harness
- the required test cases
- integration points for the visual and audio designers

The implementation must work in a browser with no build step, no Node, no npm, no package manager, and no test runner. The only external validation available is:

- a JavaScript syntax check
- tests executed inside a headless page against `window.__game`

---

## 2. Non-Goals and Cuts

The following are intentionally excluded:

- No procedural level generation.
  - The level is fixed and data-driven.
  - A future level can be added by editing level data, not by adding a generator.
- No physics engine.
- No external libraries.
- No ES module imports.
- No npm packages.
- No TypeScript.
- No build step.
- No save system.
- No difficulty options.
- No touch controls.
- No mouse aiming.
- No scoring system beyond the required win-screen stats.
- No persistent audio assets required for tests.
  - Audio hooks must exist and be recorded.
  - Actual audio playback is optional and asset-driven.

### Why these cuts exist

The game is short, single-level, keyboard-driven, and must be testable in a headless page. Every added system increases the surface area for integration failure. The core game is already complete with stealth, power, noise, AI, timer, win/lose states, and HUD.

---

## 3. File Layout

The project must contain these files.

```text
index.html
css/game.css
js/constants.js
js/math.js
js/prng.js
js/level-data.js
js/level.js
js/collision.js
js/pathfinding.js
js/noise.js
js/fridge.js
js/resident.js
js/input.js
js/audio.js
js/hud.js
js/render.js
js/game.js
js/debug.js
js/main.js
test/test.html
test/test.js
```

### File responsibilities

| File | Responsibility |
|---|---|
| `index.html` | Production game page. Loads CSS and JS in order. Contains canvas, HUD, overlays, buttons. |
| `css/game.css` | Layout, HUD styling, warning flashes, overlays, vignette. |
| `js/constants.js` | All tunable values and key mappings. |
| `js/math.js` | Vector, angle, rectangle, OBB, circle, and line-of-sight math. |
| `js/prng.js` | Deterministic seeded PRNG. |
| `js/level-data.js` | The fixed level definition. |
| `js/level.js` | Level compiler, validation, navgrid, room lookup, room adjacency. |
| `js/collision.js` | Fridge OBB vs solid rect collision, resident circle vs solid rect collision. |
| `js/pathfinding.js` | A* pathfinding on the navgrid. |
| `js/noise.js` | Noise event emission and hearing resolution. |
| `js/fridge.js` | Fridge state, movement, plug, door, hum, slide, power. |
| `js/resident.js` | Resident AI, perception, suspicion, movement, catch. |
| `js/input.js` | Keyboard input and debug input queue. |
| `js/audio.js` | Audio hook playback and recording. |
| `js/hud.js` | DOM HUD updates. |
| `js/render.js` | Canvas world rendering. |
| `js/game.js` | Game state machine, simulation tick, win/lose checks. |
| `js/debug.js` | Exposes `window.__game`. |
| `js/main.js` | Boots the game. Starts real-time loop only in production mode. |
| `test/test.html` | Test page. Loads game scripts plus test harness. |
| `test/test.js` | Tiny test harness and required tests. |

---

## 4. Script Loading Model

All JavaScript files are classic scripts loaded in order.

Do not use:

```js
import
export
require
module.exports
```

Use a single global namespace:

```js
window.FE = window.FE || {};
```

Example:

```js
window.FE = window.FE || {};

FE.Math = (function () {
  function dist(x1, y1, x2, y2) {
    var dx = x2 - x1;
    var dy = y2 - y1;
    return Math.sqrt(dx * dx + dy * dy);
  }

  return {
    dist: dist
  };
})();
```

The only allowed globals are:

- `window.FE`
- `window.__game`
- `window.__testResults` in the test page

### Why

Classic scripts avoid module loading issues in headless pages and file-based validation. They also make integration simpler for the next agent.

---

## 5. Production vs Test Mode

`index.html` is production mode.

`test/test.html` is test mode.

`test/test.html` must set this before loading any game scripts:

```html
<script>
  window.FE_TEST_MODE = true;
</script>
```

In test mode:

- no `requestAnimationFrame` loop runs
- no keyboard events are bound
- no visibility-based auto-pause is bound
- the game still boots
- `window.__game` is available
- tests drive the game through `window.__game`

In production mode:

- `requestAnimationFrame` runs
- keyboard input is bound
- visibility changes auto-pause the game

### Why

Tests must be deterministic. A real-time loop would race with test-driven ticks.

---

## 6. Core Loop and Determinism

The game uses a fixed simulation tick.

```js
FE.TICKS_PER_SECOND = 120;
FE.TICK = 1 / 120;
```

All gameplay updates happen in integer ticks.

Production loop:

```text
requestAnimationFrame
  -> measure real dt
  -> clamp dt to 0.1 seconds
  -> add dt to accumulator
  -> while accumulator >= TICK:
       game.tick()
       accumulator -= TICK
  -> render
```

Debug/test loop:

```text
window.__game.advanceTicks(n)
  -> calls game.tick() n times
  -> no real-time dependency
```

### Tick rules

- `game.tick()` only advances the world when state is `playing`.
- While paused, `advanceTicks()` does not change game state.
- The simulation tick counter only increments while playing.
- All timers use seconds internally but are updated by `TICK`.

### Why fixed ticks

- Deterministic tests.
- Stable collision at high slide speed.
- Stable AI and noise timing.
- Easy to validate with `advanceTicks(600)` for 5 seconds.

---

## 7. Global State Shape

`window.__game.getState()` must return a plain serializable object.

Recommended shape:

```js
{
  state: "start" | "playing" | "paused" | "win" | "lose",
  tick: number,
  time: number,
  timeRemaining: number,

  fridge: {
    x: number,
    y: number,
    angle: number,
    angleDeg: number,
    speed: number,
    speedAbs: number,

    plugged: boolean,
    plugAttempt: {
      active: boolean,
      remaining: number
    },

    power: number,
    doorOpen: boolean,

    slide: {
      active: boolean,
      remaining: number,
      cooldown: number
    },

    humCooldown: number,

    room: "kitchen" | "hallway" | "living",
    inWinZone: boolean,

    powerFlash: boolean,
    nearestOutletId: string | null
  },

  residents: [
    {
      id: "mom" | "dad" | "kid",
      active: boolean,
      x: number,
      y: number,
      angle: number,
      angleDeg: number,
      state: "routine" | "suspicious" | "investigate" | "search",
      suspicion: number,
      target: { x: number, y: number },
      lastKnown: { x: number, y: number },
      pathLength: number,
      hasPath: boolean
    }
  ],

  stats: {
    noiseEvents: number,
    residentsLured: number,
    luredIds: []
  },

  effects: {
    vignetteIntensity: number,
    noiseRings: [
      {
        x: number,
        y: number,
        radius: number,
        maxRadius: number,
        remaining: number
      }
    ]
  },

  hud: {
    objective: string,
    prompt: string,
    timerWarning: boolean,
    powerWarning: boolean,
    plug: boolean,
    door: boolean
  },

  loseReason: null | "caught" | "power" | "timer"
}
```

### Notes

- `angle` is radians internally.
- `angleDeg` is provided for tests and HUD.
- `time` is elapsed playing seconds.
- `timeRemaining` starts at `120`.
- `residents` always contains all three residents, with `active: false` before spawn.

---

## 8. Constants

All gameplay values should live in `js/constants.js`.

Required constants:

```js
FE.TICKS_PER_SECOND = 120;
FE.TICK = 1 / 120;

FE.GAME_TIME = 120;

FE.FRIDGE = {
  LENGTH: 64,
  WIDTH: 32,
  HALF_LENGTH: 32,
  HALF_WIDTH: 16,

  MAX_WADDLE_SPEED: 50,
  ACCELERATION: 120,
  DECELERATION: 180,
  TURN_SPEED_DEG: 100,

  SLIDE_SPEED: 150,
  SLIDE_DURATION: 0.25,
  SLIDE_COOLDOWN: 0.6,
  SLIDE_COST: 10,

  PLUG_RADIUS: 48,
  PLUG_TIME: 0.5,
  RECHARGE_RATE: 15,

  DRAIN_PASSIVE: 1,
  DRAIN_WADDLE: 3,
  DRAIN_ROTATE: 1.5,
  DRAIN_DOOR: 0.5,

  HUM_COST: 15,
  HUM_COOLDOWN: 3,
  HUM_RADIUS: 160,
  HUM_ALERT: 100
};

FE.NOISE = {
  STEP: { radius: 12, alert: 15, interval: 0.6, minSpeed: 10 },
  SLIDE: { radius: 50, alert: 45, interval: 0.2 },
  COLLISION: { radius: 25, alert: 30, minImpactSpeed: 30 },
  PLUG: { radius: 10, alert: 10 },
  UNPLUG: { radius: 20, alert: 25 },
  DOOR: { radius: 15, alert: 15 },
  HUM: { radius: 160, alert: 100 }
};

FE.RESIDENT = {
  RADIUS: 20,
  ROUTINE_SPEED: 70,
  INVESTIGATE_SPEED: 110,
  VIEW_RADIUS: 160,
  FOV_DEG: 120,
  LOS_STEP: 8,
  CATCH_DISTANCE: 40,

  SUSPICION_BASE: 20,
  SUSPICION_MOVING: 20,
  SUSPICION_UNPLUGGED: 20,
  SUSPICION_DOOR: 10,
  SUSPICION_NOT_KITCHEN: 10,
  SUSPICION_CLOSE: 20,
  SUSPICION_CLOSE_DISTANCE: 80,
  SUSPICION_DECAY: 25,
  SUSPICIOUS_NO_DETECT_TIME: 1.5,
  SEARCH_TIME: 3,

  PATH_RECALC_TIME: 0.5,
  DWELL_MIN: 0.5,
  DWELL_MAX: 2.0
};

FE.KEYS = {
  UP: ["KeyW", "ArrowUp"],
  DOWN: ["KeyS", "ArrowDown"],
  LEFT: ["KeyA", "ArrowLeft"],
  RIGHT: ["KeyD", "ArrowRight"],
  SLIDE: ["Space"],
  DOOR: ["KeyE"],
  HUM: ["KeyQ"],
  PLUG: ["KeyP"],
  PAUSE: ["Escape"]
};
```

### Why

Centralizing constants makes tuning easier and makes tests predictable.

---

## 9. Level Data and Level Compiler

The level is not procedurally generated. It is a fixed data object compiled into runtime structures.

This is the “level generator” for this project: it generates the runtime level, navgrid, room graph, and validation results from level data.

### 9.1 Nav Tile Decision

The gameplay document mentions a 32-unit pathfinding tile, but the level dimensions and doorway sizes do not align cleanly with 32:

- `720 / 32 = 22.5`
- doorway height is `80`, which is not a multiple of `32`

Engineering uses:

```js
FE.NAV_TILE = 20;
```

This gives:

```text
1280 / 20 = 64 columns
720 / 20 = 36 rows
80 / 20 = 4 doorway cells
```

This makes the navgrid exact, deterministic, and easier to validate.

### Why this supersedes the 32-unit tile

- All designer coordinates are multiples of 20 or align cleanly.
- Doorways become exactly 4 cells tall.
- The grid is exactly `64 x 36`.
- A* is still cheap.
- Collision remains continuous and uses the original designer units.

If the team insists on 32, the level compiler would need fractional tiles and special boundary rules. That is more complex for no gameplay benefit.

---

## 10. Fixed Level Data

`js/level-data.js` must define the level.

```js
FE.levelData = {
  width: 1280,
  height: 720,
  navTile: 20,

  rooms: [
    {
      id: "kitchen",
      x: 0,
      y: 0,
      w: 480,
      h: 720,
      adjacent: ["hallway"]
    },
    {
      id: "hallway",
      x: 480,
      y: 0,
      w: 320,
      h: 720,
      adjacent: ["kitchen", "living"]
    },
    {
      id: "living",
      x: 800,
      y: 0,
      w: 480,
      h: 720,
      adjacent: ["hallway"]
    }
  ],

  walls: [
    { id: "top", x: 0, y: 0, w: 1280, h: 20, blocksMovement: true, blocksSight: true },
    { id: "bottom", x: 0, y: 700, w: 1280, h: 20, blocksMovement: true, blocksSight: true },
    { id: "left", x: 0, y: 0, w: 20, h: 720, blocksMovement: true, blocksSight: true },

    { id: "right-top", x: 1260, y: 0, w: 20, h: 320, blocksMovement: true, blocksSight: true },
    { id: "right-bottom", x: 1260, y: 400, w: 20, h: 320, blocksMovement: true, blocksSight: true },

    { id: "kitchen-hall-top", x: 470, y: 0, w: 20, h: 320, blocksMovement: true, blocksSight: true },
    { id: "kitchen-hall-bottom", x: 470, y: 400, w: 20, h: 320, blocksMovement: true, blocksSight: true },

    { id: "hall-living-top", x: 790, y: 0, w: 20, h: 320, blocksMovement: true, blocksSight: true },
    { id: "hall-living-bottom", x: 790, y: 400, w: 20, h: 320, blocksMovement: true, blocksSight: true }
  ],

  obstacles: [
    { id: "top-counter", x: 20, y: 20, w: 440, h: 60, blocksMovement: true, blocksSight: true },
    { id: "left-counter", x: 20, y: 100, w: 60, h: 320, blocksMovement: true, blocksSight: true },
    { id: "sink", x: 200, y: 100, w: 80, h: 80, blocksMovement: true, blocksSight: true },
    { id: "stove", x: 360, y: 100, w: 80, h: 80, blocksMovement: true, blocksSight: true },

    { id: "plant", x: 600, y: 120, w: 60, h: 60, blocksMovement: true, blocksSight: true },
    { id: "shoe-rack", x: 600, y: 540, w: 60, h: 60, blocksMovement: true, blocksSight: true },

    { id: "sofa", x: 900, y: 80, w: 220, h: 80, blocksMovement: true, blocksSight: true },
    { id: "coffee-table", x: 1000, y: 300, w: 100, h: 80, blocksMovement: true, blocksSight: true },
    { id: "tv-stand", x: 1200, y: 80, w: 60, h: 120, blocksMovement: true, blocksSight: true },
    { id: "bookshelf", x: 1200, y: 520, w: 60, h: 120, blocksMovement: true, blocksSight: true }
  ],

  outlets: [
    { id: "kitchen-outlet", x: 120, y: 500, radius: 48 },
    { id: "hallway-outlet", x: 640, y: 360, radius: 48 },
    { id: "living-outlet", x: 900, y: 600, radius: 48 }
  ],

  residents: [
    {
      id: "mom",
      spawnSeconds: 5,
      waypoints: [
        { x: 140, y: 140 },
        { x: 300, y: 140 },
        { x: 300, y: 620 },
        { x: 140, y: 620 }
      ]
    },
    {
      id: "dad",
      spawnSeconds: 10,
      waypoints: [
        { x: 1000, y: 200 },
        { x: 640, y: 200 },
        { x: 640, y: 500 },
        { x: 1000, y: 500 }
      ]
    },
    {
      id: "kid",
      spawnSeconds: 20,
      waypoints: [
        { x: 1050, y: 240 },
        { x: 1160, y: 360 },
        { x: 1050, y: 480 },
        { x: 940, y: 360 }
      ]
    }
  ],

  fridgeStart: {
    x: 180,
    y: 500,
    angle: 0,
    plugged: true,
    power: 100,
    doorOpen: false
  },

  winZone: {
    x: 1240,
    y: 320,
    w: 40,
    h: 80
  }
};
```

### Why walls are explicit

The gameplay document describes openings but not wall rectangles. Explicit wall rectangles make collision, line of sight, and navgrid generation deterministic.

The internal walls are 20 units thick and aligned to the 20-unit navgrid.

---

## 11. Level Compiler

`js/level.js` must compile `FE.levelData` into a runtime level.

Recommended API:

```js
FE.Level = {
  compile: function (data) {
    // returns runtime level
  },
  validate: function (data) {
    // throws Error if invalid
  },
  roomAt: function (x, y) {
    // returns "kitchen" | "hallway" | "living"
  },
  roomModifier: function (roomA, roomB) {
    // returns 1.0, 0.5, or 0.0
  },
  solidRects: function () {
    // returns movement-blocking rects
  },
  sightRects: function () {
    // returns sight-blocking rects
  }
};
```

### Compile steps

1. Copy level data.
2. Build `solidRects`:
   - all walls with `blocksMovement: true`
   - all obstacles with `blocksMovement: true`
3. Build `sightRects`:
   - all walls with `blocksSight: true`
   - all obstacles with `blocksSight: true`
4. Build navgrid:
   - `cols = width / navTile`
   - `rows = height / navTile`
   - cell is walkable if its center is not inside any solid rect
5. Build room adjacency map.
6. Run validation.

### Navgrid cell rule

A cell is walkable if:

```text
cell center is inside the playfield
AND
cell center is not inside any movement-blocking rect
```

Cell center:

```text
x = col * navTile + navTile / 2
y = row * navTile + navTile / 2
```

### Room lookup

Use the designer x ranges:

```text
x < 480       -> kitchen
480 <= x < 800 -> hallway
x >= 800      -> living
```

This is simpler and more stable than using room rectangles that overlap wall thickness.

### Room modifier

```text
same room        -> 1.0
adjacent rooms   -> 0.5
non-adjacent     -> 0.0
```

Adjacency:

```text
kitchen adjacent hallway
hallway adjacent living
kitchen not adjacent living
```

### Validation requirements

`FE.Level.validate` must throw if any of these fail:

- playfield dimensions are positive
- navgrid dimensions are integers
- fridge start center is not inside a solid rect
- fridge start OBB does not intersect a solid rect
- every outlet center is not inside a solid rect
- every resident waypoint is not inside a solid rect
- win zone center is not inside a solid rect
- an A* path exists from fridge start to win zone center using static navgrid
- room graph is connected

### Why validation matters

The gameplay designer owns level content, but engineering owns making it function. A bad level should fail tests immediately, not produce weird runtime behavior.

---

## 12. Math and Collision

### 12.1 Vector and angle helpers

Required functions:

```js
FE.Math.dist(x1, y1, x2, y2)
FE.Math.angleTo(x1, y1, x2, y2)
FE.Math.angleDiff(a, b)
FE.Math.normalizeAngle(a)
FE.Math.degToRad(deg)
FE.Math.radToDeg(rad)
FE.Math.lerpAngle(a, b, t)
```

Angles are radians internally.

### 12.2 Point in rect

Use half-open intervals:

```text
x >= rect.x && x < rect.x + rect.w
y >= rect.y && y < rect.y + rect.h
```

### 12.3 Fridge collider

The fridge is an oriented bounding box.

```text
length = 64
width = 32
halfLength = 32
halfWidth = 16
```

Local axes:

```text
forward = (cos(angle), sin(angle))
side = (-sin(angle), cos(angle))
```

Corners:

```text
center + forward * halfLength + side * halfWidth
center + forward * halfLength - side * halfWidth
center - forward * halfLength + side * halfWidth
center - forward * halfLength - side * halfWidth
```

### 12.4 Fridge vs solid rect collision

Use SAT between an OBB and an AABB.

Axes to test:

- world X
- world Y
- fridge forward axis
- fridge side axis

For each axis:

1. Project fridge OBB.
2. Project AABB.
3. If separated, no collision.
4. Track minimum overlap axis.

If colliding:

- push fridge center out along the minimum translation vector
- repeat against all solids, up to 2 passes
- if collision occurred, record impact speed for noise

### Why SAT

The fridge rotates. Axis-aligned collision would be wrong. SAT is small, deterministic, and sufficient for this game.

### 12.5 Resident vs solid rect collision

Residents are circles with radius `20`.

Use circle vs AABB:

1. Find closest point on rect to circle center.
2. If distance < radius, push circle out.
3. If center is inside rect, push out along smallest penetration axis.

### 12.6 Line of sight

Line of sight is blocked by sight rects.

Algorithm:

```text
from resident center to fridge center
sample every 8 units
if any sample is inside a sight rect, blocked
```

Use:

```text
for d = 0; d <= distance; d += 8
```

If the endpoint is inside a sight rect, treat as blocked.

---

## 13. Fridge System

### 13.1 Initial state

At game start:

```text
x = 180
y = 500
angle = 0
plugged = true
power = 100
doorOpen = false
slide.active = false
slide.cooldown = 0
humCooldown = 0
plugAttempt.active = false
```

### 13.2 Movement

Waddle input is relative to facing direction.

Input mapping:

```text
W / Up    -> forward
S / Down  -> backward
A / Left  -> rotate left
D / Right -> rotate right
```

Movement model:

- `speed` is scalar along facing direction.
- Positive is forward.
- Negative is backward.
- Max forward/back speed is `50`.
- Acceleration is `120`.
- Deceleration is `180`.

Target speed:

```text
if forward input: target = 50
else if backward input: target = -50
else: target = 0
```

Update speed:

```text
if speed < target:
  speed += ACCELERATION * dt
  clamp to target
else if speed > target:
  speed -= DECELERATION * dt
  clamp to target
```

Position update:

```text
x += cos(angle) * speed * dt
y += sin(angle) * speed * dt
```

Rotation:

```text
if left input: angle -= TURN_SPEED * dt
if right input: angle += TURN_SPEED * dt
```

`TURN_SPEED` is `100 degrees/sec`.

### 13.3 Plugged movement restrictions

If plugged:

- no waddle movement
- no rotation
- no slide
- no plug attempt
- door can toggle
- hum can occur if power allows

### 13.4 Slide

Slide conditions:

- state is playing
- fridge is unplugged
- power >= 10
- slide cooldown <= 0
- slide is not already active
- plug attempt is not active

On successful slide:

```text
slide.active = true
slide.remaining = 0.25
slide.cooldown = 0.6
power -= 10
emit noise type "slide"
play audio hook "slide"
```

While sliding:

- move at `150` units/sec in facing direction
- ignore waddle input
- ignore rotation input
- emit slide noise every `0.2` seconds while active
- if collision occurs, slide ends

After slide ends:

```text
slide.active = false
```

Cooldown continues counting down.

### Why slide is not waddle drain

Slide has an instant power cost. Waddle drain should not also apply during slide.

---

## 14. Plug and Power System

### 14.1 Power

Power range:

```text
0 to 100
```

Power starts at `100`.

### 14.2 Plugged behavior

If plugged:

- cannot move
- cannot rotate
- cannot slide
- power recharges at `15/sec`
- passive drain is `0`

### 14.3 Unplugged drain

If unplugged:

- passive drain: `1/sec`
- waddle drain: `+3/sec` if not sliding and `speedAbs > 1`
- rotate drain: `+1.5/sec` if rotating input is active
- door drain: `+0.5/sec` if door open

Slide and hum are instant costs.

### 14.4 Plug attempt

Pressing `P` while unplugged:

1. Find nearest outlet within `48` units.
2. If none:
   - no plug attempt
   - optional prompt: “No outlet nearby.”
3. If one exists:
   - start plug attempt
   - `plugAttempt.active = true`
   - `plugAttempt.remaining = 0.5`
   - emit noise type `plug`
   - play audio hook `plug`

During plug attempt:

- fridge remains unplugged
- passive power drain continues
- if player moves, rotates, slides, or presses `P` again:
  - plug attempt fails
  - fridge remains unplugged

If plug attempt completes:

- `plugged = true`
- `plugAttempt.active = false`
- fridge becomes stationary
- recharge begins

### 14.5 Unplug

Pressing `P` while plugged:

- immediately unplug
- emit noise type `unplug`
- play audio hook `unplug`

### 14.6 Power loss

If power reaches `0`:

- lose reason is `power`
- lose text is “Your hum faded.”

Instant costs can cause power loss. Recharge does not rescue the fridge in the same tick after an instant cost reduces power to zero.

### Why

This makes power management active and prevents plugged-in stalling from being completely safe.

---

## 15. Door and Hum System

### 15.1 Door

Press `E` to toggle door.

On toggle:

- emit noise type `door`
- play audio hook `door_open` or `door_close`
- if unplugged and door open, power drains `+0.5/sec`
- residents are more suspicious of an open door

### 15.2 Hum

Press `Q`.

Hum conditions:

- door open
- power >= 15
- hum cooldown <= 0
- state is playing

On successful hum:

```text
power -= 15
humCooldown = 3
emit noise type "hum"
play audio hook "hum"
```

Hum noise:

```text
radius = 160
alert = 100
```

Residents who hear hum with alert >= 50 are set to investigate the hum location.

### 15.3 Hum while plugged

Hum is allowed while plugged if power is sufficient.

This matches the gameplay rule that hum can still be used while plugged.

### Why

The door is the fridge’s identity. Hum is the main active stealth tool.

---

## 16. Noise System

Noise is event-based.

When a noise event is emitted:

1. Record event.
2. Increment `stats.noiseEvents`.
3. For each active resident:
   - determine source room
   - determine resident room
   - apply room modifier
   - check hearing distance
   - update suspicion and state

### 16.1 Noise event shape

```js
{
  tick: number,
  type: "step" | "slide" | "collision" | "plug" | "unplug" | "door" | "hum" | "force",
  x: number,
  y: number,
  radius: number,
  alert: number,
  heardBy: []
}
```

### 16.2 Noise sources

| Source | Radius | Alert | Notes |
|---|---:|---:|---|
| Waddle step | 12 | 15 | every 0.6s while not sliding and speed > 10 |
| Slide | 50 | 45 | at slide start and every 0.2s while sliding |
| Collision | 25 | 30 | if impact speed > 30 |
| Plug connection | 10 | 10 | when plug attempt starts |
| Unplug | 20 | 25 | when unplugging |
| Door toggle | 15 | 15 | when door opens or closes |
| Hum | 160 | 100 | at fridge position |

### 16.3 Hearing algorithm

For each active resident:

```text
sourceRoom = roomAt(noise.x, noise.y)
residentRoom = roomAt(resident.x, resident.y)
modifier = roomModifier(sourceRoom, residentRoom)
effectiveRadius = noise.radius * modifier
distance = dist(resident, noise)

if distance <= effectiveRadius:
  resident.lastKnown = noise position
  resident.suspicion = max(resident.suspicion, noise.alert)
  if noise.alert >= 50:
    resident.state = "investigate"
    resident.target = noise position
    mark resident as lured if not already counted
```

### 16.4 Residents lured stat

`stats.residentsLured` counts unique residents that enter `investigate` because of a noise event with alert >= 50.

Sight-based investigation does not count as “lured.”

### Why

This gives the win screen a meaningful stat tied to the hum/decoy mechanic.

---

## 17. Resident System

### 17.1 Resident data

Each resident has:

```text
id
active
x
y
angle
state
suspicion
target
lastKnown
waypointIndex
dwellTime
path
pathIndex
hasPath
pathTimer
searchTimer
noDetectTimer
```

States:

```text
routine
suspicious
investigate
search
```

### 17.2 Spawn times

Residents activate at:

```text
mom = 5 seconds
dad = 10 seconds
kid = 20 seconds
```

On activation:

- choose first waypoint that is at least `40` units from fridge
- if none, delay spawn and recheck every `1` second
- state is `routine`
- suspicion is `0`
- angle faces next waypoint
- dwell time is random between `0.5` and `2.0` seconds

### Why spawn safety check

Prevents an unfair instant lose if the player is standing at a spawn point when the resident appears.

---

## 18. Resident Perception

### 18.1 Sight

A resident sees the fridge if:

- distance <= `160`
- fridge is inside field of view
- line of sight is not blocked

Field of view is `120` degrees total, so half-angle is `60` degrees.

Angle check:

```text
angleToResident = angle from resident facing to fridge vector
if abs(angleToResident) <= 60 degrees, in FOV
```

### 18.2 Anomaly detection

The fridge is abnormal if any of these are true:

- unplugged
- moving, `speedAbs > 5`
- door open
- not in kitchen
- within `80` units of resident

If the fridge is plugged, stationary, in the kitchen, door closed, and not within `80` units, it is normal.

### 18.3 Suspicion rate

If a resident sees an abnormal fridge:

```text
rate = 20
if moving: rate += 20
if unplugged: rate += 20
if door open: rate += 10
if not kitchen: rate += 10
if distance < 80: rate += 20
```

Suspicion increases by:

```text
rate * dt
```

If the resident no longer sees an abnormal fridge:

```text
suspicion -= 25 * dt
clamp to 0
```

### 18.4 Suspicion thresholds

- `suspicion > 0` and state is `routine` -> become `suspicious`
- `suspicion >= 100` -> become `investigate`
- noise alert >= 50 -> become `investigate` immediately

---

## 19. Resident AI States

### 19.1 Routine

- follows waypoint loop
- speed `70`
- faces movement direction
- dwells at each waypoint for random `0.5` to `2.0` seconds
- if suspicion > 0, becomes `suspicious`

### 19.2 Suspicious

- stops moving
- faces fridge if seen, otherwise faces `lastKnown`
- if sees abnormal fridge, suspicion increases
- if no abnormal detection for `1.5` seconds, suspicion decays
- if suspicion reaches `0`, returns to `routine`
- if suspicion reaches `100`, becomes `investigate`

### 19.3 Investigate

- moves to target at speed `110`
- target is usually `lastKnown`
- if resident sees fridge while investigating:
  - target becomes fridge current position
  - suspicion becomes `100`
- if reaches target and does not see fridge:
  - becomes `search`

### 19.4 Search

- waits at target for `3` seconds
- scans by rotating
- perception remains active
- if sees abnormal fridge, becomes `suspicious` or `investigate` based on suspicion
- after `3` seconds:
  - state becomes `routine`
  - suspicion becomes `0`

### Why

This creates a readable detection loop:

```text
normal -> suspicious -> investigate -> search -> routine
```

The player can see suspicion rising and react.

---

## 20. Resident Pathfinding

Residents use A* on the navgrid.

### 20.1 Grid

```text
tile = 20
cols = 64
rows = 36
```

### 20.2 Walkable cells

Static walkable cells come from the level compiler.

Dynamic blocked cells come from the fridge.

Fridge dynamic blocking:

- mark a cell blocked if its center is inside the fridge OBB
- this approximates the fridge as a moving obstacle
- use the actual OBB, not a fixed 3x2 tile

### Why actual OBB

The fridge collider is `64 x 32`. A fixed 3x2 tile would not represent its actual footprint accurately at all angles.

### 20.3 Path recalculation

Recalculate path:

- immediately when target changes significantly
- every `0.5` seconds
- when state changes to `routine` or `investigate`

If no path exists:

- resident stops
- faces target
- does not catch fridge unless within `40` units

### 20.4 A* requirements

- 4-neighbor movement
- Manhattan heuristic
- deterministic tie-breaking
- integer or stable float scores
- if goal cell is blocked, search for nearest walkable cell within a small radius
- if start cell is blocked by fridge, allow start cell

### Why

Residents must navigate around furniture and doorways. Direct movement would get them stuck.

---

## 21. Catch Condition

A resident catches the fridge if:

```text
dist(resident.center, fridge.center) <= 40
```

When caught:

- state becomes `lose`
- lose reason is `caught`
- lose text is “You got unplugged.”

Catch is checked after resident movement.

### Why

Distance-based catching is simple and readable.

---

## 22. Win and Lose Priority

At the end of each playing tick, check in this order:

1. Win
2. Caught
3. Power depleted
4. Timer expired

### Win

Fridge center is in win zone:

```text
x >= 1240
320 <= y <= 400
```

If win condition is true, the game wins even if another lose condition is also true in the same tick.

### Lose reasons

| Reason | Text |
|---|---|
| caught | “You got unplugged.” |
| power | “Your hum faded.” |
| timer | “The movers arrived.” |

### Why priority matters

The design explicitly says reaching the door at the same moment as another condition should win.

---

## 23. Game States

States:

```text
start
playing
paused
win
lose
```

### 23.1 Start

- world is visible but not updated
- timer is `120`
- residents are inactive
- Play button starts game

### 23.2 Playing

- all systems update
- timer counts down
- residents spawn over time

### 23.3 Paused

- timer stops
- residents stop
- fridge stops
- noise events stop
- plug attempt freezes
- slide freezes
- overlay shows Resume and Restart

Pause is triggered by:

- `Escape` while playing
- browser tab hidden while playing

Resume is triggered by:

- `Escape` while paused
- Resume button

### 23.4 Win

- triggered by win zone
- shows stats
- Play Again button calls restart

### 23.5 Lose

- triggered by caught, power, or timer
- shows lose reason
- Retry button calls restart

---

## 24. Restart and Reset

Required debug/game methods:

```js
reset()
start()
restart()
pause()
resume()
```

Behavior:

| Method | Behavior |
|---|---|
| `reset()` | Clears world and returns to `start` state. |
| `start()` | If in `start`, enters `playing`. |
| `restart()` | Calls `reset()` then enters `playing`. |
| `pause()` | If `playing`, enters `paused`. |
| `resume()` | If `paused`, enters `playing`. |

UI buttons:

- Start screen Play -> `start()`
- Pause Resume -> `resume()`
- Pause Restart -> `restart()`
- Win Play Again -> `restart()`
- Lose Retry -> `restart()`

### Why

Tests need clean deterministic resets. UI needs immediate retry without returning to start screen.

---

## 25. HUD

The HUD is DOM-based.

Required DOM ids:

```html
<canvas id="game-canvas" width="1280" height="720"></canvas>

<div id="hud">
  <div id="hud-objective"></div>
  <div id="hud-timer"></div>
  <div id="hud-power-wrap">
    <div id="hud-power-bar"></div>
    <span id="hud-plug-icon"></span>
    <span id="hud-door-icon"></span>
  </div>
  <div id="hud-prompt"></div>
  <div id="hud-controls"></div>
</div>

<div id="vignette"></div>

<div id="overlay-start" class="overlay">
  <h1>Fridge Escape</h1>
  <p>You are awake. Leave before the movers arrive.</p>
  <div id="start-controls"></div>
  <button id="btn-play">Play</button>
</div>

<div id="overlay-pause" class="overlay hidden">
  <h2>Paused</h2>
  <button id="btn-resume">Resume</button>
  <button id="btn-pause-restart">Restart</button>
</div>

<div id="overlay-end" class="overlay hidden">
  <h2 id="end-title"></h2>
  <p id="end-reason"></p>
  <div id="end-stats"></div>
  <button id="btn-again"></button>
</div>
```

### 25.1 Objective text

Use:

| Condition | Objective |
|---|---|
| Plugged in kitchen at start | “Unplug and leave.” |
| Unplugged in kitchen | “Leave the kitchen.” |
| In hallway | “Cross the hallway.” |
| In living room | “Reach the front door.” |
| In win zone | “Escape!” |

### 25.2 Timer

Display seconds remaining.

Warning state:

- when `timeRemaining < 30`
- timer flashes red
- audio hook `timer_warning` plays once when crossing below 30

### 25.3 Power

Display power bar from `0` to `100`.

Warning state:

- when `power < 25`
- power bar flashes red
- audio hook `power_warning` plays once when crossing below 25

### 25.4 Plug and door icons

- plug icon shows plugged/unplugged
- door icon shows open/closed

### 25.5 Contextual prompt

Prompt priority:

1. If plug attempt active:
   - “Hold still to plug in.”
2. Else if near outlet and unplugged:
   - “Press P to plug in and recharge.”
3. Else if plugged:
   - “Press P to unplug.”
4. Else if power < 25:
   - “Find an outlet.”
5. Else if door open and hum ready:
   - “Press Q to hum.”
6. Else if door closed and power >= 15:
   - “Press E to open your door.”
7. Else if slide ready:
   - “Press Space to slide. It is loud.”
8. Else:
   - empty string

### 25.6 Tutorial prompts

Use a simple tutorial step system.

Tutorial steps:

| Step | Prompt | Advance condition |
|---|---|---|
| 0 | “You are awake. Press P to unplug.” | fridge unplugs |
| 1 | “W/S: waddle. A/D: turn.” | fridge moves more than 20 units from start |
| 2 | “Space: slide. Fast, but loud.” | slide used or 5 seconds pass |
| 3 | “E: open/close door. Q: hum. Hum lures residents.” | door opened or 5 seconds pass |
| 4 | “Reach the front door before time runs out.” | win |

Tutorial prompt can be overridden by urgent contextual prompts such as plug attempt or low power.

### Why

The player needs clear guidance without a manual.

---

## 26. World Indicators

These are rendered in the world, not only in the HUD.

### 26.1 Resident awareness

Above each active resident:

- suspicion `0`: no icon
- suspicion `1` to `99`: eye icon, opacity = suspicion / 100
- suspicion `100`: exclamation icon

### 26.2 Noise rings

When a noise event occurs:

- create a ring at source
- max radius proportional to noise radius
- fade over about `0.4` seconds
- hum rings should be visibly larger than other rings

State should expose:

```js
effects.noiseRings
```

### 26.3 Warning vignette

Use a DOM overlay with inset shadow.

Vignette rule:

```text
maxSuspicion = maximum resident suspicion

if maxSuspicion > 50:
  vignetteIntensity = maxSuspicion / 100
else:
  vignetteIntensity = 0
```

At suspicion `100`, vignette intensity is `1`.

### Why

The vignette gives emotional warning without requiring the player to inspect every resident.

---

## 27. Audio System

The visual/audio designer owns the actual sound design. Engineering owns the hooks and playback implementation.

### 27.1 Audio hooks

Required hooks:

```text
waddle
slide
plug
unplug
door_open
door_close
hum
suspicion
investigate
timer_warning
power_warning
win
lose
```

### 27.2 Audio asset manifest

The audio designer may provide:

```js
window.FE.audioAssets = {
  waddle: "assets/audio/waddle.ogg",
  slide: "assets/audio/slide.ogg",
  plug: "assets/audio/plug.ogg",
  unplug: "assets/audio/unplug.ogg",
  door_open: "assets/audio/door_open.ogg",
  door_close: "assets/audio/door_close.ogg",
  hum: "assets/audio/hum.ogg",
  suspicion: "assets/audio/suspicion.ogg",
  investigate: "assets/audio/investigate.ogg",
  timer_warning: "assets/audio/timer_warning.ogg",
  power_warning: "assets/audio/power_warning.ogg",
  win: "assets/audio/win.ogg",
  lose: "assets/audio/lose.ogg"
};
```

If assets are missing, audio playback is silent, but hooks are still recorded.

### 27.3 Loop handling

`waddle` is a loop.

- start when fridge `speedAbs > 10` and not sliding
- stop when `speedAbs <= 10` or sliding

All other hooks are one-shots.

### 27.4 Audio event recording

`window.__game.getAudioEvents(sinceTick)` returns:

```js
[
  {
    tick: number,
    hook: string,
    loop: boolean
  }
]
```

### Why

Tests can validate that the correct hooks fire without requiring actual audio files.

---

## 28. Rendering

The world is rendered on canvas.

The HUD is rendered in DOM.

### 28.1 Canvas

Canvas size:

```text
1280 x 720
```

It should scale to fit the viewport while preserving aspect ratio.

### 28.2 Draw order

1. floor / room backgrounds
2. win zone
3. outlets
4. obstacles
5. walls
6. residents
7. fridge
8. noise rings
9. resident awareness icons

Vignette is DOM.

### 28.3 Visual designer integration

The visual designer may replace or extend:

- `js/render.js`
- `css/game.css`

They should not need to change:

- state shape
- debug API
- simulation logic
- level compiler

Placeholder rendering should be simple vector shapes:

- fridge: rotated rectangle
- residents: circles
- outlets: small circles
- win zone: highlighted doorway
- obstacles: filled rects
- walls: darker rects

### Why

This keeps visual work separate from simulation logic.

---

## 29. Input System

### 29.1 Production keyboard input

Bind to `window`.

Prevent default for game keys to avoid page scrolling.

Held keys:

```text
W / ArrowUp
S / ArrowDown
A / ArrowLeft
D / ArrowRight
```

Edge-triggered keys:

```text
Space
E
Q
P
Escape
```

### 29.2 Edge handling

Edge actions are queued and processed once per tick.

Processing order:

```text
Escape
P
E
Q
Space
```

If `Escape` pauses the game, other edge actions in that tick are ignored.

### 29.3 Debug input

`window.__game` must expose:

```js
setHeld(codes)
clearHeld()
tap(code)
```

Examples:

```js
__game.setHeld(["KeyW"]);
__game.tap("KeyP");
__game.clearHeld();
```

`tap(code)` simulates a keydown/keyup edge action.

### Why

Tests must be able to drive input deterministically.

---

## 30. Debug API

`window.__game` is the official test and QA API.

It must be available after the game boots.

### 30.1 Required API

```js
window.__game = {
  version: "1.0.0",
  ready: false,

  boot: function () {},
  reset: function () {},
  start: function () {},
  restart: function () {},
  pause: function () {},
  resume: function () {},

  tick: function () {},
  advanceTicks: function (n) {},

  getState: function () {},
  getNoiseEvents: function (sinceTick) {},
  getAudioEvents: function (sinceTick) {},
  clearEvents: function () {},

  setHeld: function (codes) {},
  clearHeld: function () {},
  tap: function (code) {},

  simulateVisibility: function (hidden) {},

  setSeed: function (seed) {},
  setFridge: function (partial) {},
  setResident: function (id, partial) {},
  setTimeRemaining: function (seconds) {},
  forceNoise: function (event) {},
  getLevel: function () {}
};
```

### 30.2 Method behavior

| Method | Behavior |
|---|---|
| `boot()` | Initializes game. Called automatically by `main.js`. |
| `reset()` | Resets to start state. |
| `start()` | Starts playing from start state. |
| `restart()` | Resets and starts playing. |
| `pause()` | Pauses if playing. |
| `resume()` | Resumes if paused. |
| `tick()` | Advances one fixed tick if playing. |
| `advanceTicks(n)` | Advances `n` ticks. |
| `getState()` | Returns serializable state. |
| `getNoiseEvents(sinceTick)` | Returns noise events with `tick >= sinceTick`. |
| `getAudioEvents(sinceTick)` | Returns audio events with `tick >= sinceTick`. |
| `clearEvents()` | Clears noise and audio event buffers. |
| `setHeld(codes)` | Sets held keys. |
| `clearHeld()` | Releases all held keys. |
| `tap(code)` | Simulates an edge key press. |
| `simulateVisibility(hidden)` | Simulates tab visibility change. |
| `setSeed(seed)` | Sets deterministic PRNG seed. |
| `setFridge(partial)` | Overrides fridge fields for tests. |
| `setResident(id, partial)` | Overrides resident fields for tests. |
| `setTimeRemaining(seconds)` | Sets timer for tests. |
| `forceNoise(event)` | Emits a noise event through the normal noise system. |
| `getLevel()` | Returns compiled level data. |

### 30.3 `setFridge` allowed fields

```js
{
  x,
  y,
  angle,
  plugged,
  power,
  doorOpen,
  slideCooldown,
  humCooldown,
  clearSlide
}
```

If `clearSlide` is true:

```text
slide.active = false
slide.remaining = 0
```

### 30.4 `setResident` allowed fields

```js
{
  active,
  x,
  y,
  angle,
  state,
  suspicion,
  target
}
```

### 30.5 `forceNoise` shape

```js
{
  x: number,
  y: number,
  radius: number,
  alert: number,
  type: "force"
}
```

### Why

Tests need to validate systems without waiting through long gameplay sequences. The API is also useful for QA.

---

## 31. Event Buffers

Noise and audio events should be stored in bounded buffers.

Recommended limits:

```text
maxNoiseEvents = 4096
maxAudioEvents = 4096
```

When the buffer is full, drop oldest events.

Stats counters must not be dropped.

### Why

Long sessions could otherwise grow unbounded arrays. Tests can call `clearEvents()` between cases.

---

## 32. PRNG

Use a deterministic seeded PRNG.

Recommended: mulberry32.

```js
FE.PRNG = {
  seed: function (value) {},
  next: function () {},
  range: function (min, max) {}
};
```

Default seed:

```js
1
```

Tests should call:

```js
__game.setSeed(1);
```

before any test that depends on random dwell times.

### Why

Resident dwell times are random. Tests must be deterministic.

---

## 33. Test Harness

The test harness is a tiny custom runner inside `test/test.js`.

No external test framework.

### 33.1 `test/test.html`

Must:

1. Set `window.FE_TEST_MODE = true`
2. Load all game scripts in the same order as `index.html`
3. Load `test/test.js`

Example:

```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Fridge Escape Tests</title>
  <link rel="stylesheet" href="../css/game.css" />
</head>
<body>
  <script>window.FE_TEST_MODE = true;</script>

  <script src="../js/constants.js"></script>
  <script src="../js/math.js"></script>
  <script src="../js/prng.js"></script>
  <script src="../js/level-data.js"></script>
  <script src="../js/level.js"></script>
  <script src="../js/collision.js"></script>
  <script src="../js/pathfinding.js"></script>
  <script src="../js/noise.js"></script>
  <script src="../js/fridge.js"></script>
  <script src="../js/resident.js"></script>
  <script src="../js/input.js"></script>
  <script src="../js/audio.js"></script>
  <script src="../js/hud.js"></script>
  <script src="../js/render.js"></script>
  <script src="../js/game.js"></script>
  <script src="../js/debug.js"></script>
  <script src="../js/main.js"></script>

  <script src="test.js"></script>
</body>
</html>
```

### 33.2 Test result object

`test/test.js` must set:

```js
window.__testResults = {
  total: number,
  passed: number,
  failed: number,
  failures: [
    {
      name: string,
      message: string
    }
  ]
};
```

It should also set:

```js
window.__testsDone = true;
```

and log:

```js
console.log(JSON.stringify(window.__testResults));
```

### 33.3 Harness requirements

The harness must provide:

```js
test(name, fn)
assert(condition, message)
assertClose(actual, expected, epsilon, message)
ticks(seconds)
advance(seconds)
waitUntil(predicate, maxSeconds)
resetGame()
startGame()
```

Behavior:

- `ticks(seconds)` returns `Math.round(seconds * 120)`
- `advance(seconds)` calls `__game.advanceTicks(ticks(seconds))`
- `waitUntil` advances one tick at a time until predicate is true or timeout
- `resetGame()` calls:
  - `__game.reset()`
  - `__game.clearHeld()`
  - `__game.clearEvents()`
  - `__game.setSeed(1)`
- `startGame()` calls `__game.start()`

### Why

This gives enough test capability without a test runner.

---

## 34. Required Tests

The following tests are required. They should prove the game is finished and playable.

### 34.1 Boot and State

#### Test: boot state

Pass if:

- `window.__game.ready` is true
- `getState().state` is `"start"`
- fridge is at start position
- fridge is plugged
- power is `100`
- time remaining is `120`
- all residents are inactive

---

#### Test: start game

Pass if:

- after `start()`, state is `"playing"`
- after advancing `1` second, `timeRemaining` is approximately `119`
- tick is `120`

---

#### Test: pause and resume

Pass if:

- start game
- advance `5` seconds
- pause
- advance `5` seconds
- state is still `"paused"`
- time remaining unchanged during paused advance
- resume
- advance `1` second
- time remaining decreases by approximately `1`

---

#### Test: hidden tab pauses game

Pass if:

- start game
- advance `5` seconds
- `simulateVisibility(true)`
- state is `"paused"`
- advance `5` seconds
- time remaining unchanged
- `simulateVisibility(false)`
- state remains `"paused"` until `resume()`

---

### 34.2 Level and Navgrid

#### Test: level validation passes

Pass if:

- `FE.Level.validate(FE.levelData)` does not throw
- compiled level has navgrid `64 x 36`

---

#### Test: win zone reachable

Pass if:

- A* path exists from fridge start to win zone center
- path length is greater than `0`

---

#### Test: room modifiers

Pass if:

- kitchen to kitchen is `1.0`
- kitchen to hallway is `0.5`
- hallway to living is `0.5`
- kitchen to living is `0.0`

---

### 34.3 Fridge Movement

#### Test: unplug

Pass if:

- start game
- tap `KeyP`
- fridge `plugged` is false
- a noise event of type `unplug` is recorded
- audio hook `unplug` is recorded
- after advancing `1` second, power is approximately `99`

---

#### Test: waddle forward

Pass if:

- start game
- unplug
- set held `KeyW`
- advance `1` second
- fridge x increased
- speed is at most `50`
- power decreased more than passive-only drain

Expected approximate power after 1 second while moving:

```text
100 - 1 - 3 = 96
```

Allow epsilon `0.2`.

---

#### Test: waddle backward

Pass if:

- start game
- unplug
- set held `KeyS`
- advance `1` second
- fridge x decreased

---

#### Test: rotation

Pass if:

- start game
- unplug
- set held `KeyD`
- advance `1` second
- angle increased by approximately `100` degrees
- power includes rotate drain

Expected approximate power after 1 second while rotating but not moving:

```text
100 - 1 - 1.5 = 97.5
```

Allow epsilon `0.2`.

---

#### Test: plugged fridge cannot move

Pass if:

- start game
- do not unplug
- set held `KeyW`
- advance `1` second
- fridge position unchanged
- power remains `100`

---

#### Test: collision stops movement

Pass if:

- set fridge near a wall
- unplug
- slide or waddle into wall
- fridge does not end inside wall
- if impact speed > 30, collision noise is emitted

---

### 34.4 Slide

#### Test: slide success

Pass if:

- start game
- unplug
- power is `100`
- tap `Space`
- slide active for approximately `0.25` seconds
- power becomes `90`
- slide cooldown is `0.6`
- noise event type `slide` is recorded
- audio hook `slide` is recorded

---

#### Test: slide cooldown

Pass if:

- after successful slide, immediately tapping `Space` does not start another slide
- after advancing `0.6` seconds, slide can start again if power allows

---

#### Test: slide requires power

Pass if:

- set fridge power to `9`
- unplug
- tap `Space`
- slide does not start
- `fridge.powerFlash` is true

---

#### Test: slide requires unplugged

Pass if:

- start game
- fridge is plugged
- tap `Space`
- slide does not start

---

### 34.5 Plug System

#### Test: plug attempt success

Pass if:

- set fridge near kitchen outlet
- set fridge unplugged
- tap `KeyP`
- plug attempt active
- advance `0.5` seconds
- fridge is plugged
- power begins recharging

---

#### Test: plug attempt interrupted by movement

Pass if:

- set fridge near outlet
- set fridge unplugged
- tap `KeyP`
- set held `KeyW`
- advance `1` tick
- plug attempt is inactive
- fridge is still unplugged

---

#### Test: plug attempt canceled by P

Pass if:

- set fridge near outlet
- set fridge unplugged
- tap `KeyP`
- tap `KeyP` again
- plug attempt is inactive
- fridge is still unplugged

---

#### Test: no outlet nearby

Pass if:

- set fridge far from outlets
- set fridge unplugged
- tap `KeyP`
- plug attempt is inactive
- no plug noise event is emitted

---

#### Test: recharge

Pass if:

- set fridge plugged
- set power to `50`
- advance `1` second
- power is approximately `65`

---

### 34.6 Door and Hum

#### Test: door toggle

Pass if:

- start game
- tap `KeyE`
- doorOpen is true
- door noise event emitted
- audio hook `door_open` recorded
- tap `KeyE`
- doorOpen is false
- audio hook `door_close` recorded

---

#### Test: door open drain

Pass if:

- unplug
- open door
- advance `1` second
- power includes `+0.5/sec` drain

Expected approximate power after 1 second stationary with door open:

```text
100 - 1 - 0.5 = 98.5
```

Allow epsilon `0.2`.

---

#### Test: hum requires door

Pass if:

- unplug
- door closed
- tap `KeyQ`
- hum does not occur
- no hum noise event

---

#### Test: hum success

Pass if:

- unplug
- open door
- power `100`
- tap `KeyQ`
- power becomes `85`
- hum cooldown is `3`
- noise event type `hum` with radius `160` and alert `100` is recorded
- audio hook `hum` recorded

---

#### Test: hum cooldown

Pass if:

- after successful hum, tapping `KeyQ` again does not hum
- after advancing `3` seconds, hum can occur again if door open and power sufficient

---

#### Test: hum requires power

Pass if:

- set power to `14`
- unplug
- open door
- tap `KeyQ`
- hum does not occur
- `powerFlash` is true

---

### 34.7 Noise System

#### Test: same room hearing

Pass if:

- create resident in kitchen
- force noise in kitchen within radius
- resident hears noise
- suspicion is at least alert value
- `lastKnown` equals noise position

---

#### Test: adjacent room hearing reduced

Pass if:

- create resident in hallway
- force noise in kitchen with radius `100`
- effective radius is `50`
- resident at distance `40` hears
- resident at distance `60` does not hear

---

#### Test: non-adjacent room no hearing

Pass if:

- create resident in living room
- force noise in kitchen with radius `200`
- resident does not hear

---

#### Test: loud noise triggers investigate

Pass if:

- create resident in routine
- force noise with alert `60`
- resident state becomes `investigate`
- target equals noise position
- `stats.residentsLured` includes resident id

---

#### Test: quiet noise triggers suspicious

Pass if:

- create resident in routine
- force noise with alert `20`
- resident state becomes `suspicious`
- suspicion is at least `20`
- resident is not counted as lured

---

### 34.8 Resident Spawn

#### Test: mom spawns at 5 seconds

Pass if:

- start game
- advance `4.9` seconds
- mom inactive
- advance `0.2` seconds
- mom active

---

#### Test: dad spawns at 10 seconds

Pass if:

- start game
- advance `9.9` seconds
- dad inactive
- advance `0.2` seconds
- dad active

---

#### Test: kid spawns at 20 seconds

Pass if:

- start game
- advance `19.9` seconds
- kid inactive
- advance `0.2` seconds
- kid active

---

### 34.9 Resident Perception

#### Test: normal fridge in kitchen not suspicious

Pass if:

- resident in kitchen
- fridge plugged, stationary, door closed, in kitchen
- advance `1` second
- resident suspicion remains `0`

---

#### Test: unplugged fridge in kitchen raises suspicion

Pass if:

- resident sees fridge
- fridge unplugged and stationary in kitchen
- advance `1` second
- suspicion increased by approximately `40`

Expected:

```text
base 20 + unplugged 20 = 40
```

Allow epsilon `1`.

---

#### Test: moving unplugged hallway fridge raises suspicion faster

Pass if:

- resident sees fridge
- fridge unplugged, moving, hallway
- advance `1` second
- suspicion increased by approximately `70`

Expected:

```text
base 20 + moving 20 + unplugged 20 + not kitchen 10 = 70
```

Allow epsilon `1`.

---

#### Test: line of sight blocks suspicion

Pass if:

- place obstacle between resident and fridge
- fridge is abnormal
- advance `1` second
- suspicion does not increase from sight

---

### 34.10 Resident AI

#### Test: suspicious decays

Pass if:

- set resident suspicious with suspicion `50`
- make fridge not visible/abnormal
- advance `1.5` seconds
- resident returns to routine
- suspicion is `0`

---

#### Test: investigate moves to target

Pass if:

- set resident investigate with target far away
- advance enough ticks
- resident position moves toward target
- after reaching target, resident enters search

---

#### Test: search returns to routine

Pass if:

- set resident search
- advance `3` seconds
- resident state is routine
- suspicion is `0`

---

#### Test: catch triggers lose

Pass if:

- start game
- set active resident within `40` units of fridge
- advance `1` tick
- state is `lose`
- lose reason is `caught`

---

### 34.11 Pathfinding

#### Test: resident path avoids obstacle

Pass if:

- set resident and target on opposite sides of an obstacle
- path exists
- path does not pass through blocked cells

---

#### Test: no path stops resident

Pass if:

- set fridge blocking the only route
- set resident investigate target across route
- advance enough ticks
- resident `hasPath` is false
- resident stops
- game does not crash

---

### 34.12 Win and Lose

#### Test: win at front door

Pass if:

- start game
- set fridge in win zone
- advance `1` tick
- state is `win`
- stats include time used, noise events, residents lured

---

#### Test: win priority over catch

Pass if:

- set fridge in win zone
- set resident within `40`
- advance `1` tick
- state is `win`

---

#### Test: power lose

Pass if:

- start game
- set fridge power to `0`
- advance `1` tick
- state is `lose`
- lose reason is `power`

---

#### Test: timer lose

Pass if:

- start game
- set time remaining to `0`
- advance `1` tick
- state is `lose`
- lose reason is `timer`

---

#### Test: power priority over timer

Pass if:

- set fridge power to `0`
- set time remaining to `0`
- advance `1` tick
- state is `lose`
- lose reason is `power`

---

### 34.13 HUD

#### Test: objective updates by room

Pass if:

- kitchen unplugged -> “Leave the kitchen.”
- hallway -> “Cross the hallway.”
- living room -> “Reach the front door.”

---

#### Test: timer warning

Pass if:

- set time remaining to `31`
- advance `1` second
- `hud.timerWarning` is true
- audio hook `timer_warning` recorded once

---

#### Test: power warning

Pass if:

- set power to `26`
- unplug
- advance enough to drop below `25`
- `hud.powerWarning` is true
- audio hook `power_warning` recorded once

---

### 34.14 Stats

#### Test: noise event count

Pass if:

- start game
- unplug
- open door
- hum
- `stats.noiseEvents` is at least `3`

---

#### Test: residents lured unique count

Pass if:

- force loud noise heard by mom and dad
- `stats.residentsLured` is `2`
- `stats.luredIds` contains both ids
- forcing another loud noise heard by mom does not increase count

---

### 34.15 Determinism

#### Test: same inputs produce same state

Pass if:

- reset, start, set seed
- run same input sequence for `10` seconds
- record state hash
- reset, start, set same seed
- run same input sequence
- state hash matches

Input sequence example:

```text
tap P
hold W for 2 seconds
release W
hold D for 1 second
release D
tap Space
hold W for 3 seconds
release W
```

Use a simple hash of `JSON.stringify(getState())` with floating values rounded to 3 decimals.

### Why determinism test

It proves the simulation is testable and not dependent on hidden real-time behavior.

---

## 35. Test Harness Implementation Sketch

This is not necessarily final code, but the required behavior.

```js
window.__testResults = {
  total: 0,
  passed: 0,
  failed: 0,
  failures: []
};

var tests = [];

function test(name, fn) {
  tests.push({ name: name, fn: fn });
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message || "assertion failed");
  }
}

function assertClose(actual, expected, epsilon, message) {
  var ok = Math.abs(actual - expected) <= (epsilon === undefined ? 0.01 : epsilon);
  if (!ok) {
    throw new Error(
      (message || "assertClose failed") +
      " expected " + expected +
      " got " + actual
    );
  }
}

function ticks(seconds) {
  return Math.round(seconds * 120);
}

function advance(seconds) {
  window.__game.advanceTicks(ticks(seconds));
}

function waitUntil(predicate, maxSeconds) {
  var max = ticks(maxSeconds || 10);
  for (var i = 0; i < max; i++) {
    window.__game.advanceTicks(1);
    if (predicate()) return true;
  }
  return false;
}

function resetGame() {
  window.__game.reset();
  window.__game.clearHeld();
  window.__game.clearEvents();
  window.__game.setSeed(1);
}

function startGame() {
  window.__game.start();
}

function runTests() {
  for (var i = 0; i < tests.length; i++) {
    var t = tests[i];
    window.__testResults.total++;
    try {
      t.fn();
      window.__testResults.passed++;
    } catch (err) {
      window.__testResults.failed++;
      window.__testResults.failures.push({
        name: t.name,
        message: err.message
      });
    }
  }

  window.__testsDone = true;
  console.log(JSON.stringify(window.__testResults));
}
```

Tests should call `resetGame()` and `startGame()` as needed.

---

## 36. Acceptance Criteria

The game is considered engineering-complete when all of the following are true:

1. `index.html` loads without syntax errors.
2. `test/test.html` loads without syntax errors.
3. `window.__game` exists after load.
4. `window.__testResults.failed` is `0`.
5. All required tests in section 34 pass.
6. The level validator passes.
7. The win zone is reachable.
8. The player can:
   - start the game
   - unplug
   - waddle
   - rotate
   - slide
   - plug in
   - open/close door
   - hum
   - pause/resume
   - lose by catch, power, or timer
   - win at front door
   - restart
9. Hidden tab pauses the game in production mode.
10. Audio hooks fire even if no audio assets are present.
11. No external libraries are required.
12. No build step is required.

---

## 37. Manual QA Script

A human or QA agent should also verify:

1. Open `index.html`.
2. Click Play.
3. Press `P` to unplug.
4. Press `W` to waddle.
5. Press `A` and `D` to rotate.
6. Press `Space` to slide.
7. Press `E` to open door.
8. Press `Q` to hum.
9. Move near an outlet and press `P` to plug.
10. Wait to observe recharge.
11. Press `P` to unplug.
12. Press `Escape` to pause.
13. Press `Escape` to resume.
14. Let a resident catch the fridge or let timer expire.
15. Retry.
16. Reach the front door and verify win screen.

---

## 38. Integration Notes for Other Agents

### For the gameplay designer

- Level content lives in `js/level-data.js`.
- Do not assume a procedural generator.
- If changing level geometry, the level validator may fail.
- If changing resident waypoints, ensure they are walkable.
- If changing outlets, ensure they are within `48`-unit reach of intended paths.

### For the visual designer

- Canvas rendering is in `js/render.js`.
- HUD styling is in `css/game.css`.
- Use the DOM ids defined in section 25.
- Do not change `window.__game` state shape.
- Placeholder visuals are acceptable until final art is integrated.

### For the audio designer

- Provide audio assets through `window.FE.audioAssets`.
- Use the hook names in section 27.
- Tests do not require actual audio files.
- If assets are missing, the game must remain playable silently.

---

## 39. Final Engineering Intent

The implementation should feel like a small, deterministic, data-driven stealth game.

The important engineering properties are:

- fixed tick simulation
- serializable state
- debug API for headless tests
- level compiler and validation
- simple A* pathfinding
- event-based noise
- clear win/lose priority
- no external dependencies
- minimal but complete test harness

If a feature is not required by gameplay, audio hooks, HUD, win/lose conditions, or tests, cut it.