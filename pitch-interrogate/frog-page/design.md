# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Browser game: a platformer where you play as a frog | Whole document; #4 Gameplay Spec; #5 Characters |
| Side-scrolling 2D platformer view | #1.1 Units; #3 Visual Spec; #4.10 Camera |
| Real-time | #1.1 Units; #4.1 Input; #4.2 Crouch and committed leap |
| Play as a small frog | #4.1 Player and input; #5 Characters |
| Goal is the moonlit pond on the rooftops, where other frogs are already calling | #3 Visual Spec; #4.9 Crafted leg progression; #6 Audio |
| Move through rain barrels, gutters, garden edges, wet walls, branches, twigs, small physical supports | #4.4 Surfaces; #4.5 Breakable supports; #4.9 Level content |
| Frog does not run or fight | #4.1 Input; #4.7 Failure, dangle, and reset |
| Frog moves by crouching to coil and aim a committed leap | #4.2 Crouch and committed leap |
| Frog sticks to wet surfaces | #4.4 Stick, slide, and surface state |
| Frog hangs from twigs and swings with its tongue | #4.3 Tongue anchoring, hanging, swinging |
| Tongue is primarily for anchoring, hanging, swinging, catching grabbable supports | #4.3 Tongue anchoring, hanging, swinging |
| Tongue can disturb or pull small physical objects when that changes the scene physically | #4.8 Tongue physical disturbance |
| Game is built as crafted levels or legs of the journey | #4.9 Crafted leg progression and difficulty escalation |
| Each leg moves frog from low exposed place to higher safe perch or district boundary | #4.9 Crafted leg progression and difficulty escalation |
| Moonlit pond and calling frogs remain distant goal | #3 Visual Spec; #4.9 Crafted leg progression; #6 Audio |
| Difficulty comes from reading what can be caught, what will break, what is too slick, and what is watching the route | #4.4 Surfaces; #4.5 Breakable supports; #4.6 Watching dangers; #4.9 Difficulty escalation |
| Watching dangers: cats, herons, fish, sprinklers | #4.6 Watching dangers and attention; #4.9 Level content |
| Watching dangers are readable through attention or movement patterns | #4.6 Watching dangers and attention |
| Player avoids, waits, distracts through physical cause and effect, or takes a harder physical route | #4.6 Watching dangers; #4.8 Tongue physical disturbance; #4.9 Level design |
| A bad jump cannot be casually corrected in midair | #4.2 Crouch and committed leap; #4.10 Camera |
| Frog may slide, fall, or dangle for a beat before rethinking | #4.4 Stick, slide, and surface state; #4.7 Failure, dangle, and reset |
| Failure returns to last safe perch or leg start | #4.7 Failure, dangle, and reset; #4.9 Checkpoints |
| First day includes crouch, committed leap, stick, hang, swing, grabbable supports, wet/slippery/breakable surfaces, at least one watching danger | #0.3 Tier 1; #4.2–#4.7 |
| Camera keeps frog, next perch, supports, surfaces, and watching dangers in frame | #4.10 Camera |
| A run is one crafted leg | #4.9 Crafted leg progression; #7 UX state machine |
| Tone: small, slippery, alive in a wet world | #3 Visual Spec; #4.11 Feel; #6 Audio |
| Joy is finding clever physical route upward when obvious route would get you swallowed | #4.9 Level design; #4.11 Feel |
| Getting caught is embarrassment and reset, not combat | #4.7 Failure, dangle, and reset; #5 Characters |
| Look and sound: moonlit wet rooftops and garden edges, soft frog calls, water sounds, hazards readable through attention and movement | #3 Visual Spec; #6 Audio |
| Core mechanics exactly: crouch/committed leap, tongue anchoring/swinging, stick/slide/surface state, breakable supports, watching dangers/attention, failure/dangle/reset | #0.3 Tier 1; #4.2–#4.7 |
| Supporting mechanics exactly: tongue physical disturbance, crafted leg progression/difficulty escalation | #0.3 Tier 2; #4.8–#4.9 |
| Extra mechanics: none | #0.3; #4.12 Extra mechanics |
| Content exactly: small frog, moonlit pond, other frogs calling, rooftops, rain barrels, gutters, garden edges, wet walls, twigs, tongue, cats, herons, fish, sprinklers, branch, cork, strand of spider silk, smooth/dry surfaces, thin supports, sturdy edges/branches/anchors, safe perch, district boundary, obvious path, clever physical route | #4.9 Content roster; #4.2–#4.9 |
| Left out: running/fighting, tongue attacks, collectathon, hidden crouch stealth, free midair steering, combat when caught, fighting/commanding danger directly, new powers/modes, run ending at next pond | #0.2 Decisions; #4.1; #4.2; #4.6; #4.7; #4.9 |
| Builder must have concrete content, numbers, rules, input, run structure, visuals, audio, engineering contracts | Whole document |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| Game prompt | Final: platformer where you play as a frog. | Provided. |
| View | Final: side-scrolling 2D, camera keeps frog, next perch, supports, surfaces, watching dangers in frame. | Provided. |
| Time | Final: real-time. | Provided. |
| Run | Final: one run is one crafted leg. | Provided. |
| Tone | Final: small, slippery, alive in a wet world; getting caught is embarrassment and reset. | Provided. |
| Look and sound | Final: moonlit wet rooftops, soft frog calls, water sounds, readable hazards. | Provided. |
| Core mechanics | Final: exactly crouch/committed leap, tongue anchoring/swinging, stick/slide/surface state, breakable supports, watching dangers/attention, failure/dangle/reset. | Provided. |
| Supporting mechanics | Final: exactly tongue physical disturbance and crafted leg progression/difficulty escalation. | Provided. |
| Extra mechanics | Final: none. | Provided. |
| Content | Final: exactly listed content. | Provided. |
| Left out | Final: no running/fighting, no tongue attacks, no collectathon, no hidden crouch stealth, no free midair steering, no combat when caught, no new powers/modes, no run ending at next pond. | Provided. |
| Platforms | Final: browser, desktop/laptop keyboard + mouse required. Touch is out of scope. | Side-scrolling precision platforming with aiming is more reliable with mouse/keyboard. |
| Renderer | Final: single `<canvas>` for the game world; HTML/CSS only for screens and HUD. | Keeps visual control while satisfying HTML/CSS UI requirement. |
| Player | Final: unnamed small frog. No customization, no upgrades, no stats. | Keeps tone and scope. |
| Pickups | Final: zero pickups. No collectathon. | Explicitly left out. |
| Combat | Final: zero combat. Hazards cannot be attacked or commanded. | Explicitly left out. |
| Crouch | Final: crouch is visible coil and charge. It is not stealth. | Provided. |
| Stillness | Final: stillness means frog velocity and input-driven motion are near zero. Crouch held does not count as stealth. | Prevents hidden crouch stealth. |
| Input: aim | Final: mouse cursor sets aim vector for leap and tongue. | Precise committed leaps and tongue anchoring require 2D aim. |
| Input: crouch | Final: hold `Space` to crouch/charge; release to leap. | One clear verb for crouch/committed leap. |
| Input: tongue | Final: press `E` to fire tongue at mouse cursor; press `E` again to detach. | Clear named verb for anchoring/hanging/swinging/disturbing. |
| Input: stick | Final: hold `S` or `Down` while touching a wet surface to grip. Smooth/dry surfaces ignore grip input. | Gives stick a named input and makes surface reading active. |
| Input: swing | Final: `A/D` or `Left/Right` apply swing torque only while hanging. On grounded surfaces they rotate facing only; they do not run. | Prevents running while allowing pendulum control. |
| Midair control | Final: no air control. No horizontal steering after takeoff. | Provided. |
| Physics scale | Final: 1 unit = 1 pixel. Canvas 960×540. World coordinates x right, y down. | Standard 2D browser platforming. |
| Fixed timestep | Final: 60 Hz fixed update; render interpolation allowed. | Deterministic tests and stable physics. |
| Frog size | Final: hitbox 14×12 px. Visual body 18×14 px. Crouch visual 18×10 px. | Small frog, fair collisions. |
| Gravity | Final: 1600 px/s². | Gives readable jumps and dangerous falls. |
| Terminal velocity | Final: 950 px/s. | Prevents absurd falls. |
| Crouch charge | Final: min 0.10 s, max 0.45 s. Release before min cancels without jump. | Committed but responsive. |
| Leap speed | Final: 300 + 480 × chargeNorm, cap 780 px/s. | Max height ≈190 px; enough for crafted chains. |
| Aim angle | Final: cursor vector normalized. If cursor within 80 px of frog center, use facing horizontal. | Avoids zero-vector ambiguity. |
| Tongue length | Final: 260 px max. Attach radius 12 px. Cooldown 0.18 s. | Reachable anchors without making levels trivial. |
| Hang/swing constraint | Final: while attached, distance to anchor constrained to tongue length. `A/D` torque 520 px/s², damping 0.985. | Pendulum feel without free flight. |
| Stick conditions | Final: wet surface + holding `S`/`Down` + normal impact ≤820 px/s + tangential speed ≤500 px/s => stuck. | Makes grip readable and skillful. |
| Slide conditions | Final: wet not gripping: tangential acceleration 720 px/s². Smooth/dry: tangential acceleration 1360 px/s². | Smooth/dry are too slick; wet walls can be dangerous if not gripped. |
| Breakable supports | Final: strain 0..1. Passive hang +0.35/s. Swing max +0.45/s. Impact add up to 0.5. Break at strain ≥1.0. | Readable failure through cracks and snap. |
| Safe perch | Final: `isSafe=true` perches are checkpoints and visually moonlit. Ordinary perches can be stood on but are not checkpoints. | Supports failure return rules. |
| Failure reset | Final: reset frog to last safe perch; if none, leg start. Reset all hazards, breakables, and disturbables to initial state. | Guarantees solvability and clarity. |
| Dangle | Final: if a fall is stopped by tongue on a grabbable support, frog hangs/dangles until player detaches or support breaks. | Provided. |
| Watching dangers | Final: cats, herons, fish, sprinklers are hazards. They use attention or movement patterns, not HP or combat. | Provided. |
| Attention visual | Final: hazards show visible attention cones, eye states, water ripples, sprinkler warning. | Hazards must be readable. |
| Cover | Final: solid world geometry blocks hazard line-of-sight. No separate stealth system. | Uses existing level objects. |
| Disturbable objects | Final: branch, cork, strand of spider silk. They only change hazard attention, line-of-sight, or timers through physical cause/effect. | Provided supporting mechanic. |
| Legs | Final: three shipped legs: Rain Barrel Yard, Gutter Ridge, Garden Edge District. | Enough to demonstrate crafted progression without adding new systems. |
| Tier 1 | Final: one complete leg with all core mechanics and one cat. | First day requirement. |
| Tier 2 | Final: adds physical disturbance, two more legs, heron, fish, sprinkler, branch, cork, spider silk. | Supporting mechanics only after working core. |
| Tier 3 | Final: none. | Extra mechanics none. |
| Game completion | Final: after Leg 3 goal, show moonlit pond and calling frogs as epilogue, not another run. | Pond remains distant goal. |
| HUD | Final: minimal HUD only for charge, grip, tongue target, breakable strain, leg state. No combat/collect HUD. | Keeps focus. |
| Debug API | Final: one function per gameplay system plus input functions. | Required by brief. |

