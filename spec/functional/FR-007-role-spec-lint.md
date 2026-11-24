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
its rule. Role specs live under `spec/roles/`, which `quire matrix` reads.
`quire matrix` and `quoin gap-analysis` then report, per role spec, rules with
no criterion (unmeasured), criteria with no binder (unbound evaluation), and
metrics no objective uses. Unmeasured rules are errors, not coverage statistics:
the lint exits nonzero. A rule that cannot be measured is rewritten until it can
or deleted; there is no waiver field.

Binding. A deterministic evaluation is bound when the evaluator
(`ix-board retro eval`) carries its ID as a trace tag on the registered query.
Those tags are in the ix-board repository, so the lint reads them through
`quire matrix --repo` naming that repository. A judgement evaluation is bound
when its rubric reference resolves to the named rubric file, version and check
slug. When the evaluator repository is not supplied or unavailable, every
deterministic evaluation is reported `unbound`, which fails the lint; an
unavailable evaluator never yields a pass.

Version bumps. The lint compares the role spec with its base revision (the
merge base with the default branch). A change to any rule, metric, objective or
evaluation row requires a higher frontmatter `version`; a changed table with an
unchanged or lower version fails. Deleting a rule with its evaluations is legal
and requires the same bump.

Skill citations. The lint scans skills that carry `role_spec_version`
frontmatter and reports any cited rule ID absent from the role spec at that
version.

The capabilities this assumes of Quire (rule-parented criteria through a column,
objective-to-metric resolution, unused-metric orphan check, cross-row asserts
and versioned rubric references) are delivered by SWM-245.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-007-AC-1 | A role spec containing a rule with no evaluation row exits nonzero, naming the rule ID. | Test |
| FR-007-AC-2 | A role spec containing an objective with an empty metric list, or a metric ID that is not defined, exits nonzero, naming the objective ID. | Test |
| FR-007-AC-3 | A role spec in which every rule has at least one evaluation and every objective at least one defined metric, with evaluator bindings supplied, exits zero. | Test |
| FR-007-AC-4 | An evaluation naming a rule that does not exist, and a metric used by no objective, are each reported; the first fails the lint, the second is a warning. | Test |
| FR-007-AC-5 | A deterministic evaluation whose ID is tagged on no registered query, and a judgement evaluation whose rubric reference does not resolve, are reported as `unbound` and fail the lint. | Test |
| FR-007-AC-6 | The lint output is derived from `quire matrix` rows for the role spec's rules; no separate parser of the role spec tables exists in this repository. | Inspection |
| FR-007-AC-7 | Deleting a rule row together with its evaluations makes the lint pass when the version is bumped; no field marks a rule as exempt from evaluation. | Test |
| FR-007-AC-8 | A skill whose frontmatter cites a rule ID absent from the role spec at its `role_spec_version` is reported and fails the lint. | Test |
| FR-007-AC-9 | A role spec file under `spec/roles/` appears in `quire matrix` output; the same file under any directory outside `spec/` produces no rows and the lint reports it as unscanned. | Test |
| FR-007-AC-10 | Running the lint with the evaluator repository absent or unreadable reports every deterministic evaluation `unbound` and exits nonzero; supplying it via `quire matrix --repo` binds tagged queries. | Test |
| FR-007-AC-11 | A change to any rule, metric, objective or evaluation row against the base revision with an unchanged or lower `version` fails, naming the changed table; the same change with a higher version passes. | Test |

## Dependencies

- SWM-245: the `RoleSpec` Quire archetype with trace targets, cross-row asserts,
  metric and objective resolution, and versioned rubric references.
- `quire matrix --repo` for cross-repository trace tags in ix-board.
- [FR-006](FR-006-role-spec-format.md), the format being linted.
