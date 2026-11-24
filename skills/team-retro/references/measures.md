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

Use emitted assessments, loop findings and `delta.regressing` only. Thresholds,
multi-snapshot predicates and availability streaks belong to ix-board, configured
per scope after its baseline. Do not calculate a flag from raw values here.
Older output without a requested flag is unavailable for that assessment;
report its valid raw metrics independently without inventing a color.

Read all ten classes in [Department evidence](department-health.md), including
flow/WIP, serial dependencies, pin/version churn, resources, liveness,
authority/policy, signal integrity, rework, decisions and communication. That
reference also covers planner audit counts and the three repeating-loop types.

Route progress/scope/planning findings to the planner, execution/rework findings
to the code lead, resource findings to their configured host/build owner, and
authority/decision findings to the configured decision owner. Use a returned
owner/action route when present; a missing route is unrouted, not permission to
assign another tab. Deduplicate unchanged conditions and batch new/worsened
findings once per owner/tick. Source outages and empty populations retain their
specific reasons instead of becoming performance failures.

`agents_working_share` is the share of reported agents classified `WORKING`
under the lifecycle query definition. `WAITING` and `RECENT` remain separate
states and contribute no execution to the numerator. A lower share can reflect
valid waiting or completed work; it does not establish idle agents or lower
productivity. Observe those states without nudging. Unknown classifications,
missing teams or relevant unavailable sources make the share unavailable.
Preserve the metric's availability and query; never reconstruct a share from
partial rows, worker counts or file ages.

Agent rows from `ix-board agents` carry worker counts. Prefer `active_direct_workers`;
a present `null` is unknown and never falls back to the deprecated `live_subagents`
alias. Nullable worker counts do not measure execution or spare slots. Older reports'
numeric `live_subagents` measures legacy recent-file evidence; its lifecycle count
remains unknown.

## Owners

| Family | Owner |
|---|---|
| progress, scope | planner |
| flow, rework, stability, utilization, resource | code lead |
| a decision waiting on the owner | user |

## Reading `delta`

`since_previous` and `since_baseline` carry a `state`: `changed` (with `change`, which is 0 when the value did not move), `unavailable`, or `query_changed` (with both queries). `regressing` is true only after the metric moved against its direction in each of the latest two comparisons, which needs three snapshots with comparable queries; backfilled records never count toward it.

The lifecycle execution-share query is versioned separately from the old
activity heuristic. A transition between them is `query_changed`, even with
identical windows and thresholds. Show both queries under Data quality and
suppress trend, regression and utilization flags across that boundary. Missing
or unsupported query provenance leaves the interpretation unknown. Keep old
records as recorded; do not relabel their values with the new definition.

## Subjective scores

The rubrics reserve 2/1/0 for cited judgment against their anchors. Quantitative
rows consume deterministic ix-board measurements/assessments, never transcript
counts or model arithmetic. Missing or unsupported evidence is `n/a` under Data
quality; it is not a failure or a clean score. Do not average role scores.

## Baseline

The first record in the store is the baseline unless the configuration names `baseline_taken_at`. Give a team a baseline from its past window with `ix-board retro backfill --config <file> --since <date> --until <date>`, once, using the same `--window` as every later snapshot; a comparison between records taken with different windows or thresholds is reported as `query_changed` and carries no change value.

Backfill reconstructs `prs_merged_per_hour`, `pr_cycle_median_hours`, `pr_cycle_p90_hours`, `path_closed`, `intake_new`, `net_closed_minus_new` and `done_reopened`. The Linear metrics use today's path set and project membership, because the past blocker graph is not recorded. Every other metric is `unavailable` in a backfilled record, so changes since the baseline exist for those seven only until the team has a baseline snapshot of its own. Backfill refuses a range that contains a snapshot and skips days it already wrote.

A target is a range the team sets after at least one full retro, per project.
