# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Game prompt: a space shooter where you fight waves of aliens | 4.27 Progression, 4.6 Waves, 4.5 Enemies, 4.7 Bosses |
| Dimension: 2D | 1.1 Units, axes, frames, 3 Visual Spec |
| Camera: top-down | 1.1 Units, axes, frames, 3 Visual Spec |
| Time model: real-time | 1.1 Units, axes, frames, 1.2 Important conventions |
| Movement model: free movement | 4.2 Player vehicle and movement |
| Session shape: a sequence of levels | 4.27 Progression and difficulty |
| Failure: lose a life | 4.2 Player vehicle and movement, 4.27 Progression and difficulty |
| Tone: tense | 3 Visual Spec, 4.30 Feel, 6 Audio |
| Size: a handful of levels, under 30 minutes | 0.2 Decisions, 4.27 Progression and difficulty |
| Win/lose: defeat a final boss | 4.7 Bosses, 4.27 Progression and difficulty |
| Core mechanics: enemies, shoot, weapons, dodge, waves, vehicles, fly, steer, aim, spawn points, bosses, objectives, difficulty ramp | 4.2 through 4.8, 0.3 Tiers |
| Supporting mechanics: score, rewards, memorize, abilities / special moves, unlocks | 4.9 through 4.12, 0.3 Tiers |
| Extra mechanics: dash, boosts, collectibles, consumables, armour / defence, high scores, traps, equipment, evolution, combos, plot, damage types, cutscenes, transform, medals / ranks, leaderboard | 4.13 through 4.26, 0.3 Tiers |
| Art style: neon / synthwave: dark background, glowing saturated lines and bloom | 3 Visual Spec |
| Palette: dark: mostly black with a few bright accents | 3 Visual Spec, 1.2 Important conventions |
| Typography: techno / display: angular, futuristic letters | 3 Visual Spec, 7 UX |
| Music: synth loop: electronic loop with a beat | 6 Audio |
| Sound effects style: retro bleeps: synthesized chip sounds | 6 Audio |
| Screens: title, pause, settings, game over, win, high scores | 7 UX |
| HUD: health, score, combo counter, wave number | 7 UX, 4 Gameplay Spec |
| Effects: screen shake, particles, hit flash, slow motion on hit, trails, bloom | 3 Visual Spec, 4.30 Feel |
| Accessibility: colour-blind safe palette, reduced motion, remappable keys, difficulty options | 1.2 Important conventions, 3 Visual Spec, 7 UX, 4.8 Difficulty ramp |

## 0.2 Decisions

| Decision | Value / Ruling | Why |
| --- | --- | --- |
| Game identity | The player pilots the **Vanta Skiff**, a neon anti-swarm interceptor fighting five synthwave sectors. | Gives the player a concrete vehicle and a tense, final-destination structure. |
| Level count | Exactly **5 levels**. | “A handful” and keeps a full run under 30 minutes. |
| Wave count | Level 1: 3 waves. Level 2: 3. Level 3: 4. Level 4: 4. Level 5: 5. | Creates a difficulty ramp without making the session too long. |
| Estimated playtime | Target **22–28 minutes** on Normal. | Fits under 30 minutes while allowing boss fights. |
| Arena | Fixed **1920 × 1080 px** top-down arena, no scrolling. | Simplifies camera, collision, spawn points, and top-down legibility. |
| Camera | Fixed to arena center. | Top-down, no pan, keeps spawn points and player visible. |
| Player identity | Pilot **Kael**, ship **Vanta Skiff**. | Small narrative anchor without adding a cutscene-heavy system. |
| Lives | Normal difficulty starts with **3 lives**. Easy **4**, Hard **2**. | “Lose a life” becomes a concrete run resource. |
| Hull | Player hull max **100** base. | Gives a readable health bar and damage budget. |
| Movement speed | Base max speed **280 px/s**. | Fits the 1920 × 1080 arena and projectile speeds. |
| Acceleration | **1800 px/s²** toward target velocity. | Snappy but controllable. |
| Friction | When no movement input, velocity decays by factor `exp(-6 * dt)`. | Free movement with slight drift feel. |
| Aim model | Mouse aim, twin-stick. Ship nose always points at pointer. | Standard browser twin-stick; keeps steering and aiming separate. |
| Primary weapons | **Pulse** and **Ion Lance** are the Tier 1 weapons. | Fulfills “weapons” with a small, distinct pair. |
| Weapon switch | `R` cycles Pulse → Ion Lance. | Concrete named input for the weapon system. |
| Dodge | Core dodge input is `X`: 100 px sidestep, 0.10 s duration, 0.08 s invulnerability, 2.0 s cooldown. | Satisfies core “dodge” without overlapping the extra “dash”. |
| Dash | Extra dash input is `Shift`: 220 px phase dash, 0.22 s invulnerability, charge-based. | Satisfies extra “dash” as a bigger, charged move. |
| Enemy roster | Six enemy vehicles: **Mote, Dart, Bruiser, Turret, Seeker, Bomber**. | Small enough to learn, large enough to build waves. |
| Boss roster | Five bosses, one per level, final boss **Black Sun Sovereign**. | Matches win condition: defeat a final boss. |
| Spawn points | Three enemy gates per level: **A** top-left, **B** top-right, **C** bottom-center. Player spawn left-center. Boss spawn center. | Concrete top-down spawn points for waves and bosses. |
| Objectives | Each level objective: clear all waves, then destroy the boss. Final level objective: destroy the final boss. | Directly implements objectives and win/lose. |
| Difficulty ramp | Enemy HP, speed, fire rate, and damage scale by level and wave. | Core mechanic “difficulty ramp” with concrete numbers. |
| Difficulty options | Easy / Normal / Hard modify enemy stats, player lives, and player damage. | Required accessibility decision. |
| Score | Score is Tier 2. Base score per enemy/trap/boss. | Supporting mechanic, not a dependency of Tier 1. |
| Combo | Combo is Tier 4. Combo counter appears as zero until built. | Extra mechanic, not core. |
| Rewards | Level-clear score bonus plus automatic unlocks. | Supporting mechanic without adding a shop screen. |
| Memorize | Implement **Recall** (`M`): reveals the next 3 spawn events of the current wave for 2–3 s. | Concrete supporting mechanic with named input. |
| Ability | **Neon Burst** (`Q`): radial projectile burst, clears small enemy projectiles, charge-based. | Supporting “abilities / special moves”. |
| Unlocks | Automatic unlocks after levels: ability charge, hull, Recall duration, dash charge, equipment. | Supporting mechanic, no extra UI screen needed. |
| Collectibles | Immediate pickups: Hull Cell, Boost Cell, Armor Plate, Surge Cell, Score Gem, Data Cube. | Extra mechanic with concrete drops and effects. |
| Consumables | Stored capsules: Repair, Surge, Shield. Used with `E`. | Extra mechanic distinct from immediate collectibles. |
| Armour | Separate armor bar, max 30 base, absorbs damage before hull. | Extra “armour / defence”. |
| Traps | **Pulse Mine** and **Static Gate**. | Extra traps with telegraphs and destruction rules. |
| Equipment | One active module at a time: Redline, Aegis, Phase. Toggle with `F`. | Extra equipment with named input. |
| Evolution | Data Cubes evolve the Skiff at 10 and 25 data. | Extra evolution with visible stat changes. |
| Damage types | Kinetic, Beam, Plasma with enemy resistances. | Extra damage types with numbers. |
| Transform | `T`: Ghost Hull for 5 s, charge-based. | Extra transform with named input. |
| Boosts | Hold `Space` to boost, drains boost energy. | Extra boosts with concrete numbers. |
| Plot | Short per-level vignette lines. | Extra plot, kept minimal and tense. |
| Cutscenes | 3-second pre-level vignettes, skippable with `Enter`. | Extra cutscenes without adding new screens. |
| Medals / ranks | Score medal thresholds and level/rank titles. | Extra medals/ranks with numbers. |
| High scores | Best score per difficulty, saved locally. | Extra high scores. |
| Leaderboard | Local top 10 with 3-letter initials. | Extra leaderboard with a small input rule. |
| High scores screen data | Screen shell exists from Tier 1. High score data is Tier 3. Leaderboard data is Tier 4. | Resolves screen requirement without making extra mechanics Tier 1. |
| Pause behavior | Pausing freezes gameplay and timescale. | Standard and accessible. |
| Settings | Difficulty, reduced motion, key remapping, volume. | Required accessibility and settings screen. |
| Local storage keys | `neon-swarm.settings`, `neon-swarm.highscores`, `neon-swarm.leaderboard`. | Keeps persistence explicit. |
| Randomness | Gameplay randomness uses a seeded RNG from `ctx.rand`. No `Math.random()` in gameplay. | Deterministic tests. |
| Fixed step | 60 Hz fixed simulation step. | Stable movement, collisions, and timers. |
| Color-blind safety | No red/green-only coding. Use cyan, magenta, yellow, orange, blue, white and distinct shapes. | Required accessibility. |
| Reduced motion | Disables screen shake, slow motion, halves particles, shortens trails, static stars. | Required accessibility. |
| Typography | Uppercase, letter-spaced, angular display font stack. | Matches techno/display requirement. |

## 0.3 Tiers

| Tier | Name | Scope | Included systems | Not yet included | Exit condition |
| --- | --- | --- | --- | --- | --- |
| Tier 1 | Core playable | Minimal viable game the player can finish | enemies, shoot, weapons, dodge, waves, vehicles, fly, steer, aim, spawn points, bosses, objectives, difficulty ramp, lives, level sequence, base HUD, base screens, base audio, base effects | score logic, rewards, memorize, abilities, unlocks, dash, boosts, collectibles, armour, traps, high score data, and all other extras | A player can start, play all 5 levels, win by defeating the final boss, or game over, with all core mechanics using their final numbers. |
| Tier 2 | Supporting systems | Adds the supporting band | score, rewards, memorize, abilities / special moves, unlocks | all extra systems | Score, Recall, Neon Burst, rewards, and unlocks work on top of Tier 1 without changing core rules. |
| Tier 3 | Survival extras | First extra band | dash, boosts, collectibles, armour / defence, high scores, traps | consumables, equipment, evolution, combos, plot, damage types, cutscenes, transform, medals/ranks, leaderboard | Extra mobility, pickups, armor, traps, and local high scores work without breaking Tier 1/2. |
| Tier 4 | Full meta and presentation | Second extra band | consumables, equipment, evolution, combos, plot, damage types, cutscenes, transform, medals / ranks, leaderboard | none required by decisions | All listed extra mechanics are present with their numbers, inputs, and visuals. |

