# visual.md

## 1. Visual Identity

**Working title:** Cat: Mice Hunt  
**Visual style:** Warm Paper Arcade / soft vector top-down.

The game should look like a bright, playful, slightly frantic domestic arcade scene. The cat is the hero: confident, rounded, and readable. The mice are small, nervous, and easy to track. The arena should feel cozy but clear enough for fast top-down chase gameplay.

### Core Visual Principles

1. **Readable first.**  
   The player must always know where the cat, mice, holes, and pounce cooldown are.

2. **Cozy but urgent.**  
   The palette is warm and soft, but gameplay feedback is snappy, bright, and immediate.

3. **2.5D presentation only.**  
   Use shadows, raised obstacles, and recessed holes for depth. Depth must never affect gameplay.

4. **Distinct levels, one game.**  
   Each level changes floor, wall tone, and obstacle props, but all levels share the same palette logic, entity colors, UI, and animation language.

5. **No visual clutter.**  
   Backgrounds are low-contrast. Entities are high-contrast. Effects are short and localized.

**Why:**  
A browser top-down arcade game needs instant readability at 960 x 540. A soft vector style is cheap to render, easy to keep consistent, and fits the playful cat-and-mouse fantasy without becoming childish or noisy.

---

## 2. Canvas, Safe Areas, and Layout

Game canvas:

```text
960 x 540
```

There is no camera scrolling.

### HUD Safe Areas

| Area | Region | Purpose |
|---|---:|---|
| Top HUD | `y = 0` to `y = 68` | Score, combo, level/wave, progress, lives, pause |
| Bottom HUD | `y = 504` to `y = 540` | Pounce cooldown |
| Center message | centered at `x = 480`, `y = 210` | Temporary gameplay messages |
| Overlay panels | centered | Menus, level complete, game over, pause |

Entities may enter HUD safe areas. HUD elements must remain sparse and readable, but they should not become large panels during active gameplay.

**Why:**  
The arena is small. Large HUD panels would hide mice and holes. A thin, sparse HUD keeps the player focused on the chase.

---

## 3. Color Palette

Use the following core palette throughout the game.

### Core UI and Text

| Role | Hex | Usage |
|---|---|---|
| Dark text | `#2F2A25` | Primary text, labels, HUD text |
| Cream panel | `#FFF8EC` | Buttons, panels, UI surfaces |
| Panel border | `#E8DCC8` | Panel and button borders |
| UI accent | `#3FA3A3` | Progress fill, focus, positive UI accents |
| Gold | `#F2B84B` | Combo, score popups, pounce ready, success |
| Warning red | `#E2574C` | Escape, life loss, danger |
| Muted gray | `#9A938B` | Disabled text, secondary text |

### Entity Colors

| Entity | Hex | Notes |
|---|---|---|
| Cat body | `#F2A65A` | Orange tabby |
| Cat stripe | `#C96F2E` | Darker orange stripes |
| Cat belly | `#FFF1DC` | Light underside/belly |
| Cat nose | `#F28B82` | Small pink nose |
| Normal mouse | `#8A8F98` | Neutral gray |
| Fast mouse | `#6FA7C7` | Cool blue-gray |
| Big mouse | `#4F5560` | Dark slate, clearly larger |
| Mouse belly | `#D9DDE3` | Light underbelly |
| Hole dark | `#2A1F1A` | Hole interior |
| Hole rim | `#4A362B` | Hole edge |
| Hole highlight | `#F7D9A8` | Subtle rim highlight |

### Level Accent Rules

Level backgrounds may use different floor and wall colors, but entity colors stay constant.

**Why:**  
Constant entity colors make cat, mice, holes, and UI readable in every level. Level variation comes from the environment, not from changing the player’s or prey’s colors.

---

## 4. Typography

Use a rounded, friendly sans-serif font.

Recommended font stack:

```css
font-family: "Nunito", "Segoe UI", system-ui, sans-serif;
```

For score and numbers:

```css
font-family: "JetBrains Mono", "Courier New", monospace;
```

### Type Sizes

| Element | Size | Weight | Notes |
|---|---:|---:|---|
| Main menu title | 48px | Bold | Uppercase or title case |
| Overlay title | 28px | Bold | Uppercase optional |
| Center gameplay message | 32px | Bold | Short text only |
| Level intro level number | 36px | Bold | |
| Level intro objective | 20px | SemiBold | |
| HUD score | 18px | SemiBold | Monospace |
| HUD combo | 16px | Bold | Gold when active |
| HUD level/wave | 12px | SemiBold | Uppercase |
| Progress text | 14px | SemiBold | |
| Pounce label | 12px | SemiBold | Optional but recommended |
| Button text | 18px | SemiBold | |
| Small help text | 12px | Normal | |

### Text Readability

All gameplay text should use a soft cream shadow or outline:

```css
text-shadow: 0 1px 0 rgba(255, 248, 236, 0.7), 0 0 4px rgba(255, 248, 236, 0.45);
```

**Why:**  
The floor colors change by level. A consistent cream glow keeps dark text readable without using heavy boxes.

---

## 5. 2.5D Presentation

The game is top-down, but it should feel slightly physical.

### Shadows

- Cat and mice have soft elliptical shadows.
- Shadow offset: `2px` down and right.
- Shadow opacity: `0.22` to `0.28`.
- Shadows are non-interactive and do not affect collision.

### Pounce Lift

When the cat pounces:

- Cat body stretches in the pounce direction.
- Shadow stretches slightly in the pounce direction.
- Shadow opacity drops to about `0.16` for the first half of the pounce.
- On landing, the cat squashes slightly for `0.05s`.

