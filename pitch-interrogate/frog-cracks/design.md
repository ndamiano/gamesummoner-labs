# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| A platformer where the player plays as a frog | §4.1, §4.2, §5 |
| Real-time continuous platformer, no turns, no pause-time actions, no menu-time traversal | §1.2, §7 |
| The player is a small, wet frog at frog scale | §3, §4.1, §4.2, §5 |
| Crouch-hops, sticky pads, tongue probes, committed tongue anchors, water, currents, physical world changes | §4.2–§4.5, §4.10–§4.11 |
| Handcrafted, connected, bounded places, not an open world | §4.14, §2.3 |
| Each place has exactly one Answering Node with a live Answering chorus | §4.8, §4.14 |
| A place is completed only when the frog holds a croak at the Answering Node while a stable return route exists | §4.8, §4.14 |
| Final rooftop pond needs no return route and ends the game when called | §4.8, §4.14, §7 |
| Animals, rain, wind, sprinklers, rain barrels, currents, weak surfaces, edible insects are read through physical tells | §3, §4.6, §4.11–§4.12, §6 |
| No combat, death, survival meter, collectathon, abstract puzzle machine | §0.2, §4, §7, §9 |
| Low-angle side-view platformer with layered parallax and close camera at frog scale | §1.1, §3, §4.14 |
| Run begins under a dripping gutter on a leaf floating in a rain barrel | §4.14, §7 |
| Run ends at the moonlit rooftop pond when the frog calls and the full chorus answers | §4.8, §4.14, §7 |
| Quiet, wet, patient, physical tone; failure produces embarrassment, delay, rethink | §3, §4, §5, §6 |
| Readable low-scale wet materials; no HUD markers for anchors, goals, hazards, completion | §3, §6, §7 |
| Core mechanics: Frog Body and Hop, Tongue, Grip and Climbing, Water and Wet Surfaces, Animal Attention, Failure Recovery and Safe Perch, Answer Call and Place Completion | §4.2–§4.8 |
| Supporting mechanics: Eating Body States, Reactive World, Active Environmental Systems | §4.9–§4.11 |
| Extra mechanics: Rain and Weather, Soft Ladder and Revisitation | §4.12–§4.13 |
| Concrete content, numbers, input, run structure, visuals/audio, engineering contracts, tests, build order, done definitions | All sections |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| All prompt decisions are final | Adopted unchanged | User says high-level decisions are final |
| Game is a browser game | HTML/CSS shell + canvas/WebAudio/WebGL2 fallback | Browser target |
| No combat, death, score, collectathon, survival meters | No health, no score, no death screen, no required pickups | Preserves forgiving, physical tone |
| No HUD markers for anchors, goals, hazards, completion | Normal gameplay HUD is empty; only debug overlay exists | Preserves material language and listening |
| No pause-time actions or menu-time traversal | No pause screen; browser tab suspend only auto-suspends simulation | Keeps real-time continuous |
| Places are handcrafted, connected, bounded | Place graph with local bounds and thresholds | Prevents open world |
| Each place has exactly one Answering Node | Place record enforces one `answerNode` | Required by decisions |
| A run must be finishable | Tier1 contains a minimal three-place run: P01, P02, P99 | Tier1 must be buildable and finishable |
| Full described run is richer | Tier2 expands to six places: P01, P02, P03, P04, P05, P99 | Adds content without breaking Tier1 |
| Final place is exempt from return route rule | P99 has `returnRouteRequired=false` | Required by decisions |
| First place return target | P01 return target is the stable rain-barrel stone rim, not the temporary leaf | Leaf teaches lightness but is not durable stable perch |
| Player identity | The player is an unnamed small wet frog; no costume, no adventurer identity | Required tone |
| Input scheme | Keyboard primary: Space crouch-hop, arrows/WASD aim/crawl/climb/swim, Z tongue, C call | One clear real-time control set |
| Frog cannot run | Ground crawl max 26 px/s; no run state | Required by decisions |
| Hop is commitment-based | Crouch charge controls power; no air steering except environmental forces | Required by decisions |
| Tongue has light grab/probe and committed anchor | One tongue key: tap/probe, hold to commit when target is anchor | Matches two registers |
| Food eating is optional and temporary | Eating never required, no meter, no collect score | Required by decisions |
| Eating effects are deterministic by insect type | Fly=sneeze, beetle=sluggish, wasp=next jump buzz kick | Required by decisions |
| Animals are attention hazards, not combat | Cat/heron/fish attention states, no health, no defeat | Required by decisions |
| Failure recovery never unresolved | Last safe perch, current deposit, rescue ledge fallback | Required by decisions |
| Answer call is held croak | Hold C; completion requires live chorus, stable perch, route | Required by decisions |
| Stable return route is a precondition | Route graph checked before call can succeed | Required by decisions |
| Physical changes may persist | World state persists per place across revisits | Required by decisions |
| No UI markers | Material, audio, camera, ambient call only | Required by decisions |
| No random eating effects | Effects fixed by live insect kind | Required by decisions |
| Hazards require physical tells | Every hazard has visual/audio tell before effect | Required by decisions |
| No abstract switches/locked doors | Only physical interactions: pull, wet, knock, distract, ride, climb | Required by decisions |
| Number of places in final spec | Full spec defines 6 places, Tier1 uses 3 | Balanced: finishable Tier1, richer later |
| Place IDs | P01 Rain Barrel Gutter, P02 Damp Wall Stone Path, P03 Wet Crate Alley, P04 Branch Vine Trellis, P05 Greenhouse Lily Basin, P99 Moonlit Rooftop Pond | Clear contract for builder |
| World units | px, seconds, fixed 60 Hz simulation | Simple browser physics |
| Canvas base size | 1280×720, responsive letterbox | Common browser size |
| Camera | Close, low-angle, target above frog, deadzone, clamp to place bounds | Frog-scale view |
| Fixed timestep | 1/60 s with interpolation | Deterministic physics |
| Random source | Deterministic xorshift32 seeded per run only for ambient particles; no gameplay randomness | No random eating, no hidden unfairness |
| Audio | Synthesized WebAudio only | No assets required |
| Screens | HTML/CSS only for title/help/end; canvas for game | Required by UX section |
| No HUD | No visible HUD in PLAYING; debug overlay optional | Required by decisions |
| Testing | High-level tests per tier prove contracts | Required by spec |
| Definition of done | Tier-aligned checklists | Required by spec |

## 0.3 Tiers

Priority list. Tier 1 is guaranteed. Higher tiers may be left unbuilt.

| Tier | Segment | Contents | Completion |
| --- | --- | --- | --- |
| 1 | Core playable frog run | Fixed loop, input, camera, P01, P02, P99, Frog Body/Hop, Tongue, Grip, Water, Animal Attention, Failure Recovery, Answer Call, place completion, final ending | Player can start under gutter, finish rooftop pond |
| 2 | Supporting mechanics and expanded run | Eating Body States, Reactive World, Active Environmental Systems, P03-P05, more hazards, optional routes | Full described run begins to exist |
| 3 | Extra systems and soft ladder | Rain and Weather, Soft Ladder and Revisitation, wind, wetness persistence, optional early routes, revisitation | World becomes more systemic and optional |
| 4 | Polish within decisions | Better material tells, audio mix, micro-animation, accessibility fallbacks, performance | No new systems |

---

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Item | Value | Notes |
| --- | --- | --- |
| Simulation step | 1/60 s | Fixed timestep |
| Max physics substeps per render frame | 4 | Prevent spiral |
| Render interpolation | Linear between previous/current physics state | Smooth visuals |
| Coordinate system | x right, y down | Canvas convention |
| Angle | radians, 0 right, positive clockwise | Due y-down |
| World unit | 1 px at camera zoom 1.0 | All physics in px/s |
| Base canvas | 1280×720 | Letterboxed responsive |
| Camera zoom | 1.25 | Close frog scale |
| Visible world at zoom | 1024×576 px | 1280/1.25, 720/1.25 |
| Frog body | 30 px wide, 22 px tall | Collision capsule |
| Frog center | Collision center | Physics uses center |
| Ground crawl speed | 26 px/s | Never “run” |
| Gravity | 1150 px/s² | Default |
| Terminal fall | 700 px/s | Safety |
| Air drag | 0.015 | Very light |
| Ground friction | 260 px/s² deceleration | Stop quickly |
| Camera deadzone | x 180 px, y 120 px | Frog stays mostly centered |
| Camera vertical offset | target y = frog.y - 40 px | Low-angle sky visibility |
| Place bounds | Axis-aligned rectangles | Hard camera clamp |
| RNG | xorshift32 | Deterministic, seed per run |
| Frame counter | integer increment per fixed step | Used for tests |

