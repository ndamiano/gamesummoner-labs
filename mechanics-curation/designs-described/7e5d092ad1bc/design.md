# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Game prompt: roguelike deckbuilder where you're a wizard cat climbing a tower | `# 4. GAMEPLAY SPEC`, `# 5. CHARACTERS`, `# 0.2 Decisions` |
| Dimension: 2D | `# 1.1 Units, axes, frames`, `# 3. VISUAL SPEC` |
| Camera: side-on | `# 3. VISUAL SPEC`, `# 4.4 Procedural Generation` |
| Time model: turn-based | `# 1.2 Important conventions`, `# 4.1 Combat` |
| Movement model: grid-based | `# 4.1 Combat`, `# 4.4 Procedural Generation`, `# 7. UX` |
| Session shape: sequence of levels | `# 4.3 Roguelike`, `# 4.4 Procedural Generation` |
| Failure: permadeath, start a new run | `# 4.3 Roguelike`, `# 7. UX`, `# 11. DEFINITION OF DONE` |
| Tone: silly | `# 4. GAMEPLAY SPEC`, `# 5. CHARACTERS`, `# 6. AUDIO`, `# 7. UX` |
| Size: a handful of levels, under 30 minutes | `# 0.2 Decisions`, `# 4.3 Roguelike`, `# 4. Progression and difficulty` |
| Win/lose: reach exit, defeat final boss | `# 4.3 Roguelike`, `# 4.4 Procedural Generation` |
| Core mechanic: combat | `# 4.1 Combat` |
| Core mechanic: cards | `# 4.2 Cards` |
| Core mechanic: roguelike | `# 4.3 Roguelike` |
| Core mechanic: procedural generation | `# 4.4 Procedural Generation` |
| Supporting mechanic: abilities | `# 4.5 Abilities` |
| Supporting mechanic: hazards | `# 4.6 Hazards` |
| Supporting mechanic: economy | `# 4.7 Economy` |
| Extra mechanics: none | `# 0.2 Decisions`, `# 11. DEFINITION OF DONE` |
| Art style: pixel art, low-resolution sprites, visible square pixels, limited palette | `# 3. VISUAL SPEC`, `# 5. CHARACTERS` |
| Palette: saturated, bright, strong colours | `# 3. VISUAL SPEC` |
| Typography: pixel font, blocky bitmap letters | `# 3. VISUAL SPEC`, `# 7. UX` |
| Music: chiptune, retro console bleeps | `# 6. AUDIO` |
| Sound effects style: retro bleeps, synthesized chip sounds | `# 6. AUDIO` |
| Screens: title, pause, settings, game over, win | `# 7. UX` |
| HUD: health, currency | `# 7. UX` |
| Effects: screen shake, particles, hit flash | `# 3. VISUAL SPEC`, `# 1.1 Units, axes, frames` |
| Accessibility: colour-blind safe palette, reduced motion, remappable keys, difficulty options | `# 3. VISUAL SPEC`, `# 7. UX`, `# 1.2 Important conventions` |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| High-level prompt | Final as given: wizard cat climbs a tower in a roguelike deckbuilder. | Sets all downstream content. |
| Dimension: 2D | Final as given. | Required. |
| Camera: side-on | Final side-on fixed viewport. No scrolling. The whole level is visible. | Keeps scope small and makes grid movement readable. |
| Time model: turn-based | Final as given. Player turn, then enemy turns. | Required. |
| Movement model: grid-based | Final as given. Integer tile coordinates. 4-directional movement. | Required. |
| Session shape: sequence of levels | Final as given. Exactly 5 levels: 4 climb levels and 1 final boss level. | A handful of levels. Keeps runs under 30 minutes. |
| Failure: permadeath | Final as given. Death ends run. New run starts from level 1. | Required. |
| Tone: silly | Final as given. Cat puns, yarn, fish, absurd towers. | Required. |
| Size: under 30 minutes | Target: level 1 2 min, levels 2-4 3-5 min each, boss 6-8 min, total 20-28 min. | Matches request. |
| Win/lose | Final as given. Normal exits unlock after all enemies in that level are defeated. Final exit unlocks after final boss is defeated. | Ensures the run is a climb and a boss fight. |
| Core mechanic: combat | Final as given. Implemented as HP, Guard, enemy attacks, card attacks, boss fight. | Required. |
| Core mechanic: cards | Final as given. Deck, hand, draw, discard, energy, card effects. | Required. |
| Core mechanic: roguelike | Final as given. Permadeath, procedural levels, card rewards, minimal persistent unlocks. | Required. |
| Core mechanic: procedural generation | Final as given. Seeded level generation with validation. | Required. |
| Supporting mechanic: abilities | Final as given. One active ability with cooldown. Tier 2. | Required. |
| Supporting mechanic: hazards | Final as given. Spikes, lava, falling pits. Tier 2. | Required. |
| Supporting mechanic: economy | Final as given. Currency, shop, buy, sell, trade. Tier 2. | Required. |
| Extra mechanics | None. No relics, no crafting, no skill trees, no stealth, no companion system. | Explicitly excluded. |
| Art style | Final as given. Pixel art, 16 logical pixel tiles, visible pixels, limited palette. | Required. |
| Palette | Final as given plus concrete colour-blind safe palette. | Required accessibility. |
| Typography | Final as given. Pixel font for all UI. | Required. |
| Music | Final as given. Chiptune loops for title, levels, boss, game over, win. | Required. |
| Sound effects | Final as given. Synthesized chip sounds. | Required. |
| Screens | Final required screens: title, pause, settings, game over, win. Technical `BOOT` state allowed. Level clear is an in-game modal, not a new full screen. | Keeps required screens exact while allowing card/roguelike completion. |
| HUD | Final required HUD: health, currency. Additional card/turn controls are necessary for the required card system. | Core cards cannot be played without visible hand/energy. |
| Effects | Final as given: screen shake, particles, hit flash. | Required. |
| Accessibility | Final as given: colour-blind palette, reduced motion, remappable keys, difficulty options. | Required. |
| Grid size | 18 × 12 tiles. | Fits side-on viewport, supports 5 short levels, keeps pathfinding simple. |
| Tile logical size | 16 × 16 logical pixels. | Standard small pixel art unit. |
| Display scale | 3× logical scale: 864 × 576 CSS pixels. | Visible pixels, still small. |
| Player identity | Wizard Cat, named Mittens. Silly. | Prompt. |
| Player max HP | Normal 30. Easy 40. Hard 20. | Difficulty options. |
| Player movement | 3 move points per turn by default. Orthogonal tile movement. | Turn-based grid movement. |
| Player energy | 3 energy per turn. | Card costs. |
| Player hand | Draw up to 5 cards at start of each player turn. Hand limit 7. | Deckbuilder. |
| Deck rule | At start of turn, discard current hand, draw up to 5. If deck empty, shuffle discard into deck. | Standard, readable deckbuilder. |
| Card targeting | Cards auto-target by direction/radius/self. Facing controls directional cards. | Keeps input simple and keyboard accessible. |
| Guard | Temporary damage absorption. Resets at start of player turn. | Needed for defensive cards without adding a new top-level system. |
| Level count | 5 total levels. | Handful of levels, short runs. |
| Level structure | One grid per level. Exit locked until all enemies defeated. Final boss level exit locked until boss defeated. | Sequence of levels, win/lose requirements. |
| Enemy count | Level 1: 2. Level 2: 3. Level 3: 4. Level 4: 5. Level 5: boss + 2. Difficulty modifies count. | Keeps run short. |
| Enemy roster | Mouse Scout, Rat Mage, Golem Crate, Archmage Doggo boss. | Sufficient variety, no extra systems. |
| Starting deck | 12 cards. | Enough for a short run. |
| Card reward | At end of each normal level, choose 1 of 3 random cards. | Roguelike/deckbuilder progression. |
| Persistent unlocks | Minimal: after reaching level 3 unlock one stronger card in reward pool; after winning unlock one starting card. | Roguelike may carry over unlocks. |
| Currency | Earned from enemy kills and level clear. Displayed in HUD. Tier 1 tracks and shows it; spending is Tier 2 economy. | Required HUD without making economy a Tier 1 dependency. |
| Shop | Tier 2. Appears in level clear modal. Offers 3 random items. Buy, sell, trade. | Required economy. |
| Ability | Tier 2. One active ability: Familiar Dash. Cooldown only, no mana. | Required abilities without adding resource system. |
| Hazards | Tier 2. Spikes, lava, pits. | Required hazards. |
| Difficulty | Easy, Normal, Hard with explicit numeric effects. | Required accessibility. |
| Input defaults | WASD/arrows, 1-5, Space, Q, Esc, Enter. Remappable. | Required input and accessibility. |
| RNG | Deterministic seeded PRNG. No `Math.random()` in gameplay. | Required procedural generation and tests. |
| Rendering | World and UI are DOM/HTML/CSS sprites and panels. JS updates state/classes. No canvas/WebGL. | Matches “HTML and CSS only” UX. |
| Save data | Settings and persistent unlocks stored in `localStorage`. | Required accessibility and persistent unlocks. |

