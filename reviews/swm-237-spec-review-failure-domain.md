---
id: SR-026
title: "failure-domain review of SWM-237 build scheduler extension"
type: SpecReview
analysis: failure-domain
scope: "agent-ix/dev-team; SWM-237; spec/** diff origin/main...071569c (PR dev-team#31)"
review_set: subset
date: 2026-11-24
---

> Numbering note: finding text cites the pre-renumber ids of the reviewed head 071569c (US-002 is now US-003; FR-006..FR-013 are now FR-009..FR-016).

## Summary

Failure-mode pass over throttling, probes, target pool, remote dispatch and metrics. The orphan-pause bound the lead requires is not met, two pause paths can stall until `max_pause`, and submission idempotency and path identity are unspecified.

Ticket: SWM-237. PR: dev-team#31 at 071569c. Lead decisions on the author's open questions were treated as intent.

## Verdict

**FAIL**. FND-001 (orphaned paused group bounded only by the next client command) reproduces the heat-guard incident shape and must be fixed with the governor. Covered well: throttling acts only on lease-owned groups never by name (FR-007-AC-2), signal hysteresis (AC-1), SIGCONT before SIGTERM on timeout/cancel (AC-5), held slots never evicted and foreign dirs never deleted (FR-009), transport drop after submission (FR-011-AC-3), hung probe timeout (NFR-002), no fabricated metric values (FR-012-AC-4).

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | A paused group whose supervisor and watchdog die stays SIGSTOPped 'until the next client command or watchdog start', which is unbounded on an idle host: this is the 46-stopped-builds incident. Lead decision 3 requires that orphaned paused groups cannot persist beyond one sample interval while the governor runs. Rewrite AC-3 so that, with the governor running, the orphan is resumed (or re-owned) within one sample interval and `ix_build_paused_orphans` returns to zero within that bound; keep `recover` as the fallback when the governor is down. | spec/functional/FR-007-scheduler-owned-throttling.md:53 |
| FND-002 | medium | Unspecified: the probe that drives an active pause (for example Tctl) becomes unavailable or stale while leases are paused. FR-006 turns it into zero slots, but no rule says whether paused groups are resumed, held or aborted, so they sit stopped until `max_pause`. State the behavior (for example hold paused for at most N samples, then resume or abort with reason `probe_unavailable`) and add an AC. | spec/functional/FR-007-scheduler-owned-throttling.md:38-45 |
| FND-003 | medium | SIGSTOP does not release resident memory, so a memory-class pause stops growth but cannot by itself bring the reading down. If the reading stays above threshold, the rule pauses lease after lease until all are paused and the resume threshold is never reached; nothing ends the stall before `max_pause`. Specify the escalation (abort the paused largest-RSS lease after K samples without improvement) or justify relying on swap-out, with an AC. | spec/functional/FR-007-scheduler-owned-throttling.md:28-31 |
| FND-004 | medium | Idempotency covers only drops after submission. If the transport drops after the remote enqueued the request but before the caller received the job id, the caller cannot call `result` and a retry enqueues a second build. Require a caller-generated request id (FR-005 already has stable ids) that the remote deduplicates, and an AC that severs the transport mid-submission. | spec/functional/FR-011-remote-dispatch-pushed-sha.md:33-35 |
| FND-005 | medium | Serialization on a caller-named target directory is keyed on 'that path' with no identity rule. Relative paths, symlinks, and case variants on case-insensitive APFS name one directory with different strings and would run concurrently, the 30-minute shared-target block from US-002. Key on the canonicalized path (or device+inode) and add an AC using a symlinked alias. | spec/functional/FR-009-target-dir-pool.md:37-39 |
| FND-006 | medium | `ix_build_lane_running{lane}` labels by lane, which FR-008 defines as the request owner, such as a lead's session. Session ids are minted continuously, so the label set is unbounded over time, which NFR-002's bounded-label intent excludes (its list names ticket, request, command). Bound lanes to a configured set or drop the label from the Prometheus series and keep per-lane data in the JSON snapshot. | spec/functional/FR-012-build-metrics-export.md:41 |
| FND-007 | low | Abort targets may be paused leases (an abort threshold is above the pause threshold), but SIGCONT-before-SIGTERM is required only for timeout and cancellation (AC-5). Extend AC-4 so an aborted paused lease is continued before termination. | spec/functional/FR-007-scheduler-owned-throttling.md:54 |

