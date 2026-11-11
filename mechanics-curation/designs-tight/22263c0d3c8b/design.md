# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Platformer where you play as a frog | §4.1 Platforming, §5 Characters |
| 2D | §1.1 Units, §2.3 Module specifics, §3 Visual Spec |
| Side-on camera | §1.1, §4.1 Platforming, §3 Visual Spec |
| Real-time time model | §1.2, §4.1 Platforming, §4.3 Hazards, §7 UX |
| Free movement model | §4.1 Platforming, §4.2 Physics |
| Session shape: sequence of levels | §4.6 Progression, §4.3 Level roster, §7 UX state machine |
| Failure: lose a life | §4.3 Hazards, §4.1 Platforming, §7 UX Game Over |
| Silly tone | §3 Visual Spec, §5 Characters, §6 Audio, §7 UX copy |
| Size: a handful of levels, under 30 minutes | §4.3 Level roster, §4.6 Progression |
| Win/lose: reach the exit | §4.1 Platforming, §4.3 Level roster, §7 UX Win/Game Over |
| Core mechanic: platforming | §4.1 Platforming, Tier 1 |
| Core mechanic: physics | §4.2 Physics, Tier 1 |
| Core mechanic: hazards | §4.3 Hazards, Tier 1 |
| Supporting mechanic: collectibles | §4.4 Collectibles, Tier 2 |
| Extra mechanic: scoring | §4.5 Scoring, Tier 3 |
| Art style: pixel art, low-resolution sprites, visible square pixels, limited palette | §3 Visual Spec, §5 Characters |
| Palette: saturated | §3 Visual Spec |
| Typography: pixel font, blocky bitmap letters | §3 Visual Spec, §7 UX |
| Music: chiptune, retro console bleeps | §6 Audio |
| Sound effects style: retro bleeps, synthesized chip sounds | §6 Audio |
| Screens: title, pause, settings, game over, win, high scores | §7 UX |
| HUD: score | §7 UX HUD |
| Effects: particles, hit flash | §3 Visual Spec, §4.3 Hazards, §4.4 Collectibles |
| Accessibility: colour-blind safe palette | §3 Visual Spec, §1.2, §7 UX |
| Accessibility: reduced motion | §1.2, §3 Visual Spec, §5 Characters, §7 UX |
| Accessibility: remappable keys | §1.2, §2.3, §7 UX |
| Accessibility: difficulty options | §4.6 Progression and Difficulty, §7 UX |

## 0.2 Decisions

| Decision | Final ruling | Why |
| --- | --- | --- |
| Player identity | “Flap”, a small, loud, overconfident frog with a tiny crown that keeps falling off. | Silly, immediate, readable in pixel art, avoids adding story systems. |
| Level count | Exactly 5 levels. | “Handful” becomes concrete; fits under 30 minutes. |
| Total playtime budget | Par times total 19:30; target real player time 18–27 minutes. | Keeps under 30 minutes while allowing exploration. |
| Lives | Easy: 9 lives. Normal: 3 lives. Hard: 1 life. | Required failure mode; difficulty options. |
| Life loss | Touching a hazard or falling out of bounds costs 1 life and restarts the current level at `level.spawn`. | Simple, fair, no extra checkpoint system. |
| Win condition | Reach the exit in Level 5. | Required win/lose. |
| Lose condition | Lives reach 0. Game Over screen appears. | Required failure. |
| Enemy content | “Enemy-like” dangers are fixed hazards only: Snap-Fly Trap, Electric Pond, Spike Lily. No enemy AI system. | Core mechanics list only hazards; no separate enemy system may be added. |
| Traps | Traps are the same hazard types, placed as level hazards. | Avoids adding a separate trap system. |
| Pickups | Golden Flies. One collectible type, set of 78 total across all levels. | Required collectibles as a set. |
| Physics objects | Wobbly Crate, Rolling Barrel, Bouncy Ball, Plank. | Provides physics puzzles without adding separate systems. |
| Physics interaction | Player can push, drop on, and stand on physics objects. No grab, no throw, no inventory. | Physics is core but must not become an extra interaction system. |
| Collectible scoring | Collectibles award points only when Tier 3 scoring is enabled. In Tier 2 they are collectible but unscored. | Keeps scoring as a later extra mechanic. |
| Scoring | Points for golden flies, level clear, collect-all, no-hit, and time bonus. High scores stored locally. | Required scoring and best scores. |
| HUD | Only one HUD element: Score. Lives are not shown during play; they are shown on Pause and Game Over. | The requested HUD list is exactly score. |
| Camera | Side-on, clamped to level bounds, follows player with a deadzone. No rotation, no zoom, no camera shake. | Required side-on camera; avoids adding screen-shake systems. |
| Fixed timestep | 60 Hz game step; physics uses 3 substeps per game step. | Deterministic, testable, real-time. |
| Collision | AABB for player, platforms, crates, barrels, planks; circle for balls; sensors for hazards, collectibles, exits. | Simple, deterministic, enough for platforming and physics. |
| Colour palette | Saturated but colour-blind safe Okabe/Ito-inspired palette. Always colour-blind safe by default. | Required art style plus accessibility. |
| Reduced motion | When enabled: particles disabled, hit flash reduced to one static white frame, UI transitions disabled, collectible/hazard idle animations disabled. | Required accessibility. |
| Remappable keys | All game and menu actions remappable. Defaults documented. | Required accessibility. |
| Difficulty options | Easy/Normal/Hard selectable before a run; changing difficulty restarts the run. | Required accessibility and failure tuning. |
| Screens | Exactly: Title, Settings, Playing, Pause, Game Over, Win, High Scores. No level-select screen. | Required screens; level sequence is automatic. |
| Audio | Synthesized chiptune music and bleeps only. No sample-based audio. | Required music and sound style. |
| Particles | Only particles are: collect burst, hazard hit burst, small landing dust. | Required effects; no unrelated particle systems. |
| Hit flash | Only hit flash is player-white flash and hazard red-orange flash. | Required hit flash. |
| High scores | Top 10 scores stored in `localStorage`, tagged with difficulty and date. | Required best scores. |
| Random source | No random source affects gameplay. `Math.random()` is allowed only for particle jitter and cosmetic timing. | Keeps runs deterministic and testable. |

## 0.3 Tiers

