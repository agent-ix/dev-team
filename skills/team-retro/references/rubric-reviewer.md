# Reviewer rubric

Score each row 0, 1 or 2 and cite the evidence.

| Check | 2 | 1 | 0 | Evidence |
|---|---|---|---|---|
| One reviewer | Exactly one reviewer per pull request | One had two | Several per pull request, or the author reviewed | `reviewer` markers |
| Record | Every review has a Linear marker comment with SR id, `pr=`, reviewed head | A marker missing a field | Review only on the pull request | `linear issue comment list` |
| Dispositions | Every finding's latest outcome is not `still-open` at merge | One open at merge with a recorded reason | Open at merge, no reason | disposition markers |
| Rounds to clean | Clean after 2 rounds or fewer | 3 or 4 | 5 or more | markers |
| Findings quality | Each finding names file, line and a failure scenario | Some lack the scenario | Findings without evidence | review comments |
| Scope | Reviewed the diff only | One out-of-diff finding | Reviewed the tree | markers, comments |
| Latency | Review posted within the lane's expected cycle | Late once | A pull request waited on review past the idle threshold | `prs_ready_unmerged`, markers |

Read next: [strategies.md](strategies.md) entries "Tier the review", "One gate per pull request".
