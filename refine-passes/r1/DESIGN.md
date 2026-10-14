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
| hold | **Pivot** | rotate facing continuously while held; snaps to 45-degree steps (v0 ships 4 facings / 90-degree steps — 14.2-h); release commits | 0 (free) |
| hold 2 s | **Rest** | open the menu / end-of-room actions; opens on *release* of the hold (14.2-b) | free |

**Cost = the number of enemy actions that verb schedules** (14.2-f). Sprint's printed
"3 turns" is implemented as 2, and is a single tunable.

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

> **Correction (14.2-a):** as written, this axis cannot be reached — a gap of 260 ms or
> more already ends the burst, so no multi-press burst can ever read Normal or Careful.
> The tier is therefore measured over a **rolling cadence window** (median gap of the last
> 5 press timestamps within 2500 ms, gaps across bursts included), not inside one burst.

### 2.3 Thresholds (starting values, all tunable)

| Constant | Value | Notes |
|---|---|---|
| `DEBOUNCE` | 40 ms | below this, a second press is the *same* press |
| `HOLD_START` | 240 ms | press held past this -> pivot begins, step is cancelled |
| `COMMIT_WINDOW` | 260 ms | silence after the last press, then the burst is executed. It is also the burst boundary — `SLOW_GAP` is gone (14.2-a) |
| `TIER_SLOW` | 700 ms | rolling-window median gap above this = Careful (replaces `SLOW_GAP`) |
| `TIER_FAST` | 260 ms | rolling-window median gap below this = Frantic. Same number as `COMMIT_WINDOW` by coincidence; they stay separate constants because relics move one and not the other |
| `CADENCE_WINDOW` | 2500 ms | how far back the tier's median is taken over |
| `CADENCE_N` | 5 | press timestamps in that window; below 3 samples the tier is Normal |
| `IDLE_WAIT` | 1500 ms | no input -> Brace, once per idle period (14.2-c) |
| `REST_HOLD` | 2000 ms | menu, on release of the hold (14.2-b) |
| `MAX_VERB` | 5 | ladder saturates at Sprint; presses 6+ are ignored (14.2-g) |
| `RESOLVE_ANIM` | 120 ms | input during this window is buffered, never dropped (14.2-i) |

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

> As implemented, the `elif now - last_press > SLOW_GAP` branch is unreachable and has
> been deleted; the burst boundary *is* `COMMIT_WINDOW`. Tiering has moved out of
> `on_press` into the rolling cadence window (14.2-a).

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
- Threshold sliders (`COMMIT_WINDOW`, `TIER_SLOW`, `IDLE_WAIT`) with a live
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

Toolchain for all three (decided in 14.1-D1/D2): zero-dependency ES modules, `index.html`
opened directly in a browser, and `node --test` for the recogniser and simulation, which
run headless because they take the clock and the RNG as arguments. M1 and M2 are built as
one pass (14.1-D3); the concrete slice and its definition of done are 14.3 and 14.6.

## 13. Open questions — answered

These are decisions, not facts. Each carries the trigger that would reopen it.

1. **Is Pivot free forever?** **Free, in v0 and v1.** It is the only steering the game
   has; charging for it turns an accessibility feature into a tax and makes the
   graceful-degradation promises in 2.5 lies ("mis-aiming is never a trap"). Instead of a
   cost, make rotation *risky by geometry*: enemies follow a facing change, and the
   Sentinel archetype keys off it. Hard mode taxes whiffs, not pivots.
   *Reopen if:* playtests show players spinning to farm free information at zero cost —
   then cap it at one rotation per commit window, still free.
2. **Is the rate axis too subtle to teach?** **Keep it — but it had to be re-measured
   first; as specified it was unreachable (14.2-a).** It ships behind the always-on
   cadence meter and is instrumented from room 1.
   *Kill trigger:* fewer than 20% of bursts in rooms 1-5 land in Careful voluntarily ->
   cut the axis and go count-only in M3.
3. **Rotating camera?** **No. Fixed north-up map with a strong facing arrow for the
   first build.** It cannot be evaluated without a playtest, and it triples the
   rendering cost of the prototype. The input grammar is identical either way, which is
   exactly why we can defer it; it comes back as a toggle.
