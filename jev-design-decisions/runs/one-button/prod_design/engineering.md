# `engineering.md`

## 0. Handoff note

This document is the implementation contract for **Cadence**, a one-button, tempo-based side-view roguelike.

It defines:

- the files that should exist,
- the runtime architecture,
- the core simulation rules,
- the procedural room/floor generation logic,
- the boss implementation rules,
- the relic/upgrade/meta systems,
- the debug API used by headless tests,
- the test harness,
- the required test set.

The implementation is **vanilla HTML, CSS, and JavaScript only**.

There is:

- no Node,
- no npm,
- no bundler,
- no TypeScript,
- no external runtime dependency,
- no test runner.

Tests run inside a headless browser page by driving the game through:

```js
window.__game
```

and inspecting:

```js
window.__game.getState()
window.__game.getLog()
window.__testResults
```

If a behavior is not explicitly defined here, it is not load-bearing.

---

# 1. Files that should exist

## 1.1 Required files

```text
index.html
test.html
css/style.css
js/config.js
js/utils.js
js/rng.js
js/save.js
js/relics.js
js/upgrades.js
js/entities.js
js/rooms.js
js/bosses.js
js/input.js
js/audio.js
js/render.js
js/ui.js
js/game.js
js/debug.js
js/main.js
js/test-harness.js
js/tests.js
```

## 1.2 Optional files

These are optional and should be treated as integration points for the visual/audio designer.

```text
assets/
assets/manifest.js
```

`assets/manifest.js` may define:

```js
window.CadenceAssets = {
  tileSize: 48,
  sprites: {
    player: "assets/player.png",
    enemy_chaser: "assets/chaser.png",
    enemy_spiky: "assets/spiky.png",
    enemy_shooter: "assets/shooter.png",
    barrier: "assets/barrier.png",
    boss_1: "assets/boss1.png",
    boss_2: "assets/boss2.png",
    boss_3: "assets/boss3.png",
    boss_4: "assets/boss4.png",
    boss_5: "assets/boss5.png"
  },
  audio: {
    tap: "assets/tap.ogg",
    move: "assets/move.ogg",
    attack: "assets/attack.ogg",
    parry: "assets/parry.ogg",
    flick: "assets/flick.ogg",
    player_damage: "assets/player_damage.ogg",
    enemy_damage: "assets/enemy_damage.ogg",
    parry_ready: "assets/parry_ready.ogg",
    room_clear: "assets/room_clear.ogg",
    boss_phase: "assets/boss_phase.ogg",
    relic_pickup: "assets/relic_pickup.ogg",
    shard_pickup: "assets/shard_pickup.ogg",
    door_unlock: "assets/door_unlock.ogg",
    death: "assets/death.ogg",
    victory: "assets/victory.ogg",
    trap_warning: "assets/trap_warning.ogg",
    trap_danger: "assets/trap_danger.ogg",
    projectile: "assets/projectile.ogg",
    boss_charge: "assets/boss_charge.ogg",
    boss_shot: "assets/boss_shot.ogg",
    upgrade_buy: "assets/upgrade_buy.ogg",
    cannot_buy: "assets/cannot_buy.ogg"
  }
};
```

If `window.CadenceAssets` is missing, the game must still work using procedural fallback rendering and no audio.

---

# 2. Load order

`index.html` must load scripts in this order:

```html
<script src="js/config.js"></script>
<script src="js/utils.js"></script>
<script src="js/rng.js"></script>
<script src="js/save.js"></script>
<script src="js/relics.js"></script>
<script src="js/upgrades.js"></script>
<script src="js/entities.js"></script>
<script src="js/rooms.js"></script>
<script src="js/bosses.js"></script>
<script src="js/input.js"></script>
<script src="js/audio.js"></script>
<script src="js/render.js"></script>
<script src="js/ui.js"></script>
<script src="js/game.js"></script>
<script src="js/debug.js"></script>
<script src="js/main.js"></script>
```

`test.html` loads the same files, but before `js/main.js` it sets:

```html
<script>
  window.CadenceTestMode = true;
</script>
```

Then after `js/main.js`:

```html
<script src="js/test-harness.js"></script>
<script src="js/tests.js"></script>
```

## Why classic scripts instead of ES modules?

The handoff environment may open files directly or serve them in a minimal headless browser. ES modules can fail under `file://` or minimal static hosting due to module CORS/import resolution.

Classic scripts with a single global namespace are the most robust choice.

---

# 3. Global namespace

All code attaches to:

```js
window.Cadence
```

Example:

```js
(function () {
  "use strict";

  const C = (window.Cadence = window.Cadence || {});

  C.utils = {
    clamp(value, min, max) {
      return Math.max(min, Math.min(max, value));
    }
  };
})();
```

The only global test/debug object is:

```js
window.__game
```

The only global test result object is:

```js
window.__testResults
```

Do not create other globals.

---

# 4. Runtime architecture

## 4.1 Game creation

`js/game.js` must expose:

```js
Cadence.createGame(config)
```

`config` may contain:

```js
{
  headless: false,
  seed: null,
  saveKey: "cadence.save.v1"
}
```

`js/main.js` creates the game and exposes the debug API:

```js
const game = Cadence.createGame({
  headless: Boolean(window.CadenceTestMode)
});

window.__game = Cadence.debug(game);
```

In normal browser mode, `main.js` starts the animation loop.

In test mode:

- no `requestAnimationFrame` loop is started,
- no audio is played,
- rendering is optional,
- all simulation is driven by `window.__game.tick(dt)`.

## 4.2 Why this matters

The headless test environment must be able to run the entire game without real time, real input, audio, or visual assets.

The debug API is the test seam.

---

# 5. State machine

The game has these modes:

```text
title
upgrade
run
death
victory
```

Pause is not a mode. Pause is a flag inside `run`.

## 5.1 Mode transitions

| Current mode | Tap behavior |
|---|---|
| `title` | Start a new run. |
| `upgrade` | Confirm highlighted card, or quick-tap cancel to title. |
| `run` | Perform Tempo action. |
| `death` | Continue to Upgrade if shards > 0, otherwise Title. |
| `victory` | Continue to Upgrade if shards > 0, otherwise Title. |

## 5.2 Pause

`game.paused` is only valid during `run`.

If the page loses focus or becomes hidden:

- `game.paused = true`,
- simulation stops,
- UI shows “Tap to continue”.

On the first tap while paused:

- pause is cleared,
- the tap is consumed,
- no run action is performed.

On the next tap:

- normal Tempo action occurs.

## Why pause is a flag and not a mode?

Pause should not destroy run state. It only suspends the run update loop.

---

# 6. Determinism

The game must be deterministic when driven by the debug API.

## 6.1 Rules

All randomness must come from:

```js
game.rng
```

Do not use:

```js
Math.random()
```

in gameplay logic.

Do not use:

```js
Date.now()
performance.now()
```

for gameplay logic.

Use:

```js
game.time
```

for all in-game timing.

`game.time` advances only through:

```js
game.update(dt)
```

which is called by:

- the real animation loop in browser mode,
- `window.__game.tick(dt)` in test mode.

## 6.2 RNG

`js/rng.js` must provide a seeded 32-bit RNG.

Recommended implementation: `mulberry32`.

API:

```js
C.RNG.create(seed)
```

Returns:

```js
{
  next(),
  nextFloat(min, max),
  nextInt(min, max),
  chance(probability),
  pick(array),
  shuffle(array),
  weighted(items)
}
```

`weighted(items)` accepts:

```js
[
  { value: "chaser", weight: 70 },
  { value: "shooter", weight: 30 }
]
```

and returns `value`.

## Why seeded RNG?

Tests must be repeatable. Room generation, relic drops, shard piles, and Echo rolls must all be reproducible from a seed.

---

# 7. Core constants

`js/config.js` must define all tunable gameplay constants.

Required constants:

```js
C.CONFIG = {
  TEMPO_MAX: 100,
  TAP_GAIN: 30,
  TEMPO_DECAY: 30,

  MOVE_ZONE_MAX: 39,
  ATTACK_ZONE_MAX: 69,

  PARRY_COOLDOWN: 0.8,
  PARRY_IFRAMES: 0.3,
  PLAYER_IFRAMES: 0.8,

  MOVE_DISTANCE: 1.0,
  MOVE_DISTANCE_MAX: 1.5,

  ATTACK_DAMAGE: 15,
  PARRY_DAMAGE: 10,
  FLICK_DAMAGE: 2,

  ATTACK_RANGE: 1.5,
  PARRY_RADIUS: 1.5,
  FLICK_RADIUS: 1.0,

  KNOCKBACK: 2.0,
  BOSS_KNOCKBACK_FACTOR: 0.5,

  PLAYER_WIDTH: 1.0,
  ENEMY_WIDTH: 1.0,
  BARRIER_WIDTH: 1.0,
  PROJECTILE_WIDTH: 0.5,

  DOOR_TRANSITION_TIME: 0.2,

  ROOM_CLEAR_BONUS: 10,
  BOSS_KILL_BONUS: 100,
  DEATH_BONUS: 50,
  VICTORY_BONUS: 200,

  SHARD_PILE_MIN: 5,
  SHARD_PILE_MAX: 15,

  UPGRADE_COSTS: [50, 100, 200, 400, 800],

  UPGRADE_AUTO_ADVANCE_TIME: 1.5,
  UPGRADE_CANCEL_WINDOW: 0.3,
  UPGRADE_AUTO_RETURN_TIME: 3.0
};
```

