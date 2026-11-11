# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| “A lighthouse keeper on a stormy night, swinging the beam to steer ships past the rocks while keeping the lamp fuelled.” | The player is the lighthouse keeper. The player’s cursor aims the lighthouse beam. Ships move across the sea and must be guided through rock barriers into a safe harbor. The lamp fuel runs down and must be refuelled from the lighthouse fuel tank. |
| `dimension: 2d` | One fixed 2D canvas scene, logical size 1280 × 720. |
| `camera: side-on` | The view is a side-on storm cross-section. The vertical screen axis represents sea depth lanes, not vertical elevation. |
| `time model: real-time` | Continuous real-time play using a fixed 60 Hz simulation step. |
| `movement model: no movement, cursor only` | No movable player body. The only in-game input is pointer position. No in-game mouse buttons, keyboard, or touch drag movement. |
| `session shape: single screen` | One fixed screen. No scrolling, no levels, no camera movement. |
| `failure: lose a life` | A ship collision with a rock or a lamp extinguish costs one life. |
| `tone: tense` | Dark storm, fuel clock, increasing ship pressure, screen shake, hit flash, ambient dread audio. |
| `size: one screen, a few minutes` | Standard difficulty is tuned for a skilled run of roughly 2–4 minutes. |
| `win/lose: survive as long as possible` | No win state. The run ends when lives reach 0. Score is ships saved and time survived. |
| `core mechanics: upkeep` | Fuel gauge decays. The player must hold the cursor over the lighthouse fuel tank to transfer fuel. |
| `core mechanics: multitasking` | The player must choose between refuelling and guiding multiple ships. Every unattended ship worsens by drifting toward an upcoming rock lane. |
| `core mechanics: escort` | Ships enter from the right and must be guided through three rock barriers to the safe harbor at the left. |
| `supporting mechanics: none` | No upgrades, powerups, enemies, traps, pickups, score modifiers, unlocks, or secondary systems. |
| `extra mechanics: none` | No extra mechanics are added. |
| `art style: hand-drawn / painterly: brush strokes, ink lines or watercolour texture` | All rendering is procedural painterly: soft gradients, noise, ink outlines, brush-like spray, watercolour sea washes. |
| `palette: dark: mostly black with a few bright accents` | Near-black storm palette with amber beam, pale ship silhouettes, cyan safe harbor, white/magenta danger accents. |
| `typography: hand-lettered: drawn, irregular letters` | UI uses a hand-lettered font stack and slight irregular rotation. |
| `music: ambient: slow textures, no strong beat` | Continuous synthesized low drones and filtered noise, no percussive beat. |
| `sound effects style: realistic: recorded-sounding impacts and foley` | Synthesized sounds are designed as foley-like: wood cracks, oil flow, wave wash, metal clicks, low impacts. |
| `screens: title, game over` | Title state and game-over state. No pause state. |
| `hud: none` | No HUD overlay. All in-game state is diegetic: lamp flame, fuel tank oil level, life oil cans, ship and rock states. |
| `effects: screen shake, particles, hit flash, trails, bloom` | Implemented as canvas effects with reduced-motion support. |
| `accessibility: colour-blind safe palette, reduced motion, difficulty options` | Default palette avoids red/green reliance. Reduced-motion toggle disables shake, particles, trails, bloom. Difficulty presets are Calm, Standard, Gale. |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| Game prompt | Final: lighthouse keeper, beam steering, rocks, lamp fuel. | Direct user request. |
| 2D | Final: canvas 2D. | Direct user request. |
| Side-on camera | Final: side-on cross-section. Vertical screen position is treated as sea depth lanes for gameplay clarity. | Preserves side-on framing while making “steer past rocks” readable in one screen. |
| Real-time | Final: continuous real-time. | Direct user request. |
| No movement, cursor only | Final: pointer position only. In-game refuel is hover over the fuel tank. No in-game clicks. | Direct user request and keeps input simple. |
| Single screen | Final: one fixed canvas. | Direct user request. |
| Failure loses a life | Final: lives are a resource. | Direct user request. |
| Lives count | Standard: 3. Calm: 5. Gale: 2. | Gives accessible difficulty options without adding mechanics. |
| Tone | Final: tense. | Direct user request. |
| Session length | Final: one screen, few minutes. | Direct user request. |
| Win/lose | Final: no win. Survive as long as possible. | Direct user request. |
| Upkeep mechanic | Final: lamp fuel decays; player refuels by hovering cursor on fuel tank. | Direct core mechanic. |
| Multitasking mechanic | Final: jobs are refuel and guide multiple ships. Each worsens when unattended. | Direct core mechanic. |
| Escort mechanic | Final: guide ships from right edge to safe harbor at left through rock barriers. | Direct core mechanic. |
| Supporting mechanics | Final: none. | User decision. |
| Extra mechanics | Final: none. | User decision. |
| Art style | Final: procedural hand-drawn painterly canvas rendering. | User decision. |
| Palette | Final: dark near-black with amber, cyan, pale grey, white/magenta accents. | User decision. |
| Color-blind safety | Final: no red/green critical encoding. Use shape, brightness, outline, position. | User decision. |
| Typography | Final: hand-lettered CSS font stack, irregular rotation. | User decision. |
| Music | Final: ambient low drones and noise textures. | User decision. |
| Sound effects | Final: synthesized foley-like sounds. | User decision. |
| Screens | Final: title and game over only. | User decision. |
| HUD | Final: no HUD overlay. | User decision. |
| Effects | Final: screen shake, particles, hit flash, trails, bloom. | User decision. |
| Reduced motion | Final: toggle. Default follows OS preference. Disables shake, particles, trails, bloom, flicker. | User decision. |
| Difficulty options | Final: Calm, Standard, Gale. | User decision. |
| Logical resolution | Final: 1280 × 720 logical canvas. CSS scales to viewport while preserving aspect ratio. | Fixed single-screen design needs stable coordinates. |
| Coordinate axes | Final: x increases right, y increases down. | Standard 2D canvas convention. |
| Game phases | Final: `title`, `playing`, `gameOver`. No pause. | Session is real-time single screen. |
| Fixed timestep | Final: 1/60 s. Render after accumulator. | Deterministic tests and stable physics. |
| RNG | Final: seeded xorshift32. No `Math.random()` in gameplay. | Reproducible tests and debug. |
| Player identity | Final: the player is the lighthouse keeper. No movable avatar. The lighthouse, lamp, and fuel tank are the player’s body. A small non-interactive keeper silhouette may appear for atmosphere. | Direct prompt and no-movement constraint. |
| Enemies | Final: none. | No enemies in prompt; supporting/extra none. |
| Traps | Final: none. | No traps in prompt; supporting/extra none. |
| Pickups | Final: none. | Fuel is a fixed lighthouse tank, not a pickup. |
| Hazards | Final: three fixed rock barriers across the sea. | Required by “past the rocks.” |
| Sea lanes | Final: five lane centers at y = 320, 400, 480, 560, 640. | Makes “steer past rocks” concrete and testable in one screen. |
| Rock barriers | Final: R1 x=1000–1060, R2 x=720–780, R3 x=440–500 with safe/rock lane patterns. | Creates a repeating escort path and increasing pressure. |
| Ship spawn | Final: ships spawn at x=1280 in a lane safe for the first barrier. | Prevents unavoidable first-barrier deaths. |
| Ship goal | Final: save ship when x < 180. | Safe harbor behind lighthouse. |
| Beam input | Final: cursor angle from lamp origin selects beam direction. | Matches “swinging the beam.” |
| Beam guidance | Final: a ship is guided if inside the beam cone. Its target lane is the lane nearest the beam line at its x position. | Cursor-only guidance with no extra input. |
| Unlit ship behavior | Final: unlit ships drift toward the nearest rock lane of the next upcoming barrier. If none, drift toward center safe lane. | Makes escort pressure explicit and testable. |
| Refuel input | Final: hover pointer inside fuel tank rectangle. Beam disabled while hovering. | Cursor-only, creates multitasking. |
| Fuel tank position | Final: rect x=40, y=430, width=120, height=220. | Left lighthouse base, away from sea guidance area. |
| Lamp origin | Final: x=110, y=180. | Side-on lighthouse lamp. |
| Beam cone | Final: normal half-angle 6°. Low fuel shrinks to 2°. | Makes low fuel visually and mechanically meaningful. |
| Fuel start | Final: 100%. | Standard resource gauge. |
| Fuel drain | Final: base 1.4%/s plus 0.35%/s per guided ship, multiplied by stage/difficulty. | Tense upkeep without impossible drain. |
| Refuel rate | Final: 14%/s. | Fast enough to recover, slow enough to create multitasking. |
| Low fuel | Final: below 35% beam narrows; below 15% flicker/warning. | Visible and mechanical pressure. |
| Lamp out | Final: fuel 0 causes life loss, lamp relights at 20% after 1.5 s disabled. | Failure loses a life, run continues. |
| Score | Final: `finalScore = shipsSaved * 100 + floor(timeSurvived)`. | “Survive as long as possible” without in-run HUD. |
| Game over | Final: lives <= 0. Show game over screen. | Required. |
| Difficulty presets | Final: Calm, Standard, Gale. | Required. |
| Accessibility | Final: color-blind safe palette default, reduced-motion toggle, difficulty options. | Required. |
| No HUD | Final: no DOM HUD during play. | Required. |
| Diegetic state indicators | Final: fuel tank oil level, lamp flame size, life oil cans, ship guided outline, rock outlines. | Communicates state without HUD. |

