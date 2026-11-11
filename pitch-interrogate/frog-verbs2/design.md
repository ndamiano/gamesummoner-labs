# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Browser game: a platformer where the player plays as a frog | `4.1 Player movement`, `5. CHARACTERS`, `7. UX` |
| Side-on 2D platformer view; camera follows the frog and shows shadowed cover, open lit spaces, watcher attention, and the Moon Pool’s draining state | `3. VISUAL SPEC`, `4.5 Shadow, cover, and being seen`, `4.6 Watchers and attention`, `4.8 Moon Pool goal and closure`, `2.3 Camera module` |
| Real-time | `1.2 Important conventions`, `4.7 Time cycle and night changes` |
| Frog wakes on a lily in a rain barrel; starting place and platform; leaving the barrel starts the attempt | `4.2 Attempt start and reset`, `4.4 Fixed dangers`, `4.8 Moon Pool goal and closure`, `9. TESTS` |
| One crossing is the whole game; no next crossing | `0.2 Decisions`, `4.2 Attempt start and reset`, `4.8 Moon Pool goal and closure`, `7. UX` |
| If the frog is taken, attempt resets to the start of the same crossing | `4.2 Attempt start and reset`, `4.4 Fixed dangers`, `4.6 Watchers and attention`, `11. DEFINITION OF DONE` |
| If the frog enters the Moon Pool before it closes, the game records whether rain lily bulbs were completed and returns to the start of the same crossing | `4.8 Moon Pool goal and closure`, `4.9 Rain lily bulbs and set completion`, `7. UX`, `11. DEFINITION OF DONE` |
| It becomes harder as the night moves: shadows shrink, lamps warm, watchers change where they look, drains and fans change state, hidden places become reachable or deadly, Moon Pool drains until closed | `4.4 Fixed dangers`, `4.6 Watchers and attention`, `4.7 Time cycle and night changes`, `4.12 Hidden places becoming reachable or deadly`, `4.8 Moon Pool goal and closure` |
| Tone: small in a place that notices you; wet and loud air; night changes around the player; every crossing is a decision about whether to be seen | `3. VISUAL SPEC`, `4.12 Hidden places becoming reachable or deadly`, `5. CHARACTERS`, `6. AUDIO`, `7. UX` |
| Look and sound: wet rooftop night at close range; rain-soaked surfaces, dripping water, drain steam, distant city hum, warm lamp glow, glass, shadowed ledges, quiet stretches broken by watcher movement | `3. VISUAL SPEC`, `6. AUDIO` |
| Core mechanics exactly: platforming and route viability; shadow, cover, and being seen; watchers and attention; fixed dangers; time cycle and night changes; attempt, failure, and reset; Moon Pool goal and closure; rain lily bulbs and set completion | `4. GAMEPLAY SPEC`, `9. TESTS`, `11. DEFINITION OF DONE` |
| Supporting mechanics exactly: loose tile disturbance; cat appearance event; hidden places becoming reachable or deadly | `4.10 Loose tile disturbance`, `4.11 Cat appearance event`, `4.12 Hidden places becoming reachable or deadly` |
| Extra mechanics: none | `0.2 Decisions`, `0.3 Tiers`, `11. DEFINITION OF DONE` |
| Content exactly: rain barrels, gutters, open gutters, windowsill, wire, awnings, greenhouse glass, greenhouse hatch, pool grate, heron, cat, drains, lamps, broken glass, fans, wet ledges, shadow, yard, watchers, night, first light | `4. GAMEPLAY SPEC` rosters, `0.2 Decisions` |
| Left out: not road-crossing, not combat, not story with named characters, not survival, not roguelike, not vehicles, not building/fighting through the world; no next crossing, no health, no armor, no damage state, no permanent progression beyond recording bulbs, no random cat spawn, no separate greenhouse-glass hazard except the Moon Pool closing hatch | `0.2 Decisions`, `2. CONTRACTS`, `11. DEFINITION OF DONE`, `A. SANITY` |

## 0.2 Decisions

| Decision | Source | Ruling | Why |
| --- | --- | --- | --- |
| Game is a platformer where you play as a frog | User request | Keep. The frog is a small tree frog; platforming is the only verb. | Direct request. |
| Side-on 2D platformer view; camera follows | Game decisions | Keep. Canvas viewport is `960x540`, world is `3200x900`, camera follows with deadzone and clamping. | Lets the player see cover, light, attention, and pool state. |
| Real-time | Game decisions | Keep. Fixed-step real-time simulation at 60 updates/second. | Gives timing pressure and watchable watcher cycles. |
| One crossing is the whole game | Game decisions | Keep. After completion or failure, return to the same start. No level select, no next crossing, no unlocks. | Matches the final decision. |
| Failure resets to start of same crossing | Game decisions | Keep. Failure is instant reset after 1.0 second death animation. | No damage state, no lives, no meta progression. |
| Moon Pool drains and closes at first light | Game decisions | Keep. Pool water is a continuous value from `1.0` to `0.0` over 120 seconds. Closing at `0.0` fails the attempt immediately. | Creates a hard, readable timer without health. |
| Rain lily bulbs are a set; they do not change the frog or open anything | Game decisions | Keep. There are exactly 5 bulbs. Completion is a boolean shown only on success. | Set completion is optional mastery, not progression. |
| If attempt fails, bulbs are lost | Game decisions | Keep. Bulb collection state resets on every reset. | Preserves one-attempt risk. |
| Watchers notice when the frog is in sightline and not hidden | Game decisions | Keep. Visibility is cone/attention-rect plus occlusion. If visible, watcher enters `alert`; if frog reaches shadow before `1.0` seconds, watcher backs off. | Makes shadow and timing the core safety rule. |
| Watcher turns and covers next surface with attention | Game decisions | Keep. When a watcher sees the frog, it adds a temporary `attentionRect` to the next surface in its `surfacePath` for 2.0 seconds. | Makes a route become unsafe after being spotted. |
| If the frog cannot reach shadow before attention reaches its surface, watcher takes the frog | Game decisions | Keep. `alertDuration = 1.0` seconds. If not hidden for the full duration, the frog is taken. | Gives a clear, testable escape window. |
| Fixed dangers are drains, lamps, broken glass, fans, open gutters | Game decisions | Keep exactly these types. No other instant dangers are added. | The content list is final. |
| Fixed dangers take the frog; no damage state | Game decisions | Keep. Any active fixed-danger overlap ends the attempt immediately. | No health, no recovery. |
| Drains and fans may change state | Game decisions | Keep. Each has deterministic active intervals listed in `4.4`. | Time cycle creates difficulty without randomness. |
| Lamps when cold/dark are safe nearby but fixture still dangerous if touched; when warm/lit, fixture and light make surfaces deadly or watched | Game decisions | Keep. Lamp fixture is always instant kill. Lamp light is a watcher attention with the same `alertDuration`. | Separates physical danger from being seen. |
| Open gutters are gaps and fixed dangers | Game decisions | Keep. Falling into an open-gutter rectangle or below `y >= 900` ends the attempt. | Gaps are not just platforming failures; they are fixed dangers. |
| Time cycle begins when frog wakes and crossing starts | Game decisions | Keep. Night timer starts only when `attemptActive` becomes true after leaving the rain barrel. | The start is a safe observation space. |
| Shadows shrink as night moves | Game decisions | Keep. Lamp lights expand from length 0 to fixed lengths during warming phases. This removes dark safe space near hidden places and some ledges. | Shadows are represented by absence of attention/light. |
| Lamps warm | Game decisions | Keep. Two lamps warm on deterministic schedules. | Adds night-changing danger without new systems. |
| Watchers change where they look | Game decisions | Keep. Heron has a deterministic patrol; cat has a deterministic watch/turn cycle; lamp lights expand. | Creates changing routes and timing windows. |
| Hidden places become reachable or deadly | Game decisions | Keep. Hidden places are optional ledges/bulbs. They are reachable only while no active attention or fixed danger covers them. They become deadly when schedules activate attention or fixed danger. | This is a ruling rule for optional routes. |
| Attempt, failure, reset | Game decisions | Keep. Same layout, night reset, bulb loss, tile reset, cat reset. | No permanent progression. |
| Moon Pool goal and closure | Game decisions | Keep. Success only if pool water `> 0` and frog overlaps water. If water reaches `0`, attempt fails. | Final goal is readable and time-limited. |
| Rain lily bulbs and set completion | Game decisions | Keep. 5 bulbs total. Success screen shows only whether the set was completed. No persistent unlocks. | Optional challenge inside one crossing. |
| Loose tile disturbance | Game decisions | Keep. One loose tile contains bulb `BULB_1`. Taking it drops the tile for the rest of the attempt. | Closes a short route and creates a meaningful optional risk. |
| Cat appearance event | Game decisions | Keep. Cat appears only after `BULB_1` is collected and the frog reaches `W1`. No random cat. | Fixed event tied to bulb-taking risk. |
| No extra mechanics | Game decisions | Keep. Tier 3 contains no new gameplay systems. | Extra mechanics are explicitly none. |
| World size | My decision | `3200x900` px world. | Long enough for one crossing, small enough to test. |
| Viewport | My decision | `960x540` px. | Standard browser 16:9 view. |
| Units | My decision | Pixels, seconds, degrees, fractions. | Simple for browser physics and tests. |
| Input | My decision | Keyboard only: Left/A, Right/D, Space/W/Up jump. No pause, no restart, no context action. | Input is only platforming; failure auto-resets. |
| Player size | My decision | `10x10` px AABB. | Small enough for narrow ledges and gutters. |
| Movement numbers | My decision | `maxSpeed=170`, `accel=1400`, `gravity=1500`, `jumpVel=520`, `coyote=0.08`, `jumpBuffer=0.08`, `maxFall=720`. | Gives about 90 px jump height and 118 px horizontal jump, matching platform spacing. |
| Number of bulbs | My decision | Exactly 5. | A set is readable and testable without adding a huge level. |
| First bulb | My decision | `BULB_1` under the loose tile is the cat trigger bulb. Other bulbs do not trigger the cat. | Matches the loose-tile and cat decision as one linked event. |
| Level route | My decision | One continuous left-to-right crossing from `BARREL` to `MOON_POOL`, with an upper wire/awning route and a lower wet-ledge route. | Gives route choice and watcher/lamp pressure. |
| Visibility method | My decision | A watcher or lamp sees the frog if the frog center is inside its cone or temporary attention rectangle and the ray from eye/light origin to the frog does not intersect an occluding solid surface. | Implements shadow, cover, and being seen concretely. |
| Occlusion | My decision | Solid platforms and greenhouse glass frame occlude rays. One-way thin ledges do not. | Uses existing content as cover without adding new systems. |
| Attention state machine | My decision | `calm`, `alert`, `cooldown`. `alertDuration=1.0`, `hideGrace=0.35`, `cooldown=1.2`, `coverNextDuration=2.0`. | Gives one clean rule for all watchers and lamp attention. |
| Heron behavior | My decision | Stationary watcher on the yard ledge with deterministic cone patrol. | Heron is a fixed watcher, not an enemy or combatant. |
| Cat behavior | My decision | Stationary awning watcher with deterministic 3.5s watch, 2.5s turn cycle after trigger. | Cat is a fixed event and a timing obstacle. |
| Lamp behavior | My decision | Lamp fixture always instant kill; lamp light is attention with same alert rule. | Satisfies both fixed danger and watcher attention. |
| Drain/fan behavior | My decision | Active rectangles instant kill; inactive rectangles passable. Deterministic intervals. | Fixed dangers change state but do not become entities. |
| Moon Pool success method | My decision | Success if `poolWater > 0` and frog center overlaps water rectangle. | “Entering before it closes” is literal. |
| Completion record | My decision | Session-only boolean `lastCompletion.bulbsComplete`. No localStorage. | “No permanent progression beyond recording whether bulbs were completed.” |
| Failure handling | My decision | No manual restart. Auto-reset after death animation. | The game returns to start automatically by decision. |
| UI | My decision | HTML/CSS overlays for HUD and screens; game world drawn on canvas. | Required UX is HTML/CSS. |
| Audio | My decision | Synthesized via audio API only; no samples. | Builder has audio API. |

