# gameplay.md

## 1. Core Premise

This is a single-player, top-down, 2D space salvage game.

The player pilots a small salvage ship around a space station. Wrecks drift in a debris field around the station. The player attaches to a wreck, tows it back to the station, unloads it for salvage score and parts, then uses parts to upgrade the ship. The ship becomes stronger, can tow heavier wrecks, survives longer, and eventually retrieves the final high-value wreck.

Core fantasy:

> “I am a salvage pilot. Every wreck I bring back makes my ship better, and the next wreck is bigger, farther, and more dangerous.”

Core loop:

1. Leave station.
2. Identify a wreck.
3. Approach and attach tow.
4. Return to station while avoiding debris, mines, and tow stress.
5. Dock and unload.
6. Gain salvage score and parts.
7. Upgrade ship.
8. Complete next contract.
9. Retrieve final wreck and win.

Target playtime: 15–25 minutes per full run.

There is no timer, no combat, no weapons, no enemies, and no vertical axis.

---

## 2. Dimensionality

Use **2D top-down**, north-up.

- Logical gameplay exists only on the X/Y plane.
- The camera does not rotate with the ship.
- The ship rotates in 2D.
- All movement, collision, towing, and hazards are 2D.
- Visuals may use parallax background, lighting, or pseudo-depth, but there is no gameplay Z-axis.

Why 2D:

- Towing is easiest to read when the ship, tow line, and wreck are all on one plane.
- A minimap is straightforward.
- Collision and physics are simpler and more stable.
- 2.5D or 3D would add spatial complexity without improving the core salvage loop.

---

## 3. Scope and Cuts

Included:

- One player.
- One ship.
- One station.
- One continuous world.
- Five wreck tiers.
- Four upgrade tracks.
- Five contracts.
- Environmental hazards: debris and mines.
- Checkpointing at station.
- Win state and death state.

Cut:

- Weapons.
- Enemy ships.
- Pirates.
- Cargo capacity.
- Multiple part types.
- Fuel or oxygen.
- Repair kits.
- Trading.
- Multiple stations.
- Side quests.
- Narrative beyond contract names.
- Vertical movement.
- Multiple salvageable objects per run beyond wrecks.
- Save system between runs.

Why these cuts:

- The core verb is towing. Anything that competes with towing dilutes the loop.
- A single part currency prevents softlocks and keeps the economy readable.
- No cargo capacity because the player tows one wreck at a time. Adding cargo would create inventory management that is not central to the fantasy.
- Environmental hazards provide danger without requiring combat systems.
- Checkpointing at the station keeps death fair and keeps progression smooth.

---

## 4. Game Flow

### Main States

1. **Title**
2. **Start**
3. **Contract Active**
4. **At Station**
5. **Upgrade Menu**
6. **Game Over**
7. **Victory**
8. **Paused**

### Start

- The player starts at the station.
- Hull is full.
- Parts are 0.
- All upgrades are level 0.
- Contract 1 is active.
- Ring 1 is unlocked.
- The tutorial begins.

### Contract Progression

- Contracts 1 through 4 are score-based.
- Contract 5 is the final wreck retrieval.
- Completing a contract unlocks the next area.
- Contract score resets after each contract completes.
- Excess score does not carry over.

### Death

- If ship hull reaches 0, the ship is destroyed.
- The player returns to the last station checkpoint.
- The current contract is retried from that checkpoint.
- The player does not restart the whole run.

### Victory

- The player wins by unloading the final wreck, the Aurora Black Box, at the station.

---

## 5. World Layout

The game uses one continuous world.

The station is at the center. Salvage rings expand outward from the station.

### Station

- Position: `(0, 0)`
- Safe zone radius: `120`
- Dock zone radius: `50`
- The station safe zone has no debris and no mines.
- Hull regenerates inside the safe zone.
- The station is not a solid collision object.
- The dock zone is where unloading happens.

### World Boundary

- Outer boundary radius: `3200`
- No wrecks are placed beyond `3200`.
- If the ship crosses the boundary, apply a soft clamp:
  - Reduce outward velocity.
  - Show prompt: `No signal beyond boundary`.

