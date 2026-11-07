# Reviewer rubric

Score each row 0, 1 or 2 and cite the evidence.

| Check | 2 | 1 | 0 | Evidence |
|---|---|---|---|---|
| One reviewer | Exactly one distinct `run=` value across the `reviewer` markers of each pull request | One pull request had two | Several per pull request, or the author reviewed | `reviewer` markers (`run=`, `pr=`) |
| Record | Every reviewed pull request has a Linear marker comment carrying `id=`, `method=`, `pr=` and `run=` | A marker missing one of those fields | Review only on the pull request | `linear issue comment list <TICKET> --json` |
| Dispositions | Every finding's latest outcome is not `still-open` at merge | One open at merge with a recorded reason | Open at merge, no reason | disposition markers |
| Rounds to clean | Clean after 2 rounds or fewer | 3 or 4 | 5 or more | markers |
| Findings quality | Every finding row names a file or line and a failure scenario | At most a third of rows lack one | More than a third lack one | review comments |
| Scope | Every finding's file is in the pull request's file list | One finding outside it | Several | `gh pr view --json files`, comments |
| Latency | `prs_ready_unmerged` is 0 and each marker was posted before the pull request was idle for `pr_idle_hours` | One pull request waited past it once | Several, or `prs_ready_unmerged` above 0 for two ticks | `snapshot`, marker times |

Read next: [strategies.md](strategies.md) entries "Tier the review", "One gate per pull request".
