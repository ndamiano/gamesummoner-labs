# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Browser game | Entire spec; canvas + HTML/CSS UI, no external assets |
| Platformer where you play as a frog | Player identity in §4, §5 |
| 2D | §1, §3, §7 |
| Side-on camera | §1.1, §4.4 |
| Real-time | §1.1 fixed-step loop |
| Free movement | §4.2 movement rules |
| Sequence of levels | §4.38 progression, §7 level select |
| Failure restarts the level | §4.5, §4.7, §7 game over |
| Silly tone | Names, art, audio, level content in §3, §4, §5, §6 |
| A handful of levels, under 30 minutes | §4.38: 7 levels, target playtime 18–28 minutes |
| Win/lose: reach the exit | §4.7 objectives, §7 win/game over |
| Core mechanics: jump, objectives, falling, map/world, bounce | §4.2, §4.4, §4.5, §4.6, §4.7 |
| Supporting mechanics: traps, environmental damage, physics objects, swim, enemies, difficulty ramp, abilities/special moves, dodge, spawn points, climb, unlocks | §4.9–§4.18, §4.38 |
| Extra mechanics: landmarks, dash, rewards, decoration, switches and doors, puzzle types, secrets, hints, boosts, collectibles, throw, score, guards, flee, keys and locked doors, push and pull, transform, collectible creatures, combos, medals/ranks | §4.19–§4.37 |
| Pixel art: low-resolution sprites, visible square pixels, limited palette | §3 |
| Saturated bright, strong colours | §3 palette |
| Pixel font: blocky bitmap letters | §7 |
| Chiptune: retro console bleeps | §6 music |
| Sound effects: retro bleeps, synthesized chip sounds | §6 SFX |
| Screens: title, pause, settings, game over, win, level select, high scores | §7 |
| HUD: score | §7 HUD |
| Effects: screen shake, particles, hit flash | §4.39, §3, §6 |
| Accessibility: colour-blind safe palette, reduced motion, remappable keys | §3, §7, §11 |

## 0.2 Decisions

| Decision | Value | Why |
| --- | --- | --- |
| Player name | Puddle the Frog | Silly, short, fits pixel font |
| Frog hitbox | Normal 14×14 px, duck 14×8 px, squash 8×8 px | Chunky but responsive on a 16 px tile grid |
| One-hit death | Yes | Keeps failure simple, fits “restart the level”, avoids HUD hearts |
| Death interruption | 0.9 s freeze then `gameOver` screen | Preserves real-time feel but allows a required screen |
| Checkpoint behaviour | Touching a spawn point saves a snapshot; death restores that snapshot | Satisfies “restart the level” while making spawn points useful |
| Stomping enemies | Not used | Stomp is not in the allowed mechanics list; enemies are defeated by thrown seed or bounce-bonk |
| Bounce combat rule | If player `bounceTimer > 0` and overlaps enemy, enemy dies | Makes core bounce interact with enemies without adding stomp |
| Score visibility | Only in-game HUD score; rewards/rank shown on win screen | Honours “HUD: score” exactly |
| Combo display | No HUD combo meter; internal multiplier plus particles/win screen note | Keeps HUD score-only |
| Level count | 7 levels | “A handful”, under 30 minutes |
| Target playtime | 18–28 minutes | Under 30 minutes with replay |
| Level select behaviour | Sequential unlock; replay any unlocked level | Matches “sequence of levels” while allowing replay |
| High scores | Top 10 level-clear entries + per-level best | Simple and useful without adding name entry |
| Persistence | `localStorage` | Browser game; settings, unlocks, bests, high scores |
| Menu navigation | Same left/right/up/down/jump/grab inputs, plus pause action | Avoids adding new gameplay systems |
| UI-only pause action | `pause` default Escape/KeyP | Required for pause screen; not a gameplay mechanic |
| Randomness | Seeded `mulberry32` per level | Deterministic tests and consistent traps/enemy timing |
| Presentation randomness | Also uses `state.rng` | Reduces nondeterminism and respects reduced motion |
| Decoration mechanic | Decorations are non-solid “boopable” scenery; player or seed overlap gives +5 once | Makes decoration a concrete used mechanic without blocking movement |
| Landmark mechanic | Press `landmark` near a sign for +50 once and a 0.8 s exit arrow | Gives landmarks a named input and number |
| Hint mechanic | Press `hint` near a sign to show level hint for 3 s | Gives hints a named input and number |
| Transform mechanic | `transform` turns frog into 8×8 Squash for 1.5 s, cooldown 3 s | Concrete extra move; useful for small gaps |
| Flee mechanic | Tad creatures flee for 0.7 s when player is close, then can be rescued | Connects flee and collectible creatures cleanly |
| Guards mechanic | Guard enemies patrol and block a door until defeated | Gives guards a concrete role separate from basic enemies |
| Push and pull mechanic | Push by moving into objects; pull by holding `grab` | Concrete extra interaction |
| Keys and locked doors | Key pickup consumed by locked door | Classic but simple |
| Medals/ranks | Bronze/Silver/Gold/Froggy per level based on final score and conditions | Gives win screen meaning without HUD clutter |
| Colour-blind safety | Blue/yellow/magenta/cyan/orange palette, black outlines, shape symbols | Avoids red/green dependency |
| Reduced motion | Screen shake amplitude 0, particles 0, hit flash disabled | Direct accessibility support |
| Remappable keys | All gameplay actions remappable in settings | Direct accessibility support |

## 0.3 Tiers

| Tier | Name | Contains | “Done” means |
| --- | --- | --- | --- |
| 1 | Core Frog | Move, jump, gravity, map/world, falling, bounce, exit, title/playing/gameOver/win stubs, score field, fixed loop, basic canvas, HUD score | A player can finish Level 1 core: move, jump, bounce, fall or reach exit |
| 2 | Hazard & Mobility | Traps, environmental damage, physics objects, swim, enemies, difficulty ramp, special move double jump, dodge duck, spawn points, climb, unlocks, Levels 1–3 playable slice | Player can die to hazards, defeat enemies, swim, climb, use checkpoints, unlock Level 3 |
| 3 | Score & World Gimmicks | Landmarks, rewards, decoration, switches/doors, puzzle types, secrets, hints, boosts, collectibles, throw, score, high scores, Levels 1–7 content skeleton | Player can collect, throw seeds, solve switches/doors, find secrets, see score/high scores |
| 4 | Advanced World | Guards, flee, keys/locked doors, push/pull, transform, collectible creatures, combos, medals/ranks, final Level 7 | Full roster and rank conditions work; all 7 levels clearable |
| 5 | Presentation & Accessibility | Chiptune music, SFX, screen shake, particles, hit flash, settings, reduced motion, remappable keys, colour-blind aids, high scores persistence | All required presentation/accessibility systems work; game is shippable |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Item | Value / Convention |
| --- | --- |
| Space | 2D side-on |
| X axis | Right = positive |
| Y axis | Down = positive |
| Pixel | 1 game pixel = 1 screen pixel at base resolution |
| Base canvas | 320×180 px |
| Tile size | 16 px |
| Time step | Fixed 1/60 s = 0.016666… s |
| Max frame delta | 0.1 s |
| Timer units | seconds |
| Speed units | px/s |
| Acceleration units | px/s² |
| Angle units | radians |
| Viewport | 320×180 px |
| Level bounds | Defined per level in tiles; camera clamped |
| Death fall line | `levelHeightPx + 32` below player bottom |
| Player normal size | 14×14 px |
| Player duck size | 14×8 px |
| Player squash size | 8×8 px |
| Ground speed | 132 px/s |
| Duck speed | 79 px/s |
| Swim speed | 80 px/s |
| Ground acceleration | 1100 px/s² |
| Ground friction | 1400 px/s² |
| Air acceleration | 700 px/s² |
| Jump velocity | -330 px/s |
| Double jump velocity | -260 px/s |
| Water jump/swim-up speed | -150 px/s |
| Gravity | 1200 px/s² |
| Falling gravity | 1600 px/s² |
| Max fall speed | 520 px/s |
| Water max fall speed | 120 px/s |
| Coyote time | 0.09 s |
| Jump buffer | 0.10 s |
| Variable jump release multiplier | 1.9× gravity while rising if jump released |
| Bounce pad launch | -470 px/s on land, -240 px/s in water |
| Bounce pad cooldown | 0.10 s |
| Player bounce bonk timer | 0.25 s |
| Boost pad speed | 360 px/s horizontal, -380 px/s vertical |
| Boost pad duration | 0.22 s |
| Dash speed | 320 px/s |
| Dash duration | 0.15 s |
| Dash cooldown | 0.50 s |
| Dash i-frames | 0.15 s |
| Throw seed speed | 420 px/s |
| Throw seed lifetime | 0.80 s |
| Throw cooldown | 0.25 s |
| Max active seeds | 1 |
| Transform squash duration | 1.50 s |
| Transform cooldown | 3.00 s |
| Climb speed | 96 px/s |
| Vine jump off speed | -260 px/s |
| Checkpoint invulnerability | 1.00 s |
| Camera lookahead | 16 px in facing direction |
| Camera smoothing | 0.18 per fixed step |
| Camera max speed | 480 px/s |
| Max particles | 32 normal, 0 reduced motion |
| Max screen shake magnitude | 4 px, 0 reduced motion |
| Hit flash duration | 0.12 s, disabled reduced motion |
| Combo window | 2.00 s |
| Max combo multiplier | 5 |
| Puffer mine fuse | 0.60 s |
| Puffer trigger radius | 40 px |
| Puffer explosion radius | 30 px |
| Swinging log length | 40 px |
| Swinging log width | 8 px |
| Swinging log angular speed | 1.60 rad/s |
| Acid puddle | Instant death |
| Sour mist kill timer | 0.40 s |
| Tad flee radius | 64 px |
| Tad flee speed | 200 px/s |
| Tad flee duration | 0.70 s |
| Tad follow speed | 80 px/s |
| Tad follow offset | 12 px behind player |
| Landmark radius | 48 px |
| Landmark arrow duration | 0.80 s |
| Landmark score | +50 once |
| Hint radius | 48 px |
| Hint display duration | 3.00 s |
| Hint cooldown | 1.00 s |
| Decoration boop score | +5 once |
| Grab range | 48 px |
| Pull speed | 80 px/s |
| Push max object speed | 120 px/s |
| Key door open | Permanent |
| Timed switch door open | 4.00 s |
| Permanent switch door open | Permanent |
| Pressure plate hold time | 0.20 s |
| Bounce beacon open time | 4.00 s |
| Guard door-block radius | 24 px |
| Guard honk radius | 48 px |

