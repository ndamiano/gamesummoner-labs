# CADENCE

*A roguelike with one button. What you do is decided by how fast you press it.*

Working title: **CADENCE** (alternates: *Pulsewalk*, *One Rhythm*, *Metronome*)
One-line pitch: a grid-based dungeon crawler played with a single input, where the
**frequency of your presses** is the whole verb set — one tap walks, a quick double
cuts, a hold turns, a hold-your-ground pause defends.

---

## 1. Design thesis

Most one-button games hide the verb behind context ("press to do the only sensible
thing"). CADENCE does the opposite: **the input itself carries the meaning**, through
its timing. This has three consequences we are designing for:

1. **Your body state becomes game state.** A panicked player mashes and fights
   aggressively and sloppily. A calm player ticks slowly and plays carefully. The
   controller is a proxy for your pulse, and the game can see it.
2. **Stillness is a verb.** Clicking means moving, and moving means attacking. Not
   clicking is *bracing* — defending, listening, waiting. The default input (doing
   nothing) is a legal, useful action, which makes the game almost free to operate.
3. **The control scheme is the upgrade tree.** Run progress doesn't only give you
   damage and items; it gives you *new meanings for the button*. A build is a
   different click grammar.

Everything below follows from those three.

**Non-goals:** no analog stick, no second button, no modifiers, no drag. One physical
input (mouse left, Space, gamepad A, or a single switch). Menus use the same button.

---

## 2. The input grammar

A **burst** is the unit of input: every press, plus the gaps between them, gathered
until the player goes quiet for one *commit window*. A burst is read on two axes:

| Axis | Read from | Maps to |
|---|---|---|
| **Count** | number of presses in the burst | **verb** (step / strike / brace / pivot / dash) |
| **Rate** | median gap between presses | **intensity modifier** (careful / normal / frantic) |

Two axes from one button is the whole depth budget of the game.

### 2.1 Verb ladder (v0)

| Burst | Verb | Effect | Cost |
|---|---|---|---|
| *(no input, 1.5 s)* | **Brace** | +1 Guard on the tile you face; enemies get a free move | free |
| 1 tap | **Step** | move 1 tile in your facing | 1 turn |
| 2 taps | **Strike** | attack the tile in front | 1 turn |
| 3 taps | **Lunge** | attack + hop forward into the vacated tile | 1 turn |
| 4 taps | **Guard** | full guard this turn, reflect 1 hit | 1 turn |
| 5+ taps | **Sprint** | move 3 tiles in a straight line, stopping on contact | 3 turns |
| hold | **Pivot** | rotate facing continuously while held; snaps to 45-degree steps; release commits | 0 (free) |
| hold 2 s | **Rest** | open the menu / end-of-room actions | free |

Pivot being free is load-bearing: without it the game is unsteerable, and with a free
cost it can never be punished, so mis-aiming is never a trap.

### 2.2 Rate modifiers

| Median gap | Tier | Effect |
|---|---|---|
| over 700 ms | **Careful** | -25% damage, +1 Guard afterwards, silent (no aggro) |
| 260-700 ms | **Normal** | as printed |
| under 260 ms | **Frantic** | +30% damage, +1 Aggro, no Guard benefit, cannot be interrupted |

Rate tiers are also what the *game* reacts to (section 8): enemies that punish frantic
play, doors and puzzles that only open to careful ticking.

### 2.3 Thresholds (starting values, all tunable)

| Constant | Value | Notes |
|---|---|---|
| `DEBOUNCE` | 40 ms | below this, a second press is the *same* press |
| `HOLD_START` | 240 ms | press held past this -> pivot begins, step is cancelled |
| `COMMIT_WINDOW` | 260 ms | silence after the last press, then the burst is executed |
| `SLOW_GAP` | 700 ms | a gap this long inside a burst splits it into two bursts |
| `IDLE_WAIT` | 1500 ms | no input -> Brace |
| `REST_HOLD` | 2000 ms | menu |

Worst-case input-to-effect latency is therefore ~`HOLD_START + COMMIT_WINDOW` = ~500 ms,
and ~260 ms for the common single step. That is unacceptable in an action game and
fine in a turn-based one — see the next section, which is why the game is turn-based.

### 2.4 Recogniser state machine

```
            +--------------------------+
            |        IDLE            |<----------------+
            |  (world waits / braces)|                |
            +-----------+------------+                |
             press      |                            | execute verb
                        v                            |
            +--------------------------+             |
            |   PENDING (t=0)         |             |
            |  intent = STEP          |             |
            |  show intent ghost      |             |
            +-----------+-------------+             |
        held 240ms      |        press #2           |
      +-----------------+--------+------------------+|
      v                          v                  |
  +-------------+      +---------------------+      |
  | PIVOTING    |      | PENDING (t=0 reset) |      |
  | rotate while|      | intent = STRIKE     |      |
  | held; free  |      | meter tier = FRANTIC|      |
  +------+------+      +----------+----------+      |
         | release                | 260ms silence   |
         +-----------+------------+---------------->+
                     v
              (facing committed; next press is a new burst)
```

Each additional press within the commit window *escalates the pending intent* rather
than starting a new one. The player watches the intent climb — Step -> Strike -> Lunge
— and can stop climbing by simply stopping. This is the trick that turns input latency
from a bug into a beat: the delay is visible, and it is a window in which the player
can still change their mind.

```python
def on_press(now):
    if now - last_press < DEBOUNCE: return
    if burst is empty:
        start_pending(now, intent=STEP)
    elif now - last_press > SLOW_GAP:
        commit(); start_pending(now, intent=STEP)
    else:
        intent = ladder[min(len(burst), MAX_VERB)]
        show_escalation(intent)
    last_press = now

def on_tick(now):
    if holding and hold_ms > HOLD_START: mode = PIVOT
    if burst and now - last_press > COMMIT_WINDOW: commit()
    if not burst and now - last_action > IDLE_WAIT: brace()
```

### 2.5 Graceful degradation (the most important rule in the document)

Every verb falls back to the safest sensible interpretation when the board makes it
nonsensical:

- Strike with no target in front -> becomes a **Step** into that tile (no turn lost).
- Lunge blocked by a wall -> Strike only.
- Sprint into a closed door -> stop at the last free tile.
- Pivot with nothing to see -> rotate anyway (always allowed).

The single most likely input error in this game is "I clicked twice because I wanted
to walk twice." Making that error *harmless* in normal mode converts the game's worst
frustration into a non-event. Hard mode keeps the whiff for players who want the tax.

---

## 3. Turn-based, deliberately

Execution speed must never be gated by input speed, or the scheme punishes the players
least able to produce fast clean clicks (motor impairments, tremor, older hardware,
touchscreens, one-switch access). So:

- The world advances **only when a verb commits**. Idle is not punished by damage;
  it is Braced, which is defensive.
- Nothing can happen while you are mid-burst. No enemy moves in your commit window.
  Every decision is fully determined and inspectable.
- The dungeon's pace is literally the player's cadence. A fast run is a fast-clicking
  run; a slow, thoughtful run is slow and safe. Both are valid play.

An optional **Live mode** (section 10) adds real-time enemy movement for players who
want the twitch tax, as an explicit difficulty dial rather than the default.

---

## 4. "Forward" — navigation with one axis

You always have a **facing**. The dungeon is a square-tile grid, rendered top-down,
and the camera slowly rotates so your facing is always *up-right* (a soft 20-degree
per-frame rotation, only when facing changes; this keeps "forward" physically felt).

- Step moves along facing. Pivot rotates it for free.
- **Fork rule:** when the corridor ahead branches, the tile previews both branches and
  the *verb selects the branch*: Step takes the well-lit main path, Strike takes the
  dark branch, Guard takes the safe alcove. Decisions with real consequences become a
  click-count question instead of a steering question — the one-input answer to
  "how do I make choices?"
- **Doors, chests, stairs, pickups:** committed by the verb you use on them. Step
  opens a door (it costs a turn — opening is a turn, as in Cogmind or Caves of Qud).
  Strike smashes a lock. Guard on a chest = examine it safely (reveals contents without
  opening; some chests are mimics and only strike reveals that).
- **No diagonal walking.** Facing snaps to 4 (v0) or 8 (v1) directions; keep this
  simple so intent preview is unambiguous.

Design tension to be honest about: with one axis, the spatial puzzle *is* routing and
facing, and rooms must be built so that turning is cheap but positioning matters
(corridors, sightlines, pushable enemies, knockback, "get behind me" geometry). Wide
open rooms are boring under this scheme; bottlenecks are where the game lives.

---

## 5. Legibility — the hard problem

If the player cannot predict what their clicks will do, the design fails. Requirements,
in priority order:

1. **Intent ghost.** The affected tile(s) are highlighted the instant PENDING opens,
   and change shape as the intent escalates. Before any verb resolves, the player has
   already seen the outcome.
2. **Cadence meter** (bottom centre, always on). A short horizontal bar with the
   ladder's rungs on it. Presses light rungs left to right. The current tier
   (Careful/Normal/Frantic) tints it grey / amber / red. It is a metronome face:
   the player's own rhythm, mirrored back — this is the game's signature UI and its
   diegetic "health of your nerve".
3. **Commit flash + distinct per-verb feedback.** Each verb has its own sound, screen
   shake and glyph. A strike must *feel* different from a step even with the audio off.
4. **Turn counter and undo of one verb** in Calm mode (one undo per room, free).
   Learning the grammar should cost nothing.
5. **No hidden thresholds.** Pause > Input shows a live diagram of your own recent
   bursts and where your gaps landed relative to the thresholds; players can see their
   own rhythm and adjust it.
6. **A visual language, not a visual style.** Section 14 is the art direction that serves all
   five above: one palette, one glyph vocabulary, and three redundant channels (shape,
   position, motion) for every state, so legibility never depends on colour or hearing.

### 5.1 Tutorial (first three rooms, no text)

1. Empty corridor, one step of light: any click walks. Nothing else exists.
2. One rat in front of you: one click walks into it (graceful degradation -> bump),
   two clicks kill it. The verb ladder is now understood through the body.
3. A wall to the left with a gap: holding rotates; the first click after rotating walks.
Then a title card: *"You only have one button. How fast you press it is the rest."*

---

## 6. Progression: the grammar is the loot

Items/relics modify the click grammar. This is the deep axis and the reason the
concept sustains a real game rather than a mechanic.

| Relic | Effect on grammar |
|---|---|
| Metronome | Commit window +120 ms (more time to escalate; fewer misclicks) |
| Hair Trigger | Commit window -90 ms, Frantic tier unreachable — fast but brittle |
| Twin Cut | Strike hits both diagonals as well |
| Stutter | Your 3rd press in any burst costs nothing (Lunge becomes free) |
| Hollow Cadence | Careful-tier verbs deal triple damage — slow play becomes the build |
| Drummer | 5-tap Sprint costs 1 turn instead of 3 |
| Iron Rest | Brace instead grants Guard 2 and heals 1 |
| Offbeat | Reverses the ladder: 1 tap = Strike, 2 = Step. Terrifying. |
| Fidget | If you idle twice in a row you automatically Step (removes Bracing) |
| Conductor (relic, late) | Unlocks a 4th axis: press *duration* as modifier |

Because the reward is a control scheme, the same dungeon feels different across runs
for a reason no other genre can claim.

---

## 7. Encounters read your rhythm

Enemies are telegraphed and deterministic, but several archetypes are keyed to cadence:

- **Sentinel** — freezes while you are Careful, flinches at Frantic. Teaches tier choice.
- **Mirror** — copies your last burst's count as its own action count. Mash and it mashes.
- **Tic** — moves one tile per 500 ms of *your* input; you control the clock.
- **Priestess** — immune until you Strike three times at the same tier.
- **Swarm** — aggro scales with total presses in the last 10 s (a panic detector).

Boss idea, "The Drummer": a fight that is a rhythm test — the boss exposes a beat, and
the only window in which its guard breaks is at the same period you can produce with
your own clicks. The whole fight is "match my tempo with your hand."

---

## 8. Run structure

- Run length: 12-18 minutes, 3 floors, ~25 rooms.
- Room types: corridor skirmish, bottleneck, fork (choice via verb), vault (locked,
  needs Strike), shrine (relic, costs a *cadence tax*: e.g. "your next room, your
  commit window is 120 ms"), shop (price is in turns taken, not gold — the currency
  is your pace), nest, exit.
- Death is permanent; the run's **cadence profile** (your histogram of tiers and
  misclicks) is shown at the end, then saved as a personal stat.
