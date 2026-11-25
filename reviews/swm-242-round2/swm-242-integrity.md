---
id: SR-045
title: "Integrity analysis — SWM-242 FR-015"
type: SpecReview
analysis: integrity
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md; related FR-005, FR-009, FR-010, FR-011; ix-board FR-041"
review_set: subset
---

## Summary

Checked FR-015 completeness, consistency, atomicity, testability, and verification coverage. AC-11 and AC-12 make the newly specified interval and capacity behavior observable, while the configured-capacity source remains inconsistent with FR-009.

## Verdict

**FAIL** — FR-015 and FR-009 prescribe conflicting sources for configured capacity, so FR-015 cannot be implemented against one unambiguous policy source.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | The new configured-capacity metric and its criterion name host policy `capacity_units`, while FR-009 excludes the earlier JSON host policy and defines the TOML profile as the only source of host limits without defining `capacity_units` there. This unresolved source conflict prevents a single consistent implementation and verification oracle. | FR-015 Behavior; FR-015-AC-2; FR-015-AC-12; FR-009 Behavior |

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | still-open | The new wording distinguishes the metric's `capacity_units` from FR-009 `[host].max_slots`, but FR-009 still says TOML is the only source of host limits, states its computed sustainable slot count is the enabled capacity used by FR-005, and explicitly rejects the earlier JSON host policy. FR-015 does not establish whether the effective admission configuration is a distinct authoritative source or how it relates to FR-009's enabled capacity, so the normative conflict remains. |
| FND-001 | fixed | Round 2, head d1023710e636c65dcabf7f7235edc8d1215bd05b: FR-009 now makes TOML the target source and permits the transitional capacity_units read until SWM-239, so the source is defined. Residual wording defects are recorded in SR-051. |
