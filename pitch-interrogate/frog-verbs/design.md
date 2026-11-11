# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Browser game. | `index.html`, `src/main.js`, Canvas + HTML/CSS UI. |
| Platformer where you play as a frog. | `# 4. GAMEPLAY SPEC`, `# 5. CHARACTERS`, Frog Movement. |
| Side-view platformer camera follows the frog across a pond segment. | `# 1. CONVENTIONS`, Camera, `src/camera.js`. |
| Keep relevant ledges, hazards, heron perches, sight lines, safe-ledge moss, and water depth readable. | `# 3. VISUAL SPEC`, `# 4. GAMEPLAY SPEC`. |
| Real-time time cycle: dusk → deep dusk → night → continuous night change. | Core mechanic: Time Cycle. `src/timeCycle.js`. |
| Run starts at dusk from a dry, hazard-free, sight-line-free entry ledge. | Level Segment 01: `entry_ledge`, `# 4. GAMEPLAY SPEC`. |
| Goal is the old nursery pool on the far side. | Level Segment 01: `goal_pool`, run-ending logic. |
| Leaving the pond segment ends the run and its time cycle. | Run boundary logic in `src/state.js`. |
| Difficulty rises at fixed stage boundaries and continues changing through night. | Time Cycle stage table, water/pad events. |
| Tone: small frog crossing a dusk marsh, staying quiet under herons, hazards bite, hidden moonflies mark secret routes, night rearranges safe paths. | `# 3. VISUAL SPEC`, `# 4. GAMEPLAY SPEC`, `# 6. AUDIO`, `# 7. UX`. |
| Look: rain-swollen marsh, pale-bellied frog, pale moss safe ledges, pale glints, moonfly glows, reduced contrast at night. | `# 3. VISUAL SPEC`. |
| Sound: wet landings, heron caws, splashes, current ripples, clear hazard-timing cues. | `# 6. AUDIO`. |
| Core mechanics: Frog Movement, Platforms and Safe Ledges, Heron Stealth, hazards, Water and Current, time cycle. | Tier 1, `# 4. GAMEPLAY SPEC`. |
| Supporting mechanics: Moonflies and Hidden Routes, Tilting Lily Pads. | Tier 2, `# 4. GAMEPLAY SPEC`. |
| Extra mechanics: none. | No extra systems are added. |
| Content: small pale-bellied frog, rain-swollen marsh, lily pads, tilting lily pads, half-sunk logs, reed ledges, wet stepping stones, low mushroom caps, herons, sight lines, shadows, caws, safe ledges, last safe ledge, entry ledge, pale glints, pale moss, cattail thorns, slick oil, snapping turtle jaws, sharp reed bundles, deep water, shallow water, current, time cycle, dusk/deep dusk/night, rising water, sinking/rising pads, moonflies, moonfly glows, hidden stones, secret crossings, old nursery pool. | Rosters and system specs in `# 4. GAMEPLAY SPEC`. |
| Left out: combat, story with named characters, survival feeding/thirst, creature-collection, block-pushing puzzles, hidden stats/confusing rules, instant death from deep water, lives, fighting hazards, mandatory moonflies, time cycles that loop to dusk, drowning from rising water. | `# 0.2 Decisions`, `# 9. TESTS`, `# A. SANITY`. |

## 0.2 Decisions

| Decision | Source | Ruling | Why |
| --- | --- | --- | --- |
| Game is a side-view platformer. | Provided | Fixed. | Required. |
| Player is a small pale-bellied frog. | Provided | Fixed. | Character identity is fixed. |
| No named characters. | Provided | Fixed. | Avoid story. |
| No combat. | Provided | Fixed. | Hazards are read/avoided, not fought. |
| No lives. | Provided | Fixed. | Hazards/herons reset position, not kill. |
| No instant death from deep water. | Provided | Fixed. | Deep water carries to safe edge. |
| No drowning from rising water. | Provided | Fixed. | Water removes footing, then depth/current rules apply. |
| No mandatory moonflies. | Provided | Fixed. | Optional collectibles reveal hidden routes only. |
| No time cycle loop back to dusk. | Provided | Fixed. | Cycle runs once per run. |
| Core mechanics are Tier 1. | Provided | Fixed. | Tier 1 must be finishable. |
| Supporting mechanics are Tier 2. | Provided | Fixed. | They are additions, not dependencies. |
| Extra mechanics: none. | Provided | Fixed. | No Tier 3 systems. |
| Core bullet mentions “some pads tilt” while Supporting lists Tilting Lily Pads. | Conflict | The actual interactive tilting behavior is Tier 2. Tier 1 only includes the safe-ledge condition `tiltAngle == 0` and a debug field. No normal Tier 1 pad tilts. | Preserves Tier 1 independence and honors supporting mechanics as Tier 2. |
| Viewport. | Open | 960×540 canvas, level 2560×540, horizontal camera only. | Enough room for a single pond segment and readable sight lines. |
| Units. | Open | Pixels and seconds. World axes: x right, y down. Gravity positive down. | Direct Canvas mapping, simple AABB physics. |
| Fixed timestep. | Open | 60 Hz fixed update, max 5 steps/frame, render interpolates. | Deterministic platforming and heron timing. |
| Input. | Open | Keyboard: Left/Right walk/turn, Down duck, Space short-hop, Shift+Space long-hop. | Clear named inputs; no air rescue. |
| Air control. | Open | 0 while airborne. Horizontal velocity is locked at takeoff. | Enforces committed hops. |
| Coyote time. | Open | 0. | No rescue from bad takeoff. |
| Jump buffer. | Open | 0.10 s. | Minor input tolerance, not movement rescue. |
| Frog size. | Open | Standing AABB 18×14, crouched 18×8. | Small frog silhouette, duck/hide logic. |
| Frog walk speed. | Open | 150 px/s, duck speed 45 px/s. | Supports short/long gap design. |
| Short hop. | Open | Initial vy = -261 px/s, height ≈ 34 px, airtime ≈ 0.522 s. | Named short-hop. |
| Long hop. | Open | Initial vy = -358 px/s, height ≈ 64 px, airtime ≈ 0.716 s. | Named long-hop; defines shallow/deep threshold. |
| Max jump height. | Open | 64 px. | Required for shallow/deep water rule. |
| Required gap design. | Open | Short gaps 45–62 px. Long gaps 72–96 px. No rescue air control. | Makes gaps committed. |
| Level content count. | Open | One segment with 28 initial crossing surfaces, 2 herons, 12 hazards, 6 moonflies, 6 hidden stones. | Concrete roster without adding extra systems. |
| Surface type counts. | Open | 10 lily pads, 4 half-sunk logs, 5 reed ledges, 6 wet stepping stones, 3 low mushroom caps. | Exactly the provided platform types. |
| Hazard counts. | Open | 4 cattail thorns, 2 snapping turtle jaws, 3 sharp reed bundles, 3 slick oil patches. | Exactly the provided hazard types. |
| Heron count. | Open | 2 herons at far-side perches. | Enough for suppression rules, not chaotic. |
| Moonfly count. | Open | 6 moonflies revealing 6 hidden stones. | Set complete but optional. |
| Stage boundaries. | Open | Dusk 0–90 s, Deep dusk 90–180 s, Night 180+ with continuous change until 600 s then asymptotic hold. | Real-time, once, never loops. |
| Waterline. | Open | Dusk y=400, Deep dusk y=385, Night boundary y=360, continuous night to y=318. Entry/goal top y=300 remain dry. | Rises without drowning entry/goal. |
| Shallow/deep threshold. | Open | depth ≤ 64 px shallow, > 64 px deep. | Matches max jump height. |
| Current. | Open | Carries at 55 px/s toward nearest safe edge; weak steer 18 px/s; ignores hazards/herons; fallback entry. | Deep water is transport, not death. |
| Safe ledge definition. | Provided | Solid, dry, outside active sight line, not touching hazard, not tilting/sinking. | Fixed. |
| Last safe ledge. | Provided | Default reset after hazard/heron. | Fixed. |
| Safe fallback. | Provided | Search backward along path; else entry ledge. | Fixed. |
| Entry ledge. | Provided | Always dry, hazard-free, outside sight lines. | Fixed. |
| Heron visibility meters. | Open | 0–100. Fill 38/34/30 per second by stage. Drain 55/s. Warning 1.1 s. | Enough time to stop/hide. |
| Heron warning resolution. | Open | Once warning starts, only full hiding aborts. Leaving the line without occlusion does not abort. | Clarifies “must be fully hidden before caw ends.” |
| Multiple heron suppression. | Provided | One warning suppresses others; dive clears all. | Fixed. |
| Same-instant fill tie-break. | Provided | Closest sight line triggers. | Fixed. |
| Hazard hit. | Provided | No death/life cost; reset to last safe ledge or fallback. | Fixed. |
| Turtle jaws. | Open | Closed 2.0 s, pre-snap 0.45 s, open 1.2 s. Closed is platform; open is hazard. | Readable timing hazard. |
| Oil patches. | Open | Slide 130 px/s; if slide lands on ledge, reset; if reaches water, current. | Fixed traction behavior. |
| Reed bundles. | Open | Landing rejection; standing/walking contact also hazard hit. | “Feet touch” includes grounded contact. |
| Time-cycle surface changes. | Open | Low shortcuts sink at boundaries; two optional rising pads create new crossings; primary route remains above waterline. | Makes learned path a gamble without making run impossible. |
| Hidden route. | Open | Optional upper route using revealed stones, harder, can avoid herons but passes hazards. | Matches provided optional harder route. |
| Tilting pads. | Open | 3 optional tilting lily pads in Tier 2. Max tilt 28°, failure slides into water. | Tier 2 addition, not required. |
| HUD. | Open | Shows stage, warning countdown, optional moonfly count in Tier 2. No hidden stats. | Readability. |
| Screens. | Open | Title, playing, ended_success, ended_left, debug. No pause system. | Avoids extra mechanics. |
| Audio. | Open | Synthesized SFX + ambient music only. | Required look/sound and tier 1 audio. |

