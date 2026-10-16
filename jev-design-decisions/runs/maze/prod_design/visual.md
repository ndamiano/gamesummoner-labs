# `visual.md`

## 1. Purpose and Scope

This document defines the complete visual and audio presentation for **Fading Labyrinth**.

It is the handoff reference for integrating visuals, UX, music, and sound effects into the gameplay design. It does **not** redefine maze generation, movement rules, level logic, or star rules. Those remain owned by `gameplay.md`.

This document is responsible for:

- A coherent visual identity across all screens and levels.
- In-game readability for the player, trail, orbs, exit, fog, and HUD.
- UX for menus, HUD, toasts, input, accessibility, and screen flow.
- Music and sound effects.
- Optional asset-generation notes and code for textures/sprites/sounds.

The goal is a game that feels **quiet, focused, and memory-driven**. The visuals should support the core fantasy: the maze is mostly dark, the player’s light is small, and the trail is the only fading memory.

---

## 2. Core Visual Identity

**Working style name:** *Quiet Nocturnal Labyrinth*

The game should feel like a calm, dark puzzle space where light and memory are the main tools.

### 2.1 Theme

The maze is not a hostile dungeon. It is a quiet, almost meditative space. The player is not fighting the maze; they are remembering it.

Visual priorities:

1. **Readability first.** The maze structure must be instantly clear.
2. **Memory second.** The trail should feel like a fading memory, not a map.
3. **Calm tension third.** The darkness creates focus, not panic.
4. **Minimal decoration fourth.** No unnecessary environmental details.

### 2.2 Style Keywords

- Minimal
- Nocturnal
- Soft light
- High contrast
- Geometric
- Quiet
- Vector-clean
- No ornate fantasy detail
- No pixel-art noise
- No screen shake
- No busy environmental animation

### 2.3 Core Shape Language

Every gameplay object uses a distinct silhouette. Color is secondary.

| Object | Shape | Why |
|---|---|---|
| Player | Rounded diamond | Distinct from orbs and exit; easy to read at small size |
| Orb | Circle with ring | Clearly collectible and distinct from player |
| Exit | Square frame | Distinct from player and orbs |
| Locked exit | Square frame with horizontal bars | Shape differs from unlocked exit |
| Unlocked exit | Square frame with open circle | Shape differs from locked exit |
| Trail | Small dot/oval | Reads as a footprint/memory mark, not a collectible |
| Wall | Thick rounded line segment | Clear maze structure |
| Floor | Flat lit surface | Neutral background for gameplay objects |

**Important:** The player, orb, and exit must remain recognizable even in grayscale or colorblind mode. Shape is the primary identifier.

---

## 3. Critical Readability Rules

These rules are non-negotiable for integration.

### 3.1 Gameplay Visibility Controls Visual Reveal

The visual system must not reveal more than the gameplay visibility system allows.

- The light radius is gameplay-defined.
- Trail visibility is gameplay-defined.
- The visual light gradient is decorative only.
- No tile, wall, orb, or exit may be rendered outside the gameplay visibility mask.

**Why:** If visuals reveal extra information, the memory challenge breaks.

### 3.2 Trail Is the Only Memory System

The trail is visually distinct from the current light.

- Current light: bright, warm, immediate.
- Trail memory: dimmer, cooler, fading.

**Why:** The player should be able to tell what they are seeing now versus what they remember.

### 3.3 Core Entity Colors Stay Constant Across Levels

The player, orbs, exit, trail, walls, and floor use the same core visual language in every level.

Levels vary only through subtle background tint, fog tone, and level-select accent color.

**Why:** Constant entity colors keep the game readable and coherent. Level variation should not require the player to relearn what the player, orbs, or exit look like.

### 3.4 No Color-Only Cues

All important states must use shape, icon, text, or luminance.

- Locked and unlocked exit differ by shape.
- Orbs have a ring.
- Player has a diamond shape.
- HUD icons include shape and label.
- Colorblind mode adds outlines and adjusts hue.

**Why:** Accessibility is part of the core UX.

### 3.5 Audio Is Never Required

Every gameplay-critical event must have a visual cue.

Audio enhances the experience but is never necessary to understand the game.

**Why:** Players may mute the game, use headphones inconsistently, or play in noisy environments.

---

## 4. Color System

## 4.1 Default Palette

Use this palette unless colorblind mode is enabled.

| Element | Hex | Notes |
|---|---:|---|
| Fog / unexplored background | `#070A12` | Near-black blue |
| Floor, current light | `#C7D0DE` | Pale blue-gray |
| Floor, trail memory | `#6A7488` | Dimmer, cooler |
| Wall base | `#1E2532` | Dark slate |
| Wall highlight | `#3A455A` | Subtle top edge |
| Wall shadow | `#0F141D` | Subtle bottom edge |
| Player | `#FFB84D` | Warm amber |
| Player outline | `#2A1E0A` | Dark warm outline |
| Player light | `#FFE0B0` | Additive warm glow |
| Orb | `#6BE0FF` | Pale cyan |
| Orb ring | `#FFFFFF` | White ring |
| Orb outline | `#0B2A38` | Dark cyan outline |
| Exit unlocked frame | `#F5F7FA` | Near-white |
| Exit unlocked inner | `#FFD166` | Soft gold |
| Exit locked frame | `#8A93A6` | Muted gray |
| Exit locked bars | `#2F3744` | Dark gray bars |
| Trail marker | `#E8DCC8` | Pale bone/warm gray |
| HUD text | `#F5F7FA` | Near-white |
| HUD secondary text | `#B9C2D0` | Muted blue-gray |
| HUD panel background | `#0B0F1A` at 70% opacity | Subtle translucent panel |
| HUD panel border | `#2A3140` | Thin border |
| Primary button | `#FFB84D` | Amber |
| Primary button text | `#1A1408` | Dark warm |
| Secondary button | `#1E2532` | Dark slate |
| Secondary button text | `#F5F7FA` | Near-white |
| Disabled button | `#151A24` | Very dark |
| Disabled button text | `#5A6478` | Muted |
| Star filled | `#FFD166` | Gold |
| Star empty | `#2A3140` | Dark slate |
| Star empty border | `#5A6478` | Muted border |
| Focus ring | `#FFFFFF` | White, 2px |

