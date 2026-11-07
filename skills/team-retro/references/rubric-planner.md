# Planner rubric

Score each row 0, 1 or 2 and cite the evidence. The planner plans and minds; it does not code, review or run another team's resources.

| Check | 2 | 1 | 0 | Evidence |
|---|---|---|---|---|
| Path set explicit | Gate tickets are named in the configuration and `ix-board chain <gate>` was run since the last retro | Named, not run | No gate tickets named | `config.json`, planner transcript |
| Intake discipline | `intake_new` is at most `path_closed` and `issues_without_milestone` is 0 | One of the two holds | Neither holds | `snapshot` |
| One count | `source_count_disagreement` is 0 and every quoted open-ticket count names its query | Disagreement exists but each count names its query | Counts quoted with no query | `snapshot`, messages the planner sent |
| Done means landed | `path_closed_unverified` and `done_reopened` are 0 | One is above 0 and has a recorded cause | Above 0 with no cause | `snapshot`, tracker |
| Role discipline | The planner started no review or coding subagents, did no work in another lead's lane and managed no other machine's resources | One incident, corrected | Repeated, or uncorrected | planner transcript (find it with `ix-board agents <team> --json`, then count `Agent` calls and relay sends), `agent-msg log` |
| Check-in cadence | Every planner message in the window is a done, blocked, decision or handoff message and no two messages to the same recipient are under 30 minutes apart | One exception | Several | `agent-msg log --since 24h` filtered by the planner's address |
| Decisions made | `decisions_open` is 0, or each open decision has a recommendation and an owner | Open without a recommendation | The same decision requested twice | `snapshot`, message log |
| Plan matches code | Each blocker edge a lane reported as wrong was corrected in Linear within one tick | One uncorrected | Several | relay log, `ix-board chain <gate>` |

Read next: [strategies.md](strategies.md) entries "Count the path", "Freeze intake", "Fix the graph".
