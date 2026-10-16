# visual.md

## 1. Purpose and Scope

This document defines the visual and audio presentation for the top-down space salvage game.

It is the source of truth for:

- Overall visual style.
- World readability.
- HUD and UX.
- Station, ship, wreck, debris, mine, and effect presentation.
- Music and sound effects.
- Visual feedback for gameplay states.

It does not define gameplay rules beyond how gameplay systems should be presented.

The game should look like a quiet, practical salvage operation around a space station. The core visual job is to make towing readable, the station feel safe, hazards feel avoidable, and upgrades feel meaningful.

---

## 2. Core Visual Direction

### Style

Use a clean 2D top-down style with:

- North-up camera.
- No camera rotation.
- No vertical axis.
- No 3D rotation.
- Pseudo-depth only through parallax, glow, rim lighting, and soft shadows.
- Strong silhouettes.
- Low clutter.
- High contrast between player, wrecks, hazards, and background.

The game should feel like a working salvage tug, not a military combat ship. The visual language should be functional, slightly worn, and service-oriented.

### Mood by Area

| Area | Mood | Visual Feeling |
|---|---|---|
| Station | Safe, warm, stable | Bright warm lights, calm motion, clear dock zone |
| Ring 1 | Beginner, approachable | Brighter background, sparse debris, station glow |
| Ring 2 | Caution | Cooler tint, first mine glints, more dust |
| Ring 3 | Tension | Darker, denser debris, violet/teal background |
| Ring 4 | Heavy, industrial | Brown/amber dust, larger debris, heavier wrecks |
| Final Corridor | Ominous, final | Near-black background, aurora streaks, high contrast |

### Why

Towing is the core mechanic. The camera must stay readable while the player, tow line, and wreck are all visible. The station must always read as the safe destination. Hazards must be avoidable through visual reading, not surprise.

---

## 3. Scale, Resolution, and Camera

### Target Resolution

Use 1280 x 720 as the base layout.

Scale UI proportionally for other resolutions while preserving HUD safe margins.

### World Scale

Use 1 world unit = 1 pixel at zoom 1.0.

| Object | Gameplay Radius | Visual Size |
|---|---:|---:|
| Ship | 14 | 34 x 22 px sprite |
| Scrap Can | 18 | 36 x 36 px |
| Transport Hauler | 24 | 48 x 48 px |
| Fighter Frame | 26 | 52 x 52 px |
| Cargo Liner | 32 | 64 x 64 px |
| Aurora Black Box | 36 | 72 x 72 px |
| Mine | 12 | 24 x 24 px |
| Debris cluster | 25–50 | Scale to match collision radius |
| Station safe zone | 120 | 240 px diameter visual field |
| Dock zone | 50 | 100 px diameter visual field |

### Visual Size Rule

Visual silhouettes should not exceed collision radii by more than 2 pixels.

Why:

- The player must trust what they see.
- A wreck or debris cluster that looks larger than its collision circle feels unfair.
- A wreck that looks smaller than its collision circle also feels unfair.

### Camera

- Camera is centered on the ship.
- Camera does not rotate.
- While towing, if ship-to-wreck distance is greater than 100 world units, center the camera on the midpoint between ship and wreck.
- Use fixed zoom 1.0 by default.
- If both ship and wreck cannot fit at zoom 1.0, zoom out to a minimum of 0.85.
- Do not use camera roll, shake, or rotation to express tow stress.

Why:

- Fixed north-up presentation makes the tow line and minimap easier to read.
- Slight zoom-out is acceptable because the tow relationship becomes the main subject.
- Camera shake should be feedback, not navigation.

---

## 4. Color System

### Base Palette

| Use | Hex | Notes |
|---|---:|---|
| Space black | `#05070D` | Base background |
| Deep space blue | `#0A1220` | Nebula and panel base |
| UI panel | `#0B1220` | 80% opacity |
| UI border | `#2E4A5A` | Subtle technical border |
| White text | `#F4F7FB` | Primary text |
| Muted text | `#9FB0C0` | Secondary text |

### Semantic Colors

| Meaning | Hex | Use |
|---|---:|---|
| Player / interactive | `#55F1FF` | Ship, player arrow, attachable prompts |
| Station / score | `#FFC46B` | Station, contract, score popups |
| Success / parts / dock | `#55FF9A` | Unload, parts, contract complete |
| Warning | `#FFD24D` | Moderate tow stress, speed warnings |
| Danger / damage | `#FF4D5A` | Hull damage, mines, high stress |
| Scanner / final | `#B48BFF` | Scanner effects, final wreck accent |

### Wreck Tier Colors

All wrecks share a desaturated gray hull base. Tier identity comes from size, silhouette, and one accent color.

| Wreck | Accent Color | Hex |
|---|---|---:|
| Scrap Can | Rust orange | `#FF7A3D` |
| Transport Hauler | Slate teal | `#6FC7B0` |
| Fighter Frame | Magenta | `#FF5AF1` |
| Cargo Liner | Mustard | `#FFC84D` |
| Aurora Black Box | Violet/gold/cyan aurora | `#B48BFF`, `#FFD24D`, `#55F1FF` |

### Ring Background Tints

| Ring | Background Tint | Notes |
|---|---:|---|
| Ring 1 | `#102033` | Brighter, warm station glow |
| Ring 2 | `#0F2A2C` | Cooler teal, first caution |
| Ring 3 | `#1A1430` | Darker violet, denser |
| Ring 4 | `#2A1A10` | Brown/amber industrial dust |
| Final Corridor | `#05070D` | Near-black with aurora streaks |

### Colorblind and Readability Rules

Do not rely on color alone.

- Player is an arrow shape and bright cyan.
- Danger uses red plus white warning rings.
- Success uses green plus check or plus symbols.
- Wrecks use size, silhouette, and accent light.
- Locked wrecks are dark gray with no accent light.
- Mines are red blinking spheres with white warning rings when armed.

Why:

- The game must be readable for colorblind players.
- The core loop depends on quickly identifying wrecks, hazards, and station zones.

---

## 5. Typography and UI Style

### Font

Use a clean technical sans-serif.

Preferred font:

- `Rajdhani`
- Fallback: `Chakra Petch`
- Final fallback: system sans-serif

Use tabular numerals for all HUD numbers.

### Type Sizes

| Use | Size |
|---|---:|
| HUD labels | 12 px |
| HUD values | 16 px |
| Prompts | 20 px |
| Menu headers | 24 px |
| Title screen title | 56 px |
| Game over / victory header | 40 px |

Use uppercase for short labels. Use sentence case for longer prompts.

### UI Panel Style

- Background: `#0B1220` at 80% opacity.
- Border: 1 px `#2E4A5A`.
- Corners: 4 px cut corners, not rounded.
- Inner glow: very subtle cyan or amber depending on context.
- No heavy drop shadows.
- No glassmorphism.

### Buttons

| State | Fill | Border | Text |
|---|---:|---:|---:|
| Idle | `#12233A` | `#2E4A5A` | `#F4F7FB` |
| Hover | `#1B3550` | `#55F1FF` | `#FFFFFF` |
| Active | `#0F1B2A` | `#55F1FF` | `#FFFFFF` |
| Disabled | `#101820` | `#1E2A35` | `#5D6B7A` |

### Keycaps

Render keyboard keys as small rounded rectangles:

- Background: `#101820`.
- Border: `#55F1FF`.
- Text: `#FFFFFF`.
- Size: 24 x 24 px for single keys.
- Use for `Q`, `U`, `Tab`, `P`, `Esc`, `A`, `D`, `W`, `S`.

### Icons

Use simple 20 x 20 px line icons with 2 px stroke.

| Icon | Meaning |
|---|---|
| Shield | Hull |
| Gauge | Speed |
| Hex bolt | Parts |
| Clipboard | Contract |
| Hook | Tow |
| Radar | Scanner |
| Station ring | Station / safe zone |
| Explosion | Mine / damage |

---

## 6. World Presentation

### Z-Order

Render in this order:

1. Far starfield.
2. Mid starfield and nebula.
3. Near dust.
4. World boundary effect.
5. Station safe zone.
6. Dock zone.
7. Station.
8. Debris clusters.
9. Wrecks.
10. Mines.
11. Tow line.
12. Ship.
13. Particles.
14. Vignettes and damage overlays.
15. HUD.
16. Prompts.
17. Banners.
18. Menus and full-screen states.

### Parallax Layers

Use three background layers.

| Layer | Speed | Contents |
|---|---:|---|
| Far | 0.1x | Small stars, faint nebula |
| Mid | 0.25x | Larger stars, colored nebula clouds |
| Near | 0.5x | Tiny dust motes, non-collidable |

Near dust must be visually distinct from debris:

- Dust is 1–2 px.
- Dust has no rim light.
- Dust has no collision warning.
- Dust does not blink.

Why:

- Parallax gives depth without breaking top-down gameplay.
- Dust must not be confused with hazards.

### World Boundary

At radius 3200, show a subtle boundary:

- Faint white circular grid.
- Static noise near the edge.
- Slight dark vignette.
- Prompt: `No signal beyond boundary`.

Do not show a solid wall.

Why:

- The gameplay boundary is a soft clamp.
- A hard wall would contradict the movement model.

---

## 7. Station, Safe Zone, and Dock Zone

### Station Visual

The station is the visual anchor of the game.

Use a top-down station with:

- Central warm core.
- 3 or 4 rotating service arms.
- Open lattice structure.
- Warm amber lights.
- Subtle slow rotation, visual only.
- No solid wall impression.

The station should look serviceable and open, not fortress-like.

Why:

- Gameplay says the station is not a solid collision object.
- The visual must not suggest that the player will collide with it.
- The station should feel like a docking platform and repair bay, not a physical obstacle.

### Safe Zone

Safe zone radius: 120.

Visual:

- Soft cyan circular field.
- Dashed outer edge.
- Radius: 120 world units.
- Color: `#55F1FF` at 20–30% opacity.
- Gentle 2-second pulse.
- Background inside the safe zone is slightly brighter.
- No debris or mines are shown inside the safe zone.

Why:

- The safe zone must be readable at a glance.
- Cyan matches player and interactive systems.
- The pulse communicates safety without becoming distracting.

### Dock Zone

Dock zone radius: 50.

Visual:

- Brighter ring inside the safe zone.
- Radius: 50 world units.
- Color: `#55FF9A`.
- Solid ring, not dashed.
- Rotating inward chevrons.
- Slight green glow.
- When the player is inside and towing, the dock ring brightens.
- When the player is inside but speed is too high, the ring flashes yellow.

Why:

- The safe zone is general safety.
- The dock zone is the specific unload area.
- Green communicates success and unloading.
- The rotating chevrons make the dock feel active without adding clutter.

### Contract Board

Show a small floating holographic panel near the station.

Contents:

- Active contract name.
- Contract progress.
- Reward parts.
- Recommended upgrade tag, if applicable.

Style:

- Amber border.
- Dark translucent panel.
- 160 x 96 px.
- Positioned near the station but not overlapping the dock zone.

When a contract completes:

- Contract board flashes green.
- A stamp-like `COMPLETE` appears for 1.5 seconds.
- Reward parts fly from the board to the parts counter.

Why:

- The station is the progression hub.
- Showing the contract at the station reinforces the loop: salvage, return, refit.

### Checkpoint Feedback

When the ship enters the safe zone:

- Small white pulse ring around the ship.
- Small green prompt: `Checkpoint saved`.
- Hull regeneration is shown by the hull bar filling and small green sparkles near the ship.

Why:

- Checkpointing is a core fairness system.
- The player should know that returning to the station is safe and preserves progress.

### Ring Unlock Feedback

When a ring unlocks:

- Show banner: `Ring 2 Unlocked`, `Ring 3 Unlocked`, etc.
- Minimap reveals the new ring boundary.
- The new ring boundary lights up in cyan for 1 second.
- Background tint shifts to the new ring treatment.

Why:

- Ring progression is a core spatial reward.
- The player should feel that the world is expanding.

---

## 8. Player Ship

### Base Ship

The ship is a small salvage tug.

Visual silhouette:

