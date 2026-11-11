# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| A platformer where you play as a frog | `Player` record, `Platforming` system, `Characters` |
| 2D | Level grid, camera, collision, render contract |
| Side-on camera | `Camera` system, visual side-on pond levels |
| Real-time | Fixed real-time update loop, level timer |
| Free movement | Continuous AABB physics, not tile-grid movement |
| A sequence of levels | `Level` records, level roster, level progression |
| Failure restarts the level | `Hazards` hit rule, `Player` death state, level reset |
| Silly tone | Frog character, fly pickups, bug-zapper hazards, chiptune bleeps, silly names |
| A handful of levels, under 30 minutes | 6 levels, total par time 495 seconds |
| Win by reaching the exit | `Exit` system, win state |
| Core mechanic: platforming | `Platforming` system with gravity, jumping, surfaces, collision |
| Core mechanic: hazards | `Hazards` system with fixed-position dangers |
| Supporting mechanic: collectibles | `Collectibles` system with flies |
| Supporting mechanic: scoring | `Scoring` and `HighScores` systems |
| Extra mechanics: none | No enemies, no powerups, no dash, no double jump, no shooting |
| Pixel art, low-resolution sprites, visible square pixels, limited palette | Visual spec, palette, sprite sizes, `image-rendering: pixelated` |
| Saturated palette | Palette table |
| Pixel font | UX typography |
| Chiptune music | Audio music table |
| Retro bleep sound effects | Audio sound table |
| Screens: title, pause, settings, win, level select, high scores | UX state machine |
| HUD: score | HUD table |
| Effects: particles, hit flash | `Effects` and `Particles` systems |
| Accessibility: colour-blind safe palette, reduced motion, remappable keys | Palette rules, `Settings`, `Input` |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| Player is a frog | The player is “Pip”, a small bright blue pond frog. | Fits the prompt and silly tone. |
| Platformer | The game is a side-on action platformer with gravity and jumping. | Required. |
| 2D side-on | Levels are flat 2D tile/entity spaces viewed from the side. | Required. |
| Real-time | Updates run in real time at a fixed 60 Hz simulation step. | Required and deterministic. |
| Free movement | The player moves continuously with velocity, not cell-to-cell. | Required. |
| Sequence of levels | There are exactly 6 levels. | “Handful of levels.” |
| Failure restarts level | A hazard touch causes a short death state, then the same level restarts automatically. | Required. |
| No fail screen | Death is transient; there is no separate lose screen. | Failure is restart, not a new screen. |
| Win condition | Touching the exit finishes the level. | Required. |
| Silly tone | Names, pickups, hazards, and audio are pond-frog silly. | Required. |
| Under 30 minutes | Total par time is 495 seconds. | Required. |
| Core mechanics only | Platforming and hazards are the only core systems. | Required. |
| No enemies | There are no moving enemies. All dangers are fixed hazards. | Hazards are defined as fixed in place. |
| Hazards are fixed in place | Hazards never move, chase, shoot, or patrol. | Required. |
| Hazard types | 3 hazard types: spiky reed, thorn log, bug zapper. | Concrete content. |
| Collectibles | The collectible is a “Fly”. Each level contains exactly 5 flies. | Concrete set. |
| Collectible set | A level set is complete when all 5 flies in that level are collected. | Required. |
| Scoring | Score awards flies, exit completion, time bonus, and no-hit bonus. | Required. |
| High scores | Store the top 5 completed-run scores and best level score. | Required. |
| Extra mechanics | None. No dash, double jump, wall jump, powerups, or combat. | Required. |
| Pixel art | Logical canvas is 480x270, tile size 16, sprites are 8–32 px, rendered pixelated. | Required. |
| Limited palette | Use the 12-color palette in Visual Spec. | Required. |
| Saturated palette | Colors are bright and high-chroma. | Required. |
| Colour-blind safe palette | Critical objects use distinct shapes and luminance; palette avoids relying on red/green. | Required. |
| Pixel font | UI uses a bitmap pixel font named `PixelFont`, fallback monospace. | Required. |
| Chiptune music | Music is generated with square/triangle/noise voices. | Required. |
| Retro bleeps | SFX are short synthesized chip blips. | Required. |
| Screens | Only title, pause, settings, win, level select, high scores, plus the game view. | Required. |
| Settings | Settings only contain remappable keys and reduced motion. | Matches accessibility list. |
| Reduced motion | Disables particles, hit flash, camera smoothing, UI motion. | Required. |
| Remappable keys | Actions `left`, `right`, `jump`, `pause`, `restart`, `confirm`, `back` are remappable. | Required. |
| HUD | The only HUD element is the score. | Required. |
| Effects | Particles and player hit flash are the only effects. | Required. |
| Default controls | Keyboard first: arrows/A/D/W/Space. | Common browser platformer controls. |
| Death rule | One hazard touch kills and restarts the level. | Simple, matches failure rule. |
| Level count | 6 levels. | Handful. |
| Level dimensions | Levels are 40x17 to 80x20 tiles. | Short, under 30 minutes. |
| Level par times | 45, 60, 75, 90, 105, 120 seconds. | Under 30 minutes. |
| Collectible count | 5 flies per level, 30 total. | Concrete set. |
| Hazard count | 70 static hazards total. | Concrete content. |
| Score formula | Exit 500, fly 100, time bonus up to 500, no-hit 200. | Awards good play. |
| Persistence | LocalStorage. | Browser game. |
| Rendering | Canvas for game, HTML/CSS for screens and HUD. | UX requirement. |
| Audio API | Web Audio API with synthesized oscillators/noise. | Required. |
| Fixed step | 60 Hz fixed simulation, render interpolation not required. | Deterministic. |
| RNG | Deterministic seeded RNG per level. | Reproducible particles. |

## 0.3 Tiers

| Tier | Segment | Scope | Guarantees |
| --- | --- | --- | --- |
| Tier 1 | Core playable single level | Input defaults, platforming, hazards, exit, death/restart, camera, pixel art, palette, pixel font, chiptune SFX/music, particles, hit flash, HUD score placeholder, title screen, pause screen, single-level win screen. | Guaranteed to build and be finishable. |
| Tier 2 | Supporting mechanics and accessibility | Collectibles, scoring, high scores, settings screen, remappable keys, reduced motion, best score persistence. | Small complete addition on top of Tier 1. |
| Tier 3 | Full sequence | Level select, levels 2–6, level unlocking, full-run win, final high scores, difficulty tuning. | Higher-tier content; may be left unbuilt if stopped, but final game needs it. |

