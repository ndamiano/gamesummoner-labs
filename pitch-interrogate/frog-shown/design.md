# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| A platformer where the player is a frog. | All sections; the player is a small frog, not a human in a frog suit. |
| Side-on 2D platformer view; camera follows at ground scale; vertical scroll; distant rooftop pond visible when possible. | `1.1`, `3. VISUAL SPEC`, `4.12 Progression and difficulty`, `5. CHARACTERS` |
| Real-time. | `1.1`, `2. CONTRACTS`, `4. GAMEPLAY SPEC` |
| Run begins when the frog wakes on a leaf in a rain barrel or is placed at the last safe perch after a hazard reset. | `4.6 Forgiving failure and reset`, `4.13 Runs and level structure` |
| Run ends when the frog reaches the next safe perch; full game ends when the frog reaches the moonlit rooftop pond. | `4.6`, `4.13`, `7. UX`, `11. DEFINITION OF DONE` |
| Opening places close together and legible; later places more vertical, connected, combined, and harder. | `4.13 Progression and difficulty`, `4.7 Combined traversal`, `4.10 Route variety` |
| Tone: quiet, wet, forgiving but never weightless; embarrassment, delay, forced rethink; noticing the world at frog scale. | `3. VISUAL SPEC`, `4. GAMEPLAY SPEC`, `5. CHARACTERS`, `6. AUDIO`, `7. UX` |
| Look/sound: rain-soaked garden and city edge; gutters, rain barrels, drainpipes, stone paths, greenhouse glass, dripping vines, puddles, moonlit rooftop pond; rain, drips, gurgles, frog calls, readable animal cues. | `3. VISUAL SPEC`, `6. AUDIO` |
| Core mechanics exactly: crouch-hop, tongue, sticky climbing and sliding, wet-surface movement and water recovery, avoidance and stillness, forgiving failure and reset. | `4.1`–`4.6`, Tier 1 in `0.3` |
| Supporting mechanics exactly: combined traversal, hazard escalation and distraction, environmental consequences, route variety. | `4.7`–`4.10`, Tier 2 in `0.3` |
| Extra mechanics exactly: eating reactions. | `4.11`, Tier 3 in `0.3` |
| Concrete content: frog, hazards, traps, anchors, landmarks, levels, rules, numbers, input, run structure, visuals, audio, engineering contracts. | All sections |
| Do not add systems left out: no combat, no collectathon, no survival meters, no death screen, no score shame, no locked doors/switches, no map-like reading, no open world, no abstract puzzle machines, no human platformer with frog costume. | `0.2 Decisions`, `4. GAMEPLAY SPEC`, `A. SANITY` |

## 0.2 Decisions

The decisions already made are final. The rulings below close every open decision.

| Decision | Ruling | Why |
| --- | --- | --- |
| Engine | HTML5 Canvas 2D + TypeScript/JavaScript ES modules. No game engine, no external libraries. | Fits a browser game, keeps the builder in control, and lets the spec be precise. |
| UI | Plain HTML/CSS overlays for screens; no framework. World is Canvas. | Satisfies “UX: HTML and CSS only” while preserving a real-time Canvas game. |
| Audio | Synthesized sounds through the available audio API. No audio files. | The prompt gives an audio API and asks for synthesized recipes. |
| World units | 1 unit = 1 cm. 100 units = 1 m. | Gives frog-scale numbers without floating tiny decimals. |
| Canvas logical size | 960×540 px, scale 8 px/unit. Viewport is 120×67.5 units. | Gives a readable 8 cm frog as 64 px and a quiet side-view framing. |
| Coordinate system | x right, y down. Gravity is positive y. | Standard Canvas physics. |
| Physics loop | Fixed 60 Hz step. Max 5 steps per rendered frame. | Deterministic, testable, real-time. |
| Random source | Seeded deterministic PRNG (`xorshift128+`) seeded from `GameState.seed`. | Tests and replayable failure. |
| Player controls | Keyboard + mouse. `A/D` or arrows move. `Space` hold crouch / release crouch-hop. Mouse or `J` tongue with aim. `E` pull physical objects. `Escape` pause. | Keeps the tongue readable as an aim verb, while keyboard-only testing is possible. |
| Movement | Left and right input exist, but the frog does not run. Ground movement is produced by hops, friction, and landing. | Preserves “moves to the right; frog hops; it does not run.” |
| Air control | None. Once airborne, the frog lives with the result. | Commitment and aim are core. |
| Wall jump | No wall jump. Walls are climbed, slid, held, or left by moving away. | The decisions specify sticky climbing and sliding, not wall-jump platforming. |
| Coyote time / jump buffering | None. No forgiveness that makes the frog feel like a human platformer. | Honors “once leaves ground it must live with the result.” |
| Level count | Full game: 5 levels. Tier 1 vertical slice: 3 levels ending at a simplified rooftop pond. | Tier 1 must be finishable; Tier 2 expands into the fuller game. |
| Safe perch | A visible glowing perch. Touch radius 12 units. Reaching it completes the run and loads the next level. | Matches “run ends when reaching next safe perch.” |
| Goal perch | Final moonlit lily in rooftop pond. Touch radius 14 units. | Final game ends at the pond. |
| Failure | No death. Reset to last safe perch, or hazard-specific nearby safe ground. Delay and embarrassment only. | Required tone. |
| Pickups | None. Flies, wasps, beetles are ambient ecology and flavor, not inventory, counters, or score. | Required “not a collectathon.” |
| Enemies | Cat, heron, fish are hazards, not enemies to defeat. | Required “not a combat platformer.” |
| Traps | Slippery surfaces, crumbling ledges, weak anchors, currents, wind, sprinklers, tipping rain barrels. | All are in the supplied content/hazard list. |
| Interact input | `E` pull/hold is only for listed physical objects: cork, sprinkler valve, branch disturbance. No generic switch system. | Environmental consequences require physical interaction, but no abstract switches. |
| Environmental persistence | Interactable effects persist until the level goal. Hazards reset to initial patrol after a frog reset. | Prevents softlocks and supports “forced rethink.” |
| Cat model | Attention meter 0–100. Moving while visible raises it; stillness lowers it. Cat steps closer, then swats. | Required “moving too much makes the cat step closer.” |
| Heron model | Shadow zone over open ground. Strike if frog moves in shadow. Can be distracted by disturbing a branch. | Required distraction and open-ground danger. |
| Fish model | Patrols water, telegraphs snap, resets frog to nearest water edge. | Required hazard. |
| Sprinkler model | Auto-starts sometimes; can be manually started by pulling valve. Makes surfaces slippery and knocks caterpillars off branches. | Required environmental consequence. |
| Wind model | Zones apply horizontal force to airborne frog. Visual streaks. Player is expected to anchor with tongue before hopping. | Required rooftop hazard. |
| Current model | Water volumes with velocity. Carries frog and leaves. | Required water hazard/environmental consequence. |
| Water recovery | Frog swims poorly, surfaces, and can haul out with a small crouch-hop at edges. | Required “swim awkwardly and haul onto nearest edge.” |
| Tongue constraints | Max reach 150 units. Only visible anchors. Cannot stick to smooth glass or open water. Weak anchors break or slip. | Required “not a magic rope.” |
| Sticky walls | Damp climbable walls can be climbed, slid, and held. Smooth glass cannot be stuck to. | Required sticky climbing and sliding. |
| Wet surfaces | Friction table. Bad landings slide. Leaves rock. | Required wet-surface movement. |
| Eating reactions | Eating insects causes physical reactions only: sneeze, hiccup/puff, no score. | Required extra mechanics. |
| HUD | No numeric HUD. Only diegetic world markers: safe perch glow, anchor glints, animal cues. | No map-like reading, no score, no counters. |
| Debug | A debug object exposes direct state for each system and input setters for tests. | Required contracts and tests. |
| Save | No save system. Progress is session-only. | Not requested; avoids extra systems. |
| Accessibility | Pause, readable visual cues, no timed input required beyond real-time physics. | Supports quiet, forgiving tone without adding systems. |
| Multiplayer | Single-player only. | Not requested. |

## 0.3 Tiers

Tier 1 is the core mechanics and a finishable minimal game. Tier 2 adds supporting mechanics and the full level sequence. Tier 3 adds extra mechanics. Polish is not a tier.

| Tier | Segment | Scope | Definition |
| --- | --- | --- | --- |
| Tier 1 | Core traversal and quiet failure | Crouch-hop, tongue anchors/swing/miss/weak anchors, sticky climbing/sliding, wet surfaces, leaf rock, water entry/swim/edge haul, current-free basic water, cat watching/stillness/reset, safe perch, no death, no score. | Player can start on a leaf in a rain barrel, traverse 3 short levels, and reach a simplified rooftop pond. |
| Tier 2 | Supporting mechanics | Combined traversal, hazard escalation and distraction, environmental consequences, route variety, heron, fish, sprinkler, wind, currents, slippery glass, weak anchors, tipping rain barrels, full 5-level sequence. | Player can traverse richer greenhouse and koi-pond places, use hazards, take direct or longer routes, and reach the full rooftop pond. |
| Tier 3 | Eating reactions | Fly sneeze, wasp hiccup/puff, beetle flavor. No counters. | Eating is present as small physical feedback and joke, not progress. |

