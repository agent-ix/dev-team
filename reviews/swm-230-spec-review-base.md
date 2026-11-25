---
id: SR-043
title: "spec-review base of SWM-230 role specs and rubrics"
type: SpecReview
analysis: base
scope: "agent-ix/dev-team; SWM-230; diff origin/main...9cba2bd84b78bfdfc8cb073c429026b846f2c400 (PR dev-team#37): spec/roles/{coder,reviewer,code-lead,planner}.md, spec/rubrics/rubric-{coder,reviewer,code-lead,planner}.md, spec/spec.md; against FR-006, FR-007, FR-008 and ix-board origin/main 67655b8 (FR-024, FR-029, FR-033, FR-035, FR-039, FR-041)"
review_set: subset
date: 2026-11-25
---

# spec-review base of SWM-230 role specs and rubrics

## Summary

Base review of four role specs and four rubrics at 9cba2bd84b78bfdfc8cb073c429026b846f2c400, with attention to whether evaluations can fail and whether `ix-board retro eval` can compute each query. Ticket: SWM-230.

## Verdict

**FAIL**. Three high findings: three merge and review-dispatch evaluations cannot be computed correctly from the sources they name.

Acceptance criteria: objectives and metrics exist for each of the four roles, including code-lead tickets closed per hour, PR cycle p50 and p90 and rework rounds. Every row of the four former rubrics maps to at least one rule with an evaluation and to a named check. Skills cite the rule ids.

Checks run with spec-artifacts-process 9f4f514 and spec-artifacts-iso origin/main: `quire validate` on `spec/**/*.md` exit 0, `--strict` on roles and rubrics exit 0, `--okf` exit 0, `quire coverage` exit 0 (30, 20, 22 and 23 evaluations minted, all unbacked). Every query used is defined, every defined query is used, no metric query is reused by an evaluation, and every rubric check is cited. With the locally installed spec-artifacts-process v0.29.2 the Rubric and RoleSpec types are not registered. Other analysis lenses were not run separately; consistency findings are in this base review. FR-007 binding was not checked because the lint is not built.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | LEAD-R11-E1 counts merged code PRs with no passing gate-log run at the merged head. The gate log has neither fact: each line carries pr, kind and four timestamps, no exit status and no commit hash (gate-log.md:18-19, scripts/team-gate:106). An implementer cannot compute it, and counting any gate line as passing lets a PR merged on a red gate pass. LEAD-R17-E1 depends on the same 'passing final gate'. | spec/roles/code-lead.md:88 |
| FND-002 | high | LEAD-R09-E1 compares the merged head with the last reviewed head, but no record holds the reviewed head: the reviewer and reviewer-dispositions markers carry no commit id and no GitHub review is posted. 'Changes behavior' also has no counting rule. The evaluation that guards unreviewed merges cannot be computed from the stated sources. | spec/roles/code-lead.md:87 |
| FND-003 | high | LEAD-R02-E1 reads pr_without_reviewer_age_hours, which counts GitHub review requests and GitHub reviews (ix-board department/collect.rs, pull_requests.rs). Reviews here are Linear markers, so a reviewed PR still counts as unreviewed. The GitHub collector takes the review-ready time only from a ready_for_review event, so one PR opened non-draft, as the coder skill does, makes the whole value unavailable. As a p90 it also passes with up to a tenth of PRs far over the limit although the rule says every PR, and it is unavailable when nothing is waiting, the compliant state. | spec/roles/code-lead.md:146 |
| FND-004 | medium | CODE-R13-E1 counts only acted_not_focused. Under ix-board FR-035 an order that was delivered and never acted on is ack_expired (timed_out when never delivered). A lane that ignores its order entirely therefore passes the rule that requires it to take the order up by the deadline. | spec/roles/coder.md:148 |
| FND-005 | medium | LEAD-R17-E1 needs a clean latest disposition, but a review with no findings gets no disposition pass, so the commonest clean PR is never counted. It also counts only PRs still open at evaluation time on a 3h cadence, so a PR merged two hours after becoming ready but before the run passes. Spec-only PRs, which skip the gate, are never counted. | spec/roles/code-lead.md:89 |
| FND-006 | medium | REV-M03 ends at 'the disposition after which no finding is still-open or without outcome', over PRs that reached that state. A first-pass clean review has no disposition, so those PRs drop out of the median; the metric overstates review-to-clean time and a window with only clean reviews is empty. | spec/roles/reviewer.md:63 |
| FND-007 | medium | REV-R12-E1 compares dispatch-to-first-comment time with 'the configured review age limit', but no spec, skill or ix-board configuration field defines that limit, so the query cannot be computed. LEAD-R02 names the same limit while LEAD-R02-E1 fixes it at 1 hour and REV-M02 targets a first-review p90 of 4 hours. | spec/roles/reviewer.md:78 |
| FND-008 | medium | The transcript source is defined as a fixed pattern query, but no pattern or marker is given for queries that classify meaning: message kinds (all four specs), delivery claims, done reports, recorded order audits. Skills define no message-kind tag. Two implementers would count the same transcript differently, so these deterministic verdicts are not reproducible as FR-008 requires. | spec/roles/coder.md:90 |
| FND-009 | medium | REV-R08 is about the reviewer not reporting a PR mergeable with an open finding; the check cited by REV-R08-E2 grades whether any finding was open at merge. A reviewer that correctly reports not mergeable, followed by a lead that merges anyway, scores 0 against the reviewer. The evaluation note admits the merge is the lead's. | spec/rubrics/rubric-reviewer.md:33 |
| FND-010 | low | CODE-R06 forbids a new PR or ticket for a finding on the open PR, but its query counts every PR or ticket created during a fix round. Filing a spec gap owned by another repo, which the coder and code-lead skills require of the coder, fails the evaluation. | spec/roles/coder.md:83 |
| FND-011 | low | PLAN-R11-E1 (recommendation on every ruling) cites the decisions check, which also grades ownership, rule PLAN-R10. A ruling with a recommendation but no owner scores below 2 and fails PLAN-R11, naming the wrong rule. | spec/rubrics/rubric-planner.md:39 |
| FND-012 | low | ledger.need_ready_tickets_unanswered does not exclude requests younger than a day at a daily run, names no stored ready count to measure 'gained', and reads as net growth: a planner that supplies the tickets while lanes consume them can fail PLAN-R14. | spec/roles/planner.md:82 |
| FND-013 | low | The producer column says the named ticket owns each missing producer. SWM-261 lists only minder and orchestrator references, and ix-board FR-039 defers the order_focus_at_deadline table behind ledger.lane_orders_due to SWM-255. Rows also say none while saying a requirement specifies the series or table, which contradicts the definition of none. | spec/roles/coder.md:73 |
| FND-014 | low | LEAD-R01 with a trigger of 'unblocked at some time in the window' fails a lead when a gate-path ticket unblocks minutes before the daily window ends. | spec/roles/code-lead.md:121 |