- Meta progression: unlock new starting grammars (a "class" is a ladder variant, e.g.
  the Duelist starts with Offbeat; the Warden starts with a longer Commit window).

## 9. Failure modes and mitigations

| Risk | Mitigation |
|---|---|
| Double-click intended as two steps | Graceful degradation (2.5); one undo per room; Sprint for fast movement |
| Input latency feels like lag | PENDING state is always visible; nothing can happen during it |
| Accidental escalation while mashing | Tier is shown before commit; Escalation is opt-out by stopping |
| Tremor / involuntary presses | `DEBOUNCE`, per-player threshold sliders, Assist mode below |
| Grammar gets too big to remember | 6 verbs max on the ladder; everything else is a modifier; pause screen shows your current ladder as a poster |
| "Just click randomly and win" | Random clicking lands in Frantic, which costs Guard and buys aggro; the ladder's cheapest verb is the *slow* one |
| Touchscreen jitter | Same debounce; touch-up used as the press event, not down |

## 10. Accessibility and plumbing

- Any single switch works: mouse, keyboard (Space), gamepad (A), touchscreen, or a
  switch-access adapter. This is a genuinely switch-operable roguelike — say so loudly.
- **Assist mode:** after 1.2 s of stillness a dwell wheel appears at the ladder's
  rungs; a single press selects the rung you are dwelling on. Same one button, no
  timing required at all. This is the fallback that makes the game playable for
  players who cannot produce clean click frequencies, and it costs nothing for
  everyone else.
