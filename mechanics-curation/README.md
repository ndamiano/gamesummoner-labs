# mechanics-curation

Status: planned

Control: the words JEV chose for each of 111 distinct asks, in `asks.md`. 24 come from the decide
chain of a build (the newest chain of each ask, pinned in `control/`), 87 from the 2026-10-15
coverage probe in `labs/jev-design-decisions/runs/cov` (same 157 rows and question, frame only).
`words.md` turns it round: each catalogue word with the number of asks that chose it.

## Purpose

The designer writes the game from the words the decide step hands it: the frame, the mechanics
kept from `prompts/design/mechanics.json`, the look and sound, the screens, HUD, effects and
accessibility lists. If those words are not the game the ask describes, nothing after them can
put it right.

What the 111 asks show before anyone reads them one by one:

- The same words are chosen whatever the ask: difficulty ramp on 78 of 111, objectives 77,
  decoration 73, rewards 69, collectibles 64, spawn points and landmarks 63, score 60, boosts 58,
  dash 55, unlocks 52, hints 51.
- An ask's own verb can have no word. "A tiny ghost haunting a bakery at night, scaring customers
  to steal pastries before sunrise" got sneak, detection and hiding spots, and nothing for scaring.
- The same ask got leaderboard, medals / ranks, decoration, matches ("play happens in timed or
  scored matches"), both fly and jump, and three endings for a one-screen game.
- The count runs from 4 words to 97.

Already measured in `labs/jev-design-decisions`, and bearing on this lab:

- JEV takes the nearest wrong option over an escape option, so a word missing from the list is
  never reported as missing (2026-10-14, escape-hatch probes).
- A yes/no asked of a whole design ("is this design sufficient?") put every real design between
  0.62 and 0.80 and followed how much design there was, not how good it was (2026-10-14).
- A question over a group of words reads as the average of the words, not "any of" (2026-10-15).

## Hypothesis

The words chosen to feed the game design do not properly represent the game in the prompt: for a
given ask they include words that do not belong to that game and leave out words it needs.

Two measures.

1. **Nick's read of `asks.md`.** For an ask, the words that do not belong and the words that are
   missing. The number is wrong words per ask, and for each word how often it is wrong when it is
   chosen. This is the ground truth.
2. **A JEV grade.** `[kind] score`, 0 to 5: "How well does this design ask represent the prompt
   `{initial prompt}`?" with the design prompt under it, the design prompt being the decided state
   as the writer receives it. The number is the expected score.

The grade is an instrument and has to be shown to work before it is read. JEV chose every one of
these words itself at over 0.6, so it may simply agree with its own picks; the sufficiency probe
above is the same shape of question and did not separate. The check is each ask graded on its own
words and on every other ask's words.

- The grade works: an ask's own words outscore another ask's words nearly every time, and taking
  out the words Nick marked wrong raises the score.
- The hypothesis holds: Nick marks wrong or missing words on most asks.
- Idea failure, hypothesis: Nick finds the words mostly right, and the fault is after the decide
  step.
- Idea failure, grade: another game's words score as well as the ask's own. Then the read stays
  Nick's, and no arm is scored by JEV.

## Setup

- `survey.py` writes `asks.md` and `words.md` and pins `control/`.
- `grade.py`, to write: one `score` read per (ask, design prompt) pair against the local decide
  box's engine, in the shape `contract/decide.py` already sends (`gamesummoner-images`), which
  carries the `score` kind and has no caller for it today. The 24 build asks have a whole design
  prompt; the 87 probe asks have a frame and mechanics only, and need today's chain run on them
  first (about 16 s each).

Run 1: the ghost-bakery ask graded on its own design prompt and on the other 23.

    ../../venv/bin/python survey.py

## Log

**2026-11-05, systems probe 1: three system rows on the ghost-bakery ask (`systems.py`,
`systems/6382ea1e857f.jsonl`).** Nick's `prompts/design/systems.json`: stealth, survival and
crafting, each a name with a one-sentence definition. State is the ask and its frame as the
mechanics step saw it, which carries "win/lose: survive as long as possible". JEV through
llama-swap's `gamesummoner-decide`, the head and prompt from `contract/decide.py`. Nick's call
before the run: only stealth.

| rows | question | stealth | survival | crafting |
|---|---|---:|---:|---:|
| name and definition | Does this mechanic make sense for this game | 0.816 | 0.130 | 0.120 |
| name and definition | Does this system make sense for this game | 0.703 | 0.106 | 0.102 |
| bare name | Does this mechanic make sense for this game | 0.834 | 0.763 | 0.104 |
| bare name | Does this game contain | 0.846 | 0.873 | 0.023 |

Read: with the definitions only stealth is kept, as called. The bare name reproduces the 2026-10-14
word match on this ask (survival kept at 0.76 and 0.87), and the definition is what removes it.
One ask, three rows. Verdict: works.

**2026-11-05, systems probe 1 repeated: the same four forms, 20 rounds each (`repeat.py`,
`systems/6382ea1e857f.repeats.jsonl`).** Ten rounds one read at a time, ten with up to 8 reads in
flight, same ask, state and engine as above.

| rows | question | stealth | survival | crafting |
|---|---|---|---|---|
| name and definition | Does this mechanic make sense for this game | 0.753–0.828, kept 20/20 | 0.100–0.127, 0/20 | 0.111–0.126, 0/20 |
| name and definition | Does this system make sense for this game | 0.635–0.769, kept 20/20 | 0.092–0.114, 0/20 | 0.096–0.111, 0/20 |
| bare name | Does this mechanic make sense for this game | 0.810–0.839, kept 20/20 | 0.728–0.765, kept 20/20 | 0.100–0.114, 0/20 |
| bare name | Does this game contain | 0.826–0.858, kept 20/20 | 0.845–0.879, kept 20/20 | 0.021–0.031, 0/20 |

Read: no form changed what it kept in 20 rounds. A read is not repeatable to the digit on this
engine: the same prompt moved by up to 0.05 one at a time and 0.13 across both modes ("system"
wording, stealth). With definitions the rejected rows never passed 0.13; the "system" wording
leaves stealth 0.035 over the line at its lowest, the "mechanic" wording 0.15. Verdict: works,
consistently.

**2026-11-05, systems probe 2: seven systems on the 24 build asks (`across.py`,
`systems/across.jsonl`).** Nick's list grown to stealth, survival, crafting, combat, roguelike,
economy and story, each defined as "A system for …". Question "Does this system make sense for
this game", one read at a time, each ask's own frame as state. Nick before the run: not sold that
seven is near all of them, or that they do not overlap.

- Kept by, of 24 asks: story 8, combat 6, economy 5, stealth 3, crafting 3, survival 0, roguelike 0.
- 11 asks kept no system: gears puzzle, hiragana, frog platformer, frogs eating bugs, lighthouse,
  rhythm DJ, cart racing, kart racing, penguin climb, blorp, zombie.
- Where the right system is not on the list a neighbour takes the ask: both farming games kept
  crafting at 0.89 and 0.95, the city builder at 0.85.
- The roguelike deckbuilder did not keep roguelike (0.51).
- Story sits between 0.50 and 0.70 on 17 of the 24 asks.
- Kept together: crafting and economy on 3 of the 5 asks that kept either; no other pair on more
  than half.

Read: both of Nick's doubts hold on this list. Seven systems leave 11 of 24 asks with nothing, and
a missing system is answered by the nearest one rather than by none. One pair overlaps (crafting,
economy), and story behaves as the generic row. Verdict: works as a probe; the list is not done.

**2026-11-05, correction to probe 2's read (Nick).** Every system is asked on its own against the
same state, so no row's answer depends on which other rows are on the list. "A neighbour takes the
ask" and "answered by the nearest one" are wrong: crafting's 0.89 and 0.95 on the farming games
are JEV's answer to the crafting definition alone and would be the same with a farming row beside
it. The nearest-wrong-option finding of 2026-10-14 was about one choice among listed options, not
independent yes/no rows. What stands: 11 of 24 asks kept none of the seven. Whether that means
rows are missing, or that those games are carried by something other than a system, is open.

**2026-11-05, systems probe 3: a 46-row candidate list on the 24 build asks (`across.py --systems
candidates.json`, `systems/across-candidates.jsonl`, per ask in `systems/across-candidates.md`).**
Nick: the list should be more or less every major system a game can use, as building blocks; choose
blocks that make sense first, then cull so a game does not overcommit. `candidates.json` is Nick's
seven as he wrote them plus 39 drafted by Claude in the same form, not yet ruled on by Nick. Same
question and states as probe 2.

- Every ask kept at least one system. Kept per ask: min 1, median 7, max 22 (the 157-row catalogue
  on the same asks: 7, 41, 83).
- 11% of the 1,104 answers fall between 0.50 and 0.70.
- The surest pick is the ask's own block: gears puzzles 0.95 and nothing else; rhythm DJ rhythm
  0.97; hiragana quiz 0.82; kart racing driving 0.97; murder mystery investigation 0.93; deckbuilder
  cards 0.92; tower defense waves 0.89; farming farming 0.97.
- Kept most widely: collectibles 16 of 24, scoring 13, abilities 12, hazards 10, physics 9.
- Never kept: survival, units, sports (no such ask in the 24) and roguelike (0.51 on the roguelike
  deckbuilder, which kept procedural generation 0.77 and progression 0.67).
- The large asks still take many: make gta6 22, the two farming games 19 and 20, collecting
  monsters 17, the city builder 14.
- Pairs kept together are mostly the two farming games and the city builder keeping the same
  dozen rows; three like asks cannot show which rows overlap.

Read: with a wider list each ask's defining block comes out on top with a clear margin, and small
asks stay small. Open for the cull: the five widely kept rows, the roguelike row, and how many
blocks a large ask should take. Verdict: works as a probe; rows await Nick's ruling.

**2026-11-05, known games: six asks for a game like an established one (`known.py`,
`predictions.json`, `systems/known.jsonl`, `systems/known.md`).** Nick: predict what each should
have, then see what a prompt for something similar gets. Asks "a game like the binding of isaac /
slay the spire / tales of symphonia / grounded / pokemon red" and "single player league of
legends". Each ran prod's frame steps, then the 46 candidate rows on that state. The predictions
are Claude's, written to `predictions.json` before the run as core (must be kept) and fine (either
way), and not yet checked by Nick.

