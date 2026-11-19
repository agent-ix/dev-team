---
id: SR-005
title: code-review review of SWM-161 department monitoring
type: SpecReview
analysis: code-review
scope: agent-ix/dev-team; SWM-161; spec/** and docs/department-monitoring.md at db2e482
review_set: subset
---

## Summary

Language-independent review of the ten Markdown files: ownership, links, duplication, integrity and scope. No runtime code, tests or copied upstream definitions were changed; no implementation completeness claim is made.

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
- id: docs/department-monitoring.md
  path: docs/department-monitoring.md
  role: examined
  excerpt: This is the counting and ownership contract referenced by the functional requirements, not a claim of
    deployed behavior. The request is tracked in [SWM-160](https://linear.app/agent-ix/issue/SWM-160). A sanitized
    replay of its planner incidents is the pilot; selectors and thresholds remain configurable.
- id: FR-001
  path: spec/functional/FR-001-evidence-contract.md
  role: examined
  excerpt: The monitoring collector SHALL emit scoped evidence records using the common envelope in [the design](../../docs/department-monitoring.md#evidence-and-comparison-contract).
- id: FR-002
  path: spec/functional/FR-002-deterministic-metrics.md
  role: examined
  excerpt: The ix-board retro collector SHALL compute each measure in the [metric catalog](../../docs/department-monitoring.md#metric-catalog)
    from normalized evidence.
- id: FR-003
  path: spec/functional/FR-003-role-safeguards.md
  role: examined
  excerpt: The dev-team role skills SHALL require the evidence and action checks in the [role contract](../../docs/department-monitoring.md#role-contract).
- id: FR-004
  path: spec/functional/FR-004-terminal-views.md
  role: examined
  excerpt: The monitoring TUI SHALL render status, health and retro from one versioned report model independent
    of terminal widget code.
- id: FR-005
  path: spec/functional/FR-005-fair-build-scheduler.md
  role: examined
  excerpt: The shared Rust build scheduler SHALL grant build leases from configured or verified live host capacity
    using stable FIFO order and bounded priority aging.
- id: IT-001
  path: spec/integration/IT-001-incident-replay.md
  role: examined
  excerpt: Verify that normalized tracker/VCS/pane/relay/host/scheduler evidence produces the expected department
    findings and terminal model across two unrelated teams.
- id: NFR-001
  path: spec/non-functional/NFR-001-reproducible-measurement.md
  role: examined
  excerpt: The monitoring collector SHALL compute identical metric payloads for identical normalized evidence, configuration
    and observation clock without writing to the observed tracker, repository, relay queues or live sessions.
- id: spec/spec.md
  path: spec/spec.md
  role: examined
  excerpt: Catch planning defects, bottlenecks, churn and wasted capacity before a team spends another work interval
    repeating them. This contract governs reusable dev-team guidance and the interfaces it consumes from ix-board
    and build tools.
- id: US-001
  path: spec/usecase/US-001-department-monitoring.md
  role: examined
  excerpt: '**As a** development department owner **I want** to see where planned work stops advancing and who can
    unblock it **So that** I can correct planning, rework and resource waste across teams.'
```

## Method and Limits

No applicable AssuranceProfile exists in the reviewed spec tree; direct review applies. User-directed pin/version telemetry and attributable evidence are requested behavior, not unasked-for file tracking. No desktop implementation, lifecycle replacement, test implementation or private transcript copy is claimed.

Checks: spec validation and EARS summary exit 0 (9/9 grammar-clean); git diff --check exit 0. quire matrix --strict exits 1 for preimplementation coverage (23 untagged criteria and 6 design gaps), expected in this spec-only stage. Its NFR template/extractor mismatch is reported separately; no implementation gap is inferred here. Risk-complexity, evidence-standard recommendation, object review and criterion-strength/Jev are outside this bounded selected review set. Runtime model identifier is unavailable to this harness; marker records unavailable instead of inventing an exact model.
