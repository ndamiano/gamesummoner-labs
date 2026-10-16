# Look and sound

Draft for markup. JEV narrows each decision to an option; the LLM then writes the specifics
inside it (which colours, which sounds, what the HUD shows). Every option carries a one-line
description, since bare names got word-matched in the systems run.

Frame and kept systems go in the state. Each answer is carried into the next question's state.

## One (pick one)

| Decision | Options |
|---|---|
| Art style, 2D | pixel art: low-resolution sprites with visible square pixels and a limited palette; flat vector: clean flat shapes, solid colours, crisp edges; hand-drawn / painterly: brush strokes, ink lines or watercolour texture; anime / cel-shaded: bold outlines, flat banded shading; neon / synthwave: dark background, glowing saturated lines and bloom; minimalist geometric: abstract primitives, few colours |
| Art style, 3D | low-poly: few large flat-shaded polygons; voxel: everything built from cubes; realistic: lifelike materials, lighting and proportions; stylized / toon: soft shapes, bright colours, cartoon proportions; neon / synthwave: dark scenes, glowing lines and bloom; minimalist geometric: abstract primitives, few colours |
| Palette | warm: reds, oranges, yellows; cold: blues, teals, greys; dark: mostly black with a few bright accents; pastel: soft light colours; saturated: bright, strong colours; monochrome: one hue in many shades |
| Lighting, 3D only | daylight: bright, even sun; night: dark with local light sources; dusk / golden hour: low warm light, long shadows; indoor: artificial light, enclosed; fog / murk: limited view distance |
| Typography | pixel font: blocky bitmap letters; clean sans: plain modern letters; serif: book-like letters; hand-lettered: drawn, irregular letters; techno / display: angular, futuristic letters |
| Music | none: no music; ambient: slow textures, no strong beat; chiptune: retro console bleeps; synth loop: electronic loop with a beat; orchestral: strings, brass, drums; acoustic: guitar, piano, folk instruments |
| Sound effects style | retro bleeps: synthesized chip sounds; realistic: recorded-sounding impacts and foley; cartoony: exaggerated boings and pops; minimal: soft clicks and tones |

## Many (yes/no each)

| Decision | Options |
|---|---|
| Screens | title, pause, settings, game over, win, level select, high scores |
| HUD | health, score, timer, minimap, ammo, combo counter, wave number, currency |
| Effects | screen shake, particles, hit flash, slow motion on hit, trails, bloom |
| Accessibility | colour-blind safe palette, reduced motion, remappable keys, difficulty options |

## Left to the LLM

Animations per character, which events get a sound, exact colours, asset list.

## Open

- Missing options? The list has to hold the right answer.
- Is palette separate from art style, or does neon / synthwave already decide it?
- HUD and screens lean on systems (score, waves): fine to ask them after systems.
