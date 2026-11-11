# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Game prompt: a game about frogs eating bugs | §4.1, §4.2, §5, §6 |
| Dimension: 2D | §1.1, §2.2, §3, §4 |
| Camera: top-down | §3, §4.2, §5 |
| Time model: real-time | §1.1, §1.2, §2.3, §9 |
| Movement model: free movement | §4.2 Frog Movement, §7 |
| Session shape: endless | §4.1, §4.2 Spawn System, §4.3 Progression |
| Failure: lose a life | §4.2 Lives and Failure, §5, §9 |
| Tone: silly | §3, §5, §6, §7 |
| Size: one screen, a few minutes | §1.1, §3, §4.3 |
| Win/lose: survive as long as possible, no ending, play forever | §4.1, §4.2 Lives and Failure, §4.3 |
| Core mechanics: catching | §0.3 Tier 1, §4.2 Tongue Catching |
| Supporting mechanics: scoring | §0.3 Tier 2, §4.2 Scoring |
| Extra mechanics: none | §0.2 Decisions, §4.2 Rosters |
| Art style: flat vector, clean flat shapes, solid colours, crisp edges | §3, §5 |
| Palette: saturated, bright, strong colours | §3 |
| Typography: hand-lettered, drawn, irregular letters | §3, §7 |
| Music: chiptune, retro console bleeps | §6 |
| Sound effects style: retro bleeps, synthesized chip sounds | §6 |
| Screens: title, pause, game over, high scores | §7 |
| HUD: health, score, combo counter | §7 |
| Effects: particles, hit flash | §3, §4.2, §5 |
| Accessibility: colour-blind safe palette, reduced motion, remappable keys, difficulty options | §0.2, §3, §4.2, §7, §9 |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| Prompt is “frogs eating bugs” | The player is a hungry cartoon frog on a single pond screen. Bugs are catchable targets. | Directly satisfies the prompt without adding unrelated systems. |
| 2D | All gameplay is 2D canvas drawing. | Required. |
| Top-down camera | Fixed top-down arena, no scrolling. | Required. |
| Real-time | Fixed 60 Hz simulation with render interpolation not required; one update per fixed step. | Required, deterministic, testable. |
| Free movement | 8-direction movement with WASD/arrow keys. Pointer/touch only affects tongue aim. | Required movement model. |
| Endless | No win condition. Run continues until lives reach 0. | Required. |
| Failure is lose a life | Frog starts with lives; collision with hazard bugs removes one life, not instant death. | Required. |
| Tone is silly | Round frog, exaggerated tongue, pop particles, goofy bug faces, bright chiptune. | Required. |
| One screen, a few minutes | Logical arena is 960×540. Difficulty ramps so normal skilled runs target 2–4 minutes, easy longer, hard shorter. | Required. |
| Survive as long as possible | Score is survival length plus bug-catching efficiency. | Required. |
| Core mechanics: catching | Catching is the only core verb: move, aim, launch tongue, catch edible bugs. | Required. |
| Supporting mechanics: scoring | Score and combo are Tier 2. They do not block Tier 1 core catching. | Required. |
| Extra mechanics: none | No powerups, no traps, no pickups, no upgrades, no weapons, no abilities beyond movement and tongue catching. | Required. |
| Flat vector art | No gradients, no shadows, no blur. Solid fills, crisp outlines. | Required. |
| Saturated palette | Bright saturated flat colors, but accessible by shape and luminance. | Required. |
| Hand-lettered typography | UI uses a hand-lettered font stack with system fallbacks. | Required. |
| Chiptune music | Simple square/triangle arpeggio loop. | Required. |
| Retro bleeps | All sounds synthesized from oscillators and noise. | Required. |
| Screens: title, pause, game over, high scores | Exactly these four screens. Options/remap are embedded in title/pause, not separate screens. | Required. |
| HUD: health, score, combo counter | Exactly these three HUD elements. | Required. |
| Effects: particles, hit flash | Exactly these two effects. No screen shake, no trails, no extra overlays. | Required. |
| Colour-blind safe palette | No red/green-only distinctions. Hazards have spiky silhouettes and angry faces; edible bugs have round cute silhouettes. | Required. |
| Reduced motion | Toggle reduces particles, blinking, and hit-flash intensity. | Required. |
| Remappable keys | All keyboard actions can be remapped. Pointer/touch remains supported. | Required. |
| Difficulty options | Easy, Normal, Hard selectable in title/pause. | Required. |
| Arena size | 960×540 logical pixels, one screen. | Creates a fixed, testable play area. |
| Player identity | The player controls an unnamed hungry frog. No character-select system. | Keeps scope tiny and prompt-focused. |
| Edible bug types | Exactly 3: Fly, Moth, Dragonfly. | Enough variety for core catching without extra mechanics. |
| Hazard bug types | Exactly 2: Angry Wasp, Hornet. | Provides required life loss without adding traps or powerups. |
| Traps | 0. | Extra mechanics are none. |
| Pickups | 0. | Extra mechanics are none. |
| Input | Keyboard: WASD/arrows move, Space/J launches tongue. Pointer/touch sets aim and can launch tongue. | Supports free movement and accessible keyboard play. |
| Aim | Keyboard players aim in last movement direction. Pointer players aim toward pointer. | Keeps keyboard-only players functional. |
| Lives | Normal 3, Easy 5, Hard 2. | Required life-loss failure. |
| Invulnerability | 1.5 seconds after damage, with blink unless reduced motion. | Prevents unfair instant death. |
| Tongue | One active tongue, 170 px reach, 0.26 s cooldown. | Core mechanic needs clear, readable numbers. |
| Catching rule | Tongue catches the first edible bug whose hitbox intersects the tongue capsule. Hazards are not catchable. | Simple, testable core mechanic. |
| Combo | Consecutive catches within a time window increase multiplier up to 10. | Supports scoring without extra mechanics. |
| High scores | Local top 10 scores, no name entry. | Avoids adding a text-input system not requested. |
| High score data | `{score, difficulty, date}`. | Provides useful high-score info without player-name system. |
| Music | Looping chiptune track in title and gameplay; stops on game over. | Required audio. |
| Sound effects | Synthesized bleeps only. | Required audio style. |
| UI implementation | DOM/CSS screens over canvas. Game world is canvas. | Required HTML/CSS for UX. |
| Random source | Seeded mulberry32 RNG per run. | Deterministic tests. |
| Collision | Circle-circle for body hazards; capsule-circle for tongue catching. | Precise and simple. |
| Pause | Stops simulation and music, shows pause screen. | Required. |
| Restart | Available from pause and game over. | Required for endless survival loop. |
| Difficulty change during pause | Selecting a new difficulty in pause restarts the run with that difficulty. | Avoids ambiguous mid-run rule changes. |
| Reduced motion behaviour | Particles disabled, hit flash becomes static outline, no blinking. | Required accessibility. |
| Remap behaviour | Key capture in title/pause. Conflicts disallowed for core actions. | Required accessibility. |
| High scores persistence | `localStorage` with in-memory fallback. | Practical local high scores. |

