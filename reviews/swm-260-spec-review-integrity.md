---
id: SR-039
title: "Integrity analysis of SWM-260 FR-015 build outcome set"
type: SpecReview
analysis: integrity
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md"
review_set: subset
---

## Summary

Checked the closed outcome set and FR-015-AC-8 at e6a1b6880c4b4b5b616722261cf31a98d96e5d84 (PR dev-team#38, ticket SWM-260) for consistency with FR-005, FR-009, FR-010 and ix-board FR-041. The set is not closed by the requirements that produce the reasons, and one clause of AC-8 refers to a set no requirement defines.

## Verdict

**CONDITIONAL**. The table matches the reasons FR-010 spells out, and the override paragraph removes the overlap between a state value and a reason value. The enumerated part of AC-8 is falsifiable: each of eleven values must rise by one, no other series may rise, and no other value may be exported. FR-015 keeps its existing relationships to FR-005 and FR-010; no new edge is needed.

## Findings

| ID      | Severity | Summary | Refs |
| ------- | -------- | ------- | ---- |
| FND-001 | medium   | FR-015 declares a closed set, but nothing limits the reasons that can reach it. FR-009 gives every `[[limit]]` free `abort_above` and `reason` keys and refuses neither value, and FR-010 records `aborted_<reason>`. A loadable profile with a package-power limit carrying `abort_above` and reason `power` yields `aborted_power`, so the exporter must break AC-8 or drop or mislabel the request. Have FR-009 or FR-010 refuse `abort_above` outside memory, swap, compressor, host_load and thermal. | spec/functional/FR-015-build-metrics-export.md:43, spec/functional/FR-009-host-profile-sustainable-slots.md:35, spec/functional/FR-010-scheduler-owned-throttling.md:25 |
| FND-002 | low      | AC-8 opens with "the scheduler's FR-010 reason set", which FR-010 does not define: it gives the template `aborted_<reason>` and names `rss_cap` and `pause_exceeded` in prose. The AC then repeats seven literals, so a test hardcodes them and a reason added to the scheduler later is not detected. Name the enumerable source the test iterates, or drop the first clause. | spec/functional/FR-015-build-metrics-export.md:72, spec/functional/FR-010-scheduler-owned-throttling.md:25 |
