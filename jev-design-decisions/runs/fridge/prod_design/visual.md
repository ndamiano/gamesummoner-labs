# visual.md

## 1. Scope and Authority

This document is authoritative for:

- Visual style.
- HUD and UX.
- World readability.
- Zone identity.
- Animation and visual feedback.
- Music.
- Sound effects.

This document does **not** override `gameplay.md`.

If a visual element would change hitboxes, timers, AI, movement, noise values, win/lose logic, or control behavior, the visual element must be adjusted or removed.

Important integration rule:

- All visual effects are presentation-only.
- All audio is presentation-only.
- Gameplay values in `gameplay.md` remain the source of truth.

---

## 2. Visual Direction

The game should feel like a **heavy, awake appliance trying to leave a normal house**.

The visual fantasy is not horror. It is domestic tension.

The house should feel familiar, warm, and slightly watchful. The fridge should feel vulnerable, alive, and electric.

### Visual Pillars

1. **Awake appliance**
   - The fridge is not a monster.
   - It has a quiet cyan “life-light” that communicates sentience, power, and state.
   - Its movement should feel bulky and deliberate.

2. **Domestic tension**
   - The house is cozy, not scary.
   - Warm wood, soft shadows, household objects, and lamp light create comfort.
   - Tension comes from people moving through that comfort.

3. **Readable stealth**
   - The player must instantly understand:
     - Where the fridge is.
     - Which way it faces.
     - Whether it is plugged in.
     - Whether its door is open.
     - How much power it has.
     - Where residents are looking.
     - Where noise went.
     - How suspicious residents are.

4. **One house, three moods**
   - Kitchen: warm, safe, occupied.
   - Hallway: constrained, neutral, transitional.
   - Living room: cooler, duskier, final.

All three zones use the same base style, but their lighting, floor tone, and furniture make them distinct.

---

## 3. Art Style

### Base Style

- 2D top-down.
- Soft vector / canvas shapes.
- Rounded corners.
- Low saturation.
- Warm domestic palette.
- 2.5D shadows for depth.
- No 3D.
- No camera rotation.
- No scrolling.
- No pixel art.
- No heavy outlines.
- No cartoon gore.
- No sci-fi UI.

### Shape Language

- Fridge: rounded rectangle with a small front face.
- Residents: soft circles with a facing indicator.
- Furniture: rounded rectangles with subtle top surfaces.
- UI: flat panels, rounded corners, keycaps.
- Effects: soft rings, glows, and short flashes.

### Readability Rules

- The fridge must always be the clearest object on screen.
- Residents must be readable even when moving.
- Danger must be readable without reading text.
- Noise must be readable as a physical event.
- The player should never need a map.

### What Is Cut by Design

| Cut Piece | Why |
|---|---|
| Minimap | The house is one screen. Objective text is enough. |
| Resident suspicion numbers | Icons and vignette are cleaner. |
| Full path lines for residents | Would reduce tension and clutter. |
| Extra non-gameplay furniture | Would clutter the small playfield. |
| Day/night cycle | One dusk mood is enough. |
| Weather | Not needed. |
| Character customization | Scope. |
| Voice lines | Abstract audio is cleaner and more universal. |
| Complex particles | The game should feel heavy, not explosive. |
| 3D models | Not needed for top-down browser stealth. |

---

## 4. Canvas, Scale, and World Layout

### Playfield

- Logical size: `1280 x 720`.
- Tile size: `32`.
- Camera: fixed.
- No scrolling.
- Scale to fit window with letterboxing if needed.
- Maintain aspect ratio.

### Visual Wall Thickness

- Visual wall thickness: `16` units.
- This is presentation only.
- Gameplay collision remains authoritative from `gameplay.md`.

### Doorways

Visual doorways should match gameplay openings:

- Kitchen to Hallway: `x = 480`, `y = 320` to `400`.
- Hallway to Living Room: `x = 800`, `y = 320` to `400`.
- Front Door: `x = 1280`, `y = 320` to `400`.

Internal doorways should have:

- A subtle door frame.
- A slightly darker threshold strip.
- No visible door panel, because the openings are open passages.

The front door should be visually distinct:

- An open doorway.
- A soft outdoor light beyond it.
- A faint threshold line at `x = 1240`, `y = 320` to `400`.

Why the threshold line exists:

- The win condition is precise.
- A faint line helps the player understand the exact escape point without adding a new mechanic.

---

## 5. Entity Scale

### Fridge

Gameplay collider:

- Length: `64`.
- Width: `32`.

Visual size:

- Length: `68`.
- Width: `36`.

The extra `2` units per side are for outline and shadow only.

Why:

- Keeps collision feel honest.
- Gives the fridge enough room for a readable face, LED, and door.

### Residents

Gameplay collider:

- Radius: `20`.

Visual size:

- Radius: `22`.

Why:

- Allows a soft shadow and outline without making residents feel larger than their hitbox.

### Layer Order

Draw in this order:

1. Floor.
2. Zone lighting overlays.
3. Object shadows.
4. Furniture and walls.
5. Outlets.
6. Noise rings.
7. Fridge and residents, sorted by `y` for subtle 2.5D depth.
8. Awareness icons.
9. Sight cones, if enabled.
10. Warning vignette.
11. HUD.

Why:

- Keeps the player’s fridge readable.
- Keeps awareness icons above entities.
- Keeps HUD always on top.

---

## 6. Color System

### Global Semantic Colors

| Purpose | Color | Hex / Value |
|---|---:|---|
| UI background | Charcoal | `#171a1c` |
| UI text | Warm white | `#f4f1ea` |
| UI secondary text | Muted sand | `#b8b3a8` |
| Panel background | Translucent charcoal | `rgba(23, 26, 28, 0.72)` |
| Panel border | Soft white | `rgba(244, 241, 234, 0.14)` |
| Fridge body | Off-white | `#eef3f4` |
| Fridge outline | Dark slate | `#3f4a4d` |
| Fridge cyan / sentience | Cool cyan | `#7bd8d6` |
| Fridge dim | Muted teal | `#4f6d6f` |
| Power high | Soft green | `#8fe388` |
| Power medium | Amber | `#f4b942` |
| Power low | Red | `#e14b4b` |
| Danger | Red | `#e14b4b` |
| Noise small | Warm white | `#fff7e0` |
| Noise medium | Amber | `#f4b942` |
| Noise loud | Orange-red | `#ff7a59` |
| Hum | Cyan | `#7bd8d6` |
| Shadow | Soft brown-black | `rgba(25, 20, 18, 0.18)` |

