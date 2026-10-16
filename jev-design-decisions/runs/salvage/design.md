# 0. SCOPE

## 0.1 Asked

| Requirement | Where it lives |
| --- | --- |
| Top-down space salvage game where the player tows wrecks to a station and uses wreck parts to upgrade the ship | §4 Carry & Tow, §4 Economy, §4 Crafting & Recipes, §4 Equipment & Tools |
| 2D | §1.1, §3 |
| Top-down camera | §1.1, §3, §7 |
| Single player | §4 Player Ship & Movement |
| Real-time with pause | §1.2, §7 |
| Free movement | §4 Player Ship & Movement |
| Open world session shape | §4 Map/World |
| Failure: lose a life | §4 Player Health & Lives |
| Cozy tone | §0.2, §4, §5 |
| Many levels, a few hours | §0.3, §4 Map/World, §4 Progression |
| Win/lose: none defined by the user | §0.2, §7 |
| Mechanics list: carry and tow, steer, map/world, vehicles, landmarks, boosts, rewards, armour/defence, player health, unlocks, side quests, secrets, lore, recipes, dash, collectibles, fly, difficulty ramp, selling, hints, spawn points, conversations, consumables, currency, merchants, objectives, plot, crafting stations, quest givers, fast travel, score, shops, traps, prices, inventory limit, gathering spots, resource types, tools needed, equipment, skill tree, trading, pick up and drop, respawn, cutscenes | §4, §5, §6, §7 |
| Pixel art: low-resolution sprites with visible square pixels and a limited palette | §3 |
| Cold palette: blues, teals, greys | §3 |
| Pixel font: blocky bitmap letters | §7 |
| Music: chiptune | §6 |
| Sound effects: retro bleeps, synthesized chip sounds | §6 |
| Screens: title, pause, settings, game over | §7 |
| HUD: health, score, minimap, currency | §7 |
| Effects: particles, hit flash, trails | §3, §4 Feel |
| Accessibility: colour-blind safe palette, reduced motion, remappable keys, difficulty options | §1.2, §3, §7 |

## 0.2 Decisions

| Decision | Value | Why |
| --- | --- | --- |
| Game identity | Cozy salvage tug pilot in a cold asteroid belt | Matches tone and core salvage fantasy |
| Player identity | Wren, a junior salvage tug pilot | Gives a light character anchor without a heavy RPG |
| World | One continuous open world of 12 named sectors | Satisfies “open world” and “many levels” |
| Sector count | 12 | Enough for a few hours, still buildable |
| Sector size | 1024 x 1280 px | Gives room for landmarks, wrecks, traps, gathering spots |
| World size | 4096 x 3840 px | Four columns by three rows of sectors |
| Failure | 3 lives; losing a life respawns the player, losing all lives shows game over | Keeps consequence without harsh permadeath |
| No formal victory | No victory screen, no win state | User left `win/lose` empty |
| No enemy units | No hostile ships or combat enemies | Mechanics list includes traps but not enemies; cozy tone avoids combat |
| Hostile content | Environmental traps only | Keeps damage systems within listed mechanics |
| No save system | Each run starts fresh from title | Not requested; avoids unlisted persistence systems |
| Menus inside pause | Inventory, shop, crafting, skill tree, quest log, fast travel are tabs inside the pause screen | Keeps top-level screens exactly: title, pause, settings, game over |
| Conversations as radio overlays | NPCs speak via short on-canvas text lines, not a separate dialogue screen | Keeps screens exact while still satisfying conversations |
| HUD exactness | HUD has exactly health, score, minimap, currency | Follows listed HUD parts |
| Lives display | Life pips are sub-fields of the health HUD element | Keeps HUD element count exact while making lives visible |
| No camera shake | Damage uses hit flash only | Effects list is particles, hit flash, trails |
| Random source | Deterministic seeded RNG per sector | Tests and content layout must be reproducible |
| Fixed timestep | 1/60 second gameplay step | Stable physics and deterministic tests |
| Starting currency | 50 credits | Allows first tool purchase and early progression without free power |
| Starting lives | 3 | Clear, small consequence budget |
| Inventory model | 8 base slots, one item per slot, no stacking | Simple inventory limit and crafting checks |
| Tools purchasable at station | Cryo Cutter and Magnet Grapple can be bought at station | Prevents circular dependency with tool-gated resources |
| Score vs currency | Score is progression metric; currency is spending power | Both are required and distinct |
| Docking rule | Towed wreck converts to parts and adds score if inventory has space | Directly connects towing to upgrades and inventory limit |
| Selling rule | Parts sell in pause at stations/kiosks | Keeps shop UI inside pause while satisfying selling/merchants |
| Fast travel | Available in pause for visited landmarks | Keeps top-level screens exact and avoids in-map menus |
| Difficulty options | Casual, Cozy, Challenging | Required accessibility option |
| Reduced motion | Disables particles, trails, cutscene fades, minimap ping | Required accessibility option |
| Remappable keys | All gameplay keys are remappable | Required accessibility option |
| Colour-blind safety | Cold palette with luminance separation and shape-coded icons | Required accessibility option |
| Session length target | 2.5 to 3.5 hours for full content | Matches “a few hours” |
| Main progression | 12 main objectives unlock 12 sectors | Gives structure to open world |
| Side content | 12 side quests, 12 secrets, 12 lore entries, 48 collectibles | Satisfies side quests, secrets, lore, collectibles |
| Cutscenes | 4 cutscenes: intro, sector 4, sector 8, final | Satisfies cutscenes without adding a victory |

## 0.3 Tiers

| Tier | Name | Contents | Exit criterion |
| --- | --- | --- | --- |
| Tier 1 | Core Salvage Loop | Title, pause, settings, game over; 3 playable sectors; player ship; steer/fly/dash; hook/tow/dock; parts/inventory; traps; hull/shield/lives/respawn; station selling; basic crafting/equipment; score/currency/minimap/health HUD; base audio; accessibility options | Player can fly, tow a wreck, dock it, collect parts, sell parts, craft/equip an upgrade, die, respawn, and lose all lives to game over |
| Tier 2 | Full World & Economy | 12 sectors; all wrecks, traps, gathering spots, landmarks; main objectives; fast travel; full shops/merchants/prices/trading; all recipes, tools, equipment, consumables, boosts; difficulty ramp and options; full score/reward tables; full effects | Player can complete all 12 sectors through main objectives using the full economy and ship upgrades |
| Tier 3 | Narrative & Meta | 12 side quests; skill tree; 12 secrets; 48 collectibles; 12 lore entries; conversations; 4 cutscenes; plot text; full hints; quest log | Player can complete all side quests, collect all lore/secrets/collectibles, fill the skill tree, and trigger all cutscenes |

# 1. CONVENTIONS

## 1.1 Units, axes, frames

| Quantity | Unit | Value / convention |
| --- | --- | --- |
| Coordinate system | pixels, top-left origin | `x` increases right, `y` increases down |
| Camera | top-down, no rotation | Follows player |
| Canvas size | pixels | 960 x 540, scaled with integer pixel scaling |
| Game pixel | pixels | 1 game pixel = 1 rendered pixel |
| World width | pixels | 4096 |
| World height | pixels | 3840 |
| Sector width | pixels | 1024 |
| Sector height | pixels | 1280 |
| Sector grid | integers | 4 columns by 3 rows |
| Sector ID | integer | 1 to 12 |
| Time | seconds | Float seconds |
| Fixed timestep | seconds | 1 / 60 |
| Speed | pixels/second | Ship speeds are px/s |
| Acceleration | pixels/second² | Ship acceleration is px/s² |
| Rotation | radians/second | Turn rates are rad/s |
| Angle | radians | Heading 0 faces right, positive angle rotates clockwise on screen |
| Currency | integer credits | No fractional credits |
| Score | integer points | No fractional score |
| Lives | integer | 0 to 3 |
| Skill points | integer | 0 to 19 |
| Inventory slots | integer | 8, 12, or 16 depending on cargo module |
| Distance | pixels | Hook range, pickup radius, trap radius are px |

## 1.2 Important conventions

| Convention | Rule |
| --- | --- |
| Fixed-step loop | Gameplay updates at 1/60 s; rendering may run at display rate |
| RNG source | Use one seeded RNG per sector: `seed = 1337 * sectorId` |
| No gameplay `Math.random` | All gameplay randomness uses the seeded sector RNG |
| Debug randomness | Debug API may use non-seeded random only in debug functions |
| IDs | All world objects have stable string or integer IDs |
| No subpixel rendering | Sprites and camera snap to integer pixels |
| No save | No persistence between sessions |
| Screens | Top-level screen states are only `title`, `game`, `pause`, `settings`, `gameover` |
| Pause tabs | Pause has tabs but does not change the top-level screen state |
| Input polling | Input is polled each fixed step for movement; actions are event-driven |
| Audio | All audio is synthesized; no sampled audio |
| Reduced motion | When enabled, particles, trails, cutscene fades, and minimap ping are disabled |
| Colour-blind safety | Gameplay-relevant icons use shape and luminance, not hue alone |
| No enemies | No hostile units; damage comes from traps, boundary hazards, and wreck-break events |
| Menus | Shop, crafting, inventory, skill tree, quest log, and fast travel are pause tabs |
| Conversations | NPC dialogue is shown as short radio text overlays, not separate screens |