## 1.2 Important conventions

- All gameplay code runs at fixed 60 Hz.
- Rendering may interpolate but never changes state.
- No pause menu, no time-scaled UI, no menu traversal.
- Browser tab hidden may set `phase=SUSPENDED`; on return it resumes with no simulation catch-up beyond max substeps.
- No gameplay randomness affects mechanics. RNG only for non-mechanical ambient particles.
- No HUD markers. If debug overlay is enabled, it is not part of normal gameplay.
- Every hazard has a physical tell before activation.
- Every fall resolves to a stable perch, safe deposit, or current exit.
- Every place has one and only one `answerNode`.
- A place is completed only by `answerNode + liveChorus + stableReturnRoute + heldCroak`.
- Final P99 has `returnRouteRequired=false`.
- Physical changes persist for the session unless a place reset is explicitly requested by debug.
- Eating is optional and never required for completion.
- No animal can be defeated.
- No object can be collected for score.
- No UI marker may point to an anchor, goal, hazard, safe perch, or completion.
- All sounds are synthesized.
- All UI screens are HTML/CSS only. The game world is canvas.
- Input is edge-triggered for taps and level-triggered for holds.

---

# 2. CONTRACTS

## 2.1 Module layout

```text
index.html
style.css
src/
  main.js
  boot.js
  game.js
  state.js
  input.js
  engine.js
  physics.js
  collision.js
  frog.js
  tongue.js
  grip.js
  water.js
  animals.js
  answer.js
  route.js
  places.js
  objects.js
  weather.js
  audio.js
  render.js
  ui.js
  debug.js
  tests.js
  util/
    rng.js
    math.js
    time.js
```

| File | Responsibility |
| --- | --- |
| `main.js` | Boot, canvas, loop, error boundary |
| `game.js` | Top-level phase update, place loading, run lifecycle |
| `state.js` | Global state records, reset, safe perch tracking |
| `input.js` | Keyboard mapping, edge/level state, debug input functions |
| `engine.js` | Fixed loop, interpolation, frame counter |
| `physics.js` | Rigid body, impulses, gravity, drag, constraints |
| `collision.js` | Capsule vs tile/object, surface normals, material lookup |
| `frog.js` | Frog states, crouch-hop, crawl, body states |
| `tongue.js` | Probe, food grab, anchor commit, rope, swing, yank |
| `grip.js` | Surface grip, climb, temporary surfaces, slides |
| `water.js` | Float, paddle, currents, safe deposit, exit edges |
| `animals.js` | Cat, heron, fish attention and states |
| `answer.js` | Croak hold, chorus response, place completion |
| `route.js` | Stable return route graph verification |
| `places.js` | Place definitions, thresholds, load/unload, rest nodes |
| `objects.js` | Reactive objects, physical properties, persistent changes |
| `weather.js` | Rain, wind, wetness, puddles, weather fronts |
| `audio.js` | Synthesized sounds, ambient mix, noise propagation |
| `render.js` | Parallax, camera, world draw, no HUD markers |
| `ui.js` | HTML screens, state machine, no gameplay HUD |
| `debug.js` | Debug overlay and debug API |
| `tests.js` | Test harness and high-level tests |

## 2.2 Global context

All fields below must exist in `state` or in modules that are reachable from `game.state`.

| Path | Type | Required fields | Used by |
| --- | --- | --- | --- |
| `state.phase` | enum | `BOOT`, `TITLE`, `HOW_TO`, `PLAYING`, `ENDING`, `SUSPENDED`, `ERROR` | UI, game loop |
| `state.frame` | int | fixed step counter | tests, audio |
| `state.time` | float | seconds | systems |
| `state.rng` | object | `seed`, `next()`, `range()` | ambient, deterministic tests |
| `state.input` | object | `keyboard`, `crouch`, `tongueTap`, `tongueHold`, `callHold`, `aim`, `move`, `up`, `down`, `restartDebug` | all input rules |
| `state.camera` | object | `x`, `y`, `zoom`, `targetX`, `targetY`, `shake`, `interpolation` | render |
| `state.currentPlace` | string | place id | places, answer, route |
| `state.lastSafePerch` | object | `placeId`, `objectId`, `x`, `y`, `timestamp`, `valid` | failure recovery |
| `state.frog` | object | see Frog Record | all core systems |
| `state.world` | object | `objects`, `surfaces`, `hazards`, `animals`, `water`, `audioNodes` | gameplay |
| `state.places` | map | all place records | places, route, answer |
| `state.route` | object | `currentGraph`, `lastCheck`, `reachable` | answer, debug |
| `state.weather` | object | `state`, `wetness`, `particles`, `wind`, `rain` | weather, surfaces |
| `state.answer` | object | `placeId`, `nodeId`, `holding`, `held`, `interrupted`, `completed`, `restNode` | answer |
| `state.audio` | object | `mix`, `ambient`, `noiseEvents`, `lastNoise` | audio, animals |
| `state.debug` | object | `enabled`, `overlay`, `selectedEntity`, `testMode` | debug, tests |

### Frog Record

| Field | Type | Meaning |
| --- | --- | --- |
| `frog.pos` | `{x,y}` | center px |
| `frog.vel` | `{x,y}` | px/s |
| `frog.facing` | int | -1 left, 1 right |
| `frog.grounded` | bool | on stable surface |
| `frog.state` | enum | `IDLE`, `CROUCH`, `AIR`, `GRIP`, `SWIM`, `TONGUE`, `CAUGHT`, `SETTLE` |
| `frog.crouch` | object | `active`, `time`, `charge`, `aim` |
| `frog.charge` | float | 0..1 |
| `frog.bodyState` | enum | `NORMAL`, `SNEEZING`, `SLUGGISH`, `BUZZED` |
| `frog.bodyStateTimer` | float | seconds |
| `frog.tongue` | object | see Tongue Record |
| `frog.grip` | object | see Grip Record |
| `frog.water` | object | see Water Record |
| `frog.lastSafePerch` | object | duplicate of state for convenience |
| `frog.caughtBy` | enum/null | `CAT`, `HERON`, `FISH`, `NONE` |
| `frog.callHeld` | float | seconds |
| `frog.isCalling` | bool | held croak |
| `frog.throatSwelling` | float | 0..1 visual tell |
| `frog.eyeTarget` | object | nearest threat |

### Tongue Record

| Field | Type | Meaning |
| --- | --- | --- |
| `tongue.state` | enum | `IDLE`, `EXTEND`, `PROBE`, `EAT`, `COMMIT`, `ROPE`, `RETRACT` |
| `tongue.tip` | `{x,y}` | current tip |
| `tongue.length` | float | current length px |
| `tongue.maxLen` | float | 220 |
| `tongue.target` | object/null | food or anchor |
| `tongue.anchor` | object/null | committed anchor |
| `tongue.commitTimer` | float | hold-to-commit timer |
| `tongue.loadTimer` | float | weak anchor failure timer |
| `tongue.foodTimer` | float | eat animation timer |

### Grip Record

| Field | Type | Meaning |
| --- | --- | --- |
| `grip.active` | bool | on climbable surface |
| `grip.surfaceId` | string | object/surface id |
| `grip.normal` | `{x,y}` | surface normal |
| `grip.tangent` | `{x,y}` | allowed slide direction |
| `grip.breakTimer` | float | temporary surface timer |
| `grip.slideVel` | float | along tangent |

### Water Record

| Field | Type | Meaning |
| --- | --- | --- |
| `water.inWater` | bool | true if center below water surface |
| `water.surfaceY` | float | current water surface |
| `water.current` | `{x,y}` | px/s |
| `water.submerged` | bool | below surface |
| `water.noExitTimer` | float | seconds without exit |
| `water.safeDeposit` | object | target perch |

## 2.3 Module specifics

