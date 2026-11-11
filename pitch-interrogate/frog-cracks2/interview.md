# The interview

## Round 1

### Interrogator

CRACKS
- The tongue’s grab, swing, release, and failure states do not fit together. The page says holding extends and catching, “Releasing lets the frog swing,” but also “If the player guesses wrong, the tongue snaps out and grabs nothing, and the frog drops,” and “A missed tongue leaves the frog dangling for a beat before it falls.” A builder cannot tell whether a missed tongue catches nothing, grabs weakly, or leaves the frog attached.
- The rules for sticking, sliding, and slipping are not separated. “its sticky pads catch. The player can slide upward against it” and “climb damp walls, slide down wet ones” conflict with “Surfaces are wet, slick, sticky, brittle, or moving,” “condensation makes the metal frames slippery,” and “It cannot stick to smooth glass or open water.” The page does not say what makes a surface clingable, climbable, slippery, or non-grabbable, or how the player moves upward on a wall.
- Hazards sometimes act on their own and sometimes can be used by the player, but the page does not say how the world decides. “A sprinkler can start without warning” and later “start a sprinkler to knock a caterpillar off a branch” sit next to “The world is not made of locked doors or switches.” The builder needs to know whether hazards are scripted, random, triggered by the frog’s actions, or only available in certain levels.
- The cat’s awareness and behavior are not ruled. “Moving too much makes the cat step closer” and “A cat can swat at the frog if it is noticed” do not define what counts as movement or notice, how close it must be, what state the cat moves through, or what happens after a swat beyond resetting.
- The heron’s threat is not tied to a clear trigger. “A heron’s shadow passes over open ground, and the player learns that open ground is dangerous” and “If a heron snaps at the frog…” do not say when open ground is dangerous, what the shadow means, how the heron chooses to strike, or how disturbing a branch makes the heron look elsewhere.

QUESTIONS
1. The page says: “The player holds the tongue control and the frog’s tongue extends, catching the branch. Releasing lets the frog swing. If the timing is wrong, the frog drops into a puddle.” It also says: “If the player guesses wrong, the tongue snaps out and grabs nothing, and the frog drops” and “A missed tongue leaves the frog dangling for a beat before it falls.” What is the actual order of a tongue grab, swing, release, and failure?

2. The page says: “When the frog lands on it, its sticky pads catch. The player can slide upward against it.” Later it says: “Surfaces are wet, slick, sticky, brittle, or moving,” “condensation makes the metal frames slippery,” and “It cannot stick to smooth glass or open water.” What decides whether the frog clings, slides, or slips, and what does the player do to move upward on a wall?

3. The page says: “A sprinkler can start without warning” and later says the player can “start a sprinkler to knock a caterpillar off a branch.” It also says: “The world is not made of locked doors or switches. It is made of small physical consequences.” What makes a hazard begin on its own, and what makes a hazard something the player can intentionally use?

4. The page says: “Moving too much makes the cat step closer.” and “A cat can swat at the frog if it is noticed.” What counts as the cat noticing the frog, and what does the cat do after it notices, after it steps closer, and after it swats?

5. The page says: “A heron’s shadow passes over open ground, and the player learns that open ground is dangerous.” and “If a heron snaps at the frog, there is a brief dark swallow, then the frog is coughed up nearby.” What makes open ground dangerous, and what makes the heron choose to snap at the frog?

### Pitcher

1. The tongue is one held action. Hold it and the tongue extends along the frog’s aim; if the tip hits a grabbable anchor, it sticks at contact. While held, the frog is attached and can pull or swing. Release detaches it and keeps the momentum. A clean miss has no dangle: it grabs nothing and the frog falls normally. Only a weak anchor catches, slips, and leaves the frog dangling for a beat before falling. “Timing is wrong” means releasing too low or too late, so the swing fails and the frog drops. The dangle line is the weak-anchor case, not the clean miss.

2. Pads grip only damp, textured, porous surfaces: bark, moss, wet wood, rough stone, damp concrete. Smooth, dry, dusty, oily, glazed, glass, open water, and metal covered in a condensation film do not grip. On a climbable damp wall, landing makes the frog cling; it does not slide upward. To move upward, the player holds toward the wall and times small hops or crawls, each successful pad contact moving the frog a little. On a slippery surface, holding toward the wall only slows the slide; the frog slides down. The page’s “slide upward” is not the game.

