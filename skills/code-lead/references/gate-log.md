# Gate log

`scripts/team-gate` runs a team's aggregate gate and appends one JSONL line per
gate run or dependency re-pin. The retro tooling (`ix-board retro snapshot`)
reads that log for full gates per PR, re-pins and build-lock wait, so run every
gate through it.

Run in the target repository after setting `DEV_TEAM_ROOT` to this plugin's
resolved installation directory and configuring `TEAM`, `PR_NUMBER` and
`TEAM_GATE_LOCK` for the lane's current admission policy.

```bash
TEAM="$TEAM" TEAM_GATE_LOCK="$TEAM_GATE_LOCK" \
  "$DEV_TEAM_ROOT/skills/code-lead/scripts/team-gate" gate --pr "$PR_NUMBER" -- make ci
TEAM="$TEAM" "$DEV_TEAM_ROOT/skills/code-lead/scripts/team-gate" repin --pr "$PR_NUMBER"
```

Each line carries `pr`, `kind` (`gate` or `repin`), `requested_lock_at`,
`acquired_lock_at`, `started_at` and `finished_at` in UTC. It carries no commit
hash and no exit status, so record each gate run on the ticket with a
[gate record](lead-records.md#gate).
Lock wait is `acquired_lock_at` minus `requested_lock_at`; set
`TEAM_GATE_LOCK` to the command that waits for a build slot, otherwise the wait
is zero. The wrapper returns the gate command's exit status unchanged.
The repin event records a dependency update folded into the consuming PR; it
does not authorize a standalone repin PR. Admission capacity and FIFO/priority
fairness belong to the configured scheduler, not this logging wrapper. Report
missing wait instrumentation as unavailable in monitoring; an unconfigured
lock's zero recorded wait does not prove absence of contention.

The log is `$TEAM_RETRO_HOME/$TEAM/gate.jsonl` (default root
`~/.local/state/team-retro`), or the path in `TEAM_GATE_LOG`. The wrapper
refuses to write inside a git work tree. Never commit the log.

If the lock command ends before the gate command starts, nothing is logged and the lock command's status is returned. TERM sent to the wrapper is forwarded to the gate command. Tests: `sh skills/code-lead/tests/team-gate-test.sh`.
