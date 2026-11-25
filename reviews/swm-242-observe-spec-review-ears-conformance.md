---
id: SR-065
title: "EARS conformance analysis of the SWM-242 observe contract wording"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md (PR #43 diff, head 890d7a78a4a68ac64fc5e89a8bd257f4112e7b67), checked against agent-ix/dev-tools locked-build at bce5f4a7a20000a56275e3bc49b290fc1053732d"
review_set: subset
---

## Summary

Ticket: SWM-242. quire validate exits 0; the grammar warnings on line 55 remain and those on line 57 and AC-15 present on main are gone because their shall statements were removed. Two removals leave behaviour without an obligation.

## Verdict

**CONDITIONAL**: one medium and one low finding.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | The obligation that host adoption confirm group or cgroup delivery of SIGKILL and stop signals is replaced by the description Host wrappers route these signals, which requires nothing; a PID-only SIGKILL leaves the build running after the caller sees it end. | spec/functional/FR-015-build-metrics-export.md:55, spec/functional/FR-015-build-metrics-export.md:95 |
| FND-002 | low | Start order and both time bounds are plain present tense with no shall, and the one shared interval does not say what shares it. | spec/functional/FR-015-build-metrics-export.md:57 |

## Replacement Text

### FND-001

spec/functional/FR-015-build-metrics-export.md:55, replace the sentence beginning "Host wrappers route these signals" with:

```text
Host wrappers SHALL send these signals to the command's process group or cgroup, and host adoption SHALL confirm it.
```

spec/functional/FR-015-build-metrics-export.md:95, replace the matching AC-15 sentence with:

```text
Host adoption confirms that the wrapper sends them to the process group or cgroup.
```

### FND-002

spec/functional/FR-015-build-metrics-export.md:57, replace the first sentence with:

```text
The observer SHALL start the already-admitted command before reading host configuration or touching observer state.
```

spec/functional/FR-015-build-metrics-export.md:57, replace the two sentences beginning "Preflight state and configuration work" and "Completion work" with:

```text
The observer SHALL stop waiting for preflight state and configuration work 1000 ms after the preflight worker starts; that work can overlap command execution. When the command exits, waiting for an unfinished preflight and doing completion work SHALL share one 1000 ms interval, after which the observer abandons both.
```


## Dispositions

Applied by the dev-team #43 follow-up at head `002c2f1b0519adda61fac278a03c79e78e3ede54`.

| FND | outcome | reason |
| --- | ------- | ------ |
| FND-001 | fixed | The normative contract requires wrappers to target the process group or cgroup and requires host adoption to confirm that behavior. |
| FND-002 | fixed | Start order, timeout, and shared post-exit bound now use explicit SHALL obligations and name both waits in the shared interval. |
