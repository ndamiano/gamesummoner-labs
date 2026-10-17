# visual.md

## 1. Document Purpose

This document is the visual, UX, and audio source of truth for **FROG: POND TO PEAK**.

It defines:

- the coherent visual style
- the UI/UX layout and flow
- level art direction
- entity visuals
- animation and feedback
- music
- sound effects
- accessibility and readability rules
- asset sizes and animation timings
- cuts

It does **not** change gameplay behavior. If a visual choice would change gameplay, keep the gameplay rule and change the visual presentation.

Handoff priority:

- `gameplay.md` wins for behavior, numbers, hitboxes, state rules, and required events.
- `visual.md` wins for presentation, layout, style, animation, audio, and UX clarity.

---

## 2. Core Visual Identity

### Working title

**FROG: POND TO PEAK**

### Core visual fantasy

A small, bright frog makes a big journey through a readable pond world.

The game should look:

- small
- bright
- bouncy
- calm
- forgiving
- readable

The world should feel like a living pond: water, leaves, lily pads, reeds, rain, cliffs, and a final waterfall.

### Visual style

Use **soft pixel art** with a friendly, rounded look.

Rules:

- Base pixel grid: 16 logical pixels.
- Render scale: 2x.
- Tile size: 32 px.
- Use nearest-neighbor scaling.
- Round sprite draw positions to a 2 px screen grid to avoid shimmer.
- Use limited palettes per level.
- Use high contrast for gameplay objects.
- Use low contrast for background decoration.
- Use clear silhouettes.
- Use simple shapes.
- Avoid photorealism.
- Avoid overly sharp or noisy textures.

### Why this style

A small frog platformer needs readable spacing, clear hazards, and clear safe surfaces. Soft pixel art keeps the game cozy and small while still giving crisp platforming feedback. Limited palettes keep the levels distinct but coherent.

---

## 3. Global Visual Rules

### Logical resolution

- 1280 x 720 px.
- Tile size: 32 px.
- All UI coordinates are in logical pixels.

### Layer priority

From back to front:

1. Sky / far background
2. Midground scenery
3. Gameplay tiles and entities
4. Particles and effects
5. HUD and menus

### Contrast rules

- Background: low saturation, low detail.
- Midground: medium saturation.
- Gameplay objects: full saturation and clear outlines.
- HUD: highest contrast.

No decorative background element should look like a gameplay object.

Examples:

- Background lily pads must be dimmer, smaller, and non-interactive.
- Background leaves must not look like one-way platforms.
- Background thorn-like shapes are forbidden.
- Background water must not look like a playable water rectangle unless it is actual water.

### Outlines

Use outlines to separate important objects from the background.

Recommended outline colors:

- Dark green outline: `#1B2A1F`
- Dark blue outline: `#16324A`
- Dark red outline: `#5A1F1A`

Use 1–2 px outlines depending on sprite size.

### Color roles

These color roles stay consistent across all levels.

| Role | Color | Purpose |
|---|---:|---|
| Safe ground | warm brown / moss green | walkable solid surface |
| One-way leaf | pale yellow-green | thin platform, not bouncy |
| Lily pad | bright saturated green | bouncy platform |
| Water | blue / cyan | safe movement space |
| Current | cyan arrows | horizontal force direction |
| Hazard | red / orange | damage |
| Collectible | white / cyan dewdrop | optional pickup |
| Checkpoint | pink / white lotus | respawn and heal |
| Exit | white / blue waterfall | level objective |
| Player | bright green | protagonist |
| Enemy | indigo / cyan / slate | threat |
| UI accent | amber | selection, perfect, important highlight |

### Accessibility rules

- Do not rely on color alone.
- Hazards use shape and color.
- Water uses blue plus surface animation.
- Currents use arrows.
- Lily pads use shape, brightness, and bounce feedback.
- One-way leaves use thinness and leaf shape.
- Text must remain readable on all backgrounds.
- Use text outline or panel behind text.
- Avoid strobing.
- Maximum blink rate: 8 Hz.
- No gameplay-critical information should appear only in the top 64 px except HUD.
- No lightning gameplay effects.
- No motion that hides hitboxes.

### Animation timing

All animations run at 60 logical updates per second.

Use frame-based timing where possible.

General timing:

- Fast UI animation: 0.15 s
- Medium UI animation: 0.25 s
- Fast effect: 0.10 s
- Medium effect: 0.20 s
- Large effect: 0.40 s

### Effects rules

Effects must support gameplay, not hide it.

Rules:

- Effects must not obscure the player hitbox for more than 2 frames.
- Effects must not obscure enemy hitboxes for more than 2 frames.
- Particle count should stay small.
- Recommended maximum active particles: 128.
- Use simple shapes: circles, lines, small pixel blobs.
- No heavy post-processing.
- No blur that hides gameplay.
- No full-screen flash.

### Screen shake

Use very small screen shake only for strong feedback.

| Event | Shake | Duration |
|---|---:|---:|
| Stomp | 2 px | 0.05 s |
| Boss hit | 3 px | 0.08 s |
| Boss death | 6 px | 0.20 s |
| Player damage | 2 px | 0.05 s |

No screen shake for:

- normal running
- normal jumping
- normal landing
- water splash
- menu actions

Why: the game should feel bouncy but not dizzy. The player is small and the world should stay readable.

---

## 4. Typography and UI Style

### Font

Use a clean pixel font.

Recommended base font:

- 9 x 18 pixel font.
- Scale 1x = 18 px.
- Scale 2x = 36 px.
- Scale 3x = 54 px.

If an exact font is unavailable, use a readable monospace pixel font with similar proportions.

### Text sizes

| Use | Size |
|---|---:|
| Small / prompt | 18 px |
| Heading | 36 px |
| Title | 54 px |

### Text color

- Primary text: `#FFFFFF`
- Secondary text: `#D8E8E0`
- Accent text: `#FFC24A`
- Danger text: `#FF6A5A`
- Text outline: `#1B2A1F`
- Text shadow: 2 px downward, `rgba(0,0,0,0.35)`

Outline scale:

- 18 px text: 2 px outline
- 36 px text: 3 px outline
- 54 px text: 4 px outline

### UI panel

Use rounded panels for menus and messages.

Panel style:

- Fill: `rgba(16, 28, 24, 0.72)`
- Border: `rgba(255, 255, 255, 0.18)`
- Corner radius: 12 px
- Padding: 16 px

### UI animation

- Fade in/out: 0.15 s
- Slide in: 0.20 s
- Menu select pulse: 0.10 s
- Heart refill: 0.20 s
- Dewdrop count pulse: 0.15 s

### Why

A short platformer needs menus that are instantly readable. One panel style, one font family, and one accent color keep the UI coherent without competing with the level art.

---

## 5. Player Frog Visuals

### Visual bounds

- Frog visual size: 32 x 32 px.
- Player hitbox: 20 x 28 px.
- Horizontal alignment: center frog visual on player center X.
- Vertical alignment: align frog visual bottom to player hitbox bottom.

This makes the frog’s feet visually touch the ground.

### Frog palette

| Part | Color |
|---|---:|
| Body | `#59C94C` |
| Light body | `#8FE76B` |
| Belly | `#EAF9D8` |
| Outline | `#1B2A1F` |
| Eye white | `#FFFFFF` |
| Pupil | `#111111` |
| Hurt tint | `#FF5A5A` |
| Death tint | `#8A9A92` |

### Frog states

| State | Visual |
|---|---|
| Idle | slight breathing, 2 frames |
| Run | 4-frame leg cycle, body leans forward |
| Jump | legs tucked, eyes slightly up |
| Fall | legs splayed |
| Swim | body more horizontal, legs kick |
| Surface jump | small crouch before leaving water |
| Lily bounce | squash on pad, then stretch upward |
| Stomp | feet down, eyes focused |
| Hurt | red tint, eyes squeezed |
| Invulnerable | blink between full opacity and 35% opacity |
| Death | gray tint, X eyes, deflate / fall over |

### Animation timing

| Animation | Frames | Rate |
|---|---:|---:|
| Idle | 2 | 12 fps |
| Run | 4 | 12 fps |
| Swim | 2 | 8 fps |
| Death | 2 | 10 fps |
| Bounce squash | 1 | instant |
| Hurt | 1 | instant |

### Facing

The frog must clearly face left or right.

Rules:

- Eyes and body orientation indicate facing.
- Mirror the sprite for left/right.
- In water, facing follows horizontal input.
- During invulnerability, the frog blinks but still faces the last movement direction.

### Invulnerability

- Duration: 1.2 s.
- Blink: full opacity and 35% opacity.
- Blink rate: 8 Hz.
- The frog remains visible enough to track.

Why: the player needs to know they are safe, but the frog should not disappear completely.

### Death

Death animation:

1. Stop input.
2. Frog turns gray.
3. Eyes become X.
4. Frog deflates or falls over.
5. Duration: 0.6 s.
6. Then fade to respawn.

Screen effect:

- Slight desaturation: 20% for 0.3 s.
- No red flash.

Why: death should feel sad and small, not violent.

### Player feedback effects

| Event | Visual |
|---|---|
| Run on ground | small dust puffs every 0.15 s |
| Jump | small dust puff or water splash if near water |
| Land on ground | small dust puff |
| Enter water | splash ring and droplets |
| Swim | small bubbles |
| Lily pad bounce | green bounce ring and pad squash |
| Stomp | puff and enemy squish |
| Damage | red flash on frog for 2 frames |
| Checkpoint | hearts refill with pulse |

---

## 6. World Objects

## 6.1 Solid Ground

Solid ground is the main walkable surface.

### Visual rules

- Top edge: 6 px bright grass, moss, or stone highlight.
- Body: dirt, stone, or mud depending on level.
- Sides: darker fill.
- Corners: rounded or beveled pixel corners.
- Ground must be clearly darker or more textured than background.

### Ground tile variants

Use at least:

- top-left
- top-right
- top
- left
- right
- fill
- bottom-left
- bottom-right

### Why

Ground is the safest visual in the game. It should always read as “I can stand here.”

---

## 6.2 One-Way Leaf Platforms

One-way platforms are thin leaf platforms.

### Hitbox

- Width: 128 px.
- Height: 16 px.
- Visual top aligns with hitbox top.

### Visual size

- 128 x 16 px.

### Appearance

- Thin leaf shape.
- Pale yellow-green color.
- Slight stem or tip on one end.
- Visible underside shadow.
- No bounce indicator.
- No thick top edge.

### Palette

| Part | Color |
|---|---:|
| Leaf top | `#C9D97A` |
| Leaf shadow | `#7FA34A` |
| Stem | `#5C7A32` |
| Outline | `#1B2A1F` |

### Behavior visuals

- When the player lands, the leaf bends down 2–3 px.
- When the player leaves, the leaf returns over 0.10 s.
- Moving leaf platforms get a faint motion trail.

### Why

One-way leaves must look thin enough to pass through from below, but solid enough to stand on from above. They must not look like lily pads.

---

## 6.3 Moving Platforms

Moving platforms are one-way leaf platforms that move on a sine path.

### Visual rules

- Same leaf shape as static one-way platforms.
- Add 2 faint trail copies behind the motion direction.
- Trail alpha: 0.30 and 0.15.
- Slight tilt in motion direction.
- When carrying the player, the leaf bends 3 px.

### Why

The player needs to understand that the platform moves and carries them. Motion trails make this obvious without adding a new UI symbol.

---

## 6.4 Lily Pads

Lily pads are bouncy one-way platforms.

### Hitbox

- Width: 64 px.
- Height: 16 px.
- Visual top aligns with hitbox top.

### Visual size

- 64 x 24 px.
- The top 16 px are the bounce surface.
- The lower 8 px are pad thickness.

### Appearance

- Bright green oval pad.
- Small notch or leaf vein.
- One white/cyan water droplet near center.
- Soft dark outline.
- Slight highlight on top edge.

### Palette

| Part | Color |
|---|---:|
| Pad | `#4FCB5A` |
| Light pad | `#8BEA86` |
| Dark pad | `#2E8A3E` |
| Droplet | `#DFFBFF` |
| Outline | `#1B2A1F` |

### Bounce visuals

When the player bounces:

1. Pad squashes vertically by 20% for 2 frames.
2. A green ring expands from the pad.
3. 3–4 small water droplets pop upward.
4. If the player held Jump, the ring is slightly brighter.

### Why

