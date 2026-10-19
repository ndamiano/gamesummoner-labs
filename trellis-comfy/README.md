# trellis-comfy

Status: done
Control: `labs/img2threed/glbview/m/*.trellis.glb` (trellis_server at prod settings on the same
subjects), and the 2026-09-04 ComfyUI 0.34.4 spike outputs in `~/output/trellis2-comfy/out/`

## Purpose

`GameSummoner summon` is meant to run locally against four hard dependencies: llama-swap, ComfyUI,
the decision model, and a tool-calling LLM. The custom TRELLIS engine
(`gamesummoner-images/engines/trellis/trellis_server.py`, its own venv, repo checkout, CUDA
extensions and Blackwell patches) is a fifth install for every new user, and one more server to
maintain. ComfyUI 0.34 runs TRELLIS.2 natively, with remesh, decimate, unwrap and voxel texture
bake nodes, so mesh generation can move onto the ComfyUI the user already brings. The mesh path is
rarely called today (see the design-tiers-skip-art finding), so the bar is to match what it has.
Speed and simplicity are not things to be gained here.

## Hypothesis

A ComfyUI TRELLIS.2 graph at prod settings (bf16, 512 voxel tier, decimate 50k, unwrap, bake
1024) returns a GLB that loads in the game runtime. Judged side by side against trellis_server on
the same subject, it is no worse in shape or texture, and its resident time per mesh is within the
8-13 s that trellis_server takes on the 5090.

Idea failure: comfy's graph cannot produce a baked-texture GLB at 512 without OOM on a 32 GB card,
its output is visibly worse on shape or texture at matched settings, or the GLB fails
`runtime/decimate.mjs` / the three.js loader.

## Setup

- ComfyUI `~/comfy/ComfyUI-0.34` (v0.34.4) in `~/comfy/comfy-env-034`, launched with
  `--use-pytorch-cross-attention` and under `labs/rig-lab/safe -m 45G` with `--disable-dynamic-vram`.
- Weights: `trellis_2_bf16`, both TRELLIS.2 VAEs, `dino_v3_vit_l`, already placed.
- Graph (`run.py`): comfy's TRELLIS.2 template samplers, then prod's `o_voxel.postprocess.to_glb`
  chain rebuilt from native nodes: FillHoles 0.03 → RemeshMesh udf (band 1, project 0) →
  DecimateMesh 50k → UnwrapMesh → BakeTextureFromVoxel 1024 → ApplyTextureToMesh with base
  colour, metallic and roughness. bf16 weights, 512 tier, as in `runpod/mesh/entrypoint.sh`.
- Known gap left for a second run if this one falls short: prod samples 12/12/12 steps with
  rescale_t 5/3/3, while the template runs the shape stage at 20 steps with its own shift and CFG
  cutoffs.
- Run: `./launch.sh`, then `python3 run.py ~/comfy/ComfyUI-0.34/input/broken-wooden-cart.png`.
  It times a cold and a warm pass and then runs `runtime/decimate.mjs` on the GLB.
- Subject: `broken-wooden-cart`, the same PNG behind `img2threed/glbview/m/broken-wooden-cart.trellis.glb`.
- 5090, local. Waits for the card to be free (one GPU queue at a time).

## Log

### 2026-10-18 run 1: broken-wooden-cart, seed 7, 5090

The control's old GLB (`img2threed/glbview/m/broken-wooden-cart.trellis.glb`) is a dangling
symlink, so trellis_server was run fresh with the local_gpu argv on the same PNG.

| | trellis_server | comfy graph |
|---|---|---|
| resident s/mesh | 9.6, 8.0 | 8.5, 9.0 |
| cold, from launch | 21 s load + 11 s warmup | 16-17 s first mesh |
| triangles raw → after decimate.mjs | 49,244 → 19,994 | 49,926 → 19,977 |
| maps | base colour + metallic/roughness, 1024 | same |
| texture encoding | webp, 2.2 MB GLB | png, 4.0 MB GLB |
| NORMAL | yes | yes, once MeshSmoothNormals sits after UnwrapMesh |
| doubleSided | false | true, and no node exposes it |

The first pass had MeshSmoothNormals before UnwrapMesh, which split vertices along seams and dropped
the normals (implementation fix, rerun). The first warm timing (0.5 s) was comfy's cache replaying an
identical graph, so the warm pass now uses seed + 1.

Read: structural and speed parity. Two encoding gaps remain (png not webp, double-sided). The
visual comparison is still to do: `out/index.html?glb=<file>` served on :8399.

## Outcome

Yes: the ComfyUI TRELLIS.2 graph matches trellis_server on speed and structure (resident 8.5–9.0 s
per mesh against 8.0–9.6, same triangle counts after decimate, same maps). The two encoding gaps
were closed outside the graph: decimate.mjs writes webp textures and single-sided materials
(ai-agent-test 73df3e4). Adopted: meshes render on the ComfyUI box and the mesh queue and
trellis_server are gone (ai-agent-test 0b2e02f, gamesummoner-images 87f8378). The side-by-side
visual check was not recorded.
