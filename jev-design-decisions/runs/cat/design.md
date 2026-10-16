# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Game prompt: player is a cat trying to catch mice | §0.2, §4, §5 |
| Dimension: 2D | §1.1, §3, §4.14 |
| Camera: top-down | §1.1, §3, §4.14 |
| Players: single player | §0.2, §7 |
| Time model: real-time | §1.1, §4 |
| Movement model: free movement | §1.1, §4.1 |
| Session shape: sequence of levels | §0.2, §4.20, §7 |
| Failure: restart the level | §4.8, §4.22, §7 |
| Tone: silly | §3, §4, §5, §6 |
| Size: a handful of levels, under 30 minutes | §0.2, §4.20 |
| Win/lose condition: reach the exit | §4.6, §4.22 |
| Mechanics: dash, boosts, chase and catch, objectives, difficulty ramp, spawn points, score, traps, landmarks, unlocks, decoration, collectibles, melee attack, medals / ranks, secrets, rewards, collectible creatures, hints, keys and locked doors, combos, abilities / special moves, switches and doors, map / world, noise, high scores, puzzle types | §4 |
| Art style: flat vector | §3 |
| Palette: saturated bright colours | §3 |
| Typography: hand-lettered | §3, §7 |
| Music: chiptune | §6 |
| Sound effects style: retro bleeps | §6 |
| Screens: title, pause, settings, game over, win, level select, high scores | §7 |
| HUD: score, combo counter | §7 |
| Effects: particles, hit flash, trails | §3, §4.23 |
| Accessibility: colour-blind safe palette, reduced motion, remappable keys, difficulty options | §3, §4.20, §7 |

## 0.2 Decisions

| Decision | Final Value | Why |
| --- | --- | --- |
| Game prompt | Cat chasing and catching mice | User request. |
| Dimension | 2D | Given final decision. |
| Camera | Top-down | Given final decision. |
| Player count | Single player | Given final decision. |
| Time model | Real-time, fixed 60 Hz logic | Given real-time; fixed logic keeps gameplay deterministic and testable. |
| Movement model | Free 2D movement | Given final decision. |
| Session shape | Sequence of 7 levels | “Handful” means 7 levels; 7 levels supports a clear ramp and under-30-minute play. |
| Failure | Touching a danger trap restarts the current level | Gives a clear fail without adding health/lives systems. |
| Tone | Silly, bright, low stakes | Given tone. |
| Size | 7 levels, target 22–30 minutes | Fits “handful” and “under 30 minutes”. |
| Win/lose condition | Reach the exit after required mice are caught | Uses given win/lose while making cat catching mice the objective. |
| Art style | Flat vector | Given final decision. |
| Palette | Saturated, colour-blind safe, shape-coded | Given palette plus accessibility requirement. |
| Typography | Hand-lettered cursive with per-character jitter | Given final decision. |
| Music | Chiptune | Given final decision. |
| Sound effects | Retro synthesized bleeps | Given final decision. |
| Screens | Exactly title, pause, settings, game over, win, level select, high scores | Given final screen list. |
| HUD | Exactly score and combo counter | Given final HUD list. |
| Effects | Exactly particles, hit flash, trails | Given final effects list. |
| Accessibility | Colour-blind safe palette, reduced motion, remappable keys, difficulty options | Given final accessibility list. |
| Game name | “Whisker Panic” | Short, silly, fits cat theme. |
| Player identity | Sir Pounce, an orange cat | Gives player a silly identity without adding narrative systems. |
| Target creatures | Mice are the catchable targets | Directly from prompt. |
| Optional creatures | Special “Collectible Mice” | Fills “collectible creatures” without adding a new species system. |
| Level count | 7 | Concrete interpretation of “a handful”. |
| Base canvas | 800 × 600 logical pixels | Standard browser size, easy to scale. |
| World coordinates | Pixels, x right, y down | Simple browser canvas convention. |
| Player base speed | 220 px/s | Feels responsive but avoidable. |
| Dash speed | 360 px/s for 0.14 s | Dash is useful but not permanent speed. |
| Dash cooldown | 0.75 s Classic | Prevents spam while allowing skill. |
| Pounce range | 34 px capsule, 13 px radius | Melee feel without being too generous. |
| Pounce cooldown | 0.45 s Classic | Encourages deliberate catches. |
| Mouse base wander speed | 120 px/s | Slow enough to chase. |
| Mouse flee speed | 220 px/s base, level-scaled | Creates chase tension. |
| Combo timer | 3.0 s Classic | Clear combo pressure. |
| Combo cap | 3.0× multiplier | Prevents score runaway. |
| Score base: common mouse | 100 | Core reward. |
| Score base: special mouse | 500, final level 600 | Optional reward is strong. |
| Score base: cheese | 50 | Pickup reward. |
| Score base: turbo cheese | 100 | Boost reward. |
| Score base: key | 200 | Progression reward. |
| Level completion bonus | 500, final level 1000 | Rewards finishing. |
| Fail condition | Danger trap contact | Simple, readable, no health system. |
| Trap types | Snap trap, cheese spinner, yarn ball | Gives fail and non-fail trap variety within “traps”. |
| Door types | Exit door, key door, switch door | Uses keys/doors and switches/doors. |
| Key system | Shape-coded keys: circle, square, diamond | Colour-blind safe; multiple keys matter. |
| Switch system | Plate switches and pounce levers | Gives simple puzzle interaction without adding a separate interact key. |
| Noise mechanic | Cat movement, dash, pounce, special create noise events that alert mice | Uses listed “noise” meaningfully. |
| Secret mechanic | One secret alcove per level containing the special mouse | Uses “secrets” and “collectible creatures” together. |
| Hints | Timed text hints when stuck | Uses listed “hints”. |
| Medals | Bronze/Silver/Gold per level, medal points 1/2/3 | Supports ranks and unlocks. |
| Rank | Based on total medal points, max 21 | Gives long-session reward. |
| Unlocks | Levels unlock sequentially; abilities unlock by medal points | Uses listed unlocks. |
| Abilities | 3 passive unlocks plus 1 special move | Uses “abilities / special moves” without a shop. |
| High scores | Top 10 level-clear entries plus per-level bests | Concrete high score content. |
| Difficulty options | Careful, Classic, Zippy | Uses listed difficulty options without changing core rules. |
| Reduced motion | Disables trails, reduces particles, static noise rings, no shake-like effects | Meets accessibility. |
| Remappable keys | All gameplay keys remappable | Meets accessibility. |
| Save system | localStorage for progress, high scores, settings | Needed for persistence. |
| No assets | All art canvas/vector, all audio Web Audio | Fits browser build and flat vector style. |
| Determinism | Seeded xorshift32 RNG, fixed-step loop | Needed for tests and consistent levels. |

## 0.3 Tiers

Tier 1 is the minimal viable game: one playable level, core cat chase/catch loop, score/combo, fail/restart, win, basic screens, basic HUD, basic art/audio.

Tier 2 is the full content game: all 7 levels, all listed mechanics, difficulty options, remappable keys, settings, medals, high scores, secrets, collectible creatures, hints, switches, keys, traps, boosts, noise, progress.

Tier 3 is the polished progression game: abilities/special moves, ranks, full rewards, reduced-motion polish, full effects, persistence, final win presentation.

| System | Tier |
| --- | --- |
| Fixed loop, RNG, canvas, input, camera, world/collision | 1 |
| Cat movement, dash, pounce, basic catch | 1 |
| Common mice, required objective, exit, score, combo | 1 |
| Snap traps, fail/restart, basic game over | 1 |
| Title, level select, pause, game over, win, basic HUD | 1 |
| Basic flat vector art, basic chiptune/SFX | 1 |
| All 7 levels, difficulty ramp | 2 |
| Cheese/turbo/key pickups, boosts | 2 |
| Cheese spinner, yarn ball traps | 2 |
| Keys and key doors | 2 |
| Plate switches, pounce levers, switch doors | 2 |
| Noise events and mouse hearing | 2 |
| Mouse doze state | 2 |
| Landmarks and decoration | 2 |
| Secrets and collectible creatures | 2 |
| Hints | 2 |
| Medals, level rewards, unlocks, high scores | 2 |
| Settings, difficulty options, remappable keys, reduced motion | 2 |
| Passive abilities | 3 |
| Purr Burst special move | 3 |
| Ranks and collection suffix | 3 |
| Full particles/trails/hit flash polish | 3 |
| Full audio variations and final win presentation | 3 |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Quantity | Unit / Value |
| --- | --- |
| Coordinate axis | x increases right, y increases down |
| Position | pixels |
| World size | pixels |
| Speed | pixels per second, px/s |
| Acceleration | pixels per second squared, px/s² |
| Radius | pixels |
| Time | seconds |
| Logic step | fixed `dt = 1 / 60` s |
| Target render | requestAnimationFrame, latest state |
| Max accumulated frame time | 0.25 s |
| Logical viewport | 800 × 600 px |
| Player radius | 16 px |
| Mouse radius | 10 px |
| Pickup radius | 12 px |
| Snap trap hit radius | 18 px |
| Cheese spinner hit radius | 18 px |
| Yarn ball hit radius | 14 px |
| Pounce capsule | 34 px long, 13 px radius |
| Facing | normalized 2D vector |
| Diagonal movement | normalized to length 1 |
| Collision | circle vs AABB walls/doors, circle vs circle entities |
| Level origin | top-left of level world is `(0, 0)` |