# 2. CONTRACTS

## 2.1 Module layout

| File | Responsibility |
| --- | --- |
| `index.html` | DOM shells for canvas and the four top-level screens |
| `styles.css` | Pixel-font styling, HUD layout, screen layout, reduced-motion CSS |
| `main.js` | Boot, fixed-step loop, screen state transitions |
| `state.js` | Global context factory, reset, events, score/currency/lives |
| `input.js` | Key binding, remapping, action dispatch |
| `ship.js` | Ship physics, health, shield, dash, lives, respawn |
| `tow.js` | Hook, towing, docking, wreck breaking, pick up/drop |
| `world.js` | Sectors, landmarks, traps, gathering spots, collectibles, secrets, fast travel |
| `inventory.js` | Inventory slots, item add/remove, selected slot, ground items |
| `equipment.js` | Equipment slots, module stats, tools, equipment application |
| `economy.js` | Currency, prices, selling, buying, trading, merchant rules |
| `crafting.js` | Recipes, crafting stations, craft checks |
| `quests.js` | Main objectives, side quests, quest givers, conversations, cutscenes, lore |
| `hud.js` | HUD rendering: health, score, minimap, currency |
| `audio.js` | Synthesized SFX and chiptune music |
| `settings.js` | Accessibility settings, difficulty options, key remap |
| `debug.js` | Debug API and input test functions |

## 2.2 Global context

| Field | Type | Meaning |
| --- | --- | --- |
| `screen` | string | `title`, `game`, `pause`, `settings`, `gameover` |
| `pauseTab` | string/null | `resume`, `inventory`, `shop`, `crafting`, `skill`, `quests`, `fasttravel`, `settings` |
| `time` | number | Seconds since game start |
| `lives` | number | Remaining lives |
| `score` | number | Current score |
| `currency` | number | Current credits |
| `skillPoints` | number | Current skill points |
| `difficulty` | object | Active difficulty mode and multipliers |
| `settings` | object | Accessibility and control settings |
| `ship` | object | Player ship state and equipment |
| `hook` | object | Tow hook state |
| `towed` | object/null | Currently towed wreck state |
| `inventory` | array | Inventory slots |
| `selectedSlot` | number | Selected inventory slot index |
| `groundItems` | array | Items dropped in the current sector |
| `world` | object | World, sector, landmarks, traps, resources, collectibles |
| `quests` | object | Quest state and active objectives |
| `boosts` | array | Active temporary boosts |
| `toasts` | array | Transient hint/toast messages |
| `cutscene` | object | Active cutscene state |
| `gameOver` | object | Game over reason and summary |
| `rng` | function | Seeded RNG for current sector |

`ship` fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `x`, `y` | number | Ship position |
| `heading` | number | Ship facing in radians |
| `vx`, `vy` | number | Velocity |
| `throttle` | number | -1, 0, or 1 |
| `turn` | number | -1, 0, or 1 |
| `hp` | number | Current hull health |
| `maxHp` | number | Maximum hull health |
| `shield` | number | Current shield |
| `maxShield` | number | Maximum shield |
| `lastDamageTime` | number | Time of last damage |
| `dashTimer` | number | Remaining dash time |
| `dashCooldown` | number | Remaining dash cooldown |
| `invulnTimer` | number | Remaining invulnerability |
| `alive` | boolean | Whether the ship is alive |
| `engine` | string | Engine module ID |
| `shieldModule` | string | Shield module ID |
| `hookModule` | string | Hook module ID |
| `cargoModule` | string | Cargo module ID |
| `toolA` | string | Tool slot A |
| `toolB` | string | Tool slot B |
| `selectedSlot` | number | Selected inventory slot |

`world` fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `sectorId` | number | Current sector |
| `unlockedSectors` | array | Unlocked sector IDs |
| `visitedLandmarks` | array | Visited landmark IDs |
| `landmarks` | array | Landmark records |
| `traps` | array | Trap records in current sector |
| `wrecks` | array | Wreck records in current sector |
| `gathering` | array | Gathering spot records |
| `collectibles` | array | Collectible records |
| `secrets` | array | Secret cache records |
| `minimap` | object | Render data for minimap |

## 2.3 Module specifics

| Module | Required exported functions |
| --- | --- |
| `state.js` | `createGameState()`, `resetGame()`, `setScreen(name, tab)`, `addScore(n)`, `addCurrency(n)`, `addSkillPoints(n)`, `addToast(text)`, `unlockSector(id)`, `markLandmarkVisited(id)`, `getSectorById(id)` |
| `input.js` | `init()`, `setKeys(keyMap)`, `getThrottle()`, `getTurn()`, `dash()`, `hook()`, `interact()`, `drop()`, `selectSlot(i)`, `pause()`, `startGame()`, `settings()`, `confirm()`, `cancel()` |
| `ship.js` | `update(dt)`, `applyDamage(raw, source)`, `heal(amount)`, `chargeShield(amount)`, `loseLife()`, `respawn()`, `applyDash()`, `getStats()`, `hasTool(id)`, `setModule(slot, moduleId)`, `getModule(slot)` |
| `tow.js` | `update(dt)`, `toggleHook()`, `attachNearestWreck()`, `attachWreck(id)`, `detach()`, `dockTowed()`, `breakWreck(id)`, `pickupNearest()`, `dropSelected()`, `canDock()` |
| `world.js` | `loadSector(id)`, `update(dt)`, `getSectorAt(x, y)`, `fastTravel(landmarkId)`, `canFastTravel(id)`, `spawnSectorContent(id)`, `triggerTrap(trapId, ship)`, `updateGathering(dt)`, `openSecret(id)` |
| `inventory.js` | `getSlots()`, `getItem(slot)`, `addItem(itemId)`, `removeItem(itemId, count)`, `hasItems(itemId, count)`, `findEmptySlot()`, `selectSlot(i)`, `getPartCounts()`, `clearParts()`, `addGroundItem(itemId, x, y)`, `getNearestGroundItem()` |
| `equipment.js` | `getStats()`, `equip(slot, moduleId)`, `unequip(slot)`, `hasTool(moduleId)`, `canCraft(recipeId)`, `craft(recipeId)` |
| `economy.js` | `sellParts(merchantId)`, `buyItem(merchantId, itemId)`, `tradeModule(merchantId, slot)`, `exchangeResources(merchantId, fromId, toId)`, `getSellPrice(itemId, merchantId)`, `getBuyPrice(merchantId, itemId)`, `applyPriceMods()` |
| `crafting.js` | `getRecipe(id)`, `canCraft(id)`, `craft(id)`, `getAvailableRecipes(landmarkId)` |
| `quests.js` | `update()`, `startQuest(id)`, `completeObjective(id)`, `completeQuest(id)`, `getActiveQuests()`, `playConversation(npcId)`, `playCutscene(id)`, `unlockLore(id)`, `getMainObjectiveForSector(sectorId)` |
| `hud.js` | `render()`, `renderHealth()`, `renderScore()`, `renderCurrency()`, `renderMinimap()` |
| `audio.js` | `play(name)`, `startMusic()`, `stopMusic()`, `init()` |
| `settings.js` | `get()`, `set(field, value)`, `remapKey(action, key)`, `applyDifficulty(mode)` |
| `debug.js` | All debug functions listed in §8 |

# 3. VISUAL SPEC

The game looks like a cold, low-pixel salvage chart: flat top-down space in deep blue-grey, with small bright cyan sprites for the player, wrecks, and parts. The ship is a compact teal tug with a pale nose and grey wings. Wrecks are larger blocky hulks in grey-blue with one or two cyan light pixels. Traps are readable by shape: ice spikes are pale jagged triangles, debris shards are angular grey chunks, magnetic anomalies are concentric grey rings, fuel leaks are soft teal smears, and drone fragments are small grey boxes with a blinking white pixel. Landmarks use bold silhouettes: the station is a large cross-shaped dock, beacons are thin cyan spires, kiosks are small grey squares with a teal awning, and cold current nodes are pale ring shapes. Everything is drawn on a 16-pixel logical grid with visible square pixels.

Lighting and atmosphere: there is no dynamic lighting system. Atmosphere is made by a dark background, a faint grid, sparse star pixels, and a slow drift of background snow-like specks. Important objects use brighter pixels. Damage uses a 1-frame white hit flash on the damaged sprite. No screen shake is used.

Space: the world is a 4096 x 3840 px top-down plane divided into 12 rectangular sectors. Sector borders are thin dark lines when unlocked and thick nebula walls when locked. The station is in sector 1. Other landmarks are placed at deterministic seeded positions within their sectors.

Palette:

| Name | Hex | Role |
| --- | --- | --- |
| Void | `#0A1218` | Deep background |
| Deep | `#101E2A` | Sector background variation |
| Slate | `#1E3544` | Walls, borders, dark UI |
| Steel | `#2C4C5C` | Ship hulls, kiosk bodies |
| Teal | `#3D7A82` | Wreck bodies, trap rings |
| Cyan | `#6FC3C9` | Player accent, beacons, highlights |
| Ice | `#B7EAEA` | Bright parts, ice, fast travel |
| Frost | `#E8F7F8` | Damage flash, important icons |
| Char | `#2B2F35` | Shadow pixels, trap outlines |
| Grey | `#5A6570` | Wreck grey, debris |
| Mist | `#9AA8B5` | Background stars, minor UI |
| Pale | `#DDE7EC` | Text, HUD, pale landmarks |

Recipe table:

| Element | Pixels | Palette use | Animation / rule |
| --- | --- | --- | --- |
| Player ship | 16 x 16 | Steel, Cyan, Frost | 8 facings; thrust animation when `throttle != 0`; dash stretch 3 frames |
| Towed wreck | 32 x 16 | Steel, Grey, Cyan | 4 intact frames; cable is 1 px cyan line from ship to wreck |
| Scutter wreck | 16 x 16 | Steel, Grey | Small variant of wreck |
| Hauler wreck | 32 x 16 | Steel, Grey | Medium wreck |
| Cryo wreck | 32 x 16 | Teal, Cyan | Cyan tank pixels |
| Probe wreck | 24 x 16 | Grey, Cyan | Antenna pixel |
| Relay wreck | 40 x 20 | Steel, Cyan, Frost | Large wreck with two lights |
| Ice spike | 16 x 16 | Frost, Ice, Char | Static jagged triangle |
| Debris shard | 12 x 12 | Grey, Char | Static angular chunk |
| Magnetic anomaly | 32 x 32 | Grey, Teal | 3 concentric rings, 2 fps pulse |
| Fuel leak | 24 x 24 | Teal, Cyan | 4-frame smear pulse |
| Drone fragment | 16 x 16 | Grey, Frost | Blinking 1 px warning before pulse |
| Station | 64 x 64 | Steel, Cyan, Frost | Dock cross; cyan dock lights |
| Beacon | 16 x 32 | Cyan, Ice | Thin spire; fast travel if unlocked |
| Kiosk | 32 x 32 | Steel, Teal | Small square with teal top |
| Cold current node | 32 x 32 | Ice, Frost | Ring shape |
| Part icon | 8 x 8 | Frost, Cyan, Ice | One icon per resource type |
| Pickup particle | 2 x 2 | Frost, Cyan | 6 particles for 0.3 s |
| Damage particle | 2 x 2 | Frost, Char | 8 particles for 0.3 s |
| Dash trail | 8 x 8 | Cyan, Ice | 3 ghost frames for 0.3 s |
| Cutscene panel | 320 x 180 | Full palette | Letterbox; 3-panel pixel illustration |

# 4. GAMEPLAY SPEC

Wren pilots a small salvage tug through a cold open-world belt of 12 sectors. The core loop is: fly to a wreck, hook it, tow it back to a station or dock, convert it into salvage parts, sell or craft the parts, and install better ship equipment. Hazards are environmental traps, not enemies. Progression is driven by main objectives that unlock sectors, side quests that teach the player optional content, and a skill tree that rewards repeated play. The ship can be damaged by traps, can lose a life if hull reaches zero, and respawns at the last safe landmark. All economic and crafting actions happen in the pause screen, while real-time play handles movement, towing, picking up, and avoiding traps.

## Records with rosters

| Record | Count | Key fields |
| --- | ---: | --- |
| Player ship | 1 | `x`, `y`, `heading`, `hp`, `shield`, `lives`, equipment |
| Wreck | 96 | `id`, `type`, `x`, `y`, `integrity`, `parts`, `spawnSector` |
| Trap | 168 | `id`, `type`, `x`, `y`, `sector`, `cooldown` |
| Landmark | 20 | `id`, `type`, `sector`, `x`, `y`, `functions` |
| Gathering spot | 153 | `id`, `type`, `sector`, `x`, `y`, `cooldown` |
| Collectible | 48 | `id`, `type`, `sector`, `x`, `y`, `collected` |
| Secret | 12 | `id`, `sector`, `x`, `y`, `condition`, `reward`, `opened` |
| Main objective | 12 | `id`, `sector`, `requirement`, `reward`, `unlock` |
| Side quest | 12 | `id`, `giver`, `sector`, `objective`, `reward` |
| NPC / quest giver | 5 | `id`, `name`, `location`, `lines` |
| Recipe | 14 | `id`, `output`, `resources`, `currency` |
| Module | 15 | `id`, `slot`, `stats`, `cost` |
| Consumable | 5 | `id`, `effect`, `cost` |
| Resource type | 5 | `id`, `name`, `sellPrice` |
| Lore entry | 12 | `id`, `sector`, `text` |
| Cutscene | 4 | `id`, `trigger`, `panels` |
| Conversation set | 15 | `id`, `npc`, `state`, `line` |

## Player Ship & Movement — Tier 1

| Rule | Value |
| --- | --- |
| Starting position | Station dock in sector 1 |
| Starting heading | 0 radians |
| Starting hull | 100 |
| Starting shield | 50 |
| Starting lives | 3 |
| Turning speed | 4.2 rad/s |
| Turning speed while towing | 3.1 rad/s |
| Base max speed | 240 px/s from stock engine |
| Reverse max speed | 50% of max speed |
| Base acceleration | 900 px/s² |
| Base drag | 3.0 per second |
| Dash speed | 520 px/s |
| Dash duration | 0.18 s |
| Dash cooldown | 1.1 s from stock engine |
| Dash while towing | dash speed x 0.75 |
| Movement | Free 2D movement; heading is rotated by turn input, velocity applies throttle along heading |
| Input priority | Dash cancels current thrust for dash duration |
| Bounds | Ship clamps to world bounds; locked sector walls block movement |

Ship stats are calculated from equipment:

| Module slot | Base effect |
| --- | --- |
| Engine | max speed, acceleration, dash cooldown |
| Shield | max shield, shield regen, hull bonus |
| Hook | hook range, attach time, tow speed bonus |
| Cargo | inventory limit |
| Tool A | tool capability |
| Tool B | tool capability |

## Carry & Tow — Tier 1

| Rule | Value |
| --- | --- |
| Hook range base | 180 px |
| Hook attach time base | 0.3 s |
| Hook input | `F` toggles hook |
| Attach rule | If a wreck is within hook range and no line-of-sight blocker exists, begin attach timer |
| Attach complete | Wreck becomes `towed` |
| Towed distance | 96 px behind ship heading |
| Towed speed base | 160 px/s |
| Towed acceleration while towing | 700 px/s² |
| Towed drag while towing | 3.4 per second |
| Towed turn rate while towing | 3.1 rad/s |
| Towed wreck integrity | 100 |
| Towed damage rule | While towing, damage taken by the player also deals 50% rounded up to wreck integrity |
| Wreck break rule | If integrity reaches 0, wreck breaks, drops its parts, hook detaches, wreck respawn timer starts |
| Wreck respawn time | 45 s |
| Dock rule | Docking a wreck requires enough empty inventory slots for all parts in the wreck |
| Dock reward | Adds wreck parts to inventory and adds wreck score |
| Dock failure | If inventory is full, docking does nothing and shows a hint |
| Detach | `F` detaches a towed wreck; wreck remains in world at current towed position |

Pick up and drop:

| Rule | Value |
| --- | --- |
| Pickup radius | 48 px |
| Pickup input | `E` when nearest interactable is a ground item |
| Pickup rule | Adds one item to first empty inventory slot |
| Drop input | `Q` drops selected slot |
| Drop rule | Creates a ground item at ship position |
| Ground item limit per sector | 24 |
| Ground item despawn | 300 s |
| Inventory full | Pickup or drop fails if no slot / limit exceeded |

Inventory limit:

| Rule | Value |
| --- | --- |
| Base inventory | 8 slots |
| Expanded Hold | 12 slots |
| Salvage Bay | 16 slots |
| Slot contents | One item per slot; no stacking |
| Selected slot | `1` to `8` selects first 8 slots; if cargo is larger, keys `9` and `0` select slots 9 and 10 if remapped; otherwise pause inventory selects higher slots |

## Map/World — Tier 1 for 3 sectors, Tier 2 for 12 sectors

| Rule | Value |
| --- | --- |
| World size | 4096 x 3840 px |
| Sectors | 12 |
| Sector grid | 4 columns by 3 rows |
| Sector size | 1024 x 1280 px |
| Initial unlocked sector | 1 |
| Sector unlock | Main objective completion unlocks next sector |
| Sector borders | Locked borders are impassable nebula walls; unlocked borders are passable grid lines |
| Landmarks per sector | Station, beacons, kiosks, and nodes as listed in landmark table |
| Spawn points | Station, visited Relic Beacons, visited Kiosks, visited Cold Current Nodes |
| Last safe spawn | Last visited spawn point |
| Fast travel | Pause tab; can travel to any visited landmark |
| Fast travel cooldown | 3 s |
| Fast travel duration | 1.0 s, 0.2 s with reduced motion |
| Fast travel restriction | Cannot fast travel while towing |
| Fast travel reward | None |

