# engineering.md

## 0. Purpose and scope

This document is the engineering specification for **Cat: Mice Hunt**.

It defines:

- The files that must exist.
- The runtime architecture.
- The data shapes.
- The game loop and update order.
- The exact gameplay systems required by `gameplay.md`.
- The level data that must be implemented.
- The debug API exposed on `window.__game`.
- The lightweight browser test harness exposed on `window.__test`.
- The required tests that prove the game is complete, playable, and stable.

The implementation must be **vanilla HTML, CSS, and JavaScript only**.

There is:

- No Node.js.
- No npm.
- No bundler.
- No build step.
- No test runner.
- No external runtime library.
- No physics engine.
- No pathfinding library.

The only external validation available is:

1. A syntax check of the JavaScript files.
2. A headless browser page that loads the game and drives it through `window.__game`.
3. A browser-side test harness that records pass/fail results on `window.__testResults`.

All gameplay values from `gameplay.md` are requirements unless this document explicitly documents an engineering conflict and provides a minimal correction.

---

## 1. Major engineering decisions

### 1.1 Classic scripts, not ES modules

Use classic `<script>` tags in dependency order.

Reasons:

- No build step.
- Works from `file://` in more environments.
- Easier for a syntax-only check.
- Simpler for a headless integration agent.
- Avoids module loading edge cases.

All code should attach to a single global namespace:

```js
window.Game = window.Game || {};
```

Allowed globals:

```js
window.Game
window.__game
window.__test
window.__testResults
```

No other globals should be created.

---

### 1.2 Canvas for gameplay, DOM for HUD and menus

Use:

- A `<canvas>` for the arena, cat, mice, holes, and obstacles.
- DOM elements for menus, HUD, overlays, buttons, and center messages.

Reasons:

- Canvas is the right tool for 2D top-down entities.
- DOM is easier for accessible buttons and visual designer styling.
- The game state remains in JavaScript, so tests do not need to scrape pixels.
- The visual designer can style the DOM without touching gameplay logic.

The canvas coordinate system is always:

```text
960 x 540
```

CSS may scale the canvas visually, but the logical coordinate system must remain `960 x 540`.

---

### 1.3 Fixed timestep

Use a fixed simulation timestep:

```js
const FIXED_DT = 1 / 60;
```

Use a maximum real-frame delta:

```js
const MAX_FRAME_DT = 1 / 30;
```

Reasons:

- `gameplay.md` requires clamped delta time.
- Fixed steps make tests deterministic.
- It prevents physics and AI instability after tab suspension.
- It allows `window.__game.step(seconds)` to advance the game in exact fixed increments.

The production loop uses an accumulator:

```js
accumulator += realDt;
while (accumulator >= FIXED_DT) {
  update(FIXED_DT);
  accumulator -= FIXED_DT;
}
```

`realDt` is clamped to `MAX_FRAME_DT`.

---

### 1.4 Debug-driven testing

Because there is no test runner, the game must expose a rich debug API on:

```js
window.__game
```

Tests must be able to:

- Start campaign or endless mode.
- Start specific levels or waves.
- Step time manually.
- Set cat position and velocity.
- Force pounce.
- Force mouse spawn.
- Force catch.
- Force escape.
- Set mouse timers.
- Set hole occupancy/blocking.
- Set score, lives, combo, caught count.
- Read full serializable state.
- Validate level data.
- Disable audio.
- Seed the RNG.

This is required so tests can validate gameplay without relying on wall-clock time, user input, rendering, or audio.

---

### 1.5 Deterministic RNG

The game must use a seeded RNG for all gameplay randomness.

Default runtime seed:

```js
Date.now()
```

Test seed:

```js
1337
```

The RNG must be replaceable through:

```js
window.__game.setSeed(seed)
```

Use a small deterministic PRNG such as `mulberry32`.

No gameplay logic may call `Math.random()` directly.

---

### 1.6 Level 2 conflict correction

`gameplay.md` states that the cat start position is always:

```text
480, 270
```

Level 2 has an obstacle:

```text
400, 230, 160, 80
```

That rectangle contains `(480, 270)`.

This is an internal conflict in the provided level data.

Engineering correction:

- On level load, attempt to place the cat at `(480, 270)`.
- If the cat circle collides with an obstacle, resolve the collision using the same circle-vs-AABB resolution used during gameplay.
- If the cat is fully inside an obstacle, push it out along the smallest axis overlap.
- If a tie occurs, push upward first.
- If still invalid, try deterministic offsets:

```text
(0, -80)
(0, +80)
(+80, 0)
(-80, 0)
```

For Level 2, this produces a valid cat start at approximately:

```text
480, 212
```

This is the only layout correction. No other level data is changed.

Level validation must validate the **post-correction** cat start position.

---

## 2. Required files

The project must contain at least these files:

```text
index.html
css/style.css
audio/ui_click.ogg
audio/pounce.ogg
audio/catch.ogg
audio/multi_catch.ogg
audio/startle.ogg
audio/escape.ogg
audio/level_complete.ogg
audio/campaign_complete.ogg
audio/game_over.ogg
audio/endless_wave_complete.ogg
audio/endless_game_over.ogg
js/config.js
js/utils.js
js/rng.js
js/save.js
js/input.js
js/audio.js
js/levels.js
js/collision.js
js/entities.js
js/game.js
js/ui.js
js/render.js
js/main.js
js/debug.js
js/test-harness.js
js/tests.js
```

Audio files may be missing in early integration. The audio system must not crash if files are missing.

The game must be fully playable with fallback vector graphics if no visual assets are present.

---

## 3. File responsibilities

### `index.html`

- Loads CSS.
- Creates the canvas and DOM UI containers.
- Loads all JavaScript files in dependency order.
- Starts the game.
- If `?test=1` is present, disables auto-step, disables audio, seeds the RNG, and runs tests.

Required script order:

```html
<script src="js/config.js"></script>
<script src="js/utils.js"></script>
<script src="js/rng.js"></script>
<script src="js/save.js"></script>
<script src="js/input.js"></script>
<script src="js/audio.js"></script>
<script src="js/levels.js"></script>
<script src="js/collision.js"></script>
<script src="js/entities.js"></script>
<script src="js/game.js"></script>
<script src="js/ui.js"></script>
<script src="js/render.js"></script>
<script src="js/debug.js"></script>
<script src="js/main.js"></script>
<script src="js/test-harness.js"></script>
<script src="js/tests.js"></script>
```

At the end of `index.html`, include:

```html
<script>
  if (new URLSearchParams(location.search).has("test")) {
    window.__game.setAutoStep(false);
    window.__game.setAudioEnabled(false);
    window.__game.setSeed(1337);
    window.__test.run().then(function (results) {
      window.__testResults = results;
      console.log("[TESTS]", JSON.stringify(results, null, 2));
    });
  }
</script>
```

---

### `css/style.css`

Responsible for:

- Centering the game.
- Scaling the canvas while preserving aspect ratio.
- Styling HUD.
- Styling menus and overlays.
- Styling progress bars.
- Styling life icons.
- Styling center messages.

The CSS must not affect gameplay coordinates.

The logical game area is always `960 x 540`.

---

### `js/config.js`

Contains all tunable constants.

Required config shape:

```js
window.Game.config = {
  ARENA: { width: 960, height: 540 },
  FIXED_DT: 1 / 60,
  MAX_FRAME_DT: 1 / 30,

  CAT: {
    radius: 18,
    maxSpeed: 260,
    acceleration: 2200,
    friction: 1200,
    pounceSpeed: 520,
    pounceDuration: 0.18,
    pounceCooldown: 0.8,
    pounceBuffer: 0.1
  },

  MOUSE: {
    acceleration: 1800,
    emergeDuration: 0.25,
    enterDuration: 0.3,
    escapeTime: 2.5,
    startleDuration: 0.3,
    startleSpeedMultiplier: 1.3,
    fleeDistance: 140,
    separationDistance: 28,
    separationWeight: 0.5,
    wanderMinInterval: 0.3,
    wanderMaxInterval: 0.6,
    wanderMaxTurn: Math.PI / 4,
    obstacleLookahead: 20,
    stuckSpeedThreshold: 1,
    stuckTimerLimit: 1.0
  },

  HOLE: {
    radius: 24,
    occupyDuration: 0.8,
    blockDistance: 40
  },

  COMBO: {
    window: 3.0,
    step: 0.25,
    maxMultiplier: 3.0
  },

  SCORE: {
    catchBase: 100,
    pounceBonus: 50,
    fastCatchBonus: 50,
    fastCatchTime: 1.0,
    multiCatchBonusPerExtra: 100,
    levelLifeBonus: 500,
    levelPerfectBonus: 1000,
    endlessWaveNumberBonus: 500,
    endlessLifeBonus: 250,
    endlessPerfectBonus: 1000
  },

  SPAWN: {
    initialDelay: 1.0
  },

  MESSAGES: {
    minDuration: 1.0,
    maxDuration: 1.5
  },

  AUTO_ADVANCE: {
    levelComplete: 3.0,
    endlessWaveComplete: 3.0
  },

  LEVEL_INTRO_DURATION: 1.5,

  LIVES: 3
};
```

Mouse type config:

```js
window.Game.config.MICE = {
  normal: { speed: 180, radius: 14 },
  fast:   { speed: 220, radius: 12 },
  big:    { speed: 150, radius: 20 }
};
```

---

### `js/utils.js`

Provides pure helper functions.

Required utilities:

```js
clamp(value, min, max)
clampVectorLength(vector, max)
normalize(vector)
length(vector)
dot(a, b)
rotateVector(vector, radians)
moveToward(current, target, delta)
lerp(a, b, t)
distance(a, b)
sub(a, b)
add(a, b)
scale(vector, scalar)
deepCopy(value)
```

Vector shape:

```js
{ x: number, y: number }
```

`normalize` must return `{ x: 0, y: 0 }` for zero-length vectors.

`clampVectorLength` must preserve direction and clamp magnitude.

---

### `js/rng.js`

Provides deterministic RNG.

Required API:

```js
window.Game.RNG = {
  create(seed),
  pickWeighted(weights, rng)
};
```

`create(seed)` returns:

```js
{
  next(),
  range(min, max),
  int(min, max),
  angle()
}
```

`pickWeighted(weights, rng)` accepts:

```js
{
  normal: 50,
  fast: 30,
  big: 20
}
```

and returns one of the keys.

If total weight is zero, return `null`.

---

### `js/save.js`

Handles persistence.

Save key:

```js
"cat_mice_hunt_save_v1"
```

Default save:

```js
{
  endless_unlocked: false,
  campaign_high_score: 0,
  endless_high_score: 0,
  endless_best_wave: 0,
  total_plays: 0
}
```

Required API:

```js
window.Game.Save = {
  load(),
  save(data),
  reset()
};
```

Rules:

- If `localStorage` is unavailable, use an in-memory object.
- If saved data is corrupt, return defaults.
- Missing fields are filled with defaults.
- No mid-level progress is saved.

---

### `js/input.js`

Handles keyboard and mouse input.

Required API:

```js
window.Game.Input = {
  init(canvas),
  destroy(),
  getMovement(),
  consumePouncePress(),
  consumePausePress(),
  reset()
};
```

Movement input:

```js
{ x: -1 | 0 | 1, y: -1 | 0 | 1 }
```

The game normalizes this vector before using it.

Supported keys:

```text
W / ArrowUp
A / ArrowLeft
S / ArrowDown
D / ArrowRight
Space
Left mouse button
Esc
P
```

Rules:

- Prevent default behavior for arrows and Space when the game is focused.
- Ignore `e.repeat` for pounce.
- Left mouse button only triggers pounce when pressed on the canvas.
- Clicking UI buttons must not trigger pounce.
- `Esc` or `P` toggles pause when gameplay is active.
- Browser blur triggers a focus-loss event that the game uses to pause.

---

### `js/audio.js`

Implements audio cue playback.

Required API:

```js
window.Game.Audio = {
  init(),
  setEnabled(enabled),
  isEnabled(),
  unlock(),
  play(cue),
  getLastCue()
};
```

Audio files:

```text
audio/ui_click.ogg
audio/pounce.ogg
audio/catch.ogg
audio/multi_catch.ogg
audio/startle.ogg
audio/escape.ogg
audio/level_complete.ogg
audio/campaign_complete.ogg
audio/game_over.ogg
audio/endless_wave_complete.ogg
audio/endless_game_over.ogg
```

Optional file not required for gameplay:

```text
audio/combo_milestone.ogg
```

Engineering decision: do not trigger a combo milestone sound.

Reason:

- `gameplay.md` lists it as optional.
- Adding arbitrary milestone thresholds would add feel complexity without a gameplay rule.
- The combo HUD already communicates combo state.

Audio rules:

- Each cue has a small pool of 3 `Audio` elements to allow overlap.
- `play(cue)` records `lastCue` even when audio is disabled.
- If audio is disabled, no actual playback occurs.
- If a file is missing, playback failures are silently swallowed.
- Audio unlock occurs on first user gesture:
  - keydown
  - mousedown
  - click

---

### `js/levels.js`

Contains level data and endless wave generation.

Required API:

```js
window.Game.Levels = {
  getLevel(levelNumber),
  getEndlessWave(waveNumber),
  validateLevel(levelNumber),
  validateWave(waveNumber)
};
```

Level data is an array indexed `0..9`, but level numbers are `1..10`.

Level shape:

```js
{
  level: 1,
  target: 5,
  maxActive: 2,
  spawnInterval: 2.0,
  mix: { normal: 100, fast: 0, big: 0 },
  holes: [[120, 420], [840, 420]],
  obstacles: []
}
```

Obstacle shape:

```js
{
  x: number,
  y: number,
  width: number,
  height: number
}
```

Hole shape:

```js
{
  x: number,
  y: number
}
```

Validation returns:

```js
{
  valid: boolean,
  errors: string[]
}
```

Validation checks:

- Level number is `1..10`.
- Target is a positive integer.
- Max active is `1..7`.
- Spawn interval is greater than zero.
- Mouse mix has non-negative weights and total weight greater than zero.
- Hole count is `1..6`.
- Hole positions are inside the arena with at least `24px` margin.
- Obstacle count is `0..3`.
- Obstacles are inside the arena.
- No hole circle intersects an obstacle.
- Cat start position, after correction, is valid.
- Every hole is reachable from the cat start using a coarse BFS reachability check.

Reachability check:

- Use a `20px` grid.
- Mark a cell blocked if its center is outside the arena or collides with an obstacle using a `10px` radius.
- Flood fill from the cat start cell using 4-directional movement.
- Every hole center cell must be reachable.

This validation is for tests and debugging. It is not a runtime gameplay feature.

---

### `js/collision.js`

Provides collision helpers.

Required API:

```js
window.Game.Collision = {
  clampToArena(position, radius),
  circleIntersectsAABB(circle, aabb),
  resolveCircleAABB(circle, aabb),
  resolveEntity(entity, obstacles)
};
```

Circle shape:

```js
{
  x: number,
  y: number,
  radius: number
}
```

AABB shape:

```js
{
  x: number,
  y: number,
  width: number,
  height: number
}
```

Rules:

- Arena bounds clamp position to:

```text
x: [radius, 960 - radius]
y: [radius, 540 - radius]
```

- Circle-vs-AABB uses closest point.
- If the circle center is inside the AABB, push out along the smallest axis overlap.
- If there is a tie, push upward first.
- `resolveEntity` clamps to arena and resolves all obstacles.
- For stability, resolve obstacles twice per frame for each entity.

---

### `js/entities.js`

Contains entity factory functions.

Required API:

```js
window.Game.Entities = {
  createCat(),
  createMouse(type, hole, id),
  createHole(x, y),
  createObstacle(x, y, width, height)
};
```

Cat shape:

```js
{
  x: 480,
  y: 270,
  vx: 0,
  vy: 0,
  radius: 18,
  pounceTimer: 0,
  pounceCooldown: 0,
  pounceBuffer: 0,
  pounceDirection: { x: 1, y: 0 },
  lastDirection: { x: 1, y: 0 }
}
```

Mouse shape:

```js
{
  id: integer,
  type: "normal" | "fast" | "big",
  state: "emerging" | "fleeing" | "entering",
  x: number,
  y: number,
  vx: 0,
  vy: 0,
  radius: number,
  maxSpeed: number,
  outTime: 0,
  emergeTimer: 0.25,
  enterTimer: 0,
  startleTimer: 0,
  holeIndex: -1,
  wanderAngle: number,
  wanderTimer: number,
  stuckTimer: 0,
  pendingEscape: false
}
```

Hole shape:

```js
{
  x: number,
  y: number,
  radius: 24,
  occupiedTimer: 0,
  blocked: false,
  blockedOverride: null
}
```

Obstacle shape:

```js
{
  x: number,
  y: number,
  width: number,
  height: number
}
```

Mouse states in the active list are only:

```text
emerging
fleeing
entering
```

`caught` and `escaped` are event outcomes, not active states.

---

### `js/game.js`

Contains the main game object.

Required API:

```js
window.Game.Game = function () {};
```

The game object owns:

- State.
- Save data.
- RNG.
- Input.
- Audio.
- Level data.
- Entities.
- Timers.
- Score.
- Combo.
- Lives.
- State machine.
- Update loop.

Main methods:

```js
init()
startLoop()
stopLoop()
update(dt)
render()
reset()
startCampaign()
startEndless()
startLevel(levelNumber)
startWave(waveNumber)
next()
retry()
pause()
resume()
restart()
mainMenu()
howToPlay()
back()
simulateFocusLoss()
```

The game must expose its current state through a method used by the debug API:

```js
getState()
```

`getState()` must return a serializable deep copy.

No functions, DOM nodes, audio elements, or canvas contexts may be included in state.

---

### `js/ui.js`

Handles DOM UI.

Required API:

```js
window.Game.UI = {
  init(root),
  show(screen, data),
  updateHUD(state),
  showMessage(text, priority, duration)
};
```

UI screens:

```text
menu
howToPlay
levelIntro
playing
paused
levelComplete
campaignComplete
gameOver
endlessWaveComplete
endlessGameOver
```

The UI reads state from the game and updates DOM.

The UI must not modify gameplay state directly.

UI actions call game methods:

```js
game.startCampaign()
game.startEndless()
game.howToPlay()
game.back()
game.pause()
game.resume()
game.restart()
game.mainMenu()
game.next()
game.retry()
```

All UI button clicks play `ui_click`.

---

### `js/render.js`

Handles canvas rendering.

Required API:

```js
window.Game.Render = {
  init(canvas),
  draw(state)
};
```

Rendering must be purely state-driven.

Draw order:

1. Background.
2. Obstacles.
3. Holes.
4. Mice.
5. Cat.
6. Optional pounce effect.

Fallback visuals are required.

Suggested fallbacks:

- Arena background: neutral color.
- Obstacles: rounded rectangles.
- Holes: dark circles.
- Normal mouse: small gray ellipse.
- Fast mouse: smaller lighter gray ellipse.
- Big mouse: larger brown-gray ellipse.
- Cat: orange circle with ears.
- Pouncing cat: slightly stretched shape.

The visual designer may replace these with sprites, but the render layer must remain state-driven.

---

### `js/main.js`

Bootstraps the game.

Responsibilities:

- Create the game instance.
- Initialize input, audio, UI, render.
- Attach `window.__game` using `GameDebug.create(game)`.
- Start the production loop unless in test mode.
- Handle browser blur focus loss.

Test mode is detected by:

```js
new URLSearchParams(location.search).has("test")
```

In test mode:

- Do not start the production requestAnimationFrame loop.
- Disable audio.
- Seed RNG with `1337`.
- Allow tests to call `window.__game.step()`.

---

### `js/debug.js`

Creates `window.__game`.

Required API:

```js
window.GameDebug = {
  create(game)
};
```

The returned object is assigned to:

```js
window.__game
```

This API is the only interface tests may use to drive the game.

See section 8 for the full API.

---

### `js/test-harness.js`

Provides a minimal browser test harness.

Required API:

```js
window.__test = {
  test(name, fn),
  assert(condition, message),
  assertClose(actual, expected, epsilon, message),
  assertDeepEqual(actual, expected, message),
  getResults(),
  run()
};
```

`run()` returns a Promise that resolves to:

```js
{
  passed: number,
  failed: number,
  total: number,
  failures: [
    {
      name: string,
      message: string,
      stack: string
    }
  ]
}
```