## 0.3 Tiers

| Tier | Segment | Description |
| --- | --- | --- |
| Tier 1 | Core playable leg | A player can start Leg 1, crouch/aim/leap, stick to wet walls, slide on slick surfaces, tongue-attach to sturdy anchors and breakable twigs, hang/swing, avoid or be caught by one cat, fail to last safe perch or leg start, and reach the Leg 1 safe perch/district boundary. Includes final art style, palette, animation, audio, HUD, camera. |
| Tier 2 | Supporting content and cause/effect | Adds physical disturbance: branch, cork, strand of spider silk. Adds Leg 2 and Leg 3. Adds heron, fish, sprinkler. Adds crafted leg progression and difficulty escalation. Adds district boundaries and game complete epilogue. |
| Tier 3 | Extra mechanics | None. Do not add systems. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Item | Value | Notes |
| --- | --- | --- |
| Canvas logical size | 960 × 540 | CSS may scale; game logic uses logical px. |
| World unit | 1 px | All positions, sizes, speeds are px or px/s. |
| Axis | x right, y down | Gravity positive y. Jump velocities have negative y. |
| Angle | radians, 0 right, positive clockwise | For rendering and aim. |
| Fixed timestep | 1/60 s | Update in 16.666... ms steps. |
| Max substeps per frame | 4 | Prevent physics tunneling. |
| Render interpolation | allowed | Use previous and current state for smooth visuals. |
| Frog hitbox | 14 × 12 | Centered on frog position. |
| Frog visual body | 18 × 14 | Crouch visual 18 × 10. |
| Collision method | swept AABB for frog; circle/line for tongue anchors | Supports must be simple. |
| Coordinate origin | top-left of world | World bounds per leg. |
| Time | seconds | All rule numbers use seconds. |
| Speed | px/s | All velocities. |
| Acceleration | px/s² | Gravity, slide, swing torque. |
| Strain | 0..1 | Breakable support stress. |
| Attention | 0..1 | Hazard suspicion. |

## 1.2 Important conventions

| Convention | Rule |
| --- | --- |
| Deterministic simulation | Use one seeded RNG per leg. Never call `Math.random()` in gameplay logic. Seed is `legIndex * 1000 + attemptNumber`. |
| Fixed update | All gameplay rules run only inside `step(dt)` with fixed `dt = 1/60`. |
| No free midair steering | After leaving a surface or release, `A/D` do not alter frog velocity unless tongue is attached and state is hanging/swinging. |
| No hidden stealth | Visibility is based on actual velocity, line-of-sight, and hazard patterns. Crouch is visible coil only. |
| No combat | Hazards have no HP, no damage, no player attack. Capture causes reset. |
| No collectibles | No pickups, no score, no currency. |
| No powers | No permanent upgrades, no separate modes. |
| Safe perch is checkpoint | Only entities with `isSafe=true` are checkpoints. |
| Reset restores world | On failure, all hazards, breakable supports, and disturbables return to initial state. Frog is placed at last safe perch or leg start. |
| Readable hazards | Every hazard must expose visual state: neutral, suspicious, locked, acting, cooldown. |
| Surface state is visible | Wet, smooth/dry, sturdy, thin, and safe surfaces must be visually distinct. |
| Input state is pure | Input module only records raw input; gameplay systems consume it. |
| Debug functions are read-only | Debug API may read state but must not mutate gameplay except explicit debug helpers. |
| Tests use deterministic seeds | Tests must set seed and fixed step manually. |

# 2. CONTRACTS

## 2.1 Module layout

```text
index.html
styles.css
js/
  main.js
  loop.js
  input.js
  context.js
  camera.js
  level.js
  frog.js
  tongue.js
  surfaces.js
  breakables.js
  hazards.js
  disturbables.js
  failure.js
  progression.js
  render.js
  audio.js
  hud.js
  screens.js
  debug.js
  tests.js
```

| Module | Responsibility |
| --- | --- |
| `main.js` | Boot, start loop, load level, bind screens. |
| `loop.js` | Fixed timestep loop, render interpolation. |
| `input.js` | Keyboard/mouse state, aim vector, action edges. |
| `context.js` | Global records and state transitions. |
| `camera.js` | Side-scroll camera constraints. |
| `level.js` | Level data, entity registry, bounds, checkpoints, goals. |
| `frog.js` | Frog state machine, physics, crouch, leap, stick, slide, hang, caught, reset. |
| `tongue.js` | Tongue fire, attach, detach, constraint, swing torque, disturbance. |
| `surfaces.js` | Surface collision, wet/smooth state, grip/slide resolution. |
| `breakables.js` | Support strain, cracking, snapping. |
| `hazards.js` | Cat, heron, fish, sprinkler attention and movement patterns. |
| `disturbables.js` | Branch, cork, spider silk physical cause/effect. |
| `failure.js` | Dangle, fall, caught, checkpoint restore, reset. |
| `progression.js` | Leg start, goal reached, leg progression, game complete. |
| `render.js` | Canvas drawing, palette, world effects, hazard cues. |
| `audio.js` | Synthesized sound effects and ambient layers. |
| `hud.js` | HUD elements bound to context fields. |
| `screens.js` | HTML/CSS screen state machine. |
| `debug.js` | Debug API. |
| `tests.js` | Automated tests. |

## 2.2 Global context

All gameplay records live in one global context. These are the required fields.

```js
const GameContext = {
  mode: "boot", // boot,title,legIntro,playing,caught,legComplete,gameComplete,debug
  seed: 0,
  legIndex: 0,
  attemptNumber: 0,
  time: 0,
  input: InputState,
  camera: CameraState,
  level: LevelState,
  frog: FrogState,
  tongue: TongueState,
  surfaces: SurfaceIndex,
  breakables: BreakableIndex,
  hazards: HazardIndex,
  disturbables: DisturbableIndex,
  failure: FailureState,
  progression: ProgressionState,
  hud: HUDState,
  audio: AudioState
};
```

