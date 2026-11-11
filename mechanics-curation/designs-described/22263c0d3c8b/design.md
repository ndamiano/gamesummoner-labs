# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Browser game built by an agentic AI | `# 2. CONTRACTS`, `# 10. BUILD ORDER`, `# 11. DEFINITION OF DONE` |
| Platformer where you play as a frog | `# 4. GAMEPLAY SPEC`, `# 5. CHARACTERS` |
| 2D | `# 1. CONVENTIONS`, `# 3. VISUAL SPEC`, `# 4. GAMEPLAY SPEC` |
| Side-on camera | `# 3. VISUAL SPEC`, `# 4. GAMEPLAY SPEC`, `# 2. CONTRACTS` |
| Real-time | `# 1. CONVENTIONS`, `# 2. CONTRACTS`, `# 4. GAMEPLAY SPEC` |
| Free movement | `# 4. GAMEPLAY SPEC` platforming rules |
| Sequence of levels | `# 4. GAMEPLAY SPEC`, `# 7. UX` |
| Failure: restart the level | `# 4. GAMEPLAY SPEC`, `# 7. UX` |
| Silly tone | `# 3. VISUAL SPEC`, `# 5. CHARACTERS`, `# 6. AUDIO` |
| Handful of levels, under 30 minutes | `# 0.2 Decisions`, `# 4. GAMEPLAY SPEC` level roster |
| Win/lose: reach the exit | `# 4. GAMEPLAY SPEC`, `# 7. UX` |
| Core mechanic: platforming | `# 4. GAMEPLAY SPEC` platforming |
| Core mechanic: physics | `# 4. GAMEPLAY SPEC` physics |
| Core mechanic: hazards | `# 4. GAMEPLAY SPEC` hazards |
| Supporting mechanics: none | `# 0.2 Decisions`, `# 4. GAMEPLAY SPEC` |
| Extra mechanic: collectibles | `# 4. GAMEPLAY SPEC` collectibles, tier 3 |
| Pixel art, low-resolution sprites, visible square pixels, limited palette | `# 3. VISUAL SPEC` |
| Saturated palette | `# 3. VISUAL SPEC` palette |
| Pixel font | `# 3. VISUAL SPEC`, `# 7. UX` |
| Chiptune music | `# 6. AUDIO` |
| Retro bleep sound effects | `# 6. AUDIO` |
| Screens: title, pause, settings, win, level select | `# 7. UX` |
| HUD: score | `# 7. UX` HUD |
| Effects: particles, hit flash | `# 3. VISUAL SPEC`, `# 4. GAMEPLAY SPEC`, `# 6. AUDIO` |
| Accessibility: colour-blind safe palette, reduced motion, remappable keys | `# 3. VISUAL SPEC`, `# 7. UX`, `# 2. CONTRACTS` |

## 0.2 Decisions

| Decision | Final ruling | Why |
| --- | --- | --- |
| Player identity | A blue tree frog named **Blorp**. Silly, non-canonical, colour-blind-safe. | Avoids red/green confusion and fits saturated palette. |
| Level count | Exactly **5 levels**. | “Handful” and under 30 minutes. |
| Target completion time | **25 minutes** total target: 3, 4, 5, 6, 7 minutes per level. | Leaves margin under 30 minutes. |
| Level names | L1 Pond Steps, L2 Log Roll, L3 Lily Bounce, L4 Moss Climb, L5 Fly Feast. | Progressive teaching order. |
| Enemies | Dragonflies and beetles are **hazard entities**, not combat enemies. | Preserves “supporting mechanics: none”. |
| Traps | Spikes, lava, pits/falling. | Directly requested hazard examples. |
| Pickups | Flies, 8 per level, 40 total. | Fits frog, collectibles-as-set, bounded score. |
| Physics objects used by player | Rolling logs and bounce pads. | Gives fall/roll/bounce/collision without combat or puzzles. |
| Climbing | Ladders/vines are climbable tiles. | Required by platforming. |
| One-way platforms | Allowed as platforming surfaces, not a separate mechanic. | Helps level flow while staying inside platforming. |
| Combat | None. | No supporting mechanics. |
| Health/lives | None. One hazard contact = death. | Simple, silly, fast restart. |
| Death behaviour | Hit flash, death particles, 0.75 s transition, auto-restart current level. | Required failure model. |
| Exit behaviour | Exit triggers after 0.20 s overlap. | Prevents accidental instant completion. |
| Collectibles required for win | No. Win only requires exit. | Win/lose says reach exit. |
| Collectibles set | 8 flies per level. Full set gives +500 bonus. | “Collect as a set” without gating win. |
| Score values | Fly +100, exit +500, all-flies bonus +500. Max per level 1800, max total 9000. | Bounded, readable. |
| Score persistence | Session-only. No localStorage. | Avoids extra systems. |
| Level unlock | Linear. L1 unlocked. Completing Ln unlocks Ln+1. | Sequence of levels. |
| Canvas | Logical canvas **320×180**, integer scale, 16px tiles. | Low-resolution pixel art. |
| Camera | Side-on, clamped to level bounds, smooth follow normally, snap with reduced motion. | Required camera. |
| Input | Keyboard only. Remappable actions. | Accessibility. |
| Default keys | Left: A/ArrowLeft, Right: D/ArrowRight, Up: W/ArrowUp, Down: S/ArrowDown, Jump: Space/Z/K, Pause: Escape, Restart: R. | Standard browser platformer defaults. |
| Jump model | Single jump, no double jump, no wall jump. | Core platforming only. |
| Feel | Coyote time 0.10s, jump buffer 0.12s, variable jump cut, squash. | Makes core platforming fun. |
| Physics model | Custom fixed-step tile + body collision. No external physics engine. | Deterministic, testable, small. |
| Randomness | Seeded mulberry32 RNG only for particles and blink timing. | Deterministic tests. |
| Palette | Saturated blue/orange/yellow/magenta set, no red/green-only signals. | Colour-blind safe and bright. |
| Font | Built-in bitmap pixel font, fallback monospace, uppercase. | Required typography. |
| Screens | Title, Level Select, Settings, Playing, Paused, Win. | Exactly requested screens. |
| Level complete | Reuses **Win** screen with “NEXT LEVEL” or “GAME COMPLETE”. | Avoids adding an unlisted screen. |
| HUD | One score panel only. | HUD: score. |
| Effects | Particles and hit flash exist. Reduced motion disables particles and camera smoothing. | Required effects + accessibility. |
| Music | One chiptune loop and one win jingle. | Chiptune requested. |
| Sound effects | Synthesized retro bleeps. | Audio style requested. |
| Settings | Remap keys, reduced motion, music volume, SFX volume. | Required accessibility plus basic audio control. |
| Persistence | None. | No extra systems. |
| Testing | Tiered tests in `# 9. TESTS`. | Definition of done. |

