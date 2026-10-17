# gameplay.md

## 1. Document Purpose

This document is the complete gameplay source of truth for a frog platformer.

It defines:

- dimensionality
- world space and level layout
- gameplay systems
- algorithms
- progression
- player-facing numbers
- HUD
- content
- edge cases
- cuts

The visual designer can use this document to know what must be visible and where it must be placed. The engineering agent can use this document to implement behavior. Audio specifics are out of scope, but required audio events are named.

---

## 2. Game Identity

Working title:

**FROG: POND TO PEAK**

Core fantasy:

A small frog makes a big journey from a quiet pond to the Great Waterfall.

Core verbs:

- Run
- Jump
- Swim
- Bounce on lily pads
- Stomp enemies

The game is a short, complete, linear 2D side-scrolling platformer.

Estimated total playtime:

- 10 to 15 minutes

---

## 3. Dimensionality

The game is **2D side-view**.

All gameplay occurs on the X-Y plane.

There is no third axis.

Design logic:

- A frog platformer needs readable vertical and horizontal spacing.
- 2D side-view makes jump distance, water depth, and lily pad bounce easy to read.
- 3D or 2.5D would dilute the core platforming challenge and increase scope.
- The frog’s small size and big jumps are best expressed through precise 2D spacing.

Camera:

- 2D camera
- follows the player
- clamped to level bounds
- smooth follow
- small look-ahead in the player’s facing direction

Camera feel targets:

- deadzone: 200 px horizontally, 120 px vertically
- look-ahead: 40 px in facing direction
- smoothing: fast enough to feel responsive, not so fast that the screen shakes

---

## 4. Logical Resolution and Units

Logical resolution:

- 1280 x 720 px

Tile size:

- 32 px

Update rate:

- 60 logical updates per second
- dt = 1 / 60

Coordinate system:

- X increases to the right
- Y increases downward
- origin is top-left

Level bounds:

- left wall at x = 0
- right wall at x = level_width
- ceiling at y = 0
- death below y = level_height + 100

Player cannot leave the level from the sides or top.

Falling below the level causes death and respawn.

---

## 5. Core Loop

Each level follows the same loop:

1. Player spawns at the level start.
2. Player moves through the level.
3. Player collects optional dewdrops.
4. Player avoids or stomps enemies.
5. Player uses water, lily pads, and platforms to reach the exit.
6. Player reaches the waterfall exit.
7. Level completes and the next level unlocks.

The goal is always:

**Reach the waterfall.**

Dewdrops are optional.

---

## 6. Controls

Keyboard controls:

### Movement

- Move left: A or Left Arrow
- Move right: D or Right Arrow

### Jump / Swim

- Jump: Space, W, or Up Arrow
- In water, holding Jump swims upward.

### Pause

- Pause: Esc

### Menus

- Move menu: W, S, Up, or Down
- Confirm: Enter or Space
- Back: Esc

Design logic:

- The game uses one primary action key for jumping and swimming.
- This keeps the frog’s movement simple and readable.
- No secondary ability is required.

---

## 7. Game States

The game has these states:

1. Title
2. Controls
3. Playing
4. Paused
5. Level Complete
6. Game Complete

State rules:

### Title

Shown when the game starts.

If a save exists and the game is not complete:

- Continue
- New Game
- Controls

If the game is complete:

- Play Again
- New Game
- Controls

### Controls

Shows the control list.

Esc returns to the previous menu.

### Playing

Normal gameplay.

Esc opens Pause.

### Paused

Shown only during Playing.

Options:

- Resume
- Restart Level
- Controls
- Quit to Title

Pause is disabled during:

- Level Complete
- Game Complete
- Title
- Controls
- death animation

### Level Complete

Shown when the player touches an active exit.

Shows:

- level name
- dewdrop count
- optional perfect message
- “Press Enter or Space to continue”

Continuing starts the next level.

### Game Complete

Shown after Level 6.

Shows:

- ending text
- “Press Enter or Space to return to title”

---

## 8. Save Data

Save data stores only:

```json
{
  "unlocked_level": 1,
  "completed": false
}
```

Rules:

- `unlocked_level` is 1 through 6.
- `completed` is true only after Level 6.
- In-level progress is not saved.
- Dewdrops are not saved between sessions.
- Quitting to title saves the current unlocked level.
- New Game resets save data.
- Play Again resets save data and starts Level 1.

Design logic:

- A short linear platformer does not need complex meta-progression.
- Saving only unlocked levels keeps the game simple and complete.
- In-level checkpoints handle failure better than persistent in-level saves.

---

## 9. Progression

The game is linear.

Level unlock order:

1. Pond Edge
2. Lily Rush
3. Reed Hollow
4. Stormy Creek
5. Cliffside Ponds
6. Great Waterfall

There is no level select.