Derived player stats are computed from:

- base constants,
- permanent upgrades,
- in-run relics.

Do not store derived stats as the source of truth. Recompute them when:

- a relic is picked up,
- a relic is converted,
- an upgrade is purchased,
- a new run starts.

---

# 8. Save state

`js/save.js` manages persistent meta state.

Default save:

```js
{
  version: 1,
  shards: 0,
  upgrades: {
    vitality: 0,
    blade: 0,
    pulse: 0,
    ward: 0
  },
  bestFloor: 0
}
```

Persistence key:

```js
"cadence.save.v1"
```

Use `localStorage` when available.

If `localStorage` throws or is unavailable, fall back to an in-memory object.

Save on:

- upgrade purchase,
- death,
- victory,
- best floor update.

## 8.1 Why in-memory fallback?

Headless or sandboxed environments may block `localStorage`. The game must still run and be testable.

---

# 9. Player stats

## 9.1 Base player

At the start of a run:

```js
{
  x: 2,
  hp: maxHp,
  maxHp: maxHearts * 40,
  maxHearts: 5,
  tempo: 0,
  parryCooldown: 0,
  iFrameTimer: 0,
  parryIFrameTimer: 0,
  relics: [],
  clockworkStacks: 0,
  clockworkAttackCounter: 0
}
```

## 9.2 Derived stats

Compute:

```js
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

## 9.3 Why recompute derived stats?

Relics and upgrades can be picked up or purchased at different times. Storing derived stats directly would create hidden state and stacking bugs.

---

# 10. Input

The only gameplay input is a tap.

Accepted real input:

- pointer down anywhere,
- `Space`,
- `Enter`.

Ignore:

- key repeat,
- pointer hold,
- pointer release,
- directional keys,
- mouse wheel.

## 10.1 Tap queue

All taps are placed into:

```js
game.inputQueue
```

The update loop processes the queue sequentially.

This satisfies the rule:

> If multiple taps occur in the same frame, process them sequentially.

## 10.2 Debug tap

`window.__game.tap()` must use the same path as real input.

It should not bypass Tempo rules.

---

# 11. Update loop

The only simulation entry point is:

```js
game.update(dt)
```

`dt` is in seconds.

Clamp:

```js
dt = Math.min(dt, 0.1)
```

`game.time += dt`

## 11.1 Run update order

For mode `run`, update in this exact order:

```text
1. If door transition timer is active, advance it.
2. If door transition completes, transition to next room and return.
3. Decay player timers:
   - tempo
   - parryCooldown
   - iFrameTimer
   - parryIFrameTimer
4. Process all queued taps.
5. Update enemies.
6. Update boss.
7. Update projectiles.
8. Update traps.
9. Resolve collisions and damage.
10. Check room clear / door state.
11. Update effects, toasts, damage numbers.
```

## Why this order?

It makes Tempo behavior deterministic.

Every frame:

1. Tempo decays.
2. Taps are applied.
3. Actions happen.
4. World reacts.

This matches the gameplay rule that the action is determined by Tempo **after the tap is applied**.

---

# 12. Tempo system

Tempo is a number from `0` to `100`.

## 12.1 Decay

Each frame:

```js
player.tempo = max(0, player.tempo - player.tempoDecay * dt)
```

## 12.2 Tap resolution

On tap:

```js
player.tempo = min(100, player.tempo + CONFIG.TAP_GAIN)

if player.tempo <= 39:
  performMove()
else if player.tempo <= 69:
  performAttack()
else:
  if player.parryCooldown <= 0 or player.clockworkStacks > 0:
    performParry()
  else:
    performFlick()
```

## 12.3 Next action preview

The HUD and debug state must expose:

```js
nextTempo = min(100, player.tempo + CONFIG.TAP_GAIN)
```

`nextAction` is:

```text
move
attack
parry
flick
```

Rules:

```text
if nextTempo <= 39:
  nextAction = "move"
else if nextTempo <= 69:
  nextAction = "attack"
else:
  if player.parryCooldown <= 0 or player.clockworkStacks > 0:
    nextAction = "parry"
  else:
    nextAction = "flick"
```

## Why expose `nextAction`?

The HUD marker is the player’s primary decision tool. Tests must be able to verify the exact result of the next tap without simulating it.

---

# 13. Player actions

## 13.1 Coordinate system

All positions are in tiles.

`x` increases to the right.

Entities have:

```js
x
width
```

For most entities:

```js
width = 1.0
```

The player occupies:

```text
[player.x, player.x + 1]
```

The room spans:

```text
[0, room.width]
```

The door tile is:

```js
room.doorX = room.width - 1
```

The player starts at:

```js
x = 2
```

## 13.2 Move

Move attempts to advance:

```js
targetX = player.x + player.moveDistance
```

Move is blocked if:

- `targetX < 0`,
- `targetX + player.width > room.width`,
- the target interval overlaps a barrier,
- the target interval overlaps an enemy,
- the target interval enters the door tile while the door is locked.

If blocked:

- player position does not change,
- Tempo still changes,
- log `blocked: true`.

If not blocked:

- set `player.x = targetX`,
- log `blocked: false`.

## 13.3 Attack

Attack does not move the player.

Forward hitbox:

```text
[player.x + 1, player.x + 1 + player.attackRange]
```

Attack:

- damages all enemies in hitbox,
- damages all barriers in hitbox,
- destroys all projectiles in hitbox,
- does not knock enemies back,
- does not reset Tempo.

Echo relic:

- after normal damage is applied,
- if `rng.chance(player.echoChance)` succeeds,
- deal `player.attackDamage` again to all enemies/barriers in the same hitbox.

Echo triggers once per attack, not per target.

## 13.4 Parry

Parry:

- resets Tempo to `0`,
- sets `player.parryCooldown = player.parryCooldownMax`,
- sets `player.parryIFrameTimer = 0.3`,
- damages enemies/barriers in radius,
- knocks back enemies in radius,
- destroys projectiles in radius.

Parry radius interval:

```text
[player.x + 0.5 - player.parryRadius,
 player.x + 0.5 + player.parryRadius]
```

With base radius `1.5`:

```text
[player.x - 1, player.x + 2]
```

Clockwork relic:

- after 3 attacks, set `player.clockworkStacks = 1`,
- max 1 stack,
- if Parry is on cooldown but `clockworkStacks > 0`,
  - consume stack,
  - perform Parry,
  - set `parryCooldown = parryCooldownMax`.

## 13.5 Flick

Flick occurs when:

- Tempo after tap is `70-100`,
- Parry cooldown is active,
- no Clockwork stack is available.

Flick:

- resets Tempo to `0`,
- deals `player.flickDamage` in radius,
- destroys projectiles in radius,
- does not grant i-frames,
- does not knock enemies back.

Flick radius interval:

```text
[player.x + 0.5 - player.flickRadius,
 player.x + 0.5 + player.flickRadius]
```

With base radius `1.0`:

```text
[player.x - 0.5, player.x + 1.5]
```

---

# 14. Damage rules

## 14.1 Player damage

All normal damage is `1 heart`, or `40 HP`.

`damagePlayer(source)`:

1. If player is already dead, return.
2. If `player.iFrameTimer > 0` or `player.parryIFrameTimer > 0`, ignore damage.
3. Otherwise:
   - `player.hp -= 40`,
   - set `player.iFrameTimer = player.playerIFramesMax`,
   - emit `player_damage`,
   - create damage number,
   - if `player.hp <= 0`, trigger death.

## 14.2 Enemy damage

`damageEnemy(enemy, amount, source)`:

1. `enemy.hp -= amount`.
2. Emit `enemy_damage`.
3. If `enemy.hp <= 0`:
   - remove enemy,
   - add enemy shard reward,
   - increment `runStats.enemiesKilled`,
   - emit `enemy_died`.

## 14.3 Barrier damage

`damageBarrier(barrier, amount, source)`:

1. `barrier.hp -= amount`.
2. If `barrier.hp <= 0`:
   - remove barrier,
   - add `15` shards,
   - emit `barrier_broken`.

## 14.4 Knockback

When an enemy is knocked back:

```js
direction = sign(enemy.x - player.x)
if direction === 0:
  direction = 1

