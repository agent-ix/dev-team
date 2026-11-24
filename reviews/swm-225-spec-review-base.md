---
id: SR-033
title: "spec-review base of SWM-225 rubric switch and minder spec"
type: SpecReview
analysis: base
scope: "agent-ix/dev-team; SWM-225; diff origin/main...5656282 (PR dev-team#33): skills/team-minder/**, skills/team-retro/**, skills/index.json, README.md, spec/rubrics/rubric-minder.md; against spec/roles/minder.md v3"
review_set: subset
date: 2026-11-24
---

# spec-review base of SWM-225 rubric switch and minder spec

## Summary

Base spec review of the rubric-minder edit and team-retro's switch to it, plus the role spec rules the lead's decisions 2 and 3 require to change.

Ticket: SWM-225. PR: dev-team#33 at 5656282. The lead's four decisions on the coder's open points were treated as binding intent.

## Verdict

**FAIL**. The rubric edit itself is correct: the deferral note is replaced by a statement that team-retro scores with v2, the rubric version stays 2 because no check changed, and team-retro cites `rubric-minder@2#<check>`. The findings are what the lead's decisions now require of the spec: a v4 role spec splitting MIND-R13 (high), rules for DEAD and empty-list idle lanes, a matching rubric v3, and rung 1 for blocked lanes.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | Lead decision 2 (owner approved answering dialogs and queued questions, SWM-226) is not in the spec: MIND-R13 v3 escalates every BLOCKED(question) to the lead. Bump spec/roles/minder.md to v4: split MIND-R13 so a queued_question (Codex 'Queued follow-up inputs') matching a standing order is answered and logged like a dialog (extend MIND-R11/R12/R14 and their evaluations to queued_question), and only a free-form question (last_class=question) is escalated to the lead. | spec/roles/minder.md:128 |
| FND-002 | medium | Lead decision 3 accepts routing DEAD lanes and IDLE lanes with an empty assignment list to the orchestrator with evidence, but no MIND rule requires either; the skill rows cite MIND-R16 (evidence content) as their authority. Add rules (with objective, class, source and evaluations) in the v4 bump: a DEAD lane, and an IDLE lane with an empty FR-072 list, SHALL be routed to the orchestrator with fleet status evidence in the tick found. | spec/roles/minder.md:116-131 |
| FND-003 | medium | After the decision-2 split, this check still scores a 'question' block not escalated to the lead as a failure, so a minder correctly answering a queued_question per a standing order would score 0, and #dialog-answer/#uncovered-answer do not mention queued questions. Bump the rubric to v3 with the v4 spec (login-blocker covers free-form questions only; dialog-answer and uncovered-answer cover queued_question) and move team-retro's citation to rubric-minder@3 in the same release, per the no-contradiction rule this PR applies. | spec/rubrics/rubric-minder.md:38 |
| FND-004 | medium | The in-fleet ladder sends rung 1 to the worker for every condition, including escalate_block conditions whose lane sits at a dialog, login or usage-limit screen. Relay delivery into that pane is pane input that MIND-R14 forbids and can select a dialog option. In v4, state that rung 1 is skipped (or deferred) while the lane is BLOCKED, or that rung 1 for a blocked lane goes to the lead. | spec/roles/minder.md:57-68 |

## Examined Scope

