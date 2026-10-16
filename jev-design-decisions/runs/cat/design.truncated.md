# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Player is a cat trying to catch mice | #4 Gameplay, #5 Characters |
| 2D game | #1 Conventions, #3 Visual Spec |
| Top-down camera | #3 Visual Spec, #4 Map/World |
| Single player | #0, #7 UX |
| Real-time time model | #1 Conventions, #4 Systems |
| Free movement | #4 Movement & Input |
| Session is a sequence of levels | #4 Progression, #7 Level Select |
| Failure restarts the level | #4 Failure, #7 Game Over |
| Tone is silly | #3 Visual, #4 Names, #5 Characters, #6 Audio |
| Handful of levels, under 30 minutes | #4 Progression |
| Win/lose: reach the exit | #4 Objectives, #7 Win/Game Over |
| Mechanics: dash, boosts, chase and catch, objectives, difficulty ramp, spawn points, score, traps, landmarks, unlocks, decoration, collectibles, melee attack, medals / ranks, secrets, rewards, collectible creatures, hints, keys and locked doors, combos, abilities / special moves, switches and doors, map / world, noise, high scores, puzzle types | #4 Gameplay Systems |
| Art style: flat vector: clean flat shapes, solid colours, crisp edges | #3 Visual Spec |
| Palette: saturated: bright, strong colours | #3 Visual Spec |
| Typography: hand-lettered: drawn, irregular letters | #3 Visual Spec, #7 UX |
| Music: chiptune: retro console bleeps | #6 Audio |
| Sound effects style: retro bleeps: synthesized chip sounds | #6 Audio |
| Screens: title, pause, settings, game over, win, level select, high scores | #7 UX |
| HUD: score, combo counter | #7 UX |
| Effects: particles, hit flash, trails | #3 Visual, #4 Effects |
| Accessibility: colour-blind safe palette, reduced motion, remappable keys, difficulty options | #0, #4, #7 |

## 0.2 Decisions

| Decision | Final value | Why |
| --- | --- | --- |
| Game prompt | Cat catches mice | Locked input |
| Dimension | 2D | Locked input |
| Camera | Top-down | Locked input |
| Players | Single player | Locked input |
| Time model | Real-time | Locked input |
| Movement model | Free 8-way movement | Locked input |
| Session shape | Sequence of levels | Locked input |
| Failure | Restart the level | Locked input |
| Tone | Silly | Locked input |
| Size | 6 levels, target 23 minutes first clear | “Handful”, under 30 minutes |
| Win/lose | Level wins when cat reaches exit; level fails if squeaked before reaching it | Keeps the listed win while giving a clear failure |
| Art style | Flat vector, solid colour, no gradients | Locked input |
| Palette | Saturated, colour-blind safe, shape-coded | Locked input + accessibility |
| Typography | Hand-lettered style simulated with cursive stack and irregular CSS transforms | Browser-friendly, no external font assets required |
| Music | Chiptune WebAudio synth | Locked input |
| SFX | Retro bleeps, WebAudio synth | Locked input |
| Screens | Exactly: title, pause, settings, game over, win, level select, high scores | Locked input |
| HUD | Exactly: score, combo counter | Locked input |
| Effects | Exactly: particles, hit flash, trails | Locked input |
| Accessibility | Colour-blind safe, reduced motion, remappable keys, difficulty options | Locked input |
| Player identity | “Mousie-Butt”, an orange tabby cat | Silly, readable silhouette |
| Failure condition | Body contact with a Squeak Mouse while not dashing and not invulnerable | Makes chase/catch meaningful and gives a clear Game Over reason |
| Level count | 6 levels | Handful, under 30 minutes |
| Level target times | 2, 3, 4, 4, 5, 5 minutes = 23 minutes | Under 30 minutes |
| Tile size | 32 px | Clean vector grid, crisp edges |
| Level size | 40 × 24 tiles = 1280 × 768 px | Top-down map/world larger than screen |
| Viewport | 800 × 480 px | Browser-friendly top-down camera |
| Fixed step | 60 Hz logic, rendered per rAF | Stable real-time feel |
| Random source | Mulberry32, seeded per level and attempt | Deterministic tests and fair retries |
| Cat speed | 240 px/s | Responsive without floaty |
| Cat hit radius | 12 px | Fair chase/fail contact |
| Mouse hit radius | 10 px | Slightly smaller, easier to catch |
| Dash speed | 560 px/s for 0.20 s | Strong but limited special movement |
| Dash cooldown | Casual 0.90 s, Normal 1.10 s, Insane 1.30 s | Difficulty options |
| Dash i-frames | Casual 0.30 s, Normal 0.22 s, Insane 0.18 s | Dash is safe but not permanent |
| Melee cooldown | 0.35 s | Snappy attack |
| Melee range | 36 px normal, 48 px with Catnip | Close-range catch tool |
| Melee arc | 100° total, 50° half-angle | Generous but directional |
| Special move | “Mousie-Nado”, cooldown 8 s, radius 96 px, duration 0.25 s | One clear ability/special move |
| Scamper speed | Wander 140 px/s, flee 180 px/s | Passive chase target |
| Key Mouse speed | Flee 210 px/s | Reward is slightly harder |
| Squeak speed | Casual 160, Normal 200, Insane 240 px/s | Difficulty options |
| Squeak chase radius | Casual 220, Normal 260, Insane 300 px | Difficulty options |
| Combo timer | 2.00 s | Encourages continuous catches |
| Combo multiplier | x1 for 0-2, x2 for 3-5, x3 for 6-8, x4 for 9-11, x5 for 12+ | Simple readable combo counter |
| Base score table | Scamper 100, Key 250, Squeak 150, Bunny 200, Duck 250, Shrimp 300, Cheese 50, Fish 100, Bell 150, Catnip 250 | Different values keep chasing fun |
| Medals | Bronze reach exit, Silver score threshold, Gold score threshold | Satisfies medals/ranks |
| Rank | Based on sum of best scores per completed level | High-score rank without a timer |
| High scores | Local top 10 completions + best per level | Single-player browser persistence |
| Traps | Snap Trap, Catnip Bomb, Bonk Boot | Traps without a second hidden failure system |
| Trap bonk | Returns cat to spawn, dizzy, combo reset, optional score penalty | Failure remains Squeak contact |
| Boosts | Fish speed 3 s, Bell dash cooldown 5 s, Catnip melee range 4 s | Boosts are timed stat changes |
| Noise | Noise pulses wake mice and activate Noise Switches | Gives noise gameplay weight |
| Keys | Key Mouse drops key; locked doors consume keys | Keys and locked doors |
| Switches | Paw, Noise, Dash; toggleable | Switches and doors |
| Doors | Exit door and Breeze Door; locked by keys/switches | Doors with puzzle use |
| Breeze Door | Opens 0.80 s when linked switches are on; stays open only if cat passes through | Uses dash for puzzle |
| Secrets | Reveal by dash or melee within 20 px of secret tile | Secrets without new UI |
| Collectible creatures | Bunny, Duck, Shrimp; catch for score and Pals count | Satisfies collectible creatures |
| Hints | Level start hint, locked door hint, Squeak wake hint, switch hint | Hints without extra screen |
| Rewards | Cat Naps from best medals: Bronze 1, Silver 2, Gold 3 | Reward without a shop system |
| Unlocks | Next level unlock + visual unlocks at 3/6/9 Cat Naps | Unlocks and rewards |
| Difficulty options | Casual, Normal, Insane | Accessibility/difficulty ramp |
| Save key | `meow-mouse-maze-save-v1` | Single local save |
| No external assets | All audio synthesized, all visuals drawn from palette/shapes | Browser build constraint |
| UI technology | HTML/CSS screens and HUD; canvas world | UX decision |
| Audio technology | WebAudio API | Audio decision |
| Single failure source | Only Squeak body contact fails | Clear fail, less accidental frustration |
| Cat Naps are not a shop | Cat Naps only unlock cosmetic titles/visuals | Avoids adding a system not in decisions |