- Arrow-like but rounded.
- Clear nose marker.
- Bright cyan hull edge.
- Dark cockpit.
- Rear thruster.
- Front tow hook.

Base colors:

- Hull edge: `#55F1FF`.
- Hull body: `#103040`.
- Cockpit: `#F4F7FB`.
- Thruster flame: `#FF9A3D` with white core.

The ship should be the brightest player-controlled object in the world.

Why:

- The player must always know where their ship is.
- The ship must stand out against dark space, debris, and wrecks.

### Movement Visuals

#### Thrust

When thrusting:

- Orange/white flame from rear.
- Flame length increases with speed.
- Small particle trail.
- Engine glow.

#### Brake

When braking:

- Small white/blue reverse puff.
- Slight exhaust fade.
- No dramatic effect.

#### Turn

When turning:

- Subtle servo animation.
- No visible trail unless thrusting.

Why:

- The ship should feel floaty but controllable.
- Effects should communicate input, not overwhelm the screen.

### Upgrade Visuals

Upgrades should be visible on the ship.

#### Hull Plating

- Add visible armor plates around the hull.
- Increase outline thickness slightly.
- Add amber/steel accents.
- Level 1: one side plate.
- Level 2: two side plates.
- Level 3: full plated hull.

Why:

- Hull upgrades should feel like physical protection.

#### Thrusters

- Engine pods grow.
- Exhaust becomes brighter and wider.
- Level 1: single larger engine.
- Level 2: dual engines.
- Level 3: dual engines with visible exhaust glow.

Why:

- Speed upgrades should be immediately visible.

#### Tow Servos

- Front tow arm grows.
- Add hydraulic pistons and cable housing.
- Level 0: small hook.
- Level 1: medium clamp.
- Level 2: large clamp.
- Level 3: dual clamp with reinforced housing.

Why:

- Towing is the core mechanic.
- Tow upgrades must feel like the ship is physically better at towing.

#### Scanner

- Add dish/antenna on top.
- Level 1: small dish and faint violet scan ring.
- Level 2: larger dish and stronger scan ring.

Why:

- Scanner upgrades should feel like added sensor equipment.

### Hull Damage Visuals

When the ship takes hull damage:

- Red flash on the ship hull.
- Red vignette for 150 ms.
- Hull bar flashes.
- Small spark or breach particles.
- Screen shake up to 4 px.

When hull is below 30%:

- Ship outline pulses red at 2 Hz.
- Small warning particles.
- Hull bar pulses.

Why:

- Hull damage must be readable.
- Low hull should create urgency without hiding the ship.

### Ship Destruction

When the ship is destroyed:

- Explosion centered on ship.
- Tow line breaks if towing.
- Red vignette.
- Screen shake 6 px.
- Ship sprite breaks into 4–6 fragments.
- Fragments fade over 0.8 seconds.
- Then show Game Over screen.

Why:

- Death must be clearly communicated.
- The towed wreck must remain visible in the world before the Game Over screen appears.

---

## 9. Wrecks

### Common Wreck Style

All active wrecks share:

- Desaturated gray hull base.
- Broken edges.
- Dark interior details.
- One tier accent color.
- A small blinking status light in the tier accent color.
- Slight slow rotation for visual life, not gameplay.

Why:

- Wrecks should look damaged but still whole.
- The blinking light distinguishes active wrecks from debris and locked wrecks.

### Wreck Tier Visuals

| Wreck | Silhouette | Accent | Visual Notes |
|---|---|---|---|
| Scrap Can | Small canister | Rust orange | Simple, compact, low detail |
| Transport Hauler | Shuttle/transport | Slate teal | Broken wing, cargo pods |
| Fighter Frame | Angular fighter | Magenta | Sharp broken wings, exposed frame |
| Cargo Liner | Large boxy liner | Mustard | Containers, broken hull panels |
| Aurora Black Box | Black cube | Violet/gold/cyan | Rotating rings, aurora glow, unique |

### Wreck States

#### Locked

- Dark gray silhouette.
- No accent light.
- No blinking.
- 40% opacity.
- Not shown on minimap.
- No scanner data.

Why:

- Locked wrecks may be visible in the world but must not invite interaction.

#### Active

- Full color.
- Accent light blinks at 1 Hz.
- Shown on minimap.
- Can be scanned, towed, and unloadded.

#### Towed

- Tow line connected.
- Integrity bar visible.
- Wreck may emit small damage particles if integrity is low.

#### Unloadded

- Wreck fades out over 0.5 seconds.
- Score and part popups appear.
- Wreck is removed from the world.

### Wreck Integrity Visuals

Wreck integrity should be readable when towing or scanning.

Use both an integrity bar and light state.

| Integrity | Visual State |
|---|---|
| Greater than 60% | Accent light steady, hull mostly intact |
| 30% to 60% | Accent light flickers, visible cracks, small smoke/spark particles |
| Less than 30% | Accent light weak, exposed interior, more sparks, darker hull |
| 0% | Dark, broken-looking, but still whole enough to tow |

Why:

- Parts depend on careful salvage.
- The player should see the difference between a clean wreck and a damaged wreck.
- A zero-integrity wreck must still look towable.

### Scanner Data Card

With Scanner Level 1, when within 200 units of a wreck:

Show a small data card near the wreck.

Contents:

- Wreck name.
- Mass.
- Part yield.
- Integrity percentage.

Style:

- 140 x 64 px.
- Dark panel.
- Cyan border.
- Fade in over 150 ms.
- Fade out when out of range.

Why:

- Scanner upgrades should feel like information, not just minimap dots.

### Aurora Black Box

The final wreck must be visually distinct.

Use:

- Black cube core.
- Violet, gold, and cyan aurora glow.
- Slowly rotating rings.
- Soft pulse.
- Unique minimap icon: gold/violet diamond.
- Slightly larger than other wrecks.
- No blinking status light; use aurora pulse instead.

Why:

- The final wreck is the win condition.
- It should feel special without breaking the salvage aesthetic.

---

## 10. Tow System Visuals

### Tow Attach

When the player is not towing and is near an active wreck:

- If attachable:
  - Show dashed cyan preview line from ship to wreck.
  - Show prompt: `Q: Attach Tow`.
  - Show faint cyan attach range circle around the ship.
