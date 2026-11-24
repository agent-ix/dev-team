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

The shared Rust tool SHALL provide every function of the slot wrapper, the remote test runner, the heat guard and the health logger, so that those scripts can be deleted. The tool is Rust only, with no Python and no logic-bearing shell.

## Behavior

Each retired function maps to a requirement:

| Retired function | Replacement |
|---|---|
| Slot wrapper: first-free lockf slot, hand-tuned slot count | FR-005 queue; FR-009 sustainable slots |
| Slot wrapper: priority marker for merge-ready gates | FR-011 `gate` class |
| Slot wrapper: default `CARGO_BUILD_JOBS` | FR-009 `jobs_per_slot`, exported to the job |
| Remote runner: build a pushed sha in a per-slot worktree and target | FR-012 slot, FR-014 dispatch |
| Remote runner: rc, test result lines, failure and panic lines | FR-013 summary |
| Remote runner: hold file, memory and disk gates before start | FR-009 required probes and `block_above`; FR-010 `hold` and `resume` |
| Remote runner: CPU set, nice level, debug-info and incremental env | FR-009 `cpu_set`, `[weight] nice`, `[env]` |
| Remote runner: per-test RSS watchdog | FR-010 `rss_cap` |
| Heat guard: stop at high Tctl, resume lower; memory stop | FR-010 governor pause and resume; abort policy |
| Health logger: Tctl, load, memory, fans every 30 s; HOT marker | FR-015 probe series |

**Retirement gate.** Existing builds finish under their original wrappers; a script is deleted only when `locked-build retire-check --since 24h` passes on that host. The governor records an `admission_stall` event whenever a request has waited longer than `stall_wait` (default 5 minutes) while at least one free slot existed and no admission block reason applied, and a `paused_orphan` event whenever a paused group had no live owner at a sample. The check passes when the window of the last 24 hours holds at least one completed build, zero `admission_stall` events and zero `paused_orphan` events. Deleting the scripts in the lead tooling directory is tracked separately (Linear SWM-244).

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-016-AC-1 | A parity table in the tool reference maps each retired function above to a command or profile key, and every mapped command exists in `--help`. | Inspection |
| FR-016-AC-2 | A job starts with the profile's `cpu_set`, `[weight] nice` and `[env]` values and `CARGO_BUILD_JOBS` equal to `jobs_per_slot`; a request override is applied within `[request_limits]` and refused outside (FR-009-AC-10). | Test |
| FR-016-AC-3 | The tool tree contains no `.py` file and no shell script with a conditional or loop; Makefile recipes invoke only `cargo` and the built binary. | Inspection |
| FR-016-AC-4 | With a fixture where a request waits 6 minutes with a free slot, `retire-check` fails and reports the stall; with a paused orphan event it fails; with 24 hours of builds and neither event it passes; with no builds in the window it fails as unproven. | Test |
| FR-016-AC-5 | The reference and migration guide state the cutover order and name `retire-check` as the per-script retirement condition. | Inspection |

## Dependencies

- [FR-009](FR-009-host-profile-sustainable-slots.md), [FR-010](FR-010-scheduler-owned-throttling.md), [FR-011](FR-011-priority-classes-lane-fair-share.md), [FR-012](FR-012-target-dir-pool.md), [FR-013](FR-013-structured-job-output.md), [FR-014](FR-014-remote-dispatch-pushed-sha.md) and [FR-015](FR-015-build-metrics-export.md).