## 0.3 Tiers

| Tier | Name | Included systems | Exit criterion |
| --- | --- | --- | --- |
| Tier 1 | Core loop | Title, level select for L1, game, pause, win, game over, high scores, settings; cat movement, dash, melee, Scamper/Key/Squeak mice, chase/catch, score, combo, traps Snap, reach exit, Squeak fail, restart, local high scores, reduced motion, difficulty, remappable keys, particles, hit flash, trails, basic chiptune/SFX | A player can play Level 1 from title to win/fail with working core feel and required screens |
| Tier 2 | Full content | All 6 levels, level unlock progression, keys, locked doors, switches, Breeze Door, all traps, boosts, collectibles, creatures, secrets, noise, special move, medals, ranks, rewards, unlocks, hints, high score per level, puzzle types, full level rosters | A player can complete all 6 levels with all listed mechanics present |
| Tier 3 | Polish and proof | Full audio table, visual unlock cosmetics, high score rank detail, colour-blind shape cue audit, reduced-motion audit, remap all actions, performance stability, debug API, tests, no forbidden systems/screens | The game can be demonstrated as finished against the Definition of Done |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Thing | Unit | Value / rule |
| --- | --- | --- |
| Coordinate | pixels | World coordinates are float pixels |
| Tile | pixels | 1 tile = 32 px |
| Level size | tiles | 40 × 24 |
| Level size | pixels | 1280 × 768 |
| Viewport | pixels | 800 × 480 |
| X axis | pixels | Positive X is right |
| Y axis | pixels | Positive Y is down |
| Facing | integer | 0 right, 1 down-right, 2 down, 3 down-left, 4 left, 5 up-left, 6 up, 7 up-right |
| Time | seconds | All durations are seconds |
| Speed | pixels/second | Cat 240, Dash 560, mice see tables |
| Radius | pixels | Cat 12, mouse 10, pickup 10 |
| Score | integer | No fractional score |
| Logic step | seconds | 1/60 = 0.016666... |
| Logic frequency | Hz | 60 |
| Render | rAF | Render latest state every animation frame |
| Max accumulator | seconds | 0.25 |
| Random | seeded integer | Mulberry32 |

## 1.2 Important conventions

- One global `ctx` object holds all gameplay state. UI reads from `ctx`; only `game.js` mutates top-level state directly.
- The logic loop is fixed-step at 60 Hz. The renderer does not advance gameplay.
- All gameplay randomness uses `ctx.rng`. `Math.random()` is forbidden in gameplay code.
- Level layout is deterministic. Runtime mouse wander, particle variation, and test seeds use `ctx.rng`.
- All speeds are pixels/second. All cooldowns and timers are seconds.
- All collision is circle vs tile/entity. Cat and mouse move axis-separated against solid tiles.
- Mice do not collide with each other.
- Pickups are collected by cat body contact or melee.
- Squeak Mice are the only failure source.
- Traps are non-fatal.
- Effects are visual-only.
- Reduced motion disables trails, particles, screen hit flash, camera shake, and Breeze Door flash. Timings do not change.
- Colour-blind safety is always on. No gameplay meaning is conveyed by red/green alone.
- UI is HTML/CSS only. The world is canvas.
- Audio is WebAudio only. No audio files.
- Persistence uses `localStorage` with one save object.
- No network, no external fonts, no image assets, no audio assets.
- If a level object coordinate overlaps a solid tile, the loader moves it to the nearest floor tile using the level seed. The shipped coordinates are intended to be floor tiles.

# 2. CONTRACTS

## 2.1 Module layout

| File/module | Responsibility |
| --- | --- |
| `index.html` | Canvas, UI screens, HUD, button containers |
| `css/main.css` | Palette, hand-lettered typography, screen layout, HUD |
| `js/config.js` | Constants only |
| `js/rng.js` | Seeded RNG |
| `js/input.js` | Key binding, held/pressed state, remap, simulation |
| `js/audio.js` | WebAudio synth SFX/music |
| `js/storage.js` | Save/load settings, progression, high scores |
| `js/level.js` | Level data, reset, tile collision |
| `js/cat.js` | Cat state, movement, dash, melee, special, boosts |
| `js/mouse.js` | Mice AI, catch, wake, fail |
| `js/creature.js` | Collectible creatures |
| `js/pickup.js` | Collectibles, keys, secrets |
| `js/trap.js` | Traps and trap effects |
| `js/door.js` | Doors, keys, Breeze Door |
| `js/switch.js` | Switches and door linkage |
| `js/effects.js` | Particles, hit flash, trails, noise rings |
| `js/camera.js` | Camera follow and shake |
| `js/ui.js` | Screen state machine, HUD, HTML/CSS screens |
| `js/game.js` | Boot, fixed-step loop, start/restart/complete/fail |
| `js/debug.js` | Direct state functions and input simulation |

## 2.2 Global context

| Field | Type | Purpose |
| --- | --- | --- |
| `ctx.state` | string | Current UI/game state |
| `ctx.prevState` | string | State before settings/high scores |
| `ctx.levelId` | string | Current level id |
| `ctx.level` | LevelRecord | Loaded level data |
| `ctx.cat` | CatRecord | Player cat |
| `ctx.mice` | MouseRecord[] | Hostile/reward mice |
| `ctx.creatures` | CreatureRecord[] | Collectible creatures |
| `ctx.collectibles` | PickupRecord[] | Collectible pickups and key drops |
| `ctx.traps` | TrapRecord[] | Traps |
| `ctx.doors` | DoorRecord[] | Doors |
| `ctx.switches` | SwitchRecord[] | Switches |
| `ctx.landmarks` | LandmarkRecord[] | Furniture/landmarks |
| `ctx.secrets` | SecretRecord[] | Hidden rewards |
| `ctx.effects` | EffectRecord[] | Particles/trails/hit flashes |
| `ctx.noisePulses` | NoisePulseRecord[] | Noise pulses |
| `ctx.camera` | object | Camera position |
| `ctx.time` | object | Loop timing |
| `ctx.score` | integer | Current level score |
| `ctx.combo` | object | Combo count/multiplier/timer |
| `ctx.bestCombo` | integer | Best combo count this attempt |
| `ctx.hasKeys` | integer | Keys carried |
| `ctx.settings` | SettingsRecord | User settings |
| `ctx.progression` | ProgressionRecord | Unlocks/medals/Cat Naps |
| `ctx.highScores` | HighScoreRecord | High scores |
| `ctx.rng` | RNG | Seeded RNG |
| `ctx.failReason` | string/null | Failure reason |
| `ctx.winInfo` | object/null | Win summary |
| `ctx.hint` | object | Active hint |
| `ctx.audio` | object | Audio state |
| `ctx.input` | object | Input state |

