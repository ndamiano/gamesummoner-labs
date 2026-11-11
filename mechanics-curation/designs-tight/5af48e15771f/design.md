# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Game prompt: lighthouse keeper on a stormy night, swinging the beam to steer ships past the rocks while keeping the lamp fuelled | `# 4. GAMEPLAY SPEC`, `# 5. CHARACTERS`, `# 3. VISUAL SPEC` |
| Dimension: 2d | `# 1.1 Units, axes, frames`, `# 2. CONTRACTS`, `# 3. VISUAL SPEC` |
| Camera: side-on | `# 3. VISUAL SPEC`, `# 4. GAMEPLAY SPEC` |
| Time model: real-time | `# 1.1 Units, axes, frames`, `# 1.2 Important conventions`, `# 4. GAMEPLAY SPEC` |
| Movement model: no movement, cursor only | `# 0.2 Decisions`, `# 7. UX`, `# 8. DEBUG API` |
| Session shape: single screen | `# 3. VISUAL SPEC`, `# 7. UX` |
| Failure: lose a life | `# 4. GAMEPLAY SPEC`, `# 11. DEFINITION OF DONE` |
| Tone: tense | `# 3. VISUAL SPEC`, `# 6. AUDIO`, `# 4. GAMEPLAY SPEC` |
| Size: one screen, a few minutes | `# 4. GAMEPLAY SPEC`, `# 10. BUILD ORDER` |
| Win/lose: survive as long as possible | `# 4. GAMEPLAY SPEC`, `# 7. UX` |
| Core mechanic: upkeep: a supply runs down and must be topped up before it runs out | `# 4. GAMEPLAY SPEC` → Upkeep |
| Core mechanic: multitasking: several jobs get worse when left alone; player chooses which to attend | `# 4. GAMEPLAY SPEC` → Multitasking |
| Core mechanic: escort: guide or protect others who cannot look after themselves until safety | `# 4. GAMEPLAY SPEC` → Escort |
| Supporting mechanic: scoring: awards points and records best scores | `# 4. GAMEPLAY SPEC` → Scoring |
| Extra mechanics: none | `# 0.2 Decisions`, `# 0.3 Tiers` |
| Art style: hand-drawn / painterly | `# 3. VISUAL SPEC`, `# 5. CHARACTERS` |
| Palette: dark, mostly black with a few bright accents | `# 3. VISUAL SPEC` |
| Typography: hand-lettered | `# 3. VISUAL SPEC`, `# 7. UX` |
| Music: ambient | `# 6. AUDIO` |
| Sound effects style: realistic recorded-sounding impacts and foley | `# 6. AUDIO` |
| Screens: title, game over | `# 7. UX` |
| HUD: score | `# 7. UX` |
| Effects: screen shake, particles, hit flash, trails, bloom | `# 3. VISUAL SPEC`, `# 4. GAMEPLAY SPEC` |
| Accessibility: colour-blind safe palette, reduced motion, difficulty options | `# 0.2 Decisions`, `# 3. VISUAL SPEC`, `# 4. GAMEPLAY SPEC`, `# 7. UX` |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| The player is a lighthouse keeper | The player is an unseen keeper. The cursor represents the keeper’s aim and hand. No avatar moves. | Preserves “no movement, cursor only” while making the prompt literal. |
| No character movement | Input is pointer only: move pointer to aim the beam; hold pointer inside the fuel pump to refill. | Required input model. |
| Single screen | One logical canvas, fixed layout. No scrolling, no camera follow. | Required session shape. |
| Side-on camera | The lighthouse is on the left shore. The sea is to the right. Ships travel from right to left toward the harbor. | Side-on view, readable beam sweep. |
| Lighthouse position | Tower visual occupies `x=100..180`, `y=120..560`; lamp origin is `(150, 220)`; fuel pump hitbox is `x=110..190`, `y=600..660`. | Gives the beam a clear origin and puts the fuel pump behind the player. |
| Harbor/safety | Safe harbor is `x<=130`, `y=500..570`. Ships are safe when inside it. | Gives a concrete “until they reach safety” target. |
| Enemies | None. No hostile characters. | The prompt asks for protection, not combat. Extra mechanics are forbidden. |
| Traps | Four static rocks/reefs. Exact positions and radii in `# 4. GAMEPLAY SPEC`. | Concrete hazard content without adding systems. |
| Pickups | None. Fuel is refilled only at the fixed fuel pump. | Avoids adding a pickup system not listed. |
| Lives | Three lives. Displayed as three oil-wick flames on the lighthouse base, not as HUD. | Required failure model. |
| HUD | HUD contains only numeric score. Fuel and lives are diegetic scene objects. | Required HUD is score only. |
| Fuel | A single lamp fuel gauge. It drains while the lamp is online. It can be refilled only by holding the pointer inside the fuel pump. | Core upkeep. |
| Lamp failure | If fuel reaches `0`, the lamp goes offline for `2.0s`, the player loses one life, and fuel is restored to `25`. | Makes fuel failure a life loss, not instant game over. |
| Beam control | Pointer position sets the beam aim point. The beam is always visible unless pumping or lamp offline. | Cursor-only control. |
| Guidance model | The beam guides only the ship nearest to the beam aim point, within a guidance radius. The player chooses which ship to attend by aiming near it. | Makes multitasking concrete. |
| Ships | Three ship types: Dinghy, Sloop, Schooner. They are escort targets, not enemies. | Gives escalating content without adding new systems. |
| Ship failure | If a ship collides with a rock, the player loses a life. | Required life loss. |
| Ship success | If a ship reaches the safe harbor, it is docked and removed. | Escort completion. |
| Multitasking | The player can attend either the fuel pump or one ship at a time. Fuel and each ship worsen when unattended. | Implements the required multitasking system. |
| Spawn progression | Time-based spawn caps and intervals. First ship at `8s`; active cap rises to `4` at `150s` on Normal. | Produces a few-minute tense run. |
| Scoring | Survival points, safe ship points scaled by how calm the ship was, and fuel-save bonus. Best scores stored locally. | Supporting mechanic. |
| Difficulty options | Three presets: Easy, Normal, Intense. These change lives, fuel rates, spawn rates, and ship behavior. | Required accessibility/difficulty decision. |
| Colour-blind safe palette | Uses luminance, shape, and blue/orange/amber accents rather than red/green distinctions. | Required accessibility. |
| Reduced motion | Disables screen shake, trails, animated bloom, and most particles; keeps static glow and readable states. | Required accessibility. |
| Screens | Title and Game Over only. No pause screen. | Required screens only. |
| Fixed step | Gameplay updates at `1/60s`. Render may interpolate. | Deterministic real-time behavior. |
| Deterministic random source | Seeded Mulberry32. No `Math.random()` in gameplay. | Testable runs. |
| Extra systems | None. Collision, spawn, and job urgency are implementation details inside the three core systems. | Extra mechanics are forbidden. |
| Tier 1 | Upkeep, Multitasking, Escort, required accessibility baseline, required art/audio/effects, score HUD element present but not scored until Tier 2. | Core must be playable and finished first. |
| Tier 2 | Scoring and best scores. | Supporting mechanic. |
| Tier 3 | Not used. Extra mechanics are none. | Required list has no extra mechanics. |