### Color Rules

- Red is reserved for danger:
  - Low power.
  - High suspicion.
  - Vignette.
  - Lose state.
- Cyan is the fridge’s identity:
  - LED.
  - Plug state.
  - Hum.
  - Door open glow.
- Amber is used for medium warnings:
  - Medium noise.
  - Suspicion.
  - Timer warning.
- Green is used only for healthy power.
- Do not use red and green as the only distinction anywhere. Always pair color with shape, icon, or motion.

---

## 7. Zone Identity

The house is one continuous level, but each room should feel distinct.

All zones share:

- The same wall base style.
- The same shadow language.
- The same UI palette.
- The same soft rounded furniture style.

They differ in:

- Floor tone.
- Lighting temperature.
- Furniture.
- Mood.

---

### 7.1 Kitchen

**Mood:**  
Safe, warm, occupied.

**Visual identity:**  
Light wood, cream counters, stainless steel, warm lamp light.

**Palette:**

| Element | Color |
|---|---|
| Floor base | `#e3d3bd` |
| Floor line | `#c9b79d` |
| Floor accent | `#d8c7ae` |
| Wall | `#d9c7a9` |
| Baseboard | `#8a7b68` |
| Counter top | `#cfc4b3` |
| Cabinet | `#8a7b68` |
| Steel | `#aeb6b8` |
| Dark steel | `#3f4a4d` |
| Lamp glow | `#ffdf9e` at `0.08` alpha |

**Visual notes:**

- The kitchen should be the brightest room.
- Use a soft warm radial glow around the counter area.
- Counters should read as tall furniture from above.
- The sink and stove should be clearly metallic.
- The fridge start position should feel normal: it is plugged in and sitting in the kitchen.

**Why:**

- The kitchen is the tutorial and starting safe zone.
- It should feel calm enough to learn controls, but still occupied by Mom.

---

### 7.2 Hallway

**Mood:**  
Constrained, neutral, transitional.

**Visual identity:**  
Narrow passage, runner rug, small plant, shoe rack, cooler shadows.

**Palette:**

| Element | Color |
|---|---|
| Floor base | `#cbb9a2` |
| Floor line | `#b5a28b` |
| Floor accent | `#d8c7ae` |
| Runner rug | `#8a6f5c` |
| Runner pattern | `#d9c7a9` |
| Wall | `#cbb9a2` |
| Baseboard | `#7b6a55` |
| Plant leaves | `#6d8b6a` |
| Plant pot | `#a86f4f` |
| Shoe rack | `#7b6a55` |
| Shoe colors | `#4f6d8a`, `#b56a7a`, `#d8a44a` |
| Light | `#f2ead9` at `0.07` alpha |

**Visual notes:**

- The hallway should feel narrower than the other rooms.
- Use a long runner rug to guide the eye from kitchen to living room.
- The plant and shoe rack should be clearly solid.
- Shadows should be slightly cooler than in the kitchen.

**Why:**

- The hallway is the middle pressure zone.
- It should feel tighter and more exposed.
- The rug gives a subtle visual path without adding an arrow.

---

### 7.3 Living Room

**Mood:**  
Duskier, final, more exposed.

**Visual identity:**  
Cooler floor, blue-grey rug, dark TV, lamp light, front door light.

**Palette:**

| Element | Color |
|---|---|
| Floor base | `#b7a994` |
| Floor line | `#9f8f7a` |
| Floor accent | `#c7b8a3` |
| Rug | `#6d7b8c` |
| Rug pattern | `#a9b7c4` |
| Wall | `#b8c2c9` |
| Baseboard | `#4a4038` |
| Sofa | `#7d6f8a` |
| Sofa cushion | `#9a8aa5` |
| Coffee table | `#8a6f5c` |
| TV stand | `#4a4038` |
| TV screen | `#171a1c` |
| Bookshelf | `#6d5b4a` |
| Book colors | `#b56a7a`, `#6d8ba8`, `#d8a44a`, `#6d8b6a` |
| Dusk overlay | `#203040` at `0.08` alpha |
| Lamp glow | `#ffcf8a` at `0.10` alpha |

**Visual notes:**

- The living room should feel cooler and darker.
- The front door should glow softly.
- The TV should be off, dark, and slightly reflective.
- The rug should make the center of the room feel open but visually bounded.
- The bookshelf should contain muted colored books, matching resident colors.

**Why:**

- This is the final room.
- It should feel closer to escape, but also more exposed.
- The cooler lighting increases tension without changing gameplay.

---

## 8. Fridge Visuals

The fridge is the player character.

It must always be readable as:

- A fridge.
- A character.
- A powered machine.
- A vulnerable object.

### 8.1 Base Fridge Sprite

Local orientation:

- Facing direction is `+x` in local space.
- The fridge’s “face” is the short front edge in the direction it is facing.
- The door is on the front face.

Base sprite:

- Rounded rectangle.
- Off-white body.
- Dark slate outline.
- Vertical seam near the front.
- Small front face panel.
- One cyan LED “eye” near the front.
- Soft shadow offset down-right.

Why the door is on the front face:

- This makes facing direction obvious.
- It makes door state obvious.
- It gives the fridge a simple character face without becoming a monster.

### 8.2 Fridge LED

The LED is the fridge’s sentience indicator.

| State | LED Color | Behavior |
|---|---|---|
| Plugged | Bright cyan | Steady, slight pulse every 2 seconds |
| Unplugged, healthy power | Muted teal | Dimmer, steady |
| Low power | Flickering red/teal | Flickers at 0.5 Hz |
| Power depleted | Dark grey | Off |
| Humming | Bright cyan | Flashes 3 times over 0.3 seconds |
| Caught | Red | Flashes once, then dark |

Why:

- The LED gives the fridge identity.
- It communicates power state without relying only on the HUD.

---

### 8.3 Cord and Plug State

The fridge has a power cord.

When plugged:

- A cable connects the fridge to the plugged outlet.
- The cable is dark slate with a thin cyan core.
- The outlet glows cyan.
- A small power pulse travels along the cable every 2 seconds.

When unplugged:

- The cable dangles from the rear of the fridge.
- The cable is dark slate with no cyan core.
- The outlet does not glow unless the fridge is in plug range.

Why:

- Plug state is a core mechanic.
- The cable makes it obvious whether the fridge is connected to the house.

---