| game | core kept | core missed | kept, not predicted | kept in all |
|---|---|---|---|---:|
| the binding of isaac | 2 of 3 | roguelike 0.58 | none | 8 |
| slay the spire | 3 of 4 | roguelike 0.56 | waves 0.61 | 9 |
| tales of symphonia | 10 of 11 | world map 0.59 | none | 14 |
| grounded | 7 of 8 | survival 0.50 | physics 0.79, platforming 0.73, dialogue 0.71, relationships 0.69, puzzles 0.63 | 22 |
| pokemon red | 4 of 4 | none | time cycle 0.71, relationships 0.69 | 13 |
| league of legends, single player | 4 of 6 | opponents 0.47, economy 0.31 | hazards 0.84, story 0.67, quests 0.62 | 11 |

Read: 30 of 36 predicted core systems kept, and no row from an unrelated kind of game (farming,
driving, rhythm, quiz, sports, cards outside slay the spire) on any of the six. The six misses are
four rows: roguelike on both roguelikes, survival on the survival game, economy and opponents on
league of legends. Hazards is kept on five of six, story on all six. Two frames read wrong and may
pull rows with them: tales of symphonia as "a sequence of levels" (world map 0.59), league of
legends as "single screen … reach the exit". Verdict: works; the four missed rows and the
predictions go to Nick.

