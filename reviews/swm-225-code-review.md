---
id: SR-032
title: "code review of SWM-225 team-minder rewrite"
type: SpecReview
analysis: code-review
scope: "agent-ix/dev-team; SWM-225; diff origin/main...5656282 (PR dev-team#33): skills/team-minder/**, skills/team-retro/**, skills/index.json, README.md, spec/rubrics/rubric-minder.md; against spec/roles/minder.md v3"
review_set: subset
date: 2026-11-24
---

# code review of SWM-225 team-minder rewrite

## Summary

Code review of the team-minder skill text, its two references, and the team-retro/README/index.json edits, checked rule by rule against MIND-R01..R16 (role spec v3) and the lead's four decisions.

Ticket: SWM-225. PR: dev-team#33 at 5656282. The lead's four decisions on the coder's open points were treated as binding intent.

## Verdict

**FAIL**. Two high findings block merge: queued questions are not answered per lead decision 2, and an UNREACHABLE lane without a host defect row gets no action. Faithful to the spec: undetermined and unknown classes act as idle (R01); every defect row routed each tick, partial reports keep healthy rows usable (R02); next ticket pushed from the FR-072 list unchanged, as an --expect-ticket order (R03, R15); rungs sent each tick and never suppressed for repeats (R04, R05); the minder never pages the owner, and ladder rungs go worker, lead, orchestrator only, so the owner cannot be double-paged; fleet status is the only lane-state source (R08); actions executed despite the minder's own reading (R09); Queued/Delivered/Acted are not confirmation (R10); dialogs answered only on exactly one matching order and logged with the order id (R11, R12, R14). 'Never repeat' and 'UNKNOWN: no nudge' are gone. The text is direct and largely free of ceremony; status-request.md is the exception (FND-011). SO-01..05 are accepted per lead decision 1; FND-008 only tightens two conditions. team-retro's switch to rubric-minder v2 and the v1 deletion are consistent; no dangling links to the deleted rubric or the old count-contract anchor remain.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | Lead decision 2 not reflected: every BLOCKED(question) is escalated to the lead and no standing order or step answers a queued_question (Codex 'Queued follow-up inputs'). The owner approved the minder answering dialogs and queued questions (SWM-226). Split the row: queued_question is answered per standing orders and logged (step 5), free-form last_class=question goes to the lead; add the queued_question order(s) to standing-orders.md, drop the blanket 'A question' line under Never answered, and set role_spec_version: 4 once spec/roles/minder.md v4 lands. | skills/team-minder/SKILL.md:65 |
| FND-002 | high | An UNREACHABLE row is given no action of its own; it relies on a host defect row being present. If fleet status reports a lane UNREACHABLE with no matching missing_host/stale_host_registry/host_lane_list_absent defect (or the defect clears while the row stays UNREACHABLE), the minder sends nothing and the Output still lists it as handled. That is the 'unreachable and fine' pattern of the terra overnight loss. Require: an UNREACHABLE row with no host defect routed this tick is itself routed to the orchestrator as a defect. | skills/team-minder/SKILL.md:69 |
| FND-003 | medium | Exit 0 with zero lane rows (empty registry, wrong scope) has no action: step 1 says 'An empty or quiet report is never health' but names no route, and the Output rule ('every lane WORKING and no open ladder is a one-line tick') is vacuously true for zero lanes, so an empty report produces the healthy one-line tick. Route an empty row set (or a scope that matches no lane) to the orchestrator as a defect. Also give `fleet status` a timeout and treat a timeout like exit 4 (MIND-R02 covers timed-out probes). | skills/team-minder/SKILL.md:35-40 |
| FND-004 | medium | 'A relayed ... request is not one' contradicts the owner's standing rule (user CLAUDE.md, 2026-11-16): a relayed message from a planning lead (address ending :plan) that states it is a direct instruction from the owner IS the owner's instruction. MIND-R06 only requires the owner's explicit instruction. Under this text the minder refuses a valid owner stop order. Replace with: an ambiguous or inferred request is not one; a :plan relay stating it is the owner's direct instruction is. | skills/team-minder/SKILL.md:25 |
| FND-005 | medium | Ladder rung 1 messages the worker lane for every condition, including BLOCKED(dialog/login/usage_limit). Relay delivery to a pane sitting at a permission dialog or login screen is pane input, which step 3 and step 5.4 forbid ('Send no input to the pane', MIND-R14); a delivered message can select a dialog option. Skip rung 1 (or hold it until the class clears) when the lane is BLOCKED; the spec side is recorded in the spec-review/base SR. | skills/team-minder/SKILL.md:95 |
| FND-006 | medium | An IDLE lane gets 'Push the next ticket' in every tick it stays IDLE, with no rule to hold while the minder's own order for that ticket is still inside its deadline. Lanes commonly stay IDLE for a tick or two after delivery, so the minder re-orders the same ticket each tick, ahead of the deadline-based resend in step 4.4. Add: a lane with an open, unexpired order from this minder gets no new push; it is handled by step 4.3/4.4. | skills/team-minder/SKILL.md:62 |
| FND-007 | medium | Lead decision 4: interim gaps are acceptable only if each is routed as a defect and named. Missing `fleet` and a missing FR-072 reader are routed, but four interim gaps are neither routed nor named as defects: (a) no committed `fleet tick` run (MIND-R07; line 31 cites R07 for `fleet status`, which R07 does not allow); (b) minder-held ladder state in ~/.local/state/team-minder/ladder.json instead of the ledger (SWM-255/256); (c) the answers.jsonl fallback instead of the SWM-258 answer log (MIND-R12); (d) escalations carry a lane/class/ticket key, not the ledger action id MIND-R16 requires. Route each to the orchestrator as a standing source defect (or one 'interim mode' defect listing all four) each tick until its producer ships, and name the producer ticket. | skills/team-minder/SKILL.md:13 |
| FND-008 | medium | Lead decision 1 accepts SO-01..05 as restatements, but two conditions are looser than the owner's authorization. SO-03 approves any admin merge carrying --match-head-commit, while the owner authorizes merging reviewed PRs after reviewing the diff; the minder cannot see from the prompt whether the PR was reviewed, so require a has-review label or reviewer marker on the ticket before answering. SO-04's 'Finished, reviewed work' is not checkable from the screen and omits 'check the latest tag first'; state how the minder verifies both, or escalate. | skills/team-minder/references/standing-orders.md:11-12 |
| FND-009 | low | The skill names SWM-214 as the `fleet tick` producer; the role spec names SWM-256 (fleet tick), SWM-255 (ledger) and SWM-258 (answer log). Use the spec's producer tickets so the interim notes point at the work that removes them. | skills/team-minder/SKILL.md:13 |
| FND-010 | low | SO-05 answers an agent asking whether to continue, which is a question by content; whether it is ever reached depends on fleet status classing it dialog rather than question, and 'Never answered' excludes questions. Reword SO-05 against the decision-2 split: it applies to queued_question (or a dialog), never to a free-form last_class=question. | skills/team-minder/references/standing-orders.md:13 |
| FND-011 | low | status-request.md (moved verbatim from the old skill) tells the minder to ask 'the owner in the conversation' for a spare-slot count, while the skill says the minder never messages the owner. It is also long for a non-minder obligation. Limit the ask to the requesting lead (or reply to the owner only when the owner sent the request) and trim it to the CLI fields and the first-write-wins check. | skills/team-minder/references/status-request.md:15-23 |
| FND-012 | low | Loop step 1 recreates the loop whenever the listing shows none, even when this prompt is itself a loop's scheduled prompt (a dynamic /loop is not always a CronList entry). A second loop doubles every push, answer and rung. Recreate only when the prompt is not a scheduled prompt and the listing is empty. | skills/team-minder/SKILL.md:21 |