Sector names:

| Sector | Name |
| ---: | --- |
| 1 | Cold Dock |
| 2 | Frost Shelf |
| 3 | Drift Reach |
| 4 | Blue Hollow |
| 5 | Static Veil |
| 6 | Grey Trench |
| 7 | Polar Gate |
| 8 | Quiet Narrows |
| 9 | Dim Current |
| 10 | Ash Ridge |
| 11 | Pale Expanse |
| 12 | The Cold Current |

## Vehicles — Tier 1 for player, Tier 2 for full wreck roster

| Vehicle | Role |
| --- | --- |
| Player salvage tug | Only player-controlled vehicle |
| Scutter wreck | Small towable wreck |
| Hauler wreck | Medium towable wreck |
| Cryo Tank wreck | Tool-gated towable wreck |
| Probe wreck | Tool-gated towable wreck |
| Relay wreck | Large high-value towable wreck |

Wreck roster per sector:

| Sector | Scutter | Hauler | Cryo Tank | Probe | Relay | Total |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 4 | 2 | 0 | 0 | 2 | 8 |
| 2 | 3 | 3 | 1 | 0 | 1 | 8 |
| 3 | 3 | 2 | 1 | 1 | 1 | 8 |
| 4 | 2 | 3 | 1 | 1 | 1 | 8 |
| 5 | 2 | 3 | 1 | 1 | 1 | 8 |
| 6 | 2 | 3 | 1 | 1 | 1 | 8 |
| 7 | 1 | 3 | 1 | 1 | 2 | 8 |
| 8 | 1 | 3 | 1 | 1 | 2 | 8 |
| 9 | 1 | 3 | 1 | 1 | 2 | 8 |
| 10 | 1 | 2 | 1 | 2 | 2 | 8 |
| 11 | 1 | 2 | 1 | 2 | 2 | 8 |
| 12 | 0 | 2 | 1 | 2 | 3 | 8 |

Wreck parts:

| Wreck | Parts |
| --- | --- |
| Scutter | 1 Plating |
| Hauler | 2 Plating, 1 Coil |
| Cryo Tank | 2 Cryo |
| Probe | 1 Data, 1 Shard |
| Relay | 1 Plating, 1 Coil, 1 Shard, 1 Data |

Wreck score:

| Wreck | Score |
| --- | ---: |
| Scutter | 100 |
| Hauler | 180 |
| Cryo Tank | 250 |
| Probe | 250 |
| Relay | 400 |

Wreck score is multiplied by sector price multiplier and rounded down.

## Landmarks — Tier 1 for station and 2 landmarks, Tier 2 for all

| Landmark type | Count | Locations | Functions |
| --- | ---: | --- | --- |
| Station Coldlight | 1 | Sector 1 | Dock, shop, crafting, fast travel hub, spawn, quest giver |
| Relic Beacon | 11 | Sectors 2 to 12 | Fast travel, spawn, some repair objectives |
| Drifter Kiosk | 4 | Sectors 4, 7, 10, 12 | Shop, crafting, fast travel, spawn, quest giver |
| Cold Current Node | 4 | Sectors 3, 6, 9, 12 | Lore, secret, fast travel, final dock |

Total landmarks: 20.

## Traps — Tier 1

| Trap | Count rule | Base damage | Effect |
| --- | ---: | ---: | --- |
| Ice Spike | 40% of sector trap count | 12 | Contact damage every 0.5 s while overlapping radius 16 px |
| Debris Shard | 20% | 20 | One-hit knockback 120 px, cooldown 1.0 s, radius 14 px |
| Magnetic Anomaly | 20% | 6/s | Radius 120 px, pulls ship 80 px/s² toward center, continuous damage while inside |
| Fuel Leak | 10% | 8/s | Radius 48 px, burns for 2 s after leaving |
| Rogue Drone Fragment | 10%, minimum 1 in sectors 4+ | 18 | Pulse radius 90 px every 3.0 s, 0.8 s warning blink |

Trap placement uses the sector seeded RNG. Damage is multiplied by sector damage multiplier, difficulty damage multiplier, and active damage-reduction boosts.

## Player Health & Lives — Tier 1

| Rule | Value |
| --- | --- |
| Hull health | Base 100 |
| Shield | Base 50 |
| Shield regen | 6/s after 2.5 s without damage |
| Damage order | Shield absorbs first, then hull |
| Hull 0 | Lose 1 life |
| Lives | Start 3 |
| Life lost score penalty | -250 |
| Respawn location | Last safe spawn |
| Respawn hull | 50% of max hull |
| Respawn shield | 0 |
| Respawn invulnerability | 1.0 s |
| Towed wreck on life loss | Wreck breaks and drops parts at death position |
| Game over | Lives reach 0 |
| Game over screen | Shows score and currency, offers new run |

## Armour / Defence — Tier 1

| Rule | Value |
| --- | --- |
| Defence type | Shield |
| Shield module | Controls max shield and regen |
| Aegis Plate | Adds 20 max hull |
| Shield Bubble consumable | Reduces incoming damage by 60% for 5 s |
| Damage reduction stacking | Only one damage-reduction boost active; strongest applies |

## Boosts — Tier 2

| Boost | Source | Effect | Duration |
| --- | --- | --- | ---: |
| Warp | Warp Fuel consumable | Max speed +50%, acceleration +50% | 6 s |
| Tug Surge | Tug Surge consumable | Hook range +80 px, tow speed +30 px/s | 8 s |
| Bubble | Shield Bubble consumable | Incoming damage -60% | 5 s |

Boosts do not stack with themselves; using a boost refreshes its duration.

## Consumables — Tier 2

| Consumable | Effect | Cost |
| --- | --- | ---: |
| Repair Gel | Restores 30 hull | 15 |
| Shield Charge | Restores 50 shield | 20 |
| Warp Fuel | Applies Warp boost | 18 |
| Tug Surge | Applies Tug Surge boost | 22 |
| Shield Bubble | Applies Bubble boost | 25 |

Use rule: select slot, press `E` when no higher-priority interactable exists.

## Resources & Gathering — Tier 1 for basic, Tier 2 for full

Resource types:

| Resource | Base sell price |
| --- | ---: |
| Plating | 4 |
| Coil | 7 |
| Cryo | 12 |
| Shard | 9 |
| Data | 18 |

Gathering spots per sector:

| Spot | Sector 1 count | Sector 2-12 count | Tool needed | Yield | Cooldown |
| --- | ---: | ---: | --- | --- | ---: |
| Plating Pile | 4 | 4 | None | 1 Plating | 8 s |
| Coil Nest | 3 | 3 | None | 1 Coil | 8 s |
| Ice Cache | 0 | 2 | Cryo Cutter | 1 Cryo | 10 s |
| Shard Outcrop | 3 | 3 | None | 1 Shard | 8 s |
| Data Beacon | 0 | 1 | Magnet Grapple | 1 Data | 12 s |

Total gathering spots: 153.

Tools needed:

| Tool | Capability |
| --- | --- |
| Tug Wrench | Default tool; allows basic gathering and basic crafting |
| Cryo Cutter | Required for Ice Cache gathering and Cryo Tank wreck attachment |
| Magnet Grapple | Required for Data Beacon gathering and Probe wreck attachment |

## Economy — Tier 1 for basic selling, Tier 2 for full economy

| Rule | Value |
| --- | --- |
| Currency | Credits, integer |
| Starting currency | 50 |
| Score | Integer points |
| Selling | Parts sold in pause at station or kiosk |
| Sell action | `Sell All Parts` sells every part in inventory |
| Station sell price | `basePrice * priceMultiplier` |
| Kiosk sell price | `round(basePrice * 0.8 * priceMultiplier)` |
| Station buy cost | Item base buy cost |
| Kiosk consumable buy cost | `round(baseCost * 1.1)` |
| Trading | Kiosks allow module trade-back and resource exchange |
| Module trade-back | Unequip module and receive 50% of its station buy cost |
| Resource exchange | 5 Plating -> 1 Coil, 5 Coil -> 1 Shard, 5 Shard -> 1 Data |
| Resource exchange cost | Requires 5 source items and 1 empty inventory slot |
| Merchant price mods | Difficulty, sector price, Haggler, Bulk Rates |

Price multipliers:

| Modifier | Sell | Buy |
| --- | ---: | ---: |
| Casual difficulty | 1.15 | 0.90 |
| Cozy difficulty | 1.00 | 1.00 |
| Challenging difficulty | 0.90 | 1.10 |
| Haggler skill | 1.05 | 0.95 |
| Bulk Rates skill | 1.10 | 1.00 |
| Sector price | Sector table | Sector table |

