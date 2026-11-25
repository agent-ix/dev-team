---
id: REV
role: reviewer
version: 1
type: RoleSpec
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
  - target: ix://agent-ix/ix-board/FR-029
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-033
    type: depends_on
---
# Role spec: reviewer

## Purpose

The reviewer gives one pull request its one independent review: it runs every
review method the change needs in one pass, writes each method's review
artifact, posts marked findings to the project's ticket tracker, and records an
outcome for every finding in later disposition passes. It reads the frozen diff
and never edits it. It does not fix findings or merge: the [coder](coder.md)
fixes and the [code lead](code-lead.md) dispatches and merges.

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
- `github`: pull request records, comments and file lists.
- `linear`: ticket comments, read as `reviewer` and `reviewer-dispositions`
  markers and their data blocks.
- `hooks`: hook activity events (ix-relay FR-068) of the evaluated session.
- `transcript`: the evaluated session's transcript, read by a fixed pattern
  query.

`retro` and `prom` values cover a team's scope and window, not one session. A
role row uses the value; a session row is `unavailable` unless the scope and
window hold exactly one session of this role (dev-team FR-001, FR-008). A
department or exporter value whose configuration is absent is `unavailable`.

The Producer column states what exists on ix-board `origin/main`: `computed`
means ix-board computes the value today and only its registration as an
evaluator query is open (SWM-221); `none` means no ix-board requirement defines
it, and the named ticket owns the producer.

| Query | Counts | Producer |
|---|---|---|
| prom.ix_team_new_pr_first_review_median_seconds_24h | Median seconds from a new pull request to its first recorded review, 24 hours | computed (ix-board FR-033) |
| prom.ix_team_new_pr_first_review_p90_seconds_24h | The 90th percentile of the same delays | computed (ix-board FR-033) |
| prom.ix_team_review_findings_rejected_24h | Findings whose latest disposition is `rejected`, 24 hours | computed (ix-board FR-033) |
| retro.review_round_policy_excess | Pull requests above the configured review round limit | computed (ix-board FR-029) |
| linear.review_to_clean_median_hours | Median hours from a pull request's first `reviewer` marker to the disposition after which no finding is still-open or without outcome, over pull requests that reached that state in the window | none (SWM-261) |
| linear.review_markers | `reviewer` and `reviewer-dispositions` comments posted in the window for the evaluated run or scope | none (SWM-261) |
| linear.reviewed_prs | Pull requests with a review recorded or dispatched in the window | none (SWM-261) |
| linear.prs_with_multiple_reviewer_runs | Reviewed pull requests whose `reviewer` markers carry more than one `run=` value | none (SWM-261) |
| linear.review_markers_missing_fields | `reviewer` markers lacking `id=`, `method=`, `pr=` or `run=` | none (SWM-261) |
| linear.disposition_rounds | Disposition passes run in the window | none (SWM-261) |
| linear.findings_without_outcome_after_disposition | Findings that were still-open or without outcome before a disposition pass and got no row in it | none (SWM-261) |
| linear.merged_prs_without_review_record | Pull requests merged in the window with no `reviewer` marker naming them on their ticket | none (SWM-261) |
| linear.review_findings | Findings in `reviewer` data blocks posted in the window | none (SWM-261) |
| linear.findings_without_location_or_scenario | Findings with an empty `path` and `lines`, or an empty `finding` text | none (SWM-261) |
| linear.findings_outside_pr_files | Findings whose `path` is not in the pull request's file list | none (SWM-261) |
| linear.review_comments_unparseable_or_incomplete | Review comments whose data block does not parse, or that lack a required field, including `after_excerpt` on a `fixed` row and `reason` on any other outcome | none (SWM-261) |
| github.pr_comments_carrying_findings | GitHub pull request or issue comments by the reviewer that carry a finding id, excerpt or review section | none (SWM-261) |
| hooks.role_turns | Turns of the evaluated session in the window | none (SWM-221) |
| transcript.review_passes | Review passes the session ran | none (SWM-221) |
| transcript.review_passes_over_age_limit | Review passes whose first posted comment came later than the configured review age limit after dispatch | none (SWM-221) |
| transcript.reviewer_branch_writes | File edits, commits or pushes the session made in the reviewed worktree or branch | none (SWM-221) |
| transcript.mergeable_reports_with_open_finding | Reports calling a pull request mergeable while a finding's latest outcome is `still-open` or missing | none (SWM-221) |
| transcript.mergeable_reports | Reports that state whether a pull request is mergeable | none (SWM-221) |
| transcript.outbound_messages | Messages the session sent to another agent | none (SWM-221) |
| transcript.messages_outside_allowed_kinds | Outbound messages that are not done, blocked, decision, handoff or the one-line etiquette reply | none (SWM-221) |

