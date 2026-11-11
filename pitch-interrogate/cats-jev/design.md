# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| A browser game: tower defense where cats defend a fish market. | Full spec |
| Player is the Forecat, organizer of a dawn fish market. | 4.1, 7, Characters |
| Player builds cat beds at stalls, crates, aisles, and angles. | 4.2, 4.3 |
| Cats automatically fight seagulls, rats, raccoons, and other thieves. | 4.4, 4.5 |
| Customers try to buy fish from open stalls. | 4.7 |
| Successful sales create coins, which buy more cats, repairs, and ability charges. | 4.7, 4.9 |
| Waves come down market aisles toward the Market Scale, crates, and exits. | 4.2, 4.6 |
| Stolen fish and blocked customers darken stalls, abandon positions, lower economy, and make later waves harsher. | 4.7, 4.8, 4.12 |
| Abilities are quick market tricks. | 4.9 |
| Scoring records how well the market was defended, not merely whether it survived. | 4.10 |
| Fixed oblique overhead view of the fish market floor. | 3, 7 |
| Real-time, with building and repair allowed before the first wave and after each wave is resolved. | 4.1 |
| Next wave begins when the market bell tolls the next count. | 4.1, 4.6 |
| Run starts by lifting the Closed sign and loading the Market Scale with the day’s stock. | 4.1, 7 |
| A wave breaks through when an enemy reaches the Market Scale or carries a fish crate to a market exit. | 4.4, 4.5 |
| Run ends when the Market Scale’s stock reaches zero and the Closed sign is hung. | 4.1, 7 |
| Harder as lost stock and lost customers scale later waves. | 4.12 |
| Darkened stalls and abandoned cat beds create gaps and weak points. | 4.3, 4.8 |
| Melting ice lowers sale value and attracts rats. | 4.7, 4.8 |
| Middle waves use distraction/draw-away patterns and larger thieves. | 4.6, 4.12 |
| Tone: wet dawn fish market, not a clean battlefield. | 3, 4.13, 5, 6 |
| The market is the target, the economy, and the stage. | 4.2, 4.7, 4.10 |
| Scoring keeps pressure clean: not just surviving, but defending the market well. | 4.10 |
| Failure shown through crates knocked open, ice melting, signs tilting, cat beds abandoned. | 3, 4.3, 4.7, 4.8, 5 |
| Look and sound: wet dawn fish-market stalls, crates, awnings, ice, scales, carts, and cat beds. | 3, 6 |
| Sounds of market bells, gulls, rats, raccoons, sales, cat tricks, and closing signs. | 6 |
| Core mechanics: combat, building, waves, economy. | 4.3–4.7 |
| Supporting mechanics: abilities, scoring. | 4.9–4.10 |
| Extra mechanics: none. | 0.3 |
| Content roster exactly as given. | 4.1, 5 |
| Left out: cat raising, fish cooking, city builder, action cat control, generic tower defense with cats pasted on human towers, player-triggered jokes, separate rules from jokes. | 0.2, 4.11 |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| Game premise is cats defending a fish market. | Accepted as final. | User decision. |
| Fixed oblique overhead view. | Accepted as final. Implemented as a DOM/SVG/CSS faux-oblique market floor, not a 3D engine. | Preserves browser/HTML constraint and makes hit testing reliable. |
| Real-time with prep before first wave and after each wave. | Accepted as final. Prep phase is a timed market bell countdown; the player may toll early after 5s, otherwise the bell rings at 30s. | Gives player control without adding a new game mode. |
| Run starts by lifting Closed sign. | Accepted as final. Title screen shows Closed sign; clicking it starts the run and loads stock. | Directly implements prompt. |
| Run ends when Market Scale stock reaches zero. | Accepted as final. No separate win condition; high scores reward quality. | Avoids adding systems left out. |
| Market Scale is both defended target and stock meter. | Accepted as final. `stock` is the Market Scale meter. | Directly implements prompt. |
| Waves begin after market bell tolls next count. | Accepted as final. Bell count is the wave number. | Directly implements prompt. |
| Core mechanics are combat, building, waves, economy. | Tier 1 exactly. | Required by task. |
| Abilities and scoring are supporting mechanics. | Tier 2. | Required by task. |
| Extra mechanics none. | Tier 3 has no new gameplay systems. | Required by task. |
| Content roster is exact. | No new cat types, enemy types, abilities, or mechanics. | Required by task. |
| Jokes are automatic feedback only. | Implemented as visual/audio feedback triggers, no rules. | Required by task. |
| Market layout was left open. | Use a deterministic 3-lane market graph with 12 stall nodes, 1 Market Scale node, 3 customer entrances, 2 raccoon exits, and 16 build pads. | Concrete enough for tests; still reads as market aisles, stalls, crates, ice, awnings, and angles. |
| “Stalls, crates, aisles, and angles” was left open. | Build pads are at stall nodes, aisle nodes, and four angle pads between lanes. | Implements the prompt literally without adding a city builder. |
| Exact cat defense areas were left open. | Use range-based coverage around cat beds with type-specific ranges and target types. | Simple, testable, and still “placed cats automatically defend their covered area.” |
| Cat bed orientation was left open. | No player-facing orientation. Cats automatically face the nearest valid enemy; coverage is range-based. | Avoids adding a control system not requested. |
| “Better positions” was left open. | Position quality is computed from number of target nodes covered, high-value stalls covered, and exits blocked. Used only for UI highlight, not a rule. | Implements the stated definition without adding a rule. |
| “Gap” was left open. | A gap exists when a fish target node or Market Scale node is not covered for the relevant threat type. | Directly matches core definition. |
| “Spread too thin” was left open. | UI warning when any high-value stall or Market Scale lane is uncovered. | Feedback only, no new rule. |
| “Weak point” was left open. | A darkened stall, low-confidence stall, or uncovered high-value target. Larger thieves target and occupy weak points. | Matches core definition. |
| “Cats overwhelmed” was left open. | When an enemy reaches a target and is not defeated, one active cat covering that target becomes overwhelmed and abandons its bed. If no cat covers the target, no cat is overwhelmed. | Prevents punishing cats that never had responsibility for the target. |
| “Turn away” was left open. | An enemy is turned away if it is defeated, pushed back by knockback, stopped by an ability, or forced to leave before reaching a target. | Matches wording. |
| “Single small cat cannot turn away larger thieves” was left open. | If a larger thief is covered only by one small cat (`Mackerel` or `Alley`), that cat deals 0 damage. Two small cats or any heavy/anti-air cat can damage it. | Clear, testable interpretation. |
| Customer carts were left open. | Each customer enters at a customer entrance node with a cart. If an enemy occupies the entrance, junction, or any path node, the customer leaves. | Implements “if an enemy blocks one, the customer leaves.” |
| Customer count was left open. | `customerFlow` starts at 6, min 1, max 12. Served customers increase it by 1; lost customers decrease it by 1. | Implements missing customers lowering future earning. |
| Sales were left open. | A sale takes 2s, buys 1 fish, earns 6 coins base, modified by ice/crate state. | Concrete economy. |
| Market Scale stock amount was left open. | Initial `stock = 100`. 12 crates each start with 8 fish (96), Market Scale starts with 4. Total 100. | Makes crates and scale feed one stock meter. |
| Ice tubs were left open. | Each stall has an ice tub with 100 integrity. It melts slowly during waves and faster near enemies. Below 50 it is melted: sale value halves, stock decays, and rats are attracted. Repair restores it. | Implements melting ice. |
| Awning poles were left open. | One pole per lane. Can be intact or broken. Awning Drop uses intact pole and damages it. Broken poles create tilting signs and reduce customer flow. Repair restores. | Implements prompt. |
| Temporary market repairs were left open. | Purchasable in prep for 25 coins; temporarily restores any broken market position for 45s after the next wave starts. | Implements “temporary market repairs” without adding a new mode. |
| Wave table was left open. | Use fixed waves 1–10, then endless generated waves scaled by hunger. | Gives a playable run and testable progression. |
| Gull King was left open. | Wave 10 boss, and every 10th endless wave. Drops from an awning pole, targets Market Scale, summons seagulls, tries to carry a crate, and causes immediate closing blow if it reaches Market Scale. | Implements prompt. |
| Ability targeting was left open. | Each ability has a specific click target and validity rule. Invalid targets fizzle and start cooldown. | Implements prompt. |
| Scoring formula was left open. | Defined formula rewarding stock saved, coins, customers, kills, unbroken stalls, high-value stalls, covered aisles, perfect waves, and penalizing failures. | Implements “defending well.” |
| Best scores were left open. | Store best score in `localStorage` key `catfish.bestScore`. | “Records best scores” requires persistence. |
| RNG was left open. | Deterministic xorshift64 seeded from `runSeed`. | Tests need determinism. |
| Rendering was left open. | HTML/CSS/SVG only; no canvas/WebGL. Oblique view is faked with layered DOM/SVG, not hit-testing transformed 3D. | Satisfies “HTML and CSS only” for screens. |
| Input was left open. | Mouse/touch click/tap for sign, pads, repairs, abilities, and bell. Keyboard hotkeys mirror the same actions. | Gives concrete player input. |
| Traps and pickups were mentioned in the generic designer prompt. | No traps or pickups exist. Temporary repairs and abilities are purchases/actions, not pickups. | Avoids adding systems left out. |

