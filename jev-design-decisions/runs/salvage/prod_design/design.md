# 0. SCOPE

This document is the single merged design that supersedes `gameplay.md`, `visual.md`, and `engineering.md`. Where the source documents disagreed, this document makes a final ruling. Where `engineering.md` was empty, this document fills the engineering gaps. Where anything was dropped, the drop is documented in **0.2 Decisions**.

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Top-down 2D space salvage game | 1.1, 3, 4 |
| Player tows wrecks back to a station | 4.10, 4.12 |
| Wrecks’ parts upgrade the player’s ship | 4.14 |
| Station is a safe hub with safe zone and dock zone | 4.12 |
| No combat, weapons, enemies, or vertical axis | 0.2, 4 |
| Single player, single continuous run | 4.1, 4.16 |
| Target playtime 15–25 minutes | 4.18 |
| Five wreck tiers | 4.8 |
| Four upgrade tracks | 4.14 |
| Five contracts | 4.15 |
| Environmental hazards: debris and mines | 4.11 |
| Checkpointing at station | 4.13 |
| Win by retrieving and unloading the Aurora Black Box | 4.15 |
| Death returns player to last station checkpoint | 4.13 |
| Seeded map generation | 4.16 |
| North-up fixed camera | 1.1, 3, 4.6 |
| Readable, accessible presentation | 3, 5, 7 |
| Synthesized audio, no external audio files | 6 |

## 0.2 Decisions

| Decision | gameplay.md | visual.md | engineering.md | Ruling / reasoning |
| --- | --- | --- | --- | --- |
| Engineering document is empty | Not provided | Not provided | Empty | This spec defines all engineering contracts, conventions, module layout, global context, debug API, tests, build order, and definition of done. |
| External image assets | Not specified | Lists PNG asset list and optional Python asset generators | Not provided | Dropped external PNG asset list and Python asset snippets. Builder must render world and UI procedurally using canvas/DOM/SVG and the visual recipes in this spec. Sizes, colors, silhouettes, and motion rules are retained. |
| External audio files | Not specified | Lists `.mp3` and `.wav` file names | Not provided | Dropped external audio file names. Builder must synthesize all audio through the audio API. SFX recipes, music stems, timing, and mixing rules are retained. |
| Tow force clamp contradicts tow snap | Says clamp total tow force to `tow_power`, but also says line snaps if spring force exceeds `1.25 * tow_power` | Uses force ratio vs `tow_power` | Not provided | Ruling: spring force is not clamped to `tow_power`. The applied tow force vector is hard-capped at `1.5 * tow_power`. Stress ratio is `spring_force / tow_power`. Snap occurs if stress ratio exceeds `1.25` continuously for `0.5` seconds. This preserves `tow_power` as a rating while making snap possible. |
| Expected towed top speed table | Gives approximate tugged top speeds by tow level | Not specified | Not provided | The table is retained as design intent, but it is non-binding. The spring-damper constants are authoritative. Do not add ad hoc velocity clamps to force exact speeds. If the feel is wrong, tune damping or visual feedback, not the core constants. |
| Camera zoom | No zoom specified | Zoom out to minimum `0.85` if ship and wreck cannot both fit at `1.0` | Not provided | Adopt visual ruling. Default zoom is `1.0`. While towing, if both ship and wreck cannot fit at `1.0`, zoom out to minimum `0.85`. No camera roll. |
| Screen shake | Not specified | Allows shake for damage/explosions but says do not use shake to express tow stress | Not provided | Screen shake is allowed only for impact events: hull damage, wreck damage, mine explosion, tow snap, ship destruction. Maximum shake is `6 px`, duration under `300 ms`. No shake for tow stress. |
| Mine arming disarm | Mine arms on proximity, explodes after `0.4 s` | Shows armed state | Not provided | Once a mine is armed, it cannot be disarmed. The fuse continues even if the trigger leaves proximity. |
| Checkpoint refresh | Checkpoint created whenever ship is inside safe zone | Shows checkpoint feedback | Not provided | Checkpoint is refreshed continuously while the ship is inside the safe zone, or at least whenever any checkpointed value changes. This makes the station a true safe point. |
| Collision restitution | Says “low restitution” but gives no number | Not specified | Not provided | Restitution is `0.2` for all circle collisions. |
| Wreck-wreck collision | Says towed wreck can collide with other wrecks | Not specified | Not provided | Wrecks are dynamic circles. Wreck-wreck collisions separate the wrecks, apply wreck damage to both using the wreck damage formula, and do not directly damage the ship unless the ship is also involved. |
| Debris-wreck damage | Says collisions damage the wreck | Not specified | Not provided | Debris-wreck collisions use `wreck_damage = clamp(relative_speed * 0.15, 0, 20)`. |
| Scanner world warning | Scanner Level 2 shows mines with warning radius, primarily minimap | Shows nearby dashed red warning circle in world within `250` units | Not provided | Adopt visual ruling. Scanner Level 2 shows mines on minimap and, in the world, shows a dashed red warning circle of radius `70` for mines within `250` units. |
| Locked wrecks | Locked wrecks may be visible as inert silhouettes | Locked wrecks are dark gray, `40%` opacity, no light, not on minimap | Not provided | Adopt visual ruling. Locked wrecks may be rendered in the world but have no interaction and are not shown on the minimap. |
| Upgrade menu input | `Tab` or `I`, station only, not while towing | Same | Not provided | `Tab` and `I` open/close upgrade menu only when inside safe zone and not towing. `Tab` must be prevented from changing browser focus. |
| Contract fallback | Auto-complete score contract if no eligible active wrecks remain | Not specified | Not provided | Keep fallback. It applies only to score contracts, not the final wreck contract. |
| Random source | Seeded RNG required | Seeded visual variation only | Not provided | Use Mulberry32. Gameplay RNG is seeded from run seed. Visual RNG is seeded from `run_seed ^ 0x9E3779B9`. No `Math.random()` for gameplay. |
| Simulation step | Not specified | Not specified | Empty | Fixed timestep of `1 / 60` seconds. Accumulate real frame time, clamp to `0.1 s`, run at most `5` fixed steps per frame. |
| Units | World units used | 1 world unit = 1 pixel at zoom `1.0` | Not provided | 1 world unit = 1 pixel at zoom `1.0`. Time is seconds. Mass is an abstract unit. Force is mass * world unit / second². |
| HUD implementation | HUD elements specified | HUD layout specified | Not provided | HUD and screens are HTML/CSS/DOM/SVG. The world may be rendered on canvas, but the UX layer must not depend on canvas-drawn text or canvas-only UI. |
| Reduce motion option | Not specified | Says “if a reduce-motion option is added” | Not provided | No user-facing reduce-motion setting in Tier 3. A debug flag may exist. Shake and particle limits remain mandatory. |
| Save system between runs | Cut | Cut | Not provided | No persistent save between runs. Checkpointing is in-memory only. |
| Multiple part types | Cut | Cut | Not provided | One currency: `Parts`. |
| Combat | Cut | Cut | Not provided | No weapons, enemies, enemy fire, or combat UI. |
| Total parts available | States total parts available is `77` | Not specified | Not provided | Computed from the wreck and contract tables is `75`: `61` wreck parts + `14` contract reward parts. The `77` figure is superseded as a documentation error. The economy still exceeds the `41` total upgrade cost. |

## 0.3 Tiers

| Tier | Segment | Included systems | Exit meaning |
| --- | --- | --- | --- |
| Tier 1 | Core vertical slice | Fixed-step loop, input, ship movement, station zones, one contract, Scrap Cans, tow attach/detach, unload, parts, all four upgrade tracks at basic levels, minimal HUD, pause, provisional victory after Contract 1, basic debug | The core salvage loop is playable end-to-end. |
| Tier 2 | Full content and failure states | All rings, all wreck tiers, debris, mines, contracts 2–5, final Aurora Black Box, checkpoint/death, fallback, full map generation, scanner, boundary, final victory | The full designed run is playable from start to final victory. |
| Tier 3 | Presentation | Full visual spec: parallax, station, zones, ship/wreck/mine visuals, tow line states, effects, minimap, scanner card, upgrade visuals, banners, popups, accessibility rules | The game looks like the merged visual design. |
| Tier 4 | Audio | Synthesized SFX, synthesized music stems, dynamic mixing, positional audio, ducking | The game has the merged audio design. |
| Tier 5 | Verification and polish | Full debug API, automated tests, performance checks, sanity checks | The builder can prove each tier is done code-wise. |

Tier 1 is guaranteed to build. Higher tiers may be left unbuilt, but each built tier must satisfy its definition of done in section 11.

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Concept | Convention |
| --- | --- |
| World plane | 2D top-down, X/Y only. No gameplay Z-axis. |
| X axis | Positive X is east / right. |
| Y axis | Positive Y is south / down. Negative Y is north / up. |
| North-up | The camera does not rotate. Negative Y is visually north. |
| World unit | 1 world unit = 1 pixel at zoom `1.0`. |
| Time | Seconds. |
| Fixed step | `dt = 1 / 60` seconds. |
| Angle | Radians. Heading `0` points east. Positive heading rotates clockwise on screen. |
| Speed | World units / second. |
| Mass | Abstract mass unit. |
| Force | Mass * world unit / second². |
| Heading vector | `(cos(heading), sin(heading))`. |
| Turn input | `A` / Left decreases heading. `D` / Right increases heading. |
| Coordinates | Station is `(0, 0)`. Final Aurora Black Box is `(0, -3000)`. |

## 1.2 Important conventions

- All gameplay constants live in one config module.
- The simulation uses a fixed-step loop.
- Real frame delta is clamped to `0.1 s`.
- At most `5` fixed steps run per rendered frame.
- Gameplay randomness uses one seeded RNG.
- Visual-only randomness uses a separate seeded RNG.
- No `Math.random()` may affect gameplay.
- All collisions are circle-based.
- The station is not a solid collision object.
- The world boundary is a soft clamp, not a solid wall.
- Checkpointing is in-memory only.
- All critical gameplay information must also be visible, not audio-only.
- HUD and screens are HTML/CSS/DOM/SVG.
- Particle counts must stay within the budgets in section 3.
- Screen shake is limited to impact events and capped at `6 px`.
- The same run seed must produce the same gameplay world.

# 2. CONTRACTS

## 2.1 Module layout

