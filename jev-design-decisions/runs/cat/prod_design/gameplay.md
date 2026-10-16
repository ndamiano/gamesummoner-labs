# gameplay.md

## 1. Game Identity

Working title: **Cat: Mice Hunt**

This is a short, complete 2D top-down arcade game. The player controls a cat in a single-screen arena. Mice emerge from holes and try to escape back into holes. The cat must catch the required number of mice before too many escape.

The game is designed to be:

- Easy to understand in 10 seconds.
- Easy to play, but demanding enough to retry.
- Complete from start to finish with no missing states.
- Smoothly progressive from tutorial to final level and then endless mode.

---

## 2. Dimensionality

Use **2D top-down gameplay**.

- All movement, collision, AI, and catching happen in a single 2D plane.
- There is no camera scrolling.
- Each level is a single fixed arena.
- The game may use 2.5D presentation, such as shadows, height, or parallax, but depth must not affect gameplay.
- No 3D movement, no aiming in 3D, no depth-based collisions.

**Why:**  
A single-screen 2D top-down arena is the clearest way to make a browser cat-and-mouse game. It avoids camera complexity, makes mouse AI easier to read, and keeps the player focused on chasing and pouncing.

---

## 3. Core Loop

1. A level begins.
2. Mice spawn from holes.
3. Mice flee from the cat.
4. After a short time, mice try to escape back into holes.
5. The cat catches mice by touching them or pouncing on them.
6. If the cat catches enough mice, the level is complete.
7. If too many mice escape, the level fails.

The core fantasy is:

> The cat is fast, playful, and slightly overconfident. The mice are small, nervous, and always trying to get away.

The core tension is:

> Can you catch the mouse before it disappears?

---

## 4. Objective

Each level has a clear objective:

> Catch **X** mice.  
> Do not let **3** mice escape.

- The player starts each level with 3 lives.
- Each escaped mouse costs 1 life.
- If 3 mice escape, the level fails.
- If the player catches the required number of mice before losing all lives, the level is complete.

**Why:**  
This creates immediate stakes without requiring a timer. The player does not need to understand a countdown; they only need to understand: catch mice, stop them from hiding.

---

## 5. Arena and Layout

All levels use the same playable arena size:

- Playable area: **960 x 540 pixels**
- Single screen
- No camera movement
- Walls at the outer edge
- Cat start position: **480, 270** for all levels

Entities use 2D positions:

- `x` increases to the right.
- `y` increases downward.

### 5.1 Arena Elements

Each level contains:

- The cat.
- Mice.
- Holes.
- Obstacles.
- Arena bounds.

### 5.2 Holes

Holes are circular spawn and escape points.

- Hole radius: **24 pixels**
- Mice spawn from holes.
- Mice can enter any hole to escape.
- A mouse can enter a hole only if:
  - It has been out for at least **2.5 seconds**.
  - It is within **24 pixels** of the hole center.
  - The hole is not currently occupied.
  - The cat is not blocking the hole.

A hole is considered **occupied** for **0.8 seconds** after a mouse begins entering it.

A hole is considered **blocked** if the cat’s center is within **40 pixels** of the hole center.

**Why:**  
Holes create the main cat-and-mouse dynamic. The player can chase mice, but can also temporarily block one hole by standing on it. This adds light tactics without requiring a separate ability.

### 5.3 Obstacles

Obstacles are solid rectangular objects.

- They block movement for both cat and mice.
- They do not block hole entry unless a hole overlaps them.
- Level layouts are designed so holes are never inside obstacles.
- No level should make a mouse permanently unreachable.
- Obstacles should create chase variety, not mazes.

Obstacle format:

```text
x, y, width, height
```

### 5.4 Level Design Goals

Levels should:

- Start simple.
- Add one new idea at a time.
- Increase mouse count and speed gradually.
- Introduce more holes before increasing difficulty too much.
- Keep every level playable in under 60 seconds for a competent player.
- Keep no level frustratingly long.

---

## 6. Entities

### 6.1 Cat

The player controls one cat.

Cat properties:

- Radius: **18 pixels**
- Max speed: **260 pixels/second**
- Acceleration: **2200 pixels/second²**
- Friction/deceleration: **1200 pixels/second²**
- Pounce speed: **520 pixels/second**
- Pounce duration: **0.18 seconds**
- Pounce cooldown: **0.8 seconds**
- Input buffer for pounce: **0.1 seconds**

The cat can:

- Move in 2D.
- Pounce in the current movement direction.
- Catch mice by contact.
- Temporarily block holes by standing near them.

The cat does not have health. Lives are based on escaped mice.

**Why:**  
The cat should feel fast and responsive. The pounce gives the player a satisfying burst of speed without needing stamina, health, or complex resources.

### 6.2 Mice

Mice are the main interactive enemies/prey.

Mouse states:

1. **Emerging**
2. **Fleeing**
3. **Entering hole**
4. **Caught**
5. **Escaped**

Mouse states are explained in Section 9.

Mouse properties by type:

| Mouse Type | Speed | Radius | Special |
|---|---:|---:|---|
| Normal | 180 | 14 | None |
| Fast | 220 | 12 | Moves faster |
| Big | 150 | 20 | Can only be caught while the cat is pouncing |

All mice:

- Acceleration: **1800 pixels/second²**
- Can be caught by normal contact unless they are Big mice.
- Can escape into holes after **2.5 seconds**.
- Cannot enter a blocked hole.
- Cannot enter an occupied hole.

**Why:**  
Three mouse types are enough. Normal teaches the base loop, Fast increases pressure, and Big forces the player to use pouncing intentionally. Adding more mouse types would complicate AI and HUD without improving the core chase.

---

## 7. Controls

### 7.1 Movement

Move the cat with:

- **W / A / S / D**
- **Arrow keys**

Movement is 2D top-down.

### 7.2 Pounce

Pounce with:

- **Space**
- **Left mouse button**

Pounce direction:

- If the player is currently moving, pounce in the movement direction.
- If the player is not moving, pounce in the last movement direction.
- If the cat has never moved, pounce to the right.

### 7.3 Pause

Pause with:

- **Esc**
- **P**

**Why:**  
Keyboard and mouse support is needed for browser play. Pouncing with either input makes the game accessible without requiring complex input mapping.

---

## 8. Core Systems

The game uses the following systems:

1. Game state system.
2. Cat movement system.
3. Mouse AI system.
4. Collision system.
5. Hole system.
6. Spawning system.
7. Catching system.
8. Escape system.
9. Lives system.
10. Scoring system.
11. Combo system.
12. Level progression system.
13. Endless mode system.
14. HUD system.
15. UI flow system.

---

## 9. Mouse AI

Mouse AI is a simple state machine.

### 9.1 Mouse States

#### 9.1.1 Emerging

A mouse begins in the **Emerging** state when it spawns.

- Duration: **0.25 seconds**
- Mouse does not move.
- Mouse is not catchable during this state.
- After the timer ends, the mouse becomes **Fleeing**.

**Why:**  
This prevents the player from catching a mouse before it is visible and gives the player a fair reaction window.

#### 9.1.2 Fleeing

This is the normal active state.

The mouse:

- Moves away from the cat.
- Wanders slightly.
- Tries to find a hole after **2.5 seconds**.
- Avoids obstacles.
- Avoids overlapping other mice.
- Can be caught by contact.

Fleeing behavior:

- If the cat is within **140 pixels**, the mouse strongly flees away from the cat.
- If the cat is farther than **140 pixels**, the mouse wanders more.
- After **2.5 seconds** out, the mouse begins seeking the nearest available hole.
- The hole-seeking weight increases the longer the mouse is out.

Wander behavior:

- Each mouse has a wander direction.
- Every **0.3 to 0.6 seconds**, the mouse changes its wander direction by a random angle between **-45 degrees** and **+45 degrees**.

Separation behavior:

- If another mouse is within **28 pixels**, the mouse moves away from it.

**Why:**  
Mice should feel like prey. They should panic when the cat is close, but not be so perfect that they are impossible to catch.

#### 9.1.3 Entering Hole

A mouse enters this state when it decides to escape.

- Duration: **0.3 seconds**
- The mouse moves slightly toward the hole center.
- The hole becomes occupied for **0.8 seconds**.
- The mouse is still catchable during this state.
- If caught during this state, the mouse is caught and does not escape.
- If the timer ends, the mouse escapes.

**Why:**  
Allowing the player to catch a mouse while it is entering a hole rewards precise timing and prevents escape from feeling instant and unfair.

#### 9.1.4 Caught

The mouse is removed from the arena.

- Score is added.
- Combo is updated.
- Catch event is processed.

#### 9.1.5 Escaped

The mouse is removed from the arena.

- The player loses 1 life.
- Combo resets.
- Escape event is processed.

---

## 10. Mouse Movement Algorithm

Use the following algorithm for each mouse in the **Fleeing** state.

```text
out_time += dt

desired = vector(0, 0)

distance_to_cat = distance(mouse_position, cat_position)

if distance_to_cat < 140:
    desired += normalize(mouse_position - cat_position) * 1.0
else:
    desired += normalize(mouse_position - cat_position) * 0.3

desired += mouse.wander_direction * 0.6

if mouse.out_time >= 2.5 and mouse.startle_timer <= 0:
    hole = nearest_available_hole(mouse)
    if hole exists:
        seek_weight = min(1.5, 0.5 + (mouse.out_time - 2.5))
        desired += normalize(hole.position - mouse.position) * seek_weight

desired += separation_from_other_mice(mouse)

if desired.length < 0.1:
    desired = mouse.wander_direction

desired = avoid_obstacles(mouse.position, desired)

mouse.velocity += normalize(desired) * mouse.acceleration * dt
mouse.velocity = clamp_length(mouse.velocity, mouse.max_speed)
mouse.position += mouse.velocity * dt
resolve_collisions(mouse)
```

