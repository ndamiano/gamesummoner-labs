# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| “a platformer where you play as a frog” | 1.1, 4. Platforming, 5. Characters |
| Game name: **Bullfrog Crossing** | 7. UX, title screen |
| Room-based 2D platformer | 1.1, 2.1, 2.2, 4. Level content |
| Side-on 2D platformer view | 1.1, 3. Visual Spec, 4. Camera |
| Camera follows the frog within one room at a time | 4. Camera |
| Rooms are discrete connected spaces, not an open world | 4. Level content, 4. Room progression |
| Real-time continuous platforming, no turn system | 1.1, 1.2, 4. Platforming |
| Run starts at the opening room’s start edge | 4. Room progression, 4. Level content |
| Rooms are crossed in the named order: opening greenhouse, flooded potting bench, broken fountain, root-choked greenhouse, abandoned children’s pond | 4. Level content, 4. Room progression |
| A room is completed when the frog reaches its exit edge | 4. Room progression |
| Exit opens the next connected room | 4. Room progression |
| Run ends when the frog exits the abandoned children’s pond | 4. Room progression, 7. UX |
| Failure does not end the run | 4. Hazards, 7. UX |
| The frog returns to the last safe edge after failure | 4. Hazards, 4. Platforming |
| Completed rooms remain completed | 4. Room progression, 2.2, 4. Scoring |
| Player may replay completed rooms to improve recorded scores | 4. Scoring, 7. UX |
| Difficulty increases as later rooms become longer, darker, wetter, more connected, more densely arranged with fixed hazards, less obvious in safe lines, and more populated with hidden moths | 4. Progression and difficulty, 3. Visual Spec |
| Tone: “particular quiet, rainy world” | 3. Visual Spec, 6. Audio, 7. UX |
| “The pleasure is finding the safe line through a dangerous place and leaving a better score than before.” | 4. Progression and difficulty, 4. Scoring |
| “The game does not fight back. It takes the rhythm away.” | 4. Hazards, 5. Characters, 6. Audio |
| Frog is “a frog that belongs in the swamp but has been displaced into a human greenhouse.” | 3. Visual Spec, 5. Characters, 7. UX summary text |
| Look: moonlit, rain-swollen, wet, dark greenhouse and swamp rooms | 3. Visual Spec |
| Materials: moonlit glass, flooded clay pots, lily pads, black moss, broken glass, still oil, pale moths | 3. Visual Spec, 4. Level content |
| Sound: quiet rain, water, glass, small platforming touches, no combat or power-up sounds | 6. Audio |
| Core mechanics: platforming and hazards | 4. Platforming, 4. Hazards |
| Platforming is the only player verb | 1.1, 4. Platforming, 7. UX |
| Safe surfaces: cracked tile edges, overturned pots, wet glass, glass shelves, flooded clay pots, lily pads, ledges, start edges, exit edges | 4. Level content, 3. Visual Spec |
| No swimming, climbing, gliding, dashing, special movement, or special powers | 0.2, 4. Platforming |
| Wet glass and flooded surfaces are ordinary platforming surfaces unless listed as hazards | 3. Visual Spec, 4. Hazards |
| If the frog leaves safe surfaces into water or void, or touches a hazard, it is returned to the last safe edge | 4. Hazards |
| Hazards are fixed, non-combat obstacles | 4. Hazards |
| Earliest hazards: shard of broken glass, slick of black moss, snapped mousetrap waiting in a leaf | 4. Hazards, 4. Level content |
| Later hazards: still pools of oil, bad edges, water in flooded basins and rooms, other fixed traps | 4. Hazards, 4. Level content |
| Hazards do not move, attack, become safe, or require combat | 4. Hazards |
| Supporting mechanic: collectibles are pale moths | 4. Collectibles |
| Moths are placed off the straight line and reachable through alternate platforming lines | 4. Level content, 4. Collectibles |
| Collecting moths does not grant abilities or change rooms | 4. Collectibles |
| Moths remain collected after failure and after completing a room | 4. Collectibles, 2.2 |
| Extra mechanic: scoring rewards clean, complete crossings | 4. Scoring |
| Base clean completed crossing score is 100 | 4. Scoring |
| Each moth collected in that room adds 10 | 4. Scoring |
| Moths collected in earlier attempts count because they persist | 4. Collectibles, 4. Scoring |
| Room stores highest clean completed crossing score | 4. Scoring, 2.2 |
| Unclean completions open the next room but do not record a score | 4. Scoring |
| Interface shows best recorded score, moths collected, and whether current attempt is clean | 7. UX |
| Content list: title, setting, start edge, no instruction, safe surfaces, hazards, moths, rooms, exit drain, narrative framing | 4. Level content, 7. UX, 3. Visual Spec |
| Left out: combat, shooter mechanics, puzzle mechanics, special powers, open world, new verbs, fighting the greenhouse, swimming, traversal powers, moving hazards, combat hazards, moth abilities, room changes from collectibles | 0.2, 4, 5, 6, 7 |

## 0.2 Decisions