## 1.2 Important conventions

1. Gameplay runs on a fixed step of `1/60 s`. Rendering may interpolate, but rules always use fixed-step time.
2. All gameplay-affecting randomness uses `state.rng`, a seeded `mulberry32` instance seeded per level: `seed = levelIndex * 7919 + 1234`.
3. Presentation randomness also uses `state.rng` unless reduced motion disables it.
4. All timers are in seconds and decrement by `dt`.
5. All damage is instant. The frog has 1 hit point. There is no health bar.
6. The only failure is death. Death always leads to `gameOver`, then retry restores the active spawn snapshot.
7. The only win condition is touching the exit.
8. No mechanic outside the allowed list may be added. If a system would require health, lives, inventory screens, crafting, dialogue, shops, or stomp damage, it is not allowed.
9. The in-game HUD contains only score.
10. The game uses exactly these screens: `title`, `levelSelect`, `playing`, `paused`, `settings`, `gameOver`, `win`, `highScores`.
11. The allowed effects are exactly: screen shake, particles, hit flash.
12. The palette is colour-blind safe by default: no red/green-only distinctions.
13. All keys are remappable in settings.
14. The game must work without external files: sprites are drawn from code arrays or primitive rectangles; audio is synthesized.
15. Level data is hand-authored and deterministic.
16. Module code must not mutate global state directly unless the module owns that state.

# 2. CONTRACTS

## 2.1 Module layout

| Module | Responsibility |
| --- | --- |
| `src/main.ts` | Bootstrap, loop, screen routing |
| `src/core/constants.ts` | All numeric constants from §1 |
| `src/core/rng.ts` | `mulberry32`, `createRng` |
| `src/core/math.ts` | `clamp`, `lerp`, `aabb`, `rectIntersects` |
| `src/state/state.ts` | Create global state, transitions, save/load |
| `src/input/input.ts` | Bindings, key polling, action state |
| `src/game/level.ts` | Load level data, tiles, camera bounds, spawn points |
| `src/game/player.ts` | Player movement, jump, duck, swim, climb, abilities |
| `src/game/enemies.ts` | Enemy AI, defeat, guards |
| `src/game/traps.ts` | Trap update and states |
| `src/game/environment.ts` | Acid, mist, water zones |
| `src/game/physics.ts` | Physics objects, push/pull, collisions |
| `src/game/pickups.ts` | Collectibles, score, combo, secrets |
| `src/game/systems.ts` | Switches, doors, keys, puzzles, landmarks, hints, boosts, decoration |
| `src/game/creatures.ts` | Tad flee/rescue/follow |
| `src/game/effects.ts` | Screen shake, particles, hit flash |
| `src/game/audio.ts` | Music and SFX synthesis |
| `src/ui/ui.ts` | Screen state, HUD, DOM screens |
| `src/render/renderer.ts` | Draw canvas world and sprites |
| `src/debug/debug.ts` | Debug API |

## 2.2 Global context

```ts
type Screen =
  | 'title'
  | 'levelSelect'
  | 'playing'
  | 'paused'
  | 'settings'
  | 'gameOver'
  | 'win'
  | 'highScores';

type Action =
  | 'left'
  | 'right'
  | 'jump'
  | 'up'
  | 'down'
  | 'ability'
  | 'dash'
  | 'throw'
  | 'transform'
  | 'hint'
  | 'landmark'
  | 'grab'
  | 'pause';

interface Settings {
  musicVolume: number;
  sfxVolume: number;
  reducedMotion: boolean;
  colorBlindAids: boolean;
  bindings: Record<Action, string[]>;
}

interface ScoreState {
  current: number;
  comboCount: number;
  comboTimer: number;
  comboMultiplier: number;
  maxComboMultiplier: number;
  noDeath: boolean;
  allCollectibles: boolean;
  secretFound: boolean;
  rewardBonuses: number[];
}

interface Player {
  x: number;
  y: number;
  vx: number;
  vy: number;
  w: number;
  h: number;
  facing: 1 | -1;
  onGround: boolean;
  inWater: boolean;
  onVine: boolean;
  ducking: boolean;
  squashTimer: number;
  squashCooldown: number;
  airJumps: number;
  coyoteTimer: number;
  jumpBufferTimer: number;
  jumpHeld: boolean;
  bounceTimer: number;
  dashTimer: number;
  dashCooldown: number;
  dashIFrames: number;
  throwCooldown: number;
  activeSeed: { x: number; y: number; vx: number; lifetime: number } | null;
  dead: boolean;
  deadTimer: number;
  invulnerable: number;
  grabbedObject: number; // physics object id or -1
  swimInput: number;
  climbInput: number;
}

interface Enemy {
  id: number;
  type: 'snail' | 'buzz' | 'pump' | 'guard';
  x: number;
  y: number;
  vx: number;
  vy: number;
  dir: 1 | -1;
  state: 'idle' | 'patrol' | 'flee' | 'honk' | 'dead';
  range: number;
  minX: number;
  maxX: number;
  hp: number;
  score: number;
  guardDoorId: number; // -1 unless guard
  honkTimer: number;
  deadTimer: number;
}

interface Trap {
  id: number;
  type: 'spike' | 'log' | 'puffer';
  x: number;
  y: number;
  state: 'idle' | 'armed' | 'exploded' | 'rotating';
  timer: number;
  angle: number;
  angleVel: number;
  pivotX: number;
  pivotY: number;
}

interface PhysicsObject {
  id: number;
  type: 'pebble' | 'mudpot';
  x: number;
  y: number;
  vx: number;
  vy: number;
  w: number;
  h: number;
  mass: number;
  onGround: boolean;
  grabbed: boolean;
}

interface Pickup {
  id: number;
  type: 'leaf' | 'lily' | 'tad' | 'secret' | 'key';
  x: number;
  y: number;
  collected: boolean;
}

interface Creature {
  id: number;
  type: 'tad';
  x: number;
  y: number;
  vx: number;
  vy: number;
  state: 'idle' | 'flee' | 'rescued';
  fleeTimer: number;
}

interface Switch {
  id: number;
  x: number;
  y: number;
  pressed: boolean;
  timed: boolean;
  openTimer: number;
}

interface Door {
  id: number;
  x: number;
  y: number;
  open: boolean;
  locked: boolean;
  guardBlocked: boolean;
  openTimer: number;
  switchId: number;
}

interface Landmark {
  id: number;
  x: number;
  y: number;
  rung: boolean;
  arrowTimer: number;
  cooldown: number;
}

interface Hint {
  id: number;
  x: number;
  y: number;
  text: string;
  showTimer: number;
  cooldown: number;
}

interface Decoration {
  id: number;
  x: number;
  y: number;
  type: 'mushroom' | 'lily' | 'rock' | 'sign';
  booped: boolean;
  wobble: number;
}

interface LevelRuntime {
  index: number;
  name: string;
  widthTiles: number;
  heightTiles: number;
  tiles: Uint8Array;
  spawn: { x: number; y: number };
  exit: { x: number; y: number };
  activeCheckpoint: number;
  snapshots: {
    score: number;
    collected: boolean[];
    rescued: boolean[];
    secretFound: boolean;
    keys: number;
    switchesPressed: boolean[];
    doorsOpen: boolean[];
  }[];
  checkpoints: { x: number; y: number }[];
}

interface SaveData {
  settings: Settings;
  unlockedLevel: number;
  levelBests: number[];
  medals: (null | 'bronze' | 'silver' | 'gold' | 'froggy')[];
  highScores: { levelIndex: number; score: number; medal: string; time: number }[];
}

interface GameState {
  screen: Screen;
  time: number;
  dt: number;
  level: LevelRuntime;
  player: Player;
  enemies: Enemy[];
  traps: Trap[];
  physicsObjects: PhysicsObject[];
  pickups: Pickup[];
  creatures: Creature[];
  switches: Switch[];
  doors: Door[];
  landmarks: Landmark[];
  hints: Hint[];
  decorations: Decoration[];
  boosts: { id: number; x: number; y: number; dir: 'left' | 'right' | 'up' | 'down'; active: boolean; timer: number }[];
  keys: number;
  score: ScoreState;
  settings: Settings;
  save: SaveData;
  rng: () => number;
  camera: { x: number; y: number; shakeX: number; shakeY: number; shakeMagnitude: number; shakeTimer: number };
  effects: { particles: { x: number; y: number; vx: number; vy: number; life: number; color: number }[]; hitFlash: number };
  audio: { musicState: 'title' | 'play' | 'win' | 'gameOver' };
  ui: { selected: number; hintText: string; hintTextTimer: number };
}
```

