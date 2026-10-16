# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| One-button game | §1.2, §2.3, §4.1, §4.2, §7, §8 |
| Action is decided by how fast the player presses | §4.1 Tempo system, §4.2 Player actions, §7 HUD |
| Roguelike loop | §4.7 Room generation, §4.11 Relic system, §4.12 Shard economy, §4.13 Meta progression, §4.14 Progression |
| Permadeath | §4.13 Death and victory flow, §7 state machine |
| Procedural rooms | §4.7 Room generation, §2.3 `rooms` module |
| Random relics | §4.11 Relic system, §2.3 `relics` module |
| Meta progression between runs | §4.13 Meta progression, §2.3 `upgrades` / `save` modules |
| Five floors ending in a final boss | §4.6 Room structure, §4.10 Boss content, §4.14 Progression |
| Readable next action | §3 Visual spec, §4.1 HUD marker, §7 HUD table |
| Browser game, no build step | §1.2, §2.1 Module layout, §10 Build order |
| No hidden inputs, no hold, no direction | §1.2, §4.2, §7, §19 cut list in §4.17 |
| Side-view, single-lane space | §3 Space, §4.6 Room structure, §5 Characters |
| Heat / risk from fast input | §4.1 Tempo decay, §4.2 Parry and Flick, §4.3 derived stats |
| Distinguishable feedback for every core event | §4.15 Feel and pacing, §6 Audio, §7 UX |
| Accessibility without color-only cues | §3 Visual spec, §7 UX, §9 Tests |

## 0.2 Decisions

| # | Decision | Gameplay | Visual | Engineering | Ruling / Reasoning |
| ---: | --- | --- | --- | --- | --- |
| 1 | Final-boss victory trigger | Final boss death ends the run successfully. | Victory triggered when The Metronome dies. | Victory triggers when the player enters the final door. | **Ruling: final-boss death triggers Victory immediately** for Floor 5. Floors 1–4 still require entering the open door. Reason: gameplay and visual both say the final boss death is the victory moment; requiring a final door tap after the climax adds an unnecessary input and conflicts with the design fantasy. |
| 2 | Rendered tile size | Not specified. | 1 tile = 32px. | Fallback `tileSize = 48`. | **Ruling: default rendered tile size is 32px.** Asset manifest may override it. Reason: visual is binding for presentation, and 32px matches the specified HUD and entity sizes. Gameplay units remain tiles, not pixels. |
| 3 | Collision widths | Not explicit. | Player 0.8 wide, Chaser 0.8, Spiky 0.6, Shooter 0.8, projectile 0.3. | Player/enemy/barrier width 1.0, projectile width 0.5. | **Ruling: collision width is 1.0 tile for player, enemies, and barriers; 0.5 tile for projectiles.** Visual draw sizes remain as visual. Reason: single-lane blocking is simpler and fairer with uniform 1.0-tile collision boxes. |
| 4 | Continue from death/victory | “If shards > 0, go to Upgrade.” | “If shards earned > 0, go to Upgrade.” | If `save.shards > 0`, enter Upgrade. | **Ruling: use total spendable shards, `save.shards > 0`.** Reason: meta progression should be available whenever the player has spendable shards, including shards earned in previous runs. |
| 5 | Relic drop weights | Relics listed but no weights. | Rarity palette only. | 60 Common / 30 Rare / 10 Epic. | **Ruling: adopt 60/30/10 drop weights.** Reason: needed for procedural relics and matches intended build variety. |
| 6 | Clockwork relic behavior | After 3 Attacks, next Parry ignores cooldown; max 1 stack. | No extra rule. | Partial stack logic. | **Ruling: precise rule** — `clockworkAttackCounter` increments on every Attack action. When it reaches 3 and `clockworkStacks === 0`, set `clockworkStacks = 1` and reset counter to 0. A Parry performed while `parryCooldown > 0` consumes the stack. A Parry performed while ready does not consume the stack. Reason: removes ambiguity while preserving the designed “charged parry” feel. |
| 7 | Boss idle/recover timing | Boss patterns listed but no base timing. | Boss warnings ≥ 0.5s. | `idleInterval = 1.0`, `recoverTime = 0.5`; final boss phase 3 uses `0.7 / 0.3`. | **Ruling: adopt engineering timings.** Reason: makes bosses fair, testable, and deterministic. |
| 8 | Boss dash / piston distance | “Quick dash” / “lunges” without exact distance. | Visual lunges. | Fixed 4 tiles, clamped. | **Ruling: fixed 4-tile dash/piston movement.** Reason: deterministic and testable while still reading as a lunge. |
| 9 | Boss stomp trap placement | “Creates one spike trap in front of the player.” | Trap warning visual. | `x = round(player.x + 1)`, clamped to `3..room.width - 2`. | **Ruling: adopt engineering placement.** Reason: deterministic, avoids spawning on player start or door. |
| 10 | Enemy count capacity cap | Enemy count formula can exceed spacing capacity. | No rule. | Cap enemy count to valid spaced positions. | **Ruling: adopt capacity cap.** Reason: prevents invalid rooms and softlocks. |
| 11 | Room entry reset | Not explicit. | HUD should be predictable. | Reset Tempo, Parry cooldown, and i-frames on room entry. | **Ruling: adopt room-entry reset.** Reason: each room is a clean tactical state; carrying hidden heat or cooldowns is unfair and hurts readability. |
| 12 | Door lock conditions | Door locked until enemies dead and barriers broken. | Door states. | Boss also locks door; traps/relics/shards do not. | **Ruling: door opens when all enemies, barriers, and the boss, if present, are dead. Traps, relics, and shard piles never lock the door.** Reason: traps must have safe phases; letting traps lock the door can create timing softlocks. |
| 13 | Shooter firing fairness | Shooter fires projectiles. | Projectiles must be readable. | Shooter only fires if distance > 1.5 and no barrier blocks. | **Ruling: adopt Shooter fire rules.** Reason: prevents projectiles from spawning directly on the player with no reaction time. |
| 14 | HUD implementation | HUD requirements. | Detailed visual layout. | DOM HUD with required IDs. | **Ruling: HUD is DOM/CSS; world is canvas.** Reason: text, toasts, slots, and accessibility are easier in DOM. |
| 15 | Audio necessity | Requires distinguishable events. | Full SFX/music design. | Audio may no-op. | **Ruling: audio is nonessential. All critical information is visual. Audio APIs must no-op safely when unavailable.** Reason: game must be playable and testable with audio muted or missing. |
| 16 | Music and gameplay tempo | Tempo is player-driven. | Music BPM must not dictate player Tempo. | No music requirement. | **Ruling: music is adaptive but never forces player taps.** Reason: preserves the core skill of cadence. |
| 17 | Simulation stepping | Frame-based tempo decay. | No rule. | `update(dt)` clamps `dt` to 0.1. | **Ruling: canonical logical step is 1/60 s. `tick(dt)` substeps in 1/60 s chunks. `update(dt)` clamps each substep to 0.1 s.** Reason: keeps tests deterministic while supporting `tick(0.7)` style waits. |
| 18 | Save persistence | Meta progression. | No rule. | `localStorage` with in-memory fallback. | **Ruling: use `localStorage` when available; otherwise in-memory save.** Reason: headless/sandboxed environments must still run. |
| 19 | Tutorial hint wording | “Tap in the orange zone to attack”, “Quick triple-tap to parry”. | “Tap in the amber zone to attack”, “Burst taps to parry”. | Toast names. | **Ruling: use visual wording**: `Tap slowly to move`, `Tap in the amber zone to attack`, `Burst taps to parry`. Reason: matches the immutable amber action color and is more accurate than “triple-tap”. |
| 20 | Dropped visual extras | Not required. | Settings menu, minimap, room labels, enemy HP bars, hover, pause button are cut. | Not required. | **Ruling: drop settings menu, minimap, room labels, enemy HP bars except boss, hover, and pause button.** Reason: they compete with the Tempo marker or require extra input axes. |

## 0.3 Tiers

| Tier | Name | Included systems | Exit condition |
| ---: | --- | --- | --- |
| 1 | Core vertical slice | Config, RNG, save, input, Tempo, Move/Attack/Parry/Flick, player stats, damage, knockback, Floor 1 room generation, Chaser, Barrier, Spike trap, projectile, relic, shard, Boss 1, death, upgrade, title, basic HUD, fallback rendering, no audio. | A player can start a run, clear Floor 1, die or beat Boss 1, spend shards, and save state using one tap. Tier 1 tests pass. |
| 2 | Full five-floor roguelike | Floors 2–5, Spiky, Shooter, all enemy unlocks, floor scaling, Bosses 2–5, full room generation, victory flow, full procedural run. | A full seeded run can reach Floor 5 and trigger Victory. Tier 2 tests pass. |
| 3 | Visual identity | Floor palettes, character silhouettes, animations, particles, screen shake, telegraphs, accessibility cues, reduced motion, visual recipe table. | All floors render distinctly, all action states are visually distinguishable, and accessibility rules pass. Tier 3 tests pass. |
| 4 | Audio | Synthesized SFX, adaptive music, mixing, no-op audio safety. | All listed SFX can be triggered without exceptions, music states switch, and audio can be disabled safely. Tier 4 tests pass. |

---

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Quantity | Unit / value | Notes |
| --- | --- | --- |
| Position | tiles | `x` increases to the right. `y` is the single lane and is not simulated. |
| Rendered tile size | 32px default | Asset manifest may override. Gameplay always uses tiles. |
| Virtual resolution | 960 × 540 | Scaled to viewport with letterboxing. |
| Safe area | 16px inset | Critical UI stays inside safe area. |
| Time | seconds | `game.time` is the only gameplay clock. |
| Logical step | 1/60 s | `tick(dt)` substeps in 1/60 s chunks. |
| Max update substep | 0.1 s | `update(dt)` clamps each substep. |
| Tempo | 0–100 | Dimensionless. |
| Tempo gain per tap | +30 | Applied before action resolution. |
| Tempo decay | 30 per second base | Modified by relics/upgrades. |
| Speed | tiles/second | Enemies, projectiles, boss charges. |
| Distance | tiles | Movement, ranges, radii, knockback. |
| Damage | HP | 1 heart = 40 HP. |
| Cooldown | seconds | Parry, i-frames, upgrade timers. |
| Door transition | 0.2 s | After player overlaps open door. |
| Knockback tween | 0.1 s | Enemy knockback movement. |

## 1.2 Important conventions

- The implementation is vanilla HTML, CSS, and JavaScript only.
- No Node, npm, bundler, TypeScript, external runtime dependency, or build step.
- Scripts load as classic `<script>` files in the order defined in §2.1.
- All game code attaches to `window.Cadence`.
- The only allowed globals are:
  - `window.Cadence`
  - `window.__game`
  - `window.__test`
  - `window.__runTests`
  - `window.__testResults`
  - optional `window.CadenceAssets`
  - optional `window.CadenceTestMode`
- All gameplay randomness comes from `game.rng`, a seeded `mulberry32`-style RNG.
- Do not use `Math.random()` in gameplay logic.
- Do not use `Date.now()` or `performance.now()` for gameplay logic.
- Use `game.time` for all in-game timing.
- The only input is a tap:
  - pointer down anywhere,
  - `Space`,
  - `Enter`.
- Ignore:
  - key repeat,
  - pointer hold,
  - pointer release,
  - directional keys,
  - mouse wheel,
  - hover.
- Multiple taps in the same frame are queued and processed sequentially.
- Audio must no-op safely if unavailable.
- Rendering must no-op safely if canvas or assets are unavailable.
- Save storage must fall back to memory if `localStorage` is unavailable or throws.
- No visible on-screen button.
- No hover interaction.
- No pause button. Pause is an automatic flag inside `run`.

---

# 2. CONTRACTS

## 2.1 Module layout