## Metrics

| ID | Name | Evidence source | Query | Unit | Target | Direction |
|---|---|---|---|---|---|---|
| REV-M01 | Pull request to first review, median | ix-board-metric | prom.ix_team_new_pr_first_review_median_seconds_24h | seconds | 3600 | lower |
| REV-M02 | Pull request to first review, p90 | ix-board-metric | prom.ix_team_new_pr_first_review_p90_seconds_24h | seconds | 14400 | lower |
| REV-M03 | Review-to-clean time, median | linear | linear.review_to_clean_median_hours | hours | 4 | lower |
| REV-M04 | Findings rejected as not defects, 24 hours | ix-board-metric | prom.ix_team_review_findings_rejected_24h | findings | 1 | lower |

## Objectives

| ID | Objective | Metrics |
|---|---|---|
| REV-O01 | A frozen pull request gets its review quickly | REV-M01, REV-M02 |
| REV-O02 | A reviewed pull request reaches mergeable in few passes | REV-M03 |
| REV-O03 | Review findings are real defects the coder can act on | REV-M04 |

## Rules

| ID | Rule | Objective | Class | Source |
|---|---|---|---|---|
| REV-R01 | Each reviewed pull request SHALL carry reviews from exactly one reviewer run. | REV-O02 | multiple-reviewers | Rubric row One reviewer; strategy "Tier the review" |
| REV-R02 | A reviewer SHALL NOT review a pull request it authored. | REV-O03 | self-review | Rubric row One reviewer; no agent reviews its own work, code-lead skill |
| REV-R03 | The reviewer SHALL NOT edit, commit or push to the branch it reviews. | REV-O02 | reviewer-edits-branch | A branch changed mid-review leaves the reviewed diff stale, code-lead freeze step |
| REV-R04 | The reviewer SHALL post each method's review to the pull request's ticket. | REV-O02 | review-unrecorded | Rubric row Record; a brief without the role left findings nowhere durable, code-lead never list |
| REV-R05 | Every review marker SHALL carry the `id=`, `method=`, `pr=` and `run=` fields. | REV-O02 | marker-incomplete | Rubric row Record |
| REV-R06 | The reviewer SHALL NOT post findings, excerpts or review sections to a GitHub pull request or issue. | REV-O03 | findings-leaked | Reviewer skill step 7: findings on a public pull request are published |
| REV-R07 | Each disposition pass SHALL record an outcome for every finding whose latest outcome is still-open or missing. | REV-O02 | disposition-missing | Rubric row Dispositions |
| REV-R08 | The reviewer SHALL NOT report a pull request mergeable while a finding's latest outcome is still-open or missing. | REV-O02 | open-finding-mergeable | Rubric row Dispositions: findings open at merge |
| REV-R09 | Each pull request SHALL reach a clean disposition within the current review round policy. | REV-O02 | round-excess | Rubric row Rounds to clean |
| REV-R10 | Every finding SHALL name a file or line and a failure scenario. | REV-O03 | unactionable-finding | Rubric row Findings quality |
| REV-R11 | Every finding SHALL be on a file in the pull request's file list. | REV-O03 | out-of-scope-finding | Rubric row Scope; review the diff only |
| REV-R12 | The reviewer SHALL post its review within the configured review age limit of its dispatch. | REV-O01 | review-stall | Rubric row Latency |
| REV-R13 | The reviewer SHALL read each posted comment back and repair one whose data block does not parse or lacks a required field. | REV-O02 | broken-review-data | 3 of 123 reviewer comments did not parse and 19 of 65 fixed rows lacked `after_excerpt`, reviewer skill step 9 |
| REV-R14 | The reviewer SHALL NOT send a message other than done, blocked, decision, handoff or the one-line etiquette reply. | REV-O01 | comms-noise | Status polls and progress messages between lanes, reviewer skill Communication |

## Evaluations