## 0.3 Tiers

Tier 1 is the complete core game. It is playable, winnable, losable, drawn, heard, and tested.

### Tier 1: Core

1. Project shell, state machine, input mapping, settings storage.
2. Accessibility: difficulty selection, colour-blind safe palette, reduced motion flag, remappable keys.
3. Pixel rendering for world, characters, tiles, HUD, screens.
4. Audio API integration for chiptune music and retro bleeps.
5. Effects: screen shake, particles, hit flash.
6. Grid world, 18 × 12 levels, side-on view, fixed camera.
7. Player movement, facing, turn points.
8. Card deck, hand, draw, discard, energy, play card.
9. Combat: damage, Guard, enemy HP, player HP, death.
10. Enemy AI for Mouse Scout, Rat Mage, Golem Crate.
11. Procedural generation for levels 1-4 and boss level.
12. Run structure: 5 levels, exits, permadeath, win, game over.
13. Final boss: Archmage Doggo.
14. Required screens: title, pause, settings, game over, win.
15. Required HUD: health, currency, plus necessary card/turn UI.
16. Card rewards after normal levels.
17. Minimal persistent unlocks.
18. Difficulty options affecting HP, damage, enemy count.

### Tier 2: Supporting mechanics

1. Active ability: Familiar Dash with cooldown.
2. Hazards: spikes, lava, falling pits.
3. Economy: currency spending, shop, buy, sell, trade.
4. Shop offers generated procedurally.
5. Ability cooldown reset item.
6. Difficulty interaction with hazards and shop prices.

### Tier 3: Later only if Tier 2 is complete

None. The prompt says extra mechanics: none.

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Quantity | Unit | Value | Notes |
| --- | --- | --- | --- |
| Grid width | tiles | 18 | x range 0..17 |
| Grid height | tiles | 12 | y range 0..11 |
| x axis | tile index | integer | 0 left to 17 right |
| y axis | tile index | integer | 0 top to 11 bottom |
| Tile logical size | logical px | 16 × 16 | Pixel art unit |
| Display scale | CSS px per logical px | 3 | World viewport 864 × 576 CSS px |
| Player sprite logical size | logical px | 16 × 16 | One tile |
| Boss sprite logical size | logical px | 32 × 32 | Occupies 1 logical tile but rendered larger |
| Time | discrete turns | integer | No real-time gameplay logic |
| Animation timing | fps | 8, 10, or 12 | Per animation |
| Screen shake | logical px | 2, 4, or 6 | Applied for 80-200 ms |
| Hit flash | milliseconds | 60-120 | White overlay or bright outline |
| Particle lifetime | milliseconds | 300-900 | Reduced motion disables |
| Damage | integer | 1-8 | All combat numbers are integers |
| HP | integer | 1-60 | Player and enemies |
| Guard | integer | 0-20 | Temporary |
| Energy | integer | 0-3 | Reset each player turn |
| Move points | integer | 2-4 | Difficulty dependent |
| Currency | integer | 0+ | Earned and spent |
| Cooldown | player turns | integer | Ability only |

## 1.2 Important conventions

1. **Deterministic RNG**
   - All procedural generation and card/shop offers use a seeded PRNG.
   - Use `mulberry32` or equivalent 32-bit deterministic PRNG.
   - No gameplay code may call `Math.random()`.
   - `runSeed` is a 32-bit unsigned integer.
   - Level seed is `hash32(runSeed, levelIndex, layoutAttempt)`.
   - Card reward seed is `hash32(runSeed, levelIndex, "reward")`.
   - Shop seed is `hash32(runSeed, levelIndex, "shop")`.

2. **Fixed logical resolution**
   - World logical size: 18 × 12 tiles, 288 × 192 logical pixels.
   - Display scale: 3×.
   - CSS must use `image-rendering: pixelated` for all sprite layers.

3. **Turn-based logic is event-driven**
   - Game state changes only from player input, level clear, enemy turn resolution, or debug functions.
   - Animation frames use `requestAnimationFrame`, but no gameplay rule depends on frame delta.
   - If reduced motion is enabled, animation timers may be shortened but logic remains identical.

4. **Integer arithmetic**
   - HP, damage, Guard, energy, move points, currency, cooldowns, card effects are integers.
   - Difficulty damage scaling:
     - Easy: `Math.floor(baseDamage * 0.75)`
     - Normal: `baseDamage`
     - Hard: `Math.ceil(baseDamage * 1.25)`

5. **State machine is the only UI mode source**
   - `document.body.dataset.state` controls visible screens.
   - Gameplay input is ignored unless state is `GAME` or `LEVEL_CLEAR` as specified.

6. **Save data**
   - Settings key: `wizardCatTower.settings.v1`
   - Persistent unlock key: `wizardCatTower.unlocks.v1`
   - Settings and unlocks persist across runs.
   - Run state does not persist after death or win except unlocks.

7. **Colour-blind safety**
   - Important states are never communicated by hue alone.
   - Player has cyan hat. Enemies have orange/magenta/yellow/purple with distinct shapes.
   - Health is cyan bar. Currency is yellow coin icon. Guard is purple shield. Hazards have shape patterns.

8. **Reduced motion**
   - When enabled:
     - Screen shake amplitude becomes 0.
     - Particles are disabled.
     - Hit flash becomes a static high-contrast outline for 120 ms.
   - Gameplay timing and logic are unchanged.

9. **Remappable keys**
   - All gameplay and menu inputs listed in `# 7. UX` are remappable.
   - Settings screen captures one key at a time and writes to `keymap`.
   - Default keymap must work on standard US keyboard.

10. **No extra systems**
    - Guard is part of combat.
    - Card rewards are part of cards/roguelike.
    - Persistent unlocks are part of roguelike.
    - Shop is part of economy.
    - No relics, crafting, companion, stealth, or other mechanics.

# 2. CONTRACTS

## 2.1 Module layout

```text
/src
  main.ts
  state.ts
  config.ts
  rng.ts
  input.ts
  save.ts
  audio.ts
  render/
    world.ts
    effects.ts
    palette.ts
  ui/
    screens.ts
    hud.ts
    level-clear.ts
    settings.ts
  gameplay/
    run.ts
    levelgen.ts
    combat.ts
    cards.ts
    enemies.ts
    abilities.ts
    hazards.ts
    economy.ts
  debug/
    api.ts
/tests
  rng.test.ts
  levelgen.test.ts
  cards.test.ts
  combat.test.ts
  run.test.ts
  abilities.test.ts
  hazards.test.ts
  economy.test.ts
  input.test.ts
/assets
  sprites/
    player.png
    enemies.png
    tiles.png
    ui.png
  fonts/
    pixel-font.css
```

## 2.2 Global context

The global context is the single authoritative state object.

