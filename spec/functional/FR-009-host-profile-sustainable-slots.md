---
id: FR-009
title: Compute sustainable build slots from a host profile and measured headroom
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-003
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-005
    type: depends_on
---
# FR-009: Compute sustainable build slots from a host profile and measured headroom

## Description

The scheduler SHALL compute each host's number of sustainable build slots from one TOML host profile and live probe readings, and use that number as enabled capacity in the
[FR-005](FR-005-fair-build-scheduler.md) admission rules. No slot count is edited by hand or recorded in a comment. One slot is one FR-005 resource unit.

The TOML profile is the only source of host limits. The earlier JSON host policy is no longer read: a JSON policy file found at the state or configuration path is ignored with a warning naming the file, and no converter or compatibility reader exists. Probes are pluggable per host architecture and come from the shared host-probe crate extracted from relay-watcher (Linear SWM-238); this requirement depends on that crate and does not define a second probe implementation.

## Behavior

The profile has these tables. Unknown keys are refused at load with a diagnostic naming the key.

| Table and keys | Meaning |
|---|---|
| `[host]` `name`, `max_slots`, `cpu_cores`, `jobs_per_slot`, `cpu_set` | Host label; hard slot ceiling; cores (default measured); `CARGO_BUILD_JOBS` per slot; optional CPU affinity |
| `[memory]` `ram_per_job_default`, `ram_per_job_min`, `reserve`, `history_window`, `grow_after` | Per-job RAM before history exists, its floor, RAM kept free, jobs of history used, hold time before a rise in slots applies |
| `[reserve]` `cpu_cores`, `memory`, `services` | CPU and memory reserved for shared services on this host (for example the relay Redis bus on titan, Prometheus and kind on luna); `services` is a documentation list shown in status |
| `[weight]` `cpu_weight`, `nice` | Scheduling weight of builds below services: Linux and WSL run each job in a systemd user scope with `CPUWeight` (default 20 against the default 100); macOS runs jobs at `nice` (default 10) |
| `[pool]` `path`, `budget`, `per_key_slots`, `min_free`, `max_age` | Target-pool settings of [FR-012](FR-012-target-dir-pool.md) |
| `[governor]` `sample_interval`, `heartbeat_stale`, `watchdog_poll`, `max_pause`, `probe_timeout`, `stall_wait`, `max_lane_labels` | Sampling cadence (`sample_interval`, default 5 s); age at which watchdogs treat the governor as dead (`heartbeat_stale`, default 15 s); longest pause (`max_pause`); per-probe timeout (`probe_timeout`); watchdog observation interval (`watchdog_poll`, default 5 s, also the FR-005 supervisor poll); wait that counts as an admission stall (`stall_wait`, default 5 min, FR-016); distinct lane label values (`max_lane_labels`, default 64, FR-015) |
| `[repos.<name>]` `mirror`, `remote` | Bare mirror directory and remote URL for a repo on this host (FR-014) |
| `[commands]` `allow` | Non-cargo commands a dispatched job may run in a checkout (FR-014); empty by default |
| `[[probe]]` `name`, `kind`, `required`, `interval` | A probe from the shared crate and whether its loss is fatal to admission |
| `[[limit]]` `probe`, `pause_above`, `resume_below`, `abort_above`, `block_above`, `reason` | Thresholds on a probe reading and the `reason` they report, one of `thermal`, `memory`, `swap`, `compressor` or `host_load`; see [FR-010](FR-010-scheduler-owned-throttling.md) |
| `[env]` | Environment set for every job (for example `CARGO_INCREMENTAL`) |
| `[request_limits]` `jobs_per_slot`, `nice`, `rss_cap` each with `min` and `max` | Bounds within which a request may override the profile value |
| `[agents]` `patterns` | Command patterns counted as agent processes |

Probes include CPU package temperature (titan Tctl) and package power; memory compressor size and swap use (draco); WSL available memory and WSL memory limit (terra); available RAM; one-minute load; free disk for the pool. A reading carries a value, a unit, an observation time, or an explicit unavailable reason.