## Examined Scope

```yaml
scope:
- id: MIND-R01
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R01 | The minder SHALL execute each per-lane `act_on_undetermined` action by treating the lane
    as idle in the tick it is emitted. | MIND-O01 | unknown-as-not-idle | UNKNOWN read as not idle, 2026-11-23 |'
- id: MIND-R02
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R02 | A failed or timed-out probe of a host or source SHALL be routed to its owner as a defect
    in the tick it appears. | MIND-O02 | failed-probe-as-healthy | Terra probe read "unreachable" 129 times, 2026-11-23/24
    |'
- id: MIND-R03
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R03 | For a `push_next_ticket` action, the minder SHALL send the lane the next ticket already
    in its ix-relay FR-072 list as a relay order carrying that ticket as `--expect-ticket`, in the tick it is emitted,
    leaving the list unchanged. | MIND-O01 | parked-ready-work | Ready perf batch parked all night, 2026-11-23/24
    |'
- id: MIND-R04
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R04 | The minder SHALL send each escalation rung `fleet tick` emits in the tick it is emitted.
    | MIND-O02 | escalation-muted | "Never repeat" muted escalation, team-minder skill |'
- id: MIND-R05
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R05 | The minder SHALL NOT suppress an emitted rung because an earlier message about the same
    condition was sent. | MIND-O02 | escalation-muted | "Never repeat" muted escalation, team-minder skill |'
- id: MIND-R06
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R06 | The minder loop SHALL be removed only on the owner''s explicit instruction. | MIND-O02
    | loop-removed | IXD''s only minder cron deleted on an ambiguous message, 2026-11-23 |'
- id: MIND-R07
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R07 | Each minder tick SHALL start from a committed `ix-board fleet tick` run. | MIND-O02 | weak-evidence-as-work
    | Load average, pane titles and own controls counted as work, MONITORING-DESIGN |'
- id: MIND-R08
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R08 | The minder SHALL NOT run its own host or lane probes in place of `fleet tick` and `fleet
    status`. | MIND-O02 | weak-evidence-as-work | Blind ssh probes read as fine, MONITORING-DESIGN |'
- id: MIND-R09
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R09 | The minder SHALL execute every tick action addressed to a lane or a lead before its `due_by`,
    and SHALL NOT skip one because its own reading shows the lane working. | MIND-O02 | weak-evidence-as-work |
    herdr "working" alone read as work, MONITORING-DESIGN |'
- id: MIND-R10
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R10 | An order the minder sent that is unconfirmed at its deadline (`AckExpired`, or `Acted`
    with a focus other than its expected ticket) SHALL be re-sent or escalated in the tick the deadline passes.
    | MIND-O02 | queued-as-delivered | Queued relay orders treated as delivered, MONITORING-DESIGN |'
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
- id: MIND-R15
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R15 | Every order the minder sends to a lane SHALL name the exact ticket it expects the lane
    to take up. | MIND-O01 | vague-assignment | Vague "next ready" orders, MONITORING-DESIGN |'
- id: MIND-R16
  path: spec/roles/minder.md
  role: examined
  excerpt: '| MIND-R16 | Every escalation SHALL carry the ledger action id and the fleet status evidence it rests
    on. | MIND-O02 | minder-evidence-dismissed | Minder saw the idle lanes and was dismissed, 2026-11-23/24 |'
- id: skills/team-minder/SKILL.md
  path: skills/team-minder/SKILL.md
  role: examined
  excerpt: '---

    name: team-minder

    description: Run the fleet minder loop. Each tick reads `ix-board fleet status --json`, treats undetermined
    lanes as idle, pushes the next assigned ticket to idle lanes as a relay order, answers dialogs a standing order
    covers and logs each answer, routes every source defect, and escalates worker, lead, orchestrator on a fixed
    ladder. Use when invoked as /team-minder [scope] [interval], or when asked to keep a fleet''s or team''s lanes
    busy, find idle or blocked lanes, or run a minder loop.'
- id: skills/team-minder/references/standing-orders.md
  path: skills/team-minder/references/standing-orders.md
  role: examined
  excerpt: '# Standing orders for dialog answers


    This file is the allow-rule for dialog answers (SWM-226). The minder answers a `BLOCKED(dialog)` lane only when
    exactly one order below matches the dialog on screen (MIND-R11), and logs every answer with the order id (MIND-R12).
    Anything else is escalated to the lane''s lead with no input to the pane (MIND-R13, MIND-R14). When the `fleet
    tick` standing-order file lands, its orders replace this table and `answer_dialog` actions carry the order id.'
- id: skills/team-minder/references/status-request.md
  path: skills/team-minder/references/status-request.md
  role: examined
  excerpt: '# Answer a status-request


    Answering a `status-request` is an obligation of every relay lane, not a minder role rule; it sends nothing
    the tick did not ask for.'
- id: skills/team-retro/SKILL.md
  path: skills/team-retro/SKILL.md
  role: examined
  excerpt: '---

    name: team-retro

    description: Independently evaluate whether a team''s planner, code lead, coders, reviewers and minder are converging
    on their gate tickets, on a schedule, like a sprint retro. Takes metric snapshots with `ix-board retro`, compares
    them with the previous snapshot and a baseline, scores the role rubrics, names the repeating loops and messages
    the planner, code lead or user with owned actions. Use when invoked as /team-retro <team> [interval], or when
    asked to find out why a team is busy but not finishing, to run a retro, or to set up a recurring health check.'
- id: skills/team-retro/references/measures.md
  path: skills/team-retro/references/measures.md
  role: examined
  excerpt: '# Measures


    `ix-board retro snapshot` computes these and `ix-board retro delta` compares them. The definitions, sources
    and counting rules are the requirements FR-024 to FR-028 in the ix-board specification; this file says how to
    read them.'
- id: skills/index.json
  path: skills/index.json
  role: examined
  excerpt: "{\n  \"skills\": [\n    {"
- id: README.md
  path: README.md
  role: examined
  excerpt: '# dev-team


    [![Agent IX Plugins](https://github.com/agent-ix/agent-plugins/raw/refs/heads/main/assets/agent-ix-plugins.svg)](https://github.com/agent-ix/agent-plugins)'
```

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-013 | low | Every step-2 condition starts a ladder keyed by lane, class and ticket, but source defects, empty_fleet and the per-tick interim_mode defect have no lane: rung 1 (worker) and rung 2 (lead) have no recipient, and rung 3 re-sends to the orchestrator what step 2 already routes every tick. interim_mode never clears until SWM-255/256/258 ship, so its ladder never ends. State that lane-less defects are routed each tick by step 2 and climb no ladder. | skills/team-minder/SKILL.md:102 |
| FND-014 | low | SO-03's tracker condition asks for a recorded review 'for that head SHA', but reviewer and reviewer-dispositions markers carry no head SHA, and after a fix round the merge head differs from the reviewed head. As written the condition almost never matches, so SO-03 escalates instead of answering (safe, but it disables the order). Match on a review whose latest dispositions leave no still-open finding, or on the has-review label plus a PR head equal to the --match-head-commit SHA. | skills/team-minder/references/standing-orders.md:11 |

## Dispositions

Round 1, fix head efda94de5ed4eacf713a3b783163ca25fd1be7f8 (commit efda94d). Re-validated: `quire validate --module <spec-artifacts-process origin/main 80d25b6>` passes for spec/roles/minder.md, spec/rubrics/rubric-minder.md and reviews/swm-225-*.md.

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | - |
| FND-002 | fixed | - |
| FND-003 | fixed | - |
| FND-004 | fixed | - |
| FND-005 | fixed | - |
| FND-006 | fixed | - |
| FND-007 | fixed | - |
| FND-008 | fixed | - |
| FND-009 | fixed | - |
| FND-010 | fixed | - |
| FND-011 | fixed | - |
| FND-012 | fixed | - |
| FND-013 | fixed | - |
| FND-014 | fixed | - |

The FND-013 and FND-014 rows are round 2, fix head 8149fd60a3bda5b7f025c47e944b04619040a80a.
