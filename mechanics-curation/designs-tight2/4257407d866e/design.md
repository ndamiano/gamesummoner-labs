# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Game prompt: a tower defense game where cats defend a fish market | §4.2 Building, §4.3 Economy, §4.4 Waves, §5 Characters, §3 Visual Spec |
| Dimension: 2d | §1.1 Units, §2 Contracts, §3 Visual Spec, §4 Gameplay Spec |
| Camera: top-down | §1.1 Units, §3 Visual Spec, §4.4 Waves |
| Time model: real-time | §1.2 Important conventions, §2.3 Module specifics, §4.4 Waves |
| Movement model: no movement, cursor only | §0.2 Decisions, §1.2 Important conventions, §7 UX, §8 Debug API |
| Session shape: a sequence of levels | §4.4 Waves, §4.7 Progression and difficulty, §7 UX |
| Failure: restart the level | §4.4 Waves, §4.7 Progression, §7 UX, §11 Definition of Done |
| Tone: silly | §4.7 Feel, §5 Characters, §6 Audio, §3 Visual Spec |
| Size: a handful of levels, under 30 minutes | §4.4 Waves, §4.7 Progression, §11 Definition of Done |
| Win/lose: defeat a final boss | §4.4 Waves, §4.7 Progression, §7 UX |
| Core mechanic: combat | §4.1 Combat |
| Core mechanic: building | §4.2 Building |
| Core mechanic: economy | §4.3 Economy |
| Core mechanic: waves | §4.4 Waves |
| Supporting mechanic: abilities | §4.5 Abilities |
| Extra mechanic: scoring | §4.6 Scoring |
| Art style: flat vector: clean flat shapes, solid colours, crisp edges | §3 Visual Spec, §5 Characters |
| Palette: saturated: bright, strong colours | §3 Visual Spec |
| Typography: clean sans: plain modern letters | §7 UX |
| Music: chiptune: retro console bleeps | §6 Audio |
| Sound effects style: retro bleeps: synthesized chip sounds | §6 Audio |
| Screens: title, pause, settings, game over, win, level select, high scores | §7 UX |
| HUD: health, score, wave number, currency | §7 UX |
| Effects: particles, hit flash | §3 Visual Spec, §4.1 Combat, §6 Audio, §11 Definition of Done |
| Accessibility: colour-blind safe palette, reduced motion, difficulty options | §3 Visual Spec, §4.7 Progression and difficulty, §7 UX, §9 Tests, §11 Definition of Done |

## 0.2 Decisions

| Category | Decision | Why |
| --- | --- | --- |
| Final prompt | Cats defend a fish market from fish thieves. | Keeps the requested premise direct and silly. |
| Player role | The player is the invisible market manager cat. The cursor is the manager’s paw. | “No movement, cursor only” is satisfied while preserving agency. |
| Dimension | 2D canvas game with fixed virtual resolution 960×540. | Simple, browser-friendly, top-down tower defense. |
| Camera | Fixed top-down camera per level. No camera movement, zoom, or rotation. | Required decision; keeps input cursor-only and avoids movement. |
| Time model | Real-time with fixed 60 Hz simulation step. | Deterministic gameplay, easier tests, still feels live. |
| Movement model | No player-controlled movement. Enemies move along fixed paths. Player input is pointer only. | Preserves “no movement” for the player while allowing tower-defense waves. |
| Input | Pointer only: hover, left click, right click cancel. No keyboard required. | Required decision. |
| Session shape | Five sequential levels. Level select unlocks next level after win. | “Handful” and sequence of levels. |
| Failure | If base HP reaches 0, show Game Over. Restart the same level. | Required decision. |
| Win | Level 5 final boss must be killed. Killing boss and clearing wave shows Win. | Required decision. |
| Tone | Market cats, fish thieves, yarn traps, fish coins, silly names and bleeps. | Requested silly tone. |
| Size | Five levels with total par time 26:30. | Under 30 minutes. |
| Core combat | Towers automatically attack enemies. Enemies damage the market base. One side loses when HP reaches 0. | Concrete combat system. |
| Core building | Place cat towers and yarn traps on allowed cells. Upgrade or sell cat towers. | Concrete building system. |
| Core economy | Earn Fish from kills and wave clears. Spend Fish on towers, upgrades, traps. | Concrete economy system. |
| Core waves | Fixed wave tables. Waves start automatically after delay and are harder than previous waves. | Required wave system. |
| Supporting abilities | Three pointer-targeted abilities with cooldowns: Catnip Frenzy, Fish Freeze, Net Drop. | Concrete abilities system. |
| Extra scoring | Level score from kills, wave clears, leftover HP, leftover Fish. Top 5 per level stored locally. | Concrete scoring system. |
| Art style | Procedural flat vector shapes with solid fills and crisp outlines. No bitmap assets. | Required art style. |
| Palette | Saturated, color-blind-safe palette using blue, orange, yellow, purple, cyan, gray, plus shape patterns. | Required palette and accessibility. |
| Typography | System clean sans font stack. | Required typography without external assets. |
| Music | Synthesized chiptune loops using Web Audio oscillators. | Required music style. |
| Sound effects | Synthesized retro bleeps using oscillators/noise. | Required SFX style. |
| Screens | Title, level select, gameplay, pause, settings, game over, win, high scores. | Required screens. |
| HUD | HTML/CSS overlay with health, score, wave, currency, build palette, ability buttons. | Required HUD. |
| Effects | Particles and hit flash. Reduced motion can reduce particles. | Required effects and accessibility. |
| Accessibility | Safe palette from Tier 1. Difficulty and reduced-motion options added in Tier 4. | Required accessibility. |
| Level count | Exactly 5 levels. | “Handful” and final boss sequence. |
| Level names | 1 Market Open, 2 Fish Flies, 3 Raccoon Racket, 4 Crab Caper, 5 Gull King. | Progression and silly tone. |
| Enemy roster | Rat, Seagull, Raccoon, Crab, Gull King. | Concrete enemies. |
| Buildable roster | Alley Cat, Fishmonger Cat, Laser Pointer Cat, Yarn Trap. | Concrete traps/towers under Building. |
| Pickups | Fish Coin, Wave Bonus Coin, Boss Tuna Coin. Auto-collected visual/economy feedback. | Concrete pickups without adding a separate system. |
| Ability roster | Catnip Frenzy, Fish Freeze, Net Drop. | Concrete abilities. |
| Scoring values | Enemy score values, wave clear points, HP points, Fish points, difficulty multiplier. | Concrete scoring. |
| Difficulty options | Easy, Normal, Hard multipliers. | Required accessibility. |
| Reduced motion | Disables particles, shortens/softens flashes, disables banner motion. | Required accessibility. |
| Color-blind strategy | Distinct shapes and patterns, not color alone. | Required accessibility. |
| Grid | 32×18 cell grid, 30 px cells. | Simple placement and tests. |
| Path model | Polyline waypoints. Path cells are cells whose centers are within 15 px of a segment. | Deterministic maps and enemy movement. |
| Buildable cells | Non-path cells within 150 px of path, not occupied. | Prevents dead placement while keeping maps simple. |
| Trap cells | Path cells not within 45 px of spawn or base. | Keeps traps useful but not instant-win. |
| Targeting | Towers always target the enemy furthest along the path within range. | Removes extra UI and keeps system simple. |
| Projectiles | Alley Cat and Fishmonger Cat use homing projectiles. Laser Pointer Cat is hitscan. | Concrete combat rules. |
| Armor | Damage reduced by armor, minimum 1. Laser L3 ignores armor. | Concrete combat depth. |
| Status effects | Slow, freeze, stun, buffs. Strongest slow wins. | Concrete status rules. |
| Economy | Kill rewards immediate. Wave bonus on clear. Sell refund 70%. | Concrete economy rules. |
| Wave starts | Automatic. No early-call button. | Keeps scope small. |
| Progress storage | Local storage for unlocked levels, settings, high scores. | Needed for sequence and high scores. |
| RNG | Deterministic mulberry32 for particles only. Gameplay spawns are table-driven. | Testability. |
| Tiering | Tier 1 core game, Tier 2 abilities, Tier 3 scoring/high scores, Tier 4 accessibility options. | Required tiering. |
| Tier 1 score | Score HUD element exists but remains 0 until Tier 3 scoring rules. | HUD requirement without making scoring a core dependency. |
| Tier 1 difficulty | Normal only. Difficulty options are Tier 4. | Keeps Tier 1 focused on core mechanics. |
| Tier 1 reduced motion | Effects enabled. Reduced-motion toggle is Tier 4. | Keeps Tier 1 focused on core mechanics. |
| Module style | Vanilla ES modules, no external assets, no frameworks. | Browser game, agent-buildable. |
| UI style | HTML/CSS screens and HUD; canvas only for game world. | Required UX constraint. |
| Custom cursor | Canvas-drawn paw cursor inside game area. | Cursor-only input and theme. |
| Sound toggle | Sound on/off button. No sliders. | Cursor-only settings. |
| Difficulty selection | Three buttons. No sliders. | Cursor-only settings. |
| High scores | Top 5 per level with score, difficulty, date. No player names. | Cursor-only, no extra input. |
| Replay | Completed levels can be replayed. Best scores keep maximum. | Level select requirement. |
| Fail scoring | Failed attempts do not save high scores. | Clean scoring. |
| Win scoring | Win saves level score. | Clean scoring. |

