# 0. SCOPE
## 0.1 Asked
| Requirement | Where it lives |
| --- | --- |
| Player is a fridge that has just gained sentience and is trying to escape a house | #4 GAMEPLAY SPEC, #5 CHARACTERS |
| 3D game | #1 CONVENTIONS, #3 VISUAL SPEC, #4 GAMEPLAY SPEC |
| First-person camera | #1 CONVENTIONS, #3 VISUAL SPEC, #4 GAMEPLAY SPEC |
| Single player | #4 GAMEPLAY SPEC |
| Real-time | #1 CONVENTIONS, #4 GAMEPLAY SPEC |
| Free movement | #4 GAMEPLAY SPEC, player movement and steering |
| Connected rooms | #3 VISUAL SPEC, #4 GAMEPLAY SPEC, level roster |
| Failure restarts the level | #4 GAMEPLAY SPEC, #7 UX |
| Silly tone | #3 VISUAL SPEC, #4 GAMEPLAY SPEC, #5 CHARACTERS, #6 AUDIO |
| A handful of levels, under 30 minutes | #4 GAMEPLAY SPEC, level roster, #11 DEFINITION OF DONE |
| Win/lose is reach the exit | #4 GAMEPLAY SPEC, #7 UX |
| Mechanics: map / world, objectives, boosts, landmarks, hints, traps, noise, dash, switches and doors, physics objects, detection, puzzle types, push and pull, abilities / special moves, decoration, secrets, difficulty ramp, sneak, guards, keys and locked doors, flee, plot, key items, unlocks, collectibles, steer, pick up and drop, spawn points, conversations | #0.2 Decisions, #4 GAMEPLAY SPEC |
| Art style: stylized / toon, soft shapes, bright colours, cartoon proportions | #3 VISUAL SPEC |
| Palette: saturated, bright, strong colours | #3 VISUAL SPEC |
| Lighting: indoor, artificial light, enclosed | #3 VISUAL SPEC |
| Typography: hand-lettered, drawn, irregular letters | #3 VISUAL SPEC, #7 UX |
| Music: chiptune, retro console bleeps | #6 AUDIO |
| Sound effects style: retro bleeps, synthesized chip sounds | #6 AUDIO |
| Screens: title, pause, settings, game over, win, level select | #7 UX |
| HUD: minimap | #4 GAMEPLAY SPEC, minimap system, #7 UX |
| Effects: screen shake, particles | #3 VISUAL SPEC, #4 GAMEPLAY SPEC |
| Accessibility: colour-blind safe palette, reduced motion, remappable keys, difficulty options | #3 VISUAL SPEC, #4 GAMEPLAY SPEC, #7 UX |

## 0.2 Decisions
| Decision | Final value | Why |
| --- | --- | --- |
| Player identity | Player is “Frost”, a sentient double-door fridge. | Makes the prompt concrete and keeps the joke visible. |
| Playable level count | 5 levels. | Satisfies “a handful” and keeps total runtime under 30 minutes. |
| Target runtime | 17 to 23 minutes for first playthrough. | Leaves margin under 30 minutes while allowing retries. |
| Level names | Kitchen Rollout, Living Sled, Hallway Racket, Basement Bloop, Garage Getaway. | Silly, readable, and matches the house escape structure. |
| House escape route | Kitchen to Living to Hallway to Basement to Garage to back gate. | Gives a clear spatial story and connected-room progression. |
| Guard identity | Household appliance guards: Roomba Guard and Upright Vac Guard. | Keeps tone silly and avoids human enemies. |
| Guard count | 8 total guards across levels: Level 1 has 1 Roomba, Level 2 has 1 Upright Vac, Levels 3 to 5 have 2 guards each. | Creates a difficulty ramp without overloading a single level. |
| Failure triggers | Caught by a guard or touching a BamDoor trap. | Gives two understandable failure types without adding health. |
| Failure behavior | Restart the same level. Dynamic level state resets. Global unlock progress persists. | Meets the failure decision while preserving silly collectible unlocks. |
| Win condition | Touch the level exit zone after the exit door is open. | Directly matches “reach the exit”. |
| Player body type | Grounded rolling fridge, no jump, no flying. | Keeps free movement but maintains fridge proportions and house scale. |
| Player collision | Circle radius 0.35 metres, eye height 1.55 metres. | Fits first-person fridge scale and doorway widths. |
| Player walk speed | 2.8 metres per second. | Feels brisk but not twitchy for a fridge. |
| Player quiet speed | 1.4 metres per second. | Makes sneak meaningfully slower. |
| Dash speed | 5.6 metres per second for 0.22 seconds. | Allows short bursts to escape guards and reach boosts. |
| Dash cooldown | Normal 1.4 seconds, Easy 1.0 seconds, Hard 1.8 seconds. | Lets difficulty options alter pressure without changing core movement. |
| Quiet roll / sneak | Hold QuietRoll to move slowly and emit no footstep noise. | Directly implements the sneak mechanic. |
| Abilities | Dash and QuietRoll. | Covers abilities / special moves without adding extra combat moves. |
| Noise model | Movement and actions emit noise events with radii. Guards hear them only with line of sight. | Ties noise to detection and level geometry. |
| Walk noise radius | 3.0 metres, emitted every 0.35 seconds. | Keeps walking detectable but not instantly lethal. |
| Dash noise radius | 8.0 metres, one event. | Makes dash exciting and risky. |
| Interact noise radius | 4.0 metres, one event. | Punishes careless key and switch use. |
| Guard detection | Line-of-sight cone fills a 0 to 1 detection meter. Full meter causes chase. | Gives readable detection and fair chase behavior. |
| Guard catch radius | 0.8 metres. | Prevents false catches in narrow doorways. |
| Guard lose-line timer | If chased and line of sight is broken for 4 seconds, the guard returns to patrol. | Defines the flee mechanic. |
| Small item carrying | One carried item at a time. Keys are carried items. | Implements pick up and drop without an inventory system. |
| Key behavior | Keys are consumed when they open their door. | Makes key items matter and keeps inventory minimal. |
| Door types | KeyDoor, PressureDoor, HoldSwitchDoor. | Covers keys and locked doors plus switches and doors without extra types. |
| Pressure plate requirement | Plates open when a physics object of required mass rests on them. | Gives push and pull a purpose. |
| Hold switch timing | Hold 1.0 seconds to open. Door stays open 3.0 seconds after release. | Creates a timed puzzle without adding a timer HUD. |
| Physics objects | Stool, Chair, Crate, Box. | Gives a small, testable push/pull roster. |
| Push and pull rules | Grab large object for 0.3 seconds. Moving forward pushes, moving backward pulls. Object max speed 2.5 metres per second. | Keeps physics simple and testable. |
| Trap types | AlarmMat, WetSpill, BamDoor. | Covers noisy, slowing, and instant-fail traps. |
| Boost types | ButterPad, FanBlast. | Covers speed and directional boost without adding flight. |
| Collectibles | 10 Snack Bits total, 2 per level. | Small enough to finish quickly, enough to feel collectible. |
| Secret count | 5 secret alcoves, one per level. | Gives every level a hidden reward. |
| Unlock thresholds | 5 Snack Bits unlock Golden Crisper visual. 10 Snack Bits unlock Full Escape Jingle. | Implements unlocks without adding score. |
| Plot delivery | Five 3D conversation signs, one per level. | Implements conversations and plot without HUD text. |
| Hint delivery | Sticky-note signs in the world. | Matches hand-lettered typography and keeps HUD limited to minimap. |
| Landmarks | Exit glow, key arrow, floor route decals. | Helps navigation without adding HUD arrows. |
| Minimap content | Rooms, player arrow, exit marker, guard dots, door markers. | Satisfies HUD decision while staying useful. |
| Minimap size | 180 by 180 CSS pixels, scale 6 pixels per metre, top-right. | Large enough for connected rooms, small enough not to dominate. |
| Color palette | Cyan player, orange Roomba, purple Upright Vac, magenta keys, yellow exit/danger, blue safe interactions, teal floors, cream walls. | Saturated, bright, cartoon, and colour-blind safe when paired with shape icons. |
| No red-green dependency | Every gameplay color has a shape or icon backup: star for key, arrow for exit, triangle for danger, circle for safe. | Meets colour-blind safety. |
| Screen shake rules | Dash, alarms, fans, BamDoor, and guard alerts shake the camera. Reduced motion disables it. | Uses the required effect without harming accessibility. |
| Particle rules | Dash puffs, trap sparks, collectible crumbs, win confetti. Reduced motion limits particles to 10. | Uses the required effect while respecting reduced motion. |
| Music identity | One chiptune base track with chase, win, game-over, title, and pause variants. | Keeps audio small but distinct. |
| Audio implementation | Web Audio synthesized SFX and music. | Meets browser and synthesized chip-sound decisions. |
| Fixed timestep | Simulation updates at 60 Hz, render follows display frame. | Keeps movement, detection, and timers testable. |
| Random source | Seeded `mulberry32` per level. | Makes particle and guard jitter deterministic for tests. |
| Persistence | Settings, unlocked levels, collected Snack Bits, and secrets persist in `localStorage`. | Gives unlocks meaning without adding save-system complexity. |
| Crosshair | No crosshair. Interactables are highlighted in-world. | Keeps HUD exactly minimap. |
| Inventory | No inventory screen. One carried item only. | Avoids adding a system the decisions did not request. |
| Health | No health. Failure is binary. | Keeps failure aligned with restart-the-level. |
| Timer | No level time limit. Real-time only. | Avoids adding a countdown system. |

## 0.3 Tiers
| Tier | Segment | Contents | When it is done |
| --- | --- | --- | --- |
| Tier 1 | Minimal playable fridge escape | Title, pause, settings, game over, win, level select; Level 1; first-person movement and steering; dash and quiet roll; noise; one Roomba guard; detection, chase, catch, flee; key pickup, key door, exit; one AlarmMat, one WetSpill, one ButterPad; hints, landmarks, one conversation sign, minimap; settings for difficulty, reduced motion, and key remapping; basic synthesized audio. | A player can start Level 1, move freely, avoid or escape the Roomba, find the Spatula Key, open the front door, reach the exit, fail and retry, pause, open settings, and win. |
| Tier 2 | Full content and systems | All 5 levels; all door and switch types; all trap and boost types; both guard types; push and pull; physics objects; pressure plates; hold switch; all keys; all collectibles and unlocks; all secrets; all hints, conversations, landmarks, and decorations; full difficulty ramp; level unlock progression; full plot notes. | A player can beat all 5 levels in order, solve every listed puzzle, collect all Snack Bits, trigger all conversations, and unlock both final rewards. |
| Tier 3 | Polish, contracts, accessibility, and proof | Full visual recipe applied; full audio recipe applied; particles and screen shake; colour-blind palette verified; reduced motion verified; remappable keys verified; difficulty options verified; debug API complete; tests complete; performance pass on all levels. | The game matches the visual, audio, accessibility, engineering, and test contracts, and every Tier 1 and Tier 2 feature still works. |

