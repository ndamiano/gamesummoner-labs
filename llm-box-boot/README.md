# llm box boot: why 140–300 s between "pack downloaded" and "serving"

Status: single-run
Control: prod EC2 llm boots of 2026-10-27 (eu-north-1) and 2026-11-04 (us-east-1, us-west-2),
boot logs in `s3://gamesummoner-models-<region>-<account>/bootlogs/`

## Purpose

A Private game on 2026-11-04 waited 776 s for its first llm job while a Quality game's was claimed
at once. One us-east-1 spot box was killed by the 420 s boot deadline before it ever served, and
its replacement had to be on-demand at $2.13/hr. Every cold Flash-Next box is paid time before it
earns, and the variance is what blows through the deadline.

Measured from the boot logs and the live us-west-2 box (i-0bfe258b6f45d4227):

| phase | eu-north-1 10-27 | us-east-1 11-04 (killed) | us-west-2 11-04 |
|---|---|---|---|
| launch → entrypoint starts | ~90 s | ~40 s | 52 s (16 kernel + 36 userspace) |
| pack on instance store | +87 s | +87 s | +89 s |
| basalt "loaded" | 202 s | not done at 298 s | 137 s |
| ready → worker registered | ? | — | ~65 s, unexplained |
| launch → registered | 387 s | killed at 425 s | 343 s |

Inside today's 137 s engine load (engine.log on the live box):

- `image encoder staged ... (85.7 s)`: 862 MiB of weights plus one warm-up encode. The same line
  read **1.1 s** when the AMI was baked on 2026-10-19 with a warm disk.
- experts pre-filled into VRAM from the pack: 28.6 s (2689 MB/s).
- 14.5 GiB pinned RAM complement: 20 s.

The image encoder's timer covers opening `mmproj.gguf` (876 MiB, on the root EBS volume under
`/root/.cache/basalt/.../vision`) and the first cuBLAS/cuBLASLt use, which loads ~0.6 GB of
library from `/usr/local/cuda-13.3` (also the root volume). The root volume is a gp3 restored from
the AMI snapshot: every block is fetched from S3 on first read, and gp3 defaults to 125 MB/s
even when warm. The rest of the engine's start (libcuda, the driver's JIT libraries, the basalt
binary, the venv) reads the same cold volume.

## Hypothesis

The variable middle of the boot is first-touch reads of the root EBS volume, not the pack, the
GPU or Basalt. Reading the ~2 GB of files the engine and worker touch in parallel at the very
start of the boot, while s5cmd pulls the pack (network and EBS hydration are separate paths),
moves those reads under the 70–90 s download.

Measured: pack-on-disk → engine ready, and launch → engine ready, on one box.

- Works: image encoder stage under 5 s, pack-on-disk → ready under 60 s (28.6 + 20 + small),
  launch → ready under 200 s.
- Idea failure: the encoder stage stays above 30 s with the files pre-read, or the pre-read itself
  takes far longer than the download and only moves the wait.

Every line carries a timestamp this time, so the 65 s ready → registered gap gets placed too.

## Setup

`run.sh` launches one g7e.2xlarge from the prod llm AMI with `boot.sh` as its user-data. The
image's entrypoint runs a user-data script instead of the worker, so the box never joins prod:
no worker token, no CP. `boot.sh`:

1. timestamps every line it writes (`python3 -u` stamp filter);
2. samples `/proc/meminfo` (Dirty, Writeback, Cached, MemFree) and `/proc/diskstats` for the root
   EBS and the instance store every second;
3. pre-reads the startup files with `xargs -P 32 cat` in the background (the list is what the
   live box had mapped, plus `/root/.cache/basalt`, `/opt/basalt`, `/opt/gamesummoner` and the
   python stdlib);
4. pulls the pack exactly as `entrypoint.sh` does;
5. starts basalt with the entrypoint's config and command line, stamps its stdout and its
   `engine.log`;