Before each test, the harness should:

```js
window.__game.reset();
window.__game.setAudioEnabled(false);
window.__game.setSeed(1337);
```

This prevents cross-test contamination.

Tests may override save data after reset.

---

### `js/tests.js`

Contains the required tests.

Tests register using:

```js
window.__test.test("name", async function () {
  // assertions
});
```

Tests must use `window.__game` only.

Tests must not use:

- `document`
- `window` except for `__game` and `__test`
- real timers
- `setTimeout`
- `setInterval`
- `requestAnimationFrame`
- user input
- audio playback
- network requests

---

## 4. Required DOM structure

`index.html` must include at least:

```html
<div id="game-root">
  <canvas id="game-canvas" width="960" height="540"></canvas>

  <div id="hud">
    <div id="hud-left">
      <div id="score">Score: 000000</div>
      <div id="combo" hidden>Combo: x1.00</div>
      <div id="level-label">Level 1</div>
    </div>

    <div id="hud-center">
      <div id="caught-label">Caught: 0 / 0</div>
      <div id="progress">
        <div id="progress-fill"></div>
      </div>
    </div>

    <div id="hud-right">
      <div id="lives">
        <span class="life full"></span>
        <span class="life full"></span>
        <span class="life full"></span>
      </div>
      <button id="pause-button" type="button">II</button>
    </div>

    <div id="pounce-wrap">
      <div id="pounce-label">Pounce</div>
      <div id="pounce-bar">
        <div id="pounce-fill"></div>
      </div>
    </div>

    <div id="center-message" hidden></div>
  </div>

  <div id="overlay">
    <div id="screen-menu" class="screen">
      <h1>Cat: Mice Hunt</h1>
      <button id="btn-play" type="button">Play</button>
      <button id="btn-endless" type="button" hidden>Endless</button>
      <button id="btn-how" type="button">How to Play</button>
    </div>

    <div id="screen-how" class="screen" hidden>
      <h2>How to Play</h2>
      <div id="how-content"></div>
      <button id="btn-back" type="button">Back</button>
    </div>

    <div id="screen-intro" class="screen" hidden>
      <h2 id="intro-title"></h2>
      <p id="intro-objective"></p>
      <p id="intro-lives"></p>
      <p id="intro-new-type" hidden></p>
    </div>

    <div id="screen-pause" class="screen" hidden>
      <h2>Paused</h2>
      <button id="btn-resume" type="button">Resume</button>
      <button id="btn-restart" type="button">Restart</button>
      <button id="btn-menu-from-pause" type="button">Main Menu</button>
    </div>

    <div id="screen-level-complete" class="screen" hidden>
      <h2 id="complete-title"></h2>
      <p id="complete-score"></p>
      <p id="complete-bonus"></p>
      <p id="complete-high"></p>
      <button id="btn-next" type="button">Next Level</button>
    </div>

    <div id="screen-campaign-complete" class="screen" hidden>
      <h2>Campaign Complete</h2>
      <p id="campaign-score"></p>
      <p id="campaign-high"></p>
      <button id="btn-play-endless" type="button">Play Endless</button>
      <button id="btn-menu-from-campaign" type="button">Main Menu</button>
    </div>

    <div id="screen-game-over" class="screen" hidden>
      <h2>Game Over</h2>
      <p id="gameover-context"></p>
      <p id="gameover-score"></p>
      <button id="btn-retry" type="button">Retry</button>
      <button id="btn-menu-from-gameover" type="button">Main Menu</button>
    </div>

    <div id="screen-endless-wave-complete" class="screen" hidden>
      <h2 id="wave-complete-title"></h2>
      <p id="wave-complete-score"></p>
      <p id="wave-complete-bonus"></p>
      <p id="wave-complete-countdown"></p>
    </div>
  </div>
</div>
```

The visual designer may restyle these elements, but the IDs should remain stable because UI logic depends on them.

---

## 5. State machine

The game uses a screen-based state machine.

Screens:

```text
menu
howToPlay
levelIntro
playing
paused
levelComplete
campaignComplete
gameOver
endlessWaveComplete
endlessGameOver
```

Mode:

```text
null
campaign
endless
```

### 5.1 Menu

Initial screen.

State:

```js
screen = "menu"
mode = null
level = null
wave = null
score = 0
```

Buttons:

- Play: starts campaign level 1 with score 0.
- Endless: starts endless wave 1 with score 0, only if unlocked.
- How to Play: shows how-to-play screen.

---

### 5.2 How to Play

State:

```js
screen = "howToPlay"
```

Content:

```text
Move: WASD or Arrow Keys
Pounce: Space or Left Click

Catch mice before they hide.
Mice can hide in holes after 2.5 seconds.
Pounce to catch Big mice.
Catch mice quickly to build combo.
Do not let 3 mice escape.

Normal: Standard mouse.
Fast: Faster, smaller mouse.
Big: Can only be caught while pouncing.
```

Back returns to menu.

---

### 5.3 Level Intro

Used for campaign levels only.

Duration:

```text
1.5 seconds
```

State:

```js
screen = "levelIntro"
mode = "campaign"
level = 1..10
wave = null
```

Behavior:

- Cat is controllable.
- No mice exist.
- No spawning.
- Intro timer counts down.
- When timer reaches zero:
  - Screen becomes `playing`.
  - `spawnTimer` becomes `1.0`.
  - Center message shows level objective if needed.

Level intro displays:

```text
Level X
Catch Y mice
3 lives
New mouse type: Fast   // Level 3
New mouse type: Big    // Level 4
```

---

### 5.4 Playing

Main gameplay screen.

State:

```js
screen = "playing"
mode = "campaign" | "endless"
```

Behavior:

- Cat updates.
- Mice update.
- Spawning occurs.
- Catching occurs.
- Escaping occurs.
- HUD updates.
- Combo timer updates.
- Messages update.

---

### 5.5 Paused

Pause can occur from:

```text
levelIntro
playing
levelComplete
endlessWaveComplete
```

State:

```js
screen = "paused"
pausedFrom = previous screen
```

Behavior:

- All gameplay timers stop.
- No movement.
- No spawning.
- No score changes.
- No life changes.
- No auto-advance.

Pause triggers:

- `Esc`
- `P`
- Browser loses focus
- Pause button

Resume returns to `pausedFrom`.

Restart restarts current level or wave using `scoreAtStart`.

Main Menu clears the active run.

---

### 5.6 Level Complete

Triggered when:

```js
caught >= target
```

in campaign mode.

State:

```js
screen = "levelComplete"
```

Behavior:

- Gameplay stops.
- Level complete bonus is added.
- High score is updated.
- Save is written.
- After 3 seconds, automatically advance.
- Player can click Next immediately.

If level 10 is complete:

- Go to `campaignComplete`.
- Unlock endless mode.

---

### 5.7 Campaign Complete

State:

```js
screen = "campaignComplete"
mode = "campaign"
level = 10
```

Behavior:

- Save `endless_unlocked = true`.
- Save campaign high score.
- Buttons:
  - Play Endless
  - Main Menu

---

### 5.8 Game Over

Triggered when:

```js
lives <= 0
```

and target was not reached.

State:

```js
screen = "gameOver"
```

Behavior:

- Save high score.
- Buttons:
  - Retry
  - Main Menu

Retry:

- Restarts same level or wave.
- Resets lives to 3.
- Resets score to `scoreAtStart`.
- Resets combo.
- Resets caught count.
- Resets escapes in run.
- Resets entities.

---

### 5.9 Endless Wave Complete

Triggered when:

```js
caught >= target
```

in endless mode.

State:

```js
screen = "endlessWaveComplete"
```

Behavior:

- Wave bonus added.
- Endless high score updated.
- `endless_best_wave` updated.
- Save written.
- After 3 seconds, automatically start next wave.
- Score carries forward.
- Lives reset next wave.
- Combo resets next wave.

---

### 5.10 Endless Game Over

Triggered when:

```js
lives <= 0
```

in endless mode.

State:

```js
screen = "endlessGameOver"
```

Behavior:

- Save endless high score.
- Buttons:
  - Retry Wave
  - Main Menu

Retry wave:

- Restarts same wave.
- Resets lives to 3.
- Resets score to `scoreAtStart`.
- Resets combo.
- Resets caught count.
- Resets escapes in wave.
- Resets entities.

---

## 6. Core state shape

`window.__game.getState()` must return a serializable object shaped like:

```js
{
  version: 1,
  screen: "menu",
  mode: null,
  level: null,
  wave: null,
  layoutLevel: null,

  score: 0,
  highScore: 0,
  scoreAtStart: 0,

  lives: 0,
  caught: 0,
  target: 0,
  escapesInRun: 0,

  combo: 0,
  comboMultiplier: 1,
  lastCatchTime: -1,

  spawnTimer: 0,
  spawnInterval: 0,
  maxActive: 0,
  mouseMix: { normal: 0, fast: 0, big: 0 },

  screenTimer: 0,
  paused: false,
  pausedFrom: null,

  cat: {
    x: 480,
    y: 270,
    vx: 0,
    vy: 0,
    radius: 18,
    pounceTimer: 0,
    pounceCooldown: 0,
    pounceBuffer: 0,
    pounceDirection: { x: 1, y: 0 },
    lastDirection: { x: 1, y: 0 },
    pouncing: false,
    pounceReadiness: 1
  },

  mice: [],
  holes: [],
  obstacles: [],

  progress: 0,
  messages: [],
  audio: {
    enabled: false,
    lastCue: null
  },
  save: {
    endless_unlocked: false,
    campaign_high_score: 0,
    endless_high_score: 0,
    endless_best_wave: 0,
    total_plays: 0
  },
  time: {
    elapsed: 0,
    frame: 0
  },
  stats: {
    catches: 0,
    escapes: 0,
    pounces: 0,
    multiCatches: 0
  },
  lastCatchEvent: null,
  lastEscapeEvent: null,
  lastBonusEvent: null
}
```

Mouse state in `mice`:

```js
{
  id: 1,
  type: "normal",
  state: "fleeing",
  x: 120,
  y: 420,
  vx: 0,
  vy: 0,
  radius: 14,
  maxSpeed: 180,
  outTime: 0,
  emergeTimer: 0,
  enterTimer: 0,
  startleTimer: 0,
  holeIndex: 0,
  wanderAngle: 0,
  wanderTimer: 0,
  stuckTimer: 0,
  pendingEscape: false
}
```