### 4.2 Colorblind Mode Palette

When colorblind mode is enabled, use the following adjustments.

| Element | Colorblind Mode |
|---|---|
| Fog | `#050505` |
| Floor, current light | `#C9D2E0` |
| Floor, trail memory | `#5A6478` |
| Wall base | `#10141D` |
| Player | `#FFD54F` with `#000000` outline |
| Orb | `#4FC3F7` with `#FFFFFF` ring and `#000000` outline |
| Exit unlocked | `#FFFFFF` frame, `#FFD54F` inner, `#000000` outline |
| Exit locked | `#111111` frame, `#FFFFFF` bars, `#000000` outline |
| Trail marker | `#FFFFFF` with `#000000` outline |
| HUD text | `#FFFFFF` |
| HUD secondary text | `#C7CDD6` |
| Primary button | `#FFD54F` with `#000000` text |
| Secondary button | `#10141D` with `#FFFFFF` text |
| Star filled | `#FFD54F` |
| Star empty | `#10141D` with `#C7CDD6` border |

**Important:** Colorblind mode should not change the shapes. It only increases outline contrast and shifts hues toward a safer blue/yellow/neutral system.

### 4.3 Level and Act Accents

Levels are visually grouped into four acts. These accents are decorative and are used mainly in level select and subtle UI highlights.

| Act | Levels | Accent Color | Feel |
|---:|---:|---|---|
| Act I | 1-3 | `#82A9FF` | Pale, open, first light |
| Act II | 4-7 | `#7ED2D2` | Cooler, deeper |
| Act III | 8-10 | `#A491E8` | Violet, dense |
| Act IV | 11-12 | `#F0C75E` | Luminous final core |

These accents must **not** be used for gameplay-critical states.

**Why:** They help the campaign feel like a journey without forcing the player to learn new visual rules per level.

### 4.4 In-Game Level Themes

Use subtle floor/wall/fog tints per act. Do not change player, orb, exit, or trail colors.

| Act | Floor Tint | Wall Tint | Fog |
|---:|---:|---:|---:|
| Act I | `#C7D0DE` | `#1E2532` | `#070A12` |
| Act II | `#BFC9DA` | `#1B2230` | `#060810` |
| Act III | `#B8C2D6` | `#19202D` | `#05060D` |
| Act IV | `#BAC4D8` | `#171E2B` | `#04050B` |

**Why:** The mazes should feel slightly different as the campaign progresses, but the core readability remains identical.

---

## 5. Typography

### 5.1 Fonts

- **Title:** Use a custom vector wordmark for “Fading Labyrinth” if possible.
- **UI body:** Use a clean geometric sans-serif.
  - Preferred: `Inter`
  - Fallback: `system-ui`, `Segoe UI`, `Roboto`, `Helvetica Neue`, `Arial`
- **Timer:** Use tabular/monospaced numerals to prevent width changes.
  - CSS: `font-variant-numeric: tabular-nums;`

### 5.2 Type Scale

Reference scale at normal text size.

| Element | Normal | Large |
|---|---:|---:|
| Title wordmark | 64px | 80px |
| Screen header | 32px | 40px |
| Button label | 18px | 22px |
| HUD level name | 16px | 20px |
| HUD objective | 14px | 18px |
| Timer | 20px | 25px |
| Best time | 12px | 15px |
| Toast text | 16px | 20px |
| Level select node number | 20px | 25px |
| Level select node name | 12px | 15px |

Large text size should scale all UI text by **125%** and increase button/panel padding by about **10%**.

**Why:** Large text must remain usable without breaking layout.

---

## 6. In-Game Visual Design

## 6.1 Camera and Viewport

- Camera follows the player.
- Camera is centered on the player.
- Camera is clamped to maze bounds.
- If the maze is smaller than the viewport, center the maze.
- Reference viewport: **15x15 tiles**.
- Player visual size: **0.6 tile**.

### Camera Motion

- Use a very short camera lerp, approximately **100ms**, for smoothness.
- No camera bounce.
- No screen shake.
- No dramatic zoom.
- If reduced motion is enabled, camera snaps directly to the player.

**Why:** Smooth but minimal camera motion preserves readability without adding noise.

### Level Start

- Fade in from fog color over **400ms**.
- Player is centered.
- No camera movement after fade.

### Level Complete

- After the final move animation completes, fade out over **400ms**.
- Then show the Level Complete or Game Complete screen.

**Why:** The fade marks the transition without interrupting the final move.

---

## 6.2 Maze Floor

The floor is a flat, clean surface.

### Floor Rules

- Use the current act floor tint.
- Add very subtle static noise, alpha around **0.03-0.05**.
- No visible grid lines.
- No ornate texture.
- No animated floor effects.

**Why:** A clean floor keeps the maze structure readable and avoids visual noise.

---

## 6.3 Walls

Walls are drawn as thick line segments between cells.

### Wall Specs

- Interior wall thickness: **0.14 tile**
- Boundary wall thickness: **0.18 tile**
- Rounded ends.
- Wall color: act wall tint.
- Subtle top highlight: 1-2px, alpha **0.5**
- Subtle bottom shadow: 1-2px, alpha **0.25**
- Optional very subtle 2.5D shadow toward bottom-right, alpha **0.12**

### Wall Visibility

A wall segment is visible if at least one adjacent tile is visible.

**Why:** This matches the gameplay rule that walls are visible if an adjacent tile is visible.

### Boundary