## 0.3 Tiers

Tier list is priority order.

1. **Tier 1 — Core playable crossing.**  
   Build: fixed loop, input, frog movement, static platforms, safe ledges/moss, last-safe reset, heron sight lines and warnings, hazards, shallow/deep water/current, time cycle stage boundaries, segment 01 normal route, entry ledge, goal pool, camera, HUD, screens, palette, animations, SFX/music.  
   Must be finishable without moonflies or tilting.

2. **Tier 2 — Optional depth.**  
   Build: moonflies, hidden stones, secret crossing, time-cycle visibility boost, tilting lily pads.  
   Must not be required to finish.

3. **Tier 3 — None.**  
   Extra mechanics: none.

---

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Value | Number | Meaning |
| --- | ---: | --- |
| Canvas logical size | 960×540 px | Playfield viewport. |
| Level width | 2560 px | One pond segment. |
| Level height | 540 px | No vertical scroll. |
| World axes | x right, y down | Canvas coordinates. |
| Gravity | +1000 px/s² | Positive y is down. |
| Fixed timestep | 1/60 s | Gameplay update. |
| Max steps/frame | 5 | Prevent spiral of death. |
| Render interpolation | enabled | Smooth visuals, fixed logic. |
| Frog standing AABB | 18×14 px | Collision box. |
| Frog crouched AABB | 18×8 px | Duck/hide box. |
| Frog center offset | y = top + h/2 | For sight-line distance. |
| Walk speed | 150 px/s | Ground horizontal max. |
| Duck speed | 45 px/s | Ground horizontal max while ducked. |
| Ground accel | 900 px/s² | Control. |
| Ground friction | 1200 px/s² | Stop. |
| Air control | 0 px/s | Committed hops. |
| Short-hop initial vy | -261 px/s | Tap short hop. |
| Long-hop initial vy | -358 px/s | Shift+Space long hop. |
| Short-hop height | 34 px | Calculated. |
| Long-hop height | 64 px | Calculated. |
| Short-hop airtime | 0.522 s | Calculated. |
| Long-hop airtime | 0.716 s | Calculated. |
| Short-hop horizontal reach | 78 px | At 150 px/s. |
| Long-hop horizontal reach | 107 px | At 150 px/s. |
| Design short gap | 45–62 px | Required short hop. |
| Design long gap | 72–96 px | Required long hop. |
| Landing tolerance | 4 px | Feet crossing top. |
| Jump buffer | 0.10 s | Input tolerance. |
| Coyote time | 0 s | No ledge rescue. |
| Max jump height | 64 px | Defines shallow water. |
| Shallow water threshold | bottom - waterline ≤ 64 px | Frog can jump out. |
| Deep water threshold | bottom - waterline > 64 px | Current starts. |
| Initial waterline | y=400 | Dusk. |
| Deep dusk waterline | y=385 | At 90 s. |
| Night boundary waterline | y=360 | At 180 s. |
| Night max waterline | y=318 | After t=600 s. |
| Entry ledge top | y=300 | Always dry. |
| Goal ledge top | y=300 | Always dry. |
| Primary safe surface top | y ≤ 300 | Always above night water. |
| Low shortcut top | y 330–390 | Sinks later. |
| Rising optional pad initial top | y=360 | Rises at boundaries. |
| Current speed | 55 px/s | Toward safe edge. |
| Current steer | 18 px/s | Weak player influence. |
| Current timeout | 10 s | Then entry fallback. |
| Heron meter max | 100 | Notice. |
| Dusk fill rate | 38/s | Moving in line. |
| Deep dusk fill rate | 34/s | Moving in line. |
| Night fill rate | 30/s | Moving in line. |
| Drain rate | 55/s | Hidden/outside/no warning. |
| Warning duration | 1.1 s | Caw countdown. |
| Turtle closed | 2.0 s | Platform. |
| Turtle pre-snap | 0.45 s | Cue. |
| Turtle open | 1.2 s | Hazard. |
| Oil slide speed | 130 px/s | Traction hazard. |
| Oil forced slide time | 0.35 s | Minimum loss of control. |
| Tilting max angle | 28° | Tier 2 failure. |
| Moonfly radius | 10 px | Pickup hitbox. |
| Hidden stone width | 36–52 px | Optional surfaces. |

## 1.2 Important conventions

