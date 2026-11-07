# Minder rubric

Score each row 0, 1 or 2 and cite the evidence. This scores `team-minder`.

| Check | 2 | 1 | 0 | Evidence |
|---|---|---|---|---|
| Loop alive | A minder loop exists for the team and ticked in the last interval | Ticked late | No loop, or it stopped without the user's word | CronList, relay log |
| No unauthorised stop | The loop was cancelled only on the user's word | Paused with a recorded reason | Cancelled on a peer's claim | transcript |
| Idle recovery | Each idle agent was messaged once and resumed within one interval | Resumed after a second interval | Stayed idle after a message | `ix-board agents`, relay log |
| Delivery checked | Messages were confirmed queued and the agent resumed | Delivered, resumption not checked | A failed delivery read as success | relay log |
| Message hygiene | Only done, blocked, decision or handoff messages sent | Occasional status message | Repeated polls or progress messages | relay log |
| Scope | Reported only on its own team's agents | One out-of-scope message | Reported on other teams | relay log |

Read next: [strategies.md](strategies.md) entry "Verify delivery".
