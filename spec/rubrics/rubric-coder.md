---
id: rubric-coder
version: 3
type: Rubric
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
---
# Rubric: coder

The coder rubric grades the judgement evaluations of the
[coder role spec](../roles/coder.md). `/team-retro` grades it from the coder's
pull request and report, never by asking the coder. A judgement evaluation cites
one check as `rubric-coder@3#<check-slug>`.

Each check scores 0, 1 or 2 with one cited piece of evidence, or `n/a` when the
evidence was not read. `n/a` is listed under Data quality and is never counted
as 0 or 2. Scores are not averaged. A judgement score never overrides a
deterministic verdict on the same rule.

Quantitative checks (`size`, `rounds`) use supported ix-board measurements and
assessments only. If a requested count, rate or threshold comparison is not
emitted, score the check `n/a`; do not reconstruct it by counting markers or
pull requests by hand.

## Checks

| ID | Check | Scale |
|----|-------|-------|
| rubric-coder@3#size | The pull request fits the configured size policy; with none configured, or for a Block, the check is n/a. Evidence: ix-board pull request size assessment, the ticket. | 2: the emitted size assessment meets policy; 1: an excess with a recorded split; 0: an excess left without remedy |
| rubric-coder@3#scope | Every changed file belongs to the ticket's scope. Evidence: `gh pr view --json files`, the ticket, the files other lanes own. | 2: all changed files belong; 1: one unrelated file; 0: several, or a change in another lane's files |
| rubric-coder@3#rounds | The pull request reached clean within the current review round policy. Evidence: ix-board round policy assessment. | 2: the emitted round assessment meets policy; 1: an excess with an owned remedy; 0: an excess ignored |
| rubric-coder@3#rework-cause | Every finding fixed in a round has a `fixed` outcome in the next disposition round. Evidence: `reviewer-dispositions` markers. | 2: no finding returned still-open; 1: one finding returned `still-open` once; 0: a finding returned `still-open` twice |
| rubric-coder@3#finding-pull-request | The coder opened no second pull request for a finding on its open pull request. A stacked part of a split recorded on the ticket, and other work of the ticket, is not one. Evidence: the second pull requests of the ticket, their descriptions and changes, the findings, the split record. | 2: none opened for a finding; 1: one opened, then closed and folded back into the pull request; 0: a finding fixed or left to a second pull request |
| rubric-coder@3#finding-ticket | The coder opened no new ticket for a finding on its open pull request; it reported items owned elsewhere for the leader to file. Evidence: the session's ticket creations and the report. | 2: none opened; 1: one opened, then folded back into the pull request; 0: a finding left to a new ticket |
| rubric-coder@3#one-directory | The coder worked only in the assigned directory. Evidence: the `local_paths` listing, the transcript. | 2: only the assigned directory; 1: one stray directory, removed; 0: a clone or worktree created for review or gate |
| rubric-coder@3#false-done | No done claim was made over a failing check. Evidence: pull request, check logs, the report. | 2: no done claim over a failing check; 1: a wrong done claim the coder corrected before anyone acted on it; 0: reported done while checks fail |
| rubric-coder@3#honest-report | The report names what is done, what is not and what failed. Evidence: pull request, check logs, the report. | 2: all three named; 1: one failed or unfinished item missing; 0: several missing, or the report omits that anything failed or is unfinished |
| rubric-coder@3#report-timing | Every coder report came after the checks it cites had finished. Evidence: check logs, report timestamps. | 2: every report timestamped after the checks it cites; 1: one report earlier than a cited check's finish; 0: several |
| rubric-coder@3#review-files | No commit of the pull request adds or changes a reviewer SR file; review records live on the tracker ticket. Evidence: pull request commits and files. | 2: no SR file in the pull request; 1: one removed before review returned; 0: SR files committed in fix rounds |
| rubric-coder@3#block-structure | In a Block, the coder implemented the structure or mechanism chosen in the design note and added the tests of its kind; each ticket-specific exception has the lead's written reason on the ticket. Evidence: pull request commits and files, the design note, ticket comments. | 2: structure and tests present, no unexplained exception; 1: one unexplained exception; 0: tickets built one by one with no shared structure. n/a outside a Block |
| rubric-coder@3#comms | Every message is done, blocked, decision, handoff or the one-line etiquette reply. Evidence: the session's sends. | 2: every message is one of those; 1: one other message; 0: several |

## Notes

- A missing measurement is never read as zero.
- Read next: the [strategies](../../skills/team-retro/references/strategies.md)
  entry "Split large pull requests".