| Module / file | Responsibility | Tier |
| --- | --- | --- |
| `index.html` | Page shell, canvas/DOM mount, HUD DOM, screens | 1 |
| `style.css` | HUD, screens, prompts, buttons, minimap, panels | 1 |
| `main.js` | Bootstrap, fixed-step loop, state machine entry | 1 |
| `config.js` | All constants, tables, contracts, upgrades, wreck tiers | 1 |
| `rng.js` | Seeded RNG and visual RNG | 1 |
| `input.js` | Keyboard input, action mapping, debug input injection | 1 |
| `world.js` | World state, rings, boundary, map generation | 1/2 |
| `ship.js` | Ship stats, movement, hull, input effects | 1 |
| `collision.js` | Circle overlap, separation, damage, boundary clamp | 1/2 |
| `tow.js` | Attach, detach, spring-damper, stress, snap | 1 |
| `wreck.js` | Wreck records, integrity, parts yield, unload | 1/2 |
| `hazard.js` | Debris and mine behavior | 2 |
| `station.js` | Safe zone, dock zone, unload, checkpoint refresh | 1/2 |
| `contract.js` | Contracts, score, ring unlock, fallback | 1/2 |
| `upgrade.js` | Upgrade tracks, costs, purchase, stat application | 1 |
| `checkpoint.js` | Save/load in-run checkpoint | 2 |
| `camera.js` | Camera centering, zoom, shake | 1/3 |
| `hud.js` | HUD updates, prompts, popups, minimap | 1/3 |
| `ux.js` | Screen state machine, title, pause, game over, victory | 1 |
| `audio.js` | Synthesized SFX and music | 4 |
| `debug.js` | Debug API | 1/5 |
| `tests.js` | High-level tier tests | 5 |

## 2.2 Global context

The global context `G` must contain every field required by gameplay records.

```ts
type Vec2 = { x: number; y: number };

type ShipState = {
  position: Vec2;
  velocity: Vec2;
  heading: number;
  hull: number;
  maxHull: number;
  mass: number;
  collisionRadius: number;
  thrust: number;
  drag: number;
  turnRate: number;
  hullLevel: number;
  thrusterLevel: number;
  towLevel: number;
  scannerLevel: number;
  towPower: number;
  attachRange: number;
  maxTowMass: number;
  towedWreckId: number | null;
  thrustActive: boolean;
  brakeActive: boolean;
  inSafeZone: boolean;
  inDockZone: boolean;
  unloadActive: boolean;
  unloadProgress: number;
};

type WreckTier =
  | "ScrapCan"
  | "TransportHauler"
  | "FighterFrame"
  | "CargoLiner"
  | "AuroraBlackBox";

type WreckStateName =
  | "locked"
  | "active"
  | "towed"
  | "unloadded";

type Wreck = {
  id: number;
  tier: WreckTier;
  name: string;
  position: Vec2;
  velocity: Vec2;
  mass: number;
  radius: number;
  initialIntegrity: number;
  currentIntegrity: number;
  score: number;
  baseParts: number;
  towRequirement: number;
  state: WreckStateName;
  ringIndex: number;
  isFinal: boolean;
};

type Debris = {
  id: number;
  position: Vec2;
  radius: number;
};

type MineStateName =
  | "dormant"
  | "armed"
  | "exploding"
  | "destroyed";

type Mine = {
  id: number;
  position: Vec2;
  radius: number;
  proximityRadius: number;
  explosionRadius: number;
  explosionDamageShip: number;
  explosionDamageWreck: number;
  fuseTime: number;
  state: MineStateName;
  armTimer: number;
  explosionTimer: number;
};

type ContractType = "score" | "final";

type Contract = {
  index: number;
  name: string;
  type: ContractType;
  requiredScore: number;
  currentScore: number;
  rewardParts: number;
  unlockedRing: number;
  completed: boolean;
};

type GameStateName =
  | "title"
  | "start"
  | "contractActive"
  | "atStation"
  | "upgradeMenu"
  | "paused"
  | "gameOver"
  | "victory";

type InputState = {
  rotateLeft: boolean;
  rotateRight: boolean;
  thrust: boolean;
  brake: boolean;
  tow: boolean;
  unload: boolean;
  upgrade: boolean;
  pause: boolean;
  enter: boolean;
};

type CameraState = {
  position: Vec2;
  zoom: number;
  shakeMagnitude: number;
  shakeTime: number;
  shakeOffset: Vec2;
};

type TowState = {
  wreckId: number | null;
  restLength: number;
  K: number;
  C: number;
  springForce: number;
  stressRatio: number;
  snapTimer: number;
  snapWarningActive: boolean;
};

type Prompt = {
  text: string;
  type: "info" | "warning" | "failure" | "success";
  time: number;
};

type Popup = {
  text: string;
  color: string;
  position: Vec2;
  age: number;
};

type Checkpoint = {
  contractIndex: number;
  contractScore: number;
  unlockedRings: boolean[];
  parts: number;
  totalPartsCollected: number;
  wrecksSalvaged: number;
  upgradeLevels: {
    hull: number;
    thrusters: number;
    tow: number;
    scanner: number;
  };
  hull: number;
  unloaddedWreckIds: number[];
  wreckIntegrity: Record<number, number>;
  mineStates: Record<number, MineStateName>;
  shipPosition: Vec2;
};

type GlobalContext = {
  state: GameStateName;
  pausedState: GameStateName | null;
  time: number;
  runTime: number;
  seed: number;
  rng: {
    next(): number;
    range(min: number, max: number): number;
    angle(): number;
    radius(min: number, max: number): number;
  };
  visualRng: {
    next(): number;
    range(min: number, max: number): number;
    angle(): number;
    radius(min: number, max: number): number;
  };
  ship: ShipState;
  wrecks: Wreck[];
  debris: Debris[];
  mines: Mine[];
  contracts: Contract[];
  activeContractIndex: number;
  unlockedRings: boolean[];
  parts: number;
  totalPartsCollected: number;
  wrecksSalvaged: number;
  checkpoint: Checkpoint | null;
  input: InputState;
  camera: CameraState;
  tow: TowState;
  prompts: Prompt[];
  popups: Popup[];
  banner: {
    text: string;
    time: number;
    active: boolean;
  };
  audio: {
    muted: boolean;
    musicState: string;
    activeLoops: string[];
  };
};
```

## 2.3 Module specifics

| Module | Required functions | Tier |
| --- | --- | --- |
| `config.js` | `getConfig()`, `getWreckTier(name)`, `getUpgrade(track, level)`, `getContract(index)`, `getRing(index)`, `getRingRange(index)` | 1 |
| `rng.js` | `createRng(seed)`, `next()`, `range(min, max)`, `angle()`, `radius(min, max)` | 1 |
| `main.js` | `init()`, `startLoop()`, `stopLoop()`, `update(dt)`, `render()`, `stepOnce()` | 1 |
| `input.js` | `bind()`, `unbind()`, `update()`, `isDown(action)`, `justPressed(action)`, `simulate(action, down)` | 1 |
| `world.js` | `generateWorld(seed)`, `placeWrecks()`, `placeDebris()`, `placeMines()`, `placeFixedWrecks()`, `isBeyondBoundary(pos)`, `clampToBoundary(entity)` | 1/2 |
| `ship.js` | `initShip()`, `updateShip(dt)`, `applyInput(dt)`, `applyDrag(dt)`, `damageHull(amount)`, `healHull(amount)`, `getStats()`, `setStats(partial)` | 1 |
| `collision.js` | `circleOverlap(a, b)`, `resolvePair(a, b, restitution)`, `shipDebrisCollisions()`, `shipWreckCollisions()`, `wreckDebrisCollisions()`, `wreckWreckCollisions()`, `applyShipCollisionDamage(relativeSpeed)`, `applyWreckCollisionDamage(relativeSpeed)` | 1/2 |
| `tow.js` | `canAttach(wreck)`, `attach(wreckId)`, `detach()`, `updateTow(dt)`, `getStressRatio()`, `snapLine()`, `getAttachFailReason(wreck)` | 1 |
| `wreck.js` | `initWrecks(world)`, `updateWrecks(dt)`, `damageWreck(id, amount)`, `getPartsYield(wreck)`, `unloadWreck(id)`, `setWreckState(id, state)`, `getWreck(id)` | 1/2 |
| `hazard.js` | `initHazards(world)`, `updateMines(dt)`, `armMine(id)`, `explodeMine(id)`, `applyExplosion(mine)`, `updateDebris(dt)` | 2 |
| `station.js` | `isSafeZone(pos)`, `isDockZone(pos)`, `updateStation(dt)`, `startUnload()`, `updateUnload(dt)`, `completeUnload()`, `refreshCheckpoint()` | 1/2 |
| `contract.js` | `initContracts()`, `updateContracts()`, `addScore(amount)`, `completeContract()`, `unlockRing(index)`, `fallbackComplete()`, `getActive()` | 1/2 |
| `upgrade.js` | `getTrack(name)`, `canBuy(name)`, `buy(name)`, `applyUpgrade(name)`, `getRecommended()` | 1 |
| `checkpoint.js` | `save()`, `load()`, `create()`, `restore()` | 2 |
| `camera.js` | `update(dt)`, `computeZoom()`, `addShake(amount)`, `getOffset()` | 1/3 |
| `hud.js` | `update()`, `setPrompt(text, type)`, `addPopup(text, color)`, `showBanner(text)`, `updateMinimap()` | 1/3 |
| `ux.js` | `setState(state)`, `showTitle()`, `showStart()`, `showGameOver()`, `showVictory()`, `toggleUpgradeMenu()`, `togglePause()` | 1 |
| `audio.js` | `init()`, `play(name)`, `startLoop(name)`, `stopLoop(name)`, `setMusic(state)`, `duck(amount, duration)` | 4 |
| `debug.js` | See section 8 | 1/5 |
| `tests.js` | `runTier(n)`, `assert(condition, message)` | 5 |

# 3. VISUAL SPEC

The game looks like a quiet, practical salvage operation around a working space station. The visual language is functional, slightly worn, and service-oriented. The player ship is bright cyan and unmistakable. Wrecks are desaturated gray with one accent color and size-based tier identity. The station is warm amber and safe. Hazards are readable before they punish. The core visual job is to make the tow line, station safety, wreck condition, and mine danger easy to read at a glance.

Lighting and atmosphere use rim lighting, soft glow, vignettes, and ring-based background tints. The station has a warm core and rotating service arms. The safe zone is a soft cyan field. The dock zone is a brighter green ring with inward chevrons. The field becomes cooler and darker outward. The final corridor is near-black with aurora streaks.

The space is one continuous world centered on the station. Rings expand outward. The world boundary is a soft visual edge, not a wall. Parallax is pseudo-depth only: far stars, mid nebula, near dust. Dust is visually distinct from debris.

## Visual recipe table

