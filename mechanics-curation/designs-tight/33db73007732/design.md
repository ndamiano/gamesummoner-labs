# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Game prompt: A game about frogs eating bugs | `# 4. GAMEPLAY SPEC`, `# 5. CHARACTERS`, `# 3. VISUAL SPEC` |
| Dimension: 2D | `# 1.1 Units, axes, frames`, `# 3. VISUAL SPEC`, `# 4. GAMEPLAY SPEC` |
| Camera: top-down | `# 1.1 Units, axes, frames`, `# 3. VISUAL SPEC`, `# 4. GAMEPLAY SPEC` |
| Time model: real-time | `# 1.2 Important conventions`, `# 2. CONTRACTS`, `# 4. GAMEPLAY SPEC` |
| Movement model: free movement | `# 4.1 Catching System`, `# 5. CHARACTERS` |
| Session shape: endless | `# 4.3 Difficulty and Progression`, `# 4.4 Run Structure`, `# 7. UX` |
| Failure: lose a life | `# 4.1 Catching System`, `# 4.4 Run Structure`, `# 7. UX` |
| Tone: silly | `# 3. VISUAL SPEC`, `# 5. CHARACTERS`, `# 6. AUDIO`, `# 7. UX` |
| Size: one screen, a few minutes | `# 1.1 Units, axes, frames`, `# 3. VISUAL SPEC`, `# 4.3 Difficulty and Progression` |
| Win/lose: survive as long as possible, no ending, play forever | `# 4.4 Run Structure`, `# 7. UX`, `# 11. DEFINITION OF DONE` |
| Core mechanics: catching targets move around the scene and the player must catch them | `# 0.3 Tiers`, `# 4.1 Catching System` |
| Supporting mechanics: scoring awards points and records best scores | `# 4.2 Scoring System`, `# 7. UX` |
| Extra mechanics: none | `# 4.1 Catching System`, `# 4.3 Difficulty and Progression` |
| Art style: flat vector, clean flat shapes, solid colours, crisp edges | `# 3. VISUAL SPEC`, `# 5. CHARACTERS` |
| Palette: saturated, bright, strong colours | `# 3. VISUAL SPEC` |
| Typography: hand-lettered, drawn, irregular letters | `# 3. VISUAL SPEC`, `# 7. UX` |
| Music: chiptune, retro console bleeps | `# 6. AUDIO` |
| Sound effects style: retro bleeps, synthesized chip sounds | `# 6. AUDIO` |
| Screens: title, pause, game over, high scores | `# 7. UX` |
| HUD: health, score, combo counter | `# 7. UX` |
| Effects: particles, hit flash | `# 3. VISUAL SPEC`, `# 4.1 Catching System`, `# 6. AUDIO` |
| Accessibility: colour-blind safe palette, reduced motion, difficulty options | `# 3. VISUAL SPEC`, `# 7. UX`, `# 4.3 Difficulty and Progression` |

## 0.2 Decisions