| File | Responsibility | Tier |
| --- | --- | ---: |
| `index.html` | Loads runtime scripts and DOM shell. | 1 |
| `test.html` | Loads runtime scripts in test mode, then test harness and tests. | 1 |
| `css/style.css` | All CSS for HUD, overlays, scaling, accessibility. | 1/3 |
| `js/config.js` | All tunable constants. | 1 |
| `js/utils.js` | Math, interval, clamp, lerp helpers. | 1 |
| `js/rng.js` | Seeded RNG. | 1 |
| `js/save.js` | Persistent meta state and fallback. | 1 |
| `js/relics.js` | Relic definitions, drop weights, conversion values. | 1 |
| `js/upgrades.js` | Upgrade definitions and costs. | 1 |
| `js/entities.js` | Enemy, projectile, trap, barrier, relic, shard pile creation and updates. | 1 |
| `js/rooms.js` | Room/floor generation and validation. | 1/2 |
| `js/bosses.js` | Boss definitions, state machine, patterns, phases. | 1/2 |
| `js/input.js` | Tap binding and queue. | 1 |
| `js/audio.js` | Synthesized SFX/music, no-op safety. | 4 |
| `js/render.js` | Canvas world rendering and fallback. | 1/3 |
| `js/ui.js` | DOM HUD, toasts, overlays, state screens. | 1/3 |
| `js/game.js` | Core game state, update loop, Tempo, actions, flow. | 1 |
| `js/debug.js` | `window.__game` debug/test API. | 1 |
| `js/main.js` | Creates game, binds input, starts loop. | 1 |
| `js/test-harness.js` | Tiny synchronous test harness. | 1 |
| `js/tests.js` | Required tests. | 1/2/3/4 |
| optional `assets/manifest.js` | Optional sprite/audio manifest. | 3/4 |

## 2.2 Global context

The game instance is created by `Cadence.createGame(config)`. It is not exposed directly as a global; `window.__game` is the debug wrapper.

```js
const game = {
  version: 1,

  // Mode and timing
  mode: "title",            // "title" | "upgrade" | "run" | "death" | "victory"
  paused: false,            // only valid in "run"
  time: 0,                  // seconds
  rngSeed: 0,
  rng: null,                // seeded RNG instance

  // Input
  tapQueue: [],             // queued taps, processed sequentially

  // Persistent meta state
  save: {
    version: 1,
    shards: 0,
    upgrades: {
      vitality: 0,
      blade: 0,
      pulse: 0,
      ward: 0
    },
    bestFloor: 0
  },

  // Current spendable shards, kept in sync with save.shards
  shards: 0,

  // Player
  player: null,             // present during run/death/victory

  // Current room
  room: null,

  // World records
  enemies: [],
  projectiles: [],
  traps: [],
  barriers: [],
  relics: [],
  shardPiles: [],
  boss: null,

  // Upgrade state
  upgrade: null,

  // Run stats
  runStats: {
    shardsEarned: 0,
    enemiesKilled: 0,
    bossesKilled: 0,
    roomsCleared: 0
  },

  // Last resolved tap action
  lastAction: null,

  // Transient UI/world feedback
  toasts: [],               // internal: [{ text, ttl }]
  effects: [],               // internal: [{ id, type, x, y, ttl, data }]
  tutorialStep: 0,

  // Event log
  log: []
};
```

Player record:

```js
game.player = {
  x: 2,
  hp: 200,
  maxHp: 200,
  maxHearts: 5,

  tempo: 0,
  nextTempo: 0,
  nextAction: "move",       // "move" | "attack" | "parry" | "flick"

  parryCooldown: 0,
  parryCooldownMax: 0.8,
  iFrameTimer: 0,
  parryIFrameTimer: 0,

  moveDistance: 1.0,
  attackDamage: 15,
  parryDamage: 10,
  flickDamage: 2,
  attackRange: 1.5,
  parryRadius: 1.5,
  flickRadius: 1.0,
  tempoDecay: 30,
  echoChance: 0,
  thornDamage: 0,

  clockworkStacks: 0,
  clockworkAttackCounter: 0,

  relics: []                // relic IDs, max 5
};
```

Room record:

```js
game.room = {
  floor: 1,
  index: 0,                 // 0..4
  type: "combat",           // "combat" | "treasure" | "trap" | "boss"
  width: 16,
  doorX: 15,
  doorState: "locked",      // "locked" | "open"
  cleared: false,
  clearBonusGiven: false,
  tutorial: false,
  transitionTimer: 0        // 0..0.2
};
```

Enemy record:

```js
{
  id: 1,
  type: "chaser",           // "chaser" | "spiky" | "shooter"
  x: 8,
  hp: 30,
  maxHp: 30,
  speed: 2.0,
  fireTimer: 0,             // shooter only
  thornTimer: 0,
  kbTimer: 0,
  kbFrom: 0,
  kbTo: 0,
  width: 1.0
}
```

Projectile record:

```js
{
  id: 1,
  x: 10,
  vx: -4,
  owner: "enemy",           // "enemy" | "boss"
  width: 0.5
}
```

Trap record:

```js
{
  id: 1,
  x: 10,
  phase: "safe",            // "safe" | "warning" | "danger"
  timer: 1.0,
  safeDuration: 1.0,
  warningDuration: 0.5,
  dangerDuration: 0.4
}
```

Barrier record:

```js
{
  id: 1,
  x: 12,
  hp: 40,
  maxHp: 40,
  width: 1.0
}
```

Relic record:

```js
{
  id: 1,
  x: 13,
  relicId: "heavyCog"
}
```

Shard pile record:

```js
{
  id: 1,
  x: 9,
  amount: 10
}
```

Boss record:

```js
{
  id: 1,
  floor: 1,
  name: "Clockwork Golem",
  x: 18,
  hp: 250,
  maxHp: 250,
  state: "idle",            // "idle" | "telegraph" | "attack" | "recover"
  stateTimer: 1.0,
  pattern: null,
  phase: 1,
  shotQueue: [],            // [{ delay, fired }]
  attackTimer: 0,
  phaseTriggers: {},
  width: 1.0,
  kbTimer: 0,
  kbFrom: 0,
  kbTo: 0,
  isBoss: true
}
```

Upgrade record:

```js
game.upgrade = {
  cursor: 0,                // 0..4
  cursorTimer: 0,
  lastTapTime: -Infinity,
  autoReturnActive: false,
  autoReturnTimer: 0
};
```

Last action record:

```js
game.lastAction = {
  type: "move",              // "move" | "attack" | "parry" | "flick"
  blocked: false,
  tempoBefore: 0,
  tempoAfter: 30,
  damage: [
    {
      id: 1,
      amount: 15
    }
  ]
};
```

Toast record:

```js
{
  text: "Room cleared",
  ttl: 1.6
}
```

Effect record:

```js
{
  id: 1,
  type: "damageNumber",      // "damageNumber" | "particle" | "shake" | "flash"
  x: 0,
  y: 0,
  ttl: 0.5,
  data: {}
}
```

Log entry:

```js
{
  t: 0.0,
  event: "tap",
  data: {}
}
```

## 2.3 Module specifics

| Module | Required functions / exports | Notes |
| --- | --- | --- |
| `config` | `C.CONFIG` | All constants from §1.1 and §4. |
| `utils` | `clamp(v, min, max)`, `lerp(a, b, t)`, `intervalOverlap(a0, a1, b0, b1)`, `tileInterval(x, width)` | No randomness. |
| `rng` | `C.RNG.create(seed)` returning `next()`, `nextFloat(min, max)`, `nextInt(min, max)`, `chance(p)`, `pick(arr)`, `shuffle(arr)`, `weighted(items)` | Seeded deterministic RNG. |
| `save` | `C.save.default()`, `C.save.load(key)`, `C.save.write(save)`, `C.save.migrate(save)` | localStorage with memory fallback. |
| `relics` | `C.RELICS`, `C.relics.dropRelic(rng)`, `C.relics.conversionValue(rarity)`, `C.relics.name(id)` | Drop weights 60/30/10. |
| `upgrades` | `C.UPGRADES`, `C.upgrades.cost(level)`, `C.upgrades.maxed(save, id)` | Costs `[50, 100, 200, 400, 800]`. |
| `entities` | `createEnemy(type, x, floor, rng)`, `createProjectile(x, vx, owner)`, `createTrap(x, floor)`, `createBarrier(x, floor)`, `createRelic(x, relicId)`, `createShardPile(x, amount)`, `updateEnemy(enemy, dt, game)`, `updateProjectile(proj, dt, game)`, `updateTrap(trap, dt, game)`, `damagePlayer(game, hearts, source)`, `damageEnemy(game, enemy, amount, source)`, `damageBarrier(game, barrier, amount, source)`, `knockbackEnemy(game, enemy)` | Core simulation. |
| `rooms` | `C.rooms.generateFloor(floor, rng)`, `C.rooms.generateRoom(floor, index, type, rng)`, `C.rooms.validate(room)`, `C.rooms.findFreeTile(room, min, max, preferred)` | Validator returns string array. |
| `bosses` | `C.BOSSES`, `C.bosses.createBoss(floor, room, rng)`, `C.bosses.updateBoss(boss, dt, game)`, `C.bosses.startPattern(boss, pattern)`, `C.bosses.triggerPhase(boss, game)`, `C.bosses.bossDeath(boss, game)` | Boss state machine. |
| `input` | `C.input.bind(target, onTap)`, `C.input.queueTap(game)`, `C.input.drainQueue(game)` | One tap only. |
| `audio` | `C.audio.init()`, `C.audio.playSfx(name)`, `C.audio.setMusicState(state)`, `C.audio.setLayer(layer, level)`, `C.audio.duck(amount, ms)` | Must no-op safely. |
| `render` | `C.render.init(canvas)`, `C.render.resize()`, `C.render.draw(game)` | Fallback if canvas unavailable. |
| `ui` | `C.ui.bind()`, `C.ui.updateHUD(game)`, `C.ui.showToast(game, text)`, `C.ui.updateOverlay(game)` | DOM HUD. |
| `game` | `C.game.createGame(config)`, `game.update(dt)`, `game.tap()`, `game.processTap()`, `game.performMove()`, `game.performAttack()`, `game.performParry()`, `game.performFlick()`, `game.recomputePlayerStats()`, `game.enterMode(mode)`, `game.startRun(seed)`, `game.enterRoom(floor, index)`, `game.checkRoomClear()`, `game.updateDoorTransition(dt)`, `game.triggerDeath()`, `game.triggerVictory()`, `game.updateUpgrade(dt)`, `game.confirmUpgradeCard(index)`, `game.log(event, data)` | Core game. |
| `debug` | `C.debug(game)` returning `window.__game` API | Test seam. |
| `main` | `main()` | Creates game, binds input, starts loop. |
| `test-harness` | `window.__test.it`, `window.__test.assert`, `window.__test.assertClose`, `window.__test.assertDeep`, `window.__test.results`, `window.__runTests` | Synchronous tests. |
| `tests` | test definitions | See §9. |

---

# 3. VISUAL SPEC

**Look:** Cadence is a flat vector / low-detail 2D clockwork rhythm dungeon. The screen is dark, precise, and mechanical. The player is a small mechanical warden whose core color changes with the next action. The dungeon is built from gears, pistons, spikes, barriers, crystals, and metronome motifs. Every floor changes atmosphere, but the control language never changes: cyan is Move, amber is Attack, violet-white is Parry, gray is Flick, red is danger, and yellow is warning.

**Lighting and atmosphere:** Each floor uses a dark far background, a muted wall layer, and a brighter horizontal floor lane. The lane is the brightest horizontal band. Ambient particles are subtle and never resemble enemy projectiles. No ambient particle uses bright red. Floor 5 may use faint action-color accents, but the action palette remains dominant in UI and player feedback.

**Space:** The game uses a virtual 960 × 540 canvas, scaled to fit the viewport while preserving aspect ratio. One gameplay tile is one unit. The default rendered tile size is 32px. The playable space is a side-view single-lane corridor. The camera follows the player and clamps to the current room. The door is 1.5 tiles wide and 2 tiles tall. Room transitions use a short fade.

## Immutable action palette

