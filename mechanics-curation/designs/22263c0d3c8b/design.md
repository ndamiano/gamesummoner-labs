# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Browser game an agentic AI will build | `index.html`, `src/main.js`, fixed-step browser loop |
| Platformer where you play as a frog | Player is a pixel frog; gameplay is platforming |
| 2d | Canvas side-on 2D world only |
| Camera: side-on | Fixed side-on camera, no scrolling camera system |
| Time model: real-time | Fixed real-time loop, pause freezes simulation |
| Movement model: free movement | Continuous horizontal movement and vertical jump physics |
| Session shape: a sequence of levels | 5 levels, unlocked in order, level select replays unlocked levels |
| Failure: restart the level | Hazard contact triggers automatic level restart |
| Tone: silly | Frog name, fly-jar goal, silly hazard names, chiptune bleeps, bright palette |
| Size: a handful of levels, under 30 minutes | 5 levels, target total clean completion time 7 min 20 s |
| Win/lose: reach the exit | Exit object completes level; final exit opens win screen |
| Core mechanics: platforming | Jump, run, land, avoid gaps, reach exit |
| Core mechanics: physics | Gravity, velocity, collision, jump height, air control |
| Core mechanics: hazards | Static spikes, moving saw hazards, biting dragonfly hazards |
| Supporting mechanics: none | No combat, health, lives, checkpoints, power-ups, inventory, timers, save system |
| Extra mechanics: collectibles | Golden Flies are tier 3 only and never required to finish |
| Art style: pixel art: low-resolution sprites, visible square pixels, limited palette | 640×360 internal canvas, integer scaling, 16 px sprites, 12-color palette |
| Palette: saturated: bright, strong colours | Palette table in Visual Spec |
| Typography: pixel font: blocky bitmap letters | 8×8 bitmap font for all UI |
| Music: chiptune: retro console bleeps | Synthesized chiptune music tracks |
| Sound effects style: retro bleeps: synthesized chip sounds | Synthesized sound table |
| Screens: title, pause, settings, win, level select | DOM screens and state machine |
| HUD: score | DOM HUD shows only score |
| Effects: particles, hit flash | Particle system and hit flash effect |
| Accessibility: colour-blind safe palette | Always-on palette with shape/luminance separation |
| Accessibility: reduced motion | Setting disables particles, bobbing, squash, screen flashes |
| Accessibility: remappable keys | Settings screen remaps left, right, jump, pause |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| Player identity | Gribbit the frog, a 16×16 pixel frog trying to reach a buzzing fly jar | Gives the game a concrete, silly protagonist without adding mechanics |
| Goal object | “Buzzing Fly Jar” exit | Matches frog/fly tone and is visually distinct from hazards |
| Camera | Fixed side-on camera per level, no scrolling | The provided camera decision does not require scrolling; fixed screens keep scope small and avoid a camera system |
| Internal resolution | 640×360 logical pixels | Large enough for platforming, small enough for visible pixel art; integer scaling preserves square pixels |
| Tile size | 16×16 px | Standard pixel-art platformer unit |
| Level count | 5 levels | “Handful” while allowing a complete sequence under 30 minutes |
| Session flow | Title → Level Select → Level 1 → Level 2 → Level 3 → Level 4 → Level 5 → Win | Required sequence of levels plus required level select and win screens |
| Failure handling | Instant level restart after 0.5 s hit sequence | Required failure rule; avoids lives/health systems |
| Score source | +500 per level clear, +100 per Golden Fly | HUD score is required. Tier 1 can use level-clear score; collectibles are tier 3 extras |
| Max score | 6000 | 30 collectibles × 100 + 5 level clears × 500 |
| Collectibles | Golden Flies, 30 total, optional | Extra mechanic only; never required to reach exit |
| Enemies | Biting Dragonfly hazards | “Enemies” are represented as moving hazards, not a separate combat system |
| Traps | Reed Spikes static hazards, Whirring Saw moving hazards | Hazards are core; no extra trap system |
| Platforms | Solid rectangles only, no one-way platforms | Keeps physics and platforming finite and testable |
| Death model | One hit restarts level | No health, no combat, no lives |
| Physics style | Tuned arcade platformer with coyote time and jump buffering | Makes core platforming feel fair without adding new mechanics |
| Randomness | No gameplay randomness | Keeps tests deterministic |
| Particles | Deterministic decorative particles only | Required effect, but not a random system |
| Save system | In-memory only | No save requirement; level select unlocks during current session |
| Settings | Reduced motion, remappable keys; colour-blind safe palette is always on | Matches accessibility requirements without adding a separate palette system |
| Input | Keyboard only for gameplay; mouse/keyboard for UI | Avoids adding touch or controller systems not requested |
| Audio | Synthesized only | Required retro bleeps and chiptune, no external assets |
| UI | HTML/CSS DOM screens, not canvas UI | Required HTML/CSS screens |
| No added systems | No combat, health, lives, checkpoints, power-ups, timers, inventory, save, procedural generation, camera scrolling, one-way platforms, wall jumps, double jumps | The decisions list the game parts; extra systems are forbidden |

## 0.3 Tiers

1. **Tier 1 — Core playable frog platforming**
   - One complete level.
   - Player movement, jump, landing, collision, gravity, air control.
   - Static hazards and one moving hazard.
   - Exit completes the level.
   - Failure restarts the level.
   - Title, basic pause, one-level win screen.
   - Pixel art, palette, pixel font, HUD score, particles, hit flash, chiptune music, bleeps.
   - This is the guaranteed-buildable core game.

2. **Tier 2 — Required session completeness**
   - Five levels.
   - Level select with sequential unlocks.
   - Full pause menu.
   - Settings screen.
   - Reduced motion.
   - Remappable keys.
   - Win screen after level 5.
   - No supporting mechanics exist, so this tier is content and required presentation completion.

