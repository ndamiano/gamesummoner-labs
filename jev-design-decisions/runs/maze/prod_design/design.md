# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Make a browser game about solving mazes | Sections 0, 4, 7, 10 |
| Playable in a browser with no build step or external libraries | Sections 1, 2, 10 |
| 2D top-down maze solving | Sections 3, 4.1, 4.2 |
| Grid-based cell movement | Sections 4.2, 8 |
| Limited visibility around the player | Sections 4.3, 5, 8 |
| Fading trail as the only memory system | Sections 4.3, 5, 8 |
| 12-level campaign | Sections 4.5, 7, 9 |
| Optional orbs that unlock the exit | Sections 4.4, 5, 8 |
| No fail state | Sections 4.5, 7, 11 |
| Stars based on time | Sections 4.5, 7, 8, 9 |
| Save completed levels, stars, best times, settings | Sections 4.6, 7, 8, 9 |
| Keyboard, gamepad, and touch input | Sections 4.2, 7, 8, 9 |
| Accessibility: colorblind mode, reduced motion, text size | Sections 3, 4.7, 7, 9 |
| Deterministic level generation | Sections 4.1, 8, 9 |
| No minimap, exit arrow, persistent memory map, or fail state | Sections 0.2, 4.3, 4.5, 11 |
| HUD and screens are HTML/CSS UI | Sections 7, 10 |
| Debug API for headless testing | Sections 8, 9, 11 |

## 0.2 Decisions

| Topic | Gameplay | Visual | Engineering | Ruling / Reasoning |
| --- | --- | --- | --- | --- |
| Authoritative 3-star times | Level table plus rule: 3-star time is `70%` of par, rounded down to the nearest second. Some table values do not exactly match the formula. | Silent. | Use explicit `threeStarMs` values from the level table; formula only if missing. | The level table is authoritative. The formula is only a fallback for future levels that omit `threeStarMs`. This preserves designer-authored star thresholds and keeps tests stable. |
| Fallback mazes | One hand-designed fallback layout per level. | Silent. | Deterministic fallback builder replaces hand-designed data. | Use the deterministic fallback builder. Hand-designed maze data is dropped because it is brittle, hard to maintain, and unnecessary when a deterministic builder can satisfy the same constraints. |
| Entity shapes | Requires clear distinction between player, orb, exit, trail, walls, fog, locked/unlocked exit. | Player: rounded diamond. Orb: circle with ring. Exit: square frame. Locked exit: square frame with bars. Unlocked exit: square frame with open circle. | Player: circle with directional notch. Orb: diamond. Exit: square. | Use the visual designer’s shape language. Engineering’s shape names are superseded. The visual shapes better match the quiet, readable identity and still satisfy gameplay’s accessibility requirement. |
| Audio implementation | Lists required sound events. | Provides synthesized WebAudio SFX recipes and optional music. | Expects optional `.wav` files; audio must be non-essential. | Use synthesized WebAudio by default. Optional `.wav` files are dropped. The game must not require external audio assets and must not crash if audio is unavailable. |
| Input setting | Settings list includes Input: Keyboard / Gamepad / Touch. | Settings Input row is informational only and must not disable input methods. | Save includes `settings.input`, used as a tie-breaker. | All supported inputs are always active. The user-facing Settings screen shows an informational Input row only. `settings.input` remains an internal debug/tie-breaker value with default `"auto"`, not a user-facing toggle. |
| Volume settings | Silent. | Adds master, music, and SFX volume sliders. | Cuts an audio mute setting. | Include master, music, and SFX volume sliders. Master volume at `0` effectively mutes audio. No separate mute setting is required. Volume settings do not affect stars or gameplay timing. |
| Maze rendering | Requires readable top-down maze. | Uses canvas-like presentation, fog, light, and shapes. | Uses one `<canvas>` for maze rendering and DOM for HUD. | The maze viewport is a `<canvas>`. All screens, HUD, toasts, buttons, and menus are HTML/CSS/DOM. The canvas is a presentation surface, not an interactive UI control. |
| Level 12 completion | Game complete screen appears after completing Level 12. | Level 12 goes directly to Game Complete; Game Complete shows final level stats. | Levels 1-11 use `levelComplete`; Level 12 uses `gameComplete`. | Level 12 goes directly to `gameComplete`. The Game Complete screen includes the final level’s name, stars, time, best time, and total stars. |
| Camera smoothing | Camera follows and centers on player, clamped to maze bounds. | 100 ms camera lerp; reduced motion snaps. | Reduced motion disables camera easing. | Tier 1 uses direct clamped camera. Tier 2 adds 100 ms camera lerp. Reduced motion always snaps directly to the player. |
| Trail memory brightness | Trail tiles remain visible outside light radius. | Trail-only tiles render dimmer than current light tiles. | Silent. | Include trail memory brightness as presentation only. It does not change gameplay visibility rules. |
| Star reveal and audio | Stars are optional performance goals. | Star animation: first star at 200 ms, second at 600 ms, third at 1000 ms; reduced motion fades. | Plays `"star"` once per new star earned. | Level Complete animates the earned stars using the visual timings. Audio plays one `"star"` sound for each newly earned star above the previously saved star count. Reduced motion shows stars statically or with simple fade. |
| Act accents and music | Levels progress through acts implicitly by level number. | Adds act accent colors, in-game tints, and ambient music. | Audio is non-essential. | Act accents, title/level-select background maze lines, star pop animation, and generative music are Tier 3 presentation polish. They must not affect gameplay, stars, visibility, or timing. |
| Optional SVG snippets | Silent. | Provides optional SVG asset snippets. | Silent. | The normative visual recipe table supersedes the optional SVG snippets. The SVG snippets are dropped as redundant once shape, size, color, and geometry are specified. |

### Dropped source details

| Dropped item | Source | Reason |
| --- | --- | --- |
| Hand-designed fallback maze data | Gameplay | Replaced by deterministic fallback builder. |
| Optional `.wav` audio files | Engineering | Replaced by synthesized WebAudio. |
| Engineering shape names: player circle, orb diamond | Engineering | Superseded by visual shape language. |
| User-facing input method toggle | Gameplay/Engineering | Superseded by informational input row; all inputs remain active. |
| Separate audio mute setting | Engineering | Master volume at `0` is sufficient. |
| Best time display in level select | Visual cut list | Stars are enough for level select; best time remains in HUD and complete screens. |
| Act labels in level select | Visual cut list | Accent colors and node progression are enough. |
| Animated fog | Visual cut list | Static fog is calmer and does not imply hidden movement. |
| Screen shake | Visual cut list | No fail state or combat; shake would feel punitive. |
| Complex wall textures | Visual cut list | Walls must remain instantly readable. |
| Per-level entity colors | Visual cut list | Core entity colors must remain constant for readability. |
| Mouse-only interactions | Visual cut list | Keyboard, gamepad, and touch must all work. |
| Audio-only cues | Visual cut list | Every gameplay-critical event must have a visual cue. |
| Narrative art/story | Visual cut list | The maze and fading trail are the core experience. |
| Moving environmental particles | Visual cut list | Particles can distract from memory and readability. |
| Enemies, traps, moving walls, health, lives | Gameplay cut list | They distract from maze solving and memory. |
| Minimap, arrow to exit, persistent memory map | Gameplay cut list | They undermine the fading-trail memory mechanic. |
| Keys and doors | Gameplay cut list | Orbs are simpler and avoid dependency problems. |
| Fail state | Gameplay cut list | Maze solving is already challenging; restart is enough. |
| Upgrades | Gameplay cut list | Upgrades would make star times unfair. |
| Endless mode | Gameplay cut list | The game is a focused 12-level campaign. |
| Narrative | Gameplay cut list | A short puzzle game does not need story. |
| Mid-level save | Gameplay/Engineering | Levels are short; restarting is simple and fair. |
| Gameplay-affecting difficulty settings | Gameplay/Engineering | Changing light radius or trail lifetime would make stars unfair. |
| High-DPI-specific gameplay logic | Engineering | High-DPI affects rendering only, not gameplay rules. |
| Procedural narrative | Engineering | Out of scope. |

## 0.3 Tiers

| Tier | Name | Included systems | Purpose |
| --- | --- | --- | --- |
| Tier 1 | Core playable campaign | Level table, deterministic generation, fallback builder, movement, visibility, trail, objective, timer, stars, save, title, level select, gameplay, pause, level complete, game complete, basic canvas rendering, basic HUD, toasts, tutorial hints, keyboard/gamepad/touch input, no fail state | Minimal viable game: a complete, playable 12-level maze campaign. |
| Tier 2 | Full visual and accessibility spec | Full palettes, colorblind mode, reduced motion, text size, synthesized SFX, volume settings, toasts styling, level select node states, settings persistence, trail memory brightness, camera lerp, focus states, accessible shapes | Makes the game match the full visual/accessibility design. |
| Tier 3 | Presentation polish | Act accent colors, in-game act tints, title/level-select background maze lines, star pop animation, generative ambient music, optional decorative flourishes | Improves atmosphere without changing gameplay or fairness. |