```ts
type Difficulty = "easy" | "normal" | "hard";

type Facing = "up" | "down" | "left" | "right";

type Mode =
  | "boot"
  | "title"
  | "settings"
  | "game"
  | "level_clear"
  | "paused"
  | "game_over"
  | "win";

type Keymap = Record<
  | "moveUp"
  | "moveDown"
  | "moveLeft"
  | "moveRight"
  | "playCard1"
  | "playCard2"
  | "playCard3"
  | "playCard4"
  | "playCard5"
  | "endTurn"
  | "ability"
  | "pause"
  | "confirm"
  | "back"
  | "startRun"
  | "openSettings",
  string
>;

interface Settings {
  difficulty: Difficulty;
  volume: number; // 0..1
  reducedMotion: boolean;
  colorBlindSafe: boolean; // always true in this build, stored for settings UI
  keymap: Keymap;
}

interface Unlocks {
  reachedLevel3: boolean;
  wonGame: boolean;
}

interface CardDef {
  id: string;
  name: string;
  cost: number;
  type: "attack" | "guard" | "heal" | "draw" | "move";
  target: "self" | "adjacentFront" | "ray" | "radiusManhattan" | "nearest" | "adjacentFour";
  range?: number;
  damage?: number;
  guard?: number;
  heal?: number;
  draw?: number;
  move?: number;
  flavor: string;
  tier: 1 | 2;
}

interface CardInstance {
  uid: string;
  defId: string;
}

interface PlayerRecord {
  x: number;
  y: number;
  facing: Facing;
  hp: number;
  maxHp: number;
  guard: number;
  currency: number;
  movePoints: number;
  energy: number;
  deck: CardInstance[];
  hand: CardInstance[];
  discard: CardInstance[];
  abilityCooldown: number;
}

interface EnemyRecord {
  uid: string;
  defId: string;
  x: number;
  y: number;
  hp: number;
  maxHp: number;
  alive: boolean;
  animState: "idle" | "walk" | "attack" | "hit" | "death";
  animFrame: number;
  facing: "left" | "right";
  bossPatternTurn: number;
}

interface HazardRecord {
  uid: string;
  type: "spike" | "lava" | "pit";
  x: number;
  y: number;
  damage: number;
  active: boolean;
}

interface LevelRecord {
  index: number; // 1..5
  seed: number;
  layoutAttempt: number;
  grid: Uint8Array; // 0 floor, 1 wall, 2 exit, 3 start, 4 boss spawn
  width: number;
  height: number;
  enemies: EnemyRecord[];
  hazards: HazardRecord[];
  exitX: number;
  exitY: number;
  exitLocked: boolean;
  turn: number;
  rng: Rng;
}

interface RunRecord {
  seed: number;
  level: number; // 1..5
  difficulty: Difficulty;
  startedAt: number;
  unlocked: Unlocks;
}

interface RewardOffer {
  cardDefIds: string[];
}

interface ShopOffer {
  id: string;
  defId: string;
  cost: number;
  kind: "heal" | "maxHp" | "randomCard" | "removeCard" | "trade" | "resetAbility";
}

interface UiRecord {
  mode: Mode;
  message: string | null;
  reward: RewardOffer | null;
  shop: ShopOffer[] | null;
  selectedCardIndex: number | null;
  selectedShopIndex: number | null;
}

interface EffectsRecord {
  screenShake: {
    x: number;
    y: number;
    durationMs: number;
  };
  particles: {
    id: string;
    kind: "spark" | "poof" | "coin" | "magic" | "blood";
    x: number;
    y: number;
    lifeMs: number;
  }[];
  hitFlash: {
    targetUid: string | null;
    durationMs: number;
  };
}

interface AnimationRecord {
  player: {
    animState: "idle" | "walk" | "cast" | "hit" | "death" | "dash";
    frame: number;
    timeMs: number;
  };
  enemies: Record<string, {
    animState: "idle" | "walk" | "attack" | "hit" | "death";
    frame: number;
    timeMs: number;
  }>;
}

interface GlobalContext {
  settings: Settings;
  unlocks: Unlocks;
  run: RunRecord | null;
  player: PlayerRecord | null;
  level: LevelRecord | null;
  ui: UiRecord;
  effects: EffectsRecord;
  animations: AnimationRecord;
  rng: Rng;
}
```

All modules receive and mutate the same `GlobalContext` through explicit functions. No hidden global mutable state is allowed.

## 2.3 Module specifics

| Module | Required exports / functions | Contract |
| --- | --- | --- |
| `rng.ts` | `createRng(seed: number): Rng`, `hash32(...numbers: number[]): number` | Must be deterministic. `Rng` has `next(): number`, `int(min, max): number`, `shuffle<T>(arr: T[]): T[]`, `pick<T>(arr: T[]): T`. |
| `config.ts` | `CARDS`, `ENEMIES`, `LEVEL_TABLE`, `SHOP_ITEMS`, `DEFAULT_SETTINGS`, `DEFAULT_KEYMAP`, `PALETTE` | Pure data. No gameplay logic. |
| `state.ts` | `createInitialContext(): GlobalContext`, `cloneContextForTest(ctx): GlobalContext` | Only place that creates initial mode `boot`. |
| `save.ts` | `loadSettings(): Settings`, `saveSettings(s: Settings): void`, `loadUnlocks(): Unlocks`, `saveUnlocks(u: Unlocks): void` | Must fail gracefully if storage unavailable. |
| `input.ts` | `bindInput(ctx: GlobalContext): void`, `handleKey(event: KeyboardEvent, ctx: GlobalContext): boolean`, `getActionForKey(key: string, ctx: GlobalContext): Action \| null` | Must not mutate gameplay state directly. It calls gameplay functions. |
| `run.ts` | `startRun(ctx, seed?: number, difficulty?: Difficulty): void`, `nextLevel(ctx): void`, `completeLevel(ctx): void`, `gameOver(ctx): void`, `win(ctx): void`, `restartRun(ctx): void` | Owns run-level transitions and permadeath. |
| `levelgen.ts` | `generateLevel(ctx, levelIndex: number): void`, `validatePath(grid, start, exit): boolean`, `placeEnemies(ctx): void`, `placeHazards(ctx): void` | Must use deterministic RNG. Must guarantee start/exit path. |
| `combat.ts` | `beginPlayerTurn(ctx): void`, `endPlayerTurn(ctx): void`, `runEnemyTurn(ctx): void`, `applyDamage(ctx, targetUid, amount): void`, `applyGuard(ctx, targetUid, amount): void`, `heal(ctx, targetUid, amount): void`, `isPlayerDead(ctx): boolean` | Owns HP, Guard, damage, death. |
| `cards.ts` | `shuffleDeck(ctx): void`, `drawCards(ctx, count: number): void`, `playCard(ctx, handIndex: number): boolean`, `addCard(ctx, defId: string): void`, `removeCard(ctx, uid: string): void`, `generateRewardChoices(ctx): string[]` | Owns deck, hand, discard, card effects. |
| `enemies.ts` | `spawnEnemy(ctx, defId, x, y): EnemyRecord`, `enemyAct(ctx, enemyUid): void`, `findPath(grid, start, goal): Point[]`, `canSee(grid, a, b): boolean` | Owns enemy AI. |
| `abilities.ts` | `activateAbility(ctx): boolean`, `tickAbilityCooldown(ctx): void`, `getAbilityState(ctx): { ready: boolean, cooldown: number }` | Tier 2. No mana, cooldown only. |
| `hazards.ts` | `activateHazard(ctx, hazardUid): void`, `applyFallingPit(ctx, player, yStart): void`, `placeHazards(ctx): void` | Tier 2. |
| `economy.ts` | `addCurrency(ctx, amount): void`, `generateShopOffers(ctx): ShopOffer[]`, `buyShopOffer(ctx, offerIndex: number): boolean`, `sellCard(ctx, cardUid: string): boolean`, `tradeCard(ctx, cardUid: string): boolean` | Tier 2. |
| `ui/screens.ts` | `setMode(ctx, mode: Mode): void`, `renderTitle(ctx): void`, `renderPause(ctx): void`, `renderSettings(ctx): void`, `renderGameOver(ctx): void`, `renderWin(ctx): void` | HTML/CSS only. |
| `ui/hud.ts` | `renderHud(ctx): void`, `updateHealthBar(ctx): void`, `updateCurrency(ctx): void`, `renderHand(ctx): void` | HTML/CSS only. |
| `ui/level-clear.ts` | `openLevelClear(ctx): void`, `chooseReward(ctx, index: number): void`, `closeLevelClear(ctx): void` | Modal inside game state. |
| `render/world.ts` | `renderWorld(ctx): void`, `renderTiles(ctx): void`, `renderEntities(ctx): void`, `renderExit(ctx): void` | DOM/CSS sprites only. |
| `render/effects.ts` | `shake(ctx, px, ms): void`, `spawnParticles(ctx, kind, x, y, count): void`, `hitFlash(ctx, uid, ms): void`, `renderEffects(ctx): void` | Respects reduced motion. |
| `audio.ts` | `playMusic(name: MusicName): void`, `stopMusic(): void`, `playSfx(name: SfxName): void`, `setVolume(v: number): void` | Uses provided audio API. |
| `debug/api.ts` | All functions in `# 8. DEBUG API` | Test and dev hooks. |

# 3. VISUAL SPEC

The game looks like a silly pixel-art tower dungeon: a small 18 × 12 side-on room filled with platforms, bookshelves, yarn, fish, and a wizard cat. Everything is 16-pixel tiles with hard edges and no smoothing. The palette is bright and saturated, using cyan, orange, magenta, yellow, purple, and dark blue. Important information is always shape-coded, not colour-coded alone. The player is always visible in the centre-left of the screen; the exit is always visible top-right.

