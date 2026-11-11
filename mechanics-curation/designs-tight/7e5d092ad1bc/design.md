# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Browser game | §1, §2, §7, §10 |
| 2D | §1.1, §3, §4, §5 |
| Side-on camera | §1.1, §3, §5 |
| Turn-based time model | §4.1, §4.2, §4.3, §4.4 |
| Grid-based movement model | §1.1, §4.2, §4.3 |
| A sequence of levels | §0.2, §4.1, §4.6, §4.11 |
| Failure is permadeath; start a new run | §4.1, §7, §11 |
| Tone is silly | §0.2, §3, §4, §5, §6, §7 |
| Size is a handful of levels, under 30 minutes | §0.2, §4.6, §4.11, §11 |
| Win by reaching the exit and defeating a final boss | §4.1, §4.6, §4.11, §7, §11 |
| Core mechanic: combat | §4.1, §4.4, §5, §6, §9 |
| Core mechanic: roguelike | §4.1, §7, §9, §11 |
| Core mechanic: cards | §4.1, §4.5, §5, §6, §7, §9 |
| Supporting mechanic: procedural generation | §4.6, §9, §11 |
| Supporting mechanic: progression | §4.7, §4.11, §9, §11 |
| Supporting mechanic: hazards | §4.8, §9, §11 |
| Supporting mechanic: inventory | §4.9, §9, §11 |
| Supporting mechanic: economy | §4.10, §9, §11 |
| Extra mechanics: none | §0.2, §4, §11 |
| Art style: pixel art, low-resolution sprites, visible square pixels, limited palette | §1.1, §3, §5 |
| Palette: saturated | §3 |
| Typography: pixel font, blocky bitmap letters | §3, §7 |
| Music: chiptune | §6 |
| Sound effects: retro bleeps, synthesized chip sounds | §6 |
| Screens: title, pause, settings, game over, win | §7 |
| HUD: health, currency | §7 |
| Effects: screen shake, particles, hit flash | §3, §5, §6, §7 |
| Accessibility: colour-blind safe palette | §3, §7, §11 |
| Accessibility: reduced motion | §1.2, §3, §7, §9, §11 |
| Accessibility: remappable keys | §1.2, §7, §8, §9, §11 |
| Accessibility: difficulty options | §4.11, §7, §9, §11 |
| Player request: “wizard cat climbing a tower” | §0.2, §3, §4, §5, §6, §7 |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| Who the player is | Sir Whiskers, a wizard cat climbing a magical tower. | Makes the premise literal, silly, and pixel-friendly. |
| Final boss | Grand Archmage Dog, Sir Barksworth. | Opposite of cat wizard, comedic, easy silhouette. |
| Level count | Full game: 4 normal levels + 1 boss level. Tier 1 minimal run: 2 normal levels + 1 boss level. | “Handful of levels” and under 30 minutes while preserving a sequence and final boss. |
| Grid size | 24 × 14 tiles. | Fits a fixed side-on screen at 16 px tiles, readable and simple. |
| Tile size | 16 logical pixels. | Low-resolution pixel art, visible square pixels. |
| Logical canvas size | 384 × 224 px, integer-scaled. | 24 × 14 × 16. |
| Camera | Fixed camera per level; no scrolling. | Keeps turn-based grid tactics readable and implementation simple. |
| Gravity | No continuous gravity. Side-on is visual; gameplay is tactical grid movement. | Prevents physics complexity and keeps movement deterministic. |
| Movement | Cardinal only: up, down, left, right. Diagonal movement is not allowed. | Grid-based, testable, side-on tactical. |
| Move points | Player starts with 2 move points per turn. Some cards and blessings can increase movement. | Gives positioning without real-time speed. |
| Energy | Player starts with 3 energy per turn. Energy is separate from move points. | Deckbuilder cost system without overcomplicating actions. |
| Hand | Draw to 5 cards at the start of each player turn. Hand maximum 5, upgradable to 7. | Standard deckbuilder clarity. |
| Deck | Start with exactly 10 cards. New levels reset draw pile to all owned cards shuffled. | Keeps run state clean and deterministic. |
| Card effects | Only direct effects: damage, area damage, self-heal, draw, move/teleport. | Avoids extra systems beyond cards and combat. |
| Status effects | No status effects. Damage bonuses and temporary energy bonuses are run upgrades/items, not combat statuses. | Keeps combat as “attacks deal damage until one side is defeated.” |
| Enemy factions | One enemy faction only. No allies. | “Player’s side” is the player plus cards/items. |
| Enemy AI | If the player is in range and line of sight, attack. Otherwise move toward an attackable position and attack if possible. | Deterministic, testable, tactical. |
| Line of sight | 8-direction Bresenham line between tile centers. Walls block. Adjacent melee attacks do not need LOS. | Simple and testable. |
| Targeting | Cards use an aim cursor. Keyboard: arrow keys to move cursor, Enter to confirm, Esc to cancel. Mouse: click card, click target. | Supports keyboard-first and mouse fallback. |
| Remappable keys | All named input actions are remappable in Settings. | Required accessibility. |
| RNG | One seeded Mulberry32 RNG. No `Math.random()` in gameplay. | Reproducible tests and procedural generation. |
| Procedural generation | Tier 2 adds full generated levels. Tier 1 uses fixed templates with seeded random spawn choices only. | Core roguelike must be different enough without making procedural generation a tier 1 dependency. |
| Currency in Tier 1 | `state.run.gold` exists and the HUD shows it, but it remains `0` in Tier 1. Earning and spending are Tier 2 economy. | Required HUD without making economy a core dependency. |
| Economy | Full economy appears in Tier 2: kill drops, coin pickups, shop, item purchases, card purchases. | Supports progression without being required for core combat. |
| Inventory | Exactly 3 inventory slots. Items do not stack. | Concrete limit. |
| Items | Exactly 3 item types: healing, energy, area damage. | Small, complete, no extra systems. |
| Hazards | Exactly 3 hazard types: spike rug, cursed candle, shock wire. Hazards damage the player when the player enters the tile. | Concrete, fixed-in-place dangers. |
| Progression | After each normal level, the player chooses one blessing from three random choices. Blessings affect HP, energy, draw, movement, card damage, or deck contents. | “Progression” without meta-progression or extra systems. |
| Difficulty | Three options: Easy, Normal, Hard. They scale player HP, enemy HP, enemy damage, and gold. | Required accessibility option. |
| Colour-blind safe palette | Always on. Uses saturated magenta, cyan, orange, yellow, blue, white, black, and pattern overlays. | Required accessibility. |
| Reduced motion | Setting disables screen shake and particles. Hit flash is reduced to a single-frame white outline. | Required accessibility. |
| Screens | Title, Pause, Settings, Game Over, Win. The live game is a state, not a “screen.” | Matches requested screen list while allowing game state. |
| UI implementation | Screens and HUD are HTML/CSS DOM overlays. JavaScript toggles classes and text. | Required UX constraint. |
| Audio | WebAudio synthesized chiptune. No audio files. | Retro bleeps and builder API assumption. |
| Extra systems | None. | Explicit final decision. |

## 0.3 Tiers

Tier 1 is the core game. It must be finished, tuned, and playable as a minimal run. Tier 2 adds supporting mechanics on top of a working Tier 1. There is no Tier 3 because extra mechanics are none.