## 0.3 Tiers

| Tier | Priority | Goal | Systems included | Notes |
| --- | --- | --- | --- | --- |
| 1 | Required | Minimal playable game that can be finished. | Combat, Building, Economy, Waves, Level sequence, required screens except high scores, HUD, art, audio, particles, hit flash, safe palette. | Normal difficulty only. Score HUD exists but stays 0. Traps and pickups are Tier 1 content under Building/Economy. |
| 2 | High | Add special powers. | Abilities, ability HUD, ability cooldowns, ability unlock progression. | Not a dependency of Tier 1. |
| 3 | High | Add scoring and records. | Scoring rules, score HUD updates, high scores screen, local high-score storage, level-select best score display. | Not a dependency of Tier 1 or 2. |
| 4 | High | Add accessibility options. | Difficulty options, reduced motion, enhanced pattern settings, settings polish. | Safe palette is already Tier 1. |
| 5 | Polish | Optional stabilization. | Performance tuning, layout polish, balance tweaks. | Not required for done. |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Concept | Value | Notes |
| --- | --- | --- |
| Virtual canvas width | 960 px | All game logic uses this coordinate space. |
| Virtual canvas height | 540 px | Top-down play area. |
| Origin | Top-left `(0,0)` | `x` right, `y` down. |
| Grid | 32 columns × 18 rows | Full canvas grid. |
| Cell size | 30 px | Cell centers are `15 + 30*col`, `15 + 30*row`. |
| Simulation step | `1/60` s | Fixed update. Render may interpolate. |
| Frame rate | 60 Hz logic | Render at browser rAF. |
| Time | Seconds as float | All timers, cooldowns, durations use seconds. |
| Distance | Pixels | Ranges, path lengths, projectile distances. |
| Speed | Pixels per second | Enemy and projectile speeds. |
| HP | Integer | Base and enemy HP. |
| Damage | Integer | Tower and ability damage. |
| Currency | Fish, integer | Displayed in HUD. |
| Score | Integer | Tier 1 stays 0; Tier 3 fills it. |
| Rotation | Radians | Tower aiming and enemy facing. |
| Radius | Pixels | Enemy, projectile, splash, ability radii. |
| Fire rate | Shots per second | Tower rate. |
| Cooldown | Seconds | Ability cooldown. |

## 1.2 Important conventions

1. The game is a single HTML page with vanilla ES modules. No frameworks, external fonts, or external images/audio.
2. The game world is drawn on a `<canvas>`. Screens and HUD are HTML/CSS overlays only.
3. The simulation is fixed-step. `update(dt = 1/60)` is the only place gameplay state changes.
4. Render is read-only. Render must not mutate gameplay state.
5. Input is pointer-only. Pointer coordinates are converted from DOM client coordinates to virtual canvas coordinates.
6. No keyboard input is required for any game action.
7. Right click cancels the current build or ability selection.
8. All gameplay spawns are deterministic from wave tables. Randomness is only for particles and is seeded.
9. RNG uses mulberry32. Seed: `levelId * 10000 + difficultyIndex * 100 + attempt`.
10. Entity IDs are incrementing integers starting at 1 for each level attempt.
11. All timers count down. A timer at `<= 0` means expired.
12. Pausing stops simulation but preserves state.
13. Restarting a level resets all gameplay state but preserves settings and progress.
14. All critical states must be identifiable by shape or pattern, not color alone.
15. All numbers in this spec are final unless explicitly marked as placeholder.
16. The score record exists in Tier 1 for HUD compatibility, but scoring rules are Tier 3.
17. Abilities are never required to complete Tier 1.
18. High scores are never required to complete Tier 1.
19. Difficulty options are never required to complete Tier 1; Tier 1 always uses Normal.
20. Reduced motion is never required to complete Tier 1; Tier 1 uses normal effects.

# 2. CONTRACTS

## 2.1 Module layout

```text
index.html
styles.css
main.js

core/config.js
core/state.js
core/loop.js
core/input.js
core/rng.js

systems/combat.js
systems/building.js
systems/economy.js
systems/waves.js
systems/abilities.js
systems/scoring.js

render/renderer.js
render/palette.js
render/effects.js

audio/audio.js

ui/screens.js
ui/hud.js
ui/stateMachine.js

data/levels.js
data/enemies.js
data/towers.js
data/traps.js
data/abilities.js
data/scoring.js

debug/debug.js
```

## 2.2 Global context

| Field | Type | Required contents |
| --- | --- | --- |
| `ctx.version` | string | `"catfish-market-v1"`. |
| `ctx.mode` | enum | `title`, `levelSelect`, `playing`, `paused`, `settings`, `gameOver`, `win`, `highScores`. |
| `ctx.settings` | object | `soundEnabled`, `difficulty`, `reducedMotion`. |
| `ctx.progress` | object | `unlockedLevel`, `completedLevel`, `highScores`. |
| `ctx.level` | object | Current level state: `id`, `name`, `path`, `baseCell`, `spawnCell`, `waveIndex`, `totalWaves`, `waveActive`, `spawnQueue`, `nextWaveTimer`, `completed`, `parTime`. |
| `ctx.base` | object | `hp`, `maxHp`, `x`, `y`, `radius`, `flashTimer`. |
| `ctx.economy` | object | `fish`, `totalEarned`, `totalSpent`. |
| `ctx.score` | object | `current`, `kills`, `waveClears`, `levelScore`, `lastReason`. |
| `ctx.entities` | object | Arrays: `towers`, `traps`, `enemies`, `projectiles`, `beams`, `particles`, `pickups`. |
| `ctx.abilities` | object | `unlocked`, `selected`, `cooldowns`, `activeAreas`, `buffs`. |
| `ctx.input` | object | `pointer`, `leftClick`, `rightClick`, `hover`, `buildSelected`, `abilitySelected`, `selectedEntity`. |
| `ctx.ui` | object | `banner`, `messageQueue`, `paletteState`, `selectedPanel`, `screens`. |
| `ctx.rng` | object | `seed`, `state`, `nextFloat()`, `nextInt(min,max)`. |
| `ctx.time` | object | `elapsed`, `step`, `lastStep`, `paused`. |
| `ctx.debug` | object | Debug API functions. |
| `ctx.audio` | object | Audio handle and mute state. |

## 2.3 Module specifics

