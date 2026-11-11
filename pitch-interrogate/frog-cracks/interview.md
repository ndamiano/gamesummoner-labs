# The interview

## Round 1

### Interrogator

CRACKS
- The tongue is called the main verb, but the page does not define how an anchor becomes known to the player, or what separates safe, weak, and unusable anchors.
- Wall-climbing is named as a core verb, but the page does not say what makes a surface climbable or what states govern holding, sliding up, or falling.
- Failure recovery is described as reset to “last safe perch” and “coughed up nearby,” but no rule defines safe perch, nearest edge, or outcomes when none exists.
- Hazards react to “moving too much” and “open ground,” but no rule says what triggers cat or heron attention, approach, or attack.
- Eating is called “flavor and feedback, not progress,” yet eating a wasp is described as causing a “useful sideways hop,” leaving its mechanical role unclear.
- The page describes an opening phase, then “later game” and “levels,” but it does not say what completes one place and begins another.

QUESTIONS
1. The page says, “The tongue is the main verb, but it is not a magic rope. It catches things that are small, grabbable, and visible... If the player guesses wrong, the tongue snaps out and grabs nothing... If they guess slightly wrong, the tongue catches a weak object, and the object breaks or moves unexpectedly.” How does the game decide which anchors are safe, weak, or unusable, and how does the player learn the difference before using the tongue?

2. The page says, “When the frog lands on it, its sticky pads catch. The player can slide upward against it.” What conditions make a surface climbable, and what states govern the frog holding, climbing, slipping, or falling on it?

3. The page says, “If a cat catches the frog... reset to the last safe perch. If a heron snaps... the frog is coughed up nearby. If the frog gets into water... it must haul itself onto the nearest edge. There is no death screen.” What counts as a safe perch or nearest edge, and what happens when a fall or hazard cannot be resolved by returning the frog to an obvious perch?

4. The page says, “Moving too much makes the cat step closer” and “A heron’s shadow passes over open ground, and the player learns that open ground is dangerous.” What states cause the cat and heron to notice, approach, or strike, and what player behaviors change those states?

5. The page says, “eat a wasp and get dizzy, causing a weird but useful sideways hop” but also, “These are flavor and feedback, not progress.” How can eating affect traversal, and how does the player control whether those effects help or hinder them?

### Pitcher

Here is how my game resolves those seams.

1. The tongue has two registers: a light grab and a committed anchor. A light grab catches anything small enough to eat. A committed anchor needs something with structure enough to support the frog’s weight. Safe anchors are solid, thick, damp, textured things with visible grain or edges: wet wood, braided hose, metal grates, stone lips, thick vines, strong spider silk. Weak anchors are dry, torn, translucent, fraying, loose, or too light: dry leaves, paper, cracked tile, rotten stems, thin webs, loose string. Unusable anchors are smooth, slick, hollow, or open: glass, polished plastic, bare metal, water, air. The player learns this by material language and safe testing. A quick tongue flick is a probe; it does not commit the body. Safe objects give a firm recoil and stay still. Weak objects flutter, crack, droop, or snap. Unusable objects slide, splash, or ignore the tongue. The game does not mark anchors with UI. It teaches by showing what the tongue catches and what happens when you hang from it.

2. A surface is climbable if it is wet and textured enough for sticky pads: mossy stone, damp brick, rough bark, rubber, metal grates, condensation-coated frames, or other surfaces that read as grippy. Dry, smooth, oily, or polished surfaces are not climbable; they cause a slide or a fall. Climbing is a contact state. When the frog’s pads meet a climbable surface, it automatically enters Grip. A stable wall grip can be rested on. Moving up makes the frog slide upward. Moving down makes it slide down. Jumping releases it. Some surfaces are temporary: they allow Grip for a short time, then Slip, then Fall. Crumbling ledges, rotten bark, cracked tiles, and loose moss can break under the frog. Hazard contact can also break Grip. The player learns the difference by reading material: stable surfaces hold, temporary surfaces sag or crack, and nonclimbable surfaces reject the pads.

