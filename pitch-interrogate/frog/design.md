# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| “a platformer where you play as a frog” | Player is Mire, a side-on 2D real-time platformer: 4.1, 5 |
| Mire is a mud-stained tree frog trying to get home after the town drains the ponds | Title/story framing: 7, 4.8; visual character: 3, 5 |
| Whole game is a linear route home through town, made of single crossings | 12 authored crossings, no hub: 4.8 |
| Each crossing starts on a safe wet perch and ends at another safe wet perch | Crossing rules: 4.4; safe perch records: 4.4, 4.7 |
| Mire runs, leaps, clings, and uses her tongue to swing, snag keys, pull planks, nudge objects, operate latches | Core mechanics: 4.1, 4.2; supporting mechanics: 4.5, 4.6 |
| Tongue is core traversal, limited by reach, line of sight, barriers, and real anchor validity | Tongue system: 4.2; barriers: 4.2, 4.3 |
| No fighting, shiny collectibles, health bars, lives, upgrades, hub, permanent puzzle changes | Scope exclusions: 0.2, 4.9, 7 |
| Hazards are ordinary human-scale dangers with behavior; being caught fails the current crossing and returns to last safe perch | Hazard system: 4.3; capture/reset: 4.4 |
| Falling off normal ledge only changes landing unless landing place is active hazard; lower areas may continue if they lead onward | Fall rules: 4.1, 4.4 |
| Harder by exposure, hazard schedules, precise tongue interactions | Difficulty progression: 4.8 |
| Side-on 2D platformer view, low camera close to Mire, readable horizontal routes | Camera and visual readability: 1.1, 3 |
| Real-time | Fixed-step real-time loop: 1.1, 1.2 |
| Tone: small animal moving through a human-sized world; every crossing is about getting across without being caught | Visual/audio/gameplay feel: 3, 4.9, 6 |
| Look and sound: readable low-scale household/outdoor spaces; hazards announced by visible motion and diegetic sound, not UI meters/bars | Visual spec: 3; audio spec: 6; HUD: 7 |
| Core mechanics: run, leap, cling, tongue, hazards and being caught, crossing | Tier 1: 0.3, 4.1–4.4 |
| Supporting mechanics: keys, loose planks, intermediate safe perches | Tier 2: 0.3, 4.5–4.7 |
| Extra mechanics: none | No Tier 3 mechanics: 0.3 |
| Content roster: Mire, hidden marsh, town drains ponds, linear route, perches, spaces, wires, keys, loose planks, latches, gate catches, people, hand, dog, bucket, drains, drain current, sprinklers, lawnmowers, traffic, cat, damp pot, rain trap, shaded planter, sticky surfaces, non-sticky surfaces, barriers, weak anchors | Records/rosters: 4.2; level table: 4.8; characters: 5 |
| Left out: fighting, collectibles, combat, health bars, death states, lives, upgrades, collectible items, persistent unlocks, permanent changes, ordinary ledges as safe perches, climbing smooth glass/painted siding, tongue altering hazards, meters, clocks, timers, hub, etc. | Explicit exclusions and sanity checks: 0.2, 4.4, 4.9, 7, A |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| Player is Mire, a mud-stained tree frog | Final. One playable character. | Request fixes the player. |
| Game is a platformer | Final. Real-time side-on 2D platforming with run/leap/cling/tongue. | Request fixes genre. |
| The whole game is a linear route home through town | Final. 12 ordered crossings, no hub, no level select. | Request fixes structure. |
| Each level is a single crossing from safe perch to safe perch | Final. Each authored crossing has one start perch and one end perch. | Request fixes run structure. |
| Being caught fails the crossing and returns to last safe perch | Final. No death, no lives, only lost progress. | Request fixes punishment. |
| Falling from normal ledges is not failure by itself | Final. Only explicit loss zones or active hazards cause failure. | Request fixes forgiving fall behavior. |
| Reset restores puzzle state beyond last safe perch | Final. Authored objects carry `order`; reset restores objects with `order >= checkpoint.order`. | Makes the crossing clean and repeatable. |
| No fighting, collectibles, health, lives, upgrades, hub, permanent puzzle changes | Final. These systems are not implemented. | Request explicitly excludes them. |
| View is side-on 2D with low camera close to Mire | Final. Canvas viewport 960×540; camera follows Mire with target y below Mire so ground stays low and readable. | Matches requested readability. |
| Time is real-time | Final. Fixed 60 Hz simulation, no turn-based or time-slowing mechanics. | Request fixes time. |
| Core mechanics are run, leap, cling, tongue, hazards, crossing | Final. Tier 1 implements exactly these systems. | Request bands core mechanics. |
| Supporting mechanics are keys, loose planks, intermediate safe perches | Final. Tier 2 implements exactly these additions. | Request bands supporting mechanics. |
| Extra mechanics: none | Final. No Tier 3 gameplay mechanics. | Request says none. |
| Total crossings | **12 crossings.** | Enough to express a town route and gradual difficulty without becoming a hub game. |
| Final crossing | Crossing 12 reaches hidden marsh and ends the game. | Request requires hidden marsh as ending. |
| Standard canvas | **960×540 logical viewport**, CSS-scaled to browser window. | Common readable browser canvas size; supports low-scale side view. |
| World units | **pixels**, **seconds**, 60 Hz fixed step. | Simple deterministic platformer physics. |
| Coordinate axes | x increases right, y increases down; origin top-left of level. | Standard canvas coordinates. |
| Fixed-step loop | `dt = 1/60` fixed; render interpolation optional. | Prevents physics variability. |
| Deterministic RNG | Mulberry32 seeded from level id for optional non-gameplay jitter only. | Avoids random failure causes. |
| Player visual size | 24×18 px sprite. | Small enough for low-scale human world, large enough to read. |
| Player collision box | 20×14 px centered. | Forgiving but readable. |
| Mouth point | `x + 10 * facing`, `y - 2`. | Gives tongue a clear visual origin. |
| Run max speed | **150 px/s**. | Fast enough for traversal, slow enough for hazard timing. |
| Run acceleration | **1100 px/s²** grounded, **650 px/s²** airborne. | Responsive but controllable. |
| Ground friction | **1400 px/s²**. | Quick stop for precise platforming. |
| Air drag | **140 px/s²** opposite horizontal velocity. | Limits air steering. |
| Jump velocity | **-360 px/s**. | Gives ~72 px jump height with chosen gravity, enough for small ledges. |
| Gravity | **1000 px/s²**. | Standard snappy platformer feel. |
| Max fall speed | **620 px/s**. | Prevents tunneling and over-long falls. |
| Variable jump | If leap released before apex, vertical velocity multiplies by **0.45**. | Gives control without adding new mechanics. |
| Coyote time | **0.08 s**. | Forgives edge runs. |
| Jump buffer | **0.12 s**. | Makes ledges feel responsive. |
| Double jump | **Not allowed.** | Preserves puzzle constraints. |
| Cling input | Hold `Shift` while touching a sticky surface. | Separate from leap; no attack. |
| Cling surfaces | Only surfaces with `sticky=true`: visibly damp, mossy, rough, wet, or otherwise frog-sticky. | Matches request. |
| Non-cling surfaces | Smooth glass, painted siding, `sticky=false`. | Request explicitly forbids climbing them. |
| Cling hold | While clinging, vertical velocity forced to 0; gravity ignored. | Frog can hold still. |
| Cling shimmy speed | **70 px/s** along wall/ceiling. | Lets Mire reposition under ledges without becoming a climbing system. |
| Cling release | Stop holding cling, or press leap. Pressing leap while clinging gives impulse **160 px/s away from surface**, **240 px/s upward**. | Lets Mire detach and reposition; it is a transition from cling/leap, not a separate mechanic. |
| Clinging to hazard/moving surfaces | Allowed if surface is marked `sticky=true` and `hazard_surface=true`; if hazard becomes active or active hitbox intersects, Mire is caught. | Request allows getting caught while clinging. |
| Tongue aim | Mouse pointer or touch drag aims from mouth point. Keyboard fallback: pressing `E` targets nearest valid anchor within ±60° of facing direction. | Primary mouse is intuitive; keyboard fallback preserves accessibility. |
| Tongue grab/release | Left mouse button or `E`. Holding maintains attachment; releasing ends it. | No cooldown, no stamina. |
| Tongue max reach | **220 px** from mouth to anchor point. | Makes anchors deliberate and readable. |
| Tongue extension/retraction animation speed | **1000 px/s**. | Fast enough not to feel sluggish, visible enough to read. |
| Tongue rope minimum length | **24 px**. | Prevents Mire occupying anchor exactly. |
| Tongue rope constraint | If distance exceeds max, clamp position to max length and remove radial velocity component; preserve tangential velocity with 0.99 damping. | Gives readable swing without complex rope physics. |
| Tongue fixed-anchor pull | While attached to a fixed anchor, if move input points within 45° toward anchor, tongue shortens at **180 px/s** to minimum length. | Core traversal pull without needing authored movable objects. |
| Tongue movable-object pull | While attached to a movable object, object is dragged toward mouth with max **160 px/s**; max authored displacement **180 px** unless it snaps into a target. | Enough for keys and planks without full rigid-body simulation. |
| Tongue can target only environmental anchors | Valid anchors: wires, hooks, keys, latches, gate catches, loose planks, wet rims, mossy pegs. Hazards are never anchors. | Request forbids tongue altering hazards. |
| Line of sight | Segment ray from mouth to anchor; blocked by `block_tongue=true` objects: walls, glass, mesh. | Request fixes barriers. |
| Weak anchors | Have `grip=weak`, `angle_limit=30°`, `max_impulse=180 px/s`. Strong anchors have `angle_limit=120°`, no impulse limit. | Creates anchor-choice difficulty. |
| Weak anchor slip | If grab angle outside limit or player velocity at grab exceeds limit, tongue slips after **0.12 s**, detaches, no capture penalty. | Bad grab leaves Mire exposed, not punished separately. |
| No tongue cooldown | None. | Request forbids. |
| No tongue stamina | None. | Request forbids. |
| Hazard capture | Active hazard hitbox intersecting player hitbox, or player entering bucket/drain active zone, causes capture. | Request fixes capture. |
| Capture result | `game.state = captured`; after 0.45 s reset to last safe perch. No death. | Request fixes punishment. |
| Lost result | Player inside explicit `loss_zone` or y > level height + 64 causes lost; after 0.45 s reset to last safe perch. | Request fixes lost failure. |
| Normal falling | No fall damage, no automatic fail, lower ledges may continue. | Request fixes forgiving falls. |
| Safe perches | Only records with `safe=true` are safe. Normal platforms are never safe. | Request forbids ordinary ledges as safe perches. |
| Intermediate safe perches | Exactly 3 authored: rain trap in gutter, damp pot, shaded underside of planter. They set checkpoint and reset beyond. | Request says rare and deliberate. |
| Keys | Exactly 3 authored keys. Not collectibles. | Request says keys are latch objects, not collectible items. |
| Latches | Exactly 3 authored latches. | Matches keys/gate puzzle content. |
| Gate catches | Exactly 2 authored gate catches. | Matches key-operated gates. |
| Loose planks | Exactly 4 authored loose planks. | Matches temporary bridge/nudge content. |
| People | Exactly 2 authored walking people. | Request lists people as hazards. |
| Hand | Exactly 4 authored hand capture hazards. | Request lists hand as hazard. |
| Dog | Exactly 2 authored dog hazards. | Request lists dog as hazard. |
| Bucket | Exactly 3 authored bucket capture hazards. | Request lists bucket as hazard. |
| Open drains | Exactly 5 authored drain hazards. | Request lists open drains as hazards. |
| Sprinklers | Exactly 5 authored sprinklers. | Request lists sprinklers as hazards. |
| Lawnmowers | Exactly 5 authored lawnmowers. | Request lists lawnmowers as hazards. |
| Traffic | Exactly 6 authored traffic hazards. | Request lists traffic as hazards. |
| Cat | Exactly 5 authored cats. | Request lists cat as hazard. |
| Pickups | **None.** | Request forbids collectibles. |
| Upgrades | **None.** | Request forbids upgrades. |
| Lives | **None.** | Request forbids lives. |
| Health | **None.** | Request forbids health. |
| UI meters/bars | **None.** | Request forbids UI meters or bars. |
| HUD | No persistent gameplay HUD. Only state screens and brief non-metric text. | Keeps tone and diegetic readability. |
| Art style | Flat readable vector-like shapes, low-scale household objects, wet specular highlights, 2px dark outlines, muted dusk palette. | Matches requested readable low-scale household spaces. |
| Audio | Synthesized diegetic sounds and low ambient route sound. No UI meters. | Builder has audio API; request wants diegetic sound. |
| Tier 1 | Core mechanics only, plus a 4-crossing vertical slice that can be completed. | Request bands core mechanics as Tier 1. |
| Tier 2 | Supporting mechanics and full 12-crossing route. | Request bands supporting mechanics as Tier 2. |
| Tier 3 | None. | Request says extra mechanics none. |