# 1. CONVENTIONS
## 1.1 Units, axes, frames
| Quantity | Unit | Value or convention |
| --- | --- | --- |
| Distance | metres | All world positions, radii, and speeds use metres. |
| Height | metres | Y is up. Ground is `y = 0`. Ceiling is `y = 2.6`. |
| Speed | metres per second | Movement and impulse speeds use m/s. |
| Angle | radians | Rotations use radians. |
| Time | seconds | All cooldowns, durations, and timers use seconds. |
| Mass | kilograms | Physics object mass. |
| Noise radius | metres | Noise events define a hearing radius. |
| Detection | 0 to 1 scalar | Guard detection meter. |
| Simulation step | seconds | `dt = 1 / 60`. |
| Render frame | display-dependent | Render follows `requestAnimationFrame`, simulation is fixed step. |
| Axes | three.js-style | X is right, Y is up, Z is world depth. Camera forward is the camera’s local negative Z direction. |
| Player radius | metres | 0.35. |
| Player eye height | metres | 1.55. |
| Player walk speed | m/s | 2.8. |
| Player quiet speed | m/s | 1.4. |
| Player dash speed | m/s | 5.6. |
| Dash duration | seconds | 0.22. |
| Dash cooldown normal | seconds | 1.4. |
| Dash cooldown easy | seconds | 1.0. |
| Dash cooldown hard | seconds | 1.8. |
| Player acceleration | m/s² | 24. |
| Player friction | m/s² | 12. |
| Player turn rate | rad/s | 5. |
| Doorway width | metres | 1.2. |
| Doorway height | metres | 2.2. |
| Room ceiling | metres | 2.6. |
| Interact range | metres | 1.5. |
| Interact view alignment | dot product | Minimum `0.6` with camera forward. |
| Guard catch radius | metres | 0.8. |
| Roomba patrol speed | m/s | 1.6. |
| Roomba investigate speed | m/s | 2.4. |
| Roomba chase speed | m/s | 2.6. |
| Upright Vac patrol speed | m/s | 1.8. |
| Upright Vac investigate speed | m/s | 2.6. |
| Upright Vac chase speed | m/s | 3.0. |
| Guard turn rate | rad/s | 3.0. |
| Roomba sight distance | metres | 7.0. |
| Roomba cone half-angle | radians | 0.785, approximately 45 degrees. |
| Upright Vac sight distance | metres | 9.0. |
| Upright Vac cone half-angle | radians | 0.611, approximately 35 degrees. |
| Guard detection rate normal | per second | 0.9. |
| Guard detection rate easy | per second | 0.55. |
| Guard detection rate hard | per second | 1.2. |
| Guard lose-line timer | seconds | 4.0. |
| Walk noise interval | seconds | 0.35. |
| Walk noise radius | metres | 3.0. |
| Quiet noise radius | metres | 0.0. |
| Dash noise radius | metres | 8.0. |
| Interact noise radius | metres | 4.0. |
| AlarmMat noise radius | metres | 8.0. |
| AlarmMat noise duration | seconds | 0.6. |
| WetSpill slip duration | seconds | 1.5. |
| WetSpill speed multiplier | scalar | 0.5. |
| ButterPad speed multiplier | scalar | 1.6. |
| ButterPad duration | seconds | 1.8. |
| FanBlast impulse | m/s | 3.5. |
| FanBlast duration | seconds | 0.5. |
| FanBlast radius | metres | 2.0. |
| FanBlast cone half-angle | radians | 0.785. |
| HoldSwitch hold time | seconds | 1.0. |
| HoldSwitch open hold | seconds | 3.0. |
| Physics grab time | seconds | 0.3. |
| Physics max object speed | m/s | 2.5. |
| Physics push force | newtons | 90. |
| Physics pull force | newtons | 60. |
| Physics release distance | metres | 1.2. |
| Collectible collect radius | metres | 0.6. |
| Secret trigger radius | metres | 1.5. |
| Hint trigger radius | metres | 1.2. |
| Conversation trigger radius | metres | 1.5. |
| Minimap size | CSS pixels | 180 by 180. |
| Minimap scale | pixels per metre | 6. |
| Minimap offset | CSS pixels | 12 pixels from top and right. |
| Camera bob normal | metres | 0.03. |
| Camera bob frequency | hertz | 2.0. |
| Max particle count normal | particles | 120. |
| Max particle count reduced motion | particles | 10. |

## 1.2 Important conventions
- Use one global context object, called `C`, as the single source of gameplay truth. No module may keep authoritative gameplay state outside `C`.
- Use a fixed simulation timestep of `1 / 60` seconds. Accumulate frame time and run simulation updates in a `while` loop.
- Use `performance.now()` for frame timing. Clamp accumulator delta to 0.25 seconds to avoid spiral of death.
- Use a seeded random function per level: `mulberry32(1337 + levelIndex)`. Store it in `C.random`.
- Level data is immutable. Loading a level creates runtime copies in `C.level` and related arrays.
- All entity IDs are unique within a level. Persistent run data uses global IDs where needed.
- All timers are in seconds. All angles are in radians. All world positions use metres and Y-up.
- The player has no health, no score, no inventory screen, no jump, no timer, and no crosshair.
- The only HUD element is the minimap.
- Interactables are highlighted in the 3D world. No center dot or reticle is allowed.
- Audio must not start before the first user gesture.
- Settings, unlocked levels, collected Snack Bits, and discovered secrets persist in `localStorage` under the key `fridge-escape-v1`.
- Colour-blind safety is always active. The palette must not rely on red versus green alone.
- Reduced motion disables screen shake, camera bob, and most animation pulses. It reduces particles to the maximum allowed by the reduced-motion count.
- Failure restarts the current level. It does not reset `C.run.levelsUnlocked`, `C.run.collectedSnackIds`, or `C.run.secretsFoundIds`.
- Collision uses circle versus AABB for the player and simple AABB or circle resolution for physics objects.
- Line of sight for guard sight and noise hearing is a raycast against level collision AABBs.
- Doors block the player unless their runtime `open` state is true.
- Open doors remain open for the remainder of the level unless the door type says otherwise.
- HoldSwitch doors close after their open-hold timer expires.
- Pressure doors are open only while a qualified object is on the plate.

# 2. CONTRACTS
## 2.1 Module layout
| Module | File | Responsibility |
| --- | --- | --- |
| Main | `main.js` | Boot, screen state machine, fixed loop, start/win/fail flow. |
| Context | `context.js` | Create and persist `C`, settings, run data, and local storage. |
| Input | `input.js` | Remappable actions, pointer look, axis reading, action press/release. |
| Audio | `audio.js` | Web Audio init, synthesized SFX, music loops, mute-safe startup. |
| Levels | `levels.js` | Level data, level load, runtime entity creation, unlock rules. |
| Player | `player.js` | Player movement, steering, dash, quiet roll, interaction carry. |
| Physics | `physics.js` | Collision, raycasts, dynamic objects, push and pull. |
| Guards | `guards.js` | Guard state machine, patrol, investigate, chase, detection. |
| Interactions | `interactions.js` | Doors, switches, pickup, drop, object grab. |
| Hazards | `hazards.js` | Traps and boosts. |
| Collectibles | `collectibles.js` | Snack Bits, secrets, unlocks. |
| World Text | `worldtext.js` | Hints, conversations, landmarks, decoration placement. |
| Minimap | `minimap.js` | Minimap canvas drawing. |
| Effects | `effects.js` | Screen shake and particles. |
| UI | `ui.js` | HTML/CSS screens, settings, level select, buttons. |
| Debug | `debug.js` | Direct state mutation and player input test functions. |

## 2.2 Global context
| Field | Type | Description |
| --- | --- | --- |
| `C.screen` | string | One of `TITLE`, `PAUSE`, `SETTINGS`, `GAME_OVER`, `WIN`, `LEVEL_SELECT`, `PLAYING`. |
| `C.previousScreen` | string | Screen to return to when Settings closes. |
| `C.settings` | object | Difficulty, reduced motion, screen shake, keybinds. |
| `C.run` | object | Persistent progression. |
| `C.run.levelsUnlocked` | integer | Number of unlocked levels, 1 to 5. |
| `C.run.collectedSnackIds` | array of strings | Persistent collected Snack Bit IDs. |
| `C.run.secretsFoundIds` | array of strings | Persistent discovered secret IDs. |
| `C.run.goldenCrisperUnlocked` | boolean | True after 5 Snack Bits. |
| `C.run.fullEscapeJingleUnlocked` | boolean | True after 10 Snack Bits. |
| `C.levelIndex` | integer | Current zero-based level index, 0 to 4. |
| `C.level` | object | Loaded level runtime data. |
| `C.levelTime` | number | Seconds since level load. |
| `C.player` | object | Player runtime state. |
| `C.guards` | array | Runtime guard entities. |
| `C.doors` | array | Runtime door entities. |
| `C.switches` | array | Runtime switch entities. |
| `C.traps` | array | Runtime trap entities. |
| `C.boosts` | array | Runtime boost entities. |
| `C.physics` | array | Runtime physics object entities. |
| `C.collectibles` | array | Runtime Snack Bit entities. |
| `C.secrets` | array | Runtime secret entities. |
| `C.hints` | array | Runtime hint entities. |
| `C.conversations` | array | Runtime conversation sign entities. |
| `C.landmarks` | array | Runtime landmark entities. |
| `C.decorations` | array | Runtime decoration entities. |
| `C.input` | object | Input state and action readers. |
| `C.audio` | object | Current music ID and audio queue state. |
| `C.effects` | object | Shake and particle state. |
| `C.minimap` | object | Minimap canvas and draw state. |
| `C.random` | function | Seeded random function for current level. |
| `C.debug` | object | Debug API functions. |

## 2.3 Module specifics
| Record | Required fields |
| --- | --- |
| Level | `id`, `name`, `musicId`, `spawn`, `exit`, `rooms`, `collectibles`, `secrets`, `guards`, `doors`, `switches`, `traps`, `boosts`, `physics`, `hints`, `conversations`, `landmarks`, `decorations`, `plot` |
| SpawnPoint | `id`, `pos`, `rotY` |
| Exit | `id`, `doorId`, `pos`, `triggerRadius` |
| Door | `id`, `type`, `pos`, `rotY`, `open`, `keyId`, `switchId`, `holdTime`, `openHold` |
| Switch | `id`, `type`, `pos`, `state`, `doorId`, `requiredMass`, `holdTime`, `openHold` |
| Trap | `id`, `type`, `pos`, `size`, `cooldown`, `active` |
| Boost | `id`, `type`, `pos`, `dir`, `radius`, `power`, `duration`, `cooldown` |
| PhysicsObject | `id`, `type`, `name`, `pos`, `rotY`, `vel`, `mass`, `size`, `grabbed` |
| Guard | `id`, `type`, `pos`, `rotY`, `waypoints`, `waypointIndex`, `state`, `detection`, `targetPos`, `loseTimer`, `speed`, `hearingMultiplier`, `sightDistance`, `coneHalfAngle`, `detectionRate` |
| Collectible | `id`, `pos`, `found`, `secretId` |
| Secret | `id`, `pos`, `found`, `radius` |
| Hint | `id`, `pos`, `text`, `seen` |
| Conversation | `id`, `pos`, `text`, `seen` |
| Landmark | `id`, `type`, `pos` |
| Decoration | `id`, `type`, `pos`, `rotY`, `size`, `collides` |
| Settings | `difficulty`, `reducedMotion`, `screenShake`, `keybinds` |
| Player | `pos`, `rotY`, `vel`, `mode`, `dashTimer`, `dashCooldown`, `slipTimer`, `speedMult`, `carriedItemId`, `pushObjectId`, `noiseTimer`, `bobPhase` |