| Tier | Goal | Included segments | Done means |
| --- | --- | --- | --- |
| Tier 1 | Core playable frog platformer with platforming, physics, hazards, one full level, win/lose, required art/audio/effects/HUD. | Input, fixed-step loop, camera, player platforming, static platforms, physics objects, hazards, Level 1, exit, level completion, Game Over, Win, Title, Pause, Score HUD showing `0`, pixel art, chiptune audio, particles, hit flash. | A player can start from Title, play Level 1, lose lives, reach the exit, see Win, lose all lives and see Game Over, pause, and see all required Tier 1 visuals/audio/HUD. |
| Tier 2 | Full session and supporting collectibles. | Levels 2–5, Golden Fly collectibles, collected-set tracking, Pause life display, Settings screen, difficulty options, remappable keys, reduced motion, colour-blind safe palette enforcement. | A player can play all 5 levels, find 78 collectibles, change accessibility settings, and finish the full session. |
| Tier 3 | Scoring and best scores. | Score events, level bonuses, time bonus, no-hit bonus, collect-all bonus, High Scores screen, high-score storage, best score display on Win/Game Over. | A player can earn points, see final score, and high scores persist after restart. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Concept | Value |
| --- | ---: |
| Native game resolution | 640 × 360 pixels |
| Display scaling | Integer scale: 1×, 2×, 3×. Minimum visible scale 1×. |
| Tile size | 16 × 16 pixels |
| Coordinate system | x increases right, y increases down. Origin at top-left of level. |
| Time unit | seconds |
| Fixed timestep | 1/60 second |
| Physics substeps | 3 substeps per fixed timestep, dt = 1/180 second |
| Player sprite | 16 × 16 pixels |
| Player hitbox | 12 × 14 pixels, offset x +2, y +2 from sprite origin |
| Player max horizontal speed | 160 px/s |
| Player horizontal acceleration, grounded | 1600 px/s² |
| Player horizontal acceleration, airborne | 1200 px/s² |
| Ground friction | 2600 px/s² |
| Air friction | 400 px/s² |
| Jump initial velocity | -420 px/s |
| Gravity | 1200 px/s² |
| Terminal fall velocity | 420 px/s |
| Coyote time | 0.10 s |
| Jump buffer | 0.10 s |
| Variable jump cutoff | If jump is released while `vy < -180`, set `vy = -180` |
| Landing sound threshold | `vy > 300` |
| Camera deadzone | x: 80 px, y: 56 px |
| Camera follow lerp | 12 per second |
| Physics max body speed | 600 px/s |
| Mass unit | arbitrary; player mass = 1.0 |
| Angles | radians |
| Animation frame unit | seconds |

## 1.2 Important conventions

- All gameplay runs on a fixed 60 Hz update loop. Rendering may interpolate for display but gameplay state advances only in fixed steps.
- Physics collision resolution is deterministic. Level data is static and loaded exactly as authored.
- No randomness affects player position, physics outcomes, hazard behaviour, collectible placement, scoring, or level layout.
- `Math.random()` is allowed only for cosmetic particle jitter and cosmetic animation timing.
- Input actions are abstract: `left`, `right`, `jump`, `pause`, `confirm`, `back`, `menuUp`, `menuDown`, `menuLeft`, `menuRight`.
- Key mappings are stored in `settings.remap` and default to the documented map.
- The game supports keyboard input only. No mouse click is required to play, though mouse may activate UI buttons.
- The colour palette is always colour-blind safe. There is no “unsafe” palette option.
- Reduced motion is a setting. When enabled, particles are disabled, hit flash is a single static frame, UI transitions are disabled, and idle sprite animations are disabled.
- Difficulty is selected from Title or Settings before a run. Changing difficulty starts a new run.
- The only HUD element is Score. Remaining lives are shown only on Pause, Game Over, and Win screens.
- The game canvas renders gameplay. All menu screens are HTML/CSS overlays or HTML/CSS pages. No gameplay UI is drawn in the canvas.
- The pixel font is a blocky bitmap font rendered at integer pixel sizes. It is never anti-aliased.
- Sprites are drawn with `image-rendering: pixelated` and integer scaling.
- Local storage key: `frogPlatformer.highScores.v1`.
- A run is a sequence of levels starting at Level 1. There is no free level select.
- Pause freezes real-time timers and physics.
- If the player falls below `level.height + 32`, they lose a life.

# 2. CONTRACTS

## 2.1 Module layout

```text
/index.html
/css/style.css
/css/pixel-font.css
/js/main.js
/js/global.js
/js/input.js
/js/player.js
/js/physics.js
/js/level.js
/js/hazards.js
/js/collectibles.js
/js/scoring.js
/js/render.js
/js/audio.js
/js/ui.js
/js/storage.js
/js/debug.js
/levels/level1.js
/levels/level2.js
/levels/level3.js
/levels/level4.js
/levels/level5.js
/assets/pixel-font.png
/assets/sprites.js
```

## 2.2 Global context

```js
const G = {
  settings: {
    difficulty: "normal", // "easy" | "normal" | "hard"
    reducedMotion: false,
    colorBlindSafe: true,
    remap: {
      left: ["ArrowLeft", "KeyA"],
      right: ["ArrowRight", "KeyD"],
      jump: ["Space", "KeyZ", "KeyW", "ArrowUp"],
      pause: ["Escape", "KeyP"],
      confirm: ["Enter", "Space"],
      back: ["Escape"],
      menuUp: ["ArrowUp", "KeyW"],
      menuDown: ["ArrowDown", "KeyS"],
      menuLeft: ["ArrowLeft", "KeyA"],
      menuRight: ["ArrowRight", "KeyD"]
    }
  },

  input: {
    actions: {
      left: false,
      right: false,
      jump: false,
      pause: false,
      confirm: false,
      back: false,
      menuUp: false,
      menuDown: false,
      menuLeft: false,
      menuRight: false
    },
    pressed: {
      left: false,
      right: false,
      jump: false,
      pause: false,
      confirm: false,
      back: false,
      menuUp: false,
      menuDown: false,
      menuLeft: false,
      menuRight: false
    },
    buffers: {
      jump: 0
    }
  },

  run: {
    active: false,
    startedAt: 0,
    levelIndex: 0,
    completedLevels: 0,
    lives: 3,
    maxLives: 3,
    levelTime: 0,
    totalScore: 0,
    gameWon: false,
    gameOver: false
  },

  camera: {
    x: 0,
    y: 0,
    targetX: 0,
    targetY: 0,
    bounds: { x: 0, y: 0, width: 640, height: 360 }
  },

  player: {
    x: 0,
    y: 0,
    vx: 0,
    vy: 0,
    width: 12,
    height: 14,
    grounded: false,
    coyoteTimer: 0,
    jumpBufferTimer: 0,
    invulnTimer: 0,
    hitFlashTimer: 0,
    facing: 1, // 1 right, -1 left
    animState: "idle", // idle | run | jump | fall | hit
    animTime: 0,
    alive: true
  },

  level: {
    id: 1,
    name: "",
    width: 0,
    height: 0,
    spawn: { x: 0, y: 0 },
    exit: { x: 0, y: 0, width: 16, height: 24, active: true },
    platforms: [], // { x, y, width, height, friction, restitution }
    hazards: [], // { id, type, x, y, width, height, hitboxX, hitboxY, hitboxWidth, hitboxHeight, active }
    physicsObjects: [], // { id, type, x, y, width, height, radius, mass, friction, restitution }
    collectibles: [], // { id, x, y, width, height, collected, hiddenHint }
    parTime: 0
  },

  physics: {
    bodies: [], // unified runtime bodies generated from level.physicsObjects and level.platforms
    substep: 1 / 180
  },

  collectibles: {
    total: 0,
    collected: 0,
    setComplete: false
  },

  scoring: {
    current: 0,
    levelScore: 0,
    bonuses: {
      collectAll: 0,
      noHit: 0,
      time: 0
    },
    highScores: [],
    bestScore: 0,
    noHit: true
  },

  effects: {
    particles: [], // { x, y, vx, vy, life, maxLife, color, size }
    hitFlash: false,
    hitFlashTime: 0
  },

  ui: {
    screen: "title", // title | settings | playing | paused | gameOver | win | highScores
    focus: null,
    message: "",
    error: ""
  },

  audio: {
    musicTrack: null,
    lastSoundAt: {}
  }
};
```

