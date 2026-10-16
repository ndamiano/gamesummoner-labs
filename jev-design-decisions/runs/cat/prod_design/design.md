# 0. SCOPE

This document is the single merged design for **Cat: Mice Hunt**. It supersedes the separate gameplay, visual, and engineering documents. Where the original documents disagreed, this document makes a final ruling. Where they left gaps because they did not have the other documents, this document fills the gap. Anything dropped from the original designs is documented in **0.2 Decisions**.

The game is a short, complete 2D top-down browser arcade game. The player controls a cat in a fixed single-screen arena. Mice emerge from holes, flee from the cat, and try to escape back into holes. The player wins by catching enough mice before too many escape.

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Play as a cat trying to catch mice | 4.1 Game state, 4.2 Cat movement, 4.7 Catching |
| 2D top-down gameplay | 1.1 Units, axes, frames; 3 Visual Spec |
| Single-screen arena, no camera scrolling | 1.1, 3, 4.17 |
| Arena size is 960 x 540 pixels | 1.1, 2.2, 3 |
| Cat start position is 480, 270 unless corrected | 4.12, 4.18, 0.2 |
| Mice spawn from holes | 4.6 Spawning |
| Mice can escape into holes after 2.5 seconds | 4.3 Mouse AI, 4.5 Hole system |
| Cat catches mice by contact or pounce | 4.2 Cat movement, 4.7 Catching |
| Catch X mice to complete a level | 4.12 Level progression, 4.18 |
| Do not let 3 mice escape | 4.9 Lives |
| Each escaped mouse costs 1 life | 4.8 Escape, 4.9 Lives |
| Cat has no health | 4.2, 4.9 |
| Pounce is the cat’s main action | 4.2 Cat movement |
| Three mouse types: Normal, Fast, Big | 4.3, 4.21 |
| Big mice can only be caught while pouncing | 4.7 Catching |
| 10 campaign levels | 4.12, 4.18 |
| Endless Mode unlocks after Level 10 | 4.13, 4.19 |
| HUD shows score, combo, level/wave, progress, lives, pounce | 4.14, 7 |
| Save high scores and endless unlock | 4.16, 2.2 |
| Browser game with no build step | 1.2, 2.1 |
| Vanilla HTML, CSS, JavaScript only | 1.2, 2.1 |
| Fixed or clamped delta time | 1.1, 1.2 |
| Maximum active mice in Endless is 7 | 4.13, 4.17 |
| Maximum holes per level is 6 | 4.5, 4.17 |
| Maximum obstacles per level is 3 | 4.4, 4.17 |
| No full pathfinding | 4.3, 4.17 |
| No physics engine | 1.2, 4.4 |
| Audio cues for gameplay events | 6 |
| Debug API for tests | 8 |
| Browser test harness | 8, 9 |
| Tests prove each tier is done | 9, 11 |

## 0.2 Decisions

| Decision | Gameplay | Visual | Engineering | Ruling / Reasoning |
| --- | --- | --- | --- | --- |
| External assets | Silent. | Suggested pre-made PNG assets and sprite sheets. | Required `audio/*.ogg` files but allowed missing files and fallback vector graphics. | **No external image or audio assets are required.** All visuals are drawn procedurally on canvas or with CSS. All audio is synthesized with WebAudio. This keeps the game fully browser-playable with no build step, no asset loading, and deterministic tests. |
| Audio implementation | Listed required cues. | Gave SFX descriptions, music, panning, ducking, and procedural audio recipes. | Required `.ogg` files, audio pools, and `lastCue` recording. | **Use WebAudio synthesized cues.** The `.ogg` files are dropped. `Audio.play(cue)` records `lastCue` even when disabled. Music is Tier 4 and optional. |
| Combo milestone audio | Listed as optional. | Recommended a chime at `x2.0` and `x3.0`. | Explicitly cut combo milestone audio. | **Cut combo milestone audio.** The HUD pulse remains. This avoids arbitrary feel complexity and keeps audio cues tied to concrete gameplay events. |
| Level 2 cat start | Cat start is always 480, 270. | Silent. | Level 2 obstacle contains 480, 270; corrected start is approximately 480, 212. | **Use the engineering correction.** On level load, place the cat at 480, 270 and resolve collision with obstacles. If fully inside, push out along smallest axis overlap, tie pushes upward first, then try deterministic offsets. Level validation checks the post-correction position. |
| Mouse states | Listed Emerging, Fleeing, Entering hole, Caught, Escaped. | Animated all five. | Active states are only `emerging`, `fleeing`, `entering`; caught/escaped are event outcomes. | **Active mouse states are `emerging`, `fleeing`, `entering`.** `caught` and `escaped` are not stored on active mice; they are processed as events and remove the mouse from the active list. |
| Endless wave intro | No separate endless intro required. | Silent. | No endless wave intro screen; show center message `Wave X`. | **No endless wave intro screen.** Endless waves start directly in `playing` with a center message and `spawnTimer = 1.0`. |
| High score on main menu | High score appears on complete screens. | Cut high score display on main menu. | No main menu high score in DOM. | **No high score on the main menu.** High scores appear on level complete, campaign complete, game over, endless wave complete, and endless game over screens. |
| Pause availability | Paused state triggered by Esc, P, browser focus loss. | Pause button in HUD. | Pause can occur from `levelIntro`, `playing`, `levelComplete`, `endlessWaveComplete`. | **Pause is allowed from `levelIntro`, `playing`, `levelComplete`, and `endlessWaveComplete`.** `pausedFrom` stores the previous screen. |
| Level select | No level select. | No level select. | No level select. | **No level select.** The campaign is linear. Retry is enough. |
| Camera | No camera movement. | Canvas 960 x 540, no scrolling. | Canvas logical size 960 x 540. | **No camera.** The canvas is always 960 x 540 logical pixels. CSS may scale it visually. |
| HUD safe areas | HUD must not block gameplay. | Entities may enter HUD safe areas; HUD must remain sparse. | HUD is DOM over canvas. | **Entities may render under HUD safe areas.** HUD elements are sparse and non-blocking. Gameplay logic is not affected by HUD regions. |
| Music | Silent. | Required menu, gameplay, and endless music with adaptive layers. | Silent except audio files and cues. | **Music is Tier 4 and optional.** It is synthesized, not file-based. Tier 1 through Tier 3 do not require music. |
| Reduced motion | Silent. | Respect reduced motion where possible. | Silent. | **Reduced motion is Tier 4.** If the browser prefers reduced motion, disable speed lines, vignette pulses, and reduce particles. Essential state changes remain visible. |
| Save scope | Save only minimum data. | Silent. | Save key, defaults, no mid-level progress. | **Save only `endless_unlocked`, `campaign_high_score`, `endless_high_score`, `endless_best_wave`, and `total_plays`.** No mid-level progress is saved. |
| Test mode | Silent. | Silent. | `?test=1` disables auto-step, disables audio, seeds RNG, runs tests. | **Keep test mode.** Loading `index.html?test=1` must produce `window.__testResults` with `failed === 0` for the current tier. |
| Cut features | Listed many cuts. | Listed many visual/audio cuts. | Listed many engineering cuts. | **All listed cuts remain cut.** See 4.17 Cut features. |

## 0.3 Tiers

| Tier | Name | Included systems | Exit criterion |
| ---: | --- | --- | --- |
| 1 | Core playable loop | Runtime, fixed timestep, input, canvas, debug API, test harness, menu, how to play, Level 1 intro, playing, pause, game over, retry, cat movement, pounce, normal mouse AI, holes, collision, spawning, catching, escaping, lives, score, combo, basic HUD, basic visuals, core SFX, minimal save. | A player can start Level 1, move and pounce the cat, catch normal mice, lose lives when mice escape, fail, retry, and see a stable, testable core loop. |
| 2 | Campaign complete | Levels 2 through 10, Level 2 cat correction, Fast and Big mice, mouse mixes, level complete, campaign complete, level themes, full scoring bonuses, high score persistence, endless unlock flag, full campaign tests. | The player can complete or fail all 10 campaign levels, see bonuses, unlock Endless Mode, and persist campaign high score. |
| 3 | Endless mode | Endless start, wave generation, endless wave complete, endless game over, endless retry, endless high score, endless best wave, endless SFX, endless tests. | The player can start Endless Mode after unlock, complete or fail waves 1 through 5, retry, and persist endless high score and best wave. |
| 4 | Presentation polish | Adaptive music, panning, ducking, reduced motion, extra particles, pre-rendered backgrounds, detailed level props, score popups beyond basic, combo pulse polish, motion-sensitive options. | The game feels polished and performant, but Tier 4 is not required to prove the core game is complete. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Quantity | Unit | Value / Convention |
| --- | --- | --- |
| Arena width | pixels | `960` |
| Arena height | pixels | `540` |
| X axis | pixels | Increases to the right |
| Y axis | pixels | Increases downward |
| Time | seconds | Floating point seconds |
| Position | pixels | `{ x, y }` |
| Velocity | pixels/second | `{ x, y }` |
| Acceleration | pixels/second² | Scalar or vector |
| Angle | radians in code, degrees in design | Degrees may appear in design tables; code converts to radians |
| Fixed simulation step | seconds | `FIXED_DT = 1 / 60` |
| Maximum real-frame delta | seconds | `MAX_FRAME_DT = 1 / 30` |
| Cat radius | pixels | `18` |
| Cat max speed | pixels/second | `260` |
| Cat acceleration | pixels/second² | `2200` |
| Cat friction/deceleration | pixels/second² | `1200` |
| Pounce speed | pixels/second | `520` |
| Pounce duration | seconds | `0.18` |
| Pounce cooldown | seconds | `0.8` |
| Pounce input buffer | seconds | `0.1` |
| Mouse acceleration | pixels/second² | `1800` |
| Mouse emerge duration | seconds | `0.25` |
| Mouse enter duration | seconds | `0.3` |
| Mouse escape time | seconds | `2.5` |
| Startle duration | seconds | `0.3` |
| Startle speed multiplier | multiplier | `1.3` |
| Flee distance | pixels | `140` |
| Separation distance | pixels | `28` |
| Separation weight | scalar | `0.5` |
| Wander interval min | seconds | `0.3` |
| Wander interval max | seconds | `0.6` |
| Max wander turn | degrees | `45` |
| Obstacle lookahead | pixels | `20` |
| Hole radius | pixels | `24` |
| Hole occupied duration | seconds | `0.8` |
| Hole block distance | pixels | `40` |
| Combo window | seconds | `3.0` |
| Combo step | multiplier | `0.25` |
| Max combo multiplier | multiplier | `3.0` |
| Catch base score | points | `100` |
| Pounce catch bonus | points | `50` |
| Fast catch bonus | points | `50` |
| Fast catch time | seconds | `1.0` |
| Multi-catch bonus per extra mouse | points | `100` |
| Level life bonus | points per life | `500` |
| Level perfect bonus | points | `1000` |
| Endless wave number bonus | points per wave | `500` |
| Endless life bonus | points per life | `250` |
| Endless perfect bonus | points | `1000` |
| Initial spawn delay | seconds | `1.0` |
| Level intro duration | seconds | `1.5` |
| Auto-advance duration | seconds | `3.0` |
| Lives | integer | `3` |
| Maximum active mice in Endless | integer | `7` |
| Maximum holes per level | integer | `6` |
| Maximum obstacles per level | integer | `3` |

## 1.2 Important conventions

- The implementation is **vanilla HTML, CSS, and JavaScript only**.
- No Node.js, npm, bundler, build step, external runtime library, physics engine, or pathfinding library is allowed.
- All gameplay code attaches to `window.Game`.
- The only allowed globals are:
  - `window.Game`
  - `window.__game`
  - `window.__test`
  - `window.__testResults`
- The canvas logical coordinate system is always `960 x 540`.
- CSS may scale the canvas visually, but gameplay coordinates never change.
- The simulation uses a fixed timestep of `1 / 60` second.
- Real frame delta is clamped to `1 / 30` second.
- The production loop uses an accumulator:
  ```js
  accumulator += realDt;
  while (accumulator >= FIXED_DT) {
    update(FIXED_DT);
    accumulator -= FIXED_DT;
  }
  ```
- All gameplay randomness uses the seeded RNG in `js/rng.js`.
- No gameplay logic may call `Math.random()` directly.
- Default runtime seed is `Date.now()`.
- Test seed is `1337`.
- Game state returned by `getState()` must be serializable.
- Game state must not contain functions, DOM nodes, audio nodes, or canvas contexts.
- UI must not modify gameplay state directly. UI calls game methods.
- Audio may be disabled in tests, but `lastCue` must still be recorded.
- Catch processing happens before escape processing in the same frame.
- If the target is reached in the same frame that a mouse escapes, level/wave complete wins.
- No external assets are required.
- All tunable gameplay constants live in `js/config.js`.
- All level data lives in `js/levels.js`.
- Endless wave generation lives in `Game.Levels.getEndlessWave`.
- Tests must not use real timers, user input, audio playback, network requests, or rendered pixels.
- Tests may only use `window.__game` and `window.__test`.

# 2. CONTRACTS

## 2.1 Module layout

| File | Responsibility | Tier |
| --- | --- | ---: |
| `index.html` | Loads CSS and scripts, creates canvas and DOM UI, starts game or test mode. | 1 |
| `css/style.css` | Layout, scaling, HUD, menus, overlays, progress bars, life icons, center messages. | 1 |
| `js/config.js` | All tunable constants. | 1 |
| `js/utils.js` | Pure vector and math helpers. | 1 |
| `js/rng.js` | Seeded deterministic RNG. | 1 |
| `js/save.js` | Save load/save/reset with in-memory fallback. | 1 |
| `js/input.js` | Keyboard and mouse input. | 1 |
| `js/audio.js` | WebAudio synthesized cues, music, unlock, panning, ducking. | 1 for SFX, 4 for music polish |
| `js/levels.js` | Campaign levels, endless waves, validation. | 1 for Level 1, 2 for full campaign, 3 for endless |
| `js/collision.js` | Arena clamp and circle-vs-AABB resolution. | 1 |
| `js/entities.js` | Cat, mouse, hole, obstacle factories. | 1 |
| `js/game.js` | Main game object, state machine, update loop, systems. | 1 |
| `js/ui.js` | DOM UI screens and HUD updates. | 1 |
| `js/render.js` | Canvas rendering from state. | 1 |
| `js/main.js` | Bootstrap, loop start, test mode detection, focus loss. | 1 |
| `js/debug.js` | Creates `window.__game`. | 1 |
| `js/test-harness.js` | Creates `window.__test`. | 1 |
| `js/tests.js` | Required tests. | 1+ |