- Threshold sliders (`COMMIT_WINDOW`, `SLOW_GAP`, `IDLE_WAIT`) with a live
  "practice tile" so the player can feel the change, not read it.
- Full colourblind-safe tier coding (shape + position, not hue), per-verb glyphs,
  and no timing requirement for any *defensive* action.

## 11. Telemetry & tuning

Log every burst: `[t0, deltas[], count, median_gap, tier, verb, target_outcome]`.
- Histogram of inter-click gaps across players -> set thresholds at the natural
  valleys instead of hand-picked ms values.
- Misclick rate = % of verbs immediately followed by an undo or a "no target"
  degradation. Target under 8% by room 5.
- Tier distribution is the difficulty dial's readout: if most players sit in Frantic,
  the ladder's escalation is too greedy.

## 12. Build plan

1. **M1 - feel (1 week).** Terminal/grid prototype, one button, verbs + graceful
   degradation, no art. Only question: does a double click *feel* like a sword?
2. **M2 - legibility (1 week).** Intent ghost, cadence meter, commit flash, tutorial
   rooms 1-3. Only question: can a stranger play room 2 without instructions?
3. **M3 - grammar as content (2 weeks).** 8 relics, 4 enemies, one floor, one boss.
   Kill anything that doesn't change how the button means something.

## 13. Open questions

- Should Pivot be free forever, or cost a turn at higher difficulty? (Free is more
  accessible; costly is more tactical.)
- Is the Rate axis too subtle to teach without a visible metronome? Prototype with and
  without it — if M2 shows players never reaching Careful, cut the axis and go
  count-only.
- Camera rotation to enforce "forward" may cause motion sickness; alternative is a
  fixed north-up map with a very strong facing arrow. Test both in M2.
- Does an Undo-per-room make the game too safe, or is it the thing that makes the
  input learnable at all?

---

## 14. Visual design

*A lantern in a stone room. Everything warm on the screen is you; everything else is the room.*