4. **Undo per room?** **Yes, but as a named mode rather than a hidden rule.** Calm
   (undo allowed, whiffs forgiven) / Standard (no undo, whiffs forgiven) / Hard (no undo,
   whiff kept). In a turn-based sim an undo is a state snapshot, ~free to implement
   (14.5), so the only real question is what it costs the fiction of risk — and that is
   a dial, not a design compromise.

---

## 14. Build readiness: what I need, and what I decided

Nothing below needs your permission to start; every row states the assumption I will
build on if you stay silent. The genuinely blocking ones are D3, D5 and the four items
in 14.7.

### 14.1 Questions I would ask you, and the decisions I took

| # | Question | Decision (default if unanswered) | Reopen if |
|---|---|---|---|
| D1 | What artifact do you actually want to run — browser, terminal, or a library? | **Browser, zero-dependency**: `index.html` + ES modules, no build step, no `npm install`, no network. Open the file, press Space. | You want a native/mobile shell, or an engine. |
| D2 | Language/stack? | **Plain JavaScript (ES2022, no framework).** It is the only target that both runs where the game will be played and delivers real input timestamps. The sandbox has Node 22 (no network, no pygame) and `node --test` works offline, so the *same* core files are unit-tested headlessly. A Python build would be a second, unplayable implementation. | You insist on Godot/Unity — the core has no DOM dependency and ports as-is. |
| D3 | First slice: M1 alone, or M1+M2 together? | **M1 + M2 in one pass.** The intent ghost is the feedback that makes the recogniser legible; a bare M1 can only be judged by someone who already knows the grammar. Plus 3 enemies and 2 relics as probes. | You want to answer "does a double click feel like a sword" with zero UI first — same codebase, `--no-ghost` flag, one day of work. |
| D4 | Are the numbers in 2.1-2.3 promises or placeholders? | **Placeholders.** Every constant lives in one file (`src/cfg.js`) that both the game and the Pause > Input diagram read. Nothing is hard-coded twice. Defaults are as printed, with the corrections in 14.2. | You have telemetry to seed them. |
| D5 | Will a human play this, or am I the only tester? | **Assume I am the only tester**, and compensate: a practice tile, the burst log printed on the end screen, and scripted-input tests (14.6) that pin the grammar. Everything M2 is supposed to answer ("can a stranger clear room 2 without instructions") stays explicitly unverified. | You can put a stranger in front of it — then I add an input-recording file so you can watch a run without being there. |
| D6 | Art: ASCII glyphs or drawn shapes? | **Glyphs with a shape language.** System monospace only (no downloaded fonts, no network assets), no sprites. Verb identity by shape and position, never hue alone (section 10). | You have a palette or an artist. |
| D7 | Is sound in scope? | **Yes, synthesised** — WebAudio, ~60 lines, no files. Per-verb audio is a section 5 requirement and costs nothing to fake with oscillators and envelopes. Mute toggle. | You want recorded samples (unfetchable offline). |
| D8 | Which input surfaces must work on day one? | **Pointer (mouse), Space/Enter, and touch** — press on `pointerdown`, but touch commits on `pointerup` per section 9; OS key auto-repeat is never a press. Gamepad polling waits for M3 (it needs a poll loop, not an event). This is the product's central claim ("any single switch"), so it is not deferrable. | You only care about keyboard for now. |
| D9 | How much run structure to fake? | **One floor, 8 hand-authored rooms**: tutorial 1-3 exactly as 5.1, then corridor, bottleneck, fork, vault, exit. No shop, no meta, no procedural generation, no floor 2. Section 8's 25 rooms / 3 floors is a target, not a deliverable. | You want generation early — the room format (14.5) is already what a generator would emit. |
| D10 | Difficulty modes now? | **Calm and Standard.** Hard is a flag once 2.5 exists. Live mode (section 3) is out of scope. | — |

### 14.2 Contradictions in the current spec that had to be settled first

A build that took sections 2.1-2.4 literally would not work. Resolved as follows.