## 0.3 Tiers

| Tier | Segment | Contents | Notes |
| --- | --- | --- | --- |
| Tier 1 | Core playable game | Title, Standard run, lamp fuel upkeep, cursor beam, ship guidance, rock barriers, collision, lives, game over, diegetic state, required dark painterly art, ambient audio, required effects, no HUD, default color-blind safe palette, basic reduced-motion handling. | Must be finished and fun before higher tiers. |
| Tier 2 | Required settings expansion | Calm, Standard, Gale difficulty presets. Explicit reduced-motion toggle. Settings UI on title. | Adds no new mechanics. Required for full accessibility/difficulty decision. |
| Tier 3 | None | No supporting or extra mechanics. | Do not add systems beyond Tier 2. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Value | Number |
| --- | --- |
| Logical canvas width | 1280 px |
| Logical canvas height | 720 px |
| Simulation timestep | 1/60 s |
| Time unit | seconds |
| Position unit | logical pixels |
| Speed unit | pixels/second |
| Fuel unit | percent, 0–100 |
| Angle unit | degrees |
| x axis | positive right |
| y axis | positive down |
| Lamp origin | x=110, y=180 |
| Fuel tank rect | x=40, y=430, w=120, h=220 |
| Sea lane centers | L0=320, L1=400, L2=480, L3=560, L4=640 |
| Lane spacing | 80 px |
| Ship collision box | width 36 px, height 18 px |
| Rock lane collision height | 60 px centered on lane center |
| Safe harbor trigger | x < 180 |
| Ship spawn x | 1280 |
| Beam maximum length | 1200 px |

## 1.2 Important conventions

| Convention | Rule |
| --- | --- |
| Fixed step loop | `accumulator += deltaTime`; while `accumulator >= 1/60`, call `update(1/60)`. Render once per animation frame. |
| No pause | There is no pause phase. |
| No HUD | No DOM elements overlay the canvas during `playing`. |
| Deterministic RNG | Use `GAME.rng.next()` only. Seed is stored in `GAME.seed`. |
| No `Math.random()` | Gameplay randomness must be seeded. |
| Settings | `GAME.settings` is the single source of truth for difficulty and accessibility. |
| Color encoding | Critical state must not rely only on color. Use shape, outline, position, or animation. |
| Reduced motion | When `settings.reducedMotion` is true, disable screen shake, particles, trails, bloom, flicker, and large flash effects. |
| Canvas scaling | Canvas CSS may scale, but all game logic uses logical coordinates. |
| Pointer input | Pointer events are converted to logical canvas coordinates. If pointer leaves canvas, keep last valid pointer position. |
| No in-game buttons | Title and game-over buttons are DOM UI. Gameplay has no click input. |
| No extra systems | Do not add enemies, traps, pickups, upgrades, or secondary resources. |

# 2. CONTRACTS

## 2.1 Module layout