## 1.2 Important conventions

1. Use ES modules. All gameplay state lives in `Game.context`.
2. Use a fixed-step loop: accumulate real time, step gameplay in `1/60` s increments.
3. Render after all logic steps. Do not mix render timing into gameplay rules.
4. Use `context.rng` for all gameplay randomness. Do not use `Math.random()` in gameplay.
5. RNG is xorshift32. Seed formula:
   `seed = 0x9E3779B9 ^ (levelIndex * 0x85EBCA6B) ^ difficultyIndex * 0xC2B2AE35`.
6. Use `PALETTE` constants for colours. Do not scatter raw hex values through modules.
7. Use `ACCESSIBILITY` flags before creating effects.
8. Use the listed screens only. No extra screens.
9. Use the listed HUD elements only: score and combo counter.
10. Use the listed effects only: particles, hit flash, trails. No camera shake.
11. Colour-blind safety is always on: danger, keys, doors, and special creatures use shape/icon cues, not colour alone.
12. All UI is HTML/CSS. The canvas renders the world only.
13. Persist only progress, high scores, and settings in `localStorage` under `whiskerPanic.v1`.
14. No external image or audio assets. Draw vector shapes; synthesize audio with Web Audio.
15. Mice are immune to traps. Traps affect the cat only.
16. Closed doors block the cat, mice, noise, and sight. Open doors do not block.
17. Decorations do not block movement unless explicitly represented as walls in level data.
18. All timers count down in seconds using fixed `dt`.
19. A level is complete only when the exit door is open and the cat overlaps the exit.
20. Failure is immediate on danger trap contact and restarts the same level.

# 2. CONTRACTS

## 2.1 Module layout

```text
index.html
style.css
main.js

src/core/loop.js
src/core/rng.js
src/core/input.js
src/core/storage.js
src/core/audio.js
src/core/particles.js

src/state/context.js
src/state/screens.js

src/render/camera.js
src/render/draw.js

src/game/levels.js
src/game/player.js
src/game/mouse.js
src/game/traps.js
src/game/pickups.js
src/game/doors.js
src/game/switches.js
src/game/noise.js
src/game/score.js
src/game/hints.js
src/game/progress.js

src/debug/debug.js
```

## 2.2 Global context

```ts
interface GameContext {
  now: number;
  frame: number;
  state:
    | "title"
    | "levels"
    | "playing"
    | "paused"
    | "settings"
    | "gameover"
    | "win";
  previousState: string;

  difficulty: "careful" | "classic" | "zippy";
  accessibility: {
    reducedMotion: boolean;
    colorBlindSafe: boolean;
    remaps: Record<ActionKey, string>;
  };

  rng: Xorshift32;

  levelIndex: number;
  level: LevelRecord | null;

  player: PlayerRecord;
  mice: MouseRecord[];
  traps: TrapRecord[];
  pickups: PickupRecord[];
  doors: DoorRecord[];
  switches: SwitchRecord[];
  noise: NoiseEvent[];

  score: number;
  combo: number;
  comboTimer: number;
  multiplier: number;
  caughtCommon: number;
  caughtSpecial: number;

  hint: HintRecord | null;
  hintCooldown: number;

  effects: {
    particles: ParticleRecord[];
    trails: TrailRecord[];
    flashes: FlashRecord[];
  };

  progress: ProgressRecord;
  audio: {
    music: string | null;
  };

  debug: {
    godMode: boolean;
    showHitboxes: boolean;
  };
}
```

### PlayerRecord

```ts
interface PlayerRecord {
  x: number;
  y: number;
  vx: number;
  vy: number;
  facingX: number;
  facingY: number;
  radius: number;
  baseSpeed: number;
  speedMultiplier: number;

  boostTime: number;
  dashTime: number;
  dashCooldown: number;
  pounceTime: number;
  pounceCooldown: number;
  stunTime: number;
  noiseTimer: number;

  specialCooldown: number;
  specialTime: number;

  abilities: {
    nimblePaws: boolean;
    longSnout: boolean;
    purrBurst: boolean;
  };
}
```

### MouseRecord

```ts
interface MouseRecord {
  id: string;
  type: string;
  isCommon: boolean;
  isSpecial: boolean;
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  state: "wander" | "alert" | "doze" | "stunned" | "caught";
  stateTimer: number;
  dozeTimer: number;
  speedFactor: number;
  collected: boolean;
}
```

### TrapRecord

```ts
interface TrapRecord {
  id: string;
  type: "snap" | "spinner" | "yarn";
  x: number;
  y: number;
  vx: number;
  vy: number;
  waypoints: { x: number; y: number }[];
  waypointIndex: number;
  speed: number;
  hitRadius: number;
  danger: boolean;
  flash: number;
}
```

### PickupRecord

```ts
interface PickupRecord {
  id: string;
  type: "cheese" | "turbo" | "key" | "secretCheese";
  keyShape?: "circle" | "square" | "diamond";
  x: number;
  y: number;
  radius: number;
  collected: boolean;
}
```

### DoorRecord

```ts
interface DoorRecord {
  id: string;
  type: "exit" | "key" | "switch";
  x: number;
  y: number;
  w: number;
  h: number;
  open: boolean;
  keyShape?: "circle" | "square" | "diamond";
  switchId?: string;
  timer: number;
}
```

### SwitchRecord

```ts
interface SwitchRecord {
  id: string;
  type: "plate" | "lever";
  x: number;
  y: number;
  linkedDoorId: string;
  used: boolean;
  cooldown: number;
  timer: number;
  secret: boolean;
}
```

### NoiseEvent

```ts
interface NoiseEvent {
  x: number;
  y: number;
  maxRadius: number;
  age: number;
  duration: number;
  intensity: number;
}
```

### Effect records

```ts
interface ParticleRecord {
  x: number;
  y: number;
  vx: number;
  vy: number;
  color: string;
  size: number;
  age: number;
  maxAge: number;
}

interface TrailRecord {
  x: number;
  y: number;
  age: number;
  maxAge: number;
  color: string;
}

interface FlashRecord {
  target: string;
  age: number;
  maxAge: number;
}
```

### HintRecord

```ts
interface HintRecord {
  text: string;
  age: number;
  maxAge: number;
  trigger: string;
}
```

### ProgressRecord

```ts
interface ProgressRecord {
  unlockedLevel: number;
  medalsByLevel: (null | "bronze" | "silver" | "gold")[];
  medalPoints: number;
  collectedCreatures: Record<string, boolean>;
  bestByLevel: {
    score: number;
    combo: number;
    medal: null | "bronze" | "silver" | "gold";
  }[];
  highScores: {
    levelIndex: number;
    levelName: string;
    score: number;
    combo: number;
    medal: null | "bronze" | "silver" | "gold";
    ts: number;
  }[];
  settings: {
    difficulty: "careful" | "classic" | "zippy";
    reducedMotion: boolean;
    remaps: Record<ActionKey, string>;
  };
}
```

## 2.3 Module specifics

