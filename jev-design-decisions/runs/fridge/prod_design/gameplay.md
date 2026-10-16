# gameplay.md

## 1. Design Summary

**Game concept:** The player is a refrigerator that has just become sentient. The fridge must escape the house before the movers arrive.

**Core fantasy:**  
You are heavy, awkward, and vulnerable. You do not fight. You observe, wait, move quietly, use the house’s power, and slip past the people who own you.

**Core loop:**  
1. Unplug yourself.  
2. Move through the house.  
3. Avoid being seen or heard.  
4. Recharge at outlets when safe.  
5. Reach the front door before the timer ends.

**Win condition:**  
The fridge reaches the front door threshold before the 120-second escape timer ends.

**Lose conditions:**  
- A resident catches the fridge.  
- The fridge’s power reaches 0.  
- The 120-second timer reaches 0.

**Why this design is the right one:**  
A fridge is not a combat character. It is large, slow, and normally stationary. Stealth and timing fit the fantasy better than action. A single continuous house level gives a clean end-to-end experience without loading screens or level-select complexity. The timer prevents the player from stalling in a safe state, which is necessary because a plugged-in fridge in the kitchen could otherwise be safe indefinitely.

---

## 2. Dimensionality

**Chosen dimensionality: 2D top-down.**

The gameplay is fully 2D top-down. The visual designer may add 2.5D shadows or height, but no gameplay mechanic depends on depth, jumping, or 3D line of sight.

**Why top-down 2D:**
- House navigation is clearest from above.
- Doorway fitting and rotation are easier to understand.
- Resident line of sight and noise propagation are easier to read.
- It is more browser-friendly than 3D.
- It avoids the problem of side-view rooms hiding important layout information.

**Cut by design:**
- No 3D movement.
- No jumping.
- No depth-based hiding.
- No camera rotation.

---

## 3. Space and Layout

The game is one continuous level: a single house.

**Logical playfield size:**  
1280 x 720 units.

The playfield is divided into three main rooms from left to right:

| Room | X Range | Purpose |
|---|---:|---|
| Kitchen | 0 to 480 | Start area, tutorial, first resident |
| Hallway | 480 to 800 | Middle pressure, recharge, noise management |
| Living Room | 800 to 1280 | Final approach to front door |

**Openings:**

| Opening | Location | Size |
|---|---|---:|
| Kitchen to Hallway | x = 480, y = 320 to 400 | 80 units tall |
| Hallway to Living Room | x = 800, y = 320 to 400 | 80 units tall |
| Front Door | x = 1280, y = 320 to 400 | 80 units tall |

The front door is the win zone. The fridge wins when its center enters the front door threshold:
- x >= 1240
- y between 320 and 400

**Why one continuous level:**  
The escape is a single journey through a house. Splitting it into separate levels would break the tension and make the escape feel artificial. One level allows smooth progression from tutorial to final pressure.

---

## 4. Map Content

### 4.1 Kitchen

The kitchen is the starting room.

**Fridge start position:**
- x: 180
- y: 500
- angle: 0 degrees, facing right
- plugged in
- power: 100

**Kitchen outlet:**
- x: 120
- y: 500
- non-blocking
- recharge point

**Kitchen obstacles:**

| Object | Rectangular Bounds | Blocks Movement | Blocks Line of Sight |
|---|---|---|---|
| Top counter | x 20 to 460, y 20 to 80 | Yes | Yes |
| Left counter | x 20 to 80, y 100 to 420 | Yes | Yes |
| Sink | x 200 to 280, y 100 to 180 | Yes | Yes |
| Stove | x 360 to 440, y 100 to 180 | Yes | Yes |

**Kitchen resident: Mom**

Mom appears at 5 seconds.

Waypoint loop:
1. x 140, y 140
2. x 300, y 140
3. x 300, y 620
4. x 140, y 620

Mom loops through the kitchen. Her route is designed to force the player to time movement, but she does not pass within 40 units of the fridge start position.

---

### 4.2 Hallway

