# The interview

## Round 1

### Interrogator

## CRACKS

- The heron threat is named as a core system, but the rules for noticing, warning, seeing, and hiding are not specified.
- “Last safe ledge” and “nearest safe edge” are used as failure/reset points, but nothing says what makes a ledge or edge safe or how those points are chosen.
- Hazards are said to “hurt on touch,” but the actual consequence of a hazard hit is left unclear and described only as costing “the line” or bouncing the frog “out of the route.”
- Specific hazards are named with behavior words—“open and shut,” “snag a bad landing,” “slick oil patches”—without saying what those behaviors do to the player or the world.
- Deep water and current are described as a non-death setback, but the rules for being carried, escaping, and what counts as a safe place to be washed into are missing.
- The time cycle is central, but the page does not say what advances it, what stages it has, or what causes the marsh to change.
- Night changes such as rising water, sinking/rising pads, and harder-to-see oil are named, but their rules and effects on the player are not defined.
- Moonflies are collectibles, but the page does not say what collecting one actually reveals, whether the effect is permanent, or how it relates to the time cycle’s claim that hidden paths “become clearer.”
- The page says moonflies are “not needed to finish,” but also says they can open a hidden route or shortcut, without saying whether that route changes progression, is optional, can be blocked, or is ever required.
- “Tilting lily pads” are named as a particular part of the game, but no rule explains what tilting means or how the frog interacts with it.
- “Committed hops” and “move in bursts, then stop, then move again” are presented as player behavior, but the page does not say what game rule creates or enforces that behavior.

## QUESTIONS

1. When a heron “notice[s] the frog,” what in the game makes that notice happen, what makes a heron’s “sight lines … readable,” what later makes “their shadows become harder to see,” and what exactly counts as getting “under a pad or flatten[ing] behind a reed” during the warning?

2. What makes a ledge or edge “safe,” how is the “last safe ledge” chosen after a heron dive or after being washed by current, and what happens if the nearest “safe edge” is not actually safe?

3. What exactly happens when the frog touches a hazard: what is “the line” that is costed, what does it mean to be “bounced out of the route,” and what is the final consequence of a hazard hit?

4. What do “snapping turtle jaws that open and shut in the shallows,” “sharp reed bundles that snag a bad landing,” and “slick oil patches” do when the frog touches them, lands near them, or moves through them?

5. What does the current do when the frog is in deep water, what counts as the “nearest safe edge” to be washed toward, and what can the player do to escape, be carried, or be harmed while in the water?

6. What advances the time cycle from dusk into night, what begins and ends each stage of the cycle, and what determines the moment “the marsh changes what it asks”?

7. What causes “water rises slightly, some pads sink, others rise, and oil becomes harder to spot,” what happens to the frog if it is on a pad that sinks or rises, and how can the player respond to those changes?

8. Are hidden stepping stones and secret crossings revealed by collecting moonflies, by the time cycle, or by both, and what exactly changes in the world when “their glow reveals hidden stepping stones and secret crossings” or when “the moonflies’ hidden paths become clearer”?

9. If moonflies are “not needed to finish,” what does it mean for them to be “opening a harder, more graceful route through the same marsh,” and can that route ever be required, blocked, lost, or changed by the time cycle?

10. What does a “tilting lily pad” do when the frog lands on it, stands on it, moves from it, or leaves it, and how does that change the platforming challenge?

11. What does it mean for the path across to be “a chain of small committed hops,” and what game rule makes the player “move in bursts, then stop, then move again” instead of allowing continuous movement?

### Pitcher

1. A heron notices when a visibility meter fills. At dusk the sight line is shown as a pale glint across water and reeds, and the meter fills when the frog moves inside that line. Later the glint becomes dimmer and the sight line is still there but harder to read. Getting “under a pad or flatten behind a reed” means the player ducks and places the frog fully behind an occluder or under a low pad so no part is visible; if the frog is hidden before the caw ends, the dive fails, and if not, the dive resets the frog.

2. A ledge or edge is safe when it is solid, dry, outside any active heron sight line, not touching a hazard, and not currently tilting or sinking. The game marks these with faint pale moss. The “last safe ledge” is the most recently occupied safe ledge. After a heron dive, the frog is returned there. If the current would carry the frog to an edge that has become unsafe, that edge is not considered; the game chooses the next nearest safe edge. If no safe edge exists, the current drops the frog at the entry ledge of that pond segment.

3. A hazard hit does not kill. It breaks the player’s current chain of hops through that hazard set and returns the frog to the last safe ledge before the hazard. “Costing the line” means losing the uninterrupted run through that hazard sequence. “Bounced out of the route” means the frog is flung or pushed back to that safe ledge, losing forward progress but not a life.