Hole state:

```js
{
  x: 120,
  y: 420,
  radius: 24,
  occupiedTimer: 0,
  blocked: false,
  blockedOverride: null
}
```

Message state:

```js
{
  text: "Mouse escaped!",
  priority: 70,
  remaining: 1.0,
  duration: 1.0
}
```

`lastCatchEvent`:

```js
{
  time: number,
  count: number,
  scoreDelta: number,
  multiBonus: number,
  pouncing: boolean
}
```

`lastEscapeEvent`:

```js
{
  time: number,
  mouseType: string,
  livesRemaining: number
}
```

`lastBonusEvent`:

```js
{
  type: "levelComplete" | "endlessWaveComplete",
  bonus: number,
  perfect: boolean,
  scoreDelta: number
}
```

---

## 7. Required level data

The following level data must be implemented exactly in `js/levels.js`.

```js
const LEVELS = [
  {
    level: 1,
    target: 5,
    maxActive: 2,
    spawnInterval: 2.0,
    mix: { normal: 100, fast: 0, big: 0 },
    holes: [[120, 420], [840, 420]],
    obstacles: []
  },
  {
    level: 2,
    target: 8,
    maxActive: 3,
    spawnInterval: 1.8,
    mix: { normal: 100, fast: 0, big: 0 },
    holes: [[120, 120], [840, 120], [480, 440]],
    obstacles: [[400, 230, 160, 80]]
  },
  {
    level: 3,
    target: 10,
    maxActive: 3,
    spawnInterval: 1.6,
    mix: { normal: 75, fast: 25, big: 0 },
    holes: [[120, 420], [480, 120], [840, 420]],
    obstacles: [[180, 180, 120, 80], [660, 300, 120, 80]]
  },
  {
    level: 4,
    target: 10,
    maxActive: 3,
    spawnInterval: 1.6,
    mix: { normal: 80, fast: 0, big: 20 },
    holes: [[120, 120], [840, 120], [120, 420], [840, 420]],
    obstacles: [[300, 150, 200, 80], [480, 330, 120, 120]]
  },
  {
    level: 5,
    target: 12,
    maxActive: 4,
    spawnInterval: 1.5,
    mix: { normal: 50, fast: 30, big: 20 },
    holes: [[120, 120], [480, 440], [840, 120]],
    obstacles: [[150, 200, 120, 120], [690, 200, 120, 120]]
  },
  {
    level: 6,
    target: 14,
    maxActive: 4,
    spawnInterval: 1.4,
    mix: { normal: 40, fast: 40, big: 20 },
    holes: [[120, 120], [840, 120], [120, 420], [840, 420]],
    obstacles: [[360, 120, 240, 80], [240, 320, 120, 80], [600, 320, 120, 80]]
  },
  {
    level: 7,
    target: 16,
    maxActive: 4,
    spawnInterval: 1.3,
    mix: { normal: 30, fast: 50, big: 20 },
    holes: [[120, 120], [480, 120], [840, 120], [480, 440]],
    obstacles: [[180, 180, 100, 180], [680, 180, 100, 180]]
  },
  {
    level: 8,
    target: 16,
    maxActive: 5,
    spawnInterval: 1.2,
    mix: { normal: 30, fast: 30, big: 40 },
    holes: [[120, 120], [840, 120], [120, 420], [480, 440], [840, 420]],
    obstacles: [[300, 120, 120, 80], [540, 120, 120, 80], [420, 300, 120, 80]]
  },
  {
    level: 9,
    target: 18,
    maxActive: 5,
    spawnInterval: 1.1,
    mix: { normal: 30, fast: 35, big: 35 },
    holes: [[120, 120], [480, 120], [840, 120], [120, 420], [840, 420]],
    obstacles: [[200, 200, 120, 80], [420, 320, 120, 80], [640, 200, 120, 80]]
  },
  {
    level: 10,
    target: 20,
    maxActive: 5,
    spawnInterval: 1.0,
    mix: { normal: 25, fast: 45, big: 30 },
    holes: [[120, 120], [480, 120], [840, 120], [120, 420], [480, 440], [840, 420]],
    obstacles: [[160, 160, 120, 120], [680, 160, 120, 120], [400, 320, 160, 80]]
  }
];
```

Obstacles in the data are arrays `[x, y, width, height]`.

The level loader must convert them to objects:

```js
{ x, y, width, height }
```

---

## 8. Endless wave generation

`Game.Levels.getEndlessWave(waveNumber)` must use:

```js
layoutLevel = [10, 9, 8][(waveNumber - 1) % 3]
```

Wave parameters:

```js
target = Math.min(50, 15 + 5 * (waveNumber - 1));

spawnInterval = Math.max(0.6, 1.0 - 0.05 * (waveNumber - 1));

maxActive = Math.min(7, 4 + Math.floor((waveNumber + 1) / 2));

lives = 3;
```

Mouse mix:

```js
normal = Math.max(10, 40 - 2 * (waveNumber - 1));
fast = 35 + 2 * (waveNumber - 1);
big = 25 + 2 * (waveNumber - 1);
```

Wave shape:

```js
{
  wave: number,
  layoutLevel: number,
  target: number,
  spawnInterval: number,
  maxActive: number,
  mix: { normal, fast, big },
  holes: [[x, y], ...],
  obstacles: [[x, y, w, h], ...]
}
```

Endless waves use the holes and obstacles from the selected campaign layout.

---

## 9. Game loop and update order

### 9.1 Production loop

```js
function loop(now) {
  const dt = Math.min(MAX_FRAME_DT, (now - lastTime) / 1000);
  lastTime = now;

  accumulator += dt;

  while (accumulator >= FIXED_DT) {
    update(FIXED_DT);
    accumulator -= FIXED_DT;
  }

  render();
  updateUI();
  requestAnimationFrame(loop);
}
```

If paused:

- Do not call `update`.
- Still render and update UI if needed.

---

### 9.2 Update eligibility

Call `update(dt)` only when:

```js
screen === "levelIntro"
screen === "playing"
screen === "levelComplete"
screen === "endlessWaveComplete"
```

and:

```js
paused === false
```

For `levelComplete` and `endlessWaveComplete`, update only:

- `screenTimer`
- messages
- UI

Do not update entities.

---

### 9.3 Level intro update

When `screen === "levelIntro"`:

1. Update cat movement.
2. Decrement `screenTimer`.
3. Update messages.
4. If `screenTimer <= 0`:
   - Set `screen = "playing"`.
   - Set `spawnTimer = 1.0`.
   - Show center message if needed.

No mouse spawning occurs during intro.

---

### 9.4 Playing update order

When `screen === "playing"`, update in this exact order:

1. Update cat.
2. Update hole blocked state.
3. Decrement hole occupied timers.
4. Update spawning.
5. Update all mice.
6. Process catches.
7. If target reached, trigger level/wave complete and skip escapes.
8. Otherwise process escapes.
9. Update combo timeout.
10. Update messages.
11. Update `time.elapsed` and `time.frame`.

This order is required to satisfy the rule that catches win over escapes in the same frame.

---

## 10. Cat system

### 10.1 Cat update

Each frame:

```js
input = normalize(input.movement)
```

Pounce press handling:

```js
if pouncePressed:
    if pounceCooldown <= 0:
        startPounce()
    else:
        pounceBuffer = 0.1
```

Buffer decay:

```js
pounceBuffer = max(0, pounceBuffer - dt)
```

If cooldown becomes ready and buffer is active:

```js
if pounceCooldown <= 0 and pounceBuffer > 0:
    startPounce()
    pounceBuffer = 0
```

`startPounce()`:

```js
if input.length > 0:
    pounceDirection = input
    lastDirection = input
else:
    pounceDirection = lastDirection

pounceTimer = 0.18
pounceCooldown = 0.8
pouncing = true
audio.play("pounce")
stats.pounces += 1
```

Movement:

```js
if pounceTimer > 0:
    velocity = pounceDirection * 520
    pounceTimer = max(0, pounceTimer - dt)
    if pounceTimer === 0:
        pouncing = false
else:
    if input.length > 0:
        velocity += input * 2200 * dt
        lastDirection = input
    else:
        velocity = moveToward(velocity, 0, 1200 * dt)

    velocity = clampVectorLength(velocity, 260)
```

Position:

```js
position += velocity * dt
resolveEntity(cat, obstacles)
```

Cooldown:

```js
pounceCooldown = max(0, pounceCooldown - dt)
```

Pounce readiness for HUD:

```js
if pounceCooldown <= 0:
    pounceReadiness = 1
else:
    pounceReadiness = 1 - pounceCooldown / 0.8
```

Clamp readiness between 0 and 1.

---

### 10.2 Pounce direction rules

- If moving, pounce in current movement direction.
- If not moving, pounce in last movement direction.
- If no last direction exists, pounce right:

```js
{ x: 1, y: 0 }
```

---

## 11. Mouse AI

### 11.1 Mouse states

Active mouse states:

```text
emerging
fleeing
entering
```

#### Emerging

- Duration: `0.25s`
- Mouse does not move.
- Mouse is not catchable.
- After timer ends, state becomes `fleeing`.
- `outTime` starts at `0` when fleeing begins.

#### Fleeing

- Mouse moves according to AI.
- Catchable.
- Can enter a hole after `outTime >= 2.5`.
- Can become startled if it is a Big mouse touched by a non-pouncing cat.

#### Entering

- Duration: `0.3s`
- Mouse moves slightly toward hole center.
- Hole becomes occupied for `0.8s`.
- Mouse is still catchable.
- If caught, it does not escape.
- If timer ends, it escapes.

---

### 11.2 Mouse update

For each active mouse:

```js
if state === "emerging":
    emergeTimer -= dt
    if emergeTimer <= 0:
        state = "fleeing"
        outTime = 0
        wanderAngle = rng.angle()
        wanderTimer = rng.range(0.3, 0.6)
        continue
```

For `fleeing`:

```js
outTime += dt
startleTimer = max(0, startleTimer - dt)
wanderTimer -= dt
```

If `wanderTimer <= 0`:

```js
wanderAngle += rng.range(-45deg, +45deg)
wanderTimer = rng.range(0.3, 0.6)
```