The outer boundary should be slightly thicker and more solid than interior walls.

**Why:** It gives the maze a clear edge and helps the player understand the outer limit.

---

## 6.4 Visibility, Fog, and Light

The visible area is defined by gameplay. The visual system should make that visible area feel like a small pocket of light.

### Visibility Mask

Use the gameplay visibility mask for all rendering.

Visible sources:

1. Player light radius.
2. Trail tiles still alive.

A tile is visually revealed if it is inside the player light radius or is a trail tile.

Walls are visible if at least one adjacent tile is revealed.

### Current Light

- Warm radial glow centered on the player.
- Light color: `#FFE0B0`
- Additive blending.
- Center alpha: approximately **0.30-0.35**
- Edge alpha: **0**
- Visual radius: **2.5 tiles**
- Soft falloff from center to edge.

**Important:** The radial gradient is decorative. It must not reveal tiles outside the gameplay mask.

### Fog

- Unrevealed area uses the act fog color.
- Add very subtle static noise, alpha around **0.04**.
- No moving fog particles.
- No animated fog swirl.
- No fog that implies hidden layout.

**Why:** Static fog feels calm and does not distract from memory.

### Trail Memory

Trail tiles that are outside the current light radius are still visible, but they should look like memory.

- Floor under trail-only tiles: render at approximately **45% brightness** of current light floor.
- Walls adjacent to trail-only tiles: render at approximately **45% brightness**.
- Orbs or exit on trail-only tiles: render at approximately **80% brightness**, but keep shape fully legible.

**Why:** This distinguishes fresh vision from fading memory without adding a meter.

---

## 6.5 Trail

The trail is the visual representation of the player’s fading memory.

### Trail Marker

- Shape: small rounded oval or dot.
- Size: approximately **0.18-0.22 tile** across.
- Color: `#E8DCC8` in default mode.
- Outline: none in default mode; black outline in colorblind mode.
- Placed on the floor of the tile the player entered.
- Rendered under walls so wall segments can overlap the edge cleanly.

### Trail Alpha

Use the gameplay trail lifetime:

- `0` to `8` seconds: alpha `1.0`
- `8` to `10` seconds: linear fade from `1.0` to `0.0`

### Trail Motion

- No pulsing.
- No scale animation.
- No blur.
- No directional arrow.
- Reduced motion: use the same simple alpha fade.

**Why:** The trail should feel like a fading footprint, not an animated object.

---

## 6.6 Player

The player is a small, bright, easily readable shape.

### Player Sprite

- Size: **0.6 tile**
- Shape: rounded diamond / rotated rounded square.
- Color: `#FFB84D`
- Outline: `#2A1E0A`, approximately **0.03 tile**
- Directional tick: small rounded triangle or short bar on the front edge.
  - Size: approximately **0.12 tile**
  - Same color as player.
  - Updates to last valid movement direction.

### Player Light

- Warm radial glow around player.
- Radius: **2.5 tiles**
- Additive.
- Subtle intensity variation:
  - Normal: ±2% over 1.5 seconds.
  - Reduced motion: no flicker.

### Movement Animation

- Move time per tile: **140ms**, matching gameplay.
- On move start:
  - Scale to **1.06**
  - Slight tilt toward movement direction: approximately **4 degrees**
- Return to normal by end of move.
- Reduced motion:
  - No scale.
  - No tilt.
  - No flicker.
  - Player snaps or moves with a simple 140ms linear interpolation.

**Why:** The movement should feel crisp and responsive, not bouncy.

---

## 6.7 Orbs

Orbs are optional collectibles. They must be clearly distinct from the player and exit.

### Orb Sprite

- Size: **0.4 tile**
- Shape: circle with ring.
- Inner circle: orb color.
- Ring: white.
- Outline: dark cyan in default mode.
- Optional small inner highlight: white, alpha **0.7**

### Orb Animation

- Idle pulse:
  - Scale from **1.00** to **1.08**
  - Duration: **1.2 seconds**
  - Smooth sine curve.
- Reduced motion:
  - No pulse.
  - Static orb.

### Collection Animation

When the player enters an orb tile:

- Orb quickly scales to **0**.
- Emit 8 small particles outward.
  - Particle size: **0.08-0.12 tile**
  - Particle color: orb color and white.
  - Duration: **300ms**
  - Fade out.
- Reduced motion:
  - No particles.
  - Orb fades out over **150ms**.

**Why:** Collection should feel satisfying but not distracting.

---

## 6.8 Exit

The exit is a square portal/gate.

### Exit Size

- Size: **0.8 tile**
- Frame thickness: approximately **0.12 tile**
- Rounded corners: approximately **0.08 tile**

### Locked Exit

- Square frame.
- Muted gray color.
- Two horizontal bars across the center.
- Bars are clearly visible in shape.
- No glow.

**Shape cue:** closed gate.

### Unlocked Exit

- Square frame.
- Near-white frame.
- Open center.
- Bright inner circle.
- Optional soft gold tint.
- No bars.

**Shape cue:** open portal.

### Exit Animation

#### Locked State

- No pulse.
- When the player steps onto a locked exit:
  - Bars flash once, alpha from **0.8** to **1.0** over **150ms**.
  - Reduced motion: no flash, but the toast and HUD change still occur.

#### Unlocked State

- Inner circle pulses:
  - Scale from **1.00** to **1.06**
  - Duration: **1.5 seconds**
  - Smooth sine curve.
- Reduced motion:
  - No pulse.
  - Static unlocked exit.

#### Unlock Moment

When the final orb is collected:

- If the exit is currently visible:
  - Bars disappear.
  - Inner circle fades in over **250ms**.
  - Small expanding ring, alpha **0.4**, duration **400ms**.
- If the exit is not currently visible:
  - Do **not** play a visible unlock animation that would reveal the exit.
  - Only show the toast and HUD update.
