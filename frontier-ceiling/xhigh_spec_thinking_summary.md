I'm working through the core design constraints for this game — 2D side-on turn-based grid movement across a short sequence of levels with permadeath and a silly tone, where winning means reaching the exit and defeating a final boss. I'm starting to outline the tier-one mechanics like player health and enemy behavior.

I'm sorting mechanics into tiers of importance: tier two covers things like weapons, dodging, traps, and shops, while tier three adds extras like taming, companions, and score systems. I'm noticing some tension since elements like score, combo counters, and currency appear in HUD and screen designs despite being lower-tier mechanics, so I need to reconcile that against the rule that only tier-one mechanics should be visually represented in the chosen art style.

My resolution: HUD slots get reserved space early, but individual elements like currency, score, and combo counters only become visible once their corresponding mechanic tier unlocks — health stays tier one, currency appears at tier two, and score/combo show up at tier three. I'm applying the same logic to screens, placing things like the high-scores screen alongside its tier-three mechanic rather than treating it as a pure UX decision available from the start.

Since later-tier mechanics can't be dependencies of tier 1, their HUD elements shouldn't appear in tier 1 either — I'll note that ruling explicitly. Accessibility options like colorblind palettes, reduced motion, remappable keys, and difficulty settings are a separate concern though, and difficulty options specifically can live in tier 1 as a setting affecting HP/damage without conflicting with the tier 2 difficulty-ramp mechanic. Turning to the core game itself: it's a roguelike deckbuilder with grid-based movement, side-on perspective, climbing and falling — essentially a side-view tower where each floor is a grid of tiles.

I'm sketching the turn-based core loop: a wizard cat with a hand of cards representing moves and attacks, spending a mana-like resource each turn, with cards like "Scamper" for lateral movement and "Pounce" for jumping, plus gravity rules where stepping off a ledge causes a fall with damage past a certain height, enemies on the grid, and an exit door per floor leading to a boss on the final one.

Free movement with 2 move points per turn, costing extra to climb, while cards handle block and special moves. But I notice melee attack and shoot are listed as tier 2 mechanics, not tier 1 — which raises the question of how the player actually damages enemies at the base tier, since that must come through ability/spell cards instead of basic attacks.

That separation seems workable: tier 1 cards act as spells hitting a target tile within range, no projectile travel involved, while tier 2 introduces melee as a free bump-to-attack action and shooting as a projectile that travels across the grid until blocked. I'm second-guessing whether a tier 1 card like "Claw Swipe" that hits an adjacent tile counts as melee, so I'll avoid naming adjacency-based attacks in a way that conflicts with the tier 2 melee mechanic.

A bigger concern surfaces though: if armour/defense is reserved for tier 2, tier 1 has no block mechanic at all, which is unusual for a deckbuilder. That means early defense has to come from movement away from threats and healing cards rather than blocking, so tier 1's card pool shapes up as Move, ranged Attack spells, Heal, and Draw effects.

Enemies instead telegraph their intents on specific tiles, letting the player dodge by repositioning — like Into the Breach. Tier 2 then introduces a proper Dodge mechanic (a card granting a charge that negates the next hit and hops you a tile) and a Dash action for multi-tile straight-line movement, plus terrain features like ladders/vines for climbing and falling hazards.

Falling needs its own weight: no support means you drop with damage scaling past a couple tiles, though pushing enemies off ledges stays a tier 3 feature rather than base kit. I want falling to feel like a genuine tactical option too — a way to dodge or take a shortcut — and I'm toying with simple tier 1 cards like a gravity effect that weighs an enemy down, keeping the overall system lightweight.

Now I'm sketching concrete falling interactions: a "Feather Fall" card that cancels fall damage and draws a card, and a "Pounce" special move letting you drop onto an enemy below in your column for bonus damage based on distance fallen, without hurting yourself. Flying enemies like bats ignore gravity entirely while slime-type enemies are affected normally, and I'm deciding movement works through a flat allowance of free steps each turn alongside a separate mana pool for cards.

A step lets a unit shift one tile horizontally on solid ground or vertically on a ladder, with falling off ledges happening automatically and for free. I'm weighing whether cards should grant bonus steps instead of movement being fully card-driven, since the latter risks unplayable hands, and leaning toward keeping a baseline of free steps with cards as supplements; enemies get one move per turn plus a telegraphed attack shown at the start of the player's turn.

Like Into the Breach, enemies announce targets before the player acts, letting the player reposition out of danger, which keeps things simple but risks attacks being too easy to dodge with so much mobility. To counter this, I'm considering some attacks as "tracking" types that hit wherever the player ends up within range, such as a swooping bat or a line-based archer shot, rather than locking to a fixed tile.

Tile-telegraphing seems clearest: at the start of the player's turn, each enemy that can currently reach the player locks and highlights its attack tiles in red with a damage number, so the player knows exactly what's coming. If the player isn't in range, the enemy shows a move intent instead, advancing toward the player before re-evaluating its next action.

Since attacks often cover multiple tiles and the player only gets limited steps per turn, simply stepping off the marked tile won't always be safe, which keeps the pressure meaningful even though telegraphed attacks are dodgeable in principle. I'm weighing whether enemies should also get a move after attacking to prevent the player from just dancing around with ranged spells indefinitely.

So I'm thinking of making floors objective-driven -- reach the exit, fight through guarding enemies, maybe a vertical tower layout with ladders and ledges that cost extra movement to traverse, which naturally limits infinite kiting since the player must commit to climbing or progressing rather than endlessly circling. Enemies like a ranged "Archer Rat" with a long line-attack pattern would punish players who try to kite in open corridors.

Objectives could vary by floor type: early floors unlock the exit once you simply reach it, mid floors require clearing all enemies first, and boss floors need the boss defeated before the exit opens. After each floor I'm considering a reward step where the player picks one of three cards to add to their deck, with maybe a heal option or a card-removal choice as part of the deck-building loop.

Then I'm thinking through the physical layout of a floor — ladders and vines for climbing, grid dimensions per level, and pixel resolution choices like a low-res internal canvas scaled up with 16x16 tiles, with vertical camera scrolling since levels are taller than the screen.

I'm also deciding where the card hand UI should live — since everything is HTML/CSS, the hand could be an HTML overlay at the bottom for easier click handling and text rendering, styled with pixel fonts and crisp image-rendering to match the pixel art aesthetic.

Now I'm working out canvas dimensions: an internal resolution like 320×180 scaled by an integer factor (4x to 1280x720), with levels around 16 tiles wide and 18-24 tiles tall, scrolling vertically as the camera follows the player within clamped bounds.

I realize putting the hand overlay directly over the bottom of the world view would obscure gameplay, so I'm restructuring the layout: canvas on top, hand panel as a separate DOM element below it. I'm settling on 16px tiles with a 20×10 tile view (320×160) plus a thin HUD bar, keeping the hand panel outside the game canvas entirely.

Cards should rest mostly hidden, showing just name and cost, then rise to full height on hover or selection. For level size, I'm thinking 16×22 columns centered in the 320px viewport with side margins showing tower exterior, camera following the player vertically — though maybe smaller levels would keep turn-based combat tighter and faster given the under-30-minute goal.

I'm settling on 5 floors total (4 regular plus a boss), each taking roughly 4-5 minutes, with floors sized 16×20 tiles. For construction, rather than handmaking every floor I'll assemble them procedurally from handmade 16×6 room chunks stacked vertically (plus entry/exit rows), randomly selected per floor with horizontal flipping and enemy spawn markers embedded in the chunk templates — giving roguelike variety while staying manageable to build.

I'm distinguishing basic enemy placement at level generation from the tier 2 "spawn points" mechanic, which I'll implement as visible mousehole tiles that spawn a new enemy every 4 turns until destroyed. Now I'm thinking through the player character's name and identity — leaning toward something like "Professor Mittens" for the wizard cat protagonist.

Then I'm defining the core stats and turn structure: HP 30 max on normal difficulty, 3 mana and 2 steps per turn, drawing 5 cards with a hand max of 10. I'm laying out the turn sequence — player refills resources and acts, then enemies execute and plan intents, then gravity resolves — and working through how gravity applies after any movement, with support determined by solid tiles, platforms, or ladders.

Now I'm figuring out fall damage math: no damage for short falls, scaling damage for falls of three tiles or more, with bats exempt since they fly. I'm also brainstorming a goofy "pounce" mechanic where landing on another unit crushes them for bonus damage while the faller rests on top, treating units as solid support for whatever lands on them.

Settling on landing-on-a-unit rules: the one landed on takes damage proportional to fall distance while the faller avoids fall damage entirely, turning drops into an offensive tool. Then I'm moving to ladder mechanics, where standing on a ladder tile counts as support and climbing requires ladder tiles above or below.

I should define distinct tile types: solid brick that blocks and supports from the cell below, one-way platforms that support but allow passing through upward and dropping down, and ladder cells that units can occupy and climb within. I'm working through how ladders interact with floor rows, like whether the floor cell itself can double as a ladder cell so units standing above it can descend through.

Falls are confined to tier 1 within the floor, while spikes and traps belong to tier 2. For the climbing mechanic, I like the idea of ladders being styled as dangling yarn ropes or curtains for the cat theme — keeping the underlying type as LADDER in code but giving it a cuter visual identity.

Actually, rope visuals might be too narrow to read clearly, so wooden scratching-post ladders wrapped in rope would be clearer while still fitting the theme. For pacing, I need to figure out movement costs: with 3 steps per turn on a ~16×20 floor with a typical path of 35 tiles, that's roughly 12 turns of pure movement plus combat, so across 5 floors I'm estimating around 75 turns total.

That puts the run near 25 minutes at 20 seconds per turn, which is cutting it close to the 30-minute target, so I should shrink floor dimensions — maybe 15 columns by 17 rows, or consider fitting the whole level on screen at 20×11 tiles without scrolling to speed things up, though that weakens the climbing feel compared to a scrolling layout.

Working out the grid more precisely: a 15-wide, 18-tall layout with a solid ceiling row and ground row, divided into chunks of four rows each — three air rows plus one floor row where units stand, with ladders threading through to connect levels, and no jumping outside special move cards.

Actually reconsidering the fall damage balance: with two air rows plus one floor row per chunk, dropping one floor level costs nothing, but dropping two levels deals real damage, which feels like a cleaner risk/reward than the larger gap.

I'm mapping out the full grid: 5 stacked chunks of 3 rows each, with the bottom ground row closing it off, and the exit placed on the top layer right above its floor.

I'm working out the vertical spacing between layers — each layer's standing row sits just one air row below the floor of the layer above, giving only two rows of headroom, and ladders need to span that gap connecting layer L to L+1.

For fall damage, I'm setting a threshold where drops of 3 tiles or less are free, and anything beyond that costs 2 damage per extra tile, so a two-layer fall deals 6 damage and a three-layer fall deals 12. With 5 layers total, that puts the overall structure height at 16 rows.

Estimating pacing now: each layer takes roughly 10 steps to traverse, so across 5 layers that's 40-50 steps, around 15 turns plus combat, which might push total playtime close to 30 minutes with 4 normal floors and a boss floor. To tighten this up, I'm considering trimming to 4 layers per floor instead, giving a height of 13 rows with floor rows at 12, 9, 6, 3 and standing rows at 11, 8, 5, 2.

Working out the canvas dimensions now: a 15x13 tile level at 16px tiles gives 240x208 pixels, and I'm figuring out how the camera should scroll vertically to keep the visible area correct given the hand overlay at the bottom covers about 36px and the HUD takes 14px at top, leaving a visible world of roughly 8 tiles.

For the boss floor, I'll keep it the same 15x13 fixed arena size.

For level generation, rather than per-layer chunk templates, I'm considering handmade floor strip templates for each major row (3, 6, 9) — 15-character strings using symbols for walls, gaps, and ladders, with the constraint that each strip needs at least one ladder connecting through the layers above.

