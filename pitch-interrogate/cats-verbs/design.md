# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Browser game. | `1.2 Important conventions`, `2.1 Module layout`, `7. UX` |
| A tower defense game where cats defend a fish market. | `0.2 Decisions`, `4. GAMEPLAY SPEC`, `4.7 Enemy Raids`, `4.8 Basic Market Defenses`, `5. CHARACTERS` |
| Real-time market defense, not turn-based. | `1.1 Units, axes, frames`, `4.1 Run Structure and Night State`, `4.3 Customers`, `4.6 Cat Units`, `4.7 Enemy Raids` |
| Player is the head cat and keeper of a wet dockside fish market at night. | `0.2 Decisions`, `7. UX`, `4.1 Run Structure`, `4.5 Resources` |
| Assign cats to posts, patrols, alarms, and market objects. | `4.6 Cat Units`, `4.10 Advanced Cat Roles and Patrol`, `8. DEBUG API` |
| Place market defenses. | `4.8 Basic Market Defenses`, `4.14 Advanced Market Objects`, `7. UX` |
| Manage fresh fish, ice, scraps, coins. | `4.5 Resources, Economy, and Upkeep`, `4.4 Stock and Fish Supply`, `7. UX` |
| Use the market’s own objects to keep stalls open. | `4.8`, `4.14`, `5. CHARACTERS` |
| Gulls, seagulls, raccoons, rival cats, and dock hazards raid the aisles. | `4.7 Enemy Raids and Hazards`, `4.15 Progression and Strange Raids` |
| Cats are not obedient machines: distracted, hungry, frightened, curious, tired, pulled by habits, fish, naps, other cats, bells. | `4.6 Cat Units`, `4.10`, `4.11`, `4.12`, `4.17` |
| Market is open, fragile, smelly, full of things that fail: ice melts, fish spoils, aisles slippery/noisy, customers complain/panic, stalls blocked/ruined/occupied/taken over. | `4.2 Market, Stalls, and Aisles`, `4.3 Customers`, `4.4 Stock`, `4.5 Upkeep`, `4.16 Cascading Failure` |
| Player decides what to protect, repair, let fail, and which failure to absorb. | `4.2`, `4.5`, `4.16`, `7. UX` |
| Night ends when dawn bell rings. | `4.1 Run Structure`, `4.9 Bell and Emergency Response` |
| Win if market still open. | `4.1 Run Structure`, `4.16` |
| Lose if enough stalls lost or market cannot serve any customer for a full raid. | `4.1 Run Structure`, `4.3 Customers` |
| Fixed angled overhead view of whole market, with stalls, aisles, stock, customers, cats, enemies, defenses, market states visible. | `3. VISUAL SPEC`, `4.2`, `5. CHARACTERS` |
| Clear panels for coins, fresh fish, ice, scraps, cat orders, stall condition. | `7. UX`, `4.5`, `4.6` |
| Real-time upkeep, spoilage, cat behavior, customer patience run continuously. | `4.1`, `4.2`, `4.3`, `4.5`, `4.6` |
| During a raid: enemies enter, cats fight/chase, objects break, emergency orders, bell, placed defenses. | `4.1`, `4.6`, `4.7`, `4.8`, `4.9` |
| Between raids: build, repair, sell fish, spend coins, reassign cats, choose sacrifice. | `4.1`, `4.5`, `4.8`, `4.14`, `7. UX` |
| Run starts with market waking up, cats asleep, fish under lamps, initial stock, initial defenses, first stall choice. | `4.1`, `4.2`, `4.3`, `4.4`, `5. CHARACTERS` |
| First raid begins when market opens and customers arrive. | `4.1`, `4.3`, `4.7` |
| Run ends at dawn bell. Market open means majority trade stalls functional and at least one customer buying. | `4.1`, `4.2`, `4.3` |
| Market lost if majority stalls ruined/closed/occupied, or cannot serve any customer for full raid. | `4.1`, `4.2`, `4.3` |
| Night progresses: upkeep rises, ice melts faster, enemies bring tactics, stalls fragile, customers nervous, random problems more often. | `4.15 Progression and Strange Raids`, `4.16 Cascading Failure` |
| Tone: wet, smelly, funny fish market defended by cats. | `3. VISUAL SPEC`, `4. GAMEPLAY SPEC`, `5. CHARACTERS`, `6. AUDIO` |
| Not a generic medieval tower defense with wizards/castles. | `0.2 Decisions`, `3. VISUAL SPEC`, `4. GAMEPLAY SPEC` |
| Not about winning a battle on a clean path. | `4.2`, `4.7`, `4.15` |
| Not a platformer, stealth, one-cat survival, story RPG, farm, racing, rooftop cat game. | `0.2 Decisions`, `A. SANITY` |
| The game has exactly the listed parts; no added systems. | `0.2 Decisions`, `4. GAMEPLAY SPEC`, `A. SANITY` |

## 0.2 Decisions

