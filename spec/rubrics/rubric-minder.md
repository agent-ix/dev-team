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
[minder role spec](../roles/minder.md). A judgement evaluation cites one
check as `rubric-minder@2#<check-slug>`. `/team-retro` keeps scoring the
minder with its own version 1 rubric
(`skills/team-retro/references/rubric-minder.md`) until the minder skill
rewrite (SWM-225) moves the skill and team-retro to this version together.

Each check scores 0, 1 or 2 with one cited piece of evidence. A check scores
`n/a` when its evidence was not read; `n/a` is listed under Data quality and is
never counted as 0 or 2. Scores are not averaged. Deterministic measurements
come from the fleet ledger, relay receipts, hook events, the dialog answer log
and transcript queries; a judgement score never overrides a deterministic
verdict on the same rule.

Version 2 replaces two version 1 anchors that contradicted the role spec:
version 1 scored "unknown treated idle" and "repeated nudge" as failures, and
the role spec now requires both (MIND-R01, MIND-R05). Every send that
`fleet tick` emits, including `act_on_undetermined` actions and every ladder
rung, is required behaviour and is never scored down by any check.

## Checks

| ID | Check | Scale |
|----|-------|-------|
| rubric-minder@2#loop-alive | The minder loop ran every scheduled tick. Evidence: committed fleet ticks attributed to the minder session, scheduler entries. | 2: every tick committed; 1: a late or missed tick has a recorded remedy; 0: the loop stopped or was removed without the owner's instruction |
| rubric-minder@2#scope-coverage | Every registered lane and host in `ix-board fleet status` was considered in the tick. Evidence: status rows, defect rows, the tick's actions. | 2: every lane and defect accounted for; 1: a gap was routed to an owner; 0: a missing lane or host was treated as healthy |
| rubric-minder@2#liveness | Lane state was taken from `fleet tick` and `fleet status`, not from the minder's own reading. Evidence: tick actions and the minder's sends and answers. | 2: every action addressed to a lane or lead executed as emitted; 1: one action skipped, then corrected in the next tick; 0: an action skipped because a single weak signal (pane title, load average, self-report, queued order) was read as work |
| rubric-minder@2#undetermined-as-idle | Each per-lane `act_on_undetermined` action was executed by treating the lane as idle. Evidence: `act_on_undetermined` actions and the minder's sends. | 2: every such action executed in its tick; 1: executed one tick late; 0: an undetermined lane left alone as if working |
| rubric-minder@2#login-blocker | Login, usage-limit, question and unmatched dialog blocks were escalated to the lane's lead at rung 0. Evidence: `escalate_block` actions, the minder's sends. | 2: every such block escalated in the tick it was found; 1: escalated one tick late; 0: a block not escalated, or reported as working |
| rubric-minder@2#uncovered-answer | No dialog, login or permission prompt was answered without a matching standing order. Evidence: answer log, transcript, open `escalate_block` actions. | 2: no uncovered answer; 1: an uncovered answer the minder itself reported and routed; 0: an uncovered prompt answered silently |
| rubric-minder@2#dialog-answer | A dialog matching a standing order was answered per that order and logged with the order id. Evidence: `answer_dialog` actions, the answer log, the lane's next class. | 2: answered in the tick and logged; 1: answered late or the log entry incomplete; 0: a matched dialog left blocking the lane |
| rubric-minder@2#overdue-order | An order unconfirmed at its deadline (`AckExpired`, or `Acted` with focus on another ticket) was re-sent or escalated in the tick the deadline passed. Evidence: receipts, fleet focus, `resend_order` actions, escalations. | 2: every such order re-sent or escalated in its tick; 1: handled one tick late; 0: an unconfirmed order ignored or reported as taken up |
| rubric-minder@2#confirmation | An order was counted as taken up only when the lane's derived focus matched the ordered ticket. Evidence: receipts, fleet focus, the minder's report. | 2: every confirmation cites a focus match; 1: an order explicitly reported unconfirmed with its owner; 0: a queued, delivered or `Acted` order reported as taken up |
| rubric-minder@2#escalation-ladder | Every in-fleet ladder rung that `fleet tick` emitted was sent in its tick, including repeats to a recipient that already had an earlier rung. Owner paging is Alertmanager's and is not graded here. Evidence: ledger rung records, the minder's sends. | 2: every rung sent in its tick; 1: a rung sent one tick late; 0: a rung suppressed because an earlier message was sent |
| rubric-minder@2#evidence-cited | Each escalation carried its ledger action id and the status evidence it rests on. Evidence: escalation messages. | 2: every escalation cites action id and evidence; 1: one escalation lacks a reference; 0: escalations sent as opinion with no evidence reference |
| rubric-minder@2#message-hygiene | The minder sent nothing beyond what `fleet tick` emitted, and no status polls. Sends the tick emits (pushes, `act_on_undetermined`, resends, answers, every ladder rung) count as required, never as excess. Evidence: relay sends by the minder against tick actions. | 2: every send matches an emitted action or rung; 1: one send outside them, corrected; 0: status polls, or repeated sends that no action or rung emitted |
| rubric-minder@2#failed-probe | Every failed or timed-out source was routed to its owner as a defect in the tick. Evidence: `ix_fleet_probe_ok`, defect rows, `fix_source` actions and their routing. | 2: every failure routed in the tick; 1: recorded, route missing; 0: a failed probe read as healthy, or as unreachable-and-fine |

## Notes

- A missing worker field is never read as zero, and a partial row is never
  read as complete evidence for any score.
- An unconfirmed order does not justify a blind resend or an authentication
  approval; resends follow `resend_order` actions only.