### Obstacles

Obstacles are raised:

- Top surface is lighter.
- Bottom/right edge is darker.
- Side height: `4px`.
- Corner radius: `4px`.
- Shadow: `3px` offset, opacity `0.20`.

### Holes

Holes are recessed:

- Dark radial interior.
- Thin rim.
- Subtle inner shadow.
- No drop shadow.

**Why:**  
Small 2.5D cues make the arena feel like a real room without adding depth-based gameplay or visual noise.

---

## 6. Arena and Level Visual Themes

All levels use the same `960 x 540` arena. Do not change hole or obstacle positions based on this document. Only apply the visual theme.

The game should feel like moving through different areas of a cat’s home or home surroundings. Each level gets a distinct floor, wall tone, and obstacle prop style, but the overall look stays warm, clean, and coherent.

### Level Theme Table

| Level | Area | Floor Color | Wall Color | Accent Color | Obstacle Style | Mood |
|---:|---|---|---|---|---|---|
| 1 | Kitchen | `#F7E8D2` | `#5B3A29` | `#F2D08A` | None | Bright, open, tutorial |
| 2 | Dining Nook | `#E8C9A0` | `#5B3A29` | `#D98A6A` | Table / rug | Warm, domestic |
| 3 | Living Room | `#D8E8E4` | `#3E4A5A` | `#E7B84C` | Sofa / ottoman | Cozy, playful |
| 4 | Bedroom | `#E5EAF2` | `#4A4A5A` | `#E8A7B5` | Bed / chest | Soft, slightly calmer |
| 5 | Study | `#DDE8D4` | `#3E4A3E` | `#E7B84C` | Bookcase / desk | Neat, slightly busy |
| 6 | Laundry | `#F2F2E8` + checker `#D8E8E4` | `#3E4A5A` | `#6FA7C7` | Baskets / counter | Clean, patterned |
| 7 | Hallway | `#E8D0B0` | `#5B3A29` | `#E7B84C` | Cabinets / shelves | Narrow, directional |
| 8 | Attic | `#D8B890` | `#4A3525` | `#C98A5B` | Crates / barrels | Dusty, enclosed |
| 9 | Basement | `#D8D8D0` | `#3E4A5A` | `#6FA7C7` | Pipes / boxes | Cool, slightly tense |
| 10 | Patio at Dusk | `#E8D8C0` | `#3E4A5A` | `#B57A4C` | Planters / boxes | Final, higher pressure |

### Level Background Rules

- Floor patterns must be subtle.
- Pattern contrast should be no more than about `8%` to `12%` of the base floor color.
- No floor pattern should resemble a mouse, hole, or UI icon.
- Walls are an `8px` visual border inside the canvas.
- Walls do not change collision. The playable area remains the full `960 x 540`.
- Add a very soft vignette, opacity around `0.08`, to focus the center.

### Obstacle Style Notes

Obstacles are rectangles from the gameplay document. Visually, they should look like furniture or props, but their collision shape remains exactly the same.

| Level | Obstacle Visual |
|---:|---|
| 2 | Wooden table top or rug with subtle border |
| 3 | Rounded sofa cushion or ottoman |
| 4 | Bed edge or wooden chest |
| 5 | Bookcase or desk with low-contrast book spines |
| 6 | Woven basket or laundry counter |
| 7 | Cabinet or shelf with simple door lines |
| 8 | Wooden crate or barrel top |
| 9 | Concrete block or pipe cover |
| 10 | Stone planter or wooden box |

Keep prop details low-contrast. Details should not create false edges that look like holes or mice.

**Why:**  
Distinct level themes make the campaign feel like progression, while constant entity colors and UI keep the game coherent and readable.

---

## 7. Entity Visuals

## 7.1 Cat

The cat is the player character and should be the most readable object on screen.

### Cat Visual Size

- Gameplay radius: `18px`.
- Visual bounding size: about `40 x 40px`.
- Body should appear slightly larger than the collision radius because of shadow and tail.

### Cat Design

- Orange tabby cat.
- Rounded body.
- Two triangular ears.
- Curved tail.
- Four small paws visible from top-down.
- Simple face: two dark eyes, small pink nose.
- Darker orange stripes on back.

### Cat States

| State | Visual |
|---|---|
| Idle | Tail wags slowly, ears twitch occasionally |
| Moving | Paws bob, tail follows movement, body rotates toward movement direction |
| Pouncing | Body stretches `1.35x` in pounce direction, paws extend, tail straightens, speed lines appear |
| Landing | Brief squash `0.85x` vertically for `0.05s` |
| Catching | Brief happy face: eyes become curved lines for `0.12s` |
| Blocked hole | No special cat animation needed; hole shows blocked state |

### Cat Color Details

- Body: `#F2A65A`
- Stripes: `#C96F2E`
- Belly/face light: `#FFF1DC`
- Eyes: `#2B2B2B`
- Nose: `#F28B82`
- Outline: optional `1px` darker orange `#B85F22`, opacity `0.35`

**Why:**  
The cat needs to be instantly recognizable and trackable. A rounded orange cat with a tail gives clear direction and motion without needing complex sprites.

---

## 7.2 Mice

There are three mouse types. They must be distinguishable by color, size, shape, and animation.

### Mouse Visual Size

| Mouse Type | Gameplay Radius | Visual Size | Notes |
|---|---:|---:|---|
| Normal | `14px` | about `28 x 20px` | Standard prey |
| Fast | `12px` | about `24 x 17px` | Smaller, sleeker |
| Big | `20px` | about `38 x 30px` | Larger, chunkier |