## 0.3 Tiers

| Tier | Priority | Contains | Does not contain | Done when |
| --- | --- | --- | --- | --- |
| Tier 1 | Highest | Core catching only: fixed arena, top-down art, chiptune audio, title/pause/game-over/high-score screen shells, frog movement, tongue catching, edible bug spawning, hazard bugs, lives/failure, game over, HUD health, particles, hit flash, colour-blind safe palette, reduced motion, remappable keys, difficulty options. | Score values, combo multiplier rules, populated high scores. | A player can start a run, catch bugs, get hit, lose lives, pause, remap keys, choose difficulty, reduce motion, and lose. |
| Tier 2 | Required supporting | Scoring: base scores, combo counter, combo timer, score multiplier, score display, game-over score, local high-score saving and list. | Extra mechanics, powerups, traps, pickups. | A player sees score and combo, and high scores are stored and shown. |
| Tier 3 | None | No extra mechanics are allowed. Any further work is polish only, not new mechanics. | New systems. | Not applicable. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Concept | Value |
| --- | --- |
| Logical canvas size | 960 × 540 px |
| Coordinate origin | Top-left |
| X axis | Right is positive |
| Y axis | Down is positive |
| Speed units | pixels per second |
| Distance units | pixels |
| Time units | seconds |
| Fixed timestep | `FIXED_DT = 1 / 60` |
| Render loop | `requestAnimationFrame`, accumulator, update fixed steps only |
| Angles | radians, `atan2(y, x)` |
| Hitboxes | circles and capsules |
| Entity sizes | defined in §4.2 records |
| Safe arena bounds | `x: [24, 936]`, `y: [24, 516]` |
| Entity centre clamp | `x: [radius+24, 936-radius]`, `y: [radius+24, 516-radius]` |
| Score type | non-negative integer |
| Lives type | integer |
| Timer type | seconds |

## 1.2 Important conventions

| Convention | Rule |
| --- | --- |
| Fixed step | Simulation only advances in exact `FIXED_DT` steps. Render does not mutate gameplay. |
| Paused | No simulation updates. `run.time` does not advance. Music and sound are stopped. |
| Game over | Simulation stops. Final screen shows after save. |
| RNG | Use seeded `mulberry32`. Seed is `Date.now()` unless debug sets a seed. All run randomness uses `ctx.rng`. |
| No external physics | No physics engine. Simple collision math only. |
| No canvas UI | HUD and screens are DOM/CSS. Game entities are canvas. |
| No gradients | Flat fills and solid outlines only. |
| No red/green-only meaning | Colour-blind safety enforced by shape and luminance. |
| Reduced motion | When enabled, particles are not spawned, entity hit flash is static, and blinking is replaced by solid outline. |
| Remappable keys | Default keys are fallback. Player can remap all keyboard actions. |
| Difficulty | Stored in `settings.difficulty`. Applied when a run starts. |
| High scores | Stored in `localStorage` key `frogBugHighScoresV1`. If unavailable, store in memory. |
| Input capture | During remap capture, all gameplay input is ignored except Escape to cancel. |
| Pointer input | Optional. Keyboard-only play must be complete. |
| Collision order | 1. tongue catches edible bugs, 2. hazard bugs damage frog, 3. bounds clamp. |
| Entity cleanup | Removed entities are filtered out after updates. |
| Sound | All sounds are synthesized. No audio files. |
| Music | Chiptune loop. Stops on pause/game over. Restarts on run start. |
| Determinism | Tests may call `debug.setSeed(n)` and run exact fixed steps. |

# 2. CONTRACTS

## 2.1 Module layout

| File | Responsibility | Exposes |
| --- | --- | --- |
| `index.html` | Canvas and DOM screens/HUD. | DOM ids. |
| `style.css` | Hand-lettered UI, HUD, screens, accessibility styles. | CSS. |
| `js/main.js` | Bootstrap, loop, run lifecycle. | `startGame`, `pauseGame`, `resumeGame`, `restartRun`, `returnToTitle`, `loop`. |
| `js/state.js` | Global context, run state, settings, high scores. | `createContext`, `initRun`, `setPhase`, `saveHighScore`. |
| `js/rng.js` | Seeded RNG. | `createRng`, `next`, `range`, `chance`, `pickWeighted`. |
| `js/input.js` | Keyboard/pointer input, remapping, aim. | `bindInput`, `handleKey`, `handlePointer`, `getMovementVector`, `getAimDirection`, `setKeyMap`, `captureKey`. |
| `js/entities.js` | Entity factories and record creation. | `createFrog`, `createEdibleBug`, `createHazardBug`, `createTongue`, `createParticle`, `createHitFlash`. |
| `js/systems/frog.js` | Frog movement, bounds, facing. | `updateFrog`. |
| `js/systems/tongue.js` | Tongue launch, movement, catch detection. | `updateTongue`, `fireTongue`, `catchCollisions`. |
| `js/systems/bugs.js` | Bug spawn and movement. | `spawnBugs`, `updateEdibleBugs`, `updateHazardBugs`. |
| `js/systems/combat.js` | Hazard collisions, lives, game over. | `updateHazardCollisions`, `damageFrog`, `checkGameOver`. |
| `js/systems/scoring.js` | Score, combo, multiplier. | `addCatchScore`, `updateCombo`. |
| `js/systems/effects.js` | Particles and hit flash. | `updateParticles`, `updateHitFlashes`. |
| `js/render.js` | Canvas drawing. | `renderFrame`. |
| `js/audio.js` | Synthesized sound and music. | `playSound`, `startMusic`, `stopMusic`. |
| `js/ui.js` | DOM screens, HUD, state machine. | `showScreen`, `updateHUD`, `updateScreens`. |
| `js/storage.js` | Settings and high-score persistence. | `loadSettings`, `saveSettings`, `loadHighScores`, `saveHighScores`. |
| `js/debug.js` | Debug API. | `debug.*`. |

## 2.2 Global context

The global context is `window.FrogGame`.