Tier 1 is guaranteed to build. Tier 2 and Tier 3 may be left unbuilt only if they do not break Tier 1 behavior.

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Quantity | Value | Notes |
| --- | ---: | --- |
| Logical tile unit | `1` | One maze cell is 1 tile. |
| X axis | Right | Cell coordinates increase to the right. |
| Y axis | Down | Cell coordinates increase downward. |
| Cell center | `(x + 0.5, y + 0.5)` | Used for Euclidean distance checks. |
| Time unit | milliseconds | All gameplay timers use ms. |
| Fixed logic step | `1 ms` | Logic advances in 1 ms steps. `tick(ms)` calls the update path `ms` times. |
| Move time per tile | `140 ms` | One completed tile move. |
| Movement speed | `~7.1 tiles/sec` | Derived from `1000 / 140`. |
| Light radius | `2.5` tiles | Euclidean distance from player cell center to tile center. |
| Light radius squared | `6.25` | Used for distance checks. |
| Trail lifetime | `10000 ms` | 10 seconds. |
| Trail fade duration | `2000 ms` | Fade from `8000 ms` to `10000 ms`. |
| Toast duration | `1500 ms` | One toast at a time. |
| Viewport tiles | `15 x 15` | Reference visible area. |
| Max straight corridor | `8` tiles | Validation fails if exceeded. |
| Generation attempts | `10` | Normal generation attempts before fallback. |
| Total levels | `12` | Fixed campaign. |
| Total stars | `36` | 12 levels x 3 stars. |
| Canvas tile size | `cssSize / 15` | `cssSize = min(containerWidth, containerHeight)`. |
| Device pixel ratio | `dpr` | Canvas backing store scaled by `dpr`. |
| Player visual size | `0.6` tile | Rounded diamond. |
| Orb visual size | `0.4` tile | Circle with ring. |
| Exit visual size | `0.8` tile | Square frame. |
| Trail marker size | `0.18` to `0.22` tile | Small rounded oval/dot. |
| Interior wall thickness | `0.14` tile | Rounded line segment. |
| Boundary wall thickness | `0.18` tile | Slightly thicker than interior walls. |
| Camera lerp | `100 ms` | Tier 2 only; reduced motion snaps. |
| Level fade in/out | `400 ms` | Presentation only. |
| Toast fade in/out | `200 ms` | Presentation only. |
| Star reveal times | `200 ms`, `600 ms`, `1000 ms` | For first, second, third earned star. |
| Orb idle pulse | `1200 ms` | Scale `1.00` to `1.08`. |
| Orb collect animation | `300 ms` | Scale to `0` plus particles. |
| Exit unlocked pulse | `1500 ms` | Scale `1.00` to `1.06`. |
| Exit unlock ring | `400 ms` | Expanding ring, alpha `0.4`. |
| Locked exit flash | `150 ms` | Alpha `0.8` to `1.0`. |
| Player move animation | `140 ms` | Scale `1.06`, tilt `4` degrees, Tier 2. |
| Player light flicker | `±2%` over `1500 ms` | Tier 2; disabled by reduced motion. |
| Input priority tie-break | `keyboard`, `gamepad`, `touch` | Used only if input timestamps tie. |
| Gamepad stick threshold | `0.5` | Left stick movement. |
| Touch swipe threshold | `24` pixels | Direction is larger axis. |

## 1.2 Important conventions

- Vanilla HTML, CSS, and JavaScript only. No Node, npm, bundler, framework, test runner, or external library.
- All game code attaches to `window.FL`.
- Debug API is exposed as `window.__game`.
- No `Math.random()` in gameplay, generation, save, star, level, trail, visibility, or movement logic.
- Use `FL.rng.mulberry32` for all deterministic randomness.
- Level seed: `1000 + levelId`.
- Attempt seed: `FL.rng.attemptSeed(levelId, attempt)`.
- Fallback seed: `FL.rng.fallbackSeed(levelId)`.
- Logic is time-driven by `update(1)` or `tick(ms)`. Real time APIs must not directly mutate gameplay state.
- In normal play, `requestAnimationFrame` supplies delta time to an accumulator; the accumulator calls fixed 1 ms logic steps.
- In tests, `window.__game.tick(ms)` advances exactly `ms` logic milliseconds.
- State returned by `getState()` must be JSON-safe.
- Internal maze walls may be `Uint8Array`, but `getState()` must expose them as a normal array.
- Logical visibility uses the player’s current grid cell, not interpolated visual position.
- Rendering may use interpolated positions for presentation, but rules use logical cells.
- No persistent seen-map. The only memory system is the fading trail.
- All gameplay-critical events must have a visual cue. Audio is never required.
- Accessibility settings must not change maze layout, light radius, trail lifetime, star times, or level generation.
- No mouse-only interaction. Keyboard, gamepad, and touch must all work.
- Save occurs after level complete, settings change, and hint flag change. No mid-level save.
- There is no fail state.
- Toasts do not block movement.
- One toast may be active at a time.
- Orbs are sorted by `y`, then `x` in final maze state.
- Trail is sorted by `y`, then `x`.
- Visible tiles are sorted by `y`, then `x`.
- Event log and audio log are for debugging and testing; they must not affect gameplay.

# 2. CONTRACTS

## 2.1 Module layout

| File | Responsibility | Tier |
| --- | --- | ---: |
| `index.html` | Loads CSS and JS, defines screen sections, canvas, HUD, toast. | 1 |
| `test.html` | Loads same files plus `js/tests.js`, sets `window.__runTests = true`. | 1 |
| `css/styles.css` | All UI styling, CSS variables, palettes, accessibility classes. | 1 |
| `js/config.js` | `FL.config` constants. | 1 |
| `js/rng.js` | `FL.rng` deterministic PRNG and seed helpers. | 1 |
| `js/levels.js` | `FL.levels` level table and helpers. | 1 |
| `js/maze.js` | `FL.maze` maze representation, generation, validation, BFS, fallback. | 1 |
| `js/save.js` | `FL.save` persistence, normalization, unlock rules. | 1 |
| `js/audio.js` | `FL.audio` synthesized audio manager. | 2 |
| `js/input.js` | `FL.input` keyboard, gamepad, touch input. | 1 |
| `js/render.js` | `FL.render` canvas maze rendering. | 1 |
| `js/game.js` | `FL.game` runtime state and update logic. | 1 |
| `js/ui.js` | `FL.ui` DOM screens, HUD, toasts, hints, settings. | 1 |
| `js/debug.js` | `window.__game` debug API. | 1 |
| `js/tests.js` | Test harness and required tests. | 1 |

Dropped: optional `audio/*.wav` files.

## 2.2 Global context

```js
window.FL = {
  config: {},
  rng: {},
  levels: {},
  maze: {},
  save: {},
  audio: {},
  input: {},
  render: {},
  game: {},
  ui: {},
  debug: {}
};

window.__game = {
  /* defined in js/debug.js */
};
```

`FL.game.state` is the runtime state.

```js
FL.game.state = {
  version: 1,

  screen:
    "title" |
    "howToPlay" |
    "levelSelect" |
    "gameplay" |
    "pause" |
    "settings" |
    "levelComplete" |
    "gameComplete",

  levelId: null,
  selectedLevelId: null,
  settingsReturnTo: "title" | "pause" | null,

  level: null,
  maze: null,

  player: {
    x: 0,
    y: 0,
    moving: false,
    target: null,
    progressMs: 0,
    bufferedDirection: null,
    facing: null
  },

  timerMs: 0,
  timerStarted: false,

  exitUnlocked: false,
  orbsCollected: 0,
  lockedExitToastShown: false,

  trail: [
    {
      x: 0,
      y: 0,
      ageMs: 0,
      alpha: 1
    }
  ],

  visibleTiles: [
    { x: 0, y: 0 }
  ],

  toasts: [
    {
      text: "",
      remainingMs: 0
    }
  ],

  hint: {
    levelId: null,
    key: null,
    text: null
  },

  levelComplete: {
    levelId: 0,
    timeMs: 0,
    starsEarned: 0,
    bestMs: 0,
    newStars: 0
  } | null,

  gameComplete: {
    totalStars: 0
  } | null,

  save: {},
  settings: {},
  totalStars: 0,

  audioEnabled: true,
  audioLogging: true,
  audioLog: [],
  eventLog: []
};
```

Default settings:

```js
{
  input: "auto",
  colorblind: false,
  reducedMotion: false,
  textSize: "normal",
  masterVolume: 80,
  musicVolume: 60,
  sfxVolume: 80
}
```

`settings.input` is internal only. It may be used as a tie-breaker in input priority, but the UI must not present it as a toggle.

Default save:

```js
{
  version: 1,
  completed: {},
  stars: {},
  bestMs: {},
  settings: {
    input: "auto",
    colorblind: false,
    reducedMotion: false,
    textSize: "normal",
    masterVolume: 80,
    musicVolume: 60,
    sfxVolume: 80
  },
  hintsShown: {
    level1Move: false,
    level1Trail: false,
    level3Orb: false
  }
}
```

`FL.game.state.maze` in `getState()` must be JSON-safe:

```js
{
  width: number,
  height: number,
  walls: number[],
  start: { x, y },
  exit: { x, y },
  orbs: [{ x, y, collected: boolean }],
  loopCount: number,
  seed: number,
  fallbackUsed: boolean
}
```

## 2.3 Module specifics

| Module | Required exports / functions | Notes |
| --- | --- | --- |
| `FL.config` | `MOVE_MS`, `LIGHT_RADIUS`, `LIGHT_RADIUS_SQUARED`, `TRAIL_LIFETIME_MS`, `TRAIL_FADE_MS`, `TOAST_MS`, `VIEWPORT_TILES`, `MAX_CORRIDOR_TILES`, `GENERATION_ATTEMPTS`, `TOTAL_LEVELS`, `TOTAL_STARS`, `STEP_MS`, `CAMERA_LERP_MS`, `FADE_MS`, `STAR_REVEAL_MS`, `INPUT_PRIORITY` | All numeric constants. |
| `FL.rng` | `mulberry32(seed)`, `levelSeed(levelId)`, `attemptSeed(levelId, attempt)`, `fallbackSeed(levelId)`, `randomInt(rng, n)`, `shuffle(arr, rng)` | Deterministic PRNG. |
| `FL.levels` | `LEVELS`, `getLevel(id)`, `totalStars(save)` | Level table and helpers. |
| `FL.maze` | `DIRS`, `createMaze(width, height)`, `cellIndex(maze, x, y)`, `inBounds(maze, x, y)`, `hasWall(maze, x, y, dir)`, `isOpen(maze, x, y, dir)`, `removeWall(maze, x, y, dir)`, `reAddWall(maze, x, y, dir)`, `isBoundaryWall(maze, x, y, dir)`, `neighbor(maze, x, y, dir)`, `bfs(maze, from)`, `farthestCell(maze, start)`, `maxStraightCorridor(maze)`, `generateLevel(level, options)`, `validateMaze(maze, level, options)`, `buildFallback(level, seed)` | Maze logic. |
| `FL.save` | `defaultSave()`, `load()`, `save(state)`, `normalize(save)`, `isUnlocked(save, levelId)`, `playLevelId(save)`, `updateComplete(save, levelId, timeMs, stars)`, `updateSettings(save, settings)`, `setHintShown(save, key)` | Persistence. |
| `FL.audio` | `init()`, `play(name)`, `setEnabled(enabled)`, `setLogging(enabled)`, `setVolumes({ master, music, sfx })`, `ensureContext()`, `playTone(params)`, `playNoiseTick(params)`, `startMusic(context)`, `stopMusic()` | Synthesized audio. |
| `FL.input` | `bind()`, `unbind()`, `press(direction)`, `release(direction)`, `swipe(direction)`, `gamepadPress(direction)`, `gamepadRelease(direction)`, `pollGamepad()`, `clear()`, `getHeld()`, `getMostRecent()` | Input buffer. |
| `FL.render` | `init()`, `resize()`, `render(state)`, `drawFog()`, `drawFloor()`, `drawTrail()`, `drawWalls()`, `drawExit()`, `drawOrbs()`, `drawPlayer()`, `updateCamera(state)`, `applySettings(state)` | Canvas rendering. |
| `FL.game` | `init()`, `update(dtMs)`, `startLevel(levelId, options)`, `restartLevel()`, `pause()`, `resume()`, `quitToTitle()`, `openHowToPlay()`, `openLevelSelect()`, `openSettings()`, `nextLevel()`, `replayLevel()`, `setScreen(screen)`, `stepMovement(state)`, `updateTimer(state)`, `updateTrail(state)`, `updateVisibility(state)`, `updateToasts(state)`, `collectOrb(state, orb)`, `completeLevel(state)`, `getState()` | Core runtime. |
| `FL.ui` | `bind()`, `showScreen(state)`, `updateHUD(state)`, `updateTitle(state)`, `updateHowToPlay(state)`, `updateLevelSelect(state)`, `updateSettings(state)`, `updateLevelComplete(state)`, `updateGameComplete(state)`, `showToast(state)`, `setHint(state)`, `focusScreen(state)` | DOM UI. |
| `FL.debug` | All `window.__game` functions listed in Section 8. | Debug API. |