The visual brief is the input brief in another medium: one channel has to carry everything, so
it must be legible rather than pretty. Three laws follow, and everything below is derived from
them.

1. **Light is the interface.** The dungeon is dark and quiet; the only warm, moving thing on
   screen is the player and their rhythm. Attention is directed by brightness, never by an arrow.
2. **Hue is assigned by meaning, never by decoration.** Warm = you and your cadence. Cool =
   the room's affordances. Violet = the grammar itself. A new room type may reuse a role; it
   may not invent a colour.
3. **Nothing is legible by colour alone.** Every state also has a shape and a position, and
   most have a motion. Not an accessibility add-on: it is why the tier coding survives a
   projector, a greyscale capture, a phone in sunlight and a colourblind player.

**The test applied to every visual decision:** audio off, game in greyscale, 20% brightness,
720p — can you still tell which verb you just committed, and which tile you are about to move
into? If not, it is not a graphics bug, it is a control bug.

**Non-goals for the look:** no painterly environments, no props or environmental storytelling,
no particles, no parallax, no per-room tile variants. The look is deliberately cheap. A game
whose verb set *is* a control scheme cannot also spend its identity on art; the art exists to
make the grammar readable, and it should be possible to swap this look for someone else's
prettier one without touching a mechanic. The shape law (14.2) and the tier coding (14.4) are
the only things that must survive that swap.

### 14.1 Palette

Ten colours, three hue families, never more than five lit in one frame.

| Name | Hex | Role | Never |
|---|---|---|---|
| INK | `#0E1116` | void, everything outside the light | inside a room |
| SLATE | `#1B2129` | unlit floor | in UI |
| (floor near) | `#28313C` | floor inside the lantern: slate + 14% lantern | as a UI fill |
| STONE | `#2C343F` | wall faces, rendered *darker* than the floor | as an accent |
| EDGE | `#39424E` | inactive UI, unlit rungs, frame lines | as a gameplay object |
| ASH | `#8C93A0` | **Careful** tier, secondary text, unaware enemies | combat |
| CHALK | `#E8E4DA` | the player, primary text | anything else at full strength |
| LANTERN | `#E8A33D` | **Normal** tier, light, intent ghost, all intent previews | damage |
| EMBER | `#D4483B` | **Frantic** tier, damage dealt and taken, aggro | decoration |
| TEAL | `#4FA3A5` | the room's verbs: doors, chests, stairs, switches | combat |
| VIOLET | `#7C6BD1` | the grammar: relics, ladder changes, pause accent | the diegetic world |

Violet is the only "impossible" colour in the room: a relic should look like an edit to the
rules, not like a prop. Tier colours are locked to ASH / LANTERN / EMBER and are the only
colours allowed to tint UI chrome: the meter, the ghost and the frames use the same three for
the whole game, in every locale and every difficulty.

### 14.2 The shape law

One rule generates every glyph in the game: **rung *n* of the ladder is a polygon with *n*
sides.** 0 taps is an open ring, 1 a dot, 2 a two-sided lens, 3 a triangle, 4 a square, 5 a
pentagon. The count is literally countable, the ladder reads as increasing complexity, and it
survives greyscale.

The same six shapes are then reused everywhere, without variation: the meter's rungs, the
intent ghost on the floor, the commit flash, the pause poster, the tutorial cards, the icons in
the input diagram, and the sound design's per-verb motifs (one shape, one timbre, one
gesture, 15.3). One vocabulary, learned once.

All glyphs are drawn **screen-aligned** — never rotated with the world, never scaled per
encounter. Minimum glyph size 22 px at 1080p, 15 px at 720p; minimum text size 13 px.

![The shape law and the palette](figures/01_shape_law_and_palette.png)

### 14.3 The world: tiles, light, camera

- **Grid, top-down.** 46 px per tile at 1080p (the character is ~34 px tall; the whole ladder
  fits inside a 1200 px safe area). A room is one screen.
- **Walls are holes, not objects.** A wall face is always *darker* than the floor beside it,
  with a 1 px lit lip on the edges facing the lantern. The room is read as silhouette. No
  texture, no noise, no tile variants: per-room variety costs legibility, and this game cannot
  afford it.
- **One light.** A soft falloff centred on the player, radius ~7 tiles, warm-tinted within 3.
  No shadow casting in v0 — light is a readability device, not a mechanic. If a light mechanic
  ever arrives it must never be able to hide the intent ghost.
- **Camera.** Rotates in a soft ~20 degrees-per-frame eased turn so facing always reads
  up-right (section 4). Everything that is not world geometry — glyphs, labels, the meter, the
  ghost's shape — stays screen-aligned. The facing notch lives on the **player's rim**, not in
  the camera, so the composition is unchanged if the rotation is cut for motion sickness (open
  question 13): the fallback is a fixed north-up grid with the same rim notch. Draw 8 detents
  on the rim and enable 4 in v0, which also settles the 45-degree-versus-4-direction mismatch
  between 2.1 and 4.
- **Enemies** are darker than the tile they stand on, with exactly one bright feature (the eye
  = aggro state). You read them as holes in the light. The brightest thing on screen is always
  you, or the tile you are about to affect.
- **Interactable states** use one colour and stroke patterns: solid teal = openable, dashed
  teal = locked, teal with a violet flicker after a Strike = mimic revealed. No object gets a
  colour of its own.

![Screen composition](figures/04_screen_composition.png)