There are no permanent upgrades.

There are no power-ups.

Progression comes from:

- learning movement
- learning water
- learning lily pad bounce
- learning moving platforms
- learning currents
- learning the boss

Design logic:

- The frog’s abilities are fixed.
- This keeps the fantasy clear: the frog is small, but it can jump, swim, and bounce.
- Upgrades would obscure the core movement and increase scope.

---

## 10. Player Systems

## 10.1 Player Hitbox

Player AABB:

- width: 20 px
- height: 28 px

Player spawn position is given as center coordinates.

For ground top y = 640:

- player center y = 626

For ground top y = 1216:

- player center y = 1202

---

## 10.2 Ground Movement

Numbers:

- max run speed: 240 px/s
- ground acceleration: 1800 px/s²
- air acceleration: 1200 px/s²
- ground friction: 1600 px/s²
- air friction: 200 px/s²
- gravity: 1400 px/s²
- max fall speed: 900 px/s
- jump velocity: -520 px/s

Horizontal movement algorithm:

```text
input = 0
if right pressed: input += 1
if left pressed: input -= 1

if input != 0:
    vx += input * acceleration * dt
    clamp vx to [-max_speed, max_speed]
else:
    apply friction toward 0
```

Acceleration and max speed depend on context:

- on ground: acceleration 1800, max speed 240
- in air: acceleration 1200, max speed 240
- in water: acceleration 700, max speed 160

Friction:

- on ground with no input: 1600
- in air with no input: 200
- in water with no input: 900

Design logic:

- 240 px/s is fast enough to feel lively but slow enough to read gaps.
- Air control is strong so jumps feel responsive.
- Friction is high on ground so the frog stops quickly.
- Air friction is low so the frog can adjust in midair.

---

## 10.3 Jumping

Jump numbers:

- jump velocity: -520 px/s
- coyote time: 0.08 s
- jump buffer: 0.12 s
- variable jump release: multiply current upward velocity by 0.45

Algorithm:

```text
if jump pressed:
    store jump buffer timer = 0.12

if on ground or coyote timer > 0:
    if jump buffer timer > 0:
        vy = -520
        on_ground = false
        coyote_timer = 0
        jump_buffer_timer = 0
        jump_cut_applied = false

if jump released:
    if vy < 0 and jump_cut_applied == false:
        vy *= 0.45
        jump_cut_applied = true
```

Coyote time:

- If the player walks off a platform, they can still jump for 0.08 s.

Jump buffer:

- If the player presses jump slightly before landing, the jump triggers on landing.

Design logic:

- Coyote time and jump buffering make the game feel fair.
- Variable jump allows short hops and full jumps.
- The frog should feel snappy, not floaty.

---

## 10.4 Water Movement

Water is a movement space, not a hazard.

The frog cannot drown.

Water numbers:

- water gravity: 350 px/s²
- water max fall speed: 220 px/s
- water max horizontal speed: 160 px/s
- water acceleration: 700 px/s²
- water friction: 900 px/s²
- surface jump velocity: -460 px/s
- swim upward acceleration: 900 px/s²
- swim upward max velocity: -220 px/s

Water state detection:

```text
in_water = player center is inside any water rectangle
```

Surface detection:

```text
on_surface =
    not in_water
    and player feet are within 6 px above water top
    and player horizontally overlaps water rectangle
```

Water vertical movement:

```text
if in_water:
    if jump held:
        vy -= 900 * dt
        if vy < -220: vy = -220
    else:
        vy += 350 * dt
        if vy > 220: vy = 220

if on_surface and jump pressed:
    vy = -460
```

Entering water:

```text
if player enters water and vy > 220:
    vy = 220
```

Design logic:

- Water should feel like swimming, not falling.
- The frog can move upward by holding Jump.
- Surface jumps are weaker than land jumps because water is dense.
- Water is forgiving because the frog belongs in water.

---

## 10.5 Lily Pad Bounce

Lily pads are bouncy one-way platforms.

The player cannot stand on a lily pad.

Lily pad bounce numbers:

- normal bounce velocity: -620 px/s
- jump-held bounce velocity: -680 px/s

Algorithm:

```text
if player is falling:
    if previous bottom <= lily_pad_top:
        if new bottom >= lily_pad_top:
            if horizontal overlap:
                if jump held:
                    vy = -680
                else:
                    vy = -620
                on_ground = false
                jump_cut_applied = false
```

Design logic:

- Lily pads are the frog’s signature movement tool.
- They let the frog reach higher than normal jumps.
- Holding Jump gives a small reward for deliberate input.
- The bounce is strong but not so strong that it breaks level spacing.

---

## 10.6 Stomping

The player can stomp certain enemies.

Stomp detection:

```text
if player overlaps enemy:
    if player is falling:
        if previous player bottom <= enemy top + 4:
            stomp enemy
```

