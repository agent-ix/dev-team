---
id: LEAD
role: code-lead
version: 1
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
---
# Role spec: code lead

## Purpose

The code lead runs the coding lane for one team or project: it takes planned
tickets in order, dispatches a [coder](coder.md) and one
[reviewer](reviewer.md) per pull request, verifies, runs the aggregate gate once
after review, merges, keeps the tracker true and keeps landing work. It
orchestrates and does not author code, specs or reviews. Planning and order
belong to the [planner](planner.md).

A repository, organization or direct user rule that differs from a gate or merge
rule here wins. The code lead records it as a `waiver` record
([FR-017](../functional/FR-017-role-evaluation-records.md)).

Targets are initial values. The evaluator's role rows (dev-team FR-008) show
whether a target is met and whether a rule moves its objective; the director
proposes changes through a role spec version bump.

## Query sources and producers

A query reference is `<source>.<name>`, an evaluator query that
`ix-board retro eval` (SWM-221) registers. The source prefix names the store the
query reads: `retro` (the ix-board retro catalog, ix-board FR-024, or
department report, ix-board FR-029; `retro.<id>_max` is the largest value of a
keyed department measurement), `prom` (series of the ix-board team exporter,
ix-board FR-033; `prom.ix_team_<name>` is the series `ix_team_<name>`), `github`
(pull request records, heads and merge state), `linear` (tracker history and the
marker comments of FR-017), `hooks` (hook activity events, ix-relay FR-068) and
`transcript` (the evaluated session's transcript, read with the terms of
FR-017).

Terms such as finding, closed, clean, covered, ready to merge, waived and send
are those of FR-017. Counts are over the evaluation window and the team's scope.
`retro` and `prom` values cover a team, not one session: a role row uses the
value, and a session row is `unavailable` unless the scope and window hold
exactly one session of this role (dev-team FR-001, FR-008). A value whose
configuration is absent is `unavailable`.

The Producer column states what exists on ix-board `origin/main`: `computed`
means ix-board computes the value today and only its registration as an
evaluator query is open; `none` means no ix-board requirement defines it.

