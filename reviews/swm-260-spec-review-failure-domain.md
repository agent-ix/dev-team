---
id: SR-040
title: "Failure domain analysis of SWM-260 FR-015 build outcome set"
type: SpecReview
analysis: failure-domain
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md"
review_set: subset
---

## Summary

Examined the counting rule and outcome labels at e6a1b6880c4b4b5b616722261cf31a98d96e5d84 (PR dev-team#38, ticket SWM-260) for competing termination causes, first appearance of a series and restart. Three failure cases are unspecified.

## Verdict

**CONDITIONAL**. A child crash, a signaled child and a lost or rebooted supervisor end in FR-005 states that the table covers, and pause or operator hold ends a request only through `pause_exceeded`, which is listed. Cause precedence, zero-valued series and once-only counting across restart remain open. Request identity is the FR-005 request id.

## Findings

| ID      | Severity | Summary | Refs |
| ------- | -------- | ------- | ---- |
| FND-001 | medium   | No rule picks the outcome when two end causes apply to one request. A user cancel or hold deadline starts termination and the lease exceeds `rss_cap` or is picked for abort during the grace period; or memory and swap are both above `abort_above` in one sample. "Ends with a termination reason" lets one implementation keep the first cause and another overwrite it, so a cancelled build can count as `aborted_memory`. State that the first recorded cause wins and how one reason is chosen among simultaneous breaches. | spec/functional/FR-015-build-metrics-export.md:59, spec/functional/FR-010-scheduler-owned-throttling.md:25 |
| FND-002 | medium   | The closed set is not required to be exported at zero. A labelled series that first appears at 1 shows no increase in Prometheus, so the first `aborted_thermal` for a priority on a host can be missed by the ix-board FR-041 `build_abort` check, and the drain it justifies is listed as lacking throttle evidence. Require every outcome value for every priority to be exported from 0, with an AC. | spec/functional/FR-015-build-metrics-export.md:43, spec/functional/FR-015-build-metrics-export.md:72 |
| FND-003 | medium   | "Counts each request once" has no criterion across restart, recovery or prune. AC-3 only forbids a decrease and AC-8 does not restart, so a scheduler that replays persisted terminal events and counts a finished request again passes every AC and reports aborts that did not happen. Require equal per-outcome values before and after a restart, recover and prune. | spec/functional/FR-015-build-metrics-export.md:43, spec/functional/FR-015-build-metrics-export.md:67 |