## 2.3 Module specifics

| Module | Responsibilities | Required functions |
| --- | --- | --- |
| `main.js` | Boot, run lifecycle, fixed-step loop, level progression. | `init()`, `startRun(difficulty)`, `startLevel(index)`, `update(dt)`, `completeLevel()`, `loseLife()`, `gameOver()`, `winGame()` |
| `global.js` | Single mutable context. | `getContext()` |
| `input.js` | Keyboard remapping, action state, pressed state, buffers. | `getActionState(action)`, `getActionPressed(action)`, `setActionState(action, value)`, `setActionPressed(action, value)`, `setRemap(action, keys)`, `getRemap()`, `resetRemap()`, `clearBuffers()` |
| `player.js` | Frog movement, jump, hit, respawn. | `updatePlayer(dt)`, `tryJump()`, `applyHit(source)`, `respawnPlayer()`, `getPlayerAABB()`, `getMotionState()` |
| `physics.js` | Static and dynamic bodies, substepping, impulse response. | `initPhysics()`, `addStaticBox(box)`, `addDynamicBox(obj)`, `addDynamicCircle(obj)`, `stepPhysics(dt)`, `applyPlayerImpulse(body, player)`, `getBodies()` |
| `level.js` | Level loading, exit detection, level bounds. | `loadLevel(id)`, `unloadLevel()`, `isExitReached(playerAABB)`, `getLevelBounds()` |
| `hazards.js` | Fixed hazards, collision, life loss. | `loadHazards(level)`, `updateHazards(dt)`, `checkHazards(playerAABB)`, `getHazardState()` |
| `collectibles.js` | Golden Fly collection, set tracking. | `loadCollectibles(level)`, `checkCollectibles(playerAABB)`, `getCollectibleState()`, `getRemaining()` |
| `scoring.js` | Points, bonuses, high scores. | `addPoints(amount, reason)`, `finishLevel()`, `computeLevelBonus()`, `loadHighScores()`, `saveHighScore(entry)`, `getHighScores()`, `getScoreBreakdown()` |
| `render.js` | Canvas rendering, camera, particles, hit flash. | `renderFrame(ctx)`, `drawPlayer()`, `drawLevel()`, `drawHazards()`, `drawCollectibles()`, `drawPhysicsObjects()`, `drawExit()`, `spawnParticles(kind, x, y)`, `applyHitFlash()` |
| `audio.js` | Synthesized sounds and chiptune music. | `playSound(name)`, `playMusic(name)`, `stopMusic()` |
| `ui.js` | HTML/CSS screens, HUD, settings UI, focus. | `setScreen(name)`, `updateHUD()`, `showMessage(text)`, `bindSettings()`, `renderHighScores(scores)` |
| `storage.js` | Local persistence for high scores. | `loadHighScores()`, `saveHighScores(scores)` |
| `debug.js` | Direct access for tests and debug. | `debugPlatforming()`, `debugPhysics()`, `debugHazards()`, `debugCollectibles()`, `debugScoring()`, `debugInputLeft(on)`, `debugInputRight(on)`, `debugInputJump(on)`, `debugInputPause(on)` |

# 3. VISUAL SPEC

The game is a bright, silly bog rendered as low-resolution pixel art. Everything is built from 16×16 tiles and small 16×16 sprites with thick black outlines, flat saturated colour, and no gradients. The player is a green frog with huge eyes and a tiny crooked crown. Hazards are fixed enemy-like dangers: snap traps, electric puddles, and spike lilies. Physics objects are grey crates, barrels, balls, and planks with clear blue bolt or wheel markings. Collectibles are golden flies that glow with a yellow pixel halo. The exit is a blue sunbeam gate with a white arrow. The screen is always readable at small size and uses shape plus colour, never colour alone.

Lighting is flat and cheerful. There is no dynamic light, no soft shadow, and no bloom. Depth is communicated by black outlines, light top highlights, and dark bottom edges. Hit flash is the only moment the sprite becomes white. Particles are tiny square pixels. Reduced motion disables particles and uses one static white frame for hit flash.

The space is a side-on cartoon bog and castle path. Each level is a rectangular map larger than the 640×360 camera. The camera follows the player horizontally and vertically with a deadzone and clamps to level bounds. Platforms are mossy stone, wooden dock, and castle brick tiles. Hazards are visually distinct by shape: spikes are triangular, electric ponds zig-zag, snap traps have open mouths. Physics objects are neutral grey with blue markings so they are not confused with hazards or collectibles.

## Palette