3. Hazards are authored physical systems, not switches or random dice. A hazard begins on its own when its own state reaches a visible threshold: pressure builds in a sprinkler, a timer weight falls, an animal patrol reaches a line. A hazard becomes something the player can intentionally use when the player can change that physical state: knock a cork loose, hit a hose clamp, disturb a branch, splash near a water sensor. “Without warning” means no HUD prompt, not invisible randomness.

4. The cat notices by line of sight plus movement or noise. Standing still in cover is hidden; moving, hopping, or splashing in view raises its attention. When noticed, the cat steps closer only while the frog remains visible or moving. If the frog stays exposed near it, the cat swats. After the swat, the cat loses interest for a few seconds and returns to watching or patrolling; the frog is reset. If the frog stops or hides, the cat’s attention decays.

5. Open ground is dangerous when it lies in a heron’s hunting sight: water, lawn, open tiles, places with no cover or anchor. The shadow is the telegraph marking the target area. The heron snaps when the frog moves or splashes inside that sight while unhidden. If the frog is still, under cover, on a wall, or outside sight, the heron ignores it. Disturbing a branch creates motion elsewhere, so the heron shifts attention and stops hunting that spot.

## Round 2

### Interrogator

CRACKS
- The tongue’s eating action is not placed in the ruled tongue system. The page says: “A quick flick snaps out, catches the fly, and the frog swallows it.” The ruled tongue is “one held action” that sticks to anchors, can be held while attached, and detaches on release. A builder cannot tell how eating works, whether it is a separate action, or how it interacts with grabbing anchors.
- The goal is named as the destination, but what completes it is not ruled. The page says: “The goal is always visible in a distant shape: a rooftop pond, a ring of lilies, a faint chorus.” It does not say what reaching that shape does, what ends, what begins, or what counts as completion.
- Reset and failure are incomplete. The page says: “the frog is reset to the last safe perch” and “the frog is coughed up nearby.” It also says: “Water carries the player in currents.” A builder cannot tell what a last safe perch is, or what happens when the frog falls out of the authored space, is carried by a current, or ends where no edge or perch exists.
- Eating effects are left as “might” and “can.” The page says: “Eating a wasp might make the frog hiccup and puff, which can cause a strange hop. Eating a fly might make it sneeze.” A builder needs to know whether these are reliable mechanics, optional flavor, or authored interactions.
- Weak anchors are a core tongue failure mode but are not defined. The page says: “If they guess slightly wrong, the tongue catches a weak object, and the object breaks or moves unexpectedly.” A builder cannot tell how weak anchors are identified, whether they are always authored, or what allowed outcomes occur when they fail.

QUESTIONS
1. The page says: “The goal is always visible in a distant shape: a rooftop pond, a ring of lilies, a faint chorus.” What condition completes a crafted place or the game?

2. The page says: “the frog is reset to the last safe perch” and “the frog is coughed up nearby.” It also says: “Water carries the player in currents.” What is a last safe perch, and what happens when the frog falls, is carried away, or ends up where no edge or perch can be reached?

3. The page says: “A quick flick snaps out, catches the fly, and the frog swallows it.” It also describes the tongue as “one held action” that sticks to anchors and is released to detach. How does eating an insect work as a game action, and how is it distinguished from grabbing an anchor?

4. The page says: “Eating a wasp might make the frog hiccup and puff, which can cause a strange hop. Eating a fly might make it sneeze.” When does an eaten insect produce a physical effect that the player can plan around, and when does it produce no effect?

5. The page says: “If they guess slightly wrong, the tongue catches a weak object, and the object breaks or moves unexpectedly.” How is a weak anchor determined in the rules, and what are the allowed outcomes when it breaks, slips, or moves?

### Pitcher

1. A crafted place completes when the frog reaches the place’s authored endpoint: the next perch, drain outlet, roofline, lily pad, or rooftop pond. The endpoint itself is the completion condition. No collecting, switches, or hidden objectives are required. If the frog reaches it by any authored route, the place ends and the next place begins. The game completes when the final moonlit rooftop pond is reached; after that the frog joins the calling chorus and the game ends.

2. A last safe perch is the most recent authored perch where the frog stood safely for a beat: a stable ledge, branch, barrel rim, tile, or bank that is not moving, submerged, in a current, or actively hazard-triggered. It is not the nearest random object. If the frog falls out of the authored space, is carried by a current to a dead end, or is returned by a hazard, it reappears at that last safe perch. If no reachable perch exists, the game places it at the nearest authored safe bank or checkpoint for that hazard, or at the place’s opening perch if needed. “Coughed up nearby” means the nearest safe perch that will not drop the frog back into the same hazard.

