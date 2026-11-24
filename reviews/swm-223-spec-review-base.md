---
id: SR-028
title: "base review of SWM-222/223 orchestrator and minder role specs"
type: SpecReview
analysis: base
scope: "agent-ix/dev-team; SWM-222, SWM-223; spec/roles/**, spec/rubrics/**, spec/functional/FR-006, spec/spec.md, skills/team-retro diff origin/main...96d8047 (PR dev-team#32)"
review_set: subset
date: 2026-11-24
---

# base review of SWM-222/223 orchestrator and minder role specs

## Summary

Tickets: SWM-222 (orchestrator role spec), SWM-223 (minder role spec). Frozen PR: dev-team#32 at 96d8047. Evidence contracts read from origin/main: ix-board FR-034..043, ix-relay FR-058 and FR-067..072, dev-team FR-006..010 and FR-015. Validation re-run with quire 0.52.1 against the spec-artifacts-process origin/main export (80d25b6): validate, --strict, --okf and coverage exit 0.

## Verdict

**FAIL**. The format holds. Every rule has at least one evaluation, every objective has a metric, no metric query equals an evaluation query, IDs are unique, and quire validate, --strict, --okf and coverage all exit 0 against spec-artifacts-process origin/main 80d25b6 (46 role-evaluation targets, 11 rubric references resolved). The nine failure classes each map to rules. Four kinds of defect block merge. The minder's ladder contradicts its own tick-0 rules. One threshold cannot be met at the default tick. 'Cycle' is undefined, so orchestrator rules are not evaluator-stable. ORCH-R01, R08 and MIND-R03 are unachievable or mis-measured as written against the ix-board and ix-relay contracts.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | MIND-R04's ladder (worker at 5, lead at 10, orchestrator at 15, owner at 30 minutes) contradicts MIND-R11 and ix-board FR-038, which send `escalate_block` to the lead in the tick a block is found (minute 0), and MIND-R03, which pushes the worker at minute 0. 'Unresolved problem' and the ladder's start time are undefined, so two evaluators disagree on whether a lead message at minute 2 passes or breaks the ladder. Define the problem set (which tick action kinds), the clock start (action `emitted_at`), and state that a tick action's first send is rung 1. | spec/roles/minder.md:66 |
| FND-002 | high | MIND-R04-E1 requires rung latency <= 2 minutes, but the minder only acts at ticks and the ix-board FR-039 default tick interval is 5 minutes; a rung that falls due between ticks is sent up to 5 minutes late, so the evaluation fails by construction at the default cadence. Set the threshold to one tick interval (or state the tick interval the threshold assumes). | spec/roles/minder.md:86 |
| FND-003 | medium | 'Cycle' is undefined for the orchestrator. ORCH-R04, R06, R08, R13, R14 and R21 require action 'in the cycle it appears', and ORCH-R08-E1 counts defects 'open beyond one cycle', but no orchestrator cycle length or start is stated (the minder has a tick, the orchestrator has none). Two evaluators cannot agree on a pass; define the cycle (for example the fleet tick interval) or restate each rule in minutes. | spec/roles/orchestrator.md:130 |
| FND-004 | medium | ORCH-R08 allows a defect to be 'fixed, or routed to a named owner with a ticket', but ORCH-R08-E1 counts defects_open_beyond_one_cycle = 0. A correctly routed defect that needs real repair work (the terra probe) stays open and fails every tick. The evaluation must count defects neither fixed nor routed, and routing (owner plus ticket) has no producer in the ledger (ix-board FR-039 `defect` table). | spec/roles/orchestrator.md:160 |
| FND-005 | medium | ORCH-R01-E1 counts orchestrator orders without `--expect-ticket`, but ix-board FR-035 `fleet assign` never sets `--expect-ticket` (ix-relay FR-071 makes it optional), so every compliant assignment fails. The evaluations are also crossed: R01 ('made with fleet assign') is what ORCH-R02-E1 measures (orders not via fleet assign), and nothing checks 'exact chain, in order'. Ticket FR-035 to set `--expect-ticket` to the first ticket, and pair R01 with a via-fleet-assign query. | spec/roles/orchestrator.md:151 |
| FND-006 | medium | MIND-R03 has the minder push using the `push_next_ticket` assign command, but `fleet assign` writes through ix-relay FR-072, which refuses callers without the orchestrator role (ix-board FR-035 step 4, FR-035-AC-8), and a later assign replaces the whole list (FR-035 step 7). As written the minder's push is either refused or truncates the lane's queue, breaking ORCH-R03 (queue >= 2). State whether the minder holds the orchestrator relay role and that the push re-sends the remaining list, or make the push a plain order with `--expect-ticket`. | spec/roles/minder.md:65 |
| FND-007 | medium | MIND-R12 is judgement-only because 'no evidence source records' answers sent outside the relay, but the spec already uses a deterministic transcript pattern query (MIND-R14-E1). The same kind works here: in the minder transcript, any pane-input command (herdr send/keys, answer text) aimed at a lane while an `escalate_block` action for that lane is open in the ledger is a violation. The cited upgrade path names SWM-226, which is the standing-order allow-rule and has no answer log; the answer log is only an AC of SWM-225. Add the transcript evaluation now, or name a ticket that produces the answer log. | spec/roles/minder.md:96 |
| FND-008 | medium | MIND-R10 joins two obligations, answering a matched dialog in the tick and logging the answer with the order id; MIND-R10-E1 checks only latency, so the logging half is unevaluated (and no producer of the answer log is specified). Split the rule and give the log half its own evaluation, per FR-006 atomic rules. | spec/roles/minder.md:72 |
| FND-009 | medium | Two ix-board FR-038 tick action kinds have no owning rule: `escalate_stuck` (STUCK or LOOP lane) and `escalate_stale_pr` both target the lead, so MIND-R08 ('every lane-targeted tick action') excludes them, MIND-R11 covers only `escalate_block`, and no ORCH rule covers them. A STUCK or LOOP lane can therefore be left unescalated with every rule passing. Extend MIND-R08 to every tick action addressed to a lane or a lead. | spec/roles/minder.md:70 |
| FND-010 | medium | MIND-R09-E2 cites rubric-minder@2#confirmation, which grades whether an order was counted as taken up only on a focus match; MIND-R09 is about re-sending or escalating an expired order, which is rubric-minder@2#overdue-order. Likewise MIND-R12-E1's #login-blocker scores R11's escalation timing as well as R12's no-answer, so a low score does not say which rule broke. Cite the matching check, or split the check. | spec/roles/minder.md:93 |
| FND-011 | medium | Judged per brief item 6: merging the role spec while team-minder still says 'never repeat' and 'UNKNOWN: no nudge or inferred idle' (skills/team-minder/SKILL.md:90, :132) is acceptable on its own, because a spec does not change runtime behaviour. This PR also ships team-retro 0.2.1, which scores the minder with rubric-minder@2 (undetermined-as-idle, escalation-ladder) right away. A minder following its own skill then scores 0 and gets retro actions that contradict that skill. Hold the team-retro 0.2.1 release, or make SWM-225 block it, or mark those two checks n/a until team-minder cites MIND version 3. | skills/team-retro/SKILL.md:63 |
| FND-012 | medium | ORCH-M04 measures order act latency (`Delivered` to `Acted`), but this spec says that `Acted` is not uptake (MIND-R09 note, ORCH-R05), and ix-relay FR-067 records `Acted` on the recipient's next tool event. A lane that is already WORKING acts within seconds whatever the order says, so ORCH-O04 ('assignments are taken up promptly') looks met while assignments are ignored. Measure time from send to focus match (confirmation) per assignment as the objective, with a query distinct from ORCH-R05-E1's max. | spec/roles/orchestrator.md:104 |
| FND-013 | low | MIND-M04 (unwatched minutes, the tick gap) and its objective MIND-O04 ('the fleet is never unwatched') measure whether the minder ran its loop, which is MIND-R06/R07 compliance, not a throughput outcome as FR-006 requires of objectives. It is fine as an alert, but as an objective it cannot show whether a rule moves throughput. | spec/roles/minder.md:48 |
| FND-014 | low | ORCH-M06's target is 'recorded host level', which is not numeric and is in a different unit (lanes and build slots) from the metric (builds per host-hour). State the target as the throughput recorded at the found level (ORCH-R18 records it), with a tolerance. | spec/roles/orchestrator.md:106 |
| FND-015 | low | MIND-R07 joins 'start from a committed tick' and 'SHALL NOT substitute own probes'. MIND-R07-E1 checks only the first; the second has no evaluation, and the hook events of ix-relay FR-068 carry tool names only, so it cannot be checked from hooks. | spec/roles/minder.md:69 |