| Field | Required because |
| --- | --- |
| `screen` | State machine in §7 |
| `time`, `dt` | Real-time fixed loop |
| `level` | Map/world, spawn points, exit |
| `player` | All player rules |
| `enemies` | Enemy rules |
| `traps` | Trap rules |
| `physicsObjects` | Physics objects and push/pull |
| `pickups` | Collectibles, secrets, keys, score |
| `creatures` | Collectible creatures and flee |
| `switches`, `doors` | Switches, doors, keys, puzzles |
| `landmarks`, `hints`, `decorations`, `boosts` | Extra world mechanics |
| `keys` | Keys and locked doors |
| `score` | Score, combo, rewards |
| `settings` | Accessibility and volume |
| `save` | Unlocks, high scores, persistence |
| `rng` | Determinism |
| `camera` | Side-on camera and shake |
| `effects` | Required effects |
| `audio` | Music state |
| `ui` | Menu selection and hint display |

## 2.3 Module specifics

| Module | Required exported functions |
| --- | --- |
| `core/rng` | `createRng(seed: number): () => number` |
| `core/math` | `clamp(v: number, a: number, b: number): number`, `lerp(a: number, b: number, t: number): number`, `aabb(a: Rect, b: Rect): boolean` |
| `state/state` | `createGameState(): GameState`, `loadSave(): SaveData`, `saveState(state: GameState): void`, `transition(state: GameState, next: Screen): void` |
| `input/input` | `initInput(el: HTMLElement): void`, `getInput(action: Action): boolean`, `consumePress(action: Action): boolean`, `remap(state: GameState, action: Action, code: string): void` |
| `game/level` | `loadLevel(state: GameState, index: number): void`, `tileAt(state: GameState, tx: number, ty: number): number`, `collideRect(state: GameState, x: number, y: number, w: number, h: number, ignoreDoors?: boolean): boolean`, `setCheckpoint(state: GameState, index: number): void`, `restoreSnapshot(state: GameState): void` |
| `game/player` | `updatePlayer(state: GameState, dt: number): void`, `die(state: GameState): void`, `respawn(state: GameState): void`, `setSquash(state: GameState, on: boolean): void` |
| `game/enemies` | `updateEnemies(state: GameState, dt: number): void`, `defeatEnemy(state: GameState, id: number): void`, `spawnEnemy(state: GameState, type: Enemy['type'], x: number, y: number): number` |
| `game/traps` | `updateTraps(state: GameState, dt: number): void`, `triggerPuffer(state: GameState, id: number): void` |
| `game/environment` | `updateEnvironment(state: GameState, dt: number): void` |
| `game/physics` | `updatePhysics(state: GameState, dt: number): void`, `grabObject(state: GameState, id: number): void`, `releaseObject(state: GameState): void`, `impulse(state: GameState, id: number, vx: number, vy: number): void` |
| `game/pickups` | `updatePickups(state: GameState, dt: number): void`, `collect(state: GameState, id: number): void`, `addScore(state: GameState, base: number, usesCombo: boolean): void` |
| `game/systems` | `updateSystems(state: GameState, dt: number): void`, `pressSwitch(state: GameState, id: number): void`, `openDoor(state: GameState, id: number, permanent: boolean): void`, `unlockDoor(state: GameState, id: number): void` |
| `game/creatures` | `updateCreatures(state: GameState, dt: number): void`, `rescue(state: GameState, id: number): void` |
| `game/effects` | `addParticles(state: GameState, x: number, y: number, color: number, count: number): void`, `shake(state: GameState, magnitude: number): void`, `hitFlash(state: GameState): void`, `updateEffects(state: GameState, dt: number): void` |
| `game/audio` | `playMusic(state: GameState, name: 'title' | 'play' | 'win' | 'gameOver'): void`, `playSfx(state: GameState, name: string): void` |
| `ui/ui` | `renderUI(state: GameState): void`, `onUiInput(state: GameState, action: Action): void` |
| `render/renderer` | `render(state: GameState): void` |
| `debug/debug` | All functions listed in §8 |

# 3. VISUAL SPEC

The look is a wet, bouncy, silly pond in saturated pixel art. The base canvas is 320×180 and is scaled up with integer CSS scaling so pixels remain square. Every sprite uses a 16-color palette, thick black outlines, and simple readable silhouettes. The frog is a bright mint blob with big eyes; enemies are round or spiky enough to read at 16 px. The world feels like a cartoon diorama: mud, lily pads, water, mushrooms, and weird little machines, all in bright colours.

Lighting and atmosphere are flat and cheerful. There is no dynamic lighting. Shadow is represented by one dithered dark indigo pixel row under objects. Water has a slow two-frame glisten. Danger is signalled by magenta/orange and shape symbols, not colour alone.

The space is a side-on tile world. Foreground, midground, and background use the same palette. Background layers scroll at 0.25 and 0.5 parallax. Gameplay tiles are 16×16. The camera is side-on and clamped to level bounds.

| Asset | Palette use | Pixel recipe | Motion / frames | Gameplay implication |
| --- | --- | --- | --- | --- |
| Puddle frog | Mint body, white eye, black outline, yellow tongue dot | 14×14 rounded square, 2 px eye, 4 px mouth | idle 2 frames, run 4 frames, jump 2 frames, duck 1 frame, squash 1 frame | Size changes for duck/squash |
| Squash frog | Same, smaller | 8×8 circle | 1 frame, slight wobble | Passes 8 px gaps |
| Bounce pad | Yellow top, orange base, black arrow | 16×8 pad with upward arrow | 2 frames compress/release | Launches player |
| Boost pad | Cyan arrow on yellow | 16×16 arrow | 2 frame blink | Sets player velocity |
| Exit pad | Magenta swirl, white ring | 16×32 vertical pad | 3-frame swirl | Win trigger |
| Spike trap | Magenta triangles, black outline | 16×8 row of triangles | 2-frame up/down | Death zone |
| Swinging log | Orange brown bar, black outline | 40×8 bar on pivot | Continuous rotation | Rotating death |
| Puffer mine | Orange sphere, magenta spikes | 12×12 | idle, armed blink, exploded | Timer death |
| Acid puddle | Orange/yellow bubbles, black outline | 16×8 surface | 3-frame bubbles | Instant death |
| Sour mist | Pink cloud, white bubbles | 16×16 cloud | 2-frame drift | 0.4 s kill |
| Water | Cyan surface, light cyan body | 16×16 | 2-frame glisten | Swim zone |
| Vine | Mint ladder, black outline | 8×16 | 1 frame | Climb |
| Pebble | Grey-blue stone, black outline | 12×12 | 1 frame | Physics object |
| Mud pot | Brown pot, black rim | 16×16 | 1 frame | Physics object |
| Switch | Yellow lever, black base | 16×16 | 2-frame down/up | Opens doors |
| Door | Indigo planks, black outline | 16×32 | open/close 2 frames | Blocks movement |
| Locked door | Same + magenta lock icon | 16×32 | lock glow 2 frames | Requires key |
| Key | Yellow key, black outline | 8×8 | 2-frame spin | Key pickup |
| Leaf | Mint leaf, yellow vein | 8×8 | 2-frame flutter | +50 |
| Lily | Magenta flower, mint pad | 12×12 | 2-frame bloom | +100 |
| Tad | Cyan blob, black eye | 8×8 | idle/flee/rescued | Collectible creature |
| Secret sprout | Bright yellow sprout, sparkles | 12×12 | 3-frame twinkle | +500 secret |
| Landmark sign | Indigo post, yellow flag | 16×32 | flag 2 frames | Press `landmark` |
| Hint sign | Cyan sign, white question mark | 16×32 | question blink | Press `hint` |
| Decoration mushroom | Magenta cap, white spots | 12×12 | 1-frame wobble | +5 boop |
| Decoration rock | Indigo boulder | 16×16 | 1-frame | +5 boop |
| Decoration lily | Mint pad, magenta bud | 16×8 | 2-frame | +5 boop |
| Guard snoot | Orange frog, yellow helmet | 14×14 | patrol 4 frames, honk 2 | Blocks doors |
| Snail | Cyan shell, mint body | 14×10 | 2-frame creep | Enemy |
| Buzzfly | Yellow body, magenta wings | 12×12 | 4-frame buzz | Enemy |
| Pump toad | Orange toad, white belly | 14×14 | 2-frame hop | Enemy |
| Seed projectile | Yellow circle, black outline | 6×6 | 1 frame | Throw |
| HUD score | White pixel digits, black outline | Canvas text | None | Score only |

