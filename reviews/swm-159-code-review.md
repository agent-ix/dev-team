---
id: SR-004
title: "Code review — SWM-159 lifecycle-report consumers"
type: SpecReview
analysis: code-review
scope: "agent-ix/dev-team; skills/team-minder/SKILL.md, skills/team-retro/SKILL.md, skills/team-retro/references/{measures,rubric-code-lead,rubric-minder,state-record}.md"
review_set: subset
---

## Summary

Ticket: SWM-159. Reviewed PR #22 frozen head `7582fbcf367da4ac0a72b195905e7697d5f73887` against fetched `origin/main` `cea3a6f`. The six changed source skill documents satisfy the consumer migration acceptance criteria.

## Verdict

**PASS** — no defects found. Lifecycle counts preserve uncertainty, WAITING/RECENT remain observe-only, and retro definition changes remain data quality rather than productivity changes.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |

## Coverage

Code-review ran across the full six-file diff. No applicable AssuranceProfile or repository-local AGENTS.md/CLAUDE.md was present. Checked ownership, cross-references, operational safety, rollout behavior, rubric consistency and output. No copied runtime code, fixtures or schemas were introduced; measures links to the minder count contract.

Rust and React lanes are not applicable: no executable source changed. Quoin gap-analysis was considered and skipped because this documentation-only scope has no spec root or criterion/test/source chain. Spec-review sub-analyses are not applicable: no spec/ or plan/ artifact changed. Manually checked the approved delivery plan and SWM-159 acceptance prose against all changed guidance. Plan completion: not assessed.

Focused checks: diff whitespace validation passed; all 12 relative links and anchors resolve. No aggregate gate or Rust test was run. No branch edit, commit, push, merge, installed-cache edit or session restart occurred.

## Acceptance walkthrough

| Condition | Required action checked | Result |
| --- | --- | --- |
| Lifecycle WAITING and RECENT | Observe without recovery messages; neither contributes execution | Covered |
| Preferred count null; numeric alias | Preserve null without alias fallback | Covered |
| Legacy numeric alias only | Legacy evidence; lifecycle count remains unknown | Covered |
| Exact zero or positive counts | Complete graph for zero; no execution or capacity inference | Covered |
| Quiet active or recent completed workers | Ages cannot establish lifecycle activity | Covered |
| Legacy WORKING or WAITING-STUCK | Current execution or complete pending-wait evidence; otherwise UNKNOWN | Covered |
| Unsupported verdict | UNKNOWN with no guessed replacement or recovery | Covered |
| Nonzero command with healthy stdout | Preserve status/errors; stop recovery and report rows separately | Covered |
| Success with machine errors, missing teams or partial sources | Report gaps; independently usable complete rows; no clean fleet claim | Covered |
| Unresolved retro population | Preserve unavailable metric; no recomputation from healthy rows | Covered |
| Changed or absent query provenance | Data quality; suppress utilization/trend/regression flags; preserve legacy meaning | Covered |
| Uncertain recovery rubric evidence | n/a and Data quality; WAITING/RECENT do not fail recovery | Covered |

## Examined units

