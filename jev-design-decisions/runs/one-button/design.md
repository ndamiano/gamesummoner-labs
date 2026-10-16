# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| A roguelike with one button. What you do is decided by how fast you press it. | Sections 4.1, 7, 8 |
| `dimension: 2d` | Section 1.1, Section 3 |
| `camera: top-down` | Section 1.1, Section 3 |
| `players: single player` | Section 0.1, Section 4 |
| `time model: real-time` | Section 1.2 |
| `movement model: free movement` | Section 4.2 |
| `session shape: endless` | Section 4.7 |
| `failure: permadeath, start a new run` | Section 4.8 |
| `tone: tense` | Sections 3, 4, 6 |
| `size: one screen, a few minutes` | Section 1.1, Section 3, Section 4 |
| `win/lose: ['survive as long as possible']` | Section 4.6, Section 4.8 |
| `systems: combat, survival, creatures, hazards, score and records, waves and spawning` | Section 4 |
| `system parts: combat: enemies, player health; hazards: traps, environmental damage; score and records: score, combos, high scores, leaderboard; waves and spawning: waves, spawn points, difficulty ramp` | Section 4.3, Section 4.4, Section 4.5, Section 4.6, Section 4.7 |
| `art style: pixel art: low-resolution sprites with visible square pixels and a limited palette` | Section 3 |
| `palette: dark: mostly black with a few bright accents` | Section 3 |
| `typography: pixel font: blocky bitmap letters` | Section 3, Section 7 |
| `music: chiptune: retro console bleeps` | Section 6 |
| `sound effects style: retro bleeps: synthesized chip sounds` | Section 6 |
| `screens: title, game over, high scores` | Section 7 |
| `hud: health, score, timer, combo counter, wave number` | Section 7 |
| `effects: screen shake, particles, hit flash, trails` | Section 3, Section 4.9 |
| `accessibility: colour-blind safe palette, reduced motion` | Section 3, Section 4.9, Section 7 |

## 0.2 Decisions

| Decision | Value / Ruling | Why |
| --- | --- | --- |
| Core premise | One physical press is the only gameplay input. Press speed, measured as the interval since the previous press, selects the action. | Directly implements “what you do is decided by how fast you press it.” |
| Input surface | The whole playfield is the button. Pointer press/tap provides a press plus an aim point. Keyboard Space is also the button and uses the last pointer position as aim; if none exists, it uses screen center. | Keeps the game to one button while still enabling top-down free movement. Aim is part of the same press event, not a second control. |
| Dimension | 2D top-down fixed arena. | Matches requested dimension and camera. |
| Camera | Fixed. No scrolling, no zoom, no camera follow. | Required by “one screen.” |
| Players | Single player only. | Matches requested players. |
| Time model | Real-time fixed-step simulation at 60 Hz. | Keeps timing stable for press-speed categories and hazard damage. |
| Movement model | Free continuous movement toward the aim point, initiated by slow presses. | Satisfies free movement without adding arrow keys or a second button. |
| Session shape | Endless waves. No final wave, no win state. | Matches endless session and “survive as long as possible.” |
| Failure | Player health 0 ends the run. Restart creates a fresh run. | Matches permadeath and new-run restart. |
| Tone | Dark arena, sparse bright sprites, short i-frames, no healing, close-range traps and enemies. | Creates tense, high-stakes play. |
| Size | Internal render size 480 × 270 px, scaled integer-only to the browser window. | One screen, pixel art with visible square pixels. |
| Win/lose | Lose when player health is 0. Score is survival time, kills, traps avoided, and wave progression. | Matches “survive as long as possible.” |
| Systems | Exactly: combat, survival, creatures, hazards, score and records, waves and spawning. No pickups, upgrades, inventory, dialogue, shop, pause, or difficulty selection. | The requested system list is final. |
| Combat parts | Enemies, player health. | Matches system parts. |
| Hazard parts | Traps, environmental damage. | Matches system parts. |
| Score parts | Score, combos, high scores, local leaderboard. | Matches system parts. |
| Wave parts | Waves, spawn points, difficulty ramp. | Matches system parts. |
| Art style | Pixel art, low-resolution sprites, visible square pixels, limited palette. | Matches requested art style. |
| Palette | Mostly black with bright accents. No red/green-only identification. | Matches palette and colour-blind safety. |
| Typography | Pixel font. Primary: `Press Start 2P` or equivalent pixel webfont. Fallback: monospace. No proportional font. | Matches requested typography while keeping UI HTML/CSS-only. |
| Music | Synthesized chiptune loop using WebAudio. | Matches requested music. |
| Sound effects | Synthesized retro bleeps using WebAudio. | Matches requested SFX style. |
| Screens | Title, Game Over, High Scores. | Matches requested screens. |
| HUD | Health, score, timer, combo counter, wave number. | Matches requested HUD. |
| Effects | Screen shake, particles, hit flash, trails. | Matches requested effects. |
| Accessibility | Colour-blind safe palette and reduced motion. Reduced motion is enabled automatically by `prefers-reduced-motion: reduce` or `?rm=1`. | Matches requested accessibility. |
| Internal resolution | 480 × 270 px. | Small enough to feel one-screen, large enough for readable pixel sprites. |
| Display scaling | CSS `image-rendering: pixelated`; integer scale only when possible. | Preserves visible square pixels. |
| Fixed step | 60 Hz, `dt = 1 / 60` second. | Stable timing for input categories, cooldowns, hazards, and tests. |
| Random source | One seeded PRNG per run: mulberry32. Default seed from current time; tests may inject a seed. | Deterministic gameplay and tests. |
| Player identity | The player is “The Warden,” a lone maintenance beacon trapped in a collapsing signal grid. | Gives a concrete protagonist without adding narrative systems. |
| Pickups | None. | Pickups were not included in the final system parts, so adding them would violate the fixed system list. |
| Healing | None. | Keeps survival tense and avoids an unrequested healing system. |
| Player health | 100 HP. No regen. 0.5 s invulnerability after any discrete damage. | Keeps runs short, tense, and readable. |
| Input categories | Slow: ≥ 750 ms = move. Medium: 350–749 ms = strike. Fast: 150–349 ms = dash. Frantic: < 150 ms = frenzy. | Gives four distinct actions from press speed alone. |
| First press | Treated as 1000 ms interval, therefore STEP. | Avoids ambiguous first input. |
| Enemy roster | Mote, Shard, Wisp, Golem. | Four silhouettes are enough for top-down one-screen survival without bloat. |
| Trap roster | Spike, Laser, Acid. | Covers discrete damage, continuous beam damage, and slowing environmental damage. |
| Wave length | 20.0 s spawn window per wave. Wave ends when all enemies die after the window. | Produces short, escalating pressure. |
| Intermission | 3.0 s between waves. | Gives a brief breath without breaking tense pacing. |
| High scores | Local top 10 in `localStorage`. No name input. | Keeps the one-button promise and avoids extra UI input. |
| Expected run length | Casual death 60–180 s. Skilled death 180–360 s. | Matches “a few minutes.” |

## 0.3 Tiers

| Tier | Name | Contains | Exit intent |
| --- | --- | --- | --- |
| T1 | Minimal viable game | Fixed-step loop, title/game-over screens, one-button input, STEP and STRIKE actions, player health, Mote enemies, wave spawning, score/timer/wave/health HUD, local high score top 1, basic pixel visuals, basic SFX, permadeath. | A playable one-button survival loop exists. |
| T2 | Full action and danger | DASH, FRENZY, combo system, all enemy types, all trap types, difficulty ramp, screen shake, particles, hit flash, trails, local high score top 10, game-over stats. | The full press-speed fantasy and hazard pressure exist. |
| T3 | Polish and accessibility | Reduced motion support, colour-blind safe verification, audio layering, high-score persistence across reloads, input feedback, wave banners, best combo/wave records, defensive edge-case handling. | The game feels finished, accessible, and robust. |

