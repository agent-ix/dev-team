---
id: SR-063
title: "Code review of the SWM-242 observe contract wording"
type: SpecReview
analysis: code-review
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md (PR #43 diff, head 890d7a78a4a68ac64fc5e89a8bd257f4112e7b67), checked against agent-ix/dev-tools ix-build at bce5f4a7a20000a56275e3bc49b290fc1053732d"
review_set: subset
---

## Summary

Ticket: SWM-242. Checked each changed sentence against the code and the release binary. True at that head: the command starts before configuration or state I/O, the command and the forwarding loop do not wait for the state lock, preflight is abandoned 1000 ms after its worker starts, and completion shares one 1000 ms post-exit deadline (a compound stall returned at 1.03 s). Two sentences are false.

## Verdict

**CONDITIONAL**: one medium and one low finding. Language lanes do not apply to a Markdown-only change.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | The paragraph and AC-15 say every catchable non-stop signal sent only to the caller-started PID is forwarded. SIGPIPE and SIGCHLD are not, nor are SIGILL, SIGFPE and SIGSEGV, nor EMT and INFO on macOS, nor STKFLT, PWR and real-time signals on Linux. Reproduced on both. | spec/functional/FR-015-build-metrics-export.md:55, spec/functional/FR-015-build-metrics-export.md:95 |
| FND-002 | low | A failure is said to leave no further observer writes. A preflight write stalled past 1000 ms still completes after the warning, with its queue wait and kind marker, and the worker then writes again to remove the busy row. Reproduced with a stalled rename. | spec/functional/FR-015-build-metrics-export.md:57 |

## Replacement Text

### FND-001

The list below matches the code once dev-tools#27 stops forwarding SIGXFSZ (SR-005 FND-035) and registers its handlers before spawn (SR-005 FND-037). Without the first change, add SIGXFSZ to both lists; without the second, a signal sent just after the command starts is not forwarded.

spec/functional/FR-015-build-metrics-export.md:55, replace the sentence beginning "A catchable non-stop signal" with these two sentences:

```text
Each of SIGHUP, SIGINT, SIGQUIT, SIGTRAP, SIGABRT, SIGBUS, SIGSYS, SIGALRM, SIGTERM, SIGUSR1, SIGUSR2, SIGCONT, SIGURG, SIGXCPU, SIGVTALRM, SIGPROF, SIGWINCH and SIGIO sent only to the process ID the caller started is forwarded and reaches the command at least once; a group signal may be delivered a second time by forwarding, so each forwarded signal reaches the command at most twice. No other signal sent only to that process ID is forwarded.
```

spec/functional/FR-015-build-metrics-export.md:95, replace the matching sentence in FR-015-AC-15 with:

```text
Each of SIGHUP, SIGINT, SIGQUIT, SIGTRAP, SIGABRT, SIGBUS, SIGSYS, SIGALRM, SIGTERM, SIGUSR1, SIGUSR2, SIGCONT, SIGURG, SIGXCPU, SIGVTALRM, SIGPROF, SIGWINCH and SIGIO sent only to the caller-started process ID is forwarded and reaches the command at least once; a group signal may be delivered a second time by forwarding, so each forwarded signal reaches the command at most twice. No other signal sent only to that PID is forwarded.
```

### FND-002

spec/functional/FR-015-build-metrics-export.md:57, replace "emits one warning and leaves the command running without further observer writes." with:

```text
emits one warning and leaves the command running. A preflight write already in progress at that warning can still complete; the only further write the observer makes is removal of the occupancy row that write added.
```

## New findings (disposition pass 1)

Head 2b91f17ad9c7ab4bb52b5f55d38dda2f26584cb2.

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-003 | medium | The PR writes the five #43 records over the merged #41 records, so merging removes SR-052 to SR-056 and their dispositions from reviews/ on main and makes those ids look unused to the next allocation. Fix: restore the five files from origin/main and add the #43 records under swm-242-pr43- names. | reviews/swm-242-observe-code-review.md:1 |

In /Users/peter/dev/worktrees/dev-team-swm-242-observe2: `git checkout origin/main -- reviews/swm-242-observe-code-review.md reviews/swm-242-observe-spec-review-base.md reviews/swm-242-observe-spec-review-ears-conformance.md reviews/swm-242-observe-spec-review-failure-domain.md reviews/swm-242-observe-spec-review-integrity.md`, then add the reviewer's five files as reviews/swm-242-pr43-code-review.md, -spec-review-base.md, -spec-review-ears-conformance.md, -spec-review-failure-domain.md and -spec-review-integrity.md.

## Dispositions

Round 1, head 2b91f17ad9c7ab4bb52b5f55d38dda2f26584cb2. The FR-015 text equals the proposed edit.

| FND | outcome | reason |
| --- | ------- | ------ |
| FND-001 | fixed | Both statements list the forwarded set, matching the code at fd77413. |
| FND-002 | fixed | An in-flight preflight write and its row removal are allowed. |
| FND-003 | still-open | Found in this pass; restore the #41 records and rename the #43 files. |

Round 2, head 985b805e4c5672afb2f9934e8aa3345ad2b587f5.

| FND | outcome | reason |
| --- | ------- | ------ |
| FND-003 | fixed | The five #41 files equal origin/main and the #43 records are added under swm-242-pr43- names; the diff is those five files and FR-015. |
