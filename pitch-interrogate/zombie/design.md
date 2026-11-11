# CURB APPEAL — Design Specification
### *Backwards Project Zomboid. You are the zombie. Keep the brains coming.*

Working title is the interrogator's; the pitcher has not named the game.

# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| "a zombie survival game" | The player is a zombie whose survival is a brains meter that never stops draining (§4.1) |
| Play as the zombie; the goal is to survive | §4.1, §4.15 |
| Hunt humans for brains to eat | §4.3 humans, §4.4 grab and eat |
| Humans are dumb and about as fast as you; catching is stealth | §4.2 sneak, §4.3 senses |
| Build from junk found around | §4.5 junk, §4.6 building |
| Ramshackle traps that somehow still catch people | §4.7 traps, Buildables roster |
| Lures: free wifi sign with a jammer, banana stand with a stack of money and a pit, free puppies | §4.8, §4.10 |
| Brain rot cleaning station that sucks the brain out | §4.10 |
| A fridge; harvest brains from trapped humans for later | §4.9 |
| Trapped humans stay in the trap until you walk over, and they make noise | §4.7 |
| Witnesses matter | §4.3 witnesses, §4.11 heat |
| Heat from people caught or killed: locals go missing, a cop investigates, more police, national guard | §4.11, §4.12 |
| Weapons for the armed humans | §4.13 |
| A ramshackle decayed mansion with a fetid pool; decorating for its own sake | §4.14 |
| A small map, a road the build area is off of, everyone comes from off map, 2 to 4 people at a time | §3 Space, §4.3 spawning |
| No ending, no day and night, no day counter | §4.15 |
| One meter: brains is hunger and health | §4.1 |

## 0.2 Decisions

N = ruled by the pitcher. C = ruled by the interrogator to make the pitch buildable.

| Decision | Ruling | By |
| --- | --- | --- |
| View | 2D, top-down, one fixed screen, no scrolling | C |
| Time | Real-time, fixed 60 Hz step | C |
| Tone | Silly. Everything the zombie builds looks like it cannot work, and works | N |
| Failure | Brains meter reaches 0: game over, start again | N |
| Speeds | Zombie walks 120 px/s; a fleeing civilian runs 130 px/s, so a chase is lost | N (same speed), C (numbers) |
| Catching by hand | Come from outside the human's sight cone, sneak the last stretch, grab | N (stealth, dumb AI), C (cone and hearing) |
| Why build | Hand hunting feeds you unreliably; traps and lures make brains steady | N |
| Baited box trap | The Box on a Stick has a latte under it and tempts passers-by a little | C |
| Buildings | A building may lure, catch, store, or only decorate, and may do several | N |
| Junk | Four kinds: Cardboard, Rope, Scrap, Gizmos | C |
| Junk sources | Six fixed spots that refill, and one piece from every human eaten or harvested | C |
| Trapped humans | Wait in the trap and yell; eat on the spot or harvest the brain for the fridge | N |
| Brainless husk | A human the Brain Rot Station has emptied walks home happy and can never be a witness | C |
| Heat | Rises with people caught and with witnesses who get away; never falls; no clock | N (trigger), C (numbers) |
| Law | Lone cop, then police pairs, then national guard squads; they shoot; they are also food | N (ladder), C (rules) |
| Weapons | They stun; a stunned human can be grabbed from any side. Humans only ever die by being eaten | C |
| Free Donuts | A lure that works only on police | C |
| Mansion | Walls, a door and decor placed on the old foundation; walls block sight and bullets | N (mansion, decor), C (sight rule) |
| Humans on the map | 2 to 4 civilians at once | N |
| Score | Brains eaten, time undead, peak heat, home score; best brains eaten is saved | C |
| Art | Flat vector shapes drawn in code, no image files, every actor at least 28 px with a dark outline | C |
| Audio | Synthesised through `lib/audio.js` | C |
| Input | Keyboard to move and act, mouse to place buildings | C |

## 0.3 Tiers

| Tier | Name | What it adds | Done when |
| --- | --- | --- | --- |
| 1 | Day one | The lot and road, the zombie, the draining meter and starving, civilians crossing, sight and hearing, sneaking, grab and eat, junk spots, the build menu, the Box on a Stick trap with yelling, HUD, title and game over | A player can start, sneak up on a human and eat them, search junk, build a box trap that catches someone, and eventually starve to a game over screen with a score |
| 2 | Brains on tap | Free WiFi sign, Fridge with harvest, deposit and eat, Banana Stand, Brain Rot Station, Free Puppies | A player can lure people deep into the lot, bank brains in the fridge and live off it |
| 3 | The heat | Heat meter and levels, witnesses, flyers, the cop, police pairs, guard squads, bullets, weapons and stun, Free Donuts | Catching people brings the law, the law can kill the zombie, and the zombie can stun and eat the law |
| 4 | Home sweet home | Mansion walls and door that block sight and bullets, decor, home score | A player can build and decorate the mansion and hide the worst of it from the road |

Each tier is a complete game on top of the one before it. Tier 1 uses the final art style, sound and feel from the start.

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Thing | Value |
| --- | --- |
| Logical canvas | 1280 x 720, scaled to the window by `lib/canvas.js` (`createCanvas(canvas, { width: 1280, height: 720 })`) |
| Tile | 40 px. Grid is 32 columns x 18 rows. Tile (c, r) covers x from 40c, y from 40r |
| Origin | Top-left, x right, y down |
| Distances | px. Speeds px/s. Times in seconds |
| Simulation step | 1/60 s, fixed |
| Actor position | Centre point. Actors are circles for collision |
| Angles | Radians, 0 pointing right, growing clockwise on screen |

## 1.2 Important conventions

- One fixed-step loop: accumulate frame time, run whole 1/60 steps, at most 5 per frame.
- Update order each step: input, zombie, humans and law, lures and traps, puppies, bullets and weapons, heat, spawning, effects, then render.
- Every tunable number in this document lives in `src/tuning.js` under the name given in its table, and nowhere else.
- Random numbers come from one seeded `mulberry32` in `src/rng.js`. The seed is `Date.now()` at run start and can be set from the debug API.
- Buildings occupy whole tiles. Actors are not blocked by buildings except Wall tiles (§4.14) and the map edge for the zombie.
- Humans and law walk in straight lines between waypoints. There is no path-finding.
- Nothing is loaded from an image or sound file. Draw with canvas shapes; sound with `lib/audio.js`; keys and mouse with `lib/input.js`.
- Readability rule: every actor is at least 28 px across, has a 2 px outline of `#1B1B2A`, and is drawn over ground that differs clearly in lightness. Nothing important is told by colour alone: alarmed humans carry a "!", lured humans a phone or heart icon, trapped humans a "HELP!" bubble.
- Save data: `localStorage["curbAppeal.best.v1"]`, a single number. If storage fails, keep it in memory.

# 2. CONTRACTS

## 2.1 Module layout