| Object | Visual recipe | Gameplay rule implied | Tier |
| --- | --- | --- | --- |
| Space background | Base `#05070D`, ring tints, parallax starfield | No gameplay Z-axis | 3 |
| Far starfield | Small stars, faint nebula, `0.1x` parallax | Non-collidable | 3 |
| Mid starfield | Larger stars, colored nebula, `0.25x` parallax | Non-collidable | 3 |
| Near dust | 1–2 px dust motes, `0.5x` parallax, no rim light, no blink | Non-collidable, not a hazard | 3 |
| World boundary | Faint white circular grid, static noise, slight vignette at radius `3200` | Soft clamp, prompt `No signal beyond boundary` | 2/3 |
| Station | Warm amber core, 3–4 rotating service arms, open lattice, not solid-looking | Station is not a solid collision object | 1/3 |
| Safe zone | Cyan circular field, radius `120`, dashed outer edge, `#55F1FF` at 20–30% opacity, 2-second pulse | Hull regen, checkpoint, upgrade access | 1/3 |
| Dock zone | Green solid ring, radius `50`, `#55FF9A`, rotating inward chevrons | Unload zone | 1/3 |
| Contract board | Amber-bordered holographic panel near station, `160 x 96 px` | Shows active contract and reward | 2/3 |
| Player ship | Arrow-like rounded salvage tug, bright cyan edge `#55F1FF`, dark cockpit, rear thruster, front tow hook | Player is always readable | 1/3 |
| Scrap Can | Small canister, rust orange accent `#FF7A3D`, visual size `36 x 36 px`, collision radius `18` | Tier identity by size and accent | 1/3 |
| Transport Hauler | Shuttle/transport, slate teal accent `#6FC7B0`, visual size `48 x 48 px`, collision radius `24` | Tier identity by size and accent | 2/3 |
| Fighter Frame | Angular fighter, magenta accent `#FF5AF1`, visual size `52 x 52 px`, collision radius `26` | Tier identity by size and accent | 2/3 |
| Cargo Liner | Large boxy liner, mustard accent `#FFC84D`, visual size `64 x 64 px`, collision radius `32` | Tier identity by size and accent | 2/3 |
| Aurora Black Box | Black cube, violet/gold/cyan aurora glow, rotating rings, visual size `72 x 72 px`, collision radius `36` | Final wreck, visually distinct | 2/3 |
| Locked wreck | Dark gray silhouette, no accent light, `40%` opacity | Not interactive, not on minimap | 2/3 |
| Debris cluster | 3–7 rock/metal chunks, dark gray/brown, irregular silhouette, size matches collision radius `25–50` | Static circular obstacle | 2/3 |
| Mine dormant | Dark sphere, red blinking light, radius `12`, faint at distance | Proximity hazard | 2/3 |
| Mine armed | Fast red blink, expanding white/red ring to proximity radius `35` | Fuse active | 2/3 |
| Mine warning | Scanner Level 2: dashed red circle radius `70`, shown when mine within `250` units | Scanner reduces uncertainty | 2/3 |
| Tow line normal | Cyan line, 2 px wide, force ratio `0–0.75` | Tow active | 1/3 |
| Tow line moderate | Yellow line, 2–3 px wide, force ratio `0.75–1.0` | Stress increasing | 3 |
| Tow line high | Red line, 3 px wide, slight vibration, force ratio `1.0–1.25` | High stress | 3 |
| Tow snap warning | Flashing red line, snap timer arc, force ratio `>1.25` | Snap in `0.5 s` if sustained | 3 |
| Tow stress meter | Bottom-center meter `120 x 8 px`, marker at `1.0`, snap zone beyond `1.25` | Readable stress without staring at line | 3 |
| Hull damage | Red flash, red vignette `150 ms`, hull bar flash, sparks, shake up to `4 px` | Damage readable | 1/3 |
| Low hull | Ship outline pulses red at `2 Hz`, hull bar pulses | Urgency without hiding ship | 3 |
| Ship destruction | Explosion, 4–6 fragments fade over `0.8 s`, red vignette, shake `6 px` | Death clearly communicated | 2/3 |
| Unload progress | Circular ring around ship, radius `20 px`, `#55FF9A`, fills over `2.0 s` | Hold-to-unload progress | 1/3 |
| Score popup | Amber `#FFC46B`, floats upward `0.8 s` | Reward readable | 1/3 |
| Part popup | Green `#55FF9A`, hex bolt icon, floats upward `0.8 s` | Reward readable | 1/3 |
| Contract complete | Green progress flash, banner `Contract Complete`, reward parts fly to counter | Progression communicated | 2/3 |
| Ring unlock | Banner `Ring N Unlocked`, minimap boundary lights cyan for `1 s`, background tint shifts | World expansion communicated | 2/3 |

## Color system

| Use | Hex | Notes |
| --- | ---: | --- |
| Space black | `#05070D` | Base background |
| Deep space blue | `#0A1220` | Nebula and panel base |
| UI panel | `#0B1220` | 80% opacity |
| UI border | `#2E4A5A` | Subtle technical border |
| White text | `#F4F7FB` | Primary text |
| Muted text | `#9FB0C0` | Secondary text |
| Player / interactive | `#55F1FF` | Ship, player arrow, attachable prompts |
| Station / score | `#FFC46B` | Station, contract, score popups |
| Success / parts / dock | `#55FF9A` | Unload, parts, contract complete |
| Warning | `#FFD24D` | Moderate tow stress, speed warnings |
| Danger / damage | `#FF4D5A` | Hull damage, mines, high stress |
| Scanner / final | `#B48BFF` | Scanner effects, final wreck accent |

## Ring background tints

| Ring | Background tint | Notes |
| --- | ---: | --- |
| Ring 1 | `#102033` | Brighter, warm station glow |
| Ring 2 | `#0F2A2C` | Cooler teal, first caution |
| Ring 3 | `#1A1430` | Darker violet, denser |
| Ring 4 | `#2A1A10` | Brown/amber industrial dust |
| Final Corridor | `#05070D` | Near-black with aurora streaks |

## Z-order

1. Far starfield.
2. Mid starfield and nebula.
3. Near dust.
4. World boundary effect.
5. Station safe zone.
6. Dock zone.
7. Station.
8. Debris clusters.
9. Wrecks.
10. Mines.
11. Tow line.
12. Ship.
13. Particles.
14. Vignettes and damage overlays.
15. HUD.
16. Prompts.
17. Banners.
18. Menus and full-screen states.

# 4. GAMEPLAY SPEC

This is a single-player, top-down, 2D space salvage game. The player pilots a small salvage tug around a central station, attaches to drifting wrecks, tows them back through debris and mines, unloads them in the dock zone, earns salvage score and parts, and uses parts to upgrade the ship. Progression is contract-based. The player completes four score contracts, unlocks outer rings, then retrieves the final Aurora Black Box to win. Death returns the player to the last station checkpoint. The game has no combat, no weapons, no enemies, and no vertical axis.

## 4.0 Records and rosters

| Record | Key fields | Tier |
| --- | --- | --- |
| Ship | `position`, `velocity`, `heading`, `hull`, `maxHull`, `thrust`, `drag`, `turnRate`, `towLevel`, `hullLevel`, `thrusterLevel`, `scannerLevel`, `towedWreckId` | 1 |
| Wreck | `id`, `tier`, `position`, `velocity`, `mass`, `radius`, `initialIntegrity`, `currentIntegrity`, `score`, `baseParts`, `towRequirement`, `state`, `ringIndex`, `isFinal` | 1/2 |
| Debris | `id`, `position`, `radius` | 2 |
| Mine | `id`, `position`, `radius`, `proximityRadius`, `explosionRadius`, `state`, `armTimer` | 2 |
| Contract | `index`, `name`, `type`, `requiredScore`, `currentScore`, `rewardParts`, `unlockedRing`, `completed` | 1/2 |
| Run | `seed`, `parts`, `totalPartsCollected`, `wrecksSalvaged`, `unlockedRings`, `checkpoint` | 1/2 |

## 4.1 Core loop [Tier 1]

1. Leave station.
2. Identify a wreck.
3. Approach and attach tow.
4. Return to station while avoiding hazards and tow stress.
5. Dock and unload.
6. Gain salvage score and parts.
7. Upgrade ship.
8. Complete next contract.
9. Retrieve final wreck and win.

Target playtime: `15–25` minutes per full run.

There is no timer, no combat, no weapons, no enemies, and no vertical axis.

## 4.2 Ship base stats [Tier 1]

| Stat | Base value |
| --- | ---: |
| Ship mass | `50` |
| Ship collision radius | `14` |
| Max hull | `100` |
| Thrust | `300` |
| Drag | `1.2` |
| Turn rate | `3.0` rad/s |
| Tow power | `250` |
| Tow attach range | `60` |
| Max tow mass | `50` |
| Scanner level | `0` |

## 4.3 Movement [Tier 1]

The ship uses 2D inertia.

Each fixed step:

```text
heading += turn_input * 3.0 * dt
velocity += heading_vector * thrust * dt
velocity -= velocity * 3.0 * dt   // if brake input active
velocity -= velocity * 1.2 * dt   // drag
position += velocity * dt
clamp position to world boundary
```

### Expected unladen speed [Tier 1, non-binding target]

| Thruster level | Thrust | Drag | Max speed |
| ---: | ---: | ---: | ---: |
| 0 | `300` | `1.2` | `250` |
| 1 | `360` | `1.2` | `300` |
| 2 | `420` | `1.2` | `350` |
| 3 | `480` | `1.2` | `400` |

Speed is in world units per second.

## 4.4 Hull and damage [Tier 1/2]

- Hull is the ship’s health.
- Hull does not regenerate outside the station safe zone.
- Inside the station safe zone, hull regenerates at `10` hull per second up to max hull.
- If hull reaches `0`, the ship is destroyed.

### Collision damage [Tier 1/2]

When the ship collides with a wreck, debris cluster, or another ship-like object:

1. Calculate relative speed.
2. If relative speed is less than `10`, no damage occurs.
3. Otherwise:

```text
ship_damage = clamp(relative_speed * 0.2, 0, 30)
```

Maximum ship collision damage is `30`.

### Wreck damage [Tier 1/2]

When a wreck is hit:

```text
wreck_damage = clamp(relative_speed * 0.15, 0, 20)
```

Wreck damage reduces wreck integrity.

## 4.5 Collision [Tier 1/2]

- All collisions use circles.
- Restitution is `0.2`.
- Collisions separate objects and reflect velocity with low restitution.
- Debris clusters are static.
- Wrecks are dynamic.
- The ship is dynamic.
- Towed wrecks can collide with debris, mines, other wrecks, and the boundary.
- Collisions damage the wreck.
- Collisions can push the ship through the tow connection.
- A towed wreck can trigger mines.
- A towed wreck can enter the station safe zone without taking damage.