## 0.3 Tiers

Priority list. Tier 1 is the complete core game. Tier 2 is the complete supporting layer. Tier 3 is not a mechanic layer; it is optional tuning only and must not add systems.

| Tier | Segment | Must include | Notes |
| --- | --- | --- | --- |
| 1 | Core platforming and attempt | Player movement, jump, landing, collision, camera, attempt start, attempt reset, open gutter deaths | This is the playable body of the game. |
| 1 | Core fixed dangers | Drains, lamps fixture, broken glass, fans, open gutters | Instant danger system with deterministic schedules for drains/fans. |
| 1 | Core shadow and attention | Visibility, occlusion, shadow safety, watcher alert, take, lamp attention | Core emotional rule: do not be seen. |
| 1 | Core watchers | Heron with deterministic patrol and attention rectangles | No cat until Tier 2. |
| 1 | Core time cycle and Moon Pool | Night timer, pool drain, pool close, first light, success/fail | The whole run must finish. |
| 1 | Core bulbs and completion record | 5 bulbs, collect/reset, completion boolean, completion screen | Core optional set. |
| 2 | Loose tile disturbance | `TILE_1`, `BULB_1`, tile falls, route closes, reset restores | Small complete addition. |
| 2 | Cat appearance event | Trigger after `BULB_1` and `W1`, cat watcher on `A1`, deterministic cycle, reset removes | Small complete addition. |
| 2 | Hidden places becoming reachable or deadly | Optional ledges and bulbs that become reachable/deadly by schedules | Uses existing systems only. |
| 3 | Optional tuning only | Timing, cone length, lamp schedules, bulb placement risk | No new records, systems, inputs, hazards, watchers, or content. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Name | Value | Meaning |
| --- | ---: | --- |
| `VIEWPORT_W` | 960 | Canvas CSS and drawing width in px. |
| `VIEWPORT_H` | 540 | Canvas CSS and drawing height in px. |
| `WORLD_W` | 3200 | World width in px. |
| `WORLD_H` | 900 | World height in px. |
| Axis X | right positive | Horizontal movement. |
| Axis Y | down positive | Gravity and falling. |
| `PLAYER_W` | 10 | Player collision width. |
| `PLAYER_H` | 10 | Player collision height. |
| `TILE` | 16 | Visual grid unit only; gameplay uses rectangles. |
| `FPS` | 60 | Fixed simulation step. |
| `DT` | 1/60 | Fixed timestep in seconds. |
| Angle unit | degrees | 0 right, 90 down, 180 left, 270 up. |
| `NIGHT_DURATION` | 120 | Seconds from attempt start to first light. |
| `POOL_WATER_START` | 1.0 | Moon Pool water fraction at attempt start. |
| `POOL_WATER_CLOSED` | 0.0 | Water fraction that closes the pool. |
| `ALERT_DURATION` | 1.0 | Seconds a visible frog may remain visible before being taken. |
| `HIDE_GRACE` | 0.35 | Seconds hidden before watcher backs off. |
| `WATCHER_COOLDOWN` | 1.2 | Seconds after escape before watcher resumes normal attention. |
| `COVER_NEXT_DURATION` | 2.0 | Seconds a watcher covers the next surface after spotting. |
| `BULB_RADIUS` | 7 | Collection radius for bulbs. |
| `RANGE_EPS` | 0.001 | Floating comparison epsilon. |

## 1.2 Important conventions

| Rule | Why |
| --- | --- |
| Use one global context object `G`. No hidden module state for gameplay. | Tests and debug need deterministic access. |
| Use fixed timestep `DT = 1/60` with accumulator. Render interpolation is optional only. | Platforming and timer tests need determinism. |
| No `Math.random()` in gameplay. All schedules, patrols, and events are deterministic. | The cat is a fixed event; reset must be repeatable. |
| All gameplay objects use stable string IDs. | Tests and debug can inspect state directly. |
| All rectangles are `{x,y,w,h}` with top-left origin. | Collision and visibility are simple. |
| All angles are degrees. | Spec numbers are readable. |
| A failure is terminal for the attempt. No health, no damage, no partial state. | Matches “no damage state”. |
| Reset restores all attempt state: player, bulbs, tile, cat, watchers, hazards, pool, night timer. | Matches “same crossing, night reset”. |
| Completion does not advance to a new crossing. It shows the bulb-set result and returns to the same start. | Matches “no next crossing”. |
| UI is HTML/CSS. The world canvas is the only canvas. | UX requirement. |
| Audio is synthesized through the provided audio API. No loaded sample assets. | Builder has audio API. |
| No pause, no restart button, no context action, no pause menu. | No extra systems. |
| One-way platforms only collide from above when previous bottom is above the platform top and vertical velocity is downward. | Thin ledges and wires should not block upward movement. |
| Solid platforms collide on all sides. | Gutters, windowsills, awnings, ledges, barrel, pool walls. |
| Occlusion rays ignore the platform the player is standing on. | Standing on a surface must not hide the player from a watcher above that same surface. |
| Lamp light is attention, not instant kill, except the lamp fixture rectangle. | Separates being seen from touching a fixed danger. |
| Open gutter death includes any overlap with an open-gutter rectangle or `player.y >= WORLD_H`. | Falls through gaps are fixed dangers. |

