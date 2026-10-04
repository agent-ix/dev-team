---
name: feature-request
description: Write a request for a new capability as a Linear ticket that another agent can build and a stakeholder agent can later accept. Use when you hit something the tooling cannot do, want new functionality, or are asked to file a feature request. For feedback on an existing feature use feature-feedback; to verify a delivered feature use feature-check.
---

# Feature Request

If this plugin is not initialized or an Agent IX command fails, read [the dev-team setup guide](https://github.com/agent-ix/dev-team/blob/main/setup.md) for its prerequisites and local diagnosis.

Request something new. The reader is the agent or team that will build it, and later the agent that will check it. Write for both.

## Context

We battle-test the components of our collaborative workflow by using them ourselves. Agents are the stakeholders and UAT testers. A request comes from real use: something you tried to do and could not.

## Process

1. Confirm it is new. Search the project's ticket tracker for an existing ticket (Linear: `linear issue query --search "<keywords>" --team <TEAM> --json`). If one exists, comment on it instead of filing a duplicate.
2. If the request is about an existing feature that is weak (not absent), use feature-feedback instead.
3. Write the request using the template below.
4. File it in the project's ticket tracker. Linear is the default: `linear issue create --team <TEAM> --label feature-request --no-interactive --title "..." --description-file <file>` (`linear api` for anything the subcommands miss). See [Other trackers](#other-trackers) if the project uses something else.
5. If a specific lead owns the area, tell them once: `agent-msg send <lead> "<TICKET-ID>: <one line>"`. Find the name with `agent-msg find <query>`.

## Template

```
Title: <capability, as a noun phrase. Not "add X button".>

Stakeholder: <which agent or role needs this, and the task they were doing>

Situation: <what you tried, the exact command or step, what happened.
Quote the error or the missing output.>

Desired capability: <what should be possible. Behaviour, not implementation.>

Acceptance checks:
1. <observable check: an input, an action, an expected result>
2. ...

Not in scope: <what this request does not ask for>

Workaround today: <what you did instead, and its cost. "none" is a valid answer.>
```

## Rules

- Acceptance checks are runnable by a different agent with no context from you. Each names an action and an observable result. "Works well" is not a check.
- Describe the capability, not the design. Suggest an implementation only under a separate "Suggestion" line, and mark it optional.
- Every check must be something you can test yourself when the feature lands (feature-check will do exactly that).
- Quote evidence from your own run. Do not assert what you did not measure.
- One capability per ticket. Split anything that needs two owners.
- If the request also describes the current state of an existing feature, add a short Works / Friction / Gaps section, same shape as feature-feedback.

## Other trackers

Linear is the default because it's what this org uses. A project using GitHub
Issues instead (no Linear workspace) files there: `gh issue create --title
"..." --body-file <file> --label feature-request`, and searches with `gh
issue list --search "<keywords>"`. Jira or another tracker: use its own
create and search commands in place of the Linear ones above — the template,
rules and coordination below stay the same. Don't invent a tracker that isn't
configured for the project; ask if it's unclear which one to use.

## Coordination

The ticket is the record. The bus (ix-relay) is the doorbell. Only leads use the bus; a subagent reports to its lead instead.

1. File the ticket first. Put a "Requester:" line in it with your bus name from `agent-msg whoami`. The bus has no threads, so the builder needs this address to reply.
2. Find the owner: `agent-msg find <area>`. Send one line:
   `agent-msg send <owner> "REQUEST <ID> <title>: <one-line need>. Acceptance checks are in the ticket. Reply 'READY <ID> <ref>' when built."`
3. If `agent-msg whoami` fails (for example Redis refused), skip the message. Add a ticket comment "relay unavailable, please pick up from Linear" and continue. Never block on the bus.
4. Do not wait. Carry on with other work. When `READY <ID> ...` arrives, treat it as a claim and run feature-check on it.
5. When the feature is delivered, feature-check and feature-feedback close the loop.

## Output

Report the ticket ID and URL, and the acceptance checks as filed. Next action for the reader: who is expected to pick it up.