| Query | Source and fields | Counting rule | Producer |
|---|---|---|---|
| retro.tickets_closed_per_hour | tracker state history; GitHub merge state; blocker relations | Issues of the configured projects and the gate path moved to completed in the window with a merged pull request attached, each once, divided by the window hours | none |
| retro.pr_cycle_median_hours | GitHub merged pull requests | As ix-board FR-024: median creation-to-merge hours | computed (ix-board FR-024) |
| retro.pr_cycle_p90_hours | GitHub merged pull requests | As ix-board FR-024: 90th percentile of the same hours | computed (ix-board FR-024) |
| retro.fix_rounds_max | tracker marker first lines | As ix-board FR-024: highest disposition `round=` on one pull request | computed (ix-board FR-024) |
| retro.main_red_minutes | main branch check runs | As ix-board FR-024 | computed (ix-board FR-024) |
| retro.path_remaining | tracker blocker relations | As ix-board FR-024: open issues transitively blocking a gate ticket | computed (ix-board FR-024) |
| retro.path_closed | tracker state history | As ix-board FR-024: gate-path issues completed in the window | computed (ix-board FR-024) |
| retro.prs_open | GitHub open pull requests | As ix-board FR-024 | computed (ix-board FR-024) |
| retro.gate_log_runs | gate log lines: `pr`, `kind`, `finished_at` | Lines with `kind` `gate` and `finished_at` in the window | none |
| retro.wip_active | department report | As ix-board FR-029: started, unfinished scoped issues | computed (ix-board FR-029) |
| retro.claims_without_movement | department report | As ix-board FR-029: started claims with no movement past the stale interval | computed (ix-board FR-029) |
| retro.merged_open | department report | As ix-board FR-029: open issues whose pull request is merged and obligations are met | computed (ix-board FR-029) |
| retro.review_round_policy_excess | department report | As ix-board FR-029: pull requests above the configured review round limit | computed (ix-board FR-029) |
| retro.repin_only_prs | department report | As ix-board FR-029: pull requests whose substantive diff only changes dependency pins | computed (ix-board FR-029) |
| retro.host_overcommit_units_max | department report | As ix-board FR-029: build units above capacity, largest over configured hosts | computed (ix-board FR-029) |
| retro.idle_with_ready | department report | As ix-board FR-029: verified idle scoped lanes with a ready issue | computed (ix-board FR-029) |
| prom.ix_team_ready_issues | exporter series | As ix-board FR-033: ready issues of the scope | computed (ix-board FR-033) |
| linear.path_tickets_unblocked_at_window_start | tracker blocker relations and state history | Gate-path issues open at the window start whose every blocker was completed or canceled then | none |
| linear.merged_prs_without_review_record | GitHub merged pull requests; `reviewer` field `pr` | Pull requests merged in the window with no `reviewer` comment on their ticket naming them | none |
| linear.findings_open_at_merge | marker data blocks and `final-fix` records; GitHub merge time | Findings of pull requests merged in the window that were open at the merge time | none |
| linear.gate_records | `lead-record` `kind=gate` comments | Gate records created in the window | none |
| linear.waiver_records | `lead-record` `kind=waiver` comments | Waiver records created in the window | none |
| linear.gate_runs_without_record | gate log lines; gate record `finished` | Lines of `retro.gate_log_runs` whose `finished_at` equals the `finished` of no gate record | none |
| linear.redundant_gate_runs | gate records `head`, `exit`, `started`; GitHub commits | Gate records of the window whose head is covered from the head of an earlier record with `exit=0` on the same pull request, leaving out pull requests waived for LEAD-R06 | none |
| linear.gate_runs_before_clean_review | gate record `started`; review markers | Gate records of the window at whose `started` time the pull request's review was not clean, leaving out pull requests waived for LEAD-R20 | none |
| github.merged_prs | GitHub merged pull requests | Pull requests merged in the window | none |
| github.review_ready_prs | GitHub `createdAt`, draft events, state | Pull requests ready for review at some time in the window and not closed unmerged | none |
| github.review_ready_prs_undispatched | the same; `reviewer` comments; lead transcripts: agent dispatch calls; `eval.review_age_limit_hours` | Pull requests whose ready-for-review time plus the limit is in the window, with neither a `reviewer` comment nor a lead dispatch whose prompt names `/reviewer` and the pull request number by that deadline; one still without either from an earlier window is counted again. A pull request with no comment and an unreadable lead transcript makes the value `unavailable` | none |
| github.merges_beyond_reviewed_change | GitHub merged head and commits; review markers; `rebase` and `final-fix` records | Pull requests merged in the window whose merged head is not review-covered | none |
| github.merges_without_covering_gate | GitHub files and merged head; gate, `rebase` and `final-fix` records | Pull requests merged in the window that require a gate and whose merged head is not gate-covered, leaving out pull requests waived for LEAD-R11 | none |
| github.prs_ready_to_merge | GitHub pull requests and base branches; markers and records | Pull requests that were ready to merge at some time in the window and are not closed unmerged | none |
| github.ready_prs_unmerged_over_hour | the same; merge time | Pull requests of `github.prs_ready_to_merge` merged, or still open at evaluation, more than 3600 seconds after becoming ready, leaving out pull requests waived for LEAD-R17 | none |
| hooks.role_turns | hook prompt events | Turns of the evaluated session in the window | none |
| transcript.lead_extra_trees | tool calls of the lead and its subagents: command | Commands matching `git worktree add` or `git clone` for a repository and ticket (read from the target path or branch) after the first, while an earlier tree of that pair was not removed | none |
| transcript.lead_authored_edits | tool calls of the lead session itself: file path | File edit or write calls on a file inside a worktree of a team repository and outside its `reviews/` directory | none |
| transcript.outbound_messages | sends | The session's sends | none |

## Metrics

| ID | Name | Evidence source | Query | Unit | Target | Direction |
|---|---|---|---|---|---|---|
| LEAD-M01 | Tickets closed per hour, with the change on the default branch | ix-board-metric | retro.tickets_closed_per_hour | tickets/hour | 0.5 | higher |
| LEAD-M02 | Pull request cycle time, p50: creation to merge | ix-board-metric | retro.pr_cycle_median_hours | hours | 4 | lower |
| LEAD-M03 | Pull request cycle time, p90: creation to merge | ix-board-metric | retro.pr_cycle_p90_hours | hours | 24 | lower |
| LEAD-M04 | Rework rounds: most fix rounds on one pull request | ix-board-metric | retro.fix_rounds_max | rounds | 2 | lower |
| LEAD-M05 | Main red minutes in the 24 hour window | ix-board-metric | retro.main_red_minutes | minutes/day | 30 | lower |

## Objectives

| ID | Objective | Metrics |
|---|---|---|
| LEAD-O01 | Planned tickets land continuously | LEAD-M01 |
| LEAD-O02 | A pull request lands quickly after it opens | LEAD-M02, LEAD-M03 |
| LEAD-O03 | Work is done once | LEAD-M04 |
| LEAD-O04 | The default branch stays usable for every lane | LEAD-M05 |

