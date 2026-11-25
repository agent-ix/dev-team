---
id: LEAD
role: code-lead
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
---
# Role spec: code lead

## Purpose

The code lead runs the coding lane for one team or project: it takes planned
tickets in order, dispatches a [coder](coder.md) and one
[reviewer](reviewer.md) per pull request, verifies, runs the aggregate gate once,
merges, keeps the tracker true and keeps landing work. It orchestrates and does
not author code, specs or reviews. Planning and order belong to the
[planner](planner.md).

Targets are initial values. The evaluator's role rows (dev-team FR-008) show
whether a target is met and whether a rule moves its objective; the director
proposes changes through a role spec version bump.

## Query sources and producers

A query reference is `<source>.<name>`, an evaluator query that
`ix-board retro eval` (SWM-221) registers. The source prefix names the store the
query reads:

- `retro`: the ix-board retro record. `retro.<id>` is the metric of that id in
  the retro catalog (ix-board FR-024) or the department catalog (ix-board
  FR-029). For a duration measurement `retro.<id>_p90` is its `p90` statistic,
  and for a keyed measurement `retro.<id>_max` is the largest value over its
  keys.
- `prom`: series the ix-board team exporter serves (ix-board FR-033);
  `prom.ix_team_<name>` is the series `ix_team_<name>`.
- `github`: pull request records, heads, reviews and merge state, joined with
  the gate log where stated.
- `linear`: tracker state history and the `reviewer` and `reviewer-dispositions`
  markers and data blocks.
- `hooks`: hook activity events (ix-relay FR-068) of the evaluated session.
- `transcript`: the evaluated session's transcript, read by a fixed pattern
  query.

`retro` and `prom` values cover a team's scope and window, not one session. A
role row uses the value; a session row is `unavailable` unless the scope and
window hold exactly one session of this role (dev-team FR-001, FR-008). A
department or exporter value whose configuration is absent is `unavailable`,
and so is a duration statistic over an empty population.

The Producer column states what exists on ix-board `origin/main`: `computed`
means ix-board computes the value today and only its registration as an
evaluator query is open (SWM-221); `none` means no ix-board requirement defines
it, and the named ticket owns the producer.

