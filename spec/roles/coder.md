---
id: CODE
role: coder
version: 3
type: RoleSpec
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-017
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-024
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-029
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-033
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-039
    type: depends_on
---
# Role spec: coder

## Purpose

The coder turns one assigned ticket, or one batch of like tickets, into one
frozen pull request: spec change first when no requirement owns the behavior,
then code and tests, in the one worktree the ticket has. It runs focused checks,
opens the pull request, reports once, and fixes every review finding in the same
pull request. The role covers both a coder subagent that a
[code lead](code-lead.md) dispatches and a coding lane session that takes up an
assigned ticket chain. The coder does not review its own work, run the aggregate
gate or merge: the [reviewer](reviewer.md) reviews and the code lead gates and
merges.

Builds use the PATH `cargo` shim or
`locked-build run --class <must-fix|point|block|periodic> -- cargo ...`.
In `lease_accounted` mode, admission sums active lease caps with the requested
cap against the configured memory budget, and enforces each running lease at
its cap.

Targets are initial values. The evaluator's role rows (dev-team FR-008) show
whether a target is met and whether a rule moves its objective; the director
proposes changes through a role spec version bump.

## Query sources and producers

A query reference is `<source>.<name>`, an evaluator query that
`ix-board retro eval` (SWM-221) registers. The source prefix names the store the
query reads: `retro` (the ix-board retro catalog, ix-board FR-024, or
department report, ix-board FR-029), `prom` (series of the ix-board team
exporter, ix-board FR-033; `prom.ix_team_<name>` is the series
`ix_team_<name>`), `ledger` (the fleet ledger, ix-board FR-039), `github` (pull
request records), `linear` (tracker history and the marker comments of
[FR-017](../functional/FR-017-role-evaluation-records.md)), `hooks` (hook
activity events, ix-relay FR-068) and `transcript` (the evaluated session's
transcript, read with the terms of FR-017).

Terms such as finding, waived, report and send are those of FR-017. Counts are
over the evaluation window and the team's scope unless a rule says otherwise.
`retro` and `prom` values cover a team, not one session: a role row uses the
value, and a session row is `unavailable` unless the scope and window hold
exactly one session of this role (dev-team FR-001, FR-008). A value whose
configuration is absent is `unavailable`.

The Producer column states what exists on ix-board `origin/main`: `computed`
means ix-board computes the value today and only its registration as an
evaluator query is open; `specified` means an ix-board requirement defines the
query, or the stored rows or series it reads, and no code returns the query;
`none` means no ix-board requirement defines it.