| Module | Purpose | Tier |
| --- | --- | --- |
| `index.html` | Canvas, title screen, game-over screen, settings controls. | Tier 1 |
| `css/style.css` | Dark theme, hand-lettered typography, screen state machine, accessibility styles. | Tier 1 |
| `js/main.js` | Boot, fixed-step loop, phase control, render call. | Tier 1 |
| `js/records.js` | Record factories and shape validation. | Tier 1 |
| `js/rng.js` | Seeded xorshift32 RNG. | Tier 1 |
| `js/settings.js` | Difficulty presets, reduced-motion setting, color-blind safe palette flag. | Tier 1/2 |
| `js/input.js` | Pointer/touch to logical cursor coordinates. | Tier 1 |
| `js/game.js` | Run state, stage progression, lives, score, game over. | Tier 1 |
| `js/upkeep.js` | Lamp fuel, refuel, lamp out. | Tier 1 |
| `js/escort.js` | Ship spawn, movement, guidance, save, destroy. | Tier 1 |
| `js/multitasking.js` | Job pressure metrics and coordination state. | Tier 1 |
| `js/rocks.js` | Barrier data, upcoming barrier lookup, rock lane lookup. | Tier 1 |
| `js/collision.js` | Ship/rock collision and safe harbor checks. | Tier 1 |
| `js/render.js` | Painterly canvas rendering, effects, diegetic state. | Tier 1 |
| `js/audio.js` | Synthesized ambient audio and foley. | Tier 1 |
| `js/ui.js` | Title and game-over DOM screens. | Tier 1/2 |
| `js/debug.js` | Debug API for tests and inspection. | Tier 1 |

## 2.2 Global context

The global context must contain every field used by gameplay systems and tests.

```js
window.GAME = {
  phase: "title" | "playing" | "gameOver",
  frame: number,
  time: number,
  seed: number,
  rng: {
    next: function() -> number 0..1
  },
  settings: {
    difficulty: "calm" | "standard" | "gale",
    reducedMotion: boolean,
    colorBlindSafe: true
  },
  input: {
    x: number,
    y: number,
    aimX: number,
    aimY: number,
    insideFuelTank: boolean
  },
  lamp: {
    fuel: number,
    active: boolean,
    halfAngle: number,
    outTimer: number,
    lowWarn: boolean
  },
  stage: {
    index: number,
    nextSpawn: number,
    maxActive: number,
    speedMult: number,
    fuelMult: number
  },
  lives: number,
  score: {
    saved: number,
    timeSurvived: number,
    finalScore: number
  },
  ships: Array<ShipRecord>,
  barriers: Array<BarrierRecord>,
  particles: Array<ParticleRecord>,
  effects: {
    shakeAmount: number,
    shakeTimer: number,
    hitFlash: number
  }
};
```

Record shapes:

```js
ShipRecord = {
  id: number,
  x: number,
  y: number,
  vx: number,
  targetLane: number,
  state: "active" | "saved" | "destroyed",
  bobPhase: number,
  guided: boolean,
  spawnTime: number
}

BarrierRecord = {
  id: number,
  xStart: number,
  xEnd: number,
  safeLanes: number[],
  rockLanes: number[]
}

ParticleRecord = {
  x: number,
  y: number,
  vx: number,
  vy: number,
  ttl: number,
  life: number,
  kind: "oil" | "spark" | "spray" | "wake"
}
```

## 2.3 Module specifics

| Module | Required functions | Tier |
| --- | --- | --- |
| `main.js` | `boot()`, `startGame()`, `loop(timestamp)`, `update(dt)`, `render()`, `setPhase(phase)` | Tier 1 |
| `records.js` | `createShip(id, lane)`, `createBarriers()`, `createParticle(kind, x, y)`, `validateContext()` | Tier 1 |
| `rng.js` | `createRng(seed)`, `next(rng)`, `nextInt(rng, min, max)`, `nextFloat(rng, min, max)` | Tier 1 |
| `settings.js` | `getSettings()`, `setDifficulty(id)`, `setReducedMotion(value)`, `applyOsReducedMotion()` | Tier 1/2 |
| `input.js` | `attachPointer(canvas)`, `updateInput()`, `getCursor()`, `isInsideFuelTank(x, y)` | Tier 1 |
| `game.js` | `startRun()`, `updateGame(dt)`, `updateStage()`, `loseLife(reason)`, `endRun()`, `addScoreShip()`, `getScore()` | Tier 1 |
| `upkeep.js` | `updateLamp(dt)`, `refuel(dt)`, `setFuel(value)`, `getFuel()`, `isLowFuel()`, `lampOut()`, `getState()` | Tier 1 |
| `escort.js` | `trySpawn(dt)`, `updateShips(dt)`, `setTargetLane(ship, lane)`, `saveShip(ship)`, `destroyShip(ship)`, `getState()` | Tier 1 |
| `multitasking.js` | `updateJobs(dt)`, `getActiveJobCount()`, `getJobPressure()`, `getState()` | Tier 1 |
| `rocks.js` | `getBarriers()`, `getUpcomingBarrier(ship)`, `getNearestRockLane(ship)`, `isRockLane(barrier, lane)` | Tier 1 |
| `collision.js` | `checkShipAgainstBarriers(ship)`, `checkShipSafe(ship)`, `checkAllShips()` | Tier 1 |
| `render.js` | `render(ctx)`, `drawLighthouse()`, `drawBeam()`, `drawSea()`, `drawShips()`, `drawRocks()`, `drawParticles()`, `applyEffects()` | Tier 1 |
| `audio.js` | `initAudio()`, `startMusic()`, `stopMusic()`, `play(name)`, `setBeamHum(active, intensity)` | Tier 1 |
| `ui.js` | `bindUi()`, `showTitle()`, `showGameOver()`, `setPhaseDom(phase)` | Tier 1/2 |
| `debug.js` | `install()`, `upkeep()`, `escort()`, `multitasking()`, `input.setPointer(x, y)`, `game.setLives(n)`, `game.setTime(t)` | Tier 1 |

# 3. VISUAL SPEC

The game is a dark, hand-drawn storm at night. The lighthouse is a black silhouette on the left, lit only by its own amber lamp. The sea is painted in horizontal watercolour bands of near-black and deep blue. The beam is the brightest object: a warm amber cone with dust particles and soft bloom. Ships are pale, simple silhouettes with ink outlines. Rocks are jagged dark shapes outlined in pale ink so they remain readable without color. The screen is mostly black with a few bright accents: amber lamp, cyan safe harbor, pale ships, white/magenta danger flashes.