| Module | Required functions |
| --- | --- |
| main | `boot()`, `setScreen(name)`, `startLevel(index)`, `failLevel()`, `winLevel()`, `update(dt)`, `render()` |
| context | `create()`, `save()`, `load()`, `resetRun()` |
| input | `bindDefaults()`, `setBinds(map)`, `press(action)`, `release(action)`, `getAxis()`, `getLookDelta()`, `consumeLookDelta()`, `isAction(action)` |
| audio | `init()`, `playMusic(id)`, `stopMusic()`, `playSfx(id)` |
| levels | `getLevelData(index)`, `loadLevel(index)`, `getUnlockedCount()`, `unlockNext()` |
| player | `resetPlayer(level)`, `updatePlayer(dt)`, `applyMovement(dt)`, `startDash()`, `setQuiet(on)`, `interact()`, `drop()` |
| physics | `updatePhysics(dt)`, `moveCircle(pos, radius, vel)`, `raycast(from, to)`, `canGrab(obj)`, `grab(obj)`, `release()`, `pushPull(dt)` |
| guards | `updateGuards(dt)`, `setGuardState(guard, state)`, `emitNoise(pos, radius, sourceId)`, `lineOfSight(from, to)` |
| interactions | `getInteractable()`, `useInteractable()`, `updateDoors(dt)`, `updateSwitches(dt)`, `unlockDoor(id)`, `toggleSwitch(id)`, `holdSwitch(id, dt)` |
| hazards | `updateTraps(dt)`, `triggerTrap(id)`, `updateBoosts(dt)`, `activateBoost(id)` |
| collectibles | `updateCollectibles()`, `markCollected(id)`, `markSecret(id)` |
| worldtext | `updateHints(dt)`, `updateConversations(dt)`, `drawLandmarks()` |
| minimap | `update()`, `draw()` |
| effects | `addShake(intensity, duration)`, `addParticle(type, pos, count)`, `update(dt)` |
| ui | `render()`, `openScreen(name)`, `bindSettings()`, `bindLevelSelect()`, `bindButtons()` |
| debug | All functions listed in #8 DEBUG API. |

# 3. VISUAL SPEC
The game looks like a bright cartoon appliance kitchen: soft rounded walls, saturated floors, chunky props, and a first-person view from inside a fridge’s glass door. Shapes are friendly and slightly exaggerated. The fridge view model is a rounded cyan door frame with two crisper bins at the bottom. Guards are small rolling appliances with big simple faces. Traps and boosts use obvious shapes and symbols rather than subtle colour only.

Lighting is fully indoor and artificial. Every room has a warm ceiling lamp at intensity 1.2 and a cool fill light at intensity 0.6. No daylight enters. Exit doors glow yellow at emissive strength 0.8. Interactive objects pulse with a magenta or blue outline. Reduced motion disables pulses, shake, and bobbing.

Space is a connected house made of rounded rooms. Rooms are 4 to 8 metres across, 2.6 metres high, with 1.2 metre doorways. Walls are cream with soft teal floors. Doorways are wide enough for the fridge. Furniture is cartoon-scale and never blocks required routes except through intentional pressure or key puzzles.

| Element | Geometry | Material | Colour / shape | Gameplay meaning |
| --- | --- | --- | --- | --- |
| Fridge view frame | Rounded rectangle frame, 1.2 by 1.8 metres visual | Smooth plastic toon | Cyan `#36C5F0` with cream edge | Player identity. |
| Crisper bins | Two rounded boxes at bottom of frame | Soft plastic | Cyan and cream | Player “hands”. |
| Kitchen walls | Rounded box walls | Matte toon | Cream `#F6E7C8` | Navigation and line-of-sight. |
| Floors | Flat rounded floor | Matte toon | Teal `#26B6AD` | Ground plane. |
| Ceilings | Flat rounded ceiling | Matte toon | Soft cream `#FFF6E2` | Enclosed room feel. |
| Roomba Guard | Low cylinder, 0.4 diameter, 0.18 high | Smooth plastic, black bumper | Orange `#FF7A1C`, cyan eye | Low-speed guard. |
| Upright Vac Guard | Tall cone body with handle, 0.6 by 1.2 metres | Smooth plastic | Purple `#7A4BFF`, blue headlamp | Faster guard. |
| KeyDoor | Rounded door, 1.2 by 2.2 metres | Bright plastic | Magenta star keyhole, blue frame | Requires carried key. |
| PressureDoor | Rounded door with floor plate | Bright plastic | Blue frame, yellow plate | Opens when object mass meets plate requirement. |
| HoldSwitchDoor | Rounded door with side lever | Bright plastic | Orange lever, blue frame | Opens while held and for 3 seconds after release. |
| AlarmMat | Flat square mat, 0.6 by 0.6 metres | Rubber toon | Blue base, yellow triangle, black stripes | Loud noise trigger. |
| WetSpill | Flat puddle, 1.0 by 1.0 metres | Glossy toon | Yellow puddle, blue bubbles | Slows player and blocks dash. |
| BamDoor | Spring door with orange stripe | Bright plastic | Orange and black triangle | Instant level fail. |
| ButterPad | Circular pad, 0.8 diameter | Rubber toon | Yellow circle, blue rim, star shape | Speed boost. |
| FanBlast | Small floor fan with arrows | Bright plastic | Cyan fan, yellow arrow | Directional impulse boost. |
| Snack Bit | Small star cookie, 0.25 wide | Toon cookie | Yellow with blue dots | Collectible. |
| Key item | Star-shaped key, 0.25 long | Toon metal | Magenta star | Carried key item. |
| Sticky note hint | Flat note, 0.3 by 0.4 metres | Paper | Cream with black hand letters | In-world hint. |
| Conversation board | Speech bubble sign, 0.9 by 0.6 metres | Paper and wood | Cream bubble, black text | Plot conversation. |
| Exit landmark | Glowing arrow above exit door, 0.6 wide | Emissive toon | Yellow arrow | Marks exit. |
| Key landmark | Small floor arrow near key path | Emissive toon | Magenta arrow | Points toward required key area. |
| Route decal | Flat floor arrow, 0.4 long | Matte toon | Cyan arrow | Helps navigation. |
| Secret alcove | Hidden rounded nook, 1.2 deep | Matte toon | Slightly darker cream with star decal | Secret space. |
| Decoration | Rounded appliance props | Matte toon | Bright palette colours | Non-interactive flavour. |
| Dash particles | Small puffs | Soft particle | Cyan and white | Dash feedback. |
| Trap particles | Sparks and drips | Soft particle | Yellow and blue | Trap feedback. |
| Collectible particles | Cookie crumbs | Soft particle | Yellow and brown | Collectible feedback. |
| Win particles | Confetti stars | Soft particle | Cyan, orange, purple, yellow | Win feedback. |

# 4. GAMEPLAY SPEC
Frost is a fridge that woke up in the middle of a house and must roll out before the appliance guards notice. The player controls Frost in first person, moves freely through connected rooms, hears and avoids guard detection, uses dash and quiet roll, picks up keys, pushes or pulls household objects, triggers switches, and reaches the level exit. The game is silly, fast, and short: five levels, one win condition, two failure triggers, and a minimap as the only HUD element.

## 4.1 Levels, Run, Spawn Points, Objectives [Tier 1]
- There are exactly 5 levels.
- Level 1 is always unlocked.
- Winning a level unlocks the next level.
- Level select shows 5 buttons. Locked buttons are greyed out with a closed padlock shape.
- The level objective is always: reach the level exit zone.
- The exit zone is a trigger circle at the exit door.
- The exit trigger radius is 0.8 metres.
- The player wins only if the exit door is open and the player is inside the exit trigger zone.
- Failure restarts the current level.
- On restart, all guards, doors, switches, traps, boosts, physics objects, and level collectibles reset.
- Persistent run progress does not reset on failure.
- Each level has one spawn point.
- Spawn points are defined in level data and used at level start and after failure.

| Level | Rooms | Exit | Required key | Guards | Traps | Boosts | Physics | Collectibles | Hints / Conversation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Level 1 Kitchen Rollout | Fridge Nook, Kitchen, Pantry, Front Door Hall | `front_door` KeyDoor | `spatula_key` | 1 Roomba | 1 AlarmMat, 1 WetSpill | 1 ButterPad | None | 2 Snack Bits, 1 secret | 2 hints, Dad conversation |
| Level 2 Living Sled | Kitchen, Living, Dining, Den, Patio | `patio_door` KeyDoor | `remote_key` | 1 Upright Vac | 1 AlarmMat, 1 WetSpill | 1 FanBlast | 1 Stool | 2 Snack Bits, 1 secret | 3 hints, Mom conversation |
| Level 3 Hallway Racket | Entry Hall, Bedroom, Bathroom, Office, Basement Door | `basement_door` KeyDoor | `basement_key` | 1 Roomba, 1 Upright Vac | 1 BamDoor, 1 AlarmMat | 1 ButterPad | 1 Crate | 2 Snack Bits, 1 secret | 3 hints, Cat conversation |
| Level 4 Basement Bloop | Basement Entry, Laundry, Workshop, Utility, Garage Door | `garage_door` HoldSwitchDoor | `breaker_key` opens `workshop_door` | 1 Roomba, 1 Upright Vac | 1 AlarmMat, 1 BamDoor | 1 FanBlast | 1 Crate, 1 Chair | 2 Snack Bits, 1 secret | 3 hints, Toaster conversation |
| Level 5 Garage Getaway | Garage, Mudroom, Backyard Path | `back_gate` KeyDoor | `backgate_key` | 1 Roomba, 1 Upright Vac | 1 BamDoor, 1 AlarmMat | 1 FanBlast | 1 Box | 2 Snack Bits, 1 secret | 3 hints, Whole House conversation |

