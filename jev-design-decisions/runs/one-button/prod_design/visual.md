# `visual.md`

## 0. Scope and handoff note

This document is the authoritative visual, UX, music, and sound-effect design for **Cadence**, the one-button tempo roguelike defined in `gameplay.md`.

It defines:

- The coherent visual style across title, run, pause, death, victory, and upgrade states.
- The UX experience for a one-button game.
- The HUD and how the player reads **what the next tap will do**.
- The visual language for player actions, enemies, traps, barriers, doors, relics, shards, bosses, and rooms.
- The distinct but coherent look of the five floors.
- The music direction and adaptive behavior.
- The sound-effect system and event names.
- Accessibility rules.
- Load-bearing visual decisions that must not be changed casually.

The engineering agent may choose rendering technology, but the visual decisions in this document are binding unless a decision is explicitly marked as optional.

If a visual element is not listed here, it should not be added unless it is required by `gameplay.md`.

---

## 1. Visual identity

### 1.1 Working title

**Cadence**

### 1.2 Core visual fantasy

The game should feel like a **clockwork rhythm dungeon**.

The player is not controlling a character with buttons. The player is controlling a **pulse**. The dungeon is made of gears, pistons, spikes, barriers, and metronome-like systems. The player’s tempo is the only thing that matters.

The visual style should communicate:

- Precision.
- Tempo.
- Heat.
- Risk.
- Mechanical danger.
- One clear input.

### 1.3 Art style

Use a **flat vector / low-detail 2D** style.

Recommended look:

- Clean silhouettes.
- Thick outlines on gameplay objects.
- Limited palette per floor.
- High contrast between gameplay objects and background.
- Simple animations.
- No detailed shading.
- No realistic textures.
- No photographic assets.
- No complex perspective.

The game is side-view, single-lane. The visual style should make the lane readable instantly.

### 1.4 Visual grammar

Use these shapes consistently:

| Shape / Motif | Meaning |
|---|---|
| Pendulum / metronome | Tempo, title, final boss |
| Gear | Systems, doors, upgrades, barriers |
| Circle / pulse | Safe, player core, parry |
| Arrow / footstep | Movement |
| Slash / angular arc | Attack |
| Ring / expanding pulse | Parry |
| Broken ring / weak spark | Flick |
| Spikes / teeth | Danger, traps, enemy contact |
| Crystal / shard | Currency |
| Pedestal / relic | In-run item |

Do not use these motifs for unrelated meanings.

### 1.5 Core design principles

1. **One glance must reveal the next action.**  
   The Tempo marker is the most important UI element in the game.

2. **Do not add a visible button.**  
   The whole screen is the button. A visible button would imply a separate control and distract from cadence.

3. **Do not rely on color alone.**  
   Every important state must have shape, icon, animation, or text support.

4. **Action colors are immutable.**  
   Move, Attack, Parry, and Flick keep the same visual identity on every floor.

5. **Floors may change atmosphere, but not the control language.**  
   The player should always know that cyan means Move, amber means Attack, white/violet means Parry, and gray means Flick.

6. **Menus are predictable.**  
   Menus do not inherit run Tempo. They use simple one-button navigation.

7. **Cut anything that competes with the Tempo marker.**  
   If an effect makes the next tap less readable, remove it.

---

## 2. Color system

### 2.1 Immutable action palette

These colors are used everywhere the player’s next action is shown.

| Meaning | Color | Hex | Usage |
|---|---:|---:|---|
| Move / Cool | Cyan | `#3AE0FF` | Move zone, move feedback, move icon, low-tempo player core |
| Attack / Warm | Amber | `#FFB020` | Attack zone, attack slash, attack icon, mid-tempo player core |
| Parry / Hot | Violet-white | Core `#F4EDFF`, rim `#A855F7` | Parry zone, parry ring, parry icon, high-tempo player core |
| Flick / Failed Parry | Gray | `#9AA3B2` | Flick icon, flick spark, failed parry feedback |
| Danger | Red | `#FF4D4D` | Player damage, enemy projectiles, active traps, boss warnings |
| Warning | Yellow | `#FFD84D` | Trap warning phase, caution, unaffordable upgrade cost |
| UI Background | Near-black | `#0F1115` | Base UI background |
| UI Panel | Dark slate | `#1A1E26` | Toasts, cards, summary panels |
| UI Border | Slate | `#3A4150` | Panels, slots, bars |
| Primary Text | Off-white | `#F5F7FA` | Most text |
| Secondary Text | Light gray | `#A8B2C1` | Labels, subtext |
| Shards | Pale blue-white | `#DDE6FF` | Shard icon, shard count, shard particles |

#### Why this palette

- **Cyan** reads as cool, safe, and slow.
- **Amber** reads as warm, offensive, and active.
- **Violet-white** reads as hot, powerful, and expensive.
- **Gray** clearly reads as weak or failed.
- **Red** is reserved for damage and danger. It should not be used for normal movement or attacks.

Do not use red for normal player actions.

Do not use amber for enemy projectiles. Enemy projectiles are red.

Do not use violet for normal floor background accents in a way that competes with Parry.

### 2.2 Floor palettes

Floors change atmosphere, but gameplay object colors remain fixed.

Use a dark background with muted midtones. Gameplay objects must always be brighter than the environment.

| Floor | Theme | Far background | Wall | Floor | Accent | Ambient particles |
|---:|---|---:|---:|---:|---:|---|
| 1 | Bronze Vault | `#17120D` | `#3A2B1E` | `#5A432C` | `#8A6B45` | Warm dust, `#D8B27A`, 15% opacity |
| 2 | Verdant Gearworks | `#0F1A16` | `#243B31` | `#345244` | `#5E8C70` | Green spores, `#9AD1B0`, 15% opacity |
| 3 | Amber Undercroft | `#140B06` | `#3A2214` | `#5C341A` | `#C47A32` | Embers, `#FF9A3C`, 12% opacity |
| 4 | Cobalt Machine | `#0A1118` | `#1F3040` | `#2E465A` | `#6E93A8` | Cool sparks, `#9AB8CC`, 12% opacity |
| 5 | Chromatic Metronome | `#08080C` | `#181820` | `#26262E` | `#F5F7FA` | White motes with faint action-color tints, 10% opacity |

#### Floor palette rules

- The far background should be low contrast.
- The wall layer should be readable but not distracting.
- The floor lane should be the brightest horizontal band.
- Ambient particles must never resemble enemy projectiles.
- Ambient particles must never use bright red.
- Floor 5 may use all action colors, but only as faint ambient accents. The action palette remains dominant in UI and player feedback.

### 2.3 Rarity palette

Used only for relics and upgrade cards.

| Rarity | Border / glow | Hex |
|---|---|---:|
| Common | Neutral gray | `#B8C0CC` |
| Rare | Gold | `#FFD84D` |
| Epic | Magenta | `#FF7FE0` |

