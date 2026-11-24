---
id: SR-020
title: base review of SWM-220 role spec format and lint
type: SpecReview
analysis: base
review_set: subset
scope: "agent-ix/dev-team; SWM-220; spec/** and roles/minder.md at 627838c"
---

## Summary

Base checklist review of the role-spec format (FR-006), lint (FR-007), evaluation result record (FR-008), use case US-002 and the worked minder role spec, judged against owner intent (W4a): every rule measurable and traceable, per-session and per-role evaluation, objectives tied to throughput, and feedback that improves skills.

Ticket: SWM-220. Frozen PR: dev-team#30, 627838cfb2e62e93914b47e43cbd573dcc7a5a15.

## Verdict

**FAIL**. The structure is right and mostly lean: four tables, rule = requirement, evaluation = criterion, explicit n.a./unavailable, append-only replayable rows. But the result record cannot do the before/after skill-version comparison the feedback loop depends on, the per-session objective row is untested, and the worked example ties objectives to rule-compliance counts rather than throughput.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | Role rule rows split pass rate only by role_spec_version and previous window, never by skill_version, and objective metrics (AC-4) are not split by any version. A skill PR that fixes a failing rule usually does not bump the role spec, so the before/after comparison of rule pass rate and objective metrics per skill version (the W4a feedback loop and US-002 'which skill instruction to change') cannot be produced. Add per-skill_version (and per-role_spec_version) splits for both rule pass rate and objective metrics, with an AC. | spec/functional/FR-008-evaluation-result-record.md:55 |
| FND-002 | medium | The session objective row (session_id, metric_id, value, target, direction, met) has no acceptance criterion: AC-1 covers session rule rows and AC-4 covers role rows only. Per-session objective evaluation is explicit owner intent; add an AC that a fixture session yields one objective row per metric with met/unmet and unavailable handling. | spec/functional/FR-008-evaluation-result-record.md:36-37 |
| FND-003 | medium | AC-6 requires a rule per overnight failure class 'named in its source column', which is satisfied by whatever the source column names, so it cannot fail; and 'validates once the archetype is installed' is unverifiable now. Enumerate the failure classes (US-002 names three; the plan names nine) and require a rule for each listed class. | spec/functional/FR-006-role-spec-format.md:55 |
| FND-004 | medium | Minder objectives use MIND-M03 and MIND-M04, which are rule-compliance counts that mirror MIND-R01-E1 and MIND-R02-E1, contrary to FR-006 'Objectives are throughput outcomes, not behaviors'. Correlating a rule's pass rate with its own violation count is circular, so the 'which rules matter' analysis is defeated for these rules. Keep objectives on M01/M02-style outcomes, and add an FR-006 check (or AC) that a metric is not just an evaluation's query. | roles/minder.md:34-35 |
| FND-005 | medium | rubric-minder@1 check 'Scope coverage' does not resolve: skills/team-retro/references/rubric-minder.md carries no version, and its Scope coverage row grades omitted remote lanes, not failed probes recorded as defects (MIND-R02). Under FR-007-AC-5 the worked example itself would fail the lint; 'score 2' also has no stated scale. | roles/minder.md:53 |

## Examined Scope