## 0.3 Tiers

Priority order. Tier 1 is required for a playable core. Higher tiers may be left unbuilt if time runs out.

1. **Tier 1 — Core mechanics vertical slice**
   - Platforming: run, jump, climb, one-way platforms, coyote, buffer, jump cut.
   - Physics: gravity, rolling logs, bounce pads, player interaction.
   - Hazards: spikes, lava, pit/falling, dragonfly, beetle.
   - Level 1 only: one complete level with exit, death/restart.
   - Required screens minimal: Title, Level Select with only L1, Playing, Paused, Settings with defaults/reduced motion, Win for L1.
   - Art style, palette, pixel font, basic sounds, HUD score, particles, hit flash.
   - Fixed timestep, camera, deterministic RNG.

2. **Tier 2 — Full session and accessibility completion**
   - Add Levels 2–5 with final counts and difficulty.
   - Linear unlock progression.
   - Full level select UI.
   - Full pause and settings: remappable keys, volumes.
   - Win screen modes: NEXT LEVEL and GAME COMPLETE.
   - Target times, unlock state, restart behaviour across levels.
   - Full reduced-motion behaviour.

3. **Tier 3 — Collectibles extra mechanic**
   - Fly pickups, 8 per level.
   - Hidden placement patterns.
   - Fly score, all-fly bonus.
   - Score panel fly progress.
   - Win screen collection summary.

4. **Tier 4 — Polish**
   - More particles, richer idle/run/death animation, extra silly sounds, level-select collection display, optional visual flourishes.
   - No new mechanics.

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Item | Value | Notes |
| --- | --- | --- |
| Axis origin | Top-left | x increases right, y increases down |
| Logical pixel | 1px | All gameplay numbers are logical pixels |
| Tile size | 16px | All level grids use 16px tiles |
| Logical canvas | 320×180 | 16:9 |
| Canvas scale | integer scale 2–5 | CSS scaling only, no fractional scaling |
| Fixed timestep | 1/60 s = 16.6667 ms | Update only in fixed steps |
| Max steps/frame | 5 | Prevent spiral of death |
| Velocity units | px/s | Player and bodies |
| Acceleration units | px/s² | Gravity, run, friction |
| Angle units | radians | Slopes and log spin |
| Player sprite | 16×16 | Draw size |
| Player hitbox | 12×12 | Centered: x +2, y +2 |
| Spike hitbox | 16×12 | Bottom-aligned 12px top hazard |
| Lava hitbox | area | Any overlap |
| Dragonfly hitbox | 14×14 | Centered |
| Beetle hitbox | 14×12 | Centered |
| Fly sprite | 8×8 | Draw size |
| Fly hitbox | 8×8 | Exact |
| Log radius | 10px | Circle body |
| Bounce pad size | 16×8 | Static trigger |
| Ladder tile | 16×16 | Climbable |
| One-way tile | 16×8 | Top collision only |
| Exit trigger | 16×16 | Overlap 0.20s |
| Render fps | 60 | Tied to fixed step |
| Animation fps | see `# 5. CHARACTERS` | Named animations |

## 1.2 Important conventions

| Rule | Required behaviour |
| --- | --- |
| Module style | ES modules, no frameworks, no external libraries |
| Game loop | `requestAnimationFrame` accumulator with fixed 1/60 step |
| Update order | Input → state machine → player → physics → hazards → collectibles → camera → particles → render |
| Rendering | Integer pixel positions, `image-rendering: pixelated`, no anti-aliasing |
| Collision | Axis-separated AABB for tiles/player; circle vs AABB for logs |
| State | One global `game` context; modules mutate only their owned fields |
| Input | Raw keys mapped to actions; gameplay reads actions only |
| Remapping | Action names stable: `left`, `right`, `up`, `down`, `jump`, `pause`, `restart` |
| Random | `rng(seed)` only. No `Math.random`. |
| Reduced motion | When true: no particles, no camera smoothing, no squash, no screen flash except outline flash, simplified animations |
| Colour-blind safety | No information encoded only by red/green. Use shape, outline, animation. |
| Determinism | Same seed + same inputs = same physics/particle result |
| Restart | Rebuilds current level state from level definition; preserves banked score and unlock state |
| Pause | Stops all updates and timers; audio may duck but not stop unless muted |
| Win | Current level complete only on exit trigger; no auto-win on death |
| No extra systems | No combat, no power-ups, no save, no lives, no enemies defeated, no crafting, no stealth, no timers in HUD |

# 2. CONTRACTS

## 2.1 Module layout

