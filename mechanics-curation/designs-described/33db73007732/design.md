# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Game about frogs eating bugs | Player is a frog; bugs are catchable targets; `Catching` system is the core mechanic. |
| 2d | Logical canvas is a flat 2D top-down scene: 960 x 640 px. |
| camera: top-down | Fixed top-down camera; no scrolling, no zoom, no rotation. |
| time model: real-time | Fixed 60 Hz simulation loop; real-time player actions. |
| movement model: free movement | Player moves continuously with keyboard movement actions. |
| session shape: endless | No level completion, no win condition, no hard timer cap. |
| failure: lose a life | Bugs escaping cause `lives.value -= 1`; game over at 0 lives. |
| tone: silly | Frog character, bug names, hand-lettered UI, chiptune bleeps, exaggerated tongue. |
| size: one screen, a few minutes | One fixed screen; difficulty curve targets 3-8 minute typical runs but no artificial cap. |
| win/lose: survive as long as possible, no ending, play forever | Endless survival; game over only when lives reach 0. |
| core mechanics: catching | Tier 1: tongue catching of moving bugs before they escape. |
| supporting mechanics: scoring | Tier 2: points, combo multiplier, high scores, ranks. |
| extra mechanics: none | No traps, pickups, power-ups, weapons, tools, shops, upgrades, or secondary modes. |
| art style: flat vector | Canvas vector shapes, solid fills, crisp outlines, no gradients, no textures. |
| palette: saturated | Bright, strong, colour-blind-safe palette in Section 3. |
| typography: hand-lettered | UI font stack and hand-drawn transforms in Section 3 and Section 7. |
| music: chiptune | Web Audio synthesized chiptune loop in Section 6. |
| sound effects style: retro bleeps | Web Audio synthesized square/triangle/noise bleeps in Section 6. |
| screens: title, pause, game over, high scores | UI state machine in Section 7. |
| hud: health, score, combo counter | HUD table in Section 7. |
| effects: particles, hit flash | Effects system in Section 4 and Section 3. |
| accessibility: colour-blind safe palette, reduced motion, remappable keys, difficulty options | Palette, reduced-motion rules, input remapping, difficulty tables in Sections 3, 4, 7. |

## 0.2 Decisions

| Decision | Source | Final ruling | Why |
| --- | --- | --- | --- |
| Player identity | User: “frogs eating bugs” | Player is “Frogbert”, a round flat-vector pond frog with a long silly tongue. | Directly satisfies frog-eating-bugs and supports tongue catching. |
| What are “enemies” | User: no extra mechanics | There are no enemy systems. Bugs are targets, not enemies. | Prevents adding combat or enemy behaviour beyond catching. |
| Traps | User: extra mechanics none | No traps. | Extra mechanics are forbidden. |
| Pickups | User: extra mechanics none | No pickups, power-ups, or consumables. | Extra mechanics are forbidden. |
| Core catching method | Open | Press Catch key to shoot a tongue segment in facing direction; tongue catches bugs inside its segment hitbox. | Gives a named input, clear skill, and fits frog fantasy. |
| Failure trigger | Open | A bug escapes when it crosses the escape boundary; this loses one life. | Makes “before they get away” concrete. |
| Bug roster | Open | Exactly 4 bug types: Housefly, Mosquito, Dragonfly, Firefly. | Provides variety without adding systems. |
| Bug escape model | Open | Each bug has an `escapeTimer`; when expired it dashes to nearest edge; crossing edge loses a life. | Readable, testable, and fits “get away”. |
| Lives | Open | Easy 5 lives, Normal 3 lives, Hard 2 lives. | Supports difficulty options and failure system. |
| Life loss recovery | Open | On life loss, 1.2 s grace: no new spawns, bugs become `startled`, no further life loss. | Prevents instant double deaths and keeps runs fair. |
| World size | Open | 960 x 640 logical px; safe area inset 28 px from each edge. | One screen, browser-safe, consistent units. |
| Player movement | Open | Direct velocity from input, clamped to safe area. | Simple, responsive, testable free movement. |
| Facing | Open | Facing follows last non-zero movement direction. | Gives tongue aiming without mouse. |
| Input | Open | Keyboard only by default; actions remappable. | Matches remappable keys requirement; avoids extra input systems. |
| Catch input | Open | Default `Space` or `J`; edge-triggered. | One clear named input for core mechanic. |
| Pause | Open | Default `Esc` or `P`; pause screen exists. | Required screen and real-time safety. |
| Difficulty options | Accessibility requirement | Easy, Normal, Hard selectable from title/pause. | Required accessibility option; changes numeric constants only. |
| Reduced motion | Accessibility requirement | Detects OS `prefers-reduced-motion`; also toggle. Reduces particles, flash, wobble. | Required accessibility option. |
| Colour-blind safety | Accessibility requirement | Palette uses shapes, labels, and colour-blind-safe colours. | Required accessibility option. |
| Scoring | Supporting mechanic | Points per bug; combo multiplier increases on consecutive catches within 3.0 s; cap multiplier 10. | Required scoring and combo. |
| High scores | Supporting mechanic | LocalStorage top 10 high scores. | Required high scores. |
| Ranks | Supporting mechanic | Score thresholds determine rank label. | Required ranks. |
| High score persistence | Open | `localStorage` key `frog-snack-highscores-v1`. | Browser-local persistence; no backend. |
| Screens | Required list | Only title, pause, game over, high scores. Settings are embedded in title/pause, not a new screen. | Matches exact screens list. |
| HUD | Required list | Health, score, combo counter only. | Exact HUD parts. |
| Effects | Required list | Particles and hit flash only. | Exact effects parts. |
| Art style | Required | Flat vector canvas drawing with solid fills and crisp outlines. | Matches chosen style. |
| Palette | Required | Saturated but colour-blind-safe palette with distinct shapes. | Matches palette and accessibility. |
| Typography | Required | Hand-lettered fallback stack and irregular CSS transforms. | Matches typography without external assets. |
| Audio | Required | Web Audio synthesized chiptune music and retro bleeps. | Matches music and SFX style. |
| RNG | Open | Seeded deterministic RNG for all gameplay randomness. | Testability and reproducibility. |
| Time scaling | Open | Continuous difficulty scaling by run time, plus Easy/Normal/Hard modifiers. | Endless survival needs progression. |
| Typical run length | User: “a few minutes” vs endless | No hard cap; tuning targets 3-8 minute typical failures, but can continue forever. | Resolves contradiction without breaking endless requirement. |
| Module language | Open | Vanilla JavaScript, no build tools, no external libraries. | Easy for agent to build in browser. |
| Rendering | Open | HTML/CSS for UI; Canvas 2D for game entities. | Keeps UX HTML/CSS while allowing simple vector gameplay. |