Record shapes:

| Record | Required fields |
| --- | --- |
| LevelRecord | `id`, `name`, `seed`, `targetMinutes`, `spawn`, `exit`, `doors`, `switches`, `mice`, `creatures`, `collectibles`, `traps`, `landmarks`, `secrets`, `hint`, `silverScore`, `goldScore`, `musicId` |
| CatRecord | `x`, `y`, `vx`, `vy`, `facing`, `state`, `speed`, `dashTime`, `dashCooldown`, `meleeTime`, `meleeCooldown`, `specialTime`, `specialCooldown`, `boostSpeedUntil`, `boostDashUntil`, `boostMeleeUntil`, `invulnerableUntil`, `dizzyUntil`, `trailTimer` |
| MouseRecord | `id`, `type`, `x`, `y`, `vx`, `vy`, `facing`, `state`, `speed`, `baseScore`, `hasKey`, `asleep`, `stunUntil`, `wanderTimer`, `wakeTimer`, `caught` |
| CreatureRecord | `id`, `type`, `x`, `y`, `vx`, `vy`, `facing`, `state`, `speed`, `baseScore`, `caught`, `wanderTimer` |
| PickupRecord | `id`, `type`, `x`, `y`, `taken`, `score`, `boostType`, `duration` |
| TrapRecord | `id`, `type`, `x`, `y`, `armed`, `rearmUntil`, `activeUntil` |
| DoorRecord | `id`, `x`, `y`, `w`, `h`, `open`, `locked`, `keySlots`, `keysCollected`, `linkedSwitchIds`, `isBreeze`, `breezeOpenUntil` |
| SwitchRecord | `id`, `type`, `x`, `y`, `on`, `linkedDoorIds` |
| LandmarkRecord | `id`, `type`, `x`, `y`, `w`, `h`, `collision`, `secretId` |
| SecretRecord | `id`, `x`, `y`, `rewardType`, `revealed` |
| EffectRecord | `id`, `type`, `x`, `y`, `ttl`, `maxTtl`, `data` |
| NoisePulseRecord | `x`, `y`, `radius`, `ttl` |
| SettingsRecord | `reducedMotion`, `difficulty`, `keys`, `volume`, `musicVolume`, `sfxVolume` |
| ProgressionRecord | `unlockedLevels`, `bestMedal`, `catNaps`, `visualUnlocks`, `levelBest`, `secretsFound` |
| HighScoreRecord | `completions`, `bestPerLevel`, `bestTotal`, `rank` |

## 2.3 Module specifics

| Module | Required state fields | Required functions |
| --- | --- | --- |
| `config.js` | `TILE`, `FPS`, `DT`, `LEVEL_W`, `LEVEL_H`, `VIEW_W`, `VIEW_H`, `CAT_SPEED`, `CAT_RADIUS`, `MOUSE_RADIUS`, `PICKUP_RADIUS`, `DASH_SPEED`, `DASH_DURATION`, `DASH_IFRAMES`, `MELEE_RANGE`, `MELEE_HALF_ANGLE`, `MELEE_COOLDOWN`, `MELEE_DURATION`, `SPECIAL_RADIUS`, `SPECIAL_COOLDOWN`, `SPECIAL_DURATION`, `COMBO_TIME`, `SCORE_TABLE`, `MEDAL_THRESHOLDS`, `RANK_THRESHOLDS`, `UNLOCK_THRESHOLDS`, `TRAP_TABLE`, `BOOST_TABLE`, `NOISE_TABLE`, `DIFFICULTY_TABLE` | `get(action, difficulty)` for tables |
| `rng.js` | `ctx.rng.seed`, `ctx.rng.state` | `createRng(seed)`, `rngNext()`, `rngNextInt(min, max)` |
| `input.js` | `ctx.input.keys`, `ctx.input.held`, `ctx.input.pressed`, `ctx.input.buffer` | `initInput()`, `isHeld(action)`, `consumePress(action)`, `setKeyMap(action, keyCode)`, `simulateMove(dx, dy)`, `simulatePress(action)`, `resetInput()` |
| `audio.js` | `ctx.audio.ready`, `ctx.audio.musicId`, `ctx.audio.playing`, `ctx.audio.volume`, `ctx.audio.musicVolume`, `ctx.audio.sfxVolume` | `initAudio()`, `playSfx(name)`, `playMusic(id)`, `stopMusic()`, `setVolumes()`, `resumeOnInput()` |
| `storage.js` | `ctx.settings`, `ctx.progression`, `ctx.highScores` | `loadSave()`, `saveSave()`, `addHighScore(entry)`, `updateProgression(winInfo)`, `resetSave()` |
| `level.js` | `ctx.level`, `ctx.levelId` | `loadLevel(id)`, `resetLevel(id)`, `isSolidTile(tileX, tileY)`, `isSolidPoint(x, y, radius)`, `getExitDoor()`, `getSpawn()` |
| `cat.js` | `ctx.cat`, `ctx.hasKeys`, `ctx.score`, `ctx.combo` | `updateCat(dt)`, `moveCat(dt)`, `tryDash()`, `tryMelee()`, `trySpecial()`, `applyBoost(type)`, `bonkCat(cause)`, `setCatState(state)`, `getCatFacing()`, `isCatSafe()` |
| `mouse.js` | `ctx.mice` | `updateMice(dt)`, `wakeMouseById(id)`, `wakeMouseInRadius(x, y, radius)`, `catchMouse(id)`, `spawnMouse(type, x, y, sleeping)`, `getSqueakFail()` |
| `creature.js` | `ctx.creatures` | `updateCreatures(dt)`, `catchCreature(id)`, `spawnCreature(type, x, y)` |
| `pickup.js` | `ctx.collectibles`, `ctx.hasKeys` | `updatePickups(dt)`, `collectPickup(id)`, `spawnPickup(type, x, y)`, `dropKey(x, y)`, `revealSecret(id)`, `collectAllAt(x, y, radius)` |
| `trap.js` | `ctx.traps` | `updateTraps(dt)`, `triggerTrap(id)`, `bonkFromTrap(trap)`, `stunMiceInRadius(x, y, radius, duration)`, `spawnTrap(type, x, y)` |
| `door.js` | `ctx.doors`, `ctx.hasKeys` | `updateDoors(dt)`, `touchDoor(door)`, `consumeKey(door)`, `setDoorOpen(id, open)`, `startBreeze(door)` |
| `switch.js` | `ctx.switches` | `updateSwitches(dt)`, `activateSwitch(id, source)`, `setSwitchOn(id, on)`, `areSwitchesOn(door)` |
| `effects.js` | `ctx.effects`, `ctx.noisePulses` | `updateEffects(dt)`, `spawnCatchParticles(x, y, type)`, `spawnDashTrail(x, y, facing)`, `spawnHitFlash(x, y, screen)`, `spawnNoiseRing(x, y, radius)`, `clearEffects()` |
| `camera.js` | `ctx.camera` | `updateCamera(dt)`, `shake(magnitude, duration)`, `resetCamera()` |
| `ui.js` | `ctx.state`, `ctx.prevState`, `ctx.winInfo`, `ctx.failReason` | `showScreen(state)`, `updateHUD()`, `renderTitle()`, `renderLevelSelect()`, `renderSettings()`, `renderPause()`, `renderGameOver()`, `renderWin()`, `renderHighScores()`, `bindUI()` |
| `game.js` | `ctx`, `ctx.time`, `ctx.state` | `boot()`, `startLevel(id)`, `tick(dt)`, `completeLevel()`, `failLevel(reason)`, `restartLevel()`, `getFixedDt()` |
| `debug.js` | access to all `ctx` fields | See #8 Debug API |