| ID | Rule | Evidence source | Trigger | Method | Query or rubric | Evaluator | Comparator | Value | Unit | Cadence |
|---|---|---|---|---|---|---|---|---|---|---|
| REV-R01-E1 | REV-R01 | linear | linear.reviewed_prs | deterministic | linear.prs_with_multiple_reviewer_runs | evaluator | = | 0 | pull_requests | 3h |
| REV-R01-E2 | REV-R01 | linear | linear.reviewed_prs | judgement | rubric-reviewer@1#one-reviewer | team-retro | >= | 2 | score | daily |
| REV-R02-E1 | REV-R02 | github | linear.reviewed_prs | judgement | rubric-reviewer@1#author-independence | team-retro | >= | 2 | score | daily |
| REV-R03-E1 | REV-R03 | transcript | transcript.review_passes | deterministic | transcript.reviewer_branch_writes | evaluator | = | 0 | writes | session-end |
| REV-R04-E1 | REV-R04 | linear | linear.reviewed_prs | deterministic | linear.merged_prs_without_review_record | evaluator | = | 0 | pull_requests | 3h |
| REV-R04-E2 | REV-R04 | linear | linear.reviewed_prs | judgement | rubric-reviewer@1#record | team-retro | >= | 2 | score | daily |
| REV-R05-E1 | REV-R05 | linear | linear.review_markers | deterministic | linear.review_markers_missing_fields | evaluator | = | 0 | markers | 3h |
| REV-R05-E2 | REV-R05 | linear | linear.review_markers | judgement | rubric-reviewer@1#marker-fields | team-retro | >= | 2 | score | daily |
| REV-R06-E1 | REV-R06 | github | hooks.role_turns | deterministic | github.pr_comments_carrying_findings | evaluator | = | 0 | comments | 3h |
| REV-R07-E1 | REV-R07 | linear | linear.disposition_rounds | deterministic | linear.findings_without_outcome_after_disposition | evaluator | = | 0 | findings | 3h |
| REV-R08-E1 | REV-R08 | transcript | transcript.mergeable_reports | deterministic | transcript.mergeable_reports_with_open_finding | evaluator | = | 0 | reports | session-end |
| REV-R08-E2 | REV-R08 | linear | linear.reviewed_prs | judgement | rubric-reviewer@1#dispositions | team-retro | >= | 2 | score | daily |
| REV-R09-E1 | REV-R09 | ix-board-metric | linear.reviewed_prs | deterministic | retro.review_round_policy_excess | evaluator | = | 0 | pull_requests | 3h |
| REV-R09-E2 | REV-R09 | linear | linear.reviewed_prs | judgement | rubric-reviewer@1#rounds-to-clean | team-retro | >= | 2 | score | daily |
| REV-R10-E1 | REV-R10 | linear | linear.review_findings | deterministic | linear.findings_without_location_or_scenario | evaluator | = | 0 | findings | 3h |
| REV-R10-E2 | REV-R10 | linear | linear.review_findings | judgement | rubric-reviewer@1#findings-quality | team-retro | >= | 2 | score | daily |
| REV-R11-E1 | REV-R11 | linear | linear.review_findings | deterministic | linear.findings_outside_pr_files | evaluator | = | 0 | findings | 3h |
| REV-R11-E2 | REV-R11 | github | linear.review_findings | judgement | rubric-reviewer@1#scope | team-retro | >= | 2 | score | daily |
| REV-R12-E1 | REV-R12 | transcript | transcript.review_passes | deterministic | transcript.review_passes_over_age_limit | evaluator | = | 0 | passes | session-end |
| REV-R12-E2 | REV-R12 | ix-board-metric | linear.reviewed_prs | judgement | rubric-reviewer@1#latency | team-retro | >= | 2 | score | daily |
| REV-R13-E1 | REV-R13 | linear | linear.review_markers | deterministic | linear.review_comments_unparseable_or_incomplete | evaluator | = | 0 | comments | 3h |
| REV-R14-E1 | REV-R14 | transcript | transcript.outbound_messages | deterministic | transcript.messages_outside_allowed_kinds | evaluator | = | 0 | messages | session-end |

## Rubric mapping

Each row of the former team-retro reviewer rubric maps to rules here and to a
check of [rubric-reviewer](../rubrics/rubric-reviewer.md).

| Rubric row | Rules | Checks |
|---|---|---|
| One reviewer | REV-R01, REV-R02 | one-reviewer, author-independence |
| Record | REV-R04, REV-R05 | record, marker-fields |
| Dispositions | REV-R07, REV-R08 | dispositions |
| Rounds to clean | REV-R09 | rounds-to-clean |
| Findings quality | REV-R10 | findings-quality |
| Scope | REV-R11 | scope |
| Latency | REV-R12 | latency |

## Evaluation notes

- Judgement-only rules, graded by team-retro and flagged under dev-team FR-006:
  REV-R02, because no source attributes pull request authorship to a reviewer
  run. Every other rule has a deterministic evaluation.
- REV-R04-E1 and the code lead's LEAD-R10-E1 read the same query: a merged
  pull request with no record breaks the reviewer's posting rule and the
  [code lead](code-lead.md)'s merge rule.
- REV-R08-E2 grades findings still open at merge; the merge itself is the code
  lead's (LEAD-R08).
- REV-R12-E1 measures the reviewer from its own dispatch. A pull request still
  waiting for a reviewer is the code lead's (LEAD-R02).
- A clean review posts `findings: []`; REV-R10 and REV-R11 are then `n.a.`.
