# 0. CONCEPT

The first playable game is one hand-built library floor: a side-on grid room with floor tiles, floating stairs, a locked door at top right, and a bell above it. Pip, a wizard cat, starts bottom left. The player does one thing: pick a card from the bottom hand; the card moves Pip, attacks a nearby target, then ends the turn. Drawn cards come from a face-down pile bottom left and go to discard bottom right. Three things act on their own: Book Guards patrol and hit adjacent tiles, Soup Pots drip steam damaging occupants, and the Bell Door stays shut until Pip touches a Feather Key token on a shelf. Card kinds are Move cards (Dash, Climb), Attack cards (Wand-Sword, Crossbow), and Item cards (Feather Key, Heal). HUD top shows health, currency, score, combo.

# 1. DECISIONS

Game prompt: roguelike deckbuilder where you're a wizard cat climbing a tower
dimension: 2d
camera: side-on
time model: turn-based
movement model: grid-based
session shape: a sequence of levels
failure: permadeath, start a new run
tone: silly
size: a handful of levels, under 30 minutes
win/lose: reach the exit, defeat a final boss
core mechanics: player health, cards, enemies, jump, climb, hand, draw / discard, objectives, abilities / special moves, deck building, falling, bosses
supporting mechanics: rewards, dodge, weapons, collectibles, melee attack, difficulty ramp, traps, spawn points, shoot, key items, currency, dash, environmental damage, puzzle types, secrets, inventory limit, armour / defence, consumables, switches and doors, shops, prices
extra mechanics: hints, damage types, throw, transform, spell words, keys and locked doors, score, equipment, flee, landmarks, merchants, hiding spots, conversations, sneak, push and pull, merge, high scores, combos, roll dice, plot, waves, selling, collectible creatures, guards, cutscenes, companions, taming, allies, medals / ranks, decoration
art style: pixel art: low-resolution sprites with visible square pixels and a limited palette
palette: saturated: bright, strong colours
typography: pixel font: blocky bitmap letters
music: chiptune: retro console bleeps
sound effects style: retro bleeps: synthesized chip sounds
screens: title, pause, settings, game over, win, high scores
hud: health, score, combo counter, currency
effects: screen shake, particles, hit flash
accessibility: colour-blind safe palette, reduced motion, remappable keys, difficulty options

# 2. HOW IT IS BUILT


Build it as a crappy framework first: a fixed grid, a square player, square enemies, rectangular cards, a face-down pile, a discard pile, a locked exit square, and a top HUD bar, with no art, no names, and no text. Make it play by moving the square, hitting squares, drawing and discarding rectangles, and reaching the exit. Then replace each placeholder with the concept’s thing one at a time: the player square becomes Pip, enemy squares become Book Guards, hazard squares become Soup Pots, the exit becomes the Bell Door, cards become Move, Attack, and Item cards, and the square key becomes the Feather Key token. Only then add the pixel sprites, chiptune bleeps, and HUD labels. A turn-based grid deckbuilder is a fixed grid, a player token, enemy tokens, hazard tokens, a card hand, a draw pile, a discard pile, and a locked exit; nothing in the concept changes what a turn-based grid deckbuilder is.

# 3. THE GAME WE WANT

## Story
A user asked for a browser game: roguelike deckbuilder where you're a wizard cat climbing a tower. You are Pip, a scruffy wizard cat whose hat is a stolen tea cosy. The Tower of Whiskerfall is a sideways puzzle palace of books, cauldrons, and floating stairs, and its exit is the rooftop bell that can wake the sleeping spell words. The obvious alternative—taking the magical lift, asking a human for help, or simply napping until the problem solves itself—is not open to you because the lift was eaten by the final boss, humans cannot see the tower unless a cat rings the bell, and every nap makes the boss one card stronger. If you fail, the tower’s magic is sold to a merchant guild, cats become ordinary cats, and the world loses its silly enchantment. Your player health is nine lives, but it is a single fragile bar; when it empties, permadeath starts a new run. You climb with cards, hand, draw / discard, objectives, abilities / special moves, deck building, jump, climb, falling, enemies, and bosses, and every run tells the same plot in a fresh, ridiculous way.

