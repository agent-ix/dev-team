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
SWM-221) SHALL emit evaluation results as four row kinds, defined here so the
evaluator, the minder, team-retro and the director read one shape. This
requirement defines the record; the evaluator's implementation belongs to
ix-board.

## Behavior

Every row carries `record_version`, `role`, `role_spec_version`, `skill_version`
(both recorded per session by the session start hook, ix-relay SWM-224 and
SWM-202), evaluation window, `evaluated_at` and `evaluator_version`.

- **Session rule row**: `session_id`, `rule_id`, `evaluation_id`, `verdict`
  (`pass`, `fail`, `n.a.`, `unavailable`), measured value, threshold (as
  comparator, value and unit), and evidence references (ledger row IDs, receipt
  IDs, event IDs, URLs or transcript offsets). The verdict is `n.a.` when the
  evaluation's trigger query found no occurrence in the window, `unavailable`
  when the trigger or evidence source could not be read, otherwise `pass` or
  `fail` from the threshold comparison. Neither `n.a.` nor `unavailable` counts
  as a pass. A judgement verdict also carries the rubric reference, the grading
  role and the cited evidence relied on.
- **Session objective row**: `session_id`, `metric_id`, value, target,
  direction, and whether the target was met, or `unavailable`.
- **Role rule row**: `rule_id`, sessions evaluated, counts of pass, fail,
  `n.a.` and `unavailable`, and pass rate over decided sessions. The row is
  produced for the whole window, for the previous window, and split by
  `skill_version` and by `role_spec_version`. Sessions with either version
  missing are reported in a separate group, never assigned one.
- **Role objective row**: `metric_id` value over the same window with the same
  splits by `skill_version` and `role_spec_version`, so rule pass rate and
  throughput are compared for the same set of sessions.

Rule flags. A rule failing in at least a configured fraction of decided
sessions is a skill defect candidate naming the rule ID and skill version. A
rule is a pruning candidate when it passes at 100% over N consecutive windows
(N configurable) and sessions that ran an earlier version without the rule show
no worse objective metrics for the rule's objective (value not worse by more
than a configured tolerance). If no earlier version without the rule has
enough decided sessions to compare, the rule is flagged `untestable` rather
than pruned, because a constant pass rate has no variance to associate with
an outcome.

Rows are append-only and replaying the same evidence, spec version and clock
yields identical rows. A `fail` on a `tick`-cadence deterministic evaluation is
also emitted as an alert input to the minder.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-008-AC-1 | A fixed ledger fixture yields exactly one session rule row per evaluation of the minder spec for a session, each with verdict, measured value, structured threshold and at least one evidence reference for every `pass` and `fail`. | Test |
| FR-008-AC-2 | A window where an evaluation's trigger query found no occurrence yields `n.a.` even when the violation count is zero; an unreadable trigger or evidence source yields `unavailable`; neither is counted in the pass rate numerator or denominator, and a window with the trigger fired and zero violations yields `pass`. | Test |
| FR-008-AC-3 | Role rule rows report pass rate per rule across sessions for the window and the previous window, split by `skill_version` and by `role_spec_version`; sessions missing either version are reported in a separate group. | Test |
| FR-008-AC-4 | Role objective rows carry each metric over the same window with the same splits by `skill_version` and `role_spec_version`; a metric with missing evidence is `unavailable`, not zero. | Test |
| FR-008-AC-5 | Evaluating the same inputs twice with a fixed clock produces identical rows, and the evaluator performs no write to any observed system. | Test |
| FR-008-AC-6 | A judgement verdict row without rubric reference, grading role or cited evidence is rejected by the record validator. | Test |
| FR-008-AC-7 | A rule failing in at least the configured fraction of decided sessions is marked a skill defect candidate carrying the rule ID, skill version and role spec version. | Test |
| FR-008-AC-8 | A failed `tick`-cadence deterministic evaluation is emitted as an alert input identifying the rule ID, session and evidence within the same tick. | Test |
| FR-008-AC-9 | A fixture session yields exactly one session objective row per metric of the role spec, each with value, target, direction and met, unmet or `unavailable`. | Test |
| FR-008-AC-10 | A rule passing at 100% for N windows whose earlier-version sessions without it show objective values no worse than the tolerance is marked a pruning candidate; the same rule with no comparable earlier-version sessions is marked `untestable`; with a worse earlier-version objective it is neither. N and the tolerance come from configuration. | Test |
| FR-008-AC-11 | A fixture with sessions across two skill versions and one role spec version produces distinct pass rates and objective values per skill version, so a skill change can be compared before and after without a role spec bump. | Test |

## Dependencies

- [FR-006](FR-006-role-spec-format.md), the rules and evaluations being recorded.
- [FR-001](FR-001-evidence-contract.md), honest unknowns and provenance.
- ix-board `retro eval` (SWM-221), the producer; ix-relay session start hook
  recording skill and role spec version (SWM-224, SWM-202).