```text
index.html
styles/game.css
src/main.js        boot, loop, screen changes
src/tuning.js      every number
src/rng.js         seeded random
src/state.js       the game context and newRun()
src/map.js         tile regions, junk spots, lamp posts, helpers
src/zombie.js      movement, sneak, meter, grab, eat, harvest
src/humans.js      civilians: spawn, routes, senses, alarm, flee, lured, trapped, husk
src/junk.js        junk spots, inventory
src/build.js       build menu state, placement rules, demolish, buildables roster
src/traps.js       box trap, pit, yelling
src/lures.js       tempt rolls, wifi sign, banana stand, donuts
src/station.js     brain rot station
src/puppies.js     free puppies
src/fridge.js      storage
src/heat.js        heat value and level
src/law.js         cop, police, guard, bullets
src/weapons.js     mailbox, gnome, stun
src/home.js        walls, door, decor, sight blocking, home score
src/render.js      all drawing
src/ui.js          HTML screens, HUD, build panel, prompt line
src/sound.js       named sounds over lib/audio.js
src/debug.js       window.debug
```

## 2.2 Global context

One object, `game`, created by `newRun()` in `src/state.js`.

| Field | Type | Start | Meaning |
| --- | --- | --- | --- |
| `screen` | string | `"title"` | `title`, `playing`, `paused`, `gameover` |
| `time` | number s | 0 | Time undead this run |
| `zombie` | Zombie | see record | The player |
| `humans` | Human[] | [] | Civilians and husks |
| `law` | Lawman[] | [] | Cops, police, guards |
| `bullets` | Bullet[] | [] | |
| `buildings` | Building[] | [] | Everything placed |
| `spots` | JunkSpot[] | 6 from roster | |
| `junk` | `{cardboard, rope, scrap, gizmo}` | all 0 | Carried junk |
| `carriedBrains` | number | 0 | 0 to 3 |
| `heat` | number | 0 | |
| `heatLevel` | number | 0 | 0 to 3 |
| `brainsEaten` | number | 0 | Score |
| `peakHeatLevel` | number | 0 | |
| `buildMode` | `{open, tab, selected}` | closed | |
| `weapon` | `{id, uses}` or null | null | |
| `effects` | `{particles, texts, shake}` | empty | |
| `settings` | `{volume, reducedMotion}` | 0.6, browser preference | |
| `lastHurtBy` | string | `""` | `bullet` if shot in the last 3 s |

## 2.3 Module specifics

| Module | Functions |
| --- | --- |
| `zombie.js` | `stepZombie(dt)`, `tryGrab()`, `tryInteract()`, `hurt(amount, by)`, `feed(amount)` |
| `humans.js` | `spawnCivilian(kind, side)`, `stepHumans(dt)`, `alarm(h, cause)`, `canSee(h, x, y)`, `canHear(h, x, y, radius)`, `removeHuman(h, how)` |
| `junk.js` | `searchSpot(spot)`, `addJunk(type, n)`, `canAfford(cost)`, `pay(cost)`, `refund(cost)` |
| `build.js` | `BUILDABLES`, `canPlace(id, col, row)`, `place(id, col, row)`, `demolish(b)`, `buildingAt(col, row)` |
| `traps.js` | `stepTraps(dt)`, `trap(b, h)`, `releaseFrom(b)`, `yell(x, y, radius)` |
| `lures.js` | `stepLures(dt)`, `tempt(b, h)` |
| `station.js` | `stepStations(dt)` |
| `puppies.js` | `stepPuppies(dt)` |
| `fridge.js` | `deposit(f)`, `eatFrom(f)`, `fridgeWithSpace(x, y)` |
| `heat.js` | `addHeat(n, why)`, `levelFor(heat)` |
| `law.js` | `stepLaw(dt)`, `spawnLaw(kind, side)`, `fire(l)`, `stepBullets(dt)` |
| `weapons.js` | `craft(id)`, `useWeapon()`, `stun(target, seconds)` |
| `home.js` | `sightBlocked(x1, y1, x2, y2)`, `homeScore()` |

Every field a rule below names exists in `game` or on the record it names.

# 3. VISUAL SPEC

Flat vector, top-down, dusk. The top of the screen is a tidy suburban street in clean pastels. Everything below the sidewalk is yours: a dead lawn in grey-green, a cracked foundation, and whatever you have nailed together. Humans are bright and clean. The zombie and everything it builds is wonky: lines a few degrees off, tape, mismatched colours.

## Lighting and atmosphere

No lighting model. A fixed dusk tint: the ground colours below are final. Lamp posts on the sidewalk draw a soft yellow circle of radius 60 at 15% opacity. A cop's flashlight is a pale yellow wedge.

## Space

| Region | Tiles (columns, rows) | Walkable | Buildable | Drawn as |
| --- | --- | --- | --- | --- |
| Backdrop | 0 to 31, row 0 | no | no | Neighbours' fences and hedges |
| Road | 0 to 31, rows 1 to 2 | yes | no | Asphalt `#4A4E5A`, dashed centre line |
| Sidewalk | 0 to 31, row 3 | yes | no | Concrete `#C9C6BD`, slab lines |
| Front yard | 0 to 31, rows 4 to 8 | yes | yes | Dead lawn `#8A9A6B` with darker tufts |
| Back lot | 0 to 31, rows 9 to 17 | yes | yes | Darker dead lawn `#6F7F58` |
| Foundation | 12 to 19, rows 11 to 15 | yes | yes | Cracked slab `#9A948A`, inside the back lot |

| Fixture | Tile | Notes |
| --- | --- | --- |
| Lamp post A, B, C | (6, 3), (16, 3), (26, 3) | Flyers appear on them at heat level 1 |
| Trash Can A | (4, 4) | Junk spot |
| Trash Can B | (27, 4) | Junk spot |
| Dumpster | (0, 10) | Junk spot, drawn 2 tiles wide over (0, 10) and (1, 10) |
| Recycling Bin | (30, 9) | Junk spot |
| Junk Pile | (6, 15) | Junk spot |
| Shed Wreck | (25, 15) | Junk spot |
| Zombie start | centre of (16, 10) | |

Fixture tiles cannot be built on.

## Palette

| Name | Hex | Used for |
| --- | --- | --- |
| Outline | `#1B1B2A` | All outlines, text shadows |
| Zombie | `#7BC96F` | Zombie body |
| Zombie dark | `#3E7A3A` | Zombie arms, puppies |
| Brain | `#FF8FB1` | Brains, meter fill |
| Local | `#FF8A5B` | Local's shirt |
| Jogger | `#4FC3F7` | Jogger's shirt |
| Phone Guy | `#FFD54F` | Phone Guy's shirt |
| Shopper | `#C77DFF` | Shopper's shirt |
| Skin | `#F2C9A1` | Human heads |
| Police | `#27408B` | Cop and police uniforms |
| Guard | `#556B2F` | Guard uniforms |
| Alarm | `#FF3B30` | "!" marks, alarmed sight cones, bullets |
| Cardboard | `#B98B5E` | Cardboard things |
| Scrap | `#8D99A6` | Metal things |
| Rope | `#D9C27A` | Rope, tape |
| Gizmo | `#58D6C9` | Electronics, wifi waves |
| Fetid | `#5E7D2E` | Pool water |
| Panel | `#20222E` | UI panels, 90% opaque |
| Text | `#F5F3E7` | UI text |

