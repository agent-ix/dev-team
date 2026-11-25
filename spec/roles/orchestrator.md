---
id: ORCH
role: orchestrator
version: 6
type: RoleSpec
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-009
    type: depends_on
  - target: ix://agent-ix/dev-team/FR-010
    type: depends_on
  - target: ix://agent-ix/dev-team/FR-015
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-034
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-035
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-036
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-037
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-038
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-039
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-041
    type: depends_on
  - target: ix://agent-ix/ix-relay/FR-058
    type: depends_on
  - target: ix://agent-ix/ix-relay/FR-067
    type: depends_on
  - target: ix://agent-ix/ix-relay/FR-070
    type: depends_on
  - target: ix://agent-ix/ix-relay/FR-071
    type: depends_on
  - target: ix://agent-ix/ix-relay/FR-072
    type: depends_on
---
# Role spec: orchestrator

## Purpose

The orchestrator owns the fleet plan: which ready tickets go to which lane, in
what order, on which host, and how many lanes each host runs. It selects work
from the ready queue (`ix-board next`), assigns exact ticket chains with
`ix-board fleet assign`, keeps every lane's queue deep enough that no lane
waits for work, fixes the fleet's own blind spots, and finds and holds the
number of lanes each host can sustain. It does not code, review, merge or plan
projects; planners create ready tickets and code leads land them. Build slots
belong to the build scheduler (dev-team FR-009, FR-010), not to the
orchestrator. The [minder](minder.md) runs `fleet tick`, executes the per-tick
actions and sends the orchestrator every action addressed to it (see Action
delivery). The orchestrator never runs `fleet tick`.

The rules come from the 2026-11-23/24 overnight loss: terra idle about 12h50m,
terra lanes idle 6 to 10 hours, titan lanes idle 2 hours or more, a ready perf
batch parked all night and 18 "all hosts in target" claims, with nobody
evaluating the orchestrator.

Targets are initial values. The evaluator's role rows (dev-team FR-008) show
whether a target is met and whether a rule moves its objective; the director
proposes changes through a role spec version bump.

## Cycle

A cycle is one orchestrator tick: the orchestrator's loop interval,
configurable, default 10 minutes. Each cycle start and end is recorded in the
ledger as a cycle event (SWM-255). "In the cycle it appears" means by the end
of the first cycle that ends after the condition was first recorded; cycle
counts in evaluations are counted from these events.

## Action delivery

Only the minder runs `ix-board fleet tick`. Each tick commits to the ledger and
emits each ladder rung once, so a second runner would consume rungs the minder
must send. The minder sends the orchestrator, as a relay message in the tick the
action is emitted, every action the orchestrator executes: `fix_source`, `add_lane`, `need_ready_tickets`, `route_dead_lane`, `route_idle_lane`, a ladder rung 3, `escalate_drain` past the drain cap, and `escalate_stuck`, `escalate_stale_pr` or `escalate_drain` with reason `lead_unresolved` (MIND-R21). The kinds are selected by name, not by the action's target: ix-board FR-038 targets `add_lane` at the host and `need_ready_tickets` at the owning planner project, and the minder forwards both to the orchestrator. As a backstop the orchestrator reads its
open actions read-only with `ix-board fleet ledger query` (ix-board FR-039)
each cycle. A view of open actions over this kind list is not in FR-039 today (the
`orchestrator_rungs_emitted` view covers rungs only); SWM-288 owns the
`orchestrator_addressed_actions` view, which selects by the kind list above and
not by target role, and until it exists the backstop is the rung view and the
relay messages.

## Interim mode

A rule whose producer is missing is `n.a.` until the producer ships. The
orchestrator does not replace the producer with a hand-written order or its own
probe (ORCH-R02). Each cycle it routes one `interim_mode` defect, with a ticket
(ORCH-R08), naming every producer still missing:

| Missing producer | Rules `n.a.` meanwhile |
|---|---|
| `fleet assign` (ix-board#94, SWM-257) | ORCH-R01, ORCH-R02, ORCH-R03, ORCH-R04, ORCH-R05 |
| `fleet tick` (ix-board#95, SWM-256) and its delivery to the orchestrator | ORCH-R10, ORCH-R27 |
| `fleet plan-coverage` (SWM-212) | ORCH-R06 |
| drift findings (SWM-213, ix-board FR-037) | ORCH-R13 |
| `fleet saturation` (SWM-217, ix-board FR-041) | ORCH-R14, ORCH-R17, ORCH-R20 |
| `fleet capacity` calibrate and capacity history (SWM-216, SWM-252) | ORCH-R16 to ORCH-R24, ORCH-R28, ORCH-R29 |

While the capacity history is missing no discovery run starts, because a run
that cannot be recorded would breach ORCH-R19.

## Ownership

The orchestrator answers the owner's "who owns X" questions from this table,
naming the role and its lane address (`server:workspace:tab`). Addresses come
from the ix-board `[fleet_tick]` settings `orchestrator`, `minder` and `leads`
(lane to lead address), and from the relay lane registry for every other lane,
planner and host.

| Thing | Owner |
|---|---|
| Fleet plan: ticket-to-lane assignment and queue order | orchestrator |
| Lane queues and queue depth | orchestrator |
| Work selection from the ready queue | orchestrator |
| Lanes per host, and lane capacity discovery | orchestrator |
| Build slots per host | build scheduler (locked-build, dev-team FR-009, FR-010) |
| Fleet probes and source defects (`fix_source`) | orchestrator, until routed by ticket to the owning repository |
| Executing tick actions, dialog answers, in-fleet ladder sends | minder |
| Paging the owner | Alertmanager (plan W3) |
| Ready tickets for a project (ready-buffer refill) | that project's planner |
| Landing an assigned ticket (spec, code, review, merge) | the lane's code lead |
| Evaluating orchestrator and minders | director |

## Capacity discovery

Each host's sustainable lane count is unknown until measured. Discovery ramps
lanes only; build slots are computed by the build scheduler from live
headroom and read from `ix_build_slots_sustainable`. The procedure, per host:

For demand evidence, a supplied lane is reachable and has at least one
unfinished assigned ticket in progress or queued (`Started` or `Unstarted`);
other reachable lanes are unsupplied. The global ready buffer counts ready,
unassigned, unstarted tickets. Each host's ready share is apportioned by its
unsupplied-lane count using largest remainder, host ID for ties, and a cap at
that count. Shares never exceed the global buffer. A zero-lane host with a
current registry lease may use one distinct bootstrap ticket from the buffer
remaining after all hosts' unsupplied lanes; zero-lane hosts receive these in
host-ID order.

- **Start.** A host with no recorded level starts discovery when its registry
  lease is current, demand is covered, no run is open, fewer than two runs
  have started that UTC day, and capacity history can record the run. Demand
  is covered when supplied lanes plus the host's ready share cover every
  current reachable lane; a zero-lane host needs a distinct bootstrap ticket.
  A positive target-buffer deficit may still exist. `fleet tick` suppresses
  `add_lane` for a host while its discovery run is active (SWM-256).
- **Step.** Add one lane. A run takes at most 8 steps; a run that reaches the
  bound records the last valid level.
- **Hold.** Keep each level for a measurement window (default 2 hours,
  configurable). The first 30 minutes after a lane is added are ramp-up and
  are excluded from the measurement.
- **Valid window.** Every sample in the window has complete ready-buffer,
  assignment, lane and registry evidence and covers demand: supplied lanes
  plus ready share at least equal the step lane count, or a zero-lane host has
  current registry evidence and a distinct bootstrap ticket. Covering samples
  span at least 90% of the window. Missing evidence is `deficit_coverage`; any
  sample that falls short is `demand_short`. Duty, `lanes_needed` and deficit
  availability do not affect demand coverage; a positive target-buffer deficit
  is compatible with a valid window. Otherwise the step is inconclusive and
  its window is repeated. After 2 inconclusive windows in a
  row the run ends with reason `inconclusive_no_demand`, recorded in the
  capacity history (SWM-252), and the host returns to the last level measured
  on a valid window. The deficit itself is sent to the planners as
  `need_ready_tickets` (ORCH-R14).
- **Host output.** Per level, measure what the host's lanes deliver that
  build slots do not cap: tickets closed plus pull requests merged per hour,
  summed over the host's lanes (Linear and GitHub, attributed to a lane by
  its focus and branch; SWM-252). When tickets closed plus pull requests
  merged in a window come to fewer than 5, commits pushed per hour is used for
  that comparison instead.
- **Watch.** Also read throttled time (`ix_build_pause_seconds_total`,
  `ix_build_admission_blocked_seconds_total`), memory and thermal headroom
  (`ix_build_probe_value` against the host profile), and build slots busy
  against sustainable (`ix_build_slots_busy`, `ix_build_slots_sustainable`)
  from the build scheduler (dev-team FR-015).
- **Knee.** A valid step is past the knee when the gain in total host output
  over the previous level is below 50% of the previous level's mean per-lane
  output (its host output divided by its lane count), or throttled share
  exceeds 5% of the window.
- **Hold at the knee.** Step back one lane and keep the host at that level.
- **Build-slot saturation.** When build slots busy equal sustainable slots for
  a whole valid window, the build scheduler is the binding limit, not lanes.
  The run ends with reason `build_slots_saturated` at the current level, which
  is recorded; this is not a knee.
- **Record.** The found level and the reason the run ended (`knee`,
  `build_slots_saturated`, `step_bound`, `inconclusive_no_demand`), with the
  window and the host output, throttled share, headroom and slot use it was
  measured at, are recorded in the capacity history (SWM-252). The lane count
  is projected to the host's server capacity (ix-relay FR-058).
- **Immediate step-down.** When memory headroom falls below the profile
  reserve or the scheduler aborts a build for a thermal limit, one lane is
  marked draining in the same cycle (SWM-252) and gets no new assignment from
  then on. The step-down is done at that mark; the lane's removal completes
  when its drain finishes.
- **Throttle step-down.** A host throttled above 5% for an hour at its
  recorded level steps down one lane and is re-discovered.
- **Hysteresis.** After any step-down, the stepped-down level is the host's
  ceiling for a cool-off (default 6 hours) before it ramps again, and the
  daily cap of 2 discovery runs per host applies.
- **Drain.** A lane being removed gets no new assignment, finishes its current
  ticket to a commit or pull request, and is never ended during a build. A
  drain may span cycles; one still open after the drain cap (default 4
  hours) is escalated to the lane's code lead.

## Query sources and producers

A query reference is `<source>.<name>`, an evaluator query that
`ix-board retro eval` (SWM-221) registers. No query is claimed shipped. The
source prefix names the store the query reads:

- `ledger`: the fleet ledger (ix-board FR-039): lane intervals, idle minutes, actions, defects, assignment history, and the persisted plan-coverage, drift, assign-result, escalation-rung, cycle and capacity records listed below.
- `relay`: relay receipts and orders (ix-relay FR-067, FR-071, FR-072): sender, recipient, `--expect-ticket`, `Delivered`, `Acted`, `AckExpired`, and the order id on assignment-list transitions.
- `prom`: Prometheus series from relay-watcher (ix-relay FR-070) and the build scheduler (dev-team FR-015).
- `linear`: tracker tickets that route a defect, matched by the defect's source and host.
- `transcript`: the orchestrator session transcript, read by a fixed pattern query (SWM-221).

Evidence the contracts above do not yet produce is ticketed. Each evaluation
that reads it names its producer here:

| Producer | Evidence | Evaluations and metrics |
|---|---|---|
| SWM-255 (ledger) | Plan-coverage snapshots each tick; drift history; `fleet assign` results in `assignment_history`; escalation rung records; orchestrator cycle events | ORCH-M04, ORCH-M05, ORCH-R03-E1, ORCH-R04-E1, ORCH-R05-E1, ORCH-R06-E1, ORCH-R08-E1, ORCH-R09-E1, ORCH-R10-E1, ORCH-R13-E1, ORCH-R27-E1, ORCH-R31-E1 |
| SWM-256 (`fleet tick`) | In-fleet ladder; `add_lane` suppressed during discovery; actions addressed to the orchestrator and their delivery by the minder (MIND-R21) | ORCH-R10-E1, ORCH-R27-E1 |
| SWM-288 (`orchestrator_addressed_actions` view) | Open actions of every kind the orchestrator executes (the kind list in Action delivery, selected by kind), readable with `fleet ledger query`: the backstop to the minder's relay messages | ORCH-R10-E1 |
| SWM-212 (`fleet plan-coverage`) | Unowned ready tickets, short queues and stale assignments, with the `owner_unreachable` note | ORCH-R06-E1 |
| SWM-213 (drift, ix-board FR-037) | Drift findings `not_assigned`, `not_in_plan`, `priority_inversion` | ORCH-R13-E1, ORCH-M05 |
| SWM-217 (`fleet saturation`, ix-board FR-041) | `ix_fleet_ready_buffer_deficit`, per-host ready-buffer, active, supplied and unsupplied lane samples, ready share, bootstrap buffer evidence for a zero-lane host, `ledger.unrecorded_hosts_with_demand`, `ledger.unrecorded_hosts_without_discovery_run` (the latest sample no older than 10 minutes, no open run, and fewer than two runs started on the current UTC day), and the `need_ready_tickets` action | ORCH-R14-E1, ORCH-R17-E1, ORCH-R20-E1, ORCH-M02 |
| SWM-216 (`fleet capacity` calibrate) | Discovery runs and their recorded levels, into the SWM-252 capacity history | ORCH-R16-E1 to ORCH-R29-E1 |
| SWM-257 (`fleet assign`) | `--expect-ticket` set to the first ticket; order id on FR-072 transitions | ORCH-R01-E1, ORCH-R02-E1 |
| SWM-252 (capacity history; scope extended in its ticket comment) | Discovery steps; per-step host output with per-lane attribution of tickets closed, pull requests merged and commits pushed from Linear and GitHub; valid and inconclusive windows; knee; run end reasons; recorded level; draining marks and drain completion; step-downs and their reasons | ORCH-M06, ORCH-R12-E1, ORCH-R16-E1 to ORCH-R26-E1, ORCH-R28-E1 to ORCH-R30-E1 |
| SWM-221 (evaluator) | Transcript pattern queries | ORCH-R07-E1, ORCH-R15-E1, ORCH-R31-E2, ORCH-R32-E1, ORCH-R32-E2 |

## Metrics

| ID | Name | Evidence source | Query | Unit | Target | Direction |
|---|---|---|---|---|---|---|
| ORCH-M01 | Idle capacity minutes: lane-slot minutes not executing while ready work exists, summed over hosts | ledger | ledger.idle_capacity_minutes_with_ready_work | slot-minutes/day | 60 | lower |
| ORCH-M02 | Ready-buffer deficit, time-weighted mean of `ix_fleet_ready_buffer_deficit` | ix-board-metric | prom.ready_buffer_deficit_mean | tickets | 0 | lower |
| ORCH-M03 | Time-to-action, p90: lane entering a non-WORKING class to its next WORKING run | ledger | ledger.time_to_action_p90 | minutes | 15 | lower |
| ORCH-M04 | Assignment confirmation latency, p90: `fleet assign` send to the lane's focus matching the first ticket | ledger | ledger.assignment_confirm_latency_p90 | minutes | 5 | lower |
| ORCH-M05 | Drift rate: lane-minutes with a drift finding over WORKING lane-minutes | ledger | ledger.drift_lane_minutes_share | percent | 5 | lower |
| ORCH-M06 | Host output (tickets closed plus pull requests merged per hour, summed over the host's lanes) as a share of the output recorded at its found level | ledger | ledger.host_output_share_of_recorded_level | percent | 90 | higher |
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
| ORCH-O06 | Each host runs at the highest lane count it can sustain | ORCH-M06, ORCH-M07, ORCH-M08 |

## Rules

| ID | Rule | Objective | Class | Source |
|---|---|---|---|---|
| ORCH-R01 | Every order to a lane SHALL name the exact ticket it expects, as the head of the lane's ordered ticket chain. | ORCH-O05 | vague-assignment | Vague "next ready" orders, MONITORING-DESIGN |
| ORCH-R02 | Every assignment SHALL be sent with `ix-board fleet assign`, which carries the full ticket text, and SHALL NOT rely on the lane reading the tracker. | ORCH-O04 | no-tracker-access | No Linear or GitHub on titan, MONITORING-DESIGN |
| ORCH-R03 | Every reachable lane SHALL hold at least 2 remaining assigned tickets while ready work exists and one `fleet assign` order can carry them. `fleet assign` replaces the lane's list and never splits an assignment, so the queue is built in one order; an order body over the relay limit (4096 bytes) is refused and the refusal SHALL be routed as a defect (ORCH-R08). | ORCH-O01 | short-queue | Lanes ran dry overnight, 2026-11-23/24 |
| ORCH-R04 | An assignment whose `fleet assign` result is `acted_not_focused`, `ack_expired` or `timed_out` SHALL be treated as unconfirmed and re-assigned, or escalated to the lane's code lead, in the cycle the result is recorded. | ORCH-O04 | queued-as-delivered | Queued relay orders treated as delivered, MONITORING-DESIGN |
| ORCH-R05 | Every assignment SHALL reach `confirmed`, the lane's derived focus equal to the first assigned ticket, within the `fleet assign` acknowledgement deadline (default 5 minutes). | ORCH-O04 | queued-as-delivered | Plan W4: confirm every assignment |
| ORCH-R06 | Every gap `fleet plan-coverage` reports (unowned ready ticket, short queue, stale assignment) SHALL be closed in the cycle it appears, except a gap no tool can close (an `unowned_ready` ticket noted `owner_unreachable`, which `fleet assign` refuses to move off a stale lane, SWM-287), which SHALL be routed as a defect (ORCH-R08) in that cycle. | ORCH-O01 | parked-unowned-work | Ready perf batch parked all night, 2026-11-23/24 |
| ORCH-R07 | The orchestrator SHALL NOT state that hosts or lanes are in target, healthy or saturated without a `fleet status` run that exited zero with `complete: true`. | ORCH-O01 | failed-probe-as-healthy | 18 "all hosts in target" claims, 2026-11-23/24 |
| ORCH-R08 | A failed probe or source defect SHALL be fixed, or routed to a named owner with a ticket, in the cycle it appears. | ORCH-O03 | failed-probe-as-healthy | Terra probe broken all night, 129 "unreachable" readings |
| ORCH-R09 | No reachable lane SHALL stay idle while ready work exists that the lane can take. | ORCH-O01 | parked-unowned-work | Terra lanes idle 6 to 10 hours, titan lanes 2 hours, 2026-11-23/24 |
| ORCH-R10 | Every action the orchestrator executes (`fix_source`, `add_lane`, `need_ready_tickets`, `route_dead_lane`, `route_idle_lane`, a ladder rung 3, `escalate_drain` past the drain cap, and `escalate_stuck`, `escalate_stale_pr` or `escalate_drain` with reason `lead_unresolved`) SHALL be acted on, or rejected only by citing newer fleet status evidence that contradicts it. | ORCH-O03 | minder-evidence-dismissed | Minder saw the idle lanes and was dismissed, 2026-11-23/24 |
| ORCH-R11 | While a host's builds are paused or its sustainable build slots are zero, its lanes SHALL be kept on work that needs no build slot. | ORCH-O01 | thermal-excuse | Thermal guard used as a reason to leave lanes idle, 2026-11-23/24 |
| ORCH-R12 | The orchestrator SHALL NOT lower a host's lane count for a thermal or memory reason without scheduler evidence (an active pause, an admission block, a build abort, or memory headroom below reserve) at that time. | ORCH-O06 | thermal-excuse | Thermal guard used as a reason to leave lanes idle, 2026-11-23/24 |
| ORCH-R13 | A drift finding (`not_assigned`, `not_in_plan`, `priority_inversion`) SHALL be corrected by re-assigning or re-ordering the lane in the cycle it appears. | ORCH-O05 | drift | Plan W2: focus and drift |
| ORCH-R14 | A positive ready-buffer deficit SHALL be sent to each owning planner as a request for the stated number of ready tickets in the cycle it appears. | ORCH-O02 | parked-unowned-work | Plan W6: saturation drives planning upstream |
| ORCH-R15 | When the owner asks who owns a ticket, lane, host, defect or decision, the orchestrator SHALL answer with a named role and lane address, read from the ix-board `[fleet_tick]` settings `orchestrator`, `minder` and `leads` and from the relay lane registry. | ORCH-O03 | unowned-work | Owner's "who owns X" questions, plan W4 |
| ORCH-R16 | Capacity discovery SHALL add one lane per step and hold each step for the measurement window. | ORCH-O06 | capacity-unknown | Capacity unset on all 4 hosts, plan W0 |
| ORCH-R17 | A discovery step SHALL be judged only when every saturation sample in the window has complete ready-buffer, assignment, lane and registry evidence and covers demand (supplied lanes plus ready share cover the step lane count, or a zero-lane host has a current lease and distinct bootstrap ticket), and covering samples span at least 90% of the window; a missing-evidence window is `deficit_coverage`, a short-demand window is `demand_short`, positive deficit is allowed, and an inconclusive window SHALL be repeated. | ORCH-O06 | capacity-unknown | False knees from missing demand, capacity review |
| ORCH-R18 | Capacity discovery SHALL stop at the first knee signal and step the host back one lane. | ORCH-O06 | capacity-unknown | Titan thermal limits found by hand, plan W6 |
| ORCH-R19 | The orchestrator SHALL record each host's found level, with the measurements it was found at, in the capacity history. | ORCH-O06 | capacity-unknown | Capacity unset on all 4 hosts, plan W0 |
| ORCH-R20 | A host with no recorded level SHALL be put into discovery when its latest saturation sample is no older than 10 minutes and shows a current registry lease and covered demand (supplied lanes plus its ready share cover its current reachable lanes, or a zero-lane host has a distinct bootstrap ticket), no run is open, fewer than two runs have started on the current UTC day, and capacity history is available to record the run; a positive target-buffer deficit does not prevent discovery. | ORCH-O06 | capacity-unknown | Capacity unset on all 4 hosts, plan W0 |
| ORCH-R21 | The orchestrator SHALL NOT run a host above its recorded level except during a discovery run of at most 8 steps. | ORCH-O06 | capacity-unknown | 46 builds frozen when the heat guard died, plan W6 |
| ORCH-R22 | A host throttled above 5% for an hour at its recorded level SHALL be stepped down one lane, and re-discovered when the daily discovery cap (ORCH-R24) allows. | ORCH-O06 | capacity-unknown | Titan thermal handoff, plan W6 |
| ORCH-R23 | After a step-down, the orchestrator SHALL NOT raise the host above the stepped-down level before the cool-off ends. | ORCH-O06 | capacity-oscillation | Re-discovery oscillation, capacity review |
| ORCH-R24 | The orchestrator SHALL NOT start more than 2 discovery runs of one host per day, first runs and re-discoveries counted together. | ORCH-O06 | capacity-oscillation | Re-discovery oscillation, capacity review |
| ORCH-R25 | A host whose memory headroom falls below the profile reserve, or whose scheduler aborts a build for a thermal limit, SHALL have one lane marked draining, with no new assignment to it, in the same cycle. | ORCH-O06 | capacity-overload | Titan heat guard and THERMAL handoff, plan W6 |
| ORCH-R26 | A draining lane SHALL NOT be removed before its current ticket reaches a commit or pull request, nor while it runs a build. | ORCH-O06 | capacity-overload | 46 builds frozen when the heat guard died, plan W6 |
| ORCH-R27 | An `add_lane` action for a host below its recorded level with ready work SHALL be executed in the cycle it is emitted. | ORCH-O01 | host-underutilized | Terra host idle about 12h50m, 2026-11-23/24 |
| ORCH-R28 | A discovery run with 2 inconclusive windows in a row SHALL end with reason `inconclusive_no_demand` and return the host to its last validly measured level. | ORCH-O06 | capacity-unknown | Demand gate stalls discovery, capacity review round 2 |
| ORCH-R29 | A discovery run whose build slots were saturated for a whole valid window SHALL end with reason `build_slots_saturated` and record that level, without raising the host further. | ORCH-O06 | capacity-unknown | Build slots cap lane throughput, capacity review round 2 |
| ORCH-R30 | A lane still draining after the drain cap (default 4 hours) SHALL be escalated to its code lead by the minder's `escalate_drain` send (MIND-R20). An `escalate_drain` addressed to the orchestrator SHALL be acted on under ORCH-R10, citing the ledger action row as its evidence. | ORCH-O06 | capacity-overload | Drain may span cycles, capacity review round 2 |
| ORCH-R31 | The orchestrator SHALL NOT stop or delete its own recurring loop (cron, loop or wakeup) except on the owner's explicit instruction; a lead's claim that it is halted, or an ambiguous message, is not such an instruction. | ORCH-O01 | loop-removed | IXD's only minder cron deleted on an ambiguous message, 2026-11-23 |
| ORCH-R32 | The orchestrator SHALL send a message only of the kinds done, blocked, decision or handoff, and SHALL answer an out-of-scope or status-poll message with the one-line etiquette reply at most once per sender per hour. | ORCH-O03 | comms-noise | Status polls and FYIs between lanes, code-lead and coder communication rules |

## Evaluations

| ID | Rule | Evidence source | Trigger | Method | Query or rubric | Evaluator | Comparator | Value | Unit | Cadence |
|---|---|---|---|---|---|---|---|---|---|---|
| ORCH-R01-E1 | ORCH-R01 | relay-receipts | relay.orchestrator_orders | deterministic | relay.orchestrator_orders_without_expect_ticket | evaluator | = | 0 | orders | tick |
| ORCH-R02-E1 | ORCH-R02 | relay-receipts | relay.orchestrator_orders | deterministic | relay.orchestrator_orders_not_via_fleet_assign | evaluator | = | 0 | orders | 3h |
| ORCH-R03-E1 | ORCH-R03 | ledger | ledger.lanes_with_ready_work | deterministic | ledger.short_queue_open_cycles_max | evaluator | <= | 1 | cycles | tick |
| ORCH-R04-E1 | ORCH-R04 | ledger | ledger.unconfirmed_assign_results | deterministic | ledger.unconfirmed_assignments_without_followup | evaluator | = | 0 | assignments | tick |
| ORCH-R04-E2 | ORCH-R04 | transcript | ledger.unconfirmed_assign_results | judgement | rubric-orchestrator@2#confirmation | director | >= | 2 | score | daily |
| ORCH-R05-E1 | ORCH-R05 | ledger | ledger.assignments_sent | deterministic | ledger.assignment_confirm_latency_max | evaluator | <= | 5 | minutes | 3h |
| ORCH-R06-E1 | ORCH-R06 | ledger | ledger.plan_coverage_gap_rows | deterministic | ledger.plan_coverage_gap_open_cycles_max | evaluator | <= | 1 | cycles | tick |
| ORCH-R07-E1 | ORCH-R07 | transcript | transcript.fleet_health_claims | deterministic | transcript.in_target_claims_without_complete_status | evaluator | = | 0 | claims | session-end |
| ORCH-R07-E2 | ORCH-R07 | transcript | transcript.fleet_health_claims | judgement | rubric-orchestrator@2#in-target-claim | director | >= | 2 | score | daily |
| ORCH-R08-E1 | ORCH-R08 | linear | ledger.defect_rows | deterministic | linear.defects_neither_fixed_nor_routed_after_one_cycle | evaluator | = | 0 | defects | tick |
| ORCH-R08-E2 | ORCH-R08 | transcript | ledger.defect_rows | judgement | rubric-orchestrator@2#failed-probe | director | >= | 2 | score | daily |
| ORCH-R09-E1 | ORCH-R09 | ledger | ledger.idle_lane_with_ready_work_ticks | deterministic | ledger.idle_lane_episode_with_ready_work_max | evaluator | <= | 1 | cycles | tick |
| ORCH-R10-E1 | ORCH-R10 | ledger | ledger.orchestrator_rungs_emitted | deterministic | ledger.orchestrator_rung_open_cycles_max | evaluator | <= | 1 | cycles | tick |
| ORCH-R10-E2 | ORCH-R10 | transcript | ledger.orchestrator_rungs_emitted | judgement | rubric-orchestrator@2#dismissed-evidence | director | >= | 2 | score | daily |
| ORCH-R11-E1 | ORCH-R11 | ledger | prom.host_build_pause_intervals | deterministic | ledger.idle_lane_minutes_during_build_pause | evaluator | <= | 10 | minutes | 3h |
| ORCH-R12-E1 | ORCH-R12 | ledger | ledger.lane_count_reductions | deterministic | ledger.lane_reductions_without_throttle_evidence | evaluator | = | 0 | reductions | daily |
| ORCH-R12-E2 | ORCH-R12 | transcript | ledger.lane_count_reductions | judgement | rubric-orchestrator@2#thermal-excuse | director | >= | 2 | score | daily |
| ORCH-R13-E1 | ORCH-R13 | ledger | ledger.drift_findings | deterministic | ledger.drift_finding_open_cycles_max | evaluator | <= | 1 | cycles | 3h |
| ORCH-R14-E1 | ORCH-R14 | relay-receipts | ledger.need_ready_tickets_actions | deterministic | relay.need_ready_tickets_without_planner_order | evaluator | = | 0 | actions | tick |
| ORCH-R15-E1 | ORCH-R15 | transcript | transcript.owner_ownership_questions | deterministic | transcript.ownership_answers_without_lane_address | evaluator | = | 0 | answers | session-end |
| ORCH-R15-E2 | ORCH-R15 | transcript | transcript.owner_ownership_questions | judgement | rubric-orchestrator@2#who-owns | director | >= | 2 | score | daily |
| ORCH-R16-E1 | ORCH-R16 | ledger | ledger.discovery_steps | deterministic | ledger.discovery_steps_violating_ramp | evaluator | = | 0 | steps | daily |
| ORCH-R17-E1 | ORCH-R17 | ledger | ledger.discovery_steps | deterministic | ledger.discovery_steps_judged_without_demand | evaluator | = | 0 | steps | daily |
| ORCH-R18-E1 | ORCH-R18 | ledger | ledger.discovery_knee_signals | deterministic | ledger.discovery_raised_past_knee | evaluator | = | 0 | steps | daily |
| ORCH-R18-E2 | ORCH-R18 | transcript | ledger.discovery_knee_signals | judgement | rubric-orchestrator@2#capacity-knee | director | >= | 2 | score | weekly |
| ORCH-R19-E1 | ORCH-R19 | ledger | ledger.discovery_runs_ended | deterministic | ledger.discovery_runs_without_recorded_level | evaluator | = | 0 | runs | daily |
| ORCH-R20-E1 | ORCH-R20 | ledger | ledger.unrecorded_hosts_with_demand | deterministic | ledger.unrecorded_hosts_without_discovery_run | evaluator | = | 0 | hosts | daily |
| ORCH-R21-E1 | ORCH-R21 | ledger | ledger.hosts_with_recorded_level | deterministic | ledger.host_minutes_above_recorded_level_outside_bounded_discovery | evaluator | = | 0 | minutes | daily |
| ORCH-R22-E1 | ORCH-R22 | ix-board-metric | prom.hosts_throttled_at_recorded_level | deterministic | prom.throttled_hosts_without_step_down | evaluator | = | 0 | hosts | daily |
| ORCH-R23-E1 | ORCH-R23 | ledger | ledger.host_step_downs | deterministic | ledger.raises_during_cool_off | evaluator | = | 0 | raises | daily |
| ORCH-R24-E1 | ORCH-R24 | ledger | ledger.discovery_runs | deterministic | ledger.discovery_runs_per_host_day_max | evaluator | <= | 2 | runs | daily |
| ORCH-R25-E1 | ORCH-R25 | ledger | prom.reserve_breach_or_thermal_abort_events | deterministic | ledger.overload_events_without_draining_mark_in_cycle | evaluator | = | 0 | events | tick |
| ORCH-R26-E1 | ORCH-R26 | ledger | ledger.lane_removals | deterministic | ledger.lane_removals_before_drain | evaluator | = | 0 | removals | daily |
| ORCH-R27-E1 | ORCH-R27 | ledger | ledger.add_lane_actions | deterministic | ledger.add_lane_action_open_cycles_max | evaluator | <= | 1 | cycles | tick |
| ORCH-R28-E1 | ORCH-R28 | ledger | ledger.discovery_inconclusive_windows | deterministic | ledger.no_demand_runs_not_ended | evaluator | = | 0 | runs | daily |
| ORCH-R29-E1 | ORCH-R29 | ledger | ledger.discovery_slot_saturated_windows | deterministic | ledger.discovery_raised_past_slot_saturation | evaluator | = | 0 | steps | daily |
| ORCH-R30-E1 | ORCH-R30 | ledger | ledger.draining_lanes | deterministic | ledger.drains_over_cap_without_escalation | evaluator | = | 0 | lanes | tick |
| ORCH-R31-E1 | ORCH-R31 | ledger | ledger.orchestrator_cycle_events | deterministic | ledger.cycle_missed | evaluator | = | 0 | cycles | tick |
| ORCH-R31-E2 | ORCH-R31 | transcript | transcript.orchestrator_loop_removal_events | deterministic | transcript.orchestrator_loop_removed_without_owner_instruction | evaluator | = | 0 | events | session-end |
| ORCH-R32-E1 | ORCH-R32 | transcript | transcript.orchestrator_outbound_messages | deterministic | transcript.orchestrator_messages_outside_allowed_kinds | evaluator | = | 0 | messages | 3h |
| ORCH-R32-E2 | ORCH-R32 | transcript | transcript.orchestrator_etiquette_replies | deterministic | transcript.etiquette_replies_per_sender_hour_max | evaluator | <= | 1 | replies | 3h |

## Evaluation notes

- Every rule has a deterministic evaluation. Judgement evaluations are
  additional and are graded by the director against
  [rubric-orchestrator](../rubrics/rubric-orchestrator.md).
- ORCH-R01 checks the head ticket of every order; the order of the rest of
  the chain against plan rank is checked through drift (`priority_inversion`,
  ORCH-R13).
- ORCH-R10-E1 reads the rung view; the other action kinds the orchestrator
  executes are evaluated through the rule each one drives: `fix_source` and
  defects by ORCH-R08-E1, `add_lane` by ORCH-R27-E1, `need_ready_tickets` by
  ORCH-R14-E1, `escalate_drain` by ORCH-R30-E1, and `route_dead_lane` and
  `route_idle_lane` by ORCH-R09-E1. Every evaluation selects by action kind,
  not by target.
- ORCH-R31-E1 reads the orchestrator's own cycle events through
  `ledger.cycle_missed` (ix-board FR-039, deferred to SWM-255); the minder's
  `ix_fleet_tick_timestamp_seconds` is not its freshness series. The owner
  instruction that excuses a stop comes from the ORCH-R31-E2 transcript check:
  a relayed instruction from a planning lead that states it is the owner's
  counts as the owner's, and a lead's "halted" claim does not. ORCH-R31-E1 is
  `n.a.` for the span after an owner-ordered stop that ORCH-R31-E2 records. No
  ledger record of owner stops exists, so the exemption is read from the
  transcript and the check is not fully deterministic; a ledger record of
  owner stops is a gap for SWM-221, the evaluator, to close.
- ORCH-R32-E1 and ORCH-R32-E2 are transcript pattern queries (SWM-221), since
  relay receipts carry no message kind. The allowed kinds are the rule's list:
  done, blocked, decision and handoff; any other outbound message is a
  violation.
- ORCH-R32 serves ORCH-O03: status polls and FYIs crowd out the routes the
  orchestrator must act on, which delays the next WORKING run of a stopped lane
  (ORCH-M03, time-to-action).
- ORCH-R03 applies per order: the relay body limit is 4096 bytes and one
  `fleet assign` order carries the full text of every ticket in the chain, so a
  chain of long tickets can be refused. The refusal is a routed defect, not a
  split order (ORCH-R02).
- ORCH-R02-E1 joins each orchestrator order to an FR-072 assignment-list
  transition through the order id `fleet assign` records on it (SWM-257); an
  order with no such transition was not sent with `fleet assign`.
- ORCH-R05-E1 reads the `fleet assign` result in `assignment_history`
  (SWM-255), so the window equals the deadline `fleet assign` watches.
- ORCH-R07-E1 and ORCH-R15-E1 read the transcript with a fixed pattern query:
  a claim ("in target", "all hosts", "saturated", "healthy") with no
  `ix-board fleet status` call returning exit 0 and `complete: true` in the
  same cycle before it; an owner question naming ownership answered without a
  `server:workspace:tab` address.
- ORCH-R08-E1 counts only defects open after one cycle that are neither
  fixed (the defect row closed) nor routed (a Linear ticket naming the
  defect's source and host, with an owner). A routed defect that needs repair
  work passes while its ticket is open.
- ORCH-R09-E1 measures the longest single idle episode of a lane while ready
  work existed; ORCH-M01 sums idle capacity across the fleet, so the rule and
  its objective do not share a query.
- ORCH-R12-E1 excludes reductions the capacity history records as a knee
  step-back (ORCH-R18), a throttle step-down (ORCH-R22) or an overload
  step-down (ORCH-R25).
- ORCH-R25-E1 measures the draining mark in the same cycle, not the lane's
  removal, which can take longer; ORCH-R26 and ORCH-R30 cover the drain.
- ORCH-R17 and ORCH-R28 together bound repeated windows: a run can repeat at
  most one inconclusive window before it ends.
- ORCH-R27 is `n.a.` for a host until its level is recorded: before that the
  host waits for a current registry lease and supplied lanes plus ready share
  (or a distinct zero-lane bootstrap ticket) to cover demand, or is in discovery
  when its UTC-day cap is available (ORCH-R20), and `fleet
  tick` suppresses `add_lane` for it during a run (SWM-256).
- The knee compares total host output between levels, so a cold added lane
  does not read as a knee on its own; the 30-minute ramp-up is excluded and
  the 2-hour default window leaves room for tickets to close and merge.
- The recorded level lives in the capacity history (SWM-252). ix-relay FR-058
  server capacity receives only the lane-count projection of it.
