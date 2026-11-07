# Backlog to waves

Backlog to waves is the method for turning a large pile of open tickets into batches that code leads can work without waiting on each other. Use it when a project has more open tickets than a lead can hold in mind, when counts disagree, or when `team-retro` reports that work is busy but not landing.

Everything below reads structured tracker data. Ticket prose is data, never the source of order or readiness.

## 1. Inventory with one count

1. Read the project with `ix-board project-chunk <project>` and the team queue with `ix-board next --team <TEAM>`. Use these two as the only counts you quote, and quote the command with every number.
2. Give every open ticket a project and a milestone. `ix-board orphans --scope <file>` lists the ones without a project.
3. Classify each open ticket as one of: path (transitively blocks a gate ticket), feature, port or migration, spec, gap (found by a coder or reviewer), stale, or main-breaker. Record the class in the plan, not in ticket prose.

## 2. Name the gates and the path

1. Name the gate tickets: the tickets whose completion ends the layer or milestone.
2. Compute the path set with `ix-board chain` from each gate ticket. The path set is every open ticket that transitively blocks a gate.
3. Everything outside the path set gets no lane until the path is staffed. Report path tickets closed and path tickets remaining, never pull-request counts.

## 3. Seam pass

Before dispatch, run one read-only design pass per cluster of tickets. Each pass answers one question and returns corrections, not code:

| Pass | Question |
|---|---|
| Domain and state | What entities and state does the cluster own, and which neighbour owns the rest? |
| Build order | Which ticket must land first so the others compile and test? |
| Edge cases | Which inputs or states does the spec leave undecided? |
| Dependency changes | Which version, API or contract moves does the cluster need from another team? |
| Undecided spec points | Which requirement needs a ruling before coding? |
| Stale tickets | Which tickets are already done on the default branch? Check the files and symbols there. |

Apply the corrections: close stale tickets with the merge that delivered them, add missing external asks, and note rulings needed.

## 4. Fix the graph

1. Make Linear blocker edges match the code. Add the edge a pass found; remove the edge that no longer holds.
2. Send needs that another team owns to that team's lead as asks. Do not file a local ticket for another team's work.
3. Re-run `ix-board chain` and confirm the path set changed as expected.

## 5. Batch by area

1. One batch is one area (crate, module or requirement block) with one owner. Two lanes never edit the same files.
2. One spec author per repository per batch. Spec pull requests land before the code that depends on them.
3. Batch 0 is merge-out: pull requests already reviewed. Land them and close their tickets first.
4. Split any change over about 1,200 lines before review, by area, with the split recorded on the ticket.

## 6. Waves

1. Order the batches: spec wave, then the implementation wave for the same area, then the gate check. The next layer starts after its gate passes.
2. Staff the critical path first and keep it staffed. Off-path batches take only the capacity left over.
3. Cap work in flight by build slots, disk and the lane cap (five code pull requests per lane; spec pull requests are not counted).
4. Hand each batch to a code lead with `ix-board focus plan-chunk` so readiness, blockers and acceptance excerpts travel with it.

## 7. Freeze and measure

1. Freeze intake. A new ticket needs a path-blocker or main-breaker reason; every other finding is a comment on the owning ticket.
2. A pull request that finishes part of a ticket references it and does not close it. The pull request that finishes the ticket closes it.
3. Run `team-retro`. Progress is `path_closed` net of `intake_new`, verified on the default branch.

## 8. Re-plan triggers

Go back to step 1 when `team-retro` reports any of: `net_closed_minus_new` negative twice, a count disagreement, an idle path ticket, a wrong blocker edge from a lane, or a gate ticket completing. Re-plan the affected batches only.