| Role | Hex | Usage | Colour-blind note |
| --- | --- | --- | --- |
| Background dark | `#101018` | Sky, cave, UI background | High contrast |
| Background light | `#1F2430` | Distant bog shapes | Low contrast, not gameplay |
| Player body | `#009E73` | Flap body | Distinct from orange and yellow |
| Player outline | `#000000` | All sprites | Always present |
| Player highlight | `#FFFFFF` | Eyes, outline inner | Shape cue |
| Platform stone | `#555555` | Static platforms | Neutral |
| Platform edge | `#888888` | Top highlight | Shape cue |
| Hazard primary | `#D55E00` | All hazards | Orange-vermillion, not red/green pair |
| Hazard secondary | `#FFFFFF` | Sparks, teeth, spike tips | Shape cue |
| Collectible | `#F0E442` | Golden flies | Yellow, distinct from hazard orange |
| Exit | `#0072B2` | Sunbeam gate | Blue, distinct from player green |
| Physics neutral | `#7F7F7F` | Crates, barrels, balls, planks | Neutral |
| Physics marker | `#56B4E9` | Bolts, wheels, plank edges | Light blue, shape cue |
| UI text | `#FFFFFF` | Pixel font | High contrast |
| UI focus | `#F0E442` | Focus ring | Yellow |
| Particle hit | `#D55E00` | Hazard particles | Matches hazard |
| Particle collect | `#F0E442` | Collect particles | Matches collectible |
| Particle dust | `#FFFFFF` | Landing dust | Neutral |

## Recipe table

| Element | Dimensions | Visual recipe | Animation | Rule implied |
| --- | ---: | --- | --- | --- |
| Flap | 16×16 sprite, 12×14 hitbox | Green oval body, white eyes, black pupils, small yellow crown | Idle 2 frames, run 4 frames, jump/fall 1 frame each | Player hitbox is slightly smaller than sprite |
| Static platform | 16×16 tile | Grey stone, black outline, light top edge | None | Solid collision |
| Spike Lily | 16×16 | Orange base, white triangular spikes | None | Fixed hazard, hurts on touch |
| Electric Pond | 16×16 or 32×16 | Dark base, white zig-zag, orange sparks | 2-frame spark, disabled by reduced motion | Fixed hazard, hurts on touch |
| Snap-Fly Trap | 24×16 | Orange mouth, white teeth, black interior | 2-frame chomp, disabled by reduced motion | Fixed hazard, hurts on touch |
| Wobbly Crate | 16×16 | Grey box, blue bolts | None | Pushable, stackable, solid |
| Rolling Barrel | 16×32 | Grey barrel, blue rings | None | Heavier pushable, solid |
| Bouncy Ball | circle r=8 | Grey circle, white highlight, blue seam | None | Bouncy, rolls, can be stood on |
| Plank | 64×8 | Grey plank, blue edge | None | Long pushable platform |
| Golden Fly | 10×10 | Yellow body, white wings, black eyes | 2-frame bob, disabled by reduced motion | Collectible set |
| Exit | 16×24 | Blue portal, white arrow, yellow sunbeam edge | 2-frame pulse, disabled by reduced motion | Reaching it completes level |
| Score HUD | 640×360 coordinate | Pixel font, white text, black outline | None | Score display |
| Hit flash | Player-sized | White 1-frame overlay | 0.18 s normal, 1 frame reduced | Damage feedback |
| Particles | 1–3 px squares | Orange, yellow, or white squares | 0.25–0.6 s life | Feedback only |

# 4. GAMEPLAY SPEC

The player is Flap, a loud little frog crossing five levels of bog, traps, and castle rooftops. The player moves left and right, jumps under gravity, and uses physics objects such as crates, barrels, balls, and planks to reach platforms and exits. Hazards are fixed, enemy-like dangers: spike lilies, electric ponds, and snap-fly traps. Touching a hazard or falling out of bounds costs one life and restarts the level. Golden Flies are hidden collectibles forming a set of 78. Reaching the exit completes a level. Reaching the exit of Level 5 wins the game. Losing all lives produces Game Over. Scoring rewards collectibles, level completion, perfect play, and fast play.

## Records with rosters

### Player record

| Field | Type | Initial | Rules |
| --- | --- | ---: | --- |
| `player.x`, `player.y` | float px | level.spawn | Position in level coordinates |
| `player.vx`, `player.vy` | float px/s | 0 | Velocity |
| `player.width`, `player.height` | int px | 12, 14 | Collision box |
| `player.grounded` | bool | false | True when supported by upward normal |
| `player.coyoteTimer` | float s | 0 | Counts down after leaving ground |
| `player.jumpBufferTimer` | float s | 0 | Counts down after jump input |
| `player.invulnTimer` | float s | 0 | After hit, ignores hazards |
| `player.hitFlashTimer` | float s | 0 | White flash duration |
| `player.facing` | int | 1 | 1 right, -1 left |
| `player.animState` | string | idle | idle, run, jump, fall, hit |
| `player.alive` | bool | true | False after Game Over |

### Physics object roster

| Type | Shape | Mass | Friction | Restitution | Player use |
| --- | --- | ---: | ---: | ---: | --- |
| Wobbly Crate | 16×16 AABB | 2.0 | 0.50 | 0.05 | Push, stack, stand on |
| Rolling Barrel | 16×32 AABB | 3.0 | 0.35 | 0.05 | Push heavy objects, block gaps |
| Bouncy Ball | circle r=8 | 1.0 | 0.15 | 0.78 | Roll, bounce, stand on |
| Plank | 64×8 AABB | 4.0 | 0.60 | 0.00 | Bridge, see-saw, stack base |

### Hazard roster

| Type | Size | Hitbox | Damage | Fixed behaviour |
| --- | ---: | ---: | ---: | --- |
| Spike Lily | 16×16 | 12×12 centred | 1 life | Static, always active |
| Electric Pond | 16×16 or 32×16 | full rectangle | 1 life | Static, always active |
| Snap-Fly Trap | 24×16 | 20×12 centred | 1 life | Static, always active |

### Collectible roster

| Type | Hitbox | Count per level | Set total | Points when scored |
| --- | ---: | ---: | ---: | ---: |
| Golden Fly | 10×10 | Level 1: 10, Level 2: 14, Level 3: 16, Level 4: 18, Level 5: 20 | 78 | 100 |

### Exit record

| Field | Type | Value | Rules |
| --- | --- | ---: | --- |
| `level.exit.x`, `level.exit.y` | float px | per level | Position |
| `level.exit.width`, `level.exit.height` | int px | 16, 24 | Player AABB overlap completes level |
| `level.exit.active` | bool | true | False only during transition |

### Level roster

