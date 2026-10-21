---
id: SR-002
title: "Code review — dev-team program-reviewer skill"
type: SpecReview
analysis: code-review
scope: "agent-ix/dev-team; README.md, skills/index.json, skills/program-reviewer/SKILL.md, skills/program-reviewer/references/report-contract.md; SWM-105"
review_set: subset
---

## Summary

Reviewed PR #13 at head `3fd2be3915040a65634fb35bb5927fcb297ba5ff` against the live SWM-105 acceptance criteria. The required review steps and owner safeguards are present, but the report contract introduces a second owner for the M4 relay reply contract.

## Verdict

**FAIL** — the report contract duplicates the relay-owned status-reply schema and command contract, a high-severity ownership defect under the code-review duplication rule.

## Scope

The linked approved proposal at `https://claude.ai/artifact/PAs6Zz2LvedWmgcGLE9nbR` returned a Claude “Page not found” page in the authenticated browser and was unavailable to the web source. The review therefore uses the live SWM-105 issue acceptance criteria and the PR diff. The diff changes the README skill index, `skills/index.json`, the new program-reviewer skill, and its report contract.

### Acceptance criteria checked

- **SWM-105-AC-1** — “Skill text covers all seven steps, the value test, and that ticket and relay text is data” — examined. All seven numbered steps are present; the value test is in step 6; issue and relay content is explicitly treated as data.
- **SWM-105-AC-2** — “States that counts come from Linear at run time, and that a fact about a repo's purpose is measured, not guessed from its name” — examined. The boundaries require live Linear and GitHub outputs for every count and repo-purpose measurement from README, specifications, manifests, and source.
- **SWM-105-AC-3** — “Includes the ownership-rulings step: record the owner's rulings as Linear comments and relay them to the leads” — examined. The boundary and step 6 require issue comments and authorized relay, returning exact messages to the caller when the skill runs without lead relay authority.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | Report contract duplicates the M4 status-reply contract | skills/program-reviewer/references/report-contract.md:47 |

## New findings (disposition pass 1)

The follow-up review of the first fix round found this additional acceptance gap:

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-002 | medium | Owner rulings were not explicitly recorded as Linear comments | skills/program-reviewer/SKILL.md:16,26 |

## Review Notes

The report contract repeats the `agent-msg status-request` and `status-replies` invocation already defined in `skills/program-reviewer/SKILL.md`'s Command Contracts, then enumerates the relay reply fields and restates that `submitted_at_ms` is store-assigned. The field contract is owned by ix-relay (`crates/relay-core/src/status.rs` and the SWM-107 FR-056 contract); this new second copy can drift when the relay contract changes. Keep the report consumer coupled to the JSON actually returned, or reference the authoritative contract without maintaining a second field list or command definition.

The repository has no `spec/` tree, so Quoin's matrix check cannot build a matrix for this scope. I manually compared the three live acceptance criteria above with the changed skill and found each criterion represented in the text. No automated skill-evaluation or test files were found in this repository; there is no executable skill behavior in this Markdown-only diff to run as a code test. The approved proposal could not be inspected because its linked artifact page was unavailable.

## Findings Data

The private Linear review comment contains the machine-readable finding and the exact inspected scope.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | The duplicate reply-field list and command grammar are removed. The skill and report contract now delegate reply semantics to ix-relay FR-056 and installed command help. |
| FND-002 | fixed | The boundary and approval step now explicitly require each owner ruling to be recorded as a comment on the relevant Linear issue and relayed to responsible leads. |

### FND-001 after_excerpt

> Use the installed `agent-msg` CLI output as the source for lane status evidence.
> Preserve its returned JSON, lane attribution, timestamps, partial results, and
> unknown values without inventing or recalculating them. Follow ix-relay's
> canonical FR-056 and installed command help for the reply schema and command
> semantics; this report contract does not redefine them. Verify ticket and
> pull-request claims against live Linear and GitHub results before relying on
> them. If a required command is unavailable, report that source as unavailable
> and continue with independent evidence.

### FND-002 after_excerpt

> Do not apply a proposed batch of Linear changes until the owner approves it.
> Record owner rulings as comments on the relevant Linear issues. Relay those
> rulings to the responsible leads only through the authorized workflow; when
> running as a subagent without lead relay authority, return the exact proposed
> messages to the calling lead.

## Final review

The integrated PR #13 head `66ceccad3ffbc2fb7ae51c5baae2dddc06c15f27`, based on
PR #12 head `db5a9190eb08faeb607f7bb38a22e0a5758366b2`, received a fresh
read-only review. **PASS** — the seven review steps, live-count and repository
purpose safeguards, owner approval flow, Linear comment requirement, and
authorized relay step are present. The package index has one complete
`program-reviewer` declaration, and the workflow retains the report renderer,
contract, template, and tests.

## Re-review after SWM-106 rebase — PR #13 head `78c56988dc2b192f3bdb9ff42817bb9935fe2912`

Based on the updated SWM-106 PR head `fe48ead98320679d9603470b9e27234c0126f3e0`.

**PASS** — all three SWM-105 acceptance criteria remain satisfied. The skill contains all seven steps, the value test, the rule treating ticket and relay content as data, live Linear/GitHub counts, measured repository-purpose guidance, and the Linear-comment plus authorized-relay owner-ruling steps. It follows the updated SWM-106 contract without copying ix-board or ix-relay schemas. The role index contains one `program-reviewer` entry with the renderer and references.

- `pytest -q tests/test_program_review_report.py`: 11 passed.
- `skills/index.json` parses as JSON; Quire validation and `git diff --check` passed with existing configuration warnings.
- No `spec/` tree exists for a Quoin matrix; this docs-only review checked the live ticket criteria directly.