| Mechanic | Tier |
| --- | --- |
| enemies | Tier 1 |
| shoot | Tier 1 |
| weapons | Tier 1 |
| dodge | Tier 1 |
| waves | Tier 1 |
| vehicles | Tier 1 |
| fly | Tier 1 |
| steer | Tier 1 |
| aim | Tier 1 |
| spawn points | Tier 1 |
| bosses | Tier 1 |
| objectives | Tier 1 |
| difficulty ramp | Tier 1 |
| score | Tier 2 |
| rewards | Tier 2 |
| memorize | Tier 2 |
| abilities / special moves | Tier 2 |
| unlocks | Tier 2 |
| dash | Tier 3 |
| boosts | Tier 3 |
| collectibles | Tier 3 |
| consumables | Tier 4 |
| armour / defence | Tier 3 |
| high scores | Tier 3 |
| traps | Tier 3 |
| equipment | Tier 4 |
| evolution | Tier 4 |
| combos | Tier 4 |
| plot | Tier 4 |
| damage types | Tier 4 |
| cutscenes | Tier 4 |
| transform | Tier 4 |
| medals / ranks | Tier 4 |
| leaderboard | Tier 4 |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Quantity | Unit / Convention | Notes |
| --- | --- | --- |
| Coordinate system | Pixels | Origin top-left. X increases right, Y increases down. |
| Arena | 1920 × 1080 px | Fixed world. No camera scroll. |
| Bounds margin | 20 px | Entity centers are clamped to `[20, 1900]` on X and `[20, 1060]` on Y. |
| Time | Seconds | All timers are seconds. |
| Simulation step | 1 / 60 s | Fixed 60 Hz step. |
| Frame delta | Seconds | `dt` passed to update is `1/60` before timescale. |
| Timescale | Unitless | Normal is 1.0. Slow motion on player hit is 0.3 for 0.18 s. |
| Speed | Pixels per second | Example: 280 px/s. |
| Distance | Pixels | Example: 100 px dash distance. |
| Radius | Pixels | Collision radius. |
| Angle | Radians | 0 points right, π/2 points down. |
| Damage | Float | Display rounded to integer. |
| Health / Armor | Float | Display rounded to integer. |
| Projectile lifetime | Seconds | Destroyed after lifetime. |
| Cooldown / recharge | Seconds | Count down by scaled `dt`. |
| Score | Integer | Rounded up when applying multipliers. |
| Random source | Seeded RNG | `ctx.rand.next()` returns `[0, 1)`. |

## 1.2 Important conventions

- The game uses a **fixed timestep** simulation at 60 Hz. Rendering may occur more frequently, but gameplay updates happen in fixed 1/60 s steps.
- The accumulator clamps frame delta to **0.25 s** maximum to avoid spiral of death.
- All gameplay randomness uses `ctx.rand.next()`. `Math.random()` is not used in gameplay, spawning, drops, or tests.
- Tests may set `ctx.rand.seed = 1` for deterministic behavior.
- All modules mutate only the global context through their exported functions.
- All gameplay values come from data tables in `data/`. Modules do not hard-code enemy stats, weapon stats, or level layouts.
- All timers use scaled time: `timer -= dt * ctx.clock.timescale`.
- Collision uses circle-vs-circle for entities and circle-vs-segment for Static Gates.
- Projectiles do not collide with each other.
- Enemy projectiles do not collide with the player during player invulnerability.
- Player contact damage has a 0.5 s per-enemy cooldown.
- Reduced motion disables: screen shake, slow motion, star drift, long trails, and high particle counts.
- Colour-blind safety is always active. No mechanic depends only on red vs green.
- Settings persist to `neon-swarm.settings`.
- High scores persist to `neon-swarm.highscores`.
- Leaderboard persists to `neon-swarm.leaderboard`.
- The game has no network, no external images, and no external audio files.
- Audio is synthesized with the Web Audio API.
- UI screens are HTML/CSS overlays. The world is canvas.
- The player does not pick up or use items with mouse input, except aiming.

# 2. CONTRACTS

## 2.1 Module layout

| File / Module | Exports | Purpose |
| --- | --- | --- |
| `index.html` | DOM structure | Canvas, HUD, screen overlays. |
| `style.css` | CSS classes | Neon synthwave UI, HUD, buttons, reduced-motion rules. |
| `main.js` | `init()`, `start()`, `setState()`, `getContext()` | Bootstraps context, owns state machine, calls loop. |
| `modules/loop.js` | `createLoop()`, `step()`, `render()` | Fixed-step accumulator. |
| `modules/input.js` | `init()`, `isDown()`, `consumePress()`, `pointer()`, `setKeybind()`, `getBinds()` | Keyboard/mouse state and remapped actions. |
| `modules/settings.js` | `load()`, `save()`, `get()`, `set()`, `apply()` | Persistent settings. |
| `modules/audio.js` | `init()`, `playSfx()`, `startMusic()`, `stopMusic()`, `setVolume()` | Web Audio synthesis. |
| `modules/ui.js` | `setState()`, `render()`, `bindScreenKeys()` | DOM screens and transitions. |
| `modules/hud.js` | `update()`, `render()` | HUD from context. |
| `modules/player.js` | `update()`, `damage()`, `fire()`, `switchWeapon()`, `dodge()`, `dash()`, `boost()`, `recall()`, `ability()`, `transform()`, `useConsumable()`, `cycleEquipment()` | Player vehicle. |
| `modules/enemy.js` | `spawn()`, `update()`, `damage()`, `clear()` | Enemy vehicles. |
| `modules/boss.js` | `spawn()`, `update()`, `damage()`, `clear()` | Boss vehicles. |
| `modules/projectile.js` | `update()`, `firePlayer()`, `fireEnemy()`, `clear()` | Player and enemy projectiles. |
| `modules/wave.js` | `startLevel()`, `startWave()`, `update()`, `spawnNext()`, `completeLevel()` | Wave spawning and level flow. |
| `modules/trap.js` | `spawn()`, `update()`, `damage()`, `clear()` | Traps. |
| `modules/collectible.js` | `spawn()`, `update()`, `collect()` | Pickups. |
| `modules/effects.js` | `addShake()`, `addHitFlash()`, `slowMo()`, `addParticles()`, `addTrail()`, `update()` | Visual effects. |
| `modules/debug.js` | `debug*()` functions | Direct state access and input injection. |
| `data/weapons.js` | `WEAPONS` | Weapon table. |
| `data/enemies.js` | `ENEMIES`, `ENEMY_DAMAGE_TYPES` | Enemy stats and resistances. |
| `data/bosses.js` | `BOSSES` | Boss stats and patterns. |
| `data/levels.js` | `LEVELS` | Level and wave tables. |
| `data/collectibles.js` | `COLLECTIBLES`, `CONSUMABLES` | Pickup data. |
| `data/traps.js` | `TRAPS` | Trap data. |
| `data/equipment.js` | `EQUIPMENT` | Equipment modules. |
| `data/evolution.js` | `EVOLUTION` | Evolution thresholds. |
| `data/medals.js` | `MEDALS`, `RANKS` | Medal and rank data. |
| `data/settings.js` | `DEFAULT_SETTINGS` | Default settings. |
| `tests/run.js` | `runTests()` | Headless tests. |

## 2.2 Global context

| Field | Type / Shape | Notes |
| --- | --- | --- |
| `ctx.state` | string | `title`, `pause`, `settings`, `playing`, `gameover`, `win`, `highscores`. |
| `ctx.previousState` | string or null | State to return from settings. |
| `ctx.difficulty` | `easy`, `normal`, `hard` | Active difficulty. |
| `ctx.reducedMotion` | boolean | Accessibility toggle. |
| `ctx.volume` | `{ master, music, sfx }` | 0–1. |
| `ctx.keybinds` | object | Action → key code. |
| `ctx.clock` | object | `elapsed`, `step`, `timescale`, `slowMoTimer`. |
| `ctx.rand` | object | `seed`, `next()`. |
| `ctx.run` | object | Run-level state. |
| `ctx.run.levelIndex` | integer 0–4 | Current level. |
| `ctx.run.waveIndex` | integer 0-based | Current wave. |
| `ctx.run.lives` | integer | Remaining lives. |
| `ctx.run.maxLives` | integer | From difficulty. |
| `ctx.run.score` | integer | Current run score. |
| `ctx.run.scoreAtLevelStart` | integer | Snapshot for retries. |
| `ctx.run.combo` | integer | Tier 4. |
| `ctx.run.comboTimer` | number | Seconds remaining in combo. |
| `ctx.run.comboMultiplier` | number | Computed from combo. |
| `ctx.run.bestScore` | integer | Highest score in run. |
| `ctx.run.highScores` | object | Best score per difficulty. |
| `ctx.run.leaderboard` | array | Top 10 entries. |
| `ctx.run.evolutionData` | integer | Data Cube count. |
| `ctx.run.evolutionStage` | integer 0–2 | Current evolution. |
| `ctx.run.unlocks` | object | Applied unlocks. |
| `ctx.run.levelSnapshot` | object | Snapshot at level start. |
| `ctx.player` | object | Player vehicle record. |
| `ctx.player.pos` | `{ x, y }` | Player center. |
| `ctx.player.vel` | `{ x, y }` | Velocity. |
| `ctx.player.angle` | number | Aim angle in radians. |
| `ctx.player.maxSpeed` | number | Base 280. |
| `ctx.player.acceleration` | number | Base 1800. |
| `ctx.player.hull` | number | Current hull. |
| `ctx.player.maxHull` | number | Base 100. |
| `ctx.player.armor` | number | Tier 3. |
| `ctx.player.maxArmor` | number | Tier 3. |
| `ctx.player.armorRegen` | number | Armor regen per second. |
| `ctx.player.armorDelayTimer` | number | Time since last damage. |
| `ctx.player.invulnTimer` | number | Invulnerability seconds. |
| `ctx.player.hitFlashTimer` | number | Hit flash timer. |
| `ctx.player.weaponIndex` | integer 0–1 | Current weapon. |
| `ctx.player.fireCooldown` | number | Seconds until next shot. |
| `ctx.player.switchLockout` | number | Weapon switch lockout. |
| `ctx.player.dodgeTimer` | number | Active dodge time. |
| `ctx.player.dodgeCooldown` | number | Dodge cooldown. |
| `ctx.player.dodgeDir` | `{ x, y }` | Dodge direction. |
| `ctx.player.dashTimer` | number | Active dash time. |
| `ctx.player.dashCharges` | integer | Extra dash. |
| `ctx.player.dashRecharge` | number[] | Recharge timers per charge. |
| `ctx.player.dashDir` | `{ x, y }` | Dash direction. |
| `ctx.player.boostEnergy` | number | 0–100. |
| `ctx.player.boosting` | boolean | Boost active. |
| `ctx.player.transformCharges` | integer | Transform charges. |
| `ctx.player.transformTimer` | number | Transform active time. |
| `ctx.player.transformRecharge` | number[] | Transform recharge timers. |
| `ctx.player.abilityCharges` | integer | Neon Burst charges. |
| `ctx.player.abilityRecharge` | number[] | Neon Burst recharge timers. |
| `ctx.player.recallUses` | integer | Recall uses remaining this level. |
| `ctx.player.recallTimer` | number | Recall active time. |
| `ctx.player.recallCooldown` | number | Recall cooldown. |
| `ctx.player.consumables` | `{ repair, surge, shield }` | Tier 4 inventory. |
| `ctx.player.equipmentInstalled` | string[] | Installed equipment ids. |
| `ctx.player.equipmentIndex` | integer | Active equipment index. |
| `ctx.player.trail` | array | Trail points. |
| `ctx.weapons` | array | Weapon records. |
| `ctx.enemies` | array | Enemy vehicle records. |
| `ctx.boss` | object or null | Boss record. |
| `ctx.projectiles.player` | array | Player projectiles. |
| `ctx.projectiles.enemy` | array | Enemy projectiles. |
| `ctx.traps` | array | Trap records. |
| `ctx.collectibles` | array | Immediate pickup records. |
| `ctx.particles` | array | Effect particles. |
| `ctx.floatTexts` | array | Damage/score popups. |
| `ctx.level` | object | Current level data. |
| `ctx.wave` | object | Wave state. |
| `ctx.wave.state` | string | `intermission`, `spawning`, `clearing`, `boss`, `complete`. |
| `ctx.wave.spawnQueue` | array | Remaining spawn events. |
| `ctx.wave.intermissionTimer` | number | Seconds until next wave. |
| `ctx.effects` | object | `shakeMag`, `hitFlash`, `bloom`. |
| `ctx.audio` | object | Music state. |
| `ctx.ui` | object | UI selection state. |
| `ctx.debug` | object | Debug flags. |

