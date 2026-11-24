---
id: SR-036
title: "gap analysis of SWM-227 fleet-orchestrator skill against the orchestrator role spec"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/dev-team; SWM-227; diff origin/main...a2402722a57927d2d8cd9a63a94ac2dbb2d20ad3 (PR dev-team#35): skills/fleet-orchestrator/** traced against spec/roles/orchestrator.md v1 (ORCH-R01..R30, Ownership, Capacity discovery, Query sources and producers); ix-board FR-035..FR-041 on origin/main 541c6c9, #94 and #95"
review_set: subset
date: 2026-11-24
---

# gap analysis of SWM-227 fleet-orchestrator skill against the orchestrator role spec

## Summary

Ticket: SWM-227. PR: dev-team#35 at a2402722. The skill is the implementation
here; spec/roles/orchestrator.md v1 is the requirement. Each of the 30 rules
was traced to the skill text that carries it, and the spec was checked for gaps
the skill cannot close on its own. Plan completion: not assessed. `quoin
matrix` was not used: role-spec rules have no test rows, so the trace is
rule-to-instruction by hand. `quire validate` on the role spec exits 3 with
installed quire 0.52.1 (no RoleSpec archetype); origin/main gives the same exit,
so this is not counted against the PR.

## Verdict

**PASS for the trace, with spec amendments needed.** Every ORCH-R01..R30 is
cited and carried faithfully; no cited id is missing from the spec. The
findings below are gaps in the spec itself (four reported by the coder, four
found in review). The skill-side defects are in SR-035.

Faithful carriage, rule by rule: R01 (named head ticket, `--expect-ticket`),
R02 (`fleet assign` only), R03 (queue >= 2), R04 and R05 (only `confirmed`
counts; receipts are not confirmation), R06 (three plan-coverage lists closed
in the cycle; `unavailable` never read as empty), R07 (health words only next
to an exit-0 `complete: true` run), R08 (fix or route by ticket in the cycle),
R09 and R11 (no idle reachable lane; no-build work while builds pause), R10
(act on a rung or reject with newer evidence), R12 (scheduler evidence for a
thermal or memory reduction), R13 (drift corrected), R14 (deficit to planners),
R15 (role plus address), R16 to R29 in references/capacity-discovery.md with
the spec's numbers (8 steps, 2-hour window, 30-minute ramp, 50% knee, 5%
throttle, 6-hour cool-off, 2 runs a day, fewer-than-5 fallback), R30 cited.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | ORCH-R30 makes the orchestrator escalate a drain past the cap, but ix-board FR-038 emits `escalate_drain` to the lane's lead for the minder to send and says the role spec "is to be updated to say so". The minder spec v4 does not list `escalate_drain`, so neither role owns the send. Amend R30 to: an `escalate_drain` action SHALL be sent to the lane's lead in the tick it is emitted (a minder rule, added to the minder spec's rung 0 list), and the orchestrator SHALL act on a drain rung addressed to it under R10. | spec/roles/orchestrator.md:235 |
| FND-002 | medium | ORCH-R15 requires a lane address in every ownership answer, but the Ownership table names roles only and no source for the addresses. Amend the Ownership section to name where each role's address is read: the ix-board `[fleet_tick]` settings (`orchestrator`, `minder`, `leads`) and the relay lane registry for lanes. | spec/roles/orchestrator.md:220 |
| FND-003 | medium | No rule or producer row says where the orchestrator reads drift findings (R13) and the ready-buffer deficit (R14, R17, R20) before SWM-213 (FR-037 drift) and SWM-217 (FR-041 saturation, `need_ready_tickets`) land. The producers table has no SWM-213 or SWM-217 row. Add both producer rows, and state the interim: no drift source means R13 is `n.a.` and the missing source is a routed defect. | spec/roles/orchestrator.md:218 |
| FND-004 | medium | The ticket and the spec disagree. SWM-227 AC 1 says "confirm Acted", which R04 and R05 forbid. The coder reports a ticket claim that the orchestrator owns `escalate_*` targets; the spec gives it only `fix_source`, rung 3 (R10) and the drain cap. FR-038 does make the orchestrator the owner of `escalate_stuck`, `escalate_stale_pr` and `escalate_drain` for a lane with no configured lead (`lead_unresolved`), and sends rung 3 early (`lead_unresolved_fallthrough`); no ORCH rule covers that. Amend R10 to cover every action addressed to the orchestrator, and correct the ticket AC to "confirm by focus (R05)". | spec/roles/orchestrator.md:215 |
| FND-005 | high | ORCH-R27 (`add_lane`), R14 (`need_ready_tickets`) and R08 (`fix_source`) depend on tick actions, but the spec gives no path by which they reach the orchestrator. `fleet tick` commits a tick and emits each rung once (FR-038, ix-board#95), so the orchestrator cannot run it alongside the minder, and the minder spec does not route those three kinds. Amend the minder spec to route `add_lane`, `need_ready_tickets` and `fix_source` to the orchestrator as rung 0, or name a read-only ledger view of open orchestrator-addressed actions. | spec/roles/orchestrator.md:232 |
| FND-006 | medium | ORCH-R04 says an unconfirmed assignment is "re-assigned or escalated" but names no escalation recipient. The orchestrator is the ladder's last rung and never pages the owner, so the target is undefined. Name the lane's code lead. | spec/roles/orchestrator.md:209 |
| FND-007 | medium | The spec has no interim clause for missing producers. R02 forbids any order not sent with `fleet assign`, which is not installed, so R01, R03, R05 and R09 are all breached until ix-board#94 lands, and the lanes go idle (the failure class of the 2026-11-23/24 loss). R19 and R20 conflict the same way while the capacity history is missing. The skill's reading (send no hand-written order, report the gap) is correct under R02. Add an interim rule like the minder's `interim_mode`, which states what the orchestrator does and routes while each producer is missing. | spec/roles/orchestrator.md:207 |
| FND-008 | medium | R02 requires one `fleet assign` order with the full text of every ticket, and R03 requires two or more queued tickets. FR-035 on #94 refuses an order body over the relay limit of 4096 bytes and never splits an assignment. Two long tickets can make R02 and R03 unsatisfiable together. Amend R02 or FR-035, for example a body that carries the head ticket in full and the rest by identifier and title. | spec/roles/orchestrator.md:208 |

## Examined Scope

```yaml
scope:
- id: ORCH-R01
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'Every order to a lane SHALL name the exact ticket it expects, as the head of the lane''s ordered ticket chain.'
- id: ORCH-R02
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'Every assignment SHALL be sent with `ix-board fleet assign`, which carries the full ticket text, and SHALL NOT rely on the lane reading the tracker.'
- id: ORCH-R03
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'Every reachable lane SHALL hold at least 2 remaining assigned tickets while ready work exists.'
- id: ORCH-R04
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'An assignment whose `fleet assign` result is `acted_not_focused`, `ack_expired` or `timed_out` SHALL be treated as unconfirmed and re-assigned or escalated in the cycle the result is recorded.'
- id: ORCH-R05
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'Every assignment SHALL reach `confirmed`, the lane''s derived focus equal to the first assigned ticket, within the `fleet assign` acknowledgement deadline (default 5 minutes).'
- id: ORCH-R06
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'Every gap `fleet plan-coverage` reports (unowned ready ticket, short queue, stale assignment) SHALL be closed in the cycle it appears.'
- id: ORCH-R07
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'The orchestrator SHALL NOT state that hosts or lanes are in target, healthy or saturated without a `fleet status` run that exited zero with `complete: true`.'
- id: ORCH-R08
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'A failed probe or source defect SHALL be fixed, or routed to a named owner with a ticket, in the cycle it appears.'
- id: ORCH-R09
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'No reachable lane SHALL stay idle while ready work exists that the lane can take.'
- id: ORCH-R10
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'An in-fleet ladder rung addressed to the orchestrator SHALL be acted on, or rejected only by citing newer fleet status evidence that contradicts it.'
- id: ORCH-R11
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'While a host''s builds are paused or its sustainable build slots are zero, its lanes SHALL be kept on work that needs no build slot.'
- id: ORCH-R12
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'The orchestrator SHALL NOT lower a host''s lane count for a thermal or memory reason without scheduler evidence (an active pause, an admission block, a build abort, or memory headroom below reserve) at that time.'
- id: ORCH-R13
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'A drift finding (`not_assigned`, `not_in_plan`, `priority_inversion`) SHALL be corrected by re-assigning or re-ordering the lane in the cycle it appears.'
- id: ORCH-R14
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'A positive ready-buffer deficit SHALL be sent to each owning planner as a request for the stated number of ready tickets in the cycle it appears.'
- id: ORCH-R15
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'When the owner asks who owns a ticket, lane, host, defect or decision, the orchestrator SHALL answer with a named role and lane address.'
- id: ORCH-R16
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'Capacity discovery SHALL add one lane per step and hold each step for the measurement window.'
- id: ORCH-R17
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'A discovery step SHALL be judged only on a window in which the ready-buffer deficit was zero throughout, and an inconclusive window SHALL be repeated.'
- id: ORCH-R18
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'Capacity discovery SHALL stop at the first knee signal and step the host back one lane.'
- id: ORCH-R19
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'The orchestrator SHALL record each host''s found level, with the measurements it was found at, in the capacity history.'
- id: ORCH-R20
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'A host with no recorded level SHALL be put into discovery when the ready-buffer deficit is zero.'
- id: ORCH-R21
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'The orchestrator SHALL NOT run a host above its recorded level except during a discovery run of at most 8 steps.'
- id: ORCH-R22
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'A host throttled above 5% for an hour at its recorded level SHALL be stepped down one lane, and re-discovered when the daily discovery cap (ORCH-R24) allows.'
- id: ORCH-R23
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'After a step-down, the orchestrator SHALL NOT raise the host above the stepped-down level before the cool-off ends.'
- id: ORCH-R24
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'The orchestrator SHALL NOT start more than 2 discovery runs of one host per day, first runs and re-discoveries counted together.'
- id: ORCH-R25
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'A host whose memory headroom falls below the profile reserve, or whose scheduler aborts a build for a thermal limit, SHALL have one lane marked draining, with no new assignment to it, in the same cycle.'
- id: ORCH-R26
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'A draining lane SHALL NOT be removed before its current ticket reaches a commit or pull request, nor while it runs a build.'
- id: ORCH-R27
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'An `add_lane` action for a host below its recorded level with ready work SHALL be executed in the cycle it is emitted.'
- id: ORCH-R28
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'A discovery run with 2 inconclusive windows in a row SHALL end with reason `inconclusive_no_demand` and return the host to its last validly measured level.'
- id: ORCH-R29
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'A discovery run whose build slots were saturated for a whole valid window SHALL end with reason `build_slots_saturated` and record that level, without raising the host further.'
- id: ORCH-R30
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'A lane still draining after the drain cap (default 4 hours) SHALL be escalated to its code lead.'
- id: ORCH-Ownership
  path: spec/roles/orchestrator.md
  role: examined
  excerpt: 'The orchestrator answers the owner''s "who owns X" questions from this table, naming the role and its lane address (server:workspace:tab) as registered in the relay.'
- id: skills/fleet-orchestrator/SKILL.md
  path: skills/fleet-orchestrator/SKILL.md
  role: context_only
  excerpt: 'Each instruction below cites the rule it implements as ORCH-Rnn; evaluations and feedback point at those ids.'
```