## Visual recipe table

| Thing | Size | Recipe |
| --- | --- | --- |
| Zombie | 30 px | Circle body in Zombie, two short Zombie dark arms held forward in the facing direction, one eye bigger than the other, body tilts 8 degrees side to side while walking. Sneaking: body squashed to 80% height and arms pulled in |
| Civilian | 28 px | Circle shirt in the kind's colour, smaller Skin circle head offset toward facing, kind prop (see roster) |
| Sight cone | per rules | A wedge from the human in the facing direction, white at 10% opacity; Alarm colour at 20% when alarmed. Always drawn for civilians and law, so the player can read where it is safe |
| Husk | 28 px | A civilian in grey `#A0A0A0` with spiral eyes and a small smile, walking slowly |
| Cop, police | 30 px | Police colour body, cap, yellow flashlight wedge |
| Guard | 32 px | Guard colour body, helmet, rifle line |
| Junk spot | 1 tile | Trash can: Scrap cylinder with lid. Dumpster: wide Scrap box. Recycling bin: Gizmo-coloured box. Junk pile: heap of mixed shapes. Shed wreck: collapsed Cardboard-coloured planks. Lid or top drawn open and darker while empty |
| Box on a Stick | 1 tile | Cardboard square tilted up on a Rope-coloured stick, a small white cup under it. Sprung: box flat on the ground, shaking, "HELP!" bubble |
| Free WiFi Sign | 1 tile | Crooked Cardboard sign on a post reading "FREE WiFi" with three Gizmo arcs pulsing; a small box with an antenna taped to the post |
| Banana Stand | 2 tiles wide | Wonky Cardboard booth with a yellow banana on the roof, a stack of green bills on the counter. The pit tile in front is a brown rug; sprung: a dark hole with eyes |
| Brain Rot Station | 1 tile | A recliner in Scrap with a colander helmet on a hose to a jar. Jar shows 0, 1 or 2 Brain blobs |
| Free Puppies | 1 tile | Cardboard box reading "FREE PUPPIES", two Zombie dark ears poking out. Puppies: 14 px Zombie dark ovals with tails |
| Fridge | 1 tile | Tall Scrap rectangle, door hanging off one hinge, Brain-coloured glow from the gap. A number 0 to 6 on the door |
| Free Donuts | 1 tile | Pink box on a stool reading "FREE DONUTS" |
| Wall | 1 tile | Mismatched Cardboard and Scrap planks nailed at angles |
| Door | 1 tile | A Wall with a crooked door shape and a doormat |
| Fetid Pool | 2 x 2 tiles | Fetid-colour rounded rectangle with bubbles and a floating rubber duck |
| Dead Flamingo | 1 tile | Grey-pink flamingo lying on its side on a wire leg |
| Crooked Sign | 1 tile | "HOME SWEET HOME" on a board at 15 degrees |
| Tombstone | 1 tile | Grey rounded slab with a mailbox flag |
| Flyer | 16 px | White rectangle on a lamp post with a face and "MISSING" |
| Bullet | 8 px | Alarm-colour dot with a short trail |
| Build ghost | per building | The building at 50% opacity, tinted green if placeable and red if not |

# 4. GAMEPLAY SPEC

You are a zombie on a dead lawn beside a quiet road. Your brains meter drains all the time, and when it is empty you are gone. People wander past along the sidewalk and sometimes cut across your yard. They are as fast as you once they run, so you sneak up behind them, grab them and eat. You search trash for junk and nail it into things that should not work: a box on a stick, a free wifi sign, a banana stand with a pit in front. Trapped people yell until you come for them, and anyone who hears and gets away is a witness. Every person who goes missing raises the heat, and the heat brings a cop, then more police, then the national guard, who shoot. You stun them with a mailbox on a stick and eat them too. There is no ending; you last as long as the brains keep coming.

## Records and rosters

### Zombie record

| Field | Start | Notes |
| --- | --- | --- |
| `x`, `y` | 660, 420 | Centre of tile (16, 10) |
| `r` | 15 | Collision radius |
| `facing` | 0 | Angle of last movement |
| `sneaking` | false | True while Shift is held |
| `brains` | 70 | 0 to 100 |
| `busy` | null | `{kind: "eat" or "harvest" or "search" or "fridge", t, target}` while an action runs; the zombie cannot move |
| `hitFlash` | 0 | Seconds of white flash left |

### Human kinds

| Kind | Share of spawns | Walk | Flee | Hears | Brain value | Drops | Prop |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Local | 35% | 60 | 130 | yes | 35 | 1 Cardboard | A parcel |
| Jogger | 20% | 100 | 130 | no (earbuds) | 35 | 1 Rope | Headband |
| Phone Guy | 25% | 50 | 130 | yes | 35 | 1 Gizmo | Phone held in front |
| Shopper | 20% | 55 | 130 | yes | 35 | 1 Scrap | Shopping bag of cans |

### Human record

| Field | Notes |
| --- | --- |
| `kind`, `x`, `y`, `r` (14), `facing`, `speed` | |
| `state` | `walking`, `shortcut`, `lured`, `using`, `alarmed`, `trapped`, `dragged`, `stunned`, `husk` |
| `route` | Waypoint list |
| `temptedBy` | Ids of buildings already rolled for, so each is rolled once |
| `luredTo` | Building id while lured |
| `timer` | State timer |

### Junk spots

| Spot | Cardboard | Rope | Scrap | Gizmo |
| --- | ---: | ---: | ---: | ---: |
| Trash Can A, B | 50% | 20% | 20% | 10% |
| Dumpster | 30% | 10% | 50% | 10% |
| Recycling Bin | 60% | 0% | 15% | 25% |
| Junk Pile | 20% | 45% | 35% | 0% |
| Shed Wreck | 0% | 30% | 40% | 30% |

### Buildables

Cost letters: C Cardboard, R Rope, S Scrap, G Gizmo, B one carried brain.