### 14.4 The cadence meter

The signature element (section 5, item 2). Spec at 1080p: 460 x 74 px, bottom centre, always
on, never covered by any panel — if a panel would cover it, the panel moves.

- Six rungs at fixed positions, drawn with the shape law. Rungs never move or re-order: the
  meter's geography is muscle memory, and re-learning it mid-run taxes the wrong thing.
- A **playhead** sits on the current rung and only ever travels left to right, so a burst
  leaves a visible trace instead of a blinking icon.
- The baseline under the rungs fills to the current rung in the tier colour.
- Frame and behaviour per tier: **Careful** grey, static; **Normal** amber, pulsing at the
  median gap you are actually producing (the metronome face — this is the diegetic part);
  **Frantic** red, frame jittering 3 px. Reduced-motion swaps the jitter for a solid double
  frame, so the tier stays readable without motion.
- **Idle:** at `IDLE_WAIT`, rung 0 lights and the frame breathes once. Bracing must have a
  face, or doing nothing looks like the game has frozen.
- Not on the meter: a timer, a millisecond readout, a combo counter. The numbers live in
  Pause > Input (section 5, item 5), where they are *your* numbers rather than a HUD element.

![Cadence meter, four states](figures/02_cadence_meter.png)

### 14.5 The intent ghost, and drawing one burst

The escalation *is* the animation. While the recogniser is in PENDING the affected tile is
outlined 2 px and filled 16% in the tier colour, holding the glyph of the pending verb; each
added press morphs it to the next rung's shape, and Step / Lunge / Sprint draw a thin ray along
the path they would take. By the time the verb commits the player has already seen the outcome,
which is what turns `COMMIT_WINDOW` latency from lag into a beat.

**Degradations are shown, not hidden.** A Strike with nothing in front draws its ghost, then
morphs to the Step glyph with a small tick reading "as Step". The graceful degradation of 2.5
has to be visible in the ghost, because the ghost is the only place the player is looking at
that moment.

Commit flash: 2 frames, a 4% full-screen lift in the tier colour, plus the verb's glyph fired
from the player. Never a white flash (photosensitivity), never more than 4 px of shake; with
reduced motion both are replaced by the glyph alone.

![One burst, drawn](figures/05_burst_timeline.png)

### 14.6 Verb feedback

Every verb gets its own sound, glyph, light behaviour and duration. The requirement: each row
is identifiable with audio off and the game in greyscale, from glyph and light alone. If two
rows are confusable, one of the two verbs gets redesigned — the same bar as M1's "does a double
click *feel* like a sword", applied to pixels. The Sound column is the short form: section 15 is the
audio design, and the two must not drift apart.

| Verb | Sound | Screen | Light | Duration |
|---|---|---|---|---|
| Brace | low thud, cloth | ring expands from your tile | lantern dims 10% for 6 frames | 150 ms |
| Step | one soft cloth per tile crossed | dust at the destination | none | 120 ms |
| Strike | dry click, hard attack | spike glyph along facing, 2 px shake for 1 frame | 10% flare | 140 ms |
| Lunge | click then scuff, two-tone | double chevron + 3-tile streak | flare | 160 ms |
| Guard | single bell | ring around you, persists to your next turn | none | 180 ms + ring |
| Sprint | three cloths, spaced at your own gaps | fading dot trail along the path | the light travels with you | 3 x 120 ms |
| Pivot | continuous soft scrape | dashed arc guide while held | none | while held |
| Rest | page turn | world desaturates 40%, vignette closes | dims | 200 ms |

### 14.7 Screen layout and the pause poster

The complete persistent HUD: floor and room counter (top left, 15 px), turn counter under it
(13 px, ASH), guard **pips on the player** (not a bar, not a corner), and the cadence meter.
That is all of it, and the list is closed.

- Room names are drawn on the door tile, shop prices on the counter tile, damage as a brief
  glyph on the target. No popups, no floating number columns, nothing that can sit on the tile
  you are about to step into.
- **No minimap in v0.** A room is one screen, the meter owns the bottom of the frame, and a
  minimap is the fastest way to make this game look like every other roguelike.
- Pause > Ladder is the verb set as a poster, in the same column order as the meter — glyph,
  taps, verb, effect, cost — so reading the poster and reading the meter are the same act. It
  is also the tutorial card and the store-page art, drawn by the same code.

![The ladder poster](figures/03_ladder_poster.png)

### 14.8 Motion and pacing

- **Input outranks presentation.** If a burst commits while the previous verb is still
  animating, that animation collapses to its end state. The world never animates ahead of you,
  as in section 3.
- No verb animation longer than 180 ms; turn resolution is skippable by pressing again.
- One easing curve for everything (ease-out, 120 ms) except Pivot, which is linear while held.
- **Nothing idles.** No breathing, bobbing or pulsing on player or enemies. A still world is
  the baseline that makes motion mean *something happened*, and it keeps the screen readable for
  players who take their time reading it.
- Reduced-motion: no shake, no jitter, no pulse. Shape, position and colour carry everything,
  which is exactly what they are already required to carry.

### 14.9 Never-list

Enemy health bars (their telegraph is their shape and the tier they react to) · a player health
bar · blood, debris, sparks · parallax and background art · tile variants for variety · more
than one accent hue per meaning · anything that pulses or floats while the player is idle ·
text that explains what the ghost already showed.

### 14.10 How these figures are made