## 2.3 Module specifics

| Module | Required functions | Purpose |
| --- | --- | --- |
| `main.js` | `init()`, `start()`, `setState(state)`, `getContext()` | Boot, state machine, context access. |
| `loop.js` | `createLoop(update, render)`, `step(dt)` | Fixed-step update. |
| `input.js` | `init()`, `isDown(action)`, `consumePress(action)`, `pointer()`, `setKeybind(action, keyCode)`, `getBinds()` | Input polling and remapping. |
| `settings.js` | `load()`, `save()`, `get(key)`, `set(key, value)`, `apply()` | Persistent settings. |
| `audio.js` | `init()`, `playSfx(name)`, `startMusic()`, `stopMusic()`, `setVolume(channel, value)` | Synthesized audio. |
| `ui.js` | `setState(state)`, `render()`, `bindScreenKeys()` | DOM screen state. |
| `hud.js` | `update()`, `render()` | HUD values. |
| `player.js` | `update(dt)`, `damage(amount, source)`, `fire(dt)`, `switchWeapon()`, `dodge()`, `dash()`, `boost(dt)`, `recall()`, `ability()`, `transform()`, `useConsumable()`, `cycleEquipment()` | Player rules. |
| `enemy.js` | `spawn(type, gate)`, `update(dt)`, `damage(enemy, amount)`, `clear()` | Enemy rules. |
| `boss.js` | `spawn(levelIndex)`, `update(dt)`, `damage(boss, amount)`, `clear()` | Boss rules. |
| `projectile.js` | `update(dt)`, `firePlayer(weaponIndex)`, `fireEnemy(owner, target, kind)`, `clear()` | Projectile rules. |
| `wave.js` | `startLevel(levelIndex)`, `startWave(waveIndex)`, `update(dt)`, `spawnNext()`, `completeLevel()` | Wave and level flow. |
| `trap.js` | `spawn(type, position)`, `update(dt)`, `damage(trap, amount)`, `clear()` | Trap rules. |
| `collectible.js` | `spawn(type, pos)`, `update(dt)`, `collect(collectible)` | Pickup rules. |
| `effects.js` | `addShake(mag)`, `addHitFlash(color)`, `slowMo(duration, scale)`, `addParticles(pos, color, count)`, `addTrail(entity)`, `update(dt)` | Effects. |
| `debug.js` | functions in section 8 | Direct state access. |
| `tests/run.js` | `runTests()` | Headless validation. |

# 3. VISUAL SPEC

The game is a dark neon synthwave top-down shooter: a black void filled with saturated glowing lines, angular ships, and bright particle bursts. The mood is tense and clean, not busy. The player ship and player bullets read as cyan, enemy threats read as magenta/orange/yellow, and hazards read as orange/yellow. Everything important is shape-coded, not only color-coded. The visual language favors sharp polygons, thin glowing outlines, additive particles, and strong silhouettes.

Lighting and atmosphere are emissive-only. There are no realistic shadows or soft global illumination. The world is lit by its own glow: ship outlines, projectile trails, particle explosions, and gate warnings. Bloom is simulated with canvas shadow blur and additive blending. The background is nearly black with a faint synthwave grid and slow star layers. The arena is bounded by a subtle neon frame.

The space is a fixed 1920 × 1080 px top-down sector. The floor is a dark grid. Three spawn gates are visible at fixed positions: top-left, top-right, and bottom-center. The player spawn is left-center. The boss spawn is center. The outer bounds are a 20 px safe margin with a faint border glow. No scrolling occurs.

| Element | Visual recipe | Numbers / notes |
| --- | --- | --- |
| Background | Solid fill | `#03030a`. |
| Grid | Thin lines | 80 px spacing. Color `#111435`, alpha 0.35. Every 4th line `#1c1f4a`, alpha 0.45. |
| Arena border | Rounded rectangle stroke | 2 px, `#0a2a44`, alpha 0.6. |
| Star layer 1 | 1 px white dots | 90 dots, alpha 0.18, speed 4 px/s. Static in reduced motion. |
| Star layer 2 | 2 px cyan dots | 45 dots, alpha 0.28, speed 8 px/s. |
| Star layer 3 | 3 px magenta dots | 20 dots, alpha 0.22, speed 16 px/s. |
| Player ship | Angular chevron / arrowhead | 36 px wide, 44 px long. Fill `#071022`. Stroke cyan `#00f0ff`, 3 px. Inner cockpit line white, 2 px. |
| Player engine | Small glowing triangle behind ship | Cyan, 10 px, pulses 1 Hz. |
| Player trail | Fading line trail | 12 points, 3 px width, alpha 0.5. Reduced motion: 4 points. |
| Player bullet Pulse | Short glowing rectangle | 12 × 4 px, cyan, shadow blur 8. |
| Player bullet Lance | Thin bolt | 24 × 5 px, cyan-white, shadow blur 12. |
| Enemy bullet | Diamond orb | 10 px, magenta `#ff2ba8`, shadow blur 8. |
| Mote | Small triangle | 22 px, orange `#ff7a00` stroke, dark fill. |
| Dart | Arrow / dart shape | 26 px, magenta `#ff2ba8` stroke. |
| Bruiser | Hexagonal hull | 48 px, blue `#4d7cff` stroke, dark fill, inner plate line. |
| Turret | Square base with circular head | 52 px base, yellow `#ffe100` stroke, head rotates. |
| Seeker | Thin curved chevron | 30 px, magenta/blue mix, strong trail. |
| Bomber | Spiked orb | 36 px, orange stroke, yellow warning pulse before explode. |
| Boss Herald | Spiky diamond | 96 px, magenta/cyan. |
| Boss Warden | Reef slab with emitter nodes | 120 px, blue/cyan. |
| Boss Tyrant | Armored cinder tank | 140 px, orange/yellow. |
| Boss Queen | Hollow crown / spire | 160 px, magenta/white. |
| Boss Sovereign | Black sun disc with corona | 200 px, black core, magenta/yellow corona. |
| Spawn gate | Angular portal | 80 × 48 px. Idle dark cyan. Warning yellow, 0.6 s before spawn. |
| Player spawn | Faint landing marker | 60 px cyan ring, alpha 0.25. |
| Boss spawn | Center hex marker | 160 px magenta ring, alpha 0.25. |
| Pulse Mine | Triangle mine | 24 px, orange. Charging: white pulse. Armed: orange blink 4 Hz. |
| Static Gate | Horizontal or vertical beam | 300 px long, 8 px wide. Telegraph yellow, active orange. |
| Hull Cell | Cross | 24 px cyan. |
| Boost Cell | Bolt | 24 px yellow. |
| Armor Plate | Hexagon | 24 px magenta. |
| Surge Cell | Star | 24 px blue. |
| Score Gem | Diamond | 20 px orange. |
| Data Cube | Cube outline | 24 px white. |
| HUD panels | Angular clipped panels | Background `rgba(4,4,12,0.78)`. Border 2 px cyan or magenta. |
| HUD text | Techno display | Uppercase, letter-spacing 0.12em. |
| Buttons | Angular rectangles | 2 px magenta border. Hover fill `#0a0a1a`. Text cyan. |
| Hit flash | Full entity white overlay | 0.06 s. |
| Player hurt flash | White overlay on player | 0.06 s, plus 0.8 s invuln blink. |
| Explosion particles | Triangular shards | 16 particles normal, 6 reduced. Lifetime 0.5 s. Speed 100–300 px/s. |
| Screen shake | Camera offset | Small 4 px, player hit 8 px, boss phase 12 px. |
| Slow motion | Timescale change | 0.3 for 0.18 s on player hit. Disabled in reduced motion. |
| Bloom | Canvas shadow + additive particles | Shadow blur 8–16 px for neon elements. |
| Colour-blind coding | Shape + color | Mote triangle, Dart arrow, Bruiser hexagon, Turret square, Seeker chevron, Bomber spiked orb. No red/green-only meaning. |
| Reduced motion | Static stars, no shake, no slow motion, fewer particles, shorter trails | Applied when `ctx.reducedMotion` is true. |
| Typography | Techno / display | `font-family: "Bahnschrift", "Orbitron", "Segoe UI", sans-serif; text-transform: uppercase; letter-spacing: 0.12em;` Headings may use `transform: skewX(-6deg);` for angular feel. |

# 4. GAMEPLAY SPEC

The player pilots the Vanta Skiff through five fixed top-down sectors. Each sector has several enemy waves, then a boss. The player moves freely with keyboard, aims with the mouse, shoots two Tier 1 weapons, dodges with `X`, and uses later-tier abilities, pickups, traps, and meta progression as they are added. If hull reaches 0, the player loses a life and the current level restarts from its snapshot. If no lives remain, the run ends in game over. Defeating the fifth and final boss, the Black Sun Sovereign, wins the game. The game is tense: telegraphed hazards, limited lives, dense projectiles, and a dark neon arena.

## 4.1 Records and rosters

### 4.1.1 Player record

| Field | Initial | Notes |
| --- | --- | --- |
| `pos` | Level spawn | 192 px, 540 px. |
| `vel` | 0, 0 | Velocity. |
| `angle` | 0 | Aim angle. |
| `maxSpeed` | 280 | px/s. |
| `acceleration` | 1800 | px/s². |
| `hull` | 100 | Current hull. |
| `maxHull` | 100 | Base. |
| `armor` | 0 | Tier 3. |
| `maxArmor` | 30 | Tier 3. |
| `armorRegen` | 1 | Tier 3. |
| `invulnTimer` | 0 | Seconds. |
| `weaponIndex` | 0 | Pulse. |
| `fireCooldown` | 0 | Seconds. |
| `switchLockout` | 0 | Seconds. |
| `dodgeTimer` | 0 | Seconds. |
| `dodgeCooldown` | 0 | Seconds. |
| `dashCharges` | 2 | Tier 3. |
| `dashRecharge` | `[8, 8]` | Tier 3. |
| `boostEnergy` | 50 | Tier 3. |
| `transformCharges` | 2 | Tier 4. |
| `transformTimer` | 0 | Tier 4. |
| `abilityCharges` | 2 | Tier 2. |
| `abilityRecharge` | `[8, 8]` | Tier 2. |
| `recallUses` | 3 | Tier 2, per level. |
| `recallTimer` | 0 | Tier 2. |
| `recallCooldown` | 0 | Tier 2. |
| `consumables` | `{ repair: 0, surge: 0, shield: 0 }` | Tier 4. |
| `equipmentInstalled` | `["redline"]` | Grows with unlocks. |
| `equipmentIndex` | 0 | Active equipment. |
| `trail` | [] | Visual trail. |

