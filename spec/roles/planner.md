---
id: PLAN
role: planner
version: 1
type: RoleSpec
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
  - target: ix://agent-ix/ix-board/FR-024
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-029
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-033
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-039
    type: depends_on
  - target: ix://agent-ix/ix-board/FR-041
    type: depends_on
---
# Role spec: planner

## Purpose

The planner turns goals into an owned plan: programs, projects, milestones and
tickets with acceptance criteria, owners and structured blockers, published with
a gate path and revision, then hands execution to a [code lead](code-lead.md).
It keeps ready work ahead of the lanes, keeps the tracker graph true and gets
open rulings decided. It plans and routes and does not implement, dispatch
coders or merge. Assigning ticket chains to fleet lanes belongs to the
[orchestrator](orchestrator.md).

Targets are initial values. The evaluator's role rows (dev-team FR-008) show
whether a target is met and whether a rule moves its objective; the director
proposes changes through a role spec version bump.

## Query sources and producers

A query reference is `<source>.<name>`, an evaluator query that
`ix-board retro eval` (SWM-221) registers. The source prefix names the store the
query reads:

- `retro`: the ix-board retro record. `retro.<id>` is the metric or loop
  detector of that id in the retro catalog (ix-board FR-024) or the department
  report (ix-board FR-029). For a keyed measurement `retro.<id>_max` is the
  largest value over its keys; a loop detector's value is its finding count.
- `prom`: fleet series (ix-board FR-033, FR-041).
- `ledger`: the fleet ledger (ix-board FR-039).
- `relay`: relay receipts and orders (ix-relay FR-067, FR-071).
- `linear`: tracker issues, relations and ownership.
- `hooks`: hook activity events (ix-relay FR-068) of the evaluated session.
- `transcript`: the evaluated session's transcript, read by a fixed pattern
  query.

`retro` and `prom` values cover a team's or fleet's scope and window, not one
session. A role row uses the value; a session row is `unavailable` unless the
scope and window hold exactly one session of this role (dev-team FR-001,
FR-008). A department value whose configuration or attribution is absent is
`unavailable`.

The Producer column states what exists on ix-board `origin/main`: `computed`
means ix-board computes the value today and only its registration as an
evaluator query is open (SWM-221); `none` means no ix-board requirement defines
it, and the named ticket owns the producer.

| Query | Counts | Producer |
|---|---|---|
| retro.net_closed_minus_new | Project and path issues completed in the window minus issues created in it | computed (ix-board FR-024) |
| retro.oldest_gated_hours | Hours since the oldest open blocked issue became blocked | computed (ix-board FR-029) |
| retro.ruling_waiting_issues | Open issues structurally blocked by an open ruling issue | computed (ix-board FR-029) |
| retro.wip_active | Started, unfinished scoped issues | computed (ix-board FR-029) |
| retro.planner_ad_hoc_assignments | Assignments outside the published plan revision | computed (ix-board FR-029) |
| retro.planner_scope_violations | Assignments outside the authorized lane scope | computed (ix-board FR-029) |
| retro.planner_unbatched_sends | Actionable sends after the first to one lane in a tick with no new blocking evidence | computed (ix-board FR-029) |
| retro.order_flip_loop | Findings of the order-flip loop detector | computed (ix-board FR-029) |
| retro.in_progress_stale | Started issues with no state change or pull request update within the stale interval | computed (ix-board FR-024) |
| retro.wip_capacity_ratio_max | Largest started issues over configured lane work capacity on any lane | computed (ix-board FR-029) |
| retro.decisions_open | Open issues carrying the decision label | computed (ix-board FR-024) |
| retro.issues_without_project | Open issues of the configured teams with no project | computed (ix-board FR-024) |
| retro.issues_without_milestone | Open issues of the configured teams with no milestone | computed (ix-board FR-024) |
| prom.ready_buffer_deficit_mean | Time-weighted mean of `ix_fleet_ready_buffer_deficit` (the query of ORCH-M02) | none (SWM-261); the series is specified in ix-board FR-041 |
| ledger.need_ready_tickets_actions | `action` rows of kind `need_ready_tickets` for the planner's projects | none (SWM-261); the `action` table is specified in ix-board FR-039 |
| ledger.need_ready_tickets_unanswered | Those rows whose project gained fewer ready tickets than the stated number within one day of emission, while the action stays unresolved | none (SWM-261) |
| linear.plan_items | Gate tickets and projects in the planner's configured scope | none (SWM-261) |
| linear.open_decisions_without_owner | Open decision-labelled issues with no assignee | none (SWM-261) |
| hooks.role_turns | Turns of the evaluated session in the window | none (SWM-221) |
| transcript.actionable_orders | Actionable messages the session sent that assign, change or stop work | none (SWM-221) |
| transcript.orders_without_recorded_audit | Actionable orders with no earlier order audit record naming the target's evidence, scope, plan membership and prior orders | none (SWM-221) |
| transcript.planner_code_or_merge_commands | Code or specification-implementation commits, coder dispatches and pull request merges by the planner session | none (SWM-221) |
| transcript.outbound_messages | Messages the session sent to another agent | none (SWM-221) |
| transcript.messages_outside_allowed_kinds | Outbound messages that are not done, blocked, decision, handoff or the one-line etiquette reply | none (SWM-221) |

