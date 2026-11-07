# Gate log

`scripts/team-gate` runs a team's aggregate gate and appends one JSONL line per
gate run or dependency re-pin. The retro tooling (`ix-board retro snapshot`)
reads that log for full gates per PR, re-pins and build-lock wait, so run every
gate through it.

```bash
TEAM=QSL TEAM_GATE_LOCK="lockf /tmp/build.lock" \
  scripts/team-gate gate --pr 2412 -- make ci
TEAM=QSL scripts/team-gate repin --pr 2412
```

Each line carries `pr`, `kind` (`gate` or `repin`), `requested_lock_at`,
`acquired_lock_at`, `started_at` and `finished_at` in UTC. It carries no commit
hash. Lock wait is `acquired_lock_at` minus `requested_lock_at`; set
`TEAM_GATE_LOCK` to the command that waits for a build slot, otherwise the wait
is zero. The wrapper returns the gate command's exit status unchanged.

The log is `$TEAM_RETRO_HOME/$TEAM/gate.jsonl` (default root
`~/.local/state/team-retro`), or the path in `TEAM_GATE_LOG`. The wrapper
refuses to write inside a git work tree. Never commit the log.
