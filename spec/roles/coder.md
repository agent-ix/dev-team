---
id: CODE
role: coder
version: 1
type: RoleSpec
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
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

Targets are initial values. The evaluator's role rows (dev-team FR-008) show
whether a target is met and whether a rule moves its objective; the director
proposes changes through a role spec version bump.

## Query sources and producers

A query reference is `<source>.<name>`, an evaluator query that
`ix-board retro eval` (SWM-221) registers. The source prefix names the store the
query reads:

- `retro`: the ix-board retro record. `retro.<id>` is the metric of that id in
  the retro catalog (ix-board FR-024) or the department catalog (ix-board
  FR-029).
- `prom`: series the ix-board team exporter serves (ix-board FR-033);
  `prom.ix_team_<name>` is the series `ix_team_<name>`.
- `ledger`: the fleet ledger (ix-board FR-039).
- `github`: pull request records, pushes and merge state.
- `linear`: tracker state history and the `reviewer` and `reviewer-dispositions`
  markers and data blocks that the reviewer posts.
- `hooks`: hook activity events (ix-relay FR-068) of the evaluated session.
- `transcript`: the evaluated session's transcript, read by a fixed pattern
  query.

`retro` and `prom` values cover a team's scope and window, not one session. A
role row uses the value; a session row is `unavailable` unless the scope and
window hold exactly one session of this role (dev-team FR-001, FR-008). A
department or exporter value whose configuration is absent is `unavailable`.

The Producer column states what exists on ix-board `origin/main`: `computed`
means ix-board computes the value today and only its registration as an
evaluator query is open (SWM-221); `specified` means an ix-board requirement
defines it and no code computes it; `none` means no ix-board requirement defines
it, and the named ticket owns the producer.