6. waits for `/v1/models`, sends one short chat request, records it;
7. copies its logs to `s3://<bucket>/lab/llm-box-boot/<instance>/` and powers off (instance
   shutdown behaviour is terminate).

```
AWS_REGION=us-west-2 ./run.sh ami-0fd3668cab20dc240 [--on-demand]   # the prod llm AMI, from prod settings
```

Cost: ~8 min of one g7e.2xlarge, ~$0.15 spot, ~$0.30 on-demand.

Run 2 takes the startup files off the root volume. `boot_pack.sh` is one prep boot, the stand-in
for a bake-time step: it tars `/root/.cache/basalt`, `/opt/basalt`, `/opt/gamesummoner`,
`/usr/lib/python3.12` and the cuBLAS, cudart, libcuda and libnvidia libraries into
`s3://<bucket>/lab/llm-box-boot/hot.tar`. `boot2.sh` is run 1's boot with the pre-read replaced:
it streams `hot.tar` onto the instance store beside the pack pull, bind-mounts each folder and
library over its root-volume path, turns on GPU persistence after the mounts, and starts the
engine with nothing else changed.

```
USERDATA=boot_pack.sh AWS_REGION=us-west-2 ./run.sh ami-0fd3668cab20dc240   # once, writes hot.tar
USERDATA=boot2.sh AWS_REGION=us-west-2 ./run.sh ami-0fd3668cab20dc240
```

Run 3 measures the pack pull's ceilings, because runs 1 and 2 showed the instance store writing a
flat ~1.56 GB/s at 99–100% busy for the whole pull while g7e.2xlarge's network baseline is 50 Gbps
(6.25 GB/s). `boot3.sh`: raw 30 GiB write and read with O_DIRECT on the instance store, the first
60 GiB of the pack from S3 to `/dev/null` at three s5cmd settings (no disk), then the prod pull.
If raw write is ~1.56 GB/s the pull is disk-bound and no s5cmd setting helps; the lever is then
writing less before the engine starts or loading from the network while the pull runs.

```
USERDATA=boot3.sh AWS_REGION=us-west-2 ./run.sh ami-0fd3668cab20dc240
```

## Log

### 2026-11-05 run 1, i-0a3740eaa55b0f4f2, us-west-2a spot

Logs in `run1/`. Times are seconds after the entrypoint started (uptime 38 s at that point).

| t | event |
|---|---|
| 0 | entrypoint starts; pre-read and pack pull start together |
| 38 | GPU persistence on (37 s, its driver files are on the root volume too) |
| 82 | pack on the instance store (81 s) |
| 82 | engine starts; pre-read still running |
| 95–162 | `image encoder staged (67.1 s)` |
| 164 | pre-read done: 6089 files, 1204 MiB, in 163 s |
| 164–194 | experts pre-filled from the pack, 30.3 s at 2543 MB/s |
| 194–210 | pinned RAM complement, 16 s |
| 211 | `/v1/models` answers; first reply 0.21 s later |

Disk samples: the root EBS volume read at **15–28 MB/s** for the whole first 165 s, and the
instance store read nothing until 166 s, when the EBS reads ended. The engine's own work from the
NVMe pack is 47 s. Dirty pages peaked at 11 GB during the pull and were flushed by 105 s, so they
were not the problem.

Read: the diagnosis holds and the fix does not. The image encoder's stage ended the moment the
pre-read ended: both were waiting on the same snapshot-backed blocks, and 32 parallel readers
did not lift a lazy-loaded gp3 volume above ~25 MB/s. ~1.2 GB of startup files at that rate is
~60–80 s whatever reads them. Pack → ready was 129 s against 137 s on the prod box; launch →
ready ~266 s.

The 65 s "ready → registered" gap from the prod table is not a gap: Basalt's `loaded ... in N s`
timer starts at its first load-progress line, not at engine start. On the prod us-west-2 box the
engine started at 01:53:30 and the worker's first claim (which sets `registered_at`) came at
01:56:52, 202 s later: 137 s of Basalt's timer, ≤4 s of 2 s polling, and ~61 s of engine start-up
before the timer, reading the cold root volume. Here the pre-read had half-warmed those files and
that phase was 12 s.