The hallway is the middle room. It is narrow enough to feel constrained but wide enough for the fridge to rotate.

**Hallway outlet:**
- x: 640
- y: 360
- non-blocking
- recharge point

**Hallway obstacles:**

| Object | Rectangular Bounds | Blocks Movement | Blocks Line of Sight |
|---|---|---|---|
| Potted plant | x 600 to 660, y 120 to 180 | Yes | Yes |
| Shoe rack | x 600 to 660, y 540 to 600 | Yes | Yes |

**Hallway resident: Dad**

Dad appears at 10 seconds.

Waypoint loop:
1. x 1000, y 200
2. x 640, y 200
3. x 640, y 500
4. x 1000, y 500

Dad crosses between the living room and hallway. His route creates repeated pressure in the middle room.

---

### 4.3 Living Room

The living room contains the front door.

**Living room outlet:**
- x: 900
- y: 600
- non-blocking
- recharge point

**Living room obstacles:**

| Object | Rectangular Bounds | Blocks Movement | Blocks Line of Sight |
|---|---|---|---|
| Sofa | x 900 to 1120, y 80 to 160 | Yes | Yes |
| Coffee table | x 1000 to 1100, y 300 to 380 | Yes | Yes |
| TV stand | x 1200 to 1260, y 80 to 200 | Yes | Yes |
| Bookshelf | x 1200 to 1260, y 520 to 640 | Yes | Yes |

The coffee table blocks the direct path to the front door. The player must go around it either above or below.

**Living room resident: Kid**

Kid appears at 20 seconds.

Waypoint loop:
1. x 1050, y 240
2. x 1160, y 360
3. x 1050, y 480
4. x 940, y 360

Kid moves around the coffee table and creates final pressure near the front door.

---

## 5. Game States

The game has five states:

1. **Start**
2. **Playing**
3. **Paused**
4. **Win**
5. **Lose**

### 5.1 Start State

Display:
- Title: “Fridge Escape”
- Subtitle: “You are awake. Leave before the movers arrive.”
- Play button
- Controls list

The game does not update the world until Play is pressed.

### 5.2 Playing State

All systems update.

The escape timer starts when the game enters Playing.

### 5.3 Paused State

Pause is triggered by Escape.

While paused:
- Timer stops.
- Residents stop.
- Fridge stops.
- Noise events stop.
- An overlay displays:
  - Resume
  - Restart

If the browser tab becomes hidden, the game automatically pauses.

### 5.4 Win State

Triggered when the fridge center enters the front door threshold.

Display:
- “You escaped.”
- Time used
- Number of noise events created
- Number of residents lured
- Play Again button

### 5.5 Lose State

Lose reasons:
- “You got unplugged.”
- “Your hum faded.”
- “The movers arrived.”

Display:
- Lose reason
- Retry button

**Lose priority order:**
1. Win
2. Caught by resident
3. Power depleted
4. Timer expired

This order matters for edge cases. If the fridge reaches the door at the same moment as another condition, the player wins.

---

## 6. Player Systems

The player controls the fridge.

### 6.1 Controls

| Input | Action |
|---|---|
| W or Up | Waddle forward |
| S or Down | Waddle backward |
| A or Left | Turn left |
| D or Right | Turn right |
| Space | Slide |
| E | Open or close fridge door |
| Q | Hum |
| P | Plug in or unplug |
| Escape | Pause |

**Why keyboard only:**  
This is a browser game with precise timing. Keyboard input is the clearest input model. Touch support can be added later, but it is not required for the core design.

---

## 7. Fridge Movement

The fridge is a rotated rectangle.

**Collider:**
- Length: 64 units
- Width: 32 units
- Rotates around its center.

The fridge cannot overlap walls, counters, furniture, or other blocked tiles.

### 7.1 Waddling

Waddling is the default movement.

| Property | Value |
|---|---:|
| Max waddle speed | 50 units/sec |
| Acceleration | 120 units/sec² |
| Deceleration | 180 units/sec² |

