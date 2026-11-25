---
id: SR-061
title: "Integrity review of SWM-252 per-host ready buffer"
type: SpecReview
analysis: integrity
scope: "agent-ix/dev-team@bcbaf7fc20497e47aa7b99b4b1ba2a05b6363786; spec/roles/orchestrator.md, skills/fleet-orchestrator/references/capacity-discovery.md, skills/fleet-orchestrator/SKILL.md, spec/rubrics/rubric-orchestrator.md"
review_set: subset
---

## Summary

Ticket: SWM-252. Cross-document completeness of the demand rule: role spec, skill, reference, rubric and the ix-board FR-041 definition of the ready buffer.

## Verdict

**CONDITIONAL**. The four documents agree on the threshold (the greater of one ticket and the lane count at start, the step lane count for a window). The quantity compared with that threshold is not defined per host.

## Findings

| ID      | Severity | Summary | Refs |
| ------- | -------- | ------- | ---- |
| FND-001 | medium   | "Its ready buffer" has no definition: FR-041 defines one global buffer. Read as global, 3 hosts of 10 lanes with 12 ready tickets are all covered (30 lanes, 12 tickets); read as a share of 4 each, none is. ix-board#102 does both: a zero-lane host gets the global count and other hosts a share proportional to their target, so a host with unavailable duty gets no share and is never covered. | spec/roles/orchestrator.md:134, spec/roles/orchestrator.md:270 |
