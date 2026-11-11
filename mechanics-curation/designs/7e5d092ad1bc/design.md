# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Roguelike deckbuilder where you're a wizard cat climbing a tower | 4.1, 4.2, 4.3, 4.5, 5, 6, 7 |
| 2D | 1.1, 3, 4.1, 5 |
| Side-on camera | 1.1, 3, 5 |
| Turn-based time model | 1.1, 1.2, 4.1, 4.2, 4.3, 9 |
| Grid-based movement model | 1.1, 4.1, 4.2, 4.3, 7 |
| Session shape: a sequence of levels | 4.5, 4.9, 10, 11 |
| Failure: permadeath, start a new run | 4.3, 4.5, 7, 9, 11 |
| Tone: silly | 0.2, 4, 5, 6 |
| Size: a handful of levels, under 30 minutes | 0.2, 4.5, 4.9 |
| Win/lose: reach the exit, defeat a final boss | 4.3, 4.5, 7, 9 |
| Core mechanics: combat, cards, roguelike, procedural generation | 4.1-4.5, Tier 1 |
| Supporting mechanics: abilities, hazards, economy | 4.6-4.8, Tier 2 |
| Extra mechanics: none | 0.2, 0.3, A |
| Art style: pixel art: low-resolution sprites with visible square pixels and a limited palette | 1.1, 3, 5 |
| Palette: saturated: bright, strong colours | 3, 5 |
| Typography: pixel font: blocky bitmap letters | 3, 7 |
| Music: chiptune: retro console bleeps | 6 |
| Sound effects style: retro bleeps: synthesized chip sounds | 6 |
| Screens: title, pause, settings, game over, win | 7, 11 |
| HUD: health, currency | 7, 2.2 |
| Effects: screen shake, particles, hit flash | 3, 4.3, 6, 7 |
| Accessibility: colour-blind safe palette, reduced motion, remappable keys, difficulty options | 3, 4.9, 7, 11 |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| Player identity | Wisp, a small wizard cat in a pointy hat. Silly, readable, 16×16 pixel sprite. | Directly satisfies “wizard cat” and tone. |
| Run length | Exactly 5 levels: 4 normal tower floors + 1 final boss floor. Target total: 22-28 minutes at Normal. | “Handful of levels” and “under 30 minutes”. |
| Grid size | 24×14 tiles. Tile size: 16 px. Game viewport: 384×224. UI card area: 96 px below viewport. Base canvas/UI logical size: 480×320. | Small enough for quick procedural levels, side-on view, pixel art. |
| Camera | Fixed side-on camera. No scrolling. Entire level fits on screen. | Required side-on, keeps generation simple and readable. |
| Turn order | Player turn, then enemy turn. No initiative system. | Simple deckbuilder turn model. |
| Movement | Grid movement is card/ability driven. No free movement. Player uses targeting cursor with arrow keys. | Makes cards central to deckbuilding. |
| Player health | Start and max 40 HP on Normal. Block absorbs damage and is removed at start of next player turn. | Clear combat numbers. |
| Player energy | 3 energy per player turn. Energy resets each turn. | Standard deckbuilder pacing. |
| Starting deck | 10 cards: 4 Claw Strike, 4 Arcane Step, 2 Yarn Ward. | Gives immediate attack, movement, defense. |
| Draw rules | Draw to 5 cards at start of turn. Max hand 7. Discard hand at end of turn. Reshuffle discard into draw when draw pile empty. | Roguelike deckbuilder basics. |
| Deck cap | 15 cards. Rewards after levels 1-4 add one card each. Shop can remove cards. | Prevents unbounded deck. |
| Card rewards | After each normal level, choose 1 of 3 random cards from reward pool. | Deckbuilder progression. |
| Procedural generation | Deterministic seed-based generation. Same seed + settings = same level. | Roguelike fairness and testability. |
| Level generation | BSP-style room carving in 24×14 grid. 3-6 rooms. Corridors connect rooms. Start in leftmost room, exit in right/topmost room. Final level is a large arena with cover. | Enough variety without extra systems. |
| Enemies | Four normal enemy types + one final boss. Numbers fixed in 4. | Concrete combat content. |
| Hazards | Three hazard types: Spike Floor, Hex Tile, Arcane Coil. | Supporting mechanic, visible, numerical. |
| Pickups | Coin and Milk. | Economy and health content, no extra systems. |
| Economy | Coins from pickups/enemy drops. Altars on normal levels allow buying cards, removing cards, or healing. | Supporting economy without adding a top-level shop screen. |
| Abilities | Two active cat abilities: Purr Shield and Feline Leap. Unlocked by clearing levels, not required to finish. | Supporting mechanic, not a core dependency. |
| Final boss | Archmage Mouser, HP 70 Normal, summons minions, enters frenzy at low HP. | Satisfies “defeat a final boss”. |
| Win condition | Defeat boss, then stand on exit and press Enter. | Satisfies both “reach exit” and “defeat final boss”. |
| Lose condition | Player HP ≤ 0. Immediate game over. Run cannot continue. | Permadeath. |
| Screens | Exact top-level screens: title, pause, settings, game over, win. Level reward and altar are temporary in-game overlays, not new top-level screens. | Respects requested screen list. |
| HUD | Always shows Health and Currency. Currency is 0 until economy is built. | Required HUD without making economy a Tier 1 dependency. |
| Accessibility palette | Default palette is saturated but colour-blind safe: uses blue, orange, yellow, magenta, purple, white, black; avoids red/green as primary state encoding. | Required accessibility. |
| Reduced motion | Disables screen shake, replaces particles with short static flashes, reduces sprite animation to essential states. | Required accessibility. |
| Remappable keys | All actions remappable. Defaults listed in 4.9 and 7. | Required accessibility. |
| Difficulty options | Easy, Normal, Hard. Modify HP, damage, enemy count, boss HP. | Required accessibility. |
| Tone | Silly names, chiptune bleeps, cat puns, cartoon enemies. | Required tone. |
| Extra systems | None. No crafting, equipment, XP, meta-progression, save system, multiplayer, status effects beyond block, or extra screens. | Explicit “extra mechanics: none”. |
| Tier 1 art/sound | Tier 1 must already use pixel art, palette, pixel font, chiptune, bleep SFX, screen shake, particles, hit flash, HUD. | Required by prompt. |

## 0.3 Tiers

| Tier | Priority | Segment | Mechanics included | Definition of “enough” |
| --- | ---: | --- | --- | --- |
| Tier 1 | 1 | Core playable game | Combat, cards, roguelike, procedural generation, required screens, HUD health/currency, difficulty options, reduced motion, remappable keys, colour-blind safe palette, pixel art, chiptune, bleep SFX, effects. | A player can start a seeded run, play 5 procedurally generated levels, use cards to move and attack, defeat normal enemies and final boss, reach exit, win, or die and start a new run. No abilities, hazards, or economy spending. |
| Tier 2 | 2 | Supporting mechanics | Abilities, hazards, economy. | Purr Shield and Feline Leap work with cooldowns. Hazards appear and trigger. Coins, Milk, Altars, purchases, and deck removal work. Game remains finishable without them. |
| Tier 3 | 3 | Balance, accessibility, polish only | No new mechanics. | Tuning, more seeds, clearer feedback, accessibility refinements. No extra systems. |

