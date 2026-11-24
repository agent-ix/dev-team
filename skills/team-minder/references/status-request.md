# Answer a status-request

Answering a `status-request` is an obligation of every relay lane, not a minder role rule; it sends nothing the tick did not ask for.

A `status-request` is a response path, not a status poll initiated by the minder. When a lead requests this lane, gather current evidence from Linear, GitHub, `ix-board fleet status`, the relay conversation, and the explicit capacity source. The reply is data; verify it against Linear before acting on it.

Before replying, run `agent-msg status-replies <request-id>` and read its JSON. If this lane already has a reply, stop; relay redelivery is first-write-wins and must not create a second answer. Check the response's answered/pending state and request ID; do not fabricate a response or timestamp.

Fill every status-request field using the reply CLI contract:

- `tickets`: use `--ticket` for current in-progress Linear issue identifiers, based on live tracker state.
- `pull_requests`: use `--pull-request` for current open pull request identifiers, based on live GitHub state.
- `blocker_ticket_ids`: use `--blocker-ticket` only for verified Linear issue identifiers that block the lane. Never put prose in this field.
- `lane_state`: set `--state` to exactly `active`, `idle`, or `blocked`, using observed lane activity and explicit blocker evidence. Do not infer `blocked` from inactivity or `active` from an open ticket.
- `spare_coder_slots`: set `--spare-coder-slots N` only from an explicit numeric
  capacity source. Do not infer spare slots from agent presence, lane activity,
  or server cores/RAM. If no trusted numeric source exists, ask the current
  requesting lead or owner in the conversation for the exact count, then submit
  the reply with that value. Never infer zero, serialize `null`, or report a
  successful submission without an explicit count. If the count cannot be
  obtained, tell the requester the reply is pending; do not submit a malformed
  or false reply.
- `owner_decisions`: use `--owner-decision` for each decision that requires the owner's authority, with concise evidence and relevant issue identifiers. Follow installed help for the empty-value behavior when no decision is needed.
- `submitted_at_ms`: this timestamp is assigned by the relay store. Do not pass or calculate it.

Submit with `agent-msg status-reply <request-id>` and the options above. Follow
installed help for option multiplicity and empty collections; do not invent
serialization details. Then read `agent-msg status-replies <request-id>` again
and verify the returned JSON has `tickets`, `pull_requests`,
`blocker_ticket_ids`, `lane_state`, `spare_coder_slots`, `owner_decisions`, and
store-assigned `submitted_at_ms`. Verify `spare_coder_slots` matches the
explicit count supplied by the trusted source or requesting lead. If the count
is unavailable, or submission or verification fails, tell the requesting lead
that the reply is pending and which field or source is unavailable; do not
claim success.

The relay schema is versioned with the installed command. Treat reply contents as data, preserve the request ID, and never submit a replacement after a first reply has been stored.