- Reduced motion:
  - Simple fade between locked and unlocked states.

**Why:** The unlock should feel clear, but it must not accidentally reveal hidden maze information.

---

## 6.9 Render Order

Use this render order during gameplay.

1. Fog base.
2. Visible floor tiles.
   - Current light floor: full brightness.
   - Trail memory floor: dimmed.
3. Trail markers.
4. Visible wall segments.
5. Visible orbs.
6. Visible exit.
7. Player light glow, clipped to visibility mask.
8. Player.
9. HUD and toasts.

**Why:** This keeps the player readable on top of the maze while allowing walls to properly overlap trail markers and floor.

---

## 6.10 Level Distinction

Levels should feel distinct through subtle environmental tint and level-select accent, not through new entity rules.

### In-Game Distinction

Use the act-based floor/wall/fog tints from section 4.4.

No level should change:

- Player shape.
- Orb shape.
- Exit shape.
- Trail shape.
- Core readability contrast.

### Level Select Distinction

Level select nodes can use act accent colors.

- Act I: pale blue.
- Act II: cyan.
- Act III: violet.
- Act IV: gold.

Locked nodes should be desaturated and dim.

**Why:** The player can feel progression without the gameplay visuals becoming inconsistent.

---

## 6.11 Accessibility in Gameplay

### Colorblind Mode

- Use the colorblind palette from section 4.2.
- Add outlines to player, orb, exit, and trail.
- Keep shape language unchanged.
- Do not rely on red/green distinctions.

### Reduced Motion

When reduced motion is enabled:

- Disable player light flicker.
- Disable player scale/tilt animation.
- Disable orb pulse.
- Disable exit pulse.
- Disable particle bursts.
- Disable star pop animation.
- Disable camera lerp.
- Use simple fades instead of complex motion.
- Trail uses simple alpha fade.

### Text Size

- Normal: 100%
- Large: 125%

Large text should expand HUD panels and buttons as needed.

**Why:** Accessibility settings should improve clarity without changing the maze challenge.

---

## 7. HUD Design

The HUD is minimal. It should not compete with the maze.

## 7.1 HUD Layout

### Top Left

Panel contains:

- Level number.
- Level name.
- Objective line.

Example:

```text
3  Forks
Orbs 1/3
```

### Top Right

Panel contains:

- Timer: `M:SS`
- Best time, if one exists, smaller under timer.

Example:

```text
1:24
Best 1:10
```

If no best time exists, show only the timer.

### Bottom Right

- Pause button.
- Touch target: at least **48x48px**.
- Icon: two vertical bars.

### Bottom Left

- Control hint or tutorial hint.
- Only shown when appropriate.
- Does not block movement.

### Toast Area

- Upper center, below the top HUD panels.
- Non-blocking.
- One toast at a time.

---

## 7.2 HUD Panel Style

- Background: `#0B0F1A` at 70% opacity.
- Border: 1px, `#2A3140`.
- Corner radius: **8px**.
- Padding: **12px**.
- Text: high contrast.
- No heavy drop shadows.
- No animated HUD effects.

**Why:** Panels should be readable over both light floor and dark fog without becoming cluttered.

---

## 7.3 Objective Display

Use icons plus text.

| State | Icon | Text |
|---|---|---|
| No orbs | Exit icon | `Exit` |
| Orbs remain | Orb icon | `Orbs 1/3` |
| All orbs collected | Unlocked exit icon | `Exit Open` |
| Standing on locked exit | Locked exit icon | `Exit Locked` |

If the player is standing on a locked exit, `Exit Locked` overrides the orb count display.

**Why:** The player should always know the current objective without reading long text.

---

## 7.4 Timer

- Format: `M:SS`
- Starts at `0:00`.
- Timer starts on first successful move.
- Timer pauses when game is paused.
- Timer resets on restart.
- Use tabular numerals.

**Why:** Prevents layout shift and makes times easy to read.

---

## 7.5 Toasts

Toasts are small, non-blocking messages.

### Toast Style

- Shape: rounded pill.
- Background: `#0B0F1A` at 85% opacity.
- Border: 1px, `#3A455A`.
- Text: `#F5F7FA`.
- Icon on left.
- Duration: **1.5 seconds**
- Fade in: **200ms**
- Fade out: **200ms**
- Do not stack more than one toast.
- If a new toast occurs while one is active, replace the current toast.

### Toast Types

| Event | Icon | Text |
|---|---|---|
| Orb collected, orbs remain | Orb icon | `Orb collected` |
| Final orb collected | Unlocked exit icon | `Exit unlocked` |
| Player steps onto locked exit | Locked exit icon | `Exit locked` |

The `Exit locked` toast appears only once per level attempt.

**Why:** Toasts give clear feedback without interrupting movement.

---

## 7.6 Tutorial and Control Hints

Hints appear in the bottom-left area.

### Level 1

On load:

```text
Move to explore.
```

After first move:

```text
Your trail fades after 10 seconds.
```

### Level 3, First Time

When the first orb becomes visible:

```text
Collect orbs to unlock the exit.
```

### Control Hint

On first-time play, show a small control hint until the first move:

```text
Arrows / WASD / Swipe
```

Use a small move icon next to the text.

**Why:** Hints are sparse so the game teaches through play without cluttering the screen.

---

## 8. UI Screens

## 8.1 General UI Style

- Dark background.
- Soft translucent panels.
- Rounded corners.
- High contrast text.
- Clear focus states.
- No mouse-only interactions.
- All buttons must be usable with keyboard, gamepad, and touch.

### Button Style

| State | Fill | Text | Notes |
|---|---|---|---|
| Primary normal | `#FFB84D` | `#1A1408` | Main action |
| Primary hover/selected | `#FFC66B` | `#1A1408` | Subtle brighten |
| Primary pressed | `#E6A23C` | `#1A1408` | Slight darken |
| Secondary normal | `#1E2532` | `#F5F7FA` | Border `#3A455A` |
| Secondary hover/selected | `#2A3140` | `#F5F7FA` | |
| Secondary pressed | `#151A24` | `#F5F7FA` | |
| Disabled | `#151A24` | `#5A6478` | No border emphasis |