| ID | Name | Size (tiles) | Par time | Start | Exit | Static platforms | Hazards | Physics objects | Collectibles | Key goal |
| ---: | --- | ---: | ---: | --- | --- | ---: | --- | --- | ---: | --- |
| 1 | Lily Pad 101 | 48×28 | 150 s | 4,20 | 42,8 | 20 | 3 Spike Lily | 2 crates | 10 | Jump, push a crate, reach exit |
| 2 | The Fly Trap | 64×28 | 210 s | 4,20 | 58,12 | 35 | 4 Spike Lily, 3 Snap-Fly Trap | 4 crates, 1 barrel | 14 | Use crates and barrel to cross gaps |
| 3 | Crate Hopping | 80×32 | 240 s | 4,24 | 72,10 | 45 | 5 Spike Lily, 4 Electric Pond | 6 crates, 2 barrels, 1 plank | 16 | Stack crates and use plank |
| 4 | Bouncy Bog | 96×32 | 270 s | 4,24 | 88,12 | 50 | 6 Spike Lily, 5 Electric Pond, 4 Snap-Fly Trap | 4 crates, 5 balls, 2 planks | 18 | Use balls to reach high ledges |
| 5 | King Fly Castle | 112×36 | 300 s | 4,28 | 104,8 | 70 | 7 Spike Lily, 6 Electric Pond, 6 Snap-Fly Trap | 6 crates, 4 barrels, 5 balls, 3 planks | 20 | Combine push, stack, bounce, and avoidance |

## 4.1 Platforming (Tier 1)

| Rule | Number |
| --- | ---: |
| Input: move left | `left` action sets horizontal acceleration negative |
| Input: move right | `right` action sets horizontal acceleration positive |
| Input: jump | `jump` action starts jump if grounded or coyote available, or buffers jump |
| Input: pause | `pause` action toggles Pause while playing |
| Horizontal max speed | 160 px/s |
| Ground acceleration | 1600 px/s² |
| Air acceleration | 1200 px/s² |
| Ground friction | 2600 px/s² |
| Air friction | 400 px/s² |
| Jump velocity | -420 px/s |
| Gravity | 1200 px/s² |
| Terminal fall | 420 px/s |
| Maximum jump height | 73.5 px from flat ground |
| Minimum jump height | approximately 13.5 px if released immediately after velocity reaches -180 |
| Coyote time | 0.10 s |
| Jump buffer | 0.10 s |
| Variable jump cutoff | If jump released while `vy < -180`, set `vy = -180` |
| Landing threshold | `vy > 300` triggers land sound and dust |
| Grounded rule | Contact normal y > 0.8 while `vy >= 0` |
| Facing | Set to movement direction when horizontal input is active |
| Out-of-bounds death | `player.y > level.height + 32` |
| Respawn | Reset to `level.spawn`, zero velocity, apply invulnerability |
| Invulnerability after respawn | Normal 1.2 s, Easy 1.8 s, Hard 0.8 s |

## 4.2 Physics (Tier 1)

| Rule | Number |
| --- | ---: |
| Physics fixed step | 1/60 s |
| Physics substeps | 3 per step, dt = 1/180 |
| Static platforms | Friction 0.8, restitution 0.0 |
| Player mass | 1.0 |
| Player restitution | 0.0 |
| Player friction | 0.25 |
| Max body speed | 600 px/s |
| Player push impulse | Horizontal impulse = `clamp(player.vx * 0.9 + sign(player.vx) * 120, -300, 300)` |
| Player vertical push impulse | Vertical impulse = `clamp(player.vy * 0.8 + sign(player.vy) * 80, -300, 300)` |
| Stand on dynamic bodies | Allowed if contact normal is upward and body supports player |
| Collision layers | Player solid vs static/dynamic; hazards sensor; collectibles sensor; exit sensor |
| Ball bounce | Restitution 0.78 |
| Crate stack stability | Crate friction 0.50, restitution 0.05 |
| Barrel roll | Barrel friction 0.35, restitution 0.05 |
| Plank use | Plank is a long pushable solid, not a fixed bridge |
| No grab | Player cannot carry, throw, or attach objects |
| No breakables | Physics objects never break |
| No physics hazards | Physics objects do not damage the player |

## 4.3 Hazards (Tier 1)

| Rule | Number |
| --- | ---: |
| Hazard placement | Fixed in level data, never AI-driven |
| Hazard collision | AABB overlap with player hitbox |
| Hazard damage | 1 life |
| Hit response | Decrement lives, set `invulnTimer`, spawn hit particles, apply hit flash |
| Hit flash duration | 0.18 s normal, 1 fixed frame when reduced motion is on |
| Invulnerability | Normal 1.2 s, Easy 1.8 s, Hard 0.8 s |
| During invulnerability | Hazards do not damage; player sprite blinks white/black every 0.12 s |
| Life reaches 0 | Game Over |
| Life > 0 | Restart current level at `level.spawn` |
| Hazard destruction | None |
| Hazard movement | None |
| Hazard activation | Always active |
| Hazard sound | Plays once per hit |
| Hit particles | 12 orange squares, life 0.45 s, disabled by reduced motion |

## 4.4 Collectibles (Tier 2)

| Rule | Number |
| --- | ---: |
| Collectible type | Golden Fly |
| Hitbox | 10×10 |
| Collection | Player AABB overlap sets `collected = true` |
| Input | No dedicated input; collected by existing movement and jump inputs |
| Total set | 78 Golden Flies across all levels |
| Level 1 | 10 |
| Level 2 | 14 |
| Level 3 | 16 |
| Level 4 | 18 |
| Level 5 | 20 |
| Set tracking | `collectibles.collected` and `collectibles.total` |
| Set complete | `collected == 78` |
| Visual feedback | 8 yellow particles on collection, disabled by reduced motion |
| Sound | `collect` sound |
| Pause display | “Flies: collected/total in current level” |
| Win display | “Flies found: X/78” |
| Scoring | Not active until Tier 3 |

## 4.5 Scoring (Tier 3)

| Event | Points | Notes |
| --- | ---: | --- |
| Golden Fly collected | 100 | Only when scoring is enabled |
| Level clear | 1000 | Added when exit is reached |
| Collect all flies in level | 2000 | Added when level collectibles complete |
| No-hit level | 1500 Normal/Hard, 0 Easy | No-hit tracked per level |
| Time bonus | `floor((parTime - levelTime) * 20)` capped at 1000 | Normal/Hard only, Easy disabled |
| Final win bonus | 5000 | Added only on Level 5 completion |
| High score list | Top 10 | Stored locally |
| Best score | Highest of high scores | Displayed on Win/Game Over |

Scoring rules:

- Score is added only at discrete events.
- Life loss does not subtract score.
- Restarting a level after life loss does not refund points already awarded.
- High score entry stores: `score`, `difficulty`, `completedLevels`, `dateISO`.
- High scores are sorted descending by score.
- If score exceeds best, Win/Game Over shows “NEW BEST”.
- Changing difficulty starts a new run and clears current score.

