# 0. SCOPE
## 0.1 Asked
| Requirement | Where it lives |
| --- | --- |
| Platformer where you play as a frog | #4 GAMEPLAY SPEC, #5 CHARACTERS |
| 2D side-on camera | #1 CONVENTIONS, #3 VISUAL SPEC, #4 Map / World |
| Real-time time model | #1 CONVENTIONS, #2 CONTRACTS |
| Free movement model | #4 Player movement, #4 Jump, #4 Swim, #4 Dash |
| Sequence of levels | #4 Progression and difficulty |
| Failure restarts the level | #4 Falling, #4 Spawn Points, #7 UX |
| Silly tone | #0.2 Decisions, #3 VISUAL SPEC, #5 CHARACTERS, #6 AUDIO |
| Handful of levels, under 30 minutes | #4 Progression and difficulty |
| Win/lose: reach the exit | #4 Objectives, #4 Falling |
| Core mechanics: jump, objectives, falling, map / world, bounce | #0.3 Tiers, #4 Systems |
| Supporting mechanics: traps, environmental damage, physics objects, swim, enemies, difficulty ramp, abilities / special moves, dodge, spawn points, climb, unlocks | #0.3 Tiers, #4 Systems |
| Extra mechanics: landmarks, dash, rewards, decoration, switches and doors, puzzle types, secrets, hints, boosts, collectibles, throw, score, guards, flee, keys and locked doors, push and pull, transform, collectible creatures, combos, medals / ranks | #0.3 Tiers, #4 Systems |
| Pixel art: low-resolution sprites with visible square pixels and limited palette | #3 VISUAL SPEC, #1 CONVENTIONS |
| Saturated palette: bright, strong colours | #3 VISUAL SPEC |
| Pixel font: blocky bitmap letters | #3 VISUAL SPEC, #7 UX |
| Chiptune music: retro console bleeps | #6 AUDIO |
| Retro bleep sound effects: synthesized chip sounds | #6 AUDIO |
| Screens: title, pause, settings, game over, win, level select, high scores | #7 UX |
| HUD: score | #7 UX |
| Effects: screen shake, particles, hit flash | #4 Feel, #3 VISUAL SPEC |
| Accessibility: colour-blind safe palette, reduced motion, remappable keys | #0.2 Decisions, #3 VISUAL SPEC, #7 UX, #8 DEBUG API |

## 0.2 Decisions
| Decision | Ruling | Why |
| --- | --- | --- |
| Game title | Brib the Gummy Frog | Gives the frog an identity and a silly tone. |
| Player character | Brib, a gummy lilac-green frog with a cream belly | Clear silhouette, silly but readable. |
| World name | Gummy Lagoon | One place for all 6 levels. |
| Level count | 6 levels | A handful, not too many, under 30 minutes. |
| Target playtime | 24 minutes first clear, 18 minutes skilled clear | Under 30 minutes with room for retries. |
| Failure model | One-hit death, full level reset | Matches “restart the level” and avoids unlisted health/lives. |
| Win model | Overlap Exit Pad | Matches “reach the exit”. |
| No health, no lives, no timer | Frog dies once from hazards; score and medals track skill | Keeps scope tight and matches the fixed win/lose rule. |
| Canvas resolution | 640 x 360, 16 px tiles, integer scaling | Pixel art stays crisp and side-on. |
| Tile size | 16 px | Low-resolution sprite target. |
| Frame rate | 60 Hz fixed step | Real-time and testable. |
| Coordinate system | x right, y down | Standard 2D screen convention. |
| Speed units | px/frame at 60 fps | Easy to tune and test. |
| Player hitbox | 12 x 14 px default | Slim enough for gaps, big enough to see. |
| Move speed | 1.9 px/frame | Snappy frog movement. |
| Acceleration | 0.35 px/frame² | Responsive but not floaty. |
| Friction | vx *= 0.7 when no input | Quick stop. |
| Gravity | 0.45 px/frame² | Standard platformer arc. |
| Max fall | 9.0 px/frame | Prevents tunneling and sudden drops. |
| Jump velocity | -5.6 px/frame | Reaches 2.2 tiles. |
| Coyote time | 6 frames | Forgiving edge jumps. |
| Jump buffer | 6 frames | Forgiving early presses. |
| Variable jump | Release jump while rising: vy *= 0.55 once | Short hops feel controllable. |
| Air Bounce velocity | -6.4 px/frame | Higher than jump, once per air arc. |
| Bounce Pad velocity | -7.8 px/frame | Very high launch, core fun. |
| Air Bounce reset | Ground, Bounce Pad, or exiting water with vy < -2.0 | Prevents stale bounces. |
| Falling death | player.y > level.height * 16 + 32 | Simple pit rule. |
| One-way lily pads | Collide from above only; Drop Through is Down + Jump | Adds map variety without breaking Jump. |
| Camera | Viewport 640 x 360, deadzone 120 x 80, lerp 0.18, clamped to level | Side-on follow without jitter. |
| Screen shake | Death 2 px for 6 frames; bounce 1 px for 3 frames; hit 1 px for 4 frames | Effects decision, tuned small. |
| Reduced motion | Disables screen shake, parallax motion, reduces particles by 75%, hit flash becomes 1 frame | Accessibility without removing feedback. |
| Colour-blind safe palette | 16 saturated colours; danger is orange, poison is magenta, water is blue, collectibles are yellow; hazards use icons and luminance differences | Avoids red/green-only signalling. |
| Limited palette | Exactly 16 game colours plus UI white | Matches pixel art decision. |
| Pixel font | “PixelFrog8”, a bundled 8 x 8 bitmap font, CSS fallback “Press Start 2P”, monospace | Blocky bitmap letters. |
| Audio engine | WebAudio synthesized sounds, no external samples | Matches retro bleeps and keeps build self-contained. |
| Music | One chiptune main loop, 140 BPM, square lead, triangle bass, noise hats | Retro console feel. |
| Default gameplay keys | Left: A / ArrowLeft, Right: D / ArrowRight, Jump: W / ArrowUp / Space, Down: S / ArrowDown, Throw: X, Slap: L, Dash: K, Transform: C, Pull: E, Pause: P / Escape | Common browser keys, remappable. |
| Remappable keys | Settings stores one remapped key per gameplay action; defaults remain until remapped | Accessibility decision. |
| Settings contents | Reduced motion on/off, key remap, audio volume 0-100 | Keeps settings screen useful without adding gameplay systems. |
| Level unlock | Sequential: completing level N unlocks N+1 | Session shape is a sequence of levels. |
| Level select | Shows all 6; only unlocked levels are selectable | Uses the required screen without adding lives/permadeath. |
| High scores | Top 10 total scores, saved locally | Required screen, simple persistence. |
| Score persistence | Total score persists across levels in a run; death resets score to level start score | Keeps retry fair. |
| Medal rule | Bronze: clear; Silver: clear and at least 50% of level gems; Gold: clear, all gems, no death | Avoids arbitrary score thresholds and uses listed collectibles. |
| Rank rule | 0-2 medals: Puddle Rookie, 3-5: Lily Lancer, 6: Giggle Grandmaster | Simple final rank. |
| Enemy roster | Slug Snot, Zippy Dragonfly, Puff Beetle, Toad Guard, Puddler Flee | Covers enemies, guards, flee. |
| Trap roster | Spike Vine, Drop Brick, Geyser Jet | Covers traps without adding unlisted systems. |
| Environmental damage roster | Poison Sludge, Steam Vent, Electric Pad | Concrete damage zones. |
| Physics object roster | Falling Lily Pad, Mushroom Crate, Wobble Mushroom | Covers physics objects, push/pull, secrets. |
| Pickup roster | Lily Gem, Honey Shroom, Key, Guppy Buddy | Covers collectibles, boosts, keys, collectible creatures. |
| Switch/door roster | Switch Pad, Door, Key Door | Covers switches and doors, keys and locked doors. |
| Hint roster | Hint Stump with one text per level | Covers hints. |
| Secret rule | 1 secret in levels 3-6; secret gives +250 score and 1 Honey Shroom | Avoids tier dependency on Guppy Buddy. |
| Transform effect | Puff Toad: 180 frames, 1-hit shield, no Air Bounce, 2x push strength | Gives transform a clear risk/reward. |
| Guppy Buddy duration | 1200 frames, absorbs one kill source, then disappears | Gives collectible creatures a clear role. |
| Combo multiplier | Max x5, window 90 frames, resets on death | Gives combos teeth without health. |
| Throw pea | Unlimited with 30-frame cooldown | No unlisted inventory. |
| Slap | 45-frame cooldown, stuns enemies, breaks fragile objects | Supports “abilities / special moves” without duplicating Throw. |
| Dodge | Crouch dodge with Down, 12 frames, 27-frame cooldown | Uses Down for sink/drop without adding a separate roll system. |
| Landmark interaction | Hold Jump within 16 px for 30 frames to inspect | Gives landmarks a named input without collision. |
| Decoration | Non-interactive background props; Move changes the camera viewpoint | Keeps decoration decorative. |
| No external assets | All sprites drawn from palette, all audio synthesized | Builder can finish in browser. |
| Random source | mulberry32 seeded per level | Deterministic tests. |
| Collision | Axis-aligned bounding boxes only, no rotation | Simple, testable, pixel-friendly. |
| Save key | localStorage “brib_gummy_frog_v1” | Simple local persistence. |
| UI implementation | DOM overlays over canvas, HTML/CSS only | Matches UX constraint. |

## 0.3 Tiers
| Tier | Name | Systems included | Done means |
| --- | --- | --- | --- |
| 1 | Core Hop | Jump, Objectives, Falling, Map / World, Bounce | A player can enter Level 1, move, jump, bounce, fall, reach the Exit, win, and restart on failure. |
| 2 | Survival | Traps, Environmental Damage, Physics Objects, Swim, Enemies, Difficulty Ramp, Abilities / Special Moves, Dodge, Spawn Points, Climb, Unlocks | A player can finish Levels 2-4 with hazards, swim, climb, enemies, physics objects, and level unlock. |
| 3 | World | Landmarks, Dash, Rewards, Decoration, Switches and Doors, Puzzle Types, Secrets, Hints, Boosts, Collectibles, Throw, Score, Keys and Locked Doors | A player can finish Levels 5-6 with score, collectibles, doors, keys, switches, puzzles, secrets, hints, boosts, dash, throw, landmarks, and decoration. |
| 4 | Full Meta | Guards, Flee, Push and Pull, Transform, Collectible Creatures, Combos, Medals / Ranks | The full 6-level game is complete with advanced enemies, push/pull, transform, creatures, combos, medals, ranks, and high scores. |

