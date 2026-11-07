# Code lead rubric

Score each row 0, 1 or 2 and cite the evidence. The code lead dispatches, verifies, merges and keeps the tracker true.

| Check | 2 | 1 | 0 | Evidence |
|---|---|---|---|---|
| Gate progress | `path_closed` rose since the last retro | Flat with a named blocker | Flat with no blocker | `delta` |
| Review queue | `prs_ready_unmerged` is 0 | 1 to 2 for one tick | Above 2, or any for two ticks | `snapshot` |
| Work in flight | `prs_open` at or below the lane cap and `prs_idle` is 0 | One idle pull request with a reason | Several idle, or no cap | `snapshot` |
| Pull-request size | `prs_oversize` is 0 | 1 with a split plan | More than 1 | `snapshot` |
| Fix rounds | `fix_rounds_max` is 2 or less | 3 or 4 | 5 or more | `snapshot` |
| Rework | `head_shas_per_pr_max` is 3 or less and `full_gates_max` is 2 or less | One exceeds | Both exceed | `snapshot` |
| Main health | `main_red_incidents` is 0 | 1 incident fixed inside the window | More than 1, or red longer than a gate cycle | `snapshot` |
| Merge safety | Every merge in the window was at the reviewed head | One mismatch, corrected | Merged at an unseen head | `gh pr view`, merge records |
| One directory per ticket | One worktree or clone per ticket, shared by coder, reviewer and gate | One duplicate, removed | Separate review clones | `worktrees_prunable`, `local_paths` listing |
| Resources | `orphan_slots` is 0 and `build_lock_wait_minutes` is not the longest part of a gate cycle | One of the two | Both | `snapshot` |
| Messages delivered | `messages_undelivered` is 0 and every lane message was acknowledged by work resuming | One undelivered message found and repeated | Idle lane after a message read as delivered | `snapshot`, pane state |
| Agents working | `agents_working_share` met the lane's staffing and idle minutes stayed under the idle threshold | One lane idle past the threshold | A lane idle with a ready ticket | `ix-board agents` |

Read next: [strategies.md](strategies.md) entries "Merge-out first", "Split large pull requests", "Delta-gate main", "Verify delivery".