| Decision | Final ruling | Why |
| --- | --- | --- |
| Game prompt: platformer where you play as a frog | Accepted exactly: a 2D side-on platformer with a small frog as the only player-controlled entity. | Direct user request. |
| Game name: **Bullfrog Crossing** | Accepted exactly. Shown on title screen and run summary. | Direct high-level decision. |
| Room-based 2D platformer | Accepted exactly. Each room is a discrete level rectangle with start and exit. | Direct high-level decision. |
| Side-on 2D view | Accepted exactly. Canvas is 960×540 viewport. | Direct high-level decision. |
| Camera follows frog within one room | Accepted exactly. Camera clamps to room bounds and follows the frog. | Direct high-level decision. |
| Rooms are discrete connected spaces | Accepted exactly. No open-world map, no seamless world. | Direct high-level decision. |
| Real-time continuous platforming | Accepted exactly. Fixed-step 60 Hz simulation. | Direct high-level decision. |
| Run starts with frog on cracked tile edge at opening room’s start edge | Accepted exactly. `room1_opening_greenhouse` start safe surface is a cracked tile edge. | Direct high-level decision. |
| No instruction except the shape of the next safe surface | Accepted exactly. During gameplay there is no tutorial text, arrows, or objective text. UI screens may have minimal system text only. | Direct high-level decision. |
| Room order: opening greenhouse, flooded potting bench, broken fountain, root-choked greenhouse, abandoned children’s pond | Accepted exactly. IDs: `room1_opening_greenhouse`, `room2_flooded_potting_bench`, `room3_broken_fountain`, `room4_root_choked_greenhouse`, `room5_abandoned_childrens_pond`. | Direct high-level decision. |
| Room completed when frog reaches exit edge | Accepted exactly. Exit trigger overlaps the right side of the final safe edge. | Direct high-level decision. |
| Exit opens next connected room | Accepted exactly. In normal run mode, room completion transitions to the next room. | Direct high-level decision. |
| Run ends when frog exits abandoned children’s pond | Accepted exactly. Final room completion enters run summary. | Direct high-level decision. |
| Failure does not end the run | Accepted exactly. Hazard/fall resets position only; no game over. | Direct high-level decision. |
| Frog returns to last safe edge after hazard/fall | Accepted exactly. Last safe edge is the last safe surface the frog stood on before the failed move. If none, use room start edge. | Direct high-level decision; “last grounded safe surface” is the only deterministic interpretation that matches “standing on before the failed move.” |
| Completed rooms remain completed | Accepted exactly. `run.completedRooms[roomId] = true` persists. | Direct high-level decision. |
| Player may replay completed rooms to improve recorded scores | Accepted exactly. Room select screen lists completed rooms; replay mode returns to summary on completion. | Direct high-level decision. |
| Difficulty increases: longer, darker, wetter, more connected, denser hazards, less obvious safe lines, more hidden moths | Accepted exactly. Implemented by room width, hazard count, water hazard count, visual darkness/rain alpha, alternate-line complexity, and moth count. | Direct high-level decision. |
| Tone: quiet, rainy world | Accepted exactly. No combat, no death, no aggressive feedback. Hazard reset is a quiet rhythm loss. | Direct high-level decision. |
| “The game does not fight back. It takes the rhythm away.” | Accepted exactly. Hazards do not kill, damage, score-penalize, or punish with UI scolding. They only reset position and mark attempt unclean. | Direct high-level decision. |
| Frog belongs in swamp but displaced into human greenhouse | Accepted exactly. Narrative framing appears in title/summary only; no gameplay system changes. | Direct high-level decision. |
| Look and sound: moonlit, rain-swollen, wet, dark greenhouse and swamp rooms | Accepted exactly. Palette, rain, water, glass, moss, oil, moths all specified. | Direct high-level decision. |
| Materials: moonlit glass, flooded clay pots, lily pads, black moss, broken glass, still oil, pale moths | Accepted exactly as visual materials for safe surfaces and hazards/collectibles. | Direct high-level decision. |
| Sound: quiet rain, water, glass, small platforming touches, no combat or power-up sounds | Accepted exactly. All audio synthesized; no combat, power-up, or aggressive UI sounds. | Direct high-level decision. |
| Core mechanics: platforming and hazards | Accepted exactly as Tier 1. | Direct high-level decision. |
| Platforming is the only player verb | Accepted exactly. Input is move and jump only during gameplay. Restart/pause are UI controls, not new traversal verbs. | Direct high-level decision. |
| Safe surfaces are non-hazard platforms and edges | Accepted exactly. Safe surfaces are solid AABBs. | Direct high-level decision. |
| Safe surface types: cracked tile edges, overturned pots, wet glass, glass shelves, flooded clay pots, lily pads, ledges, start edges, exit edges | Accepted exactly. All are safe surfaces unless a hazard rectangle is placed on them. | Direct high-level decision. |
| A room is a crossing from start edge to exit edge | Accepted exactly. | Direct high-level decision. |
| No swimming, climbing, gliding, dashing, special movement, special powers | Accepted exactly. Frog has only ground move, jump, gravity, collision, and reset. | Direct high-level decision. |
| Wet glass and flooded surfaces are ordinary platforming surfaces unless listed as hazards | Accepted exactly. Visual wetness does not change physics. Only hazard rectangles cause reset. | Direct high-level decision. |
| If frog leaves safe surfaces into water/void or touches hazard, return to last safe edge | Accepted exactly. | Direct high-level decision. |
| Last safe edge means nearest non-hazard surface frog was standing on before failed move, or start edge if none | Ruled as last grounded safe surface. This is deterministic and matches “standing on before.” | Prevents ambiguous spatial “nearest” edge cases. |
| Current attempt’s unrecorded crossing progress is discarded | Ruled: after reset, position returns to last safe surface, clean attempt flag becomes false, and any progress beyond that surface is discarded. Moth collection does not reset. | Matches “last safe edge” while preserving collectible persistence. |
| Hazards are fixed, non-combat obstacles | Accepted exactly. Hazards are static rectangles. | Direct high-level decision. |
| Earliest hazards: broken glass, black moss, snapped mousetrap | Accepted exactly in Room 1. | Direct high-level decision. |
| Later hazards: oil, bad edges, water in flooded basins/rooms, other fixed traps | Accepted exactly in Rooms 2-5. | Direct high-level decision. |
| Hazards do not move, attack, become safe, or require combat | Accepted exactly. | Direct high-level decision. |
| Collectibles are pale moths | Accepted exactly as Tier 2. | Direct high-level decision. |
| Moths placed off straight line and reachable through alternate lines | Accepted exactly. Moth coordinates are above/left of hazard-bearing platforms. | Direct high-level decision. |
| Collecting moths gives no ability and does not change rooms | Accepted exactly. | Direct high-level decision. |
| Moths count toward room score | Accepted exactly in Tier 3. | Direct high-level decision. |
| Moths remain collected after failure and after completing a room | Accepted exactly. Room moth collection state persists. | Direct high-level decision. |
| Scoring rewards clean, complete crossings | Accepted exactly as Tier 3. | Direct high-level decision. |
| Crossing complete when frog reaches exit edge | Accepted exactly. | Direct high-level decision. |
| Crossing clean when no hazard touched and no fall returns frog | Ruled: any hazard reset, water reset, or void reset sets `attempt.clean = false`. | Direct high-level decision. |
| Base clean completed crossing score is 100 | Accepted exactly. | Direct high-level decision. |
| Each moth collected in that room adds 10 | Accepted exactly. | Direct high-level decision. |
| Moths collected in earlier attempts count | Accepted exactly. Room moth collection state persists across attempts. | Direct high-level decision. |
| Room stores highest clean completed score | Accepted exactly. | Direct high-level decision. |
| Unclean completions open next room but do not record score | Accepted exactly. | Direct high-level decision. |
| Interface shows best recorded score, moths collected, current clean status | Accepted exactly in Tier 3. | Direct high-level decision. |
| Title: **Bullfrog Crossing** | Accepted exactly. | Direct high-level decision. |
| “rain-swollen greenhouse after closing” | Accepted exactly as title/room visual framing. | Direct high-level decision. |
| “small frog sitting on a cracked tile edge” | Accepted exactly as start edge and title visual. | Direct high-level decision. |
| “no instruction except the shape of the next safe surface” | Accepted exactly. No in-game instruction text. | Direct high-level decision. |
| “overturned pots, wet glass, and lily pads floating in a flooded basin” | Accepted exactly as Room 1 safe surfaces. | Direct high-level decision. |
| “glass shelves” | Accepted exactly as safe surfaces in later rooms. | Direct high-level decision. |
| “shard of broken glass”, “slick of black moss”, “snapped mousetrap waiting in a leaf” | Accepted exactly as Room 1 hazards. | Direct high-level decision. |
| “still pools of oil” | Accepted exactly as hazard type. | Direct high-level decision. |
| “bad edges” and “small traps” | Ruled as `badEdge` thin hazard rectangles and `mousetrap` small trap hazard. | Makes the content list concrete without adding moving systems. |
| “pale moth behind a pot” | Accepted exactly as Room 1 first collectible. | Direct high-level decision. |
| “pale moths” | Accepted exactly as collectibles. | Direct high-level decision. |
| “moonlit glass” | Accepted exactly as visual material for glass surfaces and atmosphere. | Direct high-level decision. |
| “flooded clay pots” | Accepted exactly as safe pot platforms with water hazards around/under them. | Direct high-level decision. |
| “lily pads in a greenhouse basin” | Accepted exactly as safe floating platforms over water hazards. | Direct high-level decision. |
| “flooded basin” | Accepted exactly as water hazard area. | Direct high-level decision. |
| “connected swamp rooms: flooded potting bench, broken fountain, root-choked greenhouse, abandoned children’s pond” | Accepted exactly as Rooms 2-5. | Direct high-level decision. |
| “drain at the end of the opening greenhouse” | Accepted exactly as Room 1 exit trigger. | Direct high-level decision. |
| “frog that belongs in the swamp but has been displaced into a human greenhouse” | Accepted exactly as title/summary framing only. | Direct high-level decision. |
| Left out: combat, shooter mechanics, puzzle mechanics, special powers, open world, new verbs, fighting greenhouse, swimming, traversal powers, moving hazards, combat hazards, moth abilities, room changes from collectibles | Accepted exactly. No such systems are specified. | Direct high-level decision. |
| Player identity | Ruled: unnamed small frog. No name, dialogue, or character progression. | Keeps focus on platforming and avoids adding narrative systems. |
| Enemies | Ruled: no enemies. Hazards are obstacles, not characters. | Left out combat; hazards are fixed obstacles. |
| Input device | Ruled: keyboard only during gameplay. UI uses pointer/keyboard. | Browser game scope; avoids adding touch as a new input system. |
| Keyboard mapping | Ruled: Left/A move left; Right/D move right; Space/W/Up jump; R restart room; Esc pause; Enter start/select. | Standard platformer mapping. |
| Canvas size | Ruled: 960×540 logical canvas, scaled to fit browser. | Fits side-on room view and leaves room height for vertical variation. |
| Room height | Ruled: 720 px. | Allows camera vertical framing while keeping one-room view. |
| Room widths | Ruled: 1700, 1900, 2100, 2300, 2500 px. | Enforces “longer” difficulty. |
| Player size | Ruled: 24×18 px collision box. | Small frog; fits level gaps. |
| Physics constants | Ruled: gravity 1800 px/s², jump velocity -650 px/s, max run speed 240 px/s, max fall 900 px/s, coyote 0.08s, jump buffer 0.12s, jump cut factor 0.45. | Produces jump height ~117 px and horizontal jump distance ~173 px, matching level gaps. |
| Level design safety limits | Ruled: platform gap ≤150 px, vertical up ≤90 px, hazard-bearing platforms leave at least 40 px safe landing on one side or 30 px on each side, platform width ≥80 px. | Makes coordinates tunable and playable. |
| Hazard placement coordinates | Ruled: hazards on platforms are placed at right edges unless otherwise noted. | Avoids impossible landing segments while preserving “on surface” hazards. |
| Coordinates are exact but tunable | Ruled: listed coordinates are the initial concrete layout; builder may adjust within safety limits only. | Provides concrete content while allowing playtest correction. |
| Last safe surface storage | Ruled: store `lastSafe.surfaceId` whenever grounded on safe surface and not overlapping hazard. | Deterministic reset. |
| Clean attempt flag | Ruled: `attempt.clean = true` on room load/restart; any hazard/water/void reset sets false; collecting moths does not affect it. | Directly matches scoring rules. |
| Room completion priority | Ruled: collision order is movement → safe collision → hazard check → collectible check → exit check. If hazard and exit overlap, hazard wins. | Prevents cheating through hazard into exit. |
| Unclean completion marks room completed | Ruled: reaching exit sets `completedRooms[roomId] = true` even if unclean. | Direct decision: unclean completion opens next room. |
| Score formula | Ruled: `score = 100 + 10 * roomState[roomId].mothsCollected` only for clean completed crossing. | Direct decision. |
| Max moths | Ruled: Room 1: 1, Room 2: 2, Room 3: 3, Room 4: 4, Room 5: 5. Total 15. | Enforces “more populated with hidden moths.” |
| Max scores | Ruled: 110, 120, 130, 140, 150 per room; total 650. | Derived from scoring formula. |
| Persistence | Ruled: `localStorage` key `bullfrog-crossing-v1`. Stores completed rooms, best scores, collected moth IDs. | Required for best scores and replay. |
| Room select | Ruled: available from pause and after run summary. Lists only completed rooms. | Required for replaying completed rooms. |
| Replay mode | Ruled: replay loads a completed room, does not advance run, and returns to summary/room select on completion. | Separates run progression from score improvement. |
| Restart current room | Ruled: `R` or pause button reloads current room with fresh clean attempt. If room already completed, mode is replay. | Provides a clean attempt without adding a new game system. |
| Camera smoothing | Ruled: target camera position lerps at rate 12/s, clamped to room bounds. No camera shake. | Quiet tone; no fighting back. |
| Audio implementation | Ruled: synthesized Web Audio API only; no external assets. | Browser game, no assets. |
| UI implementation | Ruled: game world on canvas; screens and HUD are HTML/CSS overlays. | Required by UX section. |
| Random source | Ruled: gameplay is deterministic. Visual rain uses seeded PRNG only. | Avoids gameplay randomness. |
| No time bonus | Ruled: score has no time component. Faster lines are player-chosen, not scored. | Direct scoring decision has no time bonus. |

