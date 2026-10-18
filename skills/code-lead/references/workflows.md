# Workflows

Sequencing beyond the per-ticket loop: whether a ticket is specced before it
is coded, and how layered plans from the planner are executed.

## Spec check before code (every ticket)

Before dispatching a coder, check whether the work is specced:

- The ticket is in the org's specced state, and/or a requirement already owns
  the behavior. Check both — a state alone isn't proof. Read the spec itself;
  don't trust the tracker state to be current.
- Specced → dispatch a coder straight away.
- Not specced → spec it first: spec author, then spec reviewer, then the spec
  PR merges. Only then dispatch the coder.

Never code unspecced behavior. Never re-spec work that already has an owning
requirement — that's churn, not progress.

## Layered spec waves

The team-planner owns layered, architecture-first planning: it lays out the
milestones and gate tickets in the tracker. The code lead only executes them.
Work the layers in order, start a layer's tickets after the previous layer's
gate ticket passes, and run each layer's spec PRs before the code that depends
on them. Each spec author gets its own non-overlapping block of requirement ids.

## Spec-only tickets

Some tickets exist only to produce a spec, with no code planned against them
in that ticket. They're done when the spec PR merges. Move them to the org's
specced or done state per the org's own convention — don't hold them open
waiting for code that belongs to a different ticket.

## Small or already-specced work

Work that's small, or already has an owning requirement, skips the spec-wave
machinery entirely and goes straight to the code step. See
[Work kinds](../SKILL.md#work-kinds) for who
does that work.