# 3. VISUAL SPEC

*Fading Labyrinth* is a quiet, nocturnal, high-contrast maze. The visual identity is calm and meditative: a dark fog surrounds the player, a small warm light reveals the nearby maze, and a pale trail fades like a memory. The style is minimal, geometric, vector-clean, and readable. There is no ornate fantasy detail, no pixel-art noise, no screen shake, and no busy environmental animation.

Lighting and atmosphere are central. The player’s light is a small warm radial glow centered on the player. Unrevealed space is near-black blue fog. The current light is bright and warm; trail memory is dimmer and cooler. Fog is static, with very subtle noise. No animated fog, particles, or environmental motion may imply hidden movement. The lighting gradient is decorative and must never reveal tiles outside the gameplay visibility mask.

The space is a flat 2D top-down grid rendered on a square canvas. The reference viewport shows `15 x 15` tiles. The camera centers on the player and clamps to maze bounds. If the maze is smaller than the viewport, the maze is centered. Walls are thick rounded line segments. The floor is a flat lit surface. The outer boundary is slightly thicker than interior walls. The player, orbs, exit, and trail must remain instantly distinguishable by shape, not color alone.

### Default palette

| Element | Hex | Notes |
| --- | ---: | --- |
| Fog / unexplored background | `#070A12` | Near-black blue |
| Floor, current light | `#C7D0DE` | Pale blue-gray |
| Floor, trail memory | `#6A7488` | Dimmer, cooler |
| Wall base | `#1E2532` | Dark slate |
| Wall highlight | `#3A455A` | Subtle top edge |
| Wall shadow | `#0F141D` | Subtle bottom edge |
| Player | `#FFB84D` | Warm amber |
| Player outline | `#2A1E0A` | Dark warm outline |
| Player light | `#FFE0B0` | Additive warm glow |
| Orb | `#6BE0FF` | Pale cyan |
| Orb ring | `#FFFFFF` | White ring |
| Orb outline | `#0B2A38` | Dark cyan outline |
| Exit unlocked frame | `#F5F7FA` | Near-white |
| Exit unlocked inner | `#FFD166` | Soft gold |
| Exit locked frame | `#8A93A6` | Muted gray |
| Exit locked bars | `#2F3744` | Dark gray bars |
| Trail marker | `#E8DCC8` | Pale bone/warm gray |
| HUD text | `#F5F7FA` | Near-white |
| HUD secondary text | `#B9C2D0` | Muted blue-gray |
| HUD panel background | `#0B0F1A` at 70% opacity | Subtle translucent panel |
| HUD panel border | `#2A3140` | Thin border |
| Primary button | `#FFB84D` | Amber |
| Primary button text | `#1A1408` | Dark warm |
| Secondary button | `#1E2532` | Dark slate |
| Secondary button text | `#F5F7FA` | Near-white |
| Disabled button | `#151A24` | Very dark |
| Disabled button text | `#5A6478` | Muted |
| Star filled | `#FFD166` | Gold |
| Star empty | `#2A3140` | Dark slate |
| Star empty border | `#5A6478` | Muted border |
| Focus ring | `#FFFFFF` | White, 2px |

### Colorblind palette

| Element | Colorblind mode |
| --- | --- |
| Fog | `#050505` |
| Floor, current light | `#C9D2E0` |
| Floor, trail memory | `#5A6478` |
| Wall base | `#10141D` |
| Player | `#FFD54F` with `#000000` outline |
| Orb | `#4FC3F7` with `#FFFFFF` ring and `#000000` outline |
| Exit unlocked | `#FFFFFF` frame, `#FFD54F` inner, `#000000` outline |
| Exit locked | `#111111` frame, `#FFFFFF` bars, `#000000` outline |
| Trail marker | `#FFFFFF` with `#000000` outline |
| HUD text | `#FFFFFF` |
| HUD secondary text | `#C7CDD6` |
| Primary button | `#FFD54F` with `#000000` text |
| Secondary button | `#10141D` with `#FFFFFF` text |
| Star filled | `#FFD54F` |
| Star empty | `#10141D` with `#C7CDD6` border |

Colorblind mode changes palette and outlines only. It does not change shapes.

### Act accents

| Act | Levels | Accent color | Feel |
| ---: | ---: | ---: | --- |
| Act I | 1-3 | `#82A9FF` | Pale, open, first light |
| Act II | 4-7 | `#7ED2D2` | Cooler, deeper |
| Act III | 8-10 | `#A491E8` | Violet, dense |
| Act IV | 11-12 | `#F0C75E` | Luminous final core |

Act accents are decorative only. They must not encode gameplay-critical states.

### In-game level themes

| Act | Floor tint | Wall tint | Fog |
| ---: | ---: | ---: | ---: |
| Act I | `#C7D0DE` | `#1E2532` | `#070A12` |
| Act II | `#BFC9DA` | `#1B2230` | `#060810` |
| Act III | `#B8C2D6` | `#19202D` | `#05060D` |
| Act IV | `#BAC4D8` | `#171E2B` | `#04050B` |

In-game themes are Tier 3. Tier 1 may use Act I colors for all levels.

### Typography

| Element | Normal | Large |
| --- | ---: | ---: |
| Title wordmark | 64px | 80px |
| Screen header | 32px | 40px |
| Button label | 18px | 22px |
| HUD level name | 16px | 20px |
| HUD objective | 14px | 18px |
| Timer | 20px | 25px |
| Best time | 12px | 15px |
| Toast text | 16px | 20px |
| Level select node number | 20px | 25px |
| Level select node name | 12px | 15px |

Large text scales UI text by `125%` and increases button/panel padding by about `10%`.

Timer uses tabular numerals:

```css
font-variant-numeric: tabular-nums;
```

### Visual recipe table

| Element | Shape / recipe | Size | Default color | Colorblind color | Animation | Tier |
| --- | --- | ---: | --- | --- | --- | ---: |
| Player | Rounded diamond / rotated rounded square with directional tick on front edge | `0.6` tile | `#FFB84D`, outline `#2A1E0A` | `#FFD54F`, black outline | Move: scale `1.06`, tilt `4` degrees over `140 ms`; idle light flicker `±2%` over `1500 ms` | 1 basic shape, 2 animation |
| Orb | Circle with white ring and small inner highlight | `0.4` tile | `#6BE0FF`, ring `#FFFFFF`, outline `#0B2A38` | `#4FC3F7`, white ring, black outline | Idle pulse scale `1.00` to `1.08` over `1200 ms`; collect scale to `0` over `300 ms` with 8 particles | 1 basic shape, 2/3 animation |
| Exit locked | Square frame with two horizontal bars | `0.8` tile | Frame `#8A93A6`, bars `#2F3744` | Frame `#111111`, bars `#FFFFFF`, black outline | No pulse; locked flash alpha `0.8` to `1.0` over `150 ms` when stepped on | 1 |
| Exit unlocked | Square frame with open center and bright inner circle | `0.8` tile | Frame `#F5F7FA`, inner `#FFD166` | Frame `#FFFFFF`, inner `#FFD54F`, black outline | Inner circle pulse scale `1.00` to `1.06` over `1500 ms`; unlock ring `400 ms` | 1 |
| Trail marker | Small rounded oval/dot on floor | `0.18` to `0.22` tile | `#E8DCC8` | `#FFFFFF` with black outline | Alpha `1.0` from `0` to `8000 ms`; linear fade to `0.0` from `8000` to `10000 ms` | 1 |
| Wall interior | Thick rounded line segment | `0.14` tile thick | `#1E2532`, highlight `#3A455A`, shadow `#0F141D` | `#10141D` | Static | 1 |
| Wall boundary | Thick rounded line segment | `0.18` tile thick | `#1E2532`, highlight `#3A455A`, shadow `#0F141D` | `#10141D` | Static | 1 |
| Floor | Flat lit surface | `1` tile | Act floor tint | Act floor tint | Static subtle noise alpha `0.03` to `0.05` | 1 |
| Fog | Flat unexplored background | Full canvas | Act fog tint | `#050505` | Static subtle noise alpha `0.04` | 1 |
| Player light | Warm radial additive glow | Radius `2.5` tiles | `#FFE0B0`, center alpha `0.30` to `0.35`, edge alpha `0` | Same, no flicker if reduced motion | Decorative only; clipped to visibility mask | 1 |
| Trail memory floor | Floor under trail-only tiles | `1` tile | About `45%` brightness of current light floor | Same | Static | 2 |
| Trail memory walls | Walls adjacent to trail-only tiles | Wall thickness | About `45%` brightness | Same | Static | 2 |
| Trail memory entities | Orbs/exit on trail-only tiles | Entity size | About `80%` brightness, shape fully legible | Same | Static | 2 |

### Render order

1. Fog base.
2. Visible floor tiles.
   - Current light floor: full brightness.
   - Trail memory floor: dimmed.
3. Trail markers.
4. Visible wall segments.
5. Visible orbs.
6. Visible exit.
7. Player light glow, clipped to visibility mask.
8. Player.
9. HUD and toasts.

### Visual rules ruled against gameplay

- The visual system must not reveal more than the gameplay visibility mask allows.
- A tile is visually revealed only if it is inside the player light radius or is an active trail tile.
- A wall segment is visible only if at least one adjacent tile is revealed.
- Orbs and the exit are visible only if their tile is revealed.
- If the final orb is collected while the exit is not visible, do not play a visible unlock animation that would reveal the exit. Show only toast and HUD update.
- Trail memory brightness is presentation only. It does not extend gameplay visibility.
- Act accents and themes are decorative only.
- Shapes must remain distinguishable in grayscale and colorblind mode.

