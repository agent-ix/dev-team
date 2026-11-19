# Coder rubric

Score each row 0, 1 or 2 and cite the evidence. Read a coder's work from its pull request and report and never by asking the coder.

| Check | 2 | 1 | 0 | Evidence |
|---|---|---|---|---|
| Size | Emitted size assessment meets configured policy | Excess has recorded split | Excess left without remedy | ix-board PR-size assessment |
| Scope | Changed files all belong to the ticket's requirement block | One unrelated file | Several, or a change in another lane's files | `gh pr view --json files` |
| Rounds | Emitted round assessment meets current policy | Excess has owned remedy | Excess ignored | ix-board round-policy assessment |
| Rework cause | Every finding fixed in a round has a `fixed` outcome in the next disposition round | One finding returned as `still-open` once | A finding returned as `still-open` twice | `reviewer-dispositions` markers |
| One directory | Worked only in the assigned directory | One stray directory, removed | Created a clone or worktree for review or gate | `local_paths` listing |
| Honest report | Report names what is done, what is not and what failed | Missing the failed item | Reports done while checks fail | pull request, gate log |
| Stalls | Every coder report on a pull request is timestamped after that pull request's last gate `finished_at` in the gate log | One report earlier than its gate's `finished_at` | Several | gate log, coder reports |

Read next: [strategies.md](strategies.md) entry "Split large pull requests".

Quantitative rows use supported ix-board measurements/assessments only. If a
requested count, rate or threshold comparison is not emitted, score it `n/a`;
do not reconstruct it by counting markers or PRs manually.