## 4.6 Camera [Tier 1/3]

- Camera is centered on the ship.
- Camera does not rotate.
- While towing, if the distance between ship and wreck is greater than `100`, the camera centers on the midpoint between the ship and wreck.
- The camera should keep both the ship and the towed wreck visible whenever possible.
- Default zoom is `1.0`.
- If both ship and wreck cannot fit at zoom `1.0`, zoom out to a minimum of `0.85`.
- No camera roll.
- No camera shake for tow stress.

## 4.7 Controls [Tier 1]

| Input | Action |
| --- | --- |
| `A` / `D` or Left / Right | Rotate ship |
| `W` / Up | Thrust |
| `S` / Down | Brake |
| `Q` or `E` | Attach / detach tow |
| `U` | Hold to unload |
| `Tab` or `I` | Open upgrade menu, station only |
| `P` or `Esc` | Pause |

## 4.8 Wreck tiers and roster [Tier 1/2]

| Wreck | Mass | Initial integrity | Score | Parts | Tow requirement | Count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Scrap Can | `20` | `50` | `10` | `1` | Level `0` | `14` |
| Transport Hauler | `40` | `90` | `25` | `2` | Level `0` | `9` |
| Fighter Frame | `60` | `130` | `40` | `2` | Level `1` | `8` |
| Cargo Liner | `90` | `180` | `60` | `3` | Level `2` | `3` |
| Aurora Black Box | `120` | `250` | `100` | `4` | Level `3` | `1` |

### Wreck collision radius [Tier 1/2]

| Wreck | Radius |
| --- | ---: |
| Scrap Can | `18` |
| Transport Hauler | `24` |
| Fighter Frame | `26` |
| Cargo Liner | `32` |
| Aurora Black Box | `36` |

## 4.9 Wreck integrity and parts [Tier 1]

- Each wreck has integrity.
- Integrity starts at the initial value in the wreck tier table.
- Integrity decreases when the wreck is hit.
- Integrity does not regenerate.
- Wrecks do not break or disappear from damage.
- A wreck with `0` integrity can still be towed and unloaded.

### Parts yield based on integrity [Tier 1]

| Integrity at unload | Parts received |
| --- | ---: |
| Greater than `60%` of initial integrity | Full parts |
| `30%` to `60%` of initial integrity | Full parts minus `1` |
| Less than `30%` of initial integrity | `0` parts |

Example:

- Cargo Liner normally yields `3` parts.
- If unloaded at `70%` integrity, it yields `3` parts.
- If unloaded at `40%` integrity, it yields `2` parts.
- If unloaded at `10%` integrity, it yields `0` parts.

### Score [Tier 1]

- Score is fixed by wreck tier.
- Score is not reduced by damage.
- Parts are the reward for careful salvage.

### Wreck states [Tier 1/2]

1. **Locked**
   - Not yet unlocked.
   - No interaction.
   - Not shown on minimap.
2. **Active**
   - Can be scanned, towed, and unloaded.
3. **Towed**
   - Currently attached to player ship.
4. **Unloaded**
   - Removed from the world.

### Wreck information display [Tier 2]

Without Scanner Level `1`:

- Wrecks are visible in the world.
- Wrecks appear on the minimap.
- Parts, integrity, and mass are hidden.

With Scanner Level `1`:

- When within `200` of a wreck, show:
  - Wreck name.
  - Mass.
  - Part yield.
  - Integrity percentage.

With Scanner Level `2`:

- Mines are shown on the minimap.
- Mines show a warning radius.

## 4.10 Tow system [Tier 1]

Towing is the core mechanic.

### Attach conditions [Tier 1]

The player can attach to a wreck only if all of the following are true:

1. The wreck is active.
2. The player is not already towing another wreck.
3. The wreck is within the current tow attach range.
4. The current tow level is greater than or equal to the wreck’s tow requirement.
5. The wreck mass is less than or equal to the current max tow mass.
6. The relative speed between ship and wreck is less than `50`.

If attachment fails, show a prompt:

- `Too fast to attach`
- `Cannot tow: mass exceeded`
- `Detach current tow first`
- `Out of range`

### Tow attach range [Tier 1]

| Tow level | Attach range |
| ---: | ---: |
| 0 | `60` |
| 1 | `70` |
| 2 | `80` |
| 3 | `95` |

### Max tow mass [Tier 1]

| Tow level | Max tow mass |
| ---: | ---: |
| 0 | `50` |
| 1 | `70` |
| 2 | `100` |
| 3 | `130` |

### Tow physics [Tier 1]

The tow connection is a spring-damper line.

Constants:

- Rest length: `50`
- Ship mass: `50`
- Wreck mass: variable
- Wreck drag: `3.0`

For each towed wreck:

1. Calculate the vector from the ship’s tow point to the wreck’s tow point.
2. Calculate distance.
3. If distance is greater than rest length:
   - Extension = distance - `50`.
   - `K = tow_power / 20`.
   - Spring force = `K * extension`.
   - Applied spring force is hard-capped at `1.5 * tow_power`.
   - Apply spring force to the wreck toward the ship.
   - Apply opposite force to the ship.
4. Apply damping:
   - Damping opposes relative velocity along the tow line.
   - Damping coefficient:

```text
C = 2 * sqrt(K * (ship_mass + wreck_mass)) * 0.4
```

5. The total tow force vector is hard-capped at `1.5 * tow_power`.
6. Apply wreck drag:

```text
wreck_velocity -= wreck_velocity * 3.0 * dt
```

7. Apply normal ship drag to the ship.

### Tow stress and line snap [Tier 1]

- Stress ratio is `spring_force / tow_power`.
- If stress ratio exceeds `1.25` continuously for `0.5` seconds, the tow line snaps.
- When the line snaps:
  - The wreck detaches.
  - The wreck keeps its current velocity.
  - Show prompt: `Tow line snapped`.
  - Important audio and visual feedback are required.

### Expected tugged speed [Tier 1, non-binding target]

| Tow level | Tow power | Approximate tugged top speed |
| ---: | ---: | ---: |
| 0 | `250` | `60` |
| 1 | `400` | `95` |
| 2 | `600` | `143` |
| 3 | `850` | `202` |

The exact speed depends on wreck mass and drag. The feel should be:

- Level `0` towing is slow and awkward.
- Level `1` towing is manageable.
- Level `2` towing is comfortable.
- Level `3` towing is fast enough for the final wreck but still feels heavy.

### Detach [Tier 1]

- The player can detach at any time using the tow input.
- Detaching does not damage the wreck.
- The wreck keeps its current velocity.
- The player can reattach later if conditions are met.

### Towed wreck collisions [Tier 2]

- A towed wreck can collide with debris, mines, other wrecks, and the boundary.
- Collisions damage the wreck.
- Collisions can push the ship.
- A towed wreck can trigger mines.
- A towed wreck can enter the station safe zone without taking damage.

## 4.11 Hazards [Tier 2]

### Debris clusters [Tier 2]

- Debris clusters are static circular obstacles.
- Radius: `25` to `50`.
- They do not move.
- They do not take damage.
- They do not disappear.
- Colliding with debris damages the ship and any towed wreck.
- Collision response:
  - Separate the ship or wreck from the debris.
  - Reflect velocity with restitution `0.2`.
  - Apply damage based on relative speed.

### Mines [Tier 2]

- Mines are circular hazards.
- Mine radius: `12`.
- Proximity trigger radius: `35`.
- Explosion radius: `70`.
- Explosion damage to ship: `25`.
- Explosion damage to wreck: `20`.
- Fuse time: `0.4` seconds.

Mine behavior:

1. If the ship or a towed wreck enters the proximity radius, the mine arms.
2. After `0.4` seconds, it explodes.
3. The explosion damages all ships and wrecks within the explosion radius.
4. The mine is destroyed.
5. Mines do not chain-react.
6. Once armed, a mine cannot be disarmed.

Scanner interaction:

- Scanner Level `0`:
  - Mines are not shown on the minimap.
  - Mines are faintly visible in the world when close.
- Scanner Level `1`:
  - Mines are shown on the minimap.
- Scanner Level `2`:
  - Mines are shown on the minimap with a warning radius.
  - In the world, when a mine is within `250` units, show a dashed red circle around it with radius `70`.

## 4.12 Station systems [Tier 1/2]

### Safe zone [Tier 1]

- Radius: `120` around station center.
- Effects:
  - Hull regenerates at `10` per second.
  - Checkpoint updates.
  - Upgrade menu can be opened.
  - Contract board is available.

### Dock zone [Tier 1]

- Radius: `50`.
- Used for unloading.

### Unloading [Tier 1]

The player can unload a towed wreck if:

1. The ship is inside the dock zone.
2. Ship speed is less than `20`.
3. The player is holding the unload input.
4. The player is towing a wreck.

Unload time:

- `2.0` seconds.

When unload completes:

1. Add the wreck’s fixed score to the current contract score.
2. Calculate parts based on current wreck integrity.
3. Add parts to the player’s parts inventory.
4. Remove the wreck from the world.
5. Detach the tow.
6. If the contract requirement is met, complete the contract.

If the player leaves the dock zone or exceeds speed `20`, unload progress resets.

If the player is not towing, the unload input does nothing.

If the player detaches during unload, unload cancels.

## 4.13 Checkpointing [Tier 2]

A checkpoint is refreshed whenever the ship is inside the station safe zone.

The checkpoint stores:

- Current contract index.
- Current contract score.
- Unlocked rings.
- Parts inventory.
- Upgrade levels.
- Hull value.
- Which wrecks have been unloaded.
- Wreck integrity values.
- Mine states.
- Ship position.

On death:

1. Load the last checkpoint.
2. Respawn at the station.
3. Keep all checkpointed progress.
4. Lose any progress made after the last checkpoint.

Why checkpoint at station:

- The station is the natural safe point.
- It makes death fair.
- It preserves the core progression loop.
- It avoids full-run restarts.

## 4.14 Upgrade systems [Tier 1]

Use a single part currency called **Parts**.

There are no separate part types.

### Upgrade tracks [Tier 1]

| Track | Purpose |
| --- | --- |
| Hull Plating | Increases max hull |
| Thrusters | Increases thrust and top speed |
| Tow Servos | Increases tow power, attach range, and max tow mass |
| Scanner | Reveals wreck data and mines |

### Hull Plating [Tier 1]