## 0.3 Tiers

| Tier | Segment | Included | Notes |
| --- | --- | --- | --- |
| Tier 1 | Core mechanics: platforming and hazards | Player physics, safe surfaces, fixed hazards, water/void reset, last safe edge, camera, five named rooms, run progression, room completion, final run completion, base art, base audio, minimal room-progress HUD. | No moths, no score records, no clean indicator. This is the minimal complete run. |
| Tier 2 | Supporting mechanic: collectibles | Pale moths in all rooms, persistent room moth counts, moth collect sound, moth HUD count, alternate-line visibility. | Does not change platforming physics or room state. |
| Tier 3 | Extra mechanic: scoring | Clean attempt flag, clean completion recording, best score storage, score formula, current clean indicator, run summary, room select, replay mode, local persistence. | Uses Tier 2 moth counts but Tier 1 can run with zero moths. |
| Tier 4 | Optional hardening only | Debug/test polish, accessibility contrast, storage reset UI. | Not required for game completion. No new gameplay systems. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Item | Value |
| --- | --- |
| Coordinate origin | Top-left of room rectangle |
| X axis | Positive right |
| Y axis | Positive down |
| Simulation units | pixels, seconds |
| Render viewport | 960×540 logical pixels |
| Room height | 720 px |
| Room 1 width | 1700 px |
| Room 2 width | 1900 px |
| Room 3 width | 2100 px |
| Room 4 width | 2300 px |
| Room 5 width | 2500 px |
| Fixed timestep | `dt = 1 / 60` s |
| Fixed step accumulator max | 5 steps per frame |
| Render interpolation | yes, using previous and current physics state |
| Frog collision size | 24×18 px |
| Collectible collision size | 18×18 px |
| Hazard collision size | per hazard table |
| Safe surface collision | solid AABB |
| Water hazard collision | non-solid trigger AABB |
| Void trigger | outside room bounds or `player.y > room.height` |
| Collision epsilon | 0.01 px |
| Max run speed | 240 px/s |
| Ground acceleration | 2800 px/s² |
| Ground deceleration | 3200 px/s² |
| Air acceleration | 2400 px/s² |
| Air deceleration | 1600 px/s² |
| Gravity | 1800 px/s² |
| Jump velocity | -650 px/s |
| Max fall velocity | 900 px/s |
| Coyote time | 0.08 s |
| Jump buffer | 0.12 s |
| Variable jump cut | if jump released and `vy < -200`, set `vy *= 0.45` |
| Jump height full | ~117.4 px |
| Horizontal jump distance full | ~173 px |
| Level design max gap | 150 px |
| Level design max vertical up | 90 px |
| Platform minimum width | 80 px |
| Hazard-bearing platform safe landing | at least 40 px on one side or 30 px on both sides |

## 1.2 Important conventions

- Use a fixed 60 Hz simulation loop. Render may run at requestAnimationFrame rate, but gameplay only advances in fixed steps.
- Gameplay must not use unseeded randomness. Visual rain, water shimmer, and moth bobbing may use a seeded PRNG such as Mulberry32.
- No external assets. All visuals are Canvas 2D primitives or CSS. All audio is synthesized.
- No gameplay text during room play. No arrows, no tutorial, no prompts.
- All gameplay state lives in the global context described in 2.2.
- Collision order every fixed step:
  1. Apply input and physics.
  2. Move X, resolve safe surface collision.
  3. Move Y, resolve safe surface collision.
  4. Update grounded/coyote state.
  5. Check hazards and water/void. If hazard triggers, reset and stop later checks.
  6. Check collectibles if enabled.
  7. Check exit if enabled.
- If a hazard and exit overlap, hazard wins.
- If a collectible and hazard overlap, hazard wins and collectible is not collected.
- If a collectible and exit overlap, collectible is collected first, then exit triggers.
- Reset is not death. It is a quiet return to last safe edge.
- No pause during room transition except canceling to summary if requested by UI; default transition is 0.85 s.
- All coordinates in the spec are top-left rectangle coordinates: `x, y, w, h`.
- For a platform, `y` is the top surface.
- For hazards on platforms, hazard bottom should equal platform top unless noted as water/void.
- If playtesting finds an unreachable coordinate, the builder may adjust only within the listed level design safety limits. This is tuning, not redesign.

# 2. CONTRACTS

## 2.1 Module layout

| File | Responsibility |
| --- | --- |
| `index.html` | Canvas mount, HTML screens, HUD containers. |
| `css/ui.css` | CSS-only screens, HUD, summary, room select. |
| `js/main.js` | Boot, requestAnimationFrame loop, fixed-step accumulator, state dispatch. |
| `js/state.js` | Global context initialization, state machine transitions, run/room mode setup. |
| `js/input.js` | Keyboard state, input buffers, debug input hooks. |
| `js/physics.js` | Gravity, velocity integration, AABB collision, surface contact. |
| `js/player.js` | Player movement, jump, coyote, buffer, facing, animation state, last safe storage. |
| `js/levels/room_data.js` | Static room rosters: safe surfaces, hazards, collectibles, exits. |
| `js/level.js` | Load room, validate room, start edge, exit trigger, room progression. |
| `js/hazards.js` | Hazard rectangles, collision checks, water/void, reset to last safe. |
| `js/collectibles.js` | Moth state, collection, persistence, count. |
| `js/scoring.js` | Clean attempt, score calculation, best score storage, summary data. |
| `js/camera.js` | Camera follow, clamp, transition fade. |
| `js/render.js` | Canvas rendering: world, player, hazards, moths, rain, HUD canvas effects if any. |
| `js/audio.js` | Synthesized sound engine, ambient loops, event sounds. |
| `js/ui.js` | HTML screen state, HUD field binding, pause, summary, room select. |
| `js/storage.js` | Load/save/reset local storage. |
| `js/debug.js` | Debug API functions. |

## 2.2 Global context

```js
const G = {
  app: {
    now: 0,
    dt: 1 / 60,
    accumulator: 0,
    fixedSteps: 0,
    state: "boot", // boot | title | play_room | room_transition | paused | run_complete | room_select
    paused: false,
    transition: { active: false, alpha: 0, nextRoomId: null, mode: null, timer: 0 }
  },

  input: {
    left: false,
    right: false,
    jump: false,
    jumpPressed: false,
    jumpReleased: false,
    restart: false,
    pause: false,
    select: false,
    pointer: { x: 0, y: 0, down: false }
  },

  run: {
    currentRoomIndex: 0,
    currentRoomId: null,
    mode: "progress", // progress | replay
    completedRooms: {}, // roomId -> true
    startedAt: 0,
    finished: false
  },

  room: {
    id: null,
    name: null,
    width: 0,
    height: 720,
    safeSurfaces: [], // {id, type, x, y, w, h}
    hazards: [], // {id, type, x, y, w, h}
    collectibles: [], // {id, x, y, w, h}
    exit: {id, x, y, w, h},
    startSurfaceId: null,
    finalSurfaceId: null
  },

  player: {
    x: 0,
    y: 0,
    vx: 0,
    vy: 0,
    w: 24,
    h: 18,
    grounded: false,
    facing: 1, // 1 right, -1 left
    coyoteTimer: 0,
    jumpBufferTimer: 0,
    jumpCutAvailable: false,
    animation: "idle", // idle | run | jump | fall | land | reset
    animationTimer: 0,
    squash: 0,
    stretch: 0,
    enabled: true
  },

  lastSafe: {
    surfaceId: null,
    x: 0,
    y: 0
  },

  attempt: {
    clean: true,
    resets: 0,
    startedAt: 0
  },

  collectibles: {
    enabled: false, // Tier 2
    collected: {}, // collectibleId -> true
    roomCount: 0
  },

  scoring: {
    enabled: false, // Tier 3
    roomStates: {
      // roomId: {
      //   completed: false,
      //   bestScore: null,
      //   mothsCollected: 0,
      //   collectedMothIds: []
      // }
    }
  },

  camera: {
    x: 0,
    y: 0,
    targetX: 0,
    targetY: 0,
    lerp: 12
  },

  render: {
    seed: 12345,
    rainAlpha: 0.08,
    darkness: 0.0,
    waterShimmer: 0,
    particles: []
  },

  ui: {
    screens: {},
    hud: {
      roomIndex: 0,
      roomName: "",
      bestScore: null,
      mothsCollected: 0,
      mothMax: 0,
      clean: true,
      resetFlash: 0
    },
    selectedRoomId: null
  },

  audio: {
    ready: false,
    masterGain: 0.7,
    rainGain: 0.25,
    waterGain: 0.18,
    sfxGain: 0.5
  }
};
```

