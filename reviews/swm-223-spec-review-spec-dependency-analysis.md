---
id: SR-031
title: "dependency review of SWM-222/223 role-spec evidence enablers"
type: SpecReview
analysis: dependency
scope: "agent-ix/dev-team; SWM-222, SWM-223; spec/roles/**, spec/rubrics/**, spec/functional/FR-006, spec/spec.md, skills/team-retro diff origin/main...96d8047 (PR dev-team#32)"
review_set: subset
date: 2026-11-24
---

# dependency review of SWM-222/223 role-spec evidence enablers

## Summary

Tickets: SWM-222 (orchestrator role spec), SWM-223 (minder role spec). Frozen PR: dev-team#32 at 96d8047. Evidence contracts read from origin/main: ix-board FR-034..043, ix-relay FR-058 and FR-067..072, dev-team FR-006..010 and FR-015. Validation re-run with quire 0.52.1 against the spec-artifacts-process origin/main export (80d25b6): validate, --strict, --okf and coverage exit 0.

## Verdict

**PASS with findings**. Enablement is separable from the role specs, and the filed tickets cover the module release (SWM-253), the capacity ledger (SWM-252) and the evaluator and transcript kind (SWM-221). Seven evidence producers are missing tickets, and the cross-repository dependencies are prose only.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | The role specs depend on evidence enablers that no ticket covers: plan-coverage snapshot persistence (ORCH-R03-E1, R06-E1), escalation and rung records (MIND-R04-E1, R05-E1, ORCH-R10-E1), the minder's acts on undetermined lanes (MIND-R01-E1), drift persistence (ORCH-M05, R13-E1), `fleet assign` results in the ledger (ORCH-R04-E1, R05-E1), `--expect-ticket` on `fleet assign` orders (ORCH-R01-E1), and an order-to-assign join key (ORCH-R02-E1). The dialog answer log is only an AC of SWM-225. Only SWM-252 (capacity), SWM-221 (evaluator, transcript) and SWM-253 (module) are filed. These need ix-board and ix-relay tickets before SWM-221 can bind the queries. | spec/roles/orchestrator.md:6-12 |
| FND-002 | low | The cross-repository contracts the specs read from (ix-board FR-034 to FR-041, ix-relay FR-058 and FR-067 to FR-072) appear only in prose. MIND declares no `depends_on` at all, not even on its tick source, ix-board FR-038, and ORCH declares only dev-team FR-009 and FR-015. A change to those contracts therefore shows no blast radius on the role specs. Declare them as `depends_on` relationships where the module allows cross-repository targets. | spec/roles/minder.md:6-8 |

## Examined Scope

```yaml
scope:
- id: ORCH
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'relationships: FR-006 satisfies; FR-009 depends_on; FR-015 depends_on'
- id: MIND
  path: spec/roles/minder.md
  role: examined
  excerpt: 'relationships: FR-006 satisfies'
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
```

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | - |
| FND-002 | fixed | - |
