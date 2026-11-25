---
id: SR-051
title: "Base spec review — SWM-242 FR-015"
type: SpecReview
analysis: base
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md; related FR-005, FR-009, FR-010, FR-011; ix-board FR-041"
review_set: subset
---

## Summary

Reviewed FR-015's IDs, links, requirement quality, criteria, and source consistency against FR-005/009/010/011 and ix-board FR-041. The new metrics semantics are concrete and cover host-wide admission blocking, configured slots, and unsupported sources, but the configured-capacity source conflicts with FR-009.

## Verdict

**FAIL** — FR-015 assigns `ix_build_slots_configured` to host policy `capacity_units`, while FR-009 says the TOML profile is the only source of host limits and that the earlier JSON host policy is ignored; the source of this required metric is therefore contradictory.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | FR-015 defines `ix_build_slots_configured` from host policy `capacity_units`, but FR-009 says the TOML profile is the only source of host limits and explicitly says the earlier JSON host policy is no longer read. FR-015 does not identify a TOML `capacity_units` field or reconcile the JSON policy exclusion, leaving the metric's required source undefined or prohibited. Align the source statements while preserving the agreed configured-capacity meaning. | FR-015 Behavior; FR-015-AC-2; FR-015-AC-12; FR-009 Description; FR-009 Behavior |

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | still-open | The new wording distinguishes the metric's `capacity_units` from FR-009 `[host].max_slots`, but FR-009 still says TOML is the only source of host limits, states its computed sustainable slot count is the enabled capacity used by FR-005, and explicitly rejects the earlier JSON host policy. FR-015 does not establish whether the effective admission configuration is a distinct authoritative source or how it relates to FR-009's enabled capacity, so the normative conflict remains. |
| FND-001 | fixed | Round 2, head d1023710e636c65dcabf7f7235edc8d1215bd05b: FR-009 now makes TOML the target source and permits the transitional capacity_units read until SWM-239, so the source is defined and permitted. |
| FND-002 | still-open | Found in round 2; no fix yet. |
| FND-003 | still-open | Found in round 2; no fix yet. |
| FND-004 | still-open | Found in round 2; no fix yet. |
| FND-005 | still-open | Found in round 2; no fix yet. |
| FND-006 | still-open | Found in round 2; no fix yet. |
| FND-007 | still-open | Found in round 2; no fix yet. |
| FND-002 | fixed | Round 3, head 38f2026: ix_build_pause_seconds_total is restored with thermal and operator reasons, absent until produced. |
| FND-003 | fixed | Round 3: the reason set again lists all seven values, absent until produced (precedence gap is FND-009). |
| FND-004 | accepted-no-change | Round 3: the PR states that abort execution, classification and increments are deliberately unverified in this slice, consistent with the owner order of no aborting governor; abort values are now checked as present at zero. Verification belongs with the governor work. |
| FND-005 | fixed | Round 3: AC-1 names an exact absence set and states the zero-valued outcome exception (the set itself is FND-008). |
| FND-006 | fixed | Round 3: after SWM-239 configured slots come from TOML [host].max_slots, and AC-2 separates the two states. |
| FND-007 | fixed | Round 3: FR-009-AC-8 separates before and after the profile and verifies the JSON file no longer affects values. |
| FND-008 | still-open | Found in round 3; no fix yet. |
| FND-009 | still-open | Found in round 3; no fix yet. |
| FND-010 | still-open | Found in round 3; no fix yet. |
| FND-008 | fixed | Round 4, head 44ef56f: the six emitted and eleven further absent names are listed and match all 19 table names; AC-1 can pass for this build (see FND-011). |
| FND-009 | fixed | Round 4: precedence now orders all seven reasons (see FND-012). |
| FND-010 | fixed | Round 4: both comment bodies are deleted and quire validate of reviews/**/*.md exits 0. |
| FND-011 | still-open | Found in round 4; no fix yet. |
| FND-012 | still-open | Found in round 4; no fix yet. |

## New findings (disposition pass 2)