### Rings

| Ring | Radial Range | Unlocked After | Content |
|---|---:|---|---|
| Ring 1 | 120–800 | Start | Tutorial wrecks, low hazards |
| Ring 2 | 800–1600 | Contract 1 | First haulers, first mines |
| Ring 3 | 1600–2400 | Contract 2 | Heavier wrecks, denser hazards |
| Ring 4 | 2400–3000 | Contract 3 | Cargo liners, final prep |
| Final Corridor | 3000–3200 | Contract 4 | Aurora Black Box |

### Content Counts

| Ring | Wrecks | Debris Clusters | Mines |
|---|---|---:|---:|
| Ring 1 | 10 Scrap Cans | 8 | 0 |
| Ring 2 | 6 Transport Haulers, 4 Scrap Cans | 12 | 4 |
| Ring 3 | 4 Fighter Frames, 3 Transport Haulers | 16 | 8 |
| Ring 4 | 3 Cargo Liners, 4 Fighter Frames, 2 Transport Haulers | 20 | 12 |
| Final Corridor | 1 Aurora Black Box | 4 | 6 |

Total wrecks: 37  
Total debris clusters: 60  
Total mines: 30

### Tutorial Placement

Two Ring 1 Scrap Cans are fixed for the tutorial:

- Scrap Can A: `(300, 0)`
- Scrap Can B: `(0, 300)`

The remaining Ring 1 wrecks are procedurally placed.

### Final Wreck Placement

The Aurora Black Box is fixed at:

- `(0, -3000)`

It is only active after Contract 4 completes.

---

## 6. Map Generation Algorithm

Use a seeded random number generator at the start of a run.

### Wreck Placement

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
6. Retry up to 1000 times.
7. If still invalid, place it at the next valid angle in a spiral outward from the center of the ring.

### Debris Placement

For each debris cluster:

1. Sample a position in the ring.
2. Reject if:
   - It is within `120` of the station center.
   - It is within `100` of another debris cluster.
   - It is within `80` of a wreck.
   - It is within `50` of a mine.
3. Assign radius between `25` and `50`.

### Mine Placement

For each mine:

1. Sample a position in the ring or final corridor.
2. Reject if:
   - It is within `200` of the station center.
   - It is within `100` of another mine.
   - It is within `100` of a wreck.
   - It is within `50` of a debris cluster.
3. Accept if valid.

### Locked Rings

- Wrecks in locked rings are not interactive.
- They are not shown on the minimap.
- They do not count toward contracts.
- They may be visually present as inert silhouettes, but no gameplay interaction is allowed until the ring unlocks.

---

## 7. Ship Systems

### Ship Base Stats

| Stat | Base Value |
|---|---:|
| Ship mass | 50 |
| Ship collision radius | 14 |
| Max hull | 100 |
| Thrust | 300 |
| Drag | 1.2 |
| Turn rate | 3.0 rad/s |
| Tow power | 250 |
| Tow attach range | 60 |
| Max tow mass | 50 |
| Scanner level | 0 |

### Movement

The ship uses 2D inertia.

Each frame:

1. Update heading:

```text
heading += turn_input * 3.0 * dt
```

2. Apply thrust if thrust input is active:

```text
velocity += heading_vector * thrust * dt
```

3. Apply brake if brake input is active:

```text
velocity -= velocity * 3.0 * dt
```

4. Apply drag:

```text
velocity -= velocity * 1.2 * dt
```

5. Update position:

```text
position += velocity * dt
```

6. Clamp position to the world boundary.

### Expected Unladen Speed

| Thruster Level | Thrust | Drag | Max Speed |
|---:|---:|---:|---:|
| 0 | 300 | 1.2 | 250 |
| 1 | 360 | 1.2 | 300 |
| 2 | 420 | 1.2 | 350 |
| 3 | 480 | 1.2 | 400 |

Speed is in world units per second.

### Hull

- Hull is the ship’s health.
- Hull does not regenerate outside the station safe zone.
- Inside the station safe zone, hull regenerates at `10` hull per second up to max hull.
- If hull reaches `0`, the ship is destroyed.