---

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Concept | Value | Notes |
| --- | ---: | --- |
| Logical screen | 480×320 px | Base UI/canvas size. |
| Game viewport | 384×224 px | At x=0, y=0. |
| Card/UI strip | 480×96 px | At x=0, y=224. |
| Grid width | 24 tiles | x: 0-23 left to right. |
| Grid height | 14 tiles | y: 0-13 top to bottom. |
| Tile size | 16×16 px | All sprites/tiles are 16×16 unless noted. |
| Boss sprite | 32×32 px | Occupies one tile logically. |
| Player sprite | 16×16 px | One tile. |
| Normal enemy sprite | 16×16 px | One tile. |
| Camera | Fixed | No scrolling. |
| Facing | -1 = left, 1 = right | Side-on only. |
| Fixed timestep | 1/60 second | 60 fps logic step. |
| Turn | Discrete | No turn timer. |
| HP | Integer | Minimum 0. |
| Damage | Integer | Minimum 0. |
| Block | Integer | Max 30. |
| Energy | Integer | Max 3. |
| Hand size | Integer | Draw to 5, max 7. |
| Deck size | Integer | Start 10, max 15. |
| Coin | Integer | Display max 99; values above 99 clamp display to 99 but internal may exceed 99. |
| Cooldown | Player turns | Integer. |
| Screen shake | 4 px max amplitude | Disabled by reduced motion. |
| Particles | 8-16 per effect | Disabled/replaced by reduced motion. |
| Hit flash | 2 frames white overlay | Reduced motion: 1 frame opacity pulse. |
| Pixel font | 8 px bitmap | Blocky, 1px black outline. |

## 1.2 Important conventions

| Convention | Rule |
| --- | --- |
| Deterministic RNG | Use xorshift32. Seed is a 32-bit unsigned integer derived from user seed string. All generation, rewards, enemy placement, and random choices use this RNG. |
| RNG order | Generation runs before gameplay. Card rewards and enemy AI randomness use the same per-run RNG. Same seed + settings must produce same run. |
| No floating point gameplay state | Positions, HP, damage, energy, coins, cooldowns are integers. Animation interpolation may use floats only for rendering. |
| Pure gameplay state | Gameplay modules mutate state through exported functions. Rendering reads state only. No DOM access from gameplay modules. |
| Input is buffered once per frame | Input module converts key events into action actions. Gameplay consumes actions in fixed step. |
| Turn actions are atomic | A card or ability either fully resolves or is rejected before state changes. |
| Death is immediate | HP ≤ 0 sets entity dead. Dead entities cannot act, be targeted, or trigger effects. |
| Permadeath | Player death ends run. No continue, save, retry mid-run, or meta-progression. |
| Accessibility defaults | Colour-blind safe palette is default. Reduced motion default off. Difficulty default Normal. |
| Reduced motion | If enabled, screen shake amplitude = 0, particles = 0, hit flash = opacity pulse max 0.5 alpha for 1 frame, idle animation uses opacity only. |
| Colour-blind safe encoding | Never rely on red/green hue alone. Use shape, position, icon, and numeric text. |
| Pixel rendering | Canvas image smoothing disabled. All sprites drawn on integer pixel coordinates. |
| Sound | Use synthesized Web Audio or provided audio API. No sample packs required. |
| Settings persistence | Settings stored in `localStorage` under key `wizard_cat_settings_v1`. |
| No extra systems | Do not add crafting, equipment, XP, save, multiplayer, status effects, skill tree, map screen, or new top-level screens. |

---

# 2. CONTRACTS

## 2.1 Module layout

| File | Purpose | Tier |
| --- | --- | --- |
| `src/main.js` | Boot, game loop, screen router. | 1 |
| `src/config.js` | Constants: grid size, tile size, palette, default settings, keymap. | 1 |
| `src/rng.js` | Seed hashing, xorshift32 RNG. | 1 |
| `src/state.js` | Global context, state factory, reset run. | 1 |
| `src/settings.js` | Load/save settings, remappable keys, difficulty multipliers. | 1 |
| `src/generation.js` | Procedural level generation, reachability validation. | 1 |
| `src/cards.js` | Deck, draw pile, hand, discard, card play, rewards. | 1 |
| `src/combat.js` | Damage, block, death, enemy AI, turn order. | 1 |
| `src/abilities.js` | Active abilities, cooldowns. | 2 |
| `src/hazards.js` | Hazard placement, triggers, destruction. | 2 |
| `src/economy.js` | Coins, pickups, altars, purchases. | 2 |
| `src/input.js` | Keyboard mapping, action queue. | 1 |
| `src/render.js` | Canvas rendering, pixel art drawing, effects. | 1 |
| `src/audio.js` | Chiptune music and bleep SFX. | 1 |
| `src/ui.js` | DOM screens, HUD, overlays. | 1 |
| `src/debug.js` | Debug API. | 1 |
| `src/tests.js` | Self-tests. | 1 |

## 2.2 Global context

```ts
type Screen =
  | "title"
  | "settings"
  | "game"
  | "pause"
  | "gameOver"
  | "win";

type Difficulty = "easy" | "normal" | "hard";

interface KeyMap {
  moveCursorUp: string;
  moveCursorDown: string;
  moveCursorLeft: string;
  moveCursorRight: string;
  selectCard1: string;
  selectCard2: string;
  selectCard3: string;
  selectCard4: string;
  selectCard5: string;
  playSelected: string;
  endTurn: string;
  ability1: string;
  ability2: string;
  confirm: string;
  back: string;
  pause: string;
  exitLevel: string;
}

interface Settings {
  difficulty: Difficulty;
  reducedMotion: boolean;
  colorBlindSafe: boolean; // always true in default palette; toggle kept for future palette variants
  keyMap: KeyMap;
  musicVolume: number; // 0-1
  sfxVolume: number; // 0-1
}

interface Rng {
  state: number;
  next(): number; // 0 <= n < 1
  nextInt(min: number, max: number): number; // inclusive
  shuffle<T>(arr: T[]): void;
  pick<T>(arr: T[]): T;
}

interface Vec2 {
  x: number;
  y: number;
}

interface Entity {
  id: string;
  kind: string;
  x: number;
  y: number;
  facing: -1 | 1;
  hp: number;
  maxHp: number;
  block: number;
  move: number;
  attack: number;
  attackRange: number;
  alive: boolean;
  flags: {
    flying?: boolean;
    boss?: boolean;
    minion?: boolean;
    frenzy?: boolean;
  };
  aiState: "idle" | "moving" | "attacking" | "hurt" | "dying";
}

interface PlayerState extends Entity {
  energy: number;
  maxEnergy: number;
  maxHand: number;
  deck: string[];
  drawPile: string[];
  discardPile: string[];
  hand: string[];
  coins: number;
  unlockedAbilities: string[];
}

interface CardState {
  selectedCardIndex: number | null;
  selectedAbilityId: string | null;
  cursor: Vec2;
  targetValid: boolean;
}

interface LevelState {
  index: number; // 0-4
  width: number;
  height: number;
  tiles: Uint8Array; // 0 floor, 1 wall, 2 exit, 3 altar, 4 pickup, 5 hazard
  entities: Entity[];
  hazards: Hazard[];
  pickups: Pickup[];
  start: Vec2;
  exit: Vec2;
  altar: Vec2 | null;
  bossDefeated: boolean;
}

interface Hazard {
  id: string;
  type: "spike" | "hex" | "coil";
  x: number;
  y: number;
  hp: number;
  active: boolean;
  triggered: boolean;
}

interface Pickup {
  id: string;
  type: "coin" | "milk";
  x: number;
  y: number;
  amount: number;
  collected: boolean;
}

interface AbilityState {
  id: string;
  name: string;
  key: string;
  cost: number;
  cooldown: number;
  cooldownRemaining: number;
  unlocked: boolean;
}

interface EffectsState {
  shakeFrames: number;
  shakeAmplitude: number;
  particles: Particle[];
  hitFlashEntityId: string | null;
  hitFlashFrames: number;
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  color: string;
  kind: "spark" | "coin" | "heal" | "block";
}

interface UIState {
  overlay: null | "reward" | "altar" | "removeCard";
  rewardChoices: string[];
  altarMenu: string[];
  message: string;
  messageTimer: number;
}

interface GlobalContext {
  seed: string;
  rng: Rng;
  screen: Screen;
  settings: Settings;
  time: {
    frame: number;
    dt: number;
  };
  run: {
    startedAt: number;
    levelsCleared: number;
    deaths: number;
  };
  level: LevelState;
  player: PlayerState;
  cards: CardState;
  abilities: AbilityState[];
  economy: {
    coins: number;
    altarsUsed: number;
  };
  effects: EffectsState;
  ui: UIState;
  input: {
    actions: InputAction[];
    held: Record<string, boolean>;
  };
}
```