The fridge can waddle forward and backward relative to its facing direction.

**Why waddling is slow:**  
The fridge should feel heavy. Waddling is safe but not fast enough to outrun a resident.

---

### 7.2 Rotation

| Property | Value |
|---|---:|
| Rotation speed | 100 degrees/sec |

The fridge turns slowly.

**Why rotation is slow:**  
Fitting through doorways should be deliberate. The player must plan orientation before entering tight spaces.

---

### 7.3 Sliding

Sliding is a short burst of speed.

| Property | Value |
|---|---:|
| Slide speed | 150 units/sec |
| Slide duration | 0.25 seconds |
| Slide cooldown | 0.6 seconds |
| Slide power cost | 10 power |
| Slide noise | Loud |

The fridge slides in the direction it is facing.

The player can slide only if:
- Power is at least 10.
- Slide cooldown has finished.
- The fridge is unplugged.

**Why sliding exists:**  
Sliding gives the player an escape tool. It is faster than residents, but it is noisy. This creates the core risk/reward: speed versus detection.

---

## 8. Plug and Power System

The fridge is powered by the house’s electricity.

**Power range:**
- 0 to 100
- Starts at 100

### 8.1 Plugged State

When plugged:
- The fridge cannot move.
- The fridge cannot rotate.
- The fridge cannot slide.
- Power recharges at 15 power/sec.
- Passive power drain is 0.
- The door can still be opened or closed.
- Hum can still be used if power is available.

### 8.2 Unplugged State

When unplugged:
- The fridge can move.
- Power drains.
- The fridge can plug into an outlet.

### 8.3 Power Drain

Power drains only while unplugged.

| Condition | Drain |
|---|---:|
| Passive, unplugged | 1 power/sec |
| Waddling, speed > 1 unit/sec | +3 power/sec |
| Rotating | +1.5 power/sec |
| Door open | +0.5 power/sec |
| Sliding | 10 power instant cost |
| Hum | 15 power instant cost |

**Why power drains only while unplugged:**  
This makes plugging in a meaningful safe state. The player can recharge, but while plugged they are stationary and vulnerable.

---

### 8.4 Plugging and Unplugging

The fridge can plug into any outlet.

**Outlet radius:**
- 48 units

**Plug action:**
- If unplugged and within 48 units of an outlet, pressing P starts a 0.5-second connection.
- If the player moves, rotates, slides, or unplugs during connection, the plug attempt fails.
- If connection succeeds, the fridge becomes plugged.

**Unplug action:**
- If plugged, pressing P immediately unplugs the fridge.

**Noise:**
- Plug connection emits a small noise.
- Unplugging emits a medium noise.

**Why plug/unplug is a player action:**  
It makes power management active rather than automatic. The player must decide when to stop and recharge.

---

## 9. Door and Hum System

The fridge has a door.

### 9.1 Door State

The door can be:
- Closed
- Open

Pressing E toggles the door.

**Gameplay effects of door open:**
- The fridge can hum.
- If unplugged, power drains at +0.5/sec.
- Residents are more suspicious of the fridge.

**Why the door matters:**  
The door is the fridge’s identity. It is also the source of its “voice.” Opening the door makes the fridge more noticeable, but it enables the hum action.

---

### 9.2 Hum

Hum is a loud noise event used to lure residents.

| Property | Value |
|---|---:|
| Power cost | 15 |
| Cooldown | 3 seconds |
| Noise radius | 160 |
| Noise alert value | 100 |
| Requirement | Door must be open |

The hum occurs at the fridge’s current position.

Residents who hear the hum investigate the hum location, not necessarily the fridge’s current location after it moves.

**Why hum exists:**  
Hum gives the player an active stealth tool. The player can create a decoy by humming, then move away. This is important because the player cannot fight or hide indefinitely.

---

## 10. Noise System

Noise is event-based. Noise does not persist over time. When an action creates noise, it immediately checks whether residents hear it.

### 10.1 Noise Events