```js
InputState = {
  keys: {
    space: false,
    e: false,
    s: false,
    down: false,
    a: false,
    d: false,
    left: false,
    right: false,
    enter: false
  },
  edges: {
    spaceDown: false,
    spaceUp: false,
    eDown: false,
    sDown: false,
    sUp: false,
    aDown: false,
    dDown: false,
    enterDown: false
  },
  mouse: {
    x: 0,
    y: 0,
    insideCanvas: false
  },
  aim: {
    x: 0,
    y: 0,
    angle: 0,
    distance: 0,
    valid: false
  }
};
```

```js
CameraState = {
  x: 0,
  y: 0,
  targetX: 0,
  targetY: 0,
  deadzoneX: 180,
  deadzoneY: 120,
  lerp: 0.12,
  bounds: { minX: 0, minY: 0, maxX: 0, maxY: 0 }
};
```

```js
LevelState = {
  id: "",
  name: "",
  bounds: { width: 0, height: 0 },
  entities: [], // Entity[]
  hazards: [], // Hazard[]
  disturbables: [], // Disturbable[]
  checkpoints: [], // Entity id[]
  goalId: "",
  startFrog: { x: 0, y: 0, facing: 1 },
  moonPond: { x: 0, y: 0, visible: false },
  ambient: {
    rain: false,
    water: false,
    frogCalls: false
  }
};
```

```js
Entity = {
  id: "",
  type: "perch|wetWall|smoothWall|sturdyAnchor|twig|thinSupport|safePerch|goalPerch",
  x: 0,
  y: 0,
  w: 0,
  h: 0,
  shape: "rect|circle|segment",
  radius: 0,
  segment: { x1: 0, y1: 0, x2: 0, y2: 0 },
  surface: "wet|smooth|dry|none",
  grip: false,
  isSafe: false,
  isGoal: false,
  isStart: false,
  isObstacle: false,
  blocksLineOfSight: true,
  breakable: false,
  maxStrain: 0,
  strain: 0,
  broken: false,
  grabbable: false,
  sturdy: false,
  tags: []
};
```

```js
FrogState = {
  x: 0,
  y: 0,
  vx: 0,
  vy: 0,
  facing: 1,
  angle: 0,
  state: "grounded", // grounded,crouching,air,wallContact,sliding,stuck,hanging,swinging,dangle,caught,reset
  grounded: false,
  crouching: false,
  crouchStart: 0,
  charge: 0,
  chargeNorm: 0,
  aim: { x: 0, y: 0, angle: 0 },
  lastGroundNormal: { x: 0, y: 0 },
  surfaceId: null,
  gripHeld: false,
  stuck: false,
  slideTimer: 0,
  tongueId: null,
  dangleTimer: 0,
  caughtTimer: 0,
  resetTimer: 0,
  lastSafeId: null,
  startId: null,
  alive: true,
  canLeap: false,
  canTongue: true,
  canGrip: false,
  canSwing: false
};
```

```js
TongueState = {
  id: "",
  active: false,
  attached: false,
  anchorId: null,
  targetX: 0,
  targetY: 0,
  length: 0,
  maxLength: 260,
  cooldown: 0,
  cooldownMax: 0.18,
  attachRadius: 12,
  strain: 0,
  disturbanceTargetId: null,
  state: "retracted", // retracted,extending,attached,detaching,broken
  extendTimer: 0,
  extendSpeed: 1800,
  detachTimer: 0
};
```

```js
Hazard = {
  id: "",
  type: "cat|heron|fish|sprinkler",
  x: 0,
  y: 0,
  facing: 1,
  state: "neutral", // neutral,suspicious,locked,acting,cooldown,disabled
  attention: 0,
  maxAttention: 1.0,
  lockTimer: 0,
  actionTimer: 0,
  cooldown: 0,
  patrol: {
    a: { x: 0, y: 0 },
    b: { x: 0, y: 0 },
    speed: 0,
    active: true
  },
  lineOfSight: {
    range: 0,
    angle: 0,
    blocked: false
  },
  attentionCone: {
    range: 0,
    angle: 0
  },
  capture: {
    w: 0,
    h: 0,
    active: false
  },
  disabledUntil: 0,
  divertedUntil: 0,
  initial: {}
};
```

```js
Disturbable = {
  id: "",
  type: "branch|cork|spiderSilk",
  x: 0,
  y: 0,
  grabbable: true,
  state: "untouched", // untouched,pulled,active,spent
  effectTargetId: "",
  effectStart: 0,
  effectDuration: 0,
  initial: {}
};
```

```js
FailureState = {
  lastSafeId: null,
  startId: null,
  caughtBy: null,
  dangleUntil: 0,
  resetCount: 0
};
```

```js
ProgressionState = {
  legIndex: 0,
  legComplete: false,
  goalReached: false,
  allLegsComplete: false,
  moonPondRevealed: false,
  frogCalls: false
};
```

```js
HUDState = {
  charge: 0,
  grip: false,
  tongueTarget: null,
  breakableStrain: null,
  legName: "",
  safePerchFound: false,
  attentionWarning: false
};
```

```js
AudioState = {
  enabled: true,
  ambient: {
    rain: false,
    water: false,
    frogCalls: false
  },
  lastSound: {
    name: "",
    time: 0
  }
};
```

## 2.3 Module specifics

### `input.js`

```js
Input.getAim(frog) -> { x, y, angle, distance, valid }
Input.consumeEdge(name) -> boolean
Input.isDown(name) -> boolean
Input.setAimForTest(x, y) -> void
```

Required fields: `InputState`.

### `frog.js`

```js
Frog.update(input, level, tongue, dt) -> void
Frog.tryLeap(frog, input) -> void
Frog.canStick(frog, surface) -> boolean
Frog.applySlide(frog, surface, dt) -> void
Frog.enterCaught(frog, hazardId) -> void
Frog.resetTo(frog, entityId) -> void
Frog.getState() -> FrogState
```

### `tongue.js`

```js
Tongue.fire(input, frog, level) -> void
Tongue.attach(anchorId) -> void
Tongue.detach(reason) -> void
Tongue.applySwing(input, frog, dt) -> void
Tongue.applyConstraint(frog, dt) -> void
Tongue.tryDisturb(level, frog, input) -> void
Tongue.getState() -> TongueState
```

### `surfaces.js`

```js
Surfaces.getAt(x, y) -> Entity|null
Surfaces.isWet(entity) -> boolean
Surfaces.isSmooth(entity) -> boolean
Surfaces.canStick(frog, entity) -> boolean
Surfaces.resolveCollision(frog, entity, dt) -> void
Surfaces.getState() -> SurfaceIndex
```

### `breakables.js`

```js
Breakables.addStrain(entity, amount) -> void
Breakables.addImpactStrain(entity, impactSpeed) -> void
Breakables.step(dt) -> void
Breakables.isBroken(entityId) -> boolean
Breakables.reset(entityId) -> void
Breakables.getState() -> BreakableIndex
```

### `hazards.js`

```js
Hazards.update(frog, level, dt) -> void
Hazards.canSee(hazard, frog) -> boolean
Hazards.addAttention(hazard, amount) -> void
Hazards.decayAttention(hazard, amount, dt) -> void
Hazards.lock(hazard) -> void
Hazards.act(hazard, frog) -> void
Hazards.disable(hazard, seconds) -> void
Hazards.divert(hazard, seconds) -> void
Hazards.getState() -> HazardIndex
```

### `disturbables.js`

```js
Disturbables.tryGrab(frog, tongue, level) -> boolean
Disturbables.pull(disturbable, direction) -> void
Disturbables.applyEffect(disturbable, hazards, frog, level) -> void
Disturbables.step(dt) -> void
Disturbables.getState() -> DisturbableIndex
```

### `failure.js`

```js
Failure.check(frog, level, hazards, dt) -> void
Failure.beginDangle(frog, seconds) -> void
Failure.beginCaught(frog, hazardId) -> void
Failure.beginFallReset(frog) -> void
Failure.restoreCheckpoint(frog, level) -> void
Failure.resetWorld(level) -> void
Failure.getState() -> FailureState
```

### `progression.js`

```js
Progression.startLeg(index) -> void
Progression.checkGoal(frog, level) -> boolean
Progression.completeLeg() -> void
Progression.nextLeg() -> void
Progression.completeGame() -> void
Progression.getState() -> ProgressionState
```

### `camera.js`

```js
Camera.focusFrog(frog, level) -> void
Camera.update(dt) -> void
Camera.clampToLevel(level) -> void
Camera.getState() -> CameraState
```

