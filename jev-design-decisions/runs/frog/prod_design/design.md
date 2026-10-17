# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| A browser game that can be opened from `index.html` | §7, §10, §11 |
| A platformer where the player is a frog | §4, §5 |
| 2D side-view gameplay on X-Y plane | §1, §4 |
| Core verbs: run, jump, swim, lily-pad bounce, stomp | §4 |
| Short, complete, linear frog journey from pond to waterfall | §4 |
| Six authored levels: Pond Edge, Lily Rush, Reed Hollow, Stormy Creek, Cliffside Ponds, Great Waterfall | §4 |
| Optional dewdrop collection with per-level count | §4, §7 |
| Enemies and hazards: mosquito, dragonfly, thorn | §4 |
| Water, currents, lily pads, one-way platforms, moving platforms | §4 |
| Heron boss gates the ending in Level 6 | §4 |
| Save only unlocked level and completion state | §4, §7 |
| Title, Controls, Playing, Paused, Level Complete, Game Complete states | §7 |
| HUD with hearts, dewdrop count, and message area | §4, §7 |
| Readable pond visual style with clear safe/danger/objective language | §3, §5 |
| Audio feedback for important gameplay events | §6 |
| Vanilla HTML, CSS, and JavaScript only | §1, §2 |
| No build step, no external libraries, no Node/npm | §1, §2 |
| Deterministic fixed-step simulation | §1, §2 |
| Debug API and in-page test harness | §8, §9 |

## 0.2 Decisions

| Decision | gameplay.md | visual.md | engineering.md | Ruling / Reason |
| --- | --- | --- | --- | --- |
| Tier 1 scope | Defines full 6-level gameplay, boss, save, HUD, screens. | Defines full visual polish, effects, audio direction. | Defines full engineering, tests, debug API, placeholder-friendly runtime. | **Tier 1 is the complete playable gameplay game with placeholder/simple presentation and no required audible audio.** Tier 2 is full presentation and SFX. Tier 3 is music/ambience. Reason: the user asked for a frog platformer and the gameplay design defines a complete short game; Tier 1 should prove the full game works, while polish can be left unbuilt. |
| Audio implementation | Names required gameplay audio events. | Provides synthesized SFX recipes and music direction. | Expects optional `.ogg`/`.mp3` files, says missing audio must fail silently, and cuts music. | **Drop required external audio files.** Use browser WebAudio synthesis for Tier 2 SFX. Tier 1 may record audio events silently. Reason: no asset dependency, deterministic tests, visual already gives synthesis recipes, engineering allows missing audio. |
| Music | Not specified. | Specifies title, level, boss, and game-complete music. | Cuts music. | **Music is Tier 3 optional, not required for Tier 1 or Tier 2.** Reason: engineering cut, scope control, and the game is fully playable without music. |
| Screen shake and particles | Not required. | Requires small screen shake and particle effects. | Cuts screen shake and particle effects. | **Tier 1 uses minimal non-obscuring state feedback only: no screen shake, no particles.** Tier 2 implements visual.md effects and the small screen-shake table. Reason: keep Tier 1 buildable and readable, while preserving the visual designer’s intended feel as an improvement tier. |
| Visual art | Requires visible player, world objects, enemies, boss, exits, HUD. | Full soft pixel-art direction, palettes, animations. | Placeholder rendering is acceptable; missing images must not break the game. | **Tier 1 uses high-contrast placeholder shapes or simple generated canvas shapes.** Tier 2 implements full visual.md art direction. Reason: gameplay correctness first, presentation second. |
| Hitboxes vs visual sizes | Defines gameplay hitboxes. | Defines larger visual sizes for some entities. | Defines hitboxes and says visuals must not change collision. | **Gameplay hitboxes are canonical.** Visual sizes are presentation only. Reason: behavior and tests must remain stable. |
| Audio event list | Lists 10 required events. | Adds dewdrop, player death, boss lunge, exit activation, UI, perfect. | Requires 10 named events. | **Expand required SFX names to include the visual additions.** Core 10 events must be wired in Tier 1 as recorded events; all listed SFX are Tier 2 audible. Reason: the added cues materially improve feedback and are low scope when synthesized. |
| Boss persistence on death vs restart | Death respawn keeps boss dead and exit unlocked. | Boss death visual unlocks exit. | Restart Level resets boss if present; death respawn keeps boss dead. | **Player death after boss death keeps boss dead and exit unlocked. Restart Level resets the boss to alive and locks the exit again.** Reason: death should not punish the player by repeating the boss, but explicit restart is a full level reset. |
| Jump buffer test timing | Jump buffer is 0.12 s. | N/A. | Test says press jump 8 frames before landing. | **Use 6 frames before landing for the jump-buffer test.** 8 frames is 0.133 s, which exceeds the 0.12 s buffer. Reason: gameplay number is authoritative. |
| Variable jump cut scope | Generic release algorithm. | Surface jump should feel weaker. | Says jump cut applies only to land jumps, not water swimming; surface jump does not set `jumpCutApplied`. | **Variable jump cut applies to land jumps and lily-pad bounces. It does not apply to surface jumps or swimming.** Surface jumps set `jumpType = "surface"` and are not cut. Reason: water should feel dense and fixed; surface jumps are not normal land jumps. |
| Randomness | No random enemy spawns. | Some decorative sparkle/bob effects. | Requires deterministic tests and no runtime level generation. | **No `Math.random` in gameplay logic.** Decorative effects use deterministic time/entity-id patterns. Reason: determinism and testability. |
| One-way platform drop-through | Player cannot drop through. | Thin visual implies pass-through from below. | Player cannot drop through. | **No drop-through.** Reason: all three designs agree. |
| In-level save | No in-level save. | N/A. | No in-level save. | **No in-level save.** Checkpoints and respawn handle failure. |
| Controls | Keyboard only. | N/A. | Keyboard only. | **Keyboard only.** No controller, mobile, or remappable controls. |
| Level validation | Levels are authored. | N/A. | Structural validation only. | **Validation is structural only.** No solvability checker. |
| Camera feel | Deadzone, lookahead, smooth follow. | N/A. | Gives smoothing factor 10. | **Use engineering camera algorithm with smoothing factor 10.** |
| Level Complete message priority | Level Complete is a screen. | Level Complete is a screen, not HUD message. | Same. | **HUD message priority is Checkpoint > Tutorial prompt > Level name.** Level Complete is a separate screen. |
| Dropped/cut items | Cuts double jump, wall jump, dash, tongue, power-ups, upgrades, score, timer, star ratings, level select, open world, secrets, multiple frogs, companion, inventory, weapon, health pickups, lives, meta-unlocks, difficulty modes, controller, remappable controls. | Cuts objective arrow, minimap, score, timer, star ratings, level select UI, power-up icons, health pickup icons, controller icons, settings menu, accessibility settings, cutscenes, extra characters, fireflies, lightning, floating petals, decorative hazards/platforms, water wipe, loading screens, 3D-style backgrounds, parallax beyond 3 layers, heavy post-processing, normal-movement shake. Also music/ambience cut from required scope by ruling. | Cuts procedural levels, level select, score, timer, star ratings, lives, health pickups, power-ups, upgrades, controller, remappable controls, mobile touch, music, mute UI, volume UI, settings, minimap, objective arrow, screen shake, particles, damage numbers, floating text, hitbox debug draw, FPS counter, console debug UI, network, cloud save, analytics, error reporting, service worker, PWA, WebGL, external libraries, build step, TypeScript, ES modules, Node tests, npm, test runner, unit framework, solvability checker, random spawns, dynamic difficulty, secrets, hidden paths, multiple frogs, companion, inventory, weapons, difficulty modes. | **All listed cuts remain cut.** Anything dropped from the three documents is either explicitly cut by a designer or moved to an optional higher tier as documented above. |

## 0.3 Tiers

| Tier | Name | Meaning | Includes | Excludes |
| --- | --- | --- | --- | --- |
| Tier 1 | Core playable frog platformer | Minimal viable game: the full designed gameplay can be played from title to game complete. | All 6 authored levels, player movement, jumping, water, lily pads, one-way platforms, moving platforms, currents, enemies, thorns, stomping, damage, death/respawn, dewdrops, checkpoints, exits, boss, save, screens, HUD, tutorial prompts, camera, debug API, test harness, placeholder visuals, silent audio event recording. | Full pixel art, particles, screen shake, audible SFX, music, ambience, decorative polish. |
| Tier 2 | Presentation and feedback | A better-looking, better-feeling game. | Full visual.md art direction, level palettes, character animations, effects, small screen shake, transitions, synthesized SFX, accessibility readability rules. | Music and ambience. |
| Tier 3 | Music and ambience | Complete audio atmosphere. | Synthesized title/level/boss/game-complete music and ambience per visual.md. | Nothing required beyond Tier 2 if skipped. |

System tier map:

| System | Tier |
| --- | --- |
| Game state machine | Tier 1 |
| Save system | Tier 1 |
| Level data and validation | Tier 1 |
| Player movement | Tier 1 |
| Jumping | Tier 1 |
| Water | Tier 1 |
| Lily pads | Tier 1 |
| One-way platforms | Tier 1 |
| Moving platforms | Tier 1 |
| Currents | Tier 1 |
| Stomping | Tier 1 |
| Damage and invulnerability | Tier 1 |
| Death and respawn | Tier 1 |
| Dewdrops | Tier 1 |
| Checkpoints | Tier 1 |
| Exits | Tier 1 |
| Enemies | Tier 1 |
| Boss | Tier 1 |
| HUD | Tier 1 |
| Tutorial prompts | Tier 1 |
| Camera | Tier 1 |
| Debug API | Tier 1 |
| Test harness | Tier 1 |
| Placeholder visuals | Tier 1 |
| Full pixel art | Tier 2 |
| Character animations | Tier 2 |
| Particles and screen shake | Tier 2 |
| Synthesized SFX | Tier 2 |
| Music and ambience | Tier 3 |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

The game is 2D side-view. All gameplay coordinates are logical pixels.

| Convention | Value / Rule |
| --- | --- |
| Logical resolution | 1280 x 720 px |
| Tile size | 32 px |
| Logical update rate | 60 updates/sec |
| Fixed timestep | `dt = 1 / 60` seconds |
| X axis | Increases to the right |
| Y axis | Increases downward |
| Origin | Top-left |
| Speeds | px/s |
| Accelerations | px/s² |
| Timers | seconds |
| Rectangles | Top-left `{ x, y, w, h }` |
| Center-based entities | Spawn, dewdrops, checkpoints, exits, enemies, boss use center coordinates |
| Center to rect | `x = cx - w / 2`, `y = cy - h / 2` |
| Rendering | May run at display refresh rate, but gameplay uses fixed steps |
| Max frame time | 0.25 s accumulator clamp |
| Presentation pixel grid | 16 logical px, Tier 2 |
| Presentation render scale | 2x, Tier 2 |
| Sprite snap | Round sprite draw positions to 2 px screen grid, Tier 2 |
| Scaling | Nearest-neighbor, Tier 2 |

Canonical constants:

| Constant | Value | Notes |
| --- | ---: | --- |
| `VIEW_W` | 1280 | Canvas logical width |
| `VIEW_H` | 720 | Canvas logical height |
| `TILE` | 32 | Tile size |
| `DT` | `1 / 60` | Fixed timestep |
| `MAX_FRAME_TIME` | 0.25 | Accumulator clamp |
| `PLAYER_W` | 20 | Player hitbox width |
| `PLAYER_H` | 28 | Player hitbox height |
| `RUN_MAX_SPEED` | 240 | Ground/air max horizontal speed |
| `GROUND_ACCEL` | 1800 | Ground acceleration |
| `AIR_ACCEL` | 1200 | Air acceleration |
| `GROUND_FRICTION` | 1600 | Ground friction with no input |
| `AIR_FRICTION` | 200 | Air friction with no input |
| `GRAVITY` | 1400 | Normal gravity |
| `MAX_FALL_SPEED` | 900 | Normal max fall speed |
| `JUMP_VY` | -520 | Land jump velocity |
| `COYOTE_TIME` | 0.08 | Seconds |
| `JUMP_BUFFER_TIME` | 0.12 | Seconds |
| `JUMP_CUT_FACTOR` | 0.45 | Variable jump cut multiplier |
| `WATER_GRAVITY` | 350 | Water sink acceleration |
| `WATER_MAX_FALL_SPEED` | 220 | Water max downward speed |
| `WATER_MAX_SPEED` | 160 | Water max horizontal speed |
| `WATER_ACCEL` | 700 | Water horizontal acceleration |
| `WATER_FRICTION` | 900 | Water horizontal friction |
| `SURFACE_JUMP_VY` | -460 | Water surface jump velocity |
| `SWIM_UP_ACCEL` | 900 | Swim upward acceleration |
| `SWIM_UP_MAX_VY` | -220 | Swim upward max velocity |
| `WATER_SURFACE_TOLERANCE` | 6 | Surface detection tolerance |
| `LILY_BOUNCE_VY` | -620 | Lily pad bounce without jump held |
| `LILY_BOUNCE_JUMP_VY` | -680 | Lily pad bounce with jump held |
| `STOMP_BOUNCE_VY` | -380 | Normal enemy stomp bounce |
| `BOSS_STOMP_BOUNCE_VY` | -420 | Boss stomp bounce |
| `STOMP_TOLERANCE` | 4 | Normal stomp top tolerance |
| `BOSS_STOMP_ZONE` | 12 | Boss stomp zone height |
| `MAX_HEARTS` | 3 | Player hearts |
| `INVULN_TIME` | 1.2 | Invulnerability seconds |
| `KNOCKBACK_X` | 260 | Horizontal knockback speed |
| `KNOCKBACK_Y` | -220 | Vertical knockback speed |
| `DEATH_TIME` | 0.6 | Death animation seconds |
| `CURRENT_FORCE` | 120 | Current acceleration magnitude |
| `CAMERA_DEADZONE_X` | 200 | Horizontal camera deadzone |
| `CAMERA_DEADZONE_Y` | 120 | Vertical camera deadzone |
| `CAMERA_LOOKAHEAD` | 40 | Facing lookahead |
| `CAMERA_SMOOTHING` | 10 | Exponential smoothing factor |
| `SAVE_KEY` | `"frog-pond-to-peak-save"` | localStorage key |
| `DEWDROP_W` | 16 | Dewdrop hitbox width |
| `DEWDROP_H` | 16 | Dewdrop hitbox height |
| `CHECKPOINT_W` | 32 | Checkpoint hitbox width |
| `CHECKPOINT_H` | 32 | Checkpoint hitbox height |
| `EXIT_W` | 48 | Exit hitbox width |
| `EXIT_H` | 64 | Exit hitbox height |
| `MOSQUITO_W` | 24 | Mosquito hitbox width |
| `MOSQUITO_H` | 20 | Mosquito hitbox height |
| `DRAGONFLY_W` | 28 | Dragonfly hitbox width |
| `DRAGONFLY_H` | 16 | Dragonfly hitbox height |
| `HERON_W` | 56 | Heron hitbox width |
| `HERON_H` | 80 | Heron hitbox height |

Boss constants:

| Constant | Value |
| --- | ---: |
| `BOSS.HP` | 6 |
| `BOSS.PHASE1.idle` | 1.2 |
| `BOSS.PHASE1.lunge` | 0.4 |
| `BOSS.PHASE1.recover` | 0.8 |
| `BOSS.PHASE1.lungeSpeed` | 320 |
| `BOSS.PHASE2.idle` | 0.8 |
| `BOSS.PHASE2.lunge` | 0.4 |
| `BOSS.PHASE2.recover` | 0.6 |
| `BOSS.PHASE2.lungeSpeed` | 380 |

Presentation constants, Tier 2:

| Constant | Value | Notes |
| --- | ---: | --- |
| `MAX_PARTICLES` | 128 | Max active particles |
| `MAX_BLINK_HZ` | 8 | Max invulnerability blink toggles/sec |
| `UI_FAST_ANIM` | 0.15 | Fast UI animation |
| `UI_MEDIUM_ANIM` | 0.25 | Medium UI animation |
| `EFFECT_FAST` | 0.10 | Fast effect |
| `EFFECT_MEDIUM` | 0.20 | Medium effect |
| `EFFECT_LARGE` | 0.40 | Large effect |