Rarity is shown by border and icon glow. Do not change relic icon shape based on rarity.

### 2.4 Contrast rules

- All HUD text must have at least 7:1 contrast against its background.
- All gameplay objects must have at least 3:1 contrast against the floor lane.
- Enemy projectiles must be visible against every floor palette.
- Parry zone must remain distinguishable from Attack zone even in low-vision conditions.
- If a floor accent color gets too close to an action color, mute the floor accent.

---

## 3. Typography and layout

### 3.1 Font

Use a clean geometric sans-serif.

Recommended stack:

```css
font-family: "Inter", "Roboto", "Helvetica Neue", Arial, sans-serif;
```

Use monospaced numerals for counts:

```css
font-variant-numeric: tabular-nums;
```

### 3.2 Type scale

| Element | Size | Weight |
|---|---:|---:|
| Title logo | 48–64px | 800 |
| State title | 32–40px | 800 |
| Toast text | 16px | 600 |
| HUD text | 12–14px | 600 |
| Damage numbers | 14px | 700 |
| Upgrade card name | 16px | 700 |
| Upgrade card effect | 12px | 500 |
| Upgrade card cost | 14px | 700 |

Use uppercase for short HUD labels:

- `F1 R1`
- `MOVE`
- `ATTACK`
- `PARRY`
- `MAX`

Use sentence case for toasts:

- `Room cleared`
- `Relic acquired: Metronome`
- `Cannot buy`

### 3.3 Virtual resolution

Design for a virtual canvas of:

```text
960 x 540
```

Scale to fit the viewport while preserving aspect ratio.

Use letterboxing if necessary.

Do not design for a separate portrait layout unless the viewport is significantly taller than wide. If portrait is used, scale the virtual canvas to fit the width and center it vertically.

### 3.4 Tile size

```text
1 tile = 32px
```

The lane is one tile tall for gameplay collision, but visual objects may extend vertically.

### 3.5 Safe area

Keep important UI inside:

```text
16px from top
16px from left
16px from right
16px from bottom
```

Avoid placing critical gameplay objects in the outer 24px of the screen.

---

## 4. HUD design

The HUD must be readable at a glance.

The HUD is fixed. Floor palettes do not change HUD colors.

### 4.1 HUD layout

Top area:

```text
[ HP ]          [ Tempo bar ]          [ F1 R1 ]
                        [ Boss bar, if active ]
                        [ Toasts, if active ]
```

Bottom area:

```text
[ Relic slots ]                         [ Shards ]
```

### 4.2 Player HP

Position:

```text
Top left
x = 16
y = 12
```

Display:

- A small heart icon.
- A segmented HP bar.
- Each segment represents one heart.
- If max hearts is 5, show 5 segments.
- If max hearts exceeds 5, show one segment per heart, up to 9.
- Partial hearts show partial fill.

Visual:

- Background: `#1A1E26`
- Border: `#3A4150`
- Fill: `#FF4D4D`
- Empty: `#10131A`
- Heart icon: `#FF4D4D`

Damage feedback:

- On player damage, the HP bar flashes white for 80 ms.
- The current segment flashes red for 150 ms.
- A red vignette flashes for 150 ms.

### 4.3 Tempo bar

The Tempo bar is the primary control UI.

Position:

```text
Top center
width = 420px
height = 16px
y = 12
```

If viewport width is smaller, scale the Tempo bar to `min(420px, 60vw)`.

#### Zones

The bar is divided into three zones:

| Zone | Tempo range | Visual |
|---|---:|---|
| Move | 0–39 | Cyan tint, arrow icon |
| Attack | 40–69 | Amber tint, slash icon |
| Parry | 70–100 | Violet tint, ring icon |

Zone boundaries:

```text
Move zone ends at 39% of bar width.
Attack zone ends at 69% of bar width.
Parry zone is the remainder.
```

#### Background

Base bar background:

```text
#10131A
```

Zone tints:

- Move: `rgba(58, 224, 255, 0.18)`
- Attack: `rgba(255, 176, 32, 0.18)`
- Parry: `rgba(168, 85, 247, 0.18)`

#### Current Tempo fill

Show a subtle white fill representing current Tempo.

```text
rgba(255, 255, 255, 0.22)
```

This fill is secondary. The marker is primary.

#### Next-tap marker

The marker shows `nextTempo`, not current Tempo.

The marker must be large enough to read instantly.

Recommended marker:

- A 24px circle.
- A 12px downward pointer.
- A 14px action icon inside the circle.
- White outline for contrast.

Marker position:

```text
x = barX + (nextTempo / 100) * barWidth
```

Marker moves left as Tempo decays.

#### Marker icons

| Next action | Icon | Color |
|---|---|---|
| Move | Right arrow | `#3AE0FF` |
| Attack | Diagonal slash | `#FFB020` |
| Parry | Ring | Core `#F4EDFF`, rim `#A855F7` |
| Flick | Broken ring | `#9AA3B2` |

The marker icon must change immediately when `nextTempo` crosses a zone boundary.

#### Parry cooldown

When Parry is on cooldown:

1. The Parry zone is darkened.
2. A diagonal hatch pattern covers the Parry zone.
3. A white sweep fills the Parry zone from left to right as cooldown recovers.
4. When cooldown reaches 0, the Parry zone flashes white for 200 ms.
5. A soft chime plays.

Parry cooldown overlay:

```text
rgba(16, 19, 26, 0.72)
```

Sweep fill:

```text
rgba(255, 255, 255, 0.25)
```

#### Flick indicator

If the marker is in the Parry zone but Parry is on cooldown:

- The marker becomes gray.
- The marker icon becomes a broken ring.
- The Parry zone remains hatched.
- Do not show a full Parry ring.

This is critical. The player must understand that their next fast tap will Flick, not Parry.

#### Optional zone labels

For the first 10 seconds of Floor 1, Room 1, show small labels under the Tempo bar:

```text
MOVE      ATTACK      PARRY
```

Labels fade out after 10 seconds or after the player has used Move, Attack, and Parry once.

### 4.4 Floor and room indicator

Position:

```text
Top right
x = 944, right-aligned
y = 12
```

Format:

```text
F1 R1
```

Style:

- 14px
- `#A8B2C1`
- Uppercase
- Monospaced numerals

### 4.5 Boss HP bar

Shown only when a boss is active.

Position:

```text
Below Tempo bar
y = 36
width = 420px
height = 10px
```

Visual:

- Background: `#10131A`
- Border: `#3A4150`
- Fill: `#FF4D4D`
- Boss name: 12px, `#F5F7FA`, left of bar or above bar depending on space.
- Numeric HP optional.

Boss bar should not overlap the Tempo marker.

