# State record

All retro data lives under `$TEAM_RETRO_HOME/<team>/` (default `~/.local/state/team-retro/<team>/`), outside every repository.

| File | Written by | Contents |
|---|---|---|
| `config.json` | the user or planner | the `ix-board retro` configuration for this team |
| `snapshots.jsonl` | `ix-board retro snapshot` and `backfill` | append-only metric records; never edit |
| `gate.jsonl` | `skills/code-lead/scripts/team-gate` | one line per gate run and re-pin |
| `retros/RETRO-<YYYY-MM-DD>.md` | this skill | one file per full retro |
| `actions.jsonl` | this skill | one line per owned action |

## Retro file

```markdown
# Retro <team> <YYYY-MM-DD>

## Measures
| Metric | Value | Δ last | Δ baseline | Flag |
(one row per metric; carry `unavailable` and `query_changed` as written)

## Scores
| Role | Check | Score | Evidence |

## Repeating loops
- <step> — trigger <what> — blocks <work> — strategy <entry> — owner <role> — action <text>

## Data quality
- <snapshot gaps, query_changed metrics, unavailable streaks>

## Actions
- <id> <owner> <action> <due tick>
```

## Action line

```json
{"id":"2026-11-07-1","opened":"2026-11-07","owner":"code-lead","action":"split PR over limit","status":"open","closed":null,"evidence":null}
```

`status` is `open`, `done`, `dropped` or `escalated`. Close an action only with evidence that the condition no longer holds in the next snapshot. An action open for three ticks with no change becomes `escalated` and goes to the user as a decision with a recommendation.

## Linear summary

When `--ticket` is given, post the retro's Measures table, the loops and the actions as one comment on that issue. The comment is the durable record across machines; the store holds the detail on this machine.