## 0.3 Tiers

Priority list. Tier 1 is guaranteed to build and must be a playable single-screen game. Higher tiers may be left unbuilt.

### Tier 1 — Core playable game

1. Fixed-step real-time loop, seeded RNG, global context, run configuration.
2. Title screen and Game Over screen.
3. Single-screen side-on scene: lighthouse, sea, rocks, harbor.
4. Cursor-only beam aiming and fuel pumping.
5. Upkeep system: fuel drain, fuel refill, low-fuel warning, lamp offline, life loss.
6. Multitasking system: spawn ships, track ship distress, fuel urgency, enforce one attended job at a time.
7. Escort system: beam guidance, ship steering, rock collision, harbor safety.
8. Lives system: three lives, diegetic life display, life-loss effects.
9. Required art style: hand-drawn/painterly, dark palette, hand-lettered screens.
10. Required effects: screen shake, particles, hit flash, trails, bloom.
11. Required audio: ambient music and realistic foley sounds.
12. Required accessibility baseline: colour-blind safe palette, reduced motion, difficulty presets.
13. HUD score element exists and is visible in `playing`, but scoring rules may remain disabled.

### Tier 2 — Scoring

1. Survival scoring.
2. Safe ship scoring scaled by distress.
3. Fuel-save bonus.
4. Best score storage by difficulty.
5. Final score and best score shown on Game Over.

### Tier 3 — Not used

No extra mechanics are allowed by the brief. Stop after Tier 2.

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Quantity | Value | Notes |
| --- | --- | --- |
| Logical canvas width | `1280` px | Fixed aspect `16:9`. CSS scales to viewport. |
| Logical canvas height | `720` px | One screen. |
| Coordinate system | `x` increases right, `y` increases down | Origin at top-left. |
| Fixed update step | `DT = 1 / 60` seconds | All gameplay rules use `DT`. |
| Render frame | Browser `requestAnimationFrame` | Render may interpolate from previous state. |
| Speed unit | px/s | Used for ships and particles. |
| Acceleration/steering | response rate in `1/s` | Steering is lerp response, not Newtonian force. |
| Angle unit | radians | Internal only. Cursor mapping is direct. |
| Collision unit | px circle radius | Rock and ship collision radii are explicit. |
| Time | seconds | `state.elapsed` counts only while `mode === 'playing'`. |
| Score | integer | Rounded down on every addition. |
| RNG | deterministic seeded generator | Mulberry32. |

## 1.2 Important conventions

1. **No gameplay randomness without a seed.**  
   Use `rng.next()`, `rng.range(min, max)`, and `rng.pickWeighted(weights)`.

2. **No `Math.random()` in gameplay, spawn, scoring, or tests.**  
   Tests must produce identical results for the same seed and inputs.

3. **Fixed-step gameplay.**  
   `update(DT)` is called exactly in multiples of `1/60s`. Visual interpolation is separate.

4. **No player movement.**  
   The only pointer actions are:
   - move pointer to aim beam;
   - hold pointer inside fuel pump to pump;
   - click UI buttons.

5. **No pause.**  
   The game runs real-time from `Start` until `GameOver`.

6. **No extra gameplay systems.**  
   Spawn, collision, urgency, and effects are not separate mechanics. They belong to Upkeep, Multitasking, Escort, Scoring, or presentation.

7. **HUD is score only.**  
   Fuel, lives, and ship distress must be communicated through the scene, not HUD widgets.

8. **All numbers live in config.**  
   Systems must read `state.config` and must not hard-code tuned constants.

9. **All visual state is derived from records.**  
   Render does not mutate gameplay state.

10. **Reduced motion is a rendering/accessibility mode.**  
   It changes visual intensity only. It does not change gameplay numbers.

11. **Difficulty presets change config only.**  
   Systems must not branch on difficulty except by reading config values.

12. **Scoring is optional.**  
   Tier 1 may set `config.scoringEnabled = false`. Core rules must not depend on score.

# 2. CONTRACTS

## 2.1 Module layout

```text
index.html
styles.css
src/
  main.js
  config.js
  state.js
  rng.js
  input.js
  systems/
    upkeep.js
    multitasking.js
    escort.js
    scoring.js
  render/
    scene.js
    lighthouse.js
    sea.js
    rocks.js
    ships.js
    beam.js
    effects.js
    palette.js
  audio/
    audio.js
    recipes.js
  ui/
    screens.js
    lettering.js
  debug.js
tests/
  tier1.spec.js
  tier2.spec.js
```

| File | Owns | Must not own |
| --- | --- | --- |
| `index.html` | DOM screens, canvas, HUD score element | gameplay logic |
| `styles.css` | screen layout, palette, HUD, CSS variables | gameplay state |
| `src/main.js` | boot, fixed loop, mode dispatch | rule numbers |
| `src/config.js` | constants, difficulty presets, run config | mutable state |
| `src/state.js` | record creation, reset, record fields | input handling |
| `src/rng.js` | seeded RNG | gameplay rules |
| `src/input.js` | pointer events, input records | game rules |
| `src/systems/upkeep.js` | fuel, pump, lamp offline | ship steering, score |
| `src/systems/multitasking.js` | spawn, ship distress, job urgency | beam rendering, score |
| `src/systems/escort.js` | beam target selection, ship steering, collision, harbor | fuel pump, score |
| `src/systems/scoring.js` | points, best score | core survival rules |
| `src/render/*` | drawing, effects | gameplay mutation |
| `src/audio/*` | synthesized audio recipes, playback | gameplay mutation |
| `src/ui/screens.js` | title/game-over state machine | gameplay rules |
| `src/debug.js` | direct state access for tests | normal UI |

## 2.2 Global context

The global context is one object named `G`.

| Field | Type | Owned by | Used by | Notes |
| --- | --- | --- | --- | --- |
| `G.config` | `RunConfig` | `config.js` | all systems | Immutable for the run. |
| `G.rng` | `Rng` | `rng.js` | `multitasking.js`, `state.js` | Seeded per run. |
| `G.clock` | `Clock` | `main.js` | all systems | Real-time and fixed-step timing. |
| `G.input` | `PointerInput` | `input.js` | `upkeep.js`, `escort.js`, `ui/screens.js` | Cursor only. |
| `G.state` | `GameState` | `state.js` | all systems | Single mutable run state. |
| `G.ui` | `UIState` | `ui/screens.js` | DOM, render | Screen visibility. |
| `G.effects` | `EffectState` | `render/effects.js` | render, audio | Visual effects only. |
| `G.audio` | `AudioController` | `audio/audio.js` | systems indirectly | No direct gameplay mutation. |