Lily pads are the frog’s signature tool. They should look bouncy, rewarding, and distinct from normal leaf platforms.

---

## 6.5 Water

Water is a movement space, not a hazard.

### Visual rectangle

Water visuals match the gameplay water rectangle exactly.

### Appearance

- Surface: animated bright cyan line.
- Body: blue gradient from top to bottom.
- Transparency: enough to see the frog underwater.
- Recommended water overlay: `rgba(42, 123, 181, 0.65)`.
- Surface highlight: `#7FD8FF`.
- Deep water: `#2A7BB5`.

### Surface animation

- 4-frame wave loop.
- 8 fps.
- Small vertical offset: 1–2 px.

### Water effects

| Event | Visual |
|---|---|
| Enter water | splash ring, 4–6 droplets |
| Swim upward | small bubbles below frog |
| Swim horizontally | small wake behind frog |
| Surface jump | small ripple |
| Bounce into water | splash ring |

### Why

Water should look inviting. The frog belongs there. If water looks dark or dangerous, it undermines the core fantasy.

---

## 6.6 Water Currents

Currents apply horizontal force inside water.

### Visual representation

Use animated chevrons inside the water rectangle.

Rules:

- Chevron size: 16 x 8 px.
- Chevron spacing: 64 px horizontally.
- Chevron color: `#BFF6FF`.
- Alpha: 0.50.
- Movement speed: 60 px/s in the current direction.
- Right current: chevrons point right and move right.
- Left current: chevrons point left and move left.

### Do not use

- Large arrows outside water.
- Text labels.
- Strong color changes that hide the frog.

### Why

Currents need to be readable but subtle. The player should understand “this water pushes me” without the effect becoming a visual hazard.

---

## 6.7 Thorns

Thorns are static damage hazards.

### Hitbox

- 48 x 16 px.

### Visual size

- 48 x 16 px.

### Appearance

- 5 red/orange spikes.
- Dark base.
- Bright tip.
- No animation.
- No pulsing.

### Palette

| Part | Color |
|---|---:|
| Spike | `#E84A3F` |
| Light spike | `#FF7A5C` |
| Dark base | `#8A2A22` |
| Outline | `#1B2A1F` |

### Why

Thorns should be instantly readable as danger. No animation keeps them from distracting from moving enemies and water.

---

## 6.8 Dewdrops

Dewdrops are optional collectibles.

### Hitbox

- 16 x 16 px.
- Centered on listed coordinates.

### Visual size

- 16 x 16 px.

### Appearance

- Small water droplet.
- White highlight.
- Cyan body.
- Gentle bob.
- Occasional sparkle.

### Palette

| Part | Color |
|---|---:|
| Body | `#DFFBFF` |
| Highlight | `#FFFFFF` |
| Shadow | `#6FD8FF` |

### Animation

- Bob: 4 px vertical sine.
- Period: 1.2 s.
- Sparkle: every 0.8 s.

### Collect visual

- Dewdrop pops upward 4 px.
- Fades over 0.15 s.
- 4 small sparkle particles.
- HUD dewdrop icon pulses.

### Why

Dewdrops are optional, so they should look pretty and rewarding, not urgent.

---

## 6.9 Lotus Checkpoints

Checkpoints are lotus flowers.

### Hitbox

- 32 x 32 px.
- Centered on listed coordinates.

### Visual size

- 32 x 32 px.

### States

| State | Visual |
|---|---|
| Inactive | dim lotus, petals slightly closed |
| Active | bright lotus, petals open, soft glow |
| Touching | bloom animation, petals open fully, small sparkles |

### Palette

| Part | Color |
|---|---:|
| Petal | `#FFB7D5` |
| Light petal | `#FFD9E8` |
| Dark petal | `#C76BA0` |
| Stem | `#5C8A4A` |
| Glow | `rgba(255, 183, 213, 0.35)` |

### Bloom animation

- 4 frames.
- 12 fps.
- Duration: 0.30 s.

### Checkpoint feedback

When touched:

- Lotus blooms.
- Hearts refill with a bottom-to-top fill animation.
- Message: “Checkpoint” appears.
- Small pink sparkle particles.

### Why

Checkpoints should feel like relief. The lotus should look calm, safe, and rewarding.

---

## 6.10 Waterfall Exits

Exits are waterfall portals.

### Hitbox

- 48 x 64 px.
- Centered on listed coordinates.

### Visual size

- 64 x 80 px.
- Centered on hitbox center.

### Active exit

Use for all normal exits and for Level 6 after the boss dies.

Appearance:

- Vertical white/blue waterfall.
- Bright core.
- Blue edges.
- Mist at bottom.
- Small bubbles.
- 4-frame flow loop.
- 10 fps.

Palette:

| Part | Color |
|---|---:|
| Core | `#FFFFFF` |
| Water | `#BFEFFF` |
| Edge | `#6FCBFF` |
| Mist | `rgba(255, 255, 255, 0.35)` |

### Locked exit

Use only for Level 6 before the boss dies.

Appearance:

- Still dark blue sheet.
- No flow.
- No mist.
- Small dark lotus seal at center.
- Slightly dimmer than active exit.

Palette:

| Part | Color |
|---|---:|
| Water | `#4A7A9A` |
| Edge | `#2F4F6A` |
| Seal | `#1B2A1F` |

### Activation visual

When the boss dies:

1. Lotus seal cracks.
2. Water bursts outward.
3. Mist appears.
4. Exit becomes active.
5. Duration: 0.40 s.

### Why

The exit is always the objective. Active and locked states must be visually obvious without text.

---

## 6.11 Level Bounds

Levels have left, right, and top bounds.

### Visual rules

- Left/right bounds: show reeds, cliffs, rocks, or foliage.
- Top bound in vertical levels: show canopy, rocks, or cliff ceiling.
- Do not draw invisible walls as bright lines.
- Boundaries should feel natural.

### Death below level

When the player falls below the level:

- Fade out over 0.20 s.
- No explosion.
- No red flash.
- Then respawn fade in.

Why: falling should feel like the frog slipped away, not like a violent event.

---

## 7. Enemy Visuals

## 7.1 Mosquito

### Hitbox

- 24 x 20 px.

### Visual size

- 32 x 28 px.
- Centered on hitbox center.

### Appearance

- Small dark indigo body.
- Thin legs.
- Fast wing flap.
- Small red eyes.
- Clear top surface for stomping.

