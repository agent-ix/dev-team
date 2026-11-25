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
  - target: ix://agent-ix/dev-team/FR-011
    type: depends_on
---
# FR-015: Export scheduler metrics for Prometheus and ix-board

## Description

The scheduler SHALL export per-host metrics in Prometheus text format and as the versioned JSON snapshot ix-board reads, so that queue wait, configured and sustainable slot capacity, admission blocking, and disk use can be seen for every host.

## Behavior

The supervised governor (`locked-build serve`, [FR-010](FR-010-scheduler-owned-throttling.md)) serves the Prometheus text over HTTP at `--listen ADDR`, bound to loopback unless told otherwise; it is the same process that samples and throttles. `metrics` writes the same text to standard output or atomically to a file for a textfile collector when the governor is down. The JSON status snapshot of FR-005 carries the same values. Series, labelled by `host` unless noted:

| Series | Type | Extra labels |
|---|---|---|
| `ix_build_queue_depth` | gauge | `priority` |
| `ix_build_queue_wait_seconds` | histogram | `priority` |
| `ix_build_slots_busy`, `ix_build_slots_configured`, `ix_build_slots_sustainable`, `ix_build_slots_max` | gauge | none |
| `ix_build_admission_blocked_seconds_total` | counter | `reason` (`memory`, `target_disk`, `host_load`, `probe`) |
| `ix_build_paused_orphans` | gauge | none |
| `ix_build_probe_defect` | gauge | `probe` |
| `ix_build_agent_processes`, `ix_build_agent_rss_bytes` | gauge | none |
| `ix_build_builds_total` | counter | `priority`, `outcome` |
| `ix_build_test_runs_total` | counter | `outcome` |
| `ix_build_target_dir_bytes`, `ix_build_target_dir_slots` | gauge | `repo` |
| `ix_build_probe_value`, `ix_build_probe_unavailable` | gauge | `probe` |
| `ix_build_lane_running` | gauge | `lane` |

The `lane` label is the bounded lane address `server:workspace:tab` of [FR-011](FR-011-priority-classes-lane-fair-share.md), never a session id. At most `max_lane_labels` (default 64) distinct lanes are labelled; others are summed under `other`. Until the SWM-239 TOML profile exists, `ix_build_slots_configured` is sourced from the `capacity_units` field in the locked-build per-host JSON host policy. This is the interim configured server-capacity basis; TOML remains the target configuration source. The metric reports configured capacity and no sustainable value is derived from it. `ix_build_slots_configured` is distinct from FR-009's sustainable-slot calculation. `ix_build_admission_blocked_seconds_total` measures one host-wide blocked interval, counted once regardless of the number of waiters. It accumulates only while the scheduler's selected next eligible queued request is denied by a resource admission check. Time waiting only for capacity, FIFO or priority ordering, and pause time is excluded. The `reason` is selected from the scheduler's next eligible request, with this precedence when multiple resource checks fail: `probe` for a missing, invalid or stale host sample; then `host_load`; then `target_disk`; then `memory`. The closed reason mapping is `memory` = `memory_reserve`, `target_disk` = `disk_reserve`, `host_load` = `host_load`, and `probe` = missing/invalid/stale host sample. No `operator`, `swap`, or `compressor` series is emitted because this build has no producer/source for them; unavailable sources are omitted, never represented by fabricated zero values. Agent processes are counted by the profile's command patterns. Counters derive from persisted transition events, so they stay monotonic across restarts and prune. Labels exclude ticket ids, request ids, command text and environment. Reading metrics takes no admission decision and never blocks admission longer than the state-read time. A source that cannot be read is reported through `ix_build_probe_unavailable`, not as zero.

**Build outcomes.** `ix_build_builds_total` counts each request once, when it reaches a terminal [FR-005](FR-005-fair-build-scheduler.md) state; a restart, `recover` or `prune` does not count it again. Every `outcome` value is exported for every [FR-011](FR-011-priority-classes-lane-fair-share.md) priority class from 0, before any request ends with it, so a first occurrence reads as an increase. The `outcome` label takes one value from this closed set:

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

