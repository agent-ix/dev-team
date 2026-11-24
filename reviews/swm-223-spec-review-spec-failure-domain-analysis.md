---
id: SR-030
title: "failure-domain review of SWM-222/223 capacity discovery and escalation"
type: SpecReview
analysis: failure-domain
scope: "agent-ix/dev-team; SWM-222, SWM-223; spec/roles/**, spec/rubrics/**, spec/functional/FR-006, spec/spec.md, skills/team-retro diff origin/main...96d8047 (PR dev-team#32)"
review_set: subset
date: 2026-11-24
---

# failure-domain review of SWM-222/223 capacity discovery and escalation

## Summary

Tickets: SWM-222 (orchestrator role spec), SWM-223 (minder role spec). Frozen PR: dev-team#32 at 96d8047. Evidence contracts read from origin/main: ix-board FR-034..043, ix-relay FR-058 and FR-067..072, dev-team FR-006..010 and FR-015. Validation re-run with quire 0.52.1 against the spec-artifacts-process origin/main export (80d25b6): validate, --strict, --okf and coverage exit 0.

## Verdict

**FAIL**. The capacity procedure has the right shape: step, hold, watch, knee, back off, record, re-discover. It lacks hysteresis, so re-discovery oscillates. Its knee test is scale-dependent and demand-blind. It fights the build scheduler's own control loop and the tick's `add_lane` controller, and it has no safe, fast step-down for lanes.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | Re-discovery can oscillate. ORCH-R20 steps a throttled host down one level and restarts discovery with the same knee thresholds and no hysteresis. When throttling comes from load near the knee (ambient heat, a heavier repo mix), the ramp climbs back to the level that throttled within one window, holds, throttles for an hour and steps down again, in a cycle of about 1.5 to 2 hours. Add a cool-off ceiling (the stepped-down level is the maximum for a period), a stricter re-entry signal (for example throttled share below 2% before any step up), and a cap on re-discoveries per day. | spec/roles/orchestrator.md:144 |
| FND-002 | high | The knee test ('throughput rises less than 5% over the previous level') is relative to the total. At N lanes or slots, a perfectly linear +1 step adds 1/N, so from N >= 20 every step reads as a knee. Throughput also depends on demand: with too little build-heavy ready work, or an empty gate queue, the gain is about 0 and a false knee stops the ramp low. Compare the marginal gain per added unit with the mean per unit at the previous level, and count a window only when demand saturated it (queue wait > 0 or slots busy = sustainable). | spec/roles/orchestrator.md:141 |
| FND-003 | medium | Ramping build slots duplicates the build scheduler. dev-team FR-009 and FR-010 already compute sustainable slots from live probes every 5 s, with a `grow_after` hold, admission blocks and aborts, and say that no slot count is edited by hand. The orchestrator can only move `max_slots`, a second, slower loop on the same variable. Stepping 'one lane or one build slot' also mixes two dimensions, so a knee cannot be attributed. Discover lanes per host, and read build slots from `ix_build_slots_sustainable`. | spec/roles/orchestrator.md:140 |
| FND-004 | medium | prom.capacity_reductions_without_throttle_evidence counts every reduction made without a scheduler pause, admission block or slots-below-busy. A knee step-back under ORCH-R17 (throughput or queue-wait signal) and a step-down under ORCH-R20 are reductions that the role spec requires, and a metric series cannot tell their reason, so compliant discovery fails R12-E1. Exclude reductions recorded as discovery steps (the SWM-252 discovery state). | spec/roles/orchestrator.md:166 |
| FND-005 | medium | Step-down is neither fast enough nor safe. A memory-headroom breach below the profile reserve is acted on only at the next window or after an hour of throttling, and lane memory (agent RSS) is outside the scheduler's FR-010 abort path. No drain is specified for removing a lane: stop assigning, let the current ticket reach a commit or PR, and never end a session mid-build. Add an immediate step-down on a reserve breach and a drain procedure. | spec/roles/orchestrator.md:144 |
| FND-006 | medium | Two controllers change lane count. The ix-board FR-038 `add_lane` action fires on busy ratio below 0.85 and is independent of discovery. During discovery, executing it breaks ORCH-R16 (one step per window). Before a level is recorded, which is all four hosts today, ORCH-R21 ('below its recorded level') is undefined, so neither rule says when to add lanes outside discovery. State that discovery suppresses `add_lane` per host, and that an unrecorded host starts discovery. | spec/roles/orchestrator.md:145 |
| FND-007 | low | ORCH-R19 has a loophole. It exempts time 'inside a discovery step', and no maximum discovery duration or step count is stated, so a host kept in perpetual discovery runs above its recorded level without failing R19. Bound discovery (for example a maximum number of steps per run) and count over-level minutes beyond the bound. | spec/roles/orchestrator.md:143 |

## Examined Scope

```yaml
scope:
- id: MIND-R01
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R01 | A lane whose state cannot be determined (UNKNOWN from a legacy source, or a fleet status row carrying
    a source defect) SHALL be treated as idle and acted on in the same tick. | MIND-O01 | unknown-as-not-idle | UNKNOWN read
    as not idle, 2026-11-23 |'
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
- id: ORCH-R12-E1
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: '| ORCH-R12-E1 | ORCH-R12 | ix-board-metric | prom.host_capacity_reductions | deterministic | prom.capacity_reductions_without_throttle_evidence
    | evaluator | = | 0 | reductions | daily |'
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