### Palette

| Part | Color |
|---|---:|
| Body | `#5A5F7A` |
| Wing | `#C9D9FF` |
| Eye | `#FF5A5A` |
| Outline | `#1B2A1F` |

### Animation

- Wings: 2 frames, 20 fps.
- Body bob: small sine.

### Stomp visual

- Mosquito squashes.
- 4 small particles.
- Fades over 0.20 s.

### Why

Mosquitoes should look small, slow, and stompable. Their silhouette should be readable even at distance.

---

## 7.2 Dragonfly

### Hitbox

- 28 x 16 px.

### Visual size

- 32 x 24 px.
- Centered on hitbox center.

### Appearance

- Long cyan body.
- Two pairs of wings.
- Faster wing flap than mosquito.
- Slight motion streak when moving fast.

### Palette

| Part | Color |
|---|---:|
| Body | `#2FA8C8` |
| Light body | `#4FD8D8` |
| Wing | `#DFFBFF` |
| Eye | `#FF5A5A` |
| Outline | `#1B2A1F` |

### Animation

- Wings: 2 frames, 24 fps.
- Motion streak: 2 px, alpha 0.25.

### Stomp visual

- Dragonfly squashes sideways.
- Wings flutter.
- 4 small particles.
- Fades over 0.20 s.

### Why

Dragonflies are faster than mosquitoes. Their longer body and cyan color make them distinct while staying in the pond theme.

---

## 7.3 Heron Boss

The boss is a heron.

### Hitbox

- 56 x 80 px.
- Bottom aligned to ground top.

### Visual size

- 64 x 80 px.
- Bottom aligned to hitbox bottom.
- Horizontally centered on hitbox center.

### Appearance

- Tall slate-gray bird.
- Long neck.
- Long beak.
- Large readable head.
- Soft feather shapes.
- Red eye.
- Clear head target.

### Palette

| Part | Color |
|---|---:|
| Body | `#8A93A8` |
| Light feather | `#C0C8D8` |
| Dark feather | `#4A5268` |
| Beak | `#E8A33F` |
| Eye | `#FF5A5A` |
| Stomp band | `#BFF6FF` |
| Phase 2 accent | `#FFC24A` |

### Stomp zone

The stomp zone is the top 12 px of the heron hitbox.

Visual:

- Draw a 12 px tall cyan band across the head.
- Band width: 40 px.
- Band color: `#BFF6FF`.
- Band alpha: 0.80.
- When hit, the band flashes white for 2 frames.

Why: the player only needs to learn one target: the head.

### Boss states

| State | Visual |
|---|---|
| Idle | neck up, slight breathing, blink every 2.5 s |
| Lunge | leans forward, beak extends slightly, eyes focused |
| Recover | neck retracts, body wobbles slightly |
| Dead | lies down, eyes closed, feathers puff, no movement |

### Animation timing

| State | Frames | Rate |
|---|---:|---:|
| Idle | 2 | 6 fps |
| Lunge | 2 | 12 fps |
| Recover | 1 | instant |
| Dead | 2 | 8 fps |

### Boss HP visual

Use 6 small water droplets above the heron.

Rules:

- Droplet size: 12 x 12 px.
- Spacing: 4 px.
- Centered above heron head.
- Remaining HP: bright cyan droplets.
- Lost HP: droplet fades and disappears.
- Phase 2, HP 3 or less: droplets turn amber `#FFC24A`.

Why: boss HP should be local to the boss, not added to the HUD. This keeps the HUD clean and the boss readable.

### Phase 2 visual

When HP is 3, 2, or 1:

- Heron feathers become slightly ruffled.
- Eye stays red.
- Stomp band remains cyan.
- HP droplets turn amber.
- Heron idle animation becomes slightly faster.

Why: phase 2 should feel more urgent without changing the visual language.

### Boss death visual

When HP reaches 0:

1. Heron flashes white for 2 frames.
2. HP droplets vanish.
3. Heron deflates.
4. Feathers puff outward.
5. Heron lies down.
6. Exit activates.

Duration: 0.60 s.

---

## 8. Level Art Direction

All levels share the same base style, tile logic, and color roles. Levels differ by palette, background, weather, and mood.

### Shared level rules

- Use the same gameplay object shapes.
- Recolor backgrounds and ground per level.
- Keep background low contrast.
- Keep gameplay objects high contrast.
- Do not add decorative hazards.
- Do not add decorative platforms that look like real platforms.
- Do not add decorative enemies.
- Do not add visual noise near jump paths.

### Vertical level orientation

In vertical levels, when the exit is above the camera, show a soft waterfall glow at the top edge.

Rules:

- Glow height: 16 px.
- Color: `rgba(191, 239, 255, 0.35)`.
- No arrow.
- No text.
- No gameplay effect.

Why: the player needs a subtle sense of “the waterfall is up there” without an objective arrow.

---

## 8.1 Level 1: Pond Edge

### Mood

Bright, calm, easy, morning pond.

### Palette

| Element | Color |
|---|---:|
| Sky | `#BFEFFF` |
| Distant hills | `#7FCB8A` |
| Ground | `#8A5A3B` |
| Grass | `#6DBE45` |
| Water | `#3FA9E0` |
| Accent | `#FFC24A` |

### Background

- Soft sky gradient.
- Distant rounded hills.
- Light mist near the ground.
- A few background reeds.
- No rain.
- No dark elements.

### Gameplay visual notes

- Ground should look soft and safe.
- First water, if present, should look calm.
- The one mosquito should be clearly visible against the bright background.

### Why

Level 1 teaches the basics. The art should feel welcoming and low-pressure.

---

## 8.2 Level 2: Lily Rush

### Mood

Lush, bouncy, midday pond.

### Palette

| Element | Color |
|---|---:|
| Sky | `#A8F0FF` |
| Water | `#2FA8E0` |
| Lily pads | `#4FCB5A` |
| Leaves | `#C9D97A` |
| Ground | `#7A5A3B` |
| Accent | `#FFD166` |

### Background

- Bright water reflections.
- Background lily pads, dimmer and smaller.
- Soft ripples.
- A few reeds.
- No floating petals.

### Gameplay visual notes

- Water should be the star.
- Lily pads should stand out strongly.
- The dragonfly should be readable against water.

