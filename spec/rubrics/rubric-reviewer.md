---
id: rubric-reviewer
version: 1
type: Rubric
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
---
# Rubric: reviewer

The reviewer rubric grades the judgement evaluations of the
[reviewer role spec](../roles/reviewer.md). `/team-retro` grades it. A
judgement evaluation cites one check as `rubric-reviewer@1#<check-slug>`.

Each check scores 0, 1 or 2 with one cited piece of evidence, or `n/a` when the
evidence was not read. `n/a` is listed under Data quality and is never counted
as 0 or 2. Scores are not averaged. A judgement score never overrides a
deterministic verdict on the same rule.

The quantitative check `rounds-to-clean` uses supported ix-board
measurements and assessments only. Missing counts, rates, attribution or
configured thresholds are `n/a`, not a reason to count markers or findings by
hand. The other checks cite their source records.

## Checks

| ID | Check | Scale |
|----|-------|-------|
| rubric-reviewer@1#one-reviewer | Each pull request had one independent reviewer, resumed for disposition passes. A retry or recorded replacement posts only what is missing. Evidence: `reviewer` markers (`run=`, `pr=`, `method=`), dispatch records. | 2: one reviewer on every pull request, or a recorded replacement; 1: one replacement with no recorded handoff; 0: two reviewers covering one pull request side by side, or a method reviewed twice |
| rubric-reviewer@1#author-independence | No reviewer reviewed work it authored. Evidence: `reviewer` markers, pull request commits, dispatch records. | 2: every review independent of the author; 1: an authored review found and replaced by an independent one before merge; 0: the author's review stood as the review |
| rubric-reviewer@1#record | Every reviewed pull request has a marked review comment on its ticket. Evidence: `linear issue comment list <TICKET> --json`. | 2: every method's review on the ticket; 1: one method's comment missing; 0: review only on the pull request or in chat |
| rubric-reviewer@1#marker-fields | Every marker comment carries the fields its kind requires (FR-017). Evidence: marker first lines. | 2: all fields on every marker; 1: one marker missing a field; 0: several markers missing fields |
| rubric-reviewer@1#dispositions | Every finding open before a disposition pass got an outcome in it. Evidence: disposition markers. | 2: every open finding got an outcome; 1: one missed and recorded in the next pass; 0: a finding left with no outcome |
| rubric-reviewer@1#mergeable-report | The reviewer reported a pull request mergeable only with every finding closed. Evidence: disposition markers (`mergeable=`), the reviewer's report. | 2: every statement matched the outcomes; 1: a wrong statement the reviewer corrected before the merge; 0: reported mergeable with an open finding |
| rubric-reviewer@1#rounds-to-clean | The pull request reached clean within the current round policy. Evidence: ix-board round policy assessment. | 2: the emitted round assessment meets policy; 1: an excess with an owned remedy; 0: an excess ignored |
| rubric-reviewer@1#findings-quality | Every finding row names a file or line and a failure scenario. Evidence: review comments. | 2: every row has both; 1: at most a third of rows lack one; 0: more than a third lack one |
| rubric-reviewer@1#scope | Every finding is on a changed file, or shows the failing result observed at its path. Evidence: `gh pr view --json files`, review comments. | 2: every finding meets this; 1: one outside the diff without an observed failure; 0: several |
| rubric-reviewer@1#latency | Each review was posted within the review age limit of its dispatch. Evidence: dispatch time, comment times. | 2: every review within the limit; 1: a breach with a corrective owner; 0: a known review stall ignored |
| rubric-reviewer@1#comms | Every message is done, blocked, decision, handoff or the one-line etiquette reply. Evidence: the session's sends. | 2: every message is one of those; 1: one other message; 0: several |

## Notes

- A missing measurement is never read as zero.
- Read next: the [strategies](../../skills/team-retro/references/strategies.md)
  entries "Tier the review" and "One gate per pull request".
