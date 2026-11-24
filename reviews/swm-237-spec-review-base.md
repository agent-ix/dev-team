---
id: SR-025
title: "base review of SWM-237 build scheduler extension"
type: SpecReview
analysis: base
scope: "agent-ix/dev-team; SWM-237; spec/** diff origin/main...071569c (PR dev-team#31)"
review_set: subset
date: 2026-11-24
---

> Numbering note: finding text cites the pre-renumber ids of the reviewed head 071569c (US-002 is now US-003; FR-006..FR-013 are now FR-009..FR-016).

## Summary

Base checklist over the SWM-237 spec diff (US-002, FR-006..FR-013, NFR-002, the FR-005-AC-1 edit and spec.md index), checked against the lead's eight decisions. `quire validate` passes on this branch alone, but the new IDs collide with open PR dev-team#30 and FR-007 contradicts lead decision 3 (supervised governor).

Ticket: SWM-237. PR: dev-team#31 at 071569c. Lead decisions on the author's open questions were treated as intent.

## Verdict

**FAIL**. Two high findings must be fixed before merge: the US-002/FR-006/FR-007/FR-008 ID collision with dev-team#30, and FR-007's watchdog-only throttling model that contradicts the required supervised `serve` governor. Consistent with the lead decisions: spec lives in dev-team (1); no rename, the new FRs keep FR-005's `locked-build` package (2); abort order lowest class, newest first, one per interval with thresholds held in the profile (4); fair share ceil(slots/active lanes) with reservation exempt (5); `--fallback local` explicit opt-in (6); one agent-day retirement gate (7, but see FND-005). Requirement statements are atomic, use SHALL, and every AC names a verification method.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | ID collision with open PR dev-team#30 (SWM-220): it also adds US-002, FR-006, FR-007 and FR-008 (spec/usecase/US-002-measured-role-rules.md, FR-006-role-spec-format, FR-007-role-spec-lint, FR-008-evaluation-result-record) and edits the same spec/spec.md index rows. Whichever merges second gets duplicate ids and a spec.md conflict; renumber this PR (or #30) onto ids neither uses, e.g. US-003 and FR-009 onward after #30's FR-008, and update every cross-reference and relationship. | spec/spec.md:54-57 |
| FND-002 | high | FR-007 contradicts lead decision 3 (a supervised governor owns throttling). FR-007 says no separate guard process is required and assigns pause/resume to whichever per-request watchdog holds the state lock, with `recover` on the next client command as the backstop. The decision requires a supervised `serve` governor (launchd on macOS, systemd user unit on Linux/WSL) that owns throttling and the Prometheus pull endpoint, with per-request watchdogs only as the fallback that resumes groups. Add the governor and its service-unit supervision as normative behavior with ACs, and make FR-012 `serve` that same governor rather than an optional metrics server. | spec/functional/FR-007-scheduler-owned-throttling.md:15-18,38-45 |
| FND-003 | medium | The FR-005-AC-1 edit narrows enqueue-order to one lane, but the FR-005 Behavior text still says ties are broken by lower enqueue sequence host-wide and the Description promises stable FIFO order. Under FR-008 an equal-priority request from an over-share lane yields to a later one from another lane, which the unchanged Behavior text forbids. Amend FR-005 Behavior to defer cross-lane ordering to FR-008. | spec/functional/FR-005-fair-build-scheduler.md:28-29 |
| FND-004 | medium | Lead decision 8 (TOML replaces the JSON policy, no compat layer) is only half stated: 'replaces the static JSON host policy as the source of capacity limits' leaves open whether a JSON policy is still read, merged or migrated, and the JSON policy is never defined in this spec. Add a statement and AC that the JSON policy is not read (a leftover file is refused or ignored with a diagnostic) and no conversion shim exists. | spec/functional/FR-006-host-profile-sustainable-slots.md:19-20 |
| FND-005 | medium | The retirement gate (decision 7) hinges on 'no admission dispute', which is undefined: nothing says what counts as a dispute, who records one, or where. FR-013-AC-5 only checks that the guide states the condition, so the gate cannot be evaluated. Define a dispute as a recorded event (for example an operator `hold`, a manual override, or a filed ticket against admission) and add an AC that the guide's condition is checkable from those records. | spec/functional/FR-013-retire-ad-hoc-build-scripts.md:36-39,49 |
| FND-006 | medium | 'A request-level value for the same key is refused or overrides only where the profile allows' admits two implementations. State the rule: refused unless the profile marks the key overridable, in which case the request value wins. | spec/functional/FR-013-retire-ad-hoc-build-scripts.md:47 |
| FND-007 | medium | The summary content and FR-010-AC-1's oracle are defined by 'the failure lines the retired remote runner printed' and its patterns, a script FR-013 deletes. After retirement the requirement has no stated content. Write the extraction patterns into the FR (or a committed fixture) so the oracle survives the script's deletion. | spec/functional/FR-010-structured-job-output.md:26-28 |
| FND-008 | low | Operator `hold`/`resume` is new scheduler behavior introduced only inside FR-013's parity table and AC-2; its pause reason `operator` is missing from FR-007's reason set (`thermal`, `memory`, `swap`, `compressor`, `host_load`) that FR-012's `reason` label draws on. Move the behavior into FR-007 (or its own FR) and add `operator` to the reason list. | spec/functional/FR-013-retire-ad-hoc-build-scripts.md:30 |
| FND-009 | low | FR-012-AC-6 demonstrates through the ix-board fleet view and a Grafana dashboard, but neither is listed under Dependencies, and ix-board's fleet view is an unshipped cross-repo deliverable. Name the ix-board requirement and dashboard source as dependencies. | spec/functional/FR-012-build-metrics-export.md:59-65 |