### Why

This level introduces water and lily pad bounce. The art should make water feel fun and bouncy.

---

## 8.3 Level 3: Reed Hollow

### Mood

Quiet, vertical, misty reed marsh.

### Palette

| Element | Color |
|---|---:|
| Sky | `#7FA8C8` |
| Reeds | `#3F7A5A` |
| Water accents | `#2A7BB5` |
| Leaves | `#8FBF6A` |
| Ground | `#6A5A45` |
| Accent | `#B7E4C7` |

### Background

- Tall reed silhouettes.
- Soft mist layers.
- Vertical vines.
- Dim background water pools.
- No fireflies.

### Gameplay visual notes

- One-way leaves should read clearly against reeds.
- The moving platform should have a visible trail.
- The checkpoint lotus should stand out in the mist.

### Why

Level 3 is vertical. The art should emphasize height, calm, and gentle mystery without becoming dark or confusing.

---

## 8.4 Level 4: Stormy Creek

### Mood

Stormy, wet, moving, slightly tense but not scary.

### Palette

| Element | Color |
|---|---:|
| Sky | `#5A7A9A` |
| Clouds | `#3A5A7A` |
| Water | `#2A6B9A` |
| Ground | `#6A4A35` |
| Rain | `rgba(200, 230, 255, 0.35)` |
| Accent | `#FF8C42` |

### Background

- Dark clouds.
- Light rain streaks.
- Wind-blown leaves.
- Darker water.
- No lightning.

### Rain rules

- Rain streaks: 2 px.
- Count: 60.
- Speed: 500 px/s downward.
- Alpha: 0.30.
- No gameplay effect.
- No screen flash.

### Gameplay visual notes

- Currents must be very readable.
- Thorns should stand out on wet ground.
- Water should look moving but still safe.

### Why

Stormy Creek introduces currents. The weather should communicate motion, but the player must never lose track of platforms or hazards.

---

## 8.5 Level 5: Cliffside Ponds

### Mood

Twilight cliffside, vertical, adventurous.

### Palette

| Element | Color |
|---|---:|
| Sky | `#4A5A8A` |
| Moon | `#F5F0D8` |
| Cliffs | `#5C4A3A` |
| Vines | `#3F7A4A` |
| Water | `#2A7BB5` |
| Accent | `#FFD166` |

### Background

- Twilight sky.
- Distant moon.
- Cliff edges.
- Hanging vines.
- Small background ponds.
- No fireflies.

### Gameplay visual notes

- Lily pad chains should be the brightest green objects.
- Moving platforms should have clear trails.
- The dragonfly should be readable against the twilight sky.

### Why

Level 5 is the hardest platforming level. The art should feel ambitious but still clear. Bright lily pads and clear leaves are essential.

---

## 8.6 Level 6: Great Waterfall

### Mood

Grand, bright, final, emotional.

### Palette

| Element | Color |
|---|---:|
| Sky | `#DFF6FF` |
| Waterfall | `#FFFFFF` / `#BFEFFF` |
| Rocks | `#6A7A8A` |
| Mist | `rgba(255, 255, 255, 0.35)` |
| Accent | `#FFC24A` |

### Background

- Large soft waterfall in the distance.
- Bright mist.
- Wet rocks.
- Light rays.
- Floating bubbles.
- No extra enemies in the background.

### Boss arena visual notes

- The arena floor should be simple and bright.
- The heron should be the largest enemy silhouette.
- The locked exit should be visible but clearly inactive.
- The active exit should become the brightest object after boss death.

### Why

Level 6 is the climax. The art should feel like the frog has reached something big, while the boss fight remains readable.

---

## 9. Effects and Feedback

### Effect principles

Effects should answer one question:

**What just happened?**

Every important event needs visual feedback.

---

### Movement effects

| Event | Visual |
|---|---|
| Run | small dust puffs |
| Jump | small dust or splash |
| Land | small dust |
| Water entry | splash ring and droplets |
| Swim | bubbles |
| Surface jump | ripple |
| Lily bounce | green ring and pad squash |

---

### Combat effects

| Event | Visual |
|---|---|
| Stomp enemy | puff, squish, small shake |
| Enemy death | fade and particles |
| Player damage | red flash on frog, heart loss |
| Player invulnerable | blink |
| Boss hit | head flash, feather puff, HP droplet fades |
| Boss death | white flash, feather burst, exit activates |

---

### World effects

| Event | Visual |
|---|---|
| Dewdrop collect | pop and sparkle |
| Checkpoint | lotus bloom, hearts refill |
| Exit touch | level complete transition |
| Exit locked touch | subtle dim pulse |
| Exit activation | seal breaks, water bursts |
| Perfect level complete | golden sparkle around dewdrop count |

---

### UI effects

| Event | Visual |
|---|---|
| Menu select | option pulse and frog cursor moves |
| Menu back | slight panel shift |
| Pause open | dark overlay fade |
| Level complete | panel slide up |
| Game complete | slow fade to ending |

---

### Why

The game should feel responsive and forgiving. Feedback should be immediate but small enough to keep the world readable.

---

## 10. HUD

The HUD has three sections:

1. Health
2. Dewdrop count
3. Message area

There is no timer, score, minimap, objective arrow, or extra status.

---

## 10.1 Health Section

### Location

- Top-left.
- 16 px from left edge.
- 16 px from top edge.

### Layout

- 3 heart icons.
- Each icon: 32 x 32 px.
- Spacing: 8 px.
- Positions:
  - Heart 1: x = 16, y = 16
  - Heart 2: x = 56, y = 16
  - Heart 3: x = 96, y = 16

### Heart states

| State | Visual |
|---|---|
| Full heart | red heart, solid |
| Empty heart | dark outline heart |

### Palette

| Part | Color |
|---|---:|
| Full heart | `#FF5A6E` |
| Empty heart | `#3A4A5A` |
| Heart highlight | `#FFD1DC` |
| Outline | `#1B2A1F` |

### Animations

- Heart loss: heart cracks and fades for 0.20 s, then becomes empty.
- Heart refill: heart fills from bottom to top over 0.20 s.
- Checkpoint refill: all lost hearts refill with a slight pulse.

### Why

Health must be readable at a glance. Three large hearts are enough for a short, forgiving platformer.

---

## 10.2 Dewdrop Section

### Location