## 0.3 Tiers

| Tier | Priority | Scope | Mechanics included | Not included | Done when |
| --- | --- | --- | --- | --- | --- |
| 1 | Highest | Core mechanics and a 4-crossing vertical slice. | run, leap, cling, tongue grab/swing/pull, hazard capture, crossing reset, start/end safe perches, loss zones, core visual/audio style, camera, minimal input. | Keys, latches, gate catches, loose planks, intermediate safe perches, full 12-crossing route, all remaining hazard variants. | Player can complete crossings 1–4, is captured/lost correctly, resets to last safe perch, and reaches the vertical-slice end perch. |
| 2 | Next | Supporting mechanics and complete route home. | keys, latches, gate catches, loose planks, intermediate safe perches, remaining hazard types, crossings 5–12, hidden marsh ending. | No new gameplay mechanics. | All 12 crossings load and can be completed; supporting mechanics work and reset; intermediate checkpoints work; final crossing ends at hidden marsh. |
| 3 | Optional/non-mechanical | Validation, debug, accessibility polish only. | No gameplay mechanics. | Any extra system. | Not required for “extra mechanics”; only if needed for debugging or accessibility. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Value | Number | Meaning |
| --- | ---: | --- |
| Canvas logical width | 960 px | Fixed viewport for simulation readability. |
| Canvas logical height | 540 px | Fixed viewport for simulation readability. |
| Fixed step | 1/60 s | Game logic tick. |
| Maximum render delta | 0.25 s | Prevents spiral of death. |
| Coordinate origin | top-left of level | Canvas convention. |
| x axis | positive right | Movement and camera. |
| y axis | positive down | Gravity and falling. |
| Angle | radians, 0 = right, positive clockwise | Canvas-compatible. |
| Player visual size | 24×18 px | Sprite bounds. |
| Player collision size | 20×14 px | Gameplay hitbox. |
| Player origin | center of collision box | Physics and camera. |
| Mouth point | center + `(10*facing, -2)` | Tongue origin. |
| World speed unit | px/s | All movement. |
| Acceleration unit | px/s² | Physics. |
| Reach unit | px | Tongue and hazard ranges. |
| Level minimum width | 1200 px | Smallest authored crossing. |
| Level maximum width | 2400 px | Largest authored crossing. |
| Level minimum height | 540 px | Smallest authored crossing. |
| Level maximum height | 1200 px | Largest authored crossing. |

## 1.2 Important conventions

| Convention | Rule |
| --- | --- |
| Fixed-step simulation | All gameplay systems update only with `dt = 1/60`. Rendering may interpolate but never mutates state. |
| Determinism | No unseeded randomness in gameplay. If jitter is needed, use seeded Mulberry32 from `level.id`. |
| Collision | Use swept AABB for player and moving hazards. Static platforms use AABB. |
| Raycasts | Tongue and hazard line-of-sight use line segment against axis-aligned rectangles. |
| Safety | A perch is safe only if record has `safe=true`. Normal platforms never have `safe=true`. |
| Reset order | Objects and hazards have integer `order`. Checkpoints have integer `order`. Reset restores records with `order >= checkpoint.order`. |
| No UI clocks | Internal durations exist for hazard schedules, but no UI shows time, countdown, timer, clock, or meter. |
| No hazard alteration by tongue | Anchor list excludes hazard records. |
| No collectible inventory | Keys and planks are world objects with states, not inventory items. |
| No combat | No attack input, no damage, no health, no enemy health. |
| No permanent cross-crossing state | Completion only advances `game.crossing_index`; it does not persist object states. |
| No permanent puzzle changes | All crossing puzzle state resets on capture, lost, or next crossing start. |
| Accessibility | Keyboard fallback for tongue targeting; all core actions must work with keyboard and pointer. |
| Debug | Debug functions are read-only except explicitly named debug mutation functions. |

# 2. CONTRACTS

## 2.1 Module layout