| Decision | Ruling | Why |
| --- | --- | --- |
| Player is head cat and keeper, not one small cat with health/needs. | No player avatar. The player issues orders through the HUD and market selection. | Preserves the stated role and prevents one-cat survival. |
| Fixed angled overhead view. | Use a 960×720 market viewport with a pseudo-2.5D angled overhead look: y position implies depth, objects have height offsets, no camera scrolling. | Shows the whole market and required panels. |
| Whole market visible plus clear panels. | Market canvas is left, HTML/CSS HUD is right 320px. | Keeps required panels readable and separate from canvas. |
| Market contains stalls and aisles. | Exactly 7 trade stalls and 7 aisles, one per stall. | Makes “majority” well-defined: 4 of 7. |
| Majority means majority of trade stalls. | 4 or more stalls are majority. | Simple, testable. |
| Stall open/functional/closed/ruined/occupied are distinct states. | Implement as flags plus computed `canServe`, `isFunctional`, `isClosed`, `isRuined`, `isOccupied`. | Required by market survival rules. |
| “No sellable stock” means no fish unit with freshness ≥ 60 or stock count 0. | A stall with only spoiled fish is `CLOSED` for loss counting. | Matches “closed if it has no sellable stock”. |
| A stall can be opened by the player for free during Setup/Between. | Opening does not wake cats or guarantee trade; it only enables trading if functional. | Lets player choose first stall to trade. |
| Closing a stall stops its upkeep and spoilage. | Closed stalls cannot trade, do not decay, and count toward loss if majority closed. | Creates forced sacrifice. |
| Repair returns an object to a weaker version. | Repaired stalls/defenses have max durability/counter 70 after repair, not 100. | Matches “weaker version”. |
| Occupation lasts until cleared by cat, bell, or player closing aisle. | Bell and cat combat clear occupation; closing occupied stall removes enemy but still leaves stall damaged. | Matches stated clearing methods. |
| After clearing occupation, if not repaired, stall becomes ruined. | After occupation ends, `repairDeadline = 60s`; if counter HP ≤ 30 and no repair, state becomes `RUINED`. | Creates cascade without instant death. |
| Customers enter through market gate only when market open and gate not blocked/occupied. | Gate is a market state: `OPEN`, `BLOCKED`, `OCCUPIED`. | Required by customer rules. |
| Customer service means reaching a stall, paying, reducing stock. | Sale has 1.5s service time and can be interrupted by panic. | Makes “if customer panics first, sale fails” concrete. |
| No customers means no coins and no win. | If market not open or gate blocked/occupied, no customer spawn. | Required. |
| Fish units are individual units with freshness. | Each stall has `stock: fishUnit[]`; freshness is per unit, not a single average. | Makes bad fish, sale price, spoilage, and removal concrete. |
| Initial stock includes crates behind stalls and laid-out stock. | All 7 stalls begin with fish units; player chooses which to open. | Matches run start. |
| Dock cart drops crates at loading rail at set points. | Dock cart events at t = 120, 300, 480. Payloads: fresh fish, ice, scraps. | Supplies stock without adding a shop. |
| Cat can haul crate to stall. | `Haul Crate` order: cat moves to crate, picks up, carries to target stall. | Required stock rule. |
| Fish can be reclaimed from flung trout or caught pest carrying one. | Flung trout is Tier 2; caught small enemies drop carried fish items in Tier 1. | Matches stock rules. |
| Player can move stock between stalls. | `Move Stock` order moves one fish unit at a time and leaves source reduced. | Required. |
| Market has four resources: coins, fresh fish, ice, scraps. | Fresh fish is represented by sellable fish units across stalls. No separate global fresh fish pool. | Keeps economy tied to market state. |
| Coins come from customers buying fish. | Customer sale is the only coin source. | Matches economy. |
| Fresh fish can be sold, stolen, eaten, spoiled. | Sales remove units; enemies steal; cats can eat bait; decay spoils units. | Matches rules. |
| Ice keeps stalls fresh and melts. | Ice boxes consume ice over time and reduce fish decay. | Matches core. |
| Scraps come from broken crates, nets, fish bones, waste. | Broken defenses/objects produce scraps; repair consumes them. | Matches economy. |
| Building, repairs, hiring, feeding, keeping stalls fresh cost resources. | Costs are explicit in `4.5` and `4.8`. | Required. |
| A working stall requires ice, cleaning, repair. | Upkeep actions: ice assignment, clean stall, repair structure. | Required. |
| A working defense requires durability and materials if bait/weight based. | Defenses have durability; traps require reset; baited/weighted objects require scraps or materials. | Required. |
| A working cat requires food, rest, not being overworked. | Cats have energy, hunger, condition, obedience. | Required. |
| If upkeep cannot be paid, stall spoils, cat ignores orders, defense fails. | No resources means actions fail and states degrade. | Required. |
| Cats obtained from starting roster, hired as strays between raids, or returned if fed and kept safe. | Starting roster is three named cats; one hire type “Stray Market Cat”; injured cats can be healed by feed/rest. | Required. |
| Starting cats are asleep in safe corners. | All starting cats begin `ASLEEP` at safe corners. | Required. |
| Assigning a sleeping cat does not wake it. | Assignment sets target zone only; sleep remains until wake condition. | Required. |
| Wake by feed, pay scrap, or market noise. | Feed wakes with positive effects; scrap wake wakes with obedience penalty; bell wakes nearby with fear/customer penalty. | Required. |
| If left asleep during first raid, does nothing; if enemies reach it, startled, flee, noise panics customers. | Sleeping cat woken by enemy: fear +30, flees, adds noise, nearby customers lose patience. | Required. |
| Player may assign cats to zones, order chase, guard, return, rest, repair, use defenses and market objects. | Commands are explicit input actions. | Required. |
| Player cannot directly attack enemies. | No direct attack input. Only cats and objects act. | Required. |
| Orders only work if cat present, awake, fed, not panicked, not more strongly pulled by habit or nearby fish. | Obedience gate checks those states. | Required. |
| Assigning sends cat to zone and holds it there. | `Assign Zone` sets assigned zone and move target. | Required. |
| Guard means attack first enemy in zone. | Guard state scans assigned aisle. | Required. |
| Chase means follow one enemy until caught, driven off, or leaves market. | Chase state targets one enemy. | Required. |
| Repair means spend time and scraps to restore stall/defense. | Repair order consumes scraps and progress timer. | Required. |
| Rest means cannot act but recovers obedience and condition. | Rest state blocks orders, restores stats. | Required. |
| Fighting exchanges damage with whatever it can reach. | Combat applies damage per second in range. | Required. |
| Cat injured when condition fails and flees/hides; lost if leaves market or not brought back. | Condition 0 -> injured, hides; outside bounds -> removed. | Required. |
| Feeding, resting, and cleaning repair cats. | Feed adds condition/energy; rest heals; clean aisle improves rest healing. | Required. |
| Obedience falls when hungry, frightened, overworked; rises when fed and successful. | Obedience modifiers explicit. | Required. |
| Cat naps on its own when calm, overworked, hungry, not fed. | Auto-nap conditions explicit. | Required. |
| While napping, ignores orders; zone open. | Sleep disables commands and combat. | Required. |
| Nap wakes by enemy entering zone, bell, another cat, feed. | Wake triggers explicit. | Required. |
| Obedience drops while napping and further if woken by scare. | Sleep and scare penalties explicit. | Required. |
| Raid begins when enemies cross into market. | Raids spawn from docks/alleys/roofs. | Required. |
| Raid ends when every enemy fled/driven off/caught/left with loot. | Raid active until all spawned enemies removed. | Required. |
| Enemies are hungry, fast, stupid, opportunistic. | Enemy AI uses target weights, not complex tactics. | Required. |
| If enemies pass through gap, move toward nearest bait/stall/stock. | Target selection uses bait/stock/richness/distance. | Required. |
| If reach protected thing, it is damaged/opened/stolen/spoiled. | Interactions defined per enemy. | Required. |
| If not stopped, target changes state and enemy leaves with loot. | Interaction completion changes state and spawns loot. | Required. |
| Enemy caught if small enough and defeated; driven off if fear/pain; leaves with loot if reaches target. | Small enemies can be caught; large driven off. | Required. |
| Enemies stopped by cats, intact defenses, traps, nets, driven off. | All listed stop types implemented. | Required. |
| Gulls target exposed fish, signs, open lids; dive, steal small fish, spoil stalls. | Gull stats and interactions defined. | Required. |
| Seagulls are larger, bolder harbor variant; dive at stalls, knock customers, carry bigger fish. | Seagull stats and customer knock defined. | Required. |
| Raccoons target closed containers and barricades; open lids, pull crates, steal stock. | Raccoon interactions defined. | Required. |
| Rival cats target high-value stalls and market cats; fight, steal fish, lure defenders. | Rival cat combat and taunt defined. | Required. |
| Dockworkers are hazards: knock crates, create spills, make aisles slippery. | Dockworker hazard entity defined. | Required. |
| Basic market defenses: netted awnings, ice boxes, fish-barrel barricades, hooks, ropes, little traps. | Exactly those Tier 1 defense types. | Required. |
| Netted awnings block gulls. | Gulls cannot enter covered area; may peck awning. | Required. |
| Ice boxes keep stalls fresh but melt. | Ice boxes store ice and reduce fish decay. | Required. |
| Fish-barrel barricades slow/block enemies but can be knocked over. | Barricades block nodes and take damage. | Required. |
| Hooks and ropes snag enemies or trigger traps. | Hook/rope interactions defined. | Required. |
| Traps catch small pests but must be reset. | Trap catches gulls/small pests; reset required. | Required. |
| Defense states: weakened, broken, reset by repair, left as scrap if not repaired. | Durability states and scrap drop implemented. | Required. |
| Objects are real if intact and correctly placed; decorative if only look useful. | Placement validity rules; invalid objects are `DECORATIVE` with no active effect. | Required. |
| Fish-market bell wakes nearby cats, pulls attention, can make them break post, makes customers nervous. | Bell radius, effects, cooldown defined. | Required. |
| Dawn bell is not a tool and cannot be rung/delayed/controlled. | Dawn is fixed at t = 720. | Required. |
| Advanced cat roles and patrol are supporting. | Alarm cat and patrol line are Tier 2. | Required. |
| General alarm cat watches entrances/aisles/whole market and yowls. | Alarm zone and yowl effects defined. | Tier 2. |
| Patrol line drawn through aisle/row; cat walks line and attacks along it. | Patrol input and path defined. | Tier 2. |
| Bait, tempting fish, cat-cat events are supporting. | Bait items and cat-cat events are Tier 2. | Required. |
| Tempting fish are physical bait items and pull cats/enemies. | Bait items with radius and weights defined. | Tier 2. |
| Cat breaks post if hunger/curiosity/habit stronger than order. | Break-post checks defined. | Tier 2. |
| Cat-cat events: groom, follow, block. | Cat proximity event table defined. | Tier 2. |
| Bad fish detection and removal is supporting. | Whisker detection and dump order are Tier 2. | Required. |
| Bad fish lowers customer patience, attracts pests, causes complaints. | Bad fish state effects defined. | Tier 2. |
| Flung trout events are supporting. | Flung fish event is Tier 2. | Required. |
| Flung trout is not enemy/player-controlled object. | Event spawns temporary flying fish object. | Tier 2. |
| Flung trout can distract cats, lower customer patience, create slippery patch. | Event effects defined. | Tier 2. |
| Advanced market objects: net launchers, eel barrels, salted herring barrels, broken scale. | Those exact objects added in Tier 2. | Required. |
| Net launchers stun flying enemies. | Stun range/cooldown/durability defined. | Tier 2. |
| Eel barrels make aisles slippery and slip enemies into traps. | Slip and trap interaction defined. | Tier 2. |
| Salted herring barrels are preserved stock and strong bait; closed safe, open sellable/baiting. | Barrel state and sale rules defined. | Tier 2. |
| Broken scale measures weight/freshness; false readings; broken prop; repair accurate. | Scale object states defined. | Tier 2. |
| Smoked eels are high-value guarded stock. | A04 becomes smoked eel stall in Tier 2. | Tier 2. |
| Flying trout and flung fish event. | Same as flung trout. | Tier 2. |
| Dock cart and loading rail. | Dock cart events and haul order. | Core stock, simple version Tier 1. |
| Market gate. | Gate state and customer spawn rules. | Tier 1. |
| General alarm cat. | Tier 2. | Required. |
| Patrol line. | Tier 2. | Required. |
| Tempting fish. | Tier 2. | Required. |
| Bad fish. | Tier 1 has spoiled fish units; detection/removal are Tier 2. | Required. |
| Defenses only for show. | Invalid placement state. | Tier 1. |
| Mackerel Mouth ignores gulls but hates seagulls. | Named trait activated in Tier 2. | Content tied to enemy behavior. |
| Boots patrols well but naps after empty patrol loops. | Named patrol trait activated in Tier 2. | Content tied to patrol. |
| Whisker smells bad fish before customers. | Named detection trait activated in Tier 2. | Content tied to bad fish. |
| Gulls, seagulls, raccoons, rival cats, dockworkers, customers. | Tier 1 enemy/hazard/customer roster. | Core. |
| No Gulls sign. | Placeable deterrent and gull steal event, Tier 2. | Supporting joke/enemy action. |
| Cat grooming during raid is distraction. | Tier 2 behavior. | Supporting joke rule. |
| Gull stealing sign removes deterrent and tempts area. | Tier 2. | Supporting joke rule. |
| Customers complaining about smell during attack is state change. | Complaint/panic state changes Tier 1; joke presentation Tier 2. | Core customer state. |
| Sleeping cats. | Tier 1. | Core cat rules. |
| Dawn bell. | Tier 1. | Core run end. |
| Fish-market bell. | Tier 1. | Core emergency response. |
| Basic market objects. | Tier 1. | Core defenses. |
| Advanced market objects. | Tier 2. | Supporting. |
| Run length. | 12 minutes: 0–60 setup, 60–720 night, dawn at 720. | Provides a full night and multiple raids. |
| Number of raids. | 6 scheduled raids, no overlap. | Keeps “between raids” meaningful. |
| Screen size. | 1280×720 total: 960×720 market, 320×720 HUD. | Fixed overhead view plus panels. |
| Market layout. | 7 vertical aisles from gate to stalls, spawn points at docks/roof/alleys, safe corners, loading rail. | Concrete, testable. |
| Input. | Mouse/touch selection plus keyboard shortcuts for orders, bell, building, opening/closing, repair, patrol drawing. | Makes every mechanic a named input. |
| Determinism. | Seeded PRNG and fixed 60Hz update. | Tests and reproducibility. |
| No pause. | No pause state. | Real-time requirement. |
| UI. | HTML/CSS HUD; canvas only market. | Required UX constraint. |
| Audio. | Synthesized Web Audio only, no external assets. | Builder has audio API and style constraints. |

## 0.3 Tiers

### Tier 1 — Core playable market defense

Tier 1 is a complete, finishable game using only core mechanics:

- Fixed step loop, seeded RNG, deterministic input queue.
- 960×720 market, 7 stalls, 7 aisles, gate, safe corners, loading rail.
- Setup phase, night open phase, dawn end.
- Stall states: open, functional, closed, ruined, occupied, blocked, protected, bait, rich, safe, problematic.
- Fish units, stock, spoilage, bad fish state, dock cart, haul/move stock.
- Customer spawn, target selection, complaints, panic, sale, exit.
- Resources: coins, ice, scraps, sellable fish count.
- Upkeep: ice boxes, cleaning, repairs, closing, hiring, feeding.
- Cat units: three starting cats with base behavior, one hire type, commands assign/guard/chase/return/rest/repair/feed/wake/haul/move stock.
- Cat obedience, hunger, energy, fear, injury, hiding, auto-naps, wake triggers.
- Enemy roster: gulls, seagulls, raccoons, rival cats, dockworkers.
- 6 scheduled raids with fixed compositions.
- Basic defenses: netted awnings, ice boxes, fish-barrel barricades, hooks, ropes, little traps.
- Object validity/real/decorative/weak/broken/repair states.
- Fish-market bell and dawn bell.
- Win/loss evaluation.
- Full HUD, visual style, synthesized sounds, debug API, tests.

### Tier 2 — Supporting mechanics and named content

Tier 2 adds complete additions on top of Tier 1:

- General alarm cat, patrol line, Boots patrol/nap trait, Mackerel Mouth gull/seagull trait, Whisker bad-fish trait.
- Tempting fish/bait, cat-cat events.
- Bad fish detection and removal.
- Flung trout events.
- Advanced market objects: net launcher, eel barrel, salted herring barrel, broken scale, smoked eels.
- Progression and strange raids: state-based wave modifiers and problem frequency.
- Cascading failure indicators and forced sacrifice UI.
- Joke behavior rules: No Gulls sign, cat grooming, sign stealing, complaint escalation.

### Tier 3 — Mastery, legibility, and polish

Tier 3 is optional polish on a working game:

- Market legibility overlays: aisle risk heat, cat obedience bars, enemy intent arrows, bad fish markers, decorative object warnings.
- After 10 minutes, mastery hints and predicted threat paths.
- Tuning for balance and readability.
- Extra market ambience and microfeedback.

---

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Quantity | Unit | Range / default | Notes |
| --- | --- | --- | --- |
| Game time | seconds | 0–720 | Dawn at 720. |
| Update step | seconds | fixed `dt = 1/60` | No variable step. |
| Frame rate | Hz | 60 | Fixed simulation. |
| Market viewport | pixels | 960×720 | Canvas market area. |
| HUD | pixels | 320×720 | HTML/CSS right panel. |
| Total screen | pixels | 1280×720 | Fixed design size, scaled by CSS. |
| Coordinates | pixels | origin top-left, x right, y down | Visual angle is rendering only. |
| Speed | pixels/second | usually 30–80 | Units move along node paths. |
| HP, condition, durability, counter HP | points | 0–100 except dockworker | 0 is broken/injured. |
| Freshness | points | 0–100 | ≥60 sellable, <60 bad fish. |
| Cleanliness | points | 0–100 | <40 problematic for customers. |
| Noise | points | 0–100 | >60 problematic for customers. |
| Slip | points | 0–100 | >60 problematic for customers. |
| Obedience | points | 0–100 | ≥60 required for most orders. |
| Energy | points | 0–100 | <30 blocks orders, <25 auto-nap. |
| Hunger | points | 0–100 | >60 break-post risk, >70 auto-nap risk. |
| Fear | points | 0–100 | ≥50 blocks orders, ≥60 enemy flees. |
| Patience | points | 0–100 | Customer state. |
| Coins | integer | ≥0 | Customers buy fish. |
| Ice | integer | ≥0 | Consumed by ice boxes/refills. |
| Scraps | integer | ≥0 | Repairs, feeding, traps. |
| Fish units | integer count | per stall max 12 | Each unit has freshness. |
| Raid index | integer | 1–6 | Scheduled. |
| IDs | string | `A01`–`A07`, `cat_...`, `enemy_...` | Stable for tests. |

## 1.2 Important conventions

1. **Fixed step loop only.**
   - Simulation runs at exactly `dt = 1/60`.
   - Render interpolation may be used for visuals only.
   - No gameplay logic uses wall-clock delta.

2. **Seeded PRNG.**
   - Use a deterministic PRNG such as Mulberry32.
   - All randomness comes from `state.rng.next()`.
   - No `Math.random()` gameplay use.
   - Seed is stored in `state.seed`.

3. **No external assets.**
   - Visuals are Canvas 2D vector shapes.
   - Audio is Web Audio synthesized.
   - HUD is HTML/CSS.

4. **No pause.**
   - The game is real-time.
   - Game over is the only non-playing state.

5. **Input queue.**
   - Inputs are enqueued with `state.time` and processed at simulation boundaries.
   - This makes tests deterministic.

6. **State order.**
   Each tick runs in this order:
   1. `progression.update`
   2. `market.update`
   3. `stalls.update`
   4. `aisles.update`
   5. `stock.update`
   6. `dockCart.update`
   7. `customers.update`
   8. `cats.update`
   9. `enemies.update`
   10. `defenses.update`
   11. `events.update`
   12. `bell.update`
   13. `winLoss.check`
   14. `ui.sync`

7. **All gameplay state is in global context.**
   - No hidden globals.
   - Modules read/write `state`.

8. **No added systems.**
   - No tech tree, player avatar, direct combat, stealth, farm, racing, story RPG, one-cat survival, or clean-path tower defense.

---

# 2. CONTRACTS

## 2.1 Module layout

```text
index.html
style.css
src/
  main.js                 # boot, canvas, loop, input listener, resize
  rng.js                  # seeded PRNG
  state.js                # createInitialState, records, reset
  input.js                # input queue, commands, pointer/key mapping
  loop.js                 # fixed step update/render
  market.js               # phases, win/loss, market open checks
  stalls.js               # stall state, fish units, repair/clean/open/close
  aisles.js               # aisle state, path, blocked, clean/noise/slip
  stock.js                # dock cart, haul, move stock, fish unit rules
  economy.js              # resources, costs, hiring, upkeep failures
  cats.js                 # cats, commands, obedience, naps, combat, injury
  enemies.js              # enemies, hazards, waves, occupation, interactions
  defenses.js             # placement, validity, durability, effects
  bell.js                 # fish-market bell, dawn bell
  customers.js            # spawn, target, patience, complaints, sales
  progression.js          # night scaling, strange raids, random problems
  ui.js                   # HUD sync, panels, state machine
  render.js               # market drawing
  audio.js                # synthesized audio
  debug.js                # debug API
```

## 2.2 Global context

Every gameplay rule and test must use these fields.

```js
state = {
  version: "0.1",
  seed: 1,
  rng: { next: fn, int: fn, float: fn, chance: fn },

  time: 0,
  dt: 1/60,
  frame: 0,
  phase: "TITLE" | "SETUP" | "OPEN" | "GAME_OVER",
  result: null | "WIN" | "LOSS",
  lossReason: null | string,

  market: {
    nextRaidTime: 60,
    raidActive: false,
    currentRaid: 0,
    salesDuringRaid: 0,
    lastSaleAt: -999,
    lastCustomerBuyingAt: -999,
    activeBuyingCustomers: 0,
    marketOpen: false,
    functionalStallCount: 0,
    nonFunctionalLossCount: 0
  },

  gate: {
    x: 480,
    y: 690,
    state: "OPEN" | "BLOCKED" | "OCCUPIED",
    occupiedBy: null
  },

  stalls: [
    {
      id: "A01",
      name: "Fresh Catch",
      type: "normal" | "saltedHerring" | "smokedEels",
      x: 120,
      y: 150,
      price: 4,
      maxStock: 12,
      stock: [
        {
          id: "fish_A01_0",
          type: "normal" | "salted" | "smoked",
          freshness: 100
        }
      ],
      counterHP: 100,
      maxCounter: 100,
      iceBoxId: null,
      closed: false,
      occupiedBy: null,
      repairDeadline: null,
      lastSaleAt: -999,
      baitLevel: 0,
      richLevel: 0,
      safeLevel: 0,
      state: "CLOSED" | "OPEN" | "SPOILED" | "OCCUPIED" | "RUINED" | "BLOCKED"
    }
  ],

  aisles: [
    {
      id: "A01",
      stallId: "A01",
      nodes: [
        { x: 120, y: 630, blocked: false },
        { x: 120, y: 540, blocked: false },
        { x: 120, y: 450, blocked: false },
        { x: 120, y: 360, blocked: false },
        { x: 120, y: 270, blocked: false },
        { x: 120, y: 210, blocked: false },
        { x: 120, y: 180, blocked: false }
      ],
      cleanliness: 100,
      noise: 0,
      slip: 0,
      blocked: false,
      protected: false,
      baitLevel: 0,
      richLevel: 0,
      safeLevel: 0,
      occupiedBy: null,
      state: "FRESH" | "SPOILED" | "SLIPPERY" | "NOISY" | "BLOCKED" | "OCCUPIED" | "PROTECTED" | "BAIT" | "RICH" | "SAFE" | "PROBLEMATIC"
    }
  ],

  customers: [
    {
      id: "cust_1",
      x: 480,
      y: 690,
      targetStall: "A01",
      path: [],
      patience: 100,
      maxPatience: 100,
      speed: 35,
      state: "ENTERING" | "CHOOSING" | "WALKING" | "BUYING" | "COMPLAINING" | "PANICKING" | "LEAVING",
      complaintCount: 0,
      lastComplaintAt: -999
    }
  ],

  cats: [
    {
      id: "cat_mackerel",
      name: "Mackerel Mouth",
      x: 60,
      y: 660,
      assignedZone: null,
      order: "IDLE" | "GUARD" | "CHASE" | "RETURN" | "REST" | "REPAIR" | "HAUL" | "MOVE_STOCK" | "ALARM" | "PATROL",
      target: null,
      condition: 100,
      energy: 100,
      obedience: 70,
      hunger: 0,
      fear: 0,
      asleep: true,
      distractedTimer: 0,
      attack: 9,
      speed: 55,
      traits: ["one_ear", "ignore_gulls", "hates_seagulls"],
      state: "ASLEEP" | "IDLE" | "MOVING" | "GUARDING" | "CHASING" | "FIGHTING" | "RESTING" | "REPAIRING" | "INJURED" | "HIDING" | "NAPPING" | "DISTRACTED"
    }
  ],

  enemies: [
    {
      id: "enemy_1",
      type: "gull" | "seagull" | "raccoon" | "rivalCat" | "dockworker",
      x: 0,
      y: 0,
      targetAisle: null,
      targetObject: null,
      hp: 12,
      maxHp: 12,
      speed: 70,
      attack: 2,
      fear: 0,
      carrying: [],
      state: "ENTERING" | "MOVING" | "INTERACTING" | "OCCUPYING" | "FIGHTING" | "FLEEING" | "LEAVING" | "CAUGHT",
      interactionTimer: 0,
      occupationTimer: 0
    }
  ],

  fishItems: [
    {
      id: "fish_item_1",
      type: "normal" | "salted" | "smoked",
      freshness: 90,
      x: 0,
      y: 0,
      flying: false,
      flightTimer: 0,
      flightPath: [],
      carriedBy: null
    }
  ],

  crates: [
    {
      id: "crate_1",
      type: "freshFish" | "ice" | "scraps",
      x: 960,
      y: 600,
      payload: { stock: 8, ice: 20, scraps: 10 },
      hauledBy: null,
      decayTimer: 60
    }
  ],

  defenses: [
    {
      id: "def_1",
      type: "netAwning" | "iceBox" | "barricade" | "hook" | "rope" | "trap",
      x: 0,
      y: 0,
      targetStall: null,
      durability: 80,
      maxDurability: 80,
      active: true,
      valid: true,
      state: "REAL" | "WEAK" | "BROKEN" | "DECORATIVE",
      cooldown: 0,
      armed: true,
      radius: 120,
      anchor: null
    }
  ],

  bell: {
    x: 480,
    y: 630,
    cooldown: 0,
    lastRingAt: -999
  },

  resources: {
    coins: 30,
    ice: 40,
    scraps: 20
  },

  events: {
    problemTimer: 60,
    flungFishTimer: 60,
    log: []
  },

  stats: {
    totalCoinsEarned: 0,
    totalFishSold: 0,
    totalFishSpoiled: 0,
    enemiesCaught: 0,
    enemiesDrivenOff: 0,
    stallsLost: 0,
    customersPanicked: 0
  },

  input: {
    queue: [],
    selectedCat: null,
    selectedStall: null,
    selectedAisle: null,
    selectedDefense: null,
    selectedEnemy: null,
    selectedItem: null
  },

  ui: {
    panelMode: "MARKET" | "CAT" | "STALL" | "DEFENSE" | "CUSTOMER",
    tooltip: null
  }
}
```

## 2.3 Module specifics