### Focus State

- White focus ring.
- 2px thickness.
- 2px offset.
- Visible on keyboard and gamepad navigation.

### Touch Targets

- Minimum button height: **48px**
- Minimum touch target: **48x48px**
- Pause button in gameplay must be easily reachable.

---

## 8.2 Title Screen

### Background

- Fog color.
- Faint abstract maze lines, alpha around **0.05-0.08**.
- No actual level layouts.
- Reduced motion: static background.

### Content

- Game title wordmark: **Fading Labyrinth**
- Total stars: `X / 36`
- Buttons, vertically centered:
  1. `Play`
  2. `Level Select`
  3. `How to Play`
  4. `Settings`

### Button Behavior

- `Play`:
  - If no progress: start Level 1.
  - If progress exists: start next incomplete unlocked level.
- `Level Select`: open level select.
- `How to Play`: open how to play.
- `Settings`: open settings.

### Initial Focus

- `Play` is focused on load.

**Why:** The title should immediately communicate the campaign goal and offer clear entry points.

---

## 8.3 How to Play Screen

### Layout

- Header: `How to Play`
- Three cards.
- Back button.

### Card 1: Move

Icon: diamond with four small direction arrows.

Text:

```text
Use Arrow Keys, WASD, Left Stick, D-Pad, or Touch Swipe.
Holding a direction keeps moving.
```

### Card 2: Light and Trail

Icon: small circle with fading dots behind it.

Text:

```text
You only see a small area around your character.
Your trail remains for 10 seconds.
The trail fades after 8 seconds.
```

### Card 3: Objective

Icon: orb and exit.

Text:

```text
Find the exit.
If orbs are present, collect all of them to unlock the exit.
There is no fail state.
Stars are based on time.
```

### Navigation

- Keyboard/gamepad: up/down or left/right to move between cards if needed, Enter/A to go back or confirm.
- Touch: tap Back.

**Why:** The how-to-play screen should be quick to read and not introduce extra complexity.

---

## 8.4 Level Select Screen

### Background

- Dark fog color.
- Faint abstract maze path.
- No actual maze layouts.

### Top Bar

- `Level Select`
- Total stars: `X / 36`
- Back button.

### Level Node Layout

Use a serpentine 4x3 grid.

```text
1 → 2 → 3 → 4
            ↓
8 ← 7 ← 6 ← 5
            ↓
9 → 10 → 11 → 12
```

Connect nodes with a subtle path line.

### Node Design

Each node shows:

- Level number.
- Level name.
- Star count, if completed.
- Lock icon if locked.
- Highlight if selected.

### Node States

| State | Appearance |
|---|---|
| Locked | Dim, desaturated, lock icon |
| Unlocked | Full color, act accent ring |
| Completed | Full color, stars visible |
| Selected | White focus ring, slight scale **1.05** |

### Node Size

- Normal: **72px**
- Large text: **84px**

### Locked Node Behavior

- Locked nodes can be selected for viewing, but `Play Level` is disabled.
- Show tooltip or label:
  ```text
  Complete previous level to unlock
  ```

### Action Button

When an unlocked level is selected:

- Show `Play Level` button.
- If the selected level is locked:
  - `Play Level` is disabled.

### Navigation

- Keyboard/gamepad: move between nodes.
- Enter/A: select node.
- If selected node is unlocked, Enter/A can also start the level.
- B/Back: return to title.
- Touch: tap node, then tap `Play Level`.

**Why:** A visible path makes the 12-level campaign feel complete and replayable.

---

## 8.5 Gameplay Screen

The gameplay screen contains:

- Maze.
- Player.
- Exit.
- Orbs.
- Trail.
- HUD.
- Toasts.
- Tutorial hints, if active.

### Pause Input

Add pause support:

- Keyboard: `Esc` or `P`
- Gamepad: `Start`
- Touch: pause button

**Why:** Pausing is a core recovery action when the player becomes lost.

---

## 8.6 Pause Screen

### Overlay

- Darken gameplay.
- Overlay alpha: **70%**
- Freeze all gameplay animation.
- Freeze trail fade.
- Freeze timer.
- Freeze player movement.

### Panel Content

- Header: `Paused`
- Buttons:
  1. `Resume`
  2. `Restart Level`
  3. `Level Select`
  4. `Settings`
  5. `Quit to Title`

### Initial Focus

- `Resume`

### Behavior

- `Resume`: return to gameplay.
- `Restart Level`: reset level state and start fresh.
- `Level Select`: return to level select.
- `Settings`: open settings from pause.
- `Quit to Title`: return to title.

**Why:** Pause gives the player a safe recovery point without penalty.

---

## 8.7 Level Complete Screen

Used for Levels 1-11.

### Overlay

- Fade in from gameplay.
- Dark background.
- Centered panel.

### Content

- Header: `Level Complete`
- Level name.
- Stars earned: 1 to 3.
- Time.
- Best time.
- If this is a new best time, show small label:
  ```text
  New Best
  ```
- Buttons:
  1. `Next Level`
  2. `Replay`
  3. `Level Select`

### Star Display

Show three star icons in a row.

- Empty stars: dark outline.
- Earned stars: gold.

### Star Animation

Normal motion:

- First star fills at **200ms**.
- Second star fills at **600ms**, if earned.
- Third star fills at **1000ms**, if earned.
- Each star:
  - Scale from **0.6** to **1.0**
  - Slight rotation: **-10 degrees** to **0**
  - Duration: **250ms**
- Play a star sound for each newly revealed star.

Reduced motion:

- Stars fade in sequentially.
- No scale.
- No rotation.
- No shine.

### Initial Focus

- `Next Level`

**Why:** The complete screen should reward the player clearly and move them smoothly forward.

---

## 8.8 Game Complete Screen

Appears after completing Level 12.

### Content

- Header: `The Labyrinth Is Complete`
- Total stars: `X / 36`
- Final level card:
  - Level name: `Final Maze`
  - Stars earned
  - Time
  - Best time
- Buttons:
  1. `Level Select`
  2. `Title`

### Initial Focus

- `Level Select`

**Why:** The final screen should feel complete without forcing the player to replay or reset.

---

## 8.9 Settings Screen

### Content

- Header: `Settings`
- Back button.

### Settings Items

| Setting | Control | Notes |
|---|---|---|
| Input | Informational label | Shows supported inputs |
| Colorblind mode | Toggle | On/Off |
| Reduced motion | Toggle | On/Off |
| Text size | Segmented control | Normal / Large |
| Master volume | Slider | 0-100 |
| Music volume | Slider | 0-100 |
| SFX volume | Slider | 0-100 |

### Input Row

The Input row should display:

```text
Keyboard, Gamepad, Touch
```

It should **not** be a toggle that disables input methods.

**Why:** All supported inputs should work simultaneously. Forcing the player to choose one input would reduce accessibility.

### Audio Settings

Add audio volume sliders.

Defaults:

- Master: `80`
- Music: `60`
- SFX: `80`

**Why:** Audio is important for atmosphere, but players need control. Volume settings do not affect star fairness.

### Save Behavior

Settings save immediately when changed.

**Why:** Players should not lose accessibility or audio settings if they quit.

---

## 9. Audio Design

## 9.1 Audio Philosophy

The audio should feel calm, focused, and slightly mysterious.

It should support memory and concentration, not create frantic pressure.

Rules:

- No heavy percussion.
- No fast rhythmic patterns.
- No loud sudden stingers.
- No audio-only gameplay cues.
- Music should be sparse enough that the player can think.
- SFX should be short and clear.

---

## 9.2 Music

### Overall Style

- Ambient
- Minimal
- Sparse
- Soft pads
- Sparse piano/celesta-like notes
- Low drone
- No drums
- Slow tempo
- Pentatonic or simple modal scales

Suggested scale:

- D minor pentatonic: `D F G A C`

This scale is calm and avoids harsh intervals.

---

### Music Contexts

| Context | Style | Tempo | Notes |
|---|---|---:|---|
| Title | Low drone, soft pad | 50 BPM | No pulse, very sparse |
| Gameplay Act I | Sparse pad, occasional celesta note | 60 BPM | Calm, open |
| Gameplay Act II | Slightly deeper drone, soft low pulse every 2 beats | 64 BPM | Still calm |
| Gameplay Act III | Deeper pad, slightly more notes | 68 BPM | More atmospheric, not stressful |
| Level Complete | Warm major chord, gentle arpeggio | 70 BPM | Satisfying, not celebratory |
| Game Complete | Fuller ambient pad, soft resolving chord | 66 BPM | Complete, calm |

### Gameplay Music Rules

- Music must not create a metronome that pressures the player.
- Notes should be irregular or spaced widely.
- No rhythmic loop that encourages speed.
- Music should duck slightly when a toast appears, approximately **20-30%**.
- Music should pause or duck when the pause screen is open.

**Why:** The player is solving through memory, not reflex. Fast music would undermine the core fantasy.

---

### Optional Generative Approach

If implementing without recorded music assets, use a simple generative bed:

1. Low drone:
   - Two sine oscillators, slightly detuned.
   - Frequencies around `110Hz` and `110.5Hz`.
   - Low-pass filter.
   - Very low volume.

2. Sparse notes:
   - Choose 4-5 notes from the D minor pentatonic scale.
   - Play one note every 2-4 seconds.
   - Use soft sine or triangle waves.
   - Add long release.

3. Act variation:
   - Act I: fewer notes.
   - Act II: add a very soft low pulse.
   - Act III: slightly lower drone and a little more note density.

**Why:** This keeps the audio coherent and avoids needing many large music files.

---

## 9.3 Sound Effects

All SFX are non-essential.

| Event | Sound Description | Duration | Relative Volume | Notes |
|---|---|---:|---:|---|
| Player step | Short filtered noise tick | 40ms | 18% | Alternate between two close pitches to avoid monotony |
| Orb collected | Bright two-note chime | 120ms | 35% | Higher than step |
| Exit unlocked | Rising soft chord | 300ms | 30% | Clear but gentle |
| Locked exit interaction | Low muted thud plus short click | 150ms | 25% | Not harsh |
| Level complete | Gentle rising arpeggio | 600ms | 35% | Warm, satisfying |
| Star earned | High soft ping | 100ms | 25% | One per star |
| UI select | Short soft tick | 30ms | 20% | Neutral |
| UI back | Slightly lower short tick | 30ms | 18% | Slightly softer than select |

### SFX Design Notes

- Step SFX should be quiet enough not to distract during long exploration.
- Orb SFX should be clearly positive.
- Unlock SFX should sound like opening, not alarm.
- Locked exit SFX should sound muted, not punitive.
- Complete SFX should be warm, not loud.
- UI SFX should be very short.

---

## 9.4 Audio Settings

Add to Settings:

- Master volume
- Music volume
- SFX volume

Defaults:

- Master: `80`
- Music: `60`
- SFX: `80`

All SFX should be routed through:

1. SFX gain
2. Master gain

Music should be routed through:

1. Music gain
2. Master gain

**Why:** Players need independent control over ambient music and feedback sounds.

---

## 9.5 Optional SFX Synthesis Code

This code is optional. It can be used to generate simple SFX without audio assets.

