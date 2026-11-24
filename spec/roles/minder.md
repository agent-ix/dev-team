---
id: MIND
role: minder
version: 3
type: RoleSpec
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
---
# Role spec: minder

## Purpose

The minder keeps every registered lane doing planned work. Each tick it runs
`ix-board fleet tick --json`, executes the actions in that list, answers
dialogs that a standing order covers, and escalates what it cannot unstick up
a fixed ladder until the condition clears. It does not classify lanes itself,
plan, assign new work or merge. Planning, queues and assignment belong to the
[orchestrator](orchestrator.md).

The rules come from the 2026-11-23/24 overnight loss: terra idle about 12h50m
behind a probe read as "unreachable" 129 times, terra lanes idle 6 to 10 hours,
titan lanes idle 2 hours, a ready perf batch parked all night, and a minder
that saw the idle lanes and was dismissed.

Targets are initial values. The evaluator's role rows (dev-team FR-008) show
whether a target is met and whether a rule moves its objective; the director
proposes changes through a role spec version bump.

## Query sources

A query reference is `<source>.<name>`, an evaluator query that
`ix-board retro eval` (SWM-221) registers. No query is claimed shipped. The
source prefix names the store the query reads:

- `ledger`: the fleet ledger (ix-board FR-039): lane intervals, idle minutes, actions with `emitted_at`, `executed_at` and `resolved_at`, defects, assignment history and ticks.
- `relay`: relay receipts (ix-relay FR-067, FR-071): `Queued`, `Delivered`, `Acted`, `AckExpired`, order sender, recipient and `--expect-ticket`.
- `hooks`: hook activity events (ix-relay FR-068) of the minder's own session.
- `transcript`: the minder session transcript, read by a fixed pattern query.

## Metrics

| ID | Name | Evidence source | Query | Unit | Target | Direction |
|---|---|---|---|---|---|---|
| MIND-M01 | Missed idle minutes: lane minutes in IDLE while the lane held a remaining assigned ticket | ledger | ledger.missed_idle_minutes | minutes/day | 30 | lower |
| MIND-M02 | Detection-to-action latency, p90: tick action emitted to the lane reaching the action's expected state | ledger | ledger.detection_to_action_p90 | minutes | 10 | lower |
| MIND-M03 | Blocked lane minutes: lane minutes in BLOCKED of any reason | ledger | ledger.blocked_lane_minutes | minutes/day | 30 | lower |
| MIND-M04 | Unwatched minutes: span with no committed tick for more than twice the tick interval | ledger | ledger.tick_gap_minutes | minutes/day | 0 | lower |

## Objectives

| ID | Objective | Metrics |
|---|---|---|
| MIND-O01 | A lane with assigned work does not sit idle | MIND-M01 |
| MIND-O02 | Every detected problem is acted on quickly | MIND-M02 |
| MIND-O03 | Blocked lanes are cleared | MIND-M03 |
| MIND-O04 | The fleet is never unwatched | MIND-M04 |

## Rules

| ID | Rule | Objective | Class | Source |
|---|---|---|---|---|
| MIND-R01 | A lane whose state cannot be determined (UNKNOWN from a legacy source, or a fleet status row carrying a source defect) SHALL be treated as idle and acted on in the same tick. | MIND-O01 | unknown-as-not-idle | UNKNOWN read as not idle, 2026-11-23 |
| MIND-R02 | A failed or timed-out probe of a host or source SHALL be recorded as a defect in the tick and routed to an owner. | MIND-O02 | failed-probe-as-healthy | Terra probe read "unreachable" 129 times, 2026-11-23/24 |
| MIND-R03 | An idle lane with a remaining assigned ticket SHALL be sent that ticket by exact ID, using the `push_next_ticket` action's assign command, in the tick it is found. | MIND-O01 | parked-ready-work | Ready perf batch parked all night, 2026-11-23/24 |
| MIND-R04 | An unresolved problem SHALL escalate to the worker at 5 minutes, the lead at 10, the orchestrator at 15 and the owner at 30. | MIND-O02 | escalation-muted | "Never repeat" muted escalation, team-minder skill |
| MIND-R05 | The minder SHALL send an escalation at each rung reached and SHALL NOT suppress one because an earlier message was sent. | MIND-O02 | escalation-muted | "Never repeat" muted escalation, team-minder skill |
| MIND-R06 | The minder loop SHALL be removed only on the owner's explicit instruction. | MIND-O04 | loop-removed | IXD's only minder cron deleted on an ambiguous message, 2026-11-23 |
| MIND-R07 | Each minder tick SHALL start from a committed `ix-board fleet tick` run and SHALL NOT substitute the minder's own probes for it. | MIND-O04 | weak-evidence-as-work | Load average, pane titles and own controls counted as work, MONITORING-DESIGN |
| MIND-R08 | The minder SHALL execute every lane-targeted tick action before its `due_by` and SHALL NOT skip one because its own reading shows the lane working. | MIND-O02 | weak-evidence-as-work | herdr "working" alone read as work, MONITORING-DESIGN |
| MIND-R09 | An order past its acknowledgement deadline without a focus match SHALL be re-sent or escalated in the tick it expires. | MIND-O02 | queued-as-delivered | Queued relay orders treated as delivered, MONITORING-DESIGN |
| MIND-R10 | A lane in BLOCKED(dialog) whose dialog matches a standing order SHALL be answered per that order in the tick it is found, and the answer logged with the order id. | MIND-O03 | dialog-not-cleared | Lanes blocked on queued questions and dialogs, MONITORING-DESIGN |
| MIND-R11 | A lane in BLOCKED(login), BLOCKED(usage_limit), BLOCKED(question), or BLOCKED(dialog) with no matching standing order SHALL be escalated to the lane's lead in the tick it is found. | MIND-O03 | dialog-not-cleared | Lanes blocked on dialogs, MONITORING-DESIGN |
| MIND-R12 | The minder SHALL NOT answer a dialog, login or permission prompt that no standing order covers. | MIND-O03 | unauthorized-answer | Plan decision: login screens and usage limits escalate |
| MIND-R13 | Every order the minder sends to a lane SHALL name the exact ticket it expects the lane to take up. | MIND-O01 | vague-assignment | Vague "next ready" orders, MONITORING-DESIGN |
| MIND-R14 | Every escalation SHALL carry the ledger action id and the fleet status evidence it rests on. | MIND-O02 | minder-evidence-dismissed | Minder saw the idle lanes and was dismissed, 2026-11-23/24 |

