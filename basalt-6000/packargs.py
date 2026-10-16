"""Print a .basalt pack's recorded build inputs (everything in meta but the per-tensor tables)."""
import json
import sys

sys.path.insert(0, sys.argv[2])
import model_file

meta = json.loads(model_file.ModelFile(sys.argv[1]).read("meta"))
for k, v in meta.items():
    s = json.dumps(v)
    print(k, ":", s[:400])