Tier 1 must include the chosen visual and audio style. Tier 2 does not add new art or sound styles; it uses Tier 1’s style. Tier 3 adds content only.

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Quantity | Value | Meaning |
| --- | ---: | --- |
| Logical canvas width | 480 px | Fixed low-resolution game viewport. |
| Logical canvas height | 270 px | Fixed low-resolution game viewport. |
| Tile size | 16 px | Platform grid unit. |
| Coordinate origin | Level top-left | `x` increases right, `y` increases down. |
| Screen origin | Viewport top-left | Camera transform subtracts camera position. |
| Simulation timestep | 1/60 s | Fixed real-time step. |
| Render frame budget | 60 fps | One render per animation frame. |
| Player hitbox width | 10 px | Collision box. |
| Player hitbox height | 12 px | Collision box. |
| Player sprite size | 16x16 px | Draw sprite; hitbox is centered horizontally and aligned near feet. |
| Sprite offset from hitbox | x -3, y -4 | Draw sprite around hitbox. |
| Gravity | 2000 px/s² | Downward acceleration. |
| Jump impulse | -650 px/s | Upward velocity on jump. |
| Max fall speed | 950 px/s | Terminal downward velocity. |
| Max horizontal speed | 180 px/s | Running cap. |
| Ground acceleration | 1500 px/s² | Horizontal acceleration on ground. |
| Air acceleration | 1000 px/s² | Horizontal acceleration in air. |
| Ground friction | 1800 px/s² | Opposes horizontal motion on ground. |
| Air drag | 200 px/s² | Opposes horizontal motion in air. |
| Jump cut factor | 0.45 | If jump released while rising, multiply `vy` by 0.45 once. |
| Coyote time | 0.08 s | Jump allowed briefly after leaving ground. |
| Jump buffer | 0.11 s | Jump press remembered briefly before landing. |
| Death duration | 0.9 s | Hurt state before automatic level restart. |
| Hit flash duration | 0.25 s | White flash on player hitbox. |
| Particle lifetime | 0.25–0.6 s | Depends on effect. |
| Camera smoothing | 10 per second | Exponential follow. |
| Camera horizontal deadzone | 32 px | Player can move inside deadzone without camera movement. |
| Camera vertical deadzone | 24 px | Player can move inside deadzone without camera movement. |

## 1.2 Important conventions

- Use one fixed-step loop:
  - `requestAnimationFrame` collects elapsed time.
  - Simulation runs in whole `dt = 1/60` steps.
  - If more than 5 steps accumulate, clamp to 5 to avoid death spirals.
- Input is sampled at the start of each simulation step.
- Update order is always:
  1. Input actions
  2. Player/platforming
  3. Hazards
  4. Collectibles
  5. Exit check
  6. Scoring/time
  7. Camera
  8. Particles/effects
  9. Render
- Use axis-aligned bounding box collision only.
- Collision resolution order:
  1. Move X, resolve X.
  2. Move Y, resolve Y.
- Ground detection:
  - Player is grounded if the pixel below the bottom edge overlaps a solid tile.
- All sprites and UI must use the specified palette.
- Critical gameplay states must not rely on color alone:
  - Hazards have spiky/zapping silhouettes.
  - Flies have fly silhouettes.
  - Exit has a large ring/arrow silhouette.
- Reduced motion must not change gameplay hitboxes, timings, or physics.
- Use deterministic RNG:
  - Algorithm: `mulberry32`.
  - Seed: `level.id * 977 + 1337`.
  - Particle randomness consumes the deterministic RNG only.
- Save data version key:
  - `frogPlatformer.save.v1`
- If LocalStorage is unavailable, keep save data in memory for the session.

# 2. CONTRACTS

## 2.1 Module layout

```text
index.html
assets/
  pixel.woff
  favicon.ico
css/
  game.css
js/
  main.js
  loop.js
  state.js
  input.js
  player.js
  platforming.js
  level.js
  hazards.js
  collectibles.js
  scoring.js
  highscores.js
  camera.js
  particles.js
  effects.js
  audio.js
  ui.js
  save.js
  debug.js
levels/
  level1.json
  level2.json
  level3.json
  level4.json
  level5.json
  level6.json
```

## 2.2 Global context

The global context is one mutable object owned by `state.js`.

```js
const global = {
  state: "TITLE", // TITLE | LEVEL_SELECT | SETTINGS | PLAYING | PAUSED | WIN | HIGH_SCORES
  previousState: null,

  ui: {
    focusIndex: 0,
    selectedLevel: 0,
    remapAction: null,
    remapCapture: false,
    settingsReturnState: "TITLE",
    winLevelIndex: 0,
    runComplete: false
  },

  settings: {
    keyMap: {
      left: ["ArrowLeft", "KeyA"],
      right: ["ArrowRight", "KeyD"],
      jump: ["Space", "ArrowUp", "KeyW"],
      pause: ["KeyP", "Escape"],
      restart: ["KeyR"],
      confirm: ["Enter"],
      back: ["Escape"]
    },
    reducedMotion: false,
    colorSafeAlways: true
  },

  input: {
    keyDown: {},
    actionDown: {},
    actionPressedThisStep: {},
    actionReleasedThisStep: {}
  },

  camera: {
    x: 0,
    y: 0,
    targetX: 0,
    targetY: 0,
    minX: 0,
    minY: 0,
    maxX: 0,
    maxY: 0
  },

  level: {
    id: 0,
    name: "",
    seed: 0,
    widthTiles: 0,
    heightTiles: 0,
    widthPx: 0,
    heightPx: 0,
    tiles: [],
    solids: [],
    parTime: 0,
    unlocked: false,
    completed: false,
    bestLevelScore: 0,
    exit: {
      id: 0,
      x: 0,
      y: 0,
      w: 0,
      h: 0,
      reached: false
    }
  },

  player: {
    x: 0,
    y: 0,
    w: 10,
    h: 12,
    vx: 0,
    vy: 0,
    facing: 1, // 1 right, -1 left
    grounded: false,
    coyoteTimer: 0,
    jumpBufferTimer: 0,
    jumpCutAvailable: false,
    alive: true,
    state: "idle", // idle | run | jump | fall | hurt
    animation: "idle",
    animationFrame: 0,
    animationTimer: 0,
    hitFlashTimer: 0,
    deathTimer: 0
  },

  hazards: {
    list: [] // { id, type, x, y, w, h, active, animationTimer }
  },

  collectibles: {
    list: [], // { id, x, y, w, h, collected, collectedAt }
    collectedCount: 0,
    totalCount: 0
  },

  score: {
    runScore: 0,
    levelScore: 0,
    flyScore: 0,
    exitScore: 0,
    timeBonus: 0,
    noHitBonus: 0,
    timeElapsed: 0,
    hitCount: 0,
    noHit: true,
    setComplete: false
  },

  effects: {
    particles: [], // { x, y, vx, vy, life, maxLife, color, size }
    hitFlashTimer: 0,
    lastSpawnRngState: 0
  },

  highScores: {
    top5: [], // { score, date, levelsCompleted, levelScores }
    bestLevel: {} // levelId -> bestScore
  },

  save: {
    version: "frogPlatformer.save.v1",
    unlockedLevel: 0,
    completed: {},
    bestLevel: {},
    top5: []
  },

  audio: {
    context: null,
    masterGain: null,
    unlocked: false,
    musicTrack: null,
    musicNodes: []
  },

  rng: {
    seed: 0,
    state: 0
  },

  debug: {
    enabled: false
  }
};
```