### 4.1.2 Weapon roster

| Weapon | Index | Damage | Fire interval | Projectile speed | Lifetime | Radius | Pierce | Damage type | Visual |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Pulse | 0 | 10 | 0.125 s | 900 px/s | 1.2 s | 4 px | 0 | Kinetic | Cyan short bolt |
| Ion Lance | 1 | 35 | 0.5 s | 1400 px/s | 1.0 s | 5 px | 3 | Beam | Cyan-white bolt |

### 4.1.3 Enemy roster

Base values are Normal difficulty, Level 1, Wave 1. Scaling is applied in 4.8.

| Enemy | Type | HP | Speed | Contact damage | Attack | Projectile damage | Projectile speed | Score | Radius |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| Mote | small swarm | 20 | 140 | 10 | none | 0 | 0 | 50 | 14 |
| Dart | shooter | 35 | 110 | 8 | one projectile every 1.8 s | 12 | 320 | 100 | 14 |
| Bruiser | tank | 140 | 70 | 25 | 3-way burst every 2.5 s | 15 | 320 | 250 | 24 |
| Turret | stationary | 200 | 0 | 20 | aims and fires every 1.2 s | 18 | 360 | 300 | 26 |
| Seeker | homing | 60 | 170 | 20 | none | 0 | 0 | 200 | 16 |
| Bomber | suicide | 80 | 190 | 35 | explodes on contact or after 8 s, AoE 100 px | 35 | 0 | 250 | 18 |

### 4.1.4 Boss roster

| Boss | Level | HP | Contact damage | Base score | Pattern summary |
| --- | --- | ---: | ---: | ---: | --- |
| Swarm Herald | 1 | 800 | 20 | 5000 | Radial bursts, summons Motes, phase 2 faster radials, phase 3 spiral. |
| Reef Warden | 2 | 1400 | 25 | 7500 | Rotating beams, summons Darts, phase 2 four beams, phase 3 crossing beams. |
| Cinder Tyrant | 3 | 2200 | 30 | 10000 | Fire lanes, Bomber summons, phase 2 charge dash, phase 3 spiral + lanes. |
| Hollow Queen | 4 | 3200 | 35 | 15000 | Seeker swarms, laser gates, radial rings, phase 3 expanding rings. |
| Black Sun Sovereign | 5 | 4500 | 40 | 25000 | Three phases: radial spirals, sunbeams, enrage with summons. |

### 4.1.5 Level and wave roster

| Level | Name | Waves | Enemy gates | Boss | Objective |
| --- | --- | ---: | --- | --- | --- |
| 1 | Neon Meridian | 3 | A, B, C | Swarm Herald | Clear 3 waves, destroy Herald. |
| 2 | Static Reef | 3 | A, B, C | Reef Warden | Clear 3 waves, destroy Warden. |
| 3 | Cinder Drift | 4 | A, B, C | Cinder Tyrant | Clear 4 waves, destroy Tyrant. |
| 4 | Hollow Orbit | 4 | A, B, C | Hollow Queen | Clear 4 waves, destroy Queen. |
| 5 | Black Sun Gate | 5 | A, B, C | Black Sun Sovereign | Clear 5 waves, destroy Sovereign. |

| Level | Wave | Enemy spawn composition | Trap composition |
| --- | --- | --- | --- |
| 1 | 1 | Mote × 6 | none |
| 1 | 2 | Mote × 8, Dart × 2 | none |
| 1 | 3 | Mote × 4, Dart × 3, Bruiser × 1 | none |
| 2 | 1 | Dart × 6, Mote × 4 | none |
| 2 | 2 | Mote × 8, Dart × 4, Mine × 2 | Pulse Mines |
| 2 | 3 | Bruiser × 2, Dart × 4, Mote × 6, Gate × 1 | Static Gate |
| 3 | 1 | Bruiser × 3, Dart × 5 | Mine × 2 |
| 3 | 2 | Turret × 2, Seeker × 6 | Mine × 2 |
| 3 | 3 | Turret × 1, Bruiser × 3, Bomber × 4 | Gate × 1 |
| 3 | 4 | Turret × 3, Dart × 6 | Gate × 1, Mine × 2 |
| 4 | 1 | Seeker × 8, Turret × 3 | Gate × 2 |
| 4 | 2 | Bomber × 6, Bruiser × 3 | Mine × 3 |
| 4 | 3 | Seeker × 8, Turret × 4, Dart × 4 | Gate × 1 |
| 4 | 4 | Turret × 4, Bomber × 5, Seeker × 5 | Gate × 1 |
| 5 | 1 | Seeker × 8, Bomber × 4 | Mine × 2 |
| 5 | 2 | Bruiser × 5, Turret × 4 | Gate × 1 |
| 5 | 3 | Bomber × 7, Dart × 6 | Mine × 3 |
| 5 | 4 | Bruiser × 4, Seeker × 8 | Gate × 2 |
| 5 | 5 | Turret × 4, Bomber × 5, Seeker × 6 | Gate × 2, Mine × 2 |

### 4.1.6 Collectible roster

| Collectible | Icon | Effect | Weight |
| --- | --- | --- | ---: |
| Hull Cell | Cyan cross | +20 hull, capped | 25 |
| Boost Cell | Yellow bolt | +25 boost energy, capped at 100 | 20 |
| Armor Plate | Magenta hexagon | +15 armor, capped | 15 |
| Surge Cell | Blue star | +1 Neon Burst charge, capped | 10 |
| Score Gem | Orange diamond | +250 score | 15 |
| Data Cube | White cube | +1 evolution data | 15 |

### 4.1.7 Consumable roster

| Consumable | Inventory key | Use effect |
| --- | --- | --- |
| Repair Cell | `repair` | +25 hull, capped. |
| Surge Cell | `surge` | +1 Neon Burst charge, capped. |
| Shield Cell | `shield` | +20 armor, capped. |

### 4.1.8 Trap roster

| Trap | HP | Behavior | Damage |
| --- | ---: | --- | --- |
| Pulse Mine | 15 | Charges 0.8 s, active 10 s. Explodes if player within 90 px or if shot. | 18 AoE |
| Static Gate | 30 | 1 s telegraph, 2 s active, 3 s off, 3 cycles. Beam segment 300 px. | 25 per 0.5 s tick |

### 4.1.9 Equipment roster

| Equipment id | Unlock | Active effect |
| --- | --- | --- |
| Redline | Base | +10% damage, -5% fire interval. |
| Aegis | Level 3 reward | +10 max armor, +1 armor regen per second. |
| Phase | Level 4 reward | Dash recharge 20% faster, boost energy regen +2/s. |

### 4.1.10 Evolution roster

| Stage | Data required | Effect |
| --- | ---: | --- |
| Skiff I | 0 | Base stats. |
| Skiff II | 10 | +10 max hull, +5% projectile speed. |
| Skiff III | 25 | +1 max ability charge, +10% damage, +10 max armor. |

### 4.1.11 Medal and rank roster

| Score medal | Threshold |
| --- | ---: |
| Bronze | 10,000 |
| Silver | 25,000 |
| Gold | 50,000 |
| Platinum | 100,000 |
| Diamond | 150,000 |

| Rank | Condition |
| --- | --- |
| Rookie | Reached level 1. |
| Runner | Reached level 2. |
| Ace | Reached level 3. |
| Legend | Reached level 4. |
| Star | Reached level 5 pre-boss. |
| Sovereign | Won the game. |

## 4.2 Player vehicle and movement — Tier 1

| Rule | Value |
| --- | --- |
| Player spawn | 192 px, 540 px. |
| Lives | Easy 4, Normal 3, Hard 2. |
| Hull | Max 100 base. Starts full at level start. |
| Max speed | 280 px/s. |
| Acceleration | 1800 px/s² toward target velocity. |
| Friction | `vel *= exp(-6 * dt)` when no movement input and not dodging/dashing. |
| Input | `moveUp`, `moveDown`, `moveLeft`, `moveRight`. |
| Vector normalization | Diagonal input is normalized to length 1. |
| Aim | Mouse pointer. `angle = atan2(pointerY - pos.y, pointerX - pos.x)`. |
| Bounds | Center clamped to 20 px margin. |
| Contact damage | If enemy overlaps player and enemy contact cooldown is ready, deal contact damage. |
| Invulnerability | After any player damage, 0.8 s invuln. After respawn, 3.0 s invuln. |
| Death | If hull <= 0: lose a life, clear level state to level snapshot, reset player to spawn, full hull, 3.0 s invuln. |
| Game over | If no lives remain, state becomes `gameover`. |
| Retry | Game over screen `R` retries current level, resets lives to difficulty max, score to `scoreAtLevelStart`. |
| HUD health | Shows lives pips and hull bar. |

## 4.3 Weapons and shooting — Tier 1

| Rule | Value |
| --- | --- |
| Fire input | Hold left mouse. |
| Weapon switch | `R` cycles weapon index. |
| Switch lockout | 0.2 s. |
| Muzzle offset | 24 px from player center along aim. |
| Muzzle flash | 0.05 s. |
| Pulse fire interval | 0.125 s. |
| Ion Lance fire interval | 0.5 s. |
| Projectile spawn | At muzzle offset. |
| Projectile lifetime | From weapon table. |
| Pierce | Ion Lance pierces up to 3 enemies. Pulse pierces 0. |
| Player damage multiplier | Difficulty player damage × equipment × evolution × transform. |
| Sound | `shoot_pulse` or `shoot_lance`. |

## 4.4 Dodge — Tier 1

| Rule | Value |
| --- | --- |
| Input | `X`. |
| Cooldown | 2.0 s. |
| Duration | 0.10 s. |
| Distance | 100 px. |
| Direction | Movement direction if moving; otherwise away from nearest enemy; otherwise aim direction. |
| Invulnerability | 0.08 s during dodge. |
| Velocity during dodge | 1000 px/s along direction. |
| After dodge | Velocity set to 0. |
| Failure | If cooldown active, play fail SFX. |
| Sound | `dodge`. |
| Visual | Cyan side trail, 0.15 s. |

## 4.5 Enemies — Tier 1

| Rule | Value |
| --- | --- |
| Spawn | Enemy spawns at gate position, scale-in 0.2 s, no i-frames. |
| HP | Base × level/wave/difficulty multipliers. |
| Contact | Circle overlap, 0.5 s per-enemy cooldown. |
| Contact damage | Enemy table value × difficulty damage × wave/level damage ramp. |
| Death | Explosion particles, score if Tier 2 built, possible drop if Tier 3 built. |
| Mote AI | Seek player with sinusoidal wobble. Wobble perpendicular amplitude 60 px/s, frequency 4 Hz. |
| Dart AI | Keep 260 px distance. If too close, retreat. Else strafe perpendicular at 90 px/s. Fires at player position plus 0.2 s player velocity lead. |
| Bruiser AI | Slow seek. Fires 3-way burst: spread 0.4 rad. |
| Turret AI | Stationary. Rotates toward player at max 120 deg/s. Fires single projectile. |
| Seeker AI | Homing. Max turn rate 2.4 rad/s. Lifetime 12 s. Despawn quietly. |
| Bomber AI | Accelerates toward player. Explodes if within 40 px or after 8 s. AoE 100 px. |
| Enemy projectile | Lifetime 3.0 s, speed from enemy table, damage from enemy table. |
| Enemy projectiles can be destroyed | No, except Neon Burst clears them in Tier 2. |