- Use one deterministic RNG: `mulberry32(0x20250101)` for particles/ambient only. Gameplay never uses random.
- All gameplay logic runs in fixed-step `updateFixed(ctx, dt)`.
- Input is sampled per fixed step from an `inputState` snapshot.
- No hidden stats. All visible values are HUD/visual rules.
- All surfaces are AABB solids. Non-solid visual props cannot block movement.
- All sight lines are line segments with ray-AABB intersection and occlusion checks.
- Reset always chooses a point on a currently safe interval, never water/hazard/tilting/sight line.
- A “safe ledge” is a surface interval, not necessarily the whole surface.
- A “safe edge” is a point on a safe interval reachable from water.
- The entry ledge is the final fallback.
- Time cycle begins at run start and stops at run end.
- Stage boundaries are absolute run time, not player position.
- No pause system. Debug state is not player-facing.
- All sounds are synthesized from Web Audio API.
- All UI screens are HTML/CSS. Canvas draws only game world.

---

# 2. CONTRACTS

## 2.1 Module layout

```text
index.html
styles.css
src/main.js
src/gameLoop.js
src/input.js
src/state.js
src/frog.js
src/platforms.js
src/herons.js
src/hazards.js
src/water.js
src/timeCycle.js
src/moonflies.js
src/tilting.js
src/camera.js
src/render.js
src/audio.js
src/hud.js
src/levels/segment01.js
src/debug.js
```

| File | Tier | Responsibility |
| --- | --- | --- |
| `main.js` | 1 | Boot, canvas, context init, loop start. |
| `gameLoop.js` | 1 | Fixed step, accumulator, render interpolation. |
| `input.js` | 1 | Keyboard named inputs, buffer. |
| `state.js` | 1 | Run state, title/end transitions, level reset. |
| `frog.js` | 1 | Frog physics, states, collisions, reset. |
| `platforms.js` | 1 | Surface records, safe intervals, last-safe logic. |
| `herons.js` | 1 | Sight lines, meters, warnings, dives. |
| `hazards.js` | 1 | Cattails, turtles, reed bundles, oil. |
| `water.js` | 1 | Shallow/deep water, current, safe edges. |
| `timeCycle.js` | 1 | Stage boundaries, waterline, surface events. |
| `moonflies.js` | 2 | Moonflies, reveal routes. |
| `tilting.js` | 2 | Tilting pads. |
| `camera.js` | 1 | Horizontal follow, clamp. |
| `render.js` | 1 | Draw world, effects, palette. |
| `audio.js` | 1 | Synth SFX/music. |
| `hud.js` | 1 | HTML HUD updates. |
| `segment01.js` | 1 | Fixed level content. |
| `debug.js` | 1 | Debug API. |

## 2.2 Global context

```js
// ctx is one mutable object. No hidden gameplay state outside ctx.
ctx = {
  mode: "title" | "playing" | "ended_success" | "ended_left" | "debug",
  seed: 0x20250101,
  rng: mulberry32(seed),

  time: {
    runTime: 0,
    stage: "dusk" | "deep_dusk" | "night",
    nextBoundary: 90,
    boundaryFlash: 0,
    nightContinuous: false,
    waterline: 400,
    glintAlpha: 0.55,
    oilAlpha: 0.35,
    fillRate: 38,
    drainRate: 55,
    eventQueue: [] // fixed, deterministic
  },

  input: {
    state: {
      left: false, right: false,
      down: false,
      hopShort: false, hopLong: false
    },
    pressed: { ... },
    released: { ... },
    buffer: { hopShort: 0, hopLong: 0 }
  },

  frog: {
    id: "frog",
    x: 80, y: 286, w: 18, h: 14,
    vx: 0, vy: 0,
    facing: 1,
    grounded: false,
    groundId: null,
    groundPoint: null,
    state: "grounded" | "air" | "crouch" | "shallow" | "carried" | "hit",
    hitTimer: 0,
    control: true,
    slideTimer: 0,
    slideDir: 0,
    waterMode: null, // "shallow" | "carried"
    waterTargetId: null,
    currentTimeout: 0,
    lastSafeLedgeId: null,
    lastSafePoint: null,
    path: [], // [{ledgeId, x, y, time}]
    visibleTo: [], // heron ids
    fullyHidden: false
  },

  camera: {
    x: 0, y: 0,
    targetX: 0,
    shake: 0
  },

  platforms: [
    {
      id: "entry_ledge",
      type: "entry",
      x: 40, y: 300, w: 120, h: 40,
      solid: true,
      occluder: false,
      category: "entry",
      topY: 300,
      submerged: false,
      sinking: false,
      rising: false,
      tiltAngle: 0,
      tiltMax: 0,
      safeIntervals: [],
      moss: true
    }
  ],

  surfaces: [
    {
      id: "surface_id",
      type: "lily" | "log" | "reed" | "stone" | "mushroom" | "turtle_closed",
      x: 0, y: 0, w: 0, h: 0,
      topY: 0,
      solid: true,
      occluder: false,
      category: "primary" | "low_shortcut" | "rising" | "hidden",
      submerged: false,
      sinking: false,
      rising: false,
      tiltAngle: 0,
      safeIntervals: [],
      revealed: true, // hidden stones: false until moonfly
      glow: 0
    }
  ],

  hazards: [
    {
      id: "cattail_1",
      type: "cattail" | "turtle" | "reed_bundle" | "oil",
      x: 0, y: 0, w: 0, h: 0,
      enabled: true,
      phase: "idle" | "closed" | "pre_snap" | "open" | "oil_active",
      phaseTime: 0,
      slideDir: 0,
      linkedSurfaceId: null
    }
  ],

  herons: [
    {
      id: "heron_1",
      eyeX: 2340, eyeY: 130,
      perchX: 2360, perchY: 120,
      length: 1500,
      angleMin: 20, angleMax: 65,
      period: 12, phaseOffset: 0,
      angle: 20,
      meter: 0,
      warning: false,
      warningEnd: 0,
      suppressed: false,
      headState: "scan" | "alert" | "caw" | "dive",
      headTimer: 0
    }
  ],

  moonflies: [
    {
      id: "moonfly_1",
      x: 0, y: 0,
      radius: 10,
      collected: false,
      revealsRouteId: "hidden_route_1"
    }
  ],

  hiddenRoutes: [
    {
      id: "hidden_route_1",
      revealed: false,
      surfaceIds: ["hidden_stone_1", "hidden_stone_2"],
      visibility: 0
    }
  ],

  water: {
    lineY: 400,
    zones: [
      { id: "shallow_left", x: 160, w: 220, bottomY: 455 },
      { id: "deep_main", x: 380, w: 1820, bottomY: 540 },
      { id: "shallow_right", x: 2200, w: 240, bottomY: 450 }
    ],
    ripples: [],
    currentActive: false
  },

  ui: {
    stageLabel: "DUSK",
    warningCountdown: 0,
    moonflyCount: 0,
    moonflyTotal: 6,
    message: ""
  },

  debug: {
    enabled: false,
    showSafeIntervals: false,
    showSightRays: false
  }
};
```

## 2.3 Module specifics