## 2.3 Module specifics

| Module | Required functions | Purpose |
| --- | --- | --- |
| `loop.js` | `startLoop()`, `stopLoop()`, `step(dt)`, `render()` | Fixed real-time loop. |
| `state.js` | `setState(name)`, `getState()`, `canTransition(from, to)` | Owns global state transitions. |
| `input.js` | `initInput()`, `sampleStep()`, `isDown(action)`, `justPressed(action)`, `justReleased(action)`, `setAction(action, down)`, `getKeyMap()`, `setKeyMap(map)`, `validateKeyMap(map)` | Input and remapping. |
| `player.js` | `resetPlayer(x, y)`, `getPlayerRect()`, `setPlayer(pos, vel)`, `killPlayer()`, `isPlayerAlive()` | Player record and state. |
| `platforming.js` | `stepPlayer(dt)`, `getGrounded()`, `setGrounded(value)`, `canJump()`, `jump()`, `cutJump()`, `getRect()` | Movement, gravity, collision. |
| `level.js` | `loadLevel(id)`, `unloadLevel()`, `resetLevel()`, `getExitRect()`, `isUnlocked(id)`, `unlockNext()`, `completeLevel()`, `getLevelRecord(id)` | Level loading and progression. |
| `hazards.js` | `loadHazards(entities)`, `stepHazards(dt)`, `getHazardRect(hazard)`, `hitTest(rect)`, `setHazardActive(id, active)`, `resetHazards()` | Fixed hazards. |
| `collectibles.js` | `loadCollectibles(entities)`, `stepCollectibles(dt)`, `collect(id)`, `getRemainingCount()`, `getCollectedCount()`, `resetCollectibles()` | Fly pickups. |
| `scoring.js` | `startLevelTimer()`, `stepScore(dt)`, `addFlyScore()`, `addExitScore()`, `calculateTimeBonus()`, `calculateNoHitBonus()`, `finalizeLevelScore()`, `getScoreSnapshot()` | Score records. |
| `highscores.js` | `loadHighScores()`, `saveHighScores()`, `submitRunScore(run)`, `getTop5()`, `getBestLevel(id)`, `recordBestLevel(id, score)` | Best score records. |
| `camera.js` | `initCamera(level)`, `stepCamera(dt)`, `getCamera()`, `setCamera(x, y)`, `clampCamera()` | Side-on follow camera. |
| `particles.js` | `spawnParticles(type, x, y, count)`, `stepParticles(dt)`, `getParticles()`, `clearParticles()` | Deterministic particles. |
| `effects.js` | `setHitFlash(duration)`, `getHitFlash()`, `stepEffects(dt)`, `applyReducedMotionPolicy()` | Hit flash and motion policy. |
| `audio.js` | `unlockAudio()`, `play(name)`, `playMusic(track)`, `stopMusic()`, `isAudioUnlocked()` | Web Audio synthesis. |
| `ui.js` | `renderState(state)`, `showHUD()`, `hideHUD()`, `updateScoreDisplay(score)`, `renderLevelSelect()`, `renderSettings()`, `renderHighScores()` | HTML/CSS screens. |
| `save.js` | `loadSave()`, `writeSave()`, `clearSave()` | LocalStorage persistence. |
| `debug.js` | `debugPlatforming(cmd, payload)`, `debugHazards(cmd, payload)`, `debugCollectibles(cmd, payload)`, `debugScoring(cmd, payload)`, `debugLevel(cmd, payload)`, `debugCamera(cmd, payload)`, `debugEffects(cmd, payload)`, `debugInput(action, state)` | Direct system access for tests. |

# 3. VISUAL SPEC

The game looks like a bright, silly pixel-art pond. Everything is built from 16-pixel tiles and small 8–32 pixel sprites with black outlines, flat saturated colors, and no realistic shading. Platforms are purple lily pads and logs, hazards are magenta spiky plants and electric bug zappers, collectibles are yellow flies, and the exit is a large cyan-white lily pad ring. The frog is small, blue, and cartoonish. The screen is always low-resolution and pixelated.

## Lighting and atmosphere

- No dynamic lighting.
- Backgrounds are flat with simple dithered bands.
- No shadows except fixed dark outlines.
- Water has two flat tones with small horizontal dither lines.
- The mood is bright, wet, and goofy, not scary.
- Reduced motion disables background dither animation and particle effects.

## Space

The space is a cartoon pond:

- Platforms: lily pads, logs, mud ledges.
- Hazards: spiky reeds, thorn logs, bug zappers.
- Collectibles: flies buzzing in fixed positions.
- Exit: giant lily pad ring with a white arrow.
- Background: dark blue water, purple shore tiles, cattail silhouettes.

## Palette

| Role | Hex | Notes |
| --- | --- | --- |
| Black / outline | `#0B1D2A` | All critical outlines. |
| Water dark | `#17465F` | Background water. |
| Water light | `#2D7790` | Water highlights. |
| Platform dark | `#7A00FF` | Lily pad/log base. |
| Platform light | `#A855F7` | Platform top edge. |
| Player body | `#29D3FF` | Frog body. |
| White / highlight | `#F7F7F7` | Eyes, exit, UI text. |
| Collectible yellow | `#FFD400` | Flies. |
| Hazard magenta | `#FF2E63` | Spikes/zapper danger. |
| Hazard accent orange | `#FF8C00` | Zapper sparks and hazard trim. |
| Exit cyan | `#00E5FF` | Exit ring. |
| UI focus yellow | `#FFD400` | Menu focus. |

Critical gameplay roles are encoded by shape and luminance:

- Hazards are spiky or electric, magenta/orange.
- Flies are tiny yellow wing shapes.
- Exit is a large ring with arrow, cyan/white.
- Player is a frog silhouette, blue/white eyes.

## Visual recipe table

