# animation-model-i2i: a hand-keyed Blender mannequin, re-skinned frame by frame by Qwen-Image 2.1 edit

Status: single-run
Control: none run. Prior art: `labs/anim-still` (MiniMax-H3 sheets, retired on license), the
2026-09-04 charsheet arm (pose-by-prose redraws the character; a stick figure as edit-plus image2
transferred the pose 0/9).

## Purpose

A quick look, outside the lab procedure, at whether a sprite animation can come from two cheap
parts: a low-poly humanoid animated by hand in Blender, and an image edit model that swaps the
mannequin for the character in a reference sheet, one frame at a time. Motion, frame count, loop
and timing are all ours; the model only has to draw the character in a pose it is shown.

## Hypothesis

Qwen-Image 2.1 Turbo edit, given a mannequin frame and the character sheet, draws the sheet's
character in the mannequin's pose, and holds identity across the frames well enough for a walk
cycle to read. Measured by eye on a GIF, plus silhouette IoU of each edited frame against its
mannequin frame (`fidelity.py`). Idea failure: the model ignores the mannequin's pose, or the
character changes from frame to frame.

## Setup

One character (`character.jpeg`, a third-party character sheet), one action (side-view walk,
facing right), the local 5090. Edit model: `qwen_image_2.1_turbo_int8_convrot` with the
`qwen3vl_8b_int8_convrot` encoder and the 2.1 VAE, from the `qwen-2.1-turbo-edit` workflow in
`~/comfy/mess-with-comfy` (the `~/comfy/ComfyUI` checkout predates the 2.1 nodes). 8 turbo steps,
896x1184 out, about 7-9 s a frame, so a 16-frame cycle is about 2.5 minutes.

Comfy on the 5090 needs `--use-pytorch-cross-attention` (xformers has no sm_120 kernel):

    cd ~/comfy/mess-with-comfy && ~/Documents/ai-agent-test/labs/rig-lab/safe -m 45G \
      ~/Documents/Comfy/comfy-env/bin/python main.py --port 8189 \
      --disable-dynamic-vram --disable-pinned-memory --use-pytorch-cross-attention

The best chain (run9) from this folder, with `PY=~/Documents/Comfy/comfy-env/bin/python`:

    blender -b --python mannequin.py -- mannequin3 16 neutral
    blender -b --python mannequin.py -- mannequin_tpose 0 neutral
    mkdir -p tpose_in && cp mannequin_tpose/tpose.png tpose_in/frame_00.png
    $PY edit.py tpose_in tpose_s23 --seed 23 --start 0.99 --prompt prompt_tpose.txt
    cp tpose_s23/frame_00.png tpose_ref.png
    $PY edit.py mannequin3 run9 --start 0.99 --ref tpose_ref.png \
      --prompt prompt_neutral_tpose.txt --extra head_ref.png prompt_head.txt
    $PY fidelity.py mannequin3 run9

- `mannequin.py`: the humanoid, the walk (thigh 24° sine, knee flex in swing, feet held level,
  arms opposite, lowest foot snapped to the ground each frame), orthographic side renders and the
  screen position of each hand (`hands.json`). Style `outfit` = blocks coloured like the sheet,
  `neutral` = grey artist's mannequin with ball joints and mitten hands. Far-side limbs are darker
  in both. Frame count 0 renders a front-view T-pose.
- `edit.py`: mannequin frame as image1, reference as image2, optional fixed image3 (`--extra`),
  optional first-frame anchor (`--anchor`), and `--start` to sample from the noised mannequin
  latent instead of an empty one.
- `fidelity.py`: silhouette IoU against the mannequin, keyed on the border colour (the 2.1 VAE
  writes RGBA with near-opaque alpha, so alpha cannot be the matte).
- `head_ref.png` is a hand crop of `run3/frame_03.png`. The sheet and each run's `walk.gif` (plus
  `run3_vs_run7.gif`, `run7_vs_run9.gif`) are in git; frames, strips and mannequin renders are on
  disk only.

## Log

### 2026-11-17: run1 to run9, one session

