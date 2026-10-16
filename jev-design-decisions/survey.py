import json, glob, os, re, collections
VENDOR = {"world.js", "three.module.js", "GLTFLoader.js", "BufferGeometryUtils.js"}
rows = []
for spec in sorted(glob.glob("/home/nick/output/runs/*/spec.json")):
    run = os.path.dirname(spec); d = json.load(open(spec))
    prompt = (d.get("ask") or "").strip(); src = "ask"
    if not prompt:
        prompt = (d.get("request") or "").strip(); src = "request"
    g = os.path.join(run, "game")
    if not prompt or not os.path.exists(os.path.join(g, "index.html")):
        continue
    code = ""
    for f in glob.glob(g + "/**/*.js", recursive=True) + [os.path.join(g, "index.html")]:
        if os.path.basename(f) in VENDOR or "/node_modules/" in f or "/vendor/" in f or "/game/lib/" in f: continue
        try: code += open(f, errors="ignore").read()
        except OSError: pass
    persp = bool(re.search(r"PerspectiveCamera", code)); three = bool(re.search(r"\bTHREE\b|from ['\"][./]*three", code))
    dim = "3d" if persp else ("2d-three-ortho" if three else "2d")
    rows.append({"run": os.path.basename(run), "src": src, "prompt": prompt, "built": dim})
json.dump(rows, open("rows.json", "w"), indent=1)
print(len(rows), "built runs", len({r["prompt"] for r in rows}), "distinct prompts")
print(collections.Counter(r["built"] for r in rows), collections.Counter(r["src"] for r in rows))