## 4.6 Waves and spawn points — Tier 1

| Rule | Value |
| --- | --- |
| Level start | Load level data, reset wave queue, reset traps/collectibles/enemies, snapshot run state. |
| Intermission before wave 1 | 2.0 s. |
| Intermission between waves | 2.0 s. |
| Spawn gate positions | A: 160, 120. B: 1760, 120. C: 960, 960. |
| Spawn warning | Gate glows yellow for 0.6 s before spawn. |
| Spawn interval | Easy 1.0 s, Normal 0.8 s, Hard 0.65 s. |
| Max alive enemies | Easy 10, Normal 12, Hard 14. Boss is not counted toward max alive enemies. |
| Spawn order | From level wave table. Gates are assigned in table order or evenly distributed if not specified. |
| Wave completion | All spawned enemies dead and no active traps. |
| Objective banner | Shown during intermission: “CLEAR WAVE x/y”. |
| Boss spawn | After final wave, boss warning 1.0 s, then boss spawns at center. |
| Boss defeat | Level complete. |

## 4.7 Bosses — Tier 1

Common boss rules:

| Rule | Value |
| --- | --- |
| Boss spawn | Center 960, 540. |
| Intro invuln | 1.0 s. |
| Contact damage | Boss table value. |
| Phase transition | At 66% and 33% HP where specified. |
| Phase stun | 1.5 s, boss takes +50% damage during stun. |
| Boss score | Added on death. |
| Boss death | Large explosion, 12 px shake, level complete. |

| Boss | Patterns |
| --- | --- |
| Swarm Herald | Phase 1: 12 radial projectiles every 2.0 s, speed 260. Summon 4 Motes every 10 s. Phase 2: 16 radial projectiles every 1.7 s, speed 300. Summon 6 Motes every 9 s. Phase 3: 8-arm spiral, 24 projectiles over 3.0 s, speed 320. |
| Reef Warden | Phase 1: 3 rotating beams, 30 deg/s, telegraph 0.6 s, active 2.0 s, every 4.0 s. Summon 3 Darts every 8 s. Phase 2: 4 rotating beams, 40 deg/s. Summon 4 Darts every 7 s. Phase 3: crossing beams from center, 45 deg/s, plus 2 Darts every 5 s. |
| Cinder Tyrant | Phase 1: 3 horizontal fire lanes, telegraph 0.8 s, projectile speed 400. Summon 4 Bombers every 12 s. Phase 2: adds charge dash: telegraph 0.6 s, speed 700 px/s, duration 1.2 s, cooldown 6.0 s. Phase 3: spiral plus lanes, summon 2 Bruisers and 2 Bombers every 10 s. |
| Hollow Queen | Phase 1: summon 6 Seekers every 9 s, radial ring of 16 projectiles every 4.0 s, speed 280. Phase 2: adds 3 laser gates cycling, summon 4 Bruisers once. Phase 3: expanding rings: 3 rings, each 20 projectiles, speed 320, plus Seeker summon 6 every 7 s. |
| Black Sun Sovereign | Phase 1: radial spirals, 2 arms, 30 projectiles over 4.0 s, speed 300. Summon mixed enemies every 12 s: 2 Motes, 1 Dart, 1 Bomber. Phase 2: 4 sunbeams rotating 35 deg/s, telegraph 0.6 s, active 2.5 s. Summon 2 Seekers every 8 s. Phase 3: enrage: spiral speed 360, sunbeams 50 deg/s, summon 2 Bombers every 6 s. |

## 4.8 Difficulty ramp — Tier 1

Enemy stat formulas use:

- `L` = level index 1–5.
- `W` = wave index 1–N.

| Stat | Formula / value |
| --- | --- |
| Enemy HP multiplier | `1 + (L - 1) * 0.15 + (W - 1) * 0.05` × difficulty enemy HP. |
| Enemy speed | Base speed × difficulty speed + `(L - 1) * 10` + `(W - 1) * 2`. |
| Enemy fire interval | Base interval × difficulty fire interval / `(1 + (L - 1) * 0.05 + (W - 1) * 0.02)`. |
| Enemy damage | Base damage × `(1 + (L - 1) * 0.05 + (W - 1) * 0.02)` × difficulty damage. |
| Boss HP multiplier | Difficulty enemy HP. |
| Boss damage multiplier | Difficulty damage. |

| Difficulty | Enemy HP | Enemy damage | Enemy speed | Enemy fire interval | Spawn interval | Max alive | Player lives | Player damage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Easy | 0.70 | 0.70 | 0.90 | 1.15 | 1.0 s | 10 | 4 | 1.15 |
| Normal | 1.00 | 1.00 | 1.00 | 1.00 | 0.8 s | 12 | 3 | 1.00 |
| Hard | 1.30 | 1.30 | 1.10 | 0.85 | 0.65 s | 14 | 2 | 0.90 |

## 4.9 Score — Tier 2

| Rule | Value |
| --- | --- |
| Score starts | 0. |
| Score source | Kills, trap destruction, collectibles, boss kills, level rewards. |
| Score on death | Reset to `scoreAtLevelStart`. |
| Score on retry | Reset to `scoreAtLevelStart`. |
| Final high score | Saved on game over or win. |
| Combo multiplier | Applied only in Tier 4. |

| Source | Base score |
| --- | ---: |
| Mote | 50 |
| Dart | 100 |
| Bruiser | 250 |
| Turret | 300 |
| Seeker | 200 |
| Bomber | 250 |
| Pulse Mine destroyed | 25 |
| Static Gate destroyed | 50 |
| Collectible picked up | 10 |
| Score Gem | 250 |
| Boss level 1 | 5000 |
| Boss level 2 | 7500 |
| Boss level 3 | 10000 |
| Boss level 4 | 15000 |
| Boss level 5 | 25000 |

## 4.10 Rewards — Tier 2

| Rule | Value |
| --- | --- |
| When | After each level boss death. |
| Hull | Restored to max. |
| Score bonus | Added instantly. |
| Unlock | Applied instantly and stored. |
| Next level | Starts after 2.5 s. |

| Level cleared | Score bonus | Unlock |
| --- | ---: | --- |
| 1 | 1500 | Neon Burst max charges 3. |
| 2 | 3000 | Max hull +10. |
| 3 | 4500 | Recall duration 3.0 s. Equipment Bay unlocked: Redline and Aegis installed. |
| 4 | 6000 | Phase Dash max charges 3. Phase module installed. |
| 5 | 10000 | Win. |

## 4.11 Memorize: Recall — Tier 2

| Rule | Value |
| --- | --- |
| Name | Recall. |
| Input | `M`. |
| Uses | 3 per level. |
| Cooldown | 12.0 s. |
| Duration | 2.0 s base, 3.0 s after Level 3 unlock. |
| Effect | Reveals the next 3 spawn events of the current wave as gate icons, enemy type icons, and 0.1 s timing increments. |
| If no remaining spawns | No effect, SFX fail. |
| If no uses | No effect, SFX fail. |
| Gameplay alteration | None. It only displays information. |
| Sound | `recall`. |

## 4.12 Ability: Neon Burst — Tier 2

| Rule | Value |
| --- | --- |
| Input | `Q`. |
| Max charges | 2 base, 3 after Level 1 unlock, 4 after Skiff III evolution. |
| Charge recharge | 8.0 s per charge. |
| Effect | Fires 24 radial projectiles. |
| Projectile damage | 12. |
| Projectile speed | 500 px/s. |
| Projectile lifetime | 1.0 s. |
| Radius | 300 px. |
| Clears enemy projectiles | All enemy projectiles within 300 px are removed. |
| I-frames | None. |
| Failure | If 0 charges, SFX fail. |
| Sound | `ability`. |

## 4.13 Dash — Tier 3

| Rule | Value |
| --- | --- |
| Input | `Shift`. |
| Max charges | 2 base, 3 after Level 4 unlock. |
| Charge recharge | 8.0 s per charge. Phase equipment reduces by 20%. |
| Duration | 0.18 s. |
| Distance | 220 px. |
| Velocity | 1222 px/s. |
| Direction | Movement direction if moving; otherwise aim direction. |
| Invulnerability | 0.22 s during dash. |
| After dash | Velocity set to 0. |
| Failure | If 0 charges, SFX fail. |
| Sound | `dash`. |
| Visual | Magenta phase trail. |

## 4.14 Boosts — Tier 3

| Rule | Value |
| --- | --- |
| Input | Hold `Space`. |
| Boost energy max | 100. |
| Start energy per level | 50. |
| Regen | 5.0/s when not boosting. |
| Consumption | 35.0/s while boosting. |
| Minimum to start | 5 energy. |
| Stop condition | Release input or energy reaches 0. |
| Speed effect | Max speed +35%. |
| Total speed cap | 450 px/s including boost and transform. |
| Visual | Yellow engine trail, longer player trail. |
| Sound | `boost_loop` while active. |

## 4.15 Collectibles — Tier 3

| Rule | Value |
| --- | --- |
| Drop chance per enemy death | 8%. |
| Drop chance per trap destruction | 20%. |
| Wave clear drop | 1 collectible, guaranteed. |
| Max on field | 6. |
| Lifespan | 10 s. |
| Blink | Last 3 s. |
| Pickup radius | 30 px. |
| Collection | Automatic on overlap. |
| Score | +10 per collectible. |
| Sound | `pickup`. |

Weighted spawn table:

| Type | Weight |
| --- | ---: |
| Hull Cell | 25 |
| Boost Cell | 20 |
| Armor Plate | 15 |
| Surge Cell | 10 |
| Score Gem | 15 |
| Data Cube | 15 |

## 4.16 Armour / defence — Tier 3

| Rule | Value |
| --- | --- |
| Max armor | 30 base. |
| Start armor per level | 0. |
| Regen | 1.0/s after 3.0 s without damage. |
| Damage absorption | All damage subtracts armor first. Overflow applies to hull. |
| Visual | Magenta armor bar above hull bar. |
| Hit flash | Magenta flash on armor hit. |
| Armor sources | Armor Plate +15, Shield Cell +20, Aegis equipment +10 max and +1 regen, Skiff III +10 max. |

## 4.17 Traps — Tier 3

| Trap | Rule | Value |
| --- | --- | --- |
| Pulse Mine | HP | 15. |
| Pulse Mine | Charge time | 0.8 s. |
| Pulse Mine | Active time | 10 s. |
| Pulse Mine | Explosion radius | 90 px. |
| Pulse Mine | Damage | 18. |
| Pulse Mine | Trigger | Player within 90 px while armed, or destroyed by player. |
| Static Gate | HP | 30. |
| Static Gate | Length | 300 px. |
| Static Gate | Width | 8 px. |
| Static Gate | Cycle | 1 s telegraph, 2 s active, 3 s off. |
| Static Gate | Cycles | 3. |
| Static Gate | Damage tick | 25 per 0.5 s while active. |
| Static Gate | Positions | Vertical at x 480 or 1440, horizontal at y 360 or 720, centered. |
| Trap warning | SFX `trap_warning` during telegraph. |
| Trap destruction | Score 25 for mine, 50 for gate. |

## 4.18 High scores — Tier 3

