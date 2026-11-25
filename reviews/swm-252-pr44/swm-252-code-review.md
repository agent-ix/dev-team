---
id: SR-058
title: "Code review of SWM-252 demand-coverage orchestrator skill text"
type: SpecReview
analysis: code-review
scope: "agent-ix/dev-team@bcbaf7fc20497e47aa7b99b4b1ba2a05b6363786; skills/fleet-orchestrator/SKILL.md, skills/fleet-orchestrator/references/capacity-discovery.md, spec/roles/orchestrator.md, spec/rubrics/rubric-orchestrator.md"
review_set: subset
---

## Summary

Ticket: SWM-252. PR dev-team#44, diff origin/main...bcbaf7fc20497e47aa7b99b4b1ba2a05b6363786. The skill text, its capacity reference and the rubric were compared with the orchestrator role spec at the same head, with the minder decision of 2026-11-25 on demand in ix-board FR-041, and with the FR-041 amendment and view definitions in the ix-board#102 worktree (head 056a782 plus uncommitted changes, read only).

## Verdict

**CONDITIONAL**. The new demand rule appears in the role spec, the skill, the reference and the rubric, and a search of the repository outside reviews/ finds no remaining zero-deficit gate. The view name unrecorded_hosts_with_demand matches ix-board#102; the reason demand_short is not named in this repository, as deficit_nonzero was not. The planner signal (ORCH-R14, SKILL.md step 8, the planner role spec) is unchanged. Rubric citations are all at version 2 and the skill frontmatter is at version 6. quire validate exits 0 with the spec-artifacts-process module from its origin/main (17da2da); the installed modules do not register RoleSpec or Rubric and reject both the base and the head files the same way. git diff --check passes. Gap analysis does not apply: the diff changes no production code.

## Findings

| ID      | Severity | Summary | Refs |
| ------- | -------- | ------- | ---- |
| FND-001 | medium   | Both skill files dropped, or never state, the start condition "the capacity history is available to record the run" that ORCH-R20 requires; the reference removed it in this diff. Only the not-installed case remains, so with fleet capacity installed and the ledger unwritable a run is started that cannot be recorded, breaching ORCH-R19. | skills/fleet-orchestrator/references/capacity-discovery.md:7, skills/fleet-orchestrator/SKILL.md:142 |
| FND-002 | low      | The skill and the reference say "current lane count" where the role spec and ORCH-R20 say "current reachable lane count". With 2 reachable and 2 unreachable lanes and 3 ready tickets the spec starts discovery and the skill reading does not. | skills/fleet-orchestrator/SKILL.md:142, skills/fleet-orchestrator/references/capacity-discovery.md:7 |
| FND-003 | low      | The frontmatter moved to role_spec_version 6 while the body still says the skill is the role "version 5". | skills/fleet-orchestrator/SKILL.md:11 |
| FND-004 | low      | The ownership reference still names role spec version 5 after the spec moved to 6. | skills/fleet-orchestrator/references/ownership.md:19 |