## 2.3 Module specifics

| Module | Required exports | Used by rule/test | Notes |
| --- | --- | --- | --- |
| `rng.js` | `hashSeed`, `createRng`, `xorshift32` | Determinism tests. | Must not use `Math.random` in gameplay. |
| `state.js` | `createInitialState`, `resetRun`, `startLevel` | All tests. | Builds player, empty level, default settings. |
| `settings.js` | `loadSettings`, `saveSettings`, `applyDifficulty`, `remapKey` | Accessibility and difficulty tests. | Defaults are deterministic. |
| `generation.js` | `generateLevel(levelIndex, rng, settings)`, `validateLevel(level)`, `bfsReachable(level, start, goal)` | Tier 1 generation tests. | Must guarantee start/exit reachable. |
| `cards.js` | `startPlayerTurn`, `drawTo`, `shuffleDiscard`, `playCard`, `discardHand`, `offerReward`, `addCardToDeck`, `removeCardFromDeck` | Card and deck tests. | Card IDs are strings. |
| `combat.js` | `endPlayerTurn`, `enemyTurn`, `damageEntity`, `applyBlock`, `killEntity`, `pathfind`, `lineOfSight` | Combat tests. | No floating point. |
| `abilities.js` | `unlockAbility`, `useAbility`, `tickAbilityCooldowns` | Tier 2 ability tests. | Uses same targeting rules as cards. |
| `hazards.js` | `placeHazards`, `triggerHazard`, `damageHazard`, `endTurnHazardEffects` | Tier 2 hazard tests. | Tier 1 can call no-op. |
| `economy.js` | `addCoin`, `collectPickup`, `placeAltar`, `openAltar`, `purchaseCard`, `purchaseHeal`, `purchaseRemove` | Tier 2 economy tests. | Tier 1 can call no-op. |
| `input.js` | `bindKeys`, `queueAction`, `consumeActions`, `remap` | Input tests. | Must respect `settings.keyMap`. |
| `render.js` | `drawFrame`, `drawLevel`, `drawPlayer`, `drawEnemies`, `drawCards`, `drawEffects` | Visual smoke tests. | Reads state only. |
| `audio.js` | `playSfx`, `playMusic`, `stopMusic`, `setVolume` | Audio smoke tests. | Synthesized only. |
| `ui.js` | `showScreen`, `updateHud`, `showReward`, `showAltar`, `hideOverlay` | UX tests. | HTML/CSS only. |
| `debug.js` | `debug` object | Debug and tests. | Reaches state directly. |
| `tests.js` | `runTests` | CI/manual validation. | Returns pass/fail list. |

---

# 3. VISUAL SPEC

The game looks like a tiny, saturated pixel-art tower: bright blue-violet stone, orange wizard-cat fur, cyan robot mice, magenta imps, yellow coin sparkles, and chunky 16×16 sprites with visible square pixels. Everything is drawn on a 480×320 logical surface, the game area is 384×224, and the hand of cards sits below it in a pixel-font card tray. The tone is silly: enemies look like household objects and mice in silly hats, traps are cartoonish, and UI text is short and goofy.

Lighting and atmosphere: flat pixel lighting with a dark indigo background and bright local highlights. No dynamic shadows. Walls have top-edge highlights. Hazards have animated warning pulses unless reduced motion is on. Hit effects use white flash, orange sparks, and cyan coin sparkles. The screen shake is short and punchy, never constant.

Space: fixed side-on grid. Background layers:
- Layer 0: dark indigo wall pattern.
- Layer 1: brighter purple wall blocks.
- Layer 2: blue floor tiles.
- Layer 3: hazards, pickups, exit portal.
- Layer 4: entities.
- Layer 5: particles and hit flashes.
- Layer 6: UI overlay.

Default 16-colour saturated palette:

| Role | Hex |
| --- | --- |
| Background dark | `#090312` |
| Background mid | `#180D2E` |
| Floor dark | `#244A8F` |
| Floor bright | `#3A73D9` |
| Wall dark | `#3A1B6B` |
| Wall main | `#6A35C0` |
| Wall highlight | `#9F5CFF` |
| Player main | `#FF9F1C` |
| Player highlight | `#FFD166` |
| White | `#FFFFFF` |
| Enemy cyan | `#22D3EE` |
| Enemy magenta | `#FF2E9A` |
| Enemy purple | `#A855F7` |
| Hazard orange | `#FF6B00` |
| Coin yellow | `#FFD60A` |
| Black | `#000000` |

Recipe table:

| Element | Visual recipe | Rule implied | Accessibility cue |
| --- | --- | --- | --- |
| Player | 16×16 orange cat, white hat, tiny staff, tail wag 2 frames. | Player entity. | Name label on hover/debug, numeric HP. |
| Normal enemy | Silhouette-only enemy, 16×16, one bright enemy colour. | Enemy HP/attack. | Shape differs per enemy; debug ID. |
| Boss | 32×32 purple robe, big hat, glowing staff. | Boss phase. | Large silhouette, boss name banner. |
| Wall | Purple block with black outline and top highlight. | Blocks movement/LOS. | Shape is explicit. |
| Floor | Dark blue tile with faint grid. | Walkable. | Grid cursor visible. |
| Exit | Yellow portal swirl, 16×16, 4-frame pulse. | Level exit. | Arrow glyph and text “EXIT”. |
| Altar | Coin bowl with yellow sparkles. | Economy. | Coin icon and text. |
| Spike Floor | Orange spikes, black base. | 3 damage on entry. | Spikes shape. |
| Hex Tile | Magenta tile with pulsing hex. | 2 damage at end of turn. | Hex glyph. |
| Arcane Coil | Cyan coil, HP bar. | Destructible obstacle. | HP bar. |
| Coin | Yellow coin, 2-frame spin. | +1 coin. | Coin shape. |
| Milk | White bottle, blue stripe. | +5 HP. | Bottle shape. |
| Cards | Rectangular pixel card, cost top-left, icon centre, text bottom. | Playable actions. | Numeric cost, keyboard number. |
| HUD health | Pink number and heart glyph. | Player HP. | Numeric text. |
| HUD currency | Yellow number and coin glyph. | Coins. | Numeric text. |
| Cursor | White 2px square with arrow. | Targeting. | Shape and colour. |
| Screen shake | Offset render by ±4 px for 120 ms. | Impact feedback. | Disabled in reduced motion. |
| Particles | 8-16 1-2px squares, lifetime 18-30 frames. | Hit/coin/heal feedback. | Disabled in reduced motion. |
| Hit flash | White overlay 2 frames. | Damage confirmation. | Short opacity pulse in reduced motion. |

