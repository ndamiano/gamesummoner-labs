# 0. CONCEPT
A hand-built valley plot fills the screen: a cottage on the left, three soil beds in the middle, a well by the beds, a merchant stall on the right, and a pond edge at the bottom. The player is a small pixel gardener who walks freely, pauses, and uses a bottom hotbar. A merchant stands at the stall and changes prices; a glowgoat wanders near the pond; spore-sprites drift over ripe crops. The player tends crops: plants, waters, harvests. This produces crops, coins, and seeds. There are three crops: Glassleaf, Echovine, Bubblebeans. There are three tools: watering can, net, hoe. The top-right HUD has a minimap, day, and currency.

# 1. DECISIONS

Game prompt: cozy farming game but the crops are weird alien plants
dimension: 2d
camera: top-down
time model: real-time with pause
movement model: free movement
session shape: open world
failure: no failure
tone: cozy
size: many levels, a few hours
win/lose: no ending, play forever
core mechanics: crops, grow, harvest, pick up and drop, map / world, resource types, wait and collect, gathering spots, materials, currency
supporting mechanics: unlocks, tools needed, selling, watering / tending, recipes, collectibles, placement, rewards, dig, respawn, prices, inventory limit, landmarks, shops, conversations, day / night, carry and tow, crafting stations, throw, merchants, secrets, buildable pieces, push and pull, consumables, hints, cook, dash, trading, rooms / structures, decoration, seasons, equipment, experience and levels, merge, quest givers
extra mechanics: fast travel, townsfolk, side quests, plot, upgrades to crafted items, relationships / affection, boosts, lore, collectible creatures, buildings with jobs, production chains, livestock, pets, taming, skill tree, cutscenes, companions
art style: pixel art: low-resolution sprites with visible square pixels and a limited palette
palette: pastel: soft light colours
typography: pixel font: blocky bitmap letters
music: acoustic: guitar, piano, folk instruments
sound effects style: minimal: soft clicks and tones
screens: title, pause, settings
hud: minimap, currency
effects: particles
accessibility: colour-blind safe palette, reduced motion, remappable keys

# 2. HOW IT IS BUILT

Build it with an AI as a crappy framework first: a fixed hand-built tile map, a moving square player, generic timed squares that can be planted, watered, and harvested, a stationary square that can sell items, a wandering square, drifting dots, a bottom hotbar with three selectable slots, a top-right HUD with a minimap, a day counter, and a currency counter, and a pause key; get that looping with keyboard controls until it plays before art. Then replace each placeholder one at a time: the fixed map becomes the valley plot, the timed squares become Glassleaf, Echovine, and Bubblebeans, the hotbar slots become the watering can, net, and hoe, the sell square becomes the merchant, the wandering square becomes the glowgoat, the dots become spore-sprites, and the generic counters become day and currency; do not add new rules, systems, or screens while doing this. Then draw the UI in pixel font: hotbar, minimap, currency, day, and pause panel. A cozy farming sandbox is one hand-built map, one player, three crops, three tools, one shop, one time clock, one HUD; nothing in the concept changes what a cozy farming sandbox is.

# 3. THE GAME WE WANT

## Story
You are a gentle traveller who arrives in the Hollow Vale with one seed-pod and a note from your estranged grandmother. She used to say that the best way to understand the universe is to grow something in it. You have chosen to stay, because you want the quiet kind of life your grandmother never let herself have: a cozy farming game but the crops are weird alien plants. You are not here to win or prove anything. You are here to learn how these seeds behave, to tend them, and to let them change the places and people around you. The obvious alternative—leaving as soon as the first season ends—is not open to you. The only road out closes after the first meteor-bloom, not as a trap, but as a slow invitation: the land asks to be noticed. If you fail, there is no catastrophe. The worst that can happen is that the valley remains unfinished: friendships stay shallow, gardens stay small, and the alien plants keep their secrets. That is the stake: not loss, but missed warmth.