### Mouse Type Visuals

| Mouse | Color | Shape | Animation | Special Visual |
|---|---|---|---|---|
| Normal | Gray `#8A8F98` | Round body, small ears, thin tail | Standard run cycle | None |
| Fast | Blue-gray `#6FA7C7` | Sleeker body, smaller ears, stiffer tail | Faster run cycle, small speed lines when moving fast | Cyan streak behind when speed > `150px/s` |
| Big | Dark slate `#4F5560` | Chunkier body, thicker tail, larger head | Slower, heavier run cycle | Small gold paw badge on back |

### Big Mouse Telegraph

The Big mouse must clearly communicate: “I can only be caught while pouncing.”

Use all of the following:

- Larger body.
- Darker color.
- Thick tail.
- Small gold paw badge on the back.
- When the cat is not pouncing, the paw badge can pulse very subtly.
- When the cat is pouncing, the paw badge glows brighter.

**Why:**  
Players need to understand Big mice without reading text during gameplay. Size, color, and a paw icon make the rule obvious.

### Mouse Face

Keep faces simple:

- Two dark eyes.
- Small pink nose.
- When startled: eyes become larger white circles with small black pupils.
- When caught: eyes become `x x` or curved happy lines, depending on tone. Keep it playful, not violent.

### Mouse States

| State | Visual |
|---|---|
| Emerging | Scale `0.4` to `1.0`, alpha `0` to `1`, shadow appears, small dust puff |
| Fleeing | Normal run animation, tail flicks, direction rotates toward movement |
| Entering hole | Mouse scales down to `0.55`, alpha fades to `0`, moves toward hole center, tail disappears last |
| Caught | Mouse becomes a small fur puff and 3-4 gold stars, then score popup |
| Escaped | Mouse sinks into hole, hole ripple plays, small dust puff |

**Why:**  
Clear state animations make spawning, escaping, and catching fair. The player should never wonder whether a mouse is visible, catchable, or escaping.

---

## 7.3 Holes

Holes are circular spawn and escape points.

### Hole Visual Size

- Gameplay radius: `24px`.
- Visual size: `48 x 48px`.
- Interior: dark radial gradient.
- Rim: `4px` thick.
- Rim color: `#4A362B`.
- Highlight: thin `1px` arc on top-left, color `#F7D9A8`, opacity `0.35`.

### Hole States

| State | Visual |
|---|---|
| Empty | Dark circle with rim |
| Spawn | Mouse emerges, small dust puff, brief ripple |
| Occupied | Teal swirl inside hole for `0.8s` |
| Blocked by cat | Gold rim glow and small paw print on rim |
| Escape | Mouse sinks, ripple expands, dust puff |

### Blocked Hole Visual

When the cat is within `40px` of the hole center:

- Hole rim glows gold.
- A small paw print appears on the rim.
- The paw print remains while the cat is blocking.
- If the cat pounces over the hole, the paw print can briefly enlarge.

**Why:**  
Blocking holes is a core tactic. The player needs to see that standing near a hole prevents escape.

### Occupied Hole Visual

When a mouse is entering:

- Teal swirl or circular ripple.
- No other mouse can visually appear to enter.
- Swirl lasts `0.8s`, matching occupied timer.

**Why:**  
Occupied and blocked states must be visually different. Occupied is temporary and mouse-related; blocked is player-controlled.

---

## 7.4 Obstacles

Obstacles are solid rectangles.

### Obstacle Visual Rules

- Use level theme prop style.
- Top surface is lighter than side.
- Side height: `4px`.
- Corner radius: `4px`.
- Shadow: `3px` offset, opacity `0.20`.
- No animated obstacle details.
- No obstacle detail should look like a hole.
- Obstacle shadows must not cover hole centers. If an obstacle is close to a hole, reduce shadow spread.

**Why:**  
Obstacles should read as furniture or props, not as gameplay hazards beyond blocking movement. They must not create visual confusion with holes or mice.

---

## 8. HUD and UI Layout

## 8.1 Top Left: Score, Combo, Level/Wave

Position:

```text
Score:      x = 16, y = 12
Combo:      x = 16, y = 36
Level/Wave: x = 16, y = 56
```

### Score

- Font: `18px` monospace.
- Color: `#2F2A25`.
- Format:

```text
Score 000000
```

### Combo

- Font: `16px` bold.
- Color: `#F2B84B`.
- Show only when combo multiplier is greater than `1.0`.
- Format:

```text
Combo x1.25
```

When combo is active:

- Text pulses once on each catch.
- When combo resets, text fades out over `0.2s`.

### Level or Wave

- Font: `12px` semiBold uppercase.
- Color: `#2F2A25` at `60%` opacity.
- Campaign:

```text
LEVEL 3
```

- Endless:

```text
WAVE 5
```

**Why:**  
The top left contains persistent status. It should be compact and always readable without distracting from the center of the arena.

---

## 8.2 Top Center: Progress

Position:

```text
Progress text: centered at x = 480, y = 10
Progress bar:  x = 360, y = 28, width = 240, height = 12
```

### Progress Text

- Font: `14px` semiBold.
- Color: `#2F2A25`.
- Format:

```text
Caught 7/10
```

### Progress Bar

- Background: `#E8DCC8`
- Fill: `#3FA3A3`
- Corner radius: `6px`
- Fill amount: `caught_count / target_catches`
- Clamp between `0` and `1`.
- When complete, fill becomes `#F2B84B`.
- On catch, the bar pulses once with a `0.15s` ease-out fill animation.

**Why:**  
The progress bar is the main objective feedback. It should be centered because catching is the core goal.