| Source | Radius | Alert Value | Notes |
|---|---:|---:|---|
| Waddle step | 12 | 15 | Emits every 0.6 seconds while speed > 10 |
| Slide | 50 | 45 | Emits at slide start and every 0.2 seconds while sliding |
| Collision | 25 | 30 | Emits if impact speed > 30 |
| Plug connection | 10 | 10 | Emits when plug starts |
| Unplug | 20 | 25 | Emits when unplugging |
| Door toggle | 15 | 15 | Emits when door opens or closes |
| Hum | 160 | 100 | Emits at fridge position |

### 10.2 Room Modifier

Noise is reduced across room boundaries.

| Relationship | Radius Modifier |
|---|---:|
| Same room | 1.0 |
| Adjacent room | 0.5 |
| Non-adjacent room | 0.0 |

Room adjacency:
- Kitchen is adjacent to Hallway.
- Hallway is adjacent to Living Room.
- Kitchen is not adjacent to Living Room.

**Why room modifiers exist:**  
They make the house feel like a real house. A loud slide in the kitchen should not instantly wake someone in the living room, but a hum should travel farther.

---

### 10.3 Hearing Algorithm

When a noise event is emitted:

For each resident:
1. Determine the resident’s room.
2. Determine the noise source room.
3. Apply room modifier to noise radius.
4. If distance from resident to noise source is less than or equal to modified radius, the resident hears the noise.
5. Set the resident’s `lastKnownPosition` to the noise source.
6. Set the resident’s suspicion to at least the noise alert value.
7. If alert value is 50 or higher, set the resident state to Investigate and set their target to the noise source.

**Why alert values matter:**  
Small noises make residents suspicious. Large noises make them investigate. This gives different actions different levels of danger.

---

## 11. Resident Systems

Residents are the main threat.

There are three residents:
- Mom
- Dad
- Kid

All residents use the same perception and AI rules.

### 11.1 Resident Collider

Residents are circles.

| Property | Value |
|---|---:|
| Radius | 20 units |

Residents do not block line of sight.

---

### 11.2 Resident Movement Speeds

| State | Speed |
|---|---:|
| Routine | 70 units/sec |
| Investigate | 110 units/sec |

**Why residents are faster than waddling:**  
The player cannot safely outrun residents by waddling. The player must hide, wait, or use slide.

**Why slide is faster than residents:**  
Slide gives a short escape window, but it is noisy and limited by cooldown and power.

---

### 11.3 Resident Spawn Times

| Resident | Spawn Time |
|---|---:|
| Mom | 5 seconds |
| Dad | 10 seconds |
| Kid | 20 seconds |

The first 5 seconds are safe. This gives the player time to learn the basic controls before the first resident appears.

**Why staggered spawns:**  
It creates a smooth difficulty ramp. The player learns movement in the kitchen, then faces hallway pressure, then faces the final living room challenge.

---

## 12. Resident Perception

Residents can detect the fridge by sight and sound.

### 12.1 Sight

Each resident has a view cone.

| Property | Value |
|---|---:|
| View radius | 160 units |
| Field of view | 120 degrees |

A resident can see the fridge if:
- The fridge is within view radius.
- The fridge is inside the resident’s field of view.
- Line of sight is not blocked by walls or furniture.

**Line of sight algorithm:**
- Cast a line from the resident’s center to the fridge’s center.
- Sample every 8 units.
- If any sample intersects a blocking tile, line of sight is blocked.

**Why line of sight matters:**  
The player must use furniture as cover. Without line-of-sight blocking, stealth would be too simple.

---

### 12.2 Anomaly Detection

A resident only becomes suspicious if the fridge looks abnormal.

The fridge is considered abnormal if any of the following are true:
- The fridge is unplugged.
- The fridge is moving, speed > 5 units/sec.
- The fridge door is open.
- The fridge is not in the kitchen.
- The fridge is within 80 units of the resident.

If the fridge is plugged, stationary, in the kitchen, and its door is closed, residents do not gain suspicion from seeing it.