### `level.js`

```js
Level.load(legIndex, seed) -> LevelState
Level.getGoal() -> Entity
Level.getStart() -> Entity
Level.getSafePerches() -> Entity[]
Level.getSupports() -> Entity[]
Level.resetDynamic() -> void
Level.getState() -> LevelState
```

### `render.js`

```js
Render.draw(ctx, context) -> void
Render.drawFrog(ctx, frog, camera) -> void
Render.drawLevel(ctx, level, camera) -> void
Render.drawTongue(ctx, tongue, frog, camera) -> void
Render.drawHazards(ctx, hazards, camera) -> void
Render.drawEffects(ctx, context, camera) -> void
```

### `audio.js`

```js
Audio.play(name) -> void
Audio.ambient.set(kind, enabled) -> void
Audio.getState() -> AudioState
```

### `hud.js`

```js
HUD.update(context) -> void
HUD.setCharge(value) -> void
HUD.setGrip(active) -> void
HUD.setTongueTarget(entityId) -> void
HUD.setBreakableStrain(entityId, value) -> void
HUD.setLegName(name) -> void
```

### `screens.js`

```js
Screens.goto(mode) -> void
Screens.showTitle() -> void
Screens.showLegIntro(legIndex) -> void
Screens.showPlaying() -> void
Screens.showCaught(reason) -> void
Screens.showLegComplete(legIndex) -> void
Screens.showGameComplete() -> void
```

# 3. VISUAL SPEC

The look is moonlit wet rooftops and garden edges: dark blue-black sky, silver puddle shine, mossy green perches, rusted rain barrels, and slim wet highlights. The frog is a small, readable silhouette with bright eyes and a subtle wet rim. Surfaces tell the truth through material: wet walls shine, smooth/dry surfaces are dull and pale, sturdy anchors have clear metal or rope glints, and thin twigs have visible cracks and flex. Hazards are readable through posture and attention cues, not through combat UI. The moonlit pond is always a distant visual and audio goal, never a collectathon.

### Lighting and atmosphere

| Element | Rule |
| --- | --- |
| Global light | Moonlight from upper right. Strong rim on wet surfaces. |
| Sky | Very dark navy with soft moon halo. |
| Rain | Optional thin diagonal streaks only in Leg 1 and Leg 2; Leg 3 no rain. |
| Wet shine | Wet surfaces have 2px cyan-white highlight along top and edge. |
| Smooth/dry shine | Smooth surfaces have flat gray body and weak specular, no cyan highlight. |
| Safe perch | Soft moon ring, 4px, color `#c8f2ff`, pulsing 1.2s. |
| Goal perch | Larger moon ring, brighter, calls sound when approached. |
| Breakable strain | Cracks appear at strain 0.35, 0.65, 0.90. Color shifts green to amber to red. |
| Attention cue | Cat eye slits, heron head orientation, fish ripple, sprinkler warning glow. |
| Cover | Solid objects block line-of-sight; draw shadowed occlusion band behind cover. |

### Space

| Space | Visual language |
| --- | --- |
| Low exposed start | Open roof edge, dark sky, no moon ring. |
| Rain barrels | Cylindrical barrels, ribbed tops, water shine. |
| Gutters | Long metal channels, dripping edges. |
| Garden edges | Wooden beams, moss, leaves, planters. |
| Wet walls | Shiny cyan-edged surfaces, water trails. |
| Smooth/dry walls | Pale gray, matte, dry crack texture. |
| Sturdy anchors | Metal hooks, rope ends, gutter brackets, bright glint. |
| Thin supports | Brown twigs, small joints, visible cracks when stressed. |
| Branch | Leafy branch with hanging motion. |
| Cork | Red-brown cork in barrel hole. |
| Spider silk | Thin white line with subtle vibration. |
| Moonlit pond | Distant background only, shimmering surface, frog silhouettes. |

### Recipe table

| Visual target | Recipe |
| --- | --- |
| Palette | `#08111c` sky, `#13233a` roof, `#1d4f4b` moss, `#6f4d2a` wood, `#8f9ba8` metal, `#d8f6ff` moon highlight, `#7ef9ff` wet shine, `#f2c94c` warning, `#e74c3c` danger, `#b7f7c0` safe. |
| Frog | Body `#2e7d5b`, belly `#d9f2d2`, eyes `#f7f7d0`, pupil vertical slit, wet rim `#8ff6ff`. |
| Cat | Black silhouette, two amber eyes, tail readable, attention cone `rgba(242,201,76,0.18)`. |
| Heron | Tall gray silhouette, long neck, dark beak, eye `#fff`, strike line `#fff`. |
| Fish | Dark shape under water, white eye, ripple circles. |
| Sprinkler | Metal head, water arc, warning glow. |
| Camera | Always frame frog plus next reachable perch and nearest hazard. |
| Screen shake | Only on snap, splash, or caught; max 3px, 0.18s. |

# 4. GAMEPLAY SPEC

The game is a quiet, precise platformer. The player is a small frog trying to climb from low wet rooftops toward a moonlit pond that remains visible but distant. A run is one crafted leg: start low and exposed, read supports, wetness, breakage, and watching dangers, then use crouch/leap, tongue anchoring, hanging, swinging, and stick/slide to reach a higher safe perch or district boundary. There is no combat, no running, no collectathon, and no free midair steering. Failure is embarrassment and reset, not punishment by damage.

## Records and rosters

### Roster: player

| Item | Count | Notes |
| --- | ---: | --- |
| Small frog | 1 | The only player-controlled entity. |

### Roster: hazards

| Hazard | Tier | Leg 1 | Leg 2 | Leg 3 | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Cat | 1 | 1 | 1 | 0 | 2 |
| Heron | 2 | 0 | 1 | 0 | 1 |
| Fish | 2 | 0 | 0 | 1 | 1 |
| Sprinkler | 2 | 0 | 0 | 1 | 1 |

### Roster: traps and hazards

| Trap type | Count |
| --- | ---: |
| Cat | 2 |
| Heron | 1 |
| Fish | 1 |
| Sprinkler | 1 |

### Roster: pickups

| Pickup | Count |
| --- | ---: |
| None | 0 |

### Roster: physical supports and surfaces

| Object | Leg 1 | Leg 2 | Leg 3 | Total |
| --- | ---: | ---: | ---: | ---: |
| Start perch | 1 | 1 | 1 | 3 |
| Safe perch checkpoint | 1 | 1 | 1 | 3 |
| Goal safe perch / district boundary | 1 | 1 | 1 | 3 |
| Ordinary perch | 2 | 3 | 4 | 9 |
| Wet wall | 2 | 2 | 2 | 6 |
| Smooth/dry wall | 1 | 2 | 2 | 5 |
| Sturdy anchor | 3 | 4 | 5 | 12 |
| Breakable twig | 2 | 4 | 5 | 11 |
| Thin support | 2 | 4 | 5 | 11 |
| Branch | 0 | 1 | 0 | 1 |
| Cork | 0 | 0 | 1 | 1 |
| Strand of spider silk | 0 | 0 | 1 | 1 |

### Roster: world goal

| Item | Count | Notes |
| --- | ---: | --- |
| Moonlit pond | 1 | Distant background goal. |
| Other frogs calling | 1 ambient group | Audio and background silhouettes. |

## 4.1 Player and input

**Tier:** 1

| Input | State | Effect |
| --- | --- | --- |
| Mouse move | aim | Sets frog aim vector for crouch and tongue. |
| `Space` hold | crouching | Coils frog and charges leap. |
| `Space` release | air | If charge ≥0.10s, executes committed leap. If <0.10s, cancels crouch. |
| `E` press | tongue | Fires tongue toward aim. If attached, detaches. |
| `S` or `Down` hold | wallContact/stuck | Attempts grip on touched surface. |
| `A/D` or `Left/Right` | swinging | Applies swing torque while hanging. |
| `A/D` or `Left/Right` | grounded | Rotates facing only; no run. |
| `Enter` | UI | Confirms screen transitions. |

Rules:

1. The frog has no locomotion speed. It cannot walk or run.
2. The frog has no air control.
3. The frog can only change motion through:
   - committed leap,
   - stick/slide,
   - tongue attach,
   - swing torque,
   - hazard impulse,
   - reset.
4. Mouse aim is not considered player movement for hazard detection.
5. Facing follows aim when aim is valid; otherwise `A/D` set facing.
6. The frog’s hitbox is 14×12. Collision center is frog position.

## 4.2 Crouch and committed leap

**Tier:** 1

Rules:

1. Hold `Space` to crouch.
2. Crouch visual: frog compresses to 18×10.
3. Charge starts at 0.
4. Minimum charge time: 0.10s.
5. Maximum charge time: 0.45s.
6. `chargeNorm = clamp((heldTime - 0.10) / (0.45 - 0.10), 0, 1)`.
7. Release before 0.10s: no leap, exit crouch.
8. On release, compute aim vector:
   - If mouse distance ≥80 px, aim = normalized mouse vector.
   - Else aim = facing horizontal.
9. Leap speed:
   - `speed = 300 + 480 * chargeNorm`.
   - Cap 780 px/s.
10. Set frog velocity to `aim * speed`.
11. State becomes `air`.
12. No horizontal input changes velocity while air.
13. Crouch does not hide the frog from hazards.

Numbers:

| Value | Number |
| --- | ---: |
| Min charge | 0.10s |
| Max charge | 0.45s |
| Min speed | 300 px/s |
| Max speed | 780 px/s |
| Gravity | 1600 px/s² |
| Terminal velocity | 950 px/s |
| Max vertical height | ~190 px |
| Air control | 0 |

## 4.3 Tongue anchoring, hanging, swinging

**Tier:** 1

Rules:

1. Press `E` to fire tongue toward aim.
2. Tongue extends at 1800 px/s.
3. Max length: 260 px.
4. Attach radius: 12 px.
5. Tongue can attach only to entities with `grabbable=true`.
6. Cooldown after fire or detach: 0.18s.
7. If tongue attaches:
   - frog state becomes `hanging`,
   - distance to anchor is constrained to current tongue length,
   - velocity projected onto pendulum tangent.
8. Press `E` again to detach.
9. While hanging, `A/D` apply swing torque:
   - torque 520 px/s²,
   - damping 0.985 per fixed step.
10. While swinging, frog state is `swinging`.
11. Release from anchor keeps current velocity; no free steering after release.
12. If anchor is breakable, strain rules apply.
13. If anchor is sturdy, no strain.
14. Tongue cannot attack hazards.
15. Tongue cannot collect items.

Numbers:

| Value | Number |
| --- | ---: |
| Max length | 260 px |
| Extend speed | 1800 px/s |
| Attach radius | 12 px |
| Cooldown | 0.18s |
| Detach delay | 0.05s |
| Swing torque | 520 px/s² |
| Damping | 0.985 |

## 4.4 Stick, slide, and surface state

**Tier:** 1

Surface types:

| Surface | Grip | Visual | Behavior |
| --- | --- | --- | --- |
| Wet wall | allowed | cyan shine | Can be stuck if holding `S`. |
| Smooth/dry wall | not allowed | pale matte | Slides fast, cannot stick. |
| Perch top | grounded | normal | Frog can stand, crouch, leap. |
| Safe perch | grounded | moon ring | Checkpoint, safe. |
| Goal perch | grounded | bright moon ring | Leg complete. |

Rules:

1. If frog collides with surface, state becomes `wallContact`.
2. If holding `S` and surface is wet:
   - if normal impact ≤820 px/s and tangential speed ≤500 px/s, state becomes `stuck`.
   - velocity becomes zero.
3. While stuck, holding `S` maintains grip.
4. Releasing `S` makes frog slide or fall.
5. Pressing `Space` while stuck performs a committed leap from the wall.
6. Pressing `E` while stuck can fire tongue.
7. If surface is smooth/dry, holding `S` has no grip effect.
8. Slide acceleration:
   - wet not gripping: 720 px/s² along surface tangent.
   - smooth/dry: 1360 px/s² along surface tangent.
9. Max slide speed 650 px/s.
10. If frog lands on a perch with downward speed >820 px/s, it slides off unless perch is safe and speed ≤950 px/s.
11. Safe perches always accept landing if speed ≤950 px/s.
12. Ordinary perches accept landing only if speed ≤820 px/s; otherwise frog slides off.

Numbers:

| Value | Number |
| --- | ---: |
| Grip normal impact max | 820 px/s |
| Grip tangential speed max | 500 px/s |
| Wet slide acceleration | 720 px/s² |
| Smooth/dry slide acceleration | 1360 px/s² |
| Max slide speed | 650 px/s |
| Ordinary perch landing max | 820 px/s |
| Safe perch landing max | 950 px/s |

## 4.5 Breakable supports

**Tier:** 1

Rules:

1. Entities with `breakable=true` can be grabbed or stood on until strain reaches 1.0.
2. Strain sources:
   - passive hanging: +0.35/s,
   - swing at max torque: +0.45/s,
   - impact attach: if normal impact >400 px/s, add `(impact - 400) / 1000`, cap 0.5.
3. Strain never decreases while attached.
4. Breakable supports break at strain ≥1.0.
5. On break:
   - tongue detaches if attached,
   - support becomes non-collidable and non-grabbable,
   - snap sound plays,
   - frog falls according to physics.
6. Visual strain:
   - 0.35: small crack,
   - 0.65: amber crack,
   - 0.90: red crack and slight flex.
7. Sturdy supports have `breakable=false` and `maxStrain=0`.
8. Thin supports are always breakable.
9. Breakable supports can be used for a beat; if the player reacts, they can detach before break.

Numbers:

| Value | Number |
| --- | ---: |
| Passive strain | 0.35/s |
| Swing strain | 0.45/s max |
| Impact strain cap | 0.5 |
| Break threshold | 1.0 |
| Visual cracks | 0.35, 0.65, 0.90 |

## 4.6 Watching dangers and attention

**Tier:** 1 for cat system; Tier 2 for heron, fish, sprinkler content.

General rules:

1. Hazards are not enemies with health.
2. Hazards cannot be attacked.
3. Hazards cannot be commanded.
4. Hazards are readable through visible attention or movement patterns.
5. Solid geometry blocks line-of-sight.
6. Player movement is measured as frog speed, not mouse movement.
7. Stillness means frog speed <15 px/s and no swing input.
8. Attention max is 1.0.
9. At attention ≥1.0, hazard enters `locked`.
10. Locked hazards act after their lock timer.
11. Acting hazards may capture the frog.
12. Capture causes `caught` state and reset.
13. Disturbances can divert, disable, or delay hazards through physical cause/effect.

### Cat

| Property | Number |
| --- | ---: |
| Patrol speed | 90 px/s |
| Attention cone range | 240 px |
| Attention cone total angle | 120° |
| Suspicion from movement >40 px/s | +1.0/s |
| Suspicion from crouch/aim without motion | +0.2/s |
| Decay from stillness | -1.2/s |
| Lock threshold | 1.0 |
| Lock time | 0.7s |
| Pounce speed | 700 px/s |
| Pounce active | 0.25s |
| Cooldown | 1.4s |
| Capture box | 18×18 |

Rules:

1. Cat patrols a tempting roof edge or gutter.
2. If frog is in cone and visible, attention increases.
3. If frog is still or behind cover, attention decays.
4. Cat pounces toward frog’s last visible position.
5. If pounce capture box intersects frog, caught.

### Heron

| Property | Number |
| --- | ---: |
| Range | 300 px |
| Vision angle | 90° |
| Suspicion from landing | +0.8 instant |
| Suspicion from movement >40 px/s | +1.2/s |
| Decay from stillness | -1.0/s |
| Lock time | 0.8s |
| Strike active | 0.25s |
| Strike length | 80 px |
| Cooldown | 1.6s |
| Capture box | 16×44 |

Rules:

1. Heron stands near water or garden edge.
2. It watches open perches.
3. Landing noise and movement increase attention.
4. Stillness and cover reduce attention.
5. Strike is a straight peck line.

### Fish

| Property | Number |
| --- | ---: |
| Ripple range | 160 px |
| Suspicion from splash/movement >60 px/s | +1.0/s |
| Decay from stillness | -0.8/s |
| Lock time | 0.6s |
| Lunge speed | 650 px/s |
| Lunge active | 0.2s |
| Cooldown | 1.2s |
| Capture box | 22×16 |

Rules:

1. Fish occupy water areas such as rain barrels or gutter pools.
2. They detect movement patterns through ripples.
3. Still water and still frog reduce attention.
4. Lunge is vertical/surface burst.

### Sprinkler

| Property | Number |
| --- | ---: |
| Off delay | 2.0s |
| Warning | 0.6s |
| Sweep | 1.5s |
| Sweep angle | 110° |
| Sweep range | 180 px |
| Impulse on hit | 350 px/s outward |
| Reset on off | cycle restart |

Rules:

1. Sprinkler is a movement-pattern hazard, not attention hazard.
2. Warning glow tells next sweep.
3. Sweep knocks frog off perch; it does not instantly capture.
4. If knocked into fall, normal failure rules apply.
5. Physical disturbance can delay next cycle by 2.5s.