| Module | Required functions |
| --- | --- |
| `engine.js` | `initLoop()`, `step(dt)`, `render(alpha)`, `setPhase(phase)`, `requestResume()` |
| `input.js` | `bindKeyboard()`, `isDown(action)`, `justPressed(action)`, `release(action)`, `getAimVector()`, `getMoveVector()`, `debugInput(action)` |
| `physics.js` | `applyImpulse(body, imp)`, `addGravity(body)`, `applyDrag(body)`, `clampVelocity(body)`, `integrate(body, dt)` |
| `collision.js` | `capsuleVsWorld(frog)`, `surfaceAt(point)`, `normalAt(point)`, `materialAt(point)`, `lineOfSight(a,b,cover)` |
| `frog.js` | `updateFrog(dt)`, `startCrouch()`, `releaseCrouch()`, `applyCrawl()`, `setBodyState(type)`, `clearBodyState()`, `canHop()`, `canGrip()`, `canSwim()` |
| `tongue.js` | `probe()`, `commitIfAnchor()`, `attachFood(target)`, `attachAnchor(target)`, `updateRope(dt)`, `releaseRope()`, `yank(target, impulse)`, `breakAnchor(reason)` |
| `grip.js` | `enterGrip(surface)`, `exitGrip()`, `moveAlongGrip(input,dt)`, `temporarySurfaceUpdate(dt)`, `breakSurface(surface)`, `isClimbable(surface)` |
| `water.js` | `enterWater(water)`, `exitWater()`, `updateFloat(dt)`, `updatePaddle(input,dt)`, `applyCurrent(water,dt)`, `findSafeDeposit()`, `safeDeposit(frog)` |
| `animals.js` | `updateCat(state,dt)`, `updateHeron(state,dt)`, `updateFish(state,dt)`, `addNoise(event)`, `addVisualAttention(source)`, `catchFrog(animal)`, `resetFromCatch(animal)` |
| `answer.js` | `startCall()`, `updateCall(dt)`, `interruptCall(reason)`, `canCallAt(node)`, `completePlace(place)`, `makeRestNode(node)`, `finalEnd()` |
| `route.js` | `buildGraph(place)`, `updateEdgePassability(edge)`, `isReturnRoutePassable(place)`, `safeDropEdge(a,b)`, `safeCurrentEdge(edge)`, `stableSurface(surface)`, `findPath(from,to)` |
| `places.js` | `loadPlace(id)`, `unloadPlace(id)`, `crossThreshold(id)`, `getAnswerNode(id)`, `getRestNode(id)`, `getReturnTarget(id)`, `markCompleted(id)` |
| `objects.js` | `updateReactive(dt)`, `pullObject(obj,impulse)`, `wetSurface(obj,amount)`, `breakObject(obj)`, `startSprinkler(obj)`, `pullCork(obj)`, `tipRainBarrel(obj)`, `disturbBranch(obj)` |
| `weather.js` | `startFront(place)`, `updateWeather(dt)`, `wetSurfaces(dt)`, `expandPuddles(dt)`, `startWind()`, `applyWind(frog,dt)` |
| `audio.js` | `playSound(name,pos)`, `playAmbient(place)`, `stopAmbient()`, `emitNoise(event)`, `playChorus(place,node)`, `playFullChorus()` |
| `render.js` | `updateCamera(dt)`, `drawWorld()`, `drawParallax()`, `drawPlace()`, `drawFrog()`, `drawAnimals()`, `drawWeather()` |
| `ui.js` | `showTitle()`, `showHowTo()`, `showPlaying()`, `showEnding()`, `hideUI()`, `restartRun()` |
| `debug.js` | `toggleDebug()`, `getFrogState()`, `getTongueState()`, `getGripState()`, `getWaterState()`, `getAnimalState(id)`, `getAnswerState(place)`, `getRouteState(place)`, `getWeatherState()`, `getInputState()` |
| `tests.js` | `runTier1Tests()`, `runTier2Tests()`, `runTier3Tests()` |

---

# 3. VISUAL SPEC

The game is a readable, low-angle side-view frog-scale world. The player sees wet surfaces, parallax depth, and next-place silhouettes rather than UI. The palette is dusk-to-night rain: slate, moss, wet glass, moonlight. Everything is drawn to communicate material: thick damp wood holds, fraying paper breaks, glass rejects, wet stone slides or grips by texture, water ripples and carries, animals have visible attention tells. No arrows, icons, markers, bars, or completion prompts exist in normal play.

## Lighting and atmosphere

| Element | Look |
| --- | --- |
| Time of day | Dusk to moonlit night |
| Key light | Cold moonlight from upper right, low intensity |
| Fill | Dim ambient teal |
| Wet highlights | Specular streaks on rain, glass, wet metal |
| Depth fog | Distant layers desaturated to #1a2530 |
| Rain | Thin droplets, ripples, mist; no HUD weather icon |
| Sound-visual sync | Drips, splashes, ripples, cat eyes, heron shadow, fish wake |
| Mood | Quiet, wet, patient; hazards feel physical, not arcade |

## Space

| Layer | Parallax factor | Content |
| --- | --- | --- |
| Far sky | 0.05 | Moon, clouds, distant rooftops |
| Mid city/garden | 0.18 | Distant silhouettes, next place goal |
| Near world | 1.0 | Playable platforms, water, animals, objects |
| Foreground | 1.25 | Blurred vines, rain, water edges |

Camera rules:

- Camera target is frog center plus `(0,-40)`.
- Deadzone: x 180, y 120.
- Max camera speed: 1800 px/s.
- Clamp to place bounds.
- During final chorus, camera slowly rises to reveal full pond; no UI.

## Visual recipe table

| Visual | Appearance | Gameplay rule |
| --- | --- | --- |
| Safe anchor | Thick, damp, grain, dark wet wood/stone/metal edge; small sticky contact on tongue probe | Can commit tongue and support frog |
| Weak anchor | Dry, torn, translucent, fraying, cracked, loose; flutters under tongue tap | May break under load |
| Unusable anchor | Smooth glass, polished plastic, open water, air; tongue tip slides or ignores | Cannot stick |
| Climbable surface | Matte texture, visible grain, damp moss/brick/bark/rubber/grate | Grip enters |
| Nonclimbable surface | Smooth, oily, polished, water-filmed, glass | Slide/fall |
| Temporary surface | Sag, crack, dry rot, crumbling edge | Brief grip then fail |
| Water surface | Dark reflective, ripples, floating leaves | Float/paddle; not a platform |
| Current | Directional ripples, carried debris, pipe gurgle | Adds force |
| Answering Node | Stable perch beside live water body; faint concentric ripples, ambient chorus audio | Completion perch |
| Rest Node | Same stable perch after completion; chorus becomes friendly | Safe perch |
| Cat | Still silhouette, eyes follow, throat low, paw shift | Attention states |
| Heron | Tall silhouette, shadow ellipse, slow head turn | Open ground attention |
| Fish | Ripple rings, subtle wake, lily root cover | Water attention |
| Insect alive | Twitch, buzz motion, leg kick | Eating effect possible |
| Insect dead/stunned | Still, no buzz | No eating effect |
| Sprinkler tell | Valve tremor, pressure hiss, droplets before spray | Active hazard |
| Rain tell | Cloud shadow, first large drops, wind shift, surface shine | Weather state |
| Wind tell | Flags, leaves, rain drift, ripples | Horizontal force |
| Goal | Distant pond, rooftop, lily ring, faint chorus | Route direction |
| No HUD | No icons, no bars, no arrows, no counters | Required |

---

# 4. GAMEPLAY SPEC

The game is a forgiving but weighty real-time platforming puzzle about a frog reading rain-soaked places at its own scale. The player crouch-hops, probes with the tongue, commits to anchors, climbs textured wet surfaces, swims weakly, avoids animal attention, changes small physical conditions, and only completes a place by holding a croak at its one Answering Node after a stable way back exists. The final rooftop pond ends the run when the full chorus answers.

## 4.1 Records and rosters

### Player

| Record | Value |
| --- | --- |
| Player | Small wet frog |
| Name | None |
| Costume | None |
| Abilities | Hop, crawl slow, grip, tongue, swim, call |
| Health | None |
| Score | None |
| Required eating | None |
| Death | None |

### Animal roster

| Animal | Tier | Count in Tier1 | Count full run | States |
| --- | --- | --- | --- | --- |
| Cat | 1 | 1 | 2 | Unaware, Watching, Prowling, Strike |
| Heron | 1 | 1 | 2 | Hunting, Shadowed, Strike |
| Fish | 1 | 1 | 4+ | Idle, Alerted, Lunge |

### Hazard roster

| Hazard | Tier | Physical tell | Effect |
| --- | --- | --- | --- |
| Sprinkler | 2 | Valve tremor, hiss, wet arcs | Wet surfaces, noise, knock light objects |
| Rain barrel tip | 2 | Slosh, tilt, creak | Pour current, carry frog |
| Pipe/drain current | 1/2 | Gurgle, spit, ripple | Directional water push |
| Crumbling ledge | 1 | Crack, sag, dry rot | Temporary grip then break |
| Slippery surface | 1 | Water film, shine | Slide/fall |
| Wind | 3 | Flags, rain drift, ripples | Horizontal force |
| Rain front | 3 | Cloud shadow, first drops, wind shift | Wet surfaces, puddles, currents |

### Pickups / edible insects

