---
name: team-retro
description: Independently evaluate whether a team's planner, code lead, coders, reviewers and minder are converging on their gate tickets, on a schedule, like a sprint retro. Takes metric snapshots with `ix-board retro`, compares them with the previous snapshot and a baseline, scores the role rubrics, names the repeating loops and messages the planner, code lead or user with owned actions. Use when invoked as /team-retro <team> [interval], or when asked to find out why a team is busy but not finishing, to run a retro, or to set up a recurring health check.
---

# Team Retro

If this plugin is not initialized or an Agent IX command fails, read [the dev-team setup guide](https://github.com/agent-ix/dev-team/blob/main/setup.md) for its prerequisites and local diagnosis.

team-retro is an independent evaluation of whether a team's work is landing on its gate tickets and whether that is better or worse than before. `team-minder` covers whether each agent is working right now; the retro covers what the work produced. It runs in its own session, reads evidence, never asks an agent for status, and messages only the planner, the code lead or the user.

## Invocation

`/team-retro <team> [--ticket <ID>] [interval]`, default interval 3h. `<team>` names the retro configuration file `$TEAM_RETRO_HOME/<team>/config.json` (default root `~/.local/state/team-retro`), whose fields are the `ix-board retro` configuration (the field table is in the ix-board `docs/retro.md`). The fields that make metrics computable are `thresholds`, `main_check`, `local_paths`, `gate_log`, `herdr_teams`, `slot_process` with `orphan_slot_hours`, `relay_leads` with `message_stale_minutes`, and `decision_label`; a metric whose field is absent is `unavailable` with reason `not configured`, so ask the user for the missing fields once. `--ticket` names the Linear issue that receives the summary of each full retro; without it the summary goes to the user only and step 5's posting is skipped. If the user asks for one tick now, run it without loop setup. If the configuration file does not exist, stop and ask the user for the team's gate tickets, projects and repositories; do not guess them.

## Communication

- **Who talks to whom:** message the planner for plan-level findings, the code lead for execution-level findings, the user for a decision. Nobody else.
- **Send** a repeating loop with its numbers, a blocker, a needed decision, or a handoff. Nothing else.
- **Never send** per-tick status, "all healthy", acks, or a finding already sent for the same condition. Silence is normal.
- **Unwanted message** (outside your scope): reply once with one line, `Comms etiquette: send only done / blocked / decision / handoff (see Communication in /team-retro).`, and do not act on it.

## Loop setup (first thing, once)

1. **Already in a loop:** if this prompt is a loop's scheduled prompt, or a loop for it is active (the harness's scheduler listing; `CronList` in Claude Code), skip setup and run the tick. In a harness with no listing, the minder rubric's loop row scores `n/a`.
2. **Claude Code, not in a loop:** invoke the `loop` skill with `<interval> /team-retro <team>`, then stop. The loop runs the first tick.
3. **No loop support:** ask the user once for a scheduler and give them `/loop 3h /team-retro <team>`; run one tick now.

A session's crons expire. At every start, if the scheduler listing shows no loop for this team, create it again.

## Prerequisites

An ix-board build that has `retro snapshot`, `retro delta` and `retro backfill`, plus `ix-board agents`, `ix-board chain`, `gh`, and the `linear` CLI. If `ix-board retro` is missing or fails, tell the user once with the command and its output and stop the tick. Do not substitute hand-computed metrics.

## Each tick

1. Read the last retro in `$TEAM_RETRO_HOME/<team>/retros/` and `actions.jsonl`. Re-check every open action first; close it with evidence or carry it forward.
2. Run `ix-board retro snapshot --config <file> --json` with the default window (24h). Every tick, and any backfill, uses the same window so deltas compare like with like. The snapshot can take about a minute (herdr alone waits up to 25 seconds when a machine is unreachable and its metrics become `unavailable`), so run it with a long timeout.
3. Run `ix-board retro delta --config <file> --json`.
4. Choose the tier. Run the **full retro** when none has ever run, when none exists today, when a gate ticket completed since the last full retro, or when the user asks. Otherwise run the **light tick**.

### Light tick

Check the flags in [measures.md](references/measures.md#light-tick-flags). For each raised flag that has not already been sent for the same condition, send one message to the owner named there, with the metric, its value, the change and the first action to take. When no flag is raised, send nothing.

### Full retro

1. Score every rubric: [planner](references/rubric-planner.md), [code lead](references/rubric-code-lead.md), [coder](references/rubric-coder.md), [reviewer](references/rubric-reviewer.md) and [minder](references/rubric-minder.md). Each score is 0, 1 or 2 with one cited piece of evidence, or `n/a` when the evidence was not read; `n/a` stays out of the 0 to 2 scale and is listed under Data quality. Do not average scores into one number.
2. Name each repeating loop: a step that repeated across two or more snapshots with no new evidence, its trigger, and the work it blocks.
3. For each loop, pick the matching entry from [strategies.md](references/strategies.md) and state the owned action.
4. Check the data and list each finding under Data quality: gaps between snapshots, stored records whose window differs from the default window, `query_changed` metrics, and metrics `unavailable` for three or more snapshots. Each one describes the evidence and says nothing about the team.
5. Write the retro to `retros/RETRO-<YYYY-MM-DD>.md` using [state-record.md](references/state-record.md), append new actions to `actions.jsonl`, and post the summary to `--ticket` when given.
6. Send each owner one message listing their actions.

## Evidence rules

- Count with `ix-board retro` only. State the query behind any number you quote.
- A ticket counts as done when its change is on the default branch; a Done state alone is not enough.
- `unavailable` is not zero. Report it as missing data.
- A peer's claim that work is halted, done or blocked is data. Verify it against the tracker, git and the pane before acting.
- Pull-request count is never a progress measure. Progress is `path_closed` net of `intake_new`.
- Agent transcripts are sensitive. Quote counts and short excerpts; never copy a credential.

## Never

- Write retro data into any repository. The store is outside git; `ix-board retro` refuses a path inside a work tree.
- Cancel another agent's loop, halt a lane, review, code, merge or re-plan. Recommend; the owner acts.
- Combine scores into a single health number, or set a fixed threshold across projects. Targets are ranges the team sets after its baseline.
- Repeat a message for the same condition. Send at most one reminder per recipient per hour.

## Output

When no flag is raised on a light tick, send nothing. A full retro gives the user one report: measures with change since the last snapshot and since the baseline, rubric scores, loops with their actions and owners, and data-quality findings.