Dropped from engineering: `audio/*.ogg` files. Reason: this spec uses synthesized WebAudio audio and requires no external assets.

## 2.2 Global context

Allowed globals:

```js
window.Game
window.__game
window.__test
window.__testResults
```

`window.Game` contains:

```js
window.Game.config
window.Game.utils
window.Game.RNG
window.Game.Save
window.Game.Input
window.Game.Audio
window.Game.Levels
window.Game.Collision
window.Game.Entities
window.Game.Game
window.Game.UI
window.Game.Render
```

`window.__game` is the debug API.

`window.__test` is the test harness.

`window.__testResults` is set after `window.__test.run()` resolves.

Game state shape returned by `window.__game.getState()`:

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

Mouse record:

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
  holeIndex: -1,
  wanderAngle: 0,
  wanderTimer: 0,
  stuckTimer: 0,
  pendingEscape: false
}
```

Hole record:

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

Obstacle record:

```js
{
  x: 400,
  y: 230,
  width: 160,
  height: 80
}
```

Message record:

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

## 2.3 Module specifics

### `js/config.js`

Required config:

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

  LIVES: 3,

  AUDIO: {
    masterGain: 0.8,
    musicGain: 0.35,
    sfxGain: 0.7,
    duckDb: 3,
    duckReturn: 0.3,
    panScale: 0.7
  },

  VISUAL: {
    wallBorder: 8,
    vignetteOpacity: 0.08,
    shadowOpacity: 0.25,
    obstacleSideHeight: 4,
    obstacleCornerRadius: 4,
    particleLimit: 20,
    maxStarsPerCatch: 4,
    maxDustPerEvent: 5,
    scorePopupLimit: 5,
    effectObscureLimit: 0.1
  }
};

window.Game.config.MICE = {
  normal: { speed: 180, radius: 14 },
  fast:   { speed: 220, radius: 12 },
  big:    { speed: 150, radius: 20 }
};
```

### `js/utils.js`

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

Rules:

- `normalize` returns `{ x: 0, y: 0 }` for zero-length vectors.
- `clampVectorLength` preserves direction and clamps magnitude.
- `deepCopy` must produce plain serializable copies.

### `js/rng.js`

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

Use a small deterministic PRNG such as `mulberry32`.

### `js/save.js`

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

### `js/input.js`

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

### `js/audio.js`

Required API:

```js
window.Game.Audio = {
  init(),
  setEnabled(enabled),
  isEnabled(),
  unlock(),
  play(cue),
  playMusic(track),
  stopMusic(),
  getLastCue()
};
```

Rules:

- Audio is synthesized with WebAudio.
- No external audio files are required.
- `play(cue)` records `lastCue` even when audio is disabled.
- If audio is disabled, no actual playback occurs.
- Audio unlock occurs on first user gesture:
  - keydown
  - mousedown
  - click
- If the AudioContext is suspended, resume it on user interaction.
- Pause all audio when the game pauses.
- Stop gameplay SFX when the browser loses focus.
- Music is Tier 4. If not built, `playMusic` and `stopMusic` may be no-ops, but the API must exist.

### `js/levels.js`

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

Obstacle shape after loading:

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

### `js/collision.js`

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

### `js/entities.js`

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

### `js/game.js`

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
getState()
```

`getState()` must return a serializable deep copy.

### `js/ui.js`

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

### `js/render.js`

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

Fallback visuals are required:

- Arena background: neutral color or Level 1 theme.
- Obstacles: rounded rectangles.
- Holes: dark circles.
- Normal mouse: small gray ellipse.
- Fast mouse: smaller blue-gray ellipse.
- Big mouse: larger dark slate ellipse.
- Cat: orange circle with ears.
- Pouncing cat: slightly stretched shape.

### `js/main.js`

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

### `js/debug.js`

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

See section 8 for the full API.

### `js/test-harness.js`

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

Tests may override save data after reset.

### `js/tests.js`

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

# 3. VISUAL SPEC

The game looks like a bright, warm, slightly frantic domestic arcade scene rendered in soft vector top-down style. The cat is the hero: rounded, orange, confident, and immediately readable. The mice are small, nervous, and easy to track. The arena feels cozy but clear enough for fast top-down chase gameplay. Depth is presented only through small 2.5D cues such as shadows, raised obstacles, and recessed holes. Depth never affects gameplay.

## Lighting and atmosphere

- Lighting is even and warm.
- No harsh shadows.
- No screen shake.
- No full-screen flashes during active gameplay.
- A very soft vignette focuses the center.
- Vignette opacity is about `0.08`.
- Effects are short, localized, and readable.
- Red vignette is used only for mouse escape.
- Gold flash is used only for level/wave complete.
- Dim overlays are used only when gameplay is stopped.

## Space

- Canvas is `960 x 540`.
- No camera scrolling.
- Playable area is the full `960 x 540`.
- Walls are an `8px` visual border inside the canvas.
- Walls do not change collision.
- HUD safe areas:
  - Top HUD: `y = 0` to `y = 68`
  - Bottom HUD: `y = 504` to `y = 540`
  - Center message: centered at `x = 480`, `y = 210`
  - Overlay panels: centered
- Entities may enter HUD safe areas.
- HUD elements must remain sparse and readable.

## Palette

### Core UI and text

| Role | Hex | Usage |
| --- | --- | --- |
| Dark text | `#2F2A25` | Primary text, labels, HUD text |
| Cream panel | `#FFF8EC` | Buttons, panels, UI surfaces |
| Panel border | `#E8DCC8` | Panel and button borders |
| UI accent | `#3FA3A3` | Progress fill, focus, positive UI accents |
| Gold | `#F2B84B` | Combo, score popups, pounce ready, success |
| Warning red | `#E2574C` | Escape, life loss, danger |
| Muted gray | `#9A938B` | Disabled text, secondary text |

### Entity colors

| Entity | Hex | Notes |
| --- | --- | --- |
| Cat body | `#F2A65A` | Orange tabby |
| Cat stripe | `#C96F2E` | Darker orange stripes |
| Cat belly | `#FFF1DC` | Light underside/belly |
| Cat nose | `#F28B82` | Small pink nose |
| Normal mouse | `#8A8F98` | Neutral gray |
| Fast mouse | `#6FA7C7` | Cool blue-gray |
| Big mouse | `#4F5560` | Dark slate, clearly larger |
| Mouse belly | `#D9DDE3` | Light underbelly |
| Hole dark | `#2A1F1A` | Hole interior |
| Hole rim | `#4A362B` | Hole edge |
| Hole highlight | `#F7D9A8` | Subtle rim highlight |

Level backgrounds may use different floor and wall colors, but entity colors stay constant.

## Typography

Use a rounded, friendly sans-serif font.

Recommended font stack:

```css
font-family: "Nunito", "Segoe UI", system-ui, sans-serif;
```

For score and numbers:

```css
font-family: "JetBrains Mono", "Courier New", monospace;
```

| Element | Size | Weight | Notes |
| --- | ---: | ---: | --- |
| Main menu title | 48px | Bold | Uppercase or title case |
| Overlay title | 28px | Bold | Uppercase optional |
| Center gameplay message | 32px | Bold | Short text only |
| Level intro level number | 36px | Bold |  |
| Level intro objective | 20px | SemiBold |  |
| HUD score | 18px | SemiBold | Monospace |
| HUD combo | 16px | Bold | Gold when active |
| HUD level/wave | 12px | SemiBold | Uppercase |
| Progress text | 14px | SemiBold |  |
| Pounce label | 12px | SemiBold | Optional but recommended |
| Button text | 18px | SemiBold |  |
| Small help text | 12px | Normal |  |

All gameplay text should use a soft cream shadow or outline:

```css
text-shadow: 0 1px 0 rgba(255, 248, 236, 0.7), 0 0 4px rgba(255, 248, 236, 0.45);
```

## 2.5D presentation

### Shadows

- Cat and mice have soft elliptical shadows.
- Shadow offset: `2px` down and right.
- Shadow opacity: `0.22` to `0.28`.
- Shadows are non-interactive and do not affect collision.

### Pounce lift

When the cat pounces:

- Cat body stretches in the pounce direction.
- Shadow stretches slightly in the pounce direction.
- Shadow opacity drops to about `0.16` for the first half of the pounce.
- On landing, the cat squashes slightly for `0.05s`.

### Obstacles

Obstacles are raised:

- Top surface is lighter.
- Bottom/right edge is darker.
- Side height: `4px`.
- Corner radius: `4px`.
- Shadow: `3px` offset, opacity `0.20`.

### Holes

Holes are recessed:

- Dark radial interior.
- Thin rim.
- Subtle inner shadow.
- No drop shadow.

## Level themes

| Level | Area | Floor Color | Wall Color | Accent Color | Obstacle Style | Mood |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Kitchen | `#F7E8D2` | `#5B3A29` | `#F2D08A` | None | Bright, open, tutorial |
| 2 | Dining Nook | `#E8C9A0` | `#5B3A29` | `#D98A6A` | Table / rug | Warm, domestic |
| 3 | Living Room | `#D8E8E4` | `#3E4A5A` | `#E7B84C` | Sofa / ottoman | Cozy, playful |
| 4 | Bedroom | `#E5EAF2` | `#4A4A5A` | `#E8A7B5` | Bed / chest | Soft, slightly calmer |
| 5 | Study | `#DDE8D4` | `#3E4A3E` | `#E7B84C` | Bookcase / desk | Neat, slightly busy |
| 6 | Laundry | `#F2F2E8` + checker `#D8E8E4` | `#3E4A5A` | `#6FA7C7` | Baskets / counter | Clean, patterned |
| 7 | Hallway | `#E8D0B0` | `#5B3A29` | `#E7B84C` | Cabinets / shelves | Narrow, directional |
| 8 | Attic | `#D8B890` | `#4A3525` | `#C98A5B` | Crates / barrels | Dusty, enclosed |
| 9 | Basement | `#D8D8D0` | `#3E4A5A` | `#6FA7C7` | Pipes / boxes | Cool, slightly tense |
| 10 | Patio at Dusk | `#E8D8C0` | `#3E4A5A` | `#B57A4C` | Planters / boxes | Final, higher pressure |

Level background rules:

- Floor patterns must be subtle.
- Pattern contrast should be no more than about `8%` to `12%` of the base floor color.
- No floor pattern should resemble a mouse, hole, or UI icon.
- Walls are an `8px` visual border inside the canvas.
- Walls do not change collision.
- Add a very soft vignette, opacity around `0.08`.

Obstacle style notes:

| Level | Obstacle Visual |
| ---: | --- |
| 2 | Wooden table top or rug with subtle border |
| 3 | Rounded sofa cushion or ottoman |
| 4 | Bed edge or wooden chest |
| 5 | Bookcase or desk with low-contrast book spines |
| 6 | Woven basket or laundry counter |
| 7 | Cabinet or shelf with simple door lines |
| 8 | Wooden crate or barrel top |
| 9 | Concrete block or pipe cover |
| 10 | Stone planter or wooden box |

Keep prop details low-contrast. Details should not create false edges that look like holes or mice.

## Entity visuals

### Cat

- Gameplay radius: `18px`.
- Visual bounding size: about `40 x 40px`.
- Body should appear slightly larger than the collision radius because of shadow and tail.
- Orange tabby cat.
- Rounded body.
- Two triangular ears.
- Curved tail.
- Four small paws visible from top-down.
- Simple face: two dark eyes, small pink nose.
- Darker orange stripes on back.

Cat color details:

- Body: `#F2A65A`
- Stripes: `#C96F2E`
- Belly/face light: `#FFF1DC`
- Eyes: `#2B2B2B`
- Nose: `#F28B82`
- Outline: optional `1px` darker orange `#B85F22`, opacity `0.35`

### Mice

| Mouse Type | Gameplay Radius | Visual Size | Notes |
| --- | ---: | ---: | --- |
| Normal | `14px` | about `28 x 20px` | Standard prey |
| Fast | `12px` | about `24 x 17px` | Smaller, sleeker |
| Big | `20px` | about `38 x 30px` | Larger, chunkier |

| Mouse | Color | Shape | Animation | Special Visual |
| --- | --- | --- | --- | --- |
| Normal | Gray `#8A8F98` | Round body, small ears, thin tail | Standard run cycle | None |
| Fast | Blue-gray `#6FA7C7` | Sleeker body, smaller ears, stiffer tail | Faster run cycle, small speed lines when moving fast | Cyan streak behind when speed > `150px/s` |
| Big | Dark slate `#4F5560` | Chunkier body, thicker tail, larger head | Slower, heavier run cycle | Small gold paw badge on back |

Big mouse telegraph:

- Larger body.
- Darker color.
- Thick tail.
- Small gold paw badge on the back.
- When the cat is not pouncing, the paw badge can pulse very subtly.
- When the cat is pouncing, the paw badge glows brighter.

Mouse face:

- Two dark eyes.
- Small pink nose.
- When startled: eyes become larger white circles with small black pupils.
- When caught: eyes become `x x` or curved happy lines, depending on tone. Keep it playful, not violent.

### Holes

- Gameplay radius: `24px`.
- Visual size: `48 x 48px`.
- Interior: dark radial gradient.
- Rim: `4px` thick.
- Rim color: `#4A362B`.
- Highlight: thin `1px` arc on top-left, color `#F7D9A8`, opacity `0.35`.

Hole states:

| State | Visual |
| --- | --- |
| Empty | Dark circle with rim |
| Spawn | Mouse emerges, small dust puff, brief ripple |
| Occupied | Teal swirl inside hole for `0.8s` |
| Blocked by cat | Gold rim glow and small paw print on rim |
| Escape | Mouse sinks, ripple expands, dust puff |

Blocked hole visual:

When the cat is within `40px` of the hole center:

- Hole rim glows gold.
- A small paw print appears on the rim.
- The paw print remains while the cat is blocking.
- If the cat pounces over the hole, the paw print can briefly enlarge.

Occupied hole visual:

When a mouse is entering:

- Teal swirl or circular ripple.
- No other mouse can visually appear to enter.
- Swirl lasts `0.8s`, matching occupied timer.

## HUD layout

### Top left

Position:

```text
Score:      x = 16, y = 12
Combo:      x = 16, y = 36
Level/Wave: x = 16, y = 56
```

Score:

- Font: `18px` monospace.
- Color: `#2F2A25`.
- Format:
  ```text
  Score 000000
  ```

Combo:

- Font: `16px` bold.
- Color: `#F2B84B`.
- Show only when combo multiplier is greater than `1.0`.
- Format:
  ```text
  Combo x1.25
  ```

When combo is active:

- Text pulses once on each catch.
- When combo resets, text fades out over `0.2s`.

