---
id: FR-011
title: Schedule by priority class with fair share per lane
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-003
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-005
    type: depends_on
---
# FR-011: Schedule by priority class with fair share per lane

## Description

A request SHALL carry a named priority class, `gate`, `test` or `check`, that maps
to the FR-005 base priority range. A lane is the request's owner, written as the bounded lane address `server:workspace:tab`; a session id is not a lane and is refused. The scheduler SHALL keep one lane from monopolizing a host while
other lanes wait, without weakening the FR-005 ordering and reservation guarantees.

## Behavior

The classes map to base priorities `check` = 0, `test` = 1, `gate` = 2 with
`maximum_priority` = 2 and the profile's aging interval. A merge-ready final gate is
submitted as `gate` and is admitted before waiting `test` and `check` work, as the
retired slot wrapper's priority marker did, but a waiting gate cannot hold off a
lower class forever: FR-005 aging and reservation still apply. Priority is chosen
by the caller from a closed set; an unknown class is refused. A caller cannot
raise the priority of a queued request; it can cancel and resubmit.

Fair share per lane: at one effective priority, when more than one lane has
eligible waiting requests, a request from a lane that already holds its
share or more (sustainable slots, counted as resource units, divided by the number of lanes
with running or eligible work, rounded up; a lane's holding is the sum of units its running leases occupy) yields to an equal-priority request from a lane under
its share. Within one lane, order stays enqueue order. A reserved request under
the FR-005 reservation rule is exempt from the share rule. Lane share never
preempts running work. A lane with no waiting competitor may use every free slot.
A request that omits a lane or ticket, or whose lane is not a lane address, is refused.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-011-AC-1 | With one slot busy and `check`, `test` and `gate` requests queued in that order, the gate is admitted first, then the test, then the check, before any aging threshold; an unknown class and a missing lane are refused with a request error. | Test |
| FR-011-AC-2 | Under sustained `gate` arrivals on a deterministic clock, a queued `check` request reaches reservation after `(2+1) * aging` and starts before any later arrival, matching FR-005-AC-1. | Test |
| FR-011-AC-3 | With two slots, lane A holding both and lane B waiting at equal priority, B's request is admitted first when a slot frees even though A's request was enqueued earlier; with B absent, A's waiting requests use free slots in enqueue order. | Test |
| FR-011-AC-4 | A request at its reservation threshold is admitted ahead of an under-share lane's equal-priority request, and the fair-share rule never signals a running lease. | Test |
| FR-011-AC-5 | Replaying the reported 70-minute starvation shape (a wrapper waiting behind continuously arriving peers) on the deterministic clock gives that wrapper a lease within the reservation bound. | Test |
| FR-011-AC-6 | With three sustainable units, lane A holding one two-unit lease, lane B holding none, one unit free, and A's one-unit request enqueued before B's, B's request is admitted first because A holds 2 of a share of 2 units (counted in units, not leases). A lane given as a session id is refused. | Test |

## Dependencies

- [FR-005](FR-005-fair-build-scheduler.md), aging, reservation and FIFO within a lane.
- [FR-009](FR-009-host-profile-sustainable-slots.md), sustainable slot count used in the lane share.
