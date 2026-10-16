# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| The player is a fridge that has just gained sentience. | 4.1, 5.1 |
| The fridge is trying to escape a house. | 4.1, 4.4, 4.17 |
| The escape must happen before the movers arrive. | 4.1, 4.17, 4.11 |
| The game is 2D top-down. | 4.2 |
| The playfield is one continuous house, 1280 x 720 units. | 4.3 |
| The house has three rooms: Kitchen, Hallway, Living Room. | 4.3, 4.4 |
| The fridge starts plugged in the kitchen at x 180, y 500, angle 0, power 100. | 4.4, 4.5 |
| The fridge must unplug to move. | 4.6, 4.8 |
| The fridge has limited power and must recharge at outlets. | 4.6, 4.9 |
| The fridge can waddle, rotate, slide, open/close its door, and hum. | 4.7, 4.8, 4.10 |
| Movement and actions create noise. | 4.11 |
| Noise can make residents suspicious or cause them to investigate. | 4.11, 4.13 |
| There are three residents: Mom, Dad, and Kid. | 4.4, 4.12 |
| Residents spawn at 5, 10, and 20 seconds. | 4.12 |
| Residents have sight, suspicion, AI states, and pathfinding. | 4.12, 4.13, 4.14, 4.15 |
| A resident catches the fridge if within 40 units. | 4.16 |
| The player wins by reaching the front door threshold before the timer ends. | 4.17 |
| The player loses if caught, power reaches 0, or the 120-second timer reaches 0. | 4.17 |
| Win priority is above all lose conditions. | 4.17, 4.20 |
| The game has Start, Playing, Paused, Win, and Lose states. | 4.6, 7.1 |
| The HUD shows objective, timer, power, plug state, door state, and prompts. | 4.18, 7.2 |
| The game must be playable in a browser with no build step. | 1.2, 2.1 |
| The game must be testable through `window.__game`. | 2.3, 8 |
| Visuals must be readable and must not change gameplay rules. | 3, 7 |
| Audio must be synthesized or hook-based and must not be the only information channel. | 6, 7 |

## 0.2 Decisions

| Topic | Gameplay | Visual | Engineering | Ruling / Reason |
| --- | --- | --- | --- | --- |
| Dimensionality | 2D top-down. | 2D top-down, fixed camera, no scrolling. | Canvas 1280 x 720, fixed logical size. | Keep 2D top-down. No 3D, no jumping, no camera rotation, no scrolling. |
| Playfield size | 1280 x 720 units. | 1280 x 720, scale to fit with letterboxing. | Canvas 1280 x 720. | Keep 1280 x 720 logical units. Rendering may scale to viewport while preserving aspect ratio. |
| Pathfinding tile size | 32-unit grid. | Tile size 32. | Nav tile 20, grid 64 x 36. | Use 20-unit nav tiles for pathfinding and validation. 32 remains only an optional visual floor-tile size. Reason: 20 makes 1280, 720, and 80-unit doorways exact. |
| Wall thickness | Openings defined, wall rectangles not fully specified. | Visual wall thickness 16, presentation only. | Explicit 20-unit wall rectangles. | Collision, line of sight, and navgrid use the 20-unit engineering wall rectangles. Visuals may draw a 16-unit visual face inside the 20-unit solid rect, but must not alter collision. |
| Fridge visual size | Collider 64 x 32. | Visual size 68 x 36. | Collider 64 x 32. | Use 64 x 32 for collision. 68 x 36 is presentation only. |
| Resident visual size | Collider radius 20. | Visual radius 22. | Collider radius 20. | Use radius 20 for collision and catch. 22 is presentation only. |
| Sight cones | Sight radius 160, FOV 120, LOS blocked. | Subtle clipped sight cones. | Draw order includes residents/fridge; cones optional. | Sight cones are Tier 2. If drawn, they must use radius 160, FOV 120, and be clipped by the same sight-blocking rects used by gameplay. Fallback is a stronger facing indicator. |
| Vignette formula | Intensity equals highest suspicion / 100 when above 50. | Alpha formula: `((maxSuspicion - 50) / 50) * 0.45`, pulse at 100. | `vignetteIntensity = maxSuspicion / 100` if above 50, else 0. | State stores normalized `vignetteIntensity = maxSuspicion / 100` when `maxSuspicion > 50`, else 0. Renderer converts it to visual alpha using the visual formula. |
| Tutorial prompts | Six contextual prompts. | Six prompts with visual triggers. | Five tutorial steps with advance conditions. | Use the merged tutorial table in 7.3. Visual triggers are kept where they improve teaching; engineering advance conditions are kept where they make tests stable. |
| Contextual prompt priority | Examples only. | Error, plug-state, tutorial, idle. | Specific prompt priority list. | Use the merged priority in 7.4. Errors and plug attempts override tutorial text. |
| Audio implementation | Lists audio hooks. | Full SFX and music design. | Audio hooks required; actual playback optional and asset-driven. | Audio is synthesized with WebAudio where possible. No external audio files are required. The optional external asset manifest is dropped from the required build. |
| Collision sound | Collision noise event exists. | Collision SFX exists. | Required hooks did not include collision. | Add `collision` audio hook. It plays when collision noise is emitted. |
| Timer tick | Timer warning below 30. | Clock tick every second below 30 and warning pulse. | `timer_warning` hook plays once when crossing below 30. | Keep `timer_warning` as a one-shot crossing event. Add `timer_tick` for the per-second tick while below 30. |
| Power warning | Power warning below 25. | Low buzz periodically below 25. | `power_warning` hook plays once when crossing below 25. | Keep `power_warning` as a one-shot crossing event. Add optional `power_buzz` periodic sound while below 25. |
| Resident spawn safety | Spawn times only. | Fade-in visual only. | Choose first waypoint at least 40 units from fridge; delay if unsafe. | Keep engineering spawn safety check. It prevents unfair instant catches. |
| Fridge as path obstacle | Approximate 3x2 tile. | Not specified. | Use actual fridge OBB. | Use the actual fridge OBB to block nav cells. It is more accurate than a fixed 3x2 approximation. |
| Layer order | World indicators needed. | Detailed layer order. | Simpler draw order. | Use the merged layer order in 3.4. Sight cones are drawn before awareness icons so icons remain readable. |
| HUD layout | HUD sections. | Recommended positions and styles. | Required DOM ids. | Use engineering DOM ids and visual layout/typography. Positions are CSS defaults, not gameplay constraints. |
| Front door geometry | Front door at x = 1280, y 320 to 400. | Threshold line at x = 1240. | Right wall gap at x 1260 to 1280, y 320 to 400; win zone x >= 1240. | The authoritative win condition is x >= 1240 and y between 320 and 400. The collision opening is the 20-unit wall gap from x 1260 to 1280. Visuals draw the threshold at x = 1240 and outdoor light beyond x = 1280. |
| Touch controls | Keyboard only; touch later. | Buttons keyboard accessible. | No touch controls. | Keyboard is required. On-screen buttons are accessible but touch drag controls are not required. |
| Save system | Cut. | Cut. | Cut. | Cut. Restart is simpler for a short game. |
| Difficulty options | Cut. | Cut. | Cut. | Cut. One tuned experience is the scope. |
| Scoring | Win-screen stats only. | No full scoring. | No scoring beyond required stats. | Keep only win-screen stats: time used, noise events, residents lured. |
| Minimap | Not required. | Cut. | Not required. | Cut. One-screen objective text is enough. |
| Resident suspicion numbers | Icons and vignette. | Icons and vignette, no numbers. | Icons and vignette. | No numeric suspicion HUD. Use eye/exclamation icons and vignette. |
| Resident path lines | Not required. | Cut full path lines. | Not required. | Cut. Paths are internal only. |
| External audio assets | Not required. | Synthesized SFX/music preferred. | Optional asset manifest. | Drop the required external asset manifest. Synthesized audio is the default. |
| Procedural asset code | Not specified. | Optional reference code. | Not specified. | The optional procedural code in visual.md is not required. The visual goals, palettes, and numeric recipes are authoritative. |

### Dropped or Deferred Items

| Item | Source | Ruling | Reason |
| --- | --- | --- | --- |
| 3D movement | Gameplay cut | Dropped | Top-down 2D is the core. |
| Jumping | Gameplay cut | Dropped | Not part of fridge fantasy. |
| Depth-based hiding | Gameplay cut | Dropped | Not readable in top-down 2D. |
| Camera rotation | Gameplay cut | Dropped | Fixed camera is simpler and clearer. |
| Combat | Gameplay cut | Dropped | A fridge should not fight. |
| Inventory | Gameplay cut | Dropped | Distracts from movement stealth. |
| Multiple levels | Gameplay cut | Dropped | One house is a complete escape. |
| Locked interior doors | Gameplay cut | Dropped | Adds puzzle complexity without improving core feel. |
| Food thawing | Gameplay cut | Dropped | Adds another timer and distracts from power/noise. |
| Save system | Gameplay cut | Dropped | Game is short; restart is simpler. |
| Difficulty options | Gameplay cut | Dropped | One tuned experience is better for scope. |
| Mouse aiming | Gameplay cut | Dropped | Keyboard movement is clearer. |
| Pets or extra characters | Gameplay cut | Dropped | Adds AI complexity without enough value. |
| Multiple players | Gameplay cut | Dropped | Breaks the lonely, vulnerable fantasy. |
| Minimap | Visual cut | Dropped | House is one screen. |
| Resident suspicion numbers | Visual cut | Dropped | Icons and vignette are cleaner. |
| Full resident path lines | Visual cut | Dropped | Reduces tension and clutter. |
| Extra non-gameplay furniture | Visual cut | Dropped | Clutters the small playfield. |
| Day/night cycle | Visual cut | Dropped | One dusk mood is enough. |
| Weather | Visual cut | Dropped | Not needed. |
| Character customization | Visual cut | Dropped | Scope. |
| Voice lines | Visual cut | Dropped | Abstract audio is cleaner. |
| Complex particles | Visual cut | Dropped | Game should feel heavy, not explosive. |
| 3D models | Visual cut | Dropped | Not needed. |
| External audio files | Engineering optional | Dropped from required build | Synthesized audio is sufficient and testable. |
| Optional procedural asset code | Visual optional | Deferred / optional | Visual goals are authoritative; code is reference only. |

## 0.3 Tiers

| Tier | Segment | What it includes | Why this tier |
| --- | --- | --- | --- |
| Tier 1 | Playable core simulation | Fixed tick loop, PRNG, level data, level compiler, validation, navgrid, collision, pathfinding, input, fridge movement, plug/power, door/hum, noise, residents, perception, AI, catch, timer, win/lose, start/pause/restart, minimal HUD, placeholder rendering, audio hook recording, debug API, required Tier 1 tests. | This is the minimal viable game and the minimum required to prove the design works. |
| Tier 2 | Readable stealth presentation | Full visual spec: zones, lighting, sprites, shadows, cords, LED, door light, cooldown arcs, sight cones, awareness icons, noise rings, hearing ticks, vignette, animations, screen shake, polished HUD, tutorial prompts, controls reminder, synthesized SFX, synthesized music, accessibility rules. | This makes the game feel like a finished stealth escape rather than a gray simulation. |
| Tier 3 | Optional polish and fallbacks | Optional procedural asset generation, performance fallbacks, extended manual QA, optional visual flourishes beyond required readability. | These improve production value but are not required to say the core game is done. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Quantity | Unit | Value / Convention | Notes |
| --- | ---: | --- | --- |
| Playfield width | units | 1280 | Logical canvas units. |
| Playfield height | units | 720 | Logical canvas units. |
| X axis | units | Right is positive. | Top-down world. |
| Y axis | units | Down is positive. | Canvas coordinate convention. |
| Angle | radians | Internal angles are radians. | `0` radians faces +x. Positive angle rotates clockwise in canvas space. |
| Angle display | degrees | `angleDeg` provided for HUD/tests. | `angleDeg = radToDeg(angle)`. |
| Speed | units/sec | Linear speed. | Waddle max 50, slide 150, resident routine 70, investigate 110. |
| Acceleration | units/sec² | Fridge acceleration. | Waddle acceleration 120. |
| Deceleration | units/sec² | Fridge deceleration. | Waddle deceleration 180. |
| Rotation speed | degrees/sec | Fridge turn speed. | 100 degrees/sec. |
| Time | seconds | Game time is seconds internally. | Updated by fixed ticks. |
| Tick | seconds | `1 / 120` | 120 ticks per second. |
| Production dt clamp | seconds | 0.1 | Prevents tunneling after tab lag. |
| Nav tile | units | 20 | Used for A* grid. |
| Navgrid columns | cells | 64 | `1280 / 20`. |
| Navgrid rows | cells | 36 | `720 / 20`. |
| Visual floor tile | units | 32 | Optional rendering only. |
| Power | power units | 0 to 100 | Starts at 100. |
| Suspicion | suspicion units | 0 to 100 | Per resident. |
| Noise radius | units | Event-specific | Modified by room adjacency. |
| Noise alert | alert units | 0 to 100 | Sets minimum suspicion and can trigger investigation. |
| View radius | units | 160 | Resident sight. |
| Field of view | degrees | 120 | Total cone angle. |
| LOS sample step | units | 8 | Line-of-sight sampling. |
| Catch distance | units | 40 | Resident center to fridge center. |
| Plug radius | units | 48 | Distance from fridge center to outlet center. |
| Plug connection time | seconds | 0.5 | Must remain still. |
| Recharge rate | power/sec | 15 | While plugged. |
| Passive drain | power/sec | 1 | While unplugged. |
| Waddle drain | power/sec | 3 | While unplugged, not sliding, `speedAbs > 1`. |
| Rotate drain | power/sec | 1.5 | While unplugged and rotating input active. |
| Door drain | power/sec | 0.5 | While unplugged and door open. |
| Slide cost | power | 10 | Instant. |
| Hum cost | power | 15 | Instant. |
| Slide duration | seconds | 0.25 | |
| Slide cooldown | seconds | 0.6 | |
| Hum cooldown | seconds | 3 | |
| Step noise interval | seconds | 0.6 | While speed > 10. |
| Slide noise interval | seconds | 0.2 | While sliding. |
| Collision impact threshold | units/sec | 30 | Minimum impact speed for collision noise. |
| Suspicion base rate | suspicion/sec | 20 | When seeing abnormal fridge. |
| Suspicion decay rate | suspicion/sec | 25 | When not seeing abnormal fridge. |
| Suspicious no-detect reset | seconds | 1.5 | Clears suspicion and returns to routine. |
| Search duration | seconds | 3 | |
| Path recalculation interval | seconds | 0.5 | |
| Dwell time range | seconds | 0.5 to 2.0 | Random, PRNG-controlled. |
| Game timer | seconds | 120 | Escape timer. |
| Timer warning threshold | seconds | 30 | Below this, timer warns. |
| Power warning threshold | power | 25 | Below this, power warns. |
| Win zone X threshold | units | 1240 | Fridge center must be `x >= 1240`. |
| Win zone Y range | units | 320 to 400 | Fridge center must be within range. |

