---
id: SR-066
title: "Integrity analysis of the SWM-242 observe contract wording"
type: SpecReview
analysis: integrity
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md (PR #43 diff, head 890d7a78a4a68ac64fc5e89a8bd257f4112e7b67), checked against agent-ix/dev-tools locked-build at bce5f4a7a20000a56275e3bc49b290fc1053732d"
review_set: subset
---

## Summary

Ticket: SWM-242. Checked the changed statements for testability and agreement with AC-21. The post-exit bound is now conditional on an undefined path.

## Verdict

**CONDITIONAL**: one medium finding.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | The 1000 ms stdio bound now applies only on the normal forwarding path, which nothing defines, so any overrun can be called off that path. The real exceptions are a stopped observer and a warning blocked on a full stderr pipe (reproduced: a fail-open observe still running after 3 s). | spec/functional/FR-015-build-metrics-export.md:55, spec/functional/FR-015-build-metrics-export.md:95 |

## Replacement Text

### FND-001

spec/functional/FR-015-build-metrics-export.md:55, replace the last sentence with:

```text
Unless a signal has stopped the observer or its warning write to the caller's standard error blocks, no observer process keeps the command's stdio open more than 1000 ms after the command exits.
```

spec/functional/FR-015-build-metrics-export.md:95, replace the last sentence of the AC-15 cell with:

```text
Unless a signal has stopped the observer or its warning write to the caller's standard error blocks, no observer process holds the command's pipes open more than 1000 ms after command exit.
```


## Dispositions

Applied by the dev-team #43 follow-up at head `002c2f1b0519adda61fac278a03c79e78e3ede54`.

| FND | outcome | reason |
| --- | ------- | ------ |
| FND-001 | fixed | AC-15 now names the only exceptions to the 1000 ms stdio release bound: a stopped observer or a warning write blocked on stderr. |