Level or wave:

- Font: `12px` semiBold uppercase.
- Color: `#2F2A25` at `60%` opacity.
- Campaign:
  ```text
  LEVEL 3
  ```
- Endless:
  ```text
  WAVE 5
  ```

### Top center

Position:

```text
Progress text: centered at x = 480, y = 10
Progress bar:  x = 360, y = 28, width = 240, height = 12
```

Progress text:

- Font: `14px` semiBold.
- Color: `#2F2A25`.
- Format:
  ```text
  Caught 7/10
  ```

Progress bar:

- Background: `#E8DCC8`
- Fill: `#3FA3A3`
- Corner radius: `6px`
- Fill amount: `caught_count / target_catches`
- Clamp between `0` and `1`.
- When complete, fill becomes `#F2B84B`.
- On catch, the bar pulses once with a `0.15s` ease-out fill animation.

### Top right

Position:

```text
Lives:  x = 830, y = 22
Pause:  x = 912, y = 16, width = 32, height = 32
```

Lives:

- Display three mouse head icons.
- Icon size: `20 x 20px`.
- Spacing: `8px`.
- Full life: gray mouse head, color `#8A8F98`.
- Lost life: outline only, color `#C9C9C9`, opacity `0.7`.
- When a life is lost:
  - Icon cracks briefly.
  - Icon fades to lost state over `0.3s`.
  - A small red flash appears on the icon.

Pause button:

- Size: `32 x 32px`.
- Corner radius: `8px`.
- Background: `#FFF8EC` at `90%` opacity.
- Border: `#E8DCC8`.
- Icon: two vertical bars, color `#2F2A25`.
- Hover: background becomes `#3FA3A3`, icon becomes `#FFF8EC`.
- Focus: `3px` outline `#3FA3A3`.

### Bottom center

Position:

```text
Label: centered at x = 480, y = 504
Bar:   x = 420, y = 520, width = 120, height = 8
```

Pounce label:

- Font: `12px` semiBold.
- Color: `#2F2A25` at `70%` opacity.
- Text:
  ```text
  Pounce
  ```

Pounce bar:

- Background: `#E8DCC8`
- Fill: `#F2B84B`
- Corner radius: `4px`
- Fills left to right as pounce becomes ready.
- When full:
  - Fill pulses gently.
  - Optional small glow.
- When pounce is buffered:
  - Bar flashes white once for `0.1s`.

### Center screen messages

Position:

```text
Center point: x = 480, y = 210
```

Messages are non-interactive.

Message rules:

- Only one message at a time.
- Higher priority replaces lower priority.
- Duration: `1.0s` to `1.5s`.
- Fade in: `0.15s`.
- Hold: `0.8s` to `1.0s`.
- Fade out: `0.25s`.
- No background panel during active gameplay.
- Use large text with cream shadow.

Message priority:

| Priority | Message | Color | Duration |
| ---: | --- | --- | ---: |
| 1 | Game Over | Use overlay, not center message | — |
| 2 | Level Complete | Use overlay, not center message | — |
| 3 | Wave Complete | Use overlay, not center message | — |
| 4 | Mouse escaped! | `#E2574C` | `1.0s` |
| 5 | New mouse type: Fast / Big | `#3FA3A3` | `1.2s` |
| 6 | Level X / Wave X | `#2F2A25` | `1.0s` |

Example messages:

```text
Level 3
Wave 5
Mouse escaped!
New mouse type: Fast
New mouse type: Big
```

## UI components

### Buttons

Default button:

- Width: `180px`
- Height: `44px`
- Corner radius: `10px`
- Background: `#FFF8EC`
- Border: `2px` `#E8DCC8`
- Text: `#2F2A25`
- Font: `18px` semiBold

Button states:

| State | Visual |
| --- | --- |
| Default | Cream background, dark text |
| Hover | Background `#3FA3A3`, text `#FFF8EC`, button lifts `2px` |
| Pressed | Button drops `2px` |
| Focus | `3px` outline `#3FA3A3`, offset `2px` |
| Disabled | Background `#E8E2D8`, text `#9A938B`, no hover |

Primary button:

Use primary style for main actions:

- Play
- Retry
- Resume
- Next Level
- Play Endless

Primary hover:

- Success/progress: gold `#F2B84B` with dark text.
- Neutral/system: teal `#3FA3A3`.

### Panels

Overlay panels:

- Background: `#FFF8EC` at `95%` opacity.
- Border: `2px` `#E8DCC8`.
- Corner radius: `16px`.
- Shadow: soft drop shadow, opacity `0.18`.
- Width: usually `420px`.
- Height: `240px` to `300px` depending on content.

Dim background behind panels:

```text
rgba(31, 26, 22, 0.45)
```

Game over uses a slightly darker dim:

```text
rgba(31, 26, 22, 0.55)
```

### Icons

| Icon | Size | Use |
| --- | ---: | --- |
| Mouse head | `20 x 20px` | Lives, objective, progress |
| Paw print | `16 x 16px` | Pounce, Big mouse badge, blocked hole |
| Pause | `20 x 20px` | Pause button |
| Lock | `16 x 16px` | Locked Endless button |
| Star | `12 x 12px` | Catch particles, score feedback |
| Speed line | vector | Fast mouse, pounce feedback |

## State-by-state visuals

### Main menu

- Background: Level 1 Kitchen theme, dimmed `20%`.
- Optional subtle animation: cat tail wags, mouse icon peeks from a hole.
- Title centered at `x = 480, y = 120`.
- Buttons centered vertically.

Content:

```text
Cat: Mice Hunt
Play
Endless
How to Play
```

Button positions:

```text
Play:        centered at x = 480, y = 260
Endless:     centered at x = 480, y = 320
How to Play: centered at x = 480, y = 380
```

Button size: `200 x 48px`.

Endless button:

- If unlocked: normal button.
- If locked: disabled button with lock icon.
- Locked text:
  ```text
  Endless
  ```
- Small helper text below button, optional:
  ```text
  Complete Level 10
  ```

### How to Play

- Panel: `560 x 360px`, centered.
- Title: `How to Play`.
- Back button bottom-right.

Content:

```text
Move: WASD or Arrow Keys
Pounce: Space or Left Click

Catch mice before they hide.
Mice can hide in holes after 2.5 seconds.
Pounce to catch Big mice.
Catch mice quickly to build combo.
Do not let 3 mice escape.
```

Mouse type row:

- Normal mouse icon: `Normal: Standard mouse.`
- Fast mouse icon: `Fast: Faster, smaller mouse.`
- Big mouse icon: `Big: Can only be caught while pouncing.`

### Level intro

Duration: `1.5s`.

The arena is visible and the cat is controllable. No mice spawn.

Layout:

```text
Area name:   centered at x = 480, y = 150
Level:       centered at x = 480, y = 190
Objective:   centered at x = 480, y = 235
Lives:       centered at x = 480, y = 270
New type:    centered at x = 480, y = 310
```

Content:

```text
Kitchen
Level 1
Catch 5 mice
[3 mouse head icons]
```

If a new mouse type appears:

```text
New mouse type: Fast
```

or:

```text
New mouse type: Big
```

Visual notes:

- Area name uses the level accent color.
- Level number is large and bold.
- Objective includes a small mouse icon before the text.
- New mouse type appears with the corresponding mouse icon.
- No large panel. Use text with cream shadow.
- Fade in: `0.2s`, fade out: `0.2s`.

### Playing

During active gameplay:

- HUD is visible.
- Center messages appear only for important events.
- No overlay panels.
- No large background changes.
- Cat, mice, holes, and obstacles remain fully visible.

### Paused

- Dim background: `rgba(31, 26, 22, 0.45)`.
- Panel: `360 x 260px`, centered.
- Title: `Paused`.

Buttons:

```text
Resume
Restart
Main Menu
```

Button size: `180 x 44px`.

Behavior:

- All gameplay animation stops.
- Music pauses or lowers to a muted drone if music is built.
- SFX stop.
- Pause button in HUD is replaced by panel buttons.

### Level complete

- Dim background.
- Panel: `420 x 280px`, centered.
- Title: `Level X Complete`.
- Gold accent underline or small star icon.

Content:

```text
Level 3 Complete
Score: 004500
Life bonus: 1500
Clean bonus: 1000
Bonus: 2500
High Score: 005200
Next Level
```

If no clean bonus, omit that line.

If high score is new:

- Show gold badge:
  ```text
  New High Score
  ```

Auto progress:

- Text below button:
  ```text
  Next in 3
  ```
- Small progress bar: `120 x 6px`, fills over `3s`.
- Player can click Next immediately.

### Campaign complete

- Dim background.
- Panel: `420 x 300px`, centered.
- Title: `Campaign Complete`.
- Small celebratory particles: gold stars, max `12`, slow drift.

Content:

```text
Campaign Complete
Score: 012500
High Score: 012500
Endless Unlocked
Play Endless
Main Menu
```

Endless unlocked:

- Show a small lock icon breaking open or a gold badge.
- Keep it simple; no long animation.

### Game over

- Dim background slightly darker than pause: `rgba(31, 26, 22, 0.55)`.
- Panel: `420 x 260px`, centered.
- Title: `Game Over`.
- Use warning red accent, but keep it soft.

Content:

```text
Game Over
Level 3
Score: 004200
Retry Level
Main Menu
```

Mood:

- No harsh visual punishment.
- No red flashing.
- Optional small mouse icon slipping into a hole.

### Endless wave complete

- Dim background.
- Panel: `420 x 280px`, centered.
- Title: `Wave X Complete`.

Content:

```text
Wave 5 Complete
Score: 018400
Wave bonus: 2500
Life bonus: 750
Clean bonus: 1000
Bonus: 4250
Next Wave in 3
```

Auto progress:

- Progress bar fills over `3s`.
- No button required, but optional `Next Wave` button can appear.

### Endless game over

Same as Game Over, but title context changes.

Content:

```text
Game Over
Wave 5
Score: 021300
Retry Wave
Main Menu
```

## Gameplay feedback

Feedback should be immediate, localized, and short.

### Pounce

When the cat pounces:

- Cat stretches.
- Shadow stretches.
- 2-3 dust puffs at start.
- 2-3 dust puffs at landing.
- Speed lines in pounce direction.
- Pounce bar flashes if input was buffered.

Duration:

- Pounce animation matches `0.18s` pounce duration.
- Landing squash: `0.05s`.

### Catch

When a mouse is caught:

- Mouse disappears into a small fur puff.
- 3-4 gold stars appear.
- Score popup appears at mouse position.
- Cat does a brief happy face.
- Progress bar pulses.
- Combo text pulses if active.

Score popup:

- Font: `14px` bold.
- Color: `#F2B84B` for bonus points, `#2F2A25` for base points.
- Animation: rise `20px`, fade over `0.8s`.
- Show final points after combo multiplier.

Examples:

```text
+100
+150
+200
```

If a pounce or quick bonus applies, the popup can be gold. No need to show every bonus reason as text.

### Multi-catch

If multiple mice are caught in the same catch event:

- Each mouse gets its own score popup.
- One additional gold text appears near the cat:
  ```text
  MULTI +100
  ```
- Multi-catch chime plays.
- Slight gold flash on the progress bar.

### Combo

Combo is shown in the top left.

When combo increases:

- Combo text pulses.
- Color remains gold.
- Optional small star sparkle near combo text.

When combo resets:

- Combo text fades out.
- No large punishment effect.

No combo milestone audio.

### Mouse escape

When a mouse escapes:

- Mouse sinks into hole.
- Hole ripple expands.
- Small dust puff.
- Red center message:
  ```text
  Mouse escaped!
  ```
- One life icon cracks and fades.
- Soft red vignette pulse around screen edges for `0.2s`, opacity `0.12`.
- Combo resets visually.

No screen shake.

### Big mouse startle

When a Big mouse is touched by a non-pouncing cat:

- Big mouse flashes white for `0.08s`.
- Eyes become wide.
- Tail puffs.
- Small speed lines appear.
- Startle squeak plays.
- Mouse moves away faster.

No catch occurs.

### Hole blocked

When the cat blocks a hole:

- Hole rim glows gold.
- Paw print appears on rim.
- Mice seeking that hole should visibly avoid it.

No text.

### Hole occupied

When a mouse enters a hole:

- Teal swirl appears.
- Other mice avoid the hole.
- Swirl lasts `0.8s`.

### Spawn

When a mouse emerges:

- Small dust puff.
- Mouse scales from `0.4` to `1.0`.
- Shadow appears.
- No warning icon needed.

## Particles and screen effects

Particle limits:

- Maximum active particles: `20`.
- Maximum stars per catch: `4`.
- Maximum dust puffs per event: `5`.
- Particles should not obscure mice or holes for more than `0.1s`.

Particle types:

| Effect | Color | Duration |
| --- | --- | ---: |
| Dust puff | `#D9C8A8` | `0.3s` |
| Catch stars | `#F2B84B` | `0.4s` |
| Escape dust | `#C9C9C9` | `0.4s` |
| Pounce dust | `#D9C8A8` | `0.25s` |
| Red vignette | `#E2574C` | `0.2s` |
| Gold success flash | `#F2B84B` | `0.2s` |

Screen effects:

- No screen shake.
- No full-screen flashes during active gameplay.
- Red vignette only on escape.
- Gold flash only on level/wave complete.
- Dim overlays only when gameplay is stopped.

## Visual rules that imply gameplay rules

| Visual | Implied gameplay rule |
| --- | --- |
| Blocked hole gold rim and paw print | Cat within `40px` of hole center blocks that hole. |
| Occupied hole teal swirl for `0.8s` | Hole is occupied for `0.8s` after a mouse begins entering. |
| Emerging mouse scale/alpha over `0.25s` | Mouse is not catchable while emerging. |
| Entering mouse scale down and sink over `0.3s` | Mouse is still catchable while entering. |
| Big mouse paw badge | Big mouse can only be caught while cat is pouncing. |
| Big mouse badge glows while pouncing | Pounce is the required catch condition for Big mice. |
| Fast mouse streak above `150px/s` | Fast mouse speed is `220px/s`. |
| Mouse escape red vignette | Escape costs 1 life. |
| Life icon crack/fade | Life was lost. |
| Pounce bar fill | Pounce cooldown is ready when full. |
| Progress bar fill | Fill is `caught / target`, clamped `0` to `1`. |

# 4. GAMEPLAY SPEC

The game is a short, complete 2D top-down arcade chase. The player controls a fast, playful cat in a fixed single-screen arena. Mice emerge from holes, flee from the cat, and try to escape back into holes. The cat wins by catching the required number of mice before three mice escape. The core fantasy is that the cat is fast and slightly overconfident, while the mice are small, nervous, and always trying to get away. The core tension is: can you catch the mouse before it disappears?