3. A safe perch is the most recent stable, weight-bearing contact that is not part of a moving hazard, not in a hazard’s active attack zone, and not structurally failing: a dry ledge, sturdy branch, stone lip, cork, stable wall grip, lily root, or similar object that would plausibly hold a frog. The “last safe perch” is the nearest such point that still exists and is still safe. If a cat catches the frog, it is batted away and placed back at that perch. If a heron catches it, the frog is coughed up at the nearest safe perch outside the heron’s strike zone. If the frog enters water, it can swim poorly toward the nearest stable edge. If there is no obvious edge nearby, the current carries it to a guaranteed side, or the game returns it to the last stable node. There is no unresolved fall. If a hazard would leave the frog with nowhere to go, the game nudges the hazard, moves the frog to a rescue ledge, or places it at the nearest stable object. The punishment is delay and embarrassment, not death.

4. The cat has four states: Unaware, Watching, Prowling, and Strike. It notices the frog only if the frog moves inside its line of sight or makes noise: hopping, splashing, tongue snaps, falling objects, scraping on metal. Motion and noise raise Watching. Stillness, cover, and distance lower it. If Watching gets high enough, the cat enters Prowling and steps closer. If the frog stays exposed near it, the cat Strikes. The player changes this by freezing, hiding behind leaves, moving behind a barrier, or making a louder noise somewhere else to pull the cat’s attention. The heron has three states: Hunting, Shadowed, and Strike. It notices open ground. If the frog is in an exposed area without overhead cover, the heron’s shadow drifts over that ground and attention rises. Moving in the open raises it faster. Cover, waiting in shadow, and moving from covered place to covered place lower it. The heron Strikes when attention is high and the frog is exposed. The player can distract it by disturbing a branch, starting a sprinkler, knocking something, or making it look elsewhere. Open ground is not instant death. It is a state the player has to cross carefully.

5. Eating is never required, never scored, and never permanent. It is a body state, not progression. Flies, wasps, and beetles affect the frog briefly. A fly might make the frog sneeze. A beetle might make it sluggish. A wasp makes the frog Buzzed for a short time: the next jump gets a sideways kick and less control. That can help the frog cross a gap if the player times it deliberately, but it can also ruin a jump if the player is careless. The player controls this by choosing whether to eat, when to eat, and whether to use the effect. Eating can create clever traversal, but it does not unlock new abilities, fill a meter, or count toward completion. The rule is: eating changes the body for a moment, but the game never asks the frog to eat in order to move forward.

If the designer also needs the unasked seam: a place is completed when the frog reaches its next visible water body or rooftop perch and the frog’s call answers. The next place begins when the frog enters a plausible frog route into that new area: a drain, a window, a vine, a gutter, or a gap. Completion is physical arrival, not an abstract trigger box.

## Round 2

### Interrogator

CRACKS
- The committed tongue is defined as a valid anchor, not as a traversal action: after a committed anchor attaches, the page does not say what the frog can do with it, how that movement is generated, or what makes it fail.
- Water and aquatic hazards are named, but the page does not define the states or outcomes of being in water, swimming, being carried by currents, being slowed, exiting, or being attacked by fish.
- The page says hazards can start without warning but also that the player can start hazards, and it describes physical consequences without saying what objects or hazards can be changed, what can change them, or how those changes propagate.
- Place completion depends on “the frog’s call answers” and entering a “plausible frog route,” but the call, the choice of goal among visible water bodies or perches, and the transition to the next place are undefined.

QUESTIONS
1. The page says, “The tongue is the main verb… It is for moving,” and describes “a tongue that can grab, yank, and pull,” while your answer says, “A committed anchor needs something with structure enough to support the frog’s weight.” Once a committed anchor attaches, what can the frog do with it, what makes each action possible or fail, and what ends the anchor?

2. The page says, “Water carries the player in currents but also slows them down,” and “If the frog gets into water, it can swim, but poorly, and it must haul itself onto the nearest edge.” What states, actions, and outcomes define the frog being in water, and how do swimming, drifting, being carried, slowed movement, exiting, and fish or pond hazards fit together?

3. The page says, “A sprinkler can start without warning, turning a ledge into a slide,” but also says the player can “start a sprinkler to knock a caterpillar off a branch so the branch dips lower,” and states, “The world is not made of locked doors or switches. It is made of small physical consequences.” What makes an object or hazard automatic, player-caused, or changeable; what can the frog do to change it; and how do those changes spread through a place without becoming abstract switches?