Compute desired direction:

```js
desired = { x: 0, y: 0 }

distToCat = distance(mouse, cat)

if distToCat < 140:
    desired += normalize(mouse - cat) * 1.0
else:
    desired += normalize(mouse - cat) * 0.3

desired += normalize(wanderVector) * 0.6

if outTime >= 2.5 and startleTimer <= 0:
    hole = nearestAvailableHole(mouse)
    if hole exists:
        seekWeight = Math.min(1.5, 0.5 + (outTime - 2.5))
        desired += normalize(hole - mouse) * seekWeight

desired += separationFromOtherMice(mouse)

if length(desired) < 0.1:
    desired = normalize(wanderVector)

desired = normalize(desired)
desired = avoidObstacles(mouse, desired)
```

Apply acceleration:

```js
effectiveMaxSpeed = mouse.maxSpeed
if mouse.type === "big" and startleTimer > 0:
    effectiveMaxSpeed *= 1.3

mouse.vx += desired.x * 1800 * dt
mouse.vy += desired.y * 1800 * dt
velocity = clampVectorLength(velocity, effectiveMaxSpeed)
position += velocity * dt
resolveEntity(mouse, obstacles)
```

Stuck recovery:

```js
if length(velocity) < 1:
    stuckTimer += dt
else:
    stuckTimer = 0

if stuckTimer >= 1.0:
    wanderAngle = rng.angle()
    wanderTimer = rng.range(0.3, 0.6)
    stuckTimer = 0
```

---

### 11.3 Separation

For each other active mouse in `fleeing` state:

```js
if distance < 28:
    desired += normalize(this - other) * 0.5
```

Do not separate against `emerging` or `entering` mice.

Reason:

- Emerging mice are stationary and not yet active.
- Entering mice are committed to a hole and should not create jittery escape behavior.

---

### 11.4 Obstacle avoidance

Use the provided simple lookahead algorithm.

```js
function avoidObstacles(mouse, desired):
    lookahead = 20
    testPosition = mouse.position + desired * lookahead

    if circleAt(testPosition, mouse.radius) does not collide with any obstacle:
        return desired

    for angle in [30, -30, 60, -60, 90, -90, 120, -120]:
        rotated = rotate(desired, angle)
        testPosition = mouse.position + rotated * lookahead
        if circleAt(testPosition, mouse.radius) does not collide:
            return rotated

    return rotate(desired, 180)
```

Angles are degrees internally converted to radians.

---

### 11.5 Nearest available hole

A hole is available for escape if:

```js
hole.occupiedTimer <= 0
and distance(cat, hole) > 40
```

If `hole.blockedOverride` is set by debug, use that value instead of the computed blocked state.

Choose the nearest available hole by center distance.

If no hole is available, the mouse does not seek a hole.

---

### 11.6 Entering hole

A mouse may enter a hole if:

```js
state === "fleeing"
and outTime >= 2.5
and startleTimer <= 0
and distance(mouse, hole) <= 24
and hole.occupiedTimer <= 0
and hole is not blocked
```

When entering:

```js
state = "entering"
enterTimer = 0.3
holeIndex = index
hole.occupiedTimer = 0.8
pendingEscape = false
```

While entering:

```js
enterTimer -= dt
move slightly toward hole center at 60 px/s
resolveEntity(mouse, obstacles)
```

If `enterTimer <= 0`:

```js
pendingEscape = true
```

Do not remove the mouse immediately. Removal happens in escape processing after catch processing.

---

## 12. Hole system

Each hole has:

```js
{
  x,
  y,
  radius: 24,
  occupiedTimer: 0,
  blocked: false,
  blockedOverride: null
}
```

Blocked state:

```js
if blockedOverride !== null:
    blocked = blockedOverride
else:
    blocked = distance(cat, hole) <= 40
```

Occupancy:

- Set to `0.8` when a mouse begins entering.
- Decrements each frame while greater than zero.
- Continues even if the mouse is caught during entry.
- No other mouse may enter while `occupiedTimer > 0`.

Spawning does not occupy a hole.

---

## 13. Spawning system

Spawn conditions:

```js
screen === "playing"
and caught < target
and activeMouseCount < maxActive
and spawnTimer <= 0
and at least one hole is available
```

Hole available for spawning:

```js
hole.occupiedTimer <= 0
and hole is not blocked
```

At level/wave start:

```js
spawnTimer = 1.0
```

For campaign levels, this happens when intro ends.

For endless waves, this happens immediately when the wave starts.

After spawn:

```js
spawnTimer = level.spawnInterval
```

If no hole is available:

- `spawnTimer` continues decreasing to zero.
- Spawning waits until a hole becomes available.

Mouse type selection:

```js
type = RNG.pickWeighted(level.mix, rng)
```

If `pickWeighted` returns null, do not spawn.

Spawn position:

- Hole center.
- State: `emerging`.
- `emergeTimer = 0.25`.
- `outTime = 0`.
- Velocity zero.

---

## 14. Catching system

Catch check occurs after mouse movement and before escape finalization.

A mouse is catchable if:

```js
state === "fleeing" or state === "entering"
and distance(cat, mouse) < cat.radius + mouse.radius
```

Big mouse rule:

```js
if mouse.type === "big":
    canCatch = cat.pounceTimer > 0
else:
    canCatch = true
```

If a Big mouse is touched while `canCatch === false`:

- Do not catch.
- Set `startleTimer = 0.3`.
- Play `startle`.
- Mouse continues fleeing.
- While startled:
  - Max speed multiplied by `1.3`.
  - Cannot seek holes.
  - Still flees from cat.

If caught:

1. Remove mouse from active list.
2. Mark as caught for this frame.
3. Add to catch event count.

Catch scoring is processed after all catchable mice in the frame are identified.

---

## 15. Score and combo

### 15.1 Combo update

On each caught mouse:

```js
if lastCatchTime < 0 or time - lastCatchTime > 3.0:
    combo = 1
else:
    combo += 1

lastCatchTime = time
comboMultiplier = Math.min(3.0, 1.0 + 0.25 * (combo - 1))
```

If no catch occurs for `3.0` seconds:

```js
combo = 0
comboMultiplier = 1.0
```

If a mouse escapes:

```js
combo = 0
comboMultiplier = 1.0
```

Combo resets at level/wave start.

---

### 15.2 Catch score

For each caught mouse:

```js
base = 100
bonus = 0

if cat.pounceTimer > 0:
    bonus += 50

if mouse.outTime < 1.0:
    bonus += 50

points = base + bonus
score += floor(points * comboMultiplier)
```

`mouse.outTime` is the time spent in `fleeing` state.

---

### 15.3 Multi-catch bonus

If multiple mice are caught in the same frame:

```js
multiBonus = 100 * (caughtCount - 1)
score += multiBonus
```

This bonus is added once per frame, not per mouse.

`lastCatchEvent` must record:

```js
{
  time,
  count,
  scoreDelta,
  multiBonus,
  pouncing
}
```

`pouncing` is true if the cat was pouncing during the catch event.

---

## 16. Escape system

A mouse escapes when:

```js
state === "entering"
and enterTimer <= 0
and not caught this frame
```

Escape processing happens after catch processing.

For each escaping mouse:

1. Remove from active list.
2. `lives -= 1`.
3. `escapesInRun += 1`.
4. `combo = 0`.
5. Play `escape`.
6. Show center message:

```text
Mouse escaped!
```

If `lives <= 0`:

- Trigger game over.

If multiple mice escape in the same frame:

- Each reduces lives by 1.
- Game over triggers if lives reach zero or below.

---

## 17. Level complete and game over priority

Catches are processed before escapes.

If in the same frame:

- The final catch reaches target.
- Another mouse completes entering a hole.

Then:

- Level/wave complete wins.
- The escape is not processed.
- Lives are not reduced.

This is required by `gameplay.md` edge case 28.9.

---

## 18. Level complete system

When campaign target is reached:

```js
caught >= target
```

Do:

1. Stop spawning.
2. Stop mouse updates.
3. Add level bonus.
4. Update high score.
5. Save.
6. Show `levelComplete` screen.
7. Set `screenTimer = 3.0`.

Level bonus:

```js
bonus = lives * 500
if escapesInRun === 0:
    bonus += 1000
score += bonus
```

`lastBonusEvent`:

```js
{
  type: "levelComplete",
  bonus: bonus,
  perfect: escapesInRun === 0,
  scoreDelta: bonus
}
```

After 3 seconds:

- If level < 10:
  - Start next level.
- If level === 10:
  - Trigger campaign complete.

Player can click Next immediately.

---

## 19. Campaign complete

When level 10 completes:

1. Set `save.endless_unlocked = true`.
2. Update campaign high score.
3. Save.
4. Show `campaignComplete`.

Buttons:

- Play Endless
- Main Menu

---

## 20. Game over system

When:

```js
lives <= 0
and target not reached
```

Do:

1. Stop gameplay.
2. Update high score.
3. Save.
4. Show `gameOver` or `endlessGameOver`.

Retry:

- Restarts current level or wave.
- Uses `scoreAtStart`.
- Resets lives to 3.
- Resets combo.
- Resets caught.
- Resets escapes in run.
- Clears mice.
- Resets holes.
- Resets cat position.
- Resets pounce timers.

---

## 21. Endless mode

Endless mode is unlocked after campaign complete.

`startEndless()` should refuse to start if:

```js
save.endless_unlocked === false
```

Tests can set save data to unlock it.

Starting endless:

```js
mode = "endless"
score = 0
total_plays += 1
startWave(1)
```

Starting a wave:

1. Load wave layout.
2. Set `wave`.
3. Set `layoutLevel`.
4. Set `target`.
5. Set `spawnInterval`.
6. Set `maxActive`.
7. Set `mouseMix`.
8. Set `lives = 3`.
9. Set `caught = 0`.
10. Set `escapesInRun = 0`.
11. Set `combo = 0`.
12. Set `lastCatchTime = -1`.
13. Set `scoreAtStart = current score`.
14. Clear mice.
15. Reset holes.
16. Reset cat.
17. Set `spawnTimer = 1.0`.
18. Set `screen = "playing"`.
19. Show center message:

```text
Wave X
```

There is no separate endless wave intro screen.

Reason:

- `gameplay.md` does not require one.
- A short center message is enough.
- It keeps endless flow fast.

---

## 22. Endless wave complete

When endless target is reached:

1. Add wave bonus.
2. Update endless high score.
3. Update `endless_best_wave`.
4. Save.
5. Show `endlessWaveComplete`.
6. Set `screenTimer = 3.0`.

Wave bonus:

```js
bonus = wave * 500
bonus += lives * 250
if escapesInRun === 0:
    bonus += 1000
score += bonus
```

After 3 seconds:

- Start next wave.
- Score carries forward.
- Lives reset to 3.
- Combo resets.

---

## 23. Save system

Save data:

```js
{
  endless_unlocked: boolean,
  campaign_high_score: integer,
  endless_high_score: integer,
  endless_best_wave: integer,
  total_plays: integer
}
```

Save timing:

- Campaign level complete.
- Campaign complete.
- Campaign game over.
- Endless wave complete.
- Endless game over.

High score update:

Campaign:

```js
if score > save.campaign_high_score:
    save.campaign_high_score = score
```

Endless:

```js
if score > save.endless_high_score:
    save.endless_high_score = score
```

Best wave:

```js
if wave > save.endless_best_wave:
    save.endless_best_wave = wave
```

Total plays:

- Increment when starting campaign.
- Increment when starting endless.

No mid-level progress is saved.

---

## 24. Audio implementation

Audio cues are triggered by gameplay events.

Required cues:

| Event | Cue |
|---|---|
| UI button click | `ui_click` |
| Pounce starts | `pounce` |
| Mouse caught | `catch` |
| Multi-catch | `multi_catch` |
| Big mouse touched while not pouncing | `startle` |
| Mouse escapes | `escape` |
| Level complete | `level_complete` |
| Campaign complete | `campaign_complete` |
| Campaign game over | `game_over` |
| Endless wave complete | `endless_wave_complete` |
| Endless game over | `endless_game_over` |

Optional cue not triggered:

| Event | Cue |
|---|---|
| Combo milestone | `combo_milestone` |

The audio manager must record `lastCue` in state even when audio is disabled.

This allows tests to verify event triggering without actual sound.

---

## 25. HUD rules

HUD is updated from state.

### 25.1 Score

Display:

```text
Score: 000000
```

Always visible during gameplay.

---

### 25.2 Combo

Display only when:

```js
comboMultiplier > 1.0
```

Format:

```text
Combo: x1.25
```

Round to two decimals.

---

### 25.3 Level or wave

Campaign:

```text
Level 3
```

Endless:

```text
Wave 5
```

Always visible during gameplay.

---

### 25.4 Progress

Display:

```text
Caught: 7 / 10
```

Progress bar fill:

```js
progress = clamp(caught / target, 0, 1)
```

---

### 25.5 Lives

Display 3 life icons.

Full icons:

```js
remainingLives
```

Empty icons:

```js
3 - remainingLives
```

---

### 25.6 Pounce bar

Bar:

```text
width: 120px
height: 8px
```

Fill:

```js
pounceReadiness
```

When full, pounce is ready.

Optional label:

```text
Pounce
```

---

### 25.7 Center messages

Only one message at a time.

Higher priority replaces lower priority.

Priority values:

```js
gameOver: 100
levelComplete: 90
waveComplete: 80
mouseEscaped: 70
newMouseType: 60
levelStart: 50
waveStart: 50
```

Duration:

```text
1.0 to 1.5 seconds
```

Messages must not block gameplay.

---

## 26. UI flow details

### 26.1 Main menu

Buttons:

- Play
- Endless, only if unlocked
- How to Play

Play:

```js
score = 0
startCampaign()
```

Endless:

```js
score = 0
startEndless()
```

---

### 26.2 How to play

Back returns to menu.

No gameplay timers run.

---

### 26.3 Pause

Pause overlay buttons:

- Resume
- Restart
- Main Menu

Resume:

- Returns to `pausedFrom`.

Restart:

- Restarts current level or wave from `scoreAtStart`.

Main Menu:

- Clears active run.
- Does not save mid-level progress.

---

### 26.4 Level complete

Buttons:

- Next Level

Auto-advance after 3 seconds.

For level 10, the screen becomes campaign complete instead.

---

### 26.5 Campaign complete

Buttons:

- Play Endless
- Main Menu

---

### 26.6 Game over

Buttons:

- Retry
- Main Menu

Retry restarts current level or wave.

---

### 26.7 Endless wave complete

No required button.

Auto-advance after 3 seconds.

Display:

```text
Wave X Complete
Score: N
Bonus: N
Next Wave in 3
```

Countdown can be integer seconds:

```text
3
2
1
```

---

## 27. Debug API: `window.__game`

The debug API is required for tests.

All methods must be safe to call from tests.

All setters should clamp values to valid ranges where reasonable.

### 27.1 State and save

```js
getState()
getSave()
setSave(saveObject)
reset()
```

`reset()`:

- Returns to menu.
- Clears entities.
- Clears score.
- Clears active level/wave.
- Keeps save data.
- Clears messages.
- Clears audio last cue.
- Does not change `window.__game` seed unless explicitly set.

---

### 27.2 Flow

```js
startCampaign()
startEndless()
startLevel(levelNumber)
startWave(waveNumber)
next()
retry()
mainMenu()
howToPlay()
back()
```

`startLevel(levelNumber)`:

- Starts a campaign level using current score as `scoreAtStart`.
- For normal campaign flow, `startCampaign()` sets score to 0 first.

`startWave(waveNumber)`:

- Starts an endless wave using current score as `scoreAtStart`.
- For normal endless flow, `startEndless()` sets score to 0 first.

`startEndless()`:

- Returns `false` and does nothing if endless is not unlocked.
- Returns `true` and starts wave 1 if unlocked.

---

### 27.3 Pause and focus

```js
pause()
resume()
setPaused(boolean)
simulateFocusLoss()
```

`simulateFocusLoss()` triggers the same behavior as browser blur.

---

### 27.4 Time control

```js
setAutoStep(boolean)
step(seconds)
stepUntil(predicate, maxSeconds)
getFixedDt()
```

`step(seconds)`:

- Advances the simulation by whole fixed steps.
- Returns number of steps executed.
- Stops early if the game leaves an update-eligible screen.
- Does nothing if paused.

`stepUntil(predicate, maxSeconds)`:

- Repeatedly steps until predicate returns true.
- Predicate receives `getState()`.
- Returns `true` if condition met, `false` if timeout.
- Default `maxSeconds` is `10`.

---

### 27.5 RNG

```js
setSeed(seed)
getSeed()
```

`setSeed` resets the RNG.

---

### 27.6 Input

```js
setMovementInput(x, y)
setPounceDown(boolean)
triggerPounce()
clearInput()
```

`setMovementInput(x, y)` sets raw input values.

The game normalizes the vector.

`triggerPounce()` simulates a pounce press edge.

---

### 27.7 Cat control

```js
setCatPosition(x, y)
setCatVelocity(x, y)
setPounceTimer(t)
setPounceCooldown(t)
setPounceBuffer(t)
setLastDirection(x, y)
```

All values are clamped to sensible ranges.

---

### 27.8 Mouse control

```js
forceSpawn({ type, holeIndex })
forceCatch({ mouseId, pouncing })
forceEscape({ mouseId })
setMousePosition(id, x, y)
setMouseState(id, state)
setMouseOutTime(id, t)
setMouseEnterTimer(id, t)
setMouseStartleTimer(id, t)
setMouseStuckTimer(id, t)
setMouseVelocity(id, x, y)
```

`forceSpawn`:

- Creates a mouse immediately.
- Bypasses spawn timer and max active rules.
- Uses given type or chooses using current level mix and RNG.
- Uses given `holeIndex` or first hole.
- Returns new mouse id.
- Does not reset `spawnTimer`.

`forceCatch`:

- Catches the given mouse immediately.
- Bypasses collision.
- Uses `pouncing` for score and Big mouse rules.
- If no `mouseId` is given, catch the first catchable active mouse.
- Returns `true` if a mouse was caught.

`forceEscape`:

- Processes escape for the given mouse immediately.
- Returns `true` if escape was processed.

---

### 27.9 Run control

```js
setLives(n)
setScore(n)
setCombo(n)
setLastCatchTime(t)
setCaught(n)
setTarget(n)
setEscapesInRun(n)
setSpawnTimer(t)
```

All values are integers or seconds as appropriate.

---

### 27.10 Hole control

```js
setHoleOccupied(index, t)
setHoleBlocked(index, blocked)
clearHoleOverrides()
```

`setHoleBlocked` sets `blockedOverride`.

`clearHoleOverrides()` removes all debug blocking overrides.

---

### 27.11 Audio

```js
setAudioEnabled(boolean)
playCue(cue)
```

`playCue` records `lastCue` and plays audio if enabled.

---

### 27.12 Level data

```js
getLevelData(levelNumber)
getWaveData(waveNumber)
validateLevel(levelNumber)
validateWave(waveNumber)
```

These return plain data objects.

---

## 28. Test harness: `window.__test`

The test harness must be minimal but sufficient.

Required API:

```js
window.__test.test(name, fn)
window.__test.assert(condition, message)
window.__test.assertClose(actual, expected, epsilon, message)
window.__test.assertDeepEqual(actual, expected, message)
window.__test.getResults()
window.__test.run()
```

`run()` must:

- Execute tests sequentially.
- Support async test functions.
- Catch assertion failures.
- Record failures with stack traces.
- Reset the game before each test.
- Resolve with final results.
- Assign results to `window.__testResults`.

Result shape:

```js
{
  passed: number,
  failed: number,
  total: number,
  failures: [
    {
      name: string,
      message: string,
      stack: string
    }
  ]
}
```

Default epsilon for `assertClose`:

```js
0.001
```

---

## 29. Required tests

The following tests are required.

They must pass when loading:

```text
index.html?test=1
```

and checking:

```js
window.__testResults.failed === 0
```

Tests should use helpers:

```js
const G = window.__game;
const T = window.__test;

async function stepTo(screen, maxSeconds = 10) {
  return G.stepUntil(function (state) {
    return state.screen === screen;
  }, maxSeconds);
}
```

---

### 29.1 Bootstrap tests

#### Test: debug API exists

Assert:

```js
typeof window.__game === "object"
typeof window.__test === "object"
```

#### Test: initial state is menu

Assert:

```js
state.screen === "menu"
state.mode === null
state.level === null
state.wave === null
state.score === 0
state.lives === 0
state.caught === 0
state.target === 0
state.mice.length === 0
```

#### Test: save defaults

After reset:

```js
state.save.endless_unlocked === false
state.save.campaign_high_score === 0
state.save.endless_high_score === 0
state.save.endless_best_wave === 0
state.save.total_plays === 0
```

---

### 29.2 Level data tests

#### Test: all 10 levels exist

For `1..10`:

```js
G.getLevelData(n) is not null
```

#### Test: level parameters match gameplay

For each level, assert target, max active, spawn interval, and mix.

#### Test: level layouts match gameplay

Assert holes and obstacles exactly.

#### Test: all levels validate

For `1..10`:

```js
G.validateLevel(n).valid === true
```

#### Test: Level 2 cat start is valid

Start level 2.

Assert:

```js
cat.x is within arena bounds
cat.y is within arena bounds
cat is not inside obstacle
cat.y <= 212.01
```

#### Test: endless wave 1 data

Assert:

```js
wave = 1
layoutLevel = 10
target = 15
spawnInterval = 1.0
maxActive = 5
```

#### Test: endless wave 2 data

Assert:

```js
wave = 2
layoutLevel = 9
target = 20
spawnInterval = 0.95
maxActive = 5
```

#### Test: endless wave 3 data

Assert:

```js
wave = 3
layoutLevel = 8
target = 25
spawnInterval = 0.9
maxActive = 6
```

#### Test: endless wave 5 data

Assert:

```js
wave = 5
target = 35
maxActive = 7
```

#### Test: endless wave caps

For wave 100:

```js
target <= 50
spawnInterval >= 0.6
maxActive <= 7
```

---

### 29.3 Campaign flow tests

#### Test: start campaign

Call:

```js
G.startCampaign()
```

Assert:

```js
state.mode === "campaign"
state.level === 1
state.screen === "levelIntro"
state.score === 0
state.save.total_plays >= 1
```

#### Test: level intro lasts 1.5 seconds

Start campaign.

Step `1.49`.

Assert:

```js
state.screen === "levelIntro"
```

Step `0.02`.

Assert:

```js
state.screen === "playing"
state.spawnTimer <= 1.0
```

#### Test: no mice during intro

Start campaign.

Step `1.5`.

Assert:

```js
state.mice.length === 0
```

#### Test: first mouse spawns 1.0 seconds after intro

Start campaign.

Step `1.5`.

Assert no mice.

Step `0.99`.

Assert no mice.

Step `0.02`.

Assert:

```js
state.mice.length === 1
```

---

### 29.4 Cat movement tests

#### Test: cat moves right with input

Start level 1.

Step to playing.

Record initial `cat.x`.

Set movement input `(1, 0)`.

Step `0.5`.

Assert:

```js
cat.x increased
cat.vx > 0
```

Clear input.

Step `0.5`.

Assert:

```js
cat.vx is closer to 0 than before
```

#### Test: cat respects arena bounds

Set cat position near right wall.

Set movement right.

Step `0.5`.

Assert:

```js
cat.x <= 960 - cat.radius
```

#### Test: cat collides with obstacle

Start level 2.

Step to playing.

Set cat position above central obstacle.

Set movement down.

Step `0.5`.

Assert cat is not inside obstacle.

---

### 29.5 Pounce tests

#### Test: pounce starts and lasts 0.18 seconds

Start level 1.

Step to playing.

Set movement right.

Step `0.05`.

Trigger pounce.

Assert:

```js
cat.pounceTimer > 0
cat.pounceCooldown > 0
cat.pouncing === true
state.stats.pounces >= 1
state.audio.lastCue === "pounce"
```

Step `0.18`.

Assert:

```js
cat.pounceTimer === 0
cat.pouncing === false
```

#### Test: pounce cooldown is 0.8 seconds

After pounce:

```js
cat.pounceCooldown approximately 0.8
```

Step `0.3`.

Assert:

```js
cat.pounceCooldown approximately 0.5
```

#### Test: pounce buffer works

Set pounce cooldown to `0.05`.

Trigger pounce.

Assert pounce did not start immediately.

Step `0.04`.

Assert pounce did not start.

Step `0.02`.

Assert pounce started.

#### Test: pounce uses last direction

Set last direction down.

Clear movement input.

Trigger pounce.

Assert:

```js
cat.vy > 0
cat.vx === 0
```

#### Test: pounce defaults right if no direction

Set last direction to zero or reset cat.

Clear input.

Trigger pounce.

Assert:

```js
cat.vx > 0
cat.vy === 0
```

---

### 29.6 Mouse spawn tests

#### Test: mouse emerges then flees

Start level 1.

Step to playing.

Force spawn normal mouse.

Assert:

```js
mouse.state === "emerging"
mouse.emergeTimer approximately 0.25
```

Step `0.25`.

Assert:

```js
mouse.state === "fleeing"
mouse.outTime approximately 0
```

#### Test: spawn respects max active

Start level 1.

Step to playing.

Force spawn one mouse.

Set spawn timer to `0`.

Step `0.05`.

Assert:

```js
state.mice.length === 2
```

Step `0.05`.

Assert:

```js
state.mice.length === 2
```

#### Test: spawn waits when holes blocked

Start level 1.

Step to playing.

Set all holes blocked.

Set spawn timer to `0`.

Step `0.5`.

Assert no mice.

Clear hole overrides.

Step `0.5`.

Assert at least one mouse.

---

### 29.7 Mouse AI tests

#### Test: mouse flees from cat

Start level 1.

Step to playing.

Force spawn normal mouse.

Step `0.25` to make it flee.

Place cat left of mouse.

Step `0.2`.

Assert mouse moved away from cat.

#### Test: mouse seeks hole after 2.5 seconds

Start level 1.

Step to playing.

Force spawn normal mouse.

Step `0.25`.

Set mouse out time to `2.5`.

Place mouse near a hole.

Place cat far away.

Step `0.2`.

Assert mouse moved toward the hole.

#### Test: mouse enters available hole

Start level 1.

Step to playing.

Force spawn normal mouse.

Place mouse within `24px` of a hole.

Set out time to `3`.

Place cat far away.

Step `0.31`.

Assert:

```js
state.lives === 2
state.mice.length === 0
state.audio.lastCue === "escape"
```

#### Test: mouse cannot enter blocked hole

Start level 1.

Step to playing.

Force spawn normal mouse.

Place mouse near hole.

Set out time to `3`.

Place cat within `40px` of hole.

Step `0.5`.

Assert mouse has not escaped.

#### Test: mouse cannot enter occupied hole

Start level 1.

Step to playing.

Force spawn normal mouse.

Place mouse near hole.

Set out time to `3`.

Set hole occupied timer to `0.8`.

Step `0.3`.

Assert mouse has not escaped.

---

### 29.8 Catching tests

#### Test: normal mouse caught by contact

Start level 1.

Step to playing.

Force spawn normal mouse.

Place mouse overlapping cat.

Step `0.02`.

Assert:

```js
state.caught === 1
state.mice.length === 0
state.score === 100
state.combo === 1
state.audio.lastCue === "catch"
```

#### Test: pounce catch bonus

Set mouse out time to `1.5`.

Set pounce timer to `0.1`.

Catch mouse.

Assert score is `150`.

#### Test: fast catch bonus

Set mouse out time to `0.5`.

No pounce.

Catch mouse.

Assert score is `150`.

#### Test: pounce and fast catch bonus

Set mouse out time to `0.5`.

Set pounce timer to `0.1`.

Catch mouse.

Assert score is `200`.

#### Test: Big mouse not caught without pounce

Force spawn Big mouse.

Place overlapping cat.

No pounce.

Step.

Assert:

```js
state.caught === 0
mouse.startleTimer > 0
state.audio.lastCue === "startle"
```

#### Test: Big mouse caught while pouncing

Force spawn Big mouse.

Place overlapping cat.

Set pounce timer to `0.1`.

Step.

Assert:

```js
state.caught === 1
state.mice.length === 0
```

#### Test: multi-catch bonus

Force spawn two normal mice.

Place both overlapping cat.

Set out time greater than `1.0`.

Step one frame.

Assert:

```js
state.caught === 2
state.lastCatchEvent.count === 2
state.lastCatchEvent.multiBonus === 100
```

Expected score:

```js
first catch: 100
second catch: floor(100 * 1.25) = 125
multi bonus: 100
total: 325
```

---

### 29.9 Combo tests

#### Test: combo increases within 3 seconds

Catch mouse.

Assert combo `1`.

Step `2`.

Catch second mouse.

Assert combo `2`.

#### Test: combo resets after 3 seconds

Catch mouse.

Step `3.1`.

Assert:

```js
state.combo === 0
state.comboMultiplier === 1
```

#### Test: escape resets combo

Catch mouse.

Assert combo `1`.

Force escape another mouse.

Assert:

```js
state.combo === 0
```

---

### 29.10 Lives and game over tests

#### Test: escape reduces lives

Start level 1.

Force spawn mouse.

Force escape.

Assert:

```js
state.lives === 2
state.escapesInRun === 1
```

#### Test: game over at zero lives

Start level 1.

Set lives to `1`.

Force escape.

Assert:

```js
state.lives === 0
state.screen === "gameOver"
```

#### Test: multiple escapes same frame

Start level 1.

Set lives to `2`.

Force spawn two mice.

Set both to entering with small enter timer.

Step one frame.

Assert:

```js
state.lives === 0
state.screen === "gameOver"
```

#### Test: target reached same frame as escape wins

Start level 1.

Set target to `1`.

Set lives to `1`.

Force spawn mouse A.

Force spawn mouse B.

Make A catchable.

Make B entering with small enter timer.

Step one frame.

Assert:

```js
state.screen === "levelComplete"
state.lives === 1
state.caught >= 1
```

---

### 29.11 Level complete tests

#### Test: level complete adds bonus

Start level 1.

Set caught to `target - 1`.

Set score to `0`.

Set lives to `3`.

Set escapes in run to `0`.

Set combo to `0`.

Force spawn normal mouse.

Set mouse out time to `1.5`.

Force catch.