---

# 4. GAMEPLAY SPEC

The player is Wisp, a wizard cat climbing five tower floors. Each floor is a fixed 24×14 side-on grid generated from a seed. The player has 40 HP, 3 energy, and a 10-card starting deck. Every turn the player draws 5 cards, spends energy to play cards that move, attack, defend, heal, or teleport, then ends the turn. Enemies then move and attack. The player clears normal floors by reaching the exit, choosing one card reward, and optionally using altars. The final floor contains Archmage Mouser; after defeating the boss, the exit activates. Death ends the run permanently.

## 4.0 Records and rosters

### Core records

| Record | Fields |
| --- | --- |
| `PlayerState` | id, kind, x, y, facing, hp, maxHp, block, move, attack, attackRange, alive, energy, maxEnergy, maxHand, deck, drawPile, discardPile, hand, coins, unlockedAbilities. |
| `Entity` | id, kind, x, y, facing, hp, maxHp, block, move, attack, attackRange, alive, flags, aiState. |
| `Card` | id, name, cost, targetType, range, effect, source, tier. |
| `LevelState` | index, width, height, tiles, entities, hazards, pickups, start, exit, altar, bossDefeated. |
| `Hazard` | id, type, x, y, hp, active, triggered. |
| `Pickup` | id, type, x, y, amount, collected. |
| `AbilityState` | id, name, key, cost, cooldown, cooldownRemaining, unlocked. |
| `EconomyState` | coins, altarsUsed. |
| `EffectsState` | shakeFrames, shakeAmplitude, particles, hitFlashEntityId, hitFlashFrames. |
| `UIState` | overlay, rewardChoices, altarMenu, message, messageTimer. |

### Player starting deck

| Card ID | Name | Cost | Target | Range | Effect | Count | Tier |
| --- | --- | ---: | --- | ---: | --- | ---: | --- |
| `claw_strike` | Claw Strike | 1 | Enemy | 1 | 4 damage | 4 | 1 |
| `arcane_step` | Arcane Step | 1 | Empty cell | 2 | Move there | 4 | 1 |
| `yarn_ward` | Yarn Ward | 1 | Self | 0 | Gain 5 Block | 2 | 1 |

### Card reward pool

| Card ID | Name | Cost | Target | Range | Effect | Source | Tier |
| --- | --- | ---: | --- | ---: | --- | --- | --- |
| `swift_paw` | Swift Paw | 1 | Empty cell | 3 | Move there | Reward | 1 |
| `arcane_bolt` | Arcane Bolt | 2 | Enemy in straight line | 5 | 6 damage, walls block | Reward | 1 |
| `blink` | Blink | 2 | Empty cell | 3 | Teleport there | Reward | 1 |
| `purr_heal` | Purr Heal | 2 | Self | 0 | Heal 6 HP | Reward | 1 |
| `fireball` | Fireball | 3 | Cell | 4 | 5 damage to target cell and adjacent cardinal enemies | Reward | 1 |

Reward choices: after Levels 0-3, offer 3 random distinct choices from the reward pool plus starting card IDs. Duplicates are allowed across offers but each offer has no duplicate IDs.

### Normal enemy roster

| Enemy ID | Name | HP Normal | Damage | Move | Attack range | Behaviour | Coin drop | Level counts |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| `squeakbot` | Squeakbot | 8 | 3 | 2 | 1 | Melee, pathfinds to player. | 1 | L0:3, L1:2, L3:2 |
| `hex_bat` | Hex Bat | 6 | 2 | 3 | 1 | Melee, ignores hazards, pathfinds through walls. | 1 | L1:2, L2:2 |
| `scroll_imp` | Scroll Imp | 10 | 4 | 2 | 4 | Ranged line-of-sight, moves if no target. | 2 | L2:3, L3:2 |
| `broom_golem` | Broom Golem | 16 | 5 | 1 | 1 | Slow melee, high HP. | 2 | L3:2 |

### Final boss roster

| Enemy ID | Name | HP Normal | Damage | Move | Attack range | Behaviour |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `archmage_mouser` | Archmage Mouser | 70 | 7 melee, 5 ranged | 2 | 1 melee, 5 ranged | Starts with 1 Squeakbot. At 50% HP summons 2 Squeakbots once. At 25% HP gains Frenzy: move +1, damage +2. |

### Hazard roster

| Hazard ID | Name | HP | Trigger | Effect | Placement | Tier |
| --- | --- | ---: | --- | --- | --- | --- |
| `spike` | Spike Floor | N/A | Player enters tile | 3 damage once, becomes broken. | Floor tiles, not start/exit. | 2 |
| `hex` | Hex Tile | N/A | End of player turn if player stands on it | 2 damage each time. | Floor tiles, not start/exit. | 2 |
| `coil` | Arcane Coil | 5 | Attacked | Destroyed, drops 1 coin. | Blocks corridor segments. | 2 |

### Pickup roster

| Pickup ID | Name | Amount | Effect | Tier |
| --- | --- | ---: | --- | --- |
| `coin` | Coin | 1 | +1 coin. | 2 |
| `milk` | Milk | 5 | +5 HP, capped at max HP. | 2 |

### Ability roster

| Ability ID | Name | Key default | Cost | Cooldown | Effect | Unlock | Tier |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| `purr_shield` | Purr Shield | Q | 2 | 5 | Gain 8 Block. | Clear Level 0. | 2 |
| `feline_leap` | Feline Leap | E | 2 | 6 | Move to empty cell within Manhattan distance 4, ignoring walls/hazards. Cannot land on occupied tile. | Clear Level 2. | 2 |

### Level content table

| Level | Name | Rooms | Start/exit distance | Normal enemies | Hazards | Pickups | Altar | Target time |
| ---: | --- | ---: | ---: | --- | --- | --- | --- | ---: |
| 0 | Toy Basement | 3 | ≥10 tiles | 3 Squeakbot | None | 2 coins | Yes | 2-3 min |
| 1 | Broom Cupboard | 4 | ≥12 tiles | 2 Squeakbot, 2 Hex Bat | 2 Spike | 4 coins, 1 milk | Yes | 4 min |
| 2 | Scroll Attic | 4 | ≥12 tiles | 2 Hex Bat, 3 Scroll Imp | 2 Spike, 1 Hex | 6 coins, 1 milk | Yes | 5 min |
| 3 | Cauldron Kitchen | 5 | ≥14 tiles | 2 Scroll Imp, 2 Broom Golem, 2 Squeakbot | 2 Spike, 1 Hex, 2 Coil | 8 coins, 2 milk | Yes | 5-6 min |
| 4 | Wizard’s Peak | 1 large arena | N/A | Boss + 1 Squeakbot | 2 Coil | None | No | 6-8 min |

## 4.1 Turn and grid input — Tier 1