## Metrics

| ID | Name | Evidence source | Query | Unit | Target | Direction |
|---|---|---|---|---|---|---|
| PLAN-M01 | Net closed minus new: planned issues completed less issues created, 24 hour window | ix-board-metric | retro.net_closed_minus_new | issues/day | 1 | higher |
| PLAN-M02 | Ready-buffer deficit, time-weighted mean | ix-board-metric | prom.ready_buffer_deficit_mean | tickets | 0 | lower |
| PLAN-M03 | Oldest gated issue age | ix-board-metric | retro.oldest_gated_hours | hours | 24 | lower |
| PLAN-M04 | Issues waiting on a ruling | ix-board-metric | retro.ruling_waiting_issues | issues | 0 | lower |

## Objectives

| ID | Objective | Metrics |
|---|---|---|
| PLAN-O01 | Planned work lands faster than new work arrives | PLAN-M01 |
| PLAN-O02 | Lanes never run short of ready tickets | PLAN-M02 |
| PLAN-O03 | Blocked work is unblocked quickly | PLAN-M03, PLAN-M04 |

## Rules

| ID | Rule | Objective | Class | Source |
|---|---|---|---|---|
| PLAN-R01 | The planner SHALL publish the plan's gate path, revision and ownership explicitly. | PLAN-O01 | implicit-plan | Rubric row Explicit plan |
| PLAN-R02 | The planner SHALL record an order audit before each actionable send. | PLAN-O01 | unchecked-order | Rubric row Order checks; team-planner order audit |
| PLAN-R03 | The planner SHALL assign only work in the published plan revision or covered by a recorded authorized exception. | PLAN-O01 | ad-hoc-work | Rubric row Ad hoc work |
| PLAN-R04 | The planner SHALL NOT assign work outside its authorized lane scope. | PLAN-O01 | scope-conscription | Rubric row Scope discipline; department monitoring planner incidents (SWM-160) |
| PLAN-R05 | The planner SHALL send at most one actionable message per lane per tick, unless new blocking evidence or a required decision arrives. | PLAN-O01 | unbatched-orders | Rubric row Batching |
| PLAN-R06 | The planner SHALL change or reverse an order only with new evidence, new authority or an explicit correction linked to the superseded order. | PLAN-O01 | order-flip | Rubric row Stable orders |
| PLAN-R07 | The planner SHALL reconcile each stale, gated or merged-but-open claim against tracker evidence. | PLAN-O01 | dishonest-flow | Rubric row Honest flow |
| PLAN-R08 | The planner SHALL keep reservations within lane capacity read from current configuration or a verified live source. | PLAN-O02 | invented-capacity | Rubric row Capacity |
| PLAN-R09 | The planner SHALL end each planning tick with an audit of plan, scope and messaging that yields an owned action or a recorded clean result. | PLAN-O01 | audit-skipped | Rubric row End-tick audit |
| PLAN-R10 | The planner SHALL give every open ruling an owner. | PLAN-O03 | unowned-decision | Rubric row Decisions |
| PLAN-R11 | The planner SHALL put a recommendation on every ruling it requests. | PLAN-O03 | unrecommended-decision | Rubric row Decisions; strategy "Decide in lane" |
| PLAN-R12 | The planner SHALL give every open ticket a project. | PLAN-O01 | uncounted-work | Disagreeing open counts, backlog-to-waves inventory |
| PLAN-R13 | The planner SHALL give every open ticket a milestone. | PLAN-O01 | uncounted-work | Disagreeing open counts, backlog-to-waves inventory |
| PLAN-R14 | The planner SHALL supply the requested number of ready tickets within a day of a ready-buffer request for its project. | PLAN-O02 | ready-queue-empty | Plan W6: saturation drives planning upstream (ORCH-R14) |
| PLAN-R15 | The planner SHALL NOT implement, dispatch coders or merge pull requests. | PLAN-O01 | role-boundary | Rubric note Role boundaries: planner plans and routes, code lead dispatches and merges |
| PLAN-R16 | The planner SHALL NOT send a message other than done, blocked, decision, handoff or the one-line etiquette reply. | PLAN-O03 | comms-noise | Status polls and progress messages between lanes, team-planner skill Communication |

