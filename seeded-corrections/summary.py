import collections
import json
import sys

rows = [json.loads(line) for line in open(sys.argv[1])]
by = collections.defaultdict(collections.Counter)
for r in rows:
    c = by[r["arm"]]
    c["branches"] += 1
    c["turns"] += len(r["turns"])
    c["direct"] += r["direct_calls"]
    c["refused"] += r.get("refused", 0)
    c["branches_with_direct"] += r["direct_calls"] > 0
    c["branches_with_refused"] += r.get("refused", 0) > 0
    c["reads"] += sum(len(t["reads"]) for t in r["turns"])
    c["writes"] += sum(1 for t in r["turns"]
                       if {"write_file", "edit_file"} & set(t["tools_called"]))
    c["seconds"] += sum(t["seconds"] for t in r["turns"])
for arm, c in sorted(by.items()):
    t = c["turns"] or 1
    print(f"{arm:7} branches={c['branches']:3} turns={c['turns']:4} "
          f"direct={c['direct']:3} ({c['direct'] / t:.1%}/turn, {c['branches_with_direct']} branches) "
          f"refused={c['refused']:3} ({c['refused'] / t:.1%}/turn, {c['branches_with_refused']} branches) "
          f"reads/branch={c['reads'] / c['branches']:.1f} write-turns/branch={c['writes'] / c['branches']:.2f} "
          f"s/branch={c['seconds'] / c['branches']:.0f}")