| Module | Required exports | Why |
| --- | --- | --- |
| `gameLoop.js` | `startLoop(ctx)`, `stopLoop()` | Fixed step and rendering. |
| `input.js` | `bindInput(ctx)`, `sampleInput(ctx, dt)`, `clearInputBuffers(ctx)` | Named inputs. |
| `state.js` | `startRun(ctx)`, `endRun(ctx, reason)`, `updateRunState(ctx)` | Run lifecycle. |
| `frog.js` | `updateFrog(ctx, dt)`, `applyFrogInput(ctx, dt)`, `resolveFrogCollisions(ctx)`, `hitFrog(ctx, reason)`, `resetFrog(ctx)` | Core movement and reset. |
| `platforms.js` | `updatePlatforms(ctx, dt)`, `computeSafeIntervals(ctx)`, `isPointSafe(ctx, x, y)`, `getLastSafeOrFallback(ctx)`, `isSurfaceSafe(ctx, surface)` | Safe ledges. |
| `herons.js` | `updateHerons(ctx, dt)`, `rayIntersectsFrog(ctx, heron)`, `isFrogFullyHidden(ctx)`, `startWarning(ctx, heron)`, `resolveWarning(ctx, heron)` | Stealth. |
| `hazards.js` | `updateHazards(ctx, dt)`, `hazardTouch(ctx, hazard)`, `oilSlide(ctx, dt)` | Hazards. |
| `water.js` | `enterWater(ctx)`, `updateWaterState(ctx, dt)`, `chooseSafeEdge(ctx)`, `depositEntry(ctx)` | Water/current. |
| `timeCycle.js` | `updateTimeCycle(ctx, dt)`, `applyBoundary(ctx, stage)`, `applyNightContinuous(ctx, dt)` | Time cycle. |
| `moonflies.js` | `updateMoonflies(ctx, dt)`, `collectMoonfly(ctx, id)`, `revealRoute(ctx, routeId)` | Tier 2. |
| `tilting.js` | `updateTilting(ctx, dt)`, `startTilt(ctx, surface, offset)`, `slideOffTilt(ctx, surface)` | Tier 2. |
| `camera.js` | `updateCamera(ctx, dt)` | View. |
| `render.js` | `render(ctx)` | Visual spec. |
| `audio.js` | `initAudio()`, `playSound(ctx, name)`, `setAmbience(ctx, stage)` | Audio. |
| `hud.js` | `updateHUD(ctx)` | HUD. |
| `segment01.js` | `buildSegment01(ctx)` | Fixed content. |
| `debug.js` | `debugFrog`, `debugPlatforms`, `debugHerons`, `debugHazards`, `debugWater`, `debugTime`, `debugMoonflies`, `debugTilting`, `debugInput` | Tests/debug. |

---

# 3. VISUAL SPEC

The look is a rain-swollen marsh crossing at dusk that darkens into night. The frog is a small pale-bellied silhouette against wet greens, teal water, and dark reeds. Safe ledges have faint pale moss; heron sight lines are pale glints across water and reeds; hazards are sharp and readable; moonflies are soft blue-white glows. At night, contrast lowers, but hazard timing cues, sight-line shadows, current ripples, and safe moss remain legible. The camera keeps the frog slightly left of center while moving right so herons, water depth, and upcoming hazards remain readable.

## Lighting and atmosphere

- Dusk: cool teal-blue sky, low warm horizon glow, water reflections visible, sight-line glints bright.
- Deep dusk: desaturated indigo, less sky detail, glints dimmer, oil patches less visible.
- Night: near-black blue, silhouettes dominate, moonfly glows and current ripples provide navigation.
- Stage boundary: 0.7 s light shift flash. No text needed, but HUD stage label updates.
- Continuous night: slow darkening, waterline rise, pad movement, reduced oil visibility.

## Space

- The pond segment is horizontal, left to right.
- Left edge: entry ledge on dry dark bank.
- Middle: lily pads, logs, reed ledges, stones, mushroom caps, hazards, water.
- Right edge: heron perches and old nursery pool.
- Water depth is readable: shallow zones show a lighter bottom silhouette; deep zones show dark water and ripple arrows.
- Safe ledges show pale moss only when currently safe. The last safe ledge has slightly brighter moss.

## Recipe table

| Layer | Draw | Color / alpha | Rule tie |
| --- | --- | --- | --- |
| Sky | vertical gradient | Dusk `#243447`→`#3a4a55`; Deep `#16202a`→`#24303a`; Night `#0a1016`→`#101a22` | Time cycle. |
| Water surface | line + shimmer | Base `#1f3a45`; highlights `#3f6f7a`; alpha 0.92 | Water depth. |
| Shallow bottom | visible pale band | `#2f515c`, alpha 0.55 | Depth ≤64. |
| Current ripples | moving arrows | `#7fb7c9`, alpha 0.35–0.7 | Deep water target. |
| Platforms | type silhouettes | Lily `#3f5a3a`, log `#2e2a24`, reed `#264a33`, stone `#2b3338`, mushroom `#3a2e36` | Crossing surfaces. |
| Safe moss | dotted pale edge | `#b9d8a8`, alpha 0.22 dusk, 0.18 deep, 0.14 night; last safe 0.30 | Safe ledges. |
| Cattail thorns | brown spike clusters | `#5a3a26`, outline `#8a5a35` | Fixed hazard. |
| Turtle jaws | closed pale platform / open teeth | Closed `#4f6b4a`, open hazard `#8a2f2f` | Timed hazard. |
| Reed bundles | thin sharp lines | `#4f3a2a`, highlight `#8a6a4a` | Landing hazard. |
| Oil patches | dark slick | `#10171f`, alpha 0.35 dusk, 0.25 deep, 0.15 night | Traction hazard. |
| Heron bodies | fixed silhouettes | `#151b20`, eye glint `#d9f2ff` | Watchers. |
| Sight-line glint | 3px line | `#dff7ff`, alpha 0.55 dusk, 0.35 deep, 0.18 night | Notice. |
| Sight-line shadow | blurred wider line | `#0b1116`, alpha 0.25/0.15/0.08 | Harder to read cue. |
| Warning pulse | glint flicker | white pulse 6Hz | Caw warning. |
| Frog | small rounded body, pale belly | Back `#5d7f5a`, belly `#dfe8d7`, eye `#10150f` | Player. |
| Moonfly | small glow | `#dff7ff`, glow alpha 0.65–0.95 | Optional collectible. |
| Hidden stone glow | faint outline | `#dff7ff`, alpha 0.45→0.9 by stage | Revealed route. |
| Hit/reset puff | dark ripple | `#0b1116`, alpha 0.45 | Reset. |

---

# 4. GAMEPLAY SPEC

The game is a one-segment side-view platformer. The player controls a small pale-bellied frog starting on a safe entry ledge at dusk. The goal is to reach the old nursery pool on the far side. The player walks, turns, ducks, short-hops, and long-hops across lily pads, logs, reed ledges, stones, and mushroom caps while avoiding fixed hazards and heron sight lines. The frog can fall into water: shallow water is a failed landing the frog can jump out of; deep water carries the frog weakly toward safe edges. Real-time stage boundaries change light, waterline, pad positions, and visibility. Optional moonflies reveal hidden stones and a harder secret crossing. The player can finish the game without collecting anything.

## Records and rosters

### Record shapes

```js
Frog {
  id, x, y, w, h, vx, vy, facing, grounded, groundId, groundPoint,
  state, hitTimer, control, slideTimer, slideDir,
  waterMode, waterTargetId, currentTimeout,
  lastSafeLedgeId, lastSafePoint, path, visibleTo, fullyHidden
}

Surface {
  id, type, x, y, w, h, topY,
  solid, occluder, category, submerged, sinking, rising,
  tiltAngle, safeIntervals, revealed, glow
}

Hazard {
  id, type, x, y, w, h, enabled,
  phase, phaseTime, slideDir, linkedSurfaceId
}

Heron {
  id, eyeX, eyeY, perchX, perchY,
  length, angleMin, angleMax, period, phaseOffset, angle,
  meter, warning, warningEnd, suppressed, headState, headTimer
}

Moonfly {
  id, x, y, radius, collected, revealsRouteId
}

HiddenRoute {
  id, revealed, surfaceIds, visibility
}

WaterZone {
  id, x, w, bottomY
}
```