| Rule | Number |
| --- | ---: |
| Player turn starts | Draw to 5, reset energy to 3, remove Block. |
| Player actions | Play cards, use abilities, end turn. |
| End turn | Discard hand, tick ability cooldowns, trigger end-turn hazards, run enemy turn, then start next player turn. |
| Targeting cursor | Starts at player position. |
| Cursor movement | Move cursor 1 tile per key press. |
| Card selection | Number keys 1-5 select hand slot. |
| Play selected | Space confirms if legal. |
| Cancel selection | Escape. |
| End turn | X. |
| Exit level | Stand on exit tile and press Enter. |
| Altar | Stand on altar tile and press Enter. |
| Pause | Escape. |
| Invalid action | Play invalid buzz, shake card 4px for 6 frames, no state change. |

## 4.2 Cards and deck — Tier 1

| Rule | Number |
| --- | ---: |
| Start deck | 10 cards. |
| Shuffle | Fisher-Yates using deterministic RNG at run start. |
| Draw pile | Start shuffled copy of deck. |
| Discard pile | Empty. |
| Draw | At player turn start, draw until hand size 5 or draw pile empty. |
| Empty draw pile | Shuffle discard into draw pile. |
| Both empty | Draw 0. |
| Play cost | Energy must be ≥ card cost. |
| Energy after play | Subtract cost. |
| Card after play | Move to discard pile. |
| Hand max | 7. If hand already ≥5 at start, draw 0. |
| Reward | After clearing Levels 0-3, add one chosen card to deck. |
| Remove card | Economy only, Tier 2. |
| Deck cap | 15. If at cap, rewards disabled. |

### Card targeting

| Target type | Legal target |
| --- | --- |
| Self | Always legal if cost paid. |
| Enemy | Alive enemy within range, line-of-sight if card requires it. |
| Empty cell | Within range, not wall, not occupied, not exit unless moving to exit is allowed. |
| Straight line enemy | Enemy on cardinal ray from player, no wall between, within range. |
| Cell AoE | Target cell within range, not wall. Affects enemies in target and adjacent cardinal cells. |

### Card effects

| Card ID | Resolution |
| --- | --- |
| `claw_strike` | Damage target enemy 4. |
| `arcane_step` | Move player to target empty cell. |
| `swift_paw` | Move player to target empty cell. |
| `yarn_ward` | Add 5 Block, cap 30. |
| `arcane_bolt` | Damage target enemy 6. |
| `blink` | Teleport player to target empty cell. |
| `purr_heal` | Heal 6 HP. |
| `fireball` | Damage target cell and adjacent cardinal enemies 5. |

## 4.3 Combat and enemies — Tier 1

| Rule | Number |
| --- | --- |
| Damage order | Enemy attack targets player. Block absorbs first. Remaining damage hits HP. |
| Player damage to enemy | Block is not used by normal enemies. |
| Block cap | 30. |
| Block removal | At start of player turn. |
| HP cap | Cannot exceed max HP. |
| Death | HP ≤ 0, alive=false, play death SFX, spawn death particles. |
| Player death | Screen goes to game over after 1 second death animation. |
| Enemy death | Remains as corpse sprite until end of turn, cannot be targeted. |
| Coin drop | On enemy death, spawn coin pickup at enemy tile if economy enabled; otherwise no drop. |
| Line-of-sight | Bresenham line from attacker to target. Walls block. Enemies do not block LOS. |
| Pathfinding | BFS to nearest tile adjacent to player. Max move steps = enemy move. |
| Enemy order | Entities in `level.entities` array order. |
| Enemy turn | For each alive enemy: attack if possible, else move, then attack if possible. |
| Enemy movement | Cannot move through walls. Hex Bat can move through hazards but not walls. Enemies cannot share tiles. |
| Enemy attack | Applies enemy damage. Plays hit flash and SFX. |
| Boss summon | At 50% HP, spawn 2 Squeakbots in adjacent empty cells if available. |
| Boss frenzy | At 25% HP, once: move +=1, melee damage +=2, ranged damage +=2. |
| Boss defeat | Sets `bossDefeated=true`, activates exit. |

## 4.4 Procedural generation — Tier 1

| Rule | Number |
| --- | ---: |
| Grid | 24×14. |
| Border | All border tiles are walls. |
| Rooms | Generate 3-6 rooms per normal level. Final level: 1 room 20×10 centred. |
| Room carving | Divide into 3×3 zones. Select zones. Room size 5-9 wide, 4-7 tall. |
| Corridors | Connect room centres with 1-tile corridors. |
| Start | Centre of leftmost room. |
| Exit | Centre of rightmost or topmost room. |
| Start/exit distance | Manhattan distance ≥ minimum from level table. |
| Reachability | BFS must prove start can reach exit without enemies. Retry up to 100 times. |
| Enemy placement | Not in start room. At least 4 tiles from start. Not on exit. |
| Altar placement | Centre of middle room, not on start/exit. |
| Hazard placement | Not on start/exit. Not required to reach exit. |
| Pickup placement | In dead ends or random empty floor, not on start/exit. |
| Final level | Boss at centre, exit behind boss. 2 Arcane Coils as cover. |
| Determinism | Same seed/settings produce same level. |

## 4.5 Run structure and rewards — Tier 1

| Step | Rule |
| --- | --- |
| Title | Enter seed or random. Start run. |
| Level 0-3 | Clear by standing on exit and pressing Enter. |
| Level complete | Show reward overlay, choose 1 of 3 cards. |
| Level 4 | Boss must be defeated before exit activates. |
| Win | Stand on activated exit and press Enter. |
| Lose | Player HP ≤ 0. |
| Permadeath | Game over screen. New run starts at title with new seed. |
| Stats on win/lose | Levels cleared, time, final deck size, coins. |
| Session cap | Target under 30 minutes. If a level takes >10 minutes, difficulty is considered too high; no auto-change. |

## 4.6 Abilities — Tier 2

| Rule | Number |
| --- | ---: |
| Ability input | Q = Purr Shield, E = Feline Leap. |
| Energy cost | Purr Shield 2, Feline Leap 2. |
| Cooldown tick | End of player turn, decrement by 1. |
| Ready | CooldownRemaining == 0. |
| Use blocked | If energy insufficient, cooldown active, or target illegal. |
| Purr Shield | Add 8 Block, cap 30. |
| Feline Leap | Target empty cell within Manhattan distance 4. Ignores walls/hazards during path. Cannot land on entities or exit unless allowed. |
| Unlock | Purr Shield after clearing Level 0. Feline Leap after clearing Level 2. |
| UI | Ability buttons show key, cost, cooldown remaining. |

## 4.7 Hazards — Tier 2

| Hazard | Trigger | Damage | Other |
| --- | --- | ---: | --- |
| Spike Floor | Player enters tile | 3 | Becomes broken after first trigger. Enemies ignore. |
| Hex Tile | End of player turn while player stands on it | 2 | Persists. Enemies ignore. |
| Arcane Coil | Attacked by any damage source | 5 HP | Destroyed, drops 1 coin if economy enabled. Blocks movement and LOS. |

Placement counts are in level table. Hazards never block the only path to exit.

## 4.8 Economy — Tier 2