#### Boss phase feedback

On boss phase change:

- Boss flashes white for 200 ms.
- Boss bar flashes white for 200 ms.
- A toast appears: `Phase 2` or `Phase 3`.
- A music stinger plays.

For the final boss, The Metronome, show three small phase pips to the right of the boss bar.

### 4.6 Relic slots

Position:

```text
Bottom left
x = 16
y = 500
```

Display 5 slots.

Each slot:

- 28px circle.
- 16px icon.
- Empty slots are dim.
- Filled slots show relic icon.
- Rarity is shown by border color.

Empty slot:

```text
fill = #10131A
border = #3A4150
opacity = 0.5
```

Filled slot:

```text
fill = #1A1E26
border = rarity color
```

Relic pickup:

- The relic flies from its world position to the next empty slot.
- The slot flashes white for 150 ms.
- A toast appears.

Relic conversion:

- The relic shatters into shard particles.
- Particles fly to the shard counter.
- A toast appears.

### 4.7 Shard counter

Position:

```text
Bottom right
x = 944, right-aligned
y = 500
```

Display:

- Shard icon: 20px.
- Shard count: 16px, `#F5F7FA`.

Shard icon:

- A small diamond crystal.
- Color: `#DDE6FF`.
- Slight white highlight.

Shard pickup:

- Small crystal particles fly from the source to the shard counter.
- The shard count pulses for 100 ms.

### 4.8 Toasts

Toasts appear center-top, below the boss bar if present.

Position:

```text
x = 480, centered
y = 64
max width = 600px
height = 32px
```

Style:

- Background: `rgba(26, 30, 38, 0.92)`
- Border: `#3A4150`
- Text: 16px, `#F5F7FA`
- Optional icon on the left.

Behavior:

- Max 3 toasts visible.
- Each toast lasts 1.6 seconds.
- Toasts fade in over 100 ms and fade out over 200 ms.
- Toasts never block the Tempo bar.
- Toasts never block the player or enemies.

Toast examples:

```text
Room cleared
Relic acquired: Metronome
Relic converted: +20 shards
Boss: Gear Knight
Phase 2
Upgrade purchased: Blade
Cannot buy
Maxed
```

### 4.9 Damage numbers

Display brief damage numbers for player damage dealt and player damage taken.

Style:

- 14px bold.
- Float upward 20px over 500 ms.
- Fade out after 600 ms.
- Use monospaced numerals.

Player damage dealt:

```text
color = #F5F7FA
outline = #FFB020, 1px
```

Player damage taken:

```text
color = #FF4D4D
outline = #F5F7FA, 1px
```

Position:

- Damage dealt: above the damaged enemy or barrier.
- Damage taken: above the player.

If multiple damage numbers appear at once, stagger them vertically by 8px.

### 4.10 Door state

The door is at the right side of the room.

Door size:

```text
1.5 tiles wide
2 tiles tall
```

#### Locked

- Closed metal door.
- Dark.
- Gear lock in center.
- No light.
- Color: muted floor accent, darkened.

Locked feedback:

- If the player attempts to move into a locked door, the door thuds.
- The door shakes 2px for 80 ms.
- A dull sound plays.

#### Unlocking

- The gear lock spins.
- A thin light seam appears.
- The light seam grows over 300 ms.

#### Open

- The door is open.
- A soft light fills the doorway.
- The light color is warm white: `#FFF3D6`.
- The player can move into it.

### 4.11 Tutorial hints

Floor 1, Room 1 shows brief hints.

Use toasts with icons.

Sequence:

1. On run start:
   - `Tap slowly to move`
   - Icon: Move arrow.

2. After the player’s first successful move:
   - `Tap in the amber zone to attack`
   - Icon: Attack slash.

3. After the player’s first successful attack:
   - `Burst taps to parry`
   - Icon: Parry ring.

Rules:

- Show one hint at a time.
- Each hint lasts 2.5 seconds.
- Hide a hint permanently once the corresponding action has been used successfully.
- Do not show hints after Floor 1, Room 1.

### 4.12 Pause state

There is no pause button.

If the app loses focus:

- The game pauses automatically.
- The music pauses or ducks to near silence.
- A dark overlay appears.
- The text `Tap to continue` appears center screen.
- Any tap resumes the game.

Overlay:

```text
rgba(0, 0, 0, 0.72)
```

Text:

- 32px
- `#F5F7FA`
- Pulsing opacity between 0.7 and 1.0 over 1 second.

---

## 5. Gameplay visuals

### 5.1 Player

The player is a small mechanical warden.

Size:

```text
0.8 tiles wide
0.9 tiles tall
```

At 32px tile size:

```text
25px wide
29px tall
```

Visual:

- Dark rounded body: `#22262E`
- White outline: 2px
- Small visor: white line
- Core: circle in center
- Core color matches the next action color:
  - Move: cyan
  - Attack: amber
  - Parry: violet-white
  - Flick: gray
- Optional heat ring:
  - Radius 14px
  - Stroke 2px
  - Color matches next action
  - Opacity 0.25 at low Tempo, 0.5 at high Tempo

The heat ring is subtle. It should not compete with the Tempo bar.

### 5.2 Player action visuals

#### Move

Trigger: low Tempo tap.

Visual:

- Player leans forward 8°.
- Small cyan dust puffs at the feet.
- Movement tween: 100 ms.
- No large flash.

Blocked move:

- Player bumps forward 4px.
- Gray dust puff.
- Small thud sound.
- No damage.

#### Attack

Trigger: mid Tempo tap.

Visual:

- Amber slash arc extends from the player’s front to 1.5 tiles.
- Slash lasts 120 ms.
- Small amber sparks at the end of the arc.
- Enemies or barriers in the hitbox flash white.

Attack should feel quick and offensive, but not as large as Parry.

#### Parry

Trigger: high Tempo tap when Parry is ready.

Visual:

- White-violet ring expands from the player.
- Ring reaches 1.5 tile radius over 200 ms.
- Player flashes white for 100 ms.
- Small screen shake: 2px for 100 ms.
- Enemies in radius are knocked back.
- Projectiles in radius shatter.

Parry should feel powerful and clean.

#### Flick

Trigger: high Tempo tap while Parry is on cooldown.

Visual:

- Small gray spark around the player.
- Radius visual: 1.0 tile.
- Lasts 80 ms.
- No i-frame flash.
- No screen shake.
- No white ring.

Flick must look clearly weaker than Parry.

#### Player damage

Visual:

- Player flashes red for 100 ms.
- Red vignette flashes for 150 ms.
- Screen shake: 4px for 150 ms.
- Player blinks during i-frames.
- Blink rate: 8 times per second.

#### Player death

Visual:

- Player core shatters.
- Small white and red particles.
- Screen desaturates to 40% over 300 ms.
- Tempo bar visually breaks or dims.
- Transition to death summary after 600 ms.