Lighting is flat pixel art with fake torch glow made from low-alpha orange radial gradients and dithered floor tiles. There is no dynamic light simulation. The atmosphere is goofy: crooked bookshelves, floating yarn, paw prints, and a final boss made of a dog in a wizard hat.

The space is a single fixed side-on viewport per level. The camera never scrolls. The border is always solid walls. Platforms are horizontal floor segments. The start is always bottom-left. The exit is always top-right. The final boss room adds a large 32 × 32 pixel boss sprite but keeps the same grid.

| Element | Visual recipe | State/animation | Colour/pattern rule |
| --- | --- | --- | --- |
| Background | Dark blue gradient, dithered stars, crooked shelves | Static | `#101322` to `#241b4f` |
| Wall tile | Brick outline, hard 1px highlights | Static | `#7209b7` outline, `#3a0ca3` fill |
| Floor tile | Stone with paw print decals | Static | `#2b2d42` fill, `#4361ee` specks |
| Platform | Stone ledge with 1px top highlight | Static | `#4361ee` top, `#2b2d42` body |
| Start pad | Yarn ball circle | Static | `#ffd166` yellow |
| Exit portal | Swirling portal with cat tail icon | Locked: grey dashed border. Unlocked: cyan swirl | Locked `#8d99ae`, unlocked `#00d4ff` |
| Player cat | White cat, purple robe, cyan wizard hat, tail | Idle, walk, cast, hit, death, dash | Hat cyan `#00d4ff`, robe purple `#7209b7` |
| Mouse Scout | Orange mouse with tiny sword | Idle, walk, attack, hit, death | Orange `#ff8800`, dark outline |
| Rat Mage | Magenta rat with staff | Idle, cast, attack, hit, death | Magenta `#ff00aa` |
| Golem Crate | Yellow crate with eyes | Idle, attack, hit, death | Yellow `#ffd60a`, brown planks |
| Boss | Purple dog in wizard hat, 32 × 32 | Idle, cast, attack, hit, death | Purple `#b14bff`, cyan hat |
| Spike | White triangle on tile | Static | White `#ffffff`, black outline |
| Lava | Orange-yellow wavy tile | Animated shimmer 8 fps unless reduced motion | `#ff7b00` and `#ffd166` |
| Pit | Black hole with edge shading | Static | Black `#000000`, grey edge |
| Health bar | Horizontal bar, heart icon | Fills left to right | Cyan `#00d4ff`, dark track |
| Currency | Coin icon with fish imprint | Static | Yellow `#ffd166` |
| Guard icon | Shield icon | Static | Purple `#b5179e` |
| Card face | 48 × 64 logical px pixel card, cost top-left | Hover/select outline | Border matches card type: attack orange, guard purple, heal cyan, draw yellow, move magenta |
| UI text | Pixel bitmap font, 8 px logical | Static | White `#ffffff` on dark panel |
| Screen shake | Whole world layer translates randomly | 80-200 ms | Disabled when reduced motion |
| Particles | 1-2 logical px squares | Spawn, fall/fade | Sparks white/orange, poof grey, coins yellow |
| Hit flash | Entity sprite turns white | 60-120 ms | Reduced motion: static white outline |

# 4. GAMEPLAY SPEC

The player is a wizard cat climbing five procedural tower levels. Each level is one side-on grid. The cat can move up to 3 tiles per turn and play cards for 3 energy. Enemies take turns after the player. Normal exits unlock after all enemies in that level are defeated. The final exit unlocks after the final boss is defeated. Card rewards add new cards to the deck. Death is permanent: the run ends and a new run begins.

## Records and rosters

### Player record

| Field | Type | Initial Normal | Notes |
| --- | --- | --- | --- |
| `hp` | integer | 30 | Death if 0 |
| `maxHp` | integer | 30 | Difficulty changes this |
| `guard` | integer | 0 | Absorbs damage, resets at start of player turn |
| `currency` | integer | 0 | Earned from kills and level clear |
| `movePoints` | integer | 3 | Reset each player turn |
| `energy` | integer | 3 | Reset each player turn |
| `deck` | CardInstance[] | 12 cards | Starting deck |
| `hand` | CardInstance[] | [] | Max 7 |
| `discard` | CardInstance[] | [] | Shuffles into deck when deck empty |
| `facing` | Facing | `right` | Changes on movement |
| `abilityCooldown` | integer | 0 | Tier 2 only |

### Starting deck roster

| Card ID | Name | Copies | Cost | Effect |
| --- | --- | ---: | ---: | --- |
| `swat` | Swat | 4 | 0 | 3 damage to enemy in facing adjacent tile |
| `arcane_yarn` | Arcane Yarn | 4 | 1 | 6 damage to first enemy in facing ray up to 4 tiles |
| `hiss` | Hiss | 2 | 0 | 1 damage to all enemies within Manhattan distance 3 |
| `purr_nap` | Purr Nap | 2 | 1 | Gain 5 Guard |

### Card reward pool roster: base Tier 1

| Card ID | Name | Cost | Target | Effect |
| --- | --- | ---: | --- | --- |
| `fireball` | Fireball | 1 | Ray range 6 | 8 damage to first enemy |
| `hairball` | Hairball | 1 | Nearest enemy | 3 damage ignoring walls |
| `yarn_shield` | Yarn Shield | 0 | Self | Gain 3 Guard |
| `nine_lives` | Nine Lives | 2 | Self | Heal 6 HP |
| `focus` | Focus | 0 | Self | Draw 2 cards, hand limit 7 |
| `static_meow` | Static Meow | 0 | Adjacent four tiles | 2 damage to enemies in up/down/left/right tiles |

### Persistent unlock roster

| Unlock ID | Trigger | Effect |
| --- | --- | --- |
| `yarn_plus` | Reach level 3 in any run | Add `arcane_yarn_plus` to reward pool for future runs |
| `lucky_paw` | Win the game | Add `lucky_paw` to starting deck for future runs |

| Unlocked Card ID | Name | Cost | Target | Effect |
| --- | --- | ---: | --- | --- |
| `arcane_yarn_plus` | Arcane Yarn+ | 1 | Ray range 4 | 8 damage to first enemy |
| `lucky_paw` | Lucky Paw | 0 | Self | Draw 1 card |

### Enemy roster

| Enemy ID | Name | HP | Move | Attack | Range | AI summary | Currency value | Levels |
| --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| `mouse` | Mouse Scout | 6 | 3 | 2 | 1 | Melee chase | 3 | 1-4, boss minions |
| `rat_mage` | Rat Mage | 8 | 1 | 4 | 2-4 orthogonal LOS | Keep distance, ranged attack, flee adjacent | 5 | 2-4 |
| `golem` | Golem Crate | 14 | 1 | 5 | 1 | Slow melee | 8 | 3-4 |
| `boss` | Archmage Doggo | 50 normal | 2 | 5 | 1 or LOS 8 | Move toward player, melee adjacent, ranged if LOS | 25 | 5 |

### Level roster

| Level | Name | Enemies normal | Hazards Tier 2 | Exit rule |
| ---: | --- | --- | --- | --- |
| 1 | Lobby of Bad Yarn | 2 Mouse | 0 | All enemies dead |
| 2 | Library of Loud Mice | 2 Mouse, 1 Rat Mage | 1 spike | All enemies dead |
| 3 | Kitchen of Cursed Cheese | 2 Rat Mage, 2 Golem | 1 spike, 1 lava | All enemies dead |
| 4 | Roof of Angry Pigeons | 1 Mouse, 2 Rat Mage, 2 Golem | 1 spike, 1 lava, 1 pit | All enemies dead |
| 5 | Throne of Archmage Doggo | Boss + 2 Mouse | 1 spike, 1 lava, 1 pit | Boss dead |

### Hazard roster

| Hazard ID | Name | Trigger | Damage | Movement effect |
| --- | --- | --- | ---: | --- |
| `spike` | Spike | Player enters tile | 1 | None |
| `lava` | Lava | Player enters tile | 2 | Player returns to previous tile |
| `pit` | Falling Pit | Player enters tile | `max(0, fallDistance - 1)` | Player falls down until floor |

### Shop item roster: Tier 2

