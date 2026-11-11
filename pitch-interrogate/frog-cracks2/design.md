# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Browser game: platformer where the player is a frog | §4, §5, §10 |
| Side-on 2D/2.5D platformer with low frog-scale camera, parallax layers, distant rooftop pond goal whenever possible | §3 |
| Real-time run beginning under a dripping gutter on a leaf in a rain barrel | §4, §7 |
| Frog moves right, crouch-hops in arcs, uses tongue to eat insects or grab visible anchors, sticks to damp textured surfaces, avoids/distracts hazards without combat | §4, §5, §8 |
| Clear authored places, each completed by reaching its endpoint | §4, §7 |
| Routes built from what a frog can and cannot do | §4, §5 |
| Failure is forgiving but never weightless: embarrassment, delay, forced rethink | §4, §5, §9 |
| Tone: quiet and wet; small wet frog; reading, timing, trusting the frog’s body | §3, §4, §5, §6 |
| Look: rain-soaked garden and city edge seen from ground: gutters, rain barrels, drainpipes, stone paths, greenhouse glass, dripping vines, puddles, rooftop pond, ring of lilies, faint chorus | §3, §4 |
| Sound: diegetic and wet; drips, rain, splashes, gurgling pipes, animal movement, frog calls; no HUD prompts | §6, §7 |
| Core mechanics exactly: ground states/crouch-hop, tongue/eating/anchors, sticky pads/grip, shallow water/puddles/swimming, checkpoints/reset, cat awareness, place completion, core verb availability | §4 tier 1 |
| Supporting mechanics exactly: hazard activation, weak anchors, lily pads/floatables, hollow landmarks, currents, drainpipes, sprinklers, dynamic surfaces, heron, fish | §4 tier 2 |
| Extra mechanics exactly: wind zones, wasp puff, multi-route traversal | §4 tier 3 |
| Concrete content: who the player is, enemies, traps, pickups, numbers | §4, §5, §6 |
| Rules of every system with numbers | §4 |
| Input drives game | §4, §8 |
| Run structure | §0.3, §4 |
| Visuals/audio within chosen style | §3, §6 |
| Engineering contracts | §2 |
| No added systems outside decisions | §0.2, §A |
| No death screen, no score, no collectathon, no survival meters, no combat, no locked doors/switches, no random hazards, no HUD prompts | §0.2, §4, §7 |
| No running, walking, sliding, crawling on ordinary ground; no air steering/braking/second push/aim change | §4 tier 1 |
| No jumping from deep still water; no slide upward on walls; no release-to-swing; no insects as anchors; no wasp aim | §4 |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| Play as a frog | Player is a small wet frog with frog-only verbs: crouch-hop, tongue, sticky pads, swim/paddle/haul. No human movement verbs. | Preserves the requested body and scale language. |
| No running/walking/sliding/crawling on ordinary ground | Ground only supports standing, aiming/facing, crouch-charging, launching. | Makes traversal about arcs and reading distances. |
| Airborne is ballistic | No air steering, braking, second push, or aim change while airborne. Exceptions: tongue catch, wind, current, wasp impulse. | Failure comes from committed crouch-hop arcs. |
| Crouch-hop is hold-and-release | Tap crouch gives minimal hop; hold crouch gives longer aimed arc to fixed cap. Facing/aim changes launch direction but not movement. | Core verb is legible, physical, and forgiving. |
| Tongue is one held action | Quick tap = snap/eat. Hold = extension/anchor attachment. Short snap cannot stick. Held extension cannot eat. | Prevents mode confusion and keeps one verb. |
| Tongue catches visible anchors and edible insects only | Anchors are authored, visible, and tagged. Insects are never anchors. | Physical tags are the rule. |
| Clean miss has no dangle | If tongue misses, it does not attach and does not constrain the frog. | Keeps failure clean and avoids accidental rescue. |
| Release detaches and keeps momentum | While attached, holding input pulls/swings. Releasing removes the constraint and preserves velocity. | Makes swinging intentional and commit-based. |
| Sticky pads grip only damp textured porous surfaces | Bark, moss, wet wood, rough stone, damp concrete grip. Glass, smooth metal with condensation, dry/dusty/oily/glazed surfaces do not. | Creates clear visual rules and non-grip hazards. |
| Wall climb is timed small hops/crawls | No upward slide. Holding toward wall maintains cling; crouch taps move up small increments. | Keeps wall movement frog-like and deliberate. |
| Puddles are platforms only when bottom or authored floatable is support | Water surface itself is not a platform. | Maintains scale language and physical clarity. |
| Deep still water cannot be jumped from | Frog can paddle poorly and haul out on authored edges. Strong water pushes it. | Prevents water from becoming generic jump pad. |
| Last safe perch is authored and recent | It is a stable perch where frog stood safely for 0.75s, not nearest random object. | Forgiving but not weightless. |
| Reset restores checkpoint state | Dynamic changes after checkpoint are undone unless they became part of a newer safe perch. | Prevents soft locks and keeps routes readable. |
| Cat awareness is line-of-sight plus movement/noise | Stillness and cover reduce attention. Notice, approach, swat, cooldown. No combat. | Teaches stillness and reading attention. |
| Place completion is endpoint reach only | No collecting, switches, hidden objectives. | Keeps authored places focused on traversal. |
| All core verbs available from start | Teaching moments are authored entities, not unlocks. | Avoids hidden systems and keeps player agency. |
| Hazards are physical systems, not dice | Activation comes from visible physical thresholds: pressure, patrol line, weight, splash, water level. | No invisible randomness. |
| Weak anchors are authored and visually cued | Cracked/frayed/waterlogged/loose/special sway. Allowed slip/break/move. | Adds risk and route reading without unfairness. |
| Lily pads/floatables are buoyant, load-sensitive platforms | They drift, tilt, sink, capsize, or become temporary platforms when lodged. | Water becomes a physical space, not decorative. |
| Hollow landmarks are real interiors | Frog can enter through authored openings and exit through authored openings. | Uses scale language: barrels, cans, pipes. |
| Currents are authored directional water fields | Strong flow carries frog unless edge/anchor reached. Weak flow can be fought. | Water is traversal and hazard. |
| Drainpipes gurgle/spit | Pressure builds visibly, then pulse wets, pushes, clears, or creates current. | Physical hazard telegraph. |
| Sprinklers wet surfaces and push objects | Smooth surfaces become slick; porous surfaces only damp unless washed away. | Creates route-changing wetness. |
| Dynamic surfaces have stress cues | Leaves bend/sink, barrels tip, crumbling ledges crack/break. | Risk is readable and resettable. |
| Heron hunts open sight | Shadow telegraphs target. Stillness/cover/wall/outside sight avoids snap. | Open ground becomes dangerous without combat. |
| Fish lurks in ponds and strikes water entry/splash/movement | Ripples, bubbles, disturbed pads, shape under surface telegraph. | Water hazard is legible. |
| Wind zones are authored horizontal force zones | Shown by flags, plants, rain, dust, ripples, audio. | Rooftops have physical risk. |
| Wasp puff is forced and unaimed | Eating wasp causes one authored sideways impulse/hop. | Puzzle use without aiming. |
| Multi-route traversal is level design, not a separate menu | Direct dangerous and longer safer routes use verbs and physical consequences. | The world is made of consequences, not locks. |
| No HUD prompts | No in-game HUD, counters, objective text, prompts, or meters. | Tone is quiet and diegetic. |
| No death screen | Reset is a short embarrassed cough/reset at last safe perch. | Failure is delay and rethink. |
| No score/collect | Flies are not coins. Eating has no counter. | Not a collectathon. |
| No combat | Hazards reset or distract; no defeating enemies. | Frog finds a way, not fights. |
| No open world | Authored places with endpoints. | Clear crafted places. |
| No locked doors/switches/abstract puzzle machines | Hazards are physical thresholds. | World feels wet and real. |
| Tier 1 is core mechanics only | Support/extra mechanics are later tiers. | Guaranteed playable core. |
| Tier 1 has art/sound/juice | Tier 1 is already drawn, animated, and heard. | Polish is not deferred. |
| Tier 1 minimal run reaches final rooftop pond | Short teaching run: rain barrel, damp wall, branch/cat, final pond. | Player can finish core game. |
| Full run inserts supporting/extra places before final | Tier 2/3 expand between branch/cat and final pond. | Later stops teaching and starts trusting. |
| Units are meters and seconds | 1m = 100px logical. | Stable physics numbers. |
| Fixed timestep 1/60s | All gameplay deterministic. | Tests and reproducibility. |
| No random gameplay source | All cycles/patrols authored deterministic. | No invisible randomness. |
| Input: keyboard only | Aim with arrows/A/D/W, crouch with down/S/Shift, tongue with Space/J. | One held tongue action, no mouse complexity. |
| Title/complete screens are HTML/CSS overlays | No gameplay HUD. | Required UX without HUD prompts. |
| Camera is low and follows frog with clamps | Never shows empty void; keeps goal visible when possible. | Frog-scale and goal visibility. |
| Audio is synthesized | Table in §6. | Builder can produce sounds without assets. |
| Reset uses snapshots | Dynamic state restored from last safe perch. | No permanent broken world. |
| Cat/heron/fish reset frog | No damage/death. | Embarrassment/delay. |
| Wasps only affect traversal where authored | Eating elsewhere is just eaten. | No generic traversal effects. |
| Final completion is joining chorus | Game ends at rooftop pond endpoint. | No post-goal collect. |

## 0.3 Tiers

Priority list. Tier 1 must be complete and finishable. Higher tiers may be left unbuilt.