## 4.2 Player Movement and Steering [Tier 1]
- The player moves on the ground plane only.
- The player cannot jump.
- The player cannot fly.
- Movement is free-form and not grid-based.
- The player’s local forward direction is the camera’s negative Z direction.
- MoveForward and MoveBack set desired velocity along the camera forward and backward directions.
- MoveLeft and MoveRight set strafe velocity perpendicular to camera forward.
- Mouse look changes `C.player.rotY`.
- Keyboard look is not required and is not part of default controls.
- The input axis is the normalized sum of forward and strafe inputs.
- The player velocity approaches the desired velocity with acceleration 24 m/s².
- When no movement input is present, velocity decays with friction 12 m/s².
- The player turns with the mouse at a maximum of 5 rad/s.
- While pushing a physics object, player forward input pushes the object and player backward input pulls the object.
- While carrying a key, movement speed is unchanged.
- Player collision is a circle with radius 0.35 metres.
- Player collision checks against walls, closed doors, decorations marked `collides: true`, and ungrabbed physics objects.
- Open doors do not block the player.
- The camera is locked at eye height 1.55 metres above the player position.
- Camera bob uses 0.03 metres at 2 hertz while walking and is disabled by reduced motion.

## 4.3 Abilities, Dash, Quiet Roll, Sneak [Tier 1]
- The player has two special movement abilities: Dash and QuietRoll.
- Dash:
  - Triggered by pressing Dash.
  - Available only if `C.player.dashCooldown <= 0`, `C.player.slipTimer <= 0`, and the player is not pushing a physics object.
  - Sets `C.player.mode` to `dash` for 0.22 seconds.
  - Sets desired speed to 5.6 m/s in the current movement direction. If no movement direction exists, dash moves in the camera forward direction.
  - Sets `C.player.dashCooldown` to the difficulty-specific cooldown.
  - Emits one noise event with radius 8.0 metres.
  - Adds screen shake intensity 0.05 for 0.15 seconds, unless reduced motion is enabled.
  - Emits 6 dash particles, unless reduced motion reduces the count.
- QuietRoll:
  - Triggered by holding QuietRoll.
  - Sets `C.player.mode` to `quiet` while held.
  - Sets desired speed to 1.4 m/s.
  - Emits no footstep noise while held.
  - Cannot start Dash while actively moving in quiet mode? It can, but Dash overrides quiet for 0.22 seconds.
  - Releasing QuietRoll returns the player to walk mode.
- Walk:
  - Default mode.
  - Desired speed 2.8 m/s.
  - Emits footstep noise every 0.35 seconds while moving at speed greater than 0.1 m/s.
- Slip:
  - Applied by WetSpill.
  - Sets `C.player.slipTimer` to 1.5 seconds.
  - Multiplies player speed by 0.5.
  - Blocks Dash while active.

## 4.4 Noise [Tier 1]
- Noise is an event system, not a meter.
- Noise events have a position, radius, and source ID.
- A guard hears a noise event if:
  - The guard is within the event radius multiplied by the difficulty hearing multiplier and the guard hearing multiplier.
  - A raycast from the guard to the noise position is not blocked by collision geometry.
- If a guard hears a noise event, the guard enters Investigate state if it was in Patrol or Return, or gains 0.25 detection if it was already Investigate.
- Noise sources:
  - Walk footstep: radius 3.0, every 0.35 seconds while walking.
  - QuietRoll: radius 0.0.
  - Dash: radius 8.0, one event.
  - Interact: radius 4.0, one event.
  - AlarmMat: radius 8.0, emitted as 6 ticks over 0.6 seconds.
  - BamDoor: no noise, immediate fail.
  - WetSpill: no noise.
- Difficulty hearing multiplier:
  - Easy: 0.75.
  - Normal: 1.00.
  - Hard: 1.25.
- Guard hearing multiplier:
  - Roomba: 1.00.
  - Upright Vac: 0.85.

## 4.5 Guards and Detection [Tier 1]
- Guard states are `patrol`, `investigate`, `chase`, and `return`.
- Guards have no health.
- Guards do not open doors.
- Guards do not pick up objects.
- Guards cannot pass through walls.
- Guard movement uses the same collision system as the player but with their own radius.
  - Roomba radius: 0.35 metres.
  - Upright Vac radius: 0.45 metres.
- Patrol:
  - Guard follows waypoints at patrol speed.
  - Waits 0.5 seconds at each waypoint.
  - Faces movement direction.
- Investigate:
  - Triggered by hearing noise or partial detection.
  - Guard moves to `targetPos` at investigate speed.
  - If the player is seen while investigating, detection continues to fill.
  - If no player is seen for 2.0 seconds at the target, guard enters Return.
- Chase:
  - Triggered when detection reaches 1.0.
  - Guard moves to the player’s last seen position at chase speed.
  - If the player has line of sight, last seen position updates continuously.
  - If line of sight is broken, `loseTimer` counts up.
  - If `loseTimer` reaches 4.0 seconds, guard enters Return.
  - If the player is seen again during chase, `loseTimer` resets to 0 and detection remains 1.0.
- Return:
  - Guard returns to its patrol waypoint loop at investigate speed.
  - Detection resets to 0.
- Detection:
  - The guard sees the player if the player is within sight distance, inside the cone, and a raycast is unblocked.
  - While seen, `guard.detection += guard.detectionRate * difficultyDetectionMultiplier * dt`.
  - While not seen and not chasing, `guard.detection` decays at 0.6 per second to a minimum of 0.
  - Difficulty detection multiplier:
    - Easy: 0.61, using rate 0.55.
    - Normal: 1.0, using rate 0.9.
    - Hard: 1.33, using rate 1.2.
- Guard catch:
  - If guard distance to player is less than 0.8 metres, the player fails.
  - The game over screen appears.
  - The Roomba or Upright Vac plays a catch animation and sound.

## 4.6 Flee [Tier 1]
- Flee is not a separate input. It is a rule set.
- A player is fleeing when a guard is in chase state.
- The player can flee by:
  - Keeping distance with walk speed when possible.
  - Using Dash to create distance.
  - Breaking line of sight for 4.0 seconds.
- If the player stays visible, the guard continues chasing.
- If the player breaks line of sight and stays out of sight and hearing, the guard returns to patrol after 4.0 seconds.
- If the player makes noise while hiding, the guard may retarget the noise position.
- If the player re-enters the guard’s cone while `loseTimer` is under 4.0 seconds, `loseTimer` resets and chase continues.
- Guard chase speed is always lower than Dash speed on all difficulties:
  - Roomba hard chase: 3.0 m/s.
  - Upright Vac hard chase: 3.45 m/s.
  - Dash: 5.6 m/s.

## 4.7 Pick Up and Drop, Key Items [Tier 1]
- Small items can be picked up and dropped.
- The player can carry one small item at a time.
- Keys are small items.
- Snack Bits are not carried; they are auto-collected on touch.
- To pick up a small item:
  - The item must be within 1.5 metres.
  - The item must be aligned with camera forward with dot product at least 0.6.
  - The player must not already be carrying an item.
  - The player must press Interact.
- Picking up a key sets `C.player.carriedItemId` to the key ID.
- Pressing Drop while carrying a small item sets `C.player.carriedItemId` to null and places the item at the player position with 0.25 metre forward offset.
- A dropped key can be picked up again.
- A key is consumed when it opens its matching KeyDoor.
- Required key roster:

| Level | Key ID | Opens | Location |
| --- | --- | --- | --- |
| Level 1 | `spatula_key` | `front_door` | Pantry snack drawer |
| Level 2 | `remote_key` | `patio_door` | Dining TV cabinet |
| Level 3 | `basement_key` | `basement_door` | Office after pressure door |
| Level 4 | `breaker_key` | `workshop_door` | Utility after pressure door |
| Level 5 | `backgate_key` | `back_gate` | Workbench after pressure door |

## 4.8 Push and Pull [Tier 2]
- Large physics objects can be grabbed, pushed, and pulled.
- Physics object types:

| Object | ID suffix | Mass | Size |
| --- | --- | --- | --- |
| Stool | `stool` | 5 kg | 0.5 by 0.5 by 0.6 metres |
| Chair | `chair` | 8 kg | 0.6 by 0.6 by 0.9 metres |
| Crate | `crate` | 20 kg | 0.8 by 0.8 by 0.8 metres |
| Box | `box` | 15 kg | 0.7 by 0.7 by 0.7 metres |

- To grab a large object:
  - The object must be within 1.5 metres.
  - The object must be aligned with camera forward with dot product at least 0.6.
  - The player must not already be pushing another object.
  - The player must hold Interact for 0.3 seconds.
- While grabbed:
  - The object follows the player’s movement input.
  - Moving forward applies 90 newtons of push force.
  - Moving backward applies 60 newtons of pull force.
  - Object velocity is capped at 2.5 m/s.
  - The object collides with walls and other objects.
  - The player cannot Dash while grabbed.
  - If the player moves more than 1.2 metres from the object, the object releases.
- While not grabbed:
  - Objects do not move unless pushed by a fan boost? No, FanBlast only affects the player. Objects remain static unless grabbed.
  - Objects block the player if in the path.
- Push and pull is used to place objects on pressure plates.

## 4.9 Keys and Locked Doors [Tier 1]
- A KeyDoor is closed and blocks the player.
- A KeyDoor requires the matching key item.
- To open a KeyDoor:
  - The player must be within 1.5 metres.
  - The player must be aligned with the door with dot product at least 0.6.
  - `C.player.carriedItemId` must equal the door’s `keyId`.
  - The player must press Interact.
- Opening a KeyDoor:
  - Sets the door `open` to true.
  - Consumes the key.
  - Plays the key door open sound.
  - Emits one interact noise event.
- If the player interacts without the correct key:
  - The door shakes.
  - An error sound plays.
  - The door remains closed.

## 4.10 Switches and Doors [Tier 2]
- Door types:

| Door type | Open rule | Close rule |
| --- | --- | --- |
| KeyDoor | Correct key consumed | Never closes |
| PressureDoor | Qualified object on plate | Closes when object leaves plate |
| HoldSwitchDoor | Switch held or open-hold timer active | Closes after 3.0 seconds without hold |

- PressureDoor:
  - Linked to a pressure switch.
  - Opens when a grabbed or placed physics object with mass at least `switch.requiredMass` is on the plate.
  - The object must remain on the plate.
  - If the object is pushed off, the door closes.
- HoldSwitchDoor:
  - Linked to a hold switch.
  - Player presses and holds Interact for 1.0 seconds.
  - Door opens while holding.
  - After release, door stays open for 3.0 seconds.
  - If the player presses and holds again before timeout, the timer resets.
- Switch interaction rules:
  - Interacting with a switch emits one noise event with radius 4.0 metres.
  - Holding a switch does not emit continuous noise; only the initial interaction emits noise.

## 4.11 Traps [Tier 1]
- Trap types:

| Trap | Trigger | Effect |
| --- | --- | --- |
| AlarmMat | Player enters 0.6 by 0.6 metre zone | Loud noise. |
| WetSpill | Player enters 1.0 by 1.0 metre zone | Slows player. |
| BamDoor | Player enters 0.5 by 0.5 metre trigger zone | Instant level fail. |