### 10.1 Nearest Available Hole

A hole is available if:

```text
hole.occupied_timer <= 0
and distance(cat_position, hole.position) > 40
```

The mouse chooses the nearest available hole.

If no hole is available, the mouse does not seek a hole and continues fleeing/wandering.

### 10.2 Obstacle Avoidance

Use simple predicted collision avoidance.

```text
function avoid_obstacles(position, desired_direction):
    test_position = position + desired_direction * 20

    if test_position does not collide with any obstacle:
        return desired_direction

    for angle in [30, -30, 60, -60, 90, -90, 120, -120]:
        rotated = rotate(desired_direction, angle)
        test_position = position + rotated * 20
        if test_position does not collide with any obstacle:
            return rotated

    return rotate(desired_direction, 180)
```

**Why:**  
Full pathfinding is unnecessary for a single-screen arena. Simple avoidance keeps the AI readable and cheap enough for a browser game.

---

## 11. Cat Movement Algorithm

```text
function update_cat(dt):
    input = normalized movement input vector

    if pounce_pressed and pounce_cooldown <= 0:
        if input.length > 0:
            pounce_direction = input
            last_direction = input
        else:
            pounce_direction = last_direction

        pounce_timer = 0.18
        pounce_cooldown = 0.8

    if pounce_timer > 0:
        cat.velocity = pounce_direction * 520
        pounce_timer -= dt
    else:
        if input.length > 0:
            cat.velocity += input * 2200 * dt
            last_direction = input
        else:
            cat.velocity = move_toward(cat.velocity, 0, 1200 * dt)

        cat.velocity = clamp_length(cat.velocity, 260)

    cat.position += cat.velocity * dt
    resolve_collisions(cat)

    pounce_cooldown = max(0, pounce_cooldown - dt)
```

### 11.1 Pounce Buffer

If the player presses pounce while the cooldown is still active, store the input for **0.1 seconds**.

If the cooldown becomes ready within that window, execute the pounce.

**Why:**  
This makes pouncing feel responsive and avoids frustrating missed inputs.

---

## 12. Collision System

All collisions are 2D circle-based.

### 12.1 Circle vs Arena Bounds

Clamp each entity:

```text
x = clamp(x, radius, 960 - radius)
y = clamp(y, radius, 540 - radius)
```

### 12.2 Circle vs Obstacle AABB

For each obstacle:

```text
closest_x = clamp(circle.x, obstacle.x, obstacle.x + obstacle.width)
closest_y = clamp(circle.y, obstacle.y, obstacle.y + obstacle.height)

dx = circle.x - closest_x
dy = circle.y - closest_y
distance = sqrt(dx*dx + dy*dy)

if distance < circle.radius:
    push circle out along (dx, dy)
```

If `distance == 0`, push the circle out using the smallest axis overlap.

### 12.3 Catch Collision

A mouse is caught if:

```text
distance(cat_position, mouse_position) < cat.radius + mouse.radius
```

Catchable mouse states:

- Fleeing
- Entering hole

Not catchable states:

- Emerging
- Caught
- Escaped

**Why:**  
Circle collision is simple, stable, and appropriate for a top-down browser game.

---

## 13. Hole System

### 13.1 Hole Data

Each hole has:

- Position: `x, y`
- Radius: `24`
- Occupied timer: starts at `0`
- Blocked state: calculated from cat position

### 13.2 Hole Occupancy

When a mouse begins entering a hole:

```text
hole.occupied_timer = 0.8
```

While `occupied_timer > 0`, no other mouse can enter that hole.

The occupied timer continues even if the mouse is caught during entry.

### 13.3 Hole Blocking

A mouse cannot enter a hole if:

```text
distance(cat_position, hole.position) <= 40
```

The cat does not need a special action to block a hole. Standing near the hole is enough.

**Why:**  
This gives the player a simple defensive tactic without adding a button, resource, or UI state.

---

## 14. Spawning System

Mice spawn from holes.

### 14.1 Spawn Conditions

A mouse can spawn if:

- The level is in the **Playing** state.
- `caught_count < target_catches`
- `active_mouse_count < max_active_mice`
- `spawn_timer <= 0`
- At least one hole is available.

A hole is available for spawning if:

```text
hole.occupied_timer <= 0
and distance(cat_position, hole.position) > 40
```

### 14.2 Spawn Timer

At the start of a level:

```text
spawn_timer = 1.0
```

After each spawn:

```text
spawn_timer = level.spawn_interval
```

If no hole is available, the spawn timer keeps counting down, but spawning is delayed until a hole becomes available.

### 14.3 Mouse Type Selection