Stomp bounce:

- normal enemy stomp bounce: -380 px/s
- boss stomp bounce: -420 px/s

Stomp rules:

- Stomping works even if the player is invulnerable.
- Stomping a normal enemy kills it.
- Stomping the boss reduces boss HP.
- If the player touches an enemy from the side or below, the player takes damage.

Design logic:

- Stomping gives the player an active verb.
- It makes enemies interactive instead of only obstacles.
- It rewards timing and positioning.

---

## 10.7 Damage

Player health:

- 3 hearts
- 1 hit per heart
- hearts refill at checkpoints

Invulnerability:

- duration: 1.2 s
- player cannot take damage while invulnerable
- stomp checks still work while invulnerable

Knockback:

- horizontal knockback: 260 px/s away from damage source
- vertical knockback: -220 px/s

Damage algorithm:

```text
if invulnerability_timer > 0:
    ignore damage

hearts -= 1
invulnerability_timer = 1.2

if source center x <= player center x:
    vx = 260
else:
    vx = -260

vy = -220

if hearts <= 0:
    start death
```

Design logic:

- 3 hearts is forgiving enough for a short platformer.
- Checkpoint refill avoids lives and meta-frustration.
- Knockback is strong enough to save the player from staying in danger.

---

## 10.8 Death and Respawn

Death causes:

- hearts reach 0
- player falls below level_height + 100

Death behavior:

1. Stop player input.
2. Play death animation for 0.6 s.
3. Respawn at last checkpoint or level spawn.
4. Refill hearts to 3.
5. Keep already collected dewdrops.
6. Reset enemies to initial positions.
7. Reset moving platforms to initial phase.
8. If the boss is dead, keep the boss dead and the exit unlocked.

Design logic:

- Keeping dewdrops avoids punishing optional collection.
- Resetting enemies prevents unfair states.
- Keeping the boss dead after boss death avoids repeating the boss.

---

## 11. World Systems

## 11.1 Solids

Solids are normal platforms.

They block movement from all sides.

Solids are used for:

- ground
- boss arena floor

---

## 11.2 One-Way Platforms

One-way platforms are thin platforms.

They block only from below.

The player can pass through them from below.

They are used for:

- leaf platforms
- exit platforms in vertical levels

One-way platform collision:

```text
if player is falling:
    if previous bottom <= platform_top:
        if new bottom >= platform_top:
            if horizontal overlap:
                land on platform
                vy = 0
                on_ground = true
```

The player cannot drop through one-way platforms.

Design logic:

- One-way platforms allow dense vertical levels without blocking upward movement.
- Not allowing drop-through keeps controls simple.

---

## 11.3 Moving Platforms

Moving platforms are one-way platforms that move on a sine path.

They carry the player.

Moving platform data:

- start position
- width
- height
- axis: x or y
- amplitude
- period

Position algorithm:

```text
offset = amplitude * sin(2 * PI * time / period)

if axis == x:
    x = start_x + offset
    y = start_y
else:
    x = start_x
    y = start_y + offset
```

Carry algorithm:

```text
delta = current_position - previous_position

if player is standing on this moving platform:
    player position += delta
```

Design logic:

- Moving platforms add timing without adding new controls.
- They are important for vertical levels.
- They carry the player so movement feels physical.

---

## 11.4 Water Currents

Currents are water zones that apply horizontal force.

Current numbers:

- force: 120 px/s²
- direction: left or right

Current algorithm:

```text
if player center is inside current rectangle:
    vx += current_force * dt
    clamp vx to water max speed
```

Design logic:

- Currents make water levels feel dynamic.
- 120 px/s² is noticeable but controllable.
- The frog can still swim against a current, but it is slower.

---

## 11.5 Dewdrops

Dewdrops are optional collectibles.

Dewdrop hitbox:

- 16 x 16 px
- centered on listed coordinates

Behavior:

- touching a dewdrop collects it
- collected dewdrops remain collected after respawn
- restarting the level resets dewdrops
- dewdrops do not affect progression

HUD displays:

- current collected count
- total count for the current level

Design logic:

- Dewdrops encourage exploration without forcing risk.
- They give the player a secondary goal without adding score pressure.

---

## 11.6 Checkpoints

Checkpoints are lotus flowers.

Checkpoint hitbox:

- 32 x 32 px
- centered on listed coordinates

Behavior:

- touching a checkpoint sets the respawn point
- touching a checkpoint refills hearts to 3
- shows “Checkpoint” message

Design logic:

- Checkpoints reduce frustration.
- Refilling hearts makes checkpoints feel rewarding.

---

## 11.7 Exits

Exits are waterfall portals.

Exit hitbox:

- 48 x 64 px
- centered on listed coordinates

Behavior:

- touching an active exit completes the level
- in Level 6, the exit is locked until the boss is defeated

Design logic:

- The exit is always the objective.
- The final boss gates the ending, not a collectible.

---

## 12. Enemy Systems

## 12.1 Mosquito

Mosquito is a small flying enemy.

Hitbox:

- 24 x 20 px

Movement:

- horizontal patrol speed: 80 px/s
- reverses at patrol bounds
- vertical sine amplitude: 24 px
- vertical sine period: 1.6 s

Algorithm:

```text
if x < min_x or x > max_x:
    direction *= -1

x += direction * 80 * dt
y = base_y + 24 * sin(2 * PI * time / 1.6)
```

Behavior:

- stompable
- touching from side or below damages player

Design logic:

- Mosquitoes are slow and predictable.
- They teach stomping without being too hard.

---

## 12.2 Dragonfly

Dragonfly is a faster horizontal flying enemy.

Hitbox:

- 28 x 16 px

Movement:

- patrol speed: 180 px/s
- reverses at patrol bounds
- fixed y

Algorithm:

```text
if x < min_x or x > max_x:
    direction *= -1

x += direction * 180 * dt
```

Behavior:

- stompable
- touching from side or below damages player

Design logic:

- Dragonflies are faster than mosquitoes.
- They appear after the player has learned stomping.

---

## 12.3 Thorn

Thorn is a static hazard.

Hitbox:

- 48 x 16 px
- listed as a rectangle

Behavior:

- not stompable
- touching damages player

Design logic:

- Thorns provide simple static danger.
- They do not need AI.

---

## 13. Boss System: Heron

Boss name:

**Heron**

Level:

- Level 6, Great Waterfall

Boss hitbox:

- 56 x 80 px

Boss spawn:

- center: 640, 600
- ground top: 640

Boss HP:

- 6 stomp hits

Boss arena bounds:

- min x: 100
- max x: 1180

Boss states:

1. Idle
2. Lunge
3. Recover
4. Dead

### Phase 1

Used while HP is 6, 5, or 4.

State timings:

- idle: 1.2 s
- lunge: 0.4 s
- recover: 0.8 s

Lunge speed:

- 320 px/s toward player

### Phase 2

Used while HP is 3, 2, or 1.

State timings:

- idle: 0.8 s
- lunge: 0.4 s
- recover: 0.6 s

Lunge speed:

- 380 px/s toward player

### Boss Algorithm

```text
if state == idle:
    face player
    timer -= dt
    if timer <= 0:
        state = lunge
        timer = 0.4
        direction = sign(player_x - boss_x)

if state == lunge:
    vx = direction * lunge_speed
    timer -= dt
    if timer <= 0:
        state = recover
        timer = recover_time
        vx = 0

if state == recover:
    vx = 0
    timer -= dt
    if timer <= 0:
        state = idle
        timer = idle_time

clamp boss x to [100, 1180]
boss y = ground_top - boss_height
```

### Boss Stomp

The player can stomp the heron from above.

Stomp zone:

- top 12 px of the heron hitbox

Stomp behavior:

```text
if player is falling:
    if previous player bottom <= heron_top + 12:
        if horizontal overlap:
            heron HP -= 1
            player vy = -420
            if heron HP <= 0:
                heron state = dead
                unlock exit
```

Design logic:

- The heron is a simple boss because the game is short.
- The player only needs to learn one target: the head.
- Phase 2 increases pressure without changing mechanics.
- The boss gates the ending but does not require a new ability.

---

## 14. Collision and Update Order

The recommended update order is:

1. Add moving platform delta to player if standing on one.
2. Apply horizontal input.
3. Apply water and current forces.
4. Apply vertical gravity or swimming.
5. Move player horizontally and resolve solid collisions.
6. Move player vertically and resolve:
   - solids
   - one-way platforms
   - lily pads
7. Update enemies.
8. Check player-enemy collisions.
9. Check dewdrop collection.
10. Check checkpoint touch.
11. Check exit touch.
12. Update timers and HUD.

Stomp checks should use the player’s bottom position from before vertical movement.

Design logic:

- This order prevents tunneling and keeps platforming predictable.
- Moving platforms should carry the player before input so the player does not slip off.

---

## 15. HUD

The HUD has three sections.

There is no timer, score, minimap, or objective arrow.

## 15.1 Health Section

Location:

- top-left
- 16 px from left edge
- 16 px from top edge

Content:

- 3 heart icons
- each icon 32 x 32 px
- 8 px spacing between icons

Display:

- full heart = current health
- empty heart = lost health

Behavior:

- updates immediately on damage
- refills at checkpoints and respawn

Design logic:

- Health must be readable at a glance.
- Three icons are enough for the game’s difficulty.

---

## 15.2 Dewdrop Section

Location:

- top-right
- 16 px from right edge
- 16 px from top edge

Content:

- dewdrop icon
- count text

Format:

```text
x / y
```

Where:

- x = dewdrops collected in current level
- y = total dewdrops in current level

Display:

- icon 24 x 24 px
- text 18 px
- right-aligned

Behavior:

- updates immediately on collection
- persists through respawn
- resets on level restart

Design logic:

- The player needs to know how many optional dewdrops remain.
- A per-level count is clearer than a global score.

---

## 15.3 Message Section

Location:

- top-center
- 48 px below top edge
- max width 600 px

Content priority:

1. Level Complete
2. Checkpoint
3. Tutorial prompt
4. Level name

Messages:

- Level name appears for 2.5 s at level start.
- Tutorial prompts appear until their condition is met or expire after 5 s.
- “Checkpoint” appears for 1.5 s.
- “Level Complete” appears on the Level Complete screen.

Design logic:

- A single message area avoids HUD clutter.
- Priority prevents conflicting messages.

---

## 16. Tutorial Prompts

Tutorial prompts appear in the Message Section.

### Level 1

Prompt:

- “Move with A/D or Left/Right”
  - shown at spawn
  - hidden after first horizontal input

Prompt:

- “Jump with Space”
  - shown when player x >= 300
  - hidden after first jump

Prompt:

- “Land on enemies to stomp them”
  - shown when player x >= 1350
  - hidden after first stomp or when player x >= 1500

Prompt:

- “Reach the waterfall”
  - shown when player x >= 1750

### Level 2

Prompt:

- “Hold Jump to swim”
  - shown when player x >= 350
  - hidden after first water jump or swim input while in water

Prompt:

- “Lily pads bounce”
  - shown when player x >= 500
  - hidden after first lily pad bounce

### Level 3

Prompt:

- “Leaves are one-way platforms”
  - shown when player x >= 250
  - hidden after first one-way platform landing

Prompt:

- “Moving leaves carry you”
  - shown when player x >= 750 and player y <= 400
  - hidden after first moving platform ride

### Level 4

Prompt:

- “Currents push you”
  - shown when player x >= 280
  - hidden after first current force is applied

### Level 5

Prompt:

- “Chain lily pads to climb”
  - shown when player x >= 950
  - hidden after first lily pad bounce

### Level 6

Prompt:

- “Stomp the heron’s head”
  - shown at boss arena start
  - hidden after first boss stomp

Design logic:

- Each level teaches one new idea.
- Prompts are minimal so the game does not feel like a manual.

---

## 17. Level Design Principles

All levels follow these rules:

- Max normal jump gap: 160 px
- Max normal vertical step: 88 px
- Lily pad bounce can cover larger vertical gaps.
- Hazards should be avoidable with at least 1 second of reaction time.
- Checkpoints appear in safe locations.
- Dewdrops are optional and should not require impossible precision.
- No random enemy spawns.
- No hidden required paths.
- No level is harder because of a mechanic the player has not seen.

Design logic:

- The game should feel fair.
- Difficulty should come from spacing and timing, not luck.

---

## 18. Level Content

## 18.1 Level 1: Pond Edge

Level size:

- 2000 x 720 px

Estimated time:

- 45 to 60 seconds

Purpose:

- teach movement, jumping, stomping, and the objective

Spawn:

- center: 100, 626

Solids:

```text
0, 640, 900, 80
1020, 640, 480, 80
1660, 640, 340, 80
```

One-way platforms:

```text
1100, 552, 128, 16
```

Hazards:

```text
Thorn: 1350, 624, 48, 16
```

Enemies:

```text
Mosquito:
    center: 1450, 570
    min_x: 1380
    max_x: 1520
    base_y: 570
```

Dewdrops:

```text
200, 600
400, 560
700, 560
1160, 508
1700, 560
```

Total dewdrops:

- 5

Checkpoint:

- center: 1700, 624

Exit:

- center: 1900, 608

Level notes:

- The first gap is 120 px.
- The second gap is 160 px.
- The one-way platform is optional for the dewdrop above it.
- The mosquito is stompable and appears before the final gap.

---

## 18.2 Level 2: Lily Rush

Level size:

- 2400 x 720 px

Estimated time:

- 75 to 90 seconds

Purpose:

- introduce water, swimming, surface jumps, and lily pad bounce

Spawn:

- center: 100, 626

Solids:

```text
0, 640, 400, 80
900, 640, 300, 80
1800, 640, 600, 80
```

Water:

```text
400, 560, 500, 160
1200, 560, 600, 160
```

Lily pads:

```text
520, 560, 64, 16
680, 520, 64, 16
840, 560, 64, 16
1280, 560, 64, 16
1440, 500, 64, 16
1600, 560, 64, 16
```

Hazards:

```text
Thorn: 1000, 624, 48, 16
```