---

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Value | Number | Meaning |
| --- | ---: | --- |
| Unit | 1 unit = 1 cm | All gameplay distances. |
| Meter | 100 units | Reference only. |
| Canvas logical size | 960 × 540 px | Render target. |
| Pixel scale | 8 px/unit | 1 unit renders as 8 px. |
| Viewport | 120 × 67.5 units | 1.20 m × 0.675 m at any moment. |
| Axis | x right, y down | Standard screen coordinates. |
| Fixed timestep | 1/60 s | Physics and rules. |
| Max physics steps per frame | 5 | Prevent spiral of death. |
| Gravity | 1000 units/s² | Game-feel gravity, not exact Earth gravity. |
| Max fall speed | 900 units/s | Prevent tunneling. |
| Max horizontal speed | 450 units/s | Caps wind/current/slide. |
| Frog hitbox | 8 × 6 units | Centered at `frog.pos`. |
| Frog visual size | 14 × 10 units | Wider than hitbox for readability. |
| Mouth offset | x: facing × 5, y: -1 | Tongue starts here. |
| Safe perch radius | 12 units | Completion trigger. |
| Goal perch radius | 14 units | Final trigger. |
| Tongue max length | 150 units | Not magic rope; reachable only with visible anchors. |
| Tongue extension speed | 1800 units/s | Quick flick. |
| Tongue retract speed | 2400 units/s | Fast miss. |
| Crouch-hop max charge | 0.50 s | Full commitment. |
| Crouch-hop min charge | 0.05 s | Tiny hop. |
| Crouch-hop max launch speed | 480 units/s | Full hop. |
| Crouch-hop min launch speed | 180 units/s | Min hop. |
| Wall climb speed | 140 units/s | Damp sticky wall. |
| Wall slide speed | 200 units/s | Wet non-climb wall. |
| Swim max speed | 100 units/s | Awkward frog. |
| Current max speed | 180 units/s | Can overpower swim. |
| Wind force | 180 units/s² horizontal | Changes hop arc. |
| Rain particles | max 120 | Performance and atmosphere. |
| Ambient insects | 2–5 per level | Ecology, not pickups. |

## 1.2 Important conventions

- Use a fixed 60 Hz update. Render interpolation is optional but must not affect gameplay.
- All random events use `rng.next()` from the seeded PRNG. No `Math.random()` in gameplay.
- No external libraries. No framework. No physics engine.
- No death, no lives, no health, no stamina, no hunger, no thirst, no score, no currency, no collectible counter.
- No combat verbs. The only verbs are movement, tongue, sticky contact, observation, waiting, and physical pull.
- No locked doors, switches, keycards, timers that block progress, or abstract puzzle machines.
- No minimap, compass, quest log, objective list, or map-like HUD.
- Safe perch markers are diegetic world objects, not HUD widgets.
- All mechanics must be visible and testable through the debug API.
- The game may pause, but pause is not a survival mechanic.
- If a hazard resets the frog, the level state is not reloaded. Interactable environmental changes persist. Hazards reset to initial patrol positions and attention states.
- If a level has a direct dangerous route and a longer safe route, both must be reachable without hidden mechanics.
- Anchors, slippery surfaces, weak anchors, and safe perches must have clear visual signatures.
- All audio is synthesized. No recorded animal sounds.

---

# 2. CONTRACTS

## 2.1 Module layout

```txt
index.html
style.css
src/
  main.ts
  constants.ts
  rng.ts
  input.ts
  state.ts
  levelLoader.ts
  levels/
    m1_rain_barrel.ts
    m2_drainpipe_cat.ts
    m3_rooftop_mvp.ts
    l1_rain_barrel.ts
    l2_drainpipe_cat.ts
    l3_greenhouse.ts
    l4_koi_pond.ts
    l5_rooftop_full.ts
  physics.ts
  camera.ts
  crouchHop.ts
  tongue.ts
  anchors.ts
  walls.ts
  water.ts
  cat.ts
  heron.ts
  fish.ts
  sprinkler.ts
  wind.ts
  interactables.ts
  insects.ts
  frog.ts
  render.ts
  audio.ts
  ui.ts
  debug.ts
tests/
  tier1.test.ts
  tier2.test.ts
  tier3.test.ts
```

## 2.2 Global context

The global context is a mutable `GameState` owned by `main.ts`. Every rule reads and writes through it.

```ts
type Vec2 = { x: number; y: number };
type Rect = { x: number; y: number; w: number; h: number };
type Facing = -1 | 1;

type Mode =
  | "boot"
  | "title"
  | "levelStart"
  | "playing"
  | "paused"
  | "embarrassment"
  | "ending";

type FrogState =
  | "grounded"
  | "airborne"
  | "wall"
  | "water"
  | "attached"
  | "reset"
  | "ending";

type SurfaceType =
  | "wetLeaf"
  | "rainBarrelRim"
  | "drainpipeInterior"
  | "wetCrate"
  | "stickyTile"
  | "mossyStone"
  | "woodenFenceRail"
  | "stonePath"
  | "wetTile"
  | "greenhouseGlass"
  | "condensationFrame"
  | "drippingVine"
  | "lilyPad"
  | "tinCan"
  | "gardenHose"
  | "crumblingLedge"
  | "safePerchSurface"
  | "goalLily";

type AnchorType =
  | "branch"
  | "twig"
  | "hangingWire"
  | "bottleCap"
  | "spiderSilk"
  | "insectLeg"
  | "crackedTileEdge"
  | "drippingVineAnchor";

type InsectType = "fly" | "wasp" | "beetle";
type InteractableType = "cork" | "sprinklerValve" | "branchDisturb";
type HazardType =
  | "cat"
  | "heron"
  | "fish"
  | "sprinkler"
  | "wind"
  | "rainBarrelTip";

type EdibleEffect = "none" | "sneeze" | "hiccup";

interface InputState {
  move: -1 | 0 | 1;
  crouchHeld: boolean;
  crouchPressed: boolean;
  crouchReleased: boolean;
  tongueHeld: boolean;
  tonguePressed: boolean;
  tongueReleased: boolean;
  tongueAim: Vec2;
  interactHeld: boolean;
  pausePressed: boolean;
  startPressed: boolean;
}

interface Surface {
  id: string;
  rect: Rect;
  type: SurfaceType;
  friction: number;
  climbable: boolean;
  stickyTongue: boolean;
  occluder: boolean;
  breakable: boolean;
  breakTimer: number;
  breakLimit: number;
  respawnTimer: number;
  broken: boolean;
  moving: boolean;
  moveOffset: Vec2;
  moveTarget: Vec2;
  moveSpeed: number;
  rocking: number;
}

interface Anchor {
  id: string;
  pos: Vec2;
  radius: number;
  type: AnchorType;
  validForTongue: boolean;
  breakTime: number;
  breakSpeed: number;
  slipAmount: number;
  broken: boolean;
  visible: boolean;
}

interface WaterVolume {
  id: string;
  rect: Rect;
  depth: number;
  current: Vec2;
  currentStrength: number;
}

interface Current {
  id: string;
  rect: Rect;
  velocity: Vec2;
  strength: number;
  active: boolean;
}

interface SafePerch {
  id: string;
  pos: Vec2;
  radius: number;
  reached: boolean;
}

interface GoalPerch {
  id: string;
  pos: Vec2;
  radius: number;
}

interface CatHazard {
  id: string;
  type: "cat";
  pos: Vec2;
  initialPos: Vec2;
  facing: Facing;
  attention: number;
  state: "watching" | "approaching" | "crouched" | "strike";
  step: number;
  maxSteps: number;
  strikeTimer: number;
  hitRect: Rect;
}

interface HeronHazard {
  id: string;
  type: "heron";
  pos: Vec2;
  initialPos: Vec2;
  patrolStart: Vec2;
  patrolEnd: Vec2;
  shadowRect: Rect;
  attention: number;
  state: "patrol" | "shadow" | "distracted" | "strike";
  distractionTimer: number;
  strikeTimer: number;
  hitRect: Rect;
}

interface FishHazard {
  id: string;
  type: "fish";
  pos: Vec2;
  initialPos: Vec2;
  patrolPath: Vec2[];
  state: "patrol" | "telegraph" | "snap";
  telegraphTimer: number;
  hitRadius: number;
}

interface SprinklerHazard {
  id: string;
  type: "sprinkler";
  pos: Vec2;
  zone: Rect;
  state: "off" | "on";
  timer: number;
  autoInterval: number;
  autoOnTime: number;
  manualOnTime: number;
  affectsCaterpillar: boolean;
}

interface WindHazard {
  id: string;
  type: "wind";
  zone: Rect;
  force: number;
  direction: Facing;
  state: "calm" | "building" | "blowing";
  timer: number;
  nextChangeTimer: number;
}

interface RainBarrelTip {
  id: string;
  type: "rainBarrelTip";
  body: Rect;
  state: "stable" | "rocking" | "tip";
  timer: number;
  impulseThreshold: number;
}

type Hazard =
  | CatHazard
  | HeronHazard
  | FishHazard
  | SprinklerHazard
  | WindHazard
  | RainBarrelTip;

interface Interactable {
  id: string;
  type: InteractableType;
  pos: Vec2;
  radius: number;
  progress: number;
  completeTimer: number;
  state: "idle" | "pulling" | "complete";
  effect: string;
}

interface Insect {
  id: string;
  type: InsectType;
  pos: Vec2;
  vel: Vec2;
  path: Vec2[];
  alive: boolean;
  eaten: boolean;
  radius: number;
}

interface Level {
  id: string;
  name: string;
  sequence: "mvp" | "full";
  bounds: Rect;
  start: Vec2;
  surfaces: Surface[];
  anchors: Anchor[];
  water: WaterVolume[];
  currents: Current[];
  hazards: Hazard[];
  interactables: Interactable[];
  insects: Insect[];
  safePerch: SafePerch;
  goal?: GoalPerch;
  isFinal: boolean;
  routeHints: string[];
}

interface Frog {
  pos: Vec2;
  vel: Vec2;
  size: { w: number; h: number };
  facing: Facing;
  state: FrogState;
  groundedSurfaceId: string | null;
  wallSurfaceId: string | null;
  crouch: {
    held: boolean;
    charge: number;
  };
  tongue: {
    active: boolean;
    targetId: string | null;
    targetKind: "anchor" | "insect" | "none";
    anchorPos: Vec2;
    length: number;
    missTimer: number;
    attachedTime: number;
    eatEffect: EdibleEffect;
  };
  swim: {
    inWater: boolean;
    depth: number;
    paddle: number;
    edgeId: string | null;
  };
  eatenEffect: {
    type: EdibleEffect;
    timer: number;
    impulse: Vec2;
  };
  embarrassment: {
    timer: number;
    cause: string;
  };
  lastSafePerch: Vec2;
  animation: string;
  animationTime: number;
}

interface Camera {
  pos: Vec2;
  target: Vec2;
  deadzone: { x: number; y: number };
  lerp: number;
  shake: number;
  pondVisible: boolean;
}

interface RNG {
  seed: number;
  next: () => number;
  nextFloat: (min: number, max: number) => number;
  nextInt: (min: number, max: number) => number;
}

interface GameState {
  mode: Mode;
  seed: number;
  time: number;
  levelIndex: number;
  sequence: "mvp" | "full";
  level: Level;
  frog: Frog;
  input: InputState;
  camera: Camera;
  rng: RNG;
  reset: {
    active: boolean;
    timer: number;
    cause: string;
    target: Vec2;
  };
  ending: {
    active: boolean;
    timer: number;
  };
  audio: {
    rainGain: number;
    ambient: string;
  };
  ui: {
    screen: Mode;
    resetMessage: string;
    endingMessage: string;
  };
}
```