| Level | Max hull | Cost |
| ---: | ---: | ---: |
| 0 | `100` | `0` |
| 1 | `140` | `2` |
| 2 | `180` | `4` |
| 3 | `240` | `6` |

### Thrusters [Tier 1]

| Level | Thrust | Max speed | Cost |
| ---: | ---: | ---: | ---: |
| 0 | `300` | `250` | `0` |
| 1 | `360` | `300` | `2` |
| 2 | `420` | `350` | `4` |
| 3 | `480` | `400` | `6` |

Drag remains `1.2` at all levels.

### Tow Servos [Tier 1]

| Level | Tow power | Attach range | Max tow mass | Cost |
| ---: | ---: | ---: | ---: | ---: |
| 0 | `250` | `60` | `50` | `0` |
| 1 | `400` | `70` | `70` | `2` |
| 2 | `600` | `80` | `100` | `4` |
| 3 | `850` | `95` | `130` | `6` |

### Scanner [Tier 1/2]

| Level | Effect | Cost |
| ---: | --- | ---: |
| 0 | Basic minimap: station, player, active wrecks | `0` |
| 1 | Shows wreck mass, part yield, and integrity | `2` |
| 2 | Shows mines on minimap with warning radius | `3` |

### Total upgrade cost [Tier 1]

Maxing all upgrades costs:

```text
Hull: 2 + 4 + 6 = 12
Thrusters: 2 + 4 + 6 = 12
Tow Servos: 2 + 4 + 6 = 12
Scanner: 2 + 3 = 5
Total: 41
```

### Total parts available [Tier 1/2]

Computed from the wreck and contract tables:

```text
Wreck parts: 61
Contract rewards: 14
Total: 75
```

This guarantees that a player can always afford the required final upgrades if they salvage enough wrecks, and it prevents hard softlocks.

## 4.15 Contracts and progression [Tier 1/2]

### Contract rules [Tier 1/2]

- Only one contract is active at a time.
- Contracts `1` through `4` require salvage score.
- Contract `5` requires the final wreck.
- Wrecks in unlocked rings count toward the active score contract.
- During the final contract, only the Aurora Black Box counts toward contract progress.
- Other wrecks can still be salvaged for parts during the final contract.

### Contract table [Tier 1/2]

| Contract | Name | Requirement | Unlock | Reward |
| ---: | --- | --- | --- | ---: |
| 1 | First Shift | `20` salvage score | Ring 2 | `2` parts |
| 2 | Hauler Run | `60` salvage score | Ring 3 | `3` parts |
| 3 | Deep Field | `100` salvage score | Ring 4 | `4` parts |
| 4 | Heavy Salvage | `180` salvage score | Final Corridor | `5` parts |
| 5 | Aurora Black Box | Return the Aurora Black Box | Victory | — |

### Contract examples [Tier 2]

#### Contract 1

Requirement: `20`

Possible completion:

- 2 Scrap Cans: `10 + 10 = 20`

#### Contract 2

Requirement: `60`

Possible completion:

- 2 Transport Haulers + 1 Scrap Can: `25 + 25 + 10 = 60`

#### Contract 3

Requirement: `100`

Possible completion:

- 2 Fighter Frames + 1 Transport Hauler: `40 + 40 + 25 = 105`

#### Contract 4

Requirement: `180`

Possible completion:

- 3 Cargo Liners: `60 + 60 + 60 = `180`

### Recommended upgrade path [Tier 2]

This is not mandatory, but the contract board should recommend upgrades.

| After contract | Recommended upgrades |
| --- | --- |
| 1 | Tow Servos Level `1` or Thrusters Level `1` |
| 2 | Tow Servos Level `2`, Hull Plating Level `1` |
| 3 | Tow Servos Level `3`, Hull Plating Level `2`, Thrusters Level `2` |
| 4 | Scanner Level `1`, any remaining survivability upgrades |

### Required final upgrade [Tier 2]

The Aurora Black Box has mass `120`.

To tow it, the player needs:

- Tow Servos Level `3`.

Recommended final ship:

- Hull Plating Level `2` or higher.
- Thrusters Level `2` or higher.
- Tow Servos Level `3`.
- Scanner Level `1` or higher.

Minimum required to complete the final contract:

- Tow Servos Level `3`.

### Fallback rule [Tier 2]

If a score contract is active and no eligible active wrecks remain, automatically complete the contract and grant the reward.

This prevents a softlock in case of unexpected content depletion.

## 4.16 World layout and map generation [Tier 1/2]

The game uses one continuous world.

The station is at the center. Salvage rings expand outward from the station.

### Station [Tier 1]

- Position: `(0, 0)`
- Safe zone radius: `120`
- Dock zone radius: `50`
- The station safe zone has no debris and no mines.
- Hull regenerates inside the safe zone.
- The station is not a solid collision object.
- The dock zone is where unloading happens.

### World boundary [Tier 2]

- Outer boundary radius: `3200`
- No wrecks are placed beyond `3200`.
- If the ship crosses the boundary, apply a soft clamp:
  - Reduce outward velocity.
  - Show prompt: `No signal beyond boundary`.

### Rings [Tier 1/2]

| Ring | Radial range | Unlocked after | Content |
| --- | ---: | --- | --- |
| Ring 1 | `120–800` | Start | Tutorial wrecks, low hazards |
| Ring 2 | `800–1600` | Contract 1 | First haulers, first mines |
| Ring 3 | `1600–2400` | Contract 2 | Heavier wrecks, denser hazards |
| Ring 4 | `2400–3000` | Contract 3 | Cargo liners, final prep |
| Final Corridor | `3000–3200` | Contract 4 | Aurora Black Box |

### Content counts [Tier 2]

| Ring | Wrecks | Debris clusters | Mines |
| --- | --- | ---: | ---: |
| Ring 1 | `10` Scrap Cans | `8` | `0` |
| Ring 2 | `6` Transport Haulers, `4` Scrap Cans | `12` | `4` |
| Ring 3 | `4` Fighter Frames, `3` Transport Haulers | `16` | `8` |
| Ring 4 | `3` Cargo Liners, `4` Fighter Frames, `2` Transport Haulers | `20` | `12` |
| Final Corridor | `1` Aurora Black Box | `4` | `6` |

Total wrecks: `37`  
Total debris clusters: `60`  
Total mines: `30`

### Tutorial placement [Tier 1]

Two Ring 1 Scrap Cans are fixed for the tutorial:

- Scrap Can A: `(300, 0)`
- Scrap Can B: `(0, 300)`

The remaining Ring 1 wrecks are procedurally placed.

### Final wreck placement [Tier 2]

The Aurora Black Box is fixed at:

- `(0, -3000)`

It is only active after Contract 4 completes.

### Map generation algorithm [Tier 1/2]

Use a seeded random number generator at the start of a run.

#### Wreck placement

For each wreck count in a ring:

1. Choose a random angle.
2. Choose a random radius within the ring range.
3. Convert to X/Y position.
4. Reject the position if:
   - It is within `160` of the station center.
   - It is within `120` of another wreck.
   - It is within `80` of a debris cluster.
   - It is within `150` of the final wreck.
   - It is beyond the world boundary.
5. Accept the position if valid.
6. Retry up to `1000` times.
7. If still invalid, place it at the next valid angle in a spiral outward from the center of the ring.

#### Debris placement

For each debris cluster:

1. Sample a position in the ring.
2. Reject if:
   - It is within `120` of the station center.
   - It is within `100` of another debris cluster.
   - It is within `80` of a wreck.
   - It is within `50` of a mine.
3. Assign radius between `25` and `50`.

#### Mine placement

For each mine:

1. Sample a position in the ring or final corridor.
2. Reject if:
   - It is within `200` of the station center.
   - It is within `100` of another mine.
   - It is within `100` of a wreck.
   - It is within `50` of a debris cluster.
3. Accept if valid.

#### Locked rings [Tier 2]

- Wrecks in locked rings are not interactive.
- They are not shown on the minimap.
- They do not count toward contracts.
- They may be visually present as inert silhouettes, but no gameplay interaction is allowed until the ring unlocks.

## 4.17 Content sections [Tier 2]

### Section 1: Tutorial / First Shift [Tier 1]

Location:

- Station and Ring 1.

Objective:

- Teach movement, towing, docking, unloading, and upgrading.
- Complete Contract 1.

Content:

- `2` fixed tutorial Scrap Cans.
- `8` additional Scrap Cans.
- `8` debris clusters.
- No mines.

Tutorial prompts:

1. `Use A/D to rotate. Use W to thrust.`
2. `Approach a Scrap Can. Press Q to attach.`
3. `Tow it back to the station.`
4. `Hold U in the dock to unload.`
5. `Use parts to upgrade your ship.`

Expected player progression:

- Player earns at least `2` parts from wrecks.
- Player earns `2` contract reward parts.
- Player can afford one Level `1` upgrade.

### Section 2: Hauler Run [Tier 2]

Location:

- Ring 2.

Objective:

- Introduce heavier wrecks and first mines.
- Complete Contract 2.

Content:

- `6` Transport Haulers.
- `4` Scrap Cans.
- `12` debris clusters.
- `4` mines.

Expected player progression:

- Player learns that tow mass matters.
- Player should consider Tow Servos Level `1`.
- Player may buy Thrusters Level `1` for faster travel.

### Section 3: Deep Field [Tier 2]

Location:

- Ring 3.

Objective:

- Introduce Fighter Frames and denser hazards.
- Complete Contract 3.

Content:

- `4` Fighter Frames.
- `3` Transport Haulers.
- `16` debris clusters.
- `8` mines.

Expected player progression:

- Player needs Tow Servos Level `1` to tow Fighter Frames.
- Hull Plating Level `1` becomes useful.
- Scanner Level `1` becomes useful for mine avoidance.

### Section 4: Heavy Salvage [Tier 2]

Location:

- Ring 4.

Objective:

- Introduce Cargo Liners and prepare for the final wreck.
- Complete Contract 4.

Content:

- `3` Cargo Liners.
- `4` Fighter Frames.
- `2` Transport Haulers.
- `20` debris clusters.
- `12` mines.

Expected player progression:

- Player needs Tow Servos Level `2` to tow Cargo Liners efficiently.
- Player should aim for Tow Servos Level `3`.
- Hull and Thruster upgrades become important for the long final trip.

### Section 5: Aurora Black Box [Tier 2]

Location:

- Final Corridor.

Objective:

- Retrieve the Aurora Black Box.
- Win the game.

Content:

- `1` Aurora Black Box.
- `4` debris clusters.
- `6` mines.

Expected player progression:

- Player needs Tow Servos Level `3`.
- The final trip is long, so Thrusters and Hull matter.
- Scanner helps avoid final-corridor mines.

Victory condition:

- Unload the Aurora Black Box at the station.

## 4.18 Feel and pacing [Tier 1/2]

The game should feel like careful piloting, not action.

Key feelings:

- The ship should feel floaty but controllable.
- Towing should feel heavy.
- Returning with a heavy wreck should feel tense.
- The station should feel safe.
- Upgrades should feel meaningful immediately.
- Damage should be readable.
- Mines should create avoidable danger, not random punishment.

### Pacing goals [Tier 2]

| Phase | Target feel |
| --- | --- |
| Tutorial | Simple, safe, quick first success |
| Contract 2 | Slightly harder, first upgrade decision |
| Contract 3 | More planning, mine awareness |
| Contract 4 | Heavy wrecks, upgrade urgency |
| Final | Long tense return, payoff |

### Travel time feel [Tier 2]

At base speed:

- Ring 1 is very close.
- Ring 2 is a short trip.
- Ring 3 is a moderate trip.
- Ring 4 is a long trip.
- Final corridor is the longest and most dangerous.

Towing should noticeably slow the player:

- Level `0` towing feels sluggish.
- Level `1` towing feels workable.
- Level `2` towing feels comfortable.
- Level `3` towing feels fast but still heavy.

### Damage frequency [Tier 2]

The player should usually avoid most damage, but not always.

Expected:

- Early game: occasional small hull loss.
- Mid game: avoidable mine danger.
- Late game: one bad collision or mine can be serious.
- Final: hull upgrades matter.

### Upgrade pacing [Tier 2]

The player should usually be able to buy one useful upgrade after each contract.

The game should not require perfect salvage. The player can complete the game with imperfect upgrades as long as they have enough parts for Tow Servos Level `3`.

## 4.19 Edge cases [Tier 2]

### Attach failures

- If wreck mass exceeds max tow mass, attachment fails.
- If relative speed is too high, attachment fails.
- If player is already towing, attachment fails.
- If wreck is out of range, attachment fails.
- Each failure shows a clear prompt.

### Line snap

- If the tow line is overstressed, it snaps.
- The wreck remains in the world.
- The player can reattach later.

### Wreck at zero integrity

- A wreck at zero integrity can still be towed.
- It yields `0` parts.
- It still gives full score.
- This prevents damaged wrecks from becoming unfinishable.

### Final wreck at low integrity

- The Aurora Black Box can be damaged.
- It still completes the final contract when unloaded.
- Parts may be reduced or zero.
- Victory is not blocked by wreck integrity.

### Unload failure

- If the player is outside the dock zone, unload does not start.
- If speed is too high, unload does not start.
- If the player leaves the dock zone during unload, progress resets.
- If the player detaches during unload, unload cancels.

### Death while towing

- If the ship is destroyed while towing:
  - The towed wreck remains in the world.
  - The checkpoint restores the state from the last station entry.
  - If the wreck had not been unloaded, it is restored to its checkpoint state.
  - The player can reattach and continue.

### Death at station

- If the ship is destroyed while inside the station safe zone, the checkpoint is the current station state.
- The player respawns at the station with the checkpointed hull and progress.

### Boundary

- The ship cannot leave the world boundary.
- The towed wreck cannot leave the world boundary.
- If a towed wreck is pushed against the boundary, clamp its position and apply tow stress normally.

### Contract completion while towing

- Contract completion only happens after unload.
- Therefore, the player is not towing when a contract completes.

### All wrecks removed

- If all eligible wrecks for a score contract are unloaded and the contract is not complete, auto-complete the contract.
- This is a safety fallback.

### Final wreck unreachable by upgrades

- The final wreck can only be attached with Tow Servos Level `3`.
- The game provides enough total parts to reach Tow Servos Level `3`.
- If the player lacks Tow Servos Level `3`, they can continue salvaging other active wrecks for parts.

### Pause

- Pausing stops all simulation.
- The player can resume, retry the current contract, or restart the run.

# 5. CHARACTERS

## 5.1 Player ship

The player ship is a small salvage tug. It is the brightest player-controlled object in the world.

### Silhouette

- Arrow-like but rounded.
- Clear nose marker.
- Bright cyan hull edge.
- Dark cockpit.
- Rear thruster.
- Front tow hook.

### Base colors

| Part | Color |
| --- | ---: |
| Hull edge | `#55F1FF` |
| Hull body | `#103040` |
| Cockpit | `#F4F7FB` |
| Thruster flame | `#FF9A3D` with white core |