- AlarmMat:
  - Emits 6 noise ticks over 0.6 seconds.
  - Each tick has radius 8.0 metres.
  - Adds screen shake intensity 0.12 for 0.3 seconds, unless reduced motion.
  - Emits 12 spark particles, unless reduced motion.
  - Cooldown 0.5 seconds.
- WetSpill:
  - Sets player slip timer to 1.5 seconds.
  - Multiplies player speed by 0.5.
  - Blocks Dash while active.
  - Adds screen shake intensity 0.04 for 0.1 seconds, unless reduced motion.
  - Emits 6 droplet particles.
  - Cooldown 0.2 seconds.
- BamDoor:
  - Instant fail.
  - Adds screen shake intensity 0.25 for 0.5 seconds, unless reduced motion.
  - Emits 20 crash particles.
  - Plays BamDoor sound.
  - Transitions to GAME_OVER.

## 4.12 Boosts [Tier 1]
- Boost types:

| Boost | Trigger | Effect |
| --- | --- | --- |
| ButterPad | Player enters 0.8 diameter circle | Speed multiplier. |
| FanBlast | Player inside fan radius and cone | Directional impulse. |

- ButterPad:
  - Sets player speed multiplier to 1.6 for 1.8 seconds.
  - Can combine with Dash.
  - Adds screen shake intensity 0.03 for 0.1 seconds, unless reduced motion.
  - Emits 6 puff particles.
  - Cooldown 0.5 seconds.
- FanBlast:
  - Affects the player only.
  - If the player is within 2.0 metres and inside the fan cone, the player receives an impulse of 3.5 m/s over 0.5 seconds in the fan direction.
  - The player can be redirected by walls during the impulse.
  - Adds screen shake intensity 0.08 for 0.2 seconds, unless reduced motion.
  - Emits 10 wind particles.
  - Cooldown 0.5 seconds.

## 4.13 Physics Objects and Puzzle Types [Tier 2]
- Puzzle types used in the game:

| Puzzle type | Example | Rule |
| --- | --- | --- |
| Fetch Key | Level 1 front door | Find key, carry it, open door. |
| Pressure Plate | Level 2 den door | Push or pull object onto plate. |
| Hold Door | Level 4 garage door | Hold switch, pass through before door closes. |
| Guard Escort | Level 3 office | Move through guarded rooms while carrying key. |

- Pressure plate required mass:

| Level | Plate ID | Required mass |
| --- | --- | --- |
| Level 2 | `den_plate` | 4 kg |
| Level 3 | `office_plate` | 10 kg |
| Level 4 | `utility_plate` | 10 kg |
| Level 5 | `workbench_plate` | 12 kg |

- Puzzle placement:
  - Level 2: Stool opens `den_door`.
  - Level 3: Crate opens `office_door`, where `basement_key` is located.
  - Level 4: Crate opens `utility_door`, where `breaker_key` is located.
  - Level 5: Box opens `workbench_door`, where `backgate_key` is located.

## 4.14 Collectibles and Unlocks [Tier 2]
- There are exactly 10 Snack Bits.
- Each level has 2 Snack Bits:
  - 1 visible Snack Bit.
  - 1 secret Snack Bit.
- Snack Bits are auto-collected when the player is within 0.6 metres.
- Collecting a Snack Bit:
  - Adds its ID to `C.run.collectedSnackIds` if not already present.
  - Emits 8 cookie crumb particles.
  - Plays collectible sound.
  - Adds 0.03 screen shake, unless reduced motion.
- Unlocks:
  - After 5 unique Snack Bits, `C.run.goldenCrisperUnlocked` becomes true.
    - Effect: title and level select show a golden crispr icon next to the game title.
    - No gameplay effect.
  - After 10 unique Snack Bits, `C.run.fullEscapeJingleUnlocked` becomes true.
    - Effect: the WIN screen plays the Full Escape Jingle instead of the normal win sting.
    - No gameplay effect.
- Snack Bit IDs:

| Level | Visible ID | Secret ID |
| --- | --- | --- |
| Level 1 | `snack_1_visible` | `snack_1_secret` |
| Level 2 | `snack_2_visible` | `snack_2_secret` |
| Level 3 | `snack_3_visible` | `snack_3_secret` |
| Level 4 | `snack_4_visible` | `snack_4_secret` |
| Level 5 | `snack_5_visible` | `snack_5_secret` |

## 4.15 Secrets [Tier 2]
- There are exactly 5 secret alcoves, one per level.
- Secret trigger radius is 1.5 metres.
- Entering the radius sets `C.secrets[i].found` to true for the level runtime.
- If the secret ID is not already in `C.run.secretsFoundIds`, it is added.
- Each secret alcove contains one secret Snack Bit.
- Secret alcoves are not required to win.
- Secret locations:

| Level | Secret ID | Location |
| --- | --- | --- |
| Level 1 | `secret_1` | Behind pantry shelf |
| Level 2 | `secret_2` | Behind bookshelf |
| Level 3 | `secret_3` | Bedroom closet |
| Level 4 | `secret_4` | Behind boiler |
| Level 5 | `secret_5` | Under workbench |

## 4.16 Hints [Tier 1]
- Hints are 3D sticky notes.
- Hint trigger radius is 1.2 metres.
- When the player is within radius and facing the hint with dot product at least 0.6, the hint is marked seen.
- Seen hints do not repeat.
- Hint text appears as hand-lettered text on the note for 4.0 seconds after first trigger.
- A hint bleep plays on first trigger.
- Hint roster:

| Level | Hint ID | Text |
| --- | --- | --- |
| Level 1 | `hint_1a` | “Front door likes a star-shaped key.” |
| Level 1 | `hint_1b` | “Check the drawer that smells like chips.” |
| Level 2 | `hint_2a` | “The TV cabinet hides the remote key.” |
| Level 2 | `hint_2b` | “Stools are good plate seats.” |
| Level 2 | `hint_2c` | “The den is behind the blue plate.” |
| Level 3 | `hint_3a` | “Basement key is past the office plate.” |
| Level 3 | `hint_3b` | “Crate is heavier than it looks.” |
| Level 3 | `hint_3c` | “Do not hug the spring door.” |
| Level 4 | `hint_4a` | “Breaker key lives in the workshop.” |
| Level 4 | `hint_4b` | “Hold the big orange lever.” |
| Level 4 | `hint_4c` | “The utility door wants a heavy friend.” |
| Level 5 | `hint_5a` | “Back gate key is behind the workbench plate.” |
| Level 5 | `hint_5b` | “Fan helps, but the gate wants a key.” |
| Level 5 | `hint_5c` | “The house is loud. Run quiet or run fast.” |

## 4.17 Landmarks [Tier 1]
- Landmarks are non-interactive visual guides.
- Landmark types:

| Type | Appearance | Placement |
| --- | --- | --- |
| Exit glow | Yellow arrow above exit door | Always above the level exit door. |
| Key arrow | Magenta floor arrow | Points toward the required key area. |
| Route decal | Cyan floor arrow | Marks the intended path through tricky rooms. |

- Landmarks do not affect gameplay.
- Landmarks are visible in the 3D world.
- Landmarks are not shown as separate HUD elements.
- The minimap shows exit, doors, guards, and player only.

## 4.18 Conversations and Plot [Tier 2]
- Conversations are 3D speech-board signs.
- Conversation trigger radius is 1.5 metres.
- When the player is within radius and facing the sign with dot product at least 0.6, the conversation is marked seen.
- Seen conversations do not repeat.
- A conversation chime plays on first trigger.
- Plot text appears on the sign for 5.0 seconds.
- Plot roster:

| Level | Conversation ID | Text |
| --- | --- | --- |
| Level 1 | `talk_1` | “Dad: Why is the fridge making eye contact?” |
| Level 2 | `talk_2` | “Mom: Did the appliances stage a little coup?” |
| Level 3 | `talk_3` | “Cat: Meow. That is my statement.” |
| Level 4 | `talk_4` | “Toaster: BEEP. Escape route approved.” |
| Level 5 | `talk_5` | “Whole House: Disappointed, but we tip our lids.” |

## 4.19 Minimap [Tier 1]
- The minimap is the only HUD element.
- The minimap is a 180 by 180 CSS pixel canvas.
- The minimap is positioned 12 CSS pixels from the top and right of the game viewport.
- The minimap scale is 6 CSS pixels per metre.
- The minimap is visible during PLAYING and PAUSE.
- The minimap is hidden during TITLE, SETTINGS, GAME_OVER, WIN, and LEVEL_SELECT.
- Minimap layers:

| Layer | Record field | Visual |
| --- | --- | --- |
| Rooms | `C.level.rooms` | Cream shapes on dark teal background. |
| Player | `C.player.pos`, `C.player.rotY` | Cyan arrow. |
| Exit | `C.level.exit.pos` | Yellow star. |
| Guards | `C.guards[i].pos` | Orange and purple dots. |
| Doors | `C.doors[i].pos`, `C.doors[i].open` | Closed doors are blue squares, open doors are hollow blue squares. |
| Switches | `C.switches[i].pos` | Small orange circles. |
| Traps | `C.traps[i].pos` | Small yellow triangles. |

- Guard dot colour:
  - Roomba: orange.
  - Upright Vac: purple.
- Reduced motion disables the player arrow pulse and minimap ping animations.

## 4.20 Difficulty, Accessibility, and Options [Tier 1]
- Difficulty options:

| Difficulty | Detection rate | Chase speed multiplier | Hearing multiplier | Dash cooldown |
| --- | --- | --- | --- | --- |
| Easy | 0.55 per second | 0.85 | 0.75 | 1.0 seconds |
| Normal | 0.9 per second | 1.00 | 1.00 | 1.4 seconds |
| Hard | 1.2 per second | 1.15 | 1.25 | 1.8 seconds |

- Reduced motion:
  - Disables screen shake.
  - Disables camera bob.
  - Reduces particles to a maximum of 10 active particles.
  - Disables minimap pulse animations.
  - Keeps gameplay timers unchanged.
- Screen shake option:
  - If reduced motion is off, screen shake can be enabled or disabled separately.
  - If reduced motion is on, screen shake is forced off.
- Colour-blind safe palette:
  - Always active.
  - No gameplay information is conveyed by red versus green alone.
  - Every critical colour has a shape or icon backup.
- Remappable keys:
  - Remappable actions: MoveForward, MoveBack, MoveLeft, MoveRight, Dash, QuietRoll, Interact, Drop, Pause.
  - Mouse look is always pointer-lock mouse look and is not remappable to a key.
  - Keybinds persist in settings.
  - Invalid duplicate bindings are rejected with a UI bleep.