| Id | Name | Tier | Tab | Cost | Footprint | What it does |
| --- | --- | ---: | --- | --- | --- | --- |
| `box` | Box on a Stick | 1 | Traps | 2C 1R | 1 x 1 | Trap. Bait radius 110, tempt 35%. Holds 1. Yell radius 260 |
| `wifi` | Free WiFi Sign | 2 | Traps | 2C 2G | 1 x 1, plus a free standing tile directly below it | Lure. Radius 300, tempt 60% (Phone Guy 100%). Up to 3 people stand and stare at their phones for 6 s with senses off |
| `fridge` | Fridge | 2 | Traps | 3S 1G | 1 x 1 | Store. Holds 6 brains |
| `banana` | Banana Stand | 2 | Traps | 3C 2S 1R | 2 x 1, plus a pit tile directly below its left tile | Lure and trap. Radius 260, tempt 50% (Shopper 100%). The pit holds 1. Yell radius 130 |
| `station` | Brain Rot Cleaning Station | 2 | Traps | 3S 2G 1R | 1 x 1 | Lure and harvester. Radius 140, tempt 60%. Sits 3 s, then one brain goes in the jar (holds 2). No yell. Leaves a husk |
| `puppies` | Free Puppies | 2 | Traps | 2C 1R 1B | 1 x 1 | Lure and helper. Radius 200, tempt 70%. Two puppies drag the human to a fridge. Yell radius 260 the whole way |
| `donuts` | Free Donuts | 3 | Traps | 2C 1S | 1 x 1 | Lure for cops and police only. Radius 240, tempt 80%. They stand 5 s eating with senses off |
| `mailbox` | Mailbox on a Stick | 3 | Gear | 2S 1R | carried | Weapon. See §4.13 |
| `gnome` | Gnome on a Rope | 3 | Gear | 1S 2R | carried | Weapon. See §4.13 |
| `wall` | Wall | 4 | Home | 1C 1S | 1 x 1 | Blocks sight, bullets and walking. Home 1 |
| `door` | Door | 4 | Home | 1C | 1 x 1 | A wall the zombie can walk through. Home 1 |
| `pool` | Fetid Pool | 4 | Home | 2S 2R | 2 x 2 | Decor. Home 5 |
| `flamingo` | Dead Flamingo | 4 | Home | 1S | 1 x 1 | Decor. Home 2 |
| `sign` | Crooked Sign | 4 | Home | 1C | 1 x 1 | Decor. Home 2 |
| `tombstone` | Tombstone Mailbox | 4 | Home | 1S | 1 x 1 | Decor. Home 2 |

### Law roster

| Kind | From heat level | Group | Walk | Sight range, half-angle | Fires every | Damage | Shot range | Brain value | Grabbable |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| Cop | 1 | 1 | 50 | 300, 35 degrees | 1.2 s | 12 | 340 | 50 | From outside the cone, or stunned, or trapped |
| Police | 2 | 2 | 55 | 300, 35 degrees | 1.2 s | 12 | 340 | 50 | Same as cop |
| Guard | 3 | 3 | 60 | 340, 40 degrees | 0.9 s | 18 | 400 | 60 | Only stunned or trapped |

### Heat levels

| Level | Name | Heat | What arrives |
| ---: | --- | --- | --- |
| 0 | Quiet street | 0 to 5 | Civilians only |
| 1 | Flyers | 6 to 15 | Flyers on the lamp posts. One cop at a time |
| 2 | Police | 16 to 29 | Police in pairs, who also sweep the front yard |
| 3 | National Guard | 30 and up | Guard squads of three, who search the whole lot |

## 4.1 Brains meter — Tier 1

| Tuning name | Value |
| --- | ---: |
| `brainsMax` | 100 |
| `brainsStart` | 70 |
| `brainsDrain` | 0.6 per second |
| `eatTime` | 0.8 s |

- `brains` falls by `brainsDrain * dt` every step while the screen is `playing`.
- Eating adds the brain value and clamps to `brainsMax`. Anything over is wasted.
- Damage subtracts from the same meter.
- At `brains <= 0`: the zombie collapses for 1.2 s, then the screen becomes `gameover`.
- Under 25 the meter bar flashes and a low heartbeat sound plays once every 2 s.

## 4.2 Zombie movement and sneaking — Tier 1

| Tuning name | Value |
| --- | ---: |
| `zombieWalk` | 120 px/s |
| `zombieSneak` | 85 px/s |
| `walkNoise` | 90 px |
| `sneakNoise` | 0 px |

- W A S D or the arrow keys move in 8 directions at constant speed, normalised on diagonals. No acceleration.
- Holding Shift sneaks: slower and silent.
- The zombie is kept inside x 15 to 1265 and y 55 to 705, so it can walk the road, sidewalk, yard and lot but not the backdrop.
- The zombie cannot enter Wall tiles; it can enter Door tiles and every other building tile.
- While `busy` is set the zombie does not move. Any movement key pressed after the first 0.2 s of a search cancels the search. Eating and harvesting cannot be cancelled.

## 4.3 Humans — Tier 1

### Spawning

| Tuning name | Value |
| --- | ---: |
| `civiliansTarget` | 3 |
| `civiliansMax` | 4 |
| `spawnGap` | 4 s minimum between civilian spawns |
| `shortcutChance` | 0.35 |

- Once a second, if civilians on the map (not counting husks, trapped or dragged) number fewer than `civiliansTarget` and `spawnGap` has passed, spawn one. Never exceed `civiliansMax`. At run start spawn 2 at once.
- A civilian enters from the left edge (x = -20) or the right edge (x = 1300), chosen at random, on the sidewalk at y = 140. Joggers use the road at y = 100.
- Its route is a straight walk to the opposite edge, where it leaves the map and is removed.
- With `shortcutChance` (never for Joggers), the route cuts through the front yard: it walks the sidewalk to a random x between 240 and 1040, then to two random points in the front yard (x within 300 px of the previous point, y between 180 and 340), then back to the sidewalk and on to the exit.

### Senses

| Tuning name | Value |
| --- | ---: |
| `sightRange` | 240 px |
| `sightHalfAngle` | 45 degrees |

- A civilian sees the zombie when the zombie's centre is within `sightRange` and within `sightHalfAngle` of the civilian's facing, and no Wall blocks the line (§4.14).
- A civilian hears the zombie when the zombie is within `walkNoise` and is moving without sneaking. Joggers never hear.
- A civilian also sees a grab, an eating or a harvest that happens inside its sight cone, and hears a yell within the yell's radius.
- Civilians in the states `using`, `trapped`, `dragged`, `stunned` and `husk` sense nothing.

### Alarm, fleeing and witnesses

- Seeing or hearing the zombie, seeing a grab, or hearing a yell sets a civilian to `alarmed`: a red "!" appears, its cone turns red, it drops any lure, and it runs at its flee speed to the sidewalk and then to the nearer side edge.
- An alarmed civilian that leaves the map is a **witness**. A "WITNESS!" text shows at that edge. From Tier 3 this adds heat (§4.11).
- An alarmed civilian can still be grabbed if the zombie gets within grab range, and can still blunder into a trap.

## 4.4 Grab and eat — Tier 1

| Tuning name | Value |
| --- | ---: |
| `grabRange` | 36 px, centre to centre |

- Space, with a civilian within `grabRange` who is not `trapped`, `dragged` or `husk`: the zombie grabs and starts eating. `busy = {kind: "eat", t: eatTime}`. The human is held in place.
- When the timer ends: `feed(brain value)`, `brainsEaten += 1`, the human is removed, its drop is added to the junk carried with a floating "+1 Rope" text, and from Tier 3 `addHeat(1, "caught")`.
- Space next to a trapped human or a human in a pit eats them the same way and re-arms the trap.
- Space takes the nearest valid target. The prompt line always names what Space and E will do right now.

## 4.5 Junk and inventory — Tier 1

| Tuning name | Value |
| --- | ---: |
| `searchTime` | 1.0 s |
| `spotRefill` | 25 s |
| `junkCap` | 20 pieces in total |