| Query | Source and fields | Counting rule | Producer |
|---|---|---|---|
| retro.fix_rounds_max | tracker marker first lines | As ix-board FR-024: highest disposition `round=` on one pull request open or merged in the window | computed (ix-board FR-024) |
| retro.prs_oversize | GitHub open pull requests, `pr_oversize_lines` | As ix-board FR-024: open pull requests whose added plus deleted lines exceed the threshold | computed (ix-board FR-024) |
| retro.prs_open | GitHub open pull requests | As ix-board FR-024 | computed (ix-board FR-024) |
| retro.review_round_policy_excess | department report | As ix-board FR-029: pull requests above the configured review round limit | computed (ix-board FR-029) |
| prom.ix_team_review_prs_with_findings_share_24h | exporter series | As ix-board FR-033: share of classifiable reviewed pull requests with at least one finding | computed (ix-board FR-033) |
| ledger.lane_orders_due | `order_focus_at_deadline`: `order_id`, `lane`, `deadline_at`, `outcome`; relay order send time | Rows for the evaluated lane with `deadline_at` in the window, leaving out an order when a later order to the lane was sent before its `deadline_at` | specified (ix-board FR-039; rows are not yet written) |
| ledger.lane_orders_not_taken_up | same rows | Rows of `ledger.lane_orders_due` with `outcome` `acted_not_focused` or `ack_expired`; `timed_out`, never delivered, is left out | specified (ix-board FR-039; rows are not yet written) |
| github.authored_prs | GitHub pull requests; transcript `git push` and `gh pr create` calls | Pull requests the session opened or pushed to in the window | none |
| github.ticket_start_to_pr_open_median_hours | tracker state history; GitHub `createdAt` | Over pull requests created in the window with a ticket: hours from the ticket's first entry into a started state to `createdAt`, median; a pull request created before that entry is left out | none |
| github.second_prs_during_review | GitHub pull requests: repository, ticket, `createdAt`, close time; `reviewer` comments | Pull requests created in the window while another pull request of the same repository and ticket was open and already had a `reviewer` comment | none |
| linear.fix_round_findings | marker data blocks | Findings first recorded in the window on pull requests open or merged in the window | none |
| linear.fix_round_findings_returned_still_open | `dispositions` rows and `new_findings` | Rows with outcome `still-open` created in the window on those pull requests, once per finding and round, leaving out a finding first listed in the `new_findings` of that round | none |
| hooks.role_turns | hook prompt events | Turns of the evaluated session in the window | none |
| transcript.coder_reports | sends | The session's coder reports | none |
| transcript.coder_extra_trees | tool calls: command, working directory | Commands matching `git worktree add` or `git clone` for the repository of a pull request the session pushed to, whose target path is not the tree it pushed from | none |
| transcript.coder_aggregate_gate_runs | tool calls: command; `eval.gate_commands` | Commands matching `team-gate gate` or a gate command of the repository, leaving out pull requests waived for CODE-R10 | none |
| transcript.coder_merge_commands | tool calls: command | Commands matching `gh pr merge`, and `git push` commands whose destination is the default branch | none |
| transcript.coder_unrequested_pushes | tool calls and incoming messages: command, sender, time | `git push` commands to a pull request branch made after a report with no incoming message from the dispatcher between the latest report and the push, leaving out pull requests waived for CODE-R12 | none |
| transcript.outbound_messages | sends | The session's sends | none |

## Metrics

| ID | Name | Evidence source | Query | Unit | Target | Direction |
|---|---|---|---|---|---|---|
| CODE-M01 | Start-to-pull-request time, median: ticket entering its started state to its pull request opening | github | github.ticket_start_to_pr_open_median_hours | hours | 4 | lower |
| CODE-M02 | Share of reviewed pull requests with at least one finding, 24 hours | ix-board-metric | prom.ix_team_review_prs_with_findings_share_24h | ratio | 0.5 | lower |
| CODE-M03 | Rework rounds: most fix rounds on one pull request | ix-board-metric | retro.fix_rounds_max | rounds | 2 | lower |

## Objectives

| ID | Objective | Metrics |
|---|---|---|
| CODE-O01 | An assigned ticket reaches a reviewable pull request quickly | CODE-M01 |
| CODE-O02 | A coded pull request lands with little rework | CODE-M02, CODE-M03 |

## Rules

