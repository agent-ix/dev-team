---
id: SR-057
title: "Code review of SWM-311 unconditional code-lead work reports"
type: SpecReview
analysis: code-review
scope: "agent-ix/dev-team@8765a6c40f8880b2a0e9c62e28f5d4937927e91e; skills/code-lead/SKILL.md, skills/index.json, plugin.json, .claude-plugin/marketplace.json, .claude-plugin/plugin.json, .codex-plugin/plugin.json"
review_set: subset
---

## Summary

Ticket: SWM-311. PR dev-team#42, diff origin/main...8765a6c40f8880b2a0e9c62e28f5d4937927e91e: skill text and manifest versions. Command syntax was compared with the subcommand help of the installed agent-msg 0.5.0 and with the ix-relay origin/main sources `crates/agent-msg/src/work.rs`, `crates/relay-core/src/work.rs`, `crates/relay-core/src/store/work.rs` and `crates/relay-ops/src/work.rs`. The trigger rules were compared with the consumer, factory-panel origin/main FR-028, `hooks/workview.tsx`, `hooks/work.ts` and `hooks/band/modules.ts`. Only read commands were run against the bus; no report was written.

## Verdict

**CHANGES REQUESTED**: three medium and one low finding, all in the "Dashboard work reports" section.

Checked and correct: the `work scope`, `focus`, `agent` and `remove` command forms and flags; `--lead` and `--session` are accepted between `work` and the subcommand and `agent-msg work show --lead x` is rejected; `--all-team` is exclusive of the narrower selectors; `agent` replaces one entry and `scope` replaces the previous scope. A failed report is non-blocking, and the 150-second limit covers the 120-second bounded Linear read that precedes `scope`, `focus` and `agent`.

Codex leads bind: every live Codex pane seen through `herdr agent list` on draco, luna, titan and terra reported a session id from Herdr, and `agent-msg work events` holds Codex agent transitions. No Codex-specific skill text is required.

Versions agree: 0.7.1 in the four plugin manifests (latest tag v0.7.0), code-lead 0.5.1 in `skills/index.json`; `claude plugin validate .` and `git diff --check` pass. No other dev-team skill dispatches ticket subagents for a team, so stating the duty in code-lead alone meets the second acceptance criterion. The third criterion (release, reload, Work tab) is post-merge and was not assessed.

Gap-analysis and spec-review do not apply: no production code and no `spec/` or `plan/` change.

## Findings

| ID      | Severity | Summary | Refs |
| ------- | -------- | ------- | ---- |
| FND-001 | medium   | The Work tab lists a lead's tickets from `agent` entries only. The start row publishes entries only for live subagents and one entry carries one ticket, so after a restart a ticket awaiting gate or merge is not listed, and a batch shows one of its tickets; `focus --ticket` does not add them. | skills/code-lead/SKILL.md:134, skills/code-lead/SKILL.md:148 |
| FND-002 | medium   | Reports are keyed by agent process, so a restart starts empty and the 30-minute refresh writes only `focus`. "Report again at the next row above" never resends a failed `scope` or a failed `done`, leaving the scope missing or an entry `running`. | skills/code-lead/SKILL.md:139, skills/code-lead/SKILL.md:157 |
| FND-003 | medium   | "Limit each wait" cannot produce the 30-minute `focus` for a Claude Code lead: a background subagent leaves the lead with no wait to limit, and nothing wakes it until the subagent finishes. | skills/code-lead/SKILL.md:154 |
| FND-004 | low      | A `failed` or `canceled` entry stays until the ticket closes, and the consumer marks a lead failed while any entry is `failed`, even after a replacement subagent is running. | skills/code-lead/SKILL.md:153 |
