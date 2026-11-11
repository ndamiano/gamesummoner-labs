# 0. CONCEPT

A first playable game is one hand-built side-on bakery: street window and register left, display case center, ovens and flour sacks right, moon gate far right, sunrise timer top. The player is a tiny ghost floating freely. A sleepy customer enters left, browses, leaves; a suspicious customer sees farther and raises detection; a baker guard patrols ovens to register and chases. The player's one verb is scare: fly close and press. It makes a sleepy customer drop a cream puff or croissant, makes a suspicious customer alert guards, and makes guards chase; touching a dropped pastry scores. Hiding in a flour sack, display case, or cold oven lowers detection. If detection fills or a guard catches you, you lose a life and respawn; reaching the moon gate ends the night.

# 1. DECISIONS

Game prompt: a game where you're a tiny ghost haunting a bakery at night, scaring customers to steal pastries before sunrise
dimension: 2d
camera: side-on
time model: real-time
movement model: free movement
session shape: single screen
failure: lose a life
tone: silly
size: one screen, a few minutes
win/lose: survive as long as possible, reach the exit, beat a score
core mechanics: sneak, score, detection, hiding spots, fly, enemies, dodge, flee, abilities / special moves, objectives
supporting mechanics: noise, pick up and drop, timers, dash, guards, chase and catch, spawn points, collectibles, matches, jump, rewards, difficulty ramp, high scores, boosts, landmarks
extra mechanics: traps, inventory limit, hints, secrets, endings, transform, combos, decoration, medals / ranks, leaderboard
art style: pixel art: low-resolution sprites with visible square pixels and a limited palette
palette: dark: mostly black with a few bright accents
typography: pixel font: blocky bitmap letters
music: chiptune: retro console bleeps
sound effects style: retro bleeps: synthesized chip sounds
screens: title, pause, settings, game over, win, high scores
hud: health, score, timer, combo counter
effects: screen shake, particles, hit flash, trails
accessibility: colour-blind safe palette, reduced motion, remappable keys, difficulty options

# 2. HOW IT IS BUILT


Build a crappy framework first: a hand-placed room rectangle, a player dot, three moving dots, three static boxes, two collectible dots, one detection value, one life counter, one timer, one score counter, one scare key, one caught check, and placeholder title/pause/settings/game-over/win/high-score screens; tune free movement, distance checks, scare state, drop-on-scare, overlap pickup, hide-box detection decay, respawn, timer, and end checks until it plays. Then replace the player dot with the tiny ghost, the moving dots with the sleepy customer, suspicious customer, and baker guard, the static boxes with the flour sack, display case, and cold oven, the collectible dots with the cream puff and croissant, the scare key with the scare verb, the detection value with the detection meter, the timer with the sunrise timer, and the placeholder screens with the pixel title, pause, settings, game over, win, and high-score UI; no concept item adds a rule, system, or screen not already present. A timed one-screen stealth heist is 1 room, 1 player, 1 scare verb, 3 people, 2 pastries, 3 hiding spots, 1 detection meter, 1 timer; nothing in the concept changes what a timed one-screen stealth heist is.

# 3. THE GAME WE WANT

## Story
This is a game where you're a tiny ghost haunting a bakery at night, scaring customers to steal pastries before sunrise. You are Pim, a former bakery mascot made of moonlight and crumbs. You accidentally ate the Head Baker's Moonberry Proof, a recipe so bright it bound you to the bakery and turned your body into a tiny haunting. The Head Baker has sealed the ovens with dawn salt and locked the moon gate. Waiting politely is not open to you: sunrise burns every unclaimed pastry and erases any ghost that has not paid the proof. If you fail, the bakery becomes a daytime shop, your hiding spots become offices, and you spend eternity smelling bread you cannot touch. The stakes are small, silly, and personal: you want your crumbs, your moonlight, and one last night of haunting.

