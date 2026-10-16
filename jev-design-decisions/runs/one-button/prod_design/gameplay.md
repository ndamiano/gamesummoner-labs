# `gameplay.md`

## 0. Scope and handoff note

This document defines the playable gameplay for a one-button roguelike. The visual designer owns imagery, the engineering agent owns implementation, and the audio/visual agent owns sound specifics. This document defines what must be played, displayed, generated, progressed through, and how it should feel.

Working title: **Cadence**

One-sentence design:  
A one-button, tempo-based side-view roguelike where slow taps move the player forward, medium taps attack, and fast taps trigger a defensive parry.

The core fantasy is:  
**Your rhythm is your controller.** The player is not choosing between buttons. The player is choosing between speeds of pressing.

---

## 1. Core design pillars

1. **One button, one skill: cadence**
   - The only input is a tap.
   - The game converts recent tap speed into a readable **Tempo** value.
   - Tempo determines the next action.

2. **Readable tempo**
   - The HUD shows a Tempo marker.
   - The marker tells the player what their next tap will do.
   - The player should never have to guess whether their next tap will move, attack, or parry.

3. **Heat and risk**
   - Fast input is powerful but “heats up” the player.
   - If the player is too hot, they cannot safely move.
   - Wasting a fast tap can cause a weak **Flick** instead of a full Parry.

4. **Roguelike loop**
   - Permadeath.
   - Procedural rooms.
   - Random relics.
   - Meta progression between runs.
   - Five floors, ending in a final boss.

5. **No hidden inputs**
   - No hold, no direction, no second button.
   - If a mechanic requires a separate input to understand, it is cut.

---

## 2. Dimensionality

### Decision: 2D side-view, single-lane gameplay

The game is **2D side-view**.

The playable space is a horizontal corridor. The player moves only rightward through rooms. There is no vertical movement, no jumping, no directional control, and no depth axis.

### Why not 2.5D or 3D?

- A one-button game cannot support depth movement.
- Depth would create unfair positioning that the player cannot control.
- The entire skill should be temporal: **how fast you press**.
- A flat side-view corridor makes the Tempo system readable.

### Why single-lane?

- The player has no left/right or up/down control.
- A single lane keeps the challenge about timing, not spatial navigation.
- Enemies, projectiles, traps, and barriers all exist on the same horizontal line.
- This makes the game easier to balance and easier to read at a glance.

---

## 3. Space and layout

### 3.1 Overall dungeon structure

The dungeon is a linear sequence of rooms.

A run has:

- **5 Floors**
- Each floor has:
  - 4 normal rooms
  - 1 boss room

The player always enters a room from the left and exits through a door on the right.

There is no backtracking.

### 3.2 Room size

Room width scales with floor:

| Floor | Normal room width |
|---:|---:|
| 1 | 16–20 tiles |
| 2 | 18–22 tiles |
| 3 | 20–24 tiles |
| 4 | 22–26 tiles |
| 5 | 24–28 tiles |

Boss room width:

| Floor | Boss room width |
|---:|---:|
| 1 | 22 tiles |
| 2 | 24 tiles |
| 3 | 26 tiles |
| 4 | 28 tiles |
| 5 | 30 tiles |

Tile unit:

- 1 tile = 1 gameplay unit.
- Player starts at x = 2.
- Door is at x = room width - 1.

### 3.3 Room types

Normal rooms can be one of:

1. **Combat**
   - Enemies.
   - Optional barrier.
   - Optional trap.
   - Optional relic.

2. **Treasure**
   - No enemies.
   - 1–2 relics.
   - 1–3 shard piles.

3. **Trap**
   - No enemies.
   - 2–3 spike traps.
   - 1 relic.

Boss rooms:

- Boss.
- Optional adds.
- No normal traps.
- No barriers.

### 3.4 Room sequence

To ensure a smooth learning curve:

| Floor | Room 1 | Room 2 | Room 3 | Room 4 | Room 5 |
|---:|---|---|---|---|---|
| 1 | Combat tutorial | Treasure | Combat | Trap | Boss |
| 2 | Combat | Random | Combat | Random | Boss |
| 3 | Combat | Random | Random | Random | Boss |
| 4 | Combat | Random | Random | Random | Boss |
| 5 | Combat | Random | Random | Random | Boss |

Random room weights:

| Room type | Weight |
|---|---:|
| Combat | 60% |
| Treasure | 25% |
| Trap | 15% |

If a floor has no Treasure room among rooms 2–4, room 3 becomes Treasure.

### 3.5 Door rules

A room door is locked until:

- All enemies are dead, and
- All barriers are broken.

When the door opens:

- If the player is not on the door tile, they must tap to move into it.
- If the player is already overlapping the door tile, transition after 200 ms.

### 3.6 Camera

- Side-view camera follows the player.
- Camera clamps to room bounds.
- Camera does not expose areas outside the current room.

---

## 4. One-button input: Tempo system

### 4.1 Core input

The only input is a **tap**.

A tap is a press-down event.

- Hold duration has no effect.
- Release has no effect.
- If the player holds the button, only the initial press-down counts.
- If multiple taps occur in the same frame, process them sequentially.

### 4.2 Tempo is the abstraction of press speed

The game does not directly ask for “move” or “attack.”  
The player presses one button at different rates, and the game converts that into **Tempo**.

Tempo is a value from **0 to 100**.

- Tapping raises Tempo.
- Tempo decays over time.
- The action performed is determined by the Tempo value **after the tap is applied**.

This is important: the player is not choosing an action directly. They are choosing a cadence, and the cadence determines the action.

### 4.3 Tempo constants

| Constant | Value |
|---|---:|
| Max Tempo | 100 |
| Tempo gain per tap | +30 |
| Tempo decay | 30 per second |
| Move zone | 0–39 |
| Attack zone | 40–69 |
| Parry zone | 70–100 |

### 4.4 Tempo update algorithm

Every frame:

```ts
tempo = max(0, tempo - TEMPO_DECAY * dt)
parryCooldown = max(0, parryCooldown - dt)
```

On tap:

```ts
tempo = min(100, tempo + TAP_GAIN)

if tempo <= 39:
    performMove()
else if tempo <= 69:
    performAttack()
else:
    if parryCooldown <= 0:
        performParry()
        tempo = 0
        parryCooldown = PARRY_COOLDOWN
    else:
        performFlick()
        tempo = 0
```

### 4.5 HUD marker

The HUD displays a marker representing the **next tap result**.

The marker value is:

```ts
nextTempo = min(100, tempo + TAP_GAIN)
```

This is the exact value that would be used if the player tapped right now.

The marker moves down over time as Tempo decays.

The player should read the HUD like this:

- Marker in **Move zone**: next tap moves.
- Marker in **Attack zone**: next tap attacks.
- Marker in **Parry zone**: next tap parries, unless Parry is on cooldown.
- Marker in **Parry zone while Parry is on cooldown**: next tap Flicks.

### 4.6 Action table

| Action | Tempo after tap | Effect | Tempo after action | Cooldown |
|---|---:|---|---:|---:|
| Move | 0–39 | Advance forward by Move Distance | Unchanged | None |
| Attack | 40–69 | Forward melee attack | Unchanged | None |
| Parry | 70–100 | Defensive pulse with i-frames and knockback | Reset to 0 | 0.8 s |
| Flick | 70–100 while Parry on cooldown | Weak pulse | Reset to 0 | None |

### 4.7 Why this feels like “how fast you press it”

- Slow tapping lets Tempo fall into the Move zone.
- Medium tapping keeps Tempo in the Attack zone.
- Fast tapping pushes Tempo into the Parry zone.
- If the player over-presses while Parry is unavailable, they waste the burst on a Flick.

The player learns to press not just “fast” or “slow,” but at the right moment relative to the Tempo marker.

---

## 5. Player actions

### 5.1 Move

Move is the low-Tempo action.

Effect:

- Player attempts to advance forward by **Move Distance**.
- Base Move Distance is **1 tile**.
- If the target position is blocked by a wall, barrier, or enemy, the move does not happen.
- Tempo still changes even if the move is blocked.

Move Distance can be modified by relics:

- Base: 1.0 tile
- Maximum: 1.5 tiles

Move feel:

- Move is the safest action.
- It is also the slowest action.
- To move repeatedly, the player must let Tempo cool.

Expected movement rhythm:

- After a Move, Tempo is usually around 30.
- To make the next tap a Move again, Tempo must decay to 9 or lower.
- With base decay of 30/sec, this takes about **0.7 seconds**.
- So base movement is roughly **1.4 taps per second**.