a. **The rate axis is unreachable.** `COMMIT_WINDOW` is 260 ms, so any gap of 260 ms or
   more ends the burst — yet Normal is "260-700 ms" and Careful is "over 700 ms". No
   burst with two or more presses can ever read Normal or Careful: every multi-press
   verb is Frantic by construction. `SLOW_GAP` (700) is dead by the same argument, since
   the burst committed long before.
   **Decision:** tier is not measured inside a burst. It is the median gap over the last
   `CADENCE_N=5` press timestamps within `CADENCE_WINDOW=2500 ms`, gaps *across* bursts
   included, with printed thresholds unchanged. That is exactly what section 11 already
   logs; it makes all three tiers reachable; it gives a single-press burst a tier (which
   2.2 leaves undefined); and it fits the thesis better — the tier is the player's pulse,
   not one burst's. `SLOW_GAP` is deleted, replaced by `TIER_SLOW`/`TIER_FAST`.
b. **`hold` -> Pivot and `hold 2 s` -> Rest are the same gesture.** **Decision:** Pivot
   runs live from 240 ms and commits on release as printed; if the hold reached
   `REST_HOLD`, the menu opens *after* that commit. Legal precisely because Pivot is free
   and never punished (2.1) — the verbs stack harmlessly. If it opens menus by accident,
   Rest moves to "hold while the world is already Braced".
c. **Brace would re-fire forever.** As printed, idling 15 s farms 10 Guard and hands the
   enemies 10 free moves. **Decision:** Brace *arms once per idle period* — entering it
   grants +1 Guard and exactly one enemy free move, and cannot re-arm until you commit a
   verb. A braced enemy's free move may not enter your tile.
d. **"Step into a monster" and "Strike into a wall" are undefined.** **Decision:** Step
   into an occupied tile = **Bump**: no movement, no damage, 1 turn, and the ghost showed
   the occupant the whole time. That is the move that teaches "walking into a thing is
   not hitting it", which is what tutorial room 2 depends on. Strike with no target =
   Step (2.5). Strike into a wall = nothing happens, no turn spent.
e. **`Guard` is used three ways and never defined.** **Decision:** Guard is an integer
   count of hits fully absorbed, cap 3, cleared when you are hit and whenever you commit
   a movement verb (Step/Lunge/Sprint — you cannot walk with your shield up). Brace +1.
   The 4-tap Guard verb sets it to cap and reflects the next hit for 1. Iron Rest scales
   the amount, never the model.
f. **"Costs 3 turns" is undefined where turns are commits.** **Decision:** the turn
   economy is enemy actions scheduled per verb: Brace 0, Pivot 0, Step/Strike/Lunge/Bump
   1, Sprint 2 (not 3: three enemy moves for three tiles of travel is a tax the ladder
   never advertises, and it is one number in `cfg.js` for playtest to disagree with).
g. **Ladder saturation.** **Decision:** the ladder saturates at Sprint; presses 6 and
   beyond are ignored entirely — there is no new rung to light and the meter must not lie.
h. **"Snaps to 45-degree steps" vs "facing snaps to 4 directions in v0".** **Decision:**
   v0 is 4 facings, 90-degree steps. 8-way is a `cfg.js` switch; nothing else depends
   on it.
i. **A press arriving while a verb animates.** **Decision:** verbs resolve over a fixed
   `RESOLVE_ANIM=120 ms`; input during it is buffered as press 1 of the next burst,
   never dropped, never reordered. The recogniser is a pure function of
   `(event, t_ms, state)` with the clock injected by the caller — that is what makes
   14.6 possible at all.
j. **Nothing says what a room is.** **Decision:** rooms are ASCII strings in
   `src/rooms.js` (14.5), hand-authored for this build, in the same shape a generator
   would emit later.

### 14.3 The first buildable slice

**In:** the full recogniser (ladder, tiers, graceful degradation, Assist dwell wheel as a
toggle); one floor of 8 hand-authored rooms including tutorial 1-3 verbatim; intent
ghost, cadence meter, commit flash, per-verb glyph and SFX; Rat, Sentinel, Mirror;
Metronome and Offbeat relics; Calm/Standard modes with one undo per room; Pause > Input
showing a live diagram of your own recent bursts against the thresholds; end-of-run
cadence histogram; burst log persisted to `localStorage`.