# 1. CONVENTIONS
## 1.1 Units, axes, frames
| Quantity | Value | Notes |
| --- | ---: | --- |
| x axis | right positive | Side-on camera. |
| y axis | down positive | Gravity positive y. |
| Frame | 1/60 second | Fixed step. |
| Tile | 16 px | All map tiles. |
| Canvas | 640 x 360 px | Internal render size. |
| Scale | integer only | No smoothing. |
| Speed | px/frame | Player, enemies, projectiles. |
| Acceleration | px/frame² | Applied each fixed frame. |
| Timers | frames | Use integer frame counters. |
| Player default hitbox | 12 x 14 px | Brib. |
| Player crouch hitbox | 10 x 8 px | Dodge. |
| Puff Toad hitbox | 18 x 12 px | Transform. |
| Pea projectile | 4 x 4 px | Throw. |
| Gem | 8 x 8 px | Collectible. |
| Guppy Buddy | 8 x 6 px | Collectible creature. |
| Slug Snot | 14 x 10 px | Enemy. |
| Zippy Dragonfly | 12 x 10 px | Enemy. |
| Puff Beetle | 12 x 12 px | Enemy. |
| Toad Guard | 14 x 14 px | Enemy guard. |
| Puddler Flee | 10 x 8 px | Flee enemy. |
| Switch Pad | 16 x 8 px | Trigger. |
| Door | 16 x 16 px | Solid when closed. |
| Key | 8 x 8 px | Pickup. |
| Honey Shroom | 12 x 12 px | Boost pickup. |
| Secret area | at least 24 x 24 px | Hidden space. |
| Landmark | 32 x 32 to 48 x 48 px | Background object. |

## 1.2 Important conventions
- The game loop is fixed step at 60 Hz. Render may run at display refresh, but gameplay updates only on accumulated frames.
- Maximum 5 fixed updates per rendered frame. If more are needed, drop the excess time.
- Use one global context object `G`. No gameplay state lives outside `G` except module constants.
- All random numbers come from `G.rng`, a `mulberry32` instance. Level load sets `G.rng = createRng(level.seed)`.
- Collision is AABB only. No rotation, no circles, no physics solver.
- Player movement is independent of camera. Camera does not change hitboxes.
- `G.frame` increments once per fixed update.
- Death always resets the current level to its initial state and places the player at the Level Spawn.
- `G.score.value` persists across levels in a run. On death, it returns to `G.run.levelStartScore`.
- Reduced motion is a global setting. It changes effects only, not rules.
- Colour-blind safety is achieved by palette, luminance, and iconography, not by hue alone.
- UI is HTML/CSS overlays. Canvas renders the game world.
- All sounds are synthesized at runtime. No external audio files.
- All sprites are generated from the 16-colour palette at load time.
- Input actions are edge-detected unless a system says “hold”.
- Settings remap gameplay actions. UI navigation keys remain fixed: arrows/WASD navigate, Enter/Space confirm, Escape cancels.

# 2. CONTRACTS
## 2.1 Module layout
| File / Module | Purpose |
| --- | --- |
| `index.html` | Canvas, UI overlays, module script includes. |
| `style.css` | Pixel font, canvas scaling, screens, HUD, reduced motion. |
| `js/main.js` | Boot, fixed-step loop, state changes, save/load glue. |
| `js/config.js` | Constants: physics, timers, palette, level data. |
| `js/rng.js` | `mulberry32` deterministic RNG. |
| `js/input.js` | Key state, remapping, action queries. |
| `js/level.js` | Level data, loading, reset, unlock, medals. |
| `js/tilemap.js` | Tile queries, collision flags, one-way rules. |
| `js/physics.js` | AABB, movement, gravity, bounce, death, win. |
| `js/player.js` | Player update and named actions. |
| `js/enemies.js` | Enemy update, contact, stun, kill, guard/flee AI. |
| `js/traps.js` | Trap update, trigger, contact. |
| `js/physicsObjects.js` | Falling pads, crates, wobbles, push/pull. |
| `js/collectibles.js` | Gems, boosts, keys, creatures. |
| `js/doors.js` | Switches, doors, key doors. |
| `js/score.js` | Score, combo, rewards. |
| `js/effects.js` | Particles, float text, screen shake, hit flash. |
| `js/audio.js` | WebAudio synthesis, music, SFX. |
| `js/ui.js` | Screens, HUD, state machine input. |
| `js/save.js` | LocalStorage run and high scores. |
| `js/debug.js` | Debug API and test input functions. |
| `js/tests.js` | High-level tier tests. |

## 2.2 Global context
| Field | Type | Meaning |
| --- | --- | --- |
| `G.canvas` | HTMLCanvasElement | 640 x 360 canvas. |
| `G.surface` | CanvasRenderingContext2D | 2D context, `imageSmoothingEnabled = false`. |
| `G.audio` | object | Audio system. |
| `G.input` | object | Input system. |
| `G.rng` | object | Deterministic RNG. |
| `G.frame` | number | Fixed update count. |
| `G.state` | string | Current screen state. |
| `G.stateData` | object | State-local UI data. |
| `G.settings` | object | Settings record. |
| `G.run` | object | Run record. |
| `G.level` | object | Current level record. |
| `G.player` | object | Player record. |
| `G.camera` | object | Camera record. |
| `G.enemies` | array | Enemy records. |
| `G.traps` | array | Trap records. |
| `G.physicsObjects` | array | Physics object records. |
| `G.collectibles` | array | Pickup records. |
| `G.switches` | array | Switch records. |
| `G.doors` | array | Door and key door records. |
| `G.hints` | array | Hint records. |
| `G.secrets` | array | Secret records. |
| `G.landmarks` | array | Landmark records. |
| `G.decorations` | array | Decoration records. |
| `G.creatures` | array | Collectible creature records. |
| `G.effects` | object | Effects record. |
| `G.score` | object | Score record. |
| `G.highScores` | array | High score records. |

Settings record:
| Field | Type | Meaning |
| --- | --- | --- |
| `settings.reducedMotion` | boolean | Reduced motion on/off. |
| `settings.volume` | number | 0-100. |
| `settings.keymap` | object | Action to key array. |

Run record:
| Field | Type | Meaning |
| --- | --- | --- |
| `run.currentLevelId` | number | 1-6. |
| `run.unlocked` | boolean[6] | Level unlock state. |
| `run.completed` | boolean[6] | Level completion state. |
| `run.medals` | object | levelId to “bronze”, “silver”, “gold”. |
| `run.totalMedals` | number | Computed total medals. |
| `run.rank` | string | Current rank. |
| `run.levelStartScore` | number | Score snapshot at level start. |
| `run.noDeath` | boolean[6] | No-death flag per level. |
| `run.keyHeld` | boolean | Key held in current level. |

Score record:
| Field | Type | Meaning |
| --- | --- | --- |
| `score.value` | number | Current total score. |
| `score.combo` | number | Current multiplier, 1-5. |
| `score.comboTimer` | number | Frames until combo resets. |

Player record:
| Field | Type | Meaning |
| --- | --- | --- |
| `player.x` | number | Left px. |
| `player.y` | number | Top px. |
| `player.w` | number | Hitbox width. |
| `player.h` | number | Hitbox height. |
| `player.vx` | number | Horizontal velocity. |
| `player.vy` | number | Vertical velocity. |
| `player.facing` | number | -1 left, 1 right. |
| `player.prevX` | number | Previous x. |
| `player.prevY` | number | Previous y. |
| `player.onGround` | boolean | Grounded. |
| `player.inWater` | boolean | In water. |
| `player.inClimb` | boolean | Climb state. |
| `player.airBouncesLeft` | number | 0 or 1. |
| `player.coyote` | number | Coyote frames. |
| `player.jumpBuffer` | number | Jump buffer frames. |
| `player.jumpCut` | boolean | Variable jump applied. |
| `player.ignoreOneWay` | number | One-way drop frames. |
| `player.dodging` | number | Dodge frames left. |
| `player.dodgeCd` | number | Dodge cooldown. |
| `player.dash` | number | Dash frames left. |
| `player.dashCd` | number | Dash cooldown. |
| `player.throwCd` | number | Throw cooldown. |
| `player.slapCd` | number | Slap cooldown. |
| `player.transform` | number | Transform frames left. |
| `player.transformCd` | number | Transform cooldown. |
| `player.shield` | boolean | Transform 1-hit shield. |
| `player.boost` | number | Boost frames left. |
| `player.creatureActive` | boolean | Guppy Buddy active. |
| `player.alive` | boolean | Alive. |
| `player.deathTimer` | number | Death animation frames. |
| `player.winTimer` | number | Win animation frames. |

Level record:
| Field | Type | Meaning |
| --- | --- | --- |
| `level.id` | number | 1-6. |
| `level.name` | string | Level name. |
| `level.seed` | number | RNG seed. |
| `level.tileW` | number | Tile width. |
| `level.tileH` | number | Tile height. |
| `level.tiles` | Uint8Array | Tile data. |
| `level.spawn` | object | Spawn point px. |
| `level.exit` | object | Exit Pad px. |
| `level.gemTotal` | number | Total gems. |
| `level.gemsCollected` | number | Collected gems. |
| `level.diedThisLevel` | boolean | Died during this level. |

Camera record:
| Field | Type | Meaning |
| --- | --- | --- |
| `camera.x` | number | Viewport left px. |
| `camera.y` | number | Viewport top px. |
| `camera.shakeX` | number | Shake offset x. |
| `camera.shakeY` | number | Shake offset y. |
| `camera.shakeFrames` | number | Shake frames left. |
| `camera.shakeIntensity` | number | Shake px. |