| Tier | Segment | Required result |
| --- | --- | --- |
| Tier 1 | T1.1 Run and level sequence | Title starts a run. Minimal run has 3 levels: Level 1, Level 2, Boss. Permadeath. Win screen after boss and exit. Game Over screen on death. |
| Tier 1 | T1.2 Grid movement and turns | Fixed 24 × 14 grid. Cardinal movement. Move points. Wall and entity blocking. End turn. Enemy turns. |
| Tier 1 | T1.3 Combat | Player cards damage enemies. Enemies damage player. Death removes entities. Player death ends run. Boss death unlocks exit. |
| Tier 1 | T1.4 Cards | 10-card start deck. Draw pile, hand, discard, reshuffle, energy, card play, card effects. |
| Tier 1 | T1.5 Required presentation | Pixel art, saturated palette, pixel font, HUD health and currency, title/pause/settings/game over/win, chiptune, bleeps, screen shake, particles, hit flash. |
| Tier 2 | T2.1 Procedural generation | Replace fixed templates with generated 5-level run. Guaranteed start-to-exit path. |
| Tier 2 | T2.2 Hazards | Add spike rug, cursed candle, shock wire. Player takes damage on entering hazard tiles. |
| Tier 2 | T2.3 Economy | Gold drops, coin pickups, level completion gold, shop offers, buying cards/items. |
| Tier 2 | T2.4 Inventory | 3 inventory slots, item pickups, item use. |
| Tier 2 | T2.5 Progression | Level-end blessing choices, applying upgrades, deck growth. |
| Tier 3 | None | Not applicable. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Name | Value | Meaning |
| --- | ---: | --- |
| `TILE_SIZE` | 16 | Logical pixels per tile. |
| `GRID_W` | 24 | Grid width in tiles. |
| `GRID_H` | 14 | Grid height in tiles. |
| `LOGICAL_W` | 384 | `GRID_W * TILE_SIZE`. |
| `LOGICAL_H` | 224 | `GRID_H * TILE_SIZE`. |
| `CANVAS_SCALE` | integer 2–4 | Integer scale applied to canvas. |
| `X_AXIS` | 0 to 23 | Left to right. |
| `Y_AXIS` | 0 to 13 | Top to bottom. |
| `MOVE_POINT` | 1 | One cardinal tile move. |
| `ENERGY` | 1 | One card cost unit. |
| `HP` | integer | Damage and health units. |
| `GOLD` | integer | Mana Coins. |
| `RANGE` | tile count | Chebyshev distance unless stated otherwise. |
| `RADIUS` | tile count | Chebyshev radius. |
| `FIXED_LOGIC_STEP` | none | Turn-based logic is event-driven. |
| `RENDER_FPS` | 60 | RequestAnimationFrame render target. |
| `ANIMATION_FPS` | 8 | Sprite animation target. |
| `HIT_FLASH_MS` | 80 | White hit flash duration. |
| `SCREEN_SHAKE_MS` | 120 | Default shake duration. |
| `SCREEN_SHAKE_PX` | 4 | Default shake magnitude. |
| `INPUT_INITIAL_DELAY_MS` | 150 | Key hold delay. |
| `INPUT_REPEAT_MS` | 50 | Key hold repeat. |
| `SEED` | uint32 | RNG seed. |

## 1.2 Important conventions

| Convention | Rule |
| --- | --- |
| RNG | Use `rng.nextUint32()`, `rng.nextFloat()`, `rng.nextInt(min, maxExclusive)`, `rng.shuffle(array)`. No `Math.random()` in gameplay. |
| Determinism | Same seed plus same inputs produces same state transitions. |
| Coordinates | All gameplay coordinates are integer tile coordinates. |
| No gravity | Entities stay where placed unless moved by player, AI, or card. |
| Side-on | Visuals use side-on tower art. Gameplay grid is a tactical map. |
| Fixed camera | Each level is one screen. No camera scrolling. |
| Integer damage | All damage, healing, and costs are integers. |
| Death | When `hp <= 0`, set `alive = false`, remove from active movement/attacks, play death animation for 500 ms, then remove from level. |
| Player death | Immediate Game Over. No revival. |
| Level start | At each level start, `drawPile = shuffle(allCards)`, `hand = []`, `discard = []`, then draw to hand maximum. |
| Deck persistence | `allCards` persists for the run. New levels reshuffle from `allCards`. |
| Accessibility | `reducedMotion` disables screen shake and particles. Key remapping must not break game logic. Difficulty multipliers are applied at spawn or run start. |
| Tests | Tests must set a fixed seed and call public module functions. Tests must not depend on visual canvas pixels. |
| No extra systems | Do not add crafting, quests, XP, meta unlocks, stealth, crafting tables, companion systems, or save slots. |

# 2. CONTRACTS

## 2.1 Module layout

```text
index.html
style.css
src/
  main.js
  state.js
  settings.js
  input.js
  rng.js
  level.js
  levelgen.js
  entities.js
  combat.js
  ai.js
  cards.js
  items.js
  inventory.js
  economy.js
  progression.js
  hazards.js
  render.js
  fx.js
  audio.js
  ui.js
  debug.js
assets/
  fonts/
    pixel-font.woff2
```

## 2.2 Global context

The global context object is `window.GAME`.

```ts
interface GameContext {
  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  settings: Settings;
  input: InputState;
  rng: RNG;
  audio: AudioAPI;
  fx: FXState;
  state: GameState;
  debug: DebugAPI;
}

interface Settings {
  difficulty: "easy" | "normal" | "hard";
  reducedMotion: boolean;
  colorSafe: true;
  masterVolume: number; // 0..1
  musicVolume: number; // 0..1
  sfxVolume: number; // 0..1
  keyMap: Record<InputAction, string>;
}

interface InputState {
  pressed: Record<InputAction, boolean>;
  justPressed: Record<InputAction, boolean>;
  targetMode: boolean;
}

type InputAction =
  | "move_up"
  | "move_down"
  | "move_left"
  | "move_right"
  | "aim_up"
  | "aim_down"
  | "aim_left"
  | "aim_right"
  | "card_1"
  | "card_2"
  | "card_3"
  | "card_4"
  | "card_5"
  | "item_1"
  | "item_2"
  | "item_3"
  | "interact"
  | "end_turn"
  | "confirm"
  | "cancel"
  | "pause"
  | "restart";

interface RNG {
  seed: number;
  nextUint32(): number;
  nextFloat(): number;
  nextInt(min: number, maxExclusive: number): number;
  shuffle<T>(arr: T[]): T[];
  fork(label: string): RNG;
}

interface GameState {
  ui: UIState;
  run: RunState;
  level: LevelState;
  entities: Entity[];
  player: PlayerState | null;
  turn: TurnState;
  cards: CardState;
  inventory: InventoryState;
  economy: EconomyState;
  progression: ProgressionState;
  hazards: HazardState;
  fx: FXState;
  audio: AudioState;
}

interface UIState {
  screen: "title" | "settings" | "pause" | "game" | "game_over" | "win";
  overlay: "none" | "blessing" | "shop" | "inventory" | "level_complete";
  shopOffers: ShopOffer[];
  blessingChoices: BlessingId[];
  message: string;
  messageTimer: number;
}

interface RunState {
  seed: number;
  levelIndex: number;
  allCards: CardId[];
  gold: number;
  maxHp: number;
  maxEnergy: number;
  handMax: number;
  maxMovePoints: number;
  damageBonus: number;
  nextTurnEnergyBonus: number;
  blessingsApplied: BlessingId[];
}

interface LevelState {
  index: number;
  seed: number;
  width: number;
  height: number;
  grid: TileType[][];
  start: Point;
  exit: Point;
  exitLocked: boolean;
  complete: boolean;
  shops: Point[];
  pickups: Pickup[];
}

interface Entity {
  id: string;
  kind: string;
  faction: "player" | "enemy";
  x: number;
  y: number;
  hp: number;
  maxHp: number;
  damage: number;
  movePoints: number;
  maxMovePoints: number;
  attackRange: number;
  ai: "none" | "melee" | "ranged" | "boss";
  alive: boolean;
  facing: "left" | "right";
  animation: string;
  hitFlash: number;
  deathTimer: number;
}

interface PlayerState extends Entity {
  kind: "wizard_cat";
  energy: number;
  maxEnergy: number;
  handMax: number;
  nextTurnEnergyBonus: number;
  damageBonus: number;
}

interface TurnState {
  number: number;
  phase: "player_start" | "player_active" | "player_end" | "enemy_active" | "level_complete";
  movePoints: number;
  maxMovePoints: number;
  energy: number;
  maxEnergy: number;
  targeting: boolean;
  selectedCardIndex: number | null;
  aimCursor: Point;
}

interface CardState {
  drawPile: CardInstance[];
  hand: CardInstance[];
  discard: CardInstance[];
}

interface CardInstance {
  instanceId: string;
  cardId: CardId;
}

interface InventoryState {
  slots: (ItemInstance | null)[]; // length 3
}

interface ItemInstance {
  instanceId: string;
  itemId: ItemId;
}

interface EconomyState {
  gold: number;
  shopOffers: ShopOffer[];
  activeShopPoint: Point | null;
}

interface ProgressionState {
  blessingChoices: BlessingId[];
  pendingBlessing: boolean;
}

interface HazardState {
  hazardById: Record<string, Hazard>;
}

interface FXState {
  shake: { x: number; y: number; time: number; magnitude: number };
  particles: Particle[];
  hitFlashes: HitFlash[];
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
  color: string;
  size: number;
}

interface HitFlash {
  entityId: string;
  time: number;
}

interface AudioState {
  currentMusic: string | null;
}

type TileType =
  | "wall"
  | "floor"
  | "exit"
  | "exit_locked"
  | "shop"
  | "coin"
  | "item"
  | "hazard_spikes"
  | "hazard_candle"
  | "hazard_shock";

interface Point {
  x: number;
  y: number;
}

interface Pickup {
  id: string;
  kind: "coin" | "item";
  itemId?: ItemId;
  value?: number;
  x: number;
  y: number;
}

interface Hazard {
  id: string;
  type: "spikes" | "candle" | "shock";
  x: number;
  y: number;
  damage: number;
}
```

