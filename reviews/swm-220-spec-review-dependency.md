---
id: SR-023
title: dependency review of SWM-220 role spec format and lint
type: SpecReview
analysis: dependency
review_set: subset
scope: "agent-ix/dev-team; SWM-220; spec/** and roles/minder.md at 627838c"
---

## Summary

Dependency review of the new relationships and the external capabilities FR-006 to FR-008 rely on, in particular whether reusing quire/quoin traceability for the lint is sound with the capabilities quire has today.

Ticket: SWM-220. Frozen PR: dev-team#30, 627838cfb2e62e93914b47e43cbd573dcc7a5a15.

## Verdict

**CONDITIONAL**. Reusing quire/quoin traceability is the right call (no second parser, the lint behaves like FR to AC to test). But FR-007 lists only 'trace-target declarations' as its dependency while the checks it promises need quire capabilities that do not exist today, and two external producers have no tracked owner.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | Quire trace targets today mint criterion ids from a table and attach them to the document (FR-NNN heading = requirement); there is no row-level requirement whose criteria are parented through another table's column (Rule), no orphan check for metrics unused by any objective, no resolution of an objective's metric list, and no rubric-file@version resolution. Deterministic bindings are trace tags in ix-board, a separate repository that a single-scope matrix does not scan (needs --repo). Name these as quire/quoin capability dependencies with tickets, or AC-6 ('no separate parser') cannot be met. | spec/functional/FR-007-role-spec-lint.md:24-33 |
| FND-002 | low | Dependencies name 'the owning Quire module' for the RoleSpec archetype (FR-006) and an ix-relay session start hook recording skill and role spec version (FR-008) without naming the module or a ticket; only SWM-221 is tracked. Name the module and link tickets so these blockers are planned. | spec/functional/FR-008-evaluation-result-record.md:63-67 |

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
- id: FR-007
  path: spec/functional/FR-007-role-spec-lint.md
  role: examined
  excerpt: The role-spec lint SHALL fail on any rule with no paired evaluation and any objective with no metric.
    It SHALL be computed by Quire and Quoin traceability, treating each rule as a requirement and each evaluation
    as its criterion, rather than by a purpose-built checker.
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
- id: FR-008
  path: spec/functional/FR-008-evaluation-result-record.md
  role: examined
  excerpt: The evaluator (`ix-board retro eval --role <r> [--session <id>] [--since <t>]`, SWM-221) SHALL emit evaluation
    results as three row kinds, defined here so the evaluator, the minder, team-retro and the director read one
    shape. This requirement defines the record; the evaluator's implementation belongs to ix-board.
- id: US-002
  path: spec/usecase/US-002-measured-role-rules.md
  role: context_only
  excerpt: '**As a** department owner running agent roles for days at a time **I want** every rule a role carries
    to come with a stated way of checking it, and the results rolled up per session and per role against the throughput
    the role exists to deliver **So that** I can see which rules are followed, which rules matter, and which skill
    instruction to change when a rule keeps failing.'
```

## Method and Limits

Diff scope: git diff origin/main...HEAD (US-002, FR-006, FR-007, FR-008, spec/spec.md index, roles/minder.md). No applicable AssuranceProfile exists in the repository; direct review applies. Spec files validate (quire validate exit 0 each); roles/minder.md fails with unknown type 'RoleSpec', as the PR declares (archetype is an external dependency). quire matrix shows all 22 new criteria untagged/requirement-without-design, expected at the spec-only stage. No hash/digest/pin antipattern found. Owner intent was read from the program plan section W4a. Criterion-strength (Jev), evidence, risk-complexity and scope-boundary lenses were not run for this bounded review set.

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-003 | low | FR-007 now attributes these capabilities to SWM-245, but SWM-245's checklist covers only the frontmatter schema, trace targets, enum/prefix/objective-metric/rule-evaluation asserts and validating the example. It does not list the unused-metric orphan check, versioned rubric references, the base-revision version-bump check or the skill-citation scan, and it still names roles/*.md. Update SWM-245, or file a sibling ticket for the lint-side checks, so the blocker is planned. This is a tracker change, not a spec edit. | spec/functional/FR-007-role-spec-lint.md:50-52 |

## Dispositions

Round 1, fix commit 4cad0509fcd863729c032e8a31aee0879594483a (reviewed diff 627838c..4cad050).

| FND | Outcome | Reason |
|---|---|---|
| FND-001 | fixed | Verified in 4cad050. |
| FND-002 | fixed | Verified in 4cad050. |
| FND-003 | still-open | New in disposition pass 1; no fix yet. |