---

## 8.3 Top Right: Lives and Pause

Position:

```text
Lives:  x = 830, y = 22
Pause:  x = 912, y = 16, width = 32, height = 32
```

### Lives

Display three mouse head icons.

- Icon size: `20 x 20px`.
- Spacing: `8px`.
- Full life: gray mouse head, color `#8A8F98`.
- Lost life: outline only, color `#C9C9C9`, opacity `0.7`.
- When a life is lost:
  - Icon cracks briefly.
  - Icon fades to lost state over `0.3s`.
  - A small red flash appears on the icon.

**Why:**  
The gameplay document uses mouse icons for lives. This directly communicates “mice escaped” without needing hearts or abstract symbols.

### Pause Button

- Size: `32 x 32px`.
- Corner radius: `8px`.
- Background: `#FFF8EC` at `90%` opacity.
- Border: `#E8DCC8`.
- Icon: two vertical bars, color `#2F2A25`.
- Hover: background becomes `#3FA3A3`, icon becomes `#FFF8EC`.
- Focus: `3px` outline `#3FA3A3`.

**Why:**  
Pause is important for browser play, especially when the tab loses focus. It should be visible but not dominant.

---

## 8.4 Bottom Center: Pounce Cooldown

Position:

```text
Label: centered at x = 480, y = 504
Bar:   x = 420, y = 520, width = 120, height = 8
```

### Pounce Label

- Font: `12px` semiBold.
- Color: `#2F2A25` at `70%` opacity.
- Text:

```text
Pounce
```

### Pounce Bar

- Background: `#E8DCC8`
- Fill: `#F2B84B`
- Corner radius: `4px`
- Fills left to right as pounce becomes ready.
- When full:
  - Fill pulses gently.
  - Optional small glow.
- When pounce is buffered:
  - Bar flashes white once for `0.1s`.

**Why:**  
Pounce is the cat’s main action. The cooldown must always be visible so the player understands when pouncing is available.

---

## 8.5 Center Screen Messages

Position:

```text
Center point: x = 480, y = 210
```

Messages are non-interactive.

### Message Rules

- Only one message at a time.
- Higher priority replaces lower priority.
- Duration: `1.0s` to `1.5s`.
- Fade in: `0.15s`.
- Hold: `0.8s` to `1.0s`.
- Fade out: `0.25s`.
- No background panel during active gameplay.
- Use large text with cream shadow.

### Message Priority

| Priority | Message | Color | Duration |
|---:|---|---|---:|
| 1 | Game Over | Use overlay, not center message | — |
| 2 | Level Complete | Use overlay, not center message | — |
| 3 | Wave Complete | Use overlay, not center message | — |
| 4 | Mouse escaped! | `#E2574C` | `1.0s` |
| 5 | New mouse type: Fast / Big | `#3FA3A3` | `1.2s` |
| 6 | Level X / Wave X | `#2F2A25` | `1.0s` |

### Example Messages

```text
Level 3
Wave 5
Mouse escaped!
New mouse type: Fast
New mouse type: Big
```

**Why:**  
Center messages should interrupt just enough to communicate important events, then disappear quickly so they do not block the chase.

---

## 9. UI Components

## 9.1 Buttons

Default button:

- Width: `180px`
- Height: `44px`
- Corner radius: `10px`
- Background: `#FFF8EC`
- Border: `2px` `#E8DCC8`
- Text: `#2F2A25`
- Font: `18px` semiBold

### Button States

| State | Visual |
|---|---|
| Default | Cream background, dark text |
| Hover | Background `#3FA3A3`, text `#FFF8EC`, button lifts `2px` |
| Pressed | Button drops `2px` |
| Focus | `3px` outline `#3FA3A3`, offset `2px` |
| Disabled | Background `#E8E2D8`, text `#9A938B`, no hover |

### Primary Button

Use primary style for main actions:

- Play
- Retry
- Resume
- Next Level
- Play Endless

Primary hover can use gold `#F2B84B` with dark text for success actions, or teal `#3FA3A3` for neutral actions. Keep consistent:

- Success/progress: gold hover.
- Neutral/system: teal hover.

**Why:**  
Buttons need clear hover and focus states for mouse and keyboard accessibility.

---

## 9.2 Panels

Overlay panels:

- Background: `#FFF8EC` at `95%` opacity.
- Border: `2px` `#E8DCC8`.
- Corner radius: `16px`.
- Shadow: soft drop shadow, opacity `0.18`.
- Width: usually `420px`.
- Height: `240px` to `300px` depending on content.

Dim background behind panels:

```text
rgba(31, 26, 22, 0.45)
```

**Why:**  
Panels should feel warm and friendly, not harsh. The dim background separates UI from gameplay without completely hiding the arena.

---

## 9.3 Icons

Use simple icons, not text-only labels.

| Icon | Size | Use |
|---|---:|---|
| Mouse head | `20 x 20px` | Lives, objective, progress |
| Paw print | `16 x 16px` | Pounce, Big mouse badge, blocked hole |
| Pause | `20 x 20px` | Pause button |
| Lock | `16 x 16px` | Locked Endless button |
| Star | `12 x 12px` | Catch particles, score feedback |
| Speed line | vector | Fast mouse, pounce feedback |

**Why:**  
Icons make the game readable in under a second and reduce reliance on text.

---

## 10. State-by-State Visuals

## 10.1 Main Menu

### Layout

- Background: Level 1 Kitchen theme, dimmed `20%`.
- Optional subtle animation: cat tail wags, mouse icon peeks from a hole.
- Title centered at `x = 480, y = 120`.
- Buttons centered vertically.