## 2.3 Module specifics

| Module | Required exports/functions | Purpose | Used by |
| --- | --- | --- | --- |
| `main.ts` | `boot()`, `loop(now)`, `update(dt)`, `render()` | Owns fixed loop, global state, mode transitions. | All |
| `constants.ts` | `UNIT`, `SCALE`, `GRAVITY`, `CROUCH_HOP`, `TONGUE`, `WATER`, `CAT`, etc. | Single source for numbers. | All |
| `rng.ts` | `createRng(seed)`, `rng.next()`, `nextFloat()`, `nextInt()` | Deterministic randomness. | Insects, rain, hazards. |
| `input.ts` | `poll()`, `getState()`, `setDebugInput(partial)`, `clear()` | Normalizes keyboard/mouse into `InputState`. | Gameplay modules. |
| `state.ts` | `createState()`, `loadLevel(state, id)`, `setMode(state, mode)` | Creates and transitions global state. | Main, tests. |
| `levelLoader.ts` | `getLevel(id)`, `getSequence(sequence)` | Loads level records. | Main, tests. |
| `physics.ts` | `integrate(frog, dt)`, `resolveSurfaceCollision(frog, surfaces)`, `raycast(origin, dir, maxLen, blockers)` | Core collision and raycasts. | Crouch-hop, tongue, walls, water, hazards. |
| `camera.ts` | `updateCamera(state, dt)` | Follows frog, vertical scroll, keeps pond visible. | Render. |
| `crouchHop.ts` | `update(frog, input, world, dt)`, `launch(frog, input, world)`, `getCharge(frog)` | Tier 1 crouch-hop rule. | Frog, tests. |
| `tongue.ts` | `update(frog, input, world, dt)`, `startTongue(frog, input)`, `extendTongue(...)`, `tryCatch(...)`, `attach(...)`, `detach(...)`, `getState()` | Tier 1 tongue rule. | Frog, tests. |
| `anchors.ts` | `getRayTargets(world, origin, dir, maxLen)`, `isAnchorValid(anchor)`, `applyWeakBreak(anchor, frog, dt)` | Anchor definitions and weak break rules. | Tongue, render. |
| `walls.ts` | `update(frog, input, world, dt)`, `isClimbable(surface)`, `getState()` | Tier 1 sticky climbing/sliding. | Frog, tests. |
| `water.ts` | `update(frog, world, dt)`, `enterWater(frog, water)`, `exitWater(frog, edge)`, `applyCurrents(frog, world)`, `getState()` | Tier 1 water recovery. | Frog, tests. |
| `cat.ts` | `update(state, dt)`, `canSee(frog, cat, world)`, `getState()` | Tier 1 avoidance/stillness. | Frog, render, tests. |
| `heron.ts` | `update(state, dt)`, `applyShadow(...)`, `distract(...)`, `getState()` | Tier 2 heron hazard. | Level 4, render, tests. |
| `fish.ts` | `update(state, dt)`, `getState()` | Tier 2 fish hazard. | Level 4, tests. |
| `sprinkler.ts` | `update(state, dt)`, `startManual(state, sprinkler)`, `getState()` | Tier 2 sprinkler hazard/consequence. | Level 3, tests. |
| `wind.ts` | `update(state, dt)`, `applyWind(frog, world, dt)`, `getState()` | Tier 2 wind hazard. | Level 5, tests. |
| `interactables.ts` | `update(state, dt)`, `applyEffect(state, interactable)`, `getState()` | Tier 2 physical pull. | Levels 3–4, tests. |
| `insects.ts` | `update(state, dt)`, `eat(frog, insect)`, `getState()` | Tier 3 eating reactions. | Tongue, render, tests. |
| `frog.ts` | `update(state, dt)`, `resetToLastSafePerch(state, cause)`, `hazardReset(state, target, cause)` | Orchestrates frog states and reset. | Main, tests. |
| `render.ts` | `draw(state)`, `drawWorld(...)`, `drawEntities(...)`, `drawWeather(...)` | Canvas visual rules. | Main. |
| `audio.ts` | `play(name, params)`, `setRainGain(gain)`, `startAmbient(track)` | Synthesized audio. | Gameplay events. |
| `ui.ts` | `setScreen(mode)`, `showReset(cause)`, `showEnding()`, `hideAll()` | HTML/CSS overlay state. | Main, tests. |
| `debug.ts` | See Section 8. | Direct access for tests. | Tests. |

---

# 3. VISUAL SPEC

The look is a quiet, wet, frog-scale world drawn with soft vector silhouettes and subtle wet highlights. The camera stays low, as if the viewer is also small. Rain is visible but not noisy. Surfaces are readable by texture and shine: a slippery tile has a cold specular streak, a sticky tile has a damp matte grip, a branch has a brown bridge silhouette, a safe perch has a soft green glow. The distant rooftop pond is always suggested by a pale moonlit shape in the far background when the camera is low enough. There are no UI counters, no abstract icons, and no map.

## Lighting and atmosphere

- Time is night after rain.
- Primary light: moonlight from upper right, cool #d8e8ff at 12% opacity.
- Secondary light: warm window spill from off-screen, amber #d9a86b at 6% opacity.
- Wet surfaces have short specular highlights and slight reflection.
- Rain particles are sparse, vertical with wind drift, 0.35 alpha.
- Drips fall from edges and create tiny ripple rings.
- Fog is very low: 4–8% dark blue haze on far layers.
- Danger cues are readable through light and silhouette, not flashing combat UI.

## Space

- The camera follows the frog with a horizontal deadzone of 30 units and vertical deadzone of 20 units.
- Vertical lookahead is 18 units above the frog when moving up.
- Camera clamps to level bounds.
- Far background layers keep the rooftop pond visible whenever the camera y is below 650 units.
- Parallax factors: sky/pond 0.08, far city 0.15, mid garden 0.35, gameplay 1.0, foreground rain 1.15.

## Palette