4. Your added seam says, “a place is completed when the frog reaches its next visible water body or rooftop perch and the frog’s call answers,” and “the next place begins when the frog enters a plausible frog route into that new area.” What is the call, how does a place decide which visible water body or perch is the one that answers, and what makes a route into a new area begin the next place instead of being another traversal path?

### Pitcher

Here is how I would close them.

1. Once a committed anchor attaches, the tongue becomes a short, taut line. The frog hangs from it; left or right creates a pendulum swing, and releasing at the right moment launches the body. If the anchor is close and strong, holding up can pull the frog toward it; if the anchor is a small movable object, a quick yank can tilt, drag, or disturb that object. If the object is too heavy, it does not move; if it is weak, it bends, snaps, or lets go under weight. The anchor ends when the player releases, the object fails, the tongue overextends, the frog is hit by a hazard, or the frog reaches a stable surface and grabs it with its pads. The game teaches this by showing tension: safe anchors stay still and creak, weak anchors sag and crack, unusable ones slide away or splash.

2. Water is a state, not a separate minigame. When the frog enters water, it floats at the surface and can paddle in short, weak strokes; it can submerge briefly, but cannot jump or stick until it is out. Currents are directional pushes that add to the frog’s motion, so swimming against them is hard and riding them can be useful. The frog can exit only by reaching an edge it can grip; smooth or dry edges cause a slip, while damp textured edges let it haul itself up. Fish and pond hazards notice movement and ripples: stillness, cover, and lily roots reduce attention, while open swimming raises it; a lunge bumps the frog toward a current or edge, not into death. If no edge is reachable, the current carries the frog to a guaranteed safe deposit or the nearest stable perch.

3. The world has three kinds of things. Static things are fixed: walls, floors, solid stone, large pipes, and permanent terrain. Reactive things can be changed by physical cause: loose corks, hinged shutters, hanging branches, floating leaves, wet surfaces, light objects, and anything with a joint or loose connection. Active things have their own behavior: animals, rain, wind, currents, sprinkler timers, and hazard routines. The frog changes things by applying plausible forces: pulling, landing, splashing, dripping, weighing on an object, eating something that affects its body, or making noise. Those changes spread only through physical contact: water wets a surface, force moves a branch, a broken object falls, vibration draws a cat, sight draws a heron, and a current moves debris. If the frog cannot touch, push, wet, break, disturb, or ride it, it is scenery.

4. The call is a held croak, not a menu prompt. It answers only at an Answering Goal: a visible water body or perch with a live chorus or another frog that will respond. Other ponds, puddles, and perches are silent, blocked, dangerous, or decorative; calling at them only produces a normal croak. A place decides its goal by having exactly one place that answers, and the player learns this by listening, by the goal’s call being heard from the route, and by the failure of calls elsewhere. A route into a new area is a Threshold: a narrow physical passage such as a drain, window, vine, gutter, or gap that crosses into a different bounded place with its own Answer Node, start perch, ambient call, and hazard set. Crossing it begins the next place because the old place’s soundscape and hazards end and the new place’s begin. Any path that stays within the same Answer Node’s soundscape is just another traversal route, not a transition.

## Round 3

### Interrogator

CRACKS
- The page frames the whole game as reaching a moonlit rooftop pond, but the place-completion rule creates many Answering Goals and Thresholds without saying which is final, how places lead to that pond, or what happens when it is reached.
- The page says the game is not an open world but also says levels become more vertical and more connected; it does not say whether places are separate one-way levels or a connected, revisitable network.
- The tongue probe rule says a light grab catches anything small enough to eat, while safe anchors are solid/thick objects and the player is told to test them with a quick flick; this does not say how probing works without eating or committing.
- The Answering Goal requires a held croak, while hazard states are raised by noise; it does not say whether the goal call is a risky noise action or can affect hazards.

QUESTIONS
1. The page says, “You are a frog… The player is a small, wet frog trying to reach a moonlit rooftop pond where the frogs are calling,” while your rule says each place ends at an Answering Goal and a Threshold. How does the game decide which place is the final moonlit rooftop pond, how does the sequence of places lead there, and what happens when the frog reaches it?

2. The page says, “The game is not an open world. It is made of clear, crafted places that can be learned and traversed,” but also says, “After the opening phase, the game stops teaching and starts trusting. The levels become more vertical and more connected.” Are the places one-way crafted levels, or can the player move between, revisit, and learn a connected set of places, and how does that change what the player is expected to remember or do?