```yaml
scope:
- id: skills/team-minder/SKILL.md:49
  path: skills/team-minder/SKILL.md
  role: examined
  excerpt: 1. Run `ix-board agents <team>... --json --idle-after 20m`. Retain its
    exit
- id: skills/team-minder/SKILL.md:62
  path: skills/team-minder/SKILL.md
  role: examined
  excerpt: |-
    Unsupported verdicts or unresolved classifications are `UNKNOWN`; never guess
       a replacement verdict from counts, ages or file writes.
- id: skills/team-minder/SKILL.md:77
  path: skills/team-minder/SKILL.md
  role: examined
  excerpt: |-
    Before waking `WAITING-STUCK`, confirm a pending wait, complete relevant evidence
    and no viable worker or work for 15m. Then use
    `herdr [--machine M] agent prompt <pane> "continue" --wait --timeout 60000`.
    Herdr rejects a blocked agent; that is fine.
- id: skills/team-minder/SKILL.md:89
  path: skills/team-minder/SKILL.md
  role: examined
  excerpt: |-
    Prefer `active_direct_workers` when the field exists. It counts distinct direct
    workers with unfinished assigned work in `running` or `waiting`; nested workers
    are separate in `active_nested_workers`. Internal approval agents are excluded.
    The deprecated `live_subagents` field is a nullable alias for
    `active_direct_workers` in lifecycle reports. A present `null` means unknown;
    never fall back to the alias to replace it. Exact zero requires a complete
    worker graph. Positive worker counts can explain waiting, but do not prove that
    the lead is executing or has spare capacity.
- id: skills/team-minder/SKILL.md:98
  path: skills/team-minder/SKILL.md
  role: examined
  excerpt: Older reports may have only numeric `live_subagents` and lack lifecycle
    fields
- id: skills/team-minder/SKILL.md:120
  path: skills/team-minder/SKILL.md
  role: examined
  excerpt: |-
    When coverage is complete and every agent is `WORKING`, `WAITING` or `RECENT`,
    the tick is silent and sends nothing. Otherwise give the user one table: agent,
    verdict, age in minutes, action taken. Include command failures, machine errors,
    missing teams and source gaps alongside it, even if no agent row was returned.
    Label `WAITING` and `RECENT` rows as observed without a nudge when shown.
- id: skills/team-retro/SKILL.md:40
  path: skills/team-retro/SKILL.md
  role: examined
  excerpt: |-
    For both commands, retain the original exit status, stdout and stderr before
       parsing. Report nonzero status and structured errors; stop the tick on command
       failure. On success, inspect metric availability and source coverage, including
       machine errors, missing teams and partial agent evidence. Keep healthy metrics
       usable independently; missing rows never establish a clean fleet.
    4. Choose the tier. Run the **full retro** when none has ever run, when none exists today, when a gate ticket completed since the last full retro, or when the user asks. Otherwise run the **light tick**.
- id: skills/team-retro/SKILL.md:65
  path: skills/team-retro/SKILL.md
  role: examined
  excerpt: "- `agents_working_share` uses the lifecycle definition only when its query"
- id: skills/team-retro/SKILL.md:70
  path: skills/team-retro/SKILL.md
  role: examined
  excerpt: "- During rollout, old snapshots retain their recorded query meaning. A
    lifecycle"
- id: skills/team-retro/references/measures.md:38
  path: skills/team-retro/references/measures.md
  role: examined
  excerpt: |-
    `agents_working_share` is the share of reported agents classified `WORKING`
    under the lifecycle query definition. `WAITING` and `RECENT` remain separate
    states and contribute no execution to the numerator. A lower share can reflect
    valid waiting or completed work; it does not establish idle agents or lower
    productivity. Observe those states without nudging. Unknown classifications,
    missing teams or relevant unavailable sources make the share unavailable.
    Preserve the metric's availability and query; never reconstruct a share from
    partial rows, worker counts or file ages.
- id: skills/team-retro/references/measures.md:47
  path: skills/team-retro/references/measures.md
  role: examined
  excerpt: |-
    Use the [minder's count contract](../../team-minder/SKILL.md#reading-worker-counts-during-rollout)
    when inspecting agent rows. Nullable worker counts stay unknown and do not
    measure execution or spare slots. Older reports' numeric `live_subagents`
    measures legacy recent-file evidence; its lifecycle count remains unknown.
- id: skills/team-retro/references/measures.md:64
  path: skills/team-retro/references/measures.md
  role: examined
  excerpt: |-
    The lifecycle execution-share query is versioned separately from the old
    activity heuristic. A transition between them is `query_changed`, even with
    identical windows and thresholds. Show both queries under Data quality and
    suppress trend, regression and utilization flags across that boundary. Missing
    or unsupported query provenance leaves the interpretation unknown. Keep old
    records as recorded; do not relabel their values with the new definition.
- id: skills/team-retro/references/rubric-code-lead.md:18
  path: skills/team-retro/references/rubric-code-lead.md
  role: examined
  excerpt: "| Agent recovery | No confirmed idle agent left unassigned with ready
    work | One confirmed idle agent past the configured threshold | A confirmed idle
    agent left with a ready ticket | Complete `ix-board agents <team>` evidence, configured
    threshold, `ix-board next` |"
- id: skills/team-retro/references/rubric-code-lead.md:24
  path: skills/team-retro/references/rubric-code-lead.md
  role: examined
  excerpt: Unknown or incomplete evidence scores `n/a` and belongs under Data quality.
- id: skills/team-retro/references/rubric-minder.md:10
  path: skills/team-retro/references/rubric-minder.md
  role: examined
  excerpt: "| Waiting and recent activity | `WAITING` and `RECENT` observed without
    nudges; unknown evidence reported | One unnecessary nudge, corrected | Repeated
    nudges or unknown treated as idle | Agent verdicts, source availability, relay
    log |"
- id: skills/team-retro/references/rubric-minder.md:19
  path: skills/team-retro/references/rubric-minder.md
  role: examined
  excerpt: Unavailable evidence scores `n/a` and belongs under Data quality.
- id: skills/team-retro/references/state-record.md:31
  path: skills/team-retro/references/state-record.md
  role: examined
  excerpt: "- <command status/errors, missing teams/source coverage, snapshot gaps,
    query_changed metrics with both queries, unavailable streaks>"
```