## 4.7 Failure, dangle, and reset

**Tier:** 1

Rules:

1. Falling below `world.height + 120` starts fall reset.
2. Being caught by hazard starts caught reset.
3. If a fall is stopped by tongue attach, frog enters `dangle`.
4. While dangle, frog can hang until:
   - player presses `E`,
   - support breaks,
   - dangle timer reaches 0, then fall continues.
5. Dangle timer from a fall catch: 1.2s.
6. Caught state lasts 0.9s.
7. Fall reset state lasts 0.8s.
8. During caught or reset, frog cannot act.
9. Reset places frog at last `isSafe=true` perch.
10. If no safe perch reached, place at leg start.
11. Reset also resets all hazards, breakables, and disturbables to initial state.
12. Reset does not grant invulnerability beyond reset state.
13. Getting caught is embarrassment animation, not combat.

Numbers:

| Value | Number |
| --- | ---: |
| Fall threshold | world.height + 120 |
| Dangle timer | 1.2s |
| Caught timer | 0.9s |
| Fall reset timer | 0.8s |
| Invulnerable after reset | 0.35s |

## 4.8 Tongue physical disturbance

**Tier:** 2

Rules:

1. Press `E` toward a disturbable object to grab it.
2. Pull direction is aim vector.
3. Pull impulse: 220 px/s applied to small object; object animates but remains fixed anchor.
4. Effects are physical cause/effect only.
5. Effects do not damage or command hazards.
6. Effects have fixed durations.
7. A disturbable object can be used once until reset.

### Branch

| Field | Value |
| --- | ---: |
| Pull impulse | 220 px/s |
| Effect delay | 0.8s |
| Effect duration | 3.0s |
| Effect | Cat attention set to 0; cat moves toward branch/away from original route for 3.0s. |
| Visual | Leaves rustle, branch sways. |

### Cork

| Field | Value |
| --- | ---: |
| Pull impulse | 220 px/s |
| Effect delay | 0.5s |
| Effect duration | 4.0s |
| Effect | Fish diverted to splash location; fish disabled for 4.0s. If near sprinkler, sprinkler cycle delayed by 2.5s. |
| Visual | Water falls, splash ripple. |

### Strand of spider silk

| Field | Value |
| --- | ---: |
| Pull impulse | 180 px/s |
| Effect delay | 0.4s |
| Effect duration | 3.5s |
| Effect | Heron line-of-sight broken; heron turns toward vibrating web and is disabled for 3.5s. |
| Visual | Silk vibrates, web moves. |

## 4.9 Crafted leg progression and difficulty escalation

**Tier:** 2 for Legs 2–3; Tier 1 for Leg 1.

### Leg structure

1. Each leg is a run.
2. Each leg starts at a low exposed place.
3. Each leg ends at a higher safe perch or district boundary.
4. The moonlit pond is visible in the background and heard by frog calls.
5. Failure returns to last safe perch or start.
6. Completion shows district boundary, then next leg intro.
7. After Leg 3, show game complete epilogue with moonlit pond and calling frogs.

### Leg 1: Rain Barrel Yard

**Tier:** 1

World bounds: 1600×700.

| Key point | Position | Notes |
| --- | ---: | --- |
| Start | 140,540 | Low rain barrel lid, not safe. |
| Checkpoint safe perch | 700,300 | Higher rain barrel rim, safe. |
| Goal safe perch | 1360,120 | Water tank rim, district boundary. |

Required entities:

| Entity | Count | Required properties |
| --- | ---: | --- |
| Start perch | 1 | `isStart=true`, not safe. |
| Safe perch | 1 | `isSafe=true`. |
| Goal perch | 1 | `isGoal=true`, `isSafe=true`. |
| Ordinary perch | 2 | usable but not checkpoints. |
| Wet wall | 2 | grip allowed. |
| Smooth/dry wall | 1 | slide hazard. |
| Sturdy anchor | 3 | grabbable, not breakable. |
| Breakable twig | 2 | grabbable, strain 1.0. |
| Cat | 1 | guards obvious open roof path. |

Required segments:

| Segment | Obvious path | Clever physical route |
| --- | --- | --- |
| 1. Low start to first perch | Open roof watched by cat | Crouch/leap to wet wall, hold grip, leap to ordinary perch. |
| 2. First perch to checkpoint | Smooth/dry wall shortcut | Stick wet wall, tongue sturdy anchor, swing to checkpoint. |
| 3. Checkpoint to goal | Open roof line watched by cat | Chain sturdy anchors and one breakable twig, time cat attention, reach goal. |

### Leg 2: Gutter Ridge

**Tier:** 2

World bounds: 1800×800.

| Key point | Position | Notes |
| --- | ---: | --- |
| Start | 160,660 | Exposed gutter edge. |
| Checkpoint safe perch | 850,400 | Safe garden beam. |
| Goal safe perch | 1550,160 | District boundary. |

Required entities:

| Entity | Count |
| --- | ---: |
| Start perch | 1 |
| Safe perch | 1 |
| Goal perch | 1 |
| Ordinary perch | 3 |
| Wet wall | 2 |
| Smooth/dry wall | 2 |
| Sturdy anchor | 4 |
| Breakable twig | 4 |
| Cat | 1 |
| Heron | 1 |
| Branch | 1 |

Required difficulty:

1. Obvious path has two watching dangers: cat and heron.
2. Several supports are thin and break under swing.
3. Smooth/dry walls force longer wet-wall chains.
4. Clever path uses branch to divert cat, then longer tongue chain.

### Leg 3: Garden Edge District

**Tier:** 2

World bounds: 2100×900.

| Key point | Position | Notes |
| --- | ---: | --- |
| Start | 180,740 | Low garden planter. |
| Checkpoint safe perch | 1050,450 | Safe roof tile. |
| Goal safe perch | 1900,180 | Final district boundary. |

Required entities:

| Entity | Count |
| --- | ---: |
| Start perch | 1 |
| Safe perch | 1 |
| Goal perch | 1 |
| Ordinary perch | 4 |
| Wet wall | 2 |
| Smooth/dry wall | 2 |
| Sturdy anchor | 5 |
| Breakable twig | 5 |
| Fish | 1 |
| Sprinkler | 1 |
| Cork | 1 |
| Strand of spider silk | 1 |

Required difficulty:

1. Obvious path crosses sprinkler and fish water.
2. Clever path uses cork to delay fish or sprinkler.
3. Clever path uses spider silk to break heron line-of-sight if heron present; if heron not present, it may be used to distract fish by vibrating leaves.
4. Long physical chains require precise tongue and breakable timing.

## 4.10 Camera

**Tier:** 1

Rules:

1. Camera target is frog center.
2. Deadzone:
   - x: ±180 px,
   - y: ±120 px.
3. If frog exits deadzone, camera lerps toward frog.
4. Lerp factor: 0.12 per fixed step.
5. Camera clamps to level bounds.
6. Camera must always include:
   - frog,
   - next reachable perch,
   - nearest grabbable supports,
   - nearest hazard attention cone,
   - goal if within 1.5 screen widths.
7. No camera shake except snap, splash, caught.

Numbers:

| Value | Number |
| --- | ---: |
| Viewport | 960×540 |
| Deadzone X | 180 px |
| Deadzone Y | 120 px |
| Lerp | 0.12 |
| Max shake | 3 px, 0.18s |

## 4.11 Feel

**Tier:** 1 polish, required from Tier 1.

| Moment | Feel rule |
| --- | --- |
| Crouch | Frog visibly compresses; charge meter fills; subtle coil sound. |
| Leap | Immediate launch, no air steering; player sees arc. |
| Stick | Small wet impact, frog sticks; holding `S` shows grip indicator. |
| Slide | Wet slide is slower and sticky-looking; smooth/dry slide is faster and flat. |
| Tongue fire | Fast, accurate, no attack sound. |
| Attach | Soft hook, frog swings. |
| Breakable stress | Cracks and flex communicate strain. |
| Break | Snap, detach, fall. |
| Hazard reading | Eyes, cones, ripples, warning glows. |
| Caught | Frog blinks, embarrassed pose, no damage numbers. |
| Reset | Soft splash or rooftop landing, not death. |
| Goal | Frog calls softly, moon pond brightens. |

## 4.12 Extra mechanics

**Tier:** 3

| Extra mechanic | Count |
| --- | ---: |
| None | 0 |

# 5. CHARACTERS

## Frog

Silhouette:

- Small, compact body.
- Large eyes visible.
- Short legs.
- Tongue is a thin pink line.
- Crouch compresses vertical profile.
- No weapons, no armor, no combat stance.