# 4. GAMEPLAY SPEC

Puddle the Frog moves freely through side-on tile levels, jumps, bounces off pads, swims in water, climbs vines, ducks, dashes, throws seeds, and solves small switches/doors. The player dies from traps, enemies, hazards, or falling, then retries from the last spawn snapshot. The only goal is to reach the exit. Levels add more hazards, enemies, keys, puzzles, secrets, and creatures until the final level. Score comes from collectibles, enemies, landmarks, decorations, secrets, and rewards. Medals rank the clear.

## 4.1 Records and rosters

### Level roster

| Level | Name | Width tiles | Height tiles | Core focus |
| --- | --- | ---: | ---: | --- |
| 0 | Puddle Yard | 40 | 18 | Move, jump, bounce, exit |
| 1 | Lily Lane | 48 | 18 | Swim, traps, enemies |
| 2 | Mud Banks | 56 | 18 | Physics, climb, doors |
| 3 | Bounce Bog | 60 | 18 | Bounce, guards, boost |
| 4 | Thicket | 64 | 18 | Keys, puzzles, throw |
| 5 | Deep Ledge | 68 | 18 | Swim, secrets, creatures |
| 6 | Giant Splash | 72 | 18 | All mechanics, final rank |

### Enemy roster

| Enemy | Type | Size | Speed | Behaviour | Score | Defeat by |
| --- | --- | ---: | ---: | --- | ---: | --- |
| Sloppy Snail | `snail` | 14×10 | 28 px/s | Patrols 48 px | 100 | Seed, bounce-bonk |
| Zippy Buzz | `buzz` | 12×12 | 120 px/s | Patrols 96 px, sine bob 6 px | 150 | Seed, bounce-bonk |
| Pump Toad | `pump` | 14×14 | 40 px/s | Hops toward player within 64 px | 100 | Seed, bounce-bonk |
| Snoot Guard | `guard` | 14×14 | 60 px/s | Patrols 128 px, honks, blocks door | 200 | Seed, bounce-bonk |

### Trap roster

| Trap | Type | Trigger | Kill rule |
| --- | --- | --- | --- |
| Popper Spike | `spike` | Always | Overlap = death |
| Swinging Log | `log` | Always rotating | Overlap log = death |
| Puffer Mine | `puffer` | Player or seed within 40 px | Fuse 0.6 s, explosion radius 30 px |

### Hazard roster

| Hazard | Type | Rule |
| --- | --- | --- |
| Acid Puddle | `acid` | Overlap = death |
| Sour Mist | `mist` | Overlap accumulates 0.4 s = death |

### Physics object roster

| Object | Type | Size | Mass | Movement |
| --- | --- | ---: | ---: | --- |
| Pebble | `pebble` | 12×12 | 1 | Falls, can be pushed/pulled |
| Mud Pot | `mudpot` | 16×16 | 2 | Falls, can be pushed/pulled |

### Pickup roster

| Pickup | Type | Score | Effect |
| --- | --- | ---: | --- |
| Leaf | `leaf` | 50 | Combo |
| Lily | `lily` | 100 | Combo |
| Tad | `tad` | 200 | Becomes rescued creature, combo |
| Secret Sprout | `secret` | 500 | Sets secret found, combo |
| Key | `key` | 100 | `state.keys += 1`, combo |

### Puzzle roster

| Puzzle | Type | Rule |
| --- | --- | --- |
| Switch Door | `switch_door` | Press permanent switch, door opens permanently |
| Bounce Beacon | `beacon` | Player while `bounceTimer > 0` hits beacon, door opens 4 s |
| Pebble Plate | `plate` | Physics object overlaps plate for 0.2 s, door opens permanently |

## 4.2 Player input and movement — Tier 1

Rules:

1. Player controls are remappable actions.
2. Holding `left` or `right` sets target horizontal velocity.
3. On ground:
   - target speed = 132 px/s
   - acceleration = 1100 px/s²
   - friction = 1400 px/s²
4. In air:
   - target speed = 132 px/s
   - acceleration = 700 px/s²
5. Ducking:
   - hold `down` on ground and not on vine/water
   - hitbox height becomes 8
   - max horizontal speed = 79 px/s
   - `jump` exits duck with vy = -260 px/s
6. Squash:
   - `transform` starts squash if cooldown ready
   - hitbox 8×8
   - duration 1.5 s
   - cooldown 3 s
   - max horizontal speed = 100 px/s
   - jump disabled while squashTimer > 0
7. Facing changes when input is nonzero.
8. Player cannot leave level bounds horizontally; vertical bounds are level-dependent.

## 4.3 Jump — Tier 1

Rules:

1. `jump` sets jumpBufferTimer = 0.10 s.
2. If on ground or coyoteTimer > 0, and jumpBufferTimer > 0:
   - vy = -330 px/s
   - onGround = false
   - coyoteTimer = 0
   - jumpBufferTimer = 0
   - jumpHeld = true
3. Coyote time:
   - when player leaves ground without jumping, coyoteTimer = 0.09 s
4. Variable jump:
   - if jump is released while vy < 0, gravity multiplier = 1.9
5. In water, `jump` acts as swim-up.
6. In vine, `jump` hops off vine with vy = -260 px/s.

## 4.4 Map/world and camera — Tier 1

Rules:

1. Levels are tile grids. Tile size = 16 px.
2. Tile types include solid, bounce, boost, vine, water, acid, mist, spike, exit, checkpoint, decoration, landmark, hint, switch, door, lockDoor, beacon, plate.
3. Solid tiles block player and physics objects.
4. Doors block unless `open` and not `guardBlocked`.
5. Exit is a 16×32 overlap zone.
6. Camera:
   - targetX = player.x + player.facing * 16 - 160
   - targetY = player.y - 90
   - camera lerps to target by 0.18 per fixed step
   - camera max speed = 480 px/s
   - camera clamped to level bounds

## 4.5 Falling and failure — Tier 1 / Spawn points — Tier 2

### Falling, Tier 1

1. Gravity = 1200 px/s².
2. If vy > 0, gravity = 1600 px/s².
3. Max fall = 520 px/s.
4. If player bottom > levelHeightPx + 32, player dies.

### Failure, Tier 1

1. On death:
   - player.dead = true
   - deadTimer = 0.9
   - hitFlash()
   - shake(4)
   - play `death`
2. After deadTimer, screen = `gameOver`.
3. Retry restores the active checkpoint snapshot.

### Spawn points, Tier 2

1. Checkpoint pads are 16×16.
2. Touching a checkpoint:
   - sets `level.activeCheckpoint`
   - saves snapshot:
     - score
     - collected pickups
     - rescued creatures
     - secretFound
     - keys
     - switches pressed
     - doors open
   - plays `checkpoint` SFX if implemented as `switch` sound variant
3. On retry:
   - player respawns at active checkpoint
   - score restored
   - pickup/creature/door/switch/key state restored
   - invulnerable = 1.0 s

## 4.6 Bounce — Tier 1

Rules:

1. Bounce pads are 16×8 solid top tiles.
2. If player overlaps pad from above and pad cooldown <= 0:
   - vy = -470 px/s, or -240 px/s if in water
   - player.bounceTimer = 0.25 s
   - pad cooldown = 0.10 s
   - play `bounce`
   - particles 4 yellow
   - shake(2)
3. While `bounceTimer > 0`, enemy overlap defeats enemy.
4. Bounce does not override player horizontal velocity.

## 4.7 Objectives — Tier 1

Rules:

1. The exit is the only win condition.
2. If player overlaps exit and not dead:
   - screen = `win`
   - compute rewards
   - add rewards to score
   - compute medal
   - save best and high score entry
   - unlock next level
   - play `win`

## 4.8 Traps — Tier 2

Rules:

1. Spike:
   - hitbox 16×8
   - overlap = death
2. Log:
   - pivot fixed
   - angle += angleVel * dt
   - collision is rotated rectangle approximated as 3 circles: pivot, mid, end
   - overlap = death
3. Puffer:
   - idle until player or seed within 40 px
   - state = armed, timer = 0.6
   - on timer expire:
     - state = exploded
     - if player within 30 px = death
     - particles 8 orange
     - shake(3)
     - play `explode`
   - seed can trigger puffer; if player outside 30 px, no death
   - defeated puffer gives +50 score