# 4. GAMEPLAY SPEC

*Fading Labyrinth* is a 2D top-down maze-solving puzzle game. The player moves through 12 deterministic mazes with limited visibility and a fading 10-second trail. Some levels require collecting orbs before the exit unlocks. There is no fail state. Progression is linear, and stars are based on time. The core fantasy is exploring a maze that erases memory: only recent footprints remain, and the player must solve through observation, memory, and route planning.

### Records and rosters

| Record | Fields | Notes |
| --- | --- | --- |
| Level | `id`, `name`, `width`, `height`, `loops`, `orbs`, `minPath`, `parMs`, `threeStarMs`, `focus` | 12 fixed levels. |
| Maze | `width`, `height`, `walls`, `start`, `exit`, `orbs`, `loopCount`, `seed`, `fallbackUsed` | `walls` is a wall-bit array. |
| Player | `x`, `y`, `moving`, `target`, `progressMs`, `bufferedDirection`, `facing` | Logical grid cell. |
| Trail | `x`, `y`, `ageMs`, `alpha` | Sorted by `y`, then `x`. |
| Toast | `text`, `remainingMs` | At most one active toast. |
| Hint | `levelId`, `key`, `text` | Sparse tutorial hints. |
| Save | `version`, `completed`, `stars`, `bestMs`, `settings`, `hintsShown` | Local persistence. |
| Settings | `input`, `colorblind`, `reducedMotion`, `textSize`, `masterVolume`, `musicVolume`, `sfxVolume` | Accessibility and audio settings. |
| Event log | `{ type, ... }` | Debug/testing only. |

## 4.1 Level generation and validation — Tier 1

Levels are procedurally generated but deterministic.

Seed:

```text
seed = 1000 + level_id
```

Generation attempts:

- Try normal generation up to `10` times.
- If all attempts fail, use the deterministic fallback builder.
- If fallback fails, throw an error.

### Generation algorithm

Use iterative recursive backtracker / DFS.

Steps:

1. Choose maze width and height from the level table.
2. Choose a start corner using the seeded RNG.
3. Generate a perfect maze using iterative recursive backtracker.
4. Choose the exit as the farthest reachable cell from the start using BFS distance.
5. Add the level’s loop count by removing interior walls.
6. Place orbs according to the level’s orb count.
7. Validate the maze.
8. If validation fails, regenerate up to `10` times.
9. If all attempts fail, use the deterministic fallback builder.

### Start corner selection

Corners:

```text
(0, 0)
(width - 1, 0)
(width - 1, height - 1)
(0, height - 1)
```

Choose:

```text
cornerIndex = randomInt(rng, 4)
```

### Farthest exit tie-break

Choose the farthest reachable cell from start using:

1. Largest distance.
2. Largest `x`.
3. Largest `y`.

### Loop addition

A perfect maze has exactly one path between any two cells. Loops are added by removing extra interior walls.

Loop count is a level parameter.

Loop placement rules:

- Only remove interior walls.
- Do not remove boundary walls.
- Avoid removing walls directly adjacent to the start or exit.
- “Directly adjacent” means one of the wall’s two cells is the start or exit, or one of the wall’s two cells is a 4-neighbor of start or exit.
- If removing a wall makes the start-to-exit path shorter than `minPath`, reject that wall.
- If the maze fails validation, regenerate.

Loop addition must add exactly `level.loops` walls.

Candidate sorting:

- Lowest impact first.
- Deterministic wall key: `x,y,dir`.

Impact:

```text
impact = max(0, currentDistance - newDistance)
```

If fewer than `level.loops` walls can be added safely, the attempt fails.

### Orb placement

Orbs are placed after the maze and exit are determined.

Placement rules:

- Orbs must be in reachable cells.
- Orbs cannot be placed on the start or exit.
- Each orb must be at least `35%` of the maximum start-to-exit BFS distance away from the start.
- Each orb must be at least `20%` of the maximum start-to-exit BFS distance away from the exit.
- Orbs must be spaced apart from each other.
- Minimum separation: `max(3, floor(min(width, height) / 4))` Manhattan distance.
- If placement fails, relax separation once:
  - `relaxedSeparation = max(2, floor(minSeparation / 2))`.
- If it still fails, regenerate the maze.

Orbs in the final maze state are sorted by:

1. `y`
2. `x`

### Validation

A generated maze is valid only if:

- Maze width and height match the level.
- Start is in bounds.
- Exit is in bounds.
- Start and exit are different cells.
- All cells are reachable from the start.
- The exit is reachable from the start.
- Every orb is reachable from the start.
- The start-to-exit BFS distance is at least the level’s `minPath`.
- No orb is on the start or exit.
- No straight corridor is longer than `8` tiles.
- The maze does not contain isolated cells.
- If exact loops are required, `maze.loopCount === level.loops`.

### Straight corridor definition

A straight corridor is a maximal sequence of cells in one cardinal direction such that:

- The wall between each consecutive pair is open.
- Interior cells in the sequence have no open perpendicular walls.
- The sequence stops when the next wall is closed or out of bounds.

Validation fails if:

```text
maxStraightCorridor > 8
```

### Fallback builder

The fallback builder creates a deterministic maze that satisfies the level constraints.

It is used only if normal generation fails.

Fallback structure:

- Serpentine spine with short side branches.
- Local coordinates generated with start at `{ x: 0, y: 0 }`.
- Main columns: `x = 0, 2, 4, ...`
- Branch columns: `x = 1, 3, 5, ...`
- For each main column, open vertical walls for the full height.
- For each branch column, open a horizontal wall to the main column immediately to its left.
- Connect main columns in a serpentine path:
  - From main column `i` to main column `i + 1`:
    - If `i` is even, connect at bottom row.
    - If `i` is odd, connect at top row.
    - Open the wall between the branch cell and the next main column at that row.

Fallback loops:

- Safe loops are added by opening vertical walls inside branch columns.
- For each branch column `x`:
  - Candidate walls between `(x, y)` and `(x, y + 1)` for `y = 0` to `height - 2`.
- These loops create small cycles in side branches.
- They do not shorten the main start-to-exit path.
- Loop candidates must still exclude walls directly adjacent to start or exit.
- Shuffle candidates with the fallback RNG.
- Open exactly `level.loops` of them.

Fallback start corner:

1. Compute local start `{ x: 0, y: 0 }`.
2. Compute local exit as farthest cell from local start.
3. Choose a corner index with the fallback RNG.
4. Transform the local maze so local start maps to the chosen corner.

Transform rules:

- Top-left: identity.
- Top-right: mirror `x`.
- Bottom-right: mirror `x` and `y`.
- Bottom-left: mirror `y`.

Direction bits must transform accordingly.

Fallback orbs:

- Use the same orb placement algorithm as normal generation.
- If orb placement fails even after relaxing separation, the fallback attempt fails.

Fallback validation:

- Must pass `validateMaze(maze, level, { exactLoops: true })`.
- If it does not, `generateLevel` throws an error.

## 4.2 Player movement — Tier 1

The player moves one tile at a time on the grid.

### Movement rules

- The player can move up, down, left, and right.
- Diagonal movement is not allowed.
- The player cannot move through walls.
- The player cannot leave the maze boundary.
- The exit cell is passable.
- Orbs are collected automatically when the player enters their cell.
- The player occupies one logical cell at a time.

### Input

Supported input:

- Keyboard: Arrow keys or WASD.
- Gamepad: Left stick or D-pad.
- Touch: Swipe in a direction to move one tile. Repeated swipes continue movement.

Keyboard and gamepad support holding a direction to keep moving. Touch uses discrete swipes.

Keyboard keys:

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

Gamepad:

- Left stick threshold: `0.5`.
- D-pad buttons:
  - Button 12: up
  - Button 13: down
  - Button 14: left
  - Button 15: right

Touch:

- Swipe threshold: `24` pixels.
- Direction is the larger axis.
- If both axes are below threshold, ignore.
- A swipe moves exactly one tile.
- Touch swipes use a one-shot press:
  - Swipe presses a direction.
  - After one move completes, that touch direction is released automatically.

### Movement feel

| Value | Number |
| --- | ---: |
| Move time per tile | `140 ms` |
| Movement speed | `~7.1 tiles/sec` |
| Input buffer | `1 direction` |
| Diagonal movement | No |
| Acceleration | None |
| Friction | None |

### Input buffer rules

- If a direction is pressed while not moving, try to move immediately if valid.
- If a direction is pressed while moving, store it as the buffer.
- If multiple directions are pressed, use the most recent one.
- When a move completes:
  - If the buffered direction is valid, start the next move immediately.
  - If the buffered direction is invalid, remain still.
- If the buffered direction is released, choose the most recent remaining held direction, if any.

Direction values:

```text
"up"
"down"
"left"
"right"
```

### Movement edge cases

- Moving into a wall: no movement.
- Moving out of bounds: no movement.
- Moving onto an orb: collect orb.
- Moving onto a locked exit: player can stand on the exit, but level does not complete.
- Moving onto an unlocked exit: level completes at the end of the move animation.
- Pausing while moving: movement pauses and preserves `progressMs`.
- Restarting while moving: movement state resets.

## 4.3 Visibility and trail — Tier 1

The player cannot see the whole maze.

### Light radius

- Light radius: `2.5` tiles.
- Visibility is measured using Euclidean distance from the player’s cell center to tile centers.
- Tiles within the light radius are visible.
- Walls are visible if at least one adjacent tile is visible.
- The current tile is always visible.

Squared distance check:

```text
dx * dx + dy * dy <= 6.25
```

### Trail

When the player moves into a tile, that tile receives a trail marker.

Trail rules:

- Trail lifetime: `10000 ms`.
- Trail fade time: last `2000 ms`.
- Trail alpha:
  - `1.0` from `0` to `8000 ms`
  - Linear fade from `1.0` to `0.0` from `8000` to `10000 ms`
- Trail tiles remain visible even if they are outside the current light radius.
- Trail is shown on the floor.
- Walls adjacent to a trail tile remain visible while that trail tile is visible.
- Old trail tiles are removed when their lifetime expires.
- Revisiting a tile resets its trail age to `0`.

### Revealed tile rule

A tile is revealed if:

```text
visibleByLight(tile) || activeTrail(tile)
```

A wall is visible if at least one of its adjacent tiles is revealed.