| Meaning | Color | Hex | Usage |
| --- | --- | ---: | --- |
| Move / Cool | Cyan | `#3AE0FF` | Move zone, move feedback, move icon, low-tempo player core |
| Attack / Warm | Amber | `#FFB020` | Attack zone, attack slash, attack icon, mid-tempo player core |
| Parry / Hot | Violet-white | Core `#F4EDFF`, rim `#A855F7` | Parry zone, parry ring, parry icon, high-tempo player core |
| Flick / Failed Parry | Gray | `#9AA3B2` | Flick icon, flick spark, failed parry feedback |
| Danger | Red | `#FF4D4D` | Player damage, enemy projectiles, active traps, boss warnings |
| Warning | Yellow | `#FFD84D` | Trap warning phase, caution, unaffordable upgrade cost |
| UI Background | Near-black | `#0F1115` | Base UI background |
| UI Panel | Dark slate | `#1A1E26` | Toasts, cards, summary panels |
| UI Border | Slate | `#3A4150` | Panels, slots, bars |
| Primary Text | Off-white | `#F5F7FA` | Most text |
| Secondary Text | Light gray | `#A8B2C1` | Labels, subtext |
| Shards | Pale blue-white | `#DDE6FF` | Shard icon, shard count, shard particles |

## Floor palettes

| Floor | Theme | Far background | Wall | Floor | Accent | Ambient particles |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | Bronze Vault | `#17120D` | `#3A2B1E` | `#5A432C` | `#8A6B45` | Warm dust, `#D8B27A`, 15% opacity |
| 2 | Verdant Gearworks | `#0F1A16` | `#243B31` | `#345244` | `#5E8C70` | Green spores, `#9AD1B0`, 15% opacity |
| 3 | Amber Undercroft | `#140B06` | `#3A2214` | `#5C341A` | `#C47A32` | Embers, `#FF9A3C`, 12% opacity |
| 4 | Cobalt Machine | `#0A1118` | `#1F3040` | `#2E465A` | `#6E93A8` | Cool sparks, `#9AB8CC`, 12% opacity |
| 5 | Chromatic Metronome | `#08080C` | `#181820` | `#26262E` | `#F5F7FA` | White motes with faint action-color tints, 10% opacity |

## Rarity palette

| Rarity | Border / glow | Hex |
| --- | --- | ---: |
| Common | Neutral gray | `#B8C0CC` |
| Rare | Gold | `#FFD84D` |
| Epic | Magenta | `#FF7FE0` |

## Typography

| Element | Size | Weight |
| --- | ---: | ---: |
| Title logo | 48–64px | 800 |
| State title | 32–40px | 800 |
| Toast text | 16px | 600 |
| HUD text | 12–14px | 600 |
| Damage numbers | 14px | 700 |
| Upgrade card name | 16px | 700 |
| Upgrade card effect | 12px | 500 |
| Upgrade card cost | 14px | 700 |

Use:

```css
font-family: "Inter", "Roboto", "Helvetica Neue", Arial, sans-serif;
font-variant-numeric: tabular-nums;
```

## Visual recipe table

| Element | Recipe | Gameplay rule it encodes |
| --- | --- | --- |
| Tempo bar | 420px × 16px top center; zones: Move 0–39 cyan tint, Attack 40–69 amber tint, Parry 70–100 violet tint. Current Tempo is a subtle white fill. | Shows current Tempo and zones. |
| Next-tap marker | 24px circle, 12px downward pointer, 14px icon, white outline. Position: `barX + (nextTempo / 100) * barWidth`. | Marker shows exact result of next tap. |
| Move marker | Right arrow, cyan `#3AE0FF`. | Next tap moves. |
| Attack marker | Diagonal slash, amber `#FFB020`. | Next tap attacks. |
| Parry marker | Ring, core `#F4EDFF`, rim `#A855F7`. | Next tap parries if ready. |
| Flick marker | Broken ring, gray `#9AA3B2`. | Next tap flicks because Parry is unavailable. |
| Parry cooldown | Parry zone darkened, diagonal hatch, white sweep fills as cooldown recovers, white flash 200ms when ready. | Parry unavailable until sweep completes. |
| Player core | Circle color matches next action. Optional heat ring: radius 14px, stroke 2px, opacity 0.25 low Tempo to 0.5 high Tempo. | Player heat is readable. |
| Move visual | Player leans forward 8°, cyan dust puffs, 100ms tween. | Move action. |
| Blocked move | Player bumps forward 4px, gray dust puff, dull thud. | Move blocked. |
| Attack visual | Amber slash arc extends 1.5 tiles, lasts 120ms, amber sparks. | Attack hitbox. |
| Parry visual | White-violet ring expands to 1.5 tile radius over 200ms, player flashes white 100ms, 2px screen shake 100ms. | Parry i-frames and radius. |
| Flick visual | Small gray spark, 1.0 tile radius visual, lasts 80ms, no shake, no i-frame flash. | Flick is weaker than Parry. |
| Player damage | Player flashes red 100ms, red vignette 150ms, 4px screen shake 150ms, blink 8 times/sec during i-frames. | Player took damage. |
| Player death | Core shatters, white/red particles, desaturate 40% over 300ms, Tempo bar dims, transition after 600ms. | Run ended. |
| Chaser | Rounded bronze beetle, 0.8 × 0.7 tiles, white outline, two white eyes, low bob. | Contact enemy. |
| Spiky | Small spiked creature, 0.6 × 0.6 tiles, bone-white body, dark spikes, red eyes, jittery movement. | Faster weaker contact enemy. |
| Shooter | Gray turret, 0.8 × 0.8 tiles, dark barrel, red lens, barrel glows red 200ms before firing. | Ranged enemy. |
| Barrier | Gear wall, 1 × 1.2 tiles, bronze `#6B5233`, white outline, cracks at 75/50/25% HP. | Blocks movement and projectiles. |
| Spike trap safe | Flat gray grate `#5A6470`, no spikes. | Safe phase. |
| Spike trap warning | Spikes rise halfway, yellow `#FFD84D`, flashes 3 times over 0.5s, exclamation shape. | Warning phase. |
| Spike trap danger | Spikes fully extended, red `#FF4D4D`, no flash. | Active damage phase. |
| Projectile | Red orb `#FF4D4D`, white core, 0.3 tile visual diameter, 0.2s trail. | Enemy projectile. |
| Relic | 0.6 × 0.6 tile icon on pedestal, slow rotation, rarity glow. | In-run item. |
| Shard pile | 3–5 small crystals, `#DDE6FF`, slight bob, soft sparkle. | Shard currency. |
| Door locked | Closed metal door, dark gear lock, no light. | Room not clear. |
| Door unlocking | Gear lock spins, thin light seam grows over 300ms. | Door opening. |
| Door open | Door open, warm white light `#FFF3D6`. | Player can enter. |
| Boss telegraph | Boss flashes red, pattern-specific ghost dots/arrows, ≥0.5s before active damage. | Fair warning. |
| Boss phase | Boss flashes white 200ms, boss bar flashes white 200ms, toast `Phase 2` / `Phase 3`. | Boss phase change. |
| Victory | White-gold burst, screen brightens briefly, Metronome shatters. | Final boss defeated. |

## Visual rules ruled against gameplay

- The Tempo marker must show `nextTempo`, not current Tempo.
- The marker icon must change immediately when `nextTempo` crosses a zone boundary.
- While Parry is on cooldown, the Parry zone must be hatched and swept.
- If the marker is in the Parry zone while Parry is on cooldown, the marker must show Flick.
- Spike traps must visually distinguish safe, warning, and danger phases.
- Boss attacks must have at least 0.5 seconds of visual warning.
- Enemy projectiles must be visually distinct from player effects.
- Action colors are immutable across floors.
- No visual may compete with the Tempo marker.

---

# 4. GAMEPLAY SPEC

**Game in one paragraph:** Cadence is a one-button, tempo-based side-view roguelike. The player presses one button at different rates. The game converts recent press speed into Tempo, a value from 0 to 100. Low Tempo taps move the player forward, mid Tempo taps attack, and high Tempo taps parry. If the player presses too fast while Parry is unavailable, the tap becomes a weak Flick. The player advances through five procedurally generated floors of single-lane rooms, defeats one boss per floor, collects relics and shards, dies permanently, and spends shards on permanent upgrades between runs. The final boss is The Metronome.

## Records and rosters

| Record | Roster / values |
| --- | --- |
| Player | One player per run. |
| Enemies | Chaser, Spiky, Shooter. |
| Barriers | One barrier type, HP scales by floor. |
| Traps | Spike trap with safe/warning/danger phases. |
| Projectiles | Enemy and boss projectiles. |
| Relics | Metronome, Heavy Cog, Spring Boot, Thorn, Iron Latch, Echo, Ward, Pulse, Glass Heart, Clockwork. |
| Shard piles | 5–15 shards. |
| Bosses | Clockwork Golem, Gear Knight, Ritual Beast, Twin Pistons, The Metronome. |
| Upgrades | Vitality, Blade, Pulse, Ward. |
| Rooms | Combat, Treasure, Trap, Boss. |

## 4.1 Tempo system — Tier 1

Tempo is the abstraction of press speed.

| Constant | Value |
| --- | ---: |
| Max Tempo | 100 |
| Tempo gain per tap | +30 |
| Tempo decay | 30 per second |
| Move zone | 0–39 |
| Attack zone | 40–69 |
| Parry zone | 70–100 |
| Parry cooldown base | 0.8 s |

Every frame:

```ts
tempo = max(0, tempo - tempoDecay * dt)
parryCooldown = max(0, parryCooldown - dt)
```

On tap:

```ts
tempo = min(100, tempo + 30)

if tempo <= 39:
    performMove()
else if tempo <= 69:
    performAttack()
else:
    if parryCooldown <= 0 or clockworkStacks > 0:
        performParry()
    else:
        performFlick()
```

HUD marker value:

```ts
nextTempo = min(100, tempo + 30)
```

`nextAction`:

```ts
if nextTempo <= 39:
    nextAction = "move"
else if nextTempo <= 69:
    nextAction = "attack"
else:
    if parryCooldown <= 0 or clockworkStacks > 0:
        nextAction = "parry"
    else:
        nextAction = "flick"
```

## 4.2 Player actions — Tier 1

| Action | Tempo after tap | Effect | Tempo after action | Cooldown |
| --- | ---: | --- | ---: | ---: |
| Move | 0–39 | Advance forward by Move Distance | Unchanged | None |
| Attack | 40–69 | Forward melee attack | Unchanged | None |
| Parry | 70–100 | Defensive pulse with i-frames and knockback | Reset to 0 | 0.8 s base |
| Flick | 70–100 while Parry unavailable | Weak pulse | Reset to 0 | None |

### Move

- Base Move Distance: 1.0 tile.
- Maximum Move Distance: 1.5 tiles.
- Move is blocked by wall, barrier, enemy, or locked door.
- Tempo still changes even if move is blocked.
- Expected base movement rhythm: about 1.4 taps/sec.

### Attack

- Base Attack Damage: 15.
- Attack hitbox starts at player front and extends 1.5 tiles forward.
- Attack covers full lane height.
- Attack damages enemies and barriers in hitbox.
- Attack destroys projectiles in hitbox.
- Attack does not move the player.
- Attack does not reset Tempo.
- Attack does not knock enemies back.
- Echo relic may cause one extra hit per attack.

### Parry

- Grants 0.3 seconds of invulnerability.
- Base Parry Damage: 10.
- Base Parry radius: 1.5 tiles.
- Base Parry cooldown: 0.8 seconds.
- Damages enemies and barriers in radius.
- Knocks enemies back in radius.
- Destroys projectiles in radius.
- Resets Tempo to 0.
- Starts Parry cooldown.

### Flick

- Occurs when Tempo after tap is 70–100 and Parry is unavailable.
- Base Flick Damage: 2.
- Base Flick radius: 1.0 tile.
- Destroys projectiles in radius.
- No invulnerability.
- No knockback.
- Resets Tempo to 0.

## 4.3 Player stats — Tier 1

Base stats:

| Stat | Base value |
| --- | ---: |
| Max hearts | 5 |
| HP per heart | 40 |
| Max HP | 200 |
| Attack Damage | 15 |
| Parry Damage | 10 |
| Flick Damage | 2 |
| Move Distance | 1.0 tile |
| Attack range | 1.5 tiles |
| Parry radius | 1.5 tiles |
| Flick radius | 1.0 tile |
| Player i-frames after damage | 0.8 s |
| Parry i-frames | 0.3 s |
| Parry cooldown | 0.8 s |

