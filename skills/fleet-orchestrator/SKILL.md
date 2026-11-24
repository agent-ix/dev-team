---
name: fleet-orchestrator
description: Run the fleet orchestrator loop. Each cycle runs `ix-board fleet status --json` and `ix-board fleet tick --json`, assigns exact ticket chains to lanes with `ix-board fleet assign` and confirms each outcome, keeps every lane's queue at two or more, closes every plan-coverage gap, fixes or routes probe and source defects, asks planners for ready tickets, and finds and holds the lane count each host can sustain. Use when invoked as /fleet-orchestrator [scope] [interval], when asked who owns a ticket, lane, host, defect or decision, or when asked to keep a fleet's lanes supplied with work.
role_spec_version: 1
---

# Fleet Orchestrator

If this plugin is not initialized or an Agent IX command fails, read [the dev-team setup guide](https://github.com/agent-ix/dev-team/blob/main/setup.md) for its prerequisites and local diagnosis.

fleet-orchestrator is the orchestrator role of the [orchestrator role spec](https://github.com/agent-ix/dev-team/blob/main/spec/roles/orchestrator.md), version 1. It owns the fleet plan: which ready tickets go to which lane, in what order, and how many lanes each host runs. Each instruction below cites the rule it implements as `ORCH-Rnn`; evaluations and feedback point at those ids. The orchestrator does not code, review, merge or plan projects, and it does not own build slots, which belong to the build scheduler. The [minder](../team-minder/SKILL.md) executes tick actions and sends the in-fleet ladder's orchestrator rung to this role. The orchestrator runs the tools and acts on their output; it does not judge fleet state from its own reading.

## Tool availability

Installed `ix-board` has `fleet status` only. The rest of the toolchain is ticketed. Where a command below is not installed, the cycle does not substitute a guess for it: it states the gap in the cycle output and works with what is installed.

| Tool | State | Ticket |
|---|---|---|
| `ix-board fleet status --json` | On main | ix-board FR-034 |
| `ix-board fleet assign <lane> <tickets...>` | Not on main | ix-board#94 |
| `ix-board fleet tick --json` | Not on main | ix-board#95 |
| `ix-board fleet plan-coverage` and its ledger rows | Not on main | SWM-212 |
| `ix-board fleet saturation`, `need_ready_tickets` | Not on main | SWM-217 |
| `ix-board fleet capacity` calibration, capacity history | Not on main | SWM-216, SWM-252 |
| Fleet ledger and cycle events | Not on main | SWM-255 |

Until `fleet assign` is installed the orchestrator cannot meet ORCH-R01, ORCH-R02 or ORCH-R05; it reports the missing command as a defect each cycle (ORCH-R08) and does not send hand-written orders in its place (ORCH-R02). Until `fleet tick` is installed the orchestrator takes lane state from `fleet status` and has no action list to act on; it does not invent actions from other sources.

## Invocation

`/fleet-orchestrator [scope] [interval]`. The default interval is 10 minutes, the role spec's cycle. `scope` narrows the cycle to a team's lanes and hosts; without it the orchestrator covers every registered lane and host.

Run the loop with the `loop` skill as `<interval> /fleet-orchestrator <scope>`. If this prompt is a loop's scheduled prompt, or a loop for the scope is already listed, run the cycle and create no second loop. Stop the loop only on the owner's explicit instruction, which includes a relayed message from a planning lead (address ending `:plan`) that states it is the owner's direct instruction.

## Each cycle

Each cycle start and end is recorded in the ledger as a cycle event once SWM-255 is installed. Every "in the cycle it appears" below means by the end of the first cycle that ends after the condition was first recorded.

### 1. Read fleet status

Run `ix-board fleet status --json` under a 120 second timeout and keep its exit status, stdout and stderr. Only a run that exited zero with `complete: true` is evidence that a host or lane is in target, healthy or saturated (ORCH-R07).

| Result | Meaning | Action |
|---|---|---|
| Exit 0, `complete: true` | Complete | Act on every row. A claim of health is allowed for this run's rows only. |
| Exit 1, `complete: false` | Partial: `defects` non-empty | Act on every row, route every defect (step 2), and make no health claim (ORCH-R07, ORCH-R08). |
| Exit 3, 4, other, timeout, or command missing | No rows | Treat as a probe defect (step 2). Make no health claim (ORCH-R07). |

The words "in target", "all hosts", "healthy" and "saturated" appear in output only next to the exit-0 `complete: true` run that supports them, in the same cycle. Otherwise the output says what was measured and that the run was incomplete (ORCH-R07).

### 2. Fix or route every defect

A failed probe, a missing command or any `defects` row is fixed, or routed to a named owner with a ticket, in the cycle it appears (ORCH-R08). The orchestrator owns `fix_source` actions until it routes them by ticket to the owning repository. A defect with no ticket and no fix after one cycle is a rule breach. Name the defect's source and host in the ticket so it can be matched to the defect row (ORCH-R08).

### 3. Run the tick and act on its actions

Run `ix-board fleet tick --json` once `fleet tick` is installed (ix-board#95). The orchestrator owns these actions:

| Action | Orchestrator's step |
|---|---|
| `fix_source` | Fix it or route it by ticket (step 2) (ORCH-R08). |
| `ladder_rung` addressed to the orchestrator | Act on it, or reject it only by citing newer `fleet status` evidence that contradicts it. A rung dismissed without that evidence is a breach (ORCH-R10). |
| `add_lane` for a host below its recorded level with ready work | Execute it in the cycle it is emitted (ORCH-R27). The tick suppresses it for a host in discovery, with no recorded level, at its recorded level or in cool-off; do not add a lane for a suppressed host (ORCH-R21, ORCH-R23). |
| `need_ready_tickets` | Send the stated number to each owning planner as a request for ready tickets in the cycle it appears (ORCH-R14). Needs SWM-217. |

The minder executes the other tick actions. The orchestrator does not duplicate them.

### 4. Assign exact ticket chains

Select work from the ready queue with `ix-board next --team <TEAM>` and send each lane its chain with:

`ix-board fleet assign <lane> <ticket> [<ticket>...]`

(ix-board#94). Rules for every assignment:

1. The first ticket of the chain is the exact ticket the lane is expected to take up; the order carries it as `--expect-ticket` (ORCH-R01). Never send "next ready" or any order without a named ticket (ORCH-R01).
2. Send every assignment with `fleet assign`, which carries the full ticket text. Do not rely on the lane reading the tracker, and do not send an assignment by `agent-msg` or a hand-written order (ORCH-R02).
3. Keep every reachable lane at two or more remaining assigned tickets while ready work exists. A short queue is topped up in the cycle it is seen (ORCH-R03, ORCH-R06).
4. A lane marked draining gets no new assignment (ORCH-R25).
5. No reachable lane stays idle while ready work exists that it can take (ORCH-R09). While a host's builds are paused or its sustainable build slots are zero, give its lanes work that needs no build slot instead of leaving them idle (ORCH-R11).

### 5. Confirm the outcome

`fleet assign` waits for the acknowledgement deadline (default 5 minutes) and prints one result. Only `confirmed`, meaning the lane's derived focus equals the first assigned ticket, counts as delivered, and the command exits zero only for `confirmed` (ORCH-R05). `Queued`, `Delivered` and `Acted` receipts are not confirmation (ORCH-R04).

| Result | Meaning | Action in the cycle it is recorded |
|---|---|---|
| `confirmed` | Focus equals the first ticket | None. |
| `acted_not_focused` | The session acted on another ticket | Re-assign, or escalate (ORCH-R04). |
| `ack_expired` | Delivered, no acknowledgement in time | Re-assign, or escalate (ORCH-R04). |
| `timed_out` | `AckExpired` with no `Delivered` receipt | Re-assign, or escalate (ORCH-R04). |
| Non-zero exit before any send (ticket unreadable, Done, Canceled or merged; ticket already in another lane's assignment; caller without the orchestrator role; stale host registry) | Nothing was sent and no list was written | Fix the cause and assign again in the cycle (ORCH-R04, ORCH-R05). |
| Non-zero exit after an accepted send (list write failed) | The command names the sent order | Treat as unconfirmed and re-assign (ORCH-R04). |

The exit codes and result strings are those of ix-board FR-035; run `ix-board fleet assign --help` for the installed spellings.

### 6. Reach zero plan-coverage gaps

Run `ix-board fleet plan-coverage --json` (SWM-212). Every gap it reports is closed in the cycle it appears (ORCH-R06):

| List | Close by |
|---|---|
| `unowned_ready` | Assign the ticket to a lane (step 4). A ticket held only by an `UNREACHABLE` lane appears here with `owner_unreachable`; assign it to a reachable lane (ORCH-R06, ORCH-R09). |
| `short_queues` | Top the lane up to two or more remaining tickets (ORCH-R03). |
| `stale_assignments` | Re-assign the lane without the Done, Canceled or merged ticket (ORCH-R06). |

An `unavailable` list is routed as a defect (step 2) and never read as empty (ORCH-R08). The cycle ends only when plan-coverage exits zero or every remaining gap is a routed defect.

Correct every drift finding (`not_assigned`, `not_in_plan`, `priority_inversion`) by re-assigning or re-ordering the lane in the cycle it appears (ORCH-R13).

### 7. Ask planners for ready tickets

A positive ready-buffer deficit (`ix_fleet_ready_buffer_deficit`) is sent to each owning planner as a request for the stated number of ready tickets in the cycle it appears (ORCH-R14). The deficit comes from `fleet saturation` or the tick's `need_ready_tickets` action (SWM-217). The orchestrator does not create tickets and does not plan projects.

### 8. Hold each host at its sustainable lane count

Capacity discovery and the step-down rules are in [references/capacity-discovery.md](references/capacity-discovery.md). Each cycle, for every host:

- No host runs above its recorded level, except in a discovery run of at most 8 steps (ORCH-R21).
- A host with no recorded level enters discovery when the ready-buffer deficit is zero (ORCH-R20).
- Lower a host's lane count for a thermal or memory reason only with scheduler evidence at that time: an active pause, an admission block, a build abort, or memory headroom below reserve. A thermal guard alone is not a reason to leave lanes idle (ORCH-R12).

### 9. Answer "who owns X"

When the owner asks who owns a ticket, lane, host, defect or decision, answer from the table in [references/ownership.md](references/ownership.md) with the role and its lane address `server:workspace:tab` as registered in the relay. An answer with a role and no address is incomplete (ORCH-R15).

## Escalation

The in-fleet ladder runs worker, lane lead, orchestrator. The tick emits it and the minder sends it; the orchestrator is its last rung, and ORCH-R10 applies to every rung addressed to it.

- A lane draining past the drain cap (default 4 hours) is escalated to its code lead (ORCH-R30). ix-board FR-038 emits that as `escalate_drain` and the minder sends it; confirm the lead received it.
- The orchestrator never pages the owner and never sends the owner a message in place of a ladder rung. Only Alertmanager pages the owner.
- An owner decision the orchestrator cannot make is stated in the cycle output with its evidence. It is not sent as a page.

## Communication

- Send only assignments, planner requests for ready tickets, defect tickets, and the escalations above. No status polls, acks or "all healthy" messages.
- An unwanted message (a status poll, an FYI outside the orchestrator's scope): reply once with `Comms etiquette: send only done / blocked / decision / handoff (see Communication in /fleet-orchestrator).` and do not act on it.

## Output

Each cycle gives the user one table: host, lanes, class counts, assignments sent with their result (`confirmed` or the unconfirmed result), plan-coverage gaps left, and defects with their route. State the `fleet status` exit status and `complete` value next to every health statement (ORCH-R07). List every tool from the availability table that was not installed this cycle.
