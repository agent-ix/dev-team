---
id: SR-034
title: "spec-review integrity of SWM-225 rubric touches"
type: SpecReview
analysis: integrity
scope: "agent-ix/dev-team; SWM-225; diff origin/main...5656282 (PR dev-team#33): skills/team-minder/**, skills/team-retro/**, skills/index.json, README.md, spec/rubrics/rubric-minder.md; against spec/roles/minder.md v3"
review_set: subset
date: 2026-11-24
---

# spec-review integrity of SWM-225 rubric touches

## Summary

Integrity analysis of the rubric-minder edit and the references to it from team-retro, the spec index and skills/index.json.

Ticket: SWM-225. PR: dev-team#33 at 5656282. The lead's four decisions on the coder's open points were treated as binding intent.

## Verdict

**PASS**. Integrity holds for the touched spec content: rubric-minder frontmatter (id, version 2, satisfies FR-006) is unchanged and consistent with its prose; every `rubric-minder@2#<slug>` cited by MIND evaluations and by team-retro resolves to a check row; the spec.md index row still points at the file; the deleted v1 rubric is no longer listed in skills/index.json and nothing in skills/ or spec/ links to it. The v4/v3 bumps the lead's decisions require are recorded in SR-033.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | low | No findings (placeholder) | - |

## Examined Scope

```yaml
scope:
- id: rubric-minder
  path: spec/rubrics/rubric-minder.md
  role: examined
  excerpt: "---\nid: rubric-minder\nversion: 2\ntype: Rubric\nrelationships:\n  - target: ix://agent-ix/dev-team/FR-006\n\
    \    type: satisfies\n---\n# Rubric: minder\n\nThe minder rubric grades the judgement evaluations of the\n[minder\
    \ role spec](../roles/minder.md). A judgement evaluation cites one\ncheck as `rubric-minder@2#<check-slug>`.\
    \ `/team-retro` scores the minder\nwith this version, and the `team-minder` skill is derived from the same role\n\
    spec version."
- id: skills/team-retro/SKILL.md:25
  path: skills/team-retro/SKILL.md
  role: examined
  excerpt: 1. **Already in a loop:** if this prompt is a loop's scheduled prompt, or a loop for it is active (the
    harness's scheduler listing; `CronList` in Claude Code), skip setup and run the tick. In a harness with no listing,
    the minder rubric's `rubric-minder@2#loop-alive` check scores `n/a`.
- id: skills/team-retro/SKILL.md:63
  path: skills/team-retro/SKILL.md
  role: examined
  excerpt: '1. Score every rubric: [planner](references/rubric-planner.md), [code lead](references/rubric-code-lead.md),
    [coder](references/rubric-coder.md), [reviewer](references/rubric-reviewer.md) and [minder](https://github.com/agent-ix/dev-team/blob/main/spec/rubrics/rubric-minder.md)
    (version 2, cited as `rubric-minder@2#<check>`). Each score is 0, 1 or 2 with one cited piece of evidence, or
    `n/a` when the evidence was not read; `n/a` stays out of the 0 to 2 scale and is listed under Data quality.
    Do not average scores into one number.'
- id: spec/spec.md:72
  path: spec/spec.md
  role: examined
  excerpt: '| [Minder rubric](rubrics/rubric-minder.md) | Judgement checks for minder evaluations and retros |'
- id: skills/index.json
  path: skills/index.json
  role: examined
  excerpt: "    },\n    {\n      \"name\": \"team-retro\",\n      \"version\": \"0.3.0\",\n      \"files\": [\n\
    \        \"SKILL.md\",\n        \"references/measures.md\",\n        \"references/department-health.md\",\n\
    \        \"references/rubric-planner.md\",\n        \"references/rubric-code-lead.md\",\n        \"references/rubric-coder.md\"\
    ,\n        \"references/rubric-reviewer.md\",\n        \"references/state-record.md\",\n        \"references/strategies.md\"\
    \n      ]"
```