| File | Purpose | Tier |
| --- | --- | --- |
| `index.html` | DOM screens, canvas, HUD shell | 1 |
| `styles.css` | Pixel font, palette CSS variables, screen state visibility, HUD | 1 |
| `src/main.js` | Boot, fixed loop, screen state machine wiring | 1 |
| `src/config.js` | All tunable numbers, level data, palette, default key map | 1 |
| `src/state.js` | Global game state, screen transitions, unlock state | 1 |
| `src/input.js` | Keyboard handling, action remap, buffered inputs | 1 |
| `src/level.js` | Level loading, tiles, spawn, exit, level completion | 1 |
| `src/player.js` | Frog controller, climb, death, hit flash | 1 |
| `src/physics.js` | Gravity, logs, bounce pads, body collision | 1 |
| `src/hazards.js` | Spikes, lava, pits, moving hazards | 1 |
| `src/collectibles.js` | Flies, set tracking, collection | 3 |
| `src/score.js` | Score record, level score, total score, bonuses | 1 |
| `src/camera.js` | Side-on camera clamp and follow | 1 |
| `src/particles.js` | Particles and reduced-motion gating | 1 |
| `src/audio.js` | Chiptune music and bleep SFX | 1 |
| `src/render.js` | Canvas rendering, hit flash, particles | 1 |
| `src/ui.js` | DOM screen state, settings UI, level select UI | 1 |
| `src/debug.js` | Debug API for tests and tools | 1 |
| `src/test.js` | Test harness for `# 9. TESTS` | 1 |

## 2.2 Global context

The global object is `window.game`.

| Path | Type | Owner | Required by | Notes |
| --- | --- | --- | --- | --- |
| `game.settings` | SettingsRecord | `input`, `ui` | render, audio, accessibility | Remap, reduced motion, volumes |
| `game.input` | InputRecord | `input` | player, ui | Action states, buffers |
| `game.state` | StateRecord | `state` | ui, level, render | Screen, current level, unlock |
| `game.level` | LevelRecord | `level` | player, physics, hazards, collectibles, render | Loaded level instance |
| `game.player` | PlayerRecord | `player` | physics, hazards, collectibles, render | Frog state |
| `game.physics` | PhysicsRecord | `physics` | level, player, render | Bodies and impulses |
| `game.hazards` | HazardRecord | `hazards` | player, render | Hazard instances |
| `game.collectibles` | CollectibleRecord | `collectibles` | score, render | Fly instances and counts |
| `game.score` | ScoreRecord | `score` | ui, render | Banked/current score |
| `game.camera` | CameraRecord | `camera` | render | Camera position, shake disabled |
| `game.particles` | ParticleRecord | `particles` | render | Active particles |
| `game.audio` | AudioRecord | `audio` | ui, gameplay | Music/SFX state |
| `game.ui` | UIRecord | `ui` | state | DOM focus and visible screen |
| `game.rng` | function(seed) | `config` | particles, blink | Seeded RNG factory |
| `game.time` | number seconds | `main` | all | Total fixed-step time |
| `game.fixedDt` | number | `config` | main | Always 1/60 |

## 2.3 Module specifics

### State module

| Function | Signature | Purpose | Tests |
| --- | --- | --- | --- |
| `init()` | `init()` | Set default screen `TITLE` | T2 |
| `goto(screen, mode)` | `goto(screen: ScreenName, mode?: string)` | Transition screens | T2 |
| `unlockLevel(index)` | `unlockLevel(index: number)` | Mark level unlocked | T2 |
| `isUnlocked(index)` | `isUnlocked(index: number): boolean` | Check unlock | T2 |
| `getState()` | `getState(): StateRecord` | Debug/test access | All |

### Input module

| Function | Signature | Purpose | Tests |
| --- | --- | --- | --- |
| `init()` | `init(settings)` | Bind keyboard and remap | T2 |
| `update()` | `update()` | Build per-frame action state and buffers | T1 |
| `get(action)` | `get(action: ActionName): boolean` | Current held state | T1 |
| `justPressed(action)` | `justPressed(action: ActionName): boolean` | One-frame press | T1 |
| `justReleased(action)` | `justReleased(action: ActionName): boolean` | Jump cut | T1 |
| `remap(action, key)` | `remap(action: ActionName, key: string)` | Settings remap | T2 |
| `getState()` | `getState(): InputRecord` | Debug/test | All |

### Level module

| Function | Signature | Purpose | Tests |
| --- | --- | --- | --- |
| `load(index)` | `load(index: number)` | Instantiate level from definition | T1/T2 |
| `reload()` | `reload()` | Restart current level | T1 |
| `tileAt(x,y)` | `tileAt(x: number, y: number): TileType` | Tile collision | T1 |
| `isSolidTile(type)` | `isSolidTile(type: TileType): boolean` | Collision gate | T1 |
| `isClimbTile(type)` | `isClimbTile(type: TileType): boolean` | Ladder | T1 |
| `isOneWay(type)` | `isOneWay(type: TileType): boolean` | Platforming | T1 |
| `complete()` | `complete()` | Trigger exit completion | T1 |
| `getState()` | `getState(): LevelRecord` | Debug/test | All |

### Player module

| Function | Signature | Purpose | Tests |
| --- | --- | --- | --- |
| `reset(spawn)` | `reset(spawn: Vec2)` | Spawn at level start | T1 |
| `update(dt)` | `update(dt: number)` | Platforming controller | T1 |
| `kill(reason)` | `kill(reason: string)` | Death transition | T1 |
| `isDead()` | `isDead(): boolean` | Hazard gate | T1 |
| `applyImpulse(vx, vy)` | `applyImpulse(vx: number, vy: number)` | Bounce pads | T1 |
| `getState()` | `getState(): PlayerRecord` | Debug/test | All |

### Physics module

| Function | Signature | Purpose | Tests |
| --- | --- | --- | --- |
| `addBody(body)` | `addBody(body: PhysicsBody)` | Spawn log/bounce pad | T1 |
| `removeBody(id)` | `removeBody(id: number)` | Remove fallen log | T1 |
| `update(dt)` | `update(dt: number)` | Integrate bodies and collisions | T1 |
| `applyBounce(body, impulse)` | `applyBounce(body: PhysicsBody, impulse: number)` | Bounce pad | T1 |
| `pushByPlayer(body, playerVel)` | `pushByPlayer(body: PhysicsBody, playerVel: number)` | Log push | T1 |
| `getState()` | `getState(): PhysicsRecord` | Debug/test | All |

### Hazards module