`figures/make_figures.py` draws every figure in this section, and the motif diagram in 15.3, with
the same primitives, palette and
glyph functions the renderer is meant to use: polygon, ellipse, line — no bitmaps, no licensed
fonts, no hand-drawn art in v0. Keep it that way through M2: if the game cannot be drawn with
those primitives and this palette, the visual design is not finished, it is decorated. Re-run
`python3 figures/make_figures.py` after any change to the palette or the ladder, so the document
and the renderer cannot drift apart.

v0 asset budget: one atlas of ~40 glyph shapes, one 8 px grain dot, one vignette. Everything
else is procedural, including the poster and the tutorial cards.

---

## 15. Sound design

*The room is silent. Everything you hear is you, or something reacting to you.*

The audio brief is the input brief and the visual brief in a third medium, and it inherits their
problem in a sharper form: **the player is the loudest and most frequent sound source in the
game.** A frantic run produces 100-300 presses in fifteen minutes, and every one of them already
has a sound. So the hard problem here is not atmosphere, it is self-masking: the game has to stay
audible *through* the sound of the player's own hand. Three laws, the same three as 14:

1. **The player is the soundtrack.** There is no score to keep time with. The only rhythmic
   element in the game is the player's own cadence, sounded back at them (15.4).
2. **Timbre is assigned by meaning, never by decoration.** Dry transients are you and your verbs.
   Resonant, room-sourced sound is the room's affordances. One impossible, purely synthesised
   family is the grammar itself: relics, ladder edits, an Offbeat reversal. A new room type may
   reuse a family; it may not invent one.
3. **Nothing is legible by sound alone.** Every cue below already has a drawn equivalent in
   section 14. Audio is a redundant channel by construction: never the only carrier, and no
   mechanic may require hearing it.

**The test applied to every audio decision:** sound on, picture at 20% brightness — can you tell
which verb you just committed, at what tier, and whether the room noticed? And the half of the
test that decides whether a cue is a control cue rather than decoration: with the audio off, is
anything lost *but pleasure*? If actual information is missing, the cue must be drawn (14.6)
before it is allowed to be heard.

**Non-goals for the sound:** no adaptive or layered score, no licensed sample library, no ambient
loops, no foley variety, no voice or barks, no UI whooshes, no sonar pings, no reverb used to
make a cue pleasant instead of identifiable. Like the look, the sound is deliberately cheap and
generated from primitives (15.9). It exists to make the grammar audible, and it should be possible
to swap this audio design for someone else's better one without touching a mechanic. The voice
budget (15.2) and the identity rule (15.3) are the only things that must survive that swap.

### 15.1 The masking problem — the hard problem

Everything else in this section is ordinary game audio. These five rules are what makes it a
CADENCE soundtrack, and they are all consequences of the input design:

1. **The switch sound and the verb sound are separate channels.** A press makes a **tick**: 12 ms,
   band-limited, fixed level, identical on every device, never tiered, never pitched, never panned.
   It says "the switch registered" and nothing else. Its emptiness is deliberate: it is the only
   sound allowed to repeat five times a second, and a sound that repeats that often cannot carry
   information — it can only carry rhythm. The verb's sound arrives at commit, ~260 ms later, and
   is the only thing permitted to change character. Two messages, two channels: *it registered*,
   and *here is what it meant*. Merging them buries both.
2. **While you are still deciding, the gaps between the ticks are the tier.** The intent ghost is
   silent on purpose (15.8). During PENDING the only audio is your own ticks, whose spacing is
   exactly what the meter is showing (14.4). Sounding the escalation would put the game's voice
   inside the player's hesitation, and an abandoned burst would be audible as a commitment.
3. **One event owns the mix.** The committed verb owns the mix for its duration (14.6); anything
   else that would sound in that window ducks 6 dB, and if it still collides it is dropped — with
   its visual equivalent kept. Input outranks presentation (14.8), so a collapsed animation
   collapses its sound too: tails are ducked, never hard-cut, because an abrupt cut is itself an
   audible event and would be heard as a verb that did not happen.
4. **Silence is the loudest cue.** The ambience floor is a room tone at the edge of hearing.
   Aggro, an unseen enemy, the Swarm's panic meter (7) and the Careful tier are heard as *changes
   in that floor*, not as added effects. This is "light is the interface" in another medium: what
   matters is what the dark stops doing.
5. **The player's rhythm must never be contradicted by the game.** Nothing in the mix is metrical
   except what the player produced (15.4). If the game had a beat, the player's hand would be
   either in time with it or wrong, and this game does not judge tempo.

### 15.2 Nine sources, three families

Mirroring 14.1: a closed list, three families — **you**, **the room**, **the grammar** — plus the
switch, which belongs to no family. Never more than three of them sounding in one frame; the tick
is listed for completeness and does not count against that limit, because it is not a game sound,
it is the controller.

| Source | Family | Role | Never |
|---|---|---|---|
| TICK | (switch) | 12 ms band-limited click: the press registered | carrying meaning; being ducked |
| CLOTH | you | soft filtered noise: movement — Step, Sprint, Lunge tail | attacks |
| CLICK | you | dry wood transient: Strike, the head of a Lunge | ambience |
| BELL | you | struck metal, long tail: Guard, and only Guard | anything else |
| THUD | room | low sine under cloth: Brace, damage taken | decoration |
| SCRAPE | you | sustained filtered noise: Pivot, while held | staccato |
| PAGE | you | paper transient plus a short filter sweep: Rest, menus | combat |
| ROOMTONE | room | 20 s generated bed, filtered per room: the presence of a space | any rhythmic content |
| GRAMMAR | grammar | two detuned sines with a slow beat: relics, ladder edits | anything diegetic |

