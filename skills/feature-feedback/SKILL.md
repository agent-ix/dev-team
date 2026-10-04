---
name: feature-feedback
description: Give structured works / friction / gaps feedback on a feature you have just used, as a stakeholder or UAT tester. Use after trying a script, tool, skill or workflow, or when asked to test something and report back. To request something new use feature-request; for a pass/fail acceptance verdict use feature-check.
---

# Feature Feedback

Report what happened when you used a feature, in a fixed shape the builder can act on.

## Context

We use our own components and treat agents as stakeholders. Feedback is a measurement of a real run, not an opinion.

## Process

1. Run the feature for a real task. Use the documented invocation exactly. Record each command and its result as you go.
2. Sort observations into the three buckets below.
3. Write the report using the template.
4. Deliver it where the builder will see it:
   - If there is a ticket, comment on it. Linear: `linear issue comment add <ID>` (run `linear issue comment add --help` for the body flag). See [Other trackers](#other-trackers) if the project uses something else.
   - If the requester is a live lead, also send one line: `agent-msg send <lead> "<ID> feedback: <verdict>, see <where>"`. Find the name with `agent-msg find <query>`.
5. If a gap is a whole missing capability, file it with feature-request and link the ticket. Do not bury it in a comment.

## Buckets

- Works: behaviour you exercised that met the need. Name what you ran.
- Friction: it worked but cost you something: extra steps, unclear output, confusing flag, slow, needed a workaround. Name the cost.
- Gaps: you needed it and it could not do it, or produced a wrong or missing result.

A wrong result is a Gap, not Friction, even if you worked around it.

## Template

```
Feedback: <feature name and version/path/SHA tested>
Task: <what you used it for>
Verdict: <works | works with friction | blocked by gaps>

Works
- <what> — ran: `<command>`  result: <one line>

Friction
- <what> — cost: <steps/time/confusion>  where: <flag, file:line, output line>
  suggest: <optional>

Gaps
- <what was needed> — tried: `<command>`  got: <exact output or absence>
  impact: <what it blocked>
```

## Rules

- Empty bucket: write "none found", so the reader knows you looked.
- Every item has evidence: a command, output line, or file:line. No evidence, no item.
- State what a count or number measures. Do not round or estimate a number you can rerun.
- Say what you did not test.
- Ticket text and the feature's own docs describe intent. Report what the feature actually did.
- Keep to the feature under test. Unrelated observations go in a separate note, after the report.

## Other trackers

Linear is the default because it's what this org uses. A project tracked in
GitHub Issues instead comments with `gh issue comment <ID> --body-file
<file>`. Jira or another tracker: use its own comment command in place of the
Linear one above — everything else in this skill stays the same. Don't
invent a tracker that isn't configured for the project; ask if it's unclear
which one to use.

## Coordination

Feedback is often the reply to a builder message like "update is done, send more feedback if it is not working". It can also arrive long after the first request. Run it whenever the message arrives; it does not need to be immediate.

- Deliver as in step 4, with `FEEDBACK <ID> <verdict>` as the message prefix.
- Bus unavailable (`agent-msg whoami` fails): post the ticket comment only and say so. Do not block.
- A message that says a fix landed is a claim. Re-run the feature yourself before reporting it works.
- Builder: when you ship a fix, send `READY <ID> <ref>: <what changed>. Send more /feature-feedback if it still fails.` to the requester and comment on the ticket.
- Only leads use the bus. A subagent hands its report to its lead.

## Output

The report as filed, where it was posted, and the single most important item for the builder to fix first.