Required global records:

| Record | Fields |
| --- | --- |
| Player | `x`, `y`, `vx`, `vy`, `w`, `h`, `grounded`, `facing`, `coyoteTimer`, `jumpBufferTimer`, `jumpCutAvailable`, `animation`, `enabled` |
| Last safe | `surfaceId`, `x`, `y` |
| Attempt | `clean`, `resets` |
| Room | `id`, `width`, `height`, `safeSurfaces`, `hazards`, `collectibles`, `exit`, `startSurfaceId`, `finalSurfaceId` |
| Run | `currentRoomIndex`, `currentRoomId`, `mode`, `completedRooms`, `finished` |
| Collectibles | `enabled`, `collected`, `roomCount` |
| Scoring | `enabled`, `roomStates` |
| Camera | `x`, `y`, `targetX`, `targetY`, `lerp` |
| Input | `left`, `right`, `jump`, `restart`, `pause` |
| UI HUD | `roomIndex`, `bestScore`, `mothsCollected`, `mothMax`, `clean`, `resetFlash` |

## 2.3 Module specifics

| Module | Required functions | Contract |
| --- | --- | --- |
| `main.js` | `boot()`, `loop(timestamp)`, `updateFixed(dt)`, `render()` | Runs fixed-step simulation, renders interpolated state. |
| `input.js` | `initInput()`, `setKey(key, value)`, `clearInput()`, `consumeJump()`, `debugInput(name, value)` | Only maps allowed inputs. No gameplay actions beyond move/jump/restart/pause. |
| `physics.js` | `applyGravity(dt)`, `integrate(dt)`, `moveX(dt)`, `moveY(dt)`, `resolveSafeCollision(player, surface)`, `clampVelocity()` | Uses AABB collision and constants from 1.1. |
| `player.js` | `updatePlayer(dt)`, `tryJump()`, `setFacing()`, `setLastSafe(surface)`, `resetToLastSafe()`, `setAnimation()` | Stores last grounded safe surface. Reset places player on top center of last safe surface or start edge. |
| `level.js` | `loadRoom(roomId, mode)`, `startRoom(roomId, mode)`, `completeRoom()`, `nextRoom()`, `validateRoom(roomData)` | Loads exact room roster. Completion sets `completedRooms[roomId] = true`. Progress mode advances; replay returns to summary. |
| `hazards.js` | `checkHazards()`, `checkWaterOrVoid()`, `markAttemptUnclean()`, `triggerReset()` | Any hazard/water/void triggers reset and clean=false. |
| `collectibles.js` | `checkCollectibles()`, `collect(id)`, `isCollected(id)`, `getRoomCount()`, `persistRoom(id)` | Enabled only Tier 2. Collection updates `G.collectibles.collected` and `G.scoring.roomStates`. |
| `scoring.js` | `isAttemptClean()`, `markAttemptUnclean()`, `recordCleanCompletion(roomId)`, `calculateScore(roomId)`, `bestScore(roomId)`, `summaryData()` | Enabled only Tier 3. Score formula: `100 + 10 * mothsCollected`. |
| `camera.js` | `updateCamera(dt)`, `clampCamera()`, `startTransition(roomId, mode)`, `updateTransition(dt)` | Camera clamps to room bounds. Transition fades and loads next room. |
| `render.js` | `renderWorld()`, `drawRoom()`, `drawSafeSurfaces()`, `drawHazards()`, `drawMoths()`, `drawPlayer()`, `drawRain()`, `drawHUDCanvasEffects()` | Tier 1 includes all base visuals. Moths only if enabled. |
| `audio.js` | `initAudio()`, `playSfx(name)`, `startAmbient(roomId)`, `stopAmbient()`, `setMasterGain(value)` | Synthesized only. No combat/power-up sounds. |
| `ui.js` | `showState(state)`, `updateHUD()`, `showSummary()`, `showRoomSelect()`, `pause()`, `resume()`, `restartRoom()` | HTML/CSS only. HUD fields map to global records. |
| `storage.js` | `loadProgress()`, `saveProgress()`, `resetProgress()` | Stores completed rooms, best scores, collected moth IDs. |
| `debug.js` | see section 8 | Direct state access for tests. |

# 3. VISUAL SPEC

The look is a quiet, rain-swollen greenhouse at night. The player sees a dark, wet, moonlit room through a side-on window. Safe surfaces are readable because they have thin moonlit rim highlights and stable geometry. Hazards are also readable but not marked with UI: broken glass has sharp pale glints, black moss is a dark matte slick, oil pools have slow iridescent shimmer, water is deep and reflective, mousetraps are small mechanical traps, and bad edges are jagged clay or tile corners. The frog is a small dark-silhouette animal with pale moonlit eye highlights and a very slight wet sheen. Pale moths are soft, low-frequency glowing shapes that do not look like power-ups. The overall feeling is calm, damp, and particular: a displaced swamp creature crossing a human greenhouse after closing.

## Lighting and atmosphere

| Element | Rule |
| --- | --- |
| Light source | Moon from upper-right, cool pale light. |
| Global ambient | Dark blue-green; room 1 ambient 35%, room 5 ambient 22%. |
| Rim light | Safe surfaces receive 1px pale rim on top/right. Hazards receive sharper or colored highlights. |
| Rain | Vertical streaks, alpha 0.06 to 0.16, speed 520-780 px/s, wind sway ±8 px. |
| Water shimmer | Slow sine wave displacement, amplitude 1px, frequency 0.12 Hz. |
| Oil shimmer | Iridescent hue shift, saturation low, alpha 0.35. |
| Moths | Pale glow, alpha pulse 0.65-0.95, bob amplitude 3px, frequency 0.28 Hz. |
| Particles | Small splash droplets on reset, no blood, no sparks. Max 8 particles. |
| Darkness progression | Each room increases `render.darkness` by 0.07 and rain alpha by 0.02. |

## Space

| Room | Visual identity |
| --- | --- |
| Opening greenhouse | Cracked tile edges, overturned pots, wet glass, lily pads in a flooded basin, drain exit. |
| Flooded potting bench | Clay pots, bench planks, glass shelves, oil pools, water basins. |
| Broken fountain | Stone/fountain rims, broken glass, oil, water, ledges. |
| Root-choked greenhouse | Dark roots, root ledges, clay pots, glass shelves, dense water. |
| Abandoned children’s pond | Lily pads, shallow pond basins, clay pots, glass shelves, moonlit water. |

## Visual recipe table

| Game element | Visual recipe | Gameplay meaning |
| --- | --- | --- |
| Frog | Body `#38594a`, belly `#7d9a82`, eyes `#d8e6d0`, 24×18 silhouette, slight squash/stretch. | Player. |
| Safe surface | Base `#253b40`, top edge `#9bb7b4`, subtle wet highlight. | Standable. |
| Cracked tile edge | Tile gray-blue, cracks darker, rim light. | Start/exit safe edge. |
| Overturned pot | Clay `#5a4034`, rim `#86664f`, dark water stain. | Safe platform. |
| Wet glass / glass shelf | Translucent `#3e5a63`, edge `#a8c7d5`, moon glint. | Safe platform. |
| Lily pad | Leaf `#2f4b39`, vein `#4f6b52`, rim light. | Safe floating platform. |
| Flooded clay pot | Pot safe top, surrounding water hazard. | Safe top only. |
| Root ledge | Dark root `#22322d`, mossy edge, rim light. | Safe platform. |
| Broken glass hazard | Sharp triangle, pale cyan `#b8e2ff`, glint animation 0.6s. | Reset on touch. |
| Black moss hazard | Matte dark green `#17271b`, slight wet sheen. | Reset on touch. |
| Mousetrap hazard | Wood `#5b4636`, metal `#8b9aa1`, snap shape. | Reset on touch. |
| Oil pool hazard | Dark `#181a1c`, iridescent hue shift. | Reset on touch. |
| Water hazard | Deep `#0b171d`, moon reflection line. | Reset on touch/fall. |
| Bad edge hazard | Jagged clay/tile corner, sharp highlight. | Reset on touch. |
| Pale moth | `#eef5cf`, soft radial glow, slow flutter. | Collectible. |
| Exit drain | Dark circular drain or grate, subtle pale reflection. | Room completion trigger. |
| HUD | System font, low opacity, monochrome pale. | Minimal status only. |