## 0.3 Tiers

| Tier | Segment | Description |
| --- | --- | --- |
| Tier 1 | Core market defense | Player can lift Closed sign, load Market Scale, build/repair cat beds, fight waves, earn from customers, lose stock, and close the market when stock reaches zero. Includes combat, building, waves, economy, market degradation, and Gull King. |
| Tier 2 | Market tricks and scoring | Adds ability charging/use and the scoring system, score HUD, wave-end score recording, and best score storage. |
| Tier 3 | None | No extra gameplay mechanics. Optional polish only. |

---

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Concept | Value / Convention |
| --- | --- |
| Logical market unit (`MU`) | 1 MU = distance between adjacent market nodes. |
| Grid coordinates | `x` increases right, `y` increases down. |
| Lane x coordinates | Lane A `x=0`, Lane B `x=4`, Lane C `x=8`. |
| Vertical node y coordinates | Enemy entrance `y=0`, stall 1 `y=1`, stall 2 `y=2`, stall 3 `y=3`, stall 4 `y=4`, junction/Market Scale `y=5`, customer entrance `y=6`. |
| Visual tile size | 64 CSS px per 1 MU for layout; presentation may compress vertically for oblique look. |
| Speed | MU/s. |
| Time | seconds. |
| Fixed logic step | `1/60s`. |
| Visual frame rate | `requestAnimationFrame`, but logic runs in fixed accumulator steps. |
| Stock unit | 1 stock = 1 fish. |
| Coin unit | integer coins. |
| Coverage distance | Euclidean distance in MU. |
| Node reach | Enemy reaches a node when its continuous position is within `0.15 MU` of node center. |

## 1.2 Important conventions

| Rule | Convention |
| --- | --- |
| Deterministic RNG | Use xorshift64 initialized from `runSeed`. No `Math.random` in gameplay logic. |
| Fixed-step loop | `update(dt = 1/60)` exactly. Visual interpolation only for drawing. |
| Phase separation | `phase = "title" | "prep" | "wave" | "gameover"`. Building and repair only in `prep`. Abilities only in `wave`. |
| No hidden player actions | All player actions are pointer clicks/taps or keyboard equivalents. |
| No canvas/WebGL | Use HTML/CSS/SVG for all visuals and screens. |
| Audio | Use the provided audio API/Web Audio synthesis only. |
| State ownership | Gameplay state lives in `globalContext`. UI reads it. Debug/tests mutate through module APIs. |
| Coverage | Coverage is computed from active cat beds, not from sprite position. |
| Targeting | Enemies and customers use deterministic path selection from the node graph. |
| Score | Score updates only at wave end in Tier 2. |
| Errors | If an action has no valid target, it does nothing except ability fizzle. No exceptions thrown. |

---

# 2. CONTRACTS

## 2.1 Module layout

| Module | Responsibility |
| --- | --- |
| `index.html` | DOM skeleton, screens, HUD, market container. |
| `style.css` | Oblique market presentation, HUD, states, animations. |
| `main.js` | Bootstrap, fixed loop, phase routing. |
| `state.js` | `globalContext`, run reset, phase transitions. |
| `world.js` | Market graph, nodes, pads, stalls, crates, ice, poles, exits, scale. |
| `input.js` | Pointer and keyboard input, action routing. |
| `build.js` | Place/repair cat beds, repairs, temporary repairs. |
| `combat.js` | Coverage, targeting, attacks, overwhelm, knockback, effects. |
| `waves.js` | Wave table, spawning, wave resolution, bell. |
| `economy.js` | Customers, sales, coin flow, customer count, stock consumption. |
| `abilities.js` | Ability charge, cooldown, targeting, effects. |
| `score.js` | Wave score, penalties, best score. |
| `audio.js` | Synthesized sound recipes and playback. |
| `ui.js` | HUD updates, screens, warnings, jokes. |
| `debug.js` | Direct system access for tests. |
| `tests.js` | Automated tests. |

## 2.2 Global context

| Field | Type | Meaning |
| --- | --- | --- |
| `runId` | string | Unique run id. |
| `runSeed` | uint64 | RNG seed. |
| `phase` | enum | `title`, `prep`, `wave`, `gameover`. |
| `time` | number | Seconds since run start. |
| `wave` | integer | Current wave count. |
| `bellCount` | integer | Next wave number displayed. |
| `bellTimer` | number | Seconds until next wave auto-starts. |
| `stock` | integer | Market Scale stock, 0–100. |
| `initialStock` | integer | Always 100. |
| `coins` | integer | Current currency. |
| `customerFlow` | integer | Current customer count, 1–12. |
| `servedCustomers` | integer | Total customers served. |
| `lostCustomers` | integer | Total customers lost. |
| `lostStock` | integer | Cumulative stock lost from theft/decay, not sales. |
| `stolenCrates` | integer | Cumulative crates carried to exit. |
| `meltedIceEvents` | integer | Cumulative ice tub melt events. |
| `enemiesDefeated` | integer | Cumulative enemies defeated. |
| `perfectWaves` | integer | Waves with zero stock loss. |
| `stalls` | array | All stall records. |
| `catBeds` | array | All build pads and bed states. |
| `cats` | array | Active cat instances. |
| `enemies` | array | Active enemy instances. |
| `customers` | array | Active customer instances. |
| `marketScale` | object | Market Scale state. |
| `exits` | array | Exit nodes. |
| `customerEntrances` | array | Customer entrance nodes. |
| `awnings` | array | Awning pole records. |
| `abilities` | array | Ability charge/cooldown records. |
| `warnings` | object | `spreadTooThin`, `gap`, `tiltingLanes`. |
| `score` | object | Current score record. |
| `bestScore` | integer | Best score. |
| `jokes` | array | Recent automatic joke IDs. |
| `rngState` | uint64 | RNG state. |

## 2.3 Module specifics

| Module | Required functions |
| --- | --- |
| `state.js` | `newRun(seed)`, `setPhase(phase)`, `startRun()`, `endRun(reason)`, `tick(dt)`. |
| `world.js` | `buildMarketGraph()`, `getNode(id)`, `getLaneNodes(lane)`, `getTargetNodes()`, `isNodeCovered(nodeId, threatType)`, `getHighValueStalls()`, `getWeakPoints()`. |
| `input.js` | `onPointerDown(x,y)`, `onKey(key)`, `liftClosedSign()`, `ringBell()`, `selectBuildType(type)`, `clickPad(padId)`, `clickRepair(targetId)`, `clickAbility(abilityId,targetId)`. |
| `build.js` | `canPlaceCatBed(padId, catType)`, `placeCatBed(padId, catType)`, `canRepair(targetId)`, `repairCatBed(bedId)`, `repairIceTub(id)`, `repairAwning(id)`, `repairStall(stallId)`, `buyTemporaryRepair(targetId)`, `updateTemporaryRepairs(dt)`. |
| `combat.js` | `updateCoverage()`, `getDefenseArea(catId)`, `selectTarget(enemyId)`, `attackEnemy(catId, enemyId, dt)`, `applyKnockback(enemyId, distance, stun)`, `applySlow(enemyId, factor, duration)`, `applyHesitate(enemyId, factor, duration)`, `markOverwhelmed(catId)`, `checkTargetReached(enemyId, targetId)`. |
| `waves.js` | `startWave(waveNumber)`, `endWave()`, `spawnEnemy(type, lane, delay)`, `updateEnemyMovement(dt)`, `resolveWaveBreak(enemyId)`, `getWaveTable(wave)`, `scaleWaveByHunger(wave)`. |
| `economy.js` | `spawnCustomer(lane)`, `updateCustomerMovement(dt)`, `startSale(customerId)`, `completeSale(customerId)`, `loseCustomer(customerId, reason)`, `consumeStock(amount, reason)`, `addCoins(amount, reason)`, `updateIceMelt(dt)`, `updateSaleValue(stallId)`. |
| `abilities.js` | `canCharge(abilityId)`, `charge(abilityId)`, `getValidTargets(abilityId)`, `useAbility(abilityId, targetId)`, `applyYarn(targetId)`, `applyNap(targetId)`, `applyFrenzy(targetId)`, `applyAwningDrop(awningId)`, `tickAbilities(dt)`. |
| `score.js` | `recordWaveScore()`, `calculateScore()`, `saveBestScore()`, `getBestScore()`, `resetScore()`. |
| `audio.js` | `play(soundName)`, `playBell(count)`, `playClosedSign()`, `playSale()`, `playAbility(name)`. |
| `ui.js` | `showScreen(name)`, `updateHUD()`, `showWarning(name)`, `showJoke(id)`, `renderMarketState()`. |
| `debug.js` | See Section 8. |
| `tests.js` | `runTier1Tests()`, `runTier2Tests()`. |