| Module | Required exports / functions |
| --- | --- |
| `loop.js` | `createLoop(update, render, maxFrame)`, `stopLoop()` |
| `rng.js` | `createRng(seed)`, `rng.nextFloat()`, `rng.nextInt(min, max)`, `rng.pick(arr)` |
| `input.js` | `createInput(remaps)`, `input.setMove(x, y)`, `input.press(action)`, `input.release(action)`, `input.saveRemaps(remaps)`, `input.loadRemaps()` |
| `storage.js` | `loadProgress()`, `saveProgress(progress)`, `defaultProgress()` |
| `audio.js` | `initAudio()`, `playSfx(name)`, `startMusic(name)`, `stopMusic()`, `resumeAudio()` |
| `particles.js` | `spawnBurst(ctx, x, y, color, count)`, `spawnTrail(ctx, x, y, color)`, `spawnFlash(ctx, target, duration)`, `updateEffects(ctx, dt)`, `drawEffects(ctx2d, camera)` |
| `context.js` | `createContext()`, `resetLevelContext(ctx, levelIndex)` |
| `screens.js` | `setScreen(ctx, name)`, `bindScreens(ctx, dom)`, `showWin(ctx)`, `showGameOver(ctx)` |
| `camera.js` | `updateCamera(ctx, dt)`, `cameraToScreen(ctx, worldX, worldY)` |
| `draw.js` | `drawWorld(ctx2d, ctx, camera)`, `drawPlayer()`, `drawMouse()`, `drawTrap()`, `drawPickup()`, `drawDoor()`, `drawSwitch()`, `drawNoise()` |
| `levels.js` | `LEVELS`, `getLevel(index)`, `loadLevel(ctx, index)`, `validateLevel(level)` |
| `player.js` | `updatePlayer(ctx, dt, input)`, `tryDash(ctx)`, `tryPounce(ctx)`, `trySpecial(ctx)`, `emitPlayerNoise(ctx, maxRadius)`, `onDangerTrapHit(ctx)`, `onYarnHit(ctx, trap)` |
| `mouse.js` | `spawnMice(ctx, level)`, `updateMouse(ctx, mouse, dt)`, `reactToNoise(ctx, mouse, noise)`, `reactToCat(ctx, mouse)`, `catchMouse(ctx, mouse)`, `rollDoze(ctx, mouse, dt)` |
| `traps.js` | `updateTraps(ctx, dt)`, `trapHitsPlayer(ctx, trap)`, `onDangerTrap(ctx, trap)`, `onYarnTrap(ctx, trap)` |
| `pickups.js` | `updatePickups(ctx, dt)`, `collectPickup(ctx, pickup)` |
| `doors.js` | `updateDoors(ctx, dt)`, `openDoor(ctx, door)`, `closeDoor(ctx, door)`, `exitReady(ctx)`, `playerAtExit(ctx)` |
| `switches.js` | `updateSwitches(ctx, dt)`, `activateSwitch(ctx, switchRec)`, `leverPounceCheck(ctx)`, `plateOverlapCheck(ctx)` |
| `noise.js` | `emitNoise(ctx, x, y, maxRadius, intensity)`, `updateNoise(ctx, dt)`, `mouseHearsNoise(ctx, mouse, noise)`, `lineOfSightClear(ctx, x1, y1, x2, y2)` |
| `score.js` | `addScore(ctx, base)`, `updateCombo(ctx, dt)`, `completeLevel(ctx)`, `awardMedal(ctx, level, score)`, `medalForScore(level, score)` |
| `hints.js` | `updateHints(ctx, dt)`, `showHint(ctx, text, trigger)`, `canHint(ctx)` |
| `progress.js` | `recordWin(ctx, score, combo, medal)`, `unlockNextLevel(ctx)`, `abilityUnlocks(ctx)`, `rankFor(points, allCreatures)`, `saveAfterWin(ctx)` |
| `debug.js` | All Debug functions in §8 |

# 3. VISUAL SPEC

The game looks like a bright, flat vector cartoon: a silly orange cat zips around top-down rooms while blue, purple, and pink mice scurry, nap, and flee. Every shape is a clean vector silhouette with a crisp black outline and solid saturated fill. The rooms feel like playful kitchen/attic/maze spaces: thick dark walls, cream or pale blue floors, bold rugs, simple landmarks, and tiny decorative props. There is no realistic lighting; only a subtle flat shadow under movable entities. The UI uses hand-lettered cursive text with slight per-character rotation, making the world feel like a cheerful retro cartoon.

Lighting and atmosphere: top-down flat lighting. No dynamic light, no gradients. Entity shadows are 20% black ellipses, 18 px wide and 8 px tall, placed 4 px below the entity. The atmosphere is bright and silly: high contrast, saturated colours, clean edges.

Space: each level is a rectangular top-down room with walls at least 16 px thick. The camera viewport is 800 × 600 px and follows the player with lerp factor `8 * dt`, clamped to the level bounds. Early levels fit mostly in one screen; later levels scroll.

| Element | Shape / Colour | Motion / Effect | Rule cue |
| --- | --- | --- | --- |
| Sir Pounce, cat | Orange circle body, black outline, triangle ears, curved tail, small nose | Idle tail wag, run squash, dash stretch, pounce nose lunge, stun spin | Player. Facing nose shows movement direction. |
| Common mouse | Oval body, big triangle ears, thin tail. Colours: Mousa cyan, Mousse purple, Nib pink | Wander bob, flee stretch, doze Zzz, caught pop | Catchable target. Dozing mice can be caught by touch. |
| Special collectible mouse | Unique overlay: diamond, crescent, star, shell, bolt, berry, star-sprinkle | Same mouse animations plus glow trail | Optional collectible creature. Adds to collection. |
| Snap trap | Red rectangle with black X shape | Hit flash, fail burst | Danger trap: immediate fail. |
| Cheese spinner | Orange wheel with triangle cutout | Rotates while moving | Danger trap: immediate fail. |
| Yarn ball | Pink circle with black swirl | Bounces, squashes on bounce | Stun trap: 0.9 s stun and knockback, not fail. |
| Cheese puff | Yellow square with small white cheese hole | Static, tiny bob | Collectible score. |
| Turbo cheese | Cyan star | Static, pulse | Boost pickup. |
| Key | Yellow circle/square/diamond with black outline | Static, pulse | Opens matching key door. Shape matters, not colour. |
| Exit door | Blue rectangle with white arrow when open, grey with lock icon when locked | Opens after required mice | Win point. |
| Key door | Grey rectangle with key shape icon | Opens when matching key collected | Locked door. |
| Switch door | Grey rectangle with lever icon | Opens/closes via switch | Door controlled by switch. |
| Plate switch | Sunken yellow circle | Presses down when used | One-use switch. |
| Lever switch | Yellow lever on grey base | Pounce to toggle | Pounce-activated switch. |
| Noise ring | Thin blue ring | Expands from cat | Mice hear this if unobstructed. |
| Trail | Small fading circle or line | Fades over 0.3 s | Dash/boost feedback. |
| Particle | Small square/circle | Bursts and fades | Catch, fail, pickup feedback. |
| Hit flash | White overlay on entity | 0.08 s | Pounce hit or trap hit. |
| Hand-lettered UI | Cursive text, per-character rotation -3° to +3° | Static or gentle bounce on buttons | All screens use this typography. |

# 4. GAMEPLAY SPEC

You play Sir Pounce, a silly orange cat who must catch mice, avoid traps, find keys and switches, and reach the exit before the level fails. Each level starts with the cat at a spawn rug and mice at mouse-hole spawn points. The exit stays locked until the required number of common mice is caught. Catching mice builds combo and score. Traps can stun or immediately fail the level. Optional secret alcoves contain collectible special mice. The tone is bright and ridiculous: mice nap, traps are cheese and yarn, and failure means the cat gets bounced back to the start of the level.

## Level roster

| Level | Name | World | Common mice | Required | Special creature | Decoration | Landmarks |
| --- | --- | ---: | ---: | ---: | --- | ---: | --- |
| 1 | Kibble Kitchen | 1000 × 700 | 3 | 2 | Turbo Tippy | 4 | Start rug 1, mouse holes 3, cheese counter 1, exit 1, lamp 1 |
| 2 | Cheese Hall | 1100 × 750 | 4 | 3 | Gold Glint | 5 | Start rug 1, mouse holes 4, cheese counter 1, exit 1, lamps 2 |
| 3 | Yarn Attic | 1100 × 750 | 5 | 3 | Shell Shush | 6 | Start rug 1, mouse holes 5, cheese counter 1, exit 1, lamps 2 |
| 4 | Mouse Maze | 1300 × 850 | 6 | 4 | Zap Zig | 8 | Start rug 1, mouse holes 6, cheese counter 1, exit 1, lamps 3 |
| 5 | Purr Purlin | 1300 × 850 | 7 | 4 | Moon Moone | 8 | Start rug 1, mouse holes 7, cheese counter 1, exit 1, lamps 3 |
| 6 | Grand Mousery | 1500 × 950 | 8 | 5 | Berry Bob | 10 | Start rug 1, mouse holes 8, cheese counter 1, exit 1, lamps 4 |
| 7 | Whisker’s Finale | 1600 × 1000 | 9 | 6 | Star Sprinkles | 12 | Start rug 1, mouse holes 9, cheese counter 1, exit 1, lamps 4 |

| Level | Keys | Key doors | Switches | Switch doors | Traps: snap / spinner / yarn | Cheese | Turbo | Silver score | Gold score |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | — | 0 | — | 0 | 2 / 0 / 0 | 6 | 1 | 800 | 1300 |
| 2 | Circle 1 | 1 | Plate 1, Lever 1 | 2 | 2 / 1 / 1 | 7 | 1 | 1200 | 1800 |
| 3 | Square 1 | 1 | Plate 1, Lever 1 | 2 | 2 / 1 / 2 | 8 | 1 | 1400 | 2000 |
| 4 | Circle 1, Square 1 | 2 | Lever 2 | 2 | 3 / 2 / 1 | 8 | 2 | 1800 | 2600 |
| 5 | Circle 1, Square 1 | 2 | Plate 2, Lever 1 | 3 | 3 / 2 / 2 | 9 | 2 | 2100 | 3000 |
| 6 | Circle 1, Square 1, Diamond 1 | 3 | Plate 2, Lever 2 | 4 | 4 / 3 / 2 | 10 | 2 | 2400 | 3400 |
| 7 | Circle 1, Square 1, Diamond 1 | 3 | Plate 2, Lever 2 | 4 | 4 / 3 / 3 | 12 | 3 | 3200 | 4500 |

