# Planner rubric

Score each row 0, 1 or 2 and cite the evidence. The planner plans and minds; it does not code, review or run another team's resources.

| Check | 2 | 1 | 0 | Evidence |
|---|---|---|---|---|
| Path set explicit | Gate tickets are named and `path_remaining` was recomputed since the last retro | Named, not recomputed | No gate tickets named | retro config, `ix-board chain` |
| Intake discipline | `intake_new` is at most `path_closed` and `issues_without_milestone` is 0 | One of the two holds | Neither holds | `snapshot` |
| One count | `source_count_disagreement` is 0 and every quoted open-ticket count names its query | Disagreement exists but each count names its query | Counts quoted with no query | `snapshot`, messages the planner sent |
| Done means landed | `path_closed_unverified` and `done_reopened` are 0 | One is above 0 and has a recorded cause | Above 0 with no cause | `snapshot`, tracker |
| Role discipline | No review or coding subagents started by the planner, no work taken from another lead's lane, no other machine's resources managed | One incident, corrected | Repeated, or uncorrected | planner transcript (count `Agent` calls and relay sends to other lanes), `agent-msg log` |
| Check-in cadence | Updates to the user and lead are spaced by the agreed interval and each reports done, blocked, decision or handoff | Occasionally early or status-only | Repeated status-only messages | `agent-msg log` |
| Decisions made | `decisions_open` is 0, or each open decision has a recommendation and an owner | Open without a recommendation | The same decision requested twice | `snapshot`, message log |
| Plan matches code | Blocker edges added or corrected since the last retro after a seam pass | Edges unchanged while the lane reported a wrong edge | A lane reported a wrong edge and it stayed | tracker history, lane reports |

Read next: [strategies.md](strategies.md) entries "Count the path", "Freeze intake", "Fix the graph".