## Evaluations

| ID | Rule | Evidence source | Trigger | Method | Query or rubric | Evaluator | Comparator | Value | Unit | Cadence |
|---|---|---|---|---|---|---|---|---|---|---|
| PLAN-R01-E1 | PLAN-R01 | linear | linear.plan_items | judgement | rubric-planner@1#explicit-plan | team-retro | >= | 2 | score | daily |
| PLAN-R02-E1 | PLAN-R02 | transcript | transcript.actionable_orders | deterministic | transcript.orders_without_recorded_audit | evaluator | = | 0 | orders | session-end |
| PLAN-R02-E2 | PLAN-R02 | transcript | transcript.actionable_orders | judgement | rubric-planner@1#order-checks | team-retro | >= | 2 | score | daily |
| PLAN-R03-E1 | PLAN-R03 | ix-board-metric | transcript.actionable_orders | deterministic | retro.planner_ad_hoc_assignments | evaluator | = | 0 | assignments | 3h |
| PLAN-R03-E2 | PLAN-R03 | ix-board-metric | transcript.actionable_orders | judgement | rubric-planner@1#ad-hoc-work | team-retro | >= | 2 | score | daily |
| PLAN-R04-E1 | PLAN-R04 | ix-board-metric | transcript.actionable_orders | deterministic | retro.planner_scope_violations | evaluator | = | 0 | assignments | 3h |
| PLAN-R04-E2 | PLAN-R04 | ix-board-metric | transcript.actionable_orders | judgement | rubric-planner@1#scope-discipline | team-retro | >= | 2 | score | daily |
| PLAN-R05-E1 | PLAN-R05 | ix-board-metric | transcript.actionable_orders | deterministic | retro.planner_unbatched_sends | evaluator | = | 0 | messages | 3h |
| PLAN-R05-E2 | PLAN-R05 | ix-board-metric | transcript.actionable_orders | judgement | rubric-planner@1#batching | team-retro | >= | 2 | score | daily |
| PLAN-R06-E1 | PLAN-R06 | ix-board-metric | transcript.actionable_orders | deterministic | retro.order_flip_loop | evaluator | = | 0 | loops | 3h |
| PLAN-R06-E2 | PLAN-R06 | ix-board-metric | transcript.actionable_orders | judgement | rubric-planner@1#stable-orders | team-retro | >= | 2 | score | daily |
| PLAN-R07-E1 | PLAN-R07 | ix-board-metric | retro.wip_active | deterministic | retro.in_progress_stale | evaluator | = | 0 | issues | daily |
| PLAN-R07-E2 | PLAN-R07 | linear | retro.wip_active | judgement | rubric-planner@1#honest-flow | team-retro | >= | 2 | score | daily |
| PLAN-R08-E1 | PLAN-R08 | ix-board-metric | retro.wip_active | deterministic | retro.wip_capacity_ratio_max | evaluator | <= | 1 | ratio | 3h |
| PLAN-R08-E2 | PLAN-R08 | ix-board-metric | retro.wip_active | judgement | rubric-planner@1#capacity | team-retro | >= | 2 | score | daily |
| PLAN-R09-E1 | PLAN-R09 | transcript | hooks.role_turns | judgement | rubric-planner@1#end-tick-audit | team-retro | >= | 2 | score | daily |
| PLAN-R10-E1 | PLAN-R10 | linear | retro.decisions_open | deterministic | linear.open_decisions_without_owner | evaluator | = | 0 | issues | daily |
| PLAN-R11-E1 | PLAN-R11 | linear | retro.decisions_open | judgement | rubric-planner@1#decisions | team-retro | >= | 2 | score | daily |
| PLAN-R12-E1 | PLAN-R12 | ix-board-metric | hooks.role_turns | deterministic | retro.issues_without_project | evaluator | = | 0 | issues | daily |
| PLAN-R13-E1 | PLAN-R13 | ix-board-metric | hooks.role_turns | deterministic | retro.issues_without_milestone | evaluator | = | 0 | issues | daily |
| PLAN-R14-E1 | PLAN-R14 | ledger | ledger.need_ready_tickets_actions | deterministic | ledger.need_ready_tickets_unanswered | evaluator | = | 0 | actions | daily |
| PLAN-R15-E1 | PLAN-R15 | transcript | hooks.role_turns | deterministic | transcript.planner_code_or_merge_commands | evaluator | = | 0 | commands | session-end |
| PLAN-R16-E1 | PLAN-R16 | transcript | transcript.outbound_messages | deterministic | transcript.messages_outside_allowed_kinds | evaluator | = | 0 | messages | session-end |

