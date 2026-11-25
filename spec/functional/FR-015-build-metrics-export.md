---
id: FR-015
title: Export scheduler metrics for Prometheus and ix-board
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-003
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-001
    type: depends_on
  - target: ix://agent-ix/dev-team/FR-005
    type: depends_on
  - target: ix://agent-ix/dev-team/FR-010
    type: depends_on
---
# FR-015: Export scheduler metrics for Prometheus and ix-board

## Description

The scheduler SHALL export per-host metrics in Prometheus text format and as the versioned JSON snapshot ix-board reads, so that queue wait, slot utilization against what the host can sustain, pause time and disk use can be seen for every host.

## Behavior

The supervised governor (`locked-build serve`, [FR-010](FR-010-scheduler-owned-throttling.md)) serves the Prometheus text over HTTP at `--listen ADDR`, bound to loopback unless told otherwise; it is the same process that samples and throttles. `metrics` writes the same text to standard output or atomically to a file for a textfile collector when the governor is down. The JSON status snapshot of FR-005 carries the same values. Series, labelled by `host` unless noted:

| Series | Type | Extra labels |
|---|---|---|
| `ix_build_queue_depth` | gauge | `priority` |
| `ix_build_queue_wait_seconds` | histogram | `priority` |
| `ix_build_slots_busy`, `ix_build_slots_sustainable`, `ix_build_slots_max` | gauge | none |
| `ix_build_pause_seconds_total` | counter | `reason` (`thermal`, `operator`) |
| `ix_build_admission_blocked_seconds_total` | counter | `reason` (`memory`, `swap`, `compressor`, `host_load`, `target_disk`, `operator`, `probe`) |
| `ix_build_paused_orphans` | gauge | none |
| `ix_build_probe_defect` | gauge | `probe` |
| `ix_build_agent_processes`, `ix_build_agent_rss_bytes` | gauge | none |
| `ix_build_builds_total` | counter | `priority`, `outcome` |
| `ix_build_test_runs_total` | counter | `outcome` |
| `ix_build_target_dir_bytes`, `ix_build_target_dir_slots` | gauge | `repo` |
| `ix_build_probe_value`, `ix_build_probe_unavailable` | gauge | `probe` |
| `ix_build_lane_running` | gauge | `lane` |

The `lane` label is the bounded lane address `server:workspace:tab` of [FR-011](FR-011-priority-classes-lane-fair-share.md), never a session id. At most `max_lane_labels` (default 64) distinct lanes are labelled; others are summed under `other`. Agent processes are counted by the profile's command patterns. Counters derive from persisted transition events, so they stay monotonic across restarts and prune. Labels exclude ticket ids, request ids, command text and environment. Reading metrics takes no admission decision and never blocks admission longer than the state-read time. A source that cannot be read is reported through `ix_build_probe_unavailable`, not as zero.

**Build outcomes.** `ix_build_builds_total` counts each request once, when it reaches a terminal [FR-005](FR-005-fair-build-scheduler.md) state. Its `outcome` label takes one value from this closed set:

| `outcome` | How the request ended |
|---|---|
| `ok` | FR-005 state `succeeded` |
| `failed` | FR-005 state `failed`, with no FR-010 termination reason |
| `cancelled` | Cancelled while queued or running, with no FR-010 termination reason |
| `timed_out` | FR-005 state `timed_out` (hold deadline) |
| `aborted_memory` | Aborted above the memory `abort_above` |
| `aborted_swap` | Aborted above the swap `abort_above` |
| `aborted_compressor` | Aborted above the compressor `abort_above` |
| `aborted_host_load` | Aborted above the host-load `abort_above` |
| `aborted_thermal` | Aborted above the thermal `abort_above` |
| `rss_cap` | Terminated for exceeding its `rss_cap` |
| `pause_exceeded` | Cancelled for staying paused beyond `max_pause` |

A request that [FR-010](FR-010-scheduler-owned-throttling.md) ends with a termination reason counts under that reason, spelled as FR-010 records it, in place of the value for its FR-005 state. Only the resource-limit aborts begin with `aborted_`, so a consumer selects them with `outcome=~"aborted_.*"`.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-015-AC-1 | After a scripted sequence of queued, running, paused and finished requests, every series in the table appears with the expected value and labels, and `promtool check metrics` accepts the output. | Test |
| FR-015-AC-2 | `ix_build_slots_busy` and `ix_build_slots_sustainable` match the snapshot's occupied units and computed slot count at the same sample; `ix_build_pause_seconds_total{reason}` equals the recorded pause durations. | Test |
| FR-015-AC-3 | Counters do not decrease across a scheduler restart or after `prune`. | Test |
| FR-015-AC-4 | A required probe that is unavailable yields `ix_build_probe_unavailable` of 1 and no fabricated value; the exposition contains no ticket id, request id, command argument or environment value. | Test |
| FR-015-AC-5 | A fixture with 10 000 retained requests produces the exposition in under 200 ms and the governor's endpoint answers a scrape while a request is being admitted. | Test |
| FR-015-AC-6 | With 70 distinct lane addresses and `max_lane_labels` of 64, the output has 64 `lane` values plus `other`, each a `server:workspace:tab` address. | Test |
| FR-015-AC-7 | Series appear in a live Prometheus scrape of a host, and the Grafana fleet dashboard (delivered with SWM-242) and the ix-board fleet view read slots busy, sustainable slots, queue wait by priority and pause seconds with host and observation time. | Demonstration |
| FR-015-AC-8 | Every termination reason in the scheduler's FR-010 reason set appears as an `outcome` value: a scripted request ended for each of `aborted_memory`, `aborted_swap`, `aborted_compressor`, `aborted_host_load`, `aborted_thermal`, `rss_cap` and `pause_exceeded`, and one ending in each of `ok`, `failed`, `cancelled` and `timed_out`, raises `ix_build_builds_total` for that value by one and for no other; no other `outcome` value is exported. | Test |

## Dependencies

- [FR-001](FR-001-evidence-contract.md), evidence envelope consumed by ix-board.
- [FR-005](FR-005-fair-build-scheduler.md), events and snapshot.
- [FR-010](FR-010-scheduler-owned-throttling.md), governor, pause and termination reasons, and orphan state.
- ix-board fleet view (Linear W2, not yet delivered): consumer of the snapshot; AC-7 cannot be demonstrated before it ships.
- The Grafana fleet dashboard (Linear SWM-242): consumer of the Prometheus series.
