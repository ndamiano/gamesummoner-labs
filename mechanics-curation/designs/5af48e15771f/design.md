# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Prompt: lighthouse keeper on a stormy night, swinging the beam to steer ships past the rocks while keeping the lamp fuelled | §4.1 Upkeep, §4.2 Multitasking, §4.3 Escort, §5 Characters |
| 2d | §1.1 Units, axes, frames; §2 Contracts; §3 Visual Spec |
| side-on camera | §3 Visual Spec; §4.3 Escort; §5 Characters |
| real-time | §1.2 Important conventions; §2.2 Global context; §4.3 Escort |
| no movement, cursor only | §1.2 Important conventions; §2.3 Module specifics; §4.2 Multitasking; §7 UX |
| single screen | §1.1 Units, axes, frames; §3 Visual Spec; §7 UX |
| failure: lose a life | §4.3 Escort; §4.4 Lives and failure; §9 Tests |
| tense tone | §3 Visual Spec; §4.5 Feel; §6 Audio |
| one screen, a few minutes | §1.1 Units, axes, frames; §4.4 Progression and difficulty; §9 Tests |
| survive as long as possible | §4.4 Progression and difficulty; §7 UX; §9 Tests |
| core mechanics: upkeep, multitasking, escort | §0.3 Tiers; §4.1 Upkeep; §4.2 Multitasking; §4.3 Escort |
| supporting mechanics: none | §0.2 Decisions; §0.3 Tiers; §4.3 Escort |
| extra mechanics: none | §0.2 Decisions; §0.3 Tiers; §4.3 Escort |
| art style: hand-drawn / painterly: brush strokes, ink lines or watercolour texture | §3 Visual Spec; §5 Characters |
| palette: dark: mostly black with a few bright accents | §3 Visual Spec; §7 UX |
| typography: hand-lettered: drawn, irregular letters | §3 Visual Spec; §7 UX |
| music: ambient: slow textures, no strong beat | §6 Audio |
| sound effects style: realistic: recorded-sounding impacts and foley | §6 Audio |
| screens: title, game over | §7 UX |
| hud: none | §3 Visual Spec; §7 UX |
| effects: screen shake, particles, hit flash, trails, bloom | §3 Visual Spec; §2.3 Module specifics; §4.3 Escort |
| accessibility: colour-blind safe palette, reduced motion, difficulty options | §0.2 Decisions; §0.3 Tiers; §4.4 Progression and difficulty; §7 UX; §9 Tests |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| Prompt is final | The game is a fixed-screen storm survival game. | It satisfies the requested high concept without adding systems. |
| Dimension | 2D canvas, fixed camera, no scrolling. | Requested dimension and single screen. |
| Camera | Side-on, fixed. | Requested camera. |
| Time model | Real-time, no pause screen, no slow motion, no time control. | Requested real-time and only title/game-over screens. |
| Movement model | Player does not move any entity. The pointer aims the lamp beam. Holding the primary pointer button while inside the pump refuels. | Requested cursor-only input. Pumping is still cursor-only. |
| Session shape | One screen, one run, no level transitions. | Requested single screen. |
| Failure | A life is lost when a ship hits a rock, or when the lamp stays out too long. | Requested failure: lose a life. |
| Win/lose | No win. Game over when lives reach 0. Final time is shown on the game-over screen. | Requested survive as long as possible. |
| Player identity | The player is the lighthouse keeper, represented only by the cursor and the lamp/pump controls. No visible keeper sprite. | Preserves no-movement, cursor-only design. |
| Core mechanics | Exactly three: upkeep, multitasking, escort. | Requested core mechanics. |
| Supporting mechanics | None. | Requested none. |
| Extra mechanics | None. | Requested none. |
| Enemies | No enemies. Ships are escort targets, not enemies. | Prompt says steer ships, not fight them. |
| Traps | Two rock clusters, each with one collision circle. | Concrete hazard count while preserving simple single-screen play. |
| Pickups | None. | Requested none. |
| Lives | Three lives on all difficulties. | Keeps failure simple and consistent. |
| Lives display | Three small lamp wicks on the lamp fixture are extinguished as lives are lost. | No HUD, but status remains visible. |
| Fuel display | A vertical oil tube on the lighthouse shows amber fuel level. | No HUD, but status remains visible. |
| Beam display | The beam is a visible wedge from the lamp to the pointer. A brighter faint centerline is drawn for guidance. | The core escort input must be visible. |
| Pump display | A circular pump valve area on the lighthouse base. It glows amber when active. | Makes the upkeep input visible. |
| Canvas size | Logical canvas 1280×720, scaled to fit browser. | Gives fixed coordinates for all numbers. |
| Coordinate origin | Top-left, x right, y down. | Standard 2D canvas convention. |
| Fixed step | 60 Hz fixed timestep, max 5 substeps per rendered frame. | Deterministic real-time simulation. |
| RNG | Seeded `mulberry32` PRNG. | Reproducible spawning and tests. |
| External assets | No external art, fonts, or audio files. All visuals are procedural canvas drawing and all audio is synthesized. | Browser-game scope and audio API requirement. |
| HUD | No overlay HUD. All status is diegetic on the lighthouse. | Requested HUD: none. |
| Screens | Title and game over only. Difficulty and reduced-motion options are on the title screen. | Requested screens and accessibility. |
| Difficulty options | Easy, Normal, Hard multipliers for drain, refill, ship speed, spawn interval, guidance, beam width, pump radius, and lamp-out grace. | Requested difficulty options without adding mechanics. |
| Reduced motion | Enabled by default if the browser reports `prefers-reduced-motion`. Reduces shake, flash, bloom, particles, rain, and lamp flicker. | Requested accessibility. |
| Colour-blind safe palette | Dark base with amber, cyan, violet, and white accents. No red/green state signalling. | Requested colour-blind safe palette. |
| Typography | Hand-lettered UI text using SVG paths or CSS-transformed glyph fragments. Fallback system cursive with per-character rotation and jitter. | Requested hand-lettered typography. |
| Music | Continuous synthesized ambient storm drone and wind texture. No beat. | Requested ambient music with no strong beat. |
| Sound effects | Synthesized noise-based foley for impacts, pumping, water, lamp events. | Requested realistic recorded-sounding foley. |
| Effects | Screen shake, particles, hit flash, trails, and bloom are present in Tier 1 at a basic level and improved in Tier 2/3. | Requested effects. |
| Expected normal run length | 2–4 minutes median, with later phases becoming harder. | Requested a few minutes. |
| Safe ship passage | A ship reaching the left harbour edge is removed safely. No fuel or life reward. | Avoids adding a pickup or reward mechanic. |
| Ship-ship collision | None. Ships pass through each other. | Not requested; avoids adding a system. |
| Lighthouse collision | Ships do not collide with the lighthouse. They exit safely at the harbour edge. | Keeps hazards limited to requested rocks. |
| Pause | No pause UI. Browser rAF stopping is not treated as a game pause. | Only title and game-over screens are allowed. |
| Settings persistence | Not required. Settings are title-screen state only. | Avoids adding systems not requested. |

