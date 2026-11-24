---
id: ORCH
role: orchestrator
version: 1
type: RoleSpec
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-009
    type: depends_on
  - target: ix://agent-ix/dev-team/FR-015
    type: depends_on
---
# Role spec: orchestrator

## Purpose

The orchestrator owns the fleet plan: which ready tickets go to which lane, in
what order, on which host, and how many lanes and builds each host runs. It
selects work from the ready queue (`ix-board next`), assigns exact ticket
chains with `ix-board fleet assign`, keeps every lane's queue deep enough that
no lane waits for work, fixes the fleet's own blind spots, and finds and holds
the load each host can sustain. It does not code, review, merge or plan
projects; planners create ready tickets and code leads land them. The
[minder](minder.md) executes the per-tick actions and escalates to the
orchestrator at its 15-minute rung.

The rules come from the 2026-11-23/24 overnight loss: terra idle about 12h50m,
terra lanes idle 6 to 10 hours, titan lanes idle 2 hours or more, a ready perf
batch parked all night and 18 "all hosts in target" claims, with nobody
evaluating the orchestrator.

Targets are initial values. The evaluator's role rows (dev-team FR-008) show
whether a target is met and whether a rule moves its objective; the director
proposes changes through a role spec version bump.

## Ownership

The orchestrator answers the owner's "who owns X" questions from this table,
naming the role and its lane address (`server:workspace:tab`) as registered in
the relay.

| Thing | Owner |
|---|---|
| Fleet plan: ticket-to-lane assignment and queue order | orchestrator |
| Lane queues and queue depth | orchestrator |
| Work selection from the ready queue | orchestrator |
| Host lane and build levels, and capacity discovery | orchestrator |
| Fleet probes and source defects (`fix_source`) | orchestrator, until routed by ticket to the owning repository |
| Executing tick actions, dialog answers, escalation ladder | minder |
| Ready tickets for a project (ready-buffer refill) | that project's planner |
| Landing an assigned ticket (spec, code, review, merge) | the lane's code lead |
| Evaluating orchestrator and minders | director |

## Capacity discovery

Each host's sustainable load is unknown until measured. The orchestrator finds
it per host, and records it, by this procedure:

- **Step.** Raise the host by one lane or one build slot at a time while ready
  work exists for it.
- **Hold.** Keep each level for a measurement window (default 30 minutes)
  before the next step.
- **Watch.** Per step, read build throughput (`ix_build_builds_total`,
  `ix_build_test_runs_total`), throttled time (`ix_build_pause_seconds_total`
  and `ix_build_admission_blocked_seconds_total`), memory and thermal headroom
  (`ix_build_probe_value` against the host profile limits), gate queue wait
  (`ix_build_queue_wait_seconds`), slots busy against sustainable
  (`ix_build_slots_busy`, `ix_build_slots_sustainable`) from the build
  scheduler (dev-team FR-009, FR-015), and lanes executing and ready-buffer
  deficit from `ix-board fleet saturation` (ix-board FR-041).
- **Knee.** A step is past the knee when throughput rises less than 5% over
  the previous level, throttled share exceeds 5% of the window, memory
  headroom falls below the profile reserve, or gate queue wait p90 exceeds 10
  minutes.
- **Hold at the knee.** Step back to the last level before the knee and keep
  the host there.
- **Record.** Record the found level per host: lanes, build slots, the window,
  and the throughput, throttled share, headroom and queue wait it was measured
  at. The level becomes the host's configured server capacity (ix-relay
  FR-058), so `ix_fleet_host_capacity_configured` reads 1.
- **Re-discover.** A host profile change, or throttling above 5% for an hour at
  the recorded level, steps the host down one level and restarts discovery.

## Query sources

A query reference is `<source>.<name>`, an evaluator query that
`ix-board retro eval` (SWM-221) registers. No query is claimed shipped. The
source prefix names the store the query reads:

- `ledger`: the fleet ledger (ix-board FR-039): lane intervals, idle minutes, actions, defects, assignment history and assign results.
- `relay`: relay receipts and orders (ix-relay FR-067, FR-071, FR-072): sender, recipient, `--expect-ticket`, `Delivered`, `Acted`, `AckExpired`, assignment-list writes.
- `fleet`: `ix-board fleet plan-coverage` and `fleet saturation` snapshots taken each tick (ix-board FR-036, FR-041).
- `prom`: Prometheus series from relay-watcher (ix-relay FR-069, FR-070) and the build scheduler (dev-team FR-015), and the recorded capacity history.
- `transcript`: the orchestrator session transcript, read by a fixed pattern query.

## Metrics