- E within 44 px of a full junk spot starts a search. After `searchTime` the spot gives one piece chosen by its row in the junk spot table, shows it as floating text, and becomes empty for `spotRefill`.
- At `junkCap` nothing more is picked up and the prompt reads "Pockets full".
- The HUD shows the four counts at all times.

## 4.6 Building — Tier 1

- B opens and closes the build panel on the right edge. The game keeps running. While it is open, Space and E do nothing.
- The panel lists the buildables of the tiers built so far, by tab, each with its name, icon and cost. A cost the player cannot pay is shown in red.
- Clicking an entry or pressing its number selects it. The mouse then shows a ghost on the tile under the cursor.
- A placement is valid when every footprint tile is in the front yard or back lot, holds no building and no fixture, and the buildable's extra tile (standing tile or pit tile) is also free, buildable ground. The zombie may stand on the tile.
- Left click on a valid tile pays the cost and places the building at once. The ghost stays selected for another. Right click or Escape clears the selection.
- X with the cursor over a building demolishes it and refunds half of each cost, rounded down. A trap holding a human cannot be demolished.
- Gear entries are crafted on click and replace the weapon carried.

## 4.7 Traps — Tier 1

| Tuning name | Value |
| --- | ---: |
| `trapTrigger` | 20 px from the trap tile's centre |
| `yellEvery` | 2.5 s |
| `boxBaitRadius` | 110 px |
| `boxTempt` | 0.35 |
| `boxYell` | 260 px |

- **Bait.** The first time a civilian who is `walking` or `shortcut` comes within `boxBaitRadius` of an armed box, roll `boxTempt` once. On success the civilian becomes `lured` and walks straight to the box.
- **Springing.** Any civilian or lawman whose centre comes within `trapTrigger` of an armed trap is trapped, whatever state they were in: state `trapped`, held at the trap's centre. The trap is now sprung and catches nobody else.
- **Yelling.** A trapped human yells every `yellEvery`: a "HELP!" bubble, a sound, and `yell(x, y, radius)` alarms every sensing civilian within the radius and calls every lawman within twice the radius to investigate (§4.12).
- **Collecting.** Space eats the trapped human (§4.4). E harvests (§4.9) once a Fridge exists. Either way the trap re-arms.
- A trap holds its human for ever unless a lawman frees them.

## 4.8 Lures — Tier 2

| Tuning name | Value |
| --- | ---: |
| `wifiRadius`, `wifiTempt`, `wifiStand`, `wifiSlots` | 300 px, 0.6, 6 s, 3 |
| `bananaRadius`, `bananaTempt`, `bananaYell` | 260 px, 0.5, 130 px |

- **Tempting.** The first time a civilian who is `walking` or `shortcut` enters a lure's radius, roll its tempt chance once (the kind named in the roster always succeeds). A lure that is full or busy does not roll. On success the civilian is `lured` to that building and walks in a straight line to its target tile.
- A lured civilian still springs any armed trap whose trigger it crosses on the way. This is how a lure at the back of the lot feeds traps placed in front of it.
- **Free WiFi Sign.** The target is the standing tile below the sign. On arrival the civilian is `using` for `wifiStand`, facing the sign, with a phone icon over its head and its senses off. Up to `wifiSlots` stand side by side. Afterwards it walks back to the sidewalk and on to its exit, and is never tempted by that sign again.
- **Banana Stand.** The target is the pit tile. On arrival the civilian falls in: `trapped` in the pit, yelling at `bananaYell`. While the pit is full the stand tempts nobody.
- A wall tile on the straight line stops a lured civilian; after 1 s it gives up and returns to its route.

## 4.9 Fridge and harvesting — Tier 2

| Tuning name | Value |
| --- | ---: |
| `harvestTime` | 1.2 s |
| `carryMax` | 3 brains |
| `fridgeCap` | 6 brains |
| `storedBrainValue` | 35 |
| `fridgeEatTime` | 0.5 s |

- E next to a trapped human, with fewer than `carryMax` brains carried: harvest. After `harvestTime` the human is removed, `carriedBrains += 1`, the drop is added, the trap re-arms, and `addHeat(1, "caught")`.
- E within 44 px of a Fridge deposits as many carried brains as fit.
- Space within 44 px of a Fridge holding at least one brain eats one: after `fridgeEatTime`, `feed(storedBrainValue)` and `brainsEaten += 1`.
- Q eats one carried brain on the spot, same time and value.
- The number on the fridge door and the carried-brain slots on the HUD always show the counts.

## 4.10 Brain Rot Cleaning Station and Free Puppies — Tier 2

| Tuning name | Value |
| --- | ---: |
| `stationRadius`, `stationTempt`, `stationSit`, `stationJars` | 140 px, 0.6, 3 s, 2 |
| `huskSpeed` | 40 px/s |
| `puppyRadius`, `puppyTempt`, `puppyKneel`, `puppyDrag`, `puppyYell` | 200 px, 0.7, 1 s, 70 px/s, 260 px |

- **Station.** Tempts like a lure while it has a free jar and nobody is in the chair. The civilian sits, `using`, for `stationSit`. Then a jar fills, `addHeat(1, "caught")`, and the civilian stands up as a `husk`: grey, spiral-eyed, smiling. A husk walks at `huskSpeed` to the nearer edge and leaves. It senses nothing, is never a witness, cannot be eaten and springs no traps. The station never yells.
- E at the station takes jars into carried brains. Space at the station eats one jar.
- **Puppies.** Tempts like a lure while both puppies are home. The civilian walks to the box and kneels for `puppyKneel`. Then the puppies bite on and the civilian is `dragged` at `puppyDrag` toward the nearest Fridge with space, yelling at `puppyYell` on the usual yell timer the whole way.
- On reaching the fridge: one brain is stored, the human is removed, `addHeat(1, "caught")`, and the puppies trot home at 140 px/s. No junk is dropped.
- With no Fridge that has space, the puppies hold the human at the box as a trapped human until the zombie collects them.
- A lawman who reaches a dragged human frees them as from a trap, and the puppies run home.

## 4.11 Heat — Tier 3

| Event | Heat |
| --- | ---: |
| A civilian caught: eaten, harvested, emptied by the station or stored by puppies | +1 |
| A witness leaves the map | +3 |
| A cop, police officer or guard eaten or harvested | +2 |

- Heat never falls. `heatLevel` is read from the heat levels table and `peakHeatLevel` tracks the highest reached.
- On reaching a new level: a banner with the level's name for 3 s and a siren sound. At level 1, flyers appear on the three lamp posts.
- The HUD shows four badges, lit up to the current level, and the level's name.

## 4.12 The law — Tier 3

| Tuning name | Value |
| --- | ---: |
| `lawGap` | Cop 20 s, Police 15 s, Guard 30 s after the last group has left or been eaten |
| `investigateSpeed` | 80 px/s |
| `freeTime` | 2 s |
| `bulletSpeed` | 420 px/s |
| `loseSightAfter` | 3 s |