## 0.3 Tiers

| Tier | Scope | Mechanics added | Higher-tier dependencies | Done when |
| --- | --- | --- | --- | --- |
| Tier 1 | Core game only: title, playing, game over, fixed loop, seeded RNG, lighthouse lamp, fuel upkeep, cursor beam, pump, two rocks, ship escort, lives, diegetic status, required accessibility defaults, basic hand-drawn visuals, basic synthesized audio, basic required effects. | Exactly the three core mechanics: upkeep, multitasking, escort. | None. | A player can start from title, play a full run, lose lives, and see game over with survival time. |
| Tier 2 | Hardening and accessibility completion: full difficulty option behaviour, reduced-motion polish, focus-visible UI, colour palette audit, robust pointer handling, deterministic test hooks. | No new mechanics. | Tier 1. | Difficulty and reduced-motion options work correctly; UI is keyboard accessible; palette and contrast pass checks. |
| Tier 3 | Advanced juice: richer bloom, trails, particles, water animation, rain texture, audio layering, performance stability. | No new mechanics. | Tier 1 and preferably Tier 2. | Visual/audio polish improves feel without changing gameplay rules. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Item | Value | Notes |
| --- | --- | --- |
| Logical canvas width | 1280 px | Fixed world width. |
| Logical canvas height | 720 px | Fixed world height. |
| World coordinate origin | 0,0 top-left | Canvas convention. |
| x axis | Positive right | Ships move negative x. |
| y axis | Positive down | Beam angles positive downward. |
| Speed units | px/s | Used for ships and particles. |
| Acceleration units | px/s² | Used for steering. |
| Angle units | Internal radians; documented degrees. | 0° = horizontal right; positive = downward. |
| Time unit | seconds | Simulation time. |
| Fixed timestep | 1/60 s = 0.0166667 s | All gameplay rules use this dt. |
| Max substeps per frame | 5 | Prevents runaway catch-up. |
| Render frame budget | Best effort | Gameplay updates are fixed step. |
| Sea top | y = 360 | Water surface line. |
| Sea bottom clamp | y = 720 | Visual bottom; ship centre clamp is y = 684. |
| Harbour safe exit x | x <= 260 | Ship is removed safely. |
| Spawn x | x = 1240 | Right edge, inside canvas. |
| Lamp position | x = 150, y = 300 | Beam origin. |
| Lighthouse visual bounds | x 90–210, y 300–720 | Non-colliding. |
| Pump position | x = 150, y = 600 | Centre of pump interaction. |
| Pump radius normal | 36 px | Cursor interaction radius. |
| Beam length | 1300 px | From lamp. |
| Beam min angle | 0° | Horizontal right. |
| Beam max angle | 80° | Down-right, covers near shore and far sea. |
| Beam half-width normal | 36 px | Guidance and visual half width. |
| Ship radius | 16 px | Collision circle. |
| Rock collision radius normal | 24 px | Rock collision circle. |
| Rock visual radius normal | 36 px | Painterly silhouette larger than collision. |
| Fuel max | 100 units | No HUD units shown. |
| Fuel normal drain | 0.9 units/s | Normal difficulty. |
| Fuel normal refill | 24 units/s | Normal difficulty. |
| Ship normal base speed range | 95–145 px/s | Increases with progression. |
| Ship normal guided max vy | 180 px/s | Beam steering cap. |
| Ship normal unguided max vy | 55 px/s | Rock-drift cap. |
| Guided acceleration normal | 320 px/s² | Beam guidance. |
| Unguided acceleration normal | 140 px/s² | Rock drift. |
| Lamp out grace normal | 1.5 s | Before life loss. |
| Recovery transition duration | 2.0 s | After each life loss; no new lives lost during transition. |

## 1.2 Important conventions

| Convention | Rule |
| --- | --- |
| Single source of time | All gameplay uses accumulated fixed-step dt. Render interpolation is optional. |
| Single source of randomness | `rng.float()`, `rng.int(min, max)`, and `rng.choice(array)` only. Seed is set at run start. |
| No gameplay pause | There is no pause state. Browser tab visibility may stop rAF, but no pause UI or mechanic is added. |
| Cursor only | The pointer is the only gameplay input. No keyboard gameplay input. UI may be keyboard accessible. |
| No HUD | No DOM overlay or canvas overlay HUD during playing. Status is drawn on the lighthouse world objects. |
| No new systems | Tier 2 and Tier 3 must not add mechanics. They only refine the three core mechanics and required presentation/accessibility. |
| Deterministic tests | Tests must seed RNG and use debug commands rather than private internals. |
| Fixed world | Camera never moves. All positions are absolute canvas coordinates. |
| Reduced motion | When enabled, remove screen shake, hit flash, bloom, non-essential particles, rain motion, and lamp flicker. Gameplay numbers remain unchanged. |
| Colour communication | Use shape, position, and luminance. Amber = fuel/lamp. Cyan = guidance/safe. Violet = danger/rock warning. White = impact/feedback. |
| Audio start | Audio context may be created on first user interaction, normally title start click. |
| Safe exit | Ship removal at x <= 260 is safe and does not affect lives or fuel. |
| Collision priority | If a life loss starts a transition, later collisions in the same fixed step are ignored. |
| Difficulty | Difficulty multipliers apply only to gameplay numbers, not to input model or screens. |

# 2. CONTRACTS

## 2.1 Module layout

| File | Responsibility |
| --- | --- |
| `index.html` | Canvas element, DOM title/game-over screens, accessibility controls. |
| `styles.css` | Dark UI, hand-lettered text styling, focus states, reduced-motion CSS. |
| `main.js` | Bootstraps canvas, modules, fixed loop, screen state. |
| `constants.js` | All numeric constants from this spec. |
| `rng.js` | Seeded `mulberry32` PRNG and helpers. |
| `input.js` | Pointer position and primary button state. |
| `state.js` | Global context, run state, screen state, settings. |
| `world.js` | Fixed world layout, rocks, reset run. |
| `lamp.js` | Fuel, lamp lit state, lamp out grace, relight, fuel visual state. |
| `pump.js` | Pump hit test and refuel accumulation. |
| `beam.js` | Pointer-to-angle conversion, beam geometry, guidance hit test. |
| `escort.js` | Ship spawning, ship physics, drift, guidance, collisions, safe exit. |
| `rocks.js` | Rock data and collision tests. |
| `lives.js` | Lives, transition, game over trigger. |
| `fx.js` | Screen shake, hit flash, particles, trails, bloom. |
| `audio.js` | Web Audio graph, ambient textures, synthesized foley. |
| `ui.js` | Title/game-over DOM state, difficulty and reduced-motion controls. |
| `debug.js` | One debug entry point per gameplay system. |
| `tests.js` | High-level validation tests. |

## 2.2 Global context

All modules access one global context object. The object is created in `state.js` and stored as `window.GAME`.