## 1.2 Important conventions

- Use vanilla HTML, CSS, and JavaScript only.
- No Node, npm, build step, external libraries, or ES modules.
- Use classic `<script>` files wrapped in IIFEs.
- Attach code only to `window.FrogGame`, `window.__game`, and, in `test.html`, `window.__test`, `window.__testsDone`, `window.__testResults`.
- Logic always updates in fixed `dt = 1 / 60` steps.
- Rendering must not modify gameplay state.
- All gameplay numbers must come from `FrogGame.Constants`.
- No gameplay logic may depend on canvas pixels, DOM measurements, or camera position.
- No `Math.random` in gameplay logic. Decorative effects use deterministic time/entity-id patterns.
- Rectangles use top-left coordinates unless explicitly marked center-based.
- Player position is stored as center coordinates.
- Enemy, boss, dewdrop, checkpoint, and exit data use center coordinates.
- Solid, one-way, lily pad, water, current, thorn, and moving platform data use top-left rectangles.
- Collision is axis-separated.
- Stomp checks use the player’s bottom position from before vertical movement.
- Save data stores only `unlocked_level` and `completed`.
- In-level progress, dewdrops, checkpoint state, and boss HP are not saved.
- Audio must not block boot.
- Missing audio must fail silently.
- Audio may unlock on first user gesture.
- Tests must not use real timers, network, image files, audio files, or user interaction.
- Tests drive the game only through `window.__game`.
- `getState()` must return JSON-serializable data only.
- Effects must not obscure the player or enemy hitboxes for more than 2 frames, Tier 2.
- No gameplay-critical information appears only in the top 64 px except HUD.
- No lightning, strobing, or motion that hides hitboxes.

# 2. CONTRACTS

## 2.1 Module layout

Required files:

```text
index.html
test.html
css/style.css

js/constants.js
js/utils.js
js/save.js
js/input.js
js/audio.js
js/assets.js
js/levels.js
js/level.js
js/collision.js
js/player.js
js/enemies.js
js/camera.js
js/hud.js
js/ui.js
js/game.js
js/debug.js
js/main.js

test/test-harness.js
test/tests.js
```

Optional files:

```text
assets/images/*
```

Audio files are not required. Tier 2 audio is synthesized with WebAudio. `js/assets.js` may load optional images, but the game must run without them.

## 2.2 Global context

Global namespace:

```js
window.FrogGame = {
  Constants,
  Utils,
  Save,
  Input,
  Audio,
  Assets,
  LevelData,
  Level,
  Collision,
  Player,
  Enemies,
  Camera,
  HUD,
  UI,
  Game,
  Debug,
  main
};
```

Runtime game state must contain every field needed by gameplay records:

```js
{
  gameState: "title" | "controls" | "playing" | "paused" | "levelComplete" | "gameComplete",
  version: "1.0.0",

  save: {
    exists: boolean,
    unlocked_level: number,
    completed: boolean
  },

  title: {
    options: [string],
    selectedIndex: number,
    confirm: null | {
      prompt: string,
      options: [string],
      selectedIndex: number
    }
  },

  level: {
    index: number,
    id: number,
    name: string,
    width: number,
    height: number,
    time: number,
    respawn: { x, y }
  },

  player: {
    x: number,
    y: number,
    vx: number,
    vy: number,
    facing: number,
    onGround: boolean,
    inWater: boolean,
    onSurface: boolean,
    hearts: number,
    invulnTimer: number,
    coyoteTimer: number,
    jumpBufferTimer: number,
    jumpCutApplied: boolean,
    jumpType: "none" | "land" | "lily" | "surface" | "stomp" | "swim",
    dead: boolean,
    deathTimer: number,
    deaths: number,
    standingPlatformId: null | string,
    wasInWater: boolean
  },

  input: {
    left: boolean,
    right: boolean,
    jumpHeld: boolean
  },

  world: {
    solids: [ { id, x, y, w, h } ],
    oneWays: [ { id, x, y, w, h, movingId } ],
    lilyPads: [ { id, x, y, w, h } ],
    waters: [ { id, x, y, w, h } ],
    currents: [ { id, x, y, w, h, force } ],
    thorns: [ { id, x, y, w, h } ],
    movingPlatforms: [
      {
        id,
        x,
        y,
        previousX,
        previousY,
        axis,
        amplitude,
        period
      }
    ]
  },

  dewdrops: {
    collected: number,
    total: number,
    collectedIds: [number]
  },

  enemies: [
    {
      id,
      type,
      alive,
      x,
      y,
      w,
      h,
      minX,
      maxX,
      baseY,
      direction
    }
  ],

  boss: {
    exists: boolean,
    alive: boolean,
    hp: number,
    state: "idle" | "lunge" | "recover" | "dead",
    x: number,
    y: number,
    w: number,
    h: number,
    minX: number,
    maxX: number,
    direction: number,
    timer: number
  },

  exit: {
    x: number,
    y: number,
    w: number,
    h: number,
    locked: boolean,
    active: boolean
  },

  checkpoint: null | {
    x: number,
    y: number,
    w: number,
    h: number,
    activated: boolean
  },

  message: {
    text: string,
    remaining: number,
    priority: number
  },

  tutorial: {
    activeId: null | string,
    flags: {
      firstHorizontalInput: boolean,
      firstJump: boolean,
      firstStomp: boolean,
      firstWaterJumpOrSwim: boolean,
      firstLilyBounce: boolean,
      firstOneWayLanding: boolean,
      firstMovingPlatformRide: boolean,
      firstCurrentForce: boolean,
      firstBossStomp: boolean
    },
    shownTime: number
  },

  levelComplete: null | {
    levelName: string,
    dewdropsCollected: number,
    dewdropsTotal: number,
    perfect: boolean,
    nextLevel: number
  },

  gameComplete: null | {
    completed: boolean
  },

  camera: {
    x: number,
    y: number
  },

  audio: {
    enabled: boolean,
    lastEvent: null | string,
    musicState: null | string
  }
}
```

`getState()` returns this shape or a JSON-safe subset that includes all fields above. It must not contain functions, DOM nodes, canvas contexts, or circular references.

## 2.3 Module specifics

| Module | Required exports / functions | Purpose |
| --- | --- | --- |
| `FrogGame.Constants` | Constant object | All gameplay numbers |
| `FrogGame.Utils` | `clamp`, `lerp`, `rectFromCenter`, `rectsOverlap`, `applyFriction`, `deepCopy` | Shared math and data utilities |
| `FrogGame.Save` | `load`, `save`, `clear`, `exists` | localStorage with memory fallback |
| `FrogGame.Input` | `init`, `handleKeyDown`, `handleKeyUp`, `clearEdges`, `getState`, `setDebug` | Keyboard state and debug input |
| `FrogGame.Audio` | `play`, `setEnabled`, `getLastEvent`, `unlock`, `initSynth`, `stopMusic`, `setMusicState` | Silent event recording plus Tier 2/3 synthesis |
| `FrogGame.Assets` | `load`, `getImage`, `hasImage` | Optional image loading |
| `FrogGame.LevelData` | `LEVELS`, `validate`, `testLevel`, `generateSmokeLevel` | Authored level data and test factories |
| `FrogGame.Level` | `fromData`, `reset`, `updateMovingPlatforms` | Runtime level creation and reset |
| `FrogGame.Collision` | `playerRect`, `movePlayer`, `resolveHorizontalSolids`, `resolveVerticalSolids`, `resolveOneWays`, `resolveLilyPads`, `checkStomp` | Axis-separated movement and collision |
| `FrogGame.Player` | `create`, `update`, `damage`, `die`, `respawn` | Player behavior |
| `FrogGame.Enemies` | `create`, `update`, `stomp`, `applyPlayerEnemyCollisions` | Enemy and hazard behavior |
| `FrogGame.Camera` | `create`, `update` | Camera follow and clamp |
| `FrogGame.HUD` | `render`, `updateHearts`, `updateDewdrops`, `showMessage` | DOM HUD |
| `FrogGame.UI` | `render`, `showScreen`, `handleInput`, `getTitleOptions`, `handleTitle`, `handlePause`, `handleLevelComplete`, `handleGameComplete` | Screens and menus |
| `FrogGame.Game` | `boot`, `update`, `render`, `setState`, `loadLevel`, `loadTestLevel`, `completeLevel`, `completeGame`, `restartLevel`, `respawnPlayer`, `updateTutorial`, `updateMessages` | Top-level game orchestration |
| `FrogGame.Debug` | `create`, `getState`, `step`, `until` | `window.__game` debug API |
| `FrogGame.main` | `init` | Boot entry point |

# 3. VISUAL SPEC

The game looks like a small, bright, readable pond world rendered in soft pixel art. The frog is small and bright green; water is inviting blue/cyan; lily pads are saturated green; one-way leaves are pale and thin; hazards are red/orange; checkpoints are pink lotus flowers; exits are white/blue waterfalls. The visual language must make safe, bouncy, dangerous, and objective elements instantly distinguishable. Backgrounds are calm and low-contrast; gameplay objects are high-contrast and outlined. The world should feel small, bouncy, calm, and forgiving, while the final level feels grand.

Lighting and atmosphere:

| Level / State | Lighting / Atmosphere | Tier |
| --- | --- | --- |
| Title | Soft morning or dusk pond, frog on lily pad, distant waterfall, gentle water animation | Tier 2 |
| Level 1 Pond Edge | Bright, calm morning, soft sky gradient, distant rounded hills, light mist, no dark elements | Tier 2 |
| Level 2 Lily Rush | Bright midday water, reflections, dim background lily pads, soft ripples | Tier 2 |
| Level 3 Reed Hollow | Quiet vertical mist, tall reed silhouettes, vertical vines, dim background pools | Tier 2 |
| Level 4 Stormy Creek | Dark clouds, light rain streaks, wind-blown leaves, darker water, no lightning | Tier 2 |
| Level 5 Cliffside Ponds | Twilight cliffside, distant moon, hanging vines, small background ponds | Tier 2 |
| Level 6 Great Waterfall | Grand bright final space, large soft waterfall, bright mist, wet rocks, light rays | Tier 2 |
| Game Complete | Large sky, tiny pond, small frog silhouette, soft waterfall glow | Tier 2 |

Space and layer rules:

| Rule | Value / Behavior | Tier |
| --- | --- | --- |
| Layer order | Sky/far background, midground scenery, gameplay tiles/entities, particles/effects, HUD/menus | Tier 1/2 |
| Parallax | No more than 3 layers | Tier 2 |
| Background contrast | Low saturation, low detail | Tier 2 |
| Midground contrast | Medium saturation | Tier 2 |
| Gameplay contrast | Full saturation, clear outlines | Tier 1/2 |
| HUD contrast | Highest contrast | Tier 1 |
| Decorative hazards | Forbidden | Tier 1 |
| Decorative platforms that look real | Forbidden | Tier 1 |
| Background thorn-like shapes | Forbidden | Tier 1 |
| Background water that looks playable | Forbidden unless it is actual water | Tier 1 |
| Vertical level objective glow | 16 px tall glow at top edge, `rgba(191, 239, 255, 0.35)`, no arrow or text | Tier 2 |
| Level bounds | Reeds, cliffs, rocks, foliage, or canopy; no bright invisible wall lines | Tier 2 |

Color roles:

| Role | Color / Style | Purpose | Tier |
| --- | --- | --- | --- |
| Safe ground | Warm brown / moss green | Walkable solid surface | Tier 1/2 |
| One-way leaf | Pale yellow-green | Thin platform, not bouncy | Tier 1/2 |
| Lily pad | Bright saturated green | Bouncy platform | Tier 1/2 |
| Water | Blue / cyan | Safe movement space | Tier 1/2 |
| Current | Cyan arrows/chevrons | Horizontal force direction | Tier 1/2 |
| Hazard | Red / orange | Damage | Tier 1/2 |
| Collectible | White / cyan dewdrop | Optional pickup | Tier 1/2 |
| Checkpoint | Pink / white lotus | Respawn and heal | Tier 1/2 |
| Exit | White / blue waterfall | Level objective | Tier 1/2 |
| Player | Bright green | Protagonist | Tier 1/2 |
| Enemy | Indigo / cyan / slate | Threat | Tier 1/2 |
| UI accent | Amber | Selection, perfect, important highlight | Tier 1/2 |

Typography and UI style:

| Element | Rule | Tier |
| --- | --- | --- |
| Font | Clean pixel font, or readable monospace pixel fallback | Tier 2 |
| Small / prompt text | 18 px | Tier 1 |
| Heading text | 36 px | Tier 1 |
| Title text | 54 px | Tier 2 |
| Primary text | `#FFFFFF` | Tier 1 |
| Secondary text | `#D8E8E0` | Tier 1 |
| Accent text | `#FFC24A` | Tier 1 |
| Danger text | `#FF6A5A` | Tier 1 |
| Text outline | `#1B2A1F` | Tier 1 |
| Text shadow | 2 px downward, `rgba(0,0,0,0.35)` | Tier 2 |
| UI panel fill | `rgba(16, 28, 24, 0.72)` | Tier 1 |
| UI panel border | `rgba(255, 255, 255, 0.18)` | Tier 1 |
| UI panel radius | 12 px | Tier 2 |
| UI panel padding | 16 px | Tier 1 |
| Menu selected highlight | Amber rounded highlight | Tier 1 |
| Frog cursor | 32 x 32 px left of selected option | Tier 2 |

Visual recipe table:

| Entity / Element | Visual recipe | Key colors | Animation / motion | Tier | Gameplay rule implied |
| --- | --- | --- | --- | --- | --- |
| Player frog | 32 x 32 visual centered on player X, bottom aligned to hitbox bottom; bright green body, pale belly, dark outline, clear eyes | Body `#59C94C`, light `#8FE76B`, belly `#EAF9D8`, outline `#1B2A1F` | Idle 2 frames 12 fps; run 4 frames 12 fps; swim 2 frames 8 fps; death 2 frames 10 fps | Tier 2 | Facing, invulnerability blink, death state must be visible |
| Player invulnerable | Blink between full opacity and 35% opacity | Hurt tint `#FF5A5A` optional | 8 toggles/sec | Tier 1/2 | Player cannot take damage while invulnerable |
| Player death | Gray tint, X eyes, deflate/fall over | Death tint `#8A9A92` | 0.6 s | Tier 1/2 | Input stops, respawn after 0.6 s |
| Solid ground | 32 px tiles, bright top edge, darker body, rounded/beveled corners | Level palette | None | Tier 2 | Blocks movement from all sides |
| One-way leaf | 128 x 16 thin leaf, pale yellow-green, slight stem, underside shadow | Leaf `#C9D97A`, shadow `#7FA34A`, stem `#5C7A32` | Bend 2-3 px on landing, return 0.10 s | Tier 2 | Blocks only from below, no drop-through |
| Moving leaf | Same leaf plus 2 faint trails, slight tilt, bend 3 px while carrying | Trail alpha 0.30 and 0.15 | Sine motion, motion trail | Tier 2 | Carries player |
| Lily pad | 64 x 24 bright green oval, top 16 px bounce surface, lower 8 px thickness, droplet near center | Pad `#4FCB5A`, light `#8BEA86`, dark `#2E8A3E`, droplet `#DFFBFF` | Squash 20% for 2 frames, green ring, 3-4 droplets | Tier 2 | Bounces player, cannot stand |
| Water | Water rectangle exactly matches gameplay water rect; blue gradient, animated surface | Overlay `rgba(42, 123, 181, 0.65)`, surface `#7FD8FF`, deep `#2A7BB5` | 4-frame wave loop 8 fps, 1-2 px offset | Tier 2 | Safe movement space, not hazard |
| Current | Animated chevrons inside water rectangle | Chevron `#BFF6FF`, alpha 0.50 | 16 x 8 chevrons, 64 px spacing, 60 px/s in force direction | Tier 2 | Applies horizontal force |
| Thorn | 48 x 16 static spikes, dark base, bright tips | Spike `#E84A3F`, light `#FF7A5C`, base `#8A2A22` | None | Tier 2 | Touch damages player |
| Dewdrop | 16 x 16 droplet, white highlight, cyan body | Body `#DFFBFF`, highlight `#FFFFFF`, shadow `#6FD8FF` | 4 px bob, 1.2 s period; sparkle every 0.8 s | Tier 2 | Optional collectible |
| Checkpoint lotus | 32 x 32 lotus, inactive dim/closed, active bright/open, touching bloom | Petal `#FFB7D5`, light `#FFD9E8`, dark `#C76BA0`, glow `rgba(255,183,213,0.35)` | Bloom 4 frames 12 fps, 0.30 s | Tier 2 | Sets respawn and refills hearts |
| Active exit | 64 x 80 waterfall visual centered on 48 x 64 hitbox; bright core, blue edges, mist, bubbles | Core `#FFFFFF`, water `#BFEFFF`, edge `#6FCBFF`, mist `rgba(255,255,255,0.35)` | 4-frame flow loop 10 fps | Tier 2 | Touch completes level |
| Locked exit | Still dark blue sheet, no flow/mist, dark lotus seal | Water `#4A7A9A`, edge `#2F4F6A`, seal `#1B2A1F` | None | Tier 2 | Level 6 exit inactive until boss dead |
| Exit activation | Seal cracks, water bursts, mist appears | Active exit colors | 0.40 s | Tier 2 | Boss death unlocks exit |
| Mosquito | 32 x 28 visual centered on 24 x 20 hitbox; dark indigo body, thin legs, fast wings, red eyes | Body `#5A5F7A`, wing `#C9D9FF`, eye `#FF5A5A` | Wings 2 frames 20 fps; small body bob | Tier 2 | Stompable flying enemy |
| Dragonfly | 32 x 24 visual centered on 28 x 16 hitbox; long cyan body, two wing pairs, motion streak | Body `#2FA8C8`, light `#4FD8D8`, wing `#DFFBFF`, eye `#FF5A5A` | Wings 2 frames 24 fps; 2 px streak alpha 0.25 | Tier 2 | Faster stompable flying enemy |
| Heron boss | 64 x 80 visual centered on 56 x 80 hitbox; tall slate bird, long neck/beak, large head, red eye | Body `#8A93A8`, light `#C0C8D8`, dark `#4A5268`, beak `#E8A33F`, eye `#FF5A5A` | Idle 2 frames 6 fps; lunge 2 frames 12 fps; dead 2 frames 8 fps | Tier 2 | Boss with head stomp zone |
| Heron stomp band | 40 x 12 cyan band across head | Band `#BFF6FF`, alpha 0.80 | Flash white 2 frames on hit | Tier 2 | Top 12 px of boss hitbox is stompable |
| Boss HP droplets | 6 droplets 12 x 12, 4 px spacing, above head | Cyan remaining, amber `#FFC24A` at HP 3 or less | Fade on loss | Tier 2 | Shows boss HP locally |
| Heart full | 32 x 32 red heart | Full `#FF5A6E`, highlight `#FFD1DC` | Loss crack/fade 0.20 s; refill bottom-to-top 0.20 s | Tier 2 | Player health |
| Heart empty | 32 x 32 dark outline heart | Empty `#3A4A5A` | None | Tier 2 | Lost health |
| Dewdrop HUD icon | 24 x 24 dewdrop icon | Same as collectible | Pulse 0.15 s on collect | Tier 2 | Optional collection count |
| Message panel | Rounded translucent panel | Panel fill/border per UI style | Fade in 0.20 s, fade out 0.30 s | Tier 2 | Shows level name, checkpoint, tutorial |

Effects and screen shake, Tier 2:

| Event | Visual effect | Screen shake | Duration |
| --- | --- | ---: | ---: |
| Stomp | Puff, enemy squish | 2 px | 0.05 s |
| Boss hit | Head flash, feather puff, HP droplet fades | 3 px | 0.08 s |
| Boss death | White flash, feather burst, exit activates | 6 px | 0.20 s |
| Player damage | Red flash on frog, heart loss | 2 px | 0.05 s |
| Run | Small dust puffs every 0.15 s | None | — |
| Jump | Small dust puff or water splash if near water | None | — |
| Land | Small dust puff | None | — |
| Enter water | Splash ring, 4-6 droplets | None | — |
| Swim | Small bubbles/wake | None | — |
| Surface jump | Small ripple | None | — |
| Lily bounce | Green ring, pad squash, droplets | None | — |
| Dewdrop collect | Pop upward 4 px, fade 0.15 s, 4 sparkles | None | — |
| Checkpoint | Lotus bloom, hearts refill, pink sparkles | None | — |
| Exit locked touch | Subtle dim pulse | None | — |
| Perfect level complete | Golden sparkle around dewdrop count | None | — |

Transitions:

| Transition | Style | Duration | Tier |
| --- | --- | ---: | --- |
| To title | Fade to dark green | 0.20 s | Tier 2 |
| Title to level | Fade from dark green | 0.20 s | Tier 2 |
| Level complete to next level | Fade to dark green | 0.20 s | Tier 2 |
| Death to respawn | Fade out, then fade in | 0.20 s | Tier 2 |
| Pause open | Dark overlay fade | 0.15 s | Tier 1/2 |
| Pause close | Dark overlay fade | 0.15 s | Tier 1/2 |
| Game complete | Slow fade | 0.40 s | Tier 2 |

Visual rules where a visual implies gameplay:

| Visual | Implied rule | Ruling |
| --- | --- | --- |
| Locked exit is still/dark/sealed | Exit does not complete level | Gameplay owns exit active state; visual must match `exit.active` |
| Current chevrons point left/right | Current pushes in that direction | Force value from level data owns behavior; visual direction must match sign |
| Lily pad is bright green and bouncy | Player bounces, cannot stand | Gameplay owns bounce; visual must not make it look like a one-way leaf |
| One-way leaf is thin | Player can pass through from below | Gameplay owns one-way collision; no drop-through |
| Thorn is red/orange spikes | Touch damages player | Gameplay owns damage; visual must not animate in a misleading way |
| Lotus checkpoint blooms | Respawn point set and hearts refill | Gameplay owns checkpoint behavior |
| Active waterfall flows | Touch completes level | Gameplay owns exit completion |
| Boss head band is cyan | Top 12 px is stomp zone | Gameplay owns stomp zone; visual band is guidance |

# 4. GAMEPLAY SPEC

The player is a small frog traveling through six short 2D side-view levels from a quiet pond to the Great Waterfall. The core loop is: spawn, move through the level, optionally collect dewdrops, avoid or stomp enemies, use water/lily pads/platforms/currents, reach the waterfall exit, and unlock the next level. The frog can run, jump, swim, bounce on lily pads, and stomp enemies. The final level contains a Heron boss that gates the ending. The game is linear, short, forgiving, and readable.

## 4.1 Records

Save record:

```js
{
  unlocked_level: 1,
  completed: false
}
```

Level record:

```js
{
  id,
  name,
  width,
  height,
  spawn: { x, y },
  solids: [ { id, x, y, w, h } ],
  oneWays: [ { id, x, y, w, h, movingId } ],
  lilyPads: [ { id, x, y, w, h } ],
  waters: [ { id, x, y, w, h } ],
  currents: [ { id, x, y, w, h, force } ],
  thorns: [ { id, x, y, w, h } ],
  enemies: [ { id, type, x, y, w, h, minX, maxX, baseY, direction, alive } ],
  dewdrops: [ { id, x, y, w, h, collected } ],
  checkpoint: { id, x, y, w, h, activated } | null,
  exit: { id, x, y, w, h, locked, active },
  movingPlatforms: [ { id, start, current, previous, axis, amplitude, period } ],
  boss: runtimeBoss | null,
  time: 0,
  respawn: { x, y },
  events: tutorialEventFlags
}
```

Player record:

```js
{
  x,
  y,
  vx,
  vy,
  facing: 1,
  onGround: false,
  inWater: false,
  onSurface: false,
  hearts: 3,
  invulnTimer: 0,
  coyoteTimer: 0,
  jumpBufferTimer: 0,
  jumpCutApplied: false,
  jumpType: "none",
  dead: false,
  deathTimer: 0,
  deaths: 0,
  standingPlatformId: null,
  wasInWater: false
}
```

Enemy record:

```js
{
  id,
  type: "mosquito" | "dragonfly",
  x,
  y,
  w,
  h,
  minX,
  maxX,
  baseY,
  direction: 1 | -1,
  alive: true
}
```

Boss record:

```js
{
  id: "boss-0",
  type: "heron",
  x,
  y,
  w: 56,
  h: 80,
  hp: 6,
  state: "idle",
  timer: 1.2,
  direction: 1,
  alive: true,
  minX: 100,
  maxX: 1180
}
```

Dewdrop record:

```js
{
  id,
  x,
  y,
  w: 16,
  h: 16,
  collected: false
}
```

Checkpoint record:

```js
{
  id,
  x,
  y,
  w: 32,
  h: 32,
  activated: false
}
```

Exit record:

```js
{
  id,
  x,
  y,
  w: 48,
  h: 64,
  locked: boolean,
  active: boolean
}
```

Moving platform record:

```js
{
  id,
  start: { x, y },
  current: { x, y },
  previous: { x, y },
  axis: "x" | "y",
  amplitude,
  period
}
```

## 4.2 Level rosters

Level data uses top-left rectangles unless marked center. Enemy, dewdrop, checkpoint, and exit coordinates are centers.

### Level 1: Pond Edge — Tier 1

| Field | Value |
| --- | --- |
| id | 1 |
| name | Pond Edge |
| width | 2000 |
| height | 720 |
| estimated time | 45-60 seconds |
| purpose | Teach movement, jumping, stomping, objective |
| spawn center | 100, 626 |
| total dewdrops | 5 |
| checkpoint center | 1700, 624 |
| exit center | 1900, 608 |
| exit locked | false |
| boss | none |

| Entity | x | y | w | h | Extra |
| --- | ---: | ---: | ---: | ---: | --- |
| solid | 0 | 640 | 900 | 80 | top-left |
| solid | 1020 | 640 | 480 | 80 | top-left |
| solid | 1660 | 640 | 340 | 80 | top-left |
| oneWay | 1100 | 552 | 128 | 16 | top-left |
| thorn | 1350 | 624 | 48 | 16 | top-left |
| mosquito | 1450 | 570 | 24 | 20 | center, min_x=1380, max_x=1520, base_y=570 |
| dewdrop | 200 | 600 | 16 | 16 | center |
| dewdrop | 400 | 560 | 16 | 16 | center |
| dewdrop | 700 | 560 | 16 | 16 | center |
| dewdrop | 1160 | 508 | 16 | 16 | center |
| dewdrop | 1700 | 560 | 16 | 16 | center |

Level notes: first gap is 120 px, second gap is 160 px, one-way platform is optional for dewdrop, mosquito appears before final gap.

### Level 2: Lily Rush — Tier 1

| Field | Value |
| --- | --- |
| id | 2 |
| name | Lily Rush |
| width | 2400 |
| height | 720 |
| estimated time | 75-90 seconds |
| purpose | Introduce water, swimming, surface jumps, lily pad bounce |
| spawn center | 100, 626 |
| total dewdrops | 7 |
| checkpoint center | 1850, 624 |
| exit center | 2300, 608 |
| exit locked | false |
| boss | none |

| Entity | x | y | w | h | Extra |
| --- | ---: | ---: | ---: | ---: | --- |
| solid | 0 | 640 | 400 | 80 | top-left |
| solid | 900 | 640 | 300 | 80 | top-left |
| solid | 1800 | 640 | 600 | 80 | top-left |
| water | 400 | 560 | 500 | 160 | top-left |
| water | 1200 | 560 | 600 | 160 | top-left |
| lilyPad | 520 | 560 | 64 | 16 | top-left |
| lilyPad | 680 | 520 | 64 | 16 | top-left |
| lilyPad | 840 | 560 | 64 | 16 | top-left |
| lilyPad | 1280 | 560 | 64 | 16 | top-left |
| lilyPad | 1440 | 500 | 64 | 16 | top-left |
| lilyPad | 1600 | 560 | 64 | 16 | top-left |
| thorn | 1000 | 624 | 48 | 16 | top-left |
| dragonfly | 1500 | 460 | 28 | 16 | center, min_x=1300, max_x=1700, fixed y |
| dewdrop | 200 | 600 | 16 | 16 | center |
| dewdrop | 600 | 520 | 16 | 16 | center |
| dewdrop | 760 | 480 | 16 | 16 | center |
| dewdrop | 1000 | 560 | 16 | 16 | center |
| dewdrop | 1350 | 520 | 16 | 16 | center |
| dewdrop | 1550 | 460 | 16 | 16 | center |
| dewdrop | 2100 | 600 | 16 | 16 | center |

Level notes: first water, lily pads are intended crossing, falling into water is not lethal, dragonfly guards second water crossing.

### Level 3: Reed Hollow — Tier 1

| Field | Value |
| --- | --- |
| id | 3 |
| name | Reed Hollow |
| width | 1600 |
| height | 1280 |
| estimated time | 90-120 seconds |
| purpose | Introduce one-way platforms, vertical climbing, moving platforms |
| spawn center | 100, 1202 |
| total dewdrops | 12 |
| checkpoint center | 1314, 672 |
| exit center | 1264, 216 |
| exit locked | false |
| boss | none |

| Entity | x | y | w | h | Extra |
| --- | ---: | ---: | ---: | ---: | --- |
| solid | 0 | 1216 | 1600 | 64 | top-left |
| oneWay | 300 | 1128 | 128 | 16 | top-left |
| oneWay | 500 | 1040 | 128 | 16 | top-left |
| oneWay | 700 | 952 | 128 | 16 | top-left |
| oneWay | 900 | 864 | 128 | 16 | top-left |
| oneWay | 1250 | 688 | 128 | 16 | top-left |
| oneWay | 1050 | 600 | 128 | 16 | top-left |
| oneWay | 850 | 512 | 128 | 16 | top-left |
| oneWay | 650 | 424 | 128 | 16 | top-left |
| oneWay | 450 | 336 | 128 | 16 | top-left |
| oneWay | 1200 | 248 | 128 | 16 | top-left |
| lilyPad | 1100 | 776 | 64 | 16 | top-left |
| movingPlatform | 800 | 248 | 128 | 16 | top-left, axis=x, amplitude=240, period=4 |
| thorn | 200 | 1200 | 48 | 16 | top-left |
| mosquito | 800 | 820 | 24 | 20 | center, min_x=700, max_x=1000, base_y=820 |
| dewdrop | 200 | 1180 | 16 | 16 | center |
| dewdrop | 350 | 1090 | 16 | 16 | center |
| dewdrop | 550 | 1000 | 16 | 16 | center |
| dewdrop | 750 | 910 | 16 | 16 | center |
| dewdrop | 950 | 820 | 16 | 16 | center |
| dewdrop | 1150 | 730 | 16 | 16 | center |
| dewdrop | 1314 | 650 | 16 | 16 | center |
| dewdrop | 1100 | 560 | 16 | 16 | center |
| dewdrop | 900 | 470 | 16 | 16 | center |
| dewdrop | 700 | 380 | 16 | 16 | center |
| dewdrop | 500 | 290 | 16 | 16 | center |
| dewdrop | 800 | 210 | 16 | 16 | center |

Level notes: vertical level, one-way platforms and one lily pad, moving platform required to reach exit, checkpoint after first major climb.

### Level 4: Stormy Creek — Tier 1

| Field | Value |
| --- | --- |
| id | 4 |
| name | Stormy Creek |
| width | 2800 |
| height | 720 |
| estimated time | 120-150 seconds |
| purpose | Introduce currents, combine water/lily pads/hazards |
| spawn center | 100, 626 |
| total dewdrops | 11 |
| checkpoint center | 1500, 624 |
| exit center | 2700, 608 |
| exit locked | false |
| boss | none |