### 5.2 Attack

Attack is the mid-Tempo action.

Effect:

- Deals **Attack Damage** to enemies and barriers in a forward hitbox.
- Destroys projectiles in the hitbox.
- Does not move the player.
- Does not reset Tempo.

Attack hitbox:

- Starts at the player’s front.
- Extends **1.5 tiles** forward.
- Covers the full lane height.

Base Attack Damage:

- 15

Attack can be modified by upgrades and relics.

Expected attack rhythm:

- A single Attack can leave the player “hot.”
- Sustained tapping will eventually push Tempo into the Parry zone.
- The player should attack in bursts, not as a continuous button mash.

Typical burst:

- 2–3 Attacks, then Parry or cooldown.

### 5.3 Parry

Parry is the high-Tempo action.

Effect:

- Grants **0.3 seconds** of invulnerability.
- Deals **Parry Damage** in a radius around the player.
- Knocks back enemies in the radius.
- Destroys projectiles in the radius.
- Resets Tempo to 0.
- Starts Parry cooldown.

Parry radius:

- 1.5 tiles around the player.

Base Parry Damage:

- 10

Base Parry cooldown:

- 0.8 seconds

Parry feel:

- Parry is the most powerful action.
- It is also the most expensive.
- It resets Tempo, so the player must rebuild Tempo before parrying again.
- If Parry is on cooldown, a high-Tempo tap becomes a Flick.

### 5.4 Flick

Flick is the failed Parry.

It occurs when:

- Tempo after tap is 70–100, but
- Parry cooldown is still active.

Effect:

- Deals **2 damage** in a radius around the player.
- Destroys projectiles in a smaller radius.
- No invulnerability.
- Resets Tempo to 0.

Flick radius:

- 1.0 tile

Flick is not useless, but it is clearly weaker than Parry. It exists so that over-pressing has a defined, non-broken result.

---

## 6. Player stats and combat rules

### 6.1 Player base stats

| Stat | Base value |
|---|---:|
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

### 6.2 Damage taken

All normal enemy attacks deal **1 heart**, or **40 HP**.

Sources:

- Enemy contact
- Projectiles
- Spike traps
- Boss attacks

If the player has active i-frames, damage is ignored.

Player i-frames:

- Base: 0.8 seconds
- Can be increased by upgrades/relics
- Maximum: 1.2 seconds

### 6.3 Enemy damage

Enemies deal damage by:

- Contact
- Projectiles
- Boss patterns

All enemy damage is normalized to 1 heart unless stated otherwise.

### 6.4 Player attack rules

Attack:

- Hits all enemies/barriers in the forward hitbox.
- Destroys projectiles in the forward hitbox.
- Does not knock enemies back.

Parry:

- Hits all enemies/barriers in radius.
- Destroys projectiles in radius.
- Knocks enemies back.

Flick:

- Hits all enemies/barriers in radius.
- Destroys projectiles in radius.
- No knockback.
- No i-frames.

### 6.5 Knockback

When an enemy is knocked back:

- It moves away from the player by **2 tiles**.
- Movement is a short tween, about 100 ms.
- If blocked by a wall, it stops.
- If knocked off-screen left, it despawns.

Boss knockback:

- Bosses take only **50% knockback**.

Barriers:

- Barriers do not move.

### 6.6 Enemy contact blocking

If an enemy occupies the tile the player is trying to move into, the Move action is blocked.

This means:

- The player cannot simply walk through enemies.
- The player must Attack, Parry, or Flick to remove or knock back the enemy.

Projectiles do not block movement. If the player moves into a projectile, collision rules apply.

### 6.7 Projectile rules

Projectiles:

- Move horizontally toward the player.
- Deal 1 heart on hit.
- Are destroyed by:
  - Attack hitbox
  - Parry radius
  - Flick radius
- Despawn if they leave the room.

Base projectile speed:

- 4 tiles/sec
- Scales by floor.

---

## 7. Room generation algorithm

### 7.1 General generation function

For each floor:

1. Create room sequence.
2. For each normal room:
   - Choose width.
   - Populate based on room type.
3. Create boss room.
4. Apply floor difficulty scaling.

### 7.2 Normal room width

```ts
width = 14 + floor * 2 + randomInt(0, 4)
```