### 5.3 Enemy visuals

All enemies are on the single lane.

Enemy hit feedback:

- White flash: 50 ms.
- Small damage number.
- Small hit spark.

Enemy death:

- Enemy shatters into 6–10 small shards.
- Shards are pale blue-white.
- A small gear particle appears if the enemy is mechanical.
- Shard count increases.

#### Chaser

Size:

```text
0.8 tiles wide
0.7 tiles tall
```

Visual:

- Rounded beetle shape.
- Bronze body: `#4A3A2A`
- White outline: 2px
- Two small white eyes.
- Low profile.

Movement:

- Slight bob.
- Feet or treads move toward the player.

#### Spiky

Size:

```text
0.6 tiles wide
0.6 tiles tall
```

Visual:

- Small spiked creature.
- Bone-white body: `#D9D2C5`
- Dark spikes: `#2A2A30`
- Red eyes: `#FF4D4D`
- Faster, more jittery movement than Chaser.

#### Shooter

Size:

```text
0.8 tiles wide
0.8 tiles tall
```

Visual:

- Gray turret body: `#5A6470`
- Dark barrel pointing left.
- Red lens: `#FF4D4D`
- Small base.

Firing:

- Barrel glows red 200 ms before projectile.
- Projectile spawns with muzzle flash.

#### Barrier

Size:

```text
1 tile wide
1.2 tiles tall
```

Visual:

- Gear wall.
- Bronze color: `#6B5233`
- White outline.
- Central gear.
- Cracks appear at 75%, 50%, and 25% HP.

Barrier hit:

- White flash.
- Small metal spark.
- Crack advances.

Barrier break:

- Shatters into gear fragments.
- 15 shard particles fly out.
- A heavy clank plays.

### 5.4 Spike trap

Size:

```text
1 tile wide
0.3 tiles tall
```

States:

#### Safe

- Flat gray grate.
- Color: `#5A6470`
- No spikes.

#### Warning

- Spikes rise halfway.
- Color: `#FFD84D`
- Flashes 3 times over 0.5 seconds.
- A small exclamation shape appears above the trap.

#### Danger

- Spikes fully extended.
- Color: `#FF4D4D`
- No flash.
- Active damage.

Spike trap visuals must be readable from across the room.

### 5.5 Projectiles

Enemy projectiles only.

Size:

```text
0.3 tile diameter
```

Visual:

- Red orb: `#FF4D4D`
- White core: `#F5F7FA`
- Short red trail: 0.2 seconds.
- Slight pulse.

Projectile rules:

- Projectiles move left toward the player.
- They are destroyed by Attack, Parry, or Flick.
- On destruction, they shatter into 3–5 red sparks.
- They despawn when leaving the room.

Do not use projectile visuals for player actions. Player actions are slashes, rings, and sparks.

### 5.6 Relics

Relic size:

```text
0.6 tiles wide
0.6 tiles tall
```

Relic visual:

- Floats above a small pedestal.
- Rotates slowly.
- Rarity glow.
- Icon-specific shape.

Relic icons:

| Relic | Icon |
|---|---|
| Metronome | Small pendulum triangle |
| Heavy Cog | Gear |
| Spring Boot | Boot with spring |
| Thorn | Leaf/thorn |
| Iron Latch | Latch hook |
| Echo | Two concentric arcs |
| Ward | Shield |
| Pulse | Ring pulse |
| Glass Heart | Heart with crack |
| Clockwork | Gear with clock face |

Relic pickup:

- Relic flies to the next empty slot.
- Slot flashes.
- Toast appears.

Relic conversion:

- Relic shatters.
- Shard particles fly to the shard counter.
- Toast appears.

### 5.7 Shard piles

Shard pile size:

```text
0.5 tiles wide
0.5 tiles tall
```

Visual:

- 3–5 small crystals.
- Color: `#DDE6FF`
- Slight bob.
- Soft sparkle.

Pickup:

- Crystals fly to the shard counter.
- Shard count pulses.
- Tiny ping sound plays.

### 5.8 Room transition

When the player enters an open door:

- If the player is overlapping the door, transition after 200 ms.
- Use a short fade.

Transition:

- Fade to black over 150 ms.
- Load next room.
- Fade in over 150 ms.

Floor transition:

- Fade over 300 ms.
- Show toast: `Floor 2`, `Floor 3`, etc.
- Music crossfades to the new floor’s run music.

---

## 6. Floors and bosses

### 6.1 Floor identity

Each floor uses the same room structure and action language, but changes atmosphere.

| Floor | Theme | Mood | Visual focus |
|---:|---|---|---|
| 1 | Bronze Vault | Learn, warm, readable | Clear bronze, high readability |
| 2 | Verdant Gearworks | Organic machinery, slightly hostile | Green walls, copper pipes, spores |
| 3 | Amber Undercroft | Heat, pressure, danger | Deep amber, embers, crystals |
| 4 | Cobalt Machine | Cold industry, precision | Blue-gray steel, pistons, sparks |
| 5 | Chromatic Metronome | Final rhythm, high contrast | Black/white, all action colors, metronome |

### 6.2 Room type visuals

#### Combat room

- Enemies.
- Optional barrier.
- Optional trap.
- Optional relic.
- Standard door.

#### Treasure room

- No enemies.
- 1–2 relic pedestals.
- 1–3 shard piles.
- Slightly brighter light.
- No traps.

#### Trap room

- No enemies.
- 2–3 spike traps.
- 1 relic.
- Floor grates are more visible.
- Warning lights may blink subtly.

#### Boss room

- Larger ceiling.
- Boss near the right side.
- Boss HP bar appears.
- Door is locked until boss is dead.
- Environmental details intensify:
  - Floor 1: larger gears.
  - Floor 2: vines and pipes.
  - Floor 3: glowing amber crystals.
  - Floor 4: piston mechanisms.
  - Floor 5: giant metronome pendulum in background.

### 6.3 Boss visuals

All bosses have:

- A distinct silhouette.
- A boss HP bar.
- At least 0.5 seconds of visual warning before active attacks.
- A phase transition flash.
- A death shatter.

Boss contact damage is visually indicated by the same red damage feedback as normal enemies.

#### Floor 1 boss: Clockwork Golem

Size:

```text
3 tiles wide
2.5 tiles tall
```

Visual:

- Large bronze golem.
- One central eye.
- Visible pendulum on chest.
- Heavy arms.

Patterns:

| Pattern | Telegraph | Active visual |
|---|---|---|
| Charge | Golem flashes red, red arrow line appears along lane | Golem stretches, red speed lines |
| Stomp | Spike trap appears with warning phase | Golem slams, dust |
| Triple shot | Muzzle/eye glows, three ghost dots appear | Three red projectiles fire |