| Query | Counts | Producer |
|---|---|---|
| retro.tickets_closed_per_hour | Issues of the configured projects and the gate path moved to completed in the window with a merged pull request attached, each once, divided by window hours | none (SWM-261) |
| retro.pr_cycle_median_hours | Median creation-to-merge hours of pull requests merged in the window | computed (ix-board FR-024) |
| retro.pr_cycle_p90_hours | 90th percentile of the same hours | computed (ix-board FR-024) |
| retro.fix_rounds_max | Highest reviewer disposition round on one pull request open or merged in the window | computed (ix-board FR-024) |
| retro.main_red_minutes | Minutes the checked main branch was failing in the window | computed (ix-board FR-024) |
| retro.path_remaining | Open issues transitively blocking a gate ticket | computed (ix-board FR-024) |
| retro.path_closed | Gate-path issues completed in the window | computed (ix-board FR-024) |
| retro.prs_open | Open pull requests in the configured repositories | computed (ix-board FR-024) |
| retro.full_gates_max | Largest number of gate-log gate runs for one pull request in the window | computed (ix-board FR-024) |
| retro.pr_without_reviewer_age_hours_p90 | 90th percentile age of open non-draft pull requests with no assigned reviewer and no qualifying review | computed (ix-board FR-029) |
| retro.wip_active | Started, unfinished scoped issues | computed (ix-board FR-029) |
| retro.claims_without_movement | Started claims older than the stale interval with no later movement | computed (ix-board FR-029) |
| retro.merged_open | Open issues whose pull request is merged and whose completion obligations are met | computed (ix-board FR-029) |
| retro.review_round_policy_excess | Pull requests above the configured review round limit | computed (ix-board FR-029) |
| retro.repin_only_prs | Pull requests whose substantive diff only changes dependency pins | computed (ix-board FR-029) |
| retro.host_overcommit_units_max | Largest build units used above capacity on any configured host | computed (ix-board FR-029) |
| retro.idle_with_ready | Verified idle scoped lanes with at least one ready issue | computed (ix-board FR-029) |
| prom.ix_team_ready_issues | Ready issues of the scope | computed (ix-board FR-033) |
| linear.unblocked_path_tickets | Open gate-path tickets with no open blocker at some time in the window | none (SWM-261) |
| linear.findings_still_open_at_merge | Findings of merged pull requests whose latest outcome at merge time is `still-open` or missing | none (SWM-261) |
| linear.merged_prs_without_review_record | Pull requests merged in the window with no `reviewer` marker naming them on their ticket | none (SWM-261) |
| github.merged_prs | Pull requests merged in the window | none (SWM-261) |
| github.merges_with_unreviewed_changes | Merged pull requests whose merged head changes behavior beyond the last reviewed head, other than review artifact files and a one-line final fix | none (SWM-261) |
| github.merged_code_prs_without_passing_gate | Merged pull requests that change code or tests and have no passing gate-log run at the merged head | none (SWM-261) |
| github.clean_gated_prs_unmerged_over_hour | Open pull requests with a clean latest disposition and a passing final gate for more than one hour | none (SWM-261) |
| hooks.role_turns | Turns of the evaluated session in the window | none (SWM-221) |
| transcript.lead_worktrees_beyond_one_per_ticket | Worktrees or clones the session created for a ticket that already had one, including those named in review or gate dispatches | none (SWM-221) |
| transcript.delivery_claims | Statements by the session that an order, merge or fix was delivered or completed | none (SWM-221) |
| transcript.completion_claims_without_confirmation | Delivery claims with no cited pane observation, pull request or commit SHA | none (SWM-221) |
| transcript.lead_authored_changes | File edits or commits by the lead session itself to code, spec or review files, other than committing a reviewer's artifact unchanged | none (SWM-221) |
| transcript.outbound_messages | Messages the session sent to another agent | none (SWM-221) |
| transcript.messages_outside_allowed_kinds | Outbound messages that are not done, blocked, decision, handoff or the one-line etiquette reply | none (SWM-221) |

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
| LEAD-R01 | The code lead SHALL close a gate-path ticket in every daily window in which one is unblocked. | LEAD-O01 | gate-flat | Rubric row Gate progress; strategy "Count the path" |
| LEAD-R02 | The code lead SHALL dispatch a reviewer for every open non-draft pull request within the configured review age limit. | LEAD-O02 | review-stall | Rubric row Review and flow |
| LEAD-R03 | The code lead SHALL move a gated or stale, unworked started ticket to the team's ready state. | LEAD-O01 | stale-claim | Rubric row Honest state |
| LEAD-R04 | The code lead SHALL close a ticket in the work cycle its change and every completion obligation are on the default branch. | LEAD-O01 | merged-open | Merged pull requests left on open tickets, department monitoring metric merged_open |
| LEAD-R05 | The code lead SHALL keep every pull request within the current review round policy. | LEAD-O03 | round-excess | Rubric row Fix rounds |
| LEAD-R06 | The code lead SHALL run the aggregate gate no more than once per pull request, at its final head. | LEAD-O02 | repeated-gate | Rubric row Gate discipline; strategy "One gate per pull request" |
| LEAD-R07 | The code lead SHALL fold a required dependency pin into the pull request that needs it, never into a repin-only pull request. | LEAD-O02 | repin-churn | Rubric row Pin discipline |
| LEAD-R08 | The code lead SHALL NOT merge a pull request with a finding whose latest outcome is still-open or missing. | LEAD-O04 | open-finding-merged | Rubric row Merge safety |
| LEAD-R09 | The code lead SHALL NOT merge behavior that no review covered, other than a one-line final fix it read. | LEAD-O04 | unreviewed-merge | Rubric row Merge safety |
| LEAD-R10 | The code lead SHALL merge only a pull request that carries a recorded independent review. | LEAD-O04 | unreviewed-merge | Rubric row Merge safety; subagents quoted gate output they never ran, code-lead verification |
| LEAD-R11 | The code lead SHALL NOT merge a pull request that changes code or tests without a passing aggregate gate at the merged head. | LEAD-O04 | ungated-merge | Never leave a repo red, code-lead never list |
| LEAD-R12 | The code lead SHALL give each ticket one worktree, shared by coder, reviewer and gate. | LEAD-O02 | duplicate-worktree | Rubric row One directory |
| LEAD-R13 | The code lead SHALL admit builds only within current configured or verified capacity. | LEAD-O02 | capacity-overload | Rubric row Resources |
| LEAD-R14 | The code lead SHALL assign ready work to every confirmed idle lane or worker. | LEAD-O01 | idle-with-ready | Rubric row Agent recovery |
| LEAD-R15 | The code lead SHALL report work as delivered only on confirmation by pane, pull request or commit SHA. | LEAD-O01 | queued-as-delivered | Rubric row Delivery; strategy "Verify delivery" |
| LEAD-R16 | The code lead SHALL NOT author code, spec or review changes itself. | LEAD-O01 | lead-does-the-work | Never code the change yourself, code-lead never list |
| LEAD-R17 | The code lead SHALL merge a pull request within one hour of its clean review and passing final gate. | LEAD-O02 | reviewed-unmerged | Strategy "Merge-out first": reviewed work waiting to land |
| LEAD-R18 | The code lead SHALL NOT send a message other than done, blocked, decision, handoff or the one-line etiquette reply. | LEAD-O01 | comms-noise | Status polls and progress messages between lanes, code-lead skill Communication |