Then clamp to reasonable bounds:

- Minimum: 14
- Maximum: 28

### 7.3 Combat room generation

Enemy count:

```ts
enemyCount = min(8, 2 + floor + randomInt(0, 2))
```

Enemy placement:

- Spawn x positions between 8 and room width - 4.
- Minimum spacing between enemies: 2 tiles.
- No enemy may spawn closer than 4 tiles from the player start.

Optional content:

| Content | Chance |
|---|---:|
| Barrier | 20% |
| Spike trap | 30% |
| Relic | 30% |
| Shard pile | 50% |

Barrier placement:

- x between 10 and 16.
- Not overlapping enemies.

Trap placement:

- x between 8 and room width - 4.
- Not overlapping enemies or barriers.

Relic placement:

- Usually near the door: x = room width - 3.
- If blocked, choose nearest free tile.

Shard pile placement:

- Random free tile between x = 6 and door.

### 7.4 Treasure room generation

- No enemies.
- 1–2 relics.
- 1–3 shard piles.
- No traps.
- No barriers.

### 7.5 Trap room generation

- No enemies.
- 2–3 spike traps.
- 1 relic.
- No barriers.

Trap placement:

- Spaced at least 3 tiles apart.
- Not at player start or door.

### 7.6 Boss room generation

- Width from boss table.
- Boss spawns near the door: x = room width - 4.
- Adds spawn between x = room width - 10 and x = room width - 5.
- No traps.
- No barriers.

---

## 8. Difficulty scaling

### 8.1 Enemy HP scaling

```ts
enemyHP = baseHP * (1 + 0.15 * (floor - 1))
```

### 8.2 Enemy speed scaling

```ts
enemySpeed = baseSpeed * (1 + 0.05 * (floor - 1))
```

### 8.3 Projectile speed scaling

```ts
projectileSpeed = 4 + 0.5 * (floor - 1)
```

### 8.4 Spike trap danger duration

```ts
dangerDuration = 0.4 + 0.05 * (floor - 1)
```

Floor values:

| Floor | Danger duration |
|---:|---:|
| 1 | 0.4 s |
| 2 | 0.45 s |
| 3 | 0.5 s |
| 4 | 0.55 s |
| 5 | 0.6 s |

### 8.5 Barrier HP scaling

```ts
barrierHP = 40 + 5 * (floor - 1)
```

Floor values:

| Floor | Barrier HP |
|---:|---:|
| 1 | 40 |
| 2 | 45 |
| 3 | 50 |
| 4 | 55 |
| 5 | 60 |

---

## 9. Enemy content

All enemies exist on the single lane.

### 9.1 Chaser

Behavior:

- Moves toward the player.
- Deals contact damage.
- No ranged attack.

Stats:

| Stat | Base value |
|---|---:|
| HP | 30 |
| Speed | 2.0 tiles/sec |
| Contact damage | 1 heart |
| Shards on death | 5 |

Unlocked:

- Floor 1

### 9.2 Spiky

Behavior:

- Faster, weaker chaser.
- Deals contact damage.

Stats:

| Stat | Base value |
|---|---:|
| HP | 20 |
| Speed | 3.0 tiles/sec |
| Contact damage | 1 heart |
| Shards on death | 8 |

Unlocked:

- Floor 3

### 9.3 Shooter

Behavior:

- Tries to keep distance.
- Fires projectiles at the player.

Distance behavior:

- If distance to player is less than 3 tiles, moves away.
- If distance is greater than 5 tiles, moves toward player.
- Otherwise, stays in place.

Stats:

| Stat | Base value |
|---|---:|
| HP | 45 |
| Speed | 1.0 tiles/sec |
| Projectile damage | 1 heart |
| Fire rate | 1 projectile / 2.0 s |
| Projectile speed | 4 tiles/sec base |
| Shards on death | 10 |

Unlocked:

- Floor 2

### 9.4 Barrier

Behavior:

- Stationary.
- Blocks movement.
- Blocks projectiles.
- Can be damaged by Attack, Parry, and Flick.

Stats:

| Stat | Base value |
|---|---:|
| HP | 40, scales by floor |
| Shards on break | 15 |

Unlocked:

- Floor 1

### 9.5 Spike trap

Behavior:

- Covers 1 tile.
- Cycles between safe and dangerous.
- Deals 1 heart if the player overlaps during danger.