| Module | Responsibility |
| --- | --- |
| `index.html` | Canvas, HTML overlay screens, CSS hooks. |
| `css/ui.css` | HTML/CSS only screens, no gameplay HUD meters. |
| `js/main.js` | Bootstrap, state machine, crossing advance. |
| `js/loop.js` | Fixed-step update and render scheduling. |
| `js/input.js` | Keyboard/pointer state, tongue aim, pause. |
| `js/camera.js` | Low camera follow, clamping, capture shake. |
| `js/physics.js` | Swept AABB, raycasts, rope constraint. |
| `js/player.js` | Mire states, run/leap/cling, capture/lost. |
| `js/tongue.js` | Aim, grab, release, rope, pull, slip. |
| `js/objects.js` | Keys, latches, gate catches, loose planks, movable state, reset. |
| `js/hazards.js` | People, hand, dog, bucket, drains, sprinklers, lawnmowers, traffic, cat, capture tests. |
| `js/levels.js` | Level records, load, checkpoint order, completion. |
| `js/render.js` | Canvas draw, visuals, effects. |
| `js/audio.js` | Synthesized sound playback. |
| `js/ui.js` | HTML/CSS screen state, no persistent HUD. |
| `js/debug.js` | Debug API. |
| `js/tests.js` | Automated high-level tests. |

## 2.2 Global context

The global context is a plain object passed to systems.

| Field | Type | Required fields / meaning |
| --- | --- | --- |
| `ctx.config` | object | All constants from 4.1–4.3. |
| `ctx.rng` | function | Deterministic RNG seeded by level id. |
| `ctx.input` | object | Current input state and edge events. |
| `ctx.camera` | object | `x`, `y`, `targetX`, `targetY`, `shake`. |
| `ctx.game` | object | `state`, `crossingIndex`, `lastSafePerchId`, `message`, `resetPending`, `gameComplete`. |
| `ctx.level` | object | Current level record. |
| `ctx.player` | object | Player record. |
| `ctx.tongue` | object | Tongue record. |
| `ctx.hazards` | array | Current hazard records. |
| `ctx.objects` | array | Current movable/latch/key/plank/gate records. |
| `ctx.anchors` | array | Current tongue anchor records. |
| `ctx.perches` | array | Safe perch records. |
| `ctx.platforms` | array | Solid/static platform records. |
| `ctx.lossZones` | array | Explicit loss rectangles. |
| `ctx.debug` | object | Enabled flag and debug-only overrides. |

Player record fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Always `"mire"`. |
| `pos` | `{x,y}` | Center position. |
| `vel` | `{x,y}` | Velocity. |
| `facing` | -1 or 1 | Left/right. |
| `state` | string | `grounded`, `air`, `clinging`, `captured`, `lost`, `safe`, `resetting`. |
| `grounded` | bool | On non-hazard safe ground. |
| `clinging` | bool | Attached to sticky surface. |
| `clingNormal` | `{x,y}` | Surface normal for detachment. |
| `coyoteTimer` | number | Remaining coyote time. |
| `jumpBuffer` | number | Remaining buffered jump. |
| `lastSafePerchId` | string | Current checkpoint. |
| `captureReason` | string | `hazard`, `bucket`, `drain`, `hand`, `dog`, `cat`, `traffic`, `mower`, `sprinkler`, `person`, `lost`. |

Tongue record fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `state` | string | `idle`, `extending`, `attached`, `releasing`, `slipping`. |
| `aim` | `{x,y}` | World aim point. |
| `targetId` | string or null | Current anchor/object id. |
| `anchorPoint` | `{x,y}` | Current attachment point. |
| `length` | number | Current rope length. |
| `maxLength` | number | 220. |
| `minLength` | number | 24. |
| `slipTimer` | number | Weak anchor slip delay. |
| `grabAngleError` | number | Debug value. |
| `grabImpulse` | number | Debug value. |

Level record fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | `c01` through `c12`. |
| `index` | number | 1–12. |
| `name` | string | Display name. |
| `width` | number | World width. |
| `height` | number | World height. |
| `startPerchId` | string | Guaranteed start. |
| `endPerchId` | string | Completion target. |
| `checkpoints` | array | Safe perch ids. |
| `platforms` | array | Static platforms. |
| `anchors` | array | Tongue anchors. |
| `hazards` | array | Hazard instances. |
| `objects` | array | Keys/latches/gates/planks. |
| `perches` | array | Safe perch records. |
| `lossZones` | array | Loss rectangles. |

Hazard record fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Unique per level. |
| `type` | string | One of `person`, `hand`, `dog`, `bucket`, `open_drain`, `sprinkler`, `lawnmower`, `traffic`, `cat`. |
| `order` | number | Reset order. |
| `state` | string | Type-specific state. |
| `hitbox` | `{x,y,w,h}` or circle | Active capture box. |
| `active` | bool | Whether capture is enabled. |
| `warning` | bool | Visual/audio warning active. |
| `path` | array | For moving hazards. |
| `initial` | object | Reset snapshot. |

Object record fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Unique per level. |
| `type` | string | `key`, `latch`, `gate_catch`, `gate`, `plank`. |
| `order` | number | Reset order. |
| `pos` | `{x,y}` | Current position. |
| `initialPos` | `{x,y}` | Reset position. |
| `state` | string | `in_latch`, `loose`, `in_gate`, `closed`, `open`, `resting`, `dragging`, `placed`. |
| `anchorPoint` | `{x,y}` | Tongue attachment point. |
| `pullAxis` | `{x,y}` | For keys/latches. |
| `targetId` | string | Gate catch or bridge slot. |

Safe perch record fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Unique per level. |
| `type` | string | `start`, `end`, `rain_trap`, `damp_pot`, `planter_underside`. |
| `safe` | bool | Always true. |
| `end` | bool | True only for end perch. |
| `checkpoint` | bool | True for start and intermediates. |
| `order` | number | Reset order. |
| `hitbox` | `{x,y,w,h}` | Safe overlap. |

## 2.3 Module specifics

| Module | Required functions |
| --- | --- |
| `loop.js` | `start(ctx)`, `step(dt)`, `render(ctx)`, `setPaused(bool)` |
| `input.js` | `getState()`, `consumeJump()`, `consumeTongueGrab()`, `getPointerWorld()`, `setKeyboardFallback(bool)` |
| `camera.js` | `update(ctx, dt)`, `clampToLevel(ctx)`, `shake(amount)` |
| `physics.js` | `moveAndCollide(entity, dt, solids)`, `raycast(a, b, blockers)`, `applyRope(entity, anchorPoint, maxLen)`, `intersectAABB(a,b)` |
| `player.js` | `spawn(ctx, perch)`, `update(ctx, dt)`, `capture(ctx, reason)`, `lose(ctx)`, `reset(ctx, perchId)`, `state()` |
| `tongue.js` | `update(ctx, dt)`, `aim(ctx, worldPoint)`, `grab(ctx)`, `release(ctx)`, `canGrab(ctx, anchor)`, `state()` |
| `hazards.js` | `update(ctx, dt)`, `reset(ctx, order)`, `captureTest(ctx)`, `state()` |
| `objects.js` | `update(ctx, dt)`, `reset(ctx, order)`, `onTongueAttach(ctx, obj)`, `onTongueDetach(ctx, obj)`, `state()` |
| `levels.js` | `load(ctx, crossingIndex)`, `complete(ctx)`, `setCheckpoint(ctx, perchId)`, `resetBeyond(ctx, order)`, `next(ctx)` |
| `render.js` | `draw(ctx)`, `drawPlayer(ctx)`, `drawTongue(ctx)`, `drawHazards(ctx)`, `drawObjects(ctx)`, `drawPerches(ctx)` |
| `audio.js` | `play(name, params)`, `setAmbient(name, level)`, `stopAll()` |
| `ui.js` | `showScreen(state)`, `hideScreens()`, `setMessage(text)`, `showCrossingIntro(level)` |
| `debug.js` | See 8. |
| `tests.js` | See 9. |

# 3. VISUAL SPEC

The look is a readable low-scale household world where Mire is tiny and everything else is familiar human-scale: wet stones, backyard fences, shed walls, gutters, clotheslines, buckets, lawnmowers, sprinkler heads, drains, car lanes, cat shapes, and ordinary hands. Shapes are flat and slightly cartoonish but not shiny: 2px dark outlines, solid low-saturation fills, small speckles for mud, and bright specular streaks only where surfaces are wet. Safe perches are the only glowing-with-water places. Hazards are readable by silhouette and motion, not UI indicators.

## 3.1 Lighting and atmosphere