amount = CONFIG.KNOCKBACK
if enemy.isBoss:
  amount *= CONFIG.BOSS_KNOCKBACK_FACTOR

targetX = enemy.x + direction * amount
```

Knockback is a `100 ms` tween.

If blocked by a wall or barrier, clamp target.

If target is off-screen left:

```js
targetX < -1
```

the enemy despawns after the tween.

Bosses do not despawn from knockback. Bosses are clamped to room bounds.

## Why tween knockback?

Instant knockback can look broken and makes tests harder to reason about. A short deterministic tween preserves the gameplay intent while remaining testable.

---

# 15. Entities

## 15.1 Enemy definitions

Base definitions:

```js
C.ENEMIES = {
  chaser: {
    name: "Chaser",
    hp: 30,
    speed: 2.0,
    shards: 5,
    width: 1.0
  },
  spiky: {
    name: "Spiky",
    hp: 20,
    speed: 3.0,
    shards: 8,
    width: 1.0
  },
  shooter: {
    name: "Shooter",
    hp: 45,
    speed: 1.0,
    shards: 10,
    width: 1.0,
    fireRate: 2.0
  }
}
```

Floor scaling:

```js
enemy.hp = base.hp * (1 + 0.15 * (floor - 1))
enemy.speed = base.speed * (1 + 0.05 * (floor - 1))
```

Shard rewards do not scale.

## 15.2 Enemy AI

### Chaser

- moves toward player,
- deals contact damage,
- blocked by barriers and walls.

### Spiky

- same as Chaser,
- faster and weaker.

### Shooter

- tries to maintain distance.
- If distance to player is `< 3`, moves away.
- If distance to player is `> 5`, moves toward player.
- Otherwise stays.
- Fires one projectile every `2.0 s`.

Shooter fire rules:

- only fires if distance to player is `> 1.5`,
- only fires if no barrier is between shooter and player.

## Why Shooter fire rules?

This prevents projectiles from spawning directly on the player with no reaction time, which would violate the fairness rules.

## 15.3 Contact damage

If player interval overlaps enemy interval:

- deal `1 heart` to player,
- if Thorn relic is present, deal `player.thornDamage` to enemy once per enemy per second.

Each enemy has:

```js
thornTimer
```

When overlapping:

```js
enemy.thornTimer -= dt
if enemy.thornTimer <= 0:
  damageEnemy(enemy, player.thornDamage, "thorn")
  enemy.thornTimer = 1.0
```

Thorn can trigger even if the player is in i-frames, because the enemy is still in contact.

---

# 16. Projectiles

Projectile object:

```js
{
  id,
  x,
  vx,
  owner: "enemy" | "boss",
  width: 0.5
}
```

Projectile speed:

```js
projectileSpeed = 4 + 0.5 * (floor - 1)
```

Projectiles move left:

```js
vx = -projectileSpeed
```

Spawn position:

```js
x = shooter.x - 0.5
```

Projectile update:

1. Move:
   ```js
   x += vx * dt
   ```
2. If projectile overlaps barrier, destroy projectile.
3. If projectile leaves room:
   ```js
   x < -1 or x > room.width + 1
   ```
   destroy projectile.
4. If projectile overlaps player:
   - if player has i-frames, do nothing,
   - otherwise damage player and destroy projectile.

Boss projectiles have:

```js
owner = "boss"
```

When a boss dies, all projectiles with `owner === "boss"` are destroyed.

Enemy projectiles remain after enemy death.

## Why keep enemy projectiles?

This matches normal roguelike projectile behavior and avoids hidden cleanup assumptions.

---

# 17. Barriers

Barrier object:

```js
{
  id,
  x,
  hp,
  maxHp,
  width: 1.0
}
```

Barrier HP:

```js
barrierHP = 40 + 5 * (floor - 1)
```

Barriers:

- block player movement,
- block enemy movement,
- block projectiles,
- can be damaged by Attack, Parry, and Flick,
- do not move,
- drop `15` shards on break.

---

# 18. Spike traps

Trap object:

```js
{
  id,
  x,
  phase: "safe" | "warning" | "danger",
  timer,
  safeDuration: 1.0,
  warningDuration: 0.5,
  dangerDuration
}
```

Danger duration:

```js
dangerDuration = 0.4 + 0.05 * (floor - 1)
```

Cycle:

```text
safe -> warning -> danger -> safe
```

If player overlaps trap during `danger`:

- deal `1 heart` damage.

Traps do not block movement.

Every trap must have a safe phase.

---

# 19. Relics on floor

Relic object:

```js
{
  id,
  x,
  relicId
}
```

Relics do not block movement.

When player overlaps relic:

1. If player has fewer than `5` relics:
   - add relic,
   - recompute player stats,
   - toast `Relic acquired: [name]`,
   - emit `relic_pickup`.
2. If player already has `5` relics:
   - convert relic to shards,
   - toast `Relic converted: +X shards`,
   - emit `relic_converted`.

Conversion values:

```text
Common: 10
Rare: 20
Epic: 30
```

---

# 20. Shard piles

Shard pile object:

```js
{
  id,
  x,
  amount
}
```

Amount is generated when the pile is created:

```js
amount = rng.nextInt(5, 15)
```

Shard piles do not block movement.

When player overlaps:

- add `amount` to shards,
- remove pile,
- toast or floating text,
- emit `shard_pickup`.

---

# 21. Relic definitions

`js/relics.js` must define:

```js
C.RELICS = {
  metronome: {
    name: "Metronome",
    rarity: "common"
  },
  heavyCog: {
    name: "Heavy Cog",
    rarity: "common"
  },
  springBoot: {
    name: "Spring Boot",
    rarity: "common"
  },
  thorn: {
    name: "Thorn",
    rarity: "common"
  },
  ironLatch: {
    name: "Iron Latch",
    rarity: "rare"
  },
  echo: {
    name: "Echo",
    rarity: "rare"
  },
  ward: {
    name: "Ward",
    rarity: "rare"
  },
  pulse: {
    name: "Pulse",
    rarity: "rare"
  },
  glassHeart: {
    name: "Glass Heart",
    rarity: "epic"
  },
  clockwork: {
    name: "Clockwork",
    rarity: "epic"
  }
}
```

Relic drop weights:

```text
Common: 60
Rare: 30
Epic: 10
```

When spawning a relic:

1. choose rarity by weight,
2. choose a random relic of that rarity.

Duplicates are allowed.

## Why 60/30/10?

The gameplay document defines relics and conversion values but not drop weights. A common/rare/epic distribution is needed for build variety and meta pacing. 60/30/10 gives readable common builds while preserving rare and epic spikes.

---

# 22. Upgrades

`js/upgrades.js` must define:

```js
C.UPGRADES = {
  vitality: {
    name: "Vitality",
    maxLevel: 5
  },
  blade: {
    name: "Blade",
    maxLevel: 5
  },
  pulse: {
    name: "Pulse",
    maxLevel: 5
  },
  ward: {
    name: "Ward",
    maxLevel: 5
  }
}
```

Costs:

```js
[50, 100, 200, 400, 800]
```

Level `0` is base.

Cost to buy level `1` is `50`.

Cost to buy level `5` is `800`.

Upgrade effects are applied through derived stat computation.

---

# 23. Upgrade state

The Upgrade state uses one button but does **not** use run Tempo.

State:

```js
game.upgrade = {
  cursor: 0,
  cursorTimer: 0,
  lastTapTime: -Infinity,
  autoReturnTimer: 0,
  autoReturnActive: false
}
```

Cards:

```text
0: Vitality
1: Blade
2: Pulse
3: Ward
4: Done
```

Cursor starts at `0`.

## 23.1 Upgrade update

Each frame:

```js
upgrade.cursorTimer += dt

if upgrade.cursorTimer >= 1.5:
  upgrade.cursor = (upgrade.cursor + 1) % 5
  upgrade.cursorTimer -= 1.5
```

If auto-return is active:

```js
upgrade.autoReturnTimer += dt

if upgrade.autoReturnTimer >= 3.0:
  enterTitle()
```

Auto-return is active when:

- shards are `0`, or
- all upgrades are maxed.

## 23.2 Upgrade tap

On tap:

```js
if game.time - upgrade.lastTapTime < 0.3:
  enterTitle()
  return