- Top-right.
- 16 px from right edge.
- 16 px from top edge.

### Layout

- Dewdrop icon: 24 x 24 px.
- Count text: 18 px.
- Format: `x / y`
- The icon is the rightmost element.
- The text is right-aligned to the left of the icon.

Recommended positions:

- Icon: x = 1240, y = 16
- Text right edge: x = 1232
- Text top: y = 16

### Dewdrop icon

Use the same dewdrop visual as collectibles, scaled to 24 x 24 px.

### Text

- White text.
- Dark outline.
- Right-aligned.

### Animations

- On collect: icon pulses for 0.15 s.
- Count increments immediately.
- On perfect level complete: count text glows amber for 0.50 s.

### Why

The player needs to know optional progress without score pressure. A per-level count is clearer than a global score.

---

## 10.3 Message Section

### Location

- Top-center.
- 48 px below top edge.
- Max width: 600 px.
- Min width: 220 px.
- Height: 48 px.
- Centered at x = 640.

### Panel

- Rounded rectangle.
- Fill: `rgba(16, 28, 24, 0.72)`.
- Border: `rgba(255, 255, 255, 0.18)`.
- Corner radius: 12 px.

### Message priority

Highest to lowest:

1. Level Complete
2. Checkpoint
3. Tutorial prompt
4. Level name

If multiple messages are active, show only the highest priority.

### Message types

| Message | Size | Duration |
|---|---:|---:|
| Level name | 36 px | 2.5 s |
| Tutorial prompt | 18 px | until condition met or 5 s |
| Checkpoint | 36 px | 1.5 s |
| Level Complete | screen, not message | screen state |

### Animation

- Fade in: 0.20 s.
- Fade out: 0.30 s.
- No bounce.
- No slide.

### Why

A single message area avoids HUD clutter. Priority prevents conflicting messages.

---

## 10.4 HUD State Rules

| Game state | HUD behavior |
|---|---|
| Playing | visible |
| Paused | dimmed behind pause overlay |
| Death | visible, dimmed slightly |
| Level Complete | hidden |
| Game Complete | hidden |
| Title | hidden |
| Controls | hidden |

Why: the HUD belongs to gameplay. Menus should feel separate.

---

## 11. Screens and UX Flow

## 11.1 Title Screen

### Background

- Pond at dusk or soft morning.
- Frog sitting on a lily pad.
- Distant waterfall.
- Gentle water animation.
- No gameplay entities.

### Layout

Centered vertically.

| Element | Position / Size |
|---|---|
| Title | y = 180, 54 px |
| Subtitle | y = 250, 18 px |
| Menu start | y = 340 |
| Menu line height | 56 px |

### Title text

```text
FROG: POND TO PEAK
```

### Subtitle

```text
A small jump to the waterfall
```

### Menu options

If no save:

```text
New Game
Controls
```

If save exists and game not complete:

```text
Continue
New Game
Controls
```

If game complete:

```text
Play Again
New Game
Controls
```

### Menu visual

- Selected option: amber rounded highlight.
- Unselected option: white text at 70% opacity.
- Frog cursor: 32 x 32 px, left of selected option.
- Selection highlight size: 280 x 48 px.

### New Game confirmation

If a save exists and New Game is selected:

```text
Start over?

Yes
No
```

Layout:

- Panel: 400 x 160 px.
- Centered.
- “Start over?” at top.
- Yes / No below.
- Yes is selected by default.

### Why

The title should feel like the start of a small journey. The frog cursor reinforces the character without adding complex UI.

---

## 11.2 Controls Screen

### Background

- Dimmed title background.
- Dark panel.

### Layout

| Element | Position / Size |
|---|---|
| Title | y = 100, 36 px |
| List start | y = 180 |
| Line height | 40 px |
| Back prompt | y = 640, 18 px |

### Content

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

### Visual style

- Use text only.
- No keycap assets required.
- Keep lines short.
- Use secondary color for “Menus:” label.

### Why

A short platformer does not need a large controls screen. Text is clear and low-scope.

---

## 11.3 Pause Menu

### Trigger

Esc during Playing.

### Visual

- Dark overlay: `rgba(0, 0, 0, 0.55)`.
- Game and HUD dimmed behind overlay.
- Panel centered.

### Layout

| Element | Position / Size |
|---|---|
| PAUSED | y = 200, 36 px |
| Menu start | y = 300 |
| Menu line height | 56 px |

### Options

```text
Resume
Restart Level
Controls
Quit to Title
```

### Behavior visuals

- Resume: fade out pause overlay.
- Restart Level: fade to black, then level restarts.
- Controls: open Controls screen; returning goes back to Pause.
- Quit to Title: fade to Title.

### Why

Pause should feel like a calm break, not a complex options menu.

---

## 11.4 Level Complete Screen

### Trigger

Player touches active exit in Levels 1–5.

### Visual

- Dark translucent overlay.
- Background level dimmed.
- Panel slides up.

### Layout

| Element | Position / Size |
|---|---|
| LEVEL COMPLETE | y = 180, 36 px |
| Level name | y = 250, 36 px |
| Dewdrops line | y = 320, 36 px |
| Perfect line | y = 380, 36 px |
| Continue prompt | y = 560, 18 px |

### Content

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

### Perfect visual

- Text color: amber `#FFC24A`.
- Dewdrop count pulses.
- Small golden sparkle particles around count.

### Continue behavior

- Press Enter or Space.
- Fade to next level.

### Why

The player should get immediate, simple feedback. No timer or rank keeps the game relaxed.

---

## 11.5 Game Complete Screen

### Trigger

Player touches active exit in Level 6.

### Visual

- Large sky background.
- Tiny lily pad / pond in the distance.
- Small frog silhouette.
- Soft waterfall glow.
- Calm mist.

### Layout

| Element | Position / Size |
|---|---|
| Main text | y = 220, 36 px |
| Subtitle | y = 300, 36 px |
| Prompt | y = 560, 18 px |

### Content

```text
THE FROG REACHED THE GREAT WATERFALL.

The pond is now a small dot in a big sky.

Press Enter or Space to return to title
```

### Visual notes

- The pond should be very small.
- The frog should be a tiny silhouette.
- The sky should feel large.
- No gameplay HUD.

### Why

The ending should complete the journey emotionally without adding a cutscene.