## Examined Scope

```yaml
scope:
- id: MIND-R01
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R01 | A lane whose state cannot be determined (UNKNOWN from a legacy source, or a fleet status row carrying
    a source defect) SHALL be treated as idle and acted on in the same tick. | MIND-O01 | unknown-as-not-idle | UNKNOWN read
    as not idle, 2026-11-23 |'
- id: MIND-R02
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R02 | A failed or timed-out probe of a host or source SHALL be recorded as a defect in the tick and routed
    to an owner. | MIND-O02 | failed-probe-as-healthy | Terra probe read "unreachable" 129 times, 2026-11-23/24 |'
- id: MIND-R03
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R03 | An idle lane with a remaining assigned ticket SHALL be sent that ticket by exact ID, using the `push_next_ticket`
    action''s assign command, in the tick it is found. | MIND-O01 | parked-ready-work | Ready perf batch parked all night,
    2026-11-23/24 |'
- id: MIND-R04
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R04 | An unresolved problem SHALL escalate to the worker at 5 minutes, the lead at 10, the orchestrator
    at 15 and the owner at 30. | MIND-O02 | escalation-muted | "Never repeat" muted escalation, team-minder skill |'
- id: MIND-R05
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R05 | The minder SHALL send an escalation at each rung reached and SHALL NOT suppress one because an earlier
    message was sent. | MIND-O02 | escalation-muted | "Never repeat" muted escalation, team-minder skill |'
- id: MIND-R06
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R06 | The minder loop SHALL be removed only on the owner''s explicit instruction. | MIND-O04 | loop-removed
    | IXD''s only minder cron deleted on an ambiguous message, 2026-11-23 |'
- id: MIND-R07
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R07 | Each minder tick SHALL start from a committed `ix-board fleet tick` run and SHALL NOT substitute
    the minder''s own probes for it. | MIND-O04 | weak-evidence-as-work | Load average, pane titles and own controls counted
    as work, MONITORING-DESIGN |'
- id: MIND-R08
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R08 | The minder SHALL execute every lane-targeted tick action before its `due_by` and SHALL NOT skip one
    because its own reading shows the lane working. | MIND-O02 | weak-evidence-as-work | herdr "working" alone read as work,
    MONITORING-DESIGN |'
- id: MIND-R09
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R09 | An order past its acknowledgement deadline without a focus match SHALL be re-sent or escalated in
    the tick it expires. | MIND-O02 | queued-as-delivered | Queued relay orders treated as delivered, MONITORING-DESIGN |'
- id: MIND-R10
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R10 | A lane in BLOCKED(dialog) whose dialog matches a standing order SHALL be answered per that order
    in the tick it is found, and the answer logged with the order id. | MIND-O03 | dialog-not-cleared | Lanes blocked on queued
    questions and dialogs, MONITORING-DESIGN |'
- id: MIND-R11
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R11 | A lane in BLOCKED(login), BLOCKED(usage_limit), BLOCKED(question), or BLOCKED(dialog) with no matching
    standing order SHALL be escalated to the lane''s lead in the tick it is found. | MIND-O03 | dialog-not-cleared | Lanes
    blocked on dialogs, MONITORING-DESIGN |'
- id: MIND-R12
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R12 | The minder SHALL NOT answer a dialog, login or permission prompt that no standing order covers. |
    MIND-O03 | unauthorized-answer | Plan decision: login screens and usage limits escalate |'
- id: MIND-R13
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R13 | Every order the minder sends to a lane SHALL name the exact ticket it expects the lane to take up.
    | MIND-O01 | vague-assignment | Vague "next ready" orders, MONITORING-DESIGN |'
- id: MIND-R14
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R14 | Every escalation SHALL carry the ledger action id and the fleet status evidence it rests on. | MIND-O02
    | minder-evidence-dismissed | Minder saw the idle lanes and was dismissed, 2026-11-23/24 |'
- id: ORCH-R01
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R01 | Every assignment SHALL be made with `ix-board fleet assign` naming the exact ticket chain for the
    lane, in order. | ORCH-O05 | vague-assignment | Vague "next ready" orders, MONITORING-DESIGN |'
- id: ORCH-R02
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R02 | An order to a lane SHALL carry the full ticket text and SHALL NOT depend on the lane reading the
    tracker. | ORCH-O04 | no-tracker-access | No Linear or GitHub on titan, MONITORING-DESIGN |'
- id: ORCH-R03
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R03 | Every reachable lane SHALL hold at least 2 remaining assigned tickets while ready work exists. |
    ORCH-O01 | short-queue | Lanes ran dry overnight, 2026-11-23/24 |'
- id: ORCH-R04
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R04 | An assignment whose `fleet assign` result is `acted_not_focused`, `ack_expired` or `timed_out` SHALL
    be treated as unconfirmed and re-assigned or escalated in the same cycle. | ORCH-O04 | queued-as-delivered | Queued relay
    orders treated as delivered, MONITORING-DESIGN |'
- id: ORCH-R05
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R05 | Every assignment SHALL reach `confirmed`, the lane''s derived focus equal to the first assigned ticket,
    within 10 minutes of being sent. | ORCH-O04 | queued-as-delivered | Plan W4: confirm every assignment |'
- id: ORCH-R06
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R06 | Every gap `fleet plan-coverage` reports (unowned ready ticket, short queue, stale assignment) SHALL
    be closed in the cycle it appears. | ORCH-O01 | parked-unowned-work | Ready perf batch parked all night, 2026-11-23/24
    |'
- id: ORCH-R07
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R07 | The orchestrator SHALL NOT state that hosts or lanes are in target, healthy or saturated without
    a `fleet status` run that exited zero with `complete: true`. | ORCH-O01 | failed-probe-as-healthy | 18 "all hosts in target"
    claims, 2026-11-23/24 |'
- id: ORCH-R08
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R08 | A failed probe or source defect SHALL be fixed, or routed to a named owner with a ticket, by the
    orchestrator in the cycle it appears. | ORCH-O03 | failed-probe-as-healthy | Terra probe broken all night, 129 "unreachable"
    readings |'
- id: ORCH-R09
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R09 | No reachable lane SHALL stay idle while ready work exists that the lane can take. | ORCH-O01 | parked-unowned-work
    | Terra lanes idle 6 to 10 hours, titan lanes 2 hours, 2026-11-23/24 |'
- id: ORCH-R10
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R10 | A minder escalation SHALL be acted on, or rejected only by citing newer fleet status evidence that
    contradicts it. | ORCH-O03 | minder-evidence-dismissed | Minder saw the idle lanes and was dismissed, 2026-11-23/24 |'
- id: ORCH-R11
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R11 | While a host''s builds are paused or its sustainable build slots are zero, its lanes SHALL be kept
    on work that needs no build slot. | ORCH-O01 | thermal-excuse | Thermal guard used as a reason to leave lanes idle, 2026-11-23/24
    |'
- id: ORCH-R12
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R12 | The orchestrator SHALL NOT lower a host''s lane or build level for a thermal or memory reason without
    scheduler evidence (an active pause, an admission block, or sustainable slots below busy) at that time. | ORCH-O06 | thermal-excuse
    | Thermal guard used as a reason to leave lanes idle, 2026-11-23/24 |'
- id: ORCH-R13
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R13 | A drift finding (`not_assigned`, `not_in_plan`, `priority_inversion`) SHALL be corrected by re-assigning
    or re-ordering the lane in the cycle it appears. | ORCH-O05 | drift | Plan W2: focus and drift |'
- id: ORCH-R14
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R14 | A positive ready-buffer deficit SHALL be sent to each owning planner as a request for the stated
    number of ready tickets in the cycle it appears. | ORCH-O02 | parked-unowned-work | Plan W6: saturation drives planning
    upstream |'
- id: ORCH-R15
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R15 | When the owner asks who owns a ticket, lane, host, defect or decision, the orchestrator SHALL answer
    with a named role and lane address. | ORCH-O03 | unowned-work | Owner''s "who owns X" questions, plan W4 |'
- id: ORCH-R16
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R16 | Capacity discovery SHALL raise a host by one lane or one build slot per step and hold each step for
    the measurement window. | ORCH-O06 | capacity-unknown | Capacity unset on all 4 hosts, plan W0 |'
- id: ORCH-R17
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R17 | Capacity discovery SHALL stop raising a host at the first knee signal and step back to the last level
    before it. | ORCH-O06 | capacity-unknown | Titan thermal limits found by hand, plan W6 |'
- id: ORCH-R18
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R18 | The orchestrator SHALL record each host''s found sustainable level, with the measurements it was
    found at, as the host''s configured capacity. | ORCH-O06 | capacity-unknown | Capacity unset on all 4 hosts, plan W0 |'
- id: ORCH-R19
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R19 | The orchestrator SHALL NOT run a host above its recorded sustainable level outside a discovery step.
    | ORCH-O06 | capacity-unknown | 46 builds frozen when the heat guard died, plan W6 |'
- id: ORCH-R20
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R20 | A host throttled above 5% for an hour at its recorded level SHALL be stepped down one level and re-discovered.
    | ORCH-O06 | capacity-unknown | Titan thermal handoff, plan W6 |'
- id: ORCH-R21
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R21 | An `add_lane` action for a host below its recorded level with ready work SHALL be executed in the
    cycle it is emitted. | ORCH-O01 | host-underutilized | Terra host idle about 12h50m, 2026-11-23/24 |'
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
- id: rubric-minder@2#loop-alive
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#loop-alive | The minder loop ran every scheduled tick. Evidence: committed fleet ticks in the
    ledger, the tick metric, scheduler entries. | 2: every tick committed; 1: a late or missed tick has a recorded remedy;
    0: the loop stopped or was removed without the owner''s instruction |'
- id: rubric-minder@2#scope-coverage
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#scope-coverage | Every registered lane and host in `ix-board fleet status` was considered in
    the tick. Evidence: status rows, defect rows, the tick''s actions. | 2: every lane and defect accounted for; 1: a gap
    was routed to an owner; 0: a missing lane or host was treated as healthy |'
- id: rubric-minder@2#liveness
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#liveness | Lane state was taken from `fleet tick` and `fleet status`, not from the minder''s
    own reading. Evidence: tick actions and the minder''s sends. | 2: every lane-targeted action executed as emitted; 1: one
    action skipped, then corrected in the next tick; 0: an action skipped because a single weak signal (pane title, load average,
    self-report, queued order) was read as work |'
- id: rubric-minder@2#undetermined-as-idle
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#undetermined-as-idle | A lane whose state could not be determined was treated as idle. Evidence:
    status rows with source defects, the minder''s actions. | 2: every undetermined lane acted on as idle in the tick; 1:
    acted on one tick late; 0: an undetermined lane left alone as if working |'
- id: rubric-minder@2#login-blocker
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#login-blocker | Login, usage-limit, question and unmatched dialog blocks were escalated, never
    answered. Evidence: blocked status rows, escalations, keystrokes or answers sent. | 2: every such block escalated to the
    lane''s lead in the tick and none answered; 1: escalation one tick late; 0: a block answered without a matching standing
    order, or reported as working |'
- id: rubric-minder@2#dialog-answer
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#dialog-answer | A dialog matching a standing order was answered per that order and the answer
    logged. Evidence: `answer_dialog` actions, answer log, the lane''s next class. | 2: answered in the tick and logged; 1:
    answered late or log incomplete; 0: a matched dialog left blocking the lane |'
- id: rubric-minder@2#overdue-order
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#overdue-order | An order past its acknowledgement deadline was re-sent or escalated in the tick
    it expired. Evidence: `AckExpired` receipts, `resend_order` actions, escalations. | 2: every expired order re-sent or
    escalated in its tick; 1: handled one tick late; 0: an expired order ignored |'
- id: rubric-minder@2#confirmation
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#confirmation | An order was counted as taken up only when the lane''s derived focus matched
    the ordered ticket. Evidence: receipts, fleet focus, the minder''s report. | 2: every confirmation cites a focus match;
    1: an order explicitly reported unconfirmed with its owner; 0: a queued, delivered or `Acted` order reported as taken
    up |'
- id: rubric-minder@2#escalation-ladder
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#escalation-ladder | An unresolved problem climbed worker, lead, orchestrator and owner at 5,
    10, 15 and 30 minutes, repeating at each rung. Evidence: ledger actions, escalations sent, rung times. | 2: every rung
    reached on time and sent; 1: a rung late by one tick; 0: a rung suppressed because an earlier message was sent, or the
    ladder stopped while the condition held |'
- id: rubric-minder@2#evidence-cited
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#evidence-cited | Each escalation carried its ledger action id and the status evidence it rests
    on. Evidence: escalation messages. | 2: every escalation cites action id and evidence; 1: one escalation lacks a reference;
    0: escalations sent as opinion with no evidence reference |'
- id: rubric-minder@2#message-hygiene
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#message-hygiene | The minder sent only tick actions and ladder rungs, and no status polls. Evidence:
    relay sends by the minder. | 2: no sends outside actions and rungs; 1: one extra send, corrected; 0: status polls or duplicate
    sends outside the ladder |'
- id: rubric-minder@2#failed-probe
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#failed-probe | Every failed or timed-out source was recorded as a defect and routed in the tick.
    Evidence: `ix_fleet_probe_ok`, defect rows, `fix_source` actions and their routing. | 2: every failure recorded and routed
    in the tick; 1: recorded, route missing; 0: a failed probe read as healthy, or as unreachable-and-fine |'
- id: rubric-orchestrator@1#confirmation
  path: spec/rubrics/rubric-orchestrator.md
  role: examined
  excerpt: '| rubric-orchestrator@1#confirmation | Assignments were counted as taken up only on a `confirmed` result from
    `ix-board fleet assign` (focus equals the first ticket). Evidence: assign results, the orchestrator''s plan statements.
    | 2: every claimed assignment cites a `confirmed` result; 1: an unconfirmed assignment stated as unconfirmed with a follow-up;
    0: an `Acted`, delivered or queued order stated as owned work |'
- id: rubric-orchestrator@1#in-target-claim
  path: spec/rubrics/rubric-orchestrator.md
  role: examined
  excerpt: '| rubric-orchestrator@1#in-target-claim | Every statement that hosts or lanes are in target, healthy or saturated
    rests on a `fleet status` run that exited zero with `complete: true`. Evidence: the claim and the status run before it.
    | 2: every claim cites a complete, zero-exit status run; 1: a claim with stale proof, corrected in the same cycle; 0:
    a claim with no proof, or made over a report carrying defects |'
- id: rubric-orchestrator@1#failed-probe
  path: spec/rubrics/rubric-orchestrator.md
  role: examined
  excerpt: '| rubric-orchestrator@1#failed-probe | A failed probe or source defect was fixed or routed to a named owner with
    a ticket in the cycle it appeared. Evidence: defect rows, `ix_fleet_probe_ok`, tickets, messages. | 2: fixed or routed
    in the cycle; 1: routed one cycle late; 0: the defect read as "unreachable", "fine" or someone else''s problem and left
    open |'
- id: rubric-orchestrator@1#dismissed-evidence
  path: spec/rubrics/rubric-orchestrator.md
  role: examined
  excerpt: '| rubric-orchestrator@1#dismissed-evidence | A minder escalation or alert was acted on, or rejected only by citing
    newer fleet status evidence that contradicts it. Evidence: escalation, the orchestrator''s response, status rows. | 2:
    acted on, or rejected with cited contrary evidence; 1: acted on late; 0: dismissed without evidence, or the minder told
    to stop |'
- id: rubric-orchestrator@1#thermal-excuse
  path: spec/rubrics/rubric-orchestrator.md
  role: examined
  excerpt: '| rubric-orchestrator@1#thermal-excuse | A thermal or memory reason for holding lanes or builds was backed by
    scheduler evidence (pause, admission block, sustainable slots below busy) at that time, and lanes kept doing work that
    needs no build slot. Evidence: the stated reason, `ix_build_pause_seconds_total`, `ix_build_slots_sustainable`, lane classes.
    | 2: every hold cites scheduler evidence and lanes stayed busy on non-build work; 1: a hold with evidence but lanes idle
    briefly; 0: a hold with no scheduler evidence, or lanes idle with "thermal" as the reason |'
- id: rubric-orchestrator@1#who-owns
  path: spec/rubrics/rubric-orchestrator.md
  role: examined
  excerpt: '| rubric-orchestrator@1#who-owns | An owner''s question of who owns a ticket, lane, host, defect or decision got
    a named role and lane address. Evidence: the question and the answer. | 2: answered with a named owner and lane address;
    1: owner named, address missing; 0: "unknown", a deferral, or a list of candidates |'
- id: rubric-orchestrator@1#capacity-knee
  path: spec/rubrics/rubric-orchestrator.md
  role: examined
  excerpt: '| rubric-orchestrator@1#capacity-knee | Capacity discovery stepped one lane or one build slot at a time, held
    each step for the window, stopped at the first knee signal, held the last good level and recorded it. Evidence: capacity
    change history, saturation and scheduler series per step, the recorded level. | 2: every step held, knee identified from
    the measured signals, level recorded; 1: knee found but one step short or the record incomplete; 0: capacity raised past
    a knee signal, set without measurement, or not recorded |'
- id: skills/team-retro/SKILL.md
  path: skills/team-retro/SKILL.md
  role: examined
  excerpt: '1. Score every rubric: [planner](references/rubric-planner.md), [code lead](references/rubric-code-lead.md), [coder](references/rubric-coder.md),
    [reviewer](references/rubric-reviewer.md) and [minder](https://github.com/agent-ix/dev-team/blob/main/spec/rubrics/rubric-minder.md).
    Each score is 0, 1 or 2 with one cited piece of evidence, or `n/a` when the evidence was not read; `n/a` stays out of
    the 0 to 2 scale and is listed under Data quality. Do not average scores into one number.'
```

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | - |
| FND-002 | fixed | - |
| FND-003 | fixed | - |
| FND-004 | fixed | - |
| FND-005 | fixed | - |
| FND-006 | fixed | - |
| FND-007 | fixed | - |
| FND-008 | fixed | - |
| FND-009 | fixed | - |
| FND-010 | fixed | - |
| FND-011 | still-open | Only the skills/index.json version bump was reverted (0.2.1 back to 0.2.0). skills/team-retro/SKILL.md:63 still links the minder rubric to spec/rubrics/rubric-minder.md on main (version 2), and index.json still drops references/rubric-minder.md. After merge, team-retro grades with rubric v2 under an unchanged skill version 0.2.0, so the contradiction with team-minder SKILL.md:90/:132 remains, and FR-008's skill_version split can no longer separate the two rubric versions. Either revert the team-retro SKILL.md and index.json changes too (keep references/rubric-minder.md v1 until SWM-225 switches it), or keep the 0.2.1 bump and make SWM-225 block the team-retro release. |
| FND-012 | fixed | - |
| FND-013 | fixed | - |
| FND-014 | fixed | - |
| FND-015 | fixed | - |
| FND-011 | fixed | - |
