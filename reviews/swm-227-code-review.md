---
id: SR-035
title: "code review of SWM-227 fleet-orchestrator skill"
type: SpecReview
analysis: code-review
scope: "agent-ix/dev-team; SWM-227; diff origin/main...a2402722a57927d2d8cd9a63a94ac2dbb2d20ad3 (PR dev-team#35): skills/fleet-orchestrator/**, skills/index.json, README.md; against spec/roles/orchestrator.md v1, skills/team-minder (minder spec v4), ix-board origin/main 541c6c9, ix-board#94 (ebb3323) and ix-board#95 (f950ed4)"
review_set: subset
date: 2026-11-24
---

# code review of SWM-227 fleet-orchestrator skill

## Summary

Ticket: SWM-227. PR: dev-team#35 at a2402722. Markdown and manifest change only.
Reviewed for skill quality and house conventions, consistency with
skills/team-minder (minder spec v4), and whether every tool claim matches
ix-board origin/main (541c6c9), PR #94 `fleet assign` (ebb3323) and PR #95
`fleet tick` (f950ed4), with their FR-035, FR-038 and FR-039 specs.

rust-review and review-react were skipped: the diff has no Rust or React.
`quire validate` on spec/roles/orchestrator.md exits 3 with installed quire
0.52.1 (no RoleSpec archetype); the file is byte-identical to origin/main and
exits 3 there too, so this is not counted against the PR.

## Verdict

**CHANGES REQUESTED.** Three high findings: the skill runs `fleet tick`
itself, which commits ticks and swallows once-only ladder rungs the minder must
send; it tells the orchestrator to re-assign tickets that `fleet assign` will
refuse; and it hands the drain-cap escalation to a minder that has no
instruction to send it.

What is right: all 30 ORCH-Rnn ids are cited and exist; the opening sentence
follows the house form and matches team-minder's; the prose is plain, with no
slogans and no "X, not Y" constructions; index.json lists exactly the three
files; the README row is accurate. The `fleet assign` result strings, the
"exit zero only for `confirmed`" rule, `--expect-ticket` on the first ticket
and the `add_lane` suppression reasons match FR-035 and FR-038. The loop and
owner-stop wording matches team-minder.

