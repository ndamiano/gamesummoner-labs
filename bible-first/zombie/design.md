# 0. CONCEPT

Bloomwick Churchyard is one hand-built graveyard corner with two candy roofs, a hedge, a well, and a low fence. First-person Gulp appears at a spawn point; the screen shows a crosshair center, minimap top-left, score top-right, combo bottom-center. Four movers act on their own: two townsfolk (a baker, a guard) walk preset paths and run home when hit, and two animals (a chicken, a duckling) peck near the well and flee when approached. Two targets sit against the fence: a crate and a barrel. The player only presses melee: a bonk makes a target or mover recoil, makes movers run, and raises the combo counter; the only result is a silly reaction chain and a score bump.

# 1. DECISIONS

Game prompt: zombie game but you're the zombie lol
dimension: 3d
camera: first-person
time model: real-time
movement model: free movement
session shape: open world
failure: no failure
tone: silly
size: many levels, a few hours
win/lose: none
core mechanics: map / world, jump, melee attack, falling
supporting mechanics: abilities / special moves, chase and catch, pick up and drop, spawn points, climb, physics objects, landmarks, unlocks, dash, dodge, collectibles, noise, detection, throw, hiding spots, secrets, switches and doors, townsfolk, push and pull, swim
extra mechanics: rewards, hints, carry and tow, guards, transform, boosts, conversations, score, experience and levels, decoration, day / night, keys and locked doors, grapple and swing, quest givers, side quests, fast travel, lore, herd and lead, collectible creatures, skill tree, companions
art style: stylized / toon: soft shapes, bright colours, cartoon proportions
palette: saturated: bright, strong colours
lighting: daylight: bright, even sun
typography: hand-lettered: drawn, irregular letters
music: chiptune: retro console bleeps
sound effects style: retro bleeps: synthesized chip sounds
screens: title, pause, settings
hud: score, minimap, combo counter
effects: particles, hit flash, trails
accessibility: colour-blind safe palette, reduced motion, remappable keys

# 2. HOW IT IS BUILT


Build a crappy 3D first-person framework with a gray box place, a capsule player, four moving boxes with wander/hit-flee stubs, two gray target boxes, a number counter, and placeholder title/pause/settings screens until it moves, hits, and counts; then the UI: replace the gray box place with the hand-built churchyard, the capsule with Gulp, the moving boxes with the townsfolk and animals, the target boxes with the crate and barrel, the number with score/combo, and the placeholder screens with hand-lettered title/pause/settings. These replacements only swap placeholders; they never add a rule, system, or screen the framework lacked. A first-person sandbox is 1 place, 1 player, 4 movers, 2 targets, 1 melee action, 1 counter, and 1 menu shell; nothing in the concept changes what a first-person sandbox is.

# 3. THE GAME WE WANT

## Story
This is a zombie game but you're the zombie lol, and that is the whole joke: you are Gulp, a freshly risen, brightly coloured zombie with mismatched buttons for eyes, waking up in the sunny churchyard of Bloomwick. You are not the monster a human hero is supposed to defeat; you are the only available hero, because the town's old adventurer has retired, the quest board still says “save the valley from the zombie menace,” and the valley already has one zombie on it. The obvious alternative is not open to you: you cannot be the brave townsfolk, because your arms are comically stiff, your heart is a decorative turnip, and the protective hats only fit people with hair. You are stuck being the zombie, and the game asks you to do the heroic thing anyway. The story answers why this is happening: Bloomwick's fear machine has been running on bad rumors, and the only way to quiet it is for the feared zombie to become helpful, silly, and impossible to misunderstand. What is at stake is not death, because there is no failure, but belonging. If you never learn to help, the townsfolk keep running, their doors stay locked, your lost companion Nibbles the duckling stays missing, and the valley loops in frightened screaming. If you do help, fear becomes curiosity, and the world opens.