| Item ID | Name | Cost | Effect |
| --- | --- | ---: | --- |
| `tonic` | Health Tonic | 12 | Heal 10 HP, capped at max |
| `max_hp` | Max HP Up | 20 | +5 max HP and heal 5 |
| `random_card` | Random Card | 18 | Add random card from reward pool |
| `remove_card` | Remove Card | 8 | Choose one owned card and remove it from deck |
| `trade_card` | Trade Card | 6 | Choose one owned card, remove it, gain random card |
| `reset_ability` | Reset Ability | 10 | Set ability cooldown to 0 |

Sell price for any card: 5 currency.

## 4.1 Combat

Tier: 1

### Turn structure

1. Player turn begins.
   - Increment `level.turn`.
   - Reset player `guard = 0`.
   - Reset player `energy = 3`.
   - Reset player `movePoints = 3` or difficulty value.
   - Tick ability cooldown if Tier 2.
   - Discard current hand.
   - Draw up to 5 cards.
2. Player acts until pressing End Turn or entering exit.
3. Player presses End Turn.
   - Play end-turn sound.
   - Resolve player end-of-turn effects if any.
   - All living enemies act in `uid` ascending order.
4. Next player turn begins.

### Player movement

- Player may move orthogonally one tile per input action.
- Each movement costs 1 move point.
- Movement is blocked by walls, the current tile, other enemies, and the player cannot move onto an enemy.
- Movement onto exit is allowed only if `exitLocked === false`.
- Movement updates `facing` to the movement direction.
- If move points are 0, movement inputs do nothing except play error sound.
- Cards may grant extra movement. Movement from cards does not cost move points.

### Facing

- Initial facing is `right`.
- Facing only changes on successful movement.
- Directional cards use facing.
- If a directional card has no valid target, it cannot be played.

### Damage

- All damage is integer.
- Damage to player:
  - First reduce `guard` by `min(guard, damage)`.
  - Remaining damage reduces `hp`.
- Damage to enemy:
  - Reduce enemy `hp`.
  - If `hp <= 0`, mark dead, remove from combat, award currency, spawn particles, play enemy death sound.
- Player death:
  - If `hp <= 0`, run `gameOver(ctx)`.
  - Permadeath: no continue, no revive.

### Guard

- Guard is a temporary combat state, not a separate system.
- Guard does not reduce incoming damage by itself; it absorbs damage.
- Guard resets to 0 at start of each player turn.
- Guard can be generated by cards or shop items only if specified.

### Enemy AI

All enemy AI uses BFS pathfinding on the grid. Enemies cannot move onto walls, the player, other enemies, or hazards unless the hazard is passable.

#### Mouse Scout

- If adjacent to player, attack for 2 damage.
- Else path toward player and move up to 3 tiles.
- If no path, do nothing.

#### Rat Mage

- If adjacent to player, try to move one tile away from player if possible.
- Else if player is within orthogonal range 2-4 and line of sight is clear, attack for 4 damage.
- Else path toward player and move up to 1 tile.
- Line of sight is blocked by walls only.

#### Golem Crate

- If adjacent to player, attack for 5 damage.
- Else path toward player and move up to 1 tile.

#### Archmage Doggo boss

- HP 50 normal, 40 easy, 60 hard.
- If adjacent, melee attack for 5 damage.
- Else if orthogonal line of sight within 8, ranged attack for 5 damage.
- Else path toward player and move up to 2 tiles.
- Does not use complex phases. The difficulty and HP make it the final test.

### Enemy damage scaling

- Easy: `Math.floor(base * 0.75)`
- Normal: `base`
- Hard: `Math.ceil(base * 1.25)`

## 4.2 Cards

Tier: 1

### Deck rules

- A run starts with the starting deck plus any persistent starting-card unlocks.
- Base starting deck size: 12.
- Card instances are unique by `uid`.
- When a card is played, it is moved to `discard` after resolution.
- At start of each player turn:
  - Move all `hand` cards to `discard`.
  - If `deck.length === 0`, shuffle `discard` into `deck` using deterministic RNG.
  - Draw until hand size is 5 or deck is empty.
- Hand limit is 7.
- Draw effects cannot exceed hand limit.

### Playing cards

- Player presses key `1` through `5` to play the corresponding hand slot.
- If the slot is empty, play error sound.
- If card cost > energy, play error sound.
- If card target is invalid, play error sound.
- On successful play:
  - Subtract cost from energy.
  - Resolve effect.
  - Move card to discard.
  - Play card sound.
  - Trigger visual effect.
- Card energy is not refunded if the effect fails for a reason other than invalid target.

### Targeting rules

- `self`: no target check.
- `adjacentFront`: one tile in facing direction. Valid only if an enemy is there.
- `ray`: starting one tile in facing direction, step until wall or range. First enemy is target. Walls block.
- `radiusManhattan`: all enemies with `abs(dx) + abs(dy) <= range`.
- `adjacentFour`: up, down, left, right adjacent tiles.
- `nearest`: enemy with smallest Manhattan distance. Tie-break by lower `y`, then lower `x`.

### Card effects

All card numbers are fixed except where difficulty affects enemy damage only.

| Card ID | Resolution |
| --- | --- |
| `swat` | Deal 3 damage to target adjacent front |
| `arcane_yarn` | Deal 6 damage to first target in ray range 4 |
| `hiss` | Deal 1 damage to all enemies in Manhattan radius 3 |
| `purr_nap` | Gain 5 Guard |
| `fireball` | Deal 8 damage to first target in ray range 6 |
| `hairball` | Deal 3 damage to nearest enemy, walls ignored |
| `yarn_shield` | Gain 3 Guard |
| `nine_lives` | Heal 6 HP up to max |
| `focus` | Draw 2 cards up to hand limit |
| `static_meow` | Deal 2 damage to enemies in four adjacent tiles |
| `arcane_yarn_plus` | Deal 8 damage to first target in ray range 4 |
| `lucky_paw` | Draw 1 card up to hand limit |

### Card rewards

- At end of each normal level, generate 3 distinct card choices from the reward pool plus unlocked cards.
- If the pool has fewer than 3 due to invalidation, allow duplicates from the remaining pool.
- Player selects with keys `1`, `2`, `3` or UI buttons.
- Selected card is added to `deck`.
- After selection, close modal and start next level.

## 4.3 Roguelike

Tier: 1

### Run start

- New run starts from Title or Game Over.
- `runSeed` is generated from OS entropy in normal play, or supplied by tests/debug.
- `run.level = 1`.
- Player is reset to base stats for selected difficulty.
- Deck is reset to starting deck plus persistent unlocks.
- Currency reset to 0.
- Persistent unlocks are loaded from storage.

### Level flow

- Level 1: 2 Mouse.
- Level 2: 3 enemies.
- Level 3: 4 enemies.
- Level 4: 5 enemies.
- Level 5: boss + 2 Mouse.
- After each normal level, open Level Clear modal and choose card reward.
- After level 5 boss is defeated, exit unlocks.
- Stepping on final exit calls `win(ctx)`.

### Exit locking

- Normal level exit locked until all enemy records in that level have `alive === false`.
- Boss level exit locked until boss record has `alive === false`.
- Locked exit renders grey dashed border and cannot be entered.
- Unlocked exit renders cyan swirl and can be entered.

### Permadeath

- When player HP reaches 0:
  - Stop enemy turns.
  - Play game over sound.
  - Set mode `game_over`.
  - Run state is cleared.
  - New run resets everything except settings and persistent unlocks.

### Persistent unlocks

- Unlock `reachedLevel3` when a run reaches level 3.
- Unlock `wonGame` when a run wins.
- Save to storage.
- Future runs use unlock effects listed above.

## 4.4 Procedural Generation

Tier: 1

### Seeding

- `runSeed` is 32-bit unsigned integer.
- Level seed: `hash32(runSeed, levelIndex, layoutAttempt)`.
- If generated layout fails validation, increment `layoutAttempt` and try again up to 32 times.
- If all attempts fail, use fallback layout.

### Fallback layout

- Open room with three horizontal platforms:
  - y 8, x 2..15
  - y 5, x 2..15
  - y 2, x 2..15
- Clear vertical path at x 1, x 8, x 16.
- Start `(1,10)`, exit `(16,1)`.

### Normal level generation

1. Fill grid with floor.
2. Set border walls.
3. Clear start pad at `(1,10)` and exit at `(16,1)`.
4. Place 7-10 horizontal platform segments:
   - Length 2-5.
   - y range 2-9.
   - x range 1-16.
   - Avoid start and exit tiles.
5. Place 4-8 wall obstacles:
   - Single tiles or 1×2 pillars.
   - Avoid start, exit, and a 3-tile radius around start.
