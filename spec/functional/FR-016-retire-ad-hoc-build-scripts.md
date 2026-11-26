---
id: FR-016
title: Cover and retire the ad hoc build scripts
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-003
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-005
    type: depends_on
---
# FR-016: Cover and retire the ad hoc build scripts

## Description

The shipped Rust tool provides shared Cargo admission and execution through the
PATH `cargo` shim or an explicit
`locked-build run --class <must-fix|point|block|periodic> -- cargo ...`
invocation. In `lease_accounted` mode, each lease is charged and enforced at
its configured memory cap; admission fits the requested cap plus active lease
caps within `memory_budget_bytes`. The additional wrapper functions and
retirement checks below are target requirements; each row distinguishes current
shipped behavior from work that remains to be implemented. The tool is Rust
only, with no Python and no logic-bearing shell.

## Behavior

Each retired function maps to a requirement:

| Retired function | Shipped locked-build behavior | Remaining target requirement |
|---|---|---|
| Slot wrapper: first-free lockf slot, hand-tuned slot count | `run`, `status`, `cancel`, and `recover` use the configured capacity and persistent queue. | FR-005 queue/reservation behavior and FR-009 sustainable-capacity policy. |
| Slot wrapper: priority marker for merge-ready gates | `run --class` and `LOCKED_BUILD_CLASS` support `must-fix`, `point`, `block`, and `periodic`; direct runs default to `periodic`, the Cargo shim to `point`. | FR-011 lane-address validation and cross-lane fair share are not shipped. |
| Slot wrapper: default `CARGO_BUILD_JOBS` | Policy supports `cargo_build_jobs`, `rust_test_threads`, and `cargo_incremental`; the scheduler scales Cargo jobs by active leased units. | FR-009 `jobs_per_slot` is not a policy field in `dev-tools/tools/locked-build/src/config.rs`. |
| Remote runner: build a pushed sha in an isolated checkout and target | No remote-dispatch or repository-pool command is exposed by `tools/locked-build/src/main.rs`. | FR-012 target modes and FR-014 pushed-sha dispatch. |
| Remote runner: rc, test result lines, failure and panic lines | `run` returns the child exit status; `status` exposes request states and transitions. | FR-013 structured result summary and test-output parsing. |
| Remote runner: hold file, memory and disk gates before start | Policy supports `memory_admission`, `memory_budget_bytes`, per-class `memory_cap_by_class`, `disk_reserve_bytes`, and `maximum_load`; no hold-file interface is shipped. | FR-010 hold/thermal controls and any host-specific hold-file migration. |
| Remote runner: CPU set, nice level, debug-info and incremental env | `cargo_incremental` and Cargo job/thread settings are supported; `cpu_set`, `[weight] nice`, and `[env]` are absent from `dev-tools/tools/locked-build/src/config.rs`. | FR-009 host/weight/env policy behavior and `jobs_per_slot` remain target requirements. |
| Remote runner: per-test RSS watchdog | Per-lease caps use `memory_cap_by_class` and are enforced by cgroup/RSS watchdog; `memory_cap_bytes` is a derived request field, not a host-policy key. | Per-test caps or request overrides governed by `[request_limits]` are not shipped in `dev-tools/tools/locked-build/src/config.rs`. |
| Heat guard: stop at high Tctl, resume lower; memory stop | `sample` collects configured read-only sources and `status` reports scheduler state; neither pauses nor resumes builds. | FR-009 probes and FR-010 thermal/limit controls. |
| Health logger: Tctl, load, memory, fans every 30 s; HOT marker | `sample` and `metrics` exist for configured sources; there is no general fan/HOT-marker logger. | Host-specific health logging and thermal marker behavior. |
| Host admission wrapper: FIFO/load gate and lane locks | `run`, `status`, `cancel`, and `recover` provide shared queue and lease supervision. | Any remaining host-specific lane-lock migration. |
| Per-lane Cargo admission | PATH `cargo` shim or `run --class <must-fix|point|block|periodic> -- cargo ...`; policy key `real_cargo` selects real Cargo. | No additional admission wrapper is required for Cargo. |
| Per-ticket build/test admission | PATH `cargo` shim or `run --class <must-fix|point|block|periodic> -- cargo ...`; lease supervision applies to the command. | Repository-specific gate orchestration remains outside the scheduler. |

**Retirement gate.** Existing builds finish under their original wrappers. An
operator uses `status` and `metrics` evidence over a 24-hour window before
removing a host or lane entry point. The intended window must contain at least
one completed build, zero `admission_stall` events (a request waited longer
than `stall_wait` while a slot was free and no admission block reason applied),
and zero `paused_orphan` events (a paused group had no live owner at a sample).
At present, `tools/locked-build/src/metrics.rs` does not produce
`ix_build_paused_orphans`, and `tools/locked-build/src/sample.rs` has no
`admission_stall` source. Until those producers exist, both observations are
unavailable: missing series or events do not count as zero, and this gate stays
pending rather than passing.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-016-AC-1 | The parity table distinguishes shipped commands and policy keys from target requirements; each claimed shipped subcommand appears in `locked-build --help` and each claimed shipped policy key exists in the host policy schema. Class selection is exercised by FR-011-AC-1. | Test |
| FR-016-AC-2 | Target requirement: once the FR-009 profile controls ship, a job starts with configured `cpu_set`, `[weight] nice`, and `[env]` values, `CARGO_BUILD_JOBS` follows `jobs_per_slot`, and `[request_limits]` accepts in-range overrides and refuses out-of-range values. The current host policy schema in `dev-tools/tools/locked-build/src/config.rs` has none of `cpu_set`, `[weight] nice`, `[env]`, `jobs_per_slot`, or `[request_limits]`; it instead exposes `cargo_build_jobs`, `rust_test_threads`, and `cargo_incremental`. | Test |
| FR-016-AC-3 | The tool tree contains no `.py` file and no shell script with a conditional or loop; Makefile recipes invoke only `cargo` and the built binary. | Inspection |
| FR-016-AC-4 | Current status: the retirement gate is unobservable until `admission_stall` and `paused_orphan` producers ship; missing observations never count as zero. Target requirement: with producer-backed `status` and `metrics` fixtures, a request waiting 6 minutes with a free slot reports the stall, a paused orphan is reported, and a 24-hour window with at least one build and neither event passes; with no builds it remains unproven and the entry point stays. | Test |
| FR-016-AC-5 | The reference and migration guide state the cutover order and name `status` and `metrics` as the evidence used for each retirement decision. | Inspection |

## Dependencies

- [FR-009](FR-009-host-profile-sustainable-slots.md), [FR-010](FR-010-scheduler-owned-throttling.md), [FR-011](FR-011-priority-classes-lane-fair-share.md), [FR-012](FR-012-target-dir-pool.md), [FR-013](FR-013-structured-job-output.md), [FR-014](FR-014-remote-dispatch-pushed-sha.md) and [FR-015](FR-015-build-metrics-export.md).
