# Minder rubric

Rubric version: 1 (cited as `rubric-minder@1`; bump on any change to a check or its scoring). Checks are cited by the slug in the first column of the id list below the table.

Score 2/1/0 with cited judgment. Deterministic measurements come from ix-board;
missing or partial evidence scores `n/a` under Data quality.

| Check | 2 | 1 | 0 | Evidence |
|---|---|---|---|---|
| Loop alive | Scheduled observation confirmed | Late tick has remedy | Loop stopped without user direction | Scheduler evidence |
| Scope coverage | Every configured host/lane accounted for | Gap explicitly routed | Omitted remote lanes treated healthy | Configured scope and source coverage |
| Liveness | Pane lifecycle reconciled with movement/tokens | Conflict kept unknown | Legacy counts or relay seen treated as work | Verified pane/PR/worktree/token observations |
| Waiting/recent | Observed without nudges | Incorrect nudge corrected | Repeated nudge or unknown treated idle | Lifecycle provenance and actions |
| Login blocker | Verified auth screen routed this tick | Owner remedy pending | Login screen reported working | Verified pane and owned blocker |
| Overdue order | Configured deadline breach escalated this tick | Escalation lacks route, reported | Known overdue order ignored | Emitted overdue assessment and action |
| Confirmation | Actual pane/PR-head/SHA cited | Explicitly unconfirmed with owner | Enqueued/delivered claimed as acted on | Order confirmation record |
| Message hygiene | One actionable batch, no blind retry | Excess corrected | Repeated polls or duplicate sends | Attributed comms assessment |
| Failed probe | Every failed or timed-out source recorded as a defect and routed this tick | Defect recorded, route missing | Failed probe read as healthy or unreachable-and-fine | Source health rows and routed defects |

Check slugs: `loop-alive`, `scope-coverage`, `liveness`, `waiting-recent`, `login-blocker`, `overdue-order`, `confirmation`, `message-hygiene`, `failed-probe`.

Never infer zero from a missing worker field or recover a partial `IDLE` /
`WAITING-STUCK` row. Preserve the
[minder's lifecycle rollout contract](../../team-minder/SKILL.md#reading-worker-counts-during-rollout).
An unconfirmed order does not justify a blind resend or authentication approval.
Use configured acknowledgement policy; an absent policy remains unavailable.

Read next: [strategies](strategies.md).