4. Turtle jaws are timed hazards: when open, touching them causes a hazard hit; when closed, they can be jumped over or stood on until they open. Reed bundles are landing hazards: if the frog’s feet touch one, the landing is rejected and the frog is pushed back to the last safe ledge. Oil slicks are traction hazards: touching one removes control and slides the frog along the slick; if the slide reaches water, the current takes over, and if it would otherwise stop on a ledge, the player has still lost the line and is returned to the last safe ledge.

5. Deep water has no foothold. The frog can turn and paddle weakly but cannot jump until it reaches an edge. The current follows visible ripples and carries the frog toward the nearest safe edge. The player can steer slightly toward that edge. If the current carries past it, or if no safe edge is available, the frog is deposited at the entry ledge of that pond segment.

6. The time cycle advances in real time while the frog is in play. The level begins at dusk when the player enters the marsh. It then moves through fixed stages: dusk, deep dusk, and night. Each stage begins when the clock reaches its threshold and ends when the next threshold is reached. The moment “the marsh changes what it asks” is exactly one of these stage boundaries, marked by a shift in light.

7. The stage update directly changes world states. Water rises by raising the water line around low ledges. Some pads sink by lowering into the water; others rise by lifting into a new reachable position. If the frog is on a pad that sinks, it falls into the water and the current takes it. If a pad rises, it may create a new crossing or expose the frog to a heron sight line. Oil keeps the same collision and behavior, but its visual contrast is reduced. The player must move before the boundary, avoid becoming stranded, or use the new raised path.

8. Collecting a moonfly permanently reveals one hidden route: its associated stepping stones or secret crossing become visible as a faint glow. The time cycle does not reveal new routes on its own; it only makes already revealed routes easier to see and follow. So moonflies give the information, and the time cycle increases its visibility.

9. The moonfly route is optional. It is an alternate, harder crossing through the same marsh, not required to finish. The normal route always remains available. The time cycle can block it, make it harder, or temporarily remove it by sinking stones, raising water, or changing sight lines, but it never becomes mandatory.

10. A tilting lily pad leans toward the frog’s weight and movement. Landing off-center starts a tilt; standing still off-center increases it; moving across it changes the tilt in the direction of movement. If the tilt becomes too steep, the frog slides into the water and the current takes it. The player can counterbalance by moving opposite the tilt or jump before it becomes too steep. This changes the platforming challenge from simply landing on a pad to balancing, timing, and choosing where to land.

11. “Committed hops” means each gap is placed so it requires one deliberate jump with no extra movement option to rescue a bad takeoff. Continuous movement is allowed, but the heron detection system punishes it: moving inside a sight line fills the notice meter, so the player must stop, hide, or move only when safe. Lily pads also tilt under continuous movement, so the game encourages bursts of movement followed by stillness.

## Round 2

### Interrogator

## CRACKS

- The page makes stillness and hiding the core of the stealth part, but it does not say what happens to the heron’s notice state when the frog stops, leaves a sight line, re-enters a sight line, or survives a warning. A builder cannot make the loop work without knowing whether stopping reduces danger, preserves danger, or only works after a full reset.

- The page says the time cycle runs from dusk into night and also says the marsh is “always in the middle of changing,” but it does not say what happens after night is reached, whether the cycle stops, loops, continues, or what begins and ends the overall cycle.

- The page says deep water “washes the frog back toward the nearest safe edge,” but it does not say whether the frog is vulnerable to hazards or herons while being carried, whether the current can be interrupted, or what happens if the chosen safe edge becomes unsafe before the frog arrives.

## QUESTIONS

1. The page says the player must be “staying still and staying out of sight while something is actively looking,” and that “if the player does not get under a pad or flatten behind a reed, the heron dives.” What happens to the heron’s notice while the frog moves, stops, hides, leaves a sight line, re-enters a sight line, or survives a warning?

2. The page says “The time cycle runs from dusk into night” but also says “the marsh is always in the middle of changing.” Does the cycle stop at night, loop, continue changing, or end in some other way, and what begins and ends the overall cycle?

3. The page says “the current washes the frog back toward the nearest safe edge.” While the frog is being carried by the current, what can affect the frog, and what happens if the current passes through hazards, enters a heron’s sight line, or reaches an edge that is no longer safe?

### Pitcher

1. A heron’s notice is a meter. It fills only when the frog moves inside a sight line. If the frog stops inside that sight line, the meter stops filling but does not drain; the danger remains at whatever level it reached. If the frog fully hides or leaves the sight line, the meter drains. If it drains before the warning, nothing happens. If the warning has begun, the frog may still move, but it must be fully hidden before the dive; if it is, the heron aborts, the meter resets, and the frog is not punished. If the frog re-enters a sight line while the meter is still active, it begins filling again; if it re-enters or fails to hide during the warning, the dive happens.