### 8.4 Plug Range Visual

When the fridge is unplugged and within `48` units of an outlet:

- The outlet glows cyan.
- A faint dashed cyan circle appears around the outlet.
- Circle radius: `48`.
- Alpha: `0.25`.
- Line width: `2`.
- Dashed pattern: `6, 6`.

Why:

- The plug radius is not obvious from the outlet size alone.
- This helps the player find recharge points quickly.

---

### 8.5 Plug Connection Progress

Plug connection takes `0.5` seconds.

Visual:

- A cyan arc fills around the fridge.
- Arc radius: `26`.
- Start angle: `-90 degrees`.
- Fill duration: `0.5` seconds.
- Line width: `3`.
- Color: `#7bd8d6`.

If the plug attempt is interrupted:

- The arc resets.
- The cable snaps back to the unplugged state.
- No success sound or flash plays.

Why:

- The player needs clear feedback that the plug is not instant.
- Interruption should be visually obvious.

---

### 8.6 Door State

Door closed:

- Front face panel is flush with the body.
- No light spill.

Door open:

- The front face panel swings outward.
- Interior light spills forward.
- The LED becomes brighter.
- A soft cyan glow appears around the open door.

Door animation:

- Open: `0.2` seconds.
- Close: `0.2` seconds.
- Easing: ease-out.

Light spill:

- Shape: soft trapezoid extending forward from the door.
- Length: `40` units.
- Width at far edge: `32` units.
- Color: cyan.
- Alpha: `0.25`.

Why:

- Door state is a core mechanic.
- The light spill makes the fridge more noticeable, matching gameplay suspicion.

---

### 8.7 Movement Visuals

#### Waddling

When the fridge waddles:

- Slight squash and stretch.
  - Forward scale: `1.02`.
  - Side scale: `0.98`.
- Shadow shifts slightly opposite movement.
- Small dust puff appears behind the fridge every `0.6` seconds.
  - Dust color: warm grey.
  - Alpha: `0.2`.
  - Lifetime: `0.3` seconds.

Why:

- Waddling should feel heavy and quiet.
- Dust puffs make steps readable without adding particles everywhere.

#### Sliding

When the fridge slides:

- Motion streaks appear behind it.
  - 3 streaks.
  - Length: `30` units.
  - Alpha: `0.3`.
  - Lifetime: `0.2` seconds.
- Scuff marks appear on the floor.
  - 2 dark lines.
  - Alpha: `0.25`.
  - Lifetime: `1` second.
- Shadow stretches slightly in the direction of movement.
- A loud noise ring appears.

Why:

- Sliding is fast, heavy, and loud.
- The visual should communicate speed and noise immediately.

#### Collision

If the fridge collides with an object at impact speed greater than `30`:

- White flash on fridge for `0.05` seconds.
- Small screen shake:
  - Magnitude: `2` pixels.
  - Duration: `0.1` seconds.
- Impact noise ring appears.

If impact speed is lower:

- No flash.
- No shake.
- No noise.

Why:

- Minor bumps should not feel as dangerous as hard collisions.

---

### 8.8 Cooldown Visuals

The player needs to understand slide and hum cooldowns.

Use small arcs around the fridge:

| Cooldown | Color | Radius | Duration |
|---|---|---:|---:|
| Slide cooldown | White | `26` | `0.6` seconds |
| Hum cooldown | Cyan | `26` | `3` seconds |

Behavior:

- Arc fills clockwise.
- When complete, the arc disappears.
- If both are active, draw the slide arc slightly inside the hum arc.

Why:

- Cooldowns are core to risk/reward.
- The player should not need to guess whether slide or hum is available.

---

### 8.9 Low Power Visuals

When power is below `25`:

- Fridge body desaturates slightly.
- LED flickers.
- Power bar flashes red.
- A low buzz sound plays periodically.

When power is below `10`:

- LED becomes mostly red.
- Fridge outline darkens.
- Movement visual squash becomes slightly weaker.

Why:

- Low power should feel like the fridge is dying.
- It should be obvious before the player fails.

---

### 8.10 Fridge State Transitions

| Event | Visual |
|---|---|
| Game starts | LED fades in over `0.5` seconds |
| Unplug | Cable snaps free, small grey pop ring |
| Plug success | Cyan flash, cable connects, outlet glows |
| Door open | Panel swings, cyan light spill |
| Door close | Panel swings back, light fades |
| Hum | Cyan pulse, LED flash, large ring |
| Caught | Red flash, freeze for `0.2` seconds, cord yank |
| Power depleted | LED dies, body greys out, desaturate |
| Win | Door light expands, screen brightens |

---

## 9. Resident Visuals

Residents are the main threat.

They should feel like normal people, not monsters.

### 9.1 Base Resident Sprite

Residents are top-down circles.

Base:

- Circle radius: `22` visual.
- Soft shadow offset down-right.
- Dark slate outline.
- A small facing indicator in the direction they are looking.
- Slight body bob while moving.

Facing indicator:

- A small light dot or wedge near the edge of the circle.
- It should make the resident’s view direction obvious.

Why:

- The player needs to know which way residents are looking.
- The indicator should be subtle but readable.

---

### 9.2 Resident Distinction

All residents use the same collider and AI, but they must be visually distinct.

| Resident | Color | Visual Detail |
|---|---|---|
| Mom | Muted rose `#b56a7a` | Small bun / hair detail |
| Dad | Slate blue `#6d8ba8` | Broader shoulder shading |
| Kid | Mustard `#d8a44a` | Small backpack dot |

Do not make the kid visually much smaller than the others.

Why:

- The collider is the same size for all residents.
- Visual size should not mislead the player about threat range.

---

### 9.3 Resident Spawn

Residents appear at:

- Mom: `5` seconds.
- Dad: `10` seconds.
- Kid: `20` seconds.

Visual:

- Fade in over `0.3` seconds.
- Slight scale from `0.9` to `1.0`.

Why:

- Avoids abrupt pop-in.
- Keeps the first 5 seconds calm.

---

### 9.4 Resident States

#### Routine

- Normal walk cycle.
- Faces movement direction.
- No awareness icon.
- Sight cone is faint.

#### Suspicious

- Stops moving.
- Faces the fridge.
- Eye icon appears above head.
- Eye icon opacity equals `suspicion / 100`.
- Sight cone brightens slightly.
- Body outline may get a subtle amber tint.

Why:

- Suspicious is the warning state.
- The player should see it before full investigation.

#### Investigate