| Tier | Segment | Must include | Notes |
| --- | --- | --- | --- |
| 1 | Core frog run | Places: `rain_barrel_leaf`, `damp_wall_puddle`, `branch_cat`, final `rooftop_pond`. Core mechanics: ground/crouch-hop, tongue/eat/anchor, sticky pads, shallow/deep water, checkpoints/reset, cat, place completion, all verbs available. Full art, audio, reset, title/complete. | Minimal viable game. No heron/fish/lily/current/sprinkler/wind/wasp. |
| 2 | Supporting garden systems | Places: `koi_pond_lilies`, `greenhouse_sprinkler`, `drainpipe_currents`. Systems: hazard activation, weak anchors, lily pads/floatables, hollow landmarks, currents, drainpipes, sprinklers, dynamic surfaces, heron, fish. | Inserts before final. Each system complete on top of tier 1. |
| 3 | Extra rooftop trust | Place: `gutter_wind_final`. Systems: wind zones, wasp puff, multi-route traversal. Expanded final approach with direct dangerous vs longer safe routes. | Stops teaching and starts trusting. |
| 4 | Full run integration | Full place chain `rain_barrel_leaf → damp_wall_puddle → branch_cat → koi_pond_lilies → greenhouse_sprinkler → drainpipe_currents → gutter_wind_final → rooftop_pond`. All tiers integrated. | Only if tiers 2-3 built. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Item | Value |
| --- | --- |
| World units | meters |
| Render scale | 1m = 100px |
| Logical canvas | 960x540px = 9.6m x 5.4m |
| Coordinate axes | x right, y up |
| Fixed timestep | 1/60s = 0.0166667s |
| Max catch-up fixed steps | 4 per frame |
| Interpolation | render only; gameplay state not interpolated by physics |
| Gravity | -20.0 m/s² |
| Terminal fall speed | -18.0 m/s |
| Collision epsilon | 0.01m |
| Frog collision box | 0.28m wide, 0.18m tall |
| Frog origin | center bottom of collision box |
| Frog visual height | 0.22m including head, 0.18m collision height |
| Mouth point | front edge +0.16m from center, y +0.03m |
| Eye points | y +0.14m, x ±0.05m |
| Anchor hit radius | 0.12m |
| Insect edible radius | 0.07m for flies/wasps, 0.08m for beetles |
| Surface bounds | AABBs with normal side |
| Water surface | horizontal y line; bottom y line for deep water |
| Safe perch box | minimum 0.35m x 0.18m |
| Endpoint trigger | 0.5m x 0.5m or perch with `endpoint:true` |
| Angles | degrees, 0 horizontal right, 90 up, negative not used for launch |
| Aim angles available | 0, 45, 90, and mirrored left |
| Default facing | right toward goal |
| Max crouch launch speed | 8.0 m/s |
| Min crouch launch speed | 3.0 m/s |
| Max crouch charge time | 0.90s |
| Tap crouch threshold | press duration < 0.10s |
| Max jump height | 1.60m at 90° with max charge |
| Max horizontal jump range | 3.20m at 45° with max charge |
| Wall climb step | +0.25m per successful pad contact |
| Wall climb cooldown | 0.22s |
| Slippery slide max | 2.2 m/s |
| Water paddle speed | 0.55 m/s |
| Haul edge distance | 0.35m |
| Haul time | 0.35s |
| Cat notice threshold | attention 0.65 |
| Cat attention decay | 0.45/s when hidden/still |
| Cat approach speed | 1.4 m/s |
| Cat swat distance | 1.6m |
| Cat swat exposure time | 1.0s |
| Cat cooldown | 5.0s |
| Heron snap delay | 0.6s after movement/splash in sight |
| Heron attention shift after disturbance | 3.0s |
| Fish strike radius | 0.9m |
| Fish dunk time | 0.8s |
| Fish cooldown | 3.0s |
| Weak anchor slip time | 3.0s under load |
| Weak anchor break time | 4.5s under load |
| Lily pad capsize angle | 25° |
| Current strong flow | >0.7 m/s |
| Current weak flow | <=0.5 m/s |
| Drainpipe spit duration | 0.35s |
| Drainpipe spit radius | 1.2m |
| Drainpipe spit impulse | 3.0 m/s |
| Sprinkler active | 4.0s |
| Sprinkler idle | 9.0s |
| Sprinkler cone | 55° |
| Sprinkler range | 4.5m |
| Wind gust strength | 4.0 m/s horizontal acceleration |
| Wind calm | 8.0s |
| Wind gust | 1.8s |
| Wasp puff grounded impulse | 2.2 m/s sideways |
| Wasp puff airborne impulse | 1.6 m/s sideways for 0.15s |
| Place transition fade | 0.4s |
| Reset cough animation | 0.8s |
| Safe perch confirmation | 0.75s grounded on perch |

## 1.2 Important conventions

| Rule | Implementation |
| --- | --- |
| Fixed step loop | `while accumulator >= dt: update(dt)`. Render outside. |
| No random gameplay | No `Math.random()` in gameplay, physics, hazards, animals, insects, or level state. Use authored paths and timers. |
| Deterministic audio | Ambient audio may use fixed noise filters and authored patterns, not random gameplay events. |
| All verbs available from start | No unlock flags for crouch-hop, tongue, sticky pads, water. |
| Input does not move frog on ordinary ground | Aim keys change facing/aim only. |
| Airborne no control | Airborne ignores aim/crouch except tongue, wind, current, wasp impulse. |
| No HUD | No HUD elements in gameplay. Title/complete overlays only. |
| No counters | No score, collect count, timer, objective counter, completion percentage. |
| No combat | Hazards reset/distract; no health, damage, defeat. |
| Reset is not death | Short reset animation, no death screen. |
| Place completion = endpoint trigger | No hidden goals. |
| Surface tags are authoritative | Gripability, slipperiness, wetness are data fields. |
| Anchor tags are authoritative | Stable/weak/edible are data fields. |
| Insects are not anchors | Insect records cannot have `anchor:true`. |
| Weak anchors are authored | Placed in level data, never random. |
| Dynamic state snapshots | Checkpoints store dynamic object states. Reset restores snapshot. |
| No permanent broken world | All breakable/tilted/eaten state re-forms on reset. |
| No soft lock | If no reachable safe perch, place opening perch or nearest authored safe bank is used. |
| Camera clamps | Keep authored space visible; do not show empty void. |
| Goal visibility | Background parallax includes rooftop pond shape in all outdoor places where possible. |
| Place transitions | Fade only; no menu. |
| Tests use debug API | Do not rely on pixels or screenshots. |

# 2. CONTRACTS

## 2.1 Module layout

| Module | Responsibility |
| --- | --- |
| `index.html` | Canvas, title/complete overlay containers, script tag. |
| `styles.css` | Full-page canvas, overlay state machine, no gameplay HUD. |
| `main.js` | Bootstrap, fixed step loop, render loop, state machine bridge. |
| `input.js` | Keyboard state, press/release, tap/hold detection, debug input. |
| `state.js` | Game state, snapshots, reset, place transition state. |
| `world.js` | World records, place loading, entity registries. |
| `places.js` | Place chain, endpoints, completion, next place. |
| `physics.js` | AABB collision, raycasts, rope constraint, force integration. |
| `frog.js` | Frog states, crouch-hop, aiming, clinging, swimming, reset. |
| `tongue.js` | Quick snap, held extension, eating, anchor attachment, pull/swing. |
| `surfaces.js` | Surface tags, grip, slip, climb, wetness. |
| `water.js` | Water volumes, shallow/deep, paddle, haul, splash. |
| `checkpoints.js` | Safe perch detection, snapshot, reset. |
| `cat.js` | Cat awareness, approach, swat, cooldown. |
| `heron.js` | Heron sight, shadow, snap, attention shift. |
| `fish.js` | Fish lurk, strike, dunk, spit. |
| `hazards.js` | Generic physical threshold state machine. |
| `anchors.js` | Stable/weak anchor stress, slip/break/move. |
| `floatables.js` | Lily pads, leaves, corks, lids, buoyancy, capsize. |
| `hollows.js` | Barrel/drainpipe/tin can/cat door interiors and exits. |
| `currents.js` | Flow fields, swim strength, carrying. |
| `sprinkler.js` | Sprinkler cycles, wet surfaces, object push. |
| `drainpipe.js` | Pressure, gurgle, spit. |
| `dynamic.js` | Leaves, barrels, crumbling ledges. |
| `wind.js` | Wind zones, gusts, cues. |
| `wasp.js` | Wasp eating, puff impulse. |
| `insects.js` | Flies, wasps, beetles paths, eaten state. |
| `audio.js` | Synthesized sound registry and playback. |
| `render.js` | Parallax, camera, character rendering, visual cues. |
| `ui.js` | Title, Playing, Completed state machine. |
| `debug.js` | Direct state access and input functions for tests. |
| `tests.js` | High-level tests per tier. |

## 2.2 Global context