---

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Unit / Quantity | Value | Notes |
| --- | --- | --- |
| Internal render width | `480` px | Fixed. No camera scrolling. |
| Internal render height | `270` px | Fixed. No camera scrolling. |
| Axis | X right, Y down. | Top-down 2D. |
| Origin | Top-left of internal canvas is `(0, 0)`. | All coordinates are internal pixels. |
| Playable area | `x: 8` to `472`, `y: 8` to `262`. | 8 px wall inset. |
| Playable width | `464` px. |  |
| Playable height | `254` px. |  |
| Fixed step | `1 / 60` second. | 60 Hz. |
| Frame delta | `dt` in seconds. | All speeds are px/s. |
| Speed | px/s. | Player, enemies, bolts. |
| Distance | px. | Collision radii, trap sizes, dash distance. |
| Health | Unitless HP. | Player max 100. |
| Damage | Unitless HP damage. | Discrete or per-second rate. |
| Score | Integer points. | Displayed as integer. |
| Time | Seconds. | HUD displays `mm:ss`. |
| Press interval | Milliseconds. | `performance.now()` timestamps. |
| Angle | Radians. | `0` points right, `π/2` points down. |
| Player radius | `6` px. |  |
| Bolt radius | `2` px. |  |
| Enemy radius | Mote `4`, Shard `5`, Wisp `5`, Golem `8` px. |  |
| Trap sizes | See Section 4.5. |  |
| Sprite scale | 1 internal pixel = 1 square. | All sprites are drawn at integer coordinates. |

## 1.2 Important conventions

- Use a fixed-step loop. Render may run on `requestAnimationFrame`, but gameplay advances in exact `1 / 60` second steps.
- Clamp the accumulator so a dropped frame adds no more than `0.25` seconds of catch-up.
- Use one seeded PRNG per run. Do not call `Math.random()` directly in gameplay, spawning, traps, enemy behaviour, or score logic.
- Default run seed: `Math.floor(Date.now() % 2147483647)`. Tests must be able to set `game.runSeed`.
- The only gameplay input is a primary press: pointerdown on the canvas or `keydown` for Space. Ignore key repeat, secondary pointer buttons, touch gestures, mouse movement, arrow keys, WASD, and gamepad input.
- The pointer press location is part of the same one-button press. It is not an extra button.
- For Space with no previous pointer position, use the center of the internal canvas: `(240, 135)`.
- Do not add a camera. The entire arena is always visible.
- Clamp player and enemy positions to the playable area.
- Player and enemies are non-physical. They do not block each other. Contact applies damage based on rules and i-frames.
- Projectiles do not collide with walls until they leave the playable area or expire.
- All damage, spawning, trap state changes, and score updates happen in gameplay modules, not render modules.
- Render modules only read `game` and draw.
- Use `localStorage` only for high scores. Wrap all storage access in `try/catch`.
- Create WebAudio only after the first user gesture. If WebAudio is unavailable, the game must continue silently.
- Reduced motion is read once at startup:
  - `window.matchMedia('(prefers-reduced-motion: reduce)').matches`
  - or URL query `?rm=1`
- Colour-blind safety is always on. Do not identify enemy type or trap state by colour alone. Use shape and animation.
- All UI text is uppercase where possible and uses the pixel font class.

---

# 2. CONTRACTS

## 2.1 Module layout

| Module / File | Responsibility |
| --- | --- |
| `index.html` | Canvas, HUD DOM, screen overlays, CSS link, main script. |
| `css/style.css` | Layout, pixel font, HUD, screens, hidden states, pixelated canvas. |
| `src/config.js` | All numeric constants from this spec. |
| `src/rng.js` | Seeded PRNG. |
| `src/input.js` | One-button input, press interval, aim, category. |
| `src/player.js` | Player state, STEP, STRIKE, DASH, FRENZY, health. |
| `src/enemies.js` | Enemy roster, enemy updates, enemy damage, enemy death. |
| `src/projectiles.js` | Bolt creation, movement, collision. |
| `src/hazards.js` | Trap creation, trap cycles, environmental damage, trap disable. |
| `src/waves.js` | Wave state, composition, spawning, difficulty ramp, intermission. |
| `src/score.js` | Score, combo, high scores, records. |
| `src/effects.js` | Screen shake, particles, hit flash, trails. |
| `src/audio.js` | WebAudio init, SFX, music. |
| `src/ui.js` | Screen state, HUD DOM updates, high-score list. |
| `src/render.js` | Canvas drawing only. |
| `src/main.js` | Bootstrap, state machine, fixed-step loop, run lifecycle. |
| `src/debug.js` | Debug API functions. |

## 2.2 Global context

The global object is `game`.

| Field | Type | Purpose |
| --- | --- | --- |
| `game.state` | string | `'BOOT'`, `'TITLE'`, `'PLAYING'`, `'GAME_OVER'`, `'HIGH_SCORES'`. |
| `game.time` | number | Run elapsed seconds while `PLAYING`. |
| `game.runSeed` | number | Seed for the current run PRNG. |
| `game.rng` | object | Seeded PRNG with `int`, `float`, `pick`. |
| `game.settings.reducedMotion` | boolean | Accessibility flag. |
| `game.settings.volume` | number | Master audio volume, `0.0` to `1.0`. |
| `game.settings.colorBlindSafe` | boolean | Always `true`. Documented for render checks. |
| `game.player` | object | Player state. |
| `game.enemies` | array | Active enemy records. |
| `game.bolts` | array | Active bolt records. |
| `game.hazards` | array | Active trap records. |
| `game.particles` | array | Visual particles. |
| `game.score.value` | number | Current integer score. |
| `game.score.lastWholeSecond` | number | Used to award +1 per whole second. |
| `game.combo.value` | number | Current combo, `0` to `10`. |
| `game.combo.max` | number | Always `10`. |
| `game.combo.timer` | number | Seconds until first combo decay step. |
| `game.combo.best` | number | Highest combo this run. |
| `game.wave.number` | number | Current wave, starts at `1`. |
| `game.wave.state` | string | `'INTERMISSION'`, `'SPAWNING'`, `'ACTIVE'`, `'CLEARING'`. |
| `game.wave.timer` | number | Seconds remaining in current wave state. |
| `game.wave.activeTimer` | number | Seconds remaining in the 20 s spawn window. |
| `game.wave.nextExtraSpawn` | number | Seconds until next extra mid-wave spawn. |
| `game.input.lastPressMs` | number | Last gameplay press timestamp. |
| `game.input.lastAim` | object | `{ x, y }` last aim point. |
| `game.input.facing` | number | Last player facing angle. |
| `game.effects.shakeTime` | number | Remaining screen shake seconds. |
| `game.effects.shakeAmp` | number | Screen shake amplitude px. |
| `game.effects.flashTime` | number | Remaining global hit-flash seconds. |
| `game.ui.highScores` | array | Saved high score entries. |
| `game.ui.lastRun` | object | `{ score, wave, time, combo, newHighScore, rank }`. |
| `game.ui.newHighScore` | boolean | Whether current run made top 10. |
| `game.ui.rank` | number | High-score rank, `-1` if not in list. |

Player record:

| Field | Type | Purpose |
| --- | --- | --- |
| `game.player.x` | number | Player X. |
| `game.player.y` | number | Player Y. |
| `game.player.vx` | number | Horizontal velocity. |
| `game.player.vy` | number | Vertical velocity. |
| `game.player.health` | number | Current HP. |
| `game.player.maxHealth` | number | Always `100`. |
| `game.player.iframes` | number | Remaining invulnerability seconds. |
| `game.player.stepTarget` | object | `{ x, y }` STEP aim. |
| `game.player.stepTimer` | number | Remaining STEP seconds. |
| `game.player.dashDir` | object | `{ x, y }` normalized dash direction. |
| `game.player.dashTimer` | number | Remaining DASH seconds. |
| `game.player.dashCd` | number | Remaining DASH cooldown seconds. |
| `game.player.strikeCd` | number | Remaining STRIKE cooldown seconds. |
| `game.player.frenzyCd` | number | Remaining FRENZY cooldown seconds. |
| `game.player.facing` | number | Player facing angle. |
| `game.player.alive` | boolean | `false` when health ≤ 0. |
| `game.player.dashNearMissIds` | array | Enemy IDs already scored as near misses for current dash. |

Enemy record:

| Field | Type | Purpose |
| --- | --- | --- |
| `id` | number | Unique integer. |
| `type` | string | `'MOTE'`, `'SHARD'`, `'WISP'`, `'GOLEM'`. |
| `x` | number | Position X. |
| `y` | number | Position Y. |
| `vx` | number | Velocity X. |
| `vy` | number | Velocity Y. |
| `hp` | number | Current HP. |
| `maxHp` | number | Maximum HP for this wave. |
| `radius` | number | Collision radius. |
| `speed` | number | Base speed before wave scaling. |
| `damage` | number | Contact damage. |
| `score` | number | Base kill score. |
| `state` | string | `'SPAWN_WARN'`, `'NORMAL'`, `'CHARGE'`, `'DASH'`, `'STUN'`, `'HIT'`. |
| `stateTimer` | number | Seconds in current state. |
| `attackTimer` | number | Time until next enemy attack behaviour. |
| `wobblePhase` | number | For Mote wobble. |
| `hitFlash` | number | Remaining hit-flash seconds. |
| `dead` | boolean | Remove when true. |