# 2. CONTRACTS

## 2.1 Module layout

```text
src/
  main.js
  engine/
    loop.js
    input.js
    camera.js
    collision.js
    render.js
  gameplay/
    context.js
    player.js
    level.js
    platform.js
    hazards.js
    watchers.js
    night.js
    pool.js
    bulbs.js
    tile.js
    cat.js
    reset.js
  ui/
    screens.js
    hud.js
  audio/
    audio.js
    recipes.js
  debug/
    api.js
  tests/
    tier1.js
    tier2.js
    integration.js
index.html
styles.css
```

## 2.2 Global context

The global context is the single source of truth. Every field below must exist.

```ts
const G = {
  mode: "boot" | "wake" | "playing" | "failed" | "completed",
  time: number,              // total real seconds since boot
  frame: number,
  modeTimer: number,         // seconds in current mode, for overlays/animations

  attempt: {
    active: boolean,
    failReason: "none" | "open_gutter" | "drain" | "lamp_fixture" | "broken_glass" | "fan" | "watcher" | "pool_closed",
    failTime: number,
    completionTime: number
  },

  night: {
    time: number,            // seconds since attempt start
    duration: 120,
    firstLight: boolean,
    shadowShrink: number     // 0..1, visual and lamp expansion driver
  },

  pool: {
    water: number,           // 1.0 to 0.0
    closed: boolean,
    success: boolean,
    basin: { x: 2780, y: 620, w: 200, h: 180 },
    waterTop: number,        // computed
    grate: { x: 2780, y: 790, w: 200, h: 10 },
    hatch: { x: 2900, y: 560, w: 80, h: 120, closed: boolean }
  },

  completion: {
    bulbsComplete: boolean,
    collectedCount: number
  },

  player: {
    x: number,
    y: number,
    w: 10,
    h: 10,
    vx: number,
    vy: number,
    facing: -1 | 1,
    grounded: boolean,
    groundId: string | null,
    coyote: number,
    jumpBuffer: number,
    jumpHeld: boolean,
    alive: boolean,
    animation: "idle" | "wake" | "move" | "jump" | "fall" | "land" | "take"
  },

  input: {
    left: boolean,
    right: boolean,
    jump: boolean,
    jumpPressed: boolean,
    axis: number
  },

  camera: {
    x: number,
    y: number,
    shake: number
  },

  level: {
    platforms: Platform[],
    occluders: Rectangle[],
    hazards: Hazard[],
    watchers: Watcher[],
    bulbs: Bulb[],
    tile: Tile,
    greenhouseGlass: Rectangle,
    trigger: {
      startExit: Rectangle,
      windowsill: Rectangle
    }
  },

  tile: {
    id: "TILE_1",
    present: boolean,
    falling: boolean,
    fallTime: number,
    rect: Rectangle,
    bulbId: "BULB_1"
  },

  cat: {
    active: boolean,
    x: number,
    y: number,
    state: "absent" | "appearing" | "watching" | "turned" | "alert" | "taking",
    timer: number,
    cycleTimer: number,
    facing: number,
    alertT: number,
    hiddenT: number,
    cooldown: number,
    attentionRect: Rectangle | null
  },

  watchers: Watcher[],
  hazards: Hazard[],
  bulbs: Bulb[],

  ui: {
    hudVisible: boolean,
    bulbsText: string,
    nightText: string,
    poolText: string,
    alertVisible: boolean,
    endText: string
  },

  audio: {
    ambientStarted: boolean,
    currentLoops: string[],
    lastPlayed: Record<string, number>
  }
};
```

Required nested record shapes:

```ts
type Rectangle = { x: number; y: number; w: number; h: number };

type Platform = {
  id: string;
  type: "solid" | "one-way" | "occluder";
  rect: Rectangle;
  top: number;
  material: "barrel" | "gutter" | "windowsill" | "wire" | "awning" | "wet_ledge" | "greenhouse" | "pool_wall";
  canFall: boolean;
  present: boolean;
};

type Hazard = {
  id: string;
  type: "open_gutter" | "drain" | "lamp_fixture" | "broken_glass" | "fan";
  rect: Rectangle;
  activeAlways: boolean;
  activeIntervals: Array<[number, number]>;
  active: boolean;
  kill: boolean;
};

type Watcher = {
  id: string;
  type: "heron" | "cat" | "lamp_light";
  active: boolean;
  x: number;
  y: number;
  baseAngle: number;
  halfAngle: number;
  coneLength: number;
  state: "calm" | "alert" | "cooldown" | "off";
  alertT: number;
  hiddenT: number;
  cooldown: number;
  surfacePath: string[];
  nextSurfaceId: string | null;
  attentionRect: Rectangle | null;
  attentionT: number;
  cycleTimer: number;
  patrolPhase: number;
};

type Bulb = {
  id: string;
  x: number;
  y: number;
  r: number;
  collected: boolean;
  requiredForCat: boolean;
  hiddenPlace: boolean;
};
```

## 2.3 Module specifics

| Module | Required exports/functions | Contract |
| --- | --- | --- |
| `engine/loop.js` | `startLoop()`, `step(dt)`, `render()` | Runs fixed `DT=1/60`; calls update then render; never mutates gameplay outside `G`. |
| `engine/input.js` | `pollInput()`, `axis()`, `jumpPressed()`, `jumpHeld()` | Returns current input values. No game logic. |
| `engine/camera.js` | `followPlayer(dt)`, `clampCamera()` | Camera target is player center with deadzone `x=60,y=40`; lerp rate 8/s; clamp to world. |
| `engine/collision.js` | `resolvePlayer(dt)`, `rectOverlap(a,b)`, `rayIntersectsRect(a,b,rect)`, `isOccluded(from,to,ignoreIds)` | Implements solid and one-way collision. |
| `gameplay/player.js` | `spawnPlayer()`, `updatePlayer(dt)`, `takePlayer(reason)`, `playerRect()` | Player state only; no direct world mutation except calling reset/take. |
| `gameplay/level.js` | `buildLevel()`, `resetLevel()`, `resetAttempt()` | Creates all platforms, hazards, watchers, bulbs, tile, triggers, occluders. Reset restores initial state. |
| `gameplay/platform.js` | `getPlatform(id)`, `setPlatformPresent(id,present)`, `isSurfaceWatched(surfaceId)` | Route viability: a surface is unusable if absent, watched, or covered by active fixed danger. |
| `gameplay/hazards.js` | `updateHazards(dt)`, `isActive(hazard)`, `checkHazardCollisions()`, `killReasonFor(hazard)` | Drains/fans/open gutters/broken glass/lamp fixture kill on active overlap. |
| `gameplay/watchers.js` | `updateWatchers(dt)`, `isPlayerVisible(watcher)`, `startAlert(watcher)`, `takeByWatcher(watcher)`, `addLampAttention(lamp)` | All watcher attention behavior. |
| `gameplay/night.js` | `updateNight(dt)`, `poolWaterAt(time)`, `poolClosed()`, `setFirstLight()`, `lampStateAt(lamp,time)` | Time and lamp schedules. |
| `gameplay/pool.js` | `updatePool(dt)`, `tryEnterPool()`, `closePool()` | Success and closure. |
| `gameplay/bulbs.js` | `updateBulbs(dt)`, `collectBulb(id)`, `bulbSetComplete()`, `resetBulbs()` | Bulb collection and set boolean. |
| `gameplay/tile.js` | `updateTile(dt)`, `disturbTile(id)`, `resetTile()` | Loose tile support. |
| `gameplay/cat.js` | `updateCat(dt)`, `checkCatTrigger()`, `spawnCat()`, `removeCat()` | Fixed event only. |
| `gameplay/reset.js` | `resetAttempt(reason)`, `completeAttempt()` | Central reset/completion. |
| `ui/screens.js` | `setMode(mode)`, `showFailure(reason)`, `showCompletion()`, `returnToStart()` | HTML/CSS state machine. |
| `ui/hud.js` | `updateHud()` | Updates DOM elements from `G`. |
| `audio/audio.js` | `play(name)`, `startLoop(name)`, `stopLoop(name)`, `setAmbient(enabled)` | Synthesized audio only. |
| `debug/api.js` | see `8. DEBUG API` | Direct state inspection and forcing. |
| `tests/*` | tier test functions | Use debug API only. |