### Roster counts

| Entity | Count | Type breakdown |
| --- | ---: | --- |
| Entry ledge | 1 | `entry_ledge` |
| Goal pool | 1 | `goal_pool` |
| Initial crossing surfaces | 28 | 10 lily pads, 4 half-sunk logs, 5 reed ledges, 6 wet stepping stones, 3 low mushroom caps |
| Primary safe surfaces | 16 | Top y ≤ 300, reachable from entry to goal |
| Low shortcut surfaces | 10 | Top y 330–390, sink later |
| Optional rising pads | 2 | Lily pads, initial top y 360, rise later |
| Hidden stones | 6 | Tier 2, initially non-solid/invisible |
| Herons | 2 | Fixed perches, scanning sight lines |
| Cattail thorns | 4 | Static hazard |
| Snapping turtle jaws | 2 | Timed hazard/platform |
| Sharp reed bundles | 3 | Landing hazard |
| Slick oil patches | 3 | Traction hazard |
| Moonflies | 6 | Optional collectibles |

### Level Segment 01 key content

| ID | Purpose | Key numbers |
| --- | --- | --- |
| `entry_ledge` | Run start | x 40–160, top y 300, always safe |
| `goal_pool` | Run end | x 2440–2560, top y 300, trigger when frog overlaps top interval |
| `heron_1` | Far-side watcher | eye x2340 y130, length1500, angle 20°–65°, period12s |
| `heron_2` | Far-side watcher | eye x2420 y180, length1400, angle 35°–80°, period15s, offset 0.35 |
| `shallow_left` | Left failed landing | x160 w220 bottomY455 |
| `deep_main` | Central current | x380 w1820 bottomY540 |
| `shallow_right` | Right failed landing | x2200 w240 bottomY450 |

Content constraints:

- Required primary route has 16 surfaces.
- Primary gaps are 45–96 px and require short or long hops.
- Every primary surface has at least one 20 px safe interval not occupied by hazards or permanent structures.
- Each heron line covers any required primary surface for at most 35% of its period.
- Each required primary surface has a continuous safe window of at least 1.2s per cycle.
- Entry ledge is never intersected by heron sight lines.
- Goal ledge is never submerged and never has hazard overlap.

## Frog Movement — Tier 1

### Inputs

| Named input | Keys | Effect |
| --- | --- | --- |
| `move_left` | ArrowLeft, A | Walk left, turn left when grounded. |
| `move_right` | ArrowRight, D | Walk right, turn right when grounded. |
| `duck` | ArrowDown, S | Crouch to 18×8, speed 45. Cannot hop while held. |
| `hop_short` | Space | Short-hop if grounded and not ducked. |
| `hop_long` | Shift+Space, X | Long-hop if grounded and not ducked. |

### Movement rules

- Grounded movement uses acceleration 900, friction 1200, max speed 150, duck max 45.
- Turning reverses facing immediately when input is opposite while grounded.
- Air control is 0. Horizontal velocity is locked at takeoff.
- No double jump.
- No coyote time.
- Jump buffer 0.10s.
- `hop_short`: vy = -261.
- `hop_long`: vy = -358.
- If both short and long are buffered, long takes priority.
- Landing occurs when bottom AABB crosses a solid surface top by ≤4px while vy ≥ 0.
- Landing on a safe surface updates `lastSafeLedgeId` and `lastSafePoint` to a safe interval point near the landing position.
- Landing on a hazard or unsafe surface triggers that surface’s rule.
- Ducking reduces hitbox height to 8. It does not move the frog unless movement input is held.
- Frog cannot jump while `state == carried`.
- Frog can jump while `state == shallow` using normal jump velocities.

### Committed-hop design

- A required gap must have no intermediate platform within jump reach unless it is optional.
- A bad takeoff cannot be rescued by air control, double jump, or coyote.
- The player must stop, aim, choose short or long, and commit.

## Platforms and Safe Ledges — Tier 1

### Surface rules

A surface is solid if `solid == true`. All provided crossing surfaces are solid except hidden stones before reveal.

A surface interval is safe only if:

1. Solid.
2. Dry: `topY < water.lineY`.
3. Not submerged by time cycle: `submerged == false`.
4. Not tilting: `tiltAngle <= 0.5°` (Tier 1 always true).
5. Not sinking.
6. Not overlapping hazard hitboxes.
7. Not inside an active heron sight line.
8. Not a rejected landing hazard interval.

Safe intervals are computed each frame and cached for the frame.

### Safe ledge marking

- Draw pale moss on all safe intervals.
- Draw brighter moss on `lastSafePoint`.
- If an interval becomes unsafe, moss fades within 0.15s.
- Surface becoming unsafe due to heron line does not move the frog.

### Last safe ledge

- Update `lastSafeLedgeId` and `lastSafePoint` only when the frog is grounded on a currently safe interval and not in `hit`.
- Append to `path` when occupying a new safe ledge.
- `path` stores the last 24 safe ledge points, oldest first.

### Reset algorithm

When reset is requested:

1. If `lastSafeLedgeId` exists and has a current safe interval, use the nearest safe point on it.
2. Else search `path` backward from most recent to oldest. Use first currently safe interval.
3. Else use `entry_ledge` safe point x=100 y=286.
4. Never place frog inside water, hazard, tilting pad, or active sight line.
5. Set `state=hit`, `hitTimer=0.45`, zero velocity, facing right.
6. After `hitTimer`, return to grounded state if the target is a ledge.

## Heron Stealth — Tier 1

### Heron placement

| Heron | Perch | Eye | Line length | Angle arc | Period |
| --- | --- | --- | ---: | --- | ---: |
| `heron_1` | 2360,120 | 2340,130 | 1500 | 20°–65° | 12s |
| `heron_2` | 2420,180 | 2420,180 | 1400 | 35°–80° | 15s, offset 0.35 |

Angles are measured from leftward horizontal, clockwise downward. `0°` points left, `90°` points down.

### Sight-line geometry

- Sight line is a ray segment from eye to endpoint.
- It intersects frog AABB if any part of the frog is on the line.
- Occluders block the ray if they intersect it before the frog.
- Frog is fully hidden if the ray is blocked or no intersection exists.
- Ducking alone does not hide unless fully occluded.

### Visibility meter

- Each heron has `meter` 0–100.
- Meter fills only when frog is moving inside that sight line.
- “Moving” means `abs(vx) > 5` or `vy != 0` or `state == air`.
- Idle inside line: meter neither fills nor drains.
- Fully hidden or outside line: meter drains at 55/s.
- Fill rate by stage: Dusk 38/s, Deep dusk 34/s, Night 30/s.
- If frog re-enters a line while meter is active, fill resumes.

### Warning and dive

- If meter reaches 100 and no warning is active, start warning.
- Warning duration 1.1s.
- During warning, frog may move but must be fully hidden before it ends.
- If fully hidden before end: abort, reset all active meters to 0.
- If not fully hidden at end: that heron dives, frog resets, all warnings/meters reset.
- If another heron reaches 100 while a warning is active, it is suppressed and does not start a second warning.
- If two reach 100 at the same fixed step, the one with shortest distance from frog center to line segment triggers; others reset.
- Before warning starts, if frog hides or leaves all lines, all notice meters drain to zero.
- After warning starts, only full hiding aborts.