Cycle:

| Phase | Duration |
|---|---:|
| Safe | 1.0 s |
| Warning | 0.5 s |
| Danger | 0.4–0.6 s by floor |

The warning phase is visual only.

Unlocked:

- Floor 1

---

## 10. Enemy unlock schedule

| Floor | Available enemies |
|---:|---|
| 1 | Chaser, Barrier, Spike trap |
| 2 | Chaser, Shooter, Barrier, Spike trap |
| 3 | Chaser, Spiky, Shooter, Barrier, Spike trap |
| 4 | Chaser, Spiky, Shooter, Barrier, Spike trap |
| 5 | Chaser, Spiky, Shooter, Barrier, Spike trap |

Enemy type weights for combat rooms:

| Floor | Chaser | Spiky | Shooter |
|---:|---:|---:|---:|
| 1 | 100% | 0% | 0% |
| 2 | 70% | 0% | 30% |
| 3 | 50% | 25% | 25% |
| 4 | 40% | 30% | 30% |
| 5 | 35% | 35% | 30% |

---

## 11. Boss content

Each floor ends with a boss.

Bosses have a health bar displayed in the HUD.

All boss attacks have at least a **0.5 second warning** before the active damage phase.

Boss contact damage:

- 1 heart

Boss attacks:

- 1 heart

Boss knockback:

- 50% of normal knockback

Boss shard reward:

- 100 shards

### 11.1 Floor 1 boss: Clockwork Golem

HP:

- 250

Adds:

- None

Patterns:

1. **Charge**
   - Warns for 0.5 s.
   - Moves quickly across the room.
   - Speed: 6 tiles/sec.

2. **Stomp**
   - Warns for 0.5 s.
   - Creates one spike trap in front of the player.
   - The trap begins its normal cycle.

3. **Triple shot**
   - Fires 3 projectiles in a horizontal line.
   - Projectile spacing: 0.25 s.

Phase transition:

- At 50% HP, summon 2 Chasers.

### 11.2 Floor 2 boss: Gear Knight

HP:

- 300

Adds:

- 1 Shooter

Patterns:

1. **Dash left**
   - Quick dash toward the player.
   - Warning: 0.5 s.

2. **Double shot**
   - Fires 2 projectiles, 0.2 s apart.

3. **Summon**
   - At 50% HP, summon 1 Chaser.

### 11.3 Floor 3 boss: Ritual Beast

HP:

- 350

Adds:

- 2 Spikies

Patterns:

1. **Spiral shot**
   - Fires 5 projectiles in a short burst.
   - Projectile spacing: 0.15 s.

2. **Charge**
   - Same as Floor 1 charge.

3. **Summon**
   - At 66% HP, summon 1 Spiky.
   - At 33% HP, summon 1 Chaser.

### 11.4 Floor 4 boss: Twin Pistons

HP:

- 400

Adds:

- 2 Chasers

Patterns:

1. **Left piston**
   - Boss lunges left.
   - Warning: 0.5 s.

2. **Right piston**
   - Boss lunges right.
   - Warning: 0.5 s.

3. **Fan shot**
   - Fires 4 projectiles in a fan pattern.
   - Since gameplay is single-lane, the fan is expressed as staggered projectile timing and slight vertical visual variation, but all projectiles affect the lane.

4. **Barrier spawn**
   - At 50% HP, spawn one barrier between boss and player.

### 11.5 Floor 5 boss: The Metronome

HP:

- 500

Adds:

- 2 Spikies

The final boss uses all previous patterns in a tempo-based rhythm.

Patterns:

1. **Slow stomp**
   - Creates a spike trap.

2. **Medium charge**
   - Charges across the room.

3. **Fast burst**
   - Fires 5 projectiles rapidly.

Phase thresholds:

| HP | Phase |
|---:|---|
| 100–66% | Slow stomp, medium charge |
| 66–33% | Adds fast burst |
| 33–0% | All patterns, faster timing |

Final boss victory:

- Defeating The Metronome ends the run successfully.

---

## 12. Relic system

Relics are in-run items.

The player can hold up to **5 relics**.

If the player picks up a relic while already at 5 relics:

- The new relic is converted to shards.
- Conversion values:
  - Common: 10 shards
  - Rare: 20 shards
  - Epic: 30 shards

