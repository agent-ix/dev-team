---
id: FR-014
title: Dispatch a build of a pushed commit to a named host
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-003
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-012
    type: depends_on
  - target: ix://agent-ix/dev-team/FR-013
    type: depends_on
---
# FR-014: Dispatch a build of a pushed commit to a named host

## Description

`run --host <name> --repo <repo> --sha <sha> --class <class> -- <cargo args>` SHALL build the pushed commit on the named host under that host's scheduler, profile and repository/toolchain target-pool mode ([FR-012](FR-012-target-dir-pool.md)), and return the [FR-013](FR-013-structured-job-output.md) summary. This is the first routing step. Choosing a host automatically is a later flag and is not specified here.

## Behavior

Hosts are named in the caller's configuration with a transport command, for example `ssh titan` or, for a Windows host, `wsl.exe --`; the scheduler does not assume ssh. The caller resolves the sha to a full commit and checks that the remote repository contains it. An unpushed or unknown sha is refused with the commit and remote named; the tool never pushes.

**Repository store on the remote.** Each host's profile maps a repo name to one configured bare mirror directory (`[repos.<name>] mirror = path, remote = url`). The remote side fetches into that mirror under a per-repo lock, so concurrent fetches serialize, and each pool slot is a `git worktree` of the mirror at the commit, sharing its object store. A repo name with no configured mirror is refused. Mirror bytes count in the pool disk budget ([FR-012](FR-012-target-dir-pool.md)).

**Idempotent submission.** The caller generates a job key (a random 128-bit value, `--job-key`, created once per `run` and reused on any retry). The remote deduplicates on the key: a repeated submission returns the existing job id and, if finished, its summary, and never enqueues a second build. The key is retained as long as the job's index row. This covers a transport that drops after the remote enqueued but before the caller learned the job id.

The remote runs the job under its own queue with the same lane, ticket and priority class; priority and fair share apply on the remote queue. The job's life is independent of the transport: if the connection drops after submission the job keeps running remotely and `result --host <name> --job-key <key>` (or `<job id>`) retrieves the summary. An unreachable host, a transport authentication failure or an unknown host name is an explicit error with its own exit code; the tool does not fall back to another host or to a local run unless the caller passes `--fallback local`, in which case the summary states that the run was local. `--host auto` is accepted by the parser and refused with a not-available message. A command that is not a cargo invocation runs in the checkout only when the profile allowlists it.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-014-AC-1 | Against a fixture remote reached through a local transport command, the pushed sha is built in a repository/toolchain pool slot of a configured mirror and the summary names host, sha and slot; the caller's working tree is not read. | Test |
| FR-014-AC-2 | An unpushed sha is refused before any remote execution, naming sha and remote; the tool performs no push. A repo with no configured mirror is refused naming the repo. | Test |
| FR-014-AC-3 | Severing the transport after submission leaves the job running; `result --host` later returns its summary and the build ran exactly once. | Test |
| FR-014-AC-4 | Severing the transport after the remote enqueued but before the job id reaches the caller, then retrying `run` with the same job key, yields one remote request and one build; the retry returns that job's id or summary. | Test |
| FR-014-AC-5 | An unreachable host and an unknown host return distinct nonzero exit codes with the host named; no local run occurs; with `--fallback local` the run occurs locally and the summary flags it. | Test |
| FR-014-AC-6 | Two remote requests of classes `must-fix` and `periodic` on a one-slot host are admitted in configured FR-011 order on the remote queue; the request event and summary retain the named class for each. | Test |
| FR-014-AC-7 | `--host auto` is refused with a not-available message and creates no request. | Test |
| FR-014-AC-8 | Two concurrent submissions for one repo fetch into the mirror one after the other under the lock, and both slots check out their commits without corrupting the mirror. | Test |
| FR-014-AC-9 | A transport defined as `wsl.exe --` and one defined as `ssh <alias>` dispatch through one code path with no host-specific branch outside configuration. | Inspection |

## Dependencies

- [FR-011](FR-011-priority-classes-lane-fair-share.md), priority and fair share on the remote queue.
- [FR-012](FR-012-target-dir-pool.md), repository/toolchain pool slot checkout of the commit and disk budget.
- [FR-013](FR-013-structured-job-output.md), returned summary.