| Role | Hex | Use |
| --- | --- | --- |
| SkyNight | `#071018` | Base sky. |
| FarCity | `#0d1824` | Distant rooftops. |
| MidSilhouette | `#11202c` | Trees, fences, barrels. |
| WetSurface | `#1c2b36` | Wet stone, crates, gutters. |
| WetHighlight | `#6d93a8` | Specular streaks. |
| Moss | `#2f5d3a` | Mossy stone, vines. |
| Leaf | `#3a7a4a` | Leaves, lilies. |
| Wood | `#4a3a2c` | Fence rails, crates. |
| Metal | `#56626c` | Drainpipes, tin cans. |
| Glass | `#66aabf` at 22% | Greenhouse glass. |
| Water | `#123044` at 60% | Ponds, rain barrels. |
| PuddleReflect | `#4a7d99` | Puddle reflections. |
| Moonlight | `#d8e8ff` | Rim light, pond glow. |
| SafePerch | `#79d0b0` | Safe perch glow. |
| Anchor | `#d7b56d` | Visible grabbable anchors. |
| DangerCat | `#b04c4c` | Cat eyes, attention cue. |
| DangerHeron | `#8996a8` | Heron shadow. |
| DangerFish | `#6d8ba0` | Fish bubbles. |
| Rain | `#8fa8bd` at 35% | Rain particles. |
| UI | `#cfe3f5` | Minimal text. |

## Visual recipe table

| Layer | Draw recipe | Visual rule |
| --- | --- | --- |
| Sky/pond | Flat dark gradient; moon circle radius 18; rooftop pond silhouette with lily rings. | Keeps the goal as a distant quiet shape. |
| Far city | Simple rectangles, no detail, parallax 0.15. | Reads as scale, not gameplay. |
| Mid garden | Barrel/crate/fence silhouettes, parallax 0.35. | Never occludes gameplay anchors. |
| Gameplay surfaces | Rounded rectangles for platforms; thin highlight strips for wet surfaces; matte texture for sticky/climbable surfaces. | Friction and climbability are visible. |
| Smooth glass | Blue translucent rectangles, no outline, no anchor glint. | Tongue cannot stick. |
| Water | Dark translucent rectangles, animated ripple lines, current arrows. | Open water cannot be tongue-stuck. |
| Anchors | Small shapes plus 3-unit gold outline, pulse 1.2 Hz. | Only visible anchors are valid. |
| Weak anchors | Same outline with tiny crack marks. | Player can read risk. |
| Safe perch | Soft green glow, radius 18, pulse 1.0 Hz. | Goal of a run. |
| Goal lily | Lily circle radius 14, moonlight rim, subtle frog chorus ripple. | Final goal. |
| Frog | Low oval body, short legs, large eyes, throat swell, no tools. | Not a human in a frog suit. |
| Cat | Large silhouette, two red eye points, slow step animation. | Cat is a disaster, not an enemy. |
| Heron | Tall still silhouette; shadow rectangle spreads under it. | Open ground becomes dangerous. |
| Fish | Small dark shape; bubble ring telegraph. | Water hazard is readable. |
| Sprinkler | Small metal nozzle; arc of droplets when active. | Physical consequence. |
| Wind | Thin horizontal streaks, speed tied to force. | Changes hop arc. |
| Rain | 120 max particles, 1–2 px lines, fall 900 units/s. | Atmosphere, not gameplay. |
| Drips | Point particles from surface edges, ripple on impact. | Teaches wetness. |

---

# 4. GAMEPLAY SPEC

The game is a quiet traversal platformer. The player is a small frog trying to reach a moonlit rooftop pond. There is no combat and no score. The player reads scenes as a frog would: find a route upward, use the tongue only on visible grabbable anchors, respect wet and slippery surfaces, wait out animals, and use small physical consequences. Failure is forgiving: the frog slips, lands in water, gets batted away, or is carried off, but the result is delay and embarrassment, not death.

## 4.0 Records and rosters

The game has exactly these gameplay object kinds.

| Record | Roster | Tier | Counter? |
| --- | --- | --- | --- |
| Frog | One player frog. | 1 | No. |
| Surfaces | wetLeaf, rainBarrelRim, drainpipeInterior, wetCrate, stickyTile, mossyStone, woodenFenceRail, stonePath, wetTile, greenhouseGlass, condensationFrame, drippingVine, lilyPad, tinCan, gardenHose, crumblingLedge, safePerchSurface, goalLily. | 1 for basic surfaces; 2 for glass, crumbling, vines, lilies. | No. |
| Anchors | branch, twig, hangingWire, bottleCap, spiderSilk, insectLeg, crackedTileEdge, drippingVineAnchor. | 1 for basic anchors; 2 for weak/vine. | No. |
| Water volumes | puddle, rain barrel, drain, koi pond, rooftop pond. | 1 basic water; 2 koi/current. | No. |
| Currents | pipe current, pond current, water-carried leaf. | 2. | No. |
| Safe perch | One per level, except final goal. | 1. | No. |
| Goal perch | Rooftop moonlit lily. | 1. | No. |
| Hazards | cat, heron, fish, sprinkler, wind, rain barrel tip. | Cat 1; others 2. | No. |
| Interactables | cork, sprinklerValve, branchDisturb. | 2. | No. |
| Insects | fly, wasp, beetle. | 3. | No. |
| Pickups | None. | N/A | No. |

## 4.1 Crouch-hop — Tier 1

Crouch-hop is the primary movement verb. The frog does not run. Movement comes from coiling, aiming, and releasing.

| Rule | Number |
| --- | ---: |
| Input | Hold `Space` while grounded. Release to launch. |
| Min charge | 0.05 s. |
| Max charge | 0.50 s. |
| Launch speed | `180 + 300 * charge / 0.50`, max 480. |
| Horizontal aim | If move input is held, `vx = move * min(210, 0.45 * speed)`. |
| Vertical aim | If move input is held, `vy = -0.82 * speed`. If no move input, `vy = -0.95 * speed`. |
| Air control | None. Move input is ignored after launch. |
| Mid-air jump | None. |
| Coyote time | None. |
| Jump buffering | None. |
| Full hop height | About 104 units straight up, about 78 units with horizontal aim. |
| Full horizontal distance | About 165 units with max horizontal cap. |
| First tutorial gap | 45 units horizontal, 10 units vertical. |
| Opening max gap | 60 units. |
| Later max gap | Up to 160 units with tongue assistance. |

Landing behavior:

| Surface | Landing effect |
| --- | --- |
| Any grounded surface | Frog enters `grounded`. |
| If landing on low-friction surface and `abs(vel.x) > 120` | Frog enters `sliding` for 0.50 s with surface friction. |
| If landing in water | Frog enters `water` if water depth > 4. |
| If landing on leaf | Leaf rocks; frog receives 30% of leaf impulse. |

## 4.2 Tongue — Tier 1

The tongue is the main traversal verb. It is not a magic rope.

| Rule | Number |
| --- | ---: |
| Input | Hold mouse button or `J`. Aim with mouse pointer or keyboard aim vector. |
| Max length | 150 units. |
| Extension speed | 1800 units/s. |
| Retract speed | 2400 units/s. |
| Ray width | 4 units. |
| Anchor hit radius | 6 units. |
| Target priority | Nearest valid target along ray: insect or anchor. Solid surfaces block. |
| Insect catch | Eat immediately, no attachment. |
| Anchor catch | Enter `attached`. Rope length = clamp(distance, 25, 150). |
| Swing input | While attached, move input applies tangential acceleration 260 units/s². |
| Release | Detach and keep velocity. |
| Miss | Tongue extends to max, then retracts. `missTimer = 0.25` s. No re-fire during miss. |
| Cannot stick | Smooth glass, open water, invisible surfaces, broken anchors. |
| Air use | Allowed when airborne or wall-clinging. |
| Water use | Disabled. |
| Attached movement | Crouch-hop disabled; only pendulum and pump. |

Anchor roster:

| Anchor type | Valid | Break time | Break speed | Slip amount | Notes |
| --- | --- | ---: | ---: | ---: | --- |
| branch | yes | none | none | 0 | Strong bridge. |
| twig | weak | 1.2 s | 420 | 0 | Small. |
| hangingWire | strong | none | none | 0 | Fixed wire. |
| bottleCap | weak | 1.0 s | 360 | 12 | May slip downward. |
| spiderSilk | weak | 0.7 s | 260 | 18 | Stretches, breaks fast. |
| insectLeg | weak | 0.8 s | 300 | 0 | Target may twitch. |
| crackedTileEdge | weak | 1.5 s | 500 | 0 | Near glass/tile edges. |
| drippingVineAnchor | strong | none | none | 0 | Vine can be climbed too. |

Weak object behavior:

- If `attachedTime > breakTime` or `speed > breakSpeed`, the anchor breaks.
- On break, the frog receives a small recoil away from the anchor: 60 units/s.
- Slip amount increases rope length while attached, causing unexpected sag.
- A missed tongue leaves the frog with an extended tongue for 0.25 s; physics continues, producing a dangle before falling.