## 4.9 Environmental damage — Tier 2

Rules:

1. Acid puddle:
   - overlap = death
2. Sour mist:
   - if player inside, mistTimer += dt
   - if outside, mistTimer = 0
   - if mistTimer >= 0.4, death
3. Water is not environmental damage.

## 4.10 Physics objects — Tier 2 / Push and pull — Tier 4

### Physics objects, Tier 2

1. Objects have gravity 1200 px/s².
2. Objects collide with solid tiles.
3. Objects can be pushed by player horizontal movement.
4. Bounce pads launch objects upward at -320 px/s.
5. Seed hit applies impulse 120 px/s in seed direction.

### Push and pull, Tier 4

1. Push:
   - if player moving into ungrabbed object, object.vx = player.vx * 0.8
   - object max speed = 120 px/s
2. Pull:
   - hold `grab`
   - player grabs nearest object within 48 px
   - one object max
   - object moves toward player at 80 px/s
   - release `grab` drops object
3. Carried object can activate switches and plates.

## 4.11 Swim — Tier 2

Rules:

1. Water tiles set `player.inWater = true`.
2. In water:
   - gravity = 0
   - horizontal max speed = 80 px/s
   - acceleration = 900 px/s²
   - holding `up` sets vy = -150 px/s
   - holding `down` sets vy = 100 px/s
   - no down input sets vy = 0
   - max fall = 120 px/s
3. Bounce pads work in water with vy = -240 px/s.
4. Acid and mist are separate from water.

## 4.12 Enemies — Tier 2

Rules:

1. Enemy contact = death unless player.dashIFrames > 0 or invulnerable > 0.
2. Enemy defeat:
   - seed direct overlap
   - player overlap while bounceTimer > 0
3. On defeat:
   - add score
   - particles 6 enemy colour
   - play `enemyDie`
   - state = dead, deadTimer = 0.3
4. Enemy motion:
   - snail: patrol between minX/maxX, speed 28
   - buzz: patrol horizontal, y bob = sin(time * 6) * 6
   - pump: if player within 64 px, hop: vy = -180, vx toward player = 40; else idle
   - guard: patrol between minX/maxX, speed 60; if player within 48 px, honk 0.5 s, honkTimer

## 4.13 Difficulty ramp — Tier 2

Rules:

1. Levels increase hazard density.
2. Counts are fixed per level roster in §4.38.
3. No random enemy spawning; all enemies/traps/hazards are placed in level data.
4. Difficulty comes from count, placement, and required mechanics.

## 4.14 Abilities/special moves — Tier 2

Rules:

1. `ability` is the special move.
2. On ground: nothing.
3. In air: if airJumps > 0:
   - vy = -260 px/s
   - airJumps -= 1
   - play `doubleJump`
   - particles 3 cyan
4. In water: if airJumps > 0:
   - vy = -220 px/s
   - airJumps -= 1
   - play `doubleJump`
5. airJumps resets to 1 when onGround or inWater.

## 4.15 Dodge — Tier 2

Rules:

1. Dodge is duck.
2. Hold `down` on ground, not vine, not water:
   - ducking = true
   - hitbox height = 8
   - max speed = 79 px/s
3. Release `down` or press `jump` ends duck.
4. Ducking does not grant i-frames.

## 4.16 Climb — Tier 2

Rules:

1. Vine tiles are non-solid.
2. If player overlaps vine:
   - onVine = true
   - gravity = 0
   - vx = 0 unless `left`/`right` taps? No: horizontal movement disabled while on vine.
3. Holding `up`: vy = -96 px/s.
4. Holding `down`: vy = +96 px/s.
5. No up/down: vy = 0.
6. `jump` hops off vine: onVine = false, vy = -260 px/s.
7. Climbing resets airJumps to 1.

## 4.17 Unlocks — Tier 2

Rules:

1. Level 0 is unlocked at start.
2. Winning level N unlocks level N+1.
3. Level select shows locked levels as greyed out with lock icon.
4. Locked levels cannot be selected.

## 4.18 Landmarks — Tier 3

Rules:

1. Landmark sign is 16×32.
2. If player within 48 px and `landmark` pressed:
   - if not rung:
     - addScore(50, false)
     - rung = true
     - play `landmark`
   - arrowTimer = 0.8
   - cooldown = 2.0
3. Arrow points from player to exit for 0.8 s.
4. Reduced motion: arrow still shows but no particles.

## 4.19 Rewards — Tier 3

Rules:

1. Rewards are computed on exit.
2. Bonuses:
   - No Death: +500 if `score.noDeath`
   - All Collectibles: +300 if all pickups collected
   - Secret Found: +500 if `score.secretFound`
   - Max Combo: +250 if `score.maxComboMultiplier >= 5`
3. Bonuses are added to `score.current` before medal computation.

## 4.20 Decoration — Tier 3

Rules:

1. Decorations are non-solid.
2. If player or seed overlaps unbooped decoration:
   - addScore(5, false)
   - booped = true
   - wobble = 0.3
   - particles 3 decoration colour
   - play `boop`
3. Booped decorations remain in place and no longer score.

## 4.21 Switches and doors — Tier 3

Rules:

1. Switch is 16×16.
2. Player, seed, or physics object overlap can press switch.
3. Switch types:
   - timed: door opens 4 s
   - permanent: door opens permanently
4. Door:
   - 16×32 solid unless open
   - open animation 0.3 s
   - blocks player and physics objects
5. Door openTimer decrements for timed doors.
6. Permanent doors do not close.

## 4.22 Puzzle types — Tier 3

Rules:

1. Switch Door:
   - one permanent switch controls one door
2. Bounce Beacon:
   - beacon is 16×16 target
   - if player overlaps beacon while bounceTimer > 0:
     - linked door opens 4 s
     - play `switch`
3. Pebble Plate:
   - plate is 16×8
   - if physics object with mass >= 1 overlaps for 0.2 s:
     - linked door opens permanently
     - play `switch`

## 4.23 Secrets — Tier 3

Rules:

1. Secret Sprout is a pickup.
2. Collecting secret:
   - addScore(500, true)
   - score.secretFound = true
   - particles 10 yellow
   - play `secret`
3. Secrets are hidden but do not require hidden level.

## 4.24 Hints — Tier 3

Rules:

1. Hint sign is 16×32.
2. If player within 48 px and `hint` pressed and cooldown <= 0:
   - ui.hintText = hint.text
   - ui.hintTextTimer = 3.0
   - hint.cooldown = 1.0
   - play `hint`
3. Hint text is shown in a small pixel-font box above the player; it is not HUD score.

## 4.25 Boosts — Tier 3

Rules:

1. Boost pads are 16×16.
2. If player overlaps boost:
   - set velocity:
     - left: vx = -360
     - right: vx = 360
     - up: vy = -380
     - down: vy = 180
   - boost timer = 0.22
   - play `boost`
   - particles 4 cyan
3. While boost timer > 0, gravity is 50% normal.

## 4.26 Collectibles — Tier 3

Rules:

1. Collectibles are pickups.
2. Overlap collects them.
3. Collection:
   - collected = true
   - addScore(base, true)
   - particles by type
   - SFX by type
4. All collectibles condition uses all pickup IDs in level.

## 4.27 Throw — Tier 3

Rules:

1. `throw` creates one seed if no active seed and throwCooldown <= 0.
2. Seed:
   - position = player centre + facing * 8
   - vx = facing * 420
   - lifetime = 0.8
   - size 6×6
3. Seed:
   - travels straight
   - dies on solid tile
   - can defeat enemies
   - can trigger puffer mines
   - can press switches
   - can boop decorations
   - can impulse physics objects
4. throwCooldown = 0.25.
5. play `throw` on create, `seedHit` on hit.

## 4.28 Score — Tier 3

Rules:

1. `score.current` starts 0 per level.
2. Score can be added by pickups, enemies, landmarks, decorations, puffer defeat, rewards.
3. Combo applies only to pickups.
4. Combo:
   - on pickup collect:
     - if comboTimer <= 0, comboCount = 0
     - comboCount += 1
     - comboMultiplier = min(5, comboCount)
     - comboTimer = 2.0
   - add base * comboMultiplier
   - maxComboMultiplier = max(maxComboMultiplier, comboMultiplier)
5. Combo timer decrements; if <= 0, comboCount = 0.
6. Death resets combo and restores snapshot score.
7. HUD displays `score.current` only.

## 4.29 Guards — Tier 4

Rules:

1. Guard is enemy type `guard`.
2. Guard has `guardDoorId`.
3. If guard alive and within 24 px of its door:
   - door.guardBlocked = true
4. If guard defeated:
   - linked door.guardBlocked = false permanently
5. Guard honks when player within 48 px.
6. Defeat score = 200.

## 4.30 Flee — Tier 4

Rules:

1. Flee applies to Tad creatures.
2. If player within 64 px and Tad state = idle:
   - state = flee
   - fleeTimer = 0.7
   - velocity away from player = 200 px/s