Enemies:

```text
Dragonfly:
    center: 1500, 460
    min_x: 1300
    max_x: 1700
```

Dewdrops:

```text
200, 600
600, 520
760, 480
1000, 560
1350, 520
1550, 460
2100, 600
```

Total dewdrops:

- 7

Checkpoint:

- center: 1850, 624

Exit:

- center: 2300, 608

Level notes:

- The player enters water for the first time.
- Lily pads are the intended crossing method.
- Falling into water is not lethal.
- The dragonfly guards the second water crossing.

---

## 18.3 Level 3: Reed Hollow

Level size:

- 1600 x 1280 px

Estimated time:

- 90 to 120 seconds

Purpose:

- introduce one-way platforms, vertical climbing, and moving platforms

Spawn:

- center: 100, 1202

Solids:

```text
0, 1216, 1600, 64
```

One-way platforms:

```text
300, 1128, 128, 16
500, 1040, 128, 16
700, 952, 128, 16
900, 864, 128, 16
1250, 688, 128, 16
1050, 600, 128, 16
850, 512, 128, 16
650, 424, 128, 16
450, 336, 128, 16
1200, 248, 128, 16
```

Lily pads:

```text
1100, 776, 64, 16
```

Moving platforms:

```text
start: 800, 248, 128, 16
axis: x
amplitude: 240
period: 4
```

Hazards:

```text
Thorn: 200, 1200, 48, 16
```

Enemies:

```text
Mosquito:
    center: 800, 820
    min_x: 700
    max_x: 1000
    base_y: 820
```

Dewdrops:

```text
200, 1180
350, 1090
550, 1000
750, 910
950, 820
1150, 730
1314, 650
1100, 560
900, 470
700, 380
500, 290
800, 210
```

Total dewdrops:

- 12

Checkpoint:

- center: 1314, 672

Exit:

- center: 1264, 216

Level notes:

- This level is vertical.
- The player climbs using one-way platforms and one lily pad.
- The moving platform is required to reach the exit.
- The checkpoint is placed after the first major climb.

---

## 18.4 Level 4: Stormy Creek

Level size:

- 2800 x 720 px

Estimated time:

- 120 to 150 seconds

Purpose:

- introduce currents and combine water, lily pads, and hazards

Spawn:

- center: 100, 626

Solids:

```text
0, 640, 300, 80
700, 640, 200, 80
1400, 640, 300, 80
2200, 640, 600, 80
```

Water:

```text
300, 560, 400, 160
900, 560, 500, 160
1700, 560, 500, 160
```

Currents:

```text
300, 560, 400, 160, force +120
900, 560, 500, 160, force -120
1700, 560, 500, 160, force +120
```

Lily pads:

```text
400, 560, 64, 16
550, 520, 64, 16
1000, 560, 64, 16
1150, 500, 64, 16
1300, 560, 64, 16
1800, 560, 64, 16
1950, 520, 64, 16
2100, 560, 64, 16
```

Hazards:

```text
Thorn: 800, 624, 48, 16
Thorn: 1600, 624, 48, 16
Thorn: 2300, 624, 48, 16
```

Enemies:

```text
Dragonfly:
    center: 1100, 460
    min_x: 950
    max_x: 1350

Dragonfly:
    center: 1900, 460
    min_x: 1750
    max_x: 2150
```

Dewdrops:

```text
200, 600
450, 520
600, 480
850, 600
1050, 520
1200, 460
1450, 600
1850, 520
2000, 480
2400, 600
2600, 560
```

Total dewdrops:

- 11

Checkpoint:

- center: 1500, 624

Exit:

- center: 2700, 608

Level notes:

- The first current pushes right.
- The second current pushes left.
- The third current pushes right.
- The player must use lily pads and timing to cross.
- Thorns punish careless landings after water sections.

---

## 18.5 Level 5: Cliffside Ponds

Level size:

- 2000 x 1280 px

Estimated time:

- 120 to 150 seconds

Purpose:

- combine vertical climbing, lily pad chains, moving platforms, and enemies

Spawn:

- center: 100, 1202

Solids:

```text
0, 1216, 2000, 64
```

One-way platforms:

```text
200, 1128, 128, 16
400, 1040, 128, 16
600, 952, 128, 16
800, 864, 128, 16
1500, 512, 128, 16
1300, 424, 128, 16
1100, 336, 128, 16
900, 248, 128, 16
1600, 248, 128, 16
```

Lily pads:

```text
1000, 776, 64, 16
1150, 688, 64, 16
1300, 600, 64, 16
```

Moving platforms:

```text
start: 1200, 288, 128, 16
axis: x
amplitude: 160
period: 4
```

Hazards:

```text
Thorn: 500, 1200, 48, 16
Thorn: 1400, 1200, 48, 16
```