| Element | Size | Colors | Animation | Rule implication |
| --- | ---: | --- | --- | --- |
| Solid tile | 16x16 | `#7A00FF`, `#A855F7`, `#0B1D2A` | Static | Blocks movement. |
| Player frog | 16x16 sprite, 10x12 hitbox | `#29D3FF`, `#F7F7F7`, `#0B1D2A` | Idle/run/jump/fall/hurt | Touching hazards kills. |
| Spiky reed | 16x10 | `#FF2E63`, `#0B1D2A` | 2-frame pulse, 0.25s | Touch kills. |
| Thorn log | 16x16 | `#7A00FF`, `#FF2E63`, `#0B1D2A` | Static thorns | Touch kills. |
| Bug zapper | 8x32 | `#FF8C00`, `#FF2E63`, `#F7F7F7` | 2-frame electric pulse, 0.15s | Touch kills. |
| Fly collectible | 12x12 sprite, 10x10 hitbox | `#FFD400`, `#0B1D2A` | 2-frame wing flap, 0.1s | Collected on touch. |
| Exit | 32x24 sprite, 20x20 trigger | `#00E5FF`, `#F7F7F7`, `#0B1D2A` | Slow ring pulse unless reduced motion | Touch wins level. |
| Particle | 1–3 px square | Role color | Velocity + life | Visual feedback only. |
| Hit flash | Hitbox overlay | `#F7F7F7` | 0.25s | Player took hazard hit. |
| HUD score | Text | `#F7F7F7` | No animation | Displays score. |
| Pixel font | 10px bitmap letters | `#F7F7F7` | Static | UI text. |

# 4. GAMEPLAY SPEC

The player controls Pip the Frog through six short side-on pond levels. Pip runs left and right, jumps under gravity, and must avoid fixed hazards. Touching a hazard kills Pip and restarts the level. Reaching the exit wins the level. Optional yellow flies are hidden in risky or off-path places. Score is awarded for finishing, collecting flies, playing fast, and avoiding hits. High scores are stored locally.

## Records and rosters

### Player record

| Field | Type | Initial | Used by |
| --- | --- | --- | --- |
| `x` | number px | level start x | collision, camera |
| `y` | number px | level start y | collision, camera |
| `w` | number px | 10 | collision |
| `h` | number px | 12 | collision |
| `vx` | number px/s | 0 | movement |
| `vy` | number px/s | 0 | gravity, jump |
| `facing` | number | 1 | animation |
| `grounded` | boolean | false | jump, animation |
| `coyoteTimer` | number s | 0 | jump tolerance |
| `jumpBufferTimer` | number s | 0 | jump input tolerance |
| `jumpCutAvailable` | boolean | false | variable jump |
| `alive` | boolean | true | gameplay |
| `state` | string | idle | animation |
| `hitFlashTimer` | number s | 0 | hit flash |
| `deathTimer` | number s | 0 | restart |

### Enemies roster

| Enemy | Count | Notes |
| --- | ---: | --- |
| None | 0 | No moving enemies. All dangers are fixed hazards. |

### Hazard roster

| Type | Width | Height | Count total | Count per level | Behavior |
| --- | ---: | ---: | ---: | --- | --- |
| `spiky_reed` | 16 | 10 | 33 | L1:3, L2:4, L3:5, L4:6, L5:7, L6:8 | Static spike strip, kills on touch. |
| `thorn_log` | 16 | 16 | 20 | L1:0, L2:2, L3:3, L4:4, L5:5, L6:6 | Static thorny log, kills on touch. |
| `bug_zapper` | 8 | 32 | 17 | L1:0, L2:0, L3:1, L4:3, L5:5, L6:8 | Static electric field, kills on touch. |

### Collectible roster

| Type | Width | Height | Count per level | Count total | Behavior |
| --- | ---: | ---: | ---: | ---: | --- |
| `fly` | 10 | 10 | 5 | 30 | Static pickup. Collected on touch. |

### Exit record

| Field | Type | Initial | Used by |
| --- | --- | --- | --- |
| `id` | number | level-specific | win test |
| `x` | number px | level design | collision |
| `y` | number px | level design | collision |
| `w` | number px | 20 | trigger |
| `h` | number px | 20 | trigger |
| `reached` | boolean | false | win state |

### Level record

| Field | Type | Used by |
| --- | --- | --- |
| `id` | number 0–5 | progression |
| `name` | string | UI |
| `seed` | number | deterministic RNG |
| `widthTiles`, `heightTiles` | number | bounds, camera |
| `tiles` | string[] | solid collision |
| `solids` | AABB[] | platforming |
| `parTime` | number s | scoring |
| `unlocked` | boolean | level select |
| `completed` | boolean | progression |
| `bestLevelScore` | number | high scores |
| `exit` | Exit | win |

### Score record

| Field | Type | Used by |
| --- | --- | --- |
| `runScore` | number | completed levels |
| `levelScore` | number | current level attempt |
| `flyScore` | number | collectibles |
| `exitScore` | number | exit |
| `timeBonus` | number | scoring |
| `noHitBonus` | number | scoring |
| `timeElapsed` | number s | scoring |
| `hitCount` | number | no-hit bonus |
| `noHit` | boolean | scoring |
| `setComplete` | boolean | all flies in level |

### High score record

| Field | Type | Used by |
| --- | --- | --- |
| `score` | number | top 5 |
| `date` | ISO string | UI |
| `levelsCompleted` | number | UI |
| `levelScores` | number[] | detail |
| `bestLevel[levelId]` | number | level select |

### Settings record

| Field | Type | Default | Used by |
| --- | --- | --- | --- |
| `keyMap` | action -> string[] | defaults | input |
| `reducedMotion` | boolean | browser preference | effects/camera |
| `colorSafeAlways` | boolean | true | visual |

### Particle record

| Field | Type | Used by |
| --- | --- | --- |
| `x`, `y` | number px | render |
| `vx`, `vy` | number px/s | motion |
| `life`, `maxLife` | number s | fade |
| `color` | hex | render |
| `size` | number px | render |

## 4.1 Input and remapping (Tier 1 default, Tier 2 remapping)

| Action | Default keys | Purpose |
| --- | --- | --- |
| `left` | `ArrowLeft`, `KeyA` | Move left. |
| `right` | `ArrowRight`, `KeyD` | Move right. |
| `jump` | `Space`, `ArrowUp`, `KeyW` | Jump and variable jump cut. |
| `pause` | `KeyP`, `Escape` | Pause/resume. |
| `restart` | `KeyR` | Restart current level. |
| `confirm` | `Enter` | Activate UI control. |
| `back` | `Escape` | Return in UI. |

Rules:

- Input state is sampled once per fixed step.
- `justPressed` means pressed on the first sampled step.
- `justReleased` means released on the first sampled step.
- Remapping allows one action per key mapping list.
- A key may be bound to multiple actions only if `pause`, `restart`, `back`, or `confirm` are not being used for movement/jump.
- If a key is assigned to two movement/jump actions, the last assignment wins and the old binding is removed.
- Browser reserved keys are ignored: `F5`, `F11`, `Ctrl`, `Shift`, `Alt`, `Meta`.
- Settings store key codes, not characters.

## 4.2 Platforming (Tier 1)

Movement rules:

- If `left` is held:
  - Accelerate left at 1500 px/s² on ground or 1000 px/s² in air.
- If `right` is held:
  - Accelerate right at 1500 px/s² on ground or 1000 px/s² in air.
- If neither direction is held:
  - Apply ground friction 1800 px/s² if grounded.
  - Apply air drag 200 px/s² if airborne.
- Horizontal speed is clamped to 180 px/s.
- Gravity is applied every step: `vy += 2000 * dt`.
- Fall speed is clamped to 950 px/s.

Jump rules:

- Jump is allowed if:
  - `grounded` is true, or
  - `coyoteTimer > 0`.
- On jump:
  - `vy = -650`
  - `grounded = false`
  - `coyoteTimer = 0`
  - `jumpBufferTimer = 0`
  - `jumpCutAvailable = true`
- If `jump` is pressed while airborne:
  - `jumpBufferTimer = 0.11`
- If landing occurs while `jumpBufferTimer > 0`:
  - Jump immediately.
- If grounded and not jumping:
  - `coyoteTimer = 0.08`
- If grounded becomes false without jumping:
  - `coyoteTimer` counts down from 0.08.
- If `jump` is released while `vy < -100` and `jumpCutAvailable` is true:
  - `vy *= 0.45`
  - `jumpCutAvailable = false`

Collision rules:

- Solid tiles are AABBs aligned to 16 px grid.
- Player AABB is 10x12.
- Resolve X first, then Y.
- If Y resolution pushes player upward, set `grounded = true`.
- If player leaves solid ground, set `grounded = false`.
- No slopes, no one-way platforms, no wall jumping.

Camera rules:

- Camera target centers the player unless inside deadzone.
- Deadzone:
  - Horizontal: 32 px.
  - Vertical: 24 px.
- Follow smoothing:
  - `camera.x += (targetX - camera.x) * (1 - exp(-10 * dt))`
  - Same for `camera.y`.
- Clamp camera to level bounds.
- Render camera position rounded to integer pixels.
- If reduced motion is enabled:
  - Skip smoothing and set camera directly to clamped target.

## 4.3 Hazards (Tier 1)

Hazard types:

| Type | Hitbox | Touch result | Animation |
| --- | --- | --- | --- |
| `spiky_reed` | 16x10 | Kill. | Pulse 2 frames at 0.25s. |
| `thorn_log` | 16x16 | Kill. | Static. |
| `bug_zapper` | 8x32 | Kill. | Pulse 2 frames at 0.15s. |

Rules:

- Hazards are fixed in place.
- Hazards never move, rotate, shoot, or change hitbox.
- Every hazard hitbox is active at all times.
- If player AABB intersects hazard AABB:
  - Set `player.alive = false`.
  - Set `player.state = "hurt"`.
  - Set `hitCount += 1`.
  - Set `noHit = false`.
  - Set `hitFlashTimer = 0.25`.
  - Spawn 8 hazard-color particles.
  - Play `hazard_hit`.
  - Start `deathTimer = 0.9`.
- While dead:
  - Player input is ignored.
  - Physics is ignored.
  - Hazards and collectibles do not update.
- After 0.9 seconds:
  - Reset player position, velocity, timers.
  - Reset hazards animation only.
  - Reset collectibles to uncollected.
  - Reset level timer and level score.
  - Keep `runScore` from completed levels.
- Pressing `restart` during play performs the same immediate reset without waiting.

## 4.4 Exit and failure restart (Tier 1 single level, Tier 3 full sequence)

Exit rules:

- Exit trigger AABB is 20x20.
- If player AABB intersects exit AABB:
  - Set `exit.reached = true`.
  - Play `level_win`.
  - Finalize level score.
  - Add `levelScore` to `runScore`.
  - Mark level completed.
  - If Tier 3, unlock next level.
  - Enter win state.

Failure rules:

- Losing is only caused by hazard touch.
- There is no lose screen.
- Death restarts the level automatically.
- The player may also press `restart` to restart immediately.

## 4.5 Collectibles (Tier 2)

Collectible rules:

- Each level has exactly 5 flies.
- Fly hitbox is 10x10.
- If player AABB intersects fly AABB:
  - Set `collected = true`.
  - Increment `collectedCount`.
  - Add 100 to `flyScore`.
  - Spawn 6 yellow particles.
  - Play `collect`.
- Flies do not respawn until level reset.
- If `collectedCount == 5`:
  - Set `setComplete = true`.
  - Play `collect` a second time as a short set-complete jingle.
- Collecting all flies is optional. It only affects score.

## 4.6 Scoring and high scores (Tier 2)

Score components:

| Component | Points | Condition |
| --- | ---: | --- |
| Exit | 500 | Reach exit. |
| Fly | 100 each | Collect fly. |
| Time bonus | 0–500 | Finish faster than par. |
| No-hit bonus | 200 | Finish with `hitCount == 0`. |

Maximum per level:

```text
500 + 500 + 500 + 200 = 1700
```

Maximum total for 6 levels:

```text
1700 * 6 = 10200
```

Time bonus formula:

```text
if timeElapsed <= parTime:
  timeBonus = 500
else if timeElapsed >= 2 * parTime:
  timeBonus = 0
else:
  timeBonus = floor(500 * (2 * parTime - timeElapsed) / parTime)
```

No-hit bonus:

```text
if hitCount == 0:
  noHitBonus = 200
else:
  noHitBonus = 0
```

Level restart:

- Resets `timeElapsed`, `hitCount`, `noHit`, `flyScore`, `exitScore`, `timeBonus`, `noHitBonus`, `levelScore`, `collectedCount`.
- Does not reset `runScore` from completed previous levels.

High scores:

- On winning a level, store `bestLevelScore` for that level.
- On completing the full run:
  - Create record:
    ```js
    {
      score: runScore,
      date: new Date().toISOString(),
      levelsCompleted: 6,
      levelScores: [level0Score, level1Score, level2Score, level3Score, level4Score, level5Score]
    }
    ```
  - Insert into `top5`.
  - Sort descending by `score`.
  - Keep top 5.
  - Save to LocalStorage.

## 4.7 Camera (Tier 1)