| Module | Required exports/functions | Called by | Purpose |
| --- | --- | --- | --- |
| `core/config.js` | `CONFIG`, `DIFFICULTY_MULTIPLIERS`, `LEVEL_IDS` | All modules | Final numeric constants. |
| `core/state.js` | `createContext()`, `resetLevel(ctx, levelId)`, `setState(ctx, mode)` | `main.js`, systems | Owns global context. |
| `core/loop.js` | `startLoop()`, `stopLoop()`, `tick(dt)`, `pause()`, `resume()` | `main.js`, UI | Fixed-step loop. |
| `core/input.js` | `initInput()`, `getPointer()`, `leftClick()`, `rightClick()`, `clearClick()` | UI, systems | Pointer-only input. |
| `core/rng.js` | `mulberry32(seed)`, `randomParticle(seed)` | Effects | Deterministic particles. |
| `systems/combat.js` | `updateCombat(dt)`, `spawnEnemy(ctx, type, startProgress)`, `damageEnemy(ctx, enemyId, rawDamage, ignoreArmor)`, `damageBase(ctx, amount)`, `applyStatus(ctx, enemyId, status)`, `getEnemiesInRange(ctx, x, y, radius)` | Building, Waves, Abilities, Tests | Combat rules. |
| `systems/building.js` | `updateBuilding(dt)`, `canPlace(ctx, cell, type)`, `place(ctx, cell, type)`, `upgrade(ctx, entityId)`, `sell(ctx, entityId)`, `triggerTrap(ctx, trapId)`, `getSelectedEntity(ctx)` | Input, UI, Tests | Building rules. |
| `systems/economy.js` | `updateEconomy(dt)`, `addFish(ctx, amount, reason)`, `spendFish(ctx, amount, reason)`, `refund(ctx, amount, reason)`, `getFish(ctx)` | Building, Waves, Combat, Tests | Economy rules. |
| `systems/waves.js` | `updateWaves(dt)`, `startWave(ctx, waveIndex)`, `getWaveTable(levelId)`, `isWaveComplete(ctx)`, `completeLevel(ctx)`, `failLevel(ctx)` | Loop, Tests | Wave sequencing. |
| `systems/abilities.js` | `updateAbilities(dt)`, `selectAbility(ctx, abilityId)`, `triggerAbility(ctx, abilityId, x, y)`, `getCooldown(ctx, abilityId)`, `unlockAbility(ctx, abilityId)` | Input, UI, Tests | Ability rules. |
| `systems/scoring.js` | `updateScore(ctx)`, `addKillScore(ctx, enemyType)`, `addWaveScore(ctx, waveIndex)`, `finishLevelScore(ctx)`, `saveHighScore(ctx)`, `getHighScores(ctx, levelId)` | Combat, Waves, UI, Tests | Scoring rules. |
| `render/renderer.js` | `render(ctx)` | Loop | Draws world. |
| `render/palette.js` | `COLORS`, `PATTERNS`, `shapeFor(type)` | Renderer | Flat vector palette. |
| `render/effects.js` | `hitFlash(ctx, entity)`, `spawnParticles(ctx, kind, x, y)`, `updateEffects(dt)` | Combat, Building, Abilities | Particles and flashes. |
| `audio/audio.js` | `initAudio()`, `play(name)`, `playMusic(name)`, `stopMusic()`, `setMuted(boolean)` | Systems, UI | Synthesized audio. |
| `ui/screens.js` | `showScreen(name)`, `hideScreens()`, `bindScreenEvents()` | State machine | HTML screens. |
| `ui/hud.js` | `updateHUD(ctx)`, `showBanner(text, duration)` | Loop | HUD updates. |
| `ui/stateMachine.js` | `transition(from, to)`, `allowedTransitions` | Screens, game | Screen state machine. |
| `data/levels.js` | `LEVELS` | Waves, Renderer | Level and path data. |
| `data/enemies.js` | `ENEMIES` | Combat, Waves | Enemy stats. |
| `data/towers.js` | `TOWERS` | Building, Combat | Tower stats. |
| `data/traps.js` | `TRAPS` | Building | Trap stats. |
| `data/abilities.js` | `ABILITIES` | Abilities, UI | Ability stats. |
| `data/scoring.js` | `SCORE_RULES` | Scoring | Score values. |
| `debug/debug.js` | All functions in §8 | Tests, console | Direct system access. |

# 3. VISUAL SPEC

The game is a bright, silly, flat-vector fish market seen from directly above. The market floor is dark navy, path aisles are lighter blue-gray, and every interactive object is a crisp geometric shape with a strong outline. Cat defenders are white cat silhouettes with colored workwear: cyan collar for Alley Cat, orange apron for Fishmonger Cat, magenta collar for Laser Pointer Cat. Enemies are bold animal shapes: rats are gray wedges, gulls are yellow winged diamonds, raccoons are purple masked circles, crabs are blue wide bodies, and the Gull King is a large orange crown shape. The market base is a yellow fish stall. Currency is a gold fish coin. Everything uses solid fills, 2 px outlines, and no gradients.

Lighting and atmosphere are flat and daytime-market bright: no dynamic light, no shadows except tiny dark outlines, no fog. The atmosphere is busy and cartoonish, not realistic. The space is a fixed 960×540 top-down market. The path is a visible walkway made of dashed tiles. Build cells are shown as crate outlines with paw marks. Trap cells show yarn dashes. The base is always at the right side. The HUD is a clean sans HTML strip around the canvas.

| Element | Shape recipe | Fill hex | Outline hex | Pattern | Motion |
| --- | --- | --- | --- | --- | --- |
| Background | Full rect | `#0B1220` | none | none | none |
| Market floor | Rect | `#142033` | `#0B1220` | subtle crate lines | none |
| Path | Thick polyline | `#1F2A44` | `#355075` | dashed center line | none |
| Spawn marker | Arrow into market | `#FB8B24` | `#FFD23F` | chevrons | pulse 1 Hz |
| Base stall | Rounded stall + fish | `#FFB703` | `#003049` | fish icon | idle bob 0.5 Hz |
| Base health bar | Rect | `#00A8E8` | `#FFFFFF` | diagonal stripes when low | none |
| Build cell | Crate outline + paw | `#24344F` | `#4CC9F0` | paw mark | hover outline brightens |
| Trap cell | Path tile with yarn | `#1F2A44` | `#B5179E` | yarn dashes | rotate 0.2 Hz |
| Alley Cat | Cat head + cyan collar | `#F8F9FA` | `#003049` | cyan triangle marker | tail wag 2 Hz |
| Fishmonger Cat | Cat head + orange apron | `#F8F9FA` | `#003049` | orange square marker | idle bob 1 Hz |
| Laser Pointer Cat | Cat head + magenta collar | `#F8F9FA` | `#003049` | magenta diamond marker | scan eye 0.8 Hz |
| Yarn Trap | Yarn ball | `#B5179E` | `#FFFFFF` | yarn swirl | rotate 0.5 Hz |
| Fish Coin | Fish shape | `#FFD23F` | `#003049` | eye dot | fly to HUD |
| Rat | Wedge body + tail | `#8D99AE` | `#003049` | gray pattern | walk bob |
| Seagull | Diamond + wings | `#FFD23F` | `#003049` | wing stripes | wing flap |
| Raccoon | Circle + mask | `#B5179E` | `#003049` | mask pattern | tail sway |
| Crab | Wide body + claws | `#00A8E8` | `#003049` | shell ridges | side scuttle |
| Gull King | Large gull + crown | `#FB8B24` | `#003049` | crown pattern | slow flap |
| Projectile | Small circle | `#FFFFFF` | `#003049` | none | trail |
| Laser beam | Line | `#B5179E` | `#FFFFFF` | none | fade 0.12 s |
| Hit flash | Outline only | transparent | `#FFFFFF` | none | 80 ms |
| Death particle | Circles + fish bits | mixed | `#003049` | none | 0.4 s |
| Ability area | Ring | transparent | `#4CC9F0` | ability icon | expand 0.25 s |
| Cursor | Paw | `#FFD23F` | `#003049` | paw | follows pointer |

# 4. GAMEPLAY SPEC

The player is the head cat of a fish market. The player does not move. The player uses a cursor to place cat defenders and yarn traps, upgrade or sell cat defenders, and use special abilities. Fish thieves enter through market aisles and walk toward the fish stall. If they reach the stall, they damage it. The player earns Fish from kills and wave clears, spends Fish on defenses, survives wave sequences, and wins by defeating the Gull King in Level 5.

## 4.0 Records and rosters

