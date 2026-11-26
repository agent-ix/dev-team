# Churn retrospective

Run at each work-cycle restart and at the team's configured cadence. A repeated
gate, pin, merge hold or ruling with no changed evidence triggers an immediate
check. Continue unrelated, unblocked planned work.

## Record and read

Keep raw PR/ticket, dispatch, review/disposition, gate, lock and dependency
events in the existing state record and configured telemetry logs. Preserve
source IDs, timestamps, owner and reason when an event occurs. Do not reconstruct
event counts or durations from chat memory.

Use `ix-board retro snapshot --config <file> --json` and
`ix-board retro delta --config <file> --json` only when the installed CLI
advertises them. Follow the shared
[department evidence contract](../../team-retro/references/department-health.md).
Read emitted gate/fix rounds, pin churn, wait/hold, throughput, ruling/comms and
loop assessments with their prior/baseline changes. Missing metric, provenance
or instrumentation stays unavailable; no manual rate or loop calculation.

`ix-board next --team <TEAM>`, focus hygiene/plan-chunk and `gh pr view` remain
valid evidence for queue order, file overlap, current heads and blockers. They
do not replace a missing retro detector. Attribute work from explicit ticket
and lane ownership, not a shared account name. Preserve configured capacity and
source age separately from reported worker activity.

## Respond

1. Name each emitted repeating loop with event evidence, trigger and blocked
   work. A qualitative concern without a detector remains a cited concern,
   never a measured count or severity.
2. Test each proposed repeated gate, pin or hold: which changed input or risk
   will it check, and what decision uses the result? Remove repetition that adds
   no evidence within current authority. Keep required review and merge gates.
3. Use focused checks during iteration and one lead-run final aggregate gate.
   Fold same-Block work into its one PR, keep review records on the ticket, and
   act on a tripwire (more than 2 review rounds, 15 commits (not a Block) or 3 idle hours) by
   consolidating or recutting.
   Keep findings inside their original PR under current review-round policy.
   Fold required pins into consuming PRs under the assigned pin owner/window.
4. Route cross-team protocol, ownership or authority decisions once to their
   owner with evidence, options, tradeoff and recommendation. Hold only dependent
   work; do not impose rules on another lane.
5. Record one owned next action or that no supported finding was raised.
   The independent team-retro interprets the same model on its schedule.

## Agent conflicts

Before dispatch, compare live ticket/branch/file ownership with open PR file
lists and actual changed heads. Keep one pusher per branch. Resolve overlapping
scope before another dispatch; route foreign ownership through the planner.
Incompatible rulings require a single recorded resolution before more re-pins,
gates or briefs. Never infer conflict or spare capacity from worker counts.