| Element | Rule |
| --- | --- |
| Global lighting | Overcast dusk. Low contrast, cool ambient. No harsh god rays. |
| Wet surfaces | Narrow pale specular streaks, animated shimmer at 0.8 Hz. |
| Safe perches | Slight green/cyan water shimmer, soft dark wet halo, tiny droplet glints. |
| Hazards | Warm or high-contrast accents: red mower, blue sprinkler water, gray cat, yellow car, white hand shadow. |
| Capture effect | Brief dark vignette and a non-scary capture flourish: hand closing, bucket rim, drain swirl, net shadow. No blood, no death icon. |
| Reset effect | 0.45 s fade with water drop sound; Mire reappears sitting on safe perch. |

## 3.2 Space

| Space | Visual cues |
| --- | --- |
| Backyards | Grass strips, fence slats, soil beds, pots, garden tools. |
| Rooftops | Tile shingles, gutters, chimneys, antenna wires. |
| Flooded gutters | Dark gutter channel with water shimmer; rain trap visible as wet catch basin. |
| Drains | Dark circular mouth, wet grate, small bubbles when gurgling. |
| Buckets | Plastic rim, handle, interior dark. |
| Wires | Thin gray clothesline with visible tension; damp/mossy pegs are anchors. |
| Latches/keys | Small metal key, latch plate, gate catch. No glow. |
| Planks | Weathered wood, slightly damp edges. |
| People/hands | Simple human shapes, large hands, ordinary clothing colors. |
| Traffic | Small car silhouettes moving along road, headlights off. |
| Cat | Crouched gray cat, eyes as small bright dots only during warning. |
| Hidden marsh | Final area with reeds, wet moss, dark water, soft green safe glow. |

## 3.3 Visual recipe table

| Element | Visual | Palette | Motion/readability |
| --- | --- | --- | --- |
| Mire body | Compact tree frog, mud-stained back, wide eyes. | body `#8fbf68`, belly `#d7e7a5`, mud `#7d5a3f`, eye `#f5f0c8`, pupil `#12141c` | Facing flips; mouth offset visible; tongue origin obvious. |
| Safe perch | Wet stone, damp pot, rain trap, planter underside. | wet base `#2e5a4d`, shimmer `#7bd7b3`, moss `#6d8f4f` | Always visibly wet; never looks like normal ledge. |
| Normal platform | Dry wood/stone/siding. | wood `#7a6450`, stone `#55606b`, siding `#8a7f76` | No water shimmer; not safe. |
| Sticky surface | Moss, damp brick, rough stone, wet wood. | moss `#6d8f4f`, damp `#3c6b5b` | Small speckle texture; clingable. |
| Non-sticky surface | Smooth glass, painted siding. | glass `#7fa7c9`, paint `#a89e91` | Flat specular only; no moss. |
| Tongue | Pink line from mouth, slight taper. | tongue `#e6879c`, outline `#5b2c38` | Extends/retracts visibly; taut when attached. |
| Wire anchor | Thin taut wire with damp peg. | wire `#b7c0c7`, peg `#8b7a62` | Anchor point is a small wet dot. |
| Weak anchor | Wet string, damp leaf, loose peg. | weak `#879f72`, damp `#3c6b5b` | Slight wobble; less solid outline. |
| Key | Small metal key, no glow. | key `#c4a25a`, dark outline `#4a3b1e` | Can be grabbed; not collectible. |
| Latch | Plate with key slot. | metal `#9aa0a6`, wood `#6a5745` | Key extraction visible along axis. |
| Gate catch | Metal catch on gate. | metal `#9aa0a6` | Key insertion target has dark socket. |
| Gate | Wooden gate. | wood `#6a5745` | Closed is solid; open swings away. |
| Loose plank | Weathered board. | plank `#8b7256`, wet edge `#3c6b5b` | Drags with visible tongue line. |
| Person | Walking adult shape. | clothes `#5e6672`, skin `#d7b59a` | Footstep shadow; hand reach shadow. |
| Hand | Large ordinary hand. | skin `#d7b59a`, shadow `#1a1d24` | Hover shadow, closing fingers. |
| Dog | Low dog silhouette. | fur `#6d5140`, collar `#b73a2a` | Patrol line visible by footstep dust. |
| Bucket | Plastic bucket. | body `#d9762a`, rim `#f0a500`, interior `#15181d` | Interior dark; capture if entered. |
| Open drain | Circular drain mouth. | hole `#0d1116`, wet `#2e5a4d` | Bubbles during gurgle; swirl during current. |
| Sprinkler | Small sprinkler head. | head `#9aa0a6`, water `#5aa9e6` | Clean arc sweep; water line visible. |
| Lawnmower | Red mower on fixed path. | body `#c44536`, wheels `#1a1d24` | Path shadow; engine shake. |
| Traffic | Car silhouette. | car `#e5e5e5`, tires `#1a1d24`, hazard yellow `#f0a500` | Motion blur not excessive; lane visible. |
| Cat | Gray crouched cat. | fur `#5d5d66`, eyes `#f5c84a` | Crouch, head fix, pounce streak. |
| Hidden marsh | Reeds, water, wet moss. | reeds `#6d8f4f`, water `#2e5a4d`, glow `#7bd7b3` | Safe perch glows gently. |

# 4. GAMEPLAY SPEC

The game is a linear sequence of 12 single-screen or scrolling single-crossing puzzles. Each crossing starts with Mire on a safe wet perch and ends at another safe wet perch. The player runs, leaps, clings, and uses the tongue to traverse. Hazards behave as ordinary world objects: they move, spray, close, flush, drive, or pounce. If a hazard catches Mire, or if she reaches an explicit no-recoverable-route loss zone, the crossing fails and she returns to the last safe perch. Falling from normal ledges is not failure. Supporting mechanics add keys, latches, gates, loose planks, and rare intermediate safe perches. There is no combat, no collectible loop, no health, no lives, no upgrades, and no persistent puzzle state across crossings.

## 4.1 Records and rosters

### 4.1.1 Roster totals

| Category | Count | Notes |
| --- | ---: | --- |
| Playable characters | 1 | Mire only. |
| Crossings | 12 | Linear route home. |
| Start safe perches | 12 | One per crossing. |
| End safe perches | 12 | One per crossing; final is hidden marsh. |
| Intermediate safe perches | 3 | Rain trap, damp pot, shaded planter underside. |
| Pickups | 0 | Explicitly none. |
| Upgrades | 0 | Explicitly none. |
| Lives | 0 | Explicitly none. |
| Health systems | 0 | Explicitly none. |
| People | 2 | Walking capture hazards. |
| Hands | 4 | Closing hand capture hazards. |
| Dogs | 2 | Patrol/chase capture hazards. |
| Buckets | 3 | Static capture hazards. |
| Open drains | 5 | Periodic drain/current hazards. |
| Sprinklers | 5 | Arc-sweep hazards. |
| Lawnmowers | 5 | Fixed-path mowing hazards. |
| Traffic | 6 | Moving car capture hazards. |
| Cats | 5 | Crouch/pounce capture hazards. |
| Keys | 3 | Not collectibles. |
| Latches | 3 | Key holders. |
| Gate catches | 2 | Key insertion targets. |
| Gates | 2 | Closed/open platforms. |
| Loose planks | 4 | Temporary bridges/nudge objects. |
| Tongue anchors | 74 total authored | Wires, weak anchors, keys, latches, planks, wet rims, mossy pegs. Counts per level in 4.8. |
| Loss zones | At least 1 per hazardous vertical/bottom area | Explicit only; normal falls do not fail. |

## 4.2 Player system — Tier 1

### 4.2.1 Input mapping

| Action | Primary input | Keyboard fallback | Notes |
| --- | --- | --- | --- |
| Run left | `A` or Left Arrow | Left Arrow | No attack. |
| Run right | `D` or Right Arrow | Right Arrow | No attack. |
| Leap | `Space` or `W` or Up Arrow | Space | Buffered and coyote supported. |
| Cling | Hold `Shift` | Shift | Only on `sticky=true` surfaces. |
| Tongue aim | Mouse pointer or touch drag | `E` targets nearest valid anchor in facing arc | Pointer is primary. |
| Tongue grab/release | Left mouse button or `E` | `E` | Holding maintains attachment. |
| Pause | `Esc` | Esc | UI only. |

### 4.2.2 States