Assert:

```js
state.screen === "levelComplete"
state.caught >= target
state.lastBonusEvent.type === "levelComplete"
state.lastBonusEvent.bonus === 2500
state.score === 2600
```

Explanation:

- Catch score: `100`
- Level bonus: `3 * 500 + 1000 = 2500`
- Total: `2600`

#### Test: level complete perfect bonus omitted with escape

Start level 1.

Set caught to `target - 1`.

Set lives to `2`.

Set escapes in run to `1`.

Set score to `0`.

Force catch.

Assert:

```js
state.lastBonusEvent.bonus === 1000
```

Explanation:

- `2 * 500 = 1000`
- No perfect bonus.

#### Test: level complete auto-advances

Complete level 1.

Step `2.99`.

Assert still level complete.

Step `0.02`.

Assert:

```js
state.level === 2
state.screen === "levelIntro"
```

#### Test: level 10 complete triggers campaign complete

Start level 10.

Set caught to `target - 1`.

Force spawn and catch.

Assert:

```js
state.screen === "campaignComplete"
state.save.endless_unlocked === true
```

---

### 29.12 Retry tests

#### Test: retry resets score to level start

Start level 1.

Set score to `1000` mid-level.

Trigger game over.

Call retry.

Assert:

```js
state.score === 0
state.lives === 3
state.caught === 0
state.combo === 0
```

#### Test: retry resets lives

Fail level.

Retry.

Assert:

```js
state.lives === 3
```

#### Test: retry clears mice

Fail level after spawning mice.

Retry.

Assert:

```js
state.mice.length === 0
```

---

### 29.13 Endless mode tests

#### Test: endless locked by default

Reset.

Call `startEndless()`.

Assert:

```js
state.screen === "menu"
```

#### Test: endless starts when unlocked

Set save `endless_unlocked = true`.

Call `startEndless()`.

Assert:

```js
state.mode === "endless"
state.wave === 1
state.screen === "playing"
state.score === 0
```

#### Test: endless wave complete bonus

Start endless.

Set caught to `target - 1`.

Set score to `0`.

Set lives to `3`.

Set escapes in run to `0`.

Force spawn and catch.

Assert:

```js
state.screen === "endlessWaveComplete"
state.lastBonusEvent.type === "endlessWaveComplete"
state.lastBonusEvent.bonus === 1750
state.score === 1850
```

Explanation:

- Catch: `100`
- Wave bonus: `1 * 500 + 3 * 250 + 1000 = 1750`
- Total: `1850`

#### Test: endless wave auto-advances

Complete wave 1.

Step `2.99`.

Assert still wave complete.

Step `0.02`.

Assert:

```js
state.wave === 2
state.lives === 3
state.combo === 0
```

#### Test: endless retry resets score to wave start

Start endless.

Set score to `500` mid-wave.

Trigger endless game over.

Retry.

Assert:

```js
state.score === 0
state.lives === 3
```

#### Test: endless best wave saved

Start endless.

Complete wave 1.

Assert:

```js
state.save.endless_best_wave >= 1
```

---

### 29.14 Pause tests

#### Test: pause stops time

Start level 1.

Step to playing.

Record `state.time.elapsed`.

Pause.

Step `1`.

Assert:

```js
state.time.elapsed unchanged
```

#### Test: pause stops mouse movement

Start level 1.

Spawn mouse.

Step to playing.

Record mouse position.

Pause.

Step `1`.

Assert mouse position unchanged.

#### Test: resume restores gameplay

Pause.

Resume.

Step `0.1`.

Assert time advanced.

#### Test: focus loss pauses

Start level 1.

Step to playing.

Call `simulateFocusLoss()`.

Assert:

```js
state.screen === "paused"
```

Resume.

Assert:

```js
state.screen === "playing"
```

---

### 29.15 HUD state tests

#### Test: progress clamps

Set caught to `10`.

Set target to `5`.

Assert:

```js
state.progress === 1
```

#### Test: combo hidden when multiplier is 1

Set combo to `0`.

Assert:

```js
state.comboMultiplier === 1
```

Set combo to `2`.

Assert:

```js
state.comboMultiplier === 1.25
```

#### Test: pounce readiness

Set pounce cooldown to `0.4`.

Assert:

```js
state.cat.pounceReadiness approximately 0.5
```

Set pounce cooldown to `0`.

Assert:

```js
state.cat.pounceReadiness === 1
```

---

### 29.16 Audio cue tests

Audio must be disabled, but `lastCue` must still update.

#### Test: pounce cue

Disable audio.

Set pounce cooldown to `0`.

Trigger pounce.

Assert:

```js
state.audio.lastCue === "pounce"
```

#### Test: catch cue

Force catch.

Assert:

```js
state.audio.lastCue === "catch"
```

#### Test: multi-catch cue

Force two catches same frame.

Assert:

```js
state.audio.lastCue === "multi_catch"
```

#### Test: startle cue

Touch Big mouse without pounce.

Assert:

```js
state.audio.lastCue === "startle"
```

#### Test: escape cue

Force escape.

Assert:

```js
state.audio.lastCue === "escape"
```

---

### 29.17 High score and save tests

#### Test: campaign high score updates

Set save campaign high score to `0`.

Complete level 1 with score `1000`.

Assert:

```js
state.save.campaign_high_score === 1000
```

#### Test: campaign high score does not decrease

Set save campaign high score to `5000`.

Complete level 1 with score `1000`.

Assert:

```js
state.save.campaign_high_score === 5000
```

#### Test: endless high score separate

Set campaign high score to `100`.

Set endless high score to `0`.

Complete endless wave with score `500`.

Assert:

```js
state.save.campaign_high_score === 100
state.save.endless_high_score === 500
```

---

### 29.18 End-to-end playability tests

#### Test: all campaign levels can be completed

For each level `1..10`:

1. Start level.
2. Step to playing.
3. Set caught to `target - 1`.
4. Force spawn normal mouse.
5. Force catch.
6. Assert screen is `levelComplete` for levels `1..9`.
7. Assert screen is `campaignComplete` for level `10`.

This proves every level loads and completes.

#### Test: all campaign levels can fail and retry

For each level `1..10`:

1. Start level.
2. Step to playing.
3. Set lives to `1`.
4. Force spawn mouse.
5. Force escape.
6. Assert game over.
7. Retry.
8. Assert:
   - lives `3`
   - caught `0`
   - score equals level start score
   - screen is `levelIntro` or `playing`

#### Test: endless waves 1 through 5 can be completed

For waves `1..5`:

1. Ensure endless unlocked.
2. Start wave.
3. Set caught to `target - 1`.
4. Force spawn and catch.
5. Assert wave complete.
6. Assert score carried forward.
7. Step to next wave.

#### Test: full campaign to endless unlock

1. Reset.
2. Start campaign.
3. For levels `1..10`, complete each level using debug catches.
4. Assert campaign complete.
5. Assert endless unlocked.
6. Start endless.
7. Assert wave 1 playing.

This is the highest-level proof that the game is finished and playable.

---

## 30. Invariant tests

These tests should run after many random steps to catch instability.

#### Test: random smoke test

For 200 random frames:

- Start level 5.
- Set random movement input.
- Randomly trigger pounce.
- Step one fixed frame.
- Assert:
  - cat position within arena.
  - all mice within arena.
  - no mouse state is invalid.
  - active mice count <= max active.
  - lives between 0 and 3.
  - caught >= 0.
  - score >= 0.
  - combo >= 0.
  - pounce timers within valid ranges.
  - hole occupied timers within valid ranges.

Use seed `1337` so the test is deterministic.

#### Test: no NaN values

After random smoke test:

Assert no `NaN` in:

- cat position/velocity.
- mouse position/velocity.
- score.
- combo.
- timers.

---

## 31. Acceptance criteria

The game is considered engineering-complete when:

1. All required files exist.
2. All JavaScript files pass syntax check.
3. The page loads without console errors.
4. `window.__game` exists.
5. `window.__test` exists.
6. Loading `index.html?test=1` runs all required tests.
7. `window.__testResults.failed === 0`.
8. The menu is playable.
9. Campaign levels 1 through 10 load and complete.
10. Game over and retry work.
11. Endless mode unlocks after campaign complete.
12. Endless waves 1 through 5 load and complete.
13. Pause and focus-loss pause work.
14. Audio cues are triggered even when audio is disabled.
15. Save data persists high scores and endless unlock.
16. No mouse can become permanently stuck under normal level data.
17. No level makes a hole unreachable according to validation.
18. Catches always win over escapes in the same frame.
19. The game remains stable with maximum endless constraints:
    - 7 active mice
    - 6 holes
    - 3 obstacles
    - fixed timestep
    - no pathfinding

---

## 32. Cut features

The following are intentionally not included:

- No level select screen.
- No mid-level save.
- No camera scrolling.
- No 3D movement.
- No mouse aiming.
- No cat health.
- No mouse health.
- No player upgrades.
- No stamina.
- No shop.
- No cosmetic unlocks.
- No boss mice.
- No destructible obstacles.
- No full pathfinding.
- No combo milestone audio.
- No dynamic level generator beyond the specified endless wave formula.

Reason:

Each cut feature adds state, UI, or AI complexity without improving the core chase loop.

---

## 33. Integration notes for other agents

### 33.1 For visual designer

- The canvas is `960 x 540`.
- The DOM structure in section 4 is stable.
- HUD IDs are stable.
- Render fallbacks exist.
- Visual changes should not modify game state.
- If sprites are added, they should be loaded by `render.js` or `audio.js`-style asset handling without changing gameplay logic.

### 33.2 For gameplay designer

- All gameplay numbers are centralized in `js/config.js`.
- Level data is centralized in `js/levels.js`.
- Endless wave formula is centralized in `Game.Levels.getEndlessWave`.
- Mouse AI constants are in `config.MOUSE`.
- Cat feel constants are in `config.CAT`.
- Score constants are in `config.SCORE`.

### 33.3 For integration agent

- Do not add a build step.
- Do not add npm.
- Do not add a test runner.
- Do not replace the debug API.
- Do not remove `window.__game`.
- Do not remove `window.__test`.
- Do not make tests depend on real time.
- Do not make tests depend on audio playback.
- Do not make tests depend on rendered pixels.
- Keep all gameplay randomness behind the seeded RNG.