## 0.3 Tiers

Priority list. Tier 1 must be complete enough to play and fail. Higher tiers may be left unbuilt.

1. **Tier 1 - Core catching game**
   - Fixed real-time loop.
   - Default keyboard input.
   - Player frog free movement.
   - Tongue catching.
   - Four bug target types.
   - Bug spawning, wandering, avoidance, escaping.
   - Life loss when bugs escape.
   - Game over at 0 lives.
   - Title, pause, game over screens.
   - HUD health, score placeholder, combo placeholder.
   - Flat vector art, saturated colour-blind-safe palette, hand-lettered UI.
   - Chiptune music, retro bleeps.
   - Particles and hit flash.
   - Reduced-motion detection and keymap data structure.
   - Normal difficulty constants.

2. **Tier 2 - Scoring and high scores**
   - Points per catch.
   - Combo counter and combo timer.
   - Combo multiplier.
   - Ranks.
   - High score storage.
   - High scores screen.
   - Game over high score insertion and new-high-score display.

3. **Tier 3 - Accessibility and difficulty UI**
   - Easy/Normal/Hard selection UI.
   - Remappable key UI.
   - Reduced motion toggle.
   - Settings persistence.
   - Extra polish, debug tooling, and test coverage.

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Item | Value |
| --- | --- |
| Logical canvas size | 960 x 640 px |
| Coordinate origin | Top-left of canvas |
| X axis | Positive right |
| Y axis | Positive down |
| Angle zero | 0 radians points right |
| Angle positive | Clockwise |
| Speed units | px/s |
| Acceleration units | px/s² |
| Time units | seconds |
| Fixed timestep | `dt = 1 / 60` |
| Simulation update rate | 60 Hz fixed step |
| Render rate | requestAnimationFrame |
| Safe play bounds | `{ left: 28, right: 932, top: 28, bottom: 612 }` |
| Spawn inset from safe bounds | 90 px |
| Escape boundary margin | Bug center crossing safe bounds by 12 px causes escape life loss |
| Player radius | 22 px |
| Tongue half-width collision radius | 8 px |
| Bug radii | 7-12 px per type |
| Minimum player-bug spawn distance | 180 px |
| Catch input edge duration | One simulated frame |
| Catch cooldown | 0.30 s |
| Catch tongue duration | 0.12 s |
| Combo timer | 3.0 s |
| Life loss grace | 1.2 s |
| Hit flash duration | 0.18 s normal, 0.08 s reduced motion |
| Particle lifetime | 0.45 s normal, 0.0 s reduced motion |

## 1.2 Important conventions

| Rule | Detail |
| --- | --- |
| Determinism | All randomness uses `Game.rand()` backed by seeded `mulberry32`. Never call `Math.random()` in gameplay systems. |
| RNG seed | Seeded from `Date.now()` unless debug sets `ctx.run.seed`. |
| Fixed step | Accumulator loop. Simulation only advances in exact `1/60` steps. |
| State ownership | Systems mutate only records they own. UI reads state. Render reads state. Input writes input state only. |
| UI separation | Screens and HUD are HTML/CSS. Gameplay entities are Canvas 2D. |
| No external assets | Fonts use system fallbacks. Audio is synthesized. No image or audio files. |
| Collision | Circle-circle for bounds. Segment-circle for tongue. |
| Bounds | Player center is clamped to safe bounds. Bugs may briefly cross safe bounds while escaping. |
| Input | Actions are logical strings, not key codes. Key codes map to actions. |
| Reduced motion | Core movement remains. Particles, screen flashes, wobble, and cosmetic animation are reduced. |
| Colour-blind safety | Do not encode gameplay meaning by colour alone. Bug types must have distinct shapes and labels. |
| Persistence | High scores and settings stored in `localStorage` under versioned keys. |
| Pause | Paused state stops simulation but keeps render and UI. |
| Game over | Game over stops simulation. Restart resets run records only, not settings or high scores. |
| Error handling | Any exception in a system resets run to title rather than leaving broken play state. |

# 2. CONTRACTS

## 2.1 Module layout

| Path | Responsibility |
| --- | --- |
| `index.html` | Canvas, HUD, screens, settings controls, debug root. |
| `style.css` | Flat vector UI, hand-lettered typography, screens, HUD, accessibility states. |
| `src/main.js` | Bootstrap, canvas setup, fixed loop, mode routing. |
| `src/constants.js` | Numeric constants, palettes, bug roster, difficulty table, rank table. |
| `src/rng.js` | Seeded RNG and `Game.rand()`. |
| `src/context.js` | Create global context, reset run, apply settings. |
| `src/input.js` | Key map, action state, edge detection, remap validation. |
| `src/player.js` | Player movement, facing, tongue state. |
| `src/catching.js` | Tongue activation, segment collision, catch handling. |
| `src/bugs.js` | Bug records, bug behaviour, escape state. |
| `src/spawn.js` | Spawn timing, type weighting, active cap. |
| `src/lives.js` | Life loss, grace, game over trigger. |
| `src/scoring.js` | Score, combo, multiplier, rank. |
| `src/highscores.js` | Local high score storage and ranking. |
| `src/effects.js` | Particles, hit flash. |
| `src/audio.js` | Web Audio music and SFX. |
| `src/render.js` | Canvas vector rendering. |
| `src/ui/hud.js` | HUD DOM updates. |
| `src/ui/screens.js` | Screen state machine and DOM overlays. |
| `src/debug.js` | Debug API. |

## 2.2 Global context

The single global context object is `window.frogGame`.