| State | Entry | Exit |
| --- | --- | --- |
| `grounded` | Collision with non-hazard platform. | Air, captured, lost, safe. |
| `air` | Left platform or jump. | Grounded, clinging, captured, lost. |
| `clinging` | Touch sticky surface and hold cling. | Air, grounded, captured. |
| `captured` | Hazard capture test true. | Reset to last safe perch. |
| `lost` | Loss zone or y > level.height + 64. | Reset to last safe perch. |
| `safe` | Center inside safe perch and stable for 0.2 s. | Normal states after leaving perch. |
| `resetting` | Capture/lost timeout complete. | Spawn at last safe perch. |

### 4.2.3 Movement numbers

| Parameter | Value |
| --- | ---: |
| Run max speed | 150 px/s |
| Ground acceleration | 1100 px/s² |
| Air acceleration | 650 px/s² |
| Ground friction | 1400 px/s² |
| Air drag | 140 px/s² |
| Jump velocity | -360 px/s |
| Gravity | 1000 px/s² |
| Max fall speed | 620 px/s |
| Variable jump cut | multiply vy by 0.45 if released before apex |
| Coyote time | 0.08 s |
| Jump buffer | 0.12 s |
| Max wall climb | Not a climb system; only cling/shimmy/leap transition. |
| Cling shimmy speed | 70 px/s |
| Cling jump impulse | 160 px/s away from surface, 240 px/s upward |
| Safe perch set delay | 0.2 s stable overlap |

### 4.2.4 Collision and fall rules

| Rule | Number |
| --- | ---: |
| Player collision box | 20×14 px |
| Swept collision max step | `|vel| * dt` |
| Normal platform fall failure | None |
| Explicit loss zones | Only `ctx.lossZones` or y > level.height + 64 |
| Lower-area continuation | Allowed if authored platform leads onward. |
| Falling into active hazard | Hazard capture test handles it. |

## 4.3 Tongue system — Tier 1

### 4.3.1 States

| State | Behavior |
| --- | --- |
| `idle` | No attachment. |
| `extending` | Animation toward target; no force yet. |
| `attached` | Rope constraint and optional pull. |
| `slipping` | Weak anchor failing; detaches after 0.12 s. |
| `releasing` | Animation back to mouth; no force. |

### 4.3.2 Grab validation

| Rule | Value |
| --- | --- |
| Max reach | 220 px |
| Target selection | Anchor center within 16 px of pointer ray or pointer within 16 px of anchor center. |
| Line of sight | Segment from mouth to anchor must not intersect `block_tongue=true`. |
| Valid anchor types | `wire`, `hook`, `key`, `latch`, `gate_catch`, `plank`, `wet_rim`, `mossy_peg`. |
| Invalid anchor types | Any hazard, smooth glass, painted siding, dry smooth peg. |
| No valid target | No state change; no punishment. |
| Barrier types | `wall`, `glass`, `mesh` with `block_tongue=true`. |

### 4.3.3 Rope and swing

| Parameter | Value |
| --- | ---: |
| Max length | 220 px |
| Min length | 24 px |
| Extension speed | 1000 px/s |
| Retraction speed | 1000 px/s |
| Radial velocity removal | Remove velocity component along rope when clamped. |
| Tangential damping | 0.99 per frame while attached. |
| Swing input | Air control remains active at 650 px/s². |
| Pull fixed anchor | Shorten at 180 px/s if input within 45° toward anchor. |
| Pull movable object | Drag object toward mouth at max 160 px/s. |

### 4.3.4 Weak anchors

| Parameter | Strong | Weak |
| --- | ---: | ---: |
| Angle limit | 120° | 30° |
| Max grab impulse | unlimited | 180 px/s |
| Slip delay | none | 0.12 s |
| Result | stable attachment | tongue detaches, Mire may fall, no capture |

### 4.3.5 Pulling authored objects

| Object | Pull rule |
| --- | --- |
| Key in latch | Drag along `pullAxis`; after 24 px displacement, key state becomes `loose`. |
| Loose key | Drag toward mouth; can be carried into gate catch. |
| Gate catch | If key center is within 12 px of catch and tongue releases, key state becomes `in_gate`; gate opens. |
| Loose plank | Drag toward mouth up to 180 px unless target slot reached. |
| Bridge slot | If plank center within 12 px of slot, plank state becomes `placed`; it becomes static platform. |
| Nudge | Same drag rules with small displacement; no inventory. |
| Hazard | Cannot be target or altered. |

## 4.4 Hazards and being caught — Tier 1

### 4.4.1 Capture rules

| Rule | Number |
| --- | ---: |
| Capture test | Active hazard hitbox intersects player hitbox, or player center enters bucket/drain active zone. |
| Safe perch immunity | Capture disabled while player center is inside `safe=true` perch. |
| Cling to hazard surface | If `hazard_surface=true` and hazard active, capture. |
| Capture timeout before reset | 0.45 s |
| Lost timeout before reset | 0.45 s |
| Death | None. |
| Lives | None. |

### 4.4.2 Hazard type table

| Hazard | Warning | Behavior | Capture numbers | Capture reason |
| --- | --- | --- | --- | --- |
| `person` | Footstep shadows, clothing motion. | Walks fixed path. | Speed 90–120 px/s, hitbox 36×140, active while moving. | `person` |
| `hand` | Hover shadow, fingers open. | Hovers 1.0 s, closes 0.35 s, holds 0.7 s, retracts 1.3 s. | Circle radius 42 during close/hold. | `hand` |
| `dog` | Bark, low patrol posture. | Patrols 70 px/s; if player within 200 px, chases 150 px/s. | Hitbox 52×36. | `dog` |
| `bucket` | Dark rim, no active warning. | Static. | Capture if player center enters 64×64 bucket interior. | `bucket` |
| `open_drain` | Bubbles/gurgle 0.8 s. | Dormant 3–5 s, gurgle 0.8 s, current 1.2 s, cooldown 1.5 s. | Current zone 48×56 above drain; pull vy += 550 px/s²; capture after center reaches drain or 0.5 s in zone. | `drain` |
| `sprinkler` | Click, arc starts. | Idle 3.0 s, sweep 1.2 s, off 1.8 s. | Arc radius 210 px, thickness 16 px, capture on active arc. | `sprinkler` |
| `lawnmower` | Engine drone louder within 180 px. | Moves fixed path, pauses 1.2 s at endpoints. | Speed 120–170 px/s, hitbox 80×40. | `mower` |
| `traffic` | Tire sound, lane motion. | Cars spawn every 2.5–4.5 s, move across. | Speed 220–320 px/s, hitbox 110×48. | `traffic` |
| `cat` | Crouches, eyes fix, body wiggle. | Crouch 1.2 s, pounce 0.5 s toward player position at crouch start, recover 1.7 s. | Pounce speed 320 px/s, hitbox 36×28. | `cat` |

## 4.5 Crossing system — Tier 1

### 4.5.1 Start and end

| Rule | Value |
| --- | ---: |
| Start perch | `safe=true`, `checkpoint=true`, `end=false`, order 0. |
| End perch | `safe=true`, `checkpoint=false` or true, `end=true`, order 1000. |
| Completion test | Player center inside end perch and stable for 0.2 s. |
| Completion result | `game.crossingIndex += 1`; load next crossing. |
| Final result | Crossing 12 completion sets `game.gameComplete=true` and shows game complete screen. |

### 4.5.2 Reset and checkpointing

| Rule | Value |
| --- | ---: |
| Initial checkpoint | Start perch. |
| Intermediate checkpoint | Sets `game.lastSafePerchId` and resets future objects only. |
| Reset scope | Restore player, tongue, camera, hazards, and objects with `order >= checkpoint.order`. |
| Start reset scope | Restore all crossing records. |
| Reset animation | 0.45 s fade/splash. |
| Puzzle state after reset | Keys return to latches, gates close, planks snap back, opened states reverse. |
| Cross-crossing state | None. |

## 4.6 Keys, latches, gate catches — Tier 2

| Rule | Number |
| --- | ---: |
| Key visual size | 18×10 px |
| Key tongue anchor | Yes |
| Key states | `in_latch`, `loose`, `in_gate` |
| Latch extraction displacement | 24 px along `pullAxis` |
| Gate catch insertion radius | 12 px |
| Insertion hold time | 0.2 s while key center inside catch and tongue released |
| Gate closed | Solid platform |
| Gate open | Passable; swing animation 0.35 s |
| Reset | Key returns to initial state/position; gate closes. |
| Inventory | None. Keys are world objects. |

## 4.7 Loose planks — Tier 2

| Rule | Number |
| --- | ---: |
| Plank small size | 96×10 px |
| Plank large size | 140×12 px |
| Tongue anchor | Yes |
| Drag speed | 160 px/s |
| Max free displacement | 180 px |
| Bridge slot snap radius | 12 px |
| Placed plank | Static platform |
| Temporary bridge | Allowed only if authored in a bridge slot. |
| Nudge | Small displacement using same drag rules. |
| Reset | Plank returns to `resting` and initial position. |

