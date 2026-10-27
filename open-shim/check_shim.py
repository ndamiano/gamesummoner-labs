import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "seeded-corrections"))
from lib import paths
paths.bootstrap()
from lib.replay import replay
import openshim
import positions
from maestro.codegen.pyexec import runner

work = paths.OUTPUT / "branch-work" / "open-shim-check"
shutil.rmtree(work, ignore_errors=True)
w = positions.fix_start(paths.RUNS / "1629ea1ae380", "8a22202c1e36", work / "world")
game = work / "game"
shutil.copytree(w.dir, game)
tools = replay._tools_for(game, w.build, w.source_run)

CASES = {
    "read": 'print(len(open("design/design.md").read()))',
    "with+iter": 'with open("design/design.md") as f:\n    print(sum(1 for _ in f))',
    "readlines": 'print(open("index.html").readlines()[:2])',
    "missing": 'open("nope.js").read()',
    "missing caught": 'try:\n    open("nope.js")\nexcept FileNotFoundError as e:\n    print("caught", e)',
    "outside": 'open("/tmp/maps.json", "w").write("{}")',
    "binary": 'open("assets/actor-koi.webp", "rb")',
    "write no close": 'open("shimtest.txt", "w").write("hello\\n")\nprint(read_file("shimtest.txt"))',
    "append": 'with open("shimtest.txt", "a") as f:\n    f.write("more\\n")\nprint(read_file("shimtest.txt"))',
    "own traceback line": 'x = 1\ny = 2\nraise ValueError("mine")',
    "still banned": 'eval("1")',
    "dunder still banned": 'print(open.__init__)',
}
was = openshim.install()
try:
    for name, code in CASES.items():
        out = runner.run(code, tools)
        print(f"=== {name}: refused={out.refused!r} failed={out.failed} ledger={out.ledger}")
        print(out.stdout.strip()[:400])
finally:
    openshim.restore(was)
print("restored ban:", "open" in runner.BANNED_CALLS)
