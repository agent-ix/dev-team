---
id: FR-012
title: Manage target pools and owner directories
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-003
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-009
    type: depends_on
---
# FR-012: Manage target pools and owner directories

## Description

The scheduler SHALL support a repository/toolchain target pool and a per-owner
target-directory mode. The host profile selects pool mode with `[pool]` or
per-owner mode with `target_root`. Pool mode SHALL hold each selected slot
exclusively through verified command exit. Per-owner mode SHALL keep directories
private across owners and defer cleanup while an owner has an active lease. Both
modes SHALL preserve reusable build artifacts and keep managed data within the
configured disk boundaries.

## Behavior

**Repository/toolchain pool mode.** A pool key is the repository name, the
toolchain identity (compiler version and host triple), and the build profile
environment that changes artifacts. A slot is one target directory, with a
detached checkout of the requested commit when the host builds a pushed commit
([FR-014](FR-014-remote-dispatch-pushed-sha.md)). A job needs a free slot of its
key in addition to a lease. The scheduler selects the free slot with the most
recent use (warmest); if none is free and the pool is below its slot limit and
disk budget, it creates one. Otherwise, the request waits queued with reason
`target_slot` or `target_disk` and keeps its age. A slot is held exclusively from
admission to verified exit, then released with its last-used time and last
commit recorded.

The profile sets a total pool budget and a per-key slot limit. Before creating
or growing a slot, the scheduler evicts free slots in least-recently-used order
until the budget fits; it never evicts a held slot. Directories in the pool root
that the scheduler did not create are reported and never deleted. `pool status`
reports bytes per key and slot, and `pool prune` removes free slots older than a
configured age or over budget. Bare repository mirrors of [FR-014](FR-014-remote-dispatch-pushed-sha.md)
are counted in the same disk budget. A configured shared compiler cache is
exposed to jobs by environment, counted in the disk budget, and reported with
hit statistics.

When a caller names an explicit target directory, the scheduler serializes
requests on its canonical path, resolving symlinks and case-folding paths on
case-insensitive filesystems. This prevents two builds from using the same
directory through aliases or from different worktrees.

**Per-owner mode.** When `target_root` is configured, each owner receives a
private `CARGO_TARGET_DIR` beneath that root. A later lease for the same owner
reuses the directory; another owner receives a different directory. At lease
end, cleanup is skipped while another lease for that owner is active. If
`trim_after_ms` is configured, the scheduler deletes the owner's directory when
the newest file's idle age reaches or exceeds that duration. If `max_bytes` is
configured, it deletes the directory when its measured size exceeds that limit.
The scheduler refuses symlink entries and never follows or deletes a path
outside the configured target root.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-012-AC-1 | Two sequential jobs with the same repository, toolchain, and build-profile key use the same pool slot and the second finds the first job's artifacts; concurrent jobs never receive the same slot. | Test |
| FR-012-AC-2 | With a budget fitting two slots and three keys in use, creating a third slot evicts the least-recently-used free slot and never a held one; if all slots are held, the request waits with reason `target_disk` and keeps its enqueue age. | Test |
| FR-012-AC-3 | Two concurrent requests naming one explicit target directory from different worktrees run one after another; the waiting request reports `target_slot`. | Test |
| FR-012-AC-4 | Requests naming one target directory through a relative path, symlink alias, or case variant on a case-insensitive filesystem run one after another and report `target_slot` while waiting. | Test |
| FR-012-AC-5 | A directory in the pool root that the scheduler did not create appears as foreign in `pool status` and survives `pool prune`. | Test |
| FR-012-AC-6 | `pool prune` removes free slots older than the configured age or over budget and reports reclaimed bytes; after restart, it releases slots only when lease exit is verified and keeps a slot held while its child group is still running. | Test |
| FR-012-AC-7 | With a shared compiler cache configured, the job environment points to it, its size counts toward the budget, and hit statistics appear in the job summary; without one, the environment is untouched. | Test |
| FR-012-AC-8 | In per-owner mode, sequential leases for one owner reuse its `CARGO_TARGET_DIR`, while leases for different owners receive different paths beneath `target_root`. | Test |
| FR-012-AC-9 | At lease end, a target is deleted when its newest file has been idle for at least `trim_after_ms`, or when its measured size exceeds `max_bytes`; otherwise its artifacts remain available to the next lease for that owner. | Test |
| FR-012-AC-10 | Per-owner cleanup is skipped while another lease for that owner is active. A symlink entry or a resolved path that escapes `target_root` is refused, and no path outside the root is deleted. | Test |

## Dependencies

- [FR-009](FR-009-host-profile-sustainable-slots.md), disk probe and reserve.
- [FR-005](FR-005-fair-build-scheduler.md), lease lifecycle and crash recovery.