Cheese counts include the two secret-cheese pickups inside each secret alcove.

## Mouse roster

| Mouse type | Common? | Shape / colour | Wander speed | Flee speed | Score | Notes |
| --- | --- | --- | ---: | ---: | ---: | --- |
| Mousa | Yes | Cyan oval, round ears | 120 px/s | 220 px/s | 100 | Basic mouse. |
| Mousse | Yes | Purple oval, tall ears | 130 px/s | 230 px/s | 100 | Slightly faster. |
| Nib | Yes | Pink oval, small ears | 140 px/s | 240 px/s | 100 | More urgent. |
| Turbo Tippy | No | Yellow diamond mouse | 160 px/s | 250 px/s | 500 | Level 1 collectible creature. |
| Gold Glint | No | Gold circle mouse with sparkle | 160 px/s | 250 px/s | 500 | Level 2 collectible creature. |
| Shell Shush | No | Teal shell mouse | 160 px/s | 250 px/s | 500 | Level 3 collectible creature. |
| Zap Zig | No | Blue bolt mouse | 170 px/s | 260 px/s | 500 | Level 4 collectible creature. |
| Moon Moone | No | Purple crescent mouse | 170 px/s | 260 px/s | 500 | Level 5 collectible creature. |
| Berry Bob | No | Magenta berry mouse | 180 px/s | 270 px/s | 500 | Level 6 collectible creature. |
| Star Sprinkles | No | White star mouse | 190 px/s | 280 px/s | 600 | Level 7 collectible creature. |

All mouse speeds are multiplied by the level speed factor and difficulty mouse-speed multiplier.

## Trap roster

| Trap | Type | Movement | Hit radius | Effect | Visual cue |
| --- | --- | --- | ---: | --- | --- |
| Snap trap | Danger | Static | 18 px | Immediate fail | Red rectangle with black X. |
| Cheese spinner | Danger | Moves along waypoints at 120 px/s | 18 px | Immediate fail | Orange wheel with triangle cutout. |
| Yarn ball | Stun | Bounces between waypoints at 90 px/s | 14 px | Cat stunned 0.9 s, knockback 160 px/s | Pink circle with black swirl. |

## Pickup roster

| Pickup | Effect | Score | Shape |
| --- | --- | ---: | --- |
| Cheese puff | Collect score | 50 | Yellow square. |
| Turbo cheese | Speed boost 4 s, +35% speed | 100 | Cyan star. |
| Key | Opens matching key door | 200 | Yellow circle/square/diamond. |
| Secret cheese | Optional secret score | 50 | Yellow square with star notch. |

## Door and switch roster

| Door | Open condition | Collision when closed |
| --- | --- | --- |
| Exit door | `caughtCommon >= level.requiredMice` | Yes until unlocked. |
| Key door | Player has collected matching key shape | Yes until open. |
| Switch door | Linked switch opens it | Yes until open. |

| Switch | Activation | Effect |
| --- | --- | --- |
| Plate switch | Cat overlaps plate. One-use. | Opens linked switch door for 6.0 s. |
| Lever switch | Pounce hitbox touches lever. Toggle. Cooldown 1.0 s. | Opens/closes linked switch door permanently until toggled again. |

## 4.1 Movement and input [Tier 1]

- Input vector comes from remapped Up/Down/Left/Right keys.
- Diagonal input is normalized to length 1.
- Player acceleration: `1800 px/s²`.
- Player max speed: `220 px/s * speedMultiplier * boostMultiplier`.
- Friction when no input: `2200 px/s²`.
- If speed > 20 px/s, facing becomes normalized velocity.
- If speed <= 20 px/s, facing keeps last direction.
- Player is a circle radius 16 px.
- Player collides with walls and closed doors.
- Stunned player cannot move, dash, pounce, or use special.

## 4.2 Dash [Tier 1]

- Input: Dash.
- Condition: `dashCooldown <= 0` and not stunned.
- Dash duration: `0.14 s`.
- Dash speed: `360 px/s` in input/facing direction.
- Dash cooldown Classic: `0.75 s`.
- Careful: `0.65 s`; Zippy: `0.85 s`.
- Dash emits noise radius `150 px`.
- Dash creates trail if reduced motion is off.
- Dash does not pass through walls or closed doors.

## 4.3 Melee attack / pounce [Tier 1]

- Input: Pounce.
- Condition: `pounceCooldown <= 0` and not stunned.
- Pounce active time: `0.08 s`.
- Pounce cooldown Classic: `0.45 s`.
- Careful: `0.40 s`; Zippy: `0.50 s`.
- Pounce hit shape: capsule in facing direction.
  - Start: player center + facing × 10 px.
  - End: player center + facing × 44 px.
  - Radius: 13 px.
- Pounce lunges player forward at `80 px/s` for `0.08 s`.
- Pounce emits noise radius `170 px`.
- Pounce can catch mice and activate lever switches.
- Pounce hit triggers hit flash on the mouse if caught.

## 4.4 Chase and catch [Tier 1]

Common mice are the objective. Special mice are optional collectibles.

Mouse states:

| State | Rule |
| --- | --- |
| Wander | Moves at wander speed. Chooses new random direction every 1.0–2.0 s. Avoids walls with tangent steering. |
| Alert | Triggered by cat sight or noise. Flees away from threat for 1.6 s. |
| Doze | [Tier 2] If unalerted for 6–10 s, 25% chance to doze for 1.8 s. Dozing mouse speed 0. Dozing mouse can be caught by cat body overlap. |
| Stunned | [Tier 3] From Purr Burst. Speed 0 for 1.2 s. |
| Caught | Removed from level, score added. |

Cat sight:

- Mouse sees cat if distance <= 140 px and line of sight is not blocked by walls or closed doors.
- Seeing cat sets alert state.

Catch rules:

- Common mouse: pounce catch required, except if dozing.
- Special mouse: pounce catch required, except if dozing.
- Dozing mouse: cat body overlap catches it.
- Catching a common mouse increments `caughtCommon`.
- Catching a special mouse does not increment `caughtCommon`.
- Catching any mouse increments combo and adds score with multiplier.

## 4.5 Noise [Tier 2]

Noise events are created by the cat.

| Source | Noise radius | Intensity |
| --- | ---: | ---: |
| Movement | 60 px | 0.3 |
| Dash | 150 px | 1.0 |
| Pounce | 170 px | 1.2 |
| Purr Burst | 240 px | 1.5 |

Movement noise is emitted every `0.25 s` if player speed > 80 px/s.

Noise event:

- Duration: `0.35 s`.
- Radius grows from 0 to max radius over duration.
- Mouse hears noise if:
  - distance from mouse to noise center <= noise max radius;
  - line of sight is clear of walls and closed doors;
  - mouse is not already caught.
- Hearing noise sets mouse alert state for `1.4 s`.
- Visual: expanding blue ring, alpha 0.35.
- Reduced motion: static 12 px circle at cat position, no expansion.

## 4.6 Objectives [Tier 1]

- Each level has `requiredMice`.
- `caughtCommon` tracks only common mice.
- Exit door is locked while `caughtCommon < requiredMice`.
- When `caughtCommon >= requiredMice`:
  - exit door opens permanently;
  - play `exit_unlock`;
  - exit arrow appears.
- The level objective is reached only when the player overlaps the exit while the exit is open.
- Level start hint displays “Catch N mice!” for 3 s.

## 4.7 Score and combo [Tier 1]

Score bases:

| Event | Base score |
| --- | ---: |
| Common mouse caught | 100 |
| Special mouse caught | 500, Level 7 special 600 |
| Cheese puff collected | 50 |
| Turbo cheese collected | 100 |
| Key collected | 200 |
| Secret cheese collected | 50 |
| Level completion bonus | 500, Level 7 completion 1000 |

Combo:

- Combo increments on every mouse catch.
- Combo timer Classic: `3.0 s`.
- Careful: `5.0 s`; Zippy: `2.2 s`.
- Multiplier: `min(3.0, 1 + 0.25 * (combo - 1))`.
- Score added: `round(base * multiplier)`.
- If combo timer expires, combo resets to 0 and multiplier becomes 1.0.
- Failure restarts level and resets score/combo.

HUD combo is visible when `combo > 0`.

## 4.8 Traps [Tier 1 / Tier 2]

Snap trap [Tier 1]:

- Static.
- Danger.
- If player circle overlaps trap hit circle, level fails.
- Fail sequence:
  - play `trap_fail`;
  - spawn fail particles;
  - hit flash player;
  - state `gameover`;
  - after 1.5 s or on confirm input, reload same level.

Cheese spinner [Tier 2]:

- Moves along authored waypoints at 120 px/s.
- Danger.
- Contact fails level like snap trap.
- Zippy difficulty: speed 132 px/s, hit radius 19.8 px.

Yarn ball [Tier 2]:

- Moves between waypoints, bouncing direction on wall or waypoint.
- Base speed: 90 px/s.
- Non-danger.
- On hit:
  - player `stunTime = 0.9 s`;
  - player knockback away from yarn at 160 px/s;
  - yarn changes direction;
  - play `trap_stun`;
  - hit flash player.
- Stun prevents movement/dash/pounce/special.

Difficulty trap hit radii:

| Difficulty | Trap hit radius multiplier |
| --- | ---: |
| Careful | 0.85 |
| Classic | 1.00 |
| Zippy | 1.10 |

## 4.9 Collectibles [Tier 1 / Tier 2]

Cheese puff [Tier 1]:

- Static.
- Collect on overlap.
- Adds 50 score with current multiplier? No: pickups use base score without mouse-combo multiplier except combo is not reset. To keep simple, pickups add flat base score.
- Spawn yellow particle burst.
- Play `cheese`.

Turbo cheese [Tier 2]:

- Collect on overlap.
- Adds 100 score.
- Applies speed boost.
- Play `boost`.

Key [Tier 2]:

- Has shape: circle, square, diamond.
- Collect on overlap.
- Adds 200 score.
- Opens matching key door.
- Play `key`.

Secret cheese [Tier 2]:

- Found in secret alcoves.
- Adds 50 score.
- Visually a cheese puff with star notch.

## 4.10 Boosts [Tier 2]

Turbo cheese effect:

- `boostTime = max(boostTime, 4.0)`.
- Speed multiplier while active: `1.35`.
- Boost stack rule: refresh duration, do not stack speed.
- Boost creates trail if reduced motion is off.
- Boost does not affect dash speed; dash speed remains 360 px/s.
- Boost does not affect mouse speed.

## 4.11 Keys and locked doors [Tier 2]

- Keys are shape-coded: circle, square, diamond.
- Each key door has one required key shape.
- When a key of matching shape is collected:
  - all matching key doors open permanently;
  - play `door_open`;
  - door icon changes to open.
- Keys of other shapes do not open that door.
- Key doors block collision while closed.
- Mice collide with closed key doors.
- If a mouse spawns behind a closed key door, it remains inaccessible until the door opens.

## 4.12 Switches and doors [Tier 2]

Plate switch:

- Triggered when player overlaps switch circle radius 16 px.
- One-use only.
- On activate:
  - linked switch door opens;
  - door timer `6.0 s`;
  - play `switch_click`;
  - plate stays pressed.
- After 6.0 s, linked door closes if no other active switch keeps it open.

Lever switch:

- Triggered by pounce hitbox overlap.
- Toggle behaviour.
- Cooldown `1.0 s` after activation.
- On activate:
  - if linked door closed, open permanently;
  - if linked door open, close permanently;
  - play `switch_click`.
- Lever visual flips up/down.

Switch doors:

- Closed by default.
- Open/closed state controlled only by linked switch.
- Open switch door is non-solid.
- Closed switch door blocks cat and mice.

## 4.13 Landmarks and decoration [Tier 2]

Landmarks are non-interactive orientation objects:

| Landmark | Count | Purpose |
| --- | ---: | --- |
| Start rug | 1 per level | Player spawn point. |
| Mouse hole | 1 per common mouse | Mouse initial spawn point. |
| Cheese counter | 1 per level | Visual landmark near cheese cluster. |
| Exit door | 1 per level | Win point. |
| Lamp | 1–4 per level | Orientation. |

Decoration:

- Non-interactive flat props: rugs, plants, crates, books, yarn rolls.
- Decoration count per level is from level roster.
- Decorations do not block movement unless the level author represents them as wall rectangles.
- Secret alcoves use a unique floor colour and a small “?” star decoration.

## 4.14 Map / world [Tier 1]

- Level world is a rectangular area with wall rectangles.
- World bounds from level roster.
- Player cannot leave world bounds.
- Camera viewport 800 × 600.
- Camera follows player and clamps to world.
- Walls are AABB rectangles, minimum thickness 16 px.
- Closed doors are AABB rectangles.
- Mice and traps do not spawn inside walls.
- Every level must have at least one valid path from player spawn to every required mouse spawn and to the exit after required progression.

## 4.15 Secrets and collectible creatures [Tier 2]

Each level has one secret alcove:

- Contains the level’s special collectible mouse.
- Contains 2 secret cheese pickups.
- Entry is a switch door linked to one secret switch.
- Secret door looks like a slightly odd wall panel until opened.
- Secret alcove has unique floor colour and “?” star.
- The special mouse does not count toward `requiredMice`.
- Catching the special mouse:
  - adds 500 score, or 600 for Level 7;
  - adds creature to `progress.collectedCreatures`;
  - shows reward on win screen.
- All 7 creatures collected adds “★ Collector” suffix to rank.

## 4.16 Hints [Tier 2]

Hints appear as a hand-lettered text banner for 3 s.
Hint cooldown: 10 s.
Only one hint at a time.

| Trigger | Hint text |
| --- | --- |
| Player idle for 4 s | “Move with WASD or arrows.” |
| No catch for 8 s and required not met | “Pounce to catch mice.” |
| Locked key door touched for 4 s | “Find the matching key shape.” |
| Switch door closed and linked switch unused for 10 s | “Use plates and levers to open doors.” |
| Player near secret switch for 5 s | “Something clicks here.” |
| Exit locked and all required mice caught but exit not touched for 3 s | “The exit is open. Go!” |

## 4.17 Progression, medals, ranks, unlocks, rewards [Tier 2 / Tier 3]

Level medal:

| Medal | Condition | Medal points |
| --- | --- | ---: |
| Bronze | Complete level | 1 |
| Silver | Score >= level Silver target | 2 |
| Gold | Score >= level Gold target | 3 |

Only the highest medal for a level counts. Re-clearing a level can improve best score and medal.

Rank by total medal points, max 21:

| Medal points | Rank |
| ---: | --- |
| 0 | Paw Cadet |
| 1–2 | Whisker Scout |
| 3–4 | Mouson Hunter |
| 5 | Cheese Champion |
| 6 | Cat Captain |
| 7–10 | Feline Frenzy |
| 11–14 | Whisker Wizard |
| 15–17 | Purr Monarch |
| 18–20 | Mouson Myth |
| 21 | Sir Pounce, Legend |

If all 7 collectible creatures are collected, append “★ Collector” to rank.

Level rewards on win:

- Completion bonus added to score before medal determination.
- Medal awarded.
- Next level unlocked.
- High score entry posted.
- Best by level updated.
- Collection creature shown if collected.
- Ability unlocks shown if newly unlocked. [Tier 3]

## 4.18 High scores [Tier 2]

- Each level win posts an entry:
  - level index,
  - level name,
  - final score,
  - best combo during level,
  - medal,
  - timestamp.
- High Scores screen shows top 10 entries sorted by score descending.
- Best by level stores highest score, highest combo, and best medal.
- Total best score is the sum of best-by-level scores for levels 1–7.
- Stored in localStorage.

## 4.19 Abilities / special moves [Tier 3]

Abilities unlock from total medal points.

| Ability | Unlock | Effect |
| --- | ---: | --- |
| Nimble Paws | 3 points | Dash cooldown becomes 0.60 s Classic, 0.52 s Careful, 0.68 s Zippy. |
| Long Snout | 6 points | Pounce capsule length becomes 42 px and radius becomes 15 px. |
| Purr Burst | 12 points | Unlocks special move. |

Purr Burst special move:

- Input: Special.
- Condition: unlocked, `specialCooldown <= 0`, not stunned.
- Cooldown: `8.0 s`.
- Effect:
  - emits noise radius 240 px;
  - all mice within 240 px become stunned for 1.2 s;
  - player gets speed multiplier `1.20` for 2.0 s;
  - does not catch mice directly;
  - play `special`;
  - visual blue ring.
- Reduced motion: ring is static, no expansion.

## 4.20 Difficulty ramp and difficulty options [Tier 2]

Level ramp:

| Level | World | Common mice | Required | Speed factor | Traps increase | Doors/keys increase |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | 1000 × 700 | 3 | 2 | 1.00 | 2 danger | none |
| 2 | 1100 × 750 | 4 | 3 | 1.05 | 3 danger + 1 stun | 1 key, 2 switch doors |
| 3 | 1100 × 750 | 5 | 3 | 1.10 | 3 danger + 2 stun | 1 key, 2 switch doors |
| 4 | 1300 × 850 | 6 | 4 | 1.15 | 5 danger + 1 stun | 2 keys, 2 switch doors |
| 5 | 1300 × 850 | 7 | 4 | 1.20 | 5 danger + 2 stun | 2 keys, 3 switch doors |
| 6 | 1500 × 950 | 8 | 5 | 1.25 | 7 danger + 2 stun | 3 keys, 4 switch doors |
| 7 | 1600 × 1000 | 9 | 6 | 1.30 | 7 danger + 3 stun | 3 keys, 4 switch doors |

Difficulty options:

| Setting | Careful | Classic | Zippy |
| --- | ---: | ---: | ---: |
| Mouse speed multiplier | 0.90 | 1.00 | 1.15 |
| Trap hit radius multiplier | 0.85 | 1.00 | 1.10 |
| Trap speed multiplier | 0.90 | 1.00 | 1.10 |
| Combo timer | 5.0 s | 3.0 s | 2.2 s |
| Dash cooldown | 0.65 s | 0.75 s | 0.85 s |
| Pounce cooldown | 0.40 s | 0.45 s | 0.50 s |
| Yarn stun | 0.8 s | 0.9 s | 1.0 s |

Danger traps still fail in all difficulties.

## 4.21 Puzzle types [Tier 2]

| Puzzle type | Rule |
| --- | --- |
| Key door | Find matching shape key to open a locked path. |
| Plate timing | Stand on plate, then cross before 6.0 s timer closes door. |
| Lever toggle | Pounce lever to open/close a door at the right moment. |
| Noise herding | Dash or pounce creates noise; mice flee and may become easier to pounce. |
| Doze catch | Wait for a mouse to doze, then touch it to catch without pounce. |
| Trap path | Avoid danger traps and manage yarn stun windows. |
| Secret lure | Find hidden plate/lever that opens secret alcove with collectible mouse. |
| Exit race | Catch required mice while managing doors and traps. |

## 4.22 Fail and win flow [Tier 1]

Fail:

- Trigger: cat touches snap trap or cheese spinner.
- Consequence:
  - state `gameover`;
  - score/combo lost;
  - after 1.5 s or confirm input, reload same level;
  - no level unlock or high score posted.

Win:

- Trigger: exit door open and cat overlaps exit.
- Consequence:
  - state `win`;
  - completion bonus added;
  - medal awarded;
  - high score posted;
  - next level unlocked;
  - final level win shows total best score and rank.

## 4.23 Feel [Tier 1 / Tier 3]

Base feel:

- Cat is snappy: high acceleration, short dash, short pounce.
- Mice are skittish: quick flee, wall-aware steering.
- Traps are readable: danger always has shape cue.
- Combos feel rhythmic: quick catches keep multiplier alive.

Effects:

| Effect | Normal | Reduced motion |
| --- | --- | --- |
| Catch particles | 12 particles, 0.4 s | 3 particles, 0.4 s |
| Fail particles | 20 particles, 0.6 s | 3 particles, 0.6 s |
| Cheese particles | 6 particles, 0.25 s | 2 particles, 0.25 s |
| Dash trail | 10 trail points, 0.3 s | no trail |
| Boost trail | continuous trail, 0.3 s fade | no trail |
| Noise ring | expanding ring, 0.35 s | static 12 px circle |
| Hit flash | 0.08 s white overlay | 0.08 s tint only |
| Pounce lunge | 80 px/s forward | same, no extra stretch |

# 5. CHARACTERS

## Sir Pounce, the cat

Silhouette:

- Circle body radius 16 px.
- Two triangle ears on top.
- Small nose cone in facing direction.
- Curved tail behind body.
- Black outline 3 px.
- Orange fill `#FFA000`.
- Tail and inner ears darker orange `#FF8A00`.

Facings:

- Facing is shown by nose direction.
- Cat can face any 2D direction.
- Ears shift slightly toward facing.

Animations:

| Animation | Motion rule |
| --- | --- |
| idle | Tail wags side to side every 0.8 s. Body scale pulses 1.00–1.02. |
| run | Body squashes 8% perpendicular to movement at 8 Hz. Paws as small dots move in facing direction. |
| dash | Body stretches 15% along velocity. Trail appears. |
| pounce | Nose extends 10 px toward facing for 0.08 s. Ears flatten. |
| stun | Cat spins 180° over 0.9 s. Three black stars orbit for 0.9 s. |
| caught | Ears point up, body bounces scale 1.0 → 1.15 → 1.0 over 0.2 s. |
| boost | No extra shape change; cyan trail only. |

States needed by gameplay rules:

- Normal
- Dash
- Pounce
- Stunned
- Boosted
- Fail flash

## Mice

Silhouette:

- Oval body radius 10 px.
- Two large triangle ears.
- Thin tail line behind body.
- Black outline 2 px.
- Common colours:
  - Mousa cyan `#40C4FF`
  - Mousse purple `#B388FF`
  - Nib pink `#FF4FA8`
- Special mice have unique overlay shape:
  - Turbo Tippy: yellow diamond.
  - Gold Glint: gold circle sparkle.
  - Shell Shush: teal shell swirl.
  - Zap Zig: blue bolt.
  - Moon Moone: purple crescent.
  - Berry Bob: magenta berry.
  - Star Sprinkles: white star.

Facings:

- Mouse nose/ear direction shows movement.
- Mice can face any 2D direction.

Animations:

| Animation | Motion rule |
| --- | --- |
| wander | Body bobs vertically 4 px at 4 Hz. Tail sways. |
| alert | Ears point away from threat. Body stretches 12% along flee direction. |
| flee | Stretch 12% along velocity. Tail straightens. Speed lines optional if reduced motion off. |
| doze | Body flattens to 80% height. Zzz particles every 0.8 s. |
| stunned | Mouse spins 360° over 1.2 s. Star icon above head. |
| caught | Scale 1.0 → 1.2 → 0 over 0.15 s, then particles. |

States needed by gameplay rules:

- Wander
- Alert
- Doze
- Stunned
- Caught

# 6. AUDIO

The audio API is Web Audio. All sounds are synthesized. Music is chiptune: square lead, triangle bass, noise percussion. The mood is silly and upbeat.

| Name | Recipe | When it plays |
| --- | --- | --- |
| `music_title` | 104 BPM. Square bass C–E–G–C, triangle pentatonic lead, noise hat every beat, 8-bar loop. | Title, level select, high scores, settings. |
| `music_game` | 128 BPM. Square bass root notes, triangle silly pentatonic lead, noise snare on beats 2 and 4, 16-bar loop. | Playing state. |
| `music_win` | 140 BPM. Square major arpeggio C–E–G–C, triangle fill, noise cheer, 4-bar one-shot. | Win screen. |
| `music_gameover` | 90 BPM. Descending square D–C–A–F, triangle low bass, noise thud, 4-bar one-shot. | Game over screen. |
| `ui_click` | Square 880 Hz, 0.04 s, quick decay. | Button press. |
| `ui_back` | Square 440 Hz → 330 Hz, 0.06 s. | Back button. |
| `dash` | Sawtooth 220 Hz → 660 Hz, 0.08 s, gain 0.25. | Player dash. |
| `pounce` | Square 300 Hz → 120 Hz, 0.05 s, gain 0.3. | Pounce input. |
| `catch_mouse` | Square 880 Hz → 1320 Hz, 0.08 s, plus triangle 1568 Hz 0.05 s. | Mouse caught. |
| `cheese` | Triangle 784 Hz, 0.05 s. | Cheese/secret cheese collected. |
| `boost` | Sawtooth 440 Hz → 880 Hz, 0.15 s. | Turbo cheese collected. |
| `key` | Square 1046 Hz, 0.04 s. | Key collected. |
| `door_open` | Sawtooth 110 Hz → 220 Hz, 0.18 s. | Any door opens. |
| `door_close` | Sawtooth 220 Hz → 110 Hz, 0.18 s. | Switch door closes. |
| `switch_click` | Square 523 Hz, 0.03 s. | Plate or lever activates. |
| `trap_fail` | White noise 0.25 s plus square 200 Hz → 60 Hz 0.30 s. | Danger trap hit. |
| `trap_stun` | Square 200 Hz with ±20 Hz wobble, 0.12 s. | Yarn ball hit. |
| `special` | Sawtooth 330 Hz → 660 Hz, 0.20 s, plus noise 0.15 s. | Purr Burst. |
| `hint` | Triangle 880 Hz, 0.06 s. | Hint appears. |
| `exit_unlock` | Square 1046 Hz then 1568 Hz, 0.12 s each. | Exit unlocks. |
| `gameover` | Square 660, 440, 330, 110 Hz, 0.15 s each. | Game over screen. |
| `win` | Square 523, 659, 784, 1046 Hz, 0.12 s each. | Win screen. |

# 7. UX

All screens are HTML/CSS overlays above the canvas. The canvas always shows the current level background or a flat title background.

## State machine

| From | Event / Input | To |
| --- | --- | --- |
| title | Start pressed | levels |
| title | Settings pressed | settings |
| title | High Scores pressed | highscores |
| levels | Select unlocked level | playing |
| levels | Back pressed | title |
| playing | Pause pressed | paused |
| playing | Danger trap hit | gameover |
| playing | Exit reached | win |
| paused | Resume pressed | playing |
| paused | Settings pressed | settings |
| paused | Quit pressed | levels |
| settings | Back pressed | previousState |
| gameover | 1.5 s timer or confirm | playing |
| win | Continue pressed | levels |
| win | Title pressed | title |
| highscores | Back pressed | previousState |

## DOM structure