3. **Tier 3 — Extra collectibles**
   - Golden Fly pickups.
   - Collectible score.
   - Collectible particles and sound.
   - Collectible reset on level restart.
   - Collectibles are optional and never required for level completion.

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Item | Value | Notes |
| --- | --- | --- |
| Logical canvas | 640×360 px | Internal game resolution |
| Integer scale | 1, 2, 3, 4, 5, 6 | Fit browser window without stretching |
| Tile unit | 16 px | Used for level layout |
| Axis | `+x` right, `+y` down | Standard canvas coordinates |
| Time unit | seconds | Fixed timestep |
| Fixed timestep | 1/60 s | 60 Hz simulation |
| Max accumulator | 0.25 s | Prevents spiral of death |
| Player sprite | 16×16 px | Visual only |
| Player hitbox | 12×14 px | Offset `(2, 2)` from sprite top-left |
| Player max horizontal speed | 160 px/s | Ground and air |
| Ground acceleration | 1200 px/s² | With input |
| Air acceleration | 900 px/s² | With input |
| Ground friction | 1600 px/s² | No input |
| Air drag | 300 px/s² | No input |
| Jump velocity | -320 px/s | Initial upward impulse |
| Gravity | 900 px/s² | Normal |
| Falling multiplier | 1.35 | Applied when `vy > 0` |
| Jump cut velocity | -120 px/s | If jump released while `vy < -120`, set `vy = -120` |
| Terminal fall speed | 520 px/s | Clamp |
| Coyote time | 0.10 s | Jump shortly after leaving ground |
| Jump buffer | 0.12 s | Jump shortly before landing |
| Full jump height | about 57 px | 3.5 tiles |
| Minimum jump height | about 8 px | If jump is cut immediately |
| Full air time | about 0.71 s | Up and down at full jump |
| Safe platform gap | 96 px | 6 tiles |
| Required platform gap max | 112 px | 7 tiles |
| Hazard hitboxes | See Hazard table | AABB |
| Collectible hitbox | 12×12 px | AABB |
| Exit hitbox | 24×24 px | AABB |

## 1.2 Important conventions

| Rule | Contract |
| --- | --- |
| Fixed-step loop | Update simulation in 1/60 s steps. Render after steps. Do not use variable `dt` for gameplay. |
| Deterministic simulation | No `Math.random()` in gameplay. Decorative particle motion uses fixed offsets. |
| Collision order | Update input, update player motion, resolve x collisions, resolve y collisions, update hazards, check player/hazard collision, check exit, check collectibles. |
| AABB only | All gameplay collision is axis-aligned bounding boxes. |
| Pixel rendering | Physics positions may be floats; rendering rounds to integer pixels. |
| No external assets | Sprites, fonts, and audio are generated or synthesized. |
| UI is DOM | Title, pause, settings, win, level select, and HUD are HTML/CSS. The game canvas is only the playfield. |
| Pause freezes simulation | While paused, no gameplay updates, no audio simulation, no input buffering for gameplay. |
| Settings are in-memory | Session-only. No localStorage. |
| Reduced motion | When enabled: no particles, no bobbing, no squash, no screen flashes, no decorative animation. Essential state changes use static visual indicators. |
| Colour-blind safe palette | Always enabled. Never rely on red/green alone. |
| Remappable keys | Key map is data. Default keys are documented. Conflicts clear previous assignments. |
| Level restart | Restores level entities and player to level start. Preserves session score from before the level attempt. |
| Level select replay | Starting a level from level select resets session score to 0. |
| No hidden systems | No health, lives, checkpoints, power-ups, timers, combat, inventory, save, procedural generation, scrolling camera. |

# 2. CONTRACTS

## 2.1 Module layout

```text
index.html
styles/
  main.css
  screens.css
  hud.css
  pixel-font.css
src/
  main.js
  context.js
  settings.js
  input.js
  levels.js
  level.js
  platforming.js
  physics.js
  hazards.js
  collectibles.js
  score.js
  effects.js
  render.js
  audio.js
  ui.js
  debug.js
tests/
  tier1-tests.js
  tier2-tests.js
  tier3-tests.js
```

## 2.2 Global context

The game uses one global context object. All gameplay rules read and write through it.

```js
window.frogGame = {
  mode: "title", // title | level_select | playing | paused | settings | win
  settings: {
    colorBlindSafe: true,
    reducedMotion: false,
    keyMap: {
      left: ["ArrowLeft", "KeyA"],
      right: ["ArrowRight", "KeyD"],
      jump: ["Space", "KeyW", "ArrowUp"],
      pause: ["Escape"]
    }
  },
  input: {
    actions: {
      left: false,
      right: false,
      jump: false,
      pause: false
    },
    pressed: {
      left: false,
      right: false,
      jump: false,
      pause: false
    },
    ui: {
      up: false,
      down: false,
      select: false,
      back: false,
      focusChanged: false
    }
  },
  runtime: {
    fixedDt: 1 / 60,
    accumulator: 0,
    lastTime: 0,
    frameCount: 0
  },
  session: {
    currentLevelIndex: 0,
    unlockedLevel: 0,
    score: 0,
    scoreAtLevelStart: 0,
    maxScore: 6000
  },
  level: {
    index: 0,
    width: 640,
    height: 360,
    spawn: { x: 32, y: 320 },
    exit: {
      x: 0,
      y: 0,
      w: 24,
      h: 24,
      active: false,
      reached: false
    },
    platforms: [], // {x,y,w,h}
    hazards: [], // {type,x,y,w,h,path,speed,dir,phase,active}
    collectibles: [] // {x,y,w,h,collected,id}
  },
  player: {
    x: 0,
    y: 0,
    w: 12,
    h: 14,
    vx: 0,
    vy: 0,
    facing: 1, // 1 right, -1 left
    onGround: false,
    coyoteTimer: 0,
    jumpBufferTimer: 0,
    jumpHeld: false,
    alive: true,
    animation: "idle", // idle | walk | jump | fall | hurt
    animationTimer: 0
  },
  effects: {
    particles: [], // {x,y,vx,vy,life,maxLife,color,size,kind}
    hitFlash: {
      active: false,
      timer: 0,
      maxTimer: 0.5
    },
    levelTransition: {
      active: false,
      timer: 0,
      maxTimer: 0.75
    }
  },
  audio: {
    currentMusic: null
  },
  ui: {
    currentScreen: "title",
    settingsReturnMode: "title",
    pauseReturnMode: "playing",
    selectedLevel: 0
  }
};
```