| Path | Type | Initial value | Used by |
| --- | --- | --- | --- |
| `runtime.fixedDt` | number | 0.0166667 | engine, tests |
| `runtime.maxSubsteps` | number | 5 | engine |
| `runtime.frame` | integer | 0 | debug |
| `runtime.timeSurvived` | number | 0 | lives, game over |
| `runtime.transitionTimer` | number | 0 | lives, spawn, collision |
| `runtime.spawnTimer` | number | 0 | escort |
| `runtime.patternIndex` | integer | 0 | escort |
| `runtime.activeShipCount` | integer | 0 | escort |
| `rng.seed` | integer | derived from `performance.now()` or test seed | rng |
| `rng.nextFloat()` | function | returns [0,1) | escort, fx |
| `rng.nextInt(min, max)` | function | returns integer inclusive | escort |
| `rng.choice(array)` | function | returns item | escort |
| `settings.difficulty` | string | `"normal"` | lamp, escort, beam, pump |
| `settings.reducedMotion` | boolean | from media query | fx, render, ui |
| `settings.colorSafe` | boolean | true | render, ui |
| `screen` | string | `"title"` | ui, engine |
| `lives.count` | integer | 3 | lives, render |
| `lives.max` | integer | 3 | lives |
| `lives.transitioning` | boolean | false | lives, escort, collision |
| `lamp.x` | number | 150 | beam, render |
| `lamp.y` | number | 300 | beam, render |
| `lamp.fuel` | number | 100 | lamp, render, debug |
| `lamp.maxFuel` | number | 100 | lamp |
| `lamp.drainRate` | number | 0.9 | lamp, difficulty |
| `lamp.lit` | boolean | true | beam, lamp |
| `lamp.outTimer` | number | 0 | lamp, lives |
| `lamp.outGrace` | number | 1.5 | lamp, difficulty |
| `lamp.intensity` | number | 1 | render, beam visual |
| `lamp.guidanceFactor` | number | 1 | beam guidance |
| `lamp.wicks` | array | `[true,true,true]` | render, lives |
| `pump.x` | number | 150 | pump, render |
| `pump.y` | number | 600 | pump, render |
| `pump.radius` | number | 36 | pump, difficulty |
| `pump.refillRate` | number | 24 | pump, difficulty |
| `pump.active` | boolean | false | pump, fx, audio |
| `beam.angle` | number | radians | beam, render |
| `beam.minAngle` | number | 0 | beam |
| `beam.maxAngle` | number | 80 degrees in radians | beam |
| `beam.length` | number | 1300 | beam, render |
| `beam.halfWidth` | number | 36 | beam, difficulty |
| `beam.active` | boolean | true | beam, escort |
| `cursor.x` | number | 640 | input, beam, pump |
| `cursor.y` | number | 360 | input, beam, pump |
| `cursor.buttonDown` | boolean | false | input, pump |
| `cursor.insidePump` | boolean | false | pump |
| `ships` | array | [] | escort, render, debug |
| `rocks` | array | two rock records | escort, render |
| `particles` | array | [] | fx, render |
| `fx.shake.x` | number | 0 | render |
| `fx.shake.y` | number | 0 | render |
| `fx.shake.time` | number | 0 | render |
| `fx.shake.mag` | number | 0 | render |
| `fx.hitFlash.time` | number | 0 | render |
| `fx.hitFlash.strength` | number | 0 | render |
| `fx.bloom.strength` | number | 0.35 | render |
| `fx.trails` | array | [] | render |
| `spawn.schedule` | array | normal schedule | escort |
| `spawn.interval` | number | 5.5 | escort, difficulty |
| `spawn.speed` | number | 95 | escort, difficulty |
| `spawn.maxActive` | integer | 1 | escort |
| `spawn.patterns` | array | normal patterns | escort |
| `audio.enabled` | boolean | true | audio |
| `finalTime` | number | 0 | ui, game over |

### Record schemas

| Record | Fields | Purpose |
| --- | --- | --- |
| `Ship` | `id`, `x`, `y`, `vx`, `vy`, `r`, `targetRockIndex`, `guided`, `alive`, `safe`, `bobPhase` | Escort target. |
| `Rock` | `id`, `x`, `y`, `r`, `visualR`, `type` | Fixed hazard. |
| `SpawnPattern` | `targetRockIndex`, `spawnY` | Spawn behaviour. |
| `Particle` | `id`, `x`, `y`, `vx`, `vy`, `life`, `maxLife`, `type`, `color` | Visual effect. |
| `Trail` | `x`, `y`, `age`, `maxAge`, `kind` | Beam or wake trail. |
| `Wick` | `id`, `lit`, `x`, `y`, `flickerPhase` | Life display. |

## 2.3 Module specifics