Bolt record:

| Field | Type | Purpose |
| --- | --- | --- |
| `id` | number | Unique integer. |
| `x` | number | Position X. |
| `y` | number | Position Y. |
| `vx` | number | Velocity X. |
| `vy` | number | Velocity Y. |
| `radius` | number | Always `2`. |
| `damage` | number | Always `12`. |
| `life` | number | Remaining seconds. |

Hazard record:

| Field | Type | Purpose |
| --- | --- | --- |
| `id` | number | Unique integer. |
| `type` | string | `'SPIKE'`, `'LASER'`, `'ACID'`. |
| `x` | number | Center X. |
| `y` | number | Center Y. |
| `w` | number | Width for spike/laser. |
| `h` | number | Height for spike/laser. |
| `radius` | number | Radius for acid. |
| `orientation` | string | `'H'`, `'V'`, or `'NONE'`. |
| `state` | string | `'OFF'`, `'WARNING'`, `'ACTIVE'`. |
| `stateTimer` | number | Seconds remaining in state. |
| `life` | number | Seconds until trap despawns. |
| `disabledTimer` | number | Seconds remaining in FRENZY-disabled state. |

Particle record:

| Field | Type | Purpose |
| --- | --- | --- |
| `x` | number | Position X. |
| `y` | number | Position Y. |
| `vx` | number | Velocity X. |
| `vy` | number | Velocity Y. |
| `life` | number | Remaining seconds. |
| `maxLife` | number | Initial seconds. |
| `color` | string | Palette colour. |
| `size` | number | Pixel size. |

## 2.3 Module specifics

| Module | Exported functions / fields | Required behaviour |
| --- | --- | --- |
| `src/rng.js` | `createRNG(seed)` | Returns `{ state, int(min, max), float(min, max), pick(arr) }`. |
| `src/rng.js` | `RNG.int(min, max)` | Inclusive integer. |
| `src/rng.js` | `RNG.float(min, max)` | Float in `[min, max)`. |
| `src/rng.js` | `RNG.pick(arr)` | Random array element. |
| `src/input.js` | `init(canvas)` | Bind pointerdown and Space. |
| `src/input.js` | `categoryFor(intervalMs)` | Returns `'STEP'`, `'STRIKE'`, `'DASH'`, `'FRENZY'`. |
| `src/input.js` | `press(x, y, nowMs)` | Records aim and calls gameplay callback. |
| `src/input.js` | `lastAim()` | Returns `{ x, y }`. |
| `src/player.js` | `reset(x, y)` | Set player to start values. |
| `src/player.js` | `update(dt)` | Advance STEP, DASH, cooldowns, i-frames. |
| `src/player.js` | `step(aim)` | Start/update STEP. |
| `src/player.js` | `strike(aim)` | Fire bolt if cooldown ready. |
| `src/player.js` | `dash(aim)` | Start dash if cooldown ready. |
| `src/player.js` | `frenzy()` | Apply FRENZY if combo and cooldown allow. |
| `src/player.js` | `addDamage(amount)` | Apply discrete damage respecting i-frames. |
| `src/player.js` | `setHealth(value)` | Clamp to `0` to `100`. |
| `src/enemies.js` | `spawn(type, x, y)` | Create enemy with wave-scaled stats. |
| `src/enemies.js` | `update(dt)` | Move enemies, run states, apply contact damage. |
| `src/enemies.js` | `hit(enemy, amount)` | Reduce HP, set hit flash. |
| `src/enemies.js` | `kill(enemy)` | Mark dead, trigger score/particles. |
| `src/projectiles.js` | `spawn(x, y, angle)` | Create bolt from angle. |
| `src/projectiles.js` | `update(dt)` | Move bolts, collide with enemies, remove expired. |
| `src/hazards.js` | `spawn(type, x, y)` | Create trap with valid position. |
| `src/hazards.js` | `update(dt)` | Advance trap cycles and life. |
| `src/hazards.js` | `damagePlayer(dt)` | Apply spike/laser/acid damage. |
| `src/hazards.js` | `disableNearest(x, y, radius)` | Disable nearest non-off trap in radius. |
| `src/hazards.js` | `clearAll()` | Remove all traps. |
| `src/waves.js` | `startRun()` | Reset wave to intermission before wave 1. |
| `src/waves.js` | `update(dt)` | Advance intermission, spawning, active window, clearing. |
| `src/waves.js` | `startWave(n)` | Spawn composition and traps for wave `n`. |
| `src/waves.js` | `onEnemyKilled()` | Notify wave system of enemy death. |
| `src/waves.js` | `endWave()` | Award wave bonus and start intermission. |
| `src/score.js` | `reset()` | Reset score, combo, last whole second. |
| `src/score.js` | `add(points)` | Add points multiplied by combo. |
| `src/score.js` | `hitEnemy(enemy)` | +1 score, +1 combo. |
| `src/score.js` | `killEnemy(enemy)` | +enemy.score, +2 combo. |
| `src/score.js` | `nearMiss(enemy)` | +5 score, +1 combo. |
| `src/score.js` | `trapDisabled()` | +10 score. |
| `src/score.js` | `waveClear(wave)` | +`50 * wave`. |
| `src/score.js` | `tickTime(dt)` | +1 per whole second. |
| `src/score.js` | `updateCombo(dt)` | Decay combo over time. |
| `src/score.js` | `gameOver()` | Save high score and fill `ui.lastRun`. |
| `src/effects.js` | `addShake(amp, time)` | Start screen shake. |
| `src/effects.js` | `addParticles(x, y, count, color)` | Spawn particles. |
| `src/effects.js` | `addTrail(x, y, color)` | Spawn trail particle. |
| `src/effects.js` | `update(dt)` | Advance effects. |
| `src/audio.js` | `init()` | Create AudioContext after gesture. |
| `src/audio.js` | `play(name)` | Play SFX by name. |
| `src/audio.js` | `startMusic()` | Start chiptune loop. |
| `src/audio.js` | `stopMusic()` | Stop chiptune loop. |
| `src/audio.js` | `setVolume(value)` | Set master gain. |
| `src/ui.js` | `setScreen(state)` | Show correct DOM screen. |
| `src/ui.js` | `renderHUD()` | Update HUD fields. |
| `src/ui.js` | `loadHighScores()` | Read localStorage. |
| `src/ui.js` | `saveHighScores()` | Write localStorage. |
| `src/render.js` | `draw(ctx, game)` | Draw arena, entities, HUD-independent effects. |
| `src/main.js` | `startRun()` | Reset all systems and set `PLAYING`. |
| `src/main.js` | `gameOver()` | Set `GAME_OVER`, save score. |
| `src/main.js` | `loop(timestamp)` | Fixed-step loop. |
| `src/debug.js` | See Section 8. | Debug access. |

---

# 3. VISUAL SPEC

The game is a dark, one-screen, top-down pixel arena. The player is a small bright amber beacon in a black-blue grid. All sprites are low-resolution, blocky, and drawn from a limited palette. The screen is tense because most of the frame is empty black space, threats are small bright shapes, and the player is surrounded by traps that flash and change state. Motion is fast but readable: slow taps are deliberate, fast taps leave trails, and damage is punctuated by white flash and short shake.

Lighting and atmosphere:

- No dynamic lights.
- The arena is a flat top-down surface.
- A static 10% black vignette darkens the outer 24 px.
- Active hazards have a 2 px bright outline for readability.
- Hit flash is white for `0.06` s on enemies and `0.10` s on the player.
- Screen shake is short and subtle.
- Reduced motion disables shake, particles, and trails. Hit flash remains but is reduced to `0.03` s.

The space:

- Fixed 480 × 270 px internal viewport.
- No camera.
- 8 px walls around the playable area.
- Floor is a subtle 24 px grid.
- All entities are visible at all times.
- Spawn points are on the edges and corners.
- Traps may cover floor, player path, or enemy path.

Recipe table:

| Element | Size | Palette / colours | Shape / rules |
| --- | --- | --- | --- |
| Background | 480 × 270 | `#05070a` | Solid black-blue. |
| Floor grid | 24 px cells | `#11151c` lines on `#05070a` | Subtle 1 px grid. |
| Wall border | 8 px | `#222b36` | Solid frame. |
| Player | 12 × 12 | `#ffd23f` body, `#ffffff` flash | Rounded square beacon. Faces 8 directions. |
| Player hit flash | 12 × 12 | `#ffffff` | 0.10 s. |
| Bolt | 4 × 2 | `#8dfcff` | Horizontal/vertical 2 px line. |
| Mote | 8 × 8 | `#ff5d7a` | Circle. Two-frame pulse. |
| Shard | 10 × 10 | `#c084fc` | Diamond. Telegraph blink during charge. |
| Wisp | 10 × 10 | `#f5f7ff` | Triangle. Three-frame flicker. |
| Golem | 14 × 14 | `#7c9cff` | Square block. Two-frame stomp. |
| Enemy hit flash | enemy size | `#ffffff` | 0.06 s. |
| Spike trap | 24 × 24 | Warning `#ffd23f`, active `#ff5d7a` | Square grid of 4 spikes. Active spikes raise. |
| Laser trap | 120 × 4 | Warning `#ffd23f`, active `#ff5d7a` | Thin horizontal or vertical beam. |
| Acid trap | radius 36 | Warning `#ffd23f`, active `#8dfcff` | Circular pool. Dripples while active. |
| Trap disabled | any trap size | `#5a6572` outline | Dimmed while disabled. |
| Particle | 2 × 2 | Entity accent or `#ffffff` | Fading square. |
| Trail | 2 × 2 | `#8dfcff` or `#ffd23f` | Fading dash/frenzy trail. |
| HUD text | 12 px pixel font | `#e8f3ff` | Uppercase. |
| HUD panel | as needed | `#0b0f14` background, `#222b36` border | No images. |
| Health bar | 120 × 8 | Empty `#141a22`, fill `#ffd23f` | Fills from left. |
| Combo text | 12 px | `#e8f3ff`, `#ffd23f` at 10 | Shows combo and multiplier. |
| Wave banner | center text | `#ffd23f` | Shown for 1.0 s at wave start. |

---

# 4. GAMEPLAY SPEC

You are The Warden, a lone beacon in a one-screen collapsing grid. Your only input is a single press. A slow press makes you move toward the pressed point. A medium press fires a bolt. A fast press dashes. A frantic press, if you have enough combo, emits a radial burst that damages nearby enemies and disables a trap. Waves of creatures and environmental traps keep coming, your health does not recover, and the goal is simply to survive longer, build combo, and post a local high score.

Records and rosters:

| Record | Roster / values |
| --- | --- |
| Player | Health `100`, no regen, STEP, STRIKE, DASH, FRENZY. |
| Enemies | Mote, Shard, Wisp, Golem. |
| Hazards | Spike, Laser, Acid. |
| Bolts | Player projectile. |
| Score | Points from kills, hits, time, wave clear, near miss, trap disable. |
| Combo | `0` to `10`, multiplier `1.0` to `2.0`. |
| Waves | Endless, 20 s spawn window, 3 s intermission. |
| High scores | Local top 10. |

## 4.1 Input and action selection [T1/T2]

- The only gameplay input is one press.
- On every press, record `nowMs`, press location, and aim.
- Compute interval:
  - First press: `1000` ms.
  - Later: `nowMs - game.input.lastPressMs`.
- Update `game.input.lastPressMs = nowMs`.
- Update `game.input.lastAim` to press location.
- If press location is within `8` px of the player, use `game.input.facing` for STRIKE and DASH direction.

Press category table:

| Interval since previous press | Category | Action |
| --- | --- | --- |
| `< 150` ms | `FRENZY` | Radial burst if combo and cooldown allow. |
| `150` to `< 350` ms | `DASH` | Dash toward aim if dash cooldown ready. |
| `350` to `< 750` ms | `STRIKE` | Fire bolt toward aim if strike cooldown ready. |
| `≥ 750` ms | `STEP` | Move toward aim. |

Action availability:

| Action | Requirement | If unavailable |
| --- | --- | --- |
| `STEP` | Always available. | N/A. |
| `STRIKE` | `player.strikeCd <= 0`. | No bolt. No score. Cooldown unchanged. |
| `DASH` | `player.dashCd <= 0`. | No dash. No score. Cooldown unchanged. |
| `FRENZY` | `combo.value >= 3` and `player.frenzyCd <= 0`. | No burst. No score. Combo decay timer is reset to `2.5` s. |

## 4.2 Movement [T1/T2]

STEP [T1]:

- Triggered by interval `≥ 750` ms.
- Set `player.stepTarget` to aim.
- Set `player.stepTimer = 0.40` s.
- While `stepTimer > 0`:
  - If distance to `stepTarget` is less than `8` px, velocity is `0`.
  - Otherwise velocity is normalized direction × `190` px/s.
- STEP does not grant i-frames.
- STRIKE and FRENZY do not cancel STEP.
- DASH cancels STEP.

DASH [T2]:

- Triggered by interval `150` to `< 350` ms.
- Requires `player.dashCd <= 0`.
- Set `player.dashTimer = 0.15` s.
- Set `player.dashCd = 0.45` s.
- Set `player.iframes = max(player.iframes, 0.18)` s.
- Clear `player.dashNearMissIds`.
- During DASH:
  - Velocity is `player.dashDir × 520` px/s.
  - Player passes through enemies.
  - Player is immune to discrete contact damage.
  - Continuous trap damage still applies.
- If DASH hits a wall, clamp position and continue timer.
- Each enemy within `18` px during dash iframes grants one near miss per dash.

## 4.3 Combat [T1/T2]

Player health [T1]:

- Max health: `100`.
- Start health: `100`.
- No healing.
- Discrete damage from enemies and spikes respects `player.iframes`.
- Continuous damage from Laser and Acid does not respect i-frames.
- After any discrete damage, set `player.iframes = 0.5` s.
- If health reaches `0`, the run ends.

STRIKE [T1]:

- Triggered by interval `350` to `< 750` ms.
- Requires `player.strikeCd <= 0`.
- Set `player.strikeCd = 0.14` s.
- Fire one bolt from player center toward aim.
- Bolt:
  - Speed: `320` px/s.
  - Damage: `12`.
  - Lifetime: `0.9` s.
  - Radius: `2` px.
- Bolt stops on the first enemy it hits.
- Maximum bolts on screen: `12`. If spawning would exceed the cap, remove the oldest bolt.

FRENZY [T2]:

- Triggered by interval `< 150` ms.
- Requires `combo.value >= 3` and `player.frenzyCd <= 0`.
- Consume `3` combo.
- Set `player.frenzyCd = 1.5` s.
- Apply radial burst centered on player:
  - Radius: `84` px.
  - Enemy damage: `8`.
  - Enemy stun: `0.3` s.
  - Score: +5 per enemy hit.
- Disable the nearest active or warning trap within radius:
  - Set trap `disabledTimer = 5.0` s.
  - Force trap state to `OFF`.
  - Score: +10.
- FRENZY does not cancel STEP or DASH movement, but it interrupts dash visual timing only for rendering.

Enemy contact damage [T1/T2]:

- Applies when enemy circle and player circle overlap.
- Requires `player.iframes <= 0`.
- Damage values are enemy-specific.
- On damage:
  - Reduce player health.
  - Set player i-frames `0.5` s.
  - Play player hit SFX.
  - Add screen shake.
  - Add hit flash.

Enemy death [T1/T2]:

- When `enemy.hp <= 0`:
  - Mark dead.
  - Award kill score and combo.
  - Remove enemy after death effect.
  - Notify wave system.
  - Add particles.
  - Add small screen shake for Golem.

## 4.4 Creatures [T1/T2]

Enemy roster:

| Enemy | Tier | HP | Speed | Radius | Contact damage | Kill score |
| --- | --- | --- | --- | --- | --- | --- |
| Mote | T1 | `10` | `72` px/s | `4` px | `8` | `15` |
| Shard | T2 | `18` | `95` px/s | `5` px | `10` | `25` |
| Wisp | T2 | `12` | `130` px/s | `5` px | `6` | `30` |
| Golem | T2 | `60` | `34` px/s | `8` px | `18` | `80` |

Wave scaling [T2]:

- Enemy HP scale: `1 + 0.05 * (wave - 1)`.
- Enemy speed scale: `1 + 0.02 * (wave - 1)`, capped at `1.5`.
- Contact damage is not scaled.
- Kill score is not scaled.

Mote behaviour [T1]:

- State: `NORMAL`.
- Moves toward player at `speed`.
- Adds perpendicular wobble:
  - `wobble = sin(time * 5 + id) * 12` px/s.
- Contact damage `8`.

Shard behaviour [T2]:

- States: `NORMAL`, `CHARGE`, `DASH`.
- `NORMAL`: moves toward player at `speed`.
- Attack cycle starts every `2.2` s:
  - `CHARGE`: `0.6` s, speed reduced to `30%` of base, visual blink.
  - `DASH`: `0.4` s, speed `400` px/s in facing direction at charge start.
  - Return to `NORMAL`.