3. Eating is the short form of the same tongue action. A quick snap sends the tongue out for an instant; if it touches an edible insect, it catches and swallows it, then retracts. A held extension sends the tongue out and checks for grabbable anchors; if it touches one, it sticks and enters the attached pull/swing state. Insects are never anchors. The distinction is input length and contact class: short snap eats edible insects, held extension grabs anchors. A short snap cannot stick to an anchor, and a held extension does not become an eating action.

4. Flies and ordinary insects are flavor. Eating them may cause a cosmetic swallow, sneeze, or small animation, but they produce no traversal effect. A wasp is an authored interactive hazard/tool. Eating a wasp reliably causes a puff: the frog hiccups, puffs, and performs one involuntary small hop or altered arc. That effect can be planned around only where the wasp is placed as part of a route or puzzle. If an insect is not authored as an interactive object, it produces no mechanical effect.

5. Weak anchors are authored anchors tagged weak. They are always placed by the level, never random. They are identified by visual cues: cracked, frayed, waterlogged, loose, hanging by one thread, discolored, or swaying differently from stable anchors. They are grabbable, but they have a stress limit. If the player hangs too long, pulls the wrong way, or loads them unexpectedly, the allowed outcomes are slip, break, or move. Slip: the tongue catches, holds briefly, then slides off, leaving the frog dangling before it falls. Break: the anchor snaps away or falls, the tongue detaches, and the frog drops unless it catches another anchor. Move: the anchor shifts or swings while still attached, changing the route; if it moves past its limit, it breaks or slips.

## Round 3

### Interrogator

CRACKS
- The page and the ruled tongue action disagree about what release does. The page says: “Releasing lets the frog swing.” The ruling says: “While held, the frog is attached and can pull or swing. Release detaches it and keeps the momentum.” A builder cannot build one action from both.
- The page and the ruled eating/anchor classes disagree about insect parts as anchors. The page lists tongue-catchable things including “the legs of insects.” The ruling says: “Insects are never anchors.” A builder cannot know whether an insect leg can be grabbed with the tongue.
- The page names surfaces that sink, tip, and crumble but gives no rule for when they change, what the player can do to make them change, or what happens when the frog is on them at the moment they change: “Leaves sink. Rain barrels tip.” and “a crumbling ledge.”
- The page says a rooftop hazard changes the hop’s arc but gives no rule for what that hazard is, how the player knows it is present, or how the player can respond: “A rooftop has wind that changes the arc of a hop, so the player must use the tongue to anchor before jumping.”
- The page lists a hazard that is not otherwise ruled: “a fish that snaps.” A builder cannot know how the fish behaves, how the player detects it, or what happens when it snaps.

QUESTIONS
1. The page says: “Releasing lets the frog swing.” Your answer says: “While held, the frog is attached and can pull or swing. Release detaches it and keeps the momentum.” Which of these is the game?

2. The page says the tongue catches: “the legs of insects.” Your answer says: “Insects are never anchors.” Which is the game?

3. The page says: “Leaves sink. Rain barrels tip.” and lists “a crumbling ledge.” What decides when one of these surfaces changes, what can the player do to make it change or prevent it, and what happens when the frog is on it at the moment it changes?

4. The page says: “A rooftop has wind that changes the arc of a hop, so the player must use the tongue to anchor before jumping.” What is wind in the rules, how does the player know it is present, and what can the player do about it?

5. The page lists: “a fish that snaps.” What does the fish do, how does the player know it is a threat, and what happens when it snaps?

### Pitcher

1. The game is the held action: holding the tongue attaches the frog to an anchor, and while attached the player can pull or swing. Release detaches the frog and keeps its momentum. The page line “Releasing lets the frog swing” is not the game.

2. The game is: insects are never anchors. “Legs of insects” is not on the anchor list. A tongue snap can eat an insect, but a held extension cannot use an insect as a grab point.