## 4.8 Intermediate safe perches — Tier 2

| Type | Appearance | Placement rule |
| --- | --- | --- |
| `rain_trap` | Wet gutter catch basin with visible water. | After a dangerous vertical drain section. |
| `damp_pot` | Wet flower pot interior, hidden under overhang. | After a long exposed hazard route. |
| `planter_underside` | Shaded underside of planter, wet, hazards cannot reach. | Before a final gauntlet. |
| Common rules | `safe=true`, `checkpoint=true`, `end=false`, visible wet, not ordinary ledge. | Exactly 3 total. |
| Checkpoint effect | Sets last safe perch. | Reset starts there. |
| Reset effect | Reset all records with `order >= perch.order`. | Earlier route state is not used again. |

## 4.9 Progression and difficulty

### 4.9.1 Difficulty levers

| Lever | Implementation |
| --- | --- |
| Exposure | Fewer safe ledges, more hazard overlap. |
| Timing | Longer hazard cycles and faster schedules. |
| Tongue precision | Weak anchors, angle limits, narrow anchor lines. |
| Object dependency | Keys and planks required for route. |
| Verticality | More gutters, drains, rooftops. |
| Checkpoint scarcity | Rare intermediates only after hard sections. |

### 4.9.2 Full crossing roster

| ID | Name | Tier | World size | Start/end | Hazards | Tongue anchors | Keys/latches/gates/planks | Intermediate | Design intent |
| --- | --- | ---: | --- | --- | --- | ---: | --- | --- | --- |
| C1 | Wet Stone Path | 1 | 1200×540 | Start left, end right | 0 | 0 | 0 | 0 | Teach run, leap, cling. |
| C2 | Clothesline and Fence | 1 | 1600×720 | Start left, end right | 1 lawnmower | 4 | 0 | 0 | Teach tongue grab/swing and fixed pull. |
| C3 | Shed and Drain | 1 | 1800×900 | Start left, end right | 1 lawnmower, 2 open drains, 1 bucket | 5 | 0 | 0 | Teach capture/reset, drain warning, bucket trap. |
| C4 | Sprinkler Yard | 1 | 1800×900 | Start left, end right | 2 sprinklers, 1 hand | 5 | 0 | 0 | Teach timed arcs and hand close. |
| C5 | Gutter Rain Trap | 2 | 1800×1080 | Start left, end right | 1 open drain, 1 cat | 6 | 0 | 1 rain_trap | Teach intermediate checkpoint and vertical hazards. |
| C6 | Fence Cat | 2 | 2000×900 | Start left, end right | 1 cat, 1 hand, 1 person | 6 | 0 | 0 | Teach cat warning and person/hand routes. |
| C7 | Backyard Hand | 2 | 2000×900 | Start left, end right | 1 person, 1 hand, 1 dog, 1 bucket | 6 | 0 | 0 | Teach herding into bucket. |
| C8 | Street Edge | 2 | 2200×900 | Start left, end right | 3 traffic, 1 dog, 1 bucket | 7 | 0 | 0 | Teach exposure and traffic timing. |
| C9 | Latch Gate | 2 | 2000×900 | Start left, end right | 1 cat | 6 | 2 keys, 2 latches, 1 gate catch | 0 | Teach key/latch operation. |
| C10 | Plank Roof | 2 | 2200×1080 | Start left, end right | 1 sprinkler, 1 lawnmower, 1 traffic | 8 | 3 loose planks | 1 damp_pot | Teach plank bridge and checkpoint. |
| C11 | Rooftop Gauntlet | 2 | 2400×1200 | Start left, end right | 1 cat, 1 hand, 1 open drain, 1 sprinkler, 1 lawnmower, 1 traffic | 10 | 1 key, 1 latch, 1 gate catch, 1 plank | 1 planter_underside | Combine all systems. |
| C12 | Hidden Marsh | 2 | 2400×1200 | Start left, end marsh | 1 cat, 1 sprinkler, 1 open drain, 1 lawnmower, 1 traffic | 10 | 0 | 0 | Final crossing; ending is hidden marsh. |

### 4.9.3 Content totals from roster

| Type | Total |
| --- | ---: |
| lawnmowers | 5 |
| open drains | 5 |
| buckets | 3 |
| sprinklers | 5 |
| hands | 4 |
| cats | 5 |
| people | 2 |
| dogs | 2 |
| traffic | 6 |
| keys | 3 |
| latches | 3 |
| gate catches | 2 |
| loose planks | 4 |
| intermediate safe perches | 3 |

## 4.10 Feel

| Principle | Implementation |
| --- | --- |
| No punitive falling | Normal falls continue. |
| No hidden punishment | Bad tongue grabs slip or miss, never trigger capture. |
| Readable hazards | Motion and sound precede danger. |
| Clean repeatable puzzles | Reset restores authored state. |
| Frog-scale vulnerability | Human objects are large; Mire is small but capable. |
| No UI anxiety | No clocks, meters, bars, lives. |
| Puzzle clarity | Safe perches look safe; hazards look dangerous. |
| Tongue mastery | Reach, angle, anchor strength, and release timing matter. |

# 5. CHARACTERS

## 5.1 Mire

| Attribute | Rule |
| --- | --- |
| Silhouette | Small compact frog, low center, wide eyes, mud stains, visible mouth point. |
| Facing | Left/right only. Flip sprite horizontally. |
| Visual size | 24×18 px. |
| Collision size | 20×14 px. |
| Gameplay states | `grounded`, `air`, `clinging`, `captured`, `lost`, `safe`, `resetting`. |

### 5.1.1 Mire animations

| Animation | Trigger | Motion rule |
| --- | --- | --- |
| `idle` | Grounded, no input. | 2-frame breathe, slow blink every 4–7 s. |
| `run` | Grounded horizontal input. | 4-frame leg cycle; body bob 2 px; speed scales visual frame rate. |
| `crouch` | Jump buffer active before launch. | Squash 0.10 s. |
| `leap` | Jump launch. | Stretch 0.08 s, then airborne pose. |
| `air` | Airborne. | Legs tucked, slight rotation toward velocity. |
| `fall` | vy > 0. | Flail 2-frame loop, faster with fall speed. |
| `cling_wall` | Clinging to wall. | Limbs attach, body pressed, no gravity bob. |
| `cling_ceiling` | Clinging to ceiling. | Body hangs, slow 1-frame sway. |
| `shimmy` | Clinging + surface input. | Limbs crawl at 70 px/s. |
| `tongue_extend` | Tongue extending. | Tongue line extends from mouth to target. |
| `tongue_hold` | Attached. | Tongue taut; mouth follows. |
| `tongue_pull` | Pulling fixed anchor. | Mire shortens toward anchor, legs tucked. |
| `object_pull` | Pulling movable object. | Body leans opposite object. |
| `safe_sit` | On safe perch. | Relaxed sit, slow blink, water shimmer nearby. |
| `caught` | Capture. | Short flinch, then hazard-specific capture pose. |
| `lost` | Lost. | Small splash, fade. |
| `reset` | Spawn at perch. | 0.2 s sit-up from wet perch. |

## 5.2 Hazard characters

| Hazard | Silhouette | Animations | Facing/state rules |
| --- | --- | --- | --- |
| Person | Tall ordinary adult shape. | `walk`: 4-frame cycle, footstep shadow. | Faces path direction; active while moving. |
| Hand | Large hand from above/side. | `hover`: fingers open; `close`: fingers close; `retract`: moves away. | Circle capture during close/hold. |
| Dog | Low dog shape. | `patrol`, `alert`, `chase`, `return`. | Chase only when player within 200 px. |
| Cat | Crouched gray cat. | `idle`, `crouch`, `fix`, `pounce`, `recover`. | Pounce line set at crouch start. |
| Lawnmower | Red mower. | `move`, `pause`, `reverse`. | Path fixed; drone warning. |
| Sprinkler | Small head. | `idle`, `sweep_start`, `sweep`, `off`. | Arc starts at authored angle. |
| Traffic | Car silhouette. | `enter`, `move`, `exit`. | Fixed lane. |
| Bucket | Plastic bucket. | Static; capture shake if entered. | Capture if center enters. |
| Drain | Dark circle/grate. | `dormant`, `gurgle`, `current`, `cool`. | Bubbles and swirl communicate state. |

# 6. AUDIO

