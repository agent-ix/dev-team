---
id: rubric-code-lead
version: 2
type: Rubric
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
---
# Rubric: code lead

The code lead rubric grades the judgement evaluations of the
[code lead role spec](../roles/code-lead.md). `/team-retro` grades it. A
judgement evaluation cites one check as `rubric-code-lead@2#<check-slug>`.

Each check scores 0, 1 or 2 with one cited piece of evidence, or `n/a` when the
evidence was not read. `n/a` is listed under Data quality and is never counted
as 0 or 2. Scores are not averaged. A judgement score never overrides a
deterministic verdict on the same rule.

Quantitative checks consume ix-board assessments under the team's current
policy; unsupported measurements score `n/a`. No fixed review cap or slot count
comes from this rubric.

## Checks

| ID | Check | Scale |
|----|-------|-------|
| rubric-code-lead@2#gate-progress | The gate path is moving. Evidence: snapshot and delta path measures. | 2: emitted progress improves; 1: flat with an owned blocker; 0: flat and the blocker ignored |
| rubric-code-lead@2#review-flow | Reviewers are dispatched within the review age limit. Evidence: flow assessment, dispatch records. | 2: every dispatch within the limit; 1: a corrective owner is active; 0: a known review stall left unattended |
| rubric-code-lead@2#merge-latency | Each pull request merged within one hour of becoming ready to merge, unless a repository, organization or user rule held it. Evidence: tracker markers and records, merge times, the holding rule. | 2: every merge within the hour or held by a cited rule; 1: a breach with a corrective owner; 0: a ready pull request left unmerged |
| rubric-code-lead@2#honest-state | Unworked gated and stale claims are reconciled. Evidence: stale claim assessment, the tracker. | 2: claims reconciled; 1: correction in progress; 0: a started claim persists against evidence |
| rubric-code-lead@2#fix-rounds | Review rounds meet the current policy. Evidence: round policy assessment. | 2: current policy met; 1: an excess with a recorded remedy; 0: an excess or repeating loop ignored |
| rubric-code-lead@2#gate-discipline | Iteration uses focused checks, and the aggregate gate is not run again without a reason: a failed run, an uncovered change or a repository or organization rule. Evidence: gate records, gate log. | 2: focused iteration and every rerun with a reason; 1: a rerun that a repository or organization rule required, lacking its waiver record; 0: repeated workspace gates without new evidence |
| rubric-code-lead@2#pin-discipline | Required pins ride the consuming pull request in its window. Evidence: pin assessment, dependency owner. | 2: required pins in the consuming pull request and window; 1: drift has an owner; 0: repin-only churn continues |
| rubric-code-lead@2#open-findings | Every finding is closed, by an outcome or a recorded one-line final fix, before the merge. Evidence: tracker markers and records. | 2: every finding closed before the merge; 1: a discrepancy corrected before the merge; 0: an open finding merged |
| rubric-code-lead@2#merge-safety | The merged head differs from the reviewed head only by a passing overlap rebase or a recorded one-line final fix. Evidence: tracker markers and records, pull request commits. | 2: the review covers every merged head; 1: a discrepancy corrected before the merge; 0: an unreviewed change merged |
| rubric-code-lead@2#gate-safety | A pull request that changes a file other than Markdown merged only with a passing gate covering the merged head, unless a repository or organization rule set another gate requirement. A Markdown-only pull request needs none. Evidence: gate and waiver records, the cited rule, pull request files and commits. | 2: every merge covered, exempt or under the cited rule; 1: a discrepancy corrected before the merge; 0: a required gate missing at a merge |
| rubric-code-lead@2#one-directory | One ticket shares one coder, reviewer and gate tree. Evidence: worktree evidence. | 2: one shared tree per ticket; 1: a stray tree corrected; 0: separate review or gate worktrees |
| rubric-code-lead@2#resources | The current capacity and admission source is honored. Evidence: host, queue and hold assessment. | 2: current source honored; 1: missing telemetry routed to its owner; 0: slots invented or reservations bypassed |
| rubric-code-lead@2#agent-recovery | A confirmed idle agent with ready work is acted on. Evidence: complete lifecycle report and ready queue. | 2: confirmed idle with ready work acted on; 1: remedy owned but pending; 0: a confirmed idle agent remains unassigned |
| rubric-code-lead@2#delivery | Outcomes are distinct and confirmation is cited. Evidence: pane, pull request or SHA, relay receipt chain. | 2: outcomes distinct with confirmation cited; 1: an unconfirmed action escalated; 0: queued or seen claimed as completion |
| rubric-code-lead@2#work-class | Each ticket group was classified Point, Batch, Block or Sweep, and the class default was applied unless an explicit task, ticket, project or owner instruction differed. Evidence: dispatch record, ticket comments, pull request list per repository. | 2: class named and default applied or the instruction cited; 1: class applied late and corrected; 0: a Block split into per-ticket pull requests with no instruction behind it |
| rubric-code-lead@2#fold-open-pr | Before a new pull request opened, the change was folded into an open pull request of the same Block when one existed. Evidence: pull requests of the repository and block, ticket comments. | 2: one pull request per Block per repository, or the exception named; 1: a second pull request merged into the first; 0: parallel pull requests for one Block |
| rubric-code-lead@2#tripwires | A pull request over 2 review rounds, over 15 commits, or open 3 hours with no movement was consolidated or recut, with one line on the ticket saying why. Evidence: pull request commits, review markers, ticket comments. | 2: every tripwire acted on with its line; 1: acted on late; 0: a pull request past a tripwire left running |
| rubric-code-lead@2#named-wait | Each tick a waiting lead named the exact wait and started the next independent step. Evidence: lead transcript, fleet status, ticket comments. | 2: every wait named with a next step started; 1: a wait named late; 0: idle or waiting over 20 minutes with no named wait |
| rubric-code-lead@2#merge-check | No merge check was rerun for a main move that did not overlap the pull request files. Evidence: rebase records, gate records, `git diff --name-only`. | 2: reruns only on overlap; 1: one needless rerun; 0: reruns on every main move |
| rubric-code-lead@2#waivers | Every waiver record covers a role rule that the repository, organization or direct user rule at its `ref` differs from. Evidence: waiver records, the cited text. | 2: every `ref` states a differing rule; 1: a wrong `ref` corrected before the merge; 0: a waiver with no differing rule behind it |
| rubric-code-lead@2#comms | Every message is done, blocked, decision, handoff or the one-line etiquette reply. Evidence: the session's sends. | 2: every message is one of those; 1: one other message; 0: several |

## Notes

- `WAITING` and `RECENT` are observed without nudging and do not fail
  `agent-recovery`.
- File ages, token totals and worker counts alone establish neither idle state
  nor capacity. Unknown or incomplete evidence remains `n/a`.
- Read next: the [strategies](../../skills/team-retro/references/strategies.md).