### Content

```text
Cat: Mice Hunt
Play
Endless
How to Play
```

### Button Positions

```text
Play:        centered at x = 480, y = 260
Endless:     centered at x = 480, y = 320
How to Play: centered at x = 480, y = 380
```

Button size: `200 x 48px`.

### Endless Button

- If unlocked: normal button.
- If locked: disabled button with lock icon.
- Locked text:

```text
Endless
```

Small helper text below button, optional:

```text
Complete Level 10
```

**Why:**  
The menu should be simple. The player should immediately know the three possible actions: play campaign, play endless if available, or learn controls.

---

## 10.2 How to Play

### Layout

- Panel: `560 x 360px`, centered.
- Title: `How to Play`.
- Back button bottom-right.

### Content

Show concise sections:

```text
Move: WASD or Arrow Keys
Pounce: Space or Left Click

Catch mice before they hide.
Mice can hide in holes after 2.5 seconds.
Pounce to catch Big mice.
Catch mice quickly to build combo.
Do not let 3 mice escape.
```

Mouse type row:

- Normal mouse icon: `Normal: Standard mouse.`
- Fast mouse icon: `Fast: Faster, smaller mouse.`
- Big mouse icon: `Big: Can only be caught while pouncing.`

Use icons next to each mouse type.

**Why:**  
The How to Play screen should be scannable. Icons and short lines reduce cognitive load.

---

## 10.3 Level Intro

Duration: `1.5s`.

The arena is visible and the cat is controllable. No mice spawn.

### Layout

```text
Area name:   centered at x = 480, y = 150
Level:       centered at x = 480, y = 190
Objective:   centered at x = 480, y = 235
Lives:       centered at x = 480, y = 270
New type:    centered at x = 480, y = 310
```

### Content

```text
Kitchen
Level 1
Catch 5 mice
[3 mouse head icons]
```

If a new mouse type appears:

```text
New mouse type: Fast
```

or:

```text
New mouse type: Big
```

### Visual Notes

- Area name uses the level accent color.
- Level number is large and bold.
- Objective includes a small mouse icon before the text.
- New mouse type appears with the corresponding mouse icon.
- No large panel. Use text with cream shadow.
- Fade in: `0.2s`, fade out: `0.2s`.

**Why:**  
The intro must be fast. It should tell the player the goal and any new threat without stopping momentum.

---

## 10.4 Playing

During active gameplay:

- HUD is visible.
- Center messages appear only for important events.
- No overlay panels.
- No large background changes.
- Cat, mice, holes, and obstacles remain fully visible.

### Gameplay Feedback

See Section 11.

**Why:**  
Playing state must prioritize readability. Any visual that competes with mice or holes should be cut.

---

## 10.5 Paused

### Visual

- Dim background: `rgba(31, 26, 22, 0.45)`.
- Panel: `360 x 260px`, centered.
- Title: `Paused`.

### Buttons

```text
Resume
Restart
Main Menu
```

Button size: `180 x 44px`.

### Behavior

- All gameplay animation stops.
- Music pauses or lowers to a muted drone.
- SFX stop.
- Pause button in HUD is replaced by panel buttons.

**Why:**  
Pause should be calm and clear. The player should know exactly how to return to the game.

---

## 10.6 Level Complete

### Visual

- Dim background.
- Panel: `420 x 280px`, centered.
- Title: `Level X Complete`.
- Gold accent underline or small star icon.

### Content

```text
Level 3 Complete
Score: 004500
Life bonus: 1500
Clean bonus: 1000
Bonus: 2500
High Score: 005200
Next Level
```

If no clean bonus, omit that line.

If high score is new:

- Show gold badge:

```text
New High Score
```

### Auto Progress

- Text below button:

```text
Next in 3
```

- Small progress bar: `120 x 6px`, fills over `3s`.
- Player can click Next immediately.

**Why:**  
Level complete should feel rewarding but not slow. The bonus breakdown explains score, and auto-progress keeps the campaign moving.

---

## 10.7 Campaign Complete

### Visual

- Dim background.
- Panel: `420 x 300px`, centered.
- Title: `Campaign Complete`.
- Small celebratory particles: gold stars, max `12`, slow drift.

### Content

```text
Campaign Complete
Score: 012500
High Score: 012500
Endless Unlocked
Play Endless
Main Menu
```

### Endless Unlocked

- Show a small lock icon breaking open or a gold badge.
- Keep it simple; no long animation.

**Why:**  
Campaign completion should feel like a milestone, but the game is short. A brief celebration is enough.

---

## 10.8 Game Over

### Visual

- Dim background slightly darker than pause: `rgba(31, 26, 22, 0.55)`.
- Panel: `420 x 260px`, centered.
- Title: `Game Over`.
- Use warning red accent, but keep it soft.

### Content

```text
Game Over
Level 3
Score: 004200
Retry Level
Main Menu
```

### Mood

- No harsh visual punishment.
- No red flashing.
- Optional small mouse icon slipping into a hole.

**Why:**  
Game over should communicate failure clearly but remain friendly. The player should want to retry immediately.

---

## 10.9 Endless Wave Complete

### Visual

- Dim background.
- Panel: `420 x 280px`, centered.
- Title: `Wave X Complete`.

### Content

```text
Wave 5 Complete
Score: 018400
Wave bonus: 2500
Life bonus: 750
Clean bonus: 1000
Bonus: 4250
Next Wave in 3
```

### Auto Progress

- Progress bar fills over `3s`.
- No button required, but optional `Next Wave` button can appear.