| Module | Required functions / contracts |
| --- | --- |
| `rng.js` | `createRng(seed)`, `next()`, `int(min,max)`, `float(min,max)`, `chance(p)` |
| `state.js` | `createInitialState(seed)`, `resetRun(seed)` |
| `input.js` | `queueCommand(cmd)`, `processInput(state)`, `select(type,id)`, `assignZone(catId,zoneId)`, `order(catId,order,target)`, `placeDefense(type,x,y)`, `ringBell()`, `openStall(stallId)`, `closeStall(stallId)`, `repairTarget(targetId)`, `cleanTarget(targetId)`, `feedCat(catId,mode)`, `wakeCat(catId)`, `haulCrate(catId,crateId,targetStallId)`, `moveStock(catId,srcId,targetId)`, `drawPatrol(catId,nodes)` |
| `loop.js` | `startLoop()`, `step(state)`, `render(state)` |
| `market.js` | `setPhase`, `startRaid`, `endRaid`, `countFunctionalStalls`, `countLossStalls`, `isMarketOpen`, `checkWinLoss`, `hasActiveSale`, `lastSaleWithin(seconds)` |
| `stalls.js` | `updateStall`, `canServe`, `isFunctional`, `isClosed`, `isRuined`, `isOccupied`, `sellFish`, `addFishUnit`, `removeFishUnit`, `dumpBadFish`, `openStall`, `closeStall`, `repairStall`, `cleanStall`, `setOccupied`, `clearOccupation` |
| `aisles.js` | `updateAisle`, `isPathClear`, `isAcceptable`, `isProtected`, `computeAisleState`, `setBlocked`, `addSlip`, `addNoise`, `setCleanliness`, `addBait`, `removeBait` |
| `customers.js` | `spawnCustomer`, `chooseTarget`, `updateCustomer`, `startSale`, `completeSale`, `addComplaint`, `panic`, `knockOver`, `exitCustomer` |
| `stock.js` | `updateFishDecay`, `spawnDockCrate`, `haulCrate`, `moveStock`, `retrieveFish`, `dropCarriedFish`, `addStockPayload`, `getSellableCount`, `getBadCount` |
| `economy.js` | `canAfford`, `spend`, `refundScrap`, `getCostMultiplier`, `hireCat`, `feedCat`, `wakeWithScrap`, `applyUpkeepFailure` |
| `cats.js` | `updateCat`, `assignZone`, `wake`, `feed`, `rest`, `repair`, `chase`, `guard`, `returnToPost`, `haul`, `moveStock`, `combat`, `takeDamage`, `injure`, `hide`, `autoNap`, `wakeByTrigger`, `obeyCheck`, `breakPost`, `healByRest` |
| `enemies.js` | `spawnWave`, `spawnEnemy`, `updateEnemy`, `chooseTarget`, `moveAlongPath`, `interact`, `takeDamage`, `fear`, `flee`, `catch`, `leaveWithLoot`, `occupy`, `clearOccupation`, `updateHazard`, `applyEnemyEffects` |
| `defenses.js` | `placeDefense`, `validatePlacement`, `updateDefense`, `damageDefense`, `breakDefense`, `repairDefense`, `resetTrap`, `applyDefenseEffect`, `isDecorative` |
| `bell.js` | `ringBell`, `updateBell`, `wakeCatsByBell`, `startleEnemies`, `scareCustomers`, `addBellNoise` |
| `progression.js` | `getWave`, `getIceMult`, `getDecayMult`, `getDamageMult`, `getCustomerNervousMult`, `getProblemInterval`, `applyStrangeModifiers`, `randomProblem` |
| `ui.js` | `showPanel`, `syncHUD`, `showState`, `showGameOver`, `showDebug` |
| `render.js` | `drawMarket`, `drawStalls`, `drawAisles`, `drawCustomers`, `drawCats`, `drawEnemies`, `drawDefenses`, `drawEvents` |
| `audio.js` | `initAudio`, `play(name)`, `musicStart`, `musicStop` |
| `debug.js` | see `8. DEBUG API` |

---

# 3. VISUAL SPEC

The game is a wet dockside fish market at night: low lamps, pale fish, blue-black wet stone, wooden stalls, ice crates, nets, barrels, and small animals moving through narrow aisles. The view is fixed and angled overhead, like a model market under lamplight. Everything readable: stalls, aisles, stock, customers, cats, enemies, defenses, and market states. The art is not medieval fantasy and not a clean path; it is a messy working place.

## Lighting and atmosphere

- Global darkness: `#0b1320` deep blue-black.
- Lamp pools: radial warm yellow `#ffd28a` at 35% alpha, radius 120–180px.
- Wet floor: subtle specular streaks, animated shimmer, cyan-blue reflections `#274a66`.
- Ice: pale blue-white `#bfe7ff`, low alpha, slight pulse.
- Spoiled smell: green-brown haze `#6d7a3f` at 10% alpha around bad fish.
- Slippery patches: translucent teal puddles with ripple rings.
- Noise: small gray jagged waves around noisy areas.
- Occupied stall: red-orange glow `#b4553a` on counter.
- Protected aisle: faint blue net/grid overlay.

## Space

- Market viewport: 960×720.
- Gate: bottom center `(480,690)`.
- Aisle x positions: `120, 240, 360, 480, 600, 720, 840`.
- Aisle entry y: `630`.
- Aisle nodes y: `540, 450, 360, 270, 210, 180`.
- Stall front y: `210`.
- Stall back y: `180`.
- Stall body y: `150`.
- Spawn points: docks left `(60,90)`, roof center `(480,90)`, alleys right `(900,90)`.
- Safe corners: `(60,660)`, `(900,660)`, `(480,660)`.
- Loading rail: `(960,600)`.

## Visual recipe table

| Element | Visual recipe | Rule implied |
| --- | --- | --- |
| Stall | Wooden counter, fish crates, lamp above, stall number, price tag | Open stalls show stock; closed show shutter; ruined show broken planks. |
| Fish unit | Small fish shape, color by freshness: ≥80 silver, 60–79 dull, <60 green-brown | Freshness visible. |
| Ice box | Wooden box with blue ice, melting shrink | Ice amount and melting visible. |
| Cat | Small feline silhouette, ear notch, tail motion, order icon above head | Cat state and obedience visible. |
| Sleeping cat | Curled silhouette, slow breathing, no order icon | Asleep. |
| Customer | Human coat with basket, patience meter as small head icon | Customer state visible. |
| Gull | Small white/gray bird, quick hop/fly arcs | Small, fast, target fish. |
| Seagull | Larger pale bird, heavier wings | Large, bold, knocks customers. |
| Raccoon | Gray masked body, scrabbling hands | Targets containers/barricades. |
| Rival cat | Dark cat with collar, hostile posture | Fights and steals. |
| Dockworker | Tall human shape, boots, crate | Hazard, not combat enemy. |
| Net awning | Green net over stall, sag when weak | Blocks gulls, durability visible. |
| Barricade | Fish barrel with lid, cracks when weak | Blocks path, can fall. |
| Hook/rope | Hook on wall, rope across aisle | Snags/triggers traps. |
| Trap | Small crate trap with trigger plate | Catches small pests, reset visible. |
| Bell | Hanging brass bell with rope | Cooldown and ring state visible. |
| Gate | Iron gate with lamps | Open/blocked/occupied visible. |
| Dock cart | Small cart dropping crate | Crate type visible. |
| Aisle state | Tint overlay: spoiled green, slippery teal, noisy gray, occupied red, protected blue | Market state readable. |

---

# 4. GAMEPLAY SPEC

The game is a real-time market defense sim. The player is the head cat keeper. The player never moves as a cat and never attacks directly. The player selects stalls, aisles, cats, defenses, crates, and market objects, then issues orders and spends resources. Cats, customers, enemies, hazards, and market decay run continuously. The goal is to keep a majority of stalls functional and keep at least one customer buying until dawn.

## 4.1 Run Structure and Night State — Tier 1

### Times

| Time | Phase | Events |
| --- | --- | --- |
| 0–60 | SETUP | Market waking. No customers. No raids. Player can place defenses, open/close stalls, assign sleeping cats, wake cats, repair. |
| 60 | OPEN | Market opens. Customers may spawn. Raid 1 begins. |
| 60 | Raid 1 | Starts. |
| 150 | Raid 2 | Starts after previous raid cleared or at 150 if cleared. |
| 240 | Raid 3 | Starts after previous cleared or at 240. |
| 330 | Raid 4 | Starts after previous cleared or at 330. |
| 420 | Raid 5 | Starts after previous cleared or at 420. |
| 510 | Raid 6 | Starts after previous cleared or at 510. |
| 720 | DAWN | Dawn bell rings. Game ends. |

### Market open condition

The market is open if all are true:

- `functionalStallCount >= 4`.
- At dawn or during a raid check, at least one customer is actively buying or `lastSaleAt >= time - 10`.

### Loss conditions

Immediate loss if:

- `nonFunctionalLossCount >= 4`, where nonFunctionalLoss stalls are `RUINED`, `CLOSED`, or `OCCUPIED`.
- At the end of any raid, `salesDuringRaid == 0`.

At dawn:

- If market open, result `WIN`.
- Else result `LOSS`.

### Stall definitions

| State | Rule |
| --- | --- |
| Open | Not blocked, not occupied, stock count > 0. |
| Functional | Can serve: not closed, not ruined, not occupied, has at least one fish unit freshness ≥ 60, counter HP ≥ 30, aisle acceptable. |
| Closed | Player closed it, or no sellable stock. |
| Ruined | Counter HP ≤ 0, or occupied and not repaired within 60s after occupation. |
| Occupied | Enemy controls stall. |
| Blocked | Aisle path blocked. |
| Protected | Cat assigned to guard zone or active defense covers area. |
| Bait | Open fish, empty counter, bad fish, tempting fish, strong smells. |
| Rich | High price / high-value stock. |
| Safe | Clean, fresh, calm. |
| Problematic | Spoiled, slippery, blocked, or noisy. |

### Aisle acceptable for customers

Aisle is acceptable if:

- `cleanliness >= 40`
- `noise <= 60`
- `slip <= 60`
- path clear

### Occupation rules

- Enemy occupies stall after reaching front and remaining 3s while stall is unsafe:
  - counter HP ≤ 50, or
  - all fish freshness < 60, or
  - ice box broken/opened badly.
- Occupation clears if:
  - enemy defeated/driven off,
  - bell frightens enemy,
  - player closes occupied stall.
- After clearing occupation:
  - stall counter HP −20.
  - `repairDeadline = time + 60`.
  - if not repaired and counter HP ≤ 30, stall becomes `RUINED`.
- Repair returns stall to weaker state:
  - max counter HP after repair = 70.

## 4.2 Market, Stalls, and Aisles — Tier 1

### Stall roster