| Decision | Ruling / Final | Where | Why |
| --- | --- | --- | --- |
| Final: game prompt is frogs eating bugs | The player is a frog. Bugs are the only targets. No other species, tools, or hazards. | `# 4`, `# 5` | Keeps the prompt literal and silly. |
| Final: 2D | All entities are planar circles/segments. No z-depth. | `# 1.1`, `# 2`, `# 4` | Matches dimension decision. |
| Final: top-down camera | Fixed full-screen camera, origin top-left, x right, y down. | `# 1.1`, `# 3` | Matches camera decision and one-screen size. |
| Final: real-time | Fixed 60 Hz update loop with requestAnimationFrame accumulator. | `# 1.2`, `# 2` | Deterministic tests and stable physics. |
| Final: free movement | Continuous vector movement with acceleration/friction. | `# 4.1` | Matches free movement. |
| Final: endless session | No win state. Run ends only when health reaches 0. | `# 4.3`, `# 4.4`, `# 7` | Matches endless survival. |
| Final: failure loses a life | Health is integer lives. Wasp contact removes 1 life. | `# 4.1` | Gives failure without adding extra mechanics. |
| Final: tone is silly | Frog squash, goofy sounds, playful copy, bright shapes. | `# 3`, `# 5`, `# 6` | Matches tone. |
| Final: one screen, a few minutes | Logical canvas is 960×600. Difficulty ramps to produce typical runs of 2–5 minutes. | `# 1.1`, `# 4.3` | Matches size. |
| Final: survive as long as possible, no ending, play forever | High scores store time and score. No win screen. | `# 4.2`, `# 7` | Matches win/lose. |
| Final: core mechanic is catching | Catching is implemented with a tongue input and bug targets. | `# 4.1` | Core decision. |
| Final: supporting mechanic is scoring | Scoring/combo/high scores are Tier 2. | `# 4.2`, `# 0.3` | Required banding. |
| Final: extra mechanics none | No traps, pickups, power-ups, obstacles, camera movement, hunger, or separate hazard system. | `# 4.1`, `# 4.3` | Required exact scope. |
| Final: flat vector art | Solid fills, crisp dark outlines, no gradients, no blur except flat particle circles. | `# 3` | Required art style. |
| Final: saturated palette | Bright teal, blue, purple, yellow, orange, pink on dark blue. | `# 3` | Required palette. |
| Final: hand-lettered typography | Inline SVG hand-lettered letters and digits. Irregular baseline/stroke. | `# 3`, `# 7` | Required typography. |
| Final: chiptune music | Square/triangle/noise WebAudio loops. | `# 6` | Required music. |
| Final: retro bleep SFX | Short synthesized envelopes. | `# 6` | Required SFX. |
| Final: screens title, pause, game over, high scores | Exactly four screens. Settings live inside title/pause, not as a new screen. | `# 7` | Required exact screens. |
| Final: HUD health, score, combo counter | Exactly three HUD elements. | `# 7` | Required exact HUD. |
| Final: effects particles, hit flash | Only these effects. No screen shake. | `# 3`, `# 4.1` | Required exact effects. |
| Final: accessibility colour-blind safe palette, reduced motion, difficulty options | Palette uses shape/pattern plus colour. Reduced motion option. Easy/Normal/Hard options. | `# 3`, `# 4.3`, `# 7` | Required accessibility. |
| Designer: game title | “Ribbit Snack”. | `# 7` | Silly, fits prompt. |
| Designer: player identity | Chef Ribbit, a cartoon frog hunting bugs on a lily pond. | `# 4`, `# 5` | Gives concrete player. |
| Designer: input mapping | Move with WASD/Arrow keys. Aim with pointer if available, otherwise facing follows movement. Tongue with Space, Enter, or click. | `# 4.1`, `# 2`, `# 8` | Named input for core catching. |
| Designer: target roster | Tier 1: Fly and Wasp. Tier 2: Mosquito and Firefly. No other targets. | `# 4.1` | Keeps core minimal, adds content only after core. |
| Designer: failure source | Wasps chase the frog. If a wasp touches the frog, the frog loses one life. Catching a wasp removes it safely. | `# 4.1` | Creates failure pressure inside catching, not a separate hazard system. |
| Designer: traps/pickups | None. Extra mechanics are explicitly none. | `# 4.1` | Required scope. |
| Designer: canvas bounds | Logical canvas 960×600. Safe bounds x 16–944, y 16–584. | `# 1.1`, `# 3`, `# 4.1` | One screen with HUD overlay. |
| Designer: player numbers | Radius 18. Normal speed 190 px/s. Acceleration 1600 px/s². Friction 2200 px/s². Invulnerability 1.5 s after damage. | `# 4.1` | Concrete movement. |
| Designer: tongue numbers | Length 140 px. Tongue radius 6 px. Extend 0.12 s, hold 0.04 s, retract 0.10 s. Normal cooldown 0.35 s. | `# 4.1` | Concrete catching. |
| Designer: bug numbers | Fly r8 speed 70. Mosquito r7 speed 95. Firefly r9 speed 55. Wasp r10 base speed 75. | `# 4.1` | Concrete targets. |
| Designer: spawn numbers | Normal initial: 2 flies, 1 wasp. Normal max total 8, wasps 2. Spawn intervals: fly 2.5 s, mosquito 4.0 s, firefly 12.0 s, wasp 7.0 s. | `# 4.1` | Concrete endless spawning. |
| Designer: difficulty progression | Level increases every 30 s. Spawn intervals multiply by 0.92 per level. Wasp speed +4 per level capped +60. Total cap +1 every 2 levels capped +4. Wasp cap +1 every 3 levels capped +2. | `# 4.3` | Endless ramp. |
| Designer: difficulty options | Easy, Normal, Hard. Adjust health, player speed, tongue cooldown, wasp speed, spawn caps/intervals. | `# 4.3` | Required difficulty options. |
| Designer: scoring formula | Base points: Fly 10, Mosquito 25, Firefly 60, Wasp 45. Multiplier = 1 + floor(combo / 5), capped at 5. | `# 4.2` | Rewards performance. |
| Designer: combo rules | Any catch increments combo. Combo timer 5 s. Damage resets combo. | `# 4.2` | Concrete combo. |
| Designer: high scores | Top 10 per difficulty in localStorage. Fields: score, timeMs, maxCombo, initials, date. | `# 4.2`, `# 7` | Required best scores. |
| Designer: reduced motion | Reduces particles, disables idle bob/flicker/screen flash, keeps gameplay hitboxes unchanged. | `# 3`, `# 7` | Required accessibility. |
| Designer: colour-blind safe palette | Uses high-contrast non-red/green colours and distinct bug shapes/patterns. | `# 3` | Required accessibility. |
| Designer: RNG | Seeded mulberry32 PRNG. No Math.random in gameplay. | `# 1.2`, `# 2` | Tests and reproducibility. |
| Designer: state machine | title, playing, paused, gameOver, highScores are internal modes. Only four user-facing screens. | `# 7` | Required exact screens. |
| Designer: debug API | Direct state access for catching, scoring, input. | `# 8` | Required testability. |

## 0.3 Tiers

| Tier | Scope | Systems included | Not included |
| --- | --- | --- | --- |
| Tier 1 | Core catching and failure. A player can start, move, tongue-catch flies, avoid or tongue-catch wasps, lose lives, and reach game over. All required art, audio, HUD health, particles, and hit flash are present. | Catching: player movement, aim, tongue, Fly, Wasp, spawning, bounds, damage, game over. Minimal title, pause, game over. HUD health. Score/combo widgets exist but remain 0. | Scoring values, combo rules, high scores, Mosquito, Firefly, difficulty options, reduced motion, settings. |
| Tier 2 | Supporting scoring and best scores. Adds full score/combo/high scores and additional target content. | Scoring, combo, multiplier, high scores screen, initials entry, Mosquito, Firefly, full game over score presentation. | Difficulty options, settings, reduced motion. |
| Tier 3 | Accessibility and difficulty control. Adds options required by the prompt without adding mechanics. | Easy/Normal/Hard, reduced motion toggle, settings UI on title/pause, colour-blind safe verification. | New mechanics, traps, pickups, power-ups, extra screens, extra effects. |

---

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Value | Number |
| --- | --- |
| Logical canvas width | 960 px |
| Logical canvas height | 600 px |
| Coordinate origin | top-left |
| Positive x | right |
| Positive y | down |
| Angle 0 | east/right |
| Angle π/2 | south/down |
| Fixed update step | 1/60 s |
| Max physics steps per rendered frame | 5 |
| Player radius | 18 px |
| Player safe bounds | x 16–944, y 16–584 |
| Bug safe bounds | x 12–948, y 12–588 |
| Tongue origin offset from player centre | 20 px in facing direction |
| Tongue max length | 140 px |
| Tongue hit radius | 6 px |
| Score unit | integer points |
| Health unit | integer lives |
| Time unit | seconds for rules, milliseconds for storage |
| Speed unit | px/s |
| Acceleration unit | px/s² |

## 1.2 Important conventions

| Convention | Rule |
| --- | --- |
| Deterministic RNG | Use seeded mulberry32. All gameplay randomness reads `ctx.rng`. |
| No ambient randomness | No `Math.random()` in gameplay, render, audio scheduling, or UI logic. |
| Fixed step | Gameplay updates only in fixed `dt = 1/60`. Render does not mutate gameplay. |
| State ownership | All mutable gameplay state lives in `ctx`. Modules do not keep hidden gameplay state. |
| Pure rendering | `render.js` draws from `ctx`. It never changes gameplay fields except visual timers if explicitly allowed. |
| Input edges | `ctx.input.tonguePressed` is a one-frame edge. `catching.js` consumes it by setting it false. |
| Bounds | Player and bugs are clamped or bounced inside safe bounds. |
| Collision | All hit detection is circle or circle-segment distance. |
| Screens | UI screens are HTML/CSS overlays. Canvas only renders the game world. |
| Settings persistence | Difficulty and reduced motion persist in localStorage. High scores persist in localStorage. |
| Reduced motion | Reduces nonessential motion only. It never changes hitboxes, speeds, spawn rules, or scoring. |
| Colour-blind safety | Colour is never the only identifier. Bug types always have distinct silhouettes and patterns. |
| No extra systems | No traps, pickups, obstacles, hunger, power-ups, camera movement, screen shake, or separate hazard system. |
| Tier isolation | Tier 2 and Tier 3 must not be required for Tier 1 to run. Tier 1 may include no-op stubs for scoring. |