**2026-11-05, Nick's seven rows reworded, both probes rerun (`candidates.json`, the old text in
`candidates.before-reword.json`; `systems/known.jsonl`, `systems/across.jsonl`).** Nick: reword
roguelike, survival and economy, and rewrite all seven of his; hazards does fit single player
league of legends (added to its fine list); every miss but one sat at 0.47 or over, "they make
sense but weren't chosen". Each row now says what the player does and what the system contains.
Combat was reworded twice: "the player fights enemies" dropped the tower defense ask from 0.73 to
0.39, since its towers do the fighting, and "fighting between the player's side and enemies"
brought it to 0.79.

Known games, final wording, core kept 32 of 36 (30 before):

| game | core kept | core missed | kept, not predicted | kept in all |
|---|---|---|---|---:|
| the binding of isaac | 3 of 3 | none | none | 8 |
| slay the spire | 4 of 4 | none | none | 8 |
| tales of symphonia | 10 of 11 | world map 0.51 | none | 14 |
| grounded | 7 of 8 | survival 0.57 | physics 0.77, platforming 0.75, dialogue 0.74, economy 0.73, relationships 0.69, puzzles 0.64 | 23 |
| pokemon red | 4 of 4 | none | relationships 0.69, time cycle 0.68 | 14 |
| league of legends, single player | 4 of 6 | economy 0.58, opponents 0.49 | story 0.75, quests 0.60 | 11 |