| Module | Function | Signature | Purpose |
| --- | --- | --- | --- |
| `main.js` | `boot` | `boot(canvas)` | Create modules, bind UI, start loop. |
| `main.js` | `startRun` | `startRun(difficulty)` | Reset run and set screen to playing. |
| `main.js` | `update` | `update(realDt)` | Accumulate fixed steps. |
| `main.js` | `render` | `render()` | Draw world and effects. |
| `rng.js` | `seed` | `seed(integer)` | Set deterministic RNG. |
| `rng.js` | `float` | `float()` | PRNG float. |
| `rng.js` | `int` | `int(min, max)` | PRNG integer. |
| `rng.js` | `choice` | `choice(array)` | PRNG array selection. |
| `input.js` | `setPointer` | `setPointer(x, y)` | Update cursor world position. |
| `input.js` | `setPointerDown` | `setPointerDown(button)` | Primary button down. |
| `input.js` | `setPointerUp` | `setPointerUp()` | Primary button up. |
| `input.js` | `getPointer` | `getPointer()` | Return cursor record. |
| `input.js` | `isPumpHeld` | `isPumpHeld()` | Return whether pump input is active. |
| `state.js` | `getState` | `getState()` | Return global context. |
| `state.js` | `setScreen` | `setScreen(name)` | Change screen state. |
| `state.js` | `addRunTime` | `addRunTime(dt)` | Increment survival time. |
| `world.js` | `resetRun` | `resetRun(difficulty)` | Reset run fields, apply difficulty. |
| `world.js` | `createRocks` | `createRocks()` | Return fixed rocks. |
| `lamp.js` | `updateFuel` | `updateFuel(dt)` | Drain fuel, update lamp states. |
| `lamp.js` | `setFuel` | `setFuel(value)` | Set fuel for tests/debug. |
| `lamp.js` | `getFuel` | `getFuel()` | Return fuel. |
| `lamp.js` | `setLit` | `setLit(boolean)` | Force lamp lit state. |
| `lamp.js` | `relight` | `relight(fuel)` | Turn lamp on and clear out timer. |
| `lamp.js` | `goOut` | `goOut()` | Turn lamp off and start out timer. |
| `lamp.js` | `updateGuidanceFactor` | `updateGuidanceFactor()` | Compute guidance factor from fuel. |
| `pump.js` | `updatePump` | `updatePump(dt)` | Add fuel if active. |
| `pump.js` | `isInPump` | `isInPump(x, y)` | Hit-test pump circle. |
| `pump.js` | `setActive` | `setActive(boolean)` | Force pump state. |
| `beam.js` | `aimFromPointer` | `aimFromPointer()` | Convert cursor to angle. |
| `beam.js` | `setAngle` | `setAngle(degrees)` | Force beam angle. |
| `beam.js` | `getAngle` | `getAngle()` | Return angle. |
| `beam.js` | `centerYAt` | `centerYAt(x)` | Return beam centre y at x. |
| `beam.js` | `distanceToShip` | `distanceToShip(ship)` | Return distance from ship centre to beam centreline. |
| `beam.js` | `isActive` | `isActive()` | Return beam active. |
| `escort.js` | `updateSpawn` | `updateSpawn(dt)` | Update timers, patterns, spawn ships. |
| `escort.js` | `spawnShip` | `spawnShip(targetRockIndex, spawnY, speed)` | Create ship. |
| `escort.js` | `updateShips` | `updateShips(dt)` | Move, guide, collide, remove. |
| `escort.js` | `applyGuidance` | `applyGuidance(ship, dt)` | Beam steering. |
| `escort.js` | `applyDrift` | `applyDrift(ship, dt)` | Rock drift. |
| `escort.js` | `collideShip` | `collideShip(ship)` | Rock collision check. |
| `escort.js` | `safeExit` | `safeExit(ship)` | Safe removal. |
| `rocks.js` | `getRocks` | `getRocks()` | Return rocks. |
| `rocks.js` | `getRock` | `getRock(id)` | Return one rock. |
| `rocks.js` | `setRocks` | `setRocks(array)` | Replace rocks for tests. |
| `rocks.js` | `collideShipWithRock` | `collideShipWithRock(ship)` | Return rock or null. |
| `lives.js` | `get` | `get()` | Return lives count. |
| `lives.js` | `set` | `set(n)` | Set lives for tests. |
| `lives.js` | `lose` | `lose(reason)` | Decrement life, start transition or game over. |
| `lives.js` | `startTransition` | `startTransition()` | Set transition timer. |
| `fx.js` | `shake` | `shake(mag, duration)` | Add screen shake. |
| `fx.js` | `hitFlash` | `hitFlash(strength, duration)` | Add flash. |
| `fx.js` | `particles` | `particles(type, x, y, count)` | Add particles. |
| `fx.js` | `trail` | `trail(x, y, kind)` | Add trail. |
| `fx.js` | `setBloom` | `setBloom(strength)` | Set bloom. |
| `audio.js` | `init` | `init()` | Create AudioContext on user gesture. |
| `audio.js` | `startAmbient` | `startAmbient()` | Start storm ambient. |
| `audio.js` | `stopAmbient` | `stopAmbient()` | Stop ambient. |
| `audio.js` | `play` | `play(name)` | Play synthesized sound. |
| `ui.js` | `showTitle` | `showTitle()` | Show title screen. |
| `ui.js` | `showGameOver` | `showGameOver(finalTime)` | Show game over. |
| `ui.js` | `hideScreens` | `hideScreens()` | Hide DOM screens. |
| `ui.js` | `setDifficulty` | `setDifficulty(value)` | Store difficulty. |
| `ui.js` | `setReducedMotion` | `setReducedMotion(value)` | Store reduced motion. |
| `debug.js` | `upkeep` | `upkeep(command, value)` | One debug entry for lamp/fuel. |
| `debug.js` | `escort` | `escort(command, value)` | One debug entry for ships/rocks/spawn. |
| `debug.js` | `lives` | `lives(command, value)` | One debug entry for lives. |
| `debug.js` | `input` | `input(command, value)` | One debug entry for cursor/pump input. |
| `debug.js` | `fx` | `fx(command, value)` | One debug entry for effects. |
| `tests.js` | `runAll` | `runAll()` | Run all tier tests. |
| `tests.js` | `runTier1` | `runTier1()` | Validate core. |
| `tests.js` | `runTier2` | `runTier2()` | Validate difficulty/accessibility. |
| `tests.js` | `runTier3` | `runTier3()` | Validate polish without gameplay changes. |

# 3. VISUAL SPEC

The game is a dark, hand-painted storm tableau. A squat lighthouse sits on the left, its lamp the only warm amber source. A wide sea fills the right side, rendered as layered black-blue brush strokes, faint rain, and broken white foam. The player’s cursor is not drawn as a cursor during play; it is felt through the beam, which is a translucent amber wedge with a faint cyan-safe centerline. Ships are small dark silhouettes with pale sails, drifting toward two jagged rock clusters. Status is diegetic: fuel is an amber tube on the lighthouse, lives are small wick flames on the lamp fixture, and the pump valve glows when held. The screen is mostly black, with only amber, cyan, violet, and white accents carrying meaning.

Lighting and atmosphere: the lamp is the key light. The beam is additive and bloom-like, but the world remains dark. Rain is faint vertical streaks. Waves are low-contrast horizontal brush strokes. Rocks have a violet danger halo only when a ship is near. When reduced motion is on, rain and waves become static textures, shake is disabled, bloom is reduced, and lamp flicker is removed.

Space: fixed side-on view. Left shore and lighthouse occupy x 0–250. The sea occupies x 260–1280. Water surface is y 360. Ships move from right to left inside the sea band. Rock clusters are fixed at their coordinates below. The harbour safe edge is at x 260. There is no camera movement.

| Element | Silhouette / shape | Palette | Stroke / texture | Animation / juice |
| --- | --- | --- | --- | --- |
| Sky | Dark gradient, cloud smudges | `#070a0e` to `#0d131b` | Watercolour noise, soft brush clouds | Very slow horizontal drift unless reduced motion. |
| Lighthouse | Squat tower, lamp room, base | Body `#141a22`, ink `#020406`, rim `#243041` | Brush strokes, ink outline | Static; tiny sway only when shake occurs. |
| Lamp fixture | Circular lantern with three wicks | Flame `#ffd166`, core `#fff4c2` | Soft glow, additive | Flicker by fuel; wicks extinguish on life loss. |
| Oil fuel tube | Vertical glass tube on tower | Empty `#0e1218`, fuel `#f4a259`, highlight `#ffd166` | Ink outline, glass shine | Level decreases smoothly; amber pulse when low. |
| Pump valve | Circular valve/handle on base | Base `#1a2230`, active glow `#ffd166` | Thick ink circle, handle strokes | Handle pumps downward while active; amber particles. |
| Beam | Wedge from lamp to pointer | Outer `rgba(255,221,136,0.18)`, centerline `rgba(122,215,255,0.45)` | Soft additive, noisy light texture | Follows cursor instantly; trails when swinging; dim/flicker by fuel. |
| Sea | Layered horizontal wave bands | Deep `#0f1722`, mid `#182635`, foam `#cfe3f2` | Brush strokes, watercolour bleed | Slow horizontal motion; reduced motion static. |
| Rocks | Jagged clusters, two total | Rock `#1a2230`, edge `#2a3444`, danger halo `#b892ff` | Heavy ink outline, cracked highlights | Violet halo when ship within 120 px. |
| Ships | Small hull, single pale sail | Hull `#2b3240`, sail `#aebfd2`, ink `#05070a` | Ink outline, brush wake | Bob phase, wake trail, lean toward guided direction. |
| Particles | Sparks, foam, embers | Fuel `#ffd166`, foam `#cfe3f2`, impact `#f3f7fb`, danger `#b892ff` | Soft circles | Short-lived, physics-simulated. |
| Hit flash | Full-screen overlay | `rgba(243,247,251,0.12)` or `rgba(184,146,255,0.10)` | None | Decays over 0.25 s. |
| Title text | Hand-lettered lighthouse/keeper mark | `#f3f7fb`, accents `#ffd166`, `#7ad7ff` | Irregular SVG strokes | Static; no motion. |
| Game over text | Hand-lettered time | `#f3f7fb`, time `#ffd166` | Irregular SVG strokes | Static. |

