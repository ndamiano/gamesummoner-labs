# 0. CONCEPT

Stealth game. The view is a fixed 2D level seen from the side. The player controls a character through rooms with obstacles, hiding spaces, people, and collectible objects. The player moves with keys or a stick, crouches or hides, and presses a scare action to startle nearby people so they stop watching or move away; this creates a window to press a grab action and take an object. The screen shows the character, people with sight cones or alert meters, objects, a required-item counter, and a countdown. The player repeats: move unseen, scare, grab, leave. A level is won when the required number of objects is collected before the countdown ends. It is lost if the countdown reaches zero, the detection meter fills, or the character is caught.

# 1. WHAT EVERY ONE HAS

- Title screen with Start, How to Play, Quit, and a visible control map.
- A how-to-play screen that fits one screen and shows move, hide, scare, grab, and timer.
- A level-start screen that states the required object count and the countdown length.
- A short session, usually 2-5 minutes, with one level or a small set of 3-8 levels.
- A controllable character moved by keyboard, mouse, or stick with left, right, crouch, and interact.
- A level with fixed rooms, obstacles, hiding spaces, and sight-blocking cover.
- A fixed number of object kinds, usually one, and 3-10 copies per level.
- People who patrol, stand, or wander and can detect the character by sight or noise.
- Detection feedback: sight cones, eye icons, alert meters, and clear calm/suspicious/searching states.
- A scare action: press a button; nearby people startle, stop watching, or move away; the character can then approach an object.
- A scare cooldown or 1-3 uses per level so the player must choose when to scare.
- A grab action: press a button when close to an object; the object is added to the required counter.
- An objective counter showing required objects, collected objects, and remaining time.
- A countdown that starts when the level starts and forces the player to act quickly.
- A detection meter or caught state that rises when people see the character; full detection ends the attempt.
- A penalty for being seen: the character is reset, hidden, or forced to lose time while people search.
- A choice between safe routes and risky routes that change distance, detection risk, and item access.
- A progression track: winning a level unlocks the next level, with more people, tighter sight, or shorter timers.
- Feedback for success and failure: sound cues, screen flash, item pickup, and timer warning.
- A pause/restart option that lets the player retry the current level without losing progress.
- A win screen after collecting the required objects before the countdown ends, with time and score.
- A loss screen when the countdown ends or detection fills, with retry and level select.
