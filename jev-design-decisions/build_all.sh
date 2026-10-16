#!/usr/bin/env bash
# The four builds of runs 1 and 2, one after another: JEV design and current-chain design per prompt.
set -u
cd "$(dirname "$0")"
MAZE="make me a game about solving mazes"
ONE="A roguelike with one button. What you do is decided by how fast you press it."
./build.sh runs/maze/design.md "$MAZE" maze-jev
./build.sh runs/maze/prod_design/design.md "$MAZE" maze-chain
./build.sh runs/one-button/design.md "$ONE" one-button-jev
./build.sh runs/one-button/prod_design/design.md "$ONE" one-button-chain
echo ALL BUILDS DONE