| Query | Counts | Producer |
|---|---|---|
| retro.fix_rounds_max | Highest reviewer disposition round on one pull request open or merged in the window | computed (ix-board FR-024) |
| retro.prs_oversize | Open pull requests whose added plus deleted lines exceed `pr_oversize_lines` | computed (ix-board FR-024) |
| retro.prs_open | Open pull requests in the configured repositories | computed (ix-board FR-024) |
| retro.review_round_policy_excess | Pull requests above the configured review round limit | computed (ix-board FR-029) |
| prom.ix_team_review_prs_with_findings_share_24h | Share of classifiable reviewed pull requests in 24 hours that had at least one finding | computed (ix-board FR-033) |
| ledger.lane_orders_due | `order_focus_at_deadline` rows addressed to the evaluated lane | none (SWM-261); the table is specified in ix-board FR-039 |
| ledger.lane_orders_acted_not_focused | Rows of `ledger.lane_orders_due` with outcome `acted_not_focused` | none (SWM-261) |
| github.authored_prs | Pull requests the evaluated session opened or pushed to in the window | none (SWM-261) |
| github.ticket_start_to_pr_open_median_hours | Median hours from a ticket entering its started state to its pull request opening, over pull requests opened in the window | none (SWM-261) |
| linear.fix_round_findings | Findings sent back to the coder: findings in `reviewer` data blocks on the coder's pull requests with `clean: false` | none (SWM-261) |
| linear.fix_round_findings_returned_still_open | Disposition rows with outcome `still-open` on the coder's pull requests, one per finding and round | none (SWM-261) |
| hooks.role_turns | Turns of the evaluated session in the window | none (SWM-221) |
| transcript.coder_reports | Reports the session sent to its dispatcher | none (SWM-221) |
| transcript.coder_done_reports | Reports of `transcript.coder_reports` that state the work is done | none (SWM-221) |
| transcript.coder_worktree_or_clone_creations | `git worktree add` or `git clone` commands that create a second tree of the ticket's repository | none (SWM-221) |
| transcript.coder_pr_or_ticket_creations_in_fix_round | Pull requests or tickets the session created after a fix-round message and before its next report | none (SWM-221) |
| transcript.done_reports_with_failing_check | Done reports whose latest run of a check the session ran exited nonzero | none (SWM-221) |
| transcript.reports_before_cited_check_finished | Reports sent while a check they cite had not returned an exit status | none (SWM-221) |
| transcript.coder_aggregate_gate_runs | Runs of the repository's aggregate gate by the coder session | none (SWM-221) |
| transcript.coder_merge_commands | Pull request merge commands, or pushes to the default branch | none (SWM-221) |
| transcript.coder_pushes_to_frozen_branch | Pushes to a reported pull request branch with no fix-round message since that report | none (SWM-221) |
| transcript.outbound_messages | Messages the session sent to another agent | none (SWM-221) |
| transcript.messages_outside_allowed_kinds | Outbound messages that are not done, blocked, decision, handoff or the one-line etiquette reply | none (SWM-221) |

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
| CODE-R03 | The coder SHALL split a change above the configured pull request size limit before review. | CODE-O02 | oversize-pr | Rubric row Size; strategy "Split large pull requests" |
| CODE-R04 | The coder's pull request SHALL reach a clean review within the current review round policy. | CODE-O02 | round-excess | Rubric row Rounds |
| CODE-R05 | The coder SHALL fix every finding sent in a fix round, so that the next disposition round returns none of them still-open. | CODE-O02 | unfixed-finding | Rubric row Rework cause |
| CODE-R06 | The coder SHALL NOT open a new pull request or ticket for a finding on its open pull request. | CODE-O02 | finding-deferred | A pull request per finding caused merge mess and cascading rebases, code-lead never list |
| CODE-R07 | The coder SHALL NOT report its work done while a check it ran fails. | CODE-O02 | false-done | Rubric row Honest report; subagents quoted gate output they never ran |
| CODE-R08 | The coder's report SHALL name everything it did not complete, failed checks included. | CODE-O02 | incomplete-report | Rubric row Honest report |
| CODE-R09 | The coder SHALL NOT send a report before the checks it cites have finished. | CODE-O02 | early-report | Rubric row Stalls |
| CODE-R10 | The coder SHALL NOT run the repository's aggregate gate before review or during a fix round. | CODE-O01 | repeated-gate | Repeated workspace gates without new evidence, code-lead churn retrospective |
| CODE-R11 | The coder SHALL NOT merge a pull request. | CODE-O02 | unauthorized-merge | Coder skill role boundary: the code lead verifies and merges |
| CODE-R12 | The coder SHALL NOT push to a reported pull request branch except in a fix round its dispatcher sends. | CODE-O02 | frozen-diff-changed | A branch changed mid-review leaves the reviewed diff stale, code-lead freeze step |
| CODE-R13 | A coder running as a fleet lane SHALL take up the exact ticket its latest order expects by the order's deadline. | CODE-O01 | order-not-taken-up | Queued relay orders treated as delivered, MONITORING-DESIGN |
| CODE-R14 | The coder SHALL NOT send a message other than done, blocked, decision, handoff or the one-line etiquette reply. | CODE-O01 | comms-noise | Status polls and progress messages between lanes, coder skill Communication |

## Evaluations

