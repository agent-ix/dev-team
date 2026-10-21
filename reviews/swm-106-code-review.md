---
id: SR-002
title: "Code review — SWM-106 program review report"
type: SpecReview
analysis: code-review
scope: "agent-ix/dev-team; skills/program-reviewer/references/report-contract.md, skills/program-reviewer/references/report-template.html; Linear SWM-106 acceptance criteria"
review_set: subset
---

## Summary

Reviewed the two report reference files in PR #12 against all three SWM-106 acceptance criteria. The contract and template define the expected report shape, but this PR does not generate or emit an HTML report from command JSON.

## Verdict

**CONDITIONAL** — the initial report-generation gap and the two first-round findings are fixed; a new medium finding remains for missing reconcile finding groups silently defaulting to empty.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | No report generator or program-reviewer integration produces an HTML artifact from command JSON | skills/program-reviewer/references/report-contract.md:3 |

## Review notes

- Reviewed all three SWM-106 acceptance criteria: report values sourced from command output plus reviewer judgment; no duplicate project or ticket rows; phone-width rendering.
- Reviewed all sections of `report-contract.md` and `report-template.html`, including source handling, de-duplication, escaping, unresolved-token failure, responsive styling, and the eight required sections.
- The responsive template and the written de-duplication and escaping rules are useful contracts, but no changed file implements rendering, reads command JSON, resolves the template tokens, or writes an HTML artifact. There is also no generation test in this PR. The required output therefore remains unimplemented here.
- No code, spec, or plan files changed. Language-specific review, Quoin gap-analysis, and spec-review methods were not applicable. No tests were run because the diff is documentation/template-only and contains no executable implementation.

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-002 | medium | Reconcile finding groups in captured command JSON are omitted from the report | skills/program-reviewer/scripts/render_report.py:198-210 |
| FND-003 | medium | Source text matching a later template token is replaced with generated HTML | skills/program-reviewer/scripts/render_report.py:212-218 |

## Disposition pass 1 notes

- FND-001 is fixed: `main()` reads the JSON input, calls `render()`, creates the output directory, and writes the generated HTML. The CLI acceptance test exercises this path.
- The four focused tests pass. They cover source rendering, deduplication, escaping, mobile labels, invalid roadmap input, and writing a complete HTML file.
- FND-002 is reproducible: a captured `ix-board reconcile --json` command is listed in the report source footer, but its finding identifier is absent from the HTML. The contract requires reconcile finding evidence to merge into the canonical ticket row.
- FND-003 is reproducible: a roadmap project name of `{{allocation_html}}` is escaped while constructing the roadmap, then the later token replacement substitutes the allocation section's generated HTML inside that project cell. This violates the contract's source-value escaping requirement.
- The approved proposal artifact was not accessible in this review; the current SWM-106 ticket was used as the acceptance scope.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | The renderer reads command JSON and writes the generated HTML artifact. |
| FND-002 | fixed | Reconcile-only and repeated reconcile evidence is merged into one canonical ticket row; the regression test verifies the issue appears once with its evidence. |
| FND-003 | fixed | One-pass template token substitution preserves a source project name equal to `{{allocation_html}}`; the regression test verifies the literal value remains in its cell. |
| FND-004 | fixed | Missing or malformed reconcile groups and records now produce visible incomplete-source warnings while preserving valid findings; the regression test covers these cases. |

| FND-004 | fixed | Missing groups, non-array groups, and records without a string identifier now produce visible warnings; the regression test verifies the omitted values are identified as undetermined. |
| FND-005 | fixed | The renderer now rejects blank reconcile identifiers and flags them as incomplete; the regression test covers whitespace-only input. |

## New findings (disposition pass 2)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-004 | medium | Missing reconcile finding groups are silently treated as empty | skills/program-reviewer/scripts/render_report.py:157-160 |

## Disposition pass 2 notes

- FND-002 is fixed: all five reconcile finding groups are merged by issue identifier into canonical ticket rows. The regression test verifies a reconcile-only ticket and repeated finding evidence render once.
- FND-003 is fixed: the renderer substitutes template tokens in the original template string in one pass, so source text equal to a token is not reprocessed as markup. The regression test verifies the literal token remains in the escaped project cell.
- FND-004 is new: the reconcile loop uses `.get(group_name, [])`, so a malformed or older payload that omits one of the five required groups silently renders as if it had no findings in that group. The contract says the report consumes the five finding groups; rendering should reject the incomplete shape or mark that group unavailable.
- `pytest -q tests/test_program_review_report.py` passed (6 tests). Quoin matrix was unavailable because this repository has no `spec/` document root.


## New findings (disposition pass 3)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-005 | medium | Empty reconcile identifiers are accepted as ticket keys | skills/program-reviewer/scripts/render_report.py:171-175 |

## Disposition pass 3 notes

- FND-004 is fixed: absent or malformed reconcile finding groups and records now generate an incomplete-source warning; valid records remain rendered. The regression test covers missing groups, a malformed group, and a record without an identifier.
- FND-005 is new: validation checks only whether `identifier` is a string. An empty string is accepted, creates a blank canonical ticket row, and emits no incomplete-source warning. A direct reproduction with `identifier: ""` rendered `— Missing key` and no warning.
- `pytest -q tests/test_program_review_report.py` passed (7 tests). Quoin matrix remains unavailable because the repository has no `spec/` document root.


## Disposition pass 4 notes

- FND-005 is fixed: reconciliation now rejects blank identifiers and records a visible incomplete-source warning. The test covers a whitespace-only identifier; the same `strip()` guard rejects the empty string from the prior reproduction.
- `pytest -q tests/test_program_review_report.py` passed (7 tests); the delta contains no additional findings.

## Final review pass — exact PR head `bf961a2cf141b80e489c2cc87ddc7dbc19ef8fd4`

### Exact-head summary

Freshly reviewed the changed SWM-106 renderer, its added regression tests, and the report contract against the two findings requested for re-review. Duplicate normalized roadmap names are flagged even without `projects_in_multiple_initiatives`; blocker `nodes`/`paths` and their `blocked_by`/`issues` identifier arrays reject malformed shapes. No new findings were identified.

### Exact-head verdict

**PASS** — both requested behaviors are implemented and covered by regression tests; the focused suite passes (10 tests).

### Exact-head review notes

- Confirmed the duplicate normalized project warning is computed from roadmap entries, independent of the optional upstream membership field; test `test_reports_duplicate_normalized_project_names_without_source_finding` removes that field and verifies one project row plus the data-quality warning.
- Confirmed blocker output requires `nodes` and `paths` arrays; each node requires non-empty string identifiers and a `blocked_by` array of non-empty string identifiers; each path requires an `issues` array of non-empty string identifiers. The new regression tests cover string-valued `blocked_by` and `issues`.
- Ran `python3 -m pytest -q tests/test_program_review_report.py`: 10 passed.
- Ran `quire validate --scope . 'reviews/**/*.md'`: passed with existing module duplicate-archetype warnings. `quire write` is unavailable in this installed version (`unrecognized subcommand 'write'`). No applicable AssuranceProfile or repository spec root exists.