### Collision Damage

When the ship collides with a wreck, debris cluster, or another ship-like object:

1. Calculate relative speed.
2. If relative speed is less than `10`, no damage occurs.
3. Otherwise:

```text
ship_damage = clamp(relative_speed * 0.2, 0, 30)
```

Maximum ship collision damage is `30`.

### Wreck Damage

When a wreck is hit:

```text
wreck_damage = clamp(relative_speed * 0.15, 0, 20)
```

Wreck damage reduces wreck integrity.

### Camera

- Camera is centered on the ship.
- Camera does not rotate.
- While towing, if the distance between ship and wreck is greater than `100`, the camera centers on the midpoint between the ship and wreck.
- The camera should keep both the ship and the towed wreck visible whenever possible.

### Controls

| Input | Action |
|---|---|
| A / D or Left / Right | Rotate ship |
| W / Up | Thrust |
| S / Down | Brake |
| Q or E | Attach / detach tow |
| U | Hold to unload |
| Tab or I | Open upgrade menu, station only |
| P or Esc | Pause |

---

## 8. Wreck Systems

### Wreck Tiers

| Wreck | Mass | Initial Integrity | Score | Parts | Tow Requirement | Count |
|---|---:|---:|---:|---:|---|---:|
| Scrap Can | 20 | 50 | 10 | 1 | Level 0 | 14 |
| Transport Hauler | 40 | 90 | 25 | 2 | Level 0 | 9 |
| Fighter Frame | 60 | 130 | 40 | 2 | Level 1 | 8 |
| Cargo Liner | 90 | 180 | 60 | 3 | Level 2 | 3 |
| Aurora Black Box | 120 | 250 | 100 | 4 | Level 3 | 1 |

### Wreck Collision Radius

| Wreck | Radius |
|---|---:|
| Scrap Can | 18 |
| Transport Hauler | 24 |
| Fighter Frame | 26 |
| Cargo Liner | 32 |
| Aurora Black Box | 36 |

### Wreck Integrity

- Each wreck has integrity.
- Integrity starts at the initial value in the table.
- Integrity decreases when the wreck is hit.
- Integrity does not regenerate.
- Wrecks do not break or disappear from damage.
- A wreck with `0` integrity can still be towed and unloadded.

### Parts Yield Based on Integrity

| Integrity at Unload | Parts Received |
|---|---:|
| Greater than 60% of initial integrity | Full parts |
| 30% to 60% of initial integrity | Full parts minus 1 |
| Less than 30% of initial integrity | 0 parts |

Example:

- Cargo Liner normally yields 3 parts.
- If unloaded at 70% integrity, it yields 3 parts.
- If unloaded at 40% integrity, it yields 2 parts.
- If unloaded at 10% integrity, it yields 0 parts.

### Score

- Score is fixed by wreck tier.
- Score is not reduced by damage.
- This prevents a damaged wreck from becoming useless for contract progression.
- Parts are the reward for careful salvage.

### Wreck States

Each wreck has one of these states:

1. **Locked**
   - Not yet unlocked.
   - No interaction.
2. **Active**
   - Can be scanned, towed, and unloadded.
3. **Towed**
   - Currently attached to player ship.
4. **Unloadded**
   - Removed from the world.

### Wreck Information Display

Without Scanner Level 1:

- Wrecks are visible in the world.
- Wrecks appear on the minimap.
- Parts, integrity, and mass are hidden.

With Scanner Level 1:

- When within `200` of a wreck, show:
  - Wreck name.
  - Mass.
  - Part yield.
  - Integrity percentage.

With Scanner Level 2:

- Mines are shown on the minimap.
- Mines show a warning radius.

---

## 9. Tow System

Towing is the core mechanic.

### Attach Conditions

The player can attach to a wreck only if all of the following are true:

1. The wreck is active.
2. The player is not already towing another wreck.
3. The wreck is within the current tow attach range.
4. The wreck mass is less than or equal to the current max tow mass.
5. The relative speed between ship and wreck is less than `50`.