| Record | Required fields | Roster source |
| --- | --- | --- |
| `EnemyRecord` | `id`, `type`, `hp`, `maxHp`, `armor`, `speed`, `reward`, `baseDamage`, `score`, `radius`, `pathIndex`, `progress`, `status`, `flashTimer`, `state` | `data/enemies.js` |
| `TowerRecord` | `id`, `type`, `level`, `cell`, `x`, `y`, `range`, `damage`, `fireRate`, `fireTimer`, `aim`, `invested`, `buffs` | `data/towers.js` |
| `TrapRecord` | `id`, `type`, `cell`, `x`, `y`, `triggerRadius`, `explodeRadius`, `damage`, `slow`, `duration`, `active`, `armed` | `data/traps.js` |
| `ProjectileRecord` | `id`, `sourceId`, `targetId`, `x`, `y`, `speed`, `damage`, `splash`, `slow`, `type` | Combat |
| `BeamRecord` | `id`, `sourceId`, `targetId`, `x1`, `y1`, `x2`, `y2`, `life`, `ignoreArmor` | Combat |
| `PickupRecord` | `id`, `kind`, `value`, `x`, `y`, `targetX`, `targetY`, `flightTime`, `state` | Economy |
| `WaveRecord` | `levelId`, `waveIndex`, `groups`, `delayAfter`, `bonus` | `data/levels.js` |
| `AbilityRecord` | `id`, `name`, `unlockLevel`, `cooldown`, `radius`, `duration`, `effect`, `input` | `data/abilities.js` |
| `ScoreRecord` | `levelId`, `score`, `difficulty`, `date` | Scoring |
| `LevelRecord` | `id`, `name`, `parTime`, `startFish`, `baseHp`, `path`, `waves` | `data/levels.js` |

### Enemy roster

| Type | Name | HP | Armor | Speed px/s | Fish reward | Base damage | Score | Radius | Special |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `rat` | Fish Rat | 18 | 0 | 60 | 5 | 5 | 10 | 12 | none |
| `gull` | Snack Gull | 32 | 0 | 95 | 8 | 7 | 18 | 14 | none |
| `raccoon` | Raccoon Thief | 95 | 0 | 48 | 18 | 15 | 45 | 18 | none |
| `crab` | Shell Snatcher | 160 | 8 | 36 | 25 | 20 | 70 | 20 | armor |
| `boss` | Gull King | 4200 | 12 | 32 | 300 | 100 | 1500 | 34 | immune to freeze/stun, slow cap 50% |

### Buildable roster

| Type | Name | Cost | Upgrade costs | Max level | Sell refund | Tier |
| --- | --- | ---: | --- | ---: | --- | --- |
| `alleyCat` | Alley Cat | 50 | 40, 70 | 3 | 70% invested | 1 |
| `fishmongerCat` | Fishmonger Cat | 120 | 80, 120 | 3 | 70% invested | 1 |
| `laserCat` | Laser Pointer Cat | 175 | 120, 180 | 3 | 70% invested | 1 |
| `yarnTrap` | Yarn Trap | 60 | none | 1 | 70% if untriggered | 1 |

### Trap roster

| Type | Name | Trigger radius | Explosion radius | Damage | Slow | Duration | Max active |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `yarnTrap` | Yarn Trap | 15 | 40 | 25 | 60% | 2.5 s | 3 |

### Pickup roster

| Type | Name | Value | Visual | Collection |
| --- | --- | ---: | --- | --- |
| `fishCoin` | Fish Coin | equal to kill reward | gold fish | auto after 0.25 s |
| `waveBonus` | Wave Bonus Coin | equal to wave bonus | gold fish + banner | auto at wave clear |
| `bossTuna` | Boss Tuna Coin | 300 | large gold fish | auto on boss death |

### Ability roster

| Type | Name | Unlock | Cooldown | Radius | Effect | Input |
| --- | --- | --- | ---: | ---: | --- | --- |
| `catnipFrenzy` | Catnip Frenzy | after Level 1 win | 45 s | 120 | towers in radius: fire rate +50%, damage +25% for 8 s | click ability, click map |
| `fishFreeze` | Fish Freeze | after Level 2 win | 30 s | 110 | enemies in radius frozen 2.5 s | click ability, click map |
| `netDrop` | Net Drop | after Level 3 win | 60 s | 100 | enemies in radius slowed 80% for 4 s and take 30 damage | click ability, click map |

## 4.1 Combat — Tier 1

| Rule | Value |
| --- | --- |
| Base HP by level | L1 100, L2 100, L3 120, L4 140, L5 180 |
| Base fail | `base.hp <= 0` |
| Enemy reach base | apply `baseDamage`, kill enemy, create hit particle |
| Tower targeting | furthest along path within range |
| Tower aim speed | 180 degrees/s toward target |
| Tower fire condition | `fireTimer <= 0` and valid target |
| Fire timer reset | `1 / fireRate` |
| Projectile collision | projectile radius + enemy radius |
| Projectile on target death | continues to last known position, then vanishes |
| Laser hitscan | damages instantly, draws beam for 0.12 s |
| Armor | `damage = max(1, rawDamage - armor)` |
| Ignore armor | Laser Pointer Cat L3 only |
| Slow stacking | strongest slow applies, duration refreshes |
| Freeze/stun | speed becomes 0, overrides slower slows |
| Boss slow cap | boss minimum speed is 50% of base speed |
| Hit flash | white outline for 0.08 s |
| Death particles | 6 particles for 0.4 s |
| Coin pickup | spawn at enemy death, fly 0.35 s, economy already added |
| Wave clear | no alive enemies and no pending spawns |

### Tower combat stats

| Tower | Level | Damage | Fire rate | Range | Special |
| --- | ---: | ---: | ---: | ---: | --- |
| Alley Cat | 1 | 6 | 1.50 | 110 | single target, projectile speed 240 |
| Alley Cat | 2 | 9 | 1.55 | 120 | single target, projectile speed 240 |
| Alley Cat | 3 | 13 | 1.65 | 130 | single target, projectile speed 240 |
| Fishmonger Cat | 1 | 14 | 0.60 | 100 | splash radius 40, slow 25% 1.5 s, projectile speed 180 |
| Fishmonger Cat | 2 | 20 | 0.65 | 110 | splash radius 45, slow 35% 2.0 s, projectile speed 180 |
| Fishmonger Cat | 3 | 28 | 0.70 | 120 | splash radius 50, slow 45% 2.5 s, projectile speed 180 |
| Laser Pointer Cat | 1 | 35 | 0.40 | 180 | hitscan, beam width 4 |
| Laser Pointer Cat | 2 | 55 | 0.45 | 190 | hitscan, beam width 4 |
| Laser Pointer Cat | 3 | 80 | 0.50 | 200 | hitscan, ignores armor, beam width 5 |

### Trap combat stats

| Trap | Trigger | Effect |
| --- | --- | --- |
| Yarn Trap | enemy center within 15 px | all enemies within 40 px take 25 damage and slow 60% for 2.5 s; trap is destroyed |

## 4.2 Building — Tier 1

| Rule | Value |
| --- | --- |
| Input | select build type from HUD, left click cell |
| Cancel | right click |
| Build validation | cell allowed, fish sufficient, type unlocked, no occupied cell |
| Error | error sound, no placement |
| Tower placement | occupies cell, creates TowerRecord |
| Trap placement | occupies path cell, creates armed TrapRecord |
| Max traps active | 3 |
| Upgrade | click tower, click Upgrade button, spend Fish |
| Sell | click tower, click Sell button, refund 70% of invested |
| Trap sell | only if untriggered, refund 42 |
| Upgrade max | tower max level 3 |
| Unlock | L1 Ally Cat + Yarn Trap; L2 Fishmonger Cat; L3 Laser Pointer Cat; L4+ all |
| Path cell definition | cell center within 15 px of any path segment |
| Tower build cell definition | not path, not occupied, center distance to path <= 150 |
| Trap build cell definition | path cell, not occupied, not within 45 px of spawn or base |
| Placement feedback | valid outline cyan, invalid outline magenta |

## 4.3 Economy — Tier 1

