# deepseek-flash-41

Status: planned
Control: labs/frontier-ceiling: DeepSeek V4.1 Flash through DeepSeek's API, ~6.25 mean over six
asks (Nick's scores, 2026-10-18) at ~$0.65 a game; prod Flash-Next on rented PRO 6000s at $1.81 a
game (2026-09-06).

## Purpose

DeepSeek V4.1 Flash 1017 (763B, MIT) builds clearly better games than Flash-Next, measured
through DeepSeek's hosted API. That API sends every prompt and game to DeepSeek, which breaks the
promise that nothing leaves GameSummoner's servers or rented GPUs. Serving the same weights on
cards we rent keeps the promise. The open question is no longer quality but whether we can run it,
and at what cost per game against $0.65 hosted and $1.81 today.

## Hypothesis

## Setup

Validate the serving stack before renting anything: which engine supports the architecture on
which card (grep the wheel for the arch), how many cards and how much host RAM the weights need at
a usable quantisation, the cold-load time, and the datacenter's download bandwidth. Then one build
on the prod harness, costed the way the 2026-09-06 cost-per-game arm was (per-pod billing split
by exec-seconds).

## Log

## Outcome