## 2.3 Module specifics

| Module | Exports / functions | State it owns or mutates |
| --- | --- | --- |
| `main.js` | `init()`, `requestFrame()`, `loop(timestamp)` | `runtime` |
| `context.js` | `getState()`, `setMode(mode)`, `resetSession()` | `mode`, `session`, `ui` |
| `settings.js` | `getSettings()`, `setReducedMotion(bool)`, `setKeyMap(map)`, `remapAction(action, code)`, `clearAction(action)` | `settings` |
| `input.js` | `initInput()`, `isDown(action)`, `isPressed(action)`, `consumePressed()`, `setDebugInput(action, bool)`, `getInputState()` | `input` |
| `levels.js` | `getLevelCount()`, `getLevel(index)`, `getLevelMetadata(index)` | Level data source |
| `level.js` | `loadLevel(index)`, `resetLevel()`, `startLevelAttempt()`, `completeLevel()`, `failLevel()`, `isExitReached()`, `getLevelState()` | `level`, `player`, `session`, `effects`, `mode` |
| `platforming.js` | `updatePlayerInput()`, `updatePlayerMotion()`, `updateJumpState()`, `resolveCollisions()`, `canPlayerJump()`, `getPlatformingState()` | `player` |
| `physics.js` | `integrateVelocity(player, dt)`, `applyGravity(player, dt)`, `clampVelocity(player)`, `collideRect(a, b)`, `resolveAxis(player, platforms, axis)`, `getPhysicsState()` | `player`, helper collision math |
| `hazards.js` | `updateHazards(dt)`, `checkPlayerHazards()`, `getHazardState()`, `getHazardAt(index)` | `level.hazards`, `effects`, `session` |
| `collectibles.js` | `updateCollectibles(dt)`, `checkPlayerCollectibles()`, `getCollectibleState()`, `getCollectibleAt(index)` | `level.collectibles`, `effects`, `session` |
| `score.js` | `addScore(points)`, `setScore(value)`, `getScore()`, `getMaxScore()`, `getScoreState()` | `session.score` |
| `effects.js` | `spawnParticles(kind, x, y, count)`, `startHitFlash()`, `startLevelTransition()`, `updateEffects(dt)`, `getEffectState()` | `effects` |
| `render.js` | `render()`, `drawBackground()`, `drawPlatforms()`, `drawHazards()`, `drawCollectibles()`, `drawExit()`, `drawPlayer()`, `drawParticles()`, `drawHitFlash()` | reads context, draws canvas |
| `audio.js` | `playSound(name)`, `startMusic(name)`, `stopMusic()`, `getAudioState()` | `audio` |
| `ui.js` | `showScreen(mode)`, `updateHUD()`, `bindScreenEvents()`, `updateSettingsUI()`, `updateLevelSelectUI()` | `mode`, `ui`, DOM |
| `debug.js` | See Debug API | Reads all state; can mutate `input` for tests |

# 3. VISUAL SPEC

The game looks like a bright, silly 8-bit frog platformer. Gribbit is a teal frog with a yellow belly, hopping across blue-purple platforms in a saturated night-pond. The screen is flat side-on, with no scrolling camera. Hazards are red with black spikes or saw teeth, collectibles are bright yellow flies, and the exit is a magenta fly jar. The pixel art is chunky, readable, and always rendered with visible square pixels.

## Lighting and atmosphere

- No dynamic lighting.
- Flat night-pond mood: deep blue sky, bright saturated foreground.
- No glow, no blur, no gradients except optional 2-tone sky bands.
- Contrast is high: dark background, bright foreground shapes.
- Silhouettes must be readable at 1× scale.

## Space

- Playfield: 640×360.
- Ground and walls are solid rectangles.
- Platforms are rectangular stone/lily slabs.
- Background decor is non-colliding pixel art: lily pads, cattails, stars, water ripples.
- All levels fit one screen.

## Palette

The palette is 12 colors and is always colour-blind safe through shape and luminance differences.

| Color name | Hex | Used for |
| --- | --- | --- |
| Sky Dark | `#0e1726` | Background, outlines, UI background |
| Sky Mid | `#1b2a4a` | Background decor |
| Platform Fill | `#3a86ff` | Platforms |
| Platform Edge | `#8ecae6` | Platform highlights |
| Frog Body | `#17c3b2` | Player body |
| Frog Belly | `#ffe66d` | Player belly |
| Hazard Fill | `#ff4040` | Hazards |
| Hazard Edge | `#ffffff` | Hazard outlines and warning marks |
| Collectible | `#ffd60a` | Golden Flies |
| Exit Fill | `#ff006e` | Fly jar |
| Exit Edge | `#ffffff` | Exit highlights |
| UI Text | `#ffffff` | All text |

## Typography

| Item | Rule |
| --- | --- |
| Font | 8×8 bitmap pixel font, uppercase, monospaced |
| CSS | `font-family: "FrogPixel", monospace;` with embedded base64 bitmap font |
| Text size | 16 px on UI screens, 16 px HUD |
| Text color | `#ffffff` |
| Text shadow | 1 px `#0e1726` |
| Accessibility | High contrast, focus outlines, no italic or thin weights |

## Visual recipe table