# 3. VISUAL SPEC

The look is a close, wet, side-on rooftop at night. The player sees the frog at about 2 to 3 frog heights from the camera edge. Surfaces are shiny, dark, and slightly reflective. Safe ground is dark and damp; danger is visible as lamp glow, steam, fan motion, glass sparkle, open gutter voids, and attention cones. The Moon Pool is the brightest goal, but its water level visibly lowers through a grate. The game should feel like moving across a rooftop that is quietly watching you.

## Lighting and atmosphere

| Light / atmosphere element | Visual rule | Gameplay meaning |
| --- | --- | --- |
| Ambient night | Base dark blue-black. No global gameplay danger except `firstLight` at pool close. | Dark areas are safe unless inside attention. |
| Shadow | Areas not inside active lamp/watcher attention. Rendered as darker wet shapes. | Safe ground. |
| Lamp glow | Amber cone from lamp fixture. Starts thin and dim, expands during warm phase. | Lamp light is watcher attention. |
| Watcher attention | Cool blue cone or rectangle. Turns red when `alert`. | If frog is inside and occluded, being seen. |
| Drain steam | Low white-gray steam column when drain active. | Active fixed danger. |
| Fan motion | Rotating blades and white airflow lines when fan active. | Active fixed danger. |
| Open gutter | Void below surfaces, faint city reflection, no floor. | Fixed danger. |
| Rain | Thin vertical streaks, low alpha, parallax. | Wet tone, no gameplay effect. |
| Drips | Small periodic drips from gutters, awnings, glass. | Wet tone, no gameplay effect. |
| First light | Pale cyan wash from top-right at 100-120s. | Visual pressure; pool closes at 120s. |

## Space

| Space | Visual composition |
| --- | --- |
| Start rain barrel | Large dark barrel with lily pad, water sheen, rain ripples. Camera starts centered on barrel. |
| Yard | Lower roof area with heron silhouette, shallow yard ledge, steam from drains, low city glow. |
| Upper route | Thin wires, awnings, windowsills, lamp glints, glass reflections. |
| Lower route | Wet ledges, drain vents, fan grills, broken glass, open gutter voids. |
| Greenhouse | Old glass frame around Moon Pool, hatch, grate, pool reflection. Glass is not a hazard. |
| Moon Pool | Circular pool basin with water surface that lowers; grate becomes visible as water drains; hatch shuts at closure. |

## Recipe table

| Element | Recipe |
| --- | --- |
| Palette: night base | `#050a10`, `#0a1118`, `#14202c`, `#203142` |
| Palette: wet highlights | `#7fa8c4`, `#b9d7ea`, `#d8f0ff` low alpha |
| Palette: lamp danger | `#ff8a2a`, `#ffb35c`, `#ffd280` |
| Palette: attention calm | `#74b7ff` 20-30% alpha |
| Palette: attention alert | `#ff4d4d` 35% alpha |
| Palette: safe shadow | `#04080c`, `#071018` |
| Palette: frog | body `#3fae6d`, highlight `#7ee08a`, belly `#d7f7c7`, eye `#111827` |
| Palette: heron | feathers `#c9d2d8`, shadow `#6d7882`, beak `#d97706`, eye `#111827` |
| Palette: cat | fur `#2b2b35`, highlight `#4a4a5a`, eyes `#ffd166` |
| Palette: Moon Pool | water `#123a55`, surface highlight `#7fd7ff`, grate `#202830` |
| Frog sprite | 16x16 visual, 10x10 collision. Rounded body, small limbs, subtle wet sheen. |
| Frog animation | Idle: slight breath. Move: short leg push. Jump: legs tuck. Fall: limbs spread. Land: squash 10% for 60ms. Take: small fade/splash. |
| Heron sprite | 40x70 visual. Long neck, still pose. Eye moves to show attention. |
| Cat sprite | 28x22 visual. Compact, tail still. Eyes glow. |
| Attention cone | Drawn from watcher eye or lamp origin. Clipped by occluders. Calm blue, alert red. |
| Rain | 2px vertical lines, alpha 0.08, speed 420px/s, parallax 0.7. |
| Drips | 3px droplets, spawn from random deterministic drip points every 1.5-4.0s, no gameplay. |
| Lamp | Fixture small amber rectangle. Warm phase flickers. Light cone grows. |
| Drain | Grate rectangle. Active: steam particles upward, alpha pulsing. |
| Fan | Circular grill with 4 blades. Active: blades rotate 720deg/s, airflow lines. |
| Broken glass | Jagged white-blue highlights. Static. |
| Open gutter | Dark void, faint city reflection, no floor. |
| Greenhouse glass | Frame and reflection only. Not red, not hazard. |
| Moon Pool | Water surface line lowers with `pool.water`. Grate appears when water below `0.35`. |
| HUD | Thin dark translucent HTML bars. No canvas text for critical UI. |

# 4. GAMEPLAY SPEC

The game is one crossing. The frog starts asleep on a lily inside a rain barrel. Waking is automatic. The attempt starts when the frog leaves the barrel. The player crosses gutters, windowsills, wires, awnings, ledges, and lower wet paths toward the Moon Pool. The night changes on a fixed schedule: the heron looks, cat may appear, lamps warm, drains and fans switch, and the pool drains. The frog is safe only while hidden from attention. Any watcher, lamp light, open gutter, active drain, active fan, broken glass, lamp fixture, or pool closure ends the attempt. Completing the crossing shows whether the five rain lily bulbs were completed and returns to the same start.

## Records and rosters

### Player

| Field | Initial | Notes |
| --- | --- | --- |
| `x,y` | `170,754` | Start on lily in barrel. |
| `w,h` | `10,10` | Collision box. |
| `vx,vy` | `0,0` | Physics. |
| `facing` | `1` | Visual only. |
| `grounded` | `true` | Starts on barrel. |
| `alive` | `true` | No health. |
| `animation` | `"wake"` | Changes to `idle` at 1.2s. |

### Level platforms

All coordinates are top-left rectangles. `top` is `rect.y`.

| ID | Type | Rect | Material | Notes |
| --- | --- | --- | --- | --- |
| `BARREL` | solid | `120,760,120,120` | barrel | Start platform. Attempt begins when player leaves its bounds. |
| `L1` | one-way | `245,742,45,6` | wet_ledge | Small first hop. |
| `G1` | solid | `300,735,170,12` | gutter | Runs toward windowsill. |
| `TILE_1` | one-way | `478,720,32,6` | loose_tile | Short optional bridge. Falls if `BULB_1` taken. |
| `W1` | solid | `520,710,120,14` | windowsill | Cat trigger surface. |
| `WIRE_1` | one-way | `660,640,240,4` | wire | First safe wire crossing. |
| `A1` | solid | `900,600,300,12` | awning | Cat watches this if triggered. |
| `LEDGE_B3` | one-way | `1120,580,40,4` | wet_ledge | Hidden place for `BULB_3`. |
| `LD1` | solid | `660,760,180,14` | wet_ledge | Lower route under awning. |
| `LD2` | solid | `860,740,180,14` | wet_ledge | Lower route, `BULB_2`. |
| `LD3` | solid | `1060,720,160,14` | wet_ledge | Lower route, `DRAIN_1` sits here. |
| `W2` | solid | `1260,660,140,14` | windowsill | Upper route, `BG_1` and `BULB_4`. |
| `LD4` | solid | `1300,740,160,14` | wet_ledge | Lower route. |
| `LD5` | solid | `1500,720,160,14` | wet_ledge | Lower route. |
| `WIRE_2` | one-way | `1420,620,220,4` | wire | Upper route. |
| `A2` | solid | `1660,580,220,12` | awning | Upper route. |
| `LD6` | solid | `1700,700,160,14` | wet_ledge | Lower route. |
| `L7` | one-way | `1860,680,60,6` | wet_ledge | Thin narrow ledge. |
| `W3` | solid | `1940,620,140,14` | windowsill | Upper approach. |
| `WIRE_3` | one-way | `2100,560,200,4` | wire | Approach to greenhouse. |
| `LEDGE_B5` | one-way | `2480,548,40,4` | wet_ledge | Hidden place for `BULB_5`. |
| `GL1` | solid | `2340,600,160,14` | greenhouse | Greenhouse ledge. |
| `GL2` | solid | `2540,620,160,14` | greenhouse | Greenhouse ledge, `DRAIN_2`. |
| `GL3` | solid | `2720,650,80,14` | greenhouse | Last ledge before pool. |
| `YARD1` | solid | `520,800,360,100` | wet_ledge | Heron yard. |
| `POOL_BOTTOM` | solid | `2780,800,200,20` | pool_wall | Pool bottom/grate. |
| `GREENHOUSE_FRAME` | occluder | `2740,520,260,300` | greenhouse | Visual frame and occluder, not a hazard. |

