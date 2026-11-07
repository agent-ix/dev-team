# Strategies

Each strategy has a trigger, the action, and the measure that shows it worked. They come from retros of long-running lanes. Apply the one that matches an observed loop; do not apply them all.

| Strategy | Trigger | Action | Shows up in |
|---|---|---|---|
| Count the path | `path_closed` is 0 while merges continue, or no one can name what blocks the gates | Name the gate tickets, compute `path_remaining` from the blocker graph, staff the path first, and report path tickets closed instead of pull-request counts | `path_closed` rising |
| Freeze intake | `net_closed_minus_new` negative; lanes filing tickets faster than closing | Open a new ticket only for a path blocker or a main-breaker; record other findings as comments on the owning ticket; measure closed minus new | `intake_new` falling |
| One count | Two sources give different open counts | Pick one structured query, state it with every number, and tag every ticket with a project and milestone | `source_count_disagreement` 0 |
| Fix the graph | A lane reports a blocker edge that is wrong or missing | Run a seam pass (see [backlog-to-waves](../../team-planner/references/backlog-to-waves.md) step 3), correct the Linear edges to match the code, route other teams' needs to their owners as asks | fewer re-plans |
| Merge-out first | Many open pull requests, work waiting to land | Land the reviewed pull requests before starting new work; close their tickets against the merged change | `prs_ready_unmerged` 0 |
| Split large pull requests | `prs_oversize` above 0, rounds climbing | Split by area before review; one owner per area; stacked pull requests land in order | `prs_oversize` 0, `fix_rounds_max` falling |
| Tier the review | Review queue is the bottleneck | Spec-only changes get one review pass; code changes get one review round plus the disposition pass; no second reviewer | cycle p90 falling |
| One gate per pull request | `full_gates_max` above 2 | Run the full gate once at the final head; use focused checks for earlier rounds, re-pins and cross-repo checks | `full_gates_max` 2 or less |
| Delta-gate main | `main_red_incidents` above 0 | Check the combined tree before merging; merge only at the reviewed head; keep a control check of main | `main_red_minutes` 0 |
| Verify delivery | A lane idle after a message | Confirm the send reported queued, then confirm the lane resumed; never read an exit code as delivery | `messages_undelivered` 0 |
| Verify done | `path_closed_unverified` or `done_reopened` above 0 | Partial pull requests reference the ticket instead of closing it; count a ticket done only when its change is on the default branch | both 0 |
| Decide in lane | The same decision requested repeatedly | Make the call with a recorded reason; ask the user only for decisions that are theirs, once, with a recommendation | `decisions_open` 0 |
| One directory per ticket | `worktrees_prunable` or `disk_bytes` growing, duplicate clones | One worktree per ticket shared by coder, reviewer and gate; remove it at merge | `worktrees_prunable` 0 |
| Plan ahead with read-only agents | Seams found during coding | Before dispatch, run read-only design agents per cluster (state, build order, edge cases, dependency changes, undecided spec points, stale tickets) and apply their corrections to the graph | fewer reopened or re-ordered tickets |