upgrade.lastTapTime = game.time
confirmUpgradeCard(upgrade.cursor)
```

Confirm behavior:

- if card is an upgrade:
  - if affordable and not maxed:
    - buy,
    - save,
    - toast `Upgrade purchased`,
    - emit `upgrade_buy`,
  - if not affordable:
    - toast `Cannot buy`,
    - emit `cannot_buy`,
  - if maxed:
    - toast `Maxed`,
- if card is `Done`:
  - enter Title.

After a successful purchase, if shards are now `0` or all upgrades are maxed, activate auto-return.

## Why separate Upgrade timing?

Menus must be predictable. Inheriting run Tempo would make the shop feel random and would violate the one-button menu rule.

---

# 24. Title state

Title state shows:

- title,
- best floor,
- total shards.

Tap starts a new run.

There is no separate shop button.

---

# 25. Death and victory

## 25.1 Death

When player HP reaches `0`:

1. mode becomes `death`,
2. add `50` shards,
3. update save,
4. show death summary.

Death summary should include:

- floor reached,
- shards earned this run,
- total shards,
- best floor.

Tap:

- if shards > 0, enter Upgrade,
- otherwise enter Title.

## 25.2 Victory

When final boss dies:

1. mode becomes `victory`,
2. add `200` shards,
3. update save,
4. stop all enemies and projectiles,
5. show victory summary.

Tap:

- if shards > 0, enter Upgrade,
- otherwise enter Title.

---

# 26. Run structure

A run has:

```text
5 floors
5 rooms per floor
```

Room indices:

```text
0, 1, 2, 3, 4
```

Room `4` is always the boss room.

No backtracking.

## 26.1 Room entry

When entering a room:

- set `player.x = 2`,
- reset:
  - `player.tempo = 0`,
  - `player.parryCooldown = 0`,
  - `player.iFrameTimer = 0`,
  - `player.parryIFrameTimer = 0`,
- keep:
  - HP,
  - relics,
  - shards,
  - upgrades,
  - Clockwork stack.

## Why reset room timers?

A new room is a clean tactical state. Carrying Tempo or cooldowns across rooms would create hidden unfairness and make the HUD less predictable at room start.

---

# 27. Door rules

Door state:

```text
locked
open
```

Door is locked until:

- all enemies are dead,
- all barriers are broken,
- if a boss exists, boss is dead.

Traps, relics, and shard piles do not lock the door.

When the door opens:

- add `10` room clear bonus once,
- toast `Room cleared`,
- emit `door_unlock`.

If player overlaps door tile:

```js
player.x >= room.doorX
```

and door is open:

- start `0.2 s` transition timer.

When timer completes:

- if room index `< 4`, go to next room,
- if room index `4` and floor `< 5`, go to next floor,
- if room index `4` and floor `5`, trigger victory.

## Why door open condition excludes traps?

Traps must have safe phases. If traps locked the door, a trap timing mistake could softlock the room.

---

# 28. Room generation

`js/rooms.js` owns room generation.

It must expose:

```js
C.rooms.generateFloor(floor, rng)
C.rooms.generateRoom(floor, index, type, rng)
C.rooms.validate(room)
```

`validate(room)` returns an array of strings. Empty array means valid.

Tests must use this validator.

---

## 28.1 Floor room sequence

### Floor 1

```text
combat
treasure
combat
trap
boss
```

### Floors 2-5

```text
combat
random
random
random
boss
```

Random room weights:

```text
combat: 60
treasure: 25
trap: 15
```

If floors 2-5 have no Treasure among rooms `1`, `2`, and `3` using zero-based indices, set room index `2` to Treasure.

## Why force a Treasure room?

The gameplay document requires a smooth learning curve and shard economy. Guaranteeing at least one Treasure room prevents shard-starved runs.

---

## 28.2 Room width

Normal room width:

```js
width = 14 + floor * 2 + rng.nextInt(0, 4)
width = clamp(width, 14, 28)
```

Boss room width:

```js
width = 20 + floor * 2
```

This produces:

| Floor | Boss width |
|---:|---:|
| 1 | 22 |
| 2 | 24 |
| 3 | 26 |
| 4 | 28 |
| 5 | 30 |

---

## 28.3 Placement rules

All placed objects use integer tile positions.

This is important for:

- overlap prevention,
- spacing validation,
- softlock prevention,
- deterministic tests.

Objects that block or occupy space:

- enemies,
- barriers,
- traps,
- relics,
- shard piles.

Do not place two objects on the same tile.

Do not place any object at:

- player start `x = 2`,
- door tile `x = room.width - 1`.

---

## 28.4 Combat room generation

Enemy count:

```js
enemyCount = min(8, 2 + floor + rng.nextInt(0, 2))
```

Enemy spawn range:

```text
x = 8 to room.width - 4
```

Minimum enemy spacing:

```text
2 tiles
```

No enemy may be closer than `4` tiles from player start.

Because the spawn range starts at `8`, this is already satisfied.

### Capacity cap

The raw enemy count formula can exceed the number of valid spaced positions.

Compute capacity:

```js
minX = 8
maxX = room.width - 4
positions = []
for x = minX; x <= maxX; x += 2:
  positions.push(x)

enemyCount = min(enemyCount, positions.length)
```

Choose `enemyCount` positions from `positions`.

## Why cap enemy count?

The gameplay formula can request more enemies than the room can physically contain with the required spacing. Without a cap, generation would either fail or violate spacing rules.

### Enemy type weights

Floor 1:

```text
chaser: 100
```

Floor 2:

```text
chaser: 70
shooter: 30
```

Floor 3:

```text
chaser: 50
spiky: 25
shooter: 25
```

Floor 4:

```text
chaser: 40
spiky: 30
shooter: 30
```

Floor 5:

```text
chaser: 35
spiky: 35
shooter: 30
```

### Optional combat content

| Content | Chance |
|---|---:|
| Barrier | 20% |
| Spike trap | 30% |
| Relic | 30% |
| Shard pile | 50% |

Barrier placement:

- `x` between `10` and `min(16, room.width - 2)`,
- not overlapping enemies.

If no valid tile exists, skip barrier.

Trap placement:

- `x` between `8` and `room.width - 4`,
- not overlapping enemies or barriers.

If no valid tile exists, skip trap.

Relic placement:

- preferred `x = room.width - 3`,
- if occupied, choose nearest free tile between `6` and `room.width - 2`.

If no valid tile exists, skip relic.

Shard pile placement:

- random free tile between `6` and `room.width - 2`.

If no valid tile exists, skip shard pile.

---

## 28.5 Treasure room generation

Treasure rooms have:

- no enemies,
- no traps,
- no barriers,
- `1-2` relics,
- `1-3` shard piles.

Relic placement:

- prefer tiles near door:
  - `room.width - 3`,
  - `room.width - 4`,
  - `room.width - 5`.
- choose distinct free tiles.

If not enough free tiles, reduce relic count.

Shard pile placement:

- random free tiles between `6` and `room.width - 2`.

If not enough free tiles, reduce shard pile count.

---

## 28.6 Trap room generation

Trap rooms have:

- no enemies,
- no barriers,
- `2-3` spike traps,
- `1` relic.

Trap placement:

- `x` between `6` and `room.width - 2`,
- not player start,
- not door,
- minimum spacing `3` tiles.

Use candidate positions:

```js
for x = 6; x <= room.width - 2; x += 3:
  positions.push(x)