Camera rules:

- Screen size: 480x270.
- Camera position is top-left of viewport.
- Target:
  ```text
  targetX = player.x + player.w/2 - 240
  targetY = player.y + player.h/2 - 135
  ```
- If player is inside deadzone, keep current camera target.
- Clamp:
  ```text
  0 <= camera.x <= level.widthPx - 480
  0 <= camera.y <= level.heightPx - 270
  ```
- If level height is 270 or less, `camera.y = 0`.
- Render uses integer camera coordinates.

## 4.8 Effects (Tier 1)

Particles:

| Effect | Count | Color | Life | Velocity |
| --- | ---: | --- | ---: | --- |
| Jump dust | 4 | `#A855F7` | 0.25s | Random upward and sideways. |
| Land dust | 2 | `#A855F7` | 0.2s | Random sideways. |
| Collect fly | 6 | `#FFD400` | 0.5s | Random outward. |
| Hazard hit | 8 | `#FF2E63` | 0.6s | Random outward. |
| Exit | 10 | `#00E5FF` | 0.6s | Random outward. |

Hit flash:

- On hazard hit:
  - Draw a white rectangle over the player hitbox for 0.25s.
- Reduced motion:
  - Do not draw hit flash.
  - Do not spawn particles.
  - Use a static outline instead.

## Progression and difficulty

Level roster:

| Level | Name | Tiles | Pixels | Hazards | Flies | Par |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| 1 | Ribbon Reeds | 40x17 | 640x272 | 3 spiky reed | 5 | 45s |
| 2 | Lily Pad Hop | 50x17 | 800x272 | 4 spiky, 2 thorn | 5 | 60s |
| 3 | Mud Flap | 60x17 | 960x272 | 5 spiky, 3 thorn, 1 zapper | 5 | 75s |
| 4 | Bullfrog Bounce | 60x20 | 960x320 | 6 spiky, 4 thorn, 3 zapper | 5 | 90s |
| 5 | Dragonfly Docks | 70x20 | 1120x320 | 7 spiky, 5 thorn, 5 zapper | 5 | 105s |
| 6 | Fly Flurry Finale | 80x20 | 1280x320 | 8 spiky, 6 thorn, 8 zapper | 5 | 120s |

Total par time:

```text
45 + 60 + 75 + 90 + 105 + 120 = 495 seconds = 8.25 minutes
```

Progression rules:

- Level 1 starts unlocked.
- Completing a level unlocks the next level.
- Level select shows completed levels and unlocked levels.
- Locked levels show a padlock silhouette and cannot be selected.
- Replaying a completed level does not reduce `runScore` unless the player starts a new run.
- Full run win happens after level 6.

Difficulty curve:

- Level 1: basic jump timing, 3 hazards, no zappers.
- Level 2: longer gaps and thorn logs.
- Level 3: introduces bug zappers.
- Level 4: introduces vertical camera movement.
- Level 5: denser hazard routes.
- Level 6: longest route, most zappers, most flies hidden on optional ledges.

Feel:

- Max jump height: about 106 px, roughly 6.6 tiles.
- Full jump horizontal distance: about 117 px, roughly 7.3 tiles.
- Intended maximum safe gap: 96 px, 6 tiles.
- Intended maximum safe step-up: 80 px, 5 tiles.
- Coyote and buffer make jumps forgiving.
- Variable jump height makes short hops possible.

# 5. CHARACTERS

## Player silhouette

Pip is a compact frog:

- Wide head.
- Big eyes.
- Wide mouth.
- Short limbs.
- Webbed feet.
- Facing is left or right only.
- Body color is bright blue.
- Eyes are white with black pupils.
- Black outline everywhere.

## Player states and animations

| State | Animation | Frames | Timing | Trigger |
| --- | --- | ---: | --- | --- |
| idle | `idle` | 2 | 0.4s per frame | Grounded, no input. |
| run | `run` | 4 | 0.1s per frame | Grounded, horizontal speed > 20. |
| jump | `jump` | 1 | static | `vy < 0`. |
| fall | `fall` | 1 | static | `vy > 0` and not grounded. |
| hurt | `hurt` | 1 | static | `alive == false`. |

Facing rules:

- `facing = 1` when moving right or aiming right.
- `facing = -1` when moving left or aiming left.
- No vertical facing.
- Sprite flips horizontally.

Reduced motion:

- Idle and run animations remain but use only 1 frame.
- No particle motion.
- No hit flash.
- Camera snap.

## Object silhouettes

| Object | Silhouette |
| --- | --- |
| Spiky reed | Low magenta spike strip. |
| Thorn log | Purple log with magenta thorns. |
| Bug zapper | Thin orange/magenta electric rod. |
| Fly | Yellow body with two small wings. |
| Exit | Large lily pad ring with white arrow. |

# 6. AUDIO

All audio is synthesized with Web Audio. Audio is unlocked on first user input. Master gain is 0.3. No external audio files are required.

## Sound effects

| Name | Recipe | Plays when |
| --- | --- | --- |
| `jump` | Square oscillator, 440 Hz to 660 Hz over 0.12s, gain 0.35, attack 0.01s, decay 0.11s. | Player jumps. |
| `land` | Square oscillator, 160 Hz to 80 Hz over 0.08s, gain 0.25. | Player becomes grounded after falling > 60px. |
| `collect` | Two square notes: 880 Hz 0.08s, 1320 Hz 0.08s, gain 0.3. | Fly collected. |
| `set_complete` | Three square notes: 880, 1100, 1320 at 0.07s each, gain 0.3. | All 5 flies collected. |
| `hazard_hit` | Sawtooth 300 Hz to 80 Hz over 0.25s plus noise burst 0.12s, gain 0.45. | Player touches hazard. |
| `level_win` | Square arpeggio: C5 523.25, E5 659.25, G5 783.99, C6 1046.50, each 0.08s, gain 0.35. | Player reaches exit. |
| `restart` | Square 440 Hz to 220 Hz over 0.12s, gain 0.3. | Manual restart. |
| `ui_move` | Square 520 Hz, 0.03s, gain 0.25. | Menu navigation. |
| `ui_select` | Square 660 Hz, 0.05s, gain 0.3. | Menu confirm. |
| `pause` | Square 330 Hz, 0.08s, gain 0.25. | Pause opens. |
| `unpause` | Square 440 Hz, 0.08s, gain 0.25. | Pause closes. |
| `error` | Square 160 Hz, 0.12s, gain 0.3. | Invalid key binding. |

## Music