| Asset | Size | Shape / rule | Animation |
| --- | --- | --- | --- |
| Player idle | 16×16 | Teal frog, yellow belly, white eye dots | Idle bob 1 px, 2 Hz; disabled by reduced motion |
| Player walk | 16×16 | Same silhouette, legs alternate | 6-frame walk cycle, 12 fps |
| Player jump | 16×16 | Legs tucked | Single frame |
| Player fall | 16×16 | Legs extended | Single frame |
| Player hurt | 16×16 | White silhouette over normal sprite | Static for 0.2 s |
| Platform | any 16-px multiple | Blue fill, light top edge, dark outline | Static |
| Reed Spikes | 16×8 or 16×16 | Red spikes with black base, triangular spikes | Static |
| Whirring Saw | 16×16 | Red saw with white teeth | Rotate 12 fps |
| Biting Dragonfly | 16×12 | Red body, white wings, black eyes | Wings flap 16 fps; facing flips |
| Golden Fly | 16×16 | Yellow fly, black eyes | Static; optional bob 4 px 2 Hz; disabled by reduced motion |
| Buzzing Fly Jar | 24×24 | Magenta jar, white glass shine, fly inside | Pulse 1 Hz; static if reduced motion |
| Particles | 2×2 or 4×4 | Squares only | Life 0.25–1.0 s |
| Hit flash | Full player | White outline + white fill | 0.2 s; reduced motion uses static outline only |
| UI buttons | 8×8 pixel border | Rectangles, white text | Focus outline 2 px yellow |

# 4. GAMEPLAY SPEC

The player controls Gribbit the frog from a fixed side-on screen. The only gameplay inputs are left, right, and jump. The player runs, jumps, and lands on solid platforms while avoiding hazards. Touching any hazard restarts the level after a short hit sequence. Touching the Buzzing Fly Jar completes the level. Five levels unlock in order. Golden Flies are optional collectibles added in tier 3 and add score but never block progress.

## Records and rosters

### Player record

| Field | Type | Purpose |
| --- | --- | --- |
| `x`, `y` | float px | Physics position |
| `w`, `h` | int px | Hitbox size 12×14 |
| `vx`, `vy` | float px/s | Velocity |
| `facing` | int | 1 right, -1 left |
| `onGround` | bool | Ground contact |
| `coyoteTimer` | float s | Coyote time |
| `jumpBufferTimer` | float s | Jump buffer |
| `jumpHeld` | bool | Variable jump |
| `alive` | bool | False during hit/restart |
| `animation` | string | `idle`, `walk`, `jump`, `fall`, `hurt` |
| `animationTimer` | float s | Animation timing |

### Level record

| Field | Type | Purpose |
| --- | --- | --- |
| `index` | int | 0–4 |
| `width`, `height` | int px | 640×360 |
| `spawn` | `{x,y}` | Player start |
| `exit` | `{x,y,w,h,active,reached}` | Goal |
| `platforms` | list of `{x,y,w,h}` | Solid collision rectangles |
| `hazards` | list of hazard records | Static and moving hazards |
| `collectibles` | list of collectible records | Tier 3 only |

### Platform record

| Field | Type | Purpose |
| --- | --- | --- |
| `x`, `y`, `w`, `h` | int px | Solid rectangle |

### Hazard roster

| Hazard | Count total | Hitbox | Movement | Behavior |
| --- | ---: | --- | --- | --- |
| Reed Spikes | 20 | 16×8 | Static | Instant fail |
| Whirring Saw | 10 | 14×14 | Ping-pong along path | Instant fail |
| Biting Dragonfly | 6 | 14×12 | Ping-pong horizontal path | Instant fail |

### Hazard record

| Field | Type | Purpose |
| --- | --- | --- |
| `type` | string | `spike`, `saw`, `dragonfly` |
| `x`, `y`, `w`, `h` | float/int px | Position and hitbox |
| `path` | `{x1,y1,x2,y2}` | Movement endpoints |
| `speed` | float px/s | Saw 90, dragonfly 70 |
| `dir` | int | 1 forward, -1 backward |
| `phase` | float | Visual rotation/bob phase |
| `active` | bool | Always true |

### Collectible roster

| Collectible | Count total | Score | Required? |
| --- | ---: | ---: | --- |
| Golden Fly | 30 | 100 | No |

### Collectible record

| Field | Type | Purpose |
| --- | --- | --- |
| `id` | int | Unique within level |
| `x`, `y`, `w`, `h` | int px | 12×12 hitbox |
| `collected` | bool | Prevents double collection |

### Particle record

| Field | Type | Purpose |
| --- | --- | --- |
| `x`, `y` | float px | Position |
| `vx`, `vy` | float px/s | Velocity |
| `life`, `maxLife` | float s | Lifetime |
| `color` | hex | Particle color |
| `size` | int | 2 or 4 px |
| `kind` | string | `jump`, `land`, `collect`, `hit`, `exit` |

### Hit flash record

| Field | Type | Purpose |
| --- | --- | --- |
| `active` | bool | Whether player is in fail sequence |
| `timer` | float s | Countdown to restart |
| `maxTimer` | float s | 0.5 |

### Level content table

| Level | Name | Platforms | Static spikes | Whirring saws | Biting dragonflies | Golden Flies | Target clean time |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | Lily Pad Warmup | 8 | 2 | 0 | 0 | 3 | 35 s |
| 2 | Cattail Climb | 12 | 3 | 1 | 0 | 5 | 55 s |
| 3 | Dragonfly Docks | 16 | 4 | 2 | 1 | 6 | 80 s |
| 4 | Sawblade Bog | 20 | 5 | 3 | 2 | 7 | 110 s |
| 5 | Final Fly Jar | 24 | 6 | 4 | 3 | 9 | 160 s |

Target clean total: 440 s = 7 min 20 s. With restarts, still under 30 minutes.

## 4.1 Session and level progression `[T1 core one level, T2 full sequence]`

