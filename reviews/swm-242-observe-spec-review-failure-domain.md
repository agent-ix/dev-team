---
id: SR-067
title: "Failure-domain analysis of the SWM-242 observe contract wording"
type: SpecReview
analysis: failure-domain
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md (PR #43 diff, head 890d7a78a4a68ac64fc5e89a8bd257f4112e7b67), checked against agent-ix/dev-tools locked-build at bce5f4a7a20000a56275e3bc49b290fc1053732d"
review_set: subset
---

## Summary

Ticket: SWM-242. Probed PID-only signal delivery and observer death. The exit-order guarantee does not hold for signals that end the observer.

## Verdict

**CONDITIONAL**: one medium finding.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | The caller-started process is said not to exit before the command terminates, yet a PID-only SIGKILL, or an unforwarded terminating signal such as SIGFPE, SIGILL, SIGPWR or a real-time signal, ends the observer while the command keeps running. Reproduced on macOS and Linux. | spec/functional/FR-015-build-metrics-export.md:55, spec/functional/FR-015-build-metrics-export.md:95 |

## Replacement Text

### FND-001

spec/functional/FR-015-build-metrics-export.md:55, replace "The caller-started process does not exit before the command has terminated." with:

```text
The caller-started process does not exit before the command has terminated, except when SIGKILL or a terminating signal outside that list is sent only to it.
```

spec/functional/FR-015-build-metrics-export.md:95, replace "The caller-started process does not exit before the command terminates." with:

```text
The caller-started process does not exit before the command terminates, except when SIGKILL or a terminating signal outside that list is sent only to it.
```


## Dispositions

Applied by the dev-team #43 follow-up at head `002c2f1b0519adda61fac278a03c79e78e3ede54`.

| FND | outcome | reason |
| --- | ------- | ------ |
| FND-001 | fixed | The caller-started process exit guarantee now explicitly excludes SIGKILL and terminating signals outside the enumerated forwarded set when sent only to that process. |