| Track | Recipe | Plays when |
| --- | --- | --- |
| `title_theme` | 120 BPM, square lead, triangle bass, noise hats. 8-bar loop. Lead pattern: C4, Eb4, F4, Bb4. Bass: C2, Ab2. Gain 0.2. | Title, level select, high scores. |
| `level_theme` | 140 BPM, square lead, triangle bass, noise drums. 8-bar loop. Lead: G4, Bb4, C5, D5. Bass: G2, Eb2. Gain 0.2. | Level play. |
| `win_fanfare` | One-shot arpeggio: C5, E5, G5, C6, E6, G6, each 0.09s, square, gain 0.35. | Level win. |
| `game_complete_fanfare` | 2s fanfare using square lead and triangle bass. C major arpeggio ending on C6. | Full run win. |

Reduced motion does not mute audio.

# 7. UX

All screens and HUD are HTML/CSS. The game canvas is separate. UI state is controlled by `state.js`, but DOM rendering is HTML/CSS only.

## Typography

- Font: `PixelFont`, bitmap, blocky.
- Fallback: `monospace`.
- Size: 10px logical, scaled by integer browser zoom.
- Text color: `#F7F7F7`.
- Focus outline: 2px `#FFD400`.
- No anti-aliased UI fonts.

## State machine

| State | Enter from | Allowed transitions | Controls |
| --- | --- | --- | --- |
| TITLE | Start, quit to title | LEVEL_SELECT, SETTINGS, HIGH_SCORES, PLAYING | Start, Level Select, Settings, High Scores. |
| LEVEL_SELECT | Title, pause, win, high scores | PLAYING, SETTINGS, TITLE | Select unlocked level, back. |
| SETTINGS | Any menu/pause/win | Return to previous state | Remap keys, reduced motion, back. |
| PLAYING | Title, level select, resume | PAUSED, WIN, SETTINGS | Game input. |
| PAUSED | PLAYING | PLAYING, SETTINGS, LEVEL_SELECT, TITLE | Resume, restart level, settings, quit. |
| WIN | PLAYING | LEVEL_SELECT, HIGH_SCORES, TITLE, PLAYING next level | Continue, level select, high scores, title. |
| HIGH_SCORES | TITLE, WIN, LEVEL_SELECT | LEVEL_SELECT, TITLE | Back. |

## Screen contents

### Title

- Game title: “Pip Pond Hop”
- Buttons:
  - Start
  - Level Select
  - Settings
  - High Scores

### Pause

- Buttons:
  - Resume
  - Restart Level
  - Settings
  - Quit to Title

### Settings

- Remappable key list:
  - Left
  - Right
  - Jump
  - Pause
  - Restart
  - Confirm
  - Back
- Reduced motion toggle.
- Back button.

### Win

- Level score breakdown:
  - Exit points
  - Fly points
  - Time bonus
  - No-hit bonus
- Buttons:
  - Continue if next level exists.
  - Level Select
  - High Scores
  - Title

### Level Select

- Grid of 6 levels.
- Unlocked levels show name and best score.
- Locked levels show padlock.
- Back button.

### High Scores

- Top 5 total run scores.
- Best level scores.
- Back button.

## HUD

| Element | Record field | When visible |
| --- | --- | --- |
| `#hud-score` | `score.runScore + score.levelScore` | PLAYING and PAUSED. Hidden elsewhere. |

HUD markup:

```html
<div id="hud" aria-hidden="false">
  <span id="hud-score">0</span>
</div>
```

CSS:

```css
#hud {
  position: absolute;
  left: 8px;
  top: 8px;
  font-family: "PixelFont", monospace;
  color: #F7F7F7;
  text-shadow: 2px 2px 0 #0B1D2A;
}
```

## Accessibility

- Color is never the only signal.
- All menu actions are keyboard accessible.
- Focus outline is visible.
- Reduced motion disables:
  - Particles.
  - Hit flash.
  - Camera smoothing.
  - UI animations.
- Remappable keys cover all actions.
- Default palette is colour-blind safe.

# 8. DEBUG API

Each gameplay system has one direct debug function.

| Function | Purpose | Commands |
| --- | --- | --- |
| `debugPlatforming(cmd, payload)` | Inspect and change player physics. | `get`, `set`, `step`, `setGrounded`, `reset` |
| `debugHazards(cmd, payload)` | Inspect and change hazards. | `get`, `set`, `hitTest`, `reset` |
| `debugCollectibles(cmd, payload)` | Inspect and change collectibles. | `get`, `collect`, `reset`, `remaining` |
| `debugScoring(cmd, payload)` | Inspect and change score. | `get`, `add`, `setTime`, `finalize`, `reset` |
| `debugLevel(cmd, payload)` | Inspect and change level state. | `get`, `load`, `reset`, `win`, `unlock` |
| `debugCamera(cmd, payload)` | Inspect and change camera. | `get`, `set`, `clamp` |
| `debugEffects(cmd, payload)` | Inspect and change particles/hit flash. | `get`, `spawn`, `setHitFlash`, `clear` |

Input debug functions:

| Function | Purpose |
| --- | --- |
| `debugInput(action, state)` | Set an action to `down`, `up`, `pressed`, or `released`. |
| `debugGetInput(action)` | Return current input state for an action. |

Example:

```js
debugInput("right", "down");
debugPlatforming("step", { dt: 1/60 });
debugHazards("hitTest", { x: 10, y: 20, w: 10, h: 12 });
```

# 9. TESTS

| Test | Tier | Steps | Pass condition |
| --- | --- | --- | --- |
| Fixed step runs | 1 | Start loop, request frames. | Simulation advances in exact 1/60 steps. |
| Title to play | 1 | Press confirm on Start. | State becomes PLAYING and level 1 loads. |
| Horizontal movement | 1 | Press right, step 30 frames. | Player x increases. |
| Jump only when grounded | 1 | Press jump in air. | `vy` unchanged unless coyote/buffer. |
| Gravity applies | 1 | Force airborne player. | `vy` increases by 2000*dt each step. |
| Ground collision | 1 | Drop player onto solid tile. | Player stops, grounded true. |
| Hazard kill | 1 | Place player on spiky reed. | Player dies, particles spawn, restart timer starts. |
| Restart level | 1 | Trigger death, wait 0.9s. | Level resets to start. |
| Exit win | 1 | Place player on exit. | State becomes WIN. |
| HUD score exists | 1 | Enter PLAYING. | `#hud-score` visible. |
| Pause stops simulation | 1 | Press pause. | Player/camera/effects do not update. |
| Pixel style | 1 | Render canvas. | Image is 480x270 logical, scaled pixelated. |
| Audio unlock | 1 | Press any key. | Audio context unlocked, music can play. |
| Collectible pickup | 2 | Place player on fly. | Fly collected, score +100, particles spawn. |
| Score formula | 2 | Set time, hits, flies, call finalize. | Score matches formula. |
| High score save | 2 | Submit run score, reload. | Top 5 persists. |
| Remap key | 2 | Bind jump to KeyZ, press KeyZ. | Jump action fires. |
| Reduced motion | 2 | Enable reduced motion, trigger hazard hit. | No particles, no hit flash, no camera smoothing. |
| Level unlock | 3 | Complete level 1. | Level 2 unlocked. |
| Level select | 3 | Open level select, choose unlocked level. | Selected level loads. |
| Full sequence | 3 | Complete levels 1–6. | Full win state, top 5 run score saved. |
| Time budget | 3 | Sum level par times. | Total < 1800 seconds. |