### Visuals

- Dusk: pale glint alpha 0.55.
- Deep dusk: alpha 0.35.
- Night: alpha 0.18, shadow remains.
- Warning: line pulses white at 6Hz, heron head raises, caw sound.

## Hazards — Tier 1

General hazard hit:

- Frog enters `state=hit`, `hitTimer=0.45`.
- No life lost.
- Reset uses last safe ledge fallback.
- Current chain of hops through that hazard set is broken.
- Sound and brief dark ripple play.

### Cattail thorns

- Count 4.
- Static AABB hazards.
- Any overlap while `control` is active triggers hazard hit.
- Not affected while frog is in `carried`.

### Snapping turtle jaws

- Count 2.
- Closed phase 2.0s:
  - `linkedSurfaceId` is solid platform, can be stood on.
- Pre-snap phase 0.45s:
  - jaw edge glints, tick sound.
- Open phase 1.2s:
  - hazard AABB active.
  - touching causes hazard hit.
- If frog stands on closed jaw and it opens, hazard hit.

### Sharp reed bundles

- Count 3.
- Landing hazard rectangles.
- If frog lands with feet overlapping: reject landing, reset.
- If frog walks or stands with feet/hitbox overlapping: hazard hit.
- Not affected while carried.

### Slick oil patches

- Count 3.
- Fixed on surfaces.
- On contact while grounded:
  - `control=false`.
  - `slideDir` fixed per patch.
  - `slideSpeed=130`.
  - input ignored.
- Minimum forced slide time 0.35s.
- If slide reaches water: enter water/current.
- If slide leaves oil onto any ledge: hazard hit and reset.
- If slide overlaps hazard: hazard hit.
- Visual alpha decreases with night, collision unchanged.

## Water and Current — Tier 1

### Water zones

- `water.lineY` is current surface.
- Depth = `zone.bottomY - water.lineY`.
- If depth ≤64: shallow.
- If depth >64: deep.
- Rising water can turn shallow zones deep.

### Entering water

If frog bottom passes below waterline:

1. Find water zone under frog x.
2. If shallow:
   - `state=shallow`, `waterMode=shallow`.
   - Set y to bottom surface.
   - Frog can walk at 100 px/s and jump normally.
3. If deep:
   - `state=carried`, `waterMode=carried`.
   - Set y to `water.lineY - 7`.
   - Choose safe edge target.
   - Cannot jump.

### Deep water current

- Current speed 55 px/s toward target safe edge.
- Player can steer ±18 px/s with left/right.
- Frog cannot be affected by hazards or herons while carried.
- Target selection:
  - Choose nearest currently safe ledge edge.
  - If target becomes unsafe, reselect.
  - If no safe edge exists, deposit entry ledge.
- If frog reaches target edge within 8px, exit water onto ledge.
- If frog passes target without exiting, deposit entry ledge.
- Current timeout 10s, then deposit entry ledge.

### Shallow water

- Shallow water is a failed landing, not current.
- Frog lands on bottom.
- Frog can turn and jump out.
- No current force.
- Hazards still apply normally.

## Time Cycle — Tier 1

### Stages

| Stage | Run time | Waterline | Glint alpha | Oil alpha | Fill/drain |
| --- | ---: | ---: | ---: | ---: | --- |
| Dusk | 0–90s | 400 | 0.55 | 0.35 | 38/55 |
| Deep dusk | 90–180s | 385 | 0.35 | 0.25 | 34/55 |
| Night | 180–360s | 360→318 | 0.18 | 0.15 | 30/55 |
| Late night | 360–600s | →318 | 0.18 | 0.15 | 30/55 |
| After 600 | hold | 318 | 0.18 | 0.15 | 30/55 |

### Boundary events

At `t=90`, Deep dusk:

- Waterline 400→385.
- `low_shortcut_1..4` y += 18.
- `rising_lily_1` y -= 20.
- Light flash 0.7s.
- Sound `stage_shift`.

At `t=180`, Night:

- Waterline 385→360.
- `low_shortcut_5..8` y += 24.
- `rising_lily_2` y -= 60.
- Glint/oil alphas reduce.
- Light flash 0.7s.

Continuous night:

- From 180s to 600s, waterline decreases linearly 360→318 at 0.15 px/s.
- Every 30s after 180s:
  - one remaining `low_shortcut_*` y += 10 until submerged.
  - optional hidden route stones may rise or sink by 8px, never making them required.
- No stage loops.

### Surface changes and frog footing

- If surface top becomes below waterline, mark `submerged=true`, remove from safe list.
- If frog is grounded on that surface, immediately enter water at that spot.
- If a sinking surface moves while frog is on it, frog loses footing and enters water.
- If a rising surface moves while frog is on it, frog moves with it.
- If a surface becomes unsafe only due to heron sight line, frog is not moved.

## Moonflies and Hidden Routes — Tier 2

### Moonflies

- Count 6.
- Hidden in hollow reeds, under lifted pads, behind fallen logs, or risky detours.
- Pickup AABB circle radius 10.
- Collect by overlapping with frog hitbox.
- On collect:
  - `collected=true`.
  - `moonflyCount++`.
  - reveal one hidden route.
  - play `moonfly_collect`.
- Permanent for the run.

### Hidden stones and secret crossings

- 6 hidden stones total.
- Each belongs to one revealed route.
- Unrevealed: non-solid, invisible.
- Revealed: solid stepping stones with faint glow.
- Time cycle can sink, rise, block, or dim them, but never requires them.
- Normal primary route always remains available.
- Hidden route is harder, may avoid herons, and may pass through cattail thorns.
- Time cycle increases visibility:
  - Dusk revealed alpha 0.45.
  - Deep dusk 0.65.
  - Night 0.90.

## Tilting Lily Pads — Tier 2

### Count and placement

- 3 lily pads are tilting.
- They are optional or shortcut surfaces, not required for the primary route.

### Tilt rules

- `tiltAngle` is signed degrees. Positive tilts right.
- Max angle 28°.
- Safe only if `abs(tiltAngle) <= 0.5°`.
- Landing off-center:
  - offset = `(frogCenterX - padCenterX) / (padWidth/2)`.
  - if `abs(offset) > 0.15`, add `offset * 12°`.
- Standing still off-center:
  - tilt += offset * 6°/s.
- Moving across pad:
  - walking right adds 8°/s.
  - walking left subtracts 8°/s.
- Counterbalancing:
  - if tilt positive and walking left, additional -10°/s.
  - if tilt negative and walking right, additional +10°/s.
- If `abs(tiltAngle) >= 28°`:
  - frog slides off in tilt direction.
  - enter water using depth rule.
- If frog jumps before failure, no slide.
- When frog leaves, tilt relaxes 3°/s to zero.

## Progression and difficulty

| Stage | What changes | Player skill asked |
| --- | --- | --- |
| Dusk | Readable sight lines, low water, oil visible, low shortcuts safe. | Learn committed hops, stop/hide rhythm. |
| Deep dusk | Sight lines dim, water rises, some shortcuts sink, oil harder. | Re-evaluate safe ledges, use timing more. |
| Night | Sight lines hard to read, oil hard to see, water high, pads move. | Trust memory, use ripples/moss, take risks. |
| Optional moonfly route | Harder hidden stones, more hazards, fewer herons. | Detour and collect. |
| Optional tilting | Balance and counterbalance. | Manage continuous movement risk. |