| Item | Tier | Effect | Required | Count Tier1 | Count full |
| --- | --- | --- | --- | --- | --- |
| Fly | 2 | Sneeze recoil | No | 2 | 6 |
| Beetle | 2 | Sluggish | No | 2 | 4 |
| Wasp | 2 | Buzzed next jump | No | 1 | 4 |
| Caterpillar | 2 | Not eaten; knocks off branch | No | 1 | 2 |

### World object roster

| Object | Class | Physical properties | Use |
| --- | --- | --- | --- |
| Rain barrel | Static/reactive | Stable unless rim weighted; tip threshold 1.0s or impulse 150 | Start perch, water source, hazard |
| Gutter | Static | Narrow passage, can carry water | Route, current |
| Drainpipe | Static/active | Gurgle, spitting, current | Passage, current |
| Stone path | Static | Wet or dry texture determines grip | Ground route |
| Greenhouse glass | Static | Smooth, nonclimbable, tongue rejects | Blocker, visual |
| Dripping vine | Reactive | Thick damp safe; rotten weak | Anchor, wet source |
| Puddle | Active | Expands with rain, leaf platforms possible | Water hazard |
| Wet crate | Static/reactive | Solid stable; rotten temporary; pushable | Platform |
| Branch | Reactive | Strong if thick damp; yankable, can dip/break | Anchor, swing |
| Damp wall | Reactive | Wet textured climbable; dry may not be | Teaching grip |
| Lily pad | Reactive | Fresh floats; waterlogged weak | Floating platform |
| Tin can | Reactive | Mass 1.5, noise radius 360 | Distraction, weak anchor |
| Garden hose | Reactive/anchor | Braided strong; loose moves | Anchor, water |
| Greenhouse frame | Static/reactive | Dry textured grips; condensation slippery | Surface |
| Mossy stone | Static/reactive | Damp textured climbable | Perch |
| Fence rail | Static/reactive | Grain determines safe/rotten | Anchor/perch |
| Spider web | Reactive | Strong silk safe; thin weak | Anchor |
| Koi pond | Active | Fish attention, ripples | Hazard |
| Cat door | Static/narrow | Cat sight line, cover | Passage |
| Twig | Reactive | Thick damp safe; dry weak | Anchor, object |
| Hanging wire | Reactive | Strong visible safe; loose moves | Anchor, noise |
| Bottle cap | Reactive | Mass 0.5, noise, weak anchor | Object |
| Insect legs | Food | Tongue catch | Eating state |
| Cracked tile edge | Reactive | Weak anchor, break under load | Weak anchor |
| Glass | Static | Unusable anchor, nonclimbable | Barrier |
| Open water | Active | Unusable anchor, swim, current | Landmark, hazard |
| Cork | Reactive | Pullable, blocks drain | Physical chain |
| Leaf | Reactive | Floats, light, sinks if waterlogged | Raft, start perch |

## 4.2 Frog Body and Hop — Tier 1

### Rules

| Rule | Number |
| --- | --- |
| Input: hold Space/J crouch, release hop | `crouchHeld` |
| Input: arrows/WASD aim while crouched | aim vector |
| Input: arrows/WASD crawl when not crouched | max 26 px/s |
| Crouch min | 0.10s |
| Crouch max | 0.65s |
| Charge power | 190 + charge * 240 px/s |
| Default aim with no input | `(facing*0.25, -1)` |
| Aim if only horizontal | `(inputX, -1)` normalized |
| Aim if only vertical | `(0, inputY)` normalized |
| Air steering | none |
| Wind/current may alter body | yes |
| Landing auto-grip if climbable and normal velocity < 600 | yes |
| Landing on nonclimbable | bounce 0.15, slide |
| No run state | max crawl 26 px/s |
| Body is light | air drag 0.015 |
| Hop is committed | no air control |

### Crouch-hop state machine

| State | Entry | Exit |
| --- | --- | --- |
| `IDLE` | grounded, not crouching | `CROUCH` on Space |
| `CROUCH` | Space held | `AIR` on release |
| `AIR` | airborne | `IDLE`, `GRIP`, `SWIM`, `TONGUE` |
| `SETTLE` | final chorus | end |

### Body states

| State | Trigger | Effect | Duration |
| --- | --- | --- | --- |
| `SNEEZING` | eat live fly | backward impulse 120, control jitter 0.15s | 0.15s |
| `SLUGGISH` | eat live beetle | speed 0.6, hop power 0.75 | 4.5s |
| `BUZZED` | eat live wasp | next jump sideways impulse 180, reduced air control | next jump or 1.2s |

No body state unlocks permanent ability.

## 4.3 Tongue — Tier 1

### Input

| Input | Action |
| --- | --- |
| Tap Z/K | tongue flick/probe |
| Hold Z/K after tip contacts safe anchor | commit anchor |
| Hold Z/K while attached | keep rope |
| Release Z/K | release rope |
| While attached, arrows | pendulum swing |
| While attached, Up | pull toward anchor if close and strong |

### Rules

| Rule | Number |
| --- | --- |
| Max tongue length | 220 px |
| Tip speed | 1500 px/s |
| Probe tap duration | 0.12s |
| Commit hold threshold | 0.18s after safe anchor contact |
| Food catch radius | 12 px |
| Anchor contact radius | 16 px |
| Food target size | width/height <= 24 px |
| Anchor requires structure | strength >= 0.6 |
| Safe anchor visual | thick, damp, grain, firm recoil |
| Weak anchor visual | fraying, translucent, dry, cracked |
| Unusable anchor visual | smooth, hollow, water, air |
| Weak anchor break load time | 0.40s |
| Weak anchor break impulse | 240 |
| Rope max length | 220 px |
| Rope tangential input accel | 900 px/s² |
| Pull-up speed | 130 px/s if distance < 150 and anchor strength >= 0.7 |
| Release impulse if aim input | 160 * aim |
| Yank impulse | 180 |
| Movable object yank mass limit | 6 |
| Heavy object mass limit | >12 no move |
| Overextend failure | distance > 230 |
| Hazard hit | tongue releases |
| Stable surface grab | ends rope |

### Food behavior

| Food | Animation tell | Effect |
| --- | --- | --- |
| Live fly | twitching, buzzing | sneeze |
| Live beetle | kicking legs | sluggish |
| Live wasp | buzzing, hovering | buzzed |
| Dead/stunned/knocked | still | no effect |

## 4.4 Grip and Climbing — Tier 1

### Rules

| Rule | Number |
| --- | --- |
| Auto-enter grip | pads meet climbable surface |
| Climb speed up | 55 px/s |
| Descend speed down | 80 px/s |
| Slide if not climbing | 120 px/s max |
| Jump releases grip | Space min hop 190 |
| Hazard contact breaks grip | yes |
| Climbable if wet textured | wetness >= 0.25 and texture flag |
| Dry textured metal climbable | yes |
| Condensation metal slippery | wetness >= 0.8 or water film |
| Smooth/oily/polished nonclimbable | yes |
| Temporary surface break time | 0.35s |
| Rotten bark break time | 0.45s |
| Cracked tile break time | 0.30s |
| Stable wall rest | yes |
| Surface becomes slippery | slide acceleration 450 |
| Surface breaks | remove surface, spawn debris |

### Material table

| Surface | Dry | Wet |
| --- | --- | --- |
| Mossy stone | not climbable unless damp | climbable |
| Damp brick | climbable if textured | climbable |
| Rough bark | climbable | climbable unless rotten |
| Rubber | climbable | climbable |
| Dry textured metal | climbable | may become slippery if water film |
| Metal grate | climbable | climbable |
| Smooth metal | not climbable | not climbable |
| Glass | not climbable | not climbable |
| Polished plastic | not climbable | not climbable |
| Wet smooth tile | not climbable | slippery |

## 4.5 Water and Wet Surfaces — Tier 1

### Rules

| Rule | Number |
| --- | --- |
| Enter water | center y > surface y |
| Float | y constrained to surface with buoyancy 1.2 |
| Paddle target speed | 45 px/s |
| Paddle drag | 180 |
| Submerge | hold Down, depth 50 px |
| Cannot jump/stick in water | true |
| Current adds velocity | yes |
| Current max normal | 95 px/s safe, >95 unsafe |
| Safe current exit | within 200 px |
| Exit edge | damp textured edge only |
| Smooth/dry edge | slip |
| No exit after | 2.5s current carry to safe deposit |
| Safe deposit | nearest stable perch or terminal |
| Puddle platform | only via leaf/debris/raised water |
| Open water not platform | true |
| Answer call from open water | not allowed |

### Wetness model