## 4.3 Sticky climbing and sliding — Tier 1

Walls are surfaces to cling to, not platforms.

| Rule | Number |
| --- | --- |
| Input | Hold movement input into a damp climbable wall. |
| Climbable wall types | stickyTile, mossyStone, woodenFenceRail, drippingVine. |
| Non-climbable walls | greenhouseGlass, condensationFrame, drainpipeInterior, wetCrate, rainBarrelRim. |
| State entry | Frog overlaps wall and holds into it. |
| State exit | Frog moves away from wall, tongue attaches, or reaches top. |
| Climb up speed | 140 units/s. |
| Hold speed | 0 on climbable wall. |
| Slide down speed | 200 units/s on wet non-climb walls; 140 units/s if no input on climbable wall after 0.8 s fatigue-free hold is allowed. |
| Wall jump | None. |
| Wall crouch-hop | None. |
| Tongue from wall | Allowed. |

Surface grip table:

| Surface | Friction | Climbable | Tongue sticky | Notes |
| --- | ---: | --- | --- | --- |
| wetLeaf | 0.25 | no | no | Rocks when hit. |
| rainBarrelRim | 0.18 | no | no | Very slippery. |
| drainpipeInterior | 0.12 | no | no | Slides. |
| wetCrate | 0.35 | no | no | Path. |
| stickyTile | 0.80 | yes | no | Climbable. |
| mossyStone | 0.70 | yes | no | Damp climb. |
| woodenFenceRail | 0.60 | yes | no | Climbable rail. |
| stonePath | 0.55 | no | no | Ground. |
| wetTile | 0.20 | no | no | Slide hazard. |
| greenhouseGlass | 0.02 | no | no | Cannot stick. |
| condensationFrame | 0.05 | no | no | Slippery frame. |
| drippingVine | 0.70 | yes | yes | Climb and anchor. |
| lilyPad | 0.30 | no | no | Floating platform. |
| tinCan | 0.40 | no | no | Frog-scale landmark. |
| gardenHose | 0.50 | no | no | Ramp/slide landmark. |
| crumblingLedge | 0.50 until broken | no | no | Breaks. |
| safePerchSurface | 0.80 | no | no | Completion. |
| goalLily | 0.80 | no | no | Final completion. |

## 4.4 Wet-surface movement and water recovery — Tier 1

The frog’s body is light, slippery, and easily moved.

Ground movement:

- While grounded, the frog does not run. Horizontal velocity comes from hops, slides, currents, wind, and tongue.
- Ground friction applies deceleration: `friction * 1200 units/s²`.
- Low-friction surfaces with `friction < 0.25` produce slides when landing fast.

Leaf rock:

| Event | Number |
| --- | ---: |
| Drop hits leaf | Every 3.0–5.0 s in tutorial; first at 1.2 s. |
| Leaf impulse | ±120 horizontal, ±30 vertical. |
| Frog impulse if on leaf | 30% of leaf impulse. |
| Duration | 0.40 s. |

Water:

| Rule | Number |
| --- | ---: |
| Shallow puddle depth | ≤ 4 units: ground surface, slippery. |
| Deep water depth | > 4 units: `water` state. |
| Water gravity | 150 units/s². |
| Buoyancy upward | 260 units/s² when submerged. |
| Swim acceleration | 180 units/s². |
| Swim max speed | 100 units/s. |
| Swim drag | 1.2/s. |
| Dive input | Down gives 140 units/s². |
| Surface clamp | Frog cannot go above water top without exiting. |
| Current force | Velocity blend toward current at strength 0.8/s. |
| Edge detection | Frog overlaps edge surface and is within 12 units of water boundary. |
| Haul out | Hold crouch at edge for 0.20 s, release: impulse x = edge normal × 220, y = -260. |
| Water use of tongue | Disabled. |
| Water use of crouch-hop | Only at edges. |

Puddles as platforms:

- Shallow puddles are slippery ground.
- Floating leaves inside puddles are `wetLeaf` platforms.
- A bad hop into a shallow puddle causes a slide.
- A bad hop into deep water causes water recovery.

## 4.5 Avoidance and stillness — Tier 1

The cat is a disaster. The player avoids it by stillness, timing, and observation.

Cat detection:

| Rule | Number |
| --- | ---: |
| Detection range | 350 units. |
| Detection cone | 120° centered on cat facing. |
| Occluded by | Opaque surfaces, not glass. |
| Frog moving threshold | speed > 18 units/s. |
| Attention gain while visible and moving | +18/s. |
| Attention change while visible and still | -6/s. |
| Attention change while hidden | -25/s. |
| Attention max | 100. |
| Step closer threshold | 50. |
| Crouched threshold | 80. |
| Strike threshold | 100. |
| Strike telegraph | 0.70 s. |
| Strike lunge distance | 180 units. |
| Hit box | 30 × 25 units around cat front. |
| Max steps closer | 2. |
| Step closer distance | 100 units toward last known frog position. |
| Reset on hit | Last safe perch. |

Cat states:

| State | Behavior |
| --- | --- |
| watching | Eyes follow frog. Attention rises if frog moves. |
| approaching | Cat steps closer. Attention resets to 35 after step. |
| crouched | Cat crouches. Eyes brighter. |
| strike | Telegraph, lunge, then if hit, reset. If miss, attention = 60. |

Stillness:

- The frog can stand still on safe ground.
- The frog can hold on a wall or branch without raising attention unless it is visible and moving.
- The game does not tell the player “don’t move”; the cat’s eyes and steps teach it.

## 4.6 Forgiving failure and reset — Tier 1

Failure never becomes death.

| Failure | Result |
| --- | --- |
| Slide off wet tile | Frog slides and falls. |
| Land in shallow puddle | Frog gets slippery. |
| Land in deep water | Frog swims awkwardly and hauls out. |
| Miss tongue | Frog drops after 0.25 s dangle. |
| Weak anchor breaks | Frog drops with small recoil. |
| Cat swat | Bat animation, reset to last safe perch. |
| Fall out of bounds | Splash/dust, reset to last safe perch. |
| Heron snap | Dark swallow, coughed up nearby. |
| Fish snap | Splash, placed at nearest water edge. |
| Current carries frog | Frog is carried, then can swim to edge. |
| Wind changes hop | Frog lands somewhere else; no instant reset unless out of bounds. |

Reset sequence:

| Phase | Number |
| --- | ---: |
| Embarrassment animation | 0.50 s. |
| Input disabled | 1.20 s total. |
| Place at target | `lastSafePerch` or hazard target. |
| Velocity | zero. |
| State | `grounded` if target is safe, else `water` if target is water. |
| Hazard state | Cat, heron, fish reset to initial patrol. Interactable effects persist. |

Embarrassment language:

- No “Game Over.”
- No score.
- Text is optional and quiet: `Slipped.`, `The cat saw you.`, `The branch gave way.`
- The frog slumps, puffs, and then resumes.

## 4.7 Combined traversal — Tier 2

After the opening phase, levels require combinations of existing verbs. No new mechanics are added.

Required combined sequences:

| Level | Required combined traversal |
| --- | --- |
| L3 | Enter rain barrel through broken window → climb sticky tiles inside barrel → exit through drain → outside branch swing. |
| L4 | Pull cork → current carries leaf into place → use leaf as platform → avoid fish/current → distract heron or wait. |
| L5 | Anchor with tongue before hopping through wind → swing between branches → land on lily goal. |

Combined traversal rules:

- A rain barrel can be entered through a broken window opening 16 × 12 units.
- Inside barrel height: 90 units.
- Sticky tile climb height: 70 units.
- Drain exit: 18 × 10 units.
- Outside branch anchor: branch type, radius 8.
- Player must use crouch-hop, sticky climb, tongue, and observation together.

## 4.8 Hazard escalation and distraction — Tier 2

Hazard escalation adds readable animals and weather. The player avoids, distracts, or slips past them.

### Heron — Tier 2

| Rule | Number |
| --- | ---: |
| Patrol path | Along top of pond area, speed 40 units/s. |
| Shadow rectangle | 140 × 90 units under heron. |
| Frog in shadow threshold | speed > 10 units/s. |
| Attention gain | +25/s. |
| Strike threshold | 100. |
| Strike telegraph | 0.50 s. |
| Strike hit radius | 30 units. |
| Catch result | Dark swallow 0.80 s; place at nearest safe perch within 120 units, else last safe perch. |
| Distraction | Pull branch within 40 units. |
| Distraction duration | 4.0 s. |
| During distraction | Shadow leaves open ground; attention resets. |

### Fish — Tier 2

| Rule | Number |
| --- | ---: |
| Patrol speed | 30 units/s. |
| Detection radius | 45 units in water. |
| Telegraph | 0.35 s bubble ring. |
| Snap radius | 22 units. |
| Catch result | Splash, place at nearest water edge. |

### Sprinkler — Tier 2