```yaml
scope:
- id: US-002
  path: spec/usecase/US-002-measured-role-rules.md
  role: examined
  excerpt: '**As a** department owner running agent roles for days at a time **I want** every rule a role carries
    to come with a stated way of checking it, and the results rolled up per session and per role against the throughput
    the role exists to deliver **So that** I can see which rules are followed, which rules matter, and which skill
    instruction to change when a rule keeps failing.'
- id: FR-006
  path: spec/functional/FR-006-role-spec-format.md
  role: examined
  excerpt: 'The role-spec format SHALL define each role (coder, reviewer, code lead, planner, minder, orchestrator,
    director) as one Markdown document at `roles/<role>.md` with frontmatter `type: RoleSpec` that a Quire module
    validates. The document is the single place that says what the role is for, what it must and must not do, and
    how each statement is checked. Role skills derive from it and cite its rule IDs.'
- id: FR-006-AC-1
  path: spec/functional/FR-006-role-spec-format.md
  role: examined
  excerpt: A complete role spec with all four tables validates under `quire validate`; removing the `Evaluations`
    table, any required column, or the `version` field fails validation with a diagnostic naming the missing element.
- id: FR-006-AC-2
  path: spec/functional/FR-006-role-spec-format.md
  role: examined
  excerpt: An evaluation with an evidence source outside the declared vocabulary, a cadence outside `tick`, `session-end`,
    `3h`, `daily`, `weekly`, or a method other than `deterministic` or `judgement` fails validation.
- id: FR-006-AC-3
  path: spec/functional/FR-006-role-spec-format.md
  role: examined
  excerpt: A deterministic evaluation without a query reference, and a judgement evaluation without a rubric reference
    and rubric version, each fail validation.
- id: FR-006-AC-4
  path: spec/functional/FR-006-role-spec-format.md
  role: examined
  excerpt: A judgement evaluation with cadence `tick` fails validation; a rule whose evaluations are all judgement
    is reported as a warning, not an error.
- id: FR-006-AC-5
  path: spec/functional/FR-006-role-spec-format.md
  role: examined
  excerpt: Duplicate IDs within a role spec, an ID whose prefix differs from the frontmatter `id`, and a rule that
    names a nonexistent objective each fail validation.
- id: FR-006-AC-6
  path: spec/functional/FR-006-role-spec-format.md
  role: examined
  excerpt: 'The worked [minder role spec](../../roles/minder.md) is a complete instance: it declares at least one
    rule per overnight failure class named in its source column and validates once the `RoleSpec` archetype is installed.'
- id: FR-006-AC-7
  path: spec/functional/FR-006-role-spec-format.md
  role: examined
  excerpt: Each role skill that cites rules does so by rule ID; a cited ID absent from the role spec at the skill's
    recorded spec version is reported by the lint.
- id: FR-007
  path: spec/functional/FR-007-role-spec-lint.md
  role: examined
  excerpt: The role-spec lint SHALL fail on any rule with no paired evaluation and any objective with no metric.
    It SHALL be computed by Quire and Quoin traceability, treating each rule as a requirement and each evaluation
    as its criterion, rather than by a purpose-built checker.
- id: FR-007-AC-1
  path: spec/functional/FR-007-role-spec-lint.md
  role: examined
  excerpt: A role spec containing a rule with no evaluation row exits nonzero, naming the rule ID.
- id: FR-007-AC-2
  path: spec/functional/FR-007-role-spec-lint.md
  role: examined
  excerpt: A role spec containing an objective with an empty metric list, or a metric ID that is not defined, exits
    nonzero, naming the objective ID.
- id: FR-007-AC-3
  path: spec/functional/FR-007-role-spec-lint.md
  role: examined
  excerpt: A role spec in which every rule has at least one evaluation and every objective at least one defined
    metric exits zero.
- id: FR-007-AC-4
  path: spec/functional/FR-007-role-spec-lint.md
  role: examined
  excerpt: An evaluation naming a rule that does not exist, and a metric used by no objective, are each reported;
    the first fails the lint, the second is a warning.
- id: FR-007-AC-5
  path: spec/functional/FR-007-role-spec-lint.md
  role: examined
  excerpt: A deterministic evaluation whose ID is tagged on no registered query, and a judgement evaluation whose
    rubric reference does not resolve, are reported as unbound evaluations and fail the lint when run with the evaluator
    available.
- id: FR-007-AC-6
  path: spec/functional/FR-007-role-spec-lint.md
  role: examined
  excerpt: The lint output is derived from `quire matrix` rows for the role spec's rules; no separate parser of
    the role spec tables exists in this repository.
- id: FR-007-AC-7
  path: spec/functional/FR-007-role-spec-lint.md
  role: examined
  excerpt: Deleting a rule row together with its evaluations makes the lint pass and records the deletion in the
    role spec's version bump; there is no mechanism to mark a rule as exempt from evaluation.
- id: FR-008
  path: spec/functional/FR-008-evaluation-result-record.md
  role: examined
  excerpt: The evaluator (`ix-board retro eval --role <r> [--session <id>] [--since <t>]`, SWM-221) SHALL emit evaluation
    results as three row kinds, defined here so the evaluator, the minder, team-retro and the director read one
    shape. This requirement defines the record; the evaluator's implementation belongs to ix-board.
- id: FR-008-AC-1
  path: spec/functional/FR-008-evaluation-result-record.md
  role: examined
  excerpt: A fixed ledger fixture yields exactly one session rule row per rule and evaluation of the minder spec
    for a session, each with verdict, measured value, threshold and at least one evidence reference for every `pass`
    and `fail`.
- id: FR-008-AC-2
  path: spec/functional/FR-008-evaluation-result-record.md
  role: examined
  excerpt: A rule whose trigger did not occur yields `n.a.`, and a rule whose evidence source is unreadable yields
    `unavailable`; neither is counted in the pass rate numerator or denominator.
- id: FR-008-AC-3
  path: spec/functional/FR-008-evaluation-result-record.md
  role: examined
  excerpt: Role rule rows report pass rate per rule across sessions, the previous-window rate, and the rate split
    by `role_spec_version`; sessions recorded without a role spec version are reported separately, not assigned
    one.
- id: FR-008-AC-4
  path: spec/functional/FR-008-evaluation-result-record.md
  role: examined
  excerpt: Role rows carry the objective metric values for the same window; a metric with missing evidence is `unavailable`,
    not zero.
- id: FR-008-AC-5
  path: spec/functional/FR-008-evaluation-result-record.md
  role: examined
  excerpt: Evaluating the same inputs twice with a fixed clock produces identical rows, and the evaluator performs
    no write to any observed system.
- id: FR-008-AC-6
  path: spec/functional/FR-008-evaluation-result-record.md
  role: examined
  excerpt: A judgement verdict row without rubric version or cited evidence is rejected by the record validator.
- id: FR-008-AC-7
  path: spec/functional/FR-008-evaluation-result-record.md
  role: examined
  excerpt: A rule failing in at least the configured fraction of evaluated sessions is marked as a skill defect
    candidate carrying the rule ID and role spec version; a rule passed in every session whose pass rate shows no
    association with any objective metric over the configured number of windows is marked as a pruning candidate.
- id: FR-008-AC-8
  path: spec/functional/FR-008-evaluation-result-record.md
  role: examined
  excerpt: A failed `tick`-cadence deterministic evaluation is emitted as an alert input identifying the rule ID,
    session and evidence within the same tick.
- id: MIND-M01
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-M01 | Idle lane-minutes with ready work | ledger | ledger.idle_minutes_with_ready_work | minutes/day
    | 30 | lower |'
- id: MIND-M02
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-M02 | Time from idle detection to action | ledger | ledger.detection_to_action_p90 | minutes
    | 10 | lower |'
- id: MIND-M03
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-M03 | Lanes with unknown state treated as not idle | ledger | ledger.unknown_as_not_idle_count
    | count | 0 | lower |'
- id: MIND-M04
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-M04 | Ticks with a failed probe source and no defect row | ledger | ledger.probe_failures_without_defect
    | count | 0 | lower |'
- id: MIND-O01
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-O01 | No configured lane stays idle while assigned work waits | MIND-M01, MIND-M03 |'
- id: MIND-O02
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-O02 | Every detected problem reaches an owner who can act quickly | MIND-M02, MIND-M04 |'
- id: MIND-R01
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-R01 | A lane whose state is UNKNOWN counts as idle and is acted on in the same tick; the minder
    does not treat missing evidence as no work needed. | MIND-O01 | Unknown read as not idle, 2026-11-23 |'
- id: MIND-R02
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-R02 | A failed or timed-out probe of a host or source is recorded as a defect in the tick and
    routed to an owner; the minder never reads a failed probe as healthy or unreachable-and-fine. | MIND-O02 | Terra
    probe read unreachable 129 times |'
- id: MIND-R03
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-R03 | An idle lane with a queued ticket is sent the next assigned ticket by exact ID in the tick
    it is found. | MIND-O01 | Ready perf batch parked all night |'
- id: MIND-R04
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-R04 | An unresolved problem escalates on the ladder: worker at 5 minutes, lead at 10, orchestrator
    at 15, owner at 30; the minder repeats an escalation at each rung rather than suppressing it. | MIND-O02 | "Never
    repeat" muted escalation |'
- id: MIND-R05
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-R05 | The minder loop is removed only on the owner''s explicit instruction. | MIND-O02 | Only
    minder cron deleted on an ambiguous message |'
- id: MIND-R01-E1
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-R01-E1 | MIND-R01 | ledger | deterministic | ledger.unknown_lane_not_acted_ticks | 0 ticks |
    tick |'
- id: MIND-R02-E1
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-R02-E1 | MIND-R02 | ledger | deterministic | ledger.probe_failure_without_defect_row | 0 ticks
    | tick |'
- id: MIND-R02-E2
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-R02-E2 | MIND-R02 | transcript | judgement | rubric-minder@1 check "Scope coverage" | score 2
    | daily |'
- id: MIND-R03-E1
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-R03-E1 | MIND-R03 | relay receipts | deterministic | relay.idle_with_queue_unassigned_minutes
    | 0 minutes beyond one tick | tick |'
- id: MIND-R04-E1
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-R04-E1 | MIND-R04 | ledger | deterministic | ledger.escalation_ladder_latency_by_rung | each
    rung within 2 minutes of its time | tick |'
- id: MIND-R05-E1
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-R05-E1 | MIND-R05 | hook events | deterministic | hooks.minder_loop_removed_without_owner_instruction
    | 0 events | session-end |'
```

## Method and Limits

Diff scope: git diff origin/main...HEAD (US-002, FR-006, FR-007, FR-008, spec/spec.md index, roles/minder.md). No applicable AssuranceProfile exists in the repository; direct review applies. Spec files validate (quire validate exit 0 each); roles/minder.md fails with unknown type 'RoleSpec', as the PR declares (archetype is an external dependency). quire matrix shows all 22 new criteria untagged/requirement-without-design, expected at the spec-only stage. No hash/digest/pin antipattern found. Owner intent was read from the program plan section W4a. Criterion-strength (Jev), evidence, risk-complexity and scope-boundary lenses were not run for this bounded review set.