- Roguelike: 0.58 and 0.56 on the two roguelikes became 0.96 and 0.93, and 0.09 to 0.39 on the
  other four. On the 24 build asks it went from none to the roguelike deckbuilder (0.92) and the
  murder mystery (0.63), whose frame says "permadeath, start a new run".
- Story: off the two roguelikes (0.54, 0.56), up on tales of symphonia (0.93) and pokemon (0.89).
  On the 24 asks kept by 4 instead of 8, and between 0.50 and 0.70 on 5 instead of 17.
- Economy: league of legends 0.31 to 0.58; on the 24 asks 5 to 7, adding the tower defense and
  the deckbuilder.
- Survival: grounded 0.50 to 0.57.
- The 39 rows left alone moved by up to 0.08 between the two known-game runs, and three of them
  crossed 0.6.
- A 0.5 line on the final run would keep three of the four misses, and with them 10 rows from the
  fine lists and 11 nobody predicted.

Read: the wording of a row decides it. Three rewordings moved a row by 0.3 or more in the right
direction, and one moved a row 0.34 the wrong way until it was put right. The misses left are
within 0.11 of the line, and a row that close is inside the run-to-run movement. Verdict: works.

**2026-11-05, the systems at 0.7 against the catalogue as prod asks it (`compare.py`,
`systems/known-old.jsonl`, both lists per ask in `systems/compare.md`).** Nick: tighten to 0.7
rather than loosen; the bar is better than before, not exact. Old: prod's mechanics step, 157
rows, "does this mechanic make sense", kept over 0.6. New: the 46 candidate rows in their final
wording, kept over 0.7. The known games use one frame state for both; the 24 build asks use their
control chains for old and a fresh run for new. "Old core covered" counts a predicted core system
when any catalogue row standing for it was kept (`OLD_ROWS_FOR`, Claude's mapping); the catalogue
has no row for procedural generation.

| game | old words | of them generic | old core covered | new systems | new core kept | new, not predicted |
|---|---:|---:|---|---:|---|---|
| the binding of isaac | 52 | 9 | 1 of 3 | 6 | 3 of 3 | none |
| slay the spire | 42 | 4 | 2 of 4 | 8 | 4 of 4 | none |
| tales of symphonia | 70 | 9 | 11 of 11 | 13 | 10 of 11, no world map 0.51 | none |
| grounded | 99 | 10 | 8 of 8 | 17 | 6 of 8, no survival 0.57, building 0.60 | physics, platforming, dialogue, economy |
| pokemon red | 63 | 8 | 4 of 4 | 9 | 4 of 4 | none |
| league of legends, single player | 52 | 9 | 4 of 6 | 5 | 3 of 6, no economy 0.58, equipment 0.64, opponents 0.49 | story |

- Core: 36 predicted, old covers 30 with 378 words, new keeps 30 with 58 systems.
- New at 0.6 on the same run: 32 of 36 core, 10 not predicted, 78 systems. The tighter line costs
  two core rows and removes five unpredicted ones.
- The 24 build asks, words handed to the designer: old min 7, median 40, max 83 (median 8 of
  them generic; 29 at a 0.7 line); new min 0, median 4, max 18. The lighthouse ask keeps none.

Read: the same share of what each game needs, in about a sixth of the words, and the two
roguelikes are named as such for the first time. What the old list had and the new one drops at
0.7: survival and building on grounded, world map on tales of symphonia, equipment on league of
legends. Predictions and the old-row mapping are Claude's; no design has been written from either
list. Verdict: works, better than the control on these asks.

**2026-11-05, seven gap rows from the lighthouse and frog asks (`gaps.json`,
`systems/across-gaps.md`).** At 0.7 the 46 candidates keep nothing on the lighthouse ask and only scoring on "frogs eating
bugs". Nick described a horror reading of the lighthouse (fuel down a flight of stairs, things
appearing in the dark, ships that vanish). Claude drafted seven rows from that and from the frog
ask (`gaps.json`): upkeep, limited sight, multitasking, scares, escort, catching, growth. One run
of `across.py --systems gaps.json` on the 24 build asks, same question.