3. These surfaces are authored dynamic objects with visible stress cues. A leaf bends under sustained weight or repeated hops; when its bend limit is reached, it sinks and drops the frog unless the frog is attached. A rain barrel tips when weight crosses its tipping point, when the frog lands on the wrong side, or when the player knocks or pushes it; it rotates, sliding the frog off or carrying it. A crumbling ledge cracks on the first load and breaks on the second load or under sustained weight; the player can avoid or delay it by not landing, hopping lightly, or anchoring the tongue to offload the ledge. If it changes while the frog is on it, the surface stops being solid: the frog slides, falls, or is carried by the moving object unless the tongue catches another anchor.

4. Wind is an authored horizontal force zone on rooftops. It is shown by flags, swaying plants, drifting rain, dust, ripples, and audio. It pushes the frog while airborne and can shove a crouched frog if the frog is exposed. The player can wait out a gust, anchor with the tongue, take a lower or covered route, or time the jump with or against the wind.

5. A fish is a water hazard that lurks in ponds and koi pools. The player knows it is present from ripples, bubbles, disturbed lily pads, and the fish’s shape under the surface. It snaps when the frog enters the water, splashes, or moves within its strike radius. If it snaps, the fish grabs the frog, dunkes it, and spits it onto the nearest safe bank; if no bank is reachable, the frog returns to the last safe perch or nearest authored safe edge. It ignores a still frog on a bank or a frog under cover.

## Round 4

### Interrogator

CRACKS
- The page says “pudles that turn into platforms,” and “If the frog gets into water, it can swim, but poorly, and it must haul itself onto the nearest edge,” but it does not say what being in water or a puddle does to the frog, what swimming allows, or how the frog exits.
- The page says “Water carries the player in currents but also slows them down,” “pull a cork from a pipe so water begins to flow and carries a leaf into place,” “Drainpipes gurgle and spit,” and lists “a current that carries the frog away,” but it does not say how flows and currents move the frog or objects, when they begin, change, or stop.
- The page says “A sprinkler can start without warning, turning a ledge into a slide,” and “start a sprinkler to knock a caterpillar off a branch,” but it does not say what spray does to surfaces, objects, or the frog, or what ends it.

QUESTIONS
1. The page says: “pudles that turn into platforms.” and “If the frog gets into water, it can swim, but poorly, and it must haul itself onto the nearest edge.” What are the rules for puddles, still water, swimming, and getting out: when can water be a surface, what does it do to the frog, and how does the frog leave it?

2. The page says: “Water carries the player in currents but also slows them down,” “pull a cork from a pipe so water begins to flow and carries a leaf into place,” “Drainpipes gurgle and spit,” and lists “a current that carries the frog away.” What do currents and flows do to the frog and objects, and what rules decide when they begin, change, or stop?

3. The page says: “A sprinkler can start without warning, turning a ledge into a slide.” and “start a sprinkler to knock a caterpillar off a branch so the branch dips lower”. What does sprinkler spray do to surfaces, objects, and the frog, and what ends its effect?

### Pitcher

1. A puddle turns into a platform only when it raises an authored floatable into place, or when it is shallow enough that the bottom is the platform. The water is not the platform; the bottom, leaf, cork, or tin lid is. If the frog enters deeper still water, it sinks and swims poorly: it can paddle, but it cannot jump from the water and strong water pushes it. To leave, it paddles until its front paws catch an authored edge, then hauls itself up. If no edge is reachable, the current carries it to the nearest safe bank, or it returns to the last safe perch.

2. Currents and flows are authored directional water fields. Still water only slows; a current carries when its flow is stronger than the frog’s swim. The frog can fight weak flow but is swept by strong flow unless it reaches an edge or anchors. Floatables are carried, collide, and become temporary platforms when they lodge. A flow begins when a physical source crosses a visible threshold—cork pulled, pipe unblocked, rain fills a basin, drainpipe pressure builds—and changes when the channel, water level, or obstruction changes. It stops when the source closes, the water drains below threshold, or the place resets.

3. Sprinkler spray is an authored water source. It wets surfaces in its visible cone; if the surface is smooth or can hold a running film, it becomes a slick slide and the frog cannot grip it, while porous textured surfaces only become damp unless continuous spray washes their grip away. Spray can knock loose small objects and creatures, push floatables, fill basins, and start currents. If the frog is hit by spray, it is pushed and its next move is made from a wet surface; it does not take damage. The spray ends when its pressure cycle ends, the player interrupts the feed, or the water drains; the wet effect remains until the water recedes, dries, or the place resets.

## Round 5

### Interrogator

