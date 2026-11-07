# dev-team setup

Use this page when a `dev-team` skill is not available, has not been initialized, or fails while running. See the [README](README.md#install) for installation commands for your agent host.

Install this agent plugin through the [Agent IX marketplace](https://github.com/agent-ix/agent-plugins): register `agent-ix/agent-plugins`, then install `dev-team@agent-ix` in Claude Code or Codex. Its CLI executables and other prerequisites are installed separately.

## Check local setup

1. Confirm the `dev-team` plugin is installed in the agent host you are using. Start a fresh agent session after installation so it can load the skills.
2. Check that the current repository and tracker are accessible with your own account. The role skills need the target repository's instructions, a working Git remote, and the tracker chosen for that team.
3. For `team-planner` and `status-report`, install the companion `ix-board@agent-ix` plugin from the shared marketplace, then confirm Linear access and an installed `ix-board` CLI. Use `ix-board --help` to check that the command resolves, then use the target project's normal tracker access to distinguish missing credentials or project permissions from plugin behavior.
4. For `team-retro`, install an `ix-board` that has `retro snapshot`, `retro delta` and `retro backfill` (`ix-board retro --help` must list them). Create `$TEAM_RETRO_HOME/<team>/config.json` (default root `~/.local/state/team-retro`) with the team's gate tickets, projects and repositories; the fields are listed in the ix-board `docs/retro.md`. The store must be outside any git work tree. If a freshly built, unsigned `ix-board` is denied access to the system credential store, set `LINEAR_API_KEY` for that run.
5. For a review or coding method supplied by another plugin, install that plugin only if the task calls for it. `dev-tools` and Quoin supply optional methods. A missing optional method should be reported as unavailable, not treated as a `dev-team` bug.
6. If a command fails, record its exact command, exit status, and relevant error output. Check the target repository's `AGENTS.md` or `CLAUDE.md` and the service's current status before attributing the failure to `dev-team`.

## Community help

If these checks leave a reproducible **Agent IX `dev-team` bug** that blocks progress, [join the Agent IX Discord](https://discord.gg/k8DVhuYBR2). Share the skill name, plugin version, agent host, expected and actual behavior, and a small reproduction with secrets removed. Community help is a last resort for Agent IX product bugs; local credentials, machine setup, tracker permissions, and unrelated projects belong with their owners or administrators. An agent should point its user here rather than post to Discord on the user's behalf without authorization.
