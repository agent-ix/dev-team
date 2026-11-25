---
id: SR-042
title: "code-review of SWM-230 role skill changes"
type: SpecReview
analysis: code-review
scope: "agent-ix/dev-team; SWM-230; diff origin/main...9cba2bd84b78bfdfc8cb073c429026b846f2c400 (PR dev-team#37): skills/{coder,reviewer,code-lead,team-planner,team-retro}/SKILL.md, skills/index.json, removed skills/team-retro/references/rubric-*.md, plugin manifests; context: skills/code-lead/references/{briefs,never,gate-log}.md"
review_set: subset
date: 2026-11-25
---

# code-review of SWM-230 role skill changes

## Summary

Reviewed the skill, manifest and catalog changes at 9cba2bd84b78bfdfc8cb073c429026b846f2c400 for conflicts with standing skill behaviour, stale references and release completeness. Several new rules forbid steps the same skills require. Ticket: SWM-230.

## Verdict

**FAIL**. One high finding: the gate rules leave no compliant way to merge after a failed gate or an overlap rebase.

Clean: the 0.7.0 bump is present in all four plugin manifests, and the five changed skills have bumped catalog versions. Each of the four role skills cites every rule id of its spec and no other. The removed rubric files have no remaining live reference; the only mentions are in historical `reviews/` records. Every former rubric row maps to rules that have at least one evaluation.

Not run: gap-analysis (the diff has no production code; the ticket's acceptance criteria were checked in the spec review), rust-review and review-react (no such code). The aggregate gate was not run.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | LEAD-R11 requires a passing aggregate gate at the merged head and LEAD-R06 allows one gate run per PR. The standing verify step says that when main moved with file overlap, rebase and rerun only the confined check (briefs.md:272-275), so following it merges a head with no gate and breaks LEAD-R11, while rerunning the gate breaks LEAD-R06. After a red gate there is no compliant merge either (the spec says LEAD-R06-E1 counts the rerun). Both rules, and CODE-R10, are also absolute while the skills say a repo or org rule that differs wins. | skills/code-lead/SKILL.md:253 |
| FND-002 | medium | LEAD-R08 forbids merging while any finding's latest outcome is still-open or missing, with no exception. Step 7 and briefs.md:292-293 tell the lead to merge the coder's one-line final fix with no further disposition marker, so that finding's latest outcome stays still-open or missing. A lead that follows the skill fails LEAD-R08-E1 and scores 0 on the open-findings check; only LEAD-R09 carries the exception. | skills/code-lead/SKILL.md:244 |
| FND-003 | medium | CODE-R12 forbids any push to a reported branch except in a fix round. The standing lead procedure sends the coder to push outside a fix round twice: the overlap rebase before merge (briefs.md:274-275) and the trailing commit of SR files after a clean review (briefs.md:244-246). A coder that obeys either request fails CODE-R12-E1; a coder that obeys CODE-R12 blocks the merge. | skills/coder/SKILL.md:83 |
| FND-004 | medium | The new instruction says every finding is on a file in the PR's file list. The reviewer brief allows a 'same bug elsewhere' finding once a failure is shown at that path (briefs.md:136), and a stale reference left in an unchanged file after a deletion is such a finding. A reviewer must now drop the real defect or fail REV-R11-E1. | skills/reviewer/SKILL.md:126 |
| FND-005 | low | The planner is now told not to dispatch coders (PLAN-R15, counted by transcript.planner_code_or_merge_commands), while step 4 of the same skill still tells it to route an isolated ticket to /coder. A planner following step 4 can be counted as violating PLAN-R15; the text does not say how routing differs from dispatching. | skills/team-planner/SKILL.md:13 |
| FND-006 | low | The new line asks for one run= across the review and its disposition passes, but step 5 defines run= as an id per invocation with a fresh uuidgen when the brief gives none, and was not changed. A retried review dispatch that posts the missing methods under a new uuid is correct behaviour under the dedup rule and fails REV-R01-E1. | skills/reviewer/SKILL.md:15 |
| FND-007 | low | team-retro now reads the four rubrics from blob/main URLs while citing version 1, and the skill catalog no longer ships any rubric file. After a rubric version bump on main, an installed team-retro 0.4.0 grades with the new anchors while citing @1, and a skill-only install without GitHub access cannot score at all. | skills/team-retro/SKILL.md:63 |
