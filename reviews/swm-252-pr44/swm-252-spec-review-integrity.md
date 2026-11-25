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

## New findings (disposition pass 1)

| ID      | Severity | Summary | Refs |
| ------- | -------- | ------- | ---- |
| FND-002 | medium   | Amendment 1 covers every current-lease zero-lane host when buffer minus all unsupplied lanes is at least 1. The diff instead hands one distinct ticket per host in host-ID order, so with 1 spare ticket an earlier host that is recorded or capped takes it and a later unrecorded host is never covered. ORCH-R20 also states the zero-lane test as an alternative to one a zero-lane host passes vacuously (0 supplied plus 0 share covers 0 lanes). | spec/roles/orchestrator.md:283, spec/roles/orchestrator.md:138 |

## Dispositions

Round 1, checked at faf8cfa0fc545c689d87cbc3b169f3af6b41cdc0.

| FND     | outcome | reason |
| ------- | ------- | ------ |
| FND-001 | fixed   | The Capacity discovery section now defines supplied lanes and each host's ready share as Amendment 1 states them. |
| FND-002 | still-open | found in this pass. Needs a fix. |