| ask | upkeep | limited sight | multitasking | scares | escort | catching | growth |
|---|---:|---:|---:|---:|---:|---:|---:|
| lighthouse | 0.96 | 0.87 | 0.91 | 0.44 | 0.88 | 0.19 | 0.06 |
| frogs eating bugs | 0.30 | 0.24 | 0.17 | 0.09 | 0.02 | 0.94 | 0.68 |

- Kept over 0.7 across the 24 asks: limited sight 4, scares 4, catching 4, growth 3, escort 2,
  upkeep 1, multitasking 1. Ten asks keep none of the seven.
- Lighthouse goes from 0 systems to 4, frogs from 1 to 2.
- Scares is not kept on the lighthouse (0.44): the ask does not say horror and the frame chose
  tense, not eerie. It is kept on the haunted mall 0.92, the clock tower time loop 0.87, the
  night train murder mystery 0.78 and the ghost party DJ 0.74.
- Doubtful keeps: limited sight on the night train visual novel 0.76 and the clock tower 0.82,
  scares on the ghost party DJ, catching on the ghost bakery 0.73, growth on the zelda-like 0.72
  and on collecting monsters 0.77 (its wording, "grows stronger", overlaps progression and
  creatures).

Read: the two asks were empty because rows were missing, not because one-action games have no
systems. Upkeep, multitasking and escort fire on the lighthouse and nowhere they should not.
Limited sight and scares follow a dark or ghostly setting as much as a mechanic. Rows are
Claude's wording, not yet ruled on by Nick. Verdict: works for the two asks; three rows need a
second look.

**2026-11-05, what the designer does with the words it is handed (the 23 control asks that have
a written `design.md`; no new run).** Nick: the target for now is a plain game that is clearly
the prompt; the builds are all over the place. Counted, per design, how many of the kept
catalogue words appear in a heading of the design.

- 844 of 985 words are a heading, 86%. The deckbuilder design uses another heading form (4 of
  62); without it 840 of 923, 91%.
- "a platformer where you play as a frog": 41 words, 41 gameplay sections, one per word, among
  them transform, guards, flee, collectible creatures, plot, conversations, keys and locked
  doors, push and pull, bosses. The systems kept over 0.7 on the same ask: platforming 0.96,
  hazards 0.92, physics 0.88, collectibles 0.77.
- The lighthouse ask, 7 words: beam, ships, rocks and fuel are the tier 1 sections and none of
  them is a catalogue word; the designer took them from the ask. The catalogue words became the
  add-ons (high scores, upgrades and medals, leaderboard).

Read: the designer writes a section for nearly every word it is given, and finds the core of the
game from the ask without the list. The list sets how much is added on top. Substring match on
headings, so a rough count. No design has been written from a systems list yet.

**2026-11-05, four designs written from the systems list (`write.py`, `systems-50.json`,
`designs/<run>/design.md`, side by side in `designs/sections.md`).** Nick: do a few designs.
Prod's decide chain from the ask with one change, the mechanics step: the 46 candidates plus
upkeep, multitasking, escort and catching as rows, "Does this system make sense for this game",
kept over 0.7. First playable, look, sound, screens, hud, effects and accessibility steps as
prod. Prod's write prompt unchanged, on the local Flash-Next with the request prod sends
(temperature 0.7, xhigh, 100000 cap); the list reaches the designer as names only. One write
each, 150 to 205 s, no continuations. Baseline is the control design already on disk, written
earlier (Flash-Next for the platformer and the deckbuilder, DeepSeek for the lighthouse, none
for frogs eating bugs).

| ask | control words | control gameplay sections | systems kept | new gameplay sections |
|---|---:|---:|---|---:|
| a platformer where you play as a frog | 41 | 44 | platforming, physics, hazards; extra collectibles | 8 |
| A game about frogs eating bugs | 21 | not written | catching; supporting scoring | 9 systems under one heading |
| lighthouse keeper | 7 | 15 | upkeep, multitasking, escort | 5 |
| roguelike deckbuilder, wizard cat | 62 | 12, four of them bundles of words | combat, cards, roguelike, procedural generation; supporting abilities, hazards, economy | 12 |

- The frame came back the same as the control on all four asks.
- Platformer: run, jump, three hazards, an exit, five fixed-screen levels, optional golden
  flies. The design states what it leaves out: combat, health, lives, checkpoints, power-ups,
  inventory. The control had transform, guards, plot, conversations, collectible creatures,
  keys and locked doors and bosses as sections.