Working out the ladder mechanics: a ladder at a given floor row needs to span three rows so a unit standing below can climb up to the standing row of the layer above. I also need to make sure gaps don't interfere with ladder placement, since a unit on a gap tile falls through rather than climbing.

Instead of generating fully random floor layouts, I'm considering a handcrafted pool of layouts to avoid unreachable configurations — since random gaps could split a layer into segments that strand a unit away from the ladder, causing it to fall through instead of climbing up.

So I'd need a BFS reachability validator that checks start-to-exit paths using walk, climb, fall, and dash-over-gap rules, generating and retrying layouts until one passes or falling back to a known-good template. That seems like a solid engineering approach: generator plus validator, with handmade complete floors mirrored and randomized for enemy placement as a simpler alternative.

Designing strip layouts for the floor...

Finishing that last segment checks out too. Now I'm thinking about edge walls (out-of-bounds columns treated as solid) and entity placement: start position on a random column away from exit, exit door placed on the top layer on a supported cell a few columns from any ladder, with the reachability validator confirming the path works.

For enemy placement, I'm putting them on standing rows across floors 1–3 and away from the start on floor 0, always on supported, non-ladder, non-exit cells, following the per-floor count table. Falling becomes both a hazard and a tactic since enemies can be crushed by drops, which reinforces the core climbing/falling mechanic feeling fun on its own.

Now I'm drafting the tier 1 starter deck with a 3 mana/turn cap — starting with a Zap card (cost 1, 5 damage at range) and building out the rest of the ten-card starter set.

For range, I'm settling on Chebyshev distance without line-of-sight requirements for tier 1 spells, saving wall-blocked projectiles for tier 2. I'm also reconsidering healing cards as too strong for the starter deck, since defensive tools in tier 1 should lean on movement and positioning rather than healing, push (reserved for tier 3), or status effects like stun, which I'm now folding into the cat's special move kit instead.

So I'm sketching out a dedicated special move, "Pounce," bound to its own button with a charge meter built up by playing cards — four charges to activate. It lets the cat leap up to two tiles including vertically, ignoring gravity mid-jump and falling after landing, with potential bonus effects if the landing spot drops onto an enemy below.

I'm working through whether this gives a shortcut for climbing floors without ladders, tracing the geometry row by row to see if jumping upward lands you on solid floor, in a gap that just makes you fall back down, or actually onto the standing row above — concluding the vertical range might need adjusting for it to function as a real climb mechanic.

To avoid the visual weirdness of leaping through solid floor, I'll require line-of-sight: the path from start to destination must not cross solid cells, so gaps in floors become meaningful routes for the pounce. For resource management, I'm leaning toward a "Magic Whiskers" meter that builds up as cards are played, capping around 4, with Pounce costing a chunk of it rather than a flat cooldown.

I want to keep the special move singular—Pounce—while letting cards grant secondary effects like Hiss, rather than stacking multiple distinct special moves. For card types, I'm sketching categories like Spell for damage, Trick for movement/utility, and possibly Charm for lasting floor-based effects, while still figuring out how defense fits into the tier 1 card pool.

Thinking through tier 1 spell concepts: heals, self-teleport, and an intent-cancel effect like "Laser Pointer" that disrupts an enemy's telegraphed move, which feels like a fun defensive counter in a telegraph-based system. I'm saving bigger mechanics like transformation, push/pull, and elemental damage types for tier 3, keeping tier 1 damage simply arcane. Now I'm drafting the actual starter deck list, starting with Zap as a basic ranged damage card and a movement card called Scamper.

Continuing the starter deck with Scamper as a free movement card, Laser Pointer as a low-cost intent-cancel effect, and Lick Wounds as a small heal, while I debate whether to formalize an "exhaust" sub-mechanic tied to draw/discard, possibly introducing a "Vanish" keyword for cards that leave play permanently.

I'm settling the heal amount for Lick Wounds and adding Sparkle Burst as an area damage card, then sketching the overall deck size and draw pace. I'm also starting to build out the tier-1 reward card pool with around fourteen cards split across rarities.

Still drafting utility and crowd-control cards, trying out names like Curiosity, Laser Pointer, and a lift-and-fall damage mechanic for knocking enemies off ledges.

I'm also exploring terrain-altering cards like "Hole-y Moley" that collapse floor tiles, forcing enemies to fall and take damage, though I'm wary it could break map reachability.

To avoid softlocks, I'm considering restricting targets to exclude cells under exits/ladders and having the hole auto-close after a few turns, since units only occupy the gap transiently while falling through.

Then I'm brainstorming spells: Trapdoor to temporarily open a floor tile, Anvil as a straightforward damage spell dropped from above, and Featherfall as a simple fall-damage-negation cantrip.

I keep iterating through more ideas — Nine Lives as a rare safety-net that resets HP to 9 once per floor, Moon Beam hitting everything in a vertical column, Yowl canceling nearby enemy intents, and Zoomies granting extra movement steps — discarding some like Copycat and Hiss as too complex or redundant.

I'm also weighing small mana-generation cards like Purr-ception, balancing draw and mana gain carefully so they stay fair at uncommon rarity without creating infinite loops, while trying to avoid naming overlap with consumable items like Tuna Can.

I'm sketching a rare leap attack, Comet Cat, that deals splash damage on landing, and considering whether deck-building rewards should also offer a card-removal option alongside the usual pick-one-of-three choices to keep deck thinning viable.

Settling on a three-way reward screen after each floor: pick one of three cards, remove a card ("Groom"), or heal 8 HP. For enemies I'm leaning toward a silly premise, maybe something like a dog-wizard tower theme.

First up, a Mouse Squire: HP 8, moves 2, attacks adjacent cells in its facing direction for 4 damage. Then a flying enemy — leaning toward "Moth" — that moves through the air and dives onto all 8 surrounding cells for 3 damage.

Next I'm planning a ranged enemy, "Crossbow Rat" or "Pea-Shooter Pigeon," that fires down its whole facing row up to 5 cells for 4 damage, and a heavy "Pug Guard" with HP 20, move 1, that slams everything within 1 cell (including diagonals) for 7 damage, though I'm wary of adding a separate "guard" mechanic on top.

Renaming the heavy to "Pug Brute" to avoid confusion, I'm sketching a splitting "Hairball Slime" but deciding to skip it for now, and considering a charging "Vroomba" enemy that dashes along its row for 5 damage before settling into floors 3-4. I'm also toying with a "Sneaky Cucumber" enemy with 6 HP that doesn't attack directly but relies on some other gimmick.

For the tier 1 boss, I'm playing with silly dog-wizard names like "Sir Woofington the Wizard Dog" at 90 HP, weighing whether to make it occupy a 2x2 footprint despite the added grid complexity, and leaning toward keeping it single-tile instead.

The boss would teleport between fixed pedestals rather than walk, cycling between attacks like "Bark Bolt" hitting the player's row and "Bone Rain" marking random standing cells for 6 damage each, with the arena laid out as a 15x13 grid across layers.

For phase 2 at low health, I'm thinking of escalating moves like a shockwave hitting the boss's layer and adjacent ones. A key gimmick: since the boss occupies a 2x2 footprint, falling onto its top cells from above deals crush damage, so the arena should include ladders encouraging players to climb and drop onto it for bonus damage.

Working out the vertical layout, I need the boss's pedestals to sit on the ground layer with a gap directly above them on the next floor up, so players standing one layer higher can drop straight through the hole and land on the boss.

I'm sketching a crush damage formula tied to fall distance — something like 3 plus double the number of tiles fallen, so a deeper drop through multiple stacked gaps (say from the top layer through two aligned holes) deals much more damage than a shallow one-tile fall, while a dedicated pounce move gives a flat high-damage option as an alternative to relying on height.

Now I'm thinking through the boss encounter itself — a dog wizard character who stole a special yarn, with the win condition being defeat the boss to unlock the exit door and then reach it. I also need to work out enemy pathing rules: whether walker-type enemies avoid gaps in their patrol routes or risk falling the same way the player can.

For AI, I'm settling on using BFS pathfinding over movement graphs that include falls as valid edges (avoiding damaging falls), ladder climbing, and flying enemies moving freely in four directions. Enemies target the nearest position from which their attack pattern would hit the player, then move toward it up to their speed limit, with intents (attack vs move) recalculated each planning phase based on whether their current position covers the player's cell.

Otherwise the enemy shows a move intent and advances toward its attack position, replanning afterward — meaning an enemy that just attacked will immediately re-plan to attack again if the player remains in range, and attacks include friendly fire, damaging any unit (including other enemies) standing on locked cells except the attacker itself, which should make for some fun chaotic interactions. I want to make sure all damage is telegraphed in advance so the player is never blindsided, except for fall damage.

Enemies act sequentially within the phase with brief animations, and locked target cells stay fixed even if the player dodges away — meaning attacks can whiff if the player moves out of the targeted cell in time, giving space-constrained but meaningful dodging decisions as players balance evasion against advancing through the level.

I'll keep steps at 3 to allow climbing through tight ladder sections, while relying on enemy pattern size (like a Moth's ring of 8 cells) and objectives that sometimes force kills to maintain pressure, plus giving certain enemies aimed attacks for added threat.

For the Pigeon, I'll give it a ranged attack that locks a row segment of 5 cells, though the player can escape by climbing out of that row — passing through a locked cell mid-move is harmless since only the end position matters. For overall balance, I'm setting player HP at 30 with damage per floor scaling around 8-15 depending on carelessness, offset by healing rewards and difficulty options.

I'm also working out the deck mechanics: draw pile, hand, and discard pile, with reshuffling via seeded RNG when the draw pile empties, a hand cap of 10, and end-of-turn discarding the whole hand, plus UI buttons to inspect draw/discard contents.

For objectives, each floor assigns one goal: CLIMB (reach an open exit), CLEAR (defeat all enemies to unseal a rune-sealed exit), HUNT (defeat a crowned Champion enemy with boosted HP to unseal the exit), or the final boss fight against Barkley. I'm planning the floor progression as CLIMB, then HUNT, then CLEAR, then a random pick among the three for floor four, ending with the boss on floor five, with the current objective always displayed on the HUD.

On death, HP reaching zero triggers a Game Over screen with run stats and the option to start fresh — this is permadeath, so a mid-run refresh just loses progress, no resume needed.

Now I'm fleshing out supporting mechanics, starting with weapons: the cat equips a single wand that governs its basic melee and ranged attacks, with different wands like a starting Twig Wand, a Fish Wand, and a Feather Duster offering different damage profiles.

I'm defining the two core attack types — bump-melee against adjacent enemies dealing weapon-based damage, and a once-per-turn directional Shoot action that fires a bolt in a straight line, costing a step rather than mana since mana is reserved for cards.

Different weapons (Twig Wand, Sardine Saber, Yarn Launcher, Laser Wand) vary melee/shoot damage and range, with only one weapon equippable at a time — picking up a new one from chests or shops drops the current one. I'm also starting to sketch out a dodge reaction mechanic for the player.

Thinking more, I want tier 1 to keep a flat roster at base stats across floors, while tier 2's difficulty ramp handles scaling enemy count, HP multipliers, damage bumps on later floors, and a floor-gated roster pool for new enemy types.

For collectibles, I'm settling on "Lost Socks" — two per floor placed on the map — where collecting both grants an extra bonus reward choice at floor end, keeping the HUD limited to health, score, combo counter, and currency.

The sock count itself gets shown on the floor reward/pause screens rather than cluttering the HUD. Other mechanic-specific UI like the hand panel, mana orb, step pips, deck counts, and objective banner I'm treating as separate in-world indicators distinct from the core persistent HUD bar.

Now I'm sketching enemy spawn mechanics — mouseholes that periodically spawn Mouse Squires if conditions allow, with their own destructible HP — and trap tiles like spikes that deal damage when stepped on.

Settling on two trap types: permanent spike tiles dealing repeated damage, and single-use mousetraps that deal a bigger hit and root the unit in place; both affect enemies too, allowing luring strategies. I'm also defining a dash action letting the player move several cells in a straight line for one step cost.