## 2.3 Module specifics

| Module | Required exports | Purpose | Test hooks |
| --- | --- | --- | --- |
| `state.js` | `createSettings`, `newRun`, `startLevel`, `endTurn`, `gameOver`, `winRun`, `getPhase` | Owns run and turn state. | `newRun(seed, difficulty)`, `getPhase()`. |
| `settings.js` | `loadSettings`, `saveSettings`, `setDifficulty`, `setReducedMotion`, `setKeyMap` | Settings persistence. | `setKeyMap`, `setDifficulty`. |
| `input.js` | `initInput`, `handleKeyDown`, `handleKeyUp`, `isJustPressed`, `remapAction`, `getBindings` | Maps keys to named actions. | `remapAction`, `isJustPressed`. |
| `rng.js` | `createRNG`, `hashSeed` | Mulberry32 RNG. | `createRNG(seed)`. |
| `level.js` | `isWalkable`, `isOccupied`, `canStandAt`, `hasLOS`, `chebDistance`, `bfsPath` | Grid rules. | `hasLOS`, `bfsPath`. |
| `levelgen.js` | `generateLevel`, `ensurePath` | Tier 2 procedural generation. | `generateLevel(index, seed)`. |
| `entities.js` | `spawnEntity`, `damageEntity`, `killEntity`, `moveEntity`, `getEntity` | Entity mutation. | `damageEntity`, `moveEntity`. |
| `combat.js` | `canAttack`, `resolveAttack`, `enemyTakeTurn`, `endTurnCombat` | Combat resolution. | `resolveAttack`, `enemyTakeTurn`. |
| `ai.js` | `chooseEnemyAction`, `findAttackableTile` | Enemy AI. | `chooseEnemyAction`. |
| `cards.js` | `shuffleDeck`, `drawCards`, `canPlayCard`, `playCard`, `validCardTarget` | Card system. | `playCard`, `drawCards`. |
| `items.js` | `useItem`, `itemEffect` | Item effects. | `useItem`. |
| `inventory.js` | `addItem`, `removeItem`, `canAddItem`, `canUseItem` | Inventory limit. | `addItem`. |
| `economy.js` | `addGold`, `spendGold`, `rollEnemyDrop`, `generateShopOffers`, `buyShopOffer` | Currency and shop. | `addGold`, `spendGold`, `rollEnemyDrop`. |
| `progression.js` | `generateBlessingChoices`, `applyBlessing` | Run progression. | `applyBlessing`. |
| `hazards.js` | `triggerHazardAt`, `applyHazardDamage` | Hazard damage. | `triggerHazardAt`. |
| `render.js` | `renderFrame`, `drawWorld`, `drawSprites`, `drawFX` | Canvas drawing. | `renderFrame` smoke test. |
| `fx.js` | `screenShake`, `spawnParticles`, `hitFlash`, `updateFX` | Effects. | `screenShake`, `hitFlash`. |
| `audio.js` | `playSFX`, `startMusic`, `stopMusic`, `setVolume` | Synthesized audio. | `playSFX`, `startMusic`. |
| `ui.js` | `showScreen`, `updateHUD`, `openShop`, `closeShop`, `openInventory`, `closeInventory`, `showBlessing`, `closeBlessing` | DOM screens and HUD. | `showScreen`, `updateHUD`. |
| `debug.js` | All debug functions in §8 | Direct state access. | All. |

# 3. VISUAL SPEC

The game is a saturated low-resolution pixel tower climb. Sir Whiskers is a small cyan-furred wizard cat with a purple robe, yellow hat, and a glowing paw. The tower rooms are dark blue-grey brick platforms with bright neon hazards, glowing exits, and silly enemies. Everything is drawn on a 16 px tile grid with visible square pixels. The side-on view looks like a platformer, but movement is turn-based grid tactics. UI is chunky, blocky, and readable with patterns as well as colour.

## Lighting and atmosphere

| Element | Rule |
| --- | --- |
| Base lighting | Static. No dynamic light sources. |
| Atmosphere | Deep night tower. Background bricks are dark. Foreground tiles have strong outlines. |
| Glow | Exit, candles, shock wires, and magic cards use additive glow sprites. |
| Shadows | None. Use outlines and patterns instead. |
| Hit feedback | Entity flashes white for 80 ms. |
| Reduced motion | No additive glow animation except static glow. No particles. No shake. |

## Space

| Element | Rule |
| --- | --- |
| Camera | Fixed per level. No scrolling. |
| Grid visibility | Subtle 1 px dark outline on walkable tiles only when targeting or moving. |
| Background | 2 static parallax layers: distant tower bricks and moonlit windows. Disabled if reduced motion is on. |
| Foreground | Tiles, entities, particles, UI overlays. |
| UI | DOM overlay above canvas. |

## Palette

All colours are hex. The palette is always colour-blind safe. Hue is never the only signal; patterns and symbols are required.

| Name | Hex | Use | Pattern / symbol |
| --- | --- | --- | --- |
| `bg_deep` | `#101820` | Background | None |
| `bg_mid` | `#1b2a36` | Background bricks | Brick lines |
| `wall` | `#3b4b5a` | Walls | Brick outline |
| `floor` | `#26323c` | Walkable | Dot pattern |
| `outline` | `#000000` | Sprites | 1 px outline |
| `white` | `#f8f8ff` | Text, highlights | None |
| `black` | `#000000` | Text outline | None |
| `cat_fur` | `#00f5d4` | Player fur | Cyan outline |
| `cat_robe` | `#7209b7` | Player robe | Star pattern |
| `cat_hat` | `#ffd23f` | Player hat | None |
| `exit` | `#ffd23f` | Exit | Door glyph |
| `exit_locked` | `#8d99ae` | Locked exit | Cross glyph |
| `hazard_spikes` | `#b5179e` | Spike rug | Diagonal hatch |
| `hazard_candle` | `#ff9f1c` | Candle | Flame glyph |
| `hazard_shock` | `#00bbf9` | Shock wire | Zigzag glyph |
| `coin` | `#ffd166` | Currency pickup | Coin glyph |
| `item` | `#4cc9f0` | Item pickup | Box glyph |
| `shop` | `#f15bb5` | Shop | Bag glyph |
| `enemy_a` | `#ff9f1c` | Crow | Gear pattern |
| `enemy_b` | `#ffd166` | Mouse Mage | Star pattern |
| `enemy_c` | `#f15bb5` | Imp | Flame pattern |
| `enemy_d` | `#00bbf9` | Wraith | Book pattern |
| `enemy_e` | `#9d0208` | Golem | Broom pattern |
| `boss` | `#b5179e` | Boss | Crown pattern |
| `hp_player` | `#00f5d4` | Player HP bar | Heart glyph |
| `hp_enemy` | `#ff9f1c` | Enemy HP bar | Skull glyph |
| `energy` | `#ffd23f` | Energy pips | Bolt glyph |

## Visual recipe table

| Element | Sprite size | Base colours | Animation | Rule implication |
| --- | ---: | --- | --- | --- |
| Wizard cat | 16 × 16 | `cat_fur`, `cat_robe`, `cat_hat` | Idle bob, walk, cast, hit, death | Player entity. Facing left/right. |
| Exit door | 16 × 16 | `exit`, `white` | 4-frame glow pulse | Active exit. Reaching it ends level. |
| Locked exit | 16 × 16 | `exit_locked`, `black` | None | Boss level exit until boss dies. |
| Wall | 16 × 16 | `wall`, `outline` | None | Blocks movement and LOS. |
| Floor | 16 × 16 | `floor`, `outline` | None | Walkable. |
| Spike rug | 16 × 16 | `hazard_spikes`, `white` | 2-frame shimmer | Damages player 5 on entry. |
| Cursed candle | 16 × 16 | `hazard_candle`, `white` | 4-frame flame | Damages player 4 on entry. |
| Shock wire | 16 × 16 | `hazard_shock`, `white` | 3-frame zap | Damages player 3 on entry. |
| Coin pickup | 16 × 16 | `coin`, `black` | 4-frame spin | Adds 5 gold. Removed on pickup. |
| Item pickup | 16 × 16 | `item`, `white` | 3-frame bob | Adds item if inventory has space. |
| Shop tile | 16 × 16 | `shop`, `white` | None | Standing on it and pressing interact opens shop. |
| Clockwork Crow | 16 × 16 | `enemy_a`, `white` | Idle, walk, hit, death | Melee enemy. |
| Mouse Mage | 16 × 16 | `enemy_b`, `white` | Idle, walk, hit, death | Melee enemy. |
| Candle Imp | 16 × 16 | `enemy_c`, `white` | Idle, walk, hit, death | Melee enemy. |
| Book Wraith | 16 × 16 | `enemy_d`, `white` | Float, hit, death | Ranged enemy. |
| Broom Golem | 16 × 16 | `enemy_e`, `white` | Stomp, hit, death | Melee tank. |
| Archmage Dog | 32 × 32 | `boss`, `white` | Idle, cast, hit, phase2, death | Boss. Phase 2 changes palette to `hazard_spikes` highlights. |
| Aim cursor | 16 × 16 | `white`, `cat_fur` | Blink | Shows card target. |
| Target highlight | 16 × 16 | `exit` outline | Blink | Valid target. |
| Invalid highlight | 16 × 16 | `black`, `white` | None | Invalid target. |
| HUD health | 80 × 10 | `hp_player`, `black` | None | Shows player HP. |
| HUD currency | 16 × 16 | `coin` | None | Shows gold. |