- Frogs eating bugs: move, tongue, three edible bugs, two hazard bugs, lives; then score, combo
  and high scores.
- Lighthouse: the cursor aims the beam, holding the pointer on the pump refuels and takes the
  beam off the sea, ships drift at two rocks, three lives, survival time. No flares, streak,
  upgrades, medals or leaderboard, which the control had. Scoring read 0.62 and was not kept, so
  there is no score.
- Deckbuilder: seeded generated floors and permadeath are in tier 1. The control had neither a
  roguelike nor a generation word, wrote its floors by hand, and carried sneak, taming, hiding
  spots, cutscenes and merchants in later tiers.
- The shorter state also shortened later steps: hud went from health, score, combo counter to
  score on the platformer and from score, timer to none on the lighthouse; high scores left the
  screens on three asks; the lighthouse lost its pause and settings screens.
- The designer uses the system names as section headings, abstract ones included (a
  "Multitasking" section), and gives each concrete rules.

Read: the designs hold to the ask and to the list, and say so. They are plain. Nothing in the
platformer is particular to a frog beyond its look. Baselines differ in date and, for the
lighthouse, in model. Nothing has been built from these. Verdict: works as a design; whether it
plays is not measured.

**2026-11-05, prod's stage plan on the four new designs (`plan.py`, `designs/<run>/stages.json`,
all four in `designs/plans.md`).** Claude's worry before a build: nine fixed stages on a design
with three systems would be padded with polish stages that rework finished code. Prod's plan
prompt unchanged, same model and request as the write, parsed and landed as prod lands it. One
call each, 111 to 259 s, all four parsed first time.

| ask | systems | stages 1 to 9 | a full round plays after |
|---|---:|---|---:|
| frog platformer | 4 | static lily pad · gribbit movement · reed spikes restart · moving hazard paths · fly jar exit · five level unlock · settings accessibility · golden flies · title win feel | 5 |
| frogs eating bugs | 2 | static pond shell · frog movement control · edible bug field · tongue catch system · hazard lives failure · screens hud loop · difficulty progression · scoring high scores · audio final polish | 5 |
| lighthouse | 3 | static storm world · pointer input cursor · fuel pump upkeep · beam aiming · ship spawn drift · beam guidance · lives failure loop · spawn progression patterns · title game over | 7 |
| deckbuilder | 7 | static level frame · player control cursor · starting deck hand · combat enemy turn · seeded level generation · run rewards exit · final boss full run · tier two mechanics · final screens audio | 7 |

- No plan has a stage that only polishes. The planner cuts a small game finer instead: the
  lighthouse gets a stage for pointer input and separate stages for aiming the beam and for the
  beam guiding ships.
- The seven-system deckbuilder is the tight one: stage 8 carries abilities, hazards and economy
  together, against the plan prompt's "one system, not three", and stage 7 carries the boss and
  the enemies of three levels.
- Every plan puts title, end screens, audio and feel in stage 9, as the plan prompt asks; on
  the lighthouse that stage also carries difficulty and reduced motion.
- Only the lighthouse control run has a plan to set beside: static night world · beam aiming ·
  tier 1 ships · rocks harbour lives · fuel and drums · score and streak · flare rescue · waves
  and merchantman · title audio feel. The platformer and deckbuilder controls were built
  unstaged.

Read: the padding worry did not hold. Nine stages fit two to four systems with every stage
adding something a player sees; seven systems crowd the last three stages. Verdict: works for
the small designs; the deckbuilder plan is the one to watch in a build.

**2026-11-05, first build from a systems design: the frog platformer, run 100f46b508a3
(`build.py`, design and plan from `designs/22263c0d3c8b`).** Nick: build it. A new private run
with the control's ask, the new design and its nine-stage plan landed as prod lands them, then
prod's staged build with the build prompt unchanged, Flash-Next on the local card through
`run.py` and `scripts/local_gpu.py auto`. Control: 22263c0d3c8b, same ask, Flash-Next design
and build, 41 words, built unstaged in one 200-step conversation, so the staged chain differs
as well as the list.

- All nine stages landed. Stage 1 retried once (booted, "A network error occurred."), stage 6
  retried once (did not boot, "Unexpected token '{'"); the other seven passed first time. 290
  build steps over 11 attempts, 302 jobs, none failed, 62 minutes.
