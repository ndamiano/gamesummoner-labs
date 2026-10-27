import os
import shutil
from pathlib import Path
import sys

LABS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LABS)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(LABS, "seeded-corrections"))
from lib import paths
paths.bootstrap()
from lib.replay import replay
import positions
import realfs
from maestro.codegen.pyexec import runner

work = Path("/var/tmp/open-shim/realfs-check")
shutil.rmtree(work, ignore_errors=True)
w = positions.fix_start(paths.RUNS / "1629ea1ae380", "8a22202c1e36", work / "world")
game = work / "game"
shutil.copytree(w.dir, game)
tools = replay._tools_for(game, w.build, w.source_run)
home = os.path.expanduser("~")

ALLOWED = {
    "open read": 'print(len(open("design/design.md").read()))',
    "pathlib": 'import pathlib\nprint(sorted(str(p) for p in pathlib.Path("js").glob("*.js"))[:3])',
    "os.walk": 'import os\nprint(sum(len(f) for _, _, f in os.walk(".")))',
    "glob": 'import glob\nprint(len(glob.glob("**/*.js", recursive=True)))',
    "json.load": 'import json, glob\nprint([isinstance(json.load(open(f)), (dict, list)) for f in glob.glob("**/*.json", recursive=True)][:3])',
    "write+mkdir+remove": 'import os\nos.makedirs("tmpdir/a", exist_ok=True)\nopen("tmpdir/a/x.txt","w").write("hi")\nprint(open("tmpdir/a/x.txt").read())\nimport shutil\nshutil.rmtree("tmpdir")\nprint(os.path.exists("tmpdir"))',
    "binary": 'print(open("assets/actor-koi.webp","rb").read(4))',
    "tools still work": 'print(len(read_file("index.html")))',
    "stdlib lazy import": 'import textwrap, difflib\nprint(difflib.SequenceMatcher(None,"ab","ac").ratio())',
}
DENIED = {
    "etc passwd": 'print(open("/etc/passwd").read()[:20])',
    "parent run dir": 'print(open("../build_state.json").read()[:20])',
    "home key": f'print(open("{home}/.anthropic_key").read()[:5])',
    "listdir root": 'import os\nprint(os.listdir("/"))',
    "symlink out": 'import os\nos.symlink("/etc/passwd", "pw")\nprint(open("pw").read()[:10])',
    "hardlink": f'import os\nos.link("{home}/.bashrc", "b")',
    "write outside": 'open("/tmp/realfs-escape", "w").write("x")',
    "os.system": 'import os\nprint(os.system("id"))',
    "fork": 'import os\nprint(os.fork())',
    "subprocess import": 'import subprocess',
    "socket import": 'import socket',
    "proc environ": 'print(open("/proc/self/environ").read()[:40])',
    "repo src": f'print(open("{home}/Documents/ai-agent-test/src/maestro/codegen/tools.py").read()[:20])',
}
was = realfs.install()
from maestro.codegen.staging import game_dir
realfs._root["dir"] = str(game_dir(game).resolve())
print("root", realfs._root["dir"])
try:
    for group, cases in (("ALLOWED", ALLOWED), ("DENIED", DENIED)):
        print(f"##### {group}")
        for name, code in cases.items():
            out = runner.run(code, tools)
            last = (out.refused or out.stdout.strip().splitlines()[-1] if (out.refused or out.stdout.strip()) else "")
            print(f"{name:20} failed={out.failed} refused={bool(out.refused)} :: {last[:150]}")
finally:
    realfs.restore(was)
print("escape file exists:", os.path.exists("/tmp/realfs-escape"), "| pw link:", os.path.lexists(game_dir(game) / "pw"))