```js
window.frogGame = {
  schemaVersion: 1,
  mode: "title", // "title" | "playing" | "paused" | "gameover" | "highscores"
  settings: {
    difficulty: "normal", // "easy" | "normal" | "hard"
    reducedMotion: false,
    keyMap: {
      moveUp: ["KeyW", "ArrowUp"],
      moveDown: ["KeyS", "ArrowDown"],
      moveLeft: ["KeyA", "ArrowLeft"],
      moveRight: ["KeyD", "ArrowRight"],
      catch: ["Space", "KeyJ"],
      pause: ["Escape", "KeyP"],
      restart: ["KeyR"],
      uiSelect: ["Enter", "Space"],
      uiUp: ["KeyW", "ArrowUp"],
      uiDown: ["KeyS", "ArrowDown"],
      uiLeft: ["KeyA", "ArrowLeft"],
      uiRight: ["KeyD", "ArrowRight"]
    }
  },
  run: {
    time: 0,
    frame: 0,
    seed: 0,
    gameOverReason: ""
  },
  player: {
    pos: { x: 480, y: 320 },
    vel: { x: 0, y: 0 },
    facing: 0,
    radius: 22,
    maxSpeed: 180,
    tongue: {
      active: false,
      time: 0,
      duration: 0,
      length: 150,
      cooldown: 0,
      segment: { x1: 0, y1: 0, x2: 0, y2: 0 }
    },
    hitFlash: 0,
    alive: true
  },
  bugs: [
    {
      id: 0,
      type: "fly",
      pos: { x: 0, y: 0 },
      vel: { x: 0, y: 0 },
      heading: 0,
      radius: 9,
      points: 10,
      speed: 55,
      baseSpeed: 55,
      escapeTimer: 12,
      baseEscapeTimer: 12,
      avoidRadius: 90,
      state: "wander", // "wander" | "escaping" | "startled" | "caught"
      wanderTimer: 0,
      jitterPhase: 0,
      startleTimer: 0,
      hitFlash: 0,
      alive: true
    }
  ],
  spawn: {
    timer: 0,
    nextId: 1,
    interval: 3.2,
    maxActive: 3,
    weights: { fly: 70, mosquito: 25, dragonfly: 5, firefly: 0 }
  },
  lives: {
    value: 3,
    max: 3,
    grace: 0
  },
  scoring: {
    score: 0,
    combo: 0,
    comboTimer: 0,
    maxCombo: 0,
    multiplier: 1,
    rank: "Tadpole"
  },
  effects: {
    particles: [
      {
        pos: { x: 0, y: 0 },
        vel: { x: 0, y: 0 },
        life: 0,
        maxLife: 0,
        color: "#ffffff",
        size: 0
      }
    ],
    hitFlash: {
      alpha: 0,
      decay: 0,
      reason: ""
    }
  },
  highScores: [
    {
      score: 0,
      time: 0,
      difficulty: "normal",
      rank: "Tadpole",
      date: "1970-01-01T00:00:00.000Z"
    }
  ],
  input: {
    actions: {},
    edges: {},
    lastPressed: null
  },
  debug: {
    enabled: false
  }
};
```

## 2.3 Module specifics

| Module | Required functions | Inputs | Outputs / side effects |
| --- | --- | --- | --- |
| `rng.js` | `createRng(seed)`, `rand01(ctx)`, `randRange(ctx, min, max)`, `randInt(ctx, min, max)`, `pickWeighted(ctx, weights)` | context, numeric ranges, weight object | deterministic random values |
| `context.js` | `createGameContext(seed)`, `resetRun(ctx, difficulty)`, `applySettings(ctx, settings)` | seed, difficulty, settings | initializes or resets records |
| `input.js` | `installKeyMap(ctx)`, `setKeyMap(ctx, map)`, `validateKeyMap(map)`, `getState(ctx)`, `isDown(ctx, action)`, `consume(ctx, action)`, `setTestInput(ctx, action, down)` | key codes, actions | updates `ctx.input` |
| `player.js` | `updatePlayer(ctx, dt)`, `getPlayerState(ctx)`, `setFacing(ctx, angle)`, `startTongue(ctx)`, `clearTongue(ctx)` | context, dt | mutates player position, facing, tongue timers |
| `catching.js` | `updateCatching(ctx, dt)`, `tryCatch(ctx)`, `catchBug(ctx, bug)`, `segmentHitsCircle(seg, circle)`, `getCatchingState(ctx)` | context, dt | removes bug, triggers effects/scoring/audio |
| `bugs.js` | `updateBugs(ctx, dt)`, `spawnBug(ctx, type, pos)`, `killBug(ctx, bug, reason)`, `getBugState(ctx, id)`, `setBugEscapeTimer(ctx, id, seconds)` | context, dt, type, pos | mutates bug records |
| `spawn.js` | `updateSpawn(ctx, dt)`, `getSpawnState(ctx)`, `forceSpawn(ctx, type)`, `setSpawnInterval(ctx, seconds)` | context, dt | appends bugs, updates spawn timers |
| `lives.js` | `updateLives(ctx, dt)`, `loseLife(ctx, reason)`, `setLives(ctx, n)`, `getLivesState(ctx)` | context, dt, reason | mutates lives, grace, mode, hit flash |
| `scoring.js` | `updateScoring(ctx, dt)`, `addCatch(ctx, bug)`, `resetCombo(ctx)`, `getScoringState(ctx)`, `rankForScore(score)` | context, dt, bug | mutates score, combo, multiplier, rank |
| `highscores.js` | `loadHighScores()`, `saveHighScore(ctx)`, `getTop(ctx, n)`, `isHighScore(ctx, score)`, `clearHighScores()` | context | reads/writes localStorage, updates `ctx.highScores` |
| `effects.js` | `updateEffects(ctx, dt)`, `spawnParticles(ctx, pos, color, count, speedMin, speedMax, sizeMin, sizeMax, life)`, `triggerHitFlash(ctx, reason, alpha, duration)`, `getEffectsState(ctx)`, `clearEffects(ctx)` | context, params | mutates particles and hit flash |
| `audio.js` | `playSfx(name)`, `playMusic()`, `stopMusic()`, `setMuted(ctx, muted)`, `getAudioState(ctx)` | sound name | Web Audio playback |
| `render.js` | `setCanvas(canvas)`, `draw(ctx)` | context | draws canvas only |
| `ui/hud.js` | `updateHud(ctx)`, `setHudVisible(ctx, visible)` | context | updates DOM HUD elements |
| `ui/screens.js` | `setMode(ctx, mode)`, `getMode(ctx)`, `renderScreens(ctx)`, `bindUiControls(ctx)` | mode, context | updates DOM screen visibility |
| `debug.js` | `attachDebug(ctx)`, `getSystemState(ctx, systemName)` | context | exposes debug functions |

# 3. VISUAL SPEC

One-screen top-down pond game drawn in flat vector style: bright saturated solid colours, crisp black outlines, no gradients, no textures, no realistic lighting. The pond is a dark blue play field with flat teal lily pads and orange cattail borders. The player is a round yellow-green frog with wide flat eyes and a silly long tongue. Bugs are clear silhouette shapes: oval fly, thin mosquito, long-winged dragonfly, round glowing firefly. UI is hand-lettered, irregular, chunky, and high contrast. Everything reads as a comic pond.

