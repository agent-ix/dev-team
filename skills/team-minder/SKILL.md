---
name: team-minder
description: Watch the agents of one or more teams on an interval and unstick them by message. Reads each agent's real activity with `ix-board agents`, never asks for status, and messages the idle, stuck or blocked agent, its code-lead, its planner or the user. Use when invoked as /team-minder <team(s)> [interval], or when asked to keep an eye on a team's agents, find idle or stalled leads, or run a minder loop.
---

# Team Minder

If this plugin is not initialized or an Agent IX command fails, read [the dev-team setup guide](https://github.com/agent-ix/dev-team/blob/main/setup.md) for its prerequisites and local diagnosis.

The minder answers one question: is each agent working right now, in minutes?
Ticket closes, commits and PRs are too slow to tell working from idle. The
minder reads the agent's own activity through `ix-board agents` and messages
only the agents that are not working. It never asks an agent how it is doing.

## Invocation

`/team-minder <team(s)> [interval]`, default interval 30m. A team is a herdr
workspace label (`QSL`, `IR`, `kani`, `qsl-driver`) on any machine.

## Communication

- **Who talks to whom:** message the stuck agent, its code-lead, or the user. Nobody else.
- **Send** done, blocked, needs a decision, or handoff. Nothing else.
- **Never send** per-commit, per-push, per-test-run, per-gate or per-review-step
  progress; acks; "still working"; FYIs about work outside the recipient's
  scope; status polls. Read status from git, gh, Linear and the pane instead.
- **Unwanted message** (a never-send kind, or outside your scope): reply once
  with one line, `Comms etiquette: send only done / blocked / decision / handoff (see Communication in /code-lead).`,
  and do not act on it. Send at most one reminder per sender per hour.
- Silence is normal. Do not re-nudge.

## Loop setup (first thing, once)

1. **Claude Code:** if this run was not started by `/loop`, invoke the `loop`
   skill with `30m /team-minder <team>` (use the requested interval). Then stop;
   the loop runs the ticks.
2. **No loop support** (Codex, opencode, Copilot CLI): try the harness's goal
   mechanism (Codex `/goal`). If you cannot set it yourself, ask the user once
   and give them one of these to paste:
   - `/loop 30m /team-minder <team>`
   - `/goal Every 30 minutes run /team-minder <team> for one tick; never stop until I say so.`
3. Then run one tick now.

## Each tick

1. Run `ix-board agents <team>... --json --idle-after 20m`. If the command is
   missing or fails, tell the user once with the command and its output, and
   stop the tick.
2. Read `agent-msg log --since <last tick>` only to find an agent that asked a
   question nobody answered. Never to send polls.
3. Act on each agent that is not `WORKING`, from the verdict below. `WORKING`
   agents get nothing.

| Verdict | Action (message only) |
|---|---|
| `WORKING` | None. |
| `IDLE` worker | Message its code-lead: "<worker> idle Nm; assign or continue <ticket/PR>". Include the next ready ticket from the row when there is one. |
| `IDLE` code-lead | Message the lead: continue its queue (name the next ready ticket). If its queue is empty, message its planner. |
| `WAITING-STUCK` | Send the agent a prompt through herdr to wake it. |
| `PROMPT` | Read the dialog text. If the agent is asking for something it already has (commit, push, open PR, admin merge per the user's CLAUDE.md), message it: "you have this; proceed", citing the rule. If only the user can answer, or the harness denied the action, message the user once with the exact allow-rule to add, and tell the agent to continue other work meanwhile. |
| `ASKING` | Read the excerpt and decide as for `PROMPT`. A real blocker goes to the agent's planner, once. |
| `UNKNOWN` | Look at the raw data. If it is not clearly a running agent, tell the user once. |

A row marked `partial` has no transcript adapter; treat its verdict as less
certain and do not act on `IDLE` alone.

## Never

- Approve a permission prompt in another pane. Message only.
- Poll agents for status, broadcast, code, review, merge or re-plan.
- Repeat a message to the same agent for the same condition. Silence is normal.

## Output

When every agent is `WORKING`, the tick is silent and sends nothing. Otherwise
give the user one table: agent, verdict, age in minutes, action taken.