### Triggers

| ID | Rect | Effect |
| --- | --- | --- |
| `START_EXIT` | `236,680,24,160` | If player AABB overlaps, `attempt.active=true`, night timer starts. Also attempt starts if player AABB no longer overlaps `BARREL` and player center x > 236. |
| `WINDOWSILL_TRIGGER` | `520,696,120,14` | If `BULB_1.collected=true` and player overlaps, cat spawn is queued. |

### Fixed dangers

| ID | Type | Rect | Active | Effect |
| --- | --- | --- | --- | --- |
| `OG_1` | open_gutter | `470,748,48,152` | always | Drop death. |
| `OG_2` | open_gutter | `1450,760,120,140` | always | Drop death. |
| `OG_3` | open_gutter | `2650,760,150,140` | always | Drop death. |
| `WORLD_BOTTOM` | open_gutter | `0,900,3200,20` | always | Drop death. |
| `DRAIN_1` | drain | `1080,706,40,14` | intervals `[20,38]`, `[72,88]` | Pull/scald death. |
| `DRAIN_2` | drain | `2580,606,40,14` | intervals `[55,70]`, `[92,108]` | Pull/scald death. |
| `FAN_1` | fan | `1210,640,30,80` | intervals `[40,58]`, `[95,112]` | Blown-off death. |
| `FAN_2` | fan | `2480,560,30,80` | intervals `[68,82]`, `[100,115]` | Blown-off death. |
| `LAMP_1_FIXTURE` | lamp_fixture | `1135,520,16,16` | always | Burn death. |
| `LAMP_2_FIXTURE` | lamp_fixture | `2505,500,16,16` | always | Burn death. |
| `BG_1` | broken_glass | `1360,648,40,12` | always | Cut death. |
| `BG_2` | broken_glass | `2350,588,50,12` | always | Cut death. |

### Watchers

| ID | Type | Eye / origin | Cone / attention | Active |
| --- | --- | --- | --- | --- |
| `HERON_1` | heron | `760,778` | `coneLength=340`, calm `halfAngle=16`, alert `halfAngle=22` | Always active. |
| `CAT_1` | cat | `1062,582` | `coneLength=220`, `halfAngle=10` | Only if triggered. |
| `LAMP_1_LIGHT` | lamp_light | `1143,536` | base angle 90 down, half 12, length 0 to 45 | Active after warm schedule. |
| `LAMP_2_LIGHT` | lamp_light | `2513,516` | base angle 90 down, half 12, length 0 to 45 | Active after warm schedule. |

### Rain lily bulbs

| ID | Position | Radius | Notes |
| --- | --- | ---: | --- |
| `BULB_1` | `494,716` | 7 | Under/attached to loose tile. Required for cat trigger. |
| `BULB_2` | `950,732` | 7 | Lower route on `LD2`. |
| `BULB_3` | `1138,572` | 7 | Hidden place on `LEDGE_B3`; becomes deadly when `LAMP_1_LIGHT` is lit. |
| `BULB_4` | `1390,642` | 7 | Upper route near `W2`, above `BG_1`. |
| `BULB_5` | `2508,540` | 7 | Hidden place on `LEDGE_B5`; becomes deadly when `LAMP_2_LIGHT` is lit or `FAN_2` active. |

### Moon Pool records

| Field | Value |
| --- | --- |
| Basin | `2780,620,200,180` |
| Water top | `620 + (1 - pool.water) * 180` |
| Success rect | `2780,waterTop,200,800-waterTop` |
| Grate | `2780,790,200,10` |
| Hatch | `2900,560,80,120` |
| Close time | `night.time >= 120` |
| Closed visual | water gone behind grate, hatch shut |

## 4.1 Player movement

Tier: 1.

| Rule | Number |
| --- | ---: |
| Input axis | `-1` left, `1` right, `0` none |
| Max horizontal speed | `170` px/s |
| Ground acceleration | `1400` px/s² |
| Air acceleration multiplier | `0.75` |
| Ground friction when no input | `1800` px/s² |
| Air drag when no input | `300` px/s² |
| Gravity | `1500` px/s² |
| Jump impulse | `520` px/s upward (`vy = -520`) |
| Variable jump cut | If jump released and `vy < -200`, set `vy *= 0.45` |
| Max fall speed | `720` px/s |
| Coyote time | `0.08` s |
| Jump buffer | `0.08` s |
| Ground check | Player bottom within `2` px of top of a present platform while falling/standing |
| Landing | Set `vy=0`, `grounded=true`, `coyote=0.08`, play `land` |
| Jump conditions | `grounded` or `coyote > 0`, and `jumpBuffer > 0` |
| Facing | Updates to input axis if nonzero |
| Death | Player remains in world, `alive=false`, `animation="take"`, reset after `1.0` s |

Input mapping:

| Input | Action |
| --- | --- |
| ArrowLeft, KeyA | Move left |
| ArrowRight, KeyD | Move right |
| Space, KeyW, ArrowUp | Jump; hold for full jump, release early for shorter jump |
| KeyR | Debug reset only; not player-facing |

## 4.2 Attempt start and reset

Tier: 1.

| State | Rule |
| --- | --- |
| `wake` | After `boot`, show frog waking for 1.2s. No night timer. Player cannot fall into a hazard while in barrel. |
| `playing` | Player can move. `attempt.active` remains false until player leaves barrel. |
| Attempt start | Set `attempt.active=true`, `night.time=0`, play `attempt_start`, start ambient. |
| Normal start | If player remains in barrel, no time passes and no watchers change. |
| Failure | On any take or pool close, set `mode="failed"`, `player.alive=false`, `player.animation="take"`, play `taken`, reset after 1.0s. |
| Reset | Restore all initial level state: player, bulbs, tile, cat, watchers, hazards, pool, night timer. Return to `playing` start. |
| Completion | On success, set `mode="completed"`, calculate `bulbsComplete`, show result, return to start after 2.0s. |
| No next crossing | Completion returns to the same start, not a new level. |

## 4.3 Platform route viability

Tier: 1.

| Rule | Detail |
| --- | --- |
| Usable surface | A platform is usable if `present=true`, reachable by collision, not currently covered by an active fixed-danger rectangle, and not currently watched by an active attention rectangle that makes the surface impossible. |
| One-way platform | Player passes through upward. Lands only if previous bottom was above top and current bottom crosses top with `vy >= 0`. |
| Solid platform | Player collides on all sides. |
| Thin ledge | One-way platforms are 4-6 px tall. The frog’s 10 px collision makes them usable without special rules. |
| Open gutter | If player AABB overlaps any `open_gutter` hazard, attempt fails. |
| Route impossible | If a required gap is too wide, a required surface is absent, watched, or covered by active fixed danger, the route is impossible. |
| Route possible | If surfaces are present, reachable, and not covered by active attention or fixed danger, the route is possible. |
| Tile disturbed | If `TILE_1.present=false`, `TILE_1` is not a usable ledge. |

## 4.4 Fixed dangers

Tier: 1.