### `RunConfig`

| Field | Type | Normal value | Notes |
| --- | --- | --- | --- |
| `difficulty` | `'easy' \| 'normal' \| 'intense'` | `'normal'` | Preset selector. |
| `maxLives` | integer | `3` | Starting and maximum lives. |
| `startFuel` | number | `100` | Initial fuel. |
| `fuelMax` | number | `100` | Fuel cap. |
| `fuelDrain` | number/s | `4.5` | Drain while lamp online. |
| `fuelRefill` | number/s | `18` | Pump refill rate. |
| `lowFuel` | number | `30` | Warning threshold. |
| `lampOfflineDuration` | number | `2.0` | Seconds. |
| `lampOfflineFuel` | number | `25` | Fuel after life loss. |
| `spawnFirstAt` | number | `8.0` | First ship spawn time. |
| `spawnIntervalBase` | number | `9.0` | Base seconds. |
| `spawnIntervalMin` | number | `3.2` | Minimum seconds. |
| `spawnIntervalDecayPerSecond` | number | `0.032` | Reduces interval. |
| `maxActiveCap` | integer | `4` | Hard active ship cap. |
| `timeScoreRate` | points/s | `6` | Tier 2. |
| `scoringEnabled` | boolean | Tier 1 `false`, Tier 2 `true` | Optional. |
| `beamGuideRadius` | number | `170` | Base guidance radius. |
| `fuelPumpRect` | rect | `x=110,y=600,w=80,h=60` | Hitbox. |
| `lampOrigin` | point | `x=150,y=220` | Beam origin. |
| `harborRect` | rect | `xMax=130,yMin=500,yMax=570` | Safe zone. |
| `beamAimMinX` | number | `220` | Beam aim lower bound. |
| `beamAimMaxX` | number | `1240` | Beam aim upper bound. |
| `beamAimMinY` | number | `120` | Beam aim upper bound. |
| `beamAimMaxY` | number | `680` | Beam aim lower bound. |
| `spawnYMin` | number | `500` | Ship spawn y lower bound. |
| `spawnYMax` | number | `540` | Ship spawn y upper bound. |
| `spawnX` | number | `1280` | Ship spawn x. |
| `accessibility` | `AccessibilityConfig` | default false | Reduced motion etc. |

### `AccessibilityConfig`

| Field | Type | Default | Effect |
| --- | --- | --- | --- |
| `reducedMotion` | boolean | `false` | Disables shake, trails, animated bloom, most particles. |
| `colorBlindSafe` | boolean | `true` | Always true for this game. |
| `difficulty` | preset | `'normal'` | Already in config. |

### `Clock`

| Field | Type | Notes |
| --- | --- | --- |
| `elapsed` | seconds | Only increments in `playing`. |
| `frame` | integer | Fixed update counter. |
| `accumulator` | seconds | Fixed-step accumulator. |
| `lastTime` | ms | RAF timestamp. |

### `PointerInput`

| Field | Type | Notes |
| --- | --- | --- |
| `x` | number | Logical canvas x. |
| `y` | number | Logical canvas y. |
| `down` | boolean | Primary pointer held. |
| `insidePump` | boolean | Computed from `fuelPumpRect`. |
| `button` | string | `'start'`, `'restart'`, `'title'` for UI clicks. |

### `GameState`

| Field | Type | Notes |
| --- | --- | --- |
| `mode` | `'title' \| 'playing' \| 'gameover'` | Run screen state. |
| `runSeed` | integer | RNG seed. |
| `elapsed` | seconds | Mirrors clock while playing. |
| `lives` | integer | Current lives. |
| `score` | integer | Tier 2. |
| `bestScore` | integer | Loaded from storage in Tier 2. |
| `fuel` | number | Upkeep state. |
| `lampOnline` | boolean | False during lamp offline. |
| `lampOfflineTimer` | number | Seconds remaining. |
| `pumping` | boolean | True while pointer held in pump. |
| `beam` | `BeamState` | Aim and attended target. |
| `ships` | `Ship[]` | Active escort targets. |
| `rocks` | `Rock[]` | Static hazards. |
| `wicks` | `Wick[]` | Diegetic life display. |
| `effects` | `EffectState` | Screen shake, hit flash, particles. |
| `gameOverReason` | `'lives' \| 'none'` | Set when lives reach zero. |

### `BeamState`

| Field | Type | Notes |
| --- | --- | --- |
| `aimX` | number | Clamped beam aim point. |
| `aimY` | number | Clamped beam aim point. |
| `angle` | number | Derived from aim. |
| `enabled` | boolean | False if pumping or lamp offline. |
| `guideRadius` | number | Config scaled by fuel. |
| `attendedShipId` | string \| null | Current attended ship. |

### `Ship`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Unique. |
| `type` | `'dinghy' \| 'sloop' \| 'schooner'` | Content type. |
| `x`, `y` | number | Position. |
| `vx`, `vy` | number | Velocity. |
| `baseSpeed` | number | Unattended leftward speed. |
| `maxSpeed` | number | Guided max speed. |
| `steerRate` | number/s | Steering response. |
| `collisionRadius` | number | Collision circle. |
| `distress` | number `0..100` | Multitasking pressure. |
| `attended` | boolean | Escort state. |
| `state` | `'active' \| 'wrecked' \| 'docked'` | Ship lifecycle. |
| `safePoints` | integer | Tier 2 base points. |
| `wakeTrail` | point[] | Visual trail, not gameplay. |

### `Rock`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Static id. |
| `x`, `y` | number | Center. |
| `collisionRadius` | number | Used by collision. |
| `visualRadius` | number | Used by render. |
| `kind` | `'top' \| 'bottom'` | Visual variant. |

### `Wick`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | 0..2. |
| `alive` | boolean | Dies when a life is lost. |
| `flicker` | number | Visual only. |

### `EffectState`

| Field | Type | Notes |
| --- | --- | --- |
| `shake.amplitude` | number | Current shake amplitude. |
| `shake.duration` | number | Remaining time. |
| `hitFlash.opacity` | number | Full-screen flash. |
| `particles` | Particle[] | Transient. |
| `trails` | Trail[] | Transient. |
| `bloom.enabled` | boolean | False if reduced motion. |

## 2.3 Module specifics