| ID | Name | Tier 1 type | Price | Initial fish units | Max stock | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| A01 | Fresh Catch | normal | 4 | 10 | 12 | Easy bait. |
| A02 | Ice Mackerel | normal | 5 | 10 | 12 | Rich. |
| A03 | Herring Barrel | normal until Tier 2 | 6 | 8 | 12 | Becomes salted herring in Tier 2. |
| A04 | Smoked Eels | normal until Tier 2 | 10 | 4 | 6 | Becomes smoked eels in Tier 2. |
| A05 | Mixed Offcuts | normal | 3 | 12 | 12 | Cheap bait. |
| A06 | Dockside Ice | normal | 5 | 8 | 12 | Ice-adjacent visual. |
| A07 | Bargain Bin | normal | 4 | 10 | 12 | Low value. |

### Initial stall state

- All stalls begin `CLOSED` but with stock laid out.
- Player may open stalls during SETUP.
- Opening is free but begins upkeep and spoilage.

### Fish unit state

| Freshness | State | Effects |
| --- | --- | --- |
| 80–100 | fresh | Full sale price, no complaint. |
| 60–79 | low | Sale allowed, price ×0.6, complaint −15. |
| 0–59 | bad | Not sellable, lowers patience, attracts pests. |

### Decay

- Base fish decay: `0.25 freshness/s` per fish unit.
- Active ice box: decay ×0.1.
- Night decay multiplier: `1 + 0.25 * time/720`.

### Aisle state effects

| State | Trigger | Effect |
| --- | --- | --- |
| Fresh | clean ≥ 70, noise < 30, slip < 30 | Customers patience regen +1/s. |
| Spoiled | clean < 50 or bad fish ≥ 1 | Customer complaint −12, pest target weight +20. |
| Slippery | slip ≥ 30 | Cats 15% chance fall per node, 2s stun; everyone speed −25%. |
| Noisy | noise ≥ 30 | Cat obedience −10, customer patience −2/s. |
| Blocked | node blocked | Customers cannot reach; cats cannot pass; may trap cats. |
| Occupied | enemy controls stall | No customers; stall nonfunctional. |
| Protected | cat guard or defense active | Enemy damage to stall/defense ×0.5; target weight −50. |
| Bait | open stock, empty counter, bad fish, tempting fish | Enemy target weight +30 to +80. |
| Rich | price ≥ 6 | Coins higher, enemy target weight +10. |
| Safe | clean high, noise low | Customers stay longer. |
| Problematic | any bad state | Harder to defend, easier to lose. |

### Repair and clean

| Action | Cost | Time | Effect |
| --- | --- | --- | --- |
| Repair stall structure | 5 scraps × cost multiplier | 10s | Counter HP +40, max after repair 70. |
| Clean stall/aisle | 1 scrap × cost multiplier | 5s | Cleanliness +60, noise −30, slip −20. |
| Repair ice box | 3 scraps × cost multiplier | 6s | Durability +30. |
| Refill ice box | 3 coins + 5 ice × cost multiplier | 3s | Ice +50 up to 100. |

## 4.3 Customers — Tier 1

### Spawn

- Customers spawn only if:
  - phase `OPEN`,
  - gate state `OPEN`,
  - market has at least one functional stall,
  - current customers < 3.
- Spawn interval:
  - base 8s.
  - if any aisle `NOISY` or `SPOILED`, interval +4s.
- Maximum customers: 3.

### Target selection

Every 2s:

- Choose functional stall with highest score:

```text
score = price * freshness/100
      - aisleProblem * 5
      - distance * 0.2
```

- If no target, customer wanders and patience decays `2/s`.

### Customer state machine

| State | Behavior |
| --- | --- |
| ENTERING | Move from gate to chosen aisle entry. |
| CHOOSING | Select target. |
| WALKING | Move to stall front speed 35. |
| BUYING | Stand 1.5s at stall. |
| COMPLAINING | Play complaint, patience loss. |
| PANICKING | Speed 80, flee to gate, knock things over. |
| LEAVING | Move to gate and remove. |

### Complaints

| Cause | Patience loss |
| --- | --- |
| Smell, clean < 50 | −12 |
| Noise > 40 | −10 |
| Ruined/occupied visible | −15 |
| Failed sale | −20 |
| Bell within 300px | −15 |
| Enemy in aisle | panic |
| Flung trout nearby | −15 |
| Fighting noise in aisle | −10 |

Complaints scale with `customerNervousMult = 1 + 0.5 * time/720`.

### Panic and stampede

- If patience ≤ 0, customer panics.
- Panicking customers:
  - move to gate,
  - knock over objects:
    - aisle slip +25,
    - noise +20,
    - node blocked 8s.
- If ≥2 customers panic within 10s in same aisle:
  - stampede:
    - noise +50,
    - slip +20,
    - all customers in aisle panic.

### Sale

- Customer can complete sale only if stall `canServe`.
- On completion:
  - remove freshest fish unit.
  - coins += `floor(price * fish.freshness/100)`.
  - stock count reduced.
  - market `salesDuringRaid++`.
  - customer leaves.
- If customer panics before service completes, sale fails.

## 4.4 Stock and Fish Supply — Tier 1

### Initial stock

- Each stall begins with listed fish units.
- Crates behind stalls and laid-out stock are visual.

### Dock cart

| Time | Payload |
| --- | --- |
| 120 | 8 fresh fish units |
| 300 | 20 ice |
| 480 | 8 fresh fish units + 10 scraps |

- Crate appears at loading rail `(960,600)`.
- Crate remains 60s, then:
  - fish crate spoils into smell hazard,
  - ice crate creates small slippery patch,
  - scraps crate remains.

### Haul crate

Input: select cat → select crate → select target stall → `Haul Crate`.

- Cat moves to crate.
- Cat carries crate to target stall.
- Adds payload:
  - fresh fish: add fish units freshness 100.
  - ice: resources.ice += payload.
  - scraps: resources.scraps += payload.
- Cat is busy during haul.
- If distracted, order fails and crate remains.

### Move stock

Input: select cat → source stall → target stall → `Move Stock`.

- Moves one fish unit per 5s.
- Source stock reduced.
- Target stock added.
- Cat is busy.

### Retrieve fish

- If enemy carrying fish is caught/defeated, fish drops as fish item.
- Cat can retrieve by moving to item and hauling to assigned stall.
- Retrieval adds 1 fish unit freshness 90.

### Empty stall effects

- Stock count 0:
  - stall cannot trade.
  - state `CLOSED`.
  - baitLevel +30.
  - cats with hunger > 50 may investigate.

## 4.5 Resources, Economy, and Upkeep — Tier 1

### Starting resources

| Resource | Start |
| --- | --- |
| Coins | 30 |
| Ice | 40 |
| Scraps | 20 |

### Cost multiplier

```text
costMult = 1
if time >= 180: 1.2
if time >= 360: 1.4
if time >= 540: 1.6
```

Applies to repair, clean, ice refill, trap reset.

### Hiring

Allowed only during SETUP or between raids.

| Hire | Cost | Result |
| --- | --- | --- |
| Stray Market Cat | 12 coins | Spawns asleep at safe corner with base stray stats. |

### Feeding cats

| Feed mode | Cost | Effect |
| --- | --- | --- |
| Feed with fish | 1 fish unit from any open stall | Energy +20, hunger −30, obedience +15, condition +5, wakes cat. |
| Feed with scraps | 2 scraps | Energy +10, hunger −20, obedience +10, wakes cat. |
| Wake with scrap | 1 scrap | Wakes cat, obedience −5. |

### Upkeep failure

- No ice: fish decay continues.
- No scraps: repair/clean/reset fails.
- No food: cat hunger rises, obedience falls.
- No coin: cannot build/hire.
- If no resources for required action, action fails and state degrades.

### Closing stall

Input: select stall → `Close Stall`.

- Stops spoilage.
- Stops coin earning.
- Counts as `CLOSED` for loss.
- Can be reopened during SETUP or between raids only.

## 4.6 Cat Units, Commands, and Obedience — Tier 1

### Starting roster

Cats begin asleep in safe corners. Tier 1 includes base behavior only; named special traits activate in Tier 2.

| ID | Name | Base condition | Energy | Obedience | Speed | Attack | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cat_mackerel | Mackerel Mouth | 100 | 100 | 70 | 55 | 9 | One-eared silhouette. |
| cat_boots | Boots | 100 | 100 | 70 | 55 | 9 | Patrol-ready silhouette. |
| cat_whisker | Whisker | 100 | 100 | 70 | 55 | 9 | Detection-ready silhouette. |

### Hired stray

| Stat | Value |
| --- | --- |
| Condition | 80 |
| Energy | 80 |
| Obedience | 45 |
| Speed | 50 |
| Attack | 7 |
| Starts | Asleep at safe corner |

### Commands

| Input | Name | Rule |
| --- | --- | --- |
| Select cat, click stall/aisle | Assign Zone | Sets assigned zone and moves cat there if awake. Does not wake sleeping cat. |
| `1` | Guard | Stay in assigned zone, attack first enemy in zone. |
| `2` | Chase | Follow selected enemy until caught/driven off/leaves. |
| `3` | Return | Move to assigned post. |
| `4` | Rest | Cannot act; recover energy/condition. |
| `5` | Repair | Move to target object, spend scraps, repair. |
| `6` | Feed | Feed selected cat. |
| `7` | Wake | Wake with scrap or feed. |
| `8` | Haul | Haul crate/stock. |
| `9` | Move Stock | Move one fish unit. |
| `B` | Bell | Ring fish-market bell. |

### Obedience gate

An order succeeds only if:

- cat present,
- awake,
- not distracted,
- energy ≥ 30,
- fear < 50,
- obedience ≥ 60.

If fails:

- order ignored,
- obedience −5.

### Obedience modifiers

| Event | Obedience |
| --- | --- |
| Successful guard/chase | +5 |
| Successful fight | +5 |
| Fed | +15 |
| Completed repair | +5 |
| Ignored order | −5 |
| Auto-nap | −10 |
| Woken by scare | −15 |
| Hunger > 50 per 10s | −5 |
| Energy < 30 per 10s | −5 |
| Fear > 50 per 10s | −5 |

### Auto-nap

Cat naps if any:

- energy < 25,
- hunger > 70,
- assigned zone calm for 30s with no enemy/noise and energy < 80.

While napping:

- ignores orders,
- no fight/chase,
- zone open,
- obedience drops while napping if already scared.

Wake triggers:

- enemy enters zone,
- bell within 300px,
- another cat within 20px,
- feed.

If woken by scare:

- fear +20,
- obedience −15,
- nearby customers −15 patience,
- noise +30.

### Combat

- Guard attacks first enemy in assigned zone.
- Chase attacks followed target.
- Attack damage per second:

```text
catDamage = attack * (energy/100) * (condition/100)
```

- Enemy damage to cat:

```text
catCondition -= enemyAttack * dt
```

### Injury and loss

- If condition ≤ 0:
  - state `INJURED`,
  - runs to safe corner,
  - hides,
  - unavailable.
- If cat leaves market bounds:
  - removed as lost.
- Healing:
  - feed adds condition +5,
  - rest in clean aisle condition +5/s,
  - rest in dirty aisle condition +1/s.