Derived stats are recomputed when a relic is picked up, a relic is converted, an upgrade is purchased, or a new run starts.

```ts
maxHearts =
  5
  + save.upgrades.vitality
  + count(relics, "glassHeart")

maxHp = maxHearts * 40

attackDamage =
  15
  + save.upgrades.blade * 5
  + count(relics, "heavyCog") * 5

parryDamage =
  10
  + save.upgrades.pulse * 2
  + count(relics, "pulse") * 5

parryCooldownMax =
  clamp(
    0.8
    - save.upgrades.pulse * 0.1
    - count(relics, "ironLatch") * 0.15,
    0.4,
    1.0
  )

playerIFramesMax =
  clamp(
    0.8
    + save.upgrades.ward * 0.1
    + count(relics, "ward") * 0.2,
    0.1,
    1.2
  )

moveDistance =
  clamp(
    1.0 + count(relics, "springBoot") * 0.25,
    1.0,
    1.5
  )

tempoDecay =
  clamp(
    30
    - count(relics, "metronome") * 10
    + count(relics, "glassHeart") * 10,
    10,
    50
  )

echoChance =
  clamp(
    count(relics, "echo") * 0.25,
    0,
    0.5
  )

thornDamage =
  count(relics, "thorn") * 5

hasClockwork =
  count(relics, "clockwork") > 0
```

## 4.4 Damage and i-frames — Tier 1

- All normal enemy damage is 1 heart, or 40 HP.
- Damage sources:
  - enemy contact,
  - projectiles,
  - spike traps,
  - boss attacks.
- If player has active i-frames, damage is ignored.
- Player i-frames base: 0.8 s.
- Player i-frames maximum: 1.2 s.
- Parry i-frames: 0.3 s.
- Player damage sets `iFrameTimer = playerIFramesMax`.
- If HP reaches 0, trigger death.

## 4.5 Knockback — Tier 1

- Enemy knockback distance: 2 tiles.
- Knockback tween: 100 ms.
- Boss knockback: 50% of normal knockback.
- Barriers do not move.
- If knocked left off-screen:
  - `targetX < -1`,
  - enemy despawns after tween.
- Bosses are clamped to room bounds and do not despawn from knockback.

## 4.6 Room structure — Tier 1 / 2

A run has:

- 5 Floors.
- Each floor has 5 rooms.
- Room 4 is always the boss room.
- Player enters rooms from the left and exits through the door on the right.
- No backtracking.

Normal room width:

| Floor | Normal room width |
| ---: | ---: |
| 1 | 16–20 tiles |
| 2 | 18–22 tiles |
| 3 | 20–24 tiles |
| 4 | 22–26 tiles |
| 5 | 24–28 tiles |

Boss room width:

| Floor | Boss room width |
| ---: | ---: |
| 1 | 22 tiles |
| 2 | 24 tiles |
| 3 | 26 tiles |
| 4 | 28 tiles |
| 5 | 30 tiles |

Player starts at `x = 2`.

Door is at `x = room.width - 1`.

Room types:

| Type | Contents |
| --- | --- |
| Combat | Enemies, optional barrier, optional trap, optional relic, optional shard pile |
| Treasure | No enemies, 1–2 relics, 1–3 shard piles |
| Trap | No enemies, 2–3 spike traps, 1 relic |
| Boss | Boss, optional adds, no normal traps, no barriers |

Room sequence:

| Floor | Room 1 | Room 2 | Room 3 | Room 4 | Room 5 |
| ---: | --- | --- | --- | --- | --- |
| 1 | Combat tutorial | Treasure | Combat | Trap | Boss |
| 2 | Combat | Random | Random | Random | Boss |
| 3 | Combat | Random | Random | Random | Boss |
| 4 | Combat | Random | Random | Random | Boss |
| 5 | Combat | Random | Random | Random | Boss |

Random room weights:

| Room type | Weight |
| --- | ---: |
| Combat | 60% |
| Treasure | 25% |
| Trap | 15% |

If a floor has no Treasure room among rooms 2–4, room 3 becomes Treasure.

Door rules:

- Door is locked until:
  - all enemies are dead,
  - all barriers are broken,
  - if a boss exists, boss is dead.
- Traps, relics, and shard piles do not lock the door.
- When door opens:
  - add 10 room clear bonus once,
  - toast `Room cleared`,
  - emit `door_unlock`.
- If player overlaps open door:
  - start 0.2 s transition timer.
- If transition completes:
  - room index `< 4`: next room,
  - room index `4` and floor `< 5`: next floor,
  - room index `4` and floor `5`: Victory.

Camera:

- Follows player.
- Clamps to room bounds.
- Does not expose areas outside current room.

## 4.7 Room generation — Tier 1 / 2

Normal room width:

```ts
width = 14 + floor * 2 + randomInt(0, 4)
width = clamp(width, 14, 28)
```

Boss room width:

```ts
width = 20 + floor * 2
```

All placed objects use integer tile positions.

No object may be placed at:

- player start `x = 2`,
- door `x = room.width - 1`.

No two objects may occupy the same tile.

### Combat room generation

Enemy count:

```ts
enemyCount = min(8, 2 + floor + randomInt(0, 2))
```

Enemy spawn range:

```text
x = 8 to room.width - 4
```

Minimum enemy spacing: 2 tiles.

No enemy may spawn closer than 4 tiles from player start.

Capacity cap:

```ts
positions = []
for x = 8; x <= room.width - 4; x += 2:
    positions.push(x)

enemyCount = min(enemyCount, positions.length)
```

Optional combat content:

| Content | Chance |
| --- | ---: |
| Barrier | 20% |
| Spike trap | 30% |
| Relic | 30% |
| Shard pile | 50% |

Barrier placement:

- `x` between `10` and `min(16, room.width - 2)`.
- Not overlapping enemies.
- If no valid tile exists, skip barrier.

Trap placement:

- `x` between `8` and `room.width - 4`.
- Not overlapping enemies or barriers.
- If no valid tile exists, skip trap.

Relic placement:

- Preferred `x = room.width - 3`.
- If occupied, choose nearest free tile between `6` and `room.width - 2`.
- If no valid tile exists, skip relic.

Shard pile placement:

- Random free tile between `6` and `room.width - 2`.
- If no valid tile exists, skip shard pile.

### Treasure room generation

- No enemies.
- No traps.
- No barriers.
- 1–2 relics.
- 1–3 shard piles.

Relic placement:

- Prefer tiles near door:
  - `room.width - 3`,
  - `room.width - 4`,
  - `room.width - 5`.
- Choose distinct free tiles.
- If not enough free tiles, reduce relic count.

Shard pile placement:

- Random free tiles between `6` and `room.width - 2`.
- If not enough free tiles, reduce shard pile count.

### Trap room generation

- No enemies.
- No barriers.
- 2–3 spike traps.
- 1 relic.

Trap placement:

- `x` between `6` and `room.width - 2`.
- Not player start.
- Not door.
- Minimum spacing 3 tiles.

Use candidate positions:

```ts
for x = 6; x <= room.width - 2; x += 3:
    positions.push(x)
```

Choose up to 3 positions.

If not enough positions, reduce trap count.

Relic placement:

- Preferred `room.width - 3`.
- Otherwise nearest free tile.

### Boss room generation

- Width from boss table.
- Boss spawns at `x = room.width - 4`.
- Adds spawn between `x = room.width - 10` and `x = room.width - 5`.
- No traps.
- No barriers.
- Add positions must be distinct and not overlapping the boss.
- If not enough positions, reduce adds.

### Room validation

`C.rooms.validate(room)` must check:

1. `room.width` is within allowed bounds.
2. `room.doorX === room.width - 1`.
3. No object is at player start `x = 2`.
4. No object is at door `x = room.width - 1`.
5. No two objects occupy the same tile.
6. Combat enemies are within spawn range.
7. Combat enemies have minimum spacing 2.
8. Trap room traps have minimum spacing 3.
9. Treasure rooms have no enemies, traps, or barriers.
10. Trap rooms have no enemies or barriers.
11. Boss rooms have no traps or barriers.
12. Boss is at `room.width - 4`.
13. Boss adds are within allowed range.
14. Enemy types are unlocked for the floor.
15. Every enemy has positive HP.
16. Every barrier has positive HP.
17. Every trap has safe duration 1.0.

## 4.8 Difficulty scaling — Tier 2

Enemy HP:

```ts
enemyHP = baseHP * (1 + 0.15 * (floor - 1))
```

Enemy speed:

```ts
enemySpeed = baseSpeed * (1 + 0.05 * (floor - 1))
```

Projectile speed:

```ts
projectileSpeed = 4 + 0.5 * (floor - 1)
```

Spike trap danger duration:

```ts
dangerDuration = 0.4 + 0.05 * (floor - 1)
```

| Floor | Danger duration |
| ---: | ---: |
| 1 | 0.4 s |
| 2 | 0.45 s |
| 3 | 0.5 s |
| 4 | 0.55 s |
| 5 | 0.6 s |

Barrier HP:

```ts
barrierHP = 40 + 5 * (floor - 1)
```

| Floor | Barrier HP |
| ---: | ---: |
| 1 | 40 |
| 2 | 45 |
| 3 | 50 |
| 4 | 55 |
| 5 | 60 |

## 4.9 Enemy content — Tier 1 / 2

All enemies exist on the single lane.

### Chaser — Tier 1

Behavior:

- Moves toward player.
- Deals contact damage.
- No ranged attack.

Stats:

| Stat | Base value |
| --- | ---: |
| HP | 30 |
| Speed | 2.0 tiles/sec |
| Contact damage | 1 heart |
| Shards on death | 5 |

Unlocked: Floor 1.

### Spiky — Tier 2

Behavior:

- Faster, weaker chaser.
- Deals contact damage.

Stats:

| Stat | Base value |
| --- | ---: |
| HP | 20 |
| Speed | 3.0 tiles/sec |
| Contact damage | 1 heart |
| Shards on death | 8 |

Unlocked: Floor 3.

### Shooter — Tier 2

Behavior:

- Tries to keep distance.
- Fires projectiles at player.

Distance behavior:

- If distance to player is less than 3 tiles, moves away.
- If distance is greater than 5 tiles, moves toward player.
- Otherwise, stays in place.

Fire rules:

- Fires one projectile every 2.0 s.
- Only fires if distance to player is greater than 1.5 tiles.
- Only fires if no barrier is between shooter and player.

Stats:

| Stat | Base value |
| --- | ---: |
| HP | 45 |
| Speed | 1.0 tiles/sec |
| Projectile damage | 1 heart |
| Fire rate | 1 projectile / 2.0 s |
| Projectile speed | 4 tiles/sec base |
| Shards on death | 10 |

Unlocked: Floor 2.

### Barrier — Tier 1

Behavior:

- Stationary.
- Blocks player movement.
- Blocks enemy movement.
- Blocks projectiles.
- Can be damaged by Attack, Parry, and Flick.

Stats:

| Stat | Base value |
| --- | ---: |
| HP | 40, scales by floor |
| Shards on break | 15 |

Unlocked: Floor 1.

### Spike trap — Tier 1

Behavior:

- Covers 1 tile.
- Cycles between safe and dangerous.
- Deals 1 heart if player overlaps during danger.
- Does not block movement.

Cycle:

| Phase | Duration |
| --- | ---: |
| Safe | 1.0 s |
| Warning | 0.5 s |
| Danger | 0.4–0.6 s by floor |

The warning phase is visual only.

Unlocked: Floor 1.

## 4.10 Enemy unlock schedule — Tier 2

| Floor | Available enemies |
| ---: | --- |
| 1 | Chaser, Barrier, Spike trap |
| 2 | Chaser, Shooter, Barrier, Spike trap |
| 3 | Chaser, Spiky, Shooter, Barrier, Spike trap |
| 4 | Chaser, Spiky, Shooter, Barrier, Spike trap |
| 5 | Chaser, Spiky, Shooter, Barrier, Spike trap |

Enemy type weights for combat rooms:

| Floor | Chaser | Spiky | Shooter |
| ---: | ---: | ---: | ---: |
| 1 | 100% | 0% | 0% |
| 2 | 70% | 0% | 30% |
| 3 | 50% | 25% | 25% |
| 4 | 40% | 30% | 30% |
| 5 | 35% | 35% | 30% |

## 4.11 Boss content — Tier 1 / 2

Each floor ends with a boss.

Boss HP bar is displayed in HUD.

All boss attacks have at least 0.5 second warning before active damage.

Boss contact damage: 1 heart.

Boss attack damage: 1 heart.

Boss knockback: 50% of normal knockback.

Boss shard reward: 100 shards.

Boss base timings:

| Timing | Base | Final boss phase 3 |
| --- | ---: | ---: |
| Idle interval | 1.0 s | 0.7 s |
| Recover time | 0.5 s | 0.3 s |
| Telegraph | 0.5 s | 0.5 s |

Boss state machine:

```text
idle -> telegraph -> attack -> recover -> idle
```

### Floor 1 boss: Clockwork Golem — Tier 1

HP: 250.

Adds: None.

Patterns:

1. Charge
   - Warns for 0.5 s.
   - Moves left at 6 tiles/sec.
   - Target `x = 2`.
   - Stops at wall or barrier.

2. Stomp
   - Warns for 0.5 s.
   - Creates one spike trap in front of player.
   - Trap position: `x = round(player.x + 1)`.
   - Clamp to `3..room.width - 2`.
   - If occupied, choose nearest free tile.
   - New trap begins in safe phase.

3. Triple shot
   - Fires 3 projectiles.
   - Projectile spacing: 0.25 s.

Phase transition:

- At 50% HP, summon 2 Chasers.

### Floor 2 boss: Gear Knight — Tier 2

HP: 300.

Adds: 1 Shooter.

Patterns:

1. Dash left
   - Warns for 0.5 s.
   - Moves left 4 tiles.
   - Clamped to room bounds and barriers.

2. Double shot
   - Fires 2 projectiles.
   - Projectile spacing: 0.2 s.

Phase transition:

- At 50% HP, summon 1 Chaser.

### Floor 3 boss: Ritual Beast — Tier 2

HP: 350.

Adds: 2 Spikies.

Patterns:

1. Spiral shot
   - Fires 5 projectiles.
   - Projectile spacing: 0.15 s.

2. Charge
   - Same as Floor 1 charge.

Phase transitions:

- At 66% HP, summon 1 Spiky.
- At 33% HP, summon 1 Chaser.

### Floor 4 boss: Twin Pistons — Tier 2

HP: 400.

Adds: 2 Chasers.

Patterns:

1. Left piston
   - Warns for 0.5 s.
   - Moves left 4 tiles.

2. Right piston
   - Warns for 0.5 s.
   - Moves right 4 tiles.

3. Fan shot
   - Fires 4 projectiles.
   - Projectile spacing: 0.1 s.
   - Single-lane logic; visual may add slight vertical variation.

Phase transition:

- At 50% HP, spawn one barrier between boss and player.
- Barrier position: `x = round((player.x + boss.x) / 2)`, clamped to valid free tile.

### Floor 5 boss: The Metronome — Tier 2

HP: 500.

Adds: 2 Spikies.

Patterns:

1. Slow stomp
   - Creates a spike trap.

2. Medium charge
   - Charges across the room.

3. Fast burst
   - Fires 5 projectiles.
   - Projectile spacing: 0.1 s.

Phase thresholds:

| HP | Phase |
| ---: | --- |
| 100–66% | Slow stomp, medium charge |
| 66–33% | Adds fast burst |
| 33–0% | All patterns, faster timing |

Final boss death:

- Destroy all boss projectiles.
- Stop all enemies and projectiles.
- Trigger Victory immediately.

## 4.12 Relic system — Tier 1

Relics are in-run items.

Player can hold up to 5 relics.

If player picks up a relic while already at 5 relics:

- New relic is converted to shards.
- Conversion values:
  - Common: 10 shards
  - Rare: 20 shards
  - Epic: 30 shards

Relic pickup:

- Player overlaps relic.
- If space available:
  - add relic,
  - recompute stats,
  - toast `Relic acquired: [name]`.
- If no space:
  - convert to shards,
  - toast `Relic converted: +X shards`.

Relic drop weights:

| Rarity | Weight |
| --- | ---: |
| Common | 60 |
| Rare | 30 |
| Epic | 10 |

Relic list:

| Relic | Rarity | Effect |
| --- | --- | --- |
| Metronome | Common | Tempo decay -10 |
| Heavy Cog | Common | Attack Damage +5 |
| Spring Boot | Common | Move Distance +0.25 |
| Thorn | Common | Enemy contact deals 5 damage to the enemy, once per enemy per second |
| Iron Latch | Rare | Parry cooldown -150 ms |
| Echo | Rare | Attack has 25% chance to hit again |
| Ward | Rare | Player i-frames +200 ms |
| Pulse | Rare | Parry Damage +5 |
| Glass Heart | Epic | Max hearts +1, Tempo decay +10 |
| Clockwork | Epic | After 3 Attacks, the next Parry ignores cooldown. Max 1 stack. |

Stacking rules:

- Additive stats stack.
- Cooldown reductions cannot reduce Parry cooldown below 400 ms.
- Tempo decay cannot go below 10/sec.
- Tempo decay cannot go above 50/sec.
- Move Distance cannot exceed 1.5 tiles.
- Player i-frames cannot exceed 1.2 seconds.
- Echo chance cannot exceed 50%.
- Glass Heart can stack max hearts, but each copy also increases Tempo decay.

Clockwork precise rule:

- `clockworkAttackCounter` increments on every Attack action.
- When counter reaches 3 and `clockworkStacks === 0`:
  - set `clockworkStacks = 1`,
  - reset `clockworkAttackCounter = 0`.
- If `clockworkStacks === 1`, further attacks do not increase counter.
- If a Parry is performed while `parryCooldown > 0`:
  - consume `clockworkStacks`,
  - perform Parry,
  - set `parryCooldown = parryCooldownMax`.
- If a Parry is performed while `parryCooldown <= 0`:
  - perform Parry normally,
  - do not consume stack.

## 4.13 Shard economy — Tier 1

Shards are the meta currency.

Shards are kept after death or victory.

| Source | Shards |
| --- | ---: |
| Chaser kill | 5 |
| Spiky kill | 8 |
| Shooter kill | 10 |
| Barrier break | 15 |
| Room clear bonus | 10 |
| Boss kill | 100 |
| Shard pile | 5–15 |
| Death bonus | 50 |
| Victory bonus | 200 |
| Full relic slot conversion | 10 / 20 / 30 |

Expected run income, approximate:

| Outcome | Shards |
| --- | ---: |
| Floor 1 run | 150–250 |
| Floor 2 run | 200–350 |
| Floor 3 run | 250–400 |
| Floor 4 run | 300–500 |
| Full victory | 800–1200 |

## 4.14 Meta progression — Tier 1

Meta progression happens between runs.

The player keeps:

- Shards.
- Upgrade levels.
- Best floor reached.

The player loses:

- Relics.
- Run HP.
- Run position.

Upgrade tracks:

| Upgrade | Effect per level |
| --- | --- |
| Vitality | +1 max heart |
| Blade | +5 Attack Damage |
| Pulse | -100 ms Parry cooldown and +2 Parry Damage |
| Ward | +100 ms player i-frames |

Base to maximum:

| Upgrade | Base | Max |
| --- | ---: | ---: |
| Vitality | 5 hearts | 9 hearts |
| Blade | 15 Attack Damage | 40 Attack Damage |
| Pulse | 0.8 s cooldown / 10 Parry Damage | 0.4 s cooldown / 20 Parry Damage |
| Ward | 0.8 s i-frames | 1.2 s i-frames |

Upgrade costs:

| Level | Cost |
| ---: | ---: |
| 1 | 50 |
| 2 | 100 |
| 3 | 200 |
| 4 | 400 |
| 5 | 800 |

Total cost per track: 1550 shards.

Total cost to max all four tracks: 6200 shards.

### Upgrade state — Tier 1

The Upgrade state uses one button but does not use run Tempo.

Cards:

1. Vitality
2. Blade
3. Pulse
4. Ward
5. Done

Cursor starts on Vitality.

Cursor automatically moves to next card every 1.5 seconds.

Tap:

- If less than 0.3 seconds since last Upgrade tap:
  - cancel and return to Title.
- Otherwise:
  - confirm highlighted card.

Confirm behavior:

- If card is an upgrade:
  - If affordable and not maxed:
    - buy it,
    - save,
    - toast `Upgrade purchased: [name]`.
  - If not affordable:
    - toast `Cannot buy`.
  - If maxed:
    - toast `Maxed`.
- If card is Done:
  - return to Title.

Auto-return:

- If shards are 0 or all upgrades are maxed, return to Title after 3 seconds.

### Title state — Tier 1

Title state shows:

- Title.
- Best floor.
- Total shards.

Tap starts a new run.

There is no separate shop option.

### Death and victory flow — Tier 1

Death:

- Show death summary.
- Tap to continue.
- If `save.shards > 0`, go to Upgrade state.
- If `save.shards === 0`, go to Title.

Victory:

- Show victory summary.
- Tap to continue.
- If `save.shards > 0`, go to Upgrade state.
- If `save.shards === 0`, go to Title.

## 4.15 Progression through the game — Tier 1 / 2

A run is a single attempt to reach Floor 5 and defeat The Metronome.

Run flow:

1. Title.
2. Floor 1, Room 1.
3. Clear rooms.
4. Defeat Floor 1 boss.
5. Continue through Floor 5.
6. Defeat final boss.
7. Victory.
8. Upgrade state.
9. Title.

Death can occur at any point during a run.

Within a run:

- Rooms get harder.
- New enemy types unlock.
- Relic slots create build variety.
- The player may play defensively or aggressively based on Tempo management.

Between runs:

- Shards are used to permanently improve the player.
- The player can choose different upgrade paths.
- Relic randomness creates different runs.
- The player can retry until victory.

## 4.16 Feel and pacing — Tier 1

Expected tap rates:

| Action | How the player does it | Approximate tap rate |
| --- | --- | ---: |
| Move | Let Tempo cool, then tap | ~1.4 taps/sec |
| Attack | Tap while Tempo is mid-range | ~1.5–2.5 taps/sec |
| Parry | Quick burst of taps to push Tempo high | ~4–6 taps/sec |
| Flick | Accidental fast tap while Parry is on cooldown | n/a |

Room pacing targets:

| Room type | Target time |
| --- | ---: |
| Combat room | 8–15 seconds |
| Treasure room | 3–6 seconds |
| Trap room | 5–10 seconds |
| Boss room | 15–30 seconds |

Target full run length:

- 8–15 minutes for a successful run.
- Shorter if death occurs early.

Combat feel:

- Cool: safe, able to move.
- Warm: offensive, able to attack.
- Hot: dangerous, likely to parry or waste input.

Required distinguishable feedback:

- Tap.
- Move.
- Attack.
- Parry.
- Flick.
- Player damage.
- Enemy damage.
- Parry cooldown ready.
- Room cleared.
- Boss phase change.
- Relic pickup.
- Shard pickup.
- Door unlock.
- Death.
- Victory.

## 4.17 Edge cases — Tier 1

