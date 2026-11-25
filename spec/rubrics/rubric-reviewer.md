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

Quantitative checks (`rounds-to-clean`, `latency`) use supported ix-board
measurements and assessments only. Missing counts, rates, attribution or
configured thresholds are `n/a`, not a reason to count markers or findings by
hand. Qualitative findings still cite their source.

## Checks

| ID | Check | Scale |
|----|-------|-------|
| rubric-reviewer@1#one-reviewer | Each pull request had exactly one distinct `run=` value across its `reviewer` markers. Evidence: `reviewer` markers (`run=`, `pr=`). | 2: one run on every pull request; 1: one pull request had two; 0: several per pull request |
| rubric-reviewer@1#author-independence | No reviewer reviewed work it authored. Evidence: `reviewer` markers, pull request commits, dispatch records. | 2: every review independent of the author; 1: an authored review found and replaced by an independent one before merge; 0: the author's review stood as the review |
| rubric-reviewer@1#record | Every reviewed pull request has a marked review comment on its ticket. Evidence: `linear issue comment list <TICKET> --json`. | 2: every method's review on the ticket; 1: one method's comment missing; 0: review only on the pull request or in chat |
| rubric-reviewer@1#marker-fields | Every marker comment carries `id=`, `method=`, `pr=` and `run=`. Evidence: marker first lines. | 2: all fields on every marker; 1: one marker missing a field; 0: several markers missing fields |
| rubric-reviewer@1#dispositions | No finding's latest outcome is still-open at merge. Evidence: disposition markers. | 2: none open at merge; 1: one open at merge with a recorded reason; 0: open at merge with no reason |
| rubric-reviewer@1#rounds-to-clean | The pull request reached clean within the current round policy. Evidence: ix-board round policy assessment. | 2: the emitted round assessment meets policy; 1: an excess with an owned remedy; 0: an excess ignored |
| rubric-reviewer@1#findings-quality | Every finding row names a file or line and a failure scenario. Evidence: review comments. | 2: every row has both; 1: at most a third of rows lack one; 0: more than a third lack one |
| rubric-reviewer@1#scope | Every finding's file is in the pull request's file list. Evidence: `gh pr view --json files`, review comments. | 2: every finding inside the list; 1: one outside; 0: several outside |
| rubric-reviewer@1#latency | Review age meets the configured policy. Evidence: ix-board reviewer age and queue assessment. | 2: the emitted review age assessment meets policy; 1: a breach with a corrective owner; 0: a known review stall ignored |

## Notes

- A missing measurement is never read as zero.
- Read next: the [strategies](../../skills/team-retro/references/strategies.md)
  entries "Tier the review" and "One gate per pull request".