- If out of range:
  - Show prompt: `Out of range`.
- If too fast:
  - Show yellow preview line.
  - Show prompt: `Too fast to attach`.
- If mass exceeded:
  - Show red preview line.
  - Show prompt: `Cannot tow: mass exceeded`.
- If already towing:
  - Show prompt: `Detach current tow first`.

Why:

- Attach failures must be explained visually.
- The preview line helps the player understand the tow relationship before attaching.

### Tow Line

The tow line connects the ship’s front tow point to the wreck’s center or tow point.

Use a straight line when taut. Use a slight curve when slack.

#### Tow Line States

| State | Force Ratio | Visual |
|---|---:|---|
| Normal | 0–0.75 | Cyan line, 2 px wide |
| Moderate | 0.75–1.0 | Yellow line, 2–3 px wide |
| High | 1.0–1.25 | Red line, 3 px wide, slight vibration |
| Snap Warning | Greater than 1.25 | Flashing red line, snap timer arc |

Force ratio is current tow force divided by current `tow_power`.

#### Snap Warning

If force exceeds 1.25 x `tow_power`:

- Line flashes red.
- Show a small arc near the ship or bottom-center stress meter.
- Arc fills over 0.5 seconds.
- If it fills, the line snaps.

Why:

- The snap is a core failure state.
- The player needs a clear warning before the tow line breaks.

### Tow Snap

When the line snaps:

- Line breaks visually.
- Spark at both ends.
- Cable whip effect.
- Small white flash at the break point.
- Prompt: `Tow line snapped`.
- Wreck keeps its current velocity.
- Screen shake 4 px.

Why:

- Snapping must feel sudden but not random.
- The visual should match the physical event.

### Tow Stress Meter

Show a stress meter at bottom center while towing.

Style:

- 120 x 8 px.
- Background: `#101820`.
- Fill color matches tow line state.
- Marker at 1.0 x `tow_power`.
- Snap warning zone beyond 1.25 x `tow_power`.

Why:

- The line color is important, but a meter gives precise feedback.
- The player should be able to read stress without staring at the line.

### Towed Wreck Integrity

While towing:

- Show a small integrity bar above the wreck.
- Bar size: 40 x 4 px.
- Color:
  - Green above 60%.
  - Yellow from 30% to 60%.
  - Red below 30%.
- Also show integrity in the bottom-center tow status.

Why:

- The player must know when the wreck is taking damage.
- Parts depend on integrity, so integrity must be readable during the most important phase.

---

## 11. Hazards

### Debris Clusters

Debris clusters are static circular obstacles.

Visual:

- Cluster of 3–7 rock/metal chunks.
- Dark gray and brown tones.
- Rim lighting on one side.
- No blinking lights.
- No accent color.
- Irregular silhouette.
- Visual size matches collision radius.

When the ship or towed wreck is within 50 units:

- Add subtle white rim highlight.
- Do not make it look like a mine.

Why:

- Debris is a collision hazard, not a proximity trigger.
- It should look inert but dangerous at speed.

### Debris Collision Feedback

When colliding with debris:

- Impact flash at collision point.
- Small rock/metal particles.
- Screen shake based on impact speed.
- Hull or wreck damage feedback.
- Low restitution bounce.

Why:

- Collisions should feel physical, not cartoonish.

### Mines

Mines are circular hazards.

Mine visual:

- Dark sphere.
- Radius: 12 world units.
- Red blinking light.
- No explosion until armed.

#### Mine States

| State | Visual |
|---|---|
| Dormant, Scanner 0 | Faint red dot, hard to see at distance |
| Dormant, close range | Red light visible, slow blink |
| Armed | Fast red blink, expanding white/red ring to proximity radius 35 |
| Exploding | White flash, orange shockwave, particles, screen shake |

Blink rate:

- Dormant: 1 Hz.
- Armed: 2 Hz maximum.

Why:

- Mines must create avoidable danger.
- The armed state must be unmistakable.
- Blink rate must stay accessible.

### Mine Warning Radius

With Scanner Level 2:

- Show mines on the minimap with a warning radius.
- In the world, when a mine is within 250 units, show a dashed red circle around it.
- Circle radius: 70 world units.
- Color: `#FF4D5A` at 40% opacity.
- Do not show all warning circles at once; only show nearby mines.

Why:

- Scanner Level 2 should reduce uncertainty.
- Showing only nearby warning circles prevents visual clutter.

### Mine Explosion

When a mine explodes:

- White radial flash, not full-screen.
- Flash duration under 100 ms.
- Orange/red shockwave expands to 70 world units.
- Small debris particles.
- Screen shake 6 px.
- Red vignette if the ship is damaged.

Why:

- Explosions should feel dangerous but not epileptically strobing.
- The shockwave should communicate the explosion radius.

---

## 12. HUD and UX

### HUD Layout

Base layout for 1280 x 720:

#### Top Left

Position: 16, 16  
Size: 220 x 64 px

Contains:

- Hull label.
- Hull bar.
- Hull number.
- Speed.

Example:

```text
HULL 140 / 180
SPEED 212
```

#### Top Center

Position: centered, y = 16  
Size: 320 x 64 px

Contains:

- Active contract name.
- Contract progress bar.
- Contract score.

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

Contains:

- Parts count.
- Minimap.

Parts counter:

- Size: 160 x 32 px.
- Position: top-right corner.
- Shows `PARTS 14` with hex bolt icon.

Minimap:

- Circular.
- Radius: 100 px.
- Centered near top-right.
- Background: `#0B1220` at 70% opacity.
- Border: `#2E4A5A`.

#### Bottom Center

Contains:

- Tow status.
- Contextual prompts.

Tow status:

- Size: 320 x 40 px.
- Position: bottom center, 72 px from bottom.

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

Prompts:

- Position: bottom center, 112 px from bottom.
- Use keycaps and short text.

### Hull Bar

Style:

- Width: 180 px.
- Height: 12 px.
- Background: `#101820`.
- Fill colors:
  - Above 60%: `#55FF9A`.
  - 30% to 60%: `#FFD24D`.
  - Below 30%: `#FF4D5A`.