Orbs are visible only if their tile is revealed.

The exit is visible only if its tile is revealed.

### Visibility edge cases

- The current tile is always visible.
- The player’s light does not reveal the exit if the exit is outside the light radius.
- Orbs are only visible when in the light radius or on a visible trail tile.
- The exit is only visible when in the light radius or on a visible trail tile.
- No persistent memory map is provided.
- After trail expires, the tile is no longer visible unless in light radius.

## 4.4 Objective system — Tier 1

### Win condition

The player wins a level by entering the exit cell while the exit is unlocked.

### Exit lock

If the level has orbs:

- Exit starts locked.
- Exit becomes unlocked when all orbs are collected.
- The player can stand on the locked exit, but the level does not complete.
- The player must move to the exit again after collecting all orbs.

If the level has no orbs:

- Exit is unlocked from the start.

### Orb collection

- Orbs are collected automatically.
- Collecting an orb removes it from the maze.
- The HUD updates immediately.
- A toast message appears:
  - If orbs remain: `Orb collected`
  - If this was the final orb: `Exit unlocked`

### Objective edge cases

- Player reaches exit before collecting orbs: exit remains locked.
- Player collects final orb elsewhere: exit unlocks immediately.
- Player collects all orbs and then reaches exit: level completes.
- Player restarts level: orbs reset and exit locks again if orbs exist.
- Player pauses: objective state pauses with the level.

### Locked exit interaction

When the player completes a move onto a locked exit:

- Level does not complete.
- If `lockedExitToastShown` is false:
  - Show toast `Exit locked`.
  - Set `lockedExitToastShown` to true.
- Play audio `lockedExit`.
- The toast appears once per level attempt.

## 4.5 Progression and scoring — Tier 1

### Level unlocking

- Level 1 is unlocked at start.
- Each level unlocks the next level after completion.
- Completed levels can be replayed at any time from level select.

Unlock rule:

```text
level 1 is unlocked
level N > 1 is unlocked if level N-1 is completed
```

### No fail state

There is no fail state.

The player can always restart if they become lost. Stars provide optional challenge without blocking progression.

### Timer

- The timer starts on the player’s first successful move start.
- The timer does not start on invalid input.
- The timer pauses when the game is paused.
- The timer resets when the level is restarted.
- The timer is not a fail condition.
- Timer format: `M:SS`.
- Use floor seconds.

Example:

```text
95000 -> "1:35"
```

### Stars

Stars are optional.

Star rules:

- 1 star: Complete the level.
- 2 stars: Complete the level at or under par time.
- 3 stars: Complete the level at or under 3-star time.

Star calculation:

```text
stars = 1
if (timeMs <= level.parMs) stars = 2
if (timeMs <= level.threeStarMs) stars = 3
```

The level table’s `threeStarMs` values are authoritative. If a future level omits `threeStarMs`, compute:

```text
threeStarMs = Math.floor(parMs * 0.7 / 1000) * 1000
```

### Best time

- The game stores the best time for each level.
- Replaying a level can improve best time and stars.
- Stars are stored as the highest earned star count.
- Best time improves only when the new time is lower.
- Replaying with a worse time does not reduce saved stars.

### Level table

| Level | Name | Size | Loops | Orbs | Min Path | Par | Par ms | 3-Star | 3-Star ms | Focus |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | First Steps | 7x7 | 0 | 0 | 14 | 0:40 | 40000 | 0:28 | 28000 | Teach movement, light, and trail |
| 2 | Winding Path | 9x9 | 2 | 0 | 20 | 1:00 | 60000 | 0:42 | 42000 | Larger basic maze |
| 3 | Forks | 9x9 | 5 | 1 | 22 | 1:15 | 75000 | 0:53 | 53000 | Introduce loops and first orb |
| 4 | Gathering Light | 11x11 | 8 | 1 | 28 | 1:35 | 95000 | 1:07 | 67000 | Orbs required to unlock exit |
| 5 | Crossroads | 11x11 | 12 | 2 | 30 | 1:55 | 115000 | 1:21 | 81000 | More loops and route choice |
| 6 | Deep Hall | 13x13 | 16 | 2 | 36 | 2:20 | 140000 | 1:38 | 98000 | Size increase |
| 7 | Tangle | 13x13 | 22 | 2 | 40 | 2:40 | 160000 | 1:52 | 112000 | Dense loop structure |
| 8 | Long Way | 15x15 | 28 | 3 | 46 | 3:10 | 190000 | 2:11 | 131000 | Longer required exploration |
| 9 | Labyrinth | 15x15 | 36 | 3 | 50 | 3:40 | 220000 | 2:34 | 154000 | More orbs and ambiguity |
| 10 | Echo Chamber | 17x17 | 44 | 3 | 56 | 4:10 | 250000 | 2:53 | 173000 | Larger memory challenge |
| 11 | Winding End | 19x19 | 55 | 4 | 66 | 4:50 | 290000 | 3:23 | 203000 | Four orbs, high route complexity |
| 12 | Final Maze | 21x21 | 68 | 4 | 76 | 5:40 | 340000 | 3:58 | 238000 | Full-size final challenge |

### Progression edge cases

- Player completes level with no stars beyond 1: level still unlocks.
- Player replays a completed level: stars and best time can improve.
- Player quits mid-level: current attempt is lost, but previous progress remains.
- Player restarts: timer and level state reset, but saved progress remains.
- Player completes final level: game complete screen appears.

### Difficulty curve

Difficulty increases through:

1. Maze size.
2. Loop density.
3. Orb count.
4. Required path length.
5. Memory load.

The player never faces a new mechanic in the final level. By Level 12, all mechanics are already understood.

## 4.6 Save and settings — Tier 1

The game saves locally.

Storage:

- Use `localStorage` if available.
- If `localStorage` is unavailable or throws, use an in-memory fallback.

Storage key:

```text
"fadingLabyrinth.save.v1"
```

Save shape:

```js
{
  version: 1,
  completed: {},
  stars: {},
  bestMs: {},
  settings: {},
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

Save timing:

- Save after level complete.
- Save after settings change.
- Save after hint flag change.
- Do not save mid-level progress.

Save edge cases:

- If save file is missing, start with no progress.
- If save file is corrupted, reset to default progress.
- If a level is completed out of order through level select, update save normally.

Settings:

| Setting | Control | Save field | Notes |
| --- | --- | --- | --- |
| Input | Informational label | `input` internal only | Shows supported inputs; not a toggle. |
| Colorblind mode | Toggle | `colorblind` | On/Off. |
| Reduced motion | Toggle | `reducedMotion` | On/Off. |
| Text size | Segmented control | `textSize` | Normal / Large. |
| Master volume | Slider | `masterVolume` | 0-100. |
| Music volume | Slider | `musicVolume` | 0-100. |
| SFX volume | Slider | `sfxVolume` | 0-100. |

Settings do not affect star fairness.

## 4.7 Accessibility — Tier 2

### Input

Supported:

- Keyboard.
- Gamepad.
- Touch.

No mouse-only requirements.

All supported inputs work simultaneously.

### Colorblind support

- Use shapes and icons, not color alone.
- Exit should have a distinct shape.
- Orbs should have a distinct shape.
- Player should have a distinct shape.
- Locked and unlocked exit should differ by shape or icon, not just color.
- Colorblind mode adds outlines and adjusts hue.
- Colorblind mode does not change shapes.

### Reduced motion

When enabled:

- Disable pulsing exit animation.
- Disable star animation effects.
- Use simple fade instead of complex trail fade effects.
- Remove any screen shake or camera bounce.
- Disable player light flicker.
- Disable player scale/tilt animation.
- Disable orb pulse.
- Disable particle bursts.
- Disable camera lerp.
- Use simple fades instead of complex motion.

Reduced motion must not change movement timing, trail lifetime, light radius, or star times.

### Text

- Text size setting affects HUD and menus.
- Normal: 100%.
- Large: 125%.
- Text should remain readable at the smallest supported display size.

## 4.8 Feel — Tier 1 / 2 / 3

Movement feel:

- Crisp, responsive, and readable.
- The player should feel in control without movement becoming a reflex challenge.
- Holding a direction continues movement smoothly.
- Turning is applied after the current tile move completes.

Visibility feel:

- The player can always see enough to make the next decision, but not enough to solve the whole maze at once.
- The trail should feel like a fading memory, not a map.
- Current light is bright and immediate; trail memory is dimmer and cooler.

Difficulty feel:

- Early levels are small enough to be solved quickly.
- Mid levels introduce more loops and orbs.
- Late levels are larger and require stronger memory.
- The final level tests mastery of existing systems, not new mechanics.

# 5. CHARACTERS

## Silhouettes

| Entity | Silhouette | Why |
| --- | --- | --- |
| Player | Rounded diamond with directional tick | Distinct from orbs and exit; easy to read at small size. |
| Orb | Circle with ring | Clearly collectible and distinct from player. |
| Exit | Square frame | Distinct from player and orbs. |
| Locked exit | Square frame with horizontal bars | Shape differs from unlocked exit. |
| Unlocked exit | Square frame with open circle | Shape differs from locked exit. |
| Trail | Small dot/oval | Reads as a footprint/memory mark, not a collectible. |
| Wall | Thick rounded line segment | Clear maze structure. |
| Floor | Flat lit surface | Neutral background for gameplay objects. |

## Player states and animations

| State | Required by gameplay | Animation | Motion rules | Reduced motion |
| --- | --- | --- | --- | --- |
| Idle | Always | Static player shape with facing tick | Facing updates to last valid movement direction. | Static. |
| Moving | Movement system | Move animation | Move time `140 ms`. Scale to `1.06`. Tilt about `4` degrees toward movement direction. Return to normal by end of move. | No scale, no tilt. Use simple `140 ms` linear interpolation or snap. |
| Facing up | Input/movement | Directional tick on top edge | Tick size about `0.12` tile. Same color as player. | Same shape. |
| Facing down | Input/movement | Directional tick on bottom edge | Same. | Same. |
| Facing left | Input/movement | Directional tick on left edge | Same. | Same. |
| Facing right | Input/movement | Directional tick on right edge | Same. | Same. |

## Orb states and animations

| State | Required by gameplay | Animation | Motion rules | Reduced motion |
| --- | --- | --- | --- | --- |
| Visible | Orb visibility | Idle pulse | Scale from `1.00` to `1.08` over `1200 ms` using smooth sine curve. | No pulse. Static orb. |
| Collected | Orb collection | Collection animation | Orb scales to `0` over `300 ms`. Emit 8 small particles outward. Particle size `0.08` to `0.12` tile. Particle color orb color and white. Duration `300 ms`. Fade out. | No particles. Orb fades out over `150 ms`. |

## Exit states and animations

| State | Required by gameplay | Animation | Motion rules | Reduced motion |
| --- | --- | --- | --- | --- |
| Locked | Objective system | No pulse | When player steps onto locked exit: bars flash once, alpha from `0.8` to `1.0` over `150 ms`. | No flash. Toast and HUD still occur. |
| Unlocked | Objective system | Inner circle pulse | Scale from `1.00` to `1.06` over `1500 ms` using smooth sine curve. | No pulse. Static unlocked exit. |
| Unlock moment | Final orb collected | Unlock animation | If exit is visible: bars disappear, inner circle fades in over `250 ms`, small expanding ring alpha `0.4` over `400 ms`. If exit is not visible: no visible unlock animation. | Simple fade between locked and unlocked states. |

## Trail states

| State | Required by gameplay | Animation | Motion rules | Reduced motion |
| --- | --- | --- | --- | --- |
| Active | Trail system | Trail marker | Alpha `1.0` from `0` to `8000 ms`. Linear fade from `1.0` to `0.0` from `8000` to `10000 ms`. | Same simple alpha fade. |
| Expired | Trail lifetime | Removed | Remove marker at age `>= 10000 ms`. | Same. |

# 6. AUDIO

Audio is non-essential. Every gameplay-critical event must also have a visual cue.

All SFX are synthesized with WebAudio. No external audio files are required.

Routing:

- SFX: SFX gain -> master gain.
- Music: music gain -> master gain.
- Defaults: master `80`, music `60`, SFX `80`.

### SFX table

| Name | Recipe | When it plays |
| --- | --- | --- |
| `step` | Short filtered noise tick. Duration `40 ms`. Lowpass filter alternates between `1800 Hz` and `2200 Hz` based on step count. Gain `0.08`. Exponential decay. | Each completed tile move. |
| `orb` | Bright two-note chime. Sine `880 Hz` for `120 ms`, volume `0.20`. Sine `1318.5 Hz` delayed `50 ms` for `120 ms`, volume `0.15`. | Orb collected. |
| `exitUnlocked` | Rising soft chord. Sines `261.6 Hz`, `329.6 Hz`, `392.0 Hz`, each `300 ms`, staggered by `50 ms`. Volumes `0.15`, `0.12`, `0.12`. | Final orb collected. |
| `lockedExit` | Low muted thud plus short click. Sine `120 Hz` for `150 ms`, volume `0.15`. Noise tick `50 ms`, lowpass `800 Hz`, delayed `20 ms`, volume `0.05`. | Player steps onto locked exit. |
| `levelComplete` | Gentle rising arpeggio. Sines `261.6 Hz`, `329.6 Hz`, `392.0 Hz`, `523.3 Hz`, each `350 ms`, staggered by `100 ms`. Volume `0.15`. | Level complete. |
| `star` | High soft ping. Sine `1046.5 Hz` for `100 ms`, volume `0.15`. | Once per newly earned star. |
| `uiSelect` | Short soft tick. Triangle `1000 Hz` for `30 ms`, volume `0.08`. | Primary UI selection. |
| `uiBack` | Slightly lower short tick. Triangle `700 Hz` for `30 ms`, volume `0.07`. | Back navigation. |

### Music table — Tier 3

| Context | Style | Tempo | Recipe | When it plays |
| --- | --- | ---: | --- | --- |
| Title | Low drone, soft pad | 50 BPM | Two sine oscillators slightly detuned around `110 Hz` and `110.5 Hz`, low-pass filtered, very low volume. Sparse notes from D minor pentatonic every 2-4 seconds. | Title screen. |
| Gameplay Act I | Sparse pad, occasional celesta-like note | 60 BPM | Low drone plus sparse sine/triangle notes from D minor pentatonic. Fewer notes. | Levels 1-3. |
| Gameplay Act II | Slightly deeper drone, soft low pulse every 2 beats | 64 BPM | Lower drone, very soft low pulse, sparse notes. | Levels 4-7. |
| Gameplay Act III | Deeper pad, slightly more notes | 68 BPM | Deeper drone, slightly more note density. Still calm. | Levels 8-10. |
| Level Complete | Warm major chord, gentle arpeggio | 70 BPM | Warm chord plus gentle arpeggio. Satisfying, not celebratory. | Level Complete screen. |
| Game Complete | Fuller ambient pad, soft resolving chord | 66 BPM | Fuller pad, resolving chord. Complete, calm. | Game Complete screen. |

D minor pentatonic notes:

```text
D F G A C
```

Reference frequencies:

```text
D3 146.83 Hz
F3 174.61 Hz
G3 196.00 Hz
A3 220.00 Hz
C4 261.63 Hz
```

Music rules:

- No heavy percussion.
- No fast rhythmic patterns.
- No loud sudden stingers.
- No audio-only gameplay cues.
- Music should be sparse enough that the player can think.
- Music ducks approximately `20%` to `30%` when a toast appears.
- Music pauses or ducks when the pause screen is open.

# 7. UX

UX is implemented with HTML, CSS, and DOM. The maze viewport is a `<canvas>` presentation surface. All interactive UI controls are HTML buttons/inputs styled with CSS. No mouse-only interactions are required.

## DOM structure

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

Gameplay screen contains:

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

## State machine

| From | Event | To |
| --- | --- | --- |
| `title` | Play | `gameplay` |
| `title` | Level Select | `levelSelect` |
| `title` | How to Play | `howToPlay` |
| `title` | Settings | `settings` |
| `howToPlay` | Back | `title` |
| `levelSelect` | Play Level | `gameplay` |
| `levelSelect` | Back | `title` |
| `gameplay` | Pause | `pause` |
| `gameplay` | Level complete, level 1-11 | `levelComplete` |
| `gameplay` | Level complete, level 12 | `gameComplete` |
| `pause` | Resume | `gameplay` |
| `pause` | Restart Level | `gameplay` |
| `pause` | Level Select | `levelSelect` |
| `pause` | Settings | `settings` |
| `pause` | Quit to Title | `title` |
| `settings` | Back | `settingsReturnTo` |
| `levelComplete` | Next Level | `gameplay` |
| `levelComplete` | Replay | `gameplay` |
| `levelComplete` | Level Select | `levelSelect` |
| `gameComplete` | Level Select | `levelSelect` |
| `gameComplete` | Title | `title` |

Settings return behavior:

- If opened from title, back returns to title.
- If opened from pause, back returns to pause.

## Screens

### Title screen

Content:

- Game title: `Fading Labyrinth`
- Total stars: `X / 36`
- Buttons:
  - `Play`
  - `Level Select`
  - `How to Play`
  - `Settings`

`Play` behavior:

- If no progress: start Level 1.
- If progress exists: start the next incomplete unlocked level.
- If all levels are completed: start Level 1.

Initial focus: `Play`.

### How to Play screen

Content:

- Header: `How to Play`
- Three cards.
- Back button.

Card 1: Move

```text
Use Arrow Keys, WASD, Left Stick, D-Pad, or Touch Swipe.
Holding a direction keeps moving.
Swiping moves one tile at a time.
```

Card 2: Light and Trail

```text
You only see a small area around your character.
Your trail remains for 10 seconds.
The trail fades after 8 seconds.
```

Card 3: Objective

```text
Find the exit.
If orbs are present, collect all of them to unlock the exit.
There is no fail state.
Stars are based on time.
```

### Level Select screen

Content:

- Header: `Level Select`
- Total stars: `X / 36`
- Back button
- Serpentine 4x3 grid of 12 level nodes.
- `Play Level` button.

Node layout:

```text
1 → 2 → 3 → 4
            ↓
8 ← 7 ← 6 ← 5
            ↓
9 → 10 → 11 → 12
```

Each node shows:

- Level number.
- Level name.
- Star count, if completed.
- Lock icon if locked.
- Highlight if selected.

Node states:

| State | Appearance |
| --- | --- |
| Locked | Dim, desaturated, lock icon |
| Unlocked | Full color, act accent ring |
| Completed | Full color, stars visible |
| Selected | White focus ring, slight scale `1.05` |

Node size:

- Normal: `72px`
- Large text: `84px`

Locked node behavior:

- Locked nodes can be selected for viewing.
- `Play Level` is disabled.
- Show tooltip or label:
  ```text
  Complete previous level to unlock
  ```

### Gameplay screen

Content:

- Maze canvas.
- HUD.
- Toasts.
- Tutorial hints, if active.

Pause input:

- Keyboard: `Esc` or `P`
- Gamepad: `Start`
- Touch: pause button

### Pause screen

Overlay:

- Darken gameplay.
- Overlay alpha: `70%`
- Freeze all gameplay animation.
- Freeze trail fade.
- Freeze timer.
- Freeze player movement.
- Freeze toast timing.

Panel content:

- Header: `Paused`
- Buttons:
  1. `Resume`
  2. `Restart Level`
  3. `Level Select`
  4. `Settings`
  5. `Quit to Title`

Initial focus: `Resume`.

### Level Complete screen

Used for Levels 1-11.

Content:

- Header: `Level Complete`
- Level name.
- Stars earned: 1 to 3.
- Time.
- Best time.
- If this is a new best time, show label:
  ```text
  New Best
  ```
- Buttons:
  1. `Next Level`
  2. `Replay`
  3. `Level Select`

Initial focus: `Next Level`.

Star display:

- Three star icons in a row.
- Empty stars: dark outline.
- Earned stars: gold.

Star animation:

- First star fills at `200 ms`.
- Second star fills at `600 ms`, if earned.
- Third star fills at `1000 ms`, if earned.
- Each star:
  - Scale from `0.6` to `1.0`
  - Slight rotation: `-10 degrees` to `0`
  - Duration: `250 ms`
- Reduced motion:
  - Stars fade in sequentially.
  - No scale.
  - No rotation.
  - No shine.

### Game Complete screen

Appears after completing Level 12.

Content:

- Header: `The Labyrinth Is Complete`
- Total stars: `X / 36`
- Final level card:
  - Level name: `Final Maze`
  - Stars earned
  - Time
  - Best time
- Buttons:
  1. `Level Select`
  2. `Title`

Initial focus: `Level Select`.

### Settings screen

Content:

- Header: `Settings`
- Back button
- Settings items.

Settings items:

| Setting | Control | Notes |
| --- | --- | --- |
| Input | Informational label | Shows `Keyboard, Gamepad, Touch`. Not a toggle. |
| Colorblind mode | Toggle | On/Off. |
| Reduced motion | Toggle | On/Off. |
| Text size | Segmented control | Normal / Large. |
| Master volume | Slider | 0-100. |
| Music volume | Slider | 0-100. |
| SFX volume | Slider | 0-100. |

Settings save immediately when changed.

## HUD table

| Element | Record field | When visible |
| --- | --- | --- |
| `#hud-level` | `state.level.id`, `state.level.name` | During gameplay and pause. |
| `#hud-objective` | Computed from `state.level.orbs`, `state.orbsCollected`, `state.exitUnlocked`, `state.player` | During gameplay and pause. |
| `#hud-timer` | `state.timerMs` formatted as `M:SS` | During gameplay and pause. |
| `#hud-best` | `state.save.bestMs[state.levelId]` formatted as `M:SS` | During gameplay if a best time exists. |
| `#hud-pause` | Action button | During gameplay. |
| `#hud-hint` | `state.hint.text` | When a tutorial hint is active. |
| `#toast` | `state.toasts[0].text` | When a toast is active. |

