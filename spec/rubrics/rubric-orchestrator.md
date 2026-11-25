---
id: rubric-orchestrator
version: 2
type: Rubric
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
---
# Rubric: orchestrator

The orchestrator rubric grades the judgement evaluations of the
[orchestrator role spec](../roles/orchestrator.md). The director grades it
from the orchestrator's transcript and the fleet evidence the transcript cites.
A judgement evaluation cites one check as `rubric-orchestrator@2#<check-slug>`.

Each check scores 0, 1 or 2 with one cited piece of evidence, or `n/a` when the
evidence was not read. `n/a` is listed under Data quality and is never counted
as 0 or 2. Scores are not averaged. A judgement score never overrides a
deterministic verdict on the same rule.

## Checks

| ID | Check | Scale |
|----|-------|-------|
| rubric-orchestrator@2#confirmation | Assignments were counted as taken up only on a `confirmed` result from `ix-board fleet assign` (focus equals the first ticket). Evidence: assign results, the orchestrator's plan statements. | 2: every claimed assignment cites a `confirmed` result; 1: an unconfirmed assignment stated as unconfirmed with a follow-up; 0: an `Acted`, delivered or queued order stated as owned work |
| rubric-orchestrator@2#in-target-claim | Every statement that hosts or lanes are in target, healthy or saturated rests on a `fleet status` run that exited zero with `complete: true`. Evidence: the claim and the status run before it. | 2: every claim cites a complete, zero-exit status run; 1: a claim with stale proof, corrected in the same cycle; 0: a claim with no proof, or made over a report carrying defects |
| rubric-orchestrator@2#failed-probe | A failed probe or source defect was fixed or routed to a named owner with a ticket in the cycle it appeared. Evidence: defect rows, `ix_fleet_probe_ok`, tickets, messages. | 2: fixed or routed in the cycle; 1: routed one cycle late; 0: the defect read as "unreachable", "fine" or someone else's problem and left open |
| rubric-orchestrator@2#dismissed-evidence | A minder escalation or alert was acted on, or rejected only by citing newer fleet status evidence that contradicts it. Evidence: escalation, the orchestrator's response, status rows. | 2: acted on, or rejected with cited contrary evidence; 1: acted on late; 0: dismissed without evidence, or the minder told to stop |
| rubric-orchestrator@2#thermal-excuse | A thermal or memory reason for holding lanes or builds was backed by scheduler evidence (pause, admission block, build abort, memory headroom below reserve) at that time, and lanes kept doing work that needs no build slot. Evidence: the stated reason, `ix_build_pause_seconds_total`, `ix_build_slots_sustainable`, lane classes. | 2: every hold cites scheduler evidence and lanes stayed busy on non-build work; 1: a hold with evidence but lanes idle briefly; 0: a hold with no scheduler evidence, or lanes idle with "thermal" as the reason |
| rubric-orchestrator@2#who-owns | An owner's question of who owns a ticket, lane, host, defect or decision got a named role and lane address. Evidence: the question and the answer. | 2: answered with a named owner and lane address; 1: owner named, address missing; 0: "unknown", a deferral, or a list of candidates |
| rubric-orchestrator@2#capacity-knee | Capacity discovery started only for an unrecorded host whose latest sample was no older than 10 minutes and showed a current lease and covered demand, with no open run, fewer than two starts that UTC day, no active step-down cool-off and writable capacity history. Demand used supplied lanes (reachable lanes with any assigned ticket not completed, canceled or duplicated, including backlog state types) plus the host's ready share, apportioned across unsupplied lanes by largest remainder and host-id tie break, capped at each host's unsupplied count. For a zero-lane host with a current registry lease, the discovery-start demand gate is met when the ready buffer minus all hosts' unsupplied lanes, taken as zero when negative, plus the tickets queued behind the first ticket of any reachable lane's assignment list, is at least one. Zero-lane bootstrap never covers a step window. Every sample in a step window had complete evidence, at least one reachable lane and covered the step; covering sample intervals spanned at least 90% of the window. A missing-evidence window was `deficit_coverage`; short demand was `demand_short`; a positive deficit, duty or `lanes_needed` availability did not change demand coverage. Discovery added one lane at a time, compared total host output (tickets closed plus pull requests merged per hour, commits pushed when those come to fewer than 5 in the window) with the previous level's mean per-lane output, excluded the 30-minute ramp-up, stopped at the first knee signal and stepped back one lane, ended with `build_slots_saturated` or `inconclusive_no_demand` where those applied, and recorded level and end reason. Build slots were left to the build scheduler. Evidence: capacity history, saturation and scheduler series per step, the recorded level. | 2: every start and step followed the evidence rules, windows were valid or repeated at most once, the run ended for a recorded reason taken from measured signals, level recorded; 1: right end reason but a window was thin or record incomplete; 0: capacity raised past a knee or slot saturation, a run started without demand or record capacity, build slots changed by hand, or the level not recorded |