- Moves faster.
- Exclamation icon replaces eye icon.
- Sight cone becomes sharper and slightly amber.
- Shadow gets a faint red tint.
- Stride animation is faster.

Why:

- Investigation is the high-danger state.
- It should feel urgent.

#### Search

- Resident stops at target.
- Slowly rotates in place.
- A soft scanning arc may rotate with them.
- Awareness icon fades out.

Why:

- Search is a recovery state.
- It should feel like the resident is losing track.

---

## 10. Resident Sight Cones

Residents have a view radius of `160` and a field of view of `120` degrees.

Show a subtle sight cone for each active resident.

### Cone Settings

| State | Alpha | Color |
|---|---:|---|
| Routine | `0.06` | Warm white `#fff7e0` |
| Suspicious | `0.10` | Warm white `#fff7e0` |
| Investigate | `0.14` | Amber `#f4b942` |
| Search | `0.08` | Warm white `#fff7e0` |

### Cone Shape

- Radius: `160`.
- Field of view: `120` degrees.
- Origin: resident center.
- Direction: resident facing angle.

### Cone Clipping

Sight cones must be clipped by blocking walls and furniture.

Use the same blocking logic as gameplay line of sight.

If performance is a concern:

- Pre-render a walkable mask.
- Draw the cone to an offscreen canvas.
- Mask it with the walkable layer.

Why:

- FOV is core to stealth.
- The player needs to understand where they can be seen.
- Cones that pass through furniture would be misleading.

### Fallback

If cones are too expensive:

- Replace cones with a stronger directional indicator on residents.
- Keep awareness icons and suspicion vignette.

Why:

- Readability of resident vision is more important than cone aesthetics.

---

## 11. Awareness Icons

Above each resident, display awareness.

### Suspicion 0

- No icon.

### Suspicion 1 to 99

- Eye icon.
- Opacity equals `suspicion / 100`.
- Color: amber.
- Size: `16 x 10`.
- Position: `24` units above resident center.

### Suspicion 100

- Exclamation icon.
- Color: red.
- Size: `16 x 16`.
- Position: `24` units above resident center.
- Small pop scale from `1.2` to `1.0` over `0.15` seconds.

Why:

- The player needs a direct, per-resident warning.
- The icon should be readable even when the resident is moving.

---

## 12. Noise Visuals

Noise is event-based.

Every noise event should display a brief expanding ring.

### General Ring Rules

- Rings expand from the source.
- Ring radius equals the noise radius.
- Rings fade quickly.
- Ring alpha is reduced by `0.5` for each room boundary crossed.
- Hum rings are visibly larger and more distinct.

Why:

- The player needs to understand noise propagation.
- Room boundaries reduce noise, so the visual should suggest that reduction.

---

### Noise Ring Table

| Noise Source | Radius | Color | Duration | Line Width | Notes |
|---|---:|---|---:|---:|---|
| Waddle step | `12` | Warm white | `0.35` seconds | `2` | Small, frequent |
| Plug connection | `10` | Warm white | `0.25` seconds | `2` | Very small |
| Door toggle | `15` | Warm white | `0.30` seconds | `2` | Small |
| Unplug | `20` | Amber | `0.35` seconds | `3` | Medium |
| Collision | `25` | Amber | `0.35` seconds | `3` | Medium |
| Slide | `50` | Orange-red | `0.45` seconds | `4` | Loud |
| Hum | `160` | Cyan | `0.70` seconds | `5` | Very loud |

### Hum Ring

Hum should be unmistakable.

- Cyan color.
- Larger radius.
- Longer duration.
- Slight glow.
- LED flashes.
- Door light pulse.

Why:

- Hum is a major player action.
- It should feel like a big, deliberate noise.

---

### Hearing Ticks

When a resident hears a noise:

- A small white dot appears above the resident’s head.
- Duration: `0.2` seconds.
- Size: `4` units.
- It should appear in addition to the awareness icon.

Why:

- The player should understand exactly which residents heard the noise.
- This makes noise propagation readable without path lines.

---

## 13. Warning Vignette

When any resident has suspicion above `50`:

- Show a red screen-edge vignette.

### Vignette Formula

Let `maxSuspicion` be the highest resident suspicion.

If `maxSuspicion <= 50`:

- No vignette.

If `maxSuspicion > 50`:

- Base alpha:

```text
alpha = ((maxSuspicion - 50) / 50) * 0.45
```

At `100`:

- Add a subtle pulse:
  - Pulse amplitude: `0.05`.
  - Pulse frequency: `1` Hz.

### Visual

- Radial gradient.
- Center transparent.
- Edges red `#e14b4b`.
- No full-screen red tint.

Why:

- The vignette gives emotional pressure.
- It warns the player without requiring them to track every resident icon.

---

## 14. HUD Design

The HUD must communicate:

- Objective.
- Time remaining.
- Power.
- Plug state.
- Door state.
- Contextual prompts.
- Optional controls reminder.

The HUD should be clean, domestic, and readable.

No clutter.

---

### 14.1 HUD Layout

Use the playfield as reference:

| HUD Section | Position |
|---|---|
| Objective | Top-left |
| Escape timer | Top-center |
| Power / plug / door | Top-right |
| Contextual prompt | Bottom-left |
| Controls reminder | Bottom-right |

Suggested layout:

- Objective panel: `x = 16`, `y = 16`, `w = 260`, `h = 44`.
- Timer: centered at `x = 640`, `y = 24`.
- Top-right panel: `x = 1000`, `y = 16`, `w = 264`, `h = 64`.
- Contextual prompt: `x = 16`, `y = 656`, `w = 360`, `h = 40`.
- Controls reminder: `x = 1040`, `y = 656`, `w = 224`, `h = 40`.

These are recommended, not gameplay constraints.

---

### 14.2 Typography

Use system fonts to avoid external loading.

Suggested stack:

```css
font-family: "Trebuchet MS", "Segoe UI", Arial, sans-serif;
```

For timer:

```css
font-family: "Courier New", monospace;
```

Sizes:

| Element | Size |
|---|---:|
| Title | `64px` |
| Subtitle | `20px` |
| Objective | `18px` |
| Timer | `32px` |
| HUD labels | `14px` |
| Prompt text | `16px` |
| Button text | `18px` |

---

### 14.3 Objective Text

Top-left.

Display the current objective from `gameplay.md`:

- “Unplug and leave.”
- “Leave the kitchen.”
- “Cross the hallway.”
- “Reach the front door.”