| Module | Owns | Exposes | Must not do |
| --- | --- | --- | --- |
| `main.js` | RAF, fixed loop, mode dispatch | `boot()`, `loop(timestamp)` | Mutate config during run. |
| `config.js` | presets, constants | `createRunConfig(difficulty, accessibility)`, `NORMAL_CONFIG`, `EASY_CONFIG`, `INTENSE_CONFIG` | Store mutable run state. |
| `state.js` | record factories | `createRun(config, seed)`, `resetRun(state)`, `addLifeLost(state)` | Handle input. |
| `rng.js` | seeded RNG | `createRng(seed)`, `rng.next()`, `rng.range(a,b)`, `rng.pickWeighted(items)` | Use `Math.random()`. |
| `input.js` | pointer events | `initInput(canvas)`, `updateInput(G)`, `getInput(G)` | Change fuel or ship state directly. |
| `systems/upkeep.js` | fuel, pump, lamp offline | `updateUpkeep(state, dt)`, `canPump(state)`, `pumpFuel(state, dt)`, `triggerLampOut(state)` | Spawn ships. |
| `systems/multitasking.js` | spawn, distress, urgency | `updateMultitasking(state, dt)`, `spawnShip(state)`, `updateDistress(state, dt)`, `getJobs(state)`, `maxActive(state)` | Directly steer ships. |
| `systems/escort.js` | aim, guidance, collision, harbor | `updateEscort(state, dt)`, `setBeamAim(state, x, y)`, `selectAttendedShip(state)`, `steerShip(state, ship, dt)`, `collideShip(state, ship)`, `checkHarbor(state, ship)` | Change fuel. |
| `systems/scoring.js` | points, best | `updateScoring(state, dt)`, `awardSafeShip(state, ship)`, `awardFuelSave(state)`, `loadBest(config)`, `saveBest(config, score)` | Affect survival. |
| `render/*` | drawing | `drawScene(state, ctx, effects)` | Change `state`. |
| `audio/*` | sound synthesis | `initAudio()`, `play(name, opts)`, `setMusicEnabled(bool)` | Change `state`. |
| `ui/screens.js` | DOM screens | `showScreen(name)`, `onStart()`, `onRestart()`, `onReturnTitle()` | Run gameplay rules. |
| `debug.js` | test access | see `# 8. DEBUG API` | Be used in normal UI. |

# 3. VISUAL SPEC

The game is a dark, hand-drawn storm. The screen is mostly black, deep blue, and wet charcoal. The lighthouse is a solid painted mass on the left; the sea is a layered watercolor wash; rocks are ink-outlined reefs with rough brush texture. The only strong light is the lamp beam, a warm amber bloom that cuts through the dark. Ships are pale silhouettes with small lanterns. The beam is the player’s hand: a moving wedge of light that can rescue a ship or lead it into danger. The screen never scrolls. Tension comes from the lamp’s shrinking fuel, the growing number of distressed boats, and the rocks waiting in the dark.

## Lighting and atmosphere

| Element | Visual rule |
| --- | --- |
| Base exposure | Very dark. Background luminance under 20%. |
| Beam | Additive amber light. Core is near-white, outer glow is amber. Beam width is `18px` core and `48px` glow. |
| Bloom | Beam and lamp flame bloom. Reduced motion disables animated bloom and keeps static glow. |
| Sea | Dark blue watercolor bands. Beam reflection is a broken amber path on water. |
| Rocks | Near-black with low orange edge highlight. Danger is shown by shape and edge, not hue alone. |
| Ships | Pale blue-grey silhouettes. Guided ships have a faint amber outline. Distress ships emit thin smoke and tilt. |
| Harbor | Cool blue arch marker, luminance high enough to be visible in dark. |
| Storm | Rain streaks are low-alpha diagonal lines. Reduced motion disables rain animation. |
| Hit flash | Full-screen orange flash, max opacity `0.35`, duration `0.18s`. |

## Space

| Region | Bounds | Contents |
| --- | --- | --- |
| Lighthouse zone | `x=0..200`, `y=0..720` | Tower, lamp, fuel pump, three wicks, oil gauge. |
| Open sea | `x=200..1280`, `y=120..680` | Ships, rocks, beam, particles. |
| Harbor | `x=0..130`, `y=500..570` | Safe zone marker. |
| HUD | top-right `x=1100..1260`, `y=20..60` | Score only. |

## Recipe table

| Layer | Recipe |
| --- | --- |
| Background | Vertical gradient `#05060a -> #0a0d14`. Add static paper noise alpha `0.03`. |
| Sea | Three horizontal watercolor bands: `#101826`, `#152235`, `#1b2a3d`. Offset by slow sine for ripple. |
| Rocks | Fill `#12141a`, stroke `#ff7043` at alpha `0.22`, rough brush edge noise. |
| Lighthouse | Fill `#1a1d24`, stone strokes `#2a2f38`, window light only when lamp online. |
| Lamp flame | Flame height scales with fuel. `0%` fuel means no flame. Low fuel flickers amber. |
| Fuel gauge | Painted vertical oil gauge on tower, `x=170..180`, `y=300..540`. Oil level is fuel. |
| Wicks | Three small flames at `x=120`, `140`, `160`, `y=665`. Alive wicks burn amber; dead wicks are black stubs. |
| Beam | Draw cone from lamp to aim point. Core alpha `0.72`, glow alpha `0.18`. Additive composite. |
| Ships | Silhouette polygon. Wake trail is pale blue alpha fade. Guided outline amber. |
| Particles | Splash: blue-white circles. Sparks: amber dots. Smoke: grey rising blobs. |
| Screen shake | Canvas transform translate by noise amplitude. Disabled by reduced motion. |
| Bloom | Offscreen beam layer blurred and composited with `lighter`. Disabled animated bloom under reduced motion. |
| Typography | Title and buttons are hand-lettered SVG paths with irregular stroke widths. Fallback font stack is cursive, but gameplay does not rely on text. |

# 4. GAMEPLAY SPEC

A single run is a storm watch. The player aims a lighthouse beam with the pointer and uses it to guide lost boats past rocks into a harbor. At the same time, the lamp burns fuel. If the player aims too long, the lamp may fail; if the player pumps fuel too long, ships drift toward rocks. The player can only attend one job at a time: the fuel pump or the nearest ship to the beam aim. Each ship worsens when ignored. Each life lost is a ship wreck or a dead lamp. The run ends when all lives are gone.

## Records and rosters

| Record | Count | Notes |
| --- | ---: | --- |
| Lighthouse | 1 | Static. |
| Lamp | 1 | Static at `(150, 220)`. |
| Fuel pump | 1 | Static hitbox. |
| Rocks | 4 | Static traps. |
| Ships | 3 types, max active by time/difficulty | Escort targets. |
| Lives/wicks | 3 | Diegetic life display. |
| Pickups | 0 | None. |
| Enemies | 0 | None. |
| Score | 1 | Tier 2. |
| Particles/effects | transient | Presentation only. |

## Rock roster

| Rock | Center | Collision radius | Visual radius | Kind |
| --- | --- | ---: | ---: | --- |
| `rock-top-1` | `(360, 460)` | `52` | `66` | top |
| `rock-bottom-1` | `(620, 600)` | `56` | `70` | bottom |
| `rock-top-2` | `(880, 460)` | `52` | `66` | top |
| `rock-bottom-2` | `(1080, 600)` | `56` | `70` | bottom |

Rocks are not collidable by the beam. They collide only with ships.

## Ship type roster

