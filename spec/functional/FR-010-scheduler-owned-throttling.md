---
id: FR-010
title: Govern running builds with a supervised governor and watchdog fallback
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-003
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-009
    type: depends_on
---
# FR-010: Govern running builds with a supervised governor and watchdog fallback

## Description

A supervised governor process, `locked-build serve`, SHALL own host sampling, throttling (pause, resume, abort), operator hold and the Prometheus endpoint ([FR-015](FR-015-build-metrics-export.md)) for one host. The per-request watchdogs SHALL act as the fallback that resumes any paused group whose governor is gone, so that no process death leaves a build stopped indefinitely.

## Behavior

**Governor and supervision.** `locked-build service install` writes and enables a launchd agent on macOS or a systemd user unit on Linux and WSL, both restarting the governor on failure; `service status` reports the unit and the governor heartbeat. The governor takes one sample set per `sample_interval` and writes a heartbeat with each sample. It is the only sampler; watchdogs read the last sample.

**Scope.** Throttling acts only on process groups owned by scheduler leases, never on processes selected by name or path.

**Pause is for heat and operator only.** Reasons for pausing are `thermal` and `operator`. A thermal limit (`pause_above`, `resume_below`, with hysteresis) pauses every running lease and blocks new admission until the reading is at or below `resume_below`. Paused leases keep occupying capacity. `locked-build hold --reason TEXT [--pause]` blocks admission with reason `operator` and, with `--pause`, pauses running leases; `locked-build resume` ends it. Both are recorded with the note, and held seconds count as pause seconds with reason `operator`.

**Memory pressure never cascades pauses.** SIGSTOP does not release memory. For memory, swap, compressor and host-load limits, exceeding `block_above` refuses new admission (reason `memory`, `swap`, `compressor` or `host_load`), and exceeding `abort_above` aborts running leases by policy: lowest priority class first, newest first within the class, one lease per sample interval, until the reading is below the threshold. The same abort policy applies to a thermal reading above its `abort_above`. An abort uses the FR-005 termination path with reason `aborted_<reason>`, where `<reason>` is the breached limit's [FR-009](FR-009-host-profile-sustainable-slots.md) `reason`. A per-request or profile `rss_cap` terminates an offending lease with reason `rss_cap`.

**Termination reasons.** The termination reasons are this closed set, which the scheduler declares as one enumerated type used wherever a termination reason is recorded or exported. A cancellation and the [FR-005](FR-005-fair-build-scheduler.md) hold deadline are end causes but not termination reasons.

| Termination reason | Cause |
|---|---|
| `rss_cap` | The lease exceeds its `rss_cap` |
| `aborted_thermal` | Abort above the thermal `abort_above` |
| `aborted_memory` | Abort above the memory `abort_above` |
| `aborted_swap` | Abort above the swap `abort_above` |
| `aborted_compressor` | Abort above the compressor `abort_above` |
| `aborted_host_load` | Abort above the host-load `abort_above` |
| `pause_exceeded` | The lease stays paused beyond `max_pause` |

**One end cause.** A lease records one end cause: a cancellation, the hold deadline or one termination reason. The first cause recorded stands; a later one neither replaces it nor starts a second termination. When several termination reasons apply to a lease in one sample, the one listed first in the table is recorded. Limits above `abort_above` in the same sample share the one abort of that sample interval. A child that exits before any cause is recorded ends by its exit status.

**Continue before terminate.** Timeout, cancellation and abort of a paused lease deliver SIGCONT before SIGTERM so the child can exit.

**Probe loss fails open.** If the probe driving a pause becomes unavailable or stale, the governor resumes the paused groups at once and raises a probe defect (status field and `ix_build_probe_defect`); admission stays blocked for a required probe under FR-009.

**Fallback.** While the governor runs, a group left paused by a lost owner is resumed within one `sample_interval`. If the governor heartbeat is older than `heartbeat_stale`, each live watchdog resumes its own group and records the fact. A watchdog also resumes its group before exiting on every normal, signal and cancel path. When no governor and no watchdog is alive, `recover`, which every client command and every governor start runs first, resumes the group. Time paused does not count toward the hold deadline; a lease paused beyond `max_pause` is cancelled with reason `pause_exceeded`.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-010-AC-1 | With scripted thermal readings crossing pause and resume thresholds, all leases receive SIGSTOP once at the pause reading, no signal while paused, and SIGCONT at the resume reading; readings between the thresholds cause no signal flapping. | Test |
| FR-010-AC-2 | A memory breach above `block_above` refuses admission and pauses nothing; a breach above `abort_above` aborts the lowest-class newest lease, one per sample interval, with verified exit and reason `aborted_memory`; a same-named process outside any lease receives no signal. | Test |
| FR-010-AC-3 | With the governor running, killing with SIGKILL the supervisor and the watchdog of a paused lease leaves the group resumed within one `sample_interval` and `ix_build_paused_orphans` at zero within that bound. | Test |
| FR-010-AC-4 | With the governor killed, a paused group is resumed by its watchdog within `heartbeat_stale` plus one `watchdog_poll` (defaults 15 s and 5 s, so 20 s); with governor and all watchdogs killed, the next client command or governor start resumes it. | Test |
| FR-010-AC-5 | When the probe driving a pause becomes unavailable during a pause, the groups are resumed at the next sample, a probe defect is reported, and admission remains blocked while the probe is required. | Test |
| FR-010-AC-6 | An aborted or timed-out paused lease is continued before SIGTERM and exits through verified termination; a lease already finishing is not signaled twice. | Test |
| FR-010-AC-7 | Paused seconds do not count toward the hold deadline; a lease paused beyond `max_pause` is cancelled with reason `pause_exceeded`. | Test |
| FR-010-AC-8 | A job above its `rss_cap` is terminated with reason `rss_cap` and verified exit; a job below it is untouched. | Test |
| FR-010-AC-9 | `service install` produces a launchd plist or systemd user unit with restart on failure, generated by the Rust tool; killing the governor causes the unit manager to restart it in the test harness or the generated unit text declares restart on failure. | Test |
| FR-010-AC-10 | `hold` blocks admission with reason `operator` and a stored note until `resume`; running leases continue unless `--pause` is given; held seconds appear as pause seconds with reason `operator`; queued requests keep their age. | Test |
| FR-010-AC-11 | When a cancellation or the hold deadline is recorded first and the lease exceeds `rss_cap` or an `abort_above` is breached during the grace period, the request ends `cancelled` or `timed_out` with no termination reason. A recorded termination reason is not replaced by a later cancellation, deadline or reason. With the memory and thermal readings both above `abort_above` in one sample, one lease is aborted with `aborted_thermal`; each other adjacent pair in the termination reason table likewise records the earlier reason. Each ended group receives one termination sequence. | Test |

## Dependencies

- [FR-009](FR-009-host-profile-sustainable-slots.md), profile limits and probe samples.
- [FR-005](FR-005-fair-build-scheduler.md), lease, watchdog, recovery and termination behavior.