```

Choose up to `3` positions.

If not enough positions, reduce trap count.

Relic placement:

- preferred `room.width - 3`,
- otherwise nearest free tile.

---

## 28.7 Boss room generation

Boss room:

- width from boss table,
- boss at `x = room.width - 4`,
- adds between `x = room.width - 10` and `x = room.width - 5`,
- no traps,
- no barriers.

Adds are spawned when the room is created.

Add positions must be distinct and not overlapping the boss.

If not enough positions, reduce adds.

---

# 29. Room validation

`C.rooms.validate(room)` must check:

1. `room.width` is within allowed bounds.
2. `room.doorX === room.width - 1`.
3. No object is at player start `x = 2`.
4. No object is at door `x = room.width - 1`.
5. No two objects occupy the same tile.
6. Combat enemies are within spawn range.
7. Combat enemies have minimum spacing `2`.
8. Trap room traps have minimum spacing `3`.
9. Treasure rooms have no enemies, traps, or barriers.
10. Trap rooms have no enemies or barriers.
11. Boss rooms have no traps or barriers.
12. Boss is at `room.width - 4`.
13. Boss adds are within allowed range.
14. Enemy types are unlocked for the floor.
15. Every enemy has positive HP.
16. Every barrier has positive HP.
17. Every trap has safe duration `1.0`.

If validation returns errors, the room is invalid.

## Why a validator?

Procedural generation can silently produce unfair or broken rooms. A validator gives tests a single source of truth for generation invariants.

---

# 30. Bosses

`js/bosses.js` owns boss definitions and boss update logic.

## 30.1 Boss definitions

```js
C.BOSSES = {
  1: {
    name: "Clockwork Golem",
    hp: 250,
    adds: [],
    patterns: ["charge", "stomp", "tripleShot"],
    phases: [
      {
        threshold: 0.5,
        action: "summon",
        type: "chaser",
        count: 2
      }
    ]
  },
  2: {
    name: "Gear Knight",
    hp: 300,
    adds: ["shooter"],
    patterns: ["dash", "doubleShot"],
    phases: [
      {
        threshold: 0.5,
        action: "summon",
        type: "chaser",
        count: 1
      }
    ]
  },
  3: {
    name: "Ritual Beast",
    hp: 350,
    adds: ["spiky", "spiky"],
    patterns: ["spiralShot", "charge"],
    phases: [
      {
        threshold: 0.66,
        action: "summon",
        type: "spiky",
        count: 1
      },
      {
        threshold: 0.33,
        action: "summon",
        type: "chaser",
        count: 1
      }
    ]
  },
  4: {
    name: "Twin Pistons",
    hp: 400,
    adds: ["chaser", "chaser"],
    patterns: ["leftPiston", "rightPiston", "fanShot"],
    phases: [
      {
        threshold: 0.5,
        action: "barrier"
      }
    ]
  },
  5: {
    name: "The Metronome",
    hp: 500,
    adds: ["spiky", "spiky"],
    patterns: ["stomp", "charge", "burst"],
    phases: [
      {
        threshold: 0.66,
        action: "phase",
        phase: 2
      },
      {
        threshold: 0.33,
        action: "phase",
        phase: 3
      }
    ]
  }
}
```

## 30.2 Boss object

```js
{
  id,
  floor,
  name,
  x,
  hp,
  maxHp,
  state: "idle" | "telegraph" | "attack" | "recover",
  stateTimer,
  pattern,
  phase,
  isBoss: true,
  width: 1.0,
  shotQueue: [],
  attackTimer: 0,
  phaseTriggers: {}
}
```

## 30.3 Boss state machine

Boss update order:

1. If boss is dead, return.
2. Check phase thresholds.
3. Decrement `stateTimer`.
4. Execute state behavior.

### Idle

When timer expires:

- choose a pattern,
- set state to `telegraph`,
- set `stateTimer = 0.5`.

### Telegraph

When timer expires:

- start chosen pattern.

### Attack

Pattern-specific behavior.

When attack completes:

- set state to `recover`,
- set `stateTimer = recoverTime`.

### Recover

When timer expires:

- set state to `idle`,
- set `stateTimer = idleInterval`.

Base timings:

```js
idleInterval = 1.0
recoverTime = 0.5
```

Final boss phase 3:

```js
idleInterval = 0.7
recoverTime = 0.3
```

## Why explicit timings?

Bosses must be fair and testable. Random timing without bounds can create unfair patterns or untestable behavior.

---

## 30.4 Boss patterns

All boss attacks must have at least `0.5 s` telegraph.

### Charge

Used by:

- Floor 1 Clockwork Golem,
- Floor 3 Ritual Beast,
- Floor 5 The Metronome.

Behavior:

- after telegraph, boss moves left at `6 tiles/sec`,
- target `x = 2`,
- stops at wall or barrier,
- attack completes when target reached or blocked.

### Dash

Used by Floor 2 Gear Knight.

Behavior:

- after telegraph, boss moves left a fixed distance of `4` tiles,
- clamped to room bounds and barriers.

### Left piston

Used by Floor 4 Twin Pistons.

Behavior:

- same as dash,
- moves left `4` tiles.

### Right piston

Used by Floor 4 Twin Pistons.

Behavior:

- moves right `4` tiles,
- clamped to room bounds and barriers.

### Stomp

Used by:

- Floor 1 Clockwork Golem,
- Floor 5 The Metronome.

Behavior:

- after telegraph, create one spike trap in front of player.

Trap position:

```js
x = round(player.x + 1)
```

Clamp to:

```text
3 to room.width - 2
```

If occupied, choose nearest free tile.

New trap starts in `safe` phase.

### Triple shot

Used by Floor 1 Clockwork Golem.

Behavior:

- after telegraph, fire `3` projectiles,
- spacing `0.25 s`.

### Double shot

Used by Floor 2 Gear Knight.

Behavior:

- after telegraph, fire `2` projectiles,
- spacing `0.2 s`.

### Spiral shot

Used by Floor 3 Ritual Beast.

Behavior:

- after telegraph, fire `5` projectiles,
- spacing `0.15 s`.

### Fan shot

Used by Floor 4 Twin Pistons.

Behavior:

- after telegraph, fire `4` projectiles,
- spacing `0.1 s`.

Because gameplay is single-lane, fan shot is expressed as staggered projectile timing. All projectiles affect the lane.

Visual designers may add slight vertical visual variation, but projectile logic remains one-dimensional.

### Burst

Used by Floor 5 The Metronome.

Behavior:

- after telegraph, fire `5` projectiles rapidly,
- spacing `0.1 s`.

---

## 30.5 Boss phase triggers

Phase triggers fire once when:

```js
boss.hp / boss.maxHp <= threshold
```

For summon actions:

- spawn add at `boss.x - 2`,
- if occupied, choose nearest free tile left of boss,
- clamp to room bounds.

For barrier action:

- spawn barrier between player and boss:
  ```js
  x = round((player.x + boss.x) / 2)
  ```
- clamp to valid free tile.

For final boss phase actions:

- phase 2 unlocks `burst`,
- phase 3 uses faster idle/recover timings.

## 30.6 Boss death

When boss HP reaches `0`:

1. remove boss,
2. destroy all projectiles with `owner === "boss"`,
3. add `100` shards,
4. increment `runStats.bossesKilled`,
5. emit `boss_died`,
6. update door state.

If floor is `5`, trigger victory.

---

# 31. Tutorial hints

Floor 1, Room 1 should show hints.

Track:

```js
room.tutorial = true
run.tutorialStep = 0
```

Hints:

1. On room start:
   - toast `Tap slowly to move`.
2. After first successful Move:
   - toast `Tap in the orange zone to attack`.
3. After first successful Attack:
   - toast `Quick triple-tap to parry`.

Hints disappear after first use.

They are toasts, not blocking dialogs.

---

# 32. HUD and UI

The HUD is DOM-based.

Required DOM IDs:

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

The visual designer owns styling.

Engineering owns:

- required IDs,
- data updates,
- state binding.

## 32.1 HUD updates

Every frame or on state change, update:

- HP bar,
- Tempo marker,
- Parry cooldown overlay,
- Flick indicator,
- floor/room text,
- boss bar,
- relic slots,
- shard count,
- toasts.

Tempo marker position:

```js
markerPercent = player.nextTempo / 100 * 100
```

Parry zone is grayed out while:

```js
player.parryCooldown > 0
```

Flick indicator is visible when:

```js
player.nextAction === "flick"
```

## 32.2 Why DOM HUD?

Text, toasts, and relic slots are easier to make readable and accessible in DOM. Canvas is better for the side-view world.

---

# 33. Rendering

`js/render.js` draws the game world to:

```html
<canvas id="game-canvas"></canvas>
```

If canvas is unavailable, rendering is a no-op.

## 33.1 Camera

Camera follows player.

Camera clamps to room bounds.

Do not render outside current room.

Logical tile size:

```js
tileSize = window.CadenceAssets?.tileSize || 48
```

Camera:

```js
viewTiles = canvas.width / tileSize
cameraX = clamp(player.x - viewTiles / 2, 0, room.width - viewTiles)
```

## 33.2 Render layers

Draw in this order:

1. room background,
2. door,
3. traps,
4. shard piles,
5. relics,
6. barriers,
7. enemies,
8. boss,
9. player,
10. projectiles,
11. effects,
12. damage numbers.

## 33.3 Asset fallback

If sprites are missing, draw simple colored rectangles or circles.

Entity type determines fallback color.

## Why fallback rendering?

The game must be playable and testable before all visual assets are integrated.

---

# 34. Audio

`js/audio.js` owns audio playback.

It must:

- use `window.CadenceAssets.audio` if present,
- no-op if audio assets are missing,
- not throw if audio is unavailable,
- resume audio context on first user input if using Web Audio,
- play short event sounds.

Required audio event names are listed in section 1.2.

Audio must not block logic.

Wrap audio calls in try/catch.

## Why no-op audio?

Headless tests and early integration may not have audio assets. The game must not fail because of missing audio.

---

# 35. Debug API

`js/debug.js` wraps the game instance and exposes:

```js
window.__game
```

This is the only supported test control surface.

## 35.1 Required methods

```js
window.__game.version
window.__game.start()
window.__game.stop()

window.__game.reset(options)
window.__game.newRun(seed)
window.__game.setMode(mode)

window.__game.tap()
window.__game.tick(dt)