## Rules

| ID | Rule | Objective | Class | Source |
|---|---|---|---|---|
| LEAD-R01 | The code lead SHALL close a gate-path ticket in every daily window that opens with one unblocked. | LEAD-O01 | gate-flat | Rubric row Gate progress; strategy "Count the path" |
| LEAD-R02 | The code lead SHALL dispatch a reviewer for every pull request within the review age limit of its becoming ready for review. | LEAD-O02 | review-stall | Rubric row Review and flow |
| LEAD-R03 | The code lead SHALL move a gated or stale, unworked started ticket to the team's ready state. | LEAD-O01 | stale-claim | Rubric row Honest state |
| LEAD-R04 | The code lead SHALL close a ticket in the work cycle its change and every completion obligation are on the default branch. | LEAD-O01 | merged-open | Merged pull requests left on open tickets, department monitoring metric merged_open |
| LEAD-R05 | The code lead SHALL keep every pull request within the current review round policy. | LEAD-O03 | round-excess | Rubric row Fix rounds |
| LEAD-R06 | Unless a repository or organization rule requires it, the code lead SHALL NOT run the aggregate gate on a head that an earlier passing run already covers. | LEAD-O02 | repeated-gate | Rubric row Gate discipline; strategy "One gate per pull request" |
| LEAD-R07 | The code lead SHALL fold a required dependency pin into the pull request that needs it, never into a repin-only pull request. | LEAD-O02 | repin-churn | Rubric row Pin discipline |
| LEAD-R08 | The code lead SHALL NOT merge a pull request with a finding whose latest outcome is still-open or missing, other than a finding its one-line final fix closes. | LEAD-O04 | open-finding-merged | Rubric row Merge safety |
| LEAD-R09 | The code lead SHALL NOT merge a change that no review covered, other than a one-line final fix it read, an overlap rebase whose confined check passed, or committed review files. | LEAD-O04 | unreviewed-change-merged | Rubric row Merge safety; code-lead verify before merge |
| LEAD-R10 | The code lead SHALL merge only a pull request that carries a recorded independent review. | LEAD-O04 | unreviewed-merge | Rubric row Merge safety; subagents quoted gate output they never ran, code-lead verification |
| LEAD-R11 | Unless a repository or organization rule sets another gate requirement, the code lead SHALL NOT merge a pull request that changes a file other than Markdown without a passing aggregate gate that covers the merged head. | LEAD-O04 | ungated-merge | Never leave a repo red, code-lead never list |
| LEAD-R12 | The code lead SHALL give each ticket one worktree, shared by coder, reviewer and gate. | LEAD-O02 | duplicate-worktree | Rubric row One directory |
| LEAD-R13 | The code lead SHALL admit builds only within current configured or verified capacity. | LEAD-O02 | capacity-overload | Rubric row Resources |
| LEAD-R14 | The code lead SHALL assign ready work to every confirmed idle lane or worker. | LEAD-O01 | idle-with-ready | Rubric row Agent recovery |
| LEAD-R15 | The code lead SHALL report work as delivered only on confirmation by pane, pull request or commit SHA. | LEAD-O01 | queued-as-delivered | Rubric row Delivery; strategy "Verify delivery" |
| LEAD-R16 | The code lead SHALL NOT author code, spec or review changes itself. | LEAD-O01 | lead-does-the-work | Never code the change yourself, code-lead never list |
| LEAD-R17 | Unless a repository, organization or user rule holds it, the code lead SHALL merge a pull request within one hour of its becoming ready to merge. | LEAD-O02 | reviewed-unmerged | Strategy "Merge-out first": reviewed work waiting to land |
| LEAD-R18 | The code lead SHALL NOT send a message other than done, blocked, decision, handoff or the one-line etiquette reply. | LEAD-O01 | comms-noise | Status polls and progress messages between lanes, code-lead skill Communication |
| LEAD-R19 | The code lead SHALL record each aggregate gate run on the pull request's ticket. | LEAD-O04 | gate-unrecorded | The gate log holds no commit and no exit status; code-lead verify before merge |
| LEAD-R20 | Unless a repository or organization rule requires it, the code lead SHALL NOT start the aggregate gate while the pull request's review is not clean. | LEAD-O02 | early-gate | Rubric row Gate discipline: one final lead gate after review |
| LEAD-R21 | The code lead SHALL post a waiver record only for a role rule that the repository, organization or direct user rule at its `ref` differs from. | LEAD-O04 | unfounded-waiver | A waiver the evaluated role posts removes a pull request from that rule's queries, FR-017 waived |

