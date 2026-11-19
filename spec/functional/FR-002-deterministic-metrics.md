---
id: FR-002
title: Compute department metrics and repeated loops
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-001
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-001
    type: depends_on
---
# FR-002: Compute department metrics and repeated loops

## Description

The ix-board retro collector SHALL compute each measure in the
[metric catalog](../../docs/department-monitoring.md#metric-catalog) from normalized evidence.

## Behavior

- The snapshot command SHALL emit values or explicit unavailable entries for
  every catalog metric, including unmet configuration and history requirements.
- The delta command SHALL compare compatible snapshots with the previous record
  and configured baseline using the existing retro store and delta contracts.
- The assessment command SHALL attach configured red/amber/green thresholds,
  direction, trend and an owner/action route to each assessable class.
- When query, scope, threshold or formula identity changes, the delta command SHALL
  report `query_changed` rather than a numeric trend.
- When a metric lacks an attributable semantic classification, the collector SHALL report the classification-dependent metric unavailable.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-002-AC-1 | Fixed fixtures compute every catalog entry with exact expected count, age, ratio or nearest-rank duration percentile; replaying the same evidence and clock yields identical metric payloads. | Test |
| FR-002-AC-2 | Boundary fixtures on either side of configured stale, repin-window, WIP, wait, hold, refusal and message thresholds produce the documented assessment; absent thresholds produce unassessed values, never green. | Test |
| FR-002-AC-3 | Tag→repin, state-bounce and reversed-order fixtures emit the exact matching event IDs and participants once per qualifying sequence; duplicate events, legitimate new evidence and unrelated entities do not create a loop. | Test |
| FR-002-AC-4 | Missing state history, truncated relations, unknown message classification and an unavailable remote host make the corresponding metrics unavailable without lowering counts or denominators. | Test |
| FR-002-AC-5 | Previous/baseline comparisons include absolute changes and direction; incompatible query/config/catalog identity emits query_changed. Empty and singleton duration populations follow the catalog rules. | Test |
| FR-002-AC-6 | A department scorecard lists all ten problem classes, source age, available trend, threshold and one configured owner/action for each red; missing owner configuration is visible as unrouted rather than guessed. | Test |

## Dependencies

- [FR-001](FR-001-evidence-contract.md), scoped evidence envelope.
- Existing ix-board [delta](ix://agent-ix/ix-board/FR-027) and
  [backfill](ix://agent-ix/ix-board/FR-028) contracts.