**Out, named so nobody is surprised:** Live mode, procedural generation, floors 2-3, the
shop/nest/shrine economy, the other eight relics, Tic/Priestess/Swarm, the Drummer boss,
camera rotation, gamepad, meta-progression and starting grammars, mid-run save,
localisation, mobile layout polish, the Conductor's press-duration axis.

### 14.4 Layout and module contracts

```
index.html              canvas + input glue (~150 lines); only this file may touch the DOM
src/cfg.js              every tunable from 2.2/2.3 as data; read by game and pause screen
src/recogniser.js       PURE: (event, t, state) -> {state, verb|null, fx[]}  no DOM, no timers
src/sim.js              PURE: (state, verb, rng) -> {state, events[]}  grid, LOS, combat, AI
src/rooms.js            ASCII rooms -> {grid, entities, spawn, facing}
src/render.js           canvas draw from state only; ghost, meter, glyphs, flash
src/audio.js            WebAudio per-verb cues, parameters from cfg
src/telemetry.js        section 11 burst log -> localStorage + text histogram
src/run.js              the loop: input -> recogniser -> sim -> render; owns the clock
test/recogniser.test.js test/sim.test.js     `node --test`, offline
```

Two rules keep this testable: (1) `recogniser.js` and `sim.js` receive the clock and the
RNG as arguments and never call `Date.now()` or `Math.random()` themselves, so any input
sequence is reproducible; (2) the renderer reads state and writes nothing.

### 14.5 Data shapes the first build needs

```js
// section 11 record
{t0, deltas:[..], n, medGap, tier, verb, outcome}
// recogniser state
{phase: IDLE|PENDING|PIVOTING, presses:[t..], intent, tier, holdSince, buffered}
// world
{w, h, tiles:Uint8Array, entities:[{id,kind,hp,x,y,telegraph}],
 player:{x,y,face,hp,guard,grammar}, turn, rngSeed, room:{id,name},
 snapshots:[...]   // one per verb, for Calm undo; ~2KB structuredClone, <=200/room
                   // rng stream position is stored separately so undo cannot rewind luck}
// room ascii: '#' wall  '.' floor  '+' door  '<' stairs  '*' relic
//             'r' rat  's' sentinel  'm' mirror  '@' spawn  '^' spawn facing
```

### 14.6 Test plan (headless, runs before any human touches it)

`node --test` in the sandbox asserts the grammar, not the pixels:

1. one tap after 300 ms of silence -> Step, tier Normal.
2. two taps 120 ms apart -> Strike, tier Frantic, 1 enemy action scheduled.
3. two taps 400 ms apart -> **two Steps** (commit fired at 260 ms) — pins the section 9 mitigation for the classic double-click mistake.
4. taps at 150 ms x3 -> Lunge; x5 -> Sprint; x9 -> still Sprint (14.2-g).
5. hold 240 ms, rotate, release -> Pivot, 0 turns, facing changed; hold 2100 ms -> Pivot then Rest (14.2-b).
6. 1500 ms silence -> Brace once; another 3000 ms -> still exactly one Brace (14.2-c).
7. Strike facing empty floor -> Step, no turn lost; Step facing a rat -> Bump, 0 damage; Strike facing a wall -> no-op (14.2-d).
8. press during the 120 ms resolve window -> buffered as press 1 of the next burst (14.2-i).
9. Metronome (+120 ms commit) turns test 3 into a Strike — proof that a relic really changes the grammar.
10. Offbeat swaps 1<->2 without disturbing tiering.
11. Same seed + same scripted input -> byte-identical run transcript.

**Definition of done for the first build:** `node --test` green; `index.html` opens and
plays tutorial room 1 with no instructions on screen; the end screen prints my own tier
histogram; and from the log I can say how many of my own bursts landed Frantic.

### 14.7 Still unknown, and not decidable by me alone

- Whether a double click *feels* like a sword. That is M1's only question and only your hands can answer it.
- Whether a stranger clears tutorial room 2 without text (5.1).
- Whether the rate axis is teachable at all (13.2's kill trigger).
- Whether the switch-access claim in section 10 holds for an actual switch-access player. I can build Assist; I cannot validate it.