- Only the highest kind the heat level allows is on the map, one group at a time. A group spawns `lawGap` after the previous one is gone.
- **Patrol.** A group enters from a random side on the sidewalk and walks to the other end and back, twice, pausing 2 s at each lamp post, then leaves. Police also walk a loop through the front yard on each pass (down to y = 300 at a random x, 300 px along, back up). Guards walk a search of the whole lot instead: sidewalk, then four random points in the yard and lot, then out. Group members keep 30 px apart.
- **Investigating.** A lawman called by a yell walks at `investigateSpeed` to where it came from, with a "?" over its head. If it comes within 30 px of a trapped or dragged human it frees them over `freeTime`: the human becomes `alarmed` and runs, the trap re-arms. If it finds nothing it waits 3 s and resumes patrol.
- **Shooting.** A lawman who sees the zombie (its own range and half-angle, not blocked by a Wall) stops, turns to face the zombie, and fires at its rate. Each shot is a bullet from the lawman toward where the zombie is at that moment, at `bulletSpeed`, removed at the shot range or on hitting a Wall. A bullet within 12 px of the zombie's centre hits: `hurt(damage, "bullet")`, hit flash 0.2 s, shake 6 px for 0.2 s.
- When the zombie has been out of sight for `loseSightAfter`, the lawman walks to the last place it saw the zombie, waits 2 s, and resumes.
- **Eating the law.** A cop or police officer can be grabbed with Space from outside its sight cone. Any lawman who is stunned or trapped can be grabbed. Eating or harvesting works as for civilians with the roster's brain value and +2 heat. A cop drops 1 Gizmo; a guard drops 2 Scrap.
- The law is never tempted by the civilian lures. It springs traps by walking into them.

## 4.13 Weapons, stun and Free Donuts — Tier 3

| Weapon | Use | Reach | Stun | Cooldown | Hits before it breaks |
| --- | --- | --- | ---: | ---: | ---: |
| Mailbox on a Stick | F swings in an arc of 120 degrees ahead | 60 px | 2.5 s | 0.6 s | 12 |
| Gnome on a Rope | F throws it ahead at 360 px/s; it comes back | 220 px | 3.5 s | 1.4 s | 8 |

- One weapon is carried. Crafting another replaces it. The HUD shows its icon and hits left. At 0 it breaks with a sound and is gone.
- A hit stuns the first human or lawman it touches. Stunned: stars over the head, no movement, no senses, no shooting, grabbable from any side for the stun time.
- A swing or throw seen by a sensing civilian alarms them.
- **Free Donuts** tempts cops and police like a lure with its own numbers. They walk to it and stand `using` for 5 s with senses off. Guards ignore it.

## 4.14 Mansion and decor — Tier 4

- Walls and Doors may be placed anywhere buildable; the foundation is where a mansion is meant to go, and placing there costs the same.
- `sightBlocked(x1, y1, x2, y2)` is true when the straight line between two points crosses any Wall or Door tile. Every sight test for civilians and the law uses it, and bullets stop at those tiles.
- Yells are not blocked by walls.
- Humans and the law cannot walk through Wall or Door tiles. One that walks into a wall stops, waits 1 s, and goes on to its next waypoint by walking along the wall's side to the nearer end. The zombie walks through Doors.
- Decor does nothing but count. `homeScore()` is the sum of the Home numbers in the buildables roster. It is shown on the pause and game over screens.

## 4.15 Run, score and game over — Tier 1

- A run starts from the title with `newRun()` and ends only when the meter empties.
- The game over screen shows: "You starved." or, if `lastHurtBy` is `bullet`, "They got you."; brains eaten; time undead as minutes and seconds; from Tier 3 the peak heat level's name; from Tier 4 the home score; and the best brains eaten ever, saved when beaten.

## Progression and difficulty

- The first minute: about 115 seconds of meter. One civilian by hand buys 58 more. The first box trap costs 2 Cardboard and 1 Rope, about three searches.
- Tier 2 turns the lot into a machine: a wifi sign behind two box traps, a fridge to bank the surplus.
- Tier 3 is the price: six catches bring the first cop, sixteen heat brings pairs, thirty brings the guard. Witnesses bring it three times faster, so traps beside the road cost more than traps behind the house.
- Tier 4 is the answer to Tier 3: walls hide what the patrols would otherwise see.

## Feel

- Grabbing snaps: the human freezes, a 0.1 s squash on the zombie, a crunch, then pink particles on the last frame of eating.
- Every trap spring has a comic thump and a 4 px shake for 0.15 s.
- Tempted humans show a small heart or phone icon the moment the roll succeeds, so the player sees the lure working.
- Floating text for every gain: "+35", "+1 Scrap", "WITNESS!".
- With reduced motion on: no shake, no particles; text and icons remain.

# 5. CHARACTERS

## The zombie

| State | Motion |
| --- | --- |
| idle | Slow 2 px bob, arms drooping |
| walk | Tilt 8 degrees each way, twice a second, arms forward |
| sneak | Squashed, arms in, tilt halved |
| eat, harvest, search | Hunched over the target, head bobbing four times a second |
| hurt | White for 0.2 s |
| collapse | Shrinks flat over 1.2 s |

## Humans and law

| State | Motion and mark |
| --- | --- |
| walking, shortcut | Small step bob |
| lured | Heart or phone icon over the head, walking straight |
| using | Standing, facing the building, icon over the head |
| alarmed | Red "!", arms up, fast step bob |
| trapped | Under the box or in the pit, "HELP!" bubble on each yell |
| dragged | Lying flat, a puppy on each ankle |
| stunned | Three stars circling the head |
| husk | Grey, spiral eyes, slow sway |
| law patrol | Flashlight wedge sweeping 20 degrees each way |
| law investigating | "?" over the head |
| law shooting | Facing the zombie, muzzle flash on each shot |

# 6. AUDIO

All through `lib/audio.js`. Music: `music.start(13, 96)` on entering play, stopped on game over.