Objective display:

| State | Icon | Text | Condition |
| --- | --- | --- | --- |
| No orbs | Exit icon | `Exit` | Level has `0` orbs. |
| Orbs remain | Orb icon | `Orbs X/Y` | Orbs remain. |
| All orbs collected | Unlocked exit icon | `Exit Open` | All orbs collected and exit unlocked. |
| Standing on locked exit | Locked exit icon | `Exit Locked` | Player is on exit and exit is locked. Overrides orb count. |

Toast rules:

- Duration: `1500 ms`.
- One toast at a time.
- New toast replaces current toast.
- Fade in: `200 ms`.
- Fade out: `200 ms`.
- Do not block movement.
- Toasts pause when game is paused.

Toast types:

| Event | Icon | Text |
| --- | --- | --- |
| Orb collected, orbs remain | Orb icon | `Orb collected` |
| Final orb collected | Unlocked exit icon | `Exit unlocked` |
| Player steps onto locked exit | Locked exit icon | `Exit locked` |

The `Exit locked` toast appears only once per level attempt.

## Tutorial hints

Hints appear in the bottom-left area.

| Level | Trigger | Text | Save flag |
| ---: | --- | --- | --- |
| 1 | On load, if not shown | `Move to explore.` | `hintsShown.level1Move` |
| 1 | After first move, if not shown | `Your trail fades after 10 seconds.` | `hintsShown.level1Trail` |
| 3 | When first orb becomes visible, first time, if not shown | `Collect orbs to unlock the exit.` | `hintsShown.level3Orb` |

Control hint on first-time play until first move:

```text
Arrows / WASD / Swipe
```

## Button style

| State | Fill | Text | Notes |
| --- | --- | --- | --- |
| Primary normal | `#FFB84D` | `#1A1408` | Main action |
| Primary hover/selected | `#FFC66B` | `#1A1408` | Subtle brighten |
| Primary pressed | `#E6A23C` | `#1A1408` | Slight darken |
| Secondary normal | `#1E2532` | `#F5F7FA` | Border `#3A455A` |
| Secondary hover/selected | `#2A3140` | `#F5F7FA` |  |
| Secondary pressed | `#151A24` | `#F5F7FA` |  |
| Disabled | `#151A24` | `#5A6478` | No border emphasis |

Focus state:

- White focus ring.
- 2px thickness.
- 2px offset.
- Visible on keyboard and gamepad navigation.

Touch targets:

- Minimum button height: `48px`
- Minimum touch target: `48x48px`
- Pause button in gameplay must be easily reachable.

## CSS variables

Expected CSS custom properties:

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

Accessibility classes:

```css
.colorblind
.reduced-motion
.text-large
```

These classes affect UI and rendering presentation only. They do not affect gameplay fairness.

# 8. DEBUG API

`window.__game` is the debug API.

It must be available after `js/debug.js` loads.

| Function / property | Purpose |
| --- | --- |
| `version` | API version string. |
| `getState()` | Returns JSON-safe state copy. |
| `reset()` | Resets game to first launch. |
| `startLevel(levelId, options)` | Starts level. Options: `{ force: false }`. |
| `restartLevel()` | Restarts current level. |
| `pause()` | Pauses gameplay. |
| `resume()` | Resumes gameplay. |
| `quitToTitle()` | Returns to title. |
| `openHowToPlay()` | Opens How to Play. |
| `openLevelSelect()` | Opens Level Select. |
| `openSettings()` | Opens Settings. |
| `nextLevel()` | Starts next level from level complete. |
| `replayLevel()` | Replays current level. |
| `setScreen(screen)` | Debug screen setter. |
| `setSetting(key, value)` | Sets one setting and saves. |
| `setSettings(settings)` | Sets multiple settings and saves. |
| `press(direction)` | Presses a movement direction. |
| `release(direction)` | Releases a movement direction. |
| `swipe(direction)` | Simulates a one-shot touch swipe. |
| `gamepadPress(direction)` | Simulates gamepad direction press. |
| `gamepadRelease(direction)` | Simulates gamepad direction release. |
| `clearInput()` | Clears all input state. |
| `tick(ms)` | Advances logic by `ms` milliseconds. |
| `setAutoUpdate(enabled)` | Enables/disables rAF-driven auto update. |
| `setSave(saveObject)` | Replaces save. |
| `loadSave(jsonString)` | Loads save from JSON string. |
| `clearSave()` | Clears save to default. |
| `generateLevel(levelId, options)` | Generates maze. Options: `{ forceFallback: false, seedOverride: null }`. |
| `validateMaze(maze, levelId, options)` | Validates maze. Options: `{ exactLoops: true }`. |
| `pathfind(from, to)` | Returns BFS direction path or `null`. |
| `solveLevel()` | Returns Promise. Solves current level using debug input. |
| `setTimer(ms)` | Sets timer directly. |
| `teleport(x, y)` | Sets player logical cell without side effects. |
| `setPlayer(x, y)` | Sets player logical cell and resets movement. |
| `setFacing(direction)` | Sets player facing. |
| `collectOrb(index)` | Collects orb at sorted index. |
| `setOrbsCollected(count)` | Sets collected orb count and updates objective. |
| `setExitUnlocked(unlocked)` | Sets exit unlock state. |
| `forceComplete(timeMs)` | Completes level immediately with given timer. |
| `clearTrail()` | Clears trail. |
| `setTrail(x, y, ageMs)` | Adds/refreshes trail marker. |
| `setTrailAge(x, y, ageMs)` | Sets trail age for existing marker. |
| `showToast(text)` | Shows toast. |
| `clearToasts()` | Clears toasts. |
| `setHint(levelId, key, text)` | Sets tutorial hint. |
| `clearHint()` | Clears hint. |
| `isTileVisible(x, y)` | Returns logical visibility for tile. |
| `isWallVisible(x, y, dir)` | Returns wall segment visibility. |
| `getTrailAge(x, y)` | Returns trail age or `null`. |
| `playSfx(name)` | Plays/logs SFX. |
| `setAudioEnabled(enabled)` | Enables/disables audio playback. |
| `setAudioLogging(enabled)` | Enables/disables audio log. |
| `setVolumes({ master, music, sfx })` | Sets volume settings. |
| `audioLog` | Array of audio event names. |
| `eventLog` | Array of event objects. |
| `clearAudioLog()` | Clears audio log. |
| `clearEventLog()` | Clears event log. |

`getState()` must not return internal `Uint8Array` directly. Maze walls in state must be a normal array.

`reset()` behavior:

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

`startLevel(levelId, options)`:

- If `force` is false, level must be unlocked.
- If locked and not forced, return `false`.
- Generate or fetch deterministic maze.
- Reset level attempt state.
- Set screen to `gameplay`.
- Return `true` on success.

`tick(ms)`:

- `ms` must be a non-negative number.
- If screen is not `gameplay`, no gameplay state changes.
- If paused, no gameplay state changes.
- If level complete, no gameplay state changes.
- Processes movement, timer, trail, toasts deterministically.
- May complete multiple tile moves if `ms` is large.

`solveLevel()`:

- Returns a Promise.
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

`forceComplete(timeMs)`:

- Debug-only.
- If screen is `gameplay`:
  - Set timer to `timeMs`.
  - Complete the level immediately.

`teleport(x, y)`:

- Debug-only.
- Sets player logical cell to `x,y`.
- Does not trigger:
  - Orb collection.
  - Exit completion.
  - Trail creation.

`collectOrb(index)`:

- Debug-only.
- Marks the orb at the given sorted index as collected.
- Updates objective and exit lock state.

`isTileVisible(x, y)`:

```text
visibleByLight(x, y) || activeTrail(x, y)
```

`isWallVisible(x, y, dir)`:

Returns whether the wall segment on side `dir` of cell `(x,y)` is visible.

`getTrailAge(x, y)`:

Returns:

```text
number | null
```

# 9. TESTS

Tests run in a headless page through `test.html`.

`window.__runTests` must be `true` before `js/tests.js` runs.

When finished, set:

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

Headless validation waits until:

```js
window.__testResults !== null
```

and asserts:

```js
window.__testResults.failed === 0
```

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

## Tier 1 tests

| Test | Validates |
| --- | --- |
| Level table integrity | 12 levels exist, IDs 1-12, names non-empty, positive sizes, `parMs > threeStarMs > 0`, `minPath > 0`, `orbs >= 0`, `loops >= 0`. |
| RNG determinism | Same seed produces same sequence; different seeds differ; `randomInt` in range; shuffle deterministic. |
| Normal level generation is valid | For every level, `generateLevel` produces valid maze with exact loops, correct size/orbs/loops, corner start, farthest exit, deterministic walls/orbs/start/exit. |
| Fallback generation is valid | For every level, `forceFallback: true` produces valid maze with `fallbackUsed === true`, exact loops, corner start, farthest exit, deterministic output. |
| Movement is blocked by walls | Invalid directions do not move player. |
| Valid movement works | Valid direction moves player one tile, creates trail, starts timer. |
| Input buffer works | Direction pressed during move becomes buffered and applies after current move. |
| Holding direction continues movement | Holding a direction moves multiple tiles if path is clear. |
| Orb collection works | Orbs collect, HUD updates, toast correct, audio log contains `orb`, final orb unlocks exit. |
| Locked exit does not complete level | Standing on locked exit does not complete; toast once; audio log contains `lockedExit`. |
| Level completion works | Entering unlocked exit completes level, updates save, stars, best time, audio log. |
| Star calculation | Times below/equal 3-star, par, and above par produce 3, 2, 1 stars; replay improves/does not reduce correctly. |
| Timer starts on first move | Invalid input does not start timer; valid move starts timer. |
| Timer pauses and resumes | Pause freezes timer; resume advances timer. |
| Trail lifetime and fade | Trail age, alpha, fade, and removal are correct. |
| Trail remains visible outside light radius | Trail tile visible after teleport until expiry. |
| Light radius visibility | Tiles within `2.5` visible; outside not visible; walls adjacent to visible tiles visible. |
| No persistent memory | After trail expires, tile is not visible. |
| Save persistence and progression | Fresh save, unlock progression, out-of-order completion, corrupted save reset. |
| Level select behavior | Level 1 playable, locked levels not playable, selected level starts. |
| Input device simulation | Keyboard press/release, gamepad simulation, touch swipe, most recent input wins. |
| Full campaign playability | Reset, then solve levels 1-12 in order; levels unlock; screens correct; save updates. |
| Debug state is serializable | `JSON.stringify(__game.getState())` does not throw and contains required fields. |