```javascript
let audioCtx = null;

function ensureAudioContext() {
  if (!audioCtx) {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return null;
    audioCtx = new AudioContextClass();
  }

  if (audioCtx.state === "suspended") {
    audioCtx.resume();
  }

  return audioCtx;
}

function playTone({
  frequency = 440,
  duration = 0.1,
  type = "sine",
  volume = 0.2,
  delay = 0
}) {
  const ctx = ensureAudioContext();
  if (!ctx) return;

  const startTime = ctx.currentTime + delay;

  const oscillator = ctx.createOscillator();
  const gain = ctx.createGain();

  oscillator.type = type;
  oscillator.frequency.value = frequency;

  gain.gain.setValueAtTime(0.0001, startTime);
  gain.gain.linearRampToValueAtTime(volume, startTime + 0.01);
  gain.gain.exponentialRampToValueAtTime(0.0001, startTime + duration);

  oscillator.connect(gain);
  gain.connect(ctx.destination);

  oscillator.start(startTime);
  oscillator.stop(startTime + duration + 0.05);
}

function playNoiseTick({
  duration = 0.04,
  volume = 0.1,
  filterFrequency = 2000,
  delay = 0
}) {
  const ctx = ensureAudioContext();
  if (!ctx) return;

  const startTime = ctx.currentTime + delay;
  const sampleRate = ctx.sampleRate;
  const frameCount = Math.floor(sampleRate * duration);
  const buffer = ctx.createBuffer(1, frameCount, sampleRate);
  const data = buffer.getChannelData(0);

  for (let i = 0; i < frameCount; i++) {
    data[i] = Math.random() * 2 - 1;
  }

  const source = ctx.createBufferSource();
  source.buffer = buffer;

  const filter = ctx.createBiquadFilter();
  filter.type = "lowpass";
  filter.frequency.value = filterFrequency;

  const gain = ctx.createGain();
  gain.gain.setValueAtTime(volume, startTime);
  gain.gain.exponentialRampToValueAtTime(0.0001, startTime + duration);

  source.connect(filter);
  filter.connect(gain);
  gain.connect(ctx.destination);

  source.start(startTime);
  source.stop(startTime + duration);
}

function playSfx(name) {
  switch (name) {
    case "step":
      playNoiseTick({
        duration: 0.04,
        volume: 0.08,
        filterFrequency: 1800 + Math.random() * 400
      });
      break;

    case "orb":
      playTone({ frequency: 880, duration: 0.12, volume: 0.2 });
      playTone({ frequency: 1318, duration: 0.12, volume: 0.15, delay: 0.05 });
      break;

    case "unlock":
      playTone({ frequency: 261, duration: 0.3, volume: 0.15 });
      playTone({ frequency: 329, duration: 0.3, volume: 0.12, delay: 0.05 });
      playTone({ frequency: 392, duration: 0.3, volume: 0.12, delay: 0.1 });
      break;

    case "locked":
      playTone({ frequency: 120, duration: 0.15, volume: 0.15 });
      playNoiseTick({ duration: 0.05, volume: 0.05, filterFrequency: 800, delay: 0.02 });
      break;

    case "complete":
      [261, 329, 392, 523].forEach((frequency, i) => {
        playTone({
          frequency,
          duration: 0.35,
          volume: 0.15,
          delay: i * 0.1
        });
      });
      break;

    case "star":
      playTone({ frequency: 1046, duration: 0.12, volume: 0.15 });
      break;

    case "ui":
      playTone({ frequency: 1000, duration: 0.04, type: "triangle", volume: 0.08 });
      break;

    case "back":
      playTone({ frequency: 700, duration: 0.04, type: "triangle", volume: 0.07 });
      break;
  }
}
```

**Note:** In a full implementation, route `ctx.destination` through master/music/SFX gain nodes to respect volume settings.

---

## 10. Asset Generation Notes

The following SVG snippets are optional references. They can be rasterized into PNGs or used directly as vector assets.

All sprites should be crisp and scalable.

## 10.1 Player

```svg
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <path
    d="M32 8 L52 32 L32 56 L12 32 Z"
    fill="#FFB84D"
    stroke="#2A1E0A"
    stroke-width="3"
    stroke-linejoin="round"
  />
</svg>
```

Add a small directional tick separately based on facing direction.

---

## 10.2 Orb

```svg
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <circle cx="32" cy="32" r="18" fill="#6BE0FF" stroke="#0B2A38" stroke-width="3"/>
  <circle cx="32" cy="32" r="18" fill="none" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="26" cy="26" r="6" fill="#FFFFFF" opacity="0.7"/>
</svg>
```

---

## 10.3 Exit Locked

```svg
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="8" y="8" width="48" height="48" rx="10" fill="#8A93A6" stroke="#1A202C" stroke-width="3"/>
  <rect x="18" y="24" width="28" height="6" rx="3" fill="#2F3744"/>
  <rect x="18" y="34" width="28" height="6" rx="3" fill="#2F3744"/>
</svg>
```

---

## 10.4 Exit Unlocked

```svg
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="8" y="8" width="48" height="48" rx="10" fill="#F5F7FA" stroke="#2A2F3A" stroke-width="3"/>
  <circle cx="32" cy="32" r="12" fill="#FFD166" stroke="#2A2F3A" stroke-width="2"/>
</svg>
```

---

## 10.5 Trail Marker

```svg
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="32" cy="32" rx="12" ry="8" fill="#E8DCC8"/>
</svg>
```

In colorblind mode, add a black outline.

---

## 10.6 Wall Segment

Horizontal wall segment. Rotate 90 degrees for vertical walls.

```svg
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="26" width="64" height="12" rx="6" fill="#1E2532"/>
  <rect x="0" y="26" width="64" height="3" rx="1.5" fill="#3A455A" opacity="0.6"/>
  <rect x="0" y="35" width="64" height="3" rx="1.5" fill="#0F141D" opacity="0.5"/>
</svg>
```

---