Verdict: idea failure for the pre-read. The cause is confirmed: first reads of the root EBS volume.
Next: take the hot files off the root volume. Put the ~1.2 GB (vision `mmproj.gguf`, cuBLAS and
cuBLASLt, the basalt binary, the venv) in the region's bucket next to the pack and pull them onto
the instance store with s5cmd at boot, the way the decide box already ships its env
(`pack_env.sh`). At S3 speed that is seconds; expected pack → ready ~50 s and launch → ready under
200 s. EBS Fast Snapshot Restore would also do it, at ~$540 a month per zone.

### 2026-11-05 prep boot, i-09500b8fedd5b963d

`hot.tar` is 2.8 GB. Run 1's "1204 MiB" pre-read figure was wrong: `du -cb` through `xargs`
printed only the last batch's total, so the startup set was always 2+ GB, and `/opt/basalt` adds
its source and build tree on top. Packing it off the
cold root volume took 663 s (~4.4 MB/s), the same wall again.

### 2026-11-05 run 2, i-0d9536fd30e03ece0, us-west-2a spot

Logs in `run2/`. Times are seconds after the entrypoint started (uptime 21 s at that point).

| t | event | run 1 |
|---|---|---|
| 15 | `hot.tar` streamed and unpacked, 2793 MiB in 16 s | — |
| 16 | bind mounts in place | — |
| 36 | GPU persistence on (21 s) | 38 (37 s) |
| 86 | pack on the instance store (86 s) | 82 |
| 89–93 | `image encoder staged (2.8 s)` | 67.1 s |
| 95–125 | experts pre-filled, 30.4 s at 2533 MB/s | 30.3 s |
| 126–142 | pinned RAM complement, 16 s | 16 s |
| 143 | `/v1/models` answers; first reply 0.25 s later | 211 |

Pack → ready **57 s** (run 1: 129 s). Launch → ready ~180 s (uptime 163 s plus ~16 s before the
kernel). The bind-mount count line printed 0 because it grepped the wrong `mountinfo` field; the
2.8 s encoder stage is what shows the mounts took.

Verdict: works. Encoder under 5 s, pack → ready under 60 s, launch → ready under 200 s. The
critical path is now the pack pull (86 s) then the engine's own 57 s; nothing waits on the root
volume except GPU persistence, which runs under the pull.

For production: build `hot.tar` at bake time from the files the engine opens (not all of
`/opt/basalt`), upload it beside the pack, and have `entrypoint.sh` stream it and bind-mount before
GPU persistence and the engine. The ~61 s of engine start-up that hid before Basalt's load timer on
prod is the same cold-volume read and goes with it; confirm by launch → `registered_at` on the
first prod boots after the change.

### 2026-11-05 run 3, i-0a45ab790aee085d5, us-west-2a spot

Logs in `run3/` (salvaged over SSM). Raw instance-store write, 30 GiB with O_DIRECT: **1.49 GB/s**.
Raw read: 3.61 GB/s. The prod pull's ~1.56 GB/s is the drive's write ceiling: no s5cmd setting
can make a 107 GB pull to disk faster than ~70 s on g7e.2xlarge.

The network-only half failed on implementation: `s5cmd cat` ran on one core (102% CPU) for 20
minutes without finishing 60 GiB, the sampler's interface regex matched no NIC so there are no
network numbers, the pack-size parse came back empty, and the 15-minute watchdog never fired
(bash defers a TERM trap until the foreground pipeline exits). The box was terminated by hand
at ~21 min. The network ceiling is unmeasured; it only matters for a loader that streams from
S3 without writing to disk first.

Verdict: the pull is disk-bound (works as a measurement); network ceiling: implementation fix and
rerun only if a streaming loader is pursued. Levers that remain: write less before the engine
starts (order the pack so the engine's first reads land first, start the engine before the PLE
table lands), or load from the network while the pull runs (Basalt work).

## Outcome