| State | Wetness | Surface effect |
| --- | --- | --- |
| Dry | 0.0 | default material |
| Damp | 0.25–0.7 | textured climbable |
| Water film | 0.8–1.0 | smooth surfaces slippery |
| Glass | any | always nonclimbable/unusable |

## 4.6 Animal Attention — Tier 1

### Cat

| State | Threshold | Behavior | Tell |
| --- | --- | --- | --- |
| Unaware | 0.00–0.30 | idle | eyes not following |
| Watching | 0.30–0.60 | head follows, throat low | eye motion |
| Prowling | 0.60–0.85 | moves to last known | paw shift, crouch |
| Strike | >=0.85 and dist <220 | telegraph 0.4s, lunge 430 px/s | paw press, tail |

| Cat rule | Number |
| --- | --- |
| Sight radius | 360 px |
| Line of sight blocked by cover | yes |
| Attention while moving in sight | +0.50/s |
| Attention while still in sight | +0.15/s |
| Noise attention | event values |
| Decay not visible | -0.25/s |
| Decay covered | -0.50/s |
| Decay far | -0.35/s |
| Prowl speed | 55 px/s |
| Catch radius | 28 px |
| Bat impulse | 160 |
| Catch result | reset to last safe perch |
| Strike cooldown | 2.5s |

### Heron

| State | Threshold | Behavior | Tell |
| --- | --- | --- | --- |
| Hunting | 0.00–0.35 | scans open ground | shadow drift |
| Shadowed | 0.35–0.80 | shadow tightens | shadow ellipse shrinks |
| Strike | >=0.80 and exposed | telegraph 0.35s, dive 650 px/s | shadow locks |

| Heron rule | Number |
| --- | --- |
| Shadow radius | 220 px |
| Attention open moving | +1.20/s |
| Attention open still | +0.30/s |
| Attention covered decay | -0.80/s |
| Attention no shadow decay | -0.50/s |
| Strike range | 150 px |
| Catch radius | 26 px |
| Catch result | dark swallow, cough up outside radius 320 |
| Distraction | noise/branch disturbance moves shadow target |
| Strike cooldown | 3.5s |

### Fish

| State | Threshold | Behavior | Tell |
| --- | --- | --- | --- |
| Idle | 0.00–0.35 | patrol | calm ripple |
| Alerted | 0.35–0.80 | face frog, circling | ripple rings |
| Lunge | >=0.80 and within 140 | lunge 280 px/s | wake |

| Fish rule | Number |
| --- | --- |
| Attention moving in water | +0.90/s |
| Attention ripples | +0.60/s |
| Still decay | -0.40/s |
| Lily root cover decay | -1.00/s |
| Lunge bump impulse | 140 toward current/edge |
| Lunge cooldown | 2.0s |
| Not death | yes |

## 4.7 Failure Recovery and Safe Perch — Tier 1

### Safe perch definition

A safe perch is the most recent stable, weight-bearing contact that is:

- not part of a moving hazard,
- not in an active hazard attack zone,
- not structurally failing,
- not water unless attached to a stable edge,
- not a temporary broken surface.

Examples: dry ledge, sturdy branch, stone lip, cork, stable wall grip, lily root, rest node.

### Tracking

| Event | Update |
| --- | --- |
| Stable grounded contact for 0.30s | set `lastSafePerch` |
| Stable wall grip for 0.50s | set `lastSafePerch` |
| Surface becomes unsafe | invalidate last safe perch |
| Place completed | rest node becomes safe |
| Hazard active radius overlaps | not safe |

### Recovery

| Failure | Recovery |
| --- | --- |
| Missed tongue | dangle 0.25s, fall, normal recovery |
| Bad hop | slide/fall, normal recovery |
| Cat catch | bat impulse 160, reset to last safe perch |
| Heron catch | dark swallow 0.4s, cough up nearest safe perch outside strike zone |
| Fish lunge | bump toward current/edge, not reset |
| Water no exit | current carries to guaranteed safe deposit or last stable node |
| No safe perch exists | place at nearest rescue ledge |
| Below bounds | place at last safe perch or rescue ledge |

No death, no score, no timer penalty.

## 4.8 Answer Call and Place Completion — Tier 1

### Answering Node rules

| Rule | Number |
| --- | --- |
| One Answering Node per place | enforced |
| Node is stable perch beside water/perch | yes |
| Node has live chorus | audio flag |
| Frog must be out of water | yes |
| Frog must be on stable surface | yes |
| Hold call key | C/L |
| Held croak duration | 0.75s |
| If route exists | chorus answers after 0.75s, then 0.9s response, place complete |
| If route missing | after 0.75s no chorus, old soundscape continues |
| If hazard interrupts | call reset, place incomplete |
| Hazard interruption radius | 180 px around node |
| Croak noise radius | 560 px |
| Croak attention per 0.15s held | +0.50 |
| Successful completion | node becomes Rest Node |
| Rest node re-call | friendly chorus only |
| Final P99 | no return route required |

### Stable return route rules

A stable return route is a continuous survivable path from the Answering Node to the place’s return target using:

- stable anchors,
- climbable surfaces,
- safe drops,
- safe currents.

| Edge type | Passable condition |
| --- | --- |
| Ground | stable surface, no active hazard |
| Climb | surface climbable, no hazard |
| Safe drop | dy <=110, dx <=180, landing stable, no hazard within 120 |
| Safe current | current <=95, exit within 200, no hazard |
| Tongue anchor | anchor exists, strength >=0.6, not overextended |
| Yank/rearrange | required object moved into safe state |
| Wait/distract | hazard state not active in route |

### Completion sequence

1. Frog reaches Answering Node.
2. Route graph is checked.
3. Frog holds C.
4. If route invalid, after 0.75s node stays silent.
5. If route valid, after 0.75s chorus answers.
6. Place marked completed.
7. Answering Node becomes Rest Node.
8. Final P99: full chorus and `ENDING`.

No second call is needed if route already exists.

## 4.9 Eating Body States — Tier 2

### Rules

| Rule | Number |
| --- | --- |
| Eating required | never |
| Eating scored | never |
| Effects permanent | never |
| Random effects | never |
| Live fly | sneeze |
| Live beetle | sluggish |
| Live wasp | buzzed |
| Dead/stunned/knocked | no effect |
| Body state max | one active |
| Eating can help traversal | yes |
| Eating can ruin traversal | yes |

### Insect behavior

| Insect | Spawn pattern | Movement |
| --- | --- | --- |
| Fly | near light/leaf gaps | twitchy hover, speed 35 |
| Beetle | under surfaces | slow crawl, speed 12 |
| Wasp | near flowers/vents | hover, speed 45 |
| Caterpillar | on branch | slow crawl, speed 8 |

## 4.10 Reactive World — Tier 2

### Object classes

| Class | Examples | Rules |
| --- | --- | --- |
| Static | walls, floors, solid stone, large pipes | fixed |
| Reactive | corks, branches, leaves, wet surfaces, light objects | changed by physical cause |
| Active | animals, rain, wind, currents, sprinkler timers | own behavior |

### Physical cause model

| Cause | Effect |
| --- | --- |
| Pull | move object, yank, drag, tilt |
| Land | impulse, noise, knock |
| Splash | wet, ripple, move light object |
| Drip | wet surface |
| Weight | tip, sink, break |
| Noise | animal attention |
| Water | current, float, wet |
| Break | debris, removed surface |

### Object physical table

| Object | Mass | Strength | Noise radius | Break threshold |
| --- | --- | --- | --- | --- |
| Cork | 2.0 | 0.7 | 80 | pullable |
| Leaf | 1.0 | 0.2 | 20 | sinks after 120s wet |
| Branch strong | 12.0 | 0.9 | 120 | impulse >350 |
| Branch rotten | 4.0 | 0.3 | 120 | impulse >120 |
| Tin can | 1.5 | 0.5 | 360 | impulse >250 |
| Bottle cap | 0.5 | 0.2 | 220 | impulse >100 |
| Caterpillar | 0.2 | 0.1 | 30 | knock off branch |
| Lily pad fresh | 3.0 | 0.6 | 50 | impulse >220 |
| Lily pad waterlogged | 1.0 | 0.2 | 50 | sinks |
| Spider silk strong | 0.4 | 0.9 | 10 | impulse >400 |
| Spider silk thin | 0.1 | 0.2 | 10 | impulse >80 |
| Wet crate solid | 20.0 | 0.9 | 100 | push speed 20 |
| Wet crate rotten | 8.0 | 0.3 | 100 | impulse >150 |

## 4.11 Active Environmental Systems — Tier 2

### Sprinkler