All sounds are synthesized. No UI meters. Audio is diegetic or low ambient. Volumes are normalized 0.0–1.0.

| Name | Recipe | Plays when |
| --- | --- | --- |
| `music_route` | Low pad: two detuned sine 110 Hz and 165 Hz, lowpass 800 Hz, slow 0.08 Hz LFO, volume 0.08. Optional soft filtered noise rain bed. | During PLAYING, except captured/lost duck to 0.03. |
| `amb_town` | Brown noise lowpass 600 Hz, volume 0.05, occasional distant dog bark. | Ambient during outdoor crossings. |
| `amb_gutter` | Dripping: short sine 900 Hz decay 0.08 s, random 1–4 s intervals. | Gutter/rain-trap levels. |
| `sfx_footstep` | Low thud: sine 120 Hz decay 0.05, noise click. | Person steps. |
| `sfx_hand_hover` | Soft cloth noise, filtered 1800 Hz, loop 0.8 s. | Hand warning. |
| `sfx_hand_close` | Cloth swoosh: noise bandpass 1200 Hz, 0.15 s. | Hand closes. |
| `sfx_dog_bark` | Short square 300 Hz, formant-ish 2000 Hz, 0.12 s. | Dog alert. |
| `sfx_dog_chase` | Paw thuds 100 Hz every 0.22 s. | Dog chase. |
| `sfx_bucket_enter` | Plastic hollow: sine 220 Hz decay 0.12, noise. | Mire enters bucket. |
| `sfx_drain_gurgle` | Low sine 70–140 Hz wobble, noise, 0.8 s. | Drain warning. |
| `sfx_drain_current` | Low rumble: sawtooth 55 Hz, noise lowpass 500 Hz, 1.2 s. | Drain active. |
| `sfx_sprinkler_click` | Square 800 Hz, 0.03 s. | Sprinkler starts sweep. |
| `sfx_sprinkler_sweep` | Filtered noise sweep 1200→2600 Hz, 1.2 s. | Sprinkler active arc. |
| `sfx_mower_idle` | Sawtooth 80 Hz, tremolo 12 Hz, lowpass 900 Hz. | Lawnmower active. |
| `sfx_mower_closer` | Same as mower, volume scales with proximity up to 0.25. | Mower within 180 px. |
| `sfx_traffic_pass` | Noise sweep 400→100 Hz, 0.5 s, Doppler-like pitch. | Car passes. |
| `sfx_cat_crouch` | Low purr: sine 90 Hz, noise, 0.7 s. | Cat crouch. |
| `sfx_cat_pounce` | Short growl: square 180→90 Hz, 0.18 s. | Cat pounces. |
| `sfx_jump` | Sine 300→450 Hz, 0.08 s. | Leap launch. |
| `sfx_land` | Noise burst 20 ms lowpass 800 Hz. | Ground landing. |
| `sfx_cling` | Wet grip: short sine 500 Hz + noise, 0.05 s. | Cling attach. |
| `sfx_shimmy` | Soft wet scrape loop, 70 px/s. | Cling shimmy. |
| `sfx_tongue_extend` | Sine 200→1000 Hz, 0.06 s. | Tongue extends. |
| `sfx_tongue_grab` | Soft click: square 1000 Hz, 0.02 s. | Valid grab. |
| `sfx_tongue_slip` | Wet pop: noise bandpass 900 Hz, sine 300 Hz, 0.08 s. | Weak anchor slips. |
| `sfx_tongue_release` | Soft retract: sine 800→200 Hz, 0.05 s. | Release. |
| `sfx_latch_extract` | Metal scrape: noise bandpass 2400 Hz, 0.12 s. | Key pulled from latch. |
| `sfx_gate_open` | Latch click 1200 Hz + wood thud 160 Hz. | Gate opens. |
| `sfx_gate_close` | Wood thud 150 Hz, 0.08 s. | Reset closes gate. |
| `sfx_plank_drag` | Wood scrape: noise bandpass 1200 Hz, loop. | Plank dragged. |
| `sfx_plank_place` | Wood knock 220 Hz + click. | Plank snaps into slot. |
| `sfx_safe_perch` | Water drop: sine 900 Hz decay 0.12, shimmer. | Checkpoint/end perch reached. |
| `sfx_capture` | Soft thud 120 Hz + small frog squeak square 700 Hz. | Captured. |
| `sfx_lost` | Splash: filtered noise, low sine 180 Hz. | Lost. |
| `sfx_reset` | Splash + sit-up rustle. | Reset spawn. |
| `sfx_game_complete` | Soft frog croak: sine 220→180 Hz, 0.25 s + water shimmer. | Hidden marsh reached. |

# 7. UX

## 7.1 HTML/CSS screens and state machine

| State | Entry | Display | Exit |
| --- | --- | --- | --- |
| `BOOT` | Page load. | Blank canvas, load assets. | `TITLE` |
| `TITLE` | Boot complete. | Title screen: game name, inciting line, controls, start button. | `PLAYING` on start |
| `PLAYING` | Start or next crossing. | Game canvas, brief crossing intro text, no persistent HUD. | `PAUSED`, `CAPTURED`, `LOST`, `CROSSING_COMPLETE`, `GAME_COMPLETE` |
| `PAUSED` | Esc during PLAYING. | Pause menu with resume/restart crossing. | `PLAYING` |
| `CAPTURED` | Hazard capture. | Brief overlay “Caught” only, then reset. | `PLAYING` |
| `LOST` | Loss zone. | Brief overlay “Lost” only, then reset. | `PLAYING` |
| `CROSSING_COMPLETE` | End perch reached. | Brief overlay “Safe perch reached”, then next crossing. | `PLAYING` |
| `GAME_COMPLETE` | Crossing 12 end reached. | Hidden marsh reached; return to title. | `TITLE` |

## 7.2 HUD table

| Element | Record field | When visible |
| --- | --- | --- |
| `#title-screen` | none | TITLE |
| `#start-button` | none | TITLE |
| `#controls` | `input.help` | TITLE, PAUSED |
| `#crossing-intro` | `level.name`, `level.index` | First 1.5 s of PLAYING only |
| `#message` | `game.message` | CAPTURED, LOST, CROSSING_COMPLETE, GAME_COMPLETE |
| `#pause-menu` | `game.state` | PAUSED |
| `#debug` | debug records | Debug mode only |
| No health, lives, timer, clock, meter, bar, pickup counter, upgrade display | n/a | Never |

# 8. DEBUG API

| Function | Returns / effect |
| --- | --- |
| `debug.player()` | `{pos, vel, facing, state, grounded, clinging, lastSafePerchId, captureReason}` |
| `debug.tongue()` | `{state, targetId, anchorPoint, length, maxLength, slipTimer, grabAngleError, grabImpulse}` |
| `debug.hazards()` | Array of hazard states: `{id, type, state, active, warning, hitbox}` |
| `debug.objects()` | Array of object states: `{id, type, state, pos, initialPos, order}` |
| `debug.level()` | `{id, index, width, height, startPerchId, endPerchId, counts}` |
| `debug.crossing()` | `{crossingIndex, lastSafePerchId, state, resetPending}` |
| `debug.perches()` | Array of perch records: `{id, type, safe, end, checkpoint, order}` |
| `debug.input()` | `{move, jump, cling, tongueAim, tongueGrab, pause}` |
| `debug.forceCapture(reason)` | Debug-only: triggers capture with reason. |
| `debug.forceLost()` | Debug-only: triggers lost. |
| `debug.loadCrossing(index)` | Debug-only: loads crossing 1–12. |
| `debug.resetCheckpoint(perchId)` | Debug-only: sets checkpoint and resets beyond. |
| `debug.toggleDebug()` | Enables debug overlay and API. |

# 9. TESTS

## 9.1 Tier 1 tests

