# Churn retrospective

Run this at every work-cycle restart, after two merges, or after two hours of
active work, whichever comes first. Run it immediately if a gate, dependency
pin, merge hold or ruling repeats with no new evidence. Keep it short enough to
finish before dispatching the next round of the same work. A long-running PR
or a quiet window is a prompt to investigate, not proof of churn.

## Record and compare

In the team's existing state record, keep one row per active PR and a dated
retrospective below it. The state-record location remains the organization's
choice. A row names the owning Linear ticket, repository and PR, coder and
reviewer, current head SHA, the last reviewed SHA, and the dependency head (if
any). Update it at dispatch, gate completion, review/disposition, re-pin, head
change and merge, not from chat memory at retrospective time.

For the window since the last retrospective, record:

| Measure | Source and counting rule |
| --- | --- |
| Merges per active hour | Owned PRs merged in the window divided by lead active hours; also show the raw count. |
| Full gates per PR | Each aggregate gate start, with SHA, reason, duration and result. Count repeats on the same PR separately. |
| Fix rounds per PR | Each coder fix-round dispatch after a `/reviewer` finding or disposition. |
| Build-lock wait | Wait from requesting the lock to acquiring it, summed per PR; use the lock log or recorded timestamps. |
| Re-pins and dependency head moves | Count each consumer pin edit and each observed upstream head SHA change separately. Record the trigger. |
| Agent time per finding | Coder fix-round elapsed active time divided by findings addressed in that round; show numerator and denominator. Exclude recorded lock wait and other known idle time. |
| Messages per ruling | Count decision-request and answer messages needed to settle each ruling, and record whether it changed a dispatched brief. |

Compare each count and rate with the prior window using the same counting rule.
For a first window, write `baseline unavailable`. Mark a measure `unavailable`
when its source was not captured; do not turn missing lock or agent timing into
zero. Close with one sentence naming the observed progress and the repeating
step, or saying no repeating step was found. Record the next action and its
owner. Do not use a fixed throughput threshold across projects.

## Existing-command evidence

- Use `ix-board next --team <TEAM>` for the ready queue and `ix-board focus
  hygiene` / `focus plan-chunk` for the selected Linear focus. These answer
  order, blockers and hygiene, not PR rework or lock waits. `ix-board drift`
  needs a separate versioned evidence file and evaluates broader scope and
  ticket churn; it does not supply these per-PR measures.
- Use `gh pr list -R <owner/repo> --state merged --json number,mergedAt,url`
  for merge times and `gh pr view <N> -R <owner/repo> --json
  headRefOid,commits,mergedAt,url` for the current PR. Attribute a PR to the
  lead only from its ticket/state record, not the shared GitHub account. A
  current commit list cannot reconstruct every old head.
- When head churn matters, read the PR's paginated GitHub issue timeline with
  `gh api --paginate repos/<owner>/<repo>/issues/<N>/timeline`. Its
  `head_ref_force_pushed` events corroborate force pushes. Record ordinary
  observed head SHA changes at each dependency check in the state record;
  do not call a force-push count the total head-move count.
- Use `linear issue comment list <TICKET> --json` for the `/reviewer` and
  `reviewer-dispositions` markers. Their PR, reviewed SHA and round identify
  the real review sequence. GitHub review counts are not the source of record.
- Read each lane's gate log and the build-lock log for timestamps, head and
  result. If the lock script does not record request/acquisition times, have
  the coder record those two times in its report. Count re-pin edits and
  ruling messages from the state record and linked Linear or leader messages.

## Respond to a repeating loop

1. Stop new dispatches into that loop. Name the repeated step, what triggers
   it, and the work it prevents. Continue unrelated, unblocked planned work.
2. Apply a value test to **each** repeated gate, pin and hold: which changed
   input or failure risk will this action check, and what decision depends on
   its result? Remove a repeat that adds no evidence, within the lead's
   authority.
3. Compare the action with the repo's `CLAUDE.md`/`AGENTS.md` and the owner's
   instructions: full versus focused gates, findings inside the owning PR,
   and asynchronous cross-team progress unless a hold is explicitly required.
4. Make the smallest authorized change, record it and tell affected agents.
   Do not split findings into separate PRs or weaken a required merge gate.
5. If the cause is a cross-team protocol or owner-policy decision, ask the
   owner with the loop, before/after numbers, 2–4 viable options and a
   recommendation, one decision at a time. Hold the dependent loop while
   waiting; do not impose a new rule on another lead. Resume with the ruling
   recorded in the state record and the owning Linear ticket.

For piecemeal design rulings, collect the related open questions and their
dependencies before briefing an agent again. Ask the owner each required
decision separately, with the full shared context. Freeze only the dependent
brief until its rulings are stable. Route a ticket owned by another team to
that lead instead of repeatedly rewriting a local brief for it.

## Agent conflicts

Before dispatch and at each retrospective, compare every active agent's
ticket, branch, expected files and dependency head against live lanes and open
PRs. Check actual changed files with `gh pr view <N> -R <owner/repo> --json
files,headRefOid`. A shared branch has one pusher. If two lanes claim the same
files or requirement block, pause the later dispatch, identify the owning
ticket and give that owner the edit; resume the other lane only after its
scope no longer overlaps. If another lead owns the ticket, route the work to
that lead and keep the dependency visible in the state record. Reconcile
different head assumptions or incompatible rulings once before more re-pins,
gates or briefs. Escalate an unresolved cross-team ownership or protocol
choice to the owner with the competing claims and a recommendation.