| Rule | Number |
| --- | ---: |
| Initial unlocked level | 0 |
| Level count | 5 |
| Completing level | Unlocks `currentLevelIndex + 1` |
| Completing level 4 | Sets `unlockedLevel = 4`, all levels replayable |
| Level select | Shows levels 0–4; locked levels are disabled |
| Starting selected level | Resets `session.score = 0` |
| Level load | Sets `scoreAtLevelStart = session.score` |
| Level restart | Sets `session.score = scoreAtLevelStart` |
| Win | Only after completing level index 4 |

## 4.2 Platforming `[T1]`

| Rule | Number |
| --- | ---: |
| Named inputs | `left`, `right`, `jump` |
| Horizontal input sets acceleration | Ground 1200, air 900 |
| Max horizontal speed | 160 |
| Facing updates with horizontal velocity | 1 or -1 |
| Jump input sets jump buffer | 0.12 s |
| Ground jump allowed if `onGround` or `coyoteTimer > 0` | - |
| Jump velocity | -320 |
| Coyote time | 0.10 s |
| Jump cut on release | If `vy < -120`, set `vy = -120` |
| Landing | Sets `onGround = true`, zeroes `vy`, clears coyote |
| No double jump | - |
| No wall jump | - |
| No one-way platforms | - |

## 4.3 Physics `[T1]`

| Rule | Number |
| --- | ---: |
| Gravity | 900 px/s² |
| Falling multiplier | 1.35 when `vy > 0` |
| Terminal fall speed | 520 px/s |
| Friction | Ground 1600, air 300 |
| Collision method | AABB, axis-separated |
| x collision | Clamp x, set `vx = 0` |
| y collision | Clamp y, set `vy = 0`, set `onGround` if bottom collision |
| Fixed step | 1/60 s |
| No slopes | - |
| No momentum puzzles | - |

## 4.4 Hazards `[T1]`

| Rule | Number |
| --- | ---: |
| Hazard update after player collision | - |
| Player/hazard collision | AABB |
| Hazard contact result | `player.alive = false`, hit flash, particles, sound |
| Hit sequence duration | 0.5 s |
| During hit sequence | Player physics disabled, input disabled, level entities update for visual only |
| After hit sequence | `resetLevel()` |
| Restart preserves score | `session.score = scoreAtLevelStart` |
| Static spike speed | 0 |
| Whirring saw speed | 90 px/s |
| Saw movement | Ping-pong between path endpoints |
| Biting dragonfly speed | 70 px/s |
| Dragonfly movement | Horizontal ping-pong, optional visual bob 3 px 2 Hz |
| Dragonfly endpoint pause | 0.4 s |
| Hazards cannot be destroyed | - |
| Hazards do not damage | They fail the level instantly |

## 4.5 Score `[T1 base, T3 collectibles]`

| Rule | Number |
| --- | ---: |
| Level clear score | +500 |
| Golden Fly score | +100 |
| Max collectibles | 30 |
| Max score | 6000 |
| HUD visible | During playing and paused |
| Win screen shows score | Yes |
| Level restart | Restores score to `scoreAtLevelStart` |
| Starting new level from level select | Score resets to 0 |
| No time bonus | - |

## 4.6 Collectibles `[T3]`

| Rule | Number |
| --- | ---: |
| Named input | Movement only; no separate collect input |
| Collectible hitbox | 12×12 |
| Collision | AABB |
| Collection effect | `collected = true`, score +100, particles, sound |
| Reset | On level restart, all `collected = false` |
| Required for exit | No |
| Bob animation | 4 px vertical, 2 Hz |
| Reduced motion | No bob, static sprite |

## 4.7 Effects `[T1]`

| Effect | Trigger | Numbers |
| --- | --- | ---: |
| Jump dust | Player leaves ground via jump | 4 particles, life 0.25 s, speed 40 px/s |
| Land dust | Player lands with `vy > 180` | 6 particles, life 0.35 s, speed 55 px/s |
| Collect sparkle | Golden Fly collected | 10 particles, yellow, life 0.5 s, outward speed 80 px/s |
| Hit burst | Hazard contact | 20 particles, red/white, life 0.6 s, outward speed 120 px/s |
| Exit sparkle | Exit reached | 40 particles, magenta/yellow, life 1.0 s, outward speed 100 px/s |
| Hit flash | Hazard contact | Player white for 0.2 s, fail sequence 0.5 s |
| Level transition | Exit reached | Fade-like 3-frame pixel wipe, 0.75 s |
| Reduced motion | Setting | Particle count 0, no bob, no squash, no screen flash |

## 4.8 Accessibility `[T2]`

| Rule | Number |
| --- | ---: |
| Colour-blind safe palette | Always enabled |
| Reduced motion default | False |
| Reduced motion effect | No particles, no bobbing, no squash, no screen flashes |
| Remappable actions | left, right, jump, pause |
| Remap conflict | New key clears previous action using that key |
| UI navigation | Arrow keys, Enter, Escape |
| Focus outline | 2 px `#ffd60a` |

## Progression and difficulty

| Level | Teaches | Difficulty |
| ---: | --- | --- |
| 1 | Jump height, landing, basic hazard avoidance | Very easy |
| 2 | Moving hazard timing | Easy |
| 3 | Moving enemy avoidance, longer jumps | Medium |
| 4 | Saw + dragonfly combinations | Medium-hard |
| 5 | Precision platforming with all hazard types | Hard, but no new mechanics |

## Feel

- Starting a jump should feel immediate: jump buffer and coyote time.
- Short jumps should feel controllable: jump cut.
- Falling should be faster than rising: falling multiplier.
- Landing should feel solid: dust, squash, bleep.
- Hitting hazards should feel silly but clear: white flash, burst, instant restart.
- Collecting flies should feel rewarding but not essential: sparkle, bleep, score.

# 5. CHARACTERS

## Gribbit the frog

