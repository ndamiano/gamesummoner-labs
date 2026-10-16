"""Print how a .basalt pack stores its PLE key/value projections and whether it was built with --compat-bf16."""
import json
import re
import sys

sys.path.insert(0, "/opt/dlami/nvme/w/basalt/tools")
import model_file

m = model_file.ModelFile(sys.argv[1])
meta = json.loads(m.read("meta"))
conv = meta.get("conversions", {})
print("compat_bf16:", conv.get("compat_bf16"))
for r in conv.get("tensors", []):
    if "ple" in json.dumps(r):
        print(r)
s = json.dumps(meta)
print(sorted(set(re.findall(r'"[^"]*ple_(?:key|value)[^"]*"\s*:\s*[^,}]{0,80}', s)))[:10])