Enemies:

```text
Mosquito:
    center: 700, 820
    min_x: 600
    max_x: 900
    base_y: 820

Dragonfly:
    center: 1200, 300
    min_x: 1000
    max_x: 1400
```

Dewdrops:

```text
250, 1090
450, 1000
650, 910
850, 820
1032, 740
1182, 650
1332, 560
1564, 484
1364, 380
1164, 290
964, 210
1300, 250
```

Total dewdrops:

- 12

Checkpoint:

- center: 1564, 496

Exit:

- center: 1664, 216

Level notes:

- This is the hardest platforming level.
- The lily pad chain is the intended route upward.
- The moving platform is required for the final section.
- The dragonfly guards the upper route.

---

## 18.6 Level 6: Great Waterfall

Level size:

- 1280 x 720 px

Estimated time:

- 60 to 120 seconds

Purpose:

- final boss and ending

Spawn:

- center: 100, 626

Solids:

```text
0, 640, 1280, 80
```

Boss:

```text
Heron:
    center: 640, 600
    HP: 6
    min_x: 100
    max_x: 1180
```

Exit:

- center: 1200, 608
- locked until boss is dead

Dewdrops:

```text
200, 600
640, 500
1080, 600
```

Total dewdrops:

- 3

Level notes:

- The arena is open.
- There are no hazards other than the heron.
- The exit is visible but inactive until the boss dies.
- Dewdrops are optional and placed to encourage movement around the arena.

---

## 19. Level Complete Screen

Shown after each level except Level 6.

Content:

```text
LEVEL COMPLETE

[Level Name]

Dewdrops: x / y

Press Enter or Space to continue
```

If x == y:

```text
Perfect!
```

Design logic:

- The player gets immediate feedback on optional collection.
- There is no timer or rank because the game is short.

---

## 20. Game Complete Screen

Shown after Level 6.

Content:

```text
THE FROG REACHED THE GREAT WATERFALL.

The pond is now a small dot in a big sky.

Press Enter or Space to return to title
```

Design logic:

- The ending is simple and emotional without adding scope.
- It completes the frog’s journey.

---

## 21. Title Screen

Content:

```text
FROG: POND TO PEAK

A small jump to the waterfall

Continue
New Game
Controls
```

If the game is complete:

```text
FROG: POND TO PEAK

A small jump to the waterfall

Play Again
New Game
Controls
```

If a save exists and New Game is selected:

```text
Start over?

Yes
No
```

Design logic:

- Continue is the primary returning-player action.
- New Game requires confirmation only if a save exists.
- Play Again appears only after completion.

---

## 22. Controls Screen

Content:

```text
CONTROLS

Move: A / D or Left / Right
Jump / Swim: Space / W / Up
Pause: Esc

Menus:
Move: W / S or Up / Down
Confirm: Enter or Space
Back: Esc

Press Esc to go back
```

---

## 23. Pause Menu

Content:

```text
PAUSED

Resume
Restart Level
Controls
Quit to Title
```

Rules:

- Resume returns to the current level state.
- Restart Level resets the entire level.
- Controls opens the Controls screen.
- Quit to Title saves the current unlocked level and returns to title.

Design logic:

- Restart Level is the escape hatch for unfair or confusing moments.
- Quitting does not save in-level progress.

---

## 24. Feel Targets

The game should feel:

- responsive
- small
- bouncy
- forgiving
- readable

Specific feel targets:

- The frog should stop quickly on ground.
- The frog should adjust in air.
- Jumps should feel short and punchy.
- Lily pads should feel like a reward for landing.
- Water should feel dense but controllable.
- Enemies should be readable before they become dangerous.
- Checkpoints should feel like a relief.
- The boss should feel like a pattern to dodge, not a precision test.

Design logic:

- The frog is small, so movement should feel light.
- The game is short, so frustration should be low.
- The player should always understand why they died.

---

## 25. Difficulty Curve

Level difficulty:

1. Pond Edge: very easy
2. Lily Rush: easy, introduces water
3. Reed Hollow: moderate, introduces verticality
4. Stormy Creek: moderate, introduces currents
5. Cliffside Ponds: hard, combines mechanics
6. Great Waterfall: boss

Enemy count by level:

- Level 1: 1 mosquito
- Level 2: 1 dragonfly
- Level 3: 1 mosquito
- Level 4: 2 dragonflies
- Level 5: 1 mosquito, 1 dragonfly
- Level 6: 1 heron

Design logic:

- Difficulty rises by adding one idea at a time.
- Level 5 is the hardest platforming level.
- Level 6 is the climax but uses only learned mechanics.

---

## 26. Edge Cases

## 26.1 No Save

If no save exists:

- Title shows:
  - New Game
  - Controls
- Continue is hidden.

---

## 26.2 Completed Save

