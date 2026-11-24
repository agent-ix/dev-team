---
id: rubric-minder
version: 2
type: Rubric
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
---
# Rubric: minder

The minder rubric grades the judgement evaluations of the
[minder role spec](../roles/minder.md) and the minder row of a `/team-retro`
full retro. A judgement evaluation cites one check as
`rubric-minder@2#<check-slug>`.

Each check scores 0, 1 or 2 with one cited piece of evidence. A check scores
`n/a` when its evidence was not read; `n/a` is listed under Data quality and is
never counted as 0 or 2. Scores are not averaged. Deterministic measurements
come from the fleet ledger, relay receipts and hook events; a judgement score
never overrides a deterministic verdict on the same rule.

Version 2 replaces two version 1 anchors that contradicted the role spec:
version 1 scored "unknown treated idle" and "repeated nudge" as failures, and
the role spec now requires both (MIND-R01, MIND-R05).

## Checks

| ID | Check | Scale |
|----|-------|-------|
| rubric-minder@2#loop-alive | The minder loop ran every scheduled tick. Evidence: committed fleet ticks in the ledger, the tick metric, scheduler entries. | 2: every tick committed; 1: a late or missed tick has a recorded remedy; 0: the loop stopped or was removed without the owner's instruction |
| rubric-minder@2#scope-coverage | Every registered lane and host in `ix-board fleet status` was considered in the tick. Evidence: status rows, defect rows, the tick's actions. | 2: every lane and defect accounted for; 1: a gap was routed to an owner; 0: a missing lane or host was treated as healthy |
| rubric-minder@2#liveness | Lane state was taken from `fleet tick` and `fleet status`, not from the minder's own reading. Evidence: tick actions and the minder's sends. | 2: every lane-targeted action executed as emitted; 1: one action skipped, then corrected in the next tick; 0: an action skipped because a single weak signal (pane title, load average, self-report, queued order) was read as work |
| rubric-minder@2#undetermined-as-idle | A lane whose state could not be determined was treated as idle. Evidence: status rows with source defects, the minder's actions. | 2: every undetermined lane acted on as idle in the tick; 1: acted on one tick late; 0: an undetermined lane left alone as if working |
| rubric-minder@2#login-blocker | Login, usage-limit, question and unmatched dialog blocks were escalated, never answered. Evidence: blocked status rows, escalations, keystrokes or answers sent. | 2: every such block escalated to the lane's lead in the tick and none answered; 1: escalation one tick late; 0: a block answered without a matching standing order, or reported as working |
| rubric-minder@2#dialog-answer | A dialog matching a standing order was answered per that order and the answer logged. Evidence: `answer_dialog` actions, answer log, the lane's next class. | 2: answered in the tick and logged; 1: answered late or log incomplete; 0: a matched dialog left blocking the lane |
| rubric-minder@2#overdue-order | An order past its acknowledgement deadline was re-sent or escalated in the tick it expired. Evidence: `AckExpired` receipts, `resend_order` actions, escalations. | 2: every expired order re-sent or escalated in its tick; 1: handled one tick late; 0: an expired order ignored |
| rubric-minder@2#confirmation | An order was counted as taken up only when the lane's derived focus matched the ordered ticket. Evidence: receipts, fleet focus, the minder's report. | 2: every confirmation cites a focus match; 1: an order explicitly reported unconfirmed with its owner; 0: a queued, delivered or `Acted` order reported as taken up |
| rubric-minder@2#escalation-ladder | An unresolved problem climbed worker, lead, orchestrator and owner at 5, 10, 15 and 30 minutes, repeating at each rung. Evidence: ledger actions, escalations sent, rung times. | 2: every rung reached on time and sent; 1: a rung late by one tick; 0: a rung suppressed because an earlier message was sent, or the ladder stopped while the condition held |
| rubric-minder@2#evidence-cited | Each escalation carried its ledger action id and the status evidence it rests on. Evidence: escalation messages. | 2: every escalation cites action id and evidence; 1: one escalation lacks a reference; 0: escalations sent as opinion with no evidence reference |
| rubric-minder@2#message-hygiene | The minder sent only tick actions and ladder rungs, and no status polls. Evidence: relay sends by the minder. | 2: no sends outside actions and rungs; 1: one extra send, corrected; 0: status polls or duplicate sends outside the ladder |
| rubric-minder@2#failed-probe | Every failed or timed-out source was recorded as a defect and routed in the tick. Evidence: `ix_fleet_probe_ok`, defect rows, `fix_source` actions and their routing. | 2: every failure recorded and routed in the tick; 1: recorded, route missing; 0: a failed probe read as healthy, or as unreachable-and-fine |

## Notes

- A missing worker field is never read as zero, and a partial row is never
  read as complete evidence for any score.
- An unconfirmed order does not justify a blind resend or an authentication
  approval; resends follow `resend_order` actions only.