### Facing

- The ship faces its heading.
- Heading `0` points east.
- Positive heading rotates clockwise on screen.
- The camera does not rotate.
- The ship sprite rotates with the ship.

### Animations by name

| Animation | Trigger | Motion rule | Tier |
| --- | --- | --- | --- |
| Idle | No thrust, no brake | Ship faces heading, subtle servo idle | 1 |
| Thrust | Thrust input active | Orange/white flame from rear, flame length increases with speed, small particle trail, engine glow | 1/3 |
| Brake | Brake input active | Small white/blue reverse puff, slight exhaust fade, no dramatic effect | 1/3 |
| Turn | Rotate input active | Subtle servo animation, no visible trail unless thrusting | 1/3 |
| Towing | `towedWreckId` is not null | Front tow arm visible, tow line connected to wreck | 1/3 |
| Hull damage | Hull damage event | Red flash on hull, red vignette `150 ms`, hull bar flash, small spark or breach particles, shake up to `4 px` | 1/3 |
| Low hull | Hull below `30%` max hull | Ship outline pulses red at `2 Hz`, small warning particles, hull bar pulses | 3 |
| Destroyed | Hull reaches `0` | Explosion, tow line breaks if towing, red vignette, shake `6 px`, ship breaks into 4–6 fragments, fragments fade over `0.8 s`, then Game Over screen | 2/3 |

### Upgrade visuals

| Upgrade | Visual rule | Tier |
| --- | --- | --- |
| Hull Plating | Add visible armor plates. Level `1`: one side plate. Level `2`: two side plates. Level `3`: full plated hull. | 3 |
| Thrusters | Engine pods grow. Level `1`: single larger engine. Level `2`: dual engines. Level `3`: dual engines with visible exhaust glow. | 3 |
| Tow Servos | Front tow arm grows. Level `0`: small hook. Level `1`: medium clamp. Level `2`: large clamp. Level `3`: dual clamp with reinforced housing. | 3 |
| Scanner | Add dish/antenna. Level `1`: small dish and faint violet scan ring. Level `2`: larger dish and stronger scan ring. | 3 |

# 6. AUDIO

The builder has access to an audio API. All audio is synthesized. No external audio files are required. Gameplay must not depend on hearing audio. Every important audio cue has a visual equivalent.

## 6.1 Synthesized SFX

| Name | Recipe | When it plays | Tier |
| --- | --- | --- | --- |
| `ui_hover` | `1200 Hz` sine, `0.05 s`, exponential decay | UI hover | 4 |
| `ui_click` | `800 Hz` short click, `0.08 s` | UI click | 4 |
| `thrust_loop` | Low rumble + hiss: noise low-passed around `100–300 Hz` plus oscillator `40–80 Hz`; pitch increases with speed | While thrusting | 4 |
| `brake` | Soft reverse hiss, low-pass noise, `0.2 s` | While braking | 4 |
| `turn` | Subtle servo, quiet, `0.1 s` | While turning | 4 |
| `tow_attach` | `150 Hz` thump + `1500 Hz` latch, `0.25 s` | Tow attach succeeds | 4 |
| `tow_detach` | Release clank + slack, lower pitch than attach, `0.2 s` | Tow detach | 4 |
| `tow_stress_loop` | Creaking strain: low sawtooth `60–120 Hz` with amplitude modulation; pitch rises with stress ratio | While towing and stress ratio is high | 4 |
| `tow_snap` | `2000 Hz` snap + `1000 Hz` ping + `60 Hz` thud, `0.3 s` | Tow line snaps | 4 |
| `hull_damage` | `100 Hz` impact + `800 Hz` blip, `0.3 s` | Ship takes hull damage | 4 |
| `wreck_damage` | Metallic clang + sparks, `500 Hz`, `0.2 s` | Wreck takes damage | 4 |
| `mine_arm_loop` | High beep: `2000 Hz` square or sine, `2 Hz` rate, short repeated pulses | Mine armed | 4 |
| `mine_explosion` | `50 Hz` boom + noise burst, `0.8 s` | Mine explodes | 4 |
| `unload_start` | Servo + hum, `300 Hz`, `0.3 s` | Unload begins | 4 |
| `unload_complete` | Success chime + cargo drop: `800 Hz` + `1200 Hz`, `0.4 s` | Unload completes | 4 |
| `contract_complete` | Short fanfare: four-note warm chime, `0.6 s` | Contract completes | 4 |
| `ship_destroyed` | Explosion + hull breach: large boom + metallic break, `1.2 s` | Ship destroyed | 4 |
| `victory` | Warm victory chime: C major resolution, `1.0 s` | Victory screen | 4 |
| `boundary_warning` | Soft ping, `600 Hz`, `0.2 s` | Ship near or crossing boundary | 4 |
| `scanner_ping` | Sonar ping, `1000 Hz`, `0.1 s` | Scanner data appears | 4 |
| `upgrade_buy` | Servo + part click, satisfying mechanical click, `0.3 s` | Upgrade purchased | 4 |
| `part_pickup` | Small chime, `1500 Hz`, `0.1 s` | Parts added | 4 |

## 6.2 Synthesized music

| Name | Recipe | When it plays | Tier |
| --- | --- | --- | --- |
| `music_station` | Warm pad, soft pulse, C major, `60 BPM` | Title, station safe zone, upgrade menu | 4 |
| `music_field` | Ambient noise, sparse plucks, A minor, `70 BPM` | General salvage field, not towing | 4 |
| `music_tow` | Low ostinato, sub-bass, `80 BPM` | While towing | 4 |
| `music_stress` | Pulsing synth, metallic clicks, minor tension | Tow stress above `75%` | 4 |
| `music_final` | Darker, lower, sparse strings or synth, suspended A minor | Final corridor | 4 |
| `music_victory` | Warm C major, soft chord swell | Victory screen | 4 |
| `sfx_mine_stinger` | Short high mine stinger | Mine armed | 4 |
| `sfx_contract_complete` | Contract reward stinger | Contract complete | 4 |

## 6.3 Mixing rules