This pass reviewed the PR diff at d1023710e636c65dcabf7f7235edc8d1215bd05b against FR-010, FR-016, NFR-002, the orchestrator role and ix-board PR 102 (head 31f2fa12dbae323729db69775d7749796a19d5e4). The interim capacity_units source and the absence of a pause series from this build are decided and are not findings.

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-002 | high | The diff deletes ix_build_pause_seconds_total from FR-015 while unchanged FR-010 and FR-010-AC-10 still require held and paused time as pause seconds, and the orchestrator role, its rubric and ix-board FR-041 still name the series (ix-board: absent until its producer exists). FR-010-AC-10 held seconds have no exported series, and pause-blocked admission is measured by nothing. | spec/functional/FR-015-build-metrics-export.md:27-40; spec/functional/FR-010-scheduler-owned-throttling.md:60; spec/roles/orchestrator.md:156-160 |
| FND-003 | high | FR-015 closes the blocked reason set to four values and AC-12 requires no operator, swap or compressor series, while FR-010 requires operator holds and swap and compressor block_above refusals. The reason given is that this build has no producer, which states build state as a permanent requirement. | spec/functional/FR-015-build-metrics-export.md:32,42,77; spec/functional/FR-010-scheduler-owned-throttling.md:23-25 |
| FND-004 | medium | AC-8, AC-9 and AC-10 drop all abort coverage while the outcome table and mapping sentence still require aborted outcomes, so no criterion verifies the aborted_ values that ix-board FR-041 consumes. The remaining non-abort termination members include pause_exceeded. | spec/functional/FR-015-build-metrics-export.md:73-75 |
| FND-005 | medium | AC-1 asks for every applicable series without defining applicable, so omitting any series can pass. Its rule that a metric with no source is omitted conflicts with the requirement to export every outcome from 0, including aborted values that have no producer. | spec/functional/FR-015-build-metrics-export.md:44,66 |
| FND-006 | medium | ix_build_slots_configured is defined only until SWM-239. No TOML key or meaning replaces it (FR-009 has max_slots and computed sustainable slots), and AC-2 also requires a computed sustainable count that does not exist in the interim. | spec/functional/FR-015-build-metrics-export.md:42,67,77; spec/functional/FR-009-host-profile-sustainable-slots.md:18 |
| FND-007 | medium | Rewritten FR-009-AC-8 mixes the interim and post-profile states: it computes sustainable capacity from a TOML profile while that profile does not exist, warns about the file that is in use, and no longer verifies that the JSON file stops being read once the profile exists. | spec/functional/FR-009-host-profile-sustainable-slots.md:18,59 |

## New findings (disposition pass 3)

Fix diff d102371..38f2026 only, rated by real impact.

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-008 | medium | FR-015 calls its current-build absence set complete and says every other table series has a source in this build, and AC-1 requires them all. The current build (dev-tools PR 25) emits six series; eleven others outside the set are not produced, so the claim is false and AC-1 cannot pass for this build. | spec/functional/FR-015-build-metrics-export.md:43,69 |
| FND-009 | low | The reason set now lists seven values but the precedence orders only probe, host_load, target_disk and memory, so swap, compressor and operator are unordered once produced, although AC-11 verifies the documented precedence. | spec/functional/FR-015-build-metrics-export.md:45 |
| FND-010 | low | The diff commits two Linear comment bodies under reviews/. They are not artifacts, duplicate the SR files, and make quire validate of reviews/**/*.md fail on both. | reviews/swm-242-round2/comment-r2-SR-045.md:1; reviews/swm-242-round2/comment-r2-SR-051.md:1 |

## New findings (disposition pass 4)

Fix diff 38f2026..44ef56f only, rated by real impact.

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-011 | low | AC-1 is pinned to today's implementation: it fails as soon as any listed producer ships, and no longer requires the other table series to carry expected values and labels once produced. | spec/functional/FR-015-build-metrics-export.md:69 |
| FND-012 | low | operator is ranked last in the precedence, yet a hold never accrues here; with a hold and a memory limit together the precedence picks memory while the pause exclusion accrues nothing. | spec/functional/FR-015-build-metrics-export.md:45 |