GRAMMAR is the audio VIOLET: the only sound in the game with no physical model, because a relic is
an edit to the rules and not a prop. It is also the loudest thing in the game (15.6), and it is
always alone.

**Tier treatment is locked to three, for the whole game** — the audio of ASH / LANTERN / EMBER, and
always a *treatment* of the same source, never a different source:

| Tier | Treatment | Why |
|---|---|---|
| **Careful** | low-passed 1.8 kHz, attack +8 ms softer, no tail, -6 dB | 2.2's "silent, no aggro" made audible |
| **Normal** | as printed | |
| **Frantic** | +2 semitones, harder transient, tail +40%, +3 dB | the same verb, heard as panic |

And the rule that keeps the mix from becoming a wall: **pitch and filter carry the tier; family and
envelope carry the verb.** A Strike must still be a Strike at any tier, exactly as a lens must
still read as a lens in greyscale (14.2). Any cue identifiable by pitch alone is a tier cue
wearing a verb's clothes.

### 15.3 The shape law, heard

14.2 promises one shape, one timbre, one gesture per verb. The timbre is the family above. The
gesture is the envelope, and it has three values, one rule each:

- **falling** — fast attack, decaying tail: you acting on the room. Every verb.
- **rising** — slow attack, energy arriving: the room acting on you. Enemy moves, doors, damage.
- **sustained** — while held: an ongoing state. Pivot, Guard's ring, Rest.

Brace is the single exception to *falling*: it is you acting on yourself, so it rises before it
falls. One exception, stated once, so nobody designs it back in by accident.

So the first thing a sound tells you is *who caused it*, before you hear what it is. That is the
audio version of "walls are holes, not objects": one rule that makes the whole mix parseable.

**Grain count: the number of grains equals the number of things the verb does.** Step crosses one
tile, one cloth. Sprint crosses three, three cloths spaced at your own gaps. Strike is click plus
contact, two grains. Brace does nothing, so it has no grains at all — one low swell. Grains closer
than 80 ms merge into one grain plus a tail: that is the auditory streaming limit, not a style
choice, and it is why a Frantic burst blurs. At five presses a second a count is noise.

![Verb motifs, drawn](figures/06_verb_motifs.png)

| Verb | Family | Grains | Gesture | Identity (the thing no tier may take away) |
|---|---|---|---|---|
| Brace | THUD + CLOTH | 0 | sustained, 150 ms, rising-then-falling | the only sound below 200 Hz |
| Step | CLOTH | 1 per tile crossed | falling, 90 ms | no attack transient, ever |
| Strike | CLICK | 2 | falling, hard attack | the only dry wood transient |
| Lunge | CLICK then CLOTH | 2, 120 ms apart | falling | the only two-family pair |
| Guard | BELL | 1, 600 ms tail | sustained | the only struck metal |
| Sprint | CLOTH x3 | = tiles actually crossed, at your own gaps | falling | the spacing is yours, the family is not |
| Pivot | SCRAPE | continuous | while held, linear (14.8) | the only sustained noise |
| Rest | PAGE | 1 | falling plus a downward filter sweep | the only paper |

This is the long form of the Sound column in 14.6; the two must not drift.

**The honest tension:** the shape law counts *intent* (rung n is an n-sided polygon) and the motif
counts *effect* (n grains are n things that happen). They agree for Brace, Step and Strike, and
they diverge for the rest — a Lunge is three rungs on the meter and two sounds, a Guard is four
rungs and one bell. Do not "fix" this. The glyph counts what you asked for; the sound counts what
happened. When a Lunge is blocked by a wall (2.5) the two come apart in exactly the way 14.5 draws:
the ghost climbs to three sides and the sound is one click. Two count-languages, both true, and the
ear cannot reliably count past four anyway.

### 15.4 The score is the player's own rhythm

- **The Drone.** One room-specific drone per floor: a root note, a filtered noise bed, no melody,
  no beat, at -30 dBFS. It changes only with the tier (15.2): Careful opens it and drops it below
  the room tone, Frantic narrows it and lifts it two semitones. Slow play sounds like a quieter
  game — that is the only way the Careful tier can be taught to a player who will never read a
  number.
- **The Pulse.** A soft tick at the median gap you are *actually* producing: the audio face of the
  meter's pulsing frame (14.4). It is derived from your input, so it is always in time with you,
  and it is the one element that makes the metronome diegetic rather than decorative. Slider, not
  a feature; off by default in Calm mode.
- **The only beat that is not yours** is the Drummer boss (7): it plays a period *at* you, and the
  fight is hearing the difference between that period and your own hand. If this game has one
  piece of music, that is it — and it is an enemy, not a soundtrack.
- There is no music stem whose mute removes information: the Drone carries tier and aggro state,
  which are already carried by shape and colour. Muting it costs atmosphere only.

Open question (belongs with 13): does the Pulse teach the tier, or does it turn a turn-based game
into a rhythm game in the player's head? Prototype it silent in M2. If players start matching the
Pulse instead of reading the meter, cut it and keep the drone.

### 15.5 The room heard — sound as the second light