## Shops & Merchants — Tier 2

| Merchant | Location | Sells | Buys / trades |
| --- | --- | --- | --- |
| Station Shop | Station Coldlight | All consumables, all modules, Cryo Cutter, Magnet Grapple | Sells all part types |
| Drifter Kiosk | Kiosk landmarks | Consumables | Sells parts at 80%, trades modules, resource exchange |

Shop access:
- Press `E` at station with a towed wreck to dock.
- Press `E` at station without a towed wreck to open pause on Shop tab.
- Press `E` at kiosk to open pause on Shop tab.
- Crafting and shop are only available while adjacent to the relevant landmark.

## Crafting & Recipes — Tier 1 for basic recipes, Tier 2 for all

Crafting stations:
- Station Coldlight: all recipes.
- Drifter Kiosk: all recipes except tools.

Recipe list:

| Recipe | Output | Resources | Currency |
| --- | --- | --- | ---: |
| `repair_gel` | Repair Gel | 1 Plating | 5 |
| `shield_charge` | Shield Charge | 1 Coil | 8 |
| `warp_fuel` | Warp Fuel | 1 Cryo | 10 |
| `tug_surge` | Tug Surge | 1 Cryo, 1 Coil | 12 |
| `shield_bubble` | Shield Bubble | 1 Shard | 10 |
| `cryo_cutter` | Cryo Cutter | 2 Cryo, 1 Coil | 30 |
| `magnet_grapple` | Magnet Grapple | 2 Shard, 1 Data | 35 |
| `thrust_coil` | Thrust Coil | 2 Plating, 1 Coil | 25 |
| `plasma_ward` | Plasma Ward | 2 Shard, 1 Coil | 30 |
| `aegis_plate` | Aegis Plate | 3 Shard, 1 Data | 45 |
| `mag_hook` | Mag Hook | 2 Plating, 1 Shard | 25 |
| `grappler` | Grappler | 2 Coil, 2 Shard | 40 |
| `expanded_hold` | Expanded Hold | 2 Plating, 1 Cryo | 20 |
| `salvage_bay` | Salvage Bay | 3 Plating, 2 Cryo | 35 |

Craft rule:
- Requires resources and currency.
- Consumables require an empty inventory slot.
- Modules and tools equip directly if their slot is empty; otherwise craft fails.

## Equipment & Tools — Tier 1 for basic equipment, Tier 2 for all

Equipment slots:

| Slot | Base module |
| --- | --- |
| Engine | Stock Engine |
| Shield | Stock Shield |
| Hook | Stock Hook |
| Cargo | Stock Hold |
| Tool A | Tug Wrench |
| Tool B | Empty |

Module table:

| Module | Slot | Stats | Buy cost |
| --- | --- | --- | ---: |
| Stock Engine | Engine | Speed 240, accel 900, dash cooldown 1.1 | 0 |
| Thrust Coil | Engine | Speed 270, accel 1000, dash cooldown 1.0 | 25 |
| Ion Ram | Engine | Speed 300, accel 1100, dash cooldown 0.9 | 45 |
| Stock Shield | Shield | Shield 50, regen 6/s, hull +0 | 0 |
| Plasma Ward | Shield | Shield 75, regen 8/s, hull +0 | 30 |
| Aegis Plate | Shield | Shield 100, regen 10/s, hull +20 | 45 |
| Stock Hook | Hook | Range 180, attach 0.3, tow speed +0 | 0 |
| Mag Hook | Hook | Range 240, attach 0.2, tow speed +20 | 25 |
| Grappler | Hook | Range 300, attach 0.15, tow speed +40 | 40 |
| Stock Hold | Cargo | Inventory 8 | 0 |
| Expanded Hold | Cargo | Inventory 12 | 20 |
| Salvage Bay | Cargo | Inventory 16 | 35 |
| Tug Wrench | Tool | Basic gathering/crafting | 0 |
| Cryo Cutter | Tool | Cryo capability | 40 |
| Magnet Grapple | Tool | Data/Probe capability | 50 |

## Progression, Score, Difficulty — Tier 1 basic, Tier 2 full

Score values:

| Action | Score |
| --- | ---: |
| Pick up part | 10 |
| Collect Star Chart | 50 |
| Collect Golden Screw | 100 |
| Collect Lore Cylinder | 200 |
| Dock wreck | Wreck score x sector price multiplier |
| Open secret | 300 |
| Complete main objective | Table below |
| Complete side quest | Table below |
| Lose life | -250 |

Currency rewards:

| Action | Currency |
| --- | ---: |
| Sell part | Price table |
| Golden Screw | 25 |
| Secret | 50 |
| Main objective | Table below |
| Side quest | Table below |

Difficulty ramp:

| Sector | Trap count | Damage multiplier | Price multiplier |
| ---: | ---: | ---: | ---: |
| 1 | 3 | 1.0 | 1.0 |
| 2 | 5 | 1.1 | 1.1 |
| 3 | 7 | 1.2 | 1.2 |
| 4 | 9 | 1.3 | 1.3 |
| 5 | 11 | 1.4 | 1.4 |
| 6 | 13 | 1.5 | 1.5 |
| 7 | 15 | 1.6 | 1.6 |
| 8 | 17 | 1.7 | 1.7 |
| 9 | 19 | 1.8 | 1.8 |
| 10 | 21 | 1.9 | 1.9 |
| 11 | 23 | 2.0 | 2.0 |
| 12 | 25 | 2.2 | 2.2 |

Difficulty options:

| Option | Damage multiplier | Sell price | Buy price |
| --- | ---: | ---: | ---: |
| Casual | 0.70 | x1.15 | x0.90 |
| Cozy | 1.00 | x1.00 | x1.00 |
| Challenging | 1.30 | x0.90 | x1.10 |

Unlock table:

| Unlock | How |
| --- | --- |
| Sector | Main objective for previous sector |
| Fast travel | Visit landmark |
| Beacon fast travel | Collect Star Chart in that sector and visit beacon |
| Recipes | Known at station; kiosk recipes available at kiosk |
| Side quests | Sector unlocked and quest giver present |
| Lore | Collect Lore Cylinder or complete related quest |
| Skill tree | Skill points from main objectives and selected side quests |

## Objectives, Plot, Main Objectives — Tier 2

Plot:
The station Coldlight runs a small salvage guild in the Cold Current. Wren, a junior tug pilot, is tasked with towing wrecks, repairing beacons, and delivering parts. As Wren works through the belt, the beacons begin to hum in a pattern that matches an old survey ship signal. The final objective is not a battle but a recovery: dock a Relay wreck at the Cold Current Node to free the dormant survey ship and record its thanks.

Main objectives:

| Objective | Sector | Requirement | Currency | Score | SP | Unlock | Cutscene |
| ---: | ---: | --- | ---: | ---: | ---: | --- | --- |
| M1 | 1 | Dock any wreck at Station | 100 | 200 | 1 | Sector 2 | C0 after game start |
| M2 | 2 | Repair Beacon 2 with 2 Plating | 100 | 250 | 1 | Sector 3 | — |
| M3 | 3 | Deliver 3 Coil to Station | 150 | 250 | 1 | Sector 4 | C4 |
| M4 | 4 | Tow a Hauler Wreck to Station | 150 | 300 | 1 | Sector 5 | — |
| M5 | 5 | Repair Beacon 5 with 1 Cryo | 175 | 300 | 1 | Sector 6 | — |
| M6 | 6 | Deliver 5 Shard to Kiosk 7 | 200 | 350 | 1 | Sector 7 | — |
| M7 | 7 | Tow a Relay Wreck to Station | 250 | 400 | 1 | Sector 8 | C8 |
| M8 | 8 | Repair Beacon 8 with 2 Coil | 250 | 400 | 1 | Sector 9 | — |
| M9 | 9 | Deliver 1 Data to Station | 300 | 500 | 1 | Sector 10 | — |
| M10 | 10 | Tow a Cryo Tank Wreck to Station | 350 | 500 | 1 | Sector 11 | — |
| M11 | 11 | Repair Beacon 11 with 1 Data | 400 | 600 | 1 | Sector 12 | — |
| M12 | 12 | Dock a Relay Wreck at Cold Current Node 12 | 500 | 1000 | 1 | Final cutscene | C12 |

Objective completion rule:
- Objectives are checked in real time.
- Deliveries require the item in inventory; item is removed on completion.
- Beacon repair requires standing at beacon and consuming resources.
- Dock objectives require successful dock.

## Side Quests, Quest Givers, Conversations — Tier 3

Quest givers:

| NPC | Location | Conversations |
| --- | --- | --- |
| Dockmaster Mara | Station Coldlight | greeting, quest, complete |
| Navigator Ido | Beacon 2 | greeting, quest, complete |
| Drifter Nyx | Kiosk 4 | greeting, quest, complete |
| Station Keeper Odo | Kiosk 7 | greeting, quest, complete |
| Surveyor Lark | Kiosk 10 | greeting, quest, complete |