If the game is complete:

- Title shows:
  - Play Again
  - New Game
  - Controls
- Continue is hidden.

---

## 26.3 Player Falls Below Level

If player y > level_height + 100:

- death triggers
- respawn at last checkpoint or spawn

---

## 26.4 Player Falls Into Water

If player falls into water:

- no death
- no fall damage
- vertical velocity is capped at 220 px/s
- water physics apply

---

## 26.5 Player Touches Enemy While Invulnerable

If player is invulnerable:

- damage is ignored
- stomp checks still work
- if stomp conditions are met, the enemy is stomped

---

## 26.6 Player Touches Multiple Enemies

If the player overlaps multiple enemies:

- process stomps first
- if no stomp applies, apply one damage instance
- do not apply multiple damage instances in the same frame

---

## 26.7 Player Touches Thorn and Enemy

If the player touches a thorn and an enemy at the same time:

- stomp checks happen first
- if no stomp applies, apply one damage instance
- do not apply multiple damage instances in the same frame

---

## 26.8 Player Lands on Lily Pad While Holding Jump

If the player lands on a lily pad while holding Jump:

- bounce velocity is -680 px/s

If the player lands without holding Jump:

- bounce velocity is -620 px/s

---

## 26.9 Player Bounces Into Ceiling

If the player bounces into the ceiling:

- vertical velocity becomes 0
- the player falls normally

---

## 26.10 Player Bounces Into Water

If the player bounces from a lily pad into water:

- water physics apply
- vertical velocity is capped at 220 px/s

---

## 26.11 Player Is Pushed by Current Into Thorn

If a current pushes the player into a thorn:

- the player takes damage
- knockback applies
- the player may be knocked back into water

---

## 26.12 Player Dies on Moving Platform

If the player dies while on a moving platform:

- respawn at checkpoint or spawn
- moving platforms reset to initial phase

---

## 26.13 Player Dies After Boss Is Defeated

If the boss is dead and the player dies before touching the exit:

- respawn at level spawn
- boss remains dead
- exit remains unlocked

---

## 26.14 Player Restarts Level From Pause

If the player selects Restart Level:

- level resets completely
- dewdrops reset
- enemies reset
- moving platforms reset
- player respawns at level spawn
- hearts refill to 3

---

## 26.15 Player Quits to Title

If the player quits to title:

- save current unlocked level
- do not save in-level progress
- do not save dewdrops
- do not save boss HP

---

## 26.16 Player Reaches Exit While Boss Is Alive

In Level 6:

- if the boss is alive, the exit does nothing
- if the boss is dead, the exit completes the level

---

## 26.17 Player Touches Checkpoint While Invulnerable

If the player touches a checkpoint while invulnerable:

- checkpoint still activates
- hearts refill
- respawn point updates

---

## 26.18 Player Collects Dewdrop While Invulnerable

If the player touches a dewdrop while invulnerable:

- dewdrop is collected normally

---

## 26.19 Player Pauses During Death

Pause is disabled during death.

---

## 26.20 Player Pauses During Level Complete

Pause is disabled during Level Complete.

---

## 27. Required Audio Events

Audio specifics are out of scope, but these gameplay events require audio cues:

- jump
- water splash
- lily pad bounce
- stomp
- damage
- checkpoint
- level complete
- boss hit
- boss death
- game complete

Design logic:

- These events are important for feedback.
- The visual/audio agent decides the actual sounds.

---

## 28. Visual Design Notes for Handoff

The visual designer does not define gameplay, but these elements must be visible:

### Player

- frog hitbox area
- facing direction
- invulnerability flash or blink
- death state

### HUD

- 3 health icons
- dewdrop icon and count
- message area

### World

- solid ground
- one-way leaf platforms
- lily pads
- water
- water currents
- thorns
- dewdrops
- lotus checkpoints
- waterfall exits
- moving platforms

### Enemies

- mosquito
- dragonfly
- thorn
- heron boss

### Boss

- heron body
- heron head stomp zone
- heron HP state
- boss death state

### Exits

- active waterfall
- locked waterfall in Level 6

Design logic:

- The player must be able to distinguish safe platforms, bouncy lily pads, water, hazards, enemies, and objectives.

---

## 29. Cut List

The following ideas were considered and cut:

- double jump
- wall jump
- dash
- tongue attack
- power-ups
- permanent upgrades
- score
- timer
- star ratings
- level select
- open world
- secret levels
- multiple frogs
- companion character
- inventory
- weapon
- health pickups
- lives
- meta-unlocks
- difficulty modes
- controller support
- remappable controls

Design logic:

- The game is short and focused.
- Each cut keeps the frog’s identity clear.
- The core fantasy is a small frog making a big journey, not a frog collecting power.
- The game is better with fewer systems and tighter spacing.