Effects record:
| Field | Type | Meaning |
| --- | --- | --- |
| `effects.particles` | array | Particle records. |
| `effects.floatTexts` | array | Float text records. |
| `effects.hitFlash` | number | Hit flash frames. |

High score record:
| Field | Type | Meaning |
| --- | --- | --- |
| `score` | number | Total score. |
| `levelId` | number | Final level reached. |
| `rank` | string | Rank at save time. |
| `date` | string | ISO date. |

## 2.3 Module specifics
| Module | Required functions |
| --- | --- |
| `main.js` | `boot()`, `startLoop()`, `update()`, `render()`, `changeState(state, data)`, `startLevel(id)`, `retryLevel()`, `nextLevel()`, `toTitle()`, `toLevelSelect()`, `toHighScores()`, `toSettings()`, `saveAll()`, `loadAll()` |
| `rng.js` | `createRng(seed)`, `rng.next()`, `rng.int(min, max)`, `rng.pick(array)` |
| `input.js` | `initInput()`, `setKeymap(action, key)`, `resetKeymap()`, `isDown(action)`, `pressed(action)`, `release(action)`, `clearPressed()` |
| `level.js` | `getLevel(id)`, `loadLevel(id)`, `resetLevel()`, `isUnlocked(id)`, `unlockLevel(id)`, `getMedal(id)`, `setMedal(id, medal)`, `computeMedal(levelId, gemsCollected, allGems, noDeath)`, `computeRank(totalMedals)`, `levelCount()` |
| `tilemap.js` | `tileAt(px, py)`, `tileId(tx, ty)`, `isSolid(tx, ty)`, `isOneWay(tx, ty)`, `isWater(tx, ty)`, `isDamage(tx, ty)`, `isBouncePad(tx, ty)`, `isExit(tx, ty)`, `isSwitch(tx, ty)`, `isDoor(tx, ty)`, `isKeyDoor(tx, ty)`, `isWobble(tx, ty)`, `isClimbable(tx, ty)`, `tilesInRect(rect)`, `canStandOnOneWay(entity)` |
| `physics.js` | `aabb(a, b)`, `moveEntity(e)`, `applyGravity(e, gravity, maxFall)`, `bounceEntity(e, vy)`, `killPlayer()`, `winLevel()`, `updateCamera()`, `hasLineOfSight(a, b)` |
| `player.js` | `updatePlayer()`, `tryJump()`, `tryAirBounce()`, `tryDodge()`, `tryDash()`, `tryThrow()`, `trySlap()`, `tryTransform()`, `startClimb()`, `stopClimb()`, `swimControl()`, `setOneWayDrop()`, `consumeShield()`, `consumeCreature()` |
| `enemies.js` | `updateEnemies()`, `addEnemy(type, x, y)`, `contactPlayer(enemy)`, `stunEnemy(enemy, frames)`, `killEnemy(enemy)`, `alertGuard(guard)`, `updateFlee(enemy)`, `enemyDropsScore(enemy)` |
| `traps.js` | `updateTraps()`, `addTrap(type, x, y)`, `triggerTrap(trap)`, `trapContact(trap)` |
| `physicsObjects.js` | `updatePhysicsObjects()`, `addPhysicsObject(type, x, y)`, `isSolidObject(obj)`, `breakObject(obj)`, `bounceObject(obj, vy)`, `pushObject(obj, direction)`, `pullObject(obj, direction)`, `objectContact(obj)` |
| `collectibles.js` | `updateCollectibles()`, `addCollectible(type, x, y)`, `collect(item)`, `giveKey()`, `startBoost()`, `spawnCreature()`, `updateCreature()`, `creatureAbsorb()` |
| `doors.js` | `updateDoors()`, `addSwitch(x, y, linkedDoor, sticky)`, `addDoor(x, y, linkedSwitches, keyRequired)`, `activateSwitch(sw)`, `openDoor(door)`, `closeDoor(door)`, `unlockKeyDoor(door)` |
| `score.js` | `addScore(base, x, y)`, `tickCombo()`, `resetScore()`, `addReward(type)`, `onComboEvent()`, `levelClearReward()`, `noDeathReward()`, `secretReward()`, `creatureReward(absorbed)` |
| `effects.js` | `addParticles(x, y, count, color)`, `addFloatText(text, x, y, color)`, `screenShake(intensity, frames)`, `hitFlash(frames)`, `updateEffects()`, `renderEffects()` |
| `audio.js` | `initAudio()`, `resumeAudio()`, `playSfx(name)`, `startMusic(levelId)`, `stopMusic()`, `setVolume(percent)`, `playJingle(name)` |
| `ui.js` | `showScreen(state)`, `renderScreen()`, `updateHud()`, `handleUiInput()`, `selectedOption(state)`, `moveSelection(direction)`, `confirmSelection()`, `cancelSelection()` |
| `save.js` | `saveRun()`, `loadRun()`, `saveHighScore(entry)`, `loadHighScores()`, `clearSave()` |
| `debug.js` | See #8 DEBUG API. |

# 3. VISUAL SPEC
Brib the Gummy Frog is a bright, gummy, low-resolution pixel platformer. The world looks like a sugary lagoon: lily pads, mushrooms, ponds, and oversized silly landmarks. Every sprite is 16x16 or larger built from a 16-colour saturated palette, with 1px dark outlines and hard-edged pixels. Animation is 2-4 frames, squash-and-stretch is small, and effects are readable from 3 pixels. The tone is cheerful, wobbly, and slightly ridiculous, like a frog made of jello bouncing through a cartoon swamp.

Lighting and atmosphere are flat. There is no dynamic lighting, no fog, and no realistic shadows. Depth comes from three parallax layers: far sky at 0.1, mid scenery at 0.3, gameplay layer at 1.0. The atmosphere is always sunny and saturated. Dithered 2px shades suggest height. Water has a slow 3-frame wave. Poison bubbles. Steam puffs. Electric pads zigzag.

Space is side-on and tiled. Solid ground is a bright sandy orange with dark outline. Lily pads are bright green one-way platforms. Bounce pads have white ripple marks. Water is blue with lighter wave pixels. Exit Pads are yellow doors with a wobble animation. Hazards are unmistakable: orange spikes, magenta poison, white/orange steam, cyan/white electric. Collectibles are yellow stars. The player is a small lilac-green frog with a cream belly, 12x14 px, and a clear silhouette in every state.

Palette:
| Role | Hex | Use |
| --- | --- | --- |
| Outline | #201A3A | 1px outlines, UI contrast. |
| Sky | #59D8FF | Background. |
| Sky Light | #A8F0FF | Clouds, far hills. |
| Ground | #FFB84D | Solid top. |
| Ground Shade | #E68A2E | Solid body, mushroom. |
| Lily | #35E87A | One-way pads, frog body. |
| Lily Shade | #1FB85C | Pad shadow, frog shade. |
| Frog | #7DFF3A | Brib body highlight. |
| Frog Belly | #FFF2A0 | Belly, key, some gems. |
| Danger | #FF8A00 | Spikes, switch, warning. |
| Poison | #D23BFF | Poison sludge. |
| Water | #2E7BFF | Water. |
| Water Light | #7BD7FF | Waves, Puddler body. |
| Enemy | #FF5577 | Slug, beetle, guard accent. |
| Gem | #FFD426 | Collectibles, exit accent. |
| UI | #FFFFFF | Text, highlights, electric. |

Recipe table:
| Element | Visual | Palette / animation | Gameplay rule |
| --- | --- | --- | --- |
| Sky background | Flat rectangle + 2 cloud layers | Sky, Sky Light; clouds move 1px every 30 frames unless reduced motion | No collision. |
| Solid tile | 16x16 block, top 3px Ground, rest GroundShade, 1px Outline | 1 frame | Solid. |
| One-way lily pad | 16x8 green pad with notch | Lily, Lily Shade, Outline; 2-frame idle | Collide from above only; Drop Through Down+Jump. |
| Bounce Pad | Lily pad with 2 white ripple pixels | Lily, UI; ripple 2 frames | Launch vy = -7.8. |
| Water | 16x16 blue tile | Water, Water Light; 3-frame wave | Swim, non-solid. |
| Poison Sludge | Magenta tile with 2 bubble pixels | Poison, UI; bubbles 2 frames | Environmental damage. |
| Steam Vent | Orange tile with white puff | Danger, UI; puff 3 frames | Periodic environmental damage. |
| Electric Pad | Cyan/white zigzag tile | UI, Water Light; 2-frame flicker | Periodic environmental damage. |
| Exit Pad | 16x16 yellow door with 2 white stars | Gem, UI; wobble 4 frames | Win objective. |
| Level Spawn | 16x16 green pad with 1 frog footprint | Lily, Outline; 1 frame | Player spawn. |
| Brib idle | 16x16 frog, 2 frames blink | Frog, Lily, Frog Belly, Outline | Default state. |
| Brib run | 2-frame leg cycle | 8 frames per frame | Run. |
| Brib jump/fall | 3-frame stretch | 1 frame each | Jump, fall. |
| Brib air bounce | 2-frame puff | Frog, UI | Air Bounce. |
| Brib dodge | 16x8 crouch | Frog, Outline | Dodge. |
| Brib swim | 2-frame kick | Frog, Water Light | Swim. |
| Brib climb | 2-frame reach | Frog, Outline | Climb. |
| Brib dash | 1-frame stretch + 2 trail pixels | Frog, UI | Dash. |
| Brib throw | 2-frame mouth open + pea | Frog, Gem | Throw. |
| Brib slap | 2-frame tongue/fist | Frog, UI | Slap. |
| Puff Toad | 18x12 inflated frog, 2 frames | Frog, Lily Shade, Outline | Transform. |
| Slug Snot | 14x10 slug, 2-frame crawl | Enemy, Water Light, Outline | Enemy. |
| Zippy Dragonfly | 12x10 wings, 2-frame flap | Enemy, UI, Outline | Enemy. |
| Puff Beetle | 12x12 beetle, 2-frame hop | Enemy, Ground Shade, Outline | Enemy. |
| Toad Guard | 14x14 toad with tiny spear | Enemy, Ground, Outline | Guard. |
| Puddler Flee | 10x8 blue blob, 2-frame wobble | Water Light, Outline | Flee. |
| Guppy Buddy | 8x6 fish, 2-frame tail | Gem, Water Light, Outline | Collectible creature. |
| Lily Gem | 8x8 yellow star | Gem, UI; 4-frame twinkle | Collectible. |
| Honey Shroom | 12x12 brown/orange mushroom | Ground, Danger, Outline; 2-frame wiggle | Boost. |
| Key | 8x8 yellow key | Gem, UI; 2-frame spin | Key. |
| Switch Pad | 16x8 orange lever | Danger, UI; 2-frame lever | Switch. |
| Door | 16x16 gate, 3-frame open | Ground, Ground Shade, Outline | Solid when closed. |
| Key Door | Door with keyhole | Ground, Gem, Outline | Locked until key. |
| Wobble Mushroom | 16x16 mushroom, 2-frame wobble | Ground, Ground Shade, Outline | Breakable solid. |
| Hint Stump | 16x16 stump with white ? | Ground, UI; ? pulses | Hint. |
| Secret area | Hidden mushroom house, 24x24 | Ground, Lily, Gem | Secret reward. |
| Landmark | 32x48 giant snail/mushroom clock | Multiple palette; 2-frame blink or tick | Inspect with hold Jump. |
| Decoration | Reeds, snails, clouds, snail shells | Multiple palette; 1-2 frames | Background only. |
| HUD score | 8x8 pixel text top-left | UI on dark 2px outline | Score only. |
| Particle | 2x2 or 4x4 square | Event colour | Effects. |
| Float text | 8x8 text rising 16px | UI or event colour | Score feedback. |
| Hit flash | Player/ enemy white 1-3 frames | UI | Damage feedback. |
| Screen shake | Camera offset | No colour | Effects. |