| State | Duration | Tell | Effect |
| --- | --- | --- | --- |
| Dormant | 10–14s | dry valve | none |
| Pressurized | 2.0s | hiss, tremor | warning |
| Spraying | 4.0s | arcs, droplets | wet radius 260, knock mass <=1.2, noise +0.4 |
| Spent | 6.0s | drip | none |

Triggerable by cord, cork, loose part, impact.

### Rain barrel

| State | Trigger | Effect |
| --- | --- | --- |
| Stable | default | holds water |
| Unbalanced | frog rim weight 1.0s, impulse >150 | creak, slosh |
| Tipping | 1.2s animation | pour current 100, float leaves |
| Fallen | settled | remains wet/current source |

### Pipes and drains

| State | Tell | Effect |
| --- | --- | --- |
| Gurgle | bubbly gurgle | pressure |
| Spitting | burst droplet | impulse 80 |
| Blocked | quiet, dry | no current |
| Flowing | gurgle + ripple | current 80 |
| Empty | silent | no current |

Pull cork starts flow. Block opening stops flow.

### Wind — Tier 3

| State | Duration | Tell | Effect |
| --- | --- | --- | --- |
| Calm | 6–10s | still | none |
| Building | 2.0s | flags twitch | none |
| Gusting | 1.2s | flags/leaves/rain drift | horizontal accel 260 |
| Lull | 3.0s | settle | none |

## 4.12 Rain and Weather — Tier 3

### States

| State | Duration | Tell | Effect |
| --- | --- | --- | --- |
| Dry | varies | no shine | default |
| First drops | 1.0s | large drop, shadow | wetness +0.1 |
| Drizzle | 10s | fine rain | wetness +0.2/s |
| Steady | 20s | rain sheet | wetness +0.4/s, puddles expand |
| Downpour | 15s | heavy rain, wind | wetness +0.6/s, currents |
| Tapering | 8s | thinning | wetness decays slowly |

### Surface effects

| Surface | Wetness effect |
| --- | --- |
| Textured | climbable at wetness >=0.25 |
| Smooth | slippery at wetness >=0.8 |
| Glass | always unusable |
| Puddles | expand radius +8 px/s steady, max +40% |
| Leaves | float |
| Gutters | carry currents |

### Animal effects

| Animal | Rain effect |
| --- | --- |
| Cat | seeks cover, attention from covered movement +0.2/s |
| Heron | less active under cover, shadow moves to openings |
| Fish | more alert to ripples +0.2/s |
| Player noise | small noise masked 50%; croak/splash/metal not masked |

## 4.13 Soft Ladder and Revisitation — Tier 3

### Rules

| Rule | Number |
| --- | --- |
| Places hard-locked | no |
| Later place available | if physically reachable and answer node live |
| Main route | follow heard chorus |
| Optional routes | steep, exposed, hazard-heavy |
| Optional early completion | allowed if answer + route rules pass |
| No live chorus | never Answering Node |
| Physical dead end | remains dead end until physical change |
| Revisit completed places | yes |
| Persistent changes | yes |
| Boundaries visible/narrow | yes |

### Ambient call cue

| Element | Value |
| --- | --- |
| Answer node call audible radius | 700 px |
| Volume falloff | linear to 0 at 700 |
| Direction cue | audio panning + visual distant silhouette |
| No UI marker | true |

## 4.14 Places, run progression, difficulty

### Place graph

| Place | Name | Tier | Bounds | Start | Answer Node | Return target | Threshold |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P01 | Rain Barrel Gutter | 1 | 1500×1000 | leaf in barrel, then stone rim | stable gutter lip beside puddle | P01 stone rim | drainpipe to P02 |
| P02 | Damp Wall Stone Path | 1 | 1700×1400 | drain exit stone lip | mossy stone lip beside puddle | P01 rest node | Tier1 final vent to P99; Tier2 also to P03 |
| P03 | Wet Crate Alley | 2 | 1800×1600 | crate ledge | cork/rain-barrel lip beside overflow | P02 rest node | branch gap to P04 |
| P04 | Branch Vine Trellis | 2 | 2000×1800 | branch perch | fence rail/lily root beside pond | P03 rest node | greenhouse drain to P05 |
| P05 | Greenhouse Lily Basin | 2 | 2200×1800 | greenhouse frame ledge | lily root/cork beside koi pond | P04 rest node | vent to P99 |
| P99 | Moonlit Rooftop Pond | 1 | 2400×2000 | rooftop ledge | stone lip beside pond | none | none |

### P01 Rain Barrel Gutter

| Element | Value |
| --- | --- |
| Start | leaf at (120,820), barrel water surface y=780 |
| First stable perch | stone rim at (160,700) |
| First gap | 120 px from rim to crate |
| Teaching objects | leaf rock, crouch-hop, sticky pad, tongue probe, branch swing optional |
| Answer node | gutter lip at (1120,620) beside puddle (1050–1300, y=900) |
| Return route | answer -> safe drop to crate ledge -> climb down -> drain ledge -> barrel rim |
| Hazards | pipe gurgle optional, no active animal |
| Insects | 1 fly, 1 beetle |
| Completion | route exists initially, call once completes |
| Threshold | drainpipe at (1420,760), current 80, safe exit P02 |

### P02 Damp Wall Stone Path

| Element | Value |
| --- | --- |
| Start | stone lip at (120,1100) |
| Teaching | damp wall climb, cat watching, fish ripples, safe return |
| Answer node | mossy stone lip at (1520,760) beside puddle |
| Return target | P01 rest node |
| Route | answer -> climb down damp wall -> safe drop to stone path -> crawl to drain -> current to P01 |
| Hazards | cat at (1300,1250), fish in puddle, but answer perch outside active zones |
| Insects | 1 fly, 1 beetle |
| Completion | route passable because damp wall wet |
| Tier1 threshold | upper vent to P99 |
| Tier2 threshold | main vent to P03 |

### P03 Wet Crate Alley — Tier 2

| Element | Value |
| --- | --- |
| Start | crate ledge left |
| Teaching | temporary crates, sprinkler, rain barrel tip, cat, physical route change |
| Answer node | cork/rain-barrel lip beside overflow |
| Return target | P02 rest node |
| Initial route | dry wall not climbable; return unsafe |
| Physical change | start sprinkler to wet textured wall; then route passable |
| Hazards | 1 sprinkler, 1 cat, tipping barrel, crumbling crates |
| Insects | 2 flies, 1 wasp, 1 beetle, 1 caterpillar |
| Completion | player must create safe return, then call |

### P04 Branch Vine Trellis — Tier 2

| Element | Value |
| --- | --- |
| Start | branch perch |
| Teaching | committed tongue anchors, swinging, wasp optional, heron distraction |
| Answer node | fence rail/lily root beside pond |
| Return target | P03 rest node |
| Hazards | 1 heron, weak branches, rotten vines, wasps |
| Physical change | knock caterpillar, bend branch, distract heron |
| Insects | 2 wasps, 1 fly |
| Completion | route may require branch dip or heron wait |

### P05 Greenhouse Lily Basin — Tier 2

| Element | Value |
| --- | --- |
| Start | greenhouse frame ledge |
| Teaching | glass unusable, condensation slippery, fish attention, lily pads, cork chain |
| Answer node | lily root/cork at pond edge |
| Return target | P04 rest node |
| Hazards | 3 fish, 1 heron, slippery frames, currents, lily pads |
| Physical change | pull cork to stop current, float leaf, wet wall |
| Insects | 2 flies, 1 wasp, 1 beetle |
| Completion | make current exitable, then call |

### P99 Moonlit Rooftop Pond

| Element | Value |
| --- | --- |
| Start | rooftop ledge |
| Goal | moonlit pond, ring of lilies, full chorus |
| Answer node | stable stone lip beside pond |
| Return route | not required |
| Hazards | Tier1: heron in approach, answer perch safe; Tier3 wind optional |
| Fish | present in pond, not active at answer perch |
| Completion | hold croak at answer node, full chorus, end |

### Difficulty progression

| Place | New verb | Hazard complexity | Optional route |
| --- | --- | --- | --- |
| P01 | hop, tongue probe, safe perch | none | branch swing |
| P02 | grip, cat, fish | one animal | direct vent |
| P03 | temporary surfaces, sprinkler, physical route | two hazards | crate skip |
| P04 | committed swing, heron, wasp | two hazards | vine shortcut |
| P05 | glass, current, lily pads, fish | three hazards | roof bypass |
| P99 | final call | approach hazard only | none |

### Feel