Lighting and atmosphere:

- The only strong light source is the lighthouse beam.
- The beam casts soft bloom and illuminates rain and sea spray.
- The sea is dark and layered; far sea is darker, near sea is slightly lighter.
- Rain is drawn as thin low-alpha streaks, not gameplay objects.
- The lamp flame flickers when fuel is low.
- The fuel tank has a visible oil level.
- Three small oil-can shapes represent lives.
- Safe harbor has a cyan guide glow at the left edge.

Space:

- Lighthouse occupies x 40–220.
- Lamp origin is at x=110, y=180.
- Fuel tank is at x=40, y=430, w=120, h=220.
- Safe harbor glow begins at x < 180.
- Sea spans x 220–1280.
- Sea lanes are drawn as depth bands centered at y=320, 400, 480, 560, 640.
- Rock barriers are jagged dark obstacles across those bands.

| Element | Color | Stroke / Texture | Motion | Tier |
| --- | --- | --- | --- | --- |
| Void background | `#05070a` | Soft cloud noise | Very slow cloud drift | Tier 1 |
| Storm clouds | `#0b1420` | Watercolour washes | Slow horizontal drift | Tier 1 |
| Far sea | `#0a1420` | Horizontal noise strokes | Low parallax drift | Tier 1 |
| Mid sea | `#0f1c2a` | Brush strokes, foam flecks | Medium parallax drift | Tier 1 |
| Near sea | `#142a3a` | Larger brush strokes | Higher parallax drift | Tier 1 |
| Foam | `#718a99` at 10–25% alpha | Broken line particles | Drifts with wave bands | Tier 1 |
| Lighthouse body | `#05070a` | Thick ink outline `#d7e1ea` at low alpha | Static | Tier 1 |
| Lamp flame | `#ffb703` core, `#ffd166` glow | Radial gradient, flicker | Flicker amplitude increases when low fuel | Tier 1 |
| Beam core | `#fff3c4` | Soft cone gradient | Follows cursor instantly | Tier 1 |
| Beam glow | `#ffd166` at 18–35% alpha | Bloom, dust particles | Sweeps with cursor | Tier 1 |
| Fuel tank | `#080b10` | Glass-like rectangle, visible oil level | Oil level matches `lamp.fuel` | Tier 1 |
| Oil pour particles | `#ffb703` | Small droplets | Spawn while refuelling | Tier 1 |
| Ships | `#cfd8dd` hull, `#ffffff` outline | Simple silhouette, ink edge | Bob, turn, wake trail | Tier 1 |
| Guided ship highlight | `#ffffff` outline pulse | Thin outline | Pulse only while beam-guided | Tier 1 |
| Rocks | `#1d2a36` | Jagged ink outline `#d7e1ea` | Static | Tier 1 |
| Safe harbor | `#7ce7c4` at 15–25% alpha | Soft vertical glow | Gentle pulse | Tier 1 |
| Life oil cans | `#ffd166` when alive, `#1d2a36` when lost | Small can silhouette | Extinguish on life loss | Tier 1 |
| Hit flash | `#ffffff` to `#ff66c4` | Full-screen low-alpha flash | Short burst on life loss | Tier 1 |
| Reduced motion | same palette | Static flame, no particles, no bloom, no shake | No motion effects | Tier 1 |

# 4. GAMEPLAY SPEC

The player is a lighthouse keeper whose only direct control is the cursor. The cursor aims the lighthouse beam. Ships enter from the right and move left through three rock barriers. A ship inside the beam is guided toward the lane nearest the beam line. A ship outside the beam drifts toward an upcoming rock lane. The lamp fuel drains constantly and drains faster while guiding ships. The player must periodically move the cursor into the lighthouse fuel tank to refuel, but while refuelling the beam cannot guide ships. The run continues until three lives are lost. Each life is lost when a ship collides with a rock or the lamp extinguishes. The score is ships saved plus time survived.

## 4.1 Content roster

| Entity | Count | Key numbers | Tier |
| --- | --- | --- | --- |
| Lighthouse keeper | 1 non-movable conceptual identity | No player body. Cursor represents keeper aim. | Tier 1 |
| Lighthouse | 1 | Lamp origin x=110, y=180. Fuel tank x=40, y=430, w=120, h=220. | Tier 1 |
| Distressed ship | Dynamic | Spawn max active depends on stage. Base speed 48 px/s. Base turn rate 110 px/s. Save at x < 180. | Tier 1 |
| Rock barrier | 3 | R1 x=1000–1060, R2 x=720–780, R3 x=440–500. | Tier 1 |
| Sea lanes | 5 | y centers 320, 400, 480, 560, 640. | Tier 1 |
| Life tokens | 3 default | Standard lives 3. Calm 5. Gale 2. | Tier 1/2 |
| Enemies | 0 | None. | Tier 1 |
| Traps | 0 | None. | Tier 1 |
| Pickups | 0 | None. | Tier 1 |

## 4.2 Input model — Tier 1

| Input | Rule |
| --- | --- |
| Pointer move | Updates `GAME.input.x` and `GAME.input.y` in logical canvas coordinates. |
| Touch move | Same as pointer move. |
| Pointer leave canvas | Keep last valid pointer position. |
| In-game click | No effect. |
| Keyboard | No effect during gameplay. |
| Fuel tank hover | If `input.x >= 40 && input.x <= 160 && input.y >= 430 && input.y <= 650`, set `input.insideFuelTank = true`. |
| Beam aim | If not inside fuel tank, beam aims at clamped point: `aimX = clamp(input.x, 130, 1270)`, `aimY = clamp(input.y, 280, 700)`. |
| Beam disabled | Beam is disabled if `lamp.fuel <= 0`, `lamp.outTimer > 0`, or `input.insideFuelTank` is true. |

## 4.3 Lamp and fuel upkeep — Tier 1

| Parameter | Value |
| --- | --- |
| Starting fuel | 100 |
| Max fuel | 100 |
| Base drain | 1.4%/s |
| Guided ship drain | 0.35%/s per guided ship |
| Stage fuel multiplier | From stage table |
| Difficulty fuel multiplier | Calm 0.70, Standard 1.00, Gale 1.40 |
| Refuel rate | 14%/s while cursor is inside fuel tank and lamp is not disabled |
| Low fuel threshold | 35 |
| Warning threshold | 15 |
| Lamp out reset fuel | 20 |
| Lamp out disabled time | 1.5 s |
| Refuel during lamp out | Disabled |
| Fuel drain during lamp out | Disabled |

