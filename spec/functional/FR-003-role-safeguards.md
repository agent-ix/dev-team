---
id: FR-003
title: Ground role actions and planner self-evaluation
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-001
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-002
    type: depends_on
---
# FR-003: Ground role actions and planner self-evaluation

## Description

The dev-team role skills SHALL require the evidence and action checks in the
[role contract](../../docs/department-monitoring.md#role-contract).

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-003-AC-1 | A minder scenario with a login screen, an omitted remote lane, recently finished nested workers and queued mail requires pane lifecycle/PR-worktree/token reconciliation; neither live_subagents nor relay seen is accepted as liveness proof. | Inspection |
| FR-003-AC-2 | An order unacknowledged beyond its configured acknowledgement deadline receives an owned escalation in the current observation tick; each order records confirmed by pane, PR head or SHA, or explicitly unconfirmed. Queued messages are not blindly resent. | Inspection |
| FR-003-AC-3 | Planner instructions require pre-send evidence, authorized scope, plan membership, prior-order/changed-evidence and batch checks; end-tick audit records ad hoc assignments, out-of-scope conscription and excess messages. The planner rubric consumes their deterministic counts with cited judgment. | Inspection |
| FR-003-AC-4 | Lead/coder guidance requires focused crate checks during iteration, one lead-run aggregate gate at final head, capacity from config/live state, scoped spec-gap routing and no stale toolchain notice. Gated or stale claims are reconciled to the team's configured ready state when active work is absent. | Inspection |
| FR-003-AC-5 | Lead pin guidance folds required dependency pins into the consuming PR, names a pin owner/window and forbids repin-only PRs; review rounds use explicit current policy rather than an invented cap or automatic unsafe merge. | Inspection |
| FR-003-AC-6 | Retro and department-health instructions interpret ix-board values and route actions; no prose asks the agent to invent deterministic metrics, infer unavailable evidence as zero, hardcode slots, or conscript another lane. Unshipped commands are reported unavailable. | Inspection |

## Dependencies

- [FR-002](FR-002-deterministic-metrics.md), deterministic role evidence.
- [US-001](../usecase/US-001-department-monitoring.md), operator intent.