## World
The world is a side-on, 2D, turn-based, grid-based tower divided into a sequence of levels. Each floor is a room: a library of sneezing books, a kitchen of levitating soup, a clockwork attic, a greenhouse of meowing plants, and a rooftop arena. When the player does nothing, the tower still lives: guards patrol in loops, merchants haggle with themselves, collectible creatures hide in hiding spots, traps reset after three turns, switches and doors click, and shops restock at prices that change if you roll dice. The player can act on nearly everything. Move, dash, jump, climb, or sneak past enemies; melee attack with a wand-sword; shoot with a crossbow; throw pots, books, or fish; push and pull crates to create cover or block falling debris; open keys and locked doors; use key items such as a squeaky rune, a feather key, or a yarn compass. Environmental damage from steam, spikes, magic ink, and crumbling ledges can hurt you or enemies. Armour / defence, consumables, equipment, and weapons alter your hand and stats, but the inventory limit forces choices. The tone is silly: hit flash, particles, screen shake, chiptune music, retro bleeps, pixel font, and pixel art: low-resolution sprites with visible square pixels and a limited palette. The palette is saturated, with bright, strong colours. Accessibility options include colour-blind safe palette, reduced motion, remappable keys, difficulty options, and hints that appear when a puzzle type is unclear.

## Content
The game contains a handful of levels under 30 minutes, but each session differs. Spawn points, enemies, traps, shops, landmarks, secrets, and rewards are arranged differently, while the difficulty ramp ensures later floors use tighter rooms, more waves, and nastier bosses. There are puzzle types: switch puzzles, push and pull blocks, falling platforms, timed doors, and hidden conversations that reveal plot hints. There are combat encounters: enemies with damage types, guards with shields, merchants who may flee, and final bosses with phases. There are collectibles: spell words, key items, collectible creatures, currency, decoration, and high-score tokens. You can make things by merging duplicate cards or items into better ones. You can sell unwanted loot to merchants or shops, and the game makes selling itself absurd: prices are ridiculous and sometimes require a conversation to unlock. Taming collectible creatures into companions or allies lets them follow you, scout hiding spots, and occasionally add special moves. You can transform using spell words into a mist cat, a fish cat, or a thunder cat, changing how you move and fight. You can use abilities / special moves, dodge, flee, roll dice, and combine cards into combos. Deck building happens after each level through rewards: add, remove, upgrade, or merge cards. Across sessions, the player unlocks new cards, decorations, plot fragments, medals / ranks, and a high scores list, while the run itself remains permadeath.

## A Session
You open the title screen, choose settings, difficulty options, remappable keys, reduced motion, and start. The pause screen lets you read objectives, view your deck, and quit. The run begins at a spawn point with a small starter deck, low currency, and a hint about the exit. Each turn, you draw cards into your hand, manage the draw / discard pile, and decide whether to explore, fight, shop, sneak, dash, climb, jump, or set an objective. The HUD shows player health, score, combo counter, and currency. Early rooms teach jump, melee attack, shoot, throw, and push and pull. A shop offers equipment, consumables, armour / defence, and prices; a merchant may offer a rare card if you complete a silly conversation. Secrets hide in bookcases, behind switches and doors, or in hiding spots, and they can grant key items, spell words, or a collectible creature to tame. Combat uses cards: one card may move, another jump, another shoot, another dash, another transform, another heal, and another turn a trap against enemies. If you chain cards, the combo counter rises, particles fly, and the score climbs. If you make a mistake, screen shake, hit flash, environmental damage, or a boss attack can drain health. At the end of a level, you receive rewards, choose new cards, and deck build. Final boss fight uses waves of minions, then the boss: a giant cat-shaped vacuum called the Archmeow of the Upper Shelf, who eats cards and creates falling platforms. If you reach the exit and defeat the final boss, the win screen shows high scores, medals / ranks, and a cutscene where the rooftop bell wakes the spell words. If health reaches zero, the game over screen shows permadeath, your run’s score, and a new run button.

## Resolution
The whole game ends when the wizard cat reaches the top of the tower, rings the bell, and defeats the final boss. The tower opens, the spell words return, and the silly world is restored: books sneeze happily, cats remember magic, merchants close their absurd shops, and the final boss is shrunk into a yarn ball. The player is left with a completed plot, unlocked cards, decorations, collectible creatures, high scores, and medals / ranks. They can start another run, because the roguelike deckbuilder promises a new tower, new enemies, new shops, new traps, new bosses, and new ways to climb.