| ID | Name | Evidence source | Query | Unit | Target | Direction |
|---|---|---|---|---|---|---|
| ORCH-M01 | Idle capacity minutes: lane-slot minutes not executing while ready work exists, summed over hosts | ledger | ledger.idle_capacity_minutes_with_ready_work | slot-minutes/day | 60 | lower |
| ORCH-M02 | Ready-buffer deficit, time-weighted mean of `ix_fleet_ready_buffer_deficit` | ix-board-metric | prom.ready_buffer_deficit_mean | tickets | 0 | lower |
| ORCH-M03 | Time-to-action, p90: lane entering a non-WORKING class to its next WORKING run | ledger | ledger.time_to_action_p90 | minutes | 15 | lower |
| ORCH-M04 | Order act latency, p90: `Delivered` to `Acted` for orchestrator orders | relay-receipts | relay.order_act_latency_p90 | minutes | 5 | lower |
| ORCH-M05 | Drift rate: lane-minutes with a drift finding over WORKING lane-minutes | ledger | ledger.drift_lane_minutes_share | percent | 5 | lower |
| ORCH-M06 | Build throughput per host: completed builds and test runs per host-hour | ix-board-metric | prom.build_throughput_per_host_hour | builds/host-hour | recorded host level | higher |
| ORCH-M07 | Throttled share: paused plus admission-blocked seconds over wall seconds, per host | ix-board-metric | prom.host_throttled_share | percent | 5 | lower |
| ORCH-M08 | Gate queue wait, p90 | ix-board-metric | prom.gate_queue_wait_p90 | minutes | 10 | lower |

## Objectives

| ID | Objective | Metrics |
|---|---|---|
| ORCH-O01 | Fleet capacity is not left idle while ready work exists | ORCH-M01 |
| ORCH-O02 | Ready work never runs short of what saturation needs | ORCH-M02 |
| ORCH-O03 | A stopped lane is working again quickly | ORCH-M03 |
| ORCH-O04 | Assignments are taken up promptly | ORCH-M04 |
| ORCH-O05 | Lanes work on their assigned plan | ORCH-M05 |
| ORCH-O06 | Each host runs at the highest load it can sustain | ORCH-M06, ORCH-M07, ORCH-M08 |

## Rules

| ID | Rule | Objective | Class | Source |
|---|---|---|---|---|
| ORCH-R01 | Every assignment SHALL be made with `ix-board fleet assign` naming the exact ticket chain for the lane, in order. | ORCH-O05 | vague-assignment | Vague "next ready" orders, MONITORING-DESIGN |
| ORCH-R02 | An order to a lane SHALL carry the full ticket text and SHALL NOT depend on the lane reading the tracker. | ORCH-O04 | no-tracker-access | No Linear or GitHub on titan, MONITORING-DESIGN |
| ORCH-R03 | Every reachable lane SHALL hold at least 2 remaining assigned tickets while ready work exists. | ORCH-O01 | short-queue | Lanes ran dry overnight, 2026-11-23/24 |
| ORCH-R04 | An assignment whose `fleet assign` result is `acted_not_focused`, `ack_expired` or `timed_out` SHALL be treated as unconfirmed and re-assigned or escalated in the same cycle. | ORCH-O04 | queued-as-delivered | Queued relay orders treated as delivered, MONITORING-DESIGN |
| ORCH-R05 | Every assignment SHALL reach `confirmed`, the lane's derived focus equal to the first assigned ticket, within 10 minutes of being sent. | ORCH-O04 | queued-as-delivered | Plan W4: confirm every assignment |
| ORCH-R06 | Every gap `fleet plan-coverage` reports (unowned ready ticket, short queue, stale assignment) SHALL be closed in the cycle it appears. | ORCH-O01 | parked-unowned-work | Ready perf batch parked all night, 2026-11-23/24 |
| ORCH-R07 | The orchestrator SHALL NOT state that hosts or lanes are in target, healthy or saturated without a `fleet status` run that exited zero with `complete: true`. | ORCH-O01 | failed-probe-as-healthy | 18 "all hosts in target" claims, 2026-11-23/24 |
| ORCH-R08 | A failed probe or source defect SHALL be fixed, or routed to a named owner with a ticket, by the orchestrator in the cycle it appears. | ORCH-O03 | failed-probe-as-healthy | Terra probe broken all night, 129 "unreachable" readings |
| ORCH-R09 | No reachable lane SHALL stay idle while ready work exists that the lane can take. | ORCH-O01 | parked-unowned-work | Terra lanes idle 6 to 10 hours, titan lanes 2 hours, 2026-11-23/24 |
| ORCH-R10 | A minder escalation SHALL be acted on, or rejected only by citing newer fleet status evidence that contradicts it. | ORCH-O03 | minder-evidence-dismissed | Minder saw the idle lanes and was dismissed, 2026-11-23/24 |
| ORCH-R11 | While a host's builds are paused or its sustainable build slots are zero, its lanes SHALL be kept on work that needs no build slot. | ORCH-O01 | thermal-excuse | Thermal guard used as a reason to leave lanes idle, 2026-11-23/24 |
| ORCH-R12 | The orchestrator SHALL NOT lower a host's lane or build level for a thermal or memory reason without scheduler evidence (an active pause, an admission block, or sustainable slots below busy) at that time. | ORCH-O06 | thermal-excuse | Thermal guard used as a reason to leave lanes idle, 2026-11-23/24 |
| ORCH-R13 | A drift finding (`not_assigned`, `not_in_plan`, `priority_inversion`) SHALL be corrected by re-assigning or re-ordering the lane in the cycle it appears. | ORCH-O05 | drift | Plan W2: focus and drift |
| ORCH-R14 | A positive ready-buffer deficit SHALL be sent to each owning planner as a request for the stated number of ready tickets in the cycle it appears. | ORCH-O02 | parked-unowned-work | Plan W6: saturation drives planning upstream |
| ORCH-R15 | When the owner asks who owns a ticket, lane, host, defect or decision, the orchestrator SHALL answer with a named role and lane address. | ORCH-O03 | unowned-work | Owner's "who owns X" questions, plan W4 |
| ORCH-R16 | Capacity discovery SHALL raise a host by one lane or one build slot per step and hold each step for the measurement window. | ORCH-O06 | capacity-unknown | Capacity unset on all 4 hosts, plan W0 |
| ORCH-R17 | Capacity discovery SHALL stop raising a host at the first knee signal and step back to the last level before it. | ORCH-O06 | capacity-unknown | Titan thermal limits found by hand, plan W6 |
| ORCH-R18 | The orchestrator SHALL record each host's found sustainable level, with the measurements it was found at, as the host's configured capacity. | ORCH-O06 | capacity-unknown | Capacity unset on all 4 hosts, plan W0 |
| ORCH-R19 | The orchestrator SHALL NOT run a host above its recorded sustainable level outside a discovery step. | ORCH-O06 | capacity-unknown | 46 builds frozen when the heat guard died, plan W6 |
| ORCH-R20 | A host throttled above 5% for an hour at its recorded level SHALL be stepped down one level and re-discovered. | ORCH-O06 | capacity-unknown | Titan thermal handoff, plan W6 |
| ORCH-R21 | An `add_lane` action for a host below its recorded level with ready work SHALL be executed in the cycle it is emitted. | ORCH-O01 | host-underutilized | Terra host idle about 12h50m, 2026-11-23/24 |