---

## 12. Transitions

Use simple transitions.

| Transition | Style | Duration |
|---|---|---:|
| To title | fade to dark green | 0.20 s |
| Title to level | fade from dark green | 0.20 s |
| Level complete to next level | fade to dark green | 0.20 s |
| Death to respawn | fade out, then fade in | 0.20 s |
| Pause open | dark overlay fade | 0.15 s |
| Pause close | dark overlay fade | 0.15 s |
| Game complete | slow fade | 0.40 s |

Do not use:

- water wipe
- complex iris
- long cinematic transitions
- loading screens with spinners

Why: the game is short. Transitions should be fast and calm.

---

## 13. Audio Direction

The audio should feel:

- small
- bright
- bouncy
- calm
- original
- non-scary

Use original music and original sound effects. Do not use licensed samples.

Recommended style:

- soft chiptune
- wooden percussion
- marimba / xylophone
- gentle pads
- water and wind ambience
- no heavy bass
- no horror elements
- no loud distortion

---

## 13.1 Music States

### Title Music

- Tempo: 90 BPM.
- Scale: A minor pentatonic.
- Mood: calm, curious.
- Instruments: music box, soft pad, light water noise.
- Motif: `E4 - G4 - A4 - C5 - A4 - G4 - E4 - D4`.

### Controls / Pause

- Use current music at -6 dB.
- If opened from title, use Title Music at -6 dB.
- If opened during gameplay, use current level music at -6 dB.

### Level Complete Stinger

- Duration: 0.50 s.
- Notes: `C5 - E5 - G5 - C6`.
- Instruments: triangle wave, soft bell.
- If perfect: add golden sparkle layer.

### Game Complete Music

- Tempo: 60 BPM.
- Scale: C major.
- Mood: warm, resolved.
- Instruments: soft pad, music box, gentle waterfall.
- Chord: `C4 - E4 - G4 - C5`.

---

## 13.2 Level Music

All level music should be 8-bar loops in 4/4 time.

| Level | Tempo | Scale | Mood | Instruments | Motif |
|---|---:|---|---|---|---|
| 1 Pond Edge | 100 BPM | C major pentatonic | bright, easy | xylophone, light woodblock | `C4 - D4 - E4 - G4 - E4 - D4 - C4 - D4` |
| 2 Lily Rush | 110 BPM | C major | bouncy, playful | marimba, xylophone, soft percussion | `C4 - E4 - G4 - C5 - G4 - E4 - C4 - D4` |
| 3 Reed Hollow | 96 BPM | A minor | quiet, vertical | flute, soft pad, water drops | `A4 - C5 - E5 - C5 - A4 - G4 - A4 - E4` |
| 4 Stormy Creek | 104 BPM | D minor | tense but safe | low pulse, woodblock, rain noise | `D4 - F4 - A4 - C5 - A4 - F4 - D4 - F4` |
| 5 Cliffside Ponds | 112 BPM | E minor | rising, adventurous | wind chime, pluck, soft percussion | `E4 - G4 - B4 - E5 - B4 - G4 - E4 - G4` |
| 6 Great Waterfall | 100 BPM | C major | grand, final | soft strings, marimba, waterfall | `C4 - E4 - G4 - C5 - G4 - E4 - C4 - D4` |

### Level 6 Boss Music

When the heron is active:

- Tempo: 120 BPM.
- Scale: C minor / C major resolution.
- Mood: urgent but not scary.
- Instruments: low pulse, woodblock, waterfall ambience.
- Motif: `C4 - Eb4 - G4 - C5 - G4 - Eb4 - C4 - Eb4`.

When heron HP is 3 or less:

- Add high woodblock ticks.
- Increase pulse intensity slightly.
- Do not add new scary stingers.

When the heron dies:

- Boss music stops.
- Short resolve chord: `C4 - E4 - G4 - C5`.
- Waterfall ambience becomes brighter.

Why: the boss should feel like a pattern to dodge, not a horror moment.

---

## 13.3 Ambience

| Level / State | Ambience |
|---|---|
| Title | soft water, distant birds |
| Level 1 | light water, soft wind |
| Level 2 | water ripples, lily pad splashes |
| Level 3 | misty water, soft reed rustle |
| Level 4 | rain, wind, moving water |
| Level 5 | twilight wind, distant water |
| Level 6 | waterfall, mist, soft rocks |

Ambience rules:

- Keep ambience low.
- Do not let rain hide SFX.
- Do not let waterfall hide boss audio.
- No thunder.
- No lightning crack.

---

## 13.4 Sound Effects

All SFX should be short and clear.

Recommended mix:

- Master: -6 dB.
- Music: -12 dB.
- SFX: -6 dB.
- Ambience: -18 dB.

SFX priority:

1. Player damage
2. Boss death
3. Stomp
4. Checkpoint
5. Boss hit
6. Dewdrop
7. UI

---

### Required and added SFX

| Event | Sound design | Synthesis recipe | Duration |
|---|---|---|---:|
| Jump | short bright blip | triangle 320 Hz to 640 Hz, lowpass 2 kHz | 0.08 s |
| Water splash | soft splash | filtered noise 800 Hz to 300 Hz + sine 600 Hz to 200 Hz | 0.15 s |
| Lily pad bounce | springy pop | sine 220 Hz to 520 Hz, slight vibrato | 0.12 s |
| Stomp | soft thud + puff | noise lowpass 400 Hz + sine 100 Hz | 0.10 s |
| Damage | descending hurt blip | square 420 Hz to 140 Hz, slight distortion | 0.15 s |
| Player death | soft falling blip | triangle 300 Hz to 80 Hz, lowpass | 0.30 s |
| Checkpoint | two-note bell | sine C5 then G5 | 0.25 s |
| Dewdrop collect | tiny sparkle | sine 1320 Hz + 1760 Hz | 0.05 s |
| Level complete | small fanfare | triangle C5 - E5 - G5 | 0.50 s |
| Perfect | golden sparkle | high sine arpeggio C6 - E6 - G6 | 0.40 s |
| Boss lunge | soft whoosh | filtered noise sweep 300 Hz to 1200 Hz | 0.15 s |
| Boss hit | low thud + feather flutter | sine 80 Hz + short noise burst | 0.15 s |
| Boss death | splash + soft bell | noise splash + sine C4 | 0.60 s |
| Exit activation | water burst | filtered noise + rising sine | 0.30 s |
| Menu select | soft tick | sine 880 Hz | 0.03 s |
| Menu back | lower tick | sine 587 Hz | 0.03 s |
| Pause | soft UI blip | sine 440 Hz | 0.05 s |
| Game complete | warm chord swell | C4 - E4 - G4 - C5, slow attack | 1.00 s |