# 4. GAMEPLAY SPEC
Brib the Gummy Frog is a short silly side-on platformer where you play as Brib, a gummy frog who hops, bounces, swims, dodges, throws peas, and turns into a puffed toad to escape hazards. Each level is a single tilemap with a Level Spawn and an Exit Pad. The player’s win condition is always reaching the Exit Pad. Falling, traps, environmental damage, and enemy contact cause one-hit death, which restarts the level. Levels introduce mechanics in a fixed order: core bouncing first, survival hazards next, then switches, keys, score, and finally transform, creatures, combos, medals, and ranks. The game is 6 levels long, roughly 24 minutes on first clear.

## 4.1 Records with rosters
Level roster:
| Level | Name | Tiles | Target time | Gems | Enemies | Traps | Physics | Special focus |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | Lily Lawn | 40 x 22 | 2:00 | 2 | 0 | 0 | 0 | Jump, Air Bounce, Bounce Pad, Exit. |
| 2 | Soggy Slalom | 48 x 22 | 3:00 | 4 | 2 | 2 | 0 | Swim, falling, climb, one-way. |
| 3 | Springy Spikes | 56 x 22 | 4:00 | 5 | 4 | 4 | 2 | Traps, environmental damage, dodge. |
| 4 | Beetle Bounce | 64 x 24 | 4:00 | 6 | 6 | 6 | 4 | Enemies, physics objects, slap, throw intro. |
| 5 | Key Pond | 72 x 24 | 5:00 | 7 | 8 | 8 | 4 | Keys, doors, switches, puzzles, boost. |
| 6 | Grand Gig | 80 x 26 | 6:00 | 8 | 10 | 10 | 6 | All systems, medals, creatures, combos. |

Player record is defined in #2.2.

Enemy roster:
| Enemy | Tier | Size | Behaviour | Player interaction | Score |
| --- | ---: | --- | --- | --- | ---: |
| Slug Snot | 2 | 14 x 10 | Walks 0.3 px/f, reverses at walls/edges. | Contact kills unless stunned; Slap stuns; Throw kills. | 50 on Throw kill. |
| Zippy Dragonfly | 2 | 12 x 10 | Hover sine, 8 px amplitude, 120-frame period, patrol 64 px. | Contact kills unless stunned; Slap stuns; Throw kills. | 50 on Throw kill. |
| Puff Beetle | 2 | 12 x 12 | Hops every 90 frames, vy -3.5, vx 0.5. | Contact kills unless stunned; Slap stuns; Throw kills. | 50 on Throw kill. |
| Toad Guard | 4 | 14 x 14 | Patrols 0.4 px/f; if player within 48 px and line of sight, alerts and chases 1.4 px/f. | Contact kills; Throw stuns 90 frames. | 75 on stun escape? No: no score unless killed? Guards are not killed by Throw, only stunned. |
| Puddler Flee | 4 | 10 x 8 | If player within 40 px, flees 1.6 px/f away; reverses at walls. | Touch causes squeak and +75; no death. | 75. |

Trap roster:
| Trap | Tier | Trigger | Effect |
| --- | ---: | --- | --- |
| Spike Vine | 2 | Contact | Kill. |
| Drop Brick | 2 | Player within 24 px below or Geyser hit | Falls after 45 frames; contact while falling kills. |
| Geyser Jet | 2 | Cycle off 120, on 30 | Launch player vy -8.2; no damage. |

Environmental damage roster:
| Damage | Tier | Cycle | Effect |
| --- | ---: | --- | --- |
| Poison Sludge | 2 | Always | Kill unless shield/creature. |
| Steam Vent | 2 | Off 120, on 60 | Kill when active. |
| Electric Pad | 2 | Off 60, on 30 | Kill when active. |

Physics object roster:
| Object | Tier | Behaviour | Interactions |
| --- | ---: | --- | --- |
| Falling Lily Pad | 2 | 32x8 platform; after 120 frames stood on, falls, disappears after 240 frames. | Stand, avoid. |
| Mushroom Crate | 2 | 16x16 solid, mass 2; can be pushed/pulled in Tier 4. | Dodge break, Slap break, Throw break, Push/Pull. |
| Wobble Mushroom | 2 | 16x16 solid breakable; used for secrets and paths. | Dodge break, Slap break, Throw break. |

Pickup roster:
| Pickup | Tier | Effect |
| --- | ---: | --- |
| Lily Gem | 3 | +100 score, combo event. |
| Honey Shroom | 3 | Boost 480 frames. |
| Key | 3 | Opens one Key Door. |
| Guppy Buddy | 4 | Follows 1200 frames, absorbs one kill source. |

Switch/door roster:
| Object | Tier | Rule |
| --- | ---: | --- |
| Switch Pad | 3 | Activated by contact or pea; sticky or timed 180 frames. |
| Door | 3 | Solid when closed; opens 30 frames; linked switches/key. |
| Key Door | 3 | Solid until Key held; opens permanently. |

## 4.2 Systems
### Jump (Tier 1)
- Trigger: Jump pressed while `player.onGround` is true or `player.coyote > 0`.
- Set `player.vy = -5.6`, `player.onGround = false`, `player.airBouncesLeft = 1`, `player.jumpCut = false`.
- Coyote time: 6 frames after leaving ground.
- Jump buffer: 6 frames before landing.
- Variable jump: if Jump released while `player.vy < 0` and `!player.jumpCut`, set `player.vy *= 0.55`, `player.jumpCut = true`.
- Horizontal movement is unchanged.
- SFX: `jump`. Particles: 3.

### Objectives (Tier 1)
- The only Tier 1 objective is the Exit Pad.
- Exit Pad is a 16x16 trigger tile.
- If player AABB overlaps Exit Pad, call `winLevel()` after a 30-frame win animation.
- The objective is visible in the world; no HUD text is used because HUD is score only.
- Player uses Move input to approach.

### Falling (Tier 1)
- If `player.y > G.level.tileH * 16 + 32`, call `killPlayer()`.
- Water does not prevent falling death if the player exits the level bounds.
- Death sets `player.alive = false`, `player.deathTimer = 45`, plays `death`, then shows game over.
- Retry resets the level and respawns at Level Spawn.

### Map / World (Tier 1)
- Map is a tile grid, 16 px tiles.
- Solid tiles stop player and objects.
- One-way lily pads support the player only if previous bottom <= tile top and `player.vy >= 0`.
- Drop Through: while standing on one-way, Down + Jump sets `player.ignoreOneWay = 10`.
- Bounce Pad tiles are non-solid triggers.
- Exit Pad and Level Spawn are required tiles.
- Camera follows player with deadzone 120 x 80, lerp 0.18, clamped to level.
- Reduced motion disables camera lerp and parallax movement; camera snaps.

### Bounce (Tier 1)
- Air Bounce: if `!player.onGround`, `!player.inWater`, `player.airBouncesLeft == 1`, and Jump pressed, set `player.vy = -6.4`, `player.airBouncesLeft = 0`.
- Bounce Pad: if player overlaps Bounce Pad, set `player.vy = -7.8`, `player.airBouncesLeft = 1`.
- Reset `player.airBouncesLeft = 1` on ground, Bounce Pad, or exiting water with `player.vy < -2.0`.
- Air Bounce can be used once per airborne arc.
- SFX: `bounce`. Particles: 5. Screen shake: 1 px for 3 frames unless reduced motion.

### Traps (Tier 2)
- Spike Vine: 16x16 hazard. Contact kills.
- Drop Brick: 16x16 physics object. Trigger if player within 24 px below or Geyser hit. After 45 frames, shake, then fall with gravity. Contact while falling kills.
- Geyser Jet: 16x16 jet. Cycle: off 120 frames, on 30 frames. When on and player overlaps, set `player.vy = -8.2`. No damage.
- All traps use Move/Jump to trigger or avoid.
- SFX: `trap`.

### Environmental Damage (Tier 2)
- Poison Sludge: always active tile. Contact kills unless consumed by shield or Guppy Buddy.
- Steam Vent: cycle off 120, on 60. Contact while on kills.
- Electric Pad: cycle off 60, on 30. Contact while on kills.
- Damage contact resolution:
  1. If `player.shield` is true, consume shield, `player.transform = 0`, `player.hitFlash = 3`, no death.
  2. Else if `player.creatureActive` is true, Guppy Buddy disappears, `addScore(150)`, no death.
  3. Else `killPlayer()`.