## Evaluations

| ID | Rule | Evidence source | Trigger | Method | Query or rubric | Evaluator | Comparator | Value | Unit | Cadence |
|---|---|---|---|---|---|---|---|---|---|---|
| LEAD-R01-E1 | LEAD-R01 | ix-board-metric | linear.unblocked_path_tickets | deterministic | retro.path_closed | evaluator | >= | 1 | issues | daily |
| LEAD-R01-E2 | LEAD-R01 | linear | retro.path_remaining | judgement | rubric-code-lead@1#gate-progress | team-retro | >= | 2 | score | daily |
| LEAD-R02-E1 | LEAD-R02 | ix-board-metric | retro.prs_open | deterministic | retro.pr_without_reviewer_age_hours_p90 | evaluator | <= | 1 | hours | 3h |
| LEAD-R02-E2 | LEAD-R02 | ix-board-metric | retro.prs_open | judgement | rubric-code-lead@1#review-flow | team-retro | >= | 2 | score | daily |
| LEAD-R03-E1 | LEAD-R03 | ix-board-metric | retro.wip_active | deterministic | retro.claims_without_movement | evaluator | = | 0 | issues | 3h |
| LEAD-R03-E2 | LEAD-R03 | linear | retro.wip_active | judgement | rubric-code-lead@1#honest-state | team-retro | >= | 2 | score | daily |
| LEAD-R04-E1 | LEAD-R04 | ix-board-metric | github.merged_prs | deterministic | retro.merged_open | evaluator | = | 0 | issues | 3h |
| LEAD-R05-E1 | LEAD-R05 | ix-board-metric | retro.prs_open | deterministic | retro.review_round_policy_excess | evaluator | = | 0 | pull_requests | 3h |
| LEAD-R05-E2 | LEAD-R05 | linear | retro.prs_open | judgement | rubric-code-lead@1#fix-rounds | team-retro | >= | 2 | score | daily |
| LEAD-R06-E1 | LEAD-R06 | ix-board-metric | github.merged_prs | deterministic | retro.full_gates_max | evaluator | <= | 1 | gates | daily |
| LEAD-R06-E2 | LEAD-R06 | ix-board-metric | github.merged_prs | judgement | rubric-code-lead@1#gate-discipline | team-retro | >= | 2 | score | daily |
| LEAD-R07-E1 | LEAD-R07 | ix-board-metric | retro.prs_open | deterministic | retro.repin_only_prs | evaluator | = | 0 | pull_requests | daily |
| LEAD-R07-E2 | LEAD-R07 | github | retro.prs_open | judgement | rubric-code-lead@1#pin-discipline | team-retro | >= | 2 | score | daily |
| LEAD-R08-E1 | LEAD-R08 | linear | github.merged_prs | deterministic | linear.findings_still_open_at_merge | evaluator | = | 0 | findings | 3h |
| LEAD-R08-E2 | LEAD-R08 | linear | github.merged_prs | judgement | rubric-code-lead@1#open-findings | team-retro | >= | 2 | score | daily |
| LEAD-R09-E1 | LEAD-R09 | github | github.merged_prs | deterministic | github.merges_with_unreviewed_changes | evaluator | = | 0 | pull_requests | 3h |
| LEAD-R09-E2 | LEAD-R09 | github | github.merged_prs | judgement | rubric-code-lead@1#merge-safety | team-retro | >= | 2 | score | daily |
| LEAD-R10-E1 | LEAD-R10 | linear | github.merged_prs | deterministic | linear.merged_prs_without_review_record | evaluator | = | 0 | pull_requests | 3h |
| LEAD-R11-E1 | LEAD-R11 | github | github.merged_prs | deterministic | github.merged_code_prs_without_passing_gate | evaluator | = | 0 | pull_requests | 3h |
| LEAD-R12-E1 | LEAD-R12 | transcript | hooks.role_turns | deterministic | transcript.lead_worktrees_beyond_one_per_ticket | evaluator | = | 0 | trees | session-end |
| LEAD-R12-E2 | LEAD-R12 | transcript | hooks.role_turns | judgement | rubric-code-lead@1#one-directory | team-retro | >= | 2 | score | daily |
| LEAD-R13-E1 | LEAD-R13 | ix-board-metric | hooks.role_turns | deterministic | retro.host_overcommit_units_max | evaluator | = | 0 | units | 3h |
| LEAD-R13-E2 | LEAD-R13 | ix-board-metric | hooks.role_turns | judgement | rubric-code-lead@1#resources | team-retro | >= | 2 | score | daily |
| LEAD-R14-E1 | LEAD-R14 | ix-board-metric | prom.ix_team_ready_issues | deterministic | retro.idle_with_ready | evaluator | = | 0 | lanes | 3h |
| LEAD-R14-E2 | LEAD-R14 | ix-board-metric | prom.ix_team_ready_issues | judgement | rubric-code-lead@1#agent-recovery | team-retro | >= | 2 | score | daily |
| LEAD-R15-E1 | LEAD-R15 | transcript | transcript.delivery_claims | deterministic | transcript.completion_claims_without_confirmation | evaluator | = | 0 | claims | session-end |
| LEAD-R15-E2 | LEAD-R15 | transcript | transcript.delivery_claims | judgement | rubric-code-lead@1#delivery | team-retro | >= | 2 | score | daily |
| LEAD-R16-E1 | LEAD-R16 | transcript | hooks.role_turns | deterministic | transcript.lead_authored_changes | evaluator | = | 0 | changes | session-end |
| LEAD-R17-E1 | LEAD-R17 | github | retro.prs_open | deterministic | github.clean_gated_prs_unmerged_over_hour | evaluator | = | 0 | pull_requests | 3h |
| LEAD-R18-E1 | LEAD-R18 | transcript | transcript.outbound_messages | deterministic | transcript.messages_outside_allowed_kinds | evaluator | = | 0 | messages | session-end |