For currency I'm leaning toward a cute item like "Treats," dropped by enemies and chests and spendable in shops. I'm also starting to sketch out key items as unique quest-type objects.

Actually, I want to separate tiers more clearly: equipment are wearable slots with stats, while key items are Metroid-style permanent upgrades found in secret rooms that expand movement abilities, like something granting fall-damage immunity or extended climbing.

Then there's consumables — single-use items like catnip potions or tuna cans for quick effects.

For puzzles, I'm sketching tier concepts like rune-light sequences where stepping on tiles in the right order (shown by a mural hint) unlocks a reward chest, plus push-puzzle mechanics involving yarn balls or boulders.

For secrets, I'm thinking of cracked walls hinted visually that reveal alcoves with loot when damaged, and then shops appearing as dedicated floors between regular dungeon levels.

I'm distinguishing shops (a static vending-style room like "Kitty Kiosk" with fixed prices) from traveling merchants (a wandering NPC like a traveling Rat merchant offering rare items and haggling), and considering the shop as its own screen type for buying cards, consumables, and key items alongside the usual title, pause, settings, and game-over screens.

Since my defined screen list doesn't explicitly include reward or shop screens, I'm deciding to treat these as in-world overlays within the PLAYING state rather than separate top-level screens — so after clearing a floor, three card choices appear as a modal panel over the gameplay view, and shops become an actual room the player walks into within the level itself.

For inventory, I'm thinking the satchel caps consumables at 3 slots, tying the pick-up/drop mechanics directly to that limit.

For defense, I like introducing Fluff as a shield mechanic tied to armor cards like "Puff Up"—it absorbs damage before HP and resets each turn, added as a tier 2 pool addition, maybe even swapping into the starter deck. For items, ground pickups work with E to grab and G to drop from the belt, with weapon pickups automatically swapping out the equipped one.

Now I'm thinking about environmental hazards—puddles that deal damage if you end your turn standing in them, since cats hate water, applying to both players and enemies except maybe fish-type foes.

I'll also add lever switches that toggle doors open/closed to gate off alternate routes, creating puzzle shortcuts, and I'm starting to think through a hint system for stuck players.

For hints, pressing H could toggle a free overlay showing a dotted path toward the current objective (exit or hunt target) along with a short tooltip, plus first-time contextual tips for new mechanics.

For tier 3 extras I'm sketching a throw action: pressing T lets you throw a held item at a cell within range and line of sight, dealing damage on impact.

Throwing deals 3 damage and consumes the item, with specific belt items triggering unique splash effects when thrown—like a milk item leaving a puddle. I'm also defining an equipment system with two slots (Hat and Cloak) that grant stat bonuses, and sketching a flee mechanic letting players retreat through the entry point to escape a fight.

I'm still trying to make Flee feel like a meaningful choice rather than just skipping the floor penalty-free. Maybe it should cost a percentage of current Treats and only be usable under pressure, like when an enemy has an active attack queued against you — something like a "Bail-out Window" that opens on non-boss floors.

Actually, a concrete version: a "Cat Flap" emergency exit spawns at a random wall cell on layers 1-2; using it ends the floor instantly with no reward and a score penalty, which gives flee real teeth. I also want elemental typing — Fire, Frost, Zap on cards with enemy weaknesses and resistances creating damage multipliers — plus brass keys that unlock gold-lock vault doors and get consumed on use, and a sneak toggle that slows movement but keeps unaware enemies from noticing you.

This needs enemy awareness states too: sleeping enemies that wake if you end a turn within a few cells (closer if sneaking), patrolling guards with vision cones, and hideable cardboard boxes that break enemy tracking — all forming a stealth layer for later tiers. Each floor should also have a landmark, like a statue or fish tank, serving as both a navigation aid and maybe a lore or checkpoint trigger.

Settling landmarks as big 3×3 objects that name the floor in a banner and act as a once-per-floor healing shrine. I'm also sketching push/pull cards — one that shoves an adjacent enemy back (dealing damage if they hit something solid or fall), and another that yanks an enemy toward you from a distance.

For transform mechanics, I'm weighing a "Polymorph" card that turns an enemy into a harmless, immobile Rubber Duck for a couple turns versus a self-transform into a stronger Tiger Form with boosted melee and movement.

Actually I like the sillier meme angle better — turning the cat into a "Loaf Form": immobile, takes less damage, and slowly regenerates HP, playing on the classic cat-loaf pose.

I should also flesh out the economy and social layer: a wandering merchant NPC who shows up randomly on early floors offering discounted buys and sells, dialogue-driven NPC interactions with branching choices, and a card-merging mechanic where duplicate cards combine into stronger upgraded versions.

I'm also thinking through meta-progression and moment-to-moment combat feel: local leaderboards with initials, ambush encounters that spawn waves of enemies as survival objectives, and a combo system that rewards chaining damaging actions within a turn with escalating bonuses before resetting.

For item variety I'm sketching dice-based cards with escalating rewards on higher rolls plus animated dice visuals, a gamble option at the merchant, patrol enemies with vision cones that trigger floor-wide alarms, and a light story thread about Mittens climbing the tower to recover stolen Moon Yarn from Archmage Barkley, plus collectible creature companions and merchant selling at half price.

Now I'm expanding the critter system — five catchable species that fill out a codex with medal rewards, plus taming low-HP enemies into allies that fight alongside you for the rest of the floor, cutscenes for intro/boss/ending moments, and an end-of-run ranking system with bonus medals for specific achievements like no fall damage or a pacifist floor.

Actually, decoration should mean decorating a space, not the cat itself. I'll settle on Mittens' "Nap Nook": a title screen scene with four decoration slots, where trinkets unlocked by medals can be clicked into place—purely cosmetic but concrete and small in scope.

Now I'm organizing all 30 mechanics into tiers: Tier 3 "Combat depth" covers damage types, push/pull, throwing, combos, dice rolls, transforms, equipment, and merging; Tier 4 "Stealth & creatures" covers sneaking, guards, hiding spots, keys/locked doors, fleeing, taming, allies, companions, collectible creatures, and waves; Tier 5 "World & story" covers plot, cutscenes, conversations, merchants, selling, and landmarks; Tier 6 "Meta" covers score, high scores, medals/ranks, and decoration. I need to double check placement though—score fits tier 6 but combos belong in tier 3, and the combo counter HUD element should show up there too.

Actually, I'm reconsidering this ordering since score-related HUD elements should probably come earlier, so I'm shifting score, combos, high scores, and medals into Tier 3 to complete the HUD and screens sooner, pushing combat depth mechanics like damage types, push/pull, throwing, dice rolls, transforms, equipment, and merging into Tier 4, then stealth and creature mechanics into Tier 5, and story/world elements plus decoration into Tier 6.

Now I need to nail down concrete numbers for every mechanic, starting with core conventions: a 16×16 pixel grid at a 320×180 logical resolution with integer scaling, grid coordinates with origin top-left, and a turn-based logic model where actions resolve instantly in state while animations play out separately via requestAnimationFrame.

I'm also pinning down the RNG architecture using a seeded mulberry32 generator with separate streams for levels, cards, AI, and loot all derived from the run seed, plus fixed turn counters, integer HP/damage, facing and direction conventions, and deciding on vanilla JS ES modules with no build step.

Now I'm sketching the file layout: canvas rendering with Web Audio and localStorage for persistence, split into modules for boot/loop, context, RNG, input, grid queries, level generation, units, gravity, cards, player movement, and enemy AI.

I'm continuing to lay out the remaining pieces — boss logic, turn flow, objectives, rewards, run/floor structure, procedural pixel-art rendering with effects, audio synthesis, UI screens, a debug API, and a test runner — plus planning tier-2 modules for weapons, items, traps, environment, shops, spawners, and switches.

Now I'm thinking through how to document the sprites: since they're procedurally defined pixel maps with palette letters, I want to give a recipe table listing size, palette indices, and shape descriptions for each sprite, possibly anchoring the style with one full example map like the cat sprite.

I'm sketching a 16x16 wizard-cat sprite with a palette of outline, fur, hat, and eye colors, making sure the palette stays colorblind-safe by relying on an Okabe-Ito-based set so friend/foe distinctions work through brightness and shape, not just hue.

Rounding out the palette with sky blue, bluish green, yellow, orange, vermillion, pink, white, cream, and browns for wood tones, plus a grey, giving 16 colours total alongside transparent. I'm also noting that accessibility settings should include the colour-blind safe palette as default, along with reduced motion and other remapping options.

I'm settling on keeping the palette strictly CB-safe by default with shape/pattern redundancy always on for state-coded colours, rather than adding a separate palette toggle. The settings screen will just cover reduced motion, key remapping, difficulty, and volume sliders as the standard accessibility and audio options.

For pixel-style fonts, I'm weighing whether I can bundle a font file versus needing to rely on an external source like Google Fonts, and considering whether building a lightweight bitmap font from code is more reliable than depending on CSS font-family declarations that assume availability.

Settling on a 5×7 bitmap font with glyphs encoded as 7 rows of 5-bit values, covering ASCII 32–126, which I'll specify for the builder to hand-author. For audio, I'm planning a WebAudio synth using oscillators and noise buffers with envelopes, plus a chiptune sequencer driving separate title, floor, and boss themes along with jingles, and I need to decide how much to prescribe in terms of tempo, key, and chord progressions versus leaving it to the builder.

I'm also defining visual effects like screen shake, particles, and hit flashes, along with reduced-motion fallbacks that disable shake, shrink particle counts, and shorten flashes for photosensitivity safety. Now I'm starting to sketch out the player data structure, covering position, health, mana, steps, and a whiskers special meter.

Adding more player fields, plus generic unit and card data structures...

I'm sketching deck piles for the master list, draw pile, hand, and discard, along with targeting rules—selected cards highlight valid targets, and players can cycle with arrow keys and confirm or cancel. I'm also working through input mapping, deciding how movement keys and card selection keys might overlap with targeting controls.

Now I'm mapping out the full control scheme: movement on WASD/arrows, hand slots on number keys, confirm on Enter/Space, cancel on Escape, and still deciding how to handle end turn and consumable belt keys without clashing with other bindings.

Still mapping keys...

For mouse controls I'm adding click-to-select-card, click-target, End Turn and Pounce buttons, with hover tooltips for enemy intent. When targeting is active, arrows/WASD move the target cursor instead of the cat, confirmed by Enter or click.

Now I'm sketching the turn flow: player start draws cards and refills mana/steps, player act phase runs until End Turn, player end discards hand and triggers end-of-turn effects, then the enemy phase begins.

For the enemy phase, each living enemy executes its intent in order, gravity resolves, deaths are checked, and intents re-plan before advancing to the next turn; I'm also noting the win/loss checks and that floor starts place the player and let enemies plan before the player's first turn. I'm working through movement rules now, covering step costs, melee attacks on occupied cells, facing updates, and ladder/fall interactions.

ClimbUp and climbDown each cost 1 step and require valid ladder positioning, falling happens automatically and for free when unsupported, and support is determined by ground, solid/ladder cells below, standing on a ladder, or another unit beneath — flying units are exempt. I'm defining falling as a cell-by-cell drop until a supported position is reached.

Working through fall damage: landing on another unit crushes it for 3 + 2×d damage while the faller takes nothing, otherwise falls of 4+ cells deal 2×(d−3) damage to the faller, and I'm reconciling this against layer heights where each standing row sits 3 cells below the one above, checking that a one-layer drop equals 3 cells and the damage scales correctly for 2 and 3 layer falls.

Also need to resolve gravity in the right order — bottom-most units first, sorted by descending y — since when a support unit dies, anything above it needs to fall and potentially crush or take damage again.

Now designing Pounce: it's a special tier-1 move fueled by a Whiskers meter that fills by one for each card played and resets each floor. I'm tuning the max threshold (thinking 5) so it's ready roughly every couple turns, triggered with a key press that opens targeting and deals bonus damage when landing above an enemy.