CRACKS
- The core crouch-and-hop verb is named but not ruled. The page says the frog crouches, releases, and launches in an arc, and says the frog cannot run or correct a bad hop, but it does not say how aim is chosen, how the launch is determined, or what states the frog can or cannot change after leaving the ground.
- The page depends on the player changing the world through physical consequences, but it does not rule how the frog makes those changes. It names pulling a cork, hitting a clamp, disturbing a branch, and splashing near a sensor, but not what makes an object respond or what the frog can and cannot affect.
- Hollow landmarks are treated as traversal places, but their rules are missing. The page says a rain barrel can be entered, climbed, and exited through a drain, and lists drainpipes, tin cans, and cat doors, but does not say what it means for the frog to enter or move inside such objects.
- Lily pads and other floatable platforms are named as traversal surfaces, but their behavior is not ruled. The page says the frog can hop across lily pads and that puddles can turn into platforms, but not whether these surfaces drift, sink, hold the frog, respond to currents, or become unsafe.
- Eating a wasp is named as a special traversal effect, but its movement rule is not specified. The page says it makes the frog dizzy and causes a strange sideways hop, but not when that happens, what movement state it changes, whether the player can aim it, or what happens if it causes a bad result.

QUESTIONS
1. The page says: “Hold a control and the frog crouches, its legs coiling; release and it launches in an arc.” It also says: “The frog cannot run, so it cannot correct a bad hop by accelerating away. Its jumps are arcs, and once it leaves the ground it must live with the result.” What are the rules for crouching, aiming, releasing, and what happens after the frog leaves the ground?

2. The page says: “The world is not made of locked doors or switches. It is made of small physical consequences.” It also says: “start a sprinkler to knock a caterpillar off a branch so the branch dips lower; pull a cork from a pipe so water begins to flow and carries a leaf into place.” How does the frog change an object’s state, and what makes an object respond to that change?

3. The page says: “A rain barrel can be entered through a broken window, climbed by sticky tiles, exited through a drain.” It also lists landmarks such as “rain barrels, lily pads, drainpipes, tin cans, garden hoses, greenhouse glass, mossy stones, wooden fence rails, hanging vines, spider webs, koi ponds, cat doors, sprinklers, and rooftop ponds.” What are the rules for a frog entering, being inside, climbing, and exiting hollow landmarks or containers?

4. The page says: “A garden path can be crossed by hopping across lily pads.” It also says: “puddles that turn into platforms.” What are lily pads and other floatable platforms in the rules: how do they support the frog, how do they move, sink, or become unsafe?

5. The page says: “eat a wasp and get dizzy, causing a weird but useful sideways hop.” It also says: “Eating a wasp might make the frog hiccup and puff, which can cause a strange hop.” What does this effect do to the frog’s movement, when does it begin, can the player aim or use it, and what happens if it causes a bad landing?

### Pitcher

1. Crouch is a stationary charge. Hold crouch and the frog lowers and coils; it can still be aimed by facing and aim input, but it cannot slide, run, or leave the surface. Release launches an arc from that aim and the crouch charge, up to a fixed cap. Once airborne the frog is ballistic: it cannot air-steer, brake, change aim, or add a second push; only wind, current, or a tongue catch can change the result.

2. The frog changes the world by applying physical force to authored dynamic objects: landing, pushing, pulling or yanking with the tongue, splashing, or disturbing. A cork, clamp, branch, caterpillar, or sensor responds only if it is authored as dynamic and has a visible stress or trigger threshold. When the applied force or wetness crosses that threshold, the object moves, opens, falls, or activates; untagged scenery and too-heavy objects do not respond.

3. Hollow landmarks are real interiors with openings. If an opening is reachable and wide enough, the frog can enter; inside it stands, climbs, crawls, or swims on the interior surfaces, following the same grip and water rules. It exits only through an authored opening: a rim, drain, hole, flap, or gap; a flap opens when pushed or pulled far enough, and a drain is an exit only if the frog reaches the outlet ledge and can hop or cling out. If the object tips, breaks, or fills, the interior behaves physically: the floor tilts, surfaces collapse, or water swims the frog out.

4. Lily pads and floatables are buoyant platforms with load, drag, and stability. They support the frog while their buoyancy exceeds the load and the frog is not hanging from their edge; landing on the edge or staying too long can tilt or sink them. They drift with currents, rotate, collide, and can become temporary platforms when lodged. They become unsafe when current carries them away, load capsizes them, a splash or current destabilizes them, or water drains and they fall; if they fail under the frog, it enters the water unless attached.