---

# 3. VISUAL SPEC

The game is a wet dawn fish market seen from a fixed oblique overhead angle. The floor is dark, wet cobblestone and salt-stained tile with shallow puddles. Stalls line three market aisles, each with wooden counters, fish crates, small ice tubs, customer carts, and low awning poles. Cat beds are simple cushioned mats placed at stalls and angles. The Market Scale is a large ornate weighing scale at the center-bottom of the market, glowing faintly as the day’s stock meter. Enemies are not clean cartoon soldiers; they are market pests with wet feather edges, oily fur, and awkward market behavior. Failure is shown physically: crates crack open, ice puddles spread, signs tilt, awnings sag, stalls darken, and cat beds sit abandoned. The whole scene should feel like a cramped, damp market at dawn, not a board game.

## Lighting and atmosphere

| Element | Rule |
| --- | --- |
| Base light | Cool blue-gray dawn light from top-left. |
| Wet surfaces | Subtle specular streaks on floor tiles and puddles. |
| Stalls | Warm fish-market glow from under-counter lamps; darker when darkened. |
| Ice | Pale cyan highlight when intact; murky blue and puddle when melted. |
| Fish crates | Brown wood with silver-blue fish sheen; cracked/darker when knocked open. |
| Market Scale | Brass/green-patina metal, brightens with stock, dims as stock falls. |
| Closed sign | Heavy painted board, red-black text, sways slightly when hung. |
| Tilting sign | Warning sign rotates up to 12 degrees, drips slightly. |
| Abandoned cat bed | Empty cushion with a paw print and a small “!” until repaired. |

## Space

| Space | Description |
| --- | --- |
| Three aisles | Vertical lanes A, B, C. Enemies come from top entrances; customers come from bottom entrances. |
| Twelve stalls | Four per lane, each with a counter, fish crate, ice tub, and customer cart point. |
| Market Scale | Center-bottom junction node, visually large and central. |
| Exits | Left and right market exits near the bottom junctions, used by raccoons and other crate thieves. |
| Awning poles | One per lane at station 2, visually supporting sagging awnings. |
| Build pads | Visible as faint chalk outlines at stalls, aisle edges, and four angle pads between lanes. |
| Customer carts | Small wooden carts at customer entrances; customers push them to stalls. |
| Closed sign | Large sign over the Market Scale before start and at game over. |

## Recipe table

| Visual element | CSS/SVG recipe |
| --- | --- |
| Floor | Repeating linear-gradient cobblestone, `#2b3440` base, `#3b4756` highlights, puddle radial gradients `rgba(120,160,200,0.08)`. |
| Stall counter | Rounded rectangle, wood gradient `#6d4b2f` to `#3e2a1a`, counter top `#8b6a48`. |
| Fish crate | Small brown box with fish-scale pattern, silver-blue fish shapes, cracks when damaged. |
| Ice tub | Rounded basin, cyan gradient `#bfe8ff` to `#4f8db5`, puddle ellipse when melted. |
| Market Scale | Brass polygon shape, pan, needle, gauge glow. Stock meter is a vertical fish-stack gauge. |
| Cat bed | Soft oval cushion, paw icon, color-coded by cat type. |
| Mackerel Mouser | Slate-gray cat silhouette, thin fish-tail tail, cheap look. |
| Calico Counter Cat | Tri-color patch silhouette, perched on counter, alert. |
| Alley Cat | Dark tabby silhouette with awning shadow, low posture. |
| Ragdoll Rattler | Large fluffy pale cat with rattle collar, heavier silhouette. |
| Tabby Bell Ringer | Striped cat with small bell collar, upright posture. |
| Seagull | White-gray bird silhouette, angular wings, wet feather edges. |
| Rat swarm | Small dark oval cluster with tail streaks. |
| Raccoon | Masked gray-black raccoon silhouette, hunched, carrying crate when loaded. |
| Larger thieves | Same silhouettes scaled 1.35x, heavier outline, darker shadow. |
| Gull King | Huge gull silhouette with crown-like feather crest and a crate harness. |
| Customer | Simple market patron silhouette with small cart. |
| Closed sign | Dark board, red lettering, slight sway animation. |
| Tilting sign | Warning triangle/sign, rotates, drips. |
| Darkened stall | Dark overlay, no lamp glow, gray fish. |
| Jokes | Small non-interactive SVG callouts, fade in/out. |

---

# 4. GAMEPLAY SPEC

The player is the Forecat. They lift the Closed sign, load the Market Scale with the day’s stock, and prepare cat beds, repairs, and market tricks. During each wave, customers push carts into the market to buy fish, while seagulls, rats, raccoons, and larger thieves try to steal fish, carry crates, occupy weak points, or reach the Market Scale. Cats automatically defend their covered areas. If the market is defended well, sales continue, customers keep coming, and the stock stays high. If gaps form, stalls darken, beds are abandoned, ice melts, signs tilt, and later waves become hungrier. The run ends when the Market Scale stock reaches zero and the Closed sign is hung.

## Records and rosters

### CatBed record

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Bed/pad id. |
| `padId` | string | World pad id. |
| `nodeId` | string | Covered target node or nearest lane node. |
| `catType` | enum | `mackerel`, `calico`, `alley`, `ragdoll`, `tabby`. |
| `state` | enum | `empty`, `building`, `active`, `abandoned`, `temporary_repaired`. |
| `timer` | number | Build/repair/temporary repair timer. |
| `coverageScore` | number | UI position quality only. |

### Cat record

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Cat instance id. |
| `bedId` | string | Parent bed. |
| `type` | enum | Cat type. |
| `hp` | integer | Not used for death; cats only become overwhelmed. |
| `range` | number | Coverage radius in MU. |
| `attackSpeed` | number | Attacks/s. |
| `damage` | integer | Damage per attack. |
| `targetType` | enum | `ground`, `air`, `any`, `support`. |
| `targetId` | string | Current target. |
| `effects` | array | `frenzy`, etc. |

### Enemy record

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Enemy id. |
| `type` | enum | Roster type. |
| `hp` | integer | Current HP. |
| `maxHp` | integer | Spawn HP. |
| `speed` | number | MU/s. |
| `lane` | enum | Spawn lane or nearest lane. |
| `path` | array | Node path. |
| `pos` | object | Continuous x/y. |
| `state` | enum | `entering`, `moving`, `nibbling`, `picking`, `carrying`, `occupying`, `stunned`, `asleep`, `hesitating`, `leaving`, `defeated`. |
| `cargoStallId` | string | Crate being carried. |
| `effects` | array | Slow, hesitate, stop, nap. |

### Customer record

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Customer id. |
| `lane` | enum | Lane. |
| `targetStallId` | string | Target stall. |
| `path` | array | Nodes. |
| `pos` | object | Continuous x/y. |
| `state` | enum | `entering`, `walking`, `waiting`, `buying`, `leaving`, `served`, `lost`. |
| `saleTimer` | number | Sale progress. |

### Stall record

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Stall id. |
| `lane` | enum | Lane. |
| `station` | integer | 1–4. |
| `nodeId` | string | Target node. |
| `crateStock` | integer | Fish in crate. |
| `crateIntegrity` | integer | 0–100. |
| `confidence` | integer | 0–100 customer confidence. |
| `darkened` | boolean | Stops sales. |
| `iceTubId` | string | Ice tub. |
| `awningId` | string | Awning pole. |
| `temporaryRepairTimer` | number | Temporary repair. |

