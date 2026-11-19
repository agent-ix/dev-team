---
id: FR-001
title: Attribute scoped monitoring evidence
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-001
    type: satisfies
---
# FR-001: Attribute scoped monitoring evidence

## Description

The monitoring collector SHALL emit scoped evidence records using the common
envelope in [the design](../../docs/department-monitoring.md#evidence-and-comparison-contract).

## Behavior

- The collector SHALL derive populations from configured teams, projects,
  repositories, lanes and hosts rather than a project's hardcoded labels.
- When a required source is missing, stale, ambiguous or partially paginated,
  the collector SHALL mark dependent measurements unavailable with a reason.
- The reporter SHALL distinguish observed events from attributed classifications
  and operator-reported incidents.
- The collector SHALL preserve existing ix-board metric definitions when adding
  department metrics to its retro catalog.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-001-AC-1 | A report from two configured teams contains their separate populations and one deduplicated department rollup; no out-of-scope issue or remote lane is silently included. | Test |
| FR-001-AC-2 | Removing a required page, host, source timestamp or capacity config makes dependent values null/unavailable with source and reason; unaffected values remain visible and no unavailable class is green. | Test |
| FR-001-AC-3 | Every value exposes metric ID/version, scope, observation/window timestamps, unit, population/denominator, source references, query/config identity and status; classified events also expose attribution and classification version. | Test |
| FR-001-AC-4 | A relay enqueue does not count as delivery or acknowledgement; an ambiguous pane/session association is unknown rather than assigned to the focused pane. | Test |
| FR-001-AC-5 | An existing metric fixture produces unchanged values after catalog extension; changed formulas use a new metric ID. | Test |

## Dependencies

- [US-001](../usecase/US-001-department-monitoring.md), operator intent.
- Existing ix-board [snapshot](ix://agent-ix/ix-board/FR-024),
  [store](ix://agent-ix/ix-board/FR-025) and
  [unavailable](ix://agent-ix/ix-board/FR-026) contracts.