---

# 2. CONTRACTS

## 2.1 Module layout

```text
index.html
css/main.css
js/main.js
js/context.js
js/config.js
js/rng.js
js/input.js
js/loop.js
js/catching.js
js/scoring.js
js/characters.js
js/render.js
js/particles.js
js/audio.js
js/ui.js
js/debug.js
js/tests.js
```

| File | Responsibility |
| --- | --- |
| `index.html` | Canvas element, screen overlays, HUD, high score list, initials entry. |
| `css/main.css` | Layout, hand-lettered SVG text styling, HUD, screens, accessibility focus styles. |
| `js/main.js` | Bootstraps context, input, loop, UI, audio, debug. |
| `js/context.js` | Creates and resets `ctx`. |
| `js/config.js` | All tunable numbers. |
| `js/rng.js` | Seeded PRNG helpers. |
| `js/input.js` | Keyboard, pointer, touch input into `ctx.input`. |
| `js/loop.js` | requestAnimationFrame fixed-step loop. |
| `js/catching.js` | Core catching, spawning, bug movement, tongue, damage, game over. |
| `js/scoring.js` | Score, combo, multiplier, high scores. |
| `js/characters.js` | Character animation state helpers and drawing shapes. |
| `js/render.js` | Draws world, entities, particles, HUD, hit flash. |
| `js/particles.js` | Spawns and updates particles. |
| `js/audio.js` | Chiptune music and retro bleep SFX. |
| `js/ui.js` | Screen state machine, HUD sync, high score UI, settings UI. |
| `js/debug.js` | Direct state access for tests. |
| `js/tests.js` | Tier validation tests. |

## 2.2 Global context

All fields below are present in `ctx`. Tier 2/3 fields exist from boot but are unused until their tier.

```js
ctx = {
  version: 'ribbit-snack.1.0.0',
  mode: 'title', // 'title' | 'playing' | 'paused' | 'gameOver' | 'highScores'

  seed: number,
  rng: Rng,

  timeMs: number,
  runTimeMs: number,

  difficulty: 'easy' | 'normal' | 'hard',
  settings: {
    reducedMotion: boolean,
    difficulty: 'easy' | 'normal' | 'hard'
  },

  ui: {
    screen: 'title' | 'pause' | 'gameOver' | 'highScores',
    selectedDifficulty: 'easy' | 'normal' | 'hard',
    initials: 'AAA',
    highScoreEntryActive: boolean,
    focus: string
  },

  input: {
    keys: {
      KeyW: boolean,
      KeyA: boolean,
      KeyS: boolean,
      KeyD: boolean,
      ArrowUp: boolean,
      ArrowDown: boolean,
      ArrowLeft: boolean,
      ArrowRight: boolean,
      Space: boolean,
      Enter: boolean,
      Escape: boolean
    },
    pointer: {
      active: boolean,
      x: number,
      y: number
    },
    move: {
      x: number,
      y: number
    },
    aim: {
      x: number,
      y: number
    },
    tonguePressed: boolean
  },

  player: {
    x: number,
    y: number,
    vx: number,
    vy: number,
    radius: 18,
    facing: number,
    speed: number,
    acceleration: number,
    friction: number,
    cooldown: number,
    invulnTimer: number,
    flashTimer: number,
    health: number,
    alive: boolean,
    state: 'idle' | 'move' | 'aim' | 'tongue' | 'hurt' | 'dead',
    animTimer: number
  },

  tongue: {
    active: boolean,
    timer: number,
    phase: 'idle' | 'extend' | 'hold' | 'retract',
    ox: number,
    oy: number,
    tx: number,
    ty: number,
    length: number,
    radius: 6
  },

  bugs: [
    {
      id: number,
      type: 'fly' | 'mosquito' | 'firefly' | 'wasp',
      x: number,
      y: number,
      vx: number,
      vy: number,
      radius: number,
      speed: number,
      heading: number,
      timer: number,
      phase: number,
      alive: boolean,
      animTimer: number
    }
  ],

  spawn: {
    timers: {
      fly: number,
      mosquito: number,
      firefly: number,
      wasp: number
    },
    caps: {
      total: number,
      fly: number,
      mosquito: number,
      firefly: number,
      wasp: number
    },
    counts: {
      total: number,
      fly: number,
      mosquito: number,
      firefly: number,
      wasp: number
    },
    level: number,
    levelTimer: number
  },

  particles: [
    {
      x: number,
      y: number,
      vx: number,
      vy: number,
      radius: number,
      life: number,
      maxLife: number,
      kind: 'catch' | 'damage' | 'tongue' | 'spawn',
      color: string
    }
  ],

  flash: {
    timer: number,
    maxTimer: number
  },

  score: number,
  combo: number,
  maxCombo: number,
  comboTimer: number,

  highScores: {
    easy: HighScoreRecord[],
    normal: HighScoreRecord[],
    hard: HighScoreRecord[]
  }
}
```

`HighScoreRecord`:

```js
{
  score: number,
  timeMs: number,
  maxCombo: number,
  initials: string,
  difficulty: 'easy' | 'normal' | 'hard',
  date: string
}
```

## 2.3 Module specifics