Relic pickup:

- Player overlaps relic.
- Relic is added if space is available.
- If no space, convert to shards.
- Show a toast:
  - “Relic acquired: [name]”
  - or “Relic converted: +X shards”

### 12.1 Relic list

| Relic | Rarity | Effect |
|---|---|---|
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

### 12.2 Stacking rules

- Additive stats stack.
- Cooldown reductions cannot reduce Parry cooldown below 400 ms.
- Tempo decay cannot go below 10/sec.
- Tempo decay cannot go above 50/sec.
- Move Distance cannot exceed 1.5 tiles.
- Player i-frames cannot exceed 1.2 seconds.
- Echo chance cannot exceed 50%.
- Glass Heart can stack max hearts, but each copy also increases Tempo decay.

---

## 13. Shard economy

Shards are the meta currency.

Shards are kept after death or victory.

### 13.1 Shard sources

| Source | Shards |
|---|---:|
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

### 13.2 Expected run income

Approximate:

- Floor 1 run: 150–250 shards
- Floor 2 run: 200–350 shards
- Floor 3 run: 250–400 shards
- Floor 4 run: 300–500 shards
- Full victory: 800–1200 shards

This is approximate and depends on relic drops and deaths.

---

## 14. Meta progression

Meta progression happens between runs.

The player keeps:

- Shards
- Upgrade levels
- Best floor reached

The player loses:

- Relics
- Run HP
- Run position

### 14.1 Upgrade tracks

There are four permanent upgrade tracks.

Each track has 5 levels.

| Upgrade | Effect per level |
|---|---|
| Vitality | +1 max heart |
| Blade | +5 Attack Damage |
| Pulse | -100 ms Parry cooldown and +2 Parry Damage |
| Ward | +100 ms player i-frames |

Base to maximum:

| Upgrade | Base | Max |
|---|---:|---:|
| Vitality | 5 hearts | 9 hearts |
| Blade | 15 Attack Damage | 40 Attack Damage |
| Pulse | 0.8 s cooldown / 10 Parry Damage | 0.4 s cooldown / 20 Parry Damage |
| Ward | 0.8 s i-frames | 1.2 s i-frames |

Upgrade costs:

| Level | Cost |
|---:|---:|
| 1 | 50 |
| 2 | 100 |
| 3 | 200 |
| 4 | 400 |
| 5 | 800 |

Total cost per track:

- 1550 shards

Total cost to max all four tracks:

- 6200 shards

### 14.2 Upgrade state UI

The Upgrade state uses one button, but not the run Tempo system. This keeps menus predictable.

Upgrade state rules:

- Show 5 cards:
  1. Vitality
  2. Blade
  3. Pulse
  4. Ward
  5. Done
- Cursor starts on Vitality.
- Cursor automatically moves to the next card every 1.5 seconds.
- Tap:
  - If less than 0.3 seconds since the last Upgrade tap: cancel and return to Title.
  - Otherwise: confirm the highlighted card.

Confirm behavior:

- If card is an upgrade:
  - If affordable and not maxed, buy it.
  - If not affordable or maxed, show a brief “Cannot buy” feedback.
- If card is Done:
  - Return to Title.

Auto-return:

- If shards are 0 or all upgrades are maxed, return to Title after 3 seconds.

### 14.3 Title state

Title state:

- Shows title.
- Shows best floor.
- Shows total shards.
- Tap to start a new run.

The Title state intentionally does not have a separate shop option. The player buys upgrades after a run ends.

### 14.4 Death and victory flow

Death:

- Show death summary.
- Tap to continue.
- If shards > 0, go to Upgrade state.
- If shards = 0, go to Title.

Victory:

- Show victory summary.
- Tap to continue.
- If shards > 0, go to Upgrade state.
- If shards = 0, go to Title.

---

## 15. Progression through the game

### 15.1 Run structure

A run is a single attempt to reach Floor 5 and defeat The Metronome.

Run flow:

1. Title
2. Floor 1, Room 1
3. Clear rooms
4. Defeat Floor 1 boss
5. Floor 2
6. Continue through Floor 5
7. Defeat final boss
8. Victory
9. Upgrade state
10. Title

Death can occur at any point during the run.

### 15.2 In-run progression

Within a run:

- Rooms get harder.
- New enemy types unlock.
- Relic slots create build variety.
- The player may choose to play defensively or aggressively based on Tempo management.