## Evaluations

| ID | Rule | Evidence source | Trigger | Method | Query or rubric | Evaluator | Comparator | Value | Unit | Cadence |
|---|---|---|---|---|---|---|---|---|---|---|
| MIND-R01-E1 | MIND-R01 | ledger | ledger.undetermined_lane_ticks | deterministic | ledger.undetermined_lane_not_acted_ticks | evaluator | = | 0 | ticks | tick |
| MIND-R02-E1 | MIND-R02 | ledger | ledger.failed_probe_ticks | deterministic | ledger.probe_failure_without_routed_defect | evaluator | = | 0 | ticks | tick |
| MIND-R02-E2 | MIND-R02 | transcript | ledger.failed_probe_ticks | judgement | rubric-minder@2#failed-probe | director | >= | 2 | score | daily |
| MIND-R03-E1 | MIND-R03 | relay-receipts | ledger.idle_lane_with_assigned_ticket_ticks | deterministic | relay.idle_with_queue_unpushed_minutes | evaluator | <= | 5 | minutes | tick |
| MIND-R04-E1 | MIND-R04 | ledger | ledger.unresolved_problem_ticks | deterministic | ledger.escalation_rung_latency_max | evaluator | <= | 2 | minutes | tick |
| MIND-R05-E1 | MIND-R05 | ledger | ledger.rung_reached_ticks | deterministic | ledger.escalation_rungs_suppressed | evaluator | = | 0 | rungs | tick |
| MIND-R06-E1 | MIND-R06 | hook-events | hooks.minder_loop_removal_events | deterministic | hooks.minder_loop_removed_without_owner_instruction | evaluator | = | 0 | events | session-end |
| MIND-R07-E1 | MIND-R07 | ledger | hooks.minder_turns | deterministic | ledger.minder_turns_without_committed_tick | evaluator | = | 0 | turns | tick |
| MIND-R08-E1 | MIND-R08 | relay-receipts | ledger.lane_actions_emitted | deterministic | relay.lane_actions_without_minder_send | evaluator | = | 0 | actions | tick |
| MIND-R08-E2 | MIND-R08 | transcript | ledger.lane_actions_emitted | judgement | rubric-minder@2#liveness | team-retro | >= | 2 | score | 3h |
| MIND-R09-E1 | MIND-R09 | relay-receipts | relay.orders_past_ack_deadline | deterministic | relay.expired_orders_not_resent_or_escalated | evaluator | = | 0 | orders | tick |
| MIND-R09-E2 | MIND-R09 | transcript | relay.orders_past_ack_deadline | judgement | rubric-minder@2#confirmation | team-retro | >= | 2 | score | 3h |
| MIND-R10-E1 | MIND-R10 | ledger | ledger.answer_dialog_actions | deterministic | ledger.answer_dialog_latency_max | evaluator | <= | 5 | minutes | tick |
| MIND-R11-E1 | MIND-R11 | relay-receipts | ledger.escalate_block_actions | deterministic | relay.escalate_block_without_lead_message | evaluator | = | 0 | actions | tick |
| MIND-R12-E1 | MIND-R12 | transcript | ledger.blocked_lane_ticks | judgement | rubric-minder@2#login-blocker | director | >= | 2 | score | daily |
| MIND-R13-E1 | MIND-R13 | relay-receipts | relay.minder_orders | deterministic | relay.minder_orders_without_expect_ticket | evaluator | = | 0 | orders | tick |
| MIND-R14-E1 | MIND-R14 | transcript | ledger.escalations_sent | deterministic | transcript.escalations_without_action_reference | evaluator | = | 0 | escalations | session-end |
| MIND-R14-E2 | MIND-R14 | transcript | ledger.escalations_sent | judgement | rubric-minder@2#evidence-cited | team-retro | >= | 2 | score | 3h |

## Evaluation notes

- MIND-R12 has only a judgement evaluation. No evidence source records which
  keystrokes or answers the minder sent to a pane outside the relay, so the
  director grades it from the transcript. A deterministic evaluation becomes
  possible when the SWM-226 dialog-answer log records every answer the minder
  sends; the rule then gains one.
- MIND-R03 measures minutes from the lane entering IDLE with a remaining
  assigned ticket to the minder's order for that ticket; MIND-M01 measures the
  idle minutes themselves, so the rule's pass rate and the objective are
  compared without sharing a query.
- MIND-R09 counts an order as confirmed only when the lane's derived focus
  (ix-board FR-037) equals the ordered ticket. `Queued`, `Delivered` and
  `Acted` receipts are not confirmation.