| Module | Required exports | Reads from ctx | Writes to ctx | Required for |
| --- | --- | --- | --- | --- |
| `context.js` | `createContext(seed)`, `resetRun(ctx, difficulty)` | config | full `ctx` | All tiers |
| `config.js` | `CONFIG` constants | none | none | All tiers |
| `rng.js` | `mulberry32(seed)`, `range(rng,min,max)`, `int(rng,min,max)`, `pick(rng,array)` | none | none | Tier 1 |
| `input.js` | `bind(canvas,ctx)`, `update(ctx)`, `clearEdges(ctx)`, `getState(ctx)` | DOM events | `ctx.input` | Tier 1 |
| `loop.js` | `start(ctx,canvas)`, `stop()`, `step(ctx,dt)` | `ctx` | `ctx.timeMs`, `ctx.runTimeMs` | Tier 1 |
| `catching.js` | `initRun(ctx)`, `update(ctx,dt)`, `spawnBug(ctx,type,edge)`, `tryTongue(ctx)`, `damagePlayer(ctx,bug)`, `endRun(ctx)`, `updateSpawner(ctx,dt)`, `updateBugs(ctx,dt)`, `updateTongue(ctx,dt)`, `hitTestTongue(ctx)` | `ctx.input`, `ctx.rng`, config | `ctx.player`, `ctx.tongue`, `ctx.bugs`, `ctx.spawn`, `ctx.particles`, `ctx.flash`, `ctx.mode` | Tier 1 |
| `scoring.js` | `addCatch(ctx,bug)`, `update(ctx,dt)`, `endRun(ctx)`, `qualifies(ctx)`, `saveHighScore(ctx,initials)`, `loadHighScores()`, `getHighScores(difficulty)` | `ctx` | `ctx.score`, `ctx.combo`, `ctx.maxCombo`, `ctx.comboTimer`, `ctx.highScores` | Tier 2 |
| `characters.js` | `updateAnimation(ctx,dt)`, `drawFrog(ctx)`, `drawBug(ctx,bug)`, `drawTongue(ctx)` | `ctx` | visual timers only | Tier 1 |
| `render.js` | `draw(ctx)`, `drawWorld(ctx)`, `drawEntities(ctx)`, `drawParticles(ctx)`, `drawHUD(ctx)`, `drawFlash(ctx)` | `ctx` | none | Tier 1 |
| `particles.js` | `spawn(ctx,kind,x,y,color)`, `update(ctx,dt)`, `draw(ctx)` | `ctx` | `ctx.particles` | Tier 1 |
| `audio.js` | `init()`, `play(name)`, `startMusic(kind)`, `stopMusic()` | none required for tests | none | Tier 1 |
| `ui.js` | `bind(dom,ctx)`, `showScreen(name)`, `sync(ctx)`, `syncHUD(ctx)`, `handleKey(ctx,event)`, `openHighScores(ctx)`, `submitInitials(ctx,initials)`, `setDifficulty(ctx,difficulty)`, `setReducedMotion(ctx,value)` | `ctx`, DOM | `ctx.ui`, `ctx.settings`, `ctx.mode` | Tier 1/2/3 |
| `debug.js` | `setMode`, `setInput`, `setPointer`, `pressTongue`, `setPlayer`, `setBugs`, `spawnBug`, `setHealth`, `setScore`, `setCombo`, `setDifficulty`, `setReducedMotion`, `catchingState`, `scoringState`, `inputState` | `ctx` | `ctx` | Tests |
| `tests.js` | `runAll(ctx)` | `ctx` | test results | Tests |

---

# 3. VISUAL SPEC

Visual style: a bright, flat, silly top-down lily pond. The screen is a saturated blue water field with crisp dark outlines and simple vector shapes. The frog is a rounded teal blob with a wide mouth and cartoon eyes. Bugs are distinct silhouettes: oval flies, thin purple mosquitoes, star-shaped yellow fireflies, and striped orange wasps. The camera never moves. All feedback is immediate: tongue shots, pops, particles, and a short white hit flash. The whole look is playful, readable, and colour-blind safe because every bug type has a unique shape and pattern, not just a colour.

Lighting and atmosphere: flat, no shadows, no gradients, no blur. The pond is bright but not realistic. Atmosphere is daytime cartoon nature. The only atmospheric motion is decorative lily pad bobbing and bug hover, disabled under reduced motion.

Space: one screen only. The outer 16 px is a decorative reed border, but collision bounds are the safe bounds. Lily pads are decorative only and do not block movement. Bugs spawn from edges and fly inside bounds. The player is clamped to safe bounds.

| Element | Shape | Size | Colour | Pattern / Accessibility | Animation |
| --- | --- | --- | --- | --- | --- |
| Pond background | full canvas rect | 960×600 | `#102A56` | dark base | none |
| Water bands | horizontal flat bands | full width | `#1D4E89`, `#2A6FB5` | low contrast, decorative | static |
| Reed border | irregular flat rectangles | 16 px | `#007A66`, `#004B40` | outside collision bounds | static |
| Lily pads | rounded pads with notch | 60–110 px | `#007A66`, outline `#0A192F` | decorative | reduced motion disables bob |
| Frog body | rounded oval, mouth wedge, eye bumps | r18 | body `#00E5FF`, belly `#FFFFFF`, outline `#0A192F` | unique silhouette | idle bob, move squash |
| Frog tongue | line segment with round tip | length 140, r6 | `#FF2D95`, outline `#0A192F` | clear line | extend/retract |
| Fly | oval body, two wing circles | r8 | body `#8AB4F8`, wings `#FFFFFF` 40%, outline `#0A192F` | wing pattern | hover wobble |
| Mosquito | thin body, long proboscis | r7 | body `#B388FF`, outline `#0A192F` | dotted body line | zigzag |
| Firefly | round body with star glow | r9 | body `#FFD23F`, glow `#FFF59D`, outline `#0A192F` | star shape | flicker |
| Wasp | pointed body, triangular stinger | r10 | body `#FF6D00`, stripes `#0A192F`, wings `#FFFFFF` 30% | stripes, pointed shape | chase wobble |
| HUD panel | top bar rect | 960×64 | `#0A192F` 85% | no gameplay collision | static |
| Health hearts | heart vector | 24×22 | filled `#FFD23F`, empty `#4A5568` | shape + colour | pop on damage |
| Score text | hand-lettered digits | 28 px min | `#FFFFFF` | high contrast | static |
| Combo text | hand-lettered digits | 28 px min | `#FFD23F` | shape + colour | scale pop only if motion enabled |
| Hit flash | full-screen rect | full canvas | `#FFFFFF` | brief | duration 0.25 s, reduced motion reduces alpha/duration |
| Catch particles | circles | 3–6 px | bug colour | nonessential | disabled under reduced motion |
| Damage particles | rings/particles | 6–10 px | `#FF6D00` | nonessential | disabled under reduced motion |
| Title text | hand-lettered SVG | 72 px min | `#FFFFFF` | irregular baseline | none |
| Screen buttons | rounded rect | 220×48 | `#FF6D00`, focus `#FFFFFF` | high contrast | focus outline |