- Gates: error gate 0 rounds, play gate 0 rounds, nothing reported broken. The play judge could
  not confirm the jump from screenshots.
- Headless check by Claude: title, level select, level 1 load; Space lifts the frog 54 px and
  it lands; walking into the spike triggers the hit flash, particles and restart; no page
  errors.
- Defect: the frog draws as a near-black shape on the dark background. `game/src/render.js`
  `drawPlayer` paints each run of pixels in the colour of the run's first pixel, which is always
  the outline. The sprite data has the teal body and yellow belly the design asks for. A builder
  bug, not a design or list one, and the reason the play judge could not see the jump.
- What is on screen is what the design lists and no more: platforms, spikes, golden flies, the
  fly jar, a score. The control build shows hearts, two collectible counters, a timer and a
  tutorial sign.

Read: the short design built to the end in the staged chain with every stage adding its part,
and the game is the ask. Whether it plays better than the control is Nick's to judge by playing
both. Verdict: works; play verdict pending.

**2026-11-05, Nick's play verdict on 100f46b508a3.** "Outside of not being able to see the
frog, this seems like the first game platformer that was actually completable." One game, one
play. The staged chain and the list both differ from the control, so the verdict does not say
which of the two made it completable.

**2026-11-05, the designer handed each system with its definition (`write.py --described`,
`designs-described/<run>/design.md`, side by side in `designs-described/sections.md`).** Nick:
pass the descriptions through. Until now the designer saw names only ("core mechanics:
platforming, physics, hazards") while JEV judged name plus definition. Same four asks, the same
`decisions.json` as the names-only designs, so the kept lists are identical; the three band
lines become a list of "- name: definition". Write prompt unchanged. One write each, 154 to
201 s.

Counts of a word in the names-only design -> in the described design:

| ask | definition clause | what the designer did with it |
|---|---|---|
| frog platformer | platforming: "running, jumping and climbing" | climb 1 -> 25 |
| frog platformer | physics: "objects fall, roll, bounce and collide ... the player uses that" | rolling logs and bounce pads; bounce 0 -> 32, push 0 -> 9 |
| frog platformer | hazards: "such as spikes, lava or falling" | lava 0 -> 14, pit 0 -> 11 |
| frog platformer | collectibles: "hiding things ... collect as a set" | hidden alcoves, a set-complete bonus |
| frogs eating bugs | catching: "before they get away" | bugs flee on a timer and an escaped bug costs a life; escape 1 -> 47; the hazard wasps are gone |
| frogs eating bugs | scoring: "combos, high scores or ranks" | rank 1 -> 38 |
| deckbuilder | economy: "at shops or from menus, and may sell or trade" | shop 2 -> 41, sell 0 -> 15, trade 0 -> 10 |
| deckbuilder | roguelike: "unlocks that may carry over to later runs" | persistent unlocks saved to storage |
| deckbuilder | hazards: "such as spikes, lava or falling" | lava 0 -> 23 |

- Size: platformer 43 -> 42 KB, frogs 48 -> 47, lighthouse 51 -> 45, deckbuilder 52 -> 61.
- Lighthouse: the examples in its definitions (convoy, survivors, power, air) do not appear.
  The ask already names the ships and the fuel.
- Not attributable to the definitions on one write each: the platformer lost its saws and
  gained a beetle, the lighthouse has a final score again, the frog has a different name.

Read: the definition closes the gap between what JEV approved and what the designer builds
(physics is now physics objects). The designer also builds every clause of a definition,
examples after "such as" and options after "may" included, so scope grows, most on the game
with the most systems. The definitions were worded for JEV to judge fit, not as a spec.
Verdict: works as a mechanism; the wording of the rows now sets the scope of the game.

**2026-11-05, the rows tightened (`systems-tight.json`; the first wording stays in
`systems-50.json`), read again by JEV, and four designs written from them
(`designs-tight/<run>/design.md`, `designs-tight/sections.md`).** Nick: tighten the rows first.
32 of the 50 rows reworded so that none carries a "such as" list or a "may" option; mean length
104 to 91 characters. JEV read them on the 24 build asks (`across.py`) and the six known games
(`known.py`), same question, 0.7 line, against the first wording. Three passes.

- Rows left unchanged moved 0.01 on average between the runs, so a shift in a reworded row is
  the wording.
- Pass 1 (examples simply removed): several rows read as fitting almost anything. Equipment
  without "weapons and armour" went 0.23 to 0.72 on a cozy farming ask and gained four asks;
  time cycle as "a repeating cycle" went 0.37 to 0.86 on the time-loop ask; progression as
  "permanently stronger" fell 0.79 to 0.39 on league of legends.
- Pass 2 (seven rows given back the words that define them, without lists) and pass 3
  (abilities): known games core 32 of 36 kept (first wording 30); the 24 asks keep 166 systems
  in total (first wording 152), median 4 to 6. Scoring, economy, gathering, physics, world map
  and management still read 0.07 to 0.11 higher than before. Abilities reads between 0.5 and
  0.8 on most asks under every wording tried.

Designs: prod chain decided afresh with the tight rows, definitions handed to the designer,
write prompt unchanged, one write each, 180 to 193 s.

| ask | kept, names-only run | kept, tight rows | KB names / described / tight |
|---|---|---|---|
| frog platformer | platforming, physics, hazards, collectibles | the same plus scoring | 43 / 42 / 48 |
| frogs eating bugs | catching, scoring | the same | 48 / 47 / 45 |
| lighthouse | upkeep, multitasking, escort | the same plus scoring | 51 / 45 / 50 |
| deckbuilder | combat, cards, roguelike, procedural generation, abilities, hazards, economy | combat, roguelike, cards, procedural generation, progression, hazards, inventory, economy | 52 / 61 / 61 |

- The clauses no longer leak. Described -> tight word counts: platformer lava 14 -> 0, climb
  25 -> 0, pit 11 -> 0; frogs rank 38 -> 0, escape 47 -> 4; deckbuilder sell 15 -> 0, trade
  10 -> 0, lava 23 -> 0, unlock 47 -> 6.
- The platformer's physics row is now built as written: four kinds of loose object (crate,
  barrel, ball, plank). JEV keeps physics at about 0.9 on this ask under both wordings.