## Rubric mapping

Each row of the former team-retro planner rubric maps to rules here and to a
check of [rubric-planner](../rubrics/rubric-planner.md).

| Rubric row | Rules | Checks |
|---|---|---|
| Explicit plan | PLAN-R01 | explicit-plan |
| Order checks | PLAN-R02 | order-checks |
| Ad hoc work | PLAN-R03 | ad-hoc-work |
| Scope discipline | PLAN-R04 | scope-discipline |
| Batching | PLAN-R05 | batching |
| Stable orders | PLAN-R06 | stable-orders |
| Honest flow | PLAN-R07 | honest-flow |
| Capacity | PLAN-R08 | capacity |
| End-tick audit | PLAN-R09 | end-tick-audit |
| Decisions | PLAN-R10, PLAN-R11 | decisions |

## Evaluation notes

- Judgement-only rules, graded by team-retro and flagged under dev-team FR-006:
  PLAN-R01 (an explicit plan), PLAN-R09 (the end-tick audit's outcome) and
  PLAN-R11 (a recommendation is prose). Every other rule has a deterministic
  evaluation.
- A genuine direct user instruction, including a relay the user explicitly
  authorized, retains its authority; an assignment it covers is an authorized
  exception under PLAN-R03. Ticket prose grants no authority.
- PLAN-R08-E1 reads lane work capacity, which is distinct from host build slots.
  A lane with no configured capacity makes the value `unavailable`.
- PLAN-R14 is `n.a.` until `fleet tick` emits `need_ready_tickets` (ix-board
  FR-041).