| Test | Pass criteria |
| --- | --- |
| `fixed_step_deterministic` | Running same input sequence twice produces same state hash. |
| `run_acceleration` | Holding right reaches 150 px/s within 0.25 s. |
| `run_friction` | Releasing input stops within 0.20 s on flat ground. |
| `leap_height` | Full jump apex height is 60–80 px above takeoff. |
| `leap_variable` | Releasing early reduces height by at least 40%. |
| `coyote_time` | Jump within 0.08 s after leaving ledge succeeds. |
| `jump_buffer` | Jump input within 0.12 s before landing triggers jump on landing. |
| `cling_sticky_only` | Cling succeeds on `sticky=true`, fails on glass/painted siding. |
| `cling_shimmy` | Cling movement along surface stays 70 px/s. |
| `tongue_reach` | Grab fails beyond 220 px. |
| `tongue_line_of_sight` | Grab fails through wall/glass/mesh. |
| `tongue_valid_anchor` | Grab succeeds on wire/key/latch/plank, fails on hazard. |
| `tongue_rope_constraint` | Attached player never exceeds 220 px from fixed anchor. |
| `tongue_pull_fixed` | Pulling toward fixed anchor shortens rope to 24 px min. |
| `weak_anchor_slip` | Weak anchor slips on bad angle/impulse and does not capture. |
| `hazard_capture_mower` | Contact with active mower sets captured. |
| `hazard_capture_drain` | Active drain current captures. |
| `hazard_capture_bucket` | Bucket interior captures. |
| `hazard_capture_sprinkler` | Active arc captures. |
| `hazard_capture_hand` | Closing hand captures. |
| `capture_returns_to_start` | After capture, player spawns at start perch. |
| `normal_fall_not_lost` | Falling onto lower platform does not fail. |
| `loss_zone_fails` | Entering explicit loss zone sets lost. |
| `reset_restores_state` | Mower path, drain schedule, hand state reset. |
| `crossing_complete` | End perch stable overlap advances crossing. |
| `vertical_slice_completion` | Automated input script can complete C1–C4. |

## 9.2 Tier 2 tests

| Test | Pass criteria |
| --- | --- |
| `key_extract_latch` | Pulling key 24 px along axis opens latch/gate. |
| `key_insert_gate` | Key within 12 px of gate catch and released opens gate. |
| `key_not_inventory` | Key remains world object; no inventory record. |
| `plank_drag` | Attached plank can be dragged up to 180 px or to slot. |
| `plank_bridge` | Placed plank becomes solid static platform. |
| `plank_reset` | Plank returns to initial position. |
| `intermediate_safe` | Intermediate perch disables capture while inside. |
| `intermediate_checkpoint` | Reaching intermediate sets last safe perch. |
| `intermediate_reset_scope` | Reset restores only objects with order >= checkpoint. |
| `full_hazard_roster` | All 9 hazard types appear and capture correctly. |
| `full_route_load` | C1–C12 load without missing records. |
| `final_crossing_complete` | C12 end marsh sets game complete. |
| `no_permanent_changes` | Completing crossing then reloading it returns all puzzle state to initial. |
| `no_ui_meters` | No DOM elements for health, lives, timer, clock, meter, bar, collectibles. |

# 10. BUILD ORDER

1. Create canvas, HTML screens, CSS, fixed-step loop, debug toggle.
2. Implement input state and deterministic RNG.
3. Implement camera follow and level clamping.
4. Implement player AABB, run, gravity, leap.
5. Implement platform collision and normal fall behavior.
6. Implement safe perch records, start perch spawn, end perch completion.
7. Implement loss zones and reset flow.
8. Implement cling on sticky surfaces and non-cling surfaces.
9. Implement tongue aim, extension, valid anchors, line of sight, barriers.
10. Implement rope constraint and fixed-anchor pull.
11. Implement generic weak-anchor slip.
12. Implement hazard framework and first hazards: lawnmower, open drain, bucket, sprinkler, hand.
13. Implement capture/lost return to last safe perch.
14. Build C1–C4 and polish core visual/audio for the vertical slice.
15. Add key/latch/gate objects and reset logic.
16. Add loose planks and bridge slots.
17. Add intermediate safe perches and checkpoint reset scope.
18. Add remaining hazards: person, dog, traffic, cat.
19. Build C5–C12.
20. Add full audio table and visual polish.
21. Add debug API and tests.
22. Run Tier 1 tests, then Tier 2 tests.

# 11. DEFINITION OF DONE

## Tier 1: Core playable crossing game

High-level done: A player can run, leap, cling, and use the tongue to complete a short linear route, get caught by hazards, lose in loss zones, and reset to the last safe perch.

- [ ] Fixed 60 Hz loop and deterministic input.
- [ ] Player can run at 150 px/s with specified accel/friction.
- [ ] Player can leap with specified jump velocity, gravity, variable jump, coyote, buffer.
- [ ] Player can cling only to sticky surfaces and shimmy at 70 px/s.
- [ ] Tongue max reach 220 px, line-of-sight blockers, valid anchor list.
- [ ] Tongue rope constraint and fixed-anchor pull work.
- [ ] Weak anchors slip without capture punishment.
- [ ] Hazard capture returns Mire to last safe perch.
- [ ] Normal falling does not fail unless in loss zone.
- [ ] Start perch and end perch work.
- [ ] Crossing reset restores authored state.
- [ ] C1–C4 are playable and completable.
- [ ] Core visual style and audio play in Tier 1.
- [ ] No HUD meters, bars, clocks, lives, health, upgrades, collectibles.
- [ ] Tier 1 tests pass.

## Tier 2: Supporting mechanics and complete route home

High-level done: The full 12-crossing route home exists and can be completed, including keys, loose planks, intermediate safe perches, and all required hazard types.

- [ ] 12 crossings load in order.
- [ ] Keys can be pulled from latches.
- [ ] Keys can be inserted into gate catches.
- [ ] Gates open and close.
- [ ] Loose planks can be dragged and placed as bridges.
- [ ] Intermediate safe perches set checkpoints.
- [ ] Reset scope respects checkpoint order.
- [ ] All hazard types from 4.4 are implemented and capture correctly.
- [ ] C5–C12 are playable and completable.
- [ ] Final crossing reaches hidden marsh and ends the game.
- [ ] No permanent puzzle state persists across crossings.
- [ ] Tier 2 tests pass.

## Tier 3: None

- [ ] No extra mechanics requested.
- [ ] Optional debug/accessibility improvements only.

# A. SANITY

| Check | Result |
| --- | --- |
| Does the design implement “a platformer where you play as a frog”? | Yes. Mire is the player; side-on 2D real-time platforming. |
| Are the core mechanics exactly run, leap, cling, tongue, hazards, crossing? | Yes. Tier 1 implements those systems and no extra core gameplay systems. |
| Are supporting mechanics exactly keys, loose planks, intermediate safe perches? | Yes. Tier 2 implements only those mechanics. |
| Are extra mechanics none? | Yes. Tier 3 has no gameplay mechanics. |
| Are all content parts present? | Yes. Mire, hidden marsh, linear route, perches, spaces, wires, keys, latches, gate catches, people, hand, dog, bucket, drains, drain current, sprinklers, lawnmowers, traffic, cat, damp pot, rain trap, shaded planter, sticky surfaces, non-sticky surfaces, barriers, weak anchors. |
| Are all listed hazards present and numbered? | Yes: people 2, hands 4, dogs 2, buckets 3, open drains 5, sprinklers 5, lawnmowers 5, traffic 6, cats 5. |
| Are there no collectibles, health, lives, upgrades, hub, permanent puzzle changes? | Yes. Roster totals and rules explicitly set them to zero; crossing reset prevents permanent state. |
| Are ordinary ledges safe perches? | No. Only records with `safe=true` are safe. |
| Can Mire climb smooth glass/painted siding? | No. `sticky=false`. |
| Can tongue alter hazards? | No. Hazards are not valid anchors. |
| Are tongue reach, line of sight, barriers, and anchor validity enforced? | Yes. 220 px max, raycast blockers, valid anchor list, weak anchor slip. |
| Is bad tongue grab non-punitive? | Yes. Slip detaches without capture. |
| Is being caught not death? | Yes. Capture returns to last safe perch. |
| Is falling off normal ledge not failure? | Yes. Only explicit loss zones or active hazards fail. |
| Does reset restore puzzle state beyond last safe perch? | Yes. Object/hazard `order` and checkpoint order control reset scope. |
| Are intermediate safe perches rare and deliberate? | Yes. Exactly 3 authored. |
| Is the view side-on 2D with low camera close to Mire? | Yes. Camera target keeps Mire above center and ground low. |
| Is time real-time? | Yes. Fixed 60 Hz real-time simulation. |
| Are there UI meters, bars, clocks, or timers? | No. No persistent HUD; internal durations are simulation only. |
| Are visuals and audio present from Tier 1? | Yes. Tier 1 includes art style, palette, animations, sound effects, and ambient route sound. |
| Are numbers concrete? | Yes. Physics, tongue, hazards, level sizes, counts, and tests include numbers. |
| Did I add unrequested systems? | Checked: no combat, no health, no lives, no upgrades, no collectibles, no double jump, no stamina, no cooldowns, no inventory. Camera/UI/audio/debug are implementation support, not gameplay systems. |