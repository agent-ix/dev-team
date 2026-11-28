# Who owns X

This table is the orchestrator's answer to the owner's "who owns X" questions (ORCH-R15). Name the role and its lane address `server:workspace:tab` as registered in the relay. Read the address at answer time from the ix-board `[fleet_tick]` settings `orchestrator`, `minder` and `leads` (lane to lead address), and from the relay lane registry for every other lane, planner and host (ORCH-R15). An answer with a role and no address is incomplete (ORCH-R15).

| Thing | Owner |
|---|---|
| Fleet plan: ticket-to-lane assignment and queue order | orchestrator |
| Lane queues and queue depth | orchestrator |
| Work selection from the ready queue | orchestrator |
| Lanes per host, and lane capacity discovery | orchestrator |
| Build slots per host | build scheduler (ix-build, dev-team FR-009, FR-010) |
| Fleet probes and source defects (`fix_source`) | orchestrator, until routed by ticket to the owning repository |
| Executing tick actions, dialog answers, in-fleet ladder sends | minder |
| Paging the owner | Alertmanager |
| Ready tickets for a project (ready-buffer refill) | that project's planner |
| Landing an assigned ticket (spec, code, review, merge) | the lane's code lead |
| Evaluating orchestrator and minders | director |

Source: the Ownership section of the orchestrator role spec, version 6.