## Tier 2 tests

| Test | Validates |
| --- | --- |
| Settings affect UI and save | Changing `colorblind`, `reducedMotion`, `textSize`, volumes updates save and DOM classes/attributes. |
| Accessibility settings do not affect fairness | Light radius, trail lifetime, star thresholds, and maze generation remain unchanged. |
| Audio events are logged | Move, orb, final orb, locked exit, level complete, star, UI select, UI back are logged correctly. |
| Toast behavior | One toast at a time, replacement, duration, pause behavior. |
| Level select node states | Locked, unlocked, completed, selected states render correctly. |
| Objective HUD states | `Exit`, `Orbs X/Y`, `Exit Open`, `Exit Locked` display correctly. |
| Trail memory brightness presentation | Trail-only tiles use dimmed presentation without changing logical visibility. |

## Tier 3 tests

| Test | Validates |
| --- | --- |
| Act accent presentation | Act accents do not change gameplay-critical colors or visibility. |
| Reduced motion presentation | Reduced motion classes disable animations and camera lerp without changing timing. |
| Music non-blocking | Music start/stop does not throw and does not affect gameplay timing. |
| Star animation presentation | Star animation timing is presentation-only and respects reduced motion. |

# 10. BUILD ORDER

1. Scaffold files.
   - Create `index.html`, `test.html`, `css/styles.css`, and all JS files.
   - Define `window.FL` and load order.
   - Add basic title screen.

2. Implement deterministic foundations.
   - `FL.config`
   - `FL.rng`
   - `FL.levels`
   - Basic tests for level table and RNG.

3. Implement maze system.
   - Maze representation.
   - BFS.
   - Recursive backtracker.
   - Loop addition.
   - Orb placement.
   - Validation.
   - Fallback builder.
   - Tests for generation and fallback.

4. Implement save and progression.
   - Save load/save/normalize.
   - Unlock rules.
   - Star and best time updates.
   - Settings persistence.

5. Implement core gameplay state.
   - Game state.
   - Screen state machine.
   - Movement.
   - Input buffer.
   - Timer.
   - Trail.
   - Visibility.
   - Objective.
   - Level complete/game complete.

6. Implement input.
   - Keyboard.
   - Gamepad.
   - Touch swipe.
   - Input priority and tests.

7. Implement basic rendering.
   - Canvas sizing.
   - Camera.
   - Fog, floor, walls, trail, orbs, exit, player.
   - Visibility mask.
   - Basic shapes.

8. Implement UI screens.
   - Title.
   - How to Play.
   - Level Select.
   - Gameplay HUD.
   - Pause.
   - Settings.
   - Level Complete.
   - Game Complete.
   - Toasts and hints.

9. Implement audio.
   - Synthesized SFX.
   - Audio logging.
   - Volume settings.
   - Optional Tier 3 music.

10. Implement accessibility.
   - Colorblind palette.
   - Reduced motion.
   - Text size.
   - Focus states.
   - Touch targets.

11. Add polish.
   - Camera lerp.
   - Trail memory brightness.
   - Act accents.
   - Star animation.
   - Background maze lines.
   - Music.

12. Complete tests.
   - Tier 1 required tests.
   - Tier 2 accessibility/audio tests.
   - Tier 3 presentation tests.
   - Full campaign playability test.

# 11. DEFINITION OF DONE

## Tier 1: Core playable campaign

High level: The game is a complete, playable 12-level maze campaign with deterministic mazes, movement, visibility, trail, objective, timer, stars, save, and basic UI.

- [ ] All required files exist.
- [ ] All JS files pass syntax check.
- [ ] `index.html` loads and shows the title screen.
- [ ] `test.html` runs the test suite.
- [ ] `window.__testResults.failed === 0`.
- [ ] Level table contains all 12 levels with correct names, sizes, loops, orbs, min path, par, and 3-star times.
- [ ] All 12 levels generate valid deterministic mazes using normal generation.
- [ ] Fallback generation passes for all 12 levels.
- [ ] Player can move with keyboard, gamepad, and touch.
- [ ] Movement is blocked by walls and bounds.
- [ ] Input buffer works.
- [ ] Holding a direction continues movement.
- [ ] Timer starts on first successful move.
- [ ] Timer pauses and resumes correctly.
- [ ] Light radius visibility is correct.
- [ ] Trail lifetime and fade are correct.
- [ ] Trail remains visible outside light radius until expiry.
- [ ] No persistent memory map exists.
- [ ] Orbs collect automatically.
- [ ] Exit locks/unlocks correctly.
- [ ] Locked exit does not complete level.
- [ ] Level completes on unlocked exit.
- [ ] Stars calculate correctly.
- [ ] Best time updates correctly.
- [ ] Save persists completed levels, stars, best times, settings, and hints.
- [ ] Level select unlocks progression correctly.
- [ ] Title `Play` starts correct level.
- [ ] Pause works.
- [ ] Restart works.
- [ ] Quit mid-level preserves previous save.
- [ ] Level 12 goes to Game Complete.
- [ ] Full campaign test passes from first launch to completion.
- [ ] No fail state exists.
- [ ] No minimap, arrow, persistent memory map, or gameplay-affecting difficulty setting exists.

## Tier 2: Full visual and accessibility spec

High level: The game matches the visual identity, accessibility requirements, synthesized audio, and full UI feedback.

- [ ] Default palette is implemented.
- [ ] Colorblind palette is implemented.
- [ ] Player, orb, exit, trail, walls, and fog use correct shapes.
- [ ] Locked and unlocked exits differ by shape.
- [ ] HUD panels use correct style.
- [ ] Toasts use correct style and behavior.
- [ ] Tutorial hints display correctly.
- [ ] Level select nodes show locked, unlocked, completed, and selected states.
- [ ] Focus states are visible for keyboard and gamepad.
- [ ] Touch targets are at least `48x48px`.
- [ ] Text size setting scales UI correctly.
- [ ] Reduced motion disables required animations.
- [ ] Colorblind mode does not rely on color alone.
- [ ] Accessibility settings do not change light radius, trail lifetime, star times, or maze generation.
- [ ] Synthesized SFX play for all required events.
- [ ] Audio is non-essential and does not crash if unavailable.
- [ ] Audio events are logged.
- [ ] Master, music, and SFX volume settings persist.
- [ ] Trail memory brightness is presentation-only.
- [ ] Camera lerp is implemented and disabled by reduced motion.

## Tier 3: Presentation polish

High level: The game has full atmospheric polish without changing gameplay or fairness.

- [ ] Act accent colors are implemented in level select and optional UI highlights.
- [ ] In-game act tints are implemented.
- [ ] Title and level select backgrounds include faint abstract maze lines.
- [ ] Star pop animation is implemented.
- [ ] Reduced motion replaces star pop with simple fade.
- [ ] Generative ambient music is implemented.
- [ ] Music ducks on toast and pause.
- [ ] Music does not affect gameplay timing or stars.
- [ ] Decorative flourishes do not reveal hidden maze information.

# A. SANITY

| Check | Result |
| --- | --- |
| Checked user request against scope | Valid: browser game about solving mazes is covered by core maze systems, 12-level campaign, and browser build constraints. |
| Checked 3-star time conflict | Valid: level table values are authoritative; 70% formula is fallback only. |
| Checked fallback maze conflict | Valid: deterministic fallback builder supersedes hand-designed fallback data. |
| Checked entity shape conflict | Valid: visual shape language supersedes engineering shape names. |
| Checked audio implementation conflict | Valid: synthesized WebAudio supersedes optional `.wav` files. |
| Checked input setting conflict | Valid: user-facing input row is informational; all inputs remain active; `settings.input` is internal tie-breaker only. |
| Checked volume settings conflict | Valid: master/music/SFX sliders included; separate mute setting dropped. |
| Checked Level 12 flow | Valid: Level 12 goes directly to `gameComplete` with final level stats. |
| Checked camera smoothing | Valid: Tier 1 direct camera; Tier 2 100 ms lerp; reduced motion snaps. |
| Checked star reveal/audio conflict | Valid: visual star animation used; audio plays once per newly earned star. |
| Checked act accents/music tier | Valid: act accents, background lines, star pop, and music are Tier 3 presentation polish. |
| Checked optional SVG snippets | Valid: replaced by normative visual recipe table; dropped as redundant. |
| Checked all gameplay numbers carried | Valid: `140 ms`, `2.5` tiles, `10000 ms` trail, `2000 ms` fade, `1500 ms` toast, `8` corridor limit, `10` generation attempts, orb percentages, separation formula, level table, star times, and movement speed are present. |
| Checked all engineering functions included | Valid: required maze, save, input, render, game, UI, and debug functions are listed. |
| Checked visual palette detail | Valid: default palette, colorblind palette, act accents, in-game themes, type scale, and button styles are carried. |
| Checked state machine | Valid: all screens and transitions are listed. |
| Checked HUD mapping | Valid: HUD elements map to state fields and visibility conditions. |
| Checked debug API coverage | Valid: debug API includes state, lifecycle, input, time, save, generation, gameplay mutation, visibility, HUD, audio, and logs. |
| Checked tests against tiers | Valid: Tier 1 tests prove playable campaign; Tier 2 tests prove visual/accessibility/audio; Tier 3 tests prove polish. |
| Checked definition of done against tiers | Valid: checkboxes align with Tier 1, Tier 2, and Tier 3 goals. |
| Checked dropped features documentation | Valid: dropped items are listed in Section 0.2 with reasons. |
| Checked for unresolved errors | None found. |