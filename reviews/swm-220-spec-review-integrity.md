---
id: SR-021
title: integrity review of SWM-220 role spec format and lint
type: SpecReview
analysis: integrity
review_set: subset
scope: "agent-ix/dev-team; SWM-220; spec/** and roles/minder.md at 627838c"
---

## Summary

Integrity review of completeness and internal consistency across FR-006, FR-007 and the minder example: where role specs live versus where the lint reads, what the lint is responsible for, and whether the format's own rules are representable in its tables.

Ticket: SWM-220. Frozen PR: dev-team#30, 627838cfb2e62e93914b47e43cbd573dcc7a5a15.

## Verdict

**FAIL**. IDs, relationships and index entries are consistent and the spec files validate. The lint mechanism and the document location contradict each other, and several FR-006 behaviors have no column or check to carry them.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | FR-006 places role specs at roles/<role>.md, but FR-007 computes the lint from quire matrix, which reads documents only from <scope>/spec (quire matrix --help; quoin spec-review). As written the lint sees no role specs and exits zero. Either move role specs under spec/ (for example spec/roles/) or state how the matrix is pointed at roles/, with an AC. | spec/functional/FR-007-role-spec-lint.md:15-17 |
| FND-002 | medium | AC-7 says a skill citing a rule ID absent 'at the skill's recorded spec version' is reported by the lint, but FR-007 defines no scan of skills and nothing defines where a skill records its role spec version. It is also marked Inspection while describing an automated report. Define skill-citation checking in FR-007 (with a Test AC) and where skills record the version, or drop the lint clause. | spec/functional/FR-006-role-spec-format.md:56 |
| FND-003 | medium | 'A judgement evaluation names its evaluator role (the director)' has no column in the Evaluations table, no AC, and the minder example's judgement row names none. The plan also has team-retro running per-session evaluations every 3h, so hard-wiring the director is inconsistent. Add an Evaluator column (or drop the clause) and test it. | spec/functional/FR-006-role-spec-format.md:42-44 |
| FND-004 | low | AC-2 tests against 'the declared vocabulary' of evidence sources, but FR-006 only lists sources in a parenthetical ('ledger, relay receipts, ... ix-board metric'). State that the list is the closed enum, and where it is declared (archetype schema). | spec/functional/FR-006-role-spec-format.md:51 |
| FND-005 | low | MIND-R04 packs four rung deadlines plus a repeat-not-suppress obligation into one rule, against FR-006 'one atomic statement'. A fail does not say which part broke; split it (for example ladder timing versus no suppression). | roles/minder.md:44 |

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
- id: MIND-R02-E2
  path: roles/minder.md
  role: examined
  excerpt: '| MIND-R02-E2 | MIND-R02 | transcript | judgement | rubric-minder@1 check "Scope coverage" | score 2
    | daily |'
- id: FR-008
  path: spec/functional/FR-008-evaluation-result-record.md
  role: context_only
  excerpt: The evaluator (`ix-board retro eval --role <r> [--session <id>] [--since <t>]`, SWM-221) SHALL emit evaluation
    results as three row kinds, defined here so the evaluator, the minder, team-retro and the director read one
    shape. This requirement defines the record; the evaluator's implementation belongs to ix-board.
```

## Method and Limits

Diff scope: git diff origin/main...HEAD (US-002, FR-006, FR-007, FR-008, spec/spec.md index, roles/minder.md). No applicable AssuranceProfile exists in the repository; direct review applies. Spec files validate (quire validate exit 0 each); roles/minder.md fails with unknown type 'RoleSpec', as the PR declares (archetype is an external dependency). quire matrix shows all 22 new criteria untagged/requirement-without-design, expected at the spec-only stage. No hash/digest/pin antipattern found. Owner intent was read from the program plan section W4a. Criterion-strength (Jev), evidence, risk-complexity and scope-boundary lenses were not run for this bounded review set.

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-006 | high | Moving the example to spec/roles/ (the FND-001 fix) makes `quire validate --scope . "spec/**/*.md"` exit 3 ('unknown type RoleSpec') at this head; origin/main exits 0. The repo has no Makefile or CI workflow, but this glob is the spec validation gate the spec-review and reviewer process runs, and every later spec PR would inherit the red. Keep the example out of spec/ until SWM-245 lands (for example docs/examples/minder-role-spec.md, referenced from FR-006-AC-6), and make moving it to spec/roles/minder.md part of SWM-245's acceptance. | spec/roles/minder.md:1-9 |

## Dispositions

Round 1, fix commit 4cad0509fcd863729c032e8a31aee0879594483a (reviewed diff 627838c..4cad050).

| FND | Outcome | Reason |
|---|---|---|
| FND-001 | fixed | Verified in 4cad050. |
| FND-002 | fixed | Verified in 4cad050. |
| FND-003 | fixed | Verified in 4cad050. |
| FND-004 | fixed | Verified in 4cad050. |
| FND-005 | fixed | Verified in 4cad050. |
| FND-006 | still-open | New in disposition pass 1; no fix yet. |
| FND-006 | fixed | Verified in round 2 at 3005249. |