3. While fleeing:
   - cannot be rescued
4. When fleeTimer expires:
   - state = idle
   - velocity = 0
5. Rescued Tads no longer flee.

## 4.31 Keys and locked doors — Tier 4

Rules:

1. Key pickup:
   - state.keys += 1
   - addScore(100, true)
2. Locked door:
   - if player overlaps and state.keys > 0:
     - state.keys -= 1
     - door.locked = false
     - door.open = true permanently
     - play `keyDoor`
3. If no key, door remains solid.

## 4.32 Transform — Tier 4

Rules:

1. `transform` starts squash if squashCooldown <= 0.
2. Squash:
   - hitbox 8×8
   - squashTimer = 1.5
   - squashCooldown = 3.0
   - max speed = 100 px/s
   - jump disabled
3. Squash can pass through 8 px vertical gaps in level design.
4. Squash does not grant i-frames.
5. play `transform`.

## 4.33 Collectible creatures — Tier 4

Rules:

1. Tad is a creature.
2. Tad can be idle, fleeing, rescued.
3. If player overlaps idle Tad:
   - rescue:
     - state = rescued
     - addScore(200, true)
     - particles 5 cyan
     - play `rescue`
4. Rescued Tad follows:
   - target position = player.x - player.facing * 12, player.y
   - movement speed 80 px/s
5. Max rescued Tads per level = roster count; all can follow.
6. On death, rescued state restores from snapshot.

## 4.34 Combos — Tier 4

Rules:

1. Combo is part of score.
2. Only pickups count.
3. Multiplier max 5.
4. Max combo is recorded for reward and win screen.

## 4.35 Medals/ranks — Tier 4

Rules:

1. Medal computed after rewards.
2. Rank conditions:
   - Bronze: exit reached
   - Silver: final score >= Silver threshold and noDeath
   - Gold: final score >= Gold threshold and allCollectibles and noDeath
   - Froggy: final score >= Froggy threshold and allCollectibles and noDeath and (secretFound or maxComboMultiplier >= 5)
3. Per-level thresholds:

| Level | Silver | Gold | Froggy |
| --- | ---: | ---: | ---: |
| 0 | 350 | 600 | 900 |
| 1 | 550 | 950 | 1400 |
| 2 | 750 | 1300 | 1800 |
| 3 | 950 | 1600 | 2200 |
| 4 | 1150 | 1900 | 2600 |
| 5 | 1350 | 2200 | 2900 |
| 6 | 1550 | 2500 | 3300 |

## 4.36 Progression and difficulty

Rules:

1. Levels are a sequence.
2. Level select shows all 7 levels with locked state, best score, medal.
3. Winning level N unlocks N+1.
4. Difficulty ramp counts per level:

| Level | Leaves | Lilies | Tads | Secrets | Keys | Snails | Buzzes | Pumps | Guards | Traps | Hazards | Physics | Checkpoints | Vines | Bounce | Boosts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| 1 | 6 | 2 | 1 | 1 | 0 | 2 | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 1 | 3 | 1 |
| 2 | 8 | 3 | 1 | 1 | 1 | 2 | 1 | 1 | 0 | 3 | 2 | 2 | 2 | 2 | 4 | 2 |
| 3 | 10 | 4 | 2 | 2 | 1 | 3 | 1 | 1 | 1 | 4 | 2 | 3 | 2 | 2 | 5 | 2 |
| 4 | 12 | 5 | 2 | 2 | 2 | 3 | 2 | 1 | 2 | 5 | 3 | 4 | 3 | 3 | 6 | 3 |
| 5 | 14 | 6 | 3 | 3 | 2 | 3 | 2 | 2 | 2 | 6 | 4 | 5 | 3 | 4 | 7 | 4 |
| 6 | 16 | 8 | 3 | 3 | 3 | 4 | 2 | 3 | 3 | 7 | 5 | 6 | 4 | 4 | 8 | 5 |

5. Landmarks, hints, decorations:

| Level | Landmarks | Hints | Decorations |
| --- | ---: | ---: | ---: |
| 0 | 1 | 1 | 3 |
| 1 | 1 | 1 | 4 |
| 2 | 2 | 1 | 5 |
| 3 | 2 | 1 | 6 |
| 4 | 2 | 1 | 7 |
| 5 | 3 | 1 | 8 |
| 6 | 3 | 1 | 10 |

6. Hint text:

| Level | Hint |
| --- | --- |
| 0 | Bounce pads launch you higher than your hop. |
| 1 | Duck to slide under low spikes. |
| 2 | Pebbles can be pushed onto plates. |
| 3 | Bounce into beacons to open doors. |
| 4 | Keys open locked doors. |
| 5 | Tads flee at first, then can be rescued. |
| 6 | Squash fits through tiny gaps. |

## 4.37 Feel

1. Movement is snappy: acceleration 1100 px/s², max speed 132 px/s.
2. Jump release immediately increases gravity while rising.
3. Bounce is loud and shakey: SFX + 4 particles + shake 2.
4. Death is brief: 0.9 s, hit flash, shake 4.
5. Collectibles produce small particles and quick SFX.
6. Combo increases particle count from 3 to 8 based on multiplier.
7. Reduced motion removes shake, particles, and hit flash but keeps gameplay timing unchanged.

# 5. CHARACTERS

## Puddle the Frog

Silhouette: rounded square, big white eyes, small mouth, short legs.

Animations:

| Animation | Frames | Motion rule |
| --- | ---: | --- |
| idle | 2 | Breathing 2-frame, 2 s period |
| run | 4 | Legs cycle 0.25 s |
| jump | 2 | Stretch up on rising |
| fall | 2 | Legs tucked |
| duck | 1 | 14×8 low pose |
| squash | 1 | 8×8 blob |
| swim | 2 | Horizontal flip, small kick |
| dash | 1 | Motion line 8 px |
| throw | 1 | Arm/tongue extends 6 px |
| hurt | 1 | White flash then dead |
| dead | 2 | X eyes, 0.9 s |

Facings: left/right mirrored.

States gameplay needs:

- onGround
- inWater
- onVine
- ducking
- squashTimer > 0
- dashIFrames > 0
- bounceTimer > 0
- dead

## Sloppy Snail

Silhouette: round shell on top, small body below.

Animations:

| Animation | Frames | Motion rule |
| --- | ---: | --- |
| patrol | 2 | Slow creep |
| dead | 1 | Shell pops, particles |

States: `patrol`, `dead`.

## Zippy Buzz

Silhouette: yellow oval body, magenta wings.

Animations:

| Animation | Frames | Motion rule |
| --- | ---: | --- |
| buzz | 4 | Wings flip 0.1 s |
| dead | 1 | Wings stop |

States: `patrol`, `dead`.

## Pump Toad

Silhouette: wide orange toad, white belly.

Animations:

| Animation | Frames | Motion rule |
| --- | ---: | --- |
| idle | 2 | Belly puff |
| hop | 2 | Jump toward player |
| dead | 1 | Squashed |

States: `idle`, `patrol` as hop, `dead`.

## Snoot Guard

Silhouette: orange frog with yellow helmet.

Animations:

| Animation | Frames | Motion rule |
| --- | ---: | --- |
| patrol | 4 | March |
| honk | 2 | Helmet flash |
| dead | 1 | Toppled |

States: `patrol`, `honk`, `dead`.

## Tad

Silhouette: cyan blob, black eye.

Animations:

| Animation | Frames | Motion rule |
| --- | ---: | --- |
| idle | 2 | Wobble |
| flee | 2 | Fast dash |
| rescued | 2 | Follow bounce |

States: `idle`, `flee`, `rescued`.

# 6. AUDIO

The audio is all synthesized chiptune and retro bleeps. Music uses square leads, triangle bass, and filtered noise drums. SFX use short square/triangle/noise envelopes.

## Music

| Music | Recipe | When |
| --- | --- | --- |
| Title | 92 BPM; square lead arpeggio 392/523/659/784 Hz; triangle bass 98/131/165/196 Hz; noise hi-hat every 8th | `title` |
| Play | 132 BPM; square lead in A minor: 440/523/587/659; triangle bass octave pulses; noise snare on beats 2 and 4 | `playing`, `paused` |
| Win | 140 BPM; square fanfare 523/659/784/1046; triangle bass root; noise crash | `win` |
| Game Over | 110 BPM descending; square 659/523/392/261; triangle low 65; noise thud | `gameOver` |

## SFX