| Rule | Value |
| --- | --- |
| Save trigger | Game over or win. |
| Stored value | Best score per difficulty. |
| Display | High scores screen and end screens. |
| Storage key | `neon-swarm.highscores`. |
| Format | `{ easy: score, normal: score, hard: score }`. |

## 4.19 Consumables — Tier 4

| Rule | Value |
| --- | --- |
| Drop chance per enemy death | 5%. |
| Inventory max | 3 total consumables. |
| Use input | `E`. |
| Use priority | 1. Shield Cell if armor < max. 2. Repair Cell if hull < max. 3. Surge Cell if ability charges < max. |
| If no useful consumable | No effect, SFX fail. |
| Repair Cell | +25 hull. |
| Surge Cell | +1 ability charge. |
| Shield Cell | +20 armor. |
| Visual | Capsule icon in transient HUD text, not a permanent HUD element. |

## 4.20 Equipment — Tier 4

| Rule | Value |
| --- | --- |
| Unlock | Level 3 reward installs Redline and Aegis. Level 4 reward installs Phase. |
| Active equipment | One active module at a time. |
| Toggle input | `F`. |
| Effect scope | Only active module applies. |
| Redline | +10% damage, -5% fire interval. |
| Aegis | +10 max armor, +1 armor regen per second. |
| Phase | Dash recharge 20% faster, boost energy regen +2/s. |
| Visual | Small transient module text when toggled. |

## 4.21 Evolution — Tier 4

| Rule | Value |
| --- | --- |
| Source | Data Cubes. |
| Threshold stage 1 | 10 data. |
| Threshold stage 2 | 25 data. |
| Evolution trigger | Automatic when threshold reached. |
| Stage 1 effect | +10 max hull, +5% projectile speed. |
| Stage 2 effect | +1 max ability charge, +10% damage, +10 max armor. |
| Visual | White 1 s flash, hull outline brightens. |
| Sound | `evolve`. |
| Retry | Evolution data resets to level snapshot. |

## 4.22 Combos — Tier 4

| Rule | Value |
| --- | --- |
| Combo source | Enemy or trap kills. |
| Combo window | 2.0 s between kills. |
| Combo increment | +1 per kill. |
| Multiplier | `min(5, 1 + 0.1 * combo)`. |
| Reset | Player takes damage or combo timer expires. |
| Score application | `baseScore * multiplier`. |
| HUD | Combo counter visible when combo > 0. |
| Visual | Combo text pulses on increment. |

## 4.23 Plot and cutscenes — Tier 4

| Rule | Value |
| --- | --- |
| Plot | Kael pilots the Vanta Skiff to stop the Swarm from opening the Black Sun Gate. |
| Cutscene trigger | Before each level. |
| Duration | 3.0 s. |
| Skip | `Enter`. |
| Gameplay effect | None. |
| Visual | Dark vignette, angular text, neon underline. |

| Level | Cutscene text |
| --- | --- |
| 1 | “The Meridian is dark. The Swarm sings in static. Pilot Kael, wake the Skiff.” |
| 2 | “Reef currents carry the Warden’s pulse. Remember the pattern.” |
| 3 | “Cinders open the gate. The Tyrant tests the hull.” |
| 4 | “Hollow orbits remember your mistakes. The Queen’s eye is already on you.” |
| 5 | “Black Sun rises. One last hull between us and the Sovereign.” |

## 4.24 Damage types — Tier 4

Player damage types:

| Source | Damage type |
| --- | --- |
| Pulse | Kinetic |
| Ion Lance | Beam |
| Neon Burst | Plasma |
| Enemy projectiles | Plasma |
| Pulse Mine | Plasma |
| Static Gate | Beam |

Enemy resistance table. Values are damage multipliers.

| Enemy | Kinetic | Beam | Plasma |
| --- | ---: | ---: | ---: |
| Mote | 1.0 | 0.9 | 1.1 |
| Dart | 0.9 | 1.0 | 1.0 |
| Bruiser | 0.8 | 1.1 | 0.9 |
| Turret | 1.1 | 0.9 | 1.0 |
| Seeker | 1.0 | 1.0 | 1.0 |
| Bomber | 0.9 | 1.0 | 1.1 |
| Swarm Herald | 1.0 | 0.9 | 1.1 |
| Reef Warden | 0.9 | 1.1 | 1.0 |
| Cinder Tyrant | 1.1 | 0.9 | 1.0 |
| Hollow Queen | 1.0 | 1.0 | 1.1 |
| Black Sun Sovereign phase 1 | 1.0 | 1.0 | 1.0 |
| Black Sun Sovereign phase 2 | 1.1 | 0.9 | 1.0 |
| Black Sun Sovereign phase 3 | 1.0 | 1.0 | 1.0 |

Damage formula:

`finalDamage = baseDamage * playerDamageMultiplier * resistance`

## 4.25 Transform — Tier 4

| Rule | Value |
| --- | --- |
| Input | `T`. |
| Name | Ghost Hull. |
| Max charges | 2. |
| Charge recharge | 25.0 s. |
| Duration | 5.0 s. |
| Speed effect | +30% max speed. |
| Enemy projectile effect | Enemy projectile speed -20%. |
| Player damage effect | -25% damage. |
| Damage taken effect | -20% damage taken. |
| Visual | Hull stroke becomes magenta, ghost trail. |
| Sound | `transform`. |
| Failure | If 0 charges or already active, SFX fail. |

## 4.26 Medals, ranks, and leaderboard — Tier 4

| Rule | Value |
| --- | --- |
| Medal | Based on final score thresholds. |
| Rank | Based on level reached and win. |
| Leaderboard entry | After game over or win. |
| Leaderboard size | Top 10 local. |
| Initials | 3 A–Z characters. Default `AAA`. |
| Initials input | On high scores screen, if entry qualifies. |
| Storage key | `neon-swarm.leaderboard`. |
| Entry fields | `initials`, `score`, `level`, `rank`, `difficulty`, `timestamp`. |

## 4.27 Progression and difficulty

Run structure:

1. Title screen.
2. Player selects start.
3. Load level 1, snapshot run state.
4. Tier 4 cutscene, then 2.0 s intermission.
5. Waves spawn.
6. Final wave clear triggers boss warning.
7. Boss spawns.
8. Boss death triggers level reward.
9. Next level loads, or win if level 5.
10. If player dies with lives remaining, current level restarts from snapshot.
11. If player dies with no lives, game over.

Difficulty ramp is the level/wave/difficulty table in 4.8.

## 4.30 Feel

| Event | Effect |
| --- | --- |
| Player shot | Muzzle flash 0.05 s, small SFX, no shake. |
| Enemy hit | White hit flash 0.06 s, 4 small particles. |
| Enemy death | 16 particles, 4 px shake, score text. |
| Player hit | 8 px shake, 0.18 s slow motion at 0.3 timescale, white overlay 0.05 s, 0.8 s invuln blink. |
| Boss phase | 12 px shake, boss color flash, SFX. |
| Boss death | 24 particles, 12 px shake, 0.3 s slow motion. |
| Trap warning | 0.6–1.0 s telegraph, warning SFX. |
| Combo kill | Combo text pulse, small orange particle burst. |
| Evolution | White flash 1.0 s, slow particles. |
| Tension | Telegraphed hazards, limited lives, minor-key music, dark arena, bright enemy bullets. |

# 5. CHARACTERS

| Character | Silhouette | Animations | Facing | States needed by gameplay |
| --- | --- | --- | --- | --- |
| Vanta Skiff / Kael | Angular cyan chevron, 36 × 44 px. | Idle: engine pulse 1 Hz. Move: thrust particles. Fire: muzzle flash. Dodge: side skew. Dash: stretch to 1.2× length. Boost: elongated yellow flame. Hurt: white flash. Destroy: 0.6 s explosion. Transform: magenta ghost outline. | Nose aims at mouse pointer. Movement is independent of facing. | alive, invuln, dodging, dashing, boosting, transformed, hurt, dead. |
| Mote | Small orange triangle. | Bob: sinusoidal vertical offset. Seek: points toward player. Hit: white flash. Explode: 0.4 s scale-up fade. | Faces velocity. | alive, hit, dead. |
| Dart | Magenta arrow / dart. | Strafe: slight lateral wobble. Fire: recoil 4 px. Hit: white flash. Explode: 0.4 s scale-up fade. | Faces player. | alive, hit, dead. |
| Bruiser | Blue hexagon with inner plate. | Heavy hover: slow scale pulse 0.5 Hz. Fire: 3-way recoil. Hit: white flash. Explode: 0.6 s scale-up fade. | Faces velocity. | alive, hit, dead. |
| Turret | Yellow square base, rotating circular head. | Base idle: subtle ring pulse. Rotate: head rotates. Fire: barrel flash. Hit: white flash. Explode: 0.6 s scale-up fade. | Head faces player. | alive, hit, dead. |
| Seeker | Thin magenta/blue chevron with trail. | Home: smooth turning. Trail: 6 points. Hit: white flash. Explode: 0.3 s fade. | Faces velocity. | alive, hit, dead. |
| Bomber | Orange spiked orb. | Approach: rotation 90 deg/s. Warning: yellow pulse 0.5 s before explode. Hit: white flash. Explode: AoE flash. | Faces velocity. | alive, hit, exploding, dead. |
| Swarm Herald | 96 px spiky magenta diamond. | Idle: slow spin 10 deg/s. Fire: radial recoil. Summon: gate pulse. Phase: color shift. Dying: 1.0 s collapse. | Faces player during radial patterns. | alive, phase, stunned, hit, dying. |
| Reef Warden | 120 px blue/cyan slab. | Idle: emitter nodes pulse. Beam: rotating beam arms. Summon: node flash. Phase: color shift. Dying: slab shatter. | Static center, beams rotate. | alive, phase, stunned, hit, dying. |
| Cinder Tyrant | 140 px orange/yellow armored tank. | Idle: hull heat shimmer. Fire lanes: lane telegraph. Charge: stretch 1.3×. Phase: color shift. Dying: 1.2 s collapse. | Faces player or charge direction. | alive, phase, charging, stunned, hit, dying. |
| Hollow Queen | 160 px magenta/white crown spire. | Idle: crown rings rotate. Seeker summon: spire flash. Ring attack: expanding outline. Phase: color shift. Dying: 1.5 s collapse. | Faces player. | alive, phase, stunned, hit, dying. |
| Black Sun Sovereign | 200 px black disc with magenta/yellow corona. | Idle: corona pulse 0.25 Hz. Spiral: corona arms. Sunbeam: rotating beams. Enrage: corona speed doubles. Phase: corona color shift. Dying: 2.0 s implosion. | Static center. | alive, phase 1, phase 2, phase 3, stunned, hit, dying. |

Motion rules:

- All enemies scale in from 0 to 1 over 0.2 s on spawn.
- All enemies flash white for 0.06 s when hit.
- All enemies explode with particles and fade over 0.4 s, bosses over 1.0 s.
- Player blink during invuln: alpha toggles every 0.1 s.
- Facing is visual only; collision uses circles.

# 6. AUDIO

The builder has access to an audio API. All sounds are synthesized. No audio files are used. The music is a tense synth loop with a beat. Sound effects are short retro bleeps and noise bursts.

Music:

| Layer | Recipe | Notes |
| --- | --- | --- |
| Tempo | 120 BPM, 4/4. | Tense electronic loop. |
| Key | A minor. | Dark, driving. |
| Kick | Sine 80 Hz, pitch drops to 40 Hz over 0.1 s, on every quarter note. | Low-pass 200 Hz. |
| Bass | Square wave, 8th notes: A1, C2, E2, D2 pattern. | Low-pass 700 Hz. |
| Lead | Sawtooth 16th arpeggio: A3, C4, E4, A4. | Low-pass 1200 Hz, delay 0.25 s, low volume. |
| Hats | Noise burst 20 ms on 8th notes. | High-pass 8000 Hz. |
| Intensity | During boss fights, add a second lead an octave higher and increase hat gain by 0.2. | Controlled by `ctx.boss != null`. |
| Volume | Music default 0.8. | Master, music, sfx channels. |

SFX:

| SFX name | Recipe | When it plays |
| --- | --- | --- |
| `ui_move` | Square 800 Hz, 30 ms, low-pass 2000 Hz. | Settings option changes. |
| `ui_confirm` | Square 520 Hz to 880 Hz over 80 ms. | Enter / confirm. |
| `shoot_pulse` | Square 700 Hz to 300 Hz over 40 ms + 20 ms noise. | Pulse fire. |
| `shoot_lance` | Sawtooth 1200 Hz to 400 Hz over 90 ms + sine 220 Hz. | Ion Lance fire. |
| `enemy_hit` | Triangle 200 Hz, 20 ms, pitch down 30%. | Enemy takes damage. |
| `enemy_die` | Square 300 Hz to 50 Hz over 120 ms + noise burst. | Enemy death. |
| `player_hurt` | Sawtooth 120 Hz to 40 Hz over 150 ms + noise. | Player takes damage. |
| `explosion_small` | Noise 200 ms, band-pass 400 Hz + sine 80 Hz. | Small explosion. |
| `explosion_boss` | Noise 600 ms, low-pass 200 Hz + sub 40 Hz. | Boss death. |
| `dodge` | Triangle 400 Hz to 900 Hz over 60 ms. | Core dodge. |
| `dash` | Sine 200 Hz to 100 Hz over 100 ms + noise sweep. | Extra dash. |
| `boost_loop` | Sawtooth 80 Hz + filtered noise, gain 0.2, while active. | Boost held. |
| `ability` | Sawtooth 440 Hz to 1320 Hz over 200 ms + 8 short noise bursts. | Neon Burst. |
| `recall` | Sine 660 Hz to 1320 Hz over 100 ms, echo 0.1 s. | Recall. |
| `pickup` | Sine 880 Hz to 1760 Hz over 50 ms. | Collectible. |
| `trap_warning` | Square 220 Hz, four 100 ms beeps. | Trap telegraph. |
| `trap_hit` | Noise 80 ms + triangle 100 Hz. | Trap explodes. |
| `boss_warning` | Sawtooth 55 Hz for 1.0 s + square 220 Hz beeps. | Boss spawn. |
| `level_complete` | Square arpeggio C4, E4, G4, C5, 80 ms each. | Boss death. |
| `game_over` | Sawtooth descending A3, F3, D3, A2, 200 ms each. | Game over. |
| `evolve` | Rising sine 440 Hz to 1760 Hz over 300 ms + chime. | Evolution. |
| `transform` | Resonant filter sweep 200 Hz to 2000 Hz over 200 ms. | Transform. |
| `fail` | Square 160 Hz, 60 ms. | Failed input use. |

# 7. UX

Screens are HTML/CSS overlays. The game world is canvas. All screens use the same angular neon style. No external images are used.

HTML skeleton:

```html
<div id="game">
  <canvas id="world" width="1920" height="1080"></canvas>
  <div id="hud"></div>
  <div class="screen" id="screen-title"></div>
  <div class="screen" id="screen-pause"></div>
  <div class="screen" id="screen-settings"></div>
  <div class="screen" id="screen-gameover"></div>
  <div class="screen" id="screen-win"></div>
  <div class="screen" id="screen-highscores"></div>
</div>
```

State machine:

| State | Visible DOM | Inputs | Transitions |
| --- | --- | --- | --- |
| `title` | `#screen-title` | `Enter`: start. `H`: high scores. `S`: settings. | To `playing`, `highscores`, `settings`. |
| `pause` | `#screen-pause` | `Esc` or `Enter`: resume. `S`: settings. `Q`: quit to title. | To `playing`, `settings`, `title`. |
| `settings` | `#screen-settings` | `Esc`: back. Arrows: select. `Enter`: confirm. | To previous state. |
| `playing` | none | `Esc` or `P`: pause. Gameplay inputs active. | To `pause`. |
| `gameover` | `#screen-gameover` | `Enter`: title. `R`: retry current level. `H`: high scores. | To `title`, `playing`, `highscores`. |
| `win` | `#screen-win` | `Enter`: title. `H`: high scores. | To `title`, `highscores`. |
| `highscores` | `#screen-highscores` | `Esc`: back. `Enter`: confirm initials if prompted. Letters: initials input. | To previous state. |

Settings screen fields:

| Field | Record | Input |
| --- | --- | --- |
| Difficulty | `ctx.difficulty` | Left/right arrows or 1/2/3. |
| Reduced motion | `ctx.reducedMotion` | Up/down arrows. |
| Master volume | `ctx.volume.master` | Left/right arrows. |
| Music volume | `ctx.volume.music` | Left/right arrows. |
| SFX volume | `ctx.volume.sfx` | Left/right arrows. |
| Key remapping | `ctx.keybinds` | Select action, press new key. |

Default keybinds:

| Action | Default key |
| --- | --- |
| `moveUp` | `W` |
| `moveDown` | `S` |
| `moveLeft` | `A` |
| `moveRight` | `D` |
| `fire` | Left mouse |
| `weaponSwitch` | `R` |
| `dodge` | `X` |
| `ability` | `Q` |
| `dash` | Left `Shift` |
| `boost` | `Space` |
| `transform` | `T` |
| `recall` | `M` |
| `useConsumable` | `E` |
| `equipment` | `F` |
| `pause` | `Esc` / `P` |

HUD table:

| HUD element | Record field | When visible |
| --- | --- | --- |
| Health: lives pips | `ctx.run.lives`, `ctx.run.maxLives` | `playing`, `pause`. |
| Health: hull bar | `ctx.player.hull`, `ctx.player.maxHull` | `playing`, `pause`. |
| Health: armor bar | `ctx.player.armor`, `ctx.player.maxArmor` | Tier 3 built and armor > 0. |
| Score | `ctx.run.score` | `playing`, `pause`. Shows 0 before Tier 2. |
| Combo counter | `ctx.run.combo`, `ctx.run.comboMultiplier` | `playing`, `pause`, and `combo > 0`. Shows 0 before Tier 4. |
| Wave number | `ctx.level.name`, `ctx.wave.state`, `ctx.run.waveIndex`, level wave count | `playing`, `pause`. |

HUD layout:

- Top-left: Health panel.
- Top-center: Wave number.
- Top-right: Score and combo.
- All panels use angular clipped corners and neon borders.

# 8. DEBUG API

Debug functions reach gameplay state directly. Input functions inject player input.

| System | Function | Effect |
| --- | --- | --- |
| Player hull | `debug.setHull(value)` | Sets `ctx.player.hull`. |
| Player lives | `debug.setLives(value)` | Sets `ctx.run.lives`. |
| Player armor | `debug.setArmor(value)` | Sets `ctx.player.armor`. |
| Player boost | `debug.setBoost(value)` | Sets `ctx.player.boostEnergy`. |
| Player ability | `debug.setAbilityCharge(value)` | Sets `ctx.player.abilityCharges`. |
| Player dash | `debug.setDashCharges(value)` | Sets `ctx.player.dashCharges`. |
| Player transform | `debug.setTransformCharges(value)` | Sets `ctx.player.transformCharges`. |
| Player recall | `debug.setRecallUses(value)` | Sets `ctx.player.recallUses`. |
| Player consumables | `debug.setConsumable(type, count)` | Sets `ctx.player.consumables[type]`. |
| Player equipment | `debug.setEquipment(index)` | Sets active equipment. |
| Evolution | `debug.setEvolutionData(value)` | Sets `ctx.run.evolutionData`. |
| Score | `debug.setScore(value)` | Sets `ctx.run.score`. |
| Combo | `debug.setCombo(value)` | Sets `ctx.run.combo` and multiplier. |
| Wave | `debug.setWave(index)` | Loads current level wave. |
| Level | `debug.setLevel(index)` | Loads level. |
| Enemy | `debug.spawnEnemy(type, count)` | Spawns enemies at nearest gate. |
| Boss | `debug.spawnBoss(levelIndex)` | Spawns boss. |
| Clear enemies | `debug.clearEnemies()` | Removes enemies and boss. |
| Projectile | `debug.spawnProjectile(kind, count)` | Spawns player or enemy projectile. |
| Collectible | `debug.addCollectible(type)` | Spawns collectible at player position. |
| Trap | `debug.addTrap(type)` | Spawns trap at fixed trap anchor. |
| Effects | `debug.shake(mag)` | Triggers screen shake. |
| Effects | `debug.slowMo(duration, scale)` | Triggers slow motion. |
| Time | `debug.setTimeScale(value)` | Sets `ctx.clock.timescale`. |
| RNG | `debug.seed(value)` | Sets `ctx.rand.seed`. |
| Input press | `debugInput.press(action)` | Simulates key press. |
| Input hold | `debugInput.hold(action, ms)` | Holds action for milliseconds. |
| Input release | `debugInput.release(action)` | Releases action. |
| Pointer | `debugInput.setPointer(x, y)` | Sets mouse aim position. |
| Move | `debugInput.setMove(x, y)` | Sets movement vector. |

# 9. TESTS