The destination must be within Chebyshev range 3, non-solid, unoccupied, and reachable along a clear line ignoring units since leaping over them is allowed. After landing, normal gravity and fall damage apply, with the pounce bonus (8 damage) only triggering if the cat lands directly above an enemy, stacking with crush damage if it then falls further onto a lower enemy.

So pouncing from height stacks crush damage with the flat bonus, rewarding the cat for leaping from higher up — and crucially, the cat itself never takes fall damage from a Pounce thanks to feline grace. The move costs no steps or mana but drains all five Whiskers meter.

Now I'm turning to locking down the tier-1 card numbers, balancing player damage output against enemy HP pools (Mouse 8, Moth 6, Pigeon 7, Cucumber 10, Pug 18, Boss around 120), and starting to draft the starter deck with cards like Zap for ranged damage and Scamper for movement.

I'm fleshing out the rest of the starter deck — Sparkle Burst for area damage, Lick Wounds for healing, and Laser Pointer to cancel an enemy's next action. I reconsider Laser Pointer's cost since a free action-cancel every couple turns feels too strong at zero mana, so I bump it to 1 mana and sanity-check a typical 3-mana turn's card combinations. Then I start organizing the reward pool by rarity weights, beginning the common tier list with Zap.

Continuing with more card ideas: Moonbeam for column damage, Yowl for intent cancellation, Purrception for mana/draw, Lightning Leap tied to a special move, and Anvil Hex for a heavy single-target hit. I'm now moving into Rare tier starting with Nine Lives, a once-per-floor death-prevention effect.

I'm thinking through how to make Nine Lives not useless after its first trigger -- introducing a "Fade" keyword so the card leaves play until the next floor, which gives it a distinct lifecycle separate from exhaust or discard. Then I'm sketching Comet Cat, a leap attack that deals splash damage to adjacent enemies after landing.

For 17, I scrap a pull-based Gravity Well idea since push/pull feels too high-tier, settling instead on "Catastrophe," a rare Fade card that hits every enemy on the floor for 8 damage. For 18, I land on "Copycat," a simple one-cost rare that duplicates the next card played that turn.

That rounds out 18 cards, with the starter's heal-only Lick Wounds kept separate from the reward pool. Now I'm moving into tier 1 enemies, starting with the Mouse Squire — an 8 HP walker with speed 2 and a "Poke" attack pattern that threatens two cells ahead in its facing direction, armored and wielding a tiny toothpick spear for flavor.

Next up, the Gloom Moth: a 6 HP flier with speed 2 that moves through non-solid tiles in any of four directions, and a "Dust Puff" attack that hits all eight surrounding cells. Then the Pigeon Sniper, a 7 HP walker with speed 1 and a "Pea Shot" pattern that fires up to five cells ahead in a line, stopping at the first solid obstacle or unit — I'm working through how friendly fire and locked-cell resolution should work when the shot passes through multiple units.

The Pigeon Sniper prefers to keep its distance, using BFS to find the nearest position with a clear shot line rather than closing in like other walkers. Next, I'm sketching the Cucumber of Dread — a stationary, tanky unit with high HP and damage that hits its four orthogonal neighbors, meant to sit near ladders as area denial. Finally I'm starting on the Pug Brute, a heavier melee walker.

I'm second-guessing whether varying rosters per floor counts as scope creep versus legitimate content variation, and deciding tier 1 should just use a fixed, hand-authored set of enemies per floor rather than introducing an explicit scaling formula, keeping the ramp implicit in the design rather than a separate mechanic.

For the tier 1 boss, I'm designing Archmage Barkley, a dog wizard occupying a 2×2 space with 100 HP, stationary except for teleports, set in a fixed 15×13 arena. I'm working out his attack pattern cycle—Bark Bolt, Bone Rain, Summon Pups, Big Bark—with phase 2 adding teleports and wider bone rain coverage once he drops below half health, plus how Bark Bolt locks an entire row to force the player to reposition vertically.