5. A wasp is an authored interactive insect. A quick snap that swallows it sets a one-shot puff: if grounded, after a short hiccup the frog performs a forced small sideways hop; if airborne, the puff adds a brief sideways impulse to the current arc. The player cannot aim the puff, only plan from the wasp’s placement and the frog’s position. If the puff causes a bad landing, it is treated like any bad hop: the frog falls, gets reset, or is caught by water or hazards, with no extra penalty.

## Round 6

### Interrogator

CRACKS
- Normal ground movement is not ruled. The page says the frog moves right and hops, but does not run, while the ruled crouch is stationary. A builder cannot tell what the frog can do on the ground outside a charged hop: whether it can make short uncharged hops, crawl, walk, stand, change direction, or only idle until crouching.
- Reset rules place the frog, but do not say what happens to the place. The page says the frog is reset to the last safe perch or coughed up nearby, but does not say whether changed objects, currents, wet surfaces, broken weak anchors, tipped barrels, disturbed branches, eaten wasps, or animal attention persist, reset, or restore selectively. A builder cannot know whether failure can soft-lock a place.
- The page presents verbs as discovered or learned: tongue after a fly, sticky pads after a wall, swinging after a branch. It does not say whether these actions are available from the first minute and only taught in order, or become available after authored discoveries.
- “Drainpipes gurgle and spit” is named as behavior, but not made into a rule. A builder cannot tell whether this is a current, spray, push, ejected object, hazard trigger, or only flavor, nor what starts and stops it or how the frog can respond.

QUESTIONS
1. The page says: “The player moves to the right; the frog hops. It does not run. Hold a control and the frog crouches, its legs coiling; release and it launches in an arc.” If crouch is stationary and the frog cannot run, what are the frog’s allowed ground states and movements? Is every ground movement a crouch-release launch, or are there short hops, crawling, walking, standing, or other ground states?

2. The page says: “the frog is reset to the last safe perch” and “the frog is coughed up nearby.” When the frog is reset, what happens to the state of the place? Do changed objects, currents, wet surfaces, broken anchors, tipped barrels, eaten wasps, disturbed branches, and animal attention persist, reset, or restore selectively? If consequences persist, what prevents an unrecoverable soft lock?

3. The page says: “A fly passes nearby. The player discovers the tongue.” and “When the frog lands on it, its sticky pads catch.” Are the tongue and climbing actions available from the start and only taught in order, or do they become available after authored discoveries? What marks an ability as available to the player?

4. The page says: “Drainpipes gurgle and spit.” What is a drainpipe gurlgle/spit in the rules? What does it do to the frog, objects, surfaces, or currents; what starts and stops it; and what can the player do about it?

### Pitcher

1. On ordinary ground the frog has only standing, aiming/facing, crouch-charging, and launching. Tap crouch gives a minimal short hop; hold crouch gives a longer aimed arc. It cannot run, walk, slide, or crawl on ordinary ground. Facing/aim input changes where it will launch but does not move it. Once airborne it is ballistic: no air steering, braking, or second push, except wind, current, or a tongue catch.

2. Reset restores the place to the authored checkpoint state stored at the last safe perch. Dynamic state created after that checkpoint returns: weak anchors unbreak, tipped barrels upright, currents return to their source state, wet surfaces reset to the checkpoint’s authored wetness, animals return to default attention/patrol, and disturbed branches, corks, or eaten wasps re-form. If a change was part of reaching a new safe perch, it becomes part of that new checkpoint. If no reachable perch exists, the frog returns to the nearest authored safe bank or the place start. This prevents soft lock because every checkpoint is authored reachable and failure does not leave a permanently broken world.

3. All core verbs are available from the start. The opening fly, wall, and branch are authored teaching moments, not unlocks. Availability is marked by the player’s input and the world’s physical tags: if a surface is gripable, the pads catch; if a thing is an anchor, the tongue can catch it. Nothing is locked behind discovery.

4. A drainpipe gurgle is the telegraph of pressure building behind a partial blockage: bubbles, vibration, wetness at the pipe mouth. It ends when pressure reaches threshold and the pipe spits: a short water/air pulse that wets nearby surfaces, pushes light objects, can knock loose debris, and may create a brief current. The pulse stops when pressure releases or water drains below threshold. The player can wait, stand outside the mouth, anchor, or use the spit to move or clear objects.