| Case | Handling |
| --- | --- |
| First tap | Tempo starts at 0. First tap gives Tempo 30. First tap is always Move. |
| Tap while dead | In death mode, tap is a state transition, not a run action. No Tempo action. |
| Tap while paused | First tap resumes and is consumed. No run action. |
| Tap while door is closed | Action still occurs based on Tempo. Move does not pass through locked door. Attack and Parry can still affect enemies/barriers. |
| Tap while blocked by wall or enemy | Move is blocked. Tempo still changes. Attack and Parry still occur. |
| Multiple taps in same frame | Process taps sequentially. Each tap applies Tempo gain and action logic. |
| Tempo cap | Tempo cannot exceed 100. If Tempo is 100 and player taps: Parry if ready, Flick if on cooldown. |
| Parry cooldown active | If Tempo after tap is 70–100 and Parry cooldown is active: perform Flick, reset Tempo to 0. |
| Player overlaps door when door opens | Transition after 200 ms. |
| Enemy knocked off-screen | Despawn enemy. No penalty. |
| Projectile leaves room | Despawn projectile. |
| Trap active when player enters | If player overlaps during danger phase, deal 1 heart. If player has i-frames, no damage. |
| Relic slot full | Convert new relic to shards. Do not block pickup. |
| Upgrade not affordable | Confirm fails. Show `Cannot buy`. Cursor continues auto-advancing. |
| Upgrade maxed | Confirm fails. Show `Maxed`. |
| All upgrades maxed | Upgrade state auto-returns to Title after 3 seconds. |
| Shards are zero | Upgrade state auto-returns to Title after 3 seconds. |
| Boss dies while projectiles exist | Destroy all remaining boss projectiles. Stop boss patterns. |
| Player dies while parrying | If HP reaches 0, death occurs. Parry i-frames do not prevent death from a hit already applied. |
| Player dies at door | Death occurs. No room transition. |
| Final boss dies | Victory. Stop all enemies and projectiles. Show victory summary. |

## 4.18 Cut list

Intentionally not included:

- No second button.
- No hold input.
- No directional input.
- No jumping.
- No vertical movement.
- No 2.5D or 3D depth.
- No pause button.
- No buildings or open-world navigation.
- No puzzle rooms.
- No crafting.
- No shop inside the run.
- No multiple character classes.
- No endless mode after victory.
- No level select.
- No multiplayer.
- No settings menu.
- No minimap.
- No room labels.
- No enemy HP bars except boss.
- No hover interaction.

If a feature requires a separate input or separate decision axis, it is cut.

---

# 5. CHARACTERS

All characters face right by default in world space. Enemies visually face left because they act against the player. Bosses face left.

## Player

| Property | Value |
| --- | --- |
| Silhouette | Small mechanical warden. |
| Size | 0.8 tiles wide, 0.9 tiles tall. |
| Collision width | 1.0 tile. |
| Facing | Right. |
| Core | Circle in center, color matches next action. |

Animations:

| Animation | Motion rule |
| --- | --- |
| `idle` | Subtle core pulse. Heat ring opacity 0.25. |
| `move` | Lean forward 8°, cyan dust puffs, 100ms tween. |
| `move_blocked` | Bump forward 4px, gray dust puff. |
| `attack` | Amber slash arc extends 1.5 tiles, 120ms. |
| `parry` | White-violet ring expands to 1.5 tile radius over 200ms, player flashes white 100ms. |
| `flick` | Small gray spark, 1.0 tile radius visual, 80ms. |
| `damaged` | Flash red 100ms, blink 8 times/sec during i-frames. |
| `dead` | Core shatters, white/red particles, desaturate screen. |

## Chaser

| Property | Value |
| --- | --- |
| Silhouette | Rounded bronze beetle. |
| Size | 0.8 tiles wide, 0.7 tiles tall. |
| Collision width | 1.0 tile. |
| Facing | Left. |

Animations:

| Animation | Motion rule |
| --- | --- |
| `idle` | Low bob, treads move toward player. |
| `contact` | White flash 50ms on hit. |
| `knockback` | 100ms tween away from player. |
| `death` | Shatters into 6–10 shard particles. |

## Spiky

| Property | Value |
| --- | --- |
| Silhouette | Small spiked creature. |
| Size | 0.6 tiles wide, 0.6 tiles tall. |
| Collision width | 1.0 tile. |
| Facing | Left. |

Animations:

| Animation | Motion rule |
| --- | --- |
| `idle` | Faster, more jittery bob than Chaser. |
| `contact` | White flash 50ms on hit. |
| `knockback` | 100ms tween away from player. |
| `death` | Shatters into 6–10 shard particles. |

## Shooter

| Property | Value |
| --- | --- |
| Silhouette | Gray turret with dark barrel and red lens. |
| Size | 0.8 tiles wide, 0.8 tiles tall. |
| Collision width | 1.0 tile. |
| Facing | Left. |

Animations:

| Animation | Motion rule |
| --- | --- |
| `idle` | Small base bob. |
| `fire_warning` | Barrel glows red 200ms before projectile. |
| `fire` | Muzzle flash, projectile spawns. |
| `contact` | White flash 50ms on hit. |
| `death` | Shatters into 6–10 shard particles. |

## Barrier

| Property | Value |
| --- | --- |
| Silhouette | Gear wall. |
| Size | 1 tile wide, 1.2 tiles tall. |
| Collision width | 1.0 tile. |
| Facing | None. |

Animations:

| Animation | Motion rule |
| --- | --- |
| `idle` | Central gear rotates slowly. |
| `hit` | White flash, small metal spark, crack advances. |
| `break` | Shatters into gear fragments, 15 shard particles. |

## Bosses

All bosses:

- Have distinct silhouettes.
- Have boss HP bar.
- Have at least 0.5 seconds of visual warning before active attacks.
- Have phase transition flash.
- Have death shatter.

| Boss | Size | Silhouette | Key states |
| --- | --- | --- | --- |
| Clockwork Golem | 3 × 2.5 tiles | Large bronze golem, central eye, chest pendulum, heavy arms. | Idle, telegraph, charge, stomp, triple shot, phase summon, death. |
| Gear Knight | 2.5 × 2.5 tiles | Armored knight, large sword, gear pauldrons, blue-gray armor with amber accents. | Idle, telegraph, dash, double shot, summon, death. |
| Ritual Beast | 3 × 2.5 tiles | Dark beast, ritual circle, pendulum-like tail, amber and black. | Idle, telegraph, spiral shot, charge, summon, death. |
| Twin Pistons | 3 × 2.5 tiles | Mechanical body, two large piston arms, cobalt and steel, white warning lights. | Idle, telegraph, left piston, right piston, fan shot, barrier spawn, death. |
| The Metronome | 3 × 3 tiles | Giant metronome, black and white body, pendulum, faint action-color accents. | Idle, telegraph, slow stomp, medium charge, fast burst, phase 2, phase 3, death. |

---

# 6. AUDIO

Audio is nonessential. All critical gameplay information is visual. The builder has access to an audio API. If audio is unavailable, all audio calls must no-op safely.

## Audio API

```js
Cadence.audio.init();
Cadence.audio.playSfx("sfx.tap");
Cadence.audio.setMusicState("run");
Cadence.audio.setLayer("attack", 0.4);
Cadence.audio.duck(0.2, 200);
```

## Synthesized SFX table

| Name | Recipe | When it plays |
| --- | --- | --- |
| `sfx.tap` | Woodblock tick: square 1800Hz, 30ms, gain 0.18, fast decay. | Every accepted run tap. |
| `sfx.move` | Low soft thud: sine 120Hz falling to 70Hz, 80ms, gain 0.30. | Move action. |
| `sfx.attack` | Mid slash: noise burst bandpass 2000Hz + sawtooth sweep 300→900Hz, 100ms, gain 0.35. | Attack action. |
| `sfx.parry` | Resonant bell: sine 1200Hz + partial 1800Hz, 250ms, gain 0.50, long decay. | Parry action. |
| `sfx.flick` | Weak spark: square 400Hz, 50ms, gain 0.15, dry. | Flick action. |
| `sfx.parry.ready` | Soft chime: sine 1500Hz, 100ms, gain 0.25. | Parry cooldown ends. |
| `sfx.player.damage` | Low descending hurt: sawtooth 220→80Hz, lowpass, 200ms, gain 0.50. | Player takes damage. |
| `sfx.enemy.damage` | Short hit tick: triangle 800Hz, 40ms, gain 0.20. | Enemy/barrier takes damage. |
| `sfx.enemy.die` | Small shatter + descending blip: noise 100ms + sine 600→200Hz, 150ms, gain 0.30. | Enemy dies. |
| `sfx.barrier.hit` | Metallic clank: square 500Hz + short noise, 50ms, gain 0.25. | Barrier takes damage. |
| `sfx.barrier.break` | Larger clank + gear shatter: noise 300ms + square 200Hz, gain 0.40. | Barrier breaks. |
| `sfx.projectile.fire` | Short pew: square 300→800Hz, 80ms, gain 0.20. | Enemy fires projectile. |
| `sfx.projectile.hit` | Low pop: sine 150Hz, 60ms, gain 0.35. | Projectile hits player. |
| `sfx.projectile.destroy` | Small zap: sawtooth 1200→400Hz, 50ms, gain 0.20. | Projectile destroyed. |
| `sfx.trap.warning` | Soft alarm pulse: square 600Hz, two short pulses over 200ms, gain 0.20. | Trap enters warning phase. |
| `sfx.trap.danger` | Sharp click: highpass noise, 80ms, gain 0.30. | Trap becomes active. |
| `sfx.door.locked` | Dull thud: sine 90Hz, 100ms, gain 0.30. | Player tries to enter locked door. |
| `sfx.door.unlock` | Gear ratchet: three square 1000Hz ticks, 30ms each, spaced 80ms, gain 0.30. | Door unlocks. |
| `sfx.door.open` | Soft whoosh: lowpass noise sweep, 200ms, gain 0.25. | Player enters open door. |
| `sfx.room.clear` | Two-note chime: sine 880Hz then 1320Hz, 200ms, gain 0.30. | Room cleared. |
| `sfx.relic.acquire` | Bright three-note arpeggio: sine 660, 880, 1320Hz, 250ms, gain 0.35. | Relic picked up. |
| `sfx.relic.convert` | Small shard/coin: triangle 1500→2000Hz, 200ms, gain 0.30. | Relic converted to shards. |
| `sfx.shard.pickup` | Tiny crystal ping: sine 2000Hz, 50ms, gain 0.15. | Shard picked up. |
| `sfx.boss.warning` | Low horn/rumble: sine 60Hz + filtered noise, 400ms, gain 0.40. | Boss attack warning. |
| `sfx.boss.charge` | Rumble + whoosh: filtered noise sweep, 300ms, gain 0.40. | Boss charge. |
| `sfx.boss.stomp` | Heavy thud: sine 60Hz, 200ms, gain 0.45. | Boss stomp. |
| `sfx.boss.phase` | Stinger + chime: sawtooth 200→400Hz + sine 1000Hz, 400ms, gain 0.45. | Boss phase change. |
| `sfx.ui.tap` | Soft click: square 1200Hz, 30ms, gain 0.20. | Menu tap. |
| `sfx.upgrade.cursor` | Very soft click: sine 900Hz, 30ms, gain 0.12. | Upgrade cursor moves. |
| `sfx.upgrade.confirm` | Positive two-note chime: sine 880Hz then 1320Hz, 150ms, gain 0.30. | Upgrade purchased. |
| `sfx.upgrade.cannot` | Dull buzz: square 120Hz, 150ms, gain 0.25. | Cannot buy. |
| `sfx.upgrade.maxed` | Dry high click: square 2000Hz, 50ms, gain 0.15. | Maxed. |
| `sfx.ui.cancel` | Descending blip: sine 800→300Hz, 150ms, gain 0.25. | Cancel upgrade. |
| `sfx.death` | Low drone + tempo break: sine 80Hz + noise, 800ms, gain 0.50. | Player dies. |
| `sfx.victory` | Bright fanfare: square arpeggio C-E-G-C, 800ms, gain 0.50. | Victory. |
| `sfx.zone.move` | Optional quiet click: sine 600Hz, 20ms, gain 0.08. | Marker enters Move zone. |
| `sfx.zone.attack` | Optional quiet click: sine 900Hz, 20ms, gain 0.08. | Marker enters Attack zone. |
| `sfx.zone.parry` | Optional quiet click: sine 1400Hz, 20ms, gain 0.08. | Marker enters Parry zone. |

## Music design

Music must not dictate the player’s gameplay Tempo. Do not add a visual metronome that tells the player when to tap. Do not flash the Tempo bar to the music beat.