## Records and rosters

### Records

| Record | Purpose |
| --- | --- |
| Cat | Player-controlled entity |
| Mouse | Active prey entity |
| Hole | Spawn and escape point |
| Obstacle | Solid rectangle |
| Level | Campaign level data |
| Wave | Endless wave data |
| Message | Temporary center-screen message |
| Save | Persistent high scores and unlock |

### Mouse type roster

| Mouse Type | Speed | Radius | Special |
| --- | ---: | ---: | --- |
| Normal | 180 | 14 | None |
| Fast | 220 | 12 | Moves faster |
| Big | 150 | 20 | Can only be caught while the cat is pouncing |

All mice:

- Acceleration: `1800 pixels/second²`
- Can be caught by normal contact unless they are Big mice.
- Can escape into holes after `2.5 seconds`.
- Cannot enter a blocked hole.
- Cannot enter an occupied hole.

### Level roster

See 4.18 Level Content.

### Endless wave roster

See 4.19 Endless Mode.

## 4.1 Game state system

Tier: 1 for core screens, 2 for campaign complete screens, 3 for endless screens.

The game must support these screens:

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

### Main menu

Content:

- Title.
- Play button.
- Endless button, only if unlocked.
- How to Play button.

Behavior:

- Play starts Level 1 with score 0.
- Endless starts Wave 1 with score 0.
- How to Play opens the How to Play screen.

### How to Play

Content:

- Controls.
- Objective.
- Mouse types.
- Pounce explanation.
- Combo explanation.

Behavior:

- Back button returns to Main Menu.

### Level intro

Duration: `1.5 seconds`.

Content:

- Level number.
- Target number.
- Lives.
- New mouse type, if applicable.
- Short objective text.

Behavior:

- Cat is controllable.
- No mice spawn during intro.
- After intro, the level enters the Playing state.
- First mouse spawns `1.0 seconds` after intro ends.

### Playing

Behavior:

- Cat can move and pounce.
- Mice update.
- Spawning occurs.
- Catching and escaping occur.
- HUD updates.

### Paused

Triggered by:

- Esc
- P
- Browser losing focus
- Pause button

Content:

- Paused text.
- Resume button.
- Restart button.
- Main Menu button.

Behavior:

- All gameplay timers stop.
- No spawning.
- No mouse movement.
- No score changes.
- No life changes.
- No auto-advance.

Pause can occur from:

```text
levelIntro
playing
levelComplete
endlessWaveComplete
```

### Level complete

Triggered when:

```text
caught_count >= target_catches
```

Content:

- Level number.
- Score.
- Bonus breakdown.
- High score if updated.
- Next Level button or automatic progression.

Behavior:

- Gameplay stops.
- After `3 seconds`, automatically start next level.
- Player can also press Next immediately.
- If Level 10 is complete, go to Campaign Complete.

### Campaign complete

Triggered after Level 10.

Content:

- Campaign Complete text.
- Final score.
- High score.
- Play Endless button.
- Main Menu button.

Behavior:

- Marks Endless Mode as unlocked.
- Saves high score.

### Game over

Triggered when:

```text
lives <= 0
```

and target was not reached.

Content:

- Game Over text.
- Level number.
- Score.
- Retry Level button.
- Main Menu button.

Behavior:

- Retry restarts the same level.
- Score resets to the score at the start of that level.
- Lives reset to 3.

### Endless wave complete

Triggered when:

```text
caught_count >= target_catches
```

in Endless Mode.

Content:

- Wave number.
- Score.
- Bonus breakdown.
- Next Wave in 3 seconds.

Behavior:

- Gameplay stops.
- After `3 seconds`, start next wave.
- Score carries forward.
- Lives reset to 3.

### Endless game over

Triggered when:

```text
lives <= 0
```

in Endless Mode.

Content:

- Game Over text.
- Wave number.
- Score.
- Retry Wave button.
- Main Menu button.

Behavior:

- Retry Wave restarts the same wave.
- Score resets to the score at the start of that wave.
- Lives reset to 3.

## 4.2 Cat movement

Tier: 1.

Cat properties:

- Radius: `18 pixels`
- Max speed: `260 pixels/second`
- Acceleration: `2200 pixels/second²`
- Friction/deceleration: `1200 pixels/second²`
- Pounce speed: `520 pixels/second`
- Pounce duration: `0.18 seconds`
- Pounce cooldown: `0.8 seconds`
- Input buffer for pounce: `0.1 seconds`

The cat can:

- Move in 2D.
- Pounce in the current movement direction.
- Catch mice by contact.
- Temporarily block holes by standing near them.

The cat does not have health. Lives are based on escaped mice.

Movement:

```text
input = normalized movement input vector

if pounce_pressed and pounce_cooldown <= 0:
    start pounce

if pounce_timer > 0:
    cat.velocity = pounce_direction * 520
    pounce_timer -= dt
else:
    if input.length > 0:
        cat.velocity += input * 2200 * dt
        last_direction = input
    else:
        cat.velocity = move_toward(cat.velocity, 0, 1200 * dt)

    cat.velocity = clamp_length(cat.velocity, 260)

cat.position += cat.velocity * dt
resolve_collisions(cat)

pounce_cooldown = max(0, pounce_cooldown - dt)
```

Pounce direction:

- If the player is currently moving, pounce in the movement direction.
- If the player is not moving, pounce in the last movement direction.
- If the cat has never moved, pounce to the right.

Pounce buffer:

- If the player presses pounce while the cooldown is still active, store the input for `0.1 seconds`.
- If the cooldown becomes ready within that window, execute the pounce.

Pounce readiness for HUD:

```text
if pounceCooldown <= 0:
    pounceReadiness = 1
else:
    pounceReadiness = 1 - pounceCooldown / 0.8
```

Clamp readiness between `0` and `1`.

## 4.3 Mouse AI

Tier: 1 for Normal mice and base AI, Tier 2 for Fast and Big behavior.

Mouse active states:

1. `emerging`
2. `fleeing`
3. `entering`

`caught` and `escaped` are event outcomes, not active states.

### Emerging

A mouse begins in the `emerging` state when it spawns.

- Duration: `0.25 seconds`
- Mouse does not move.
- Mouse is not catchable during this state.
- After the timer ends, the mouse becomes `fleeing`.
- `outTime` starts at `0` when fleeing begins.

### Fleeing

This is the normal active state.

The mouse:

- Moves away from the cat.
- Wanders slightly.
- Tries to find a hole after `2.5 seconds`.
- Avoids obstacles.
- Avoids overlapping other mice.
- Can be caught by contact.

Fleeing behavior:

- If the cat is within `140 pixels`, the mouse strongly flees away from the cat.
- If the cat is farther than `140 pixels`, the mouse wanders more.
- After `2.5 seconds` out, the mouse begins seeking the nearest available hole.
- The hole-seeking weight increases the longer the mouse is out.

Wander behavior:

- Each mouse has a wander direction.
- Every `0.3` to `0.6 seconds`, the mouse changes its wander direction by a random angle between `-45 degrees` and `+45 degrees`.

Separation behavior:

- If another mouse is within `28 pixels`, the mouse moves away from it.
- Separation weight is `0.5`.
- Do not separate against `emerging` or `entering` mice.

### Entering hole

A mouse enters this state when it decides to escape.

- Duration: `0.3 seconds`
- The mouse moves slightly toward the hole center.
- The hole becomes occupied for `0.8 seconds`.
- The mouse is still catchable during this state.
- If caught during this state, the mouse is caught and does not escape.
- If the timer ends, the mouse escapes.

A mouse may enter a hole if:

```text
state === "fleeing"
and outTime >= 2.5
and startleTimer <= 0
and distance(mouse, hole) <= 24
and hole.occupiedTimer <= 0
and hole is not blocked
```

When entering:

```text
state = "entering"
enterTimer = 0.3
holeIndex = index
hole.occupiedTimer = 0.8
pendingEscape = false
```

While entering:

```text
enterTimer -= dt
move slightly toward hole center at 60 px/s
resolveEntity(mouse, obstacles)
```

If `enterTimer <= 0`:

```text
pendingEscape = true
```

Removal happens in escape processing after catch processing.

## 4.4 Collision system

Tier: 1.

All collisions are 2D circle-based.

### Circle vs arena bounds

Clamp each entity:

```text
x = clamp(x, radius, 960 - radius)
y = clamp(y, radius, 540 - radius)
```

### Circle vs obstacle AABB

For each obstacle:

```text
closest_x = clamp(circle.x, obstacle.x, obstacle.x + obstacle.width)
closest_y = clamp(circle.y, obstacle.y, obstacle.y + obstacle.height)

dx = circle.x - closest_x
dy = circle.y - closest_y
distance = sqrt(dx*dx + dy*dy)

if distance < circle.radius:
    push circle out along (dx, dy)
```

If `distance == 0`, push the circle out using the smallest axis overlap.

If there is a tie, push upward first.

Resolve obstacles twice per frame for each entity for stability.

### Catch collision

A mouse is caught if:

```text
distance(cat_position, mouse_position) < cat.radius + mouse.radius
```

Catchable mouse states:

- `fleeing`
- `entering`

Not catchable states:

- `emerging`
- removed caught/escaped outcomes

## 4.5 Hole system

Tier: 1.

Each hole has:

- Position: `x, y`
- Radius: `24`
- Occupied timer: starts at `0`
- Blocked state: calculated from cat position or debug override

### Hole occupancy

When a mouse begins entering a hole:

```text
hole.occupiedTimer = 0.8
```

While `occupiedTimer > 0`, no other mouse can enter that hole.

The occupied timer continues even if the mouse is caught during entry.

### Hole blocking

A mouse cannot enter a hole if:

```text
distance(cat_position, hole.position) <= 40
```

The cat does not need a special action to block a hole. Standing near the hole is enough.

If `hole.blockedOverride` is set by debug, use that value instead of the computed blocked state.

## 4.6 Spawning system

Tier: 1 for normal spawning, Tier 2 for full mouse mixes.

Mice spawn from holes.

### Spawn conditions

A mouse can spawn if:

- The level is in the `playing` state.
- `caught_count < target_catches`
- `active_mouse_count < max_active_mice`
- `spawn_timer <= 0`
- At least one hole is available.

A hole is available for spawning if:

```text
hole.occupiedTimer <= 0
and distance(cat_position, hole.position) > 40
```

### Spawn timer

At the start of a level:

```text
spawn_timer = 1.0
```

After each spawn:

```text
spawn_timer = level.spawn_interval
```

If no hole is available, the spawn timer keeps counting down, but spawning is delayed until a hole becomes available.

### Mouse type selection

Use the level’s mouse mix weights.

Example:

```text
Normal: 50
Fast: 30
Big: 20
```

To choose a mouse:

```text
total = sum(weights)
random_value = random(0, total)

subtract weights until random_value falls below a weight
```

If `pickWeighted` returns `null`, do not spawn.

Spawn position:

- Hole center.
- State: `emerging`.
- `emergeTimer = 0.25`.
- `outTime = 0`.
- Velocity zero.

## 4.7 Catching system

Tier: 1 for normal catching, Tier 2 for Big mouse rules.

When the cat touches a catchable mouse:

1. Set mouse state to caught outcome.
2. Remove the mouse from the active mouse list.
3. Increase `caught_count` by 1.
4. Add score.
5. Update combo.
6. Play catch audio cue.
7. If `caught_count >= target_catches`, trigger level complete.

### Normal catch

A Normal or Fast mouse can be caught by any cat contact.

### Big mouse catch

A Big mouse can only be caught if:

```text
cat.pounce_timer > 0
```

If the cat touches a Big mouse while not pouncing:

- No catch occurs.
- The mouse becomes startled for `0.3 seconds`.
- While startled:
  - Its max speed is multiplied by `1.3`.
  - It cannot seek holes.
  - It continues fleeing from the cat.
- Play startle audio cue.

## 4.8 Escape system

Tier: 1.

A mouse escapes when it completes entering a hole.

When a mouse escapes:

1. Set mouse state to escaped outcome.
2. Remove the mouse from the active mouse list.
3. Decrease `lives` by 1.
4. Reset combo to 0.
5. Play escape audio cue.
6. Show center message `Mouse escaped!`.
7. If `lives <= 0`, trigger game over.

Escape processing happens after catch processing.

If multiple mice escape in the same frame:

- Each mouse reduces lives by 1.
- If lives become 0 or below, trigger game over.

## 4.9 Lives system

Tier: 1.

Each level starts with:

```text
lives = 3
```

Each escaped mouse reduces lives by 1.

If lives reach 0, the level fails.

Lives reset to 3 at the start of each level and each endless wave.

## 4.10 Scoring system

Tier: 1 for base score, Tier 2 for full campaign bonuses.

Score is used for high scores and light competitive feedback.

### Catch score

For each caught mouse:

```text
base_points = 100
bonus_points = 0

if cat.pounce_timer > 0:
    bonus_points += 50

if mouse.out_time < 1.0:
    bonus_points += 50

points = base_points + bonus_points
score += floor(points * combo_multiplier)
```

`mouse.out_time` is the time spent in `fleeing` state.

### Multi-catch bonus

If the cat catches multiple mice in the same frame or catch event:

```text
multi_catch_bonus = 100 * (number_of_mice_caught - 1)
score += multi_catch_bonus
```

This bonus is added once per catch event, not per mouse.

### Level complete bonus

When a level is completed:

```text
bonus = lives * 500

if escapes_in_level == 0:
    bonus += 1000

score += bonus
```

### Endless wave bonus

When an endless wave is completed:

```text
bonus = wave_number * 500
bonus += lives * 250

if escapes_in_wave == 0:
    bonus += 1000

score += bonus
```

## 4.11 Combo system

Tier: 1.

Combo increases when the player catches mice quickly.

Rules:

- `combo` starts at 0.
- On each catch:
  - If time since last catch is less than or equal to `3.0 seconds`, increase combo by 1.
  - Otherwise, set combo to 1.
- Combo multiplier:

```text
combo_multiplier = 1.0 + 0.25 * (combo - 1)
combo_multiplier = min(3.0, combo_multiplier)
```

- If a mouse escapes, combo resets to 0.
- If no catch occurs for `3.0 seconds`, combo resets to 0.
- Combo resets at level/wave start.

## 4.12 Level progression

Tier: 2 for full campaign, Tier 1 for Level 1 playable loop.

The campaign consists of `10 levels`.

After completing Level 10, the player unlocks Endless Mode.

Campaign flow:

1. Main Menu.
2. Player presses Play.
3. Level 1 starts.
4. Level intro.
5. Gameplay.
6. Level complete.
7. Next level starts automatically after a short delay.
8. Repeat until Level 10.
9. Campaign complete.
10. Endless Mode unlocked.

Failure flow:

If the player fails a level:

1. Show Game Over.
2. Offer Retry Level.
3. Retry restarts the same level.
4. Score resets to the score at the start of that level.
5. Lives reset to 3.

No level select screen.

## 4.13 Endless mode

Tier: 3.

Endless Mode unlocks after completing Level 10.

Endless Mode is a separate score track.

### Endless structure

Endless Mode is divided into waves.

Each wave:

- Uses a layout.
- Has a target number of mice.
- Starts with 3 lives.
- Has its own spawn interval and max active mice.
- Has its own mouse mix.
- Carries score forward to the next wave.

If the player fails a wave:

- The wave can be retried.
- Score resets to the score at the start of that wave.
- Lives reset to 3.

### Endless wave layouts

Endless waves rotate through these layouts:

```text
Wave 1: Level 10 layout
Wave 2: Level 9 layout
Wave 3: Level 8 layout
Wave 4: Level 10 layout
Wave 5: Level 9 layout
...
```

Formula:

```text
layout_index = [10, 9, 8][(wave_number - 1) % 3]
```

Use the holes and obstacles from the selected level layout.

### Endless wave parameters

For wave number `w`:

```text
target = min(50, 15 + 5 * (w - 1))

spawn_interval = max(0.6, 1.0 - 0.05 * (w - 1))

max_active = min(7, 4 + floor((w + 1) / 2))

lives = 3
```

### Endless mouse mix

Use weighted random selection:

```text
normal_weight = max(10, 40 - 2 * (w - 1))
fast_weight = 35 + 2 * (w - 1)
big_weight = 25 + 2 * (w - 1)
```

Normalize the weights before choosing a mouse.

### Endless progression

- Score carries between waves.
- Lives reset to 3 each wave.
- Combo resets each wave.
- Wave complete bonus is added.
- Next wave starts automatically after `3 seconds`.
- There is no separate endless wave intro screen.
- Show center message `Wave X` when the wave starts.

## 4.14 HUD system

Tier: 1.

The HUD must always show the player’s current objective, score, lives, and pounce availability during active play.

### Top left

Display:

```text
Score: 000000
Combo: x1.25
Level 3
```

or, in Endless Mode:

```text
Score: 000000
Combo: x1.25
Wave 5
```

Rules:

- Score is always shown.
- Combo is shown only when combo multiplier is greater than `1.0`.
- Level or Wave is always shown.

### Top center

Display progress:

```text
Caught: 7 / 10
```

Also display a progress bar.

Progress bar rules:

- Fills from left to right.
- Fill amount = `caught_count / target_catches`
- Clamp fill between `0` and `1`.

### Top right

Display lives:

- Show 3 mouse icons.
- Full icons represent remaining lives.
- Empty or greyed icons represent lost lives.

Also display pause button:

```text
II
```

### Bottom center

Display pounce cooldown:

- A horizontal bar.
- Width: `120 pixels`
- Height: `8 pixels`
- Fills from left to right as pounce becomes ready.
- When full, pounce is ready.

Optional label:

```text
Pounce
```

### Center screen messages

Show temporary center messages for major events.

Examples:

- `Level 3`
- `Catch 10 mice`
- `New mouse type: Fast`
- `Mouse escaped!`
- `Level Complete`
- `Game Over`
- `Wave 5`
- `Next wave in 3`

Rules:

- Messages should not block gameplay.
- Duration: `1.0` to `1.5 seconds`
- Only one message at a time.
- Higher priority messages replace lower priority ones.

Priority order:

1. Game Over
2. Level Complete
3. Wave Complete
4. Mouse escaped
5. New mouse type
6. Level/Wave start

## 4.15 UI flow system

Tier: 1 for core flow, 2 for campaign complete, 3 for endless.

### Main menu

Content:

- Game title.
- Play.
- Endless, if unlocked.
- How to Play.

Behavior:

- Play starts Level 1.
- Endless starts Wave 1.
- How to Play opens instructions.

### How to Play

Content:

```text
Move: WASD or Arrow Keys
Pounce: Space or Left Click

Catch mice before they hide.
Mice can hide in holes after 2.5 seconds.
Pounce to catch Big mice.
Catch mice quickly to build combo.
Do not let 3 mice escape.
```

Mouse type descriptions:

```text
Normal: Standard mouse.
Fast: Faster, smaller mouse.
Big: Can only be caught while pouncing.
```

Behavior:

- Back returns to Main Menu.

### Level intro

Content:

```text
Level X
Catch Y mice
3 lives
```

If a new mouse type appears:

```text
New mouse type: Fast
```

or:

```text
New mouse type: Big
```

Behavior:

- Lasts `1.5 seconds`.
- Cat is controllable.
- No spawning.

### Level complete

Content:

```text
Level X Complete
Score: N
Bonus: N
High Score: N
Next Level
```

Behavior:

- Automatically advances after `3 seconds`.
- Player can click Next immediately.

### Campaign complete

Content:

```text
Campaign Complete
Score: N
High Score: N
Play Endless
Main Menu
```

Behavior:

- Unlocks Endless Mode.
- Saves high score.

### Game over

Content:

```text
Game Over
Level X
Score: N
Retry Level
Main Menu
```

Behavior:

- Retry restarts current level.
- Score resets to level start score.

### Endless wave complete

Content:

```text
Wave X Complete
Score: N
Bonus: N
Next Wave in 3
```

Behavior:

- Automatically starts next wave after `3 seconds`.

### Endless game over

Content:

```text
Game Over
Wave X
Score: N
Retry Wave
Main Menu
```

Behavior:

- Retry restarts current wave.
- Score resets to wave start score.

### Pause overlay

Content:

```text
Paused
Resume
Restart
Main Menu
```

Behavior:

- Resume returns to gameplay.
- Restart restarts current level or wave.
- Main Menu returns to Main Menu.

## 4.16 Save system

Tier: 1 for defaults, Tier 2 for campaign high score, Tier 3 for endless high score and best wave.

Save only the minimum required data.

Required save data:

```text
endless_unlocked: boolean
campaign_high_score: integer
endless_high_score: integer
endless_best_wave: integer
total_plays: integer
```

Save timing:

- Campaign level complete.
- Campaign complete.
- Campaign game over.
- Endless wave complete.
- Endless game over.

High score update:

Campaign:

```text
if score > save.campaign_high_score:
    save.campaign_high_score = score
```

Endless:

```text
if score > save.endless_high_score:
    save.endless_high_score = score
```

Best wave:

```text
if wave > save.endless_best_wave:
    save.endless_best_wave = wave
```

Total plays:

- Increment when starting campaign.
- Increment when starting endless.

No mid-level progress is saved.

## 4.17 Performance and edge cases

Tier: 1.

Performance constraints:

- Maximum active mice: `7` in Endless Mode.
- Maximum holes per level: `6`.
- Maximum obstacles per level: `3`.
- No full pathfinding.
- No physics engine required.
- Use fixed or clamped delta time.
- Recommended max delta time: `1/30 second`.

Edge cases:

| Case | Rule |
| --- | --- |
| Player pauses | All timers stop. No spawning, movement, score, or life changes. |
| Browser loses focus | Automatically pause the game. |
| Pounce pressed during cooldown | Buffer input for `0.1 seconds`. Execute pounce when cooldown is ready if buffer is still active. |
| Pounce with no movement input | Use last movement direction. If no movement direction exists yet, pounce to the right. |
| Cat blocks all spawn holes | Spawning waits until at least one hole is available. Spawn timer continues counting down. |
| Mouse cannot find available hole | Mouse continues fleeing/wandering. It does not escape until a hole becomes available. |
| Multiple mice caught same frame | Each mouse is caught. Each mouse adds its own score. Combo increases for each mouse. One multi-catch bonus is added. |
| Multiple mice escape same frame | Each mouse reduces lives by 1. If lives become 0 or below, trigger game over. |
| Target reached same frame as lives reach 0 | Process catches before escapes. If the target is reached, level complete wins. |
| Mouse caught while entering hole | The mouse is caught. It does not escape. The hole remains occupied for its normal `0.8 seconds`. |
| Big mouse touched while not pouncing | No catch. Mouse becomes startled. Mouse cannot seek holes while startled. |
| Mouse stuck against obstacle | Obstacle avoidance should rotate the mouse’s desired direction. If the mouse’s speed is near zero for `1.0 second`, force a new random wander direction. |
| Player leaves mid-level | No special save is required. High score can be saved at level complete, campaign complete, endless wave complete, or game over. |
| Retry after failure | Restart the same level or wave. Reset lives to 3. Reset score to the score at the start of that level or wave. |

Cut features:

| Cut feature | Reason |
| --- | --- |
| No player upgrades | Adds UI and progression complexity without improving core chase. |
| No cat health | Lives are based on escaped mice. |
| No mouse health | Mice are caught or escape. |
| No level select | Campaign is short and linear. |
| No timer-based failure | Lives based on escapes is clearer. |
| No camera scrolling | Single-screen arena is simpler and clearer. |
| No 3D movement | Game is 2D top-down. |
| No mouse aiming | Movement and pounce direction are enough. |
| No stamina system | Pounce cooldown is enough. |
| No shop | Not needed for short arcade game. |
| No cosmetic unlocks | Adds save and UI complexity. |
| No boss mice | Not needed for core loop. |
| No destructible obstacles | Obstacles are static chase props. |
| No persistent mid-level save | Short arcade game does not need it. |
| No full pathfinding | Simple avoidance is enough for single-screen arena. |
| No combo milestone audio | HUD communicates combo state. |
| No external assets | All visuals and audio can be procedural. |
| No screen shake | Would hide fast-moving entities. |
| No voice lines | Not needed for short browser game. |
| No in-game settings menu | Not required for this scope. |
| No high score on main menu | High scores appear on complete screens. |
| No spawn warning icon | Emerging animation is enough. |
| No hole block sound | Visual paw print is enough. |

## 4.18 Level Content

Tier: 1 for Level 1, Tier 2 for Levels 2 through 10.

All levels use the same arena size: `960 x 540`.

Cat start position for all levels:

```text
480, 270
```

Exception: Level 2 uses the corrected cat start position from 0.2.

Lives for all levels:

```text
3
```

### Level parameters table

| Level | Target | Max Active | Spawn Interval | Mouse Mix | Notes |
| ---: | ---: | ---: | ---: | --- | --- |
| 1 | 5 | 2 | 2.0 | Normal 100 | Tutorial |
| 2 | 8 | 3 | 1.8 | Normal 100 | More holes |
| 3 | 10 | 3 | 1.6 | Normal 75, Fast 25 | Introduce Fast |
| 4 | 10 | 3 | 1.6 | Normal 80, Big 20 | Introduce Big |
| 5 | 12 | 4 | 1.5 | Normal 50, Fast 30, Big 20 | First mix |
| 6 | 14 | 4 | 1.4 | Normal 40, Fast 40, Big 20 | More pressure |
| 7 | 16 | 4 | 1.3 | Normal 30, Fast 50, Big 20 | Fast-heavy |
| 8 | 16 | 5 | 1.2 | Normal 30, Fast 30, Big 40 | Big-heavy |
| 9 | 18 | 5 | 1.1 | Normal 30, Fast 35, Big 35 | Mixed pressure |
| 10 | 20 | 5 | 1.0 | Normal 25, Fast 45, Big 30 | Final level |

### Level layouts

Coordinates are in the `960 x 540` arena.

Holes are listed as:

```text
x, y
```

Obstacles are listed as:

```text
x, y, width, height
```

#### Level 1

Holes:

```text
120, 420
840, 420
```

Obstacles:

```text
none
```

Notes:

- Teaches movement, catching, and hole escape.
- Only two active mice at a time.
- No obstacles.

#### Level 2

Holes:

```text
120, 120
840, 120
480, 440
```

Obstacles:

```text
400, 230, 160, 80
```

Notes:

- Adds a third hole.
- Adds one central obstacle.
- Cat start is corrected to approximately `480, 212` because the default start is inside the obstacle.

#### Level 3

Holes:

```text
120, 420
480, 120
840, 420
```

Obstacles:

```text
180, 180, 120, 80
660, 300, 120, 80
```

Notes:

- Introduces Fast mice.
- Mice become harder to chase.

#### Level 4

Holes:

```text
120, 120
840, 120
120, 420
840, 420
```

Obstacles:

```text
300, 150, 200, 80
480, 330, 120, 120
```

Notes:

- Introduces Big mice.
- Player must use pounce to catch Big mice.

#### Level 5

Holes:

```text
120, 120
480, 440
840, 120
```

Obstacles:

```text
150, 200, 120, 120
690, 200, 120, 120
```

Notes:

- First mixed mouse types.
- Two large side obstacles.

#### Level 6

Holes:

```text
120, 120
840, 120
120, 420
840, 420
```

Obstacles:

```text
360, 120, 240, 80
240, 320, 120, 80
600, 320, 120, 80
```

Notes:

- More holes.
- Obstacles create multiple chase lanes.

#### Level 7

Holes:

```text
120, 120
480, 120
840, 120
480, 440
```

Obstacles:

```text
180, 180, 100, 180
680, 180, 100, 180
```

Notes:

- Fast-heavy level.
- Vertical obstacles create narrow chases.

#### Level 8

Holes:

```text
120, 120
840, 120
120, 420
480, 440
840, 420
```

Obstacles:

```text
300, 120, 120, 80
540, 120, 120, 80
420, 300, 120, 80
```

Notes:

- Big-heavy level.
- Five holes increase escape pressure.

#### Level 9

Holes:

```text
120, 120
480, 120
840, 120
120, 420
840, 420
```

Obstacles:

```text
200, 200, 120, 80
420, 320, 120, 80
640, 200, 120, 80
```

Notes:

- Mixed pressure.
- Obstacles are spread to prevent camping.

#### Level 10

Holes:

```text
120, 120
480, 120
840, 120
120, 420
480, 440
840, 420
```

Obstacles:

```text
160, 160, 120, 120
680, 160, 120, 120
400, 320, 160, 80
```

Notes:

- Final campaign level.
- Six holes.
- Highest target.
- Fast and Big mice are common.

## 4.19 Endless Mode Content

Tier: 3.

Endless waves use the campaign layouts from Levels 8, 9, and 10.

Wave layout formula:

```text
layoutLevel = [10, 9, 8][(waveNumber - 1) % 3]
```

Wave parameters:

```text
target = min(50, 15 + 5 * (waveNumber - 1))
spawnInterval = max(0.6, 1.0 - 0.05 * (waveNumber - 1))
maxActive = min(7, 4 + floor((waveNumber + 1) / 2))
lives = 3
```

Mouse mix:

```text
normal = max(10, 40 - 2 * (waveNumber - 1))
fast = 35 + 2 * (waveNumber - 1))
big = 25 + 2 * (waveNumber - 1)
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

## 4.20 Feel and balance

Tier: 1 for base feel, Tier 2 for campaign feel, Tier 3 for endless pressure.

The game should feel:

- Snappy.
- Slightly frantic.
- Fair.
- Readable.

### Cat feel

The cat should always feel responsive.

Key feelings:

- Movement should start immediately.
- Pounce should feel like a burst, not a slow dash.
- The cat should be able to cross the arena quickly, but not so quickly that mice are trivial.
- Pounce should be used for:
  - Crossing distance.
  - Catching Big mice.
  - Multi-catch opportunities.
  - Getting into position to block a hole.

### Mouse feel

Mice should feel like prey.

Key feelings:

- They should panic when the cat is close.
- They should not be perfectly predictable.
- They should give the player a fair chance to react.
- They should not feel like they are cheating.
- They should not get permanently stuck.

### Fairness rules

- Mice cannot enter a hole while the cat is blocking it.
- Mice cannot enter a hole that is occupied.
- Mice cannot escape instantly after spawning.
- Mice are not catchable while emerging.
- Mice can still be caught while entering a hole.
- The player can always see all active mice.
- No mouse can become invisible or uncatchable except Big mice, which are clearly special.

# 5. CHARACTERS

## Cat

Silhouette:

- Rounded orange tabby cat.
- Two triangular ears.
- Curved tail.
- Four small paws visible from top-down.
- Simple face with two dark eyes and a small pink nose.
- Darker orange stripes on back.

Facing:

- Top-down.
- Body rotates toward movement direction while moving.
- While pouncing, body aligns to pounce direction.
- If no movement direction exists, default facing is right.

Animations by name:

| Animation | Motion rules |
| --- | --- |
| Idle | Tail wags slowly. Ears twitch occasionally. Body faces last direction or right. |
| Moving | Paws bob. Tail follows movement. Body rotates toward movement direction. |
| Pouncing | Body stretches `1.35x` in pounce direction. Paws extend. Tail straightens. Speed lines appear. Duration matches `0.18s` pounce. |
| Landing | Brief squash `0.85x` vertically for `0.05s`. |
| Catching | Brief happy face: eyes become curved lines for `0.12s`. |
| Blocked hole | No special cat animation. Hole shows blocked state. |

Cat states needed by gameplay:

| Gameplay state | Visual state |
| --- | --- |
| Moving | Moving |
| Pouncing | Pouncing |
| Pounce landing | Landing |
| Catching mouse | Catching |
| Idle | Idle |

## Mice

Silhouettes:

| Mouse | Silhouette |
| --- | --- |
| Normal | Small round gray body, small ears, thin tail. |
| Fast | Smaller sleeker blue-gray body, smaller ears, stiffer tail. |
| Big | Larger chunky dark slate body, larger head, thick tail, gold paw badge. |

Facing:

- Top-down.
- Body rotates toward movement direction while fleeing.
- While entering, body rotates toward hole center.
- While emerging, body faces outward from hole or last facing.

Animations by name:

| Animation | Motion rules |
| --- | --- |
| Emerging | Scale `0.4` to `1.0`, alpha `0` to `1`, shadow appears, small dust puff. Duration `0.25s`. Not catchable. |
| Fleeing | Normal run animation. Tail flicks. Direction rotates toward movement. |
| Fast streak | Fast mouse shows cyan streak when speed > `150px/s`. |
| Big badge pulse | Big mouse paw badge pulses subtly when cat is not pouncing. |
| Big badge glow | Big mouse paw badge glows brighter when cat is pouncing. |
| Startle | Big mouse flashes white for `0.08s`. Eyes become wide. Tail puffs. Small speed lines appear. |
| Entering hole | Mouse scales down to `0.55`, alpha fades to `0`, moves toward hole center, tail disappears last. Duration `0.3s`. Still catchable. |
| Caught | Mouse becomes a small fur puff and 3-4 gold stars, then score popup. |
| Escaped | Mouse sinks into hole, hole ripple plays, small dust puff. |

Mouse states needed by gameplay:

| Gameplay state | Visual state |
| --- | --- |
| Emerging | Emerging |
| Fleeing | Fleeing |
| Entering | Entering hole |
| Caught outcome | Caught |
| Escaped outcome | Escaped |
| Big mouse startle | Startle |

# 6. AUDIO

Audio is synthesized with WebAudio. No external audio files are required.

The builder has access to an audio API. The audio system must:

- Create or resume the AudioContext on first user interaction.
- First interaction can be:
  - Clicking Play.
  - Pressing any key.
  - Clicking the canvas.
- Pause all audio when the game pauses.
- Stop gameplay SFX when the browser loses focus.
- Record `lastCue` even when audio is disabled.
- Use panning for gameplay SFX.
- Use ducking when music is built.

Master mix:

- Master gain: `0.8`
- Music gain: `0.35`
- SFX gain: `0.7`

Music ducking:

When a jingle plays:

- Lower music by `3dB`.
- Return over `0.3s` after jingle ends.

Panning:

For gameplay SFX:

```text
pan = (x / 960 - 0.5) * 0.7
```

Where `x` is the entity’s horizontal position.

- Cat pounce pans by cat x.
- Catch pans by mouse x.
- Escape pans by hole x.
- UI sounds are center.

## Synthesized SFX table

| Name | Recipe | When it plays | Tier |
| --- | --- | --- | ---: |
| `ui_click` | Square wave, `800Hz`, `0.03s`, volume `0.25`, center pan. | UI button press. | 1 |
| `pounce` | Filtered noise sweep from `400Hz` to `1600Hz` over `0.12s`, plus short sine down from `600Hz` to `200Hz` over `0.1s`, volume `0.7`, pan by cat x. | Cat pounce start. | 1 |
| `catch` | Sine sweep from `600Hz` to `900Hz` over `0.08s`, plus `30ms` noise burst, volume `0.8`, pan by mouse x. Pitch rises one semitone per combo level, capped at `+12 semitones`. | Mouse caught. | 1 |
| `multi_catch` | Two quick bright notes: `880Hz` then `1318.5Hz`, each `0.05s`, triangle wave, volume `0.6`, total `0.15s`, center or cat x. | Multi-catch event. | 1 |
| `startle` | High quick squeak with vibrato: triangle wave from `1200Hz` to `1800Hz` over `0.1s`, vibrato `20Hz`, volume `0.7`, pan by mouse x. | Big mouse touched while cat is not pouncing. | 2 |
| `escape` | Descending squeak: triangle from `900Hz` to `400Hz` over `0.2s`, plus soft `100Hz` thud at the end, volume `0.8`, pan by hole x. | Mouse escapes. | 1 |
| `level_complete` | Bright 3-note major jingle: `C5`, `E5`, `G5`, sine/triangle, `0.6s` total, volume `0.7`, center. Duck music. | Campaign level complete. | 2 |
| `campaign_complete` | Slightly longer fanfare: `C5`, `E5`, `G5`, `C6`, sine/triangle, `1.2s` total, volume `0.8`, center. Duck music. | Campaign complete. | 2 |
| `game_over` | Soft low descending sting: triangle from `220Hz` to `110Hz` over `0.6s`, volume `0.6`, center. | Campaign game over. | 1 |
| `endless_wave_complete` | Bright 4-note jingle: `D5`, `F#5`, `A5`, `D6`, sine/triangle, `0.5s` total, volume `0.7`, center. Duck music. | Endless wave complete. | 3 |
| `endless_game_over` | Low descending sting: triangle from `200Hz` to `100Hz` over `0.6s`, volume `0.6`, center. Slightly lower than campaign game over. | Endless game over. | 3 |

Cut cue:

| Name | Reason |
| --- | --- |
| `combo_milestone` | Cut because engineering explicitly cut it and gameplay listed it as optional. HUD pulse is enough. |

## Music table

Tier 4. If not built, music functions are no-ops.

| Name | Recipe | When it plays | Tier |
| --- | --- | --- | ---: |
| `music_menu` | Marimba-like sine/triangle pattern in C major, `96 BPM`, soft bass, light pizzicato, loop `20` to `30s`, volume `0.35`. | Main menu. | 4 |
| `music_gameplay` | Playful bouncy pattern in D major, `124 BPM`, marimba, pizzicato strings, light bass, soft hand drums, loop `24` to `32s`, volume `0.35`. Base layer always during gameplay. Chase layer adds pizzicato when `active_mouse_count > 0`. Pressure layer adds hand drums and low tom pulse when `lives == 1`. | Campaign playing. | 4 |
| `music_endless` | Same melodic motif in B minor or D minor, `132 BPM`, same core plus shaker, extra percussion, slightly lower bass, loop `24` to `32s`, volume `0.35`. | Endless playing. | 4 |

# 7. UX

UX is HTML and CSS only for screens and HUD. The gameplay arena is canvas. DOM elements do not affect gameplay coordinates.

## Required DOM structure

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

## State machine

| From | To | Trigger |
| --- | --- | --- |
| `menu` | `howToPlay` | How to Play button |
| `menu` | `levelIntro` | Play button |
| `menu` | `playing` | Endless button, only if unlocked |
| `howToPlay` | `menu` | Back button |
| `levelIntro` | `playing` | Intro timer reaches `0` |
| `levelIntro` | `paused` | Esc, P, pause button, focus loss |
| `playing` | `paused` | Esc, P, pause button, focus loss |
| `playing` | `levelComplete` | Campaign target reached |
| `playing` | `gameOver` | Campaign lives reach `0` |
| `playing` | `endlessWaveComplete` | Endless target reached |
| `playing` | `endlessGameOver` | Endless lives reach `0` |
| `paused` | `pausedFrom` | Resume button |
| `paused` | `levelIntro` or `playing` | Restart button |
| `paused` | `menu` | Main Menu button |
| `levelComplete` | `levelIntro` | Next button or auto-advance after `3s` |
| `levelComplete` | `campaignComplete` | Level 10 complete |
| `levelComplete` | `paused` | Esc, P, focus loss |
| `campaignComplete` | `playing` | Play Endless button |
| `campaignComplete` | `menu` | Main Menu button |
| `gameOver` | `levelIntro` or `playing` | Retry button |
| `gameOver` | `menu` | Main Menu button |
| `endlessWaveComplete` | `playing` | Auto-advance after `3s` |
| `endlessWaveComplete` | `paused` | Esc, P, focus loss |
| `endlessGameOver` | `playing` | Retry Wave button |
| `endlessGameOver` | `menu` | Main Menu button |

## HUD table

| Element | Record field | When visible |
| --- | --- | --- |
| `#score` | `state.score` | `levelIntro`, `playing` |
| `#combo` | `state.comboMultiplier` | `levelIntro`, `playing`, only when `comboMultiplier > 1.0` |
| `#level-label` | `state.level` or `state.wave` | `levelIntro`, `playing` |
| `#caught-label` | `state.caught`, `state.target` | `levelIntro`, `playing` |
| `#progress-fill` | `state.progress` | `levelIntro`, `playing` |
| `#lives` | `state.lives` | `levelIntro`, `playing` |
| `#pause-button` | `state.screen` | `playing` |
| `#pounce-label` | constant | `levelIntro`, `playing` |
| `#pounce-fill` | `state.cat.pounceReadiness` | `levelIntro`, `playing` |
| `#center-message` | `state.messages[0]` | `levelIntro`, `playing`, only when a message is active |
| `#screen-menu` | `state.screen === "menu"` | `menu` |
| `#screen-how` | `state.screen === "howToPlay"` | `howToPlay` |
| `#screen-intro` | `state.screen === "levelIntro"` | `levelIntro` |
| `#screen-pause` | `state.screen === "paused"` | `paused` |
| `#screen-level-complete` | `state.screen === "levelComplete"` | `levelComplete` |
| `#screen-campaign-complete` | `state.screen === "campaignComplete"` | `campaignComplete` |
| `#screen-game-over` | `state.screen === "gameOver"` | `gameOver` |
| `#screen-endless-wave-complete` | `state.screen === "endlessWaveComplete"` | `endlessWaveComplete` |
| `#screen-endless-game-over` | `state.screen === "endlessGameOver"` | `endlessGameOver` |

HUD visibility rule:

- HUD is visible during `levelIntro` and `playing`.
- HUD is hidden when an overlay panel is active:
  - `menu`
  - `howToPlay`
  - `paused`
  - `levelComplete`
  - `campaignComplete`
  - `gameOver`
  - `endlessWaveComplete`
  - `endlessGameOver`

Center message rules:

- Only one message at a time.
- Higher priority replaces lower priority.
- Duration is `1.0s` to `1.5s`.
- Messages do not block gameplay.

# 8. DEBUG API

`window.__game` is the only interface tests may use to drive the game.

All methods must be safe to call from tests.

All setters should clamp values to valid ranges where reasonable.

## State and save

| Function | Args / Return | Purpose |
| --- | --- | --- |
| `getState()` | returns state object | Returns serializable deep copy of current game state. |
| `getSave()` | returns save object | Returns current save data. |
| `setSave(saveObject)` | accepts save object | Overrides save data. |
| `reset()` | returns void | Returns to menu, clears entities, score, level/wave, messages, and audio last cue. Keeps save data. |

## Flow

| Function | Args / Return | Purpose |
| --- | --- | --- |
| `startCampaign()` | returns void | Starts campaign Level 1 with score 0. |
| `startEndless()` | returns boolean | Starts Endless Wave 1 if unlocked. Returns `false` and does nothing if locked. |
| `startLevel(levelNumber)` | accepts integer | Starts a campaign level using current score as `scoreAtStart`. |
| `startWave(waveNumber)` | accepts integer | Starts an endless wave using current score as `scoreAtStart`. |
| `next()` | returns void | Advances from level complete. |
| `retry()` | returns void | Restarts current level or wave. |
| `mainMenu()` | returns void | Returns to main menu and clears active run. |
| `howToPlay()` | returns void | Shows how to play. |
| `back()` | returns void | Returns from how to play to menu. |

## Pause and focus

| Function | Args / Return | Purpose |
| --- | --- | --- |
| `pause()` | returns void | Pauses game. |
| `resume()` | returns void | Resumes game. |
| `setPaused(boolean)` | accepts boolean | Sets pause state. |
| `simulateFocusLoss()` | returns void | Triggers same behavior as browser blur. |

## Time control