On damage:

- Hull bar flashes red.
- Hull number shakes slightly.
- Red vignette appears.

Why:

- Hull is the primary survival stat.
- It must be readable even during towing.

### Contract Progress Bar

Style:

- Width: 240 px.
- Height: 8 px.
- Fill: `#FFC46B`.
- Complete flash: `#55FF9A`.

When contract completes:

- Progress bar fills green.
- Banner appears: `Contract Complete`.
- Reward parts fly to parts counter.
- Progress resets for the next contract.

Why:

- Contract progression is the main pacing system.
- The player should always know how much salvage is needed.

### Minimap

Minimap scale:

- World radius 3200 maps to minimap radius 100 px.
- North is up.

Minimap contents:

| Object | Visual |
|---|---|
| Station | Amber dot, 6 px |
| Player | Cyan arrow, 8 px |
| Scrap Can | Orange dot, 4 px |
| Transport Hauler | Teal dot, 5 px |
| Fighter Frame | Magenta dot, 6 px |
| Cargo Liner | Mustard dot, 7 px |
| Aurora Black Box | Gold/violet diamond, 10 px |
| Mine, Scanner 1+ | Red dot, 3 px |
| Mine, Scanner 2 | Red dot with 70-unit warning circle |
| Ring boundaries | Faint white circles |
| Locked rings | Not shown |

Why:

- The minimap must match the world orientation.
- Wreck dot size should communicate tier without requiring the player to read labels.

### Prompt Priority

If multiple prompts are active, show the most important one first.

Priority order:

1. Failure prompts.
2. Action prompts.
3. Information prompts.

Examples:

- `Too fast to attach`
- `Cannot tow: mass exceeded`
- `Detach current tow first`
- `Out of range`
- `Q: Attach Tow`
- `Q: Detach Tow`
- `Hold U: Unload`
- `Speed too high to unload`
- `Tab: Refit`
- `Detach to refit`
- `No signal beyond boundary`
- `Tow line snapped`
- `Checkpoint saved`

Style:

- Positive/action prompts: white text with cyan keycap.
- Warning prompts: yellow text.
- Failure prompts: red text.
- Success prompts: green text.

Why:

- The player should not miss critical feedback.
- Failure prompts must be louder than optional actions.

### Score and Part Popups

When unloading:

- Score popup: `+10`, `+25`, etc.
  - Color: `#FFC46B`.
  - Floats upward for 0.8 seconds.
- Part popup: `+1`, `+2`, etc.
  - Color: `#55FF9A`.
  - Includes hex bolt icon.
  - Floats upward for 0.8 seconds.

Why:

- Unloading is the reward moment.
- The player should see exactly what they earned.

### Unload Progress

When unloading:

- Show circular progress ring around the ship.
- Radius: 20 px.
- Color: `#55FF9A`.
- Fills over 2.0 seconds.
- If speed is too high:
  - Ring turns yellow.
  - Prompt: `Speed too high to unload`.
- If the player leaves the dock zone:
  - Ring disappears.
  - Progress resets.

Why:

- Unloading is a hold action.
- The player needs clear progress feedback.

### Tutorial Visuals

During the tutorial:

- Highlight the current target with a faint cyan ring.
- Show bottom-center prompts:
  1. `Use A/D to rotate. Use W to thrust.`
  2. `Approach a Scrap Can. Press Q to attach.`
  3. `Tow it back to the station.`
  4. `Hold U in the dock to unload.`
  5. `Use parts to upgrade your ship.`

Why:

- The first loop must be easy to follow.
- Visual highlighting reduces trial and error.

---

## 13. Upgrade Menu

### When Available

The upgrade menu can be opened only:

- Inside the station safe zone.
- While not towing.

If the player tries to open it while towing:

- Prompt: `Detach to refit`.

### Layout

Use a full-screen dimmed overlay.

Panel size: 720 x 480 px, centered.

Left side:

- Ship schematic.
- Current upgrade modules highlighted in their track colors.
- Ship schematic updates immediately after purchase.

Right side:

- Parts count.
- Four upgrade track rows.

### Upgrade Track Colors

| Track | Color |
|---|---:|
| Hull Plating | `#FFC46B` |
| Thrusters | `#55F1FF` |
| Tow Servos | `#55FF9A` |
| Scanner | `#B48BFF` |

### Row Layout

Each row shows:

- Icon.
- Track name.
- Current level pips.
- Next level effect.
- Cost.
- Buy button.
- Optional `RECOMMENDED` tag.

Example:

```text
TOW SERVOS
Level 2 / 3
Next: Tow Power 850, Max Mass 130
Cost: 6 parts
[BUY]
```

### Recommended Tag

Use a small amber tag:

- Text: `RECOMMENDED`.
- Background: `#FFC46B` at 20% opacity.
- Border: `#FFC46B`.

Why:

- The contract board should guide the player without forcing a single build.

### Buy Button States

| State | Visual |
|---|---|
| Affordable | Enabled, cyan hover |
| Not affordable | Disabled, muted |
| Max level | Shows `MAX`, disabled |
| Purchase success | Button flashes green, parts count updates, ship schematic updates |

Why:

- Upgrades should feel immediate and satisfying.
- The player should see the ship change right away.

---

## 14. Game States and Screens

### Title Screen

Background:

- Dark starfield.
- Station silhouette.
- Slow aurora glow.

Text:

- Game title: `SALVAGE SHIFT`.
- Subtitle: `A top-down space salvage tug`.
- Prompt: `Press Enter to start`.

Music:

- Station theme, calm.

Why:

- The title should communicate the station-and-salvage fantasy immediately.

### Start State

- Player starts at station.
- Safe zone visible.
- Tutorial prompts begin.
- Contract 1 shown at top center.

### Contract Active

- Normal HUD.
- Active contract shown.
- Wrecks and hazards visible.
- Minimap active.

### At Station

- Safe zone glow.
- Dock zone visible.
- Contract board visible.
- Prompt: `Tab: Refit` if not towing.
- Hull regeneration visual if hull is not full.

### Upgrade Menu

- Full-screen dimmed overlay.
- Ship schematic and upgrade rows.
- World remains visible but dimmed.