The game teaches by consequence. Failure is a slide, a missed tongue, a cat noticing, a heron shadow tightening, a current carrying the frog to a safe edge. The player is never punished with death or score. The reward is noticing: a wet wall becomes climbable, a cork changes a current, a leaf becomes a route, a call answers only after the way back is safe.

---

# 5. CHARACTERS

## 5.1 Frog

### Silhouette

- Low, wide, grounded body.
- Large eyes above shoulders.
- Throat pouch visible when calling or nervous.
- Sticky toe pads visible as tiny suction cups.
- No clothing, no weapons, no human posture.

### States

| State | Animation rule |
| --- | --- |
| `IDLE` | slight breathing, eyes follow nearest threat, throat calm |
| `CROUCH` | legs coil, body lowers 8 px, eyes widen |
| `AIR` | body extends, legs trail, tongue possible |
| `LAND` | squash 2 frames, recovery 0.12s |
| `GRIP` | pads pressed, body flat, eyes scan |
| `SLIDE` | pads slip, body drags, tiny droplets |
| `SWIM` | weak strokes, head above surface |
| `TONGUE` | head turns, tongue extends |
| `ROPE` | body hangs, pendulum |
| `CALL` | throat swells, body braces |
| `CAUGHT` | limp, brief embarrassed stillness |
| `SETTLE` | final rest, slow breathing |

### Facings

- Left facing: x negative.
- Right facing: x positive.
- Eyes track nearest animal attention source.
- Throat swelling maps to `frog.throatSwelling`.

## 5.2 Cat

| State | Animation |
| --- | --- |
| `UNAWARE` | slow blink, tail idle |
| `WATCHING` | head turns, eyes follow, ears forward |
| `PROWLING` | low step, paw shift, tail low |
| `STRIKE` | crouch, paw press, lunge |
| `BAT` | gentle paw, no bite |

## 5.3 Heron

| State | Animation |
| --- | --- |
| `HUNTING` | slow scan, shadow drift |
| `SHADOWED` | shadow ellipse tightens, head lowers |
| `STRIKE` | neck tuck, dive |
| `SWALLOW` | brief dark shape, cough |

## 5.4 Fish

| State | Animation |
| --- | --- |
| `IDLE` | calm glide, ripple |
| `ALERTED` | face, circling, ripple rings |
| `LUNGE` | short burst, wake |

## 5.5 Animals

Animals are not enemies to defeat. They are attention systems. The player can wait, hide, distract, or change environment.

---

# 6. AUDIO

All sounds synthesized via WebAudio. No external assets.

| Sound name | Recipe | When it plays |
| --- | --- | --- |
| `drip` | short sine 420Hz, exponential decay 0.08s, slight slide down | leaf/pipe drip |
| `leafRock` | filtered noise 300–800Hz, bandpass sweep 0.15s | leaf tips, rain barrel wobble |
| `splashSmall` | noise burst 500–2500Hz, decay 0.15s | small hop into water |
| `splashBig` | noise 200–1200Hz + sine 120Hz, decay 0.35s | big splash, barrel |
| `tongueTap` | click 1.2kHz square 0.02s, highpass | tongue probe |
| `tongueSticky` | soft sine 320Hz + noise 0.05s | safe anchor brief contact |
| `tongueAttach` | low thump 120Hz + click | committed anchor |
| `tongueSnap` | crack 800–2000Hz noise 0.08s | weak anchor breaks |
| `ropeTension` | low filtered noise rumble 100–200Hz loop low gain | rope taut |
| `swingAir` | filtered noise sweep 200–900Hz | pendulum |
| `hopCharge` | low sine 60–120Hz rising with charge | crouch |
| `hopRelease` | sine 180Hz + noise 0.1s | hop |
| `landSoft` | sine 90Hz, decay 0.08s | soft landing |
| `landWet` | noise 300–1500Hz, decay 0.12s | wet landing |
| `slide` | filtered noise 400–1200Hz loop | slipping |
| `gripClimb` | tiny clicks 1.5kHz every 0.12s | climbing |
| `crawl` | tiny soft taps 200–500Hz | ground crawl |
| `swimStroke` | low filtered noise 200–800Hz | paddling |
| `currentGurgle` | low sine 80Hz + filtered noise bubbles | flowing pipe |
| `pipeSpit` | burst noise 600–1800Hz, sine 150Hz | pipe spitting |
| `corkPull` | wood knock 220Hz + noise | pulling cork |
| `branchCreak` | filtered saw 90Hz + noise | branch bends |
| `branchSnap` | crack 700–2500Hz | branch breaks |
| `tinCanNoise` | metallic sine 1200/1800Hz, decay 0.4s | tin can touched |
| `bottleCapPing` | sine 2200Hz, decay 0.2s | cap struck |
| `sprinklerPressurize` | rising hiss 200–800Hz | sprinkler warning |
| `sprinklerSpray` | white noise 800–4000Hz loop | sprinkler active |
| `windBuilding` | filtered noise sweep 100–600Hz | wind building |
| `windGust` | noise 200–1200Hz, LFO | gust |
| `rainDrizzle` | low noise 500–2000Hz, low gain | drizzle |
| `rainDownpour` | noise 200–3000Hz, higher gain | downpour |
| `catWatch` | soft ear flick noise, low purr 40Hz | cat watching |
| `catProwl` | paw taps 150Hz every 0.4s | cat prowling |
| `catStrike` | sharp hiss 1–3kHz, thump 100Hz | cat strike |
| `catBat` | soft thump 120Hz, no bite | cat catches frog |
| `heronWing` | low noise flap 100–500Hz | heron movement |
| `heronShadow` | low resonant hum 60Hz | shadow active |
| `heronStrike` | sharp whoosh 500–2500Hz | heron strike |
| `heronCough` | wet cough 100–300Hz | heron releases |
| `fishLunge` | bubble pop 300–900Hz | fish lunge |
| `flyBuzz` | saw 320Hz + noise loop | live fly |
| `waspBuzz` | square 180Hz + saw 360Hz | live wasp |
| `beetleClick` | low clicks 180Hz | live beetle |
| `sneeze` | noise burst 600–1800Hz | fly sneeze |
| `buzzJump` | pitch-up impulse 220→440Hz | buzzed jump |
| `croakShort` | sine 180Hz + formant 400Hz, 0.18s | non-answer croak |
| `croakHold` | sine 170Hz + formant 380Hz, loop | held croak |
| `chorusAnswer` | 3 detuned frog formants 220/280/340Hz | place answer |
| `fullChorus` | 7 frog formants + low pad 80Hz | final answer |
| `ambientGarden` | filtered noise bed 100–600Hz, occasional drip | garden place |
| `ambientRooftop` | wind bed, distant traffic hum | rooftop place |
| `settle` | soft pad 110Hz, slow fade | final end |

---

# 7. UX

## 7.1 Screens state machine

HTML/CSS only for screens. Game world is canvas.

| State | UI | Entry | Exit |
| --- | --- | --- | --- |
| `BOOT` | loading text | page load | `TITLE` |
| `TITLE` | title, controls, start | boot complete | `HOW_TO` or `PLAYING` |
| `HOW_TO` | controls and one short teaching line | title start | `PLAYING` |
| `PLAYING` | no HUD | run start | `ENDING` |
| `ENDING` | credits, restart | final chorus | `TITLE` |
| `SUSPENDED` | “resuming” only if browser returns | tab hidden | `PLAYING` |
| `ERROR` | minimal message | exception | reload |

No pause screen. No death screen. No score screen.

## 7.2 HUD table

| Element | Record field | When visible |
| --- | --- | --- |
| None in gameplay | n/a | never |
| Debug overlay | `state.debug`, `state.frog`, `state.answer`, `state.route` | debug enabled only |
| Title controls | static | `TITLE`, `HOW_TO` |
| Ending credits | `state.phase=ENDING` | `ENDING` |

No HUD markers for anchors, goals, hazards, or completion.

---

# 8. DEBUG API

| Function | Returns | Purpose |
| --- | --- | --- |
| `debug.enable()` | void | enable overlay |
| `debug.disable()` | void | disable overlay |
| `debug.frog()` | FrogRecord | inspect frog |
| `debug.tongue()` | TongueRecord | inspect tongue |
| `debug.grip()` | GripRecord | inspect grip |
| `debug.water()` | WaterRecord | inspect water |
| `debug.animal(id)` | AnimalRecord | inspect animal |
| `debug.answer(placeId)` | AnswerRecord | inspect answer state |
| `debug.route(placeId)` | RouteGraph | inspect route passability |
| `debug.place(placeId)` | PlaceRecord | inspect place |
| `debug.weather()` | WeatherRecord | inspect weather |
| `debug.objects()` | ObjectRecord[] | inspect reactive objects |
| `input.get('crouch')` | bool | crouch level state |
| `input.get('tongue')` | bool | tongue level state |
| `input.get('call')` | bool | call level state |
| `input.press('crouch')` | void | simulate press |
| `input.release('crouch')` | void | simulate release |
| `input.setAim(x,y)` | void | set aim vector |
| `input.setMove(x,y)` | void | set move vector |
| `state.resetRun()` | void | restart run |
| `state.resetPlace(id)` | void | reset one place |