## Evaluations

| ID | Rule | Evidence source | Trigger | Method | Query or rubric | Evaluator | Comparator | Value | Unit | Cadence |
|---|---|---|---|---|---|---|---|---|---|---|
| LEAD-R01-E1 | LEAD-R01 | ix-board-metric | linear.path_tickets_unblocked_at_window_start | deterministic | retro.path_closed | evaluator | >= | 1 | issues | daily |
| LEAD-R01-E2 | LEAD-R01 | linear | retro.path_remaining | judgement | rubric-code-lead@1#gate-progress | team-retro | >= | 2 | score | daily |
| LEAD-R02-E1 | LEAD-R02 | github | github.review_ready_prs | deterministic | github.review_ready_prs_undispatched | evaluator | = | 0 | pull_requests | 3h |
| LEAD-R02-E2 | LEAD-R02 | ix-board-metric | retro.prs_open | judgement | rubric-code-lead@1#review-flow | team-retro | >= | 2 | score | daily |
| LEAD-R03-E1 | LEAD-R03 | ix-board-metric | retro.wip_active | deterministic | retro.claims_without_movement | evaluator | = | 0 | issues | 3h |
| LEAD-R03-E2 | LEAD-R03 | linear | retro.wip_active | judgement | rubric-code-lead@1#honest-state | team-retro | >= | 2 | score | daily |
| LEAD-R04-E1 | LEAD-R04 | ix-board-metric | github.merged_prs | deterministic | retro.merged_open | evaluator | = | 0 | issues | 3h |
| LEAD-R05-E1 | LEAD-R05 | ix-board-metric | retro.prs_open | deterministic | retro.review_round_policy_excess | evaluator | = | 0 | pull_requests | 3h |
| LEAD-R05-E2 | LEAD-R05 | linear | retro.prs_open | judgement | rubric-code-lead@1#fix-rounds | team-retro | >= | 2 | score | daily |
| LEAD-R06-E1 | LEAD-R06 | linear | linear.gate_records | deterministic | linear.redundant_gate_runs | evaluator | = | 0 | runs | 3h |
| LEAD-R06-E2 | LEAD-R06 | linear | linear.gate_records | judgement | rubric-code-lead@1#gate-discipline | team-retro | >= | 2 | score | daily |
| LEAD-R07-E1 | LEAD-R07 | ix-board-metric | retro.prs_open | deterministic | retro.repin_only_prs | evaluator | = | 0 | pull_requests | daily |
| LEAD-R07-E2 | LEAD-R07 | github | retro.prs_open | judgement | rubric-code-lead@1#pin-discipline | team-retro | >= | 2 | score | daily |
| LEAD-R08-E1 | LEAD-R08 | linear | github.merged_prs | deterministic | linear.findings_open_at_merge | evaluator | = | 0 | findings | 3h |
| LEAD-R08-E2 | LEAD-R08 | linear | github.merged_prs | judgement | rubric-code-lead@1#open-findings | team-retro | >= | 2 | score | daily |
| LEAD-R09-E1 | LEAD-R09 | github | github.merged_prs | deterministic | github.merges_beyond_reviewed_change | evaluator | = | 0 | pull_requests | 3h |
| LEAD-R09-E2 | LEAD-R09 | github | github.merged_prs | judgement | rubric-code-lead@1#merge-safety | team-retro | >= | 2 | score | daily |
| LEAD-R10-E1 | LEAD-R10 | linear | github.merged_prs | deterministic | linear.merged_prs_without_review_record | evaluator | = | 0 | pull_requests | 3h |
| LEAD-R11-E1 | LEAD-R11 | github | github.merged_prs | deterministic | github.merges_without_covering_gate | evaluator | = | 0 | pull_requests | 3h |
| LEAD-R11-E2 | LEAD-R11 | github | github.merged_prs | judgement | rubric-code-lead@1#gate-safety | team-retro | >= | 2 | score | daily |
| LEAD-R12-E1 | LEAD-R12 | transcript | hooks.role_turns | deterministic | transcript.lead_extra_trees | evaluator | = | 0 | trees | session-end |
| LEAD-R12-E2 | LEAD-R12 | transcript | hooks.role_turns | judgement | rubric-code-lead@1#one-directory | team-retro | >= | 2 | score | daily |
| LEAD-R13-E1 | LEAD-R13 | ix-board-metric | hooks.role_turns | deterministic | retro.host_overcommit_units_max | evaluator | = | 0 | units | 3h |
| LEAD-R13-E2 | LEAD-R13 | ix-board-metric | hooks.role_turns | judgement | rubric-code-lead@1#resources | team-retro | >= | 2 | score | daily |
| LEAD-R14-E1 | LEAD-R14 | ix-board-metric | prom.ix_team_ready_issues | deterministic | retro.idle_with_ready | evaluator | = | 0 | lanes | 3h |
| LEAD-R14-E2 | LEAD-R14 | ix-board-metric | prom.ix_team_ready_issues | judgement | rubric-code-lead@1#agent-recovery | team-retro | >= | 2 | score | daily |
| LEAD-R15-E1 | LEAD-R15 | transcript | transcript.outbound_messages | judgement | rubric-code-lead@1#delivery | team-retro | >= | 2 | score | daily |
| LEAD-R16-E1 | LEAD-R16 | transcript | hooks.role_turns | deterministic | transcript.lead_authored_edits | evaluator | = | 0 | edits | session-end |
| LEAD-R17-E1 | LEAD-R17 | github | github.prs_ready_to_merge | deterministic | github.ready_prs_unmerged_over_hour | evaluator | = | 0 | pull_requests | 3h |
| LEAD-R17-E2 | LEAD-R17 | github | github.prs_ready_to_merge | judgement | rubric-code-lead@1#merge-latency | team-retro | >= | 2 | score | daily |
| LEAD-R18-E1 | LEAD-R18 | transcript | transcript.outbound_messages | judgement | rubric-code-lead@1#comms | team-retro | >= | 2 | score | daily |
| LEAD-R19-E1 | LEAD-R19 | ix-board-metric | retro.gate_log_runs | deterministic | linear.gate_runs_without_record | evaluator | = | 0 | runs | 3h |
| LEAD-R20-E1 | LEAD-R20 | linear | linear.gate_records | deterministic | linear.gate_runs_before_clean_review | evaluator | = | 0 | runs | 3h |
| LEAD-R21-E1 | LEAD-R21 | linear | linear.waiver_records | judgement | rubric-code-lead@1#waivers | team-retro | >= | 2 | score | daily |