Side quests:

| Quest | Giver | Sector | Objective | Currency | Score | SP |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| S1 | Mara | 1 | Collect 5 Plating | 50 | 250 | 0 |
| S2 | Ido | 2 | Collect 3 Coil | 60 | 250 | 1 |
| S3 | Ido | 3 | Tow 1 Scutter Wreck in Sector 3 | 75 | 350 | 0 |
| S4 | Mara | 4 | Tow 1 Hauler Wreck | 80 | 300 | 0 |
| S5 | Nyx | 4 | Collect 2 Data | 120 | 400 | 1 |
| S6 | Odo | 7 | Deliver 2 Repair Gel to Kiosk 7 | 60 | 200 | 0 |
| S7 | Odo | 7 | Collect 5 Shard | 90 | 350 | 0 |
| S8 | Nyx | 7 | Fast travel to 3 different landmarks in one run | 70 | 300 | 0 |
| S9 | Mara | 8 | Craft 3 consumables | 80 | 300 | 1 |
| S10 | Lark | 10 | Collect 2 Data | 120 | 500 | 1 |
| S11 | Odo | 10 | Tow 2 Relay Wrecks | 200 | 750 | 2 |
| S12 | Lark | 12 | Find the Sector 12 secret | 150 | 500 | 1 |

Conversation lines:

| NPC | Greeting | Quest line | Complete line |
| --- | --- | --- | --- |
| Mara | “Cold belt’s quiet tonight. Wrecks don’t tow themselves.” | “Guild needs a part. Can you carry it?” | “Good hands, Wren. The station runs smoother.” |
| Ido | “Beacons are cold, but they still remember.” | “There’s a ping only a steady tug can follow.” | “The chart lights up a little. Good work.” |
| Nyx | “I drift where the cold is thinnest.” | “I heard something that should not be adrift.” | “You found what I couldn’t. Respect.” |
| Odo | “Keep your fuel warm and your grip soft.” | “A small delivery can keep a whole sector alive.” | “The keeper nods. That is high praise.” |
| Lark | “Data is patient. Mostly.” | “One more piece, and the old ship wakes up.” | “The survey log opens. Thank you.” |

Conversations play as short radio overlays when the player stands within 64 px of an NPC and presses `E` with no higher-priority interactable.

## Skill Tree — Tier 3

Skill point sources:

| Source | SP |
| --- | ---: |
| Main objective | 1 each, 12 total |
| Side quest S2 | 1 |
| Side quest S5 | 1 |
| Side quest S9 | 1 |
| Side quest S10 | 1 |
| Side quest S11 | 2 |
| Side quest S12 | 1 |
| Total available | 19 |

Skill tree:

| Branch | Node | Cost | Effect |
| --- | --- | ---: | --- |
| Towing | Long Arm | 1 SP, 50 C | Hook range +20 |
| Towing | Soft Dock | 2 SP, 100 C, 2 Plating | Tow speed +10% |
| Towing | Salvage Sense | 3 SP, 200 C, 1 Data | Wreck part yield +1 of first listed part |
| Trading | Haggler | 1 SP, 40 C | Sell +5%, buy -5% |
| Trading | Bulk Rates | 2 SP, 80 C | Sell +10% |
| Trading | Credit Cache | 3 SP, 150 C, 1 Data | Quest score +10% |
| Defense | Patches | 1 SP, 30 C | Max hull +10 |
| Defense | Capacitor | 2 SP, 70 C | Max shield +10 |
| Defense | Auto-Repair | 3 SP, 120 C, 2 Coil | Shield regen +2/s |

Skill node prerequisites:
- Soft Dock requires Long Arm.
- Salvage Sense requires Soft Dock.
- Bulk Rates requires Haggler.
- Credit Cache requires Bulk Rates.
- Auto-Repair requires Patches and Capacitor.

## Collectibles, Secrets, Lore — Tier 3

Collectibles:

| Type | Count | Rule | Reward |
| --- | ---: | --- | --- |
| Star Chart | 12 | One per sector; required for beacon fast travel in that sector | +50 score |
| Lore Cylinder | 12 | One per sector; unlocks lore | +200 score |
| Golden Screw | 24 | Two per sector near traps | +100 score, +25 C |

Secrets:

| Sector | Secret | Condition | Resource reward |
| ---: | --- | --- | --- |
| 1 | Loose Bolt Cache | None | 3 Plating |
| 2 | Frozen Coil Box | Cryo Cutter | 2 Coil |
| 3 | Probe Echo | Magnet Grapple | 1 Data |
| 4 | Ice Pocket | None | 2 Shard |
| 5 | Static Stash | None | 3 Cryo |
| 6 | Cutter’s Cache | Cryo Cutter | 1 Data |
| 7 | Gate Scrap | None | 5 Plating |
| 8 | Narrow Stash | Magnet Grapple | 2 Cryo |
| 9 | Dim Pocket | None | 3 Coil |
| 10 | Ash Cache | None | 2 Data |
| 11 | Pale Box | Cryo Cutter | 1 Data |
| 12 | Final Cold Box | Magnet Grapple | 3 Shard |

Secret reward: 300 score + 50 C + listed resource.

Lore entries:

| Sector | Lore text |
| ---: | --- |
| 1 | “Cold Dock was built on a drowned survey grid.” |
| 2 | “The first beacon sang in a language of static.” |
| 3 | “Wrecks here face the same way the old ships did.” |
| 4 | “Blue Hollow hums when the current is thin.” |
| 5 | “A crew once named the stars by their coldness.” |
| 6 | “Grey Trench keeps what the light forgets.” |
| 7 | “Polar Gate opens only for patient tugs.” |
| 8 | “The quiet narrows remember every dropped bolt.” |
| 9 | “Dim Current carries data older than the station.” |
| 10 | “Ash Ridge is where old engines cool.” |
| 11 | “Pale Expanse looks like snow that never fell.” |
| 12 | “The Cold Current is not a storm. It is a voice.” |

## Cutscenes — Tier 3

| Cutscene | Trigger | Panels | Text |
| --- | --- | ---: | --- |
| C0 | After title start | 3 | “Cold Dock. Wren’s tug bobs at the dock.” / “The Guild needs wrecks towed and parts home.” / “The cold belt is quiet. For now.” |
| C4 | Main objective M3 complete | 3 | “A new shimmer moves through Blue Hollow.” / “The beacon lights flicker in a pattern.” / “Something old is waking up.” |
| C8 | Main objective M7 complete | 3 | “The beacons sing together.” / “Their signal matches the missing survey ship.” / “The Cold Current is not random.” |
| C12 | Main objective M12 complete | 3 | “The Relay wreck docks into the node.” / “A dormant survey ship powers on.” / “Aurora Cold logs its thanks and goes quiet.” |

Cutscene rule:
- Cutscenes are canvas overlays, not top-level screens.
- Press `E` or click to skip.
- Reduced motion disables fade, shows panels statically.

## Hints — Tier 2 basic, Tier 3 full

| Hint trigger | Text |
| --- | --- |
| First station | “Dock wrecks with E. Sell parts in pause.” |
| Hull below 30 | “Hull low. Use Repair Gel.” |
| Near main objective landmark | “Objective nearby.” |
| Quest available at NPC | “A new task is available.” |
| Fast travel unlocked | “Beacon added to fast travel.” |
| Inventory full while docking | “Inventory full. Sell or drop parts.” |
| Drone fragment warning | “Drone fragment charging.” |
| Secret condition unmet | “This cache needs a tool.” |

Hint rule:
- Toasts are transient canvas messages, not persistent HUD.
- Max 1 visible toast at a time.
- Queue max 3.
- Duration 3.5 s.
- Reduced motion disables slide-in.

## Feel — Tier 1 basic, Tier 2 full

| Feel element | Rule |
| --- | --- |
| Particles | Pickup: 6 squares, 0.3 s. Damage: 8 squares, 0.3 s |
| Hit flash | 1 frame white flash on damaged sprite |
| Trails | Engine trail 0.3 s when thrusting; dash trail 0.3 s |
| Reduced motion | Disables particles, trails, cutscene fades, minimap ping |
| Coziness | Respawn is not harsh; NPCs are friendly; no enemy attacks |
| Difficulty | Traps scale, but prices and rewards scale too |

# 5. CHARACTERS

## Player ship: Wren’s Salvage Tug

Silhouette:
- 16 x 16 px compact tug.
- Pale nose, teal body, grey wings, dark cockpit pixel.

Facings:
- 8 directions snapped from continuous heading.

Animation names and motion rules:

| Animation | Frames | Duration | Motion rule |
| --- | ---: | ---: | --- |
| `idle` | 4 | 2.0 s loop | Slight thruster flicker |
| `thrust` | 6 | 0.5 s loop | Play when `throttle != 0` |
| `reverse` | 4 | 0.7 s loop | Play when `throttle < 0` |
| `dash` | 3 | 0.18 s | Play during dash; stretch shape |
| `damaged` | 2 | 0.3 s | Play on hit flash |
| `towing` | 4 | 1.0 s loop | Play while `towed` active |
| `docking` | 2 | 1.0 s | Play during dock success |
| `dead` | 3 | 0.5 s | Play on life loss |