# 4. GAMEPLAY SPEC

The player is the lighthouse keeper. The cursor aims the lamp beam. Ships enter from the right and drift toward two rocks. The player keeps the lamp fuelled by holding the pointer inside the pump valve, but doing so points the beam away from the sea. The player must alternate between refuelling and guiding ships through the safe channel between the rocks. A ship hitting a rock costs one life. If the lamp runs out of fuel for too long, it costs one life. The run ends after three lives are lost. The only score is survival time.

## Rosters

| Roster | Count | Records |
| --- | --- | --- |
| Ships | One ship type, dynamic count | `Ship` |
| Rocks / traps | 2 | `Rock` id 0 upper, id 1 lower |
| Pickups | 0 | None |
| Pumps | 1 | `pump` |
| Lamps | 1 | `lamp` |
| Lives | 3 max | `lives` |

### Rock roster

| id | Name | x | y | collision r | visual r | Behaviour |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | Upper Rock | 880 | 450 | 24 | 36 | Ships target this rock when `targetRockIndex = 0`. |
| 1 | Lower Rock | 740 | 650 | 24 | 36 | Ships target this rock when `targetRockIndex = 1`. |

### Ship roster

| Type | r | spawn x | safe exit x | x speed | target behaviour |
| --- | --- | --- | --- | --- | --- |
| Storm ship | 16 | 1240 | <= 260 | 95–145 px/s base | Drifts toward target rock unless beam-guided. |

### Spawn pattern roster

| Pattern | targetRockIndex | spawnY | Intended threat |
| --- | --- | --- | --- |
| P0 | 0 | 560 | Ship drifts upward toward upper rock. |
| P1 | 1 | 540 | Ship drifts downward toward lower rock. |

## 4.1 Upkeep

Tier: 1.

| Rule | Number |
| --- | --- |
| Fuel maximum | 100 |
| Fuel starting value | 100 |
| Normal drain | 0.9 / s |
| Easy drain | 0.70 / s |
| Hard drain | 1.15 / s |
| Refill starting value | 0 |
| Normal refill | 24 / s |
| Easy refill | 28 / s |
| Hard refill | 22 / s |
| Pump centre | 150, 600 |
| Pump radius normal | 36 |
| Pump radius easy | 44 |
| Pump radius hard | 32 |
| Pump input | Primary pointer button held while cursor is inside pump circle. |
| Pump effect | Add `refillRate * dt` to fuel, capped at max. |
| Pump stops | When pointer leaves pump circle or button is released. |
| Fuel visual | Oil tube level = `fuel / maxFuel`. |
| Low fuel visual | If fuel < 35, amber tube pulses slowly. |
| Lamp lit | Lamp is lit when fuel > 0. |
| Lamp out | If fuel <= 0, lamp turns out and `outTimer` starts. |
| Lamp out grace normal | 1.5 s |
| Lamp out grace easy | 2.5 s |
| Lamp out grace hard | 1.2 s |
| Lamp relight | If fuel > 0, `lit = true`, `outTimer = 0`. |
| Lamp out life loss | If `outTimer > outGrace`, lose a life. |
| Life loss lamp reset | Fuel set to 40, lamp relit, out timer cleared. |
| Visual intensity | `clamp(fuel / 45, 0.18, 1)` |
| Guidance factor | `clamp((fuel - 10) / 90, 0, 1)` |
| Guidance disabled | If `fuel <= 10`, guidance factor is 0. |

## 4.2 Multitasking

Tier: 1.

| Rule | Number |
| --- | --- |
| Task A: aim beam | Move pointer anywhere. Beam angle follows pointer. |
| Task B: refuel | Hold pointer button inside pump circle. |
| Simultaneity | Pumping and sea guidance cannot be effective simultaneously because the pump is on the lighthouse, not in the sea. |
| Beam while pumping | Beam remains active if lamp is lit, but its angle points toward the pump area, so it does not guide ships in the sea. |
| Pump input priority | If cursor is inside pump and button held, fuel is added. If cursor leaves pump, fuel addition stops immediately. |
| Cursor conversion | Pointer position is converted to beam angle from lamp position. |
| Angle clamp | 0° to 80°. |
| Cursor inside pump test | `distance(cursor, pump) <= pump.radius`. |
| Pump feedback | Pump handle animates downward, amber particles, pump sound. |
| Guidance feedback | Beam centerline brightens cyan when a ship is inside guidance range. |
| Failure pressure | Fuel drain continues regardless of beam aim. |
| Required player choice | Player must allocate cursor time between pump and beam. |

## 4.3 Escort

Tier: 1.

### Beam rules

| Rule | Number |
| --- | --- |
| Beam origin | Lamp position 150, 300. |
| Beam angle | `atan2(cursor.y - lamp.y, cursor.x - lamp.x)`, clamped to 0°–80°. |
| Beam length | 1300 px. |
| Beam half-width normal | 36 px. |
| Beam half-width easy | 42 px. |
| Beam half-width hard | 30 px. |
| Beam active | Lamp lit and fuel > 10. |
| Centerline y | `lamp.y + tan(angle) * (x - lamp.x)`. |
| Guidance condition | Ship distance to centerline <= half-width and lamp guidance factor > 0. |
| Guidance visual | If a ship is guided, beam centerline becomes cyan and ship gets a subtle cyan rim. |

### Ship movement rules

| Rule | Number |
| --- | --- |
| Spawn x | 1240 |
| Safe exit x | <= 260 |
| Ship radius | 16 |
| Ship y clamp | 396 to 684 |
| Normal base speed | Pattern speed from progression table. |
| Speed multiplier easy | 0.85 |
| Speed multiplier normal | 1.00 |
| Speed multiplier hard | 1.15 |
| Unguided target | Rock y from `targetRockIndex`. |
| Unguided desired vy | `clamp((rock.y - ship.y) * 0.5, -55, 55)` |
| Unguided acceleration | 140 px/s², multiplied by difficulty guidance inverse only for hard/easy? No, unguided drift is not multiplied. |
| Guided target | Beam centerline y at ship x. |
| Guided desired vy | `clamp((targetY - ship.y) * 1.2, -180, 180)` |
| Guided acceleration normal | 320 px/s² |
| Guided acceleration easy | 400 px/s² |
| Guided acceleration hard | 288 px/s² |
| Ship-ship collision | None. |
| Safe exit | Remove ship, play soft safe-pass sound, no life or fuel change. |

