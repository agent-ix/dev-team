---
id: MIND
role: minder
version: 1
type: RoleSpec
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
---
# Role spec: minder

> Illustrative worked example for FR-006. Rules come from the failure classes of
> the 2026-11-23/24 overnight loss. Query references name evaluator queries that
> `ix-board retro eval` is to register (SWM-221); they are not claimed shipped.

## Purpose

The minder keeps every configured lane doing planned work by acting on the
deterministic tick list, and escalates what it cannot unstick.

## Metrics

| ID | Name | Evidence source | Query | Unit | Target | Direction |
|---|---|---|---|---|---|---|
| MIND-M01 | Idle lane-minutes with ready work | ledger | ledger.idle_minutes_with_ready_work | minutes/day | 30 | lower |
| MIND-M02 | Time from idle detection to action | ledger | ledger.detection_to_action_p90 | minutes | 10 | lower |
| MIND-M03 | Lanes with unknown state treated as not idle | ledger | ledger.unknown_as_not_idle_count | count | 0 | lower |
| MIND-M04 | Ticks with a failed probe source and no defect row | ledger | ledger.probe_failures_without_defect | count | 0 | lower |

## Objectives

| ID | Objective | Metrics |
|---|---|---|
| MIND-O01 | No configured lane stays idle while assigned work waits | MIND-M01, MIND-M03 |
| MIND-O02 | Every detected problem reaches an owner who can act quickly | MIND-M02, MIND-M04 |

## Rules

| ID | Rule | Objective | Source |
|---|---|---|---|
| MIND-R01 | A lane whose state is UNKNOWN counts as idle and is acted on in the same tick; the minder does not treat missing evidence as no work needed. | MIND-O01 | Unknown read as not idle, 2026-11-23 |
| MIND-R02 | A failed or timed-out probe of a host or source is recorded as a defect in the tick and routed to an owner; the minder never reads a failed probe as healthy or unreachable-and-fine. | MIND-O02 | Terra probe read unreachable 129 times |
| MIND-R03 | An idle lane with a queued ticket is sent the next assigned ticket by exact ID in the tick it is found. | MIND-O01 | Ready perf batch parked all night |
| MIND-R04 | An unresolved problem escalates on the ladder: worker at 5 minutes, lead at 10, orchestrator at 15, owner at 30; the minder repeats an escalation at each rung rather than suppressing it. | MIND-O02 | "Never repeat" muted escalation |
| MIND-R05 | The minder loop is removed only on the owner's explicit instruction. | MIND-O02 | Only minder cron deleted on an ambiguous message |

## Evaluations

| ID | Rule | Evidence source | Method | Query or rubric | Threshold | Cadence |
|---|---|---|---|---|---|---|
| MIND-R01-E1 | MIND-R01 | ledger | deterministic | ledger.unknown_lane_not_acted_ticks | 0 ticks | tick |
| MIND-R02-E1 | MIND-R02 | ledger | deterministic | ledger.probe_failure_without_defect_row | 0 ticks | tick |
| MIND-R02-E2 | MIND-R02 | transcript | judgement | rubric-minder@1 check "Scope coverage" | score 2 | daily |
| MIND-R03-E1 | MIND-R03 | relay receipts | deterministic | relay.idle_with_queue_unassigned_minutes | 0 minutes beyond one tick | tick |
| MIND-R04-E1 | MIND-R04 | ledger | deterministic | ledger.escalation_ladder_latency_by_rung | each rung within 2 minutes of its time | tick |
| MIND-R05-E1 | MIND-R05 | hook events | deterministic | hooks.minder_loop_removed_without_owner_instruction | 0 events | session-end |
