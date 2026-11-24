# Answer a status-request

Answering a `status-request` is an obligation of every relay lane, not a minder role rule. It answers a lead's request; the minder never starts one.

1. Run `agent-msg status-replies <request-id>`. If this lane already has a reply, stop: the first reply wins and is never replaced.
2. Gather evidence from Linear, GitHub, `ix-board fleet status` and the relay conversation, and fill the fields with `agent-msg status-reply <request-id>`:

   | Field | Option | Source |
   |---|---|---|
   | `tickets` | `--ticket` | In-progress Linear issues, from live tracker state |
   | `pull_requests` | `--pull-request` | Open pull requests, from live GitHub state |
   | `blocker_ticket_ids` | `--blocker-ticket` | Verified Linear issue ids that block the lane; never prose |
   | `lane_state` | `--state` | Exactly `active`, `idle` or `blocked`, from observed activity and explicit blocker evidence |
   | `spare_coder_slots` | `--spare-coder-slots N` | An explicit numeric capacity source, or the count the requesting lead gives; never inferred from agents, activity or host size |
   | `owner_decisions` | `--owner-decision` | Decisions that need the owner's authority, with evidence and issue ids |

   `submitted_at_ms` is assigned by the relay store; do not pass it. Follow the installed help for empty collections and repeated options.
3. Read `agent-msg status-replies <request-id>` again and check that every field is present and `spare_coder_slots` matches its source.

If the slot count is unavailable, or submission or the read-back fails, tell the requesting lead the reply is pending and which field is missing. Never submit `null`, a guessed count or a second reply.