| SFX | Recipe | When |
| --- | --- | --- |
| uiMove | Square 660 Hz, 0.05 s, linear decay | Menu move |
| uiSelect | Square 880 to 1320 Hz over 0.08 s | Menu confirm |
| jump | Square 300 to 600 Hz over 0.07 s | Jump |
| land | Noise 0.04 s, lowpass 800 Hz | Landing |
| bounce | Square 200 to 900 Hz 0.09 s + triangle 80 Hz 0.09 s | Bounce pad |
| doubleJump | Square 500 to 900 Hz 0.06 s | Ability |
| dash | Noise sweep 2000 to 400 Hz 0.10 s | Dash |
| duck | Triangle 200 Hz 0.05 s | Duck start |
| throw | Square 700 to 300 Hz 0.06 s | Throw seed |
| seedHit | Square 1200 Hz 0.03 s | Seed hits |
| enemyDie | Square 400 to 100 Hz 0.12 s + noise 0.05 s | Enemy defeated |
| death | Square 600 to 80 Hz 0.40 s + noise 0.15 s | Player dies |
| collectLeaf | Square 980 to 1320 Hz 0.08 s | Leaf |
| collectLily | Square 1040 to 1560 Hz 0.08 s | Lily |
| collectKey | Square arpeggio 660/990/1320 Hz, 0.15 s total | Key |
| collectTad | Square 880 then 1175 Hz, 0.10 s total | Tad |
| secret | Square fanfare 523/659/784/1046, 0.30 s total | Secret sprout |
| switch | Square 520 Hz 0.05 s | Switch press |
| door | Noise slide 400 to 1200 Hz 0.20 s | Door opens |
| keyDoor | Square 660/990/1320/1980, 0.20 s total | Locked door opens |
| boost | Square 400 to 800 Hz 0.08 s | Boost pad |
| transform | Triangle 800 to 200 Hz 0.15 s | Squash |
| landmark | Triangle 1318 Hz, 0.20 s, decay | Landmark |
| hint | Square 700 Hz twice, 0.05 s each | Hint shown |
| boop | Square 220 Hz, 0.04 s | Decoration boop |
| checkpoint | Square 660 to 990 Hz, 0.08 s | Spawn point |
| win | Square fanfare 523/659/784/1046/1318, 0.60 s total | Win screen |
| gameOver | Square 392/330/261, 0.50 s total | Game over screen |

# 7. UX

HTML and CSS only. The game canvas is 320×180 and scaled by CSS `image-rendering: pixelated`. UI is DOM overlay. Font is a blocky bitmap pixel font; if a webfont is unavailable, fallback is monospace with `font-family: monospace; letter-spacing: 1px;`.

CSS requirements:

```css
canvas {
  image-rendering: pixelated;
  width: 960px;
  height: 540px;
  background: #001018;
}
.screen {
  font-family: 'Press Start 2P', monospace;
  color: #ffffff;
  text-shadow: 2px 2px #000000;
}
button {
  background: #ffd400;
  border: 4px solid #000000;
  color: #000000;
}
button:disabled {
  background: #4a3b82;
}
```

## Screen state machine

| Current screen | Input / event | Next screen |
| --- | --- | --- |
| title | confirm | levelSelect |
| title | highScores button | highScores |
| levelSelect | select unlocked level | playing |
| levelSelect | back | title |
| playing | pause | paused |
| paused | resume | playing |
| paused | settings | settings |
| paused | retry | playing |
| paused | quit | title |
| settings | back | previous screen |
| playing | death | gameOver |
| playing | exit | win |
| gameOver | retry | playing |
| gameOver | title | title |
| win | next level | playing |
| win | levelSelect | levelSelect |
| win | highScores | highScores |
| highScores | back | previous screen |

## HUD

| Element | Record field | When visible |
| --- | --- | --- |
| `#score` | `state.score.current` | `playing`, `paused` |

The HUD displays only score. It is a top-left pixel-font number with black outline.

## Screen layouts

### title

- Game title: “PUDDLE”
- Subtitle: “Frog Platformer”
- Buttons: Play, High Scores
- Footer: “Reach the exit. Bounce a lot.”

### levelSelect

- 7 level buttons in a grid.
- Each unlocked button shows: level number, best score, medal icon if present.
- Locked buttons disabled with lock symbol.
- Back button.

### playing

- Canvas only plus `#score`.

### paused

- Overlay:
  - Resume
  - Settings
  - Retry Level
  - Title

### settings

- Music volume slider 0–100
- SFX volume slider 0–100
- Reduced Motion toggle
- Colour-blind aids toggle
- Key remap list for all actions
- Back button

### gameOver

- Title: “SPLAT!”
- Score line
- Buttons: Retry, Title

### win

- Title: “WET WIN!”
- Score line
- Rewards list
- Medal line
- Buttons: Next Level, Level Select, High Scores

### highScores

- Table: Rank, Level, Score, Medal
- Top 10 entries
- Back button

# 8. DEBUG API

All debug functions are on `window.debug` in development and exposed for tests.

| Function | Purpose |
| --- | --- |
| `debug.input.left()` | Press left |
| `debug.input.right()` | Press right |
| `debug.input.jump()` | Press jump |
| `debug.input.up()` | Press up |
| `debug.input.down()` | Press down |
| `debug.input.ability()` | Press ability |
| `debug.input.dash()` | Press dash |
| `debug.input.throw()` | Press throw |
| `debug.input.transform()` | Press transform |
| `debug.input.hint()` | Press hint |
| `debug.input.landmark()` | Press landmark |
| `debug.input.grab()` | Press grab |
| `debug.input.releaseAll()` | Release all actions |
| `debug.player.setPosition(x, y)` | Set player position |
| `debug.player.setVelocity(x, y)` | Set player velocity |
| `debug.player.setDucking(on)` | Set duck state |
| `debug.player.setAirJumps(n)` | Set double jumps |
| `debug.player.setBounceTimer(t)` | Set bounce bonk timer |
| `debug.player.setDashTimer(t)` | Set dash timer |
| `debug.player.setSquash(on)` | Set transform |
| `debug.player.kill()` | Trigger death |
| `debug.score.set(n)` | Set score |
| `debug.combo.set(count, multiplier, timer)` | Set combo |
| `debug.enemy.spawn(type, x, y)` | Spawn enemy |
| `debug.enemy.defeat(id)` | Defeat enemy |
| `debug.guard.set(id, doorId)` | Assign guard door |
| `debug.trap.set(id, state)` | Set trap state |
| `debug.trap.triggerPuffer(id)` | Arm puffer |
| `debug.env.setMistTimer(t)` | Set mist timer |
| `debug.physics.spawn(type, x, y)` | Spawn physics object |
| `debug.physics.set(id, x, y, vx, vy)` | Set physics object |
| `debug.physics.grab(id)` | Grab object |
| `debug.physics.release()` | Release object |
| `debug.swim.set(on)` | Force water state |
| `debug.checkpoint.set(index)` | Set active checkpoint |
| `debug.switch.set(id, pressed)` | Set switch |
| `debug.door.set(id, open, locked)` | Set door |
| `debug.key.set(n)` | Set keys |
| `debug.pickup.spawn(type, x, y)` | Spawn pickup |
| `debug.pickup.set(id, collected)` | Set pickup collected |
| `debug.creature.spawn(x, y)` | Spawn Tad |
| `debug.creature.rescue(id)` | Rescue Tad |
| `debug.creature.setFlee(id, on)` | Set Tad flee |
| `debug.landmark.set(id, rung)` | Set landmark rung |
| `debug.hint.show(text)` | Show hint |
| `debug.secret.set(id, found)` | Set secret found |
| `debug.boost.set(id, active)` | Set boost |
| `debug.decor.set(id, booped)` | Set decoration booped |
| `debug.medal.set(rank)` | Set medal |
| `debug.effects.shake(mag)` | Trigger shake |
| `debug.effects.hitFlash()` | Trigger hit flash |
| `debug.effects.particles(x, y, color, count)` | Spawn particles |

# 9. TESTS

Tests are high-level code-wise tests. They use debug functions and fixed-step updates.

## Tier 1 tests

| Test | Validates |
| --- | --- |
| T1.01 Title to playing | Screen transition |
| T1.02 Player spawns at level start | Spawn point |
| T1.03 Left/right movement changes x | Movement |
| T1.04 Jump applies vy and gravity returns player to ground | Jump |
| T1.05 Falling below death line triggers death | Falling |
| T1.06 Bounce pad sets vy to -470 px/s | Bounce |
| T1.07 Exit overlap sets win screen | Objective |
| T1.08 HUD score equals score.current | HUD contract |
| T1.09 Retry after death restores start | Failure restart |

## Tier 2 tests

| Test | Validates |
| --- | --- |
| T2.01 Spike overlap kills player | Traps |
| T2.02 Puffer fuse triggers after 0.6 s | Trap timing |
| T2.03 Acid puddle kills instantly | Environmental damage |
| T2.04 Sour mist kills at 0.4 s | Environmental damage |
| T2.05 Pebble falls with gravity | Physics objects |
| T2.06 Player can push pebble | Physics push |
| T2.07 Water zeroes gravity and up swims | Swim |
| T2.08 Enemy contact kills player | Enemies |
| T2.09 Seed defeats enemy | Enemy defeat |
| T2.10 Bounce-bonk defeats enemy | Bounce combat |
| T2.11 Ability gives one air jump | Special move |
| T2.12 Duck changes hitbox height to 8 | Dodge |
| T2.13 Checkpoint snapshot restores score and pickups | Spawn points |
| T2.14 Vine up/down changes y | Climb |
| T2.15 Level 1 locked before Level 0 win, unlocked after | Unlocks |
| T2.16 Level 1 has more hazards than Level 0 | Difficulty ramp |

