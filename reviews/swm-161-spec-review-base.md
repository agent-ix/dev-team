---
id: SR-006
title: base review of SWM-161 department monitoring
type: SpecReview
analysis: base
scope: agent-ix/dev-team; SWM-161; spec/** and docs/department-monitoring.md at db2e482
review_set: subset
---

## Summary

The ten requested problem classes, all 29 functional ACs, user intent, adverse replay, role safeguards and rollout limitations are represented. Two deterministic metric/assessment edge cases need clarification before implementation.

Ticket: SWM-161. Frozen PR: dev-team#23, db2e482.

## Verdict

**CONDITIONAL**. Resolve the listed findings before merge.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | claims_without_movement has no minimum claim age: an issue started seconds ago with no PR/commit/worktree movement matches the stale-cutoff rule immediately. Require the claim itself to be older than the cutoff and specify its age anchor before treating absent movement as stale. | docs/department-monitoring.md:75 |
| FND-002 | medium | Per-metric thresholds do not define a deterministic class assessment when required metrics mix red, amber, unassessed or unavailable. State the class aggregation and unknown precedence so identical reports yield the same class severity. | docs/department-monitoring.md:61 |

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
- id: FR-002-AC-1
  path: spec/functional/FR-002-deterministic-metrics.md
  role: examined
  excerpt: Fixed fixtures compute every catalog entry with exact expected count, age, ratio or nearest-rank duration
    percentile; replaying the same evidence and clock yields identical metric payloads.
- id: FR-002-AC-2
  path: spec/functional/FR-002-deterministic-metrics.md
  role: examined
  excerpt: Boundary fixtures on either side of configured stale, repin-window, WIP, wait, hold, refusal and message
    thresholds produce the documented assessment; absent thresholds produce unassessed values, never green.
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
- id: FR-002-AC-5
  path: spec/functional/FR-002-deterministic-metrics.md
  role: examined
  excerpt: Previous/baseline comparisons include absolute changes and direction; incompatible query/config/catalog
    identity emits query_changed. Empty and singleton duration populations follow the catalog rules.
- id: FR-002-AC-6
  path: spec/functional/FR-002-deterministic-metrics.md
  role: examined
  excerpt: A department scorecard lists all ten problem classes, source age, available trend, threshold and one
    configured owner/action for each red; missing owner configuration is visible as unrouted rather than guessed.
- id: FR-003-AC-1
  path: spec/functional/FR-003-role-safeguards.md
  role: examined
  excerpt: A minder scenario with a login screen, an omitted remote lane, recently finished nested workers and queued
    mail requires pane lifecycle/PR-worktree/token reconciliation; neither live_subagents nor relay seen is accepted
    as liveness proof.
- id: FR-003-AC-2
  path: spec/functional/FR-003-role-safeguards.md
  role: examined
  excerpt: An order unacknowledged beyond its configured acknowledgement deadline receives an owned escalation in
    the current observation tick; each order records confirmed by pane, PR head or SHA, or explicitly unconfirmed.
    Queued messages are not blindly resent.
- id: FR-003-AC-3
  path: spec/functional/FR-003-role-safeguards.md
  role: examined
  excerpt: Planner instructions require pre-send evidence, authorized scope, plan membership, prior-order/changed-evidence
    and batch checks; end-tick audit records ad hoc assignments, out-of-scope conscription and excess messages.
    The planner rubric consumes their deterministic counts with cited judgment.
- id: FR-003-AC-4
  path: spec/functional/FR-003-role-safeguards.md
  role: examined
  excerpt: Lead/coder guidance requires focused crate checks during iteration, one lead-run aggregate gate at final
    head, capacity from config/live state, scoped spec-gap routing and no stale toolchain notice. Gated or stale
    claims are reconciled to the team's configured ready state when active work is absent.
- id: FR-003-AC-5
  path: spec/functional/FR-003-role-safeguards.md
  role: examined
  excerpt: Lead pin guidance folds required dependency pins into the consuming PR, names a pin owner/window and
    forbids repin-only PRs; review rounds use explicit current policy rather than an invented cap or automatic unsafe
    merge.
- id: FR-003-AC-6
  path: spec/functional/FR-003-role-safeguards.md
  role: examined
  excerpt: Retro and department-health instructions interpret ix-board values and route actions; no prose asks the
    agent to invent deterministic metrics, infer unavailable evidence as zero, hardcode slots, or conscript another
    lane. Unshipped commands are reported unavailable.
- id: FR-004-AC-1
  path: spec/functional/FR-004-terminal-views.md
  role: examined
  excerpt: Given the same versioned model, TUI and JSON show matching statuses, values, evidence and actions; the
    model can be rendered without terminal initialization for a later plugin/desktop consumer.
- id: FR-004-AC-2
  path: spec/functional/FR-004-terminal-views.md
  role: examined
  excerpt: Status/health/retro switch by keyboard, preserve selected scope and show source age/unavailable diagnostics
    within an 80×24 terminal without hidden fatal errors; quit restores the terminal.
- id: FR-004-AC-3
  path: spec/functional/FR-004-terminal-views.md
  role: examined
  excerpt: With LINEAR_API_KEY unset and a valid saved credential, a scoped TUI starts without exposing credentials;
    missing auth produces an actionable diagnostic and a nonzero live-collection status, while a supplied offline
    report remains readable.
- id: FR-004-AC-4
  path: spec/functional/FR-004-terminal-views.md
  role: examined
  excerpt: Missing or ambiguous native pane identity permits an explicit project/team/offline report; no nearby
    session is guessed. An unreachable host and relation-page failure remain visible partial results.
- id: FR-004-AC-5
  path: spec/functional/FR-004-terminal-views.md
  role: examined
  excerpt: Existing dashboard startup/binding/credential tickets are linked and reused; reported-only failures are
    labeled reported until independently reproduced.
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

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | Round 1, 84265cd: The linked counting rule now requires latest started/claim time strictly before the stale cutoff, excludes fresh/restarted claims, and reports unknown history unavailable. |
| FND-002 | fixed | Round 1, 84265cd: The linked design now specifies red then amber then unknown then green precedence, explicit required populations, completeness and missing-policy behavior. |

### Round 1 evidence

```yaml
dispositions:
- fnd: FND-001
  outcome: fixed
  after_excerpt: '`claims_without_movement`: started issues whose latest started/claim timestamp is strictly before
    end minus configured stale interval and whose linked PR-head, commit and worktree evidence shows no movement
    after that cutoff; a fresh/restarted claim is excluded, and an unknown claim timestamp/history makes the metric
    unavailable'
  path: docs/department-monitoring.md
  reason: The linked counting rule now requires latest started/claim time strictly before the stale cutoff, excludes
    fresh/restarted claims, and reports unknown history unavailable.
- fnd: FND-002
  outcome: fixed
  after_excerpt: 'A class

    is red if any required metric is red; otherwise amber if any is amber; otherwise

    unknown if any required metric is unknown; otherwise green. Thus a known breach

    remains visible when other evidence is missing. Independently, `complete` is true

    only when all required metrics are assessable, and the report lists unknown IDs

    and reasons even for red/amber classes.'
  path: docs/department-monitoring.md
  reason: The linked design now specifies red then amber then unknown then green precedence, explicit required populations,
    completeness and missing-policy behavior.
```

## Disposition Verdict

**PASS** at 84265cd. Every original finding in this artifact is fixed. No new findings from the confined fix review. Original findings and initial verdict remain the historical review record.