**Why anomaly detection exists:**  
A fridge in the kitchen is normal. A fridge in the hallway is not. This makes the kitchen a starting safe zone but not a permanent safe zone once the player unplugs or moves.

---

### 12.3 Suspicion

Each resident has a suspicion value from 0 to 100.

When a resident sees an abnormal fridge:

Base suspicion rate:
- 20 suspicion/sec

Add modifiers:

| Condition | Suspicion Rate Added |
|---|---:|
| Fridge is moving | +20/sec |
| Fridge is unplugged | +20/sec |
| Fridge door is open | +10/sec |
| Fridge is not in kitchen | +10/sec |
| Fridge is within 80 units | +20/sec |

Example:
- If a resident sees an unplugged, moving fridge in the hallway, suspicion rises at 70/sec.
- If a resident sees a stationary plugged fridge in the hallway, suspicion rises at 30/sec.

When the resident no longer sees an abnormal fridge:
- Suspicion decays at 25 suspicion/sec.
- If suspicion reaches 0, the resident returns to Routine if it was only Suspicious.

**Why suspicion is gradual:**  
Instant detection would feel unfair. Gradual suspicion gives the player a chance to react, hide, or move.

---

## 13. Resident AI States

Each resident has one of four states:

1. Routine
2. Suspicious
3. Investigate
4. Search

### 13.1 Routine

The resident follows its waypoint loop.

- Moves at routine speed.
- Faces movement direction.
- Dwell time at each waypoint: 0.5 to 2 seconds, randomly chosen.
- If suspicion becomes greater than 0, the resident becomes Suspicious.

### 13.2 Suspicious

The resident stops and faces the fridge.

- Does not move.
- Accumulates suspicion if it continues to see an abnormal fridge.
- If suspicion reaches 100, becomes Investigate.
- If no abnormal detection occurs for 1.5 seconds, suspicion decays and the resident returns to Routine.

**Why Suspicious exists:**  
It gives the player a visible warning. The player can see that a resident has noticed something and can react before full investigation.

---

### 13.3 Investigate

The resident moves to the last known suspicious position.

- Moves at investigate speed.
- Uses pathfinding.
- If the resident sees the fridge while investigating, it updates its target to the fridge’s current position and sets suspicion to 100.
- If the resident reaches the target and does not see the fridge, it enters Search.

### 13.4 Search

The resident waits at the target and scans.

- Search duration: 3 seconds.
- After searching, the resident returns to Routine.

**Why Search exists:**  
It prevents residents from chasing forever. It also gives the player a chance to slip away after being heard.

---

## 14. Resident Pathfinding

Residents use A* pathfinding.

**Grid:**
- Tile size: 32 units
- Grid covers the 1280 x 720 playfield.
- Walkable tiles: floor and doorways.
- Blocked tiles: walls, counters, furniture, and other non-walkable objects.

The fridge is treated as a temporary obstacle for resident pathfinding. Approximate the fridge as a 3x2 tile obstacle.

**Path recalculation:**
- Every 0.5 seconds.
- Immediately when the resident’s target changes.
- If no path exists, the resident stops and faces its last known target.

**Why pathfinding is needed:**  
Residents must navigate around furniture and doorways. Without pathfinding, they would either move unnaturally or get stuck.

---

## 15. Catch Condition

A resident catches the fridge if:
- The resident’s center is within 40 units of the fridge’s center.

When caught:
- The game enters Lose state.
- Lose reason: “You got unplugged.”

**Why catch is distance-based:**  
It is simple and readable. The player knows not to let residents touch the fridge.

Residents path around the fridge, so catching usually happens when:
- The player moves into a resident.
- A resident investigates the player’s position.
- A resident searches near the player.

---

## 16. Escape Timer

The player has 120 seconds to escape.

The timer:
- Starts when the game enters Playing.
- Stops while paused.
- Reaches 0 only in Playing state.

If the timer reaches 0:
- The game enters Lose state.
- Lose reason: “The movers arrived.”