| Function | Signature | Purpose | Tests |
| --- | --- | --- | --- |
| `update(dt)` | `update(dt: number)` | Move patrol hazards | T1 |
| `checkPlayer(player)` | `checkPlayer(player: PlayerRecord): null \| string` | Death reason | T1 |
| `killAll()` | `killAll()` | Reset helper | T1 |
| `getState()` | `getState(): HazardRecord` | Debug/test | All |

### Collectibles module

| Function | Signature | Purpose | Tests |
| --- | --- | --- | --- |
| `update(dt)` | `update(dt: number)` | Animate flies | T3 |
| `checkPlayer(player)` | `checkPlayer(player: PlayerRecord): CollectibleResult \| null` | Collect | T3 |
| `resetLevel()` | `resetLevel()` | Reset collected flags | T3 |
| `getState()` | `getState(): CollectibleRecord` | Debug/test | All |

### Score module

| Function | Signature | Purpose | Tests |
| --- | --- | --- | --- |
| `add(points, reason)` | `add(points: number, reason: string)` | Add current level score | T1/T3 |
| `resetLevel()` | `resetLevel()` | Reset current level score | T1 |
| `completeLevel()` | `completeLevel()` | Bank score, unlock next | T1/T2 |
| `getState()` | `getState(): ScoreRecord` | Debug/test | All |

### Camera module

| Function | Signature | Purpose | Tests |
| --- | --- | --- | --- |
| `update(dt, player, level)` | `update(dt, player, level)` | Follow and clamp | T1 |
| `snap()` | `snap()` | Reduced motion/reset snap | T1/T2 |
| `getState()` | `getState(): CameraRecord` | Debug/test | All |

### Particles module

| Function | Signature | Purpose | Tests |
| --- | --- | --- | --- |
| `spawn(type, x, y)` | `spawn(type: string, x: number, y: number)` | Create particle burst | T1/T3 |
| `update(dt)` | `update(dt: number)` | Update and cull | T1 |
| `clear()` | `clear()` | Reduced motion/reset | T2 |
| `getState()` | `getState(): ParticleRecord` | Debug/test | All |

### Audio module

| Function | Signature | Purpose | Tests |
| --- | --- | --- | --- |
| `init()` | `init(settings)` | Create audio graph | T1 |
| `play(name)` | `play(name: string)` | SFX | T1/T3 |
| `startMusic(name)` | `startMusic(name: string)` | Chiptune loop | T1 |
| `stopMusic()` | `stopMusic()` | Stop loop | T1 |
| `setVolumes(music, sfx)` | `setVolumes(music: number, sfx: number)` | Settings | T2 |
| `getState()` | `getState(): AudioRecord` | Debug/test | All |

### Render module

| Function | Signature | Purpose | Tests |
| --- | --- | --- | --- |
| `init(canvas)` | `init(canvas: HTMLCanvasElement)` | Set pixelated context | T1 |
| `draw()` | `draw()` | Render current frame | T1 |
| `drawHitFlash()` | `drawHitFlash()` | Player flash | T1 |
| `drawParticles()` | `drawParticles()` | Particles | T1 |

### UI module

| Function | Signature | Purpose | Tests |
| --- | --- | --- | --- |
| `init()` | `init()` | Bind DOM screens | T1 |
| `show(screen, mode)` | `show(screen: ScreenName, mode?: string)` | Set `document.body.dataset.screen` | T1/T2 |
| `updateHUD()` | `updateHUD()` | Update score panel | T1/T3 |
| `renderLevelSelect()` | `renderLevelSelect()` | Show locks/unlocks | T2 |
| `renderSettings()` | `renderSettings()` | Remap controls | T2 |
| `getState()` | `getState(): UIRecord` | Debug/test | All |

# 3. VISUAL SPEC

A bright, low-resolution pond platformer seen from the side. Everything is built from 16px tiles and 16px sprites with hard black outlines, saturated blue/orange/yellow/magenta colours, and visible square pixels. Blorp is a blue tree frog with a big-eyed silly silhouette; hazards are spiky, pointy, or wiggly; collectibles are yellow flies; exits are pulsing glowing signs. The screen stays legible at a glance: solid platforms are orange, hazards are magenta, collectibles are yellow, and the player is cyan-blue.

Lighting is flat and graphic. There is no dynamic light, shadow, or gradient except a 1-frame white hit flash and a pulsing exit glow. The atmosphere is playful and bouncy: squash on landing, fluttering flies, wobbling dragonflies, and exaggerated death squash.

The space is a side-on pond: dark blue sky, orange lily pads and log platforms, magenta spike traps, magenta-pink lava pools, ladders made of vines, and glowing exit signs. The camera is clamped to level bounds and never rotates. Background is minimal: flat sky, a few darker blue silhouette clouds or reeds, no parallax, to keep pixel clarity.

### Palette

| Name | Hex | Usage |
| --- | --- | --- |
| ink | `#101010` | Outlines, text shadow |
| bg | `#071022` | Page background, black bars |
| sky | `#0b3d91` | Level sky |
| platform | `#ff8c00` | Solid platforms, lily pads |
| platform_edge | `#ffd200` | Platform top highlight |
| hazard | `#ff2d78` | Spikes, lava, moving hazard body |
| hazard_warn | `#ffe600` | Hazard warning animation |
| collectible | `#ffe600` | Flies |
| player | `#00bfff` | Frog body |
| player_belly | `#ffe600` | Frog belly |
| ui | `#ffffff` | UI text |
| ui_accent | `#00e5ff` | UI focus, exit glow |
| ladder | `#ff8c00` | Vines/ladders |
| one_way | `#ffd200` | One-way platform top |

### Visual recipe