If attachment fails, show a prompt:

- `Too fast to attach`
- `Cannot tow: mass exceeded`
- `Detach current tow first`
- `Out of range`

### Tow Attach Range

| Tow Level | Attach Range |
|---:|---:|
| 0 | 60 |
| 1 | 70 |
| 2 | 80 |
| 3 | 95 |

### Max Tow Mass

| Tow Level | Max Tow Mass |
|---:|---:|
| 0 | 50 |
| 1 | 70 |
| 2 | 100 |
| 3 | 130 |

### Tow Physics

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
   - Extension = distance - rest length.
   - Spring force = `min(tow_power, K * extension)`
   - `K = tow_power / 20`
   - Apply spring force to the wreck toward the ship.
   - Apply opposite force to the ship.
4. Apply damping:
   - Damping opposes relative velocity along the tow line.
   - Damping coefficient:

```text
C = 2 * sqrt(K * (ship_mass + wreck_mass)) * 0.4
```

5. Clamp total tow force to `tow_power`.
6. Apply wreck drag:

```text
wreck_velocity -= wreck_velocity * 3.0 * dt
```

7. Apply normal ship drag to the ship.

### Tow Stress and Line Snap

- If the spring force exceeds `1.25 * tow_power` continuously for `0.5` seconds, the tow line snaps.
- When the line snaps:
  - The wreck detaches.
  - The wreck keeps its current velocity.
  - Show prompt: `Tow line snapped`.
  - Important audio and visual feedback are required.

### Expected Towed Speed

These are approximate top speeds when towing a heavy wreck.

| Tow Level | Tow Power | Approximate Towed Top Speed |
|---:|---:|---:|
| 0 | 250 | 60 |
| 1 | 400 | 95 |
| 2 | 600 | 143 |
| 3 | 850 | 202 |

The exact speed depends on wreck mass and drag, but the feel should be:

- Level 0 towing is slow and awkward.
- Level 1 towing is manageable.
- Level 2 towing is comfortable.
- Level 3 towing is fast enough for the final wreck but still feels heavy.

### Detach

- The player can detach at any time using the tow input.
- Detaching does not damage the wreck.
- The wreck keeps its current velocity.
- The player can reattach later if conditions are met.

### Towed Wreck Collisions

- A towed wreck can collide with debris, mines, other wrecks, and the boundary.
- Collisions damage the wreck.
- Collisions can push the ship.
- A towed wreck can trigger mines.
- A towed wreck can enter the station safe zone without taking damage.

---

## 10. Hazard Systems

### Debris Clusters

- Debris clusters are static circular obstacles.
- Radius: `25` to `50`.
- They do not move.
- They do not take damage.
- They do not disappear.
- Colliding with debris damages the ship and any towed wreck.
- Collision response:
  - Separate the ship or wreck from the debris.
  - Reflect velocity with low restitution.
  - Apply damage based on relative speed.

### Mines

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

Scanner interaction:

- Scanner Level 0:
  - Mines are not shown on the minimap.
  - Mines are faintly visible in the world when close.
- Scanner Level 1:
  - Mines are shown on the minimap.
- Scanner Level 2:
  - Mines are shown with a warning radius.

### Station Safe Zone

- Radius: `120` around station center.
- No debris.
- No mines.
- Hull regenerates.
- Checkpoint is created.
- Docking is possible.

---

## 11. Station Systems

### Safe Zone

- Radius: `120`
- Effects:
  - Hull regenerates at `10` per second.
  - Checkpoint updates.
  - Upgrade menu can be opened.
  - Contract board is available.

### Dock Zone

- Radius: `50`
- Used for unloading.

### Unloading

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

### Checkpointing

A checkpoint is created whenever the ship is inside the station safe zone.

The checkpoint stores:

- Current contract index.
- Current contract score.
- Unlocked rings.
- Parts inventory.
- Upgrade levels.
- Hull value.
- Which wrecks have been unloadded.
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

### Upgrade Menu

The upgrade menu can be opened only:

- Inside the station safe zone.
- While not towing.

