---
id: SR-024
title: ears-conformance review of SWM-220 role spec format and lint
type: SpecReview
analysis: ears-conformance
review_set: subset
scope: "agent-ix/dev-team; SWM-220; spec/** and roles/minder.md at 627838c"
---

## Summary

EARS conformance of the three new requirement statements (FR-006, FR-007, FR-008) and the normative clauses in their Behavior sections.

Ticket: SWM-220. Frozen PR: dev-team#30, 627838cfb2e62e93914b47e43cbd573dcc7a5a15.

## Verdict

**PASS with one low finding**. All three Description statements are ubiquitous SHALL statements with a named subject. One Behavior clause uses a modal that reads as permission.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | low | 'A judgement evaluation ... may not carry a tick cadence' uses 'may not', which reads as either prohibition or permission; AC-4 shows prohibition is meant. Write 'SHALL NOT carry'. | spec/functional/FR-006-role-spec-format.md:42-44 |

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
- id: FR-008
  path: spec/functional/FR-008-evaluation-result-record.md
  role: examined
  excerpt: The evaluator (`ix-board retro eval --role <r> [--session <id>] [--since <t>]`, SWM-221) SHALL emit evaluation
    results as three row kinds, defined here so the evaluator, the minder, team-retro and the director read one
    shape. This requirement defines the record; the evaluator's implementation belongs to ix-board.
```

## Method and Limits

Diff scope: git diff origin/main...HEAD (US-002, FR-006, FR-007, FR-008, spec/spec.md index, roles/minder.md). No applicable AssuranceProfile exists in the repository; direct review applies. Spec files validate (quire validate exit 0 each); roles/minder.md fails with unknown type 'RoleSpec', as the PR declares (archetype is an external dependency). quire matrix shows all 22 new criteria untagged/requirement-without-design, expected at the spec-only stage. No hash/digest/pin antipattern found. Owner intent was read from the program plan section W4a. Criterion-strength (Jev), evidence, risk-complexity and scope-boundary lenses were not run for this bounded review set.
