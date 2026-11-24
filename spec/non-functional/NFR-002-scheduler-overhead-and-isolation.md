---
id: NFR-002
title: Bound scheduler overhead and isolate probe failure
type: NFR
quality_attribute: reliability
relationships:
  - target: ix://agent-ix/dev-team/FR-009
    type: constrains
  - target: ix://agent-ix/dev-team/FR-010
    type: constrains
  - target: ix://agent-ix/dev-team/FR-015
    type: constrains
---
# NFR-002: Bound scheduler overhead and isolate probe failure

## Statement

The scheduler SHALL NOT let a slow or failing probe delay admission decisions,
pause decisions or metric reads beyond a fixed timeout, and SHALL stay small
enough that governing a host does not consume build capacity.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|---|---|---|---|
| Time a hung probe can delay an admission or pause decision | 1 sample timeout, default 2 s | 5 s | Test |
| Scheduler CPU use on an idle host with 100 queued requests, 1 s sampling | Below 1% of one core | 2% | Test |
| Probe sampling processes spawned per sample | Zero outside the host-probe crate's declared commands | Zero | Inspection |
| Metric series label values drawn from unbounded sets (ticket, request, command) | Zero | Zero | Test |

## Verification

Inject a probe that never returns and confirm that the sample is marked
unavailable at the timeout and decisions continue, with the probe's required or
optional status applied per FR-009. Measure idle CPU over one minute with fixture
requests. Inspect the host-probe crate's command list and confirm the shared crate
is the only sampling path.