| Element | Visual rule |
| --- | --- |
| Grid | 16px tiles, hard edges, no AA |
| Player | 16×16, cyan body, yellow belly, 1px black outline, big eyes |
| Solid platform | Orange fill, 1px yellow top, black outline |
| One-way platform | 16×8 yellow top, black bottom edge |
| Spike | 16×16 magenta triangles, 1px yellow warning pulse |
| Lava | Magenta field, yellow bubbles, animated 4-frame |
| Ladder/vine | Orange vine columns, rung every 8px |
| Dragonfly | 16×16 magenta body, cyan wings, 2-frame flutter |
| Beetle | 16×16 magenta shell, black legs, 2-frame walk |
| Fly | 8×8 yellow body, black eyes, 2-frame flutter |
| Exit | 16×16 sign, white glyph, cyan glow pulse |
| Log | 20px diameter circle, brown-orange body, black outline, spin marks |
| Bounce pad | 16×8 magenta pad, yellow top, 2-frame compress |
| HUD | Pixel font, white text, black outline, top-left |
| Particles | 1–2px squares, max 80 normally, 0 in reduced motion |
| Hit flash | Player becomes white for 0.12s; reduced motion uses black outline only |

# 4. GAMEPLAY SPEC

The player is Blorp, a blue tree frog, moving through five side-on levels by running, jumping, and climbing. The core loop is: start at a spawn, survive hazards, use physics objects such as rolling logs and bounce pads, reach the exit, unlock the next level, and continue until level 5. Death is instant and restarts the current level. Optional fly collectibles are hidden in each level and add score without blocking the exit.

## Records and rosters

### Player record

| Field | Type | Initial | Notes |
| --- | --- | --- | --- |
| `x`, `y` | number | spawn | Top-left of 16×16 sprite |
| `vx`, `vy` | number | 0 | px/s |
| `facing` | `-1 \| 1` | 1 | Render flip |
| `grounded` | boolean | false | Tile contact |
| `coyote` | number | 0 | Timer |
| `jumpBuffer` | number | 0 | Timer |
| `climbing` | boolean | false | Ladder state |
| `dead` | boolean | false | Death transition |
| `deathTimer` | number | 0 | 0.75s |
| `hitFlash` | number | 0 | 0.12s |
| `squash` | number | 0 | Non-reduced motion |
| `anim` | string | `idle` | Current animation |
| `animTimer` | number | 0 | Frame timer |

### Level record

| Field | Type | Notes |
| --- | --- | --- |
| `index` | number 0–4 | Level id |
| `name` | string | Display name |
| `width`, `height` | tiles | Grid size |
| `tiles` | TileType[][] | Solid, one-way, ladder, spike, lava, empty |
| `spawn` | Vec2 tile | Player spawn |
| `exit` | Vec2 tile | Exit trigger |
| `hazards` | HazardInstance[] | Static and moving hazards |
| `physicsBodies` | PhysicsBody[] | Logs, bounce pads |
| `collectibles` | CollectibleInstance[] | Flies |
| `targetSeconds` | number | Design target |

### Level roster

| Level | ID | Width×Height | Spawn tile | Exit tile | Target |
| --- | --- | --- | --- | --- | --- |
| Pond Steps | 1 | 40×18 | 2,15 | 36,6 | 180s |
| Log Roll | 2 | 56×18 | 2,15 | 51,7 | 240s |
| Lily Bounce | 3 | 64×20 | 2,17 | 59,6 | 300s |
| Moss Climb | 4 | 72×22 | 2,19 | 67,4 | 360s |
| Fly Feast | 5 | 80×24 | 2,21 | 75,5 | 420s |

### Level content counts

| Level | Solid platforms | One-way | Ladders | Spikes | Lava | Pits | Dragonflies | Beetles | Logs | Bounce pads | Flies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 12 | 3 | 1 | 4 | 0 | 2 | 0 | 0 | 1 | 1 | 8 |
| 2 | 18 | 5 | 0 | 6 | 0 | 4 | 2 | 0 | 3 | 1 | 8 |
| 3 | 22 | 7 | 0 | 8 | 1 | 5 | 2 | 0 | 2 | 5 | 8 |
| 4 | 24 | 6 | 3 | 10 | 0 | 4 | 2 | 3 | 2 | 3 | 8 |
| 5 | 28 | 8 | 4 | 12 | 2 | 6 | 3 | 4 | 4 | 5 | 8 |
| Total | 104 | 29 | 8 | 40 | 3 | 21 | 9 | 7 | 12 | 15 | 40 |

### Hazard roster

| Type | Size | Behaviour | Count |
| --- | --- | --- | --- |
| Spike | 16×16 | Static instant death | 40 |
| Lava | area | Area instant death | 3 |
| Pit | level bottom +64 | Falling death | 21 |
| Dragonfly | 16×16 | Patrol 48–96px at 80px/s | 9 |
| Beetle | 16×16 | Walk platform at 60px/s, reverse edge/wall | 7 |

### Physics object roster

| Type | Size | Count | Use |
| --- | --- | --- | --- |
| Rolling log | radius 10 | 12 | Push, ride, bridge |
| Bounce pad | 16×8 | 15 | Launch to higher areas |

### Collectible roster

| Type | Count per level | Total | Placement pattern |
| --- | --- | --- | --- |
| Fly | 8 | 40 | 2 obvious, 3 hidden alcove, 3 physics/climb |

## 4.1 Platforming — Tier 1

| Rule | Number |
| --- | --- |
| Actions | `left`, `right`, `up`, `down`, `jump` |
| Ground detection | Player bottom overlaps solid tile top with y velocity >= 0 |
| Max run speed | 200 px/s |
| Ground run acceleration | 2400 px/s² |
| Air run acceleration | 1600 px/s² |
| Ground friction | 1800 px/s² when no horizontal input |
| Air drag | 200 px/s² |
| Gravity | 1600 px/s² |
| Max fall speed | 900 px/s |
| Jump velocity | -420 px/s |
| Variable jump cut | If `jump` released before apex, `vy *= 0.45` |
| Coyote time | 0.10s after leaving ground |
| Jump buffer | 0.12s before landing |
| Jump height | 55px, about 3.4 tiles |
| Max jump distance | 105px, about 6.5 tiles |
| One-way platforms | Land from above only |
| Drop-through | Hold `down` 0.25s while on one-way |
| Climb tile overlap | Ladder/vine tile |
| Climb speed | 120 px/s vertical |
| Ladder exit jump | Press `jump` on ladder: leave ladder, `vy = -380` |
| Facing | Flip when horizontal input held |
| Death restart | 0.75s after death |