## 4.21 Decoration [Tier 2]
- Decorations are non-interactive props.
- Decoration types include toaster, sink, counter, shelf, lamp, plant, toy, and appliance.
- Decorations have:
  - `type`
  - `pos`
  - `rotY`
  - `size`
  - `collides`
- If `collides` is true, the decoration blocks the player and physics objects.
- If `collides` is false, the decoration is visual only.
- Decorations do not appear as interactive highlights.
- Decorations do not appear on the minimap except as part of room geometry.

## 4.22 Difficulty Ramp and Progression [Tier 2]
- Level difficulty ramp:

| Level | Guard count | Trap pressure | Puzzle complexity | Target time |
| --- | --- | --- | --- | --- |
| Level 1 | 1 | Low | Key only | 2 to 3 minutes |
| Level 2 | 1 | Medium | Key plus pressure plate | 3 to 4 minutes |
| Level 3 | 2 | Medium | Pressure plate plus guard escort | 4 to 5 minutes |
| Level 4 | 2 | High | Key, pressure, hold switch | 4 to 5 minutes |
| Level 5 | 2 | High | Pressure, key, guard pressure | 4 to 6 minutes |

- Total target first-playtime: 17 to 23 minutes.
- Level select unlocks one level at a time.
- The WIN screen shows:
  - Level name.
  - “Escaped!” text.
  - Next Level button if a next level exists and is now unlocked.
  - Level Select button.
- The final WIN screen shows:
  - “You escaped the house!” text.
  - Level Select button.
  - Title button.

## 4.23 Feel [Tier 3]
- The fridge should feel heavy but agile.
- Walking has a small bob and a soft rolling sound.
- Dash feels like a short cartoon lurch.
- QuietRoll feels slower and silent.
- Guard detection has a rising bleep.
- Full detection triggers an alert bleep and camera shake.
- Interactable objects pulse with a magenta or blue outline.
- Door opens have a satisfying thunk.
- Collectibles make a crisp cookie-crunch bleep.
- Failure is fast and silly: a big BAM, spin, and game-over screen.
- Winning is a short confetti burst and jingle.

# 5. CHARACTERS
## Frost, the Player Fridge
- Silhouette: Tall rounded double-door fridge seen from inside. The player sees a cyan door frame and two crisper bins.
- Facing: First-person camera yaw. The view frame always faces the camera forward.
- Body height: 1.8 metres.
- Eye height: 1.55 metres.
- States:
  - `walk`
  - `quiet`
  - `dash`
  - `interact`
  - `push`
  - `pull`
  - `carry`
  - `fail`
  - `win`
- Animations:

| Animation | Trigger | Motion rule |
| --- | --- | --- |
| Idle | No movement | Door frame sways 0.01 metres at 0.5 hertz. Crisper bins stay low. |
| Walk | Moving in walk mode | Camera bob 0.03 metres at 2 hertz. Crisper bins lift 0.02 metres. |
| Quiet | QuietRoll held | Camera bob 0.01 metres at 1 hertz. Door frame leans back 0.05 radians. |
| Dash | Dash active | Door frame tilts forward 0.15 radians for 0.22 seconds. Crisper bins sweep sideways. |
| Interact | Interact pressed | Right crisper bin reaches forward 0.1 metres for 0.15 seconds. |
| Push | Pushing object | Both bins extend forward. Door frame leans forward 0.10 radians. |
| Pull | Pulling object | Both bins extend backward. Door frame leans back 0.10 radians. |
| Carry | Carrying key | Right bin holds the key. Key bobs 0.02 metres at 2 hertz. |
| Fail | Guard catch or BamDoor | Door frame tilts 0.30 radians and shakes for 0.5 seconds. |
| Win | Exit reached | Door frame bounces 0.20 metres and spins 0.25 radians. |

## Roomba Guard
- Silhouette: Low orange disc with black bumper and one cyan eye.
- Facing: Faces movement direction. The eye always faces the camera when alert.
- Radius: 0.35 metres.
- States:
  - `patrol`
  - `investigate`
  - `chase`
  - `return`
- Animations:

| Animation | Trigger | Motion rule |
| --- | --- | --- |
| Idle | No movement | Bumper blinks cyan every 1.0 second. |
| Patrol | Patrol state | Moves smoothly, bounces 0.01 metres at 3 hertz. |
| Investigate | Investigate state | Eye brightens. Bumper blinks 2 hertz. |
| Chase | Chase state | Body tilts forward 0.10 radians. Bumper blinks 4 hertz. |
| Alert | Detection reaches 1.0 | Eye flashes yellow for 0.25 seconds. |
| Bump | Collision with wall | Recoils 0.05 metres backward. |

## Upright Vac Guard
- Silhouette: Tall purple cone body with handle and blue headlamp.
- Facing: Body faces movement direction. Headlamp faces movement direction with 5 rad/s lag.
- Radius: 0.45 metres.
- States:
  - `patrol`
  - `investigate`
  - `chase`
  - `return`
- Animations:

| Animation | Trigger | Motion rule |
| --- | --- | --- |
| Idle | No movement | Headlamp pulses 1 hertz. |
| Patrol | Patrol state | Body sways 0.02 metres at 2 hertz. |
| Investigate | Investigate state | Headlamp brightens. Body tilts forward 0.05 radians. |
| Chase | Chase state | Body tilts forward 0.15 radians. Headlamp flashes 4 hertz. |
| Alert | Detection reaches 1.0 | Headlamp flashes yellow for 0.25 seconds. |
| Suction | Within 1.5 metres of player while chasing | Emits 2 dust particles toward player every 0.2 seconds. |
| Bump | Collision with wall | Recoils 0.05 metres backward. |

# 6. AUDIO
| Sound ID | Type | Recipe | When it plays |
| --- | --- | --- | --- |
| `music_title` | Loop | 120 BPM. Lead: square wave arpeggio C5, E5, G5, A5. Bass: triangle C3 and G3. Hats: short noise on eighth notes. | TITLE screen. |
| `music_level` | Loop | 140 BPM. Lead: square wave major bloop pattern C4, D4, E4, G4. Bass: triangle C3. Hats: short noise on quarter notes. | PLAYING, before chase. |
| `music_chase` | Loop | 180 BPM. Lead: square wave rapid arpeggio A4, C5, E5, A5. Bass: triangle A2. Hats: short noise on eighth notes. | Any guard in chase state. |
| `music_win` | One-shot | 150 BPM. Lead: square wave rising C5, E5, G5, C6. Bass: triangle chord C3, E3, G3. | WIN screen. |
| `music_gameover` | One-shot | 100 BPM. Lead: square wave descending G4, E4, C4, A3. Bass: triangle low G2. | GAME_OVER screen. |
| `music_pause` | One-shot | 90 BPM. Lead: square wave C5, E5. Bass: triangle C3. | PAUSE screen. |
| `sfx_ui_click` | SFX | Square wave 880 Hz, 0.05 seconds, gain 0.2, quick decay. | Button press. |
| `sfx_ui_error` | SFX | Square wave 220 Hz, 0.08 seconds, gain 0.25. | Invalid keybind, locked door, wrong key. |
| `sfx_footstep_walk` | SFX | Noise burst, lowpass 300 Hz, 0.04 seconds, gain 0.15. | Every 0.35 seconds while walking. |
| `sfx_footstep_quiet` | SFX | Sine wave 180 Hz, 0.03 seconds, gain 0.08. | Optional quiet roll contact only if reduced motion is off? It plays quietly while moving. |
| `sfx_dash` | SFX | Square wave sweep 200 Hz to 800 Hz over 0.18 seconds, gain 0.3. Add short noise burst. | Dash start. |
| `sfx_interact` | SFX | Square wave 660 Hz, 0.06 seconds, gain 0.2. | Successful interactable use. |
| `sfx_key_pick` | SFX | Triangle wave 987 Hz to 1319 Hz over 0.1 seconds, gain 0.25. | Picking up a key. |
| `sfx_key_door_open` | SFX | Triangle wave 392 Hz, 523 Hz, 659 Hz, each 0.08 seconds, gain 0.3. | KeyDoor opens. |
| `sfx_door_close` | SFX | Square wave 200 Hz to 100 Hz over 0.15 seconds, gain 0.25. | HoldSwitchDoor closes. |
| `sfx_switch_hold_tick` | SFX | Sine wave 440 Hz, 0.03 seconds, gain 0.1, repeated every 0.1 seconds while holding. | Holding a HoldSwitch. |
| `sfx_switch_toggle` | SFX | Square wave 220 Hz to 440 Hz over 0.08 seconds, gain 0.25. | Switch state changes. |
| `sfx_alarm` | SFX | Square wave alternating 700 Hz and 900 Hz, 0.5 seconds, gain 0.35. | AlarmMat triggered. |
| `sfx_wet` | SFX | Sine wave 120 Hz falling to 60 Hz over 0.3 seconds, gain 0.2. Add soft noise. | WetSpill triggered. |
| `sfx_bam` | SFX | Noise burst 0.2 seconds, lowpass 500 Hz, gain 0.5. Add square wave 80 Hz, 0.2 seconds. | BamDoor fail. |
| `sfx_boost_pad` | SFX | Triangle wave 523 Hz to 1046 Hz over 0.15 seconds, gain 0.3. | ButterPad triggered. |
| `sfx_fan` | SFX | Bandpass noise 400 Hz, 0.5 seconds, gain 0.25. | FanBlast active. |
| `sfx_collect` | SFX | Triangle wave 1046 Hz, 0.08 seconds, gain 0.3. Add short square wave 1568 Hz, 0.04 seconds. | Snack Bit collected. |
| `sfx_hint` | SFX | Sine wave 1200 Hz, 0.1 seconds, gain 0.2. | Hint first triggered. |
| `sfx_conversation` | SFX | Triangle wave 659 Hz to 880 Hz over 0.2 seconds, gain 0.25. | Conversation first triggered. |
| `sfx_guard_alert` | SFX | Square wave 500 Hz to 750 Hz over 0.15 seconds, gain 0.35. | Guard detection reaches 1.0. |
| `sfx_guard_chase_tick` | SFX | Square wave 300 Hz, 0.05 seconds, gain 0.2, repeated every 0.4 seconds. | Guard in chase state. |
| `sfx_caught` | SFX | Square wave 200 Hz falling to 50 Hz over 0.5 seconds, gain 0.4. Add noise burst. | Guard catches player. |
| `sfx_win_sting` | SFX | Triangle wave chord C5, E5, G5, 0.4 seconds, gain 0.4. | WIN screen if full escape jingle not unlocked. |
| `sfx_full_escape_jingle` | SFX | Square wave chord C5, E5, G5, C6, 0.6 seconds, gain 0.4. Add triangle bass C3. | WIN screen if full escape jingle unlocked. |
| `sfx_pause` | SFX | Sine wave 440 Hz, 0.05 seconds, gain 0.2. | Pause opened or closed. |

