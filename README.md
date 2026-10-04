# dev-team

[![Agent IX Plugins](https://github.com/agent-ix/agent-plugins/raw/refs/heads/main/assets/agent-ix-plugins.svg)](https://github.com/agent-ix/agent-plugins)
[![Discord](https://img.shields.io/badge/Discord-Join%20us-5865F2?logo=discord&logoColor=white)](https://discord.gg/k8DVhuYBR2)

Team planning, leadership, coding and review roles, feature coordination, and program status skills.

## Setup

If this plugin is uninitialized or a command fails, follow the [plugin setup guide](setup.md) for its required CLIs, configuration, and local diagnosis.

## Community help

If the setup checks leave a reproducible Agent IX dev-team bug that blocks progress, [join the Agent IX Discord](https://discord.gg/k8DVhuYBR2). Community help is a last resort for Agent IX product bugs, not a help desk for local credentials, machine setup, third party tools, or unrelated projects. See [setup.md](setup.md#community-help) for what to include.

## Skills

| Skill | Action |
| --- | --- |
| `team-planner` | Turn an idea into a structured Linear plan with dependencies and ready tickets. |
| `team-leader` | Coordinate a team's planned work through coding, review, and delivery. |
| `coder` | Implement an assigned ticket in its worktree and open the PR. |
| `reviewer` | Run applicable review methods and record findings against a PR and ticket. |
| `feature-request` | Record a new capability request as a buildable Linear ticket. |
| `feature-feedback` | Report observed strengths, friction, and gaps after using a feature. |
| `feature-check` | Check delivered behavior against each ticket acceptance criterion. |
| `status-report` | Report program progress, blockers, and next actions from Linear evidence. |

`team-planner` and `status-report` use Linear and ix-board for structured project status and blockers. `reviewer` can invoke review methods from `dev-tools` and specification methods from Quoin when installed. `coder` can use `dev-tools:rust-style` for Rust work. Get companion plugins from the [Agent IX marketplace](https://github.com/agent-ix/agent-plugins) and install them as `ix-board@agent-ix`, `dev-tools@agent-ix`, or `quoin@agent-ix` when the corresponding methods are needed. The role skills report unavailable methods rather than inventing results.

The planner accepts a new idea as well as an existing focus. For a large system it establishes domain boundaries, architecture layers, specifications, tests, and blocker relations before dispatching executable tickets. Its current source workflow came from Agent IX; check your own tracker and governance before applying it elsewhere.

## Install

The repository is one plugin. The same `skills/` tree is used by all four hosts.

| Host | Install |
| --- | --- |
| Claude Code | `claude plugin marketplace add agent-ix/agent-plugins` then `claude plugin install dev-team@agent-ix` |
| Codex | `codex plugin marketplace add agent-ix/agent-plugins` then `codex plugin add dev-team@agent-ix` |
| GitHub Copilot CLI | `copilot plugin install agent-ix/dev-team` |
| OpenCode | Add `"https://raw.githubusercontent.com/agent-ix/dev-team/main/skills/"` to the `skills` array in your `opencode.jsonc`; the URL serves this repository's `skills/index.json` catalog. |

Claude uses `.claude-plugin/plugin.json`, Codex and Copilot use the root portable `plugin.json`, and OpenCode uses the remote skill catalog. The [Agent IX public marketplace](https://github.com/agent-ix/agent-plugins) pins reviewed versions for Claude and Codex. The `.codex-plugin/plugin.json` file supports older Codex plugin loaders. No host-specific copy of a skill is maintained.

## License

MIT. See [LICENSE](LICENSE). See [CONTENT_RIGHTS.md](CONTENT_RIGHTS.md) for source-content rules.