| Field | Type | Required subfields | Purpose |
| --- | --- | --- | --- |
| `version` | string | — | Build tag. |
| `settings` | object | `difficulty`, `keyMap`, `reducedMotion` | Persistent user options. |
| `input` | object | `keys`, `pointerX`, `pointerY`, `pointerActive`, `aim`, `capturingAction`, `lastAction` | Current input state. |
| `run` | object | `phase`, `time`, `seed`, `lives`, `maxLives`, `score`, `combo`, `comboTimer`, `difficulty`, `nextEdibleAt`, `nextHazardAt`, `hazardMax`, `startedAt`, `endedAt` | Current run state. |
| `entities` | object | `frog`, `tongue`, `edibleBugs`, `hazardBugs`, `particles`, `hitFlashes` | All gameplay entities. |
| `highScores` | array | entries `{score, difficulty, date}` | Persisted top scores. |
| `rng` | object | `seed`, `state`, `next`, `range`, `chance`, `pickWeighted` | Deterministic randomness. |
| `audio` | object | `enabled`, `playSound`, `startMusic`, `stopMusic` | Audio API. |
| `ui` | object | `screen`, `previousScreen`, `remapAction`, `message`, `hud` | UI state. |
| `debug` | object | functions only | Testing and state inspection. |

Required records:

| Record | Required fields |
| --- | --- |
| `Frog` | `id`, `x`, `y`, `vx`, `vy`, `radius`, `facing`, `invulnTimer`, `hitFlashTimer`, `state` |
| `Tongue` | `active`, `x`, `y`, `dirX`, `dirY`, `length`, `width`, `activeTimer`, `state`, `originX`, `originY` |
| `EdibleBug` | `id`, `type`, `kind: "edible"`, `x`, `y`, `vx`, `vy`, `radius`, `speed`, `heading`, `wanderTimer`, `lifetime`, `hitFlashTimer`, `baseScore`, `state` |
| `HazardBug` | `id`, `type`, `kind: "hazard"`, `x`, `y`, `vx`, `vy`, `radius`, `speed`, `phase`, `hitFlashTimer`, `state` |
| `Particle` | `x`, `y`, `vx`, `vy`, `life`, `maxLife`, `size`, `color`, `shape` |
| `HitFlash` | `x`, `y`, `radius`, `life`, `maxLife`, `color`, `shape` |
| `HighScore` | `score`, `difficulty`, `date` |
| `Settings` | `difficulty: "easy" | "normal" | "hard"`, `keyMap`, `reducedMotion: boolean` |
| `KeyMap` | `up`, `down`, `left`, `right`, `catch`, `pause`, `restart`, `highScores`, `confirm`, `difficultyCycle` |

## 2.3 Module specifics

| Module | Function | Contract |
| --- | --- | --- |
| `main.js` | `startGame(difficulty)` | Creates a new run, sets `run.phase = "playing"`, starts music. |
| `main.js` | `pauseGame()` | If playing, sets `run.phase = "paused"`, stops music, shows pause screen. |
| `main.js` | `resumeGame()` | If paused, sets `run.phase = "playing"`, starts music, hides pause screen. |
| `main.js` | `restartRun()` | Starts a new run with current difficulty. |
| `main.js` | `returnToTitle()` | Stops run, shows title. |
| `main.js` | `loop(timestamp)` | Accumulates real dt, calls `update(FIXED_DT)` only in whole steps, then `renderFrame`. |
| `state.js` | `initRun(difficulty, seed)` | Resets run, entities, spawn timers, RNG, lives, score, combo. |
| `state.js` | `setLives(n)` | Sets `run.lives` and updates HUD. |
| `state.js` | `addScore(amount)` | Adds integer score, updates HUD. |
| `state.js` | `incrementCombo()` | Increments `run.combo`, resets `run.comboTimer`. |
| `state.js` | `resetCombo()` | Sets `run.combo = 0`, `run.comboTimer = 0`. |
| `state.js` | `saveHighScore()` | Inserts `{score, difficulty, date}`, sorts, keeps 10. |
| `rng.js` | `next()` | Returns float `[0,1)`. |
| `rng.js` | `range(min, max)` | Returns float in range. |
| `rng.js` | `pickWeighted(items)` | Picks item by weight. |
| `input.js` | `getMovementVector()` | Returns normalized `x,y` from mapped movement keys. |
| `input.js` | `getAimDirection()` | Returns normalized aim from pointer if active, otherwise frog facing. |
| `input.js` | `setKeyMap(map)` | Validates no duplicate core actions, then applies. |
| `input.js` | `captureKey(action)` | Starts remap capture for one action. |
| `entities.js` | `createFrog(x, y)` | Returns valid `Frog`. |
| `entities.js` | `createEdibleBug(type, x, y)` | Returns valid `EdibleBug`. |
| `entities.js` | `createHazardBug(type, x, y)` | Returns valid `HazardBug`. |
| `entities.js` | `createTongue(x, y, dirX, dirY)` | Returns valid `Tongue`. |
| `entities.js` | `createParticle(...)` | Returns valid `Particle`. |
| `entities.js` | `createHitFlash(...)` | Returns valid `HitFlash`. |
| `systems/frog.js` | `updateFrog(ctx, dt)` | Applies movement, bounds, facing, invuln timer. |
| `systems/tongue.js` | `fireTongue(ctx)` | Creates tongue if cooldown passed. |
| `systems/tongue.js` | `updateTongue(ctx, dt)` | Advances tongue state, calls catch detection. |
| `systems/tongue.js` | `catchCollisions(ctx, dt)` | Catches first intersecting edible bug. |
| `systems/bugs.js` | `spawnBugs(ctx, dt)` | Spawns edible and hazard bugs according to timers and caps. |
| `systems/bugs.js` | `updateEdibleBugs(ctx, dt)` | Moves and expires edible bugs. |
| `systems/bugs.js` | `updateHazardBugs(ctx, dt)` | Moves hazard bugs. |
| `systems/combat.js` | `updateHazardCollisions(ctx, dt)` | Damages frog and removes hazard on collision. |
| `systems/combat.js` | `damageFrog(ctx)` | Reduces lives, starts invuln, effects, sound. |
| `systems/combat.js` | `checkGameOver(ctx)` | Sets game over if lives <= 0. |
| `systems/scoring.js` | `addCatchScore(ctx, bug)` | Adds base score times combo multiplier. |
| `systems/scoring.js` | `updateCombo(ctx, dt)` | Decreases combo timer, resets combo at 0. |
| `systems/effects.js` | `updateParticles(ctx, dt)` | Advances and removes particles. |
| `systems/effects.js` | `updateHitFlashes(ctx, dt)` | Advances and removes hit flashes. |
| `render.js` | `renderFrame(ctx)` | Draws arena, entities, effects. |
| `audio.js` | `playSound(name)` | Plays named synthesized sound. |
| `audio.js` | `startMusic()` | Starts chiptune loop. |
| `audio.js` | `stopMusic()` | Stops music. |
| `ui.js` | `showScreen(name)` | Shows one of `title`, `pause`, `gameOver`, `highScores`. |
| `ui.js` | `updateHUD()` | Updates health, score, combo DOM. |
| `storage.js` | `loadSettings()` | Returns validated settings or defaults. |
| `storage.js` | `saveSettings(settings)` | Persists settings. |
| `storage.js` | `loadHighScores()` | Returns validated array. |
| `storage.js` | `saveHighScores(scores)` | Persists array. |

