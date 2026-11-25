---
id: SR-054
title: "EARS conformance analysis of SWM-242 observe mode"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md (PR #41 diff, head 078c982b9bf6ffdabd4c9d373d64819bb7f79212); related FR-005, FR-009, FR-010, FR-011, FR-016, NFR-002"
review_set: subset
---

## Summary

Ticket: SWM-242. The engine reports one statement, grammar clean, with no grammar finding; semantic review of the new Behavior text and criteria found three unmeasurable or ambiguous responses.

## Verdict

**FAIL**: one high, one medium and one low finding.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | The fail-open delay bound is only called short and bounded and has no value, so AC-14 passes for a one-hour wait; it also covers only the lock wait before start, not configuration reads or state writes. | spec/functional/FR-015-build-metrics-export.md:49, spec/functional/FR-015-build-metrics-export.md:88 |
| FND-002 | medium | Outcome mapping and AC-17 allow an explicit, independently known termination cause to be supplied, but the command has no option or source that supplies one, so the branch cannot be built or tested. | spec/functional/FR-015-build-metrics-export.md:47, spec/functional/FR-015-build-metrics-export.md:91 |
| FND-003 | low | A missing hint may remain "absent or explicitly unknown", which permits an unknown priority label or kind value outside the closed sets. | spec/functional/FR-015-build-metrics-export.md:47 |

## Replacement Text

### FND-001

spec/functional/FR-015-build-metrics-export.md:49, replace "with a short bounded timeout" with:

```text
within the bound below
```

spec/functional/FR-015-build-metrics-export.md:49, replace the sentence "The wait for the state lock is bounded; observer failure adds no command delay beyond that bound." with:

```text
All observer work before the command starts, including reading host configuration, waiting for the state lock and writing state, SHALL finish or be abandoned within 1000 ms of invocation, after which the command starts; observer work after the command exits SHALL finish or be abandoned within 1000 ms of that exit. The state lock is released before the command starts and is not held while it runs.
```

spec/functional/FR-015-build-metrics-export.md:88, replace the FR-015-AC-14 row with:

```text
| FR-015-AC-14 | For each observer failure case (missing or unwritable state directory, corrupt state, invalid configuration, state lock held indefinitely, a configuration path that never returns data, and observed/admitted store-mode mismatch), the invocation emits exactly one warning, performs no observer writes, and starts the command within 1000 ms of invocation. While one observed command runs, a second observer acquires the state lock. | Test |
```

### FND-002

spec/functional/FR-015-build-metrics-export.md:47, replace the text from "to `failed`, unless an explicit" through "from process status alone." with:

```text
to `failed`; observe mode records no other outcome value, because it has no source for a termination cause.
```

spec/functional/FR-015-build-metrics-export.md:91, in FR-015-AC-17, replace ", unless an explicit, independently known termination cause selects another matching closed outcome" with:

```text
; no other outcome value is incremented
```

### FND-003

spec/functional/FR-015-build-metrics-export.md:47, replace "A missing hint remains absent or explicitly unknown;" with:

```text
A missing hint stays absent from the record and the export, with no placeholder value;
```

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | Round 1, head 193bf7d: the 1000 ms bounds and lock release are at line 57 and AC-14 is replaced. |
| FND-002 | fixed | Round 1, head 193bf7d: no supplied termination cause remains in line 47 or AC-17. |
| FND-003 | fixed | Round 1, head 193bf7d: line 47 says a missing hint stays absent with no placeholder value. |
