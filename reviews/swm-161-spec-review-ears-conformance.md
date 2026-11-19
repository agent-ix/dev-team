---
id: SR-009
title: ears-conformance review of SWM-161 department monitoring
type: SpecReview
analysis: ears-conformance
scope: agent-ix/dev-team; SWM-161; spec/** and docs/department-monitoring.md at db2e482
review_set: subset
---

## Summary

The engine reports 9/9 documents grammar-clean with no EARS findings. Named actors, concrete responses and conditional unavailable behavior remain testable; US and IT prose are context rather than EARS statements.

Ticket: SWM-161. Frozen PR: dev-team#23, db2e482.

## Verdict

**PASS**. No defects found within this method’s stated scope.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | low | No findings (placeholder) | - |

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
```

## Method and Limits

No applicable AssuranceProfile exists in the reviewed spec tree; direct review applies. User-directed pin/version telemetry and attributable evidence are requested behavior, not unasked-for file tracking. No desktop implementation, lifecycle replacement, test implementation or private transcript copy is claimed.

Checks: spec validation and EARS summary exit 0 (9/9 grammar-clean); git diff --check exit 0. quire matrix --strict exits 1 for preimplementation coverage (23 untagged criteria and 6 design gaps), expected in this spec-only stage. Its NFR template/extractor mismatch is reported separately; no implementation gap is inferred here. Risk-complexity, evidence-standard recommendation, object review and criterion-strength/Jev are outside this bounded selected review set. Runtime model identifier is unavailable to this harness; marker records unavailable instead of inventing an exact model.