---

# 9. TESTS

## 9.1 Tier 1 tests

| Test | Pass condition |
| --- | --- |
| Fixed loop | frame advances at 60Hz; no pause-time actions |
| Input | Space crouch, release hop; Z tongue; C call |
| Hop arc | crouch charge maps to predictable distance |
| Frog cannot run | max ground speed <=26 px/s |
| Tongue probe | tap gives material feedback; does not commit body |
| Tongue food | live insect eaten; dead insect no effect |
| Tongue commit | hold on safe anchor creates rope |
| Tongue weak anchor | breaks under load/impulse |
| Rope swing | left/right pendulum; release launches |
| Grip | auto-enter on climbable; slide on nonclimbable |
| Temporary grip | breaks after configured time |
| Water | float, paddle, current, no jump, safe deposit |
| Safe perch | last stable contact tracked; invalidates when unsafe |
| Cat attention | states change with motion/noise/cover |
| Cat catch | resets to last safe perch, no death |
| Heron attention | open ground shadow raises attention |
| Heron catch | cough up outside strike zone |
| Fish attention | ripples raise attention; lunge bumps only |
| Answer call | hold 0.75s at invalid node no completion |
| Answer route | valid return route required before completion |
| Final end | P99 answer completes without return route |
| No HUD | screenshot/API shows no gameplay HUD markers |
| No death | no phase `DEATH`, no health field |

## 9.2 Tier 2 tests

| Test | Pass condition |
| --- | --- |
| Eating fly | sneeze impulse only, no permanent state |
| Eating beetle | sluggish for 4.5s |
| Eating wasp | buzzed next jump only |
| Reactive object | pull moves object by physical cause |
| Persistent change | wet wall remains climbable after leaving/revisiting |
| Sprinkler | pressurized tell before spray; wets surface |
| Rain barrel tip | tilt creates current |
| Pipe/cork | pulling cork starts flow |
| Expanded places | P03-P05 load and complete |
| Place completion physical change | P03 requires sprinkler to wet wall before call |

## 9.3 Tier 3 tests

| Test | Pass condition |
| --- | --- |
| Weather states | dry to drizzle/steady/downpour transitions have tells |
| Wet surfaces | rain makes textured climbable, smooth slippery |
| Puddles | expand and create current |
| Wind | gust affects hop only with visible tell |
| Soft ladder | optional route to later place possible if physically reachable |
| Revisitation | completed places remain reachable and changed state persists |
| No required eating | run completes with zero insects eaten |
| No random eating | same input yields same effect |

---

# 10. BUILD ORDER

1. Create HTML/CSS shell, canvas, responsive letterbox, fixed loop.
2. Implement `state`, `input`, `engine`, `debug` skeleton.
3. Implement camera and place bounds.
4. Implement P01 geometry and start perch.
5. Implement frog capsule, crawl, crouch-hop, landing.
6. Implement grip and material classification.
7. Implement tongue probe, food catch, anchor commit, rope.
8. Implement water, currents, safe deposit.
9. Implement safe perch tracking and failure recovery.
10. Implement animal attention for cat, heron, fish.
11. Implement route graph and stable return verification.
12. Implement answer call and place completion.
13. Implement P02 and P99.
14. Add Tier1 visuals, parallax, camera, synthesized audio.
15. Add title/help/ending UI.
16. Run Tier1 tests.
17. Add eating body states and insects.
18. Add reactive object system and persistent physical changes.
19. Add sprinkler, rain barrel, pipe systems.
20. Add P03-P05.
21. Add rain/weather and wind.
22. Add soft ladder optional routes and revisitation.
23. Polish material tells and audio mix without adding systems.

---

# 11. DEFINITION OF DONE

## Tier 1: Core playable frog run

High level: A player can start under a dripping gutter in P01, learn the core verbs, reach P99, hold a croak at the final Answering Node, hear the full chorus, and see the game end.

- [ ] Fixed 60Hz loop with no pause-time actions.
- [ ] Keyboard input maps crouch-hop, tongue, call, aim, crawl, climb, swim.
- [ ] Frog has no health, no score, no death.
- [ ] Crouch-hop has predictable arc and commitment.
- [ ] Frog cannot run; max crawl 26 px/s.
- [ ] Tongue tap probes material; safe/weak/unusable anchors differ.
- [ ] Tongue commit, rope, swing, yank, break, release work.
- [ ] Grip enters on climbable surfaces and rejects nonclimbables.
- [ ] Temporary surfaces break after configured times.
- [ ] Water floats, paddles, currents carry, no jumping in water.
- [ ] Safe perch tracking and guaranteed recovery exist.
- [ ] Cat, heron, fish attention systems exist and never kill.
- [ ] Answering Nodes are stable perches with live chorus.
- [ ] Place completion requires held croak + live chorus + stable return route.
- [ ] P99 ends without return route.
- [ ] P01, P02, P99 are handcrafted bounded places.
- [ ] No gameplay HUD markers exist.
- [ ] All Tier1 sounds and visuals exist.
- [ ] Tier1 tests pass.

## Tier 2: Supporting mechanics and expanded run

High level: The world becomes reactive and expanded without breaking Tier1.

- [ ] Eating live insects produces deterministic temporary body states.
- [ ] Dead/stunned insects produce no effect.
- [ ] Eating is never required or scored.
- [ ] Reactive objects respond only to physical causes.
- [ ] Physical changes persist across revisits.
- [ ] Sprinkler has dormant/pressurized/spraying/spent states.
- [ ] Rain barrels can tip and create currents.
- [ ] Pipes/corks can start, block, or redirect flow.
- [ ] P03-P05 exist with one Answering Node each.
- [ ] Expanded run includes cat/heron/fish/sprinkler/current hazards.
- [ ] Tier2 tests pass.

## Tier 3: Extra systems and soft ladder

High level: Weather and revisitation make routes systemic and optional.

- [ ] Rain has physical tells and changes surfaces/puddles/currents.
- [ ] Wind affects hops only with visible environmental tells.
- [ ] Optional routes can reach later places but are steep/exposed/hazard-heavy.
- [ ] Later places can be completed if answer + route rules pass.
- [ ] Completed places remain revisitable.
- [ ] No random eating or hidden unfairness.
- [ ] Tier3 tests pass.

---

# A. SANITY

| Check | Result |
| --- | --- |
| All required headings present in order | Valid |
| Prompt decisions treated as final | Valid; no contradictions introduced |
| No added core systems beyond prompt | Valid; only concrete numbers and contracts added |
| Tier1 is finishable | Valid; P01/P02/P99 form a complete run |
| Full described run present | Valid; P03-P05 added as Tier2 expansion |
| No HUD markers | Valid; normal HUD empty, debug only |
| No death/health/score | Valid; no such fields |
| No combat/defeating enemies | Valid; animals are attention hazards only |
| No collectathon/flies as coins | Valid; insects optional, no counters |
| No survival meters | Valid; no hunger/thirst/stamina |
| No required eating | Valid; completion never requires eating |
| No permanent abilities from eating | Valid; body states temporary |
| No UI markers for anchors/goals | Valid; material/audio tells only |
| No interface warnings/HUD alerts | Valid; physical tells only |
| No random eating effects | Valid; deterministic by insect type |
| No hazards without physical tell | Valid; all hazards have tells |
| No unresolved falls | Valid; safe perch/current deposit/rescue ledge |
| No open world | Valid; bounded place graph |
| No locked doors/abstract switches | Valid; physical interactions only |
| One Answering Node per place | Valid; place records enforce it |
| Answer completion requires stable return route | Valid; route graph checked before chorus |
| Final exempt from return route | Valid; P99 `returnRouteRequired=false` |
| First place return target stable | Valid; changed from temporary leaf to stone rim |
| Numbers concrete | Valid; physics, animals, answer, objects, places use numbers |
| Input drives game | Valid; controls defined and mapped to state |
| Visuals imply rules | Valid; visual recipe table maps appearance to mechanics |
| Audio table present | Valid; synthesized recipes and triggers |
| UX state machine present | Valid; no pause/death screen |
| Debug API present | Valid; per-system state functions |
| Tests and done checklists present | Valid; aligned to tiers |