| Name | Recipe | When |
| --- | --- | --- |
| `grab` | `sound({wave:'noise', from:900, to:200, ms:90, q:3, vol:0.3})` | A grab |
| `munch` | Four `sound({wave:'square', from:140, to:90, ms:60})` 0.2 s apart | While eating |
| `gulp` | `seq([[220,80],[330,120]], {wave:'triangle'})` | Eating finished |
| `search` | `noise(200, {from:1500, to:600, q:5, vol:0.2})` | Searching a spot |
| `gotJunk` | `tone(660, 80, 'square', 0.2)` | Junk gained |
| `place` | `sound({wave:'sawtooth', from:200, to:120, ms:140})` then `noise(60)` | A building placed |
| `denied` | `tone(110, 120, 'square', 0.2)` | Invalid placement, pockets full |
| `spring` | `sound({wave:'triangle', from:500, to:90, ms:220, vol:0.35})` | A trap springs |
| `yell` | `sound({wave:'sawtooth', from:700, to:500, ms:260, vol:0.25})` | Each yell |
| `alarm` | `seq([[880,70],[990,70]], {wave:'square', vol:0.25})` | A human becomes alarmed |
| `witness` | `seq([[400,120],[300,120],[200,240]], {wave:'sawtooth'})` | A witness leaves |
| `tempt` | `seq([[784,60],[988,90]], {wave:'triangle', vol:0.2})` | A lure roll succeeds |
| `slurp` | `sound({wave:'sine', from:200, to:900, ms:500, vol:0.3})` | The station takes a brain |
| `yip` | `tone(1200, 50, 'square', 0.15)` twice | Puppies bite on |
| `siren` | `sound({wave:'sine', from:600, to:900, ms:600})` twice | A new heat level |
| `shot` | `noise(70, {from:3000, to:500, q:2, vol:0.35})` | A lawman fires |
| `hurt` | `sound({wave:'square', from:180, to:80, ms:160, vol:0.35})` | The zombie is hit |
| `bonk` | `sound({wave:'triangle', from:300, to:120, ms:120, vol:0.35})` | A weapon hit |
| `break` | `noise(160, {from:1200, to:200, q:3})` | A weapon breaks |
| `hungry` | `tone(70, 160, 'sine', 0.3)` | Every 2 s under 25 brains |
| `gameover` | `seq([[330,200],[262,200],[196,500]], {wave:'triangle'})` | Collapse |

# 7. UX

HTML and CSS over one `<canvas id="game">`.

## Screens

| From | Event | To |
| --- | --- | --- |
| `title` | Enter or click Start | `playing`, after `newRun()` |
| `playing` | Escape or P | `paused` |
| `paused` | Escape, P or Resume | `playing` |
| `paused` | Restart | `playing`, after `newRun()` |
| `playing` | Meter empty and collapse finished | `gameover` |
| `gameover` | Enter or Retry | `playing`, after `newRun()` |
| `gameover`, `paused` | Title | `title` |

- **Title:** the name, the line "You are the zombie. Keep the brains coming.", a Start button, and the controls: WASD move, Shift sneak, Space grab and eat, E search and harvest, B build, mouse to place, F weapon, Q eat a carried brain, Esc pause.
- **Paused:** Resume, Restart, Title, a volume slider, a reduced motion checkbox, the home score.
- **Game over:** as §4.15, with Retry and Title.

## HUD

| Element | Record field | Where | When visible |
| --- | --- | --- | --- |
| Brains bar with number | `zombie.brains` | Top left, 260 x 24 | Playing |
| Carried brains, 3 slots | `carriedBrains` | Under the bar | From Tier 2 |
| Junk counts, 4 icons | `junk` | Top right | Playing |
| Heat badges and level name | `heat`, `heatLevel` | Top centre | From Tier 3 |
| Weapon icon and hits left | `weapon` | Bottom left | When a weapon is carried |
| Prompt line | Nearest valid action | Bottom centre | When Space, E or Q would do something |
| Build panel | `buildMode` | Right edge, 280 wide | While open |
| Banner | Heat level change | Centre, 3 s | On the change |

## Accessibility

- Reduced motion switches off shake and particles.
- Every state is marked with a shape or a word as well as a colour.
- All text is at least 16 px at the logical size, in Text colour on Panel colour or with an Outline shadow.

# 8. DEBUG API

`window.debug`, each function returning plain data.

| Function | Does |
| --- | --- |
| `debug.state()` | `{screen, time, brains, heat, heatLevel, brainsEaten, junk, carriedBrains, weapon}` |
| `debug.zombie()` | The zombie record |
| `debug.humans()` | Array of `{kind, x, y, state, facing}` |
| `debug.law()` | Array of `{kind, x, y, state}` |
| `debug.buildings()` | Array of `{id, col, row, holding, stored}` |
| `debug.spots()` | Array of `{name, full, refillIn}` |
| `debug.setBrains(n)` | Sets the meter |
| `debug.teleport(x, y)` | Moves the zombie |
| `debug.giveJunk(type, n)` | Adds junk |
| `debug.giveBrains(n)` | Adds carried brains |
| `debug.spawnHuman(kind, x, y, facing)` | Spawns a civilian standing still, facing that angle |
| `debug.spawnLaw(kind, x, y, facing)` | Spawns a lawman standing still |
| `debug.place(id, col, row)` | Places a building free of charge; returns whether it was valid |
| `debug.setHeat(n)` | Sets heat and the level |
| `debug.seed(n)` | Reseeds the random source |
| `debug.step(n)` | Runs n fixed steps |
| `debug.input(action, down)` | Holds or releases `up`, `down`, `left`, `right`, `sneak`, `grab`, `interact`, `build`, `weapon`, `eatCarried` |
| `debug.start()` | Starts a run from any screen |

# 9. TESTS

| Test | Tier | Steps | Passes when |
| --- | ---: | --- | --- |
| Meter drains | 1 | Start, step 600 | Brains is 70 - 6 = 64, within 0.1 |
| Starve | 1 | `setBrains(0.1)`, step 120 | Screen is `gameover` |
| Walk and sneak speeds | 1 | Hold right 60 steps; then with sneak | x grows by 120, then by 85 |
| Seen from the front | 1 | Human at (400,300) facing 0; zombie at (600,300) | Human becomes `alarmed` |
| Unseen from behind, sneaking | 1 | Human facing 0; zombie 100 px behind, sneaks to 30 px | Human stays `walking`; grab succeeds |
| Heard when walking | 1 | Zombie walks to 80 px behind a Local | `alarmed` |
| Jogger is deaf | 1 | Same with a Jogger | Not alarmed |
| Eat | 1 | Grab, step 48 | Brains +35, human gone, 1 junk of the kind's type, `brainsEaten` 1 |
| Search | 1 | Stand at Trash Can A, hold interact 60 steps | One junk gained, spot empty, full again after 25 s |
| Build a box | 1 | Give 2C 1R, `place("box", 10, 6)` by the panel | Junk spent, building exists |
| Invalid placement | 1 | Try the road tile (10, 2) | Refused, nothing spent |
| Box springs | 1 | Human walks over the box tile | `trapped`, trap sprung |
| Yell alarms | 1 | Second human 200 px from a trapped one, step 150 | Second is `alarmed` |
| Eat from trap | 1 | Space next to the trapped human | Eaten, trap armed again |
| Spawning bounds | 1 | Step 3600 with the zombie idle in a corner | Civilians on the map never exceed 4 |
| Wifi lures | 2 | Place wifi at (16, 12); Phone Guy enters its radius | Walks to the standing tile, `using` 6 s, senses off |
| Lure feeds a trap | 2 | Box on the line between sidewalk and sign | Lured human ends `trapped` in the box |
| Harvest and fridge | 2 | Harvest a trapped human, deposit, eat from fridge | Carried 1 then 0, fridge 1 then 0, brains +35 |
| Banana pit | 2 | Shopper enters radius | Ends `trapped` in the pit; stand tempts nobody while full |
| Station | 2 | Human sits 3 s | Jar 1, human is `husk`, no yell, husk leaves, no witness |
| Puppies | 2 | Fridge placed; human tempted | Dragged to the fridge, fridge +1, puppies home |
| Heat counts | 3 | Eat one civilian; let one alarmed civilian leave | Heat 1, then 4 |
| Levels | 3 | `setHeat(6)`, `setHeat(16)`, `setHeat(30)` | Level 1, 2, 3; a cop, a pair, a squad spawn in turn |
| Cop shoots | 3 | Zombie in a cop's cone at 200 px, step 120 | At least one bullet; brains fall by 12 per hit |
| Cop frees | 3 | Cop within 520 px of a yell | Walks to the trap, human freed and `alarmed` |
| Stun and eat a guard | 3 | Mailbox hit on a guard, then grab | Guard `stunned`, eaten, brains +60, heat +2 |
| Donuts | 3 | Cop enters the donut radius | Stands `using` 5 s, senses off |
| Walls block sight | 4 | Wall tile between a human and the zombie in its cone | Not alarmed |
| Walls stop bullets | 4 | Wall between a shooting cop and the zombie | No hit |
| Home score | 4 | Place a pool and a flamingo | `homeScore()` is 7 |