Use the level’s mouse mix weights.

Example:

```text
Normal: 50
Fast: 30
Big: 20
```

To choose a mouse:

```text
total = sum(weights)
random_value = random(0, total)

subtract weights until random_value falls below a weight
```

**Why:**  
Weighted random selection lets levels introduce and mix mouse types without complex scripting.

---

## 15. Catching System

When the cat touches a catchable mouse:

1. Set mouse state to **Caught**.
2. Remove the mouse from the active mouse list.
3. Increase `caught_count` by 1.
4. Add score.
5. Update combo.
6. Play catch audio cue.
7. If `caught_count >= target_catches`, trigger level complete.

### 15.1 Normal Catch

A Normal or Fast mouse can be caught by any cat contact.

### 15.2 Big Mouse Catch

A Big mouse can only be caught if:

```text
cat.pounce_timer > 0
```

If the cat touches a Big mouse while not pouncing:

- No catch occurs.
- The mouse becomes **startled** for **0.3 seconds**.
- While startled:
  - Its max speed is multiplied by **1.3**.
  - It cannot seek holes.
  - It continues fleeing from the cat.

**Why:**  
Big mice make pouncing meaningful. They are slower, so they are not impossible, but they force the player to use the cat’s main action.

---

## 16. Escape System

A mouse escapes when it completes entering a hole.

When a mouse escapes:

1. Set mouse state to **Escaped**.
2. Remove the mouse from the active mouse list.
3. Decrease `lives` by 1.
4. Reset combo to 0.
5. Play escape audio cue.
6. If `lives <= 0`, trigger game over.

**Why:**  
Escaping is the only failure condition. This keeps the player’s goal clear: prevent mice from hiding.

---

## 17. Lives System

Each level starts with:

```text
lives = 3
```

Each escaped mouse reduces lives by 1.

If lives reach 0, the level fails.

Lives reset to 3 at the start of each level and each endless wave.

**Why:**  
Three lives is simple and forgiving enough for a browser game. It also matches the “don’t let 3 mice escape” rule.

---

## 18. Scoring System

Score is used for high scores and light competitive feedback.

### 18.1 Catch Score

For each caught mouse:

```text
base_points = 100
bonus_points = 0

if cat.pounce_timer > 0:
    bonus_points += 50

if mouse.out_time < 1.0:
    bonus_points += 50

points = base_points + bonus_points
score += floor(points * combo_multiplier)
```

### 18.2 Multi-Catch Bonus

If the cat catches multiple mice in the same frame or catch event:

```text
multi_catch_bonus = 100 * (number_of_mice_caught - 1)
score += multi_catch_bonus
```

This bonus is added once per catch event, not per mouse.

### 18.3 Combo System

Combo increases when the player catches mice quickly.

Rules:

- `combo` starts at 0.
- On each catch:
  - If time since last catch is less than or equal to **3.0 seconds**, increase combo by 1.
  - Otherwise, set combo to 1.
- Combo multiplier:

```text
combo_multiplier = 1.0 + 0.25 * (combo - 1)
combo_multiplier = min(3.0, combo_multiplier)
```

- If a mouse escapes, combo resets to 0.
- If no catch occurs for 3.0 seconds, combo resets to 0.

### 18.4 Level Complete Bonus

When a level is completed:

```text
bonus = lives * 500

if escapes_in_level == 0:
    bonus += 1000

score += bonus
```

### 18.5 Endless Wave Bonus

When an endless wave is completed:

```text
bonus = wave_number * 500
bonus += lives * 250

if escapes_in_wave == 0:
    bonus += 1000

score += bonus
```

**Why:**  
Score rewards skill and speed without becoming the main objective. Combo encourages aggressive play, while life bonus rewards clean play.

---

## 19. Level Progression

The campaign consists of **10 levels**.

After completing Level 10, the player unlocks **Endless Mode**.

### 19.1 Campaign Flow

1. Main Menu.
2. Player presses Play.
3. Level 1 starts.
4. Level intro.
5. Gameplay.
6. Level complete.
7. Next level starts automatically after a short delay.
8. Repeat until Level 10.
9. Campaign complete.
10. Endless Mode unlocked.

### 19.2 Failure Flow

If the player fails a level:

1. Show Game Over.
2. Offer Retry Level.
3. Retry restarts the same level.
4. Score resets to the score at the start of that level.
5. Lives reset to 3.

### 19.3 Why No Level Select?

There is no level select screen.

**Why:**  
The campaign is short and linear. A level select screen would add UI complexity without improving the core experience. Retry is enough.

---

## 20. Level Content

All levels use the same arena size: **960 x 540**.

Cat start position for all levels:

```text
480, 270
```

Lives for all levels:

```text
3
```

### 20.1 Level Parameters Table