## 4.2 Physics — Tier 1

| Rule | Number |
| --- | --- |
| Global gravity | 1600 px/s² |
| Body integration | Fixed step, Euler |
| Log radius | 10px |
| Log mass | 1 |
| Log linear friction | 0.8/s |
| Log angular damping | 0.8/s |
| Log restitution vs wall | 0.0 |
| Log restitution vs player | 0.1 |
| Log push impulse | `log.vx += player.vx * 0.25`, clamp to ±120px/s |
| Log angular velocity | `log.vx / radius` |
| Player riding log | If player bottom within 4px of log top and vy >= 0, grounded, inherit log vx |
| Log removal | Center y > level height + 32 |
| Bounce pad impulse | -700 px/s vertical |
| Bounce pad cooldown | 0.25s per pad |
| Bounce pad affects logs | Impulse -500 px/s |
| Physics goal use | Logs bridge pits and create platforms; bounce pads reach one-way ledges |

## 4.3 Hazards — Tier 1

| Rule | Number |
| --- | --- |
| Spike collision | Player hitbox overlap = death |
| Lava collision | Player hitbox overlap = death |
| Pit death | Player y > level height + 64 |
| Dragonfly speed | 80 px/s |
| Dragonfly patrol | 48–96px endpoints, reverse at endpoints |
| Beetle speed | 60 px/s |
| Beetle reversal | Solid wall or platform edge |
| Hazard contact response | Set `hitFlash=0.12`, spawn death particles, play death/hazard sound, enter death transition |
| Death transition | Freeze input, animate death 3 frames, restart level after 0.75s |
| Restart state | Reset player, physics, hazards, collectibles, camera, particles; keep banked score and unlock |

## 4.4 Collectibles — Tier 3

| Rule | Number |
| --- | --- |
| Fly score | +100 |
| All-fly bonus | +500 after 8/8 in current level |
| Exit score | +500 |
| Max per level | 1800 |
| Max total | 9000 |
| Required for exit | No |
| Reset on restart | Collected flags and current level score reset |
| Hidden placement | 2 obvious, 3 hidden alcoves, 3 physics/climb |
| Collection effect | Fly disappears, yellow particle burst, collect sound |
| Set complete effect | All-fly sound, win screen shows “FLY SET COMPLETE” |

## Progression and difficulty

| Level | Teaching | Difficulty |
| --- | --- | --- |
| 1 | Run, jump, one-way, ladder, one log, one bounce pad, spikes | Very low |
| 2 | Logs across pits, dragonflies, longer gaps | Low |
| 3 | Bounce pad chains, lava, hidden flies | Medium |
| 4 | Ladders, beetles, combined climb/log/bounce | Medium-high |
| 5 | All systems, tight timing, many hazards, full fly set | High |

## Feel

| Feel rule | Number |
| --- | --- |
| Input responsiveness | Action state built each fixed step |
| Coyote | 0.10s |
| Buffer | 0.12s |
| Jump cut | 0.45 multiplier |
| Landing squash | Non-reduced: scale y 0.85, x 1.15 for 0.12s |
| Death squash | 3 frames, 100ms each |
| Hit flash | 0.12s white overlay |
| Reduced motion | No squash, no particles, no camera smoothing, outline flash only |
| Camera smoothing | Normal x lerp 12/s, y lerp 8/s; reduced motion snaps |

# 5. CHARACTERS

## Blorp — player

| State | Silhouette | Animation | Facing | Gameplay states |
| --- | --- | --- | --- | --- |
| idle | Squat, wide, big eyes, short legs | `idle_breathe` 2 frames, 600ms/frame; blink every 4–8s | left/right | `grounded` |
| run | Body leans forward, legs cycle | `run` 4 frames, 8fps | left/right | `grounded`, `abs(vx)>30` |
| jump | Tucked upward, limbs up | `jump` 1 frame | left/right | `vy < 0` |
| fall | Limbs spread, worried | `fall` 1 frame | left/right | `vy > 0` |
| climb | Limbs gripping vine | `climb` 2 frames, 4fps | left/right | `climbing` |
| death | Squashed X-eyes, tongue out | `death` 3 frames, 100ms/frame | last facing | `dead` |
| hit flash | White silhouette | 0.12s overlay | any | `hitFlash>0` |

## Dragonfly — hazard

| State | Silhouette | Animation |
| --- | --- | --- |
| patrol | Long magenta body, cyan wings | `patrol` 2-frame wing flutter, 8fps, 1px body bob |
| death | None | No defeat state |

## Beetle — hazard

| State | Silhouette | Animation |
| --- | --- | --- |
| patrol | Round magenta shell, black legs | `walk` 2-frame legs, 6fps, reverse on edge/wall |
| death | None | No defeat state |

## Fly — collectible

| State | Silhouette | Animation |
| --- | --- | --- |
| idle | Yellow 8×8 body, black eyes | `flutter` 2 frames, 10fps |
| collected | None | Removed, particles |

## Exit

| State | Silhouette | Animation |
| --- | --- | --- |
| idle | Sign with cyan glow | `pulse` 3 frames, 4fps |
| triggered | Flash white | 0.20s before completion |

# 6. AUDIO

All audio is synthesized with Web Audio oscillators/noise. No external audio files.