| ID | Rule | Objective | Class | Source |
|---|---|---|---|---|
| CODE-R01 | The coder SHALL work only in the one worktree its brief names, creating no other worktree or clone of the repository for the ticket. | CODE-O02 | duplicate-worktree | Rubric row One directory; one worktree per ticket (spec.md section 15) |
| CODE-R02 | Every file the coder's pull request changes SHALL belong to the assigned ticket's scope. | CODE-O02 | scope-creep | Rubric row Scope; changes in another lane's files |
| CODE-R03 | When the team has configured a pull request size limit, the coder SHALL split a change of a Point or Batch above it before review, and, unless the task, ticket, project or owner instruction says otherwise (LEAD-R22), SHALL NOT split a Block. | CODE-O02 | oversize-pr | Rubric row Size; strategy "Split large pull requests" |
| CODE-R04 | The coder's pull request SHALL reach a clean review within the current review round policy. | CODE-O02 | round-excess | Rubric row Rounds |
| CODE-R05 | The coder SHALL fix every finding sent in a fix round, other than one it reports as too big for the pull request or owned by another repository or lane. | CODE-O02 | unfixed-finding | Rubric row Rework cause; coder skill fix rounds |
| CODE-R06 | The coder SHALL NOT open a second pull request for a finding on its open pull request. | CODE-O02 | finding-split-off | A pull request per finding caused merge mess and cascading rebases, code-lead never list |
| CODE-R07 | The coder SHALL NOT report its work done while a check it ran fails. | CODE-O02 | false-done | Rubric row Honest report; subagents quoted gate output they never ran |
| CODE-R08 | The coder's report SHALL name everything it did not complete, failed checks included. | CODE-O02 | incomplete-report | Rubric row Honest report |
| CODE-R09 | The coder SHALL NOT send a report before the checks it cites have finished. | CODE-O02 | early-report | Rubric row Stalls |
| CODE-R10 | Unless a repository or organization rule requires it, the coder SHALL NOT run the repository's aggregate gate before review or during a fix round. | CODE-O01 | repeated-gate | Repeated workspace gates without new evidence, code-lead churn retrospective |
| CODE-R11 | The coder SHALL NOT merge a pull request. | CODE-O02 | unauthorized-merge | Coder skill role boundary: the code lead verifies and merges |
| CODE-R12 | The coder SHALL NOT push to a reported pull request branch unless its dispatcher has since sent it work on that branch: a fix round or an overlap rebase. | CODE-O02 | frozen-diff-changed | A branch changed mid-review leaves the reviewed diff stale, code-lead freeze step |
| CODE-R13 | A coder running as a fleet lane SHALL take up the exact ticket its latest order expects by the order's deadline. | CODE-O01 | order-not-taken-up | Queued relay orders treated as delivered, MONITORING-DESIGN |
| CODE-R14 | The coder SHALL NOT send a message other than done, blocked, decision, handoff or the one-line etiquette reply. | CODE-O01 | comms-noise | Status polls and progress messages between lanes, coder skill Communication |
| CODE-R15 | The coder SHALL NOT open a new ticket for a finding on its open pull request. | CODE-O02 | finding-deferred | Findings filed as new tickets, code-lead never list |
| CODE-R16 | The coder SHALL NOT commit reviewer SR files into the pull request. | CODE-O02 | review-file-churn | Review-file commits moved heads and reran checks, 2026-11-26 |

## Evaluations