### Physics Objects (Tier 2)
- Falling Lily Pad: 32x8 platform. While player stands, `fallTimer = 120`. After timer, non-solid, falls with gravity, disappears after 240 frames.
- Mushroom Crate: 16x16 solid. Can be broken by Dodge contact, Slap, or Throw. Mass 2, restitution 0.25.
- Wobble Mushroom: 16x16 solid breakable. Can be broken by Dodge, Slap, or Throw.
- Objects collide with solid tiles and player. They do not collide with each other in Tier 2.
- Player can stand on solid objects.
- Breaking creates particles and SFX `break`.

### Swim (Tier 2)
- If player centre is in a water tile, `player.inWater = true`.
- In water: gravity 0.08, max fall 1.5, move speed 1.2.
- Hold Jump: set `player.vy = -1.2`.
- Release Jump: no upward force.
- Hold Down: add 0.1 to `player.vy`, clamp to max fall.
- Air Bounce is disabled while in water.
- Exiting water: if `player.vy < -2.0`, set `player.airBouncesLeft = 1`.
- SFX: `splash` on entry, `swim_kick` every 20 frames while kicking.

### Enemies (Tier 2)
- Enemy contact kills player unless enemy is stunned or shield/creature consumes it.
- Slug Snot: `vx = 0.3 * facing`; reverses on wall or cliff.
- Zippy Dragonfly: `y = baseY + sin(G.frame / 120 * 2π) * 8`; patrols horizontally 64 px at 0.5 px/f.
- Puff Beetle: every 90 frames if grounded, `vy = -3.5`, `vx = 0.5 * facing`.
- Stunned enemy: `state = stunned`, `timer = 60`, no movement, no contact kill.
- Tier 2 has no enemy kill except later Throw; Slap only stuns.
- SFX: `enemy_die` only when kill exists in Tier 3.

### Difficulty Ramp (Tier 2)
- Levels use the roster in #4.1.
- No two kill sources are closer than 32 px horizontally.
- Enemy spawns are at least 64 px from Level Spawn.
- Traps are at least 48 px apart.
- Water depth for swim sections is at least 32 px.
- Level 1 has no kill sources other than falling.
- Level 2 introduces water and 2 enemies.
- Level 3 introduces traps and environmental damage.
- Level 4 introduces physics objects and 6 enemies.
- Level 5 introduces doors/switches and 8 enemies.
- Level 6 uses all systems and 10 enemies.

### Abilities / Special Moves (Tier 2)
- Slap: input Slap.
- If `player.slapCd == 0`, create a 20x12 hitbox in front of player for 4 frames.
- Effects: stun enemies 60 frames, break Mushroom Crate or Wobble Mushroom.
- Set `player.slapCd = 45`.
- Slap does not kill enemies in Tier 2.
- SFX: `slap`.

### Dodge (Tier 2)
- Input Down.
- If `player.dodgeCd == 0` and `!player.inClimb`:
  - `player.dodging = 12`
  - `player.dodgeCd = 27`
  - hitbox height becomes 8
  - `player.vx` speed clamps to 1.0
  - if airborne, `player.vy = 0` for first 3 frames, then gravity resumes.
- Dodge avoids low traps and damage zones that are 8 px or less tall.
- If touching Wobble Mushroom while dodging, break it.
- SFX: `dodge`.

### Spawn Points (Tier 2)
- Each level has one Level Spawn tile, 16x16.
- `loadLevel` places player at Level Spawn.
- Death resets all level state to initial and respawns at Level Spawn.
- `run.levelStartScore` is restored on death.
- Debug can teleport, but retry always uses Level Spawn.

### Climb (Tier 2)
- Climbable vine tile is non-solid.
- If player overlaps climbable tile and Jump is pressed, `player.inClimb = true`.
- While climbing:
  - `player.vy = 0`
  - Hold Jump: climb speed 1.0 px/f.
  - Horizontal input moves 0.5 px/f.
- Press Jump while climbing: leave with `vy = -5.0`.
- Cannot climb while dodging, dashing, transformed, or in water.
- SFX: `climb` every 30 frames.

### Unlocks (Tier 2)
- `run.unlocked[0] = true` initially.
- `winLevel(id)` sets `run.completed[id] = true`.
- If `id < 6`, set `run.unlocked[id] = true` for next level.
- Level select only allows `run.unlocked[levelId] == true`.
- Final level completion does not unlock anything else.
- Unlocks persist in local save.

### Landmarks (Tier 3)
- Landmarks are 32x48 background objects, parallax 0.5.
- No collision.
- Hold Jump within 16 px for 30 frames to inspect.
- Inspect shows name float text for 120 frames and plays `hint` at low volume.
- No score.
- Landmark types: Giant Snail, Mushroom Clock, Lily Tower.

### Dash (Tier 3)
- Input Dash.
- If `player.dashCd == 0`:
  - `player.dash = 8`
  - `player.dashCd = 38`
  - `player.vy = 0`
  - `player.vx = 4.2 * player.facing`
  - gravity disabled for 8 frames.
- Dash can cancel fall and clear gaps up to 2 tiles.
- Dash does not pass through solid tiles.
- SFX: `dash`.

### Rewards (Tier 3)
- Level clear reward: +500.
- No-death clear reward: +250 if `run.noDeath[levelId]` is true.
- Secret reward: +250.
- Boost expiry does not give score.
- Rewards use `addScore()` and float text.
- Tier 4 adds creature rewards to this system.

### Decoration (Tier 3)
- Decoration is non-interactive background props: reeds, clouds, snails, shells.
- Parallax 0.25 or 0.5.
- No collision, no score, no interaction.
- Move input changes camera viewpoint, which changes visible decoration.
- Animation is 1-2 frames; reduced motion freezes animation.

### Switches and Doors (Tier 3)
- Switch Pad: 16x8.
- Activated by player contact or Throw pea hit.
- Sticky switches stay on; timed switches open linked door for 180 frames then close.
- Door: 16x16.
- Closed door is solid.
- Door opens 30 frames when all linked switches are on, or if key requirement satisfied.
- If any linked switch turns off, timed door closes after 30 frames.
- SFX: `switch`, `door`.

### Puzzle Types (Tier 3)
- Key-Door Puzzle: collect Key, touch Key Door, door opens permanently.
- Switch Chain: three sticky switches linked to one exit gate; all three on opens gate permanently.
- Bounce Route: a high switch is reachable only by Bounce Pad or Air Bounce; hitting it opens a gate.
- Level 5 has 2 puzzles; Level 6 has 2 puzzles.
- Puzzles use only existing inputs: Move, Jump, Throw, Down.

### Secrets (Tier 3)
- Secret is a hidden area at least 24x24 px.
- Secret is hidden behind Wobble Mushroom or under a one-way lily pad.
- Reveal by breaking Wobble Mushroom or Drop Through.
- On first reveal: +250 score, spawn 1 Honey Shroom, mark secret revealed.
- Level 3-6 each have 1 secret.
- SFX: `secret`.

### Hints (Tier 3)
- Hint Stump is 16x16.
- Hold Jump within 12 px for 60 frames to show hint text for 180 frames.
- Hint text is level-specific:
  - Level 2: “Water slows your hop.”
  - Level 3: “Crouch under spikes.”
  - Level 4: “Slap the beetles.”
  - Level 5: “Keys open the big doors.”
  - Level 6: “Puff Toad takes one hit.”
- Hints do not change gameplay.
- SFX: `hint`.

### Boosts (Tier 3)
- Honey Shroom pickup: 12x12.
- On touch: `player.boost = 480`.
- Boost effects:
  - move speed x1.5
  - jump velocity -6.2
  - Air Bounce velocity -7.0
- Boost does not stack; touching another Honey Shroom refreshes timer.
- SFX: `boost`.

### Collectibles (Tier 3)
- Lily Gem: 8x8.
- On touch: +100 score, `level.gemsCollected++`, combo event, SFX `collect`.
- Gem counts per level:
  - Level 1: 2
  - Level 2: 4
  - Level 3: 5
  - Level 4: 6
  - Level 5: 7
  - Level 6: 8
- Gems are not required to reach Exit, but medals use them in Tier 4.

### Throw (Tier 3)
- Input Throw.
- If `player.throwCd == 0`:
  - `player.throwCd = 30`
  - spawn pea 4x4 at player mouth.
  - pea `vx = 6 * player.facing`, `vy = -0.5`, gravity 0.1, lifetime 60.
- Pea effects:
  - breaks Wobble Mushroom
  - stuns enemies 60 frames
  - kills Slug Snot, Zippy Dragonfly, Puff Beetle: +50 score
  - stuns Toad Guard 90 frames
  - causes Puddler Flee to drop +75
  - activates Switch Pad
- SFX: `throw`, `pea_hit`.

### Score (Tier 3)
- `score.value` is the only HUD element.
- Score sources:
  - Lily Gem: 100
  - Basic enemy kill: 50
  - Puddler Flee drop: 75
  - Secret: 250
  - Level clear: 500
  - No-death clear: 250
- Tier 4 adds: Guppy absorb 150, Guppy expire 50.
- `addScore(base)` uses current combo multiplier.
- Float text shows final score.
- High score is saved on win if score qualifies for top 10.

### Guards (Tier 4)
- Toad Guard: 14x14.
- Patrol state: `vx = 0.4 * facing`, range 64 px.
- Alert state: if player within 48 px and `hasLineOfSight` and vertical difference <= 16 px, set `vx = 1.4 * sign(player.x - guard.x)`.
- Contact kills.
- Throw pea stuns guard 90 frames.
- Stunned guard: no movement, no contact kill.
- SFX: `alert`, `stun`.

### Flee (Tier 4)
- Puddler Flee: 10x8.
- If player within 40 px, set `state = flee`, `vx = 1.6 * sign(enemy.x - player.x)`.
- Reverses at walls.
- If player touches Puddler:
  - Puddler disappears
  - +75 score
  - SFX `flee_squeak`
  - no death