Style:

- Warm white text.
- Small room icon to the left.
- Panel background.

Room icons:

| Room | Icon |
|---|---|
| Kitchen | Small pot or fork |
| Hallway | Small runner rug |
| Living room | Small door |

Why:

- The icon gives a subtle spatial cue.
- The text remains the primary objective.

---

### 14.4 Escape Timer

Top-center.

Display seconds remaining.

Normal:

- Warm white.
- Monospace.
- Stable.

Warning below `30` seconds:

- Red.
- Pulse scale from `1.0` to `1.05` at `1` Hz.
- Optional faint red glow.

Why:

- The timer is constant pressure.
- The warning should be obvious but not panic-inducing.

---

### 14.5 Power Bar

Top-right.

Bar:

- Width: `140`.
- Height: `12`.
- Rounded corners.
- Background: translucent white.
- Fill: semantic power color.

Power colors:

| Power | Color |
|---|---|
| 25 to 100 | Green `#8fe388` |
| 10 to 24 | Amber `#f4b942` |
| 0 to 9 | Red `#e14b4b` |

Below `25`:

- Bar flashes red at `1` Hz.
- Fridge LED flickers.
- Low power buzz plays.

Why:

- Power is a core resource.
- The player should see danger before failure.

---

### 14.6 Plug Icon

Top-right.

Shows plug state.

Plugged:

- Cyan plug icon.
- Small lightning mark.
- Slight glow.

Unplugged:

- Grey plug icon.
- No glow.

Why:

- Plug state is critical.
- The icon should be readable at a glance.

---

### 14.7 Door Icon

Top-right.

Shows door state.

Closed:

- Grey door outline.

Open:

- Cyan door outline.
- Small light spill inside icon.

Why:

- Door state affects suspicion and hum.
- It should be visible without looking at the fridge.

---

### 14.8 Contextual Prompt

Bottom-left.

Show one prompt at a time.

Style:

- Keycap boxes for keys.
- Short sentence.
- Fade in: `0.15` seconds.
- Fade out: `0.2` seconds.

Examples:

- “Press P to unplug.”
- “Press P to plug in and recharge.”
- “Press E to open your door.”
- “Press Q to hum.”
- “Press Space to slide. It is loud.”
- “No outlet nearby.”
- “Open your door to hum.”
- “Not enough power to hum.”
- “Not enough power to slide.”

Prompt priority:

1. Error prompt.
2. Plug-state prompt.
3. Tutorial prompt.
4. Idle prompt.

Why:

- Only one instruction should be active at a time.
- Errors should override tutorial text.

---

### 14.9 Tutorial Prompts

Tutorial prompts appear contextually and do not block input.

Suggested sequence:

| Prompt | Trigger |
|---|---|
| “You are awake. You need to leave.” | When Playing starts, show for `2.5` seconds |
| “Press P to unplug.” | While plugged at start |
| “W/S: waddle. A/D: turn.” | After unplugging, show for `4` seconds or until first meaningful movement |
| “Space: slide. Fast, but loud.” | After movement prompt, show for `3` seconds or until first slide |
| “E: open/close door. Q: hum. Hum lures residents.” | When door first opens, or `30` seconds after start if not shown |
| “Reach the front door before time runs out.” | When fridge enters hallway, or `45` seconds after start |

Why:

- The player learns only when relevant.
- The first 5 seconds remain calm.

---

### 14.10 Controls Reminder

Bottom-right.

Optional but recommended.

Initial:

- Full opacity for first `10` seconds.
- Then fades to `30%` opacity.
- Reappears at full opacity while paused.

Suggested compact text:

```text
WASD move · Space slide · E door · Q hum · P plug
```

Why:

- New players need controls available.
- Experienced players should not be distracted by a full control list.

---

## 15. UI Components

### Panels

- Background: `rgba(23, 26, 28, 0.72)`.
- Border: `1px` or `2px`, `rgba(244, 241, 234, 0.14)`.
- Corner radius: `10`.
- Padding: `12`.

### Buttons

Primary button:

- Background: amber `#f4b942`.
- Text: charcoal `#171a1c`.
- Corner radius: `10`.
- Padding: `12 x 24`.
- Hover: brighten by `10%`.
- Focus: cyan outline `#7bd8d6`, width `3`.

Secondary button:

- Background: translucent white.
- Text: warm white.
- Border: soft white.
- Focus: cyan outline.

### Keycaps

- Size: `24 x 24`.
- Background: `rgba(255, 255, 255, 0.08)`.
- Border: `1px`, `rgba(244, 241, 234, 0.25)`.
- Text: warm white.
- Corner radius: `6`.

Why:

- Keycaps make controls instantly readable.
- They keep the UI from feeling like a manual.

---

## 16. Game State Visuals

## 16.1 Start State

### Background

- Dimmed kitchen top-down view.
- Soft vignette.
- Fridge visible at start position.
- No residents.

### Layout

- Title: “Fridge Escape”.
- Subtitle: “You are awake. Leave before the movers arrive.”
- Play button.
- Controls list.

### Title Style

- Large bold warm white.
- Cyan underline or cyan LED accent.
- Slight letter spacing.

### Controls List

Show all controls:

| Key | Action |
|---|---|
| W / Up | Waddle forward |
| S / Down | Waddle backward |
| A / Left | Turn left |
| D / Right | Turn right |
| Space | Slide |
| E | Open or close door |
| Q | Hum |
| P | Plug or unplug |
| Escape | Pause |

Why:

- The start screen must establish premise and controls before pressure begins.

---

## 16.2 Playing State

- HUD visible.
- World active.
- Tutorial prompts appear.
- Residents spawn according to gameplay.
- Noise, awareness, and vignette systems active.

---

## 16.3 Paused State

Trigger:

- Escape.
- Browser tab hidden.

Visual:

- Dark overlay.
- World stops.
- Timer stops.
- Residents stop.
- Fridge stops.
- Noise effects stop.

Overlay content:

- “Paused”
- Resume button.
- Restart button.
- Controls list.

Why:

- Pause should feel like stepping out of the house, not leaving the game.

---

## 16.4 Win State

Trigger:

- Fridge center enters front door threshold.

Visual sequence:

1. Fridge crosses threshold.
2. Front door light expands.
3. Screen brightens.
4. Soft win jingle plays.
5. Win panel fades in.

Win panel content:

- “You escaped.”
- Time used.
- Noise events created.
- Residents lured.
- Play Again button.