```html
<div id="app">
  <canvas id="game" width="800" height="600"></canvas>

  <div id="hud">
    <div id="hud-score" class="hand">0</div>
    <div id="hud-combo" class="hand hidden">×1.0</div>
  </div>

  <div id="screen-title" class="screen">…</div>
  <div id="screen-levels" class="screen">…</div>
  <div id="screen-pause" class="screen">…</div>
  <div id="screen-settings" class="screen">…</div>
  <div id="screen-gameover" class="screen">…</div>
  <div id="screen-win" class="screen">…</div>
  <div id="screen-highscores" class="screen">…</div>

  <div id="hint-banner" class="hand hidden"></div>
  <div id="level-banner" class="hand hidden"></div>
</div>
```

HUD is intentionally limited to score and combo.

| HUD element | Record field | When visible |
| --- | --- | --- |
| `#hud-score` | `ctx.score` | state is `playing` or `paused` |
| `#hud-combo` | `ctx.multiplier`, `ctx.combo` | state is `playing` and `ctx.combo > 0` |

## Screen contents

| Screen | Contents |
| --- | --- |
| Title | Game logo, Start, Settings, High Scores. |
| Level select | 7 level cards. Locked cards greyed. Each unlocked card shows best score and medal. Select starts level. Back returns to title. |
| Pause | Resume, Settings, Quit to Level Select. |
| Settings | Difficulty select: Careful/Classic/Zippy. Reduced motion toggle. Remappable key list. Back. |
| Game over | “Ouch!” message, “Level restarted”, auto timer or confirm prompt. |
| Win | Level score, medal, rewards, new unlocks, creature collected if any, Continue, Title. Final win shows total best score and rank. |
| High scores | Top 10 entries: level name, score, combo, medal. Back. |

## Typography

- All UI text uses `.hand`.
- Font stack: `"Comic Sans MS", "Chalkboard SE", "Marker Felt", cursive`.
- Title and heading text split into per-character spans.
- Each character gets deterministic rotation between -3° and +3° and scale between 0.98 and 1.02.
- Body buttons use the same font stack but no per-character jitter to keep readability.

# 8. DEBUG API

All debug functions are exposed on `window.debug` for testing.

## Player input functions

| Function | Effect |
| --- | --- |
| `debug.input.setMove(x, y)` | Sets normalized movement vector directly. |
| `debug.input.dash()` | Triggers dash input. |
| `debug.input.pounce()` | Triggers pounce input. |
| `debug.input.special()` | Triggers special input. |
| `debug.input.pauseToggle()` | Toggles pause. |
| `debug.input.confirm()` | Confirms current screen. |
| `debug.input.back()` | Activates back action. |
| `debug.input.selectLevel(index)` | Selects a level if unlocked. |
| `debug.input.setRemap(action, keyCode)` | Changes remap for testing. |

## System debug functions

| Function | System | Effect |
| --- | --- | --- |
| `debug.loadLevel(index)` | Level | Loads level immediately. |
| `debug.failLevel()` | Fail | Triggers game over as if danger trap hit. |
| `debug.winLevel()` | Win | Triggers win as if exit reached. |
| `debug.setScore(n)` | Score | Sets current level score. |
| `debug.addScore(n)` | Score | Adds flat score. |
| `debug.setCombo(n)` | Combo | Sets combo count. |
| `debug.setComboTimer(n)` | Combo | Sets combo timer. |
| `debug.giveKey(shape)` | Keys | Collects a key without pickup. |
| `debug.openDoor(id)` | Doors | Opens door. |
| `debug.closeDoor(id)` | Doors | Closes door. |
| `debug.setSwitch(id, open)` | Switches | Sets linked door state. |
| `debug.activateSwitch(id)` | Switches | Activates switch. |
| `debug.setMouseState(id, state)` | Mice | Sets mouse state. |
| `debug.teleportMouse(id, x, y)` | Mice | Moves mouse. |
| `debug.catchMouse(id)` | Catch | Marks mouse caught and applies score. |
| `debug.setTrapSpeed(id, speed)` | Traps | Sets trap speed. |
| `debug.setTrapPosition(id, x, y)` | Traps | Moves trap. |
| `debug.collectPickup(id)` | Pickups | Collects pickup. |
| `debug.emitNoise(x, y, radius)` | Noise | Creates noise event. |
| `debug.showHint(text)` | Hints | Shows hint. |
| `debug.setMedal(levelIndex, medal)` | Progress | Sets level medal. |
| `debug.setMedalPoints(n)` | Progress | Sets total medal points. |
| `debug.unlockLevel(index)` | Progress | Unlocks level. |
| `debug.collectCreature(id)` | Collection | Marks creature collected. |
| `debug.unlockAbility(id)` | Abilities | Unlocks ability. |
| `debug.setHighScore(entry)` | High scores | Inserts high score entry. |
| `debug.setDifficulty(mode)` | Difficulty | Changes difficulty. |
| `debug.setReducedMotion(bool)` | Accessibility | Changes reduced motion. |
| `debug.godMode(bool)` | Debug | Ignores danger traps. |
| `debug.showHitboxes(bool)` | Debug | Draws collision shapes. |

# 9. TESTS

## Tier 1 tests

1. Fixed-step loop executes exactly 60 logic updates per simulated second.
2. RNG produces identical sequence for identical seed.
3. Player moves with input vector and is clamped by walls.
4. Diagonal input is normalized and does not exceed base speed.
5. Dash sets speed to 360 px/s for 0.14 s and cooldown to 0.75 s Classic.
6. Pounce creates a capsule hitbox that catches a mouse within range.
7. Pounce cooldown prevents immediate re-pounce.
8. Catching required common mice opens exit door.
9. Touching exit while open triggers win.
10. Touching snap trap triggers game over and restarts same level.
11. Score updates on mouse catch and cheese pickup.
12. Combo increments on catch and multiplier updates.
13. Combo timer expires and resets combo.
14. HUD score and combo update.
15. Title, level select, pause, game over, and win screens transition correctly.
16. Basic SFX play for dash, pounce, catch, trap fail, win.
17. Level 1 contains 3 common mice, 2 required mice, 2 snap traps, 6 cheese, 1 turbo.

## Tier 2 tests

1. All 7 levels load with correct world sizes and entity counts.
2. Key doors open only when matching key shape is collected.
3. Circle key does not open square or diamond door.
4. Plate switch opens linked door for 6.0 s then closes.
5. Lever switch toggles linked door on pounce and has 1.0 s cooldown.
6. Cheese spinner contact fails level.
7. Yarn ball contact stuns player for 0.9 s and applies knockback.
8. Turbo cheese applies 1.35× speed for 4.0 s and refreshes duration when stacked.
9. Cheese pickup adds 50 score.
10. Key pickup adds 200 score.
11. Noise event alerts mouse if line of sight is clear.
12. Noise does not alert mouse if wall or closed door blocks line of sight.
13. Dozing mouse can be caught by cat body overlap.
14. Dozing mouse wakes when noise or cat sight occurs.
15. Secret alcove contains special mouse and 2 secret cheese.
16. Catching special mouse adds to collection and does not increment `caughtCommon`.
17. Hints trigger based on idle, no catch, locked door, unused switch, and secret proximity.
18. Medals awarded by score thresholds.
19. Medal points update correctly: Bronze 1, Silver 2, Gold 3.
20. High score screen shows top 10 entries sorted by score.
21. Best-by-level updates on re-clear.
22. Difficulty options change mouse speed, trap radius, trap speed, combo timer, dash cooldown, pounce cooldown.
23. Remappable keys persist and control player correctly.
24. Reduced motion disables trails and reduces particle counts.
25. Every level has a valid path to required mice and exit after opening required doors.
26. Mice cannot pass through closed doors.
27. Cat cannot pass through closed doors.

## Tier 3 tests

1. Nimble Paws unlocks at 3 medal points and reduces dash cooldown.
2. Long Snout unlocks at 6 medal points and increases pounce capsule length/radius.
3. Purr Burst unlocks at 12 medal points.
4. Purr Burst stuns mice within 240 px for 1.2 s.
5. Purr Burst gives player 1.20× speed for 2.0 s.
6. Purr Burst cooldown is 8.0 s.
7. Rank updates by total medal points.
8. All 7 collectible creatures collected adds “★ Collector” suffix.
9. Final level win displays total best score and rank.
10. Progress persists across reload.
11. High scores persist across reload.
12. Settings persist across reload.
13. Colour-blind safe shapes exist for all keys, doors, traps, and special creatures.
14. Reduced motion still allows gameplay and effects remain readable.

# 10. BUILD ORDER