Sustainable slots are the minimum of: `max_slots`; floor((available RAM minus `[memory] reserve` and `[reserve] memory`, plus RAM held by running leases that is already measured) divided by RAM per job); floor(free pool disk above `min_free` divided by the per-slot disk estimate); floor((`cpu_cores` minus `[reserve] cpu_cores`) divided by `jobs_per_slot`); and any bound a limit declares (zero while a thermal pause is active, zero while `block_above` is exceeded).

RAM per job is the profile default until job history exists, then the 90th percentile of measured peak memory for that repo and priority class over the last `history_window` jobs, never below `ram_per_job_min`. Peak memory of a job's whole process group is measured per platform: cgroup v2 `memory.peak` of the job's systemd scope on Linux and WSL; on macOS the sum of resident memory over the group's processes sampled each `sample_interval` through `proc_pid_rusage`, whose sampling error (short peaks missed, shared pages counted twice) is accepted at 15 percent for history and for `rss_cap`.

A decrease takes effect at the next sample. An increase takes effect only after the higher value has held for `grow_after`. A shrink never terminates running leases for slot-count reasons; it is reported as overcommit under FR-005. A required probe that is unavailable or stale gives zero sustainable slots with the probe named; an optional probe that is unavailable is ignored and reported. An invalid profile, such as a resume threshold not below its pause threshold, or a `[[limit]]` whose `reason` is missing or outside the set above, is refused at load with a diagnostic naming the key. A profile edit is picked up at the next sample without restarting running builds. Because reserved CPU and memory are removed before slots are counted and jobs run at the lower weight, shared services keep priority over builds when the host is saturated.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-009-AC-1 | Given a fixture profile and scripted probe readings, the computed slot count equals the minimum of the bounds above for reading sets where each of RAM, disk, CPU, `max_slots` and a limit bound is the binding one. | Test |
| FR-009-AC-2 | A required probe that returns unavailable, or a reading older than twice the sample interval, yields zero slots and a reason naming the probe; an optional probe in the same state does not change the count and is listed as unavailable in status. | Test |
| FR-009-AC-3 | A drop in headroom lowers the count at the next sample; a rise raises it only after `grow_after` on a controllable clock; running leases are not terminated and overcommit is reported. | Test |
| FR-009-AC-4 | Fixture profiles for a thermal host (Tctl, package power), a macOS host (compressor, swap) and a WSL host (WSL memory) each load, run only their declared probes and compute slots; an unknown key and a resume threshold not below its pause threshold are each refused naming the key. | Test |
| FR-009-AC-5 | After jobs with known peak memory complete, RAM per job moves from the default to the 90th percentile of the history window and respects `ram_per_job_min`; status reports the value and its source. On Linux the peak is read from cgroup v2 `memory.peak`, on macOS from sampled `proc_pid_rusage` sums, and a fixture with a known 1 GiB peak reports within the stated tolerance. | Test |
| FR-009-AC-6 | The scheduler reads probes only through the shared host-probe crate; the repository has no second probe implementation and no hand-edited slot count in a comment, profile comment or script. | Inspection |
| FR-009-AC-7 | Replacing a profile file atomically changes ceiling and thresholds used at the next sample without restarting or signaling running builds. | Test |
| FR-009-AC-8 | A JSON host policy present at the legacy path is not read: capacity is unchanged, a warning names the file, and no code path converts it. | Test |
| FR-009-AC-9 | With `[reserve]` set to half the cores and a fixed memory amount, the slot count is computed from the remainder; on Linux each job runs in a systemd user scope with the configured `CPUWeight`, on macOS at the configured nice level, verified from the child's observed weight or nice value. | Test |
| FR-009-AC-10 | A request overriding `jobs_per_slot`, `nice` or `rss_cap` within `[request_limits]` is applied; a value outside its bounds is refused with a request error naming the key and limits; a key not listed is refused. | Test |
| FR-009-AC-11 | A limit with each `reason` of `thermal`, `memory`, `swap`, `compressor` and `host_load` loads. A profile with a `[[limit]]` whose `reason` is `power`, or is missing, is refused at load naming the key, whether the limit declares `abort_above` or `block_above`. | Test |

## Dependencies

- Shared host-probe crate extracted from relay-watcher (Linear SWM-238), a hard dependency; implementation starts after it exists.
- [FR-005](FR-005-fair-build-scheduler.md), admission and overcommit behavior.
- [FR-010](FR-010-scheduler-owned-throttling.md), limits evaluated from the same samples.
