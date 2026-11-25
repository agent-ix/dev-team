---
id: SR-053
title: "Base spec review of SWM-242 observe mode"
type: SpecReview
analysis: base
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md (PR #41 diff, head 078c982b9bf6ffdabd4c9d373d64819bb7f79212); related FR-005, FR-009, FR-010, FR-011, FR-016, NFR-002"
review_set: subset
---

## Summary

Ticket: SWM-242. Checked the new observe-mode statements and FR-015-AC-13 to AC-20 against the retained metric contract; observed stores can still export zeros for unknown values, and the configured-slot criterion has two oracles.

## Verdict

**FAIL**: one high and one medium finding. Requirement and criterion ids are unique and contiguous; no hash, digest or pin was added.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | Observed stores still export zeros for unknown values: the retained closed-outcome rule initialises every outcome (including timed_out, cancelled and all aborts) for every priority, even with no priority hint, and AC-19 permits a zero-count queue-wait histogram. AC-20 omits only three series families and names no export surface. | spec/functional/FR-015-build-metrics-export.md:49, spec/functional/FR-015-build-metrics-export.md:94 |
| FND-002 | medium | AC-16 requires the configured-slots gauge to match both the host configuration and the external wrapper's admission count, which the tool cannot observe; when they differ no implementation can pass. Busy above configured is also unspecified. | spec/functional/FR-015-build-metrics-export.md:49, spec/functional/FR-015-build-metrics-export.md:90 |

## Replacement Text

### FND-001

spec/functional/FR-015-build-metrics-export.md:49, replace the sentence beginning "Queue depth, admission-blocked time, and pause series require scheduler-owned state" with:

```text
In an observed store, overriding the closed-outcome-set zero initialization above, the **Build outcomes** paragraph below, and FR-015-AC-1, AC-8 and AC-9: `ix_build_builds_total` has only `ok` and `failed` series, for a priority only once a `--kind build` command with that priority has started; `ix_build_test_runs_total` has only `ok` and `failed` series, only once a `--kind test` command has started; `ix_build_queue_wait_seconds` has series only for a priority with at least one observation; and `ix_build_queue_depth`, `ix_build_admission_blocked_seconds_total`, `ix_build_pause_seconds_total` and `ix_build_paused_orphans` have no series. The Prometheus text and the JSON snapshot omit these values and never report them as zero.
```

spec/functional/FR-015-build-metrics-export.md:94, replace the FR-015-AC-20 row with:

```text
| FR-015-AC-20 | For an observed store, `metrics`, the governor endpoint and the JSON snapshot contain no queue-depth, admission-blocked, pause or paused-orphan value; no `ix_build_builds_total` series other than `ok` and `failed` for a priority with a started `--kind build` command; no `ix_build_test_runs_total` series before a `--kind test` command starts, and only `ok` and `failed` after; and no queue-wait series for a priority without an observation. After only commands without `--kind` and `--priority`, no build, test-run or queue-wait series appears. | Test |
```

### FND-002

spec/functional/FR-015-build-metrics-export.md:49, replace the sentence beginning "The configured-slots gauge uses" with:

```text
The configured-slots gauge uses the host configuration source above. The host configuration value SHALL be set to the number of build slots the external wrapper can admit; the observer neither measures nor enforces that number, and `ix_build_slots_busy` is exported unclamped when it exceeds the configured value.
```

spec/functional/FR-015-build-metrics-export.md:90, in FR-015-AC-16, replace the sentence beginning "`ix_build_slots_configured` matches" with:

```text
`ix_build_slots_configured` equals the host configuration's `capacity_units`, or `[host].max_slots` once the TOML profile exists.
```