- Contact damage `10` in all states.

Wisp behaviour [T2]:

- State: `NORMAL`.
- Moves toward player at `speed`.
- Changes direction randomly every `0.4` s within ± `60` degrees of player direction.
- Every `1.4` s:
  - Teleport:
    - Fade out `0.15` s.
    - Reappear at a random offset `40` to `72` px away.
    - Clamp to playable area.
- Contact damage `6`.

Golem behaviour [T2]:

- State: `NORMAL`.
- Moves directly toward player at `speed`.
- Contact damage `18`.
- On death, stronger screen shake and larger particle burst.

Stun:

- FRENZY sets enemy `state = 'STUN'` for `0.3` s.
- During stun, enemy velocity is `0`.
- Stun does not prevent contact damage if player touches the stunned enemy, but player i-frames still apply.

## 4.5 Hazards [T2]

Trap spawn [T2]:

- At the start of each wave, spawn traps:
  - Count: `min(1 + floor(wave / 3), 6)`.
- Trap type weights:
  - Spike: `40`
  - Laser: `35`
  - Acid: `25`
- Trap positions:
  - Must be inside playable area with at least `32` px from the outer wall.
  - Must be at least `60` px from the player.
  - Must be at least `48` px from the center of any other trap.
  - If a valid position is not found after 20 attempts, skip that trap.

Spike [T2]:

- Size: `24 × 24` px.
- Life: `12` s.
- Cycle total: `4.0` s.
  - `WARNING`: `0.8` s.
  - `ACTIVE`: `1.2` s.
  - `OFF`: `2.0` s.
- Damage:
  - While `ACTIVE`, if player rect overlaps spike rect and `player.iframes <= 0`, deal `12` damage.
- FRENZY can disable it.

Laser [T2]:

- Size: `120 × 4` px.
- Orientation: horizontal or vertical.
- Life: `12` s.
- Cycle total: `2.7` s.
  - `OFF`: `1.5` s.
  - `WARNING`: `0.4` s.
  - `ACTIVE`: `0.8` s.
- Damage:
  - While `ACTIVE`, if player circle intersects beam rect, deal `20` damage per second continuously.
- FRENZY can disable it.

Acid [T2]:

- Radius: `36` px.
- Life: `10` s.
- Cycle total: `6.0` s.
  - `WARNING`: `1.0` s.
  - `ACTIVE`: `4.0` s.
  - `OFF`: `1.0` s.
- Damage:
  - While `ACTIVE`, if player center is inside acid circle, deal `10` damage per second continuously.
  - Also applies slow:
    - Player STEP and DASH speed × `0.70` while inside active acid.
- FRENZY can disable it.

Trap disable [T2]:

- FRENZY selects the nearest trap whose state is `WARNING` or `ACTIVE` and distance to player is ≤ `84` px.
- Set `disabledTimer = 5.0` s.
- Force state to `OFF`.
- While disabled:
  - No damage.
  - No slow.
  - Visual dimmed.
- After `disabledTimer` expires, trap resumes normal cycle with `stateTimer` set to the start of its next state.

## 4.6 Score and records [T1/T2]

Score events:

| Event | Base points | Combo change | Tier |
| --- | --- | --- | --- |
| Bolt hits enemy | `1` | +1 | T1 |
| FRENZY hits enemy | `5` per enemy | 0 | T2 |
| Enemy kill | Enemy kill score | +2 | T1/T2 |
| Dash near miss | `5` per enemy per dash | +1 | T2 |
| FRENZY disables trap | `10` | 0 | T2 |
| Wave clear | `50 * wave` | 0 | T1 |
| Survive 1 whole second | `1` | 0 | T1 |

Combo [T2]:

- Max combo: `10`.
- Start combo: `0`.
- Gains:
  - Bolt hit: +1.
  - Kill: +2.
  - Dash near miss: +1.
- FRENZY consumes 3 combo. It does not gain combo.
- Combo timer:
  - On any gain, set `combo.timer = 2.5` s.
  - If no gain for `2.5` s, begin decay.
  - After decay begins, reduce combo by `1` every `0.5` s until `0`.
- Multiplier:
  - `multiplier = 1 + 0.1 * combo.value`.
  - Maximum multiplier: `2.0`.
- Score formula:
  - `points = round(basePoints * multiplier)`.

High scores [T1/T2]:

- Store top 10 entries in `localStorage` key `one_button_roguelike_scores_v1`.
- Entry fields:
  - `score`
  - `wave`
  - `time`
  - `combo`
  - `date`
- Sort order:
  1. `score` descending.
  2. `time` descending.
  3. `wave` descending.
  4. `combo` descending.
  5. newer date first.
- No player name input.
- If storage fails, game continues with an empty high-score list.

## 4.7 Waves and spawning [T1/T2]

Wave structure:

- Run starts in `INTERMISSION` for `3.0` s.
- Wave number starts at `1`.
- Each wave:
  - `SPAWNING`: `0.5` s spawn warning for enemies.
  - `ACTIVE`: `20.0` s spawn window.
  - `CLEARING`: after the 20 s window, wait until all enemies are dead.
- When wave clears:
  - Award wave clear score.
  - Start next wave after `3.0` s intermission.
- Waves are endless.

Spawn composition [T2]:

At wave start, desired enemy counts are:

| Enemy | Formula | Cap |
| --- | --- | --- |
| Mote | `min(3 + floor(wave / 2), 8)` | 8 |
| Wisp | `wave >= 2 ? min(floor((wave + 1) / 3), 3) : 0` | 3 |
| Shard | `wave >= 4 ? min(floor((wave - 1) / 4), 3) : 0` | 3 |
| Golem | `wave >= 6 ? min(floor((wave - 4) / 4), 2) : 0` | 2 |

If total desired enemies exceeds `14`, reduce counts in this order:

1. Mote
2. Wisp
3. Shard
4. Golem

Maximum concurrent enemies: `14`.

Mid-wave extra spawns [T2]:

- Starting from wave 2, during `ACTIVE`:
  - Every `5.0` s, if `enemies.length < 14`, spawn one extra enemy.
- Extra enemy type is weighted from available types:
  - Mote: `50`
  - Wisp: `20`
  - Shard: `15`
  - Golem: `15`
- If a type is not yet available because its wave has not started, redistribute its weight to Mote.

Spawn points [T1]:

| Point | X | Y |
| --- | --- | --- |
| Top-left | `12` | `12` |
| Top-right | `468` | `12` |
| Bottom-left | `12` | `258` |
| Bottom-right | `468` | `258` |
| Top-middle | `240` | `12` |
| Bottom-middle | `240` | `258` |
| Left-middle | `12` | `135` |
| Right-middle | `468` | `135` |

Spawn rules:

- Choose a spawn point at least `70` px from the player.
- If no spawn point is far enough, choose the farthest available point.
- Enemies spawn in a `SPAWN_WARN` state for `0.5` s.
- During `SPAWN_WARN`:
  - Enemy is visible as an outline.
  - Enemy does not move.
  - Enemy does not deal damage.
  - Enemy is not hittable by bolts.

Difficulty ramp [T2]:

- Enemy HP and speed scale as defined in Section 4.4.
- Trap count increases as defined in Section 4.5.
- Extra spawn rate remains constant but composition changes.
- No trap damage scaling.
- No player damage scaling.

## 4.8 Survival and failure [T1]

- Player starts with `100` HP.
- No healing.
- No pickups.
- Discrete damage is prevented during i-frames.
- Continuous trap damage can kill the player even during i-frames, but rates are low enough to avoid unfair melt.
- When health ≤ 0:
  - Set `player.alive = false`.
  - Stop music.
  - Play game-over SFX.
  - Save score.
  - Set `game.state = 'GAME_OVER'`.
  - Fill `game.ui.lastRun`:
    - `score`
    - `wave`
    - `time`
    - `combo` best value
    - `newHighScore`
    - `rank`

## 4.9 Feel [T2/T3]

Input feedback [T2]:

- Every gameplay press shows a small ring at the aim point for `0.04` s.
- Ring colour by category:
  - STEP: `#e8f3ff`
  - STRIKE: `#8dfcff`
  - DASH: `#c084fc`
  - FRENZY success: `#ffd23f`
  - FRENZY fail: `#5a6572`

Screen shake [T2]:

- Player hit: amplitude `5` px, duration `0.18` s.
- Golem death: amplitude `3` px, duration `0.12` s.
- FRENZY: amplitude `2` px, duration `0.08` s.
- Shake decay is exponential.
- Reduced motion disables shake.