| Entity | x | y | w | h | Extra |
| --- | ---: | ---: | ---: | ---: | --- |
| solid | 0 | 640 | 300 | 80 | top-left |
| solid | 700 | 640 | 200 | 80 | top-left |
| solid | 1400 | 640 | 300 | 80 | top-left |
| solid | 2200 | 640 | 600 | 80 | top-left |
| water | 300 | 560 | 400 | 160 | top-left |
| water | 900 | 560 | 500 | 160 | top-left |
| water | 1700 | 560 | 500 | 160 | top-left |
| current | 300 | 560 | 400 | 160 | force=+120 |
| current | 900 | 560 | 500 | 160 | force=-120 |
| current | 1700 | 560 | 500 | 160 | force=+120 |
| lilyPad | 400 | 560 | 64 | 16 | top-left |
| lilyPad | 550 | 520 | 64 | 16 | top-left |
| lilyPad | 1000 | 560 | 64 | 16 | top-left |
| lilyPad | 1150 | 500 | 64 | 16 | top-left |
| lilyPad | 1300 | 560 | 64 | 16 | top-left |
| lilyPad | 1800 | 560 | 64 | 16 | top-left |
| lilyPad | 1950 | 520 | 64 | 16 | top-left |
| lilyPad | 2100 | 560 | 64 | 16 | top-left |
| thorn | 800 | 624 | 48 | 16 | top-left |
| thorn | 1600 | 624 | 48 | 16 | top-left |
| thorn | 2300 | 624 | 48 | 16 | top-left |
| dragonfly | 1100 | 460 | 28 | 16 | center, min_x=950, max_x=1350, fixed y |
| dragonfly | 1900 | 460 | 28 | 16 | center, min_x=1750, max_x=2150, fixed y |
| dewdrop | 200 | 600 | 16 | 16 | center |
| dewdrop | 450 | 520 | 16 | 16 | center |
| dewdrop | 600 | 480 | 16 | 16 | center |
| dewdrop | 850 | 600 | 16 | 16 | center |
| dewdrop | 1050 | 520 | 16 | 16 | center |
| dewdrop | 1200 | 460 | 16 | 16 | center |
| dewdrop | 1450 | 600 | 16 | 16 | center |
| dewdrop | 1850 | 520 | 16 | 16 | center |
| dewdrop | 2000 | 480 | 16 | 16 | center |
| dewdrop | 2400 | 600 | 16 | 16 | center |
| dewdrop | 2600 | 560 | 16 | 16 | center |

Level notes: first current pushes right, second pushes left, third pushes right, lily pads and timing are required, thorns punish careless landings.

### Level 5: Cliffside Ponds — Tier 1

| Field | Value |
| --- | --- |
| id | 5 |
| name | Cliffside Ponds |
| width | 2000 |
| height | 1280 |
| estimated time | 120-150 seconds |
| purpose | Combine vertical climbing, lily pad chains, moving platforms, enemies |
| spawn center | 100, 1202 |
| total dewdrops | 12 |
| checkpoint center | 1564, 496 |
| exit center | 1664, 216 |
| exit locked | false |
| boss | none |

| Entity | x | y | w | h | Extra |
| --- | ---: | ---: | ---: | ---: | --- |
| solid | 0 | 1216 | 2000 | 64 | top-left |
| oneWay | 200 | 1128 | 128 | 16 | top-left |
| oneWay | 400 | 1040 | 128 | 16 | top-left |
| oneWay | 600 | 952 | 128 | 16 | top-left |
| oneWay | 800 | 864 | 128 | 16 | top-left |
| oneWay | 1500 | 512 | 128 | 16 | top-left |
| oneWay | 1300 | 424 | 128 | 16 | top-left |
| oneWay | 1100 | 336 | 128 | 16 | top-left |
| oneWay | 900 | 248 | 128 | 16 | top-left |
| oneWay | 1600 | 248 | 128 | 16 | top-left |
| lilyPad | 1000 | 776 | 64 | 16 | top-left |
| lilyPad | 1150 | 688 | 64 | 16 | top-left |
| lilyPad | 1300 | 600 | 64 | 16 | top-left |
| movingPlatform | 1200 | 288 | 128 | 16 | top-left, axis=x, amplitude=160, period=4 |
| thorn | 500 | 1200 | 48 | 16 | top-left |
| thorn | 1400 | 1200 | 48 | 16 | top-left |
| mosquito | 700 | 820 | 24 | 20 | center, min_x=600, max_x=900, base_y=820 |
| dragonfly | 1200 | 300 | 28 | 16 | center, min_x=1000, max_x=1400, fixed y |
| dewdrop | 250 | 1090 | 16 | 16 | center |
| dewdrop | 450 | 1000 | 16 | 16 | center |
| dewdrop | 650 | 910 | 16 | 16 | center |
| dewdrop | 850 | 820 | 16 | 16 | center |
| dewdrop | 1032 | 740 | 16 | 16 | center |
| dewdrop | 1182 | 650 | 16 | 16 | center |
| dewdrop | 1332 | 560 | 16 | 16 | center |
| dewdrop | 1564 | 484 | 16 | 16 | center |
| dewdrop | 1364 | 380 | 16 | 16 | center |
| dewdrop | 1164 | 290 | 16 | 16 | center |
| dewdrop | 964 | 210 | 16 | 16 | center |
| dewdrop | 1300 | 250 | 16 | 16 | center |

Level notes: hardest platforming level, lily pad chain is intended route, moving platform required for final section, dragonfly guards upper route.

### Level 6: Great Waterfall — Tier 1

| Field | Value |
| --- | --- |
| id | 6 |
| name | Great Waterfall |
| width | 1280 |
| height | 720 |
| estimated time | 60-120 seconds |
| purpose | Final boss and ending |
| spawn center | 100, 626 |
| total dewdrops | 3 |
| checkpoint | none |
| exit center | 1200, 608 |
| exit locked | true |
| boss | Heron |

| Entity | x | y | w | h | Extra |
| --- | ---: | ---: | ---: | ---: | --- |
| solid | 0 | 640 | 1280 | 80 | top-left |
| boss | 640 | 600 | 56 | 80 | center, hp=6, min_x=100, max_x=1180 |
| dewdrop | 200 | 600 | 16 | 16 | center |
| dewdrop | 640 | 500 | 16 | 16 | center |
| dewdrop | 1080 | 600 | 16 | 16 | center |

Level notes: open arena, no hazards other than heron, exit visible but inactive until boss dies, dewdrops optional.

## 4.3 Game states — Tier 1

States:

| State | Meaning |
| --- | --- |
| `title` | Title screen |
| `controls` | Controls screen |
| `playing` | Normal gameplay, including death animation |
| `paused` | Pause menu |
| `levelComplete` | Level complete screen, levels 1-5 |
| `gameComplete` | Game complete screen after level 6 |

State rules:

| State | Rules |
| --- | --- |
| Title | Shown at boot. Options depend on save. Esc does nothing. |
| Controls | Shows controls. Esc returns to previous menu: title or pause. |
| Playing | Normal gameplay. Esc opens pause unless player is dead. |
| Paused | Shown only from Playing. Esc resumes. |
| Level Complete | Shown after levels 1-5. Enter/Space continues. Esc ignored. Pause disabled. |
| Game Complete | Shown after level 6. Enter/Space returns to title. Esc ignored. Pause disabled. |

Pause is disabled during:

- death animation
- level complete
- game complete
- title
- controls

## 4.4 Save system — Tier 1

Save shape:

```js
{
  unlocked_level: 1,
  completed: false
}
```

Rules:

- `unlocked_level` is clamped to 1 through 6.
- `completed` is boolean.
- No in-level progress is saved.
- No dewdrops are saved.
- No boss HP is saved.
- No checkpoint is saved.
- Invalid save data is treated as no save.
- Save on level complete.
- Save on quit to title.
- Save on game complete.
- Clear on New Game.
- Clear on Play Again.

## 4.5 Progression and difficulty — Tier 1

Level order:

| Level | Name | Difficulty | New idea |
| ---: | --- | --- | --- |
| 1 | Pond Edge | Very easy | Movement, jumping, stomping, objective |
| 2 | Lily Rush | Easy | Water, swimming, surface jumps, lily pads |
| 3 | Reed Hollow | Moderate | One-way platforms, verticality, moving platforms |
| 4 | Stormy Creek | Moderate | Currents |
| 5 | Cliffside Ponds | Hard | Combined mechanics, lily chain, moving platform |
| 6 | Great Waterfall | Boss | Heron boss |

Enemy counts:

| Level | Enemies |
| ---: | --- |
| 1 | 1 mosquito |
| 2 | 1 dragonfly |
| 3 | 1 mosquito |
| 4 | 2 dragonflies |
| 5 | 1 mosquito, 1 dragonfly |
| 6 | 1 heron |

There is no level select, no permanent upgrades, no power-ups, no score, no timer, no star ratings.

Level design principles:

| Rule | Value |
| --- | ---: |
| Max normal jump gap | 160 px |
| Max normal vertical step | 88 px |
| Lily pad bounce may cover larger vertical gaps | Yes |
| Hazard reaction time | At least 1 second |
| Checkpoints in safe locations | Yes |
| Dewdrops optional | Yes |
| No random enemy spawns | Yes |
| No hidden required paths | Yes |
| No level uses unseen mechanic as required difficulty | Yes |

## 4.6 Player hitbox — Tier 1

| Field | Value |
| --- | ---: |
| Width | 20 px |
| Height | 28 px |
| Position | Center-based |
| Rect | `x = player.x - 10`, `y = player.y - 14` |
| Bottom | `player.y + 14` |

Spawn examples:

| Ground top | Player center y |
| ---: | ---: |
| 640 | 626 |
| 1216 | 1202 |

## 4.7 Ground movement — Tier 1

| Context | Acceleration | Max speed | Friction |
| --- | ---: | ---: | ---: |
| On ground | 1800 px/s² | 240 px/s | 1600 px/s² |
| In air | 1200 px/s² | 240 px/s | 200 px/s² |
| In water | 700 px/s² | 160 px/s | 900 px/s² |

Horizontal algorithm:

```text
input = 0
if right pressed: input += 1
if left pressed: input -= 1

if input != 0:
    player.facing = input
    player.vx += input * acceleration * dt
    clamp player.vx to [-max_speed, max_speed]
else:
    apply friction toward 0 using context friction
```

## 4.8 Jumping — Tier 1

| Constant | Value |
| --- | ---: |
| Jump velocity | -520 px/s |
| Coyote time | 0.08 s |
| Jump buffer | 0.12 s |
| Variable jump cut factor | 0.45 |

Algorithm:

```text
if jump pressed:
    player.jumpBufferTimer = 0.12

if player.onGround or player.coyoteTimer > 0:
    if player.jumpBufferTimer > 0:
        if not player.inWater:
            player.vy = -520
            player.onGround = false
            player.coyoteTimer = 0
            player.jumpBufferTimer = 0
            player.jumpCutApplied = false
            player.jumpType = "land"

if jump released:
    if player.vy < 0:
        if not player.jumpCutApplied:
            if player.jumpType is "land" or "lily":
                player.vy *= 0.45
                player.jumpCutApplied = true
```

Coyote time:

- If player walks off a platform, they can still jump for 0.08 s.

Jump buffer:

- If player presses jump slightly before landing, the jump triggers on landing.

## 4.9 Water movement — Tier 1

Water is a movement space, not a hazard. The frog cannot drown.

| Constant | Value |
| --- | ---: |
| Water gravity | 350 px/s² |
| Water max fall speed | 220 px/s |
| Water max horizontal speed | 160 px/s |
| Water acceleration | 700 px/s² |
| Water friction | 900 px/s² |
| Surface jump velocity | -460 px/s |
| Swim upward acceleration | 900 px/s² |
| Swim upward max velocity | -220 px/s |
| Surface tolerance | 6 px |

Detection:

```text
in_water = player center is inside any water rectangle

on_surface =
    not in_water
    and player feet are within 6 px above water top
    and player horizontally overlaps water rectangle
```

Vertical movement:

```text
if in_water:
    if jump held:
        vy -= 900 * dt
        if vy < -220: vy = -220
    else:
        vy += 350 * dt
        if vy > 220: vy = 220

if on_surface and jump pressed:
    vy = -460
    jumpType = "surface"
```

Entering water:

```text
if player enters water and vy > 220:
    vy = 220
```

While in water:

- Vertical velocity clamped to [-220, 220].
- Horizontal velocity clamped to [-160, 160].
- Surface jumps are not cut by variable jump release.

## 4.10 Lily pad bounce — Tier 1

Lily pads are bouncy one-way platforms. The player cannot stand on a lily pad.

| Condition | Bounce velocity |
| --- | ---: |
| Jump not held | -620 px/s |
| Jump held | -680 px/s |

Algorithm:

```text
if player is falling:
    if previous bottom <= lily_pad_top + EPS:
        if new bottom >= lily_pad_top:
            if horizontal overlap:
                if jump held:
                    vy = -680
                else:
                    vy = -620
                onGround = false
                standingPlatformId = null
                jumpCutApplied = false
                jumpType = "lily"
```

`EPS` is 1 px.

## 4.11 Stomping — Tier 1

| Stomp type | Bounce velocity |
| --- | ---: |
| Normal enemy | -380 px/s |
| Boss | -420 px/s |

Stomp detection:

```text
if player overlaps enemy:
    if player is falling:
        if previous player bottom <= enemy top + 4:
            stomp enemy
```

Boss stomp uses top 12 px of boss hitbox.

Stomp rules:

- Stomping works while invulnerable.
- Stomping a normal enemy kills it.
- Stomping the boss reduces boss HP.
- Side or below contact damages the player.

## 4.12 Damage — Tier 1

| Constant | Value |
| --- | ---: |
| Player health | 3 hearts |
| Damage per hit | 1 heart |
| Invulnerability duration | 1.2 s |
| Horizontal knockback | 260 px/s away from source |
| Vertical knockback | -220 px/s |

Damage algorithm:

```text
if invulnerability_timer > 0:
    ignore damage

hearts -= 1
invulnTimer = 1.2

if source center x <= player center x:
    vx = 260
else:
    vx = -260

vy = -220

if hearts <= 0:
    start death
```

Invulnerability rules:

- Player cannot take damage while invulnerable.
- Stomp checks still work while invulnerable.
- Dewdrop collection still works while invulnerable.
- Checkpoint activation still works while invulnerable.

## 4.13 Death and respawn — Tier 1

Death causes:

- Hearts reach 0.
- Player center y > level_height + 100.

Death behavior:

1. Stop player input.
2. Play death animation for 0.6 s.
3. Respawn at last checkpoint or level spawn.
4. Refill hearts to 3.
5. Keep already collected dewdrops.
6. Reset enemies to initial positions.
7. Reset moving platforms to initial phase.
8. If boss is dead, keep boss dead and exit unlocked.

Respawn resets:

```text
player.x = level.respawn.x
player.y = level.respawn.y
player.vx = 0
player.vy = 0
player.hearts = 3
player.invulnTimer = 0
player.coyoteTimer = 0
player.jumpBufferTimer = 0
player.jumpCutApplied = false
player.jumpType = "none"
player.onGround = false
player.inWater = false
player.onSurface = false
player.standingPlatformId = null
player.dead = false
player.deathTimer = 0
level.time = 0
```

## 4.14 Solids — Tier 1

Solids are normal platforms. They block movement from all sides.

Used for:

- Ground
- Boss arena floor

Collision:

```text
horizontal:
    if moving right into solid:
        player.x = solid.x - PLAYER_W / 2
        player.vx = 0
    if moving left into solid:
        player.x = solid.x + solid.w + PLAYER_W / 2
        player.vx = 0

vertical:
    if falling into solid:
        player.y = solid.y - PLAYER_H / 2
        player.vy = 0
        player.onGround = true
    if rising into solid:
        player.y = solid.y + solid.h + PLAYER_H / 2
        player.vy = 0
```

## 4.15 One-way platforms — Tier 1

One-way platforms are thin platforms. They block only from below. The player can pass through them from below. The player cannot drop through them.

Landing condition:

```text
if player.vy >= 0:
    if previousBottom <= platform.y + EPS:
        if newBottom >= platform.y:
            if horizontal overlap:
                land on platform
```

`EPS` is 1 px.

Landing:

```text
player.y = platform.y - PLAYER_H / 2
player.vy = 0
player.onGround = true
player.standingPlatformId = platform.id
```

## 4.16 Moving platforms — Tier 1

Moving platforms are one-way platforms that move on a sine path and carry the player.

Data:

- start position
- width
- height
- axis: x or y
- amplitude
- period

Position algorithm:

```text
offset = amplitude * sin(2 * PI * level.time / period)

if axis == x:
    x = start_x + offset
    y = start_y
else:
    x = start_x
    y = start_y + offset
```

Carry algorithm:

```text
delta = current_position - previous_position

if player.standingPlatformId == platform.id:
    player.x += delta.x
    player.y += delta.y
```

Rules:

- Moving platforms carry the player before input is applied.
- If the player is not standing on the platform, no carry is applied.
- If the platform moves away, the player falls normally.
- If the player dies, moving platforms reset by resetting `level.time = 0`.

## 4.17 Water currents — Tier 1

Currents are water zones that apply horizontal force.

| Constant | Value |
| --- | ---: |
| Force magnitude | 120 px/s² |
| Direction | Left or right |

Algorithm:

```text
if player center is inside current rectangle:
    vx += current_force * dt
    clamp vx to water max speed [-160, 160]
```

Current force sets tutorial flag `firstCurrentForce`.

## 4.18 Dewdrops — Tier 1

Dewdrop hitbox:

| Field | Value |
| --- | ---: |
| Width | 16 px |
| Height | 16 px |
| Coordinates | Center-based |

Behavior:

- Touching a dewdrop collects it.
- Collected dewdrops remain collected after respawn.
- Restarting the level resets dewdrops.
- Dewdrops do not affect progression.
- Collection works while invulnerable.

HUD displays:

- Current collected count
- Total count for current level
- Format: `x / y`

## 4.19 Checkpoints — Tier 1

Checkpoint hitbox:

| Field | Value |
| --- | ---: |
| Width | 32 px |
| Height | 32 px |
| Coordinates | Center-based |

Behavior:

- Touching a checkpoint sets the respawn point.
- Touching a checkpoint refills hearts to 3.
- Shows “Checkpoint” message for 1.5 s.
- Works while invulnerable.
- Repeated touch refills hearts if below 3.
- Does not reset enemies, moving platforms, or dewdrops.

Activation:

```text
if player overlaps checkpoint:
    if not checkpoint.activated:
        checkpoint.activated = true
        level.respawn.x = checkpoint.x
        level.respawn.y = checkpoint.y
        player.hearts = 3
        show message "Checkpoint"
        play audio checkpoint
    else:
        if player.hearts < 3:
            player.hearts = 3
```

## 4.20 Exits — Tier 1

Exit hitbox:

| Field | Value |
| --- | ---: |
| Width | 48 px |
| Height | 64 px |
| Coordinates | Center-based |

Behavior:

- Touching an active exit completes the level.
- In Level 6, the exit is locked until the boss is defeated.

Active rule:

```text
exit.active = exit.locked ? bossDead : true
```

Completion:

- Levels 1-5: state becomes `levelComplete`.
- Level 6: state becomes `gameComplete`.

## 4.21 Enemies — Tier 1

### Mosquito

| Field | Value |
| --- | ---: |
| Hitbox | 24 x 20 px |
| Patrol speed | 80 px/s |
| Vertical sine amplitude | 24 px |
| Vertical sine period | 1.6 s |
| Stompable | Yes |

Algorithm:

```text
if x < min_x or x > max_x:
    direction *= -1

x += direction * 80 * dt
y = base_y + 24 * sin(2 * PI * level.time / 1.6)
clamp x to [min_x, max_x]
```

### Dragonfly

| Field | Value |
| --- | ---: |
| Hitbox | 28 x 16 px |
| Patrol speed | 180 px/s |
| Y | Fixed |
| Stompable | Yes |

Algorithm:

```text
if x < min_x or x > max_x:
    direction *= -1

x += direction * 180 * dt
clamp x to [min_x, max_x]
```

### Thorn

| Field | Value |
| --- | ---: |
| Hitbox | 48 x 16 px |
| Stompable | No |
| Movement | None |

Touch damages player.

### Player-enemy collision order

Each frame:

1. Update enemies.
2. Find all living enemies overlapping player.
3. Process stomps first.
4. If any stomp applies:
   - Apply stomp bounce.
   - Do not apply damage.
5. If no stomp applies:
   - Apply exactly one damage instance from the first damaging enemy or thorn.

Multiple hazards:

- If player overlaps multiple enemies, process stomps first.
- If no stomp applies, apply one damage instance only.
- If player touches thorn and enemy at same time, stomp checks happen first; if no stomp applies, one damage instance only.

## 4.22 Boss: Heron — Tier 1

Boss hitbox:

| Field | Value |
| --- | ---: |
| Width | 56 px |
| Height | 80 px |
| HP | 6 |
| Spawn center | 640, 600 |
| Ground top | 640 |
| Arena min x | 100 |
| Arena max x | 1180 |

Boss states:

| State | Meaning |
| --- | --- |
| `idle` | Faces player, waits |
| `lunge` | Moves toward player |
| `recover` | Stops and recovers |
| `dead` | Defeated |

Phases:

| Phase | HP | Idle | Lunge | Recover | Lunge speed |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 6, 5, 4 | 1.2 s | 0.4 s | 0.8 s | 320 px/s |
| 2 | 3, 2, 1 | 0.8 s | 0.4 s | 0.6 s | 380 px/s |

Boss algorithm:

```text
if state == idle:
    direction = sign(player_x - boss_x)
    timer -= dt
    if timer <= 0:
        state = lunge
        timer = 0.4

if state == lunge:
    boss.x += direction * lunge_speed * dt
    timer -= dt
    if timer <= 0:
        state = recover
        timer = recover_time

if state == recover:
    timer -= dt
    if timer <= 0:
        state = idle
        timer = idle_time

clamp boss.x to [100, 1180]
boss.y = ground_top - boss_height / 2
```

Boss stomp zone:

- Top 12 px of boss hitbox.

Boss stomp algorithm:

```text
if player is falling:
    if previous player bottom <= heron_top + 12:
        if horizontal overlap:
            heron HP -= 1
            player vy = -420
            player onGround = false
            player jumpCutApplied = false
            if heron HP <= 0:
                heron state = dead
                heron alive = false
                unlock exit
```

Boss side/bottom contact:

- If player overlaps boss and no stomp applies, player takes damage.
- If boss is dead, it does not damage the player.

Boss persistence:

- If boss is dead and player dies, boss remains dead and exit remains unlocked.
- If player restarts level, boss resets to alive and exit locks again.

## 4.23 Collision and update order — Tier 1

Update order:

1. Add moving platform delta to player if standing on one.
2. Apply horizontal input.
3. Apply water and current forces.
4. Apply vertical gravity or swimming.
5. Move player horizontally and resolve solid collisions and level bounds.
6. Move player vertically and resolve:
   - solids
   - level bounds
   - one-way platforms
   - lily pads
7. Update enemies.
8. Check player-enemy collisions.
9. Check dewdrop collection.
10. Check checkpoint touch.
11. Check exit touch.
12. Update timers and HUD.

Stomp checks use the player’s bottom position from before vertical movement.

Level bounds:

- Left wall at x = 0.
- Right wall at x = level_width.
- Ceiling at y = 0.
- Death below y = level_height + 100.

Player cannot leave level from sides or top.

## 4.24 HUD — Tier 1

There is no timer, score, minimap, or objective arrow.

### Health section

| Field | Value |
| --- | ---: |
| Location | Top-left |
| Offset | 16 px from left, 16 px from top |
| Icons | 3 hearts |
| Icon size | 32 x 32 px |
| Spacing | 8 px |

Display:

- Full heart = current health.
- Empty heart = lost health.
- Updates immediately on damage.
- Refills at checkpoints and respawn.

### Dewdrop section

| Field | Value |
| --- | ---: |
| Location | Top-right |
| Offset | 16 px from right, 16 px from top |
| Icon size | 24 x 24 px |
| Text size | 18 px |
| Format | `x / y` |

Display:

- `x` = dewdrops collected in current level.
- `y` = total dewdrops in current level.
- Updates immediately on collection.
- Persists through respawn.
- Resets on level restart.

### Message section

| Field | Value |
| --- | ---: |
| Location | Top-center |
| Offset | 48 px below top edge |
| Max width | 600 px |
| Min width | 220 px |
| Height | 48 px |
| Center x | 640 |

Message priority:

1. Checkpoint
2. Tutorial prompt
3. Level name

Level Complete is a screen, not an HUD message.

Message durations:

| Message | Duration |
| --- | ---: |
| Level name | 2.5 s |
| Checkpoint | 1.5 s |
| Tutorial prompt | Until condition met or 5 s after shown |

## 4.25 Tutorial prompts — Tier 1

Tutorial prompts appear in the message section. They do not affect gameplay.

Event flags:

```js
{
  firstHorizontalInput: false,
  firstJump: false,
  firstStomp: false,
  firstWaterJumpOrSwim: false,
  firstLilyBounce: false,
  firstOneWayLanding: false,
  firstMovingPlatformRide: false,
  firstCurrentForce: false,
  firstBossStomp: false
}
```

Prompt table:

| Level | Prompt id | Text | Show condition | Hide condition |
| ---: | --- | --- | --- | --- |
| 1 | `move` | Move with A/D or Left/Right | At spawn | `firstHorizontalInput` |
| 1 | `jump` | Jump with Space | player x >= 300 | `firstJump` |
| 1 | `stomp` | Land on enemies to stomp them | player x >= 1350 | `firstStomp` or player x >= 1500 |
| 1 | `waterfall` | Reach the waterfall | player x >= 1750 | After 5 seconds |
| 2 | `swim` | Hold Jump to swim | player x >= 350 | `firstWaterJumpOrSwim` |
| 2 | `lily` | Lily pads bounce | player x >= 500 | `firstLilyBounce` |
| 3 | `oneway` | Leaves are one-way platforms | player x >= 250 | `firstOneWayLanding` |
| 3 | `moving` | Moving leaves carry you | player x >= 750 and player y <= 400 | `firstMovingPlatformRide` |
| 4 | `current` | Currents push you | player x >= 280 | `firstCurrentForce` |
| 5 | `chain` | Chain lily pads to climb | player x >= 950 | `firstLilyBounce` |
| 6 | `boss` | Stomp the heron’s head | At level start | `firstBossStomp` |

Active tutorial prompt is the first prompt in level order whose show condition is true and whose hide condition is not met.

## 4.26 Camera — Tier 1

Camera follows player, clamps to level bounds, uses deadzone and lookahead, and smooths.

| Constant | Value |
| --- | ---: |
| Deadzone X | 200 px |
| Deadzone Y | 120 px |
| Lookahead | 40 px |
| Smoothing | 10 |

Algorithm:

```text
halfW = 640
halfH = 360

playerLookX = player.x + (player.facing > 0 ? 40 : -40)
playerLookY = player.y

cameraCenterX = camera.x + halfW
cameraCenterY = camera.y + halfH

desiredX = camera.x
desiredY = camera.y

if playerLookX > cameraCenterX + 200:
    desiredX = playerLookX - (halfW - 200)
else if playerLookX < cameraCenterX - 200:
    desiredX = playerLookX + (halfW - 200)

if playerLookY > cameraCenterY + 120:
    desiredY = playerLookY - (halfH - 120)
else if playerLookY < cameraCenterY - 120:
    desiredY = playerLookY + (halfH - 120)

camera.x += (desiredX - camera.x) * min(1, dt * 10)
camera.y += (desiredY - camera.y) * min(1, dt * 10)

clamp camera.x to [0, level.width - 1280]
clamp camera.y to [0, level.height - 720]
```

If level is smaller than viewport, clamp camera to 0 on that axis.

Camera is visual only. Logic must not depend on camera.

## 4.27 Level complete screen — Tier 1

Shown after levels 1-5.

Content:

```text
LEVEL COMPLETE

[Level Name]

Dewdrops: x / y

Press Enter or Space to continue
```

If `x == y`:

```text
Perfect!
```

Continuing starts the next level.

## 4.28 Game complete screen — Tier 1

Shown after Level 6.

Content:

```text
THE FROG REACHED THE GREAT WATERFALL.

The pond is now a small dot in a big sky.

Press Enter or Space to return to title
```

## 4.29 Title screen — Tier 1

Content:

```text
FROG: POND TO PEAK

A small jump to the waterfall
```

Options:

| Save state | Options |
| --- | --- |
| No save | New Game, Controls |
| Save exists and not completed | Continue, New Game, Controls |
| Game complete | Play Again, New Game, Controls |

New Game confirmation, only if save exists:

```text
Start over?

Yes
No
```

## 4.30 Controls screen — Tier 1

Content:

```text
CONTROLS

Move: A / D or Left / Right
Jump / Swim: Space / W / Up
Pause: Esc

Menus:
Move: W / S or Up / Down
Confirm: Enter or Space
Back: Esc

Press Esc to go back
```

## 4.31 Pause menu — Tier 1

Content:

```text
PAUSED

Resume
Restart Level
Controls
Quit to Title
```

Rules:

- Resume returns to current level state.
- Restart Level resets the entire level.
- Controls opens Controls screen; returning goes back to Pause.
- Quit to Title saves current unlocked level and returns to title.

## 4.32 Feel targets — Tier 1

The game should feel:

- Responsive
- Small
- Bouncy
- Forgiving
- Readable

Specific targets:

- Frog stops quickly on ground.
- Frog adjusts in air.
- Jumps feel short and punchy.
- Lily pads feel like a reward for landing.
- Water feels dense but controllable.
- Enemies are readable before becoming dangerous.
- Checkpoints feel like a relief.
- Boss feels like a pattern to dodge, not a precision test.

## 4.33 Edge cases — Tier 1

| Case | Rule |
| --- | --- |
| No save | Title shows New Game and Controls only. |
| Completed save | Title shows Play Again, New Game, Controls. |
| Player falls below level | If player center y > level_height + 100, death triggers and respawn occurs. |
| Player falls into water | No death, no fall damage, vy capped at 220 px/s, water physics apply. |
| Player touches enemy while invulnerable | Damage ignored, stomp checks still work. |
| Player touches multiple enemies | Process stomps first; if no stomp applies, apply one damage instance only. |
| Player touches thorn and enemy | Stomp checks first; if no stomp applies, one damage instance only. |
| Player lands on lily pad holding jump | Bounce velocity is -680 px/s. |
| Player lands on lily pad not holding jump | Bounce velocity is -620 px/s. |
| Player bounces into ceiling | vy becomes 0, player falls normally. |
| Player bounces into water | Water physics apply, vy capped at 220 px/s. |
| Current pushes player into thorn | Player takes damage, knockback applies, may be knocked into water. |
| Player dies on moving platform | Respawn at checkpoint/spawn, moving platforms reset to initial phase. |
| Player dies after boss defeated | Respawn at level spawn, boss remains dead, exit remains unlocked. |
| Player restarts level from pause | Level resets completely, dewdrops reset, enemies reset, moving platforms reset, boss resets if present, player respawns at spawn, hearts refill. |
| Player quits to title | Save current unlocked level, do not save in-level progress, dewdrops, or boss HP. |
| Player reaches exit while boss alive | Level 6 exit does nothing. |
| Player touches checkpoint while invulnerable | Checkpoint activates, hearts refill, respawn point updates. |
| Player collects dewdrop while invulnerable | Dewdrop collects normally. |
| Player pauses during death | Pause disabled. |
| Player pauses during level complete | Pause disabled. |

# 5. CHARACTERS

## 5.1 Player frog — Tier 2 visual, Tier 1 state visibility

Silhouette:

- Small bright green frog.
- Clear left/right facing.
- Eyes and body orientation indicate facing.
- Mirror sprite for left/right.
- In water, facing follows horizontal input.
- During invulnerability, frog blinks but still faces last movement direction.