3. The page says, “A quick flick snaps out, catches the fly, and the frog swallows it,” and your rule says, “A light grab catches anything small enough to eat… A quick tongue flick is a probe; it does not commit the body,” while also saying the player tests safe anchors. How can the player test a solid, non-eatable anchor without swallowing it or committing the body, and what does the tongue do when it touches something not small enough to eat?

4. Your rule says, “The call is a held croak… It answers only at an Answering Goal,” while the hazard rules say, “It notices the frog only if the frog moves inside its line of sight or makes noise: hopping, splashing, tongue snaps, falling objects, scraping on metal.” How does the held croak interact with hazard attention, and can calling attract, distract, or otherwise change the behavior of cats, herons, or other hazards?

### Pitcher

Here is how I would close them.

1. The game is a ladder upward. The moonlit rooftop pond is the final Answering Node because it is the only place with a full chorus and no onward Threshold. Every other Answering Node is a smaller pond, perch, or calling frog that leads to one forward route closer to that final pond, usually higher, louder, or more exposed to the rooftop sound. Optional paths may branch, but they loop back, dead-end, or remain clearly shorter than the main line. When the frog reaches the rooftop pond and calls, the chorus answers, the frog settles, and the main game ends.

2. My game is not one-way levels. It is a connected set of handcrafted places, not an open world. After a place is completed, it remains reachable through stable return routes, so the player can revisit, take shortcuts, or test ideas again. What the player is expected to remember is not hidden keys, but how the place works: anchor materials, hazard routines, currents, wet surfaces, and what can be changed by touch, weight, noise, or water. The boundaries are visible and narrow, so it feels learned and bounded, not free-roaming.

3. A light tongue flick is only a grab if the tongue can curl around the target and the target is food-sized. If the target is too thick, too solid, or not food-sized, the tongue tip taps and releases; it cannot swallow it and it does not commit the body. That tap gives the same material feedback as a failed anchor: firm recoil for safe, flexing or cracking for weak, sliding or splashing for unusable. A safe anchor may show a brief sticky contact that releases under the tongue’s own weight, telling the player it can hold the frog if committed.

4. The held croak is a loud noise action. It raises the attention of cats, herons, and other hazards within hearing range, and it can be used to distract them: calling from behind cover can pull a cat’s Watching toward the frog’s perch or make a heron turn toward the sound. It is not safe by default. Answering Goals are either free of active hazards, or the hazards are arranged so the player must wait, hide, or distract them before calling. Calling at a silent perch does nothing except make noise.

## Round 4

### Interrogator

CRACKS
- The game is called a ladder upward, but also a connected set of places that remains reachable; it does not say whether places are sequentially gated or can be entered out of order.
- “Stable return routes” are named but not defined; it is unclear whether completing a place opens a safe reverse path, changes hazards, or merely lets the player retrace the original route.
- The held croak completes a place, but if a hazard interrupts it, the place’s state and retry outcome are undefined.
- A completed Answering Node remains reachable, but whether it still counts as an Answering Goal, can be called again, or becomes a safe perch is undefined.

QUESTIONS
1. The page says, “The game is a ladder upward,” and your added seam says, “Every other Answering Node is a smaller pond, perch, or calling frog that leads to one forward route closer,” but also says, “After a place is completed, it remains reachable through stable return routes.” If the player reaches a later place or Answering Node through an optional route before completing the intended previous place, does that place become available, can it be completed, or is it blocked until the main line reaches it?

2. The added seam says, “After a place is completed, it remains reachable through stable return routes.” What makes a return route stable, when does it become available, and does completing a place change the place itself to make return possible, or is return only the original unchanged path?

3. The added seam says, “The call is a held croak,” and later says, “The held croak is a loud noise action. It raises the attention of cats, herons, and other hazards within hearing range.” If a hazard interrupts or attacks during the held croak before the Answering Goal responds, does the place remain incomplete, where is the frog placed, and what must the player do to try again?

4. The added seam says, “Every other Answering Node is a smaller pond, perch, or calling frog that leads to one forward route closer,” and also says, “After a place is completed, it remains reachable.” Once a place is completed, can the frog call at its Answering Goal again, does it still function as an Answering Goal, and can it be used as a safe perch or starting point for revisits?

### Pitcher

Here is how I would close them.