## 4.6 Progression and Difficulty

### Progression

| Step | Behaviour |
| --- | --- |
| Title | Start Run begins Level 1 |
| Level complete | Award Tier 3 bonuses if enabled, increment `completedLevels`, load next level |
| Level 5 complete | Win screen |
| Game Over | Stop run, show Game Over |
| Retry from Game Over | New run from Level 1, score reset |
| Quit to Title | Run discarded, score discarded, high score not saved unless Game Over or Win occurs |
| Pause | Freeze timers and physics |
| Resume | Restore state |
| Settings from pause | Reduced motion and remaps allowed; difficulty locked |
| Settings from title | Difficulty, reduced motion, remaps allowed |

### Difficulty

| Option | Lives | Invulnerability | Time bonus | No-hit bonus | Par time |
| --- | ---: | ---: | ---: | ---: | ---: |
| Easy | 9 | 1.8 s | Disabled | 0 | Par values are ignored for time bonus |
| Normal | 3 | 1.2 s | Enabled | 1500 | Par values from level roster |
| Hard | 1 | 0.8 s | Enabled | 2500 | Par values from level roster |

### Feel

The game should feel springy, forgiving, and silly. Coyote time and jump buffer make mistakes feel recoverable. Jump height is enough to clear four tiles but not so high that levels feel floaty. Physics objects are heavy but responsive: crates stack, barrels roll slowly, balls bounce, planks bridge gaps. Hazards are never hidden: every danger has a visible shape and colour pattern. Collecting a fly is a bright reward, but never required for the win. Losing a life is a comedic “ribbit!” moment, not a punishment-heavy failure.

# 5. CHARACTERS

## Flap the Frog

- Silhouette: small rounded body, wide eyes, short legs, tiny crooked crown.
- Facing: left/right only.
- States:
  - `idle`: crown wobbles 1 px every 0.8 s.
  - `run`: four-frame cycle, body squash 1 px, legs alternate.
  - `jump`: one frame, legs tucked, mouth open.
  - `fall`: one frame, legs spread, crown tilted.
  - `hit`: one or two white flash frames, eyes become X shapes.
- Animation rules:
  - Idle animation speed: 2 frames, 500 ms each.
  - Run animation speed: 4 frames, 120 ms each.
  - Jump/fall frames do not loop.
  - Hit animation: 0.18 s white flash, or 1 frame when reduced motion is on.
  - Reduced motion: idle/run animations are static; hit flash one frame.

## Fixed Hazard Enemies

These are not AI enemies. They are fixed hazards with silhouettes.

| Hazard | Silhouette | Animation | Reduced motion |
| --- | --- | --- | --- |
| Spike Lily | Orange base, white triangular spikes | Static | Static |
| Electric Pond | Dark base, white zig-zag, orange sparks | 2-frame spark, 200 ms/frame | Static |
| Snap-Fly Trap | Orange mouth, white teeth, black interior | 2-frame chomp, 500 ms/frame | Static |

## Golden Fly

- Silhouette: small yellow oval body, white wings, black eyes.
- Animation: 2-frame bob, 150 ms/frame.
- Reduced motion: static.
- Collected state: not drawn.

## Exit

- Silhouette: blue vertical portal with white arrow and yellow sunbeam edge.
- Animation: 2-frame pulse, 250 ms/frame.
- Reduced motion: static.

# 6. AUDIO

| Sound | Recipe | Plays |
| --- | --- | --- |
| `music_title` | Chiptune loop, 120 BPM. Bass: square wave A2 110 Hz, 8 notes/bar. Lead: triangle wave C4/E4/G4 arpeggio. Percussion: noise bursts on 8ths. | Title, Settings, Pause, Game Over, Win, High Scores |
| `music_game` | Chiptune loop, 140 BPM. Bass: square wave F2 87 Hz. Lead: triangle wave F3/A3/C4. Hat: short noise bursts every 16th. | Playing |
| `jump` | Square wave, glide 220 Hz to 440 Hz, 0.12 s, volume 0.45 | Player jumps |
| `land` | Noise burst 0.08 s plus square 80 Hz decay, volume 0.35 | Player lands with `vy > 300` |
| `collect` | Two square blips: 880 Hz 0.05 s, 1320 Hz 0.07 s, volume 0.5 | Golden Fly collected |
| `hit` | Sawtooth glide 180 Hz to 60 Hz, 0.35 s, plus noise burst, volume 0.65 | Hazard hit or out-of-bounds death |
| `lifeLost` | Square glide 392 Hz to 196 Hz, 0.50 s, volume 0.6 | Life decremented but not game over |
| `gameOver` | Triangle glide 262 Hz to 131 Hz, 1.0 s, volume 0.7 | Lives reach 0 |
| `levelWin` | Square arpeggio 523, 659, 784, 1046 Hz, 0.08 s each, volume 0.55 | Exit reached |
| `finalWin` | Longer arpeggio 523, 659, 784, 1046, 1319 Hz, 0.10 s each, volume 0.65 | Level 5 completed |
| `uiMove` | Square 660 Hz, 0.03 s, volume 0.3 | Menu focus changes |
| `uiConfirm` | Square 880 Hz, 0.08 s, volume 0.35 | Menu confirm |
| `pauseToggle` | Square 440 Hz, 0.06 s, volume 0.35 | Pause/resume |
| `physicsBounce` | Square glide 320 Hz to 520 Hz, 0.06 s, volume 0.45 | Ball bounces hard |
| `crateMove` | Short noise burst 0.05 s, volume 0.25 | Crate slides |
| `crateLand` | Square 120 Hz decay, 0.07 s, volume 0.4 | Crate lands hard |
| `plankHit` | Square 180 Hz decay, 0.07 s, volume 0.35 | Plank collides |

Audio rules:

- All sounds are synthesized in the audio API. No sample files are required.
- Music loops seamlessly.
- Music stops during Game Over and Win only after a short sting.
- Reduced motion does not change audio.
- No sound plays while paused except UI sounds in Pause/Settings.

# 7. UX

All menu screens are HTML/CSS. The gameplay canvas is separate. The state machine toggles visibility of DOM screens. No gameplay UI is drawn in the canvas.

## State machine