Phase transition:

- At 50% HP, golem flashes white.
- Two Chasers emerge from gear particles.

#### Floor 2 boss: Gear Knight

Size:

```text
2.5 tiles wide
2.5 tiles tall
```

Visual:

- Armored knight.
- Large sword.
- Gear-shaped shoulder pauldrons.
- Blue-gray armor with amber accents.

Patterns:

| Pattern | Telegraph | Active visual |
|---|---|---|
| Dash left | Knight flashes red, red dash line | Knight lunges, afterimage |
| Double shot | Sword tip glows red | Two projectiles fire |
| Summon | Gear portal appears | Chaser emerges |

#### Floor 3 boss: Ritual Beast

Size:

```text
3 tiles wide
2.5 tiles tall
```

Visual:

- Dark beast.
- Ritual circle under feet.
- Pendulum-like tail.
- Amber and black coloring.

Patterns:

| Pattern | Telegraph | Active visual |
|---|---|---|
| Spiral shot | Ritual circle spins, five ghost dots | Five projectiles in short burst |
| Charge | Beast flashes red, red arrow line | Beast charges |
| Summon | Ritual circle pulses | Spiky or Chaser emerges |

#### Floor 4 boss: Twin Pistons

Size:

```text
3 tiles wide
2.5 tiles tall
```

Visual:

- Mechanical body.
- Two large piston arms.
- Cobalt and steel colors.
- White warning lights.

Patterns:

| Pattern | Telegraph | Active visual |
|---|---|---|
| Left piston | Left piston glows red | Piston lunges left |
| Right piston | Right piston glows red | Piston lunges right |
| Fan shot | Muzzle glows, staggered ghost dots | Four projectiles with slight vertical visual offset |
| Barrier spawn | Gear portal appears between boss and player | Barrier materializes |

#### Floor 5 boss: The Metronome

Size:

```text
3 tiles wide
3 tiles tall
```

Visual:

- Giant metronome.
- Black and white body.
- Pendulum swings in time with its patterns.
- Faint cyan, amber, and violet accents.

Patterns:

| Pattern | Telegraph | Active visual |
|---|---|---|
| Slow stomp | Metronome flashes red, spike trap warning | Trap appears |
| Medium charge | Metronome flashes red, red arrow line | Metronome charges |
| Fast burst | Pendulum speeds up, five ghost dots | Five rapid projectiles |

Phase thresholds:

- 100–66%: Slow stomp, medium charge.
- 66–33%: Adds fast burst.
- 33–0%: All patterns, faster timing.

Final boss death:

- Pendulum stops.
- Metronome shatters into white shards.
- All projectiles disappear.
- Victory sequence begins.

---

## 7. Game states and UX

The game has one button in every state.

There is no hover. There is no cursor. There is no second button.

### 7.1 Title state

Purpose:

- Show title.
- Show best floor.
- Show total shards.
- Start a run.

Layout:

```text
Top left: Best floor
Top right: Total shards
Center: CADENCE logo
Below logo: Subtitle
Bottom center: Tap to start
```

Visual:

- Dark background.
- Slow metronome pendulum in center.
- Logo: `CADENCE`
  - 56px
  - `#F5F7FA`
  - Bold.
- Subtitle:
  - `One button. Your tempo decides.`
  - 16px
  - `#A8B2C1`
- Best floor:
  - `Best: F3`
  - Top left
  - 16px
- Shards:
  - Shard icon + count
  - Top right
  - 16px
- Prompt:
  - `Tap to start`
  - Bottom center
  - 20px
  - Pulsing opacity.

Optional legend:

At the bottom, show three small icons:

- Move arrow.
- Attack slash.
- Parry ring.

Do not make the legend large. It is a reminder, not a tutorial.

Tap behavior:

- Any tap starts a new run.
- Transition to Floor 1, Room 1.

### 7.2 Run state

The run state is the main gameplay state.

Visual requirements:

- HUD visible.
- Tempo marker always visible.
- Player visible.
- Enemies, traps, barriers, relics, shards, and door visible.
- No visible button.
- No pause button.
- No directional controls.

### 7.3 Pause state

Triggered by loss of focus.

Visual:

- Dark overlay.
- `Tap to continue`
- Game time frozen.
- Music paused or heavily ducked.

Tap behavior:

- Any tap resumes.
- No extra confirmation.

### 7.4 Death state

Triggered when player HP reaches 0.

Visual:

- Red vignette.
- Desaturated screen.
- Summary panel appears after 600 ms.

Summary panel:

```text
Run Ended
Floor reached: F3 R2
Shards earned: 120
Total shards: 840
Best floor: F4

Tap to continue
```

Style:

- Panel: `#1A1E26`
- Border: `#3A4150`
- Title: 32px
- Stats: 16px
- Prompt: 18px, pulsing.

Tap behavior:

- If shards earned > 0, go to Upgrade state.
- If shards earned = 0, go to Title state.

### 7.5 Victory state

Triggered when The Metronome dies.

Visual:

- White-gold burst.
- Screen briefly brightens.
- Metronome shatter.
- Summary panel appears after 800 ms.

Summary panel:

```text
Victory
Shards earned: 200
Total shards: 1240
Best floor: F5

Tap to continue
```

Tap behavior:

- If shards earned > 0, go to Upgrade state.
- If shards earned = 0, go to Title state.

### 7.6 Upgrade state

The Upgrade state uses one button but does not use the run Tempo system.

Purpose:

- Spend shards on permanent upgrades.
- Return to Title.

Layout:

```text
Top left: Upgrade
Top right: Shards
Center: 5 cards
Bottom: One-button hint
```

Cards:

1. Vitality
2. Blade
3. Pulse
4. Ward
5. Done

Card size:

```text
120px wide
160px tall
```

Spacing:

```text
16px
```

On narrow screens, stack cards vertically.

#### Card content

Each upgrade card shows:

- Icon.
- Name.
- Current level pips.
- Effect.
- Cost.

Level pips:

- 5 small circles.
- Filled pips: `#F5F7FA`
- Empty pips: `#3A4150`

Cost:

- Affordable: `#F5F7FA`
- Unaffordable: `#FF4D4D`
- Maxed: text `MAX`, gray.

Card states:

| State | Visual |
|---|---|
| Affordable | Bright border, white cost |
| Unaffordable | Dimmed card, red cost |
| Maxed | Gray card, `MAX` |
| Done | White arrow icon, no cost |

Upgrade icons:

| Upgrade | Icon |
|---|---|
| Vitality | Heart |
| Blade | Sword |
| Pulse | Ring |
| Ward | Shield |
| Done | Arrow to title |

#### Cursor

The cursor is a white 3px border around the selected card.

The cursor automatically moves to the next card every 1.5 seconds.

