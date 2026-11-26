---
id: FR-012
title: Assign and trim owner target directories
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-003
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-009
    type: depends_on
---
# FR-012: Assign and trim owner target directories

## Description

When a target root is configured, the scheduler SHALL assign a private target
directory to each owner beneath it. A later lease for that same owner reuses its
directory; different owners never share one. The scheduler SHALL trim an owner's
directory when its idle age exceeds the configured age limit or its size exceeds
the configured size limit.

## Behavior

The directory path is scoped by the lease owner, not by repository and toolchain.
This intentionally keeps the cleanup boundary aligned with the owner's work and
prevents concurrent owners from mutating the same artifacts. It does not promise
cross-owner warm-cache reuse or pool-wide eviction. When `trim_after_ms` is
configured, the scheduler deletes an owner's directory at lease end if the
most recently modified file has been idle at least that long. When `max_bytes` is configured, it
deletes the owner's directory at lease end if its measured size exceeds the
limit. Cleanup is skipped while another lease for that owner is active. The
scheduler never deletes a directory outside its configured target root or a
directory it did not assign to an owner.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-012-AC-1 | Two sequential leases for one owner use the same `CARGO_TARGET_DIR`; concurrent leases for different owners receive different directories. | Test |
| FR-012-AC-2 | At lease end, a target whose idle age meets `trim_after_ms` is deleted; a target whose size exceeds `max_bytes` is deleted; otherwise its artifacts remain available to the next lease for that owner. | Test |
| FR-012-AC-3 | Cleanup is skipped while another lease for the owner is active, and the target path remains beneath the configured target root. | Test |

## Dependencies

- [FR-009](FR-009-host-profile-sustainable-slots.md), disk probe and reserve.
- [FR-005](FR-005-fair-build-scheduler.md), lease lifecycle and crash recovery.
