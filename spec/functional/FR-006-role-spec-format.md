---
id: FR-006
title: Define a role as a typed document of objectives, metrics, rules and evaluations
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-002
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-003
    type: depends_on
---
# FR-006: Define a role as a typed document of objectives, metrics, rules and evaluations

## Description

The role-spec format SHALL define each role (coder, reviewer, code lead, planner,
minder, orchestrator, director) as one Markdown document at
`spec/roles/<role>.md` with frontmatter `type: RoleSpec` that a Quire module
validates. The document lives under `spec/` because `quire matrix` reads
documents only from `<scope>/spec`; a document elsewhere would be invisible to
the lint ([FR-007](FR-007-role-spec-lint.md)). It is the single place that says
what the role is for, what it must and must not do, and how each statement is
checked. Role skills derive from it and cite its rule IDs.

## Behavior

Frontmatter carries `id` (the role's rule prefix, for example `MIND`), `role`,
`version` (a monotonically increasing integer) and relationships to the
requirements it serves. Four required tables follow, each with a stable ID
column; IDs are never reused.

- **Metrics** (`<P>-M<nn>`): name, evidence source, deterministic query
  reference, unit, target, direction (higher or lower is better). A metric
  measures a throughput outcome; its query SHALL NOT be the query of any
  evaluation, because correlating a rule's pass rate with its own violation
  count is circular.
- **Objectives** (`<P>-O<nn>`): the outcome the role owns (idle capacity
  minutes, time to action, tickets closed per hour) and the metric ID(s) that
  measure it. Objectives are throughput outcomes, not behaviors or compliance
  counts.
- **Rules** (`<P>-R<nn>`): one atomic statement of what the role must or must
  not do, the objective it serves, its failure class (a short slug) and the
  incident that produced it. A rule states behavior, never the measurement. A rule combining
  independent obligations is split so that a failure names the part that broke.
- **Evaluations** (`<P>-R<nn>-E<n>`): the rule it checks, evidence source,
  trigger, method, query or rubric reference, evaluator, threshold and cadence.
  - Evidence source is a closed enum declared in the `RoleSpec` archetype
    schema: `ledger`, `relay-receipts`, `hook-events`, `linear`, `github`,
    `transcript`, `ix-board-metric`.
  - Trigger is a deterministic query reference stating when the rule applies
    in the window (for example, a lane was idle with work queued). A window
    where the trigger did not fire yields `n.a.` rather than `pass`
    ([FR-008](FR-008-evaluation-result-record.md)).
  - Method is `deterministic` with a query reference, or `judgement` with a
    rubric reference of the form `<rubric>@<version>#<check-slug>`.
  - Evaluator is `evaluator` for deterministic evaluations; for judgement it is
    the role that grades (`director` or `team-retro`).
  - Threshold is structured: comparator (`<`, `<=`, `=`, `>=`, `>`), numeric
    value and unit.
  - Cadence is one of `tick`, `session-end`, `3h`, `daily`, `weekly`.

A judgement evaluation SHALL NOT carry cadence `tick`. A rule whose only
evaluations are judgement is flagged, not rejected.

Each session records the skill version and the role spec version it ran under
(session start hook, ix-relay SWM-224 and SWM-202). A skill that cites rules
records the role spec version it was derived from in its frontmatter
(`role_spec_version`), so a citation can be checked against that version.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-006-AC-1 | A complete role spec with all four tables validates under `quire validate`; removing the `Evaluations` table, any required column, or the `version` field fails validation with a diagnostic naming the missing element. | Test |
| FR-006-AC-2 | An evaluation with an evidence source outside the closed enum, a cadence outside `tick`, `session-end`, `3h`, `daily`, `weekly`, or a method other than `deterministic` or `judgement` fails validation. | Test |
| FR-006-AC-3 | A deterministic evaluation without a query reference, a judgement evaluation without a rubric reference of the form `<rubric>@<version>#<check-slug>`, and any evaluation without a trigger each fail validation. | Test |
| FR-006-AC-4 | A judgement evaluation with cadence `tick` fails validation; a rule whose evaluations are all judgement is reported as a warning, not an error. | Test |
| FR-006-AC-5 | Duplicate IDs within a role spec, an ID whose prefix differs from the frontmatter `id`, and a rule that names a nonexistent objective each fail validation. | Test |
| FR-006-AC-6 | The minder role spec declares at least one rule for each of these failure classes: unknown state read as not idle, failed probe read as healthy, ready work parked behind an idle lane, escalation muted or repeated-suppressed, and monitoring loop removed without owner instruction; removing the last rule of any class is detectable by the class column of the Rules table, and the spec validates once the `RoleSpec` archetype is installed. | Inspection |
| FR-006-AC-7 | A skill frontmatter `role_spec_version` and its cited rule IDs are checked against the role spec at that version; a cited ID absent from it is reported ([FR-007-AC-8](FR-007-role-spec-lint.md)). | Test |
| FR-006-AC-8 | A threshold with a missing comparator, a non-numeric value or a missing unit fails validation. | Test |
| FR-006-AC-9 | A judgement evaluation whose evaluator is neither `director` nor `team-retro`, and a deterministic evaluation whose evaluator is not `evaluator`, each fail validation. | Test |
| FR-006-AC-10 | A metric whose query reference equals the query of any evaluation fails validation, naming the metric and evaluation IDs. | Test |

## Dependencies

- A `RoleSpec` archetype in the owning Quire module repository: frontmatter
  schema, the four section tables with id columns, closed enums, and cross-row
  asserts. Tracked as SWM-245.
- ix-relay session start hook recording skill and role spec version (SWM-224,
  SWM-202).
- [US-002](../usecase/US-002-measured-role-rules.md), operator intent.