| Rule | Number |
| --- | ---: |
| Coin pickup | +1 coin. |
| Enemy coin drop | Same as enemy roster. |
| Altar interaction | Stand on altar, press Enter. |
| Buy card | 12 coins. Adds random card from reward pool. Disabled if deck size 15. |
| Remove card | 10 coins. Opens deck removal list. |
| Buy heal | 6 coins. +15 HP, capped at max HP. |
| Coin cap | Internal no cap; display clamps at 99. |
| Altars | One per Level 0-3. Final level none. |
| Economy disabled | In Tier 1, no coins generated, no altars, HUD shows 0. |

## 4.9 Difficulty and accessibility — Tier 1 required

### Difficulty options

| Setting | Player max HP | Enemy HP | Enemy damage | Enemy count | Boss HP |
| --- | ---: | ---: | ---: | --- | ---: |
| Easy | 50 | floor × 0.75 | max(1, floor × 0.75) | table count -1, min 1 | 55 |
| Normal | 40 | unchanged | unchanged | table count | 70 |
| Hard | 35 | ceil × 1.25 | ceil × 1.25 | table count +1 | 85 |

### Accessibility options

| Option | Effect |
| --- | --- |
| Colour-blind safe palette | Default. Uses palette in 3. |
| Reduced motion | Disable shake, particles, idle animation except opacity. Hit flash becomes 1-frame opacity pulse. |
| Remappable keys | All actions remappable. Default keymap below. |
| Difficulty | Easy/Normal/Hard. |
| Text size | UI text minimum 8px bitmap; cannot go smaller. |
| Sound | Music and SFX volume sliders. |

### Default keymap

| Action | Default keys |
| --- | --- |
| Move cursor up | ArrowUp, W |
| Move cursor down | ArrowDown, S |
| Move cursor left | ArrowLeft, A |
| Move cursor right | ArrowRight, D |
| Select card 1 | 1 |
| Select card 2 | 2 |
| Select card 3 | 3 |
| Select card 4 | 4 |
| Select card 5 | 5 |
| Play selected | Space |
| End turn | X |
| Ability 1 | Q |
| Ability 2 | E |
| Confirm | Enter |
| Back | Escape |
| Pause | Escape |
| Exit level | Enter |
| Altar | Enter |

## 4.10 Progression and difficulty curve

| Level | Player capability expected | Enemy pressure | New content |
| ---: | --- | --- | --- |
| 0 | Basic attack/move/block. | 3 weak melee. | Card reward. |
| 1 | Add AoE/line/ranged options. | Flying enemy, spikes. | Hazard introduction. |
| 2 | Ranged threats, need positioning. | Ranged imps, hex tiles. | Ability Purr Shield. |
| 3 | Stronger enemies, tighter economy. | Tanks, ranged, mixed hazards. | Ability Feline Leap after clear. |
| 4 | Full deck, abilities optional. | Boss, phases, minions. | Win. |

Difficulty curve is intentionally forgiving up to Level 2, then requires deck choices. Hard mode mainly increases enemy HP/damage, not new mechanics.

## 4.11 Feel

- Card play should feel snappy: selection highlight within 1 frame, resolution within 2 frames.
- Movement should be clear: cursor shows destination, path flashes for 6 frames.
- Damage should be readable: numeric damage pops for 12 frames, target flashes white for 2 frames.
- Death should be silly: enemy explodes into toy parts, then poof.
- Boss phase transitions should be dramatic but not unfair: banner text, screen shake, music sting.
- Failure should be immediate and non-punitive: game over screen has stats and a clean New Run button.

---

# 5. CHARACTERS

## 5.1 Player: Wisp

| Property | Value |
| --- | --- |
| Silhouette | Small cat with pointy wizard hat, robe, tail, staff. |
| Sprite size | 16×16. |
| Palette | Orange main, yellow highlight, white hat, purple robe. |
| Facings | Left/right only. |
| States | `idle`, `moving`, `casting`, `hurt`, `dying`. |

### Animations

| Animation | Frames | Motion rule |
| --- | ---: | --- |
| Idle | 2 | Tail flick every 12 frames; hat bob every 16 frames. Reduced motion: static or 0.5 alpha pulse every 60 frames. |
| Move | 4 | 10 fps while moving 1 tile over 8 frames. |
| Cast | 2 | Staff raises 1 frame, glow 1 frame. |
| Hurt | 1 | White flash 2 frames, knockback 2px opposite damage. Reduced motion: opacity pulse 1 frame. |
| Die | 4 | 12 fps, hat falls off, poof. |

## 5.2 Squeakbot

| Property | Value |
| --- | --- |
| Silhouette | Robot mouse with wind-up key. |
| Sprite size | 16×16. |
| Palette | Cyan body, yellow key, white eyes. |
| Facings | Left/right. |
| States | `idle`, `moving`, `attacking`, `hurt`, `dying`. |

| Animation | Frames | Motion rule |
| --- | ---: | --- |
| Idle | 2 | Wind-up key spins slowly. |
| Move | 4 | 12 fps. |
| Attack | 2 | Lunge 4px, bite. |
| Hurt | 1 | White flash. |
| Die | 4 | Falls apart into gears. |

## 5.3 Hex Bat

| Property | Value |
| --- | --- |
| Silhouette | Bat with magic hat. |
| Sprite size | 16×16. |
| Palette | Magenta body, purple wings. |
| Facings | Left/right. |
| States | `idle`, `moving`, `attacking`, `hurt`, `dying`. |

| Animation | Frames | Motion rule |
| --- | ---: | --- |
| Idle | 2 | Hover bob 1px. |
| Move | 4 | Flap, 12 fps. |
| Attack | 2 | Swoop 5px. |
| Hurt | 1 | White flash. |
| Die | 4 | Poof into stars. |

## 5.4 Scroll Imp

| Property | Value |
| --- | --- |
| Silhouette | Small imp holding scroll. |
| Sprite size | 16×16. |
| Palette | Purple body, cyan scroll, white eyes. |
| Facings | Left/right. |
| States | `idle`, `moving`, `attacking`, `hurt`, `dying`. |

| Animation | Frames | Motion rule |
| --- | ---: | --- |
| Idle | 2 | Scroll trembles. |
| Move | 4 | 10 fps. |
| Attack | 2 | Casts magic bolt from scroll. |
| Hurt | 1 | White flash. |
| Die | 4 | Unrolls into scroll. |

## 5.5 Broom Golem

| Property | Value |
| --- | --- |
| Silhouette | Broom bundle with angry face. |
| Sprite size | 16×16. |
| Palette | Brown handled by purple/orange accents, white eyes. |
| Facings | Left/right. |
| States | `idle`, `moving`, `attacking`, `hurt`, `dying`. |

| Animation | Frames | Motion rule |
| --- | ---: | --- |
| Idle | 2 | Bristles sway. |
| Move | 2 | Stomp, 6 fps. |
| Attack | 2 | Swings broom. |
| Hurt | 1 | White flash. |
| Die | 4 | Bristles fly off. |

## 5.6 Archmage Mouser

| Property | Value |
| --- | --- |
| Silhouette | Tall mouse wizard with giant hat and staff. |
| Sprite size | 32×32. |
| Palette | Purple robe, cyan magic, yellow eyes. |
| Facings | Left/right. |
| States | `idle`, `moving`, `attacking`, `summoning`, `frenzy`, `hurt`, `dying`. |