# 4. GAMEPLAY SPEC

Bullfrog Crossing is a quiet room-based platformer. The player controls a small frog that moves and jumps across safe surfaces. Each room is a crossing from a start edge to an exit edge. Hazards are fixed and do not fight back: touching them or falling into water/void returns the frog to the last safe edge and marks the attempt unclean. The player may choose the obvious line, a faster line, or an alternate line for pale moths. Completing a room opens the next room. In later attempts, clean completed crossings record scores, and collected moths improve those scores.

## Records and rosters

| Record | Roster / values |
| --- | --- |
| Player | One small frog. No enemies. No allies. |
| Rooms | 5 rooms only, in fixed order. |
| Safe surface types | `crackedTileEdge`, `overturnedPot`, `wetGlass`, `glassShelf`, `floodedClayPot`, `lilyPad`, `ledge`, `startEdge`, `exitEdge`, `rootLedge`, `benchPlank`, `fountainRim`. |
| Hazard types | `brokenGlass`, `blackMoss`, `mousetrap`, `oilPool`, `waterBasin`, `badEdge`. |
| Collectible types | `paleMoth` only. |
| Collectible counts | Room 1: 1, Room 2: 2, Room 3: 3, Room 4: 4, Room 5: 5. Total 15. |
| Score records | Per room: `bestScore`, `mothsCollected`, `collectedMothIds`, `completed`. |
| Input actions | `left`, `right`, `jump`, `restart`, `pause`. |

## 4.1 Platforming — Tier 1

| Rule | Number / behavior |
| --- | --- |
| Player verb | Move left/right and jump. |
| Ground move target | `vx = ±240` when input held. |
| Ground acceleration | 2800 px/s² toward target. |
| Ground deceleration | 3200 px/s² when no input. |
| Air control | Air acceleration 2400 px/s², air deceleration 1600 px/s². |
| Jump initiation | Only when grounded or coyote time active. |
| Jump buffer | Pressing jump within 0.12s before landing triggers jump on landing. |
| Coyote time | Jump allowed for 0.08s after leaving safe surface. |
| Jump impulse | `vy = -650`. |
| Gravity | 1800 px/s². |
| Max fall | 900 px/s. |
| Variable jump | If jump released while rising and `vy < -200`, set `vy *= 0.45`. |
| No double jump | No air jump. |
| No dash | No horizontal impulse other than move control. |
| No swim | Water is hazard, not traversal. |
| No climb | No wall interaction. |
| Safe collision | Solid AABB. Player stops on top, sides, and bottom. |
| Last safe storage | When grounded on a safe surface and not overlapping hazard, set `lastSafe.surfaceId = surface.id`. |
| Reset placement | Place player at top center of last safe surface: `x = surface.x + surface.w/2 - player.w/2`, `y = surface.y - player.h`. If no last safe, use start edge. |

## 4.2 Hazards — Tier 1

| Hazard type | Dimensions | Behavior | Visual |
| --- | ---: | --- | --- |
| `brokenGlass` | 30×30 | AABB touch resets. | Sharp pale cyan glint. |
| `blackMoss` | 50×18 | AABB touch resets. | Matte dark slick. |
| `mousetrap` | 40×20 | AABB touch resets. | Small trap. |
| `oilPool` | 40×18 | AABB touch resets. | Dark oil with iridescence. |
| `waterBasin` | variable | Non-solid; player overlap or fall into it resets. | Deep water. |
| `badEdge` | 10×15 | AABB touch resets. | Jagged edge. |

Hazard rules:

- Hazards are static.
- Hazards do not damage, kill, attack, or move.
- Hazard touch sets `attempt.clean = false`.
- Hazard touch increments `attempt.resets`.
- Hazard touch calls `resetToLastSafe()`.
- Falling into water or void uses the same reset path.
- The current attempt’s progress after the failed move is discarded.
- Moths collected are not discarded.
- Clean flag is not restored by a reset.

## 4.3 Room progression — Tier 1

| Rule | Behavior |
| --- | --- |
| Start | Run starts at `room1_opening_greenhouse` start edge. |
| Room completion | Player overlaps exit trigger and no hazard check triggers first. |
| Completion effect | `run.completedRooms[roomId] = true`. |
| Progress mode | If not final room, transition to next room. If final room, enter `run_complete`. |
| Replay mode | Completion returns to summary/room select. It does not advance run. |
| Unclean completion | Still marks room completed and opens next room. |
| Clean completion | If Tier 3 enabled, records score. |
| Restart room | Reloads current room with `attempt.clean = true`. |
| Room select | Lists completed rooms only. |

## 4.4 Collectibles — Tier 2

| Rule | Number / behavior |
| --- | --- |
| Collectible type | `paleMoth` only. |
| Collision | 18×18 AABB, non-solid. |
| Collection condition | Player overlaps moth and no hazard triggers first. |
| Collection effect | Set `collected[mothId] = true`, increment room moth count, play soft chime. |
| Persistence | Moths remain collected after reset, after room completion, after replay. |
| Abilities | None. |
| Room changes | None. |
| Clean status | Collecting does not affect clean. |
| HUD | Shows `mothsCollected / mothMax` when Tier 2 enabled. |
| Max moths | Room 1: 1, Room 2: 2, Room 3: 3, Room 4: 4, Room 5: 5. |

## 4.5 Scoring — Tier 3

| Rule | Number / behavior |
| --- | --- |
| Clean attempt | `attempt.clean = true` on room load or restart. |
| Unclean trigger | Any hazard/water/void reset sets `attempt.clean = false`. |
| Clean completion | Completion with `attempt.clean = true`. |
| Score formula | `score = 100 + 10 * roomState.mothersCollected` |
| Record condition | Only clean completed crossings record scores. |
| Best score | `roomState.bestScore = max(bestScore, score)` |
| Unclean completion | Opens next room, marks completed, but does not record score. |
| Max scores | Room 1 110, Room 2 120, Room 3 130, Room 4 140, Room 5 150. Total 650. |
| Persistence | Store best scores and collected moth IDs in local storage. |
| HUD | Shows best score, moth count, clean indicator. |
| Time bonus | None. |

## 4.6 Camera — Tier 1

| Rule | Number / behavior |
| --- | --- |
| Target | Player center. |
| Smoothing | Lerp rate 12/s. |
| Clamp X | `0 <= camera.x <= room.width - 960` |
| Clamp Y | `0 <= camera.y <= room.height - 540` |
| Camera shake | None. |
| Transition | Fade to black/dark blue over 0.85s, load next room, fade in over 0.35s. |

## 4.7 Input — Tier 1

| Input | Action |
| --- | --- |
| Left Arrow / A | Move left. |
| Right Arrow / D | Move right. |
| Space / W / Up Arrow | Jump. |
| R | Restart current room. |
| Esc | Pause. |
| Enter | Start game or confirm UI selection. |
| Pointer | UI buttons only. |

No other gameplay inputs exist.

## 4.8 Level content — Tier 1

All coordinates are `x,y,w,h`. Safe surfaces are solid. Hazards are fixed. Collectibles are listed for Tier 2 but ignored in Tier 1.

### Room 1: Opening Greenhouse

| Field | Value |
| --- | --- |
| ID | `room1_opening_greenhouse` |
| Width | 1700 |
| Height | 720 |
| Start surface | `S0` |
| Final surface | `S8` |
| Exit trigger | `1500,540,120,160` |
| Max moths | 1 |
| Hazards | 4 |

Objects:

| ID | Type | Subtype | x,y,w,h | Notes |
| --- | --- | --- | --- | --- |
| S0 | safe | crackedTileEdge | 60,620,140,24 | Start. |
| S1 | safe | overturnedPot | 260,600,80,34 |  |
| S2 | safe | glassShelf | 400,570,140,14 | Hazard-bearing. |
| S3 | safe | lilyPad | 580,560,90,16 |  |
| S4 | safe | ledge | 720,530,100,18 | Leaf ledge. |
| S5 | safe | overturnedPot | 870,560,90,40 | Hazard-bearing. |
| S6 | safe | glassShelf | 1010,520,150,14 |  |
| S7 | safe | overturnedPot | 1210,550,90,40 |  |
| S8 | safe | crackedTileEdge | 1440,620,140,24 | Final edge. |
| H1 | hazard | brokenGlass | 510,540,30,30 | Right edge of S2. |
| H2 | hazard | blackMoss | 780,512,40,18 | Right edge of S4. |
| H3 | hazard | mousetrap | 920,540,40,20 | Right edge of S5. |
| H4 | hazard | waterBasin | 560,680,300,40 | Flooded basin. |
| C1 | collectible | paleMoth | 850,470,18,18 | Behind pot. |

### Room 2: Flooded Potting Bench

| Field | Value |
| --- | --- |
| ID | `room2_flooded_potting_bench` |
| Width | 1900 |
| Height | 720 |
| Start surface | `S0` |
| Final surface | `S9` |
| Exit trigger | `1700,520,120,160` |
| Max moths | 2 |
| Hazards | 6 |