window.__game.getState()
window.__game.getSave()
window.__game.setSave(save)
window.__game.getRngSeed()
window.__game.setRngSeed(seed)

window.__game.setTempo(value)
window.__game.setParryCooldown(value)
window.__game.setPlayerHP(value)
window.__game.setPlayerX(value)
window.__game.setShards(value)
window.__game.setPlayerStat(key, value)
window.__game.setPaused(value)

window.__game.setRoom(options)
window.__game.generateFloor(floor, seed)

window.__game.spawnEnemy(type, x)
window.__game.spawnProjectile(x, vx, owner)
window.__game.spawnTrap(x)
window.__game.spawnBarrier(x)
window.__game.spawnRelic(relicId, x)
window.__game.spawnShardPile(x)

window.__game.damagePlayer(hearts, source)
window.__game.damageEnemy(id, amount, knockback)
window.__game.damageBarrier(id, amount)
window.__game.setBossHP(value)

window.__game.getLog()
window.__game.clearLog()
```

## 35.2 `reset(options)`

Options:

```js
{
  seed: 1,
  save: null,
  mode: "title"
}
```

Behavior:

- if `save` is null, use default save,
- set RNG seed,
- clear log,
- clear input queue,
- set mode to `title` unless specified otherwise,
- clear run state.

## 35.3 `newRun(seed)`

Behavior:

- if seed provided, set RNG seed,
- start a new run from current save,
- enter Floor 1, Room 1.

## 35.4 `tap()`

Enqueues a tap.

Does not immediately resolve action.

Action resolves during:

```js
tick(dt)
```

## 35.5 `tick(dt)`

Advances simulation by `dt` seconds.

Must work with:

```js
dt = 0
```

A `tick(0)` should still process queued taps.

## 35.6 `getState()`

Returns a serializable snapshot.

Required shape:

```js
{
  mode: "title" | "upgrade" | "run" | "death" | "victory",
  paused: boolean,
  time: number,

  save: {
    version: 1,
    shards: number,
    upgrades: {
      vitality: number,
      blade: number,
      pulse: number,
      ward: number
    },
    bestFloor: number
  },

  player: null | {
    x: number,
    hp: number,
    maxHp: number,
    maxHearts: number,
    tempo: number,
    nextTempo: number,
    nextAction: "move" | "attack" | "parry" | "flick",
    parryCooldown: number,
    parryCooldownMax: number,
    iFrameTimer: number,
    parryIFrameTimer: number,
    moveDistance: number,
    attackDamage: number,
    parryDamage: number,
    flickDamage: number,
    attackRange: number,
    parryRadius: number,
    flickRadius: number,
    tempoDecay: number,
    echoChance: number,
    thornDamage: number,
    clockworkStacks: number,
    relics: string[]
  },

  room: null | {
    floor: number,
    index: number,
    type: "combat" | "treasure" | "trap" | "boss",
    width: number,
    doorX: number,
    doorState: "locked" | "open",
    cleared: boolean,
    tutorial: boolean
  },

  enemies: [
    {
      id: number,
      type: string,
      x: number,
      hp: number,
      maxHp: number,
      fireTimer: number,
      thornTimer: number,
      kbTimer: number
    }
  ],

  projectiles: [
    {
      id: number,
      x: number,
      vx: number,
      owner: "enemy" | "boss"
    }
  ],

  traps: [
    {
      id: number,
      x: number,
      phase: "safe" | "warning" | "danger",
      timer: number
    }
  ],

  barriers: [
    {
      id: number,
      x: number,
      hp: number,
      maxHp: number
    }
  ],

  relics: [
    {
      id: number,
      x: number,
      relicId: string
    }
  ],

  shardPiles: [
    {
      id: number,
      x: number
    }
  ],

  boss: null | {
    id: number,
    floor: number,
    name: string,
    x: number,
    hp: number,
    maxHp: number,
    state: "idle" | "telegraph" | "attack" | "recover",
    pattern: string | null,
    phase: number,
    stateTimer: number,
    shotQueueLength: number
  },

  shards: number,

  runStats: {
    shardsEarned: number,
    enemiesKilled: number,
    bossesKilled: number,
    roomsCleared: number
  },

  upgrade: null | {
    cursor: number,
    cursorTimer: number,
    lastTapTime: number,
    autoReturnActive: boolean,
    autoReturnTimer: number
  },

  lastAction: null | {
    type: "move" | "attack" | "parry" | "flick",
    blocked: boolean,
    tempoBefore: number,
    tempoAfter: number,
    damage: [
      {
        id: number,
        amount: number
      }
    ]
  },

  toasts: string[]
}
```

## 35.7 `getLog()`

Returns a copy of the event log.

Log entries should include:

```js
{
  t: game.time,
  event: string,
  ...data
}
```

Important events:

```text
tap
move
attack
parry
flick
player_damage
enemy_damage
enemy_died
barrier_broken
projectile_destroyed
trap_damage
relic_pickup
relic_converted
shard_pickup
room_cleared
door_unlock
boss_phase
boss_died
upgrade_buy
cannot_buy
maxed
death
victory
```

## Why log?

Tests need to verify sequences, not only final state.

For example:

- a Parry should produce `parry` then `enemy_damage`,
- a Flick should produce `flick` but not `parry`,
- a room clear should produce `room_cleared` once.

---

# 36. Test harness

`js/test-harness.js` provides a tiny browser test framework.

No external test runner is used.

Required globals:

```js
window.__test
window.__runTests
window.__testResults
```

## 36.1 Harness API

```js
window.__test.it(name, fn)
window.__test.assert(condition, message)
window.__test.assertClose(actual, expected, epsilon, message)
window.__test.assertDeep(actual, expected, message)
window.__test.results()
```

`window.__runTests()` runs all tests synchronously and returns:

```js
{
  total: number,
  passed: number,
  failed: number,
  failures: [
    {
      name: string,
      message: string,
      stack: string
    }
  ]
}
```

It also assigns the same object to:

```js
window.__testResults
```

## 36.2 Test helpers

`js/tests.js` should define helpers:

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

Tests must not use real timers.

Use:

```js
game.tick(dt)
```

for all simulation time.

## 36.3 Why synchronous tests?

The handoff environment has no test runner. Synchronous tests are easier to run in a headless page and avoid promise timing flakiness.

---

# 37. Required tests

The test suite must prove the game is finished and playable.

Tests should be deterministic.

Use seeds.

Use `tick()` for time.

Use `assertClose()` for floating point values.

---

## 37.1 Bootstrap tests

### T01 Debug API exists

Assert:

```js
window.__game exists
window.__game.getState exists
window.__game.tap exists
window.__game.tick exists
```

### T02 Test harness exists

Assert:

```js
window.__test exists
window.__runTests exists
```

### T03 Reset produces title state

```js
window.__game.reset({ seed: 1 });
const s = window.__game.getState();
assert(s.mode === "title");
```

---

## 37.2 Tempo tests

### T04 First tap is Move

```js
resetGame(1);
window.__game.newRun(1);
window.__game.tap();
window.__game.tick(0);