| State | BPM | Mood |
| --- | ---: | --- |
| Title | 60 | Calm, mechanical, inviting |
| Run | 90 | Steady, industrial, readable |
| Boss | 110 | Tense, percussive, dangerous |
| Upgrade | 70 | Gentle, musical, reflective |
| Death | 50 | Low, slowed, final |
| Victory | 120 | Bright, resolved, celebratory |

Music stems:

| Stem | Description |
| --- | --- |
| `music.layer.base` | Pad and low pulse. Always present in run states. |
| `music.layer.attack` | Mid percussion and arpeggio. Active when player is in Attack zone or has attacked recently. |
| `music.layer.parry` | High tension synth and faster percussion. Active when player is in Parry zone or has parried recently. |
| `music.layer.boss` | Drums, low brass/industrial hits, and lead. Active in boss rooms. |
| `music.tick` | Soft metronome tick. Used only in Title and optionally Upgrade. Do not use in run gameplay. |

Adaptive run music:

- Base layer is always active.
- Move zone: sparse, no attack or parry layer.
- Attack zone: raise attack layer over 200ms.
- Parry zone: raise parry layer over 200ms.
- Parry zone while Parry cooldown active: lower parry layer slightly, keep weak tension layer.
- Player parries: play musical accent, swell parry layer for 300ms.
- Player flicks: dip music by 10% for 150ms, play weak accent.

Boss music:

- Base layer remains.
- Boss layer active.
- Attack and parry layers still react to player.
- Boss attacks trigger short musical accents.
- Boss phase changes trigger a stinger.

Recommended mixing:

| Bus | Level |
| --- | ---: |
| Master | 0.8 |
| Music | 0.5 |
| SFX | 0.7 |
| UI | 0.5 |

State mixing:

| State | Base | Attack | Parry | Boss | Tick |
| --- | ---: | ---: | ---: | ---: | ---: |
| Title | 0.8 | 0 | 0 | 0 | 0.4 |
| Run | 0.8 | 0–0.5 | 0–0.6 | 0 | 0 |
| Boss | 0.8 | 0–0.5 | 0–0.6 | 0.7 | 0 |
| Upgrade | 0.6 | 0 | 0 | 0 | 0.2 |
| Death | 0.8 | 0 | 0 | 0 | 0 |
| Victory | 0.8 | 0 | 0 | 0 | 0 |

Music transitions:

- Crossfade between music states over 500ms.
- Floor transitions within a run should not restart run music abruptly.
- Boss entry layers in boss stem over 500ms.
- Boss death ducks music and plays victory fanfare.

---

# 7. UX

UX is HTML and CSS only for presentation. JavaScript updates DOM classes, text, and style values, but the HUD and screens are DOM-based.

## State machine

| State | Entry | Tap behavior | Exit |
| --- | --- | --- | --- |
| `title` | Initial load, return from death/victory/upgrade | Start new run. | `run` |
| `run` | Title tap, `newRun` | Perform Tempo action. | `death`, `victory` |
| paused flag | Run loses focus | First tap resumes and is consumed. No run action. | `run` |
| `upgrade` | Death/victory if `save.shards > 0` | Confirm highlighted card, or quick-tap cancel to title. | `title` |
| `death` | Player HP reaches 0 | Continue to Upgrade if `save.shards > 0`, otherwise Title. | `upgrade` / `title` |
| `victory` | Final boss dies | Continue to Upgrade if `save.shards > 0`, otherwise Title. | `upgrade` / `title` |

Pause is not a mode. Pause is a flag inside `run`.

## Required DOM shell

```html
<div id="game-root">
  <canvas id="game-canvas"></canvas>

  <div id="hud">
    <div id="hp-bar">
      <div id="hp-fill"></div>
      <span id="hp-text"></span>
    </div>

    <div id="tempo-bar">
      <div id="tempo-zone-move"></div>
      <div id="tempo-zone-attack"></div>
      <div id="tempo-zone-parry"></div>
      <div id="tempo-marker"></div>
      <div id="tempo-cooldown"></div>
      <div id="tempo-flick"></div>
    </div>

    <div id="floor-room"></div>

    <div id="boss-bar">
      <span id="boss-name"></span>
      <div id="boss-fill"></div>
    </div>

    <div id="relic-slots">
      <div class="relic-slot"></div>
      <div class="relic-slot"></div>
      <div class="relic-slot"></div>
      <div class="relic-slot"></div>
      <div class="relic-slot"></div>
    </div>

    <div id="shards"></div>

    <div id="toasts"></div>
  </div>

  <div id="overlay"></div>
</div>
```

## HUD table

| Element | Record field | When visible |
| --- | --- | --- |
| `#hp-fill` | `player.hp / player.maxHp` | `run` |
| `#hp-text` | `player.hp` | `run` |
| `#tempo-zone-move` | `CONFIG.MOVE_ZONE_MAX` | `run` |
| `#tempo-zone-attack` | `CONFIG.ATTACK_ZONE_MAX` | `run` |
| `#tempo-zone-parry` | `CONFIG.TEMPO_MAX` | `run` |
| `#tempo-marker` | `player.nextTempo`, `player.nextAction` | `run` |
| `#tempo-cooldown` | `player.parryCooldown / player.parryCooldownMax` | `run` when `player.parryCooldown > 0` |
| `#tempo-flick` | `player.nextAction === "flick"` | `run` when next action is Flick |
| `#floor-room` | `room.floor`, `room.index` | `run` |
| `#boss-bar` | `boss.hp / boss.maxHp` | `run` when `boss` exists |
| `#boss-name` | `boss.name` | `run` when `boss` exists |
| `.relic-slot` | `player.relics[i]` | `run` |
| `#shards` | `save.shards` | `title`, `run`, `upgrade`, `death`, `victory` |
| `#toasts` | `game.toasts` | any state |
| `#overlay` | `game.mode`, `game.paused` | `title`, `paused`, `upgrade`, `death`, `victory` |

## Screens

### Title

- Shows `CADENCE`.
- Shows best floor: `Best: F3`.
- Shows total shards.
- Shows `Tap to start`.
- Optional small legend: Move arrow, Attack slash, Parry ring.
- Tap starts a new run.

### Run

- HUD visible.
- Tempo marker always visible.
- Player visible.
- Enemies, traps, barriers, relics, shards, and door visible.
- No visible button.
- No pause button.
- No directional controls.

### Pause

- Triggered by loss of focus.
- Dark overlay.
- Text: `Tap to continue`.
- Game time frozen.
- Music paused or heavily ducked.
- Any tap resumes.

### Upgrade

- One-button navigation.
- 5 cards:
  1. Vitality
  2. Blade
  3. Pulse
  4. Ward
  5. Done
- Card size: 120px × 160px.
- Spacing: 16px.
- On narrow screens, stack cards vertically.
- Cursor is a white 3px border around selected card.
- Cursor auto-advances every 1.5 seconds.
- Progress arc fills around cursor over 1.5 seconds.
- Tap resets auto-advance timer.
- Quick tap within 0.3 seconds cancels to Title.
- After a confirm tap, show small hint for 0.3 seconds:
  - `Tap again quickly to cancel`
- Auto-return after 3 seconds if shards are 0 or all upgrades are maxed.

Card states:

| State | Visual |
| --- | --- |
| Affordable | Bright border, white cost |
| Unaffordable | Dimmed card, red cost |
| Maxed | Gray card, `MAX` |
| Done | White arrow icon, no cost |

### Death

- Red vignette.
- Desaturated screen.
- Summary panel after 600ms.
- Shows:
  - `Run Ended`
  - Floor reached
  - Shards earned
  - Total shards
  - Best floor
  - `Tap to continue`
- Tap continues to Upgrade if `save.shards > 0`, otherwise Title.

### Victory

- White-gold burst.
- Screen briefly brightens.
- Metronome shatter.
- Summary panel after 800ms.
- Shows:
  - `Victory`
  - Shards earned
  - Total shards
  - Best floor
  - `Tap to continue`
- Tap continues to Upgrade if `save.shards > 0`, otherwise Title.

## CSS rules

- Scale virtual 960 × 540 to viewport while preserving aspect ratio.
- Letterbox if necessary.
- Keep important UI inside 16px safe area.
- Avoid critical gameplay objects in outer 24px of screen.
- No visible button.
- No hover styles.
- Use tabular numerals for counts.
- All important states have non-color cues.
- Reduced motion mode disables screen shake and reduces particles.

---

# 8. DEBUG API

`window.__game` is the only supported test control surface.

| Function | Description | Tier |
| --- | --- | ---: |
| `window.__game.version` | Returns version string. | 1 |
| `window.__game.start()` | Starts browser loop if not headless. | 1 |
| `window.__game.stop()` | Stops browser loop. | 1 |
| `window.__game.reset(options)` | Resets game. Options: `{ seed, save, mode }`. | 1 |
| `window.__game.newRun(seed)` | Starts a new run from current save. | 1 |
| `window.__game.setMode(mode)` | Forces mode. | 1 |
| `window.__game.tap()` | Enqueues a tap using same path as real input. | 1 |
| `window.__game.tick(dt)` | Advances simulation by `dt` seconds. Substeps in 1/60 s chunks. `tick(0)` processes queued taps. | 1 |
| `window.__game.getState()` | Returns serializable snapshot. | 1 |
| `window.__game.getSave()` | Returns save state. | 1 |
| `window.__game.setSave(save)` | Sets save state. | 1 |
| `window.__game.getRngSeed()` | Returns current RNG seed. | 1 |
| `window.__game.setRngSeed(seed)` | Sets RNG seed. | 1 |
| `window.__game.setTempo(value)` | Sets player Tempo directly. | 1 |
| `window.__game.setParryCooldown(value)` | Sets player Parry cooldown directly. | 1 |
| `window.__game.setPlayerHP(value)` | Sets player HP directly. | 1 |
| `window.__game.setPlayerX(value)` | Sets player x directly. | 1 |
| `window.__game.setShards(value)` | Sets total shards directly. | 1 |
| `window.__game.setPlayerStat(key, value)` | Sets a player stat directly. | 1 |
| `window.__game.setPaused(value)` | Sets pause flag directly. | 1 |
| `window.__game.setClockworkStacks(value)` | Sets Clockwork stack directly. | 1 |
| `window.__game.setClockworkCounter(value)` | Sets Clockwork attack counter directly. | 1 |
| `window.__game.setRoom(options)` | Sets current room directly. | 1 |
| `window.__game.generateFloor(floor, seed)` | Generates a floor and returns room array. | 1/2 |
| `window.__game.validateRoom(room)` | Runs room validator. | 1 |
| `window.__game.setDoorState(state)` | Sets door state directly. | 1 |
| `window.__game.setDoorTransition(time)` | Sets door transition timer directly. | 1 |
| `window.__game.setTutorialStep(step)` | Sets tutorial step directly. | 1 |
| `window.__game.spawnEnemy(type, x)` | Spawns enemy directly. | 1 |
| `window.__game.setEnemyHP(id, hp)` | Sets enemy HP directly. | 1 |
| `window.__game.spawnProjectile(x, vx, owner)` | Spawns projectile directly. | 1 |
| `window.__game.spawnTrap(x)` | Spawns trap directly. | 1 |
| `window.__game.setTrapPhase(id, phase)` | Sets trap phase directly. | 1 |
| `window.__game.spawnBarrier(x)` | Spawns barrier directly. | 1 |
| `window.__game.spawnRelic(relicId, x)` | Spawns relic directly. | 1 |
| `window.__game.spawnShardPile(x)` | Spawns shard pile directly. | 1 |
| `window.__game.damagePlayer(hearts, source)` | Damages player directly. | 1 |
| `window.__game.damageEnemy(id, amount, knockback)` | Damages enemy directly. | 1 |
| `window.__game.damageBarrier(id, amount)` | Damages barrier directly. | 1 |
| `window.__game.setBossHP(value)` | Sets boss HP directly. | 1/2 |
| `window.__game.setBossState(state)` | Sets boss state directly. | 2 |
| `window.__game.setUpgradeCursor(index)` | Sets upgrade cursor directly. | 1 |
| `window.__game.setBestFloor(floor)` | Sets best floor directly. | 1 |
| `window.__game.getLog()` | Returns event log copy. | 1 |
| `window.__game.clearLog()` | Clears event log. | 1 |

