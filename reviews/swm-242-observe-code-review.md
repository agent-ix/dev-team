---
id: SR-052
title: "Code review of SWM-242 observe-mode spec change"
type: SpecReview
analysis: code-review
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md (PR #41 diff, head 078c982b9bf6ffdabd4c9d373d64819bb7f79212); related FR-005, FR-009, FR-010, FR-011, FR-016, NFR-002"
review_set: subset
---

## Summary

Ticket: SWM-242. Reviewed the FR-015 diff for consistency with the retained FR-015 text and with locked-build on dev-tools origin/main; one inconsistency remains in the current-build producer lists.

## Verdict

**CONDITIONAL**: one medium finding. No duplication or vendoring in the diff. Language lanes do not apply to a Markdown-only change.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | The retained current-build lists say ix_build_test_runs_total is absent and queue depth and admission-blocked series are emitted, with no store-mode scope, while the new observe text produces test runs and omits the other two. | spec/functional/FR-015-build-metrics-export.md:43 |

## Replacement Text

### FND-001

spec/functional/FR-015-build-metrics-export.md:43, append at the end of the paragraph:

```text
 The current-build lists above describe admitted stores; for an observed store the **Observe mode** rules below define which series exist, and `observe` is the producer of `ix_build_test_runs_total`.
```

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | Round 1, head 193bf7d: the sentence scoping the current-build lists to admitted stores is appended at FR-015 line 43. The observed-store rules it points to are tracked as SR-053 FND-001. |