If the player tries to open it while towing, show:

`Detach to refit`

The upgrade menu shows:

- Current parts.
- Four upgrade tracks.
- Current level.
- Next level effect.
- Cost.
- Buy button if affordable.
- Recommended tag for upgrades useful for the current contract.

---

## 12. Upgrade Systems

Use a single part currency called **Parts**.

There are no separate part types.

Why one part type:

- Prevents softlocks from missing specific parts.
- Keeps the upgrade menu readable.
- Keeps the economy focused on one decision: which ship system to improve.

### Upgrade Tracks

| Track | Purpose |
|---|---|
| Hull Plating | Increases max hull |
| Thrusters | Increases thrust and top speed |
| Tow Servos | Increases tow power, attach range, and max tow mass |
| Scanner | Reveals wreck data and mines |

### Hull Plating

| Level | Max Hull | Cost |
|---:|---:|---:|
| 0 | 100 | 0 |
| 1 | 140 | 2 |
| 2 | 180 | 4 |
| 3 | 240 | 6 |

### Thrusters

| Level | Thrust | Max Speed | Cost |
|---:|---:|---:|---:|
| 0 | 300 | 250 | 0 |
| 1 | 360 | 300 | 2 |
| 2 | 420 | 350 | 4 |
| 3 | 480 | 400 | 6 |

Drag remains `1.2` at all levels.

### Tow Servos

| Level | Tow Power | Attach Range | Max Tow Mass | Cost |
|---:|---:|---:|---:|---:|
| 0 | 250 | 60 | 50 | 0 |
| 1 | 400 | 70 | 70 | 2 |
| 2 | 600 | 80 | 100 | 4 |
| 3 | 850 | 95 | 130 | 6 |

### Scanner

| Level | Effect | Cost |
|---:|---|---:|
| 0 | Basic minimap: station, player, active wrecks | 0 |
| 1 | Shows wreck mass, part yield, and integrity | 2 |
| 2 | Shows mines on minimap with warning radius | 3 |

### Total Upgrade Cost

Maxing all upgrades costs:

```text
Hull: 2 + 4 + 6 = 12
Thrusters: 2 + 4 + 6 = 12
Tow Servos: 2 + 4 + 6 = 12
Scanner: 2 + 3 = 5
Total: 41
```

Total parts available in a full run:

```text
Wreck parts: 63
Contract rewards: 14
Total: 77
```

This guarantees that a player can always afford the required final upgrades if they salvage enough wrecks, and it prevents hard softlocks.

---

## 13. Contracts and Progression

### Contract Rules

- Only one contract is active at a time.
- Contracts 1 through 4 require salvage score.
- Contract 5 requires the final wreck.
- Wrecks in unlocked rings count toward the active score contract.
- During the final contract, only the Aurora Black Box counts toward contract progress.
- Other wrecks can still be salvaged for parts during the final contract.

### Contract Table

| Contract | Name | Requirement | Unlock | Reward |
|---:|---|---|---|---:|
| 1 | First Shift | 20 salvage score | Ring 2 | 2 parts |
| 2 | Hauler Run | 60 salvage score | Ring 3 | 3 parts |
| 3 | Deep Field | 100 salvage score | Ring 4 | 4 parts |
| 4 | Heavy Salvage | 180 salvage score | Final Corridor | 5 parts |
| 5 | Aurora Black Box | Return the Aurora Black Box | Victory | — |

### Contract Examples

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

- 3 Cargo Liners: `60 + 60 + 60 = 180`

### Recommended Upgrade Path

This is not mandatory, but the contract board should recommend upgrades.

| After Contract | Recommended Upgrades |
|---|---|
| 1 | Tow Servos Level 1 or Thrusters Level 1 |
| 2 | Tow Servos Level 2, Hull Plating Level 1 |
| 3 | Tow Servos Level 3, Hull Plating Level 2, Thrusters Level 2 |
| 4 | Scanner Level 1, any remaining survivability upgrades |

### Required Final Upgrade

The Aurora Black Box has mass `120`.

To tow it, the player needs:

- Tow Servos Level 3.