`getState()` must expose at least:

```js
{
  mode,
  paused,
  time,
  save,
  player,
  room,
  enemies,
  projectiles,
  traps,
  barriers,
  relics,
  shardPiles,
  boss,
  shards,
  runStats,
  upgrade,
  lastAction,
  toasts
}
```

---

# 9. TESTS

Tests are synchronous, deterministic, and driven by `window.__game`.

| Tier | Test group | High-level tests |
| ---: | --- | --- |
| 1 | Bootstrap | Debug API exists. Test harness exists. Reset produces title state. |
| 1 | Tempo | First tap is Move. Tempo decay enables Move. Rapid taps produce Move, Attack, Parry. Tempo cap and Flick. Next action preview. |
| 1 | Actions | Move blocked by enemy. Move blocked by barrier. Move blocked by locked door. Attack damages enemy. Attack destroys projectile. Parry grants i-frames and damage. Parry knockback. Flick weaker and no i-frames. Player damage and i-frames. |
| 1 | Room flow | Title starts run. Room transition. Death flow. One-button room clear test. |
| 1 | Meta | Upgrade purchase. Cannot buy. Maxed upgrade. Cursor auto-advance. Quick tap cancels. Auto-return when shards zero. Auto-return when all maxed. Save persistence. Best floor update. |
| 1 | Relics | Relic pickup with space. Relic conversion when full. Tempo decay clamps. Move distance clamp. Parry cooldown clamp. Player i-frame clamp. Echo chance clamp. Clockwork relic. Thorn relic. Echo relic. |
| 1 | Edge cases | Multiple taps same frame. Tap while dead ignored. Tap while paused resumes without action. Projectile leaves room. Enemy knocked off-screen despawns. Trap active when player overlaps. Door transition does not occur after death. Relic slot full does not block pickup. |
| 1 | UI | Required DOM IDs exist. Floor/room text updates. Next action is exposed. |
| 2 | Generation | Floor sequence. Room widths. Combat room invariants. Treasure room invariants. Trap room invariants. Boss room invariants. Every generated room is clearable. Every trap has safe phase. |
| 2 | Progression | Boss room to next floor. Final boss triggers victory. Full run smoke test. |
| 2 | Bosses | Every boss can be defeated. Boss telegraph is at least 0.5s. Boss patterns do not softlock. |
| 3 | Visual | Render one frame for each floor without exceptions. HUD marker class reflects `nextAction`. Parry cooldown overlay visible when cooldown active. Flick indicator visible when next action is Flick. Reduced motion disables screen shake. Non-color cues exist for Move, Attack, Parry, Flick, trap warning, trap danger, projectile, and upgrade affordability. |
| 4 | Audio | Audio init does not throw when unavailable. `playSfx` does not throw for all listed SFX names. Music state can be set to title/run/boss/upgrade/death/victory without exceptions. Audio duck does not throw. |

Required test helpers:

```js
function resetGame(seed, save) {
  window.__game.reset({ seed, save });
}

function tick(game, dt, count) {
  for (let i = 0; i < count; i++) {
    game.tick(dt);
  }
}

function tickUntil(game, condition, maxSeconds, dt) {
  dt = dt || 1 / 60;
  maxSeconds = maxSeconds || 20;
  const steps = Math.ceil(maxSeconds / dt);

  for (let i = 0; i < steps; i++) {
    game.tick(dt);
    if (condition(game.getState())) {
      return true;
    }
  }

  return false;
}
```

Tests must not use real timers. Use `game.tick(dt)` for all simulation time.

---

# 10. BUILD ORDER

1. Scaffold files and load order.
2. Implement `config`, `utils`, `rng`, and `save`.
3. Implement core game state, mode machine, input queue, and `tick(dt)`.
4. Implement Tempo, Move, Attack, Parry, and Flick.
5. Implement player stats, derived stats, damage, i-frames, and knockback.
6. Implement Floor 1 room generation: combat, treasure, trap, boss.
7. Implement Chaser, Barrier, Spike trap, projectile, relic, and shard pile.
8. Implement Boss 1.
9. Implement death, victory, upgrade, title, and save flow.
10. Implement basic DOM HUD and fallback canvas rendering.
11. Implement debug API and Tier 1 tests.
12. Add Floors 2–5, Spiky, Shooter, enemy unlocks, floor scaling, Bosses 2–5, and victory flow.
13. Add full generation validation and Tier 2 tests.
14. Implement visual identity: floor palettes, character visuals, particles, screen shake, telegraphs, accessibility cues, reduced motion.
15. Add Tier 3 visual smoke tests.
16. Implement synthesized audio, music states, adaptive layers, and no-op safety.
17. Add Tier 4 audio tests.
18. Run full test suite and verify Definition of Done.

---

# 11. DEFINITION OF DONE

## Tier 1 done

High level: A player can play a Floor 1 vertical slice using only one tap, die or win, and spend shards.

Checkboxes:

- [ ] `index.html` loads and runs in a browser.
- [ ] `test.html` loads and runs tests in a headless page.
- [ ] `window.__game` exists.
- [ ] `window.__runTests()` returns `failed === 0` for Tier 1 tests.
- [ ] One tap is the only input.
- [ ] Tempo starts at 0.
- [ ] First tap is Move.
- [ ] Tempo decay works.
- [ ] Move zone is 0–39.
- [ ] Attack zone is 40–69.
- [ ] Parry zone is 70–100.
- [ ] Move advances 1.0 tile by default.
- [ ] Attack deals 15 damage by default.
- [ ] Parry grants 0.3s i-frames.
- [ ] Parry has 0.8s base cooldown.
- [ ] Flick occurs when Parry is unavailable.
- [ ] Player can die.
- [ ] Death adds 50 shards.
- [ ] Floor 1 has 5 rooms.
- [ ] Floor 1 sequence is combat, treasure, combat, trap, boss.
- [ ] Chaser can be damaged and killed.
- [ ] Barrier can be broken.
- [ ] Spike trap has safe, warning, and danger phases.
- [ ] Projectile can be destroyed.
- [ ] Relic can be picked up.
- [ ] Relic converts to shards when slots are full.
- [ ] Shard pile can be picked up.
- [ ] Boss 1 can be defeated.
- [ ] Upgrade state can buy Vitality, Blade, Pulse, Ward.
- [ ] Upgrade state can cancel with quick tap.
- [ ] Save state persists when storage is available.
- [ ] Basic HUD shows HP, Tempo marker, floor/room, shards, relic slots, and toasts.
- [ ] No audio is required.

## Tier 2 done

High level: A full five-floor roguelike run can be completed procedurally.

Checkboxes:

- [ ] Floors 2–5 generate.
- [ ] Room widths match formulas.
- [ ] Boss widths are 22, 24, 26, 28, 30.
- [ ] Floor 1 enemies are Chaser only.
- [ ] Floor 2 unlocks Shooter.
- [ ] Floor 3 unlocks Spiky.
- [ ] Enemy HP scales by floor.
- [ ] Enemy speed scales by floor.
- [ ] Projectile speed scales by floor.
- [ ] Barrier HP scales by floor.
- [ ] Trap danger duration scales by floor.
- [ ] Bosses 2–5 exist.
- [ ] Every boss has at least 0.5s telegraph.
- [ ] Every boss can be defeated.
- [ ] Boss death clears boss projectiles.
- [ ] Final boss death triggers Victory immediately.
- [ ] Victory adds 200 shards.
- [ ] Full seeded run can reach Victory.
- [ ] `save.bestFloor` updates to 5 on victory.
- [ ] Tier 2 tests pass.

## Tier 3 done

High level: The game visually communicates tempo, danger, floor identity, and accessibility.

Checkboxes:

- [ ] Default rendered tile size is 32px.
- [ ] Virtual resolution is 960 × 540.
- [ ] Each floor uses its assigned palette.
- [ ] Action colors are immutable.
- [ ] Move is cyan.
- [ ] Attack is amber.
- [ ] Parry is violet-white.
- [ ] Flick is gray.
- [ ] Danger is red.
- [ ] Warning is yellow.
- [ ] Tempo marker shows `nextTempo`.
- [ ] Tempo marker icon changes on zone boundary.
- [ ] Parry cooldown is hatched and swept.
- [ ] Flick indicator appears when next action is Flick.
- [ ] Spike trap safe/warning/danger phases are visually distinct.
- [ ] Boss telegraphs are visible for at least 0.5s.
- [ ] Player, enemies, barriers, projectiles, relics, shards, and doors are visually distinct.
- [ ] Particles exist for core actions.
- [ ] Screen shake exists for Parry, player damage, boss stomp, boss phase, and death.
- [ ] Reduced motion disables screen shake.
- [ ] Reduced motion reduces particles.
- [ ] Critical states have non-color cues.
- [ ] Tier 3 tests pass.

## Tier 4 done

High level: Audio reinforces feedback without being essential.

Checkboxes:

- [ ] Audio init does not throw when unavailable.
- [ ] All listed SFX names can be played without exceptions.
- [ ] SFX are distinct for Move, Attack, Parry, Flick, damage, room clear, door unlock, relic, shard, boss, UI, death, and victory.
- [ ] Music states exist for title, run, boss, upgrade, death, and victory.
- [ ] Music does not force player Tempo.
- [ ] Music can be ducked.
- [ ] Audio can be muted without breaking gameplay.
- [ ] Tier 4 tests pass.

---

# A. SANITY

| Check | Result |
| --- | --- |
| Tempo zones match action table | Valid. Move 0–39, Attack 40–69, Parry 70–100. |
| Tempo gain and decay match gameplay | Valid. +30 per tap, 30/sec base decay. |
| Parry cooldown and i-frames match gameplay | Valid. 0.8s cooldown, 0.3s i-frames. |
| Player base stats match gameplay | Valid. 5 hearts, 200 HP, 15 attack, 10 parry, 2 flick. |
| Room width formula matches table | Valid. `14 + floor * 2 + rand(0,4)` produces 16–20, 18–22, 20–24, 22–26, 24–28. |
| Boss width formula matches table | Valid. `20 + floor * 2` produces 22, 24, 26, 28, 30. |
| Tile size conflict resolved | Valid. Default 32px from visual; engineering 48 fallback superseded. |
| Collision width conflict resolved | Valid. Collision widths are 1.0 tile for player/enemies/barriers and 0.5 for projectiles; visual sizes remain visual. |
| Victory trigger conflict resolved | Valid. Final boss death triggers Victory immediately; floors 1–4 use door transition. |
| Death/victory continue condition resolved | Valid. Use total `save.shards > 0`, not only run-earned shards. |
| Relic drop weights filled | Valid. 60/30/10 adopted from engineering. |
| Clockwork behavior made precise | Valid. Counter, stack, and consumption rules defined. |
| Boss timing gap filled | Valid. 1.0s idle, 0.5s recover, 0.5s telegraph; final phase 3 faster. |
| Boss dash distance gap filled | Valid. Fixed 4 tiles. |
| Boss stomp trap placement gap filled | Valid. `round(player.x + 1)` clamped. |
| Enemy count capacity cap added | Valid. Prevents invalid spacing. |
| Room entry reset added | Valid. Resets Tempo, Parry cooldown, and i-frames. |
| Door lock conditions consistent | Valid. Enemies, barriers, and boss lock door; traps/relics/shards do not. |
| Shooter fire fairness added | Valid. No fire if too close or barrier blocks. |
| Tutorial wording conflict resolved | Valid. Use visual wording: amber zone, burst taps. |
| HUD fields present in global context | Valid. HP, Tempo, next action, cooldown, Flick, floor/room, boss, relics, shards, toasts. |
| Debug API covers gameplay systems | Valid. Tempo, player, room, entities, traps, barriers, relics, shards, door, boss, upgrade, save, RNG, log, input. |
| Tests tied to tiers | Valid. Tier 1 core, Tier 2 full roguelike, Tier 3 visual, Tier 4 audio. |
| Definition of Done matches tiers | Valid. Checkboxes align with Tier 1–4 exit conditions. |
| Dropped features documented | Valid. Settings menu, minimap, room labels, enemy HP bars, hover, and pause button dropped in §0.2 and §4.18. |