### Paused

- Dim world to 60%.
- Center panel:
  - `Paused`
  - `Resume`
  - `Retry Contract`
  - `Restart Run`

Music:

- Continue at reduced volume, or lower by 6 dB.

Why:

- Pausing should feel like a break from the shift, not a hard stop.

### Game Over

Visual sequence:

1. Ship explosion.
2. Red vignette.
3. Fade to dark red panel.

Panel contents:

```text
SHIP DESTROYED
Contract: Deep Field
Progress: 40 / 100

[Retry Contract]
```

Style:

- Red border.
- Dark background.
- Contract name and progress in white.
- Retry button in cyan.

Why:

- Death must be clear but not punishing visually.
- The player should immediately understand that they can retry the contract.

### Victory

Visual sequence:

1. Aurora Black Box unloads.
2. Station lights brighten.
3. Gold/violet vignette.
4. Victory panel fades in.

Panel contents:

```text
SHIFT COMPLETE
Aurora Black Box Recovered

Time: 18:42
Wrecks Salvaged: 23
Parts Collected: 54

[Play Again]
```

Style:

- Gold border.
- Warm background glow.
- Aurora Black Box icon or silhouette.

Why:

- Victory should feel like a successful salvage job, not a combat win.

---

## 15. Effects and Particles

### General Rules

- Keep particle counts low.
- Effects should support readability.
- No full-screen white flashes.
- No rapid strobing.
- Screen shake maximum 6 px.
- Screen shake should be short and localized.

### Particle Budget

| Effect | Approximate Particles |
|---|---:|
| Thrust | 3 per frame |
| Brake | 2 per frame |
| Hull damage | 12 |
| Wreck damage | 8 |
| Tow snap | 16 |
| Mine explosion | 40 |
| Unload complete | 24 |
| Contract complete | 16 |

### Effect Timing

| Effect | Duration |
|---|---:|
| UI fade | 150 ms |
| Prompt appear | 100 ms |
| Hull damage flash | 150 ms |
| Explosion flash | Under 100 ms |
| Explosion shockwave | 400 ms |
| Score popup | 800 ms |
| Contract banner | 2000 ms |
| Ring unlock banner | 2000 ms |

Why:

- Effects should feel responsive.
- Long effects can obscure gameplay.

---

## 16. Music

### Musical Direction

The music should support careful piloting, not action.

Use:

- Ambient synth pads.
- Low industrial pulses.
- Sparse plucks.
- Warm station themes.
- Tension layers for towing and mines.
- No combat music.
- No aggressive percussion.

Tempo range: 60–80 BPM.

Key centers:

- Station: C major.
- Field: A minor.
- Final: Suspended A minor.
- Victory: C major.

### Music Stems

Use separate stems so the game can layer dynamically.

| Stem | File Name | Purpose |
|---|---|---|
| Station | `music_station.mp3` | Safe zone, upgrade menu, title |
| Field | `music_field.mp3` | General salvage field |
| Tow | `music_tow.mp3` | Towing tension |
| Stress | `music_stress.mp3` | High tow stress |
| Final | `music_final.mp3` | Final corridor |
| Victory | `music_victory.mp3` | Victory screen |
| Mine stinger | `sfx_mine_stinger.mp3` | Mine armed |
| Contract complete | `sfx_contract_complete.mp3` | Contract reward |

### Stem Descriptions

#### Station

- Warm pad.
- Soft pulse.
- C major.
- 60 BPM.
- Feels safe and stable.

#### Field

- Ambient noise.
- Sparse plucks.
- A minor.
- 70 BPM.
- Neutral, slightly lonely.

#### Tow

- Low ostinato.
- Sub-bass.
- 80 BPM.
- Adds weight and purpose.

#### Stress

- Pulsing synth.
- Metallic clicks.
- Faster feel.
- Minor tension.
- Should not sound like alarm music.

#### Final

- Darker.
- Lower.
- Sparse strings or synth.
- Suspended chords.
- Ominous but beautiful.

#### Victory

- Warm C major.
- Soft chord swell.
- Satisfying resolution.

### Dynamic Mixing Rules

| Game State | Music Mix |
|---|---|
| Title | Station 100% |
| Station safe zone | Station 100% |
| Field, not towing | Field 70% |
| Towing | Field 60% + Tow 50% |
| Tow stress above 75% | Add Stress 50%, duck Field by 6 dB |
| Mine armed | Play Mine stinger, duck music by 10 dB |
| Mine explosion | Duck music by 15 dB for 1 second |
| Final corridor | Final 80% |
| Contract complete | Play Contract complete stinger, music continues |
| Victory | Crossfade to Victory over 3 seconds |
| Paused | Reduce music by 6 dB |
| Game over | Stop music, play ship destroyed SFX, then low game-over drone |

### Transition Rules

- Crossfade between music stems over 2 seconds.
- Do not cut music abruptly except on death.
- SFX should not fight the music.
- Important SFX, such as mine arming and tow snap, should briefly duck the music.

Why:

- The game is about careful piloting.
- Music should create safety, tension, and payoff without making the player feel rushed.

---

## 17. Sound Effects

### Audio Design Rules

- Audio should emphasize safety, danger, and success.
- Gameplay must not depend on hearing audio.
- Every important audio cue must have a visual equivalent.
- Use positional audio for world objects.
- Pan based on screen position.
- Attenuate by distance.
- Keep SFX short and clear.

### SFX List

