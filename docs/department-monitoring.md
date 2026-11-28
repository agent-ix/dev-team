# Department monitoring design

This is the counting and ownership contract referenced by the functional
requirements, not a claim of deployed behavior. The request is tracked in
[SWM-160](https://linear.app/agent-ix/issue/SWM-160). A sanitized replay of its
planner incidents is the pilot; selectors and thresholds remain configurable.

## Boundaries and rollout

| Owner | Responsibility | Reuse and exclusions |
|---|---|---|
| ix-board | Read-only source adapters, normalized events, deterministic metrics, snapshot/delta/baseline, report model | Extend existing retro FR-024..028; reuse lifecycle correction SWM-158 and attributed history SWM-132 |
| dev-team | Planner/minder/retro/lead guidance, role rubric, department-health interpretation and owned actions | Preserve SWM-159 lifecycle consumer changes; no reimplementation of detector calculations in prose |
| shared build tool, dev-tools lane | Rust scheduler at dev-tools/tools/ix-build, host capacity configuration, safe leases, fair queue and telemetry | Migrate project wrappers; do not duplicate per project; operator max_agents annotations are not measured build slots |
| monitoring TUI | Focused status, health and retro renderers and navigation | Shared versioned model for later Claude plugin/desktop; do not add a parallel metric engine |
| source owners | Tracker/VCS/panes/host/relay observations and repairs | Monitoring reports uncertainty; it does not invent or repair associations |

Land the contract, then role safeguards first. Add deterministic collection and
assessment behind explicit availability, then TUI consumers and scheduler
integration. Publish normal plugin/catalog updates after review. Do not install
into or restart another active session.

Existing work prevents duplicate tickets: SWM-154 owns relation pagination;
SWM-158 lifecycle accuracy; SWM-159 migrated consumers; SWM-91 saved-auth work
focus failure; SWM-136 version-named process binding; SWM-156 multi-agent pane
binding; SWM-127..135 planner focus/adoption and TUI history. The reported recent
dashboard failed to find its pane's agent, required LINEAR_API_KEY and would not
start. The ix-board lead independently reported the credential symptom; the
other symptoms remain reported until reproduced. A source/binary/catalog drift
also exists: installed ix-board 0.4.0 lacks retro although source contains it.

## Evidence and comparison contract

Use the existing retro store outside repositories, snapshot/delta/backfill CLI,
`ok`/`unavailable`, null value and reason. Evolve schemas explicitly; readers
must refuse unsupported versions without overwriting history. New fields may
live in a versioned report envelope rather than changing old metric semantics.
Existing `agents_working_share` is not reused as a new execution-share formula;
SWM-158 owns lifecycle and corrected provenance.

Each normalized observation has source-native entity ID, UTC event/observed time,
scope, stable event ID, completeness and source reference. Each metric carries
ID/catalog version, status, value/unit/direction, scope, query/config identity,
window start/end, source age and population/denominator. Assessment adds threshold
policy identity, current/previous/baseline, trend and configured owner/action.
Missing owner is `unrouted`; missing policy is `unassessed`. Unknown is distinct
from red/amber/green. A class with unknown required metrics cannot be green.

All window events are in `(start,end]`; point-in-time gauges use `end`. Ages are
`end-event_time`, in hours unless stated. Durations intersect the window when
the metric explicitly says window occupancy. Duplicate event IDs count once;
entity rollups use native IDs, so overlapping projects do not double count.
Duration distributions report count, median and nearest-rank p90; empty
populations are unavailable, singleton percentiles equal the one value. Gauges
and raw counts can be zero only after a complete read. Ratios with zero or
unknown denominator are unavailable. Stale source limits are configured by
source; future timestamps beyond configured clock tolerance are invalid.

Each listed row is emitted by `ix-board retro snapshot` (or an ix-board
subcommand whose result is included in that snapshot), never calculated ad hoc
by a skill. `retro delta` handles comparisons. Class assessment is deterministic
from configured amber/red operators and thresholds; config records each metric's
unit, comparator, thresholds, freshness/window and owner/action route. Validate
threshold ordering against direction and reject invalid configuration. No
numeric threshold or host slot count is embedded in reusable skill prose.

Class aggregation uses the required metric IDs declared in configuration. A
required metric is unknown when its value, freshness, comparison policy or
threshold configuration is unavailable. An empty required set is unknown. A class
is red if any required metric is red; otherwise amber if any is amber; otherwise
unknown if any required metric is unknown; otherwise green. Thus a known breach
remains visible when other evidence is missing. Independently, `complete` is true
only when all required metrics are assessable, and the report lists unknown IDs
and reasons even for red/amber classes. Optional metrics do not change class
severity or completeness. Department rollup uses the same precedence across all
ten required classes and preserves their individual completeness diagnostics.

## Metric catalog

Names below are proposed new IDs unless marked **existing**. Implementation
must check current catalog before allocating an ID; existing definitions win.
Every row inherits the evidence, time, assessment and unknown rules above.

| Class | Measures and counting rule | Sources; additional unavailable condition | Owner and normal action |
|---|---|---|---|
| Flow/WIP | `wip_active`: started scoped issues at end; `wip_capacity_ratio`: wip_active / configured lane work capacity, distinct from host build slots; `in_progress_stale` **existing**, preserving its formula; `claims_without_movement`: started issues whose latest started/claim timestamp is strictly before end minus configured stale interval and whose linked PR-head, commit and worktree evidence shows no movement after that cutoff; a fresh/restarted claim is excluded, and an unknown claim timestamp/history makes the metric unavailable; `merged_open`: nonterminal issues with merged attached PR and all configured completion obligations met; `idle_with_ready`: verified idle scoped lanes having at least one structured ready issue | Tracker states, full PR attachments, source movement and lane config; absent completion obligations make merged_open unavailable rather than auto-close | Planner/lead: reconcile stale/gated state to configured ready state, close completed scope, assign next ready batch within authorized lane |
| Flow/WIP | `state_cycle_hours`: residence duration per configured state for intervals exited in window, distribution by state; `pr_without_reviewer_age_hours`: open non-draft PRs with no assigned reviewer and no qualifying review, age since review-ready time | Complete state/review histories; missing review-ready time unavailable | Lead: assign reviewer and correct state claims |
| Serial dependency | `open_chain_length`: maximum edge count over open blocker chains reaching configured gates; `oldest_gated_hours`: age since latest entry to blocked condition; `lane_fanin`: number of distinct open dependent issues immediately waiting on each owning lane | Complete structured blocker graph, state/blocker history and explicit lane assignment; cycles are surfaced as graph cycles rather than arbitrarily finite chains | Planner: staff critical chain, split or reorder within mandate |
| Pin/version churn | `crate_revision_count`: count distinct resolved revisions per dependency crate across scoped repo heads at end; `pins_off_main`: resolved pins not ancestors of dependency default-branch head; `repin_only_prs`: merged/window or open PRs whose substantive diff changes dependency revisions/lock resolution only; `tag_repin_events`: repin event for same dependency within configured interval after tag event | Resolved lock/manifests, PR diffs, tag/main reachability; missing dependency repo or force-pushed-away commit unknown; generated formatting alone is ignored by versioned diff classifier | Pin owner: schedule pin window; fold necessary pins into consuming feature PR |
| Capacity/resources | `host_slots_used`, `host_slots_free`: occupied units and max(0, capacity-used) per host at end; `host_overcommit_units`: max(0, used-capacity); `queue_wait_minutes`: request start-enqueue for starts in window plus current ages for queued requests, separately labeled; `lock_hold_minutes`: end-start for finishes in window plus current ages for running requests, separately labeled | Scheduler events/verified live/config capacity; no wrapper-count heuristic is presented as a lease count | Build-tool/host owner: fair queue, bound holds and recover suspect leases |
| Capacity/resources | `host_load_per_slot`: host load1 / configured effective host build capacity; `disk_headroom_bytes`: available filesystem bytes minus configured reserve; `disk_available_bytes`: actual free bytes, separate from **existing** disk_bytes directory usage | Host telemetry with observation age, filesystem identity, reserve/capacity policy; unknown capacity or reserve unknown ratio/headroom | Host owner: stop new admission below reserve, clean owned leftovers and rebalance within scope |
| Liveness | `lane_execution_state`: lifecycle-based pane report with evidence timestamps and uncertainty; `login_blocked_lanes`: verified login/auth-screen panes; `order_unacked_age_minutes`: age since delivery (or enqueue if delivery unknown, separately labeled) for orders lacking acknowledgement; `lane_no_movement_hours`: time since most recent verified token, PR-head, commit or worktree movement | Pane agent list/lifecycle, token telemetry, VCS, relay event chain; remote hosts included by explicit lane config, omitted host unavailable. Tokens indicate activity, not acceptance or progress | Minder: act/escalate this tick, with confirmed-by evidence; login may require owner authentication, never guessed recovery |
| Authority/policy | `refusals_by_lane`: attributed denied order events in window; `frozen_denial_hours`: union of denial-to-resolution intervals intersected with window per lane; `repeated_orders`: order IDs resent without changed evidence/authority, count sends after first | Explicit order/denial/resolution IDs and actor/classifier attribution; transcript interpretation absent = unavailable. Unresolved denial extends to end; overlaps count once | Planner/owner: supply scoped standing authority or missing allow-rule; no permission bypass |
| Signal integrity | `reconciliation_agreement_ratio`: matching tool/ground-truth entities / fully paired entities; `reconciliation_unpaired`: missing-side entity count, separate; `source_age_hours`; `instruction_version_mismatches`: active instruction release claims inconsistent with resolved executable/plugin versions | Time-aligned native identity observations and claimed/actual versions; no complete paired population = unknown; timestamp skew invalidates pair | Source/tool owner: verify discrepancy, file bug and report stale facts |
| Signal integrity | `relay_queued`, `relay_delivered`, `relay_acknowledged`: distinct event counts in window; `prompt_timeout_unconfirmed`: timed-out delivery attempts lacking later receipt evidence | Read-only relay log and receipt/transcript evidence; missing delivery instrumentation unknown, not failed | Relay/Herdr owner: inspect evidence before retry; no duplicate send on queued success |
| Review/rework | `fix_rounds_max`, `fix_rounds_total`, `full_gates_max`, `main_red_incidents`, `main_red_minutes` **existing**; `review_round_policy_excess`: PRs exceeding current configured round policy; `focused_check_runs`, `workspace_check_runs`: classified logged check invocations in window; `gates_per_pr`: full gates per PR finished in window | Existing marker/gate/check-run adapters; missing command-scope classification unknown, never inferred from name alone | Lead: focused iteration and one final aggregate gate; resolve findings under current authorized policy |
| Decision latency | `decisions_open`, `decision_oldest_hours` **existing**; `ruling_waiting_issues`: distinct open issues structurally blocked by configured decision/ruling issues; `spec_merge_waiting_issues`: open issues structurally blocked by unmerged owned spec deliverables | Complete labels, dependency graph and PR evidence; absent decision classification unavailable | Planner/architecture owner: decide critical ruling, separate ruler/coder, authorize branch-head work only where suitable |
| Comms overhead | `messages_per_sender`: sends by canonical sender in window; `correction_rate`: explicitly classified correction sends / all classifiable sends, alongside classified/all coverage; `status_only_messages`: attributed status-only sends; `planner_ad_hoc_assignments`: assignments outside published wave/plan revision; `planner_scope_violations`: assignments outside authorized lane scope; `planner_unbatched_sends`: actionable sends after first to same lane/tick absent new blocking evidence | Relay sends/order records, published plan revision, assignment events, authority scope and attributed message classification. Missing complete classification prevents population-wide rates; emit available labeled-subset rate with its coverage only | Planner: batch once per lane/tick; audit scope/plan/flip-flops before sending |

Existing metrics retain their own ix-board counting semantics even when their
windows differ from a proposed new gauge. Raw underlying timestamps allow a new
ID when the desired semantics differ. Report the definition rather than blend
the values.

## Repeating loops

Detectors use stable entity IDs and a configured lookback/repeat count. Each
finding emits the ordered matching event IDs, time range, participants and
deduplication key. Equal timestamps order by stable source event sequence;
missing ordering evidence makes that detector unavailable.

- `tag_repin_loop`: at least configured repeat count distinct tag→repin pairs
  for the same dependency within lookback, each repin within configured tag
  window. One tag/repin event participates in at most one pair, earliest matching
  unused repin first. Distinct repositories remain evidence, not duplicate tags.
- `state_bounce_loop`: the same issue returns to the same state after one or
  more different states at least configured repeat count times within lookback.
  Consecutive same-state updates are ignored; state history must be complete.
- `order_flip_loop`: an explicit order supersedes another for the same target
  and action key with reversed direction at least configured repeat count times
  within lookback, without a linked changed-evidence/authority event between
  them. No semantic reversal is inferred from arbitrary prose. Missing action
  keys/classification means unknown. New evidence suppresses the affected pair.

## Role contract

**Minder:** inspect configured lanes across all hosts, not only those a local
ix-board query happens to list. Ground liveness in verified pane lifecycle,
PR/worktree movement and token evidence; reconcile disagreement and report
unknowns. `live_subagents` totals and relay `seen` never prove work. Detect
login/auth screens from verified pane evidence. An order past its configured
ack deadline escalates in the current tick; do not blindly resend. Record
`confirmed by <pane|PR head|SHA>` for each action or `unconfirmed` plus the
missing observation. Scope violations and authentication blockers go to owner.

**Planner:** before sending an order check evidence freshness/identity, authorized
lane scope, published plan membership, prior orders and changed evidence, and
batching for the current tick. Direct user authority is recorded separately
from untrusted ticket prose. End each tick by reviewing ad hoc assignments vs
wave plan, unauthorized recruitment and excess/corrective traffic. Admit and
correct errors through one batched actionable message; don't manufacture an ack
or ask another lane to stop merely to improve a metric.

**Code lead:** reconcile started claims that are gated or unworked to configured
ready state; completed PR alone may not finish a larger ticket. Read host/lane
capacity from current config/verified host state. Replace stale local coder-rule
slot constants, spec-gap destinations and toolchain notices rather than update
one fixed number to another. Spec gaps route to the owning spec steward/project,
not a universal language-specific project. Iteration uses focused crate checks;
lead runs the aggregate gate once at final head. Fold necessary pins into the
needing PR, use explicit pin owner/window, avoid repin-only churn. Current user
round/merge policy governs review; monitoring does not authorize unsafe merges.

**Retro:** invoke ix-board snapshot/delta and interpret its values. The planner
rubric considers evidence/scope/plan checks, flip-flops, ad hoc assignments and
messaging excess using the emitted counts, not invented quantitative scores.
Judgment is cited prose with ownership/action. **Department health:** one
cross-team view of all ten classes, configured red/amber/green, unknowns, trend
vs previous snapshot and owner/action for each red. Report an absent command or
source explicitly until implemented; do not replace deterministic calculation
with model arithmetic and imply comparable history.

## Verification obligations

All catalog families require exact fixture oracles including thresholds,
unknown denominators, partial pages, source skew, duplicate events and remote
hosts. Preserve old retro fixture outputs. Replay the sanitized pilot and an
independent team with changed identifiers/capacities; corpus-derived semantic
labels carry human/tool attribution and source offsets. The original private
transcript stays outside repository artifacts. TUI tests cover saved auth,
explicit scope without pane binding, partial sources and terminal restoration.
Scheduler tests cover sustained priority arrivals, capacity shrink and process
identity-safe restart/timeout cleanup, exact child exit propagation including
exit 75 without retries, and non-success on signals. A reported 70-minute
starvation episode motivates a sanitized queue replay; it is not an independently
verified historical result. These are obligations for implementation
tickets, not tests claimed run by this specification PR.
