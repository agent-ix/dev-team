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

## New findings (disposition pass 1)

Found in the fix diff 9cba2bd..388ee6a.

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-008 | low | The fix-round list now says a gap another repo or lane owns is filed as step 2 describes, which has the coder file it, and two bullets later says to report items owned by another repo or lane because the leader files those. A coder with a cross-owned finding that is a spec gap can file it while the leader files it again, or neither files it. | skills/coder/SKILL.md:105 |
| FND-009 | medium | Merge now needs the latest reviewer or disposition marker head to cover the merged head, but after a clean review no disposition pass runs and the reviewer posts dispositions only for artifacts that had findings. When the gate then fails on a clean-review PR and the coder fixes it with more than one line, no step can record a new head, and reposting a method is deduplicated. The lead must merge uncovered, failing LEAD-R09-E1 and verify item 7, or stay blocked. | skills/code-lead/SKILL.md:213 |

## Dispositions

Round 1, head 388ee6a1f08aa61eb88da49e83883f61635b190a.

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | skills/code-lead/SKILL.md:257-262 |
| FND-002 | fixed | skills/code-lead/SKILL.md:246-249 |
| FND-003 | fixed | skills/coder/SKILL.md:83 |
| FND-004 | fixed | skills/reviewer/SKILL.md:129-132 |
| FND-005 | fixed | skills/team-planner/SKILL.md:13 |
| FND-006 | fixed | skills/reviewer/SKILL.md:14-17 |
| FND-007 | accepted-no-change | Ruled accepted-no-change on the remainder. The version drift half is fixed: team-retro grades the rubrics shipped in its own plugin installation, or those at the install ref, cites the frontmatter version, and records n/a with reason 'rubric unavailable' otherwise. A skills-only install still ships no rubric. That is accepted: FR-006 places rubrics in spec/rubrics/, shipping them in the skill catalog would need a second copy, and the OpenCode install already fetches this repository from GitHub (README install table), so the files are reachable at the same ref. The unread case is reported as missing data, never as a score. Residual limit: the OpenCode ref is main, so a cached skill can read a newer rubric. |
