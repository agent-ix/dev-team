# Department evidence

Use this contract for department health and every requested retro metric.
The [monitoring design](../../../docs/department-monitoring.md) owns counting
definitions; this reference tells role skills how to consume them.

## Collect and interpret

Resolve the requested teams/projects to an explicit retro configuration. Keep
host/lane coverage, ownership, thresholds and baseline in that configuration,
outside git. Do not infer capacity from cores, worker counts or planning
annotations. Missing optional inputs leave their metrics unavailable.

Inspect the resolved executable/version and `ix-board retro --help`. Use only
the subcommands and options that the installed CLI advertises:

```bash
ix-board retro snapshot --config <file> --json
ix-board retro delta --config <file> --json
```

Retain command exit status, stdout and stderr before parsing. An absent command
or failed read is a capability/source failure, not a healthy department. Report
the exact command, version and error once. Do not substitute a cached binary,
hand-count source events, or fabricate a newer flag or output field.

Read supported metrics independently. New metric IDs, class assessments,
planner audits and loop results may be absent during rollout. Mark each absent
result unavailable; existing valid measurements remain usable. Never fill a
missing value with zero or calculate an absent rate, severity or detector.

For every reported result preserve its scope, window, query/catalog identity,
unit, population/denominator, source age, threshold policy, completeness and
evidence. Read previous/baseline changes and regression from `retro delta`.
`query_changed`, unavailable comparisons and unsupported schema/provenance stay
visible; do not compare unlike definitions or relabel old history.

## Problem classes

The collector owns these measurements and their deterministic assessments:

- Flow/WIP: active work vs configured lane capacity, stale claims vs movement,
  merged/open issues, idle lanes with ready work, state residence and PR age
  without a reviewer. A fresh claim is not stale merely for having no commit.
- Serial dependency: longest open blocker chain, oldest gated work and lane
  fan-in. Preserve graph-cycle and missing-history diagnostics.
- Pin/version churn: distinct dependency revisions, off-main pins, repin-only
  PRs and tag-to-repin windows.
- Capacity/resources: used/free capacity, overcommit, queue wait and lock hold,
  host load relative to capacity and disk reserve/headroom.
- Liveness: verified pane lifecycle, login/auth screens, token and PR/worktree
  movement, and overdue unacknowledged orders across configured remote hosts.
- Authority/policy: attributed refusals, frozen intervals and repeated orders.
  Missing semantic labels are unclassified, not an exact refusal count.
- Signal integrity: paired tool/ground-truth agreement, unpaired observations,
  source age, instruction/version mismatch and distinct relay outcomes.
- Review/rework: fix rounds vs current policy, repeated gates, focused/workspace
  checks and red-main incidents.
- Decision latency: open rulings, oldest ruling and dependent work waiting on
  rulings or spec merges.
- Comms overhead: sends by sender/window, attributed correction/status traffic,
  plan adherence, scope violations and unbatched orders with coverage.

Read tag/repin, state-bounce and order-flip loops only from emitted detectors,
including ordered event evidence and deduplication keys. Semantic correction,
refusal and reversal labels need actor/tool attribution. A labeled-subset rate
retains its coverage and cannot become a population-wide claim.

## Severity and action

Use configured red/amber/green assessments and their independent completeness
diagnostics. Unknown is a separate result. Missing thresholds are unassessed;
missing owners are unrouted. Show unknown required metric IDs even when another
metric produces a known red/amber breach. Do not derive class or department
severity in prose when the tool has not emitted it. No invented combined score.

For each red, name one configured owner and one concrete next action. Batch
actions by owner and deduplicate unchanged findings. Recommend within the
authorized scope; another team owns its staffing, authentication and resources.
If a route is missing, report unrouted and ask the planning owner to assign it.
Do not conscript a tab or change a running build to improve a score.