| Property | Rule |
| --- | --- |
| Silhouette | Round teal frog, yellow belly, big white eyes |
| Sprite size | 16×16 |
| Hitbox | 12×14, offset `(2, 2)` |
| Facing | Mirrors horizontally |
| States required by gameplay | `idle`, `walk`, `jump`, `fall`, `hurt`, `alive`, `dead` |

### Animations

| Animation | Frames | Rate | Motion rule |
| --- | ---: | ---: | --- |
| `idle` | 4 | 8 fps | 1 px vertical bob |
| `walk` | 6 | 12 fps | Alternate legs, 1 px body bob |
| `jump` | 1 | 0 fps | Legs tucked, body stretched 1 px |
| `fall` | 1 | 0 fps | Legs extended |
| `hurt` | 1 | 0 fps | White silhouette |
| `land_squash` | 3 | 30 fps | 0.1 s squash; disabled by reduced motion |

## Biting Dragonfly

| Property | Rule |
| --- | --- |
| Silhouette | Red dragonfly, white wings, black eyes |
| Sprite size | 16×12 |
| Hitbox | 14×12 |
| Facing | Mirrors based on movement direction |
| States | `alive`, `dead` not used; only `active` |

### Animations

| Animation | Frames | Rate | Motion rule |
| --- | ---: | ---: | --- |
| `fly` | 2 | 16 fps | Wing up/down |
| `bob` | - | 2 Hz | 3 px vertical visual offset; disabled by reduced motion |

## Whirring Saw

| Property | Rule |
| --- | --- |
| Silhouette | Red circular saw with white teeth |
| Sprite size | 16×16 |
| Hitbox | 14×14 |
| States | `active` |

### Animations

| Animation | Frames | Rate | Motion rule |
| --- | ---: | ---: | --- |
| `spin` | 8 | 12 fps | Rotate around center |

## Golden Fly

| Property | Rule |
| --- | --- |
| Silhouette | Yellow fly, black eyes |
| Sprite size | 16×16 |
| Hitbox | 12×12 |
| States | `uncollected`, `collected` |

### Animations

| Animation | Frames | Rate | Motion rule |
| --- | ---: | ---: | --- |
| `static` | 1 | 0 fps | Default |
| `bob` | - | 2 Hz | 4 px vertical offset; tier 3; disabled by reduced motion |

## Buzzing Fly Jar

| Property | Rule |
| --- | --- |
| Silhouette | Magenta jar with fly inside |
| Sprite size | 24×24 |
| Hitbox | 24×24 |
| States | `active`, `reached` |

### Animations

| Animation | Frames | Rate | Motion rule |
| --- | ---: | ---: | --- |
| `idle` | 1 | 0 fps | Default |
| `pulse` | 2 | 1 Hz | 1 px brightness/outline pulse; disabled by reduced motion |

# 6. AUDIO

All audio is synthesized at runtime. No audio files. Music and effects use square, triangle, saw, and noise-style bleeps.

| Sound name | Recipe | When it plays |
| --- | --- | --- |
| `music_title` | 100 BPM. Square lead: C5, E5, G5, A5, G5, E5. Triangle bass: C3, G3. Noise hat every 0.5 s. | Title screen |
| `music_level` | 130 BPM. Square arpeggio: A3, C4, E4, A4. Triangle bass: A2, E2. Noise kick/snare pattern. | Level playing |
| `music_win` | 120 BPM. Square fanfare: C5, E5, G5, C6. Triangle bass: C3. Noise cymbal at end. | Win screen |
| `music_none` | Silence | Pause, settings, level select, hit sequence |
| `sfx_jump` | Square, 300 Hz → 600 Hz, 0.08 s, volume 0.28 | Player jumps |
| `sfx_land` | Triangle, 120 Hz → 80 Hz, 0.05 s, volume 0.22 | Player lands |
| `sfx_collect` | Square two notes: 880 Hz 0.04 s, 1320 Hz 0.06 s, volume 0.3 | Golden Fly collected |
| `sfx_hit` | Saw/noise mix, 220 Hz → 60 Hz, 0.30 s, volume 0.35 | Hazard contact |
| `sfx_exit` | Square arpeggio: 523, 659, 784, 1046 Hz, 0.10 s each, volume 0.35 | Exit reached |
| `sfx_ui_move` | Square, 660 Hz, 0.04 s, volume 0.18 | UI focus change |
| `sfx_ui_confirm` | Square, 880 Hz, 0.06 s, volume 0.22 | UI select |
| `sfx_ui_back` | Square, 440 Hz, 0.06 s, volume 0.18 | UI back |
| `sfx_pause` | Square, 523 Hz, 0.08 s, volume 0.2 | Pause opened |
| `sfx_resume` | Square, 784 Hz, 0.08 s, volume 0.2 | Resume |
| `sfx_restart` | Square, 330 Hz, 0.08 s, volume 0.2 | Manual restart from pause |

# 7. UX

All screens are HTML/CSS DOM overlays. The game canvas is only the playfield. The state machine is data-driven.

## Screen state machine

| Screen ID | Entry condition | Visible controls | Actions |
| --- | --- | --- | --- |
| `title` | Initial load | Start, Settings | Start → `level_select`; Settings → `settings` |
| `level_select` | From title or pause quit | Enabled level buttons, Back | Select unlocked level → `playing`; Back → `title` |
| `playing` | Level started | None | Pause key → `paused`; Exit → next level or `win`; Hazard → restart same `playing` |
| `paused` | Pause from `playing` | Resume, Settings, Restart Level, Quit to Level Select | Resume → `playing`; Settings → `settings`; Restart → `playing`; Quit → `level_select` |
| `settings` | From title or paused | Reduced motion toggle, key remap list, Back | Back → previous screen |
| `win` | Level 5 completed | Play Again, Back to Title | Play Again → `level_select`; Back → `title` |

## UI keyboard controls