6. Validate 4-direction path from start to exit.
7. If invalid, retry with next `layoutAttempt`.
8. Place enemies:
   - Candidate cells must be floor, not start, not exit, not within 3 tiles of start, not on other enemies.
   - Shuffle candidate cells deterministically.
   - Place according to level roster.
9. Tier 2: place hazards after enemies.

### Boss level generation

- Same normal generation.
- Boss spawn is always `(15,4)`.
- Two Mouse spawn on nearest valid cells to boss, at least 2 tiles away from each other.
- Exit remains locked until boss dies.

### Path validation

- Use BFS from start to exit.
- Walls block.
- Exit is considered passable only for validation.
- Hazards do not block path validation.

### Enemy placement difficulty adjustment

- Normal: use level roster.
- Easy: remove 1 random non-boss enemy, minimum 1 per level.
- Hard: add 1 random enemy from the level roster, minimum 1 per level.

## 4.5 Abilities

Tier: 2

### Familiar Dash

- Input: `Q` by default.
- No resource cost.
- Cooldown: 4 player turns.
- Activation:
  - If cooldown is not 0, play error sound and do nothing.
  - If no passable tile in facing direction, play error sound and do nothing.
  - Player moves up to 4 tiles in facing direction, stopping at wall.
  - If an enemy is in the path, player stops before the enemy and deals 1 damage to that enemy.
  - Set cooldown to 4.
- Cooldown decrements by 1 at start of each player turn.
- Ability state is shown on the ability button, not as a required HUD field.

### Ability rules

- Ability does not consume energy or move points.
- Ability cannot move through walls.
- Ability cannot move onto enemies.
- Ability does not trigger hazards during movement except if the final destination tile is a hazard.
- If final destination is lava, apply lava after ability movement.
- If final destination is spike, apply spike after ability movement.

## 4.6 Hazards

Tier: 2

### Hazard placement

- Level 1: 0 hazards.
- Level 2: 1 spike.
- Level 3: 1 spike, 1 lava.
- Level 4: 1 spike, 1 lava, 1 pit.
- Level 5: 1 spike, 1 lava, 1 pit.
- Easy difficulty disables hazards.
- Hard difficulty adds 1 additional spike or lava, not pit.
- Hazards cannot be placed on start, exit, enemies, or within 2 tiles of start.

### Spike

- Trigger when player enters the tile.
- Deal 1 damage.
- Player remains on the tile.
- Triggers every time entered.
- Enemies ignore spikes.

### Lava

- Trigger when player enters the tile.
- Deal 2 damage.
- Move player back to previous tile.
- If previous tile is invalid, keep player on lava but do not move.
- Enemies ignore lava.

### Falling Pit

- Trigger when player enters pit tile.
- Determine fall distance:
  - Starting from pit y + 1, move down until a solid floor or bottom border is reached.
  - `fallDistance = landingY - pitY`.
- Damage: `max(0, fallDistance - 1)`.
- Move player to landing tile.
- If landing tile is a hazard, do not chain-trigger that hazard during the same fall.
- Enemies ignore pits.

## 4.7 Economy

Tier: 2

### Currency earning

- Enemy kill:
  - Mouse: 3
  - Rat Mage: 5
  - Golem: 8
  - Boss: 25
- Level clear: +5
- Currency is integer and never negative.

### Shop

- Shop appears in Level Clear modal for levels 1-4.
- Generate 3 distinct shop offers from the shop item roster.
- Offers are deterministic using shop seed.
- Player can buy offers if currency is enough.
- Player can sell cards for 5 currency.
- Player can trade one owned card for a random card for 6 currency.
- Buying a card adds it to deck.
- Removing a card permanently removes it from the current run.

### Shop item rules

- `tonic`: heal 10, capped at max HP.
- `max_hp`: max HP +5, heal 5, capped at new max.
- `random_card`: add random card from reward pool plus unlocks.
- `remove_card`: open card list, choose one card, remove it.
- `trade_card`: choose one owned card, remove it, add random card.
- `reset_ability`: set `abilityCooldown = 0`.

### Sell rules

- Can sell any card in `deck`, `hand`, or `discard`.
- Sold card is removed permanently from current run.
- Cannot sell the last remaining card if deck would become empty? Allow empty deck. If deck and discard are empty and hand is empty, draw does nothing.

## Progression and difficulty

### Progression

- Level 1 teaches movement and basic attack.
- Level 2 introduces ranged enemy and first card reward.
- Level 3 introduces tankier enemies and hazards.
- Level 4 tests deck choices and positioning.
- Level 5 tests HP, Guard, and boss pattern.
- Card rewards are the main run progression.
- Economy shop is optional Tier 2 progression.

### Difficulty options

| Option | Player max HP | Player move points | Enemy damage | Enemy count | Boss HP | Hazards |
| --- | ---: | ---: | --- | --- | ---: | --- |
| Easy | 40 | 4 | 75% floor | -1 minimum 1 | 40 | Disabled |
| Normal | 30 | 3 | 100% | Normal | 50 | Normal |
| Hard | 20 | 2 | 125% ceil | +1 minimum 1 | 60 | +1 hazard |

### Session target

- Level 1: 2 minutes.
- Levels 2-4: 3-5 minutes each.
- Level 5: 6-8 minutes.
- Full run: 20-28 minutes.

### Feel

- Movement is snappy and readable.
- Card play gives immediate feedback: target highlight, hit flash, particles, shake, sound.
- Silly names and small cat details keep tone light.
- Death is abrupt and funny: game over shows a paw stamp and “Try a new tower.”
- The player should always know whose turn it is, how many actions remain, and what a card will do.

# 5. CHARACTERS

## Player: Wizard Cat “Mittens”

Silhouette: small round cat body, long tail, pointy wizard hat, robe. The hat breaks the cat silhouette enough to read as wizard cat.

| State / animation | Motion rule | When gameplay needs it |
| --- | --- | --- |
| `idle` | 4 frames, 8 fps, loop, tail sway | Always when alive and not moving |
| `walk` | 4 frames, 10 fps, loop while moving | Player move |
| `cast` | 6 frames, 12 fps, one-shot | Play any card |
| `dash` | 4 frames, 14 fps, one-shot | Tier 2 ability |
| `hit` | 2 frames, 100 ms, one-shot | Player takes damage |
| `death` | 8 frames, 12 fps, one-shot, fall into poof | Player dies |

Facings: up, down, left, right.

Gameplay states needed: `alive`, `dead`.

## Enemy: Mouse Scout

Silhouette: small mouse, tiny sword, triangular ears.

| State / animation | Motion rule | When gameplay needs it |
| --- | --- | --- |
| `idle` | 4 frames, 8 fps | Alive and not acting |
| `walk` | 4 frames, 10 fps | AI movement |
| `attack` | 3 frames, 12 fps, lunge | Melee attack |
| `hit` | 2 frames, 80 ms | Damage taken |
| `death` | 5 frames, 10 fps, poof | HP <= 0 |

Facings: left, right.

Gameplay states needed: `alive`, `dead`.

## Enemy: Rat Mage

Silhouette: taller rat, staff, pointy hat.

| State / animation | Motion rule | When gameplay needs it |
| --- | --- | --- |
| `idle` | 4 frames, 8 fps | Alive and not acting |
| `walk` | 3 frames, 8 fps | AI movement |
| `cast` | 5 frames, 12 fps, staff glow | Ranged attack |
| `hit` | 2 frames, 80 ms | Damage taken |
| `death` | 5 frames, 10 fps, poof | HP <= 0 |

Facings: left, right.

Gameplay states needed: `alive`, `dead`.

## Enemy: Golem Crate

Silhouette: wooden crate with two eyes and small arms.

| State / animation | Motion rule | When gameplay needs it |
| --- | --- | --- |
| `idle` | 2 frames, 4 fps, wobble | Alive and not acting |
| `walk` | 2 frames, 6 fps, heavy shuffle | AI movement |
| `attack` | 4 frames, 12 fps, slam | Melee attack |
| `hit` | 3 frames, 100 ms | Damage taken |
| `death` | 6 frames, 10 fps, break into planks | HP <= 0 |

Facings: left, right.

Gameplay states needed: `alive`, `dead`.

## Boss: Archmage Doggo

Silhouette: 32 × 32 dog in oversized wizard hat, staff, cape.

