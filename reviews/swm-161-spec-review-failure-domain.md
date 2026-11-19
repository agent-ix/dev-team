---
id: SR-010
title: failure-domain review of SWM-161 department monitoring
type: SpecReview
analysis: failure-domain
scope: agent-ix/dev-team; SWM-161; spec/** and docs/department-monitoring.md at db2e482
review_set: subset
---

## Summary

Identity uncertainty, partial pages, remote failure, process groups, PID reuse, exit 75 and cleanup are covered. Variable-size resource requests expose an ambiguity in starvation reservation eligibility.

Ticket: SWM-161. Frozen PR: dev-team#23, db2e482.

## Verdict

**CONDITIONAL**. Resolve the listed findings before merge.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | Eligibility is undefined for reservation. On a two-unit host, a waiting two-unit request never fits current free capacity while one-unit priority work keeps rolling; treating eligible as fits-now prevents reservation and permits starvation. Define reservation eligibility against total feasible capacity and accumulate the required free units. | spec/functional/FR-005-fair-build-scheduler.md:29 |

## Examined Scope

```yaml
scope:
- id: FR-001-AC-1
  path: spec/functional/FR-001-evidence-contract.md
  role: examined
  excerpt: A report from two configured teams contains their separate populations and one deduplicated department
    rollup; no out-of-scope issue or remote lane is silently included.
- id: FR-001-AC-2
  path: spec/functional/FR-001-evidence-contract.md
  role: examined
  excerpt: Removing a required page, host, source timestamp or capacity config makes dependent values null/unavailable
    with source and reason; unaffected values remain visible and no unavailable class is green.
- id: FR-001-AC-3
  path: spec/functional/FR-001-evidence-contract.md
  role: examined
  excerpt: Every value exposes metric ID/version, scope, observation/window timestamps, unit, population/denominator,
    source references, query/config identity and status; classified events also expose attribution and classification
    version.
- id: FR-001-AC-4
  path: spec/functional/FR-001-evidence-contract.md
  role: examined
  excerpt: A relay enqueue does not count as delivery or acknowledgement; an ambiguous pane/session association
    is unknown rather than assigned to the focused pane.
- id: FR-001-AC-5
  path: spec/functional/FR-001-evidence-contract.md
  role: examined
  excerpt: An existing metric fixture produces unchanged values after catalog extension; changed formulas use a
    new metric ID.
- id: FR-005-AC-1
  path: spec/functional/FR-005-fair-build-scheduler.md
  role: examined
  excerpt: Equal-priority eligible requests run in enqueue order; repeated high-priority arrivals cannot pass an
    eligible request after its configured reservation threshold. A deterministic-clock test proves this under sustained
    arrivals.
- id: FR-005-AC-2
  path: spec/functional/FR-005-fair-build-scheduler.md
  role: examined
  excerpt: Higher-priority waiting work gets the next available capacity before aging reservation, while an already
    running child continues; capacity is never granted twice or exceeded.
- id: FR-005-AC-3
  path: spec/functional/FR-005-fair-build-scheduler.md
  role: examined
  excerpt: Capacity shrink/growth, unavailable/stale host telemetry, insufficient disk reserve and oversized requests
    follow the defined admission behavior without a hardcoded slot count.
- id: FR-005-AC-4
  path: spec/functional/FR-005-fair-build-scheduler.md
  role: examined
  excerpt: Timeout, cancellation, child crash, scheduler restart, stale heartbeat and PID-reuse fixtures reclaim
    leases only after verified termination of the owned child group; unrelated children are never terminated.
- id: FR-005-AC-5
  path: spec/functional/FR-005-fair-build-scheduler.md
  role: examined
  excerpt: Each queued/running request exposes wait/hold age, owner, resource units, host capacity and termination
    reason through JSON events consumed by ix-board; enqueue/start/end calculations match the actual transitions.
- id: FR-005-AC-6
  path: spec/functional/FR-005-fair-build-scheduler.md
  role: examined
  excerpt: Logic is Rust in a shared tool with a thin Make invocation; consumers migrate from project wrappers rather
    than copying shell/Python arbitration into Rust repositories.
- id: FR-005-AC-7
  path: spec/functional/FR-005-fair-build-scheduler.md
  role: examined
  excerpt: A child returning 75 is invoked once and its status is propagated; a signaled child returns non-success.
    Neither outcome re-enters acquisition contention or silently reruns the build.
- id: FR-002-AC-3
  path: spec/functional/FR-002-deterministic-metrics.md
  role: examined
  excerpt: Tag→repin, state-bounce and reversed-order fixtures emit the exact matching event IDs and participants
    once per qualifying sequence; duplicate events, legitimate new evidence and unrelated entities do not create
    a loop.
- id: FR-002-AC-4
  path: spec/functional/FR-002-deterministic-metrics.md
  role: examined
  excerpt: Missing state history, truncated relations, unknown message classification and an unavailable remote
    host make the corresponding metrics unavailable without lowering counts or denominators.
```

## Method and Limits

No applicable AssuranceProfile exists in the reviewed spec tree; direct review applies. User-directed pin/version telemetry and attributable evidence are requested behavior, not unasked-for file tracking. No desktop implementation, lifecycle replacement, test implementation or private transcript copy is claimed.

Checks: spec validation and EARS summary exit 0 (9/9 grammar-clean); git diff --check exit 0. quire matrix --strict exits 1 for preimplementation coverage (23 untagged criteria and 6 design gaps), expected in this spec-only stage. Its NFR template/extractor mismatch is reported separately; no implementation gap is inferred here. Risk-complexity, evidence-standard recommendation, object review and criterion-strength/Jev are outside this bounded selected review set. Runtime model identifier is unavailable to this harness; marker records unavailable instead of inventing an exact model.
