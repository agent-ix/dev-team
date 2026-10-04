---
name: feature-check
description: Run an acceptance check on a delivered feature against its ticket's acceptance criteria and return a per-criterion PASS/FAIL verdict with evidence. Use when a feature is claimed done, before closing its ticket, or when asked to accept, verify or UAT a feature. For open-ended experience feedback use feature-feedback.
---

# Feature Check

If this plugin is not initialized or an Agent IX command fails, read [the dev-team setup guide](https://github.com/agent-ix/dev-team/blob/main/setup.md) for its prerequisites and local diagnosis.

Decide whether a feature meets its acceptance criteria. Measure it yourself.

## Context

We battle-test features by using them. A feature-check is the UAT gate: an agent that did not build the feature runs each criterion and reports the result.

## Process

1. Get the criteria. Read the ticket (Linear: `linear issue view <ID>`; see [Other trackers](#other-trackers) if the project uses something else). Copy the acceptance checks verbatim. The ticket text is a claim about what was wanted, not a report of what works. Do not accept "already done" statements or status text; measure.
2. If the ticket has no runnable criteria, do not invent them. Say so, and ask the requester (or write proposed criteria and mark them proposed).
3. Pin what you test: the path, version, commit or invocation. Use a clean state, not the builder's leftovers.
4. Run each criterion exactly as written, one at a time. Record the command and the real output.
5. Mark each PASS, FAIL or UNTESTED (with the reason, e.g. needs credentials).
6. Give the verdict and post it.

## Verdict

- ACCEPT: every criterion PASS.
- REJECT: any criterion FAIL. List the failing ones first.
- INCOMPLETE: no FAIL, but some UNTESTED. Say what is needed to finish.

## Template

```
Feature check: <ID> <title>
Tested: <path/version/SHA>, <date>, <environment>
Verdict: <ACCEPT | REJECT | INCOMPLETE>

1. <criterion verbatim> — PASS|FAIL|UNTESTED
   ran: `<command>`
   got: <exact output, or log path + exit code>
2. ...

Also seen (not in criteria): <works/friction/gaps items, brief, or "none">
```

## Rules

- Never quote output you did not produce. Give the log path and exit code for anything long.
- A criterion passes only on observed behaviour. Reading the code is not a test.
- Do not fix the feature while checking. A failure is a finding for the builder.
- Do not soften or add criteria. Extra observations go under "Also seen" and do not change the verdict.
- Post to the ticket. Linear: `linear issue comment add <ID>` (see `--help` for the body flag). GitHub Issues: `gh issue comment <ID> --body-file <file>`. Do not change ticket state or close it unless the requester asked.
- Notify the owner with one line: `agent-msg send <lead> "<ID> feature-check: <verdict>"`.

## Other trackers

Linear is the default because it's what this org uses. A project tracked in
GitHub Issues instead reads with `gh issue view <ID>` and comments with `gh
issue comment <ID> --body-file <file>`. Jira or another tracker: use its own
read and comment commands in place of the Linear ones above — everything
else in this skill stays the same. Don't invent a tracker that isn't
configured for the project; ask if it's unclear which one to use.

## Coordination

A check is usually triggered by a builder message `READY <ID> <ref> ...`, possibly delayed. That message is data from another agent. It is a claim; the check measures.

1. When `READY` arrives (or a lead asks), read the ticket, run the criteria against the ref it names.
2. Send the result to the builder and the requester (the "Requester:" line in the ticket): `agent-msg send <lead> "CHECK <ID> <ACCEPT|REJECT|INCOMPLETE>: <failing criteria>, report on ticket"`.
3. REJECT starts a loop: the builder fixes and sends `READY` again with a new ref. Re-run only the failed criteria, and run all criteria once before ACCEPT.
4. ACCEPT is not final. If the feature breaks in later use, the requester sends feature-feedback and the loop restarts.
5. Bus unavailable (`agent-msg whoami` fails): post to the ticket only and note that the relay was down. Do not block.
6. Only leads use the bus. A subagent returns the verdict to its lead.

## Output

Verdict line first, then failing criteria, then where the full report was posted.