| Type | Base speed | Max speed | Steer rate | Collision radius | Distress rate | Base safe points |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dinghy | `42` | `70` | `3.4` | `18` | `1.0` | `120` |
| Sloop | `55` | `85` | `2.8` | `22` | `1.2` | `180` |
| Schooner | `68` | `100` | `2.2` | `26` | `1.45` | `260` |

All ships move from right to left when unattended. All ships are removed when docked or wrecked.

## Upkeep — Tier 1

### Rules

1. Fuel starts at `config.startFuel`.
2. While `lampOnline === true`, fuel drains at `config.fuelDrain` per second.
3. If the pointer is inside `fuelPumpRect` and `input.down === true`, then `pumping === true`.
4. While pumping:
   - fuel increases at `config.fuelRefill` per second;
   - the beam is disabled;
   - no ship is attended;
   - fuel cannot exceed `config.fuelMax`.
5. If fuel is `<= config.lowFuel`, the lamp flame flickers and the fuel gauge pulses.
6. If fuel reaches `<= 0`:
   - lose one life;
   - set `lampOnline = false`;
   - set `lampOfflineTimer = config.lampOfflineDuration`;
   - set `fuel = config.lampOfflineFuel`;
   - trigger screen shake amplitude `18`, duration `0.6s`;
   - trigger hit flash;
   - play `lamp_out`.
7. While `lampOnline === false`:
   - beam is disabled;
   - pumping has no effect;
   - lamp flame is off;
   - after `lampOfflineTimer`, `lampOnline = true`.
8. If lives reach `0`, run ends.

### Numbers

| Parameter | Normal | Easy | Intense |
| --- | ---: | ---: | ---: |
| Start fuel | `100` | `100` | `100` |
| Fuel max | `100` | `100` | `100` |
| Drain | `4.5/s` | `3.0/s` | `6.0/s` |
| Refill | `18/s` | `22/s` | `15/s` |
| Low fuel threshold | `30` | `30` | `30` |
| Lamp offline duration | `2.0s` | `2.0s` | `2.0s` |
| Lamp offline fuel | `25` | `30` | `20` |

## Multitasking — Tier 1

### Rules

1. The player can attend one job at a time:
   - if pumping, the fuel job is attended;
   - else if `beam.attendedShipId` is set, that ship job is attended;
   - otherwise no job is attended.
2. Each active ship is a job.
3. Each ship’s distress increases while unattended.
4. Each ship’s distress decreases while attended.
5. The spawn director creates more jobs over time.
6. The game must never have more than `maxActive` ships.
7. The first ship spawns at `config.spawnFirstAt`.
8. Spawn interval starts at `config.spawnIntervalBase` and decays linearly to `config.spawnIntervalMin`.
9. Type weights change by elapsed time and difficulty.
10. Ship urgency is used only for visuals and debug. It does not auto-select ships.

### Distress numbers

| Condition | Change |
| --- | ---: |
| Unattended | `+6 * type.distressRate` per second |
| Attended | `-22` per second |
| Minimum | `0` |
| Maximum | `100` |
| Panic threshold | `100` |

At `distress === 100`, ship steer rate is multiplied by `0.7` and drift toward nearest rock is stronger.

### Spawn rules

| Elapsed time | Normal max active | Easy max active | Intense max active |
| --- | ---: | ---: | ---: |
| `< 8s` | `0` | `0` | `0` |
| `8s..59s` | `1` | `1` | `1` |
| `60s..104s` | `2` | `2` | `3` |
| `105s..149s` | `3` | `3` | `5` |
| `>=150s` | `4` | `3` | `6` |

Spawn interval formula:

```text
interval = max(config.spawnIntervalMin,
             config.spawnIntervalBase - elapsed * config.spawnIntervalDecayPerSecond)
interval = interval * difficulty.intervalMultiplier
```

Difficulty interval multipliers:

| Difficulty | Multiplier |
| --- | ---: |
| Easy | `1.35` |
| Normal | `1.00` |
| Intense | `0.75` |

### Type weights — Normal

| Elapsed time | Dinghy | Sloop | Schooner |
| --- | ---: | ---: | ---: |
| `<60s` | `100%` | `0%` | `0%` |
| `60s..119s` | `60%` | `40%` | `0%` |
| `>=120s` | `40%` | `40%` | `20%` |

### Type weights — Easy

| Elapsed time | Dinghy | Sloop | Schooner |
| --- | ---: | ---: | ---: |
| `<60s` | `100%` | `0%` | `0%` |
| `60s..119s` | `80%` | `20%` | `0%` |
| `>=120s` | `60%` | `30%` | `10%` |

### Type weights — Intense

| Elapsed time | Dinghy | Sloop | Schooner |
| --- | ---: | ---: | ---: |
| `<60s` | `70%` | `30%` | `0%` |
| `60s..119s` | `40%` | `40%` | `20%` |
| `>=120s` | `20%` | `50%` | `30%` |

### Spawn position

| Field | Value |
| --- | ---: |
| Spawn x | `1280` |
| Spawn y | random `500..540` using seeded RNG |
| Initial vx | `-type.baseSpeed` |
| Initial vy | `0` |
| Initial distress | `0` |

## Escort — Tier 1

### Beam aiming

1. The pointer position is clamped to:
   - `x = config.beamAimMinX..config.beamAimMaxX`;
   - `y = config.beamAimMinY..config.beamAimMaxY`.
2. The clamped point is `beam.aimX, beam.aimY`.
3. The beam is drawn from `config.lampOrigin` to the aim point.
4. The beam is disabled if `pumping` or `lampOnline === false`.

### Guidance radius

```text
fuelFactor = clamp(fuel / config.fuelMax, 0.35, 1.0)
guideRadius = config.beamGuideRadius * fuelFactor
```

If `lampOnline === false`, `guideRadius = 0`.

### Attended ship selection

1. Candidate ships are active ships whose distance to `beam.aimX, beam.aimY` is `<= guideRadius`.
2. If there are candidates, choose the one with the smallest distance to the aim point.
3. Only that ship is attended.
4. If the player is pumping, there is no attended ship.

### Ship steering

If attended:

```text
target = beam.aimX, beam.aimY
if distance(ship, target) < 40:
  desiredDirection = (-1, 0)
else:
  desiredDirection = normalize(target - ship.position)
desiredVelocity = desiredDirection * ship.maxSpeed
```

If unattended:

```text
baseVelocity = (-ship.baseSpeed, 0)
nearestRock = rock with minimum distance to ship
driftMagnitude = (ship.distress / 100) * 0.85 * ship.maxSpeed
if ship.distress == 100:
  driftMagnitude *= 1.25
driftDirection = normalize(nearestRock.position - ship.position)
desiredVelocity = baseVelocity + driftDirection * driftMagnitude
clampMagnitude(desiredVelocity, ship.maxSpeed)
```

Steering response:

```text
response = min(1, ship.steerRate * dt)
if ship.distress == 100:
  response *= 0.7
ship.vx = lerp(ship.vx, desiredVelocity.x, response)
ship.vy = lerp(ship.vy, desiredVelocity.y, response)
ship.x += ship.vx * dt
ship.y += ship.vy * dt
```

Clamp ship y to `120..680`. Do not clamp x above `1280`.

### Rock collision

For every active ship:

```text
distance = hypot(ship.x - rock.x, ship.y - rock.y)
if distance < ship.collisionRadius + rock.collisionRadius:
  wreck ship
```

On wreck:

- remove ship;
- lose one life;
- screen shake amplitude `12`, duration `0.45s`;
- hit flash;
- splash particles;
- play `rock_crash`.

### Harbor safety

A ship is docked if:

```text
ship.x <= config.harborRect.xMax
and ship.y >= config.harborRect.yMin
and ship.y <= config.harborRect.yMax
```

On dock:

- remove ship;
- play `safe_dock`;
- Tier 2 awards points.

## Scoring — Tier 2

### Rules

1. Scoring is disabled unless `config.scoringEnabled === true`.
2. Score is always an integer.
3. Survival points are added continuously.
4. Docked ships award points scaled by their distress at the moment they become safe.
5. Fuel-save bonus is awarded once per lamp cycle.
6. Best score is stored per difficulty.

### Numbers

| Event | Normal | Easy | Intense |
| --- | ---: | ---: | ---: |
| Survival per second | `6` | `4` | `8` |
| Dinghy base | `120` | `120` | `120` |
| Sloop base | `180` | `180` | `180` |
| Schooner base | `260` | `260` | `260` |
| Distress multiplier | `1 + (100 - distress) / 200` | same | same |
| Fuel-save bonus | `40` | `25` | `60` |

Safe ship score:

```text
multiplier = 1 + (100 - ship.distress) / 200
points = floor(ship.safePoints * multiplier)
```

Fuel-save bonus conditions:

```text
fuel was < 10
fuel becomes >= 50 while pumping
award once per lampOnline cycle
```

Best score storage:

```text
localStorage key: lighthouse.best.<difficulty>
```

## Progression and difficulty

### Run shape

| Time | Normal intended pressure |
| ---: | --- |
| `0..8s` | No ships. Learn fuel and beam. |
| `8..60s` | One ship. Basic escort and fuel tradeoff. |
| `60..105s` | Up to two ships. Choose which boat to save. |
| `105..150s` | Up to three ships. Fuel pressure rises. |
| `>=150s` | Up to four ships. Tight pumping windows. |

### Difficulty presets

| Parameter | Easy | Normal | Intense |
| --- | ---: | ---: | ---: |
| Lives | `4` | `3` | `2` |
| Max active cap | `3` | `4` | `6` |
| Fuel drain | `3.0/s` | `4.5/s` | `6.0/s` |
| Fuel refill | `22/s` | `18/s` | `15/s` |
| Spawn interval multiplier | `1.35` | `1.00` | `0.75` |
| Ship speed multiplier | `0.85` | `1.00` | `1.15` |
| Distress rate multiplier | `0.85` | `1.00` | `1.25` |
| Beam guide radius | `190` | `170` | `155` |
| Time score rate | `4/s` | `6/s` | `8/s` |

Ship speed and max speed are multiplied by the ship speed multiplier when the ship is created.

## Feel

The intended feeling is a small, frantic watch. The player should feel the beam as a hand: moving it near a ship pulls that ship toward safety, but leaving the fuel pump too long darkens the lamp. The tension comes from three visible clocks:

1. The fuel gauge falling.
2. Each ship’s distress rising.
3. The rocks waiting in the dark.

The player is never forced into combat or movement. The game asks only: where do you look, and what do you hold?

# 5. CHARACTERS

## Lighthouse keeper

No visible avatar. The player is represented by:

- the beam aim point;
- the fuel pump being held;
- the lamp flame responding to fuel.

Facings: none.

States:

| State | Visual |
| --- | --- |
| Aiming | Beam follows pointer. |
| Pumping | Fuel pump handle moves, sparks, beam disabled. |
| Lamp offline | Flame gone, wicks dim, beam disabled. |

## Lighthouse

Silhouette: tapered tower on rocky shore, small gallery, lamp room, painted fuel gauge on tower, three wick flames near base.

Animation names:

| Animation | Motion rule |
| --- | --- |
| `idle` | Static. Slow rain only. |
| `lamp_flicker` | Flame height `fuel/100`. Flicker amplitude increases below `30` fuel. |
| `pump_move` | Pump handle vertical offset `sin(t*14)*4px` while pumping. |
| `lamp_offline` | Flame scale `0`, smoke puff once, no glow. |
| `wick_extinguish` | Wick flame collapses over `0.4s`, becomes black stub. |

Facings: fixed left/right structure. No gameplay facing.

## Beam

Silhouette: wedge from lamp to aim point.

Animation names:

| Animation | Motion rule |
| --- | --- |
| `beam_sweep` | End point follows clamped pointer. No smoothing except `0.08s` render interpolation. |
| `beam_low_fuel` | Core brightness multiplied by `0.55 + 0.45 * fuel/100`. |
| `beam_offline` | Not drawn. |
| `beam_pumping` | Draw only short stub to pump, no sea guidance. |

## Ships

All ships are pale, hand-drawn silhouettes. They are escort targets, not enemies.

### Dinghy

Silhouette: small rowboat, single mast stub, lantern dot.

Animation names:

| State | Animation | Rule |
| --- | --- | --- |
| active | `drift_left` | Bob `sin(t*3)*2px`, tilt `vx*0.001 rad`. |
| attended | `guided` | Amber outline, wake trail stronger. |
| distress >50 | `smoke_trail` | Smoke particles every `0.25s`. |
| distress ==100 | `panic` | Tilt oscillates `sin(t*9)*0.12 rad`, lantern flickers. |
| docked | `dock` | Fade over `0.3s`, move into harbor. |
| wrecked | `wreck` | Rotate `+0.7 rad`, sink `80px/s`, splash. |

### Sloop

Silhouette: medium sailboat, one sail, lantern dot.

Animation names: same as Dinghy, but bob `sin(t*2.4)*3px`, sail flutter stronger.

### Schooner

Silhouette: tall two-sail boat, lantern dot.

Animation names: same as Dinghy, but bob `sin(t*1.8)*4px`, slower turn response visually.

## Rocks

Silhouette: jagged reef shapes. Top rocks rise from above; bottom rocks rise from below.

Animation names:

| State | Animation |
| --- | --- |
| idle | Static. |
| hit | Brief white edge flash `0.12s`. |

Facings: fixed.

## Wicks

Three small flames at lighthouse base.

States:

| State | Visual |
| --- | --- |
| alive | Amber flame, flicker. |
| extinguished | Black stub, smoke once. |

# 6. AUDIO

The audio API is assumed to support oscillators, noise buffers, filters, gain envelopes, and simple playback. All sounds are synthesized. No external assets.