**Why:**  
Endless mode should flow faster than campaign. The wave complete screen should be brief.

---

## 10.10 Endless Game Over

### Visual

- Same as Game Over, but title context changes.

### Content

```text
Game Over
Wave 5
Score: 021300
Retry Wave
Main Menu
```

**Why:**  
Endless failure should be easy to understand and quick to retry.

---

## 11. Gameplay Feedback

Feedback should be immediate, localized, and short.

## 11.1 Pounce

When the cat pounces:

- Cat stretches.
- Shadow stretches.
- 2-3 dust puffs at start.
- 2-3 dust puffs at landing.
- Speed lines in pounce direction.
- Pounce bar flashes if input was buffered.

Duration:

- Pounce animation matches `0.18s` pounce duration.
- Landing squash: `0.05s`.

**Why:**  
Pounce should feel like a burst. The visual stretch and dust make the speed increase readable.

---

## 11.2 Catch

When a mouse is caught:

- Mouse disappears into a small fur puff.
- 3-4 gold stars appear.
- Score popup appears at mouse position.
- Cat does a brief happy face.
- Progress bar pulses.
- Combo text pulses if active.

### Score Popup

- Font: `14px` bold.
- Color: `#F2B84B` for bonus points, `#2F2A25` for base points.
- Animation: rise `20px`, fade over `0.8s`.
- Show final points after combo multiplier.

Examples:

```text
+100
+150
+200
```

If a pounce or quick bonus applies, the popup can be gold. No need to show every bonus reason as text.

**Why:**  
Score popups make scoring feel responsive without requiring the player to read the HUD.

---

## 11.3 Multi-Catch

If multiple mice are caught in the same catch event:

- Each mouse gets its own score popup.
- One additional gold text appears near the cat:

```text
MULTI +100
```

- Multi-catch chime plays.
- Slight gold flash on the progress bar.

**Why:**  
Multi-catch is a skill reward. It should feel bigger than a normal catch but not overwhelm the screen.

---

## 11.4 Combo

Combo is shown in the top left.

When combo increases:

- Combo text pulses.
- Color remains gold.
- At combo multiplier `2.0` and `3.0`, play a small milestone chime.
- Optional small star sparkle near combo text.

When combo resets:

- Combo text fades out.
- No large punishment effect.

**Why:**  
Combo should encourage aggressive play. Milestone feedback rewards sustained performance without cluttering the arena.

---

## 11.5 Mouse Escape

When a mouse escapes:

- Mouse sinks into hole.
- Hole ripple expands.
- Small dust puff.
- Red center message:

```text
Mouse escaped!
```

- One life icon cracks and fades.
- Soft red vignette pulse around screen edges for `0.2s`, opacity `0.12`.
- Combo resets visually.

No screen shake.

**Why:**  
Escape is the main failure condition. It needs strong feedback, but not so strong that it hides the next mouse.

---

## 11.6 Big Mouse Startle

When a Big mouse is touched by a non-pouncing cat:

- Big mouse flashes white for `0.08s`.
- Eyes become wide.
- Tail puffs.
- Small speed lines appear.
- Startle squeak plays.
- Mouse moves away faster.

No catch occurs.

**Why:**  
This teaches the Big mouse rule through immediate feedback. The player sees that normal contact does not work.

---

## 11.7 Hole Blocked

When the cat blocks a hole:

- Hole rim glows gold.
- Paw print appears on rim.
- Mice seeking that hole should visibly avoid it.

No text.

**Why:**  
The player needs to understand that standing near a hole matters.

---

## 11.8 Hole Occupied

When a mouse enters a hole:

- Teal swirl appears.
- Other mice avoid the hole.
- Swirl lasts `0.8s`.

**Why:**  
Occupancy is a temporary state. A distinct swirl prevents confusion with blocked holes.

---

## 11.9 Spawn

When a mouse emerges:

- Small dust puff.
- Mouse scales from `0.4` to `1.0`.
- Shadow appears.
- No warning icon needed.

**Why:**  
Spawn should be visible but not overly dramatic. The emerging state already gives the player a fair reaction window.

---

## 12. Particles and Screen Effects

Use particles sparingly.

### Particle Limits

- Maximum active particles: `20`.
- Maximum stars per catch: `4`.
- Maximum dust puffs per event: `5`.
- Particles should not obscure mice or holes for more than `0.1s`.

### Particle Types

| Effect | Color | Duration |
|---|---|---:|
| Dust puff | `#D9C8A8` | `0.3s` |
| Catch stars | `#F2B84B` | `0.4s` |
| Escape dust | `#C9C9C9` | `0.4s` |
| Pounce dust | `#D9C8A8` | `0.25s` |
| Red vignette | `#E2574C` | `0.2s` |
| Gold success flash | `#F2B84B` | `0.2s` |

### Screen Effects

- No screen shake.
- No full-screen flashes during active gameplay.
- Red vignette only on escape.
- Gold flash only on level/wave complete.
- Dim overlays only when gameplay is stopped.

**Why:**  
The game is fast. Large effects would hide mice and make the player feel cheated.

---

## 13. UX and Readability Rules

## 13.1 Visual Hierarchy

From most important to least important:

1. Cat
2. Active mice
3. Holes
4. Obstacles
5. Floor
6. HUD

**Why:**  
The player must always know where they are, where the mice are, and where mice can escape.

---

## 13.2 Colorblind and Contrast Rules

- Mouse types use color plus size and shape.
- Normal: gray, medium size.
- Fast: blue-gray, smaller, speed lines.
- Big: dark slate, larger, paw badge.
- Important UI states use icons, not color alone.
- Text contrast should meet WCAG AA where practical.
- Floor patterns are low contrast.
- Holes are always dark and circular.