**Why a timer is required:**  
Without a timer, the player could remain plugged in the kitchen indefinitely. The timer gives the game a hard end condition and creates constant pressure.

**Why 120 seconds:**  
It is long enough for a first-time player to learn and recover from mistakes, but short enough to create tension. A careful run should take roughly 60 to 90 seconds.

---

## 17. Progression Through the Game

The game progresses spatially and temporally.

### 17.1 Act 1: Kitchen

**Goal:** Leave the kitchen.

The player learns:
- Unplugging.
- Waddling.
- Turning.
- Basic noise.
- First resident pressure from Mom.

The kitchen is the safest room, but it is not safe forever because the timer exists and unplugging creates noise.

---

### 17.2 Act 2: Hallway

**Goal:** Cross the hallway.

The player learns:
- Recharging at outlets.
- Using hum to create decoys.
- Managing Dad’s crossing route.
- Deciding when to slide versus waddle.

The hallway is the most constrained space. It is where the player feels the core tension of the game.

---

### 17.3 Act 3: Living Room

**Goal:** Reach the front door.

The player combines all systems:
- Avoid Kid.
- Use cover around the coffee table.
- Manage power.
- Decide when to take final risk.

The living room is the final pressure zone. The front door is visible but not easy to reach safely.

---

### 17.4 Objective Text Progression

The HUD objective updates based on the fridge’s room.

| Condition | Objective Text |
|---|---|
| Fridge is plugged at start | “Unplug and leave.” |
| Fridge is in kitchen | “Leave the kitchen.” |
| Fridge is in hallway | “Cross the hallway.” |
| Fridge is in living room | “Reach the front door.” |

**Why objective text updates:**  
It gives the player clear progress without a map.

---

## 18. Feel and Tuning

The game should feel heavy, tense, and deliberate.

### 18.1 Movement Feel

| Feeling | How It Is Achieved |
|---|---|
| Heavy | Low waddle speed, slow acceleration, slow rotation |
| Vulnerable | Residents are faster than waddling |
| Bursty | Slide is fast but short and loud |
| Deliberate | Doorways require rotation and spacing |
| Urgent | 120-second timer |
| Resourceful | Power and hum create choices |

### 18.2 Risk/Reward Table

| Action | Benefit | Risk |
|---|---|---|
| Waddle | Quiet, controllable | Slow, drains power |
| Slide | Fast escape | Loud, uses power, has cooldown |
| Plug in | Recharges power | Stationary, vulnerable |
| Unplug | Allows movement | Noisy, starts power drain |
| Open door | Enables hum | More suspicious |
| Hum | Lures residents | Very loud, uses power, reveals location |

### 18.3 Tension Curve

| Time | Pressure |
|---|---|
| 0 to 5 seconds | Safe, tutorial |
| 5 to 20 seconds | Mom appears, kitchen pressure |
| 20 to 45 seconds | Dad appears, hallway pressure |
| 45 to 75 seconds | Kid appears, living room pressure |
| 75 to 120 seconds | Timer pressure, final approach |

The exact timing depends on player behavior, but the design intent is that pressure increases as the player approaches the front door.

---

## 19. HUD and Display

The HUD must communicate:
- Objective.
- Time remaining.
- Power.
- Plug state.
- Door state.
- Resident awareness.
- Contextual prompts.

### 19.1 HUD Layout

| HUD Section | Content |
|---|---|
| Top-left | Objective text |
| Top-center | Escape timer |
| Top-right | Power bar, plug icon, door icon |
| Bottom-left | Contextual prompt |
| Bottom-right | Optional controls reminder |

### 19.2 HUD Elements

#### Objective Text
Shows the current goal.

Examples:
- “Unplug and leave.”
- “Leave the kitchen.”
- “Cross the hallway.”
- “Reach the front door.”

#### Escape Timer
Displays seconds remaining.

Warning state:
- When timer is below 30 seconds, the timer flashes red.

#### Power Bar
Displays 0 to 100 power.