| Name | Recipe | Trigger |
| --- | --- | --- |
| `music_pond` | 140 BPM square lead, notes A4 C5 E5 A4, triangle bass A2, noise hats, 4-bar loop | Title and Playing |
| `music_win` | 120 BPM arpeggio G4 B4 D5 G5, square, triangle bass, 2 bars | Win screen |
| `sfx_jump` | square 440→660Hz, 0.08s, gain 0.15 | Jump press |
| `sfx_land` | triangle 110Hz decay, 0.06s, gain 0.12 | Landing with vy > 200 |
| `sfx_climb` | square 500Hz, 0.03s, gain 0.06 | Climb frame every 0.2s |
| `sfx_bounce` | sine 180→720Hz, 0.12s, gain 0.20 | Bounce pad |
| `sfx_log_push` | triangle 90Hz, 0.05s, gain 0.10 | Player pushes log |
| `sfx_log_roll` | square 70Hz vibrato, loop, gain 0.08 | Log vx > 50 |
| `sfx_hazard` | sawtooth 220→110Hz, 0.15s, gain 0.20 | Hazard contact |
| `sfx_death` | sawtooth 300→60Hz, 0.40s, gain 0.25 | Death transition |
| `sfx_collect` | square arpeggio 880/1174/1568Hz, 0.04s each, gain 0.18 | Fly collect |
| `sfx_fly_set` | square arpeggio C6/E6/G6/C7, 0.25s, gain 0.22 | 8/8 flies |
| `sfx_exit` | square arpeggio G4/B4/D5/G5, 0.40s, gain 0.25 | Exit triggered |
| `sfx_menu_move` | square 660Hz, 0.04s, gain 0.10 | UI navigation |
| `sfx_menu_select` | square 880Hz, 0.08s, gain 0.15 | UI confirm |
| `sfx_pause` | square 520→390Hz, 0.08s, gain 0.15 | Pause open |
| `sfx_unpause` | square 390→520Hz, 0.08s, gain 0.15 | Pause close |
| `sfx_error` | square 220Hz, 0.12s, gain 0.18 | Invalid remap |

# 7. UX

Screens are HTML/CSS only. The game canvas is a `<canvas>` element; DOM screens overlay the canvas. The body has `data-screen` set by `ui.show()`. CSS controls visibility.

## Screen state machine

| State | Entry | Input | Exit | Notes |
| --- | --- | --- | --- | --- |
| `TITLE` | Boot | `jump`/confirm | `LEVEL_SELECT` | Shows game name, controls hint |
| `LEVEL_SELECT` | From title or win | arrow keys + confirm | `PLAYING` | Locked levels disabled |
| `SETTINGS` | From title or pause | key capture, toggles | previous screen | Remap, reduced motion, volumes |
| `PLAYING` | Level select | gameplay keys | `PAUSED`, `WIN`, internal death | Updates fixed step |
| `PAUSED` | `pause` during play | resume/settings/restart/quit | `PLAYING`, `SETTINGS`, `LEVEL_SELECT` | Time stopped |
| `WIN` | Exit triggered | next/replay/select | `PLAYING` next level, `LEVEL_SELECT`, or `TITLE` | If L5, shows game complete |

## HTML/CSS contract

| Element | Attribute | Visibility rule |
| --- | --- | --- |
| `#title` | `data-screen="title"` | visible only on TITLE |
| `#level-select` | `data-screen="level-select"` | visible only on LEVEL_SELECT |
| `#settings` | `data-screen="settings"` | visible only on SETTINGS |
| `#playing-hud` | `data-screen="playing"` | visible only on PLAYING |
| `#paused` | `data-screen="paused"` | visible only on PAUSED |
| `#win` | `data-screen="win"` | visible only on WIN |
| `canvas` | always present | behind DOM screens, active during PLAYING/PAUSED |

## HUD

Only one HUD element exists: the score panel.

| Element | Record field | Visible when | Notes |
| --- | --- | --- | --- |
| `#score-panel` | `score.totalScore`, `score.currentFlies`, `game.level.flyTotal` | `data-screen="playing"` | Shows total score; fly progress is part of score panel |

# 8. DEBUG API

All debug functions are on `window.debug`.

| Function | Purpose |
| --- | --- |
| `debug.input.getState()` | Read input record |
| `debug.input.leftDown()` | Simulate left press |
| `debug.input.leftUp()` | Simulate left release |
| `debug.input.rightDown()` | Simulate right press |
| `debug.input.rightUp()` | Simulate right release |
| `debug.input.upDown()` | Simulate up press |
| `debug.input.upUp()` | Simulate up release |
| `debug.input.downDown()` | Simulate down press |
| `debug.input.downUp()` | Simulate down release |
| `debug.input.jumpDown()` | Simulate jump press |
| `debug.input.jumpUp()` | Simulate jump release |
| `debug.input.pausePress()` | Simulate pause |
| `debug.input.restartPress()` | Simulate restart |
| `debug.player.getState()` | Read player record |
| `debug.player.setState(partial)` | Force player state for tests |
| `debug.level.getState()` | Read loaded level |
| `debug.level.load(index)` | Load level |
| `debug.level.forceExit()` | Trigger exit |
| `debug.physics.getState()` | Read bodies |
| `debug.physics.addLog(x,y)` | Add test log |
| `debug.physics.addBouncePad(x,y)` | Add test bounce pad |
| `debug.hazards.getState()` | Read hazards |
| `debug.hazards.addSpike(x,y)` | Add test spike |
| `debug.collectibles.getState()` | Read flies |
| `debug.collectibles.collect(id)` | Force collect |
| `debug.score.getState()` | Read score |
| `debug.score.add(n, reason)` | Add score |
| `debug.camera.getState()` | Read camera |
| `debug.particles.getState()` | Read particles |
| `debug.audio.getState()` | Read audio state |
| `debug.ui.getState()` | Read UI screen |

# 9. TESTS

## Tier 1 tests

| Test | Steps | Pass |
| --- | --- | --- |
| Fixed loop | Run 600 frames | Exactly 600 fixed updates, no drift |
| Input actions | Simulate left/right/jump | `input.get` and `justPressed` correct |
| Run speed | Hold right 0.15s | vx ≈ 200 |
| Jump height | Jump from flat ground | max rise ≈ 55px |
| Coyote | Leave edge, press jump within 0.10s | jump succeeds |
| Buffer | Press jump 0.10s before landing | jump succeeds |
| Climb | Enter ladder, hold up/down | vertical speed 120px/s |
| One-way | Jump through below, land on top | grounded on top |
| Death restart | Overlap spike | death after flash, level reloads |
| Pit death | Fall below level height +64 | death |
| Physics log push | Walk into log | log vx changes |
| Log ride | Stand on log | player inherits log vx |
| Bounce pad | Touch pad | vy ≈ -700 |
| Exit | Overlap exit 0.20s | Win screen shown |
| HUD score | Complete level | score panel shows +500 |