const s = window.__game.getState();
assertClose(s.player.x, 3, 1e-6);
assertClose(s.player.tempo, 30, 1e-6);
assert(s.lastAction.type === "move");
assert(s.lastAction.blocked === false);
```

### T05 Tempo decay enables Move

After first Move, Tempo is `30`.

Wait `0.7 s`:

```js
window.__game.tick(0.7);
window.__game.tap();
window.__game.tick(0);
```

Expected:

```js
player.tempo === 39
lastAction.type === "move"
player.x increased by moveDistance
```

### T06 Rapid taps produce Move, Attack, Parry

Start fresh run.

Call:

```js
window.__game.tap();
window.__game.tap();
window.__game.tap();
window.__game.tick(0);
```

Expected log action sequence:

```text
move
attack
parry
```

Expected final:

```js
player.tempo === 0
player.parryCooldown > 0
player.parryIFrameTimer > 0
```

### T07 Tempo cap and Flick

Set:

```js
window.__game.setTempo(100);
window.__game.setParryCooldown(0);
```

Tap:

Expected:

```js
lastAction.type === "parry"
```

Then:

```js
window.__game.setTempo(100);
window.__game.setParryCooldown(0.5);
```

Tap:

Expected:

```js
lastAction.type === "flick"
player.tempo === 0
```

### T08 Next action preview

Set Tempo values and assert `player.nextAction`.

Examples:

| Tempo | Parry cooldown | Expected nextAction |
|---:|---:|---|
| 0 | 0 | move |
| 10 | 0 | attack |
| 40 | 0 | parry |
| 40 | 0.5 | flick |
| 80 | 0 | parry |
| 80 | 0.5 | flick |

---

## 37.3 Action tests

### T09 Move blocked by enemy

Spawn enemy at `x = 4`.

Set player `x = 3`.

Set Tempo `0`.

Tap.

Expected:

```js
lastAction.type === "move"
lastAction.blocked === true
player.x === 3
```

### T10 Move blocked by barrier

Spawn barrier at `x = 4`.

Set player `x = 3`.

Tap Move.

Expected blocked.

### T11 Move blocked by locked door

Set player near door.

Ensure door locked.

Tap Move.

Expected blocked.

### T12 Attack damages enemy in hitbox

Spawn enemy at `x = 4`.

Set player `x = 3`.

Set Tempo `50`.

Tap.

Expected:

```js
lastAction.type === "attack"
enemy.hp decreased by attackDamage
player.x unchanged
```

### T13 Attack destroys projectile

Spawn projectile in attack hitbox.

Set Tempo `50`.

Tap.

Expected projectile removed.

### T14 Parry grants i-frames and damage

Spawn enemy in parry radius.

Set player `x = 3`.

Set Tempo `80`.

Set Parry cooldown `0`.

Tap.

Expected:

```js
lastAction.type === "parry"
player.tempo === 0
player.parryIFrameTimer > 0
player.parryCooldown > 0
enemy.hp decreased
```

### T15 Parry knockback

Spawn enemy at `x = 4`.

Set player `x = 3`.

Parry.

Tick `0.2 s`.

Expected enemy `x` increased by approximately `2`.

### T16 Boss knockback is 50%

Spawn boss at `x = 5`.

Set player `x = 3`.

Ensure boss is within parry radius.

Parry.

Tick `0.2 s`.

Expected boss `x` increased by approximately `1`.

### T17 Flick is weaker and has no i-frames

Spawn enemy in flick radius.

Set Tempo `80`.

Set Parry cooldown `0.5`.

Tap.

Expected:

```js
lastAction.type === "flick"
player.tempo === 0
player.parryIFrameTimer === 0
enemy.hp decreased by flickDamage
```

### T18 Player damage and i-frames

Set player HP to `40`.

Deal `1 heart` damage.

Expected:

```js
player.hp === 0
mode === "death"
```

For i-frame test:

Set player HP to `200`.

Deal damage.

Immediately deal damage again.

Expected second damage ignored.

---

## 37.4 Room generation tests

Use:

```js
window.__game.generateFloor(floor, seed)
```

and:

```js
C.rooms.validate(room)
```

If `C.rooms` is not exposed globally, expose it through debug:

```js
window.__game.validateRoom(room)
```

Recommended: expose both.

### T19 Floor sequence

For each floor `1-5`, generate with multiple seeds.

Assert:

- Floor 1 sequence:
  ```text
  combat, treasure, combat, trap, boss
  ```
- Floors 2-5:
  - room 0 is combat,
  - room 4 is boss,
  - at least one Treasure among rooms 1-3.

### T20 Room widths

Assert normal room widths match:

```js
14 + floor * 2 + randomInt(0,4)
```

clamped to `14-28`.

Assert boss widths:

```js
20 + floor * 2
```

### T21 Combat room invariants

For many seeds:

- enemy count is at least `1` and at most `8`,
- enemy count does not exceed spaced capacity,
- enemy positions are between `8` and `width - 4`,
- enemy spacing is at least `2`,
- enemy types are unlocked for floor,
- no object at player start or door,
- no overlapping objects.

### T22 Treasure room invariants

- no enemies,
- no traps,
- no barriers,
- `1-2` relics,
- `1-3` shard piles,
- no overlapping objects.

### T23 Trap room invariants

- no enemies,
- no barriers,
- `2-3` traps,
- trap spacing at least `3`,
- `1` relic,
- no object at player start or door.

### T24 Boss room invariants

- boss exists,
- boss at `width - 4`,
- adds within `width - 10` to `width - 5`,
- no traps,
- no barriers.

### T25 Every generated room is clearable

For each generated room:

1. enter room via debug,
2. kill all enemies,
3. break all barriers,
4. if boss exists, set boss HP to `0`,
5. tick until door open.

Expected:

```js
room.doorState === "open"
room.cleared === true
```

### T26 Every trap has a safe phase

For generated traps:

- `safeDuration === 1.0`,
- cycle includes safe phase.

---

## 37.5 Progression tests

### T27 Title starts run

```js
resetGame(1);
window.__game.tap();
window.__game.tick(0);
assert(getState().mode === "run");
assert(getState().room.floor === 1);
assert(getState().room.index === 0);
```

### T28 Room transition

Use a combat room with one enemy.

Kill enemy.

Wait for door open.

Set player `x` to door.

Tick `0.21 s`.

Expected:

- room index increased,
- player `x` reset to `2`,
- room clear bonus added once.

### T29 Boss room to next floor

Use Floor 1 boss room.

Set boss HP to `0`.

Wait for door open.

Teleport to door.

Tick `0.21 s`.

Expected:

- floor `2`,
- room index `0`.

### T30 Final boss triggers victory

Use Floor 5 boss room.

Set boss HP to `0`.

Wait for door open.

Teleport to door.

Tick `0.21 s`.

Expected:

```js
mode === "victory"
shards increased by victory bonus
```

### T31 Death flow

Start run.

Set player HP to `40`.

Damage player.

Expected:

```js
mode === "death"
shards increased by death bonus
```

Tap:

- if shards > 0, mode becomes `upgrade`,
- if shards === 0, mode becomes `title`.

### T32 Full run smoke test

Use a fixed seed.

For each floor `1-5`:

For each room `0-4`:

1. enter room,
2. kill all enemies,
3. break all barriers,
4. if boss exists, set boss HP to `0`,
5. wait for door open,
6. teleport player to door,
7. tick `0.21 s`.

Expected final:

```js
mode === "victory"
save.bestFloor === 5
```

This test does not require manual skill. It proves the procedural dungeon and state machine can reach victory.

### T33 One-button room clear test

This test proves a player can clear a simple combat room using only taps and ticks.

Setup:

- reset game,
- create a Floor 1 combat room,
- clear generated enemies,
- spawn one Chaser at `x = 4`,
- no barrier,
- player at `x = 2`.

Then use only:

```js
window.__game.tap()
window.__game.tick(dt)
```

Script:

1. Tap to Move from `x=2` to `x=3`.
2. Tap immediately to Attack.
3. Wait `0.7 s` so Tempo allows another Attack.
4. Tap to Attack and kill enemy.
5. Wait until Tempo allows Move.
6. Repeat Move taps until player reaches door.
7. Wait for door transition.

Expected:

- no debug state mutation after setup,
- room transition occurs,
- player used only taps.

This is a key “playable” test.

---

## 37.6 Meta progression tests

### T34 Upgrade purchase

Set save shards to `50`.

Enter Upgrade mode.

Tap while cursor is on Vitality.

Expected:

```js
save.upgrades.vitality === 1
save.shards === 0
toast contains "Upgrade purchased"
```

### T35 Cannot buy

Set shards to `49`.

Enter Upgrade mode.

Tap Vitality.

Expected:

```js
save.upgrades.vitality === 0
save.shards === 49
toast contains "Cannot buy"
```

### T36 Maxed upgrade

Set Vitality to `5`.

Enter Upgrade mode.

Tap Vitality.

Expected:

```js
save.upgrades.vitality === 5
toast contains "Maxed"
```

### T37 Upgrade cursor auto-advances

Enter Upgrade mode.

Tick `1.5 s`.

Expected cursor `1`.

Tick another `1.5 s`.

Expected cursor `2`.

### T38 Quick tap cancels Upgrade

Enter Upgrade mode.

Tap once.

Tick `0.1 s`.

Tap again.

Expected:

```js
mode === "title"
```

### T39 Upgrade auto-return when shards are zero

Enter Upgrade mode with shards `0`.

Tick `3.1 s`.

Expected:

```js
mode === "title"
```

### T40 Upgrade auto-return when all maxed

Set all upgrades to `5`.

Set shards to `10`.

Enter Upgrade mode.

Tick `3.1 s`.

Expected:

```js
mode === "title"
```

### T41 Save persistence

Set save.

Call `setSave`.

Call `getSave`.

Expected deep equality.

If `localStorage` is available, reload or re-read save should match.

### T42 Best floor update

Start run.

Enter Floor 3 via debug.

Expected:

```js
save.bestFloor === 3
```

---

## 37.7 Relic tests

### T43 Relic pickup with space

Spawn relic.

Set player on relic.

Tick.

Expected:

- relic removed,
- player relics includes relic ID,
- derived stats updated.

### T44 Relic conversion when full

Set player relics to 5.

Spawn relic.

Set player on relic.

Tick.

Expected:

- relic removed,
- shards increased by rarity conversion,
- player relics length remains 5.

### T45 Tempo decay clamps

Set relics:

- 5 Metronome:
  - expected Tempo decay `10`.
- 5 Glass Heart:
  - expected Tempo decay `50`.

### T46 Move distance clamp

Set relics:

- 5 Spring Boot:
  - expected move distance `1.5`.

### T47 Parry cooldown clamp

Set relics/upgrades to reduce below `0.4`.

Expected parry cooldown max `0.4`.

### T48 Player i-frame clamp

Set relics/upgrades to exceed `1.2`.

Expected player i-frames max `1.2`.

### T49 Echo chance clamp

Set 5 Echo relics.

Expected echo chance `0.5`.

### T50 Clockwork relic

Give player Clockwork.

Perform 3 attacks.

Set Parry cooldown active.

Tap in Parry zone.

Expected:

- Parry occurs,
- clockwork stack consumed,
- Parry cooldown resets.

### T51 Thorn relic

Give player Thorn.

Spawn enemy overlapping player.

Tick `1.0 s`.

Expected enemy HP reduced by `5`.

Tick another `0.5 s`.

Expected no additional Thorn damage yet.

### T52 Echo relic

Set player echo chance to `1` using debug stat setter.

Spawn enemy in attack hitbox.

Attack.

Expected enemy damaged twice.

---

## 37.8 Edge case tests

### T53 Multiple taps in same frame

Queue 3 taps.

Tick once.

Expected all 3 actions processed sequentially.

### T54 Tap while dead is ignored

Enter death mode.

Tap.

Expected mode remains death and no action occurs.

### T55 Tap while paused resumes without action

Start run.

Set paused.

Tap.

Expected:

- paused false,
- no Tempo action occurred.

Tap again.

Expected normal action occurs.

### T56 Projectile leaves room

Spawn projectile near left wall moving left.

Tick until it leaves.

Expected projectile removed.

### T57 Enemy knocked off-screen despawns

Spawn enemy near left edge.

Knock it left beyond `-1`.

Tick tween.

Expected enemy removed.

### T58 Boss death clears boss projectiles

Spawn boss and boss projectiles.

Set boss HP to `0`.

Expected all boss projectiles removed.

### T59 Trap active when player overlaps

Spawn trap in danger phase.

Set player on trap.

Tick.

Expected player damaged.

If player has i-frames, expected no damage.

### T60 Door transition does not occur after death

Start door transition.

Damage player to death before transition completes.

Expected mode death and no room transition.

### T61 Relic slot full does not block pickup

Already covered by T44, but include as explicit edge case.

---

## 37.9 Boss tests

### T62 Every boss can be defeated

For each floor `1-5`:

1. create boss room,
2. set boss HP to `1`,
3. damage boss,
4. assert boss removed,
5. assert boss projectiles cleared,
6. assert door opens.

### T63 Boss telegraph is at least 0.5s

For each boss:

- force boss into telegraph,
- assert `stateTimer` is approximately `0.5`.

### T64 Boss patterns do not softlock

For each boss:

- run boss for `10 s` with player stationary at `x=2`,
- assert no exceptions,
- assert boss remains in room bounds,
- assert projectiles are removed when leaving room,
- assert boss can still be damaged.

This does not require the player to win. It proves the boss does not break the simulation.

---

# 38. UI tests

### T65 Required DOM IDs exist

Assert these elements exist:

```text
#game-canvas
#hud
#hp-bar
#tempo-bar
#tempo-marker
#floor-room
#boss-bar
#relic-slots
#shards
#toasts
#overlay
```

### T66 Floor/room text updates

Start run.

Assert:

```js
document.getElementById("floor-room").textContent
```

contains:

```text
F1 R1
```

After transitioning to room 2:

contains:

```text
F1 R2
```

### T67 Next action is exposed

Assert:

```js
getState().player.nextAction
```

is one of:

```text
move
attack
parry
flick
```

This is the testable equivalent of the HUD marker.

---

# 39. Acceptance mapping

| Gameplay acceptance criterion | Tests |
|---|---|
| Player can move, attack, parry, and die using only one button | T04, T06, T14, T18, T33 |
| Every room can be cleared without softlock | T25, T28, T32 |
| Every enemy can be damaged by at least one player action | T12, T14, T17, T33 |
| Every barrier can be broken | T10, T12, T25 |
| Every trap has a safe phase | T26 |
| Every boss can be defeated | T30, T62 |
| Player can reach victory | T30, T32 |
| Player can die and continue to meta progression | T31, T34 |
| Player can buy upgrades with one button | T34, T38 |
| HUD clearly shows what the next tap will do | T08, T67 |
| Game does not require any input other than one tap | T33, input design |

---

# 40. Important engineering decisions and why

## 40.1 Classic scripts instead of modules

**Decision:** Use classic `<script>` files and a global `Cadence` namespace.

**Why:** The environment has no build step and may run under minimal static hosting or `file://`. ES modules can fail due to import/CORS restrictions. Classic scripts are the most portable.