| run | mannequin | reference | image3 | start σ | IoU | read |
|---|---|---|---|---|---|---|
| run1 | outfit v1, both legs one colour, 8 frames | sheet | none | 1.0 | 0.699 | identity strong, pose roughly followed; legs never pass |
| run2 | outfit, far side darker, 16 frames | sheet | first frame (anchor) | 1.0 | 0.570 | every frame copies the anchor's pose |
| sweep | outfit, frames 0/4/6 | sheet | ± anchor | 0.954 / 0.895 / 0.845 | 0.967-0.989 | the mannequin comes back redrawn, no character |
| sweep | outfit, frames 4/12 | sheet | none | 0.998 / 0.995 / 0.99 / 0.985 | 0.759 / 0.759 / 0.790 / 0.803 | full character in the mannequin's pose; 0.985 starts to stiffen |
| run3 | outfit, 16 | sheet | none | 0.99 | 0.749 | legs pass, cycle reads; jacket open/closed, one hands-in-pockets frame, one pale bionic hand, hair drifts |
| run3_anchor | outfit, 16 | sheet | first frame | 0.99 | 0.542 | anchor still overrides the pose |
| run4 | outfit, 16 | sheet cropped to the jacket figure | none | 0.99 | 0.716 | jacket consistent, bionic hand gone; hands in pockets 5/16 |
| run5 | outfit, 16 | sheet | head crop | 0.99 | 0.724 | head and hair consistent across all 16 |
| run6 | neutral, 16 | sheet | none | 0.99 | 0.674 | hands clean with fingers; head drifts as in run3 |
| run7 | neutral, 16 | sheet | head crop | 0.99 | 0.642 | hands clean, head consistent |
| T-pose | neutral T-pose, front | sheet | none | 0.99 | - | seeds 7, 11, 23 all clean, hands open; 23 picked as closest to the sheet |
| run8 | neutral, 16 | T-pose | none | 0.99 | 0.679 | head drifts; hands as run7, frame 0 hand visible where run7 buried it |
| run9 | neutral, 16 | T-pose | head crop | 0.99 | 0.632 | about run7; the T-pose's gain is a frame or two of hands |

What each step found:

- **The near and far legs must differ.** In run1 frames four apart were the same silhouette, so the
  edit could not tell which leg was in front and the stride never alternated. Darker far-side
  limbs fixed it.
- **A reference image of the character overrides the pose.** The first output as image3 made
  every frame the same pose (run2, run3_anchor). A crop of only the head does not (run5, run7,
  run9).
- **Pose lock comes from the latent, and turbo only allows it in a narrow band.** The turbo
  schedule decides layout between σ 1.0 and 0.978: starting at 0.95 or below returns the
  mannequin, starting at 0.99 returns the character in the mannequin's pose. Prompt words alone
  (run1, run2) give a generic walk.
- **Hands follow the mannequin's hands.** Box hands came back as fists and once as a pale box;
  the neutral mannequin's mitten hands came back with fingers.
- **Hair drift is not the mannequin.** The neutral mannequin has no hair block, and its heads
  drift as much as run3's; the head crop fixes it on either mannequin.
- IoU falls with the neutral mannequin because it is slimmer than the clothed character. It
  measures a lost pose, not a better one; the 0.95-and-below rows score highest by failing.

Nick, on run3: "Run3 without the anchor looks good", "Overall this workflow actually works pretty
dang well." Problems he named on the way: legs not passing, 8 frames short and choppy, character
inconsistencies, then broken hands and inconsistent head and hair. Run7 and run9 address the last
two; he has not graded them. Verdict: works, for one character and one side-view cycle.

## Outcome

Not wrapped. Open before this becomes a pipeline:

- `head_ref.png` was hand-picked from run3. The chain to test: T-pose from the sheet, one side
  frame from the T-pose, its head cropped, then the cycle with T-pose and head crop.
- Other facings (front, back, 3/4) and one-shots (attack), other body plans, a second character.
- Post: matte, foot lock against the mannequin's ground contacts, packing into a sheet. Foot drift
  over a loop is unmeasured.
- Against the Kimodo text-to-motion route (`labs/rig-lab/motion`): a hand-keyed cycle here
  could equally be a generated clip retargeted onto the mannequin.
