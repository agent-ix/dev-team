# Lead records

The code lead posts these comments on the PR's ticket as the facts happen. The
role evaluations read them
([FR-017](https://github.com/agent-ix/dev-team/blob/main/spec/functional/FR-017-role-evaluation-records.md)),
and they are the gate result the ticket's state record keeps. The marker is the
first line of the comment. Values contain no spaces, `pr=` is `<repo>#<n>`, and
every commit is the full hash. Never post one for something you did not read.

```bash
linear issue comment add "$TICKET" --body-file <record>.md
```

## Gate

After every aggregate gate run, passed or failed:

```
<!-- lead-record repo=<owner>/<repo> pr=<repo>#<n> kind=gate head=<commit gated> exit=<gate exit status> started=<started_at> finished=<finished_at> -->
```

`started` and `finished` are copied from the run's
[gate log](gate-log.md) line; `exit` is the status `team-gate` returned. Read
`head` with `git rev-parse HEAD` in the worktree before starting the run, with
nothing uncommitted.

## Rebase

After the confined check of an overlap rebase:

```
<!-- lead-record repo=<owner>/<repo> pr=<repo>#<n> kind=rebase from=<head before> head=<head after> exit=<confined check exit status> -->
```

## Final fix

After reading the coder's one-line final fix:

```
<!-- lead-record repo=<owner>/<repo> pr=<repo>#<n> kind=final-fix from=<head before> head=<head after> fnd=<SR-NNN/FND-NNN,...> -->
```

The difference outside `reviews/` adds at most one line and deletes at most one.
A larger change goes back to the coder and the reviewer.

## Waiver

When a repo, org or direct user rule differs from a role rule for this PR, and
only then. `ref` points at the text that states the differing rule:

```
<!-- lead-record repo=<owner>/<repo> pr=<repo>#<n> kind=waiver covers=<rule id> ref=<file or message that states the rule> -->
```

One comment names one rule id, for example `covers=LEAD-R11` for a repo that has
no aggregate gate, or `covers=CODE-R10` for a repo that has the coder run it.

Committed review files need no record: a commit that changes only files under
`reviews/` is covered by the head before it.
