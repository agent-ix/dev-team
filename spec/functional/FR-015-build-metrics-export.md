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

The scheduler SHALL export per-host metrics in Prometheus text format and as the versioned JSON snapshot ix-board reads, so that queue wait, configured and sustainable slot capacity, pause time, admission blocking, and disk use can be seen for every host, including builds observed after an external wrapper admits them.

## Behavior

The supervised governor (`locked-build serve`, [FR-010](FR-010-scheduler-owned-throttling.md)) serves the Prometheus text over HTTP at `--listen ADDR`, bound to loopback unless told otherwise; it is the same process that samples and throttles. `metrics` writes the same text to standard output or atomically to a file for a textfile collector when the governor is down. The JSON status snapshot of FR-005 carries the same values. Series, labelled by `host` unless noted:

| Series | Type | Extra labels |
|---|---|---|
| `ix_build_queue_depth` | gauge | `priority` |
| `ix_build_queue_wait_seconds` | histogram | `priority` |
| `ix_build_slots_busy`, `ix_build_slots_configured`, `ix_build_slots_sustainable`, `ix_build_slots_max` | gauge | none |
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

The `lane` label is the bounded lane address `server:workspace:tab` of [FR-011](FR-011-priority-classes-lane-fair-share.md), never a session id. At most `max_lane_labels` (default 64) distinct lanes are labelled; others are summed under `other`. Until the SWM-239 TOML profile exists, `ix_build_slots_configured` is sourced from the `capacity_units` field in the locked-build per-host JSON host policy. After that profile exists, it is sourced from TOML `[host].max_slots`. It is a configured server-capacity value in either state; no sustainable value is derived from it. FR-009's sustainable slot count is computed separately from its TOML profile and live probes, and is unavailable before that profile exists. A series with no producer in the current build is absent until its producer exists, never exported as zero. The current locked-build implementation emits six metric names from this table: `ix_build_queue_depth`, `ix_build_queue_wait_seconds`, `ix_build_slots_busy`, `ix_build_slots_configured`, `ix_build_builds_total`, and `ix_build_admission_blocked_seconds_total`. The complete current-build absence set includes these 11 additional metric names from the table: `ix_build_slots_max`, `ix_build_paused_orphans`, `ix_build_probe_defect`, `ix_build_agent_processes`, `ix_build_agent_rss_bytes`, `ix_build_test_runs_total`, `ix_build_target_dir_bytes`, `ix_build_target_dir_slots`, `ix_build_probe_value`, `ix_build_probe_unavailable`, and `ix_build_lane_running`. It also includes `ix_build_pause_seconds_total` until a pause-time producer exists, `ix_build_slots_sustainable` before the TOML profile exists, and the `operator`, `swap`, and `compressor` reason series of `ix_build_admission_blocked_seconds_total` until their respective producers exist. The absent pause series retains the declared `thermal` and `operator` reasons. These current-build omissions do not remove the series or labels from the metrics contract. The closed `ix_build_builds_total` outcome set is an explicit exception to source-based omission: every outcome value is always emitted for every priority class, initialized to zero before a matching terminal event occurs, including abort outcomes.

For admission-blocked time, the complete `reason` set is `memory`, `swap`, `compressor`, `host_load`, `target_disk`, `operator`, and `probe`. `ix_build_admission_blocked_seconds_total` measures one host-wide interval, counted once regardless of waiter count, only while the scheduler's selected next eligible queued request is denied by a resource admission check. Time waiting only for capacity, FIFO or priority ordering, and all pause time is excluded. When multiple reasons apply to the selected request, use this complete precedence from highest to lowest: `probe` for a missing, invalid or stale host sample; `host_load`; `target_disk`; `memory`; `swap`; `compressor`; `operator`. While an operator hold or any pause is in effect this counter accrues under no reason, even when a resource limit also applies; `operator` stays in the reason set as FR-010's refusal reason, and its time is counted only in `ix_build_pause_seconds_total`. The exact current-build producer mapping is `memory` = `memory_reserve`, `target_disk` = `disk_reserve`, `host_load` = `host_load`, and `probe` = missing/invalid/stale host sample. Agent processes are counted by the profile's command patterns. Counters derive from persisted transition events, so they stay monotonic across restarts and prune. Labels exclude ticket ids, request ids, command text and environment. Reading metrics takes no admission decision and never blocks admission longer than the state-read time. A source that cannot be read is reported through `ix_build_probe_unavailable`, not as zero.

