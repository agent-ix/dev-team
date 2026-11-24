---
id: SR-029
title: "integrity review of SWM-222/223 role-spec evidence sources"
type: SpecReview
analysis: integrity
scope: "agent-ix/dev-team; SWM-222, SWM-223; spec/roles/**, spec/rubrics/**, spec/functional/FR-006, spec/spec.md, skills/team-retro diff origin/main...96d8047 (PR dev-team#32)"
review_set: subset
date: 2026-11-24
---

# integrity review of SWM-222/223 role-spec evidence sources

## Summary

Tickets: SWM-222 (orchestrator role spec), SWM-223 (minder role spec). Frozen PR: dev-team#32 at 96d8047. Evidence contracts read from origin/main: ix-board FR-034..043, ix-relay FR-058 and FR-067..072, dev-team FR-006..010 and FR-015. Validation re-run with quire 0.52.1 against the spec-artifacts-process origin/main export (80d25b6): validate, --strict, --okf and coverage exit 0.

## Verdict

**FAIL**. The query sources ledger, relay, hooks and prom mostly resolve to the ix-board FR-034..041 and ix-relay FR-067..072 contracts, and prom.* capacity reads are ticketed (SWM-252). The `fleet` source has no store. Escalation and ladder records, drift and assign results are not in any contract, and four evaluations cannot be computed as specified.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | The `fleet` query source has no store. The orchestrator spec says that plan-coverage and saturation snapshots are 'taken each tick', but ix-board FR-038 records only the tick and its actions, FR-039 has a `saturation_sample` table but no plan-coverage table, and FR-036 exports no metric. fleet.short_queue_lane_minutes_max (ORCH-R03-E1) and fleet.plan_coverage_gap_age_max (ORCH-R06-E1), the only deterministic evaluations of ORCH-R03 and R06, are unproduced and not ticketed. | spec/roles/orchestrator.md:157 |
| FND-002 | high | Escalation rungs and minder escalations are recorded in no evidence contract. ledger.escalation_rung_latency_max (MIND-R04-E1), ledger.escalation_rungs_suppressed (MIND-R05-E1), ledger.orchestrator_escalation_open_max (ORCH-R10-E1) and their triggers (ledger.unresolved_problem_ticks, rung_reached_ticks, escalations_to_orchestrator) read ledger rows that ix-board FR-039 does not define. Its `action` table holds tick-emitted actions only, FR-038 has no ladder, and the ix-relay FR-067 export excludes message bodies. The plan (W3) also puts the same ladder in Alertmanager, so two ladders would page. The record and the single ladder owner need a ticket. | spec/roles/minder.md:87 |
| FND-003 | high | MIND-R01 conflicts with the tick contract. ix-board FR-038 says the minder executes the action list and does not re-derive it, and FR-034 classes a lane that has a source defect from its remaining evidence, so a WORKING or BLOCKED row with a defect gets no idle action. Acting on it means the minder re-derives state, which MIND-R07 and R08 and rubric#message-hygiene forbid, and its act is recorded nowhere, so ledger.undetermined_lane_not_acted_ticks has no producer. 'Row carrying a source defect' is also too broad: a host-wide `stale_source` (for example temperature) would make every lane on the host idle despite fresh hook evidence. Put undetermined-as-idle into FR-034 and FR-038 (a `push_next_ticket`/`escalate` action for defect rows without hook evidence) and have MIND-R01 execute that action. | spec/roles/minder.md:63 |
| FND-004 | medium | Drift is not persisted. ix-board FR-037 computes focus and drift on read and keeps no store, and the FR-039 ledger has no drift table. `not_in_plan` also needs the historical ready queue, which the ledger does not keep. ledger.drift_finding_open_max (ORCH-R13-E1) and ledger.drift_lane_minutes_share (ORCH-M05) are unproduced and not ticketed. | spec/roles/orchestrator.md:168 |
| FND-005 | medium | The `fleet assign` results (`confirmed`, `acted_not_focused`, `ack_expired`, `timed_out`) are not specified as ledger content. FR-039's `assignment_history` has no field list, and FR-035 records only a list-write failure. ORCH-R04-E1 and ORCH-R05-E1 read them anyway. ORCH-R05's 10-minute confirm window also exceeds assign's 5-minute default deadline, after which assign stops watching, so confirmation between 5 and 10 minutes is observed by nothing unless it is derived from `lane_interval.focus`. State the derivation or ticket the field. | spec/roles/orchestrator.md:154 |
| FND-006 | medium | relay.orchestrator_orders_not_via_fleet_assign has no join key. ix-relay FR-067 receipts carry sender, target and message identity but not the command that sent them, and FR-072 transition records carry no order identity. Nothing ties an order to a `fleet assign` write, so the query cannot be computed. Ticket an order id on the FR-072 transition (or a sender tag on the order). | spec/roles/orchestrator.md:152 |
| FND-007 | medium | relay.lane_actions_without_minder_send counts lane actions with no matching minder relay send, but `answer_dialog` is executed by answering in the pane, not by a relay send, so every answered dialog counts as a miss. The FR-067 export also excludes message bodies, so a send cannot be matched to an action id; only recipient and time can be matched. Exclude `answer_dialog` (MIND-R10 covers it) and state the time-and-recipient match. | spec/roles/minder.md:90 |
| FND-008 | medium | hooks.minder_loop_removed_without_owner_instruction cannot decide 'without owner instruction' from hooks. ix-relay FR-068 events carry the tool name only, and `prompt` events carry no text, so a cron-delete tool call is visible but the owner's instruction is not. The evaluation needs the transcript (the SWM-221 transcript query kind) or an owner-instruction record. | spec/roles/minder.md:88 |
| FND-009 | medium | MIND-R09 covers an order 'past its acknowledgement deadline without a focus match', which includes `acted_not_focused` (Acted before the deadline, wrong focus). Its trigger relay.orders_past_ack_deadline sees only `AckExpired` receipts, which an Acted order never gets, so the queued-as-delivered case this rule exists for is never triggered. Add a ledger or focus-based trigger for Acted-not-focused orders. | spec/roles/minder.md:92 |
| FND-010 | low | ledger.minder_turns_without_committed_tick has no attribution. The FR-039 `tick` table (id, started_at, committed_at) records no session or caller, so a minder turn can be matched to a tick only by time window. State the time-window join, or ticket a caller field on `tick`. | spec/roles/minder.md:89 |
| FND-011 | low | The recorded capacity has two homes. The Capacity discovery 'Record' step and ORCH-R18 say the found level 'becomes the host's configured server capacity (ix-relay FR-058)', but FR-058 stores cores, RAM, max agent count and owner rules, with no build slots and no measurements. The evaluation notes say SWM-252 provides the store. Name SWM-252 as the record and FR-058 only as the lane-count projection. | spec/roles/orchestrator.md:142 |