## Tier 2 tests

| Test | Steps | Pass |
| --- | --- | --- |
| Unlock progression | Complete L1 | L2 unlocked |
| Level roster | Load each level | counts match table |
| Target times | Simulated playtest | total target ≤ 25 minutes |
| Remap | Bind jump to `x` | `x` triggers jump |
| Remap conflict | Bind duplicate key | error, no change |
| Reduced motion | Toggle on | no particles, camera snap, no squash |
| Pause | Press pause | updates stop, resume works |
| Settings volumes | Change volumes | audio gain changes |
| Win modes | Complete L1/L5 | L1 shows NEXT, L5 shows GAME COMPLETE |

## Tier 3 tests

| Test | Steps | Pass |
| --- | --- | --- |
| Fly count | Load each level | 8 flies |
| Fly collect | Touch fly | +100, count increments |
| Set bonus | Collect 8 | +500, set sound |
| Optional exit | Exit with 0 flies | level completes |
| Restart reset | Collect 3, restart | fly count resets |
| Total max | Collect all, complete all | score 9000 |

# 10. BUILD ORDER

1. Create HTML/CSS shell, pixel font, palette variables, fixed loop.
2. Implement global context, state machine, screen visibility.
3. Implement input actions, default map, remap data.
4. Implement tile collision and one platforming level block.
5. Implement player: run, jump, coyote, buffer, jump cut.
6. Implement ladder climb and one-way platforms.
7. Implement camera clamp/follow.
8. Implement spikes, lava, pit death.
9. Implement physics logs and bounce pads.
10. Implement level 1 with exit and death/restart.
11. Add basic particles, hit flash, sounds.
12. Add HUD score panel.
13. Add title, level select, pause, settings, win screens.
14. Add levels 2–5 with exact counts.
15. Add unlock progression and full settings.
16. Add collectibles and score bonuses.
17. Run tests by tier and polish.

# 11. DEFINITION OF DONE

## Tier 1 — Core playable vertical slice

High level: The player can start, play one level, use platforming, physics, and hazards, die and restart, and reach the exit.

- [ ] Fixed 1/60 loop works
- [ ] Player runs at 200px/s
- [ ] Player jumps 55px high
- [ ] Coyote and buffer work
- [ ] Ladders climb at 120px/s
- [ ] One-way platforms work
- [ ] Spikes/lava/pits kill
- [ ] Death restarts level after 0.75s
- [ ] Logs push/ride/fall
- [ ] Bounce pads apply -700px/s
- [ ] Exit triggers after 0.20s
- [ ] Title, level select, playing, pause, settings, win screens exist
- [ ] HUD score panel exists
- [ ] Pixel art and palette are used
- [ ] Basic particles and hit flash work
- [ ] Basic audio plays

## Tier 2 — Full session

High level: Five levels can be played in sequence with unlock, settings, and accessibility.

- [ ] All five level definitions load
- [ ] Level counts match roster tables
- [ ] Completing Ln unlocks Ln+1
- [ ] Level select shows locked/unlocked
- [ ] Win screen supports next level and game complete
- [ ] Remappable keys work
- [ ] Reduced motion disables particles/camera smoothing/squash
- [ ] Pause and settings work from title and gameplay
- [ ] Target total time ≤ 30 minutes

## Tier 3 — Collectibles

High level: Flies are optional set pickups that score but never block exit.

- [ ] 8 flies per level
- [ ] Hidden placement pattern exists
- [ ] Collecting fly adds +100
- [ ] All-fly bonus adds +500
- [ ] Exit works with 0 flies
- [ ] Restart resets fly collection
- [ ] Max score 9000 possible

## Tier 4 — Polish

High level: The game feels more alive without adding mechanics.

- [ ] More particles exist
- [ ] Idle/run/death animations are complete
- [ ] Audio is richer
- [ ] Win screen shows collection summary
- [ ] Level select can show collection counts

# A. SANITY

| Check | Result |
| --- | --- |
| All requested high-level decisions appear | Valid. Every requested item is mapped in `# 0.1 Asked`. |
| No supporting mechanics added | Valid. No combat, power-ups, crafting, stealth, lives, save, or enemy defeat. |
| Core mechanics are tier 1 | Valid. Platforming, physics, hazards are tier 1. |
| Collectibles are tier 3 | Valid. Extra mechanic tier is 3. |
| Screens exactly requested | Valid. Title, Level Select, Settings, Playing, Paused, Win. No separate level-complete screen. |
| HUD only score | Valid. One score panel. |
| Failure restarts level | Valid. Death transition reloads current level. |
| Win is exit only | Valid. Exit trigger completes level; collectibles optional. |
| Level count and time under 30 minutes | Valid. 5 levels, 25 minutes target. |
| Enemy/trap/pickup numbers concrete | Valid. Exact counts in level content counts. |
| Physics used to reach goals | Valid. Logs and bounce pads are required for many routes. |
| Climbing included | Valid. Ladders with numbers. |
| Side-on 2D camera | Valid. Clamped side camera. |
| Real-time fixed loop | Valid. 1/60 fixed step. |
| Free movement | Valid. Continuous velocity, no grid movement. |
| Pixel art and saturated palette | Valid. 16px tiles, palette table, no AA. |
| Colour-blind safe | Valid. Blue/orange/yellow/magenta, shape/outline signals. |
| Reduced motion | Valid. Disabled particles, camera smoothing, squash, screen flash. |
| Remappable keys | Valid. Action remap and tests. |
| Score max bounded | Valid. 9000 max. |
| Numbers internally consistent | Valid after checking level counts, score values, and target times. |