```js
const ctx = {
  time: {
    fixedStep: 0.0166667,
    accumulator: 0,
    frame: 0,
    gameClock: 0,
    running: false,
    screen: "title" // title | playing | completed
  },
  input: {
    keys: {},
    crouch: {
      down: false,
      pressTime: 0,
      releaseTime: 0,
      bufferedRelease: false
    },
    tongue: {
      down: false,
      pressTime: 0,
      releaseTime: 0,
      bufferedPress: false
    },
    aim: {
      left: false,
      right: false,
      up: false,
      down: false
    }
  },
  player: {
    id: "frog",
    position: { x: 0, y: 0 },
    velocity: { x: 0, y: 0 },
    size: { w: 0.28, h: 0.18 },
    state: "idle", // idle, crouch, charging, airborne, tongue_snap, tongue_hold, attached, cling, climb, slide, water, paddle, haul, reset, completed
    facing: 1, // 1 right, -1 left
    aimAngle: 0,
    grounded: false,
    groundedSurface: null,
    clinging: false,
    clingingSurface: null,
    attached: false,
    attachedAnchor: null,
    tongue: {
      active: false,
      mode: "none", // none, quick, held
      progress: 0,
      length: 0,
      tip: { x: 0, y: 0 },
      attached: false,
      ropeLength: 0,
      cooldown: 0
    },
    crouch: {
      active: false,
      charge: 0,
      maxCharge: 0.9
    },
    water: {
      volume: null,
      depth: 0,
      canJump: false,
      edgeTarget: null,
      haulProgress: 0
    },
    lastSafePerch: null,
    currentPlaceId: null,
    completed: false
  },
  world: {
    currentPlaceId: null,
    placeChain: [],
    places: {},
    entities: {
      perches: {},
      surfaces: {},
      anchors: {},
      waterVolumes: {},
      currents: {},
      floatables: {},
      hollows: {},
      insects: {},
      animals: {},
      hazards: {},
      endpoints: {},
      windZones: {},
      wasps: {}
    },
    checkpoints: {},
    snapshots: {},
    dynamicState: {},
    wetSurfaces: {},
    broken: {},
    eaten: {}
  },
  audio: {
    muted: false,
    ambientRainLevel: 0.35,
    chorusLevel: 0.0,
    currentPlace: null
  },
  ui: {
    overlay: "title",
    transition: { active: false, placeId: null, progress: 0 }
  },
  debug: {
    enabled: false,
    freeze: false
  }
};
```

## 2.3 Module specifics

| Module | Required functions |
| --- | --- |
| `input.js` | `setKey(code, down)`, `press(code)`, `release(code)`, `isDown(code)`, `getTapDuration(code)`, `getHoldDuration(code)`, `consumePress(code)`, `clearAll()` |
| `state.js` | `init()`, `startGame()`, `setScreen(name)`, `saveSnapshot(id)`, `restoreSnapshot(id)`, `resetToLastSafePerch()`, `transitionToPlace(placeId)` |
| `world.js` | `loadPlace(placeId)`, `getEntity(id)`, `registerEntity(type, record)`, `removeEntity(id)`, `setEntityState(id, patch)`, `getAll(type)` |
| `places.js` | `getCurrentPlace()`, `completePlace()`, `getNextPlace()`, `isEndpointReached()`, `completeGame()` |
| `physics.js` | `step(dt)`, `applyForces(body, forces)`, `integrate(body, dt)`, `resolveCollisions(body)`, `raycast(from, dir, maxDist)`, `solveRope(body, anchor, length)`, `addImpulse(body, impulse)` |
| `frog.js` | `step(dt)`, `setState(name)`, `setAim()`, `startCrouch()`, `launchFromCrouch()`, `land(surface)`, `cling(surface)`, `slide(surface)`, `enterWater(volume)`, `paddle(dt)`, `haul(edge)`, `reset(perch)`, `complete()` |
| `tongue.js` | `step(dt)`, `quickSnap()`, `startHeld()`, `attach(anchor)`, `detach()`, `eat(insect)`, `pullInput(dt)`, `getTip()` |
| `surfaces.js` | `isGripable(id)`, `isSlippery(id)`, `setWet(id, seconds)`, `isWet(id)`, `contact(frog, surface)`, `climbStep(surface)`, `applySlide(surface)`, `resetWetness(snapshot)` |
| `water.js` | `enter(volume)`, `step(frog, dt)`, `paddle(frog, dt)`, `canHaul(frog)`, `haul(frog, edge)`, `splash(frog, volume)`, `getBottomPlatform(volume)` |
| `checkpoints.js` | `isSafePerch(perch, frog)`, `maybeSetCheckpoint(frog)`, `setCheckpoint(perch)`, `resetToCheckpoint()`, `getNearestSafePerch(excludeHazard)` |
| `cat.js` | `step(dt)`, `canSee(frog)`, `addAttention(amount)`, `decayAttention(dt)`, `stepCloser(dt)`, `swat(frog)`, `resetToDefault()` |
| `heron.js` | `step(dt)`, `getSightArea()`, `isFrogInSight(frog)`, `snap(frog)`, `shiftAttention(source)`, `resetToDefault()` |
| `fish.js` | `step(dt)`, `canStrike(frog)`, `strike(frog)`, `dunk(frog)`, `spit(frog)`, `resetToDefault()` |
| `hazards.js` | `register(hazard)`, `step(hazard, dt)`, `activateThreshold(hazard)`, `startTelegraph(hazard)`, `startActive(hazard)`, `recover(hazard)`, `reset(hazard)` |
| `anchors.js` | `step(dt)`, `stress(anchor)`, `slip(anchor)`, `break(anchor)`, `move(anchor, delta)`, `reset(anchor)` |
| `floatables.js` | `step(dt)`, `supportLoad(frog, floatable)`, `tilt(floatable)`, `sink(floatable)`, `capsize(floatable)`, `drift(floatable, current)`, `reset(floatable)` |
| `hollows.js` | `canEnter(frog, hollow)`, `enter(frog, hollow)`, `canExit(frog, hollow)`, `exit(frog, hollow)`, `openFlap(hollow, amount)`, `tip(hollow)`, `fill(hollow, water)`, `reset(hollow)` |
| `currents.js` | `step(dt)`, `getFlowAt(point)`, `applyTo(frog, dt)`, `applyTo(floatable, dt)`, `start(source)`, `stop(source)`, `reset(source)` |
| `sprinkler.js` | `step(dt)`, `activate()`, `interrupt()`, `wetSurface(surface)`, `pushObject(entity)`, `reset()`, `setFeedState(state)` |
| `drainpipe.js` | `step(dt)`, `buildPressure(dt)`, `gurgle()`, `spit()`, `releasePressure()`, `reset()` |
| `dynamic.js` | `step(dt)`, `loadLeaf(leaf, frog)`, `tipBarrel(barrel, side)`, `crackLedge(ledge)`, `breakLedge(ledge)`, `reset(entity)` |
| `wind.js` | `step(dt)`, `getForceAt(point)`, `applyTo(frog, dt)`, `startGust(zone)`, `calm(zone)`, `reset(zone)` |
| `wasp.js` | `step(dt)`, `eat(wasp, frog)`, `applyPuffGrounded(frog)`, `applyPuffAirborne(frog)`, `reset(wasp)` |
| `insects.js` | `step(dt)`, `movePath(insect)`, `eat(insect)`, `respawn(insect)`, `isEdible(insect)` |
| `audio.js` | `init()`, `play(name, position)`, `setAmbient(name, level)`, `stop(name)`, `duck(name, level)`, `setChorus(level)` |
| `render.js` | `frame()`, `drawWorld()`, `drawFrog()`, `drawCat()`, `drawHeron()`, `drawFish()`, `drawHazards()`, `drawCues()`, `setCamera(frog)` |
| `ui.js` | `setOverlay(name)`, `showTitle()`, `showPlaying()`, `showCompleted()`, `startGame()`, `restartGame()` |
| `debug.js` | See §8. |
| `tests.js` | `runTier1()`, `runTier2()`, `runTier3()`, `runFull()`. |

# 3. VISUAL SPEC

The game is a quiet, wet, ground-level platformer. The frog is small and shiny, never a human in a costume. The world is built from rain-soaked surfaces seen from the frog’s point of view: dripping gutter metal, rain barrel wood, damp concrete, mossy stone, greenhouse glass, vines, gutters, and finally moonlit rooftop water. The palette is desaturated blues, greens, and grays with sharp wet highlights. The camera is low, close to the frog, and parallax layers create depth without clutter. The final rooftop pond and ring of lilies appear as a distant moonlit shape whenever the space allows it. There is no HUD.

## Lighting and atmosphere

| Element | Visual rule |
| --- | --- |
| Global light | Night rain, low ambient blue. Strong specular highlights on wet surfaces. |
| Wet surfaces | Thin white/cyan highlight on edges, small droplet trails, animated sheen. |
| Dry/smooth surfaces | Matte or faint dusty grain, no sheen. |
| Gripable damp surfaces | Darker, textured, visible moss/porous speckles, small water beads. |
| Slippery surfaces | Smooth, bright reflection band, no texture. |
| Rain | Vertical thin lines, low opacity, drifts with wind zones. |
| Drips | Falling droplets with tiny impact ripple. |
| Puddles | Dark reflective pools, ripple rings, bottom visible if shallow. |
| Glass | Transparent, faint reflection, cannot be stuck to. |
| Metal with condensation | Bright film, slippery visual cue. |
| Rooftop pond | Moonlit blue water, ring of lilies, soft light bloom, no gameplay HUD. |
| Danger telegraphs | Cat eyes, heron shadow, fish ripples, drainpipe vibration, sprinkler water cone, leaf bend, ledge cracks. |
| Goal visibility | Rooftop pond silhouette in far parallax for outdoor places; close-up for final. |

## Space

| Space | Visual identity |
| --- | --- |
| Rain barrel | Interior wood, water surface, leaf platform, gutter above. |
| Damp wall | Vertical concrete/brick, moss patches, tile edges. |
| Stone path | Wet tiles, mossy stones, puddles, fence rails. |
| Branch/cat | Wood branch, leaves, cat silhouette, roofline. |
| Koi pond | Lily pads, dark water, fish shape, banks. |
| Greenhouse | Glass, metal frames, condensation, sprinkler, plants. |
| Drainpipe | Pipe interior, bubbles, pressure vibration, weak anchors. |
| Gutter/roof | Metal canyon, wires, bottle caps, wind flags, lily ring. |
| Rooftop pond | Moonlit water, lilies, distant chorus visual pulse. |

