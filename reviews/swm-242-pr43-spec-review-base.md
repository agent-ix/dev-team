---
id: SR-064
title: "Base spec review of the SWM-242 observe contract wording"
type: SpecReview
analysis: base
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md (PR #43 diff, head 890d7a78a4a68ac64fc5e89a8bd257f4112e7b67), checked against agent-ix/dev-tools locked-build at bce5f4a7a20000a56275e3bc49b290fc1053732d"
review_set: subset
---

## Summary

Ticket: SWM-242. Checked the four changed lines against FR-015-AC-13 to AC-22. Criterion ids are unchanged and unique; no hash, digest or pin was added. AC-14 lost its measurable start condition.

## Verdict

**CONDITIONAL**: one low finding.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | low | AC-14 says the command start is not delayed, with nothing to compare against, and its last sentence holds for any lock, since a second observer acquires it after release, so neither can fail. | spec/functional/FR-015-build-metrics-export.md:94 |

## Replacement Text

### FND-001

spec/functional/FR-015-build-metrics-export.md:94, replace the FR-015-AC-14 row with:

```text
| FR-015-AC-14 | For each observer failure case (missing or unwritable state directory, corrupt state, invalid configuration, state lock held indefinitely, a configuration path that never returns data, and observed/admitted store-mode mismatch), the invocation emits exactly one warning, performs no observer writes, and starts the command without waiting for a configuration read, the state lock or a state write. A preflight still unfinished 1000 ms after its worker starts is abandoned with one warning while the command keeps running. While one observed command runs, a second observed command records its own occupancy, so both are reported busy. | Test |
```

## Dispositions

Round 1, head 2b91f17ad9c7ab4bb52b5f55d38dda2f26584cb2. The FR-015 text equals the proposed edit.

| FND | outcome | reason |
| --- | ------- | ------ |
| FND-001 | fixed | AC-14 is measurable. |