# 3. VISUAL SPEC

The game is a bright, silly top-down pond. The player is a round amber frog with large eyes and a comically long pink tongue. Edible bugs are cute, round, brightly coloured dots with tiny wings. Hazard bugs are spiky, angry, and unmistakably dangerous. The pond is a flat saturated blue-teal rectangle with simple lily pad shapes. Everything is flat vector: solid fills, crisp dark outlines, no gradients, no shadows, no blur. The visual language separates catchable and dangerous bugs by silhouette first, colour second, satisfying colour-blind safety.

Lighting and atmosphere are flat and cheerful. There is no dynamic light. The pond feels like a cartoon game board: bright, readable, high contrast. The only atmospheric motion is gentle idle bobbing and bug movement, reduced when reduced motion is on.

The space is one fixed screen. The playable pond is inset from the window edge by a thick dark border. Lily pads are decorative obstacles only visually; they do not block movement. The frog, tongue, bugs, particles, and hit flashes are the only functional world objects.

| Element | Shape recipe | Colour recipe | Size / numbers | Animation |
| --- | --- | --- | --- | --- |
| Pond arena | Rounded rectangle border, flat interior | Background `#083A5B`, border `#101820` | 960×540, border 24 px | None |
| Lily pads | Flat oval leaf with split notch | `#0F766E` fill, `#101820` outline | Decorative only | Optional tiny bob disabled in reduced motion |
| Frog body | Round blob, wide mouth, large eyes | Body `#FFB703`, outline `#101820`, eyes white/black | Radius 14 px | Idle bob, move squash, tongue stretch |
| Tongue | Capsule from frog mouth | `#FF5D8F` fill, `#101820` outline | Width 10 px, length 170 px | Extend, hold, retract |
| Fly | Small round bug, two tiny wings | `#FFD60A`, outline `#101820` | Radius 8 px | Wing flap, hover bob |
| Moth | Soft round moth with wing lobes | `#E5E5E5`, purple spots `#7209B7` | Radius 9 px | Slow flutter |
| Dragonfly | Slim darting body, two wings | `#00D4FF`, outline `#101820` | Radius 8 px | Dart, pause |
| Angry Wasp | Spiky oval, angry brows, stinger | `#7209B7`, stripes `#FFD60A` | Radius 11 px | Chase wobble |
| Hornet | Larger spiky bug, zigzag motion | `#E63946`, outline `#101820` | Radius 12 px | Zigzag chase |
| Particles | Small circles/squares | Catch: bug colour; damage: `#FF5D8F` or `#7209B7` | 3–8 px, 8–12 per event | Fade and drift |
| Hit flash | White/yellow circle outline | `#FFFFFF` or `#FFFBEB` | Radius entity radius + 4 px | Flash 0.25 s; static outline in reduced motion |
| HUD health | Heart shapes | `#FF5D8F` | 3–5 hearts depending difficulty | Heart pulses briefly when lost |
| HUD score | Large hand-lettered number | `#FFFFFF` | Top centre | None |
| HUD combo | `x2` through `x10` | `#00D4FF` | Below score | Pulse on increment |
| Typography | Irregular hand-lettered font stack | High contrast white on dark panels | Title large, HUD medium | None |

# 4. GAMEPLAY SPEC

The game is an endless top-down survival game about catching bugs with a frog’s tongue. The player moves freely around one pond screen and launches a tongue to catch edible bugs. Hazard bugs chase the frog and remove one life on contact. The run continues until lives reach zero. Scoring rewards quick consecutive catches, and high scores are stored locally. There are no traps, pickups, powerups, upgrades, or extra mechanics.

## 4.1 Rosters

| Category | Count | Items |
| --- | ---: | --- |
| Player | 1 | Frog |
| Tongues | 1 active maximum | Tongue |
| Edible bugs | 3 types | Fly, Moth, Dragonfly |
| Hazard bugs | 2 types | Angry Wasp, Hornet |
| Traps | 0 | None |
| Pickups | 0 | None |
| Effects | 2 | Particles, hit flash |
| Screens | 4 | Title, pause, game over, high scores |
| HUD elements | 3 | Health, score, combo counter |

## 4.2 Systems

### Frog Movement — Tier 1

| Rule | Number |
| --- | ---: |
| Movement input | Up, Down, Left, Right actions |
| Default keys | `W/A/S/D`, arrow keys |
| Speed | 165 px/s |
| Acceleration | Instant velocity assignment |
| Direction | Normalized 8-direction vector |
| Facing | Last non-zero movement vector |
| Bounds | Centre clamped inside arena |
| Invulnerability after damage | 1.5 s |
| Blink while invulnerable | 0.15 s on/off unless reduced motion |
| Hit flash | 0.25 s |

Rules:

1. `getMovementVector()` returns a normalized vector from mapped movement keys.
2. Frog velocity is set to `direction * 165` each fixed step.
3. If no movement input exists, velocity is set to zero.
4. If movement direction is non-zero, `frog.facing = atan2(direction.y, direction.x)`.
5. Frog position is clamped to the arena.
6. The frog is controllable while invulnerable.
7. The frog is not controllable while dead/game over.

### Tongue Catching — Tier 1

| Rule | Number |
| --- | ---: |
| Catch input | Space, J, pointer down, touch down |
| Hold-to-repeat | Yes |
| Max active tongues | 1 |
| Cooldown after press | 0.26 s |
| Tongue reach | 170 px |
| Tongue width | 10 px |
| Extend time | 0.08 s |
| Hold time | 0.08 s |
| Retract time | 0.08 s |
| Active duration | 0.24 s |
| Origin | Frog centre + facing * 18 px |
| Aim | Pointer if active, else frog facing |
| Catch collision | Capsule-circle |
| Catch effect | Bug removed, particles, hit flash, sound |
| Hazard interaction | Tongue passes through hazards with no effect |

Rules:

1. Pressing catch when cooldown is ready calls `fireTongue()`.
2. `fireTongue()` creates a tongue with origin at the frog mouth and aim from `getAimDirection()`.
3. The tongue state machine is:
   - `extending`: tip distance = `length * (timer / 0.08)`.
   - `holding`: tip distance = `length`.
   - `retracting`: tip distance = `length * (1 - (timer - 0.16) / 0.08)`.