---

# 4. GAMEPLAY SPEC

Ribbit Snack is a one-screen, real-time, top-down catching game. The player controls a frog that moves freely and shoots a tongue to catch bugs. Flies, mosquitoes, and fireflies are optional targets for points and combo. Wasps are hostile bugs that chase the frog and cause the only life loss by touching the frog. The player survives by catching wasps before they reach the frog and by catching other bugs for score. The game never ends in victory; runs continue until health reaches zero, then the score and survival time are recorded.

## Records and rosters

### Player record

| Field | Meaning |
| --- | --- |
| `x,y` | centre position |
| `vx,vy` | velocity |
| `radius` | 18 px |
| `facing` | angle in radians |
| `speed` | difficulty-dependent max speed |
| `acceleration` | 1600 px/s² |
| `friction` | 2200 px/s² |
| `cooldown` | tongue cooldown remaining |
| `invulnTimer` | damage immunity remaining |
| `flashTimer` | hit flash visual timer |
| `health` | lives, integer |
| `alive` | false when health ≤ 0 |
| `state` | `idle`, `move`, `aim`, `tongue`, `hurt`, `dead` |
| `animTimer` | animation phase |

### Bug record

| Field | Meaning |
| --- | --- |
| `id` | unique integer |
| `type` | `fly`, `mosquito`, `firefly`, `wasp` |
| `x,y` | centre position |
| `vx,vy` | velocity |
| `radius` | collision radius |
| `speed` | current speed |
| `heading` | movement angle |
| `timer` | behaviour timer |
| `phase` | sine/flicker phase |
| `alive` | removed when caught or damaging |
| `animTimer` | animation phase |

### Bug roster

| Type | Tier | Radius | Base speed | Base points | Threat |
| --- | --- | --- | --- | --- | --- |
| Fly | 1 | 8 | 70 | 10 | none |
| Mosquito | 2 | 7 | 95 | 25 | none |
| Firefly | 2 | 9 | 55 | 60 | none |
| Wasp | 1 | 10 | 75 | 45 | contact damage |

### Tongue record

| Field | Meaning |
| --- | --- |
| `active` | whether tongue is running |
| `timer` | phase timer |
| `phase` | `idle`, `extend`, `hold`, `retract` |
| `ox,oy` | mouth origin |
| `tx,ty` | current tip |
| `length` | current length |
| `radius` | 6 px |

### Particle record

| Field | Meaning |
| --- | --- |
| `x,y,vx,vy` | motion |
| `radius` | visual size |
| `life,maxLife` | lifetime |
| `kind` | `catch`, `damage`, `tongue`, `spawn` |
| `color` | hex |

### Score record

| Field | Meaning |
| --- | --- |
| `score` | current run score |
| `combo` | current combo count |
| `maxCombo` | highest combo this run |
| `comboTimer` | seconds before combo decay |

### High score record

| Field | Meaning |
| --- | --- |
| `score` | final score |
| `timeMs` | survival time |
| `maxCombo` | best combo |
| `initials` | 3 characters |
| `difficulty` | `easy`, `normal`, `hard` |
| `date` | ISO date |

### Rosters

| Roster | Exact parts |
| --- | --- |
| Player states | `idle`, `move`, `aim`, `tongue`, `hurt`, `dead` |
| Bug types | `fly`, `mosquito`, `firefly`, `wasp` |
| Difficulty options | `easy`, `normal`, `hard` |
| Screens | `title`, `pause`, `gameOver`, `highScores` |
| HUD elements | health, score, combo counter |
| Effects | particles, hit flash |
| Traps | none |
| Pickups | none |
| Extra mechanics | none |

## 4.1 Catching System (Tier 1)

Tier 1 contains the full core loop: move, aim, tongue, catch, spawn, damage, game over.

### Player movement

| Rule | Number |
| --- | --- |
| Movement input | WASD or Arrow keys |
| Input vector | normalized diagonal |
| Acceleration | 1600 px/s² |
| Friction | 2200 px/s² |
| Normal max speed | 190 px/s |
| Easy max speed | 205 px/s |
| Hard max speed | 175 px/s |
| Player radius | 18 px |
| Bounds | clamp to safe bounds |

### Aim

| Rule | Number |
| --- | --- |
| Pointer aim | if pointer active, facing points from player to pointer |
| Keyboard aim | if no pointer and input nonzero, facing follows input vector |
| No input, no pointer | keep last facing |
| Default facing | π/2, south |

### Tongue

| Rule | Number |
| --- | --- |
| Input | Space, Enter, or left click |
| Cooldown normal | 0.35 s |
| Cooldown easy | 0.28 s |
| Cooldown hard | 0.42 s |
| Origin | player centre + 20 px facing |
| Max length | 140 px |
| Hit radius | 6 px |
| Extend duration | 0.12 s |
| Hold duration | 0.04 s |
| Retract duration | 0.10 s |
| Active hitbox | extend, hold, retract phases |
| Miss penalty | none except cooldown |
| Multiple hits | only first bug hit |

### Bug behaviour

| Bug | Behaviour |
| --- | --- |
| Fly | random heading every 1.2–2.2 s, wobble amplitude 15 px/s, bounce off bounds |
| Mosquito | heading every 0.8–1.6 s, perpendicular sine amplitude 25 px/s, bounce off bounds |
| Firefly | random heading every 1.5–2.5 s; if tongue active within 120 px, flee from tongue origin; bounce off bounds |
| Wasp | if distance to player > 260 px, patrol random heading; if within 260 px, chase player with turn rate 4 rad/s; bounce off bounds |

### Spawning

Initial run state for Normal:

| Entity | Initial |
| --- | --- |
| Player | centre 480,300 |
| Fly | 2 |
| Mosquito | 0 |
| Firefly | 0 |
| Wasp | 1 |
| Score | 0 |
| Combo | 0 |
| Health | 3 |

Spawn caps Normal:

| Cap | Number |
| --- | --- |
| Total bugs | 8 |
| Fly | 5 |
| Mosquito | 3 |
| Firefly | 1 |
| Wasp | 2 |

Spawn timers Normal:

| Type | Interval |
| --- | --- |
| Fly | 2.5 s |
| Mosquito | 4.0 s |
| Firefly | 12.0 s |
| Wasp | 7.0 s |

Spawn rules:

| Rule | Number |
| --- | --- |
| Spawn edge | random edge |
| Initial velocity | inward from edge |
| Safe distance | if spawn point within 120 px of player, offset along edge |
| Cap check | skip if type cap or total cap reached |
| RNG | use `ctx.rng` only |

### Catching

| Rule | Number |
| --- | --- |
| Hit test | segment-circle distance ≤ bug.radius + tongue.radius |
| Good bug caught | remove bug, spawn particles, play catch sound |
| Wasp caught | remove wasp, spawn particles, play wasp catch sound |
| Tier 1 score effect | score remains 0 until Tier 2 |
| Tier 1 combo effect | combo remains 0 until Tier 2 |

### Damage and failure

| Rule | Number |
| --- | --- |
| Damage source | wasp contact only |
| Contact test | distance ≤ player.radius + wasp.radius |
| Damage | health -= 1 |
| Invulnerability | 1.5 s |
| Hit flash | 0.25 s |
| Combo reset | Tier 2 and later |
| Wasp on damage | remove wasp |
| Wasps during invulnerability | bounce away, no damage |
| Game over | health ≤ 0, set `mode = 'gameOver'`, stop spawning, set player dead |

## 4.2 Scoring System (Tier 2)

Tier 2 adds the supporting scoring system.

### Points

| Bug | Base points |
| --- | --- |
| Fly | 10 |
| Mosquito | 25 |
| Firefly | 60 |
| Wasp | 45 |

### Combo

| Rule | Number |
| --- | --- |
| Any catch | combo += 1 |
| Max combo tracking | `maxCombo = max(maxCombo, combo)` |
| Combo timer | 5.0 s |
| Timer reset | every catch |
| Timer expiry | combo = 0 |
| Damage | combo = 0 |
| Miss | no combo change |

### Multiplier

| Combo | Multiplier |
| --- | --- |
| 0–4 | 1 |
| 5–9 | 2 |
| 10–14 | 3 |
| 15–19 | 4 |
| 20+ | 5 |

Formula:

```text
multiplier = min(5, 1 + floor(combo / 5))
points = round(basePoints * multiplier)
score += points
```

### High scores

| Rule | Number |
| --- | --- |
| Max saved | 10 per difficulty |
| Storage key | `ribbit-snack.highscores.v1` |
| Sort | score desc, timeMs desc, maxCombo desc, date desc |
| Qualification | run score > 0 or qualifies into top 10 |
| Entry | 3 uppercase letters A-Z |
| Missing storage | fallback to session-only list |

## 4.3 Difficulty and Progression (Tier 3)

Difficulty options are settings, not mechanics. They change numeric parameters only.

### Difficulty presets

| Parameter | Easy | Normal | Hard |
| --- | --- | --- | --- |
| Health | 5 | 3 | 2 |
| Player speed | 205 | 190 | 175 |
| Tongue cooldown | 0.28 | 0.35 | 0.42 |
| Wasp speed base | 55 | 75 | 100 |
| Wasp turn rate | 3 rad/s | 4 rad/s | 5 rad/s |
| Total cap base | 6 | 8 | 10 |
| Wasp cap base | 1 | 2 | 3 |
| Spawn interval multiplier | 1.6 | 1.0 | 0.75 |

### Endless progression

| Rule | Number |
| --- | --- |
| Progression level | `floor(runTimeSec / 30)` |
| Spawn interval multiplier | `pow(0.92, level)` |
| Minimum interval multiplier | 0.35 |
| Wasp speed addition | `min(60, 4 * level)` |
| Total cap addition | `min(4, floor(level / 2))` |
| Wasp cap addition | `min(2, floor(level / 3))` |
| Good bug speed addition | `min(30, 2 * level)` |

### Run shape

| Time | Expected pressure |
| --- | --- |
| 0–20 s | learn controls, catch flies, catch first wasp |
| 20–60 s | combo building, wasp pressure begins |
| 60–180 s | multiple wasps, tighter spawn intervals |
| 180 s+ | survival pressure; score depends on risk management |

## 4.4 Run Structure

1. Player starts at title.
2. Player selects difficulty if Tier 3 is enabled; otherwise Normal.
3. Run starts with initial bugs and health.
4. Bugs move around the scene.
5. Player moves and shoots tongue.
6. Catching bugs increases score after Tier 2.
7. Wasp contact removes one life.
8. Health 0 ends the run.
9. Game over shows score and survival time.
10. High score entry appears if qualified after Tier 2.
11. Player can restart or return to title.

## 4.5 Feel

The game should feel bouncy and immediate. The frog accelerates quickly but stops cleanly. The tongue is a short, snappy line. Bugs pop into particles when caught. Wasps feel threatening because they chase, but they are always catchable with a short tongue shot. Damage is clear through a white flash and health loss. Nothing in the system punishes movement or curiosity except wasp contact.

---

# 5. CHARACTERS

## Frog

Silhouette: rounded body, two eye bumps, wide mouth wedge, tiny leg bumps.

| State | Gameplay meaning | Visual rules |
| --- | --- | --- |
| `idle` | no input, no tongue | bob amplitude 2 px, period 0.6 s |
| `move` | input active | squash along velocity, foot bumps alternate |
| `aim` | pointer or facing changed | rotate smoothly, mouth wedge points facing |
| `tongue` | tongue active | mouth opens, tongue drawn |
| `hurt` | invuln active | flash white, scale 1.05, blink every 0.15 s |
| `dead` | game over | rotate 180°, mouth X, no input |

Animation names:

| Animation | Motion rules |
| --- | --- |
| `frog_idle_bob` | vertical sine, disabled if reduced motion |
| `frog_move_squash` | scale x/y inverse, 0.18 s cycle |
| `frog_aim_rotate` | facing angle, no extra motion |
| `frog_tongue_open` | mouth wedge opens, tongue line follows phase |
| `frog_hurt_flash` | white overlay and scale pop |
| `frog_dead_flip` | rotate to 180° over 0.4 s |

Facings: full 360° rotation. No sprite sheet required.

## Bugs

Silhouette rules:

| Bug | Silhouette |
| --- | --- |
| Fly | oval body, two round wings, short legs |
| Mosquito | thin body, long proboscis, dotted abdomen |
| Firefly | round body, star-shaped glow, tiny antennae |
| Wasp | pointed abdomen, triangular stinger, black stripes, small wings |

Animations by name:

| Animation | Motion rules |
| --- | --- |
| `fly_hover` | slight vertical bob, wing flicker 12 Hz |
| `mosquito_zig` | body rotates along sine, proboscis points forward |
| `firefly_flicker` | glow alpha pulses 2 Hz |
| `wasp_chase` | slight body tilt toward velocity, stinger pulses |
| `bug_catch_pop` | scale to 1.3 then remove, particles |
| `wasp_damage_pop` | orange particles, remove wasp |

Bug facings: velocity heading. Wasps visually point toward player while chasing.

States gameplay needs:

| State | Meaning |
| --- | --- |
| `alive` | active bug |
| `caught` | removed after tongue hit |
| `damaged` | removed after player damage |

---

# 6. AUDIO

| Sound | Recipe | When it plays |
| --- | --- | --- |
| `music_title` | square arpeggio A3-C4-E4, 90 BPM, 4 bars, triangle bass, noise hat | title screen |
| `music_play` | square lead C4-E4-G4-A4, 120 BPM, triangle bass, noise hats, short loops | playing |
| `music_stop` | fade square lead over 0.2 s | pause, game over |
| `ui_hover` | square 880 Hz, 20 ms, volume 0.2 | UI focus/hover |
| `ui_select` | square 1200 Hz, 40 ms, volume 0.35 | start, restart, high scores |
| `ui_back` | square 600 Hz, 30 ms, volume 0.30 | back to title |
| `tongue_shoot` | square 300→900 Hz sweep, 70 ms, volume 0.35 | tongue launch |
| `tongue_miss` | noise, lowpass 1800 Hz, 120 ms, volume 0.15 | tongue ends with no hit |
| `catch_fly` | square 660 Hz 50 ms, then 880 Hz 50 ms | fly caught |
| `catch_mosquito` | square 784→988 Hz arpeggio, 80 ms | mosquito caught |
| `catch_firefly` | triangle 1046/1318/1568 Hz sparkle, 120 ms | firefly caught |
| `catch_wasp` | sawtooth 440→220 Hz buzz, 90 ms | wasp caught |
| `combo_up` | square 660/880/1100 Hz quick arpeggio, 80 ms | combo reaches 5,10,15,20 |
| `damage` | sawtooth 180→60 Hz, 220 ms, noise burst | player loses life |
| `game_over` | square descending 880/660/523/392 Hz, 500 ms | health reaches 0 |
| `high_score` | square fanfare 523/659/784/1046 Hz, 400 ms | qualifies for high score |

---

# 7. UX

UI is HTML/CSS only. The canvas renders the game world only. Screens are overlays. There is no settings screen. Difficulty and reduced motion controls live on title and pause.

## Screen state machine

| Current screen | Input | Next screen |
| --- | --- | --- |
| `title` | Start | `playing` |
| `title` | High Scores | `highScores` |
| `highScores` | Back | `title` |
| `playing` | Escape | `pause` |
| `pause` | Resume | `playing` |
| `pause` | Restart | `playing` |
| `pause` | Quit | `title` |
| `playing` | health 0 | `gameOver` |
| `gameOver` | Restart | `playing` |
| `gameOver` | High Scores | `highScores` |
| `gameOver` | Title | `title` |
| `highScores` | Escape | `title` |

## Screens

| Screen | Required controls | Notes |
| --- | --- | --- |
| Title | Start, difficulty selector, high scores, reduced motion toggle | Tier 1: Start only. Tier 2: High Scores. Tier 3: difficulty/reduced motion. |
| Pause | Resume, Restart, Quit, reduced motion toggle | Tier 1 minimal. Tier 3 settings. |
| Game Over | Restart, Title, High Scores, initials entry if qualified | Tier 1 minimal score/time. Tier 2 high score entry. |
| High Scores | Back | Tier 2. Lists top 10 for selected difficulty. |

## HUD

| Element | Record field | When visible |
| --- | --- | --- |
| Health hearts | `ctx.player.health` | `playing`, `paused` |
| Score | `ctx.score` | `playing`, `paused`; Tier 1 shows 0 |
| Combo counter | `ctx.combo` | `playing` when `combo > 0`; Tier 1 shows 0 |

## Accessibility UI

| Requirement | Implementation |
| --- | --- |
| Keyboard navigation | all buttons focusable, Enter activates, Escape pauses/back |
| Reduced motion | toggle on title/pause; disables idle bob, flicker, particles above 4, full-screen flash alpha |
| Colour-blind safety | high-contrast text, bug shape/pattern, never colour-only |
| Difficulty options | Easy, Normal, Hard on title after Tier 3 |

---

# 8. DEBUG API

| Function | Purpose |
| --- | --- |
| `debug.setMode(mode)` | set `ctx.mode` |
| `debug.setInput({left,right,up,down,tongue})` | set input keys directly |
| `debug.setPointer(x,y,active)` | set pointer |
| `debug.pressTongue()` | set `ctx.input.tonguePressed = true` |
| `debug.setPlayer(partial)` | merge into `ctx.player` |
| `debug.setBugs(array)` | replace `ctx.bugs` |
| `debug.spawnBug(type, edge)` | call catching spawn directly |
| `debug.setHealth(n)` | set player health |
| `debug.setScore(n)` | set score |
| `debug.setCombo(n)` | set combo |
| `debug.setDifficulty(name)` | set difficulty and reset run params |
| `debug.setReducedMotion(boolean)` | set settings |
| `debug.catchingState()` | return player, tongue, bugs, spawn state |
| `debug.scoringState()` | return score, combo, maxCombo, comboTimer, highScores |
| `debug.inputState()` | return input state |

---

# 9. TESTS

