---
id: FR-017
title: Record the facts that role evaluations count
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-002
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-006
    type: depends_on
  - target: ix://agent-ix/dev-team/FR-001
    type: depends_on
---
# FR-017: Record the facts that role evaluations count

## Description

The reviewer and code lead skills SHALL record each fact that a deterministic
role evaluation counts and that no source system holds by itself. The evaluator
(`ix-board retro eval`, SWM-221) SHALL compute the role specs' queries from
those records and the source systems under the definitions below. The query
tables of the role specs name each query's source fields and counting rule.

## Behavior

### Pull request identity

A pull request's ticket is the first tracker key in its head branch name, or
else in its title, whose prefix is a team key of the tracker. A pull request
whose ticket does not resolve has no records. A record names a pull request with
`repo=<owner>/<repo>` and `pr=<repo>#<n>`.

A pull request is ready for review from its creation time when it was opened as
non-draft, and otherwise from its first ready-for-review event. A draft is not
ready for review. A pull request requires a gate when it changes at least one
file whose name does not end in `.md`.

### Marker comments

A marker comment is a ticket comment whose first line is
`<!-- <kind> key=value ... -->`. A value contains no space. The record's time is
the comment's creation time, and its data is the comment's one fenced `yaml`
block.

| Marker | Producer | Required fields |
|---|---|---|
| `reviewer` | reviewer, one comment per method per run | `repo`, `id`, `method`, `pr`, `run`, `head` (the commit reviewed) |
| `reviewer-dispositions` | reviewer, per round, one comment for each review artifact that has findings; when none has, one on the first review artifact posted | `repo`, `id`, `round`, `run`, `head` (the commit checked), `mergeable` (`yes` or `no`, for the whole pull request after the pass) |
| `lead-record` with `kind=gate` | code lead, after every aggregate gate run | `repo`, `pr`, `kind`, `head` (the commit gated), `exit` (the gate command's exit status), `started` and `finished` (the `started_at` and `finished_at` of the gate log line) |
| `lead-record` with `kind=rebase` | code lead, after the confined check of an overlap rebase | `repo`, `pr`, `kind`, `from` (the head before the rebase), `head`, `exit` (the confined check's exit status) |
| `lead-record` with `kind=final-fix` | code lead, after reading a one-line final fix | `repo`, `pr`, `kind`, `from` (the head before the fix), `head`, `fnd` (the closed findings as `SR-NNN/FND-NNN`, comma separated) |
| `lead-record` with `kind=waiver` | code lead, when a repository, organization or direct user rule differs from a role rule for one pull request | `repo`, `pr`, `kind`, `covers` (the rule id), `ref` (the file or message that states the differing rule) |

A commit field holds the full commit hash.

### Review data

A `reviewer` data block holds `clean`, `scope` and `findings`. Each finding
holds `fnd`, `severity`, `confidence`, `method`, `check`, `artifact_id`,
`path`, `lines`, `excerpt` and `finding`. A finding whose `path` is not in the
pull request's file list also holds `outside_diff_failure`, the failing result
observed at that path.

A `reviewer-dispositions` data block holds `dispositions`, rows of `fnd` and
`outcome` (`fixed`, `rejected`, `deferred`, `accepted-no-change` or
`still-open`) with `after_excerpt` on a `fixed` row and `reason` on any other.
A pass that finds a new defect also lists it under `new_findings`, with the
fields of a review finding. `dispositions` is an empty list when the pass had no
finding to re-check, as when it reviews a change made after a clean review.

### Derived facts

- The **findings** of a pull request are each pair of review id and `fnd` in the
  `findings` of its `reviewer` comments, and in the `new_findings` of a
  `reviewer-dispositions` comment whose `repo` and `id` match one of them.
- The **latest outcome** of a finding at a time is its row in the dispositions
  comment of the highest round that has a row for it, among those created at or
  before that time.
- A merge is judged with the comments and records created at or before it.
- A finding is **closed** at a time when its latest outcome then is `fixed`,
  `rejected`, `deferred` or `accepted-no-change`, or a `final-fix` record
  created at or before that time names it. Otherwise it is **open**.
- A review is **clean** at a time when at least one `reviewer` comment exists by
  then and every finding recorded by then is closed. Its **clean time** is the
  later of the creation time of its last `reviewer` comment and the start of the
  latest unbroken clean span, both read up to the evaluation time or the merge,
  whichever is earlier. A review that is not clean then has no clean time.
- A commit is **covered** from a starting commit when it is that commit, or it
  is one step from a covered commit `C`: a `rebase` record with `exit=0` leads
  from `C` to it; or a `final-fix` record leads from `C` to it and the
  difference adds at most one line and deletes at most one line.
- A commit is **review-covered** when it is covered from the `head` of the latest
  `reviewer` or `reviewer-dispositions` comment of the pull request.
- A commit is **gate-covered** when it is covered from the `head` of a `gate`
  record with `exit=0` of the same pull request.
- A pull request is **ready to merge** when its review is clean, its head is
  review-covered and, when it requires a gate, gate-covered. It is ready from
  the latest of: its review's clean time; the creation time of the first
  reviewer or disposition comment from whose `head` its head is covered; when it
  requires a gate, the `finished` of the first passing `gate` record that covers
  its head; and the creation time of any later `rebase` record on that chain. A
  pull request whose base is not the default branch is not ready to merge.
- A pull request is **waived** for a rule when a `waiver` record for it names
  that rule in `covers`. A query that says it excludes waived pull requests
  leaves them out for that rule only, and lists each one it leaves out, with the
  waiver comment, in the evidence of its result. Whether the record's `ref`
  states a rule that differs is judged under the code lead's LEAD-R21.

### Transcript terms

A transcript query reads the evaluated session's tool calls (tool name, command
or file path, exit status, time) and incoming messages (sender, time).

- A command **matches** listed words when one of its shell segments starts with
  them, ignoring leading environment assignments and a `git -C <dir>` option.
- An **incoming message** is input from another agent or the user. Hook output
  and task notifications are not messages.
- The **dispatcher** is the sender of the session's first incoming message.
- A **send** is a call of `agent-msg send`, `herdr agent prompt`, `SendMessage`
  or `SubagentHandback`; its recipient is the call's addressee.
- A coder **report** is each send to the dispatcher after the session's first
  `gh pr create` call.

A transcript that cannot be read, or lacks a field a query needs, makes that
query `unavailable`.

### Evaluator settings

A team's evaluator settings are one JSON object in
`$TEAM_RETRO_HOME/<team>/eval.json` (default root
`~/.local/state/team-retro`). They are separate from the ix-board retro
configuration, `config.json` in the same directory, because ix-board rejects a
configuration with a key it does not know. The roles read `eval.json` for the
review age limit, and the evaluator (SWM-221) reads every key; no other ix-board
command reads the file. The queries name a key as `eval.<key>`.

| Key | Meaning | When absent |
|---|---|---|
| `review_age_limit_hours` | The review age limit the code lead and reviewer rules name | 1 |
| `gate_commands` | Per repository, the command words that run its aggregate gate; `team-gate gate` always counts | `make ci` |
| `ready_state` | The tracker state that marks a ticket ready | queries that read it are `unavailable` |

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-017-AC-1 | A fixture comment of each marker kind missing any one required field is reported as incomplete, naming the field; a complete comment of each kind is accepted. | Test |
| FR-017-AC-2 | Fixture reviews yield the expected findings, closed state and clean time for a review with no findings, one closed by a disposition, one reopened by a new finding and one closed by a final-fix record. | Test |
| FR-017-AC-3 | A head that differs from the starting commit by a passing rebase record, or by a recorded one-line fix is covered; a change under `reviews/` is a change like any other; a two-line fix, a failed rebase check, an unrecorded change and a broken chain are not. A disposition comment with an empty `dispositions` list makes its `head` the reviewed head, and a pull request is not ready to merge while its head is not review-covered. | Test |
| FR-017-AC-4 | A waiver record naming one rule removes its pull request from that rule's queries that exclude waived pull requests and from no other query, and each such result lists the pull request and the waiver comment as evidence. | Test |
| FR-017-AC-5 | Fixture transcripts yield the expected command matches, dispatcher, sends and coder reports, and an unreadable transcript yields `unavailable`. | Test |
| FR-017-AC-6 | Settings are read from `eval.json` with `config.json` unchanged; an absent file or unset `review_age_limit_hours` evaluates with a limit of one hour, and an unset `ready_state` makes the queries that read it `unavailable`. | Test |
| FR-017-AC-7 | The reviewer and code lead skills instruct each producer to post each marker with its required fields. | Inspection |

## Dependencies

- [FR-006](FR-006-role-spec-format.md), the role specs whose queries these
  records serve, and [FR-001](FR-001-evidence-contract.md), honest unknowns.
- ix-board `retro eval` (SWM-221), the reader of the records and of
  `eval.json`.