Now I'm detailing Bone Rain's column-locking mechanic (player's column plus random extras, expanding in phase 2), Summon Pups spawning mouse squire minions at fixed circles with a population cap, and Big Bark's radius-based area attack around the boss.

For teleport, the boss relocates between fixed pedestals, skipping if the destination is occupied, and falling onto the boss triggers crush damage. I'm sketching the arena dimensions and layering, placing pedestals and the boss's footprint on the ground level to balance the fight's pacing against the boss's HP pool.

I need gaps positioned directly above the boss's columns so the cat can fall from upper layers and crush it, with crush damage scaling by fall distance from each layer. I'm working out the exact pedestal column positions across the three layers to make these crush opportunities consistent.

Now I'm sketching the full arena layout row by row—floors, ladders, the exit location, and how it stays sealed until the boss is defeated, with the player's starting position and summon circle marked in.

I realize width 15 can't center a 2-wide boss symmetrically, so I'll switch to width 16 for all levels, giving 256px with 32px margins on each side at a 320 view.

With W=16, H=13, I place pedestals at columns 2-3, 7-8, and 12-13, which are symmetric around the center at 7.5. I'm sketching the arena layout row by row, placing a single-cell exit door near the top and working out where walls and the exit point go.

I'm placing ladders at x=3 and x=12 connecting layer 3 down to layer 2, with standing rows and floor gaps positioned above the pedestal columns so the cat can drop down to reach each pedestal.

Still mapping out the grid rows...

Row 12 is the solid floor. Checking layer 1's walkable segments against row 9's gaps, I see it splits into isolated sections [0-1], [4-6], [9-11], [14-15], with crossing gaps forcing a fall - ladders at columns 5 and 10 connect up from segments [4-6] and [9-11], while the outer ladders at 0 and 15 connect down to [0-1] and [14-15].

These edge segments don't connect to the middle ones without crossing a gap and falling, making parts unreachable unless Pounce can leap the three-column gap. I'm considering adding layer 0→1 ladders at columns 5 and 10 as well, stacking them with the existing layer 1→2 ladders so each column has one continuous ladder from row 6 to row 11, even though I'd prefer gaps to only be crossed by falling.

Checking pedestal placements at cols 2-3, 7-8, 12-13 against ladder positions to avoid overlaps, then working out row 6's structure for the layer1→2 ladders at x=4 and x=11.

Tracing the fall path from column 7: it drops through the gap at row 6, passes row 8's platform gap, and either crushes against the boss at row 9 (dealing significant damage) or continues to the ground floor for minor fall damage. I'm checking the ladder placements on layer 2-3 at columns 1 and 14, verifying row widths sum to 16, and considering the exit position near (7,2) or (8,2).

Deciding the Moon Door exit sits at (7,2), sealed until the boss dies, and placing summon circles on layer 2's row 5 at columns 3 and 12. For player spawn, I'm weighing options near the ladder and pedestal area, settling on (0,11) to keep distance from the boss's central pedestal at columns 7-8, and laying out the ground row with the boss occupying that center gap. Now I'm sketching the full boss arena grid row by row.

Verifying row 5's column count confirms sixteen tiles total, with pedestal anchors defined at the top-left corner of each 2×2 footprint at columns 2, 7, and 12 on row 10.

Pedestals stay walkable ground when unoccupied, and teleport effects should skip any pedestal the player is standing on. For Bone Rain, I'm defining its danger zone as every non-solid cell in the targeted column, making it a column-wide threat that's dodgeable by shifting one tile over, and I'm considering whether phase 2 should let the boss issue two intents per turn instead of one.

I'm settling on phase 2 (HP at or below 50%) locking two attacks simultaneously with overlapping cells stacking damage, and intent targeting should track the player's current row even if they're mid-climb on a ladder. For balance, Bark Bolt deals 6, Bone Rain 5, and Big Bark 8 against the player's 30 HP, with boss HP at 100 and the player's floor-5 deck dealing roughly 15-20 damage per turn, putting fights around 6-7 turns, which feels reasonable with pups adding distraction.

Now I'm defining floor objectives: Climb simply requires reaching the exit, Hunt requires killing a crowned Champion enemy with boosted stats before the exit unseals, Clear requires wiping all enemies, and Boss requires defeating Archmage Barkley. I'm assigning these per floor (F1 Climb, F2 Hunt, F3 Clear, F4 random pick, F5 Boss), and reaching an unsealed exit triggers a "Floor Complete" reward overlay, except after the boss fight which triggers the win screen.

I'm sketching the reward system: after floors 1-4, players choose between picking one of three weighted-rarity cards, Grooming (removing a card from their deck, with a minimum deck size of 6), or Catnapping (healing 8 HP) before moving to the next floor.

I'm also thinking through difficulty tiers (Kitten, Cat, Lion) that adjust max HP, enemy damage, and boss HP, plus the hand mechanics — drawing 5 cards per turn with a 10-card hand cap, and reshuffling the discard pile into the draw pile when it empties.

Now I'm working out the end-of-turn discard flow, the fade pile mechanic where played Fade cards sit until all piles recombine at floor start, and how unplayable (over-cost) cards get greyed out. For card play, I'm deciding between single-click plays for no-target cards versus a select-then-confirm flow, and settling on showing a preview on first selection with a second press or click to confirm, while targeted cards highlight valid targets and let the player cycle through them with arrows.

On the death side, enemies dying trigger poof particles and cause units above to fall into place, while player death plays a short animation before the game-over screen. For run structure, I'm sketching five floors with four generated normal levels and a boss arena, each with a silly name like "The Scratching Foyer" and "Barkley's Kennel."

I'm adding background color variation per floor and a shown run seed on the game-over screen, plus small shop "landing" floors between tiers 2-3 and 4-5 like a "Treat Kiosk Landing." Estimating total playtime at around 25 minutes across floors and rewards feels reasonable, so now I'm working out generation specifics -- floor strip layouts, row placements for each layer, ground tiles, and how ladders extend across rows.

Writing floor strip patterns...

T9 and T10 strips check out too. Now I'm working out the generation logic: pick random distinct strips for each row with possible horizontal mirroring, then figure out exit placement on row 2 requiring enough distance from ladder columns in row 3, and determine the starting position on row 11 away from ground.

For validation, I need a BFS reachability check over the player's movement graph (walking, falling, climbing) to confirm the exit is reachable from the start, allowing risky falls but still solvable. I'll retry generation up to 100 times before falling back to a guaranteed-valid fixed layout using strip T7 across all three ladder rows, with ladders aligned at the same column so the path is a straightforward climb from start to exit.

For enemy placement, I'm defining candidate cells as standable, non-solid, non-ladder tiles supported underneath, excluding the start/exit, and requiring a minimum Chebyshev distance from the spawn point, capping enemy density per layer and giving special placement rules for flying enemies and the hunter champion on mid-tier layers.

Now I'm working through the AI movement rules: walkers traverse via left/right steps onto open, unoccupied, non-exit tiles, fall when unsupported up to a safe limit of three tiles, and climb ladders vertically, while fliers move freely in four directions ignoring gravity. Goal cells are determined by whether the enemy's attack pattern, oriented toward the player, would reach the player's position, and I'm using BFS with deterministic tie-breaking (left, right, up, down) to pick the nearest path and advance the enemy up to its speed along it.

If no goal is reachable, enemies fall back to greedily minimizing Manhattan distance to the player within their speed, with cucumbers never moving due to zero speed. Since enemies act sequentially, each one's movement updates the occupancy grid for the next, and after moving each enemy turns to face the player's direction.

For the intent display, I'm figuring out how to show small icons above enemies — an attack icon with a damage number, footprints for movement, a question mark for cancelled actions, and sleep icons for idle ones — plus rendering locked/threatened cells with a vermillion hatch pattern and damage numbers that appear on hover.

Now I'm working out the danger calculation: each cell's total danger is the sum of all attack intents that would hit the player there, accounting for special cases like the Pigeon's line attack only hitting the first unit, and displaying this as a dashed telegraph outline with summed damage numbers when overlapping.

For the HUD, I'm laying out the top bar with health hearts and numeric display, plus currency and score for higher tiers, and designing the bottom play tray with mana orbs, step pips, a whisker meter with a pounce button, hand cards, draw/discard pile counts, an end turn button, and an objective banner.

Now I'm thinking through the visual style: 16×16 pixel art tiles and sprites with a larger 32×32 boss, a tower interior background with indigo bricks, starry windows, and bookshelf decor, plus simple two-frame candle flicker animation and a side-on cross-section layout of 16×13 cells bordered by stone walls and parallax night sky.

I'm also sketching out the feedback effects: screen shake amplitudes and durations for different hit types (with a reduced-motion toggle), a white hit-flash on damage, and particle systems for sparks, death poofs, landing dust, and healing sparkles with defined colors, counts, speeds, and lifespans.

For audio I'm planning a sound table plus three music loops (title, floor, boss themes) with victory/game-over jingles, encoding each in a compact notation specifying BPM, key, and note patterns per instrument channel.

Writing melody and drum patterns...

Next I'll move into defining the UX state machine with its states.

So the high scores screen is tied to the high scores mechanic, which only unlocks at tier 3. I should also document a debug API exposed via window.__game, giving access to state inspection and functions for controlling runs, players, enemies, cards, and input simulation, with more functions becoming available as tiers increase.

Tests should be unit-style, running through the debug API in the browser, plus deterministic seed-based tests. Now I'm working out tier 2 specifics, starting with the weapon system: a single weapon slot defining melee and bolt damage/range, beginning with the Twig Wand, and I'm laying out stats for additional weapons like the Sardine Saber.

I'm still fleshing out the weapon roster — Yarn Launcher, Feather Duster, Moon Staff — each with different melee/bolt tradeoffs and special effects like piercing bolts, and thinking through where weapons are found: shop purchases and secret alcoves. Now I'm defining how melee attacks work mechanically, moving into an enemy's cell to trigger an attack, including ladder-based vertical attacks.

Then I'm designing the shoot ability — firing a bolt in a straight direction with a visible projectile animation — and starting on a dash move that lets the player cover multiple cells in one action, costing extra steps but allowing faster traversal.

I'm wrestling with how dash should resolve across gaps: whether it stops at the first blocked cell, always travels a fixed distance, or lands only on supported ground, aiming for something predictable so players can reliably plan jumps over 2-cell gaps.

For Dodge, I'm designing it as a 2-step action granting a single-use token that negates the next incoming attack damage (but not fall/trap/environmental damage), lost if unused by the start of the player's next turn.

Then I'm thinking through an alternative defensive layer: Fluff points that absorb damage from enemies and traps (but not falls or environment), resetting each player turn, gained via cards like Puff Up for 6 Fluff, Cardboard Fort for 12 Fluff, and Hissy Fit which grants 4 Fluff plus some adjacent damage.

I'm also considering giving certain enemies like the Pug Brute a flat Armour stat that reduces incoming damage, keeping it separate from the player's Fluff mechanic to avoid overcomplicating things. Now I'm sketching the Tier 2 difficulty ramp across floors, adjusting enemy count, HP multiplier, damage bonus, and the enemy pool as players progress.

For the final floor, I'm planning boss phase thresholds and capping active minions at 4, plus adding an Elite enemy type with a gold outline, boosted HP and damage, and better treat drops. I'm also designing the Lost Socks collectible system — two per floor placed in varying difficulty of reach, with full collection unlocking a reward overlay offering card choices.

Now I'm moving to spawn points: mouseholes that scale 0/1/1/2 across the first four floors, acting as stationary wall structures with their own HP that periodically spawn Mouse Squires into adjacent free cells if their current spawn count is below a cap.

For traps, I'm defining spike strips that deal fixed damage to any non-flying unit entering the cell and persist indefinitely, plus mousetraps that deal heavier damage, halt movement, and then spring and vanish after triggering once.

For currency, I'm sketching out the treats economy: kill rewards scaled by enemy type, chest and floor-clear bonuses, and how the HUD tracks the total for spending at the shop. I'm also starting to outline key items as rare passive-granting pickups with some inventory limit.

Now I'm drafting five key items — a fall-damage-negating bell, a mana-boosting collar, a melee damage badge, a healing locket, and a pouch that gives starting Whiskers each floor — all displayed in a dedicated strip on the pause screen.

I'm also designing the T2 consumables system: a belt with 3 inventory slots holding items like a healing tuna can, a mana tonic, a step-and-draw milk, an area-damage yarn bomb, and an intent-canceling smoke hairball, usable via hotkeys as free actions and found through chests or drops.

For inventory limits, picking up a fourth consumable prompts the player to drop a slot, with similar swap logic for weapons (1 slot) and key items (capped at 3). Items appear as pickups on cells, requiring an E-key prompt to collect (except for auto-picked treats and socks), and picking up is also a free action costing no steps.

Now I'm working out dropping mechanics and shop pricing — consumables around 15 gold, weapons 45-60, key items 70-90, cards scaled by rarity (25/40/65), and card removal starting at 30 gold with escalating costs per use.

For the shop layout itself, I'm picturing a small fixed room using the same 16×13 frame but with only the bottom layer active: six pedestals holding cards, consumables, and a weapon or key item, plus a removal station and exit door, with no enemies present. Since there's nothing to fight, I'm considering suspending the turn/step system entirely in shops — a free-roam mode where steps don't deplete, possibly extending that rule to any floor without enemies.

I need to be careful with this "Calm" state though: if steps are unlimited but End Turn still works, players could spam heal cards between fights and trivialize HP management. So I'm deciding that in Calm mode, End Turn should be disabled entirely to prevent that heal-loop exploit while still letting steps be unlimited.

For shopping, I'm designing the interaction so walking onto a pedestal shows a prompt with the item and price, and pressing E buys it if the player has enough treats, adding the card to their deck.

For puzzles, I'm sketching two types that appear once per floor on floors 2-4, rewarding a locked Puzzle Chest with treats and a chance at a consumable or key item. One puzzle type involves stepping on three numbered pressure plates in the correct sequence to unlock the chest, with wrong order triggering a reset.

The other puzzle type uses three unlit candles that must all be lit simultaneously by hitting them with damage spells or bolts, treating candles as targetable objects alongside enemies — I'm weighing whether this makes card use feel like a meaningful trade-off between combat and puzzle-solving.

For secrets, I'm thinking of placing cracked-wall alcoves on edge cells of standing rows, with a solid cracked tile hiding a chest behind it, but I need to work out how this fits since standing rows are otherwise open air except for ladders.

I'm reconsidering the grid dimensions, deciding to make columns 0 and 17 permanent outer walls so the interior play space stays 16 wide, giving room to tuck a genuine hidden alcove behind a cracked wall without disrupting normal level geometry.

Treating out-of-bounds as solid means I don't need an explicit ceiling, so rows 0-1 can be open headroom with the exit on row 2, and columns 0/17 stay solid walls except for secrets or the cat flap. I'll keep the 18-wide walled format consistent for both tiers so the geometry lines up, then move on to defining the lever and door mechanics for tier 2.

Levers are standing-cell objects that don't block movement, while gates occupy a cell and block when closed; each floor should have at most one gate pair guarding something meaningful like a chest or ladder route. I need to make sure the validator checks that the lever stays reachable with the gate closed and the exit becomes reachable once it's opened, since a single lever should toggle all gates on that floor.

Levers can't be pressed if a gate cell is occupied, preventing gate-closing on units. For hints, I'm planning an H-key overlay showing a BFS-computed dotted path to the objective, damage numbers on danger tiles, and sparkle cues near secret walls, plus one-time contextual tip toasts for first encounters with ladders, gaps, and telegraphed attacks.

I'm weighing whether tutorial tips belong in tier 1 instead, maybe via a static controls panel in the pause screen, while keeping the full hint toggle system for tier 2. Now I'm sketching environmental hazards like puddles that deal damage to anyone standing in them at the end of a turn phase.

Then I shift to tier 3 scoring design: points for kills (scaled by enemy type), floor completion, collectibles, bonus for damage-free floors, and speed bonuses for finishing under a par turn count.

I'm also figuring out a combo system — a per-turn counter that increments with each damaging action, granting bonus damage once it hits 3+, and awarding a squared score bonus based on combo length when the turn ends.

Beyond that, I'm sketching high score tracking with local storage and initial entry, plus an end-of-run ranking system (S through D) and a set of earnable medals for things like secret collection, no fall damage, and speed runs.

Now I'm designing Tier 4, the Arcane Arsenal: elemental damage types (Zap, Fire, Frost, Plain) with a weakness/resistance matrix against enemies, applying multiplier bonuses for weak/resist hits and considering status effects like Burn from fire damage.

I'm sketching push/pull mechanics—Hiss pushes adjacent enemies away with fall or collision damage, Yarn Lasso pulls enemies toward the player—plus a throw system where pressing a key lets you hurl belt items like a distracting Tuna Can to redirect enemy intent.

I'm also adding other thrown effects (Yarn Bomb explosions, Fizzy Milk puddles, Catnip Tonic dazing nearby foes, Smoke) each dealing flat damage on hit, and designing dice-based cards like Dice Zap plus a shop gamble kiosk with randomized rewards and a pixel-art die roll animation.

Beyond that, I'm sketching equipment slots for hats and cloaks with distinct passive bonuses (damage boosts, range, fluff gain, damage mitigation), and a merge mechanic letting duplicate cards combine into upgraded "+" versions with boosted stats and reduced cost.

For Tier 5, I'm designing a stealth layer: sleeping enemies with wake radii, a sneak toggle mode, sneak-attack bonus damage, plus broader systems for keys/locked doors, taming, allies, and collectible creatures.

A Watchdog enemy patrols with a vision cone and barks to wake the whole floor if it spots the player. Cardboard boxes act as hiding spots that make the player Hidden from enemy AI until they leave or attack, and Brass Keys unlock Locked Doors.

The key leads to a Vault alcove with two rewards and is consumed on use. I'm also adding a Cat Flap escape option that ends the floor immediately with a score penalty, plus Ambush floors where entering a rug-marked zone triggers waves of enemies spawning from mouseholes every couple of enemy phases.

For taming, I'm designing an "Offer Treat" card that converts a weakened enemy into a temporary ally for the floor, with bosses immune. Tamed allies act during the enemy phase targeting nearby foes, and they leave when the floor ends—separate from a persistent Companion slot I'm still working out.

Let me rework the Companion system as "Pocket Critters": collectible creatures like Ladybug, Snail, Firefly, Frog, Goldfish, and Hamster that spawn as rare wandering pickups on floors, get caught by walking into them, and are stored in a Critter Jar collection with a persistent codex for medals. Players equip one as an active Companion from the pause menu, which then follows alongside them.

I'm distinguishing Companions (critters that float freely and give passive or triggered per-turn effects, like Snail boosting Fluff or Frog pulling pickups closer) from Allies (tamed grid-based enemy units). Moving to Tier 6, I'm planning the "Tale of the Tower" layer covering plot, cutscenes, conversations, merchants, and selling mechanics.

The story centers on Mittens' stolen Moon Yarn, taken by Archmage Barkley who wants to play fetch with the moon. I'm sketching skippable cutscenes (intro, boss intro, ending) as pixel-art panels with text, a dialogue system with portraits and branching choices for NPCs like Rattigan the Merchant, Professor Hoot, and Barkley, and merchant appearances on early floors.

Rattigan offers items at a discount and buys back consumables/weapons/equipment for half price, with cards sellable for treats. Each floor also features a unique 2x2 landmark decoration that grants a one-time blessing (healing, stat boost, or map reveal) when admired.

I'm also planning a Nap Nook customization screen with four decoration slots unlocked via medals, persisting across sessions. Checking back through my mechanic list, I've confirmed coverage of weapons, dodging, difficulty scaling, melee, collectibles, spawning, traps, ranged attacks, dashing, currency, key items, consumables, puzzles, secrets, shops, inventory limits, and pricing.

Continuing the audit, I'm cross-referencing throwing, equipment, fleeing, damage types, locked doors, stealth, landmarks, push/pull, transformation, scoring, hiding spots, merchants, dialogue, merging, high scores, enemy waves, combos, dice rolls, plot, selling, guards, collectible creatures, companions, cutscenes, taming, allies, and rank systems against which tier each belongs to.

Since Tier 5 is overloaded with ten mechanics, I'm considering splitting it into a "Stealth" grouping (sneak, guards, hiding spots, locked doors, flee, waves) and separate "Critters" and "Story" tiers for the remaining creature and narrative mechanics.

I'm double-checking tier 1's twelve core items and making sure special cases like "Trapdoor" actually map correctly under falling rather than being miscategorized.

I'm renaming it to "Pothole Hex" to avoid confusion with placed traps, and confirming the Comet Cat leap and friendly fire mechanics stay in tier 1 while armour and currency drops remain tier 2 exclusives. Now I'm checking the HP balance numbers between the player and enemies.

Since enemies telegraph attacks and players get a planning turn before enemies act, skilled play should avoid most hits except when cornered or choosing to trade attacks—that seems fine for a lighthearted game, with Lion mode offering a harder difficulty. I'm working through the turn sequence to confirm enemies mostly move first then threaten, giving players a real chance to dodge based on step range and attack range values like Zap's range 3 or Mouse poke's range 2.

I worry tier-1 difficulty might be too easy since kiting is trivial, so I'm considering ways to add pressure—like Into the Breach's approach where tension comes from multiple enemies and map constraints rather than making attacks undodgeable. I'm wary of any rule that would let enemies land hits without clear telegraphing, since that breaks the fairness of the system; instead I'm leaning toward a "move & strike" intent that still displays the full threatened pattern upfront.

I think the honest answer is keeping telegraphs fully dodgeable, with pressure instead coming from limited mana, a shared step budget tied to climbing progress, wide attack patterns, enemies converging, ladders acting as chokepoints that restrict movement to vertical only, and boss-level row/column attacks. That combination should be enough tension for a lighthearted game, though I'm also weighing whether to tighten the base step count to make climbing feel more urgent.

I'll stick with 3 steps per turn, since Scamper cards can already grant bonus movement. Enemy intents get planned based on the player's position at the end of the enemy phase, so patterns like the Pigeon's locked line or the Moth's ring stay readable and fair if the player repositions in time. I'm settling on 4 enemies per floor at tier one for the grid size, and now I'm thinking through the edge case of walker enemies climbing and stopping on ladder cells.

For pattern blocking I'm treating line attacks like the Mouse's poke as stopping at the first solid cell, while ring patterns like the Moth or Cucumber only count the non-solid cells around them. For the Pug, I'm designing a "Belly Slam" pattern that hits both sides and the row above, moving at speed 1.

The Pug's slam punishes a cat that tries to crush it by standing directly on top, giving nice counterplay. I'm also clarifying support rules — units can stand on other units, and falling onto something with enough drop distance triggers crush damage, while landing on bare ground doesn't. Enemy walkers can path across cells supported by units too, but they're blocked from walking directly into the player's space. Now I'm sketching Barkley's boss details, starting with its 2×2 footprint.

Then I'm converting the arena layout into coordinate space — mapping pedestal anchors, ladder positions, the exit, summon circles, and the player's starting square onto the 18-wide grid with its interior offset.

Building the row-by-row arena strings now, placing walls, the exit marker, and ladder gaps at their correct indices.

Verifying totals for rows 7 through 9...

y9 confirms to 18 columns with hazards placed correctly. Checking y10 and y11 lengths against the 18-column width, including the start marker S in y11, and confirming y12 is the solid floor row—all checks out, so now I move to verifying the floor above in layer 2.

Now I verify the ladder placements connecting layer 1 to layer 2: ladders at x5 and x12 align with layer 1's walkable floor segments [5-7] and [10-12], confirming both ladders are accessible from valid standing positions, while layer 0's ladders sit at x6 and x11.

Checking layer 2's standing row: solid floor spans x1-7 and x10-16 with a gap at x8-9, and ladders at x2 and x15 lead up to layer 3 where the floor is solid everywhere except the ladder columns, giving full walkability and confirming the exit at (8,2). I'm also mapping the pedestal footprints at x3-4, x8-9, and x13-14 across rows 10-11.

Checking that fall continues until it hits the boss at y=9, landing with d=4 giving crush damage of 11, versus the shorter fall from y8 that only deals 5. I'm also noting the summon circles spawn mice that descend via ladders, and starting to map out the boss's phase 1 attack sequence.

For phase 2, I'm pairing up attacks per turn — Bark Bolt with Bone Rain, Teleport with Big Bark, Summon Pups with Bark Bolt, Bone Rain with Big Bark — cycling through these pairs. Teleport resolves first, relocating the boss, then Big Bark centers on the new position, with the telegraph showing the destination pedestal and the resulting attack area ahead of time.

Bark Bolt targets the player's row at the moment the attack is planned, while Bone Rain hits the player's column plus several random interior columns, with more columns affected in phase 2. I'm setting damage values — Bark Bolt deals 6, Bone Rain 5, Big Bark 8 — and defining Big Bark's area as a wide Chebyshev-distance zone around the boss's footprint, large enough to force the player to flee in either direction.

Boss HP is 100 normally (75 for Kitten difficulty, 130 for Lion), with the phase shift triggering at 50% health. On death, all minions die too, the exit door unseals, and the player climbs to the win tile for a victory screen with no additional rewards.

I'm outlining the floor transition sequence: the cat walks through the door, the screen fades out, a reward overlay appears, then the next floor's intro banner displays its name and objective. HP carries over between floors while mana and steps reset, and I'm deciding whether whiskers should also reset to zero each floor.

Now I'm covering accessibility options — reduced motion settings that cut particle counts, disable camera shake, and simplify damage numbers — plus remappable key bindings stored in local storage with a reset-to-defaults option, and I'm about to detail the difficulty settings.

Now I'm sketching out the global context object structure that will hold version info, tier flags, settings, screen state, and separate RNG seeds for different game systems.

I'm also mapping out the run state—seed, floor progress, deck, stats tracking (damage, kills, crushes), and tier-specific fields like treats, score, equipment, and companions—plus the per-floor state including objectives and the grid itself.

Continuing to sketch out floor details like exits, units, turn phases, and hole hazards, then moving into player state: the active unit reference, card piles (draw/hand/discard/fade), turn resources (mana, steps, whiskers), and UI state for card selection and targeting.

Now I'm designing the animation and effects state—queues for move/fall events, particle effects, screen shake, camera tracking, audio, and input handling—before moving into the turn engine logic where actions synchronously mutate state and queue up animation events like unit movement and falling.

I should also account for a debug mode that lets animations run instantly for testing, plus define concrete timing values for each animation type—walks, climbs, falls, card casts, enemy actions—and establish a fixed timestep accumulator for the animation clock.

Now I'm planning the sprite system: everything authored as palette-indexed pixel arrays rendered to cached offscreen canvases, with flipped variants for facing direction and a white hit-flash variant. I'm sketching out the full roster of sprite recipes needed—cat, mouse squire, moth, pigeon, cucumber, pug, boss, and various tile types—along with their frame counts for each animation state.

Drawing the wizard cat pixel grid...

Still mapping out the pixel grid...

Mapping out legs, feet, and tail position, then starting to plot the pixel grid row by row for the hat tip, brim, and ear outlines.

Still plotting pixel rows...

This is getting too detailed for the scale involved—I'm realizing a perfect pixel-by-pixel map might not be worth the effort, and it may be better to give the builder approximate color placement guidance they can refine themselves rather than an exact imperfect grid.

I'll skip the pixel map and instead describe sprite features alongside a style rule list (1px ink outline, max 4 colors per sprite plus ink, consistent light source from upper-left). Then I'm moving into the audio table, listing out SFX entries like UI clicks, card interactions, movement sounds, combat effects, and creature-specific noises.

Rounding out the remaining tiers with sneak/stealth mechanics, taming, merchant interactions, and dialog events, each needing a quick recipe sketch. I also need music cues for title, floor, and boss themes, plus the UX screens starting with a title logo -- trying to land on a fitting game name like "Purrcane Ascent" or something in that playful cat-wizard vein.

Settling on "MEOWGIC TOWER" with hero Mittens the Mildly Magnificent. I'm sketching the title menu options (New Run, Settings, High Scores, decoration room), the pause menu, settings screen with difficulty and accessibility options, and a game-over screen with a lighthearted death message and stats.

Now I'm detailing the win screen, HUD layout, a debug API exposed through a game window object, a per-tier test list, build order, and sanity checks. I'm also nailing down card targeting rules — defining what counts as a valid 'enemy' target (including objects like spawners and cracked walls labeled as foes) and what counts as a valid 'cell' target.

I'm specifying the destination-cell rules for leap-type cards like Comet Cat, using Chebyshev distance measured as the minimum over a unit's footprint cells for 2×2 entities. Then I'm working out the damage application logic, covering dodge/armour checks, hit flashes, floater text, death handling, and the player's nine-lives armor mechanic, before defining how the Pothole Hex card converts a cell into a timed hole.

The hole restores to solid after a two-phase countdown, with delays if a unit occupies the gap cell and restrictions against targeting exits, ladders, outer walls, or the bottom row -- units above it fall immediately, and since restoration is guaranteed, soft-locks aren't possible. I'm also working through a specific boss-arena scenario where a pothole placed above a pedestal lets a unit fall through several empty rows to crush the boss below, then starting to define how the Moonbeam column effect targets enemies within its footprint.

Next I'm working through card definitions: Comet Cat's leap-and-splash damage with crush interactions, Copycat's ability to duplicate the next card's resolution, Featherfall's fall-damage negation with a crush bonus, Lightning Leap's Whiskers boost, and I'm about to detail Purrception.

I'm continuing through utility cards like Purrception, Curiosity, and Zoomies for mana and draw effects, then Yowl's intent-cancelling with boss immunity rules, and finally Catastrophe's board-wide Fade damage and Nine Lives' once-per-floor death prevention that resets HP to 9.

Finishing up Anvil Hex and renaming Big Zap to Thunderpaw, I'm settling on a silly tone for card text and locking in the final rarity tiers: commons, uncommons, and rares across the eight-card set, plus starter-only cards still to be decided.

Reward slots roll rarity weighted 60/30/10 then pick a unique card. Groom removes a card but disables below 6 deck size, Catnap heals 8 capped at max, the boss floor skips rewards, and I'm setting hand overflow at 10 cards with a fade pile counter and Space bound to End Turn.

Now I'm defining calm state: once a floor has no living enemies, phase shifts to calm where steps are unlimited, End Turn disables, and hand/mana persist, with gravity still applying. For the hunt objective, I'm choosing the champion as the enemy on the highest layer, doubling its HP and boosting damage.

Separately, I'm working out the sealed exit's visuals—glowing rune bars that dissolve with particles when unsealed—and deciding that while sealed, the exit cell acts as solid, blocking entry for both player and enemies until cleared.

Then I'm nailing down the start location as an Entry Hatch trapdoor, requiring enemies spawn at least Chebyshev distance 5 away from it, with no turn limit per floor. Victory triggers when the player enters the exit on floor 5 after defeating the boss, and I'm tracking elapsed playtime only while actively playing, not paused.

I'm working out the difficulty scaling table across Kitten/Cat/Lion settings for player HP, enemy damage, enemy HP multiplier, and boss HP, then moving into how tier 2 changes the starter deck and weapon, swapping in Puff Up and adding new cards like Cardboard Fort and Hissy Fit to the pool.

I'm adding the Hairball Volley card that fires the equipped weapon's bolt twice, then defining tier 2 enemy armor mechanics (Pug Brute reduces each hit by 2, minimum 1) and elite armor bonuses, plus treat drop rules. Now I'm sketching out the tier 2 shop layout map using a grid of wall and floor tiles.

Laying out the corridor row with pedestal markers...

I'm thinking through the pedestal contents: cards with rarity rolls, consumables, a 50/50 weapon or key item slot, a Groom station for card removal with scaling cost, and a nap pillow heal option. Since it's a shop with no enemies, I want unlimited movement and I'm considering whether this shop counts as its own level or just an interstitial.

Now I'm defining the inventory limits (3 belt slots, 3 key item slots, 1 weapon) and the chest system — puzzle chests requiring solved puzzles, secret chests tucked in alcoves, and a later vault type, each with their own treat amounts and loot-roll odds for consumables, weapons, or key items. I'm also laying out floor-by-floor distribution: one secret alcove per floor 1-4, puzzles and gated ladders appearing on floors 2-4 with set probabilities.

I'm working through hazard placement — spikes, mousetraps, puddles, and socks — making sure they stay passable so a validator can confirm no blocked paths, and keeping socks/puzzles on reachable cells. Then I move to the paw plate mechanic: three plates scattered across layers that must be stepped on in sequence (1, 2, 3) to unlock a chest, resetting if stepped out of order, followed by starting to design a similar candle-trio puzzle object.

For candles, I'm deciding they sit on cells without blocking movement, but can be targeted by damage effects like Zap, Sparkle Burst, Moonbeam, or Bolt. Once lit, they stay lit through the enemy phase, and lighting all three at once permanently opens the chest. I'm also sketching a secret alcove idea — a cracked outer wall tile that can be broken open with damage.

Cracked walls can also be broken by bumping into them with melee, or hit by area effects like Sparkle Burst and Comet Cat, with spawners, walls, and candles all counting as targetable objects. Breaking one converts it into an alcove revealing a secret chest, and I'm noting it needs a visible crack hint. I'm now moving to the gated ladder mechanic, where a gate blocks the standing cell at the top of a ladder.

The lever to toggle it sits on a nearby lower cell, with reachability validated so the exit and lever are both accessible given either gate state. Gates also block enemy pathing. Next I'm planning hint toasts with ten tips and working out puddle placement, roughly one to three per level.

Mousehole spawner objects occupy a standing cell, have 10 HP, can't be pushed, show a 3-to-1 countdown, and spawn a Mouse Squire into an adjacent free cell when it hits zero—capped at two living spawns, resetting after each spawn, with spawned mice dropping treats and spawners counting toward the clear objective. I'm placing spawners on layers 1-3 away from ladders, and now working out trap placement on supported standing cells away from ladders.

For traps, I'm excluding cells adjacent to start/exit, near ladder tops and bottoms, and near the start, while giving enemy pathfinding a cost penalty for traps and a smaller one for puddles so walkers avoid them naturally. I'm also defining the tier 3 kill-score values for each enemy type and how the combo multiplier scales them.

Beyond kill scoring, I'm laying out the rest of the scoring system: floor completion and par-time bonuses, a no-damage bonus, collectible values for socks, secrets, and puzzles, end-of-run treat bonuses, difficulty multipliers, a win bonus, and a turn-end combo bonus based on the square of the combo count. I'm also starting to define how the combo counter itself increments per damaging action.

Now I'm working out the medal system, which persists in localStorage and includes eight distinct achievements covering things like finding all secrets, collecting all socks, taking no fall damage, crushing enough enemies, finishing quickly, and hitting combo milestones.

I'm also designing the high score system: top 10 entries with initials, score, rank, floor reached, win status, difficulty, date, and seed, with a 3-letter initials entry UI. Then I'm moving into a Tier 4 feature introducing damage types (plain, zap, fire, frost) and mapping existing cards/attacks to these categories.

I'm sketching two new Tier 4 cards — Fireball dealing fire damage with splash to adjacent enemies, and Frostbite dealing frost damage plus a "Chilled" effect that skips the target's next move — along with a third card idea for an area fire effect, then starting a weakness table to define type interactions.

Working through enemy weaknesses and resistances: Mouse Squire weak to zap, Gloom Moth weak to fire but resists zap, Pigeon Sniper weak to frost, and Cucumber weak to fire while resisting frost as a "cool as a cucumber" joke — moving on to figure out the Pug's typing next.

I'm also planning how damage numbers should be color-coded and symbolized by element type, then designing push/pull mechanic cards like Hiss, which shoves an adjacent enemy horizontally and deals collision damage if it hits something, with special rules for ledges and boss immunity.

Now I'm fleshing out Lasso, a pull card that drags a distant enemy along a clear line until adjacent, followed by gravity resolution. I'm also working out the throw mechanic — selecting a belt item, targeting within range via line-of-sight, and defining landing effects like the Tuna Can creating a lure that redirects enemy movement, or the Catnip Tonic stunning nearby units for a turn.

I'm detailing more throwable items: Fizzy Milk spawns damaging puddles, Yarn Bomb deals area damage on impact, and Smoke Hairball cancels enemy intents in a radius. I'm also noting that any unit struck directly takes bonus damage, and thrown weapons leave themselves on the ground to be retrieved, while weighing how Yarn Bomb's existing targeted "use" action in an earlier tier overlaps with this new throw mechanic.

Now I'm sketching out dice-based cards — one that scales damage with a d6 roll, another with mixed outcomes ranging from HP loss to mana and card draw — plus a shop item that gambles treats on a die roll for consumables or new cards.

I also want a transform card, Loaf Form, that restricts movement but halves incoming damage and heals on revert, with a sprite swap to match. Then I'm planning the equipment system with two slots and starting to list Hat options like one that boosts all card damage and another that extends Pounce range.

For the merge rule itself, I'll define that all numeric values on the combined card multiply by 1.5 rounded up, and cards without numeric effects instead get a cost reduction of 1 (minimum 0); merged cards are locked from merging further. I should also account for a shop-based "Merge Bench" option alongside the reward overlay merge.

Now I'm sketching Tier 5 Stealth mechanics: a sneak toggle that limits movement to 2 steps while crouched, sleeping enemies that spawn with 40% probability and show no intent until woken by proximity, damage, or an alarm from a Watchdog, plus a sneak attack bonus that doubles the first hit against a sleeper. I'm also introducing the Watchdog enemy type as part of this alert system.

I'm placing one Watchdog each on floors 3-4. For hiding, I'm adding Cardboard Box objects that make the player Hidden when entered—enemies can't target or see a hidden player, and hiding ends when leaving the box or using an attack card that "pops" it. I still need to figure out whether enemies can walk into occupied box cells.

Now I'm designing Vault rooms (locked doors with Brass Keys the player must find and carry across floors to unlock chests) and a Cat Flap escape mechanism placed in the outer wall of non-boss floors.

Flee lets the player abandon a floor instantly via E-prompt, costing score and rewards but skipping incomplete objectives, except on boss/shop floors. I'm also adding an Ambush Zone on later floors marked by a rug tile that triggers multi-wave combat encounters when stepped on, with enemies spawning from nearby cells.

Each wave consists of two enemies drawn from the floor's pool, with the exit sealed until all three waves are cleared, rewarding a chest afterward. I'm also sketching a taming mechanic where a "Offer Treat" card can convert a low-health enemy into an ally for the floor, tied to a treat currency cost.

Allies act at the start of enemy phase using their own AI but target the nearest enemy, marked with a distinct hatch pattern, and disappear once the floor ends. I'm now designing a companion system tied to a Critter Jar slot, where equipped creatures like the Firefly float beside the cat and act automatically each enemy phase.

I'm sketching out the other critters' passive effects — Ladybug granting fluff, Snail healing at low HP, Frog pulling pickups, Hamster adding movement, and Goldfish boosting card draws — plus how uncaptured critters spawn and wander per floor before being caught by walking into their cell.

Now I'm planning the Critter Codex (persistent via localStorage, shown in the pause menu) and moving into Tier 6/7's story elements: plot summary, floor banners with quips, and the three key cutscenes (intro, boss intro, ending) built from sprite panels with text boxes, skippable via held Escape.

For conversations, I'm designing a bottom dialog box with portrait, name, and typewriter text, plus branching choices for NPCs like Rattigan the merchant, Professor Hoot, and Barkley who taunts at low boss HP. I'm also working out merchant spawn logic — Rattigan appearing on floors 2–4 with scaling chance, guaranteed by floor 4, occupying a non-targetable cell that blocks movement, and offering a Buy/Sell/Bye conversation flow.

Now I'm figuring out the economics: buying items at 0.8x price, selling consumables and equipment back at 50%, and card sell values split by rarity (common 8, uncommon 15, rare 25), with a minimum deck size of 6 enforced when cards are sold. I'm also placing a dedicated Sell Counter pedestal in the shop layout, working around the existing nap pillow fixture.

Then I move on to landmarks: each of the four floors gets a unique 2x2 backdrop object units can walk behind, themed per floor (Yarn Statue, Bookshelf, Vase Pyramid, Telescope), with Professor Hoot perched there offering a once-per-floor "Admire" interaction that heals the player and permanently reveals a hidden sparkle alcove on that floor.

For the title screen, I'm sketching a Nap Nook feature: a 4-slot decoration shelf where medals unlock cosmetic decorations, cycling through options on click and saving to localStorage. I also note the T3 high-scores screen needs to be reachable from the title, and I'm checking medal naming consistency since some T3 medals reference T2 content like the sock drawer and cat burglar themes, making sure each tier builds cleanly on the last.

Each tier should assume all lower tiers are fully built, so I'm planning a config flag like `BUILT_TIER` that tests can check against for each feature. Now I'm moving into the visual art direction — picturing a cozy, chaotic nighttime wizard tower rendered in chunky pixel-art style.

I'm working out the lighting approach: no dynamic lighting engine, just painted static effects like dithered moonlight shafts, flickering sconces, and distinct background tints per floor to build atmosphere cheaply.

Now I'm sketching the spatial layout: a 16×13 interior grid with margins showing the tower exterior against a starry sky, and figuring out the camera scroll math so the player stays roughly centered within the visible playfield once I account for the HUD and tray overlays.

With the camera logic settled, I'm defining the draw order from background sky through walls, tiles, objects, danger overlays, units sorted by depth, particles, and finally targeting cursors. Then I'm starting a recipe table for tile sprites, beginning with the brick pattern for the back wall using an offset-row design with mortar and highlight colors.

Adding more tile recipes...

Now I'm working out the danger overlay styling — translucent vermillion fill with diagonal hatching and a dashed border, plus damage numbers shown selectively to avoid clutter — and starting on the targeting overlay with dotted yellow outlines for valid cells.

Next I'm planning intent icons above units for attack, move, cancel, and sleep states, then moving into card frame design: canvas-drawn pixel art sprites with a mana cost gem, name bar, art box, and type-based color coding.

Now I'm sketching out the character silhouettes and animation sets, starting with Mittens the wizard cat—idle, walk, climb, cast, and fall frames with details like tail flicks, hat sway, and wand sparkles to keep the animations colorblind-safe and readable at small scale.

Continuing on, I'm defining the rest of Mittens' animation set: pounce, hurt, die (a ghost-cat spin-away sequence), and victory, plus tier-specific moves like swipe, dash with afterimages, dodge flips, loafing, and sneak crouches, all mirrored for left/right facing.

Then I move to motion interpolation rules—linear tweening between cells, accelerating falls, and parabolic pounce arcs—before sketching out the other enemy sprites: the Mouse Squire with his toothpick spear and bouncing helmet death, the fluttering Gloom Moth with its sinusoidal bob, and now I'm starting on the Pigeon Sniper with sunglasses and a pea-shooter design.

Continuing through the roster, I'm detailing the Cucumber of Dread's angry wobble and spook jump, the Pug Brute's windup-and-slam attack with shockwave particles, and a simple crown overlay for champion units, before beginning the Archmage Barkley design as a basset/afghan dog hybrid.

I'm sketching helper functions for tone and noise synthesis, including a custom pulse25 waveform for the 25% duty cycle sound, then laying out an SFX table and music tracks with separate lead, harmony, bass, and drum channels before starting to compose a floor theme in C major at 128 BPM.

Now I'm writing out the actual note sequences for lead melody, bass line, and drum pattern across four bars, then moving on to start a new boss theme track.

Now sketching the title theme in F major at a calmer 96 BPM, then outlining jingles: a quick ascending arpeggio for level completion, a longer victory fanfare, a descending pitch-bent "wah-wah" for game over, and starting on a boss phase cue.

For the shop, I'll just reuse the title theme at lower volume rather than composing new music, and set up default mixing levels for music versus tracks. Then I'm laying out the overall HTML structure with the canvas, HUD, tray, overlay, and screen containers, sizing everything through a CSS scale variable, and starting to define the state machine table that governs screen transitions.

Next I need to spec out the HUD and tray tables, the debug API, the test suite per tier, the build order, definition-of-done checklists, and sanity checks, while keeping engineering conventions firm: no external assets, everything procedural, plain ES modules with no bundler, deterministic logic separated from DOM/canvas code, and a single shared mutable context object passed through all functions.

I also need an event bus so logic emits events that audio and fx subscribe to, and I'm listing out the full event vocabulary covering cards, movement, combat, turns, objectives, floor progression, rewards, and boss/run outcomes for later tiers.

The presentation layer should build tweens from these events in order, with an animation-busy flag blocking input except pause, while the underlying logic stays synchronous so tests run instantly. I'm also pinning down core conventions: player is unit id 1 with enemies starting at 2, a 16px logical cell grid on a 320×180 screen scaled by integer factors, time tracked in ms for animation and turns for gameplay, speeds in cells per action, and Chebyshev-distance ranges except where noted like Moonbeam's column or Bolt's straight line, with damage and HP kept as integers.

Now I'm locking in frame timing at a fixed 60Hz step, screen axes with x-right/y-down and facing as ±1, and palette-indexed colors. For RNG I'm specifying mulberry32 with seeded streams derived per name, accessed through context-specific generators rather than Math.random, with a strict logic/presentation split, integer math with ceil for HP scaling and floor-with-minimum-1 for damage multipliers, and single-unit cell occupancy except for multi-cell bosses.

I'm also listing persistence keys for settings, keys, highscores, medals, tips, codex, and nook, tier gating through a config constant, text rendering exclusively through PixelText, and keeping the DOM out of logic modules — then moving into outlining the global context shape, per-module function signatures, and gameplay documentation with rosters and tables.

This document is going to be long, so I need to be thorough yet efficient, working through exit placement rules for generated floors and other remaining specifics methodically.

I'm figuring out the start position logic—picking between the two far corners based on which is farther from the exit, plus how ground and ladder rows get placed. I'm also working out how strip definitions translate into solid, air, and ladder tiles across floor rows.

Now I'm sketching the movement validator for the player: treating non-solid, supported cells as nodes, with edges for walking left/right (falling to a landing spot if unsupported) and climbing ladders upward when the cell above is open.

For enemy placement, I'm deciding candidate cells based on type — walkers and cucumbers need supported, reachable floor tiles at least a Chebyshev distance of 5 from the start, while flying moths can go anywhere in open air within range.

I'm also limiting enemy density per layer, picking a champion target by lowest height, and ensuring every enemy stays killable within spell range for the clear objective, with walkers tolerating falls up to 3 tiles.

For enemy AI, goals are reachable cells where facing toward the player hits them; I'll run a small BFS across the grid, move units step by step respecting speed and fall rules, and fall back to a greedy nearest-cell choice if no direct path exists. The pigeon type should also avoid getting too close, excluding goal cells near the player.

Cucumbers never move and just attack when adjacent, while moths use simple 4-directional BFS across open cells. For timing, each enemy's intent is planned at floor start and then re-planned after its own action during the enemy phase, using the player's current position since the player doesn't move mid-phase.

An edge case: if a player stands on a unit that moves away, the player could fall unexpectedly, leaving other enemies' already-locked intents stale, but that's acceptable since locked cells stay locked. For attack execution, I'm resolving each locked cell by damaging units there (except the attacker), with pigeons only hitting the first unit in their line, and misses occurring if the player has already moved — animations still play regardless of hit or miss.

Now I'm thinking through crush damage from falls: if an enemy walks off a ledge directly onto the player during enemy phase, that's an un-telegraphed surprise hit, which breaks the telegraphing rule, so walkers should never choose a fall that would land on a unit. But crushes caused by the player's own actions — like killing an enemy that another enemy was standing on, causing the upper one to fall — should be allowed since it's the player's doing, even though it's rare for the player to end up underneath.

I'm also working out that players falling onto enemies deals crush damage (including bosses), steps and mana don't carry between turns, max hand size is 10, and I'm detailing how calm mode works: once the last enemy dies during the player's turn, remaining steps become unlimited, the hand stays as is, End Turn gets hidden, and new enemy spawns would end calm mode and resume a normal turn.

Now I'm defining objective completion conditions—CLIMB unseals the exit immediately, HUNT unseals on champion death, CLEAR on last enemy death, BOSS on boss death—and sketching the floor outro sequence (player walks through the door, stats tally, reward overlay) plus game-over stats like floor reached and cards played.

I'm working out the card tray layout: card dimensions, hand overlap spacing when more than a few cards are held, tray peek height versus hovered/raised height, and fitting the mana/steps/Whiskers cluster on the left and draw/discard/End Turn cluster on the right within the 320px width budget.

Now I'm designing the HUD bar: HP heart icon and bar, currency counter, a separate objective banner below showing floor and goal text, and combo/score readouts on the right. I'm also calculating the pixel font grid (6px per character, 8px line height) to figure out how many characters fit per line on the HUD and on individual cards.

Since cards are too narrow for the big font, I'm splitting into two bitmap fonts -- a 5×7 "Big" font for UI text and a smaller 3×5 "Tiny" font for card text and numbers, checking that legibility holds at the render scale. I'm also sketching how a hovered card should animate, rising and scaling up slightly in the tray.

For reduced-motion mode, I'll skip the scale transition and snap instantly instead. I'm also planning the remappable keybindings table with action defaults, and a Deck view overlay (toggled with V) that shows the sorted draw pile and discard during play.

Now I'm sketching the debug API object exposed on window, covering meta functions like snapshotting state, stepping animations, starting new runs, and loading custom floor layouts, plus the start of an input section.

Still writing debug API methods...

I'm settling on giving each gameplay system one primary accessor function that reaches its state directly, rather than scattering many individual functions per system.

For testing, I'm planning a lightweight harness that runs each test using the game API in instant mode with fixed seeds, organized by tier with IDs like T1-01. I also want to double-check numbers like enemy speed relative to player kiting, and work out how boss-summoned mice spawn on circles and path to ladders to reach the player.

I'm also mapping out boss mechanics: the boss stays anchored and never falls, units can stand on it as support, and pounces onto it count as enemy contact. I'm computing the boss's area attack cells using a Chebyshev distance of 3 from its footprint, and working out which rows count as valid target cells for its bolt attack based on player position.

Damage from the boss's own attacks doesn't hurt it, but friendly fire does hit minions caught in the blast. Crossing the 50% HP threshold triggers a phase change with its own sound cue and shifts the boss into its phase-two attack sequence, while the boss itself acts last among enemies each turn. I'm also capping minion summons at four alive, spawning up to two new mice on free tiles when below that cap.

Checking the treat economy across early floors, the totals land around 95 treats before the first shop (enough for a rare card plus a consumable) and roughly 120 more before the second shop, which feels balanced. For tier 2, the run starts with the Twig Wand, no treats, an empty belt, and the starter deck including the Puff Up swap, with treats tracked in the HUD. Now I'm starting to list out the hint tips for tier 2 along with their triggers.

Continuing through the tip list: puddles hurt on turn end, levers open gates with E, and running out of steps prompts Scamper or ending turn. I'm also working through how the Calm tier gives infinite steps, and nailing down the modifier order for T3's +2 combo damage bonus — confirming it applies to all player-caused damage including crush, stacking after equipment bonuses but before damage-type multipliers.

I'm laying out the full damage pipeline: incoming enemy damage gets difficulty/ramp/elite modifiers, then T4 Loaf halving, then Dodge negation, then Fluff absorption, before hitting HP, with Nine Lives triggering at zero. Then I run through a checklist confirming core systems are covered — climbing, falling, and the Barkley boss fight all check out.

Continuing the checklist, I confirm rewards, deck building, objectives, hand management, draw/discard, cards, enemies, health, and abilities including Pounce and special cards like Comet Cat are all accounted for. Then I sketch the session flow from title screen through a five-floor run to win/lose and back to title, and plan out the documentation structure: a requirements-to-section mapping table, a decisions table with my rulings and reasoning, a tier list of mechanics, floor naming and background variants, and finally the tuning file contents.

I'm now working through camera math for the 320×180 logical canvas, figuring out the HUD and tray dimensions, the world viewport area, and how to compute the vertical camera offset so it clamps correctly against level bounds given the player's row position.

I'm verifying edge cases like the shop room's camera clamping at the bottom and drawing sky when the level area runs out, plus handling reduced-motion camera snapping and cursor-following behavior for off-screen targets. I'm also working out the mouse-to-world coordinate conversion formula before moving on to building the visual recipe table with palette colors.

Now I'm defining the full 17-color palette with hex values for ink, night, brick, lilac, blue, sky, teal, yellow, orange, and the rest, then setting up colour-blind-safe semantic pairings—danger uses vermillion with hatching, safe moves use sky with dots, valid targets use yellow with dotted outlines, and elites get distinguishing outline treatments.

I'm also deciding how enemies vs allies read visually beyond colour alone (intent icons vs heart icons), designing card frame styles by type (spell, trick), and working out HP bar fill colour and behavior for low health states with a reduced-motion fallback. Then I'm specifying mana star styling for spent vs available states, paw-print step indicators, and the five-segment whisker meter that glows and labels "POUNCE!" when full.

Now I'm defining motion rules for enemies -- tween speeds for movement, flier bobbing, attack windup and lunge timing, and projectile travel speed -- plus facing/mirroring rules for all units including the boss. I'm also working out the player's cast animation, including wand raise timing and the visual effects for different spells like a segmented lightning zap.

Still detailing spell visuals... each with its own particle motion and timing. I'm also defining the particle data structure with position, velocity, life, color, size, and gravity, and starting an audio recipe table with helper functions for generating sound blips.

Writing SFX table entries...

Adding more sound definitions...

Still defining more sound effects...

Still filling out the sound effects table...

Now I'm moving into the UX state machine, mapping out the screen flow starting with BOOT building sprites and waiting for a first gesture before transitioning to TITLE, then sketching TITLE's menu options.

I'm continuing through the remaining states: PLAYING, PAUSED with its submenu, SETTINGS as a shared screen reachable from either origin, GAME_OVER and WIN with their stats and options, HIGH_SCORES for T3, and a T7 CUTSCENE overlay state for the intro, boss reveal, and ending sequences — settling on treating cutscenes as a state overlay rather than a separate top-level screen.

Nap Nook belongs inside the TITLE screen as a panel rather than its own screen. Overlays like rewards, deck view, belt-full prompts, confirm-flee, dialog, and shop prompts all appear during PLAYING without being separate screens, and I'm now mapping out the HUD elements — HP bar, treats counter, combo display, and score — along with their visibility conditions and tier requirements.

The play tray needs an objective banner, mana, steps, a whiskers/pounce button, hand display, draw/discard/fade counts, end turn button, and floor/turn label, plus belt slots and item icons at tier 2. For fluff (armour) and dodge tokens, I'm deciding to show fluff as a lilac shield badge attached to the HP element since it's health-related, with dodge shown as an in-world swirl icon near the cat. Now I'm starting to go module by module, beginning with the config file's core constants.