### Collision and life rules

| Event | Effect |
| --- | --- |
| Ship hits rock | Ship destroyed, life lost, screen shake 12 px for 0.5 s, hit flash 0.25 s, particles. |
| Lamp out for grace | Life lost, screen shake 10 px for 0.4 s, hit flash 0.25 s, lamp relight. |
| Life lost | `lives.count -= 1`. If lives > 0, start transition. If lives == 0, game over. |
| Transition duration | 2.0 s |
| During transition | Spawn paused, active ships destroyed, no additional life loss, fuel drain continues, pump allowed. |
| After transition | Resume spawning. Fuel remains whatever it is, minimum 40 after life loss. |
| Game over | Stop gameplay updates, show final survival time. |

### Spawn progression

| Run time | Spawn interval base | Ship speed base | Max active | Patterns |
| --- | --- | --- | --- | --- |
| 0–20 s | 5.5 s | 95 px/s | 1 | P0 |
| 20–60 s | 4.2 s | 110 px/s | 2 | P0, P1 |
| 60–120 s | 3.2 s | 125 px/s | 2 | P0, P1, P1 |
| 120–180 s | 2.6 s | 135 px/s | 3 | P0, P1, P0, P1 |
| >180 s | 2.1 s | 145 px/s | 3 | P0, P1, P0, P1 |

Difficulty multipliers apply to interval and speed:

| Difficulty | Interval multiplier | Speed multiplier |
| --- | --- | --- |
| Easy | 1.40 | 0.85 |
| Normal | 1.00 | 1.00 |
| Hard | 0.75 | 1.15 |

Pattern selection:

| Rule | Number |
| --- | --- |
| Selection | `rng.choice(activePatternList)` |
| Spawn skip | If active ship count >= max active, skip spawn and reset timer. |
| Seed | Each run starts with a deterministic seed. |

## 4.4 Progression and difficulty

Tier: 1 for baseline progression; Tier 2 for full option hardening.

| Difficulty | Lives | Fuel drain | Refill | Ship speed | Spawn interval | Guidance accel | Beam half-width | Pump radius | Lamp out grace |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Easy | 3 | 0.70 / s | 28 / s | 0.85× | 1.40× | 400 px/s² | 42 | 44 | 2.5 s |
| Normal | 3 | 0.90 / s | 24 / s | 1.00× | 1.00× | 320 px/s² | 36 | 36 | 1.5 s |
| Hard | 3 | 1.15 / s | 22 / s | 1.15× | 0.75× | 288 px/s² | 30 | 32 | 1.2 s |

Expected run lengths:

| Difficulty | Target median run |
| --- | --- |
| Easy | 4–6 minutes |
| Normal | 2–4 minutes |
| Hard | 1–2 minutes |

## 4.5 Feel

The beam should feel immediate: the pointer controls the angle with no smoothing beyond the angle clamp. The pump should feel physical: holding the pointer inside the valve produces a low thud, handle motion, and amber particles. The lamp should feel fragile: as fuel falls, the beam dims, guidance weakens, and the oil tube becomes visibly low. Ships should feel reluctant: they drift toward rocks unless the beam gives a clear safe path. The safe channel between the two rocks is the readable skill area. Failure should be loud and dark: a life loss extinguishes one wick, shakes the screen, and pauses spawning long enough for the player to recover without removing the pressure.

# 5. CHARACTERS

| Character / object | Silhouette | Facing | Animations | States needed by gameplay |
| --- | --- | --- | --- | --- |
| Keeper | No visible body. Cursor presence only. | N/A | None | Input state only. |
| Lighthouse | Squat painterly tower with lamp room. | Static | `towerShake` | None. |
| Lamp | Circular lantern with three small wicks. | Faces right. | `flameIdle`, `flameFlicker`, `wickExtinguish` | `lamp.lit`, `lamp.intensity`, `lives.count`. |
| Oil tube | Vertical glass tube on lighthouse. | Static | `oilLevel`, `oilPulseLow` | `lamp.fuel`. |
| Pump | Circular valve and handle on lighthouse base. | Faces right. | `pumpHandleDown`, `pumpHandleUp`, `pumpGlow` | `pump.active`. |
| Beam | Translucent wedge with faint centerline. | Origin fixed, rotates. | `beamSweepTrail`, `beamDim`, `beamGuidanceHighlight` | `beam.active`, `beam.angle`, `beam.halfWidth`, guided ships. |
| Ship | Dark hull, pale sail, small wake. | Faces left. | `bob`, `wakeTrail`, `sailSway`, `guidedLean`, `hitShatter`, `safeFade` | `ship.guided`, `ship.alive`, `ship.safe`. |
| Rock | Jagged dark cluster. | Static | `dangerHaloPulse` | Collision proximity. |
| Particles | Sparks, foam, embers. | None | `particleDrift` | `fx.particles`. |

### Animation rules

| Animation name | Motion rule |
| --- | --- |
| `flameIdle` | Flame scale oscillates by 2% at 0.7 Hz when fuel > 70. |
| `flameFlicker` | Flame alpha jitters when fuel < 35. Disabled in reduced motion. |
| `wickExtinguish` | One wick flame shrinks and smoke rises over 0.6 s when a life is lost. |
| `oilLevel` | Fuel level height = `fuel / maxFuel`. |
| `oilPulseLow` | Amber glow pulses at 0.25 Hz when fuel < 35. |
| `pumpHandleDown` | Handle moves down 10 px over 0.25 s while pumping, cycles. |
| `pumpGlow` | Valve rim glows amber while active. |
| `beamSweepTrail` | Previous beam edge fades over 0.15 s while angle changes > 0.05 rad/frame. |
| `beamGuidanceHighlight` | Centerline shifts from amber to cyan while a ship is guided. |
| `bob` | Ship y offset = sin(`bobPhase`) * 3 px; `bobPhase` advances 2.5 rad/s. |
| `wakeTrail` | Short fading line behind ship, age 0.45 s. |
| `sailSway` | Sail vertices offset by storm wind noise, amplitude 2 px. |
| `guidedLean` | Ship tilts toward beam centerline by up to 8 degrees when guided. |
| `hitShatter` | Ship breaks into 8 dark shards and white impact particles. |
| `safeFade` | Ship fades and sinks slightly over 0.4 s at safe exit. |
| `dangerHaloPulse` | Violet halo appears around rock when any ship is within 120 px. |

# 6. AUDIO

All audio is synthesized with the audio API. No external files. The ambient bed is slow and non-rhythmic. Foley is made from filtered noise and short tonal impacts to sound recorded.