1. I choose the soft ladder. The places are not hard-locked by story gates; a later place is available if the frog can physically reach it and its Answering Node has a live chorus. The “ladder” is the readable, taught route upward: each Answering Node is heard from the next, and the next is normally reached by following that call. Optional routes to higher places are made steep, exposed, and hazard-heavy, so skipping ahead is possible but not easy. The moonlit rooftop pond is final because it is the only place with a full chorus and no onward Threshold; if the frog reaches it early and calls, the chorus answers and the game ends.

2. A stable return route is a continuous, survivable path back from the Answering Node to a previous safe perch using only stable anchors, climbable surfaces, safe drops, and currents that can be exited. It becomes available when the place is completed because the completed path leaves the world in a reversible state: a branch stays bent, a cork stays out, a leaf raft stays against a ledge, a drain cover stays off, or a wet surface stays climbable. Completing a place does change some physical objects to make return possible; it is not merely retracing the forward route if that forward route was one-way. If no such physical route exists, the place is not considered completed until the frog has created or found a safe way back.

3. If a hazard interrupts the held croak before the Answering Node responds, the place remains incomplete. The frog recovers by the normal hazard rules: a cat bats it back to the last safe perch, a heron coughs it up outside its strike zone, a current carries it to a guaranteed edge. The interrupted call raises hazard attention, but that attention decays if the frog is still, hidden, or away. To try again, the frog must return to the Answering Node after making the immediate area safe by waiting, distracting, or physically changing the hazard.

4. Once a place is completed, its Answering Node becomes a Rest Node. The frog can call there again, but it only gets a friendly chorus response, not another place completion. It no longer functions as an Answering Goal for that place. It is a safe perch: stable, free of active hazard routines in its immediate area, and usable as a starting point for revisits. If the frog moves away from the Rest Node and calls, normal hazard noise rules apply again.

## Round 5

### Interrogator

CRACKS
- Completion and return are circular: “A stable return route… becomes available when the place is completed,” yet “the place is not considered completed until the frog has created or found a safe way back.”
- The final place ends the game on a call, but the return-route rule does not say whether a final place needs a return route or what happens if none exists.
- Greenhouse material rules conflict: the page says condensation makes metal frames slippery, while the clarified rules call “condensation-coated frames” climbable.
- Active environmental hazards named in the page (“A sprinkler can start without warning,” “A rooftop has wind that changes the arc of a hop,” “Rain barrels tip.”) have no defined states, triggers, or physical effects.
- Eating effects still say “might,” leaving when fly or beetle body states occur undefined.

QUESTIONS
1. You say, “A stable return route… becomes available when the place is completed,” but also, “If no such physical route exists, the place is not considered completed until the frog has created or found a safe way back.” Does calling at an Answering Node complete the place, or does creating or finding a safe way back complete it? If both are required, what is the order, what tells the player the place is incomplete, and does the player need to call again after making the route?

2. You say, “The moonlit rooftop pond is the final Answering Node because it is the only place with a full chorus and no onward Threshold,” and, “If the frog reaches it early and calls, the chorus answers and the game ends.” Under the rule that a place is not considered completed until there is a safe way back, does the final place need a return route or Threshold? What happens if the frog can call but cannot return anywhere?

3. The page says, “A greenhouse has glass that cannot be stuck to, but condensation makes the metal frames slippery,” while your answer lists “condensation-coated frames” among surfaces that are climbable. Which material states are true for greenhouse frames, and how does the player tell whether a wet, textured surface will grip or slip?

4. The page says, “A sprinkler can start without warning,” “A rooftop has wind that changes the arc of a hop,” and “Rain barrels tip.” Your answer says “Active things have their own behavior” and changes spread by physical contact. What states, triggers, and physical consequences define these active environmental hazards, and what begins, continues, or stops them?

5. The page says, “A fly might make it sneeze,” and your answer says, “A fly might make the frog sneeze. A beetle might make it sluggish.” Under what conditions do these body states occur, and can the player predict or control them?

### Pitcher

Here is how my game closes them.

1. I choose the non-circular rule: the safe way back is a precondition, not a completion reward. A place is completed only when the frog holds the croak at an Answering Node that already has a stable return route. The order is: make or discover a stable return route from the Answering Node, then call. If the frog calls before such a route exists, the Answering Node stays silent: no answering chorus, no settling, no completion. The player knows the place is incomplete because the Answering Node’s call does not resolve and the old place’s soundscape continues. If the player creates a route after a failed call, they must call again. If the route already exists, one successful call completes the place and no second call is needed. A later place reached through an optional route can be completed only if it already satisfies this rule; otherwise it is just a hazardous dead end, not an Answering Node.