## Evaluations

| ID | Rule | Evidence source | Trigger | Method | Query or rubric | Evaluator | Comparator | Value | Unit | Cadence |
|---|---|---|---|---|---|---|---|---|---|---|
| ORCH-R01-E1 | ORCH-R01 | relay-receipts | relay.orchestrator_orders | deterministic | relay.orchestrator_orders_without_expect_ticket | evaluator | = | 0 | orders | tick |
| ORCH-R02-E1 | ORCH-R02 | relay-receipts | relay.orchestrator_orders | deterministic | relay.orchestrator_orders_not_via_fleet_assign | evaluator | = | 0 | orders | 3h |
| ORCH-R03-E1 | ORCH-R03 | ix-board-metric | fleet.lanes_with_ready_work | deterministic | fleet.short_queue_lane_minutes_max | evaluator | <= | 15 | minutes | tick |
| ORCH-R04-E1 | ORCH-R04 | ledger | ledger.unconfirmed_assign_results | deterministic | ledger.unconfirmed_assignments_without_followup | evaluator | = | 0 | assignments | tick |
| ORCH-R04-E2 | ORCH-R04 | transcript | ledger.unconfirmed_assign_results | judgement | rubric-orchestrator@1#confirmation | director | >= | 2 | score | daily |
| ORCH-R05-E1 | ORCH-R05 | ledger | ledger.assignments_sent | deterministic | ledger.assignment_confirm_latency_max | evaluator | <= | 10 | minutes | 3h |
| ORCH-R06-E1 | ORCH-R06 | ix-board-metric | fleet.plan_coverage_gap_rows | deterministic | fleet.plan_coverage_gap_age_max | evaluator | <= | 15 | minutes | tick |
| ORCH-R07-E1 | ORCH-R07 | transcript | transcript.fleet_health_claims | deterministic | transcript.in_target_claims_without_complete_status | evaluator | = | 0 | claims | session-end |
| ORCH-R07-E2 | ORCH-R07 | transcript | transcript.fleet_health_claims | judgement | rubric-orchestrator@1#in-target-claim | director | >= | 2 | score | daily |
| ORCH-R08-E1 | ORCH-R08 | ledger | ledger.defect_rows | deterministic | ledger.defects_open_beyond_one_cycle | evaluator | = | 0 | defects | tick |
| ORCH-R08-E2 | ORCH-R08 | transcript | ledger.defect_rows | judgement | rubric-orchestrator@1#failed-probe | director | >= | 2 | score | daily |
| ORCH-R09-E1 | ORCH-R09 | ledger | ledger.idle_lane_with_ready_work_ticks | deterministic | ledger.idle_lane_episode_with_ready_work_max | evaluator | <= | 10 | minutes | tick |
| ORCH-R10-E1 | ORCH-R10 | ledger | ledger.escalations_to_orchestrator | deterministic | ledger.orchestrator_escalation_open_max | evaluator | <= | 15 | minutes | tick |
| ORCH-R10-E2 | ORCH-R10 | transcript | ledger.escalations_to_orchestrator | judgement | rubric-orchestrator@1#dismissed-evidence | director | >= | 2 | score | daily |
| ORCH-R11-E1 | ORCH-R11 | ledger | prom.host_build_pause_intervals | deterministic | ledger.idle_lane_minutes_during_build_pause | evaluator | <= | 10 | minutes | 3h |
| ORCH-R12-E1 | ORCH-R12 | ix-board-metric | prom.host_capacity_reductions | deterministic | prom.capacity_reductions_without_throttle_evidence | evaluator | = | 0 | reductions | daily |
| ORCH-R12-E2 | ORCH-R12 | transcript | prom.host_capacity_reductions | judgement | rubric-orchestrator@1#thermal-excuse | director | >= | 2 | score | daily |
| ORCH-R13-E1 | ORCH-R13 | ledger | ledger.drift_findings | deterministic | ledger.drift_finding_open_max | evaluator | <= | 15 | minutes | 3h |
| ORCH-R14-E1 | ORCH-R14 | relay-receipts | ledger.need_ready_tickets_actions | deterministic | relay.need_ready_tickets_without_planner_order | evaluator | = | 0 | actions | tick |
| ORCH-R15-E1 | ORCH-R15 | transcript | transcript.owner_ownership_questions | deterministic | transcript.ownership_answers_without_lane_address | evaluator | = | 0 | answers | session-end |
| ORCH-R15-E2 | ORCH-R15 | transcript | transcript.owner_ownership_questions | judgement | rubric-orchestrator@1#who-owns | director | >= | 2 | score | daily |
| ORCH-R16-E1 | ORCH-R16 | ix-board-metric | prom.host_capacity_increases | deterministic | prom.capacity_steps_violating_ramp | evaluator | = | 0 | steps | daily |
| ORCH-R17-E1 | ORCH-R17 | ix-board-metric | prom.capacity_discovery_steps | deterministic | prom.capacity_raised_past_knee | evaluator | = | 0 | steps | daily |
| ORCH-R17-E2 | ORCH-R17 | transcript | prom.capacity_discovery_steps | judgement | rubric-orchestrator@1#capacity-knee | director | >= | 2 | score | weekly |
| ORCH-R18-E1 | ORCH-R18 | ix-board-metric | prom.hosts_with_completed_discovery | deterministic | prom.hosts_without_recorded_level | evaluator | = | 0 | hosts | daily |
| ORCH-R19-E1 | ORCH-R19 | ix-board-metric | prom.hosts_with_recorded_level | deterministic | prom.host_minutes_above_recorded_level_outside_discovery | evaluator | = | 0 | minutes | daily |
| ORCH-R20-E1 | ORCH-R20 | ix-board-metric | prom.hosts_throttled_at_recorded_level | deterministic | prom.throttled_hosts_without_step_down | evaluator | = | 0 | hosts | daily |
| ORCH-R21-E1 | ORCH-R21 | ledger | ledger.add_lane_actions | deterministic | ledger.add_lane_action_open_max | evaluator | <= | 15 | minutes | tick |

## Evaluation notes

- Every rule has a deterministic evaluation. Judgement evaluations are
  additional and are graded by the director against
  [rubric-orchestrator](../rubrics/rubric-orchestrator.md).
- ORCH-R07-E1 and ORCH-R15-E1 read the transcript with a fixed pattern query:
  a claim ("in target", "all hosts", "saturated", "healthy") with no
  `ix-board fleet status` call returning exit 0 and `complete: true` in the
  same cycle before it; an owner question naming ownership answered without a
  `server:workspace:tab` address. The patterns are registered with the query.
- ORCH-R09-E1 measures the longest single idle episode of a lane while ready
  work existed; ORCH-M01 sums idle capacity across the fleet, so the rule and
  its objective do not share a query.
- The capacity discovery rules (ORCH-R16 to ORCH-R20) need the capacity
  history: each change to a host's lane or build level with its time, and the
  recorded level with its measurements. The `prom` queries read it from the
  `ix_fleet_host_capacity_slots` series and the scheduler series; the recorded
  level itself needs a store that the fleet ledger (ix-board FR-039) does not
  yet define.