Objects:

| ID | Type | Subtype | x,y,w,h | Notes |
| --- | --- | --- | --- | --- |
| S0 | safe | crackedTileEdge | 60,600,140,24 | Start. |
| S1 | safe | floodedClayPot | 250,580,90,40 |  |
| S2 | safe | benchPlank | 400,560,160,18 | Hazard-bearing. |
| S3 | safe | lilyPad | 620,570,100,16 |  |
| S4 | safe | floodedClayPot | 780,540,90,40 |  |
| S5 | safe | glassShelf | 920,510,150,14 | Hazard-bearing. |
| S6 | safe | lilyPad | 1120,550,100,16 |  |
| S7 | safe | floodedClayPot | 1280,580,90,40 | Hazard-bearing. |
| S8 | safe | glassShelf | 1430,540,150,14 | Hazard-bearing. |
| S9 | safe | crackedTileEdge | 1600,600,140,24 | Final edge. |
| H1 | hazard | oilPool | 520,542,40,18 | Right edge of S2. |
| H2 | hazard | waterBasin | 560,680,420,40 | Flooded basin. |
| H3 | hazard | oilPool | 1030,492,40,18 | Right edge of S5. |
| H4 | hazard | brokenGlass | 1550,510,30,30 | Right edge of S8. |
| H5 | hazard | waterBasin | 1180,680,320,40 | Flooded basin. |
| H6 | hazard | badEdge | 1360,565,10,15 | Right edge of S7. |
| C1 | collectible | paleMoth | 760,470,18,18 | Behind pot. |
| C2 | collectible | paleMoth | 1150,470,18,18 | Behind oil. |

### Room 3: Broken Fountain

| Field | Value |
| --- | --- |
| ID | `room3_broken_fountain` |
| Width | 2100 |
| Height | 720 |
| Start surface | `S0` |
| Final surface | `S11` |
| Exit trigger | `1900,500,120,160` |
| Max moths | 3 |
| Hazards | 8 |

Objects:

| ID | Type | Subtype | x,y,w,h | Notes |
| --- | --- | --- | --- | --- |
| S0 | safe | crackedTileEdge | 60,580,140,24 | Start. |
| S1 | safe | floodedClayPot | 240,560,90,40 |  |
| S2 | safe | ledge | 380,530,120,18 | Hazard-bearing. |
| S3 | safe | lilyPad | 550,550,100,16 |  |
| S4 | safe | fountainRim | 700,500,120,20 | Hazard-bearing. |
| S5 | safe | floodedClayPot | 870,520,90,40 |  |
| S6 | safe | glassShelf | 1010,490,150,14 | Hazard-bearing. |
| S7 | safe | lilyPad | 1210,530,100,16 |  |
| S8 | safe | ledge | 1370,500,120,18 | Hazard-bearing. |
| S9 | safe | floodedClayPot | 1540,540,90,40 | Hazard-bearing. |
| S10 | safe | glassShelf | 1700,510,150,14 | Hazard-bearing. |
| S11 | safe | crackedTileEdge | 1880,580,140,24 | Final edge. |
| H1 | hazard | brokenGlass | 470,500,30,30 | Right edge of S2. |
| H2 | hazard | oilPool | 780,482,40,18 | Right edge of S4. |
| H3 | hazard | waterBasin | 640,680,360,40 | Basin. |
| H4 | hazard | brokenGlass | 1130,460,30,30 | Right edge of S6. |
| H5 | hazard | oilPool | 1450,482,40,18 | Right edge of S8. |
| H6 | hazard | waterBasin | 1150,680,400,40 | Basin. |
| H7 | hazard | badEdge | 1620,525,10,15 | Right edge of S9. |
| H8 | hazard | oilPool | 1810,492,40,18 | Right edge of S10. |
| C1 | collectible | paleMoth | 760,440,18,18 | Behind fountain rim. |
| C2 | collectible | paleMoth | 1040,430,18,18 | Behind glass. |
| C3 | collectible | paleMoth | 1660,440,18,18 | Behind oil. |

### Room 4: Root-Choked Greenhouse

| Field | Value |
| --- | --- |
| ID | `room4_root_choked_greenhouse` |
| Width | 2300 |
| Height | 720 |
| Start surface | `S0` |
| Final surface | `S12` |
| Exit trigger | `2100,480,120,160` |
| Max moths | 4 |
| Hazards | 10 |

Objects:

| ID | Type | Subtype | x,y,w,h | Notes |
| --- | --- | --- | --- | --- |
| S0 | safe | crackedTileEdge | 60,560,140,24 | Start. |
| S1 | safe | rootLedge | 230,540,110,18 | Hazard-bearing. |
| S2 | safe | floodedClayPot | 390,510,90,40 | Hazard-bearing. |
| S3 | safe | lilyPad | 540,530,100,16 |  |
| S4 | safe | rootLedge | 700,490,120,18 | Hazard-bearing. |
| S5 | safe | floodedClayPot | 870,520,90,40 | Hazard-bearing. |
| S6 | safe | glassShelf | 1010,480,150,14 | Hazard-bearing. |
| S7 | safe | lilyPad | 1210,520,100,16 |  |
| S8 | safe | rootLedge | 1370,480,120,18 | Hazard-bearing. |
| S9 | safe | floodedClayPot | 1540,510,90,40 | Hazard-bearing. |
| S10 | safe | glassShelf | 1700,470,150,14 | Hazard-bearing. |
| S11 | safe | lilyPad | 1900,500,100,16 |  |
| S12 | safe | crackedTileEdge | 2040,560,140,24 | Final edge. |
| H1 | hazard | oilPool | 300,522,40,18 | Right edge of S1. |
| H2 | hazard | brokenGlass | 450,480,30,30 | Right edge of S2. |
| H3 | hazard | waterBasin | 480,680,380,40 | Flooded basin. |
| H4 | hazard | blackMoss | 770,472,50,18 | Right edge of S4. |
| H5 | hazard | oilPool | 920,502,40,18 | Right edge of S5. |
| H6 | hazard | brokenGlass | 1130,450,30,30 | Right edge of S6. |
| H7 | hazard | waterBasin | 1150,680,400,40 | Flooded basin. |
| H8 | hazard | blackMoss | 1440,462,50,18 | Right edge of S8. |
| H9 | hazard | oilPool | 1590,492,40,18 | Right edge of S9. |
| H10 | hazard | brokenGlass | 1820,440,30,30 | Right edge of S10. |
| C1 | collectible | paleMoth | 360,440,18,18 | Behind pot. |
| C2 | collectible | paleMoth | 680,420,18,18 | Behind root. |
| C3 | collectible | paleMoth | 1180,430,18,18 | Behind glass. |
| C4 | collectible | paleMoth | 1660,410,18,18 | Behind oil. |

### Room 5: Abandoned Children’s Pond

| Field | Value |
| --- | --- |
| ID | `room5_abandoned_childrens_pond` |
| Width | 2500 |
| Height | 720 |
| Start surface | `S0` |
| Final surface | `S14` |
| Exit trigger | `2300,460,120,160` |
| Max moths | 5 |
| Hazards | 12 |

Objects:

| ID | Type | Subtype | x,y,w,h | Notes |
| --- | --- | --- | --- | --- |
| S0 | safe | crackedTileEdge | 60,540,140,24 | Start. |
| S1 | safe | floodedClayPot | 230,520,90,40 | Hazard-bearing. |
| S2 | safe | lilyPad | 380,500,100,16 |  |
| S3 | safe | glassShelf | 530,480,140,14 | Hazard-bearing. |
| S4 | safe | lilyPad | 720,510,100,16 | Hazard-bearing. |
| S5 | safe | floodedClayPot | 870,480,90,40 | Hazard-bearing. |
| S6 | safe | glassShelf | 1010,450,150,14 | Hazard-bearing. |
| S7 | safe | lilyPad | 1210,490,100,16 | Hazard-bearing. |
| S8 | safe | floodedClayPot | 1370,460,90,40 | Hazard-bearing. |
| S9 | safe | glassShelf | 1510,430,150,14 | Hazard-bearing. |
| S10 | safe | lilyPad | 1710,470,100,16 |  |
| S11 | safe | floodedClayPot | 1860,450,90,40 |  |
| S12 | safe | glassShelf | 2010,420,150,14 |  |
| S13 | safe | lilyPad | 2210,460,100,16 |  |
| S14 | safe | crackedTileEdge | 2340,540,140,24 | Final edge. |
| H1 | hazard | oilPool | 280,502,40,18 | Right edge of S1. |
| H2 | hazard | waterBasin | 300,680,380,40 | Pond basin. |
| H3 | hazard | brokenGlass | 640,450,30,30 | Right edge of S3. |
| H4 | hazard | blackMoss | 770,492,50,18 | Right edge of S4. |
| H5 | hazard | oilPool | 920,462,40,18 | Right edge of S5. |
| H6 | hazard | waterBasin | 820,680,420,40 | Pond basin. |
| H7 | hazard | brokenGlass | 1130,420,30,30 | Right edge of S6. |
| H8 | hazard | oilPool | 1270,472,40,18 | Right edge of S7. |
| H9 | hazard | waterBasin | 1150,680,420,40 | Pond basin. |
| H10 | hazard | blackMoss | 1410,442,50,18 | Right edge of S8. |
| H11 | hazard | oilPool | 1620,412,40,18 | Right edge of S9. |
| H12 | hazard | waterBasin | 1500,680,420,40 | Pond basin. |
| C1 | collectible | paleMoth | 360,430,18,18 | Behind pot. |
| C2 | collectible | paleMoth | 700,410,18,18 | Behind lily. |
| C3 | collectible | paleMoth | 1180,400,18,18 | Behind oil. |
| C4 | collectible | paleMoth | 1580,380,18,18 | Above oil. |
| C5 | collectible | paleMoth | 2160,370,18,18 | Behind shelf. |

