# Reviewer rubric

Score each row 0, 1 or 2 and cite the evidence.

| Check | 2 | 1 | 0 | Evidence |
|---|---|---|---|---|
| One reviewer | Exactly one distinct `run=` value across the `reviewer` markers of each pull request | One pull request had two | Several per pull request, or the author reviewed | `reviewer` markers (`run=`, `pr=`) |
| Record | Every reviewed pull request has a Linear marker comment carrying `id=`, `method=`, `pr=` and `run=` | A marker missing one of those fields | Review only on the pull request | `linear issue comment list <TICKET> --json` |
| Dispositions | Every finding's latest outcome is not `still-open` at merge | One open at merge with a recorded reason | Open at merge, no reason | disposition markers |
| Rounds to clean | Emitted round assessment meets current policy | Excess has owned remedy | Excess ignored | ix-board round-policy assessment |
| Findings quality | Every finding row names a file or line and a failure scenario | At most a third of rows lack one | More than a third lack one | review comments |
| Scope | Every finding's file is in the pull request's file list | One finding outside it | Several | `gh pr view --json files`, comments |
| Latency | Emitted review-age assessment meets policy | Breach has corrective owner | Known review stall ignored | ix-board reviewer-age/queue assessment |

Read next: [strategies.md](strategies.md) entries "Tier the review", "One gate per pull request".

Quantitative rows use supported ix-board measurements/assessments only. Missing
counts, rates, attribution or configured thresholds are `n/a`, not a reason to
count markers or findings by hand. Qualitative findings still cite their source.