2. The final rooftop pond is exempt from the return-route rule because it is not a place to be left. It is the destination, so it does not need an onward Threshold or a stable return route. If the frog reaches the moonlit pond, holds the croak, and the full chorus answers, the game ends immediately, even if there is no way back. If the frog cannot call, the game does not end.

3. The page is true: condensation makes greenhouse metal frames slippery. In my game, dry textured metal can grip, glass is unusable, and metal under condensation, running droplets, or a wet sheen is slippery and causes the pads to slide. The player reads it by the shine, the way water runs down the frame, the smearing of the tongue, and the lack of grain. A damp but matte, grainy surface may grip; a surface coated with a water film cannot.

4. Active environmental hazards are physical systems with visible tell states. Sprinkler: dormant, pressurized, spraying, spent; it starts from a pressure timer, a leaking valve, or the frog pulling a cord, breaking a cork, or striking a loose part; it sprays fixed arcs, wets surfaces, knocks light objects, makes noise, and stops when pressure drains or the valve closes. Wind: calm, building, gusting, lull; it starts from open rooftop conditions or weather; it adds horizontal force to hops and swings, moves flags, leaves, and rain, ripples water, and stops after a gust. Rain barrel: stable, unbalanced, tipping, fallen; it starts from the frog’s weight on the rim, sloshing water, a tongue yank, or impact; it pours water, creates currents, floats leaves, wets surfaces, may carry the frog, and stops when it settles. The player can begin, continue, or stop them only by plausible physical causes: weight, impact, pulling, blocking, or redirecting water.

5. Eating effects are not random. They happen when the frog swallows a live insect of that kind: a live fly twitching causes a sneeze, a live beetle kicking causes sluggishness, and a live wasp buzzing causes the Buzzed state. A dead, stunned, or knocked-down insect gives no body state. The player predicts this from the insect’s animation and controls it by choosing whether to eat, when to eat, and whether to eat live creatures. The effects are short and never required.

## Round 6

### Interrogator

CRACKS
- The optional-route rule says a later place can be completed only if it already satisfies the stable-return-route rule, but the general completion rule says the player may make or discover a stable return route before calling. These cannot both be true.
- Answering Goals may be a “visible water body,” but completion requires a stable return route and the completed node becomes a safe Rest Node; open water is not a safe perch, and it is undefined whether the frog can call from water or must reach an edge.
- The page says a sprinkler can start “without warning,” while the clarified rules say active hazards have “visible tell states.”
- The terms “stable return route” and “safe drops” decide whether a place can be completed, but what makes a drop, surface, or current safe or unsafe is not defined.
- “Rain” is listed as an active thing, but no states, triggers, or physical effects are given.

QUESTIONS
1. The answer says, “A later place reached through an optional route can be completed only if it already satisfies this rule; otherwise it is just a hazardous dead end, not an Answering Node,” while also saying, “The order is: make or discover a stable return route from the Answering Node, then call.” If a player reaches a later place early, can they create or discover a stable return route and then call, or is that place permanently a dead end until something else establishes it? What changes it from a dead end into an Answering Node?

2. The answer says, “Answering Goal: a visible water body or perch with a live chorus,” but also says, “A place is completed only when the frog holds the croak at an Answering Node that already has a stable return route,” and later, “Rest Node... safe perch: stable, free of active hazard routines.” If the Answering Goal is a water body, what exactly is the node—the water surface, an edge, a lily root, a stone lip, or something else? Can the frog call from water, or must it reach a stable perch? How can that node become a safe Rest Node?

3. The page says, “A sprinkler can start without warning, turning a ledge into a slide,” but the answer says, “Active environmental hazards are physical systems with visible tell states.” Which hazards may begin without warning, and what physical tells or lack of tells distinguish a sudden hazard from a telegraphed one?

4. The answer says, “A stable return route is a continuous, survivable path back from the Answering Node to a previous safe perch using only stable anchors, climbable surfaces, safe drops, and currents that can be exited.” What makes a drop, surface, or current safe or unsafe for that route, and what can the frog do to change an unsafe element into a safe one?