Particles [T2]:

- Enemy hit: `4` particles.
- Enemy death: `8` particles.
- Golem death: `16` particles.
- Player hit: `12` particles.
- Trap hit: `6` particles.
- FRENZY: `16` particles.
- Particle lifetime: `0.30` to `0.60` s.
- Particle velocity: `40` to `120` px/s.
- Reduced motion disables particles.

Trails [T2]:

- DASH leaves 5 trail particles along the dash path over `0.15` s.
- FRENZY leaves a radial ring trail for `0.30` s.
- Reduced motion disables trails.

Hit flash [T2]:

- Enemy hit flash: `0.06` s white.
- Player hit flash: `0.10` s white.
- Reduced motion reduces hit flash to `0.03` s.

Tense pacing [T3]:

- Wave banner lasts `1.0` s.
- High-score entry triggers a short chiptune arpeggio.
- Combo at `5` and `10` pulses the HUD combo text.
- Music adds one layer at wave 3 and one layer at wave 6.

---

# 5. CHARACTERS

Player: The Warden

| Aspect | Rule |
| --- | --- |
| Silhouette | 12 × 12 amber square with 2 px notched corners. |
| Facing | 8 directions: N, S, E, W, NE, NW, SE, SW. |
| Facing update | Updated by STEP, STRIKE, DASH. |
| Default facing | Up: `-π/2`. |

Player animations:

| Animation | Frames | Motion rule |
| --- | --- | --- |
| `idle` | 2 | Core blinks every `0.5` s. |
| `step` | 4 | 2 px bob in movement direction while `stepTimer > 0`. |
| `strike` | 2 | Recoils 1 px opposite aim for `0.12` s after STRIKE. |
| `dash` | 2 | Stretched 2 px in dash direction while `dashTimer > 0`. |
| `hit` | 1 | White flash for `0.10` s. |
| `death` | 3 | Shrinks over `0.40` s, then run is already in Game Over screen. |

Enemy roster:

| Enemy | Silhouette | Animation states needed |
| --- | --- | --- |
| Mote | 8 × 8 magenta circle | `NORMAL`, `HIT`, `STUN` |
| Shard | 10 × 10 violet diamond | `NORMAL`, `CHARGE`, `DASH`, `HIT`, `STUN` |
| Wisp | 10 × 10 white triangle | `NORMAL`, `HIT`, `STUN`, teleport fade |
| Golem | 14 × 14 indigo square | `NORMAL`, `HIT`, `STUN`, death burst |

Enemy animation rules:

| Animation | Rule |
| --- | --- |
| Mote pulse | 2-frame scale/pulse every `0.6` s. |
| Shard charge | Blink between normal and white every `0.1` s during `CHARGE`. |
| Shard dash | Stretch 2 px in dash direction during `DASH`. |
| Wisp flicker | 3-frame flicker every `0.3` s. |
| Wisp teleport | Fade out `0.15` s, reappear at new position. |
| Golem stomp | 2-frame vertical bob every `0.8` s. |
| Enemy hit flash | White for `0.06` s. |
| Enemy stun | Still, 2 px vertical wobble only if reduced motion is off. |
| Enemy death | Remove after `0.20` s particle burst. |

Trap animation rules:

| Trap | Warning | Active |
| --- | --- | --- |
| Spike | Yellow 4-spike outline, no damage. | Red-magenta spikes raised, damage. |
| Laser | Thin yellow line, low opacity. | Bright red-magenta beam, damage. |
| Acid | Yellow circle outline. | Cyan pool with 2 px dripples, damage and slow. |

---

# 6. AUDIO

All audio is synthesized with WebAudio. No audio files.

Master volume: `0.5`. Music gain: `0.25`. SFX gains are relative to master.

Music:

| Name | Recipe | When it plays |
| --- | --- | --- |
| `music_loop` | 4/4 at 112 BPM. Bass: triangle `65.4 Hz`, quarter notes, gain `0.18`. Lead: square `262 Hz`, 8th-note pattern C-C-D-C-E-C-D-C, gain `0.12`. Hat: filtered noise, high-pass around `6000 Hz`, 8th offbeats, gain `0.05`. Wave 3 adds second square lead at `311 Hz`, gain `0.08`. Wave 6 adds arpeggio square notes `392`, `494`, `659 Hz` in 16th pattern, gain `0.06`. | `PLAYING` only. Stops on `GAME_OVER`. |

SFX table:

| Name | Recipe | When it plays |
| --- | --- | --- |
| `ui_press` | Square `880 Hz`, 20 ms, gain `0.10`, fast decay. | Screen navigation press. |
| `tap_step` | Triangle `392 Hz`, 30 ms, gain `0.12`. | STEP action. |
| `tap_strike` | Square `1046 Hz`, 20 ms, gain `0.10`. | STRIKE action. |
| `tap_dash` | Sawtooth sweep `600 Hz` to `1200 Hz`, 50 ms, gain `0.15`. | DASH action. |
| `tap_frenzy` | Square chord `523`, `659`, `784 Hz`, 80 ms, gain `0.18`, plus 50 ms noise burst gain `0.08`. | Successful FRENZY. |
| `tap_fail` | Square `180 Hz`, 40 ms, gain `0.06`. | Failed FRENZY. |
| `player_hit` | Square sweep `220 Hz` to `80 Hz`, 90 ms, gain `0.22`, plus 50 ms noise gain `0.08`. | Player takes discrete damage. |
| `enemy_hit` | Square `660 Hz`, 20 ms, gain `0.08`. | Enemy takes bolt/FRENZY damage. |
| `enemy_die` | Square sweep `440 Hz` to `110 Hz`, 100 ms, gain `0.15`, plus 30 ms noise gain `0.06`. | Enemy killed. |
| `bolt_fire` | Square `1568 Hz`, 15 ms, gain `0.06`. | Bolt spawned. |
| `trap_warn` | Triangle `988 Hz`, 30 ms, twice with 80 ms gap, gain `0.07`. | Trap enters `WARNING`. |
| `trap_hit` | Low-passed noise around `1200 Hz`, 70 ms, gain `0.18`. | Player takes hazard damage. |
| `combo_up` | Triangle `1046 Hz`, 15 ms, gain `0.07`. | Combo increases. |
| `wave_start` | Square `523 Hz`, 70 ms, gain `0.12`. | Wave number increases. |
| `game_over` | Triangle sweep `392 Hz` to `65 Hz`, 600 ms, gain `0.25`. | Player death. |
| `high_score` | Square arpeggio `523`, `659`, `784`, `1046 Hz`, 50 ms each, gain `0.12`. | Entering High Scores screen with a new top 10 entry. |

---

# 7. UX

HTML and CSS only for screens and HUD. The canvas renders the arena and game entities. DOM overlays handle screens and HUD.

State machine:

| Current state | Input | Next state | Notes |
| --- | --- | --- | --- |
| `BOOT` | none | `TITLE` | Load assets, init audio unavailable, load high scores. |
| `TITLE` | one press | `PLAYING` | Start new run. |
| `PLAYING` | gameplay presses | `PLAYING` | Presses are gameplay input. |
| `PLAYING` | player health ≤ 0 | `GAME_OVER` | Save score, show game-over screen. |
| `GAME_OVER` | one press | `HIGH_SCORES` | Show final stats and top 10. |
| `HIGH_SCORES` | one press | `PLAYING` | Start a new run. |

HTML structure:

```html
<div id="stage">
  <canvas id="game" width="480" height="270"></canvas>

  <div id="hud" class="hidden">
    <div id="hud-health" class="hud-panel">
      <span class="label">HP</span>
      <div class="bar">
        <div id="hud-health-fill"></div>
      </div>
      <span id="hud-health-text"></span>
    </div>

    <div id="hud-score" class="hud-panel">
      <span class="label">SCORE</span>
      <span id="hud-score-value"></span>
    </div>

    <div id="hud-timer" class="hud-panel">
      <span class="label">TIME</span>
      <span id="hud-timer-value"></span>
    </div>

    <div id="hud-combo" class="hud-panel">
      <span class="label">COMBO</span>
      <span id="hud-combo-value"></span>
      <span id="hud-combo-mult"></span>
    </div>

    <div id="hud-wave" class="hud-panel">
      <span class="label">WAVE</span>
      <span id="hud-wave-value"></span>
    </div>
  </div>

  <section id="screen-title" class="screen">
    <h1 class="pixel-font">ONE BUTTON</h1>
    <p class="pixel-font">PRESS TO START</p>
  </section>

  <section id="screen-gameover" class="screen hidden">
    <h1 class="pixel-font">SIGNAL LOST</h1>
    <p class="pixel-font" id="gameover-score"></p>
    <p class="pixel-font" id="gameover-wave"></p>
    <p class="pixel-font" id="gameover-time"></p>
    <p class="pixel-font" id="gameover-combo"></p>
    <p class="pixel-font">PRESS FOR SCORES</p>
  </section>

  <section id="screen-highscores" class="screen hidden">
    <h1 class="pixel-font">HIGH SCORES</h1>
    <ol id="highscore-list" class="pixel-font"></ol>
    <p class="pixel-font">PRESS TO RESTART</p>
  </section>
</div>
```