# 4. GAMEPLAY SPEC

A run begins as Sir Whiskers on the bottom floor of a silly tower. Each level is a single side-on grid room with walls, enemies, optional hazards, optional coins, optional shop tiles, and an exit. On the player’s turn, Sir Whiskers can move using move points and play cards using energy. Cards target enemies, the player, or tiles. Ending the turn lets enemies act. If the player reaches an active exit, the next level starts. If the player dies, the run ends permanently. The final level contains Grand Archmage Dog. Defeating the boss unlocks the exit, and reaching it wins.

## Records

### Entity roster

| Entity ID | Name | Tier | HP | Damage | Move points | Attack range | AI | Gold drop | Item drop chance |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| `wizard_cat` | Sir Whiskers | 1 | 30 base | 0 | 2 base | 0 | none | 0 | none |
| `clockwork_crow` | Clockwork Crow | 1 | 6 | 2 | 2 | 1 | melee | 3 | 0.05 |
| `mouse_mage` | Mouse Mage | 1 | 10 | 3 | 1 | 1 | melee | 4 | 0.08 |
| `candle_imp` | Candle Imp | 2 | 8 | 4 | 1 | 1 | melee | 5 | 0.10 |
| `book_wraith` | Book Wraith | 2 | 12 | 3 | 1 | 4 | ranged | 6 | 0.12 |
| `broom_golem` | Broom Golem | 2 | 22 | 6 | 1 | 1 | melee | 10 | 0.20 |
| `archmage_dog` | Grand Archmage Dog | 1 | 90 | 8 | 2 | 2 | boss | 50 | none |

### Card roster

| Card ID | Name | Cost | Type | Target | Range / radius | Effect | Start deck count | Shop price |
| --- | --- | ---: | --- | --- | ---: | --- | ---: | ---: |
| `paw_swipe` | Paw Swipe | 1 | attack | enemy | range 4 | Deal 3 damage. | 4 | 10 |
| `flick` | Flick | 1 | move | empty tile | range 2 | Teleport to tile. | 2 | 10 |
| `nap` | Nap | 1 | heal | self | 0 | Heal 5. | 2 | 10 |
| `focus` | Focus | 0 | draw | self | 0 | Draw 1 card. | 2 | 10 |
| `static_swipe` | Static Swipe | 1 | attack | enemy | range 3 | Deal 4 damage. | 0 | 12 |
| `claw_barrage` | Claw Barrage | 2 | attack | enemy | range 5 | Deal 7 damage. | 0 | 18 |
| `fireball` | Fireball | 3 | aoe | tile | range 5, radius 1 | Deal 6 damage to all enemies in radius. | 0 | 25 |
| `blink` | Blink | 1 | move | empty tile | range 5 | Teleport to tile. | 0 | 14 |
| `healing_purr` | Healing Purr | 2 | heal | self | 0 | Heal 12. | 0 | 16 |
| `mana_chime` | Mana Chime | 1 | draw | self | 0 | Draw 2 cards. | 0 | 14 |

### Item roster

| Item ID | Name | Price | Drop chance | Effect |
| --- | --- | ---: | ---: | --- |
| `yarn_potion` | Yarn Potion | 8 | 0.10 | Heal 12. |
| `tuna_can` | Tuna Can | 10 | 0.05 | At the start of the next player turn, gain +2 energy, capped by total turn energy 5. |
| `catnip_bomb` | Catnip Bomb | 12 | 0.05 | Deal 6 damage to all enemies within radius 2 of the player. |

### Hazard roster

| Hazard ID | Name | Damage | Appearance | Tier |
| --- | --- | ---: | --- | ---: |
| `hazard_spikes` | Spike Rug | 5 | Magenta diagonal hatch | 2 |
| `hazard_candle` | Cursed Candle | 4 | Orange flame glyph | 2 |
| `hazard_shock` | Shock Wire | 3 | Cyan zigzag glyph | 2 |

### Level roster

Full game is Tier 2. Tier 1 minimal run is marked separately.

| Level | Tier | Name | Size | Start | Exit | Enemies | Hazards | Coins | Items | Shop | Exit locked |
| ---: | ---: | --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| 1 | 1 | Lobby of Mildly Annoying Mice | 24 × 14 | `(2,12)` | `(21,1)` | 2 `mouse_mage` | 0 | 0 | 0 | 0 | no |
| 2 | 1 | Creaking Gear Landing | 24 × 14 | `(2,12)` | `(21,1)` | 1 `clockwork_crow`, 1 `mouse_mage` | 0 | 0 | 0 | 0 | no |
| 3 | 1 | Boss Floor | 24 × 14 | `(2,12)` | `(21,1)` | 1 `archmage_dog` | 0 | 0 | 0 | 0 | until boss dead |
| 1 | 2 | Lobby of Mildly Annoying Mice | 24 × 14 | `(2,12)` | `(21,1)` | 3 `mouse_mage` | 0 | 2 | 0 | 0 | no |
| 2 | 2 | Squeaky Shop Stair | 24 × 14 | `(2,12)` | `(21,1)` | 2 `clockwork_crow`, 2 `mouse_mage` | 3 spikes | 3 | 1 | 1 | no |
| 3 | 2 | Candle-Cluttered Library | 24 × 14 | `(2,12)` | `(21,1)` | 2 `clockwork_crow`, 2 `mouse_mage`, 1 `candle_imp` | 3 spikes, 2 candles | 4 | 1 | 1 | no |
| 4 | 2 | Broom Closet Gauntlet | 24 × 14 | `(2,12)` | `(21,1)` | 2 `book_wraith`, 2 `broom_golem`, 2 `clockwork_crow` | 2 spikes, 3 candles, 2 shock | 5 | 2 | 0 | no |
| 5 | 2 | Boss Floor | 24 × 14 | `(2,12)` | `(21,1)` | 1 `archmage_dog` | 0 | 0 | 0 | 0 | until boss dead |

## 4.1 Roguelike

Tier: 1.

| Rule | Number / detail |
| --- | --- |
| Run start | Player presses New Run on title. If no seed is supplied, generate `seed = (Date.now() ^ cryptoRandom) >>> 0`. |
| Seed persistence | The run seed is stored in `state.run.seed`. |
| Level seed | `levelSeed = hashSeed(runSeed, levelIndex)`. |
| Run sequence | Tier 1: Level 1 → Level 2 → Boss. Full: Level 1 → Level 2 → Level 3 → Level 4 → Boss. |
| Permadeath | If `player.hp <= 0`, set `state.ui.screen = "game_over"`. No continue. |
| Restart | Game Over has “Try Again” and “Title”. Try Again starts a new run with a new seed. |
| Different each time | Tier 1: seeded random enemy spawn choices and boss phase timing. Full: procedural generation. |
| Win condition | On boss level, after boss death, unlock exit. Reaching unlocked exit sets `state.ui.screen = "win"`. |
| Run state reset | New run resets `gold`, `allCards`, `blessingsApplied`, `levelIndex`, `inventory`, `progression`. |

## 4.2 Grid movement

Tier: 1.