## Rubric mapping

Each row of the former team-retro code lead rubric maps to rules here and to a
check of [rubric-code-lead](../rubrics/rubric-code-lead.md).

| Rubric row | Rules | Checks |
|---|---|---|
| Gate progress | LEAD-R01 | gate-progress |
| Review and flow | LEAD-R02, LEAD-R17 | review-flow |
| Honest state | LEAD-R03, LEAD-R04 | honest-state |
| Fix rounds | LEAD-R05 | fix-rounds |
| Gate discipline | LEAD-R06 | gate-discipline |
| Pin discipline | LEAD-R07 | pin-discipline |
| Merge safety | LEAD-R08, LEAD-R09, LEAD-R10, LEAD-R11 | open-findings, merge-safety |
| One directory | LEAD-R12 | one-directory |
| Resources | LEAD-R13 | resources |
| Agent recovery | LEAD-R14 | agent-recovery |
| Delivery | LEAD-R15 | delivery |

## Evaluation notes

- Every rule has a deterministic evaluation, so none is judgement-only.
  Judgement evaluations are additional and are graded by team-retro.
- LEAD-R01-E1 is `n.a.` when no gate-path ticket was unblocked; the check
  `gate-progress` then grades whether the blocker has an owner.
- LEAD-R06-E1 counts a rerun after a failed gate too. The check
  `gate-discipline` scores a recorded, justified exception 1 and never
  overrides the deterministic verdict.
- LEAD-R02-E1 is `unavailable` when no open pull request lacks a reviewer,
  because a statistic over an empty population has no value.
- LEAD-R04 and LEAD-R10, LEAD-R11, LEAD-R16, LEAD-R17 and LEAD-R18 have no
  judgement evaluation.
- LEAD-R14: `WAITING` and `RECENT` agents are observed without nudging and are
  not idle. File ages, token totals and worker counts alone establish neither
  idle state nor capacity.
