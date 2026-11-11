"""Renders sample art through prod's generate_media path on a scratch private run, so an art
direction can be picked from pictures. Needs run.py up; the GPU runner drains the comfy queue.
usage: samples.py"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.paths import bootstrap

bootstrap()
from auth import store
from billing.packages import MICROS_PER_CREDIT
from db import games
from maestro.codegen.assets import request_media
from maestro.codegen.run import create_run, open_ask
from maestro.state import RunState

HERE = Path(__file__).resolve().parent
STYLE = "hand-drawn gothic storybook cartoon, scratchy dark ink outlines, muted sickly autumn palette, flat colours"
TILTED = {"view": "3/4 top-down"}
ABOVE = {"view": "top-down"}
ZOMBIE = ("a hunched green zombie homeowner in a torn brown cardigan, one eye bigger than the other, "
          "arms held out in front, dopey friendly grin")
JOGGER = "a cheerful jogger in a bright sky-blue tracksuit and headband, mid-stride, clean and tidy"
SAMPLES = [
    ("zombie-tilted", "actor", ZOMBIE, {"body": "biped", **TILTED}),
    ("zombie-above", "actor", ZOMBIE, {"body": "biped", **ABOVE}),
    ("jogger-tilted", "actor", JOGGER, {"body": "biped", **TILTED}),
    ("jogger-above", "actor", JOGGER, {"body": "biped", **ABOVE}),
    ("cop", "actor", "a suburban police officer in a navy blue uniform and cap, holding a flashlight, suspicious frown",
     {"body": "biped", **TILTED}),
    ("box-trap", "sprite", "a large cardboard box propped up on a stick with a rope tied to the stick, a paper "
     "coffee cup underneath as bait, patched with tape", TILTED),
    ("banana-stand", "sprite", "a wonky ramshackle cardboard banana stand booth with a giant yellow banana on its "
     "roof and a stack of green dollar bills on the counter, nailed together crooked", TILTED),
    ("fridge", "sprite", "a dented old white refrigerator with its door hanging off one hinge, pink glow leaking "
     "from the gap, standing on dead grass", TILTED),
    ("pool", "sprite", "a small backyard swimming pool filled with fetid murky green bubbling water, a yellow "
     "rubber duck floating in it, cracked tile rim", TILTED),
    ("lawn", "tile", "dead patchy suburban lawn, dry grey-green grass with bare dirt patches, seen from directly above", None),
    ("road", "tile", "worn dark asphalt road surface with fine cracks, seen from directly above", None),
]


def main():
    run = create_run(store.list_users()[0].id, private=True)
    games.charge_game(run, 0, MICROS_PER_CREDIT)
    open_ask(run, "art samples for a zombie survival game")
    build = games.create_build(run, kind="build")
    run_dir = RunState(run).run_dir
    for asset, kind, subject, details in SAMPLES:
        print(asset, json.dumps(request_media(run, run_dir, build, asset, subject, STYLE, kind, details)))
    (HERE / "samples-run.txt").write_text(run + "\n", encoding="utf-8")
    print("run", run, run_dir)


if __name__ == "__main__":
    main()