| System | Rule | Numbers |
| --- | --- | --- |
| Open gutters | Always active. If player AABB overlaps, attempt fails with `open_gutter`. | Rectangles listed above; world bottom always kills. |
| Drains | Active intervals kill. Inactive intervals are passable. | `DRAIN_1`: `[20,38]`, `[72,88]`. `DRAIN_2`: `[55,70]`, `[92,108]`. |
| Fans | Active intervals kill. Inactive intervals are passable. | `FAN_1`: `[40,58]`, `[95,112]`. `FAN_2`: `[68,82]`, `[100,115]`. |
| Broken glass | Always active. Overlap kills. | `BG_1`, `BG_2`. |
| Lamp fixture | Always active. Overlap kills. | `LAMP_1_FIXTURE`, `LAMP_2_FIXTURE`. |
| Lamp light | Not instant kill. It is watcher attention. If visible in light and not hidden, use watcher alert rules. | See `4.6`. |
| Death | No damage state. One overlap ends attempt. | `player.alive=false`, `animation="take"`. |

## 4.5 Shadow, cover, and being seen

Tier: 1.

| Rule | Detail |
| --- | --- |
| Shadow | Any area not inside an active watcher cone, attention rectangle, or lamp light is safe ground. |
| Cover | A solid occluder between watcher eye/light origin and player center hides the player. |
| Occluders | All `solid` platforms and `GREENHOUSE_FRAME`. One-way thin ledges are not occluders. The platform the player stands on is ignored. |
| Hidden check | `hidden = occluded || !insideAttention` |
| Visible | `visible = insideAttention && !occluded` |
| Safe | Player is safe while hidden. |
| Being seen | Any active watcher or lamp light sees the frog if visible. |
| Waiting in shadow | The player can stand still while no active attention covers them. |
| Hiding | The player can use underside of awnings, ledges, walls, and greenhouse frame to break rays. |
| Open lit space | A space covered by attention and not occluded cannot be crossed without timing or reaching shadow. |

## 4.6 Watchers and attention

Tier: 1.

### Shared watcher state machine

| State | Rule |
| --- | --- |
| `calm` | Watcher follows its schedule. If it sees the frog, enter `alert`. |
| `alert` | `alertT` increases. If the frog remains visible for `ALERT_DURATION=1.0`, take. If hidden for `HIDE_GRACE=0.35`, enter `cooldown`. |
| `cooldown` | For `WATCHER_COOLDOWN=1.2`, the watcher turns away and stops scanning that area. |
| `coverNext` | On entering `alert`, add `attentionRect` to the next surface in `surfacePath` for `COVER_NEXT_DURATION=2.0`. |
| Take | Set `attempt.failReason="watcher"`, kill player. |

### Visibility algorithm

```text
for each active watcher or lamp_light:
  if player center is inside watcher cone or attentionRect:
    if rayIntersectsOccluder(watcher.eye, player.center, ignore=[player.groundId]):
      hidden
    else:
      visible
```

### Heron `HERON_1`

| Field | Value |
| --- | --- |
| Type | heron |
| Position | stands on `YARD1`, eye `760,778` |
| Cone length | 340 |
| Calm half-angle | 16° |
| Alert half-angle | 22° |
| Surface path | `["YARD1","LD1","LD2","LD3"]` |
| Alert duration | 1.0 |
| Hide grace | 0.35 |
| Cooldown | 1.2 |
| Cover next duration | 2.0 |

Heron patrol:

| Night time | Base angle | Meaning |
| --- | ---: | --- |
| `0 <= t < 25` | `0°` | Looking right along yard. Not looking toward frog at start. |
| `25 <= t < 55` | scan `250° -> 290°` over 10s, repeat | Looks up toward lower ledges. |
| `55 <= t < 85` | scan `180° -> 360°` over 8s, repeat | Watches wider lower route. |
| `85 <= t <= 120` | scan `270° -> 180° -> 0°` over 5s, repeat | Night is harder; lower route is frequently watched. |

### Lamp attention

| ID | Warm schedule | Light length | Half-angle | Effect |
| --- | --- | ---: | ---: | --- |
| `LAMP_1_LIGHT` | dark until 35; warming 35-50; lit 50-120 | 0 -> 45 -> 45 | 12° | Makes `LEDGE_B3` watched after warm. |
| `LAMP_2_LIGHT` | dark until 75; warming 75-90; lit 90-120 | 0 -> 45 -> 45 | 12° | Makes `LEDGE_B5` watched after warm. |

Lamp light uses the same alert duration as watchers: 1.0 seconds. The lamp itself does not chase, but the lit surface remains watched while lit.

## 4.7 Time cycle and night changes

Tier: 1.

| Time | Change |
| ---: | --- |
| 0 | Attempt starts. Pool full. Lamps dark. Drains/fans inactive. Heron looks right. |
| 20 | `DRAIN_1` activates. |
| 25 | Heron begins looking up toward lower ledges. |
| 35 | `LAMP_1_LIGHT` begins warming. |
| 38 | `DRAIN_1` deactivates. |
| 40 | `FAN_1` activates. |
| 50 | `LAMP_1_LIGHT` fully lit. |
| 55 | `DRAIN_2` activates. Heron scan widens. |
| 58 | `FAN_1` deactivates. |
| 68 | `FAN_2` activates. |
| 70 | `DRAIN_2` deactivates. |
| 72 | `DRAIN_1` activates again. |
| 75 | `LAMP_2_LIGHT` begins warming. |
| 82 | `FAN_2` deactivates. |
| 85 | Heron scan becomes faster. |
| 88 | `DRAIN_1` deactivates. |
| 90 | `LAMP_2_LIGHT` fully lit. |
| 92 | `DRAIN_2` activates again. |
| 95 | `FAN_1` activates again. |
| 100 | First light visual begins. |
| 108 | `DRAIN_2` deactivates. |
| 112 | `FAN_1` deactivates. |
| 115 | `FAN_2` activates again. |
| 120 | Moon Pool water reaches 0. Greenhouse hatch shuts. Attempt fails if not already complete. |

## 4.8 Moon Pool goal and closure

Tier: 1.

| Rule | Number |
| --- | --- |
| Water formula | `pool.water = max(0, 1 - night.time / 120)` |
| Water top | `620 + (1 - pool.water) * 180` |
| Success | If `pool.water > 0` and player center is inside success rectangle, complete attempt. |
| Closure | If `night.time >= 120`, set `pool.closed=true`, `attempt.failReason="pool_closed"`, fail. |
| Success after close | Not allowed. Success check is disabled when `pool.closed=true`. |
| Visual | Water lowers. Grate appears when water below `0.35`. Hatch animates shut at 120. |
| Completion | Set `mode="completed"`, show only whether bulbs were completed, then return to start. |

## 4.9 Rain lily bulbs and set completion

Tier: 1.

| Rule | Number |
| --- | --- |
| Total bulbs | 5 |
| Collection | Player center within `7` px of bulb center. |
| Effect | `bulb.collected=true`, HUD count increases, play `bulb`, no gameplay power. |
| Set complete | `collectedCount == 5` |
| Failure | All bulb collection flags reset. |
| Completion | Show `Rain lily bulbs: completed` if count 5, otherwise `Rain lily bulbs: not completed`. |
| Persistence | Session-only boolean in `G.completion.bulbsComplete`. No localStorage. No unlocks. |
| Optional | A crossing can be completed with 0 bulbs. |

## 4.10 Loose tile disturbance

Tier: 2.

| Rule | Number |
| --- | --- |
| Tile ID | `TILE_1` |
| Initial | Present as one-way platform `478,720,32,6` |
| Bulb | `BULB_1` at `494,716` |
| Trigger | Collecting `BULB_1` sets `TILE_1.present=false`, `TILE_1.falling=true`, `fallTime=0.5` |
| Visual | Tile slips and falls into `OG_1` gap. |
| Route effect | Short bridge across `OG_1` is closed for rest of attempt. |
| Main route | Player can still jump from `G1` to `W1` without the tile. |
| Reset | Tile returns, bulb uncollected, fall state cleared. |

## 4.11 Cat appearance event

Tier: 2.

| Rule | Number |
| --- | --- |
| Trigger | `BULB_1.collected=true` and player overlaps `WINDOWSILL_TRIGGER` |
| Spawn location | On `A1`, x `1050`, y `588`, eye `1062,582` |
| No cat | If `BULB_1` not collected, cat never appears that attempt. |
| Cat state | `appearing` for 0.8s, then `watching` |
| Watch cycle | `watching` 3.5s facing left along awning, then `turned` 2.5s facing down-right. |
| Cone | length 220, half-angle 10°. |
| Alert | If visible, alert duration 0.8s. |
| Route effect | While cat is watching, upper awning route is unsafe. Lower route becomes the safer option. |
| Reset | Cat removed. |