## 40.2 Single global namespace

**Decision:** All code attaches to `window.Cadence`.

**Why:** Prevents accidental global pollution and gives one predictable integration surface.

## 40.3 Debug API as the test seam

**Decision:** Tests drive the game through `window.__game`.

**Why:** The handoff requirement says tests run in a headless page and check state. A deterministic debug API is the only reliable way to validate logic without real input, audio, or visuals.

## 40.4 Seeded RNG

**Decision:** All randomness uses a seeded RNG.

**Why:** Procedural rooms, relic drops, shard piles, and Echo rolls must be reproducible in tests.

## 40.5 Manual tick

**Decision:** `window.__game.tick(dt)` advances simulation.

**Why:** Real time causes flaky tests. Manual tick makes tests deterministic.

## 40.6 Integer tile placement

**Decision:** Generated objects use integer tile positions.

**Why:** It makes overlap, spacing, and softlock validation simple and robust.

## 40.7 Enemy count capacity cap

**Decision:** Combat enemy count is capped to the number of valid spaced positions.

**Why:** The gameplay formula can request more enemies than the room can contain while respecting minimum spacing. Without a cap, generation would violate rules or fail.

## 40.8 Door opens only when enemies/barriers are dead

**Decision:** Traps, relics, and shard piles do not lock the door.

**Why:** Traps must have safe phases. If traps locked the door, timing mistakes could create softlocks.

## 40.9 Room entry resets Tempo and cooldowns

**Decision:** Entering a new room resets Tempo, Parry cooldown, and i-frames.

**Why:** New rooms should be tactically clean. Carrying hot Tempo or cooldowns into a new room would create hidden unfairness and reduce HUD predictability.

## 40.10 Shooter fire line-of-sight

**Decision:** Shooters do not fire if a barrier blocks them or if they are too close.

**Why:** Prevents projectiles from spawning directly on the player with no reaction time.

## 40.11 Boss telegraph timer

**Decision:** All boss attacks use a `0.5 s` telegraph state.

**Why:** The gameplay document requires at least `0.5 s` warning before active damage.

## 40.12 Relic drop weights

**Decision:** Use 60% Common, 30% Rare, 10% Epic.

**Why:** The gameplay document defines relics but not drop weights. This distribution supports build variety and meta pacing without making epics too common.

## 40.13 Canvas world plus DOM HUD

**Decision:** World renders to canvas; HUD uses DOM.

**Why:** Canvas scales well for many entities. DOM is better for readable text, toasts, relic slots, and accessibility.

## 40.14 Audio no-op fallback

**Decision:** Missing audio assets do not break the game.

**Why:** The game must be testable and playable before all audio assets are integrated.

---

# 41. Cut list

These are intentionally not included:

- no second button,
- no hold input,
- no directional input,
- no jumping,
- no vertical movement,
- no 2.5D or 3D depth,
- no pause button,
- no level select,
- no crafting,
- no in-run shop,
- no multiplayer,
- no endless mode,
- no puzzle rooms,
- no backtracking,
- no build system,
- no TypeScript,
- no external runtime libraries,
- no server,
- no network gameplay.

If a feature requires a separate input axis or separate decision axis, it is cut.

---

# 42. Final implementation checklist

The implementation is complete when:

1. `index.html` loads and runs in a browser.
2. `test.html` loads and runs all tests in a headless page.
3. `window.__game` exists.
4. `window.__runTests()` returns `failed === 0`.
5. The player can play using only one button.
6. Tempo, Move, Attack, Parry, and Flick behave exactly as specified.
7. Rooms are generated procedurally and pass validation.
8. All rooms can be cleared.
9. All bosses can be defeated.
10. Death and victory flow into Upgrade or Title correctly.
11. Upgrades can be purchased with one button.
12. Save state persists across runs when storage is available.
13. Missing visual/audio assets do not break gameplay.
14. No input other than tap is required.