## 1.2 Important conventions

1. The game is built with vanilla HTML, CSS, and JavaScript.
2. No build step, no npm, no TypeScript, no ES modules, no external libraries.
3. All JavaScript files are classic scripts loaded in order.
4. The only required globals are:
   - `window.FE`
   - `window.__game`
   - `window.__testResults` in the test page
5. All gameplay updates happen on a fixed 120 Hz simulation tick.
6. Production rendering may run on `requestAnimationFrame`, but simulation uses an accumulator and fixed ticks.
7. Production delta time is clamped to 0.1 seconds.
8. Test mode does not run `requestAnimationFrame`, does not bind keyboard events, and does not bind visibility events.
9. Test mode drives the game through `window.__game`.
10. All randomness uses the deterministic PRNG in `js/prng.js`.
11. Default PRNG seed is `1`.
12. `game.tick()` only advances the world when state is `playing`.
13. `advanceTicks(n)` only advances the world while playing.
14. The simulation tick counter only increments while playing.
15. Game state must be serializable as plain JSON-compatible objects.
16. Presentation systems must not modify simulation state.
17. Audio hooks must be recorded even if audio playback is unavailable or silent.
18. Noise and audio event buffers are bounded.
19. Stats counters must not be dropped when event buffers overflow.
20. Angles are radians internally.
21. `pointInRect` uses half-open intervals:
    - `x >= rect.x && x < rect.x + rect.w`
    - `y >= rect.y && y < rect.y + rect.h`
22. Fridge collision uses oriented bounding box vs axis-aligned rectangle SAT.
23. Resident collision uses circle vs axis-aligned rectangle.
24. Line of sight samples every 8 units from resident center to fridge center.
25. Level validation must run at compile time and must throw on invalid level data.
26. Input edge actions are queued and processed once per tick.
27. Edge action processing order is:
    1. `Escape`
    2. `P`
    3. `E`
    4. `Q`
    5. `Space`
28. If `Escape` pauses the game, other edge actions in that tick are ignored.
29. Pause stops timer, fridge, residents, noise, plug attempts, slides, and audio loops.
30. Hidden browser tab pauses the game only if the game is playing.

# 2. CONTRACTS

## 2.1 Module layout

| File | Responsibility | Tier |
| --- | --- | ---: |
| `index.html` | Production game page. Loads CSS and JS in order. Contains canvas, HUD, overlays, buttons. | 1 |
| `css/game.css` | Layout, HUD styling, warning flashes, overlays, vignette. | 1 |
| `js/constants.js` | All tunable values and key mappings. | 1 |
| `js/math.js` | Vector, angle, rectangle, OBB, circle, and line-of-sight math. | 1 |
| `js/prng.js` | Deterministic seeded PRNG. | 1 |
| `js/level-data.js` | The fixed level definition. | 1 |
| `js/level.js` | Level compiler, validation, navgrid, room lookup, room adjacency. | 1 |
| `js/collision.js` | Fridge OBB vs solid rect collision, resident circle vs solid rect collision. | 1 |
| `js/pathfinding.js` | A* pathfinding on the navgrid. | 1 |
| `js/noise.js` | Noise event emission and hearing resolution. | 1 |
| `js/fridge.js` | Fridge state, movement, plug, door, hum, slide, power. | 1 |
| `js/resident.js` | Resident AI, perception, suspicion, movement, catch. | 1 |
| `js/input.js` | Keyboard input and debug input queue. | 1 |
| `js/audio.js` | Audio hook playback, synthesis, and recording. | 1 |
| `js/hud.js` | DOM HUD updates. | 1 |
| `js/render.js` | Canvas world rendering. | 1 |
| `js/game.js` | Game state machine, simulation tick, win/lose checks. | 1 |
| `js/debug.js` | Exposes `window.__game`. | 1 |
| `js/main.js` | Boots the game. Starts real-time loop only in production mode. | 1 |
| `test/test.html` | Test page. Loads game scripts plus test harness. | 1 |
| `test/test.js` | Tiny test harness and required tests. | 1 |

## 2.2 Global context

`window.__game.getState()` must return a plain serializable object.

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
      remaining: number,
      outletId: string | null
    },

    power: number,
    powerFlash: boolean,
    doorOpen: boolean,

    slide: {
      active: boolean,
      remaining: number,
      cooldown: number
    },

    humCooldown: number,

    room: "kitchen" | "hallway" | "living",
    inWinZone: boolean,
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
      waypointIndex: number,
      dwellTime: number,
      path: [{ x: number, y: number }],
      pathIndex: number,
      hasPath: boolean,
      pathLength: number,
      pathTimer: number,
      searchTimer: number,
      noDetectTimer: number,
      lured: boolean
    }
  ],

  stats: {
    noiseEvents: number,
    residentsLured: number,
    luredIds: [string],
    timeUsed: number
  },

  effects: {
    vignetteIntensity: number,
    noiseRings: [
      {
        x: number,
        y: number,
        radius: number,
        maxRadius: number,
        remaining: number,
        duration: number
      }
    ]
  },

  hud: {
    objective: string,
    prompt: string,
    timerWarning: boolean,
    powerWarning: boolean,
    plug: boolean,
    door: boolean,
    tutorialStep: number
  },

  loseReason: null | "caught" | "power" | "timer"
}
```

Notes:

- `angle` is radians internally.
- `angleDeg` is provided for tests and HUD.
- `time` is elapsed playing seconds.
- `timeUsed` equals `time`.
- `timeRemaining` starts at `120`.
- `residents` always contains all three residents, with `active: false` before spawn.
- `effects.vignetteIntensity` is `0` when max suspicion is 50 or less.
- When max suspicion is above 50, `effects.vignetteIntensity = maxSuspicion / 100`.

## 2.3 Module specifics

| Module | Required functions / API | Purpose |
| --- | --- | --- |
| `FE.Math` | `dist(x1,y1,x2,y2)`, `angleTo(x1,y1,x2,y2)`, `angleDiff(a,b)`, `normalizeAngle(a)`, `degToRad(deg)`, `radToDeg(rad)`, `lerpAngle(a,b,t)`, `pointInRect(x,y,rect)`, `obbCorners(x,y,angle,halfLength,halfWidth)` | Shared math. |
| `FE.PRNG` | `seed(value)`, `next()`, `range(min,max)` | Deterministic randomness. |
| `FE.Level` | `compile(data)`, `validate(data)`, `roomAt(x,y)`, `roomModifier(roomA,roomB)`, `solidRects()`, `sightRects()`, `navgrid()` | Level compilation and queries. |
| `FE.Collision` | `fridgeVsRects(fridge,rects)`, `resolveFridge(fridge,rects)`, `residentVsRects(resident,rects)`, `resolveResident(resident,rects)`, `lineOfSight(x1,y1,x2,y2,sightRects)` | Collision and LOS. |
| `FE.Pathfinding` | `findPath(startCell,goalCell,blockedFn)`, `nearestWalkableCell(cell,blockedFn)`, `cellFromPoint(x,y)`, `pointFromCell(col,row)` | A* pathfinding. |
| `FE.Noise` | `emit(event)`, `applyToResident(event,resident)`, `getEvents(sinceTick)`, `clear()` | Noise events. |
| `FE.Fridge` | `init()`, `update(dt)`, `applyInput(input)`, `trySlide()`, `tryToggleDoor()`, `tryHum()`, `tryPlug()`, `tryUnplug()`, `applyPowerDrain(dt)`, `nearestOutlet()` | Fridge systems. |
| `FE.Resident` | `init()`, `update(dt)`, `spawn(resident)`, `perceive(resident,fridge)`, `updateSuspicion(resident,fridge,dt)`, `updateAI(resident,dt)`, `recalcPath(resident)`, `checkCatch(resident,fridge)` | Resident systems. |
| `FE.Input` | `init()`, `bind()`, `setHeld(codes)`, `clearHeld()`, `tap(code)`, `consumeEdges()` | Keyboard and debug input. |
| `FE.Audio` | `init()`, `playHook(name)`, `startLoop(name)`, `stopLoop(name)`, `getEvents(sinceTick)`, `clear()`, `synthRecipe(name)` | Audio hooks and synthesis. |
| `FE.HUD` | `update(state)`, `setOverlay(state)`, `setPrompt(text)`, `setObjective(text)`, `setWarning(name,active)` | DOM HUD. |
| `FE.Render` | `init(canvas)`, `draw(state)`, `drawWorld(state)`, `drawFridge(state)`, `drawResident(resident)`, `drawNoiseRings(state)`, `drawSightCones(state)`, `drawAwarenessIcons(state)` | Canvas rendering. |
| `FE.Game` | `boot()`, `reset()`, `start()`, `restart()`, `pause()`, `resume()`, `tick()`, `advanceTicks(n)`, `update(dt)`, `checkEnd()` | State machine and tick. |
| `FE.Debug` | Exposes `window.__game`. | Debug API. |

`window.__game` required API:

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

`setFridge` allowed fields:

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

`setResident` allowed fields:

```js
{
  active,
  x,
  y,
  angle,
  state,
  suspicion,
  target,
  waypointIndex,
  dwellTime,
  searchTimer,
  noDetectTimer
}
```

`forceNoise` shape:

```js
{
  x: number,
  y: number,
  radius: number,
  alert: number,
  type: "force"
}
```

# 3. VISUAL SPEC

The game should look like a heavy, awake appliance trying to leave a normal house at dusk. The house is cozy, warm, and slightly watchful, not scary. The fridge is the clearest object on screen: an off-white rounded rectangle with a cyan sentience LED, a visible front door, and a power cord that tells the player whether it is plugged in. Residents are soft colored circles with facing indicators. Noise is shown as physical rings, suspicion is shown with eye and exclamation icons, and danger is shown with red vignette, red timer/power warnings, and minimal screen shake. The visual style is domestic tension: warm wood, soft shadows, household objects, lamp light, and a cooler living room that feels closer to escape but more exposed.

## 3.1 Visual pillars

| Pillar | Meaning |
| --- | --- |
| Awake appliance | The fridge is not a monster. It has a quiet cyan life-light that communicates sentience, power, and state. |
| Domestic tension | The house is cozy, not scary. Tension comes from people moving through comfort. |
| Readable stealth | The player must instantly understand fridge state, resident attention, noise, power, plug state, and door state. |
| One house, three moods | Kitchen is warm and occupied. Hallway is constrained and transitional. Living room is cooler and final. |

## 3.2 Art style rules

| Rule | Value |
| --- | --- |
| Dimensionality | 2D top-down. |
| Shapes | Soft vector / canvas shapes. |
| Corners | Rounded. |
| Saturation | Low. |
| Palette | Warm domestic palette. |
| Shadows | 2.5D soft shadows. |
| 3D | No. |
| Camera rotation | No. |
| Scrolling | No. |
| Pixel art | No. |
| Heavy outlines | No. |
| Cartoon gore | No. |
| Sci-fi UI | No. |

Shape language:

| Element | Shape |
| --- | --- |
| Fridge | Rounded rectangle with a small front face. |
| Residents | Soft circles with a facing indicator. |
| Furniture | Rounded rectangles with subtle top surfaces. |
| UI | Flat panels, rounded corners, keycaps. |
| Effects | Soft rings, glows, short flashes. |

Readability rules:

| Rule |
| --- |
| The fridge must always be the clearest object on screen. |
| Residents must be readable even when moving. |
| Danger must be readable without reading text. |
| Noise must be readable as a physical event. |
| The player should never need a map. |

## 3.3 Canvas, scale, and world layout

| Property | Value |
| --- | ---: |
| Logical playfield | 1280 x 720 |
| Visual floor tile | 32 |
| Nav tile | 20 |
| Camera | Fixed |
| Scrolling | None |
| Scaling | Scale to fit window with letterboxing if needed |
| Aspect ratio | Maintain |
| Visual wall thickness | 16 |
| Collision wall thickness | 20 |

Visual wall rule:

- The authoritative collision rects are the 20-unit engineering wall rects.
- The visual wall face may be 16 units thick.
- Visuals must not move, shrink, or expand collision rects.

Doorways:

| Doorway | Gameplay / collision location | Visual notes |
| --- | --- | --- |
| Kitchen to Hallway | x = 480 boundary, wall gap y = 320 to 400 | Subtle door frame, slightly darker threshold strip, no visible door panel. |
| Hallway to Living Room | x = 800 boundary, wall gap y = 320 to 400 | Subtle door frame, slightly darker threshold strip, no visible door panel. |
| Front Door | Wall gap x = 1260 to 1280, y = 320 to 400; win threshold x = 1240 | Open doorway, soft outdoor light beyond x = 1280, faint threshold line at x = 1240. |

Front door visual rule:

- The win condition is x >= 1240 and y between 320 and 400.
- The faint threshold line exists so the player understands the exact escape point without adding a new mechanic.

## 3.4 Layer order

Draw in this order:

| Order | Layer |
| ---: | --- |
| 1 | Floor / room backgrounds |
| 2 | Zone lighting overlays |
| 3 | Win zone / front door threshold |
| 4 | Object shadows |
| 5 | Furniture and walls |
| 6 | Outlets and plug range indicators |
| 7 | Noise rings |
| 8 | Fridge and residents, sorted by `y` for subtle 2.5D depth |
| 9 | Sight cones, if enabled |
| 10 | Awareness icons |
| 11 | Warning vignette |
| 12 | HUD |

Ruling:

- Sight cones are drawn before awareness icons so icons remain readable.
- Vignette is DOM.
- HUD is always on top.

## 3.5 Color system

Global semantic colors:

| Purpose | Color | Hex / Value |
| --- | ---: | --- |
| UI background | Charcoal | `#171a1c` |
| UI text | Warm white | `#f4f1ea` |
| UI secondary text | Muted sand | `#b8b3a8` |
| Panel background | Translucent charcoal | `rgba(23, 26, 28, 0.72)` |
| Panel border | Soft white | `rgba(244, 241, 234, 0.14)` |
| Fridge body | Off-white | `#eef3f4` |
| Fridge outline | Dark slate | `#3f4a4d` |
| Fridge cyan / sentience | Cool cyan | `#7bd8d6` |
| Fridge dim | Muted teal | `#4f6d6f` |
| Power high | Soft green | `#8fe388` |
| Power medium | Amber | `#f4b942` |
| Power low | Red | `#e14b4b` |
| Danger | Red | `#e14b4b` |
| Noise small | Warm white | `#fff7e0` |
| Noise medium | Amber | `#f4b942` |
| Noise loud | Orange-red | `#ff7a59` |
| Hum | Cyan | `#7bd8d6` |
| Shadow | Soft brown-black | `rgba(25, 20, 18, 0.18)` |

Color rules:

| Rule |
| --- |
| Red is reserved for danger: low power, high suspicion, vignette, lose state. |
| Cyan is the fridge’s identity: LED, plug state, hum, door open glow. |
| Amber is used for medium warnings: medium noise, suspicion, timer warning. |
| Green is used only for healthy power. |
| Do not use red and green as the only distinction anywhere. Always pair color with shape, icon, or motion. |

## 3.6 Zone identity

All zones share:

- The same wall base style.
- The same shadow language.
- The same UI palette.
- The same soft rounded furniture style.

They differ in:

- Floor tone.
- Lighting temperature.
- Furniture.
- Mood.

### 3.6.1 Kitchen

Mood: safe, warm, occupied.

Visual identity: light wood, cream counters, stainless steel, warm lamp light.

| Element | Color |
| --- | --- |
| Floor base | `#e3d3bd` |
| Floor line | `#c9b79d` |
| Floor accent | `#d8c7ae` |
| Wall | `#d9c7a9` |
| Baseboard | `#8a7b68` |
| Counter top | `#cfc4b3` |
| Cabinet | `#8a7b68` |
| Steel | `#aeb6b8` |
| Dark steel | `#3f4a4d` |
| Lamp glow | `#ffdf9e` at `0.08` alpha |

Visual notes:

- The kitchen should be the brightest room.
- Use a soft warm radial glow around the counter area.
- Counters should read as tall furniture from above.
- The sink and stove should be clearly metallic.
- The fridge start position should feel normal: it is plugged in and sitting in the kitchen.

### 3.6.2 Hallway

Mood: constrained, neutral, transitional.

Visual identity: narrow passage, runner rug, small plant, shoe rack, cooler shadows.

| Element | Color |
| --- | --- |
| Floor base | `#cbb9a2` |
| Floor line | `#b5a28b` |
| Floor accent | `#d8c7ae` |
| Runner rug | `#8a6f5c` |
| Runner pattern | `#d9c7a9` |
| Wall | `#cbb9a2` |
| Baseboard | `#7b6a55` |
| Plant leaves | `#6d8b6a` |
| Plant pot | `#a86f4f` |
| Shoe rack | `#7b6a55` |
| Shoe colors | `#4f6d8a`, `#b56a7a`, `#d8a44a` |
| Light | `#f2ead9` at `0.07` alpha |

Visual notes:

- The hallway should feel narrower than the other rooms.
- Use a long runner rug to guide the eye from kitchen to living room.
- The plant and shoe rack should be clearly solid.
- Shadows should be slightly cooler than in the kitchen.

### 3.6.3 Living Room

Mood: duskier, final, more exposed.

Visual identity: cooler floor, blue-grey rug, dark TV, lamp light, front door light.

| Element | Color |
| --- | --- |
| Floor base | `#b7a994` |
| Floor line | `#9f8f7a` |
| Floor accent | `#c7b8a3` |
| Rug | `#6d7b8c` |
| Rug pattern | `#a9b7c4` |
| Wall | `#b8c2c9` |
| Baseboard | `#4a4038` |
| Sofa | `#7d6f8a` |
| Sofa cushion | `#9a8aa5` |
| Coffee table | `#8a6f5c` |
| TV stand | `#4a4038` |
| TV screen | `#171a1c` |
| Bookshelf | `#6d5b4a` |
| Book colors | `#b56a7a`, `#6d8ba8`, `#d8a44a`, `#6d8b6a` |
| Dusk overlay | `#203040` at `0.08` alpha |
| Lamp glow | `#ffcf8a` at `0.10` alpha |

Visual notes:

- The living room should feel cooler and darker.
- The front door should glow softly.
- The TV should be off, dark, and slightly reflective.
- The rug should make the center of the room feel open but visually bounded.
- The bookshelf should contain muted colored books, matching resident colors.

## 3.7 Entity scale

| Entity | Gameplay collider | Visual size | Rule |
| --- | ---: | ---: | --- |
| Fridge | 64 x 32 | 68 x 36 | Extra 2 units per side are outline/shadow only. |
| Resident | Radius 20 | Radius 22 | Extra 2 units are soft shadow/outline only. |

## 3.8 Fridge visuals

Local orientation:

- Facing direction is `+x` in local space.
- The fridge’s face is the short front edge in the direction it is facing.
- The door is on the front face.

Base sprite:

| Part | Description |
| --- | --- |
| Body | Rounded rectangle. |
| Body color | Off-white. |
| Outline | Dark slate. |
| Seam | Vertical seam near the front. |
| Front face | Small front face panel. |
| LED | One cyan LED eye near the front. |
| Shadow | Soft shadow offset down-right. |

Fridge LED states:

| State | LED color | Behavior |
| --- | --- | --- |
| Plugged | Bright cyan | Steady, slight pulse every 2 seconds. |
| Unplugged, healthy power | Muted teal | Dimmer, steady. |
| Low power | Flickering red/teal | Flickers at 0.5 Hz. |
| Power depleted | Dark grey | Off. |
| Humming | Bright cyan | Flashes 3 times over 0.3 seconds. |
| Caught | Red | Flashes once, then dark. |

Cord and plug state:

| State | Visual |
| --- | --- |
| Plugged | Cable connects fridge to plugged outlet. Dark slate cable with thin cyan core. Outlet glows cyan. Small power pulse travels along cable every 2 seconds. |
| Unplugged | Cable dangles from rear of fridge. Dark slate cable with no cyan core. Outlet does not glow unless fridge is in plug range. |

Plug range visual:

When the fridge is unplugged and within 48 units of an outlet:

| Property | Value |
| --- | ---: |
| Outlet glow | Cyan |
| Dashed circle radius | 48 |
| Alpha | 0.25 |
| Line width | 2 |
| Dashed pattern | 6, 6 |

Plug connection progress:

| Property | Value |
| --- | ---: |
| Duration | 0.5 seconds |
| Arc radius | 26 |
| Start angle | -90 degrees |
| Line width | 3 |
| Color | `#7bd8d6` |

If interrupted:

- Arc resets.
- Cable snaps back to unplugged state.
- No success sound or flash plays.

Door state:

| State | Visual |
| --- | --- |
| Closed | Front face panel flush with body. No light spill. |
| Open | Front face panel swings outward. Interior light spills forward. LED becomes brighter. Soft cyan glow around open door. |

Door animation:

| Property | Value |
| --- | ---: |
| Open duration | 0.2 seconds |
| Close duration | 0.2 seconds |
| Easing | Ease-out |

Light spill:

| Property | Value |
| --- | ---: |
| Shape | Soft trapezoid extending forward from door |
| Length | 40 units |
| Width at far edge | 32 units |
| Color | Cyan |
| Alpha | 0.25 |

Movement visuals:

| Action | Visual |
| --- | --- |
| Waddling | Slight squash and stretch. Forward scale 1.02, side scale 0.98. Shadow shifts slightly opposite movement. Small dust puff behind fridge every 0.6 seconds. Dust color warm grey, alpha 0.2, lifetime 0.3 seconds. |
| Sliding | 3 motion streaks behind fridge. Streak length 30 units, alpha 0.3, lifetime 0.2 seconds. 2 dark scuff marks on floor, alpha 0.25, lifetime 1 second. Shadow stretches slightly in movement direction. Loud noise ring appears. |
| Hard collision | If impact speed > 30: white flash on fridge for 0.05 seconds. Small screen shake magnitude 2 pixels for 0.1 seconds. Impact noise ring appears. |
| Soft collision | If impact speed <= 30: no flash, no shake, no noise. |

Cooldown visuals:

| Cooldown | Color | Radius | Duration |
| --- | ---: | ---: | ---: |
| Slide cooldown | White | 26 | 0.6 seconds |
| Hum cooldown | Cyan | 26 | 3 seconds |

Cooldown behavior:

- Arc fills clockwise.
- When complete, arc disappears.
- If both are active, draw slide arc slightly inside hum arc.

Low power visuals:

| Condition | Visual |
| --- | --- |
| Power below 25 | Fridge body desaturates slightly. LED flickers. Power bar flashes red. Low buzz sound plays periodically. |
| Power below 10 | LED becomes mostly red. Fridge outline darkens. Movement squash becomes slightly weaker. |

Fridge state transitions:

| Event | Visual |
| --- | --- |
| Game starts | LED fades in over 0.5 seconds. |
| Unplug | Cable snaps free, small grey pop ring. |
| Plug success | Cyan flash, cable connects, outlet glows. |
| Door open | Panel swings, cyan light spill. |
| Door close | Panel swings back, light fades. |
| Hum | Cyan pulse, LED flash, large ring. |
| Caught | Red flash, freeze for 0.2 seconds, cord yank. |
| Power depleted | LED dies, body greys out, desaturate. |
| Win | Door light expands, screen brightens. |

## 3.9 Resident visuals

Residents are top-down circles.

Base resident:

| Property | Value |
| --- | ---: |
| Visual radius | 22 |
| Shadow | Soft shadow offset down-right |
| Outline | Dark slate |
| Facing indicator | Small light dot or wedge near edge |
| Body bob | Slight bob while moving |

Facing indicator:

- Small light dot or wedge near the edge of the circle.
- Makes resident view direction obvious.

Resident distinction:

| Resident | Color | Visual detail |
| --- | ---: | --- |
| Mom | Muted rose `#b56a7a` | Small bun / hair detail. |
| Dad | Slate blue `#6d8ba8` | Broader shoulder shading. |
| Kid | Mustard `#d8a44a` | Small backpack dot. |

Do not make the kid visually much smaller than the others.

Resident spawn:

| Resident | Spawn time |
| --- | ---: |
| Mom | 5 seconds |
| Dad | 10 seconds |
| Kid | 20 seconds |

Spawn visual:

| Property | Value |
| --- | ---: |
| Fade in | 0.3 seconds |
| Scale | 0.9 to 1.0 |

Resident state visuals:

| State | Visual |
| --- | --- |
| Routine | Normal walk cycle. Faces movement direction. No awareness icon. Sight cone faint. |
| Suspicious | Stops moving. Faces fridge. Eye icon appears above head. Eye icon opacity equals `suspicion / 100`. Sight cone brightens slightly. Body outline may get subtle amber tint. |
| Investigate | Moves faster. Exclamation icon replaces eye icon. Sight cone becomes sharper and slightly amber. Shadow gets faint red tint. Stride animation faster. |
| Search | Resident stops at target. Slowly rotates in place. Soft scanning arc may rotate with them. Awareness icon fades out. |

## 3.10 Resident sight cones

Sight cone gameplay values:

| Property | Value |
| --- | ---: |
| Radius | 160 |
| Field of view | 120 degrees |
| Origin | Resident center |
| Direction | Resident facing angle |

Cone settings:

| State | Alpha | Color |
| --- | ---: | --- |
| Routine | 0.06 | Warm white `#fff7e0` |
| Suspicious | 0.10 | Warm white `#fff7e0` |
| Investigate | 0.14 | Amber `#f4b942` |
| Search | 0.08 | Warm white `#fff7e0` |

Cone clipping:

- Sight cones must be clipped by blocking walls and furniture.
- Use the same blocking logic as gameplay line of sight.
- If performance is a concern, pre-render a walkable mask and mask the cone with it.

Fallback:

- If cones are too expensive, replace cones with a stronger directional indicator on residents.
- Keep awareness icons and suspicion vignette.

## 3.11 Awareness icons

Above each resident:

| Suspicion | Display |
| ---: | --- |
| 0 | No icon. |
| 1 to 99 | Eye icon. Opacity equals `suspicion / 100`. Color amber. Size 16 x 10. Position 24 units above resident center. |
| 100 | Exclamation icon. Color red. Size 16 x 16. Position 24 units above resident center. Small pop scale from 1.2 to 1.0 over 0.15 seconds. |

## 3.12 Noise visuals

General ring rules:

- Rings expand from the source.
- Ring radius equals the noise radius.
- Rings fade quickly.
- Ring alpha is reduced by 0.5 for each room boundary crossed.
- Hum rings are visibly larger and more distinct.

Noise ring table:

| Noise source | Radius | Color | Duration | Line width | Notes |
| --- | ---: | --- | ---: | ---: | --- |
| Waddle step | 12 | Warm white | 0.35 seconds | 2 | Small, frequent. |
| Plug connection | 10 | Warm white | 0.25 seconds | 2 | Very small. |
| Door toggle | 15 | Warm white | 0.30 seconds | 2 | Small. |
| Unplug | 20 | Amber | 0.35 seconds | 3 | Medium. |
| Collision | 25 | Amber | 0.35 seconds | 3 | Medium. |
| Slide | 50 | Orange-red | 0.45 seconds | 4 | Loud. |
| Hum | 160 | Cyan | 0.70 seconds | 5 | Very loud. |

Hum ring:

- Cyan color.
- Larger radius.
- Longer duration.
- Slight glow.
- LED flashes.
- Door light pulse.

Hearing ticks:

When a resident hears a noise:

| Property | Value |
| --- | ---: |
| Visual | Small white dot above resident’s head |
| Duration | 0.2 seconds |
| Size | 4 units |
| Behavior | Appears in addition to awareness icon. |

## 3.13 Warning vignette

Let `maxSuspicion` be the highest resident suspicion.

State rule:

```text
if maxSuspicion <= 50:
  vignetteIntensity = 0
else:
  vignetteIntensity = maxSuspicion / 100
```

Visual alpha rule:

```text
if maxSuspicion <= 50:
  alpha = 0
else:
  alpha = ((maxSuspicion - 50) / 50) * 0.45
```

At `maxSuspicion = 100`:

- Add subtle pulse.
- Pulse amplitude: 0.05.
- Pulse frequency: 1 Hz.

Visual:

- Radial gradient.
- Center transparent.
- Edges red `#e14b4b`.
- No full-screen red tint.

## 3.14 Animation and feel

Animation principles:

- Short, quiet animations for normal movement.
- Larger, louder animations for risky actions.
- No excessive screen shake.
- No fast strobing.
- No particle explosions.

Timing:

| Animation | Duration |
| --- | ---: |
| Door open/close | 0.2 seconds |
| Plug connection | 0.5 seconds |
| Slide | 0.25 seconds |
| Waddle step puff | 0.3 seconds |
| Noise ring | 0.25 to 0.7 seconds |
| Awareness icon pop | 0.15 seconds |
| State transition | 0.2 seconds |
| Win transition | 0.8 seconds |
| Lose transition | 0.6 seconds |

Screen shake:

| Event | Magnitude | Duration |
| --- | ---: | ---: |
| Hard collision | 2 pixels | 0.1 seconds |
| Caught | 4 pixels | 0.2 seconds |

## 3.15 Asset checklist

World:

- Kitchen floor tile.
- Hallway floor tile.
- Hallway runner rug.
- Living room floor tile.
- Living room rug.
- Wall segment.
- Internal doorway frame.
- Front door opening.
- Outside light beyond front door.
- Kitchen counter.
- Kitchen sink.
- Kitchen stove.
- Potted plant.
- Shoe rack.
- Sofa.
- Coffee table.
- TV stand.
- TV screen.
- Bookshelf.
- Outlets.
- Outlet glow.
- Plug range indicator.
- Front door threshold line.
- Zone lighting overlays.
- Shadows.

Fridge:

- Fridge base sprite.
- Fridge shadow.
- Fridge LED.
- Fridge door closed.
- Fridge door open.
- Fridge interior light spill.
- Plugged cord.
- Unplugged cord.
- Plug connection arc.
- Slide motion streaks.
- Slide scuff marks.
- Waddle dust puff.
- Collision flash.
- Low power desaturation.
- Caught red flash.
- Win light expansion.