A request whose recorded [FR-010](FR-010-scheduler-owned-throttling.md) end cause is a termination reason counts under that reason, spelled as in FR-010's table, in place of the value for its FR-005 state. Only the `abort_above` aborts begin with `aborted_`, so `outcome=~"aborted_.*"` selects exactly those; it does not select `rss_cap`, which a consumer names separately.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-015-AC-1 | After a scripted sequence of queued, running and finished requests, every applicable series in the table appears with the expected value and labels, and `promtool check metrics` accepts the output. A metric with no source is omitted rather than exported as zero. | Test |
| FR-015-AC-2 | `ix_build_slots_busy`, `ix_build_slots_configured` and `ix_build_slots_sustainable` match the snapshot's occupied units, the interim JSON host policy's `capacity_units` value until the SWM-239 TOML profile exists, and computed sustainable slot count at the same sample. | Test |
| FR-015-AC-3 | Counters do not decrease across a scheduler restart or after `prune`. | Test |
| FR-015-AC-4 | A required probe that is unavailable yields `ix_build_probe_unavailable` of 1 and no fabricated value; the exposition contains no ticket id, request id, command argument or environment value. | Test |
| FR-015-AC-5 | A fixture with 10 000 retained requests produces the exposition in under 200 ms and the governor's endpoint answers a scrape while a request is being admitted. | Test |
| FR-015-AC-6 | With 70 distinct lane addresses and `max_lane_labels` of 64, the output has 64 `lane` values plus `other`, each a `server:workspace:tab` address. | Test |
| FR-015-AC-7 | Series appear in a live Prometheus scrape of a host, and the Grafana fleet dashboard (delivered with SWM-242) and the ix-board fleet view read slots busy, configured and sustainable slots, queue wait by priority and disk use with host and observation time. | Demonstration |
| FR-015-AC-8 | For each non-abort member of the scheduler's FR-010 termination reason enumerated type, a scripted request ended for that reason raises `ix_build_builds_total` under the `outcome` of the same name by one and under no other. The test iterates the non-abort members, so a member with no scripted case or no outcome value fails it. One request ending `ok`, one `failed`, one `timed_out`, one cancelled while queued and one cancelled while running each raise their value (`cancelled` for both cancels) by one and no other. No `outcome` value outside this requirement's outcome table is exported. Abort outcomes are not exercised or claimed by this criterion. | Test |
| FR-015-AC-9 | With no ended request, the exposition holds `ix_build_builds_total` at 0 for every `outcome` value under each of `check`, `test` and `gate`; after one `check` request ends `failed`, that series reads 1 and every other stays 0. | Test |
| FR-015-AC-10 | With at least one request ended in each non-abort outcome, and one whose owner is lost and which `recover` then ends, the recovered request raises exactly one value by one, and every `ix_build_builds_total` value is then equal before and after a scheduler restart, a second `recover` and a `prune`. Abort outcomes are not exercised or claimed by this criterion. | Test |
| FR-015-AC-11 | With multiple queued waiters, one host-wide admission-blocked interval accrues once, not once per waiter, only while the selected next eligible queued request is denied by a resource admission check. Time blocked only by capacity, FIFO/priority ordering, or pause does not accrue. The selected reason follows the documented closed mapping and precedence. | Test |
| FR-015-AC-12 | Until the SWM-239 TOML profile exists, `ix_build_slots_configured` equals the locked-build per-host JSON host policy's `capacity_units` value. This interim metric source does not derive a sustainable value. Unsupported `operator`, `swap`, and `compressor` sources produce no series rather than zero-valued series. | Test |

## Dependencies

- [FR-001](FR-001-evidence-contract.md), evidence envelope consumed by ix-board.
- [FR-005](FR-005-fair-build-scheduler.md), events and snapshot.
- [FR-010](FR-010-scheduler-owned-throttling.md), governor, pause and termination reasons, end cause, and orphan state.
- [FR-011](FR-011-priority-classes-lane-fair-share.md), priority classes and lane addresses.
- ix-board fleet view (Linear W2, not yet delivered): consumer of the snapshot; AC-7 cannot be demonstrated before it ships.
- The Grafana fleet dashboard (Linear SWM-242): consumer of the Prometheus series.