| Event | File Name | Character | Duration | Notes |
|---|---|---|---:|---|
| UI hover | `sfx_ui_hover.wav` | Short high blip | 0.05 s | 1200 Hz sine |
| UI click | `sfx_ui_click.wav` | Short click | 0.08 s | 800 Hz |
| Thrust loop | `sfx_thrust_loop.wav` | Low rumble + hiss | Loop | Pitch increases with speed |
| Brake | `sfx_brake.wav` | Soft reverse hiss | 0.2 s | Low-pass noise |
| Turn | `sfx_turn.wav` | Subtle servo | 0.1 s | Quiet |
| Tow attach | `sfx_tow_attach.wav` | Metallic clunk + latch | 0.25 s | 150 Hz thump + 1500 Hz latch |
| Tow detach | `sfx_tow_detach.wav` | Release clank + slack | 0.2 s | Lower pitch than attach |
| Tow stress loop | `sfx_tow_stress_loop.wav` | Creaking strain | Loop | Pitch rises with stress |
| Tow snap | `sfx_tow_snap.wav` | Sharp snap + ping + thud | 0.3 s | 2000 Hz snap, 1000 Hz ping, 60 Hz thud |
| Hull damage | `sfx_hull_damage.wav` | Impact + alarm blip | 0.3 s | 100 Hz impact + 800 Hz blip |
| Wreck damage | `sfx_wreck_damage.wav` | Metallic clang + sparks | 0.2 s | 500 Hz clang |
| Mine armed | `sfx_mine_arm_loop.wav` | High beep | Loop | 2000 Hz, 2 Hz rate |
| Mine explosion | `sfx_mine_explosion.wav` | Boom + sub drop | 0.8 s | 50 Hz boom + noise |
| Unload start | `sfx_unload_start.wav` | Servo + hum | 0.3 s | 300 Hz servo |
| Unload complete | `sfx_unload_complete.wav` | Success chime + cargo drop | 0.4 s | 800 Hz + 1200 Hz |
| Contract complete | `sfx_contract_complete.wav` | Short fanfare | 0.6 s | Four-note warm chime |
| Ship destroyed | `sfx_ship_destroyed.wav` | Explosion + hull breach | 1.2 s | Large boom + metallic break |
| Victory | `sfx_victory.wav` | Warm victory chime | 1.0 s | C major resolution |
| Boundary warning | `sfx_boundary_warning.wav` | Soft ping | 0.2 s | 600 Hz |
| Scanner ping | `sfx_scanner_ping.wav` | Sonar ping | 0.1 s | 1000 Hz |
| Upgrade buy | `sfx_upgrade_buy.wav` | Servo + part click | 0.3 s | Satisfying mechanical click |
| Part pickup | `sfx_part_pickup.wav` | Small chime | 0.1 s | 1500 Hz |

### Positional Audio

For world SFX:

- Pan left/right based on object position relative to camera.
- Attenuate volume with distance.
- Use a simple distance curve:
  - 0–200 units: full volume.
  - 200–800 units: linear attenuation.
  - Beyond 800 units: -18 dB.

Why:

- Top-down space still benefits from spatial audio.
- The player should hear mines and explosions in the correct direction.

### Volume Balance

| Category | Reference Level |
|---|---:|
| Music | -12 dB |
| World SFX | 0 dB |
| UI SFX | 0 dB |
| Critical SFX | +3 dB |

Critical SFX include:

- Mine armed.
- Mine explosion.
- Tow snap.
- Hull damage.
- Ship destroyed.
- Contract complete.

Why:

- Critical events must cut through ambient music.

---

## 18. Accessibility and Readability

### Colorblind Accessibility

Use shape, brightness, and motion in addition to color.

- Player: cyan arrow.
- Danger: red plus white warning ring.
- Success: green plus check or plus symbol.
- Wrecks: size and silhouette.
- Mines: blinking sphere plus warning ring.
- Locked wrecks: dark gray plus no light.

### Low Vision Accessibility

- Minimum readable text: 16 px.
- High contrast HUD.
- Large hull bar.
- Clear prompt keycaps.
- Avoid small detail in important silhouettes.

### Motion Accessibility

- Screen shake maximum 6 px.
- No full-screen shake.
- Keep shake duration under 300 ms.
- If a reduce-motion option is added, disable non-essential shake and particle trails.

### Photoepilepsy Safety

- No full-screen flashes.
- No flashing faster than 3 Hz.
- Mine blink maximum 2 Hz.
- Explosion flash under 100 ms.
- No rapid strobing in UI or background.

### Audio Independence

All critical information must also be visible:

- Attach failures.
- Tow stress.
- Mine arming.
- Hull damage.
- Contract completion.
- Unload progress.
- Boundary warning.
- Death.
- Victory.

Why:

- The game should be fully playable with audio off.

---

## 19. Asset List

### Sprites

| Asset | Size | Notes |
|---|---:|---|
| `player_ship_base.png` | 64 x 64 | Base salvage tug |
| `player_ship_hull_1.png` | 64 x 64 | Hull Plating Level 1 |
| `player_ship_hull_2.png` | 64 x 64 | Hull Plating Level 2 |
| `player_ship_hull_3.png` | 64 x 64 | Hull Plating Level 3 |
| `player_ship_thruster_1.png` | 64 x 64 | Thruster Level 1 |
| `player_ship_thruster_2.png` | 64 x 64 | Thruster Level 2 |
| `player_ship_thruster_3.png` | 64 x 64 | Thruster Level 3 |
| `player_ship_tow_0.png` | 64 x 64 | Tow Servo Level 0 |
| `player_ship_tow_1.png` | 64 x 64 | Tow Servo Level 1 |
| `player_ship_tow_2.png` | 64 x 64 | Tow Servo Level 2 |
| `player_ship_tow_3.png` | 64 x 64 | Tow Servo Level 3 |
| `player_ship_scanner_1.png` | 64 x 64 | Scanner Level 1 |
| `player_ship_scanner_2.png` | 64 x 64 | Scanner Level 2 |
| `wreck_scrap.png` | 64 x 64 | Scrap Can |
| `wreck_hauler.png` | 64 x 64 | Transport Hauler |
| `wreck_fighter.png` | 64 x 64 | Fighter Frame |
| `wreck_liner.png` | 80 x 80 | Cargo Liner |
| `wreck_aurora.png` | 80 x 80 | Aurora Black Box |
| `wreck_locked.png` | 64 x 64 | Generic locked wreck silhouette |
| `debris_cluster.png` | 128 x 128 | Scalable debris cluster |
| `mine.png` | 32 x 32 | Mine dormant/armed base |
| `station.png` | 256 x 256 | Station core and arms |
| `safe_zone.png` | 256 x 256 | Safe zone ring |
| `dock_zone.png` | 128 x 128 | Dock zone ring |

### UI