| Rule | Number |
| --- | ---: |
| Auto interval | 20.0 s. |
| Auto on time | 6.0 s. |
| Manual start | Pull valve 1.2 s. |
| Manual on time | 10.0 s. |
| Spray radius | 120 units. |
| Surface effect | Friction becomes 0.05 while on. |
| Caterpillar effect | After 1.5 s spray, caterpillar is knocked off; branch dips down 30 units permanently. |
| Warning | 0.50 s hiss before auto start. |

### Wind — Tier 2

| Rule | Number |
| --- | ---: |
| Zone force | 180 units/s² horizontal. |
| Direction change | Every 8.0–12.0 s. |
| Build time | 1.0 s. |
| Affected states | `airborne`, `attached` at 40% force. |
| Visual | Horizontal streaks. |
| Design intent | Player must use tongue anchor before hopping. |

### Rain barrel tip — Tier 2

| Rule | Number |
| --- | ---: |
| Trigger | Landing impulse > 300 units/s or center offset > 8 units for 1.0 s. |
| Tip duration | 1.2 s. |
| Result | Water dumps; frog slides into water or reset. |

### Crumbling ledge — Tier 2

| Rule | Number |
| --- | ---: |
| Crack timer | 0.50 s after standing. |
| Break timer | 1.20 s after standing. |
| Respawn | 8.0 s. |
| Visual | Cracks spread. |

### Slippery glass — Tier 2

| Rule | Number |
| --- | ---: |
| Friction | 0.02. |
| Tongue | Cannot stick. |
| Climb | Cannot climb. |
| Condensation frame friction | 0.05. |

## 4.9 Environmental consequences — Tier 2

The world has no locked doors or abstract switches. It has physical objects.

Interactable roster:

| Type | Input | Hold time | Effect |
| --- | --- | ---: | --- |
| cork | `E` near cork | 1.5 s | Removes cork, enables pipe current for 15 s, current carries leaf to platform after 4.0 s. |
| sprinklerValve | `E` near valve | 1.2 s | Starts sprinkler for 10 s; knocks caterpillar off branch; branch dips 30 units permanently. |
| branchDisturb | `E` near branch | 0.8 s | Branch vibrates; heron distracted 4.0 s; may knock beetle off. |

Rules:

- Interaction radius: 20 units.
- The player must be close, not just aiming.
- Effects persist until the level goal.
- Hazards reset after frog reset, but environmental changes stay.
- No switch UI. The objects are drawn as physical parts.

## 4.10 Route variety — Tier 2

Each later level has a direct dangerous route and a longer safer route.

| Level | Direct dangerous route | Longer safer route |
| --- | --- | --- |
| L3 | Tongue chain across greenhouse glass using weak anchors and condensation frames. | Climb mossy stone and dripping vines, wait out sprinkler, use dipped branch. |
| L4 | Hop across lily pads under heron shadow while fish patrol. | Pull cork to bring leaf into safe place, climb drain wall, wait for shadow, distract heron. |
| L5 | Chain tongue swings across wind gap. | Anchor, wait for wind to calm, climb gutter, cross lower lily path. |

Route rules:

- Both routes must be reachable with tier 1 or tier 2 mechanics.
- Direct routes are shorter but use weak anchors, hazards, or precise timing.
- Longer routes use observation, stillness, and environmental consequences.
- No route is hidden behind a locked door or key.

## 4.11 Eating reactions — Tier 3

Eating is ecology and feedback, not progress.

| Insect | Catch result | Reaction |
| --- | --- | --- |
| fly | Tongue catches, swallow. | Sneeze: impulse x = -facing × 140, y = -90, duration 0.25 s. |
| wasp | Tongue catches, swallow. | Hiccup/puff: after 0.30 s impulse x = ±180 random, y = -160, duration 0.40 s. |
| beetle | Tongue catches, swallow. | No gameplay effect. Small burp animation. |

Rules:

- No inventory.
- No counter.
- No score.
- Eating cannot unlock routes.
- Reactions are physical and can slightly alter the next hop.

## 4.12 Progression and difficulty

### Level sequence

| Level | Tier | Name | Size units | Start | Goal | New mechanics |
| --- | --- | --- | ---: | --- | --- | --- |
| M1/L1 | 1 | Rain Barrel Leaf | 180 × 140 | leaf (35,105) | drainpipe lip (150,70) | leaf rock, crouch-hop, slippery rim, water. |
| M2/L2 | 1 | Drainpipe, Wet Crates, Branch, Gutter, Stone Path, Cat | 260 × 220 | drain exit (20,185) | greenhouse eave (235,85) | wet crates, sticky tile, branch swing, cat watching. |
| M3 | 1 | Rooftop Pond simplified | 300 × 260 | drain outlet (20,220) | central lily (260,120) | final pond, lily platforms, no wind/heron/fish. |
| L3 | 2 | Greenhouse Glass and Dripping Vines | 320 × 300 | eave (20,240) | koi edge (290,220) | glass, vines, weak anchors, crumbling ledge, sprinkler, caterpillar, rain barrel combined traversal. |
| L4 | 2 | Koi Pond and Lily Pads | 340 × 280 | pond edge (20,220) | rooftop drain (320,120) | heron, fish, currents, cork, leaf, insect legs. |
| L5 | 2 | Rooftop Pond | 380 × 320 | drain outlet (20,260) | central lily (320,120) | wind, lilies, final chorus. |

### Difficulty curve

| Phase | Levels | Max gap | Vertical rise | Hazards | Player expectation |
| --- | --- | ---: | ---: | --- | --- |
| Opening | L1–L2 | 60 units direct, 160 with branch | 80 units | slippery, water, one cat | Read one anchor at a time. |
| Middle | L3 | 180 units | 160 units | weak anchors, glass, sprinkler, crumbling | Combine climb, tongue, timing. |
| Deep garden | L4 | 180 units | 180 units | fish, heron, current, open water | Wait, distract, use consequences. |
| Rooftop | L5 | 200 units | 200 units | wind, water | Anchor before commitment. |

### Legibility rules

- Tutorial anchors have stronger outlines for the first 2 levels.
- First three levels have no hidden anchors.
- Weak anchors are visually cracked.
- Slippery surfaces always show specular streaks.
- Safe perches glow.
- The distant pond is visible in the far background whenever possible.

## 4.13 Runs and level structure

A run is one traversal from a start or last safe perch to the next safe perch.

| Rule | Number |
| --- | ---: |
| Start trigger | Frog wakes on leaf in L1. |
| Reset trigger | Placed at last safe perch. |
| Run end | Frog touches safe perch radius 12. |
| Goal end | Frog touches final lily radius 14. |
| Level transition | 1.5 s quiet fade, then load next level. |
| Ending | 3.0 s chorus, then end screen. |
| Reset on hazard | See 4.6. |
| Save | None. |

---

# 5. CHARACTERS

## 5.1 Silhouettes

- Frog: low, wide, wet. No tools, no clothing, no weapon. Short legs. Bulging eyes follow threats. Throat swells when nervous.
- Cat: large domestic silhouette, low enough to feel like a monster at frog scale. Eyes are two red points.
- Heron: tall, still, leggy. Danger is mostly its shadow.
- Fish: small dark shape in water, readable by bubbles and snap.
- Insects: tiny, simple, not cute enough to be collectibles.

## 5.2 Frog states and animations

| State | Animation | Motion rule | Facing |
| --- | --- | --- | --- |
| grounded idle | `idle_breathe` | Slow throat pulse, occasional blink, eyes follow nearest animal. | Last move input. |
| crouch coil | `crouch_coil` | Legs compress, body lowers, charge visual grows. | Current facing. |
| airborne | `airborne_arc` | Legs tuck then extend, body rotates slightly with velocity. | Lock at launch. |
| sliding | `slide_wet` | Body skids, pads smear, small spray. | Velocity direction. |
| wall cling | `wall_cling` | Pads spread, body sticks, slow climb. | Facing wall. |
| wall slide | `wall_slide` | Pads smear downward, water streaks. | Facing wall. |
| tongue extend | `tongue_extend` | Tongue line extends, mouth opens. | Aim direction. |
| tongue miss | `tongue_miss` | Tongue droops, frog dangles, small shake. | Aim direction. |
| tongue attached | `tongue_swing` | Body hangs, legs dangle, eyes look forward. | Aim direction. |
| water float | `water_float` | Belly low, paddles awkwardly, ripples. | Move input or current. |
| water edge haul | `water_haul` | Push-up, water falls off. | Edge normal. |
| cat noticed | `cat_attention` | Throat swells, eyes widen, body stills. | Toward cat. |
| embarrassed reset | `embarrassed` | Slump, puff, tiny shake, then reset. | Neutral. |
| heron swallowed | `dark_swallow` | Screen darkens, frog silhouette, cough. | Neutral. |
| fish snap | `fish_snap` | Splash, disoriented shake. | Neutral. |
| fly sneeze | `fly_sneeze` | Head jerk, small impulse. | Facing. |
| wasp hiccup | `wasp_hiccup` | Puff, sideways jig. | Random. |
| ending rest | `ending_rest` | Sit on lily, throat pulses, chorus ripple. | Toward pond. |

