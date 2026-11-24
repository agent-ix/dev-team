---
id: FR-012
title: Pool warm target directories per repository and toolchain
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-003
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-009
    type: depends_on
---
# FR-012: Pool warm target directories per repository and toolchain

## Description

The scheduler SHALL manage a pool of build target directories for each repository
and toolchain so that a build reuses compiled artifacts from an earlier build, no
two builds ever share one target directory, and the pool stays within a disk budget.

## Behavior

A pool key is the repository name, the toolchain identity (compiler version and
host triple) and the build profile environment that changes artifacts. A slot is
one target directory, with a detached checkout of the requested commit where the
host builds a pushed commit ([FR-014](FR-014-remote-dispatch-pushed-sha.md)). A job
needs a free slot of its key in addition to a lease. The scheduler selects the free
slot with the most recent use (warmest); if none is free and the pool is below
its slot limit and disk budget it creates one; otherwise the request waits queued
with reason `target_slot` or `target_disk` and keeps its age. A slot is held
exclusively from admission to verified exit and then released with its last-used
time and last commit recorded.

Disk budget: the profile sets a total pool budget and a per-key slot limit. Before
creating or growing a slot the scheduler evicts free slots in least-recently-used
order until the budget fits; it never evicts a held slot. Directories in the pool root that the scheduler
did not create are reported and never deleted. `pool status` reports bytes per key
and slot, and `pool prune` removes free slots older than a configured age or over
budget. When a caller names its own target directory, the scheduler serializes
requests on the canonical path (realpath with symlinks resolved, case-folded on case-insensitive filesystems such as default APFS) so that two builds never run on one directory under any alias or from different worktrees. Bare repository mirrors of [FR-014](FR-014-remote-dispatch-pushed-sha.md) are counted in the same disk budget. A shared compiler cache, where configured, is exposed to jobs
by environment, counted in the disk budget, and reported with hit statistics.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-012-AC-1 | Two sequential jobs on the same key use the same slot directory and the second finds the first's artifacts; two concurrent jobs on one key never receive the same directory. | Test |
| FR-012-AC-2 | With the budget fitting two slots and three keys in use, creating a third slot evicts the least recently used free slot, never a held one; if all slots are held the request waits with reason `target_disk` and keeps its enqueue age. | Test |
| FR-012-AC-3 | Two concurrent requests that name one explicit target directory from different worktrees run one after the other; the waiting one shows reason `target_slot`. | Test |
| FR-012-AC-4 | Two concurrent requests naming one target directory through a relative path, a symlink alias and (on a case-insensitive filesystem) a case variant run one after the other; the waiting ones show reason `target_slot`. | Test |
| FR-012-AC-5 | A directory in the pool root not created by the scheduler appears in `pool status` as foreign and survives `pool prune`. | Test |
| FR-012-AC-6 | `pool prune` removes free slots over age or over budget, reports reclaimed bytes, and a scheduler restart after a crash releases slots whose lease exit is verified and keeps slots whose group is still alive. | Test |
| FR-012-AC-7 | With a shared compiler cache configured the job environment points at it, its size counts toward the budget, and hit statistics appear in the job summary; with none configured the environment is untouched. | Test |

## Dependencies

- [FR-009](FR-009-host-profile-sustainable-slots.md), disk probe and reserve.
- [FR-005](FR-005-fair-build-scheduler.md), lease lifecycle and crash recovery.