| ID | Rule | Evidence source | Trigger | Method | Query or rubric | Evaluator | Comparator | Value | Unit | Cadence |
|---|---|---|---|---|---|---|---|---|---|---|
| CODE-R01-E1 | CODE-R01 | transcript | hooks.role_turns | deterministic | transcript.coder_extra_trees | evaluator | = | 0 | trees | session-end |
| CODE-R01-E2 | CODE-R01 | transcript | github.authored_prs | judgement | rubric-coder@2#one-directory | team-retro | >= | 2 | score | daily |
| CODE-R02-E1 | CODE-R02 | github | github.authored_prs | judgement | rubric-coder@2#scope | team-retro | >= | 2 | score | daily |
| CODE-R03-E2 | CODE-R03 | github | github.authored_prs | judgement | rubric-coder@2#size | team-retro | >= | 2 | score | daily |
| CODE-R04-E1 | CODE-R04 | ix-board-metric | github.authored_prs | deterministic | retro.review_round_policy_excess | evaluator | = | 0 | pull_requests | 3h |
| CODE-R04-E2 | CODE-R04 | linear | github.authored_prs | judgement | rubric-coder@2#rounds | team-retro | >= | 2 | score | daily |
| CODE-R05-E1 | CODE-R05 | linear | linear.fix_round_findings | deterministic | linear.fix_round_findings_returned_still_open | evaluator | = | 0 | findings | 3h |
| CODE-R05-E2 | CODE-R05 | linear | linear.fix_round_findings | judgement | rubric-coder@2#rework-cause | team-retro | >= | 2 | score | daily |
| CODE-R06-E1 | CODE-R06 | github | github.second_prs_during_review | judgement | rubric-coder@2#finding-pull-request | team-retro | >= | 2 | score | daily |
| CODE-R07-E1 | CODE-R07 | transcript | github.authored_prs | judgement | rubric-coder@2#false-done | team-retro | >= | 2 | score | daily |
| CODE-R08-E1 | CODE-R08 | transcript | github.authored_prs | judgement | rubric-coder@2#honest-report | team-retro | >= | 2 | score | daily |
| CODE-R09-E1 | CODE-R09 | transcript | github.authored_prs | judgement | rubric-coder@2#report-timing | team-retro | >= | 2 | score | daily |
| CODE-R10-E1 | CODE-R10 | transcript | hooks.role_turns | deterministic | transcript.coder_aggregate_gate_runs | evaluator | = | 0 | runs | session-end |
| CODE-R11-E1 | CODE-R11 | transcript | hooks.role_turns | deterministic | transcript.coder_merge_commands | evaluator | = | 0 | commands | session-end |
| CODE-R12-E1 | CODE-R12 | transcript | transcript.coder_reports | deterministic | transcript.coder_unrequested_pushes | evaluator | = | 0 | pushes | session-end |
| CODE-R13-E1 | CODE-R13 | ledger | ledger.lane_orders_due | deterministic | ledger.lane_orders_not_taken_up | evaluator | = | 0 | orders | 3h |
| CODE-R14-E1 | CODE-R14 | transcript | transcript.outbound_messages | judgement | rubric-coder@2#comms | team-retro | >= | 2 | score | daily |
| CODE-R15-E1 | CODE-R15 | linear | linear.fix_round_findings | judgement | rubric-coder@2#finding-ticket | team-retro | >= | 2 | score | daily |
| CODE-R16-E1 | CODE-R16 | github | github.authored_prs | judgement | rubric-coder@2#review-files | team-retro | >= | 2 | score | daily |

## Rubric mapping

Each row of the former team-retro coder rubric maps to rules here and to a check
of [rubric-coder](../rubrics/rubric-coder.md). The `comms` check grades the
coder skill's Communication section, which had no row.

| Rubric row | Rules | Checks |
|---|---|---|
| Size | CODE-R03 | size |
| Scope | CODE-R02 | scope |
| Rounds | CODE-R04 | rounds |
| Rework cause | CODE-R05, CODE-R06, CODE-R15 | rework-cause, finding-pull-request, finding-ticket |
| Review files | CODE-R16 | review-files |
| One directory | CODE-R01 | one-directory |
| Honest report | CODE-R07, CODE-R08 | false-done, honest-report |
| Stalls | CODE-R09 | report-timing |

## Evaluation notes

- Judgement-only rules, graded by team-retro and flagged under dev-team FR-006:
  CODE-R02 (ticket scope), CODE-R06 (whether a second pull request is for a
  finding), CODE-R07 (whether a report claims done), CODE-R08
  (report completeness), CODE-R09 (which checks a report cites), CODE-R14
  (message kind) and CODE-R15 (whether a ticket is for a finding). Each depends
  on the meaning of prose, which no recorded fact states.
- CODE-R03 is judgement-only: a deterministic oversize count cannot see the
  work class, so it would count a Block. This is an interim gap until ix-board
  can exclude a Block from `retro.prs_oversize`. The judgement check
  `size` separates a recorded split from an ignored one.
- CODE-R05-E1 counts a finding once for each round that returned it still-open.
  A finding the coder reports as too big or owned elsewhere gets a `deferred`
  outcome, which is not counted.
- CODE-R09 replaces the former Stalls anchor, which compared a report with the
  gate log. The code lead runs the aggregate gate after review, so the coder's
  report is compared with the checks it cites.
- CODE-R13 is `n.a.` for a dispatched subagent, which receives a brief and no
  relay order. An order that was never delivered is not counted against the
  coder.