Lighting and atmosphere: flat, no shadows except simple offset outlines. No day/night cycle. Mood is silly arcade pond.

Space: fixed 960 x 640 pond. The safe play area is inset 28 px from the screen edge. The outer edge is decorated with cattails and water lines to signal bounds. Lily pads are decoration only and have no collision. Bug spawn zones are invisible inset rectangles. Escaping bugs cross the visible pond edge and trigger life loss.

| Element | Shape recipe | Colour | Outline | Animation | Rule implied |
| --- | --- | --- | --- | --- | --- |
| Background water | Solid rectangle with flat ripple lines | `#0b3954` | none | slow horizontal ripple lines | fixed top-down pond |
| Safe bounds | Invisible rectangle | none | none | none | player clamp, bug escape line |
| Pond edge decoration | Cattail rectangles, rounded reed caps | `#ff70a6`, `#ffd60a`, `#2a9d8f` | `#0b1b2a` 2 px | none | visual boundary |
| Lily pads | Flat circles with wedge cut | `#2a9d8f` | `#0b1b2a` 2 px | none | decoration only |
| Player frog | Body circle, eye circles, mouth line | body `#a7c957`, eyes `#f8f9fa`, pupils `#0b1b2a` | `#0b1b2a` 2 px | idle squash, blink, tongue | player identity |
| Tongue | Thick rounded line | `#ff70a6` | `#0b1b2a` 2 px | extend/retract | catch hitbox |
| Housefly | Oval body, two wing ellipses | `#5c7cfa`, wings `#a3bffa` | `#0b1b2a` 1.5 px | wing flicker | common target |
| Mosquito | Thin body, long proboscis, thin wings | `#ff70a6` | `#0b1b2a` 1.5 px | jitter bob | fast target |
| Dragonfly | Long body, four wing quads | `#ff9f1c` | `#0b1b2a` 1.5 px | dash stretch | high-speed target |
| Firefly | Round body, glow dot | `#ffd60a` | `#0b1b2a` 1.5 px | pulse glow | rare high-point target |
| Particles | Small circles/squares | bug colour | none | fade | catch juice |
| Hit flash | Full-screen flat rectangle | `#ff70a6` | none | alpha decay | life loss |
| HUD | Chunky panels, hearts, score, combo | text `#f8f9fa`, panels `#102a43` | `#0b1b2a` 2 px | heart pulse on loss | health, score, combo |
| Screens | Full-screen overlays, hand-lettered buttons | background `#102a43`, text `#f8f9fa`, highlights `#ffd60a` | `#0b1b2a` 2 px | button tilt | title, pause, game over, high scores |

# 4. GAMEPLAY SPEC

The player controls a frog on one top-down pond screen. Bugs appear and wander, avoiding the frog. The frog moves freely and presses Catch to shoot a tongue in its facing direction. A tongue hit removes a bug and triggers particles and score. Each bug has an escape timer; when it expires the bug dashes to the pond edge. If the bug crosses the edge, the player loses a life and combo resets. The run continues until lives reach 0. The game has no win condition and no forced end.

## Records and rosters

| Record | Fields | Roster / instances | Tier |
| --- | --- | --- | --- |
| Player | `pos`, `vel`, `facing`, `radius`, `maxSpeed`, `tongue`, `hitFlash`, `alive` | 1 | Tier 1 |
| Bug | `id`, `type`, `pos`, `vel`, `heading`, `radius`, `points`, `speed`, `baseSpeed`, `escapeTimer`, `baseEscapeTimer`, `avoidRadius`, `state`, `wanderTimer`, `jitterPhase`, `startleTimer`, `hitFlash`, `alive` | dynamic list | Tier 1 |
| Spawn | `timer`, `nextId`, `interval`, `maxActive`, `weights` | 1 | Tier 1 |
| Lives | `value`, `max`, `grace` | 1 | Tier 1 |
| Scoring | `score`, `combo`, `comboTimer`, `maxCombo`, `multiplier`, `rank` | 1 | Tier 2 |
| Effects | `particles[]`, `hitFlash` | dynamic list | Tier 1 |
| HighScore | `score`, `time`, `difficulty`, `rank`, `date` | top 10 | Tier 2 |
| Settings | `difficulty`, `reducedMotion`, `keyMap` | 1 | Tier 1 data, Tier 3 UI |

Bug roster:

| Type | Radius | Points | Base escape timer | Base speed | Avoid radius | Behaviour | Spawn weight source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Housefly | 9 px | 10 | 12.0 s | 55 px/s | 90 px | slow wander, turns every 0.8-1.6 s | weight table |
| Mosquito | 8 px | 15 | 9.0 s | 85 px/s | 110 px | fast erratic, perpendicular jitter amplitude 0.25 speed | weight table |
| Dragonfly | 12 px | 30 | 7.0 s | 130 px/s | 140 px | low turn rate 0.5 rad/s, straight dashes | weight table |
| Firefly | 7 px | 50 | 14.0 s | 40 px/s | 70 px | slow zigzag, sine amplitude 25 px/s, high value | weight table |

## 4.1 Input [Tier 1]

| Rule | Number |
| --- | --- |
| Logical actions | `moveUp`, `moveDown`, `moveLeft`, `moveRight`, `catch`, `pause`, `restart`, `uiSelect`, `uiUp`, `uiDown`, `uiLeft`, `uiRight` |
| Default movement keys | `W/A/S/D` and arrow keys |
| Default catch key | `Space` or `J` |
| Default pause key | `Escape` or `P` |
| Default restart key | `R` |
| Default UI select key | `Enter` or `Space` |
| Edge detection | `consume(action)` returns true once per press |
| Remapping | `settings.keyMap` maps action to key code list |
| Conflict rule | If a key is assigned to two actions, last valid assignment wins and UI shows conflict |
| Persistence | Key map stored in `localStorage` key `frog-snack-keymap-v1` |

## 4.2 Player movement [Tier 1]

| Rule | Number |
| --- | --- |
| Start position | `{ x: 480, y: 320 }` |
| Radius | 22 px |
| Easy max speed | 165 px/s |
| Normal max speed | 180 px/s |
| Hard max speed | 200 px/s |
| Movement input vector | `x = down(Right)-down(Left)`, `y = down(Down)-down(Up)` |
| Input vector normalization | If length > 1, normalize to length 1 |
| Velocity | `vel.x = input.x * maxSpeed`, `vel.y = input.y * maxSpeed` |
| Facing update | If input length > 0, `facing = atan2(input.y, input.x)`; else unchanged |
| Position update | `pos += vel * dt` |
| Clamp | `pos.x` in `[safe.left + radius, safe.right - radius]`, `pos.y` in `[safe.top + radius, safe.bottom - radius]` |
| Reduced motion effect | No cosmetic body squash; movement unchanged |

