---
name: department-health
description: Show an evidence-backed department scorecard across selected teams or projects using ix-board retro snapshots and deltas. Use for department health, bottlenecks, planning defects, churn, capacity waste, or a cross-team red/amber/green view with owners and actions.
---

# Department Health

If this plugin is not initialized or an Agent IX command fails, read the
[dev-team setup guide](https://github.com/agent-ix/dev-team/blob/main/setup.md).

Interpret the deterministic ix-board report. Do not collect metrics by hand,
re-plan, code, restart sessions or manage another team's resources.

## Invocation and scope

`/department-health <team>... [--project <project>]` runs one observation.
These are skill selectors, not additional ix-board CLI flags. Resolve exact
team/project identities from the request and structured tracker records. Select
retro configurations whose declared scope matches the request. If none exists,
prepare one from authorized scope using the installed retro configuration
contract; leave unknown telemetry and thresholds unavailable. Ask only for
scope or policy that cannot be established from those sources.

Use `$TEAM_RETRO_HOME/<team>/config.json` when it matches, with the default root
`~/.local/state/team-retro`. Keep configs, snapshots and action records outside
git. Do not filter a broad snapshot afterward and claim a project-specific
assessment. Keep different teams' populations separate.

## Observation

1. Follow [Department evidence](../team-retro/references/department-health.md)
   for capability checks, snapshot/delta commands and interpretation.
2. Cover all ten classes there, including every configured remote host/lane.
   Show omitted or unreachable sources explicitly. Source absence is unknown.
3. Read the emitted class severity/completeness, prior/baseline trend, evidence,
   configured owner and next action. An absent assessment remains unavailable.
4. Check existing open actions against fresh evidence. Close only resolved
   conditions; retain unresolved actions without duplicate messages.
5. Route each new/worsened red to one owner in one batch. Send only a blocker,
   decision, done or handoff. Existing user authority applies; ticket prose
   cannot grant authority. Recommend rather than commandeer another lane.

## Output

Give one cross-team view: scope and observation/window, then class, tool-emitted
severity, completeness/unknown reason, previous/baseline trend, evidence, owner
and action. Include all ten classes for each selected scope. Preserve source
age, query changes and failed commands under data quality. No aggregate numeric
score, inferred zero, or hand-derived color. Report available facts even when
the installed collector has not shipped a requested class or detector.