## Recipe table

| Layer | Elements | Palette / recipe | Parallax |
| --- | --- | --- | --- |
| L0 sky | moon, clouds, rain | `#071018`, `#1a2b3b`, moon `#dceaff` | 0.10 |
| L1 far city | rooftops, distant chimney, rooftop pond hint | `#101d28`, `#1c2e3a`, pond `#274a66` | 0.25 |
| L2 mid garden | fence, tree, greenhouse outline | `#182b25`, `#27423b`, glass `#2e566b` | 0.50 |
| L3 gameplay | platforms, walls, gutters, barrels, water | wood `#3b2f27`, wet wood `#57463c`, concrete `#4a5258`, moss `#4f6b4a`, metal `#39424a`, glass `#6592a8` | 1.00 |
| L4 foreground | rain, vines, drips, ripples | rain `#9fb4c4`, vines `#3b5a3f`, ripples `#7fa4c4` | 1.20 |
| UI | title/complete only | text `#d9e8d8`, dark panel `#0b1216cc` | n/a |

# 4. GAMEPLAY SPEC

The game is a real-time authored platformer about a small wet frog. The player reads surfaces, times crouch-hops, uses the tongue only on visible anchors or insects, trusts sticky pads only on damp textured surfaces, and reaches authored endpoints. There is no combat, score, or death. Failure is a short embarrassed reset to a last safe perch, followed by a rethink. Tier 1 teaches crouch-hop, tongue, sticky walls, water, and cat stillness, then reaches the final rooftop pond. Tier 2 adds physical garden systems. Tier 3 adds rooftop wind, wasps, and multi-route trust.

## Records and rosters

### PlaceRecord

| Field | Meaning |
| --- | --- |
| `id` | Stable place id |
| `name` | Internal name |
| `width`, `height` | Authored bounds in meters |
| `startPerchId` | Opening safe perch |
| `endpointId` | Completion trigger |
| `safePerchIds[]` | Authored checkpoints |
| `entities[]` | Entity ids in place |
| `goalVisible` | Whether rooftop pond parallax visible |
| `tier` | 1, 2, or 3 |

### PerchRecord

| Field | Meaning |
| --- | --- |
| `id` | Stable id |
| `position`, `size` | AABB |
| `surfaceId` | Surface used |
| `safe` | Can become checkpoint |
| `endpoint` | Completes place |
| `moving` | Not safe if true |
| `submerged` | Not safe if true |
| `current` | Not safe if true |
| `hazard` | Not safe if true |

### SurfaceRecord

| Field | Meaning |
| --- | --- |
| `id` | Stable id |
| `bounds`, `normal` | AABB and contact side |
| `gripable` | Only true for damp textured porous |
| `wet` | Current wetness seconds |
| `slippery` | True if smooth/dry/dusty/oily/glazed/glass/condensation film |
| `material` | `bark`, `moss`, `wetWood`, `roughStone`, `dampConcrete`, `glass`, `metal`, `tile`, `leaf`, `crumblingLedge` |
| `dynamic` | Dynamic behavior type |
| `stress` | Dynamic state |

### AnchorRecord

| Field | Meaning |
| --- | --- |
| `id` | Stable id |
| `point` | Attachment point |
| `radius` | 0.12m |
| `stable` | True if cannot break/slip/move |
| `weak` | True if weak anchor |
| `visualCue` | `cracked`, `frayed`, `waterlogged`, `loose`, `thread`, `discolored`, `sway` |
| `stress` | Current stress |
| `state` | `stable`, `slipping`, `broken`, `moved` |

### InsectRecord

| Field | Meaning |
| --- | --- |
| `id` | Stable id |
| `kind` | `fly`, `wasp`, `beetle` |
| `position` | Current |
| `path[]` | Authored waypoints |
| `speed` | m/s |
| `edible` | Always true for these insects |
| `eaten` | True if consumed |
| `effect` | `none`, `cosmetic`, `waspPuff` |

### AnimalRecord

| Field | Meaning |
| --- | --- |
| `id` | Stable id |
| `kind` | `cat`, `heron`, `fish` |
| `position`, `facing` | Current |
| `attention` | 0-1 |
| `state` | Species state |
| `patrol[]` | Authored path |
| `sight` | Polygon or radius |
| `cooldown` | Seconds |

### HazardRecord

| Field | Meaning |
| --- | --- |
| `id` | Stable id |
| `kind` | `sprinkler`, `drainpipe`, `current`, `wind`, `waterSensor`, `hoseClamp`, `caterpillarBranch` |
| `state` | `idle`, `telegraph`, `active`, `recovering` |
| `timer` | Seconds |
| `threshold` | Physical value |
| `source` | Physical source |
| `effects[]` | Wet, push, current, dip, etc. |

### FloatableRecord

| Field | Meaning |
| --- | --- |
| `id` | Stable id |
| `kind` | `lilyPad`, `leaf`, `cork`, `tinLid`, `tinCan` |
| `bounds`, `position`, `rotation` | Current |
| `buoyancy` | Support capacity |
| `load` | Current load |
| `drag` | Water drag |
| `stability` | Capsize resistance |
| `state` | `floating`, `tilted`, `sinking`, `capsized`, `lodged` |

### CurrentRecord

| Field | Meaning |
| --- | --- |
| `id` | Stable id |
| `region` | AABB |
| `vector` | Direction |
| `strength` | m/s |
| `source` | Physical source id |
| `state` | `off`, `weak`, `strong` |

### WaterVolumeRecord

| Field | Meaning |
| --- | --- |
| `id` | Stable id |
| `surfaceY`, `bottomY`, `depth` | Geometry |
| `edges[]` | Haulable edges |
| `shallow` | True if bottom is platform |
| `currentIds[]` | Currents in volume |

### CheckpointSnapshot

| Field | Meaning |
| --- | --- |
| `id` | Snapshot id |
| `placeId` | Place |
| `perchId` | Last safe perch |
| `frog` | Position, velocity, state |
| `dynamicState` | All dynamic object states at snapshot time |
| `wetSurfaces` | Wetness at snapshot time |
| `animals` | Attention/patrol at snapshot time |
| `eaten` | Eaten insects at snapshot time |
| `broken` | Broken anchors/ledges at snapshot time |

## Place content roster

| Place ID | Name | Tier | Start perch | Endpoint | Size | Core/teaching |
| --- | --- | --- | --- | --- | --- | --- |
| `rain_barrel_leaf` | Rain Barrel Leaf | 1 | `start_leaf` | `barrel_rim_perch` | 5x3m | Leaf rock, move right, fly tongue, deep barrel water. |
| `damp_wall_puddle` | Damp Wall Puddle | 1 | `barrel_rim_perch` | `stone_path_perch` | 8x5m | Sticky wall, shallow puddle bottom, tile edges. |
| `branch_cat` | Branch Cat | 1 | `stone_path_perch` | `roofline_perch` | 10x6m | Branch tongue swing, cat stillness. |
| `koi_pond_lilies` | Koi Pond Lilies | 2 | `roofline_perch` | `gutter_ledge_perch` | 12x6m | Lily pads, fish, current, floatables. |
| `greenhouse_sprinkler` | Greenhouse Sprinkler | 2 | `gutter_ledge_perch` | `drainpipe_mouth_perch` | 12x7m | Glass, sprinkler, wet surfaces, hose clamp, water sensor, caterpillar branch. |
| `drainpipe_currents` | Drainpipe Currents | 2 | `drainpipe_mouth_perch` | `rooftop_perch` | 14x8m | Drainpipe, cork, current, weak anchors, hollow. |
| `gutter_wind_final` | Gutter Wind Final | 3 | `rooftop_perch` | `rooftop_pond` | 16x8m | Wind, wasp, multi-route, weak anchors, floatables. |
| `rooftop_pond` | Rooftop Pond | 1 | inside `gutter_wind_final` endpoint | game complete | 6x4m | Final pond, ring of lilies, chorus. Tier 1 uses it directly after `branch_cat`. |

## Entity content numbers