## Music

| Name | Recipe | When |
| --- | --- | --- |
| `ambient_storm` | Two detuned triangle oscillators at `48Hz` and `52Hz`, slow LFO filter cutoff `180Hz -> 320Hz`, plus brown noise at `-28dB`, no percussive beat. | Title, playing, game over. Volume ducks to `-10dB` on life loss for `0.8s`. |

## Sound effects

| Name | Recipe | When |
| --- | --- | --- |
| `ui_click` | Square `180Hz`, 30ms, gain `0.2`, quick decay. | Start, restart, difficulty buttons. |
| `beam_hum` | Sawtooth `58Hz` through lowpass `420Hz`, volume `0.06 * fuel/100`. | Continuous while beam enabled. |
| `fuel_pump_click` | Noise burst bandpass `900Hz`, 60ms, plus sine `110Hz` thump. | Every `0.25s` while pumping. |
| `fuel_low_warning` | Two sine pulses `220Hz` and `175Hz`, 120ms apart. | First time fuel crosses below `30`, then every `5s` while below. |
| `lamp_out` | Sine sweep `300Hz -> 70Hz`, 700ms, plus filtered noise. | Fuel reaches `0`. |
| `lamp_relit` | Soft sine `420Hz` swell, 300ms. | Lamp offline timer ends. |
| `ship_spawn` | Lowpass noise whoosh, 250ms, plus faint bell `430Hz`. | Ship spawn. |
| `ship_guided` | Highpassed noise wind, `-30dB`, while attended. | Continuous while attended. |
| `ship_panic` | Low rumble noise, bandpass `160Hz`, volume scales with distress. | Distress >70. |
| `safe_dock` | Wood knock: sine `160Hz`, 80ms, plus water splash noise burst. | Ship enters harbor. |
| `rock_crash` | Noise burst bandpass `500Hz`, 180ms, plus low sine `80Hz` thump. | Ship collides with rock. |
| `life_lost` | Filtered wood crack: noise `700Hz`, 140ms, plus descending sine `260Hz -> 120Hz`. | Any life loss. |
| `game_over` | Low drone `40Hz`, slow fade in, no beat. | Game Over. |
| `score_tick` | Tiny sine `880Hz`, 20ms, gain `0.08`. | Tier 2 score increase at safe ship only. |

# 7. UX

## State machine

| State | Enter | Exit |
| --- | --- | --- |
| `title` | Initial load or return from game over. | `playing` when Start clicked. |
| `playing` | Start clicked. | `gameover` when `lives <= 0`. |
| `gameover` | Lives reach zero. | `playing` when Restart clicked, `title` when Return to Title clicked. |

No pause state.

## Screens

### Title screen

HTML/CSS/SVG only.

Elements:

| Element | Behavior |
| --- | --- |
| `#title` | Hand-lettered SVG title. |
| `#difficulty-select` | Three buttons: Easy, Normal, Intense. Selected button has thick outline. |
| `#start` | Starts a run with selected difficulty and random seeded run. |
| `#reduced-motion` | Toggle checkbox. Default follows `prefers-reduced-motion`. |

No score on title.

### Game Over screen

Elements:

| Element | Behavior |
| --- | --- |
| `#gameover-title` | Hand-lettered “The Lamp Went Dark”. |
| `#final-score` | Final integer score. |
| `#best-score` | Best score for current difficulty. Tier 2. |
| `#restart` | Restarts with a new random seed, same difficulty. |
| `#return-title` | Returns to title. |

## HUD

The HUD is HTML/CSS only and contains exactly one score element.

| Element | Record field | When visible |
| --- | --- | --- |
| `#hud-score` | `state.score` | `mode === 'playing'` |

Fuel is shown as a painted gauge on the lighthouse. Lives are shown as three wicks. Neither is a HUD element.

## Input contract

| Input | Action |
| --- | --- |
| `pointermove` | Sets beam aim point. |
| `pointerdown` inside `fuelPumpRect` | Starts pumping. |
| `pointermove` while inside pump and held | Continues pumping. |
| `pointermove` outside pump while held | Stops pumping. |
| `pointerup` | Stops pumping. |
| Click `#start` | Start run. |
| Click `#restart` | Restart run. |
| Click `#return-title` | Return to title. |

No keyboard movement. Keyboard may activate HTML buttons for accessibility, but gameplay remains pointer-only.

# 8. DEBUG API

The debug API is for tests and development only. It must not be used by normal UI.

| Function | System | Direct effect |
| --- | --- | --- |
| `debug.upkeep.setFuel(value)` | Upkeep | Sets `state.fuel` clamped to config. |
| `debug.upkeep.getFuel()` | Upkeep | Returns `state.fuel`. |
| `debug.upkeep.forceLampOut()` | Upkeep | Calls `triggerLampOut(state)`. |
| `debug.multitasking.spawnShip(type, x, y)` | Multitasking | Adds a ship with given type and position. |
| `debug.multitasking.setShipDistress(shipId, value)` | Multitasking | Sets ship distress clamped to `0..100`. |
| `debug.multitasking.getJobs()` | Multitasking | Returns job urgencies for fuel and ships. |
| `debug.escort.setBeamAim(x, y)` | Escort | Sets clamped beam aim. |
| `debug.escort.getAttendedShipId()` | Escort | Returns `state.beam.attendedShipId`. |
| `debug.escort.forceCollision(shipId)` | Escort | Runs rock collision check for that ship. |
| `debug.scoring.addScore(amount)` | Scoring | Adds integer to `state.score`. |
| `debug.scoring.getScore()` | Scoring | Returns `state.score`. |
| `debug.inputs.moveBeam(x, y)` | Input | Updates `G.input.x/y`. |
| `debug.inputs.setPumpHeld(bool)` | Input | Sets `G.input.down` and pump-inside flag. |
| `debug.state.setLives(value)` | Core state | Sets `state.lives` clamped. |
| `debug.state.setMode(mode)` | Core state | Sets `state.mode`. |

# 9. TESTS

## Tier 1 tests