## 5.3 Animal states

| Animal | States | Visual cue |
| --- | --- | --- |
| Cat | watching, approaching, crouched, strike | Eyes follow, step, crouch, lunge. |
| Heron | patrol, shadow, distracted, strike | Shadow grows, head turns, snap. |
| Fish | patrol, telegraph, snap | Bubble ring, water bulge. |
| Insects | ambient, eaten | Small flight paths, swallow. |

---

# 6. AUDIO

All audio is synthesized. No recorded samples.

| Name | Recipe | When it plays |
| --- | --- | --- |
| rain_loop | Pink noise through bandpass 200–1200 Hz, gain 0.18, slow LFO ±0.02. | Ambient in outdoor levels. |
| rain_indoor | Lowpass 600 Hz, gain 0.08. | Inside rain barrel/greenhouse. |
| drip | Sine 900 Hz to 300 Hz, 15 ms, exponential decay. | Drips hit surfaces. |
| puddle_ripple | Sine 500 Hz to 200 Hz + noise burst 1–2 kHz, 80 ms. | Frog lands in shallow puddle. |
| gurgle | Bandpass noise 100–400 Hz, random bursts, gain 0.12. | Drainpipe/barrel. |
| water_enter | White noise 500–3000 Hz, 120 ms, lowpass sweep. | Frog enters water. |
| swim | Short filtered noise pulses 100–300 Hz, 80 ms intervals. | Paddling. |
| current | Lowpass noise 100–300 Hz, sustained, gain tied to current strength. | Current active. |
| crouch | Sine 80–120 Hz, gain rises with charge. | Holding crouch. |
| hop | Sine 220 Hz to 120 Hz, 80 ms, noise click. | Crouch-hop release. |
| land | Noise 200–600 Hz, 30 ms. | Ground landing. |
| slide | Filtered noise 300–900 Hz, 200 ms. | Sliding on wet surface. |
| tongue | Noise 1200–3000 Hz, 20 ms, highpass. | Tongue extends. |
| tongue_miss | Noise 600–1000 Hz, 30 ms. | Tongue grabs nothing. |
| tongue_catch | Sine click 1000 Hz, 10 ms. | Tongue catches anchor. |
| swing_air | Gentle whoosh noise 300–900 Hz, gain tied to tangential speed. | Swinging fast. |
| anchor_break | Noise 800–2500 Hz, 50 ms. | Weak anchor breaks. |
| wall_cling | Friction noise 300–800 Hz, 60 ms. | Frog sticks to wall. |
| wall_slide | Filtered noise 200–500 Hz, continuous while sliding. | Wall slide. |
| safe_perch | Soft sine bell 660/880 Hz, 300 ms, low gain. | Reaching safe perch. |
| goal_chorus | Three sine warbles 160/210/240 Hz, 1.2 s, chorus. | Final lily reached. |
| cat_step | Soft noise 100–200 Hz, 40 ms. | Cat steps closer. |
| cat_eye | Quiet low click 300 Hz, 10 ms. | Cat attention crosses 50. |
| cat_swat | Slap noise 300–1500 Hz, 120 ms. | Cat hits frog. |
| heron_shadow | Low whoosh noise 200–800 Hz, 300 ms. | Shadow enters open ground. |
| heron_snap | Sharp click 800–2000 Hz, 30 ms. | Heron strikes. |
| fish_bubble | Sine 400–700 Hz, 60 ms. | Fish telegraph. |
| fish_snap | Click 600–1800 Hz, 30 ms. | Fish snaps. |
| sprinkler_start | Hiss noise 800–4000 Hz, 300 ms. | Sprinkler starts. |
| sprinkler_loop | Filtered noise 1000–4000 Hz, gain 0.12. | Sprinkler on. |
| wind_loop | Noise 200–1200 Hz, LFO, gain tied to force. | Wind active. |
| leaf_rock | Soft wood/leaf knock 150–300 Hz, 50 ms. | Drop hits leaf. |
| fly_sneeze | Pop sine 400–100 Hz + noise, 80 ms. | Eating fly reaction. |
| wasp_hiccup | Low thump 120 Hz + pop, 120 ms. | Eating wasp reaction. |
| beetle_burp | Tiny sine 220 Hz, 30 ms. | Eating beetle flavor. |
| reset_oof | Muffled low tone 180 Hz, 100 ms. | Embarrassment reset. |

---

# 7. UX

UI screens are HTML/CSS only. The game world is Canvas. There are no numeric HUDs.

## 7.1 Screen state machine

```txt
BOOT
  -> TITLE

TITLE
  Start button / Enter -> LEVEL_START

LEVEL_START
  1.2s quiet fade -> PLAYING

PLAYING
  Escape -> PAUSED
  Reach safe perch -> LEVEL_START(next)
  Reach final goal -> ENDING
  Hazard reset -> EMBARRASSMENT

EMBARRASSMENT
  1.2s delay -> PLAYING at safe perch

PAUSED
  Resume -> PLAYING
  Quit -> TITLE

ENDING
  Continue -> TITLE
```

## 7.2 Screens

| Screen | Content | Input |
| --- | --- | --- |
| TITLE | Game name, `Start`, brief controls. | Enter or click. |
| LEVEL_START | Quiet place name only. No map, no objectives. | None. |
| PLAYING | Canvas only. | Game controls. |
| PAUSED | `Paused`, `Resume`, `Quit`. | Escape, Enter. |
| EMBARRASSMENT | Very short quiet text: `Slipped.`, `The cat saw you.`, `The branch gave way.` | None. Auto-dismiss. |
| ENDING | `The pond is here.` No score. | Continue. |

## 7.3 HUD table

There is no numeric HUD. These are diegetic on-screen markers.

| Element | Record field | When visible |
| --- | --- | --- |
| Safe perch glow | `level.safePerch.pos`, `reached` | While level active, until reached. |
| Goal lily glow | `level.goal.pos` | Final level only. |
| Anchor outline | `anchors.visible`, `validForTongue`, `broken` | When anchor is in view and not broken. |
| Weak anchor cracks | `anchors.breakTime > 0` | Weak anchors only. |
| Wet surface shine | `surface.friction < 0.25` | Slippery surfaces. |
| Climbable wall matte | `surface.climbable` | Damp climbable walls. |
| Glass no-stick tint | `surface.type == greenhouseGlass` | Greenhouse glass. |
| Water current arrows | `currents.active` | Currents. |
| Cat eye cue | `hazard.attention > 0` | Cat present. |
| Heron shadow | `hazard.shadowRect` | Heron present. |
| Fish bubble telegraph | `hazard.telegraphTimer > 0` | Fish present. |
| Wind streaks | `hazard.state == blowing` | Wind zones. |
| Reset message | `ui.resetMessage` | During embarrassment reset only. |

---

# 8. DEBUG API

The debug API is exposed as `window.__frogDebug` and also importable in tests.

| System | Function | Returns |
| --- | --- | --- |
| mode | `debug.getMode()` | `GameState.mode`, `levelIndex`. |
| input | `debug.input.setMove(-1|0|1)` | Sets move input. |
| input | `debug.input.setCrouchHeld(bool)` | Sets crouch hold. |
| input | `debug.input.releaseCrouch()` | Triggers release. |
| input | `debug.input.setTongueAim(x, y)` | Sets aim vector. |
| input | `debug.input.setTongueHeld(bool)` | Sets tongue hold. |
| input | `debug.input.setInteractHeld(bool)` | Sets pull input. |
| crouch-hop | `debug.crouchHop.getCharge()` | `charge`, `state`, `vel`. |
| tongue | `debug.tongue.getState()` | `active`, `targetId`, `length`, `missTimer`, attached state. |
| anchors | `debug.anchors.list()` | Current level anchors. |
| walls | `debug.walls.getState()` | `state`, `surfaceId`, `climbable`, `vel`. |
| water | `debug.water.getState()` | `inWater`, `depth`, `current`, `edgeId`. |
| cat | `debug.cat.getState()` | All cat hazards. |
| heron | `debug.heron.getState()` | All heron hazards. |
| fish | `debug.fish.getState()` | All fish hazards. |
| sprinkler | `debug.sprinkler.getState()` | Sprinkler states. |
| wind | `debug.wind.getState()` | Wind zones. |
| interactables | `debug.interactables.getState()` | Pull progress and effects. |
| insects | `debug.insects.getState()` | Insect positions and eaten flags. |
| frog | `debug.frog.getState()` | Full frog record. |
| level | `debug.level.getState()` | Current level record. |
| reset | `debug.reset.getState()` | Reset state and target. |
| rng | `debug.rng.getSeed()` | Seed. |

---

# 9. TESTS

Tests use the debug API and a deterministic seed.

## Tier 1 tests