**Why:**  
The game should be playable without relying on color difference alone.

---

## 13.3 Motion Sensitivity

Respect reduced motion where possible:

- Disable speed lines.
- Disable vignette pulses.
- Reduce particle count.
- Keep essential state changes visible.
- Do not remove pounce stretch or hole ripple, because they communicate gameplay state.

**Why:**  
Motion effects improve feel, but they should not become a barrier.

---

## 13.4 Fairness Rules

- All active mice must remain visible.
- No mouse can visually disappear except when entering a hole or being caught.
- Holes must always be visible.
- Blocked and occupied holes must look different.
- Big mice must be clearly marked.
- Pounce cooldown must always be visible.
- No effect may cover a mouse or hole for more than `0.1s`.

**Why:**  
The core tension is “can you catch the mouse before it disappears?” The player should never feel cheated by invisible or obscured mice.

---

## 14. Music

Use a small number of musical pieces. Do not create a unique track for every level.

## 14.1 Main Menu Music

- Tempo: `96 BPM`.
- Key: C major.
- Instruments: marimba, soft bass, light pizzicato.
- Mood: cozy, curious, gentle.
- No drums or very light percussion.
- Loop length: `20` to `30s`.

**Why:**  
The menu should feel inviting and low-pressure.

---

## 14.2 Gameplay Music

- Tempo: `124 BPM`.
- Key: D major.
- Instruments: marimba, pizzicato strings, light bass, soft hand drums.
- Mood: playful, urgent, bouncy.
- Loop length: `24` to `32s`.

### Adaptive Layers

| Layer | Trigger | Instruments |
|---|---|---|
| Base | Always during gameplay | Marimba motif, bass |
| Chase | `active_mouse_count > 0` | Pizzicato strings |
| Pressure | `lives == 1` | Hand drums, low tom pulse |

**Why:**  
One adaptive track keeps the campaign coherent while increasing tension when the player is close to failure.

---

## 14.3 Endless Music

- Tempo: `132 BPM`.
- Key: B minor or D minor, but keep the same melodic motif.
- Instruments: same core plus shaker, extra percussion, slightly lower bass.
- Mood: more intense, but still playful.

**Why:**  
Endless mode should feel like the same game pushed further, not a separate soundtrack.

---

## 14.4 Jingles

Use short jingles for state changes.

| Event | Style | Length |
|---|---|---:|
| Level complete | Bright 3-note major jingle | `0.6s` |
| Campaign complete | Slightly longer fanfare | `1.2s` |
| Endless wave complete | Bright 4-note jingle | `0.5s` |
| Game over | Soft low sting, not harsh | `0.6s` |
| Endless game over | Same sting, slightly lower | `0.6s` |

**Why:**  
Short jingles reinforce success and failure without interrupting the arcade flow.

---

## 15. Sound Effects

All SFX should be short, clear, and non-intrusive.

### Required SFX Table

| Cue | Trigger | Sound Description | Length | Volume | Notes |
|---|---|---|---:|---:|---|
| UI click | Button press | Soft wood tick | `20ms` | `0.5` | No pan |
| Pounce whoosh | Cat pounce start | Filtered noise sweep up, short sine down | `120ms` | `0.7` | Pan by cat x |
| Mouse catch pop | Mouse caught | Pop plus short blip | `80ms` | `0.8` | Pitch rises slightly with combo |
| Multi-catch chime | Multi-catch | Two quick bright notes | `150ms` | `0.6` | After catch pop |
| Big mouse startle squeak | Big mouse touched while not pouncing | High quick squeak with vibrato | `100ms` | `0.7` | Pan by mouse x |
| Mouse escape squeak | Mouse escapes | Descending squeak plus soft thud | `200ms` | `0.8` | Pan by hole x |
| Combo milestone | Combo reaches `x2.0` or `x3.0` | Small bright chime | `200ms` | `0.5` | Optional but recommended |
| Level complete jingle | Level complete | 3-note major jingle | `600ms` | `0.7` | Duck music |
| Campaign complete jingle | Campaign complete | 4-note fanfare | `1200ms` | `0.8` | Duck music |
| Game over sting | Game over | Soft low descending sting | `600ms` | `0.6` | Not harsh |
| Endless wave complete jingle | Endless wave complete | 4-note bright jingle | `500ms` | `0.7` | Duck music |
| Endless game over sting | Endless game over | Low descending sting | `600ms` | `0.6` | Slightly lower than campaign game over |

### SFX Pitch and Combo

For mouse catch:

- Base pitch: `600Hz`.
- Add one semitone per combo level.
- Cap pitch increase at `+12 semitones`.

**Why:**  
Pitch rising with combo gives subtle audio feedback that the player is building momentum.

---

## 16. Audio Mixing and Panning

### Master Mix

- Master gain: `0.8`
- Music gain: `0.35`
- SFX gain: `0.7`

### Music Ducking

When a jingle plays:

- Lower music by `3dB`.
- Return over `0.3s` after jingle ends.

### Panning

For gameplay SFX:

```text
pan = (x / 960 - 0.5) * 0.7
```

Where `x` is the entity’s horizontal position.

- Cat pounce pans by cat x.
- Catch pans by mouse x.
- Escape pans by hole x.
- UI sounds are center.

**Why:**  
Light panning helps the player locate events in a top-down arena, but it should not become disorienting.

---

## 17. Audio Unlock and Browser Notes

