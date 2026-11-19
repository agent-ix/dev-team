# Code lead rubric

Score 2/1/0 with cited evidence. Quantitative rows consume ix-board assessments
under the team's current policy; unsupported measurements score `n/a` under
Data quality. No fixed review cap or slot count comes from this rubric.

| Check | 2 | 1 | 0 | Evidence |
|---|---|---|---|---|
| Gate progress | Emitted progress improves | Flat with owned blocker | Flat and blocker ignored | Snapshot/delta path measures |
| Review and flow | Queue/WIP findings resolved | Corrective owner active | Known stall left unattended | Flow assessment, reviewer age |
| Honest state | Unworked gated/stale claims reconciled | Correction in progress | Started claim persists against evidence | Stale/merged-open assessment and tracker |
| Fix rounds | Current policy met | Excess has recorded remedy | Excess/repeating loop ignored | Round-policy assessment |
| Gate discipline | Focused iteration and one final lead gate | Justified exception recorded | Repeated workspace gates without new evidence | Classified checks and gate telemetry |
| Pin discipline | Required pins in consuming PR/window | Drift has owner | Repin-only churn continues | Pin assessment and dependency owner |
| Merge safety | Matched review/dispositions and reviewed head | Discrepancy corrected before merge | Open finding or unreviewed behavior merged | Tracker markers and PR head |
| One directory | Ticket shares one coder/reviewer/gate tree | Stray tree corrected | Separate review/gate worktrees | Worktree evidence |
| Resources | Current capacity/admission source honored | Missing telemetry routed | Slots invented or reservations bypassed | Host/queue/hold assessment |
| Agent recovery | Confirmed idle with ready work acted on | Remedy owned but pending | Confirmed idle remains unassigned | Complete lifecycle and ready queue |
| Delivery | Outcomes distinct; confirmation cited | Unconfirmed action escalated | Queued/seen claimed as completion | Pane/PR/SHA, relay receipt chain |

`WAITING` and `RECENT` are observed without nudging and do not fail recovery.
File ages, token totals and worker counts alone establish neither idle nor
capacity. Unknown or incomplete evidence remains `n/a`.

Read next: [strategies](strategies.md).