| Test | Pass condition |
| --- | --- |
| Fixed-step determinism | With seed `0x5EED`, identical input sequence produces identical state hash after `30s`. |
| No movement input | No keyboard or gamepad input changes ship or fuel state. |
| Beam aim clamping | Setting pointer outside bounds clamps aim to `beamAimMin/Max`. |
| Fuel drain | With lamp online and no pump, fuel decreases by `fuelDrain * dt` each update. |
| Fuel pump | With pointer inside pump and held, fuel increases by `fuelRefill * dt`, beam disabled, no attended ship. |
| Fuel empty life loss | Setting fuel `0` triggers one life loss, lamp offline `2s`, fuel `25`. |
| Lamp offline disables guidance | During lamp offline, `guideRadius === 0` and no ship can be attended. |
| First spawn | With seed and no inputs, no ships before `8s`, at least one active ship after `8s`. |
| Active cap | Active ships never exceed `maxActive` for current elapsed time and difficulty. |
| Distress increases unattended | A spawned ship with no beam nearby has distress increase every update. |
| Distress decreases attended | A ship within guide radius and nearest to aim has distress decrease every update. |
| Single attended ship | If multiple ships are within guide radius, exactly one is attended. |
| Pump overrides guidance | While pumping, `attendedShipId === null`. |
| Rock collision | A ship forced to collide with a rock causes one life loss and ship removal. |
| Harbor safety | A ship placed in harbor becomes `docked` and is removed. |
| Life loss ends run | Setting lives to `0` transitions to `gameover`. |
| HUD score element exists | `#hud-score` exists and is visible during `playing`. |
| Reduced motion | With `reducedMotion=true`, screen shake amplitude is `0`, trails are disabled, animated bloom is disabled. |
| Difficulty presets | Easy/Normal/Intense produce correct config values and do not crash. |
| Colour-blind safe | No required distinction relies only on red vs green. Danger has shape/edge cues. |

## Tier 2 tests

| Test | Pass condition |
| --- | --- |
| Survival score | Score increases by `timeScoreRate * dt` while playing. |
| Safe ship score | Docking a ship awards `floor(base * (1 + (100-distress)/200))`. |
| Distress scaling | A ship docked at distress `0` scores `1.5x` base; at distress `100` scores `1.0x` base. |
| Fuel-save bonus | Crossing fuel from `<10` to `>=50` while pumping awards configured bonus once. |
| Score integer | Score is always integer. |
| Best score storage | After game over, best score is stored under correct difficulty key. |
| Best score display | Game Over shows final and best score. |
| Scoring disabled | With `scoringEnabled=false`, score remains `0` and core game still works. |

# 10. BUILD ORDER

1. Create `index.html`, canvas, DOM screens, HUD score element, CSS palette variables.
2. Implement seeded RNG and fixed-step loop.
3. Implement config presets and accessibility config.
4. Implement state records and run reset.
5. Implement pointer input and pump hitbox.
6. Implement Upkeep: fuel drain, pump, lamp offline, life loss.
7. Implement Multitasking: spawn timer, max active, ship records, distress update.
8. Implement Escort: beam aim, guidance selection, ship steering, rock collision, harbor safety.
9. Implement draw scene: lighthouse, sea, rocks, beam, ships, wicks, fuel gauge.
10. Implement effects: shake, hit flash, particles, trails, bloom.
11. Implement audio: ambient music and required foley.
12. Implement title and game over state machine.
13. Verify Tier 1 with deterministic tests.
14. Add Scoring module and best score storage.
15. Verify Tier 2 with scoring tests.
16. Stop. No extra mechanics.

# 11. DEFINITION OF DONE

## Tier 1 Definition of Done

High level: a player can start from title, play a single-screen tense survival run, lose lives from ship wrecks or fuel failure, and reach game over. The game is drawn in the required style, heard through synthesized audio, shows the score HUD element, and supports required accessibility baseline.

- [ ] Fixed-step loop exists and does not use `Math.random()` in gameplay.
- [ ] Seeded RNG is used for ship type and position.
- [ ] Title screen starts Normal/Easy/Intense run.
- [ ] Game Over screen appears when lives reach zero.
- [ ] Pointer can aim beam.
- [ ] Pointer can hold fuel pump and refill fuel.
- [ ] Fuel drains, refills, warns below `30`, and causes life loss at zero.
- [ ] Lamp offline state disables beam and relights after configured duration.
- [ ] Ships spawn after first spawn time and respect active caps.
- [ ] Each ship type has its listed stats.
- [ ] Unattended ships increase distress.
- [ ] Attended ships decrease distress.
- [ ] Only one ship can be attended at a time.
- [ ] Pumping disables ship guidance.
- [ ] Ships steer toward beam aim when attended.
- [ ] Ships drift toward nearest rock when unattended.
- [ ] Ship-rock collision causes one life loss.
- [ ] Ship-harbor entry removes ship safely.
- [ ] Three lives are represented by three wicks.
- [ ] HUD contains only `#hud-score`.
- [ ] Scene uses dark palette and hand-drawn/painterly style.
- [ ] Beam bloom, particles, trails, hit flash, and screen shake exist.
- [ ] Ambient music and realistic foley play.
- [ ] Reduced motion disables animated bloom, shake, trails, and most particles.
- [ ] Difficulty presets change only config.
- [ ] Debug API functions exist.
- [ ] Tier 1 tests pass.

## Tier 2 Definition of Done

High level: the working core game now records and displays meaningful scores and best scores.

- [ ] `scoringEnabled` can be false without breaking core.
- [ ] Survival score increases in real time.
- [ ] Docking ships awards type points scaled by distress.
- [ ] Fuel-save bonus works once per lamp cycle.
- [ ] Score is integer.
- [ ] Best score is stored per difficulty.
- [ ] Game Over displays final and best score.
- [ ] Tier 2 tests pass.

# A. SANITY

| Check | Result | Notes |
| --- | --- | --- |
| Are all requested mechanics present? | Yes | Upkeep, Multitasking, Escort, Scoring. |
| Are extra mechanics added? | No | No pickups, no combat, no movement, no pause, no wind system. |
| Are core mechanics tier 1? | Yes | Upkeep, Multitasking, Escort are Tier 1. |
| Is scoring tier 2? | Yes | Scoring is Tier 2 and optional for core. |
| Does Tier 1 include required art/audio/effects? | Yes | Required style, audio, effects, and HUD element are Tier 1. |
| Is HUD limited to score? | Yes | Only `#hud-score` is HUD. Fuel/lives are diegetic. |
| Is input cursor-only? | Yes | Pointer move, pointer hold, UI clicks. No movement input. |
| Is failure lose a life? | Yes | Rock collision and fuel empty each lose one life. |
| Is win/lose survive as long as possible? | Yes | No win state; game ends at zero lives. |
| Are screens only title and game over? | Yes | State machine has only those screens. |
| Are numbers explicit? | Yes | Fuel, lives, rocks, ships, spawn, scoring, difficulty all have numbers. |
| Are records present? | Yes | GameState, RunConfig, Ship, Rock, Beam, etc. |
| Are module contracts present? | Yes | File ownership, global context, functions. |
| Are accessibility requirements present? | Yes | Colour-blind safe palette, reduced motion, difficulty options. |
| Are effects present? | Yes | Screen shake, particles, hit flash, trails, bloom. |
| Are audio recipes present? | Yes | Synthesized recipes table. |
| Are tests tied to tiers? | Yes | Tier 1 and Tier 2 test lists. |
| Did any contradiction appear? | Yes, corrected | Initial thinking placed fuel/lives in HUD; corrected to diegetic scene objects to satisfy “HUD: score”. |
| Final status | Valid | Spec is ready for an agent to build Tier 1 first, then Tier 2. |