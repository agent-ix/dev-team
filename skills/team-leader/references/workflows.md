# Workflows

Two things govern sequencing beyond the per-ticket loop: whether a ticket is
specced before it's coded, and whether the project is large enough to need
speccing in layers.

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

## Layered, architecture-first workflow (large projects)

On a large project, spec the whole architecture or module in layers before
implementing any of it. Speccing a big system one ticket at a time, in
implementation order, produces a worse design than laying out the whole shape
first and then filling it in — later layers depend on decisions the earlier
ones made, and those decisions read better as a set than one at a time.

The tracker shows this as ordered milestones (or however the org's tracker
models layers), each ending in a gate ticket. The next layer starts only
after the previous layer's gate ticket passes. Read Start-up's "Load the
plan" for where this fits the normal queue-loading step.

Within one layer:

1. Spec wave: many tickets go through speccing at once. Run them as parallel
   spec-author lanes, each with its own non-overlapping block of requirement
   IDs so two authors never collide on numbering. Each spec PR gets its own
   single spec reviewer, same as any other spec PR.
2. Implementation wave: once a ticket's spec PR has merged, it moves to
   coding and code review, same as the per-ticket loop, in parallel with
   other tickets where files don't overlap.
3. Gate: the layer's gate ticket is checked last, once every ticket in the
   layer's spec and implementation waves is done.

Don't start implementing a layer while its spec wave is still open, unless a
given ticket's own spec PR is already merged and nothing else still open in
that wave would change it.

## Spec-only tickets

Some tickets exist only to produce a spec, with no code planned against them
in that ticket. They're done when the spec PR merges. Move them to the org's
specced or done state per the org's own convention — don't hold them open
waiting for code that belongs to a different ticket.

## Small or already-specced work

Work that's small, or already has an owning requirement, skips the spec-wave
machinery entirely and goes straight to the code step. See
[Work kinds: which subagent](../SKILL.md#work-kinds-which-subagent) for who
does that work.