Visual:

- A progress arc fills around the cursor over 1.5 seconds.
- When the arc completes, the cursor moves.

If the player taps, reset the auto-advance timer to 1.5 seconds. This prevents the cursor from moving immediately after a tap.

#### Tap behavior

Track `lastUpgradeTapTime`.

On tap:

1. If less than 0.3 seconds since the last Upgrade tap:
   - Cancel Upgrade state.
   - Return to Title.
   - Play cancel sound.

2. Otherwise:
   - Confirm the highlighted card.
   - Set `lastUpgradeTapTime = now`.
   - Reset auto-advance timer.

Confirm behavior:

- If card is an upgrade:
  - If affordable and not maxed:
    - Buy it.
    - Card flashes white.
    - Level pip fills.
    - Shards decrease.
    - Toast: `Upgrade purchased: [name]`
  - If not affordable:
    - Card shakes.
    - Cost flashes red.
    - Toast: `Cannot buy`
  - If maxed:
    - Card flashes gray.
    - Toast: `Maxed`

- If card is Done:
  - Return to Title.

#### Cancel hint

After a confirm tap, show a small hint for 0.3 seconds:

```text
Tap again quickly to cancel
```

This hint appears near the bottom, below the cards.

It is necessary because the cancel rule is otherwise easy to miss.

#### Auto-return

If shards are 0 or all upgrades are maxed:

- Show a 3-second countdown ring around the Done card.
- After 3 seconds, return to Title.

---

## 8. Feedback and feel

The game must feel responsive. Every input should produce feedback.

### 8.1 Tap feedback

Every accepted tap in the run state produces:

- A short UI tick sound.
- The action-specific visual effect.
- The action-specific sound.

Do not show a tap-location ripple in the run state. The action effect at the player is the feedback.

In menus, show a small tap flash on the affected card or prompt.

### 8.2 Screen shake

Use screen shake sparingly.

| Event | Shake |
|---|---:|
| Move | None |
| Attack | None |
| Parry | 2px for 100 ms |
| Flick | None |
| Player damage | 4px for 150 ms |
| Boss stomp | 6px for 200 ms |
| Boss phase | 4px for 150 ms |
| Death | 6px for 300 ms |

Reduced motion mode disables all screen shake.

### 8.3 Flashes

| Event | Flash |
|---|---|
| Player damage | Red vignette, 150 ms |
| Parry | White ring only, no full-screen flash |
| Enemy hit | Enemy white flash, 50 ms |
| Boss phase | Boss white flash, 200 ms |
| Parry ready | Parry zone white flash, 200 ms |
| Upgrade purchase | Card white flash, 150 ms |
| Victory | White-gold screen flash, 300 ms |

Do not flash the full screen white for normal attacks.

### 8.4 Particles

Use low particle counts for mobile performance.

| Event | Particles |
|---|---|
| Move | 2–3 cyan dust puffs |
| Attack | 3–5 amber sparks |
| Parry | 8–12 white-violet ring particles |
| Flick | 2–3 gray sparks |
| Enemy death | 6–10 shard particles |
| Barrier break | 8–12 gear fragments |
| Projectile destroy | 3–5 red sparks |
| Shard pickup | 3–5 crystal particles |
| Relic convert | 6–10 shard particles |

Reduced motion mode reduces particle count by 50%.

---

## 9. Accessibility

### 9.1 Colorblind safety

Do not rely on color alone.

Required non-color cues:

- Move: arrow icon.
- Attack: slash icon.
- Parry: ring icon.
- Flick: broken ring icon.
- Parry cooldown: hatched Parry zone.
- Trap warning: yellow flashing spikes plus exclamation shape.
- Trap danger: fully extended spikes.
- Enemy projectile: red orb with white core and trail.
- Player damage: red vignette plus HP bar flash.
- Upgrade unaffordable: red cost plus dimmed card.

### 9.2 Reduced motion

If the user prefers reduced motion:

- Disable screen shake.
- Reduce particle count.
- Slow or stop ambient particle drift.
- Keep essential flashes but reduce their duration by 50%.
- Keep Tempo marker movement, because it is critical information.

### 9.3 Audio is not essential

All critical gameplay information must be visual.

Sound can reinforce feedback, but the player must be able to play with audio muted.

### 9.4 One-button accessibility

- The entire screen is the tap target.
- Do not require precise tapping.
- Do not require hold.
- Do not require swipe.
- Do not require keyboard-only interaction unless the browser maps taps/clicks to the same action.

---

## 10. Music design

The music should feel like a mechanical rhythm system, but it must not dictate the player’s gameplay Tempo.

The player’s Tempo is independent from the music’s BPM.

Do not make the music a strict metronome that forces the player to tap on beat.

### 10.1 Music states

| State | BPM | Mood |
|---|---:|---|
| Title | 60 | Calm, mechanical, inviting |
| Run | 90 | Steady, industrial, readable |
| Boss | 110 | Tense, percussive, dangerous |
| Upgrade | 70 | Gentle, musical, reflective |
| Death | 50 | Low, slowed, final |
| Victory | 120 | Bright, resolved, celebratory |

### 10.2 Music stems

Use adaptive stems:

| Stem | Description |
|---|---|
| `music.layer.base` | Pad and low pulse. Always present in run states. |
| `music.layer.attack` | Mid percussion and arpeggio. Active when the player is in the Attack zone or has attacked recently. |
| `music.layer.parry` | High tension synth and faster percussion. Active when the player is in the Parry zone or has parried recently. |
| `music.layer.boss` | Drums, low brass/industrial hits, and lead. Active in boss rooms. |
| `music.tick` | Soft metronome tick. Used only in Title and optionally Upgrade. Do not use in run gameplay. |

### 10.3 Adaptive run music

During a normal run:

- Base layer is always active.
- If the next-tap marker is in the Move zone:
  - Keep music sparse.
  - No attack layer.
  - No parry layer.
- If the next-tap marker is in the Attack zone:
  - Raise attack layer gradually over 200 ms.
- If the next-tap marker is in the Parry zone:
  - Raise parry layer gradually over 200 ms.
- If Parry is on cooldown and the marker is in the Parry zone:
  - Lower the parry layer slightly.
  - Keep a weak tension layer to indicate risk.
- If the player parries:
  - Play a musical accent.
  - Swell the parry layer for 300 ms.
- If the player flicks:
  - Briefly dip the music by 10% for 150 ms.
  - Play a weak accent.

### 10.4 Boss music

In boss rooms:

- Base layer remains.
- Boss layer is active.
- Attack and parry layers still react to the player.
- Boss attacks trigger short musical accents.
- Boss phase changes trigger a stinger.

### 10.5 Chord directions

These are optional but recommended.