Style:

- Brighter than lose.
- Warm white text.
- Cyan accent.
- No confetti.
- No excessive celebration.

Why:

- Winning should feel like relief, not spectacle.

---

## 16.5 Lose State

Lose reasons:

| Reason | Text |
|---|---|
| Caught | “You got unplugged.” |
| Power depleted | “Your hum faded.” |
| Timer expired | “The movers arrived.” |

General lose visual:

- Red vignette.
- Desaturate world.
- Dark overlay.
- Lose text.
- Retry button.

### Caught

- Red flash.
- Freeze frame for `0.2` seconds.
- Resident overlaps fridge.
- Cord yank visual.
- Screen shake: `4` pixels for `0.2` seconds.

Why:

- The player should clearly understand they were caught.

### Power Depleted

- Fridge LED dies.
- Fridge body greys out.
- Hum sound fades.
- Screen slowly desaturates.

Why:

- The player should understand the fridge lost power.

### Timer Expired

- Front door light flares orange.
- Optional faint mover silhouette at the door.
- Red vignette intensifies.

Why:

- The player should understand the movers arrived.

---

## 17. Animation and Feel

The game should feel heavy, tense, and deliberate.

### Animation Principles

- Short, quiet animations for normal movement.
- Larger, louder animations for risky actions.
- No excessive screen shake.
- No fast strobing.
- No particle explosions.

### Timing

| Animation | Duration |
|---|---:|
| Door open/close | `0.2` seconds |
| Plug connection | `0.5` seconds |
| Slide | `0.25` seconds |
| Waddle step puff | `0.3` seconds |
| Noise ring | `0.25` to `0.7` seconds |
| Awareness icon pop | `0.15` seconds |
| State transition | `0.2` seconds |
| Win transition | `0.8` seconds |
| Lose transition | `0.6` seconds |

### Screen Shake

Use minimal shake:

| Event | Magnitude | Duration |
|---|---:|---:|
| Hard collision | `2` pixels | `0.1` seconds |
| Caught | `4` pixels | `0.2` seconds |

Why:

- Shake should communicate impact, not chaos.

---

## 18. Music Design

The music should feel like a house at dusk.

It should not be horror music. It should be domestic, uneasy, and quiet.

### Musical Identity

- Style: ambient domestic tension.
- Tempo: `72 BPM`.
- Base key: D minor.
- Win key: F major.
- Lose: unresolved D minor.
- Instruments:
  - Soft felt piano.
  - Low sine hum.
  - Sub pulse.
  - Sparse string drone.
  - Filtered noise shimmer.
  - Clock tick.

### Music Philosophy

- The music should support stealth, not dominate it.
- SFX must remain clearly audible.
- Music layers should increase as the player moves through the house.
- Suspicion should add tension without becoming annoying.

---

### Music Layers

| Layer | Used When | Sound | Gain |
|---|---|---|---:|
| House hum | Playing | 55 Hz sine + 110 Hz sine, low-passed | `0.10` |
| Kitchen piano | Kitchen | Soft felt piano notes: D3, A3, F4, E4 | `0.22` |
| Hallway pulse | Hallway | 40 Hz sub pulse on beats 1 and 3 | `0.08` |
| Living room drone | Living room | D2 string drone + pulse every beat | `0.10` |
| Tension shimmer | Max suspicion > 50 | Filtered noise + high string, gain scales with suspicion | `0` to `0.12` |
| Timer tick | Timer < 30 | 1800 Hz square tick every second | `0.08` |
| Win jingle | Win | F4, A4, C5, F5 soft triangle notes | `0.35` |
| Lose sting | Lose | Detuned 110 Hz dropping to 90 Hz, low-passed | `0.35` |

### Dynamic Mixing

- Start screen:
  - House hum.
  - Very sparse piano.
  - Low volume.

- Kitchen:
  - House hum.
  - Soft piano.
  - No pulse.

- Hallway:
  - House hum.
  - Piano slightly darker.
  - Add sub pulse.

- Living room:
  - House hum.
  - Piano darker.
  - Add string drone.
  - Pulse stronger.

- Suspicion:
  - When max suspicion > 50:
    - Add tension shimmer.
    - Gain scales from `0` to `0.12`.

- Timer warning:
  - When timer < 30:
    - Add tick layer.

- Win:
  - Stop tension.
  - Crossfade to F major jingle.

- Lose:
  - Stop music loop.
  - Play lose sting.

### Crossfades

- Room changes: `1` second crossfade.
- State changes: `0.5` second crossfade.
- Win/lose: `0.3` second stop + jingle/sting.

Why:

- The player should feel the house change without sudden audio jumps.

---

## 19. Sound Effects

Sound effects must communicate:

- Movement.
- Noise.
- Power.
- Door.
- Resident awareness.
- Timer pressure.
- Win/lose.

All SFX should be short, clean, and procedural-friendly.

No voices.

No copyrighted samples.

---

### SFX Table

| Event | Trigger | Sound Design | Duration | Volume | Notes |
|---|---|---|---:|---:|---|
| Waddle loop | Every `0.6` seconds while speed > `10` | Low thump + soft scuff | `0.08` seconds | `0.22` | 80 Hz sine + filtered noise, low-pass around `300 Hz` |
| Slide burst | Slide start | Heavy rubber slide | `0.25` seconds | `0.55` | 50 Hz sine + noise sweep from `300 Hz` to `80 Hz` |
| Collision | Impact speed > `30` | Short thump | `0.08` seconds | `0.35` | Pitch varies slightly with impact speed |
| Plug connection | Plug starts | Click + soft electrical tick | `0.12` seconds | `0.30` | 1200 Hz click + 200 Hz hum |
| Unplug | Unplug | Clunk + click | `0.12` seconds | `0.45` | 70 Hz thump + 900 Hz click |
| Door open | Door opens | Soft hinge creak | `0.18` seconds | `0.30` | Band-passed noise + 180 Hz sine |
| Door close | Door closes | Soft thud + click | `0.08` seconds | `0.35` | 90 Hz thump + 600 Hz click |
| Hum | Hum action | Low fridge hum | `0.80` seconds | `0.50` | 55 Hz + 110 Hz sine, 5 Hz vibrato |
| Resident suspicion | Awareness icon appears | Soft alert ping | `0.05` seconds | `0.15` | 880 Hz sine, very quiet |
| Resident investigate | Resident enters Investigate | Sharper double ping | `0.10` seconds | `0.25` | 1320 Hz + 1760 Hz |
| Timer warning | Timer < 30 | Clock tick every second | `0.02` seconds | `0.10` | 1800 Hz square |
| Power warning | Power < 25 | Low buzz | `0.20` seconds | `0.15` | 60 Hz square, periodic |
| Win jingle | Win | Soft bell notes | `0.80` seconds | `0.40` | F4, A4, C5, F5 |
| Lose sting | Lose | Detuned drop | `0.60` seconds | `0.40` | 110 Hz dropping to 90 Hz |