Visual bounds:

| Field | Value |
| --- | ---: |
| Visual size | 32 x 32 px |
| Hitbox | 20 x 28 px |
| Horizontal alignment | Center frog visual on player center X |
| Vertical alignment | Align frog visual bottom to player hitbox bottom |

Palette:

| Part | Color |
| --- | ---: |
| Body | `#59C94C` |
| Light body | `#8FE76B` |
| Belly | `#EAF9D8` |
| Outline | `#1B2A1F` |
| Eye white | `#FFFFFF` |
| Pupil | `#111111` |
| Hurt tint | `#FF5A5A` |
| Death tint | `#8A9A92` |

Animation states:

| State | Visual | Motion rule | Gameplay trigger | Tier |
| --- | --- | --- | --- | --- |
| Idle | Slight breathing | 2 frames, 12 fps | No horizontal input, on ground | Tier 2 |
| Run | 4-frame leg cycle, body leans forward | 4 frames, 12 fps | Horizontal input on ground | Tier 2 |
| Jump | Legs tucked, eyes slightly up | 1 frame | `vy < 0` after land jump | Tier 2 |
| Fall | Legs splayed | 1 frame | `vy > 0` and not on ground | Tier 2 |
| Swim | Body more horizontal, legs kick | 2 frames, 8 fps | `inWater` true | Tier 2 |
| Surface jump | Small crouch before leaving water | 1 frame + ripple | `onSurface` and jump pressed | Tier 2 |
| Lily bounce | Squash on pad, then stretch upward | Squash 2 frames, ring effect | Lily pad bounce | Tier 2 |
| Stomp | Feet down, eyes focused | 1 frame | Stomp bounce | Tier 2 |
| Hurt | Red tint, eyes squeezed | 1 frame | Damage taken | Tier 2 |
| Invulnerable | Blink full opacity and 35% opacity | 8 toggles/sec | `invulnTimer > 0` | Tier 1/2 |
| Death | Gray tint, X eyes, deflate/fall over | 2 frames, 10 fps, 0.6 s | `dead` true | Tier 1/2 |

Player feedback effects, Tier 2:

| Event | Visual |
| --- | --- |
| Run on ground | Small dust puffs every 0.15 s |
| Jump | Small dust puff or water splash if near water |
| Land on ground | Small dust puff |
| Enter water | Splash ring and droplets |
| Swim | Small bubbles |
| Lily pad bounce | Green bounce ring and pad squash |
| Stomp | Puff and enemy squish |
| Damage | Red flash on frog for 2 frames |
| Checkpoint | Hearts refill with pulse |

## 5.2 Mosquito — Tier 2 visual, Tier 1 behavior

Silhouette:

- Small dark indigo flying bug.
- Thin legs.
- Fast wing flap.
- Small red eyes.
- Clear top surface for stomping.

Visual bounds:

| Field | Value |
| --- | ---: |
| Visual size | 32 x 28 px |
| Hitbox | 24 x 20 px |
| Alignment | Centered on hitbox center |

Palette:

| Part | Color |
| --- | ---: |
| Body | `#5A5F7A` |
| Wing | `#C9D9FF` |
| Eye | `#FF5A5A` |
| Outline | `#1B2A1F` |

Animation:

| State | Motion rule |
| --- | --- |
| Patrol | Wings 2 frames, 20 fps; small body sine bob |
| Stomp | Squash, 4 small particles, fade 0.20 s |

## 5.3 Dragonfly — Tier 2 visual, Tier 1 behavior

Silhouette:

- Long cyan body.
- Two pairs of wings.
- Faster wing flap than mosquito.
- Slight motion streak when moving fast.

Visual bounds:

| Field | Value |
| --- | ---: |
| Visual size | 32 x 24 px |
| Hitbox | 28 x 16 px |
| Alignment | Centered on hitbox center |

Palette:

| Part | Color |
| --- | ---: |
| Body | `#2FA8C8` |
| Light body | `#4FD8D8` |
| Wing | `#DFFBFF` |
| Eye | `#FF5A5A` |
| Outline | `#1B2A1F` |

Animation:

| State | Motion rule |
| --- | --- |
| Patrol | Wings 2 frames, 24 fps; 2 px motion streak alpha 0.25 |
| Stomp | Squash sideways, wings flutter, 4 particles, fade 0.20 s |

## 5.4 Heron boss — Tier 2 visual, Tier 1 behavior

Silhouette:

- Tall slate-gray bird.
- Long neck.
- Long beak.
- Large readable head.
- Soft feather shapes.
- Red eye.
- Clear head target.

Visual bounds:

| Field | Value |
| --- | ---: |
| Visual size | 64 x 80 px |
| Hitbox | 56 x 80 px |
| Alignment | Bottom aligned to hitbox bottom, horizontally centered |

Palette:

| Part | Color |
| --- | ---: |
| Body | `#8A93A8` |
| Light feather | `#C0C8D8` |
| Dark feather | `#4A5268` |
| Beak | `#E8A33F` |
| Eye | `#FF5A5A` |
| Stomp band | `#BFF6FF` |
| Phase 2 accent | `#FFC24A` |

Stomp zone visual:

| Field | Value |
| --- | ---: |
| Band height | 12 px |
| Band width | 40 px |
| Band color | `#BFF6FF` |
| Band alpha | 0.80 |
| Hit flash | White for 2 frames |

Boss states:

| State | Visual | Motion rule | Tier |
| --- | --- | --- | --- |
| Idle | Neck up, slight breathing, blink every 2.5 s | 2 frames, 6 fps | Tier 2 |
| Lunge | Leans forward, beak extends slightly, eyes focused | 2 frames, 12 fps | Tier 2 |
| Recover | Neck retracts, body wobbles slightly | 1 frame instant | Tier 2 |
| Dead | Lies down, eyes closed, feathers puff, no movement | 2 frames, 8 fps | Tier 2 |

Boss HP visual:

| Field | Value |
| --- | ---: |
| Droplet count | 6 |
| Droplet size | 12 x 12 px |
| Spacing | 4 px |
| Position | Centered above heron head |
| Remaining HP | Bright cyan droplets |
| Lost HP | Droplet fades and disappears |
| Phase 2 HP | Amber `#FFC24A` when HP 3 or less |

Phase 2 visual:

- Feathers slightly ruffled.
- Eye stays red.
- Stomp band remains cyan.
- HP droplets turn amber.
- Idle animation slightly faster.

Boss death visual:

1. Heron flashes white for 2 frames.
2. HP droplets vanish.
3. Heron deflates.
4. Feathers puff outward.
5. Heron lies down.
6. Exit activates.

Duration: 0.60 s.

# 6. AUDIO

Audio uses browser WebAudio. No external audio files are required. Tier 1 records events silently. Tier 2 plays synthesized SFX. Tier 3 plays synthesized music and ambience.

Audio rules:

- Audio must not block boot.
- Missing audio must fail silently.
- Audio unlocks on first user gesture.
- In tests, audio may be disabled.
- `play(event)` records `lastEvent` even if audio is disabled or synthesis is unavailable.
- No harsh distortion.
- Water sounds are soft.
- Boss sounds are larger than normal enemy sounds.
- UI sounds are quiet.

SFX table:

| Name | Recipe | When it plays | Tier |
| --- | --- | --- | ---: |
| `jump` | Triangle 320 Hz to 640 Hz, lowpass 2 kHz, 0.08 s | Ground jump | 2 |
| `water_splash` | Filtered noise 800 Hz to 300 Hz + sine 600 Hz to 200 Hz, 0.15 s | Entering water or surface jump | 2 |
| `lily_pad_bounce` | Sine 220 Hz to 520 Hz, slight vibrato, 0.12 s | Lily pad bounce | 2 |
| `stomp` | Noise lowpass 400 Hz + sine 100 Hz, 0.10 s | Normal enemy stomp | 2 |
| `damage` | Square 420 Hz to 140 Hz, slight distortion, 0.15 s | Player takes damage | 2 |
| `player_death` | Triangle 300 Hz to 80 Hz, lowpass, 0.30 s | Player death starts | 2 |
| `checkpoint` | Sine C5 then G5, 0.25 s | Checkpoint first activation | 2 |
| `dewdrop` | Sine 1320 Hz + 1760 Hz, 0.05 s | Dewdrop collected | 2 |
| `level_complete` | Triangle C5 - E5 - G5, 0.50 s | Levels 1-5 complete | 2 |
| `perfect` | High sine arpeggio C6 - E6 - G6, 0.40 s | Level complete with all dewdrops | 2 |
| `boss_lunge` | Filtered noise sweep 300 Hz to 1200 Hz, 0.15 s | Boss enters lunge | 2 |
| `boss_hit` | Sine 80 Hz + short noise burst, 0.15 s | Boss HP decreases but remains above 0 | 2 |
| `boss_death` | Noise splash + sine C4, 0.60 s | Boss HP reaches 0 | 2 |
| `exit_activation` | Filtered noise + rising sine, 0.30 s | Locked exit becomes active | 2 |
| `menu_select` | Sine 880 Hz, 0.03 s | Menu selection changes or confirmed | 2 |
| `menu_back` | Sine 587 Hz, 0.03 s | Esc/back in menu | 2 |
| `pause` | Sine 440 Hz, 0.05 s | Pause opens or closes | 2 |
| `game_complete` | C4 - E4 - G4 - C5 chord, slow attack, 1.00 s | Level 6 complete | 2 |

Event mapping:

| Gameplay event | Audio name |
| --- | --- |
| Ground jump | `jump` |
| Enter water | `water_splash` |
| Surface jump | `water_splash` |
| Lily pad bounce | `lily_pad_bounce` |
| Normal enemy stomp | `stomp` |
| Player damage | `damage` |
| Player death | `player_death` |
| Checkpoint activation | `checkpoint` |
| Dewdrop collect | `dewdrop` |
| Level complete | `level_complete` |
| Perfect level complete | `perfect` |
| Boss lunge | `boss_lunge` |
| Boss hit | `boss_hit` |
| Boss death | `boss_death` |
| Exit activation | `exit_activation` |
| Game complete | `game_complete` |
| Menu select | `menu_select` |
| Menu back | `menu_back` |
| Pause | `pause` |

Music and ambience, Tier 3:

| Music state | Tempo | Scale | Mood | Motif / recipe | When |
| --- | ---: | --- | --- | --- | --- |
| Title music | 90 BPM | A minor pentatonic | Calm, curious | `E4 - G4 - A4 - C5 - A4 - G4 - E4 - D4` | Title screen |
| Controls/Pause | Current music at -6 dB | Current | Quieter | Use current music or title music at -6 dB | Controls or pause |
| Level 1 music | 100 BPM | C major pentatonic | Bright, easy | `C4 - D4 - E4 - G4 - E4 - D4 - C4 - D4` | Level 1 |
| Level 2 music | 110 BPM | C major | Bouncy, playful | `C4 - E4 - G4 - C5 - G4 - E4 - C4 - D4` | Level 2 |
| Level 3 music | 96 BPM | A minor | Quiet, vertical | `A4 - C5 - E5 - C5 - A4 - G4 - A4 - E4` | Level 3 |
| Level 4 music | 104 BPM | D minor | Tense but safe | `D4 - F4 - A4 - C5 - A4 - F4 - D4 - F4` | Level 4 |
| Level 5 music | 112 BPM | E minor | Rising, adventurous | `E4 - G4 - B4 - E5 - B4 - G4 - E4 - G4` | Level 5 |
| Level 6 music | 100 BPM | C major | Grand, final | `C4 - E4 - G4 - C5 - G4 - E4 - C4 - D4` | Level 6 before boss |
| Boss music | 120 BPM | C minor / C major resolution | Urgent but not scary | `C4 - Eb4 - G4 - C5 - G4 - Eb4 - C4 - Eb4` | Heron active |
| Boss phase 2 | 120 BPM | C minor / C major resolution | More urgent | Add high woodblock ticks, increase pulse | Boss HP 3 or less |
| Boss death resolve | — | C major | Resolved | `C4 - E4 - G4 - C5` | Heron dies |
| Game complete music | 60 BPM | C major | Warm, resolved | `C4 - E4 - G4 - C5` | Game complete screen |

Ambience:

| Level / State | Ambience |
| --- | --- |
| Title | Soft water, distant birds |
| Level 1 | Light water, soft wind |
| Level 2 | Water ripples, lily pad splashes |
| Level 3 | Misty water, soft reed rustle |
| Level 4 | Rain, wind, moving water |
| Level 5 | Twilight wind, distant water |
| Level 6 | Waterfall, mist, soft rocks |

Ambience rules:

- Keep ambience low.
- Do not let rain hide SFX.
- Do not let waterfall hide boss audio.
- No thunder.
- No lightning crack.

# 7. UX

HTML and CSS only for HUD and menus. Canvas is used for the game world.

Required HTML structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>FROG: POND TO PEAK</title>
  <link rel="stylesheet" href="css/style.css" />
</head>
<body>
  <div id="game">
    <canvas id="canvas" width="1280" height="720"></canvas>

    <div id="hud" class="hidden">
      <div id="hearts" class="hud-section hearts"></div>
      <div id="dewdrops" class="hud-section dewdrops"></div>
      <div id="message" class="hud-section message"></div>
    </div>

    <div id="ui">
      <div id="screen-title" class="screen hidden"></div>
      <div id="screen-controls" class="screen hidden"></div>
      <div id="screen-pause" class="screen hidden"></div>
      <div id="screen-level-complete" class="screen hidden"></div>
      <div id="screen-game-complete" class="screen hidden"></div>
    </div>
  </div>

  <!-- scripts -->
</body>
</html>
```

`test.html` uses the same `#game` structure and adds:

```html
<pre id="test-results"></pre>
```

Required CSS anchors:

| Selector | Required behavior |
| --- | --- |
| `#game` | Maintains 16:9 aspect ratio, centered, scales to fit window |
| `#canvas` | 1280 x 720 logical pixels |
| `#hud` | Absolutely positioned over canvas |
| `#hearts` | Top-left, 16 px from left/top |
| `#dewdrops` | Top-right, 16 px from right/top |
| `#message` | Top-center, 48 px below top edge, max width 600 px |
| `#ui` | Absolutely positioned over canvas |
| `.screen` | Screen container |
| `.hidden` | Hidden element |
| `.menu-item` | Menu option |
| `.menu-item.selected` | Selected menu option |
| `.confirm` | Confirmation panel |
| `.heart` | Heart icon |
| `.heart.full` | Full heart |
| `.heart.empty` | Empty heart |
| `.dewdrop-icon` | Dewdrop HUD icon |

Screen state machine:

| From | Input / action | To | Side effects |
| --- | --- | --- | --- |
| Title | New Game, no save | Playing | Clear save, load Level 1 |
| Title | New Game, save exists | Title confirm | Show Start over? |
| Title confirm | Yes | Playing | Clear save, load Level 1 |
| Title confirm | No | Title | Cancel confirmation |
| Title | Continue | Playing | Load `save.unlocked_level` |
| Title | Play Again | Playing | Clear save, load Level 1 |
| Title | Controls | Controls | Open controls |
| Controls | Esc | Previous menu | Title or Pause |
| Playing | Esc, not dead | Paused | Open pause |
| Paused | Resume / Esc | Playing | Resume level |
| Paused | Restart Level | Playing | Reset current level |
| Paused | Controls | Controls | Return to Pause after Esc |
| Paused | Quit to Title | Title | Save current unlocked level |
| Playing | Touch active exit, levels 1-5 | Level Complete | Save next unlocked level |
| Level Complete | Enter/Space | Playing | Load next level |
| Playing | Touch active exit, Level 6 | Game Complete | Save completed true |
| Game Complete | Enter/Space | Title | Return to title |

HUD table:

| Element | Record field | When visible |
| --- | --- | --- |
| `#hud` | `gameState` | Visible during `playing` and `paused`; dimmed during pause/death; hidden otherwise |
| `#hearts` | `player.hearts` | Visible during `playing` and `paused` |
| `#dewdrops` | `dewdrops.collected`, `dewdrops.total` | Visible during `playing` and `paused` |
| `#message` | `message.text`, `message.remaining` | Visible when a message is active during `playing` or `paused` |
| `#screen-title` | `title.options`, `title.selectedIndex`, `title.confirm` | Visible when `gameState === "title"` |
| `#screen-controls` | Static controls text | Visible when `gameState === "controls"` |
| `#screen-pause` | Static pause options | Visible when `gameState === "paused"` |
| `#screen-level-complete` | `levelComplete.levelName`, `levelComplete.dewdropsCollected`, `levelComplete.dewdropsTotal`, `levelComplete.perfect`, `levelComplete.nextLevel` | Visible when `gameState === "levelComplete"` |
| `#screen-game-complete` | `gameComplete.completed` | Visible when `gameState === "gameComplete"` |

HUD state rules:

| Game state | HUD behavior |
| --- | --- |
| Playing | Visible |
| Paused | Dimmed behind pause overlay |
| Death | Visible, dimmed slightly |
| Level Complete | Hidden |
| Game Complete | Hidden |
| Title | Hidden |
| Controls | Hidden |

# 8. DEBUG API

`window.__game` is created after boot.

```js
window.__game = {
  version: "1.0.0",

  start: function (opts) {},
  reset: function (opts) {},
  step: function (frames, opts) {},
  until: function (predicate, maxFrames) {},
  getState: function () {},

  input: {
    setLeft: function (down) {},
    setRight: function (down) {},
    setJump: function (down) {},
    pressJump: function (holdFrames) {},
    setMenu: function (key, down) {},
    pressMenu: function (key) {}
  },

  actions: {
    startNewGame: function () {},
    continueGame: function () {},
    playAgain: function () {},
    selectTitleOption: function (index) {},
    moveMenu: function (dir) {},
    pressEnter: function () {},
    pressEsc: function () {},

    pause: function () {},
    resume: function () {},
    restartLevel: function () {},
    quitToTitle: function () {},

    loadLevel: function (index) {},
    loadTestLevel: function (spec) {},
    validateLevel: function (data) {},
    setSave: function (save) {},

    collectDewdrop: function (index) {},
    setDewdropCollected: function (index, collected) {},

    killEnemy: function (idOrIndex) {},
    setEnemyPosition: function (idOrIndex, x, y) {},
    setEnemyAlive: function (idOrIndex, alive) {},
    setEnemyDirection: function (idOrIndex, direction) {},

    setBossHp: function (hp) {},
    setBossState: function (state) {},
    setBossPosition: function (x, y) {},

    unlockExit: function (active) {},

    damagePlayer: function (sourceX) {},
    setHearts: function (hearts) {},
    setInvulnerable: function (seconds) {},
    teleport: function (x, y) {},
    setPlayerVelocity: function (vx, vy) {},
    setLevelTime: function (seconds) {},
    setAudioEnabled: function (enabled) {},

    setWater: function (index, x, y, w, h) {},
    setCurrentForce: function (index, force) {},
    setLilyPad: function (index, x, y, w, h) {},
    setOneWay: function (index, x, y, w, h) {},
    setThorn: function (index, x, y, w, h) {},
    setMovingPlatform: function (index, x, y) {},
    setMovingPlatformPhase: function (index, seconds) {},

    setCheckpointActivated: function (activated) {},
    setRespawn: function (x, y) {},

    setCamera: function (x, y) {},
    setMessage: function (text, seconds) {},
    setTutorialFlag: function (flag, value) {},
    setTutorialActive: function (id) {},
    triggerAudio: function (event) {}
  }
};
```

Input functions:

| Function | Behavior |
| --- | --- |
| `input.setLeft(down)` | Sets left input |
| `input.setRight(down)` | Sets right input |
| `input.setJump(down)` | Sets jump held state; sets press edge on false-to-true |
| `input.pressJump(holdFrames)` | Simulates jump press held for `holdFrames`, default 12 |
| `input.setMenu(key, down)` | Sets menu key: `"up"`, `"down"`, `"left"`, `"right"`, `"enter"`, `"space"`, `"esc"` |
| `input.pressMenu(key)` | Presses and releases menu key within one update |

Core action details:

| Function | Behavior |
| --- | --- |
| `start(opts)` | Boots game. Optional `{ level: 1 }` starts directly in that level. |
| `reset(opts)` | Resets to title. `{ save: false }` clears save; `{ save: true }` preserves save. |
| `step(frames, opts)` | Advances fixed frames, default 1. Each frame is `dt = 1/60`. Returns final state. |
| `until(predicate, maxFrames)` | Steps until predicate true, default max 120. Returns Promise. |
| `getState()` | Returns serializable state. |
| `actions.startNewGame()` | Clears save, starts Level 1, state playing. |
| `actions.continueGame()` | Starts `save.unlocked_level`, or Level 1 if no save. |
| `actions.playAgain()` | Clears save, starts Level 1. |
| `actions.selectTitleOption(index)` | Selects title option; enters confirmation if New Game with save. |
| `actions.moveMenu(dir)` | Moves menu selection, wraps around. |
| `actions.pressEnter()` | Confirms current menu/screen action. |
| `actions.pressEsc()` | Triggers Esc behavior. |
| `actions.pause()` | Pauses only if playing and not dead. |
| `actions.resume()` | Resumes only if paused. |
| `actions.restartLevel()` | Restarts current level completely. |
| `actions.quitToTitle()` | Saves current unlocked level and returns to title. |
| `actions.loadLevel(index)` | Loads authored level by 1-based index, state playing. |
| `actions.loadTestLevel(spec)` | Loads test level, state playing. |
| `actions.validateLevel(data)` | Returns validation errors. |
| `actions.setSave(save)` | Sets save state for tests. |
| `actions.collectDewdrop(index)` | Collects dewdrop by index, or first uncollected if omitted. |
| `actions.setDewdropCollected(index, collected)` | Sets dewdrop collected state. |
| `actions.killEnemy(idOrIndex)` | Kills enemy. |
| `actions.setEnemyPosition(idOrIndex, x, y)` | Sets enemy center position. |
| `actions.setEnemyAlive(idOrIndex, alive)` | Sets enemy alive state. |
| `actions.setEnemyDirection(idOrIndex, direction)` | Sets enemy direction. |
| `actions.setBossHp(hp)` | Sets boss HP; if <= 0, boss dead and exit active. |
| `actions.setBossState(state)` | Sets boss state. |
| `actions.setBossPosition(x, y)` | Sets boss center position. |
| `actions.unlockExit(active)` | Overrides exit active state. |
| `actions.damagePlayer(sourceX)` | Applies damage; default sourceX is player.x. |
| `actions.setHearts(hearts)` | Sets hearts 0-3; 0 starts death. |
| `actions.setInvulnerable(seconds)` | Sets invulnerability timer. |
| `actions.teleport(x, y)` | Teleports player center, resets velocity/onGround. |
| `actions.setPlayerVelocity(vx, vy)` | Sets player velocity. |
| `actions.setLevelTime(seconds)` | Sets level time. |
| `actions.setAudioEnabled(enabled)` | Enables/disables audio; lastEvent still records. |
| `actions.setWater(index, x, y, w, h)` | Sets water rectangle. |
| `actions.setCurrentForce(index, force)` | Sets current force, +120 or -120. |
| `actions.setLilyPad(index, x, y, w, h)` | Sets lily pad rectangle. |
| `actions.setOneWay(index, x, y, w, h)` | Sets one-way platform rectangle. |
| `actions.setThorn(index, x, y, w, h)` | Sets thorn rectangle. |
| `actions.setMovingPlatform(index, x, y)` | Sets moving platform current position. |
| `actions.setMovingPlatformPhase(index, seconds)` | Sets moving platform phase via level time offset. |
| `actions.setCheckpointActivated(activated)` | Sets checkpoint activated state. |
| `actions.setRespawn(x, y)` | Sets respawn center. |
| `actions.setCamera(x, y)` | Sets camera top-left. |
| `actions.setMessage(text, seconds)` | Sets HUD message. |
| `actions.setTutorialFlag(flag, value)` | Sets tutorial flag. |
| `actions.setTutorialActive(id)` | Sets active tutorial prompt. |
| `actions.triggerAudio(event)` | Records/plays audio event for tests. |

# 9. TESTS

Tests run in `test.html` through `window.__game` and `window.__test`. Tests use fixed stepping, no real timers, no network, no image files, no audio files, and no user interaction.

Test success criteria:

```js
window.__testResults.failed === 0
window.__testResults.assertions > 100
```

Recommended tolerances:

| Value | Tolerance |
| --- | ---: |
| Position | 1 px |
| Velocity | 5 px/s |
| Timer | 0.05 s |

## 9.1 Tier 1 tests

### Boot and debug

| Test | Setup | Assertions |
| --- | --- | --- |
| `boot.debug-api-exists` | Load `test.html` | `window.__game` exists, `getState` is function, `input` exists, `actions` exists |
| `boot.starts-at-title` | `freshGame()` | `gameState === "title"`, `save.exists === false`, title options include New Game and Controls |

### Save and title flow

| Test | Setup | Assertions |
| --- | --- | --- |
| `save.no-save-title-options` | `freshGame()` | Title options exactly `["New Game", "Controls"]` |
| `save.new-game-starts-level-1` | `freshGame()`, select New Game | `gameState === "playing"`, level index 1, name Pond Edge, `save.unlocked_level === 1`, `save.completed === false` |
| `save.new-game-confirmation-when-save-exists` | Set save exists unlocked 3, return title, select New Game | `title.confirm` not null, confirm options `["Yes", "No"]` |
| `save.new-game-confirmation-yes` | Select Yes | `gameState === "playing"`, level index 1, save exists false, completed false |
| `save.new-game-confirmation-no` | Select No | `gameState === "title"`, confirm null, save unchanged |
| `save.completed-title-options` | Set completed save, return title | Title options exactly `["Play Again", "New Game", "Controls"]` |
| `save.play-again-resets-and-starts-level-1` | Select Play Again | `gameState === "playing"`, level index 1, save exists false, completed false |
| `save.continue-starts-unlocked-level` | Set save unlocked 4, return title, select Continue | `gameState === "playing"`, level index 4, name Stormy Creek |
| `save.quit-to-title-saves-unlocked-level` | Load Level 3, pause, quit | `gameState === "title"`, save exists true, unlocked 3, completed false |

### Level data

| Test | Setup | Assertions |
| --- | --- | --- |
| `levels.all-six-load` | Load levels 1-6 | Each loads playing, name non-empty, width/height positive, player at spawn, exit exists, dewdrop total correct |
| `levels.dewdrop-totals` | Load each level | Totals are `[5, 7, 12, 11, 12, 3]` |
| `levels.level-6-has-locked-exit` | Load Level 6 | Boss exists, HP 6, alive true, exit locked true, active false |
| `levels.level-6-exit-unlocks-after-boss` | Load Level 6, `setBossHp(0)` | Boss alive false, exit active true |
| `levels.validator-rejects-invalid-data` | Invalid data: missing exit, spawn out of bounds, invalid enemy type, boss not level 6 | `validateLevel` returns non-empty errors for each |

### Player movement

| Test | Setup | Assertions |
| --- | --- | --- |
| `physics.run-right` | Ground test level, right 60 frames | `vx` close to 240, x increased |
| `physics.run-left` | Teleport middle, left 60 frames | `vx` close to -240, x decreased |
| `physics.friction-stops-player` | Run right 60 frames, release, step 60 frames | `vx === 0` |
| `physics.full-jump-height` | Press jump held at least 60 frames, step until `vy >= 0` | Max height at least 90 px and no more than 100 px |
| `physics.variable-jump-cut` | Press jump held 1 frame, step until `vy >= 0` | Max height less than 50 px |
| `physics.coyote-time` | Ground ending at x=400, teleport x=380, walk off, step 4 frames, press jump | Player jumps. Reset, walk off, step 8 frames, press jump. Player does not jump. |
| `physics.jump-buffer` | Gap test level, teleport above gap, press jump 6 frames before landing | Player jumps immediately after landing, `vy < 0` shortly after landing |
| `physics.max-fall-speed` | Teleport high, step until `vy > 800` | `vy <= 900` |

### Water

| Test | Setup | Assertions |
| --- | --- | --- |
| `water.entering-caps-vy` | Teleport above water, set `vy = 900`, step until inWater | `vy <= 220` |
| `water.swim-upward` | Teleport into water, hold jump 60 frames | `vy <= -200`, `inWater === true` |
| `water.surface-jump` | Teleport on surface, press jump | `vy` close to -460, `onSurface` was true |
| `water.current-pushes-player` | Current +120, step 30 frames; then -120, step 30 frames | `vx` increases with +120, decreases with -120 |

### Platforms

| Test | Setup | Assertions |
| --- | --- | --- |
| `platform.one-way-landing` | Teleport above one-way, step until land | `onGround === true`, `vy === 0`, bottom equals platform top within 1 px |
| `platform.one-way-pass-through` | Teleport below one-way, press jump | Player passes through while rising |
| `platform.lily-bounce` | Teleport above lily pad, no jump held, step until bounce | `vy` close to -620, `onGround === false` |
| `platform.lily-bounce-held` | Hold jump above lily pad, step until bounce | `vy` close to -680 |
| `platform.moving-platform-carries-player` | Place player on moving platform, step 30 frames | Player X changes same direction as platform, remains on platform |
| `platform.moving-platform-resets-on-respawn` | Set level time 1, kill player, wait respawn | `level.time === 0` |

### Enemies and damage

| Test | Setup | Assertions |
| --- | --- | --- |
| `enemy.mosquito-patrols` | Step 120 frames | X stays within bounds, X changes, reverses at bounds |
| `enemy.dragonfly-patrols` | Step 120 frames | X stays within bounds, X changes |
| `enemy.stomp-kills-enemy` | Enemy under player, `vy = 100`, step until collision | Enemy alive false, player `vy` close to -380 |
| `enemy.side-contact-damages` | Enemy beside player, step until collision | Hearts decrease by 1, `invulnTimer > 0`, knockback away |
| `enemy.invuln-ignores-damage` | Enemy beside player, set invulnerable 1 s, step | Hearts unchanged |
| `enemy.invuln-stomp-works` | Enemy under player, invulnerable, `vy = 100`, step | Enemy dies, hearts unchanged, bounce occurs |
| `hazard.thorn-damages` | Teleport into thorn, step | Hearts decrease by 1 |
| `hazard.multiple-hazards-apply-one-damage` | Overlap enemy and thorn, step | Hearts decrease by exactly 1 |
| `player.death-respawn` | Set hearts 1, damage player | `dead === true`; after 36 frames, `dead === false`, hearts 3, position respawn |
| `player.fall-below-level-kills` | Teleport y = level.height + 200, step | Player dies; after 36 frames respawns |

### Dewdrops, checkpoints, exits

| Test | Setup | Assertions |
| --- | --- | --- |
| `dewdrop.collect` | Teleport to dewdrop, step | `dewdrops.collected === 1` |
| `dewdrop.persist-after-respawn` | Collect, kill, wait respawn | `dewdrops.collected === 1` |
| `dewdrop.reset-on-restart` | Collect, restart | `dewdrops.collected === 0` |
| `checkpoint.sets-respawn` | Teleport to checkpoint, step, kill, wait | Respawn position equals checkpoint |
| `checkpoint.refills-hearts` | Set hearts 1, teleport to checkpoint, step | Hearts 3 |
| `exit.completes-level` | Teleport to active exit, step | `gameState === "levelComplete"`, correct dewdrop count |
| `exit.level-6-locked` | Load Level 6, teleport to exit, step; then `setBossHp(0)`, teleport, step | First remains playing; second becomes gameComplete |

### Boss

| Test | Setup | Assertions |
| --- | --- | --- |
| `boss.idle-lunge-cycle` | Load Level 6, step 72 frames | Boss changes idle to lunge, moves toward player during lunge |
| `boss.phase-2-timing` | Load Level 6, `setBossHp(3)`, `setBossState("idle")`, step 48 frames | Boss enters lunge after approximately 0.8 s, lunge speed approximately 380 px/s |
| `boss.stomp-reduces-hp` | Player above boss head, `vy = 100`, step until stomp | Boss HP decreases by 1, player `vy` close to -420 |
| `boss.death-unlocks-exit` | `setBossHp(1)`, stomp boss | Boss alive false, state dead, exit active true |
| `boss.dead-persists-after-respawn` | Kill boss, kill player, wait respawn | Boss remains dead, exit remains active |