4. During any active state, check all edible bugs for capsule-circle intersection.
5. The first intersecting edible bug is caught.
6. Catching ends the tongue immediately.
7. If no bug is caught, the tongue finishes its active duration and disappears.
8. Catching spawns 8 particles and a 0.25 s hit flash on the bug.
9. Reduced motion disables particles and uses static hit flash.

### Edible Bug Spawning and Movement — Tier 1

| Type | Speed | Radius | Wander | Lifetime | Base score | Spawn weight |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| Fly | 75 px/s | 8 px | Random heading change every 0.4–0.9 s, turn ±40° | 18 s | 10 | 60% |
| Moth | 55 px/s | 9 px | Sine flutter, random heading every 0.8–1.5 s | 18 s | 15 | 25% |
| Dragonfly | 140 px/s | 8 px | Choose target, dart, pause 0.2 s, repeat | 18 s | 25 | 15% |

Spawn rules:

1. At run start, spawn 6 edible bugs.
2. After start, edible spawn interval uses difficulty base and ramp.
3. Maximum alive edible bugs: 14.
4. Spawn point is inside arena and at least 180 px from the frog.
5. If 20 spawn attempts fail, skip that spawn attempt.
6. Bugs reflect off arena bounds.
7. Bugs fade out during the last 1 s of lifetime and are removed at 18 s.
8. Edible bugs do not damage the frog.

### Hazard Bugs — Tier 1

| Type | Speed | Radius | Behaviour | Damage |
| --- | ---: | ---: | --- | ---: |
| Angry Wasp | 95 px/s | 11 px | Direct chase | 1 life |
| Hornet | 135 px/s | 12 px | Chase plus perpendicular sine zigzag, 2 Hz, ±40 px/s | 1 life |

Hazard spawn rules:

1. No hazards at run start.
2. Hazard spawn interval uses difficulty table in §4.3.
3. Hazard max alive uses difficulty table in §4.3.
4. Spawn point is inside arena and at least 260 px from the frog.
5. Spawn weights: Wasp 70%, Hornet 30%.
6. Hazards are removed after damaging the frog.
7. Hazards reflect/clamp to arena bounds.
8. Hazards are not catchable.

### Lives, Hit Handling, Game Over — Tier 1

| Rule | Number |
| --- | ---: |
| Normal lives | 3 |
| Easy lives | 5 |
| Hard lives | 2 |
| Damage trigger | Circle-circle overlap between frog and hazard |
| Damage effect | Remove hazard, lives--, invuln 1.5 s, hit flash, particles, sound |
| Invulnerability | 1.5 s |
| Game over trigger | `run.lives <= 0` |
| Game over state | Stop simulation, stop music, show game over screen, save high score |

Rules:

1. If a hazard overlaps the frog and `frog.invulnTimer <= 0`, call `damageFrog()`.
2. `damageFrog()` reduces lives by 1 and removes the hazard.
3. Set `frog.invulnTimer = 1.5`.
4. Spawn 12 damage particles and a hit flash.
5. If `run.lives <= 0`, set `run.phase = "gameOver"`, set `run.endedAt`, save high score, show game over.
6. During invulnerability, hazards pass through the frog without damage.

### Difficulty Options — Tier 1

| Difficulty | Lives | Edible interval base/floor | Hazard interval base/floor | Hazard max start/cap | Hazard speed multiplier | Combo window |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Easy | 5 | 0.8 / 0.50 s | 20 / 10 s | 1 / 3 | 0.8 | 2.5 s |
| Normal | 3 | 0.9 / 0.55 s | 14 / 7 s | 3 / 6 | 1.0 | 2.0 s |
| Hard | 2 | 0.9 / 0.55 s | 9 / 5 s | 4 / 8 | 1.25 | 1.6 s |

Rules:

1. Difficulty is selected on title or pause.
2. Changing difficulty in pause restarts the run.
3. Difficulty applies only when a run starts.
4. All numeric spawn and life values use the selected difficulty.

### Scoring — Tier 2

| Rule | Number |
| --- | ---: |
| Fly score | 10 |
| Moth score | 15 |
| Dragonfly score | 25 |
| Hazard score | 0 |
| Score type | integer |
| Score formula | `floor(baseScore * multiplier)` |
| HUD score | visible during play and game over |

Rules:

1. When an edible bug is caught, call `addCatchScore(bug)`.
2. The multiplier is determined by combo rules in §4.2 Combo.
3. Score is added immediately.
4. Game over displays final score.
5. High scores use final score.

### Combo Counter — Tier 2

| Rule | Number |
| --- | ---: |
| Combo window | Difficulty-dependent: Easy 2.5 s, Normal 2.0 s, Hard 1.6 s |
| Combo increment | One catch within window |
| Combo reset | Window expires |
| Multiplier | `min(10, combo)` |
| Max multiplier | 10 |
| HUD combo | Visible when `run.combo > 0` |

Rules:

1. On catch:
   - if `run.time <= run.comboTimer`, set `run.combo += 1`.
   - else set `run.combo = 1`.
2. Set `run.comboTimer = run.time + comboWindow`.
3. Each fixed step, if `run.time > run.comboTimer`, set `run.combo = 0`.
4. Multiplier is `min(10, run.combo)`.
5. If combo reaches 2 through 10, play a rising combo bleep.
6. The combo counter displays `xN` where N is the multiplier.

### High Scores — Tier 2

| Rule | Number |
| --- | ---: |
| Max stored scores | 10 |
| Storage key | `frogBugHighScoresV1` |
| Entry fields | `score`, `difficulty`, `date` |
| Sort order | Descending score, then older date first |
| Save trigger | Game over |
| Display | High scores screen |

Rules:

1. On game over, create `{score: run.score, difficulty: run.difficulty, date: ISO string}`.
2. Insert into high scores.
3. Sort and keep top 10.
4. Persist to `localStorage` when available.
5. High scores screen lists rank, score, difficulty, date.
6. No player names are collected.

## 4.3 Progression and Difficulty

The run has no win condition. Difficulty increases over time to make survival eventually fail.

| Time in run | Edible spawn ramp | Hazard spawn ramp | Hazard max ramp |
| --- | --- | --- | --- |
| 0–29 s | Difficulty base | Difficulty base | Difficulty start |
| 30–59 s | Reduce edible interval by 0.05 s | Reduce hazard interval by 1.0 s | Normal +1 at 45 s, Hard +1 at 30 s, Easy +1 at 60 s |
| 60+ s | Continue ramp to floor | Continue ramp to floor | Continue ramp to cap |

Formulas:

```text
edibleInterval = max(edibleFloor, edibleBase - floor(time / 30) * 0.05)
hazardInterval = max(hazardFloor, hazardBase - floor(time / 30) * 1.0)
```

Target session lengths:

| Difficulty | Intended typical survival |
| --- | ---: |
| Easy | 4–8 minutes |
| Normal | 2–4 minutes |
| Hard | 1–3 minutes |

Progression is purely numeric: more hazards, faster hazard spawns, higher hazard caps. No new mechanics appear during a run.

## 4.4 Feel

The frog should feel responsive but not twitchy: instant velocity, no momentum, no knockback. The tongue should feel snappy: press, quick pink line, pop, particles. Catching should feel rewarding through sound, hit flash, and bug pop. Getting hit should feel funny rather than punishing: the frog flashes, hazards fly away, invulnerability blinks. The game stays readable because hazards are spiky and angry, while edible bugs are round and cute.

# 5. CHARACTERS

## 5.1 Frog

Silhouette: round body, wide mouth, big eyes, small legs. Top-down view shows body circle, eye bumps, and mouth direction.

Facing: `frog.facing` rotates the whole sprite.

States needed by gameplay:

| State | Meaning | Visual |
| --- | --- | --- |
| `idle` | No movement | Gentle bob |
| `moving` | Movement input | Body squash toward direction |
| `tongue` | Tongue active | Mouth stretched, tongue line |
| `invulnerable` | After damage | Blink unless reduced motion |
| `hit` | Short flash after damage | White/yellow outline |
| `dead` | Game over | Puffed body, X eyes |

Animations:

| Animation name | Motion rule |
| --- | --- |
| `idle_bob` | Vertical offset ±2 px, 2 Hz |
| `move_squash` | Scale x/y alternates 0.96/1.04 at 8 Hz while moving |
| `tongue_stretch` | Mouth widens while tongue active |
| `invuln_blink` | Sprite alpha toggles every 0.15 s |
| `hit_flash` | White outline for 0.25 s |
| `death_puff` | Scale to 1.25, then stop |

## 5.2 Edible Bugs

Silhouette: round, cute, small. No spikes. All edible bugs have simple eyes and tiny wings.

Facing: bug sprite faces its velocity direction.

States:

| State | Meaning | Visual |
| --- | --- | --- |
| `alive` | Normal | Type animation |
| `hit` | Caught | White flash |
| `dead` | Removed | Pop particles |

Animations:

| Type | Animation name | Motion rule |
| --- | --- | --- |
| Fly | `fly_hover` | Bob ±3 px, wing flap 12 Hz |
| Moth | `moth_flutter` | Sine path ±8 px, wing flap 6 Hz |
| Dragonfly | `dragonfly_dart` | Fast dart, brief pause, rotate to heading |
| All | `catch_pop` | Scale 1 → 1.35 → 0 over 0.12 s |

## 5.3 Hazard Bugs

Silhouette: spiky, angular, angry brows, stinger. Clearly different from edible bugs.

Facing: hazard sprite faces its velocity direction.

States:

| State | Meaning | Visual |
| --- | --- | --- |
| `alive` | Chasing | Angry wobble |
| `hit` | Damaged frog | White flash |
| `dead` | Removed after hit | Small purple/red pop |

Animations:

| Type | Animation name | Motion rule |
| --- | --- | --- |
| Angry Wasp | `wasp_chase` | Rotate toward frog, wobble ±4 px, wing flap 15 Hz |
| Hornet | `hornet_zigzag` | Rotate toward frog, perpendicular sine offset, wing flap 12 Hz |
| All | `hazard_pop` | Scale to 1.3 then remove over 0.10 s |

## 5.4 Tongue

Silhouette: pink capsule with dark outline.

States:

| State | Meaning | Visual |
| --- | --- | --- |
| `idle` | Inactive | Not drawn |
| `extending` | Moving out | Length grows |
| `holding` | Full reach | Full length |
| `retracting` | Returning | Length shrinks |
| `caught` | Bug caught | End and pop |

## 5.5 Effects

Particles:

| Event | Count | Size | Life | Colour |
| --- | ---: | ---: | ---: | --- |
| Catch | 8 | 3–7 px | 0.35 s | Bug colour |
| Hazard hit | 12 | 4–8 px | 0.45 s | `#FF5D8F` or `#7209B7` |

Hit flash:

| Event | Duration | Visual |
| --- | ---: | --- |
| Bug caught | 0.25 s | White/yellow circle outline |
| Frog damaged | 0.25 s | White/yellow circle outline |
| Reduced motion | 0.25 s | Static outline, no flash pulse |

# 6. AUDIO

| Name | Recipe | When it plays |
| --- | --- | --- |
| `music_theme` | 120 BPM chiptune loop: square lead arpeggio C4-G4-E4-G4-A4-G4-F4-E4, triangle bass C2-G2, square hats noise burst every eighth. Volume 0.25. | Title and gameplay. Stops on pause/game over. |
| `ui_confirm` | Square wave 660 Hz → 880 Hz, attack 0.01, decay 0.07. | Confirm/start/restart. |
| `ui_back` | Square wave 520 Hz → 392 Hz, decay 0.07. | Back/cancel. |
| `ui_pause` | Square wave 440 Hz → 330 Hz, decay 0.08. | Pause. |
| `ui_resume` | Square wave 330 Hz → 440 Hz, decay 0.08. | Resume. |
| `ui_highscore` | Triangle arpeggio 523, 659, 784 Hz, 0.18 s. | Open high scores. |
| `ui_start_run` | Square arpeggio 523, 659, 784, 1047 Hz, 0.25 s. | Run starts. |
| `tongue_shoot` | Sawtooth 880 Hz → 220 Hz, attack 0.005, decay 0.08, volume 0.28. | Tongue launches. |
| `tongue_miss` | Triangle 330 Hz → 110 Hz, decay 0.07, volume 0.15. | Tongue ends without catch. |
| `catch_fly` | Square blips 660, 880, 1320 Hz, 0.12 s, volume 0.35. | Fly caught. |
| `catch_moth` | Square blips 520, 780, 1040 Hz, 0.14 s, volume 0.35. | Moth caught. |
| `catch_dragonfly` | Square blips 780, 980, 1560, 1960 Hz, 0.10 s, volume 0.38. | Dragonfly caught. |
| `hit_wasp` | Sawtooth 220 Hz → 110 Hz plus noise burst, 0.25 s. | Hazard damages frog. |
| `life_lost` | Square 440 Hz → 80 Hz, 0.55 s, volume 0.35. | Life reduced. |
| `combo_2` | Square 440 Hz, 0.05 s. | Combo reaches 2. |
| `combo_3` | Square 523 Hz, 0.05 s. | Combo reaches 3. |
| `combo_4` | Square 587 Hz, 0.05 s. | Combo reaches 4. |
| `combo_5` | Square 659 Hz, 0.05 s. | Combo reaches 5. |
| `combo_6` | Square 784 Hz, 0.05 s. | Combo reaches 6. |
| `combo_7` | Square 880 Hz, 0.05 s. | Combo reaches 7. |
| `combo_8` | Square 988 Hz, 0.05 s. | Combo reaches 8. |
| `combo_9` | Square 1047 Hz, 0.05 s. | Combo reaches 9. |
| `combo_10` | Square 1319 Hz, 0.08 s. | Combo reaches 10. |
| `game_over` | Square descending 392, 330, 262, 196 Hz, 0.8 s. | Lives reach 0. |
| `spawn_bug` | Triangle 880 Hz → 440 Hz, 0.05 s, volume 0.12. | Bug spawns. |