# 3. VISUAL SPEC

Mousie-Butt is a bright, flat-vector kitchen mess: clean rounded shapes, hard black outlines, solid saturated fills, no gradients, no blur, no 3D lighting. The whole game looks like a paper cut-out board game that squeaks. Cat, mice, traps, doors, and pickups are large enough to read at 800×480. Every important state has a shape cue, not just a colour cue.

Lighting and atmosphere: flat top-down illumination. No dynamic light, no day/night, no shadow casting. The only “shadow” is a 3 px offset black shape at 15% opacity under cat/mice/traps. The atmosphere is upbeat and silly: bright floor, bold furniture, tiny crumbs, exaggerated squash-and-stretch.

Space: a top-down tile grid. Walls are dark indigo. Floors are saturated warm yellow. Furniture blocks space or acts as a passable landmark. The camera follows the cat and clamps to the level. The space is readable: exit is always cyan, locked doors are purple, switches are blue/yellow, traps are grey with black icons.

| Element | Shape | Colour | Shape cue | Motion / animation | Gameplay meaning |
| --- | --- | --- | --- | --- | --- |
| Floor | 32 px tile | `#FFD66B` / `#FFC94A` alternating | subtle checker | none | walkable |
| Wall | 32 px tile | `#4B3F72` | black edge | none | solid |
| Cat | round body, triangle ears, big head | `#FF8A3D` | black outline, white whiskers | idle bob, run leg, dash stretch | player |
| Scamper Mouse | small oval, round ears, thin tail | `#64B5F6` | round tail | tail wiggle, flee stretch | safe to catch |
| Key Mouse | small oval, round ears, key icon above | `#FFD93B` | key icon | faster flee stretch | drops key |
| Squeak Mouse | small oval, sharp ears, lightning tail | `#8E44AD` | yellow lightning tail | 0.4 s wake flash, fast chase | body contact fails unless safe |
| Bunny | round ears, small body | `#FF8FD8` | long ears | hop | collectible creature |
| Duck | oval body, beak | `#7ED6DF` | beak | waddle | collectible creature |
| Shrimp | crescent body, antennae | `#FF9F68` | curved body | scuttle | collectible creature |
| Cheese | wedge | `#FFD93B` | wedge hole | none | score |
| Fish | fish shape | `#4D96FF` | tail flick | none | speed boost |
| Bell | bell shape | `#FFA94D` | clapper | none | dash cooldown boost |
| Catnip | leafy ball | `#FF7AC0` | leaf notches | none | melee range boost |
| Key | key icon | `#FFD93B` | round head + teeth | none | unlocks doors |
| Snap Trap | grey jaws | `#B3B3B3` | tooth icon | snap 0.2 s | bonk trap |
| Catnip Bomb | round bomb | `#B3B3B3` | leaf icon | puff 0.2 s | stun mice |
| Bonk Boot | boot shape | `#B3B3B3` | star icon | shake 0.15 s | bonk + score penalty |
| Exit Door | door with arrow | `#00C2FF` | white arrow | opens 0.25 s | level win |
| Locked Door | door with lock | `#7A4FD0` | yellow lock | none | blocked until key/switch |
| Breeze Door | thin door with wind lines | `#00C2FF` | wind lines | open 0.8 s | timed dash puzzle |
| Switch | square base + lever | off `#4D96FF`, on `#FFD93B` | lever angle | clack 0.1 s | opens linked door |
| Secret | faint dashed tile | `#FFFFFF` 30% | dashed square | shimmer 0.5 s | reveal by dash/melee |
| Particles | 4 px circles/squares | element colour | shape varies by event | 0.35 s | catch/trap/boost feedback |
| Trail | rounded rectangle | `#FF8A3D` dash, `#FFD93B` boost | tapered | 0.25 s | dash/boost feedback |
| Hit flash | full screen or local circle | `#FFFFFF` | none | screen 0.15 s / local 0.08 s | fail/catch feedback |

# 4. GAMEPLAY SPEC

You are Mousie-Butt, a very confident orange cat who believes every mouse is a collectible snack, a score opportunity, and a tiny personal insult. You run freely through a bright kitchen, dash through danger, swipe with your paws, catch mice and creatures, collect silly boosts, activate switches, unlock doors, and reach the cyan exit before a Squeak Mouse squeaks you into a level restart. Score builds combos. Medals and ranks come from score. Levels ramp from a simple catch run into a noisy key-and-switch finale.

## 4.1 Records and rosters

### Mouse roster

| Type | Base score | Speed | Behaviour | Fail? | Notes |
| --- | ---: | ---: | --- | --- | --- |
| Scamper | 100 | wander 140, flee 180 | wanders, flees from cat within 220 px | No | passive mouse |
| Key Mouse | 250 | flee 210 | flees, drops key when caught | No | key source |
| Squeak Mouse | 150 | Casual 160, Normal 200, Insane 240 | asleep or chases cat/noise | Yes, unless cat safe | fail source |

### Collectible creature roster

| Type | Base score | Speed | Behaviour | Notes |
| --- | ---: | ---: | --- | --- |
| Bunny | 200 | 140 | hops away slowly | collectible creature |
| Duck | 250 | 130 | waddles away | collectible creature |
| Shrimp | 300 | 160 | scuttles away | collectible creature |

### Collectible roster

| Type | Base score | Effect | Duration |
| --- | ---: | --- | ---: |
| Cheese | 50 | none | 0 |
| Fish | 100 | movement speed +30% | 3 s |
| Bell | 150 | dash cooldown -25% | 5 s |
| Catnip | 250 | melee range +12 px | 4 s |
| Key | 0 | increments `hasKeys` | 0 |

### Trap roster

| Type | Trigger radius | Effect | Dizzy | Score penalty | Rearm |
| --- | ---: | --- | ---: | ---: | ---: |
| Snap Trap | 24 px | bonk to spawn | 0.5 s | 0 | 3 s |
| Catnip Bomb | 80 px effect | stun mice 1.5 s, +25 per stunned mouse, noise 160 px | 0 | 0 | 5 s |
| Bonk Boot | 20 px | bonk to spawn | 0.8 s | 250 min 0 | 4 s |

### Landmark roster

| Type | Size tiles | Collision | Notes |
| --- | ---: | --- | --- |
| Wall | 1×1 | solid | boundary |
| Fridge | 3×3 | solid | landmark |
| Bookshelf | 1×4 | solid | vertical |
| Cat Tree | 2×2 | solid | landmark |
| Kitchen Island | 3×2 | solid | landmark |
| Sofa | 4×2 | solid | landmark |
| Rug | 5×3 | passable | secret host |
| Plant | 1×1 | passable | secret host |
| Window | 3×1 | passable | decoration |