# 10. BUILD ORDER

1. Page, canvas at 1280 x 720, the map regions and fixtures drawn in the palette.
2. Loop, context, the zombie moving and sneaking inside the bounds.
3. The meter, its bar, starving, the game over screen with brains eaten and time.
4. Civilians: spawning, sidewalk routes, yard shortcuts, the four kinds, sight cones drawn.
5. Senses, alarm, fleeing, witnesses leaving.
6. Grab and eat with drops; the prompt line.
7. Junk spots, searching, the junk HUD.
8. The build panel, ghost, placement rules, demolish; the Box on a Stick with bait, springing, yelling and collecting.
9. Title, pause, sounds, music and feel. Tier 1 is done.
10. Free WiFi Sign and lure movement; the Fridge with harvest, deposit and eating.
11. Banana Stand, Brain Rot Station with husks, Free Puppies. Tier 2 is done.
12. Heat, levels, badges, banner, flyers.
13. The law: patrols, investigating, freeing, shooting, bullets.
14. Weapons, stun, eating the law, Free Donuts. Tier 3 is done.
15. Walls, Doors, sight and bullet blocking, decor, home score. Tier 4 is done.

# 11. DEFINITION OF DONE

## Tier 1 — Day one

- [ ] The lot, road, sidewalk, foundation, lamp posts and six junk spots are drawn and readable.
- [ ] The zombie moves, sneaks, and is plain to see at a glance.
- [ ] The meter drains, the bar shows it, and an empty meter ends the run on a game over screen with brains eaten and time undead.
- [ ] Two to four civilians are on the map, crossing on the sidewalk or through the yard, with their sight cones drawn.
- [ ] A civilian who sees or hears the zombie runs and leaves; one approached from behind while sneaking can be grabbed and eaten.
- [ ] Searching a junk spot gives junk and the spot refills.
- [ ] The build panel places a Box on a Stick for its cost on valid ground only.
- [ ] The box tempts some passers-by, springs, the human yells, the yell alarms others, and the zombie can eat the catch.
- [ ] Title, pause and game over work; every action has its sound.
- [ ] All Tier 1 tests pass.

## Tier 2 — Brains on tap

- [ ] The wifi sign draws people in and holds them with senses off; a trap on their line catches them.
- [ ] Harvesting, carrying, depositing and eating from the fridge work and show their counts.
- [ ] The banana stand lures and pits one person at a time.
- [ ] The station fills jars silently and leaves husks who walk away.
- [ ] The puppies drag a tempted human to a fridge and come home.
- [ ] All Tier 2 tests pass.

## Tier 3 — The heat

- [ ] Heat rises for catches and witnesses, the badges and level name follow, flyers appear.
- [ ] A cop, then pairs, then squads arrive at their levels, patrol, investigate yells and free the trapped.
- [ ] The law shoots the zombie on sight and each hit costs brains.
- [ ] Both weapons stun and wear out; stunned law can be eaten.
- [ ] Free Donuts holds cops and police.
- [ ] All Tier 3 tests pass.

## Tier 4 — Home sweet home

- [ ] Walls and doors can be placed, block sight, bullets and walking; the zombie uses doors.
- [ ] The five decor pieces can be placed and the home score counts them.
- [ ] All Tier 4 tests pass.

# A. SANITY

| Check | Result |
| --- | --- |
| Time to starve from the start | 70 / 0.6 = 117 s. One brain adds 35 / 0.6 = 58 s. The player needs a brain a minute |
| Can the zombie close on a walker while silent? | Sneak 85 against Local 60, Phone Guy 50, Shopper 55: closes at 25 to 35 px/s. From the 90 px hearing ring to the 36 px grab range is 54 px: about 2 s. Jogger at 100 cannot be caught by sneaking but is deaf, so walking at 120 closes at 20 px/s |
| Can the zombie run down a fleeing civilian? | No: 120 against 130. As pitched, a chase is lost |
| Time for a civilian to cross | 1320 px at 50 to 100 px/s: 13 to 26 s. With 3 on the map, roughly 8 arrivals a minute |
| Cost of the first trap | 2 Cardboard and 1 Rope. Trash cans give Cardboard half the time and the Junk Pile gives Rope 45% of the time: about 3 to 5 searches, and each eaten Local or Jogger gives one more |
| Does a box near the sidewalk overfeed? | It tempts 35% of those passing within 110 px and holds one until collected, and its yell (260 px) reaches the sidewalk, so each catch risks witnesses. Bounded by collection and, from Tier 3, by heat |
| Does a box at the back catch anyone without a lure? | No: the back lot is beyond every route. That is what the lures are for |
| Lure radii against the map | The sidewalk is at y = 140 and a tile in row r has its centre at y = 40r + 20. A wifi sign (300 px) reaches the sidewalk from as deep as row 10 (280 px away); a banana stand (260) from row 9 (240); puppies (200) from row 8 (200); the station (140) from row 6 (120). Deeper buildings need a chain |
| Yell and sight from the road | A yell of 260 px from a trap at row 10 (y = 420) reaches y = 160, just short of the sidewalk centre at 140. Traps from row 10 down are quiet to the street; traps in the front yard are not. Matches the pitch |
| Heat pace | Level 1 at 6: six clean catches, or two witnesses. Level 2 at 16, level 3 at 30. A careful player meets the cop after about six minutes |
| Bullet dodge | 420 px/s from 300 px away arrives in 0.7 s; the zombie moves 84 px in that time and the hit radius is 12 plus the body. Dodgeable by moving across the line |
| Guard without a weapon | Cannot be grabbed unless trapped. A guard's search route crosses the lot, so armed traps on it are the other answer |
| Every HUD field exists in the context | `zombie.brains`, `carriedBrains`, `junk`, `heat`, `heatLevel`, `weapon`, `buildMode`: all in §2.2 |
| Every buildable has a cost, a footprint and a rule | 15 entries; rules in §4.7 to §4.14 |
| File names | No module is named `world.js`, which the game folder already holds |
