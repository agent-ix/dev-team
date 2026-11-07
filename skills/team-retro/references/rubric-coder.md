# Coder rubric

Score each row 0, 1 or 2 and cite the evidence. Read a coder's work from its pull request and report and never by asking the coder.

| Check | 2 | 1 | 0 | Evidence |
|---|---|---|---|---|
| Size | Every pull request open or merged in the window is at or below `pr_oversize_lines` (`prs_oversize` counts open ones only; list merged ones with `gh pr list --state merged --json number,additions,deletions,mergedAt`) | One over, with the split recorded | One over with no split, or several over | `snapshot`, `gh pr list` |
| Scope | Changed files all belong to the ticket's requirement block | One unrelated file | Several, or a change in another lane's files | `gh pr view --json files` |
| Rounds | Merged after 2 review rounds or fewer | 3 or 4 | 5 or more | reviewer markers |
| Rework cause | Every finding fixed in a round has a `fixed` outcome in the next disposition round | One finding returned as `still-open` once | A finding returned as `still-open` twice | `reviewer-dispositions` markers |
| One directory | Worked only in the assigned directory | One stray directory, removed | Created a clone or worktree for review or gate | `local_paths` listing |
| Honest report | Report names what is done, what is not and what failed | Missing the failed item | Reports done while checks fail | pull request, gate log |
| Stalls | Every coder report on a pull request is timestamped after that pull request's last gate `finished_at` in the gate log | One report earlier than its gate's `finished_at` | Several | gate log, coder reports |

Read next: [strategies.md](strategies.md) entry "Split large pull requests".