Rules:

1. Fuel decreases every simulation step:
   ```js
   drain = (1.4 + 0.35 * guidedShipCount) * stageFuelMult * difficultyFuelMult;
   lamp.fuel -= drain * dt;
   ```
2. If cursor is inside fuel tank and lamp is not disabled:
   ```js
   lamp.fuel = min(100, lamp.fuel + 14 * dt);
   ```
3. If `lamp.fuel < 35`, beam half-angle shrinks:
   ```js
   halfAngle = 2 + (lamp.fuel / 35) * 4;
   ```
4. If `lamp.fuel < 15`, lamp flickers and warning audio plays.
5. If `lamp.fuel <= 0`, call `lampOut()`:
   - lose one life;
   - set `lamp.fuel = 20`;
   - set `lamp.outTimer = 1.5`;
   - disable beam;
   - play lamp-out sound.
6. While `lamp.outTimer > 0`, fuel does not drain and refuel is disabled.
7. When `lamp.outTimer` reaches 0, lamp becomes active again if `lamp.fuel > 0`.

## 4.4 Beam and ship guidance — Tier 1

| Parameter | Value |
| --- | --- |
| Beam origin | x=110, y=180 |
| Beam length | 1200 px |
| Normal beam half-angle | 6° |
| Minimum low-fuel half-angle | 2° |
| Beam angle | `atan2(aimY - lamp.y, aimX - lamp.x)` |
| Ship lit test | Angular difference between beam angle and ship position <= current half-angle |
| Target lane when lit | Lane center nearest to beam line at ship x |
| Lane tie-break | Choose lower lane index |
| Unlit target lane | Nearest rock lane of next upcoming barrier |
| No upcoming barrier target lane | Lane 2 |

Beam line calculation:

```js
lineYAtShip = lamp.y + (ship.x - lamp.x) * tan(beamAngle);
targetLane = nearestLane(lineYAtShip);
```

Lane centers:

```js
LANE_Y = [320, 400, 480, 560, 640];
```

Guided ship rules:

1. If a ship is inside the beam cone, set `ship.guided = true`.
2. Set `ship.targetLane` to nearest lane to the beam line at `ship.x`.
3. While guided, ship drift toward rock lanes is suppressed.
4. Visual guided outline pulses.
5. A single beam can guide multiple ships if all are inside the cone.

Unlit ship rules:

1. If a ship is not inside the beam cone, set `ship.guided = false`.
2. Find the next upcoming barrier:
   - barrier with the largest `xStart` such that `xStart < ship.x - 80`;
   - if none, target lane 2.
3. If a barrier exists, choose the rock lane in that barrier whose lane center is closest to `ship.y`.
4. Tie-break by lower lane index.
5. Set `ship.targetLane` to that lane.

## 4.5 Escort and hazards — Tier 1

Barrier roster:

| Barrier | xStart | xEnd | Safe lanes | Rock lanes |
| --- | --- | --- | --- | --- |
| R1 | 1000 | 1060 | 1, 3 | 0, 2, 4 |
| R2 | 720 | 780 | 0, 4 | 1, 2, 3 |
| R3 | 440 | 500 | 2 | 0, 1, 3, 4 |

Ship movement:

| Parameter | Value |
| --- | --- |
| Base ship speed | 48 px/s |
| Stage speed multiplier | From stage table |
| Difficulty speed multiplier | Calm 0.75, Standard 1.00, Gale 1.30 |
| Base turn rate | 110 px/s |
| Calm turn rate | 90 px/s |
| Gale turn rate | 130 px/s |
| Ship collision half-width | 18 px |
| Rock lane collision half-height | 30 px |
| Save trigger | x < 180 |

Rules:

1. Ship x decreases:
   ```js
   speed = 48 * stageSpeedMult * difficultySpeedMult;
   ship.x -= speed * dt;
   ```
2. Ship y moves toward `LANE_Y[ship.targetLane]`:
   ```js
   turnRate = baseTurnRate * difficultyTurnMult;
   diff = targetY - ship.y;
   ship.y += clamp(diff, -turnRate * dt, turnRate * dt);
   ```
3. Collision:
   - if `ship.x + 18 > barrier.xStart` and `ship.x - 18 < barrier.xEnd`;
   - and `abs(ship.y - LANE_Y[rockLane]) <= 30` for any rock lane;
   - then ship is destroyed and one life is lost.
4. Save:
   - if `ship.x < 180` and not collided, ship is saved;
   - increment `score.saved`;
   - remove ship.
5. Ship-ship collisions are ignored.
6. Ship visual bob is cosmetic only and does not affect collision.

## 4.6 Multitasking and run progression — Tier 1

Jobs presented to the player:

| Job | How it worsens | Player response |
| --- | --- | --- |
| Fuel lamp | Fuel drains constantly; guided ships drain faster. | Move cursor into fuel tank. |
| Ship guidance | Unlit ships target upcoming rock lanes. | Move cursor to aim beam at safe lanes. |
| Multiple ships | Spawn pressure increases with time. | Sweep cursor between ships or accept losses. |

There is no separate multitasking input. The player’s cursor choice is the multitasking decision.

Spawn rules:

| Parameter | Value |
| --- | --- |
| First spawn delay | 6.0 s |
| Spawn position | x=1280 |
| Spawn lane | Randomly chosen from R1 safe lanes `[1, 3]` |
| Spawn blocked | If active ship count >= `stage.maxActive` |
| Random source | Seeded RNG only |

Standard stage progression:

| Stage | Time range | Spawn interval | Max active | Speed multiplier | Fuel multiplier |
| --- | --- | --- | --- | --- | --- |
| 0 | 0–29 s | 6.00 s | 2 | 1.00 | 1.00 |
| 1 | 30–59 s | 5.24 s | 3 | 1.08 | 1.05 |
| 2 | 60–89 s | 4.48 s | 4 | 1.16 | 1.10 |
| 3 | 90–119 s | 3.72 s | 5 | 1.24 | 1.15 |
| 4 | 120–149 s | 2.96 s | 5 | 1.32 | 1.20 |
| 5+ | 150+ s | 2.20 s | 5 | 1.35 | 1.25 |

Stage formula:

```js
stageIndex = floor(time / 30);
spawnInterval = max(2.20, 6.00 - stageIndex * 0.76);
maxActive = min(5, 2 + stageIndex);
speedMult = 1 + min(0.35, stageIndex * 0.07);
fuelMult = 1 + min(0.25, stageIndex * 0.05);
```

## 4.7 Failure, score, and game over — Tier 1

| Event | Effect |
| --- | --- |
| Ship collides with rock | Remove ship, lose 1 life, hit flash, screen shake, impact sound. |
| Lamp extinguishes | Lose 1 life, lamp relights at 20% after 1.5 s disabled. |
| Lives <= 0 | End run. |
| Ship reaches safe harbor | Ship saved, `score.saved += 1`. |
| Time passes | `score.timeSurvived = time`. |
| Final score | `score.saved * 100 + floor(score.timeSurvived)`. |

Game over screen shows:

- ships saved;
- time survived;
- final score;
- restart button;
- return to title button.

No score is shown during gameplay because HUD is none.

## 4.8 Difficulty options — Tier 2

| Setting | Calm | Standard | Gale |
| --- | --- | --- | --- |
| Stage interval | 40 s | 30 s | 20 s |
| Starting spawn interval | 9.0 s | 6.0 s | 4.5 s |
| Minimum spawn interval | 4.0 s | 2.2 s | 1.8 s |
| Spawn decay per stage | 1.0 s | 0.76 s | 0.54 s |
| Max active cap | 3 | 5 | 7 |
| Ship speed multiplier | 0.75 | 1.00 | 1.30 |
| Turn rate | 90 px/s | 110 px/s | 130 px/s |
| Fuel decay multiplier | 0.70 | 1.00 | 1.40 |
| Lives | 5 | 3 | 2 |

Stage formulas per difficulty:

```js
stageIndex = floor(time / stageInterval);
spawnInterval = max(spawnMin, spawnBase - stageIndex * spawnDecay);
maxActive = min(maxActiveCap, 2 + stageIndex);
speedMult = difficultySpeedMult * (1 + min(0.35, stageIndex * 0.07));
fuelMult = difficultyFuelMult * (1 + min(0.25, stageIndex * 0.05));
```

## 4.9 Feel and tuning targets

| Target | Value |
| --- | --- |
| First danger | First ship reaches first barrier around 6–8 s after spawn. |
| First refuel pressure | Low fuel warning around 45–70 s without refuelling. |
| Standard skilled survival | 2–4 minutes. |
| Calm skilled survival | 4–7 minutes. |
| Gale skilled survival | 1–2 minutes. |
| Tension source | Cursor must leave sea to refuel, but leaving sea lets ships drift into rocks. |
| Recovery source | Refuel restores fuel quickly, but only if the player accepts temporary guidance loss. |

# 5. CHARACTERS

| Entity | Silhouette | Facing | States gameplay needs | Animations by name | Motion rules |
| --- | --- | --- | --- | --- | --- |
| Lighthouse keeper atmosphere figure | Small black silhouette inside lamp gallery. | Right | `idle`, `refuel_hand`, `relight_hand` | `idle_sway`, `refuel_hand`, `relight_hand` | `idle_sway`: vertical offset `sin(time * 0.2Hz) * 1px`. `refuel_hand`: a hand silhouette appears at fuel tank while refuelling. `relight_hand`: a hand silhouette flashes at lamp for 0.4 s after lamp out. Non-interactive. |
| Lighthouse | Tall dark tower, lamp room, fuel tank, life oil cans. | Faces sea to the right | `lamp_lit`, `lamp_low`, `lamp_out`, `lives_remaining` | `lamp_flicker`, `fuel_level`, `life_can_extinguish` | Flicker amplitude 0 normal, 6–12% when fuel < 35, 12–20% when fuel < 15. Fuel level matches `lamp.fuel`. Life cans extinguish when lives decrease. |
| Distressed ship | Small hull silhouette with mast. | Left, because it moves left | `active`, `guided`, `saved`, `destroyed` | `ship_bob`, `ship_creak`, `ship_turn`, `ship_wake`, `ship_impact` | `ship_bob`: cosmetic y offset `sin(bobPhase) * 3px`, `bobPhase += 0.8Hz * dt`. `ship_creak`: rotation `sin(time * 0.5Hz) * 1°`. `ship_turn`: actual y movement governed by gameplay. `ship_wake`: low-alpha particles behind ship. `ship_impact`: sparks and hull break silhouette on collision. |
| Rocks | Jagged dark rock shapes across sea lanes. | Static | `static` | `none` | Static. Outlined with pale ink so they remain visible in dark palette. |

# 6. AUDIO

| Sound name | Recipe | Plays when | Tier |
| --- | --- | --- | --- |
| `ambient_music` | Two detuned sine pads at 55 Hz and 82.5 Hz, slow LFO amplitude, filtered noise bed, no beat. | Title, playing, game over until dismissed. | Tier 1 |
| `storm_drone` | Brown noise through lowpass 180 Hz, slow gain modulation. | Continuous during playing. | Tier 1 |
| `wave_wash` | Bandpassed noise 200–600 Hz, envelope 1.2 s, random interval 4–7 s. | Random during playing. | Tier 1 |
| `wind_gust` | Noise bandpass 800–2000 Hz, slow LFO, random 6–12 s. | Random during playing. | Tier 1 |
| `thunder` | Sine 60 Hz descending to 35 Hz plus low rumble noise, duration 1.2 s. | Random every 20–40 s, disabled or softened when reduced motion. | Tier 1 |
| `beam_hum` | Sine 180 Hz + 220 Hz, volume proportional to beam active and fuel, pitch drops below 35 fuel. | While beam active. | Tier 1 |
| `lamp_flicker` | Short high-pass noise crackles. | When fuel < 15 or lamp low. | Tier 1 |
| `fuel_flow` | Filtered noise 300–900 Hz, gated envelope. | While cursor is in fuel tank and refuelling. | Tier 1 |
| `fuel_click` | Short impulse click, sine 1200 Hz transient. | When refuel starts or stops. | Tier 1 |
| `lamp_out` | Descending sine 440 Hz to 80 Hz, filtered noise burst. | Lamp fuel reaches 0. | Tier 1 |
| `lamp_relight` | Noise burst plus sine 600 Hz to 200 Hz, metallic click. | After lamp out timer finishes. | Tier 1 |
| `ship_creak` | Low wood noise, bandpass 200–800 Hz, short envelope. | When ship is within 120 px of an upcoming rock barrier. | Tier 1 |
| `rock_impact` | Low sine 60 Hz thud plus wood crack noise. | Ship collides with rock. | Tier 1 |
| `life_lost` | Low bell-like sine 110 Hz with short noise decay. | Any life loss. | Tier 1 |
| `game_over` | Minor descending bell tones 220, 174, 130 Hz, long decay. | Lives reach 0. | Tier 1 |