### HUD, UI, messages

| Test | Setup | Assertions |
| --- | --- | --- |
| `ui.level-name-message` | Ground test level, step 1 frame; step 150 frames | Message is level name, then expired |
| `ui.tutorial-movement-hides` | Load Level 1; set right, step 1 frame | `activeId` initially `move`; after input, `firstHorizontalInput` true and activeId not `move` |
| `ui.checkpoint-message` | Teleport to checkpoint, step 1 frame; step 90 frames | Message is Checkpoint, then expired |
| `ui.pause-resume` | Pause, resume | State paused, then playing |
| `ui.pause-restart-level` | Collect dewdrop, pause, restart | State playing, player at spawn, dewdrops 0 |
| `ui.pause-quit-to-title` | Load Level 3, pause, quit | State title, save unlocked 3 |
| `ui.pause-disabled-during-death` | Set hearts 1, damage player, pause | State is not paused |

### Full game flow

| Test | Setup | Assertions |
| --- | --- | --- |
| `flow.synthetic-full-loop` | Smoke level, hold right, step until level complete, max 3000 frames | `gameState === "levelComplete"`, dewdrop count at least 1, checkpoint activated if reached, no exceptions |
| `flow.level-1-scripted-completion` | New Game, hold right, jump windows: first gap x > 820 && x < 890, thorn x > 1290 && x < 1340, second gap x > 1460 && x < 1500, jump hold 14 frames when on ground in window, max 9000 frames, respawn if dead | `gameState === "levelComplete"`, `save.unlocked_level === 2`, no exceptions |
| `flow.all-levels-complete-via-exit` | For levels 1-6, load level; if level 6 `setBossHp(0)`; teleport to exit; step 1 frame | Levels 1-5 levelComplete, Level 6 gameComplete |
| `flow.game-complete-after-level-6` | Load Level 6, `setBossHp(0)`, teleport exit, step; press Enter/Space | `gameState === "gameComplete"`, save completed true, unlocked 6; then title with Play Again |

## 9.2 Tier 2 tests

| Test | Purpose |
| --- | --- |
| `audio.sfx-core-events` | Trigger each core SFX via gameplay or `triggerAudio`; assert `audio.lastEvent` |
| `audio.sfx-added-events` | Trigger dewdrop, player_death, boss_lunge, exit_activation, menu_select, menu_back, pause, perfect; assert `lastEvent` |
| `audio.disabled-still-records` | Disable audio, trigger event, assert `lastEvent` recorded |
| `ui.hud-classes` | Hearts 1-3, assert `.heart.full` / `.heart.empty` counts |
| `ui.hud-dewdrop-text` | Collect dewdrop, assert text format `x / y` |
| `ui.screens-hidden` | For each state, assert only correct screen visible |
| `ui.message-priority` | Activate checkpoint and tutorial simultaneously, assert Checkpoint shown |
| `visual.required-dom-ids` | Assert all required DOM IDs/classes exist |
| `visual.no-hitbox-obscuring` | If effect state exposed, assert no effect timer exceeds 2 frames over hitbox; otherwise manual acceptance |

## 9.3 Tier 3 tests

| Test | Purpose |
| --- | --- |
| `audio.music-state` | Assert `audio.musicState` matches title/level/boss/game complete |
| `audio.pause-ducks-music` | Assert pause/controls use current music at -6 dB or title music at -6 dB |
| `audio.boss-death-resolve` | Assert boss death stops boss music and plays resolve chord state |
| `audio.ambience-level` | Assert ambience state matches level if implemented |

# 10. BUILD ORDER

1. Scaffold files:
   - `index.html`
   - `test.html`
   - `css/style.css`
   - required `js/*` and `test/*` files.
2. Implement `FrogGame.Constants` with all canonical numbers.
3. Implement `FrogGame.Utils`.
4. Implement `FrogGame.Save` with localStorage fallback.
5. Implement `FrogGame.Input` with keyboard mapping and debug input.
6. Implement `FrogGame.Audio` silent event recording; add Tier 2/3 synthesis later.
7. Implement `FrogGame.Assets` optional image loading.
8. Implement `FrogGame.LevelData` with all six authored levels, validation, test level, smoke level.
9. Implement `FrogGame.Level` runtime creation/reset.
10. Implement `FrogGame.Collision` axis-separated movement and resolution.
11. Implement `FrogGame.Player`:
    - movement
    - jumping
    - water
    - lily pads
    - damage
    - death/respawn.
12. Implement `FrogGame.Enemies`:
    - mosquito
    - dragonfly
    - thorn
    - stomp
    - collision order.
13. Implement boss logic in `FrogGame.Enemies` or `FrogGame.Game`:
    - states
    - phases
    - stomp
    - exit unlock.
14. Implement `FrogGame.Camera`.
15. Implement `FrogGame.HUD`.
16. Implement `FrogGame.UI`:
    - title
    - controls
    - pause
    - level complete
    - game complete.
17. Implement `FrogGame.Game` orchestration:
    - state machine
    - update order
    - messages
    - tutorial prompts
    - save timing.
18. Implement `FrogGame.Debug` and `window.__game`.
19. Implement `test/test-harness.js`.
20. Implement `test/tests.js` for Tier 1.
21. Verify Tier 1 tests pass.
22. Add Tier 2 presentation:
    - CSS polish
    - canvas art
    - character animations
    - effects
    - screen shake
    - synthesized SFX.
23. Add Tier 3 audio:
    - music
    - ambience
    - mix.

# 11. DEFINITION OF DONE

## 11.1 Tier 1: Core playable frog platformer

High-level definition: A player can open `index.html`, start a new game, play all six authored levels, defeat the heron, see the game complete screen, and have save data persist unlocked level/completion. The game must pass the Tier 1 test suite.

Checkboxes:

- [ ] `index.html` opens in a normal browser and shows the title screen.
- [ ] No console errors during normal play or tests.
- [ ] Game uses only vanilla HTML, CSS, and JavaScript.
- [ ] No build step, external libraries, Node, npm, or ES modules.
- [ ] Fixed 60 Hz logic update with accumulator clamp.
- [ ] All canonical constants are used by gameplay code.
- [ ] Title screen shows correct options for no save, save, and completed save.
- [ ] New Game starts Level 1.
- [ ] New Game confirmation appears only when save exists.
- [ ] Continue starts `save.unlocked_level`.
- [ ] Play Again clears save and starts Level 1.
- [ ] Controls screen opens and returns correctly from title and pause.
- [ ] All six authored levels load from `FrogGame.LevelData.LEVELS`.
- [ ] Level validation passes for all six authored levels.
- [ ] Dewdrop totals are `[5, 7, 12, 11, 12, 3]`.
- [ ] Player can move left/right with A/D and arrows.
- [ ] Player can jump with Space/W/Up.
- [ ] Coyote time works.
- [ ] Jump buffer works.
- [ ] Variable jump cut works.
- [ ] Max fall speed is capped at 900 px/s.
- [ ] Water physics work: swim, surface jump, entry cap, horizontal clamp.
- [ ] Currents apply force and clamp to water max speed.
- [ ] One-way platforms land from above and pass through from below.
- [ ] Lily pads bounce with -620 or -680 px/s.
- [ ] Moving platforms move on sine paths and carry player.
- [ ] Mosquito patrols and is stompable.
- [ ] Dragonfly patrols and is stompable.
- [ ] Thorns damage player.
- [ ] Stomping works and applies bounce.
- [ ] Side/bottom enemy contact damages player.
- [ ] Multiple hazards apply only one damage instance.
- [ ] Invulnerability ignores damage but allows stomps.
- [ ] Player has 3 hearts.
- [ ] Checkpoints set respawn and refill hearts.
- [ ] Death from hearts 0 works.
- [ ] Death from falling below level works.
- [ ] Respawn keeps collected dewdrops.
- [ ] Respawn resets enemies and moving platforms.
- [ ] Respawn keeps boss dead if boss was dead.
- [ ] Dewdrops collect and persist through respawn.
- [ ] Dewdrops reset on level restart.
- [ ] Exits complete levels 1-5.
- [ ] Level 6 exit is locked until boss dies.
- [ ] Boss has 6 HP.
- [ ] Boss phase 1 and phase 2 timings/speeds work.
- [ ] Boss stomp zone is top 12 px.
- [ ] Boss death unlocks exit.
- [ ] Level complete screen shows level name, dewdrops, perfect, continue prompt.
- [ ] Game complete screen shows ending and returns to title.
- [ ] HUD shows hearts, dewdrop count, and messages.
- [ ] Tutorial prompts appear and hide correctly.
- [ ] Camera follows player, clamps to level bounds, uses deadzone/lookahead/smoothing.
- [ ] Save stores only `unlocked_level` and `completed`.
- [ ] Quit to title saves current unlocked level.
- [ ] `window.__game` debug API exists and works.
- [ ] `test.html` runs all Tier 1 tests.
- [ ] `window.__testResults.failed === 0`.
- [ ] `window.__testResults.assertions > 100`.

## 11.2 Tier 2: Presentation and feedback

High-level definition: The game looks and feels like the designed pond platformer: readable art, clear animations, synthesized SFX, small effects, and accessible presentation.

Checkboxes:

- [ ] Visual style matches §3: soft pixel art, bright readable pond world.
- [ ] Logical resolution remains 1280 x 720.
- [ ] Gameplay hitboxes are unchanged by visual styling.
- [ ] Player frog visual matches §5.
- [ ] Player facing is visible.
- [ ] Player invulnerability blink is visible and limited to 8 toggles/sec.
- [ ] Player death state is visible.
- [ ] Mosquito, dragonfly, and heron visuals match §5.
- [ ] Heron stomp band is visible.
- [ ] Boss HP droplets are visible.
- [ ] Solid ground, one-way leaves, lily pads, water, currents, thorns, dewdrops, checkpoints, and exits are visually distinct.
- [ ] Locked exit is visually distinct from active exit.
- [ ] Currents show direction with chevrons.
- [ ] Level palettes and backgrounds match §3.
- [ ] Backgrounds do not create fake hazards or platforms.
- [ ] Effects do not obscure hitboxes for more than 2 frames.
- [ ] Screen shake matches §3 table.
- [ ] Transitions match §3 table.
- [ ] HUD typography and panel style match §3.
- [ ] Accessibility rules are met: no color-only hazards, no strobing, no hidden hitboxes, readable text.
- [ ] Synthesized SFX are implemented for all events in §6.
- [ ] Audio event mapping matches §6.
- [ ] Missing audio does not break gameplay.
- [ ] Tier 2 tests pass.

## 11.3 Tier 3: Music and ambience

High-level definition: The game has a complete calm pond audio atmosphere with music and ambience that do not obscure SFX.

Checkboxes:

- [ ] Title music plays on title.
- [ ] Level music plays for each level.
- [ ] Boss music plays when heron is active.
- [ ] Boss phase 2 increases intensity.
- [ ] Boss death plays resolve chord.
- [ ] Game complete music plays.
- [ ] Ambience matches level state.
- [ ] Music ducks during pause/controls.
- [ ] No thunder, lightning crack, scary stingers, or harsh distortion.
- [ ] Ambience does not hide SFX.
- [ ] Tier 3 tests pass.

# A. SANITY

Checks performed:

| Check | Result | Notes / Fix |
| --- | --- | --- |
| Dewdrop totals match level data | Valid | Counts are Level 1: 5, Level 2: 7, Level 3: 12, Level 4: 11, Level 5: 12, Level 6: 3. |
| Player spawn centers produce correct feet | Valid | Ground top 640 with player center y 626 gives bottom 640. Ground top 1216 with center y 1202 gives bottom 1216. |
| Boss spawn center produces correct bottom | Valid | Boss height 80, center y 600 gives bottom 640, matching Level 6 ground top. |
| Exit centers are on or near ground where intended | Valid | Ground-level exits have center y 608, hitbox height 64, bottom 640. Vertical exits are placed above platforms. |
| Checkpoint centers align with surfaces | Valid | Level 1/2/4 checkpoints at y 624 sit on ground top 640. Level 3 checkpoint at y 672 sits on one-way top 688. Level 5 checkpoint at y 496 sits on one-way top 512. |
| Level 6 exit locked state | Valid | Level 6 exit `locked: true`, active false until boss HP reaches 0. |
| Camera clamps for small and large levels | Valid | Level 6 is 1280 x 720, camera clamps to 0. Larger levels clamp to `[0, width-1280]` and `[0, height-720]`. |
| Jump height range | Valid | With gravity 1400 and jump velocity -520, ideal height is about 96.6 px, inside engineering test range 90-100 px. |
| Coyote time frame count | Valid | 0.08 s is 4.8 frames; 4-frame jump test and 8-frame no-jump test are consistent. |
| Jump buffer frame count | Fixed | Engineering test originally used 8 frames before landing, which is 0.133 s and exceeds the 0.12 s buffer. Changed to 6 frames before landing. |
| Surface jump cut behavior | Fixed | Engineering left `jumpCutApplied` false for surface jumps, which could allow variable cut. Ruled surface jumps set `jumpType = "surface"` and are not cut. |
| Lily pad cut behavior | Valid | Lily pad bounce sets `jumpCutApplied = false`, so releasing jump can cut the bounce. This matches gameplay’s generic release algorithm and gives deliberate hold value. |
| Stomp cut behavior | Valid | Stomp sets `jumpCutApplied = false`; if player releases jump during stomp bounce, cut can apply. This is acceptable because it is player input. |
| Boss death persistence | Valid | Death respawn keeps boss dead; Restart Level resets boss alive. Documented in §0.2 and §4.13. |
| Level 1 scripted jump windows | Valid | First gap 900-1020, window 820-890; thorn 1350-1398, window 1290-1340; second gap 1500-1660, window 1460-1500. |
| Level 3 vertical spacing | Valid | One-way platform vertical steps are 88 px, matching max normal vertical step. Lily pad and moving platform cover larger gaps. |
| Level 5 vertical spacing | Valid | One-way platform vertical steps are 88 px; lily chain and moving platform cover intended route. |
| Current force values | Valid | Currents use +120 or -120, matching `CURRENT_FORCE`. |
| Enemy sizes | Valid | Mosquito 24 x 20, dragonfly 28 x 16, heron 56 x 80. |
| HUD positions | Valid | Hearts top-left 16 px, dewdrops top-right 16 px, message top-center 48 px below top, max width 600 px. |
| Message priority | Valid | Level Complete is a screen. HUD priority is Checkpoint > Tutorial > Level name. |
| Audio external file requirement | Fixed | Dropped required `.ogg`/`.mp3` files. Audio is synthesized or silent. |
| Music requirement | Fixed | Music moved to Tier 3 optional. |
| Screen shake/particles requirement | Fixed | Moved to Tier 2 optional. Tier 1 uses minimal state feedback. |
| Randomness | Valid | No `Math.random` in gameplay. Decorative effects use deterministic time/entity-id patterns. |
| DOM IDs required by engineering | Valid | `#game`, `#canvas`, `#hud`, `#hearts`, `#dewdrops`, `#message`, `#ui`, `.screen`, `.hidden`, `.menu-item`, `.menu-item.selected`, `.confirm`, `.heart`, `.heart.full`, `.heart.empty`, `.dewdrop-icon` are required. |
| Debug API serializable state | Valid | `getState()` must return plain JSON-safe data only. |
| Test harness globals | Valid | `window.__test`, `window.__testsDone`, `window.__testResults` exist only in `test.html`. |
| No gameplay dependency on rendering | Valid | Camera, canvas pixels, DOM measurements, and visual assets must not affect logic. |
| Dropped items documented | Valid | External audio files, required music, Tier 1 particles/screen shake, full art in Tier 1, and all cut features are documented in §0.2. |