### IceTub record

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Ice tub id. |
| `stallId` | string | Parent stall. |
| `integrity` | integer | 0–100. |
| `melted` | boolean | Sale value and rat attraction. |
| `temporaryRepairTimer` | number | Temporary repair. |

### AwningPole record

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Pole id. |
| `lane` | enum | Lane. |
| `integrity` | integer | 0–100. |
| `broken` | boolean | Creates gap/tilting sign. |
| `temporaryRepairTimer` | number | Temporary repair. |

### MarketScale record

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Always `scale`. |
| `stock` | integer | Same as `globalContext.stock`. |
| `closingBlowTimer` | number | Gull King blow delay. |

### Roster: cats

| Cat | Cost | Role | Range | Attack speed | Damage | Special |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| Mackerel Mouser | 10 | Cheap ground opener | 2.0 | 1.5/s | 6 | Ground only. |
| Alley Cat | 12 | Cheap under-stall/rat cat | 1.5 | 1.0/s | 5 | Ground only; rats slowed 25%. |
| Calico Counter Cat | 25 | Anti-air | 3.5 | 1.8/s | 8 | Air only. |
| Ragdoll Rattler | 35 | Heavy knockback | 1.8 | 0.7/s | 35 | Every 2 hits knockback 1 MU and stun 1.5s. |
| Tabby Bell Ringer | 50 | Support | 2.8 | 0.5/s | 3 | Every 4s hesitates nearby enemies: speed -30% for 2s. Nearby cats target enemy closest to Market Scale. |

### Roster: enemies

| Enemy | HP | Speed | Behavior |
| --- | ---: | ---: | --- |
| Seagull | 15 | 2.5 MU/s | Flies to fish target, steals 1 fish, leaves. |
| Seagull Scout | 8 | 3.2 MU/s | Fast distraction bird, steals 1 fish. |
| Gull Brute | 90 | 1.3 MU/s | Airborne brute, steals 10 fish, cannot be damaged by one small ground cat. |
| Rat Swarm | 20 | 1.3 MU/s | Nibbles 1.5 fish/s, max 12 fish, knocks crate open after 5s. |
| Large Rat Swarm | 50 | 1.7 MU/s | Nibbles 3 fish/s, max 24 fish. |
| Raccoon Crate Thief | 80 | 0.6 MU/s | Picks a crate, carries to exit. Requires sustained damage or knockback. |
| Raccoon Brute | 180 | 0.5 MU/s | Larger thief, occupies weak point, small-cat immunity against single small cat. |
| Gull King | 450 | 0.7 MU/s | Boss. Drops from awning, summons seagulls, tries to carry crate, causes immediate closing blow at Market Scale. |

### Roster: market objects

| Object | Initial state | Failure state | Repair |
| --- | --- | --- | --- |
| Fish crate | 8 fish, integrity 100 | Knocked-open at integrity <50, darkened at confidence <50 or empty. | Repair stall 30 coins. |
| Ice tub | integrity 100 | Melted at integrity <50. | Repair 20 coins. |
| Awning pole | integrity 100 | Broken at integrity <50. | Repair 15 coins. |
| Cat bed | empty or active | Abandoned after overwhelm. | Repair 8 coins. |
| Temporary repair | none | Expires after 45s. | Purchase 25 coins in prep. |
| Market Scale | 100 stock | 0 closes market. | Not directly repairable. |
| Customer cart | at customer entrance | Blocked if enemy occupies path. | Not repairable. |
| Closed sign | title/game over only | Run end. | None. |
| Tilting sign | none | Gap or broken awning. | Close gap/repair. |

## 4.1 Run and phases — Tier 1

| Phase | Rules |
| --- | --- |
| Title | Shows Closed sign. Click sign or press Enter to start. |
| Start run | Set `stock=100`, `coins=30`, `customerFlow=6`, `wave=0`, load crates, set `phase=prep`, `bellTimer=30`. |
| Prep | Building and repair allowed. No enemies, no customers, no ice decay. Bell timer counts down. Player may click bell to start early after 5s. |
| Wave | Enemies spawn, customers arrive, cats fight, abilities can be used. No building or repair. |
| Wave end | When all enemies are defeated or have left. If `stock > 0`, go to prep and increment wave. If Tier 2, record score. |
| Game over | If `stock <= 0` at any time, set `phase=gameover`, hang Closed sign, stop spawning, stop movement. |

## 4.2 Market layout and objects — Tier 1

### Node graph

| Node type | Count | Coordinates / ids |
| --- | ---: | --- |
| Enemy entrances | 3 | `EN_A (0,0)`, `EN_B (4,0)`, `EN_C (8,0)`. |
| Stall nodes | 12 | `S_A1 (0,1)` through `S_A4 (0,4)`, same for B/C. |
| Junctions | 3 | `J_A (0,5)`, `J_B (4,5)`, `J_C (8,5)`. |
| Market Scale | 1 | `SCALE = J_B`. |
| Exits | 2 | `EX_A (-2,5)`, `EX_C (10,5)`. |
| Customer entrances | 3 | `CUST_A (0,6)`, `CUST_B (4,6)`, `CUST_C (8,6)`. |
| Build pads | 16 | 12 at stall nodes, 4 angle pads at `(2,2)`, `(2,4)`, `(6,2)`, `(6,4)`. |
| Awning poles | 3 | `AWNING_A (0,2)`, `AWNING_B (4,2)`, `AWNING_C (8,2)`. |

### Edges

| Edge group | Direction |
| --- | --- |
| Ground enemy lane | `EN -> S1 -> S2 -> S3 -> S4 -> J`. |
| Bottom cross | `J_A <-> J_B <-> J_C`. |
| Market Scale target | `J_A -> J_B`, `J_C -> J_B`. |
| Raccoon exit | `J_A -> EX_A`, `J_C -> EX_C`, `J_B -> J_A -> EX_A`. |
| Customer path | `CUST -> J -> S4 -> S3 -> S2 -> S1` to target. |

## 4.3 Building and repairs — Tier 1

### Building rules

| Action | Input | Cost | Result |
| --- | --- | ---: | --- |
| Place cat bed | Click empty pad, select cat type | Cat cost | Creates active cat bed and cat. |
| Cannot build during wave | Attempt ignored | 0 | UI shakes. |
| Cannot build on abandoned bed | Click ignored | 0 | Must repair first. |
| Cannot build without coins | Click ignored | 0 | Insufficient funds feedback. |

### Repair rules

| Repair | Cost | Effect |
| --- | ---: | --- |
| Repair cat bed | 8 | Bed becomes active, cat returns. |
| Repair ice tub | 20 | Integrity to 100, `melted=false`. |
| Repair awning pole | 15 | Integrity to 100, `broken=false`, tilting sign removed if no other cause. |
| Repair darkened stall | 30 | `confidence=100`, `crateIntegrity=80`, `darkened=false`, adds 5 fish if crate stock <5. |
| Temporary market repair | 25 | Target any broken market position. Restores function for 45s after next wave starts. |

### Temporary repairs

| Rule | Number |
| --- | ---: |
| Purchase phase | Prep only. |
| Duration after wave start | 45s. |
| Effect | Treats target as repaired for all rules. |
| Expiry | Returns to previous broken state. |
| Stacking | No stacking; new temporary repair replaces old timer. |

### Position quality

| Metric | Number |
| --- | ---: |
| Target node covered | +10 |
| High-value stall covered | +20 |
| Exit path blocked | +5 |
| Used only for | UI highlight, not gameplay rules. |

## 4.4 Combat — Tier 1

### Coverage

| Rule | Number |
| --- | ---: |
| Coverage shape | Circle radius in MU around cat bed. |
| Ground coverage | Mackerel, Alley, Ragdoll. |
| Air coverage | Calico. |
| Support coverage | Tabby does not count as direct coverage for fish targets. |
| A target node is covered | If any active compatible cat’s defense area contains the node. |
| Continuous enemy coverage | If enemy position is within range. |

### Targeting

| Actor | Target selection |
| --- | --- |
| Cats | Target enemy closest to cat bed. If a Tabby is active, nearby cats target enemy closest to Market Scale instead. |
| Ground enemies | Nearest fish crate with stock, or Market Scale if no crates. |
| Raccoons | Nearest crate with stock, then nearest exit. |
| Larger thieves | Nearest weak point, else Market Scale. |
| Seagulls/Gull Brutes | Nearest fish target not covered by anti-air at spawn; if none, nearest fish target. |
| Customers | Nearest open stall with stock and clear path. |

### Attack rules

