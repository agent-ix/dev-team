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

The scheduler SHALL export per-host metrics in Prometheus text format and as the versioned JSON snapshot ix-board reads, so that queue wait, configured and sustainable slot capacity, pause time, admission blocking, and disk use can be seen for every host, including source-based samples of build activity without changing external wrappers.

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

The `lane` label is the bounded lane address `server:workspace:tab` of [FR-011](FR-011-priority-classes-lane-fair-share.md), never a session id. At most `max_lane_labels` (default 64) distinct lanes are labelled; others are summed under `other`. Until the SWM-239 TOML profile exists, `ix_build_slots_configured` for an admitted store is sourced from the `capacity_units` field in the locked-build per-host JSON host policy. After that profile exists, it is sourced from TOML `[host].max_slots`. It is a configured server-capacity value in either state; no sustainable value is derived from it. FR-009's sustainable slot count is computed separately from its TOML profile and live probes, and is unavailable before that profile exists. A series with no producer in the current build is absent until its producer exists, never exported as zero. The current locked-build implementation emits six metric names from this table: `ix_build_queue_depth`, `ix_build_queue_wait_seconds`, `ix_build_slots_busy`, `ix_build_slots_configured`, `ix_build_builds_total`, and `ix_build_admission_blocked_seconds_total`. The complete current-build absence set includes these 11 additional metric names from the table: `ix_build_slots_max`, `ix_build_paused_orphans`, `ix_build_probe_defect`, `ix_build_agent_processes`, `ix_build_agent_rss_bytes`, `ix_build_test_runs_total`, `ix_build_target_dir_bytes`, `ix_build_target_dir_slots`, `ix_build_probe_value`, `ix_build_probe_unavailable`, and `ix_build_lane_running`. It also includes `ix_build_pause_seconds_total` until a pause-time producer exists, `ix_build_slots_sustainable` before the TOML profile exists, and the `operator`, `swap`, and `compressor` reason series of `ix_build_admission_blocked_seconds_total` until their respective producers exist. The absent pause series retains the declared `thermal` and `operator` reasons. These current-build omissions do not remove the series or labels from the metrics contract. The current-build lists above describe admitted stores. The **Sampler mode** rules below define which series a read-only sample can produce from configured host sources; sampler output remains subject to the same source-based omission rule. For admitted governor stores, the closed `ix_build_builds_total` outcome set is an explicit exception to source-based omission: every outcome value is always emitted for every priority class, initialized to zero before a matching terminal event occurs, including abort outcomes.

For admission-blocked time, the complete `reason` set is `memory`, `swap`, `compressor`, `host_load`, `target_disk`, `operator`, and `probe`. `ix_build_admission_blocked_seconds_total` measures one host-wide interval, counted once regardless of waiter count, only while the scheduler's selected next eligible queued request is denied by a resource admission check. Time waiting only for capacity, FIFO or priority ordering, and all pause time is excluded. When multiple reasons apply to the selected request, use this complete precedence from highest to lowest: `probe` for a missing, invalid or stale host sample; `host_load`; `target_disk`; `memory`; `swap`; `compressor`; `operator`. While an operator hold or any pause is in effect this counter accrues under no reason, even when a resource limit also applies; `operator` stays in the reason set as FR-010's refusal reason, and its time is counted only in `ix_build_pause_seconds_total`. The exact current-build producer mapping is `memory` = `memory_reserve`, `target_disk` = `disk_reserve`, `host_load` = `host_load`, and `probe` = missing/invalid/stale host sample. Agent processes are counted by the profile's command patterns. Counters derive from persisted transition events, so they stay monotonic across restarts and prune. Labels exclude ticket ids, request ids, command text and environment. Reading metrics takes no admission decision and never blocks admission longer than the state-read time. A source that cannot be read is reported through `ix_build_probe_unavailable`, not as zero.

**Sampler mode.** `locked-build sample --config <host.json> --output <textfile>` samples the configured sources for that host and writes Prometheus text only to the requested output file. It does not create or update the versioned JSON status snapshot. JSON snapshot guarantees apply to the governor/admitted-store path; sampler-only values are not added to that snapshot. A one-minute timer invokes this command. Sampling reads only the configured process metadata, read-only lock ownership metadata, and filesystem measurements. It does not launch or wrap build commands, read command traces, acquire or change build locks, change admission or wrapper behavior, send signals, pause or cancel processes, or write build sources, target directories, or unrelated files. No persistent sampler state is needed for the instantaneous activity and disk measurements in this slice. Persistent state may be written only when needed to count a terminal outcome truthfully, and only under a sampler-owned state path.