- Create the `AudioContext` on first user interaction.
- First interaction can be:
  - Clicking Play.
  - Pressing any key.
  - Clicking the canvas.
- If audio context is suspended, resume it on user interaction.
- Pause all audio when the game pauses.
- Stop gameplay SFX when the browser loses focus.

**Why:**  
Browsers block audio until user interaction. This avoids a silent game on start.

---

## 18. Optional Procedural Audio Recipes

These are reference recipes, not required exact implementations.

```js
function blip(ctx, { freq = 600, endFreq = null, duration = 0.1, type = "sine", volume = 0.5, pan = 0 }) {
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  const panner = ctx.createStereoPanner();

  osc.type = type;
  osc.frequency.setValueAtTime(freq, ctx.currentTime);

  if (endFreq) {
    osc.frequency.exponentialRampToValueAtTime(endFreq, ctx.currentTime + duration);
  }

  gain.gain.setValueAtTime(volume, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);

  panner.pan.value = pan;

  osc.connect(gain);
  gain.connect(panner);
  panner.connect(ctx.destination);

  osc.start();
  osc.stop(ctx.currentTime + duration);
}
```

### Example Cues

```js
// UI click
blip(ctx, { freq: 800, duration: 0.03, type: "square", volume: 0.25 });

// Pounce whoosh: use filtered noise sweep from 400Hz to 1600Hz over 0.12s.

// Catch pop:
blip(ctx, { freq: 600, endFreq: 900, duration: 0.08, type: "sine", volume: 0.6 });
// Add a 30ms noise burst for the pop.

// Escape squeak:
blip(ctx, { freq: 900, endFreq: 400, duration: 0.2, type: "triangle", volume: 0.6 });
// Add a soft 100Hz thud at the end.
```

**Why:**  
Procedural audio keeps the game small, fast to load, and consistent.

---

## 19. Asset Naming Conventions

If using pre-made assets, use these names.

### Backgrounds

```text
bg_level_01.png
bg_level_02.png
bg_level_03.png
bg_level_04.png
bg_level_05.png
bg_level_06.png
bg_level_07.png
bg_level_08.png
bg_level_09.png
bg_level_10.png
```

Size: `960 x 540`.

### Entities

```text
cat.png
mouse_normal.png
mouse_fast.png
mouse_big.png
hole.png
hole_occupied.png
```

If using sprite sheets:

```text
cat_sheet.png
mouse_normal_sheet.png
mouse_fast_sheet.png
mouse_big_sheet.png
```

Recommended sprite sheet frame size: `64 x 64px`.

### UI

```text
ui_button.png
ui_button_hover.png
ui_button_disabled.png
ui_panel.png
icon_mouse_head.png
icon_paw.png
icon_pause.png
icon_lock.png
icon_star.png
```

**Why:**  
Consistent naming makes integration easier and reduces asset confusion.

---

## 20. Background Generation Notes

Backgrounds can be pre-rendered once per level.

For each level:

1. Fill canvas with floor color.
2. Add subtle pattern:
   - Tile lines for kitchen/laundry.
   - Wood planks for dining/hallway/attic.
   - Carpet noise for living/bedroom.
   - Concrete noise for basement.
   - Stone pavers for patio.
3. Add wall border: `8px` inside canvas.
4. Add soft vignette.
5. Save as `bg_level_XX.png` or draw to an offscreen canvas.

Keep pattern contrast low.

**Why:**  
Pre-rendered backgrounds are cheap to draw every frame and keep performance stable.

---

## 21. Performance Visual Constraints

- Pre-render level backgrounds.
- Pre-render obstacle shadows if possible.
- Avoid per-frame blur filters.
- Use simple shapes and cached canvases.
- Limit particles to `20` active.
- Limit score popups to `5` active.
- Avoid full-screen effects during active gameplay.
- Use short audio files or procedural audio.
- Keep music loops small.
- Target `60fps` at `960 x 540`.

**Why:**  
The gameplay is simple and fast. Visuals should not become a performance bottleneck.

---

## 22. Cut Pieces

These are intentionally excluded.

| Cut Piece | Reason |
|---|---|
| Unique music track per level | Too much audio content for a short arcade game |
| Detailed environmental animation | Distracts from mice and holes |
| Screen shake | Hides fast-moving entities |
| Complex particle systems | Unnecessary and can obscure gameplay |
| Voice lines | Not needed for a short browser game |
| Level select screen | Gameplay already cuts level select |
| Cosmetic unlocks | Adds UI and save complexity |
| Boss mice | Cuts by gameplay design |
| 3D models | Not needed for 2D top-down |
| In-game settings menu | Not required for this scope |
| High score display on main menu | Not necessary; high scores appear on complete screens |
| Spawn warning icon | Mouse emerging animation is enough |
| Hole block sound | Visual paw print is enough; sound would become repetitive |

**Why:**  
Every added visual or audio piece must improve readability, feedback, or mood. If it competes with the core chase, it should be cut.

---

## 23. Final Visual Summary

The game should look like a bright, warm, top-down cat-and-mouse arcade. The cat is orange and readable. Mice are small and distinct by size, color, and shape. Holes are dark, obvious, and clearly show when occupied or blocked. Levels change rooms and prop styles, but the UI, entity colors, and animation language stay consistent.

The UX should be:

- Understandable in 10 seconds.
- Fair during fast chases.
- Rewarding when catching mice quickly.
- Clear when a mouse escapes.
- Smooth from menu to endless mode.

The audio should be:

- Playful and bouncy during gameplay.
- Calmer in menus.
- More intense in endless mode.
- Full of short, readable SFX for pounce, catch, escape, and UI.