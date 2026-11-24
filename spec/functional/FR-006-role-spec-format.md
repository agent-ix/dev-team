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
minder, orchestrator, director) as one Markdown document at `roles/<role>.md` with frontmatter
`type: RoleSpec` that a Quire module validates. The document is the single place
that says what the role is for, what it must and must not do, and how each
statement is checked. Role skills derive from it and cite its rule IDs.

## Behavior

Frontmatter carries `id` (the role's rule prefix, for example `MIND`), `role`,
`version` (a monotonically increasing integer bumped on any change to a rule,
metric or evaluation) and relationships to the requirements it serves. Four
required tables follow, each with a stable ID column; IDs are never reused.

- **Metrics** (`<P>-M<nn>`): name, evidence source, deterministic query or
  reference, unit, target, direction (higher or lower is better).
- **Objectives** (`<P>-O<nn>`): the outcome the role owns (idle capacity
  minutes, time to action, tickets closed per hour), and the metric ID(s) that
  measure it. Objectives are throughput outcomes, not behaviors.
- **Rules** (`<P>-R<nn>`): one atomic statement of what the role must or must
  not do, the objective it serves, and the incident or failure class that
  produced it. A rule states behavior, never the measurement.
- **Evaluations** (`<P>-R<nn>-E<n>`): the rule it checks, evidence source
  (ledger, relay receipts, hook events, Linear, GitHub, transcript, ix-board
  metric), method, threshold and cadence. Method is `deterministic` with a query
  reference, or `judgement` with a rubric reference at a fixed rubric version.
  Cadence is one of `tick`, `session-end`, `3h`, `daily`, `weekly`.

A judgement evaluation names its evaluator role (the director) and may not
carry a `tick` cadence. A rule whose only evaluations are judgement is
flagged, not rejected.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-006-AC-1 | A complete role spec with all four tables validates under `quire validate`; removing the `Evaluations` table, any required column, or the `version` field fails validation with a diagnostic naming the missing element. | Test |
| FR-006-AC-2 | An evaluation with an evidence source outside the declared vocabulary, a cadence outside `tick`, `session-end`, `3h`, `daily`, `weekly`, or a method other than `deterministic` or `judgement` fails validation. | Test |
| FR-006-AC-3 | A deterministic evaluation without a query reference, and a judgement evaluation without a rubric reference and rubric version, each fail validation. | Test |
| FR-006-AC-4 | A judgement evaluation with cadence `tick` fails validation; a rule whose evaluations are all judgement is reported as a warning, not an error. | Test |
| FR-006-AC-5 | Duplicate IDs within a role spec, an ID whose prefix differs from the frontmatter `id`, and a rule that names a nonexistent objective each fail validation. | Test |
| FR-006-AC-6 | The worked [minder role spec](../../roles/minder.md) is a complete instance: it declares at least one rule per overnight failure class named in its source column and validates once the `RoleSpec` archetype is installed. | Inspection |
| FR-006-AC-7 | Each role skill that cites rules does so by rule ID; a cited ID absent from the role spec at the skill's recorded spec version is reported by the lint. | Inspection |

## Dependencies

- A `RoleSpec` archetype in the owning Quire module repository (frontmatter
  schema, section tables, id columns), delivered outside this repository.
- [US-002](../usecase/US-002-measured-role-rules.md), operator intent.