# 7. UX

The UI is HTML and CSS only. The game canvas has no HUD. The phase is controlled by `body[data-phase]`.

State machine:

| Phase | Entry | Exit |
| --- | --- | --- |
| `title` | Initial load or return from game over. | Start button pressed. |
| `playing` | Start button pressed. | Lives reach 0. |
| `gameOver` | Lives reach 0. | Restart button returns to `playing`; title button returns to `title`. |

HTML structure:

```html
<body data-phase="title">
  <canvas id="game"></canvas>
  <section id="title" class="screen">
    <h1>Keep the Lamp Lit</h1>
    <button id="start">Begin the Watch</button>
    <fieldset>
      <legend>Difficulty</legend>
      <label><input type="radio" name="difficulty" value="calm">Calm</label>
      <label><input type="radio" name="difficulty" value="standard" checked>Standard</label>
      <label><input type="radio" name="difficulty" value="gale">Gale</label>
    </fieldset>
    <label><input type="checkbox" id="reducedMotion">Reduced Motion</label>
  </section>
  <section id="gameOver" class="screen">
    <h2>The Lamp Went Dark</h2>
    <p id="finalScore"></p>
    <p id="shipsSaved"></p>
    <p id="timeSurvived"></p>
    <button id="restart">Take Another Watch</button>
    <button id="toTitle">Return to Title</button>
  </section>
</body>
```

CSS state machine:

```css
body[data-phase="title"] #title { display: block; }
body[data-phase="title"] #gameOver { display: none; }

body[data-phase="playing"] #title { display: none; }
body[data-phase="playing"] #gameOver { display: none; }

body[data-phase="gameOver"] #title { display: none; }
body[data-phase="gameOver"] #gameOver { display: block; }
```

Hand-lettered typography:

```css
body {
  background: #05070a;
  color: #f2f7fb;
  font-family: "Segoe Print", "Bradley Hand", "Comic Sans MS", cursive;
}

h1, h2 {
  transform: rotate(-1deg);
  text-shadow: 0 0 18px #ffd166;
}

button, input {
  font-family: inherit;
}

button:focus-visible,
input:focus-visible {
  outline: 3px solid #7ce7c4;
}
```

HUD table:

| HUD element | Record field | When visible |
| --- | --- | --- |
| None | None | Never. HUD is disabled. |

Diegetic indicators are not HUD:

| Diegetic element | Record field | Visible during |
| --- | --- | --- |
| Fuel tank oil level | `lamp.fuel` | Playing. |
| Lamp flame size | `lamp.fuel`, `lamp.active` | Playing. |
| Life oil cans | `lives` | Playing. |
| Ship guided outline | `ship.guided` | Playing. |
| Safe harbor glow | Fixed left edge | Playing. |

# 8. DEBUG API

| Function | Purpose | System | Tier |
| --- | --- | --- | --- |
| `window.debug.upkeep()` | Returns `lamp` state, fuel, drain rate, low state, out timer. | Upkeep | Tier 1 |
| `window.debug.escort()` | Returns active ships, spawn timer, max active, barriers. | Escort | Tier 1 |
| `window.debug.multitasking()` | Returns active job count, pressure metric, current refuel state. | Multitasking | Tier 1 |
| `window.debug.input.setPointer(x, y)` | Sets logical cursor position. | Input | Tier 1 |
| `window.debug.input.setInsideTank(boolean)` | Force fuel tank hover state. | Input/Upkeep | Tier 1 |
| `window.debug.game.setLives(n)` | Set lives. | Failure | Tier 1 |
| `window.debug.game.setTime(t)` | Set run time. | Progression | Tier 1 |
| `window.debug.game.setFuel(f)` | Set lamp fuel. | Upkeep | Tier 1 |
| `window.debug.escort.spawnShip(lane)` | Force spawn a ship in a lane. | Escort | Tier 1 |
| `window.debug.escort.setTargetLane(shipId, lane)` | Force a ship target lane. | Escort | Tier 1 |

# 9. TESTS

| Tier | Test | Steps | Expected |
| --- | --- | --- | --- |
| Tier 1 | Fixed step loop | Start game, run 120 frames. | Exactly 2.0 seconds of game time elapse. |
| Tier 1 | Seeded RNG | Set seed, spawn ships twice. | Same spawn lanes and timers. |
| Tier 1 | Input clamping | Set pointer outside canvas. | `aimX` and `aimY` remain inside allowed sea aim bounds. |
| Tier 1 | Fuel tank detection | Set pointer inside tank rect. | `input.insideFuelTank` is true. |
| Tier 1 | Fuel drain | Set fuel 50, no ships, run 1 s. | Fuel decreases by approximately 1.4%. |
| Tier 1 | Guided drain | Force one guided ship, run 1 s. | Fuel decreases by approximately 1.75%. |
| Tier 1 | Refuel | Set pointer inside tank, run 1 s. | Fuel increases by approximately 14%. |
| Tier 1 | Lamp out | Set fuel 0. | One life lost, fuel becomes 20, beam disabled for 1.5 s. |
| Tier 1 | Beam angle | Set pointer at sea target. | Beam angle points to clamped target. |
| Tier 1 | Ship lit | Spawn ship inside beam cone. | `ship.guided` true. |
| Tier 1 | Ship target lane | Aim beam line at lane center near ship. | `ship.targetLane` becomes that lane. |
| Tier 1 | Unlit drift | Spawn unlit ship near upcoming barrier. | `ship.targetLane` becomes nearest rock lane. |
| Tier 1 | Safe pass | Set ship target lane to safe lane at barrier. | No collision, ship reaches x < 180. |
| Tier 1 | Rock collision | Set ship target lane to rock lane at barrier. | Ship destroyed, lives decrease by 1. |
| Tier 1 | Save score | Ship reaches x < 180. | `score.saved` increases by 1. |
| Tier 1 | Game over | Set lives 1, force collision. | Phase becomes `gameOver`. |
| Tier 1 | No HUD | During playing, query HUD DOM elements. | No HUD elements exist. |
| Tier 1 | Screens | Load page. | Title visible. Start hides title and begins playing. Game over shows final score. |
| Tier 2 | Calm preset | Select Calm. | Lives 5, speed multiplier 0.75, max active cap 3, fuel multiplier 0.70. |
| Tier 2 | Gale preset | Select Gale. | Lives 2, speed multiplier 1.30, max active cap 7, fuel multiplier 1.40. |
| Tier 2 | Reduced motion | Set reduced motion true. | Screen shake, particles, trails, bloom, and flicker disabled. |
| Tier 2 | Color-blind safe palette | Inspect palette constants. | No critical state uses only red/green. |

