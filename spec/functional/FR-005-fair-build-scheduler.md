---
id: FR-005
title: Arbitrate shared build capacity fairly
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-001
    type: satisfies
---
# FR-005: Arbitrate shared build capacity fairly

## Description

The shared Rust build scheduler SHALL grant build leases from configured or
verified live host capacity using stable FIFO order within a lane and bounded priority aging.

The shared package is `dev-tools/tools/locked-build`. Operator planning
annotations such as ix-relay `ServerCapacity.max_agents` are not measured build
slots and cannot substitute for the configured/verified capacity source.

## Behavior

A request has a stable ID, scoped ticket/owner, host, requested resource units,
enqueue time, finite base priority and command. States are queued → running →
succeeded/failed/timed_out/cancelled; queued → cancelled is also valid. A child
crash is failed. Every transition emits a stable event ID and timestamps.

The effective priority is `base_priority + floor(wait/aging_interval)`, with
lower enqueue sequence breaking ties within one lane; between lanes at equal effective priority [FR-011](FR-011-priority-classes-lane-fair-share.md) fair share orders requests and never overrides a reservation. Base priorities lie in configured finite
range `[0,P]`; aging interval is configured positive. Reservation eligibility
means the request fits the host's total current configured/verified capacity,
regardless of how much capacity is currently free. Once the oldest such queued
request reaches `(P+1)*aging_interval`, it becomes the reserved next request.
Until it starts, newer requests cannot consume freed units on that host: released
units accumulate until the reservation's full resource request is available.
Running leases are not preempted for priority. With finite hold limits and
sufficient total host capacity, the reserved request starts after existing leases
release. Requests larger than the configured maximum host capacity fail
admission; they do not block the queue indefinitely. A temporary capacity shrink
below a reserved request's size suspends its reservation with a capacity-blocked
reason; restoring sufficient total capacity restores eligibility with its
original enqueue time and age.

Capacity shrink prevents new grants until capacity is sufficient; it does not
kill running work. Existing occupancy above the reduced capacity is reported as
overcommit; no new grant can exceed current capacity or duplicate leased units.
Missing/stale capacity or disk below configured reserve
blocks admission with reason. A configured hold deadline sends termination to
the scheduler-owned child process group, then forced termination after a
configured grace period; a lease is not reissued until child exit is verified.
Cancellation follows the same cleanup. Heartbeat loss marks a lease suspect;
recovery verifies process identity/exit before reclaiming it. PID reuse cannot
prove exit or ownership. Restart recovers persisted queued/running requests.

The wrapper returns the child's exit status exactly once, including exit 75;
it does not retry a child because its exit resembles lock contention. A signaled
child produces non-success with its signal/termination reason. Acquisition
contention and a running child's outcome are separate events.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-005-AC-1 | Equal-priority eligible requests of one lane (see FR-011 for cross-lane share) run in enqueue order; repeated high-priority arrivals cannot pass an eligible request after its configured reservation threshold. A deterministic-clock test proves this under sustained arrivals. | Test |
| FR-005-AC-2 | Higher-priority waiting work gets the next available capacity before aging reservation, while an already running child continues; no new grant exceeds current capacity or duplicates leased units. If capacity shrinks from two units to one while two units are running, both continue, overcommit is reported, and new admission waits for sufficient release. | Test |
| FR-005-AC-3 | Capacity shrink/growth, unavailable/stale host telemetry, insufficient disk reserve and oversized requests follow the defined admission behavior without a hardcoded slot count. | Test |
| FR-005-AC-4 | Timeout, cancellation, child crash, scheduler restart, stale heartbeat and PID-reuse fixtures reclaim leases only after verified termination of the owned child group; unrelated children are never terminated. | Test |
| FR-005-AC-5 | Each queued/running request exposes wait/hold age, owner, resource units, host capacity and termination reason through JSON events consumed by ix-board; enqueue/start/end calculations match the actual transitions. | Test |
| FR-005-AC-6 | Logic is Rust in a shared tool with a thin Make invocation; consumers migrate from project wrappers rather than copying shell/Python arbitration into Rust repositories. | Inspection |
| FR-005-AC-7 | A child returning 75 is invoked once and its status is propagated; a signaled child returns non-success. Neither outcome re-enters acquisition contention or silently reruns the build. | Test |
| FR-005-AC-8 | On a host with total capacity two units, a queued two-unit request reaches the reservation threshold while one-unit jobs keep arriving. The request is reservation-eligible even with fewer than two free units; no newer job consumes subsequently released units, and the reserved request starts after both units are free. | Test |

## Dependencies

- [US-001](../usecase/US-001-department-monitoring.md), capacity-waste problem.
- [FR-001](FR-001-evidence-contract.md), scheduler telemetry envelope.
