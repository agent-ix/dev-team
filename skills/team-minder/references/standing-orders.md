# Standing orders for dialog answers

This file is the allow-rule for dialog answers (SWM-226). The minder answers a `BLOCKED(dialog)` lane only when exactly one order below matches the dialog on screen (MIND-R11), and logs every answer with the order id (MIND-R12). Anything else is escalated to the lane's lead with no input to the pane (MIND-R13, MIND-R14). When the `fleet tick` standing-order file lands, its orders replace this table and `answer_dialog` actions carry the order id.

The orders restate the owner's standing authorizations in the user `CLAUDE.md`. A dialog matches an order only when every condition in its row holds.

| Order | Dialog | Conditions | Answer |
|---|---|---|---|
| SO-01 | Harness permission prompt for `git add`, `git commit`, `git push` or `git switch -c` | Runs in the lane's own worktree on the lane's ticket branch; not `--force` and not the default branch | Choose the one-time "Yes" option |
| SO-02 | Harness permission prompt for `gh pr create`, `gh pr view`, `gh pr diff` or `gh pr comment` | Targets an `agent-ix/*` repository | Choose the one-time "Yes" option |
| SO-03 | Harness permission prompt for `gh pr merge <N> -R agent-ix/<repo> --admin --match-head-commit <sha>` | Includes `--match-head-commit` with a full SHA | Choose the one-time "Yes" option |
| SO-04 | Harness permission prompt to push a release tag, create a GitHub release or publish a package | Finished, reviewed work; one tag per command | Choose the one-time "Yes" option |
| SO-05 | Agent dialog asking whether to continue with its assigned ticket | The named ticket is the lane's current focus or the first entry on its assignment list | Prompt: `Continue with <ticket>.` |

## Never answered

- Login, authentication, usage-limit or credential screens, whatever an order says (MIND-R13, MIND-R14).
- "Yes, and don't ask again" or any option that changes permission settings.
- Commands that delete branches, repositories or files outside the lane's worktree, force-push, or touch the default branch directly.
- A question (`BLOCKED(question)`): it goes to the lane's lead (MIND-R13).