---

### SFX Mixing

Suggested master mix:

| Bus | Gain |
|---|---:|
| Master | `0.80` |
| Music | `0.35` |
| SFX | `0.65` |
| UI | `0.50` |

Rules:

- Loud SFX should briefly duck music by about `-6 dB`.
- Waddle steps should never overpower resident awareness pings.
- Hum should be clearly louder than waddling.
- Timer ticks should be subtle but persistent.
- Lose sting should cut through music immediately.

Why:

- The player needs to hear awareness cues even during movement.
- Music should create mood, not compete with gameplay audio.

---

## 20. Accessibility and Readability

### Colorblind Support

Do not rely on color alone.

- Power bar uses length plus color.
- Danger uses red plus exclamation icons and vignette.
- Noise uses size, color, and ring shape.
- Plug state uses icon shape plus color.
- Door state uses icon shape plus color.

### Contrast

- UI text: `#f4f1ea` on `#171a1c`.
- This should maintain high contrast.
- Secondary text should remain readable but less prominent.

### Motion

- No strobe effects above `3` flashes per second.
- Timer pulse: `1` Hz.
- Vignette pulse: `1` Hz.
- Screen shake is small.
- No full-screen flashing.

### Audio

All critical information must also be visual:

- Suspicion.
- Noise.
- Power.
- Timer.
- Plug state.
- Door state.
- Win/lose.

Audio enhances the experience but is never the only channel.

### Input Accessibility

- Buttons should be keyboard accessible.
- Focus state should be visible.
- Enter or Space can activate the focused start-screen button.
- Escape pauses during play.

---

## 21. Asset Checklist

### World

- Kitchen floor tile.
- Hallway floor tile.
- Hallway runner rug.
- Living room floor tile.
- Living room rug.
- Wall segment.
- Internal doorway frame.
- Front door opening.
- Outside light beyond front door.
- Kitchen counter.
- Kitchen sink.
- Kitchen stove.
- Potted plant.
- Shoe rack.
- Sofa.
- Coffee table.
- TV stand.
- TV screen.
- Bookshelf.
- Outlets.
- Outlet glow.
- Plug range indicator.
- Front door threshold line.
- Zone lighting overlays.
- Shadows.

### Fridge

- Fridge base sprite.
- Fridge shadow.
- Fridge LED.
- Fridge door closed.
- Fridge door open.
- Fridge interior light spill.
- Plugged cord.
- Unplugged cord.
- Plug connection arc.
- Slide motion streaks.
- Slide scuff marks.
- Waddle dust puff.
- Collision flash.
- Low power desaturation.
- Caught red flash.
- Win light expansion.

### Residents

- Mom base sprite.
- Dad base sprite.
- Kid base sprite.
- Resident shadow.
- Resident facing indicator.
- Routine walk animation.
- Suspicious stop animation.
- Investigate fast walk animation.
- Search scan animation.
- Eye icon.
- Exclamation icon.
- Hearing tick.
- Sight cone.

### FX

- Noise rings.
- Hum ring.
- Plug success flash.
- Unplug pop ring.
- Door open/close glow.
- Warning vignette.
- Timer warning pulse.
- Power warning flash.
- State transition fades.
- Win brighten.
- Lose desaturate.

### UI

- Title screen background.
- Title text.
- Subtitle text.
- Play button.
- Resume button.
- Restart button.
- Retry button.
- Play Again button.
- Objective panel.
- Room icons.
- Timer.
- Power bar.
- Plug icon.
- Door icon.
- Contextual prompt panel.
- Keycaps.
- Controls reminder.
- Win panel.
- Lose panel.
- Pause overlay.

### Audio

- Music layers.
- SFX from table above.
- Win jingle.
- Lose sting.
- UI hover/click sounds, optional.

---

## 22. Optional Procedural Generation Reference

This section is optional. It provides reference values and simple code patterns for generating assets procedurally if no external art is available.

It is not required to match this code exactly. The visual goals above are authoritative.

### 22.1 Palette Constants

```js
const V = {
  panel: 'rgba(23, 26, 28, 0.72)',
  panelBorder: 'rgba(244, 241, 234, 0.14)',
  text: '#f4f1ea',
  subtext: '#b8b3a8',
  cyan: '#7bd8d6',
  green: '#8fe388',
  amber: '#f4b942',
  red: '#e14b4b',
  outline: '#3f4a4d',
  shadow: 'rgba(25, 20, 18, 0.18)',
  noiseSmall: '#fff7e0',
  noiseMedium: '#f4b942',
  noiseLoud: '#ff7a59'
};
```

### 22.2 Rounded Rectangle Helper

```js
function rr(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}
```

### 22.3 Floor Tile Generator

```js
function makeFloorTile(base, line, accent) {
  const c = document.createElement('canvas');
  c.width = 32;
  c.height = 32;

  const g = c.getContext('2d');

  g.fillStyle = base;
  g.fillRect(0, 0, 32, 32);

  g.globalAlpha = 0.08;
  for (let i = 0; i < 10; i++) {
    g.fillStyle = Math.random() > 0.5 ? accent : line;
    g.fillRect(
      Math.floor(Math.random() * 30),
      Math.floor(Math.random() * 30),
      2,
      2
    );
  }

  g.globalAlpha = 0.16;
  g.strokeStyle = line;
  g.lineWidth = 1;
  g.strokeRect(0.5, 0.5, 31, 31);

  g.globalAlpha = 1;
  return c;
}
```

Example usage:

```js
const kitchenFloor = makeFloorTile('#e3d3bd', '#c9b79d', '#d8c7ae');
const hallwayFloor = makeFloorTile('#cbb9a2', '#b5a28b', '#d8c7ae');
const livingFloor = makeFloorTile('#b7a994', '#9f8f7a', '#c7b8a3');
```

### 22.4 Fridge Sprite Reference

