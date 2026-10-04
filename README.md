# dev-team

[![Agent IX Plugins](https://github.com/agent-ix/agent-plugins/raw/refs/heads/main/assets/agent-ix-plugins.svg)](https://github.com/agent-ix/agent-plugins)

Team planning, leadership, coding and review roles, feature coordination, and program status skills.

## Skills

- `team-planner`, `team-leader`, `coder`, `reviewer`
- `feature-request`, `feature-feedback`, `feature-check`
- `status-report`

`team-planner` and `status-report` use Linear and ix-board for structured project status and blockers. `reviewer` can invoke review methods from `dev-tools` and specification methods from Quoin when installed. `coder` can use `dev-tools:rust-style` for Rust work. Install those plugins when the corresponding methods are needed. The role skills report unavailable methods rather than inventing results.

The planner accepts a new idea as well as an existing focus. For a large system it establishes domain boundaries, architecture layers, specifications, tests, and blocker relations before dispatching executable tickets. Its current source workflow came from Agent IX; check your own tracker and governance before applying it elsewhere.

## Install

The repository is one plugin. The same `skills/` tree is used by all four hosts.

| Host | Install |
| --- | --- |
| Claude Code | `claude plugin marketplace add agent-ix/agent-plugins` then `claude plugin install dev-team@agent-ix-public` |
| Codex | `codex plugin marketplace add agent-ix/agent-plugins` then `codex plugin add dev-team@agent-ix-public` |
| GitHub Copilot CLI | `copilot plugin install agent-ix/dev-team` |
| OpenCode | Add `"https://raw.githubusercontent.com/agent-ix/dev-team/main/skills/"` to the `skills` array in your `opencode.jsonc`; the URL serves this repository's `skills/index.json` catalog. |

Claude uses `.claude-plugin/plugin.json`, Codex and Copilot use the root portable `plugin.json`, and OpenCode uses the remote skill catalog. The [Agent IX public marketplace](https://github.com/agent-ix/agent-plugins) pins reviewed versions for Claude and Codex. The `.codex-plugin/plugin.json` file supports older Codex plugin loaders. No host-specific copy of a skill is maintained.

## License

MIT. See [LICENSE](LICENSE). See [CONTENT_RIGHTS.md](CONTENT_RIGHTS.md) for source-content rules.