## 4.3 Catching [Tier 1]

| Rule | Number |
| --- | --- |
| Catch activation | `consume("catch")` and `player.tongue.cooldown <= 0` |
| Tongue start point | `player.pos + facing * 14` |
| Tongue end point | `player.pos + facing * length` |
| Easy tongue length | 170 px |
| Normal tongue length | 150 px |
| Hard tongue length | 140 px |
| Tongue active duration | 0.12 s |
| Tongue cooldown | 0.30 s |
| Collision | Segment-circle test with collision radius `bug.radius + 8` |
| Multiple hits | Select bug with largest projection along tongue direction, closest to tongue tip |
| Catch result | Bug `alive = false`, `state = "caught"`, removed from active list |
| Catch effects | 12 bug-coloured particles, bug white flash 0.10 s, catch sound |
| Miss result | Tongue retracts after duration, miss sound |
| Catch during escaping | Allowed; no life loss if caught before boundary crossing |
| Catch during startled | Allowed |

## 4.4 Bug movement and escape [Tier 1]

| State | Rule | Numbers |
| --- | --- | --- |
| `wander` | Move at type speed. Change heading every `wanderTimer` between 0.8 and 1.6 s. | Type speed scaled by difficulty and time |
| `avoid` | If distance to player < `avoidRadius`, heading points away from player and speed multiplier 0.85. | Avoid radius scaled by difficulty |
| `escaping` | When `escapeTimer <= 0`, choose nearest safe edge and accelerate toward it at speed multiplier 1.6. Ignore player avoidance. | Escape speed = scaled speed * 1.6 |
| `startled` | During life-loss grace, move toward screen centre at speed multiplier 1.1. Escape timer paused. No life loss. | Grace 1.2 s |
| `caught` | Removed; no further update. | N/A |
| Escape life loss | If bug center crosses safe bounds by 12 px, call `loseLife("escaped")`. | margin 12 px |
| Mosquito jitter | Add perpendicular velocity `sin(time*8)*speed*0.25`. | amplitude 25% speed |
| Firefly zigzag | Add perpendicular velocity `sin(time*3)*speed*0.6`. | amplitude 60% speed |
| Dragonfly dash | Low turn rate and straight heading. | turn rate 0.5 rad/s |

## 4.5 Spawning and difficulty [Tier 1]

| Rule | Number |
| --- | --- |
| First spawn | After 1.0 s from run start |
| Spawn location | Random point in safe bounds inset 90 px |
| Player distance rule | Must be at least 180 px from player; after 10 failed attempts, spawn opposite player from centre |
| Active cap | `min(difficulty.maxCap, difficulty.maxBase + floor(time / 25))` |
| Spawn interval | `max(difficulty.spawnMin, difficulty.spawnBase - time * 0.01)` |
| Time stage | `stage = floor(time / 30)` |
| Bug speed multiplier | `min(1.5, 1 + stage * 0.04) * difficulty.speedMult` |
| Escape timer multiplier | `max(0.60, 1 - stage * 0.03) * difficulty.escapeTimerMult` |
| Avoid radius multiplier | `difficulty.avoidRadiusMult` |
| Weight table 0-29 s | fly 70, mosquito 25, dragonfly 5, firefly 0 |
| Weight table 30-59 s | fly 55, mosquito 30, dragonfly 10, firefly 5 |
| Weight table 60-119 s | fly 40, mosquito 30, dragonfly 20, firefly 10 |
| Weight table 120+ s | fly 25, mosquito 25, dragonfly 30, firefly 20 |

Difficulty table:

| Option | Lives | Player speed | Tongue length | Spawn base | Spawn min | Active base | Active cap | Bug speed mult | Escape timer mult | Avoid radius mult |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Easy | 5 | 165 px/s | 170 px | 4.0 s | 1.8 s | 2 | 6 | 0.85 | 1.30 | 0.70 |
| Normal | 3 | 180 px/s | 150 px | 3.2 s | 1.1 s | 3 | 9 | 1.00 | 1.00 | 1.00 |
| Hard | 2 | 200 px/s | 140 px | 2.2 s | 0.85 s | 4 | 12 | 1.15 | 0.80 | 1.30 |

## 4.6 Lives and failure [Tier 1]

| Rule | Number |
| --- | --- |
| Easy lives | 5 |
| Normal lives | 3 |
| Hard lives | 2 |
| Life loss trigger | Bug escapes boundary |
| Life loss effect | `lives.value -= 1`, `scoring.combo = 0`, hit flash, life-lost sound, remove escaped bug |
| Grace duration | 1.2 s |
| Grace spawn rule | Spawn timer does not advance |
| Grace bug rule | All live bugs enter `startled` |
| Grace life rule | No additional life loss during grace |
| Game over | When `lives.value <= 0`, set `mode = "gameover"`, `run.gameOverReason = "lives"` |
| Game over screen | Shows final score, time survived, rank, high score status, restart/title/high scores buttons |
| Restart | Resets run records, sets mode `playing`, keeps settings and high scores |

## 4.7 Scoring and combo [Tier 2]

| Rule | Number |
| --- | --- |
| Base points | Bug roster values: fly 10, mosquito 15, dragonfly 30, firefly 50 |
| Combo increment | On catch, `combo += 1` |
| Combo cap | 10 |
| Multiplier | `min(10, combo)` |
| Score added | `bug.points * multiplier` |
| Combo timer | 3.0 s after each catch |
| Combo timeout | If timer reaches 0, `combo = 0`, `multiplier = 1` |
| Escape timeout | If bug escapes, `combo = 0`, `multiplier = 1` |
| Game over reset | Run reset clears score and combo |
| HUD combo | Shows `x{combo}` when combo > 0 |
| Max combo | Stored for debug/game over |

## 4.8 High scores and ranks [Tier 2]

| Rule | Number |
| --- | --- |
| High score storage | `localStorage["frog-snack-highscores-v1"]` |
| Max stored | 10 |
| Sort | Score descending, then time descending, then date descending |
| Insert trigger | On game over, if score > 0 and in top 10 |
| Display | High scores screen shows rank, score, time, difficulty, date |
| New high score flag | Game over shows `NEW HIGH SCORE` if inserted |
| Rank thresholds | 0-249 Tadpole; 250-749 Froglet; 750-1499 Toad; 1500-2499 Bullfrog; 2500-3999 Pond Master; 4000+ Legendary Frog |
| Rank display | Game over and high scores |