| Control | Default |
| --- | --- |
| Move focus | Arrow keys |
| Select | Enter |
| Back | Escape |
| Toggle checkbox | Enter or Space |
| Remap key | Enter on action, press new key, Escape cancels |

## HUD

| Element | Record field | When visible |
| --- | --- | --- |
| `#hud-score` | `session.score` | `playing`, `paused` |
| `#hud-score` | hidden | `title`, `level_select`, `settings`, `win` except win screen shows final score separately |

## Accessibility UI

| Requirement | Implementation |
| --- | --- |
| Colour-blind safe palette | CSS variables use the Visual Spec palette |
| Reduced motion | Body class `.reduced-motion` disables CSS animations and game particles |
| Remappable keys | Settings list for `left`, `right`, `jump`, `pause` |
| Focus visibility | 2 px yellow outline on focused elements |
| Text size | Minimum 16 px pixel font |
| No color-only state | Locked levels show `LOCK`; enabled levels show number; settings show text state |

# 8. DEBUG API

All debug functions return plain serializable objects.

| Function | Returns / behavior |
| --- | --- |
| `debug.getPlatformingState()` | Player position, velocity, facing, animation, `onGround`, coyote, jump buffer, jump held |
| `debug.getPhysicsState()` | Player velocity, gravity applied, terminal velocity, collision helpers |
| `debug.getHazardState()` | Array of hazard type, position, path, speed, direction, active |
| `debug.getCollectibleState()` | Array of collectible id, position, collected |
| `debug.getLevelState()` | Current level index, unlocked level, spawn, exit, platform count, hazard count, collectible count |
| `debug.getScoreState()` | Score, score at level start, max score |
| `debug.getEffectState()` | Particle count, particle array, hit flash state, level transition state |
| `debug.getInputState()` | Current action down/pressed states |
| `debug.isDown(action)` | Boolean for named action |
| `debug.isPressed(action)` | Boolean for named action edge |
| `debug.setInput(action, bool)` | Sets simulated input state for tests |
| `debug.setPlayerState(partial)` | Applies allowed player fields for tests |
| `debug.setMode(mode)` | Forces mode for UI tests |
| `debug.getSettingsState()` | Settings and key map |

# 9. TESTS

## Tier 1 tests

| Test | Assertion |
| --- | --- |
| `T1-fixed-step` | Game uses 1/60 s fixed steps and caps accumulator at 0.25 s |
| `T1-no-random-gameplay` | No gameplay code calls `Math.random()` |
| `T1-jump-height` | Full jump raises player by 50–62 px |
| `T1-min-jump-height` | Jump cut raises player by 6–14 px |
| `T1-coyote-jump` | Pressing jump within 0.10 s after leaving ground jumps |
| `T1-jump-buffer` | Pressing jump within 0.12 s before landing jumps |
| `T1-collision-no-clip` | Player cannot pass through platform rectangles |
| `T1-hazard-fail` | AABB overlap with hazard sets `player.alive = false` and starts hit flash |
| `T1-hazard-restart` | After 0.5 s, level resets player to spawn and hazards to initial positions |
| `T1-exit-complete` | AABB overlap with exit starts level transition and completes level |
| `T1-score-level-clear` | Completing level adds 500 score |
| `T1-hud-score-visible` | HUD element shows current score while playing |
| `T1-pixel-art-render` | Canvas uses integer scaling and pixelated rendering |
| `T1-audio-synthesized` | `audio.js` generates sounds without external files |
| `T1-pause-freezes` | Paused mode does not update player, hazards, effects, or score |

## Tier 2 tests

| Test | Assertion |
| --- | --- |
| `T2-level-count` | `levels.getLevelCount()` returns 5 |
| `T2-level-contents` | Each level has the platform/hazard counts in the Level Content table |
| `T2-unlock-progress` | Completing level n unlocks n+1 |
| `T2-level-select-locked` | Locked level buttons are disabled |
| `T2-level-select-start` | Starting a level resets score to 0 |
| `T2-win-after-final` | Completing level index 4 enters `win` |
| `T2-settings-screen` | Settings screen exists and can be opened from title and pause |
| `T2-remap-keys` | Remapping `jump` to a new key makes that key trigger jump |
| `T2-remap-conflict` | Remapping an action to a key used by another action clears the old action’s key |
| `T2-reduced-motion` | Enabling reduced motion disables particle spawning and bob animations |
| `T2-pause-menu` | Pause menu has Resume, Settings, Restart Level, Quit to Level Select |
| `T2-restart-level` | Manual restart resets current level and preserves score at level start |
| `T2-accessible-palette` | Palette constants match Visual Spec palette |

## Tier 3 tests

| Test | Assertion |
| --- | --- |
| `T3-collectible-counts` | Levels contain 3, 5, 6, 7, 9 Golden Flies respectively |
| `T3-collect-score` | Collecting a Golden Fly adds 100 score |
| `T3-collect-once` | A collected Golden Fly does not add score again |
| `T3-collect-reset` | Restarting level resets all collectibles to uncollected |
| `T3-collect-not-required` | Level can complete with zero collectibles collected |
| `T3-collect-hud` | HUD score updates immediately after collection |
| `T3-collect-sound` | Collection calls `playSound("sfx_collect")` |
| `T3-collect-particles` | Collection spawns 10 particles unless reduced motion is enabled |

# 10. BUILD ORDER