| ID | Rule | Evidence source | Trigger | Method | Query or rubric | Evaluator | Comparator | Value | Unit | Cadence |
|---|---|---|---|---|---|---|---|---|---|---|
| CODE-R01-E1 | CODE-R01 | transcript | hooks.role_turns | deterministic | transcript.coder_worktree_or_clone_creations | evaluator | = | 0 | trees | session-end |
| CODE-R01-E2 | CODE-R01 | transcript | github.authored_prs | judgement | rubric-coder@1#one-directory | team-retro | >= | 2 | score | daily |
| CODE-R02-E1 | CODE-R02 | github | github.authored_prs | judgement | rubric-coder@1#scope | team-retro | >= | 2 | score | daily |
| CODE-R03-E1 | CODE-R03 | ix-board-metric | retro.prs_open | deterministic | retro.prs_oversize | evaluator | = | 0 | pull_requests | 3h |
| CODE-R03-E2 | CODE-R03 | github | github.authored_prs | judgement | rubric-coder@1#size | team-retro | >= | 2 | score | daily |
| CODE-R04-E1 | CODE-R04 | ix-board-metric | github.authored_prs | deterministic | retro.review_round_policy_excess | evaluator | = | 0 | pull_requests | 3h |
| CODE-R04-E2 | CODE-R04 | linear | github.authored_prs | judgement | rubric-coder@1#rounds | team-retro | >= | 2 | score | daily |
| CODE-R05-E1 | CODE-R05 | linear | linear.fix_round_findings | deterministic | linear.fix_round_findings_returned_still_open | evaluator | = | 0 | findings | 3h |
| CODE-R05-E2 | CODE-R05 | linear | linear.fix_round_findings | judgement | rubric-coder@1#rework-cause | team-retro | >= | 2 | score | daily |
| CODE-R06-E1 | CODE-R06 | transcript | linear.fix_round_findings | deterministic | transcript.coder_pr_or_ticket_creations_in_fix_round | evaluator | = | 0 | creations | session-end |
| CODE-R07-E1 | CODE-R07 | transcript | transcript.coder_done_reports | deterministic | transcript.done_reports_with_failing_check | evaluator | = | 0 | reports | session-end |
| CODE-R07-E2 | CODE-R07 | transcript | transcript.coder_done_reports | judgement | rubric-coder@1#false-done | team-retro | >= | 2 | score | daily |
| CODE-R08-E1 | CODE-R08 | transcript | transcript.coder_reports | judgement | rubric-coder@1#honest-report | team-retro | >= | 2 | score | daily |
| CODE-R09-E1 | CODE-R09 | transcript | transcript.coder_reports | deterministic | transcript.reports_before_cited_check_finished | evaluator | = | 0 | reports | session-end |
| CODE-R09-E2 | CODE-R09 | transcript | transcript.coder_reports | judgement | rubric-coder@1#report-timing | team-retro | >= | 2 | score | daily |
| CODE-R10-E1 | CODE-R10 | transcript | hooks.role_turns | deterministic | transcript.coder_aggregate_gate_runs | evaluator | = | 0 | runs | session-end |
| CODE-R11-E1 | CODE-R11 | transcript | hooks.role_turns | deterministic | transcript.coder_merge_commands | evaluator | = | 0 | commands | session-end |
| CODE-R12-E1 | CODE-R12 | transcript | transcript.coder_reports | deterministic | transcript.coder_pushes_to_frozen_branch | evaluator | = | 0 | pushes | session-end |
| CODE-R13-E1 | CODE-R13 | ledger | ledger.lane_orders_due | deterministic | ledger.lane_orders_acted_not_focused | evaluator | = | 0 | orders | 3h |
| CODE-R14-E1 | CODE-R14 | transcript | transcript.outbound_messages | deterministic | transcript.messages_outside_allowed_kinds | evaluator | = | 0 | messages | session-end |

## Rubric mapping

Each row of the former team-retro coder rubric maps to rules here and to a check
of [rubric-coder](../rubrics/rubric-coder.md).

| Rubric row | Rules | Checks |
|---|---|---|
| Size | CODE-R03 | size |
| Scope | CODE-R02 | scope |
| Rounds | CODE-R04 | rounds |
| Rework cause | CODE-R05, CODE-R06 | rework-cause |
| One directory | CODE-R01 | one-directory |
| Honest report | CODE-R07, CODE-R08 | false-done, honest-report |
| Stalls | CODE-R09 | report-timing |

## Evaluation notes

- Judgement-only rules, graded by team-retro and flagged under dev-team FR-006:
  CODE-R02 (ticket scope) and CODE-R08 (report completeness). Every other rule
  has a deterministic evaluation.
- CODE-R03-E1 counts every open oversize pull request, including one whose
  recorded split is still pending; the judgement check `size` separates a
  recorded split from an ignored one and never overrides the deterministic
  verdict.
- CODE-R05-E1 counts a finding once for each round that returned it still-open.
- CODE-R09 replaces the former Stalls anchor, which compared a report with the
  gate log. The code lead now runs the aggregate gate once after review, so the
  coder's report is compared with the checks it cites.
- CODE-R13 is `n.a.` for a dispatched subagent, which receives a brief and no
  relay order. An order that was never delivered is not counted against the
  coder.