| Rule | Number |
| --- | ---: |
| Attack interval | `1 / attackSpeed`. |
| Damage | Applied on each attack. |
| Knockback | Ragdoll pushes enemy 1 MU backward along path and stuns 1.5s every 2 hits. |
| Slow | Alley applies 25% slow to rats while in range. |
| Hesitate | Tabby applies 30% slow for 2s every 4s. |
| Frenzy | Tier 2 ability doubles attack speed and adds +1 damage for 6s. |

### Overwhelm rule

1. When an enemy reaches a target node and is not defeated, determine the responsible cat:
   - If the target is covered by one or more active cats, choose the active cat nearest to the target.
   - If no compatible cat covers the target, no cat is overwhelmed.
2. The responsible cat enters `overwhelmed`.
3. Its cat bed becomes `abandoned`.
4. The enemy proceeds to steal stock.

### Larger thief small-cat rule

| Condition | Effect |
| --- | --- |
| Larger thief covered by exactly one small cat | That small cat deals 0 damage. |
| Larger thief covered by two or more small cats | All small cats deal normal damage. |
| Larger thief covered by any heavy or anti-air cat | Normal damage applies. |

### Wave-break rule

| Event | Effect |
| --- | --- |
| Enemy reaches Market Scale | Stock loss: ground 10, seagull 5, Gull King 30. Enemy leaves. |
| Raccoon reaches exit carrying crate | Stock loss equals crate stock, max 10. `stolenCrates++`. Enemy leaves. |
| Gull King reaches Market Scale | Immediate closing blow: stock -30. If stock reaches 0, run ends. |
| Wave-break | Does not end the wave by itself; wave continues until all enemies resolved. |

## 4.5 Enemies — Tier 1

### Seagull / Scout

| Rule | Number |
| --- | ---: |
| Spawn | Over target node. |
| Movement | Straight line to target. |
| Ground barriers | Ignored. |
| On reaching target | Steals 1 fish, leaves upward. |
| If defeated | Leaves feathers, no theft. |

### Rat Swarm

| Rule | Number |
| --- | ---: |
| Spawn | Enemy entrance, target crate. |
| Nibble rate | 1.5 fish/s. |
| Max theft | 12 fish. |
| Crate damage | Integrity -10/s. |
| After theft or 5s | Moves to exit and leaves. |
| Knocked-open bonus | If crate integrity <50, rats get +20% speed and +10% spawn count at that stall. |

### Raccoon Crate Thief

| Rule | Number |
| --- | ---: |
| Spawn | Enemy entrance. |
| Target | Nearest crate with stock. |
| Pick time | 2s. |
| Carry | Attaches crate, moves to exit. |
| If defeated while carrying | Crate returns to original stall, stock restored. |
| If reaches exit | Stock lost, `stolenCrates++`. |

### Larger thieves

| Rule | Number |
| --- | ---: |
| Target | Nearest weak point, else Market Scale. |
| On reaching weak point | Enters `occupying`. |
| Occupation theft | 2 fish/s from local crate if present, else Market Scale. |
| Occupation duration | 30s; then leaves through exit causing its accumulated loss. |
| Blocks customers | Any path through occupied node is blocked. |
| Small-cat immunity | Single small cat deals 0. |

### Gull King

| Rule | Number |
| --- | ---: |
| Spawn | Drops at `AWNING_B`. |
| Target | Market Scale. |
| HP | 450. |
| Speed | 0.7 MU/s. |
| Summons | 2 Seagull Scouts every 5s, max 2 active. |
| Crate try | If passes a crate with stock, picks it and carries it. |
| Reaches Market Scale | Immediate closing blow -30 stock. |
| Defeated | No closing blow. |

## 4.6 Waves — Tier 1

### Wave timing

| Rule | Number |
| --- | ---: |
| First wave | After Closed sign lifted, prep 30s, then bell. |
| Next wave | After previous wave resolved, prep 30s, then bell. |
| Early bell | Player may ring after 5s. |
| Wave end | All enemies defeated or left. |
| Bell count | Wave number. |

### Fixed wave table

| Wave | Spawn groups | Pattern |
| ---: | --- | --- |
| 1 | 0s: 2 Rat A, 2s: 1 Rat B | Tutorial ground. |
| 2 | 0s: 1 Seagull B, 4s: 2 Rat A, 6s: 2 Rat C | Introduce air. |
| 3 | 0s: 1 Raccoon B, 5s: 3 Rat A | Introduce crates. |
| 4 | 0s: 2 Seagull A, 2s: 1 Seagull C, 5s: 3 Rat B, 7s: 1 Large Rat B | Mixed. |
| 5 | 0s: 2 Scout B, 3s: 1 Raccoon A, 5s: 1 Raccoon C, 7s: 2 Rat B | Distraction. |
| 6 | 0s: 1 Large Rat A, 2s: 1 Large Rat C, 5s: 3 Raccoon B | Draw cats away. |
| 7 | 0s: 2 Scout A, 1s: 2 Scout C, 4s: 1 Gull Brute B, 7s: 1 Raccoon A, 8s: 1 Raccoon C | Air pressure. |
| 8 | 0s: 1 Raccoon Brute A, 3s: 2 Large Rat A, 5s: 3 Seagull B, 7s: 2 Raccoon C | Weak points. |
| 9 | 0s: 1 Raccoon Brute B, 2s: 1 Gull Brute C, 4s: 2 Large Rat C, 6s: 2 Raccoon A, 8s: 2 Raccoon C | Heavy mix. |
| 10 | 0s: Gull King B, 2s: 2 Scout A, 2s: 2 Scout C, 5s: 1 Raccoon A, 6s: 1 Raccoon C | Boss. |

### Endless waves

| Rule | Number |
| --- | ---: |
| After wave 10 | Generate next wave from previous wave composition. |
| Count growth | Add 1 enemy per wave, cycling `Rat Swarm`, `Seagull`, `Raccoon`. |
| HP scaling | `maxHp *= 1 + 0.08 * (wave - 10)`. |
| Speed scaling | `speed *= 1 + 0.04 * (wave - 10)`. |
| Boss | Gull King every wave divisible by 10. |

## 4.7 Economy and customers — Tier 1

### Customer flow

| Rule | Number |
| --- | ---: |
| Initial customerFlow | 6. |
| Min / max | 1 / 12. |
| Spawn count per wave | `min(12, floor(customerFlow))`. |
| Spawn interval | `clamp(8 - 0.25 * wave, 3, 8)` seconds. |
| Served customer | `customerFlow += 1`, max 12. |
| Lost customer | `customerFlow -= 1`, min 1, `lostCustomers++`. |

### Sale rules

| Rule | Number |
| --- | ---: |
| Sale requires | Path clear, stall not darkened, crate stock >0, no enemy carrying/taking that fish. |
| Sale duration | 2s. |
| Fish sold | 1. |
| Base coin value | 6. |
| Ice multiplier | 1.0 intact, 0.5 melted. |
| Crate multiplier | 1.0 intact, 0.7 knocked-open. |
| Final coin value | `round(6 * iceMultiplier * crateMultiplier)`. |
| Stock effect | `stock--` and `crateStock--`. |
| If interrupted | Customer leaves, `lostCustomers++`, stall confidence -20. |

### Stock rules

| Source | Loss |
| --- | ---: |
| Customer sale | 1 fish. |
| Seagull | 1 fish. |
| Rat Swarm | 1.5/s, max 12. |
| Large Rat Swarm | 3/s, max 24. |
| Knocked-open crate instant | 5 fish. |
| Melted ice decay | 0.2 fish/s per melted tub. |
| Raccoon carrying crate | crate stock, max 10. |
| Ground enemy reaching Market Scale | 10 fish. |
| Seagull reaching Market Scale | 5 fish. |
| Gull King closing blow | 30 fish. |

### Market degradation

| Event | Effect |
| --- | --- |
| Customer blocked | Customer leaves, stall confidence -20. |
| Customer served | Stall confidence +5, max 100. |
| Confidence <50 | Stall darkened. |
| Crate integrity <50 | Knocked-open crate, instant -5 stock, rat bonus. |
| Ice integrity <50 | Melted, sale value half, stock decay, rats attracted. |
| Awning integrity <50 | Broken, tilting sign, lane customer spawn weight -30%. |
| Tilting sign | Lane spawn weight -50%. |
| Darkened stall | Customers avoid, becomes weak point. |

## 4.8 Gaps, weak points, tilting signs — Tier 1

### Gap rule

