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

The shared Rust tool SHALL implement the build admission and execution functions
of the host and per-lane shell wrappers so those wrappers can be retired. Cargo
commands SHALL enter through the PATH `cargo` shim or an explicit
`locked-build run --class <must-fix|point|block|periodic> -- cargo ...`
invocation. In `lease_accounted` mode, each lease is charged and enforced at
its configured memory cap; admission fits the requested cap plus active lease
caps within `memory_budget_bytes`. The tool is Rust only, with no Python and no
logic-bearing shell.

## Behavior

Each retired function maps to a requirement:

| Retired function | Replacement |
|---|---|
| Slot wrapper: first-free lockf slot, hand-tuned slot count | `run`, `status`; FR-005 queue and FR-009 capacity policy |
| Slot wrapper: priority marker for merge-ready gates | `run --class`; FR-011 configured named class |
| Slot wrapper: default `CARGO_BUILD_JOBS` | `run`; FR-009 `jobs_per_slot` and policy `cargo_build_jobs` |
| Remote runner: build a pushed sha in an isolated checkout and target | `run`; FR-012 target modes and FR-014 dispatch |
| Remote runner: rc, test result lines, failure and panic lines | `run`, `status`; FR-013 summary |
| Remote runner: hold file, memory and disk gates before start | `run`; policy `memory_admission`, `memory_budget_bytes`, and `disk_reserve_bytes` |
| Remote runner: CPU set, nice level, debug-info and incremental env | `run`; FR-009 `[host]`, `[weight]`, and `[env]` policy keys |
| Remote runner: per-test RSS watchdog | `run`; policy `memory_cap_bytes` and FR-010 `rss_cap` |
| Heat guard: stop at high Tctl, resume lower; memory stop | `sample`, `status`; FR-009 probe and FR-010 limit policy |
| Health logger: Tctl, load, memory, fans every 30 s; HOT marker | `sample`, `metrics`; FR-015 probe series |
| Host admission wrapper: FIFO/load gate and lane locks | `run`, `status`, `cancel`, `recover` |
| Per-lane Cargo admission | PATH `cargo` shim or `run --class <must-fix|point|block|periodic> -- cargo ...`; cargo-shim policy key `real_cargo` |
| Per-ticket build/test admission | PATH `cargo` shim or `run --class <must-fix|point|block|periodic> -- cargo ...`; FR-005 lease supervision |

**Retirement gate.** Existing builds finish under their original wrappers. An
operator uses `status` and `metrics` evidence over a 24-hour window before
removing a host or lane entry point. The window must contain at least one
completed build, zero `admission_stall` events (a request waited longer than
`stall_wait` while a slot was free and no admission block reason applied), and
zero `paused_orphan` events (a paused group had no live owner at a sample).

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-016-AC-1 | A parity table in the tool reference maps each retired function above to commands or policy keys; every named subcommand appears in `locked-build --help`, and every policy key exists in the host policy schema. Class selection is exercised by FR-011-AC-1. | Test |
| FR-016-AC-2 | A job starts with the profile's `cpu_set`, `[weight] nice` and `[env]` values and `CARGO_BUILD_JOBS` equal to `jobs_per_slot`; a request override is applied within `[request_limits]` and refused outside (FR-009-AC-10). | Test |
| FR-016-AC-3 | The tool tree contains no `.py` file and no shell script with a conditional or loop; Makefile recipes invoke only `cargo` and the built binary. | Inspection |
| FR-016-AC-4 | With a `status` and `metrics` fixture where a request waits 6 minutes with a free slot, the retirement evidence reports the stall; it also reports a paused orphan; with 24 hours of builds and neither event it passes; with no builds in the window it is unproven and the entry point remains. | Test |
| FR-016-AC-5 | The reference and migration guide state the cutover order and name `status` and `metrics` as the evidence used for each retirement decision. | Inspection |

## Dependencies

- [FR-009](FR-009-host-profile-sustainable-slots.md), [FR-010](FR-010-scheduler-owned-throttling.md), [FR-011](FR-011-priority-classes-lane-fair-share.md), [FR-012](FR-012-target-dir-pool.md), [FR-013](FR-013-structured-job-output.md), [FR-014](FR-014-remote-dispatch-pushed-sha.md) and [FR-015](FR-015-build-metrics-export.md).
