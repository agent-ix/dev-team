---
id: SR-007
title: integrity review of SWM-161 department monitoring
type: SpecReview
analysis: integrity
scope: agent-ix/dev-team; SWM-161; spec/** and docs/department-monitoring.md at db2e482
review_set: subset
---

## Summary

Structural validation passes. The nonpreemption behavior and capacity assertion conflict under a shrinking host; clarify the admission invariant.

Ticket: SWM-161. Frozen PR: dev-team#23, db2e482.

## Verdict

**CONDITIONAL**. Resolve the listed findings before merge.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | The unconditional never-exceeded capacity assertion conflicts with nonpreemptive capacity shrink: two running units remain after capacity shrinks to one. Apply the invariant to new grants and explicitly retain/report existing overcommit until running leases finish. | spec/functional/FR-005-fair-build-scheduler.md:55 |

## Examined Scope

```yaml
scope:
- id: FR-001-statement-1-1
  path: spec/functional/FR-001-evidence-contract.md
  role: examined
  excerpt: The monitoring collector SHALL emit scoped evidence records using the common envelope in [the design](../../docs/department-monitoring.md#evidence-and-comparison-contract).
- id: FR-001-statement-2-1
  path: spec/functional/FR-001-evidence-contract.md
  role: examined
  excerpt: '- The collector SHALL derive populations from configured teams, projects,   repositories, lanes and
    hosts rather than a project''s hardcoded labels.'
- id: FR-001-statement-2-2
  path: spec/functional/FR-001-evidence-contract.md
  role: examined
  excerpt: '- When a required source is missing, stale, ambiguous or partially paginated,   the collector SHALL
    mark dependent measurements unavailable with a reason.'
- id: FR-001-statement-2-3
  path: spec/functional/FR-001-evidence-contract.md
  role: examined
  excerpt: '- The reporter SHALL distinguish observed events from attributed classifications   and operator-reported
    incidents.'
- id: FR-001-statement-2-4
  path: spec/functional/FR-001-evidence-contract.md
  role: examined
  excerpt: '- The collector SHALL preserve existing ix-board metric definitions when adding   department metrics
    to its retro catalog.'
- id: FR-002-statement-1-1
  path: spec/functional/FR-002-deterministic-metrics.md
  role: examined
  excerpt: The ix-board retro collector SHALL compute each measure in the [metric catalog](../../docs/department-monitoring.md#metric-catalog)
    from normalized evidence.
- id: FR-002-statement-2-1
  path: spec/functional/FR-002-deterministic-metrics.md
  role: examined
  excerpt: '- The snapshot command SHALL emit values or explicit unavailable entries for   every catalog metric,
    including unmet configuration and history requirements.'
- id: FR-002-statement-2-2
  path: spec/functional/FR-002-deterministic-metrics.md
  role: examined
  excerpt: '- The delta command SHALL compare compatible snapshots with the previous record   and configured baseline
    using the existing retro store and delta contracts.'
- id: FR-002-statement-2-3
  path: spec/functional/FR-002-deterministic-metrics.md
  role: examined
  excerpt: '- The assessment command SHALL attach configured red/amber/green thresholds,   direction, trend and
    an owner/action route to each assessable class.'
- id: FR-002-statement-2-4
  path: spec/functional/FR-002-deterministic-metrics.md
  role: examined
  excerpt: '- When query, scope, threshold or formula identity changes, the delta command SHALL   report `query_changed`
    rather than a numeric trend.'
- id: FR-002-statement-2-5
  path: spec/functional/FR-002-deterministic-metrics.md
  role: examined
  excerpt: '- When a metric lacks an attributable semantic classification, the collector SHALL report the classification-dependent
    metric unavailable.'
- id: FR-003-statement-1-1
  path: spec/functional/FR-003-role-safeguards.md
  role: examined
  excerpt: The dev-team role skills SHALL require the evidence and action checks in the [role contract](../../docs/department-monitoring.md#role-contract).
- id: FR-004-statement-1-1
  path: spec/functional/FR-004-terminal-views.md
  role: examined
  excerpt: The monitoring TUI SHALL render status, health and retro from one versioned report model independent
    of terminal widget code.
- id: FR-004-statement-2-1
  path: spec/functional/FR-004-terminal-views.md
  role: examined
  excerpt: '- Status SHALL display scoped plan progress, active/ready work, lane evidence   age, configured capacity,
    blockers and the next owned action.'
- id: FR-004-statement-2-2
  path: spec/functional/FR-004-terminal-views.md
  role: examined
  excerpt: '- Health SHALL display all problem classes with severity, evidence age, trend,   owner and action, with
    drilldown to cited observations.'
- id: FR-004-statement-2-3
  path: spec/functional/FR-004-terminal-views.md
  role: examined
  excerpt: '- Retro SHALL display baseline/previous/current metrics and loop evidence with   deterministic results
    separated from role interpretation.'
- id: FR-004-statement-2-4
  path: spec/functional/FR-004-terminal-views.md
  role: examined
  excerpt: '- When pane identity cannot be verified, the TUI SHALL allow an explicit scope   view with identity-dependent
    fields unknown rather than fail to start.'
- id: FR-004-statement-2-5
  path: spec/functional/FR-004-terminal-views.md
  role: examined
  excerpt: '- The TUI SHALL resolve credentials through the existing saved-credential path   with the documented
    environment override.'
- id: FR-005-statement-1-1
  path: spec/functional/FR-005-fair-build-scheduler.md
  role: examined
  excerpt: The shared Rust build scheduler SHALL grant build leases from configured or verified live host capacity
    using stable FIFO order and bounded priority aging.
- id: NFR-001-statement-1-1
  path: spec/non-functional/NFR-001-reproducible-measurement.md
  role: examined
  excerpt: The monitoring collector SHALL compute identical metric payloads for identical normalized evidence, configuration
    and observation clock without writing to the observed tracker, repository, relay queues or live sessions.
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
```

## Method and Limits

No applicable AssuranceProfile exists in the reviewed spec tree; direct review applies. User-directed pin/version telemetry and attributable evidence are requested behavior, not unasked-for file tracking. No desktop implementation, lifecycle replacement, test implementation or private transcript copy is claimed.

Checks: spec validation and EARS summary exit 0 (9/9 grammar-clean); git diff --check exit 0. quire matrix --strict exits 1 for preimplementation coverage (23 untagged criteria and 6 design gaps), expected in this spec-only stage. Its NFR template/extractor mismatch is reported separately; no implementation gap is inferred here. Risk-complexity, evidence-standard recommendation, object review and criterion-strength/Jev are outside this bounded selected review set. Runtime model identifier is unavailable to this harness; marker records unavailable instead of inventing an exact model.

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | Round 1, 84265cd: New grants cannot exceed capacity; running work survives a two-to-one shrink with overcommit reported and admission held. |

### Round 1 evidence

```yaml
dispositions:
- fnd: FND-001
  outcome: fixed
  after_excerpt: Test |
  path: spec/functional/FR-005-fair-build-scheduler.md
  reason: New grants cannot exceed capacity; running work survives a two-to-one shrink with overcommit reported
    and admission held.
```

## Disposition Verdict

**PASS** at 84265cd. Every original finding in this artifact is fixed. No new findings from the confined fix review. Original findings and initial verdict remain the historical review record.