States gameplay needs:
- `idle`
- `moving`
- `reversing`
- `dashing`
- `damaged`
- `towing`
- `docking`
- `dead`

## NPC silhouettes

| NPC | Silhouette | Facings | Animations | States |
| --- | --- | ---: | --- | --- |
| Dockmaster Mara | 16 x 16, blue-grey coat, pale badge | 4 | `idle` 4 frames 3.0 s, `talk` 2 frames 0.5 s, `give` 2 frames 0.8 s | idle, talk, give |
| Navigator Ido | 16 x 16, grey hood, cyan scarf | 4 | same | idle, talk, give |
| Drifter Nyx | 16 x 16, slim silhouette, teal scarf | 4 | same | idle, talk, give |
| Station Keeper Odo | 16 x 16, bulky grey coat, pale visor | 4 | same | idle, talk, give |
| Surveyor Lark | 16 x 16, pale coat, small data case | 4 | same | idle, talk, give |

NPC rule:
- NPCs are static landmarks; they do not move.
- `E` plays conversation if no higher-priority interactable.
- Quest giver `give` animation plays when quest available or complete.

## Wreck vehicles

| Wreck | Silhouette | Animations | States |
| --- | --- | --- | --- |
| Scutter | 16 x 16 small hulk | `intact` 4 frames 2.0 s, `towed` 4 frames 1.0 s, `damaged` 2 frames 0.3 s, `broken` 1 frame | intact, hooking, towed, damaged, broken |
| Hauler | 32 x 16 medium hulk | same | same |
| Cryo Tank | 32 x 16 with cyan tank | same | same |
| Probe | 24 x 16 with antenna | same | same |
| Relay | 40 x 20 large hulk | same | same |

Wreck rule:
- Wrecks are non-moving vehicles.
- Wrecks can be attached, towed, damaged, broken, and respawned.

# 6. AUDIO

| Sound | Recipe | When |
| --- | --- | --- |
| `music_main` | 100 BPM chiptune loop; square bass C2/C2/G1/G1/A1/A1/F1/F1 on 8ths; pulse lead E4/G4/A4/C5 every 2 beats; triangle pad C major | During game, not on title/pause/game over |
| `ui_blip` | Square 880 Hz, 0.05 s, gain 0.3 | Menu move |
| `ui_confirm` | Square 990 Hz to 1320 Hz, 0.08 s | Confirm |
| `ui_cancel` | Triangle 330 Hz to 220 Hz, 0.08 s | Cancel |
| `thrust_loop` | Low-pass noise 800 Hz, gain follows throttle | While thrusting |
| `dash` | Square 180 Hz to 320 Hz, 0.12 s | Dash |
| `hook_attach` | Triangle 440 Hz 0.05 s, then 660 Hz 0.05 s | Hook attached |
| `hook_detach` | Triangle 660 Hz to 440 Hz, 0.06 s | Hook detached |
| `part_pickup` | Square 1046 Hz, 0.06 s | Item picked |
| `part_drop` | Square 784 Hz, 0.06 s | Item dropped |
| `damage` | Noise burst 0.1 s + square 110 Hz 0.1 s | Hull or shield hit |
| `shield_hit` | Triangle 1320 Hz, 0.05 s | Shield absorbs first |
| `death` | Square 440 Hz to 110 Hz, 0.4 s | Life lost |
| `respawn` | Triangle 220 Hz to 880 Hz, 0.3 s | Respawn |
| `sell` | Square arpeggio 880/1108/1318 Hz, 0.15 s | Parts sold |
| `buy` | Square 659 Hz to 987 Hz, 0.08 s | Item bought |
| `craft` | Pulse 523/659/784 Hz, 0.1 s | Craft complete |
| `fast_travel` | Sweep 440 Hz to 1760 Hz, 0.2 s | Fast travel |
| `beacon` | Pulse 660 Hz, 1.0 s loop | Near unlocked beacon |
| `secret_open` | Square 784/988/1175 Hz, 0.15 s | Secret opened |
| `cutscene_start` | Triangle 523 Hz to 784 Hz, 0.2 s | Cutscene begins |

# 7. UX

HTML and CSS only:
- `#app` contains `canvas#game` and four screen divs.
- Screens are DOM overlays styled with CSS.
- No external assets except an optional embedded pixel font.
- All text uses uppercase, blocky pixel-style typography.
- `image-rendering: pixelated` on canvas.
- Reduced motion adds `.reduced-motion` to `#app`, disabling CSS transitions.

DOM:

| Element | Purpose |
| --- | --- |
| `#app` | Root container |
| `canvas#game` | Game rendering |
| `#hud` | Persistent HUD: health, score, minimap, currency |
| `#screen-title` | Title screen |
| `#screen-pause` | Pause screen with tabs |
| `#screen-settings` | Settings screen |
| `#screen-gameover` | Game over screen |

State machine:

| Current | Event | Next | Notes |
| --- | --- | --- | --- |
| `title` | Start | `game` | Resets state, plays intro cutscene |
| `title` | Settings | `settings` | Returns to title |
| `game` | Pause | `pause` | Pauses fixed-step gameplay |
| `game` | Settings | `settings` | From pause only in implementation |
| `pause` | Resume | `game` | Returns to previous gameplay |
| `pause` | Settings | `settings` | Returns to pause |
| `settings` | Back | Previous screen | Title or pause |
| `game` | Lives reach 0 | `gameover` | Shows game over |
| `gameover` | New run | `title` | Full reset |

Pause tabs:

| Tab | Content |
| --- | --- |
| Resume | Return to game |
| Inventory | Show 8+ slots, select slot |
| Shop | Sell parts, buy items, trade modules/resources when near merchant |
| Crafting | Craft available recipes when near crafting station |
| Skill | Spend skill points |
| Quests | Show main and side quests |
| Fast Travel | Travel to visited landmarks |
| Settings | Accessibility options |

HUD table:

| HUD element | Record field | Visible when |
| --- | --- | --- |
| Health bar + life pips | `ship.hp`, `ship.maxHp`, `lives` | `game` |
| Score | `score` | `game` |
| Minimap | `world.minimap` | `game` |
| Currency | `currency` | `game` |

Minimap rules:
- 128 x 128 px canvas region in HUD.
- Shows current sector, player dot, unlocked landmarks, active wrecks, traps.
- Colour-blind safe: landmarks are shapes; player is a bright cross; wrecks are small squares; traps are small triangles.
- Reduced motion disables minimap ping.

CSS rules:
- Background: `#0A1218`.
- Text: `#DDE7EC`.
- Buttons: 48 x 32 px, 2 px border, no rounded corners.
- Focus: 2 px cyan outline.
- Pixel font: blocky bitmap style, 16 px or larger.
- Reduced motion: no transitions, no animations.

# 8. DEBUG API

| Function | Purpose |
| --- | --- |
| `debug_ship_set(x, y, heading)` | Set ship position and heading |
| `debug_ship_setAlive(alive)` | Set alive state |
| `debug_health_set(hp, shield, lives)` | Set health, shield, lives |
| `debug_score_set(n)` | Set score |
| `debug_score_add(n)` | Add score |
| `debug_currency_set(n)` | Set currency |
| `debug_skill_points_set(n)` | Set skill points |
| `debug_tow_attach(wreckId)` | Attach wreck directly |
| `debug_tow_detach()` | Detach wreck |
| `debug_inventory_clear()` | Clear inventory |
| `debug_inventory_give(itemId, count)` | Give items |
| `debug_equipment_set(slot, moduleId)` | Equip module |
| `debug_boost_apply(id)` | Apply boost |
| `debug_world_setSector(id)` | Load sector |
| `debug_world_unlockSector(id)` | Unlock sector |
| `debug_world_spawnTrap(type, x, y)` | Spawn trap |
| `debug_world_fastTravel(landmarkId)` | Fast travel |
| `debug_economy_sellAll()` | Sell all parts at current merchant |
| `debug_economy_buy(itemId)` | Buy item ignoring adjacency |
| `debug_crafting_craft(recipeId)` | Craft recipe |
| `debug_quests_start(questId)` | Start quest |
| `debug_quests_complete(objectiveId)` | Complete objective |
| `debug_secret_open(id)` | Open secret |
| `debug_collectible_toggle(id)` | Toggle collectible |
| `debug_lives_set(n)` | Set lives |
| `debug_difficulty_set(mode)` | Set difficulty |
| `debug_cutscene_play(id)` | Play cutscene |
| `debug_conversation_play(npcId)` | Play conversation |
| `debug_respawn()` | Trigger respawn |
| `debug_game_over()` | Trigger game over |

Player input debug functions:

| Function | Purpose |
| --- | --- |
| `input.press('thrustForward')` | Press forward thrust |
| `input.press('thrustBack')` | Press reverse thrust |
| `input.press('turnLeft')` | Press left turn |
| `input.press('turnRight')` | Press right turn |
| `input.release(action)` | Release movement key |
| `input.dash()` | Trigger dash |
| `input.hook()` | Toggle hook |
| `input.interact()` | Trigger interact |
| `input.drop()` | Drop selected |
| `input.selectSlot(i)` | Select slot |
| `input.pause()` | Trigger pause |
| `input.startGame()` | Trigger start |
| `input.settings()` | Trigger settings |

# 9. TESTS

Tier 1 tests:

- Title screen shows and Start enters game.
- Player spawns at station in sector 1.
- HUD shows health, score, minimap, currency.
- Ship turns and moves with default keys.
- Dash applies speed burst and cooldown.
- Hook attaches to a wreck within range.
- Towed wreck follows behind ship.
- Docking a wreck adds parts and score.
- Inventory full prevents docking.
- Parts can be sold in pause at station.
- Currency updates after selling.
- Basic crafting recipe can craft an item.
- Basic module can equip and change ship stat.
- Trap damages shield before hull.
- Hull reaching zero loses a life.
- Respawn occurs at last safe spawn.
- Lives reaching zero shows game over.
- Pause stops gameplay.
- Settings toggles reduced motion.
- Key remap changes one control.
- Reduced motion disables particles and trails.

Tier 2 tests:

- All 12 sectors load.
- Main objectives unlock sectors in order.
- All 96 wreck spawns exist across sectors.
- All 168 traps spawn with correct sector counts.
- All 153 gathering spots spawn with correct counts.
- Tool-gated gathering and wrecks require correct tools.
- Fast travel works only to visited landmarks.
- Fast travel blocked while towing.
- Station and kiosk prices use correct multipliers.
- Module trade-back gives 50% cost.
- Resource exchange works: 5 Plating -> 1 Coil, 5 Coil -> 1 Shard, 5 Shard -> 1 Data.
- All recipes craft when resources and currency exist.
- All equipment slots apply stats.
- All consumables apply effects.
- Boosts refresh duration and do not stack.
- Difficulty options change damage and prices.
- Score values match tables.
- Currency rewards match tables.
- Wreck break drops parts and starts respawn timer.

Tier 3 tests:

- All 12 side quests can be started and completed.
- Quest givers play correct conversations.
- Skill points awarded correctly from main and side quests.
- Skill tree nodes unlock with prerequisites.
- Skill effects modify stats.
- All 12 secrets open and give rewards.
- All 48 collectibles collect and give rewards.
- All 12 lore entries unlock.
- Star Charts unlock beacon fast travel.
- All 4 cutscenes trigger at correct points.
- Cutscenes can be skipped.
- Hints appear for low hull, objective, secret tool, and inventory full.
- Quest log in pause shows active quests.

# 10. BUILD ORDER

1. Build DOM shell, CSS, canvas, and the four top-level screens.
2. Implement fixed-step loop, state factory, and input polling.
3. Implement ship physics: heading, throttle, turn, drag, dash.
4. Implement world: 3 sectors first, station, one beacon, one kiosk.
5. Implement tow: hook, attach, tow position, detach, dock.
6. Implement wrecks, parts, inventory, pickup/drop, and inventory limit.
7. Implement traps, shield/hull damage, lives, respawn, and game over.
8. Implement HUD: health/lives, score, currency, minimap.
9. Implement station selling, basic crafting, basic equipment.
10. Add pause tabs: inventory, shop, crafting, settings.
11. Add settings: reduced motion, difficulty options, remappable keys.
12. Add audio: music loop and SFX.
13. Expand world to 12 sectors with full sector content.
14. Add main objectives, sector unlock, fast travel, and difficulty ramp.
15. Add full economy: merchants, prices, trading, shops.
16. Add full recipes, tools, equipment, consumables, boosts.
17. Add side quests, quest givers, conversations, skill tree.
18. Add secrets, collectibles, lore, cutscenes, hints.
19. Run tier tests and fix numerical/content mismatches.

# 11. DEFINITION OF DONE

## Tier 1: Core Salvage Loop

High-level definition:
A new player can start from title, fly, tow a wreck, dock it, collect parts, sell parts, craft/equip an upgrade, take trap damage, lose a life, respawn, and reach game over after losing all lives.

Checkboxes:
- [ ] Title screen starts a new game.
- [ ] Pause screen pauses and resumes.
- [ ] Settings screen toggles reduced motion and remaps one key.
- [ ] Game over screen appears at zero lives and returns to title.
- [ ] Ship moves with free 2D control.
- [ ] Dash works with duration and cooldown.
- [ ] Hook attaches to a wreck.
- [ ] Towed wreck follows and can be docked.
- [ ] Docking requires inventory space.
- [ ] Parts are added to inventory on dock.
- [ ] Parts can be sold in pause.
- [ ] Currency increases on sell.
- [ ] Score increases on dock and pickup.
- [ ] HUD shows health, score, minimap, currency.
- [ ] Trap damage reduces shield then hull.
- [ ] Hull zero loses a life.
- [ ] Respawn restores 50% hull at last safe spawn.
- [ ] One basic recipe can craft.
- [ ] One equipment module can equip and change stat.
- [ ] Reduced motion disables particles/trails.

## Tier 2: Full World & Economy

High-level definition:
All 12 sectors are playable through main objectives with full world content, full economy, full equipment, and difficulty scaling.

Checkboxes:
- [ ] 12 sectors load with correct size and borders.
- [ ] Sector unlock follows main objectives.
- [ ] 96 wrecks spawn with correct per-sector mix.
- [ ] 168 traps spawn with correct per-sector count.
- [ ] 153 gathering spots spawn with correct counts.
- [ ] 20 landmarks exist with correct functions.
- [ ] 12 main objectives complete and unlock progression.
- [ ] Fast travel works from pause to visited landmarks.
- [ ] Fast travel is blocked while towing.
- [ ] Station and kiosk sell/buy prices use exact multipliers.
- [ ] Module trade-back works at kiosks.
- [ ] Resource exchange works at kiosks.
- [ ] All 14 recipes can craft when conditions met.
- [ ] All 15 modules exist and apply stats.
- [ ] All 5 consumables apply effects.
- [ ] All 3 boosts apply and refresh.
- [ ] Difficulty options change damage and prices.
- [ ] Difficulty ramp changes trap count, damage, and price per sector.
- [ ] Wreck break and respawn timer work.
- [ ] Score and currency rewards match tables.

## Tier 3: Narrative & Meta

High-level definition:
The full content layer is present: side quests, skill tree, secrets, collectibles, lore, conversations, cutscenes, and hints.

Checkboxes:
- [ ] 12 side quests can be started and completed.
- [ ] 5 quest givers exist at correct locations.
- [ ] Conversations play as radio overlays.
- [ ] Skill points total 19 are available.
- [ ] Skill tree has 9 nodes with prerequisites.
- [ ] Skill effects modify stats.
- [ ] 12 secrets open with correct conditions and rewards.
- [ ] 48 collectibles exist and collect correctly.
- [ ] Star Charts unlock beacon fast travel.
- [ ] 12 lore entries unlock.
- [ ] 4 cutscenes trigger and can be skipped.
- [ ] Hints appear for required triggers.
- [ ] Quest log in pause shows active quests.
- [ ] No top-level screen other than title, pause, settings, game over exists.

# A. SANITY

| Check | Result |
| --- | --- |
| Section headings match required order | Valid: all required headings appear in order |
| Screens limited to title, pause, settings, game over | Valid: shop, crafting, inventory, skill, quests, fast travel are pause tabs |
| HUD limited to health, score, minimap, currency | Valid: life pips are sub-fields of health element |
| No enemy units added | Valid: hostile content is traps only |
| No victory screen added | Valid: `win/lose` empty respected |
| All mechanics from decisions covered | Valid: mapped in §0.1 and §4 |
| No camera shake added | Valid: effects limited to particles, hit flash, trails |
| No save system added | Valid: reset starts fresh |
| Tool circular dependency check | Fixed: station sells Cryo Cutter and Magnet Grapple; starting currency is 50 |
| Sector content counts consistent | Valid: 12 sectors, 96 wrecks, 168 traps, 153 gathering spots, 20 landmarks |
| Skill point economy consistent | Valid: 12 main + 7 side = 19 SP, skill tree costs 18 |
| Price and damage multipliers consistent | Valid: difficulty, sector, and skill modifiers all listed |
| Reduced motion respected | Valid: disables particles, trails, cutscene fades, minimap ping |
| Colour-blind safety respected | Valid: palette is cold, icons use shape and luminance |
| Audio is synthesized | Valid: all sounds use waveforms/frequencies, no samples |
| Fixed timestep and seeded RNG documented | Valid: §1.2 |
| Debug API has system functions and input functions | Valid: §8 |
| Tests align with tiers | Valid: §9 maps to §11 |
