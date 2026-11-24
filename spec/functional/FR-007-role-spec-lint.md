---
id: FR-007
title: Reject role rules without evaluations and objectives without metrics
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-002
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-006
    type: depends_on
---
# FR-007: Reject role rules without evaluations and objectives without metrics

## Description

The role-spec lint SHALL fail on any rule with no paired evaluation and any
objective with no metric. It SHALL be computed by Quire and Quoin traceability,
treating each rule as a requirement and each evaluation as its criterion, rather
than by a purpose-built checker.

## Behavior

The `RoleSpec` archetype declares trace targets so that rule IDs and evaluation
IDs are minted from their tables and each evaluation's `Rule` column binds it to
its rule. `quire matrix` and `quoin gap-analysis` then report, per role spec,
rules with no criterion (unmeasured), criteria with no binder (an evaluation
whose query or rubric the evaluator does not implement), and metrics no
objective uses. Unmeasured rules are errors, not coverage statistics: the lint
exits nonzero. A rule that cannot be measured is either rewritten until it can
or deleted; there is no waiver field.

A deterministic evaluation is bound when the evaluator (`ix-board retro eval`)
carries its ID as a trace tag on the registered query. A judgement evaluation is
bound when its rubric reference resolves to a file at the named version.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-007-AC-1 | A role spec containing a rule with no evaluation row exits nonzero, naming the rule ID. | Test |
| FR-007-AC-2 | A role spec containing an objective with an empty metric list, or a metric ID that is not defined, exits nonzero, naming the objective ID. | Test |
| FR-007-AC-3 | A role spec in which every rule has at least one evaluation and every objective at least one defined metric exits zero. | Test |
| FR-007-AC-4 | An evaluation naming a rule that does not exist, and a metric used by no objective, are each reported; the first fails the lint, the second is a warning. | Test |
| FR-007-AC-5 | A deterministic evaluation whose ID is tagged on no registered query, and a judgement evaluation whose rubric reference does not resolve, are reported as unbound evaluations and fail the lint when run with the evaluator available. | Test |
| FR-007-AC-6 | The lint output is derived from `quire matrix` rows for the role spec's rules; no separate parser of the role spec tables exists in this repository. | Inspection |
| FR-007-AC-7 | Deleting a rule row together with its evaluations makes the lint pass and records the deletion in the role spec's version bump; there is no mechanism to mark a rule as exempt from evaluation. | Test |

## Dependencies

- Quire trace-target declarations for `RoleSpec` (the same mechanism that mints
  `FR-nnn-AC-n` from an `Acceptance Criteria` table), in the owning module.
- [FR-006](FR-006-role-spec-format.md), the format being linted.