| Entity type | Total | Per place | Numbers/effects |
| --- | --- | --- | --- |
| Flies | 6 | `rain_barrel_leaf`:1, `damp_wall_puddle`:1, `branch_cat`:1, `koi_pond_lilies`:1, `greenhouse_sprinkler`:1, `gutter_wind_final`:1 | Edible radius 0.07m, path speed 0.8m/s. Eating causes cosmetic swallow only. Not coins. |
| Beetles | 4 | `damp_wall_puddle`:1, `branch_cat`:1, `greenhouse_sprinkler`:1, `drainpipe_currents`:1 | Edible radius 0.08m, crawl speed 0.12m/s. No traversal effect. |
| Wasps | 2 | `drainpipe_currents`:1, `gutter_wind_final`:1 | Edible radius 0.07m, hover speed 0.3m/s. Eating causes authored puff. |
| Cat | 1 | `branch_cat` | Patrol length 6m, attention system §4. |
| Heron | 1 | `koi_pond_lilies` | Sight area 2.5x1.5m, shadow telegraph, snap system §4. |
| Fish | 2 | `koi_pond_lilies`:1, `greenhouse_sprinkler`:1 | Strike radius 0.9m, dunk/spit system §4. |
| Lily pads | 6 | `koi_pond_lilies`:3, `gutter_wind_final`:3 | Interactive floatables. Final visual ring lilies are not counted as platforms. |
| Leaf floatables | 5 | `damp_wall_puddle`:1, `koi_pond_lilies`:2, `drainpipe_currents`:1, `gutter_wind_final`:1 | Dynamic/buoyant surfaces. |
| Corks | 1 | `drainpipe_currents` | Pullable physical source for current. |
| Tin lids | 2 | `drainpipe_currents`:1, `gutter_wind_final`:1 | Floatable platforms. |
| Tin can | 1 | `koi_pond_lilies` | Hollow landmark/floatable. |
| Rain barrels | 2 | `rain_barrel_leaf`:1, `drainpipe_currents`:1 | Hollow, deep water, tip dynamic. |
| Drainpipes | 2 | `rain_barrel_leaf` outlet, `drainpipe_currents`:1 | Pressure/gurgle/spit. |
| Sprinklers | 2 | `greenhouse_sprinkler`:2 | Wet surfaces, push objects. |
| Currents | 3 | `koi_pond_lilies`:1, `drainpipe_currents`:1, `gutter_wind_final`:1 | Directional water fields. |
| Weak anchors | 8 | `drainpipe_currents`:3, `gutter_wind_final`:5 | Slip/break/move. |
| Stable branch anchors | 2 | `branch_cat`:1, `drainpipe_currents`:1 | Tongue anchors. |
| Twigs | 10 | `branch_cat`:3, `greenhouse_sprinkler`:3, `drainpipe_currents`:2, `gutter_wind_final`:2 | Stable anchors unless weak-cued. |
| Hanging wires | 6 | `drainpipe_currents`:3, `gutter_wind_final`:3 | Stable anchors. |
| Bottle caps | 8 | `damp_wall_puddle`:2, `greenhouse_sprinkler`:2, `drainpipe_currents`:2, `gutter_wind_final`:2 | Stable anchors. |
| Cracked tile edges | 12 | `damp_wall_puddle`:4, `branch_cat`:4, `drainpipe_currents`:4 | Stable or weak depending visual cue. |
| Wooden fence rails | 4 | `branch_cat`:2, `koi_pond_lilies`:2 | Gripable wet wood or anchors if authored. |
| Mossy stones | 5 | `damp_wall_puddle`:2, `branch_cat`:3 | Gripable damp textured. |
| Dripping vines | 5 | `damp_wall_puddle`:2, `drainpipe_currents`:2, `gutter_wind_final`:1 | Anchors/grip/dynamic if authored. |
| Spider webs | 3 | `drainpipe_currents`:2, `gutter_wind_final`:1 | Source of weak spider silk anchors. |
| Crumbling ledges | 4 | `branch_cat`:1, `greenhouse_sprinkler`:1, `drainpipe_currents`:1, `gutter_wind_final`:1 | Crack/break. |
| Cat doors | 1 | `branch_cat` | Flap opening. |
| Hose clamps | 2 | `greenhouse_sprinkler`:2 | Hit to change flow if authored. |
| Water sensor | 1 | `greenhouse_sprinkler` | Activated by splash within 0.8m. |
| Caterpillar | 1 | `greenhouse_sprinkler` | On branch; sprinkler knocks it off, branch dips 0.45m. |
| Wind zones | 2 | `gutter_wind_final`:2 | Horizontal force zones. |

## Ground states and crouch-hop — Tier 1

| Rule | Number |
| --- | --- |
| Ordinary ground states | `idle`, `aiming`, `crouching`, `charging`, `launching`. No run/walk/slide/crawl. |
| Aim input | Left/Right sets facing. Up sets upward component. Aim angles: 0, 45, 90. No downward launch. |
| Crouch start | Press crouch while grounded. Frog crouches, legs coil. |
| Tap crouch | If release duration <0.10s, launch speed 3.0 m/s at current aim. |
| Hold crouch | Launch speed = `3.0 + 5.0 * min(charge / 0.90, 1.0)`. Max 8.0 m/s. |
| Charge cap | 0.90s. After cap, frog trembles but no penalty. |
| Launch | Release applies impulse once. State becomes airborne. |
| Airborne | Gravity only, plus wind/current/tongue/wasp. No aim/crouch/air control. |
| Landing | Collision with surface. If surface is safe perch, start checkpoint timer. |
| Reset after bad landing | If landing fails or hazard triggers, reset to last safe perch. |

## Tongue, eating, and stable anchors — Tier 1

| Rule | Number |
| --- | --- |
| Input | Space/J. Tap <0.12s = quick snap. Hold >=0.12s = held extension. |
| Quick snap | Range 1.15m. Out 0.08s, back 0.04s. Can eat edible insects. Cannot stick to anchors. |
| Held extension | Max length 2.6m, tip speed 9.0m/s. Can stick to grabbable anchors. Cannot eat. |
| Attachment | On first anchor hit, attach. Rope length = distance clamped 0.25-2.6m. |
| Clean miss | No dangle. If held extension reaches max without anchor, retracts. No constraint. |
| Pull/swing | While attached, Left/Right tangential accel 10.0m/s². Up shortens rope 1.2m/s. Down lengthens rope 1.2m/s up to max. |
| Release | Detaches and keeps momentum. |
| Cooldown | 0.18s after snap/detach. |
| Eating | Quick snap catches insect, swallow animation 0.35s, no score, no traversal effect except wasp if authored. |
| Anchors | Must be tagged and visible. Insects never anchors. |

## Sticky pads and grip — Tier 1

| Rule | Number |
| --- | --- |
| Gripable materials | bark, moss, wet wood, rough stone, damp concrete. Must be wet/damp. |
| Non-gripable | glass, smooth metal with condensation film, dry/dusty/oily/glazed, open water. |
| Cling | Landing on gripable wall sets `cling`. Does not slide upward. |
| Maintain | Hold toward wall to stay. Releasing direction causes slide at 1.0m/s but can re-cling. |
| Climb | Hold toward wall and tap crouch. Each successful pad contact moves +0.25m. Cooldown 0.22s. |
| Slide on gripable | If not holding toward wall, slide 1.0m/s. |
| Slippery wall | No cling. Gravity slide acceleration 12.0m/s², max 2.2m/s. Holding toward wall reduces acceleration to 5.0m/s² and max to 1.2m/s. |
| Wetness | Only authored wet surfaces are gripable. Sprinkler/rain can change wetness later. |

## Shallow water, puddles, and swimming — Tier 1

| Rule | Number |
| --- | --- |
| Shallow water | Depth <=0.25m. Bottom is platform. Frog can stand and crouch-hop normally. |
| Floatable puddle | Puddle becomes platform only when authored floatable is present. |
| Deep water | Depth >0.25m. Frog enters, cannot jump from water. |
| Paddle | Aim keys paddle in direction. Speed 0.55m/s. Drag 1.2. Net downward acceleration 2.0m/s² unless paddling up. |
| Haul out | If holding toward authored edge within 0.35m for 0.35s, frog hauls to perch. |
| No edge | If no reachable edge, current carries to nearest safe bank, or reset to last safe perch. Tier 1 has no currents, so reset to last safe perch. |
| Splash | Velocity into water >1.5m/s makes splash and noise. |
| Water is not platform | Only bottom, leaf, cork, tin lid, or authored floatable supports. |

## Checkpoints and reset — Tier 1

| Rule | Number |
| --- | --- |
| Safe perch | Authored perch with `safe:true`, not moving/submerged/current/hazard. |
| Set checkpoint | Frog grounded on perch for 0.75s. Store snapshot. |
| Last safe perch | Most recent authored safe perch. Not nearest object. |
| Reset triggers | Fall out of authored space, current dead end, cat swat, heron snap, fish spit, hazard return. |
| Reset target | Last safe perch. If none, nearest authored safe bank/checkpoint. If none, place opening perch. |
| Snapshot restore | Restore frog, dynamic objects, wetness, animals, eaten insects, broken anchors/ledges. |
| New checkpoint state | If change helped reach new safe perch, snapshot includes it. |
| Reset animation | Cough/shake 0.8s. No death screen. |

## Cat awareness and response — Tier 1

| Rule | Number |
| --- | --- |
| Notice inputs | Line of sight within 12m plus movement/noise. |
| Hidden | Still and behind cover/occluder. |
| Attention rates | Standing still: 0. Crouch charge: +0.10/s. Launch/landing: +0.80 instant. Splash: +0.50 instant. Moving in view: +0.35/s. |
| Decay | 0.45/s when hidden, still, or not visible. |
| Notice threshold | attention >=0.65. |
| Approach | While noticed and frog visible/moving, cat steps closer at 1.4m/s. |
| Swat | If frog exposed within 1.6m for 1.0s while noticed. |
| Swat result | Reset frog to last safe perch. Cat attention 0, cooldown 5.0s. |
| No combat | No damage, no health. |
| Visual cue | Cat eyes follow frog. |

## Place completion and core verb availability — Tier 1

| Rule | Number |
| --- | --- |
| Completion | Frog touches endpoint trigger or stands on `endpoint:true` perch. |
| Transition | 0.4s fade, load next place. |
| Game completion | Final rooftop pond endpoint reached. Frog joins chorus, completed screen. |
| No objectives | No collecting, switches, hidden goals. |
| Core verbs | Available from first frame. No unlocks. |
| Teaching | Fly, wall, branch, cat are authored entities, not gates. |

## Hazard activation and physical thresholds — Tier 2

| Rule | Number |
| --- | --- |
| State machine | `idle`, `telegraph`, `active`, `recovering`. |
| Activation | Physical variable reaches authored threshold. |
| No HUD | Telegraphs are visual/audio physical cues. |
| Determinism | Timers are fixed authored values. No random. |
| Player-changeable | Player may change physical state by hitting clamp, pulling cork, splashing sensor, disturbing branch. |
| Reset | Source returns to authored state. |

