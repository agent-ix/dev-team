---
id: US-003
title: Run agent builds on hosts that stay healthy
type: US
relationships:
  - target: ix://agent-ix/dev-team/US-001
    type: depends_on
---
# US-003: Run agent builds on hosts that stay healthy

## Story

**As a** code lead or coder agent working across several build hosts
**I want** to submit a build or test at a pushed commit, name a host and a priority, and receive a short result
**So that** hosts neither overheat or run out of memory nor sit idle, my merge gates are not stuck behind routine checks, and I do not spend context reading raw logs.

## Context

Build capacity is arbitrated today by several hand-maintained pieces: a slot
wrapper whose slot count is edited in a comment after someone reads the memory
compressor, a remote runner that builds a pushed commit in a persistent target
directory, and a heat guard that stops and resumes build processes by name.
When the heat guard died, 46 builds stayed stopped. Two builds sharing a target
directory blocked a ticket for over thirty minutes. Builds started at normal priority starved the relay bus and Prometheus on shared hosts. Agents read long logs to find
one failing test. [FR-005](../functional/FR-005-fair-build-scheduler.md) already
grants leases fairly; this story covers the host-health, target-directory,
result and routing needs around those leases.