Difficulty is never made mandatory by moonflies or tilting.

## Feel

The game should feel quiet, wet, and committed. The player hears each landing, sees moss only where safe, and understands that moving inside a glint is dangerous. Hops should be deliberate. When night comes, familiar safe cues dim but remain present. The frog is small and vulnerable, but never killed outright. The pleasure is in reading the marsh, stopping at the right time, and choosing whether to take a hidden route.

---

# 5. CHARACTERS

## Frog

Silhouette: small rounded body, short hind legs, pale belly visible from side, dark eye glint. Facing is left/right.

### Frog animations

| Animation | Trigger | Motion rule |
| --- | --- | --- |
| `idle` | grounded, no input | 2-frame breathe, 1.2s loop. |
| `walk` | grounded, move input | 4-frame cycle, 0.25s total, speed tied to vx. |
| `turn` | grounded, opposite input | 0.12s squash/stretch reverse, flips facing. |
| `duck` | down held | 0.08s flatten, height 8. |
| `shortHop` | short-hop | 0.1s crouch, tuck legs, follow physics. |
| `longHop` | long-hop | 0.14s stretch, follow physics. |
| `land` | landing | 0.12s squash, wet ripple particles. |
| `shallow` | shallow water | stand, small bubbles. |
| `waterCarry` | carried | paddle weakly, face target. |
| `hit` | hazard/heron reset | recoil, ripple, 0.45s. |
| `tiltSlide` | tilting failure | slide off pad, enter water. |

### Frog states used by gameplay

- `grounded`
- `air`
- `crouch`
- `shallow`
- `carried`
- `hit`

## Herons

Silhouette: fixed standing birds at far-side perches. Body does not walk. Only head and sight line move.

### Heron animations

| Animation | Trigger | Motion rule |
| --- | --- | --- |
| `scan` | default | Head rotates along arc. |
| `alert` | meter > 70 | Head pauses slightly, eye glint pulses. |
| `caw` | warning | Neck raises, 1.1s. |
| `dive` | failed warning | Quick lunge toward last frog position, then return. |

---

# 6. AUDIO

All audio is synthesized with Web Audio API. Music is ambient and does not affect gameplay.

| Name | Recipe | When it plays |
| --- | --- | --- |
| `ambient_dusk` | Low drone 70Hz sine + filtered noise wind, slow LFO | Playing, dusk. |
| `ambient_deep` | Add detuned 58Hz pad, reduce highs | Deep dusk. |
| `ambient_night` | Sparse high bell pulses, darker drone | Night. |
| `land_wet` | Noise burst, lowpass 600Hz, 80ms | Landing on safe/wet surface. |
| `land_soft` | Noise burst, lowpass 350Hz, 60ms | Landing on mossy safe edge. |
| `splash_shallow` | Filtered noise 1200Hz, 150ms, pitch down | Entering shallow water. |
| `splash_deep` | Noise highpass 800Hz + sine 120Hz, 300ms | Entering deep water. |
| `current_ripple` | Looping filtered brown noise, LFO 0.8Hz | While carried. |
| `heron_caw` | FM sawtooth 600→300Hz, 350ms | Warning start. |
| `heron_dive_swoosh` | Noise sweep 4kHz→500Hz, 250ms | Dive. |
| `notice_tick` | Square 420Hz, 30ms, every 0.35s | Meter >70. |
| `cattail_hit` | Square 220Hz, 60ms, noise crackle | Cattail hazard hit. |
| `turtle_pre_snap` | Click 150Hz, 30ms | 0.45s before open. |
| `turtle_snap` | Sawtooth 150→80Hz, 80ms | Turtle opens. |
| `reed_bundle_reject` | Highpass noise 3kHz, 60ms | Reed landing rejected. |
| `oil_slide` | Filtered brown noise, 130Hz lowpass loop | While sliding on oil. |
| `stage_shift` | Bell 220Hz + 330Hz, 1s | Stage boundary. |
| `moonfly_collect` | Sine 880→1320Hz, 120ms, sparkle | Collect moonfly. |
| `hidden_reveal` | Soft chime 660→990Hz, 700ms | Hidden route revealed. |
| `tilt_slide` | Filtered noise 600Hz, 150ms | Tilting pad failure. |
| `goal_pool` | Warm pad C-E-G arpeggio, 1.2s | Reach goal. |

---

# 7. UX

## HTML/CSS only screens

Screens are `<div>` elements controlled by CSS classes. Canvas remains the game view.

```text
#screen-title
#screen-playing-hud
#screen-ended-success
#screen-ended-left
#screen-debug
```

## State machine

```text
boot -> title
title -- start --> playing
playing -- reach goal --> ended_success
playing -- leave segment --> ended_left
ended_success -- restart --> title
ended_left -- restart --> title
any -- debug toggle --> debug / return
```

No pause state.

## HUD table

| HUD element | Record field | Visible when |
| --- | --- | --- |
| Stage label | `ctx.time.stage` | `mode == playing` |
| Warning countdown bar | max `heron.warningEnd - ctx.time.runTime` | Any `warning == true` |
| Warning text “HIDE” | active warning heron id | Any warning |
| Moonfly count | `ctx.ui.moonflyCount / ctx.ui.moonflyTotal` | Tier 2 enabled and `mode == playing` |
| Hidden route hint | `hiddenRoutes[].revealed` | Tier 2, after first reveal |
| Goal marker | `goal_pool` x position | Always while playing, drawn in world not DOM |

HUD must not show hidden stats, lives, health, or scores.

---

# 8. DEBUG API

```js
debugInput = {
  set(name, bool),
  tap(name),
  clear()
};

debugFrog = {
  teleport(x, y),
  setVelocity(vx, vy),
  setState(state),
  setLastSafe(ledgeId, x, y),
  clearPath()
};

debugPlatforms = {
  setSafe(id, bool),
  setSubmerged(id, bool),
  setMoss(id, bool),
  resetSafe()
};

debugHerons = {
  setAngle(id, deg),
  setMeter(id, value),
  setWarning(id, bool),
  forceDive(id),
  resetAll()
};

debugHazards = {
  setPhase(id, phase),
  setPhaseTime(id, seconds),
  trigger(id),
  resetAll()
};

debugWater = {
  setLine(y),
  setMode(mode),
  setTarget(id),
  depositEntry(),
  reset()
};

debugTime = {
  setRunTime(seconds),
  forceBoundary(stage),
  setNightContinuous(bool),
  reset()
};

debugMoonflies = {
  collect(id),
  revealRoute(id),
  reset()
};

debugTilting = {
  setAngle(id, deg),
  fail(id),
  reset()
};

debugLevel = {
  resetSegment01(),
  setCamera(x)
};
```

---

# 9. TESTS

## Tier 1 tests