## Weak anchors — Tier 2

| Rule | Number |
| --- | --- |
| Visual cues | cracked, frayed, waterlogged, loose, thread, discolored, different sway. |
| Stress | Accumulates while attached under load. Hang time counts. |
| Slip | At 3.0s load or wrong pull direction >1.0s: tongue slides off after 0.35s. |
| Break | At 4.5s load or impulse >10.0 m/s equivalent: anchor snaps/falls, frog drops. |
| Move | If attached anchor shifts >0.3m but <=0.45m, route changes. If past limit, break/slip. |
| Reset | Unbreak, restore position. |

## Lily pads and floatable platforms — Tier 2

| Rule | Number |
| --- | --- |
| Support | Supports frog if buoyancy > load and frog not hanging edge. |
| Frog load | 1.0. |
| Edge hang | If frog hangs from edge >1.5s, tilt. |
| Stay load | If standing >2.5s, tilt. |
| Tilt | 10° at 2.5s, 20° at 4.0s. |
| Capsize | 25° or load >1.3. Platform fails; frog enters water unless attached. |
| Drift | Current applies velocity scaled by drag. |
| Collide | Floatables collide and can lodge as temporary platform. |
| Reset | Floatables return to source position/state. |

## Hollow landmarks and containers — Tier 2

| Rule | Number |
| --- | --- |
| Enter | Opening width >=0.35m and reachable. |
| Inside | Same grip/water rules on interior surfaces. |
| Exit | Only through authored rim, drain, hole, flap, gap. |
| Flap | Opens when pushed/pulled 0.6m. |
| Drain exit | Only if outlet ledge reached and frog can hop/cling out. |
| Tip | Barrel/landmark can tip; floor tilts, frog slides/carried. |
| Fill | Water fills interior and swims frog out. |
| Reset | Restore interior state. |

## Currents and flows — Tier 2

| Rule | Number |
| --- | --- |
| Still water | Slows with drag 0.8. |
| Weak flow | <=0.5m/s. Frog can fight with paddle 0.55m/s. |
| Strong flow | >0.7m/s. Frog swept unless reaches edge/anchor within 0.5m. |
| Floatables | Carried, collide, lodge. |
| Source | Cork pulled, pipe unblocked, rain fills basin, drain pressure. |
| Stop | Source closes, water drains below threshold, place resets. |

## Drainpipe gurgles and spits — Tier 2

| Rule | Number |
| --- | --- |
| Pressure build | 3.0-5.0s authored cycle. Bubbles/vibration/wetness. |
| Spit | Duration 0.35s, radius 1.2m, impulse 3.0m/s. |
| Effects | Wets nearby surfaces 6.0s, pushes light objects, may knock loose debris, may create brief current. |
| Player options | Wait, stand outside mouth, anchor, use spit to move/clear. |
| Stop | Pressure releases or water drains below threshold. |

## Sprinkler spray and wet surfaces — Tier 2

| Rule | Number |
| --- | --- |
| Cycle | Idle 9.0s, active 4.0s. |
| Cone | 55°, range 4.5m. |
| Wet smooth | After 1.0s film, after 2.0s slick non-grip. |
| Wet porous | Damp only; continuous spray 3.0s washes grip away. |
| Objects | Push small objects 2.0m/s, fill basins, start currents. |
| Frog hit | Push 2.5m/s, no damage, next move from wet surface. |
| Ends | Pressure cycle ends, player interrupts feed, water drains. |
| Wet persistence | Remains until water recedes/dries/place resets. |

## Dynamic surfaces — Tier 2

| Rule | Number |
| --- | --- |
| Leaf | Sustained weight >1.2s or 3 loads bends/sinks over 0.6s. Drops unless attached. |
| Rain barrel | Tips if frog center beyond support polygon by 0.25m for 0.5s or pushed. Rotates 90° over 1.2s. |
| Crumbling ledge | First load cracks. Second load or sustained 1.5s breaks. Light launch <5.0m/s may delay. Tongue offload can prevent break. |
| Change while on | Surface stops being solid. Frog slides/falls/carried unless tongue catches another anchor. |
| Reset | Unbreak, upright, restore wetness. |

## Heron — Tier 2

| Rule | Number |
| --- | --- |
| Sight | Authored polygon. Shadow marks target area. |
| Trigger | Frog moves/splashes inside sight while unhidden. |
| Snap delay | 0.6s. |
| Ignore | Still, under cover, on wall, outside sight. |
| Distraction | Branch disturbance elsewhere shifts attention, stops hunting that spot 3.0s. |
| Snap result | Brief dark swallow, then reset to nearest safe perch not same hazard. |

## Fish — Tier 2

| Rule | Number |
| --- | --- |
| Present cues | Ripples, bubbles, disturbed lily pads, shape under surface. |
| Strike radius | 0.9m. |
| Trigger | Frog enters water, splashes, or moves within radius. |
| Ignore | Still frog on bank or under cover. |
| Strike | Grab, dunk 0.8s, spit to nearest safe bank. If none, last safe perch or nearest authored safe edge. |
| Cooldown | 3.0s. |

## Wind zones — Tier 3

| Rule | Number |
| --- | --- |
| Cues | Flags, swaying plants, drifting rain, dust, ripples, audio. |
| Cycle | Calm 8.0s, gust 1.8s, strength 4.0m/s horizontal acceleration. |
| Airborne | Pushes frog horizontally. |
| Crouched exposed | Force 3.0m/s², may shove off perch if not anchored. |
| Player options | Wait, anchor, lower/covered route, time jump with/against wind. |
| Reset | Return to calm state. |

## Wasp puff — Tier 3

| Rule | Number |
| --- | --- |
| Eating | Quick snap only. |
| Grounded | After 0.35s hiccup, forced sideways hop impulse 2.2m/s along facing. |
| Airborne | Adds sideways impulse 1.6m/s for 0.15s. |
| Aim | Player cannot aim puff. |
| Bad landing | Treated as normal bad hop. No extra penalty. |
| Authored only | Puff only where wasp placement is part of route. |

## Multi-route traversal — Tier 3

| Rule | Number |
| --- | --- |
| Direct dangerous | Example: chain of tongue swings over pond. Requires anchors, timing, weak anchor risk. |
| Longer safe | Example: climb wall, wait out cat, cross gutter. Requires grip, patience, attention. |
| Use hazards | Example: sprinkler knocks caterpillar off branch so branch dips 0.45m; cork pull starts current carrying leaf into place; splash near water sensor opens flow. |
| No locks | All routes are physical consequences. |
| Choice | Player may choose route; endpoint remains same. |

## Progression and difficulty

| Tier | Difficulty |
| --- | --- |
| Tier 1 | One verb at a time. Short places. No heron/fish/lily/current/sprinkler/wind. Cat teaches stillness. Final pond is short. |
| Tier 2 | One supporting system per place. Koi pond teaches fish/lily/current. Greenhouse teaches sprinkler/wet surfaces. Drainpipe teaches pressure/weak anchors. |
| Tier 3 | Combine verbs. Wind plus tongue. Wasp plus crouch-hop. Direct dangerous vs longer safe. |
| Overall | No score. Difficulty is route complexity and timing, not punishment. |

## Feel

| Element | Feel rule |
| --- | --- |
| Crouch | Visible coil, throat/legs compression, charge cap tremble. |
| Launch | Snappy push, no air input. |
| Tongue | Instant snap or physical rope; no magic dangle. |
| Wall | Pads catch with small thud; climb is deliberate. |
| Water | Soft splash, sluggish paddle, clear edge haul. |
| Reset | Short embarrassed cough, no death. |
| Hazards | Physical telegraphs, no HUD prompts. |
| Goal | Distant moonlit pond and chorus provide direction. |

# 5. CHARACTERS

## Player: small wet frog

| Aspect | Spec |
| --- | --- |
| Silhouette | Low body, wide crouched stance, bulging eyes, thick legs, smooth wet shine. Not human. |
| Size | Collision 0.28m wide, 0.18m tall. Visual 0.22m tall. |
| Colors | Body `#5d7a6b`, belly `#86a48f`, eyes `#d9e8d8` with black pupils, wet highlight `#dceaff`. |
| Facing | Left/right. Aim visible by body tilt and eye direction. |
| States needed | `idle`, `aiming`, `crouching`, `charging`, `airborne`, `tongue_snap`, `tongue_hold`, `attached`, `cling`, `climbing`, `sliding`, `water`, `paddle`, `haul`, `reset`, `completed`. |

### Frog animations

| Animation | Motion rule |
| --- | --- |
| `idle_breathe` | 2.0s loop. Throat subtle swell. Eyes follow threats. |
| `aim_idle` | Body leans slightly toward aim. No movement. |
| `crouch_coil` | Legs compress, body lowers. Duration follows charge. |
| `charge_tremble` | At cap, slight leg tremble. No damage. |
| `launch_push` | 0.12s leg extension. |
| `airborne_arc` | Body tucked, no input control. |
| `tongue_snap` | 0.12s tongue out/back. |
| `tongue_hold` | Tongue extends along aim, body may lean. |
| `attached_swing` | Body follows rope, pads visible. |
| `wall_cling` | Body pressed to wall, pads contact. |
| `wall_crawl_hop` | 0.18s upward hop, pads contact wall. |
| `wall_slide` | Legs splayed, slow slide. |
| `water_enter` | Splash, body flattens. |
| `paddle` | Legs paddle, body bobs. |
| `haul_edge` | Front paws catch edge, body pulls up 0.35s. |
| `embarrassed_reset` | Cough/shake 0.8s, water droplets fly. |
| `join_chorus` | Throat swells, call pose. |