CSS rules:

- `#stage` centers the canvas.
- `canvas` uses `image-rendering: pixelated`.
- Canvas scales to fit the viewport with integer scaling when possible.
- `.screen` is absolutely positioned over the canvas.
- `.hidden` sets `display: none`.
- `.pixel-font` uses:
  ```css
  font-family: 'Press Start 2P', 'Courier New', monospace;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  ```
- HUD is a top bar with 4 px pixel border.
- Health bar is 120 × 8 px.
- All text is uppercase.

HUD table:

| Element | Record field | When visible | Notes |
| --- | --- | --- | --- |
| Health bar fill | `game.player.health / game.player.maxHealth` | `PLAYING` | Width percentage. |
| Health text | `game.player.health` | `PLAYING` | Integer HP. |
| Score | `game.score.value` | `PLAYING` | Integer. |
| Timer | `game.time` | `PLAYING` | `mm:ss`. |
| Combo counter | `game.combo.value` | `PLAYING` | `COMBO 04`. |
| Combo multiplier | `1 + 0.1 * game.combo.value` | `PLAYING` | `×1.40` format. |
| Wave number | `game.wave.number` | `PLAYING` | `WAVE 03`. |
| Title text | static | `TITLE` | “ONE BUTTON / PRESS TO START”. |
| Game over score | `game.ui.lastRun.score` | `GAME_OVER` | Final score. |
| Game over wave | `game.ui.lastRun.wave` | `GAME_OVER` | Final wave. |
| Game over time | `game.ui.lastRun.time` | `GAME_OVER` | `mm:ss`. |
| Game over combo | `game.ui.lastRun.combo` | `GAME_OVER` | Best combo. |
| High score list | `game.ui.highScores` | `HIGH_SCORES` | Top 10. |
| Reduced motion indicator | `game.settings.reducedMotion` | `TITLE` | Optional small text: “RM ON”. |

---

# 8. DEBUG API

All debug functions are exposed on `window.Debug` in development and optional test builds.

| Function | System | Effect |
| --- | --- | --- |
| `Debug.press(x, y)` | Input | Simulate a press at internal coordinates using current time. |
| `Debug.tapAt(x, y, intervalMs)` | Input | Force the previous press timestamp so the next press has the given interval. |
| `Debug.tapSlow(x, y)` | Input | Simulate STEP press. |
| `Debug.tapMedium(x, y)` | Input | Simulate STRIKE press. |
| `Debug.tapFast(x, y)` | Input | Simulate DASH press. |
| `Debug.tapFrenzy(x, y)` | Input | Simulate FRENZY press. |
| `Debug.setPlayerHealth(value)` | Player / survival | Set player health clamped to `0` to `100`. |
| `Debug.addPlayerDamage(value)` | Player / survival | Apply discrete damage. |
| `Debug.setPlayerPosition(x, y)` | Player | Move player, clamped to playable area. |
| `Debug.setScore(value)` | Score | Set score. |
| `Debug.addScore(value)` | Score | Add raw score without multiplier. |
| `Debug.setCombo(value)` | Score / combo | Set combo clamped to `0` to `10`. |
| `Debug.setWave(value)` | Waves | Set wave number and start that wave immediately. |
| `Debug.startWaveNow(value)` | Waves | Clear run entities and start wave `value`. |
| `Debug.spawnEnemy(type, x, y)` | Creatures | Spawn enemy type at position with current wave scaling. |
| `Debug.spawnTrap(type, x, y)` | Hazards | Spawn trap at position, bypassing position checks. |
| `Debug.clearEnemies()` | Creatures | Remove all enemies. |
| `Debug.clearTraps()` | Hazards | Remove all traps. |
| `Debug.clearBolts()` | Combat | Remove all player bolts. |
| `Debug.addTime(seconds)` | Score / timer | Advance run time and time score. |
| `Debug.forceGameOver()` | Survival | Trigger death. |
| `Debug.setReducedMotion(value)` | Accessibility | Toggle reduced motion at runtime. |
| `Debug.setShakeEnabled(value)` | Effects | Enable/disable screen shake. |
| `Debug.setVolume(value)` | Audio | Set master volume. |
| `Debug.showScreen(state)` | UX | Force one of `TITLE`, `PLAYING`, `GAME_OVER`, `HIGH_SCORES`. |

---

# 9. TESTS

Tier 1 tests:

1. `BOOT` starts in `TITLE`.
2. A single press on `TITLE` starts a new run and sets state to `PLAYING`.
3. Fixed-step loop advances time in exact `1 / 60` s increments under simulated frames.
4. First gameplay press is treated as `STEP`.
5. A press with interval `≥ 750` ms sets `player.stepTimer` to `0.40` and moves the player toward the aim.
6. A press with interval `350` to `< 750` ms spawns a bolt with damage `12`, speed `320`, and lifetime `0.9`.
7. Player start health is `100`.
8. Mote spawns with HP `10`, speed `72`, contact damage `8`, and kill score `15` at wave 1.
9. Mote moves toward the player.
10. Bolt hitting a Mote reduces Mote HP by `12` and awards +1 score and +1 combo.
11. Killing a Mote awards `15` base score multiplied by combo multiplier.
12. Wave 1 spawns exactly `3` Motes and `1` trap.
13. Run timer increments while `PLAYING`.
14. Score, timer, combo, wave, and health HUD update.
15. Player health reaching `0` changes state to `GAME_OVER`.
16. Game Over screen shows final score, wave, time, and combo.
17. High score top 1 is saved and readable after reload if storage is available.
18. No gameplay input other than one press is required.

Tier 2 tests:

1. Press interval `150` to `< 350` ms triggers DASH.
2. DASH sets velocity to `520` px/s for `0.15` s.
3. DASH grants at least `0.18` s i-frames.
4. DASH cooldown is `0.45` s and prevents immediate repeated dashes.
5. Press interval `< 150` ms with combo `< 3` does not trigger FRENZY and does not consume combo.
6. Press interval `< 150` ms with combo `≥ 3` consumes `3` combo and applies FRENZY.
7. FRENZY deals `8` damage to enemies within `84` px.
8. FRENZY stuns affected enemies for `0.3` s.
9. FRENZY disables the nearest warning/active trap within radius and sets `disabledTimer = 5.0`.
10. FRENZY cooldown is `1.5` s.
11. Combo decays after `2.5` s without gain and then every `0.5` s.
12. Combo multiplier is `1 + 0.1 * combo.value` and caps at `2.0`.
13. Shard telegraphs for `0.6` s and dashes at `400` px/s for `0.4` s.
14. Wisp teleports every `1.4` s to a clamped position `40` to `72` px away.
15. Golem has HP `60`, speed `34`, contact damage `18`, kill score `80`.
16. Enemy HP scales by `1 + 0.05 * (wave - 1)`.
17. Enemy speed scales by `1 + 0.02 * (wave - 1)` capped at `1.5`.
18. Spike deals `12` discrete damage only while active and respects player i-frames.
19. Laser deals `20` damage per second while active.
20. Acid deals `10` damage per second and slows player movement by `30%` while active.
21. Traps spawn at least `60` px from the player and at least `48` px from other traps when valid positions exist.
22. Trap count per wave is `min(1 + floor(wave / 3), 6)`.
23. Wave 2 spawns at least `1` Wisp.
24. Wave 4 spawns at least `1` Shard.
25. Wave 6 spawns at least `1` Golem.
26. Maximum concurrent enemies is `14`.
27. Screen shake triggers on player hit.
28. Particles spawn on enemy hit and death.
29. Hit flash appears on damaged entities.
30. DASH leaves trail particles.
31. High score list stores top 10 entries and sorts by score descending.

Tier 3 tests:

1. Reduced motion disables screen shake.
2. Reduced motion disables particles.
3. Reduced motion disables trails.
4. Reduced motion still allows hit flash at reduced duration.
5. `prefers-reduced-motion: reduce` sets `game.settings.reducedMotion` true.
6. URL `?rm=1` sets `game.settings.reducedMotion` true.
7. Palette contains no red/green-only identification.
8. Enemy types are distinguishable by shape when colour is ignored.
9. Trap states are distinguishable by shape and animation when colour is ignored.
10. Audio context is created after first user gesture.
11. If WebAudio is unavailable, gameplay continues without throwing.
12. Music stops on game over.
13. Music adds one layer at wave 3 and one layer at wave 6.
14. High scores persist across reload when storage is available.
15. Corrupt `localStorage` data results in an empty high-score list without crashing.
16. Keyboard-only Space uses last pointer position or center fallback.
17. Presses at screen edges do not move entities outside the playable area.
18. A dropped frame larger than `0.25` s is clamped and does not cause an infinite update loop.
19. FRENZY fail plays `tap_fail` and does not consume combo.
20. Game Over screen press goes to High Scores screen, and High Scores press starts a new run.

---

# 10. BUILD ORDER

1. Build the HTML shell, CSS layout, canvas, fixed-step loop, and screen state machine.
2. Implement `config.js` with all numeric constants.
3. Implement seeded RNG.
4. Implement one-button input with press interval and aim.
5. Implement player reset, STEP movement, STRIKE bolt, health, i-frames, and death.
6. Implement Mote enemy, enemy movement, bolt collision, enemy death, and score/combo basics.
7. Implement wave 1 spawning, timer, HUD, title, game over, and local high score top 1.
8. Test Tier 1.
9. Implement DASH and input feedback rings.
10. Implement combo decay, multiplier, and FRENZY.
11. Implement Shard, Wisp, and Golem.
12. Implement Spike, Laser, and Acid traps.
13. Implement full wave composition, extra spawns, difficulty scaling, and trap spawning.
14. Implement screen shake, particles, hit flash, and trails.
15. Implement top 10 high scores and game-over stats.
16. Test Tier 2.
17. Implement reduced motion, colour-blind safe checks, audio layering, persistence edge cases, and wave banners.
18. Add debug API and run the full test list.
19. Test Tier 3.

---

# 11. DEFINITION OF DONE

## Tier 1 done

High level: The minimal one-button survival loop is playable from title to game over with score and high score.

Checkboxes:

- [ ] Browser page loads to `TITLE` without console errors.
- [ ] One press starts a run.
- [ ] Slow press moves player toward aim.
- [ ] Medium press fires a bolt.
- [ ] Bolt damages and kills Mote.
- [ ] Mote spawns in wave 1 and moves toward player.
- [ ] Player health decreases on contact.
- [ ] Player i-frames prevent instant repeated contact damage.
- [ ] Player death ends run.
- [ ] Game Over screen shows score, wave, time, and combo.
- [ ] HUD shows health, score, timer, combo, wave.
- [ ] Score increases from kills, hits, time, and wave clear.
- [ ] Combo increases on hits and kills.
- [ ] High score top 1 saves when storage is available.
- [ ] No extra input controls are used.
- [ ] Internal render size is 480 × 270.
- [ ] Art is pixelated and uses the limited palette.
- [ ] Basic SFX play on press, hit, kill, and death.
- [ ] Tier 1 tests pass.

## Tier 2 done

High level: The full press-speed fantasy works, all creatures and traps exist, difficulty ramps, and the game feels tense.

Checkboxes:

- [ ] Fast press dashes with correct speed, duration, i-frames, and cooldown.
- [ ] Frantic press triggers FRENZY only when combo is at least `3` and cooldown is ready.
- [ ] FRENZY consumes `3` combo.
- [ ] FRENZY damages enemies within `84` px.
- [ ] FRENZY stuns enemies for `0.3` s.
- [ ] FRENZY disables one nearby trap for `5.0` s.
- [ ] Combo decays correctly.
- [ ] Combo multiplier caps at `2.0`.
- [ ] Mote, Shard, Wisp, and Golem all spawn and behave correctly.
- [ ] Shard telegraph and dash timing are correct.
- [ ] Wisp teleport timing and distance are correct.
- [ ] Golem contact damage and score are correct.
- [ ] Spike, Laser, and Acid traps all spawn and deal correct damage.
- [ ] Acid slows player by `30%`.
- [ ] Trap positions respect distance rules.
- [ ] Wave composition formulas are correct.
- [ ] Wave 2 includes Wisp, wave 4 includes Shard, wave 6 includes Golem.
- [ ] Enemy HP and speed scale with wave.
- [ ] Maximum concurrent enemies is `14`.
- [ ] Screen shake, particles, hit flash, and trails render.
- [ ] High score list stores and displays top 10.
- [ ] Game Over screen transitions to High Scores screen.
- [ ] High Scores screen transitions to a new run.
- [ ] Tier 2 tests pass.

## Tier 3 done

High level: The game is polished, accessible, robust, and ready for a small release.

Checkboxes:

- [ ] Reduced motion disables shake, particles, and trails.
- [ ] Reduced motion is detected from media query or `?rm=1`.
- [ ] Colour-blind safe palette is used.
- [ ] Enemy types are distinguishable by shape.
- [ ] Trap states are distinguishable by shape and animation.
- [ ] Audio starts after first gesture.
- [ ] Missing WebAudio does not crash gameplay.
- [ ] Music loop starts, layers at wave 3 and wave 6, and stops on death.
- [ ] High scores persist across reload.
- [ ] Corrupt storage does not crash.
- [ ] Keyboard-only input works with pointer-position or center fallback.
- [ ] Edge presses do not push entities outside bounds.
- [ ] Frame drops are clamped.
- [ ] Debug API exposes all required functions.
- [ ] Wave banner displays for `1.0` s.
- [ ] Combo HUD pulses at `5` and `10`.
- [ ] Final high-score rank is shown when applicable.
- [ ] Tier 3 tests pass.

---

# A. SANITY

| Check | Result | Notes / fix applied |
| --- | --- | --- |
| One-button requirement | Valid. | Only primary pointer or Space is used. Aim is part of the same press. |
| Press speed decides action | Valid. | Intervals map to STEP, STRIKE, DASH, FRENZY. |
| 2D top-down | Valid. | Fixed 2D top-down arena. |
| Free movement | Valid. | Movement is continuous toward aim, not grid-locked or lane-based. |
| Endless session | Valid. | Waves increase forever. |
| Permadeath | Valid. | Health 0 ends run. Restart creates new run. |
| Tense tone | Valid. | No healing, one-screen pressure, traps, short i-frames, dark palette. |
| One screen | Valid. | No camera scrolling. |
| Systems list respected | Valid. | No pickups, upgrades, shop, pause, inventory, or extra narrative systems. |
| HUD fields | Valid. | Health, score, timer, combo, wave all present. |
| Screens | Valid. | Title, Game Over, High Scores are separate states. |
| Effects | Valid. | Screen shake, particles, hit flash, trails all specified. |
| Accessibility | Valid. | Colour-blind safe palette and reduced motion specified. |
| Pixel art | Valid. | 480 × 270 internal pixels, integer scaling, limited palette. |
| Initial STEP movement speed concern | Fixed. | STEP was initially too slow for average movement. Updated to `190` px/s for `0.40` s, giving about `76` px per slow press and roughly `101` px/s maximum steady movement. |
| FRENZY availability concern | Fixed. | FRENZY now explicitly requires combo `≥ 3`; failure does not consume combo but starts decay. |
| High score screen ambiguity | Fixed. | High Scores is its own state after Game Over, satisfying the three-screen requirement without adding a second input. |
| Pickups mentioned in prompt but not in final systems | Fixed. | Ruling: no pickups, because final system parts do not include pickups. |
| Red/green palette risk | Fixed. | Palette uses magenta, cyan, yellow, indigo, violet, and white. Shape differences are required. |
| Wave composition cap | Fixed. | If desired enemies exceed `14`, counts are reduced in a defined order. |
| Trap placement fairness | Fixed. | Traps must be at least `60` px from the player and `48` px from other trap centers. |
| Continuous damage vs i-frames | Fixed. | Discrete damage respects i-frames; continuous laser/acid damage does not, but rates are low enough to avoid unfair melt. |
| Audio autoplay risk | Fixed. | Audio context is created only after first user gesture and fails silently if unavailable. |
| Pixel font dependency | Fixed. | Pixel webfont is primary, monospace fallback is allowed. No proportional font. |
| Debug API completeness | Valid. | Functions cover input, player, score, combo, waves, creatures, hazards, effects, audio, and screens. |
| Test coverage | Valid. | Tests are tied to Tier 1, Tier 2, and Tier 3 definitions of done. |