## Rubric mapping

Each row of the former team-retro code lead rubric maps to rules here and to a
check of [rubric-code-lead](../rubrics/rubric-code-lead.md). Two checks had no
row: `comms` grades the code-lead skill's Communication section, and `waivers`
grades the waiver records.

| Rubric row | Rules | Checks |
|---|---|---|
| Gate progress | LEAD-R01 | gate-progress |
| Review and flow | LEAD-R02, LEAD-R17 | review-flow, merge-latency |
| Honest state | LEAD-R03, LEAD-R04 | honest-state |
| Fix rounds | LEAD-R05 | fix-rounds |
| Gate discipline | LEAD-R06, LEAD-R19, LEAD-R20 | gate-discipline |
| Pin discipline | LEAD-R07 | pin-discipline |
| Merge safety | LEAD-R08, LEAD-R09, LEAD-R10, LEAD-R11 | open-findings, merge-safety, gate-safety |
| One directory | LEAD-R12 | one-directory |
| Resources | LEAD-R13 | resources |
| Agent recovery | LEAD-R14 | agent-recovery |
| Delivery | LEAD-R15 | delivery |

## Evaluation notes

- Judgement-only rules, graded by team-retro and flagged under dev-team FR-006:
  LEAD-R15 (whether a statement claims delivery), LEAD-R18 (message kind) and
  LEAD-R21 (whether the cited rule differs). Each depends on the meaning of
  prose, which no recorded fact states.
- A failed gate, and a change after a passing gate that coverage does not allow,
  both leave the head uncovered, so the next run is not redundant.
- LEAD-R01 is `n.a.` when the window opens with no unblocked gate-path ticket;
  the check `gate-progress` then grades whether the blocker has an owner.
- LEAD-R04, LEAD-R10, LEAD-R16, LEAD-R19 and LEAD-R20 have no judgement
  evaluation of their own; the checks `honest-state` and `gate-discipline` grade
  LEAD-R03 and LEAD-R06 only.
- A deterministic result that leaves out a waived pull request lists it as
  evidence (FR-017). LEAD-R21 grades every waiver, including one that covers
  another role's rule.
- LEAD-R14: `WAITING` and `RECENT` agents are observed without nudging and are
  not idle. File ages, token totals and worker counts alone establish neither
  idle state nor capacity.
