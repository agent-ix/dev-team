---
id: FR-008
title: Record per-session and per-role evaluation results with evidence
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-002
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-006
    type: depends_on
  - target: ix://agent-ix/dev-team/FR-001
    type: depends_on
---
# FR-008: Record per-session and per-role evaluation results with evidence

## Description

The evaluator (`ix-board retro eval --role <r> [--session <id>] [--since <t>]`,
SWM-221) SHALL emit evaluation results as three row kinds, defined here so the
evaluator, the minder, team-retro and the director read one shape. This
requirement defines the record; the evaluator's implementation belongs to
ix-board.

## Behavior

Every row carries `record_version`, `role`, `role_spec_version`, `skill_version`
(from the session record), evaluation window, `evaluated_at` and
`evaluator_version`.

- **Session rule row**: `session_id`, `rule_id`, `evaluation_id`, `verdict`
  (`pass`, `fail`, `n.a.`, `unavailable`), measured value, threshold, and
  evidence references (ledger row IDs, receipt IDs, event IDs, URLs or
  transcript offsets). `n.a.` means the rule's trigger did not occur in the
  window; `unavailable` means the evidence source could not be read. Neither
  counts as a pass. A judgement verdict also carries the rubric version and
  the cited evidence the judge relied on.
- **Session objective row**: `session_id`, `metric_id`, value, target,
  direction, and whether the target was met.
- **Role rule row**: `rule_id`, sessions evaluated, counts of pass, fail,
  `n.a.` and `unavailable`, pass rate over decided sessions, the same figure
  for the previous window and for the previous `role_spec_version`, and the
  objective metric values over the same window so a rule's pass rate can be
  compared with outcomes. A rule failing in a configured fraction of sessions
  is marked as a skill defect candidate naming the rule ID.

Rows are append-only and replaying the same evidence, spec version and clock
yields identical rows. A verdict of `fail` on a rule whose evaluation cadence
is `tick` is also emitted as an alert input to the minder.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-008-AC-1 | A fixed ledger fixture yields exactly one session rule row per rule and evaluation of the minder spec for a session, each with verdict, measured value, threshold and at least one evidence reference for every `pass` and `fail`. | Test |
| FR-008-AC-2 | A rule whose trigger did not occur yields `n.a.`, and a rule whose evidence source is unreadable yields `unavailable`; neither is counted in the pass rate numerator or denominator. | Test |
| FR-008-AC-3 | Role rule rows report pass rate per rule across sessions, the previous-window rate, and the rate split by `role_spec_version`; sessions recorded without a role spec version are reported separately, not assigned one. | Test |
| FR-008-AC-4 | Role rows carry the objective metric values for the same window; a metric with missing evidence is `unavailable`, not zero. | Test |
| FR-008-AC-5 | Evaluating the same inputs twice with a fixed clock produces identical rows, and the evaluator performs no write to any observed system. | Test |
| FR-008-AC-6 | A judgement verdict row without rubric version or cited evidence is rejected by the record validator. | Test |
| FR-008-AC-7 | A rule failing in at least the configured fraction of evaluated sessions is marked as a skill defect candidate carrying the rule ID and role spec version; a rule passed in every session whose pass rate shows no association with any objective metric over the configured number of windows is marked as a pruning candidate. | Test |
| FR-008-AC-8 | A failed `tick`-cadence deterministic evaluation is emitted as an alert input identifying the rule ID, session and evidence within the same tick. | Test |

## Dependencies

- [FR-006](FR-006-role-spec-format.md), the rules and evaluations being recorded.
- [FR-001](FR-001-evidence-contract.md), honest unknowns and provenance.
- ix-board `retro eval` (SWM-221), the producer; session start hook recording
  skill and role spec version, delivered by ix-relay.