## 4.9 Effects [Tier 1]

| Effect | Rule | Numbers |
| --- | --- | --- |
| Catch particles | Spawn at bug position | count 12, speed 80-160 px/s, size 3-6 px, lifetime 0.45 s |
| Bug hit flash | Bug draws white overlay | duration 0.10 s |
| Life lost hit flash | Full-screen flat overlay | colour `#ff70a6`, alpha 0.45, duration 0.18 s |
| Reduced motion particles | Disabled | count 0 |
| Reduced motion hit flash | Reduced | alpha 0.15, duration 0.08 s |
| Particle update | Position += velocity * dt, alpha fades linearly | no gravity |
| Particle removal | When `life <= 0` | immediate |

## 4.10 Accessibility [Tier 1 defaults, Tier 3 UI]

| Requirement | Rule |
| --- | --- |
| Colour-blind safe palette | Palette avoids red/green-only distinctions; bug types have distinct shapes and labels |
| Reduced motion | Default from `prefers-reduced-motion: reduce`; disables particles, screen flash intensity, cosmetic wobble |
| Remappable keys | Key map stored in settings; UI in title/pause in Tier 3 |
| Difficulty options | Easy/Normal/Hard constants; selectable in title/pause in Tier 3 |
| UI readability | Minimum UI text size 18 px, high contrast, no colour-only meaning |
| Input fallback | Default keyboard works without settings UI |

## Progression and difficulty

| Time | Target feel | Numbers |
| --- | --- | --- |
| 0-30 s | Learning. Mostly flies, one or two mosquitoes. | active cap 3, interval starts 3.2 s, escape timers full |
| 30-60 s | Introduction of rare Firefly and more Dragonfly. | weights change, active cap increases every 25 s |
| 60-120 s | Pressure. Faster bugs, shorter escape timers. | stage scaling active, max active grows |
| 120-300 s | Typical failure band. High mix, short timers. | normal max active near cap, interval near minimum |
| 300+ s | Endless survival. Bug speed multiplier caps at 1.5, escape timer multiplier caps at 0.60. | no hard cap |

## Feel

- Movement should feel direct: input changes velocity instantly, no drift.
- Tongue should feel snappy: 0.12 s extension, 0.30 s cooldown.
- Catching should feel silly and exaggerated: long tongue, bug squash, bright particles.
- Escape should feel readable: bug stretches and dashes toward edge.
- Life loss should be loud but not unfair: one life per escaped bug, 1.2 s grace.
- Scoring should feel rewarding: combo counter climbs, sounds rise, rank appears at run end.

# 5. CHARACTERS

## Player: Frogbert

Silhouette: top-down round body, two eye bumps near top, wide mouth line, stubby leg nubs. Facing is indicated by eye direction and mouth line.

| State | Visual states | Animation name | Motion rules |
| --- | --- | --- | --- |
| Idle | Eyes open, mouth closed | `idle` | body scale `1 + sin(t*2π*1.1)*0.02`, blink every 4-7 s for 0.12 s |
| Move | Facing follows velocity | `move` | body squash along velocity amplitude 0.05, no legs |
| Tongue | Mouth opens, tongue extends | `tongue` | line extends from mouth to tip over 0.04 s, holds 0.08 s, retracts 0.04 s |
| Hit flash | White overlay | `hitFlash` | only on life lost screen flash, not player body unless debug |
| Game over | Eyes closed, mouth frown | `gameover` | static |

## Housefly

Silhouette: oval body, two wing ellipses, short legs.

| State | Animation | Motion rules |
| --- | --- | --- |
| `wander` | `flyWingFlicker` | wings alpha flicker 8 Hz, body bob 2 px at 2 Hz |
| `escaping` | `flyStretch` | body stretch 1.25 along velocity, wing flicker 14 Hz |
| `startled` | `flyWobble` | rotate ±3° at 6 Hz while moving centre |
| `caught` | `bugPop` | scale 1.0 to 0.0 in 0.10 s |

## Mosquito

Silhouette: thin body, long proboscis, narrow wings.

| State | Animation | Motion rules |
| --- | --- | --- |
| `wander` | `mosquitoJitter` | body jitter amplitude 3 px at 12 Hz |
| `escaping` | `mosquitoStretch` | stretch 1.35, proboscis forward |
| `startled` | `mosquitoWobble` | small circular jitter |
| `caught` | `bugPop` | scale down |

## Dragonfly

Silhouette: long segmented body, four wings.

| State | Animation | Motion rules |
| --- | --- | --- |
| `wander` | `dragonflyHover` | wings flicker 10 Hz, body stable |
| `escaping` | `dragonflyDash` | stretch 1.4, trailing motion streak |
| `startled` | `dragonflyTurn` | rotate toward centre smoothly |
| `caught` | `bugPop` | scale down |

## Firefly

Silhouette: round body, glowing rear dot.

| State | Animation | Motion rules |
| --- | --- | --- |
| `wander` | `fireflyPulse` | glow radius 6-10 px at 1.5 Hz, zigzag motion |
| `escaping` | `fireflyFlee` | glow trails, stretch 1.2 |
| `startled` | `fireflyDim` | glow pulses dim, move centre |
| `caught` | `bugPop` | glow burst then scale down |

# 6. AUDIO

All audio is synthesized with Web Audio. No external audio files.

| Sound name | Recipe | When it plays |
| --- | --- | --- |
| `music_theme` | 120 BPM chiptune loop: square lead A minor, triangle bass, noise hats, 16-step pattern | While mode is `playing`; stop on pause/game over |
| `ui_hover` | Square oscillator 440 Hz, 0.02 s, volume 0.08 | UI focus change |
| `ui_select` | Square oscillator 660 Hz to 880 Hz slide, 0.08 s | Button or menu selection |
| `game_start` | Square arpeggio C5-E5-G5-C6, 0.08 s each | Enter `playing` from title/restart |
| `pause` | Square 392 Hz to 330 Hz, 0.12 s | Enter `paused` |
| `resume` | Square 330 Hz to 392 Hz, 0.12 s | Leave `paused` |
| `tongue` | Sawtooth 900 Hz to 400 Hz slide, 0.08 s | Catch input starts tongue |
| `tongue_miss` | Square 220 Hz, 0.04 s, plus short noise | Tongue finishes without catch |
| `bug_caught` | Triangle 700 Hz to 1100 Hz, 0.08 s; noise burst 0.02 s; square blip 1320 Hz | Bug caught |
| `combo_up` | Square 880 Hz, 1100 Hz, 1320 Hz quick notes, 0.05 s each | Combo multiplier increases |
| `bug_escape` | Sawtooth 500 Hz to 200 Hz, 0.25 s | Bug crosses escape boundary |
| `life_lost` | Square 180 Hz, 0.25 s, plus low noise | Life lost |
| `game_over` | Square arpeggio A4-G4-F4-E4, 0.15 s each | Mode becomes game over |
| `new_highscore` | Square arpeggio C5-E5-G5-C6, 0.08 s each | New high score inserted |
| `spawn` | Sine 760 Hz, 0.05 s, volume 0.05 | Bug appears |
| `rank_reveal` | Square arpeggio based on rank: higher ranks higher notes | Game over rank display |