| Rule | Value |
| --- | --- |
| Currency name | Fish |
| Start Fish by level | L1 150, L2 220, L3 280, L4 340, L5 400 |
| Kill reward | from enemy roster |
| Wave completion bonus | from wave table |
| Sell refund | floor(invested * 0.7) |
| Trap refund | floor(60 * 0.7) = 42 |
| Purchase | immediate deduction |
| Insufficient funds | error sound, disabled button |
| Income tracking | `totalEarned`, `totalSpent` |
| Pickup visuals | not required for economy correctness; economy adds value immediately |
| Wave bonus pickup | visual only |
| Boss pickup | visual only |

## 4.4 Waves — Tier 1

### Level records

| Level | Name | Par time | Start Fish | Base HP | Waves | Path waypoints |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | Market Open | 2:00 | 150 | 100 | 3 | `(-30,270) -> (15,270) -> (15,150) -> (435,150) -> (435,390) -> (705,390) -> (705,270) -> (915,270)` |
| 2 | Fish Flies | 3:30 | 220 | 100 | 4 | `(-30,90) -> (15,90) -> (15,270) -> (285,270) -> (285,150) -> (585,150) -> (585,390) -> (885,390) -> (885,270) -> (915,270)` |
| 3 | Raccoon Racket | 5:30 | 280 | 120 | 5 | `(-30,450) -> (15,450) -> (15,300) -> (285,300) -> (285,150) -> (435,150) -> (435,390) -> (585,390) -> (585,210) -> (735,210) -> (735,390) -> (885,390) -> (885,270) -> (915,270)` |
| 4 | Crab Caper | 7:00 | 340 | 140 | 6 | `(-30,90) -> (15,90) -> (15,210) -> (285,210) -> (285,90) -> (585,90) -> (585,300) -> (435,300) -> (435,390) -> (735,390) -> (735,150) -> (885,150) -> (885,270) -> (915,270)` |
| 5 | Gull King | 8:30 | 400 | 180 | 6 | `(-30,270) -> (15,270) -> (15,120) -> (315,120) -> (315,390) -> (615,390) -> (615,150) -> (765,150) -> (765,270) -> (915,270)` |

### Wave rules

| Rule | Value |
| --- | --- |
| First wave delay | 5.0 s after level start |
| Wave clear delay | 8.0 s, except final wave has none |
| Spawn start | first path waypoint, progress 0 |
| Group order | groups spawn sequentially |
| Delay column | delay between enemies in that group |
| Wave complete | no alive enemies and no pending spawns |
| Final wave complete | boss dead and no pending spawns/enemies |
| Level complete | all waves complete |
| Level fail | base HP <= 0 |
| Restart | reset level attempt counter and all gameplay state |
| Unlock next | on level complete, `progress.unlockedLevel = max(current, levelId + 1)` |

### Wave tables

| Level | Wave | Spawn groups | Wave clear bonus | Delay after wave |
| ---: | ---: | --- | ---: | ---: |
| 1 | 1 | `rat x5 @1.2` | 25 | 8.0 |
| 1 | 2 | `rat x8 @1.0` | 50 | 8.0 |
| 1 | 3 | `rat x12 @0.8` | 75 | none |
| 2 | 1 | `rat x6 @1.0` | 25 | 8.0 |
| 2 | 2 | `rat x4 @1.2`, then `gull x5 @1.0` | 50 | 8.0 |
| 2 | 3 | `rat x8 @0.9`, then `gull x8 @0.8` | 75 | 8.0 |
| 2 | 4 | `gull x12 @0.7`, then `rat x4 @0.6` | 100 | none |
| 3 | 1 | `gull x10 @0.8` | 25 | 8.0 |
| 3 | 2 | `rat x8 @0.7`, then `raccoon x3 @2.0` | 50 | 8.0 |
| 3 | 3 | `gull x15 @0.7` | 75 | 8.0 |
| 3 | 4 | `raccoon x5 @1.8`, then `gull x10 @0.7` | 100 | 8.0 |
| 3 | 5 | `raccoon x8 @1.5`, then `gull x12 @0.6` | 125 | none |
| 4 | 1 | `raccoon x10 @1.4` | 25 | 8.0 |
| 4 | 2 | `gull x12 @0.7`, then `crab x3 @2.5` | 50 | 8.0 |
| 4 | 3 | `crab x6 @2.0` | 75 | 8.0 |
| 4 | 4 | `raccoon x10 @1.2`, then `gull x8 @0.7` | 100 | 8.0 |
| 4 | 5 | `crab x6 @1.8`, then `raccoon x8 @1.2` | 125 | 8.0 |
| 4 | 6 | `crab x10 @1.5`, then `raccoon x12 @1.0` | 150 | none |
| 5 | 1 | `gull x12 @0.6` | 25 | 8.0 |
| 5 | 2 | `raccoon x10 @1.2` | 50 | 8.0 |
| 5 | 3 | `crab x8 @1.7` | 75 | 8.0 |
| 5 | 4 | `raccoon x12 @1.0`, then `crab x5 @1.8` | 100 | 8.0 |
| 5 | 5 | `crab x10 @1.5`, then `raccoon x10 @1.1` | 125 | 8.0 |
| 5 | 6 | `boss x1 @0.0`, then `rat x6 @1.0`, then `gull x8 @0.9` | 150 | none |

## 4.5 Abilities — Tier 2

| Rule | Value |
| --- | --- |
| Input | click ability button, then click map |
| Cancel | right click or click ability button again |
| Cooldown starts | only after successful trigger |
| Invalid target | no cooldown, error sound |
| Ability UI | gray while locked, color while ready, gray while cooling |
| Unlock | Catnip after Level 1 win; Fish Freeze after Level 2 win; Net Drop after Level 3 win |
| Persist unlocks | stored in progress |
| Multiple abilities | allowed if ready |
| Cooldown timer | counts down in real time |
| Effect visuals | expanding ring, particles |
| Reduced motion | smaller ring, fewer particles |

### Ability stats

| Ability | Cooldown | Radius | Duration | Effect |
| --- | ---: | ---: | ---: | --- |
| Catnip Frenzy | 45 s | 120 | 8 s | towers in radius: fire rate +50%, damage +25% |
| Fish Freeze | 30 s | 110 | 2.5 s | enemies in radius frozen |
| Net Drop | 60 s | 100 | 4.0 s | enemies in radius slowed 80%, take 30 damage |

## 4.6 Scoring — Tier 3

| Rule | Value |
| --- | --- |
| Score HUD | Tier 1 shows 0. Tier 3 updates it. |
| Enemy kill score | enemy roster `score` |
| Wave clear score | `100 * waveIndex` |
| Base HP score | `remainingBaseHp * 20` |
| Fish score | `remainingFish * 1` |
| Difficulty multiplier | Easy 0.75, Normal 1.00, Hard 1.50 |
| Final level score | `floor((killScore + waveScore + hpScore + fishScore) * difficultyMultiplier)` |
| High score save | only on level win |
| High score storage | top 5 per level |
| High score fields | `score`, `difficulty`, `date` |
| Level select display | best score and best difficulty |
| Win screen display | final score, high-score rank |
| Fail | no high score saved |
| Replay | keep highest score for level |

## 4.7 Progression and difficulty

### Progression

| Stage | Unlock rule | Result |
| --- | --- | --- |
| Level 1 | always unlocked | start game |
| Level 2 | win Level 1 | unlock |
| Level 3 | win Level 2 | unlock |
| Level 4 | win Level 3 | unlock |
| Level 5 | win Level 4 | unlock |
| Completed | win Level 5 | show Win, game complete |
| Replay | any unlocked level | allowed |
| Fail | base HP <= 0 | Game Over, Restart Level |

### Difficulty options — Tier 4

| Difficulty | Enemy HP | Enemy speed | Fish reward | Base HP | Score multiplier |
| --- | ---: | ---: | ---: | ---: | ---: |
| Easy | 0.70 | 0.85 | 1.25 | 1.50 | 0.75 |
| Normal | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Hard | 1.35 | 1.15 | 0.85 | 0.75 | 1.50 |

### Accessibility options

| Option | Effect |
| --- | --- |
| Sound toggle | mutes all audio. |
| Reduced motion | disables particles, shortens hit flash to 40 ms, disables banner slide, freezes decorative motion. |
| Difficulty options | applies multipliers at level start. |
| Color-blind safe palette | always enabled. Patterns identify health, build cells, traps, enemy types, and base. |