## 4.7 Enemy Raids and Hazards — Tier 1

### Enemy roster

| Type | HP | Speed | Attack | Small? | Target | Interaction |
| --- | --- | --- | --- | --- | --- | --- |
| Gull | 12 | 70 | 2 | yes | exposed fish, signs, open lids | 1s: steal 1 fish, spoil −10 freshness |
| Seagull | 30 | 65 | 5 | no | stalls, bigger fish, customers | 2s: steal 2 fish, spoil −20, knock customer −20 patience |
| Raccoon | 45 | 40 | 8 | no | containers, barricades, ice boxes | 3s: open lid, pull crate, steal 3 fish |
| Rival Cat | 60 | 55 | 10 | no | high-value stalls, market cats | fight, steal 2 fish, can occupy |
| Dockworker | ∞ | 35 | 0 | no | crates, aisles | knock crate, spill, noise |

### Fear and outcomes

- Damage taken: `fear += damage/4`.
- Bell: `fear += 70`.
- If fear ≥ 60: state `FLEE`, move to exit.
- If HP ≤ 0:
  - small enemy: `CAUGHT`, removed, +2 scraps, drops carried fish.
  - large enemy: `DRIVEN_OFF`, leaves.
- If reaches target and not stopped:
  - target state changes,
  - enemy leaves with loot.

### Target selection

```text
targetScore = 10
            + sellableCount * 2
            + badFish * 5
            + baitLevel
            + richLevel
            - protected * 50
            - distance * 0.05
```

Spawn selection:

- Left spawn: A01, A02.
- Center spawn: A03, A04.
- Right spawn: A05, A06, A07.

### Wave tables

| Raid | Time | Enemies |
| --- | --- | --- |
| 1 | 60 | 3 gulls, 1 dockworker |
| 2 | 150 | 4 gulls, 1 raccoon |
| 3 | 240 | 2 gulls, 2 seagulls, 1 raccoon, 1 dockworker |
| 4 | 330 | 3 gulls, 2 raccoons, 1 rival cat, 1 dockworker |
| 5 | 420 | 2 gulls, 2 seagulls, 2 raccoons, 1 rival cat, 2 dockworkers |
| 6 | 510 | 3 gulls, 3 seagulls, 3 raccoons, 2 rival cats, 2 dockworkers |

### Raccoon interaction

- Ice box: durability −20, ice −20.
- Crate: destroyed, +5 scraps, creates debris.
- Stall: steals 3 fish if available.
- Can occupy stall if stall unsafe.

### Rival cat interaction

- If market cat in target zone:
  - fight for 5s.
  - if cat condition ≤ 20, cat flees.
- If no cat:
  - steal 2 fish.
  - can occupy if stall unsafe.

### Dockworker hazard

- Cannot be damaged by cats.
- Moves through random aisle.
- Every 8s:
  - knock crate: node blocked 10s, +5 scraps if crate breaks.
  - spill: aisle slip +30, noise +15.
- Cat chasing within 60px for 5s drives worker off.

## 4.8 Basic Market Defenses and Object Durability — Tier 1

### Defense roster

| Type | Cost | Durability | Effect | Weak/Broken |
| --- | --- | --- | --- | --- |
| Netted awning | 8 coins + 2 scraps | 80 | Blocks gulls in 120px radius; seagull dive 50% fail | Durability < 40 weak; 0 broken |
| Ice box | 5 coins + 8 ice | 60, ice 100 | Adjacent stall fish decay ×0.1; drains 0.2/s | Ice 0 or durability 0 broken |
| Fish-barrel barricade | 6 coins | 50 | Blocks node; enemy speed −60% adjacent | Durability < 20 weak; 0 broken |
| Hook | 4 coins | 40 | Adjacent enemy 35% snag 2s, durability −15 | Durability < 10 weak; 0 broken |
| Rope | 3 coins | 30 | Across aisle: enemies −50%, cats −25%, durability −5/s while active | Durability 0 broken |
| Little trap | 3 coins + 2 scraps | 20 | Catches small pests on node, must reset | Durability 0 broken |

### Placement validity

Objects are `REAL` only if correctly placed:

- Net awning: covers stall front or open stock and has two anchor points.
- Ice box: adjacent to stall within 60px.
- Barricade: on aisle node blocking path.
- Hook: adjacent to rope or trap.
- Rope: spans across aisle nodes.
- Trap: on walkable aisle node.

If invalid:

- state `DECORATIVE`,
- no active effect,
- still looks useful.

### Repair/reset

- Repair uses listed cost × costMult.
- Trap reset: 1 scrap × costMult, 2s.
- Broken objects leave as scrap if not repaired:
  - net: +2 scraps,
  - ice box: +1 scrap,
  - barricade: +3 scraps,
  - hook/rope/trap: +1 scrap.

### Defense effects

- Protected stall/aisle: enemy damage ×0.5.
- Barricade: enemy must attack before passing.
- Net awning: gulls cannot enter; seagulls may attack.
- Hook: snag triggers adjacent trap if armed.
- Rope: slows and takes durability while enemy/active.
- Trap: catches small pests only.

## 4.9 Bell and Emergency Response — Tier 1

### Fish-market bell

Input: `B` or bell button.

- Cooldown: 30s.
- Radius: 300px.
- Cats:
  - wake if asleep,
  - fear +10,
  - obedience −5,
  - if obedience < 70, break post and move toward bell.
- Customers:
  - patience −15,
  - complaint.
- Enemies:
  - fear +70,
  - occupied enemy flees if fear ≥ 60.
- Aisles:
  - noise +40.

### Dawn bell

- At t = 720.
- Cannot be rung, delayed, or controlled.
- Ends run and evaluates win/loss.

## 4.10 Advanced Cat Roles and Patrol — Tier 2

### General alarm cat

Input: assign cat to `ALARM` zone.

- Watches gate/spawns/market center.
- When enemy enters market:
  - yowls,
  - warning appears,
  - wakes cats within 250px,
  - wakes cats shift toward threat,
  - customers patience −10,
  - cooldown 10s.

### Patrol line

Input: select cat → `P` → draw line through aisle nodes → confirm.

- Cat walks line at speed +10%.
- Attacks any enemy within 50px of line.
- Covers multiple positions.
- If line intersects blocked node, patrol stops at block.

### Boots named trait — Tier 2

- Patrol speed +15%.
- After completing patrol loop with no fights:
  - sits and naps for 30s at route end.
- Player must feed, bell, or accept gap.

### Mackerel Mouth named trait — Tier 2

- Ignores gulls:
  - will not chase, attack, or be distracted by gulls.
- If seagull appears in assigned zone:
  - breaks orders and attacks seagull first.
- This may leave assigned stall open.

### Whisker named trait — Tier 2

- Detects bad fish in assigned zone.
- Yowls and marks bad fish for 20s.

## 4.11 Bait, Tempting Fish, and Cat-Cat Events — Tier 2

### Tempting fish

Input: place bait using 1 fish unit or 2 scraps.

- Creates bait item radius 160px.
- Enemy target weight +40.
- Cats with hunger > 50 or curiosity traits may break post.
- Cat may:
  - eat it: item removed, energy +10,
  - carry it: item follows cat as bait,
  - leave it: item remains.

### Cat-cat events

If two cats within 40px for 5s:

| Chance | Event | Effect |
| --- | --- | --- |
| 30% | Groom | Both distracted 8s, ignore orders. |
| 30% | Follow | One cat follows other, may leave zone. |
| 20% | Block | One blocks other’s path, orders unreliable. |
| 20% | None | No effect. |

Prevent by separating cats and feeding them.

## 4.12 Bad Fish Detection and Removal — Tier 2

### Detection

- Whisker detects fish freshness < 65 in assigned zone.
- Yowl:
  - marks bad fish,
  - gives player 20s to act.
- Other cats can detect only if ordered and present.

### Removal

Input: select bad fish marker → assign cat → `Dump Bad Fish`.

- Cost: 1 scrap × costMult.
- Time: 5s.
- Removes one bad fish unit.
- Cleanliness +10.
- If remaining stock has fresh units, average improves by removing bad.

### Effects

- Bad fish:
  - customer complaint −12,
  - pest target weight +20,
  - stall becomes smell source.

## 4.13 Flung Trout Events — Tier 2

### Trigger

- Gull steals fish,
- raccoon opens crate,
- customer panics,
- crate knocked over.

### Event

- Fish item flies 1.5s along arc.
- If within 50px of customer:
  - customer backs away,
  - patience −15.
- On landing:
  - aisle slip +30,
  - nearby cats distracted 3s.
- Cat can retrieve by leaving post and hauling to assigned stall.
- Retrieval adds 1 fish unit freshness 90.

## 4.14 Advanced Market Objects — Tier 2

### Net launcher

- Cost: 12 coins + 4 scraps.
- Durability 60.
- Fires at flying enemy within 200px.
- Stuns 3s.
- Cooldown 5s.
- Durability −10 per shot.
- Repair: 5 scraps × costMult, +20 durability.

### Eel barrel

- Cost: 5 coins.
- Durability 40.
- Makes aisle slip +40.
- Enemies on slippery tile:
  - 30% chance speed −50% for 2s,
  - slide 40px toward adjacent trap if trap exists.
- Repair: 2 scraps × costMult.

### Salted herring barrel

- Replaces A03 in Tier 2.
- Cost: 10 coins + 4 ice.
- Contains 8 salted fish units.
- Salted fish decay: 0.05/s.
- Closed:
  - cannot sell,
  - low smell.
- Open:
  - can sell at price 8,
  - baitLevel +40,
  - attracts gulls, raccoons, rival cats, hungry cats.
- Opening costs 1 scrap.
- If ruined:
  - clean −40,
  - smell hazard.

### Broken scale

- Placed at stall.
- Cost: 6 coins.
- Starts broken: `DECORATIVE`.
- Repair: 3 scraps × costMult.
- Accurate:
  - shows true fish freshness,
  - sale price reliable.
- False readings:
  - displayed freshness ±20,
  - coins may be reduced 10%.
- Broken:
  - prop only.

### Smoked eels

- Replaces A04 in Tier 2.
- Price 12.
- Initial stock 4.
- Freshness decay 0.15/s.
- High value.
- Guarding draws cats away from other stalls.
- If lost:
  - all customers patience −20 for 30s.

## 4.15 Progression and Strange Raids — Tier 2

### Night scaling

| System | Formula |
| --- | --- |
| Ice drain | base `0.2/s` × `(1 + 0.5 * time/720)` |
| Fish decay | base `0.25/s` × `(1 + 0.25 * time/720)` |
| Enemy damage | base × `(1 + 0.5 * time/720)` |
| Customer nervousness | complaint × `(1 + 0.5 * time/720)` |
| Customer max patience | `100 - 40 * time/720` |
| Repair cost multiplier | `1`, `1.2` at 180, `1.4` at 360, `1.6` at 540 |
| Random problem interval | `60 - 45 * time/720`, min 15s |

### Random problems

Pick random aisle:

| Problem | Effect |
| --- | --- |
| Spill | slip +30, noise +10 |
| Smell | clean −25, bait +20 |
| Noise | noise +35 |
| Crate knock | node blocked 10s, slip +15 |
| Flung trout | spawn flung fish event |

### Strange raid modifiers

| Market condition | Raid modifier |
| --- | --- |
| ≥2 spoiled stalls | +2 gulls distract |
| ≥1 occupied stall | +1 rival cat lures defenders |
| ≥2 slippery aisles | +1 dockworker creates spills |
| ≥2 customers panicked in last 60s | +2 gulls cause stampedes |
| ≥3 bad fish total | +1 raccoon opens lids |

## 4.16 Cascading Failure and Forced Sacrifice — Tier 2

### Cascading effects

| Cause | Effect |
| --- | --- |
| Spoiled stall | customers leave, less coins |
| Low coins | repair cost +20% |
| More broken stalls | enemies slip through |
| Hungry cats | obedience −20 |
| Cat abandons post | gap opens |
| Gap lets enemies take stock | fresh fish falls |
| Fresh fish falls | cats distractible |

### Forced sacrifice UI

During between raids:

- Player can close poor stalls.
- Player can let bait be stolen.
- Player can move cats from danger.
- Player can choose not to repair.

HUD shows:

- “Let fail” button,
- “Close aisle” button,
- “Sacrifice stall” confirmation.

## 4.17 Joke Behavior Rules — Tier 2

### No Gulls sign

- Cost: 2 coins.
- Durability 20.
- Radius 120px.
- Gull target weight −50.
- Gull can steal it:
  - sign removed,
  - area bait +30.

### Cat grooming during raid

- If cat idle with no threats 15s:
  - 20% chance groom for 10s.
- While grooming:
  - distracted,
  - ignores orders.

### Customers complaining while attacked

- Complaints are state changes:
  - smell,
  - noise,
  - ruined stalls,
  - failed service.
- Repeated complaints lower patience.
- Can become panic and damage market.

## 4.18 Market Legibility and Mastery — Tier 3

### Overlays

Toggle with `M`.

- Aisle risk heat:
  - green safe,
  - yellow risky,
  - red likely lost.
- Cat obedience bars.
- Enemy intent arrows.
- Bad fish markers.
- Decorative object warnings.
- Repair priority markers.

### After 10 minutes

At t ≥ 600:

- Show predicted enemy target if enough info.
- Show which aisles are bait.
- Show which cats likely obey next order.
- Show which defenses are decorative.

## Progression and Difficulty

- Early night teaches opening stalls, waking cats, placing basic defenses.
- Mid night forces ice and repair choices.
- Late night forces sacrifice, patrol/alarm play, and advanced object use.
- Difficulty rises through:
  - more enemies,
  - faster decay,
  - more nervous customers,
  - more random problems,
  - enemy tactics based on player neglect.

## Feel

- The player should feel like a keeper making bad decisions survive.
- Every failure should be visible: wet floor, bad smell, yowling cat, startled customer, broken net.
- Success should feel like a market staying alive, not just enemies dying.
- The bell is a panic tool, not a win button.
- Closing a stall is a real move, not a failure state.

---

# 5. CHARACTERS

## Cat silhouettes and states

Cats are small market cats, not heroic animals. Silhouettes should be readable by tail posture and ear shape.

### Base cat states

| State | Animation | Motion rule | Facing |
| --- | --- | --- | --- |
| Asleep | curled, slow breathing | no movement | toward safe corner |
| Idle | sit, occasional ear twitch | no movement | toward assigned zone |
| Moving | walk cycle, tail flick | move along path | movement direction |
| Guarding | crouch near post | scan left/right | toward aisle entry |
| Chasing | sprint, low body | follow target | target direction |
| Fighting | swipe, hiss | stop within 30px | target |
| Resting | lie down, slow blink | no movement | safe direction |
| Repairing | paw at object, scratch | stand beside object | object |
| Hauling | carry crate/fish, slow | move to target | target |
| Injured | limp, hide | move to safe corner | safe corner |
| Napping | auto-nap curled | no movement | current direction |
| Distracted | paw/bite fish, groom | stop 5–10s | bait |
| Alarm yowl | stand, head up, mouth arc | no movement | threat |
| Patrol | walk line | follow patrol path | path |

### Named cat traits

| Cat | Visual | Animations |
| --- | --- | --- |
| Mackerel Mouth | one-eared silhouette | ignores gulls: no target/gaze toward gulls; hates seagulls: lunges at seagulls first |
| Boots | boots/collar, long patrol stride | patrol walk, then nap at route end |
| Whisker | long whiskers, sniffing head | bad fish sniff, yowl marker |

## Enemy silhouettes and states

### Gull

| State | Animation |
| --- | --- |
| Enter | fly arc, wings flap |
| Hop | small bird walk |
| Squawk | open beak, head bob |
| Dive | fast downward arc |
| Steal | grab fish, fly off |
| Flee | scatter wings |
| Caught | trapped in crate |

Facing: movement direction.

### Seagull

| State | Animation |
| --- | --- |
| Enter | heavy wing flap |
| Circle | hover |
| Dive | straight down |
| Knock customer | wing spread |
| Carry fish | waddle/fly |
| Flee | large scatter |

Facing: target.

### Raccoon

| State | Animation |
| --- | --- |
| Scrabble | paw shuffle |
| Open lid | paw at lid |
| Pull crate | drag |
| Steal | hug fish |
| Occupy | sit over stall |
| Flee | run off |

Facing: target object.

### Rival Cat

| State | Animation |
| --- | --- |
| Stalk | low walk |
| Taunt | tail flick, hiss |
| Fight | swipe/grapple |
| Steal | carry fish |
| Occupy | sit at counter |
| Flee | run off |

Facing: target cat/stall.

### Dockworker

| State | Animation |
| --- | --- |
| Walk | heavy boots |
| Knock crate | shove |
| Spill | bucket dump |
| Driven off | hurry out |

Facing: movement.

## Customers

| State | Animation |
| --- | --- |
| Enter | walk, basket |
| Look | head turn, basket hesitation |
| Walk | normal walk |
| Buy | hand coins, receive fish |
| Complain | nose wrinkle, speech bubble |
| Panic | run, knock objects |
| Leave | exit gate |

Facing: target or exit.

## Market objects

- Fish units: small fish sprite, freshness color.
- Ice: shrink/melt animation.
- Nets: sag when weak.
- Traps: snap animation, reset animation.
- Bell: swing and ring.
- Signs: wobble, stolen animation.
- Barrels: open/close lid.
- Scale: needle animation.

---

# 6. AUDIO

All audio synthesized with Web Audio API. No external files.

| Name | Recipe | When |
| --- | --- | --- |
| `ui_click` | sine 600Hz, 40ms, quick decay | select |
| `ui_error` | square 150Hz, 120ms | invalid command |
| `build_place` | square 440Hz 50ms + noise 800Hz 30ms | place defense |
| `coin` | sine 1046Hz 80ms, second 1318Hz 50ms | customer buys |
| `bell_ring` | sine 880Hz + 1320Hz, 0.4s decay | fish-market bell |
| `dawn_bell` | sine 440Hz + 660Hz, 2s decay | dawn |
| `gull_squawk` | sawtooth 1200→900Hz, 150ms | gull spawn/steal |
| `seagull_squawk` | sawtooth 700→500Hz, 250ms | seagull |
| `raccoon_scrabble` | noise bandpass 800Hz, 200ms | raccoon action |
| `rival_hiss` | square 300Hz + noise, 200ms | rival cat |
| `dock_thud` | sine 120Hz, 200ms decay | dockworker knock |
| `wet_thud` | noise low-pass 300Hz, 200ms | slip/landing |
| `ice_crack` | white noise high-pass 4kHz, 50ms | ice break/melt |
| `cat_yowl` | sine 400→600Hz, 400ms | alarm/bad fish |
| `cat_meow` | sine 600Hz, 200ms | wake/interact |
| `cat_purr` | sine 120Hz tremolo 4Hz | fed/resting |
| `customer_complain` | triangle 300Hz, 100ms | complaint |
| `customer_panic` | noise 2kHz, 300ms | panic |
| `sale_fail` | square 220Hz 100ms | failed service |
| `trap_snap` | square 200Hz 50ms + noise | trap catches |
| `net_launch` | sawtooth 200→800Hz, 150ms | net launcher |
| `bad_fish_mark` | sine 250Hz, 200ms | Whisker marks |
| `repair_done` | triangle 520Hz + 660Hz, 150ms | repair |
| `game_win` | sine chord 440/554/659Hz, 1s | dawn win |
| `game_loss` | sine 220→110Hz, 1s | loss |
| `ambient_market` | low sine 90Hz drone + filtered noise water | night loop |
| `music_market` | slow minor arpeggio 110/165/220Hz, filtered | night music, low volume |

---

# 7. UX

## HTML and CSS only

- Canvas renders only the market.
- HUD, panels, buttons, tooltips, screens are HTML/CSS.
- No HTML text drawn inside canvas.

## Screen state machine

| State | Entry | Input allowed | Exit |
| --- | --- | --- | --- |
| TITLE | initial | click start | SETUP |
| SETUP | start run | build, open/close, assign, wake, repair | OPEN at t=60 |
| PLAYING | t>=60 | all in-game commands | GAME_OVER |
| GAME_OVER | win/loss/dawn | restart | TITLE |

## Input map

| Input | Action |
| --- | --- |
| Left click / tap | select object |
| Click stall + `O` | Open stall |
| Click stall + `C` | Close stall |
| Click stall + `R` | Order repair to selected cat |
| Click stall + `L` | Clean stall |
| Click cat + click stall/aisle | Assign zone |
| Click cat + `1` | Guard |
| Click cat + `2` | Chase |
| Click cat + `3` | Return |
| Click cat + `4` | Rest |
| Click cat + `5` | Repair |
| Click cat + `6` | Feed |
| Click cat + `7` | Wake with scrap/feed menu |
| Click cat + `8` | Haul |
| Click cat + `9` | Move stock |
| `B` | Ring bell |
| `P` | Draw patrol line |
| `D` | Place defense menu |
| `M` | Toggle mastery overlays |
| Right click | cancel selection |
| Esc | deselect |

## HUD table

| Element | Record field | Visible |
| --- | --- | --- |
| Coins | `resources.coins` | always after title |
| Fresh Fish | sum of sellable fish units | always after title |
| Ice | `resources.ice` | always after title |
| Scraps | `resources.scraps` | always after title |
| Night clock | `state.time`, `state.phase` | always after title |
| Raid timer | `market.nextRaidTime`, `market.raidActive` | always after title |
| Stall status | selected `stalls[]` | when stall selected |
| Aisle status | selected `aisles[]` | when aisle selected |
| Cat orders | selected `cats[]` | when cat selected |
| Cat order buttons | commands | when cat selected |
| Defense panel | selected `defenses[]` | when defense selected |
| Customer panel | selected `customers[]` | when customer selected |
| Bell cooldown | `bell.cooldown` | always after title |
| Market open bar | `market.functionalStallCount`, `market.marketOpen` | always after title |
| Loss warning | `market.nonFunctionalLossCount` | when ≥3 |
| Game over | `state.result`, `state.lossReason` | GAME_OVER |

