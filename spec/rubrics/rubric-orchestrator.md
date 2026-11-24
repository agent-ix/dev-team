---
id: rubric-orchestrator
version: 1
type: Rubric
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
---
# Rubric: orchestrator

The orchestrator rubric grades the judgement evaluations of the
[orchestrator role spec](../roles/orchestrator.md). The director grades it
from the orchestrator's transcript and the fleet evidence the transcript cites.
A judgement evaluation cites one check as `rubric-orchestrator@1#<check-slug>`.

Each check scores 0, 1 or 2 with one cited piece of evidence, or `n/a` when the
evidence was not read. `n/a` is listed under Data quality and is never counted
as 0 or 2. Scores are not averaged. A judgement score never overrides a
deterministic verdict on the same rule.

## Checks

| ID | Check | Scale |
|----|-------|-------|
| rubric-orchestrator@1#confirmation | Assignments were counted as taken up only on a `confirmed` result from `ix-board fleet assign` (focus equals the first ticket). Evidence: assign results, the orchestrator's plan statements. | 2: every claimed assignment cites a `confirmed` result; 1: an unconfirmed assignment stated as unconfirmed with a follow-up; 0: an `Acted`, delivered or queued order stated as owned work |
| rubric-orchestrator@1#in-target-claim | Every statement that hosts or lanes are in target, healthy or saturated rests on a `fleet status` run that exited zero with `complete: true`. Evidence: the claim and the status run before it. | 2: every claim cites a complete, zero-exit status run; 1: a claim with stale proof, corrected in the same cycle; 0: a claim with no proof, or made over a report carrying defects |
| rubric-orchestrator@1#failed-probe | A failed probe or source defect was fixed or routed to a named owner with a ticket in the cycle it appeared. Evidence: defect rows, `ix_fleet_probe_ok`, tickets, messages. | 2: fixed or routed in the cycle; 1: routed one cycle late; 0: the defect read as "unreachable", "fine" or someone else's problem and left open |
| rubric-orchestrator@1#dismissed-evidence | A minder escalation or alert was acted on, or rejected only by citing newer fleet status evidence that contradicts it. Evidence: escalation, the orchestrator's response, status rows. | 2: acted on, or rejected with cited contrary evidence; 1: acted on late; 0: dismissed without evidence, or the minder told to stop |
| rubric-orchestrator@1#thermal-excuse | A thermal or memory reason for holding lanes or builds was backed by scheduler evidence (pause, admission block, build abort, memory headroom below reserve) at that time, and lanes kept doing work that needs no build slot. Evidence: the stated reason, `ix_build_pause_seconds_total`, `ix_build_slots_sustainable`, lane classes. | 2: every hold cites scheduler evidence and lanes stayed busy on non-build work; 1: a hold with evidence but lanes idle briefly; 0: a hold with no scheduler evidence, or lanes idle with "thermal" as the reason |
| rubric-orchestrator@1#who-owns | An owner's question of who owns a ticket, lane, host, defect or decision got a named role and lane address. Evidence: the question and the answer. | 2: answered with a named owner and lane address; 1: owner named, address missing; 0: "unknown", a deferral, or a list of candidates |
| rubric-orchestrator@1#capacity-knee | Capacity discovery added one lane at a time, judged each step only on a window with demand present (zero ready-buffer deficit, non-empty build queue), compared the added lane's marginal throughput with the mean per-lane throughput of the previous level, stopped at the first knee signal, stepped back one lane and recorded the level. Build slots were left to the build scheduler. Evidence: capacity history, saturation and scheduler series per step, the recorded level. | 2: every step valid or repeated, knee identified from the measured signals, level recorded; 1: knee found but a step judged on a thin window or the record incomplete; 0: capacity raised past a knee signal, judged on a window without demand, build slots changed by hand, or the level not recorded |