## World
Bloomwick is a bright, stylized, toon-colored 3D open world with soft shapes and cartoon proportions, seen in first-person: saturated, strong colours, meadows, candy rooftops, a pumpkin patch, a windmill, a lighthouse, a river, sewers, and caves. The map / world is learned by walking it, with landmarks that teach you where you are. It runs in real time under a bright, even sun. Townsfolk bake bread, chase chickens, gossip at the well, guard bridges, decorate porches, and follow schedules that change from day / night. If you do nothing, they live anyway. You can act on them: a silly melee attack bonks crates, hats, and physics objects without hurting anyone; conversations with quest givers give hints, side quests, and lore; a chase and catch retrieves a runaway sheep; a throw knocks a switch far away; a push and pull moves a cart; a carry and tow brings a broken friend to safety. You can jump, climb, swim, dash, dodge, grapple and swing, pick up and drop, herd and lead, and use noise and detection to decide whether to sneak through hiding spots or announce yourself with a squeaky boot. Falling is part of the fun: you can drop from ledges, bounce into ponds, and land in a pile of soft particles. Switches and doors, keys and locked doors, spawn points, fast travel, and landmarks make the world navigable. Guards are not executioners; they are easily startled, easily bribed with cake, and easily distracted by a rolling barrel. You can transform into silly forms, gain boosts, decorate a home, and unlock new paths. The palette is colour-blind safe, motion effects can be reduced, and controls are remappable.

## Content
The content is designed to make many levels and a few hours feel like one living place. Places differ by movement and mood: rooftops reward grapple and swing; sewers reward swim and dodge; pumpkin fields reward herd and lead; windmill interiors reward switches and doors; caves hide collectible creatures and lore tablets; town streets reward conversations and detection. People differ by play: quest givers ask for help, guards patrol with noise and sight, townsfolk react to your actions, companions follow after you earn trust, and collectible creatures scurry, flap, or waddle away, rewarding chase and catch without punishing failure. Things to take, make, fight, or find differ by verb: you can take hats and collectibles, make small silly machines from physics objects, fight playfully by bonking scarecrows and chasing chickens, and find keys, hints, lore, and hidden creatures; physics objects can be pushed, thrown, stacked, or dropped; collectibles, keys, locked doors, switches, hints, and rewards include score, experience and levels, decoration, and new abilities and special moves. Side quests include finding lost sheep, decorating the graveyard, rescuing a cat from a roof, calming a scarecrow mob, and helping a guard understand that you are the zombie lol. Each session differs because spawn points, town schedules, day / night, hidden hints, and random collectible creatures shift what is possible. Across sessions the player grows through a skill tree, unlocks fast travel, earns decoration, recruits companions, gains boosts, and transforms, while the world remembers kindness: shops stay open, guards stop patrolling, and hidden paths appear.

## A Session
You begin at the title screen, hand-lettered and bright, with pause and settings available before play; you adjust reduced motion, remappable keys, and the colour-blind safe palette, then step into first-person Bloomwick. The HUD shows score, a minimap, and a combo counter that only rewards silly chains, not violence. A quest giver points you toward the lost sheep, and the session becomes a loop of deciding, moving, and reacting. You run with free movement, jump over fences, climb a wall, use grapple and swing across a gap, and fall into a pond with retro console bleeps and a splash particle; you swim to a bank, drop a muddy crate, pick up a key, and push a cart to a switch. A guard hears your noise, so you hide in a hedge, then use a throw to knock a barrel away and sneak past. You herd the sheep through a gate, tow the stubborn one, and catch the last one with a chase and catch that ends in a hit flash, brief trails, and a chiptune fanfare. You return to the quest giver, receive rewards and hints, decorate a corner of your home, and unlock a fast-travel point. If you succeed, the town cheers and opens a new path. If your attempt fails to catch the sheep, it hides, the guard laughs, and you can try again; there is no game over. The last screen is your own pause menu, not a defeat card; the world continues without punishing you.

## Resolution
The whole game ends softly, because there is no win or lose to force. After enough kind quests, the player learns that Bloomwick's fear was never aimed at them personally; it was aimed at loneliness. The final major quest gathers companions, guards, quest givers, townsfolk, and collectible creatures for a “Not Scary” festival, where the player is introduced not as a threat but as the valley's newest helper. The resolution is not a victory screen but a permanent change in tone: the town's music becomes a shared chiptune melody, doors stay unlocked, and the player can decorate a home, explore every hidden area, finish the skill tree, and keep discovering lore. The player is left with an open world that no longer fears them, a roster of silly companions, a decorated sanctuary, and a clear emotional joke: in a zombie game but you're the zombie lol, the scariest thing was never the zombie; it was being misunderstood. The game can be left, paused, or continued forever, because its promise is not ending, but belonging.
