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

A request SHALL carry one of the configured named priority classes
`must-fix`, `point`, `block` or `periodic`, mapped to the FR-005 base priority
range by host policy. The example policy maps them to 3, 2, 1 and 0,
respectively. A caller may select the class with `locked-build run --class` or
through the `LOCKED_BUILD_CLASS` cargo-shim setting; an unknown or unmapped
class is refused. A lane is the request's owner, written as the bounded lane address `server:workspace:tab`; a session id is not a lane and is refused. The scheduler SHALL keep one lane from monopolizing a host while
other lanes wait, without weakening the FR-005 ordering and reservation guarantees.

## Behavior

The class-to-priority map is configured per host and each value is at most
`maximum_priority`. A `must-fix` request is submitted for a fix blocking the
current review or gate; `point` is the ordinary implementation class; `block`
is for a sustained, multi-step work package; and `periodic` is for scheduled
maintenance. Higher configured priority is admitted before lower configured
priority, but aging and reservation still apply. Priority is chosen by the
caller from the configured closed set; an unknown class is refused. A caller cannot
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
| FR-011-AC-1 | With one slot busy and `periodic`, `block`, `point`, and `must-fix` requests queued in that order under the example mapping, they are admitted in descending mapped priority before any aging threshold; an unknown or unmapped class and a missing lane are refused with a request error. | Test |
| FR-011-AC-2 | Under sustained `must-fix` arrivals on a deterministic clock, a queued `periodic` request reaches reservation after `(maximum_priority+1) * aging` and starts before any later arrival, matching FR-005-AC-1. | Test |
| FR-011-AC-3 | With two slots, lane A holding both and lane B waiting at equal priority, B's request is admitted first when a slot frees even though A's request was enqueued earlier; with B absent, A's waiting requests use free slots in enqueue order. | Test |
| FR-011-AC-4 | A request at its reservation threshold is admitted ahead of an under-share lane's equal-priority request, and the fair-share rule never signals a running lease. | Test |
| FR-011-AC-5 | Replaying a request waiting behind continuously arriving higher-priority peers on a deterministic clock gives that request a lease within the reservation bound. | Test |
| FR-011-AC-6 | With three sustainable units, lane A holding one two-unit lease, lane B holding none, one unit free, and A's one-unit request enqueued before B's, B's request is admitted first because A holds 2 of a share of 2 units (counted in units, not leases). A lane given as a session id is refused. | Test |

## Dependencies

- [FR-005](FR-005-fair-build-scheduler.md), aging, reservation and FIFO within a lane.
- [FR-009](FR-009-host-profile-sustainable-slots.md), sustainable slot count used in the lane share.