### Door and switch roster

| Type | Fields | Notes |
| --- | --- | --- |
| Exit Door | `keySlots`, `linkedSwitchIds`, `isBreeze=false` | win trigger |
| Breeze Door | `keySlots`, `linkedSwitchIds`, `isBreeze=true` | opens 0.8 s, stays open only if passed |
| Paw Switch | `type='paw'` | activated by melee |
| Noise Switch | `type='noise'` | activated by noise pulse |
| Dash Switch | `type='dash'` | activated by dash trail |

## 4.2 Systems

### Movement & Input [Tier 1]

- Cat movement uses remappable actions: up, down, left, right, dash, melee, special, pause.
- Default keys: `W`/`ArrowUp`, `S`/`ArrowDown`, `A`/`ArrowLeft`, `D`/`ArrowRight`, `Space` dash, `J` melee, `K` special, `Escape` pause.
- Input is sampled every logic frame. Movement vector is normalized, so diagonals do not exceed base speed.
- Base cat speed: 240 px/s.
- Fish boost speed: 312 px/s.
- Dizzy speed: 0 px/s.
- Facing updates when input magnitude > 0.1. If no input, facing persists.
- Input buffer for dash, melee, special: 0.10 s.
- Cat cannot pass through solid tiles or closed doors.
- Dizzy cat cannot move, dash, melee, or special until `dizzyUntil`.

### Dash [Tier 1]

- Dash can start if `dashCooldown <= 0`, `dashTime <= 0`, and cat is not dizzy.
- Dash direction = current movement direction if input exists, otherwise current facing.
- Dash duration: 0.20 s.
- Dash speed: 560 px/s.
- Dash i-frames: Casual 0.30 s, Normal 0.22 s, Insane 0.18 s.
- Dash cooldown: Casual 0.90 s, Normal 1.10 s, Insane 1.30 s.
- Bell boost multiplies dash cooldown by 0.75.
- During dash, cat is safe from Squeak contact and catches mice by body overlap.
- Dash leaves trail particles every 0.03 s.
- Dash emits a noise pulse radius 160 px.
- Dashing into a wall stops dash early but cooldown still starts.

### Melee Attack [Tier 1]

- Melee can be used if `meleeCooldown <= 0` and cat is not dizzy.
- Melee cooldown: 0.35 s.
- Melee duration: 0.10 s.
- Melee range: 36 px normal, 48 px with Catnip.
- Melee arc: 100° total, 50° half-angle.
- Melee catches any mouse or creature in the arc.
- Melee activates Paw Switches in the arc.
- Melee triggers Catnip Bomb traps in the arc.
- Melee reveals secrets if melee hitbox overlaps secret trigger radius 20 px.
- Melee emits noise radius 120 px.
- Melee causes a local hit flash on caught targets.

### Special Move: Mousie-Nado [Tier 2]

- Special can be used if `specialCooldown <= 0`, cat is not dashing, and cat is not dizzy.
- Special cooldown: 8 s.
- Special duration: 0.25 s.
- Special radius: 96 px.
- During special, cat is invulnerable for 0.25 s.
- All mice and creatures within radius are caught at the end of the special.
- Each catch scores normally with current combo.
- Special emits noise radius 240 px.
- Special creates 12 radial particles.
- Special cannot be used while dashing.

### Chase & Catch [Tier 1]

Catch occurs in these cases:

| Source | Rule |
| --- | --- |
| Passive mouse body | Scamper, Key, Bunny, Duck, Shrimp are caught by cat body overlap |
| Squeak body | Squeak is caught by cat body overlap only if cat is dashing or invulnerable |
| Melee | Any mouse or creature in melee hitbox is caught |
| Special | Any mouse or creature within 96 px at special end is caught |

On catch:

- Remove target.
- Add score: `baseScore * combo.multiplier`.
- Increment `combo.count`.
- Reset `combo.timer` to 2.0 s.
- Update `bestCombo`.
- Spawn catch particles.
- Spawn local hit flash.
- Emit noise pulse: mouse 80 px, creature 80 px.
- If Key Mouse caught, drop key at mouse position.
- If creature caught, increment `winInfo.pals`.
- Squeak Mouse caught by safe body, melee, or special scores 150 and does not fail.

### Mice, Creatures & Spawn Points [Tier 1/2]

- Cat spawn is defined per level.
- Mice and creatures start at level-defined spawn points.
- Mice do not respawn, except Insane difficulty may spawn one extra Squeak at 20.0 s in the nearest unoccupied mouse spawn point.
- Scamper/Key/creature wander: pick a random direction every 0.8–1.5 s, speed per roster.
- Scamper/Key/creature flee: if cat within 220 px, move directly away from cat.
- Key Mouse flees faster than Scamper.
- Squeak asleep: speed 0, emits no chase.
- Squeak wakes if cat within chase radius or a noise pulse overlaps it.
- Squeak wake tell: 0.4 s flash before chase.
- Squeak chase: move toward cat using difficulty speed.
- Stunned mouse: speed 0, no chase, cannot fail, can be caught.
- Mice collide with solid tiles and closed doors.
- Creatures collide with solid tiles and closed doors.

### Boosts [Tier 2]

Boosts are timed stat effects from collectibles.

| Boost | Source | Effect | Duration |
| --- | --- | --- | ---: |
| Speed | Fish | cat speed +30% | 3 s |
| Dash | Bell | dash cooldown × 0.75 | 5 s |
| Melee | Catnip | melee range +12 px | 4 s |

Rules:

- Boosts refresh duration to `max(currentRemaining, duration)`.
- Boosts do not stack multipliers.
- Boosts do not affect score multipliers.
- Boosts are visualized by trail colour: Fish `#FFD93B`, Bell `#FFA94D`, Catnip `#FF7AC0`.
- Reduced motion disables boost trails but keeps the stat effect.

### Traps [Tier 1/2]

- Traps are static entities.
- Traps are non-fatal.
- If cat is dashing or invulnerable, traps do not trigger.
- Snap Trap:
  - Trigger radius 24 px.
  - Bonks cat to level spawn.
  - Dizzy 0.5 s.
  - Invulnerable 0.75 s.
  - Combo reset.
  - Rearm 3 s.
- Bonk Boot:
  - Trigger radius 20 px.
  - Bonks cat to level spawn.
  - Dizzy 0.8 s.
  - Invulnerable 1.0 s.
  - Combo reset.
  - Score penalty 250, minimum 0.
  - Rearm 4 s.
- Catnip Bomb:
  - Triggered by cat body or melee.
  - Effect radius 80 px.
  - Stuns all mice in radius for 1.5 s.
  - +25 score per stunned mouse.
  - Emits noise radius 160 px.
  - Rearm 5 s.

### Noise [Tier 2]

Noise is a set of short pulses. There is no noise meter.

| Action | Noise radius |
| --- | ---: |
| Melee | 120 px |
| Dash | 160 px |
| Collect pickup/creature | 80 px |
| Special | 240 px |
| Catnip Bomb | 160 px |
| Secret reveal | 120 px |

Rules:

- Noise pulses last 0.5 s.
- At creation, noise wakes sleeping mice within radius.
- At creation, noise activates Noise Switches within radius.
- Noise spawns a visible ring particle.
- Reduced motion renders noise rings as a single 0.15 s thin circle.

### Objectives, Keys, Doors, Switches [Tier 2]

Objective:

- The only level objective is reach the exit.
- Keys and switches are sub-objectives that make the exit reachable.

Keys:

- Key Mouse catch drops one key.
- Cat body contact with key pickup increments `hasKeys`.
- If a locked door has `keySlots > 0`, cat must have `hasKeys > 0` to unlock.
- Touching a key-locked door consumes one key and increments `door.keysCollected`.
- Door unlocks when `keysCollected == keySlots` and all linked switches are on.
- If no key, door bounces with locked SFX.

Doors:

- Closed doors block cat and mice.
- Open doors are passable.
- Exit door triggers win when cat centre overlaps exit rectangle.
- Breeze Door:
  - When all linked switches become on, door opens for 0.80 s.
  - If cat overlaps the door while open, door becomes permanently open.
  - If cat does not pass through, door closes.
  - Linked switches may be toggled off/on to re-trigger.

Switches:

- Switches toggle.
- Paw Switch: activated by melee hitbox.
- Noise Switch: activated by noise pulse overlap.
- Dash Switch: activated by dash trail overlap.
- Switch activation plays SFX and hint.
- Door opens only when `keySlots` satisfied and all linked switches are on.

Puzzle types:

| Puzzle type | Rule | Used in |
| --- | --- | --- |
| Key Chase | Catch Key Mouse to unlock door | L2, L4, L5, L6 |
| Switch Relay | Turn on all linked switches | L3, L6 |
| Breeze Dash | Pass through a door open for 0.80 s | L3 |
| Noise Wake | Wake sleeping Key/Squeak with noise | L5 |
| Squeak Route | Navigate Squeak mice while chasing/catching | L4, L5, L6 |

### Score, Combo, Medals, Ranks [Tier 1/2]

Score:

- Score is integer.
- Score event: `score += baseScore * combo.multiplier`.
- Score events: catch mouse, catch creature, collect pickup, Catnip Bomb stun bonus.
- Key pickup gives 0 score.
- Secret reveal gives 0 score; revealed pickup gives score when collected.

Combo:

- `combo.count` starts at 0.
- `combo.timer` starts at 0.
- On score event: use current multiplier, then increment count, reset timer to 2.0 s.
- If timer expires, count = 0, multiplier = x1.
- Multiplier table:
  - count 0-2: x1
  - count 3-5: x2
  - count 6-8: x3
  - count 9-11: x4
  - count 12+: x5

Medals:

| Medal | Requirement |
| --- | --- |
| Bronze | Reach exit |
| Silver | Reach exit and score >= level silverScore |
| Gold | Reach exit and score >= level goldScore |

Best medal per level is stored.

Ranks:

Rank is based on `bestTotal` = sum of best scores for completed levels.

| Rank | bestTotal |
| --- | ---: |
| Napkin Napper | 0 |
| Cheese Chaser | 5,000 |
| Squeak Sleuth | 15,000 |
| Mouse Whisperer | 35,000 |
| Cat of Chaos | 70,000 |

High scores:

- On win, store completion entry: `score`, `levelId`, `medal`, `pals`, `date`.
- Keep top 10 completions by score.
- Update best per level if score is higher.
- Recalculate `bestTotal`.
- Recalculate rank.
- Save to localStorage.

### Secrets, Collectibles, Collectible Creatures, Rewards, Unlocks [Tier 2]

Secrets:

- Each secret has a trigger tile and reward type.
- Secret is revealed if cat dashes within 20 px of the secret tile or melee hitbox overlaps the secret tile.
- On reveal:
  - Spawn reward pickup at secret tile.
  - Set `revealed = true`.
  - Save `progression.secretsFound[levelId] = true`.
  - Spawn noise radius 120 px.
  - Spawn 8 particles.
- Secrets are one-time per level attempt.

Collectibles:

- Collectibles are static until collected.
- Collected by body contact or melee.
- Collectible scores use current combo.
- Collectible may apply boost.

Collectible creatures:

- Creatures are living pickups.
- Collected by body contact or melee.
- Creature scores use current combo.
- Creature count is shown on win screen as Pals.

Rewards:

- Cat Naps are calculated from best medals:
  - Bronze: 1
  - Silver: 2
  - Gold: 3
- `progression.catNaps` is the sum of best medal naps across all levels.
- Cat Naps are not a shop currency.

Unlocks:

| Unlock | Requirement | Effect |
| --- | ---: | --- |
| Level N+1 | Complete level N | Unlocked in level select |
| Blue Bow | 3 Cat Naps | Cat wears blue bow in title/level select |
| Gold Whisker Trail | 6 Cat Naps | Cat outline becomes gold in game; dash trail uses gold if motion is on |
| Squeaky Crown | 9 Cat Naps | Crown appears on cat in title/win; win SFX adds high squeak |

### Hints [Tier 2]

Hints are short in-game text, not a screen.

| Trigger | Text | Duration |
| --- | --- | ---: |
| Level start | Level hint | 3 s |
| Locked door touch | “Need a key!” | 1 s |
| Squeak wake | “Squeak!” | 1 s |
| Switch activate | “Clack!” | 1 s |
| Breeze door open | “Hurry!” | 1 s |
| Secret reveal | “Squeaky secret!” | 1 s |

Level hints:

| Level | Hint |
| --- | --- |
| L1 | “Dash through, don’t nap.” |
| L2 | “The key is on a mouse.” |
| L3 | “Toggle switches, then dash.” |
| L4 | “Squeaks bite. Dash doesn’t.” |
| L5 | “Loud paws wake sleepy keys.” |
| L6 | “Everything you meowed, all in one room.” |

### Map, World, Landmarks, Decoration [Tier 1/2]

- Levels are 40×24 tile grids.
- Tile size 32 px.
- Solid tiles: walls, solid landmarks, closed doors.
- Passable tiles: floor, rug, plant, window, open doors.
- Camera follows cat centre and clamps to level bounds.
- Camera offset is smooth with 8 px/s lerp, or immediate if reduced motion is off and delta is small.
- Landmarks are visual furniture and collision.
- Decoration is non-colliding: crumbs, paw prints, checker floor variation, bubbles near cat tree.
- Secret tiles are passable but reveal only by dash/melee.

## 4.3 Progression and difficulty

### Level unlock [Tier 2]

- Level 1 is always unlocked.
- Completing level N unlocks level N+1.
- Level select shows locked levels with lock icon.
- Locked levels cannot be selected.

### Difficulty ramp [Tier 2]

| Level | Name | Target min | Squeak count | Key slots | Switches | Trap count | Silver | Gold |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| L1 | Naptime Kitchen | 2 | 1 | 0 | 0 | 1 | 1,200 | 2,500 |
| L2 | Cheese Vault | 3 | 2 | 1 | 0 | 3 | 1,800 | 3,500 |
| L3 | Switch Shelf | 4 | 2 | 0 | 2 | 3 | 2,200 | 4,200 |
| L4 | Squeak Alley | 4 | 4 | 2 | 0 | 6 | 2,600 | 5,000 |
| L5 | Noise Maze | 5 | 3 | 2 | 0 | 7 | 3,000 | 5,800 |
| L6 | Meow Finale | 5 | 4 | 2 | 2 | 9 | 3,600 | 7,000 |