| State / animation | Motion rule | When gameplay needs it |
| --- | --- | --- |
| `idle` | 6 frames, 8 fps, cape flap | Alive and not acting |
| `walk` | 4 frames, 8 fps | AI movement |
| `attack` | 6 frames, 12 fps, bite | Melee |
| `cast` | 8 frames, 12 fps, bark wave | Ranged |
| `hit` | 3 frames, 100 ms | Damage taken |
| `death` | 10 frames, 12 fps, hat falls off, poof | HP <= 0 |

Facings: left, right.

Gameplay states needed: `alive`, `dead`.

# 6. AUDIO

All sounds are synthesized with square, triangle, sawtooth, or noise. Volumes are relative to `settings.volume`.

| Sound name | Recipe | When it plays |
| --- | --- | --- |
| `title_music` | Square lead, 120 bpm, chord progression I-V-vi-IV, simple arpeggio bass, loop | Title screen |
| `level_music` | Triangle bass, square melody, 132 bpm, loop | Levels 1-4 |
| `boss_music` | Fast square arpeggio, 150 bpm, chromatic riff, loop | Level 5 |
| `gameover_music` | Descending square arpeggio, 90 bpm, 2s sting | Game over |
| `win_music` | Major fanfare, square lead, 110 bpm, 3s sting | Win |
| `ui_move` | Square, 440 Hz to 660 Hz, 50 ms, volume 0.3 | Menu navigation |
| `ui_select` | Square, 880 Hz, 80 ms, volume 0.4 | Confirm menu choice |
| `ui_back` | Square, 220 Hz, 80 ms, volume 0.3 | Back/pause |
| `player_move` | Square, 300 Hz, 30 ms, volume 0.25 | Player moves one tile |
| `player_hit` | Sawtooth 120 Hz to 80 Hz plus noise burst, 120 ms, volume 0.5 | Player takes damage |
| `player_death` | Square descending 400 Hz to 100 Hz, 600 ms | Player dies |
| `card_draw` | Triangle, 660 Hz, 40 ms, volume 0.3 | Card drawn |
| `card_play` | Square 520 Hz to 780 Hz, 120 ms, volume 0.45 | Card played |
| `card_invalid` | Square 160 Hz, 80 ms, volume 0.35 | Invalid card play |
| `attack_swat` | Sawtooth 180 Hz to 120 Hz, 80 ms | Swat card |
| `attack_ray` | Square sweep 700 Hz to 1200 Hz, 120 ms | Ray cards |
| `attack_radius` | Noise burst filtered, 150 ms | Area cards |
| `guard_gain` | Triangle 440 Hz to 660 Hz, 160 ms | Guard card |
| `heal` | Triangle 523 Hz to 784 Hz, 220 ms | Heal card or tonic |
| `enemy_hit` | Square noise burst 1000 Hz, 80 ms | Enemy takes damage |
| `enemy_die` | Noise decay 800 Hz to 100 Hz, 300ms | Enemy dies |
| `enemy_attack` | Sawtooth 220 Hz to 160 Hz, 100 ms | Enemy attacks |
| `boss_cast` | Square sweep 300 Hz to 900 Hz, 250 ms | Boss ranged attack |
| `level_clear` | Square arpeggio C-E-G-C, 500 ms | Exit reached |
| `shop_open` | Square 660 Hz to 880 Hz, 160 ms | Shop opens |
| `buy` | Square 880 Hz to 1100 Hz, 120 ms | Purchase |
| `sell` | Square 1100 Hz to 880 Hz, 120 ms | Sell |
| `hazard_hit` | Sawtooth 200 Hz to 120 Hz, 120 ms | Spike/lava/pit |
| `ability_ready` | Triangle 784 Hz to 1046 Hz, 160 ms | Cooldown reaches 0 |
| `ability_cast` | Square sweep 400 Hz to 1200 Hz, 180 ms | Familiar Dash |

# 7. UX

All screens and HUD are HTML/CSS. The world is a DOM layer of absolutely-positioned sprite divs styled by CSS. JavaScript updates state, classes, and positions only.

## State machine

| State | Entry | Exit | Inputs |
| --- | --- | --- | --- |
| `boot` | Page load | `title` | None |
| `title` | `boot`, settings back | `game`, `settings` | Start, Settings, Confirm |
| `settings` | Title or Pause | Previous state | Difficulty, volume, reduced motion, remap keys, Back |
| `game` | New run, resume | `paused`, `level_clear`, `game_over`, `win` | Move, play card, end turn, ability, pause |
| `level_clear` | Exit reached on level 1-4 | `game` next level | Choose reward 1-3, shop controls, Confirm |
| `paused` | Pause during game | `game`, `settings`, `title` | Resume, Settings, Quit |
| `game_over` | Player HP <= 0 | `title`, `game` new run | New run, Title |
| `win` | Final exit entered after boss dead | `title` | Title |

## Default input map

| Action | Default keys |
| --- | --- |
| Move up | `W`, `ArrowUp` |
| Move down | `S`, `ArrowDown` |
| Move left | `A`, `ArrowLeft` |
| Move right | `D`, `ArrowRight` |
| Play card 1 | `1` |
| Play card 2 | `2` |
| Play card 3 | `3` |
| Play card 4 | `4` |
| Play card 5 | `5` |
| End turn | `Space` |
| Ability | `Q` |
| Pause | `Escape` |
| Confirm | `Enter` |
| Back | `Backspace` or `Escape` |
| Start run | `Enter` on title |
| Open settings | `S` on title |

## HUD table

| Element | Record field | When visible |
| --- | --- | --- |
| Health bar | `player.hp`, `player.maxHp` | `game`, `level_clear`, `paused` |
| Currency counter | `player.currency` | `game`, `level_clear`, `paused`, `game_over`, `win` |
| Turn indicator | `level.turn` | `game` |
| Move points pips | `player.movePoints` | `game` |
| Energy pips | `player.energy` | `game` |
| Hand card slots 1-5 | `player.hand` | `game` |
| Deck count | `player.deck.length` | `game` |
| Discard count | `player.discard.length` | `game` |
| Guard value | `player.guard` | `game` only if > 0 |
| Ability button | `player.abilityCooldown` | `game`, Tier 2 only |
| Level indicator | `run.level` | `game`, `level_clear`, `paused` |
| Card reward choices | `ui.reward.cardDefIds` | `level_clear` |
| Shop offers | `ui.shop` | `level_clear`, Tier 2 only |

## Settings screen

| Control | Record field | Rule |
| --- | --- | --- |
| Difficulty selector | `settings.difficulty` | Easy, Normal, Hard |
| Volume slider | `settings.volume` | 0.0 to 1.0 |
| Reduced motion toggle | `settings.reducedMotion` | Changes visual effects only |
| Colour-blind mode indicator | `settings.colorBlindSafe` | Always true; shown as enabled |
| Key remapper | `settings.keymap` | Capture one key per action |
| Reset defaults button | `DEFAULT_KEYMAP` | Restores defaults |

# 8. DEBUG API

| System | Function | Purpose |
| --- | --- | --- |
| Run | `debugRun.startRun(seed: number, difficulty: Difficulty): void` | Starts deterministic run |
| Run | `debugRun.completeLevel(): void` | Force current level complete |
| Run | `debugRun.nextLevel(): void` | Force next level |
| Run | `debugRun.gameOver(): void` | Force game over |
| Run | `debugRun.win(): void` | Force win |
| Procedural generation | `debugProcGen.generateLevel(levelIndex: number): void` | Regenerate current level |
| Cards | `debugCards.drawCards(n: number): void` | Draw cards |
| Cards | `debugCards.playCard(index: number): boolean` | Play hand card |
| Cards | `debugCards.addCard(defId: string): void` | Add card to deck |
| Combat | `debugCombat.applyEnemyDamage(amount: number): void` | Damage player |
| Combat | `debugCombat.applyPlayerDamage(uid: string, amount: number): void` | Damage enemy |
| Combat | `debugCombat.setPlayerHp(hp: number): void` | Set player HP |
| Enemies | `debugEnemies.spawn(defId: string, x: number, y: number): void` | Spawn enemy |
| Enemies | `debugEnemies.runTurn(): void` | Force enemy turn |
| Abilities | `debugAbilities.activate(): boolean` | Activate ability |
| Abilities | `debugAbilities.setCooldown(turns: number): void` | Set ability cooldown |
| Hazards | `debugHazards.place(type: HazardType, x: number, y: number): void` | Place hazard |
| Hazards | `debugHazards.activateAt(x: number, y: number): void` | Trigger hazard |
| Economy | `debugEconomy.addCurrency(amount: number): void` | Add currency |
| Economy | `debugEconomy.generateShop(): void` | Generate shop offers |
| Economy | `debugEconomy.buy(index: number): boolean` | Buy shop offer |
| Economy | `debugEconomy.sellCard(uid: string): boolean` | Sell card |
| Input | `debugInput.move(dx: number, dy: number): void` | Move player |
| Input | `debugInput.playCard(index: number): void` | Play card input |
| Input | `debugInput.endTurn(): void` | End turn input |
| Input | `debugInput.useAbility(): void` | Use ability input |
| UI | `debugUi.setMode(mode: Mode): void` | Force UI state |
| Settings | `debugSettings.set(key: keyof Settings, value: any): void` | Change settings |