Residents:

- Mom base sprite.
- Dad base sprite.
- Kid base sprite.
- Resident shadow.
- Resident facing indicator.
- Routine walk animation.
- Suspicious stop animation.
- Investigate fast walk animation.
- Search scan animation.
- Eye icon.
- Exclamation icon.
- Hearing tick.
- Sight cone.

FX:

- Noise rings.
- Hum ring.
- Plug success flash.
- Unplug pop ring.
- Door open/close glow.
- Warning vignette.
- Timer warning pulse.
- Power warning flash.
- State transition fades.
- Win brighten.
- Lose desaturate.

UI:

- Title screen background.
- Title text.
- Subtitle text.
- Play button.
- Resume button.
- Restart button.
- Retry button.
- Play Again button.
- Objective panel.
- Room icons.
- Timer.
- Power bar.
- Plug icon.
- Door icon.
- Contextual prompt panel.
- Keycaps.
- Controls reminder.
- Win panel.
- Lose panel.
- Pause overlay.

Audio:

- Music layers.
- SFX from section 6.
- Win jingle.
- Lose sting.
- UI hover/click sounds, optional.

# 4. GAMEPLAY SPEC

The player is a newly sentient refrigerator in a normal house. The fridge begins plugged in the kitchen and must unplug, waddle through the house, avoid three residents, manage power, use noise carefully, and reach the front door before the 120-second escape timer ends. The game is a single continuous top-down stealth escape: the player cannot fight, but can move quietly, recharge, create decoys with hum, and use slide for a short noisy burst. The house is one screen, divided into Kitchen, Hallway, and Living Room, with pressure increasing as the fridge approaches the front door.

## 4.1 Records and rosters

### 4.1.1 Fridge record

| Field | Type | Notes |
| --- | --- | --- |
| `x` | number | Center X. |
| `y` | number | Center Y. |
| `angle` | number | Radians. |
| `angleDeg` | number | Degrees. |
| `speed` | number | Scalar along facing direction. Positive forward, negative backward. |
| `speedAbs` | number | Absolute speed. |
| `plugged` | boolean | Plugged state. |
| `plugAttempt` | object | Active plug connection. |
| `power` | number | 0 to 100. |
| `powerFlash` | boolean | Flash after failed power action. |
| `doorOpen` | boolean | Door state. |
| `slide` | object | Slide state. |
| `humCooldown` | number | Seconds remaining. |
| `room` | string | Kitchen, hallway, living. |
| `inWinZone` | boolean | Win zone check. |
| `nearestOutletId` | string/null | Nearest outlet within plug radius. |

Roster: one fridge.

### 4.1.2 Resident roster

| ID | Name | Spawn time | Waypoint loop |
| --- | --- | ---: | --- |
| `mom` | Mom | 5 seconds | 1. x 140, y 140; 2. x 300, y 140; 3. x 300, y 620; 4. x 140, y 620 |
| `dad` | Dad | 10 seconds | 1. x 1000, y 200; 2. x 640, y 200; 3. x 640, y 500; 4. x 1000, y 500 |
| `kid` | Kid | 20 seconds | 1. x 1050, y 240; 2. x 1160, y 360; 3. x 1050, y 480; 4. x 940, y 360 |

Resident record fields are defined in 2.2.

### 4.1.3 Outlet roster

| ID | X | Y | Radius | Notes |
| --- | ---: | ---: | ---: | --- |
| `kitchen-outlet` | 120 | 500 | 48 | Non-blocking recharge point. |
| `hallway-outlet` | 640 | 360 | 48 | Non-blocking recharge point. |
| `living-outlet` | 900 | 600 | 48 | Non-blocking recharge point. |

### 4.1.4 Obstacle roster

| Object | Rectangular bounds | Blocks movement | Blocks line of sight |
| --- | --- | --- | --- |
| Top counter | x 20 to 460, y 20 to 80 | Yes | Yes |
| Left counter | x 20 to 80, y 100 to 420 | Yes | Yes |
| Sink | x 200 to 280, y 100 to 180 | Yes | Yes |
| Stove | x 360 to 440, y 100 to 180 | Yes | Yes |
| Potted plant | x 600 to 660, y 120 to 180 | Yes | Yes |
| Shoe rack | x 600 to 660, y 540 to 600 | Yes | Yes |
| Sofa | x 900 to 1120, y 80 to 160 | Yes | Yes |
| Coffee table | x 1000 to 1100, y 300 to 380 | Yes | Yes |
| TV stand | x 1200 to 1260, y 80 to 200 | Yes | Yes |
| Bookshelf | x 1200 to 1260, y 520 to 640 | Yes | Yes |

### 4.1.5 Win zone record

| Property | Value |
| --- | ---: |
| X threshold | 1240 |
| Y range | 320 to 400 |
| Win condition | Fridge center `x >= 1240` and `y` between 320 and 400. |

### 4.1.6 Noise event record

| Field | Type | Notes |
| --- | --- | --- |
| `tick` | number | Tick when emitted. |
| `type` | string | `step`, `slide`, `collision`, `plug`, `unplug`, `door`, `hum`, `force`. |
| `x` | number | Source X. |
| `y` | number | Source Y. |
| `radius` | number | Base radius. |
| `alert` | number | Alert value. |
| `heardBy` | array | Resident IDs that heard the event. |

### 4.1.7 Noise ring record

| Field | Type | Notes |
| --- | --- | --- |
| `x` | number | Ring X. |
| `y` | number | Ring Y. |
| `radius` | number | Current radius. |
| `maxRadius` | number | Final radius. |
| `remaining` | number | Seconds remaining. |
| `duration` | number | Total duration. |

## 4.2 Dimensionality — Tier 1

Chosen dimensionality: 2D top-down.

The gameplay is fully 2D top-down. Visuals may add 2.5D shadows or height, but no gameplay mechanic depends on depth, jumping, or 3D line of sight.

Why top-down 2D:

- House navigation is clearest from above.
- Doorway fitting and rotation are easier to understand.
- Resident line of sight and noise propagation are easier to read.
- It is more browser-friendly than 3D.
- It avoids the problem of side-view rooms hiding important layout information.

Cut by design:

- No 3D movement.
- No jumping.
- No depth-based hiding.
- No camera rotation.

## 4.3 Space and layout — Tier 1

The game is one continuous level: a single house.

Logical playfield size:

| Property | Value |
| --- | ---: |
| Width | 1280 |
| Height | 720 |

Rooms:

| Room | X range | Purpose |
| --- | ---: | --- |
| Kitchen | 0 to 480 | Start area, tutorial, first resident. |
| Hallway | 480 to 800 | Middle pressure, recharge, noise management. |
| Living Room | 800 to 1280 | Final approach to front door. |

Openings:

| Opening | Location | Size |
| --- | --- | ---: |
| Kitchen to Hallway | x = 480, y = 320 to 400 | 80 units tall |
| Hallway to Living Room | x = 800, y = 320 to 400 | 80 units tall |
| Front Door | x = 1280, y = 320 to 400 | 80 units tall |

Authoritative collision note:

- The front door collision opening is the 20-unit wall gap from x = 1260 to x = 1280, y = 320 to 400.
- The win zone begins at x = 1240.

The front door is the win zone. The fridge wins when its center enters the front door threshold:

- x >= 1240
- y between 320 and 400

Why one continuous level:

- The escape is a single journey through a house.
- Splitting it into separate levels would break the tension and make the escape feel artificial.
- One level allows smooth progression from tutorial to final pressure.

## 4.4 Map content — Tier 1

### 4.4.1 Kitchen

The kitchen is the starting room.

Fridge start position:

| Property | Value |
| --- | ---: |
| x | 180 |
| y | 500 |
| angle | 0 degrees, facing right |
| plugged | true |
| power | 100 |

Kitchen outlet:

| Property | Value |
| --- | ---: |
| x | 120 |
| y | 500 |
| blocking | no |
| purpose | recharge point |

Kitchen obstacles:

| Object | Rectangular bounds | Blocks movement | Blocks line of sight |
| --- | --- | --- | --- |
| Top counter | x 20 to 460, y 20 to 80 | Yes | Yes |
| Left counter | x 20 to 80, y 100 to 420 | Yes | Yes |
| Sink | x 200 to 280, y 100 to 180 | Yes | Yes |
| Stove | x 360 to 440, y 100 to 180 | Yes | Yes |

Kitchen resident: Mom

- Mom appears at 5 seconds.
- Waypoint loop:
  1. x 140, y 140
  2. x 300, y 140
  3. x 300, y 620
  4. x 140, y 620
- Mom loops through the kitchen.
- Her route is designed to force the player to time movement.
- She does not pass within 40 units of the fridge start position.

### 4.4.2 Hallway

The hallway is the middle room. It is narrow enough to feel constrained but wide enough for the fridge to rotate.

Hallway outlet:

| Property | Value |
| --- | ---: |
| x | 640 |
| y | 360 |
| blocking | no |
| purpose | recharge point |

Hallway obstacles:

| Object | Rectangular bounds | Blocks movement | Blocks line of sight |
| --- | --- | --- | --- |
| Potted plant | x 600 to 660, y 120 to 180 | Yes | Yes |
| Shoe rack | x 600 to 660, y 540 to 600 | Yes | Yes |

Hallway resident: Dad

- Dad appears at 10 seconds.
- Waypoint loop:
  1. x 1000, y 200
  2. x 640, y 200
  3. x 640, y 500
  4. x 1000, y 500
- Dad crosses between the living room and hallway.
- His route creates repeated pressure in the middle room.

### 4.4.3 Living Room

The living room contains the front door.

Living room outlet:

| Property | Value |
| --- | ---: |
| x | 900 |
| y | 600 |
| blocking | no |
| purpose | recharge point |

Living room obstacles:

| Object | Rectangular bounds | Blocks movement | Blocks line of sight |
| --- | --- | --- | --- |
| Sofa | x 900 to 1120, y 80 to 160 | Yes | Yes |
| Coffee table | x 1000 to 1100, y 300 to 380 | Yes | Yes |
| TV stand | x 1200 to 1260, y 80 to 200 | Yes | Yes |
| Bookshelf | x 1200 to 1260, y 520 to 640 | Yes | Yes |

The coffee table blocks the direct path to the front door. The player must go around it either above or below.

Living room resident: Kid

- Kid appears at 20 seconds.
- Waypoint loop:
  1. x 1050, y 240
  2. x 1160, y 360
  3. x 1050, y 480
  4. x 940, y 360
- Kid moves around the coffee table and creates final pressure near the front door.

## 4.5 Game states — Tier 1

The game has five states:

1. Start
2. Playing
3. Paused
4. Win
5. Lose

### 4.5.1 Start state

Display:

- Title: “Fridge Escape”
- Subtitle: “You are awake. Leave before the movers arrive.”
- Play button
- Controls list

The game does not update the world until Play is pressed.

### 4.5.2 Playing state

All systems update.

The escape timer starts when the game enters Playing.

### 4.5.3 Paused state

Pause is triggered by Escape.

While paused:

- Timer stops.
- Residents stop.
- Fridge stops.
- Noise events stop.
- Plug attempt freezes.
- Slide freezes.
- An overlay displays:
  - Resume
  - Restart

If the browser tab becomes hidden, the game automatically pauses.

### 4.5.4 Win state

Triggered when the fridge center enters the front door threshold.

Display:

- “You escaped.”
- Time used
- Number of noise events created
- Number of residents lured
- Play Again button

### 4.5.5 Lose state

Lose reasons:

| Reason | Text |
| --- | --- |
| Caught | “You got unplugged.” |
| Power depleted | “Your hum faded.” |
| Timer expired | “The movers arrived.” |

Display:

- Lose reason
- Retry button

Lose priority order:

1. Win
2. Caught by resident
3. Power depleted
4. Timer expired

This order matters for edge cases. If the fridge reaches the door at the same moment as another condition, the player wins.

## 4.6 Controls — Tier 1

| Input | Action |
| --- | --- |
| W or Up | Waddle forward |
| S or Down | Waddle backward |
| A or Left | Turn left |
| D or Right | Turn right |
| Space | Slide |
| E | Open or close fridge door |
| Q | Hum |
| P | Plug in or unplug |
| Escape | Pause |

Why keyboard only:

- This is a browser game with precise timing.
- Keyboard input is the clearest input model.
- Touch support can be added later, but it is not required for the core design.

## 4.7 Fridge movement — Tier 1

The fridge is a rotated rectangle.

Collider:

| Property | Value |
| --- | ---: |
| Length | 64 units |
| Width | 32 units |
| Rotation | Around its center |

The fridge cannot overlap walls, counters, furniture, or other blocked tiles.

### 4.7.1 Waddling

Waddling is the default movement.

| Property | Value |
| --- | ---: |
| Max waddle speed | 50 units/sec |
| Acceleration | 120 units/sec² |
| Deceleration | 180 units/sec² |

The fridge can waddle forward and backward relative to its facing direction.

Why waddling is slow:

- The fridge should feel heavy.
- Waddling is safe but not fast enough to outrun a resident.

### 4.7.2 Rotation

| Property | Value |
| --- | ---: |
| Rotation speed | 100 degrees/sec |

The fridge turns slowly.

Why rotation is slow:

- Fitting through doorways should be deliberate.
- The player must plan orientation before entering tight spaces.

### 4.7.3 Sliding

Sliding is a short burst of speed.

| Property | Value |
| --- | ---: |
| Slide speed | 150 units/sec |
| Slide duration | 0.25 seconds |
| Slide cooldown | 0.6 seconds |
| Slide power cost | 10 power |
| Slide noise | Loud |

The fridge slides in the direction it is facing.

The player can slide only if:

- Power is at least 10.
- Slide cooldown has finished.
- The fridge is unplugged.
- Slide is not already active.
- Plug attempt is not active.

Why sliding exists:

- Sliding gives the player an escape tool.
- It is faster than residents, but it is noisy.
- This creates the core risk/reward: speed versus detection.

## 4.8 Plug and power system — Tier 1

The fridge is powered by the house’s electricity.

Power range:

| Property | Value |
| --- | ---: |
| Minimum | 0 |
| Maximum | 100 |
| Start | 100 |

### 4.8.1 Plugged state

When plugged:

- The fridge cannot move.
- The fridge cannot rotate.
- The fridge cannot slide.
- Power recharges at 15 power/sec.
- Passive power drain is 0.
- The door can still be opened or closed.
- Hum can still be used if power is available.

### 4.8.2 Unplugged state

When unplugged:

- The fridge can move.
- Power drains.
- The fridge can plug into an outlet.

### 4.8.3 Power drain

Power drains only while unplugged.

| Condition | Drain |
| --- | ---: |
| Passive, unplugged | 1 power/sec |
| Waddling, speed > 1 unit/sec | +3 power/sec |
| Rotating | +1.5 power/sec |
| Door open | +0.5 power/sec |
| Sliding | 10 power instant cost |
| Hum | 15 power instant cost |

Why power drains only while unplugged:

- This makes plugging in a meaningful safe state.
- The player can recharge, but while plugged they are stationary and vulnerable.

### 4.8.4 Plugging and unplugging

The fridge can plug into any outlet.

Outlet radius:

| Property | Value |
| --- | ---: |
| Plug radius | 48 units |

Plug action:

- If unplugged and within 48 units of an outlet, pressing P starts a 0.5-second connection.
- If the player moves, rotates, slides, or unplugs during connection, the plug attempt fails.
- If connection succeeds, the fridge becomes plugged.

Unplug action:

- If plugged, pressing P immediately unplugs the fridge.

Noise:

- Plug connection emits a small noise.
- Unplugging emits a medium noise.

Why plug/unplug is a player action:

- It makes power management active rather than automatic.
- The player must decide when to stop and recharge.

## 4.9 Door and hum system — Tier 1

The fridge has a door.

### 4.9.1 Door state

The door can be:

- Closed
- Open

Pressing E toggles the door.

Gameplay effects of door open:

- The fridge can hum.
- If unplugged, power drains at +0.5/sec.
- Residents are more suspicious of the fridge.

Why the door matters:

- The door is the fridge’s identity.
- It is also the source of its “voice.”
- Opening the door makes the fridge more noticeable, but it enables the hum action.

### 4.9.2 Hum

Hum is a loud noise event used to lure residents.

| Property | Value |
| --- | ---: |
| Power cost | 15 |
| Cooldown | 3 seconds |
| Noise radius | 160 |
| Noise alert value | 100 |
| Requirement | Door must be open |

The hum occurs at the fridge’s current position.

Residents who hear the hum investigate the hum location, not necessarily the fridge’s current location after it moves.

Why hum exists:

- Hum gives the player an active stealth tool.
- The player can create a decoy by humming, then move away.
- This is important because the player cannot fight or hide indefinitely.

## 4.10 Noise system — Tier 1

Noise is event-based. Noise does not persist over time. When an action creates noise, it immediately checks whether residents hear it.

### 4.10.1 Noise events

| Source | Radius | Alert value | Notes |
| --- | ---: | ---: | --- |
| Waddle step | 12 | 15 | Emits every 0.6 seconds while speed > 10. |
| Slide | 50 | 45 | Emits at slide start and every 0.2 seconds while sliding. |
| Collision | 25 | 30 | Emits if impact speed > 30. |
| Plug connection | 10 | 10 | Emits when plug starts. |
| Unplug | 20 | 25 | Emits when unplugging. |
| Door toggle | 15 | 15 | Emits when door opens or closes. |
| Hum | 160 | 100 | Emits at fridge position. |

### 4.10.2 Room modifier

Noise is reduced across room boundaries.

| Relationship | Radius modifier |
| --- | ---: |
| Same room | 1.0 |
| Adjacent room | 0.5 |
| Non-adjacent room | 0.0 |

Room adjacency:

- Kitchen is adjacent to Hallway.
- Hallway is adjacent to Living Room.
- Kitchen is not adjacent to Living Room.

Why room modifiers exist:

- They make the house feel like a real house.
- A loud slide in the kitchen should not instantly wake someone in the living room, but a hum should travel farther.

### 4.10.3 Hearing algorithm

When a noise event is emitted:

For each active resident:

1. Determine the resident’s room.
2. Determine the noise source room.
3. Apply room modifier to noise radius.
4. If distance from resident to noise source is less than or equal to modified radius, the resident hears the noise.
5. Set the resident’s `lastKnownPosition` to the noise source.
6. Set the resident’s suspicion to at least the noise alert value.
7. If alert value is 50 or higher, set the resident state to Investigate and set their target to the noise source.

Why alert values matter:

- Small noises make residents suspicious.
- Large noises make them investigate.
- This gives different actions different levels of danger.

Residents lured stat:

- `stats.residentsLured` counts unique residents that enter Investigate because of a noise event with alert >= 50.
- Sight-based investigation does not count as “lured.”

## 4.11 Resident systems — Tier 1

Residents are the main threat.

There are three residents:

- Mom
- Dad
- Kid

All residents use the same perception and AI rules.

### 4.11.1 Resident collider

Residents are circles.

| Property | Value |
| --- | ---: |
| Radius | 20 units |

Residents do not block line of sight.

### 4.11.2 Resident movement speeds

| State | Speed |
| --- | ---: |
| Routine | 70 units/sec |
| Investigate | 110 units/sec |

Why residents are faster than waddling:

- The player cannot safely outrun residents by waddling.
- The player must hide, wait, or use slide.

Why slide is faster than residents:

- Slide gives a short escape window.
- It is noisy and limited by cooldown and power.

### 4.11.3 Resident spawn times

| Resident | Spawn time |
| --- | ---: |
| Mom | 5 seconds |
| Dad | 10 seconds |
| Kid | 20 seconds |

The first 5 seconds are safe. This gives the player time to learn the basic controls before the first resident appears.

Why staggered spawns:

- It creates a smooth difficulty ramp.
- The player learns movement in the kitchen, then faces hallway pressure, then faces the final living room challenge.

Spawn safety rule:

- On activation, choose the first waypoint that is at least 40 units from the fridge.
- If none is safe, delay spawn and recheck every 1 second.
- This prevents an unfair instant lose if the player is standing at a spawn point when the resident appears.

## 4.12 Resident perception — Tier 1

Residents can detect the fridge by sight and sound.

### 4.12.1 Sight

Each resident has a view cone.

| Property | Value |
| --- | ---: |
| View radius | 160 units |
| Field of view | 120 degrees |

A resident can see the fridge if:

- The fridge is within view radius.
- The fridge is inside the resident’s field of view.
- Line of sight is not blocked by walls or furniture.

Line of sight algorithm:

- Cast a line from the resident’s center to the fridge’s center.
- Sample every 8 units.
- If any sample intersects a blocking tile, line of sight is blocked.

Why line of sight matters:

- The player must use furniture as cover.
- Without line-of-sight blocking, stealth would be too simple.

### 4.12.2 Anomaly detection

A resident only becomes suspicious if the fridge looks abnormal.

The fridge is considered abnormal if any of the following are true:

- The fridge is unplugged.
- The fridge is moving, speed > 5 units/sec.
- The fridge door is open.
- The fridge is not in the kitchen.
- The fridge is within 80 units of the resident.

If the fridge is plugged, stationary, in the kitchen, and its door is closed, residents do not gain suspicion from seeing it.

Why anomaly detection exists:

- A fridge in the kitchen is normal.
- A fridge in the hallway is not.
- This makes the kitchen a starting safe zone but not a permanent safe zone once the player unplugs or moves.

### 4.12.3 Suspicion

Each resident has a suspicion value from 0 to 100.

When a resident sees an abnormal fridge:

Base suspicion rate:

| Property | Value |
| --- | ---: |
| Base rate | 20 suspicion/sec |

Modifiers:

| Condition | Suspicion rate added |
| --- | ---: |
| Fridge is moving | +20/sec |
| Fridge is unplugged | +20/sec |
| Fridge door is open | +10/sec |
| Fridge is not in kitchen | +10/sec |
| Fridge is within 80 units | +20/sec |

Examples:

- If a resident sees an unplugged, moving fridge in the hallway, suspicion rises at 70/sec.
- If a resident sees a stationary plugged fridge in the hallway, suspicion rises at 30/sec.

When the resident no longer sees an abnormal fridge:

- Suspicion decays at 25 suspicion/sec.
- If suspicion reaches 0, the resident returns to Routine if it was only Suspicious.
- If the resident is Suspicious and no abnormal detection occurs for 1.5 seconds, suspicion is cleared to 0 and the resident returns to Routine.

Why suspicion is gradual:

- Instant detection would feel unfair.
- Gradual suspicion gives the player a chance to react, hide, or move.

## 4.13 Resident AI states — Tier 1

Each resident has one of four states:

1. Routine
2. Suspicious
3. Investigate
4. Search

### 4.13.1 Routine

The resident follows its waypoint loop.

- Moves at routine speed.
- Faces movement direction.
- Dwell time at each waypoint: 0.5 to 2 seconds, randomly chosen.
- If suspicion becomes greater than 0, the resident becomes Suspicious.

### 4.13.2 Suspicious

The resident stops and faces the fridge.

- Does not move.
- Accumulates suspicion if it continues to see an abnormal fridge.
- If suspicion reaches 100, becomes Investigate.
- If no abnormal detection occurs for 1.5 seconds, suspicion decays and the resident returns to Routine.

Why Suspicious exists:

- It gives the player a visible warning.
- The player can see that a resident has noticed something and can react before full investigation.

### 4.13.3 Investigate

The resident moves to the last known suspicious position.

- Moves at investigate speed.
- Uses pathfinding.
- If the resident sees the fridge while investigating, it updates its target to the fridge’s current position and sets suspicion to 100.
- If the resident reaches the target and does not see the fridge, it enters Search.

### 4.13.4 Search

The resident waits at the target and scans.

- Search duration: 3 seconds.
- After searching, the resident returns to Routine.
- After Search ends, suspicion becomes 0.

Why Search exists:

- It prevents residents from chasing forever.
- It also gives the player a chance to slip away after being heard.

## 4.14 Resident pathfinding — Tier 1

Residents use A* pathfinding.

Grid:

| Property | Value |
| --- | ---: |
| Tile size | 20 units |
| Grid width | 64 cells |
| Grid height | 36 cells |
| Walkable tiles | Floor and doorways |
| Blocked tiles | Walls, counters, furniture, and other non-walkable objects |

Gameplay originally specified 32-unit tiles. This spec supersedes that with 20-unit nav tiles. 32 remains only an optional visual floor tile size.

The fridge is treated as a temporary obstacle for resident pathfinding.

- Mark a nav cell blocked if its center is inside the fridge OBB.
- This approximates the fridge as a moving obstacle.
- Use the actual OBB, not a fixed 3x2 tile.

Path recalculation:

- Every 0.5 seconds.
- Immediately when the resident’s target changes significantly.
- When state changes to Routine or Investigate.
- If no path exists, the resident stops and faces its last known target.

Why pathfinding is needed:

- Residents must navigate around furniture and doorways.
- Without pathfinding, they would either move unnaturally or get stuck.

## 4.15 Catch condition — Tier 1

A resident catches the fridge if:

- The resident’s center is within 40 units of the fridge’s center.

When caught:

- The game enters Lose state.
- Lose reason: “You got unplugged.”

Why catch is distance-based:

- It is simple and readable.
- The player knows not to let residents touch the fridge.

Residents path around the fridge, so catching usually happens when:

- The player moves into a resident.
- A resident investigates the player’s position.
- A resident searches near the player.

## 4.16 Escape timer — Tier 1

The player has 120 seconds to escape.

The timer:

- Starts when the game enters Playing.
- Stops while paused.
- Reaches 0 only in Playing state.

If the timer reaches 0:

- The game enters Lose state.
- Lose reason: “The movers arrived.”

Why a timer is required:

- Without a timer, the player could remain plugged in the kitchen indefinitely.
- The timer gives the game a hard end condition and creates constant pressure.

Why 120 seconds:

- It is long enough for a first-time player to learn and recover from mistakes.
- It is short enough to create tension.
- A careful run should take roughly 60 to 90 seconds.

## 4.17 Progression through the game — Tier 1

The game progresses spatially and temporally.

### 4.17.1 Act 1: Kitchen

Goal: leave the kitchen.

The player learns:

- Unplugging.
- Waddling.
- Turning.
- Basic noise.
- First resident pressure from Mom.

The kitchen is the safest room, but it is not safe forever because the timer exists and unplugging creates noise.

### 4.17.2 Act 2: Hallway

Goal: cross the hallway.

The player learns:

- Recharging at outlets.
- Using hum to create decoys.
- Managing Dad’s crossing route.
- Deciding when to slide versus waddle.

The hallway is the most constrained space. It is where the player feels the core tension of the game.

### 4.17.3 Act 3: Living Room

Goal: reach the front door.

The player combines all systems:

- Avoid Kid.
- Use cover around the coffee table.
- Manage power.
- Decide when to take final risk.

The living room is the final pressure zone. The front door is visible but not easy to reach safely.

### 4.17.4 Objective text progression

The HUD objective updates based on the fridge’s room.

| Condition | Objective text |
| --- | --- |
| Fridge is plugged at start | “Unplug and leave.” |
| Fridge is in kitchen | “Leave the kitchen.” |
| Fridge is in hallway | “Cross the hallway.” |
| Fridge is in living room | “Reach the front door.” |
| Fridge is in win zone | “Escape!” |

Why objective text updates:

- It gives the player clear progress without a map.

## 4.18 Feel and tuning — Tier 1

The game should feel heavy, tense, and deliberate.

### 4.18.1 Movement feel

| Feeling | How it is achieved |
| --- | --- |
| Heavy | Low waddle speed, slow acceleration, slow rotation |
| Vulnerable | Residents are faster than waddling |
| Bursty | Slide is fast but short and loud |
| Deliberate | Doorways require rotation and spacing |
| Urgent | 120-second timer |
| Resourceful | Power and hum create choices |

### 4.18.2 Risk/reward table

| Action | Benefit | Risk |
| --- | --- | --- |
| Waddle | Quiet, controllable | Slow, drains power |
| Slide | Fast escape | Loud, uses power, has cooldown |
| Plug in | Recharges power | Stationary, vulnerable |
| Unplug | Allows movement | Noisy, starts power drain |
| Open door | Enables hum | More suspicious |
| Hum | Lures residents | Very loud, uses power, reveals location |

### 4.18.3 Tension curve

| Time | Pressure |
| --- | --- |
| 0 to 5 seconds | Safe, tutorial |
| 5 to 20 seconds | Mom appears, kitchen pressure |
| 20 to 45 seconds | Dad appears, hallway pressure |
| 45 to 75 seconds | Kid appears, living room pressure |
| 75 to 120 seconds | Timer pressure, final approach |

The exact timing depends on player behavior, but the design intent is that pressure increases as the player approaches the front door.

## 4.19 Edge cases and all cases — Tier 1

### 4.19.1 Pause and hidden tab

- Escape pauses the game.
- Hiding the browser tab pauses the game.
- While paused, no timer, movement, AI, or noise updates occur.

### 4.19.2 Insufficient power

If the player tries to slide with less than 10 power:

- Slide does not occur.
- Power bar flashes.

If the player tries to hum with less than 15 power:

- Hum does not occur.
- Power bar flashes.

### 4.19.3 Plug not available

If the player presses P while unplugged but not within 48 units of an outlet:

- Nothing happens.
- If a contextual prompt is active, it can show “No outlet nearby.”

If the player presses P while plugged:

- The fridge unplugs immediately.

### 4.19.4 Interrupted plug

If the player starts plugging in but moves, rotates, slides, or unplugs during the 0.5-second connection:

- Plug attempt fails.
- The fridge remains unplugged.

### 4.19.5 Multiple residents

- All residents update independently.
- The first catch condition triggers lose.
- The highest suspicion value drives the warning vignette.
- Noise events affect all residents within modified radius.