- Throw pea on Puddler also triggers drop.

### Keys and Locked Doors (Tier 3)
- Key pickup: 8x8.
- On touch: `run.keyHeld = true`, SFX `key`.
- Key Door: 16x16 solid.
- If player overlaps Key Door and `run.keyHeld == true`, open permanently, `run.keyHeld = false`.
- Key is level-specific; it does not persist across levels.
- SFX: `door`.

### Push and Pull (Tier 4)
- Applies to Mushroom Crate and Wobble Mushroom when not broken.
- Push: if player adjacent within 4 px and holds Move toward object, set object `vx = 0.8 * direction`.
- Pull: if `Pull` held and player adjacent within 4 px, set object `vx = 0.6 * direction` toward player.
- Transform increases push/pull speed by 2x.
- Object max speed 1.0 unless transformed.
- Objects obey gravity and solid tiles.
- Objects cannot be pushed through doors or solid tiles.
- SFX: `push` every 20 frames while moving.

### Transform (Tier 4)
- Input Transform.
- If `player.transformCd == 0`:
  - `player.transform = 180`
  - `player.transformCd = 540`
  - `player.w = 18`, `player.h = 12`
  - `player.shield = true`
  - move speed 1.2
  - jump velocity -5.0
  - Air Bounce disabled
  - push/pull strength 2x
- On expire:
  - revert hitbox
  - `player.shield = false`
  - particles
- If shield is true and damage contact occurs:
  - consume shield
  - `player.transform = 0`
  - `player.hitFlash = 3`
  - no death
- SFX: `transform`.

### Collectible Creatures (Tier 4)
- Guppy Buddy pickup: 8x6.
- On touch:
  - `player.creatureActive = true`
  - creature `timer = 1200`
  - max 1 active
  - SFX `creature`
- Guppy follows player with lerp 0.2, stays 8 px above player.
- On timer expire:
  - disappears
  - +50 score
- On absorbing one environmental damage or enemy contact:
  - disappears
  - +150 score
  - player safe
- Guppy does not stack.
- SFX: `absorb`.

### Combos (Tier 4)
- Combo events: collect Lily Gem, kill basic enemy, Puddler drop, bounce pad, secret reveal.
- On combo event:
  - if `score.comboTimer > 0`, `score.combo = min(5, score.combo + 1)`
  - else `score.combo = 1`
  - `score.comboTimer = 90`
- If `score.comboTimer` expires, `score.combo = 1`.
- Death resets `score.combo = 1`, `score.comboTimer = 0`.
- `addScore(base)` uses `base * score.combo`.
- Float text includes multiplier when > 1.

### Medals / Ranks (Tier 4)
- After `winLevel(id)`:
  - `gemsCollected = G.level.gemsCollected`
  - `allGems = G.level.gemsCollected >= G.level.gemTotal`
  - `noDeath = !G.run.diedThisLevel[levelId]`
  - Bronze: always.
  - Silver: `gemsCollected >= ceil(G.level.gemTotal / 2)`.
  - Gold: `allGems && noDeath`.
- Store best medal per level in `run.medals`.
- Total medals:
  - 0-2: Puddle Rookie
  - 3-5: Lily Lancer
  - 6: Giggle Grandmaster
- Medals and rank appear on win screen and level select.

## 4.3 Progression and difficulty
| Level | Systems introduced | Difficulty change |
| --- | --- | --- |
| 1 Lily Lawn | Jump, Bounce, One-way, Exit | No enemies, no traps. |
| 2 Soggy Slalom | Swim, Climb, 2 enemies, 2 traps | Water sections and pits. |
| 3 Springy Spikes | Environmental damage, Dodge, Slap, 1 secret | Hazard timing. |
| 4 Beetle Bounce | Physics objects, 6 enemies, 1 flee, 1 secret | Enemy density. |
| 5 Key Pond | Keys, doors, switches, puzzles, boost, 1 guard | Multi-part objectives. |
| 6 Grand Gig | Transform, Guppy, combos, medals, full density | All systems together. |

## 4.4 Feel
- Input response is immediate. Movement uses 0.35 acceleration and 0.7 friction.
- Jump is 5.6 upward. Air Bounce is 6.4. Bounce Pad is 7.8.
- Animations are 2-4 frames. Squash on land is 2 frames.
- Screen shake is small: death 2 px for 6 frames, bounce 1 px for 3 frames, hit 1 px for 4 frames.
- Hit flash is 3 frames normally, 1 frame with reduced motion.
- Particles:
  - jump: 3
  - land: 4
  - bounce: 5
  - death: 8
  - collect: 4
  - break: 6
- Reduced motion:
  - screen shake off
  - parallax animation off
  - particles reduced by 75%
  - hit flash 1 frame
- Audio is short and punchy. No reverb, no long tails.

# 5. CHARACTERS
| Character | Silhouette | Animations by name | Motion rules | Facing | States |
| --- | --- | --- | --- | --- | --- |
| Brib | 12x14 lilac-green frog, cream belly, 1px dark outline. | Idle: 2 frames, blink every 120 frames. Run: 2 frames, 8 frames per frame. Jump: 1 frame stretched. Fall: 1 frame relaxed. Air Bounce: 2 frames puff. Bounce Pad: 2 frames big puff. Dodge: 1 frame crouch 12 frames. Swim: 2 frames kick, 12 frames per frame. Climb: 2 frames reach, 10 frames per frame. Dash: 1 frame stretch + trail. Throw: 2 frames mouth, 10 frames. Slap: 2 frames tongue, 6 frames. Transform: 2 frames puff, 12 frames. Die: 3 frames spin, 45 frames. Win: 3 frames hop, 45 frames. | Run follows input. Jump sets vy. Air Bounce sets vy. Dodge crouches. Swim controls vertical. Climb moves vertically. Dash overrides vx for 8 frames. Transform changes hitbox and shield. | Flip sprite for left/right. Facing persists after jump unless input changes. | idle, run, jump, fall, airBounce, bouncePad, dodge, swim, climb, dash, throw, slap, transform, die, win. |
| Puff Toad | 18x12 inflated frog, rounder body, 2 frames. | Idle: 2 frames breathe. Run: 2 frames waddle. Die: 3 frames pop. | Run speed 1.2. Jump -5.0. No Air Bounce. 1-hit shield. Push strength 2x. | Flip sprite for left/right. | idle, run, shieldHit, pop. |
| Slug Snot | 14x10 pink slug, one big eye, 2-frame crawl. | Walk: 2 frames, 12 frames per frame. Stun: 1 frame star eye. Dead: 1 frame splat. | vx 0.3. Reverses at walls/cliffs. Stun 60. | Flip by facing. | walk, stun, dead. |
| Zippy Dragonfly | 12x10 blue/pink wings, 2-frame flap. | Hover: 2 frames, 4 frames per frame. Stun: 1 frame. Dead: 1 frame. | Sine hover amplitude 8, period 120. Patrol 64 px at 0.5. | Flip by facing. | hover, stun, dead. |
| Puff Beetle | 12x12 round beetle, 2-frame hop. | Hop: 2 frames. Stun: 1 frame. Dead: 1 frame. | Every 90 frames, vy -3.5, vx 0.5. | Flip by facing. | hop, stun, dead. |
| Toad Guard | 14x14 grey-pink toad with tiny spear, 2-frame patrol. | Patrol: 2 frames. Alert: 2 frames fast. Stun: 1 frame. | Patrol 0.4. Alert 1.4 if line of sight and 48 px. Throw stun 90. | Flip by facing. | patrol, alert, stun. |
| Puddler Flee | 10x8 water-light blob, 2-frame wobble. | Flee: 2 frames, 6 frames per frame. Squeak: 1 frame. | Flee 1.6 away from player. Touch drops +75. | Flip by facing. | idle, flee, squeak. |
| Guppy Buddy | 8x6 yellow fish, 2-frame tail. | Follow: 2 frames. Absorb: 1 frame burst. Expire: 1 frame fade. | Follow lerp 0.2. 1200 frames. Absorbs one kill source. | Flip by movement. | follow, absorb, expire. |
| Hint Toad | 16x16 small toad on stump, 2-frame pulse. | Hint: 2 frames, ? pulses every 60 frames. | Hold Jump 60 frames to show text 180 frames. | Static facing. | idle, hint. |