| Test | Validation |
| --- | --- |
| Fixed step determinism | Same seed and inputs produce same positions after 300 steps. |
| Crouch-hop min/max | Min charge produces low hop; max charge produces capped velocity; no air control changes velocity after launch. |
| First gap traversal | Frog can clear 45 unit tutorial gap with correct charge. |
| Tongue catch branch | Aim at branch within 150 units attaches. |
| Tongue miss | Aim at empty space extends, retracts, `missTimer = 0.25`. |
| Tongue glass | Aim at glass does not attach. |
| Tongue water | Aim at open water does not attach. |
| Weak anchor break | Spider silk breaks after threshold or speed. |
| Sticky wall climb | Frog climbs stickyTile at 140 units/s. |
| Non-climb glass | Frog cannot enter wall state on glass. |
| Water entry | Frog entering deep water enters `water`. |
| Water edge haul | Frog can exit water with edge crouch-hold. |
| Current carry | Current moves frog toward current velocity. |
| Cat attention rising | Moving while visible raises attention. |
| Cat stillness | Stillness lowers attention. |
| Cat reset | Cat strike resets to last safe perch. |
| Safe perch | Touching safe perch loads next level. |
| No death | Falling out of bounds resets, never enters death mode. |
| No score | No score, inventory, or counter fields change. |

## Tier 2 tests

| Test | Validation |
| --- | --- |
| Combined traversal | L3 can be completed only by broken window → sticky tile → drain → branch sequence or equivalent combined route. |
| Heron shadow danger | Moving under shadow raises attention and triggers strike. |
| Heron distraction | Pulling branch resets heron attention and moves shadow for 4 s. |
| Fish snap | Fish telegraph and snap reset frog to nearest water edge. |
| Sprinkler manual | Pull valve starts sprinkler and affects surfaces. |
| Sprinkler consequence | Sprinkler knocks caterpillar and dips branch 30 units. |
| Wind arc | Wind changes airborne trajectory; attached frog affected at 40%. |
| Crumbling ledge | Surface breaks after 1.2 s standing and respawns after 8 s. |
| Rain barrel tip | Heavy landing tips barrel. |
| Cork current | Pulling cork enables current and carries leaf to platform. |
| Route variety | At least one direct and one longer route exists in L3–L5. |
| Environmental persistence | After frog reset, interactable effects remain active. |

## Tier 3 tests

| Test | Validation |
| --- | --- |
| Fly sneeze | Eating fly applies sneeze impulse. |
| Wasp hiccup | Eating wasp applies delayed sideways impulse. |
| Beetle flavor | Eating beetle applies no gameplay impulse. |
| No counters | Eating does not increment score, inventory, or any counter. |

---

# 10. BUILD ORDER

1. Create HTML, CSS, Canvas, fixed loop, seeded RNG, constants.
2. Implement `GameState`, input, debug API, pause.
3. Implement physics, collision, camera, and a test level.
4. Implement frog body, grounded state, crouch-hop, launch, no air control.
5. Implement surface friction, wet slide, leaf rock, puddle shallow/deep rules.
6. Implement basic water volume, swim, current, edge haul.
7. Implement anchors, tongue raycast, attach, swing, miss, weak break.
8. Implement sticky walls, climb, slide, non-climb rejection.
9. Implement safe perch, reset, embarrassment, no death.
10. Implement cat attention and reset.
11. Implement Tier 1 levels: M1, M2, M3.
12. Implement render layers, palette, weather, diegetic markers.
13. Implement audio recipes and ambient mix.
14. Implement UI screens and HUD rules.
15. Verify Tier 1 tests and definition of done.
16. Implement Tier 2 level data and combined traversal.
17. Implement heron, fish, sprinkler, wind, rain barrel tip, crumbling ledge.
18. Implement interactables and environmental consequences.
19. Implement route variety and full 5-level sequence.
20. Verify Tier 2 tests and definition of done.
21. Implement insects and eating reactions.
22. Verify Tier 3 tests and definition of done.
23. Final sanity pass against left-out systems.

---

# 11. DEFINITION OF DONE

## Tier 1 Definition of Done

High level: A player can start on a leaf in a rain barrel, use crouch-hop, tongue, sticky walls, wet surfaces, water recovery, and cat stillness, and finish a 3-level MVP to the rooftop pond. Failure is forgiving. The game already looks and sounds like the intended quiet, wet frog-scale game.

Checkboxes:

- [ ] Fixed 60 Hz loop with seeded RNG.
- [ ] Frog hitbox and crouch-hop implemented with no air control.
- [ ] First gap and opening gaps are short and legible.
- [ ] Tongue extends, catches only visible anchors, misses glass/water, weak anchors break.
- [ ] Swing constraint and release work.
- [ ] Sticky walls can be climbed, slid, and held; glass cannot be stuck to.
- [ ] Wet surfaces have friction table and slide behavior.
- [ ] Leaf rock teaches lightness.
- [ ] Water entry, awkward swim, currents, and edge haul work.
- [ ] Cat attention rises when moving, falls when still, steps closer, and resets on swat.
- [ ] Reset never shows death or score shame.
- [ ] Safe perch completes a run and loads next level.
- [ ] MVP sequence reaches a simplified rooftop pond.
- [ ] Visuals include rain, drips, wet highlights, anchors, safe perch glow, distant pond.
- [ ] Audio includes rain, drips, gurgles, frog calls, and readable animal cues.
- [ ] No HUD counters, map, score, or survival meters.
- [ ] Tier 1 tests pass.

## Tier 2 Definition of Done

High level: The game becomes the fuller quiet traversal game. Later levels are more vertical and connected, use hazards, distraction, environmental consequences, and route variety, and still never become combat, survival, collectathon, or abstract puzzle systems.

Checkboxes:

- [ ] Full 5-level sequence is loadable.
- [ ] Combined traversal sequences are required or strongly encouraged.
- [ ] Heron shadow and distraction work.
- [ ] Fish snap works.
- [ ] Sprinkler auto/manual, slippery surfaces, caterpillar/branch dip work.
- [ ] Wind zones change hop arcs and are visually readable.
- [ ] Currents carry frog and leaf.
- [ ] Crumbling ledges and rain barrel tipping work.
- [ ] Interactables only include cork, sprinkler valve, branch disturbance.
- [ ] Environmental effects persist after frog reset.
- [ ] Each later level has direct dangerous and longer safer routes.
- [ ] Tier 2 tests pass.

## Tier 3 Definition of Done

High level: Eating is present as ecology and feedback only. It never becomes score, inventory, or progress.

Checkboxes:

- [ ] Fly, wasp, and beetle can be eaten by tongue.
- [ ] Fly causes sneeze impulse.
- [ ] Wasp causes delayed hiccup/puff impulse.
- [ ] Beetle causes no gameplay impulse.
- [ ] No counters or score are created.
- [ ] Tier 3 tests pass.

---

# A. SANITY

| Check | Result | Notes |
| --- | --- | --- |
| Core mechanics are exactly tier 1. | Valid | Crouch-hop, tongue, sticky, wet/water, cat stillness, reset are all Tier 1. |
| Supporting mechanics are tier 2. | Valid | Combined traversal, hazard escalation, environmental consequences, route variety are Tier 2. |
| Extra mechanics are tier 3. | Valid | Eating reactions are Tier 3. |
| No combat, enemies to defeat, or attack verb. | Valid | Cat, heron, fish are hazards only. |
| No collectathon, counters, or score. | Valid | No pickups, no inventory, no score, no counter fields. |
| No survival meters. | Valid | No health, stamina, hunger, thirst, or breath meter. |
| No death screen. | Valid | Reset is embarrassment and delay only. |
| No locked doors or switches. | Valid | Interactables are physical cork/valve/branch, not abstract switches. |
| No map-like HUD. | Valid | No minimap, compass, objective list, or numeric HUD. |
| Tongue is not magic rope. | Valid | Max length, visible anchors, glass/water rejection, weak anchors. |
| Frog is not a human in a frog suit. | Valid | No running, no tools, low body, hop-based movement. |
| Level sequence reaches rooftop pond. | Valid | Tier 1 MVP finishes; Tier 2 full sequence finishes. |
| All content list parts are included. | Valid | Rain barrels, drainpipes, crates, branches, cat, heron, fish, sprinkler, glass, vines, koi pond, lilies, wind, currents, anchors, insects, environmental objects are specified. |
| All hazard list parts are included. | Valid | Cat, heron, fish, sprinkler, slippery, crumbling, current, wind, rain barrel tip are specified. |
| All landmark list parts are included. | Valid | Each landmark is assigned to at least one level or visual layer. |
| All scale metaphors are represented. | Valid | Puddle as lake, gutter as canyon, cat as disaster, branch as bridge appear in visual and gameplay rules. |
| Numbers exist for every mechanic. | Valid | Inputs, thresholds, speeds, timers, radii, counts, and level dimensions are provided. |
| No extra systems added. | Valid | No combat, no save, no minimap, no inventory, no quest system, no abstract puzzle machines. |
| Engineering contracts cover records and functions. | Valid | Global context includes records; modules expose required functions. |
| Tests cover each tier. | Valid | Tier 1, 2, 3 test lists map to mechanics and definition of done. |