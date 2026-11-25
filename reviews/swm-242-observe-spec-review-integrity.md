---
id: SR-055
title: "Integrity analysis of SWM-242 observe mode"
type: SpecReview
analysis: integrity
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md (PR #41 diff, head 078c982b9bf6ffdabd4c9d373d64819bb7f79212); related FR-005, FR-009, FR-010, FR-011, FR-016, NFR-002"
review_set: subset
---

## Summary

Ticket: SWM-242. Traced observed commands through FR-005, FR-010 and FR-011; the new text limits only the observe process and only one direction of store mixing.

## Verdict

**FAIL**: one high and one medium finding. FR-015 keeps its existing user-story link and every new criterion names a verification method.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | Nothing says an observed record is not an FR-005 lease. The governor, watchdog, hold, cancel and recover may pause, signal or terminate leased process groups under FR-005 and FR-010, here the caller's own group; AC-13 constrains only the observer's decisions. | spec/functional/FR-015-build-metrics-export.md:47, spec/functional/FR-015-build-metrics-export.md:87 |
| FND-002 | medium | A store must never mix modes, but only observe is told what to do; run or another admitting command against an observed store has no defined refusal and no criterion. | spec/functional/FR-015-build-metrics-export.md:49 |

## Replacement Text

### FND-001

spec/functional/FR-015-build-metrics-export.md:47, insert after the sentence ending "or terminates the observed command.":

```text
An observed command is not an FR-005 request or lease: FR-005, FR-010 and FR-011 admission, ordering, hold, throttling, recovery signalling and termination do not apply to it. No locked-build process or command (`observe`, `serve`, a watchdog, `hold`, `resume`, `cancel`, `recover` or `prune`) originates a signal to the observed command or its process group.
```

spec/functional/FR-015-build-metrics-export.md:87, replace the FR-015-AC-13 row with:

```text
| FR-015-AC-13 | `observe` starts a wrapper-admitted command even when busy slots equal or exceed configured slots, and `ix_build_slots_busy` reports the actual count. With a governor serving the observed store while a thermal or memory limit is breached, after `hold_ms` has elapsed, and across `hold --pause`, `cancel`, `recover` and `prune`, no process in the command's group is signalled, paused or terminated by locked-build. | Test |
```

### FND-002

spec/functional/FR-015-build-metrics-export.md:49, insert after the sentence ending "runs the command without changing the store.":

```text
`run` and every other command that queues or admits work refuse an observed store with a request error and change nothing. The first recorded request fixes the store's mode, and `prune` does not reset it.
```

Append this row after FR-015-AC-20:

```text
| FR-015-AC-22 | `run` against an observed store, including one emptied by `prune`, is refused with a request error and leaves the store unchanged; concurrent first `observe` and `run` invocations on an empty store leave it holding one mode only. | Test |
```

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | Round 1, head 193bf7d: line 49 excludes observed commands from FR-005, FR-010 and FR-011 behavior and AC-13 is replaced. |
| FND-002 | still-open | Round 1, head 193bf7d: AC-22 landed, but the Behavior sentences are absent. Nothing requires every other queueing or admitting command to refuse an observed store, or says the first recorded request fixes the mode. Insert the FND-002 text after "runs the command without changing the store." in line 57. |
| FND-002 | fixed | Round 2, head 07761f1: line 57 requires run and every other queueing or admitting command to refuse an observed store, and fixes the store mode at the first recorded request. |