- **Falloff is the lantern's radius** (~7 tiles, 14.3). Nothing is positioned beyond sight: a room
  is one screen, and a sound you cannot see is a sound you cannot act on.
- **The rim doubles as a bearing indicator.** The player's rim already carries the facing detents
  (14.3). Something sounding off-screen flashes a 1-frame **tick on the outside edge of the rim** at
  that bearing — never solid, never in a tier colour, so facing (solid, inside) and hearing (tick,
  outside) cannot be confused. This is the only positional cue in the game, and it is redundant:
  the same event is already readable as shape and eye brightness.
- **Enemies sound like their telegraph** (7). The Mirror plays your last motif back an octave down,
  so you hear yourself in it. The Tic ticks at your own gaps, because you are its clock. The
  Swarm's room tone rises with your press count, which is a panic detector you can hear coming.
- **The input diagram (5, item 5) gets a "play it" button:** your last 20 bursts sounded as ticks against
  the threshold marks, so your own rhythm can be heard as well as seen. Same data, third channel,
  no new UI.

### 15.6 Mix

| Bus | Level | Rule |
|---|---|---|
| Room tone | -38 dBFS | always on, no rhythmic content, moves only with aggro |
| Drone + pulse | -30 dBFS | tier-driven, never above the room's own events |
| Press tick | -26 dBFS | fixed, never ducked, never tiered, identical on every device |
| Room events (doors, chests, stairs) | -16 dBFS | affordance family, never the verb bus |
| Verbs | -14 dBFS (-11 Frantic, -20 Careful) | owns the mix for its duration; everything but the tick ducks 6 dB |
| Damage to you | -10 dBFS | the loudest diegetic sound |
| Grammar (relic, ladder edit) | -8 dBFS | the loudest thing in the game, and always alone |

- Six voices maximum. Overflow is dropped in this priority order, worst first: extra grains, room
  events, enemy sounds, drone, verbs, and never the tick.
- No cue may step more than 12 dB inside 100 ms (startle), and no cue may peak above 6 kHz
  (repeated-transient and tinnitus fatigue). Hard limits, not a preset.
- The tick is never processed differently per device. A switch-access player must not hear a
  keyboard.

### 15.7 Accessibility

- **Nothing requires hearing.** Every cue in 15.2 and 15.3 has its 14.6 equivalent, and playing at
  zero audio is a supported configuration, not an accessibility mode. Say it as loudly as the
  one-switch claim in section 10.
- **Four sliders, not a master:** Switch (ticks), Verbs, Room (tone and events), Drone. The tick is
  a *control* sound, so a player who finds it grating must be able to silence it without losing
  verb feedback — and the other way round. A single master volume would force the wrong choice.
- **Quiet mode:** attacks softened 8 ms, tails shortened 40%, the tick moved to a lower, softer
  band. Nothing is removed and no cue becomes ambiguous: it is the same mix with the edge taken
  off, for players who cannot tolerate three hundred transients a minute.
- **Haptics** reuse the same envelopes as one rumble channel: Brace is a long low pulse, verbs are
  their own grain pattern, Frantic is a jitter. A third redundant channel, never a required one;
  reduced-motion (14.4, 14.8) also disables the jitter.
- **Mono must not break anything.** Identity lives in family and envelope, never in position.

### 15.8 Never-list

No adaptive or layered combat score · no licensed samples · no ambient loops · no footstep variety ·
no voice or barks · no menu whooshes beyond the page turn · no sonar or ping · no sound for the
intent ghost or the escalation (15.1) · no sting on room clear · no separate "damage dealt" and
"damage taken" cue beyond the family and gesture that already separate them · no device-specific
input sound · no reverb on a verb to make it pleasant · nothing that sounds more than three times
in a row without the player's hand being the cause.

### 15.9 How this sound is made

Same discipline as 14.10, and the same reason: if the audio cannot be built from a parameter
table, the sound design is not finished, it is decorated. Every source is synthesised from four
primitives — a filtered noise burst, a decaying sine, a struck-metal partial set, and a swept
filter — with no samples and no recorded audio in v0. The asset is the table; the synth is the
renderer's seed:

```
source     family   primitive     attack/decay   band (Hz)    grains  tier treatment
tick       switch   noise         0 / 12         1200-2500    1       none (fixed forever)
cloth      you      noise         5 / 110        200-1800     1..3    lp1800 / +2st / +40% tail
click      you      metal+noise   0 / 45         900-4200     2       lp1800 / +2st / +40% tail
bell       you      metal         2 / 600        1400-6000    1       lp1800 / +2st / +40% tail
thud       room     sine+noise    20 / 160       40-180       0       lp1800 / +2st / +40% tail
scrape     you      noise         40 / held      300-1200     -       lp1800 / +2st / +40% tail
page       you      noise+sweep   3 / 180        400-3000     1       lp1800 / +2st / +40% tail
roomtone   room     noise         loop, 20 s     60-900       -       aggro -> +6 dB shelf
grammar    grammar  sine pair     30 / 600 beat  220-660      1       always alone
```

v0 audio budget: 9 sources x 3 tier treatments = 27 parameter rows, three 20 s room tones, one
6-voice mixer with a side-chain on the verb bus, zero seconds of recorded audio. `figure 06` is
drawn by `figures/make_figures.py` from the same table, and any change to the ladder or the tier
thresholds must re-run it (14.10): the document and the build are not allowed to drift apart.