# 7. UX

UI is HTML/CSS only. The canvas renders gameplay entities. DOM elements are hidden or shown by `body[data-mode]`.

## Screens state machine

| Current mode | Action | Next mode | Input / control |
| --- | --- | --- | --- |
| `title` | Start | `playing` | Enter, Space, Start button |
| `title` | High scores | `highscores` | H key, High Scores button |
| `title` | Difficulty change | stays `title` | difficulty radio buttons |
| `title` | Accessibility toggle | stays `title` | reduced motion toggle, key remap button |
| `highscores` | Back | `title` | Esc, Back button |
| `playing` | Pause | `paused` | Esc, P |
| `paused` | Resume | `playing` | Esc, P, Resume button |
| `paused` | Restart | `playing` | R, Restart button |
| `paused` | Quit | `title` | Q, Quit button |
| `paused` | Difficulty change | stays `paused` | difficulty controls |
| `playing` | Game over | `gameover` | lives reach 0 |
| `gameover` | Play again | `playing` | Enter, R, Play Again button |
| `gameover` | High scores | `highscores` | H, High Scores button |
| `gameover` | Title | `title` | Esc, Title button |

## HUD table

| Element | Record field | When visible | Display rule |
| --- | --- | --- | --- |
| `#hud-health` | `ctx.lives.value`, `ctx.lives.max` | `playing`, `paused` | Heart icons; numeric fallback `3/5`; colour-blind safe labels |
| `#hud-score` | `ctx.scoring.score` | `playing`, `paused`, `gameover` | Integer with thousands separators |
| `#hud-combo` | `ctx.scoring.combo`, `ctx.scoring.multiplier` | `playing`, `paused` | Hidden when `combo == 0`; shows `COMBO x{combo}` |
| `#gameover-score` | `ctx.scoring.score` | `gameover` | Final score |
| `#gameover-time` | `ctx.run.time` | `gameover` | Minutes:seconds |
| `#gameover-rank` | `ctx.scoring.rank` | `gameover` | Rank label |
| `#gameover-highscore` | `ctx.highScores` insertion result | `gameover` | Shows `NEW HIGH SCORE` only if inserted |
| `#highscore-list` | `ctx.highScores` | `highscores` | Top 10 table |

# 8. DEBUG API

`window.frogDebug` exposes direct state and test hooks.

| Function | Purpose | Returns |
| --- | --- | --- |
| `frogDebug.input.press(action)` | Simulate key press | `true` if valid |
| `frogDebug.input.release(action)` | Simulate key release | `true` if valid |
| `frogDebug.input.move(x, y)` | Simulate normalized movement input | `true` |
| `frogDebug.input.getState()` | Read input action state | input object |
| `frogDebug.player.getState()` | Read player state | player record |
| `frogDebug.player.setPos(x, y)` | Set player position | `true` |
| `frogDebug.player.setFacing(angle)` | Set facing | `true` |
| `frogDebug.catching.getState()` | Read tongue state | tongue record |
| `frogDebug.catching.forceCatch(bugId)` | Force catch specific bug | `true` if caught |
| `frogDebug.catching.setCooldown(seconds)` | Set tongue cooldown | `true` |
| `frogDebug.bugs.getState()` | Read all bugs | bug array |
| `frogDebug.bugs.spawn(type, x, y)` | Spawn bug at position | bug id |
| `frogDebug.bugs.setEscapeTimer(bugId, seconds)` | Set escape timer | `true` |
| `frogDebug.spawn.getState()` | Read spawn state | spawn record |
| `frogDebug.spawn.setInterval(seconds)` | Set spawn interval | `true` |
| `frogDebug.spawn.forceSpawn(type)` | Force spawn | bug id |
| `frogDebug.lives.getState()` | Read lives state | lives record |
| `frogDebug.lives.set(n)` | Set lives | `true` |
| `frogDebug.lives.lose(reason)` | Trigger life loss | `true` |
| `frogDebug.scoring.getState()` | Read scoring state | scoring record |
| `frogDebug.scoring.addCatch(bug)` | Trigger scoring catch | score delta |
| `frogDebug.scoring.rank(score)` | Get rank label | string |
| `frogDebug.effects.getState()` | Read particles and hit flash | effects record |
| `frogDebug.effects.clear()` | Clear effects | `true` |
| `frogDebug.ui.setMode(mode)` | Set UI mode | `true` |
| `frogDebug.ui.getMode()` | Read mode | string |
| `frogDebug.system.getState(system)` | Generic state getter for `"player"`, `"catching"`, `"bugs"`, `"spawn"`, `"lives"`, `"scoring"`, `"effects"` | system record |

# 9. TESTS