| Level | Target | Max Active | Spawn Interval | Mouse Mix | Notes |
|---:|---:|---:|---:|---|---|
| 1 | 5 | 2 | 2.0 | Normal 100 | Tutorial |
| 2 | 8 | 3 | 1.8 | Normal 100 | More holes |
| 3 | 10 | 3 | 1.6 | Normal 75, Fast 25 | Introduce Fast |
| 4 | 10 | 3 | 1.6 | Normal 80, Big 20 | Introduce Big |
| 5 | 12 | 4 | 1.5 | Normal 50, Fast 30, Big 20 | First mix |
| 6 | 14 | 4 | 1.4 | Normal 40, Fast 40, Big 20 | More pressure |
| 7 | 16 | 4 | 1.3 | Normal 30, Fast 50, Big 20 | Fast-heavy |
| 8 | 16 | 5 | 1.2 | Normal 30, Fast 30, Big 40 | Big-heavy |
| 9 | 18 | 5 | 1.1 | Normal 30, Fast 35, Big 35 | Mixed pressure |
| 10 | 20 | 5 | 1.0 | Normal 25, Fast 45, Big 30 | Final level |

### 20.2 Level Layouts

Coordinates are in the 960 x 540 arena.

Holes are listed as:

```text
x, y
```

Obstacles are listed as:

```text
x, y, width, height
```

---

### Level 1

Holes:

```text
120, 420
840, 420
```

Obstacles:

```text
none
```

Notes:

- Teaches movement, catching, and hole escape.
- Only two active mice at a time.
- No obstacles.

---

### Level 2

Holes:

```text
120, 120
840, 120
480, 440
```

Obstacles:

```text
400, 230, 160, 80
```

Notes:

- Adds a third hole.
- Adds one central obstacle.

---

### Level 3

Holes:

```text
120, 420
480, 120
840, 420
```

Obstacles:

```text
180, 180, 120, 80
660, 300, 120, 80
```

Notes:

- Introduces Fast mice.
- Mice become harder to chase.

---

### Level 4

Holes:

```text
120, 120
840, 120
120, 420
840, 420
```

Obstacles:

```text
300, 150, 200, 80
480, 330, 120, 120
```

Notes:

- Introduces Big mice.
- Player must use pounce to catch Big mice.

---

### Level 5

Holes:

```text
120, 120
480, 440
840, 120
```

Obstacles:

```text
150, 200, 120, 120
690, 200, 120, 120
```

Notes:

- First mixed mouse types.
- Two large side obstacles.

---

### Level 6

Holes:

```text
120, 120
840, 120
120, 420
840, 420
```

Obstacles:

```text
360, 120, 240, 80
240, 320, 120, 80
600, 320, 120, 80
```

Notes:

- More holes.
- Obstacles create multiple chase lanes.

---

### Level 7

Holes:

```text
120, 120
480, 120
840, 120
480, 440
```

Obstacles:

```text
180, 180, 100, 180
680, 180, 100, 180
```

Notes:

- Fast-heavy level.
- Vertical obstacles create narrow chases.

---

### Level 8

Holes:

```text
120, 120
840, 120
120, 420
480, 440
840, 420
```

Obstacles:

```text
300, 120, 120, 80
540, 120, 120, 80
420, 300, 120, 80
```

Notes:

- Big-heavy level.
- Five holes increase escape pressure.

---

### Level 9

Holes:

```text
120, 120
480, 120
840, 120
120, 420
840, 420
```

Obstacles:

```text
200, 200, 120, 80
420, 320, 120, 80
640, 200, 120, 80
```

Notes:

- Mixed pressure.
- Obstacles are spread to prevent camping.

---

### Level 10

Holes:

```text
120, 120
480, 120
840, 120
120, 420
480, 440
840, 420
```

Obstacles:

```text
160, 160, 120, 120
680, 160, 120, 120
400, 320, 160, 80
```

Notes:

- Final campaign level.
- Six holes.
- Highest target.
- Fast and Big mice are common.

---

## 21. Mouse Type Content

### 21.1 Normal Mouse

- First appears: Level 1
- Speed: 180
- Radius: 14
- Behavior: Standard fleeing and hole-seeking.
- Purpose: Teaches the base loop.

### 21.2 Fast Mouse

- First appears: Level 3
- Speed: 220
- Radius: 12
- Behavior: Same as Normal, but faster.
- Purpose: Increases chase pressure.

### 21.3 Big Mouse

- First appears: Level 4
- Speed: 150
- Radius: 20
- Behavior:
  - Cannot be caught by normal contact.
  - Can only be caught while the cat is pouncing.
  - If touched by a non-pouncing cat, becomes startled for 0.3 seconds.
  - While startled, its speed is multiplied by 1.3 and it cannot seek holes.
- Purpose: Makes pouncing a required skill.

**Why only three types:**  
Three types are enough to create variety without overcomplicating AI, HUD, or player learning.

---

## 22. Endless Mode