| Rule | Number / detail |
| --- | --- |
| Grid | 24 × 14. Border tiles are walls. |
| Movement | Cardinal only: up, down, left, right. |
| Move points | Player starts with 2. Blessings can raise to 3 or 4. |
| Move cost | 1 move point per tile. |
| Blocking | Cannot move into wall, occupied entity, locked exit, or out of bounds. |
| Walkable | `floor`, `exit`, `shop`, `coin`, `item`, all hazard tiles. |
| Pickups | Moving onto `coin` adds 5 gold and removes tile. Moving onto `item` adds item if inventory has space. |
| Hazards | Tier 2: moving onto hazard tile applies hazard damage immediately. |
| Shop | Tier 2: moving onto shop tile does not open automatically. Player must press interact while standing on shop. |
| Exit | Moving onto active exit completes the level. |
| Teleport cards | Destination must be within card range, walkable, unoccupied, and have LOS from player. |
| Facing | Facing changes to the last horizontal movement direction. If no horizontal direction, keep previous facing. |

## 4.3 Turn system

Tier: 1.

| Phase | Rules |
| --- | --- |
| `player_start` | Draw to `handMax`. Set `turn.energy = min(player.maxEnergy + player.nextTurnEnergyBonus, 5)`. Set `turn.movePoints = player.maxMovePoints`. Reset `player.nextTurnEnergyBonus = 0`. |
| `player_active` | Player may move, play cards, use items, interact, or end turn in any order. |
| `player_end` | Player presses end turn. Set phase `enemy_active`. |
| `enemy_active` | Enemies act in spawn order. After all alive enemies act, set phase `player_start`. |
| `level_complete` | Triggered when player enters active exit. Play level complete sound, show temporary overlay, then advance level. |
| Turn number | Starts at 1 for each level. |
| Input lock | During enemy phase, player input is ignored. |
| Pause | Pause freezes all timers and animations. |

## 4.4 Combat

Tier: 1.

| Rule | Number / detail |
| --- | --- |
| Player attacks | Only through cards or items. No player melee move. |
| Card targeting | Enemy must be alive, within card range, and have LOS unless range is 0 self-target. |
| AoE targeting | Target tile must be within range and not a wall. Effect hits all enemies with Chebyshev distance <= radius from target tile. Walls do not block AoE effect. |
| Damage | `finalDamage = card.damage + player.damageBonus`. Items do not use `damageBonus`. |
| Enemy attack condition | If player is alive and within `enemy.attackRange`, and if `attackRange > 1`, LOS is required. |
| Enemy AI | If can attack, attack. Else BFS toward the nearest tile from which the enemy can attack the player, moving up to `enemy.movePoints`. After moving, attack if possible. |
| BFS | 4-direction, treats walls and other entities as blocked. |
| Enemy damage | `finalDamage = enemy.damage * settings.difficulty.enemyDamageMul`, rounded down. |
| Death | If `hp <= 0`, set `alive = false`, `deathTimer = 500`, remove from active entity list after animation. |
| Player death | If `player.hp <= 0`, immediately `game_over`. |
| Boss death | Set `level.exitLocked = false`. Replace `exit_locked` tile with `exit`. |
| Level completion | Does not require all enemies dead on normal levels. Boss level requires boss dead because exit is locked. |
| Combat feedback | On damage: hit flash, screen shake, particles, bleep. |

## 4.5 Cards

Tier: 1.

| Rule | Number / detail |
| --- | --- |
| Start deck | Exactly: 4 `paw_swipe`, 2 `flick`, 2 `nap`, 2 `focus`. |
| Deck storage | `run.allCards` contains card IDs. At level start, `drawPile = shuffle(allCards)`. |
| Draw pile | List of `CardInstance`. |
| Hand | Max 5 by default. Blessing can raise to 6 or 7. |
| Draw | At `player_start`, draw until `hand.length == handMax`. If `drawPile` empty, shuffle `discard` into `drawPile`. If both empty, stop. |
| Card selection | Press `card_1` through `card_5`. If hand has more than 5 cards, keys 1-5 select first five. Additional cards can be selected with mouse click. Keyboard-only fallback: pressing card_5 repeatedly cycles if hand > 5. |
| Targeting | Selecting a card enters `targeting = true`. Aim cursor starts at nearest valid target if any, otherwise at player. |
| Confirm | Press confirm. If target valid, play card. |
| Cancel | Press cancel. Exit targeting. |
| Cost | Subtract `card.cost` from `turn.energy`. |
| Discard | Played card moves to `discard`. |
| Focus | Cost 0, draw 1. Cannot draw beyond hand max. |
| Mana Chime | Cost 1, draw 2. Cannot draw beyond hand max. |
| Nap | Cost 1, heal 5. Healing is capped at `player.maxHp`. |
| Healing Purr | Cost 2, heal 12. Healing is capped at `player.maxHp`. |
| Flick | Cost 1, teleport to empty tile within range 2. |
| Blink | Cost 1, teleport to empty tile within range 5. |
| Paw Swipe | Cost 1, deal 3 + `damageBonus` to target enemy within range 4. |
| Static Swipe | Cost 1, deal 4 + `damageBonus` to target enemy within range 3. |
| Claw Barrage | Cost 2, deal 7 + `damageBonus` to target enemy within range 5. |
| Fireball | Cost 3, target tile within range 5, deal 6 + `damageBonus` to all enemies within radius 1. |
| End turn hand | Hand persists across turns within a level. At level end, hand and discard are cleared and all cards reshuffled. |

## 4.6 Procedural generation

Tier: 2.

| Rule | Number / detail |
| --- | --- |
| Replaces templates | Tier 2 replaces fixed layouts for levels 1-4. Boss level uses fixed layout with random obstacle count 0. |
| Grid | 24 × 14. Border walls. |
| Initial | All interior tiles `floor`. |
| Guaranteed path | Carve a staircase from start to exit using only right and up moves. Path width 1. |
| Obstacles | Add rectangular wall blocks: Level 1: 0, Level 2: 2, Level 3: 3, Level 4: 4. Each block is 3 × 2. Blocks cannot intersect path, start, exit, or border. Retry up to 20 times per block. If impossible, reduce block count by 1. |
| Reachability | Flood fill from start through walkable tiles. Exit must be reachable. If not, regenerate. |
| Enemies | Spawn from level table on reachable tiles not on path, not start, not exit, and at least 4 tiles from start. If not enough positions, allow path tiles except exit. |
| Hazards | Spawn on reachable tiles not on path, not start, not exit, not occupied. |
| Coins | Spawn on reachable tiles not on path, not start, not exit, not occupied. |
| Items | Spawn on reachable tiles not on path, not start, not exit, not occupied. |
| Shop | Spawn on reachable tile not on path if level table has shop. |
| Determinism | Use `levelSeed`. Same seed and level index produces same layout. |
| Path guarantee test | BFS from start to exit must succeed. |

## 4.7 Progression

Tier: 2.

| Rule | Number / detail |
| --- | --- |
| Blessing trigger | After completing any normal level, set `progression.pendingBlessing = true`. |
| Choices | Generate exactly 3 unique blessing IDs from pool. |
| Selection | Player selects with keys 1, 2, 3. |
| Apply | Modify run state immediately. |
| Level advance | After blessing applied, start next level. |
| Cap rules | `maxEnergy` cap 5. `handMax` cap 7. `maxMovePoints` cap 4. `damageBonus` cap 5. `maxHp` has no cap. |

### Blessing pool

| Blessing ID | Name | Effect |
| --- | --- | --- |
| `max_energy_plus` | Extra Spark | `maxEnergy += 1`, cap 5. |
| `vitality` | Catnip Vitality | `maxHp += 8`, heal to max. |
| `extra_draw` | Sharp Eyes | `handMax += 1`, cap 7. |
| `arcane_card` | Found Spell | Add one random card from shop card pool to `allCards`. |
| `enhanced_paws` | Sharper Claws | `damageBonus += 1`, cap 5. |
| `swift_paws` | Silent Paws | `maxMovePoints += 1`, cap 4. |

## 4.8 Hazards

Tier: 2.

| Rule | Number / detail |
| --- | --- |
| Placement | Fixed in level grid. |
| Trigger | When player moves into hazard tile, apply damage immediately. |
| Repeated damage | Player takes damage each time they enter the tile. If they remain on it, no additional damage at turn start. |
| Teleport | Teleporting into hazard triggers damage. |
| Death | If damage reduces player HP to 0 or below, game over. |
| Visual | Hazard tile always shows pattern and damage glyph. |
| Audio | Hazard hit sound and red/white hit flash. |

## 4.9 Inventory

Tier: 2.

| Rule | Number / detail |
| --- | --- |
| Slots | Exactly 3. |
| Stacking | None. Each item instance occupies one slot. |
| Pickup | Moving onto item tile adds item if any slot is empty. If full, message “Bag full” and item remains. |
| Use | Press `item_1`, `item_2`, or `item_3`. Consumes item. |
| Energy item | `tuna_can` sets `player.nextTurnEnergyBonus = min(player.nextTurnEnergyBonus + 2, 2)`. |
| Healing item | `yarn_potion` heals 12 capped at max HP. |
| Damage item | `catnip_bomb` deals 6 damage to all enemies within radius 2 of player. |
| Shop purchase | Item purchase fails if inventory is full. |