| Function | Args / Return | Purpose |
| --- | --- | --- |
| `setAutoStep(boolean)` | accepts boolean | Enables/disables automatic stepping. |
| `step(seconds)` | accepts seconds, returns step count | Advances simulation by whole fixed steps. Stops early if game leaves an update-eligible screen. Does nothing if paused. |
| `stepUntil(predicate, maxSeconds)` | accepts predicate and optional seconds, returns boolean | Steps until predicate receives `getState()` and returns true. Default `maxSeconds` is `10`. |
| `getFixedDt()` | returns number | Returns `1 / 60`. |

## RNG

| Function | Args / Return | Purpose |
| --- | --- | --- |
| `setSeed(seed)` | accepts number | Resets RNG seed. |
| `getSeed()` | returns number | Returns current seed. |

## Input

| Function | Args / Return | Purpose |
| --- | --- | --- |
| `setMovementInput(x, y)` | accepts numbers | Sets raw movement input. Game normalizes vector. |
| `setPounceDown(boolean)` | accepts boolean | Sets pounce held state. |
| `triggerPounce()` | returns void | Simulates a pounce press edge. |
| `triggerPause()` | returns void | Simulates a pause press edge. |
| `clearInput()` | returns void | Clears movement, pounce, and pause input. |

## Cat control

| Function | Args / Return | Purpose |
| --- | --- | --- |
| `setCatPosition(x, y)` | accepts numbers | Sets cat position, clamped to arena. |
| `setCatVelocity(x, y)` | accepts numbers | Sets cat velocity. |
| `setPounceTimer(t)` | accepts seconds | Sets pounce timer. |
| `setPounceCooldown(t)` | accepts seconds | Sets pounce cooldown. |
| `setPounceBuffer(t)` | accepts seconds | Sets pounce buffer. |
| `setLastDirection(x, y)` | accepts numbers | Sets last movement direction. |

## Mouse control

| Function | Args / Return | Purpose |
| --- | --- | --- |
| `forceSpawn({ type, holeIndex })` | accepts object, returns mouse id | Creates a mouse immediately. Bypasses spawn timer and max active rules. Uses given type or current level mix and RNG. Uses given `holeIndex` or first hole. Does not reset `spawnTimer`. |
| `forceCatch({ mouseId, pouncing })` | accepts object, returns boolean | Catches given mouse immediately. Bypasses collision. Uses `pouncing` for score and Big mouse rules. If no `mouseId`, catch first catchable active mouse. |
| `forceEscape({ mouseId })` | accepts object, returns boolean | Processes escape for given mouse immediately. |
| `setMousePosition(id, x, y)` | accepts id and numbers | Sets mouse position. |
| `setMouseState(id, state)` | accepts id and state | Sets mouse state to `emerging`, `fleeing`, or `entering`. |
| `setMouseOutTime(id, t)` | accepts id and seconds | Sets mouse `outTime`. |
| `setMouseEnterTimer(id, t)` | accepts id and seconds | Sets mouse `enterTimer`. |
| `setMouseStartleTimer(id, t)` | accepts id and seconds | Sets mouse `startleTimer`. |
| `setMouseStuckTimer(id, t)` | accepts id and seconds | Sets mouse `stuckTimer`. |
| `setMouseVelocity(id, x, y)` | accepts id and numbers | Sets mouse velocity. |

## Run control

| Function | Args / Return | Purpose |
| --- | --- | --- |
| `setLives(n)` | accepts integer | Sets lives. |
| `setScore(n)` | accepts integer | Sets score. |
| `setCombo(n)` | accepts integer | Sets combo. |
| `setLastCatchTime(t)` | accepts seconds | Sets last catch time. |
| `setCaught(n)` | accepts integer | Sets caught count. |
| `setTarget(n)` | accepts integer | Sets target. |
| `setEscapesInRun(n)` | accepts integer | Sets escapes in run. |
| `setSpawnTimer(t)` | accepts seconds | Sets spawn timer. |

## Hole control

| Function | Args / Return | Purpose |
| --- | --- | --- |
| `setHoleOccupied(index, t)` | accepts index and seconds | Sets hole occupied timer. |
| `setHoleBlocked(index, blocked)` | accepts index and boolean | Sets `blockedOverride`. |
| `clearHoleOverrides()` | returns void | Removes all debug blocking overrides. |

## Audio

| Function | Args / Return | Purpose |
| --- | --- | --- |
| `setAudioEnabled(boolean)` | accepts boolean | Enables/disables audio playback. `lastCue` still updates. |
| `playCue(cue)` | accepts cue name | Records `lastCue` and plays audio if enabled. |

## Level data

| Function | Args / Return | Purpose |
| --- | --- | --- |
| `getLevelData(levelNumber)` | accepts integer, returns level data | Returns plain level data. |
| `getWaveData(waveNumber)` | accepts integer, returns wave data | Returns plain wave data. |
| `validateLevel(levelNumber)` | accepts integer, returns validation | Validates campaign level. |
| `validateWave(waveNumber)` | accepts integer, returns validation | Validates endless wave. |

## System state getters

These functions give direct access to each gameplay system’s state.

| Function | Returns | Purpose |
| --- | --- | --- |
| `getCat()` | cat record | Cat system state. |
| `getMice()` | array of mouse records | Mouse AI and entity state. |
| `getHoles()` | array of hole records | Hole system state. |
| `getObstacles()` | array of obstacle records | Collision/level obstacle state. |
| `getSpawn()` | `{ timer, interval, maxActive, mix }` | Spawning system state. |
| `getScore()` | `{ score, highScore, scoreAtStart }` | Scoring system state. |
| `getCombo()` | `{ combo, multiplier, lastCatchTime }` | Combo system state. |
| `getLives()` | `{ lives, escapesInRun }` | Lives system state. |
| `getProgress()` | `{ caught, target, progress }` | Progress system state. |
| `getMessages()` | array of message records | Message system state. |
| `getStats()` | stats object | Event counters. |
| `getSave()` | save object | Save system state. |
| `getLevelData(levelNumber)` | level data | Level progression state. |
| `getWaveData(waveNumber)` | wave data | Endless system state. |

# 9. TESTS

Tests run in the browser using `window.__test`.

Loading `index.html?test=1` must:

- Disable auto-step.
- Disable audio.
- Seed RNG with `1337`.
- Run tests.
- Set `window.__testResults`.
- Produce `window.__testResults.failed === 0` for the current tier.

Helper:

```js
const G = window.__game;
const T = window.__test;

async function stepTo(screen, maxSeconds = 10) {
  return G.stepUntil(function (state) {
    return state.screen === screen;
  }, maxSeconds);
}
```

## Tier 1 tests

| Test group | Tests | Key assertions |
| --- | --- | --- |
| Bootstrap | Debug API exists | `typeof window.__game === "object"`, `typeof window.__test === "object"` |
| Bootstrap | Initial state is menu | `screen === "menu"`, `mode === null`, `level === null`, `wave === null`, `score === 0`, `lives === 0`, `caught === 0`, `target === 0`, `mice.length === 0` |
| Bootstrap | Save defaults | After reset: `endless_unlocked === false`, high scores `0`, `total_plays === 0` |
| Level 1 data | Level 1 exists | `G.getLevelData(1)` is not null |
| Level 1 data | Level 1 parameters | Target `5`, max active `2`, spawn interval `2.0`, mix normal `100` |
| Level 1 data | Level 1 layout | Holes `[[120, 420], [840, 420]]`, obstacles empty |
| Level 1 data | Level 1 validates | `G.validateLevel(1).valid === true` |
| Campaign flow | Start campaign | `mode === "campaign"`, `level === 1`, `screen === "levelIntro"`, `score === 0`, `total_plays >= 1` |
| Intro | Level intro lasts 1.5 seconds | Step `1.49` still intro; step `0.02` becomes playing |
| Intro | No mice during intro | After `1.5s`, `mice.length === 0` |
| Intro | First mouse spawns 1.0 seconds after intro | No mice at `0.99s` after intro; mouse exists at `1.01s` |
| Cat movement | Cat moves right with input | Set input `(1, 0)`, step, `cat.x` increases, `cat.vx > 0`; clear input, `cat.vx` decreases |
| Cat movement | Cat respects arena bounds | Near right wall, `cat.x <= 960 - cat.radius` |
| Pounce | Pounce starts and lasts 0.18 seconds | `pounceTimer > 0`, `pouncing === true`, `stats.pounces >= 1`, `lastCue === "pounce"`, after `0.18s` `pounceTimer === 0` |
| Pounce | Pounce cooldown is 0.8 seconds | After pounce, cooldown approximately `0.8`; after `0.3s`, approximately `0.5` |
| Pounce | Pounce buffer works | Set cooldown `0.05`, trigger pounce, not started; step `0.04`, not started; step `0.02`, started |
| Pounce | Pounce uses last direction | Set last direction down, clear input, trigger pounce, `cat.vy > 0`, `cat.vx === 0` |
| Pounce | Pounce defaults right | Reset direction, clear input, trigger pounce, `cat.vx > 0`, `cat.vy === 0` |
| Mouse spawn | Mouse emerges then flees | Force spawn, state `emerging`, timer approximately `0.25`; after `0.25s`, state `fleeing`, `outTime` approximately `0` |
| Mouse spawn | Spawn respects max active | Level 1 max active `2`; after two mice, no more spawn |
| Mouse spawn | Spawn waits when holes blocked | Set all holes blocked, no spawn; clear overrides, spawn occurs |
| Mouse AI | Mouse flees from cat | Place cat left of mouse, mouse moves away |
| Mouse AI | Mouse seeks hole after 2.5 seconds | Set `outTime = 2.5`, place mouse near hole, cat far, mouse moves toward hole |
| Mouse AI | Mouse enters available hole | Place mouse within `24px` of hole, `outTime = 3`, step `0.31s`, lives `2`, mouse removed, `lastCue === "escape"` |
| Mouse AI | Mouse cannot enter blocked hole | Cat within `40px` of hole, mouse does not escape |
| Mouse AI | Mouse cannot enter occupied hole | Hole occupied timer `0.8`, mouse does not escape |
| Catching | Normal mouse caught by contact | Overlap cat, step, `caught === 1`, `score === 100`, `combo === 1`, `lastCue === "catch"` |
| Catching | Pounce catch bonus | `outTime = 1.5`, pounce timer `0.1`, catch, score `150` |
| Catching | Fast catch bonus | `outTime = 0.5`, no pounce, catch, score `150` |
| Catching | Pounce and fast catch bonus | `outTime = 0.5`, pounce timer `0.1`, catch, score `200` |
| Multi-catch | Multi-catch bonus | Two normal mice overlapping cat, `caught === 2`, `lastCatchEvent.count === 2`, `multiBonus === 100`, expected score `325` |
| Combo | Combo increases within 3 seconds | Catch, combo `1`; step `2s`; catch, combo `2` |
| Combo | Combo resets after 3 seconds | Catch; step `3.1s`; combo `0`, multiplier `1` |
| Combo | Escape resets combo | Catch, combo `1`; force escape; combo `0` |
| Lives | Escape reduces lives | Force escape, lives `2`, `escapesInRun === 1` |
| Game over | Game over at zero lives | Set lives `1`, force escape, lives `0`, screen `gameOver` |
| Game over | Multiple escapes same frame | Set lives `2`, two entering mice with small timer, step, lives `0`, screen `gameOver` |
| Priority | Target reached same frame as escape wins | Set target `1`, lives `1`, one catchable mouse, one entering mouse, step, screen `levelComplete`, lives `1`, caught `>= 1` |
| Pause | Pause stops time | Record elapsed, pause, step, elapsed unchanged |
| Pause | Pause stops mouse movement | Record mouse position, pause, step, position unchanged |
| Pause | Resume restores gameplay | Pause, resume, step, time advances |
| Pause | Focus loss pauses | `simulateFocusLoss()`, screen `paused`; resume, screen `playing` |
| HUD state | Progress clamps | Set caught `10`, target `5`, progress `1` |
| HUD state | Combo hidden when multiplier is 1 | Combo `0`, multiplier `1`; combo `2`, multiplier `1.25` |
| HUD state | Pounce readiness | Cooldown `0.4`, readiness approximately `0.5`; cooldown `0`, readiness `1` |
| Audio cues | Pounce cue | Disable audio, trigger pounce, `lastCue === "pounce"` |
| Audio cues | Catch cue | Force catch, `lastCue === "catch"` |
| Audio cues | Multi-catch cue | Force two catches same frame, `lastCue === "multi_catch"` |
| Audio cues | Escape cue | Force escape, `lastCue === "escape"` |
| Invariants | Random smoke test | 200 random frames on Level 1: cat/mice in arena, valid states, counts valid, no NaN |
| Invariants | No NaN values | After smoke test, no NaN in cat/mouse positions, velocities, score, combo, timers |

## Tier 2 tests

| Test group | Tests | Key assertions |
| --- | --- | --- |
| Level data | All 10 levels exist | `G.getLevelData(n)` not null for `1..10` |
| Level data | Level parameters match gameplay | Target, max active, spawn interval, mix for each level |
| Level data | Level layouts match gameplay | Holes and obstacles exactly |
| Level data | All levels validate | `G.validateLevel(n).valid === true` for `1..10` |
| Level 2 | Level 2 cat start is valid | Start Level 2, cat inside arena, not inside obstacle, `cat.y <= 212.01` |
| Mouse types | Fast mouse data | Speed `220`, radius `12` |
| Mouse types | Big mouse data | Speed `150`, radius `20` |
| Big mouse | Big mouse not caught without pounce | Overlap cat, no pounce, `caught === 0`, `startleTimer > 0`, `lastCue === "startle"` |
| Big mouse | Big mouse caught while pouncing | Overlap cat, pounce timer `0.1`, `caught === 1`, mouse removed |
| Level complete | Level complete adds bonus | Complete Level 1 with score setup, `lastBonusEvent.bonus === 2500`, score `2600` |
| Level complete | Perfect bonus omitted with escape | Lives `2`, escapes `1`, bonus `1000` |
| Level complete | Auto-advances | Step `2.99s` still complete; step `0.02s`, level `2`, screen `levelIntro` |
| Campaign complete | Level 10 complete triggers campaign complete | Complete Level 10, screen `campaignComplete`, `save.endless_unlocked === true` |
| Retry | Retry resets score to level start | Set score `1000`, game over, retry, score `0`, lives `3`, caught `0`, combo `0` |
| Retry | Retry clears mice | Fail after spawning, retry, `mice.length === 0` |
| High score | Campaign high score updates | Complete Level 1 with score `1000`, save high score `1000` |
| High score | Campaign high score does not decrease | Existing high score `5000`, complete with `1000`, remains `5000` |
| End-to-end | All campaign levels can be completed | For `1..10`, start, set caught to target - 1, force catch, assert correct complete screen |
| End-to-end | All campaign levels can fail and retry | For `1..10`, start, set lives `1`, force escape, game over, retry, lives `3`, caught `0`, score reset |
| End-to-end | Full campaign to endless unlock | Complete all levels, campaign complete, endless unlocked, start endless, wave 1 playing |