---

# 8. DEBUG API

## System debug functions

| Function | Purpose |
| --- | --- |
| `debug.market()` | returns phase, market open, loss count, raid state |
| `debug.stalls()` | returns all stall records |
| `debug.aisles()` | returns all aisle states |
| `debug.customers()` | returns customer states |
| `debug.stock()` | returns fish units, crates, fish items |
| `debug.economy()` | returns resources and costs |
| `debug.cats()` | returns cat states |
| `debug.enemies()` | returns enemy/hazard states |
| `debug.defenses()` | returns defense states |
| `debug.bell()` | returns bell cooldown and last ring |
| `debug.progression()` | returns multipliers and event timers |
| `debug.winLoss()` | calls checks and returns result |

## Player input functions

| Function | Purpose |
| --- | --- |
| `debug.input.start()` | start run |
| `debug.input.select(type,id)` | select object |
| `debug.input.assignZone(catId,zoneId)` | assign cat |
| `debug.input.order(catId,order,target)` | issue command |
| `debug.input.placeDefense(type,x,y)` | place defense |
| `debug.input.openStall(stallId)` | open stall |
| `debug.input.closeStall(stallId)` | close stall |
| `debug.input.repairTarget(targetId)` | repair |
| `debug.input.cleanTarget(targetId)` | clean |
| `debug.input.feedCat(catId,mode)` | feed |
| `debug.input.wakeCat(catId)` | wake |
| `debug.input.haulCrate(catId,crateId,targetStallId)` | haul |
| `debug.input.moveStock(catId,srcId,targetId)` | move stock |
| `debug.input.ringBell()` | bell |
| `debug.input.drawPatrol(catId,nodes)` | patrol |
| `debug.input.hireCat()` | hire |
| `debug.input.forceRaid(i)` | spawn wave |
| `debug.input.setTime(t)` | set time for tests |
| `debug.input.spawnCustomer(stallId)` | spawn customer |
| `debug.input.spawnEnemy(type,aisleId)` | spawn enemy |
| `debug.input.setResource(name,value)` | set resource |

---

# 9. TESTS

## Tier 1 tests

| Test | Pass condition |
| --- | --- |
| Fixed loop determinism | Same seed and input queue produce same state hash at t=60. |
| Setup phase | No customers or enemies before t=60. |
| Market opens | At t=60, customers and raid 1 can spawn if market conditions allow. |
| Stall states | Opening/closing/ruining/occupating updates flags correctly. |
| Functional majority | Market open only with ≥4 functional stalls and sale/buying condition. |
| Loss by stalls | Game ends if 4 stalls are closed/ruined/occupied. |
| Loss by no sales | Raid with 0 sales ends in loss. |
| Customer sale | Customer at functional stall removes fish and adds coins. |
| Customer panic | Enemy in aisle causes customer panic and failed sale. |
| Fish spoilage | Without ice, fish freshness decays; with ice, reduced. |
| Ice box | Ice box drains and reduces decay. |
| Dock cart | Crate appears at set times and can be hauled. |
| Move stock | Moving stock reduces source and adds target. |
| Cat assignment | Assigning sleeping cat does not wake it. |
| Cat wake | Feed, scrap, or bell wakes cat. |
| Cat obedience | Order fails if asleep/hungry/low obedience. |
| Auto-nap | Calm cat naps after 30s; orders ignored. |
| Bell effects | Bell wakes cats, adds noise, frightens customers/enemies. |
| Enemy interactions | Gull steals fish, raccoon opens container, dockworker spills. |
| Occupation | Unsafe stall becomes occupied; clears by bell/cat/close. |
| Repair weaker | Repaired stall max counter 70. |
| Basic defenses | Net blocks gull, barricade blocks, trap catches gull, ice box works. |
| Decorative | Invalid defense has no active effect. |
| Dawn evaluation | At t=720 win/loss evaluates correctly. |

## Tier 2 tests

| Test | Pass condition |
| --- | --- |
| Alarm cat | Alarm yowl wakes nearby cats and warns. |
| Patrol line | Patrol cat attacks enemies along line. |
| Mackerel trait | Ignores gulls, attacks seagull first. |
| Boots trait | Naps after empty patrol loop. |
| Whisker trait | Detects bad fish before customer. |
| Tempting fish | Cats/enemies pulled by bait. |
| Cat-cat events | Proximity can cause groom/follow/block. |
| Bad fish removal | Dump removes bad fish and improves market. |
| Flung trout | Flung fish lowers customer patience and creates slip. |
| Net launcher | Stuns flying enemy. |
| Eel barrel | Creates slip and can slide enemy into trap. |
| Salted herring | Closed cannot sell, open sells and baits. |
| Broken scale | Broken decorative, repaired accurate. |
| Smoked eels | High value and loss penalty. |
| Strange raids | State-based extra enemies appear. |
| Cascading indicators | Low coins/low obedience effects appear. |
| No Gulls sign | Deters gulls until stolen. |
| Grooming | Idle cat may groom and ignore orders. |

## Tier 3 tests

| Test | Pass condition |
| --- | --- |
| Mastery overlay | Risk, obedience, intent overlays render. |
| Late hints | After 600s, predicted threat shown if enough info. |
| Readability | Bad fish, decorative objects, bait aisles visually marked. |
| Balance sanity | 8-minute playthrough can reach dawn with competent play. |

---

# 10. BUILD ORDER

1. Boot HTML/CSS canvas and fixed loop.
2. Seed RNG and global state.
3. Draw static market layout: gate, aisles, stalls, safe corners, loading rail.
4. Implement stall and fish unit records.
5. Implement phase timing: setup, open, dawn.
6. Implement opening/closing stalls.
7. Implement fish decay and spoilage.
8. Implement customers: spawn, target, walk, buy, leave.
9. Implement resources and HUD.
10. Implement ice boxes and basic upkeep.
11. Implement cat records, selection, assignment, wake, obey gate.
12. Implement guard/chase/return/rest/repair commands.
13. Implement basic enemy spawn and movement.
14. Implement enemy target selection and interactions.
15. Implement basic defenses and validity.
16. Implement bell.
17. Implement win/loss.
18. Implement full Tier 1 HUD, audio, visual states.
19. Add dock cart, haul, move stock.
20. Add full wave tables.
21. Add tests.
22. Tier 2: alarm/patrol/named traits.
23. Tier 2: bait/cat-cat/bad fish/flung trout.
24. Tier 2: advanced market objects.
25. Tier 2: progression/strange raids/cascading/joke rules.
26. Tier 3: mastery overlays and polish.

---

# 11. DEFINITION OF DONE

## Tier 1 Definition of Done

The game is a complete playable market defense run from title to dawn using only core mechanics.

- [ ] Runs in browser at 1280×720 design size.
- [ ] Fixed 60Hz simulation and seeded RNG.
- [ ] 7 stalls and 7 aisles exist.
- [ ] Market phases: setup, open, dawn.
- [ ] All stall states implemented and visible.
- [ ] Fish units spoil and can be sold.
- [ ] Customers spawn, choose stalls, buy, complain, panic, leave.
- [ ] Coins, ice, scraps, fresh fish HUD visible.
- [ ] Upkeep actions work: ice, clean, repair, close.
- [ ] Cats can be assigned, woken, fed, guarded, chased, rested, repaired, hauled.
- [ ] Cats obey or fail based on state.
- [ ] Auto-naps and wake triggers work.
- [ ] All five enemy/hazard types appear and behave.
- [ ] Basic defenses place, work, break, repair, and can be decorative.
- [ ] Bell works and dawn bell ends run.
- [ ] Win/loss conditions evaluate correctly.
- [ ] Tier 1 tests pass.

## Tier 2 Definition of Done

Tier 2 adds complete supporting mechanics without breaking Tier 1.

- [ ] Alarm cat and patrol line work.
- [ ] Named cat traits work.
- [ ] Tempting fish and cat-cat events work.
- [ ] Bad fish detection/removal works.
- [ ] Flung trout event works.
- [ ] Net launcher, eel barrel, salted herring barrel, broken scale, smoked eels work.
- [ ] Night progression and strange raids work.
- [ ] Cascading failure indicators and forced sacrifice UI work.
- [ ] No Gulls sign, grooming, complaint escalation work.
- [ ] Tier 2 tests pass.

## Tier 3 Definition of Done

Tier 3 improves legibility and mastery without changing core rules.

- [ ] Mastery overlays work.
- [ ] Late-night prediction hints work.
- [ ] Bad fish, bait, decorative objects are visually clear.
- [ ] Game remains finishable by competent play.
- [ ] Tier 3 tests pass.

---

# A. SANITY

| Check | Result |
| --- | --- |
| Does Tier 1 contain only core mechanics? | Yes. Tier 1 includes market survival, stalls/aisles, customers, stock, economy/upkeep, cats, enemies/hazards, basic defenses, bell. |
| Are supporting mechanics Tier 2? | Yes: alarm/patrol, bait/cat-cat, bad fish, flung trout, advanced objects, progression, cascading, joke rules. |
| Are extra/mastery items Tier 3? | Yes: legibility overlays and late hints. |
| Are all listed content parts present? | Yes: named cats, enemy types, customers, signs, sleeping cats, bells, basic/advanced defenses, market objects, dock cart, gate, bait, bad fish, decorative defenses. |
| Did I add extra systems? | No. Added only implementation records, layout coordinates, and tests needed for the specified systems. |
| Is the player a single cat with health/needs? | No. Player is keeper issuing orders. |
| Is it a generic medieval TD with clean path? | No. Dynamic market aisles, no clean path, no castles/wizards. |
| Are numbers concrete? | Yes: times, costs, decay, stats, speeds, thresholds, waves, resources. |
| Are inputs named? | Yes: selection, commands, bell, building, opening/closing, repair, patrol, debug inputs. |
| Is the view fixed overhead with panels? | Yes: 960×720 market, 320×720 HUD, fixed coordinates. |
| Are win/loss conditions exact? | Yes: majority functional + buying customer; loss by majority closed/ruined/occupied or no sales in full raid. |
| Are cats disobedient by design? | Yes: obedience gate, hunger, energy, fear, auto-naps, distractions, bait. |
| Are market failures cascading? | Yes: spoilage → customers → coins → repairs → enemies → cats. |
| Are basic defenses exact? | Yes: net awning, ice box, barricade, hook, rope, trap. |
| Are advanced objects exact? | Yes: net launcher, eel barrel, salted herring, broken scale, smoked eels. |
| Are bells correct? | Yes: fish-market bell is tool; dawn bell is automatic end signal. |
| Are tests tied to tiers? | Yes: Tier 1 validates core; Tier 2 validates supporting; Tier 3 validates mastery. |
| Is the design buildable by an agent? | Yes: module layout, global context, contracts, build order, definition of done. |