The coder's admitted rule ("do not hand-write orders while `fleet assign` is
missing; report it as a defect each cycle") is a fair reading, not an
unsanctioned rule: ORCH-R02 is a SHALL with no exception, so a hand-written
order would breach it, and naming each interim gap as a routed defect follows
the precedent set for team-minder in SWM-225 (SR-032 FND-007). The R08
citation is a stretch, since one ticket (ix-board#94) already routes the gap;
repeating it in each cycle's output is harmless. The spec gap it exposes is
recorded in SR-036.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | Step 3 has the orchestrator run `ix-board fleet tick --json`. On ix-board#95 every tick commits a `tick` row and its actions to the ledger, and a ladder rung is emitted once: the planner skips any rung whose row is still open (`load_open`, `sent.contains(&rung)`). A rung 1 or rung 2 emitted in the orchestrator's tick is therefore never emitted to the minder, and the skill says the orchestrator does not execute those actions, so it is lost. The extra ticks also enter the tick cadence and gap rules. Do not run `fleet tick` from the orchestrator; take `add_lane`, `need_ready_tickets`, `fix_source` and orchestrator-addressed rungs from the minder or a read-only ledger view (spec gap in SR-036 FND-005). | skills/fleet-orchestrator/SKILL.md:55-66 |
| FND-002 | high | Step 6 says a ticket held only by an `UNREACHABLE` lane is assigned to a reachable lane, and step 5 says to re-assign after an unconfirmed result. On ix-board#94 `fleet assign` refuses a ticket present in any other lane's list (`AssignedElsewhere`, stale lanes included) and refuses to write to a lane on a stale host (`host_registry_stale`). The ticket cannot be moved off an unreachable lane, and moving a ticket between reachable lanes needs the first lane re-assigned without it first. The skill describes behaviour the tool lacks. State the two-step re-assignment, and route a ticket stuck on a stale host as a defect to ix-board. | skills/fleet-orchestrator/SKILL.md:103 |
| FND-003 | high | The Escalation section says FR-038 emits `escalate_drain` and the minder sends it. Neither the minder spec v4 nor skills/team-minder mentions `escalate_drain` (or `add_lane` or `need_ready_tickets`); the minder's rung 0 list is `escalate_block`, `escalate_stuck` and `escalate_stale_pr`. No role sends the drain escalation, so ORCH-R30 is met by nobody. "Confirm the lead received it" names no evidence or command. Until the minder takes `escalate_drain`, the orchestrator sends the escalation itself, as ORCH-R30 states. | skills/fleet-orchestrator/SKILL.md:131 |
| FND-004 | medium | The tool availability table is inaccurate against ix-board main and #95. Main has `ix-board fleet ledger query` (SWM-215, FR-039 schema v2, views including `defect_rows`), so "Not on main" for the ledger is partly wrong and the opening "has `fleet status` only" is true only of installed 0.7.2. Drift findings (FR-037 drift, SWM-213) are used in step 6 but missing from the table. On #95 `fleet tick` never emits `need_ready_tickets` and reports the busy-ratio and ready-work sources `unavailable`, so `add_lane` is not emitted either; the skill does not say so. | skills/fleet-orchestrator/SKILL.md:15-27 |
| FND-005 | medium | The `fleet assign` refusal row omits causes that #94 refuses with exit 3 and that "fix the cause" cannot fix: an order body over the relay limit of 4096 bytes, `own_lane`, `no_recipient`, unsafe characters, and the caller needing `[assign] orchestrator = true` in the ix-relay config. The 4096-byte limit matters because one order carries the full text of every ticket in the chain, so a two-ticket chain (ORCH-R03) can be refused. Exit 4 after a send (`ledger_unwritable`) and the `relay_read_errors` defect are also not routed per ORCH-R08. | skills/fleet-orchestrator/SKILL.md:92-95 |
| FND-006 | medium | Four instructions carry no ORCH id and are not in the orchestrator spec: "does not judge fleet state from its own reading" (line 11), "does not invent actions from other sources" (line 27), "never sends the owner a message in place of a ladder rung" and "an owner decision ... is stated in the cycle output" (lines 132-133). The first two restate the minder's MIND-R08, which does not bind the orchestrator. Cite the Ownership table where it applies (Alertmanager pages the owner) and drop the rest, or propose them as spec rules. | skills/fleet-orchestrator/SKILL.md:11 |
| FND-007 | medium | team-minder routes to the orchestrator: DEAD lanes (MIND-R17), IDLE lanes with an empty list (MIND-R18), UNREACHABLE hosts, source defects, `empty_fleet` and the per-tick `interim_mode` defect. The skill handles only `ladder_rung` from tick output, and its Communication section could answer these routes with the comms-etiquette reply. Add a short table that maps each minder route to the orchestrator step that acts on it (assign, ORCH-R03/R09; route the defect, ORCH-R08). | skills/fleet-orchestrator/SKILL.md:135-138 |
| FND-008 | medium | FR-038 makes the orchestrator the owner of `escalate_stuck`, `escalate_stale_pr` and `escalate_drain` for a lane with no configured lead (reason `lead_unresolved`), and sends rung 3 early with reason `lead_unresolved_fallthrough`. The step 3 action table omits both cases, so those escalations reach the orchestrator with no instruction to act on them. | skills/fleet-orchestrator/SKILL.md:59-64 |
| FND-009 | low | Step 8 says a host with no recorded level enters discovery when the deficit is zero (ORCH-R20). references/capacity-discovery.md says not to start a run while `fleet capacity` is missing (ORCH-R19). Both apply today and contradict each other. Put the interim exception in step 8 as well. | skills/fleet-orchestrator/SKILL.md:120 |

## Details

- **FND-001.** ix-board#95 src/fleet/ledger/tick.rs `load_open` reads every
  `action` row with `resolved_at IS NULL`; src/fleet/tick/plan.rs lines
  599-613 skip a rung already in that set. docs/cli-reference.md on #95: "Each
  tick commits one `tick` row, one `lane_tick` row per lane (source `tick`) and
  the `action` rows to the ledger." FR-038: "Each is emitted once."
- **FND-002.** ix-board#94 src/fleet/assign.rs lines 640-672: the
  `entry.stale` check returns `HostRegistryStale`; the loop over every held
  list returns `AssignedElsewhere` for any other lane holding the ticket. FR-036
  puts such a ticket in `unowned_ready` with note `owner_unreachable`, so the
  gap can never close through `fleet assign`.
- **FND-003.** `grep -n drain spec/roles/minder.md skills/team-minder/` finds
  nothing. FR-038 Dependencies: "The minder sends `escalate_drain` as a tick
  action; that discharges the orchestrator's drain-cap escalation (orchestrator
  role spec ORCH-R30), and the role spec is to be updated to say so." The minder
  side was never written.