```yaml
scope:
- id: MIND-R04
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R04 | The minder SHALL send each escalation rung `fleet tick` emits in the tick it is emitted.
    | MIND-O02 | escalation-muted | "Never repeat" muted escalation, team-minder skill |'
- id: MIND-R11
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R11 | A lane in BLOCKED(dialog) whose dialog matches a standing order SHALL be answered per that
    order in the tick it is found. | MIND-O03 | dialog-not-cleared | Lanes blocked on queued questions and dialogs,
    MONITORING-DESIGN |'
- id: MIND-R12
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R12 | Every dialog answer the minder sends SHALL be recorded in the dialog answer log with its
    standing-order id. | MIND-O03 | dialog-not-cleared | Dialog answers unlogged and unreviewable, plan decision
    on dialogs |'
- id: MIND-R13
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R13 | A lane in BLOCKED(login), BLOCKED(usage_limit), BLOCKED(question), or BLOCKED(dialog) with
    no matching standing order SHALL be escalated to the lane''s lead in the tick it is found. | MIND-O03 | dialog-not-cleared
    | Lanes blocked on dialogs, MONITORING-DESIGN |'
- id: MIND-R14
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R14 | The minder SHALL NOT answer a dialog, login or permission prompt that no standing order
    covers. | MIND-O03 | unauthorized-answer | Plan decision: login screens and usage limits escalate |'
- id: MIND-R16
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R16 | Every escalation SHALL carry the ledger action id and the fleet status evidence it rests
    on. | MIND-O02 | minder-evidence-dismissed | Minder saw the idle lanes and was dismissed, 2026-11-23/24 |'
- id: rubric-minder@2#loop-alive
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#loop-alive | The minder loop ran every scheduled tick. Evidence: committed fleet ticks
    attributed to the minder session, scheduler entries. | 2: every tick committed; 1: a late or missed tick has
    a recorded remedy; 0: the loop stopped or was removed without the owner''s instruction |'
- id: rubric-minder@2#login-blocker
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#login-blocker | Login, usage-limit, question and unmatched dialog blocks were escalated
    to the lane''s lead at rung 0. Evidence: `escalate_block` actions, the minder''s sends. | 2: every such block
    escalated in the tick it was found; 1: escalated one tick late; 0: a block not escalated, or reported as working
    |'
- id: rubric-minder@2#uncovered-answer
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#uncovered-answer | No dialog, login or permission prompt was answered without a matching
    standing order. Evidence: answer log, transcript, open `escalate_block` actions. | 2: no uncovered answer; 1:
    an uncovered answer the minder itself reported and routed; 0: an uncovered prompt answered silently |'
- id: rubric-minder@2#dialog-answer
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#dialog-answer | A dialog matching a standing order was answered per that order and
    logged with the order id. Evidence: `answer_dialog` actions, the answer log, the lane''s next class. | 2: answered
    in the tick and logged; 1: answered late or the log entry incomplete; 0: a matched dialog left blocking the
    lane |'
- id: rubric-minder@2#escalation-ladder
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#escalation-ladder | Every in-fleet ladder rung that `fleet tick` emitted was sent
    in its tick, including repeats to a recipient that already had an earlier rung. Owner paging is Alertmanager''s
    and is not graded here. Evidence: ledger rung records, the minder''s sends. | 2: every rung sent in its tick;
    1: a rung sent one tick late; 0: a rung suppressed because an earlier message was sent |'
- id: rubric-minder@2#message-hygiene
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: '| rubric-minder@2#message-hygiene | The minder sent nothing beyond what `fleet tick` emitted, and no
    status polls. Sends the tick emits (pushes, `act_on_undetermined`, resends, answers, every ladder rung) count
    as required, never as excess. Evidence: relay sends by the minder against tick actions. | 2: every send matches
    an emitted action or rung; 1: one send outside them, corrected; 0: status polls, or repeated sends that no action
    or rung emitted |'
- id: rubric-minder
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: 'The minder rubric grades the judgement evaluations of the

    [minder role spec](../roles/minder.md). A judgement evaluation cites one

    check as `rubric-minder@2#<check-slug>`. `/team-retro` scores the minder

    with this version, and the `team-minder` skill is derived from the same role

    spec version.'
- id: skills/team-retro/SKILL.md:63
  path: skills/team-retro/SKILL.md
  role: examined
  excerpt: '1. Score every rubric: [planner](references/rubric-planner.md), [code lead](references/rubric-code-lead.md),
    [coder](references/rubric-coder.md), [reviewer](references/rubric-reviewer.md) and [minder](https://github.com/agent-ix/dev-team/blob/main/spec/rubrics/rubric-minder.md)
    (version 2, cited as `rubric-minder@2#<check>`). Each score is 0, 1 or 2 with one cited piece of evidence, or
    `n/a` when the evidence was not read; `n/a` stays out of the 0 to 2 scale and is listed under Data quality.
    Do not average scores into one number.'
```