| Game state | Music mix |
| --- | --- |
| Title | Station `100%` |
| Station safe zone | Station `100%` |
| Field, not towing | Field `70%` |
| Towing | Field `60%` + Tow `50%` |
| Tow stress above `75%` | Add Stress `50%`, duck Field by `6 dB` |
| Mine armed | Play mine stinger, duck music by `10 dB` |
| Mine explosion | Duck music by `15 dB` for `1 second` |
| Final corridor | Final `80%` |
| Contract complete | Play contract complete stinger, music continues |
| Victory | Crossfade to Victory over `3 seconds` |
| Paused | Reduce music by `6 dB` |
| Game over | Stop music, play ship destroyed SFX, then low game-over drone |

Transition rules:

- Crossfade between music stems over `2 seconds`.
- Do not cut music abruptly except on death.
- SFX should not fight the music.
- Important SFX, such as mine arming and tow snap, should briefly duck the music.

## 6.4 Positional audio

For world SFX:

- Pan left/right based on object position relative to camera.
- Attenuate volume with distance.
- Distance curve:
  - `0–200` units: full volume.
  - `200–800` units: linear attenuation.
  - Beyond `800` units: `-18 dB`.

## 6.5 Volume balance

| Category | Reference level |
| --- | ---: |
| Music | `-12 dB` |
| World SFX | `0 dB` |
| UI SFX | `0 dB` |
| Critical SFX | `+3 dB` |

Critical SFX include:

- Mine armed.
- Mine explosion.
- Tow snap.
- Hull damage.
- Ship destroyed.
- Contract complete.

# 7. UX

The UX layer is HTML/CSS/DOM/SVG. The world may be rendered on canvas, but screens, HUD, prompts, menus, and minimap must be DOM/SVG-based.

## 7.1 Screen state machine

| State | Entry condition | Exit condition | Visible screen |
| --- | --- | --- | --- |
| `title` | Page load | `Enter` pressed | Title screen |
| `start` | From title | Simulation begins | Start state |
| `contractActive` | Ship outside safe zone | Ship enters safe zone | Normal HUD |
| `atStation` | Ship inside safe zone | Ship leaves safe zone | Station HUD, contract board |
| `upgradeMenu` | `Tab` or `I` while at station and not towing | `Tab`, `I`, or `Esc` | Upgrade menu overlay |
| `paused` | `P` or `Esc` while playing | Resume, Retry Contract, Restart Run | Pause overlay |
| `gameOver` | Ship hull reaches `0` | Retry Contract | Game Over panel |
| `victory` | Aurora Black Box unloaded | Play Again | Victory panel |

## 7.2 HUD table

| Element | Record field / source | When visible |
| --- | --- | --- |
| `#hud-hull-bar` | `ship.hull / ship.maxHull` | All in-game states |
| `#hud-hull-text` | `HULL {ship.hull} / {ship.maxHull}` | All in-game states |
| `#hud-speed` | `SPEED {round(length(ship.velocity))}` | All in-game states |
| `#hud-contract-name` | `contracts[activeContractIndex].name` | All in-game states |
| `#hud-contract-progress` | `contracts[activeContractIndex].currentScore / requiredScore` | Score contracts |
| `#hud-contract-final` | `Return the wreck to the station` | Final contract |
| `#hud-parts` | `PARTS {parts}` | All in-game states |
| `#minimap` | Station, player, active wrecks, unlocked rings, mines if scanner level allows | All in-game states |
| `#tow-status-free` | `TOW: Free` | Not towing |
| `#tow-status-towing` | `TOW: {wreck.name}`, `Mass {wreck.mass} / Max {ship.maxTowMass}`, `Integrity {percent}%` | Towing |
| `#stress-meter` | `tow.stressRatio` | Towing |
| `#prompt` | `prompts[0].text` | When a prompt is active |
| `#unload-ring` | `ship.unloadProgress / 2.0` | While unloading |
| `#scanner-card` | Wreck name, mass, part yield, integrity | Scanner Level `1`, within `200` of wreck |
| `#banner` | Contract complete, ring unlock, checkpoint saved | During banner |
| `#upgrade-menu` | Parts, upgrade tracks, levels, costs, buy buttons | `upgradeMenu` state |
| `#title-screen` | Title, subtitle, start prompt | `title` state |
| `#pause-panel` | Resume, Retry Contract, Restart Run | `paused` state |
| `#game-over-panel` | `SHIP DESTROYED`, contract name, progress, Retry Contract | `gameOver` state |
| `#victory-panel` | `SHIFT COMPLETE`, stats, Play Again | `victory` state |

## 7.3 Prompt priority

If multiple prompts are active, show the most important one first.

Priority order:

1. Failure prompts.
2. Action prompts.
3. Information prompts.

Examples:

- `Too fast to attach`
- `Cannot tow: mass exceeded`
- `Detach current tow first`
- `Out of range`
- `Q: Attach Tow`
- `Q: Detach Tow`
- `Hold U: Unload`
- `Speed too high to unload`
- `Tab: Refit`
- `Detach to refit`
- `No signal beyond boundary`
- `Tow line snapped`
- `Checkpoint saved`

Prompt style:

- Positive/action prompts: white text with cyan keycap.
- Warning prompts: yellow text.
- Failure prompts: red text.
- Success prompts: green text.

## 7.4 Minimap

Minimap scale:

- World radius `3200` maps to minimap radius `100 px`.
- North is up.

Minimap contents:

| Object | Visual |
| --- | --- |
| Station | Amber dot, `6 px` |
| Player | Cyan arrow, `8 px` |
| Scrap Can | Orange dot, `4 px` |
| Transport Hauler | Teal dot, `5 px` |
| Fighter Frame | Magenta dot, `6 px` |
| Cargo Liner | Mustard dot, `7 px` |
| Aurora Black Box | Gold/violet diamond, `10 px` |
| Mine, Scanner `1+` | Red dot, `3 px` |
| Mine, Scanner `2` | Red dot with `70`-unit warning circle |
| Ring boundaries | Faint white circles |
| Locked rings | Not shown |

# 8. DEBUG API

The debug API exposes direct state access and simulated player inputs. Basic debug functions are Tier 1. The full API is Tier 5.

## 8.1 Player input functions

| Function | Effect | Tier |
| --- | --- | --- |
| `debug.input(action, down)` | Sets input action down or up. Actions: `rotateLeft`, `rotateRight`, `thrust`, `brake`, `tow`, `unload`, `upgrade`, `pause`, `enter` | 1 |
| `debug.press(action)` | Simulates a key press for one step | 1 |
| `debug.release(action)` | Simulates a key release | 1 |

## 8.2 System debug functions

| Function | System reached | Effect | Tier |
| --- | --- | --- | --- |
| `debug.get()` | Global | Returns `G` | 1 |
| `debug.setSeed(seed)` | Map generation | Sets run seed and regenerates world | 2 |
| `debug.regenerateWorld()` | Map generation | Regenerates world from current seed | 2 |
| `debug.step(n)` | Simulation | Runs `n` fixed steps immediately | 1 |
| `debug.setTime(value)` | Simulation | Sets run time | 1 |
| `debug.setState(state)` | UX | Forces game state | 1 |
| `debug.setPaused(paused)` | Simulation | Sets pause state | 1 |
| `debug.setShipPosition(x, y)` | Ship | Sets ship position | 1 |
| `debug.setShipVelocity(x, y)` | Ship | Sets ship velocity | 1 |
| `debug.setHeading(value)` | Ship | Sets ship heading | 1 |
| `debug.setHull(value)` | Hull | Sets current hull | 1 |
| `debug.setMaxHull(value)` | Hull | Sets max hull | 1 |
| `debug.setParts(value)` | Economy | Sets parts | 1 |
| `debug.setTotalParts(value)` | Economy | Sets total parts collected | 1 |
| `debug.setWrecksSalvaged(value)` | Progression | Sets wrecks salvaged count | 2 |
| `debug.setHullLevel(value)` | Upgrades | Sets hull plating level | 1 |
| `debug.setThrusterLevel(value)` | Upgrades | Sets thruster level | 1 |
| `debug.setTowLevel(value)` | Upgrades | Sets tow servo level | 1 |
| `debug.setScannerLevel(value)` | Upgrades | Sets scanner level | 1 |
| `debug.setContractIndex(value)` | Contracts | Sets active contract index | 1 |
| `debug.setContractScore(value)` | Contracts | Sets active contract score | 1 |
| `debug.completeContract()` | Contracts | Completes active contract immediately | 1 |
| `debug.unlockRing(index)` | Progression | Unlocks ring | 2 |
| `debug.spawnWreck(tier, x, y)` | Wrecks | Spawns a wreck of given tier | 2 |
| `debug.setWreckIntegrity(id, value)` | Wrecks | Sets wreck integrity | 1 |
| `debug.setWreckState(id, state)` | Wrecks | Sets wreck state | 1 |
| `debug.setWreckPosition(id, x, y)` | Wrecks | Sets wreck position | 2 |
| `debug.setWreckVelocity(id, x, y)` | Wrecks | Sets wreck velocity | 2 |
| `debug.attachTow(wreckId)` | Tow | Attaches tow directly if possible | 1 |
| `debug.detachTow()` | Tow | Detaches current tow | 1 |
| `debug.setTowStressRatio(value)` | Tow | Forces stress ratio for testing | 3 |
| `debug.addDebris(x, y, radius)` | Hazards | Adds debris cluster | 2 |
| `debug.clearDebris()` | Hazards | Removes all debris | 2 |
| `debug.addMine(x, y)` | Hazards | Adds mine | 2 |
| `debug.clearMines()` | Hazards | Removes all mines | 2 |
| `debug.setMineState(id, state)` | Hazards | Sets mine state | 2 |
| `debug.explodeMine(id)` | Hazards | Forces mine explosion | 2 |
| `debug.saveCheckpoint()` | Checkpoint | Saves checkpoint now | 2 |
| `debug.loadCheckpoint()` | Checkpoint | Loads last checkpoint | 2 |
| `debug.setCameraZoom(value)` | Camera | Sets camera zoom | 3 |
| `debug.addShake(value)` | Camera | Adds screen shake | 3 |
| `debug.setMotionReduce(value)` | Presentation | Enables debug motion reduction | 3 |
| `debug.setAudioMuted(value)` | Audio | Mutes audio | 4 |

# 9. TESTS

These are high-level tests sufficient to prove each tier is done code-wise.

## 9.1 Tier 1 tests

