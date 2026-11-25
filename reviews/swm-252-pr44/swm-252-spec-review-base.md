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

## New findings (disposition pass 1)

| ID      | Severity | Summary | Refs |
| ------- | -------- | ------- | ---- |
| FND-003 | medium   | The ORCH-R20-E1 violation query is now described as a current-candidate snapshot (latest sample at most 10 minutes old, no open run, current UTC day). The evaluator filters view rows to its window, so a daily run sees only the instant of evaluation: earlier missed starts are invisible, and a sample taken seconds before evaluation counts before the orchestrator has had a cycle. | spec/roles/orchestrator.md:230, spec/roles/orchestrator.md:327 |
| FND-004 | medium   | ORCH-R20 omits the cool-off. An unrecorded host with a step-down 1 hour ago and covered demand must be put into discovery, while ORCH-R23 forbids the raise and ix-board FR-041 refuses start within the cool-off. | spec/roles/orchestrator.md:283 |

## Dispositions

Round 1, checked at faf8cfa0fc545c689d87cbc3b169f3af6b41cdc0.

| FND     | outcome | reason |
| ------- | ------- | ------ |
| FND-001 | fixed   | ORCH-R20 excludes an open run and a used-up daily cap, and the candidate view excludes both. The view definition introduced FND-003. |
| FND-002 | still-open | the note now names the lease and share but says a host "is in discovery when its UTC-day cap is available", which ties a running discovery to the cap and drops capacity history and the open-run condition. Replace with a reference to the ORCH-R20 start conditions. |
| FND-003 | still-open | found in this pass. Needs a fix. |
| FND-004 | still-open | found in this pass. Needs a fix. |
| FND-002 | fixed | The note now refers to ORCH-R20. |
| FND-003 | still-open | The trigger of ORCH-R20-E1 is still the current-candidate view unrecorded_hosts_ready_for_discovery (latest sample per host at most 600 s old, as of now). FR-006 gives n.a. when a trigger has no row in the window, so with no current candidate at evaluation time earlier misses stay invisible. Trigger on ledger.unrecorded_hosts_with_demand (ix-board FR-041, per sample) in the E1 paragraph, the E1 row and the SWM-217 producer row. The violation query itself is now per sample. |
| FND-004 | fixed | ORCH-R20, the Start bullet, both skill files and the rubric exclude an active cool-off. |

The rows added last are round 2, checked at fc263a5c55fe5f1e8c4befb348ddac4ddd34b886.