### 4.19.6 No path

If a resident cannot path to its target:

- It stops.
- It faces its last known target.
- It does not catch the fridge unless within 40 units.

### 4.19.7 Resident blocked by fridge

The fridge is a temporary obstacle for resident pathfinding.

If the fridge blocks a resident’s path:

- The resident waits.
- The player can use this as a temporary safe spot, but if the resident is within 40 units, the player loses.

### 4.19.8 Win and lose same frame

Priority:

1. Win
2. Caught
3. Power depleted
4. Timer expired

If the fridge reaches the front door at the same time as another lose condition, the player wins.

### 4.19.9 Timer and power at zero

If power reaches 0 before the timer:

- Lose by power.

If the timer reaches 0 before power:

- Lose by timer.

If both happen in the same frame:

- Power loss takes priority over timer loss, unless the fridge is also winning, in which case win takes priority.

### 4.19.10 Hum cooldown

If the player presses Q while hum cooldown is active:

- Nothing happens.

If the player presses Q with door closed:

- Nothing happens.
- A contextual prompt can show “Open your door to hum.”

### 4.19.11 Slide cooldown

If the player presses Space while slide cooldown is active:

- Nothing happens.

### 4.19.12 Collision

If the fridge collides with a wall or object:

- Movement stops.
- If impact speed is greater than 30 units/sec, emit collision noise.

### 4.19.13 Delta time

Clamp delta time to 0.1 seconds maximum.

Why:

- Prevents tunneling and unfair jumps if the browser tab lags.

## 4.20 Cut by design — Tier 1

These are intentionally not included.

| Cut piece | Why it was cut |
| --- | --- |
| Combat | A fridge should not fight. Stealth fits the fantasy. |
| Inventory | Would complicate controls and distract from movement stealth. |
| Multiple levels | One house is enough for a complete escape. |
| Locked interior doors | Would add puzzle complexity without improving core feel. |
| Food thawing | Interesting, but would add another timer and distract from power/noise. |
| Save system | The game is short. Restart is simpler. |
| Difficulty options | One tuned experience is better for scope. |
| Mouse aiming | Keyboard movement is clearer for a top-down stealth game. |
| Pets or extra characters | Would add AI complexity without enough gameplay value. |
| Multiple players | Would break the lonely, vulnerable fantasy. |

# 5. CHARACTERS

## 5.1 Fridge

### 5.1.1 Silhouette

- Rounded rectangle.
- Off-white body.
- Dark slate outline.
- Vertical seam near the front.
- Small front face panel.
- One cyan LED eye near the front.
- Soft shadow offset down-right.
- Power cord from rear.
- Door on the front face.

Facing:

- Local facing direction is `+x`.
- The front face and door indicate facing.
- The LED is near the front.

### 5.1.2 Animations by name

| Animation | Motion rules |
| --- | --- |
| `idle_plugged` | Stationary. LED bright cyan, slight pulse every 2 seconds. Cable connected to outlet. |
| `idle_unplugged` | Stationary. LED muted teal. Cable dangles. |
| `waddle` | Slight squash and stretch. Forward scale 1.02, side scale 0.98. Shadow shifts opposite movement. Dust puff every 0.6 seconds while speed > 10. |
| `slide` | Motion streaks behind fridge. 3 streaks, length 30, alpha 0.3, lifetime 0.2. Scuff marks on floor. Shadow stretches in movement direction. |
| `collide_hard` | White flash 0.05 seconds. Screen shake 2 pixels for 0.1 seconds. Impact noise ring. |
| `door_open` | Front panel swings outward over 0.2 seconds. Cyan light spill appears. LED brightens. |
| `door_close` | Front panel swings back over 0.2 seconds. Light fades. |
| `plug_attempt` | Cyan arc fills around fridge over 0.5 seconds. |
| `plug_success` | Cyan flash. Cable connects. Outlet glows. |
| `unplug` | Cable snaps free. Small grey pop ring. |
| `hum` | Cyan pulse. LED flashes 3 times over 0.3 seconds. Large cyan noise ring. Door light pulse. |
| `low_power` | Body desaturates. LED flickers red/teal at 0.5 Hz. |
| `power_depleted` | LED dies. Body greys out. Desaturate. |
| `caught` | Red flash. Freeze for 0.2 seconds. Cord yank. LED flashes red once, then dark. |
| `win` | Door light expands. Screen brightens. |

## 5.2 Residents

### 5.2.1 Silhouettes

Residents are top-down circles.

| Resident | Color | Silhouette detail |
| --- | ---: | --- |
| Mom | Muted rose `#b56a7a` | Small bun / hair detail. |
| Dad | Slate blue `#6d8ba8` | Broader shoulder shading. |
| Kid | Mustard `#d8a44a` | Small backpack dot. |

All residents:

- Visual radius 22.
- Soft shadow offset down-right.
- Dark slate outline.
- Facing indicator near edge.
- Slight body bob while moving.

Facing:

- Resident `angle` is facing direction.
- Facing indicator is a small light dot or wedge near the edge.
- View cone, if drawn, uses the same facing angle.

### 5.2.2 Animations by name

| Animation | Motion rules |
| --- | --- |
| `spawn` | Fade in over 0.3 seconds. Scale from 0.9 to 1.0. |
| `routine_walk` | Normal walk cycle. Faces movement direction. No awareness icon. |
| `suspicious_stop` | Stops moving. Faces fridge or last known position. Eye icon appears. Amber outline tint. |
| `investigate_walk` | Faster stride. Exclamation icon. Sharper amber sight cone. Faint red shadow tint. |
| `search_scan` | Stops at target. Slowly rotates in place. Soft scanning arc may rotate. Awareness icon fades out. |
| `heard_tick` | Small white dot appears above head for 0.2 seconds when hearing noise. |

### 5.2.3 States required by gameplay

| State | Gameplay rule |
| --- | --- |
| Routine | Follows waypoint loop at 70 units/sec. |
| Suspicious | Stops, faces fridge/last known, accumulates or decays suspicion. |
| Investigate | Moves to target at 110 units/sec using pathfinding. |
| Search | Waits 3 seconds, scans, then returns to Routine. |

# 6. AUDIO

The builder has access to a WebAudio-style audio API. Audio is presentation-only. All critical information must also be visual. Audio hooks must be recorded even if playback is unavailable.

Master mix:

| Bus | Gain |
| --- | ---: |
| Master | 0.80 |
| Music | 0.35 |
| SFX | 0.65 |
| UI | 0.50 |

Mixing rules:

- Loud SFX should briefly duck music by about -6 dB.
- Waddle steps should never overpower resident awareness pings.
- Hum should be clearly louder than waddling.
- Timer ticks should be subtle but persistent.
- Lose sting should cut through music immediately.

## 6.1 SFX table

| Name / hook | Tier | Recipe | When it plays |
| --- | ---: | --- | --- |
| `waddle` | 2 | 80 Hz sine + filtered noise, low-pass around 300 Hz. Duration 0.08 seconds. Gain 0.22. Loop while speed > 10 and not sliding. | Every 0.6 seconds while fridge `speedAbs > 10` and not sliding. Record loop start/stop. |
| `slide` | 2 | 50 Hz sine + noise sweep from 300 Hz to 80 Hz. Duration 0.25 seconds. Gain 0.55. | Slide start. |
| `collision` | 2 | Short thump. 90 to 140 Hz sine, pitch varies slightly with impact speed, plus short noise. Duration 0.08 seconds. Gain 0.35. | Collision noise emitted when impact speed > 30. |
| `plug` | 2 | 1200 Hz click + 200 Hz hum, low-passed. Duration 0.12 seconds. Gain 0.30. | Plug attempt starts. |
| `unplug` | 2 | 70 Hz thump + 900 Hz click. Duration 0.12 seconds. Gain 0.45. | Fridge unplugs. |
| `door_open` | 2 | Band-passed noise + 180 Hz sine. Duration 0.18 seconds. Gain 0.30. | Door opens. |
| `door_close` | 2 | 90 Hz thump + 600 Hz click. Duration 0.08 seconds. Gain 0.35. | Door closes. |
| `hum` | 2 | 55 Hz + 110 Hz sine, 5 Hz vibrato. Duration 0.80 seconds. Gain 0.50. | Hum action succeeds. |
| `suspicion` | 2 | 880 Hz sine. Duration 0.05 seconds. Gain 0.15. | Awareness icon appears / resident enters Suspicious. |
| `investigate` | 2 | 1320 Hz + 1760 Hz double ping. Duration 0.10 seconds. Gain 0.25. | Resident enters Investigate. |
| `timer_warning` | 2 | 1800 Hz square. Duration 0.02 seconds. Gain 0.10. | One-shot when timer crosses below 30 seconds. |
| `timer_tick` | 2 | 1800 Hz square. Duration 0.02 seconds. Gain 0.08. | Every second while timer < 30. |
| `power_warning` | 2 | 60 Hz square. Duration 0.20 seconds. Gain 0.15. | One-shot when power crosses below 25. |
| `power_buzz` | 2 | 60 Hz square, periodic. Gain 0.10. | Periodic while power < 25. |
| `win` | 2 | F4, A4, C5, F5 soft triangle notes. Duration 0.80 seconds. Gain 0.40. | Win state. |
| `lose` | 2 | Detuned 110 Hz dropping to 90 Hz, low-passed. Duration 0.60 seconds. Gain 0.40. | Lose state. |

## 6.2 Music table

| Name / layer | Tier | Recipe | When it plays | Gain |
| --- | ---: | --- | --- | ---: |
| `house_hum` | 2 | 55 Hz sine + 110 Hz sine, low-passed. | Playing. | 0.10 |
| `kitchen_piano` | 2 | Soft felt piano notes: D3, A3, F4, E4. Synthesize with low-pass triangle/sine. | Fridge in kitchen. | 0.22 |
| `hallway_pulse` | 2 | 40 Hz sub pulse on beats 1 and 3. Tempo 72 BPM. | Fridge in hallway. | 0.08 |
| `living_drone` | 2 | D2 string drone + pulse every beat. | Fridge in living room. | 0.10 |
| `tension_shimmer` | 2 | Filtered noise + high string. Gain scales with max suspicion. | Max suspicion > 50. | 0 to 0.12 |
| `timer_tick_music` | 2 | 1800 Hz square tick every second. | Timer < 30. | 0.08 |
| `win_jingle` | 2 | F major notes: F4, A4, C5, F5. Soft triangle. | Win. | 0.35 |
| `lose_sting` | 2 | Unresolved D minor drop. Detuned 110 Hz to 90 Hz. | Lose. | 0.35 |

Music identity:

| Property | Value |
| --- | --- |
| Style | Ambient domestic tension. |
| Tempo | 72 BPM. |
| Base key | D minor. |
| Win key | F major. |
| Lose | Unresolved D minor. |
| Instruments | Soft felt piano, low sine hum, sub pulse, sparse string drone, filtered noise shimmer, clock tick. |

Dynamic mixing:

| Situation | Layers |
| --- | --- |
| Start screen | House hum, very sparse piano, low volume. |
| Kitchen | House hum, soft piano, no pulse. |
| Hallway | House hum, piano slightly darker, add sub pulse. |
| Living room | House hum, piano darker, add string drone, stronger pulse. |
| Suspicion | When max suspicion > 50, add tension shimmer. Gain scales from 0 to 0.12. |
| Timer warning | When timer < 30, add tick layer. |
| Win | Stop tension. Crossfade to F major jingle. |
| Lose | Stop music loop. Play lose sting. |

Crossfades:

| Change | Crossfade |
| --- | ---: |
| Room changes | 1 second |
| State changes | 0.5 seconds |
| Win/lose | 0.3 second stop + jingle/sting |

# 7. UX

UX is HTML and CSS only, plus canvas for the world. The canvas is the world viewport. The HUD, overlays, buttons, vignette, and prompts are DOM elements styled with CSS.

## 7.1 Screens as a state machine

| State | Entry | Exit | Visible UI | World updates |
| --- | --- | --- | --- | --- |
| Start | Boot / reset | Play button or `start()` | `#overlay-start` | No. |
| Playing | Start / Resume / Restart | Pause, Win, Lose | HUD, canvas, optional vignette | Yes. |
| Paused | Escape while playing, hidden tab while playing, `pause()` | Resume button, Escape, `resume()` | `#overlay-pause`, dimmed HUD | No. |
| Win | Fridge center in win zone | Play Again / `restart()` | `#overlay-end` with win content | No. |
| Lose | Caught, power 0, timer 0 | Retry / `restart()` | `#overlay-end` with lose content | No. |

State transitions:

| From | To | Trigger |
| --- | --- | --- |
| Start | Playing | Play button or `start()`. |
| Playing | Paused | Escape while playing, hidden tab while playing, `pause()`. |
| Paused | Playing | Resume button, Escape while paused, `resume()`. |
| Playing | Win | Win zone condition. |
| Playing | Lose | Caught, power depleted, timer expired. |
| Win | Playing | Play Again / `restart()`. |
| Lose | Playing | Retry / `restart()`. |
| Any | Start | `reset()`. |

HTML skeleton:

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

## 7.2 HUD table

| Element | DOM id | Record field(s) | When visible | Visual behavior |
| --- | --- | --- | --- | --- |
| World canvas | `#game-canvas` | Full state | Always | Dimmed in Start, active in Playing, frozen in Paused, behind overlays in Win/Lose. |
| Objective panel | `#hud-objective` | `hud.objective` | Playing | Top-left panel. Room icon plus text. |
| Escape timer | `#hud-timer` | `timeRemaining` | Playing | Top-center. Monospace. Flashes red below 30 seconds. |
| Power bar | `#hud-power-bar` | `fridge.power` | Playing | Top-right. Green 25-100, amber 10-24, red 0-9. Flashes red below 25. |
| Plug icon | `#hud-plug-icon` | `fridge.plugged` | Playing | Cyan with glow when plugged. Grey when unplugged. |
| Door icon | `#hud-door-icon` | `fridge.doorOpen` | Playing | Grey closed. Cyan open with small light spill. |
| Contextual prompt | `#hud-prompt` | `hud.prompt` | Playing when non-empty | Bottom-left. Keycaps for keys. Fade in 0.15s, fade out 0.2s. |
| Controls reminder | `#hud-controls` | Static | Playing | Bottom-right. Full opacity first 10 seconds, then 30% opacity. Full opacity while paused. |
| Warning vignette | `#vignette` | `effects.vignetteIntensity` | Playing when intensity > 0 | Red screen-edge vignette. Pulse at max suspicion 100. |
| Start overlay | `#overlay-start` | `state` | Start | Title, subtitle, controls list, Play button. |
| Pause overlay | `#overlay-pause` | `state` | Paused | Dark overlay, Paused title, Resume, Restart. |
| End overlay | `#overlay-end` | `state`, `loseReason`, `stats` | Win or Lose | Title, reason, stats, Play Again / Retry. |

HUD layout defaults:

| HUD section | Position |
| --- | --- |
| Objective | Top-left |
| Escape timer | Top-center |
| Power / plug / door | Top-right |
| Contextual prompt | Bottom-left |
| Controls reminder | Bottom-right |