# 7. UX
The UX uses HTML and CSS only for screens, buttons, settings, level select, and the minimap canvas frame. The 3D game renders to a full-screen canvas. The minimap is a separate canvas overlay. No inventory, no crosshair, no objective bar, and no timer are allowed.

```html
<div id="app">
  <canvas id="game"></canvas>
  <canvas id="minimap" width="180" height="180"></canvas>

  <section id="screen-title" class="screen">
    <h1 class="hand">FRIDGE ESCAPE</h1>
    <p class="hand sub">The fridge woke up. Run.</p>
    <button data-action="level-select" class="btn">Level Select</button>
    <button data-action="settings" class="btn">Settings</button>
  </section>

  <section id="screen-pause" class="screen">
    <h2 class="hand">PAUSED</h2>
    <button data-action="resume" class="btn">Resume</button>
    <button data-action="settings" class="btn">Settings</button>
    <button data-action="level-select" class="btn">Level Select</button>
  </section>

  <section id="screen-settings" class="screen">
    <h2 class="hand">SETTINGS</h2>
    <label class="setting">
      Difficulty
      <select id="setting-difficulty">
        <option value="easy">Easy</option>
        <option value="normal" selected>Normal</option>
        <option value="hard">Hard</option>
      </select>
    </label>
    <label class="setting">
      <input type="checkbox" id="setting-reduced-motion">
      Reduced motion
    </label>
    <label class="setting">
      <input type="checkbox" id="setting-screen-shake" checked>
      Screen shake
    </label>
    <div id="keybind-list"></div>
    <button data-action="close-settings" class="btn">Close</button>
  </section>

  <section id="screen-game-over" class="screen">
    <h2 class="hand">BAM!</h2>
    <p class="hand sub">The fridge got caught.</p>
    <button data-action="retry" class="btn">Retry Level</button>
    <button data-action="level-select" class="btn">Level Select</button>
  </section>

  <section id="screen-win" class="screen">
    <h2 class="hand">ESCAPED!</h2>
    <p class="hand sub" id="win-level-name">Level 1</p>
    <button data-action="next-level" class="btn">Next Level</button>
    <button data-action="level-select" class="btn">Level Select</button>
    <button data-action="title" class="btn">Title</button>
  </section>

  <section id="screen-level-select" class="screen">
    <h2 class="hand">LEVEL SELECT</h2>
    <div id="level-buttons"></div>
    <button data-action="title" class="btn">Title</button>
  </section>
</div>
```

```css
#app {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #12343B;
  font-family: "Comic Sans MS", "Chalkboard SE", "Marker Felt", cursive;
}

#game {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
}

#minimap {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 180px;
  height: 180px;
  border: 4px solid #F6E7C8;
  border-radius: 18px;
  background: #0F2B2F;
  display: none;
}

.screen {
  position: absolute;
  inset: 0;
  display: none;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 18px;
  background: rgba(15, 43, 47, 0.82);
}

.screen.visible {
  display: flex;
}

.hand {
  color: #F6E7C8;
  letter-spacing: 2px;
  transform: rotate(-1.5deg);
  text-shadow: 3px 3px 0 #171717;
}

.sub {
  transform: rotate(1deg);
}

.btn {
  font-family: inherit;
  font-size: 24px;
  padding: 12px 22px;
  border: 5px solid #171717;
  border-radius: 18px;
  background: #FFD23F;
  color: #171717;
  cursor: pointer;
  transform: rotate(-0.5deg);
}

.btn:hover {
  background: #FF7A1C;
}

.btn:focus-visible {
  outline: 6px solid #36C5F0;
  outline-offset: 4px;
}

.btn:disabled {
  background: #7C8B8F;
  color: #171717;
  cursor: not-allowed;
}

.setting {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #F6E7C8;
  font-size: 20px;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.03); }
  100% { transform: scale(1); }
}

.screen h1,
.screen h2 {
  animation: pulse 1.6s ease-in-out infinite;
}

@media (prefers-reduced-motion: reduce) {
  .screen h1,
  .screen h2,
  .btn {
    animation: none;
  }
}
```

## Screen state machine
| From | To | Event | Effect |
| --- | --- | --- | --- |
| TITLE | SETTINGS | Press Settings | `C.previousScreen` set to TITLE. |
| TITLE | LEVEL_SELECT | Press Level Select or Enter | Show unlocked levels. |
| LEVEL_SELECT | PLAYING | Press unlocked level button | `main.startLevel(index)`. |
| LEVEL_SELECT | TITLE | Press Title | Return to title. |
| PLAYING | PAUSE | Pause action | Stop simulation. Play pause sound. |
| PAUSE | PLAYING | Press Resume or Pause action | Resume simulation. |
| PAUSE | SETTINGS | Press Settings | `C.previousScreen` set to PAUSE. |
| PAUSE | LEVEL_SELECT | Press Level Select | Return to level select. |
| SETTINGS | TITLE | Press Close if previous was TITLE | Return to title. |
| SETTINGS | PAUSE | Press Close if previous was PAUSE | Return to pause. |
| PLAYING | GAME_OVER | Fail event | Play caught or BamDoor sound. |
| GAME_OVER | PLAYING | Press Retry | Restart same level. |
| GAME_OVER | LEVEL_SELECT | Press Level Select | Return to level select. |
| PLAYING | WIN | Reach exit | Play win sting or full escape jingle. Unlock next level. |
| WIN | PLAYING | Press Next Level | Start next unlocked level. |
| WIN | LEVEL_SELECT | Press Level Select | Return to level select. |
| WIN | TITLE | Press Title | Return to title. |

## HUD table
| Element | Record field | When visible |
| --- | --- | --- |
| `#minimap` | `C.level.rooms` | PLAYING, PAUSE |
| `#minimap` player arrow | `C.player.pos`, `C.player.rotY` | PLAYING, PAUSE |
| `#minimap` exit marker | `C.level.exit.pos` | PLAYING, PAUSE |
| `#minimap` guard dots | `C.guards[i].pos`, `C.guards[i].type` | PLAYING, PAUSE |
| `#minimap` door markers | `C.doors[i].pos`, `C.doors[i].open` | PLAYING, PAUSE |
| `#minimap` switch markers | `C.switches[i].pos` | PLAYING, PAUSE |
| `#minimap` trap markers | `C.traps[i].pos` | PLAYING, PAUSE |

# 8. DEBUG API
| Function | System | Effect |
| --- | --- | --- |
| `debug.setScreen(screen)` | State / screens | Sets `C.screen` and updates UI. |
| `debug.loadLevel(index)` | Levels | Loads the given level index and starts PLAYING. |
| `debug.setSpawn()` | Spawn points | Moves player to current level spawn point. |
| `debug.setPlayer(pos, rotY, mode)` | Player | Sets player position, facing, and movement mode. |
| `debug.setVelocity(x, z)` | Movement | Sets player horizontal velocity. |
| `debug.setDash(timer, cooldown)` | Dash | Sets dash active timer and cooldown. |
| `debug.setSlip(timer)` | Traps / player | Sets WetSpill slip timer. |
| `debug.setCarried(itemId)` | Pick up and drop | Sets the carried small item ID. |
| `debug.setPush(objectId)` | Push and pull | Sets the grabbed physics object ID. |
| `debug.setGuard(id, state, detection, targetPos)` | Guards / detection | Sets guard state, detection, and target. |
| `debug.emitNoise(pos, radius, sourceId)` | Noise | Emits a noise event. |
| `debug.setDoor(id, open)` | Doors | Sets door open state. |
| `debug.setSwitch(id, state)` | Switches | Sets switch state. |
| `debug.triggerTrap(id)` | Traps | Triggers a trap by ID. |
| `debug.activateBoost(id)` | Boosts | Activates a boost by ID. |
| `debug.setPhysics(id, pos, rotY, grabbed)` | Physics objects | Sets physics object transform and grabbed state. |
| `debug.collectSnack(id)` | Collectibles / unlocks | Marks a Snack Bit collected. |
| `debug.setSecret(id, found)` | Secrets | Sets secret found state and persistent run flag. |
| `debug.setHint(id, seen)` | Hints | Sets hint seen state. |
| `debug.setConversation(id, seen)` | Conversations | Sets conversation seen state. |
| `debug.setLandmark(id, visible)` | Landmarks | Toggles landmark visibility. |
| `debug.setMinimap(visible)` | Minimap | Forces minimap visibility. |
| `debug.playSfx(id)` | Audio | Plays a synthesized SFX. |
| `debug.playMusic(id)` | Audio | Plays a synthesized music loop. |
| `debug.setSetting(key, value)` | Settings / accessibility | Sets a setting and saves it. |
| `debug.setDifficulty(name)` | Difficulty | Sets difficulty to easy, normal, or hard. |
| `debug.addShake(intensity, duration)` | Effects | Adds screen shake. |
| `debug.addParticle(type, pos, count)` | Effects | Adds particles. |
| `input.press(action)` | Player input | Simulates an action key press. |
| `input.release(action)` | Player input | Simulates an action key release. |
| `input.setAxis(x, z)` | Player input | Sets movement axis directly. |
| `input.look(dx, dy)` | Player input | Adds look delta directly. |
| `input.pointerLock()` | Player input | Requests pointer lock. |
| `input.pause()` | Player input | Simulates the Pause action. |