| Tier | Test | Method | Pass criteria |
| --- | --- | --- | --- |
| Tier 1 | Fixed step stability | Run 600 simulated frames | `run.time` equals 10.0 s within 0.001 |
| Tier 1 | Player bounds | Hold movement into each wall for 5 s | Player center never outside safe bounds |
| Tier 1 | Catch activation | Press catch with cooldown ready | Tongue active, duration 0.12, cooldown 0.30 |
| Tier 1 | Catch collision | Place bug at tongue tip, force catch | Bug removed, particles spawned, catch sound called |
| Tier 1 | Escape life loss | Set bug escape timer 0, move bug past boundary | `lives.value` decreases by 1, combo reset, hit flash triggered |
| Tier 1 | Life grace | Trigger life loss with multiple bugs | No further life loss for 1.2 s, spawn timer frozen |
| Tier 1 | Game over | Set lives 0 | Mode becomes `gameover`, simulation stops |
| Tier 1 | Restart | From game over, restart | Run records reset, mode `playing`, settings preserved |
| Tier 1 | HUD update | Change lives/score/combo | DOM values match records |
| Tier 1 | No extra mechanics | Static scan for pickup/trap/enemy systems | No pickup, trap, weapon, shop, upgrade systems present |
| Tier 2 | Combo increment | Trigger 5 catches | `combo` reaches 5, multiplier 5 |
| Tier 2 | Combo cap | Trigger 12 catches | Multiplier caps at 10 |
| Tier 2 | Combo timeout | Wait 3.1 s after catch | Combo resets to 0 |
| Tier 2 | Score formula | Catch dragonfly with combo 3 | Score increases by 90 |
| Tier 2 | High score insert | Game over with score 1000 | LocalStorage contains score, rank, time, difficulty |
| Tier 2 | Rank thresholds | Call `rankForScore` at 249/250/750/1500/2500/4000 | Returns correct labels |
| Tier 3 | Difficulty constants | Set easy/normal/hard and reset | Lives, speed, spawn, timer constants match table |
| Tier 3 | Reduced motion | Enable reduced motion and catch bug | Particle count 0, hit flash reduced |
| Tier 3 | Key remap | Remap catch to `K` and press `K` | Catch triggers |
| Tier 3 | Pause stops simulation | Enter paused, advance time | `run.time` unchanged |
| Tier 3 | High scores screen | Set mode highscores | Top scores rendered |

# 10. BUILD ORDER

1. Create HTML/CSS shell, canvas, screen overlays, HUD elements.
2. Implement constants, RNG, global context, fixed loop, mode state machine.
3. Implement default input and key map.
4. Implement player movement, facing, bounds.
5. Implement bug records and basic render placeholders.
6. Implement bug wander, avoidance, escape, boundary life loss.
7. Implement spawning, active cap, weight table, difficulty constants.
8. Implement tongue catching and collision.
9. Implement lives, grace, game over, restart.
10. Implement flat vector rendering for player, bugs, tongue, particles, hit flash.
11. Implement HUD DOM updates.
12. Implement title, pause, game over screens.
13. Implement chiptune music and retro bleeps.
14. Add Tier 1 debug hooks and run Tier 1 tests.
15. Implement scoring, combo, multiplier.
16. Implement high scores storage, high scores screen, ranks.
17. Add Tier 2 debug hooks and run Tier 2 tests.
18. Implement difficulty selection UI.
19. Implement reduced motion toggle and key remap UI.
20. Add Tier 3 accessibility polish and run Tier 3 tests.

# 11. DEFINITION OF DONE

## Tier 1: core catching game

High level: A player can start the game, move a frog, catch bugs with a tongue, lose lives when bugs escape, see a playable one-screen endless survival game with art, audio, HUD, and game over.

- [ ] Fixed 60 Hz loop and deterministic RNG exist.
- [ ] Default keyboard movement and catch input work.
- [ ] Player is constrained to safe bounds and faces last movement direction.
- [ ] Catch input creates a tongue segment with correct length, duration, cooldown.
- [ ] Tongue catches bugs using segment-circle collision.
- [ ] Four bug types exist with the exact roster numbers.
- [ ] Bugs wander, avoid player, escape after timer, and lose a life at boundary.
- [ ] Spawn system uses interval, active cap, and time-weighted type table.
- [ ] Life loss triggers hit flash, particles, sound, and 1.2 s grace.
- [ ] Game over occurs at 0 lives and restart works.
- [ ] Title, pause, and game over screens work.
- [ ] HUD shows health, score placeholder, combo placeholder.
- [ ] Flat vector palette and hand-lettered UI are visible.
- [ ] Chiptune music and retro bleeps are audible.
- [ ] Reduced motion detection and key map data structure exist.
- [ ] Tier 1 tests pass.

## Tier 2: scoring and high scores

High level: Catches award points, combos increase multiplier, ranks are assigned, and high scores persist and display.

- [ ] Catch scoring uses bug base points and combo multiplier.
- [ ] Combo timer is 3.0 s and resets on timeout or escape.
- [ ] Combo counter and multiplier are capped at 10.
- [ ] HUD combo element appears only when combo > 0.
- [ ] Rank thresholds return correct labels.
- [ ] High scores save to localStorage and sort correctly.
- [ ] Game over shows final score, time, rank, and new-high-score flag.
- [ ] High scores screen displays top 10.
- [ ] Tier 2 tests pass.

## Tier 3: accessibility and difficulty UI

High level: Player can choose difficulty, remap keys, toggle reduced motion, and settings persist.

- [ ] Easy/Normal/Hard selection UI works and changes run constants correctly.
- [ ] Reduced motion toggle disables particles and reduces hit flash.
- [ ] Key remap UI validates and persists key map.
- [ ] Settings persist across reloads.
- [ ] Pause and title expose accessibility controls without adding new screens.
- [ ] Tier 3 tests pass.

# A. SANITY

| Check | Result | Notes |
| --- | --- | --- |
| Requested core mechanic only | Pass | Core is catching bugs with tongue. No combat, tools, or other core mechanics added. |
| Requested supporting mechanic only | Pass | Scoring includes points, combo, high scores, ranks. No other scoring systems. |
| Extra mechanics none | Pass | No traps, pickups, power-ups, upgrades, shops, weapons, or secondary modes. |
| Exact screens | Pass | Only title, pause, game over, high scores. Settings embedded in existing screens. |
| Exact HUD parts | Pass | Only health, score, combo counter. Game over extras are result data, not HUD. |
| Exact effects | Pass | Only particles and hit flash. |
| Accessibility requirements | Pass | Colour-blind palette, reduced motion, remappable keys, difficulty options specified. |
| Endless vs game over | Pass | No win condition; failure ends run at 0 lives; endless by design. |
| One screen vs few minutes | Pass | One fixed screen; difficulty targets 3-8 minute typical runs but no hard cap. |
| Tier order | Pass | Tier 1 core catching; Tier 2 scoring/high scores; Tier 3 accessibility/difficulty UI. |
| Tier 1 includes look/sound | Pass | Tier 1 includes flat vector art, palette, audio, particles, hit flash, HUD. |
| All systems have numbers | Pass | Movement, tongue, bugs, spawn, lives, scoring, effects, ranks have numeric values. |
| Global context contains records | Pass | Section 2.2 includes all fields used by systems. |
| Debug API reaches each system | Pass | Section 8 includes state and test functions for each system. |
| Tests validate tiers | Pass | Section 9 maps tests to Tier 1, 2, 3. |