Each host adapter uses only its named source. Draco counts distinct processes holding the six `qsl-slot` lock files, using process-table and open-file/lock ownership data; `ix_build_slots_configured` is 6 from those six paths. Terra counts distinct processes holding ordinary lane locks as shown by `/proc/<pid>/fdinfo/<fd>` lock lines; it has twelve ordinary lanes, so `ix_build_slots_configured` is 12. Kani remains separate and is excluded. Titan counts controller-admitted jobs together with `arch-test-run.sh` lock holders, de-duplicating the same process when it appears in both sources; there is no truthful fixed host capacity, so no configured-slots series is emitted. Luna counts live Cargo build/test command trees; no truthful fixed host capacity is configured, so no configured-slots series is emitted. When identities cannot be de-duplicated safely, the affected busy metric is omitted. The sampler SHALL not infer a host capacity from current concurrency.

The sampler emits `ix_build_slots_busy` only when the host source can count active work. It emits `ix_build_slots_configured` only for Draco and Terra with the sourced values above. It emits `ix_build_queue_depth` only when the adapter can directly count queued waiters; a lock holder, queue marker, or held flag alone is not a waiter count. It emits `ix_build_target_dir_bytes` only for target directories explicitly configured and successfully measured, using the existing `repo` label. It emits `ix_build_builds_total` or `ix_build_test_runs_total` only when the adapter can count terminal outcomes from a truthful source; this slice has no specified terminal-outcome source, so the sampler emits neither outcome family. It does not synthesize zero-valued series for unsupported or unobservable measurements.