## 4.10 Economy

Tier: 2.

| Rule | Number / detail |
| --- | --- |
| Currency name | Mana Coins. |
| Starting gold | 0. |
| Kill drops | On enemy death, add `enemy.gold * difficulty.goldMul`, rounded down. |
| Coin pickups | Each coin adds 5 gold. |
| Level completion | Adds 10 gold. |
| Boss completion | Adds 50 gold from boss kill plus 10 completion. |
| Shop appearance | Levels 2 and 3 only. |
| Shop interaction | Player stands on shop tile and presses interact. |
| Shop offers | 3 card offers, 3 item offers. Offers are generated from available pools using `levelSeed`. |
| Buying | Press 1-6 to buy offer. Must have enough gold. |
| Card purchase | Add card ID to `allCards`. |
| Item purchase | Add item to first empty inventory slot. |
| Spending | Subtract price from `run.gold`. |
| Insufficient gold | Show error message and sound. |
| Shop persistence | Shop disappears when level ends. Offers do not refresh during a level. |

## 4.11 Progression and difficulty

### Run progression

| Stage | Effect |
| --- | --- |
| Level 1 | Start deck only. No upgrades. |
| After Level 1 | Choose 1 blessing. |
| Shop Level 2 | Spend gold on cards/items. |
| After Level 2 | Choose 1 blessing. |
| Shop Level 3 | Spend gold on cards/items. |
| After Level 3 | Choose 1 blessing. |
| After Level 4 | Choose 1 blessing. |
| Boss Level | Fight Grand Archmage Dog. Win by reaching exit after boss death. |

### Difficulty options

| Difficulty | Player max HP | Enemy HP multiplier | Enemy damage multiplier | Gold multiplier | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| Easy | 40 | 0.70 | 0.60 | 1.20 | Player starts normal energy and movement. |
| Normal | 30 | 1.00 | 1.00 | 1.00 | Default. |
| Hard | 25 | 1.50 | 1.40 | 1.00 | Enemy AI unchanged. |

### Expected session length

| Segment | Expected time |
| --- | ---: |
| Title and run start | 0.5 min |
| Normal level | 3-5 min |
| Shop level | 4-6 min |
| Boss fight | 8-10 min |
| Full run | 20-28 min |

## 4.12 Feel

| Element | Rule |
| --- | --- |
| Input response | Movement and menu actions occur on key down. |
| Invalid action | Error bleep, message, no state change. |
| Card play | Card leaves hand, energy pips decrease, target flashes, particles spawn. |
| Hit | Target hit flash 80 ms, screen shake 4 px for 120 ms, damage particles. |
| Death | Entity fades out over 500 ms with particle burst. |
| Level complete | Banner “Meow! Onward!” for 1200 ms, then next level. |
| Game over | Banner “Naptime forever.” then Game Over screen. |
| Win | Banner “Tower Meowstered!” then Win screen. |

# 5. CHARACTERS

## Silhouettes and facings

| Character | Silhouette | Facing | Notes |
| --- | --- | --- | --- |
| Sir Whiskers | Cat ears, pointed hat, robe, tail. | Left/right only. | 16 × 16. |
| Clockwork Crow | Round bird with gear tail. | Left/right only. | 16 × 16. |
| Mouse Mage | Small mouse with wizard staff. | Left/right only. | 16 × 16. |
| Candle Imp | Flame with tiny legs. | Left/right only. | 16 × 16. |
| Book Wraith | Floating open book with ghost tail. | Left/right only. | 16 × 16. |
| Broom Golem | Broom head, barrel body. | Left/right only. | 16 × 16. |
| Grand Archmage Dog | Dog in huge wizard hat, staff. | Left/right only. | 32 × 32. |

## Animations

| Animation name | Entity | Frames | Motion rule | Gameplay state |
| --- | --- | ---: | --- | --- |
| `idle` | All | 4 | 2 px vertical bob, 8 FPS | Entity alive and not acting. |
| `walk` | All moving entities | 4 | Horizontal step, 8 FPS | `moveEntity` called. |
| `attack` | Enemies | 3 | Lunge 2 px toward player, 8 FPS | `resolveAttack`. |
| `cast` | Player, boss | 4 | Paw/staff glow, 8 FPS | Card play or boss attack. |
| `hit` | All | 2 | White flash, recoil 1 px opposite facing | `damageEntity`. |
| `death` | All | 6 | Fade and dissolve, 500 ms | `hp <= 0`. |
| `boss_phase` | Boss | 4 | Rapid bob, palette flash | Boss enters phase 2. |
| `targeting` | Player aim cursor | 2 | Blink white/cyan | Card targeting. |

## Boss phase rules

| Phase | Trigger | Change |
| --- | --- | --- |
| Phase 1 | Boss alive and HP > 45 | Base stats. |
| Phase 2 | Boss alive and HP <= 45 | `damage += 2`, `movePoints += 1`, `attackRange += 1`, play `boss_roar`, screen shake. |

# 6. AUDIO

All audio is synthesized with WebAudio. No samples. Master volume applies to all. Music and SFX volumes are separate.

## Music

| Name | Recipe | Plays when |
| --- | --- | --- |
| `music_title` | Square lead, 120 BPM, 8-bar loop, root D minor, triangle bass, noise hat every 8th. | Title, settings, pause. |
| `music_battle` | Pulse lead 140 BPM, triangle bass, square arpeggio, noise snare on 2/4. | Normal levels. |
| `music_boss` | Square lead 160 BPM, saw bass, fast noise fills, root C minor. | Boss level. |

## Sound effects

| Name | Recipe | Plays when |
| --- | --- | --- |
| `ui_move` | Square 880 Hz, 0.05 s, gain 0.10. | Menu selection. |
| `ui_confirm` | Square 660 Hz to 990 Hz, 0.12 s, gain 0.12. | Confirm action. |
| `ui_cancel` | Square 440 Hz to 330 Hz, 0.12 s, gain 0.12. | Cancel action. |
| `ui_error` | Square 220 Hz, 0.10 s, gain 0.15. | Invalid action. |
| `card_draw` | Noise burst 0.05 s + square 1200 Hz 0.04 s. | Drawing cards. |
| `card_play` | Square 500 Hz to 800 Hz, 0.15 s, gain 0.14. | Playing a card. |
| `paw_hit` | Triangle 300 Hz to 150 Hz, 0.12 s + noise. | Player damage card hits enemy. |
| `enemy_hit` | Square 200 Hz to 100 Hz, 0.10 s, gain 0.14. | Enemy damaged. |
| `enemy_attack` | Saw 150 Hz to 80 Hz, 0.20 s, gain 0.16. | Enemy attacks player. |
| `player_hit` | Saw 120 Hz to 60 Hz, 0.25 s, gain 0.20. | Player damaged. |
| `heal` | Sine 520 Hz to 780 Hz, 0.30 s, gain 0.14. | Healing card or item. |
| `move_card` | Square 1000 Hz to 400 Hz, 0.15 s, gain 0.14. | Flick or Blink. |
| `end_turn` | Triangle 440 Hz to 660 Hz, 0.10 s, gain 0.10. | Player ends turn. |
| `coin_pickup` | Square 1320 Hz to 1760 Hz, 0.10 s, gain 0.14. | Coin pickup. |
| `item_pickup` | Square 700 Hz to 1100 Hz, 0.12 s, gain 0.14. | Item pickup. |
| `item_use` | Square 800 Hz to 1200 Hz, 0.15 s, gain 0.16. | Item used. |
| `explosion` | Noise burst 0.30 s lowpass 800 Hz. | Fireball or Catnip Bomb. |
| `hazard_hit` | Saw 90 Hz to 40 Hz, 0.25 s, gain 0.20. | Player touches hazard. |
| `death` | Saw 200 Hz to 50 Hz, 0.80 s, gain 0.25. | Entity dies. |
| `player_death` | Saw 180 Hz to 40 Hz, 1.20 s, gain 0.30. | Player dies. |
| `level_complete` | Square arpeggio D-F-A-D, 0.50 s. | Level completed. |
| `boss_roar` | Saw 80 Hz to 60 Hz, 0.80 s, gain 0.28. | Boss spawn or phase 2. |
| `win` | Square arpeggio D-F-A-C-D, 1.50 s. | Win screen. |

# 7. UX

