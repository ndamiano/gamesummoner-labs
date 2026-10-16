"""Serve the tuned Q4 pack for a real build: one request at a time, conversation parking on, 262K window with the
output cap fitted to the room left (the harness budgets 131K with its own token count), left running."""
from common import *

for line in subprocess.run(["ps", "-eo", "pgid=,args="], capture_output=True, text=True).stdout.splitlines():
    pgid, args = line.strip().split(None, 1)
    if args.startswith(f"{W}/basalt/bin/basalt serve"):
        subprocess.run(["kill", "-TERM", f"-{pgid}"])
time.sleep(10)
cfg = config(PACKS["q4mtp"], **{"conversation-cache-mib": 32000, "conversation-cache-slots": 16, "max-context": 262144})
cfg["server"]["fit-max-tokens"] = True
json.dump(cfg, open(f"{W}/cfg-build.json", "w"))
log = open(f"{W}/server-build.log", "w")
subprocess.Popen([f"{W}/basalt/bin/basalt", "serve", "--config", f"{W}/cfg-build.json"], stdout=log,
                 stderr=subprocess.STDOUT, start_new_session=True)