## Examined Scope

```yaml
scope:
- id: US-002
  path: spec/usecase/US-002-agent-builds-on-sustainable-hosts.md
  role: examined
  excerpt: As a code lead or coder agent working across several build hosts I want to submit a build or test at
    a pushed commit, name a host and a priority, and receive a short result So that hosts neither overheat or run
    out of memory nor sit idle, my merge gates are not stuck behind routine checks, and I do not spend context reading
    raw logs.
- id: FR-005
  path: spec/functional/FR-005-fair-build-scheduler.md
  role: examined
  excerpt: The effective priority is `base_priority + floor(wait/aging_interval)`, with lower enqueue sequence breaking
    ties.
- id: FR-005-AC-1
  path: spec/functional/FR-005-fair-build-scheduler.md
  role: examined
  excerpt: Equal-priority eligible requests of one lane (see FR-008 for cross-lane share) run in enqueue order;
    repeated high-priority arrivals cannot pass an eligible request after its configured reservation threshold.
    A deterministic-clock test proves this under sustained arrivals.
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
- id: FR-009
  path: spec/functional/FR-009-target-dir-pool.md
  role: examined
  excerpt: When a caller names its own target directory, the scheduler serializes requests on that path so that
    two builds never run on one directory, even across different worktrees.
- id: FR-010
  path: spec/functional/FR-010-structured-job-output.md
  role: examined
  excerpt: It lists only the failure lines the retired remote runner printed, at most twelve lines, plus the log
    path and job id, and is at most 4 KiB; longer content is truncated with a `truncated` flag.
- id: FR-011
  path: spec/functional/FR-011-remote-dispatch-pushed-sha.md
  role: examined
  excerpt: The job's life is independent of the transport. If the connection drops after submission the job keeps
    running remotely and its supervisor survives; `result --host <name> <job>` retrieves the summary and the caller
    does not rerun the build.
- id: FR-012
  path: spec/functional/FR-012-build-metrics-export.md
  role: examined
  excerpt: '`metrics` writes Prometheus exposition text to standard output or atomically to a file for a textfile
    collector; `serve --listen ADDR` serves it over HTTP, bound to loopback unless told otherwise.'
- id: FR-013
  path: spec/functional/FR-013-retire-ad-hoc-build-scripts.md
  role: examined
  excerpt: 'Retirement follows the FR-005 migration rule: existing builds finish under their original wrappers,
    and a script is deleted only after the tool has run on that host for at least one full agent working day with
    no admission dispute.'
- id: NFR-002
  path: spec/non-functional/NFR-002-scheduler-overhead-and-isolation.md
  role: examined
  excerpt: The scheduler SHALL NOT let a slow or failing probe delay admission decisions, pause decisions or metric
    reads beyond a fixed timeout, and SHALL stay small enough that governing a host does not consume build capacity.
- id: spec.md
  path: spec/spec.md
  role: examined
  excerpt: '| [US-002](usecase/US-002-agent-builds-on-sustainable-hosts.md) | Agents run builds on hosts that stay
    healthy, with short results |

    | [FR-006](functional/FR-006-host-profile-sustainable-slots.md) | Per-host profile and sustainable slot count
    from measured headroom |

    | [FR-007](functional/FR-007-scheduler-owned-throttling.md) | Scheduler-owned pause, resume and abort |

    | [FR-008](functional/FR-008-priority-classes-lane-fair-share.md) | Priority classes and fair share per lane
    |'
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
- id: FR-008-AC-1
  path: spec/functional/FR-008-priority-classes-lane-fair-share.md
  role: examined
  excerpt: With one slot busy and `check`, `test` and `gate` requests queued in that order, the gate is admitted
    first, then the test, then the check, before any aging threshold; an unknown class and a missing lane are refused
    with a request error.
- id: FR-008-AC-2
  path: spec/functional/FR-008-priority-classes-lane-fair-share.md
  role: examined
  excerpt: Under sustained `gate` arrivals on a deterministic clock, a queued `check` request reaches reservation
    after `(2+1) * aging` and starts before any later arrival, matching FR-005-AC-1.
- id: FR-008-AC-3
  path: spec/functional/FR-008-priority-classes-lane-fair-share.md
  role: examined
  excerpt: With two slots, lane A holding both and lane B waiting at equal priority, B's request is admitted first
    when a slot frees even though A's request was enqueued earlier; with B absent, A's waiting requests use free
    slots in enqueue order.
- id: FR-008-AC-4
  path: spec/functional/FR-008-priority-classes-lane-fair-share.md
  role: examined
  excerpt: A request at its reservation threshold is admitted ahead of an under-share lane's equal-priority request,
    and the fair-share rule never signals a running lease.
- id: FR-008-AC-5
  path: spec/functional/FR-008-priority-classes-lane-fair-share.md
  role: examined
  excerpt: Replaying the reported 70-minute starvation shape (a wrapper waiting behind continuously arriving peers)
    on the deterministic clock gives that wrapper a lease within the reservation bound.
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
- id: FR-010-AC-1
  path: spec/functional/FR-010-structured-job-output.md
  role: examined
  excerpt: A fixture cargo test run with two failures, one panic and a compile error produces a summary whose failing
    test names, first panic and first error equal the lines extracted by the retired remote runner's patterns from
    the same log.
- id: FR-010-AC-2
  path: spec/functional/FR-010-structured-job-output.md
  role: examined
  excerpt: A run with 100 000 log lines yields a summary of at most 4 KiB with `truncated` set when needed and no
    raw log text beyond the failure lines.
- id: FR-010-AC-3
  path: spec/functional/FR-010-structured-job-output.md
  role: examined
  excerpt: '`log <job> --test NAME` returns only that test''s section within the line limit; an unknown job id returns
    a request error naming the id.'
- id: FR-010-AC-4
  path: spec/functional/FR-010-structured-job-output.md
  role: examined
  excerpt: After log pruning, `result <job>` still returns the stored summary and the index row; `log <job>` reports
    `pruned`.
- id: FR-010-AC-5
  path: spec/functional/FR-010-structured-job-output.md
  role: examined
  excerpt: 'A non-cargo command or unparsable output yields exit code, outcome and `parse: unavailable`; a child
    killed by signal reports the signal.'
- id: FR-010-AC-6
  path: spec/functional/FR-010-structured-job-output.md
  role: examined
  excerpt: A fixture whose environment holds a secret value produces no occurrence of that value in the summary,
    index or event output.
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
- id: FR-013-AC-1
  path: spec/functional/FR-013-retire-ad-hoc-build-scripts.md
  role: examined
  excerpt: A parity table in the tool reference maps each retired function above to a command or profile key, and
    every mapped command exists in `--help`.
- id: FR-013-AC-2
  path: spec/functional/FR-013-retire-ad-hoc-build-scripts.md
  role: examined
  excerpt: '`hold` blocks admission with reason `operator` and a stored note until `resume`; running leases continue;
    held seconds are reported as pause seconds.'
- id: FR-013-AC-3
  path: spec/functional/FR-013-retire-ad-hoc-build-scripts.md
  role: examined
  excerpt: A job starts with the profile's `cpu_set`, nice level and `[env]` values and `CARGO_BUILD_JOBS` equal
    to `jobs_per_slot`; a request-level value for the same key is refused or overrides only where the profile allows.
- id: FR-013-AC-4
  path: spec/functional/FR-013-retire-ad-hoc-build-scripts.md
  role: examined
  excerpt: The tool tree contains no `.py` file and no shell script with a conditional or loop; Makefile recipes
    invoke only `cargo` and the built binary.
- id: FR-013-AC-5
  path: spec/functional/FR-013-retire-ad-hoc-build-scripts.md
  role: examined
  excerpt: The reference and migration guide state the cutover order and the retirement condition per script.
```
