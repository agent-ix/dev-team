---
id: SR-059
title: "Base review of SWM-252 orchestrator demand-coverage rules"
type: SpecReview
analysis: base
scope: "agent-ix/dev-team@bcbaf7fc20497e47aa7b99b4b1ba2a05b6363786; spec/roles/orchestrator.md, spec/rubrics/rubric-orchestrator.md"
review_set: subset
---

## Summary

Ticket: SWM-252. Base checklist over the diff of the orchestrator role spec and rubric, read against ORCH-R14, ORCH-R19, ORCH-R24, ORCH-R28 and the ix-board#102 view definitions.

## Verdict

**CONDITIONAL**. Versions are bumped (role spec 6, rubric 2), every rubric citation follows, no rule or evaluation id changed, and the renamed trigger view is consistent between the producers table and ORCH-R20-E1. One rule conflicts with the daily run cap and one evaluation note states the start condition incompletely.

## Findings

| ID      | Severity | Summary | Refs |
| ------- | -------- | ------- | ---- |
| FND-001 | medium   | ORCH-R20 requires discovery whenever demand covers an unrecorded host, with no exception for an open run or the daily cap. A host whose 2 runs today ended inconclusive_no_demand still has no level and has demand, so ORCH-R20 requires a third run that ORCH-R24 forbids. ORCH-R20-E1 (value 0) also counts samples taken during a run opened more than 10 minutes earlier, which demand coverage now makes the normal case. | spec/roles/orchestrator.md:270, spec/roles/orchestrator.md:314 |
| FND-002 | low      | The ORCH-R27 note says an unrecorded host waits for demand "to cover its current lanes". It omits the one-ticket floor and the registry lease, so a zero-lane host reads as covered with an empty buffer. | spec/roles/orchestrator.md:389 |
