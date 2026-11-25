---
id: SR-062
title: "Failure-domain review of the SWM-252 demand gate"
type: SpecReview
analysis: failure-domain
scope: "agent-ix/dev-team@bcbaf7fc20497e47aa7b99b4b1ba2a05b6363786; spec/roles/orchestrator.md (ORCH-R06, ORCH-R17, ORCH-R20)"
review_set: subset
---

## Summary

Ticket: SWM-252. Whether the new demand gate can be met by an orchestrator that follows the rest of the role spec. The defect is in the minder decision, which the diff implements faithfully on this point.

## Verdict

**FAIL**. The gate counts only tickets that ORCH-R06 requires the orchestrator to remove from the count in the same cycle.

## Findings

| ID      | Severity | Summary | Refs |
| ------- | -------- | ------- | ---- |
| FND-001 | high     | The ready buffer counts ready tickets in no reachable assignment, which is what plan-coverage reports as unowned_ready and ORCH-R06 closes each cycle by assigning them. A host with 4 lanes and 8 ready tickets, 2 assigned to each lane (ORCH-R03), has ready work for every lane and a buffer of 0, so no run starts and every window is demand_short. The gate passes mainly while ORCH-R06 gaps are left open, so SWM-189 stays blocked for a compliant orchestrator. | spec/roles/orchestrator.md:267, spec/roles/orchestrator.md:256 |