| State | Entry | Visible UI | Allowed actions | Exit |
| --- | --- | --- | --- | --- |
| `title` | Boot or quit | Title screen, Start Run, Settings, High Scores | Start, Settings, High Scores | Settings, High Scores, Playing |
| `settings` | From Title or Pause | Settings panel | Change reduced motion, remap keys, choose difficulty if from Title | Title or Pause |
| `playing` | Start Run or next level | Gameplay canvas, Score HUD | Move, jump, pause | Pause, Game Over, next level, Win |
| `paused` | Pause action | Pause overlay | Resume, Settings, Quit to Title | Playing, Settings, Title |
| `gameOver` | Lives reach 0 | Game Over, score, high score rank | Retry, High Scores, Title | Title, High Scores, Playing |
| `win` | Level 5 exit | Win, final score, high score rank | Play Again, High Scores, Title | Title, High Scores, Playing |
| `highScores` | From Title or end screens | Top 10 scores | Back | Title or end screen |

## Screens

### Title

- Pixel-font title: “RIBBIT ROCKET”.
- Buttons: Start Run, Settings, High Scores.
- Keyboard focus visible with yellow outline.
- Silly subtitle: “Hop through the bog. Don’t get fly-trapped.”

### Settings

- Colour-blind safe palette: always enabled, not toggleable.
- Reduced motion: checkbox.
- Difficulty: Easy / Normal / Hard, only from Title.
- Remappable keys:
  - Left
  - Right
  - Jump
  - Pause
  - Confirm
  - Back
  - Menu Up
  - Menu Down
  - Menu Left
  - Menu Right
- Remapping UI:
  - Focus an action.
  - Press a key to remap.
  - Escape cancels.
  - Conflicts are allowed but warned.
  - Reset Defaults button.

### Pause

- Resume.
- Settings.
- Quit to Title.
- Shows current score and lives remaining.
- Shows current level flies collected.

### Game Over

- “NO MORE RIBBITS”
- Final score.
- Lives remaining: 0.
- High score rank if top 10.
- Buttons: Try Again, High Scores, Title.

### Win

- “THE CROWN IS YOURS”
- Final score.
- Breakdown: flies, level bonuses, time bonuses.
- Flies found: X/78.
- High score rank if top 10.
- Buttons: Play Again, High Scores, Title.

### High Scores

- Table: Rank, Score, Difficulty, Levels, Date.
- Top 10 only.
- Back button.

## HUD

| Element | Record field | When visible |
| --- | --- | --- |
| Score | `scoring.current` | Only while `ui.screen === "playing"` |

HUD rules:

- Score is drawn at top-left of canvas using pixel font.
- No lives, timer, level, or collectible HUD during play.
- Score updates immediately after scoring events.
- If Tier 3 scoring is not built, Score remains visible and displays `0`.

# 8. DEBUG API

```js
window.frogDebug = {
  platforming() {
    return {
      x: G.player.x,
      y: G.player.y,
      vx: G.player.vx,
      vy: G.player.vy,
      grounded: G.player.grounded,
      coyoteTimer: G.player.coyoteTimer,
      jumpBufferTimer: G.player.jumpBufferTimer,
      facing: G.player.facing,
      animState: G.player.animState
    };
  },

  physics() {
    return {
      bodies: G.physics.bodies.map(b => ({
        id: b.id,
        type: b.type,
        x: b.x,
        y: b.y,
        vx: b.vx,
        vy: b.vy,
        mass: b.mass,
        friction: b.friction,
        restitution: b.restitution
      })),
      substep: G.physics.substep
    };
  },

  hazards() {
    return {
      count: G.level.hazards.length,
      hazards: G.level.hazards.map(h => ({
        id: h.id,
        type: h.type,
        x: h.x,
        y: h.y,
        active: h.active
      })),
      invulnTimer: G.player.invulnTimer,
      hitFlashTimer: G.player.hitFlashTimer
    };
  },

  collectibles() {
    return {
      total: G.collectibles.total,
      collected: G.collectibles.collected,
      setComplete: G.collectibles.setComplete,
      remaining: G.level.collectibles.filter(c => !c.collected).length
    };
  },

  scoring() {
    return {
      current: G.scoring.current,
      bonuses: G.scoring.bonuses,
      highScores: G.scoring.highScores,
      bestScore: G.scoring.bestScore,
      noHit: G.scoring.noHit
    };
  },

  inputLeft(on) { G.input.actions.left = on; },
  inputRight(on) { G.input.actions.right = on; },
  inputJump(on) { G.input.actions.jump = on; },
  inputPause(on) { G.input.actions.pause = on; }
};
```

# 9. TESTS

## Tier 1 tests

| Test | Pass condition |
| --- | --- |
| Fixed loop starts | `init()` starts a 60 Hz update loop and renders a frame |
| Input left/right | `frogDebug.inputLeft(true)` causes negative `vx`; `inputRight(true)` causes positive `vx` |
| Jump | `inputJump(true)` while grounded sets `vy <= -420` |
| Coyote time | Jump within 0.10 s after leaving ground succeeds |
| Jump buffer | Jump within 0.10 s before landing succeeds on landing |
| Variable jump | Releasing jump at `vy < -180` sets `vy = -180` |
| Platform collision | Player cannot pass through static platform AABB |
| Physics crate push | Player contact moves crate horizontally |
| Physics ball bounce | Dropped ball bounces with restitution near 0.78 |
| Physics stack | Crate can rest on another crate without tunnelling |
| Hazard hit | Overlap with hazard decrements lives, sets invuln, applies hit flash |
| Invulnerability | Second hazard overlap during invuln does not decrement lives |
| Out of bounds | Falling below level height decrements lives |
| Level exit | Overlap exit completes level |
| Game Over | Lives reach 0 sets `ui.screen === "gameOver"` |
| Win | Completing final level sets `ui.screen === "win"` |
| Pause | Pause action freezes physics and timers |
| HUD score visible | Score DOM element is visible during playing |
| Art and audio | Pixel sprites render, chiptune music starts, required sounds play |
| Effects | Hit particles and hit flash occur unless reduced motion is enabled |

## Tier 2 tests

| Test | Pass condition |
| --- | --- |
| Load all levels | Levels 2–5 load with correct counts and bounds |
| Collectible count | Total collectibles across levels equals 78 |
| Collection | Overlap marks collectible collected and increments count |
| Set tracking | `collectibles.setComplete` becomes true only at 78/78 |
| Pause status | Pause shows lives and current level fly count |
| Settings screen | Settings reachable from Title and Pause |
| Reduced motion | Toggling disables particles and one-frame hit flash |
| Remap | Changing `jump` remap makes new key trigger jump |
| Difficulty easy | Easy starts with 9 lives and no time bonus |
| Difficulty normal | Normal starts with 3 lives |
| Difficulty hard | Hard starts with 1 life |
| Colour-blind palette | No palette entry outside approved palette table |

## Tier 3 tests