| Animation | Frames | Motion rule |
| --- | ---: | --- |
| Idle | 2 | Staff glow pulse, hat sway. |
| Move | 4 | 8 fps. |
| Attack | 3 | Staff charge, slash/bolt. |
| Summon | 3 | Circle glyph, spawn poof. |
| Frenzy | 2 | Speed lines, faster idle. |
| Hurt | 1 | White flash. |
| Die | 5 | Hat deflates, poof, win sting. |

---

# 6. AUDIO

All audio is synthesized chiptune/bleeps. No samples required. Music loops seamlessly. Music volume and SFX volume are separate 0-1 sliders.

## 6.1 Music

| Track | Recipe | When plays |
| --- | --- | --- |
| `music_title` | Square lead: A4 440 Hz, C5 523 Hz, E5 659 Hz arpeggio; triangle bass: A2 110 Hz; noise hats: 8th notes; tempo 110 BPM. | Title screen. |
| `music_level1` | Square melody: C4/E4/G4, triangle bass C2, noise kick/snare, tempo 120 BPM. | Levels 0-1. |
| `music_level2` | Square melody: D minor, triangle bass D2, faster arpeggio, tempo 130 BPM. | Levels 2-3. |
| `music_boss` | Square lead: chromatic descending, sawtooth bass E1, noise fills, tempo 140 BPM. | Level 4. |
| `music_win` | Major fanfare: C-E-G-C, triangle bass, slow noise chime, 2 bars. | Win screen. |
| `music_lose` | Minor descending chromatic, triangle bass, slow noise, 2 bars. | Game over screen. |

## 6.2 Sound effects

| SFX name | Recipe | When plays |
| --- | --- | --- |
| `ui_move` | Square 220 Hz, 0.02s, quick decay. | Cursor move. |
| `ui_confirm` | Square 440→880 Hz, 0.06s. | Confirm button. |
| `ui_back` | Square 440→220 Hz, 0.06s. | Back button. |
| `card_select` | Square 660 Hz, 0.03s. | Select card. |
| `card_invalid` | Square 110 Hz, 0.08s, vibrato. | Illegal card/ability. |
| `card_play` | Square 880→1320 Hz, 0.08s. | Card resolves. |
| `move_step` | Triangle 180 Hz, 0.03s. | Player moves. |
| `attack_claw` | Noise burst + square 220 Hz, 0.1s. | Claw Strike. |
| `attack_bolt` | Square 1200→600 Hz, 0.12s. | Arcane Bolt. |
| `attack_fireball` | Noise sweep 100→400 Hz + square 300 Hz, 0.2s. | Fireball. |
| `enemy_hurt` | Square 440→220 Hz, 0.05s. | Enemy damaged. |
| `enemy_die` | Noise burst + square 600→100 Hz, 0.25s. | Enemy dies. |
| `player_hurt` | Square 220→110 Hz + noise, 0.15s. | Player damaged. |
| `block_gain` | Triangle 660→990 Hz, 0.12s. | Gain Block. |
| `coin` | Square 1046→1318 Hz, 0.08s. | Coin pickup. |
| `heal` | Sine 523→784 Hz, 0.18s. | Milk/Purr Heal. |
| `hazard_spike` | Noise 300 Hz, 0.1s. | Spike trigger. |
| `hazard_hex` | Square 150→100 Hz, 0.15s. | Hex damage. |
| `coil_break` | Noise sweep + square 500→150 Hz, 0.25s. | Arcane Coil destroyed. |
| `end_turn` | Triangle 330→220 Hz, 0.12s. | End turn. |
| `boss_roar` | Sawtooth 100→50 Hz, 0.5s. | Boss intro/phase. |
| `win` | Square fanfare C-E-G-C, 1.2s. | Win. |
| `lose` | Square minor descent, 1.2s. | Game over. |

---

# 7. UX

UI is HTML and CSS only for screens/HUD. The game viewport may be a `<canvas>` element, but all screens, buttons, HUD, and overlays are DOM elements styled with CSS. No external UI framework.

## 7.1 Screen state machine

| State | Entry | Visible UI | Actions |
| --- | --- | --- | --- |
| `title` | Boot or quit. | Title, seed input, New Run, Settings. | New Run → `game`; Settings → `settings`. |
| `settings` | From title or pause. | Difficulty, reduced motion, key remap, volume. | Back → previous screen. |
| `game` | New Run. | HUD, game viewport, card tray, overlays. | Pause → `pause`; death → `gameOver`; win → `win`. |
| `pause` | Escape during game. | Resume, Settings, Quit to Title. | Resume → `game`; Settings → `settings`; Quit → `title`. |
| `gameOver` | Player dies. | Stats, New Run, Title. | New Run → `game`; Title → `title`. |
| `win` | Exit after boss defeated. | Stats, New Run, Title. | New Run → `game`; Title → `title`. |

Game sub-overlays:

| Overlay | Trigger | Content | Exit |
| --- | --- | --- | --- |
| `reward` | Clear normal level. | 3 card choices. | Choose card → next level. |
| `altar` | Stand on altar, Enter. | Buy card, remove card, buy heal. | Escape or choose disabled. |
| `removeCard` | Altar remove card. | Deck list. | Confirm or Escape. |

## 7.2 HUD table

| UI element | Record field | When visible | Notes |
| --- | --- | --- | --- |
| Health number | `player.hp` / `player.maxHp` | `game`, `pause` | Top-left. Pink text, heart glyph. |
| Currency number | `player.coins` / `economy.coins` | `game`, `pause` | Top-right. Yellow text, coin glyph. Tier 1 shows 0. |
| Energy pips | `player.energy` / `player.maxEnergy` | `game` | Bottom card tray. Cyan pips. |
| Hand cards | `player.hand` | `game` | Bottom strip. Number keys shown. |
| Deck counts | `player.drawPile.length`, `player.discardPile.length` | `game` | Bottom corners. |
| Ability buttons | `abilities[]` | `game` if Tier 2 built | Shows key, cost, cooldown. |
| Targeting cursor | `cards.cursor` | `game` | White square. |
| Message toast | `ui.message` | `game` | Short silly warnings. |
| Reward overlay | `ui.rewardChoices` | `game` | Not a top-level screen. |
| Altar overlay | `ui.altarMenu` | `game` | Not a top-level screen. |

---

# 8. DEBUG API

| System | Debug function | Reaches |
| --- | --- | --- |
| RNG | `debug.rng.setSeed(seed)`, `debug.rng.getState()` | RNG state. |
| Generation | `debug.generation.generateLevel(index)` | Level state. |
| Cards | `debug.cards.state()`, `debug.cards.draw(n)`, `debug.cards.play(id, x, y)` | Deck/hand/card state. |
| Combat | `debug.combat.state()`, `debug.combat.damage(id, amount)`, `debug.combat.endTurn()` | Entities/turn. |
| Abilities | `debug.abilities.state()`, `debug.abilities.use(id, x, y)` | Ability cooldowns. |
| Hazards | `debug.hazards.state()`, `debug.hazards.place(type, x, y)` | Hazards. |
| Economy | `debug.economy.state()`, `debug.economy.addCoins(n)`, `debug.economy.purchase(option)` | Coins/purchases. |
| Player state | `debug.player.state()`, `debug.player.setHp(n)`, `debug.player.setEnergy(n)` | Player. |
| Input | `debug.input.press(actionName)`, `debug.input.moveCursor(dx,dy)`, `debug.input.selectCard(i)`, `debug.input.playSelected()`, `debug.input.endTurn()`, `debug.input.useAbility(i)` | Input actions. |
| Effects | `debug.effects.shake(frames, amplitude)`, `debug.effects.flash(entityId)`, `debug.effects.spawnParticles(kind, x, y)` | Effects. |
| UI | `debug.ui.showScreen(name)`, `debug.ui.showOverlay(name)` | Screen state. |