# 10. BUILD ORDER

1. Create HTML shell with canvas, title, game over, and CSS phase state machine.
2. Implement fixed-step loop and phase transitions.
3. Implement seeded RNG and global context.
4. Implement pointer input and logical coordinate mapping.
5. Implement lighthouse, lamp, fuel tank records and constants.
6. Implement fuel drain, refuel, low fuel, lamp out.
7. Implement beam angle and beam cone calculation.
8. Implement barriers and sea lane constants.
9. Implement ship spawn, movement, target lane, guidance, unlit drift.
10. Implement collision, save, life loss, game over.
11. Implement score and final score.
12. Implement painterly base rendering: sea, lighthouse, beam, ships, rocks.
13. Implement diegetic state: fuel level, life cans, lamp flame, guided outline.
14. Implement required effects: bloom, particles, trails, hit flash, screen shake.
15. Implement ambient audio and foley.
16. Implement Standard difficulty tuning.
17. Implement debug API.
18. Run Tier 1 tests.
19. Implement Calm, Standard, Gale presets.
20. Implement explicit reduced-motion toggle.
21. Run Tier 2 tests.

# 11. DEFINITION OF DONE

## Tier 1 Definition of Done

High-level: A player can start from title, play a tense single-screen lighthouse survival game, guide ships through rocks using the cursor beam, refuel by hovering the fuel tank, lose lives on ship collisions or lamp out, reach game over, and see a final score. The game is drawn in the dark painterly style, heard through ambient storm audio, and shows required effects without HUD.

- [ ] Title screen loads and can start a Standard run.
- [ ] Game loop uses fixed 1/60 s simulation.
- [ ] Pointer-only input controls beam and fuel tank hover.
- [ ] No in-game movement, clicks, keyboard, or HUD.
- [ ] Lamp fuel drains over time.
- [ ] Guided ships increase fuel drain.
- [ ] Fuel tank hover refuels at 14%/s.
- [ ] Low fuel narrows beam and triggers warning.
- [ ] Lamp extinguish costs one life.
- [ ] Beam follows cursor and lights ships.
- [ ] Lit ships target nearest lane to beam line.
- [ ] Unlit ships target upcoming rock lanes.
- [ ] Three rock barriers exist with exact safe/rock lane patterns.
- [ ] Ships can be saved at x < 180.
- [ ] Ships collide with rock lanes and cost one life.
- [ ] Lives start at 3 and game over occurs at 0.
- [ ] Final score shows ships saved, time survived, and final score.
- [ ] Game over screen can restart or return to title.
- [ ] Dark painterly art is visible.
- [ ] Color-blind safe palette is default.
- [ ] Ambient audio and foley play.
- [ ] Screen shake, particles, hit flash, trails, and bloom are present.
- [ ] Diegetic state indicators show fuel, lives, lamp state, and guided ships.
- [ ] Debug API exposes upkeep, escort, multitasking, and input state.
- [ ] Tier 1 tests pass.

## Tier 2 Definition of Done

High-level: The completed Tier 1 game has required difficulty options and explicit accessibility controls without adding new mechanics.

- [ ] Calm preset applies its exact numbers.
- [ ] Standard preset applies its exact numbers.
- [ ] Gale preset applies its exact numbers.
- [ ] Difficulty can be selected from title before starting.
- [ ] Reduced-motion checkbox exists and disables shake, particles, trails, bloom, and flicker.
- [ ] OS reduced-motion preference is respected by default.
- [ ] Color-blind safe palette remains default and is not dependent on red/green.
- [ ] No new mechanics, enemies, traps, pickups, upgrades, or systems are added.
- [ ] Tier 2 tests pass.

# A. SANITY

| Check | Result |
| --- | --- |
| Does the spec add supporting mechanics? | No. Supporting mechanics are none. Tier 2 only adds required settings, not mechanics. |
| Does the spec add extra mechanics? | No. Tier 3 is none. |
| Are the core mechanics exactly upkeep, multitasking, escort? | Yes. Each is specified with concrete rules and numbers. |
| Is the game single screen? | Yes. Fixed 1280 × 720 logical canvas. |
| Is movement cursor only? | Yes. Gameplay input is pointer position only. No in-game clicks. |
| Is failure losing a life? | Yes. Ship collision and lamp out cost lives. |
| Is survival the objective? | Yes. No win state. Game over at lives 0. |
| Is HUD none? | Yes. No HUD elements. State is diegetic. |
| Are required effects present? | Yes: screen shake, particles, hit flash, trails, bloom. |
| Are required screens present? | Yes: title and game over only. |
| Is the palette dark? | Yes. Mostly near-black with amber/cyan/pale accents. |
| Is the palette color-blind safe? | Yes. No red/green critical encoding; shape, brightness, and outline are used. |
| Is reduced motion addressed? | Yes. Toggle and OS preference. Disables shake, particles, trails, bloom, flicker. |
| Are difficulty options addressed? | Yes. Calm, Standard, Gale with exact numbers. |
| Are numbers concrete? | Yes. All systems have numeric values. |
| Are records and global context present? | Yes. Section 2 defines fields and records. |
| Are module contracts present? | Yes. Section 2.3 lists required functions. |
| Are audio recipes present? | Yes. Section 6 gives synthesis recipes and triggers. |
| Are tests tied to tiers? | Yes. Section 9 separates Tier 1 and Tier 2 tests. |
| Are definitions of done tied to tiers? | Yes. Section 11 mirrors Section 0.3. |