States:

| State | Visual | Motion rule |
| --- | --- | --- |
| grounded | normal idle | Can crouch, tongue, aim. |
| crouching | compressed | Charge visible. |
| air | stretched | No control. |
| wallContact | touching surface | May become stuck or slide. |
| stuck | pressed to wet wall | Holding `S` maintains. |
| sliding | moving along surface | Wet or smooth visual. |
| hanging | tongue attached | Dangling. |
| swinging | moving arc | `A/D` torque. |
| dangle | after fall catch | Brief hang. |
| caught | blink, embarrassed pose | Reset timer. |
| reset | fading/splash | Return to checkpoint. |

Animations:

| Name | Trigger | Duration |
| --- | --- | ---: |
| idle | grounded | loop |
| crouch | Space held | 0.1s blend |
| leap | Space release | 0.15s |
| stickImpact | stuck start | 0.12s |
| slide | sliding | loop |
| tongueExtend | E press | until attach/max |
| tongueSnap | detach/break | 0.1s |
| hang | hanging start | 0.2s |
| swing | swinging | loop |
| breakSnap | support break | 0.2s |
| caught | hazard capture | 0.9s |
| reset | reset start | 0.8s |
| goalCall | goal reached | 1.2s |

## Cat

Silhouette: black rooftop cat, amber eyes, tail visible.

States:

| State | Visual |
| --- | --- |
| neutral | calm, tail idle |
| suspicious | eyes bright, head turns |
| locked | crouch pounce windup |
| acting | pounce |
| cooldown | looks away, resets |
| diverted | follows disturbance |

## Heron

Silhouette: tall gray bird, long neck, straight beak.

States:

| State | Visual |
| --- | --- |
| neutral | standing |
| suspicious | neck extends |
| locked | head lowered |
| acting | strike line |
| cooldown | resets |
| diverted | looks at web |

## Fish

Silhouette: dark shape in water.

States:

| State | Visual |
| --- | --- |
| neutral | idle |
| suspicious | ripples |
| locked | surface bubble |
| acting | lunge |
| cooldown | fades |
| diverted | follows splash |

## Sprinkler

Not a character, but visible hazard.

States:

| State | Visual |
| --- | --- |
| off | dark head |
| warning | amber glow |
| acting | water arc |
| cooldown | off |
| delayed | dim glow, no cycle |

# 6. AUDIO

| Sound | Recipe | When it plays |
| --- | --- | --- |
| ambient_rain | Low pink noise, lowpass 1200Hz, volume 0.08, loop | Leg 1, Leg 2 background. |
| ambient_water | Brown noise, bandpass 700Hz, slow LFO, volume 0.06, loop | Near water areas. |
| ambient_frog_calls | Short sine chirps 180–260Hz, random intervals 1.5–4s, volume 0.05, loop | Background, stronger near goal. |
| crouch | Triangle oscillator 120Hz -> 90Hz, 0.18s, volume 0.12 | Start crouch. |
| crouch_charge | Sawtooth 90Hz -> 180Hz, volume scales with charge | While crouching. |
| leap | Triangle 220Hz -> 500Hz, 0.12s, volume 0.18 | Release crouch. |
| stick_wet | Noise burst, bandpass 1800Hz, decay 0.08s, volume 0.12 | Stick to wet surface. |
| slide_wet | Filtered noise loop, 900Hz, volume 0.06 | Sliding on wet. |
| slide_smooth | Thin sine 700Hz, volume 0.05, pitch drops | Sliding on smooth/dry. |
| tongue_fire | Square 300Hz -> 120Hz, 0.05s, volume 0.12 | Press E. |
| tongue_attach | Sine 420Hz, short pluck, volume 0.14 | Tongue attaches. |
| tongue_detach | Sine 300Hz -> 180Hz, 0.07s, volume 0.1 | Detach. |
| swing_air | Soft filtered noise loop, volume 0.04 | While swinging. |
| break_crack | Noise burst, highpass 2200Hz, 0.12s, volume 0.18 | Support cracks. |
| break_snap | Square 180Hz -> 80Hz, 0.1s, volume 0.22 | Support breaks. |
| cat_attention | Low sine 70Hz, slow tremolo, volume 0.07 | Cat attention >0.5. |
| cat_pounce | Noise burst + sine 120Hz, 0.18s, volume 0.2 | Cat acts. |
| heron_strike | Sine 900Hz -> 300Hz, 0.1s, volume 0.2 | Heron strike. |
| fish_ripple | Sine 180Hz, LFO, volume 0.08 | Fish attention. |
| fish_lunge | Noise + sine 220Hz, 0.12s, volume 0.18 | Fish acts. |
| sprinkler_warning | Sine 600Hz, pulse 0.6s, volume 0.12 | Sprinkler warning. |
| sprinkler_sweep | Filtered noise, volume 0.16, loop 1.5s | Sprinkler sweep. |
| branch_pull | Wood noise, 400Hz band, 0.15s, volume 0.12 | Pull branch. |
| cork_pull | Cork pop, square 160Hz, 0.1s, volume 0.14 | Pull cork. |
| silk_pull | High sine 1800Hz, vibrato, 0.18s, volume 0.1 | Pull spider silk. |
| caught | Soft descending sine 420Hz -> 160Hz, 0.5s, volume 0.16 | Caught reset. |
| reset | Water splash noise, volume 0.14 | Reset. |
| goal_call | Frog chirp chord 180/220/260Hz, 0.8s, volume 0.2 | Reach goal. |
| moon_pond_reveal | Soft pad, sine 220/330/440Hz, volume 0.12, loop | Game complete. |

# 7. UX

## Screens state machine

| State | Show | Input | Transition |
| --- | --- | --- | --- |
| boot | loading | none | -> title |
| title | title, controls, start button | Enter/click start | -> legIntro |
| legIntro | leg name, goal, controls | Enter/click start | -> playing |
| playing | canvas, HUD | game inputs | -> caught or legComplete |
| caught | embarrassed overlay, reason | auto after 0.9s | -> playing |
| legComplete | safe perch, next leg | Enter/click next | -> legIntro or gameComplete |
| gameComplete | moonlit pond, credits | Enter/click title | -> title |
| debug | debug panel | `F1` toggles | -> playing/title |

## HUD table

| HUD element | Record field | When visible |
| --- | --- | --- |
| Leg name | `ProgressionState.legIndex`, `LevelState.name` | playing, legIntro |
| Charge meter | `FrogState.chargeNorm` | while crouching |
| Grip indicator | `FrogState.gripHeld`, `FrogState.stuck` | while wallContact or stuck |
| Tongue target highlight | `TongueState.targetX`, `TongueState.targetY`, `TongueState.active` | while aiming tongue |
| Breakable strain | nearest `Entity.strain` | when attached or near breakable |
| Safe perch found | `FailureState.lastSafeId` | after reaching checkpoint |
| Goal direction | `LevelState.goalId`, frog position | playing |
| Attention warning | any `Hazard.attention > 0.7` | playing |
| Controls hint | static | legIntro only |

## HTML/CSS requirements

1. All screens and HUD are HTML/CSS.
2. Game world renders in `<canvas>`.
3. HUD is absolutely positioned over canvas.
4. No external UI framework.
5. No modal blocking during caught; overlay fades.
6. All text uses system font stack.
7. Colors match visual palette.

# 8. DEBUG API

All debug functions are read-only unless marked.

```js
debug.input.getState() -> InputState
debug.input.setAim(x, y) -> void
debug.input.press(name) -> void
debug.input.release(name) -> void
```

```js
debug.frog.getState() -> FrogState
debug.frog.setState(state) -> void
debug.frog.setVelocity(vx, vy) -> void
debug.frog.forceReset() -> void
```

```js
debug.tongue.getState() -> TongueState
debug.tongue.forceAttach(anchorId) -> void
debug.tongue.forceDetach() -> void
```

```js
debug.surfaces.getState() -> SurfaceIndex
debug.surfaces.getAt(x, y) -> Entity|null
```

```js
debug.breakables.getState() -> BreakableIndex
debug.breakables.addStrain(entityId, amount) -> void
debug.breakables.break(entityId) -> void
```

```js
debug.hazards.getState() -> HazardIndex
debug.hazards.setAttention(hazardId, value) -> void
debug.hazards.lock(hazardId) -> void
debug.hazards.disable(hazardId, seconds) -> void
```

```js
debug.disturbables.getState() -> DisturbableIndex
debug.disturbables.pull(disturbableId, direction) -> void
debug.disturbables.resetAll() -> void
```

