---
id: IT-001
title: Replay incidents across independent team scopes
type: IT
relationships:
  - target: ix://agent-ix/dev-team/FR-001
    type: verifies
  - target: ix://agent-ix/dev-team/FR-002
    type: verifies
  - target: ix://agent-ix/dev-team/FR-004
    type: verifies
  - target: ix://agent-ix/dev-team/FR-005
    type: verifies
---
# IT-001: Replay incidents across independent team scopes

## Objective

Verify that normalized tracker/VCS/pane/relay/host/scheduler evidence produces
the expected department findings and terminal model across two unrelated teams.

## Target Integration

ix-board collectors and retro store/delta, shared scheduler event reader and
the status/health/retro renderer. Read-only adapters are exercised against fixed
source responses; a separate scheduler integration run verifies child cleanup.

## Preconditions

The 2026-11-14..19 planner corpus has been sanitized into attributed events with
source offsets and expected values. A second synthetic team uses different
IDs, hosts, capacities and thresholds. No credentials/raw transcript is bundled.
An unavailable original source is recorded as a missing pilot obligation rather
than replaced by a claimed observed incident.

## Inputs

Fixtures include stale started claims, merged-open issues, blocker fan-in,
tag→repin, state bounce, reversed orders, long lock wait, low disk, login screen,
finished nested workers, unacknowledged orders, refusal/frozen intervals, red
main, review rounds, delayed rulings and correction-heavy message traffic.

## Test Procedure

1. Collect each team's normalized source fixtures with a fixed clock.
   - IT-001-SC-01: exact populations and all expected catalog values are emitted.
2. Persist two comparable snapshots and compare previous/baseline reports.
   - IT-001-SC-02: trends, loops and owner/action routing match expected events.
3. Render status/health/retro from the shared model.
   - IT-001-SC-03: findings and partial-source statuses match JSON exactly.
4. Remove one relation page, remote pane source and semantic attribution.
   - IT-001-SC-04: affected metrics become unavailable without false green.
5. Run scheduler fairness, reservation and process-cleanup scenarios.
   - IT-001-SC-05: all requests observe the configured bound and lease safety.

## Expected Results

Every success criterion holds in both scopes, without project-specific code,
hardcoded slot counts or writes to live systems. Fixture replay verifies behavior;
it does not establish that historical symptoms were independently reproduced.
