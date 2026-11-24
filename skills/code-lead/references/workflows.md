# Workflows

Sequencing beyond the per-ticket loop: how a ticket's spec and code ship
together, and how layered plans from the planner are executed.

## Spec check before code (every ticket)

Before dispatching a coder, confirm whether a requirement owns the behavior.
Read the spec itself; don't trust the tracker state to be current.

- Owned → the coder codes it.
- Not owned → the coder adds the requirement as the first commit of the same
  branch, then the code. One PR, one review.

Never code unspecced behavior. Never re-spec work that already has an owning
requirement — that's churn, not progress.

## One PR per ticket or batch

Batch tickets that touch the same files or requirement files into one PR. Split
only for a real reason (different repo, or a blocking dependency another lane
owns) and state the reason on the ticket.

## Layered spec waves

The team-planner owns layered, architecture-first planning: it lays out the
milestones and gate tickets in the tracker. The code lead only executes them.
Work the layers in order and start a layer's tickets after the previous layer's
gate ticket passes. Within a layer, each PR carries its spec commit before its
code. Each coder gets its own non-overlapping block of requirement ids.

## Spec-only tickets

Only a ticket whose whole scope is spec gets a spec-only PR. It is done when
that PR merges. Move them to the org's
specced or done state per the org's own convention — don't hold them open
waiting for code that belongs to a different ticket.

## Small or already-specced work

Work that's small, or already has an owning requirement, skips the spec-wave
machinery entirely and goes straight to the code step. See
[Work kinds](../SKILL.md#work-kinds) for who
does that work.