2. The cycle does not stop at night and does not loop back to dusk. It runs once through the crossing: dusk, deep dusk, night. After the night boundary, night itself keeps changing continuously—water rises further, pads continue to sink or rise, and oil stays hard to see—so the marsh remains in the middle of change. The overall cycle begins when the frog enters the marsh, and it ends when the crossing ends, either by reaching the old nursery pool or by leaving that pond segment.

3. While the frog is being carried by current, it is in a transport state, not a normal play state. The frog cannot jump, can steer only weakly toward the intended safe edge, and cannot be affected by hazards or herons while the current carries it. Hazards are passed through without triggering. Heron sight lines do not fill notice or trigger dives. If the intended safe edge becomes unsafe before arrival, the current abandons it and selects the next nearest safe edge; if no safe edge exists, it deposits the frog at the entry ledge of that pond segment.

## Round 3

### Interrogator

## CRACKS

- The page says there are multiple herons and that the player learns their patterns, but it does not say how more than one heron scans the marsh, whether their sight lines move, or what happens when multiple herons notice or warn at the same time.
- The page uses “last safe ledge” as a reset point, but the time cycle and hazards can make a ledge no longer safe; it does not say what happens when the game tries to reset the frog to a ledge that has become unsafe.

## QUESTIONS

1. The page says “Herons stand at the far end of the pond and scan for movement” and “The player learns heron patterns.” How do multiple herons work in the game: do they stay fixed or move, do their sight lines move, and what happens when more than one heron notices, warns, or dives at once?

2. The page says “the heron dives and the frog is knocked back to the last safe ledge” and “A hazard hit bounces them out of the route.” If the last safe ledge or the place the game would return the frog to is no longer safe at the moment of reset, what happens?

### Pitcher

1. Herons do not walk around the pond. Each heron is fixed to its perch at the far side; what moves is its head and the sight line it casts, which sweeps through a learnable arc. Each heron has its own notice meter. If one heron’s meter fills, that one begins the warning. If another heron would also fill while that warning is live, it is suppressed: the first warning is the one that matters. If the frog is not hidden, that one heron dives, and all active warnings in that pond segment are cleared and reset. If two fill at the same instant, the one whose sight line is closest to the frog triggers, and the others reset. If the frog hides or leaves all sight lines before any warning resolves, every active notice meter drains to zero.

2. The game does not blindly return the frog to a ledge that has become unsafe. When a heron dive or hazard hit would reset the frog, it first checks the last safe ledge. If that ledge is still safe, it uses it. If it is no longer safe, the game searches backward along the path the frog came from and uses the nearest ledge that is currently safe. If there is no such ledge, it returns the frog to the entry ledge of that pond segment; that entry ledge is kept dry, hazard-free, and outside active heron sight lines. The frog is never dropped into water, onto a tilting pad, inside a hazard, or directly under a live heron sight line.

## Round 4

### Interrogator

## CRACKS

- The page says “Falling into deep water is not instant death,” but it also mentions “the shallows” and “water rises.” It does not say what happens if the frog falls into water that is not deep, or what rule decides which water is deep.
- The page says “water rises slightly” and “some pads sink, others rise,” but it does not say what happens when rising water reaches a surface the frog is currently standing on, or when a surface becomes unsafe while the frog is on it.

## QUESTIONS

1. The page says “Falling into deep water is not instant death” and also refers to “the shallows” and “water rises.” What happens when the frog falls into water that is not deep, and what rule decides which water is deep?

2. The page says “water rises slightly” and “some pads sink, others rise.” If rising water reaches a ledge, log, stone, or other surface the frog is currently standing on, or if that surface becomes unsafe while the frog is on it, what happens to the frog and how is it resolved?

### Pitcher

1. Water is split by a functional depth value. A pool is shallow if its bottom is within the frog’s maximum jump height from the water surface; it is deep if the bottom is below that. Falling into shallow water is a failed landing but not a current event: the frog lands on the bottom, can turn, and can jump out to a nearby safe edge or platform. Falling into deep water starts the carried state. If rising water makes a previously shallow pool deep, the next fall into it uses the deep-water rule.

2. Rising water does not drown the frog. At each stage boundary, any surface whose top is below the water line becomes submerged and is removed from the safe-surface list. If the frog is standing on such a surface when that happens, it loses footing and falls into the water at that spot. Then the depth rule applies: shallow water lets the frog land and jump out; deep water starts the current. Sinking pads and over-tilted pads are resolved the same way: the surface stops being a footing, and the frog is dropped into water. If the water there is shallow, the frog can exit; if it is deep, the current carries it to the nearest safe edge, using the same fallback to the segment entry ledge if no safe edge exists. A surface becoming unsafe only because a heron sight line moves onto it does not move the frog; it only makes notice possible.

## Round 5

### Interrogator

INTERVIEW OVER