### Feel

The game should feel snappy and silly. Placement clicks are immediate. Towers visibly recoil or flash. Enemies pop into coins. Wave banners are short and loud. The base flashes when damaged. The cursor is a paw. Errors are tiny descending bleeps. Wins are bright arpeggios. Failure is a descending sad bleep.

# 5. CHARACTERS

| Character | Silhouette | Facings | Gameplay states | Animations by name | Motion rules |
| --- | --- | --- | --- | --- | --- |
| Player cursor | Paw | none | hover, buildSelected, abilitySelected, invalid | `cursor_follow` | follows pointer instantly, drawn in canvas |
| Alley Cat | Small cat head, cyan collar | aims at target | idle, fired, upgraded, buffed | `idle_tail`, `aim_rotate`, `fire_recoil`, `muzzle_flash`, `buff_glow` | tail wag 2 Hz, aim max 180 deg/s, recoil 2 px |
| Fishmonger Cat | Cat head, orange apron, fish | aims at target | idle, fired, upgraded, buffed | `idle_bob`, `aim_rotate`, `launch_fish`, `splash_flash`, `buff_glow` | idle bob 1 Hz, launch squash 0.1 s |
| Laser Pointer Cat | Cat head, magenta collar, laser eye | aims at target | idle, fired, upgraded, buffed | `idle_scan`, `aim_rotate`, `beam_flash`, `buff_glow` | scan eye 0.8 Hz, beam fade 0.12 s |
| Yarn Trap | Yarn ball on path tile | none | armed, triggered, destroyed | `idle_yarn`, `trigger_net` | rotate 0.5 Hz, expand net 0.25 s |
| Fish Rat | Gray wedge, tail | path tangent | walking, slowed, frozen, hit, dying, dead | `walk_bob`, `hit_flash`, `death_pop` | bob 3 px, 8 Hz, pop scale 1→0 in 0.25 s |
| Snack Gull | Yellow diamond, wings | path tangent | walking, slowed, frozen, hit, dying, dead | `wing_flap`, `hit_flash`, `feather_pop` | flap 6 Hz, feather burst |
| Raccoon Thief | Purple circle, mask | path tangent | walking, slowed, frozen, hit, dying, dead | `walk_grab`, `hit_flash`, `death_spin` | tail sway 2 Hz, death spin 360 deg |
| Shell Snatcher | Blue wide crab, claws | path tangent | walking, slowed, frozen, hit, dying, dead | `scuttle`, `hit_flash`, `shell_crack` | side step 4 Hz, cracks 0.3 s |
| Gull King | Large gull, crown | path tangent | walking, slowed, hit, dying, dead | `slow_flap`, `hit_flash`, `big_pop` | flap 2 Hz, death scale 1→0 in 0.6 s |
| Fish Coin | Gold fish | none | spawn, flying, collected | `coin_fly` | fly to HUD 0.35 s |
| Base stall | Yellow stall, fish crate | none | idle, damaged, destroyed | `base_bob`, `base_hit`, `base_destroy` | bob 0.5 Hz, hit flash 0.08 s |

# 6. AUDIO

| Name | Recipe | When it plays |
| --- | --- | --- |
| `music_title` | Square arpeggio 440, 554, 659 Hz; 120 BPM; attack 0.02 s, decay 0.2 s; loop | Title screen |
| `music_level` | Triangle bass 110 Hz, square lead simple pattern; 120 BPM | Playing normal levels |
| `music_boss` | Same as `music_level` but 150 BPM, bass 82 Hz, lead more urgent | Level 5 final wave |
| `music_win` | Square arpeggio C major 523, 659, 784, 1046 Hz; 0.6 s | Win screen |
| `music_lose` | Square descending 330, 262, 196, 110 Hz; 0.8 s | Game Over screen |
| `sfx_click` | Square 660 Hz, 0.04 s, decay 0.03 | UI button click |
| `sfx_error` | Square 220 Hz, 0.12 s, decay 0.05 | Invalid placement, insufficient fish, invalid ability target |
| `sfx_place` | Square 660→440 Hz, 0.08 s | Tower or trap placed |
| `sfx_upgrade` | Square 523, 659, 784 Hz, 0.12 s | Tower upgraded |
| `sfx_sell` | Square 440→220 Hz, 0.10 s | Tower or trap sold |
| `sfx_coin` | Square 880 Hz, 0.05 s | Coin pickup |
| `sfx_big_coin` | Square 880, 1320 Hz, 0.12 s | Wave bonus or boss coin |
| `sfx_tower_fire` | Square 1000 Hz, 0.03 s, decay 0.02 | Alley Cat fires |
| `sfx_fish_launch` | Square 700→350 Hz, 0.06 s | Fishmonger Cat fires |
| `sfx_laser` | Sawtooth sweep 1200→300 Hz, 0.12 s | Laser Pointer Cat fires |
| `sfx_splash` | Square 300 Hz with rapid amplitude noise, 0.12 s | Fish splash or trap explosion |
| `sfx_enemy_hit` | Square 180 Hz, 0.04 s | Enemy takes damage |
| `sfx_enemy_death` | Square 523→196 Hz, 0.15 s | Enemy dies |
| `sfx_base_hit` | Square 90 Hz, 0.18 s | Base takes damage |
| `sfx_trap_trigger` | Square 780→200 Hz, 0.18 s | Yarn Trap triggers |
| `sfx_wave_start` | Square 220→880 Hz, 0.20 s | Wave begins |
| `sfx_ability_select` | Triangle 880 Hz, 0.05 s | Ability selected |
| `sfx_ability_catnip` | Square 523, 659, 784, 988 Hz, 0.25 s | Catnip Frenzy triggers |
| `sfx_ability_freeze` | Triangle 1000→600 Hz, 0.25 s | Fish Freeze triggers |
| `sfx_ability_net` | Square 300→150 Hz, 0.30 s | Net Drop triggers |
| `sfx_pause` | Square 440 Hz, 0.10 s | Pause |
| `sfx_resume` | Square 660 Hz, 0.10 s | Resume |
| `sfx_unlock` | Square 784, 988, 1175 Hz, 0.20 s | Level unlocked or ability unlocked |

# 7. UX

All screens and HUD elements are HTML/CSS only. The game canvas is behind the HUD. No UI uses canvas text. The cursor is pointer-only. UI controls are buttons, not sliders.

## 7.1 Screen state machine

| State | Entry | Visible controls | Allowed transitions |
| --- | --- | --- | --- |
| `title` | App load | Play, Settings, High Scores if Tier 3 | `levelSelect`, `settings`, `highScores` |
| `levelSelect` | Title Play | Level cards 1–5, Settings, High Scores if Tier 3 | `playing`, `settings`, `highScores`, `title` |
| `playing` | Level selected | HUD, Pause button | `paused`, `gameOver`, `win` |
| `paused` | Pause button | Resume, Restart Level, Settings, Quit to Level Select | `playing`, `settings`, `levelSelect` |
| `settings` | Settings from any screen | Sound toggle, Back; Tier 4 adds Difficulty and Reduced Motion | previous state |
| `gameOver` | Base HP <= 0 | Restart Level, Quit to Level Select | `playing`, `levelSelect` |
| `win` | Level 5 final wave complete | Continue to Level Select, High Scores if Tier 3 | `levelSelect`, `highScores` |
| `highScores` | High Scores button | Level tabs or list, Back | `title`, `levelSelect` |

## 7.2 HUD table

