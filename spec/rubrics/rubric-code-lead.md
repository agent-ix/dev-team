---
id: rubric-code-lead
version: 1
type: Rubric
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
---
# Rubric: code lead

The code lead rubric grades the judgement evaluations of the
[code lead role spec](../roles/code-lead.md). `/team-retro` grades it. A
judgement evaluation cites one check as `rubric-code-lead@1#<check-slug>`.

Each check scores 0, 1 or 2 with one cited piece of evidence, or `n/a` when the
evidence was not read. `n/a` is listed under Data quality and is never counted
as 0 or 2. Scores are not averaged. A judgement score never overrides a
deterministic verdict on the same rule.

Quantitative checks consume ix-board assessments under the team's current
policy; unsupported measurements score `n/a`. No fixed review cap or slot count
comes from this rubric.

## Checks

| ID | Check | Scale |
|----|-------|-------|
| rubric-code-lead@1#gate-progress | The gate path is moving. Evidence: snapshot and delta path measures. | 2: emitted progress improves; 1: flat with an owned blocker; 0: flat and the blocker ignored |
| rubric-code-lead@1#review-flow | Review queue and work-in-progress findings are handled, reviewed pull requests included. Evidence: flow assessment, reviewer age. | 2: queue and WIP findings resolved; 1: a corrective owner is active; 0: a known stall left unattended |
| rubric-code-lead@1#honest-state | Unworked gated, stale and merged-but-open claims are reconciled. Evidence: stale and merged-open assessments, the tracker. | 2: claims reconciled; 1: correction in progress; 0: a started claim persists against evidence |
| rubric-code-lead@1#fix-rounds | Review rounds meet the current policy. Evidence: round policy assessment. | 2: current policy met; 1: an excess with a recorded remedy; 0: an excess or repeating loop ignored |
| rubric-code-lead@1#gate-discipline | Iteration uses focused checks and the lead runs one final aggregate gate. Evidence: classified checks and gate telemetry. | 2: focused iteration and one final lead gate; 1: a justified exception recorded; 0: repeated workspace gates without new evidence |
| rubric-code-lead@1#pin-discipline | Required pins ride the consuming pull request in its window. Evidence: pin assessment, dependency owner. | 2: required pins in the consuming pull request and window; 1: drift has an owner; 0: repin-only churn continues |
| rubric-code-lead@1#open-findings | Reviews and dispositions are matched to the merged pull request before merge. Evidence: tracker markers. | 2: every finding dispositioned before merge; 1: a discrepancy corrected before merge; 0: an open finding merged |
| rubric-code-lead@1#merge-safety | Only the reviewed head and reviewed behavior are merged. Evidence: tracker markers, pull request head. | 2: matched review and reviewed head; 1: a discrepancy corrected before merge; 0: unreviewed behavior merged |
| rubric-code-lead@1#one-directory | One ticket shares one coder, reviewer and gate tree. Evidence: worktree evidence. | 2: one shared tree per ticket; 1: a stray tree corrected; 0: separate review or gate worktrees |
| rubric-code-lead@1#resources | The current capacity and admission source is honored. Evidence: host, queue and hold assessment. | 2: current source honored; 1: missing telemetry routed to its owner; 0: slots invented or reservations bypassed |
| rubric-code-lead@1#agent-recovery | A confirmed idle agent with ready work is acted on. Evidence: complete lifecycle report and ready queue. | 2: confirmed idle with ready work acted on; 1: remedy owned but pending; 0: a confirmed idle agent remains unassigned |
| rubric-code-lead@1#delivery | Outcomes are distinct and confirmation is cited. Evidence: pane, pull request or SHA, relay receipt chain. | 2: outcomes distinct with confirmation cited; 1: an unconfirmed action escalated; 0: queued or seen claimed as completion |

## Notes

- `WAITING` and `RECENT` are observed without nudging and do not fail
  `agent-recovery`.
- File ages, token totals and worker counts alone establish neither idle state
  nor capacity. Unknown or incomplete evidence remains `n/a`.
- Read next: the [strategies](../../skills/team-retro/references/strategies.md).
