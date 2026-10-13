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