| State | Suggested progression |
|---|---|
| Title | Am – F – C – G |
| Run | Dm – Bb – F – C |
| Boss | Dm – Dm – Ab – C |
| Upgrade | C – G – Am – F |
| Death | D drone |
| Victory | C – G – Am – F |

### 10.6 Instrumentation

Recommended generated instrumentation:

- Pad: lowpass sawtooth, detuned, soft.
- Bass: square or triangle, simple pulse.
- Percussion: short noise clicks, soft kick.
- Lead: triangle or sine arpeggio.
- Tension: high sine shimmer.
- Boss drums: filtered kick, snare-like noise, industrial hit.

Keep the mix clear:

- Music should not mask SFX.
- SFX should not mask the Tempo marker visually.
- Critical SFX should briefly duck music by 20% for 200 ms.

### 10.7 Music mixing

Recommended default levels:

| Bus | Level |
|---|---:|
| Master | 0.8 |
| Music | 0.5 |
| SFX | 0.7 |
| UI | 0.5 |

State mixing:

| State | Base | Attack | Parry | Boss | Tick |
|---|---:|---:|---:|---:|---:|
| Title | 0.8 | 0 | 0 | 0 | 0.4 |
| Run | 0.8 | 0–0.5 | 0–0.6 | 0 | 0 |
| Boss | 0.8 | 0–0.5 | 0–0.6 | 0.7 | 0 |
| Upgrade | 0.6 | 0 | 0 | 0 | 0.2 |
| Death | 0.8 | 0 | 0 | 0 | 0 |
| Victory | 0.8 | 0 | 0 | 0 | 0 |

### 10.8 Music transitions

- Crossfade between music states over 500 ms.
- Floor transitions within a run should not restart the run music abruptly.
- Boss entry should layer in the boss stem over 500 ms.
- Boss death should duck music and play victory fanfare.

---

## 11. Sound effects

All SFX should be short, distinct, and non-intrusive.

Use these event names in implementation.

### 11.1 Core action SFX

| Event | Trigger | Sound description | Duration | Relative gain |
|---|---|---|---:|---:|
| `sfx.tap` | Every accepted run tap | Short woodblock tick | 30 ms | 0.18 |
| `sfx.move` | Move action | Low soft thud | 80 ms | 0.30 |
| `sfx.attack` | Attack action | Mid-pitch slash, noise + rising sawtooth | 100 ms | 0.35 |
| `sfx.parry` | Parry action | Resonant bell, high and clean | 250 ms | 0.50 |
| `sfx.flick` | Flick action | Weak spark, short square blip | 50 ms | 0.15 |
| `sfx.parry.ready` | Parry cooldown ends | Soft chime | 100 ms | 0.25 |

#### Why these are distinct

- Move is low and soft.
- Attack is mid and cutting.
- Parry is high and resonant.
- Flick is weak and dry.

The player should be able to tell the actions apart by ear without looking.

### 11.2 Damage SFX

| Event | Trigger | Sound description | Duration | Relative gain |
|---|---|---|---:|---:|
| `sfx.player.damage` | Player takes damage | Low descending hurt tone | 200 ms | 0.50 |
| `sfx.enemy.damage` | Enemy/barrier takes damage | Short hit tick | 40 ms | 0.20 |
| `sfx.enemy.die` | Enemy dies | Small shatter + descending blip | 150 ms | 0.30 |
| `sfx.barrier.hit` | Barrier takes damage | Metallic clank | 50 ms | 0.25 |
| `sfx.barrier.break` | Barrier breaks | Larger clank + gear shatter | 300 ms | 0.40 |

### 11.3 Projectile SFX

| Event | Trigger | Sound description | Duration | Relative gain |
|---|---|---|---:|---:|
| `sfx.projectile.fire` | Enemy fires | Short pew, rising pitch | 80 ms | 0.20 |
| `sfx.projectile.hit` | Projectile hits player | Low pop | 60 ms | 0.35 |
| `sfx.projectile.destroy` | Projectile destroyed | Small zap | 50 ms | 0.20 |

### 11.4 Trap SFX

| Event | Trigger | Sound description | Duration | Relative gain |
|---|---|---|---:|---:|
| `sfx.trap.warning` | Trap enters warning phase | Soft alarm pulse | 200 ms | 0.20 |
| `sfx.trap.danger` | Trap becomes active | Sharp click | 80 ms | 0.30 |

### 11.5 Door and room SFX

| Event | Trigger | Sound description | Duration | Relative gain |
|---|---|---|---:|---:|
| `sfx.door.locked` | Player tries to enter locked door | Dull thud | 100 ms | 0.30 |
| `sfx.door.unlock` | Door unlocks | Gear ratchet, 3 ticks | 300 ms | 0.30 |
| `sfx.door.open` | Player enters open door | Soft whoosh | 200 ms | 0.25 |
| `sfx.room.clear` | Room cleared | Two-note chime | 200 ms | 0.30 |

### 11.6 Relic and shard SFX

| Event | Trigger | Sound description | Duration | Relative gain |
|---|---|---|---:|---:|
| `sfx.relic.acquire` | Relic picked up | Bright three-note arpeggio | 250 ms | 0.35 |
| `sfx.relic.convert` | Relic converted to shards | Small shard/coin sound | 200 ms | 0.30 |
| `sfx.shard.pickup` | Shard picked up | Tiny crystal ping | 50 ms | 0.15 |

### 11.7 Boss SFX

| Event | Trigger | Sound description | Duration | Relative gain |
|---|---|---|---:|---:|
| `sfx.boss.warning` | Boss attack warning | Low horn or rumble | 400 ms | 0.40 |
| `sfx.boss.charge` | Boss charge | Rumble + whoosh | 300 ms | 0.40 |
| `sfx.boss.stomp` | Boss stomp | Heavy thud | 200 ms | 0.45 |
| `sfx.boss.phase` | Boss phase change | Stinger + chime | 400 ms | 0.45 |

### 11.8 UI SFX

| Event | Trigger | Sound description | Duration | Relative gain |
|---|---|---|---:|---:|
| `sfx.ui.tap` | Menu tap | Soft click | 30 ms | 0.20 |
| `sfx.upgrade.cursor` | Upgrade cursor moves | Very soft click | 30 ms | 0.12 |
| `sfx.upgrade.confirm` | Upgrade purchased | Positive two-note chime | 150 ms | 0.30 |
| `sfx.upgrade.cannot` | Cannot buy | Dull buzz | 150 ms | 0.25 |
| `sfx.upgrade.maxed` | Maxed | Dry high click | 50 ms | 0.15 |
| `sfx.ui.cancel` | Cancel upgrade | Descending blip | 150 ms | 0.25 |

### 11.9 State SFX