| Test | Expected result |
| --- | --- |
| Deterministic seed | Same seed produces same fixed wreck positions. |
| Ship thrust | Holding thrust increases speed toward unladen max speed. |
| Ship brake | Holding brake reduces speed. |
| Ship turn | Turn input changes heading at `3.0 rad/s`. |
| Attach success | Near an active Scrap Can with low relative speed, `Q` attaches tow. |
| Attach failure | Out of range, too fast, mass exceeded, or already towing produces correct prompt. |
| Tow physics | Attached wreck is pulled toward ship by spring force. |
| Detach | Detaching leaves wreck with current velocity. |
| Unload conditions | Unload only starts inside dock zone, speed below `20`, towing, holding `U`. |
| Unload completion | After `2.0 s`, wreck is removed, score added, parts added. |
| Upgrade purchase | Buying an affordable upgrade reduces parts and changes ship stats. |
| Contract 1 | Completing `20` score completes Contract 1 and grants reward. |
| Provisional victory | After Contract 1 in Tier 1, provisional victory screen appears. |
| Pause | Pausing stops simulation. |
| Basic debug | `debug.setHull`, `debug.setParts`, `debug.step` work. |

## 9.2 Tier 2 tests

| Test | Expected result |
| --- | --- |
| Full map counts | World contains `37` wrecks, `60` debris clusters, `30` mines. |
| Ring unlock | Completing contracts unlocks Ring 2, Ring 3, Ring 4, Final Corridor. |
| Locked wrecks | Locked ring wrecks are not interactive and not on minimap. |
| Debris collision | Colliding with debris at speed above threshold damages ship or towed wreck. |
| Mine arming | Entering proximity arms mine; fuse is `0.4 s`. |
| Mine explosion | Explosion damages ship/wreck within `70` units and destroys mine. |
| No mine chain | One explosion does not trigger other mines. |
| Hull death | Hull `0` triggers Game Over. |
| Checkpoint restore | Death restores contract score, parts, upgrades, wreck integrity, mine states, ship position. |
| Final wreck | Aurora Black Box can only be attached with Tow Servos Level `3`. |
| Final victory | Unloading Aurora Black Box triggers Victory. |
| Fallback | If no eligible active wrecks remain for a score contract, contract auto-completes. |
| Boundary clamp | Ship and towed wreck cannot pass radius `3200`. |

## 9.3 Tier 3 tests

| Test | Expected result |
| --- | --- |
| Safe zone visual | Safe zone renders cyan dashed field radius `120`. |
| Dock zone visual | Dock zone renders green ring radius `50`. |
| Tow line states | Line color changes at stress ratios `0.75`, `1.0`, `1.25`. |
| Snap warning | Snap timer arc appears when stress exceeds `1.25`. |
| Scanner card | Scanner Level `1` shows wreck data within `200` units. |
| Mine warning | Scanner Level `2` shows nearby warning circles. |
| Minimap | Minimap shows station, player, active wrecks, unlocked rings, mines when allowed. |
| Accessibility | Critical states are readable without relying on color alone. |
| Particle budget | Particle counts stay within section 3 budgets. |

## 9.4 Tier 4 tests

| Test | Expected result |
| --- | --- |
| SFX triggers | Attach, detach, damage, mine, unload, contract, death, victory play correct SFX. |
| Music states | Music changes for title, station, field, towing, stress, final, victory, pause, game over. |
| Ducking | Mine arming and explosion duck music. |
| Positional audio | World SFX pan and attenuate by distance. |
| Audio independence | All critical gameplay information remains visible with audio muted. |

## 9.5 Tier 5 tests

| Test | Expected result |
| --- | --- |
| Debug API | All section 8 functions exist and mutate state correctly. |
| Input simulation | Debug input functions can drive the game. |
| Tier tests | `tests.runTier(1)` through `tests.runTier(4)` pass. |
| Performance | Game runs at target frame rate with full content and effects. |
| Sanity | Section A checks pass. |

# 10. BUILD ORDER

1. Scaffold HTML, CSS, canvas/DOM mount, fixed-step loop.
2. Implement config tables and constants.
3. Implement seeded RNG and deterministic world generation for Tier 1.
4. Implement input system.
5. Implement ship movement, drag, turn, hull, and boundary clamp.
6. Implement station safe zone, dock zone, unload, score, and parts.
7. Implement tow attach, detach, spring-damper, stress, and snap.
8. Implement wreck integrity, parts yield, and Scrap Can content.
9. Implement upgrade menu and all four upgrade tracks.
10. Implement Contract 1 and provisional victory.
11. Implement minimal HUD, prompts, pause, and basic debug.
12. Implement full map generation for all rings, wrecks, debris, and mines.
13. Implement full contracts, ring unlocks, scanner, checkpoint/death, final wreck, and final victory.
14. Implement full visual spec: parallax, station, zones, ship/wreck/mine visuals, tow line states, effects, minimap, scanner card, banners, popups.
15. Implement synthesized audio: SFX, music stems, mixing, ducking, positional audio.
16. Implement full debug API and automated tier tests.
17. Run sanity checks and performance checks.

# 11. DEFINITION OF DONE

## Tier 1: Core vertical slice

High level: A new player can start the game, move the ship, tow a Scrap Can, unload it, earn parts, buy an upgrade, complete Contract 1, and see a provisional victory.

- [ ] Title screen starts the game.
- [ ] Fixed-step simulation runs deterministically.
- [ ] Ship movement, turn, thrust, and brake work.
- [ ] Station safe zone and dock zone are functional.
- [ ] Hull regenerates in safe zone.
- [ ] Scrap Can wrecks exist and are unloadable.
- [ ] Tow attach and detach work.
- [ ] Tow line spring-damper works.
- [ ] Unload requires dock zone, low speed, towing, and hold input.
- [ ] Unload adds score and parts.
- [ ] Upgrade menu opens at station.
- [ ] Upgrades change ship stats.
- [ ] Contract 1 completes at `20` score.
- [ ] Provisional victory appears after Contract 1.
- [ ] Pause stops simulation.
- [ ] Basic debug functions work.

## Tier 2: Full content and failure states

High level: The full designed run is playable from start to final victory, including hazards, death, checkpointing, all contracts, all wreck tiers, and the final Aurora Black Box.

- [ ] Full world generates with correct counts.
- [ ] Rings unlock after contracts.
- [ ] All wreck tiers exist with correct stats.
- [ ] Debris clusters damage ship and towed wrecks.
- [ ] Mines arm, explode, and do not chain-react.
- [ ] Scanner levels work.
- [ ] Checkpoint saves and restores correctly.
- [ ] Death loads checkpoint and respawns at station.
- [ ] Contracts 2–5 work.
- [ ] Final Aurora Black Box requires Tow Servos Level `3`.
- [ ] Unloading Aurora Black Box triggers Victory.
- [ ] Fallback auto-complete works.
- [ ] Boundary clamp works.
- [ ] Locked rings are non-interactive and hidden from minimap.

## Tier 3: Presentation

High level: The game visually matches the merged visual spec and remains readable and accessible.

- [ ] Parallax background layers render.
- [ ] Station, safe zone, dock zone, and contract board render.
- [ ] Ship renders with correct silhouette and upgrade visuals.
- [ ] Wrecks render by tier, state, and integrity.
- [ ] Debris and mines render with correct states.
- [ ] Tow line shows normal, moderate, high, and snap warning states.
- [ ] Stress meter renders while towing.
- [ ] Scanner data card renders.
- [ ] Minimap renders all allowed objects.
- [ ] Prompts, popups, and banners render.
- [ ] Effects stay within particle budgets.
- [ ] Screen shake is limited to impact events and capped at `6 px`.
- [ ] Critical information is visible without audio.
- [ ] Colorblind readability rules are followed.

## Tier 4: Audio

High level: The game has synthesized SFX and music that match the merged audio design.

- [ ] Audio API initializes.
- [ ] All SFX in section 6.1 are synthesized and trigger correctly.
- [ ] All music stems in section 6.2 are synthesized.
- [ ] Music state changes correctly.
- [ ] Ducking rules work.
- [ ] Positional audio works for world SFX.
- [ ] Muting audio does not hide critical gameplay information.

## Tier 5: Verification and polish

High level: The builder can prove the game is done using the debug API and tests.

- [ ] Full debug API exists.
- [ ] Player input debug functions work.
- [ ] One debug function per gameplay system reaches state directly.
- [ ] Tier tests run and pass.
- [ ] Performance is acceptable with full content and effects.
- [ ] Sanity checks in section A pass.

# A. SANITY

| Check | Result | Notes |
| --- | --- | --- |
| Engineering document empty | Fixed | Section 2, 8, 9, 10, and 11 fill the missing engineering design. |
| Tow clamp vs snap contradiction | Fixed | Section 4.10 now hard-caps applied tow force at `1.5 * tow_power` and snaps at stress ratio `>1.25` for `0.5 s`. |
| Expected tugged speed inconsistency | Fixed | Section 4.10 marks the tugged speed table as non-binding design intent. Spring constants remain authoritative. |
| Total parts discrepancy | Fixed | Section 0.2 and 4.14 rule that computed total is `75`, superseding the stated `77`. |
| Checkpoint refresh ambiguity | Fixed | Section 4.13 and 0.2 define checkpoint refresh while inside safe zone. |
| Mine disarm ambiguity | Fixed | Section 4.11 rules that armed mines cannot be disarmed. |
| Restitution missing | Fixed | Section 4.5 sets restitution to `0.2`. |
| Wreck-wreck collision missing | Fixed | Section 4.5 and 0.2 define wreck-wreck collisions. |
| Debris-wreck damage missing | Fixed | Section 4.5 and 0.2 define debris-wreck damage using the wreck damage formula. |
| Camera zoom missing from gameplay | Fixed | Visual zoom rule adopted in section 4.6. |
| Screen shake scope | Fixed | Shake limited to impact events, max `6 px`, no tow stress shake. |
| External assets | Fixed | Asset list and Python snippets dropped; procedural rendering required. |
| External audio files | Fixed | Audio file names dropped; synthesized audio required. |
| HUD implementation constraint | Fixed | Section 7 requires HTML/CSS/DOM/SVG for UX. |
| Coordinate orientation | Fixed | Section 1.1 defines Y positive down, so final wreck at `(0, -3000)` is visually north. |
| Turn direction | Fixed | Section 1.1 defines positive heading clockwise on screen. |
| Locked wrecks | Fixed | Locked wrecks may be visible but are not interactive and not on minimap. |
| Scanner warning radius | Fixed | Scanner Level 2 includes world warning circles within `250` units. |
| Contract fallback | Fixed | Fallback applies to score contracts only. |
| Tier tags | Valid | Every major system in section 4 has a tier tag. |
| Debug coverage | Valid | Section 8 includes one function per major gameplay system and player input functions. |
| Tests tied to definition of done | Valid | Section 9 tests correspond to section 11 tier definitions. |