---

# 9. TESTS

| Tier | Test | Assertion |
| --- | --- | --- |
| 1 | RNG determinism | Same seed produces same random sequence. |
| 1 | Level generation determinism | Same seed/settings generates identical level for Levels 0-4. |
| 1 | Level reachability | Every generated level has BFS path from start to exit. |
| 1 | Start deck | Player starts with exactly 10 specified cards. |
| 1 | Draw rules | Start player turn draws to 5 unless hand already ≥5. |
| 1 | Reshuffle | Empty draw pile shuffles discard into draw. |
| 1 | Energy cost | Playing card subtracts exact energy. |
| 1 | Illegal card | Insufficient energy or illegal target causes no state change. |
| 1 | Claw damage | Target enemy HP decreases by 4. |
| 1 | Block | Yarn Ward adds 5 Block; damage reduces Block first. |
| 1 | Enemy AI | Enemy attacks when adjacent; otherwise moves toward player. |
| 1 | Line-of-sight | Walls block ranged attack. |
| 1 | Permadeath | Player HP ≤ 0 transitions to game over. |
| 1 | Final boss | Boss HP ≤ 0 sets `bossDefeated=true` and activates exit. |
| 1 | Win | Stand on activated exit and press Enter transitions to win. |
| 1 | Reward | Clearing Level 0 offers 3 card choices and adding one updates deck. |
| 1 | Settings | Remapped key triggers correct action. |
| 1 | Reduced motion | Shake amplitude forced 0 and particle count forced 0. |
| 1 | Difficulty | Easy/Hard modify HP/damage/count per table. |
| 2 | Purr Shield | Uses 2 energy, adds 8 Block, sets cooldown 5. |
| 2 | Feline Leap | Uses 2 energy, moves over walls, sets cooldown 6. |
| 2 | Spike damage | Player entering spike takes 3 once. |
| 2 | Hex damage | Player on hex at end turn takes 2. |
| 2 | Coil destruction | Coil takes 5 damage and is removed. |
| 2 | Coin pickup | Coin pickup increases coins by 1. |
| 2 | Altar purchase | Buy card costs 12 and adds card; remove card costs 10 and removes card; heal costs 6 and heals 15. |

---

# 10. BUILD ORDER

1. Set up fixed-step loop, canvas viewport, DOM screens, config constants.
2. Implement RNG, settings loading, difficulty, key remapping.
3. Implement global state and player record.
4. Implement grid rendering and fixed level.
5. Implement card data, deck, draw, hand UI, energy.
6. Implement targeting cursor and card play.
7. Implement combat: damage, block, death, enemy turn.
8. Implement procedural generation and reachability validation.
9. Implement 5-level run flow, rewards, exit, boss, win/lose.
10. Implement pixel art sprites, palette, animation, effects, HUD.
11. Implement chiptune music and bleep SFX.
12. Verify Tier 1 tests and definition of done.
13. Add abilities.
14. Add hazards.
15. Add economy coins, pickups, altars, purchases.
16. Add accessibility polish and balance tuning.
17. Run all tests.

---

# 11. DEFINITION OF DONE

## Tier 1 Done

High level: A player can play a complete seeded run from title to win or permadeath using only core mechanics.

- [ ] 480×320 logical layout renders.
- [ ] 24×14 grid renders as pixel art.
- [ ] Title, settings, game, pause, game over, win states work.
- [ ] Settings save and apply.
- [ ] Key remapping works.
- [ ] Reduced motion disables shake/particles.
- [ ] Colour-blind safe palette is default.
- [ ] Difficulty options apply.
- [ ] Player has 40 HP, 3 energy, 10 starting cards.
- [ ] Deck shuffles, draws, discards, reshuffles.
- [ ] Card selection, targeting, and resolution work.
- [ ] Energy cost enforced.
- [ ] Block works.
- [ ] Normal enemies have stats and AI.
- [ ] Final boss phases work.
- [ ] Levels 0-4 generate from seed and are reachable.
- [ ] Rewards after Levels 0-3 work.
- [ ] Exit requires boss defeat on Level 4.
- [ ] Player death ends run.
- [ ] HUD shows health and currency.
- [ ] Pixel font, chiptune, bleeps, shake, particles, hit flash work.
- [ ] Tier 1 tests pass.

## Tier 2 Done

High level: Supporting mechanics complete the game without becoming required for core completion.

- [ ] Purr Shield and Feline Leap unlock and work.
- [ ] Ability cooldowns tick correctly.
- [ ] Spike, Hex, and Coil hazards appear and trigger.
- [ ] Coin pickups and enemy drops work.
- [ ] Altars work in Levels 0-3.
- [ ] Purchases and deck removal work.
- [ ] Economy can be disabled without breaking Tier 1.
- [ ] Tier 2 tests pass.

## Tier 3 Done

High level: No new mechanics. Game feels balanced and accessible.

- [ ] All levels playable under 30 minutes on Normal.
- [ ] Hard/Easy are fair.
- [ ] No hidden untestable randomness.
- [ ] All debug functions work.
- [ ] Full test suite passes.

---

# A. SANITY

| Check | Result | Notes |
| --- | --- | --- |
| Core mechanics only | Valid | Tier 1 contains combat, cards, roguelike, procedural generation. |
| Supporting mechanics | Valid | Abilities, hazards, economy are Tier 2 and optional. |
| Extra mechanics | Valid | No extra mechanics added. No crafting, equipment, XP, meta progression, save, multiplayer, or status effects beyond block. |
| Required screens | Valid | Only title, pause, settings, game over, win are top-level screens. Reward and altar are in-game overlays, not new top-level screens. |
| HUD | Valid | Health and currency are always present; currency shows 0 in Tier 1. |
| Grid-based movement | Valid | Movement is tile-based via cards/abilities. |
| Turn-based | Valid | Player turn then enemy turn; no timers. |
| Side-on camera | Valid | Fixed 2D side-on viewport, no scrolling. |
| Permadeath | Valid | Player death ends run and returns to game over. |
| Win/lose | Valid | Final boss must be defeated, then exit must be used. Death loses. |
| Session length | Valid | 5 levels with target times under 30 minutes. |
| Procedural generation | Valid | Seed-based deterministic generation with reachability validation. |
| Numbers | Valid | HP, damage, energy, deck, coins, hazards, abilities, difficulty all numeric. |
| Art style | Valid | Pixel art, 16×16 sprites, visible pixels, limited saturated palette. |
| Typography | Valid | Pixel font specified in visual and UX. |
| Audio | Valid | Chiptune music and synthesized bleep SFX specified. |
| Effects | Valid | Screen shake, particles, hit flash specified with reduced-motion fallback. |
| Accessibility | Valid | Colour-blind safe palette, reduced motion, remappable keys, difficulty options specified. |
| Engineering contracts | Valid | Module layout, global context, required exports, debug API, tests included. |
| Tier 1 art/sound | Valid | Tier 1 definition includes pixel art, palette, music, SFX, effects, HUD. |
| No contradictions found | Valid | Sections 0-11 align: Tier 1 can finish without Tier 2 systems; final game includes required supporting systems. |