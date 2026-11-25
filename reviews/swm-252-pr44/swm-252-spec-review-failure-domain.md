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

## New findings (disposition pass 1)

| ID      | Severity | Summary | Refs |
| ------- | -------- | ------- | ---- |
| FND-002 | high     | The diff limits a supplied lane to Started or Unstarted tickets, narrower than Amendment 1 (any unfinished ticket). In team SWM the ready states Specify and Backlog have type backlog: 4 lanes each queued 2 Specify tickets are unsupplied, those tickets have left the buffer, and every sample is short, which restores FND-001. | spec/roles/orchestrator.md:133, skills/fleet-orchestrator/references/capacity-discovery.md:7 |
| FND-003 | medium   | Hole left in Amendment 1: a host with no reachable lane needs buffer minus unsupplied lanes of at least 1, but ORCH-R06 queues every unowned ticket on other hosts' lanes. A restarted host with 0 lanes beside 4 supplied lanes holding 2 tickets each sees a buffer of 0 and never starts, although queued tickets could be moved to it. | spec/roles/orchestrator.md:138, spec/roles/orchestrator.md:283 |
| FND-004 | medium   | ORCH-R17 and the Valid window bullet let the zero-lane bootstrap test cover a step sample. A step at 5 lanes whose lanes all become unreachable while the lease stays current and a ticket is spare is judged valid, and its collapsed output reads as a knee. | spec/roles/orchestrator.md:280, spec/roles/orchestrator.md:155 |

## New findings (disposition pass 2)

| ID | Severity | Summary | Refs |
| -- | -------- | ------- | ---- |
| FND-005 | medium | The zero-lane formula has no floor at zero, while ix-board FR-041 (the producer) computes max(0, ready_buffer - all_hosts_unsupplied_lanes) + queued_behind_first. With buffer 0, 2 unsupplied lanes elsewhere and 2 queued tickets the text gives 0 (no start) and FR-041 gives 2, so the host is listed as a start candidate and an orchestrator following the role spec fails ORCH-R20-E1. Same text in the Capacity discovery paragraph, the Start bullet, both skill files and the rubric. | spec/roles/orchestrator.md:289 |

## Dispositions

Round 1, checked at faf8cfa0fc545c689d87cbc3b169f3af6b41cdc0.

| FND     | outcome | reason |
| ------- | ------- | ------ |
| FND-001 | fixed   | Supplied lanes now count toward coverage, so assigning ready tickets no longer removes demand for Started and Unstarted tickets. The backlog-type remainder is FND-002. |
| FND-002 | still-open | found in this pass. Needs a fix. |
| FND-003 | still-open | found in this pass. Needs an amendment or an accepted-no-change decision. |
| FND-004 | still-open | found in this pass. Needs a fix. |
| FND-002 | fixed | Any assigned ticket not completed, canceled or duplicate supplies a lane, backlog types included. |
| FND-003 | fixed | The zero-lane gate counts tickets queued behind the first ticket of reachable lanes, as Amendment 2 words it, in R20, both skill files and the rubric. |
| FND-004 | fixed | ORCH-R17, the Valid window bullet, the reference and the rubric require a reachable lane and bar the zero-lane rule from step windows. |

The rows added last are round 2, checked at fc263a5c55fe5f1e8c4befb348ddac4ddd34b886.