## 4.12 Hidden places becoming reachable or deadly

Tier: 2.

| Rule | Detail |
| --- | --- |
| Hidden place | Optional ledge or bulb not on the shortest safe route. |
| Reachable | It is reachable when the player can stand on it and no active attention or fixed danger covers it. |
| Deadly | It becomes deadly when a watcher turns toward it, a lamp lights it, a drain/fan switches on, or a tile falls and removes the route. |
| Example 1 | `LEDGE_B3` is reachable before `LAMP_1_LIGHT` warms. After 50s it is watched. |
| Example 2 | `LEDGE_B5` is reachable before `LAMP_2_LIGHT` and before `FAN_2` active intervals. It becomes deadly when those activate. |
| Example 3 | Lower route is reachable when heron is looking away and drains/fans are inactive. It becomes deadly when attention or fixed danger covers it. |
| No new systems | Uses only platforms, hazards, watchers, lamps, tiles, and bulbs already defined. |

## Progression and difficulty

| Phase | Time | Player experience |
| --- | ---: | --- |
| Quiet wake | 0-20 | Learn movement, see heron, optional first tile risk. |
| First attention | 20-50 | Lower route watched, drain/fan timing, optional bulb risk. |
| Cat and lamp | 50-85 | If first bulb taken, cat watches awning; lamp lights make hidden places deadly. |
| Harder night | 85-115 | Faster heron, repeated fans/drains, second lamp lit, pool visibly low. |
| First light | 115-120 | Pool nearly gone, visual pressure, final dash. |

## Feel

The player should feel small, wet, and watched. Movement is precise but not acrobatic. The correct play is not speed alone; it is moving between safe dark places, waiting while attention sweeps away, and choosing whether a bulb is worth a risk. Failure is not combat; it is being noticed or touching something that cannot be survived.

# 5. CHARACTERS

## Frog

| State | Visual rule |
| --- | --- |
| `wake` | Eyes blink open after 1.2s. No input accepted. |
| `idle` | Slight breathing, occasional blink. |
| `move` | Short push animation, legs shift, facing follows input. |
| `jump` | Legs tuck, body stretches upward. |
| `fall` | Limbs spread, slight rotation opposite velocity. |
| `land` | Squash 10% for 60ms, wet splash particles. |
| `take` | Small splash/ripple, fade out over 0.5s. |

Collision: `10x10`.

## Heron

| State | Visual rule |
| --- | --- |
| `idle` | Still pose, head moves to show base angle. |
| `scan` | Head turns along patrol angles. |
| `alert` | Head snaps toward player, cone turns red. |
| `cooldown` | Head turns away, cone fades. |
| `take` | Quick strike animation, then reset. |

Silhouette: long neck, still body, beak points toward attention.

## Cat

| State | Visual rule |
| --- | --- |
| `absent` | Not drawn. |
| `appearing` | Fade in on awning over 0.8s, eyes glow. |
| `watching` | Sitting, head faces left along awning. |
| `turned` | Head faces down-right, tail still. |
| `alert` | Eyes brighten, cone turns red. |
| `taking` | Quick swipe, then reset. |

Silhouette: compact, low, tail straight.

# 6. AUDIO

| Name | Recipe | When it plays |
| --- | --- | --- |
| `ambient_rain` | Filtered white noise, bandpass 400-1800Hz, low gain, slow LFO amplitude. | Starts on attempt start, stops on reset. |
| `city_hum` | Two sine waves 60Hz and 120Hz, very low gain, slow detune. | Starts on attempt start. |
| `drip` | Short sine 900Hz to 500Hz, 40ms, random deterministic drip points. | Periodic ambient. |
| `wake` | Soft sine 220Hz to 330Hz, 300ms, low gain. | Start wake animation. |
| `attempt_start` | Low thud sine 80Hz, 120ms. | When attempt becomes active. |
| `move` | Tiny filtered noise 100Hz, 20ms, gated. | Foot contact while moving, max once per 0.12s. |
| `jump` | Square 220Hz to 110Hz, 80ms. | Jump. |
| `land` | Noise 180Hz, 60ms. | Landing. |
| `splash` | Bandpass noise 400-1200Hz, 180ms. | Enter pool or water death. |
| `bulb` | Sine 880Hz to 1320Hz, 120ms, sparkle partial 1760Hz. | Collect bulb. |
| `tile_fall` | Noise sweep 300Hz to 80Hz, 300ms. | Loose tile falls. |
| `cat_appear` | Sine 300Hz to 200Hz, 220ms, plus noise. | Cat appears. |
| `cat_watch` | Low sine 80Hz pulse, 100ms. | Cat enters watching cycle. |
| `heron_turn` | Filtered noise 500Hz, 150ms. | Heron changes base angle. |
| `alert` | Sine 440Hz, 100ms, two quick pulses. | Watcher/lamp sees frog. |
| `taken` | Sine 120Hz to 60Hz, 300ms. | Any death. |
| `drain_active` | Noise 150-400Hz loop, low gain. | Drain active. |
| `fan_active` | Noise 80-300Hz loop with tremolo. | Fan active. |
| `lamp_warm` | Sine 180Hz to 240Hz, 400ms. | Lamp begins warming. |
| `pool_close` | Sine 70Hz to 40Hz, 1000ms. | Pool closes at 120s. |
| `success` | Sine 660Hz, 880Hz, 990Hz arpeggio, 800ms. | Enter Moon Pool. |
| `reset` | White noise fade 300ms. | Attempt reset. |

# 7. UX

## Screens state machine

| State | Entry | Exit |
| --- | --- | --- |
| `boot` | Page load. Show simple title text for 0.8s. | `wake` |
| `wake` | Show frog waking in barrel for 1.2s. | `playing` |
| `playing` | Normal run. HUD visible. | `failed` or `completed` |
| `failed` | Death animation. Show reason briefly: “Taken”, “Pool closed”. | `playing` after 1.0s |
| `completed` | Show “Moon Pool reached” and only whether rain lily bulbs were completed. | `playing` after 2.0s |

No pause, no menu, no next crossing.

## HUD

| Element | Record field | When visible |
| --- | --- | --- |
| `#bulb-count` | `G.bulbs.filter(b=>b.collected).length` and total 5 | `mode="playing"` only |
| `#night-bar` | `G.night.time / G.night.duration` | `attempt.active=true` |
| `#pool-bar` | `G.pool.water` | `attempt.active=true` |
| `#alert-dot` | any `watcher.state="alert"` or `attempt.failReason="watcher"` | While a watcher is alert; brief flash on take |
| `#fail-reason` | `G.attempt.failReason` | `mode="failed"` |
| `#end-bulbs` | `G.completion.bulbsComplete` | `mode="completed"` |
| `#start-hint` | none | `mode="playing"` until first successful jump; fades after first jump. Not required for completion. |

HUD style: dark translucent bars, thin lines, no bright boxes over the gameplay world.

# 8. DEBUG API

| System | Function | Returns / effect |
| --- | --- | --- |
| Input | `debugInput.set(left,right,jump)` | Sets input state for tests. |
| Player | `debugPlayer.get()` | Returns player record. |
| Player | `debugPlayer.teleport(x,y)` | Moves player. |
| Attempt | `debugAttempt.start()` | Forces attempt active. |
| Attempt | `debugAttempt.reset()` | Resets attempt. |
| Level | `debugLevel.getPlatform(id)` | Returns platform. |
| Platform | `debugPlatform.setPresent(id,present)` | Sets tile/platform presence. |
| Hazards | `debugHazard.get(id)` | Returns hazard. |
| Hazards | `debugHazard.setActive(id,active)` | Forces active state. |
| Watchers | `debugWatcher.get(id)` | Returns watcher. |
| Watchers | `debugWatcher.isPlayerVisible(id)` | Returns current visibility boolean. |
| Watchers | `debugWatcher.forceAlert(id)` | Starts alert state. |
| Night | `debugNight.setTime(t)` | Sets night timer. |
| Lamp | `debugLamp.getState(id)` | Returns lamp light state. |
| Pool | `debugPool.get()` | Returns pool record. |
| Pool | `debugPool.setWater(w)` | Sets pool water. |
| Bulbs | `debugBulb.get(id)` | Returns bulb. |
| Bulbs | `debugBulb.collect(id)` | Collects bulb. |
| Tile | `debugTile.get()` | Returns tile record. |
| Tile | `debugTile.disturb()` | Disturbs tile. |
| Cat | `debugCat.get()` | Returns cat record. |
| Cat | `debugCat.spawn()` | Spawns cat. |
| UI | `debugUi.setMode(mode)` | Sets UI mode. |

