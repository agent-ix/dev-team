---
id: US-002
title: Know whether each role follows its rules and whether the rules help
type: US
relationships:
  - target: ix://agent-ix/dev-team/US-001
    type: traces_to
---
# US-002: Know whether each role follows its rules and whether the rules help

## Story

**As a** department owner running agent roles for days at a time
**I want** every rule a role carries to come with a stated way of checking it, and the results rolled up per session and per role against the throughput the role exists to deliver
**So that** I can see which rules are followed, which rules matter, and which skill instruction to change when a rule keeps failing.

## Context

Role guidance grows by one rule after each incident. Nothing checks later that
the rule was followed, or that following it helped, so the same failure class
returned after the rule was written. A rule that cannot be checked is a wish, a
rule that is always followed and moves no outcome is clutter, and a rule that is
often broken is a defect in the skill that teaches it. The owner wants
objective-leaning checks, clear feedback that names the exact rule, and role
success tied to performance such as idle capacity and time to action.

## Notes

The overnight failures that motivated this story (unreachable host read as
fine, unknown state read as not idle, muted escalation) are the first rules the
worked minder example measures. See [FR-006](../functional/FR-006-role-spec-format.md),
[FR-007](../functional/FR-007-role-spec-lint.md) and
[FR-008](../functional/FR-008-evaluation-result-record.md).
