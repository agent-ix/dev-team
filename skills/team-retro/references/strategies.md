# Strategies

Each strategy has a trigger, an owned action and an outcome to inspect. Use
emitted ix-board flags/assessments for quantitative triggers below; never compute
a missing trigger from raw values. Thresholds and review policy come from current
scope configuration. Apply only the strategy that matches supported evidence.

| Strategy | Trigger | Action | Shows up in |
|---|---|---|---|
| Count the path | Emitted busy-without-landing finding | Name gates, read the ix-board blocker path and staff it first | Emitted path-progress improvement |
| Freeze intake | `net_closed_minus_new` negative; lanes filing tickets faster than closing | Open a new ticket only for a path blocker or a main-breaker; record other findings as comments on the owning ticket; measure closed minus new | `intake_new` falling |
| One count | Two sources give different open counts | Pick one structured query, state it with every number, and tag every ticket with a project and milestone | `source_count_disagreement` 0 |
| Fix the graph | A lane reports a blocker edge that is wrong or missing | Run a seam pass (see [backlog-to-waves](../../team-planner/references/backlog-to-waves.md) step 3), correct the Linear edges to match the code, route other teams' needs to their owners as asks | fewer re-plans |
| Merge-out first | Many open pull requests, work waiting to land | Land the reviewed pull requests before starting new work; close their tickets against the merged change | `prs_ready_unmerged` 0 |
| Split large pull requests | `prs_oversize` above 0, rounds climbing | Split by area before review; one owner per area; stacked pull requests land in order | `prs_oversize` 0, `fix_rounds_max` falling |
| Tier the review | Emitted review bottleneck | Apply current authorized review policy with one reviewer; fix findings in original PR | Comparable cycle-time trend |
| One gate per pull request | Emitted repeated-gate breach | Lead runs the full gate once at final head; use focused checks for iteration | Gate-policy assessment resolved |
| Delta-gate main | `main_red_incidents` above 0 | Check the combined tree before merging; merge only at the reviewed head; keep a control check of main | `main_red_minutes` 0 |
| Verify delivery | Emitted overdue-order finding | Escalate this tick; distinguish enqueue/delivery/ack and confirm by pane, PR head or SHA; never blindly resend | Owned confirmation or explicit blocker |
| Verify done | `path_closed_unverified` or `done_reopened` above 0 | Partial pull requests reference the ticket instead of closing it; count a ticket done only when its change is on the default branch | both 0 |
| Decide in lane | The same decision requested repeatedly | Make the call with a recorded reason; ask the user only for decisions that are theirs, once, with a recommendation | `decisions_open` 0 |
| One directory per ticket | `worktrees_prunable` or `disk_bytes` growing, duplicate clones | One worktree per ticket shared by coder, reviewer and gate; remove it at merge | `worktrees_prunable` 0 |
| Plan ahead with read-only agents | Seams found during coding | Before dispatch, run read-only design agents per cluster (state, build order, edge cases, dependency changes, undecided spec points, stale tickets) and apply their corrections to the graph | fewer reopened or re-ordered tickets |