### Difficulty options [Tier 1]

| Setting | Casual | Normal | Insane |
| --- | ---: | ---: | ---: |
| Squeak speed px/s | 160 | 200 | 240 |
| Squeak chase radius px | 220 | 260 | 300 |
| Dash i-frame s | 0.30 | 0.22 | 0.18 |
| Dash cooldown s | 0.90 | 1.10 | 1.30 |
| Bonk Boot dizzy s | 0.50 | 0.50 | 0.80 |
| Bonk Boot score penalty | 0 | 250 | 250 |
| Extra Squeak at 20 s | No | No | Yes |

### Level rosters and coordinates

Coordinates are tile indices. Tile (0,0) is top-left. Object centres are placed at `(x * 32 + 16, y * 32 + 16)`.

#### Level 1: Naptime Kitchen

| Object | Coordinates | Notes |
| --- | --- | --- |
| Cat spawn | (3,3) |  |
| Exit | (37,20) | 1×2 vertical |
| Scamper mice | (10,6), (18,10), (26,6), (30,12) |  |
| Squeak mouse | (34,18) | asleep |
| Cheese | (12,8), (20,14), (28,10) |  |
| Fish | (16,16) | speed boost |
| Bell | (24,18) | dash boost |
| Secret: Catnip | (30,3) | behind Plant |
| Snap Trap | (22,10) | on Rug |
| Fridge | (2,2) | 3×3 solid |
| Kitchen Island | (14,4) | 3×2 solid |
| Rug | (22,8) | 5×3 passable |
| Plant | (30,4) | 1×1 passable |
| Cat Tree | (32,14) | 2×2 solid |
| Sofa | (8,18) | 4×2 solid |

#### Level 2: Cheese Vault

| Object | Coordinates | Notes |
| --- | --- | --- |
| Cat spawn | (3,3) |  |
| Exit | (37,20) | 1×2 vertical, keySlots 1 |
| Scamper mice | (8,8), (14,10), (20,4), (26,16), (34,6) |  |
| Key Mouse | (28,12) | drops key |
| Squeak mice | (12,16), (30,14) |  |
| Cheese | (10,12), (18,18), (24,12), (32,16) |  |
| Fish | (16,6), (28,18) |  |
| Bell | (22,14) |  |
| Secret: Fish | (18,13) | behind Cat Tree |
| Bunny | (36,8) | creature |
| Snap Traps | (14,14), (28,10) |  |
| Catnip Bomb | (20,12) |  |
| Bookshelf | (10,2) | 1×4 solid |
| Cat Tree | (18,14) | 2×2 solid |
| Fridge | (32,2) | 3×3 solid |
| Sofa | (14,18) | 4×2 solid |
| Rug | (24,8) | 5×3 passable |
| Window | (37,10) | 3×1 passable |

#### Level 3: Switch Shelf

| Object | Coordinates | Notes |
| --- | --- | --- |
| Cat spawn | (3,3) |  |
| Exit | (37,20) | open after Breeze Door |
| Breeze Door | (20,12) | linked to sw3a, sw3b |
| Paw Switch | (8,8) | sw3a |
| Dash Switch | (14,16) | sw3b |
| Scamper mice | (10,10), (14,6), (18,16), (24,10), (30,14), (34,18) |  |
| Squeak mice | (12,14), (26,18) |  |
| Cheese | (8,12), (16,8), (22,16), (28,8), (34,10) |  |
| Fish | (10,18), (20,10), (30,18) |  |
| Bell | (18,14), (32,6) |  |
| Secret: Cheese | (7,6) | behind Bookshelf |
| Secret: Bell | (30,15) | behind Rug |
| Duck creatures | (20,4), (36,18) |  |
| Snap Traps | (16,12), (26,14) |  |
| Catnip Bomb | (12,16) |  |
| Bookshelves | (6,6), (24,6) | 1×4 solid |
| Kitchen Island | (16,10) | 3×2 solid |
| Rug | (30,16) | 5×3 passable |
| Plant | (12,18) | 1×1 passable |
| Fridge | (36,2) | 3×3 solid |

#### Level 4: Squeak Alley

| Object | Coordinates | Notes |
| --- | --- | --- |
| Cat spawn | (3,3) |  |
| Exit | (37,20) | keySlots 2 |
| Key Mice | (10,14), (30,4) |  |
| Scamper mice | (14,4), (20,16), (26,10) |  |
| Squeak mice | (8,18), (16,10), (24,14), (32,16) |  |
| Cheese | (10,6), (14,12), (18,18), (24,8), (28,16), (34,12) |  |
| Fish | (12,10), (22,6), (30,18) |  |
| Bell | (16,8), (26,12), (34,8) |  |
| Secret: Catnip | (18,7) | behind Cat Tree |
| Secret: Bell | (12,15) | behind Sofa |
| Shrimp creatures | (36,10), (20,20), (28,2) |  |
| Snap Traps | (14,8), (24,10), (30,14) |  |
| Catnip Bombs | (18,14), (26,18) |  |
| Bonk Boot | (22,12) | on Rug |
| Cat Trees | (8,8), (18,8), (28,8) | 2×2 solid |
| Sofa | (12,16) | 4×2 solid |
| Fridge | (34,2) | 3×3 solid |
| Rug | (22,12) | 5×3 passable |

#### Level 5: Noise Maze

| Object | Coordinates | Notes |
| --- | --- | --- |
| Cat spawn | (3,3) |  |
| Exit | (37,20) | keySlots 2 |
| Key Mice | (22,10), (30,16) | (30,16) asleep |
| Scamper mice | (10,8), (14,14), (18,20), (26,6) |  |
| Squeak mice | (12,16), (20,12), (28,18) | asleep |
| Cheese | (6,6), (12,10), (18,4), (24,16), (30,8), (34,14), (38,6) |  |
| Fish | (10,18), (16,12), (22,8), (28,20) |  |
| Bell | (8,14), (14,20), (20,6), (26,12) |  |
| Secret: Fish | (9,12) | behind Bookshelf |
| Secret: Catnip | (36,19) | behind Fridge |
| Secret: Bell | (33,10) | behind Bookshelf |
| Bunny | (16,18) | creature |
| Duck | (24,14) | creature |
| Shrimp | (32,6) | creature |
| Snap Traps | (12,12), (18,14), (24,10), (30,16) |  |
| Catnip Bombs | (14,16), (26,8) |  |
| Bonk Boot | (20,12) |  |
| Bookshelves | (8,4), (8,12), (8,18), (16,2), (16,8), (16,16), (24,4), (24,12), (24,20), (32,2), (32,10), (32,18) | 1×4 solid |
| Fridge | (36,20) | 3×3 solid |
| Rug | (10,10) | 5×3 passable |

#### Level 6: Meow Finale