# 9. TESTS
| Tier | Test | Expected result |
| --- | --- | --- |
| Tier 1 | Boot test | Game starts on TITLE with no console errors. |
| Tier 1 | Screen transitions | TITLE, PAUSE, SETTINGS, GAME_OVER, WIN, LEVEL_SELECT all open and close correctly. |
| Tier 1 | Level load | Level 1 loads, player is at spawn, camera is first-person, minimap is visible. |
| Tier 1 | Movement | Forward input moves player at 2.8 m/s in camera forward direction within 5 percent tolerance. |
| Tier 1 | Steering | Left and right inputs produce strafe perpendicular to camera forward. Mouse look changes `C.player.rotY`. |
| Tier 1 | Collision | Player cannot pass through walls or closed doors. |
| Tier 1 | Dash | Dash gives 5.6 m/s for 0.22 seconds and sets cooldown to the difficulty value. |
| Tier 1 | Quiet roll | Holding QuietRoll sets speed to 1.4 m/s and emits no footstep noise. |
| Tier 1 | Noise | Walking emits noise radius 3.0 every 0.35 seconds. Dash emits radius 8.0 once. |
| Tier 1 | Guard detection | Guard facing player with line of sight fills detection and enters chase at 1.0. |
| Tier 1 | Guard hearing | Noise within guard hearing radius causes investigate or detection gain. |
| Tier 1 | Catch and fail | Guard within 0.8 metres triggers GAME_OVER. Retry restarts the same level. |
| Tier 1 | Flee | Breaking line of sight for 4 seconds returns guard to patrol. Re-seeing resets chase. |
| Tier 1 | Key pickup | Interacting with `spatula_key` sets `C.player.carriedItemId` to `spatula_key`. |
| Tier 1 | Key door | Opening `front_door` consumes key and sets door open. |
| Tier 1 | Win | Touching exit zone after door opens transitions to WIN and unlocks Level 2. |
| Tier 1 | Minimap | Minimap shows player arrow, exit star, guard dot, and door marker at correct positions. |
| Tier 1 | Settings | Difficulty changes guard detection and chase speed. Reduced motion disables shake. Key remapping works and persists. |
| Tier 1 | Audio | After first user gesture, music and SFX play. |
| Tier 2 | All levels load | Levels 0 to 4 load without missing IDs or broken references. |
| Tier 2 | Level unlock | Winning Level 1 unlocks Level 2. Winning Level 4 shows final win text. |
| Tier 2 | Pressure doors | Placing a qualified object on a plate opens the linked door. Removing it closes the door. |
| Tier 2 | Hold switch | Holding a hold switch for 1.0 seconds opens the door. Door closes 3.0 seconds after release. |
| Tier 2 | Push and pull | Grabbing, pushing, and pulling physics objects works. Release occurs at 1.2 metres. |
| Tier 2 | Trap behaviors | AlarmMat emits noise. WetSpill slows player for 1.5 seconds. BamDoor fails the level. |
| Tier 2 | Boost behaviors | ButterPad multiplies speed by 1.6 for 1.8 seconds. FanBlast applies directional impulse. |
| Tier 2 | Guard roster | Each level has the guard count and types listed in the level roster. |
| Tier 2 | Collectibles | All 10 Snack Bits can be collected. 5 unlocks Golden Crisper. 10 unlocks Full Escape Jingle. |
| Tier 2 | Secrets | All 5 secrets can be found. Secret IDs persist after reload. |
| Tier 2 | Hints and conversations | All hints and conversations trigger once and display the listed text. |
| Tier 2 | Landmarks | Exit glow, key arrows, and route decals appear in the correct rooms. |
| Tier 2 | Difficulty ramp | Later levels contain more traps, guards, and puzzle complexity as listed. |
| Tier 3 | Visual recipe | All visual entities use the listed geometry, colour, and shape rules. |
| Tier 3 | Colour-blind safety | No critical gameplay cue relies only on red versus green. Shape icons appear on keys, exits, dangers, and safe interactions. |
| Tier 3 | Reduced motion | Screen shake, camera bob, and excessive particles are disabled or limited. |
| Tier 3 | Remappable keys | All remappable actions respond to saved keybinds. |
| Tier 3 | Debug API | Every debug function changes the expected state. |
| Tier 3 | Persistence | Settings, unlocked levels, collected Snack Bits, and secrets survive reload. |
| Tier 3 | Performance | All 5 levels run at a stable 60 Hz simulation without growing arrays or leaking audio nodes. |

# 10. BUILD ORDER
1. Scaffold HTML, CSS, and JavaScript modules.
2. Implement global context, settings, persistence, and screen state machine.
3. Implement input with remappable actions and pointer-lock mouse look.
4. Implement Web Audio synthesis and basic music/SFX table.
5. Implement fixed-timestep loop and 3D scene bootstrap.
6. Implement player movement, steering, collision, dash, and quiet roll.
7. Implement Level 1 geometry, spawn, exit, key, key door, Roomba guard, detection, and minimap.
8. Implement fail and win flow, game over screen, and level unlock.
9. Implement settings, reduced motion, difficulty options, and key remapping.
10. Implement noise, guard investigation, chase, flee, and catch.
11. Implement traps and boosts for Level 1.
12. Implement hints, landmarks, conversation sign, and one collectible.
13. Implement push and pull, physics objects, pressure doors, and hold switches.
14. Build Levels 2 through 5 with the listed entities.
15. Implement all guards, all keys, all collectibles, secrets, unlocks, and plot notes.
16. Apply full visual recipe and colour-blind palette.
17. Apply full audio recipe and chase music transitions.
18. Implement effects: screen shake, particles, win confetti.
19. Implement debug API.
20. Run Tier 1, Tier 2, and Tier 3 tests until done.

# 11. DEFINITION OF DONE
## Tier 1 done
High level: A player can start Level 1, move and steer freely, use dash and quiet roll, avoid or flee a Roomba, find the key, open the front door, reach the exit, fail and retry, pause, open settings, and win.

- [ ] Boot reaches TITLE without console errors.
- [ ] TITLE shows game title and Level Select plus Settings buttons.
- [ ] LEVEL_SELECT shows Level 1 unlocked and Levels 2 to 5 locked.
- [ ] Starting Level 1 loads the player at spawn with first-person camera.
- [ ] Minimap is visible during PLAYING and PAUSE only.
- [ ] Minimap shows player, exit, guard, and door.
- [ ] Forward, back, left, and right inputs move the player freely.
- [ ] Mouse look changes facing.
- [ ] Player cannot pass through walls or closed doors.
- [ ] Walk speed is 2.8 m/s.
- [ ] QuietRoll speed is 1.4 m/s and emits no footstep noise.
- [ ] Dash speed is 5.6 m/s for 0.22 seconds.
- [ ] Dash cooldown matches difficulty.
- [ ] Walking emits noise radius 3.0 every 0.35 seconds.
- [ ] Dash emits noise radius 8.0.
- [ ] Roomba patrols, investigates noise, chases on full detection, and catches at 0.8 metres.
- [ ] Catch transitions to GAME_OVER.
- [ ] Retry restarts Level 1 and resets guards, doors, traps, and boosts.
- [ ] `spatula_key` can be picked up, carried, dropped, and used.
- [ ] `front_door` opens only with `spatula_key` and consumes it.
- [ ] Touching the exit zone after the door opens transitions to WIN.
- [ ] WIN unlocks Level 2.
- [ ] PAUSE, SETTINGS, GAME_OVER, WIN, and LEVEL_SELECT screens work.
- [ ] Difficulty changes detection rate, chase speed, hearing radius, and dash cooldown.
- [ ] Reduced motion disables screen shake and camera bob.
- [ ] Remappable keys work and persist.
- [ ] Audio starts after first user gesture.

## Tier 2 done
High level: All 5 levels are playable with full systems, full content, full progression, and full silly plot.

- [ ] Levels 0 to 4 load with all listed entities.
- [ ] Level select unlocks sequentially after wins.
- [ ] Final WIN shows “You escaped the house!” text.
- [ ] KeyDoor, PressureDoor, and HoldSwitchDoor all behave according to their rules.
- [ ] All 5 keys exist and open the correct doors.
- [ ] All pressure plates require the listed mass.
- [ ] All hold switches require 1.0 seconds and close after 3.0 seconds.
- [ ] Stool, Chair, Crate, and Box can be grabbed, pushed, pulled, and released.
- [ ] AlarmMat emits noise, WetSpill slows the player, and BamDoor fails the level.
- [ ] ButterPad applies speed multiplier, FanBlast applies directional impulse.
- [ ] Level 1 has 1 Roomba.
- [ ] Level 2 has 1 Upright Vac.
- [ ] Levels 3 to 5 have 1 Roomba and 1 Upright Vac each.
- [ ] All 10 Snack Bits can be collected.
- [ ] 5 Snack Bits unlock Golden Crisper visual.
- [ ] 10 Snack Bits unlock Full Escape Jingle.
- [ ] All 5 secrets can be found.
- [ ] All hints display the listed text once.
- [ ] All 5 conversations display the listed plot text once.
- [ ] Exit glow, key arrows, and route decals appear.
- [ ] Total first-playtime target is under 30 minutes.

## Tier 3 done
High level: The game is polished, accessible, audio-complete, visually consistent, and fully testable.

- [ ] Visual recipe is applied to all entities.
- [ ] Colour-blind safe palette is used with shape-icon backups.
- [ ] No HUD element exists except the minimap.
- [ ] No crosshair exists.
- [ ] No inventory screen exists.
- [ ] No health, score, or timer system exists.
- [ ] Screen shake values match the spec.
- [ ] Particle counts match normal and reduced-motion limits.
- [ ] All synthesized sounds match the audio table.
- [ ] Chase music plays when any guard chases.
- [ ] Win and game-over music play on the correct screens.
- [ ] All settings persist after reload.
- [ ] All debug functions work.
- [ ] All Tier 1 and Tier 2 tests pass.
- [ ] All Tier 3 accessibility tests pass.
- [ ] All 5 levels run without console errors.

# A. SANITY
| Check | Result | Fix / status |
| --- | --- | --- |
| Screens are exactly title, pause, settings, game over, win, level select | Valid | No extra screens added. WIN handles both level clear and final clear. |
| HUD is exactly minimap | Valid | Removed crosshair, objective text, inventory, timer, and health from HUD. Interactables are highlighted in-world. |
| Mechanics list is covered without added systems | Valid | Each listed mechanic appears in #4. No health, score, timer, shop, or inventory system was added. |
| Player is a fridge and first person | Valid | Player view is a fridge door frame with crisper bins. Camera is first-person. |
| Free movement is respected | Valid | Player can move in any ground direction using forward/back/strafe and mouse steering. |
| Connected rooms are respected | Valid | All levels are connected room layouts with doorways and no portals. |
| Failure restarts level | Valid | Guard catch and BamDoor fail restart the current level. Persistent unlock progress is documented separately. |
| Win/lose is reach exit | Valid | Win only triggers at the exit zone after the exit door is open. Loss is defined by failure triggers. |
| Under 30 minutes | Valid | 5 levels with target 17 to 23 minutes. |
| Tone is silly | Valid | Fridge sentience, appliance guards, snack bits, funny notes, BAM failure, and chiptune. |
| Colour-blind safe palette | Valid | Palette avoids red-green-only cues and uses shape icons for key, exit, danger, and safe interactions. |
| Reduced motion | Valid | Disables screen shake, camera bob, and reduces particles to 10. |
| Remappable keys | Valid | All major actions except mouse look are remappable and persisted. |
| Difficulty options | Valid | Easy, Normal, and Hard change detection, chase speed, hearing, and dash cooldown. |
| Audio is synthesized | Valid | All music and SFX use waveform, frequency, and duration recipes for Web Audio. |
| Units and numbers are consistent | Valid | Speeds, radii, timers, detection rates, and minimap scale are repeated consistently in #1, #4, #7, and #9. |
| Initial concern: crosshair would violate HUD decision | Fixed | Crosshair removed. In-world highlight used instead. |
| Initial concern: Level 1 had no guard, but Tier 1 needs failure | Fixed | Level 1 now contains one Roomba Guard. |
| Initial concern: collectible reset on failure would weaken unlocks | Fixed | Failure resets dynamic level state, but persistent `C.run` collectible and secret progress remains documented and tested. |
| Initial concern: too many switch types | Fixed | Switches limited to pressure and hold types used by levels. |
| Initial concern: trap instant fail may be too harsh | Fixed | Only BamDoor is instant fail; AlarmMat and WetSpill are hinders. BamDoor placement is limited to later levels and telegraphed by shape. |