# 7. UX

## 7.1 Screens

Screens are DOM elements. The game canvas sits behind them. Only one screen is visible at a time.

| Screen | DOM id | Visible when | Purpose |
| --- | --- | --- | --- |
| Title | `#screen-title` | `ui.screen === "title"` | Start, difficulty, remap, reduced motion |
| Pause | `#screen-pause` | `ui.screen === "pause"` | Resume, restart, high scores, options |
| Game Over | `#screen-gameover` | `ui.screen === "gameOver"` | Score, high scores, restart, title |
| High Scores | `#screen-highscores` | `ui.screen === "highScores"` | Top 10 scores, back |

No additional screens exist. Remap and difficulty controls are embedded inside title/pause.

## 7.2 State machine

| Current | Event | Next | Action |
| --- | --- | --- | --- |
| `title` | Confirm/start | `playing` | Start run, start music |
| `title` | Open high scores | `highScores` | `previousScreen = title` |
| `title` | Remap | `title` | Enter key capture mode |
| `title` | Toggle reduced motion | `title` | Save setting |
| `title` | Select difficulty | `title` | Save setting |
| `playing` | Pause key | `pause` | Stop music, show pause |
| `playing` | Lives 0 | `gameOver` | Save high score, stop music |
| `pause` | Resume | `playing` | Start music |
| `pause` | Restart | `playing` | New run |
| `pause` | Title | `title` | Stop run |
| `pause` | High scores | `highScores` | `previousScreen = pause` |
| `gameOver` | Restart | `playing` | New run |
| `gameOver` | Title | `title` | Stop run |
| `gameOver` | High scores | `highScores` | `previousScreen = gameOver` |
| `highScores` | Back | `previousScreen` | Restore previous screen |

## 7.3 HUD

| Element | Record field | When visible |
| --- | --- | --- |
| Health hearts | `run.lives`, `run.maxLives` | `run.phase === "playing"` or `run.phase === "paused"` |
| Score | `run.score` | `run.phase === "playing"`, `run.phase === "paused"`, and game over screen |
| Combo counter | `run.combo` | `run.phase === "playing"` and `run.combo > 0` |

HUD DOM structure:

```html
<div id="hud" aria-live="polite">
  <div id="hud-health"></div>
  <div id="hud-score">0</div>
  <div id="hud-combo" hidden>x0</div>
</div>
```

HUD behaviour:

1. Health renders one heart per remaining life.
2. Score renders integer with no leading zeros.
3. Combo renders `xN` only when `run.combo > 0`.
4. HUD uses hand-lettered font and high-contrast colours.
5. Reduced motion disables HUD pulse animations.

## 7.4 Typography

```css
:root {
  --font-hand: "Comic Sans MS", "Chalkboard SE", "Comic Neue", "Segoe Print", cursive;
}

body {
  font-family: var(--font-hand);
}

#hud-score {
  font-size: 28px;
  color: #ffffff;
  text-shadow: 3px 3px 0 #101820;
}

#screen-title h1 {
  font-size: 64px;
  color: #FFD60A;
  text-shadow: 4px 4px 0 #101820;
}
```

# 8. DEBUG API

| Function | Contract |
| --- | --- |
| `debug.setSeed(n)` | Sets RNG seed. |
| `debug.runFixedSteps(n)` | Advances simulation exactly n fixed steps. |
| `debug.input.press(action)` | Sets a mapped action key pressed. |
| `debug.input.release(action)` | Sets a mapped action key released. |
| `debug.input.setPointer(x, y)` | Sets pointer position and `pointerActive = true`. |
| `debug.input.clearPointer()` | Sets `pointerActive = false`. |
| `debug.input.click()` | Simulates pointer catch input. |
| `debug.frog.setPos(x, y)` | Sets frog position. |
| `debug.frog.setFacing(angle)` | Sets frog facing. |
| `debug.frog.setLives(n)` | Sets lives. |
| `debug.tongue.fire()` | Attempts to fire tongue. |
| `debug.tongue.setActive(active)` | Forces tongue active/inactive. |
| `debug.bugs.spawn(type, x, y)` | Spawns edible bug. |
| `debug.bugs.clear()` | Removes all edible bugs. |
| `debug.hazards.spawn(type, x, y)` | Spawns hazard bug. |
| `debug.hazards.clear()` | Removes all hazard bugs. |
| `debug.combat.damageFrog()` | Applies damage once. |
| `debug.combat.setInvuln(seconds)` | Sets invulnerability timer. |
| `debug.scoring.addScore(n)` | Adds score. |
| `debug.combo.set(n)` | Sets combo count. |
| `debug.combo.tick(seconds)` | Advances combo timer logic. |
| `debug.highScores.load()` | Loads high scores. |
| `debug.highScores.saveRun()` | Saves current run as high score. |
| `debug.highScores.clear()` | Clears stored high scores. |
| `debug.settings.setDifficulty(name)` | Sets difficulty setting. |
| `debug.settings.setReducedMotion(bool)` | Sets reduced motion. |
| `debug.settings.setKeyMap(map)` | Applies remap. |
| `debug.ui.showScreen(name)` | Shows a screen. |

# 9. TESTS

## Tier 1 Tests