| Rule | Number |
| --- | ---: |
| Ground gap | Target node not covered by active ground cat. |
| Air gap | Target node not covered by active Calico. |
| Scale gap | Market Scale node not covered by ground cat. |
| Gap creation | Leaving approach uncovered or losing a cat. |
| Gap closure | Build a covering cat, repair a cat bed, or use an ability that blocks the area. |

### Spread too thin

| Rule | Number |
| --- | ---: |
| Trigger | Any high-value stall or Market Scale lane is uncovered. |
| Effect | HUD warning, no direct gameplay rule. |

### Tilting sign

| Trigger | Effect |
| --- | --- |
| Any target gap in lane | Lane sign tilts, customer spawn weight -50%. |
| Broken awning in lane | Lane sign tilts, customer spawn weight -30%. |
| Closed gap/repaired awning | Sign resets if no other trigger. |

### Weak point

| Rule | Number |
| --- | ---: |
| Weak point | Darkened stall, confidence <50, uncovered high-value target. |
| Larger thief target | Nearest weak point, else Market Scale. |
| Occupation | Stops, steals 2 fish/s, blocks path, ends after 30s if not defeated. |

## 4.9 Abilities — Tier 2

All abilities are charged by spending coins during a wave. If the ability is off cooldown and the target is valid, it activates. If invalid, it fizzles and starts cooldown.

| Ability | Cost | Cooldown | Target | Effect |
| --- | ---: | ---: | --- | --- |
| Yarn Ball Tangle | 8 | 20s | Any node with at least one enemy on it or its downstream edge | Stops enemies on target node and next downstream node for 4s. |
| Catnip Nap | 10 | 30s | Any cat bed, active or abandoned | Enemies within 2.2 MU sleep 5s, cancel theft actions. |
| Hairball Frenzy | 15 | 40s | Any active cat bed | Cats within 3.0 MU attack speed x2, damage +1 for 6s. |
| Awning Drop | 20 | 45s | Intact awning pole | Damages enemies within 2.0 MU for 30, damages pole -35, creates temporary gap block for 8s. |

### Ability invalidity

| Ability | Invalid if |
| --- | --- |
| Yarn Ball Tangle | No enemy in target line. |
| Catnip Nap | No cat bed selected. |
| Hairball Frenzy | No active cat bed selected. |
| Awning Drop | Pole broken or no pole selected. |

## 4.10 Scoring — Tier 2

Score is recorded after each wave ends. Best score is saved to `localStorage` key `catfish.bestScore`.

### Score formula

```text
score =
  finalStock * 2
  + coinsEarned * 1
  + servedCustomers * 5
  + enemiesDefeated * 10
  + unbrokenStallsAtEnd * 50
  + protectedHighValueStallsAtEnd * 100
  + aislesCoveredAtWaveEnd * 20
  + perfectWaves * 200
  - penalties
```

### Penalties

| Penalty | Points |
| --- | ---: |
| Customer lost | 5 |
| Darkened stall at end | 100 |
| Stolen crate | 50 |
| Melted ice event | 25 |
| Abandoned cat bed at end | 20 |
| Closed market | 1000 |

### Wave-end bonuses

| Bonus | Number |
| --- | ---: |
| Perfect wave | Wave with zero stock lost from theft/decay. |
| Aisles covered at wave end | Count lanes where all target nodes are covered. |
| Protected high-value stalls | High-value stalls not darkened at run end. |
| Unbroken stalls | Stalls not darkened at run end. |

## 4.11 Jokes — Tier 2

Jokes are automatic feedback only. They never change rules.

| Joke | Trigger | Display |
| --- | --- | --- |
| Mackerel Flick | Calico defeats an airborne thief. | Small fish-flick callout near Calico. |
| Crate Knock | Ragdoll or ability affects enemy within 1 MU of crate. | Crate wobble and knock callout. |
| Fish-Tail Bat | Yarn Ball Tangle or Catnip Nap affects enemy near fish. | Fish-tail bat callout. |
| Post-Wave Nap | Wave ends and score is recorded. | Nearby cats nap briefly. |

## 4.12 Progression and difficulty

### Hunger

```text
hunger = clamp(
  1
  + 0.4 * lostStock / 100
  + 0.25 * lostCustomers / 6
  + 0.05 * currentDarkenedStalls
  + 0.05 * currentAbandonedBeds,
  1,
  3
)
```

### Scaling

| Rule | Number |
| --- | ---: |
| HP multiplier | `hunger`. |
| Speed multiplier | `1 + (hunger - 1) * 0.5`. |
| Extra rats for waves 1–10 | If `hunger > 1.25`, add `floor((hunger - 1) * wave / 2)` Rat Swarms. |
| Endless scaling | As above in wave table. |

### High-value stall definition

A stall is high-value if:

| Condition | Number |
| --- | ---: |
| Ice integrity | >50 |
| Crate stock | >=4 |
| Distance to Market Scale | <=2 nodes |

## 4.13 Feel

| Goal | Implementation |
| --- | --- |
| Market pressure, not abstract defense | Customers and stock are visible and reactive. |
| Building feels like covering market gaps | Coverage overlays, tilting signs, weak point highlights. |
| Failure is physical | Crates crack, ice melts, signs tilt, beds abandon. |
| Rewards are clean | Coins from sales, not kills. |
| Scoring rewards quality | Perfect waves, protected stalls, covered aisles. |
| Cats feel like market workers | Beds at stalls, bells, awnings, carts, wet dawn. |

---

# 5. CHARACTERS

## Cat silhouettes and states

| Cat | Silhouette | Facings | States |
| --- | --- | --- | --- |
| Mackerel Mouser | Low, sleek, fish-tail tail. | Faces nearest ground enemy; default down. | `idle`, `attack`, `overwhelmed`, `abandoned`. |
| Calico Counter Cat | Tri-color, perched, alert. | Faces nearest airborne enemy; default down. | `idle`, `attack`, `overwhelmed`, `abandoned`. |
| Alley Cat | Dark tabby, low under awning shadow. | Faces nearest ground enemy; default down. | `idle`, `attack`, `overwhelmed`, `abandoned`. |
| Ragdoll Rattler | Large fluffy, rattle collar. | Faces nearest heavy enemy; default down. | `idle`, `attack`, `knockback`, `overwhelmed`, `abandoned`. |
| Tabby Bell Ringer | Striped, upright, bell collar. | Faces nearest enemy; default down. | `idle`, `bell`, `support`, `overwhelmed`, `abandoned`. |

## Cat animations

| Animation | Motion rule |
| --- | --- |
| `cat_idle` | Slow breathing, tail sway, 0.8s loop. |
| `cat_attack` | Quick forward lunge/paw, 0.25s, returns to idle. |
| `cat_bell` | Head tilt, bell swing, 0.4s. |
| `cat_knockback` | Rattle shake, heavy paw sweep, 0.35s. |
| `cat_overwhelmed` | Backs away, fur puffs, 0.5s, then bed abandoned. |
| `cat_abandoned` | Empty bed, small paw print, slow pulse. |
| `cat_frenzy` | Faster attack animation, motion blur, 6s. |

## Enemy silhouettes and states

| Enemy | Silhouette | Facings | States |
| --- | --- | --- | --- |
| Seagull / Scout | Angular white-gray bird. | Faces movement. | `entering`, `moving`, `stealing`, `leaving`, `defeated`. |
| Gull Brute | Heavier gull, dark wing edges. | Faces movement. | same, plus `hesitating`. |
| Rat Swarm | Low cluster of small dark bodies. | Faces movement. | `entering`, `moving`, `nibbling`, `leaving`, `defeated`. |
| Large Rat Swarm | Bigger cluster, oily fur. | Faces movement. | same. |
| Raccoon | Masked hunched raccoon. | Faces movement. | `entering`, `moving`, `picking`, `carrying`, `leaving`, `defeated`. |
| Raccoon Brute | Larger raccoon, heavy outline. | Faces movement. | same, plus `occupying`, `smallCatImmune`. |
| Gull King | Huge crowned gull with crate harness. | Faces Market Scale. | `drop`, `moving`, `summon`, `picking`, `carrying`, `closingBlow`, `defeated`. |

## Enemy animations

| Animation | Motion rule |
| --- | --- |
| `bird_fly` | Wing flap, vertical bob, speed 0.4s loop. |
| `bird_steal` | Dive to crate, grab, ascend, 0.6s. |
| `rat_scurry` | Low jitter movement, tail streaks. |
| `rat_nibble` | Head pecks at crate, 0.3s loop. |
| `raccoon_walk` | Hunched shuffle. |
| `raccoon_pick` | Lift crate, settle on back, 2s. |
| `raccoon_carry` | Slower walk, crate bob. |
| `brute_occupy` | Plants itself, paws down, steals from crate/scale. |
| `gull_king_drop` | Drops from awning, awning bends, 1s. |
| `gull_king_summon` | Wings spread, bird cry. |
| `gull_king_close_blow` | Slams crate onto Market Scale, screen shake. |