## HTML and CSS structure

Screens are DOM overlays. The canvas is behind. JavaScript only changes classes and text.

```html
<main id="game">
  <canvas id="canvas"></canvas>
  <div id="hud"></div>
  <div id="overlay"></div>
  <section id="screen-title" class="screen"></section>
  <section id="screen-settings" class="screen"></section>
  <section id="screen-pause" class="screen"></section>
  <section id="screen-game-over" class="screen"></section>
  <section id="screen-win" class="screen"></section>
</main>
```

CSS rules:

| Rule | Value |
| --- | --- |
| Canvas image rendering | `image-rendering: pixelated;` |
| Font | `font-family: 'PixelFont', 'Press Start 2P', monospace;` |
| Text size | 16 px logical. |
| Letter spacing | 1 px. |
| UI border | 4 px solid black. |
| Button focus | White outline 2 px. |
| Reduced motion class | `.reduced-motion { transition: none; animation: none; }` |

## Screen state machine

| Current | Event | Next | Notes |
| --- | --- | --- | --- |
| Title | Confirm New Run | Game | Starts run with selected difficulty. |
| Title | Open Settings | Settings | Opens settings from title. |
| Settings | Confirm/Back | Title or Pause | Returns to previous screen. |
| Game | Press Pause | Pause | Pauses game. |
| Pause | Resume | Game | Resumes. |
| Pause | Settings | Settings | Opens settings. |
| Pause | Restart Run | Game | Starts new run. |
| Pause | Quit to Title | Title | Abandons run. |
| Game | Player HP <= 0 | Game Over | Permadeath. |
| Game | Reach active exit on boss level | Win | Ends run. |
| Game Over | Try Again | Game | New run. |
| Game Over | Title | Title | Returns to title. |
| Win | Play Again | Game | New run. |
| Win | Title | Title | Returns to title. |

## Controls

| Action | Default keys | When active |
| --- | --- | --- |
| Move up | `W` | Game, player turn. |
| Move left | `A` | Game, player turn. |
| Move down | `S` | Game, player turn. |
| Move right | `D` | Game, player turn. |
| Aim up | `ArrowUp` | Card targeting. |
| Aim left | `ArrowLeft` | Card targeting. |
| Aim down | `ArrowDown` | Card targeting. |
| Aim right | `ArrowRight` | Card targeting. |
| Play card 1-5 | `1`-`5` | Game, player turn. |
| Use item 1-3 | `6`-`8` | Game, player turn. |
| Interact | `E` | Standing on shop tile. |
| End turn | `Space` | Game, player turn. |
| Confirm | `Enter` | Menus, targeting, shop, blessing. |
| Cancel | `Escape` | Targeting, shop, inventory. |
| Pause | `Escape` | Game, not targeting. |
| Restart | `R` | Game Over, Win. |

Mouse fallback:

| Mouse | Action |
| --- | --- |
| Click card | Enter targeting. |
| Click valid target | Confirm card. |
| Right click | Cancel targeting. |
| Click shop tile | Open shop if player is adjacent or on shop tile. |
| Click item slot | Use item. |

## HUD

| Element | Record field | When visible |
| --- | --- | --- |
| Health bar | `state.player.hp`, `state.player.maxHp` | `state.ui.screen === "game"` |
| Health number | `state.player.hp` | `state.ui.screen === "game"` |
| Currency | `state.run.gold` | `state.ui.screen === "game"` |

## Card UI

| Element | Record field | When visible |
| --- | --- | --- |
| Energy pips | `state.turn.energy`, `state.turn.maxEnergy` | `state.ui.screen === "game"` |
| Hand cards | `state.cards.hand` | `state.ui.screen === "game"` |
| Draw pile count | `state.cards.drawPile.length` | `state.ui.screen === "game"` |
| Discard pile count | `state.cards.discard.length` | `state.ui.screen === "game"` |
| Aim cursor | `state.turn.aimCursor` | `state.turn.targeting === true` |
| Target highlight | valid target check | `state.turn.targeting === true` |

## Settings screen

| Setting | Control | Default | Effect |
| --- | --- | --- | --- |
| Difficulty | Buttons Easy / Normal / Hard | Normal | Applies multipliers. |
| Reduced motion | Toggle | Off | Disables shake and particles. |
| Colour-blind safe palette | Always on | On | Uses required palette. |
| Remap keys | List of actions | Defaults | Stores custom key map. |
| Master volume | Slider 0-1 | 0.8 | Audio. |
| Music volume | Slider 0-1 | 0.7 | Audio. |
| SFX volume | Slider 0-1 | 0.8 | Audio. |

# 8. DEBUG API

| Function | System | Parameters | Returns | Purpose |
| --- | --- | --- | --- | --- |
| `Debug.roguelike.startRun(seed, difficulty)` | Roguelike | `seed:number`, `difficulty:string` | `GameState` | Start a deterministic run. |
| `Debug.roguelike.restartRun()` | Roguelike | none | `GameState` | Start new run from current screen. |
| `Debug.movement.move(action)` | Movement | `action:'up'|'down'|'left'|'right'` | `boolean` | Attempt player move. |
| `Debug.turn.endTurn()` | Turn | none | `void` | End player turn. |
| `Debug.combat.damageEntity(entityId, amount)` | Combat | `entityId:string`, `amount:number` | `boolean` | Apply damage directly. |
| `Debug.combat.resolveAttack(attackerId, targetId)` | Combat | IDs | `boolean` | Resolve one attack. |
| `Debug.cards.playCard(handIndex, target)` | Cards | `handIndex:number`, `target:Point|null` | `boolean` | Play card. |
| `Debug.cards.drawCards(n)` | Cards | `n:number` | `number` | Draw cards and return number drawn. |
| `Debug.levelgen.generateLevel(index, seed)` | Procedural generation | `index:number`, `seed:number` | `LevelState` | Generate level. |
| `Debug.hazards.triggerAt(x, y)` | Hazards | `x:number`, `y:number` | `number` | Trigger hazard damage at tile. |
| `Debug.inventory.addItem(itemId)` | Inventory | `itemId:string` | `boolean` | Add item. |
| `Debug.inventory.useItem(slot)` | Inventory | `slot:number` | `boolean` | Use item. |
| `Debug.economy.addGold(n)` | Economy | `n:number` | `number` | Add gold. |
| `Debug.economy.spendGold(n)` | Economy | `n:number` | `boolean` | Spend gold. |
| `Debug.economy.buyShopOffer(index)` | Economy | `index:number` | `boolean` | Buy shop offer. |
| `Debug.progression.generateBlessingChoices()` | Progression | none | `string[]` | Generate blessing choices. |
| `Debug.progression.applyBlessing(id)` | Progression | `id:string` | `boolean` | Apply blessing. |
| `Debug.input.press(action)` | Input | `action:InputAction` | `boolean` | Simulate press. |
| `Debug.input.release(action)` | Input | `action:InputAction` | `boolean` | Simulate release. |
| `Debug.input.remap(action, keyCode)` | Input | action, key code | `boolean` | Remap key. |
| `Debug.state.get()` | State | none | `GameState` | Read state. |
| `Debug.settings.set(key, value)` | Settings | key, value | `void` | Set setting. |

# 9. TESTS

## Tier 1 tests

| Test | Assertion |
| --- | --- |
| `rng_seed_determinism` | `Debug.roguelike.startRun(123, "normal")` twice produces identical initial state. |
| `player_can_move_cardinal` | `Debug.movement.move("right")` changes player x by 1 when target is walkable. |
| `player_blocked_by_wall` | Move into wall returns false and player position unchanged. |
| `move_points_limit` | After 2 moves, third move returns false. |
| `turn_end_enemy_phase` | `Debug.turn.endTurn()` causes enemy phase and then returns to player_start. |
| `card_play_uses_energy` | Playing `paw_swipe` reduces energy by 1. |
| `card_play_discards` | Played card is removed from hand and appears in discard. |
| `card_damage_enemy` | `paw_swipe` reduces target enemy HP by 3. |
| `enemy_attack_damage` | Adjacent enemy attacks player and reduces player HP by its damage. |
| `player_death_game_over` | Setting player HP to 0 sets `state.ui.screen === "game_over"`. |
| `deck_reshuffles_discard` | Drawing from empty draw pile shuffles discard into draw pile. |
| `level_exit_advances` | Moving onto active exit starts next level. |
| `boss_exit_locked_until_death` | Boss level exit tile is locked until boss HP <= 0. |
| `win_after_boss_exit` | After boss death, reaching exit sets `state.ui.screen === "win"`. |
| `required_screens_exist` | Title, settings, pause, game over, win screens are present and reachable. |
| `hud_visible_in_game` | Health and currency HUD elements are visible in game screen. |
| `audio_no_errors` | `AudioAPI.playSFX` and `startMusic` do not throw. |
| `fx_present` | Damage causes hit flash; if reduced motion off, causes shake/particles. |

