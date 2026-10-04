# Harness mapping: Claude Code vs Codex

Both harnesses can run this skill with nothing else installed. Use the row for
the harness you're actually running in.

## Claude Code

- Dispatch a subagent: the `Agent` tool. Pick a `subagent_type` for the role
  (coder, reviewer, spec author): `general-purpose` unless the org defines
  role agents. A `fork` inherits your full context instead of starting fresh.
- Run in background: subagents launched with the `Agent` tool already run in
  the background; you're notified when one finishes. No extra flag needed.
- Resume the same subagent: `SendMessage` to its agent ID or name. This is how
  a fix round reaches the original coder with its context intact.
- Halt a subagent: the `TaskStop` tool.
- Message another leader: `SendMessage` reaches sessions on the same machine,
  and sessions on another machine only through Remote Control on the same
  account. Separate accounts per machine means it is same-machine in
  practice; for a leader under a different account, fall through to the
  herdr step below.
- Skills load from: an installed plugin's `skills/` tree (added via
  `/plugin marketplace add` + `/plugin install`), or a project's own
  `.claude/skills/`.

## Codex

- Dispatch a subagent: run it detached, capturing both a session id and a
  report file:
  `codex exec -C <worktree> -s workspace-write --json -o <worktree>/.report.md "<brief>" > <log>.jsonl &`
  Read the session id from the first event in `<log>.jsonl`, and the
  subagent's final report from `<worktree>/.report.md`. Verified: `codex exec
  --help` (`-C`, `-s`, `--json`, `-o` are all present). Drop `--worktree` —
  the leader already creates the worktree in the per-ticket loop, so a second
  managed worktree is redundant. A push step needs network access, and
  whether `workspace-write` grants that depends on the org's sandbox config.
- Run in background: `codex exec` runs to completion in its own process; the
  trailing `&` above backs it with an ordinary OS background job. Codex has no
  separate background flag.
- Resume the same subagent: `codex exec resume <SESSION_ID> "<message>"`, run
  from inside that subagent's own worktree. `codex exec resume` has no `-C` or
  `-s`; pass any config override with `-c` instead. Verified: `codex exec
  resume --help` (no `-C`/`-s` in its option list). Never pass `--last` when
  more than one lane is running in parallel — it resumes whatever session the
  daemon considers most recent, not necessarily yours.
- Halt a subagent: kill its background process. `codex exec` has no separate
  halt command.
- List subagent sessions: `codex agents` browses all agent sessions on the
  shared local app-server daemon. Verified: `codex agents --help`.
- Review a PR: `codex exec review` runs Codex's own review pass against the
  current repository; this is what `/code-review` means on Codex. Verified:
  `codex exec review --help`.
- Message another leader: unverified. No cross-session send-message command
  was found in `codex --help` or its subcommands. Fall through to the herdr
  step below, then to the ticket step in SKILL.md's "Other leaders" order.
- Skills load from the installed `dev-team` plugin (`codex plugin add
  dev-team@agent-ix-dev-team`), not from the reviewed repository. Resolve
  the skill by name; do not assume a cache version or workstation path.

Unverified: `codex features list` shows a `multi_agent` feature flag as stable
and enabled, which suggests a richer multi-agent surface than `exec` alone, but
no documented command for it was found beyond `codex exec`, `codex exec
resume`, `codex exec review`, `codex queue`, and `codex agents`. Treat those
five as the confirmed mechanism; don't assume more.

## Cross-machine leader messaging (either harness)

When herdr is on PATH, use it to reach a leader on another machine, regardless
of which harness either leader runs in:

```
herdr --machine <machine> agent prompt <agent-name> "from <your-lead-name>: <message>" --wait --timeout <ms>
```

The machine flag is a global option, not a flag of `agent prompt`. Verified:
`herdr --help` (`herdr --machine <label-or-id> <command>`) and
`herdr agent prompt --help` (`Usage: herdr agent prompt <TARGET> <TEXT>
[OPTIONS]`). Saved machines come from `herdr machine list`.

herdr types the message into the receiver's chat as if typed by hand, so
always sign it with your lead name. `--wait --timeout <ms>` waits for the
target to reach idle, done or blocked (or pass `--until` for a specific
state) and fails on timeout. If the target agent is already blocked, herdr
rejects the submission up front with `agent_blocked`, before sending
anything — treat that as "not delivered", not as a stall to retry blindly.
When herdr is not on PATH, skip this step and fall through to the ticket step
in SKILL.md's "Other leaders" order.