| Sound name | Recipe | When it plays |
| --- | --- | --- |
| `ambient_storm` | Brown noise through bandpass 120–700 Hz, slow LFO on gain at 0.04 Hz; pink noise highpass 500 Hz for wind; sine drone 55 Hz and 82 Hz with slow detune. No percussion. | Starts on first game start; continues through playing and game over at reduced volume. |
| `wave_loop` | Brown noise lowpass 220 Hz, slow amplitude LFO 0.07 Hz, subtle comb filter. | Starts with ambient. |
| `rain_texture` | White noise highpass 1800 Hz, lowpass 9000 Hz, gain 0.04, slow random modulation. | Starts with ambient; disabled or static in reduced motion. |
| `pump_loop` | Looping low thud: sine 95 Hz, attack 0.01 s, decay 0.12 s; click transient = noise burst highpass 1200 Hz. | While `pump.active`. |
| `pump_start` | One filtered noise burst 300–1200 Hz plus sine 110 Hz, 0.1 s. | When pump becomes active. |
| `pump_stop` | Short valve hiss: pink noise 800–3000 Hz, 0.15 s fade. | When pump becomes inactive. |
| `fuel_low` | Very slow low pulse: sine 70 Hz, 0.8 s, gain 0.05, triggered every 4 s while fuel < 35. | Low fuel warning. |
| `lamp_ignite` | Filtered noise burst 600–4000 Hz plus sine 160 Hz rising to 220 Hz, 0.25 s. | Lamp relights after life loss. |
| `lamp_dim` | Sawtooth 140 Hz fading to 90 Hz, lowpass 900 Hz, 0.5 s. | Fuel crosses below 35. |
| `lamp_out` | Descending sine 160 Hz to 55 Hz, noise crackle, 0.7 s. | Fuel reaches 0. |
| `ship_enter` | Soft water displacement: filtered noise 250–1800 Hz, 0.25 s. | Ship spawns. |
| `ship_guided` | Light creak: filtered noise 120–450 Hz, slow amplitude, gain 0.04. | While a ship is guided. |
| `ship_safe` | Wooden harbour creak: filtered noise 100–350 Hz, 0.35 s. | Ship reaches safe exit. |
| `rock_impact` | Stone/wood impact: noise burst 80–1500 Hz, sine 110 Hz, distortion, decay 0.6 s. | Ship hits rock. |
| `life_lost` | Deep impact 60 Hz, glass shatter noise 2500–8000 Hz, 0.8 s. | Any life loss. |
| `game_over` | Low drone swell 45–90 Hz, wind noise fade, 2.5 s. | Lives reach 0. |

# 7. UX

## Screens

| State | DOM | Allowed inputs | Transitions |
| --- | --- | --- | --- |
| `title` | Title SVG text, difficulty radio group, reduced-motion checkbox, start button. | Pointer clicks, keyboard focus, Enter/Space on buttons. | Start button -> `playing`. |
| `playing` | Canvas only. No DOM overlay except hidden accessibility live region for game state if needed. | Pointer move, pointer down/up for pump. | Lives 0 -> `gameover`. |
| `gameover` | Hand-lettered final time, Try Again button, Title button. | Pointer clicks, keyboard focus. | Try Again -> `playing`; Title -> `title`. |

## HUD

| Element | Record field | When visible |
| --- | --- | --- |
| None | None | Never |

## Diegetic status substitutes, not HUD

| Element | Record field | When visible |
| --- | --- | --- |
| Oil tube level | `lamp.fuel` | Always during `playing`. |
| Lamp brightness | `lamp.intensity` | Always during `playing`. |
| Lamp wicks | `lives.count` | Always during `playing`. |
| Pump glow | `pump.active` | While pumping. |
| Beam guidance highlight | guided ships | While a ship is guided. |
| Rock danger halo | ship proximity to rock | When ship within 120 px of rock. |

## Accessibility

| Requirement | Implementation |
| --- | --- |
| Colour-blind safe palette | Amber/cyan/violet/white only. No red/green meaning. |
| Reduced motion | Checkbox on title and system media query. Disables shake, hit flash, bloom, rain motion, wave motion, lamp flicker, non-essential particles. |
| Difficulty options | Three radio buttons on title: Easy, Normal, Hard. |
| Keyboard UI | Buttons and radios are native focusable controls with visible focus outline. |
| Screen reader | Title and game-over buttons have accessible names. Final time text is readable. |
| Pointer | Game uses pointer events. If pointer is lost, cursor position clamps to last valid value. |

# 8. DEBUG API

| System | Function | Commands | Purpose |
| --- | --- | --- | --- |
| Upkeep | `debug.upkeep(command, value)` | `get`, `setFuel`, `setDrain`, `setRefill`, `setLit`, `setOutGrace` | Reach lamp/fuel state directly. |
| Pump | included in upkeep | `getPump`, `setPumpActive` | Reach pump state directly. |
| Beam | included in escort | `getBeam`, `setAngle`, `setHalfWidth`, `centerYAt` | Reach beam state directly. |
| Escort | `debug.escort(command, value)` | `get`, `spawn`, `setInterval`, `setSpeed`, `setGuidance`, `setRocks`, `collide`, `safeExit`, `getShips` | Reach ship/rock/spawn state directly. |
| Lives | `debug.lives(command, value)` | `get`, `set`, `lose`, `startTransition` | Reach life state directly. |
| Input | `debug.input(command, value)` | `setCursor`, `setPumpHeld`, `getCursor` | Force player input state. |
| Effects | `debug.fx(command, value)` | `get`, `shake`, `hitFlash`, `particles`, `setBloom` | Reach visual effect state directly. |

Player input functions:

| Function | Signature | Purpose |
| --- | --- | --- |
| `input.setPointer` | `setPointer(x, y)` | Move cursor. |
| `input.setPointerDown` | `setPointerDown(button)` | Hold pump input. |
| `input.setPointerUp` | `setPointerUp()` | Release pump input. |
| `input.isPumpHeld` | `isPumpHeld()` | Read pump hold state. |

# 9. TESTS