## Customer silhouettes and states

| Entity | Silhouette | States |
| --- | --- | --- |
| Customer | Simple patron with market cart. | `entering`, `walking`, `waiting`, `buying`, `leaving`, `served`, `lost`. |
| Customer cart | Small wooden cart. | Attached to customer; blocked state shows brake marks. |

## Customer animations

| Animation | Motion rule |
| --- | --- |
| `customer_walk` | Pushes cart, 0.6s loop. |
| `customer_buy` | Reaches into crate, coin sparkle, 2s. |
| `customer_leave` | Turns, pushes cart away, 0.8s. |
| `customer_blocked` | Cart stops, brake marks, 0.5s. |

## Market object states

| Object | States | Visual |
| --- | --- | --- |
| Fish crate | `intact`, `damaged`, `knocked_open`, `carried`, `empty` | Cracks, fish spill, missing crate while carried. |
| Ice tub | `intact`, `melting`, `melted` | Ice shrinks, puddle grows. |
| Awning pole | `intact`, `damaged`, `broken`, `temporary_repaired` | Pole bends, awning sags. |
| Cat bed | `empty`, `active`, `abandoned`, `temporary_repaired` | Cushion, paw print, repair tape. |
| Market Scale | `loaded`, `low`, `empty` | Stock gauge dims. |
| Closed sign | `hidden`, `title`, `hung` | Board appears/sways. |
| Tilting sign | `normal`, `tilting` | Rotates, drips. |
| Darkened stall | `open`, `darkened` | Lamp off, gray fish. |

---

# 6. AUDIO

| Sound name | Recipe | When it plays |
| --- | --- | --- |
| `bell_market` | Two sine oscillators at 880Hz and 1320Hz, attack 0.01s, decay 1.2s, lowpass 2400Hz. | Wave start, wave end, early bell. |
| `closed_sign_lift` | Short wood knock: filtered noise burst 400Hz center, decay 0.18s. | Start run. |
| `closed_sign_hang` | Heavier wood knock 180Hz, decay 0.5s, slight pitch down. | Game over. |
| `gull_cry` | Sawtooth 700Hz to 400Hz, vibrato 12Hz, decay 0.35s. | Seagull spawn/attack. |
| `rat_squeak` | Square 1800Hz short pulses, decay 0.12s, lowpass 2500Hz. | Rat spawn/nibble. |
| `raccoon_grunt` | Triangle 180Hz to 120Hz with noise layer, decay 0.4s. | Raccoon spawn/carry. |
| `brute_step` | Low sine 90Hz thump, decay 0.18s. | Larger thief step/occupy. |
| `sale_coin` | Sine 1200Hz to 1600Hz, two quick notes, decay 0.25s. | Successful sale. |
| `customer_leave` | Soft wood cart roll: filtered noise 300Hz, decay 0.3s. | Lost customer. |
| `cat_trick` | Sine 500Hz to 900Hz, fast envelope, decay 0.18s. | Cat attack. |
| `cat_overwhelmed` | Low triangle 180Hz downward, decay 0.35s. | Cat overwhelmed. |
| `bed_repair` | Wood tap plus tape rustle: noise burst 900Hz, decay 0.2s. | Repair success. |
| `ice_melt` | Slow water drip: filtered noise 1200Hz random pulses. | Ice reaches melted. |
| `crate_break` | Noise burst 500Hz with comb filter, decay 0.25s. | Crate knocked open. |
| `awning_drop` | Heavy cloth/wood crash: noise 200Hz + sine 100Hz, decay 0.5s. | Awning Drop. |
| `yarn_tangle` | Bouncing triangle 300Hz to 600Hz, 3 pulses, 0.6s. | Yarn Ball Tangle. |
| `catnip_nap` | Soft sine 220Hz slow attack, decay 0.8s. | Catnip Nap. |
| `hairball_frenzy` | Rapid square 400Hz pulses, 0.5s. | Hairball Frenzy. |
| `gull_king_roar` | Sawtooth 120Hz to 80Hz + bird noise, decay 1.2s. | Gull King spawn. |
| `closing_blow` | Low sine 60Hz boom + noise, decay 1.0s. | Gull King reaches Market Scale. |
| `joke_pop` | Short sine 800Hz blip, decay 0.1s. | Automatic joke. |
| `post_wave_nap` | Soft 180Hz sine, slow fade, 1.0s. | Post-wave nap joke. |

---

# 7. UX

All screens and HUD are HTML/CSS only. The market world is rendered with absolutely positioned DOM/SVG elements. Pointer events use flat hit areas that match the visual layout.

## Screen state machine

```text
ClosedTitle
  liftClosedSign / Enter -> Prep

Prep
  ringBell / bellTimer=0 -> Wave

Wave
  all enemies resolved AND stock > 0 -> Prep
  stock <= 0 -> GameOver

Prep
  stock <= 0 -> GameOver

GameOver
  restart -> ClosedTitle
```

## Screens

| Screen | HTML elements | CSS state |
| --- | --- | --- |
| ClosedTitle | `#screen-title`, `#closed-sign` | `.phase-title` |
| Prep | `#screen-prep`, `#build-menu`, `#repair-menu`, `#bell-button` | `.phase-prep` |
| Wave | `#screen-wave`, `#ability-bar`, `#wave-warning` | `.phase-wave` |
| GameOver | `#screen-gameover`, `#closed-sign-hung`, `#score-panel` | `.phase-gameover` |

## HUD table

| Element | Record field | Visible when |
| --- | --- | --- |
| Stock gauge | `globalContext.stock` | Always after run start. |
| Coin counter | `globalContext.coins` | Always after run start. |
| Wave counter | `globalContext.wave` | Always after run start. |
| Bell timer | `globalContext.bellTimer` | Prep. |
| Customer flow | `globalContext.customerFlow` | Prep and Wave. |
| Customers served | `globalContext.servedCustomers` | Wave and GameOver. |
| Customers lost | `globalContext.lostCustomers` | Wave and GameOver. |
| Build menu | cat costs, cat types | Prep. |
| Repair menu | repair costs, target state | Prep. |
| Ability bar | ability costs, cooldowns | Wave, Tier 2. |
| Spread too thin warning | `warnings.spreadTooThin` | Wave. |
| Gap warning | `warnings.gap` | Wave. |
| Tilting lane warning | `warnings.tiltingLanes` | Wave. |
| Score panel | `score`, `bestScore` | Wave end, GameOver, Tier 2. |
| Closed sign | `phase == gameover` | GameOver. |
| Joke callouts | `jokes` | Tier 2 automatic feedback. |

---

# 8. DEBUG API

| Function | System | Purpose |
| --- | --- | --- |
| `debug.state.getState()` | state | Read full state. |
| `debug.state.setPhase(phase)` | state | Force phase. |
| `debug.state.startRun(seed)` | state | Start deterministic run. |
| `debug.world.getNode(id)` | world | Read node. |
| `debug.world.setStallField(stallId, field, value)` | world | Force market state. |
| `debug.build.place(type, padId)` | building | Force place cat. |
| `debug.build.repair(targetId)` | building | Force repair. |
| `debug.build.buyTemporary(targetId)` | building | Force temporary repair. |
| `debug.combat.getCoverage(nodeId, type)` | combat | Read coverage. |
| `debug.combat.damageEnemy(enemyId, amount)` | combat | Force damage. |
| `debug.combat.overwhelmCat(catId)` | combat | Force overwhelm. |
| `debug.waves.startWave(number)` | waves | Force wave. |
| `debug.waves.spawn(type, lane)` | waves | Force spawn. |
| `debug.waves.endWave()` | waves | Force wave end. |
| `debug.economy.setStock(value)` | economy | Set stock. |
| `debug.economy.setCoins(value)` | economy | Set coins. |
| `debug.economy.spawnCustomer(lane)` | economy | Force customer. |
| `debug.economy.serveCustomer(id)` | economy | Force sale. |
| `debug.economy.loseCustomer(id)` | economy | Force lost customer. |
| `debug.abilities.charge(id)` | abilities | Charge ability. |
| `debug.abilities.use(id, target)` | abilities | Use ability. |
| `debug.score.recordWave()` | scoring | Force score record. |
| `debug.score.getScore()` | scoring | Read score. |
| `debug.input.liftClosedSign()` | input | Simulate start. |
| `debug.input.ringBell()` | input | Simulate bell. |
| `debug.input.clickPad(padId)` | input | Simulate build click. |
| `debug.input.clickRepair(targetId)` | input | Simulate repair click. |
| `debug.input.clickAbility(id, target)` | input | Simulate ability click. |

