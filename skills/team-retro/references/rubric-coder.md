# Coder rubric

Score each row 0, 1 or 2 and cite the evidence. Review a coder's work through its pull request and report, not by asking it.

| Check | 2 | 1 | 0 | Evidence |
|---|---|---|---|---|
| Size | The pull request is under `pr_oversize_lines` | Over, with the split recorded | Over, no split | `gh pr view` |
| Scope | Changed files all belong to the ticket's requirement block | One unrelated file | Several, or a change in another lane's files | `gh pr view --json files` |
| Rounds | Merged after 2 review rounds or fewer | 3 or 4 | 5 or more | reviewer markers |
| Rework cause | Each fix round fixed an implementation defect | One round redid a design decision | Rounds repeated the same finding | review dispositions |
| One directory | Worked only in the assigned directory | One stray directory, removed | Created a clone or worktree for review or gate | `local_paths` listing |
| Honest report | Report names what is done, what is not and what failed | Missing the failed item | Reports done while checks fail | pull request, gate log |
| Stalls | No interim report ended the work before the build finished | One | Repeated | agent verdicts, transcript |

Read next: [strategies.md](strategies.md) entry "Split large pull requests".