# 9. TESTS

## Tier 1 tests

| Test | Validation |
| --- | --- |
| RNG determinism | Same seed produces same sequence and shuffled order |
| Level generation validation | For 100 seeds, every level has path from start to exit |
| Level enemy counts | Each level spawns correct count for difficulty |
| Player movement | Movement consumes move points, blocks walls, updates facing |
| Turn reset | End turn resets energy, move points, guard |
| Card draw | Start of turn discards hand and draws 5 |
| Deck shuffle | Empty deck shuffles discard |
| Card play | Energy is deducted, card moves to discard, effect resolves |
| Invalid card | Invalid target does not spend energy or move card |
| Damage | Enemy HP decreases, death removes enemy and awards currency |
| Guard | Guard absorbs damage before HP |
| Player death | HP <= 0 triggers game over and permadeath |
| Enemy AI | Mouse moves and attacks adjacent; Rat ranged attacks; Golem slow melee |
| Exit lock | Exit locked until all enemies dead |
| Boss exit lock | Final exit locked until boss dead |
| Run win | Entering final exit after boss dead triggers win |
| Run restart | Game over clears run, new run resets player and level 1 |
| Card reward | Level clear generates 3 distinct choices, selection adds card |
| Persistent unlock | Reaching level 3 and winning writes storage and affects future runs |
| HUD | Health and currency reflect player record |
| Screens | Title, pause, settings, game over, win reachable and render |
| Input remapping | Custom key triggers correct action |
| Difficulty | Easy/Hard change HP, damage, enemy count |
| Accessibility | Reduced motion disables shake/particles; colour-blind palette classes applied |

## Tier 2 tests

| Test | Validation |
| --- | --- |
| Ability activation | Q activates only when cooldown 0 |
| Ability cooldown | Cooldown decrements at start of player turn |
| Ability movement | Stops at walls/enemies, deals 1 damage if enemy blocks path |
| Spike | Entering spike deals 1 damage |
| Lava | Entering lava deals 2 and returns player |
| Pit | Falling pit deals correct damage and moves player |
| Hazard generation | Correct counts by level and difficulty |
| Currency earning | Enemy kill and level clear add currency |
| Shop generation | Three deterministic offers |
| Buy | Deducts currency and applies effect |
| Sell | Removes card and adds 5 currency |
| Trade | Removes selected card, adds random card, costs 6 |
| Reset ability | Sets cooldown to 0 |

## Tier 3 tests

None.

# 10. BUILD ORDER

1. Create project, HTML shell, CSS pixel font, fixed viewport.
2. Implement state, settings, storage, deterministic RNG.
3. Implement title, pause, settings, game over, win screens.
4. Implement input mapping and remapping.
5. Implement world DOM renderer for 18 × 12 grid.
6. Implement player sprite, movement, facing, move points.
7. Implement card data, deck, hand, draw, discard, energy.
8. Implement card play and basic targeting.
9. Implement combat damage, HP, Guard, death.
10. Implement enemy data, spawning, AI, enemy turns.
11. Implement procedural generation with path validation.
12. Implement level flow, exits, card rewards, win/lose.
13. Add pixel art sprites, animations, palette, effects.
14. Add chiptune music and retro bleeps.
15. Add HUD and accessibility options.
16. Add final boss.
17. Tune balance and run length.
18. Add Tier 2 ability.
19. Add Tier 2 hazards.
20. Add Tier 2 economy/shop.
21. Run all tests and fix tier failures.

# 11. DEFINITION OF DONE

## Tier 1: Core

High level: A player can start from the title, play five procedurally generated levels, use a deck of cards to fight enemies, reach the exit, defeat the final boss, win, die, and start a new run. The game is visually and audibly complete in the chosen style.

- [ ] State machine has title, settings, game, pause, game over, win.
- [ ] New run resets player, deck, level, currency.
- [ ] Player can move on grid, face direction, end turn.
- [ ] Player has HP, max HP, move points, energy, deck, hand, discard.
- [ ] Cards can be drawn, played, discarded, reshuffled.
- [ ] At least 12 starting cards are playable and balanced.
- [ ] Combat deals damage and kills enemies.
- [ ] Guard absorbs damage.
- [ ] Enemy AI acts for Mouse, Rat Mage, Golem.
- [ ] Procedural generation creates valid paths for 100 seeds.
- [ ] Five levels exist.
- [ ] Exits unlock correctly.
- [ ] Final boss exists and can be defeated.
- [ ] Win occurs after final exit.
- [ ] Death causes permadeath and game over.
- [ ] Card rewards appear and add cards.
- [ ] Persistent unlocks save and apply.
- [ ] HUD shows health and currency.
- [ ] HUD shows necessary card and turn controls.
- [ ] Pixel art, saturated palette, pixel font, chiptune, retro bleeps are present.
- [ ] Screen shake, particles, hit flash are present.
- [ ] Reduced motion disables shake/particles.
- [ ] Colour-blind safe palette is used.
- [ ] Difficulty options work.
- [ ] Key remapping works.
- [ ] Tests pass.

## Tier 2: Supporting mechanics

High level: Abilities, hazards, and economy are complete small additions on top of a finished Tier 1 game.

- [ ] Familiar Dash activates with Q and has 4-turn cooldown.
- [ ] Ability cooldown is visible and decrements.
- [ ] Spikes deal 1 damage.
- [ ] Lava deals 2 and pushes back.
- [ ] Pits cause fall damage.
- [ ] Hazards generate correctly by level and difficulty.
- [ ] Currency is earned from kills and level clear.
- [ ] Shop generates three deterministic offers.
- [ ] Buying, selling, trading, and reset ability work.
- [ ] Shop and economy do not break Tier 1 if disabled.
- [ ] Tests pass.

## Tier 3: Extra mechanics

High level: None. Do not add extra systems.

- [ ] No extra systems added.

# A. SANITY

| Check | Result | Notes |
| --- | --- | --- |
| All required headings present | Pass | Headings match requested order and names. |
| Core mechanics only in Tier 1 | Pass | Combat, cards, roguelike, procedural generation are Tier 1. |
| Supporting mechanics are Tier 2 | Pass | Abilities, hazards, economy are Tier 2. |
| Extra mechanics absent | Pass | Tier 3 is empty. |
| Tier 1 is playable and winnable | Pass | Five levels, final boss, exit, win state. |
| Tier 1 does not depend on Tier 2 | Pass | Currency is displayed in Tier 1 but spending/shop is Tier 2. Ability and hazards are Tier 2 only. |
| Required screens present | Pass | Title, pause, settings, game over, win. Technical `BOOT` is not a player screen. |
| Level clear does not violate screen list | Pass | Implemented as modal inside `game`, not a separate required screen. |
| Required HUD present | Pass | Health and currency. Extra card/turn UI is necessary for the required card mechanic. |
| Art/audio required from Tier 1 | Pass | Pixel art, palette, font, chiptune, bleeps, effects are Tier 1. |
| Accessibility required | Pass | Colour-blind palette, reduced motion, remappable keys, difficulty options. |
| Procedural generation deterministic | Pass | Seeded RNG, no `Math.random()`, testable. |
| Permadeath implemented | Pass | Death ends run, new run resets. |
| Session length under 30 minutes | Pass | Five levels with explicit time targets. |
| No unlisted systems added | Pass | Guard is part of combat; rewards/unlocks are part of cards/roguelike; shop is economy. |
| Numbers are concrete | Pass | HP, damage, costs, counts, cooldowns, shop prices, difficulty values are specified. |
| Input named and remappable | Pass | Keymap table and remapping rules. |
| Contracts include required fields | Pass | Global context includes all gameplay records. |
| Debug API one function per system | Pass | Each system has direct state functions. |
| Tests validate tiers | Pass | Tier 1 and Tier 2 test lists. |