## World
The game is a top-down open world made of many levels: a pastel village with tiny houses, terraced fields, a moonlit orchard, a cavern of singing crystals, a tidal mudflat, and a crashed seed-ship half swallowed by moss. You move freely through it with a small gardener, and the world continues in real time unless you pause. The townsfolk have lives of their own. Merchants restock stalls, cooks try new soups, children chase spore-sprites, shepherds move woolly glowgoats, builders haul planks, and shy archivists catalogue fragments of alien lore. If you do nothing, they still tend, trade, talk, and move toward their own quiet goals.

You can act on almost everything. You can dig soft soil, pull weeds, push and tow loaded carts, throw seed packets, water beds, harvest ripe crops, pick up and drop crates, place buildable pieces, and decorate rooms and structures. You can gather materials from gathering spots that respawn, wait and collect growing crops, sell at shops, trade with merchants, cook recipes, craft at stations, and use tools as you unlock them. The world reacts. A built tea house becomes a building with jobs. Landmarks become fast-travel points. Each action is a small kindness that changes the mood of the valley.

## Content
The content is organized around cozy tasks that grow stranger as you learn. There are many kinds of alien crops. Glassleaf is fragile and must be tended at night. Echovine grows in spirals and can be merged into stronger stalks. Bubblebeans float and must be caught with a net. Starwheat ripens in weather patterns. Moonmoss spreads across walls and can be used for decoration. Some crops are food, some are materials, some are currency-adjacent resources, and some are used to build relationships with people and creatures. You can also find collectible creatures, tame pets, rare seeds, lore fragments, tools, equipment, consumables, boosts, and secrets hidden behind waterfalls.

The people are not quest dispensers only. Quest givers are neighbours with habits: a baker who wants rare flour, a child who wants a pet name, a merchant who tests fluctuating prices, a librarian who asks you to dig beneath old trees. Side quests, plot, cutscenes, and conversations reveal the valley’s history: why the seed-ship fell, what your grandmother was searching for, and how the alien plants came to be loved here. There are skill trees, experience and levels, tool upgrades, crafted item upgrades, production chains, buildings with jobs, shops, trading posts, and rooms you can build or decorate.

Sessions differ because seasons change, markets change, townsfolk remember what you helped with, and some plants only appear after certain events. Across sessions, the valley grows: fast travel expands, new gathering spots unlock, relationships deepen, affection increases, townsfolk take jobs, animals breed, recipes unlock, and the map fills with your gardens, bridges, lanterns, and quiet memorials. The game offers many levels and a few hours of play, then continues forever.

## A Session
You begin at a title screen with soft guitar, blocky bitmap letters, and low-resolution pastel sprites breathing behind the menu. From settings you choose a colour-blind safe palette, remappable keys, reduced motion, and sound. Then you arrive at your small plot. The HUD shows a minimap, currency, day, and season. You open the map, mark a spot, and move freely through the top-down valley. You dash across a bridge, pause the real-time clock to think, then water three glassleaf beds and plant starwheat. A town notice board lists side quests and hints. You talk to a merchant, sell a small pile of materials, and buy a new tool.

You choose what to do next. Maybe you tow a cart of compost to a new field, push a fallen log aside, or cook a stew for a shy neighbour. Maybe you fish for moonmoss, dig for a relic, or chase a collectible creature with a net. You manage an inventory limit, so you pick up, drop, and return for what you need. You use crafting stations, build a lantern, place decoration, and feed a glowgoat. As you work, particles drift, plants pulse, and townsfolk react with affection, jokes, or new hints.

If you complete your day’s plan, the session ends in a soft chime, a reward, a new recipe, or a cutscene of people enjoying your garden. If you set a goal and miss it, there is no failure. The crops do not die in shame. The world simply waits, and you can rest, pause, or try again. The session closes when you choose: by sleeping, by closing the game, or by sitting on a bench while the acoustic music fades into night.

## Resolution
There is no ending. You can play forever. After a few hours you may have restored the valley, learned every crop, built every room, and heard every story, but the game keeps growing: new seasons, new visitors, new seeds, new decorations, new small problems. The player is left with a living place. The alien plants are no longer strange; they are part of the village. The people are no longer distant; they are friends. The player keeps their gardens, their tools, their companions, their recipes, their affection, and the quiet knowledge that they made a cozy world by tending it one day at a time.