---

# 9. TESTS

## Tier 1 tests

| Test | Pass condition |
| --- | --- |
| Deterministic seed | Same seed produces same RNG sequence and same first-wave spawn schedule. |
| Start run | `phase=prep`, `stock=100`, `coins=30`, `customerFlow=6`. |
| Closed sign game over | Setting `stock=0` sets `phase=gameover` and shows Closed sign. |
| Build placement | Placing Mackerel reduces coins, creates active cat bed, and covers target node. |
| Insufficient coins | Build fails and coins unchanged. |
| Abandoned bed | Overwhelmed cat sets bed `abandoned`, cannot build there until repaired. |
| Repair bed | Repair restores active bed. |
| Wave spawn | Wave 1 spawns exact table enemies. |
| Ground pathing | Rat follows `EN -> S1 -> S2 -> S3 -> S4 -> exit/scale` without teleporting. |
| Air pathing | Seagull moves directly to target and ignores ground nodes. |
| Cat kills enemy | Enemy in range is damaged and defeated before target. |
| Target breach | Enemy reaching target causes stock loss. |
| Overwhelm | Enemy reaching covered target abandons one responsible cat. |
| No cat lost on gap | Enemy reaching uncovered target causes loss but no cat abandoned. |
| Customer sale | Customer completes sale, stock -1, coins increase. |
| Customer blocked | Customer leaves, `customerFlow` decreases, stock unchanged. |
| Ice melt effect | Melted ice reduces sale value and causes stock decay. |
| Crate knock-open | Crate integrity <50 causes instant stock loss and rat bonus. |
| Awning broken | Broken awning creates tilting sign and reduces customer spawn weight. |
| Temporary repair | Temporary repair restores target, expires after 45s. |
| Wave end | Wave ends only when all enemies resolved. |
| Gull King closing blow | Gull King reaching Market Scale causes -30 stock. |
| Hunger scaling | Lost stock/customers increase next wave HP/speed. |

## Tier 2 tests

| Test | Pass condition |
| --- | --- |
| Ability charge | Charging reduces coins and sets ready. |
| Ability cooldown | Using starts cooldown; cannot reuse until expired. |
| Yarn valid | Stops enemies in line for 4s. |
| Yarn invalid | Fizzles, starts cooldown, no gameplay effect. |
| Nap valid | Puts enemies asleep, cancels theft. |
| Frenzy valid | Doubles nearby cat attack speed and adds +1 damage. |
| Awning Drop valid | Damages enemies and pole, blocks gap temporarily. |
| Scoring wave end | Score updates only at wave end. |
| Perfect wave bonus | Zero stock loss wave increments perfect waves. |
| Penalty record | Darkened stalls, abandoned beds, lost customers penalize score. |
| Best score | Game over stores best score in `localStorage`. |

## Tier 3 tests

| Test | Pass condition |
| --- | --- |
| No extra mechanics | No new systems beyond Tier 1 and Tier 2. |

---

# 10. BUILD ORDER

1. Create HTML/CSS shell, fixed loop, state machine, RNG, debug/test harness.
2. Build market graph, node coordinates, DOM/SVG market layout, oblique visual style.
3. Implement Closed sign title, start run, Market Scale stock, game over.
4. Implement build pads, cat bed placement, coverage, and cat stats.
5. Implement enemy spawn, graph movement, and basic wave table.
6. Implement combat: targeting, damage, defeat, target reach, stock loss.
7. Implement overwhelm and cat bed abandonment.
8. Implement customers, sales, coins, customer flow, and customer blocking.
9. Implement market degradation: crates, ice, awnings, darkened stalls, tilting signs.
10. Implement repairs and temporary repairs.
11. Implement wave scaling, hunger, endless waves, and Gull King.
12. Add synthesized audio and visual states for all Tier 1 effects.
13. Add Tier 2 abilities with valid/invalid targeting and cooldowns.
14. Add Tier 2 scoring, wave-end recording, score panel, and best score.
15. Add automatic jokes as feedback only.
16. Run Tier 1 tests, then Tier 2 tests.

---

# 11. DEFINITION OF DONE

## Tier 1 Definition of Done

The Tier 1 game is done when a player can start a deterministic run, prepare cats, play at least one full wave with customers and thieves, see the market degrade and recover through repairs, and lose when the Market Scale stock reaches zero.

- [ ] Fixed-step loop and deterministic RNG exist.
- [ ] Title screen shows Closed sign and can start run.
- [ ] Market graph has 3 lanes, 12 stalls, Market Scale, exits, customer entrances, awning poles, and 16 build pads.
- [ ] Stock starts at 100 and decreases correctly from sales, theft, decay, and breaches.
- [ ] Coins start at 30 and increase only from sales.
- [ ] Cat beds can be placed in prep and cannot be placed during wave.
- [ ] All five cat types have defined coverage, costs, attacks, and specials.
- [ ] Coverage determines whether target nodes are safe.
- [ ] Enemies follow correct paths and target rules.
- [ ] Seagulls fly and steal; rats nibble; raccoons carry crates; larger thieves occupy weak points.
- [ ] Gull King can appear, summon, try to carry, and cause closing blow.
- [ ] Cats overwhelm and abandon beds under the defined rule.
- [ ] Customers spawn, move, buy, or leave based on path and stall state.
- [ ] Customer flow changes with served/lost customers.
- [ ] Ice, crates, awnings, darkened stalls, and tilting signs behave as specified.
- [ ] Repairs and temporary repairs work.
- [ ] Waves 1–10 use the fixed table; endless waves scale.
- [ ] Hunger scaling affects later waves.
- [ ] Game over hangs Closed sign when stock reaches zero.
- [ ] Tier 1 tests pass.

## Tier 2 Definition of Done

The Tier 2 game is done when the player can charge and use the four market abilities and see scoring records quality after each wave.

- [ ] Ability charging costs coins and creates cooldowns.
- [ ] Yarn Ball Tangle, Catnip Nap, Hairball Frenzy, and Awning Drop work as specified.
- [ ] Invalid ability targets fizzle and start cooldown.
- [ ] Score formula updates at wave end.
- [ ] Penalties and bonuses are recorded.
- [ ] Best score persists.
- [ ] Jokes appear only as automatic feedback.
- [ ] Tier 2 tests pass.

## Tier 3 Definition of Done

- [ ] No extra gameplay systems are added.
- [ ] Optional polish does not change rules.

---

# A. SANITY

| Check | Result | Notes |
| --- | --- | --- |
| All required headings present | Pass | Headings match requested order. |
| Tier 1 contains exactly core mechanics | Pass | Combat, building, waves, economy, and required market degradation are in Tier 1. |
| Supporting mechanics are Tier 2 | Pass | Abilities and scoring are Tier 2. |
| Extra mechanics none | Pass | Tier 3 has no new systems. |
| No new systems beyond prompt | Pass | No city builder, cat raising, cooking, action control, pickups, or player-triggered jokes. |
| All content roster included | Pass | Forecat, five cats, enemy types, Gull King, market objects, abilities, scoring, jokes included. |
| Concrete numbers provided | Pass | Units, costs, HP, ranges, wave table, scoring formula, UI fields included. |
| Player input defined | Pass | Pointer/keyboard actions mapped to systems. |
| Run structure defined | Pass | Title, prep, wave, game over. |
| View within style | Pass | Wet dawn fish market, oblique overhead, failure visuals. |
| Audio defined | Pass | Synthesized sound recipes table. |
| HTML/CSS only for screens | Pass | DOM/SVG/CSS; no canvas/WebGL. |
| Global context includes all gameplay records | Pass | State fields cover all systems and tests. |
| Module specifics include functions needed by rules/tests | Pass | Each system has required functions. |
| Tests validate each tier | Pass | Tier 1 and Tier 2 test lists. |
| Definition of done matches tiers | Pass | Tier 1/2 done lists match Section 0.3. |
| Numbers internally consistent | Pass | Stock totals, sale values, costs, wave scaling, and penalties use same units. |
| Jokes do not create separate rules | Pass | Jokes are feedback only. |
| Closed sign rule consistent | Pass | In-run Closed sign appears only at game over; title sign is the pre-run sign being lifted. |