## Cat

| Aspect | Spec |
| --- | --- |
| Silhouette | Large looming cat, not cartoon adventurer. Eyes follow frog. |
| Visual size | 1.8m silhouette, collision/swat radius 1.6m. |
| Colors | Fur `#2a2b2f`, eyes `#d9e8d8`, shadow `#0b1216`. |
| States | `watching`, `noticing`, `approaching`, `swatting`, `cooldown`. |

| Animation | Motion rule |
| --- | --- |
| `watch_turn` | Head follows frog. |
| `step_closer` | Slow step toward frog when attention high. |
| `swat` | Quick paw swipe 0.25s. |
| `disinterest` | Yawn/turn away during cooldown. |

## Heron

| Aspect | Spec |
| --- | --- |
| Silhouette | Tall bird shadow, not always visible. Shadow is danger. |
| Visual size | 1.6m, shadow area 2.5x1.5m. |
| States | `hunting`, `targeting`, `snapping`, `shifted`, `cooldown`. |

| Animation | Motion rule |
| --- | --- |
| `shadow_move` | Shadow passes over ground. |
| `target_hold` | Shadow fixes area. |
| `snap` | Beak strike 0.3s. |
| `swallow_dark` | Brief dark swallow, then reset. |
| `attention_shift` | Head turns away, stops hunting. |

## Fish

| Aspect | Spec |
| --- | --- |
| Silhouette | Dark shape under water, ripples, bubbles. |
| Visual size | 0.6m, strike radius 0.9m. |
| States | `lurk`, `alert`, `striking`, `dunking`, `spitting`, `cooldown`. |

| Animation | Motion rule |
| --- | --- |
| `lurk_ripple` | Slow swim, ripple pulses. |
| `surface_alert` | Shape near surface. |
| `snap` | Water burst 0.25s. |
| `dunk` | Frog pulled underwater 0.8s. |
| `spit` | Frog moved to bank. |

## Insects

| Entity | Animation | Rule |
| --- | --- | --- |
| Fly | `fly_path` | Follows authored waypoints, speed 0.8m/s. |
| Wasp | `wasp_hover` | Hovers path, speed 0.3m/s. |
| Beetle | `beetle_crawl` | Crawls 0.12m/s. |
| Eaten | `eaten_fade` | Cosmetic swallow, re-form on reset. |

# 6. AUDIO

All audio is diegetic and synthesized. No HUD prompts. No music track except ambient rain and frog chorus.

| Name | Recipe | Plays when |
| --- | --- | --- |
| `ambient_rain` | Brown noise, lowpass 1200Hz, gain 0.25 | During all places, level varies by place. |
| `drip_single` | Sine 450Hz to 180Hz, 0.08s, gain 0.2 | Authored drip cycles. |
| `leaf_rock` | Low sine 80Hz 0.15s + filtered noise 0.1s | Leaf rocks at start. |
| `crouch_coil` | Low sine 70Hz rising to 110Hz, 0.4s | Crouch held. |
| `launch_hop` | Sine 180Hz to 90Hz 0.12s + noise burst | Crouch release. |
| `land_soft` | Short noise 300Hz, 0.06s | Landing on damp surface. |
| `land_hard` | Short noise 800Hz, 0.09s | Landing on stone/metal. |
| `tongue_snap` | Noise bandpass 1200Hz, 0.03s, gain 0.18 | Quick tongue snap. |
| `tongue_extend` | Filtered noise 400Hz, 0.08s | Held extension. |
| `tongue_attach` | Thud sine 120Hz 0.08s | Tongue sticks to anchor. |
| `tongue_miss` | Soft air noise 0.04s | Clean miss. |
| `eat_insect` | Short wet pop 600Hz, 0.05s | Eating fly/beetle. |
| `swallow` | Low gurgle 90Hz, 0.2s | Swallow animation. |
| `pad_catch` | Soft thud 150Hz, 0.05s | Sticky pad contact. |
| `wall_slide` | Long filtered noise 250Hz, 0.2s loop | Sliding on slippery wall. |
| `water_enter` | Noise bandpass 900-2500Hz, 0.12s | Frog enters water. |
| `splash` | Noise 1000-3000Hz, 0.15s | Splash event. |
| `paddle` | Short water noise 0.08s | Paddle input. |
| `haul_edge` | Wet scrape 300Hz, 0.2s | Hauling out. |
| `cat_step` | Low soft noise 120Hz, 0.08s | Cat steps closer. |
| `cat_notice` | Low growl 60Hz, 0.25s | Cat attention reaches threshold. |
| `cat_swat` | Fast noise 700Hz, 0.08s | Cat swat. |
| `cat_disinterest` | Soft exhale noise 0.3s | Cat cooldown. |
| `heron_shadow` | Low wind noise 0.4s | Shadow appears. |
| `heron_snap` | Sharp click + noise 0.1s | Heron snap. |
| `heron_shift` | Soft wing rustle 0.2s | Attention shifted. |
| `fish_ripple` | Low sine 100Hz + water noise, 0.2s | Fish present. |
| `fish_snap` | Wet slurp noise, 0.12s | Fish strike. |
| `fish_dunk` | Underwater filtered noise, 0.8s | Fish dunk. |
| `drain_gurgle` | Modulated noise 50-200Hz, 0.6s | Drainpipe pressure. |
| `drain_spit` | Pulse noise 300-1200Hz, 0.35s | Drainpipe spit. |
| `sprinkler_start` | Valve click + noise ramp, 0.2s | Sprinkler active. |
| `sprinkler_loop` | Bandpass noise 1-3kHz, gain 0.2 | Sprinkler active. |
| `sprinkler_stop` | Valve click, 0.1s | Sprinkler stops. |
| `wind_gust` | Filtered noise 200-1200Hz, 1.8s | Wind gust. |
| `wasp_puff` | Small pop 800Hz, 0.05s | Wasp puff. |
| `reset_cough` | Frog cough 150Hz, 0.2s | Reset. |
| `place_transition` | Soft water swell, 0.4s | Place complete. |
| `frog_call` | FM sine 300-450Hz, 0.15s | Chorus pulses. |
| `final_chorus` | Layered frog calls, gain ramps to 0.5 | Completed screen/final pond. |

# 7. UX

## Screens state machine

| State | Trigger | Visual | Input |
| --- | --- | --- | --- |
| `title` | Game load | Title “small wet frog”, controls summary, Start. No HUD. | Enter/click starts. |
| `playing` | Start selected | Canvas gameplay only. No HUD. | Gameplay inputs. |
| `place_transition` | Endpoint reached | 0.4s fade. | None. |
| `completed` | Final endpoint | Moonlit pond, chorus, “You joined the chorus.” Restart. | Enter/click restarts. |

## HUD table

| HUD element | Record field | When visible |
| --- | --- | --- |
| none | n/a | No persistent HUD is rendered during `playing`. |

# 8. DEBUG API

| Function | Returns / effect |
| --- | --- |
| `debug.frog.getState()` | Full player record. |
| `debug.frog.setPosition(x,y)` | Sets frog position. |
| `debug.frog.setState(state)` | Sets state. |
| `debug.input.press(code)` | Presses key. |
| `debug.input.release(code)` | Releases key. |
| `debug.input.tap(code, duration)` | Presses then releases after duration. |
| `debug.input.hold(code, duration)` | Presses then releases after duration. |
| `debug.tongue.getState()` | Tongue mode, length, tip, attached anchor. |
| `debug.tongue.attachAnchor(anchorId)` | Forces attachment for test. |
| `debug.tongue.detach()` | Detaches. |
| `debug.surfaces.getState(surfaceId)` | Gripable, wet, slippery, stress. |
| `debug.water.getState(volumeId)` | Depth, shallow, edges, currents. |
| `debug.checkpoints.getState()` | Last safe perch, snapshot id. |
| `debug.checkpoints.set(perchId)` | Forces checkpoint. |
| `debug.places.getState()` | Current place, endpoint reached, next place. |
| `debug.cat.getState()` | Attention, state, position. |
| `debug.heron.getState()` | Sight, state, attention. |
| `debug.fish.getState()` | Position, state, cooldown. |
| `debug.hazards.getState(hazardId)` | State, timer, effects. |
| `debug.anchors.getState(anchorId)` | Stable/weak, stress, state. |
| `debug.floatables.getState(id)` | Load, tilt, state. |
| `debug.hollows.getState(id)` | Interior state, openings. |
| `debug.currents.getState(id)` | Vector, strength. |
| `debug.sprinkler.getState(id)` | Cycle, wetness. |
| `debug.drainpipe.getState(id)` | Pressure, state. |
| `debug.dynamic.getState(id)` | Leaf/barrel/ledge stress. |
| `debug.wind.getState(id)` | Calm/gust, force. |
| `debug.wasp.getState(id)` | Eaten, puff state. |
| `debug.insects.getState(id)` | Position, eaten. |
| `debug.audio.getState()` | Ambient levels, chorus. |
| `debug.state.saveSnapshot(id)` | Saves snapshot. |
| `debug.state.restoreSnapshot(id)` | Restores snapshot. |
| `debug.state.resetToLastSafePerch()` | Triggers reset. |
| `debug.time.setFrame(n)` | Advances fixed steps for tests. |
| `debug.freeze(on)` | Freezes simulation. |

# 9. TESTS