Endless Mode unlocks after completing Level 10.

Endless Mode is a separate score track.

### 22.1 Endless Structure

Endless Mode is divided into waves.

Each wave:

- Uses a layout.
- Has a target number of mice.
- Starts with 3 lives.
- Has its own spawn interval and max active mice.
- Has its own mouse mix.
- Carries score forward to the next wave.

If the player fails a wave:

- The wave can be retried.
- Score resets to the score at the start of that wave.
- Lives reset to 3.

### 22.2 Endless Wave Layouts

Endless waves rotate through these layouts:

```text
Wave 1: Level 10 layout
Wave 2: Level 9 layout
Wave 3: Level 8 layout
Wave 4: Level 10 layout
Wave 5: Level 9 layout
...
```

Formula:

```text
layout_index = [10, 9, 8][(wave_number - 1) % 3]
```

Use the holes and obstacles from the selected level layout.

### 22.3 Endless Wave Parameters

For wave number `w`:

```text
target = min(50, 15 + 5 * (w - 1))

spawn_interval = max(0.6, 1.0 - 0.05 * (w - 1))

max_active = min(7, 4 + floor((w + 1) / 2))

lives = 3
```

### 22.4 Endless Mouse Mix

Use weighted random selection:

```text
normal_weight = max(10, 40 - 2 * (w - 1))
fast_weight = 35 + 2 * (w - 1)
big_weight = 25 + 2 * (w - 1)
```

Normalize the weights before choosing a mouse.

### 22.5 Endless Progression

- Score carries between waves.
- Lives reset to 3 each wave.
- Combo resets each wave.
- Wave complete bonus is added.
- Next wave starts automatically after 3 seconds.

**Why:**  
Endless Mode gives the game a post-campaign goal without requiring a second game mode with different rules.

---

## 23. Game States

The game must support these states.

### 23.1 Main Menu

Content:

- Title.
- Play button.
- Endless button, only if unlocked.
- How to Play button.

Behavior:

- Play starts Level 1 with score 0.
- Endless starts Wave 1 with score 0.
- How to Play opens the How to Play screen.

### 23.2 How to Play

Content:

- Controls.
- Objective.
- Mouse types.
- Pounce explanation.
- Combo explanation.

Behavior:

- Back button returns to Main Menu.

### 23.3 Level Intro

Duration: **1.5 seconds**

Content:

- Level number.
- Target number.
- Lives.
- New mouse type, if applicable.
- Short objective text.

Behavior:

- Cat is controllable.
- No mice spawn during intro.
- After intro, the level enters the Playing state.
- First mouse spawns 1.0 seconds after intro ends.

### 23.4 Playing

This is the main gameplay state.

Behavior:

- Cat can move and pounce.
- Mice update.
- Spawning occurs.
- Catching and escaping occur.
- HUD updates.

### 23.5 Paused

Triggered by:

- Esc
- P
- Browser losing focus

Content:

- Paused text.
- Resume button.
- Restart button.
- Main Menu button.

Behavior:

- All gameplay timers stop.
- No spawning.
- No mouse movement.
- No score changes.

### 23.6 Level Complete

Triggered when:

```text
caught_count >= target_catches
```

Content:

- Level number.
- Score.
- Bonus breakdown.
- High score if updated.
- Next Level button or automatic progression.

Behavior:

- Gameplay stops.
- After 3 seconds, automatically start next level.
- Player can also press Next immediately.
- If Level 10 is complete, go to Campaign Complete.

### 23.7 Campaign Complete

Triggered after Level 10.

Content:

- Campaign Complete text.
- Final score.
- High score.
- Play Endless button.
- Main Menu button.

Behavior:

- Marks Endless Mode as unlocked.
- Saves high score.

### 23.8 Game Over

Triggered when:

```text
lives <= 0
```

and target was not reached.

Content:

- Game Over text.
- Level number.
- Score.
- Retry Level button.
- Main Menu button.

Behavior:

- Retry restarts the same level.
- Score resets to the score at the start of that level.
- Lives reset to 3.

### 23.9 Endless Wave Complete

Triggered when:

```text
caught_count >= target_catches
```

in Endless Mode.

Content:

- Wave number.
- Score.
- Bonus breakdown.
- Next Wave in 3 seconds.

Behavior:

- Gameplay stops.
- After 3 seconds, start next wave.
- Score carries forward.
- Lives reset to 3.

### 23.10 Endless Game Over

Triggered when:

```text
lives <= 0
```

in Endless Mode.

Content:

- Game Over text.
- Wave number.
- Score.
- Retry Wave button.
- Main Menu button.

Behavior:

- Retry Wave restarts the same wave.
- Score resets to the score at the start of that wave.
- Lives reset to 3.

---

## 24. HUD

The HUD must always show the player’s current objective, score, lives, and pounce availability.

### 24.1 Top Left

Display:

```text
Score: 000000
Combo: x1.25
Level 3
```

or, in Endless Mode:

```text
Score: 000000
Combo: x1.25
Wave 5
```

Rules:

- Score is always shown.
- Combo is shown only when combo multiplier is greater than 1.0.
- Level or Wave is always shown.

### 24.2 Top Center

Display progress:

```text
Caught: 7 / 10
```

Also display a progress bar.

Progress bar rules:

- Fills from left to right.
- Fill amount = `caught_count / target_catches`
- Clamp fill between 0 and 1.

### 24.3 Top Right

Display lives:

- Show 3 mouse icons.
- Full icons represent remaining lives.
- Empty or greyed icons represent lost lives.

Also display pause button:

```text
II
```

### 24.4 Bottom Center

Display pounce cooldown:

- A horizontal bar.
- Width: **120 pixels**
- Height: **8 pixels**
- Fills from left to right as pounce becomes ready.
- When full, pounce is ready.

Optional label:

```text
Pounce
```

### 24.5 Center Screen Messages

Show temporary center messages for major events.

Examples:

- `Level 3`
- `Catch 10 mice`
- `New mouse type: Fast`
- `Mouse escaped!`
- `Level Complete`
- `Game Over`
- `Wave 5`
- `Next wave in 3`

Rules:

- Messages should not block gameplay.
- Duration: **1.0 to 1.5 seconds**
- Only one message at a time.
- Higher priority messages replace lower priority ones.

Priority order:

1. Game Over
2. Level Complete
3. Wave Complete
4. Mouse escaped
5. New mouse type
6. Level/Wave start

---

## 25. UI Section Content

### 25.1 Main Menu

Content:

- Game title.
- Play.
- Endless, if unlocked.
- How to Play.

Behavior:

- Play starts Level 1.
- Endless starts Wave 1.
- How to Play opens instructions.

### 25.2 How to Play

Content:

```text
Move: WASD or Arrow Keys
Pounce: Space or Left Click

Catch mice before they hide.
Mice can hide in holes after 2.5 seconds.
Pounce to catch Big mice.
Catch mice quickly to build combo.
Do not let 3 mice escape.
```

Mouse type descriptions:

```text
Normal: Standard mouse.
Fast: Faster, smaller mouse.
Big: Can only be caught while pouncing.
```

Behavior:

- Back returns to Main Menu.

### 25.3 Level Intro

Content:

```text
Level X
Catch Y mice
3 lives
```

If a new mouse type appears:

```text
New mouse type: Fast
```

or:

```text
New mouse type: Big
```

Behavior:

- Lasts 1.5 seconds.
- Cat is controllable.
- No spawning.

### 25.4 Gameplay HUD

See Section 24.

### 25.5 Level Complete

Content:

```text
Level X Complete
Score: N
Bonus: N
High Score: N
Next Level
```

Behavior:

- Automatically advances after 3 seconds.
- Player can click Next immediately.

### 25.6 Campaign Complete

Content:

```text
Campaign Complete
Score: N
High Score: N
Play Endless
Main Menu
```

Behavior:

- Unlocks Endless Mode.
- Saves high score.

### 25.7 Game Over

Content:

```text
Game Over
Level X
Score: N
Retry Level
Main Menu
```

Behavior:

- Retry restarts current level.
- Score resets to level start score.

### 25.8 Endless Wave Complete

Content:

```text
Wave X Complete
Score: N
Bonus: N
Next Wave in 3
```

Behavior:

- Automatically starts next wave after 3 seconds.

### 25.9 Endless Game Over

Content:

```text
Game Over
Wave X
Score: N
Retry Wave
Main Menu
```

Behavior:

- Retry restarts current wave.
- Score resets to wave start score.

### 25.10 Pause Overlay

Content:

```text
Paused
Resume
Restart
Main Menu
```

Behavior:

- Resume returns to gameplay.
- Restart restarts current level or wave.
- Main Menu returns to Main Menu.

---

## 26. Required Audio Cues

The visual/audio designer chooses the actual sounds. The gameplay system should trigger these cues.

Required audio cues:

- UI click.
- Pounce whoosh.
- Mouse catch pop.
- Multi-catch chime.
- Big mouse startle squeak.
- Mouse escape squeak.
- Combo milestone sound, if desired.
- Level complete jingle.
- Campaign complete jingle.
- Game over sting.
- Endless wave complete jingle.
- Endless game over sting.

**Why:**  
Audio cues make catching, escaping, and pouncing readable, but the actual sound design is outside this document.

---

## 27. Feel and Balance Notes

The game should feel:

- Snappy.
- Slightly frantic.
- Fair.
- Readable.

### 27.1 Cat Feel

The cat should always feel responsive.

Key feelings:

- Movement should start immediately.
- Pounce should feel like a burst, not a slow dash.
- The cat should be able to cross the arena quickly, but not so quickly that mice are trivial.
- Pounce should be used for:
  - Crossing distance.
  - Catching Big mice.
  - Multi-catch opportunities.
  - Getting into position to block a hole.

### 27.2 Mouse Feel

Mice should feel like prey.

Key feelings:

- They should panic when the cat is close.
- They should not be perfectly predictable.
- They should give the player a fair chance to react.
- They should not feel like they are cheating.
- They should not get permanently stuck.

### 27.3 Fairness Rules

- Mice cannot enter a hole while the cat is blocking it.
- Mice cannot enter a hole that is occupied.
- Mice cannot escape instantly after spawning.
- Mice are not catchable while emerging.
- Mice can still be caught while entering a hole.
- The player can always see all active mice.
- No mouse can become invisible or uncatchable except Big mice, which are clearly special.

**Why:**  
The game should never feel like the player was cheated by an invisible or impossible escape.

---

## 28. Edge Cases

The game must handle these cases.

### 28.1 Player Pauses

- All timers stop.
- No spawning.
- No mouse movement.
- No score changes.
- No life changes.

### 28.2 Browser Loses Focus

- Automatically pause the game.

### 28.3 Pounce Pressed During Cooldown

- Buffer the input for 0.1 seconds.
- Execute pounce when cooldown is ready if the buffer is still active.

### 28.4 Pounce With No Movement Input

- Use last movement direction.
- If no movement direction exists yet, pounce to the right.

### 28.5 Cat Blocks All Spawn Holes

- Spawning waits until at least one hole is available.
- Spawn timer continues counting down.

### 28.6 Mouse Cannot Find Available Hole

- Mouse continues fleeing/wandering.
- It does not escape until a hole becomes available.

### 28.7 Multiple Mice Caught Same Frame

- Each mouse is caught.
- Each mouse adds its own score.
- Combo increases for each mouse.
- One multi-catch bonus is added.

### 28.8 Multiple Mice Escape Same Frame

- Each mouse reduces lives by 1.
- If lives become 0 or below, trigger game over.

### 28.9 Target Reached Same Frame as Lives Reach 0

- Process catches before escapes.
- If the target is reached, level complete wins.
- The player should not be penalized for an escape that happens in the same frame as the final catch.

### 28.10 Mouse Caught While Entering Hole

- The mouse is caught.
- It does not escape.
- The hole remains occupied for its normal 0.8 seconds.

### 28.11 Big Mouse Touched While Not Pouncing

- No catch.
- Mouse becomes startled.
- Mouse cannot seek holes while startled.

### 28.12 Mouse Stuck Against Obstacle

- Obstacle avoidance should rotate the mouse’s desired direction.
- If the mouse’s speed is near zero for 1.0 second, force a new random wander direction.

### 28.13 Player Leaves Mid-Level

- No special save is required.
- High score can be saved at level complete, campaign complete, endless wave complete, or game over.

### 28.14 Retry After Failure

- Restart the same level or wave.
- Reset lives to 3.
- Reset score to the score at the start of that level or wave.

---

## 29. Save Data

Save only the minimum required data.

Required save data:

```text
endless_unlocked: boolean
campaign_high_score: integer
endless_high_score: integer
endless_best_wave: integer
```

Optional but useful:

```text
total_plays: integer
```

Do not save mid-level progress.

**Why:**  
This is a short arcade game. Saving full campaign progress is unnecessary and complicates the state system.

---

## 30. Performance Constraints

The game should run smoothly in a browser.

Constraints:

- Maximum active mice: 7 in Endless Mode.
- Maximum holes per level: 6.
- Maximum obstacles per level: 3.
- No full pathfinding.
- No physics engine required.
- Use fixed or clamped delta time.
- Recommended max delta time: **1/30 second**.

**Why:**  
These constraints keep the game simple and fast enough for browser performance.

---

## 31. Cut Features

The following features are intentionally not included.

- No player upgrades.
- No cat health.
- No mouse health.
- No level select.
- No timer-based failure.
- No camera scrolling.
- No 3D movement.
- No mouse aiming.
- No stamina system.
- No shop.
- No cosmetic unlocks.
- No boss mice.
- No destructible obstacles.
- No persistent mid-level save.

**Why:**  
Each cut feature would add UI, AI, or state complexity without improving the core chase. The game is stronger when the player only has to understand: move, pounce, catch mice, stop them from hiding.

---

## 32. Final Game Flow Summary

1. Player opens Main Menu.
2. Player presses Play.
3. Level 1 intro appears.
4. Gameplay begins.
5. Mice spawn from holes.
6. Player catches mice.
7. If player catches enough mice, Level Complete appears.
8. Next level starts.
9. This continues through Level 10.
10. Campaign Complete appears.
11. Endless Mode unlocks.
12. Player can play Endless Mode.
13. Endless waves increase in difficulty.
14. If the player fails, they can retry the current level or wave.