# Standing orders for dialog and queued-question answers

This file is the allow-rule for dialog and queued-question answers (SWM-226). The minder answers a lane only when exactly one order below matches what is on screen (MIND-R11), and logs every answer with the order id (MIND-R12). Everything else goes to the lane's lead, and the minder sends nothing to the pane (MIND-R13, MIND-R14). When the `fleet tick` standing-order file lands (SWM-256), its orders replace this table and `answer_dialog` actions carry the order id.

The orders restate the owner's standing authorizations in the user `CLAUDE.md`. A dialog or queued question matches an order only when every condition in its row holds. Conditions marked *tracker* are checked in Linear or GitHub, not on the screen; if the check cannot be made, the order does not match.

| Order | Applies to | Prompt | Conditions | Answer |
|---|---|---|---|---|
| SO-01 | `BLOCKED(dialog)` | Harness permission prompt for `git add`, `git commit`, `git push` or `git switch -c` | Runs in the lane's own worktree on the lane's ticket branch; not `--force` and not the default branch | Choose the one-time "Yes" option |
| SO-02 | `BLOCKED(dialog)` | Harness permission prompt for `gh pr create`, `gh pr view`, `gh pr diff` or `gh pr comment` | Targets an `agent-ix/*` repository | Choose the one-time "Yes" option |
| SO-03 | `BLOCKED(dialog)` | Harness permission prompt for `gh pr merge <N> -R agent-ix/<repo> --admin --match-head-commit <sha>` | *Tracker:* the ticket's latest reviewer dispositions leave no open finding, and the PR's current head (`gh pr view <N> --json headRefOid`) equals the full SHA passed to `--match-head-commit` | Choose the one-time "Yes" option |
| SO-04 | `BLOCKED(dialog)` | Harness permission prompt to push a release tag, create a GitHub release or publish a package | One tag per command. *Tracker:* the release's PR is merged and reviewed, and the tag is the next version after the repository's latest tag (`git ls-remote --tags` or `gh release list`) | Choose the one-time "Yes" option |
| SO-05 | `BLOCKED(question)` with relay reason `queued_question` only | A queued follow-up input (Codex "Queued follow-up inputs") asking whether to continue with an assigned ticket | The named ticket is the lane's current `focus` or the first entry on its assignment list | Prompt: `Continue with <ticket>.` |

## Never answered

- Login, authentication, usage-limit or credential screens, whatever an order says (MIND-R13, MIND-R14).
- "Yes, and don't ask again" or any option that changes permission settings.
- Commands that delete branches, repositories or files outside the lane's worktree, force-push, or touch the default branch directly.
- A free-form question (`BLOCKED(question)` with relay reason `question`): it goes to the lane's lead (MIND-R13). SO-05 never applies to it.
