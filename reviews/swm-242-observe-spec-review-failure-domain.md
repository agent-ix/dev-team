---
id: SR-056
title: "Failure-domain analysis of SWM-242 observe mode"
type: SpecReview
analysis: failure-domain
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md (PR #41 diff, head 078c982b9bf6ffdabd4c9d373d64819bb7f79212); related FR-005, FR-009, FR-010, FR-011, FR-016, NFR-002"
review_set: subset
---

## Summary

Ticket: SWM-242. Probed invalid input, signal delivery, observer death and failures after command start; each can refuse, alter or misreport a build under the current text.

## Verdict

**FAIL**: three high and one medium finding.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | Bad observer arguments are not fail-open: AC-18 says priority accepts only three values, which permits refusing to run the build, and an invalid kind, a malformed or future queued-at value and its unit are unspecified. | spec/functional/FR-015-build-metrics-export.md:47, spec/functional/FR-015-build-metrics-export.md:92 |
| FND-002 | high | Signal transparency covers only group signals. A signal to the PID the caller started may miss the command, a group signal may be forwarded twice, and the observer may exit first and release the wrapper's slot; fail-open runs and inherited descriptors are not covered. | spec/functional/FR-015-build-metrics-export.md:51, spec/functional/FR-015-build-metrics-export.md:89 |
| FND-003 | high | Dead-observer reclaim defines no outcome, liveness test or trigger. Existing recovery ends a lost running request as failed (AC-10), which would export an unknown result as a failure, and the slot may be freed while the command still runs. | spec/functional/FR-015-build-metrics-export.md:47, spec/functional/FR-015-build-metrics-export.md:90 |
| FND-004 | medium | Failures after the command starts, such as a failed or blocked completion write, are not covered: fail-open is defined only before recording, so exit status and exit delay are unconstrained. | spec/functional/FR-015-build-metrics-export.md:49 |

## Replacement Text

### FND-001

spec/functional/FR-015-build-metrics-export.md:47, insert after the sentence ending "never supplies a default priority that appears real.":

```text
An unrecognized observer option, a `--kind` or `--priority` value outside its set, or a `--queued-at-ms` value that is not a non-negative integer of Unix epoch milliseconds at or before command start emits one warning, is treated as not supplied, and never prevents or delays the command.
```

spec/functional/FR-015-build-metrics-export.md:92, replace the FR-015-AC-18 row with:

```text
| FR-015-AC-18 | `--priority` is an attribution hint, not an admission priority, and only `check`, `test` and `gate` are recorded. For an unknown observer option, `--priority urgent`, `--kind lint`, and `--queued-at-ms` values `abc`, `-1` and a future time, the command runs with its own exit status, one warning is emitted and the value is treated as not supplied. When `--priority` is absent, no priority-labeled outcome or queue-wait histogram is incremented, and no real priority value is substituted. | Test |
```

### FND-002

spec/functional/FR-015-build-metrics-export.md:51, replace the whole paragraph with:

```text
On both the recorded and the fail-open path, the command SHALL keep the caller's exit status including signal termination, stdin, stdout, stderr, every other inherited file descriptor, environment, working directory, process group, signal dispositions and signal mask, and SHALL inherit no observer file descriptor. A signal sent to the process group reaches the command exactly once. A catchable signal sent only to the process ID the caller started reaches the command exactly once, and that process does not exit before the command has terminated. SIGKILL or SIGSTOP sent only to that process ID may not reach a separate command process; this is the only exception, and host adoption SHALL confirm that the wrapper sends them to the process group or cgroup. No observer process keeps the command's stdio open more than 1000 ms after the command exits.
```

spec/functional/FR-015-build-metrics-export.md:89, replace the FR-015-AC-15 row with:

```text
| FR-015-AC-15 | On the recorded path and on each fail-open path, a command run through `observe` has the same exit status or terminating signal, stdin/stdout/stderr (apart from observer warning lines), inherited descriptors, environment, working directory, process group, signal dispositions and mask as a direct run. SIGINT, SIGTERM and SIGHUP, sent once to the group and separately once to only the process ID the caller started, each reach a trapping command exactly once and terminate a non-trapping one, and the caller-started process does not exit before the command. Pipes from the command reach end of file within 1000 ms of its exit. | Test |
```

### FND-003

spec/functional/FR-015-build-metrics-export.md:47, replace the sentence "Occupancy is recorded while the command runs, and a dead observer's busy slot is reclaimed." with:

```text
Occupancy of one slot is recorded while the command runs. The slot stays busy while the command is alive, even if the observer is dead. Once neither is verified alive (a reused process ID does not count), the next `observe` invocation or metrics export no longer counts the slot, and no outcome, exit code or signal is recorded for it.
```

spec/functional/FR-015-build-metrics-export.md:90, in FR-015-AC-16, replace the sentence "Recovery of a dead observer reclaims its busy slot." with:

```text
With only the observer killed, the slot stays busy until the command exits. With observer and command both killed, the next export reports the slot free and every `ix_build_builds_total` and `ix_build_test_runs_total` value is unchanged; FR-015-AC-10 does not apply to observed commands.
```

### FND-004

spec/functional/FR-015-build-metrics-export.md:49, insert after the sentence ending "runs the command without observer writes.":

```text
A failure after the command has started, including a failed or timed-out completion write, emits one warning, counts no outcome that was not durably recorded, and leaves the command's exit status or terminating signal unchanged.
```

Append this row after FR-015-AC-20:

```text
| FR-015-AC-21 | With the state directory made unwritable, the state corrupted, or the state lock held indefinitely after the command has started, `observe` ends with the command's own status or signal within 1000 ms of the command's exit, emits one warning, and records no partial outcome. | Test |
```

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-005 | medium | The new occupancy text records no outcome once observer and command are both dead, which literally includes a normal completion, and AC-16 no longer requires release at command completion. The wording came from the FND-003 replacement text. | spec/functional/FR-015-build-metrics-export.md:47, spec/functional/FR-015-build-metrics-export.md:96 |

## Replacement Text (disposition pass 1)

### FND-005

spec/functional/FR-015-build-metrics-export.md:47, replace the sentence beginning "Once neither is verified alive" with:

```text
A live observer releases the slot when the command completes. If neither is verified alive (a reused process ID does not count) and no completion was recorded, the next `observe` invocation or metrics export no longer counts the slot, and no outcome, exit code or signal is recorded for it.
```

spec/functional/FR-015-build-metrics-export.md:96, in FR-015-AC-16, replace the text from "While an observed command runs" through "a reused process ID does not count as alive." with:

```text
While an observed command runs, occupancy is recorded once, and a live observer releases it when the command completes. The slot remains busy while the command is alive even if the observer dies. When observer and command are both dead and no completion was recorded, the next export reports the slot free without recording an outcome, exit code or signal; a reused process ID does not count as alive.
```

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | Round 1, head 193bf7d: the invalid-argument paragraph is at line 51 and AC-18 is replaced. |
| FND-002 | fixed | Round 1, head 193bf7d: line 55 and AC-15 carry the minder-amended signal contract (at-least-once delivery, at most twice, PID-only SIGKILL and SIGSTOP excepted) and keep the other transparency terms. |
| FND-003 | fixed | Round 1, head 193bf7d: line 47 and AC-16 define liveness, the export trigger and no recorded outcome. The residual wording defect is FND-005. |
| FND-004 | fixed | Round 1, head 193bf7d: the post-start failure paragraph is at line 53 and AC-21 is added. |
| FND-005 | still-open | Round 1, head 193bf7d: found in this pass; no fix has landed. |