### SFX rules

- No SFX should last longer than 0.60 s, except game complete chord.
- No SFX should use harsh distortion.
- Water sounds should be soft.
- Boss sounds should be larger than normal enemy sounds.
- UI sounds should be quiet.

---

## 13.5 Audio Event Mapping

Map gameplay events to audio as follows:

| Gameplay event | Audio |
|---|---|
| Jump | jump SFX |
| Water splash | water splash SFX |
| Lily pad bounce | lily pad bounce SFX |
| Stomp | stomp SFX |
| Damage | damage SFX |
| Checkpoint | checkpoint SFX |
| Level complete | level complete stinger |
| Boss hit | boss hit SFX |
| Boss death | boss death SFX |
| Game complete | game complete music / SFX |

Added events:

| Event | Audio |
|---|---|
| Dewdrop collect | dewdrop SFX |
| Player death | death SFX |
| Boss lunge | boss lunge SFX |
| Exit activation | exit activation SFX |
| Menu select | menu select SFX |
| Menu back | menu back SFX |
| Pause | pause SFX |
| Perfect | perfect SFX |

Why: the required events cover major feedback, but dewdrops, death, boss lunges, and UI need their own small cues to make the game feel complete.

---

## 14. Accessibility and Readability Summary

### Contrast

- Text: minimum 4.5:1 contrast against background.
- Gameplay objects: minimum 3:1 contrast against local background.
- Player: always high contrast against ground and water.

### Colorblind support

- Hazards use shape: spikes.
- Water uses color plus animation.
- Currents use arrows.
- Lily pads use shape and brightness.
- One-way leaves use thinness.
- Boss stomp zone uses a band, not only color.

### Motion sensitivity

- No flashing gameplay hazards.
- No lightning.
- No strobing.
- Screen shake is small.
- Blink rate is limited to 8 Hz.
- Effects do not cover hitboxes.

### Text readability

- All text has outline or panel.
- No small text over busy backgrounds.
- Message area uses translucent panel.
- Menus use dark panels.

### Why

The game should be playable by a wide audience without extra settings. Readability is part of the design, not an afterthought.

---

## 15. Asset Checklist

### Player

| Asset | Size | Notes |
|---|---:|---|
| Frog idle | 32 x 32 | 2 frames |
| Frog run | 32 x 32 | 4 frames |
| Frog jump | 32 x 32 | 1 frame |
| Frog fall | 32 x 32 | 1 frame |
| Frog swim | 32 x 32 | 2 frames |
| Frog bounce | 32 x 32 | 1 frame |
| Frog stomp | 32 x 32 | 1 frame |
| Frog hurt | 32 x 32 | 1 frame |
| Frog death | 32 x 32 | 2 frames |

### World

| Asset | Size | Notes |
|---|---:|---|
| Ground top | 32 x 32 | level recolored |
| Ground side | 32 x 32 | level recolored |
| Ground fill | 32 x 32 | level recolored |
| One-way leaf | 128 x 16 | static |
| Moving leaf | 128 x 16 | with trail |
| Lily pad | 64 x 24 | bouncy |
| Water tile | 32 x 32 | animated surface |
| Current chevron | 16 x 8 | animated |
| Thorn | 48 x 16 | static |
| Dewdrop | 16 x 16 | bobbing |
| Lotus checkpoint | 32 x 32 | inactive / active / bloom |
| Exit active | 64 x 80 | 4-frame loop |
| Exit locked | 64 x 80 | still |

### Enemies

| Asset | Size | Notes |
|---|---:|---|
| Mosquito | 32 x 28 | 2-frame wings |
| Dragonfly | 32 x 24 | 2-frame wings |
| Heron idle | 64 x 80 | 2 frames |
| Heron lunge | 64 x 80 | 2 frames |
| Heron recover | 64 x 80 | 1 frame |
| Heron dead | 64 x 80 | 2 frames |
| Boss HP droplet | 12 x 12 | cyan / amber |

### UI

| Asset | Size | Notes |
|---|---:|---|
| Heart full | 32 x 32 | |
| Heart empty | 32 x 32 | |
| Dewdrop HUD icon | 24 x 24 | |
| UI panel | variable | rounded |
| Frog cursor | 32 x 32 | menu cursor |

---

## 16. Cuts

The following visual and audio pieces are cut.

### Cut visual elements

- objective arrow
- minimap
- score display
- timer
- star ratings
- level select UI
- power-up icons
- health pickup icons
- controller support icons
- remappable controls UI
- settings menu
- accessibility settings menu
- complex cutscenes
- extra characters
- background fireflies
- background lightning
- floating petals in Level 2
- decorative thorns in background
- decorative lily pads that could be confused with gameplay
- decorative platforms that could be confused with gameplay
- water wipe transitions
- long loading screens
- detailed 3D-style backgrounds
- parallax beyond 3 layers
- heavy post-processing
- screen shake on normal movement

### Cut audio elements

- thunder
- lightning crack
- scary stingers
- long musical stingers
- voice lines
- radio / phone audio
- complex orchestral score
- loud percussion
- distortion-heavy SFX
- looping SFX longer than ambience

### Why these cuts

The game is short, small, and focused. Every visual and audio element should help the player understand movement, water, lily pads, hazards, and the waterfall goal. Extra decoration would dilute the frog’s journey and make platforming harder to read.

---

## 17. Final Design Intent

The finished game should look like a small, bright pond world that gradually grows bigger as the frog travels.

Early levels should feel calm and easy.

Middle levels should feel wet, moving, and slightly mysterious.

Later levels should feel taller, stormier, and more adventurous.

The final level should feel grand but still clear.

The player should always know:

- where the frog is
- where safe ground is
- where water is
- where lily pads bounce
- where hazards are
- where the checkpoint is
- where the waterfall exit is
- how much health remains
- how many dewdrops remain
- what the current objective is

The visuals should make the frog feel small, but the journey should feel big.