### 15.3 Meta progression

Between runs:

- Shards are used to permanently improve the player.
- The player can choose different upgrade paths.
- Relic randomness creates different runs.
- The player can retry until they reach victory.

---

## 16. HUD and UI

The HUD must be readable at a glance.

### 16.1 In-run HUD

#### Top left: Player HP

Display:

- Segmented HP bar or heart pips.
- Shows current HP out of max HP.
- Flashes when damaged.

If max hearts exceed 5, use a segmented bar rather than individual icons.

#### Top center: Tempo bar

Display:

- Horizontal bar from 0 to 100.
- Three zones:
  - Move: 0–39
  - Attack: 40–69
  - Parry: 70–100
- A marker shows `nextTempo`.
- The marker should be large enough to read quickly.

Parry cooldown display:

- The Parry zone is grayed out while Parry is on cooldown.
- A small sweep or countdown fills the Parry zone as cooldown recovers.
- If the marker is in the Parry zone but Parry is on cooldown, show a **Flick** indicator.

#### Top right: Floor and room

Display:

- Example: `F3 R2`
- Small text.

#### Boss HP bar

Display only when a boss is active:

- Below the Tempo bar.
- Shows boss name and HP.
- Boss HP is numeric or segmented.

#### Bottom left: Relic slots

Display:

- 5 relic slots.
- Empty slots are visible but dim.
- Filled slots show relic icon.
- If a relic is picked up, show a brief toast.

#### Bottom right: Shards

Display:

- Shard icon.
- Current shard count.

#### Toasts

Use brief center-top toasts for:

- Room cleared
- Relic acquired
- Relic converted
- Boss phase
- Upgrade purchased
- Cannot buy

Toasts should not block gameplay.

### 16.2 Damage feedback

Display brief damage numbers for:

- Player damage dealt
- Player damage taken

This helps the player understand relics and upgrades.

The visual designer owns style, but gameplay requires the numbers to be visible.

### 16.3 Door state

The door must visually communicate:

- Locked
- Unlocking
- Open

Locked door:

- Closed.
- No transition.

Open door:

- Clearly open.
- Player can move into it.

### 16.4 Tutorial hints

Floor 1, Room 1 should show brief hints:

1. “Tap slowly to move”
2. “Tap in the orange zone to attack”
3. “Quick triple-tap to parry”

Hints should appear as short toasts and disappear after first use.

### 16.5 Pause state

There is no pause button.

If the app loses focus:

- Game pauses automatically.
- On regain focus, show a brief “Tap to continue” state.
- Any tap resumes.

This prevents unfair deaths from backgrounding.

---

## 17. Feel and pacing numbers

### 17.1 Expected tap rates

| Action | How the player does it | Approximate tap rate |
|---|---|---:|
| Move | Let Tempo cool, then tap | ~1.4 taps/sec |
| Attack | Tap while Tempo is mid-range | ~1.5–2.5 taps/sec |
| Parry | Quick burst of taps to push Tempo high | ~4–6 taps/sec |
| Flick | Accidental fast tap while Parry is on cooldown | n/a |

### 17.2 Room pacing

Target room time:

- Combat room: 8–15 seconds
- Treasure room: 3–6 seconds
- Trap room: 5–10 seconds
- Boss room: 15–30 seconds

Target full run length:

- 8–15 minutes for a successful run
- Shorter if death occurs early

### 17.3 Combat feel

The player should feel:

- **Cool**: Safe, able to move.
- **Warm**: Offensive, able to attack.
- **Hot**: Dangerous, likely to parry or waste input.

This is the emotional core of the Tempo system.

### 17.4 Feedback requirements

The following events need clear feedback:

- Tap
- Move
- Attack
- Parry
- Flick
- Player damage
- Enemy damage
- Parry cooldown ready
- Room cleared
- Boss phase change
- Relic pickup
- Shard pickup
- Door unlock
- Death
- Victory

The audio/visual agent owns the actual sound and visual style, but gameplay requires these events to be distinguishable.

---

## 18. Edge cases and all-case handling

### 18.1 First tap

- Tempo starts at 0.
- First tap gives Tempo 30.
- First tap is always Move.

### 18.2 Tap while dead

- Ignored.
- No Tempo change.
- No action.