- The platformer's frame changed between the two decide runs: failure read "restart the level"
  0.45 against "lose a life" 0.44 the first time and 0.42 against 0.43 this time, so this
  design has three lives and a game over screen. The rows play no part in that step.
- The deckbuilder is as large as the described one: eight systems kept, a shop in the level
  flow.

Read: tightening removes the leak and keeps the meaning. What sets the size of the game now is
how many rows are kept, and a row kept wrongly costs a whole built system where a bare name
used to be absorbed. A choice step whose top two options tie changes the game from run to run.
Verdict: works; the physics row on a plain platformer and the tied frame choice are open.

**2026-11-05, physics row renamed, then the second build: the frog platformer from the tight
rows with definitions, run fb0aa5866ea8 (`designs-tight2/22263c0d3c8b`).** Nick agreed the
change. The physics row became "physics objects: A system of loose objects that move and
collide under simulated physics, which the player sets in motion to solve problems." On the 24
asks it is kept on 2 (the first wording 7, the tight one 8); the frog platformer reads 0.55
(was 0.91), kart racing 0.24 (was 0.91). Known games on the full file: core 30 of 36 on this
run against 32 on the last, the difference in rows within 0.05 of the line.

Design: decided afresh, kept platforming and hazards (core), collectibles and scoring
(supporting); failure read "restart the level" again. One write, 192 s, 47 KB: run and jump,
three fixed hazards, an exit, six scrolling levels, five flies a level, score and high scores.
Claude's read of it: rules concrete and its jump numbers agree with its gravity (106 px stated,
106 computed); no level layouts, only a size, hazard counts and a par time per level; the three
hazards differ only in size; the no-hit bonus does not say whether it survives a restart.
Plan: nine stages, parsed first time.

Build: prod staged chain, Flash-Next, private run, as the first build. All nine stages passed
their check on the first attempt, no retries; 223 build steps, 236 jobs, none failed, 38
minutes (the first build: 290 steps over 11 attempts, 62 minutes). Error gate 0 rounds, play
gate 0 rounds, nothing reported broken. Headless check by Claude: no page errors, the level
loads, Space lifts the frog 100 px and it lands, the frog is drawn in its colours and is easy
to see.

Read: a second design from the short list built to the end, cleaner than the first. Verdict:
works; Nick has not played it.

## Outcome