Warning state:
- When power is below 25, the power bar flashes red.

#### Plug Icon
Shows whether the fridge is plugged or unplugged.

#### Door Icon
Shows whether the door is open or closed.

#### Contextual Prompt
Shows one relevant instruction at a time.

Examples:
- “Press P to unplug.”
- “Press P to plug in and recharge.”
- “Press E to open your door.”
- “Press Q to hum.”
- “Press Space to slide. It is loud.”

---

## 20. World Indicators

These are not HUD bars, but they must be displayed in the world.

### 20.1 Resident Awareness

Above each resident:

| Suspicion State | Display |
|---|---|
| 0 | No icon |
| 1 to 99 | Eye icon, opacity equals suspicion / 100 |
| 100 | Exclamation icon |

**Why this is needed:**  
The player needs to know when a resident is noticing them before full investigation.

---

### 20.2 Noise Rings

When a noise event occurs, display a brief expanding ring at the source.

- Ring size is proportional to noise radius.
- Ring fades quickly.
- Hum rings should be visibly larger than other noise rings.

**Why noise rings are needed:**  
They make noise propagation readable. The player can understand what was heard by whom.

---

### 20.3 Warning Vignette

When any resident has suspicion above 50:
- Show a red screen-edge vignette.
- Vignette intensity equals the highest resident suspicion divided by 100.

When any resident reaches 100:
- Vignette becomes strong.

**Why vignette is needed:**  
It gives an emotional warning without requiring the player to look at every resident icon.

---

## 21. Content by Section

### 21.1 Start Screen

Content:
- Title: “Fridge Escape”
- Subtitle: “You are awake. Leave before the movers arrive.”
- Play button
- Controls list

Purpose:
- Establish premise.
- Explain controls.
- Start the game.

---

### 21.2 Tutorial Prompts

Tutorial prompts appear contextually and do not block input.

Prompt sequence:

1. “You are awake. You need to leave.”
2. “Press P to unplug.”
3. “W/S: waddle. A/D: turn.”
4. “Space: slide. Fast, but loud.”
5. “E: open/close door. Q: hum. Hum lures residents.”
6. “Reach the front door before time runs out.”

**Why contextual prompts:**  
They teach only when relevant and avoid overwhelming the player.

---

### 21.3 Kitchen Section

Content:
- Fridge start position.
- Kitchen outlet.
- Counters, sink, stove.
- Mom resident.
- Doorway to hallway.

Purpose:
- Teach movement.
- Teach plug/unplug.
- Introduce first resident.
- Give the player a safe starting space.

---

### 21.4 Hallway Section

Content:
- Hallway outlet.
- Potted plant.
- Shoe rack.
- Dad resident.
- Doorways to kitchen and living room.

Purpose:
- Teach recharge.
- Teach hum as a decoy.
- Create middle-game pressure.

---

### 21.5 Living Room Section

Content:
- Living room outlet.
- Sofa.
- Coffee table.
- TV stand.
- Bookshelf.
- Kid resident.
- Front door.

Purpose:
- Final approach.
- Combine all systems.
- Create final tension before win.

---

### 21.6 Win Screen

Content:
- “You escaped.”
- Time used.
- Noise events created.
- Residents lured.
- Play Again button.

**Why stats exist:**  
They give a small sense of mastery without adding a full scoring system.

---

### 21.7 Lose Screen

Content depends on lose reason.

| Lose Reason | Text |
|---|---|
| Caught | “You got unplugged.” |
| Power depleted | “Your hum faded.” |
| Timer expired | “The movers arrived.” |

Also display:
- Retry button.

**Why lose reasons matter:**  
They tell the player what went wrong and what to fix.

---

## 22. Edge Cases and All Cases

The implementation must handle these cases.

### 22.1 Pause and Hidden Tab

- Escape pauses the game.
- Hiding the browser tab pauses the game.
- While paused, no timer, movement, AI, or noise updates occur.

---

### 22.2 Insufficient Power

