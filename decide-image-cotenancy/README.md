# Decide and image on one card

Status: planned
Control: the 2026-10-16 live run of frog `22263c0d3c8b` (decide alone on a g7e.2xlarge, 16.5 s
chain), and image jobs on today's RunPod 5090 boxes

## Purpose

A decide box is almost never warm. A game sends it one job of about 16 s, so every design pays a
cold boot: on the live run the decide job waited 128 s for the box and ran for 16.5 s. A box
that already serves a busy queue would make decide effectively warm.

## Hypothesis

JEV (Qwen3.8 27B NVFP4 under SGLang) and ComfyUI's image graphs share one RTX PRO 6000 with little
loss to either. VRAM is not the question: ComfyUI fits a 32 GB 5090 today and the card has 96 GB.
The question is time: the decide chain's wall time and image jobs' seconds per render, each alone
against both running at once. Expected: small, because a decide read is ~68 ms and the card has
~1.8 TB/s to share. An idea failure is a large slowdown on either side, or JEV's probabilities
moving (they should not: ComfyUI is a separate process, and the shift we measured came from
batching inside SGLang).

## Setup

To write. Starting points: the decide engine's `--mem-fraction-static` comes down from 0.91; JEV
stays `--max-running-requests 1`; one worker pulls one queue, so the box runs a decide worker and
an image worker against one contract server that lists both capabilities.

## Log

## Outcome