# 9. TESTS

| Test ID | Tier | Steps | Expected |
| --- | --- | --- | --- |
| T1-INPUT-01 | 1 | Set right input. Run 1s. | Player x increases by about 170 px. |
| T1-INPUT-02 | 1 | Grounded, press jump. | vy becomes -520, apex about 90 px. |
| T1-PLAT-01 | 1 | Drop onto solid platform. | Player lands, vy=0, grounded=true. |
| T1-PLAT-02 | 1 | Jump upward through one-way. | Player passes through. |
| T1-OPEN-01 | 1 | Move player into `OG_1`. | `attempt.failReason="open_gutter"`, reset occurs. |
| T1-HAZ-01 | 1 | Force `DRAIN_1.active=true`, move player into rect. | Death and reset. |
| T1-HAZ-02 | 1 | `DRAIN_1.active=false`, move through rect. | No death. |
| T1-VIS-01 | 1 | Place player inside heron cone, no occlusion. | `isPlayerVisible=true`, watcher enters alert. |
| T1-VIS-02 | 1 | Place player inside occluder shadow. | `isPlayerVisible=false`. |
| T1-VIS-03 | 1 | Player visible for 1.0s. | Heron takes player. |
| T1-VIS-04 | 1 | Player visible 0.5s then hidden. | Watcher enters cooldown, no take. |
| T1-TIME-01 | 1 | Set night time 119. | Pool water near 0.008. |
| T1-POOL-01 | 1 | Set water 0.5, place player in pool. | Attempt completes. |
| T1-POOL-02 | 1 | Set night time 120. | Pool closed, attempt fails. |
| T1-BULB-01 | 1 | Collect 5 bulbs. | `bulbSetComplete=true`. |
| T1-BULB-02 | 1 | Collect 2 bulbs, fail. | On reset, collected count is 0. |
| T2-TILE-01 | 2 | Collect `BULB_1`. | `TILE_1.present=false`, tile falls. |
| T2-TILE-02 | 2 | Reset. | Tile present, bulb uncollected. |
| T2-CAT-01 | 2 | Collect `BULB_1`, enter `W1`. | Cat spawns on awning. |
| T2-CAT-02 | 2 | Do not collect `BULB_1`, enter `W1`. | Cat does not spawn. |
| T2-CAT-03 | 2 | Cat active, player on awning during watch cycle. | Cat sees player and can take. |
| T2-HIDDEN-01 | 2 | Before 50s, collect `BULB_3`. | Possible. |
| T2-HIDDEN-02 | 2 | After 50s, place player on `LEDGE_B3`. | Lamp light sees player. |
| T2-HIDDEN-03 | 2 | After 90s, place player on `LEDGE_B5`. | Lamp light sees player. |
| INTEG-01 | 1+2 | Play a deterministic route collecting 0 bulbs. | Complete before 120s. |
| INTEG-02 | 1+2 | Play a route collecting all 5 bulbs. | Complete shows `bulbsComplete=true`. |

# 10. BUILD ORDER

1. Create HTML shell, CSS, canvas, fixed loop, global context.
2. Implement input and player movement.
3. Implement platforms, collision, camera, and start barrel.
4. Implement open gutter death and world bottom death.
5. Implement attempt start/reset.
6. Implement fixed dangers and schedules.
7. Implement visibility, occlusion, attention state machine.
8. Implement heron and lamp attention.
9. Implement night timer and pool drain/close.
10. Implement pool success and completion screen.
11. Implement bulbs and completion boolean.
12. Verify Tier 1 tests.
13. Implement loose tile and bulb trigger.
14. Implement cat event and cat watcher.
15. Implement hidden place rules and verify Tier 2 tests.
16. Tune only within existing systems.

# 11. DEFINITION OF DONE

## Tier 1 Definition of Done

Tier 1 is done when the player can complete one full crossing or die and restart, with all core systems working.

- [ ] Frog starts in rain barrel and can leave it.
- [ ] Leaving barrel starts the attempt and night timer.
- [ ] Player movement, jump, coyote, buffer, and variable jump work.
- [ ] Platforms are reachable and collision works.
- [ ] Open gutters and world bottom kill.
- [ ] Drains, fans, broken glass, and lamp fixtures kill when active/overlapped.
- [ ] Inactive drains and fans are passable.
- [ ] Watchers see only through cones/attention rectangles and occlusion.
- [ ] Being visible starts alert; hiding before 1.0s prevents take.
- [ ] Heron patrol runs deterministically.
- [ ] Lamp light acts as attention.
- [ ] Pool drains from 1.0 to 0.0 over 120s.
- [ ] Pool closure fails the attempt.
- [ ] Entering pool before closure completes the game.
- [ ] Completion shows only whether bulbs were completed.
- [ ] Completion and failure return to the same start.
- [ ] All 5 bulbs collect and reset.
- [ ] Tier 1 tests pass.

## Tier 2 Definition of Done

Tier 2 is done when supporting mechanics add risk without breaking Tier 1.

- [ ] `BULB_1` collection disturbs `TILE_1`.
- [ ] `TILE_1` falls and is unusable for the rest of the attempt.
- [ ] Reset restores tile and bulb.
- [ ] Cat appears only after `BULB_1` and `W1` trigger.
- [ ] Cat watches awning on deterministic cycle.
- [ ] Cat can take the frog through attention.
- [ ] Reset removes cat.
- [ ] Hidden places become reachable or deadly through existing schedules.
- [ ] No new systems are added.
- [ ] Tier 2 tests pass.

## Tier 3 Definition of Done

Tier 3 is optional tuning only.

- [ ] No new systems exist.
- [ ] No new content exists.
- [ ] Any changes are numbers inside existing systems.
- [ ] Tier 1 and Tier 2 tests still pass.

# A. SANITY

| Check | Result |
| --- | --- |
| Did I add extra gameplay systems? | No. Only platforming, fixed dangers, attention, time, pool, bulbs, tile, cat, hidden places. |
| Are all core mechanics present? | Yes: platforming/route viability, shadow/cover/seen, watchers/attention, fixed dangers, time cycle, attempt/reset, Moon Pool, bulbs. |
| Are supporting mechanics present as Tier 2 only? | Yes: loose tile, cat event, hidden places. |
| Are extra mechanics absent? | Yes. Tier 3 is tuning only. |
| Are the listed content parts present? | Yes: rain barrel, gutters, open gutters, windowsill, wire, awnings, greenhouse glass frame, greenhouse hatch, pool grate, heron, cat, drains, lamps, broken glass, fans, wet ledges, shadow, yard, watchers, night, first light. |
| Are forbidden systems excluded? | No health, armor, damage state, combat, story characters, survival, roguelike, vehicles, building, random cat, next crossing. |
| Is the game one crossing only? | Yes. Completion and failure return to the same start. |
| Are numbers concrete? | Yes: world, player, physics, timers, rectangles, schedules, visibility, pool, bulbs. |
| Is the cat deterministic? | Yes. Trigger and cycle are fixed. |
| Is the Moon Pool failure immediate at closure? | Yes. `night.time >= 120` fails attempt. |
| Are bulbs optional for completion? | Yes. Completion works with any bulb count. |
| Is set completion only shown on success? | Yes. Completion screen shows boolean. |
| Is real-time implemented? | Yes. Fixed 60Hz real-time simulation. |
| Is side-on 2D camera following the frog? | Yes. Camera follows player with deadzone and clamping. |
| Are visuals and audio present from Tier 1? | Yes. Tier 1 includes art recipe, HUD, synthesized audio. |
| Are tests tied to tiers? | Yes. Tier 1 and Tier 2 tests are separated. |
| Did I fix any inconsistency? | Yes. Chose exactly 5 bulbs and made `BULB_1` the loose-tile/cat trigger bulb to match the linked loose-tile and cat decisions. |
| Are lamp lights both fixed danger and attention? | Yes. Fixture is instant kill; light is attention. |
| Are open gutters fixed dangers? | Yes. Overlap or world bottom kills. |
| Are hidden places only using existing systems? | Yes. They are optional ledges/bulbs covered by existing attention/danger schedules. |