| Test | Validation |
| --- | --- |
| `test_fixed_timestep` | With dt accumulation, simulation updates exactly `floor(totalDt / FIXED_DT)` times. |
| `test_default_input_maps` | Default WASD/arrows move frog and Space fires tongue. |
| `test_remappable_keys` | Remapping `catch` to `KeyE` causes `KeyE` to fire tongue. |
| `test_movement_speed` | Frog cannot move more than 165 px in one second. |
| `test_bounds_clamp` | Frog cannot leave arena bounds. |
| `test_tongue_cooldown` | Second catch input before 0.26 s does not create another tongue. |
| `test_tongue_catches_fly` | Placing a fly on tongue path removes it and spawns particles/hit flash. |
| `test_tongue_does_not_catch_hazard` | Wasp on tongue path remains alive and frog is not damaged by tongue. |
| `test_hazard_damage` | Overlapping hazard reduces lives once, removes hazard, starts invuln. |
| `test_invulnerability` | Second hazard collision during invuln does not reduce lives. |
| `test_game_over` | Setting lives to 0 shows game over and stops simulation. |
| `test_spawn_caps` | Edible bugs never exceed 14; hazards never exceed difficulty cap. |
| `test_difficulty_easy` | Easy starts with 5 lives and reduced hazard max. |
| `test_difficulty_hard` | Hard starts with 2 lives and increased hazard cap. |
| `test_pause_stops_time` | While paused, `run.time` does not advance. |
| `test_reduced_motion` | Reduced motion disables particle spawning and blinking. |
| `test_colourblind_safety` | Hazards have spiky shape data and edible bugs round shape data; no red/green-only state. |
| `test_audio_calls` | Catch, shoot, hit, game over call expected `playSound` names. |
| `test_screen_state_machine` | Title → playing → pause → resume → game over transitions work. |

## Tier 2 Tests

| Test | Validation |
| --- | --- |
| `test_score_fly` | Catching fly adds 10 × current multiplier. |
| `test_score_moth` | Catching moth adds 15 × current multiplier. |
| `test_score_dragonfly` | Catching dragonfly adds 25 × current multiplier. |
| `test_combo_increment` | Two catches within window set combo to 2. |
| `test_combo_reset` | Waiting past combo window sets combo to 0. |
| `test_combo_multiplier_cap` | Combo above 10 caps multiplier at 10. |
| `test_score_updates_hud` | `run.score` updates `#hud-score`. |
| `test_combo_updates_hud` | `run.combo > 0` updates `#hud-combo`. |
| `test_highscore_save` | Game over saves score, difficulty, date. |
| `test_highscore_sort` | High scores are sorted descending by score. |
| `test_highscore_limit` | More than 10 scores are trimmed to top 10. |
| `test_highscore_screen` | High scores screen lists saved entries. |

# 10. BUILD ORDER

1. Create HTML shell, canvas, DOM screens, HUD elements, CSS layout.
2. Create global context, settings defaults, fixed-step loop.
3. Implement RNG and seeded tests.
4. Implement input mapping and remapping.
5. Draw flat arena, frog, placeholder tongue.
6. Implement frog movement and bounds.
7. Implement tongue launch, state, cooldown, aim.
8. Create edible bug records and draw them.
9. Implement bug wandering and spawn caps.
10. Implement tongue catch collision and effects.
11. Create hazard bugs and draw them.
12. Implement lives, damage, invulnerability, game over.
13. Implement title/pause/game-over/high-score screen shells.
14. Add chiptune music and all core sound effects.
15. Add accessibility: reduced motion, remapping, difficulty options.
16. Validate Tier 1 tests.
17. Add score values and HUD score.
18. Add combo timer, multiplier, combo HUD.
19. Add high-score persistence and list.
20. Validate Tier 2 tests.

# 11. DEFINITION OF DONE

## Tier 1 Definition of Done

A minimal playable core catching game exists.

- [ ] Game loads with fixed 960×540 arena.
- [ ] Simulation runs at 60 fixed steps per second.
- [ ] Title screen starts a run.
- [ ] Pause and resume stop and resume simulation.
- [ ] Game over screen appears when lives reach 0.
- [ ] High scores screen exists and can be opened, even if empty.
- [ ] Frog moves with WASD/arrows and is clamped to arena.
- [ ] Frog can fire tongue with Space/J/pointer/touch.
- [ ] Tongue has 170 px reach and 0.26 s cooldown.
- [ ] Edible bugs spawn and move.
- [ ] Tongue catches edible bugs and removes them.
- [ ] Hazard bugs spawn, chase, and damage the frog.
- [ ] Damage removes one life and starts 1.5 s invulnerability.
- [ ] Lives and failure work.
- [ ] HUD health updates.
- [ ] Flat vector art is present.
- [ ] Saturated colour-blind safe palette is used.
- [ ] Particles and hit flash occur.
- [ ] Chiptune music and retro bleeps play.
- [ ] Reduced motion reduces effects.
- [ ] Keys are remappable.
- [ ] Easy/Normal/Hard difficulty options work.
- [ ] Tier 1 tests pass.

## Tier 2 Definition of Done

Scoring and high scores are complete.

- [ ] Catching bugs adds score.
- [ ] Base scores match §4.2.
- [ ] Combo increments within window.
- [ ] Combo resets after window.
- [ ] Multiplier caps at 10.
- [ ] HUD score updates.
- [ ] HUD combo updates only when combo is active.
- [ ] Game over shows final score.
- [ ] High scores save on game over.
- [ ] High scores sort descending and keep top 10.
- [ ] High scores screen displays saved scores.
- [ ] Tier 2 tests pass.

## Tier 3 Definition of Done

Not applicable. No extra mechanics are allowed.

# A. SANITY

| Check | Result |
| --- | --- |
| Does the spec preserve the prompt “frogs eating bugs”? | Yes. Player is a frog; core verb is catching bugs. |
| Are all high-level decisions included? | Yes, mapped in §0.1 and §0.2. |
| Are core mechanics Tier 1? | Yes: movement, tongue, catching, bugs, failure. |
| Are supporting mechanics Tier 2? | Yes: scoring, combo, high scores. |
| Are extra mechanics absent? | Yes: no traps, no pickups, no powerups, no upgrades. |
| Are screens exactly title, pause, game over, high scores? | Yes. Remap and options are embedded, not separate screens. |
| Are HUD elements exactly health, score, combo counter? | Yes. |
| Are effects exactly particles and hit flash? | Yes. No screen shake or trails. |
| Is accessibility included? | Yes: colour-blind safe palette, reduced motion, remappable keys, difficulty options. |
| Are numbers concrete? | Yes: speeds, sizes, timers, spawn caps, scores, combo windows, difficulty tables. |
| Is the game one screen? | Yes: 960×540 fixed arena. |
| Is the session endless? | Yes: no win condition, ends only when lives reach 0. |
| Is failure “lose a life” not instant death? | Yes: lives, invulnerability, game over at 0. |
| Is art flat vector? | Yes: solid fills, crisp outlines, no gradients. |
| Is palette saturated but colour-blind safe? | Yes: bright colours plus shape-based hazard distinction. |
| Is audio chiptune/retro bleeps? | Yes: synthesized oscillator recipes. |
| Are tests tied to tiers? | Yes: Tier 1 core tests, Tier 2 scoring/high-score tests. |
| Are debug functions sufficient? | Yes: one per gameplay system plus input functions. |
| Are contracts sufficient for builder? | Yes: module layout, global context fields, function names. |
| Any contradictions found? | None after final pass. |