A source failure omits only the metrics derived from that source; sampling continues for independent sources. The sampler records a diagnostic with the bounded source identity and failure reason in its standard error (captured by the timer's journal). When the unavailable-probe producer is available, it may emit `ix_build_probe_unavailable{probe="<bounded-source>"} 1`; it does not add an unbounded error or path label to Prometheus. The metric series for the failed measurement itself remains absent, never zero.

Replacing the matching scripts under `_lead-bin` is a separate future adoption acceptance item. This sampler change does not modify or claim replacement of those scripts; that acceptance item remains unmet until the future adoption work does so.

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
| FR-015-AC-1 | After a scripted sequence of queued, running and finished requests, every series in the table whose producer exists in the build under test appears with its expected value and labels, and every other series and reason label is absent rather than zero; `promtool check metrics` accepts the output. For admitted stores, every `ix_build_builds_total` closed outcome value is present for each priority class, including values with no terminal event, which read as zero. | Test |
| FR-015-AC-2 | For an admitted store, before the SWM-239 TOML profile exists, `ix_build_slots_busy` and `ix_build_slots_configured` match occupied units and the JSON host policy's `capacity_units`; no sustainable value is derived or exported. After the profile exists, configured slots match TOML `[host].max_slots`, sustainable slots match the independently computed sustainable count, and all three values match the snapshot at the same sample. | Test |
| FR-015-AC-3 | Counters do not decrease across a scheduler restart or after `prune`. | Test |
| FR-015-AC-4 | A required probe that is unavailable yields `ix_build_probe_unavailable` of 1 and no fabricated value; the exposition contains no ticket id, request id, command argument or environment value. | Test |
| FR-015-AC-5 | A fixture with 10 000 retained requests produces the exposition in under 200 ms and the governor's endpoint answers a scrape while a request is being admitted. | Test |
| FR-015-AC-6 | With 70 distinct lane addresses and `max_lane_labels` of 64, the output has 64 `lane` values plus `other`, each a `server:workspace:tab` address. | Test |
| FR-015-AC-7 | Each series appears in a live Prometheus scrape when its producer is available. The Grafana fleet dashboard (delivered with SWM-242) and ix-board fleet view read slots busy, configured and sustainable slots, queue wait by priority and disk use with host and observation time; they read pause seconds when the pause-time producer is available. | Demonstration |
| FR-015-AC-8 | Every member of the closed FR-015 outcome set is present for each priority class before any request ends. For each non-abort member of FR-010's termination-reason type, including `rss_cap` and `pause_exceeded`, a scripted request ended for that reason raises exactly the matching `ix_build_builds_total{outcome}` value by one and no other. The same applies to `ok`, `failed`, `timed_out`, and cancellation while queued or running (`cancelled`). Abort outcome series are present at zero in this slice; this criterion verifies their initialization only and does not verify abort execution, classification, or incrementing an abort outcome. No outcome outside the closed set is exported. | Test |
| FR-015-AC-9 | With no ended request, `ix_build_builds_total` is 0 for every closed outcome value under each of `check`, `test` and `gate`; after one `check` request ends `failed`, that series reads 1 and every other value, including all `aborted_*` values, stays 0. | Test |
| FR-015-AC-10 | With at least one request ended in each non-abort outcome and one whose owner is lost and which `recover` then ends, the recovered request raises exactly one value by one. Every `ix_build_builds_total` value, including abort outcome values held at zero, is equal before and after a scheduler restart, a second `recover` and a `prune`. This criterion does not verify abort execution, classification, or incrementing an abort outcome. | Test |
| FR-015-AC-11 | With multiple queued waiters, one host-wide admission-blocked interval accrues once, not once per waiter, only while the selected next eligible queued request is denied by a resource admission check. Time blocked only by capacity, FIFO/priority ordering, or pause does not accrue. The selected reason follows the documented mapping and complete seven-value precedence: `probe`, `host_load`, `target_disk`, `memory`, `swap`, `compressor`, `operator`. | Test |
| FR-015-AC-12 | For an admitted store, before the SWM-239 TOML profile exists, `ix_build_slots_configured` equals the locked-build per-host JSON host policy's `capacity_units`; after it exists, the value equals TOML `[host].max_slots`. Neither configured value is used to derive sustainable slots. Unsupported `operator`, `swap`, and `compressor` admission-blocked reason sources, and pause-time sources without a producer in this build, produce no series rather than zero-valued series. | Test |
| FR-015-AC-13 | `locked-build sample --config <host.json> --output <textfile>` reads only the configured sample sources and writes its requested output. The sample starts no build command, acquires or changes no build lock, changes no build-process state, reads no command trace, writes no build source or target directory, does not change admission state, and sends no signal. It writes no persistent sampler state for instantaneous activity or disk measurements. | Test |
| FR-015-AC-14 | A one-minute timer invokes `locked-build sample --config <host.json> --output <textfile>`; the timer does not replace or wrap any host build command. | Test |
| FR-015-AC-15 | With source fixtures matching the host mappings, Draco reports busy lock holders and `ix_build_slots_configured=6`; Terra reports ordinary lane lock holders and `ix_build_slots_configured=12`, excluding Kani; Titan counts controller-admitted jobs and `arch-test-run.sh` lock holders without double-counting a PID and omits configured slots; Luna counts live Cargo build/test command trees and omits configured slots. A busy metric is omitted when its source cannot be counted or identities cannot be de-duplicated safely. | Test |
| FR-015-AC-16 | The sampler emits queue depth only for a source that directly identifies queued waiters; target-directory bytes only for configured, successfully measured directories; and outcome counters only when terminal results can be counted from a truthful source. For the sources specified in this slice, no terminal-outcome source is available, so no build or test outcome series is emitted by the sampler. | Test |
| FR-015-AC-17 | When a source is unsupported, unobservable, or fails to read or parse, only its derived metric series are omitted, never emitted as zero, and independent source metrics are still sampled. A diagnostic identifies the bounded source and failure reason; when its producer is available, `ix_build_probe_unavailable` uses only the bounded `probe` label and value 1. No unbounded error or path label is emitted. | Test |
| FR-015-AC-18 | A sample output contains Prometheus text only, with series supported by successful sources and any available bounded unavailable-probe series. `sample` does not create or change the versioned JSON status snapshot, and no sampler-only value is added to it. Failure to read one source does not suppress unrelated valid series or change a running build. | Test |

## Dependencies

- [FR-001](FR-001-evidence-contract.md), evidence envelope consumed by ix-board.
- [FR-005](FR-005-fair-build-scheduler.md), events and snapshot.
- [FR-010](FR-010-scheduler-owned-throttling.md), governor, pause and termination reasons, end cause, and orphan state.
- [FR-011](FR-011-priority-classes-lane-fair-share.md), priority classes and lane addresses.
- ix-board fleet view (Linear W2, not yet delivered): consumer of the snapshot; AC-7 cannot be demonstrated before it ships.
- The Grafana fleet dashboard (Linear SWM-242): consumer of the Prometheus series.