## World
The game happens in one 2D bakery at night, viewed side-on on a single screen: a street through the window, a counter, a display case, ovens, flour sacks, a register, and a moonlit back door. You use free movement, flying, floating, and jumping, with no paths forcing your route. The bakery is full of people who act on their own when you do nothing. Sleepy customers browse and buy. A guard baker patrols with a rolling pin. An inspector checks for crumbs. A fat cat naps in the warm oven. If you do nothing, they continue their routines until sunrise. You can act on them by scaring, distracting, hiding from, or stealing from them. A scare makes a customer jump, drop a pastry, or flee, but it creates noise and raises detection. Hiding in a flour sack, behind a cake, or inside a cold oven resets detection. Pick up and drop lets you set a pastry down to trade it, bait a customer, or stack it for a combo. Dash, jump, and special moves—flour puff, fake customer, wobble—let you dodge and flee. The bakery has landmarks: oven, register, display case, flour wall, moon window. They change how customers see, how noise spreads, and where spawn points appear for guards, customers, and collectibles.

## Content
The kinds of things in the game are deliberately different. Pastries are not identical: a cream puff is light and quiet, a croissant is crisp and noisy, a donut gives a dash boost, a moonberry tart transforms you into a bigger ghost briefly, and a cursed éclair can be dropped as a trap or used to solve a secret. Customer enemies and guards behave differently: sleepy customers can be startled gently, suspicious customers see farther, inspectors punish noise, and baker guards chase and catch on sight. Hiding spots differ: sacks block sight but make noise when opened; ovens hide heat but attract the cat; display cases are risky because they are in plain view. Collectibles include sugar coins, recipe hints, rewards, and matches. Matches let you match a customer's order for bonus points. Hints reveal safe routes and spawn points. Traps include mousetraps, floor alarms, flour bombs, and dawn salt piles. Objectives change each session: steal a certain pastry, scare three customers near the register, reach a hidden moon shelf, or survive a bakery rush. One session differs from the next through spawn points, customer types, and a difficulty ramp that adds guards, timers, and detection speed as the night deepens. Across sessions, the player grows high scores, unlocks medals and ranks, earns decoration points, opens new endings, and learns secrets that make future nights stranger but more rewarding.

## A Session
A session starts on a pixel-art title screen: low-resolution sprites, visible square pixels, a limited dark palette, chiptune music, retro bleeps, and a tiny ghost over a bakery sign. The player opens settings with remappable keys, difficulty options, reduced motion, and a colour-blind safe palette. A session lasts a few minutes. The game begins in real time. The HUD shows health, score, timer, combo counter, and inventory limit. The first minutes are quiet: the player watches customer paths, hides in sacks, and uses a gentle scare to make a sleepy customer drop a pastry. The player steals it, hides, and builds a combo by chaining scares, drops, and escapes. As the timer counts toward sunrise, guards and inspectors appear. The player uses dash and abilities to flee, drops a pastry to distract, and hides after a detection meter flashes. Flour particles and trails mark the route; hit flash and screen shake signal danger. If caught, a life is lost and the player is dropped at a safe spawn point. If the player uses the moonberry tart to transform, the ghost becomes loud and powerful, able to clear a counter but unable to hide. The session can end in several ways. If health runs out, the game over screen appears with a silly epitaph, high scores, and a leaderboard. If the player survives as long as possible but misses the exit, they receive a partial ending. If the player survives, reaches the exit, and beats the score target before sunrise, the win screen opens with medals, rank, unlocked decorations, and a new ending. Pause lets the player catch breath, view settings, and resume.

## Resolution
The whole game ends when the player completes the final night and reaches the moon gate with the moonberry tart, breaking the dawn seal. On the win path, the Head Baker discovers the tiny ghost was the bakery's missing mascot and appoints it official Night Taste Tester; the bakery remains a place of night haunting, not daytime silence. The player is left with medals, ranks, decorations, unlocked secrets, and a personal high score list. On the lose path, the ghost fades at sunrise, but each failure leaves hints that unlock the next night. The final ending is not grim: the bakery becomes a silly haunted cafe where customers laugh when a pastry vanishes, and the leaderboard remembers the highest-stealing tiny ghost. The player is left with the feeling that every night was a small, funny heist: a game about haunting, scaring, stealing, and surviving before sunrise.