## 4.9 Progression and difficulty

| Room | Width | Hazards | Moths | Water basins | Visual darkness | Safe line readability |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Opening greenhouse | 1700 | 4 | 1 | 1 | 35% ambient | Obvious. Three obvious hazards. |
| Flooded potting bench | 1900 | 6 | 2 | 2 | 42% ambient | Oil and bad edge create false safe edges. |
| Broken fountain | 2100 | 8 | 3 | 2 | 49% ambient | More vertical routes and hidden moths. |
| Root-choked greenhouse | 2300 | 10 | 4 | 2 | 56% ambient | Dense root platforms and alternate lines. |
| Abandoned children’s pond | 2500 | 12 | 5 | 4 | 63% ambient | Wide water, many moths, less obvious safe line. |

Line types:

| Line | Player behavior |
| --- | --- |
| Obvious safe line | Move right along the main platform sequence. |
| Faster line | Skip moths and choose shorter jumps, accepting hazard risk. |
| Alternate line | Leave the straight line to reach moths above or behind hazards. |
| Clean line | A completed crossing with zero resets. |

There is no time score. Faster lines are a player choice and may help the player practice clean lines, but they do not directly increase recorded score.

## 4.10 Feel

- The frog is small but responsive.
- Jumping is a short hop, not a flight.
- Coyote time and jump buffer make the game fair without adding powers.
- Hazards do not punish with death, lives, or loud failure.
- Reset is a fade and a quiet return.
- The main feedback is rhythm: the player finds a clean line, then tries to do it better.
- Moths are quiet rewards for looking past the obvious line.

# 5. CHARACTERS

## 5.1 Player: the frog

| Attribute | Specification |
| --- | --- |
| Identity | Unnamed small frog. |
| Silhouette | Low, compact, wide-eyed. |
| Collision | 24×18. |
| Facing | Left or right. Facing follows horizontal input. |
| Gameplay states | `grounded`, `airborne`, `resetting`, `enabled`. |
| Animation states | `idle`, `run`, `jump`, `fall`, `land`, `reset`. |
| No states | No attack, hurt, power-up, swim, climb, dash. |

Animation rules:

| Animation | Motion rule |
| --- | --- |
| `idle` | Breathing scale Y 1.00 to 1.02, 1.4Hz. Eyes blink every 4-9s. |
| `run` | Body lean 3px, leg cycle 12fps, squash 0.96 on foot contact. |
| `jump` | Stretch Y 1.12, X 0.92 for 0.12s. |
| `fall` | Relax to neutral, slight X 1.05 if fast. |
| `land` | Squash Y 0.90, X 1.10 for 0.08s, recover 0.12s. |
| `reset` | Fade out 0.18s, fade in 0.22s at last safe. No death pose. |

## 5.2 Pale moths

| Attribute | Specification |
| --- | --- |
| Role | Collectible object, not a character. |
| Size | 18×18. |
| Idle motion | Bob ±3px, alpha pulse 0.65-0.95. |
| Collected state | Fade out 0.25s, no remaining object. |
| Interaction | No push, no combat, no ability. |

## 5.3 Enemies

No enemies exist. Hazards are environmental objects.

# 6. AUDIO

| Sound name | Recipe | When it plays |
| --- | --- | --- |
| `rain_ambient` | Filtered white noise, lowpass 1400Hz, slow LFO gain, occasional droplet blips 2-6kHz. | Continuous in rooms, volume scaled by room rain alpha. |
| `water_ambient` | Pink noise lowpass 450Hz + sine 55Hz at low gain + slow LFO. | Rooms with water basins, volume scaled by water area. |
| `glass_ambient` | Very sparse highpassed noise, 4-8kHz, low gain. | Glass shelf rooms, low volume. |
| `jump` | Square wave 220Hz to 120Hz, 0.07s, gain 0.25. | Player jumps. |
| `land` | Filtered noise burst 700Hz, 0.08s, low sine 90Hz, gain 0.18. | Player lands. |
| `step_soft` | Noise 900Hz, 0.03s, gain 0.06. | Running footfall, rate 6-8Hz. |
| `hazard_glass` | Highpassed noise 5kHz, short decay 0.12s, low sine 180Hz. | Touching broken glass. |
| `hazard_moss` | Low sine 70Hz, soft noise lowpass 500Hz, 0.14s. | Touching black moss. |
| `hazard_trap` | Short click 1.2kHz + wood knock 160Hz, 0.1s. | Touching mousetrap. |
| `hazard_oil` | Low filtered noise 250Hz, slow decay 0.18s. | Touching oil. |
| `hazard_water` | Filtered noise 900Hz, descending lowpass, 0.2s. | Falling into water. |
| `reset_return` | Soft sine sweep 320Hz to 260Hz, 0.22s, very low gain. | After any reset, after position restore. |
| `moth_collect` | Sine 880Hz + 1320Hz, 0.12s, soft attack, gain 0.12. | Collecting a moth. |
| `room_complete` | Sine 440Hz to 660Hz, 0.35s, low gain, no fanfare. | Reaching exit. |
| `run_complete` | Two soft bell tones 550Hz and 825Hz, 0.7s, reverb-like decay. | Completing final room. |
| `ui_select` | Sine 660Hz, 0.05s, low gain. | UI button confirm. |
| `ui_back` | Sine 440Hz, 0.05s, low gain. | UI back. |

No combat sounds, power-up sounds, enemy sounds, or aggressive failure sounds.

# 7. UX

## 7.1 Screen state machine

| State | Entry | Input | Exit |
| --- | --- | --- | --- |
| `boot` | Page load | Auto after assets ready | `title` |
| `title` | Boot complete | Enter starts run; Room Select if progress exists; Title resets to title | `play_room`, `room_select`, `title` |
| `play_room` | Room loaded | Move/jump; R restart; Esc pause; exit trigger | `play_room`, `paused`, `room_transition` |
| `paused` | Esc | Resume; Restart; Room Select; Quit | `play_room`, `room_select`, `title` |
| `room_transition` | Exit reached | None | `play_room` next room or `run_complete` |
| `run_complete` | Final room completed | Room Select; Title | `room_select`, `title` |
| `room_select` | Title, pause, or run complete | Select completed room; Back | `play_room` replay, `paused`, `run_complete`, `title` |

## 7.2 HUD table

| HUD element | Record field | When visible |
| --- | --- | --- |
| Room progress dots | `run.completedRooms`, `run.currentRoomIndex` | Always in `play_room`. Five small dots; filled for completed; current dot dim. |
| Room number | `run.currentRoomIndex + 1` | Optional debug only; not shown in normal play. |
| Best score | `scoring.roomStates[currentRoomId].bestScore` | Tier 3, in `play_room`. Shows `---` if null. |
| Moths collected | `collectibles.roomCount`, room moth max | Tier 2, in `play_room`. Shows `n/max`. |
| Clean indicator | `attempt.clean` | Tier 3, in `play_room`. Small pale dot if clean, dim dot if unclean. |
| Reset flash | `attempt.resets`, transient `ui.hud.resetFlash` | Brief dim flash after any reset, Tier 1. |
| Pause menu | `app.paused` | Tier 1. Resume, Restart, Room Select, Quit. |
| Run summary | `scoring.roomStates`, `run.completedRooms` | Tier 3, in `run_complete`. Shows room names, best scores, moth counts. |
| Room select | `run.completedRooms` | Title if progress exists, pause, run complete. Lists completed rooms only. |
| Title screen | None | `title`. Shows title, Start, Controls, optional Continue/Room Select. |

No in-room instruction text. HUD status is minimal and non-narrative.

# 8. DEBUG API

