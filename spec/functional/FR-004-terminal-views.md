---
id: FR-004
title: Render shared status health and retro views
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-001
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-002
    type: depends_on
---
# FR-004: Render shared status health and retro views

## Description

The monitoring TUI SHALL render status, health and retro from one versioned
report model independent of terminal widget code.

## Behavior

- Status SHALL display scoped plan progress, active/ready work, lane evidence
  age, configured capacity, blockers and the next owned action.
- Health SHALL display all problem classes with severity, evidence age, trend,
  owner and action, with drilldown to cited observations.
- Retro SHALL display baseline/previous/current metrics and loop evidence with
  deterministic results separated from role interpretation.
- When pane identity cannot be verified, the TUI SHALL allow an explicit scope
  view with identity-dependent fields unknown rather than fail to start.
- The TUI SHALL resolve credentials through the existing saved-credential path
  with the documented environment override.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-004-AC-1 | Given the same versioned model, TUI and JSON show matching statuses, values, evidence and actions; the model can be rendered without terminal initialization for a later plugin/desktop consumer. | Test |
| FR-004-AC-2 | Status/health/retro switch by keyboard, preserve selected scope and show source age/unavailable diagnostics within an 80×24 terminal without hidden fatal errors; quit restores the terminal. | Test |
| FR-004-AC-3 | With LINEAR_API_KEY unset and a valid saved credential, a scoped TUI starts without exposing credentials; missing auth produces an actionable diagnostic and a nonzero live-collection status, while a supplied offline report remains readable. | Test |
| FR-004-AC-4 | Missing or ambiguous native pane identity permits an explicit project/team/offline report; no nearby session is guessed. An unreachable host and relation-page failure remain visible partial results. | Test |
| FR-004-AC-5 | Existing dashboard startup/binding/credential tickets are linked and reused; reported-only failures are labeled reported until independently reproduced. | Inspection |

## Dependencies

- [FR-002](FR-002-deterministic-metrics.md), report assessment model.
- [FR-001](FR-001-evidence-contract.md), uncertainty and source attribution.