| Test | Pass condition |
| --- | --- |
| Collectible points | Collecting fly adds 100 when scoring enabled |
| Level clear points | Completing level adds 1000 |
| Collect-all bonus | Completing level with all flies adds 2000 |
| No-hit bonus | Completing level with no hit adds 1500 Normal, 2500 Hard, 0 Easy |
| Time bonus | Completing under par adds capped time bonus Normal/Hard only |
| High score save | Score appears in `localStorage` after Game Over or Win |
| High score sort | High Scores screen displays top 10 sorted descending |
| Best score | Win/Game Over shows “NEW BEST” when current score exceeds previous best |

# 10. BUILD ORDER

1. Create HTML shell, pixel font CSS, canvas, DOM screens, global context.
2. Implement fixed 60 Hz loop and pause handling.
3. Implement input actions and default remaps.
4. Implement camera and level bounds.
5. Implement player AABB movement, gravity, jump, coyote, buffer, variable jump.
6. Implement static platform collision.
7. Implement physics bodies: static, crate, barrel, ball, plank.
8. Implement player impulse push and standing on dynamic bodies.
9. Implement hazards, hit, life loss, invulnerability, respawn.
10. Implement Level 1, exit, level completion, Game Over, Win.
11. Implement pixel art rendering for player, platforms, hazards, physics, exit.
12. Implement particles and hit flash.
13. Implement audio API, chiptune music, required sound effects.
14. Implement Title, Pause, Game Over, Win, Score HUD.
15. Add Levels 2–5 with exact rosters.
16. Add Golden Fly collectibles and set tracking.
17. Add Settings, reduced motion, remappable keys, difficulty options.
18. Add scoring events, bonuses, high score storage, High Scores screen.
19. Add debug API and run tests.
20. Polish copy, animation timing, accessibility focus order.

# 11. DEFINITION OF DONE

## Tier 1

High-level done: A player can start the game, play one complete frog platforming level using platforming, physics, and hazards, reach the exit, see Win, lose lives, see Game Over, pause, and experience the required pixel/chiptune presentation and HUD.

Checkboxes:

- [ ] Fixed 60 Hz loop.
- [ ] Input actions work and are buffered.
- [ ] Player moves and jumps with specified numbers.
- [ ] Static platforms collide correctly.
- [ ] Physics objects move and can be used to reach the exit.
- [ ] Crates, barrels, balls, and planks exist.
- [ ] Hazards are fixed and cause life loss.
- [ ] Falling out of bounds causes life loss.
- [ ] Lives decrement and Game Over triggers at 0.
- [ ] Exit completes Level 1.
- [ ] Win screen appears after final Tier 1 level.
- [ ] Pause freezes gameplay.
- [ ] Title, Pause, Game Over, Win screens exist.
- [ ] Score HUD is visible and displays `0`.
- [ ] Pixel art sprites and level tiles are drawn.
- [ ] Colour palette is the approved colour-blind safe palette.
- [ ] Pixel font is used.
- [ ] Chiptune music starts.
- [ ] Required sound effects play.
- [ ] Particles and hit flash occur normally.
- [ ] Debug API exposes platforming, physics, hazards, and input functions.

## Tier 2

High-level done: The full 5-level session exists, collectibles are a complete set, and accessibility settings are usable.

Checkboxes:

- [ ] Levels 2–5 load.
- [ ] Level rosters match counts and par times.
- [ ] 78 Golden Flies exist total.
- [ ] Collection updates set state.
- [ ] Pause shows lives and fly count.
- [ ] Settings screen works from Title and Pause.
- [ ] Reduced motion disables particles and reduces hit flash.
- [ ] Remappable keys work for all actions.
- [ ] Difficulty options set lives and tuning.
- [ ] Colour-blind safe palette remains enforced.
- [ ] Win and Game Over show lives remaining.

## Tier 3

High-level done: Scoring is active, bonuses work, and best scores persist.

Checkboxes:

- [ ] Collectible points add 100.
- [ ] Level clear adds 1000.
- [ ] Collect-all adds 2000.
- [ ] No-hit bonus works by difficulty.
- [ ] Time bonus works by difficulty.
- [ ] Final win bonus adds 5000.
- [ ] High scores save to local storage.
- [ ] High Scores screen shows top 10.
- [ ] Win/Game Over show best score and NEW BEST when appropriate.
- [ ] Score breakdown is shown on Win.

# A. SANITY

| Check | Result |
| --- | --- |
| Does the game keep exactly the requested mechanics? | Yes. Core: platforming, physics, hazards. Supporting: collectibles. Extra: scoring. No enemy AI, combat, inventory, checkpoint, or save systems were added. |
| Are “enemies” represented without adding a system? | Yes. Enemy-like dangers are fixed hazards only. |
| Are collectibles a set? | Yes. 78 Golden Flies total, tracked across levels. |
| Are scoring and high scores present? | Yes. Tier 3 scoring, bonuses, local high scores, best score display. |
| Is the session a sequence of levels? | Yes. Levels 1–5 in order, no free level select. |
| Is the game under 30 minutes? | Yes. Par times total 19:30, target real time 18–27 minutes. |
| Is failure losing a life? | Yes. Hazard or fall costs one life; Game Over at 0. |
| Is win reaching the exit? | Yes. Exit overlap completes level; Level 5 exit wins. |
| Is the HUD exactly score? | Yes. HUD table contains only Score. Lives appear only on non-HUD screens. |
| Are particles and hit flash included? | Yes. Defined with numbers and reduced-motion behaviour. |
| Is the palette saturated and colour-blind safe? | Yes. Okabe/Ito-inspired saturated palette with shape cues. |
| Is pixel art specified? | Yes. 16×16 sprites/tiles, visible pixels, limited palette, pixel font. |
| Is chiptune audio specified? | Yes. Synthesized waveforms, frequencies, envelopes, music and sound table. |
| Are required screens present? | Yes. Title, Settings, Playing, Pause, Game Over, Win, High Scores. |
| Are accessibility options present? | Yes. Colour-blind safe palette always, reduced motion, remappable keys, difficulty options. |
| Are numbers concrete? | Yes. Movement, physics, hazards, collectibles, scoring, levels, UI states all have numeric rules. |
| Are tiers aligned with mechanic bands? | Yes. Tier 1 core, Tier 2 collectibles and full content/accessibility, Tier 3 scoring. |
| Are contracts sufficient for tests? | Yes. Global fields and module functions are defined; debug API exposes each gameplay system and input. |
| Are there hidden contradictions? | No. Score HUD exists from Tier 1 but remains `0` until Tier 3; collectibles exist in Tier 2 but only score in Tier 3. |