| Tier | Test | Pass condition |
| --- | --- | --- |
| 1 | Title to playing | Enter/click changes screen to `playing`. |
| 1 | Crouch tap launches minimal arc | Tap crouch <0.10s produces speed 3.0m/s. |
| 1 | Crouch hold caps at max | Hold 1.0s produces speed 8.0m/s. |
| 1 | Aim changes launch direction | Press Up+Right sets angle 45°, velocity vector matches. |
| 1 | No air steering | Aim input during airborne does not change velocity except gravity. |
| 1 | Quick snap eats fly | Quick snap hits fly, fly `eaten:true`, no anchor. |
| 1 | Quick snap cannot stick | Quick snap hits anchor, no attachment. |
| 1 | Held extension attaches branch | Held extension hits branch, `attached:true`. |
| 1 | Clean miss no dangle | Held extension misses, no constraint, frog falls. |
| 1 | Release keeps momentum | Detach preserves velocity. |
| 1 | Sticky wall clings | Landing on gripable wall sets `cling`. |
| 1 | Wall climb moves up | Hold toward wall + crouch tap increases y by 0.25m. |
| 1 | Slippery wall slides | Landing on slippery wall sets slide, not cling. |
| 1 | Shallow puddle bottom is platform | Depth <=0.25m allows normal launch from bottom. |
| 1 | Deep water cannot jump | State `water`, crouch launch disabled. |
| 1 | Haul edge works | Holding toward edge within 0.35m for 0.35s moves to perch. |
| 1 | Checkpoint sets after 0.75s | Standing on safe perch sets lastSafePerch. |
| 1 | Reset restores snapshot | Dynamic leaf/barrel/eaten insect restored. |
| 1 | Cat attention rises with movement | Moving in cat sight raises attention. |
| 1 | Cat swat resets | Exposure near cat causes reset, no death screen. |
| 1 | Place completion | Touch endpoint starts transition. |
| 1 | Final completion | Touch rooftop pond sets completed screen. |
| 1 | No HUD | No HUD elements rendered in playing. |
| 2 | Weak anchor slips | Held weak anchor after 3.0s slips. |
| 2 | Weak anchor breaks | Held weak anchor after 4.5s breaks and detaches. |
| 2 | Lily pad capsizes | Standing >4.0s or load >1.3 causes capsize. |
| 2 | Hollow entry | Frog enters through opening width >=0.35m. |
| 2 | Current carries | Strong flow >0.7 moves frog if no edge/anchor. |
| 2 | Drainpipe spit | Pressure threshold creates impulse and wetness. |
| 2 | Sprinkler slicks smooth surface | Smooth surface becomes slippery after 2.0s spray. |
| 2 | Leaf sinks | Sustained >1.2s sinks leaf. |
| 2 | Ledge cracks/breaks | First load cracks, second breaks. |
| 2 | Heron snap | Moving in sight causes reset. |
| 2 | Fish strike | Water entry in radius causes dunk/spit. |
| 3 | Wind gust pushes | Airborne velocity changes during gust. |
| 3 | Wasp puff grounded | Eating wasp causes forced sideways impulse. |
| 3 | Wasp puff airborne | Eating while airborne adds impulse. |
| 3 | Multi-route reaches endpoint | Direct and safe routes both complete place. |
| Full | Full chain completes | All places loaded in order and final completes. |

# 10. BUILD ORDER

| Order | Task |
| --- | --- |
| 1 | Fixed step loop, input, global context, debug API. |
| 2 | Frog physics, crouch-hop, aim, landing. |
| 3 | Surfaces, gripable/slippery tags, wall cling/climb/slide. |
| 4 | Tongue quick/held, eating, anchors, rope. |
| 5 | Water shallow/deep, paddle, haul, splash. |
| 6 | Checkpoints, snapshots, reset. |
| 7 | Cat awareness and swat. |
| 8 | Place chain, endpoints, transitions, final completion. |
| 9 | Tier 1 art: rain barrel, damp wall, branch/cat, final pond. |
| 10 | Tier 1 audio: rain, drips, splashes, tongue, cat, chorus. |
| 11 | Tier 1 playtest and fix reachability. |
| 12 | Hazard state machine. |
| 13 | Weak anchors. |
| 14 | Lily pads/floatables. |
| 15 | Hollow landmarks. |
| 16 | Currents. |
| 17 | Drainpipe and sprinkler. |
| 18 | Dynamic surfaces. |
| 19 | Heron and fish. |
| 20 | Tier 2 places. |
| 21 | Wind zones. |
| 22 | Wasp puff. |
| 23 | Multi-route final place. |
| 24 | Full chain integration and tests. |

# 11. DEFINITION OF DONE

## Tier 1 Definition of Done

High level: A player can start at the rain barrel leaf, learn crouch-hop, tongue, sticky wall, water, and cat stillness, then reach the final rooftop pond through at least one authored route. Failure resets to last safe perch. No HUD, no combat, no score.

| Check | Done when |
| --- | --- |
| Core run finishable | Places `rain_barrel_leaf`, `damp_wall_puddle`, `branch_cat`, final `rooftop_pond` complete in order. |
| Crouch-hop complete | Tap, hold, aim, cap, no air control. |
| Tongue complete | Quick eat, held anchor, pull/swing, release momentum, clean miss no dangle. |
| Sticky pads complete | Gripable walls cling/climb; slippery walls slide. |
| Water complete | Shallow bottom platform, deep no jump, paddle, haul. |
| Checkpoints complete | Last safe perch after 0.75s, snapshot reset. |
| Cat complete | Attention, approach, swat, cooldown. |
| Place completion complete | Endpoint trigger only. |
| All verbs available | No unlock flags. |
| Art complete | Parallax, wet surfaces, low camera, goal visible where possible. |
| Audio complete | Rain, drips, splashes, tongue, cat, chorus. |
| UX complete | Title, playing, completed. No HUD. |
| Tests pass | Tier 1 tests pass. |

## Tier 2 Definition of Done

High level: Supporting systems are added without breaking tier 1. Each system is visible, physical, and testable.

| Check | Done when |
| --- | --- |
| Hazard activation | Physical thresholds, no HUD. |
| Weak anchors | Slip/break/move, visual cues. |
| Lily pads | Load, tilt, capsize, drift. |
| Hollow landmarks | Enter/exit interiors. |
| Currents | Weak/strong flow, carrying. |
| Drainpipe | Gurgle/spit, wet/push. |
| Sprinkler | Wet surfaces, slick, push. |
| Dynamic surfaces | Leaf/barrel/ledge stress. |
| Heron | Shadow, snap, distraction. |
| Fish | Ripples, strike, spit. |
| Tier 2 places | `koi_pond_lilies`, `greenhouse_sprinkler`, `drainpipe_currents` complete. |
| Reset robust | All dynamic state restores. |
| Tests pass | Tier 2 tests pass. |

## Tier 3 Definition of Done

High level: Final approach trusts player. Wind, wasps, and multi-route traversal create choices.

| Check | Done when |
| --- | --- |
| Wind zones | Gusts, cues, force, anchoring. |
| Wasp puff | Forced unaimed impulse, authored only. |
| Multi-route | Direct dangerous and longer safe routes both reach endpoint. |
| Tier 3 place | `gutter_wind_final` complete. |
| Tests pass | Tier 3 tests pass. |

## Full Definition of Done

High level: Full chain completes from start to final pond with tier 1, tier 2, and tier 3 systems integrated. No soft locks. No HUD. No random gameplay.

| Check | Done when |
| --- | --- |
| Full chain | All places load in order. |
| No soft lock | Any reset returns to safe authored perch. |
| No permanent break | Dynamic state restores. |
| No HUD prompts | No gameplay HUD. |
| No random | No random gameplay source. |
| All tests pass | Tier 1, 2, 3, full tests pass. |

# A. SANITY

| Check | Result |
| --- | --- |
| All requested high-level decisions carried? | Yes. §0.1 maps them. |
| Every decision documented? | Yes. §0.2 lists rulings and reasons. |
| Tier 1 only core mechanics? | Yes. Tier 1 systems are exactly core mechanics. Support/extra are tier 2/3. |
| Core mechanics finished in tier 1? | Yes. Crouch-hop, tongue, sticky, water, checkpoints, cat, place completion, verb availability all have numbers and tests. |
| No added systems? | Yes. No combat, score, inventory, unlocks, HUD, random, death screen, or collectathon. |
| Input maps to all verbs? | Yes. Crouch, aim, tongue, UI start/restart. |
| Numbers concrete? | Yes. Units, physics, hazards, animals, anchors, floatables, wind, wasp. |
| Content numbers concrete? | Yes. Place counts, entity totals, counts per place. |
| No HUD? | Yes. §7 has empty HUD table. |
| No death screen? | Yes. Reset animation only. |
| No air control? | Yes. §4 and tests. |
| No insects as anchors? | Yes. Insect records cannot be anchors. |
| No release-to-swing? | Yes. Release detaches and keeps momentum. |
| No jumping from deep water? | Yes. |
| No wall upward slide? | Yes. Only timed hops/crawls. |
| No wasp aim? | Yes. Forced unaimed impulse. |
| No locked doors/switches? | Yes. Physical thresholds only. |
| No random? | Yes. §1.2 and conventions. |
| Reset prevents soft lock? | Yes. Nearest safe perch, bank, opening perch fallback. |
| Art/audio present in tier 1? | Yes. §3, §6, tier 1 DoD. |
| Tests validate tiers? | Yes. §9. |
| Build order reaches done? | Yes. §10. |
| Definition of done aligns with tiers? | Yes. §11. |
| Any contradictions found? | Initial tension between final pond visibility and deep places resolved by “whenever possible” and parallax rules. |
| Any scope creep? | Removed potential extras: pause, save, collect, combat, stamina, HUD. |