## Examined Scope

```yaml
scope:
- id: MIND-R01-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R01-E1 | MIND-R01 | ledger | ledger.undetermined_lane_ticks | deterministic | ledger.undetermined_lane_not_acted_ticks
    | evaluator | = | 0 | ticks | tick |'
- id: MIND-R02-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R02-E1 | MIND-R02 | ledger | ledger.failed_probe_ticks | deterministic | ledger.probe_failure_without_routed_defect
    | evaluator | = | 0 | ticks | tick |'
- id: MIND-R02-E2
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R02-E2 | MIND-R02 | transcript | ledger.failed_probe_ticks | judgement | rubric-minder@2#failed-probe |
    director | >= | 2 | score | daily |'
- id: MIND-R03-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R03-E1 | MIND-R03 | relay-receipts | ledger.idle_lane_with_assigned_ticket_ticks | deterministic | relay.idle_with_queue_unpushed_minutes
    | evaluator | <= | 5 | minutes | tick |'
- id: MIND-R04-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R04-E1 | MIND-R04 | ledger | ledger.unresolved_problem_ticks | deterministic | ledger.escalation_rung_latency_max
    | evaluator | <= | 2 | minutes | tick |'
- id: MIND-R05-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R05-E1 | MIND-R05 | ledger | ledger.rung_reached_ticks | deterministic | ledger.escalation_rungs_suppressed
    | evaluator | = | 0 | rungs | tick |'
- id: MIND-R06-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R06-E1 | MIND-R06 | hook-events | hooks.minder_loop_removal_events | deterministic | hooks.minder_loop_removed_without_owner_instruction
    | evaluator | = | 0 | events | session-end |'
- id: MIND-R07-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R07-E1 | MIND-R07 | ledger | hooks.minder_turns | deterministic | ledger.minder_turns_without_committed_tick
    | evaluator | = | 0 | turns | tick |'
- id: MIND-R08-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R08-E1 | MIND-R08 | relay-receipts | ledger.lane_actions_emitted | deterministic | relay.lane_actions_without_minder_send
    | evaluator | = | 0 | actions | tick |'
- id: MIND-R08-E2
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R08-E2 | MIND-R08 | transcript | ledger.lane_actions_emitted | judgement | rubric-minder@2#liveness | team-retro
    | >= | 2 | score | 3h |'
- id: MIND-R09-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R09-E1 | MIND-R09 | relay-receipts | relay.orders_past_ack_deadline | deterministic | relay.expired_orders_not_resent_or_escalated
    | evaluator | = | 0 | orders | tick |'
- id: MIND-R09-E2
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R09-E2 | MIND-R09 | transcript | relay.orders_past_ack_deadline | judgement | rubric-minder@2#confirmation
    | team-retro | >= | 2 | score | 3h |'
- id: MIND-R10-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R10-E1 | MIND-R10 | ledger | ledger.answer_dialog_actions | deterministic | ledger.answer_dialog_latency_max
    | evaluator | <= | 5 | minutes | tick |'
- id: MIND-R11-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R11-E1 | MIND-R11 | relay-receipts | ledger.escalate_block_actions | deterministic | relay.escalate_block_without_lead_message
    | evaluator | = | 0 | actions | tick |'
- id: MIND-R12-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R12-E1 | MIND-R12 | transcript | ledger.blocked_lane_ticks | judgement | rubric-minder@2#login-blocker
    | director | >= | 2 | score | daily |'
- id: MIND-R13-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R13-E1 | MIND-R13 | relay-receipts | relay.minder_orders | deterministic | relay.minder_orders_without_expect_ticket
    | evaluator | = | 0 | orders | tick |'
- id: MIND-R14-E1
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R14-E1 | MIND-R14 | transcript | ledger.escalations_sent | deterministic | transcript.escalations_without_action_reference
    | evaluator | = | 0 | escalations | session-end |'
- id: MIND-R14-E2
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R14-E2 | MIND-R14 | transcript | ledger.escalations_sent | judgement | rubric-minder@2#evidence-cited |
    team-retro | >= | 2 | score | 3h |'
- id: ORCH-R01-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R01-E1 | ORCH-R01 | relay-receipts | relay.orchestrator_orders | deterministic | relay.orchestrator_orders_without_expect_ticket
    | evaluator | = | 0 | orders | tick |'
- id: ORCH-R02-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R02-E1 | ORCH-R02 | relay-receipts | relay.orchestrator_orders | deterministic | relay.orchestrator_orders_not_via_fleet_assign
    | evaluator | = | 0 | orders | 3h |'
- id: ORCH-R03-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R03-E1 | ORCH-R03 | ix-board-metric | fleet.lanes_with_ready_work | deterministic | fleet.short_queue_lane_minutes_max
    | evaluator | <= | 15 | minutes | tick |'
- id: ORCH-R04-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R04-E1 | ORCH-R04 | ledger | ledger.unconfirmed_assign_results | deterministic | ledger.unconfirmed_assignments_without_followup
    | evaluator | = | 0 | assignments | tick |'
- id: ORCH-R04-E2
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R04-E2 | ORCH-R04 | transcript | ledger.unconfirmed_assign_results | judgement | rubric-orchestrator@1#confirmation
    | director | >= | 2 | score | daily |'
- id: ORCH-R05-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R05-E1 | ORCH-R05 | ledger | ledger.assignments_sent | deterministic | ledger.assignment_confirm_latency_max
    | evaluator | <= | 10 | minutes | 3h |'
- id: ORCH-R06-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R06-E1 | ORCH-R06 | ix-board-metric | fleet.plan_coverage_gap_rows | deterministic | fleet.plan_coverage_gap_age_max
    | evaluator | <= | 15 | minutes | tick |'
- id: ORCH-R07-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R07-E1 | ORCH-R07 | transcript | transcript.fleet_health_claims | deterministic | transcript.in_target_claims_without_complete_status
    | evaluator | = | 0 | claims | session-end |'
- id: ORCH-R07-E2
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R07-E2 | ORCH-R07 | transcript | transcript.fleet_health_claims | judgement | rubric-orchestrator@1#in-target-claim
    | director | >= | 2 | score | daily |'
- id: ORCH-R08-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R08-E1 | ORCH-R08 | ledger | ledger.defect_rows | deterministic | ledger.defects_open_beyond_one_cycle
    | evaluator | = | 0 | defects | tick |'
- id: ORCH-R08-E2
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R08-E2 | ORCH-R08 | transcript | ledger.defect_rows | judgement | rubric-orchestrator@1#failed-probe |
    director | >= | 2 | score | daily |'
- id: ORCH-R09-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R09-E1 | ORCH-R09 | ledger | ledger.idle_lane_with_ready_work_ticks | deterministic | ledger.idle_lane_episode_with_ready_work_max
    | evaluator | <= | 10 | minutes | tick |'
- id: ORCH-R10-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R10-E1 | ORCH-R10 | ledger | ledger.escalations_to_orchestrator | deterministic | ledger.orchestrator_escalation_open_max
    | evaluator | <= | 15 | minutes | tick |'
- id: ORCH-R10-E2
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R10-E2 | ORCH-R10 | transcript | ledger.escalations_to_orchestrator | judgement | rubric-orchestrator@1#dismissed-evidence
    | director | >= | 2 | score | daily |'
- id: ORCH-R11-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R11-E1 | ORCH-R11 | ledger | prom.host_build_pause_intervals | deterministic | ledger.idle_lane_minutes_during_build_pause
    | evaluator | <= | 10 | minutes | 3h |'
- id: ORCH-R12-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R12-E1 | ORCH-R12 | ix-board-metric | prom.host_capacity_reductions | deterministic | prom.capacity_reductions_without_throttle_evidence
    | evaluator | = | 0 | reductions | daily |'
- id: ORCH-R12-E2
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R12-E2 | ORCH-R12 | transcript | prom.host_capacity_reductions | judgement | rubric-orchestrator@1#thermal-excuse
    | director | >= | 2 | score | daily |'
- id: ORCH-R13-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R13-E1 | ORCH-R13 | ledger | ledger.drift_findings | deterministic | ledger.drift_finding_open_max | evaluator
    | <= | 15 | minutes | 3h |'
- id: ORCH-R14-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R14-E1 | ORCH-R14 | relay-receipts | ledger.need_ready_tickets_actions | deterministic | relay.need_ready_tickets_without_planner_order
    | evaluator | = | 0 | actions | tick |'
- id: ORCH-R15-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R15-E1 | ORCH-R15 | transcript | transcript.owner_ownership_questions | deterministic | transcript.ownership_answers_without_lane_address
    | evaluator | = | 0 | answers | session-end |'
- id: ORCH-R15-E2
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R15-E2 | ORCH-R15 | transcript | transcript.owner_ownership_questions | judgement | rubric-orchestrator@1#who-owns
    | director | >= | 2 | score | daily |'
- id: ORCH-R16-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R16-E1 | ORCH-R16 | ix-board-metric | prom.host_capacity_increases | deterministic | prom.capacity_steps_violating_ramp
    | evaluator | = | 0 | steps | daily |'
- id: ORCH-R17-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R17-E1 | ORCH-R17 | ix-board-metric | prom.capacity_discovery_steps | deterministic | prom.capacity_raised_past_knee
    | evaluator | = | 0 | steps | daily |'
- id: ORCH-R17-E2
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R17-E2 | ORCH-R17 | transcript | prom.capacity_discovery_steps | judgement | rubric-orchestrator@1#capacity-knee
    | director | >= | 2 | score | weekly |'
- id: ORCH-R18-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R18-E1 | ORCH-R18 | ix-board-metric | prom.hosts_with_completed_discovery | deterministic | prom.hosts_without_recorded_level
    | evaluator | = | 0 | hosts | daily |'
- id: ORCH-R19-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R19-E1 | ORCH-R19 | ix-board-metric | prom.hosts_with_recorded_level | deterministic | prom.host_minutes_above_recorded_level_outside_discovery
    | evaluator | = | 0 | minutes | daily |'
- id: ORCH-R20-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R20-E1 | ORCH-R20 | ix-board-metric | prom.hosts_throttled_at_recorded_level | deterministic | prom.throttled_hosts_without_step_down
    | evaluator | = | 0 | hosts | daily |'
- id: ORCH-R21-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R21-E1 | ORCH-R21 | ledger | ledger.add_lane_actions | deterministic | ledger.add_lane_action_open_max
    | evaluator | <= | 15 | minutes | tick |'
- id: MIND-M01
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-M01 | Missed idle minutes: lane minutes in IDLE while the lane held a remaining assigned ticket | ledger
    | ledger.missed_idle_minutes | minutes/day | 30 | lower |'
- id: MIND-M02
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-M02 | Detection-to-action latency, p90: tick action emitted to the lane reaching the action''s expected
    state | ledger | ledger.detection_to_action_p90 | minutes | 10 | lower |'
- id: MIND-M03
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-M03 | Blocked lane minutes: lane minutes in BLOCKED of any reason | ledger | ledger.blocked_lane_minutes
    | minutes/day | 30 | lower |'
- id: MIND-M04
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-M04 | Unwatched minutes: span with no committed tick for more than twice the tick interval | ledger | ledger.tick_gap_minutes
    | minutes/day | 0 | lower |'
- id: ORCH-M01
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-M01 | Idle capacity minutes: lane-slot minutes not executing while ready work exists, summed over hosts
    | ledger | ledger.idle_capacity_minutes_with_ready_work | slot-minutes/day | 60 | lower |'
- id: ORCH-M02
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-M02 | Ready-buffer deficit, time-weighted mean of `ix_fleet_ready_buffer_deficit` | ix-board-metric | prom.ready_buffer_deficit_mean
    | tickets | 0 | lower |'
- id: ORCH-M03
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-M03 | Time-to-action, p90: lane entering a non-WORKING class to its next WORKING run | ledger | ledger.time_to_action_p90
    | minutes | 15 | lower |'
- id: ORCH-M04
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-M04 | Order act latency, p90: `Delivered` to `Acted` for orchestrator orders | relay-receipts | relay.order_act_latency_p90
    | minutes | 5 | lower |'
- id: ORCH-M05
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-M05 | Drift rate: lane-minutes with a drift finding over WORKING lane-minutes | ledger | ledger.drift_lane_minutes_share
    | percent | 5 | lower |'
- id: ORCH-M06
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-M06 | Build throughput per host: completed builds and test runs per host-hour | ix-board-metric | prom.build_throughput_per_host_hour
    | builds/host-hour | recorded host level | higher |'
- id: ORCH-M07
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-M07 | Throttled share: paused plus admission-blocked seconds over wall seconds, per host | ix-board-metric
    | prom.host_throttled_share | percent | 5 | lower |'
- id: ORCH-M08
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-M08 | Gate queue wait, p90 | ix-board-metric | prom.gate_queue_wait_p90 | minutes | 10 | lower |'
```