**Observe mode.** `locked-build observe [--kind build|test] [--priority check|test|gate] [--queued-at-ms N] -- <command...>` runs `<command...>` immediately. This mode only observes a command that an external wrapper has admitted; it never queues or admits work, checks capacity or resources, applies a priority, enforces a hold deadline, or terminates the observed command. The optional `--kind` and `--priority` values are metadata hints only and do not change execution or admission. A missing hint remains absent or explicitly unknown; the observer never infers kind or priority from command text and never supplies a default priority that appears real. A kind of `build` attributes the terminal result to build outcomes, and a kind of `test` attributes it to test-run outcomes. With no kind hint, the terminal result is recorded without a kind classification and increments neither outcome family. A build outcome increments a priority-labeled `ix_build_builds_total` series only when both `--kind build` and a `--priority` of `check`, `test`, or `gate` were supplied. A test-run outcome increments `ix_build_test_runs_total` only when `--kind test` was supplied. An absent priority never increments a priority-labeled outcome or queue-wait histogram. Queue wait is observed only when both `--queued-at-ms` and a valid `--priority` hint are supplied; the external wrapper supplies the timestamp at queue entry, before waiting, and the observer measures through command start. Without either option, no queue-wait observation is made. Occupancy is recorded while the command runs, and a dead observer's busy slot is reclaimed. An observed process maps exit code 0 to `ok` and any nonzero exit or signal termination to `failed`, unless an explicit, independently known termination cause is supplied, in which case only its matching member of the closed outcome set is used. The observer never infers timeout, cancellation, pause-exceeded, RSS-cap, or abort causes from process status alone. It retains the raw exit code or signal separately from the outcome label.

Before recording, the observer reads host configuration and acquires the state lock with a short bounded timeout. Any observer failure, including a missing or unwritable state directory, corrupt state, invalid configuration, lock timeout, or a store containing admitted requests rather than observed requests, emits one warning and runs the command without observer writes. The wait for the state lock is bounded; observer failure adds no command delay beyond that bound. A store contains either observed requests or admitted requests, never a mixture. If modes are mixed, `observe` warns once and runs the command without changing the store. The configured-slots gauge uses the host configuration source above, and its value equals the number of build slots the external wrapper can admit. Queue depth, admission-blocked time, and pause series require scheduler-owned state that observe mode cannot know; observe mode emits none of them, rather than zero.