Recommended final ship:

- Hull Plating Level 2 or higher.
- Thrusters Level 2 or higher.
- Tow Servos Level 3.
- Scanner Level 1 or higher.

Minimum required to complete the final contract:

- Tow Servos Level 3.

### Fallback Rule

If a score contract is active and no eligible active wrecks remain, automatically complete the contract and grant the reward.

This prevents a softlock in case of unexpected content depletion.

---

## 14. HUD

### Permanent HUD Elements

#### Top Left

- Hull bar.
- Hull number.
- Current speed.

Example:

```text
HULL 140 / 180
SPEED 212
```

#### Top Center

- Active contract name.
- Contract progress.

Example:

```text
Hauler Run
35 / 60 salvage score
```

For final contract:

```text
Aurora Black Box
Return the wreck to the station
```

#### Top Right

- Parts count.
- Minimap.

Example:

```text
PARTS 14
```

#### Bottom Center

- Tow status.

If not towing:

```text
TOW: Free
```

If towing:

```text
TOW: Cargo Liner
Mass 90 / Max 100
Integrity 78%
```

### Contextual Prompts

Show prompts near the bottom center when relevant.

Examples:

- `Q: Attach Tow`
- `Q: Detach Tow`
- `Too fast to attach`
- `Cannot tow: mass exceeded`
- `Hold U: Unload`
- `Speed too high to unload`
- `Detach to refit`
- `No signal beyond boundary`
- `Tow line snapped`

### Minimap

The minimap shows:

- Station.
- Player.
- Active wrecks.
- Unlocked ring boundaries.
- Mines, if Scanner Level 1 or higher.
- Final wreck, when active.

Minimap rules:

- Wrecks are shown as dots.
- Wreck dot size increases with wreck tier.
- The final wreck is visually distinct.
- Mines are shown only when Scanner Level 1 is active.
- At Scanner Level 2, mines show a warning radius.

### Upgrade Menu HUD

Shown only at station.

Display:

- Parts.
- Four upgrade tracks.
- Current level.
- Next level effect.
- Cost.
- Buy button.
- Recommended tag.

Example:

```text
TOW SERVOS
Level 2 / 3
Next: Tow Power 850, Max Mass 130
Cost: 6 parts
[BUY]
```

### Game Over Screen

Shown when the ship is destroyed.

Display:

```text
SHIP DESTROYED
Contract: Deep Field
Progress: 40 / 100

[Retry Contract]
```

### Victory Screen

Shown after unloading the Aurora Black Box.

Display:

```text
SHIFT COMPLETE
Aurora Black Box Recovered

Time: 18:42
Wrecks Salvaged: 23
Parts Collected: 54

[Play Again]
```

---

## 15. Content Sections

### Section 1: Tutorial / First Shift

Location:

- Station and Ring 1.

Objective:

- Teach movement, towing, docking, unloading, and upgrading.
- Complete Contract 1.

Content:

- 2 fixed tutorial Scrap Cans.
- 8 additional Scrap Cans.
- 8 debris clusters.
- No mines.

Tutorial prompts:

1. `Use A/D to rotate. Use W to thrust.`
2. `Approach a Scrap Can. Press Q to attach.`
3. `Tow it back to the station.`
4. `Hold U in the dock to unload.`
5. `Use parts to upgrade your ship.`

Expected player progression:

- Player earns at least 2 parts from wrecks.
- Player earns 2 contract reward parts.
- Player can afford one Level 1 upgrade.

### Section 2: Hauler Run

Location:

- Ring 2.

Objective:

- Introduce heavier wrecks and first mines.
- Complete Contract 2.

Content:

- 6 Transport Haulers.
- 4 Scrap Cans.
- 12 debris clusters.
- 4 mines.

Expected player progression:

- Player learns that tow mass matters.
- Player should consider Tow Servos Level 1.
- Player may buy Thrusters Level 1 for faster travel.

### Section 3: Deep Field

Location:

- Ring 3.

Objective:

- Introduce Fighter Frames and denser hazards.
- Complete Contract 3.

Content:

- 4 Fighter Frames.
- 3 Transport Haulers.
- 16 debris clusters.
- 8 mines.

Expected player progression:

- Player needs Tow Servos Level 1 to tow Fighter Frames.
- Hull Plating Level 1 becomes useful.
- Scanner Level 1 becomes useful for mine avoidance.

### Section 4: Heavy Salvage

Location:

- Ring 4.

Objective:

- Introduce Cargo Liners and prepare for the final wreck.
- Complete Contract 4.

Content:

- 3 Cargo Liners.
- 4 Fighter Frames.
- 2 Transport Haulers.
- 20 debris clusters.
- 12 mines.

Expected player progression:

- Player needs Tow Servos Level 2 to tow Cargo Liners efficiently.
- Player should aim for Tow Servos Level 3.
- Hull and Thruster upgrades become important for the long final trip.

### Section 5: Aurora Black Box

Location:

- Final Corridor.

Objective:

- Retrieve the Aurora Black Box.
- Win the game.

Content:

- 1 Aurora Black Box.
- 4 debris clusters.
- 6 mines.

Expected player progression:

- Player needs Tow Servos Level 3.
- The final trip is long, so Thrusters and Hull matter.
- Scanner helps avoid final-corridor mines.

Victory condition:

- Unload the Aurora Black Box at the station.

---

## 16. Feel and Pacing

### Desired Feel

The game should feel like careful piloting, not action.

Key feelings:

- The ship should feel floaty but controllable.
- Towing should feel heavy.
- Returning with a heavy wreck should feel tense.
- The station should feel safe.
- Upgrades should feel meaningful immediately.
- Damage should be readable.
- Mines should create avoidable danger, not random punishment.

### Pacing Goals

| Phase | Target Feel |
|---|---|
| Tutorial | Simple, safe, quick first success |
| Contract 2 | Slightly harder, first upgrade decision |
| Contract 3 | More planning, mine awareness |
| Contract 4 | Heavy wrecks, upgrade urgency |
| Final | Long tense return, payoff |

### Travel Time Feel

At base speed:

- Ring 1 is very close.
- Ring 2 is a short trip.
- Ring 3 is a moderate trip.
- Ring 4 is a long trip.
- Final corridor is the longest and most dangerous.

Towing should noticeably slow the player:

- Level 0 towing feels sluggish.
- Level 1 towing feels workable.
- Level 2 towing feels comfortable.
- Level 3 towing feels fast but still heavy.

### Damage Frequency

The player should usually avoid most damage, but not always.

Expected:

- Early game: occasional small hull loss.
- Mid game: avoidable mine danger.
- Late game: one bad collision or mine can be serious.
- Final: hull upgrades matter.

### Upgrade Pacing

The player should usually be able to buy one useful upgrade after each contract.

The game should not require perfect salvage. The player can complete the game with imperfect upgrades as long as they have enough parts for Tow Servos Level 3.

---

## 17. Edge Cases

### Attach Failures

- If wreck mass exceeds max tow mass, attachment fails.
- If relative speed is too high, attachment fails.
- If player is already towing, attachment fails.
- If wreck is out of range, attachment fails.
- Each failure shows a clear prompt.

### Line Snap

- If the tow line is overstressed, it snaps.
- The wreck remains in the world.
- The player can reattach later.

### Wreck at Zero Integrity

- A wreck at zero integrity can still be towed.
- It yields 0 parts.
- It still gives full score.
- This prevents damaged wrecks from becoming unfinishable.

### Final Wreck at Low Integrity

- The Aurora Black Box can be damaged.
- It still completes the final contract when unloadded.
- Parts may be reduced or zero.
- Victory is not blocked by wreck integrity.

### Unload Failure

- If the player is outside the dock zone, unload does not start.
- If speed is too high, unload does not start.
- If the player leaves the dock zone during unload, progress resets.
- If the player detaches during unload, unload cancels.

### Death While Towing

- If the ship is destroyed while towing:
  - The towed wreck remains in the world.
  - The checkpoint restores the state from the last station entry.
  - If the wreck had not been unloadded, it is restored to its checkpoint state.
  - The player can reattach and continue.