1. Create browser shell: `index.html`, canvas, DOM screen containers, CSS variables, pixel font.
2. Implement fixed-step loop and global context.
3. Implement input default key map and input edge detection.
4. Implement player physics: gravity, velocity, terminal speed.
5. Implement AABB platform collision and platforming controls.
6. Implement one level with platforms, spawn, and exit.
7. Implement static hazards and hazard collision fail.
8. Implement hit flash, hit particles, and automatic level restart.
9. Implement exit completion, level transition, and win for one level.
10. Implement score for level clear and HUD.
11. Implement pixel art rendering for player, platforms, hazards, exit, particles.
12. Implement synthesized bleeps and chiptune music.
13. Implement title, basic pause, and one-level win screens.
14. Add levels 2–5 with required platform and hazard counts.
15. Implement level select and unlock progression.
16. Implement settings screen, reduced motion, and remappable keys.
17. Add Golden Fly collectibles and score.
18. Add collectible particles and sound.
19. Run tier tests and fix failures.

# 11. DEFINITION OF DONE

## Tier 1 done

**High level:** A player can start the game, play one complete frog platforming level, fail on hazards, restart, reach the exit, and see the game presented in the required pixel/chiptune style with HUD score and effects.

- [ ] One complete level exists in level data.
- [ ] Player can move left/right with named input.
- [ ] Player can jump with named input.
- [ ] Gravity, velocity, and terminal velocity behave per numbers.
- [ ] Coyote time and jump buffer work.
- [ ] Variable jump height works.
- [ ] Player collides with all platforms without clipping.
- [ ] Static hazards cause instant level failure.
- [ ] One moving hazard causes instant level failure.
- [ ] Hazard contact triggers hit flash and particles.
- [ ] Level restarts automatically after 0.5 s.
- [ ] Exit completes the level.
- [ ] Score increases by 500 on level clear.
- [ ] HUD shows score while playing.
- [ ] Canvas renders pixel art with integer scaling.
- [ ] Player, platforms, hazards, and exit are drawn.
- [ ] Jump, land, hit, and exit sounds play.
- [ ] Title screen starts play.
- [ ] Pause key pauses and resumes.
- [ ] Win screen appears after completing the one-level sequence.
- [ ] Tier 1 tests pass.

## Tier 2 done

**High level:** The game has the required sequence of levels, level select, full pause, settings, accessibility, and win flow.

- [ ] Five levels exist.
- [ ] Level content counts match the Level Content table.
- [ ] Levels unlock in order.
- [ ] Level select shows locked and unlocked levels.
- [ ] Selecting an unlocked level starts that level.
- [ ] Completing level 5 enters win screen.
- [ ] Win screen shows final score.
- [ ] Pause menu has Resume, Settings, Restart Level, Quit to Level Select.
- [ ] Manual restart resets current level and preserves score at level start.
- [ ] Settings screen exists.
- [ ] Reduced motion setting disables particles, bobbing, squash, and screen flashes.
- [ ] Remappable keys setting changes gameplay input.
- [ ] Key remap conflicts are handled.
- [ ] UI is keyboard accessible.
- [ ] Tier 2 tests pass.

## Tier 3 done

**High level:** Optional Golden Fly collectibles exist, add score, reset correctly, and are fully optional.

- [ ] Each level contains the required Golden Fly count.
- [ ] Golden Flies are visible on screen.
- [ ] Collecting a Golden Fly adds 100 score.
- [ ] Collection plays sound and spawns particles unless reduced motion.
- [ ] Collected flies do not re-add score.
- [ ] Restarting a level resets collectibles.
- [ ] Levels can be completed without collecting any fly.
- [ ] HUD updates immediately on collection.
- [ ] Tier 3 tests pass.

# A. SANITY

| Check | Result |
| --- | --- |
| Does the spec only use the requested systems? | Yes. Added only platforming, physics, hazards, collectibles, score, effects, screens, settings. No combat, health, lives, checkpoints, timers, power-ups, inventory, save, or camera scrolling. |
| Are core mechanics tier 1? | Yes. Platforming, physics, and hazards are tier 1. |
| Are supporting mechanics tier 2? | No supporting mechanics exist. Tier 2 is required content and UI completion, not a mechanic. |
| Are extra mechanics tier 3? | Yes. Golden Fly collectibles are tier 3 only. |
| Is collectible required for completion? | No. Tier 3 tests explicitly verify optional completion. |
| Is failure restart the level? | Yes. Hazard contact triggers automatic restart after 0.5 s. |
| Is win reach the exit? | Yes. Exit completes level; level 5 exit opens win screen. |
| Are screens title, pause, settings, win, level select present? | Yes. State machine and UI sections define all five. |
| Is HUD only score? | Yes. HUD table contains only score. |
| Are effects particles and hit flash present? | Yes. Effect records, spawn rules, and render rules define them. |
| Are accessibility settings present? | Yes. Colour-blind safe palette is always on; reduced motion and remappable keys are settings. |
| Are concrete player, enemies, traps, pickups, and numbers defined? | Yes. Gribbit, Biting Dragonfly, Reed Spikes, Whirring Saw, Golden Flies, counts, scores, hitboxes, and level contents are specified. |
| Are numbers present for every system? | Yes. Movement, physics, hazards, collectibles, score, particles, and level counts have numbers. |
| Are inputs named? | Yes. `left`, `right`, `jump`, `pause`, and UI controls are named. |
| Are art, palette, typography, music, and SFX included from tier 1? | Yes. Tier 1 definition of done includes pixel art, palette, pixel font, HUD, particles, hit flash, music, and bleeps. |
| Are modules and global context sufficient for gameplay records? | Yes. Global context contains all record fields; module specifics list required functions. |
| Are tests tied to tiers? | Yes. Tier 1, 2, 3 tests correspond to tier definitions. |
| Are there external assets? | No. Audio and font are synthesized/embedded; no external asset requirement. |
| Is the session under 30 minutes? | Yes. Target clean time is 7 min 20 s; retries are expected but still bounded for a small game. |
| Did any conflict require fixing? | Yes. The prompt asks for enemies while core mechanics only list hazards. Fixed by defining enemies as moving hazards: Biting Dragonfly. |
| Did any other conflict require fixing? | Yes. HUD score is required while collectibles are tier 3. Fixed by defining score from level clear in tier 1 and collectible score in tier 3. |