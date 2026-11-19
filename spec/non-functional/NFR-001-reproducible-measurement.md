---
id: NFR-001
title: Reproduce measurements without mutating observed systems
type: NFR
quality_attribute: reliability
relationships:
  - target: ix://agent-ix/dev-team/FR-001
    type: constrains
  - target: ix://agent-ix/dev-team/FR-002
    type: constrains
---
# NFR-001: Reproduce measurements without mutating observed systems

## Statement

The monitoring collector SHALL compute identical metric payloads for identical
normalized evidence, configuration and observation clock without writing to the
observed tracker, repository, relay queues or live sessions.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|---|---|---|---|
| Metric payload differences on replay | Zero | Zero | Test |
| Mutations to observed systems during collection | Zero | Zero | Test |
| Credentials or raw private transcript content in exported fixtures | Zero | Zero | Inspection |

## Verification

Replay fixed inputs twice with a fixed clock and compare metric payloads. Record
source write attempts and reject any mutation. Inspect sanitized fixture exports;
only derived attributed events and nonsecret references leave the source corpus.