| Test | Tier | Procedure | Pass condition |
| --- | --- | --- | --- |
| T1-01 fixed loop determinism | 1 | Start seeded run, step 300 frames. | Same state hash for same seed. |
| T1-02 player bounds | 1 | Input toward corner for 5 s. | Player remains inside safe bounds. |
| T1-03 tongue input edge | 1 | Press tongue, run one frame. | Tongue becomes active and edge is consumed. |
| T1-04 tongue catch | 1 | Place Fly in tongue path. | Bug removed, particles created, no crash. |
| T1-05 wasp damage | 1 | Place Wasp at player. | Health decreases once, invuln starts, wasp removed. |
| T1-06 game over | 1 | Set health 1, trigger damage. | Mode becomes `gameOver`, player dead. |
| T1-07 spawn caps | 1 | Force many spawn attempts. | Caps never exceeded. |
| T1-08 HUD health | 1 | Damage player. | HUD hearts update. |
| T2-01 score table | 2 | Catch each bug type. | Score increases by base points. |
| T2-02 combo multiplier | 2 | Set combo 5, catch Fly. | Score increases by 20. |
| T2-03 combo timeout | 2 | Set combo 5, wait 5.1 s. | Combo becomes 0. |
| T2-04 damage resets combo | 2 | Set combo 5, damage player. | Combo becomes 0. |
| T2-05 high score sort | 2 | Save multiple scores. | List sorted by score, time, maxCombo. |
| T2-06 high score persistence | 2 | Save score, reload storage. | Stored record loads. |
| T3-01 difficulty parameters | 3 | Start Easy/Hard. | Health, speed, cooldown, caps match config. |
| T3-02 reduced motion | 3 | Enable reduced motion, trigger catch/damage. | Particles reduced, no idle bob/flicker. |
| T3-03 contrast check | 3 | Measure text/HUD colours. | Text contrast ≥ 4.5:1. |
| T3-04 screen state machine | 3 | Traverse title/pause/game over/high scores. | Only allowed transitions occur. |

---

# 10. BUILD ORDER

1. Create HTML/CSS shell, canvas, HUD, four screen overlays.
2. Build context, config, seeded RNG, fixed loop.
3. Implement input into `ctx.input`.
4. Implement player movement, bounds, facing.
5. Implement tongue state machine and hit testing.
6. Implement Fly and Wasp records, spawning, movement, bounds.
7. Implement catch removal, particles, hit flash, damage, game over.
8. Implement flat vector rendering for frog, tongue, bugs, HUD, screens.
9. Implement chiptune music and required bleeps.
10. Build Tier 1 definition of done and tests.
11. Implement scoring, combo, multiplier.
12. Implement Mosquito and Firefly.
13. Implement high scores storage, game over entry, high scores screen.
14. Implement difficulty presets and endless progression.
15. Implement reduced motion and accessibility controls.
16. Run all tier tests and fix regressions.

---

# 11. DEFINITION OF DONE

## Tier 1

High-level: A player can start from title, play a seeded Normal endless run, move freely, aim with keyboard or pointer, shoot a tongue, catch flies, avoid or catch wasps, lose lives, see health, and reach game over. The game is flat vector, saturated, hand-lettered, chiptune, with particles and hit flash.

- [ ] Fixed 60 Hz loop with deterministic seeded RNG.
- [ ] Canvas is 960×600 top-down one screen.
- [ ] Player moves with WASD/Arrows and clamps to safe bounds.
- [ ] Facing follows pointer or movement.
- [ ] Space/Enter/click launches tongue.
- [ ] Tongue has correct length, radius, phases, cooldown.
- [ ] Fly spawns, moves, bounces, can be caught.
- [ ] Wasp spawns, chases, damages on contact, can be caught.
- [ ] Spawning respects caps.
- [ ] Damage reduces health, triggers flash, starts invulnerability.
- [ ] Health 0 enters game over.
- [ ] HUD health visible.
- [ ] Score and combo HUD elements exist but remain 0.
- [ ] Particles and hit flash present.
- [ ] Title, minimal pause, minimal game over present.
- [ ] Chiptune music and required SFX play.
- [ ] Tier 1 tests pass.

## Tier 2

High-level: The game records and rewards performance. Score, combo, multiplier, additional bugs, and high scores work.

- [ ] Fly, Mosquito, Firefly, Wasp all present.
- [ ] Catching awards correct base points.
- [ ] Combo increments on any catch.
- [ ] Combo timer is 5 s.
- [ ] Damage resets combo.
- [ ] Multiplier caps at 5.
- [ ] HUD score and combo update live.
- [ ] Game over shows final score and survival time.
- [ ] High scores save top 10 per difficulty.
- [ ] Initials entry appears only when qualified.
- [ ] High scores screen lists saved scores.
- [ ] Tier 2 tests pass.

## Tier 3

High-level: Required accessibility and difficulty options are present without adding mechanics.

- [ ] Easy, Normal, Hard options selectable from title.
- [ ] Difficulty changes health, speed, cooldown, wasp speed, caps, intervals.
- [ ] Reduced motion toggle present on title and pause.
- [ ] Reduced motion disables nonessential motion and heavy particles.
- [ ] Colour-blind safe shapes and patterns remain enforced.
- [ ] UI remains exactly title, pause, game over, high scores.
- [ ] Tier 3 tests pass.

---

# A. SANITY

| Check | Result |
| --- | --- |
| All requested high-level decisions are addressed | Valid. Section 0.1 maps every decision to sections. |
| Core mechanics are exactly catching | Valid. `# 4.1` is the only core gameplay system. |
| Supporting mechanics are exactly scoring | Valid. `# 4.2` is the only supporting system. |
| Extra mechanics are none | Valid. No traps, pickups, power-ups, obstacles, hunger, or separate hazard system. |
| Failure is lose a life | Valid. Wasp contact removes one life; health 0 ends run. |
| Endless with no win | Valid. No win state; game over only on health 0. |
| One screen, a few minutes | Valid. Fixed 960×600 screen; difficulty ramp designed for typical 2–5 minute runs. |
| HUD exactly health, score, combo | Valid. No timer or extra HUD elements. |
| Screens exactly title, pause, game over, high scores | Valid. Settings are inside title/pause, not a new screen. |
| Effects exactly particles and hit flash | Valid. Removed screen shake and other effects. |
| Accessibility includes colour-blind safe palette, reduced motion, difficulty options | Valid. Palette uses shape/pattern; reduced motion and difficulty are specified. |
| Tier 1 is core only and guaranteed buildable | Valid. Tier 1 uses only Fly/Wasp and a score stub. |
| Tier 2 does not depend on Tier 3 | Valid. Scoring does not require difficulty or reduced motion. |
| Tier 3 adds no mechanics | Valid. It only changes settings and numeric parameters. |
| Contracts include all record fields needed by gameplay | Valid. Global context includes player, bugs, tongue, particles, scoring, high scores, input. |
| Tests cover each tier | Valid. Tier 1/2/3 tests are listed. |
| Corrections made | Fixed: removed considered screen shake because effects list only allows particles and hit flash. Fixed: removed considered health decay because it would be an extra survival system; failure is wasp contact only. Fixed: merged hostile bug behaviour into the catching system to avoid adding a separate hazard system. |