| System | Function | Direct state effect |
| --- | --- | --- |
| Input | `debugInput.left(boolean)`, `debugInput.right(boolean)`, `debugInput.jump(boolean)`, `debugInput.restart()`, `debugInput.pause()` | Sets `G.input`. |
| Player | `debugPlayer.teleport(x,y)`, `debugPlayer.setVelocity(vx,vy)`, `debugPlayer.setGrounded(boolean)`, `debugPlayer.setFacing(integer)`, `debugPlayer.resetToLastSafe()` | Mutates `G.player` and last safe behavior. |
| Platforming | `debugPhysics.setGravity(value)`, `debugPhysics.setJumpVelocity(value)` | Mutates physics constants for tests. |
| Hazards | `debugHazard.list()`, `debugHazard.forceReset()` | Reads hazard roster, forces reset path. |
| Level | `debugLevel.load(roomId, mode)`, `debugLevel.completeRoom()`, `debugLevel.nextRoom()`, `debugLevel.validate(roomId)` | Loads room, triggers completion/progression. |
| Collectibles | `debugCollectibles.collect(id)`, `debugCollectibles.setUncollected(id)`, `debugCollectibles.count(roomId)` | Mutates/read collectible state. |
| Scoring | `debugScoring.setClean(boolean)`, `debugScoring.completeClean()`, `debugScoring.completeUnclean()`, `debugScoring.setBest(roomId, score)` | Mutates/read scoring state. |
| Storage | `debugStorage.exportProgress()`, `debugStorage.resetProgress()` | Reads/clears persistence. |
| Camera | `debugCamera.set(x,y)`, `debugCamera.clamp()` | Mutates/clamps camera. |
| Audio | `debugAudio.play(name)` | Plays synthesized sound. |
| State | `debugState.set(stateName)` | Sets app state for UI tests. |

# 9. TESTS

| Tier | Test |
| --- | --- |
| Tier 1 | Fixed-step loop runs with `dt=1/60` and does not accumulate more than 5 steps. |
| Tier 1 | Left/right input accelerates to 240 px/s and stops at 3200 px/s² ground deceleration. |
| Tier 1 | Full jump reaches apex 115-120 px above launch surface. |
| Tier 1 | Coyote time allows jump within 0.08s after leaving surface; after 0.09s it does not. |
| Tier 1 | Jump buffer allows jump if pressed within 0.12s before landing. |
| Tier 1 | Safe surfaces stop player and set grounded. |
| Tier 1 | Touching any hazard sets `attempt.clean=false`, increments resets, and places player on last safe surface. |
| Tier 1 | If no previous safe surface exists, reset uses start edge. |
| Tier 1 | Falling into water/void uses the same reset path. |
| Tier 1 | Exit trigger completes room and loads next room in progress mode. |
| Tier 1 | Final room completion enters run summary state. |
| Tier 1 | Camera clamps to room bounds and follows player. |
| Tier 1 | All five rooms load without missing IDs, overlapping hazards/exit hazards, or invalid safe surfaces. |
| Tier 1 | Base visuals, rain, water, hazards, and platforming audio initialize without external assets. |
| Tier 2 | Collectibles module disabled in Tier 1; enabled in Tier 2. |
| Tier 2 | Moth collision collects once and increments room moth count. |
| Tier 2 | Moth collection persists after reset and after room completion. |
| Tier 2 | Moth collection does not change player physics, room state, or clean flag. |
| Tier 2 | HUD moth count updates correctly. |
| Tier 3 | Clean flag starts true on room load and restart. |
| Tier 3 | Any hazard/water/void reset sets clean false. |
| Tier 3 | Clean completion records `100 + 10 * mothsCollected`. |
| Tier 3 | Unclean completion marks room completed but records no score. |
| Tier 3 | Best score stores the highest clean score. |
| Tier 3 | Moths collected in previous attempts count in later clean completions. |
| Tier 3 | Summary and room select show completed rooms and best scores. |
| Tier 3 | Room select only lists completed rooms. |
| Tier 3 | Replay mode does not advance run progression. |
| Tier 3 | Progress persists after reload and can be reset via debug storage. |

# 10. BUILD ORDER

1. Create HTML/CSS shell, canvas mount, and base screen containers.
2. Implement fixed-step loop, global context, input mapping.
3. Implement player physics, AABB collision, jump, coyote, buffer, camera clamp.
4. Implement one room loader with safe surfaces, hazards, exit trigger.
5. Build Room 1 with base art and audio.
6. Implement last safe reset, water/void reset, hazard flags.
7. Implement room transition and run progression.
8. Build all five rooms with exact rosters.
9. Verify Tier 1 tests and finish Tier 1.
10. Add collectible state, moth visuals, collection persistence, HUD count.
11. Verify Tier 2 tests and finish Tier 2.
12. Add clean attempt state, scoring, best scores, summary, room select, storage.
13. Verify Tier 3 tests and finish Tier 3.
14. Optional Tier 4: debug polish, storage reset UI, contrast checks.

# 11. DEFINITION OF DONE

## Tier 1: Core platforming and hazards

High level: The player can start the run, cross all five rooms, fail and reset without ending the run, and finish the run. The game is visually and audibly complete for the core mechanics.

- [ ] Fixed 60 Hz loop exists.
- [ ] Keyboard move/jump works.
- [ ] Frog physics matches constants.
- [ ] Safe surfaces collide and are standable.
- [ ] Hazards are fixed and trigger reset.
- [ ] Water and void trigger reset.
- [ ] Last safe edge reset works deterministically.
- [ ] Camera follows and clamps to each room.
- [ ] All five named rooms load in order.
- [ ] Exit trigger completes rooms.
- [ ] Final room completes the run.
- [ ] Base visuals are present: moonlit greenhouse, rain, water, glass, pots, lily pads, moss, oil, broken glass, mousetrap, bad edge, frog.
- [ ] Base audio is present: rain, water, jump, land, hazard reset, room complete.
- [ ] Minimal room-progress HUD is visible.
- [ ] No combat, powers, moving hazards, swimming, or new verbs exist.

## Tier 2: Collectibles

High level: Pale moths are visible collectibles, persist after failure, count in HUD, and do not change gameplay.

- [ ] Moth objects render in all rooms.
- [ ] Moth counts match: 1, 2, 3, 4, 5.
- [ ] Moth collision collects once.
- [ ] Moth collection persists after reset.
- [ ] Moth collection persists after room completion.
- [ ] Moth collection does not grant abilities or alter rooms.
- [ ] HUD shows moth count.
- [ ] Moth collection sound is soft and non-combat.

## Tier 3: Scoring

High level: Clean completed crossings record scores, moths improve scores, best scores persist, and completed rooms can be replayed.

- [ ] Clean flag is false after any hazard/water/void reset.
- [ ] Clean flag is true after room load/restart.
- [ ] Clean completion calculates `100 + 10 * mothsCollected`.
- [ ] Unclean completion does not record score.
- [ ] Best score stores highest clean score.
- [ ] HUD shows best score and clean indicator.
- [ ] Run summary shows room scores and moth counts.
- [ ] Room select lists completed rooms.
- [ ] Replay mode updates scores but does not advance run.
- [ ] Progress persists in local storage.
- [ ] Debug storage reset works.

# A. SANITY

| Check | Result |
| --- | --- |
| Does the spec only include the requested systems? | Yes. Platforming, hazards, moths, scoring, rooms, camera, UI, audio. No combat, powers, open world, moving hazards, swimming, or new verbs. |
| Are core mechanics Tier 1? | Yes. Platforming and hazards are Tier 1. |
| Are supporting mechanics Tier 2? | Yes. Collectibles are Tier 2. |
| Are extra mechanics Tier 3? | Yes. Scoring is Tier 3. |
| Are all rooms included with exact order? | Yes. Five named rooms with IDs and rosters. |
| Are all safe surface types from the prompt used? | Yes: cracked tile edges, pots, wet glass, glass shelves, flooded clay pots, lily pads, ledges, start/exit edges. |
| Are all hazard types from the prompt used? | Yes: broken glass, black moss, mousetrap, oil, bad edges, water basins. |
| Are moths off-line and non-ability? | Yes. Moth coordinates are above/behind hazard lines; no abilities or room changes. |
| Does scoring match the formula? | Yes. Base 100, +10 per moth, best clean only, unclean no score. |
| Does failure return to last safe edge? | Yes. Last grounded safe surface, or start edge if none. |
| Does unclean completion open next room? | Yes. It marks completed and progresses but records no score. |
| Are later rooms longer, darker, wetter, denser, more moth-populated? | Yes. Width, hazard count, water basins, darkness, and moth counts increase. |
| Are physics constants and level coordinates compatible? | Yes. Jump height ~117px, max gap 150px, vertical up ≤90px, hazards placed on platform edges with safe landing margins. |
| Are coordinates tunable without changing design? | Yes. Builder may adjust within safety limits only. |
| Are all records present in global context? | Yes. Player, room, run, last safe, attempt, collectibles, scoring, camera, input, HUD. |
| Are tests tied to tiers? | Yes. Tier 1/2/3 tests in section 9. |
| Are audio sounds synthesized and non-combat? | Yes. All recipes synthesized; no combat or power-up sounds. |
| Are UI screens HTML/CSS only? | Yes. Game world on canvas; screens/HUD are HTML/CSS overlays. |
| Are there any enemies or moving hazards? | No. Explicitly none. |
| Are there any special traversal powers? | No. Only move and jump. |
| Is the tone preserved? | Yes. No death, no fight back, quiet reset, moonlit rain, score as quiet rhythm improvement. |