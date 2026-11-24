---
id: SR-022
title: failure-domain review of SWM-220 role spec format and lint
type: SpecReview
analysis: failure-domain
review_set: subset
scope: "agent-ix/dev-team; SWM-220; spec/** and roles/minder.md at 627838c"
---

## Summary

Failure-domain review of the evaluation record and format: how verdicts are decided at edges (trigger absent, evidence missing, evaluator unavailable), how versions partition results, and whether thresholds are machine-comparable.

Ticket: SWM-220. Frozen PR: dev-team#30, 627838cfb2e62e93914b47e43cbd573dcc7a5a15.

## Verdict

**CONDITIONAL**. Unknown-is-not-pass, replay determinism and read-only evaluation are well covered. Four edges let two implementers produce different verdicts or silently mix versions; resolve before implementation.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | n.a. means 'the rule's trigger did not occur', but FR-006 gives evaluations no trigger or applicability field, and the example queries are violation counts ('0 ticks') where no trigger and full compliance both read 0. Implementers will differ on n.a. versus pass; vacuous passes inflate pass rates and feed the pruning rule. Add an applicability query or column to evaluations and an AC that separates the two. | spec/functional/FR-008-evaluation-result-record.md:54 |
| FND-002 | medium | Nothing enforces FR-006's version bump on any rule, metric or evaluation change: no AC checks it, and AC-7's 'records the deletion in the role spec's version bump' cannot be tested by a lint over one file. An unbumped edit puts different rule sets under one role_spec_version, corrupting FR-008's per-version comparison. Add a check against the base revision (changed tables imply higher version) with a Test AC. | spec/functional/FR-007-role-spec-lint.md:45 |
| FND-003 | medium | The pruning criterion takes a rule 'passed in every session' and asks whether its pass rate 'shows no association' with objective metrics, but a constant pass rate has no variance, so association is undefined and the clause reduces to 'always passed for N windows'. The statistic, threshold and window count are unspecified. Define the pruning test concretely (for example always-passed for N windows and no objective change across the versions that introduced it). | spec/functional/FR-008-evaluation-result-record.md:59 |
| FND-004 | medium | Threshold is free text with no comparator, unit or type; the example uses '0 minutes beyond one tick' and 'each rung within 2 minutes of its time', which an evaluator cannot compare to FR-008's measured value deterministically. Give thresholds a typed form (comparator, value, unit) and add an AC rejecting an unparseable threshold. | spec/functional/FR-006-role-spec-format.md:35-40 |
| FND-005 | low | AC-5 fails unbound evaluations only 'when run with the evaluator available' and does not say what happens otherwise (pass, warn, or unavailable). State the result without the evaluator so a lint run without ix-board does not silently go green. | spec/functional/FR-007-role-spec-lint.md:43 |

## Examined Scope

```yaml
scope:
- id: FR-006
  path: spec/functional/FR-006-role-spec-format.md
  role: examined
  excerpt: 'The role-spec format SHALL define each role (coder, reviewer, code lead, planner, minder, orchestrator,
    director) as one Markdown document at `roles/<role>.md` with frontmatter `type: RoleSpec` that a Quire module
    validates. The document is the single place that says what the role is for, what it must and must not do, and
    how each statement is checked. Role skills derive from it and cite its rule IDs.'
- id: FR-007-AC-5
  path: spec/functional/FR-007-role-spec-lint.md
  role: examined
  excerpt: A deterministic evaluation whose ID is tagged on no registered query, and a judgement evaluation whose
    rubric reference does not resolve, are reported as unbound evaluations and fail the lint when run with the evaluator
    available.
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