5. The answer says, “Active things have their own behavior: animals, rain, wind, currents, sprinkler timers, and hazard routines.” What does rain do in the game? What states or triggers does it have, and how does it physically affect surfaces, water, noise, hazards, or traversal?

### Pitcher

Here is how my game closes them.

1. I choose the general rule: the “already satisfies” sentence was wrong. A place is not permanently locked, and a later place is not permanently a dead end just because the player reached it early. A place can be completed if three things are true: the perch has a live Answering chorus, the frog can hold the croak there, and a stable return route exists from that perch. The player may create or discover that return route first, then call. If they call before a stable return route exists, the chorus does not answer and the place remains incomplete. If they then make a safe way back, they must call again. What changes a hazardous dead end into a completable place is physical: a leaf raft is dragged to an edge, a cork is pulled to block a current, a branch is bent into a reachable anchor, a wet wall becomes climbable, or a falling object creates a stable landing. If there is no live chorus, it is never an Answering Node; it is only a dangerous perch.

2. A visible water body is the landmark, not the completion node. The Answering Node is the specific stable perch that belongs to the chorus: a stone lip, lily root, mossy edge, stable cork, gutter lip, or other stable surface beside the water. The frog cannot call from open water. If it is in water, it can hear the chorus and paddle toward the Answering perch, but it must haul itself onto a stable edge before holding the croak. When the place is completed, that perch and its immediate stable surroundings become a Rest Node. The water itself remains active: fish, ripples, currents, and pond hazards still exist around it, but the Rest Node is a stable perch free of active hazard routines. If the only edge near a water body is weak, slippery, moving, or inside a fish strike zone, it is not an Answering Node until the frog makes it stable or reaches a stable edge.

3. No hazard begins with no physical tell. The page’s “without warning” is my game only in this sense: there is no interface warning, no HUD alert, and no safe countdown. The hazard still has a physical tell, but the player may miss it. A sprinkler can feel sudden because its tell is short and local: a valve tick, a shudder in the pipe, a first droplet, a wet patch forming under a nozzle, or a pressure line flexing. Wind has tells: flags, leaves, rain drift, and ripples change before the gust. Rain has tells: a cloud shadow, first large drops, and a change in surface shine. A sudden hazard has a brief, local tell that is easy to ignore; a telegraphed hazard has a broad, sustained tell that gives the player time to react. If something has no physical tell at all, it is not a hazard in my game; it is scenery or a scripted moment.

4. A safe drop is a fall from a stable perch to a stable landing where the frog is not forced into a hazard, not thrown into open water with no exit, not landed on a weak, slippery, or moving surface, and not dropped into an active cat, heron, fish, sprinkler, current, or crumbling area. An unsafe drop may still be survivable, but it is not a stable return route because it forces the frog into delay, embarrassment, or another hazard. A safe surface is a stable anchor or climbable surface that is not currently failing, not covered by hazard, and not too slippery for the frog’s pads. A safe current is one the frog can enter, ride, and exit without being carried into a hazard or swept past all stable edges. An unsafe current has no exit, is too strong, or carries the frog into a hazard. The frog can change unsafe things into safe ones by physical cause: float a leaf to make an exit in a current, pull a cork to block a drain, wet a textured wall so it can be gripped, drag a branch into a gap, knock a hazard out of the route, or distract an animal so the area becomes passable.

5. Rain is a place-wide weather system, not a constant background effect. Its states are dry, first drops, drizzle, steady rain, downpour, and tapering. It begins when a weather front passes over the place; the tells are cloud shadow, first large drops, wind shift, and surface shine. It continues while the front covers the place and stops when the front moves away, though wetness remains afterward. Physically, rain wets surfaces: textured surfaces become climbable, smooth surfaces become slippery, metal under a water film causes slides, glass remains unusable, and puddles expand or become traversable platforms. It creates ripples, currents, floating leaves, and carried debris; it can fill gutters, start drains, float new rafts, or raise water enough to make a route possible or possible only if the player times it. It affects animals by making some seek cover and some become more alert to movement under cover; its broad sound masks small player noises, but deliberate sounds like croaks, splashes, and metal scrapes still raise hazard attention. Rain can create routes and remove them, and the player can use it by waiting, sheltering, opening a drain, redirecting water, or letting a surface become wet enough to climb.