| Object | Coordinates | Notes |
| --- | --- | --- |
| Cat spawn | (3,3) |  |
| Exit | (37,20) | keySlots 2, linked sw6a, sw6b |
| Noise Switch | (24,18) | sw6a |
| Dash Switch | (12,6) | sw6b |
| Key Mice | (14,14), (30,10) |  |
| Scamper mice | (8,10), (18,8), (24,6), (28,16), (34,12) |  |
| Squeak mice | (10,16), (16,12), (22,18), (30,14) |  |
| Cheese | (6,8), (12,12), (18,14), (24,10), (28,4), (32,18), (36,10), (38,14) |  |
| Fish | (10,14), (16,6), (22,14), (28,12), (34,6) |  |
| Bell | (8,16), (14,18), (20,10), (26,8), (32,14) |  |
| Secret: Catnip | (2,1) | behind Fridge |
| Secret: Fish | (10,9) | behind Cat Tree |
| Secret: Bell | (16,15) | behind Sofa |
| Secret: Catnip | (22,11) | behind Rug |
| Bunny | (6,18), (34,18) | creatures |
| Duck | (12,20) | creature |
| Shrimp | (20,20) | creature |
| Snap Traps | (12,10), (20,12), (28,14), (32,10) |  |
| Catnip Bombs | (16,14), (24,16), (30,12) |  |
| Bonk Boots | (18,18), (26,10) |  |
| Fridge | (2,2) | 3×3 solid |
| Cat Trees | (10,10), (20,4) | 2×2 solid |
| Sofa | (16,16) | 4×2 solid |
| Bookshelves | (28,8), (34,14) | 1×4 solid |
| Rug | (22,12) | 5×3 passable |
| Plant | (8,18) | 1×1 passable |
| Window | (36,8) | 3×1 passable |
| Kitchen Island | (6,12) | 3×2 solid |

## 4.4 Feel [Tier 3]

- Input response is immediate; no artificial delay.
- Catch scales target to 1.2× for 0.10 s before particles.
- Combo SFX pitch rises with multiplier.
- Fail causes 4 px camera shake for 0.15 s, disabled by reduced motion.
- Dash has a quick “boing” squash on end.
- Squeak wake flash is 0.4 s.
- Breeze Door open has 0.80 s yellow wind lines.
- Win screen has cat bounce 0.80 s.
- All motion respects reduced motion.

# 5. CHARACTERS

## Cat: Mousie-Butt

Silhouette: orange round body, oversized head, triangular ears, white muzzle, big black nose, short tail. Crisp black outline.

Facings: 8-way. Facing changes from movement input. When dashing, cat stretches 1.2× along facing.

| State | Motion rule | Trigger |
| --- | --- | --- |
| idle | 2-frame blink, 0.15 s bob loop | no input |
| run | 3-frame leg cycle, 8 fps, 0.05 s bob | movement input |
| dash | stretched body, tail trails, 0.20 s | dash |
| melee | paw swings forward 0.10 s | melee |
| special | spins 360° over 0.25 s, radial puffs | special |
| dizzy | stars orbit for dizzy duration | trap bonk |
| fail | spins down, X eyes, 0.50 s | Squeak fail |
| win | bounces 3 times over 0.80 s | reach exit |

## Mice

Silhouette: small oval body, round or sharp ears, thin tail. Colour and tail shape identify type.

| Type | Silhouette cue | States needed |
| --- | --- | --- |
| Scamper | round ears, round blue tail | wander, flee, caught |
| Key Mouse | yellow body, key icon above | wander, flee, caught |
| Squeak | sharp ears, purple body, yellow lightning tail | asleep, wake, chase, stunned, caught, fail |

Mouse motion rules:

- Wander: 2-frame tail wiggle, 3 fps.
- Flee: body stretches 1.15× away from cat.
- Chase: body stretches 1.25× toward cat, ears back.
- Asleep: Zzz particles every 0.8 s.
- Wake: 0.40 s yellow flash.
- Stunned: stars orbit, body squashed 0.8×.
- Caught: puff of 12 particles, no corpse.

## Collectible creatures

| Type | Silhouette cue | Motion |
| --- | --- | --- |
| Bunny | long ears, pink | hop 0.4 s |
| Duck | beak, cyan | waddle 0.5 s |
| Shrimp | curved orange body, antennae | scuttle 0.3 s |

# 6. AUDIO

Audio is synthesized with WebAudio. No files.

| Name | Type | Recipe | When it plays |
| --- | --- | --- | --- |
| M_TITLE | music | 112 BPM, 4 bars. Square lead C4-E4-G4-C5, sawtooth bass C2/G2, 8th-note noise hats, volume 0.55 | title screen |
| M_GAME | music | 124 BPM, 4 bars. Square arpeggio C4-E4-G4-E4, sawtooth bass C2-C2-F2-F2, 8th-note noise hats, volume 0.50 | level select/game/win if not overridden |
| M_GAME_OVER | music | 90 BPM, 2 bars. Low square C2-G1-C2, noise thud each beat, volume 0.35 | game over screen |
| M_WIN | music | 124 BPM, 2 bars. Square arpeggio C4-E4-G4-C5-E5, sawtooth bass C2-F2, volume 0.60 | win screen |
| SFX_UI | SFX | triangle 988 Hz, 0.05 s, fast decay | button hover/click |
| SFX_MOVE | SFX | none | movement does not play SFX to avoid noise |
| SFX_DASH | SFX | sawtooth 220→880 Hz over 0.12 s + noise 0.05 s | dash start |
| SFX_MELEE | SFX | square 160 Hz 0.05 s + noise 0.03 s | melee swing |
| SFX_SPECIAL | SFX | sine 220→440 Hz 0.20 s + square arpeggio 523/659/784 Hz | special start |
| SFX_CATCH | SFX | square 523→880 Hz 0.06 s + triangle 131 Hz 0.05 s | catch mouse/creature |
| SFX_CATCH_SQUEAK | SFX | square 880→1760 Hz 0.08 s + triangle 262 Hz 0.04 s | catch Squeak safely |
| SFX_PICKUP | SFX | triangle 659→988 Hz 0.08 s | collect cheese/fish/bell/catnip |
| SFX_KEY | SFX | square 784 Hz 0.05 s + 1047 Hz 0.05 s | key pickup |
| SFX_LOCKED | SFX | square 98 Hz 0.10 s × 2 | locked door touch |
| SFX_SWITCH | SFX | square 440 Hz 0.06 s | switch activate |
| SFX_DOOR | SFX | sawtooth 196→392 Hz 0.20 s | door opens |
| SFX_BREEZE | SFX | square 659/523/659/523 Hz 0.40 s | Breeze Door opens |
| SFX_TRAP | SFX | sawtooth 200→50 Hz 0.15 s + noise 0.10 s | Snap/Bonk trigger |
| SFX_CATNIP | SFX | sine 330→660 Hz 0.15 s + square 523 Hz 0.05 s | Catnip Bomb triggers |
| SFX_SQUEAK_WAKE | SFX | square 1319→1760 Hz 0.10 s | Squeak wakes |
| SFX_SQUEAK_FAIL | SFX | square 880→220 Hz 0.20 s + sawtooth 98 Hz 0.30 s | level fail |
| SFX_COMBO | SFX | square 440 × (1 + 0.25 × (multiplier-1)) Hz, 0.05 s | combo multiplier changes |
| SFX_WIN | SFX | square 523/659/784/1047 Hz, 0.30 s | reach exit |
| SFX