Recommended CSS positions:

| Element | Suggested position / size |
| --- | --- |
| Objective panel | x = 16, y = 16, w = 260, h = 44 |
| Timer | centered at x = 640, y = 24 |
| Top-right panel | x = 1000, y = 16, w = 264, h = 64 |
| Contextual prompt | x = 16, y = 656, w = 360, h = 40 |
| Controls reminder | x = 1040, y = 656, w = 224, h = 40 |

Typography:

```css
font-family: "Trebuchet MS", "Segoe UI", Arial, sans-serif;
```

For timer:

```css
font-family: "Courier New", monospace;
```

Sizes:

| Element | Size |
| --- | ---: |
| Title | 64px |
| Subtitle | 20px |
| Objective | 18px |
| Timer | 32px |
| HUD labels | 14px |
| Prompt text | 16px |
| Button text | 18px |

UI components:

| Component | Style |
| --- | --- |
| Panels | Background `rgba(23, 26, 28, 0.72)`, border `1px` or `2px` `rgba(244, 241, 234, 0.14)`, corner radius 10, padding 12. |
| Primary button | Background amber `#f4b942`, text charcoal `#171a1c`, corner radius 10, padding 12 x 24. Hover brighten by 10%. Focus cyan outline `#7bd8d6`, width 3. |
| Secondary button | Background translucent white, text warm white, border soft white. Focus cyan outline. |
| Keycaps | Size 24 x 24, background `rgba(255, 255, 255, 0.08)`, border `1px` `rgba(244, 241, 234, 0.25)`, text warm white, corner radius 6. |

Objective room icons:

| Room | Icon |
| --- | --- |
| Kitchen | Small pot or fork |
| Hallway | Small runner rug |
| Living room | Small door |

Start screen controls list:

| Key | Action |
| --- | --- |
| W / Up | Waddle forward |
| S / Down | Waddle backward |
| A / Left | Turn left |
| D / Right | Turn right |
| Space | Slide |
| E | Open or close door |
| Q | Hum |
| P | Plug or unplug |
| Escape | Pause |

Win screen content:

- “You escaped.”
- Time used: `stats.timeUsed`
- Noise events created: `stats.noiseEvents`
- Residents lured: `stats.residentsLured`
- Play Again button

Lose screen content:

| Lose reason | Text |
| --- | --- |
| Caught | “You got unplugged.” |
| Power depleted | “Your hum faded.” |
| Timer expired | “The movers arrived.” |

Also display Retry button.

## 7.3 Tutorial prompts — Tier 2

Tutorial prompts appear contextually and do not block input.

| Step | Prompt | Trigger / display rule | Advance condition |
| ---: | --- | --- | --- |
| 0 | “You are awake. You need to leave.” | When Playing starts. Show for 2.5 seconds. | Time or step 1. |
| 1 | “Press P to unplug.” | While plugged at start. | Fridge unplugs. |
| 2 | “W/S: waddle. A/D: turn.” | After unplugging. Show for 4 seconds or until first meaningful movement. | Fridge moves more than 20 units from start or 4 seconds pass. |
| 3 | “Space: slide. Fast, but loud.” | After movement prompt. Show for 3 seconds or until first slide. | Slide used or 3 seconds pass. |
| 4 | “E: open/close door. Q: hum. Hum lures residents.” | When door first opens, or 30 seconds after start if not shown. | Door opened or 5 seconds pass after display. |
| 5 | “Reach the front door before time runs out.” | When fridge enters hallway, or 45 seconds after start. | Win. |

Tutorial prompts can be overridden by urgent contextual prompts.

## 7.4 Contextual prompt priority — Tier 1

Show one prompt at a time.

| Priority | Condition | Prompt |
| ---: | --- | --- |
| 1 | Failed slide due to low power | “Not enough power to slide.” |
| 2 | Failed hum due to low power | “Not enough power to hum.” |
| 3 | Failed plug due to no outlet | “No outlet nearby.” |
| 4 | Failed hum due to closed door | “Open your door to hum.” |
| 5 | Plug attempt active | “Hold still to plug in.” |
| 6 | Unplugged and near outlet | “Press P to plug in and recharge.” |
| 7 | Plugged | “Press P to unplug.” |
| 8 | Power < 25 | “Find an outlet.” |
| 9 | Door open and hum ready | “Press Q to hum.” |
| 10 | Door closed and power >= 15 | “Press E to open your door.” |
| 11 | Slide ready and unplugged | “Press Space to slide. It is loud.” |
| 12 | Tutorial prompt active | Current tutorial prompt. |
| 13 | None | Empty string. |

Error prompts should display briefly, about 1 second, unless the condition persists.

## 7.5 Accessibility

Colorblind support:

- Do not rely on color alone.
- Power bar uses length plus color.
- Danger uses red plus exclamation icons and vignette.
- Noise uses size, color, and ring shape.
- Plug state uses icon shape plus color.
- Door state uses icon shape plus color.

Contrast:

- UI text: `#f4f1ea` on `#171a1c`.
- Secondary text should remain readable but less prominent.

Motion:

- No strobe effects above 3 flashes per second.
- Timer pulse: 1 Hz.
- Vignette pulse: 1 Hz.
- Screen shake is small.
- No full-screen flashing.

Audio accessibility:

All critical information must also be visual:

- Suspicion.
- Noise.
- Power.
- Timer.
- Plug state.
- Door state.
- Win/lose.

Input accessibility:

- Buttons should be keyboard accessible.
- Focus state should be visible.
- Enter or Space can activate the focused start-screen button.
- Escape pauses during play.

# 8. DEBUG API

`window.__game` is the official test and QA API. It must be available after the game boots.

| Method | Behavior | Tier |
| --- | --- | ---: |
| `boot()` | Initializes game. Called automatically by `main.js`. | 1 |
| `reset()` | Resets to start state. | 1 |
| `start()` | Starts playing from start state. | 1 |
| `restart()` | Resets and starts playing. | 1 |
| `pause()` | Pauses if playing. | 1 |
| `resume()` | Resumes if paused. | 1 |
| `tick()` | Advances one fixed tick if playing. | 1 |
| `advanceTicks(n)` | Advances `n` ticks if playing. | 1 |
| `getState()` | Returns serializable state. | 1 |
| `getNoiseEvents(sinceTick)` | Returns noise events with `tick >= sinceTick`. | 1 |
| `getAudioEvents(sinceTick)` | Returns audio events with `tick >= sinceTick`. | 1 |
| `clearEvents()` | Clears noise and audio event buffers. | 1 |
| `setHeld(codes)` | Sets held keys. | 1 |
| `clearHeld()` | Releases all held keys. | 1 |
| `tap(code)` | Simulates an edge key press. | 1 |
| `simulateVisibility(hidden)` | Simulates tab visibility change. | 1 |
| `setSeed(seed)` | Sets deterministic PRNG seed. | 1 |
| `setFridge(partial)` | Overrides fridge fields for tests. | 1 |
| `setResident(id, partial)` | Overrides resident fields for tests. | 1 |
| `setTimeRemaining(seconds)` | Sets timer for tests. | 1 |
| `forceNoise(event)` | Emits a noise event through the normal noise system. | 1 |
| `getLevel()` | Returns compiled level data. | 1 |

System-specific direct state access:

| Gameplay system | Debug function |
| --- | --- |
| Fridge position / plug / power / door / cooldowns | `setFridge(partial)` |
| Resident state / position / suspicion / target | `setResident(id, partial)` |
| Escape timer | `setTimeRemaining(seconds)` |
| Noise system | `forceNoise(event)` |
| Randomness | `setSeed(seed)` |
| Player held inputs | `setHeld(codes)`, `clearHeld()` |
| Player edge inputs | `tap(code)` |
| Visibility pause | `simulateVisibility(hidden)` |

Event buffers:

| Buffer | Limit |
| --- | ---: |
| Noise events | 4096 |
| Audio events | 4096 |

When a buffer is full, drop oldest events. Stats counters must not be dropped.

# 9. TESTS

Tests should validate each tier. Tier 1 tests prove the simulation is complete. Tier 2 tests prove presentation and audio hooks are wired. Tier 3 tests are optional polish checks.

## 9.1 Tier 1 tests

| Test group | Test | Pass condition |
| --- | --- | --- |
| Boot and state | Boot state | `window.__game.ready` is true. State is `start`. Fridge at start position. Fridge plugged. Power 100. Time remaining 120. All residents inactive. |
| Boot and state | Start game | After `start()`, state is `playing`. After advancing 1 second, `timeRemaining` is approximately 119. Tick is 120. |
| Boot and state | Pause and resume | Start, advance 5s, pause, advance 5s, state remains paused, time unchanged, resume, advance 1s, time decreases by approximately 1. |
| Boot and state | Hidden tab pauses game | Start, advance 5s, `simulateVisibility(true)`, state paused, advance 5s, time unchanged, `simulateVisibility(false)`, state remains paused until `resume()`. |
| Level and navgrid | Level validation passes | `FE.Level.validate(FE.levelData)` does not throw. Compiled level has navgrid 64 x 36. |
| Level and navgrid | Win zone reachable | A* path exists from fridge start to win zone center. Path length > 0. |
| Level and navgrid | Room modifiers | Kitchen to kitchen 1.0, kitchen to hallway 0.5, hallway to living 0.5, kitchen to living 0.0. |
| Fridge movement | Unplug | Start, tap `KeyP`, fridge unplugged, noise event `unplug` recorded, audio hook `unplug` recorded, after 1s power approximately 99. |
| Fridge movement | Waddle forward | Start, unplug, hold `KeyW`, advance 1s, fridge x increased, speed <= 50, power approximately 96. |
| Fridge movement | Waddle backward | Start, unplug, hold `KeyS`, advance 1s, fridge x decreased. |
| Fridge movement | Rotation | Start, unplug, hold `KeyD`, advance 1s, angle increased by approximately 100 degrees, power approximately 97.5. |
| Fridge movement | Plugged fridge cannot move | Start, do not unplug, hold `KeyW`, advance 1s, position unchanged, power remains 100. |
| Fridge movement | Collision stops movement | Set fridge near wall, unplug, move into wall, fridge does not end inside wall, if impact speed > 30 collision noise emitted. |
| Slide | Slide success | Start, unplug, power 100, tap `Space`, slide active for approximately 0.25s, power 90, cooldown 0.6, noise `slide` recorded, audio `slide` recorded. |
| Slide | Slide cooldown | After slide, immediate `Space` does not start another slide. After 0.6s, slide can start if power allows. |
| Slide | Slide requires power | Set power 9, unplug, tap `Space`, slide does not start, `powerFlash` true. |
| Slide | Slide requires unplugged | Start, plugged, tap `Space`, slide does not start. |
| Plug system | Plug attempt success | Set fridge near kitchen outlet, unplugged, tap `KeyP`, plug attempt active, advance 0.5s, fridge plugged, power begins recharging. |
| Plug system | Plug attempt interrupted by movement | Set fridge near outlet, unplugged, tap `KeyP`, hold `KeyW`, advance 1 tick, plug attempt inactive, fridge unplugged. |
| Plug system | Plug attempt canceled by P | Set fridge near outlet, unplugged, tap `KeyP`, tap `KeyP` again, plug attempt inactive, fridge unplugged. |
| Plug system | No outlet nearby | Set fridge far from outlets, unplugged, tap `KeyP`, plug attempt inactive, no plug noise event. |
| Plug system | Recharge | Set fridge plugged, power 50, advance 1s, power approximately 65. |
| Door and hum | Door toggle | Start, tap `KeyE`, door open, door noise emitted, audio `door_open` recorded, tap `KeyE`, door closed, audio `door_close` recorded. |
| Door and hum | Door open drain | Unplug, open door, advance 1s, power approximately 98.5. |
| Door and hum | Hum requires door | Unplug, door closed, tap `KeyQ`, hum does not occur, no hum noise event. |
| Door and hum | Hum success | Unplug, open door, power 100, tap `KeyQ`, power 85, hum cooldown 3, noise `hum` radius 160 alert 100 recorded, audio `hum` recorded. |
| Door and hum | Hum cooldown | After hum, tap `KeyQ` again does not hum. After 3s, hum can occur again if door open and power sufficient. |
| Door and hum | Hum requires power | Set power 14, unplug, open door, tap `KeyQ`, hum does not occur, `powerFlash` true. |
| Noise system | Same room hearing | Create resident in kitchen, force noise in kitchen within radius, resident hears, suspicion at least alert, `lastKnown` equals noise position. |
| Noise system | Adjacent room hearing reduced | Resident in hallway, force kitchen noise radius 100, effective radius 50, resident at distance 40 hears, resident at distance 60 does not hear. |
| Noise system | Non-adjacent room no hearing | Resident in living room, force kitchen noise radius 200, resident does not hear. |
| Noise system | Loud noise triggers investigate | Routine resident, force noise alert 60, state becomes investigate, target equals noise position, `stats.residentsLured` includes resident id. |
| Noise system | Quiet noise triggers suspicious | Routine resident, force noise alert 20, state becomes suspicious, suspicion at least 20, resident not counted as lured. |
| Resident spawn | Mom spawns at 5 seconds | Start, advance 4.9s mom inactive, advance 0.2s mom active. |
| Resident spawn | Dad spawns at 10 seconds | Start, advance 9.9s dad inactive, advance 0.2s dad active. |
| Resident spawn | Kid spawns at 20 seconds | Start, advance 19.9s kid inactive, advance 0.2s kid active. |
| Resident perception | Normal fridge in kitchen not suspicious | Resident in kitchen, fridge plugged, stationary, door closed, in kitchen, advance 1s, suspicion remains 0. |
| Resident perception | Unplugged fridge in kitchen raises suspicion | Resident sees fridge, fridge unplugged and stationary in kitchen, advance 1s, suspicion increased by approximately 40. |
| Resident perception | Moving unplugged hallway fridge raises suspicion faster | Resident sees fridge, fridge unplugged, moving, hallway, advance 1s, suspicion increased by approximately 70. |
| Resident perception | Line of sight blocks suspicion | Place obstacle between resident and fridge, fridge abnormal, advance 1s, suspicion does not increase from sight. |
| Resident AI | Suspicious decays | Set resident suspicious with suspicion 50, make fridge not visible/abnormal, advance 1.5s, resident returns to routine, suspicion 0. |
| Resident AI | Investigate moves to target | Set resident investigate with target far away, advance enough ticks, resident moves toward target, after reaching target enters search. |
| Resident AI | Search returns to routine | Set resident search, advance 3s, state routine, suspicion 0. |
| Resident AI | Catch triggers lose | Start, set active resident within 40 units of fridge, advance 1 tick, state lose, lose reason caught. |
| Pathfinding | Resident path avoids obstacle | Set resident and target on opposite sides of obstacle, path exists, path does not pass through blocked cells. |
| Pathfinding | No path stops resident | Set fridge blocking only route, set resident investigate target across route, advance enough ticks, resident `hasPath` false, resident stops, game does not crash. |
| Win and lose | Win at front door | Start, set fridge in win zone, advance 1 tick, state win, stats include time used, noise events, residents lured. |
| Win and lose | Win priority over catch | Set fridge in win zone, set resident within 40, advance 1 tick, state win. |
| Win and lose | Power lose | Start, set fridge power 0, advance 1 tick, state lose, lose reason power. |
| Win and lose | Timer lose | Start, set time remaining 0, advance 1 tick, state lose, lose reason timer. |
| Win and lose | Power priority over timer | Set power 0 and time remaining 0, advance 1 tick, state lose, lose reason power. |
| HUD | Objective updates by room | Kitchen unplugged -> “Leave the kitchen.”, hallway -> “Cross the hallway.”, living room -> “Reach the front door.” |
| HUD | Timer warning | Set time remaining 31, advance 1s, `hud.timerWarning` true, audio hook `timer_warning` recorded once. |
| HUD | Power warning | Set power 26, unplug, advance enough to drop below 25, `hud.powerWarning` true, audio hook `power_warning` recorded once. |
| Stats | Noise event count | Start, unplug, open door, hum, `stats.noiseEvents` at least 3. |
| Stats | Residents lured unique count | Force loud noise heard by mom and dad, `stats.residentsLured` is 2, `luredIds` contains both, another loud noise heard by mom does not increase count. |
| Determinism | Same inputs produce same state | Reset, start, set seed, run same input sequence for 10 seconds, record state hash, reset, start, set same seed, run same sequence, state hash matches. |