| Asset | Size | Notes |
|---|---:|---|
| `ui_panel.png` | 512 x 512 | Repeating panel texture |
| `ui_button.png` | 256 x 64 | Button states |
| `ui_keycap.png` | 32 x 32 | Keycap base |
| `icon_hull.png` | 20 x 20 | Shield |
| `icon_speed.png` | 20 x 20 | Gauge |
| `icon_parts.png` | 20 x 20 | Hex bolt |
| `icon_contract.png` | 20 x 20 | Clipboard |
| `icon_tow.png` | 20 x 20 | Hook |
| `icon_scanner.png` | 20 x 20 | Radar |
| `icon_mine.png` | 20 x 20 | Mine warning |

### Effects

| Asset | Notes |
|---|---|
| `particle_thrust.png` | Orange/white thrust particles |
| `particle_spark.png` | Damage sparks |
| `particle_smoke.png` | Low integrity smoke |
| `particle_explosion.png` | Mine and ship explosion |
| `particle_unload.png` | Unload success particles |
| `particle_score.png` | Score/part popup background |
| `fx_tow_line.png` | Tow line base, can be drawn procedurally |
| `fx_shockwave.png` | Mine explosion shockwave |
| `fx_scan_ring.png` | Scanner sweep |
| `fx_safe_zone.png` | Safe zone pulse |
| `fx_dock_zone.png` | Dock chevrons |

---

## 20. Integration Notes

### Visual State Flags

The visual system should receive these flags or values:

#### Ship

- `hull_percent`
- `speed`
- `thrust_active`
- `brake_active`
- `towing`
- `hull_level`
- `thruster_level`
- `tow_level`
- `scanner_level`

#### Wreck

- `state`: `locked`, `active`, `towed`, `unloadded`
- `tier`
- `integrity_percent`
- `scanner_data_visible`
- `is_final`

#### Mine

- `state`: `dormant`, `armed`, `exploding`
- `scanner_level`

#### Tow

- `stress_ratio`
- `attachable`
- `attach_fail_reason`
- `snap_warning_active`

#### Station

- `in_safe_zone`
- `in_dock_zone`
- `contract_progress`
- `contract_complete`
- `ring_unlocked`
- `checkpoint_saved`

#### UI

- `active_prompt`
- `prompt_type`: `info`, `warning`, `failure`, `success`
- `upgrade_menu_open`
- `paused`
- `game_over`
- `victory`

### Important Presentation Rules

- Station is not solid. Do not visually imply a solid wall.
- Safe zone and dock zone must be distinct.
- Tow line must show tension.
- Wreck tier must be distinguishable by size and color.
- Aurora Black Box must be visually distinct.
- Hull damage must flash or pulse.
- Wreck integrity must be readable when towing.
- Mines must have a clear warning state before explosion.
- Contract completion must be clearly communicated.
- Death must be clearly communicated.
- Locked wrecks may be visible but must look inert.
- Locked rings must not appear on the minimap.
- Visual size must not change collision behavior.
- Audio is optional for gameplay.

### Seeded Visual Variation

Use the run seed for visual variation only:

- Starfield placement.
- Dust placement.
- Debris cluster shape.
- Wreck rotation.
- Nebula cloud placement.

Do not use visual variation to change gameplay positions or collision radii.

Why:

- Each run should feel slightly different.
- Gameplay fairness must remain deterministic.

---

## 21. Cuts

Do not include:

- Weapon visuals.
- Enemy ships.
- Enemy fire.
- Combat UI.
- Cargo capacity UI.
- Multiple part type icons.
- Fuel or oxygen gauges.
- Repair kit UI.
- Trading UI.
- Multiple station UIs.
- Vertical depth effects.
- 3D rotation.
- Complex narrative screens.
- Save system UI.
- Decorative objects that could be confused with wrecks, debris, or mines.

Why:

- The core verb is towing.
- Any visual system that competes with towing, station safety, or salvage readability should be cut.

---

## 22. Optional Procedural Generation Notes

The following snippets are optional references for generating base assets. They are not required for gameplay integration.

### Starfield Layer

```python
from PIL import Image, ImageDraw
import random

def make_starfield(size=(1280, 720), stars=500, seed=1):
    random.seed(seed)
    img = Image.new("RGBA", size, (5, 7, 13, 255))
    draw = ImageDraw.Draw(img)

    for _ in range(stars):
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1)
        r = random.choice([1, 1, 1, 2])
        color = random.choice([
            (255, 255, 255, 180),
            (191, 217, 255, 160),
            (255, 230, 196, 140),
        ])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)

    img.save("starfield.png")
```

### Debris Cluster Silhouette

```python
from PIL import Image, ImageDraw
import random
import math

def make_debris(radius=40, seed=2):
    random.seed(seed)
    size = radius * 4
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = size // 2

    for _ in range(random.randint(4, 7)):
        points = []
        base_r = random.randint(radius // 3, radius // 2)
        x0 = center + random.randint(-radius, radius)
        y0 = center + random.randint(-radius, radius)

        for i in range(8):
            angle = i / 8 * math.tau
            r = base_r * random.uniform(0.6, 1.2)
            x = x0 + math.cos(angle) * r
            y = y0 + math.sin(angle) * r
            points.append((x, y))

        fill = random.choice([
            (42, 47, 58, 255),
            (58, 52, 48, 255),
            (64, 58, 50, 255),
        ])
        draw.polygon(points, fill=fill, outline=(10, 12, 16, 255))

    img.save(f"debris_{radius}.png")
```

### Simple UI Hover SFX

```python
import numpy as np
from scipy.io.wavfile import write

def make_ui_hover(freq=1200, duration=0.05, sr=44100):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    env = np.exp(-12 * t)
    wave = np.sin(2 * np.pi * freq * t) * env
    write("sfx_ui_hover.wav", sr, (wave * 32767).astype(np.int16))
```

### Simple Mine Beep

```python
import numpy as np
from scipy.io.wavfile import write

def make_mine_beep(freq=2000, duration=0.08, sr=44100):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    env = np.exp(-10 * t)
    wave = np.sin(2 * np.pi * freq * t) * env
    write("sfx_mine_arm_loop.wav", sr, (wave * 32767).astype(np.int16))
```