```js
function drawFridge(ctx, x, y, angle, o = {}) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(angle);

  // Shadow
  ctx.fillStyle = V.shadow;
  rr(ctx, -32 + 3, -16 + 5, 64, 32, 8);
  ctx.fill();

  // Body
  ctx.fillStyle = o.lowPower ? '#cfd4d5' : '#eef3f4';
  rr(ctx, -34, -18, 68, 36, 9);
  ctx.fill();

  ctx.strokeStyle = V.outline;
  ctx.lineWidth = 2;
  ctx.stroke();

  // Seam
  ctx.strokeStyle = '#b9c6c8';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(12, -18);
  ctx.lineTo(12, 18);
  ctx.stroke();

  // Front face
  ctx.fillStyle = '#f7fbfb';
  rr(ctx, 24, -16, 10, 32, 4);
  ctx.fill();

  // LED
  ctx.fillStyle = o.plugged
    ? V.cyan
    : o.lowPower
      ? V.red
      : '#4f6d6f';

  ctx.beginPath();
  ctx.arc(29, 0, 4, 0, Math.PI * 2);
  ctx.fill();

  // Door open
  if (o.doorOpen) {
    ctx.save();
    ctx.translate(29, -16);
    ctx.rotate(-1.4);

    ctx.fillStyle = '#f7fbfb';
    rr(ctx, 0, -2, 10, 32, 4);
    ctx.fill();

    ctx.strokeStyle = V.outline;
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.restore();

    // Light spill
    ctx.fillStyle = 'rgba(123, 216, 214, 0.25)';
    ctx.beginPath();
    ctx.moveTo(34, -16);
    ctx.lineTo(54, -26);
    ctx.lineTo(54, 26);
    ctx.lineTo(34, 16);
    ctx.closePath();
    ctx.fill();
  }

  ctx.restore();
}
```

### 22.5 Resident Sprite Reference

```js
function drawResident(ctx, x, y, angle, id, o = {}) {
  const colors = {
    mom: '#b56a7a',
    dad: '#6d8ba8',
    kid: '#d8a44a'
  };

  ctx.save();
  ctx.translate(x, y);

  // Shadow
  ctx.fillStyle = V.shadow;
  ctx.beginPath();
  ctx.arc(3, 5, 20, 0, Math.PI * 2);
  ctx.fill();

  ctx.rotate(angle);

  // Body
  ctx.fillStyle = colors[id];
  ctx.beginPath();
  ctx.arc(0, 0, 20, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = V.outline;
  ctx.lineWidth = 2;
  ctx.stroke();

  // Facing wedge
  ctx.fillStyle = 'rgba(0, 0, 0, 0.18)';
  ctx.beginPath();
  ctx.arc(0, 0, 12, -0.9, 0.9);
  ctx.arc(0, 0, 6, 0.9, -0.9, true);
  ctx.closePath();
  ctx.fill();

  // Facing dot
  ctx.fillStyle = '#f4f1ea';
  ctx.beginPath();
  ctx.arc(14, 0, 4, 0, Math.PI * 2);
  ctx.fill();

  // State ring
  if (o.suspicious) {
    ctx.strokeStyle = V.amber;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(0, 0, 22, 0, Math.PI * 2);
    ctx.stroke();
  }

  if (o.investigate) {
    ctx.strokeStyle = V.red;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(0, 0, 22, 0, Math.PI * 2);
    ctx.stroke();
  }

  ctx.restore();
}
```

### 22.6 Noise Ring Reference

```js
function drawNoiseRing(ctx, x, y, radius, t, duration, color, width = 2) {
  const p = Math.min(1, t / duration);
  const r = radius * p;

  ctx.save();
  ctx.globalAlpha = (1 - p) * 0.5;
  ctx.strokeStyle = color;
  ctx.lineWidth = width * (1 - p) + 1;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();
}
```

Example:

```js
drawNoiseRing(ctx, x, y, 160, elapsed, 0.7, V.cyan, 5);
```

### 22.7 Simple SFX Helper

This is a minimal reference for procedural WebAudio SFX.

```js
let AC;

function ac() {
  if (!AC) {
    AC = new (window.AudioContext || window.webkitAudioContext)();
  }
  return AC;
}

function tone({
  freq = 440,
  type = 'sine',
  dur = 0.1,
  gain = 0.2,
  attack = 0.01,
  release = 0.05,
  filterFreq = 0
}) {
  const ctx = ac();
  const t = ctx.currentTime;

  const osc = ctx.createOscillator();
  osc.type = type;
  osc.frequency.setValueAtTime(freq, t);

  const g = ctx.createGain();
  g.gain.setValueAtTime(0, t);
  g.gain.linearRampToValueAtTime(gain, t + attack);
  g.gain.linearRampToValueAtTime(0, t + attack + dur + release);

  let node = osc;

  if (filterFreq > 0) {
    const f = ctx.createBiquadFilter();
    f.type = 'lowpass';
    f.frequency.value = filterFreq;
    osc.connect(f);
    node = f;
  }

  node.connect(g);
  g.connect(ctx.destination);

  osc.start(t);
  osc.stop(t + attack + dur + release + 0.02);
}
```

Example SFX:

```js
// Plug connection
tone({ freq: 1200, type: 'sine', dur: 0.02, gain: 0.25 });
tone({ freq: 200, type: 'sine', dur: 0.1, gain: 0.15, filterFreq: 800 });

// Unplug
tone({ freq: 70, type: 'sine', dur: 0.08, gain: 0.35 });
tone({ freq: 900, type: 'square', dur: 0.02, gain: 0.15 });

// Timer tick
tone({ freq: 1800, type: 'square', dur: 0.02, gain: 0.08 });

// Win note
tone({ freq: 523.25, type: 'triangle', dur: 0.2, gain: 0.25 });
```

For noise-based sounds such as waddling and sliding, use a short white noise buffer passed through a low-pass filter. The exact implementation can vary, but the audible goal is:

- Waddle: soft, low, quiet.
- Slide: heavy, loud, short.
- Collision: thumpy, brief.
- Hum: low sustained sine with slight vibrato.

---

## 23. Final Visual Intent

The player should always understand:

- “I am the fridge.”
- “I am heavy and slow.”
- “The house is watching.”
- “Noise matters.”
- “Power matters.”
- “The door is close, but not safe.”

The visuals should make the escape feel like a quiet, anxious journey through a familiar house.

The game should not feel like a shooter, platformer, or puzzle game. It should feel like a stealth escape where the player is an appliance trying to leave before the world notices.