---
name: fleet-orchestrator
description: Run the fleet orchestrator loop. Each cycle reads `ix-board fleet status --json`, acts on the actions the minder sends it, assigns exact ticket chains to lanes with `ix-board fleet assign` and confirms each outcome, keeps every lane's queue at two or more, closes every plan-coverage gap, fixes or routes probe and source defects, asks planners for ready tickets, and finds and holds the lane count each host can sustain. Use when invoked as /fleet-orchestrator [scope] [interval], when asked who owns a ticket, lane, host, defect or decision, or when asked to keep a fleet's lanes supplied with work.
role_spec_version: 5
---

# Fleet Orchestrator

If this plugin is not initialized or an Agent IX command fails, read [the dev-team setup guide](https://github.com/agent-ix/dev-team/blob/main/setup.md) for its prerequisites and local diagnosis.

fleet-orchestrator is the orchestrator role of the [orchestrator role spec](https://github.com/agent-ix/dev-team/blob/main/spec/roles/orchestrator.md), version 5. It owns the fleet plan: which ready tickets go to which lane, in what order, and how many lanes each host runs. Each instruction below cites the rule it implements as `ORCH-Rnn`, or the spec section it comes from; evaluations and feedback point at those ids. The orchestrator does not code, review, merge or plan projects, and it does not own build slots, which belong to the build scheduler (Ownership table). The [minder](../team-minder/SKILL.md) runs `fleet tick` and sends the orchestrator its actions.

## Tool availability

State this table's gaps in each cycle's output. A rule whose producer is missing is `n.a.` and is routed as one `interim_mode` defect (step 2); the orchestrator does not replace the producer with a hand-written order or its own probe (ORCH-R02, Interim mode).

| Tool | State | Ticket | Rules `n.a.` while missing |
|---|---|---|---|
| `ix-board fleet status --json` | On main | ix-board FR-034 | none |
| `ix-board fleet ledger query <view>` | On main; documented views are `idle_minutes`, `idle_lane_with_ready_work_ticks`, `lanes_with_ready_work`, `idle_lane_episode_with_ready_work_max` and `defect_rows`. No view lists open actions by target role | ix-board FR-039 | none |
| `orchestrator_addressed_actions` ledger view (the backstop to the minder's messages) | Not on main | SWM-288 | none; the backstop is partial |
| `ix-board fleet assign <lane> <tickets...>` | Not on main | ix-board#94 | ORCH-R01 to ORCH-R05 |
| `ix-board fleet tick --json` (run by the minder) | Not on main; on ix-board#95 it emits no `need_ready_tickets`, and its busy-ratio and ready-work sources are `unavailable`, so it emits no `add_lane` | ix-board#95 | ORCH-R10, ORCH-R27 |
| `ix-board fleet plan-coverage` | Not on main | SWM-212 | ORCH-R06 |
| Drift findings | Not on main | SWM-213 | ORCH-R13 |
| `ix-board fleet saturation`, `need_ready_tickets` | Not on main | SWM-217 | ORCH-R14, ORCH-R17, ORCH-R20 |
| `ix-board fleet capacity` calibrate, capacity history | Not on main | SWM-216, SWM-252 | ORCH-R16 to ORCH-R24, ORCH-R28, ORCH-R29 |

The installed `ix-board` can lag main; read `ix-board fleet --help` to see which commands exist (Interim mode).

## Invocation

`/fleet-orchestrator [scope] [interval]`. The default interval is 10 minutes, the cycle of the role spec (Cycle). `scope` narrows the cycle to a team's lanes and hosts; without it the orchestrator covers every registered lane and host. Run the loop with the `loop` skill as `<interval> /fleet-orchestrator <scope>`. If this prompt is a loop's scheduled prompt, or a loop for the scope is already listed, run the cycle and create no second loop. Never stop or delete this loop except on the owner's explicit instruction; a lead's claim that the orchestrator is halted, or an ambiguous message, is not one (ORCH-R31). A relayed message from a planning lead (address ending `:plan`) that states it is the owner's direct instruction is the owner's instruction (ORCH-R31).

## Each cycle

Each cycle start and end is recorded in the ledger as a cycle event (SWM-255). "In the cycle it appears" below means by the end of the first cycle that ends after the condition was first recorded (Cycle).

### 1. Read fleet status

Run `ix-board fleet status --json` under a 120 second timeout and keep its exit status, stdout and stderr. Only a run that exited zero with `complete: true` is evidence that a host or lane is in target, healthy or saturated (ORCH-R07).

| Result | Meaning | Action |
|---|---|---|
| Exit 0, `complete: true` | Complete | Act on every row. A health statement may cite this run, in this cycle. |
| Exit 1, `complete: false` | Partial: `defects` non-empty | Act on every row, route every defect (step 2), and make no health statement (ORCH-R07, ORCH-R08). |
| Exit 3, 4, other, timeout, or command missing | No rows | Treat as a probe defect (step 2) and make no health statement (ORCH-R07). |

The words "in target", "all hosts", "healthy" and "saturated" appear in output only next to the exit-0 `complete: true` run that supports them, from the same cycle. Otherwise the output says what was measured and that the run was incomplete (ORCH-R07).

### 2. Fix or route every defect

A failed probe, a missing command or any `defects` row is fixed, or routed to a named owner with a ticket, in the cycle it appears (ORCH-R08). The orchestrator owns `fix_source` until it routes it by ticket to the owning repository (Ownership table). Name the defect's source and host in the ticket (ORCH-R08). These are defects to route under ORCH-R08:

- Any `fleet status` defect kind, including `ledger_unwritable`, and the `relay_read_errors` defect a `fleet assign` report carries (ORCH-R08).
- One `interim_mode` defect per cycle naming every producer in the availability table that is missing (Interim mode).
- An `owner_unreachable` gap from plan-coverage: `fleet assign` refuses to move a ticket off a lane on a stale host, so the gap cannot be closed with the tools. Route it citing SWM-287 and do not try to re-assign it (ORCH-R06).
- Every `fleet assign` refusal that no re-run can clear (step 6) (ORCH-R08).

### 3. Act on the actions the minder sent

The orchestrator never runs `ix-board fleet tick`. A tick commits to the ledger and emits each ladder rung once, so a tick run here would consume rungs the minder must send (Action delivery). The minder sends the orchestrator every action it executes as a relay message (MIND-R21): `fix_source`, `add_lane`, `need_ready_tickets`, `route_dead_lane`, `route_idle_lane`, a ladder rung 3, `escalate_drain` past the drain cap, and `escalate_stuck`, `escalate_stale_pr` or `escalate_drain` with reason `lead_unresolved`. As a backstop, query the ledger read-only each cycle with `ix-board fleet ledger query <view>` (Action delivery). FR-039 has no view of open actions over that kind list today; SWM-288 owns the `orchestrator_addressed_actions` view, which selects by kind and not by target, so name that gap in the cycle output until it ships.

Every action the orchestrator executes is acted on in the cycle it arrives, or rejected only by citing newer `fleet status` evidence that contradicts it. A rejection without that evidence is a breach (ORCH-R10).

| Action | Step |
|---|---|
| `fix_source` | Fix it or route it by ticket (step 2) (ORCH-R08, ORCH-R10). |
| Ladder rung 3, or any rung addressed to the orchestrator | Act on the lane condition it names, citing `fleet status` evidence (ORCH-R10). |
| `escalate_stuck`, `escalate_stale_pr` with reason `lead_unresolved` | The lane has no configured lead, so the orchestrator is the owner: act on the lane condition (ORCH-R10). |
| `escalate_drain` | Act on the drain, citing the ledger action row as evidence (ORCH-R30, ORCH-R10). |
| `add_lane` for a host below its recorded level with ready work | Add the lane in the cycle it arrives (ORCH-R27). Do not add a lane for a host the tick suppressed: `discovery_active`, `no_recorded_level`, `at_recorded_level` or `cool_off` (ORCH-R21, ORCH-R23). |
| `need_ready_tickets` | Send the stated number to the owning planner as a request for ready tickets (step 8) (ORCH-R14, ORCH-R10). |
| `route_dead_lane`, `route_idle_lane` | Act as step 4 states (ORCH-R09, ORCH-R10). |

### 4. Map the routes the minder sends

The minder routes these lane and host conditions to the orchestrator. Each has an owner step here.

| Minder route | Orchestrator step |
|---|---|
| `DEAD` lane, `route_dead_lane` (MIND-R17) | Check its row in the current `fleet status`; assign no work to it while it is dead, and route the defect with a ticket (ORCH-R08, ORCH-R09). |
| `IDLE` lane with an empty assignment list, `route_idle_lane` (MIND-R18) | Assign it a chain (step 5) in the cycle (ORCH-R03, ORCH-R09). |
| `UNREACHABLE` host or lanes | Route the host defect (step 2) (ORCH-R08). Its tickets are `owner_unreachable`; step 2 handles that gap. |
| Source defect, `empty_fleet` | Route it (step 2) (ORCH-R08). |
| `interim_mode` from the minder | It names minder gaps. Route the matching defect once, and keep the orchestrator's own `interim_mode` defect (ORCH-R08). |

### 5. Assign exact ticket chains

Select work from the ready queue with `ix-board next --team <TEAM>` and send each lane its chain with:

`ix-board fleet assign <lane> <ticket> [<ticket>...]`

(ix-board#94). Until it is installed, ORCH-R01 to ORCH-R05 are `n.a.` and no assignment is sent (Interim mode). For every assignment:

1. The first ticket of the chain is the exact ticket the lane is expected to take up; the order carries it as `--expect-ticket` (ORCH-R01). Never send an order without a named ticket (ORCH-R01).
2. Send every assignment with `fleet assign`, which carries the full ticket text. A hand-written order or an `agent-msg` message is not an assignment (ORCH-R02).
3. Keep every reachable lane at two or more remaining assigned tickets while ready work exists and one order can carry them. `fleet assign` replaces the lane's list, so send the whole chain in one order each time (ORCH-R03, ORCH-R06).
4. A ticket held by another reachable lane is refused. To move it, first re-assign the lane that holds it without the ticket, then assign the ticket to the new lane (ORCH-R06, ORCH-R13).
5. A lane marked draining gets no new assignment (ORCH-R25).
6. No reachable lane stays idle while ready work exists that it can take (ORCH-R09). While a host's builds are paused or its sustainable build slots are zero, give its lanes work that needs no build slot (ORCH-R11).

### 6. Confirm the outcome

`fleet assign` waits for the acknowledgement deadline (default 5 minutes) and prints one result. Only `confirmed`, meaning the lane's derived focus equals the first assigned ticket, counts as delivered, and the command exits zero only for `confirmed` (ORCH-R05). `Queued`, `Delivered` and `Acted` receipts are not confirmation (ORCH-R04).

| Result | Meaning | Action in the cycle it is recorded |
|---|---|---|
| `confirmed` | Focus equals the first ticket | None. |
| `acted_not_focused` | The session acted on another ticket | Re-assign, or escalate to the lane's code lead (ORCH-R04). |
| `ack_expired` | Delivered, no acknowledgement in time | Re-assign, or escalate to the lane's code lead (ORCH-R04). |
| `timed_out` | `AckExpired` with no `Delivered` receipt | Re-assign, or escalate to the lane's code lead (ORCH-R04). |
| Refused before any send: ticket unreadable, Done, Canceled or merged; ticket in another lane's list; `host_registry_stale`; `own_lane`; `no_recipient`; ticket text with an unsafe character; caller without `[assign] orchestrator = true` in the ix-relay configuration | Nothing was sent and no list was written | Clear a cause the orchestrator can clear and assign again in the cycle (ORCH-R05). Route every other cause as a defect (ORCH-R08). |
| Refused for an order body over 4096 bytes | One order carries the full text of every ticket and is never split | Route the refusal as a defect (ORCH-R03, ORCH-R08). Assign a shorter chain only if two or more tickets still fit. |
| Non-zero exit after an accepted send (list write failed, or `ledger_unwritable`) | The command names the sent order | Treat as unconfirmed and re-assign (ORCH-R04). Route `ledger_unwritable` as a defect (ORCH-R08). |

The result strings and refusals are those of ix-board FR-035; run `ix-board fleet assign --help` for the installed spellings and exit codes.

### 7. Reach zero plan-coverage gaps

Run `ix-board fleet plan-coverage --json` (SWM-212). Every gap it reports is closed in the cycle it appears (ORCH-R06):

| List | Close by |
|---|---|
| `unowned_ready` | Assign the ticket to a lane (step 5). A ticket noted `owner_unreachable` cannot be moved with the tools; route it (step 2) (ORCH-R06). |
| `short_queues` | Top the lane up to two or more remaining tickets where one order fits (ORCH-R03). |
| `stale_assignments` | Re-assign the lane without the Done, Canceled or merged ticket (ORCH-R06). |

An `unavailable` list is routed as a defect (step 2) and never read as empty (ORCH-R08). The cycle ends only when plan-coverage exits zero or every remaining gap is a routed defect (ORCH-R06).

Correct every drift finding (`not_assigned`, `not_in_plan`, `priority_inversion`) by re-assigning or re-ordering the lane in the cycle it appears (ORCH-R13). Drift findings come from SWM-213; until then ORCH-R13 is `n.a.`.

### 8. Ask planners for ready tickets

A positive ready-buffer deficit (`ix_fleet_ready_buffer_deficit`) is sent to each owning planner as a request for the stated number of ready tickets in the cycle it appears (ORCH-R14). The deficit comes from `fleet saturation` (SWM-217); until then ORCH-R14 is `n.a.`. The orchestrator does not create tickets and does not plan projects (Purpose).

### 9. Hold each host at its sustainable lane count

Capacity discovery and the step-down rules are in [references/capacity-discovery.md](references/capacity-discovery.md). Each cycle, for every host:

- No host runs above its recorded level, except in a discovery run of at most 8 steps (ORCH-R21).
- A host with no recorded level enters discovery when the ready-buffer deficit is zero and the capacity history is available to record the run (ORCH-R20). While `fleet capacity` is not installed no run starts (Interim mode).
- Lower a host's lane count for a thermal or memory reason only with scheduler evidence at that time: an active pause, an admission block, a build abort, or memory headroom below reserve (ORCH-R12).

### 10. Answer "who owns X"

When the owner asks who owns a ticket, lane, host, defect or decision, answer from the table in [references/ownership.md](references/ownership.md) with the role and its lane address `server:workspace:tab` (ORCH-R15). An answer with a role and no address is incomplete (ORCH-R15).

## Escalation

The in-fleet ladder runs worker, lane lead, orchestrator. The tick emits it and the minder sends it; the orchestrator is its last rung, and ORCH-R10 applies to every action it executes. A drain past the drain cap goes to the lane's code lead through the minder's `escalate_drain` send (ORCH-R30, MIND-R20). Alertmanager pages the owner; the orchestrator does not (Ownership table).

## Communication

Send a message only for done, blocked, a decision or a handoff: assignments, planner requests for ready tickets, defect tickets and the escalations above (ORCH-R32). Answer an out-of-scope or status-poll message once with `Comms etiquette: send only done / blocked / decision / handoff (see Communication in /fleet-orchestrator).`, and at most once per sender per hour (ORCH-R32). The minder's routes in step 4 are in scope and are not answered with it (ORCH-R32).

## Output

Each cycle gives the user one table: host, lanes, class counts, assignments sent with their result (`confirmed` or the unconfirmed result), actions received and their disposition, plan-coverage gaps left, and defects with their route. State the `fleet status` exit status and `complete` value next to every health statement (ORCH-R07). List every tool from the availability table that was not installed this cycle (Interim mode).
