# Code lead rubric

Score each row 0, 1 or 2 and cite the evidence. The code lead dispatches, verifies, merges and keeps the tracker true.

| Check | 2 | 1 | 0 | Evidence |
|---|---|---|---|---|
| Gate progress | `path_remaining` fell since the last retro | Flat with a named blocker | Flat with no blocker | `delta` |
| Review queue | `prs_ready_unmerged` is 0 | 1 to 2 for one tick | Above 2, or any for two ticks | `snapshot` |
| Work in flight | `prs_open` at or below the lane cap the user stated for this team (record it in the retro file; ask once if none) and `prs_idle` is 0 | One idle pull request with a recorded reason | Several idle, or no cap stated | `snapshot` |
| Pull-request size | `prs_oversize` is 0 | 1 with a split plan | More than 1 | `snapshot` |
| Fix rounds | `fix_rounds_max` is 2 or less | 3 or 4 | 5 or more | `snapshot` |
| Rework | `head_force_pushes_max` is 1 or less and `full_gates_max` is 2 or less | One exceeds | Both exceed | `snapshot`; to name the pull request, read each timeline's `head_ref_force_pushed` events (`gh api --paginate repos/<owner>/<repo>/issues/<N>/timeline`) |
| Main health | `main_red_incidents` is 0 | 1 incident fixed inside the window | More than 1, or red longer than a gate cycle | `snapshot` |
| Merge safety | Every merge in the window carries a Linear review marker whose pull request matches and no commits were pushed after the last disposition | One mismatch, corrected | Merged with commits after the last disposition | `gh pr view --json commits,mergedAt`, disposition markers |
| One directory per ticket | `worktrees_prunable` is 0 and each ticket has one directory under the `local_paths` entry (`ls`) | One duplicate, removed | Separate review directories | `snapshot`, `ls` of `local_paths` |
| Resources | `orphan_slots` is 0 and `build_lock_wait_minutes` is not the longest part of a gate cycle | One of the two | Both | `snapshot` |
| Messages delivered | `messages_undelivered` is 0 and every lane message was acknowledged by work resuming | One undelivered message found and repeated | Idle lane after a message read as delivered | `snapshot`, pane state |
| Agent recovery | No confirmed idle agent left unassigned with ready work | One confirmed idle agent past the configured threshold | A confirmed idle agent left with a ready ticket | Complete `ix-board agents <team>` evidence, configured threshold, `ix-board next` |

Read next: [strategies.md](strategies.md) entries "Merge-out first", "Split large pull requests", "Delta-gate main", "Verify delivery".

`WAITING` and `RECENT` are observed without nudging and do not fail agent
recovery. File ages and worker counts alone cannot establish idle or capacity.
Unknown or incomplete evidence scores `n/a` and belongs under Data quality.
