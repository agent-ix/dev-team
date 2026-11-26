---
id: rubric-planner
version: 3
type: Rubric
relationships:
  - target: ix://agent-ix/dev-team/FR-006
    type: satisfies
---
# Rubric: planner

The planner rubric grades the judgement evaluations of the
[planner role spec](../roles/planner.md). `/team-retro` grades it. A judgement
evaluation cites one check as `rubric-planner@3#<check-slug>`.

Each check scores 0, 1 or 2 for cited judgment against its anchors, or `n/a`
when the evidence was not read. `n/a` is listed under Data quality and is never
counted as 0 or 2. Scores are not averaged. A judgement score never overrides a
deterministic verdict on the same rule.

Quantitative evidence comes from ix-board snapshots, deltas and emitted audit
assessments; missing measurements or provenance are `n/a` under Data quality.
Never count transcript calls or messages by hand. Keep each team's scope and
policy separate. Use a cited qualitative concern when a deterministic audit is
unavailable, without inventing its count, rate, severity or a clean score.

## Checks

| ID | Check | Scale |
|----|-------|-------|
| rubric-planner@3#explicit-plan | The gate path, plan revision and ownership are explicit. Evidence: structured plan and blocker chain. | 2: all explicit; 1: one ambiguity resolved; 0: repeated ambiguity left unresolved |
| rubric-planner@3#order-checks | Evidence, scope, plan and prior-order checks were recorded before orders. Evidence: order audit with cited source ids. | 2: checks recorded; 1: a missed check corrected; 0: orders sent despite unresolved checks |
| rubric-planner@3#ad-hoc-work | Assignments stay in the published plan. Evidence: `planner_ad_hoc_assignments`, published revision. | 2: the emitted assessment meets policy; 1: a breach with a corrective owner; 0: a breach unowned or ignored |
| rubric-planner@3#scope-discipline | Assignments stay in the authorized lane scope. Evidence: `planner_scope_violations`, authorized lane scope. | 2: the emitted assessment meets policy; 1: an exception corrected within scope; 0: unauthorized conscription persists |
| rubric-planner@3#batching | Orders are batched per lane and tick. Evidence: `planner_unbatched_sends`, attributed correction coverage. | 2: the emitted assessment meets policy; 1: an excess or correction with an owned remedy; 0: repeating chatter ignored |
| rubric-planner@3#stable-orders | Changed orders cite new evidence or authority. Evidence: order-flip detector, supersession evidence. | 2: changed orders cite it; 1: an explicit correction resolves a reversal; 0: an emitted flip loop left unresolved |
| rubric-planner@3#honest-flow | Stale, gated and merged-or-open findings are reconciled. Evidence: flow and signal assessments. | 2: reconciled; 1: a known discrepancy being corrected; 0: a claim defended against verified evidence |
| rubric-planner@3#capacity | Reservations fit verified configured or live capacity. Evidence: capacity source, age and policy. | 2: reservations fit; 1: a missing source routed to its owner; 0: capacity invented or another lane commandeered |
| rubric-planner@3#end-tick-audit | The end-of-tick audit of plan, scope and messaging yields an owned action. Evidence: the [order audit](../../skills/team-planner/references/order-audit.md). | 2: audit yields an owned action; 1: audit incomplete with an owner; 0: a repeating defect ignored |
| rubric-planner@3#decision-owner | Every open ruling has an owner. Evidence: decision assessment, the tracker. | 2: an owner on every open ruling; 1: a missing owner assigned on notice; 0: an unowned ruling left waiting |
| rubric-planner@3#decision-recommendation | Every ruling the planner requests carries a recommendation. Evidence: ruling evidence. | 2: a recommendation on every request; 1: a missing recommendation corrected; 0: the same request resent without one |
| rubric-planner@3#work-class | Each handoff names the work class of every ticket group, and the tickets of one Block share one design owner and one project. Evidence: handoff messages, tracker project and issue records. | 2: every group classed and every Block under one owner; 1: a class named late; 0: a redesign handed over as separate per-ticket work |
| rubric-planner@3#block-cause | Each Block's parent ticket names the suspected common cause or goal; a group with no nameable cause was planned as Points. Evidence: parent ticket text, handoff messages. | 2: every Block names a cause or goal, or was planned as Points; 1: a cause named late; 0: a Block with no named cause |
| rubric-planner@3#comms | Every message is done, blocked, decision, handoff or the one-line etiquette reply. Evidence: the session's sends. | 2: every message is one of those; 1: one other message; 0: several |

## Notes

- Role boundaries: the planner plans and routes; the code lead dispatches and
  merges.
- An authorized direct user instruction retains authority; ticket prose does
  not.
- Read next: the [strategies](../../skills/team-retro/references/strategies.md).