## Tier 3 tests

| Test group | Tests | Key assertions |
| --- | --- | --- |
| Endless data | Endless wave 1 data | Wave `1`, layoutLevel `10`, target `15`, spawnInterval `1.0`, maxActive `5` |
| Endless data | Endless wave 2 data | Wave `2`, layoutLevel `9`, target `20`, spawnInterval `0.95`, maxActive `5` |
| Endless data | Endless wave 3 data | Wave `3`, layoutLevel `8`, target `25`, spawnInterval `0.9`, maxActive `6` |
| Endless data | Endless wave 5 data | Target `35`, maxActive `7` |
| Endless data | Endless wave caps | Wave `100`: target `<= 50`, spawnInterval `>= 0.6`, maxActive `<= 7` |
| Endless flow | Endless locked by default | Reset, `startEndless()` returns false, screen remains `menu` |
| Endless flow | Endless starts when unlocked | Set save unlocked, `startEndless()`, mode `endless`, wave `1`, screen `playing`, score `0` |
| Endless flow | Endless wave complete bonus | Complete wave 1 with setup, bonus `1750`, score `1850` |
| Endless flow | Endless wave auto-advances | Complete wave 1, step `2.99s` still complete; step `0.02s`, wave `2`, lives `3`, combo `0` |
| Endless flow | Endless retry resets score to wave start | Set score `500`, game over, retry, score `0`, lives `3` |
| Endless flow | Endless best wave saved | Complete wave 1, `save.endless_best_wave >= 1` |
| End-to-end | Endless waves 1 through 5 can be completed | For waves `1..5`, complete wave, score carries, next wave starts |

## Tier 4 tests

Tier 4 is optional polish. If built, these tests should pass.

| Test group | Tests | Key assertions |
| --- | --- | --- |
| Music | Music API exists | `Audio.playMusic` and `Audio.stopMusic` exist |
| Music | Music can start/stop | If built, no crash when starting/stopping music |
| Audio polish | Panning formula | Pan for x `0` is approximately `-0.35`, x `960` is approximately `0.35` |
| Audio polish | Ducking on jingle | If built, music gain ducks during jingle and returns |
| Reduced motion | Reduced motion flag | If browser prefers reduced motion, speed lines/vignette disabled or particle count reduced |
| Performance | Particle limit | Active particles never exceed `20` |
| Performance | Score popup limit | Active score popups never exceed `5` |
| Performance | Max constraints stable | 7 mice, 6 holes, 3 obstacles, fixed timestep, no pathfinding, no NaN |

# 10. BUILD ORDER

1. Create `index.html`, `css/style.css`, and base canvas layout.
2. Implement `js/config.js` with all gameplay constants.
3. Implement `js/utils.js` vector/math helpers.
4. Implement `js/rng.js` seeded RNG and weighted pick.
5. Implement `js/save.js` with localStorage fallback and defaults.
6. Implement `js/input.js` for keyboard, mouse, pause, and focus loss.
7. Implement `js/audio.js` with WebAudio unlock, SFX, `lastCue`, and disabled mode.
8. Implement `js/levels.js` with Level 1 first, then full campaign data and validation.
9. Implement `js/collision.js` arena clamp and circle-vs-AABB resolution.
10. Implement `js/entities.js` factories for cat, mouse, hole, obstacle.
11. Implement core `js/game.js` state machine: menu, how to play, level intro, playing, paused, game over.
12. Implement cat movement and pounce system.
13. Implement mouse emerging, fleeing, entering states.
14. Implement hole blocking and occupancy.
15. Implement spawning with spawn timer and max active.
16. Implement catching, escaping, lives, score, and combo.
17. Implement basic HUD and center messages.
18. Implement basic canvas rendering for cat, mice, holes, obstacles.
19. Implement `js/ui.js` DOM screens and buttons.
20. Implement `js/render.js` state-driven drawing.
21. Implement `js/main.js` bootstrap and production loop.
22. Implement `js/debug.js` full debug API.
23. Implement `js/test-harness.js`.
24. Implement Tier 1 tests.
25. Add Levels 2 through 10, Fast and Big mice, level complete, campaign complete, and Level 2 cat correction.
26. Add full scoring bonuses, high score persistence, and campaign tests.
27. Add Endless Mode, wave generation, endless complete/game over, and endless tests.
28. Add visual level themes and detailed entity animations.
29. Add Tier 4 audio music, panning, ducking, reduced motion, and extra particles.
30. Run full test suite and fix failures.

# 11. DEFINITION OF DONE

## Tier 1: Core playable loop

High level definition:

The player can open the game, start Level 1, control the cat, pounce, catch normal mice, lose lives when mice escape, fail, retry, and see a stable testable core loop.

Checkboxes:

- [ ] All Tier 1 required files exist.
- [ ] All JavaScript files pass syntax check.
- [ ] Page loads without console errors.
- [ ] `window.Game` exists.
- [ ] `window.__game` exists.
- [ ] `window.__test` exists.
- [ ] `index.html?test=1` runs tests.
- [ ] `window.__testResults.failed === 0` for Tier 1 tests.
- [ ] Main menu is playable.
- [ ] How to Play screen works.
- [ ] Level 1 intro lasts `1.5 seconds`.
- [ ] No mice spawn during intro.
- [ ] First mouse spawns `1.0 seconds` after intro.
- [ ] Cat moves with WASD and arrow keys.
- [ ] Cat pounces with Space and left mouse button.
- [ ] Pounce lasts `0.18 seconds`.
- [ ] Pounce cooldown is `0.8 seconds`.
- [ ] Pounce buffer is `0.1 seconds`.
- [ ] Cat respects arena bounds.
- [ ] Cat collides with obstacles.
- [ ] Normal mouse emerges for `0.25 seconds`.
- [ ] Normal mouse is not catchable while emerging.
- [ ] Normal mouse flees from cat.
- [ ] Normal mouse seeks hole after `2.5 seconds`.
- [ ] Normal mouse can enter available hole.
- [ ] Mouse cannot enter blocked hole.
- [ ] Mouse cannot enter occupied hole.
- [ ] Catching normal mouse increases caught count.
- [ ] Catching normal mouse adds score.
- [ ] Catching normal mouse updates combo.
- [ ] Escape reduces lives by 1.
- [ ] Three escapes trigger game over.
- [ ] Retry resets lives, caught, combo, score, and mice.
- [ ] HUD shows score, combo, level, progress, lives, and pounce.
- [ ] Center messages appear for escape and level start.
- [ ] Core SFX record `lastCue` even when disabled.
- [ ] Random smoke test passes with no NaN.

## Tier 2: Campaign complete

High level definition:

The player can complete or fail all 10 campaign levels, see Fast and Big mice, receive bonuses, unlock Endless Mode, and persist campaign high score.

Checkboxes:

- [ ] Levels 2 through 10 exist.
- [ ] Level parameters match 4.18.
- [ ] Level layouts match 4.18.
- [ ] All levels validate.
- [ ] Level 2 cat start is corrected and valid.
- [ ] Fast mouse uses speed `220` and radius `12`.
- [ ] Big mouse uses speed `150` and radius `20`.
- [ ] Big mouse cannot be caught without pounce.
- [ ] Big mouse becomes startled when touched without pounce.
- [ ] Startle duration is `0.3 seconds`.
- [ ] Startle speed multiplier is `1.3`.
- [ ] Startled Big mouse cannot seek holes.
- [ ] Level complete triggers when caught reaches target.
- [ ] Level complete bonus uses lives and perfect bonus.
- [ ] Level complete auto-advances after `3 seconds`.
- [ ] Player can click Next immediately.
- [ ] Level 10 complete triggers campaign complete.
- [ ] Campaign complete unlocks Endless Mode.
- [ ] Campaign high score persists.
- [ ] Campaign high score does not decrease.
- [ ] Game over retry works for all levels.
- [ ] End-to-end campaign completion test passes.
- [ ] End-to-end campaign failure/retry test passes.

## Tier 3: Endless mode

High level definition:

The player can start Endless Mode after unlock, complete or fail waves, retry, and persist endless high score and best wave.

Checkboxes:

- [ ] Endless Mode is locked by default.
- [ ] Endless Mode starts when unlocked.
- [ ] Endless Mode starts Wave 1 with score 0.
- [ ] Wave layout uses `[10, 9, 8]` rotation.
- [ ] Wave target formula is correct.
- [ ] Wave spawn interval formula is correct.
- [ ] Wave max active formula is correct.
- [ ] Wave mouse mix formula is correct.
- [ ] Wave 1 has target `15`, spawn interval `1.0`, max active `5`.
- [ ] Wave 2 has target `20`, spawn interval `0.95`, max active `5`.
- [ ] Wave 3 has target `25`, spawn interval `0.9`, max active `6`.
- [ ] Wave 5 has target `35`, max active `7`.
- [ ] Wave 100 caps are respected.
- [ ] Endless wave complete bonus is correct.
- [ ] Endless wave auto-advances after `3 seconds`.
- [ ] Endless score carries between waves.
- [ ] Endless lives reset to 3 each wave.
- [ ] Endless combo resets each wave.
- [ ] Endless game over retry restarts current wave.
- [ ] Endless retry resets score to wave start.
- [ ] Endless high score persists.
- [ ] Endless best wave persists.
- [ ] Endless waves 1 through 5 can be completed.

## Tier 4: Presentation polish

High level definition:

The game has optional polish: music, panning, ducking, reduced motion, extra particles, and detailed level presentation, while remaining performant.

Checkboxes:

- [ ] Music API exists.
- [ ] Music can start and stop without crash.
- [ ] Menu music plays on menu if built.
- [ ] Gameplay music plays during campaign if built.
- [ ] Endless music plays during endless if built.
- [ ] Music ducks during jingles if built.
- [ ] Panning uses formula `pan = (x / 960 - 0.5) * 0.7`.
- [ ] Reduced motion disables speed lines and vignette pulses when preferred.
- [ ] Reduced motion reduces particle count when preferred.
- [ ] Active particles never exceed `20`.
- [ ] Active score popups never exceed `5`.
- [ ] No effect obscures a mouse or hole for more than `0.1s`.
- [ ] Level themes render for all campaign levels.
- [ ] Obstacle shadows do not cover hole centers.
- [ ] Game remains stable at maximum endless constraints.

# A. SANITY

| Check | Result | Notes |
| --- | --- | --- |
| Required headings are present in the required order | Valid | Sections 0 through 11 and A are present. |
| 0.1 is a table of requirements and where they live | Valid | Includes user request and gameplay design requirements. |
| 0.2 documents disagreements and rulings | Valid | Audio, assets, Level 2 start, mouse states, combo milestone, endless intro, pause, music, reduced motion, and cuts are ruled. |
| 0.3 defines tiers and Tier 1 minimal viable game | Valid | Tier 1 is core playable loop; Tier 2 campaign; Tier 3 endless; Tier 4 polish. |
| Future systems have tier tags | Valid | Gameplay systems, level content, endless, UI, save, and tests are tagged. |
| Units and axes are defined | Valid | Pixels, seconds, x right, y down, fixed dt, max frame dt. |
| Important conventions include fixed step and RNG | Valid | No `Math.random`, seeded RNG, fixed timestep, serializable state. |
| Module layout matches no-asset ruling | Valid | `.ogg` files dropped; WebAudio used. |
| Global context includes every gameplay record field | Valid | State includes cat, mice, holes, obstacles, score, combo, lives, caught, target, escapes, spawn, messages, save, events, stats. |
| Module specifics include functions needed by rules and tests | Valid | Config, utils, RNG, save, input, audio, levels, collision, entities, game, UI, render, debug, test harness APIs are specified. |
| Visual spec includes look, lighting, space, recipe tables | Valid | Palette, typography, 2.5D, level themes, entity visuals, HUD layout, feedback, particles included. |
| Visual rules that imply gameplay rules are ruled | Valid | Blocked/occupied holes, emerging, entering, Big badge, escape vignette, pounce bar, progress bar. |
| Gameplay spec includes game paragraph, records, systems, progression, feel | Valid | Systems are broken into subsections with numbers and tiers. |
| Every gameplay number is carried | Valid | Arena, cat, mouse, hole, combo, score, level, endless, intro, auto-advance, lives, performance constraints carried. |
| Level table and layouts are carried as tables/data | Valid | All 10 levels, holes, obstacles, notes included. |
| Endless formulas are carried | Valid | Layout, target, spawn interval, max active, mix formulas included. |
| Characters section includes silhouettes, animations, facings, and gameplay states | Valid | Cat and mouse animations mapped to gameplay states. |
| Audio section includes synthesized sound table | Valid | SFX and optional music recipes included. |
| Audio section includes when sounds play | Valid | Each cue has trigger. |
| UX is HTML/CSS only for screens and HUD | Valid | Canvas used only for gameplay arena. |
| UX includes screens as state machine | Valid | State machine table included. |
| UX includes HUD table element to record field to visibility | Valid | HUD table included. |
| Debug API includes engineering API | Valid | State, flow, pause, time, RNG, input, cat, mouse, run, hole, audio, level data included. |
| Debug API extended with system state getters | Valid | `getCat`, `getMice`, `getHoles`, `getObstacles`, `getSpawn`, `getScore`, `getCombo`, `getLives`, `getProgress`, `getMessages`, `getStats`, `getSave`, level/wave getters included. |
| Debug API includes player inputs as functions | Valid | `setMovementInput`, `setPounceDown`, `triggerPounce`, `triggerPause`, `clearInput` included. |
| Tests are tied to tiers | Valid | Tier 1, 2, 3, and optional Tier 4 tests listed. |
| Build order is high level | Valid | Ordered build steps provided. |
| Definition of done aligns with tiers | Valid | Tier 1 through Tier 4 high-level definitions and checkboxes provided. |
| Dropped items are documented | Valid | `.ogg` files, asset naming, combo milestone audio, main menu high score, level select, and other cuts documented in 0.2 and 4.17. |
| Errors found and fixed | Fixed | Found conflict between engineering `.ogg` files and required synthesized audio; resolved by dropping `.ogg` files and using WebAudio. Found missing player pause input function; added `triggerPause`. Found missing per-system debug getters; added system state getters. Found missing tier tags on some systems; added tier tags throughout. |