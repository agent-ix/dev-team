# Measures

`ix-board retro snapshot` computes these and `ix-board retro delta` compares them. The definitions, sources and counting rules are the requirements FR-024 to FR-028 in the ix-board specification; this file says how to read them.

## Reading the numbers

| Family | Metrics | What they tell you |
|---|---|---|
| progress | `path_remaining`, `path_closed`, `intake_new`, `net_closed_minus_new`, `gates_remaining`, `path_closed_unverified` | Whether the work that unblocks the gate tickets is finishing faster than new work arrives. The headline pair is `path_closed` and `net_closed_minus_new`. |
| flow | `prs_merged_per_hour`, `pr_cycle_median_hours`, `pr_cycle_p90_hours`, `prs_open`, `prs_idle`, `prs_oversize`, `prs_ready_unmerged` | How fast pull requests move. Read next to progress: high flow with no `path_closed` is activity that does not reach the gates. |
| rework | `fix_rounds_max`, `fix_rounds_total`, `head_force_pushes_max`, `done_reopened`, `full_gates_max`, `repins_total` | Work done twice: review rounds, force-pushed heads, reopened tickets, repeated gates and re-pins. |
| stability | `main_red_incidents`, `main_red_minutes` | How often and how long the default branch was broken. |
| scope | `issues_without_project`, `issues_without_milestone`, `in_progress_stale`, `source_count_disagreement`, `decisions_open`, `decision_oldest_hours` | Whether the plan is countable, owned and decided. |
| utilization | `agents_working_share`, `agents_idle_minutes_max`, `messages_undelivered` | Whether agents are working and whether messages reach them. |
| resource | `worktrees_prunable`, `disk_bytes`, `orphan_slots`, `build_lock_wait_minutes` | Whether disk, worktrees and build slots are the bottleneck. |

## Light-tick flags

Raise a flag only on the stated condition. The owner is the recipient.

| Flag | Condition | Owner |
|---|---|---|
| Busy without landing | `path_closed` is 0 and `prs_merged_per_hour` is above 0 in two consecutive ticks | planner |
| Intake outruns closure | `net_closed_minus_new` is negative in two consecutive ticks | planner |
| Uncountable plan | `issues_without_milestone` above 0 or `source_count_disagreement` above 0 | planner |
| False done | `path_closed_unverified` above 0 or `done_reopened` above 0 | code lead |
| Stalled review queue | `prs_ready_unmerged` above 0 in two consecutive ticks | code lead |
| Idle or oversize pull requests | `prs_idle` or `prs_oversize` above 0 and increasing | code lead |
| Main broken | `main_red_minutes` above 0 and rising | code lead |
| Undelivered messages | `messages_undelivered` above 0 | code lead |
| Idle agents | `agents_working_share` falling for two ticks | code lead |
| Waiting decisions | `decisions_open` above 0 with `decision_oldest_hours` rising | the user |
| Regressing metric | `delta` reports `regressing` for any metric | the family's owner from the table above |
| Data gap | a metric `unavailable` with reason `not configured` for three snapshots | the user (a configuration field is missing) |

A flag whose condition holds for the next tick is not sent again unless the numbers worsened. A tick is one scheduled run; two snapshots taken minutes apart count as one. A metric that is `unavailable` with reason `herdr unavailable` or `empty population` is not a data gap: the first is an outage to mention once, the second is a valid result.

## Owners

| Family | Owner |
|---|---|
| progress, scope | planner |
| flow, rework, stability, utilization, resource | code lead |
| a decision waiting on the owner | user |

## Reading `delta`

`since_previous` and `since_baseline` carry a `state`: `changed` (with `change`, which is 0 when the value did not move), `unavailable`, or `query_changed` (with both queries). `regressing` is true only after the metric moved against its direction in each of the latest two comparisons, which needs three snapshots with comparable queries; backfilled records never count toward it.

## Subjective scores

The rubrics score what counters cannot: 2 = meets the stated anchor with cited evidence, 1 = partly, 0 = fails or no evidence. Anchors are written so two reviewers reach the same score from the same evidence. Record the evidence next to the score; a score without evidence is 0.

## Baseline

The first record in the store is the baseline unless the configuration names `baseline_taken_at`. Give a team a baseline from its past window with `ix-board retro backfill --config <file> --since <date> --until <date>`, once, using the same `--window` as every later snapshot; a comparison between records taken with different windows or thresholds is reported as `query_changed` and carries no change value.

Backfill reconstructs `prs_merged_per_hour`, `pr_cycle_median_hours`, `pr_cycle_p90_hours`, `path_closed`, `intake_new`, `net_closed_minus_new` and `done_reopened`. The Linear metrics use today's path set and project membership, because the past blocker graph is not recorded. Every other metric is `unavailable` in a backfilled record, so changes since the baseline exist for those seven only until the team has a baseline snapshot of its own. Backfill refuses a range that contains a snapshot and skips days it already wrote.

A target is a range the team sets after at least one full retro, per project.
