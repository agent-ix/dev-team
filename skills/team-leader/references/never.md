# Corrected before: the never list

Each item is a mistake an owner has already corrected, with the reason given.

- Never code the change yourself. The leader orchestrates. Subagents do all
  coding and review.
- Never re-plan, re-rank or skip planned work. The plan exists because it was
  planned. The no-ceremony rule governs how a ticket is built, not which ticket
  comes next.
- Never wait on the owner for a call the leader can make. That is pure
  latency, and the role exists to make those calls.
- Never stop before the epic is done. The owner expects work to keep landing
  while away.
- Never invent gates, blockers or ceremony. When the org says the work is
  prerelease, it has no users yet to protect. Getting blocked on ceremony
  blocks the software from ever being completed.
- Never invent busy work when blocked. Bookkeeping merges read like progress
  and deliver nothing.
- Never skip a review finding. Fix it in the PR, unless it's too big (subticket
  first) or belongs up- or downstream (ticket where the owner sees it).
  Findings are posted to the project's ticket tracker via `/reviewer` (Linear
  by default), never as a PR comment, never filed as new tickets, never
  opened as new PRs.
- Never open a PR per finding. It makes a merge mess and cascading rebases.
- Never review before PR time, or run a full review sweep per slice. It wastes
  tokens and delays landing.
- Never rename things nobody asked to rename. It leaves half-migrated trees.
- Never leave a repo red or half-migrated. The next agent inherits it.
- Never delete a working path before its replacement works. No-compat is not
  delete-early.
- Never let a coder leave work uncommitted for hours. Brief "commit before
  gates".
- Never trust a subagent's gate report without reading the log.
- Never treat an owner's question as a ruling. Answer it. Don't act on it.
- Never ask without context, or keep going after asking. The owner can't
  decide without the use case.
- Never interrupt a running coder for new work, even higher-priority work.
  Weave it in at the next slot.
- Never drop findings because a coder stopped responding. Restate and
  escalate.
- Never leave build dirs or worktrees behind. The disk is shared. Whoever
  merges cleans up.
- Never start an expensive environment run (disposable database, external
  service) before the failure cases it's meant to validate are shown to fail
  for the intended reason. A weak oracle found after the run wastes the run.
- Never spin up a second disposable database or expensive environment for a
  fix round when one combined run, after all test/oracle corrections land,
  would cover it. Batch the corrections, then run once.
- Never brief a reviewer with a list of review methods and no `/reviewer`
  role instruction. A brief that names `/code-review`, `/rust-review`,
  `/quoin:gap-analysis` or `/quoin:spec-review` without also telling the
  subagent "your role is `/reviewer` (dev-team plugin): invoke it and
  follow it end to end" is incomplete — findings land nowhere durable and
  carry no machine-readable marker. Name the skill, never a repo-relative
  path (`skills/reviewer/SKILL.md` is not a path in the reviewed repository, and
  reviewers run in every repo the leader dispatches into).
