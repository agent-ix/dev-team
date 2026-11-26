---
id: REV
role: reviewer
version: 3
type: RoleSpec
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-017
    type: depends_on
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
and never changes the branch. It does not fix findings or merge: the
[coder](coder.md) fixes and the [code lead](code-lead.md) dispatches and merges.

Targets are initial values. The evaluator's role rows (dev-team FR-008) show
whether a target is met and whether a rule moves its objective; the director
proposes changes through a role spec version bump.

## Query sources and producers

A query reference is `<source>.<name>`, an evaluator query that
`ix-board retro eval` (SWM-221) registers. The source prefix names the store the
query reads: `retro` (the ix-board department report, ix-board FR-029), `prom`
(series of the ix-board team exporter, ix-board FR-033; `prom.ix_team_<name>` is
the series `ix_team_<name>`), `github` (pull request records), `linear` (the
marker comments of
[FR-017](../functional/FR-017-role-evaluation-records.md)) and `transcript` (the
evaluated session's transcript, read with the terms of FR-017).

Terms such as finding, closed, clean time and send are those of FR-017. Counts
are over the evaluation window and the team's scope; a session row of a `linear`
query counts the comments that session posted. `retro` and `prom` values cover a
team, not one session: a role row uses the value, and a session row is
`unavailable` unless the scope and window hold exactly one session of this role
(dev-team FR-001, FR-008). A value whose configuration is absent is
`unavailable`.

The Producer column states what exists on ix-board `origin/main`: `computed`
means ix-board computes the value today and only its registration as an
evaluator query is open; `none` means no ix-board requirement defines it.

| Query | Source and fields | Counting rule | Producer |
|---|---|---|---|
| prom.ix_team_new_pr_first_review_median_seconds_24h | exporter series | As ix-board FR-033: median seconds from a new pull request to its first recorded review | computed (ix-board FR-033) |
| prom.ix_team_new_pr_first_review_p90_seconds_24h | exporter series | The 90th percentile of the same delays | computed (ix-board FR-033) |
| prom.ix_team_review_findings_rejected_24h | exporter series | As ix-board FR-033: findings whose latest disposition is `rejected` | computed (ix-board FR-033) |
| retro.review_round_policy_excess | department report | As ix-board FR-029: pull requests above the configured review round limit | computed (ix-board FR-029) |
| linear.review_to_clean_median_hours | marker creation times, data blocks | Over pull requests whose clean time is in the window: hours from the first `reviewer` comment to the clean time, median; a review with no findings is included | none |
| linear.review_markers | marker first lines | `reviewer` and `reviewer-dispositions` comments created in the window | none |
| linear.reviewed_prs | `reviewer` comments; GitHub merge state | Pull requests with a `reviewer` comment created in the window, and pull requests merged in the window | none |
| linear.pr_methods_with_multiple_runs | `reviewer` fields `pr`, `method`, `run` | Pairs of pull request and method, for the pull requests of `linear.reviewed_prs`, whose `reviewer` comments carry more than one `run` | none |
| linear.review_markers_missing_fields | marker first lines | Comments of `linear.review_markers` lacking a field FR-017 requires of their kind | none |
| linear.disposition_rounds | `reviewer-dispositions` fields `repo`, `id`, `round` | Distinct pairs of pull request and round with a comment created in the window | none |
| linear.findings_without_outcome_after_disposition | marker data blocks | For each pair of `linear.disposition_rounds`: findings recorded before the round's first comment, open then, with no row in any comment of the round | none |
| linear.mergeable_yes_with_open_finding | `mergeable` field, data blocks | Pairs of `linear.disposition_rounds` with a comment saying `mergeable=yes` while, after the round's last comment, a finding of the pull request is open | none |
| linear.merged_prs_without_review_record | GitHub merged pull requests; `reviewer` field `pr` | Pull requests merged in the window with no `reviewer` comment on their ticket naming them | none |
| linear.review_findings | marker data blocks | Findings first recorded in the window | none |
| linear.findings_without_location_or_scenario | finding fields `path`, `lines`, `finding` | Findings of `linear.review_findings` with `path` and `lines` both empty, or `finding` empty | none |
| linear.outside_diff_findings_without_failure | finding fields `path`, `outside_diff_failure`; GitHub file list | Findings whose `path` is not in the pull request's file list and whose `outside_diff_failure` is empty or absent | none |
| linear.review_comments_unparseable_or_incomplete | comment bodies | Comments of `linear.review_markers` whose yaml block does not parse or lacks a field FR-017 requires of its data | none |
| transcript.review_passes | incoming messages, tool calls | Spans from an incoming message to the next that hold a command matching `linear issue comment add` | none |
| transcript.review_passes_over_age_limit | same, times; `eval.review_age_limit_hours` | Review passes whose first `linear issue comment add` is later than the incoming message's time plus the review age limit | none |
| transcript.reviewer_branch_commits | tool calls: command, working directory | Commands matching `git commit` or `git push` run in the reviewed worktree or naming the reviewed branch | none |
| transcript.reviewer_github_posts_beyond_ticket_id | tool calls: command | Commands matching `gh pr comment`, `gh pr review`, `gh issue comment`, or `gh api` writing to a comments or reviews endpoint, other than `gh pr comment` whose body is exactly one tracker key | none |
| transcript.outbound_messages | sends | The session's sends | none |

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
| REV-R01 | Each review method SHALL be run on a pull request by only one reviewer run. | REV-O02 | multiple-reviewers | Rubric row One reviewer; strategy "Tier the review" |
| REV-R02 | A reviewer SHALL NOT review a pull request it authored. | REV-O03 | self-review | Rubric row One reviewer; no agent reviews its own work, code-lead skill |
| REV-R03 | The reviewer SHALL NOT commit or push to the branch it reviews, and its review records SHALL stay on the ticket, never in the pull request. | REV-O02 | reviewer-edits-branch | A branch changed mid-review leaves the reviewed diff stale, code-lead freeze step |
| REV-R04 | The reviewer SHALL post each method's review to the pull request's ticket. | REV-O02 | review-unrecorded | Rubric row Record; a brief without the role left findings nowhere durable, code-lead never list |
| REV-R05 | Every reviewer marker comment SHALL carry the fields its kind requires. | REV-O02 | marker-incomplete | Rubric row Record |
| REV-R06 | The reviewer SHALL NOT post findings, excerpts or review sections to a GitHub pull request or issue. | REV-O03 | findings-leaked | Reviewer skill step 7: findings on a public pull request are published |
| REV-R07 | Each disposition pass SHALL record an outcome for every finding that was open before it, judged from the fix diff and its tests, not from a second full review unless a rule changed. | REV-O02 | disposition-missing | Rubric row Dispositions |
| REV-R08 | The reviewer SHALL NOT report a pull request mergeable while one of its findings is open. | REV-O02 | open-finding-mergeable | Rubric row Dispositions: findings open at merge |
| REV-R09 | Each pull request SHALL reach a clean disposition within the current review round policy. | REV-O02 | round-excess | Rubric row Rounds to clean |
| REV-R10 | Every finding SHALL name a file or line and a failure scenario. | REV-O03 | unactionable-finding | Rubric row Findings quality |
| REV-R11 | A finding on a file outside the pull request's file list SHALL carry the failing result observed at that path. | REV-O03 | out-of-scope-finding | Rubric row Scope; reviewer brief, same bug elsewhere |
| REV-R12 | The reviewer SHALL post its review within the review age limit of its dispatch. | REV-O01 | review-stall | Rubric row Latency |
| REV-R13 | The reviewer SHALL read each posted comment back and repair one whose data block does not parse or lacks a required field. | REV-O02 | broken-review-data | 3 of 123 reviewer comments did not parse and 19 of 65 fixed rows lacked `after_excerpt`, reviewer skill step 9 |
| REV-R14 | The reviewer SHALL NOT send a message other than done, blocked, decision, handoff or the one-line etiquette reply. | REV-O01 | comms-noise | Status polls and progress messages between lanes, reviewer skill Communication |
| REV-R15 | The reviewer SHALL select its review methods from the diff, sized to the change, record the methods and why in the review comment, and SHALL NOT ask the user which methods to run. | REV-O02 | method-overreach | Every applicable method run on every pull request, 2026-11-26 |
| REV-R16 | For a Block, the reviewer SHALL review the design note before the diff (is the cause class right, are other sites missed, would the class-level tests fail on an unfixed site), then the diff, and SHALL post its findings on the ticket. | REV-O02 | design-unreviewed | Five consolidation leads fixed a Block's tickets one after another inside one pull request, 2026-11-26 |

## Evaluations

| ID | Rule | Evidence source | Trigger | Method | Query or rubric | Evaluator | Comparator | Value | Unit | Cadence |
|---|---|---|---|---|---|---|---|---|---|---|
| REV-R01-E1 | REV-R01 | linear | linear.reviewed_prs | deterministic | linear.pr_methods_with_multiple_runs | evaluator | = | 0 | methods | 3h |
| REV-R01-E2 | REV-R01 | linear | linear.reviewed_prs | judgement | rubric-reviewer@3#one-reviewer | team-retro | >= | 2 | score | daily |
| REV-R02-E1 | REV-R02 | github | linear.reviewed_prs | judgement | rubric-reviewer@3#author-independence | team-retro | >= | 2 | score | daily |
| REV-R03-E1 | REV-R03 | transcript | transcript.review_passes | deterministic | transcript.reviewer_branch_commits | evaluator | = | 0 | commands | session-end |
| REV-R04-E1 | REV-R04 | linear | linear.reviewed_prs | deterministic | linear.merged_prs_without_review_record | evaluator | = | 0 | pull_requests | 3h |
| REV-R04-E2 | REV-R04 | linear | linear.reviewed_prs | judgement | rubric-reviewer@3#record | team-retro | >= | 2 | score | daily |
| REV-R05-E1 | REV-R05 | linear | linear.review_markers | deterministic | linear.review_markers_missing_fields | evaluator | = | 0 | markers | 3h |
| REV-R05-E2 | REV-R05 | linear | linear.review_markers | judgement | rubric-reviewer@3#marker-fields | team-retro | >= | 2 | score | daily |
| REV-R06-E1 | REV-R06 | transcript | transcript.review_passes | deterministic | transcript.reviewer_github_posts_beyond_ticket_id | evaluator | = | 0 | commands | session-end |
| REV-R07-E1 | REV-R07 | linear | linear.disposition_rounds | deterministic | linear.findings_without_outcome_after_disposition | evaluator | = | 0 | findings | 3h |
| REV-R07-E2 | REV-R07 | linear | linear.disposition_rounds | judgement | rubric-reviewer@3#dispositions | team-retro | >= | 2 | score | daily |
| REV-R08-E1 | REV-R08 | linear | linear.disposition_rounds | deterministic | linear.mergeable_yes_with_open_finding | evaluator | = | 0 | passes | 3h |
| REV-R08-E2 | REV-R08 | linear | linear.disposition_rounds | judgement | rubric-reviewer@3#mergeable-report | team-retro | >= | 2 | score | daily |
| REV-R09-E1 | REV-R09 | ix-board-metric | linear.reviewed_prs | deterministic | retro.review_round_policy_excess | evaluator | = | 0 | pull_requests | 3h |
| REV-R09-E2 | REV-R09 | linear | linear.reviewed_prs | judgement | rubric-reviewer@3#rounds-to-clean | team-retro | >= | 2 | score | daily |
| REV-R10-E1 | REV-R10 | linear | linear.review_findings | deterministic | linear.findings_without_location_or_scenario | evaluator | = | 0 | findings | 3h |
| REV-R10-E2 | REV-R10 | linear | linear.review_findings | judgement | rubric-reviewer@3#findings-quality | team-retro | >= | 2 | score | daily |
| REV-R11-E1 | REV-R11 | linear | linear.review_findings | deterministic | linear.outside_diff_findings_without_failure | evaluator | = | 0 | findings | 3h |
| REV-R11-E2 | REV-R11 | github | linear.review_findings | judgement | rubric-reviewer@3#scope | team-retro | >= | 2 | score | daily |
| REV-R12-E1 | REV-R12 | transcript | transcript.review_passes | deterministic | transcript.review_passes_over_age_limit | evaluator | = | 0 | passes | session-end |
| REV-R12-E2 | REV-R12 | ix-board-metric | linear.reviewed_prs | judgement | rubric-reviewer@3#latency | team-retro | >= | 2 | score | daily |
| REV-R13-E1 | REV-R13 | linear | linear.review_markers | deterministic | linear.review_comments_unparseable_or_incomplete | evaluator | = | 0 | comments | 3h |
| REV-R14-E1 | REV-R14 | transcript | transcript.outbound_messages | judgement | rubric-reviewer@3#comms | team-retro | >= | 2 | score | daily |
| REV-R15-E1 | REV-R15 | linear | linear.review_markers | judgement | rubric-reviewer@3#method-selection | team-retro | >= | 2 | score | daily |
| REV-R16-E1 | REV-R16 | linear | linear.review_markers | judgement | rubric-reviewer@3#block-design-review | team-retro | >= | 2 | score | daily |

## Rubric mapping

Each row of the former team-retro reviewer rubric maps to rules here and to a
check of [rubric-reviewer](../rubrics/rubric-reviewer.md). The `comms` check
grades the reviewer skill's Communication section, which had no row.

| Rubric row | Rules | Checks |
|---|---|---|
| One reviewer | REV-R01, REV-R02 | one-reviewer, author-independence |
| Record | REV-R04, REV-R05 | record, marker-fields |
| Dispositions | REV-R07, REV-R08 | dispositions, mergeable-report |
| Rounds to clean | REV-R09 | rounds-to-clean |
| Findings quality | REV-R10 | findings-quality |
| Scope | REV-R11 | scope |
| Latency | REV-R12 | latency |
| Method selection | REV-R15 | method-selection |
| Block design review | REV-R16 | block-design-review |

## Evaluation notes

- Judgement-only rules, graded by team-retro and flagged under dev-team FR-006:
  REV-R02, because no source attributes pull request authorship to a reviewer
  run, and REV-R14, because a message's kind is the meaning of its prose.
- REV-R01 allows a retried or replacement dispatch to post the methods not yet
  on the ticket under a new `run`; a second run of a posted method is counted.
  The check `one-reviewer` grades two runs that split the methods between them.
- REV-R03 permits a temporary mutation of the worktree that shows a test fails,
  reverted before the pass ends.
- REV-R04-E1 and the code lead's LEAD-R10-E1 read the same query: a merged
  pull request with no record breaks the reviewer's posting rule and the
  [code lead](code-lead.md)'s merge rule.
- Merging with an open finding is the code lead's failure (LEAD-R08), never the
  reviewer's: REV-R08 grades only what the reviewer reports.
- REV-R12 measures the reviewer from its own dispatch. A pull request still
  waiting for a reviewer is the code lead's (LEAD-R02).
- A clean review posts `findings: []`; REV-R10 and REV-R11 are then `n.a.`.