| Element | Record field | When visible | Input |
| --- | --- | --- | --- |
| Health bar | `ctx.base.hp`, `ctx.base.maxHp` | `playing`, `paused` | none |
| Score | `ctx.score.current` | `playing`, `paused` | none; Tier 1 remains 0 |
| Wave number | `ctx.level.waveIndex + 1`, `ctx.level.totalWaves` | `playing`, `paused` | none |
| Currency | `ctx.economy.fish` | `playing`, `paused` | none |
| Build palette | `ctx.input.buildSelected`, tower costs, lock state | `playing` | left click select |
| Selected entity panel | `ctx.input.selectedEntity` stats | `playing` when tower selected | left click Upgrade/Sell |
| Ability buttons | `ctx.abilities.cooldowns`, `ctx.abilities.unlocked`, `ctx.abilities.selected` | Tier 2 `playing` | left click select |
| Ability cooldown overlay | `ctx.abilities.cooldowns[abilityId]` | Tier 2 `playing` | none |
| Wave banner | `ctx.ui.banner.text` | wave start only | none |
| Pause button | `ctx.mode == playing` | `playing` | left click |
| Error message | `ctx.ui.messageQueue` | invalid action | none |

## 7.3 Screen HTML/CSS rules

| Screen | Required HTML elements | CSS rules |
| --- | --- | --- |
| Title | `#title`, `#playBtn`, `#settingsBtn`, `#highScoresBtn` | clean sans, saturated buttons, large title, no motion unless reduced motion off |
| Level select | `#levelSelect`, 5 level cards, lock icons, best score text if Tier 3 | locked cards gray, unlocked cards colored, keyboard not required |
| Gameplay HUD | `#hud`, health, score, wave, fish, palette, abilities, pause | fixed top/bottom strips, high contrast, large touch targets |
| Pause | `#pause`, Resume, Restart, Settings, Quit | dark overlay, centered panel |
| Settings | `#settings`, Back, Sound toggle; Tier 4 adds difficulty buttons and reduced-motion toggle | buttons only, no sliders, clear labels |
| Game Over | `#gameOver`, Restart Level, Quit | red/orange warning, Restart primary |
| Win | `#win`, score summary, Continue, High Scores if Tier 3 | celebratory but flat, no external images |
| High Scores | `#highScores`, level tabs or list, Back | monospace numbers optional, clean sans required |

## 7.4 Accessibility UX rules

| Rule | Implementation |
| --- | --- |
| Color-blind safe palette | Always on. Patterns and shapes identify all critical states. |
| Reduced motion | When enabled, remove particles, shorten flashes, disable banner slide, disable idle decoration. |
| Difficulty options | Tier 4 adds three buttons: Easy, Normal, Hard. Changes apply on next level start. |
| Pointer-only | All controls are clickable buttons or canvas clicks. |
| Focus | If browser focus is used, it must not be required for gameplay. |
| Text contrast | Minimum 4.5:1 for body text. |

# 8. DEBUG API

| Function | System | Reaches | Purpose |
| --- | --- | --- | --- |
| `debug.game.startLevel(levelId, difficulty)` | Game | `ctx.level`, `ctx.base`, `ctx.economy` | Start a level for tests. |
| `debug.game.setMode(mode)` | UI | `ctx.mode` | Force screen state. |
| `debug.input.setPointer(x, y)` | Input | `ctx.input.pointer` | Move cursor. |
| `debug.input.leftClick()` | Input | `ctx.input.leftClick` | Click current pointer. |
| `debug.input.rightClick()` | Input | `ctx.input.rightClick` | Cancel selection. |
| `debug.building.placeAt(col, row, type)` | Building | `ctx.entities.towers`, `ctx.entities.traps` | Place a buildable directly. |
| `debug.building.upgrade(entityId)` | Building | `ctx.entities.towers` | Upgrade tower. |
| `debug.building.sell(entityId)` | Building | `ctx.entities.towers`, `ctx.entities.traps` | Sell entity. |
| `debug.economy.addFish(amount, reason)` | Economy | `ctx.economy.fish` | Add currency. |
| `debug.economy.setFish(amount)` | Economy | `ctx.economy.fish` | Set currency. |
| `debug.combat.spawnEnemy(type, progress)` | Combat | `ctx.entities.enemies` | Spawn enemy at path progress. |
| `debug.combat.damageEnemy(id, amount, ignoreArmor)` | Combat | `ctx.entities.enemies` | Damage enemy. |
| `debug.combat.damageBase(amount)` | Combat | `ctx.base.hp` | Damage base. |
| `debug.wave.startWave(index)` | Waves | `ctx.level.waveIndex`, `ctx.level.spawnQueue` | Start a wave. |
| `debug.wave.setWave(index)` | Waves | `ctx.level.waveIndex` | Jump to wave. |
| `debug.abilities.unlock(abilityId)` | Abilities | `ctx.abilities.unlocked` | Unlock ability. |
| `debug.abilities.trigger(abilityId, x, y)` | Abilities | `ctx.abilities.cooldowns`, effects | Trigger ability. |
| `debug.score.addKill(type)` | Scoring | `ctx.score.current` | Add kill score. |
| `debug.score.addWave(index)` | Scoring | `ctx.score.current` | Add wave score. |
| `debug.score.finishLevel()` | Scoring | `ctx.score.levelScore` | Compute final level score. |
| `debug.settings.setDifficulty(value)` | Settings | `ctx.settings.difficulty` | Set difficulty. |
| `debug.settings.setReducedMotion(value)` | Settings | `ctx.settings.reducedMotion` | Set reduced motion. |
| `debug.settings.setSound(value)` | Settings | `ctx.settings.soundEnabled` | Set sound. |
| `debug.progress.unlockLevel(id)` | Progress | `ctx.progress.unlockedLevel` | Unlock level. |
| `debug.progress.setHighScores(levelId, scores)` | Scoring | `ctx.progress.highScores` | Insert test high scores. |

# 9. TESTS

| Tier | Test | Steps | Expected |
| --- | --- | --- | --- |
| 1 | Fixed loop determinism | Start L1 Normal, run 10 s with same seed twice | Identical state hashes except particle state disabled. |
| 1 | Pointer-only input | Call `debug.input.setPointer`, `leftClick`, `rightClick` | No keyboard functions required. |
| 1 | Build validation | Try place on path, outside range, occupied, insufficient fish | Invalid placements fail, valid succeeds. |
| 1 | Tower placement | Set fish 50, place Alley Cat | Tower exists, fish reduced by 50. |
| 1 | Tower upgrade | Place Alley Cat, set fish 40, upgrade | Level 2 stats apply, fish reduced by 40. |
| 1 | Tower sell | Place Alley Cat, sell | Entity removed, fish +35. |
| 1 | Trap placement | Set fish 60, place Yarn Trap on path | Trap exists, fish reduced by 60. |
| 1 | Trap trigger | Spawn rat near trap | Enemy damaged/slowed, trap removed. |
| 1 | Combat kill | Spawn rat, place Alley Cat | Rat dies, coin pickup created. |
| 1 | Base damage | Spawn rat with no towers | Base HP reduced by 5. |
| 1 | Level fail | Set base HP 5, spawn rat | Mode becomes `gameOver`. |
| 1 | Level win L1 | Clear all 3 waves | Mode becomes `win`, Level 2 unlocked. |
| 1 | Restart level | Fail, call Restart | Level resets, progress preserved. |
| 1 | Sequence unlock | Win L1, open level select | L2 unlocked, L3+ locked. |
| 1 | Final boss win | Clear L5 wave 6 | Mode becomes `win`. |
| 1 | HUD required fields | Start L1 | Health, score, wave, currency elements visible. |
| 1 | Safe palette | Render any entity | Shape/pattern identifiers present, no color-only state. |
| 1 | Audio contract | Call each audio name | No errors, all sounds synthesized. |
| 1 | Screens required | Transition title, level select, pause, settings, game over, win | All states exist except high scores optional. |
| 2 | Ability unlock | Win L1, unlock Catnip | Catnip selectable. |
| 2 | Ability trigger | Call `debug.abilities.trigger('catnipFrenzy', x, y)` | Towers in radius buffed, cooldown starts. |
| 2 | Ability cooldown | Trigger Fish Freeze | Cannot trigger again until cooldown expires. |
| 2 | Ability invalid target | Select ability, click UI | No cooldown, error sound. |
| 2 | Ability net effect | Trigger Net Drop on enemies | Enemies slowed and damaged. |
| 3 | Score placeholder | Tier 1 start | Score element shows 0. |
| 3 | Kill score | Call `debug.score.addKill('rat')` | Score increases by 10. |
| 3 | Wave score | Call `debug.score.addWave(2)` | Score increases by 200. |
| 3 | Final level score | Win L1 with known state | Score matches formula. |
| 3 | High score save | Win L1 | Top 5 list stores score. |
| 3 | High score screen | Open high scores | Shows stored scores. |
| 4 | Easy difficulty | Start L1 Easy | Enemy HP, reward, base HP use multipliers. |
| 4 | Hard difficulty | Start L1 Hard | Enemy HP, speed, reward, score use multipliers. |
| 4 | Reduced motion | Enable, trigger combat | Particles disabled, flash shortened. |
| 4 | Settings persistence | Change difficulty/sound, reload | Settings restored. |
| 4 | Accessibility controls | Click difficulty and reduced-motion buttons | No keyboard required. |