# 6. AUDIO
| Sound | Recipe | When it plays |
| --- | --- | --- |
| Music: Gummy Lagoon | Loop 140 BPM. Square lead C5 E5 G5 C6 G5 E5 G5 C5, 8th notes. Triangle bass C3 G3, quarter notes. Noise hat 16th notes, lowpass 6000 Hz. Volume 0.4. Level 5-6 add octave lead. | During game state. |
| `jump` | Square 400 Hz to 700 Hz over 60 ms, gain 0.25. | Jump. |
| `bounce` | Triangle 200 Hz to 900 Hz over 80 ms + square blip 1200 Hz 20 ms. | Air Bounce or Bounce Pad. |
| `land` | Noise 30 ms, lowpass 800 Hz, gain 0.15. | Landing. |
| `dash` | Sawtooth 800 Hz to 200 Hz over 80 ms, gain 0.2. | Dash. |
| `dodge` | Square 300 Hz to 150 Hz over 60 ms. | Dodge. |
| `throw` | Square 600 Hz to 1000 Hz over 40 ms. | Throw. |
| `pea_hit` | Triangle 200 Hz 30 ms. | Pea hits object/enemy. |
| `slap` | Square 1000 Hz to 300 Hz over 40 ms. | Slap. |
| `transform` | Two square notes: 500 Hz 50 ms, 700 Hz 50 ms. | Transform. |
| `splash` | Noise 100 ms, bandpass 1200 Hz. | Enter water. |
| `swim_kick` | Noise 20 ms, bandpass 800 Hz. | Swim kick. |
| `climb` | Square 500 Hz 20 ms, repeat every 30 frames while climbing. | Climb. |
| `enemy_die` | Square 800 Hz to 200 Hz over 120 ms. | Enemy killed by Throw. |
| `stun` | Square 1200 Hz 30 ms + 800 Hz 30 ms. | Enemy stunned. |
| `death` | Square 400 Hz to 100 Hz over 300 ms + noise 100 ms. | Player dies. |
| `collect` | Square 880 Hz 40 ms + 1320 Hz 40 ms. | Collectible. |
| `key` | Square 1046 Hz 60 ms + 1568 Hz 60 ms. | Key pickup. |
| `door` | Noise 100 ms + square 200 Hz 80 ms. | Door opens. |
| `switch` | Square 660 Hz 40 ms. | Switch activated. |
| `boost` | Triangle arpeggio 440, 660, 880 Hz, 90 ms total. | Boost pickup. |
| `secret` | Chord square 523, 659, 784 Hz, 150 ms. | Secret revealed. |
| `hint` | Sine 880 Hz 100 ms, quiet. | Hint shown or landmark inspected. |
| `trap` | Square 200 Hz to 500 Hz over 50 ms. | Trap triggers. |
| `break` | Noise 40 ms + square 300 Hz 30 ms. | Object breaks. |
| `push` | Square 250 Hz 20 ms. | Push/pull object. |
| `alert` | Square 900 Hz 40 ms + 1100 Hz 40 ms. | Guard alerts. |
| `flee_squeak` | Square 1500 Hz to 2200 Hz over 40 ms. | Puddler drop. |
| `absorb` | Triangle 600 Hz to 1000 Hz over 80 ms. | Guppy absorbs damage. |
| `ui_move` | Square 600 Hz 20 ms. | UI navigation. |
| `ui_select` | Square 880 Hz 40 ms. | UI confirm. |
| `ui_cancel` | Square 400 Hz 60 ms. | UI cancel. |
| `win_jingle` | Square melody 523, 659, 784, 1046 Hz, 300 ms total. | Win screen. |
| `gameover_jingle` | Square melody 300, 250, 200, 150 Hz, 400 ms total. | Game over screen. |

# 7. UX
UI is HTML and CSS only. The canvas shows the game. DOM overlays show screens and HUD. All text uses the pixel font. Screens are fixed 640 x 360 scaled with the canvas. CSS classes:
- `.screen`: full-screen overlay, pixel font, centered.
- `.hidden`: `display: none`.
- `.hud`: top-left score.
- `.title`: large title, subtitle, menu.
- `.menu`: vertical list.
- `.option`: one menu line.
- `.selected`: white background or inverse colour.
- `.pixel-font`: `font-family: 'PixelFrog8', 'Press Start 2P', monospace;`.
- `.canvas-wrap`: integer scaled canvas and overlays.
- `.reduced-motion`: disables CSS animations.

State machine:
| State | Enter action | Inputs | Next state |
| --- | --- | --- | --- |
| `boot` | Load save, initialize canvas/audio | None | `title` |
| `title` | Show title and options: Play, High Scores | Up/Down select, Enter/Space confirm | `level_select` or `high_scores` |
| `level_select` | Show 6 level buttons, unlocked only | Left/Right select, Enter/Space confirm, Escape cancel | `game`, `title`, `high_scores` |
| `game` | Load level, start music, update player | Gameplay inputs, Pause | `pause`, `game_over`, `win` |
| `pause` | Pause update, show options: Resume, Settings, Level Select, Quit | Up/Down, Enter/Space, Escape | `game`, `settings`, `level_select`, `title` |
| `settings` | Show reduced motion, key remap, volume | Enter/Space change, Escape cancel | `pause` or `title` |
| `game_over` | Show score and level name | Enter/Space retry, Escape level select | `game`, `level_select` |
| `win` | Show score, medal, rank; options: Next, Level Select, High Scores, Quit | Enter/Space next if exists, Escape level select | `game`, `level_select`, `high_scores`, `title` |
| `high_scores` | Show top 10 | Escape/Enter back | previous screen stored in `G.stateData.returnTo` |

HUD table:
| Element | Record field | When visible |
| --- | --- | --- |
| Score | `G.score.value` | `state == "game"` or `state == "pause"` |

# 8. DEBUG API
| Function | System | Effect |
| --- | --- | --- |
| `debugSetScore(value)` | Score | Set `G.score.value`. |
| `debugAddScore(base)` | Score | Call `addScore(base)`. |
| `debugSetLevel(id)` | Level | Load level. |
| `debugResetLevel()` | Level | Reset current level. |
| `debugTeleportPlayer(x, y)` | Player | Move player. |
| `debugSetPlayerState(fields)` | Player | Override player fields. |
| `debugSetAirBounces(n)` | Bounce | Set `player.airBouncesLeft`. |
| `debugKillPlayer()` | Falling | Kill player. |
| `debugWinLevel()` | Objectives | Trigger win. |
| `debugSpawnEnemy(type, x, y)` | Enemies | Add enemy. |
| `debugSetEnemyState(id, state)` | Enemies | Set enemy state. |
| `debugStunEnemy(id, frames)` | Enemies | Stun enemy. |
| `debugKillEnemy(id)` | Enemies | Remove enemy. |
| `debugSpawnTrap(type, x, y)` | Traps | Add trap. |
| `debugSetTrapState(id, state, timer)` | Traps | Set trap state/timer. |
| `debugTriggerTrap(id)` | Traps | Trigger trap. |
| `debugSpawnPhysics(type, x, y)` | Physics Objects | Add object. |
| `debugSetPhysics(id, fields)` | Physics Objects | Override object fields. |
| `debugBreakPhysics(id)` | Physics Objects | Break object. |
| `debugSetWater(x, y, w, h)` | Swim | Replace tiles with water. |
| `debugSetDamage(x, y, type, w, h)` | Environmental Damage | Replace tiles with damage. |
| `debugSpawnCollectible(type, x, y)` | Collectibles | Add pickup. |
| `debugCollectCollectible(id)` | Collectibles | Mark collected. |
| `debugStartBoost(frames)` | Boosts | Set `player.boost`. |
| `debugGiveKey()` | Keys | Set `run.keyHeld = true`. |
| `debugUnlockKeyDoor(id)` | Keys and Locked Doors | Open door. |
| `debugSpawnSwitch(x, y, linkedDoor, sticky)` | Switches and Doors | Add switch. |
| `debugActivateSwitch(id)` | Switches and Doors | Turn switch on. |
| `debugSetDoor(id, open)` | Switches and Doors | Set door open/closed. |
| `debugSpawnHint(x, y, text)` | Hints | Add hint. |
| `debugShowHint(id)` | Hints | Show hint text. |
| `debugSpawnSecret(x, y)` | Secrets | Add secret. |
| `debugRevealSecret(id)` | Secrets | Reveal secret. |
| `debugSpawnLandmark(type, x, y)` | Landmarks | Add landmark. |
| `debugInspectLandmark(id)` | Landmarks | Show landmark name. |
| `debugSpawnDecoration(type, x, y)` | Decoration | Add decoration. |
| `debugAddReward(type)` | Rewards | Add reward score. |
| `debugStartCombo(multiplier, timer)` | Combos | Set combo. |
| `debugAwardMedal(levelId, medal)` | Medals / Ranks | Set medal. |
| `debugSetRank(rank)` | Medals / Ranks | Set rank. |
| `debugSetUnlocked(levelId, unlocked)` | Unlocks | Set unlock. |
| `debugTransform(on, frames)` | Transform | Set transform. |
| `debugSpawnCreature(x, y)` | Collectible Creatures | Spawn Guppy. |
| `debugSetCreature(active, timer)` | Collectible Creatures | Set creature state. |
| `debugSetReducedMotion(on)` | Accessibility | Toggle reduced motion. |
| `debugSetVolume(percent)` | Audio | Set volume. |
| `debugPressInput(action)` | Input | Press action. |
| `debugReleaseInput(action)` | Input | Release action. |
| `debugLeftDown(on)` | Input | Left input. |
| `debugRightDown(on)` | Input | Right input. |
| `debugJumpDown(on)` | Input | Jump input. |
| `debugDownDown(on)` | Input | Down input. |
| `debugThrowDown(on)` | Input | Throw input. |
| `debugSlapDown(on)` | Input | Slap input. |
| `debugDashDown(on)` | Input | Dash input. |
| `debugTransformDown(on)` | Input | Transform input. |
| `debugPullDown(on)` | Input | Pull input. |