## Tier 2 tests

| Test | Assertion |
| --- | --- |
| `procedural_path_exists` | For seeds 1-50, generated levels 1-4 have BFS path from start to exit. |
| `procedural_same_seed_same_level` | Same seed and level index produce same grid hash. |
| `hazard_damage_on_enter` | Moving into `hazard_spikes` reduces player HP by 5. |
| `hazard_teleport_damage` | Teleporting into hazard triggers damage. |
| `enemy_gold_drop` | Killing enemy adds expected gold. |
| `coin_pickup_gold` | Moving onto coin adds 5 gold. |
| `shop_offer_generation` | Shop level has exactly 3 card offers and 3 item offers. |
| `shop_purchase_card` | Buying card adds card to `run.allCards` and subtracts price. |
| `shop_purchase_item_inventory_full` | Cannot buy item if 3 inventory slots full. |
| `inventory_limit_3` | `Debug.inventory.addItem` fails when 3 items present. |
| `item_heal` | Using `yarn_potion` heals 12 capped at max HP. |
| `item_energy_next_turn` | Using `tuna_can` gives +2 energy at next `player_start`. |
| `item_aoe_damage` | Using `catnip_bomb` damages enemies within radius 2. |
| `blessing_choices_unique` | `Debug.progression.generateBlessingChoices()` returns 3 unique valid IDs. |
| `blessing_max_hp` | Applying `vitality` increases max HP by 8 and heals to max. |
| `blessing_energy_cap` | Applying `max_energy_plus` caps at 5. |
| `difficulty_scales_enemies` | Enemy HP/damage match difficulty multipliers. |
| `reduced_motion_disables_fx` | With `reducedMotion = true`, damage does not create particles or shake. |
| `remappable_keys` | Remapping `move_right` to `KeyX` makes `press("move_right")` move player. |

# 10. BUILD ORDER

1. Create `index.html`, CSS, canvas scaling, pixel font, DOM screen containers.
2. Implement settings, input mapping, remapping, and debug input functions.
3. Implement seeded RNG and global context.
4. Implement state skeleton: `run`, `level`, `entities`, `turn`, `cards`, `ui`.
5. Implement 24 × 14 grid and fixed renderer for walls, floors, tiles, HUD placeholders.
6. Implement player entity, cardinal movement, move points, facing, and basic animation.
7. Implement enemy entity, HP, death, and simple melee AI.
8. Implement cards: deck, draw pile, hand, discard, energy, card selection, targeting, and card effects.
9. Implement combat: player card damage, enemy attacks, damage feedback, game over, level exit, boss unlock, win.
10. Add Tier 1 fixed levels: Level 1, Level 2, Boss. Ensure a complete run is possible.
11. Add required screens: title, pause, settings, game over, win.
12. Add HUD health and currency.
13. Add pixel art, palette, animations, hit flash, particles, screen shake.
14. Add chiptune music and bleeps.
15. Verify Tier 1 tests.
16. Add procedural generation for levels 1-4.
17. Add hazards.
18. Add economy: gold drops, coins, shop, buying.
19. Add inventory and items.
20. Add progression blessings.
21. Add full 5-level run content.
22. Add accessibility tests and difficulty scaling tests.
23. Final polish: error messages, reduced motion, remapping, win/lose flow, balance.

# 11. DEFINITION OF DONE

## Tier 1: Core playable game

High-level: A player can start a run, play a minimal 3-level run, fight enemies with cards, die permanently, restart, defeat the boss, and win. The game is visibly pixel art, audibly chiptune, and has required screens and HUD.

- [ ] `state.run` exists with seed, level index, cards, gold, player stats.
- [ ] New run starts from title and creates deterministic seeded state.
- [ ] Grid is 24 × 14 with walls, floors, exit, player, enemies.
- [ ] Player can move cardinal only and is blocked by walls/entities.
- [ ] Player has 2 move points per turn.
- [ ] Player has 3 energy per turn.
- [ ] Player starts with exactly 10 cards.
- [ ] Player draws to 5 cards each turn.
- [ ] Played cards go to discard.
- [ ] Empty draw pile reshuffles discard.
- [ ] Cards can target enemies, self, or tiles as specified.
- [ ] Enemies take turns and attack the player.
- [ ] Player HP is tracked and shown.
- [ ] Currency HUD exists and shows `run.gold` even if zero.
- [ ] Death triggers Game Over.
- [ ] New run from Game Over works.
- [ ] Boss exit is locked until boss dies.
- [ ] Reaching boss exit triggers Win.
- [ ] Title, pause, settings, game over, win screens exist.
- [ ] Pixel art palette and sprites are used.
- [ ] Pixel font is used.
- [ ] Chiptune music and bleeps exist.
- [ ] Hit flash, particles, and screen shake exist.
- [ ] Reduced motion setting disables shake and particles.
- [ ] Tier 1 tests pass.

## Tier 2: Supporting mechanics

High-level: The Tier 1 game becomes a full 5-level run with generated levels, hazards, economy, inventory, and run progression.

- [ ] Full run has 4 normal levels and 1 boss level.
- [ ] Levels 1-4 are procedurally generated with guaranteed path.
- [ ] Procedural generation is deterministic by seed.
- [ ] Hazard types exist and damage player on entry.
- [ ] Coin pickups add gold.
- [ ] Enemy kills add gold.
- [ ] Shop appears on levels 2 and 3.
- [ ] Shop has 3 card offers and 3 item offers.
- [ ] Buying cards adds them to `allCards`.
- [ ] Buying items adds them to inventory if space exists.
- [ ] Inventory has exactly 3 slots.
- [ ] Items can be used with keys 6-8.
- [ ] Blessing choices appear after normal levels.
- [ ] Blessings modify run stats or deck.
- [ ] Difficulty options scale player and enemies.
- [ ] Tier 2 tests pass.

## Tier 3: Extra mechanics

High-level: Not applicable.

- [ ] No extra mechanics added beyond core and supporting mechanics.

# A. SANITY

| Check | Result | Notes |
| --- | --- | --- |
| Core mechanics are Tier 1 | Valid | Combat, roguelike, and cards are required in Tier 1. |
| Supporting mechanics are Tier 2 only | Valid | Procedural generation, progression, hazards, inventory, and economy are Tier 2. |
| Tier 1 does not depend on Tier 2 | Valid | Tier 1 uses fixed templates and zero gold. Required currency HUD exists but economy is not required. |
| Required screens exactly match | Valid | Screens are title, pause, settings, game over, win. Game is a state, not a screen. |
| HUD matches request | Valid | HUD table includes health and currency. Energy and hand are card UI, not HUD. |
| Accessibility requirements are present | Valid | Colour-safe palette, reduced motion, remappable keys, difficulty options all specified. |
| No extra systems | Valid | No crafting, quests, XP, meta progression, save slots, stealth, or companion systems. |
| Numbers are concrete | Valid | Grid, HP, energy, movement, cards, items, hazards, enemies, levels, shop prices, and difficulty multipliers are numeric. |
| Side-on and grid-based are compatible | Valid | Side-on is visual. Gameplay is turn-based tactical grid movement without gravity. |
| Under 30 minutes | Valid | 5 levels with expected 20-28 minute full run. |
| Final boss and exit win condition | Valid | Boss exit locked until boss death, then reaching exit wins. |
| Roguelike runs are different | Valid | Tier 1 uses seeded random spawn choices. Tier 2 uses deterministic procedural generation. |
| Cards are the player’s combat action | Valid | Player attacks only through cards/items. |
| Inventory limit is explicit | Valid | Exactly 3 slots. |
| Economy is spending-based | Valid | Gold from kills/coins/level completion, spent on cards/items. |
| Hazards are fixed and damage on touch | Valid | Hazard tiles deal damage when player enters. |
| Progression is run-only | Valid | Blessings apply to current run only. |
| Audio is synthesized | Valid | WebAudio recipes only, no audio files. |
| Pixel style is specified | Valid | 16 px tiles, low-res sprites, palette, pixel font. |
| Builder can test each tier | Valid | Tier 1 and Tier 2 tests are listed. |
| Debug API covers systems and inputs | Valid | One function set per system plus input functions. |
| Contracts include state fields | Valid | Global context includes all gameplay records. |
| Build order reaches Tier 1 before Tier 2 | Valid | Build order completes minimal core run before supporting mechanics. |