Example determinism input sequence:

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

## 9.2 Tier 2 tests

| Test group | Test | Pass condition |
| --- | --- | --- |
| Audio hooks | SFX hooks fire | Each SFX event emits the expected hook: `slide`, `collision`, `plug`, `unplug`, `door_open`, `door_close`, `hum`, `suspicion`, `investigate`, `timer_warning`, `power_warning`, `win`, `lose`. |
| Audio hooks | Waddle loop | `waddle` loop starts when speed > 10 and not sliding, stops when speed <= 10 or sliding. |
| Audio hooks | Timer tick | `timer_tick` plays every second while timer < 30. |
| Audio hooks | Power buzz | `power_buzz` plays periodically while power < 25. |
| Audio hooks | Audio buffer bounded | Audio events do not exceed 4096; oldest dropped; stats not dropped. |
| Rendering | Canvas size | `#game-canvas` width is 1280 and height is 720. |
| Rendering | State overlays | Start, pause, win, and lose overlays show/hide based on state. |
| Rendering | HUD DOM updates | Objective, timer, power, plug, door, prompt, and controls update from state. |
| Rendering | Vignette | `#vignette` opacity/alpha follows `effects.vignetteIntensity` and visual formula. |
| Rendering | Noise rings | Noise events create `effects.noiseRings` with correct max radius and duration. |
| Rendering | Awareness icons | Suspicion 0 no icon, 1-99 eye icon opacity suspicion/100, 100 exclamation icon. |
| Rendering | Sight cones | If enabled, cone radius 160, FOV 120, clipped by sight rects. |
| Tutorial | Tutorial sequence | Tutorial prompts advance according to 7.3. |
| Tutorial | Prompt priority | Urgent prompts override tutorial prompts according to 7.4. |
| Accessibility | Colorblind pairing | Danger, power, plug, door, and noise use shape/icon/motion in addition to color. |
| Accessibility | Motion limits | No strobe above 3 flashes/sec. Timer and vignette pulse at 1 Hz. |

## 9.3 Tier 3 optional tests

| Test group | Test | Pass condition |
| --- | --- | --- |
| Performance | Sight cone fallback | If cones are disabled, resident facing indicator remains visible and awareness icons remain visible. |
| Performance | Frame stability | Production loop clamps dt to 0.1 seconds and does not skip win/lose checks. |
| Manual QA | Full manual script | A human or QA agent can complete the manual QA script without crash. |
| Optional assets | Procedural art | If procedural assets are used, they match palette and readability rules. |

# 10. BUILD ORDER

1. Create file layout and load classic scripts in order.
2. Implement `js/constants.js` with all gameplay numbers.
3. Implement `js/math.js` and `js/prng.js`.
4. Implement `js/level-data.js` with the fixed house.
5. Implement `js/level.js`:
   - compile level
   - validate level
   - build navgrid
   - room lookup
   - room modifier
   - solid/sight rects
6. Implement `js/collision.js`:
   - fridge OBB vs rect
   - resident circle vs rect
   - line of sight
7. Implement `js/pathfinding.js`:
   - A*
   - nearest walkable
   - fridge OBB dynamic blocking
8. Implement `js/input.js`:
   - production keyboard
   - debug held/tap
   - edge queue
9. Implement `js/fridge.js`:
   - movement
   - rotation
   - slide
   - plug/unplug
   - door
   - hum
   - power drain/recharge
10. Implement `js/noise.js`:
    - noise events
    - room modifier
    - hearing
    - stats
11. Implement `js/resident.js`:
    - spawn
    - perception
    - suspicion
    - AI states
    - pathfinding
    - catch
12. Implement `js/audio.js`:
    - hooks
    - recording
    - synthesized SFX/music for Tier 2
13. Implement `js/hud.js`:
    - minimal HUD
    - polished HUD for Tier 2
14. Implement `js/render.js`:
    - placeholder rendering for Tier 1
    - full visual rendering for Tier 2
15. Implement `js/game.js`:
    - state machine
    - fixed tick
    - win/lose priority
    - pause/resume/restart
16. Implement `js/debug.js` and `js/main.js`.
17. Implement `test/test.html` and `test/test.js`.
18. Pass all Tier 1 tests.
19. Build Tier 2 visual and audio systems.
20. Pass Tier 2 tests.
21. Optional Tier 3 polish, fallbacks, and manual QA.

# 11. DEFINITION OF DONE

## 11.1 Tier 1 done: playable core simulation

High level: The game is playable end-to-end and provably deterministic through `window.__game`.

Checkboxes:

- [ ] `index.html` loads without syntax errors.
- [ ] `test/test.html` loads without syntax errors.
- [ ] `window.__game` exists after load.
- [ ] `window.__game.ready` is true.
- [ ] Game starts in `start` state with correct fridge, timer, and resident state.
- [ ] Fixed 120 Hz tick loop works in production.
- [ ] Test mode does not run `requestAnimationFrame` or bind keyboard/visibility.
- [ ] Level validation passes.
- [ ] Navgrid is 64 x 36 using 20-unit tiles.
- [ ] Win zone is reachable by A*.
- [ ] Room lookup and room modifiers are correct.
- [ ] Fridge can unplug.
- [ ] Fridge can waddle forward and backward.
- [ ] Fridge can rotate.
- [ ] Plugged fridge cannot move, rotate, or slide.
- [ ] Fridge collision prevents overlap with solids.
- [ ] Hard collision emits collision noise when impact speed > 30.
- [ ] Slide works with speed 150, duration 0.25, cooldown 0.6, cost 10.
- [ ] Slide requires unplugged, power >= 10, cooldown ready, and no active plug attempt.
- [ ] Plug attempt works with radius 48 and duration 0.5.
- [ ] Plug attempt fails if interrupted by movement, rotation, slide, or P.
- [ ] Unplug is immediate and emits noise.
- [ ] Recharge is 15 power/sec while plugged.
- [ ] Unplugged passive drain is 1 power/sec.
- [ ] Waddle drain is +3 power/sec when `speedAbs > 1`.
- [ ] Rotate drain is +1.5 power/sec.
- [ ] Door open drain is +0.5 power/sec while unplugged.
- [ ] Door toggles with E and emits noise.
- [ ] Hum requires door open, power >= 15, cooldown ready.
- [ ] Hum costs 15, cooldown 3, radius 160, alert 100.
- [ ] Noise events use correct radius/alert values.
- [ ] Noise room modifiers are 1.0, 0.5, 0.0.
- [ ] Residents spawn at 5, 10, and 20 seconds.
- [ ] Resident spawn safety check prevents spawning within 40 units of fridge.
- [ ] Resident sight uses radius 160, FOV 120, LOS step 8.
- [ ] Anomaly detection uses unplugged, moving > 5, door open, not kitchen, within 80.
- [ ] Suspicion rates and decay are correct.
- [ ] Suspicious state resets after 1.5 seconds without abnormal detection.
- [ ] Investigate state moves to target at 110 units/sec.
- [ ] Search state lasts 3 seconds and returns to routine.
- [ ] Resident pathfinding avoids obstacles.
- [ ] Fridge OBB blocks resident path cells.
- [ ] No path causes resident to stop and face target.
- [ ] Catch occurs within 40 units.
- [ ] Timer starts at 120 and counts down while playing.
- [ ] Timer stops while paused.
- [ ] Win occurs in win zone.
- [ ] Lose occurs by caught, power, or timer.
- [ ] Win priority is above caught, power, and timer.
- [ ] Power priority is above timer when both occur.
- [ ] Start, Playing, Paused, Win, and Lose states work.
- [ ] Escape pauses and resumes.
- [ ] Hidden tab pauses when playing.
- [ ] Restart returns to a fresh Playing state.
- [ ] Reset returns to Start state.
- [ ] Minimal HUD shows objective, timer, power, plug, door, prompt.
- [ ] Win screen shows time used, noise events, residents lured.
- [ ] Lose screen shows correct lose reason.
- [ ] Debug API exposes all required methods.
- [ ] `setFridge`, `setResident`, `setTimeRemaining`, and `forceNoise` work.
- [ ] `setHeld`, `clearHeld`, and `tap` work.
- [ ] Audio hooks are recorded even if audio is silent.
- [ ] Required Tier 1 tests pass.

## 11.2 Tier 2 done: readable stealth presentation

High level: The game looks and sounds like a finished domestic stealth escape.

Checkboxes:

- [ ] Kitchen, hallway, and living room have distinct floor tones, lighting, and furniture.
- [ ] Fridge is the clearest object on screen.
- [ ] Fridge LED communicates plugged, unplugged, low power, hum, caught, and depleted states.
- [ ] Fridge cord visually communicates plug state.
- [ ] Plug range circle appears at radius 48 when unplugged near outlet.
- [ ] Plug connection arc fills over 0.5 seconds.
- [ ] Door open shows light spill and cyan glow.
- [ ] Waddle, slide, and collision animations match section 3.8.
- [ ] Slide and hum cooldown arcs are visible.
- [ ] Low power visuals appear below 25 and below 10.
- [ ] Residents are visually distinct: Mom, Dad, Kid.
- [ ] Residents have facing indicators.
- [ ] Resident spawn fades in over 0.3 seconds.
- [ ] Resident states have distinct visuals.
- [ ] Sight cones are clipped by sight-blocking rects or fallback indicator is used.
- [ ] Awareness icons show eye/exclamation with correct opacity and pop.
- [ ] Noise rings use correct radius, color, duration, and line width.
- [ ] Hum ring is visibly larger and cyan.
- [ ] Hearing ticks appear above residents that hear noise.
- [ ] Warning vignette appears above max suspicion 50 and follows visual alpha formula.
- [ ] Vignette pulses at max suspicion 100.
- [ ] Screen shake is limited to hard collision and caught.
- [ ] HUD uses required DOM ids.
- [ ] HUD layout matches section 7.2.
- [ ] Timer pulses red below 30 seconds.
- [ ] Power bar uses green/amber/red and flashes below 25.
- [ ] Plug and door icons are readable without color alone.
- [ ] Contextual prompt uses keycaps and priority rules.
- [ ] Tutorial prompts follow section 7.3.
- [ ] Controls reminder fades after 10 seconds and returns when paused.
- [ ] Start screen shows title, subtitle, controls, and Play button.
- [ ] Pause screen shows Resume and Restart.
- [ ] Win screen shows required stats and Play Again.
- [ ] Lose screen shows required reason and Retry.
- [ ] Synthesized SFX match section 6.1.
- [ ] Synthesized music layers match section 6.2.
- [ ] Music crossfades and ducking follow section 6.
- [ ] Colorblind support does not rely on color alone.
- [ ] Motion rules prevent strobing above 3 flashes/sec.
- [ ] Required Tier 2 tests pass.

## 11.3 Tier 3 done: optional polish and fallbacks

High level: Optional production polish is complete, but the game is already done after Tier 2.

Checkboxes:

- [ ] Optional procedural asset generation matches palette and readability.
- [ ] Performance fallbacks for sight cones are implemented if needed.
- [ ] Manual QA script can be completed without crash.
- [ ] Optional UI hover/click sounds are present and non-disruptive.
- [ ] Extra visual flourishes do not alter gameplay values.

# A. SANITY

| Check | Result | Notes / correction |
| --- | --- | --- |
| Section headings are present in required order | Valid | `# 0` through `# 11` and `# A` are present. |
| User request is covered | Valid | Sentient fridge escaping a house is the core game. |
| Gameplay numbers are carried | Valid | Timer, speeds, drains, noise, suspicion, spawn, catch, win zone, and map numbers are present. |
| Disagreement: nav tile 32 vs 20 | Ruled | 20 is used for pathfinding/validation. 32 is visual only. |
| Disagreement: wall thickness 16 vs 20 | Ruled | Collision uses 20-unit engineering walls. Visual face may be 16. |
| Disagreement: visual entity sizes vs colliders | Ruled | Colliders remain authoritative; visual sizes are presentation only. |
| Disagreement: vignette formula | Ruled | State stores normalized intensity; renderer uses visual alpha formula. |
| Disagreement: tutorial prompt sequence | Ruled | Merged tutorial table in 7.3. |
| Disagreement: prompt priority | Ruled | Merged priority in 7.4. |
| Disagreement: audio asset manifest | Ruled | External assets dropped from required build; synthesized audio is default. |
| Gap: collision audio hook | Fixed | Added `collision` hook. |
| Gap: timer tick vs timer warning | Fixed | `timer_warning` is one-shot crossing; `timer_tick` is per-second below 30. |
| Gap: power warning vs low buzz | Fixed | `power_warning` is one-shot crossing; `power_buzz` is optional periodic. |
| Gap: resident spawn safety | Carried | Engineering spawn safety check is required. |
| Gap: fridge as path obstacle | Ruled | Actual fridge OBB blocks nav cells. |
| Gap: suspicious decay test expectation | Fixed | Suspicious state resets suspicion to 0 after 1.5 seconds without abnormal detection. |
| State shape includes gameplay fields | Valid | Fridge, resident, stats, effects, and HUD fields are present. |
| Debug API has system-specific functions | Valid | `setFridge`, `setResident`, `setTimeRemaining`, `forceNoise`, and input functions are present. |
| Tests are tied to tiers | Valid | Tier 1, Tier 2, and optional Tier 3 tests are listed. |
| Definition of done matches tiers | Valid | Tier 1, Tier 2, and Tier 3 done lists align with section 0.3. |
| Presentation does not alter simulation | Valid | Visual and audio sections explicitly preserve gameplay authority. |
| No build step required | Valid | Vanilla HTML/CSS/JS classic scripts only. |
| Dropped items documented | Valid | Cut items and dropped optional items are listed in 0.2. |