| Event | Trigger | Sound description | Duration | Relative gain |
|---|---|---|---:|---:|
| `sfx.death` | Player dies | Low drone + tempo break | 800 ms | 0.50 |
| `sfx.victory` | Victory | Bright fanfare | 800 ms | 0.50 |

### 11.10 Optional zone-change SFX

Optional:

- When the Tempo marker crosses into a new zone, play a very quiet click.
- Move zone: 600 Hz.
- Attack zone: 900 Hz.
- Parry zone: 1400 Hz.
- Duration: 20 ms.
- Gain: 0.08.

If this becomes noisy, cut it.

---

## 12. Optional implementation hints

The following code is optional. It is included to reduce ambiguity for the engineering agent.

### 12.1 Tempo bar drawing hint

```ts
function drawTempoBar(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  tempo: number,
  nextTempo: number,
  parryCooldown: number,
  parryMaxCooldown: number
) {
  const moveEnd = 0.39 * w;
  const attackEnd = 0.69 * w;

  // Background
  ctx.fillStyle = "#10131A";
  ctx.fillRect(x, y, w, h);

  // Zones
  ctx.fillStyle = "rgba(58, 224, 255, 0.18)";
  ctx.fillRect(x, y, moveEnd, h);

  ctx.fillStyle = "rgba(255, 176, 32, 0.18)";
  ctx.fillRect(x + moveEnd, y, attackEnd - moveEnd, h);

  ctx.fillStyle = "rgba(168, 85, 247, 0.18)";
  ctx.fillRect(x + attackEnd, y, w - attackEnd, h);

  // Current tempo fill
  ctx.fillStyle = "rgba(255, 255, 255, 0.22)";
  ctx.fillRect(x, y, (tempo / 100) * w, h);

  // Parry cooldown overlay
  if (parryCooldown > 0) {
    const zoneX = x + attackEnd;
    const zoneW = w - attackEnd;

    ctx.fillStyle = "rgba(16, 19, 26, 0.72)";
    ctx.fillRect(zoneX, y, zoneW, h);

    const readyFraction = 1 - parryCooldown / parryMaxCooldown;
    ctx.fillStyle = "rgba(255, 255, 255, 0.25)";
    ctx.fillRect(zoneX, y, zoneW * readyFraction, h);

    // Simple hatch for colorblind safety
    ctx.strokeStyle = "rgba(255, 255, 255, 0.12)";
    ctx.lineWidth = 1;
    for (let i = 0; i < zoneW; i += 6) {
      ctx.beginPath();
      ctx.moveTo(zoneX + i, y + h);
      ctx.lineTo(zoneX + i + h, y);
      ctx.stroke();
    }
  }

  // Marker
  const markerX = x + (nextTempo / 100) * w;
  const markerY = y + h / 2;

  let action: "move" | "attack" | "parry" | "flick";
  if (nextTempo <= 39) {
    action = "move";
  } else if (nextTempo <= 69) {
    action = "attack";
  } else {
    action = parryCooldown > 0 ? "flick" : "parry";
  }

  // Draw marker circle and icon here.
  // The icon must be one of:
  // move: right arrow
  // attack: slash
  // parry: ring
  // flick: broken ring
}
```

### 12.2 SFX naming hint

Use a single SFX function:

```ts
playSfx("sfx.parry");
playSfx("sfx.player.damage");
playSfx("sfx.upgrade.cannot");
```

Do not use different naming conventions for the same event.

---

## 13. Load-bearing visual notes

These decisions are not optional decoration.

### 13.1 The Tempo marker is the primary control

The marker must show the exact result of the next tap.

It must show:

- Move, Attack, Parry, or Flick.
- Parry cooldown state.
- Flick state when Parry is unavailable.

If the marker is ambiguous, the game fails.

### 13.2 Do not add a visible button

The whole screen is the button.

A visible button would:

- Imply a separate control.
- Distract from cadence.
- Break the one-button fantasy.

### 13.3 Do not use color alone

Every important state needs a non-color cue.

This includes:

- Tempo zones.
- Parry cooldown.
- Flick.
- Trap warning.
- Trap danger.
- Enemy projectiles.
- Upgrade affordability.

### 13.4 Do not change action colors by floor

Move is always cyan.

Attack is always amber.

Parry is always violet-white.

Flick is always gray.

If a floor palette conflicts, change the floor palette.

### 13.5 Do not make music dictate gameplay tempo

The music may have a BPM, but the player’s Tempo is independent.

Do not add a visual metronome that tells the player when to tap.

Do not flash the Tempo bar to the music beat.

### 13.6 Do not make Flick look like Parry

Flick is a failed Parry.

It must be:

- Smaller.
- Grayer.
- Weaker.
- Shorter.
- Without i-frame flash.
- Without screen shake.

### 13.7 Do not make Parry cooldown invisible

The player must know when Parry is unavailable.

The Parry zone must be:

- Darkened.
- Hatched.
- Swept as cooldown recovers.
- Flashed when ready.

### 13.8 Do not add hover

There is no mouse hover interaction.

All menus work by tap/click only.

### 13.9 Do not add a pause button

Pause is automatic on focus loss.

Resume is any tap.

### 13.10 Do not add extra HUD elements that compete with Tempo

Avoid:

- Minimap.
- Enemy HP bars except boss.
- Room type labels.
- Skill icons.
- Multiple status bars.
- Large center-screen notifications.

---

## 14. Cut list

The following are intentionally cut:

- No visible on-screen button.
- No hover effects.
- No settings menu.
- No character skins.
- No lore screens.
- No minimap.
- No room labels.
- No enemy HP bars except boss.
- No projectile trails longer than 0.2 seconds.
- No screen shake on normal attacks.
- No full-screen white flash for normal attacks.
- No music that forces a specific tap rhythm.
- No second input of any kind.
- No pause button.
- No level select.
- No endless mode visuals.
- No multiplayer indicators.

If a visual feature is not in this document, it should be cut unless required by `gameplay.md`.

---

## 15. Visual acceptance criteria

The visual design is complete when:

- A player can see what the next tap will do without reading numbers.
- The Tempo marker clearly distinguishes Move, Attack, Parry, and Flick.
- Parry cooldown is clearly visible.
- The player can distinguish Move, Attack, Parry, and Flick by sound alone.
- Enemy projectiles are clearly distinguishable from player effects.
- Spike traps clearly show safe, warning, and danger phases.
- Doors clearly show locked, unlocking, and open states.
- Relic slots clearly show empty, filled, and rarity.
- Shard count is always readable.
- Boss HP is visible during boss rooms.
- Boss attacks have at least 0.5 seconds of visual warning.
- Each floor looks distinct but uses the same action colors.
- The Upgrade state can be used with one button only.
- The Title, Death, Victory, and Upgrade states all use one button only.
- The game can be played with audio muted.
- The game remains readable with colorblind-safe cues.
- The game does not require any input other than one tap.