# 10. BUILD ORDER

1. Create `index.html`, `styles.css`, canvas, and clean sans UI shell.
2. Implement `core/config.js` with all final numbers.
3. Implement `core/state.js` with global context and level reset.
4. Implement fixed loop and render skeleton.
5. Implement pointer input and custom paw cursor.
6. Implement title, level select, gameplay, pause, settings, game over, win screens.
7. Implement HUD elements: health, score placeholder, wave, currency.
8. Implement level data and path rendering.
9. Implement enemy spawning and path movement.
10. Implement base damage and fail state.
11. Implement building: build cells, placement, selection, upgrade, sell.
12. Implement combat: targeting, projectiles, lasers, armor, statuses.
13. Implement economy: fish, rewards, costs, refunds.
14. Implement waves: wave tables, delays, wave clear, level complete.
15. Implement art, particles, hit flash, and base visuals.
16. Implement audio: music and all SFX.
17. Verify Tier 1 Definition of Done.
18. Implement abilities system and ability HUD.
19. Verify Tier 2 Definition of Done.
20. Implement scoring, high scores, and level-select best scores.
21. Verify Tier 3 Definition of Done.
22. Implement difficulty options, reduced motion, and accessibility polish.
23. Verify Tier 4 Definition of Done.
24. Playthrough all levels under 30 minutes and adjust only if numbers are wrong.

# 11. DEFINITION OF DONE

## Tier 1 Definition of Done

High level: A player can play five sequential levels, place defenses, survive waves, fail and restart, and win by defeating the final boss. The game has the required art, audio, HUD, and effects.

- [ ] Virtual canvas is 960×540 and uses 30 px cells.
- [ ] Simulation is fixed 60 Hz.
- [ ] Input is pointer-only.
- [ ] No player-controlled movement exists.
- [ ] Enemies follow fixed paths.
- [ ] Five levels exist with exact paths and wave tables.
- [ ] Level 5 final boss exists and must be killed.
- [ ] Base HP reaches 0 and causes Game Over.
- [ ] Restart Level resets gameplay but preserves progress.
- [ ] Title, level select, gameplay, pause, settings, game over, and win screens exist.
- [ ] HUD shows health, score placeholder, wave number, and currency.
- [ ] Score field exists and remains 0 in Tier 1.
- [ ] Build palette allows Alley Cat, Fishmonger Cat, Laser Pointer Cat, and Yarn Trap according to unlock rules.
- [ ] Towers can be placed, upgraded, sold.
- [ ] Traps can be placed and trigger.
- [ ] Towers automatically attack enemies.
- [ ] Enemies damage base on reaching it.
- [ ] Armor, slow, freeze, and stun rules work.
- [ ] Fish is earned from kills and wave clears.
- [ ] Fish is spent on towers, upgrades, and traps.
- [ ] Sell refunds are 70%.
- [ ] Waves start automatically and are harder than prior waves.
- [ ] Level unlock progression works.
- [ ] All art is flat vector with solid fills and crisp outlines.
- [ ] Palette is saturated and color-blind safe.
- [ ] Particles and hit flash exist.
- [ ] Chiptune music and retro bleep SFX exist.
- [ ] All required audio names play.
- [ ] No external assets are required.

## Tier 2 Definition of Done

High level: Abilities are complete, visible, and limited by cooldowns.

- [ ] Catnip Frenzy, Fish Freeze, and Net Drop exist.
- [ ] Ability buttons appear in HUD.
- [ ] Ability selection and target click work.
- [ ] Right click cancels ability selection.
- [ ] Cooldowns count down and block reuse.
- [ ] Catnip buffs towers in radius.
- [ ] Fish Freeze freezes enemies in radius.
- [ ] Net Drop slows and damages enemies in radius.
- [ ] Abilities unlock after Level 1, Level 2, and Level 3 wins.
- [ ] Ability sounds and particles play.

## Tier 3 Definition of Done

High level: The game calculates and stores scores.

- [ ] Score HUD updates during gameplay.
- [ ] Kill score values are applied.
- [ ] Wave clear score values are applied.
- [ ] Final level score includes HP and remaining Fish.
- [ ] Difficulty multiplier applies in Tier 4 but scoring formula exists in Tier 3.
- [ ] High scores screen exists.
- [ ] Top 5 scores are stored per level.
- [ ] Level select shows best score.
- [ ] Win screen shows final score and rank.
- [ ] Failed attempts do not save scores.
- [ ] Replays keep highest score.

## Tier 4 Definition of Done

High level: Accessibility options are complete.

- [ ] Sound toggle works.
- [ ] Easy, Normal, Hard difficulty buttons exist.
- [ ] Difficulty multipliers apply at level start.
- [ ] Reduced motion toggle exists.
- [ ] Reduced motion disables particles and shortens flashes.
- [ ] Color-blind safe patterns remain active.
- [ ] Settings persist locally.
- [ ] All controls remain pointer-only.

# A. SANITY

| Check | Result | Notes |
| --- | --- | --- |
| All required headings present | PASS | Sections 0 through A match requested order. |
| Asked requirements mapped | PASS | §0.1 maps every user decision. |
| Every decision documented | PASS | §0.2 includes user decisions and rulings. |
| Tiers respect core/support/extra bands | PASS | Tier 1 core only, Tier 2 abilities, Tier 3 scoring, Tier 4 accessibility options. |
| No extra systems added | PASS | Traps and pickups are content under Building/Economy, not separate systems. |
| Player movement is absent | PASS | No player movement; enemies path. |
| Cursor-only input is complete | PASS | Pointer hover/click/right-click only; UI uses buttons. |
| Real-time model is fixed-step | PASS | 60 Hz fixed simulation. |
| Session shape is sequence of levels | PASS | Five levels unlock sequentially. |
| Failure restarts level | PASS | Game Over has Restart Level. |
| Win requires final boss | PASS | Level 5 final wave includes boss and requires boss death. |
| Size under 30 minutes | PASS | Total par time 26:30. |
| Core combat is concrete | PASS | Tower stats, enemy stats, targeting, damage, statuses. |
| Core building is concrete | PASS | Towers, traps, upgrades, sells, placement rules. |
| Core economy is concrete | PASS | Start fish, rewards, wave bonuses, costs, refunds. |
| Core waves are concrete | PASS | Full wave tables and delays. |
| Abilities are concrete and not required for Tier 1 | PASS | Tier 2 abilities with inputs, cooldowns, effects. |
| Scoring is concrete and not required for Tier 1 | PASS | Tier 3 scoring with formula and high scores. |
| Screens exactly match requested list | PASS | State machine uses only requested screens. |
| HUD includes health, score, wave, currency | PASS | HUD table includes all. |
| Effects include particles and hit flash | PASS | Visual and combat rules include them. |
| Accessibility includes safe palette, reduced motion, difficulty | PASS | Safe palette Tier 1; options Tier 4. |
| Art is flat vector and saturated | PASS | Palette and recipe table use solid fills and crisp outlines. |
| Audio is chiptune and retro bleeps | PASS | Audio table uses synthesized oscillator recipes. |
| Typography is clean sans | PASS | UI CSS uses system sans stack. |
| Engineering contracts allow tests | PASS | Global context, module functions, debug API, tests. |
| Numbers are present | PASS | Units, stats, levels, waves, scoring, difficulty all numeric. |
| No external assets required | PASS | Canvas and Web Audio only. |