## Examined Scope

```yaml
scope:
- id: FR-007
  path: spec/functional/FR-007-scheduler-owned-throttling.md
  role: examined
  excerpt: The scheduler SHALL pause, resume and abort the builds it admitted when a host limit is crossed, and
    SHALL own that duty itself. No separate guard process is required for builds to be resumed, and the death of
    any one process SHALL NOT leave a build stopped indefinitely.
- id: FR-007-B
  path: spec/functional/FR-007-scheduler-owned-throttling.md
  role: examined
  excerpt: Pausing and resuming duties are performed by whichever live per-request watchdog holds the state lock
    at the sample time; samples are taken at most once per sample interval per host. A watchdog resumes its group
    before it exits on every normal, signal and cancel path. A group whose pause owner has died is resumed by the
    next live watchdog, and by `recover`, which every client command runs before it acts.
- id: FR-007-M
  path: spec/functional/FR-007-scheduler-owned-throttling.md
  role: examined
  excerpt: A memory-class limit pauses one lease, the one with the largest resident memory, then the next if the
    reading stays beyond the threshold after one sample, and resumes in reverse order at the resume threshold.
- id: FR-006
  path: spec/functional/FR-006-host-profile-sustainable-slots.md
  role: examined
  excerpt: The scheduler SHALL compute each host's number of sustainable build slots from one TOML host profile
    and live probe readings, and use that number as enabled capacity in the FR-005 admission rules. No slot count
    is edited by hand or recorded in a comment. The profile replaces the static JSON host policy as the source of
    capacity limits.
- id: FR-009
  path: spec/functional/FR-009-target-dir-pool.md
  role: examined
  excerpt: When a caller names its own target directory, the scheduler serializes requests on that path so that
    two builds never run on one directory, even across different worktrees.
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
- id: FR-012
  path: spec/functional/FR-012-build-metrics-export.md
  role: examined
  excerpt: '`metrics` writes Prometheus exposition text to standard output or atomically to a file for a textfile
    collector; `serve --listen ADDR` serves it over HTTP, bound to loopback unless told otherwise.'
- id: NFR-002
  path: spec/non-functional/NFR-002-scheduler-overhead-and-isolation.md
  role: examined
  excerpt: The scheduler SHALL NOT let a slow or failing probe delay admission decisions, pause decisions or metric
    reads beyond a fixed timeout, and SHALL stay small enough that governing a host does not consume build capacity.
- id: FR-006-AC-1
  path: spec/functional/FR-006-host-profile-sustainable-slots.md
  role: examined
  excerpt: Given a fixture profile and scripted probe readings, the computed sustainable slot count equals the minimum
    of the five bounds above for at least one reading set where each bound is the binding one.
- id: FR-006-AC-2
  path: spec/functional/FR-006-host-profile-sustainable-slots.md
  role: examined
  excerpt: A required probe that returns unavailable, or a reading older than twice the sample interval, yields
    zero sustainable slots and a reason naming the probe; an optional probe in the same state does not change the
    count and is listed as unavailable in status.
- id: FR-006-AC-3
  path: spec/functional/FR-006-host-profile-sustainable-slots.md
  role: examined
  excerpt: A drop in headroom lowers the count at the next sample; a rise raises it only after `grow_after` on a
    controllable clock; running leases are not terminated and overcommit is reported.
- id: FR-006-AC-4
  path: spec/functional/FR-006-host-profile-sustainable-slots.md
  role: examined
  excerpt: Fixture profiles for a thermal host (Tctl, package power), a macOS host (compressor, swap) and a WSL
    host (WSL memory) each load, run only their declared probes and compute slots; a profile whose resume threshold
    is not below its pause threshold is refused naming the key.
- id: FR-006-AC-5
  path: spec/functional/FR-006-host-profile-sustainable-slots.md
  role: examined
  excerpt: After jobs with known peak RSS complete, the RAM-per-job value moves from the default to the 90th percentile
    of the history window and respects the profile minimum; status reports the value and its source.
- id: FR-006-AC-6
  path: spec/functional/FR-006-host-profile-sustainable-slots.md
  role: examined
  excerpt: The scheduler reads probes only through the shared host-probe crate; the repository contains no second
    probe implementation and no hand-edited slot count in a comment, profile comment or script.
- id: FR-006-AC-7
  path: spec/functional/FR-006-host-profile-sustainable-slots.md
  role: examined
  excerpt: Replacing a profile file atomically changes the ceiling and thresholds used at the next sample without
    restarting or signaling running builds.
- id: FR-007-AC-1
  path: spec/functional/FR-007-scheduler-owned-throttling.md
  role: examined
  excerpt: With scripted probe readings crossing pause and resume thresholds, all leases receive SIGSTOP once at
    the pause reading, are not signaled again while paused, and receive SIGCONT at the resume reading; readings
    between the thresholds cause no signal flapping.
- id: FR-007-AC-2
  path: spec/functional/FR-007-scheduler-owned-throttling.md
  role: examined
  excerpt: A memory-class breach pauses only the largest-RSS lease first; a process that is not a scheduler lease
    (same program name) in the same fixture receives no signal.
- id: FR-007-AC-3
  path: spec/functional/FR-007-scheduler-owned-throttling.md
  role: examined
  excerpt: Killing with SIGKILL the supervisor and then the watchdog of a paused lease leaves the group stopped
    only until the next client command or watchdog start; the test shows the group continued by `recover` and the
    metric `ix_build_paused_orphans` returns to zero. Killing only the supervisor leaves the surviving watchdog
    resuming at the resume reading.
- id: FR-007-AC-4
  path: spec/functional/FR-007-scheduler-owned-throttling.md
  role: examined
  excerpt: At the abort threshold, leases are terminated lowest class first and newest first, one per sample interval,
    each with verified exit and reason `aborted_thermal`; a lease already finishing is not signaled twice.
- id: FR-007-AC-5
  path: spec/functional/FR-007-scheduler-owned-throttling.md
  role: examined
  excerpt: Paused seconds do not count toward the hold deadline; a lease paused beyond `max_pause` is cancelled
    with reason `pause_exceeded`, and timeout and cancellation of a paused lease deliver SIGCONT before SIGTERM
    so the child can exit.
- id: FR-007-AC-6
  path: spec/functional/FR-007-scheduler-owned-throttling.md
  role: examined
  excerpt: Thermal pause blocks new admission until the resume threshold; queued requests keep their enqueue time
    and age and reservation behavior under FR-005 resumes afterward.
- id: FR-007-AC-7
  path: spec/functional/FR-007-scheduler-owned-throttling.md
  role: examined
  excerpt: A job exceeding its configured RSS cap is terminated with reason `rss_cap` and its group exit verified;
    a job below the cap is untouched.
- id: FR-009-AC-1
  path: spec/functional/FR-009-target-dir-pool.md
  role: examined
  excerpt: Two sequential jobs on the same key use the same slot directory and the second finds the first's artifacts;
    two concurrent jobs on one key never receive the same directory.
- id: FR-009-AC-2
  path: spec/functional/FR-009-target-dir-pool.md
  role: examined
  excerpt: With the budget fitting two slots and three keys in use, creating a third slot evicts the least recently
    used free slot, never a held one; if all slots are held the request waits with reason `target_disk` and keeps
    its enqueue age.
- id: FR-009-AC-3
  path: spec/functional/FR-009-target-dir-pool.md
  role: examined
  excerpt: Two concurrent requests that name one explicit target directory from different worktrees run one after
    the other; the waiting one shows reason `target_slot`.
- id: FR-009-AC-4
  path: spec/functional/FR-009-target-dir-pool.md
  role: examined
  excerpt: A directory in the pool root not created by the scheduler appears in `pool status` as foreign and survives
    `pool prune`.
- id: FR-009-AC-5
  path: spec/functional/FR-009-target-dir-pool.md
  role: examined
  excerpt: '`pool prune` removes free slots over age or over budget, reports reclaimed bytes, and a scheduler restart
    after a crash releases slots whose lease exit is verified and keeps slots whose group is still alive.'
- id: FR-009-AC-6
  path: spec/functional/FR-009-target-dir-pool.md
  role: examined
  excerpt: With a shared compiler cache configured the job environment points at it, its size counts toward the
    budget, and hit statistics appear in the job summary; with none configured the environment is untouched.
- id: FR-011-AC-1
  path: spec/functional/FR-011-remote-dispatch-pushed-sha.md
  role: examined
  excerpt: Against a fixture remote reached through a local transport command, the pushed sha is built in a pool
    slot and the returned summary names the host, sha and slot; the working tree of the caller is not read.
- id: FR-011-AC-2
  path: spec/functional/FR-011-remote-dispatch-pushed-sha.md
  role: examined
  excerpt: An unpushed sha is refused before any remote execution, naming sha and remote; the tool performs no push.
- id: FR-011-AC-3
  path: spec/functional/FR-011-remote-dispatch-pushed-sha.md
  role: examined
  excerpt: Severing the transport after submission leaves the job running; `result --host` later returns its summary
    and the build ran exactly once.
- id: FR-011-AC-4
  path: spec/functional/FR-011-remote-dispatch-pushed-sha.md
  role: examined
  excerpt: An unreachable host and an unknown host return distinct nonzero exit codes with host named; no local
    run occurs; with `--fallback local` the run occurs locally and the summary flags it.
- id: FR-011-AC-5
  path: spec/functional/FR-011-remote-dispatch-pushed-sha.md
  role: examined
  excerpt: Two remote requests of classes `gate` and `check` on a one-slot host are admitted in FR-008 order on
    the remote queue.
- id: FR-011-AC-6
  path: spec/functional/FR-011-remote-dispatch-pushed-sha.md
  role: examined
  excerpt: '`--host auto` is refused with a not-available message and creates no request.'
- id: FR-011-AC-7
  path: spec/functional/FR-011-remote-dispatch-pushed-sha.md
  role: examined
  excerpt: A transport defined as `wsl.exe --` and one defined as `ssh <alias>` both dispatch through the same code
    path with no host-specific branch outside the profile.
- id: FR-012-AC-1
  path: spec/functional/FR-012-build-metrics-export.md
  role: examined
  excerpt: After a scripted sequence of queued, running, paused and finished requests, every series in the table
    appears with the expected value and labels, and `promtool check metrics` accepts the output.
- id: FR-012-AC-2
  path: spec/functional/FR-012-build-metrics-export.md
  role: examined
  excerpt: '`ix_build_slots_busy` and `ix_build_slots_sustainable` match the snapshot''s occupied units and computed
    slot count at the same sample; `ix_build_pause_seconds_total{reason}` equals the recorded pause durations.'
- id: FR-012-AC-3
  path: spec/functional/FR-012-build-metrics-export.md
  role: examined
  excerpt: Counters do not decrease across a scheduler restart or after `prune`.
- id: FR-012-AC-4
  path: spec/functional/FR-012-build-metrics-export.md
  role: examined
  excerpt: A required probe that is unavailable yields `ix_build_probe_unavailable` of 1 and no fabricated value;
    the exposition contains no ticket id, request id, command argument or environment value.
- id: FR-012-AC-5
  path: spec/functional/FR-012-build-metrics-export.md
  role: examined
  excerpt: A fixture with 10 000 retained requests produces the exposition in under 200 ms and the `serve` endpoint
    answers a scrape while a request is being admitted.
- id: FR-012-AC-6
  path: spec/functional/FR-012-build-metrics-export.md
  role: examined
  excerpt: The ix-board fleet view reads slots busy, sustainable slots, queue wait by priority and pause seconds
    from the JSON snapshot through the FR-001 evidence contract with host and observation time; a Prometheus scrape
    of a live host shows the same series in the Grafana dashboard.
```

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | Verified at 10413b3. |
| FND-002 | fixed | Verified at 10413b3. |
| FND-003 | fixed | Verified at 10413b3. |
| FND-004 | fixed | Verified at 10413b3. |
| FND-005 | fixed | Verified at 10413b3. |
| FND-006 | fixed | Verified at 10413b3. |
| FND-007 | fixed | Verified at 10413b3. |
