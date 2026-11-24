---
id: SR-027
title: "risk-complexity review of SWM-237 build scheduler extension"
type: SpecReview
analysis: risk-complexity
scope: "agent-ix/dev-team; SWM-237; spec/** diff origin/main...071569c (PR dev-team#31)"
review_set: subset
date: 2026-11-24
---

> Numbering note: finding text cites the pre-renumber ids of the reviewed head 071569c (US-002 is now US-003; FR-006..FR-013 are now FR-009..FR-016).

## Summary

Technical-risk pass. The design hard-depends on SWM-238 (host-probe crate) and on cross-platform per-group memory accounting the spec does not define; fair share and multi-unit requests use different units.

Ticket: SWM-237. PR: dev-team#31 at 071569c. Lead decisions on the author's open questions were treated as intent.

## Verdict

**CONDITIONAL**. No blocker on its own; resolve the measurement-source and unit findings before tasking. Low-risk parts: profile TOML loading and validation, structured summary and log index, metrics exposition, explicit `--host auto` refusal.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | RAM-per-job history (p90 of peak RSS) and the `rss_cap` abort both need the peak resident memory of a whole process group, but no source is named. Linux can use cgroup v2 memory.peak; macOS has no group accounting, and sampling-summed RSS misses short peaks and double-counts shared pages. Name the measurement per platform (or require it from the SWM-238 crate) and state the sampling error tolerance the ACs accept. | spec/functional/FR-006-host-profile-sustainable-slots.md:64 |
| FND-002 | medium | Lane share is computed in slots ('sustainable slot count divided by the number of lanes'), while FR-005 requests carry resource units and may take more than one. A lane holding one two-unit lease is under share by count but over by units. State the share in resource units and add a multi-unit AC. | spec/functional/FR-008-priority-classes-lane-fair-share.md:30-36 |
| FND-003 | low | 'The remote side fetches the repository and checks the commit out into the pool slot' leaves the repository store undefined: a per-slot clone multiplies disk and fetch cost, while a shared object store needs locking between concurrent fetches. Specify which, and count it in the FR-009 disk budget. | spec/functional/FR-011-remote-dispatch-pushed-sha.md:28-31 |

## Examined Scope

```yaml
scope:
- id: FR-006
  path: spec/functional/FR-006-host-profile-sustainable-slots.md
  role: examined
  excerpt: The scheduler SHALL compute each host's number of sustainable build slots from one TOML host profile
    and live probe readings, and use that number as enabled capacity in the FR-005 admission rules. No slot count
    is edited by hand or recorded in a comment. The profile replaces the static JSON host policy as the source of
    capacity limits.
- id: FR-007
  path: spec/functional/FR-007-scheduler-owned-throttling.md
  role: examined
  excerpt: The scheduler SHALL pause, resume and abort the builds it admitted when a host limit is crossed, and
    SHALL own that duty itself. No separate guard process is required for builds to be resumed, and the death of
    any one process SHALL NOT leave a build stopped indefinitely.
- id: FR-008
  path: spec/functional/FR-008-priority-classes-lane-fair-share.md
  role: examined
  excerpt: 'Fair share per lane: at one effective priority, when more than one lane has eligible waiting requests,
    a request from a lane that already holds more than its share (the sustainable slot count divided by the number
    of lanes with running or eligible work, rounded up) yields to an equal-priority request from a lane under its
    share.'
- id: FR-011
  path: spec/functional/FR-011-remote-dispatch-pushed-sha.md
  role: examined
  excerpt: The job's life is independent of the transport. If the connection drops after submission the job keeps
    running remotely and its supervisor survives; `result --host <name> <job>` retrieves the summary and the caller
    does not rerun the build.
- id: FR-011-B
  path: spec/functional/FR-011-remote-dispatch-pushed-sha.md
  role: examined
  excerpt: The remote side fetches the repository and checks the commit out into the pool slot, then runs under
    its own queue with the same lane, ticket and priority class.
- id: FR-006-AC-5
  path: spec/functional/FR-006-host-profile-sustainable-slots.md
  role: examined
  excerpt: After jobs with known peak RSS complete, the RAM-per-job value moves from the default to the 90th percentile
    of the history window and respects the profile minimum; status reports the value and its source.
- id: FR-007-AC-7
  path: spec/functional/FR-007-scheduler-owned-throttling.md
  role: examined
  excerpt: A job exceeding its configured RSS cap is terminated with reason `rss_cap` and its group exit verified;
    a job below the cap is untouched.
- id: FR-008-AC-3
  path: spec/functional/FR-008-priority-classes-lane-fair-share.md
  role: examined
  excerpt: With two slots, lane A holding both and lane B waiting at equal priority, B's request is admitted first
    when a slot frees even though A's request was enqueued earlier; with B absent, A's waiting requests use free
    slots in enqueue order.
- id: FR-011-AC-1
  path: spec/functional/FR-011-remote-dispatch-pushed-sha.md
  role: examined
  excerpt: Against a fixture remote reached through a local transport command, the pushed sha is built in a pool
    slot and the returned summary names the host, sha and slot; the working tree of the caller is not read.
- id: FR-011-AC-5
  path: spec/functional/FR-011-remote-dispatch-pushed-sha.md
  role: examined
  excerpt: Two remote requests of classes `gate` and `check` on a one-slot host are admitted in FR-008 order on
    the remote queue.
```

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | Verified at 10413b3. |
| FND-002 | fixed | Verified at 10413b3. |
| FND-003 | fixed | Verified at 10413b3. |
