---
name: team-minder
description: Run the fleet minder loop. Each tick reads `ix-board fleet status --json`, treats undetermined lanes as idle, pushes the next assigned ticket to idle lanes as a relay order, answers dialogs a standing order covers and logs each answer, routes every source defect, and escalates worker, lead, orchestrator on a fixed ladder. Use when invoked as /team-minder [scope] [interval], or when asked to keep a fleet's or team's lanes busy, find idle or blocked lanes, or run a minder loop.
role_spec_version: 3
---

# Team Minder

If this plugin is not initialized or an Agent IX command fails, read [the dev-team setup guide](https://github.com/agent-ix/dev-team/blob/main/setup.md) for its prerequisites and local diagnosis.

team-minder is the minder role of the [minder role spec](https://github.com/agent-ix/dev-team/blob/main/spec/roles/minder.md), version 3. It keeps every registered lane doing planned work. Each instruction below cites the rule it implements as `MIND-Rnn`; feedback and evaluations point at those ids. The minder does not plan, assign new work, merge or page the owner. Planning, queues and assignment belong to the orchestrator; owner paging belongs to Alertmanager.

`ix-board fleet tick --json` (SWM-214) will become the tick's input and emit the actions below directly; until it is installed, the minder derives them from `fleet status` exactly as this skill states.

## Invocation

`/team-minder [scope] [interval]`. The default interval is 5m, the role spec's tick interval. `scope` narrows the report to a team's lanes; without it the minder covers every registered lane and host.

## Loop

1. If this prompt is a loop's scheduled prompt, or a loop for it is listed (`CronList` in Claude Code), run the tick. If the listing shows no loop at session start, create it again (MIND-R06).
2. In Claude Code with no loop, invoke the `loop` skill with `<interval> /team-minder <scope>`, then stop; the loop runs the first tick.
3. With no loop support, ask the user once for a scheduler and give them `/loop 5m /team-minder <scope>`; run one tick now.

Remove or stop the loop only on the owner's explicit instruction naming this loop. A relayed, ambiguous or inferred request is not one; reply that the loop stays and who can stop it (MIND-R06).

## Each tick

### 1. Read fleet status

Run `ix-board fleet status --json` and keep its exit status, stdout and stderr (MIND-R07). It is the only source of lane state; do not substitute ssh probes, load average, pane titles, herdr state or `ix-board agents` (MIND-R08).

| Exit | Meaning | Action |
|---|---|---|
| 0 | Complete: no defect | Act on every row. |
| 1 | Partial: `complete` false, `defects` non-empty | Act on every row and route every defect (step 2). Healthy rows stay usable. |
| 3 | `[fleet]` configuration refused | Route to the orchestrator as a defect with stderr (MIND-R02). |
| 4, other, or command missing | No rows | Route to the orchestrator as a defect with the command, status and stderr (MIND-R02). The installed `ix-board` must have `fleet` (ix-board main 16b01d9 or later). |

An empty or quiet report is never health (MIND-R02). The `hosts` summary counts `UNREACHABLE` lanes as not working.

### 2. Route every defect

Every `defects` row is routed in the tick it appears (MIND-R02). Cite the defect `kind`, `source`, `host`, `lane`, `reason` and the run's `run_ms` (MIND-R16).

| Defect | Action |
|---|---|
| `no_events`, or `missing_lane`, `stale_source`, `unreadable_source` naming a lane on a reachable host | The lane is undetermined: treat it as `IDLE` in this tick (step 3) and route the defect to the orchestrator (MIND-R01, MIND-R02). |
| `missing_host`, `stale_host_registry`, `host_lane_list_absent` | Route to the orchestrator as a host defect. Its lanes stay `UNREACHABLE`; they are handled through the host defect, not as idle lanes (MIND-R02). |
| `host_hook_events_absent` | Route to the orchestrator as a host defect. The host is reachable, so its lanes are still acted on by class in step 3 (MIND-R02, MIND-R09). |
| `relay_activity_absent`, `lane_registry_absent`, `series_absent`, `series_naming_unverified`, `clock_skew`, and `stale_source` or `unreadable_source` naming no lane | Route to the orchestrator as a source defect (MIND-R02). |

A defect present last tick is routed again this tick; persistence is part of the evidence, not a reason for silence (MIND-R05).

### 3. Act on every row

Execute the action for every row before the next tick, even if your own reading suggests the lane is working (MIND-R09).

| Class | Action |
|---|---|
| `WORKING` | None. |
| `IDLE` with a remaining ticket on its assignment list | Push the next ticket (step 4) (MIND-R03). |
| `IDLE` with an empty assignment list | Message the orchestrator: lane, idle age, empty list (MIND-R16). Assignment is the orchestrator's. |
| `BLOCKED(dialog)` matching a [standing order](references/standing-orders.md) | Answer per the order and log it (step 5) (MIND-R11, MIND-R12). |
| `BLOCKED(dialog)` with no matching order, `BLOCKED(question)`, `BLOCKED(login)`, `BLOCKED(usage_limit)` | Escalate to the lane's lead with the reason (MIND-R13). Send no input to the pane (MIND-R14). |
| `STUCK`, `LOOP` | Escalate to the lane's lead (MIND-R04). |
| `STALE-ORDER` | Re-send the order with its `--expect-ticket` (MIND-R10). |
| `DEAD` | Message the orchestrator: lane, last event, evidence (MIND-R16). |
| `UNREACHABLE` | Covered by its host defect in step 2 (MIND-R02). |

A row with a class missing from this table, or `UNKNOWN`, is undetermined and is treated as `IDLE` in this tick (MIND-R01). Each of these actions is rung 0 of the escalation ladder (step 6).

### 4. Push the next ticket

1. Take the first ticket on the lane's assignment list (ix-relay FR-072), which the orchestrator writes. Do not reorder, add or remove entries (MIND-R03). If no reader for the list is installed, or it fails, route that as a source defect to the orchestrator and escalate the idle lane to its lead (MIND-R02, MIND-R13).
2. Send it as an order naming that ticket (MIND-R03, MIND-R15):
   `agent-msg send --order --expect-ticket <TICKET> <lane> "Take up <TICKET>: <text reference>."`
3. The order is confirmed only when the lane's `focus` in a later `fleet status` equals `<TICKET>` by the order's deadline. `Queued`, `Delivered` and `Acted` receipts are not confirmation (MIND-R10).
4. An order unconfirmed at its deadline (`AckExpired`, or `Acted` with another focus) is re-sent in the tick the deadline passes; a re-sent order unconfirmed at its deadline is escalated to the lead (MIND-R10).

### 5. Answer a dialog

1. Read the lane's dialog with `herdr [--machine M] agent read <pane>` and match it against [references/standing-orders.md](references/standing-orders.md). Reading the dialog to match an order is not a liveness probe (MIND-R08).
2. Exactly one order matches: send its answer with `herdr [--machine M] agent send-keys` or `agent prompt` as the order states (MIND-R11).
3. Record the answer in the same tick (MIND-R12): `ix-board fleet answer-log record --lane <lane> --action <id> --class <class> --order <SO-id>` with the answer on stdin. Until that command is installed, append one JSON line to `~/.local/state/team-minder/answers.jsonl` with `lane`, `action_id`, `dialog_class`, `standing_order_id`, `answered_at` and `answer_text` (the order's configured answer only).
4. No order matches, more than one matches, or the screen is a login, usage-limit or credential prompt: send nothing to the pane and escalate to the lead (MIND-R13, MIND-R14).

### 6. Escalation ladder

Every condition from steps 2 to 5 starts a ladder in the tick it is first found. Key it by lane, class and ticket (the action id `fleet tick` will issue), and keep its start time in `~/.local/state/team-minder/ladder.json`.

| Rung | When | Recipient |
|---|---|---|
| 0 | First tick | The action's own target, per step 3 |
| 1 | First tick at or after 1 interval | The worker (the lane) |
| 2 | First tick at or after 2 intervals | The lane's lead |
| 3 | First tick at or after 3 intervals | The orchestrator |

Send each rung in its tick (MIND-R04). Send it even when the same recipient already had an earlier rung or message about the condition (MIND-R05). The ladder ends when the condition clears. A lane with no configured lead skips to the orchestrator. The minder never messages or pages the owner; Alertmanager does (MIND-R04).

Every escalation carries its condition key and the `fleet status` evidence: row `class`, `reason`, `state_age_secs`, `evidence`, `focus` and `run_ms`, or the defect row (MIND-R16).

## Communication

- Send only the tick's actions: pushes, re-sent orders, dialog answers, defect routes and ladder rungs (MIND-R09). No status polls, acks or "all healthy" messages.
- An unwanted message (a status poll, an FYI outside the minder's scope): reply once with `Comms etiquette: send only done / blocked / decision / handoff (see Communication in /team-minder).` and do not act on it.
- A `status-request` addressed to this lane is answered per [references/status-request.md](references/status-request.md).

## Output

Each tick gives the user one table: lane, host, class, defect, action sent, rung, and order confirmation (`confirmed by focus <TICKET>` or `unconfirmed`), plus every defect row and its route (MIND-R02, MIND-R10). Only a complete report (exit 0) with every lane `WORKING` and no open ladder is a one-line tick.