```js
debug.failure.getState() -> FailureState
debug.failure.forceCaught(hazardId) -> void
debug.failure.forceReset() -> void
```

```js
debug.progression.getState() -> ProgressionState
debug.progression.startLeg(index) -> void
debug.progression.completeLeg() -> void
debug.progression.completeGame() -> void
```

```js
debug.camera.getState() -> CameraState
debug.camera.setCenter(x, y) -> void
```

```js
debug.level.getState() -> LevelState
debug.level.load(index) -> void
debug.level.getEntities() -> Entity[]
```

# 9. TESTS

## Tier 1 tests

| Test ID | Validation |
| --- | --- |
| T1-INPUT-01 | Mouse aim produces valid aim vector. |
| T1-INPUT-02 | `Space` hold/release creates crouch state and leap only if charge ≥0.10s. |
| T1-LEAP-01 | Max charge speed is 780 px/s. |
| T1-LEAP-02 | No horizontal air control changes velocity. |
| T1-TONGUE-01 | `E` fires tongue and attaches only to `grabbable=true` entities. |
| T1-TONGUE-02 | Tongue max length is 260 px. |
| T1-SWING-01 | While attached, `A/D` apply swing torque and constraint. |
| T1-SURFACE-01 | Wet wall + holding `S` results in stuck state. |
| T1-SURFACE-02 | Smooth/dry wall + holding `S` does not stick. |
| T1-SURFACE-03 | Slide acceleration differs wet vs smooth. |
| T1-BREAK-01 | Breakable strain increases while hanging. |
| T1-BREAK-02 | Breakable breaks at strain ≥1.0 and detaches frog. |
| T1-HAZARD-CAT-01 | Cat attention increases when frog moves in cone. |
| T1-HAZARD-CAT-02 | Cat attention decays when frog is still. |
| T1-HAZARD-CAT-03 | Cat pounce capture causes caught state. |
| T1-FAILURE-01 | Fall below world triggers reset. |
| T1-FAILURE-02 | Reset places frog at last safe perch if present. |
| T1-FAILURE-03 | Reset places frog at leg start if no safe perch. |
| T1-LEG-01 | Leg 1 goal entity triggers leg complete. |
| T1-VISUAL-01 | Wet, smooth, sturdy, thin, safe surfaces are visually distinct. |
| T1-AUDIO-01 | Core sounds play on corresponding state transitions. |
| T1-HUD-01 | Charge, grip, tongue target, strain HUD fields are bound. |

## Tier 2 tests

| Test ID | Validation |
| --- | --- |
| T2-DIST-BRANCH-01 | Pulling branch diverts cat for 3.0s. |
| T2-DIST-CORK-01 | Pulling cork disables fish for 4.0s or delays sprinkler by 2.5s. |
| T2-DIST-SILK-01 | Pulling spider silk disables heron for 3.5s. |
| T2-LEG-LOAD-01 | Leg 2 loads with required hazard and support counts. |
| T2-LEG-LOAD-02 | Leg 3 loads with required hazard and support counts. |
| T2-PROGRESS-01 | Completing Leg 1 starts Leg 2. |
| T2-PROGRESS-02 | Completing Leg 3 starts game complete. |
| T2-HAZARD-HERON-01 | Heron lock and strike capture rules work. |
| T2-HAZARD-FISH-01 | Fish ripple detection and lunge work. |
| T2-HAZARD-SPRINKLER-01 | Sprinkler warning/sweep cycle works. |
| T2-RESET-WORLD-01 | Failure resets hazards, breakables, disturbables. |

# 10. BUILD ORDER

1. Create HTML shell, canvas, CSS palette, fixed loop.
2. Implement input state and aim.
3. Implement context records.
4. Implement frog physics and grounded state.
5. Implement crouch and committed leap.
6. Implement level loading and collision.
7. Implement wet/smooth surface collision.
8. Implement stick with `S` and slide.
9. Implement tongue fire/attach/detach.
10. Implement hang and swing constraint.
11. Implement breakable strain and snap.
12. Implement cat hazard attention and pounce.
13. Implement failure, dangle, caught, reset.
14. Implement camera.
15. Implement Tier 1 Leg 1 entities.
16. Implement Tier 1 art: palette, surfaces, frog, cat.
17. Implement Tier 1 audio.
18. Implement HUD and screens.
19. Run Tier 1 tests.
20. Implement branch, cork, spider silk disturbances.
21. Implement heron, fish, sprinkler.
22. Implement Leg 2 and Leg 3.
23. Implement progression and game complete.
24. Run Tier 2 tests.
25. Balance and polish within defined numbers only.

# 11. DEFINITION OF DONE

## Tier 1 Definition of Done

High-level: A player can complete Leg 1 using only core mechanics and survive/learn through readable hazards and failure reset.

- [ ] Fixed 60Hz loop exists.
- [ ] Input state includes aim, crouch, tongue, grip, swing.
- [ ] Frog has states: grounded, crouching, air, wallContact, stuck, sliding, hanging, swinging, dangle, caught, reset.
- [ ] Crouch charges and releases a committed leap.
- [ ] No air control exists.
- [ ] Tongue attaches only to grabbable supports.
- [ ] Tongue max length and cooldown are enforced.
- [ ] Hang/swing pendulum works.
- [ ] Wet walls can be stuck with `S`.
- [ ] Smooth/dry walls cannot stick and slide faster.
- [ ] Breakable supports strain and snap.
- [ ] Cat hazard has neutral, suspicious, locked, acting, cooldown states.
- [ ] Cat attention responds to movement and stillness.
- [ ] Cat capture causes caught reset.
- [ ] Fall below world causes reset.
- [ ] Reset returns to last safe perch or leg start.
- [ ] Leg 1 has start, checkpoint, goal, required supports, one cat.
- [ ] Goal reaches leg complete.
- [ ] Camera keeps required elements in frame.
- [ ] Tier 1 visual palette and surface cues exist.
- [ ] Tier 1 audio exists.
- [ ] HUD fields exist.
- [ ] All Tier 1 tests pass.

## Tier 2 Definition of Done

High-level: A player can progress through three crafted legs, using physical disturbance and additional watching dangers, without adding any extra mechanics.

- [ ] Branch, cork, spider silk are grabbable and have defined effects.
- [ ] Disturbance effects only affect attention, line-of-sight, or timers.
- [ ] Heron hazard works.
- [ ] Fish hazard works.
- [ ] Sprinkler hazard works.
- [ ] Leg 2 loads with required counts.
- [ ] Leg 3 loads with required counts.
- [ ] Leg completion progresses to next leg.
- [ ] Game complete shows moonlit pond and calling frogs.
- [ ] Failure resets dynamic world state.
- [ ] All Tier 2 tests pass.

## Tier 3 Definition of Done

- [ ] No extra mechanics added.
- [ ] No collectathon.
- [ ] No combat.
- [ ] No new powers.
- [ ] No hidden stealth crouch.
- [ ] No run ending at the next pond.

# A. SANITY

| Check | Result |
| --- | --- |
| Does Tier 1 contain exactly core mechanics? | Yes. Crouch/leap, tongue anchor/swing, stick/slide, breakable, watching danger, failure/dangle/reset are all Tier 1. |
| Does Tier 1 include at least one watching danger? | Yes, Leg 1 includes one cat. |
| Does Tier 1 include wet/slippery/breakable supports? | Yes, Leg 1 includes wet walls, smooth/dry wall, sturdy anchors, breakable twigs. |
| Are supporting mechanics deferred to Tier 2? | Yes. Physical disturbance and leg progression beyond Leg 1 are Tier 2. |
| Are extra mechanics absent? | Yes. Tier 3 is none. |
| Are there exactly the listed content parts? | Yes. Rosters list only allowed content. Pickups are zero. |
| Is there any running? | No. Grounded movement keys rotate facing only. |
| Is there any combat? | No. Hazards capture and reset; no HP, no attack. |
| Is crouch stealth? | No. Stillness is separate and based on velocity/line-of-sight. |
| Is free midair steering forbidden? | Yes. Air state has no input velocity change. |
| Does failure return to last safe perch or leg start? | Yes, `FailureState` and tests enforce it. |
| Does the moonlit pond remain distant goal? | Yes, background goal and game complete epilogue; runs end at district boundaries. |
| Are all systems tied to records and functions? | Yes, #2 defines required fields and functions. |
| Are numbers concrete? | Yes, physics, surface, tongue, breakable, hazard, timing, and level counts are numeric. |
| Are visuals and audio present in Tier 1? | Yes, Tier 1 build order and definition of done require palette, animation, sound, HUD. |
| Are tests tied to tiers? | Yes, Tier 1 and Tier 2 tests are separate. |