# 10. BUILD ORDER

1. Create HTML shell, canvas, CSS reset, palette variables, pixel font.
2. Create fixed-step loop and global state.
3. Implement default input mapping and action sampling.
4. Implement camera clamping and integer render transform.
5. Implement level loader with tile grid and solid AABBs.
6. Implement player physics: gravity, horizontal movement, collision.
7. Implement jump, variable jump cut, coyote, buffer.
8. Implement level 1 with start, platforms, exit.
9. Implement static hazard records and hit detection.
10. Implement death, restart, and win states.
11. Add title, pause, and single-level win screens.
12. Add HUD score placeholder.
13. Add pixel art sprites and palette.
14. Add Web Audio unlock, SFX, and music.
15. Add particles and hit flash.
16. Add collectibles and fly pickup logic.
17. Add scoring, time bonus, no-hit bonus.
18. Add LocalStorage save and high scores.
19. Add settings screen with remappable keys and reduced motion.
20. Add level select and levels 2–6.
21. Add final win flow and full high score submission.
22. Run tests and tune level spacing.

# 11. DEFINITION OF DONE

## Tier 1: Core playable single level

High-level done:

- A player can start the game, play one short frog platforming level, die to hazards, restart, and win by reaching the exit.

Checkboxes:

- [ ] Fixed 60 Hz loop.
- [ ] Default keyboard controls work.
- [ ] Player moves left/right under acceleration and friction.
- [ ] Player jumps under gravity.
- [ ] Collision stops player on solid tiles.
- [ ] Coyote and jump buffer work.
- [ ] Hazard touch kills player.
- [ ] Death restarts level after 0.9s.
- [ ] Exit touch wins level.
- [ ] Title screen can start level.
- [ ] Pause stops simulation.
- [ ] Win screen appears.
- [ ] HUD score element exists.
- [ ] Canvas renders 480x270 pixel art.
- [ ] Palette matches Visual Spec.
- [ ] Player has idle/run/jump/fall/hurt animations.
- [ ] Hazard and exit visuals match recipe.
- [ ] Particles and hit flash appear.
- [ ] Audio unlock works.
- [ ] Jump, land, hit, exit sounds play.
- [ ] Music plays during level.

## Tier 2: Supporting mechanics and accessibility

High-level done:

- The Tier 1 game awards score, records best scores, lets players collect flies, remap keys, and reduce motion.

Checkboxes:

- [ ] Each level has 5 flies.
- [ ] Flies are collected on touch.
- [ ] Fly score is 100 each.
- [ ] Exit score is 500.
- [ ] Time bonus formula works.
- [ ] No-hit bonus works.
- [ ] Level restart resets level score.
- [ ] Completed-level run score persists.
- [ ] High scores save to LocalStorage.
- [ ] High scores display top 5 and best level scores.
- [ ] Settings screen exists.
- [ ] All actions are remappable.
- [ ] Reduced motion disables particles, hit flash, camera smoothing, UI motion.
- [ ] Reduced motion does not change gameplay hitboxes or physics.
- [ ] Tests for score formula and remapping pass.

## Tier 3: Full sequence

High-level done:

- The game has six levels, level select, progression, and a full-run win.

Checkboxes:

- [ ] Levels 1–6 load from JSON.
- [ ] Level dimensions match roster.
- [ ] Hazard counts match roster.
- [ ] Fly counts match roster.
- [ ] Par times match roster.
- [ ] Completing a level unlocks the next.
- [ ] Level select shows locked/unlocked levels.
- [ ] Level select loads selected unlocked level.
- [ ] Full run win appears after level 6.
- [ ] Full run high score is saved.
- [ ] Total par time is under 1800 seconds.
- [ ] All levels are finishable with max jump height 106px and max horizontal jump distance ~117px.
- [ ] All tests for Tier 3 pass.

# A. SANITY

| Check | Result | Notes |
| --- | --- | --- |
| Exact required screens only | Pass | Title, pause, settings, win, level select, high scores. Playing and paused are game states, not extra screens. |
| HUD only score | Pass | HUD table has only score. |
| No extra mechanics | Pass | No enemies, no powerups, no dash, no double jump, no combat. |
| Hazards fixed in place | Pass | Hazard types have fixed AABBs and never move. |
| Collectibles are a set | Pass | 5 flies per level, set complete at 5. |
| Scoring records best scores | Pass | Top 5 run scores and best level scores. |
| Failure restarts level | Pass | Hazard death auto-restarts after 0.9s. |
| Win by reaching exit | Pass | Exit trigger wins level. |
| Size under 30 minutes | Pass | Total par 495 seconds. |
| 2D side-on | Pass | Side-on camera and 2D level records. |
| Real-time | Pass | Fixed 60 Hz real-time loop. |
| Free movement | Pass | Continuous velocity AABB physics. |
| Pixel art low-res | Pass | 480x270 logical canvas, 16px tiles, pixelated rendering. |
| Limited saturated palette | Pass | 12-color palette. |
| Colour-blind safe | Pass | Avoids red/green critical distinction; uses shape and luminance. |
| Reduced motion | Pass | Settings and rules defined. |
| Remappable keys | Pass | Actions and settings defined. |
| Chiptune music | Pass | Web Audio recipes provided. |
| Retro bleep SFX | Pass | Synthesized recipes provided. |
| Particles and hit flash | Pass | Effect records and rules provided. |
| Tier 1 includes art and sound | Pass | Tier 1 includes style, audio, particles, HUD. |
| Tier 2 adds supporting mechanics only | Pass | Collectibles and scoring are Tier 2. |
| Tier 3 adds content only | Pass | Level sequence is Tier 3. |
| Contracts include all fields | Pass | Global context includes player, hazards, collectibles, score, settings, high scores, camera, effects. |
| Contracts include test functions | Pass | Debug API includes direct system access. |
| Numbers are consistent | Pass | Physics, levels, scores, par times, counts are internally consistent. |