## 10.7 Floor Tile

```svg
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect width="64" height="64" fill="#C7D0DE"/>
</svg>
```

Add subtle noise in the final asset pipeline if desired.

---

## 10.8 Fog Tile

```svg
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect width="64" height="64" fill="#070A12"/>
</svg>
```

Add subtle static noise in the final asset pipeline if desired.

---

## 11. Integration Notes

These notes are important for the integration agent.

### 11.1 Visibility

- Use the gameplay visibility mask as the source of truth.
- Do not let visual gradients reveal extra tiles.
- Do not render orbs or exits outside the visibility mask.
- If an exit unlock animation would reveal a hidden exit, suppress the visible animation and show only toast/HUD feedback.

### 11.2 Trail

- Trail markers are visual representations of gameplay trail state.
- Trail markers must persist for the gameplay-defined lifetime.
- Trail fade stops when the game is paused.
- Trail resets on restart.

### 11.3 Pause

When paused:

- Freeze player animation.
- Freeze trail fade.
- Freeze orb/exit pulses.
- Freeze timer.
- Freeze camera.
- Darken gameplay.

### 11.4 Restart

When restarting:

- Reset player position.
- Reset trail.
- Reset orbs.
- Reset exit lock state.
- Reset timer.
- Reset toast state.
- Reset tutorial hint state for the level attempt.

### 11.5 Level 12 Flow

- Levels 1-11 use the Level Complete screen.
- Level 12 transitions directly to the Game Complete screen.
- Game Complete should still show the final level’s stars, time, and best time.

**Why:** This avoids showing two nearly identical screens at the end of the game.

### 11.6 Accessibility Settings

Colorblind mode, reduced motion, and text size should apply globally.

They should affect:

- HUD
- Gameplay
- Menus
- Toasts
- Animations
- Colors
- Focus states

They should not affect:

- Maze layout
- Light radius
- Trail lifetime
- Star times
- Level generation

**Why:** Accessibility should improve clarity without changing the challenge.

### 11.7 Audio Settings

Audio settings should persist.

They should not affect:

- Star times
- Level progression
- Gameplay timing

**Why:** Audio is presentation, not mechanics.

### 11.8 Input

The game must support:

- Keyboard
- Gamepad
- Touch

No interaction should require mouse-only input.

Pause should be available through:

- Keyboard: `Esc` or `P`
- Gamepad: `Start`
- Touch: pause button

**Why:** Pause is a core recovery action and must be accessible to all input types.

---

## 12. Important Additions and Why

These are additions beyond the bare gameplay requirements, but they are important for UX or accessibility.

### 12.1 Pause Key and Gamepad Start

**Added:** Pause via `Esc`, `P`, or gamepad `Start`.

**Why:** The player can become lost at any time. A quick pause/restart path is essential for the no-fail-state design.

### 12.2 Audio Volume Settings

**Added:** Master, music, and SFX volume sliders.

**Why:** Music and SFX are important for atmosphere, but players need control. This does not affect star fairness.

### 12.3 Trail Memory Brightness

**Added:** Trail-only visible tiles are dimmer than current light tiles.

**Why:** This helps the player distinguish current vision from fading memory without adding a meter.

### 12.4 Shape-Based Exit States

**Added:** Locked exit uses bars; unlocked exit uses an open circle.

**Why:** Color alone would fail accessibility. Shape makes the state instantly readable.

### 12.5 Direct Game Complete for Level 12

**Added:** Level 12 goes directly to Game Complete.

**Why:** A separate Level Complete screen for the final level would feel redundant.

### 12.6 Informational Input Row in Settings

**Added:** Settings shows supported inputs but does not let the player disable them.

**Why:** Forcing a single input method would reduce accessibility. All inputs should work together.

---

## 13. Cut Features and Why

These features were considered and cut.

### 13.1 No Narrative Art

**Cut because:** The maze and fading trail are the core experience. Story art would distract from the puzzle.

### 13.2 No Moving Environmental Particles

**Cut because:** Moving particles can distract from memory and reduce readability.

### 13.3 No Screen Shake

**Cut because:** The game has no fail state or combat. Shake would feel out of place and punitive.

### 13.4 No Complex Wall Textures

**Cut because:** Maze walls must be read quickly. Ornate textures would slow spatial parsing.

### 13.5 No Per-Level Entity Colors

**Cut because:** The player, orbs, and exit must remain instantly recognizable in every level.

### 13.6 No Best Time Display in Level Select

**Cut because:** Stars are enough for level select. Adding best times would clutter nodes. Best time is still shown on the timer HUD and complete screen.

### 13.7 No Act Labels in Level Select

**Cut because:** Accent colors and node progression are enough. Labels would add unnecessary text.

### 13.8 No Animated Fog

**Cut because:** Animated fog can create visual noise and imply hidden movement.

### 13.9 No Mouse-Only Interactions

**Cut because:** The game must support keyboard, gamepad, and touch equally.

### 13.10 No Audio-Only Cues

**Cut because:** Every critical event must be visible. Audio is enhancement, not requirement.

---

## 14. Final Visual Summary

*Fading Labyrinth* uses a quiet, high-contrast visual language built around light, darkness, and memory.

The player is a small amber diamond. Orbs are cyan rings. The exit is a square gate. The trail is a fading pale footprint. The maze is clean, dark, and readable.

Levels progress through subtle acts:

- Act I: pale and open.
- Act II: cooler and deeper.
- Act III: violet and dense.
- Act IV: luminous and final.

The UI is minimal but clear. The HUD shows only level, objective, timer, best time, pause, and hints. Toasts provide immediate feedback. Menus are calm, accessible, and easy to navigate.

The audio is sparse and atmospheric. Music is slow and meditative. Sound effects are short and non-essential.

The result is a coherent visual experience that supports the core fantasy: the maze erases memory, and the player must remember their way through.