### 18.3 Tap while paused

- Ignored.
- The paused state waits for a resume tap.

### 18.4 Tap while door is closed

- Action still occurs based on Tempo.
- Move does not pass through the door.
- Attack and Parry can still affect enemies/barriers.

### 18.5 Tap while blocked by wall or enemy

- Move is blocked.
- Tempo still changes.
- Attack and Parry still occur.

### 18.6 Multiple taps in same frame

- Process taps sequentially.
- Each tap applies Tempo gain and action logic.

### 18.7 Tempo cap

- Tempo cannot exceed 100.
- If Tempo is 100 and the player taps:
  - If Parry is ready: Parry.
  - If Parry is on cooldown: Flick.

### 18.8 Parry cooldown active

- If Tempo after tap is 70–100 and Parry cooldown is active:
  - Perform Flick.
  - Reset Tempo to 0.

### 18.9 Player overlaps door when door opens

- Transition after 200 ms.

### 18.10 Enemy knocked off-screen

- Despawn enemy.
- No penalty.

### 18.11 Projectile leaves room

- Despawn projectile.

### 18.12 Trap active when player enters

- If player overlaps during danger phase, deal 1 heart.
- If player has i-frames, no damage.

### 18.13 Relic slot full

- Convert new relic to shards.
- Do not block pickup.

### 18.14 Upgrade not affordable

- Confirm fails.
- Show “Cannot buy.”
- Cursor continues auto-advancing.

### 18.15 Upgrade maxed

- Confirm fails.
- Show “Maxed.”

### 18.16 All upgrades maxed

- Upgrade state auto-returns to Title after 3 seconds.

### 18.17 Shards are zero

- Upgrade state auto-returns to Title after 3 seconds.

### 18.18 Boss dies while projectiles exist

- Destroy all remaining boss projectiles.
- Stop boss patterns.
- Show victory or room clear sequence.

### 18.19 Player dies while parrying

- If player HP reaches 0, death occurs.
- Parry i-frames do not prevent death from a hit that is already applied.

### 18.20 Player dies at door

- Death occurs.
- No room transition.

### 18.21 Final boss dies

- Victory.
- Stop all enemies and projectiles.
- Show victory summary.

---

## 19. Cut list

The following are intentionally not included:

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

If a feature requires a separate input or separate decision axis, it is cut.

---

## 20. Load-bearing handoff notes

These decisions are not optional decorations. They are the core gameplay.

1. **Do not add directional input.**
   - The game is one-button by design.
   - Direction would break the cadence skill.

2. **Do not add hold as a meaningful input.**
   - Hold would create a second input dimension.
   - It would undermine “what you do is decided by how fast you press it.”

3. **Do not change the Tempo zones without updating the HUD.**
   - The HUD marker is the player’s primary decision tool.
   - If zones change, the marker, colors, and tutorial text must change too.

4. **Do not make Parry have no cooldown.**
   - Parry is the strongest action.
   - Without cooldown, fast tapping becomes too dominant.

5. **Do not allow backtracking.**
   - The dungeon is linear.
   - Backtracking would require directional or state logic that does not fit the one-button design.

6. **Do not make traps permanently active.**
   - Traps must have a safe phase.
   - A permanently active trap can create an impossible room.

7. **Do not spawn projectiles with no reaction time.**
   - All boss attacks need at least 0.5 s warning.
   - Projectiles must be destroyable by Attack, Parry, or Flick.

8. **Do not let menus inherit run Tempo.**
   - Menus should be predictable.
   - The Upgrade state uses its own simple tap rule.

9. **Do not remove Flick.**
   - Flick is the defined result of over-pressing while Parry is unavailable.
   - Without it, the system has an undefined failure case.

10. **Do not make Move reset Tempo.**
   - Move is meant to be the “cool” action.
   - If Move reset Tempo, the player would not need to manage cadence.

---

## 21. Acceptance criteria

The design is complete when:

- A player can move, attack, parry, and die using only one button.
- Every room can be cleared without softlock.
- Every enemy can be damaged by at least one player action.
- Every barrier can be broken.
- Every trap has a safe phase.
- Every boss can be defeated.
- The player can reach victory.
- The player can die and continue to meta progression.
- The player can buy upgrades with one button.
- The HUD clearly shows what the next tap will do.
- The game does not require any input other than one tap.