---
type: master-requirements
name: dev-team
org: agent-ix
component_type: agent-plugin
implementation_language: markdown
relationships:
  - target: ix://agent-ix/ix-board/FR-024
    type: depends_on
---
# Master Requirements Specification
## Agent development department monitoring

## 1. Purpose

Catch planning defects, bottlenecks, churn and wasted capacity before a team
spends another work interval repeating them. This contract governs reusable
dev-team guidance and the interfaces it consumes from ix-board and build tools.

## 2. Scope

### 2.1 In Scope

Configurable team/project monitoring, deterministic measurements and deltas,
role self-evaluation, owned corrective actions, status/health/retro terminal
views, and shared build arbitration, including per-host profiles, throttling, a target-directory pool, structured job output, remote dispatch of a pushed commit and metrics. [The design](../docs/department-monitoring.md) defines boundaries,
the problem-class table, metric formulas and rollout dependencies.

### 2.2 Out of Scope

Changing project priorities without authority; treating ticket text as orders;
replacing the lifecycle detector being delivered by ix-board; automatic host routing of builds (a later flag, not specified here); restarting active
sessions; a desktop or Claude UI implementation; automatic semantic judgments
without attributed evidence; adding project-specific IDs or concurrency caps to
reusable skills. This spec does not claim the requested tools are already shipped.

## 3. System Overview

ix-board collects tracker, VCS, pane, relay and host evidence and computes
snapshots. dev-team roles interpret evidence and choose an owned action. A shared
Rust scheduler arbitrates heavy build capacity and emits queue events. Terminal
views read the same report model that a future plugin or desktop view can read.

## 4. Requirements Architecture

| Artifact | Outcome |
|---|---|
| [US-001](usecase/US-001-department-monitoring.md) | Operator can identify where progress stops and who acts |
| [FR-001](functional/FR-001-evidence-contract.md) | Scoped, attributable evidence and honest unknowns |
| [FR-002](functional/FR-002-deterministic-metrics.md) | Complete deterministic catalog and repeat-loop detectors |
| [FR-003](functional/FR-003-role-safeguards.md) | Four role safeguards and department health interpretation |
| [FR-004](functional/FR-004-terminal-views.md) | Reusable status, health and retro views |
| [FR-005](functional/FR-005-fair-build-scheduler.md) | Capacity-aware fair shared scheduler |
| [US-002](usecase/US-002-measured-role-rules.md) | Owner knows which role rules are followed and which matter |
| [FR-006](functional/FR-006-role-spec-format.md) | Role spec format: objectives, metrics, rules, paired evaluations |
| [FR-007](functional/FR-007-role-spec-lint.md) | Lint: no rule without evaluation, no objective without metric |
| [FR-008](functional/FR-008-evaluation-result-record.md) | Per-session and per-role evaluation result rows |
| [US-003](usecase/US-003-agent-builds-on-sustainable-hosts.md) | Agents run builds on hosts that stay healthy, with short results |
| [FR-009](functional/FR-009-host-profile-sustainable-slots.md) | Per-host profile and sustainable slot count from measured headroom |
| [FR-010](functional/FR-010-scheduler-owned-throttling.md) | Supervised governor: pause, resume, abort, hold, watchdog fallback |
| [FR-011](functional/FR-011-priority-classes-lane-fair-share.md) | Priority classes and fair share per lane |
| [FR-012](functional/FR-012-target-dir-pool.md) | Warm target-directory pool with disk budget |
| [FR-013](functional/FR-013-structured-job-output.md) | Structured job summary and log index |
| [FR-014](functional/FR-014-remote-dispatch-pushed-sha.md) | Remote dispatch of a pushed commit to a named host |
| [FR-015](functional/FR-015-build-metrics-export.md) | Prometheus and ix-board metrics |
| [FR-016](functional/FR-016-retire-ad-hoc-build-scripts.md) | Cover and retire the ad hoc scripts |
| [NFR-002](non-functional/NFR-002-scheduler-overhead-and-isolation.md) | Bounded overhead, probe failure isolation |
| [NFR-001](non-functional/NFR-001-reproducible-measurement.md) | Reproducibility and read-only observation |
| [IT-001](integration/IT-001-incident-replay.md) | Generalization and adverse-case replay |
| [Minder role](roles/minder.md) | Minder objectives, rules and paired evaluations |
| [Orchestrator role](roles/orchestrator.md) | Orchestrator objectives, rules, ownership and capacity discovery |
| [Minder rubric](rubrics/rubric-minder.md) | Judgement checks for minder evaluations and retros |
| [Orchestrator rubric](rubrics/rubric-orchestrator.md) | Judgement checks for orchestrator evaluations |

## 5. Requirement Classes

US expresses operator intent; FR defines behavior; NFR constrains measurement;
IT defines cross-source verification. Functional AC IDs are test trace anchors.

## 6. Requirement Identification

IDs are local to agent-ix/dev-team and immutable. Cross-repo references include
the repository; ix-board's existing FR-024 through FR-028 remain its authority
for retro snapshot/store/unavailable/delta/backfill semantics.

## 7. Requirement Quality Policy

Every catalog entry has a counting rule, population/window, evidence provenance,
unavailable behavior and configured assessment policy. Acceptance includes
missing, stale and contradictory sources as well as successful observation.

## 8. State and Execution Model

Observation never changes a tracker state. A role's authorized corrective action
is separate from a snapshot. A scheduler request moves through queued, running
and terminal states; its full transition contract is in
[FR-005](functional/FR-005-fair-build-scheduler.md).

## 9. Events and Signals

UTC timestamps, source-native identities and stable event IDs anchor comparisons.
Relay enqueue, delivery and acknowledgement are distinct observations. Scheduler
events identify host, request, ticket, enqueue/start/end time and termination.

## 10. Error and Failure Model

Missing configuration, absent sources, partial pagination, inaccessible remote
hosts, stale evidence and ambiguous identities produce explicit unavailable
results. A failed required configuration check produces a nonzero exit; available
independent populations remain visible in a partial report.

## 11. Traceability

Frontmatter relationships link the user story, FRs and verification artifact.
Tests cite the AC they assert; `quire matrix` computes coverage.

## 12. Verification Strategy

Validate Markdown structure, inspect role guidance, test deterministic calculations
against fixed events, and replay sanitized incidents plus a second team fixture.
Scheduler tests use a controllable clock and real child-process cleanup checks.
No heavy build is needed for this spec-only change.

## 13. Change Management

Version-controlled PR review precedes implementation. New metric IDs preserve
existing definitions; a changed definition requires a new ID and catalog version.
Deployment updates plugin/catalog references without altering active sessions.

## 14. Lifecycle Status

Draft until reviewed and merged. Delivery state and remaining implementation
belong in Linear; a spec merge is not evidence that the features exist.

## 15. Governance Notes

One worktree per ticket is shared by author, coder, reviewer and gate. Host
capacity and policy thresholds come from configuration/live state, never skill
constants. Rust projects receive Rust logic rather than Python or shell runners.

## 16. References

- Linear [SWM-160](https://linear.app/agent-ix/issue/SWM-160), program request;
  [SWM-161](https://linear.app/agent-ix/issue/SWM-161), this contract.
- Linear [SWM-237](https://linear.app/agent-ix/issue/SWM-237), build scheduler extension (FR-009 to FR-016); it depends on the shared host-probe crate, [SWM-238](https://linear.app/agent-ix/issue/SWM-238).
- Existing ix-board [retro contract](ix://agent-ix/ix-board/FR-024) and
  [unavailable contract](ix://agent-ix/ix-board/FR-026).