If the player tries to slide with less than 10 power:
- Slide does not occur.
- Power bar flashes.

If the player tries to hum with less than 15 power:
- Hum does not occur.
- Power bar flashes.

---

### 22.3 Plug Not Available

If the player presses P while unplugged but not within 48 units of an outlet:
- Nothing happens.
- If a contextual prompt is active, it can show “No outlet nearby.”

If the player presses P while plugged:
- The fridge unplugs immediately.

---

### 22.4 Interrupted Plug

If the player starts plugging in but moves, rotates, slides, or unplugs during the 0.5-second connection:
- Plug attempt fails.
- The fridge remains unplugged.

---

### 22.5 Multiple Residents

- All residents update independently.
- The first catch condition triggers lose.
- The highest suspicion value drives the warning vignette.
- Noise events affect all residents within modified radius.

---

### 22.6 No Path

If a resident cannot path to its target:
- It stops.
- It faces its last known target.
- It does not catch the fridge unless within 40 units.

---

### 22.7 Resident Blocked by Fridge

The fridge is a temporary obstacle for resident pathfinding.

If the fridge blocks a resident’s path:
- The resident waits.
- The player can use this as a temporary safe spot, but if the resident is within 40 units, the player loses.

---

### 22.8 Win and Lose Same Frame

Priority:
1. Win
2. Caught
3. Power depleted
4. Timer expired

If the fridge reaches the front door at the same time as another lose condition, the player wins.

---

### 22.9 Timer and Power at Zero

If power reaches 0 before the timer:
- Lose by power.

If the timer reaches 0 before power:
- Lose by timer.

If both happen in the same frame:
- Power loss takes priority over timer loss, unless the fridge is also winning, in which case win takes priority.

---

### 22.10 Hum Cooldown

If the player presses Q while hum cooldown is active:
- Nothing happens.

If the player presses Q with door closed:
- Nothing happens.
- A contextual prompt can show “Open your door to hum.”

---

### 22.11 Slide Cooldown

If the player presses Space while slide cooldown is active:
- Nothing happens.

---

### 22.12 Collision

If the fridge collides with a wall or object:
- Movement stops.
- If impact speed is greater than 30 units/sec, emit collision noise.

---

### 22.13 Delta Time

Clamp delta time to 0.1 seconds maximum.

**Why:**  
Prevents tunneling and unfair jumps if the browser tab lags.

---

## 23. Cut by Design

These are intentionally not included.

| Cut Piece | Why It Was Cut |
|---|---|
| Combat | A fridge should not fight. Stealth fits the fantasy. |
| Inventory | Would complicate controls and distract from movement stealth. |
| Multiple levels | One house is enough for a complete escape. |
| Locked interior doors | Would add puzzle complexity without improving core feel. |
| Food thawing | Interesting, but would add another timer and distract from power/noise. |
| Save system | The game is short. Restart is simpler. |
| Difficulty options | One tuned experience is better for scope. |
| Mouse aiming | Keyboard movement is clearer for a top-down stealth game. |
| Pets or extra characters | Would add AI complexity without enough gameplay value. |
| Multiple players | Would break the lonely, vulnerable fantasy. |

---

## 24. Audio Hooks

The visual/audio agent will create the actual sounds. The gameplay systems require these audio hooks:

- Waddle loop
- Slide burst
- Plug connection
- Unplug
- Door open
- Door close
- Hum
- Resident suspicion
- Resident investigate
- Timer warning
- Power warning
- Win jingle
- Lose sting

**Why audio hooks are listed:**  
Several systems depend on the player understanding noise and awareness. The actual sound design is not part of gameplay, but the hooks must exist.

---

## 25. Final Design Intent

The player should feel like a heavy, anxious appliance trying to leave a house. The game is not about being fast. It is about being patient, observing people, using power, and making one final move.

The player succeeds by:
- Moving quietly.
- Recharging when safe.
- Using hum to create space.
- Reading resident routines.
- Reaching the front door before the timer ends.