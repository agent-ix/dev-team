---
id: SR-003
title: "Gap analysis — SWM-106 program review renderer"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/dev-team; skills/program-reviewer/, tests/test_program_review_report.py, tests/fixtures/program-review-input.json; Linear SWM-106 acceptance criteria"
review_set: subset
---

## Summary

Manually compared the SWM-106 acceptance criteria and report contract with the renderer, its CLI, and the four focused tests. This repository has no `spec/` document root, so the computed requirement matrix and repository-wide reverse-gap audit were unavailable; plan completion was not assessed.

## Verdict

**CONDITIONAL** — the report-generation acceptance path is implemented and the focused tests pass, but reconcile findings are omitted and source text can trigger later template substitutions.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | Reconcile finding evidence is neither rendered nor covered by a test | skills/program-reviewer/scripts/render_report.py:198-210; tests/test_program_review_report.py |
| FND-002 | medium | The suite does not cover template-token text, which is substituted as generated markup | skills/program-reviewer/scripts/render_report.py:212-218; tests/test_program_review_report.py |

## Coverage

- Reconciliation: manual SWM-106 acceptance and report-contract comparison; `quoin matrix --repo . --json` and `quire matrix --scope . --format json` both refused because this repository has no `spec/` document root.
- Plan completion: not assessed
- Criteria: the repository matrix was unavailable; manually checked all three SWM-106 ticket acceptance criteria.
- AC-1: the renderer consumes captured JSON and reviewer judgments, and the CLI writes an HTML file; however, supplied reconcile command output is not consumed.
- AC-2: focused tests verify one row for a duplicated normalized project and one row for repeated blocker-ticket evidence.
- AC-3: focused tests verify mobile data labels and the narrow-screen table rules.
- Reverse-gap audit: not performed repository-wide because the required spec root is absent; this artifact reports only ticket-scope observations.
- Semantic review: skipped (not requested).

The approved proposal artifact URL was not accessible in this review; the Linear SWM-106 ticket was used as the acceptance scope.


## New findings (disposition pass 2)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | medium | Missing reconcile finding groups are silently treated as empty | skills/program-reviewer/scripts/render_report.py:157-160 |

## Disposition pass 2 notes

- FND-001 is fixed: reconcile records from all five groups are merged into the canonical ticket row. The regression test adds a reconcile-only ticket, repeats it across groups, and verifies one row with both evidence labels.
- FND-002 is fixed: source text equal to a later template token remains literal after rendering; the regression test checks the token-like project name and independent allocation output.
- FND-003 is new: `.get(group_name, [])` treats a missing required finding group as an empty group. An incomplete captured ReconcileReport can therefore omit findings without an error or unavailable marker.
- `pytest -q tests/test_program_review_report.py` passed (6 tests). The Quoin matrix remains unavailable because this repository has no `spec/` document root; the SWM-106 ticket acceptance criteria were checked manually.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | All five reconcile groups are traversed and merged by identifier into canonical rows; the regression test covers reconcile-only and repeated tickets. |
| FND-002 | fixed | Template substitution now runs once against the template, preserving source values that resemble token strings; the regression test covers this case. |
| FND-003 | fixed | Missing or malformed reconcile groups and records now produce visible incomplete-source warnings while preserving valid findings; the regression test covers these cases. |

| FND-003 | fixed | Missing or malformed reconcile groups and records now produce visible warnings; valid records continue to render, as verified by the regression test. |
| FND-004 | fixed | The renderer now rejects blank reconcile identifiers and flags them as incomplete; the regression test covers whitespace-only input. |

## New findings (disposition pass 3)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-004 | medium | Empty reconcile identifiers are accepted as ticket keys | skills/program-reviewer/scripts/render_report.py:171-175 |

## Disposition pass 3 notes

- FND-003 is fixed: the renderer reports incomplete reconcile objects, missing groups, non-array groups, and records without string identifiers while retaining valid records. The new regression test covers the partial payload.
- FND-004 is new: the renderer accepts an empty string as an identifier because it checks only the value's type. Direct reproduction produces a blank ticket row without an incomplete-source warning, contrary to the contract's treatment of missing or malformed identifiers.
- `pytest -q tests/test_program_review_report.py` passed (7 tests). The Quoin matrix remains unavailable because this repository has no `spec/` document root; ticket acceptance criteria were checked manually.


## Disposition pass 4 notes

- FND-004 is fixed: reconciliation now rejects blank identifiers and records a visible incomplete-source warning. The test covers a whitespace-only identifier; the same `strip()` guard rejects the empty string from the prior reproduction.
- `pytest -q tests/test_program_review_report.py` passed (7 tests); the delta contains no additional findings.