| Tier | Test | Expected result |
| --- | --- | --- |
| Tier 1 | Fixed loop test | Simulation steps at 60 Hz. Timers use scaled dt. |
| Tier 1 | Player movement test | Player moves with remapped keys, stays in bounds, velocity decays when idle. |
| Tier 1 | Aim and fire test | Mouse aim sets player angle. Holding fire spawns correct weapon projectiles at correct interval. |
| Tier 1 | Weapon switch test | `R` cycles Pulse and Ion Lance with 0.2 s lockout. |
| Tier 1 | Dodge test | `X` triggers 100 px dodge, 0.08 s i-frames, 2.0 s cooldown. |
| Tier 1 | Enemy spawn test | Enemies spawn from gates after 0.6 s warning and obey max alive count. |
| Tier 1 | Enemy AI test | Mote seeks, Dart shoots, Bruiser 3-way, Turret rotates, Seeker homes, Bomber explodes. |
| Tier 1 | Wave completion test | Wave completes when all spawned enemies are dead and no active traps remain. |
| Tier 1 | Boss fight test | Boss spawns after final wave, changes phase at thresholds, and dies when HP is 0. |
| Tier 1 | Level progression test | Defeating level boss advances to next level. Level 5 boss triggers win. |
| Tier 1 | Life loss test | Hull 0 loses a life and restarts current level from snapshot. |
| Tier 1 | Game over test | Hull 0 with no lives enters game over. Retry resets current level and lives. |
| Tier 1 | Difficulty test | Easy/Normal/Hard change lives, enemy HP, damage, speed, fire rate, spawn interval. |
| Tier 1 | Accessibility test | Reduced motion disables shake/slow motion/long trails. Key remapping changes input. |
| Tier 1 | Screen test | Title, pause, settings, game over, win, high scores screens navigate correctly. |
| Tier 1 | Audio test | Correct SFX trigger on fire, hit, death, player hurt, boss warning. Music starts/stops. |
| Tier 2 | Score test | Killing enemies adds base score. Score resets to level snapshot on death. |
| Tier 2 | Reward test | Level clear adds score bonus, full hull, and correct unlock. |
| Tier 2 | Recall test | `M` reveals next 3 spawn events, consumes a use, respects cooldown. |
| Tier 2 | Ability test | `Q` fires 24 projectiles, clears enemy projectiles in 300 px, consumes charge. |
| Tier 2 | Unlock test | Level unlocks persist and apply to ability, hull, Recall, and dash later. |
| Tier 3 | Dash test | `Shift` triggers 220 px dash, 0.22 s i-frames, charge recharge. |
| Tier 3 | Boost test | Holding `Space` drains boost, increases speed, stops at 0. |
| Tier 3 | Collectible test | Drops spawn by chance/weight, expire after 10 s, apply correct effect on pickup. |
| Tier 3 | Armor test | Armor absorbs damage before hull, regenerates after 3 s, caps at max. |
| Tier 3 | Trap test | Mines charge and explode. Gates telegraph, activate, and deal tick damage. |
| Tier 3 | High score test | Best score per difficulty saves and displays. |
| Tier 4 | Consumable test | `E` uses best consumable by priority and caps effects. |
| Tier 4 | Equipment test | `F` cycles equipment and applies only active module effects. |
| Tier 4 | Evolution test | Data thresholds trigger stage 1 and stage 2 stat changes. |
| Tier 4 | Combo test | Kills within 2 s increase multiplier, damage resets combo. |
| Tier 4 | Damage type test | Enemy resistances modify final damage according to table. |
| Tier 4 | Cutscene test | Cutscene plays before level and skips with `Enter`. |
| Tier 4 | Transform test | `T` applies Ghost Hull effects for 5 s and consumes charge. |
| Tier 4 | Medal/rank test | Final score and level produce correct medal and rank. |
| Tier 4 | Leaderboard test | Qualifying score prompts initials and saves top 10 entry. |

# 10. BUILD ORDER

1. Scaffold HTML/CSS/canvas, fixed 60 Hz loop, global context, seeded RNG.
2. Build input system, remappable keys, mouse aim, settings persistence.
3. Build player vehicle: movement, aim, hull, lives, respawn, game over.
4. Build weapons and projectile system with Pulse and Ion Lance.
5. Build enemy system with six enemy types, contact damage, and AI.
6. Build spawn gates, wave spawner, wave completion, and level flow.
7. Build bosses with five patterns and phases.
8. Build difficulty ramp, lives, retries, and win/game over flow.
9. Build Tier 1 HUD, screens, base audio/music/SFX, neon visuals, and effects.
10. Build Tier 2: score, rewards, Recall, Neon Burst, unlocks.
11. Build Tier 3: dash, boosts, collectibles, armor, traps, high scores.
12. Build Tier 4: consumables, equipment, evolution, combos, damage types, plot/cutscenes, transform, medals/ranks, leaderboard.
13. Wire debug API and headless tests to each tier.
14. Validate accessibility: reduced motion, colour-blind shapes, key remapping, difficulty.
15. Balance pass using test harness and debug functions.

# 11. DEFINITION OF DONE

## Tier 1 done

High level: A player can start from the title, play all five levels with core mechanics only, win by defeating the final boss, or lose all lives and reach game over. Tier 1 uses final core numbers and is visually/audio-complete in the chosen style.

- [ ] Fixed 60 Hz loop runs with clamped accumulator.
- [ ] Global context contains all required fields.
- [ ] Player moves with remappable keys and respects arena bounds.
- [ ] Mouse aim rotates ship and projectiles fire toward pointer.
- [ ] Pulse and Ion Lance fire with correct damage, interval, speed, lifetime, pierce.
- [ ] `R` switches weapons with 0.2 s lockout.
- [ ] `X` core dodge works with 100 px distance, 0.08 s i-frames, 2.0 s cooldown.
- [ ] Six enemy types exist with correct base stats and AI.
- [ ] Enemies spawn from gates with 0.6 s warning and max alive limits.
- [ ] Waves complete when enemies are dead and no active traps remain.
- [ ] Five levels load with correct wave tables.
- [ ] Five bosses spawn, phase, and die with correct patterns.
- [ ] Difficulty ramp applies level, wave, and difficulty multipliers.
- [ ] Hull 0 loses a life and restarts current level from snapshot.
- [ ] No lives remaining causes game over.
- [ ] Retry current level works from game over.
- [ ] Defeating final boss causes win.
- [ ] HUD shows health, score placeholder 0, combo placeholder 0, wave number.
- [ ] Screens: title, pause, settings, game over, win, high scores navigate.
- [ ] Settings include difficulty, reduced motion, key remapping, volume.
- [ ] Reduced motion disables shake, slow motion, star drift, long trails.
- [ ] Colour-blind safe palette and shape coding are used.
- [ ] Neon synthwave visuals, grid, stars, trails, bloom, particles are present.
- [ ] Synth loop music plays during gameplay and stops on non-playing states.
- [ ] Retro SFX play for fire, hit, death, player hurt, boss warning, UI.

## Tier 2 done

High level: Supporting systems are added without changing core rules. Score, rewards, Recall, Neon Burst, and unlocks work.

- [ ] Score increments from enemies, traps, collectibles, bosses, and rewards.
- [ ] Score resets to level snapshot on death and retry.
- [ ] Level rewards apply score bonus, full hull, and unlock.
- [ ] Recall reveals next 3 spawn events, uses 3/level, has 12 s cooldown.
- [ ] Recall duration is 2 s base and 3 s after Level 3 unlock.
- [ ] Neon Burst fires 24 radial projectiles, deals 12 damage, clears enemy projectiles within 300 px.
- [ ] Neon Burst charges max 2 base, 3 after Level 1 unlock, recharge 8 s.
- [ ] Unlocks persist across level restarts and apply correctly.
- [ ] HUD score displays real score.

## Tier 3 done

High level: First extra band works: dash, boosts, collectibles, armor, traps, high scores.

- [ ] `Shift` dash works with 220 px distance, 0.22 s i-frames, charge system.
- [ ] Dash charges max 2 base, 3 after Level 4 unlock.
- [ ] Holding `Space` boosts, drains energy, caps speed, stops at 0.
- [ ] Collectibles spawn by chance, have weights, expire, and apply effects.
- [ ] Armor absorbs damage before hull, regenerates after 3 s, caps at max.
- [ ] Pulse Mines charge, arm, explode, and can be destroyed.
- [ ] Static Gates telegraph, activate, tick damage, cycle, and can be destroyed.
- [ ] High score best per difficulty saves and displays.
- [ ] HUD armor bar appears when armor exists.

## Tier 4 done

High level: Full extra band works: consumables, equipment, evolution, combos, damage types, plot/cutscenes, transform, medals/ranks, leaderboard.

- [ ] Consumables drop, store up to 3, and `E` uses by priority.
- [ ] Equipment unlocks at Levels 3 and 4, `F` cycles active module, effects apply only to active module.
- [ ] Data Cubes track evolution and trigger Skiff II at 10 data and Skiff III at 25 data.
- [ ] Evolution stat changes apply correctly.
- [ ] Combo increments within 2 s, multiplier max ×5, resets on damage or timeout.
- [ ] Damage type resistances modify damage according to table.
- [ ] Pre-level cutscenes play for 3 s and skip with `Enter`.
- [ ] `T` transform applies Ghost Hull effects for 5 s with charge system.
- [ ] Final score produces correct medal.
- [ ] Level reached produces correct rank.
- [ ] Qualifying score prompts 3-letter initials and saves leaderboard top 10.
- [ ] High scores screen shows high score and leaderboard data.

# A. SANITY

| Check | Result | Notes |
| --- | --- | --- |
| All required section headings present | Valid | Sections 0 through A are present in order. |
| All high-level decisions from prompt included | Valid | Scope, decisions, tiers, gameplay, visuals, audio, UX, and accessibility cover them. |
| Core mechanics are Tier 1 | Valid | enemies, shoot, weapons, dodge, waves, vehicles, fly, steer, aim, spawn points, bosses, objectives, difficulty ramp are all Tier 1. |
| Supporting mechanics are Tier 2 | Valid | score, rewards, memorize, abilities, unlocks are Tier 2. |
| Extra mechanics are Tier 3+ | Valid | dash, boosts, collectibles, armour, high scores, traps are Tier 3; consumables, equipment, evolution, combos, plot, damage types, cutscenes, transform, medals/ranks, leaderboard are Tier 4. |
| No unlisted core system added | Valid | Lives are part of failure. Retry is failure handling. Volume is settings, not a gameplay system. |
| “Transform” included | Valid | Added in 4.25 and Tier 4. |
| “Memorize” has named input | Valid | Recall uses `M`. |
| “Dodge” and “dash” are distinct | Valid | Core dodge `X` is small/cooldown-based. Extra dash `Shift` is larger/charge-based. |
| HUD list is exact | Valid | Health, score, combo counter, wave number. Lives and armor are shown inside health. |
| Lives do not create a separate HUD element | Valid | Lives pips are part of the health HUD element. |
| Score/combo HUD fields before their tiers | Valid | Display 0 until Tier 2/Tier 4 logic exists. |
| High scores screen requirement vs extra tier | Valid | Screen shell exists in Tier 1; high score data is Tier 3; leaderboard data is Tier 4. |
| Under 30 minutes | Valid | 5 levels with 19 waves and 5 bosses, target 22–28 minutes. |
| Final boss win condition | Valid | Level 5 boss is final boss; death wins the game. |
| Top-down 2D fixed camera | Valid | Fixed 1920 × 1080 arena, no scroll. |
| Real-time with slow motion effect | Valid | Timescale is real-time scaled; slow motion is a timed effect. |
| Colour-blind safe palette | Valid | No red/green-only coding; shapes used; cyan/magenta/yellow/orange/blue/white. |
| Reduced motion implemented | Valid | Disables shake, slow motion, star drift, long trails, high particles. |
| Remappable keys | Valid | Settings includes key remapping for all keyboard actions. |
| Difficulty options | Valid | Easy/Normal/Hard with concrete stat changes. |
| Audio fully synthesized | Valid | Music and SFX use oscillators/noise, no files. |
| Contracts include global fields and module functions | Valid | Sections 2.2 and 2.3 list required fields/functions. |
| Debug API covers systems and inputs | Valid | Section 8 lists state functions and input injection. |
| Tests align with definition of done | Valid | Section 9 tests map to Tier 1–4 done checkboxes. |
| Numbers carried consistently | Valid | Player speed 280, dodge 100 px, dash 220 px, boost +35%, armor 30, combo max ×5, evolution 10/25 data. |
| Initial error: transform missing | Fixed | Added transform system, tier, tests, and done checkbox. |
| Initial error: lives could become extra HUD element | Fixed | Folded lives into health HUD element. |
| Initial error: score could be mistaken as Tier 1 because HUD shows it | Fixed | Score HUD shows 0 until Tier 2; scoring logic is Tier 2. |