| Test | Pass condition |
| --- | --- |
| Fixed loop determinism | Same inputs produce same state for 30s. |
| Input mapping | Named inputs trigger correct frog actions. |
| Walk/turn/duck | Speeds and hitboxes match spec. |
| Short/long hop | Heights/airtimes within ±2px/±0.02s. |
| No air control | Changing left/right in air does not change vx. |
| No double jump | Air input ignored. |
| Safe ledge update | Landing on safe interval updates last safe. |
| Unsafe due sight line | Moss disappears, frog not moved. |
| Reset last safe | Hazard hit returns to last safe. |
| Reset fallback | Last safe unsafe → search path → entry. |
| Cattail hit | Contact resets to safe. |
| Turtle closed stand | Frog can stand on closed jaw. |
| Turtle open hit | Open contact resets. |
| Reed landing reject | Feet overlap on landing resets. |
| Oil slide control loss | Input ignored while sliding. |
| Oil ledge reset | Slide onto ledge resets. |
| Oil water current | Slide into water enters carried. |
| Shallow water jump out | Frog can jump from shallow bottom. |
| Deep water current | Frog cannot jump, current moves to safe edge. |
| Current ignores hazards/herons | No meter/hazard trigger while carried. |
| Current no safe edge | Deposits entry. |
| Heron meter fill | Only moving inside line fills. |
| Heron meter stop | Idle inside line neither fills nor drains. |
| Heron drain | Hidden/outside drains. |
| Warning hide abort | Full hidden before end aborts. |
| Warning dive | Not hidden at end resets. |
| Multiple heron suppression | Second meter does not start second warning. |
| Same-instant tie | Closest line triggers. |
| Stage boundary | Waterline and alphas change at 90/180s. |
| Surface submerge | Frog on submerged surface enters water. |
| Rising pad | Frog on rising pad moves with it. |
| Goal | Reaching goal ends success. |
| Leave segment | x<0 or x>2560 ends left. |

## Tier 2 tests

| Test | Pass condition |
| --- | --- |
| Moonfly collect | Overlap reveals associated route. |
| Optional | Game finishable with zero moonflies. |
| Hidden stones | Unrevealed non-solid; revealed solid. |
| Route not mandatory | Primary route remains reachable. |
| Time visibility | Revealed stone alpha increases by stage. |
| Hidden route alteration | Time cycle can sink/rise hidden stones but not force use. |
| Tilt start | Off-center landing starts tilt. |
| Tilt safe loss | Any tilt >0.5° removes safe moss. |
| Tilt failure | ≥28° slides into water. |
| Tilt counterbalance | Opposite movement reduces angle. |
| Tilt jump escape | Jumping before failure avoids slide. |

---

# 10. BUILD ORDER

1. Scaffold HTML/CSS, canvas, fixed loop, debug context.
2. Implement input snapshot and named inputs.
3. Implement frog physics, short/long hops, duck, landing.
4. Implement static surface collision and camera.
5. Add Segment 01 primary surfaces, entry ledge, goal trigger.
6. Implement safe intervals, moss, last safe ledge, reset fallback.
7. Implement hazards: cattail, turtle, reed bundle, oil.
8. Implement water zones, shallow jump-out, deep current, safe edge selection.
9. Implement herons: sight lines, occlusion, meters, warning, dive.
10. Implement time cycle: stages, waterline, surface events, visual alphas.
11. Implement HUD and screen state machine.
12. Implement palette, animations, audio, ambient.
13. Playtest Tier 1 and tune gaps/meters/waterline.
14. Add moonflies, hidden stones, secret crossing.
15. Add tilting lily pads.
16. Add debug API and automated tests.
17. Final polish and sanity checks.

---

# 11. DEFINITION OF DONE

## Tier 1

A Tier 1 build is done when a player can start at dusk, cross the segment, and reach the goal using only core mechanics.

- [ ] Fixed 60Hz loop with deterministic input.
- [ ] Frog can walk, turn, duck, short-hop, long-hop, land.
- [ ] No air control, no double jump, no coyote.
- [ ] All 28 initial surfaces exist and are drawn in palette.
- [ ] Safe ledges show pale moss only when safe.
- [ ] Last safe ledge and fallback reset work.
- [ ] Entry ledge always safe.
- [ ] Goal pool ends run successfully.
- [ ] Leaving segment ends run.
- [ ] Heron sight lines, meters, warning, dive work.
- [ ] All 4 hazard types work.
- [ ] Shallow and deep water work.
- [ ] Current carries to safe edges and falls back to entry.
- [ ] Time cycle reaches dusk, deep dusk, night, continuous night.
- [ ] Stage boundaries change waterline, alphas, and surface positions.
- [ ] HUD shows stage and warning.
- [ ] All Tier 1 sounds play.
- [ ] Tests pass.

## Tier 2

A Tier 2 build is done when optional systems work without becoming required.

- [ ] 6 moonflies collect.
- [ ] Each reveals one hidden route.
- [ ] Hidden stones become solid only when revealed.
- [ ] Normal route remains always available.
- [ ] Hidden route visibility increases with time cycle.
- [ ] 3 tilting pads tilt, fail, counterbalance, and slide.
- [ ] Game is still finishable with zero moonflies and no tilting interactions.
- [ ] HUD shows moonfly count without hidden stats.
- [ ] Tier 2 tests pass.

## Final

- [ ] No extra systems added.
- [ ] No lives, combat, death, mandatory moonflies, or looping time cycle.
- [ ] All required content exists exactly as specified.
- [ ] Game feels readable at dusk and legible at night.
- [ ] Build order complete.

---

# A. SANITY

| Check | Result |
| --- | --- |
| Required headings present. | Valid. |
| Core mechanics are Tier 1. | Valid: Frog Movement, Platforms/Safe Ledges, Heron Stealth, Hazards, Water/Current, Time Cycle. |
| Supporting mechanics are Tier 2. | Valid: Moonflies/Hidden Routes, Tilting Lily Pads. |
| Extra mechanics: none. | Valid: no Tier 3 systems. |
| Left-out systems avoided. | Valid: no combat, lives, death, mandatory moonflies, time loop, drowning, block puzzles, feeding, creature collection. |
| Exact content parts used. | Valid: only provided platform, hazard, heron, water, moonfly, and time-cycle parts. |
| Numbers provided for every mechanic. | Valid: physics, stage timings, water, herons, hazards, moonflies, tilting. |
| Input named and drives gameplay. | Valid: `move_left`, `move_right`, `duck`, `hop_short`, `hop_long`. |
| Run structure concrete. | Valid: entry ledge, goal pool, leaving boundaries, run end. |
| Camera keeps relevant cues readable. | Valid: horizontal follow, clamped, visual recipe. |
| Time cycle runs once and ends with run. | Valid: no loop, stops on goal/leave. |
| Deep water is not instant death. | Valid: current carries to safe edge. |
| Shallow water is failed landing. | Valid: frog can jump out. |
| Safe ledges marked with pale moss. | Valid: visual recipe and safe interval rules. |
| Last safe ledge and fallback defined. | Valid: reset algorithm. |
| Entry ledge always safe. | Valid: top y 300, outside arcs, no hazards. |
| Heron meters fill only when moving inside line. | Valid: movement condition and stop rule. |
| Warning can be aborted by full hiding. | Valid: full hidden before end aborts. |
| Multiple heron suppression and tie-break defined. | Valid. |
| Hazards do not kill. | Valid: reset only. |
| Oil remains same collision but lower visibility. | Valid. |
| Time-cycle water rise does not drown. | Valid: depth/current rules apply. |
| Moonflies optional and never mandatory. | Valid. |
| Hidden route can be altered but never required. | Valid. |
| Tilting pads not required. | Valid: optional/shortcuts only. |
| Tier 1 includes art/audio/HUD. | Valid: visual/audio/HUD specified for Tier 1. |
| Tier conflict about tilting resolved. | Valid: actual tilting is Tier 2; Tier 1 only has safety flag. |
| Tests align with tiers. | Valid. |
| Definition of done aligns with tiers. | Valid. |