| Tier | Test | Pass condition |
| --- | --- | --- |
| 1 | Fixed step | Running for 1.0 real second updates exactly 60 fixed steps when not throttled. |
| 1 | Deterministic RNG | Seeding the same seed produces identical ship spawn order and positions. |
| 1 | Title to playing | Clicking Start hides title DOM and sets `screen = "playing"`. |
| 1 | Game over to title | Clicking Title from game over sets `screen = "title"`. |
| 1 | Fuel drain | With difficulty normal and no pumping, fuel decreases by 0.9 per simulated second. |
| 1 | Pump refill | With cursor inside pump and button held, fuel increases by 24 per simulated second. |
| 1 | Pump stop | If cursor leaves pump while button held, fuel stops increasing. |
| 1 | Lamp out grace | Set fuel to 0; after 1.5 s, lives decrease by 1 and lamp relights with 40. |
| 1 | Beam follows cursor | Setting cursor to a valid sea point produces the expected clamped angle and centerline. |
| 1 | Beam clamp | Cursor above lamp clamps angle to 0°; cursor far down clamps to 80°. |
| 1 | Ship spawn | `debug.escort("spawn", ...)` creates a ship with correct target and speed. |
| 1 | Unguided drift | A spawned ship without beam guidance moves toward its target rock y. |
| 1 | Guided steering | A ship inside the beam steers toward the beam centerline. |
| 1 | Rock collision life loss | Placing a ship at a rock collision point and stepping reduces lives by 1. |
| 1 | Safe exit | Moving a ship to x <= 260 removes it and does not reduce lives. |
| 1 | Transition | After life loss, spawning is paused for 2.0 s and no further life loss occurs during transition. |
| 1 | Game over | Setting lives to 0 or losing the third life sets `screen = "gameover"` and records final time. |
| 1 | No HUD | During playing, no visible DOM HUD elements exist. |
| 1 | Required effects trigger | Rock collision creates shake, hit flash, and particles. |
| 2 | Difficulty easy | Easy multipliers reduce drain, reduce ship speed, increase interval, increase beam width. |
| 2 | Difficulty hard | Hard multipliers increase drain, increase ship speed, reduce interval, reduce beam width. |
| 2 | Reduced motion | With reduced motion on, shake, hit flash, bloom, and non-essential particles are suppressed. |
| 2 | UI keyboard | Title and game-over controls are reachable by keyboard and have visible focus. |
| 2 | Palette | Rendered UI uses approved colour tokens and no red/green state colours. |
| 3 | Bloom/trails | Enabling bloom/trails does not change ship positions, lives, fuel, or spawn results. |
| 3 | Audio no beat | Ambient spectrum has no percussive transient pattern; no beat scheduler runs. |
| 3 | Performance | 60 steps/s runs without dropped fixed-step substeps exceeding 5. |

# 10. BUILD ORDER

1. Create HTML/CSS title, game-over, canvas, and dark palette tokens.
2. Implement fixed-step loop, seeded RNG, global context, and screen state.
3. Implement input pointer position and primary button state.
4. Implement world constants, lighthouse, lamp, oil tube, pump, and two rocks.
5. Implement lamp fuel drain and lamp out state.
6. Implement pump refuel and diegetic fuel/pump visuals.
7. Implement beam angle from cursor, clamps, and beam rendering.
8. Implement ship spawn records and unguided rock drift.
9. Implement beam guidance physics.
10. Implement rock collision, safe exit, lives, transition, and game over.
11. Implement basic required effects: screen shake, hit flash, particles, trails, bloom.
12. Implement basic synthesized ambient and foley.
13. Implement title difficulty and reduced-motion controls.
14. Add debug entry points and run Tier 1 tests.
15. Add Tier 2 accessibility hardening.
16. Add Tier 3 visual/audio polish.

# 11. DEFINITION OF DONE

## Tier 1 Definition of Done

A complete core game exists.

- [ ] Title screen can start a run.
- [ ] Game-over screen appears when lives reach 0.
- [ ] Final survival time is shown on game over.
- [ ] Fixed 60 Hz simulation runs.
- [ ] Seeded RNG controls spawn patterns.
- [ ] Fuel drains at difficulty rate.
- [ ] Pump refuels only when cursor is inside pump and button held.
- [ ] Lamp turns out at fuel 0.
- [ ] Lamp out grace causes life loss.
- [ ] Beam follows cursor and clamps to 0°–80°.
- [ ] Beam guidance affects ships inside half-width.
- [ ] Ships spawn from the right and move left.
- [ ] Unguided ships drift toward their target rock.
- [ ] Guided ships steer toward beam centerline.
- [ ] Rock collision costs a life.
- [ ] Safe exit removes ship without life cost.
- [ ] Three lives are tracked and shown as wicks.
- [ ] Transition pauses spawning and prevents chained life loss.
- [ ] No HUD exists during playing.
- [ ] Basic screen shake, hit flash, particles, trails, and bloom trigger on events.
- [ ] Basic synthesized ambient and foley play.
- [ ] Debug commands reach all core systems.
- [ ] Tier 1 tests pass.

## Tier 2 Definition of Done

The game is accessible and configurable without adding mechanics.

- [ ] Easy/Normal/Hard options apply all documented numbers.
- [ ] Reduced motion suppresses motion-heavy effects.
- [ ] UI controls are keyboard accessible.
- [ ] Palette uses approved colour-safe tokens.
- [ ] No red/green meaning is used.
- [ ] Tests for difficulty and reduced motion pass.

## Tier 3 Definition of Done

The game feels richer without changing gameplay.

- [ ] Bloom and trails are visually stronger but deterministic gameplay is unchanged.
- [ ] Particles and water textures are more layered.
- [ ] Audio ambient and foley are fuller but still no beat.
- [ ] Performance remains stable.
- [ ] Tier 3 tests pass.

# A. SANITY

| Check | Result |
| --- | --- |
| All requested headings present in order | Valid. |
| All requested decisions carried through | Valid. |
| No supporting mechanics added | Valid. Only three core mechanics exist. |
| No extra mechanics added | Valid. No pickups, upgrades, pause, ship-ship collision, or rewards. |
| Player input is cursor-only | Valid. Pointer aim and pointer hold are the only gameplay inputs. |
| No movement | Valid. No player entity or camera moves. |
| Single screen | Valid. One canvas screen, title and game over overlays only. |
| Side-on camera | Valid. Fixed side-on world coordinates. |
| Real-time | Valid. Fixed real-time step, no pause mechanic. |
| Failure loses a life | Valid. Rock collision and lamp-out grace each lose a life. |
| Survive as long as possible | Valid. No win condition; final time is the record. |
| HUD none | Valid. HUD table is none; status is diegetic. |
| Screens only title and game over | Valid. No settings screen; options are on title. |
| Accessibility present | Valid. Colour-safe palette, reduced motion, and difficulty options are specified. |
| Effects present | Valid. Screen shake, particles, hit flash, trails, and bloom are specified. |
| Art style present | Valid. Hand-drawn/painterly recipe is specified. |
| Palette dark with accents | Valid. Mostly black with amber/cyan/violet/white accents. |
| Typography hand-lettered | Valid. UI typography and SVG/hand-lettered approach specified. |
| Music ambient no beat | Valid. Ambient recipe has no beat scheduler. |
| Sound effects realistic foley | Valid. Noise-based foley recipes specified. |
| Rock layout is navigable | Valid. Two rocks with safe channel between y 490–610 at the relevant x positions. |
| Numbers are concrete | Valid. All systems have numeric rules. |
| Tier 1 is core only | Valid. Tier 1 contains core mechanics and required product shell, not extra systems. |
| Tier 2/3 add no mechanics | Valid. They add only accessibility hardening and polish. |
| Contracts include all needed fields | Valid. Global context and record schemas include fields required by gameplay rules. |
| Tests validate each tier | Valid. Tier 1/2/3 tests are listed. |