## Tier 3 tests

| Test | Validates |
| --- | --- |
| T3.01 Landmark press gives +50 once | Landmarks |
| T3.02 Rewards added on win | Rewards |
| T3.03 Decoration boop gives +5 once | Decoration |
| T3.04 Switch opens linked door | Switches/doors |
| T3.05 Timed door closes after 4 s | Switches/doors |
| T3.06 Bounce beacon opens door for 4 s | Puzzle type |
| T3.07 Pebble plate opens door after 0.2 s | Puzzle type |
| T3.08 Secret pickup sets secretFound | Secrets |
| T3.09 Hint press shows text for 3 s | Hints |
| T3.10 Boost pad sets velocity | Boosts |
| T3.11 Collectible adds score | Collectibles |
| T3.12 Throw seed travels 420 px/s for 0.8 s | Throw |
| T3.13 Score persists until death or win | Score |
| T3.14 High score entry saved on win | High scores |

## Tier 4 tests

| Test | Validates |
| --- | --- |
| T4.01 Guard blocks door until defeated | Guards |
| T4.02 Tad flees when player within 64 px | Flee |
| T4.03 Tad can be rescued after flee ends | Collectible creatures |
| T4.04 Key opens locked door and consumes key | Keys/locked doors |
| T4.05 Grab pulls object at 80 px/s | Push/pull |
| T4.06 Squash changes hitbox to 8×8 | Transform |
| T4.07 Combo multiplier reaches max 5 | Combos |
| T4.08 Medal computed from final score and conditions | Medals/ranks |
| T4.07 Full Level 6 clearable with all mechanics | Final progression |

## Tier 5 tests

| Test | Validates |
| --- | --- |
| T5.01 Music plays per screen | Audio |
| T5.02 SFX triggers on events | Audio |
| T5.03 Screen shake disabled with reduced motion | Accessibility |
| T5.04 Particles disabled with reduced motion | Accessibility |
| T5.05 Hit flash disabled with reduced motion | Accessibility |
| T5.06 Key remap changes input mapping | Remappable keys |
| T5.07 Colour-blind aids add outlines/symbols | Colour-blind safety |
| T5.08 Save persists settings/unlocks/high scores | Persistence |

# 10. BUILD ORDER

1. Build core loop: fixed step, canvas, state, input.
2. Implement constants, math, RNG.
3. Implement level loader and tile collision.
4. Implement player movement and jump.
5. Implement falling, death, game over, retry.
6. Implement bounce pads.
7. Implement exit and win screen.
8. Add HUD score.
9. Build Tier 1 tests.
10. Add traps, environmental damage, physics objects.
11. Add swim, enemies, special move, dodge, spawn points, climb.
12. Add difficulty-ramped Levels 1–2.
13. Build Tier 2 tests.
14. Add score, collectibles, throw, decorations, landmarks, hints, secrets, boosts, switches/doors, puzzles.
15. Add high scores, rewards.
16. Add Levels 3–6 content skeleton.
17. Build Tier 3 tests.
18. Add guards, flee, keys/locked doors, push/pull, transform, collectible creatures, combos, medals.
19. Complete Level 6 final.
20. Build Tier 4 tests.
21. Add audio, effects, settings, reduced motion, remapping, colour-blind aids.
22. Build Tier 5 tests and final pass.

# 11. DEFINITION OF DONE

## Tier 1 done

High level: A new browser tab can load, show title, start Level 0, and let a player finish by reaching exit or dying and retrying.

- [ ] Fixed step loop runs at 60 Hz.
- [ ] Title screen exists.
- [ ] Level 0 loads.
- [ ] Player can move left/right.
- [ ] Player can jump with coyote and buffer.
- [ ] Gravity and max fall work.
- [ ] Falling off level kills player.
- [ ] Bounce pad launches player.
- [ ] Exit triggers win screen.
- [ ] Death triggers game over and retry.
- [ ] HUD shows score only.
- [ ] No unsupported mechanics are present.

## Tier 2 done

High level: The player can experience hazards, enemies, water, vines, checkpoints, and level unlocks in Levels 0–2.

- [ ] Traps kill according to rules.
- [ ] Acid kills instantly.
- [ ] Mist kills after 0.4 s.
- [ ] Physics objects fall and can be pushed.
- [ ] Swim works with correct speed and gravity.
- [ ] Enemies patrol and kill on contact.
- [ ] Enemies can be defeated by seed or bounce-bonk.
- [ ] Double jump works once in air.
- [ ] Duck changes hitbox.
- [ ] Checkpoints save and restore snapshots.
- [ ] Climb works on vines.
- [ ] Level 2 unlocks after Level 1 win.
- [ ] Difficulty counts increase from Level 0 to 2.
- [ ] Tier 2 tests pass.

## Tier 3 done

High level: The player can collect, solve, find secrets, and see score/high scores in all level skeletons.

- [ ] Landmarks give score and arrow.
- [ ] Decorations boop once.
- [ ] Switches open doors.
- [ ] Timed doors close after 4 s.
- [ ] Permanent doors stay open.
- [ ] Bounce beacon puzzle works.
- [ ] Pebble plate puzzle works.
- [ ] Secrets collect and set secretFound.
- [ ] Hints show text.
- [ ] Boost pads apply velocity.
- [ ] Collectibles add score.
- [ ] Throw seeds travel and hit.
- [ ] Rewards compute on win.
- [ ] High score entries save.
- [ ] Tier 3 tests pass.

## Tier 4 done

High level: All extra mechanics work and the final level is clearable with rank evaluation.

- [ ] Guards block doors.
- [ ] Tad creatures flee and can be rescued.
- [ ] Keys open locked doors.
- [ ] Push and pull work.
- [ ] Transform squash works.
- [ ] Rescued creatures follow.
- [ ] Combo multiplier works.
- [ ] Medals compute correctly.
- [ ] All 7 levels are present and clearable.
- [ ] Tier 4 tests pass.

## Tier 5 done

High level: The game is presentation-complete and accessible.

- [ ] Music plays for title, play, win, game over.
- [ ] SFX play for listed events.
- [ ] Screen shake works and respects reduced motion.
- [ ] Particles work and respect reduced motion.
- [ ] Hit flash works and respects reduced motion.
- [ ] Settings screen changes volume, reduced motion, colour-blind aids.
- [ ] Key remapping works for all gameplay actions.
- [ ] Save persists.
- [ ] Colour-blind safe palette is used.
- [ ] All required screens exist.
- [ ] HUD contains only score.
- [ ] All tests pass.

# A. SANITY

| Check | Result |
| --- | --- |
| All required headings present | Valid: §0 through §11 and §A present |
| Core mechanics exactly jump, objectives, falling, map/world, bounce | Valid: each has its own rules in §4 |
| Supporting mechanics all present | Valid: traps, environmental damage, physics objects, swim, enemies, difficulty ramp, abilities/special moves, dodge, spawn points, climb, unlocks appear in §4 |
| Extra mechanics all present | Valid: landmarks, dash, rewards, decoration, switches/doors, puzzle types, secrets, hints, boosts, collectibles, throw, score, guards, flee, keys/locked doors, push/pull, transform, collectible creatures, combos, medals/ranks appear in §4 |
| No unlisted gameplay systems added | Valid: no health, lives, crafting, dialogue, shops, stomp, or inventory screen added |
| Screens exactly required list | Valid: title, pause, settings, game over, win, level select, high scores only |
| HUD exactly score | Valid: §7 HUD table has only `#score` |
| Effects exactly screen shake, particles, hit flash | Valid: §4.39 and §11 only use these |
| Accessibility requirements present | Valid: colour-blind safe palette, reduced motion, remappable keys in §3, §7, §11 |
| Art style requirements present | Valid: low-res pixel, visible pixels, saturated palette, pixel font in §3 and §7 |
| Audio requirements present | Valid: chiptune music and synthesized SFX tables in §6 |
| Units and numbers consistent | Valid: constants in §1.1 match rules in §4 |
| Contracts cover fields and functions | Valid: §2.2 fields, §2.3 functions, §8 debug |
| Failure restarts level | Valid: death → game over → retry snapshot |
| Win is reach exit | Valid: §4.7 |
| Real-time fixed step | Valid: §1.2 |
| Side-on camera | Valid: §1.1, §4.4 |
| Silly tone | Valid: names and art in §3, §4, §5, §6 |
| Under 30 minutes | Valid: 7 levels, target 18–28 minutes |
| Fixed an earlier red/green palette idea | Corrected to blue/yellow/magenta/cyan/orange colour-blind-safe palette |
| Fixed an earlier stomp idea | Replaced with seed and bounce-bonk to avoid unlisted stomp mechanic |
| Fixed HUD combo display idea | Removed HUD combo to keep HUD score-only |