### Death at Station

- If the ship is destroyed while inside the station safe zone, the checkpoint is the current station state.
- The player respawns at the station with the checkpointed hull and progress.

### Boundary

- The ship cannot leave the world boundary.
- The towed wreck cannot leave the world boundary.
- If a towed wreck is pushed against the boundary, clamp its position and apply tow stress normally.

### Contract Completion While Towing

- Contract completion only happens after unload.
- Therefore, the player is not towing when a contract completes.

### All Wrecks Removed

- If all eligible wrecks for a score contract are unloadded and the contract is not complete, auto-complete the contract.
- This is a safety fallback.

### Final Wreck Unreachable by Upgrades

- The final wreck can only be attached with Tow Servos Level 3.
- The game provides enough total parts to reach Tow Servos Level 3.
- If the player lacks Tow Servos Level 3, they can continue salvaging other active wrecks for parts.

### Pause

- Pausing stops all simulation.
- The player can resume, retry the current contract, or restart the run.

---

## 18. Important Design Decisions and Why

### One Part Currency

Why:

- Prevents softlocks.
- Keeps upgrade choices simple.
- Keeps the HUD clean.
- Makes the economy easy to understand.

### No Cargo Capacity

Why:

- The player tows one wreck at a time.
- Cargo capacity would add inventory management without adding to the core tow fantasy.
- Returning to the station is already the natural reset point.

### Wreck Score Is Not Reduced by Damage

Why:

- Contracts should remain completable even if the player damages a wreck.
- Parts are the reward for careful play.
- This separates contract progression from salvage quality.

### Checkpoint at Station

Why:

- The station is the safe zone.
- It makes death fair.
- It preserves progression.
- It avoids full-run restarts.

### Environmental Hazards Instead of Combat

Why:

- The core loop is towing, not fighting.
- Debris and mines create spatial tension.
- They reward navigation and upgrade investment without requiring combat systems.

### Fixed North-Up Camera

Why:

- Makes the tow line easier to read.
- Makes the minimap easier to understand.
- Reduces disorientation during long towing trips.

### Single Continuous World

Why:

- The station is the hub.
- Rings create progression without level loading.
- The player can always see the station as a destination.
- It reinforces the fantasy of returning to base.

---

## 19. Integration Notes

### For Engineering

The following systems need to be implemented:

1. 2D ship physics.
2. Circle collision.
3. Spring-damper tow system.
4. Wreck integrity and part calculation.
5. Mine proximity and fuse logic.
6. Contract state machine.
7. Ring unlock system.
8. Checkpoint save/load within a run.
9. Seeded map generation.
10. Upgrade menu state.
11. HUD state.
12. Death and respawn.
13. Victory condition.

Important data per wreck:

```text
id
tier
position
velocity
mass
radius
initial_integrity
current_integrity
score
base_parts
tow_requirement
state
```

Important data per ship:

```text
position
velocity
heading
hull
max_hull
thrust
drag
tow_level
hull_level
thruster_level
scanner_level
parts
towed_wreck_id
```

Important data per contract:

```text
index
name
type
required_score
current_score
reward_parts
unlocked_ring
completed
```

### For Visual Design

Important visual cues:

- Station safe zone should be clearly readable.
- Dock zone should be distinct from safe zone.
- Tow line should show tension.
- Wreck tier should be visually distinguishable by size and color.
- The final wreck should be visually distinct.
- Hull damage should flash or pulse.
- Wreck integrity should be readable when towing.
- Mines should have a clear warning state before explosion.
- Contract completion should be clearly communicated.
- Death should be clearly communicated.

### For Audio Design

Important audio cues:

- Tow attach.
- Tow detach.
- Tow line under stress.
- Tow line snap.
- Hull damage.
- Wreck damage.
- Mine arming.
- Mine explosion.
- Unload start.
- Unload complete.
- Contract complete.
- Ship destroyed.
- Victory.

Audio should emphasize safety, danger, and success, but the gameplay does not depend on hearing them. Visual prompts must also communicate the same information.