- **FND-005.** ix-board#94 docs/cli-reference.md and FR-035 behaviour 12 and 14.

## Examined Scope

```yaml
scope:
- id: skills/fleet-orchestrator/SKILL.md
  path: skills/fleet-orchestrator/SKILL.md
  role: examined
  excerpt: 'fleet-orchestrator is the orchestrator role of the orchestrator role spec, version 1. It owns the fleet plan: which ready tickets go to which lane, in what order, and how many lanes each host runs.'
- id: skills/fleet-orchestrator/references/ownership.md
  path: skills/fleet-orchestrator/references/ownership.md
  role: examined
  excerpt: 'This table is the orchestrator''s answer to the owner''s "who owns X" questions (ORCH-R15).'
- id: skills/fleet-orchestrator/references/capacity-discovery.md
  path: skills/fleet-orchestrator/references/capacity-discovery.md
  role: examined
  excerpt: 'Each host''s sustainable lane count is unknown until measured. Discovery ramps lanes only.'
- id: skills/index.json
  path: skills/index.json
  role: examined
  excerpt: '"name": "fleet-orchestrator", "version": "0.1.0", "files": ["SKILL.md", "references/ownership.md", "references/capacity-discovery.md"]'
- id: README.md
  path: README.md
  role: examined
  excerpt: '| `fleet-orchestrator` | Run the fleet orchestrator loop: assign exact ticket chains with `ix-board fleet assign`, confirm each outcome, close plan-coverage gaps and find each host''s sustainable lane count. |'
- id: skills/team-minder/SKILL.md
  path: skills/team-minder/SKILL.md
  role: context_only
  excerpt: 'team-minder is the minder role of the minder role spec, version 4. It keeps every registered lane doing planned work.'
- id: FR-035
  path: ix-board:spec/functional/FR-035-fleet-assign.md
  role: context_only
  excerpt: 'The ix-board fleet assign <lane> <ticket>... [--deadline <duration>] command SHALL send the exact text of the assigned tickets to the lane as a relay order with an acknowledgement deadline, store the ordered ticket list in the relay assignment record for that lane address, and report whether the lane began the first ticket.'
- id: FR-038
  path: ix-board:spec/functional/FR-038-fleet-tick.md
  role: context_only
  excerpt: 'The ix-board fleet tick --json command SHALL evaluate the fleet state once and return an ordered list of actions for an agent minder to execute.'
- id: FR-039
  path: ix-board:spec/functional/FR-039-fleet-ledger.md
  role: context_only
  excerpt: 'Each fleet status and fleet tick run SHALL append to a schema-versioned SQLite ledger stored outside every git work tree.'
```