# 9. TESTS
| Tier | Test | Pass condition |
| --- | --- | --- |
| 1 | Fixed step | 1000 simulated frames produce 1000 `G.frame` increments at 60 Hz logic. |
| 1 | Collision | Player stops at solid tile and can stand on it. |
| 1 | Jump | Pressing Jump sets `vy = -5.6` and player rises 34 px vertically. |
| 1 | Coyote | Jump works 6 frames after leaving ledge. |
| 1 | Jump buffer | Jump registered if pressed 6 frames before landing. |
| 1 | Air Bounce | In air, Jump sets `vy = -6.4` once; second air Jump does nothing. |
| 1 | Bounce Pad | Overlap sets `vy = -7.8` and resets Air Bounce. |
| 1 | One-way drop | Down+Jump on one-way pad passes through for 10 frames. |
| 1 | Falling | `player.y > level.height*16+32` triggers death and level reset. |
| 1 | Exit win | Overlap Exit Pad triggers win state. |
| 1 | HUD | Score element shows `G.score.value` in game and pause. |
| 1 | Reduced motion | Screen shake frames remain 0 when enabled. |
| 1 | Remap | Changing left key to J makes J move left. |
| 2 | Poison kill | Standing in Poison Sludge kills unless shield/creature. |
| 2 | Steam cycle | Steam kills only during active 60-frame window. |
| 2 | Electric cycle | Electric kills only during active 30-frame window. |
| 2 | Spike trap | Spike Vine contact kills. |
| 2 | Drop brick | Trigger waits 45 frames, then falls and kills on contact. |
| 2 | Geyser | Geyser launches `vy = -8.2` during active window. |
| 2 | Falling Lily Pad | Pad holds 120 frames, then falls. |
| 2 | Swim | In water, hold Jump moves upward at -1.2 px/f. |
| 2 | Exit water bounce | Leaving water with `vy < -2.0` gives one Air Bounce. |
| 2 | Enemy contact | Slug contact kills player. |
| 2 | Slap stun | Slap hitbox stuns enemy for 60 frames. |
| 2 | Dodge crouch | Dodge sets hitbox height 8 for 12 frames. |
| 2 | Climb | Holding Jump on vine moves player upward at 1.0 px/f. |
| 2 | Spawn reset | After death, player is at Level Spawn and level state is initial. |
| 2 | Unlock | Completing level 1 unlocks level 2. |
| 3 | Dash | Dash sets vx 4.2 for 8 frames and cooldown 38. |
| 3 | Throw | Throw spawns pea with vx 6 and cooldown 30. |
| 3 | Pea kill | Pea kills Slug Snot and adds 50 score. |
| 3 | Switch door | Contact or pea opens linked door. |
| 3 | Key door | Key pickup then Key Door contact opens door. |
| 3 | Switch chain | All 3 sticky switches on opens exit gate permanently. |
| 3 | Bounce puzzle | Bounce Pad hit can activate high switch. |
| 3 | Secret | Breaking Wobble reveals secret, +250 and Honey Shroom. |
| 3 | Hint | Hold Jump 60 frames near stump shows text 180 frames. |
| 3 | Boost | Honey Shroom sets move speed x1.5 and jump -6.2. |
| 3 | Collectibles | Gems add 100 and increment `level.gemsCollected`. |
| 3 | Score persistence | Death restores `run.levelStartScore`. |
| 4 | Guard alert | Guard within 48 px with line of sight chases at 1.4 px/f. |
| 4 | Guard stun | Throw stuns guard 90 frames. |
| 4 | Flee | Puddler moves away 1.6 px/f when player near. |
| 4 | Puddler drop | Touch Puddler gives +75 and no death. |
| 4 | Push | Holding Move toward crate moves crate 0.8 px/f. |
| 4 | Pull | Holding Pull moves crate toward player 0.6 px/f. |
| 4 | Transform shield | Puff Toad takes one damage contact without death. |
| 4 | Guppy absorb | Active Guppy absorbs one environmental damage and gives +150. |
| 4 | Combo | Two combo events within 90 frames makes multiplier 2. |
| 4 | Medal gold | Clear with all gems and no death awards gold. |
| 4 | Rank | 6 medals displays Giggle Grandmaster. |
| 4 | High score | Score top 10 persists after reload. |

# 10. BUILD ORDER
1. Build skeleton: `index.html`, `style.css`, canvas, DOM screens, fixed-step loop, config, RNG, input, save.
2. Implement tilemap, camera, AABB physics, player movement, Jump, Air Bounce, Bounce Pad, one-way drop, falling death, Exit win, Level 1.
3. Add all Tier 1 presentation: pixel sprites, palette, pixel font, chiptune music, SFX, particles, screen shake, hit flash, HUD score, reduced motion, remappable keys.
4. Verify Tier 1 with tests. A player must be able to finish Level 1.
5. Implement Tier 2 systems: traps, environmental damage, physics objects, swim, enemies, slap, dodge, climb, spawn reset, unlocks.
6. Build Levels 2-4 using Tier 2 content.
7. Verify Tier 2 with tests.
8. Implement Tier 3 systems: landmarks, dash, rewards, decoration, switches/doors, puzzles, secrets, hints, boosts, collectibles, throw, score, keys/doors.
9. Build Levels 5-6 with Tier 3 content.
10. Verify Tier 3 with tests.
11. Implement Tier 4 systems: guards, flee, push/pull, transform, collectible creatures, combos, medals/ranks.
12. Add full Level 6 content, high score top 10, win screen medals/rank, level select medals.
13. Verify Tier 4 with tests and full playthrough.
14. Run sanity checks, debug API, and accessibility settings.

# 11. DEFINITION OF DONE
## Tier 1 Done
High level: A new player can start from the title, enter Level 1, move Brib, jump, use Air Bounce, use Bounce Pads, fall and restart, reach the Exit Pad, and see the win screen.
- [ ] Title screen shows and can start Level 1.
- [ ] Level 1 loads with Level Spawn and Exit Pad.
- [ ] Player can move left/right with remappable keys.
- [ ] Jump works with coyote and buffer.
- [ ] Air Bounce works once per air arc.
- [ ] Bounce Pads launch player.
- [ ] One-way lily pads support and Drop Through works.
- [ ] Falling below level kills and restarts level.
- [ ] Exit Pad triggers win.
- [ ] Game over, win, pause, level select, high scores, settings screens exist.
- [ ] HUD shows score only.
- [ ] Pixel art uses 16-colour palette and visible pixels.
- [ ] Pixel font renders UI.
- [ ] Chiptune music and retro SFX play.
- [ ] Particles, screen shake, hit flash work.
- [ ] Reduced motion disables shake and reduces particles.
- [ ] Remappable keys work in settings.

## Tier 2 Done
High level: A player can finish Levels 2-4 while dealing with water, hazards, enemies, physics objects, climb, dodge, and level unlock.
- [ ] Traps trigger and kill/launch correctly.
- [ ] Environmental damage zones kill on contact.
- [ ] Poison, Steam, Electric cycles match timers.
- [ ] Physics objects fall, break, and can be stood on.
- [ ] Swim works with jump kick and down sink.
- [ ] Exiting water with upward speed grants Air Bounce.
- [ ] Enemies move and contact kills.
- [ ] Slap stuns enemies and breaks fragile objects.
- [ ] Dodge crouches and avoids low hazards.
- [ ] Climb works on vine tiles.
- [ ] Death resets level state and player to Level Spawn.
- [ ] Completing a level unlocks the next level.
- [ ] Levels 2-4 are playable end-to-end.

## Tier 3 Done
High level: A player can finish Levels 5-6 with score, collectibles, keys, doors, switches, puzzles, secrets, hints, boosts, dash, throw, landmarks, and decoration.
- [ ] Dash works with cooldown and vertical cancel.
- [ ] Throw spawns peas with correct speed and lifetime.
- [ ] Peas break Wobble Mushrooms, stun/kill enemies, activate switches.
- [ ] Switches activate by contact or pea.
- [ ] Doors open/close with switches.
- [ ] Keys open Key Doors.
- [ ] Switch Chain and Bounce Route puzzles work.
- [ ] Secrets reveal and give reward.
- [ ] Hints show text after hold.
- [ ] Honey Shroom boosts speed and jump.
- [ ] Lily Gems add score and count.
- [ ] Level clear and no-death rewards add score.
- [ ] Landmarks inspect with hold Jump.
- [ ] Decoration renders without collision.
- [ ] Score persists across levels and resets to level start on death.
- [ ] Levels 5-6 are playable end-to-end.

## Tier 4 Done
High level: The full game is complete: 6 levels, all listed mechanics, advanced enemies, transform, creatures, combos, medals, ranks, and high scores.
- [ ] Toad Guard patrols, alerts, chases, and can be stunned.
- [ ] Puddler Flee flees and drops score without killing.
- [ ] Push and Pull move physics objects.
- [ ] Transform changes hitbox, speed, shield, and push strength.
- [ ] Guppy Buddy follows, absorbs one damage, and expires.
- [ ] Combo multiplier increases within 90-frame window and maxes at 5.
- [ ] Medals award Bronze/Silver/Gold based on clear, gems, no-death.
- [ ] Rank displays correctly from total medals.
- [ ] High scores save top 10 locally.
- [ ] Level select shows medals and unlocked levels.
- [ ] Win screen shows score, medal, rank.
- [ ] Full 6-level playthrough completes under 30 minutes on first clear target.
- [ ] All debug functions reach their system state.
- [ ] All tier tests pass.

# A. SANITY
| Check | Result |
| --- | --- |
| Sections present in required order | Valid. All required headings are present. |
| Tier 1 contains exactly core mechanics | Valid. Jump, Objectives, Falling, Map / World, Bounce are Tier 1. |
| Tier 2 contains supporting mechanics | Valid. All listed supporting mechanics are Tier 2. |
| Tier 3+ contains extra mechanics | Valid. All listed extra mechanics are Tier 3 or Tier 4. |
| No unlisted health/lives/timer system | Valid. One-hit death, no lives, no timer. Transform shield is a one-hit ability, not a health pool. |
| Win/lose matches “reach the exit” | Valid. Exit Pad wins; falling/hazards/deaths restart level. |
| HUD contains only score | Valid. In-game HUD table has only Score. |
| Screens are exactly required list | Valid. Title, pause, settings, game over, win, level select, high scores. |
| Art style is pixel, low-res, limited palette | Valid. 16 px tiles, 16-colour palette, no smoothing. |
| Palette is saturated and colour-blind safe | Valid. Orange, magenta, blue, yellow used with icons and luminance contrast; no red/green-only signalling. |
| Typography is pixel font | Valid. PixelFrog8 / Press Start 2P / monospace. |
| Music is chiptune | Valid. Square lead, triangle bass, noise hats, 140 BPM. |
| SFX are synthesized retro bleeps | Valid. WebAudio recipes provided. |
| Effects include screen shake, particles, hit flash | Valid. Numbers given. |
| Accessibility includes reduced motion and remappable keys | Valid. Settings and debug functions provided. |
| Levels are a handful and under 30 minutes | Valid. 6 levels, target 24 minutes. |
| Every system has named input or explicit non-interactive status | Valid. Interactive systems list inputs; decoration/landmarks have inspection or camera viewpoint rules. |
| No tier dependency violation | Valid. Tier 1 has no dependency on Tier 2/3/4. Tier 3 secret uses Boost, not Guppy. |
| Fixed numbers are consistent | Valid. Jump, bounce, gravity, timers, and score values match across sections. |
| Error found: Down input conflict with one-way drop | Fixed. One-way drop requires Down + Jump; Dodge uses Down alone. |
| Error found: HUD initially included objective text | Fixed. HUD is score only; Exit Pad is the in-world objective. |
| Error found: secret originally gave Guppy Buddy, a Tier 4 item | Fixed. Tier 3 secret gives Honey Shroom, a Tier 3 boost. |
