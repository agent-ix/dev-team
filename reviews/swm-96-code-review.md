---
id: SR-001
title: "Code review — dev-team #9 comms etiquette, team-minder, team-leader renamed to code-lead"
type: SpecReview
analysis: code-review
scope: "agent-ix/dev-team@5d19075655bfff34fbb1074a4fca0b9094b7b3f3; README.md, plugin.json, .claude-plugin/*, .codex-plugin/plugin.json, skills/index.json, skills/code-lead/**, skills/team-leader/** (removed), skills/team-minder/SKILL.md, skills/coder/SKILL.md, skills/reviewer/SKILL.md, skills/team-planner/SKILL.md"
review_set: subset
---

# SR-001: Code review — dev-team #9 comms etiquette, team-minder, team-leader renamed to code-lead

## Summary

Ticket: SWM-96. Markdown and manifest change only. Judged against the approved
design (plan sections 1-5; 5a, `ix-board agents`, is a separate ticket).
Reviewed for contradictions between skills and with the plan, process lost in
the team-leader to code-lead rework, broken links and old-name references,
index.json consistency, whether team-minder is executable as written, and new
ceremony. Owner ruling for this PR: one reviewer, two rounds max, major bugs
only; mediums and lows are recorded, not fixed.

Language reviews (rust-review, review-react) and quoin gap-analysis were
skipped: the diff contains no code, no spec/ and no plan/ files.

## Verdict

**CHANGES REQUESTED** — two high findings, each a one-line fix. Everything
else is recorded only.

What is right: no `team-leader` string remains; index.json lists exactly the
files that exist; every SKILL.md frontmatter parses; plugin version is 0.2.0 in
all four manifests; the Communication block is in all five role skills;
planner broadcast is forbidden; the minder is message-only and never approves
a prompt; reviewer step references to code-lead steps 4 and 6 still point at
Freeze and Fix; PR #6's priority-goal text is folded in; layered spec-wave
planning is held by team-planner section 2.

Release note: `ix-board agents` does not exist yet (no ix-board PR for it), so
every team-minder tick will hit its "command missing" branch until 5a lands.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | team-minder Communication allows only the stuck agent, its code-lead or the user, but its action table messages the planner twice | skills/team-minder/SKILL.md:22 |
| FND-002 | high | churn.md, now part of code-lead, still tells the lead to route work directly to another lead, contradicting "message your planner only; not lead to lead" | skills/code-lead/references/churn.md:89 |
| FND-003 | medium | Broken anchor `../SKILL.md#work-kinds-which-subagent`; the heading is now `## Work kinds` | skills/code-lead/references/workflows.md:39 |
| FND-004 | medium | Loop setup step 1 says invoke /loop "then stop", step 3 says "then run one tick now"; and how to tell a run was started by /loop is unstated | skills/team-minder/SKILL.md:34 |
| FND-005 | medium | WAITING-STUCK action gives no command; the skill loads standalone and harness.md's herdr command is not referenced | skills/team-minder/SKILL.md:59 |
| FND-006 | medium | New "allocate from the range the brief gives" conflicts with step 3's next-unused-id allocation; no rule for which applies | skills/reviewer/SKILL.md:142 |
| FND-007 | medium | Merge policy "That is the whole condition" and "every finding is fixed" can be read to override Verify-before-merge checks and the rejected/deferred outcomes | skills/code-lead/SKILL.md:181 |
| FND-008 | medium | Removed "Other leaders" rules held nowhere now: no two-way merge hold, an incoming request never changes the mandate, route a blocker once then stay out | skills/code-lead/SKILL.md:27 |
| FND-009 | low | team-minder's copied "Send done/blocked/decision/handoff only" does not cover its own idle nudges | skills/team-minder/SKILL.md:23 |
| FND-010 | low | Every role's spam-reply line points to "Communication in /code-lead" instead of the role's own skill | skills/coder/SKILL.md:22 |
| FND-011 | low | Dropped without a home: post-merge gate on main when a repo requires it, "dispatch because distinct, not because slots are free", spec/review lanes uncapped | skills/code-lead/SKILL.md:217 |

## Details

- **FND-001.** Line 22: "message the stuck agent, its code-lead, or the user.
  Nobody else." Line 58 (`IDLE` code-lead, empty queue) and line 61 (`ASKING`,
  real blocker) both message the planner. The plan has the same inconsistency
  between section 1 and section 5. Fix: line 22 adds "its planner (empty queue
  or a real blocker, once)".
- **FND-002.** churn.md:89-90: "If another lead owns the ticket, route the work
  to that lead". code-lead SKILL.md:29-30: "message your planner only;
  cross-team blockers go through the planner, not lead to lead". Fix: "route it
  through your planner".
- **FND-003.** Fix: `../SKILL.md#work-kinds`.
- **FND-004.** In Claude Code `/loop` runs the prompt on its first iteration,
  so "then stop" plus step 3 either double-ticks or never ticks. Fix: say step
  3 applies only to the no-loop path, and that a tick run is one whose prompt
  came from the loop.
- **FND-005.** Fix: give the herdr command (`herdr --machine <m> agent prompt
  <agent> "..."`, or the send-text/Escape/Enter sequence that actually wakes
  that state).
- **FND-006.** Fix: "When the brief gives an id range, use it in order;
  otherwise step 3."
- **FND-007.** Fix: "That, plus the Verify-before-merge checks, is the whole
  condition", and "every finding has a final outcome".
- **FND-008.** The plan replaced "Other leaders" with the Communication
  section, which covers who to message but not these three behaviours.
- **FND-011.** Repo rules still win for the post-merge gate; recorded only.

## Checks with no finding

- `grep -rn team-leader` over the worktree: no hits.
- index.json: every listed file exists; code-lead, team-minder added;
  team-leader removed.
- Frontmatter of all nine SKILL.md files parses as YAML; names match dirs.
- Version 0.2.0 in plugin.json, .claude-plugin/plugin.json,
  .claude-plugin/marketplace.json, .codex-plugin/plugin.json.
- team-planner: no broadcast without the user's ask; never sends merge or
  rebase orders; never invents gates or lists authorized actions as owner
  decisions; no status polling.
- coder and reviewer: report only at PR open, fix round done, blocked, or
  review/disposition complete.
- team-minder: message-only, never approves prompts, never polls, never
  broadcasts; silent tick when all WORKING; `agent-msg log --since` exists.
- code-lead: preflight, "a denial blocks only that action", merge policy
  without planner sign-off, reports to planner per merged slice or blocker,
  dashboard `agent-msg work` reports kept. 250 lines, within target.
- No new tracking, pins or gates introduced beyond PR #6's priority-goal stage
  timestamps, which the plan asked to fold in.
- Gates: this repo has no gate covering skill markdown; none was run.