1. Scaffold `index.html`, CSS, canvas, fixed-step loop, deterministic RNG, state machine.
2. Build core input, player movement, wall collision, camera, top-down level rendering.
3. Create Level 1 data: walls, player spawn, mouse spawns, required mice, exit, cheese, snap traps.
4. Implement cat dash, pounce, mouse wander/alert/flee, catch rules, score/combo.
5. Add exit objective, fail/restart, game over, win, title, level select, pause, basic HUD.
6. Add basic flat vector art for cat, mice, traps, cheese, exit, and chiptune/SFX.
7. Add all 7 level data and verify counts, paths, and score targets.
8. Add pickups: cheese, turbo, keys, secret cheese; implement boosts.
9. Add traps: cheese spinner, yarn ball; implement danger fail and stun.
10. Add keys/key doors, plate switches, pounce levers, switch doors.
11. Add noise events, mouse hearing, line-of-sight blocking, doze state.
12. Add landmarks, decoration, secret alcoves, collectible creatures, hints.
13. Add progression: medals, medal points, high scores, level unlocks, rewards screen.
14. Add settings: difficulty options, reduced motion, remappable keys.
15. Add Tier 3 abilities, Purr Burst, ranks, collection suffix, final win presentation.
16. Run tests, polish visuals/audio, validate accessibility, persist save data.

# 11. DEFINITION OF DONE

## Tier 1 done

High level: A new player can start from title, select Level 1, move Sir Pounce, dash, pounce, catch 2 of 3 mice, avoid snap traps, reach the exit, win, fail on trap contact, and restart. Score and combo are visible.

- [ ] `index.html` loads and renders an 800 × 600 canvas.
- [ ] Fixed-step 60 Hz loop runs without drift beyond clamped frame time.
- [ ] RNG is deterministic and seeded per level/difficulty.
- [ ] Title screen has Start, Settings, High Scores.
- [ ] Level select screen shows Level 1 unlocked and Levels 2–7 locked.
- [ ] Playing state starts Level 1 with correct spawn points.
- [ ] Cat moves freely with remapped/default keys.
- [ ] Cat respects walls and world bounds.
- [ ] Dash works: 360 px/s for 0.14 s, 0.75 s Classic cooldown.
- [ ] Pounce works: 34 px capsule, 0.45 s Classic cooldown.
- [ ] Level 1 has 3 common mice and requires 2 catches.
- [ ] Catching required mice opens exit.
- [ ] Reaching open exit triggers win.
- [ ] Touching snap trap triggers game over.
- [ ] Game over restarts Level 1 after 1.5 s or confirm.
- [ ] HUD score updates.
- [ ] HUD combo updates when combo > 0.
- [ ] Combo timer and multiplier follow rules.
- [ ] Basic SFX play for dash, pounce, catch, fail, win.
- [ ] Flat vector cat, mice, cheese, snap trap, exit are visible.
- [ ] Pause works and resumes correctly.
- [ ] No health/lives system exists.
- [ ] No unlisted screens exist.

## Tier 2 done

High level: All 7 levels are playable and contain the full listed mechanics: pickups, boosts, keys, doors, switches, traps, noise, doze, secrets, collectible creatures, hints, medals, high scores, difficulty options, remappable keys, reduced motion.

- [ ] All 7 level records load with correct sizes, counts, and targets.
- [ ] Level 1–7 common mouse counts and required mice match roster.
- [ ] All common mouse types have correct base speeds.
- [ ] Level speed factor applies to mouse speeds.
- [ ] Cheese, turbo, key, and secret cheese pickups collect correctly.
- [ ] Turbo cheese applies 1.35× speed for 4.0 s.
- [ ] Keys are shape-coded and open only matching key doors.
- [ ] Plate switches open doors for 6.0 s.
- [ ] Lever switches toggle doors via pounce.
- [ ] Cheese spinner fails level on contact.
- [ ] Yarn ball stuns player and applies knockback.
- [ ] Trap hit radii apply difficulty multipliers.
- [ ] Noise events emit from movement, dash, pounce.
- [ ] Mice hear noise only with clear line of sight.
- [ ] Closed doors and walls block noise and sight.
- [ ] Mice can doze and be caught by touch.
- [ ] Each level has one secret alcove.
- [ ] Each secret contains the correct special mouse and 2 secret cheese.
- [ ] Catching special mice adds to collection.
- [ ] Special mice do not count toward required common mice.
- [ ] Hints trigger for idle, no catch, locked door, unused switch, secret, exit ready.
- [ ] Medals awarded by level score thresholds.
- [ ] Medal points update: Bronze 1, Silver 2, Gold 3.
- [ ] High Scores screen shows top 10 entries.
- [ ] Best-by-level stores score, combo, medal.
- [ ] Level unlocks are sequential.
- [ ] Difficulty options affect all listed multipliers.
- [ ] Reduced motion toggle persists and affects effects.
- [ ] Remappable keys persist and work.
- [ ] All levels are valid: required mice reachable and exit reachable after required progression.
- [ ] Colour-blind safe shape cues exist for keys, doors, traps, special mice.
- [ ] No unlisted mechanics are present.

## Tier 3 done

High level: Progression, abilities, ranks, collection, persistence, and polish are complete. The game feels finished and accessible.

- [ ] Nimble Paws unlocks at 3 medal points.
- [ ] Long Snout unlocks at 6 medal points.
- [ ] Purr Burst unlocks at 12 medal points.
- [ ] Purr Burst stuns mice within 240 px for 1.2 s.
- [ ] Purr Burst grants 1.20× speed for 2.0 s.
- [ ] Purr Burst has 8.0 s cooldown.
- [ ] Rank table displays correct rank by medal points.
- [ ] All 7 collectible creatures add “★ Collector” suffix.
- [ ] Final level win shows total best score and rank.
- [ ] Win screen shows rewards, medal, new unlocks, collected creature.
- [ ] Progress save persists after reload.
- [ ] High scores persist after reload.
- [ ] Settings persist after reload.
- [ ] Particles, trails, and hit flash match normal/reduced-motion tables.
- [ ] Audio includes title, game, win, game over, and all listed SFX.
- [ ] Hand-lettered typography is applied to UI.
- [ ] Colour-blind safe palette and shape cues are verified.
- [ ] Reduced motion is fully playable.
- [ ] All tests in §9 pass.
- [ ] No camera shake or unlisted effects exist.

# A. SANITY

| Check | Result | Why / Fix |
| --- | --- | --- |
| Win condition matches “reach the exit” | Valid | Exit is the win point after required mice. |
| Failure matches “restart the level” | Valid | Danger trap contact fails and reloads same level. |
| No health/lives system added | Valid | Failure uses traps only. |
| HUD limited to score and combo | Valid | §7 HUD table has only score and combo. |
| Screens limited to required list | Valid | State machine uses title, levels, playing, paused, settings, gameover, win, highscores. |
| Effects limited to particles, hit flash, trails | Valid | No camera shake or unlisted effects. |
| Mechanics list fully covered | Valid | Each listed mechanic has a section or roster entry. |
| Colour-blind safe palette required | Valid | Keys/doors/traps/special mice use shape/icon cues. |
| Reduced motion required | Valid | Effects table defines reduced-motion behaviour. |
| Remappable keys required | Valid | Input and settings specify remapping. |
| Difficulty options required | Valid | Careful/Classic/Zippy table defined. |
| Music chiptune | Valid | Audio section specifies chiptune recipes. |
| Sound effects retro bleeps | Valid | SFX are synthesized square/triangle/saw/noise bleeps. |
| Art flat vector | Valid | Visual spec uses clean vector shapes and solid colours. |
| Palette saturated | Valid | Palette uses bright strong colours. |
| Typography hand-lettered | Valid | UI uses cursive plus per-character jitter. |
| Size under 30 minutes | Valid | 7 levels with target playtime 22–30 minutes. |
| Level counts reasonable | Valid | 7 levels, escalating counts, fixed targets. |
| Score targets achievable | Valid | Minimum scores with required mice and all pickups are at or near Silver; Gold requires combo, extras, or special mouse. |
| Special mice not required | Valid | `caughtCommon` only counts common mice. |
| Keys matter with multiple doors | Valid | Keys are shape-coded; each door requires matching shape. |
| Switches do not require extra interact key | Valid | Plates use overlap, levers use pounce. |
| Noise has gameplay effect | Valid | Noise alerts mice and can wake dozing mice. |
| Secrets use collectible creatures | Valid | Each secret contains the level’s special mouse. |
| Medals/ranks progression consistent | Valid | Medal points max 21; rank thresholds max 21. |
| Ability unlocks achievable | Valid | 3, 6, and 12 medal points are reachable across 7 levels. |
| Module contracts include needed functions | Valid | §2.3 lists functions required by rules/tests. |
| Debug API covers systems | Valid | §8 lists direct-state functions per system plus inputs. |
| Tests align with tiers | Valid | §9 tests map to Tier 1/2/3 done boxes. |
| Build order leads to done | Valid | §10 builds core first, then content, then progression/polish. |
| Error found: rank/ability thresholds initially assumed 21 medals but only 7 level medals | Fixed | Changed to medal points: Bronze 1, Silver 2, Gold 3, max 21; ability unlocks at 3/6/12 points. |
| Error found: multiple keys could open all doors if using count | Fixed | Keys are shape-coded and doors require matching shape. |
| Error found: camera shake implied by reduced motion but not in effects list | Fixed | Removed camera shake; reduced motion only affects listed effects. |