The observed child preserves the caller's exit status, including signal termination, stdin, stdout, stderr, environment, working directory, process group, and signal delivery. Signal handling by the observer SHALL not prevent the caller's signal from reaching the observed process group.

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
| FR-015-AC-1 | After a scripted sequence of queued, running and finished requests, every series in the table whose producer exists in the build under test appears with its expected value and labels, and every other series and reason label is absent rather than zero; `promtool check metrics` accepts the output. The `ix_build_builds_total` closed outcome values are present for each priority class, including values with no terminal event, which read as zero. | Test |
| FR-015-AC-2 | Before the SWM-239 TOML profile exists, `ix_build_slots_busy` and `ix_build_slots_configured` match occupied units and the JSON host policy's `capacity_units`; no sustainable value is derived or exported. After the profile exists, configured slots match TOML `[host].max_slots`, sustainable slots match the independently computed sustainable count, and all three values match the snapshot at the same sample. | Test |
| FR-015-AC-3 | Counters do not decrease across a scheduler restart or after `prune`. | Test |
| FR-015-AC-4 | A required probe that is unavailable yields `ix_build_probe_unavailable` of 1 and no fabricated value; the exposition contains no ticket id, request id, command argument or environment value. | Test |
| FR-015-AC-5 | A fixture with 10 000 retained requests produces the exposition in under 200 ms and the governor's endpoint answers a scrape while a request is being admitted. | Test |
| FR-015-AC-6 | With 70 distinct lane addresses and `max_lane_labels` of 64, the output has 64 `lane` values plus `other`, each a `server:workspace:tab` address. | Test |
| FR-015-AC-7 | Each series appears in a live Prometheus scrape when its producer is available. The Grafana fleet dashboard (delivered with SWM-242) and ix-board fleet view read slots busy, configured and sustainable slots, queue wait by priority and disk use with host and observation time; they read pause seconds when the pause-time producer is available. | Demonstration |
| FR-015-AC-8 | Every member of the closed FR-015 outcome set is present for each priority class before any request ends. For each non-abort member of FR-010's termination-reason type, including `rss_cap` and `pause_exceeded`, a scripted request ended for that reason raises exactly the matching `ix_build_builds_total{outcome}` value by one and no other. The same applies to `ok`, `failed`, `timed_out`, and cancellation while queued or running (`cancelled`). Abort outcome series are present at zero in this slice; this criterion verifies their initialization only and does not verify abort execution, classification, or incrementing an abort outcome. No outcome outside the closed set is exported. | Test |
| FR-015-AC-9 | With no ended request, `ix_build_builds_total` is 0 for every closed outcome value under each of `check`, `test` and `gate`; after one `check` request ends `failed`, that series reads 1 and every other value, including all `aborted_*` values, stays 0. | Test |
| FR-015-AC-10 | With at least one request ended in each non-abort outcome and one whose owner is lost and which `recover` then ends, the recovered request raises exactly one value by one. Every `ix_build_builds_total` value, including abort outcome values held at zero, is equal before and after a scheduler restart, a second `recover` and a `prune`. This criterion does not verify abort execution, classification, or incrementing an abort outcome. | Test |
| FR-015-AC-11 | With multiple queued waiters, one host-wide admission-blocked interval accrues once, not once per waiter, only while the selected next eligible queued request is denied by a resource admission check. Time blocked only by capacity, FIFO/priority ordering, or pause does not accrue. The selected reason follows the documented mapping and complete seven-value precedence: `probe`, `host_load`, `target_disk`, `memory`, `swap`, `compressor`, `operator`. | Test |
| FR-015-AC-12 | Before the SWM-239 TOML profile exists, `ix_build_slots_configured` equals the locked-build per-host JSON host policy's `capacity_units`; after it exists, the value equals TOML `[host].max_slots`. Neither configured value is used to derive sustainable slots. Unsupported `operator`, `swap`, and `compressor` admission-blocked reason sources, and pause-time sources without a producer in this build, produce no series rather than zero-valued series. | Test |
| FR-015-AC-13 | Given a wrapper-admitted command and an observer invocation, the command starts immediately even when other build slots are occupied. The observer makes no queue, admission, resource, priority, hold-deadline, or termination decision for that command. | Test |
| FR-015-AC-14 | For each observer failure case (missing or unwritable state directory, corrupt state, invalid configuration, bounded lock timeout, and observed/admitted store-mode mismatch), the invocation emits exactly one warning, performs no observer writes, and starts the command without waiting beyond the observer's bounded lock-timeout interval. | Test |
| FR-015-AC-15 | A command run through `observe` has the same observable exit status, including signal termination, stdin/stdout/stderr, environment, working directory, and OS group membership as the command run directly. Tests send SIGINT and SIGTERM to that group and verify delivery to the child and its termination. | Test |
| FR-015-AC-16 | While an observed command runs, occupancy is recorded once and released at command completion. Recovery of a dead observer reclaims its busy slot. `ix_build_slots_configured` matches the host configuration's count of slots the external wrapper can admit. | Test |
| FR-015-AC-17 | With `--kind build` and a valid `--priority`, exit code 0 increments that priority's `ix_build_builds_total{outcome="ok"}` and any nonzero exit or signal termination increments its `outcome="failed"` series, unless an explicit, independently known termination cause selects another matching closed outcome. With `--kind build` but no priority, the terminal result and raw exit code or signal are recorded without incrementing a priority-labeled outcome series. With `--kind test`, the same outcome mapping increments `ix_build_test_runs_total` regardless of whether priority was hinted. The raw exit code or signal is retained separately. With no `--kind`, the terminal result is recorded without kind classification and neither outcome family is incremented; the kind is not inferred from the command. | Test |
| FR-015-AC-18 | A supplied `--priority` accepts only `check`, `test`, or `gate` and is used as an attribution hint, not an admission priority. When `--priority` is absent, no priority-labeled outcome or queue-wait histogram is incremented, and no real priority value is substituted. | Test |
| FR-015-AC-19 | Queue wait is recorded only when both `--queued-at-ms` and a valid `--priority` are supplied; with either absent, no queue-wait histogram observation is added. | Test |
| FR-015-AC-20 | Queue depth, admission-blocked seconds, and pause series have no observed value in observe mode and are absent, not zero. A state containing admitted requests is handled by the warning and fail-open behavior in FR-015-AC-14. | Test |

## Dependencies

- [FR-001](FR-001-evidence-contract.md), evidence envelope consumed by ix-board.
- [FR-005](FR-005-fair-build-scheduler.md), events and snapshot.
- [FR-010](FR-010-scheduler-owned-throttling.md), governor, pause and termination reasons, end cause, and orphan state.
- [FR-011](FR-011-priority-classes-lane-fair-share.md), priority classes and lane addresses.
- ix-board fleet view (Linear W2, not yet delivered): consumer of the snapshot; AC-7 cannot be demonstrated before it ships.
- The Grafana fleet dashboard (Linear SWM-242): consumer of the Prometheus series.
