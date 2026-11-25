---
id: SR-038
title: "Base review of SWM-260 FR-015 build outcome set"
type: SpecReview
analysis: base
scope: "agent-ix/dev-team; spec/functional/FR-015-build-metrics-export.md"
review_set: subset
---

## Summary

Base checklist over the FR-015 diff at e6a1b6880c4b4b5b616722261cf31a98d96e5d84 (PR dev-team#38, ticket SWM-260), read against FR-005, FR-010 and ix-board FR-041 at 8bf053d. One acceptance criterion leaves a stated path uncovered and one sentence is imprecise.

## Verdict

**CONDITIONAL**. Every FR-005 terminal state (succeeded, failed, timed_out, cancelled) and every FR-010 termination reason named in the text (five `aborted_` values, `rss_cap`, `pause_exceeded`) has a value, and `outcome=~"aborted_.*"` selects the five `abort_above` aborts and nothing else. Both ticket checklist items are addressed; the AC-8 test is tracked on SWM-242. IDs are well formed and AC-8 names a verification method. No hash, digest or pin is added. Applicable AssuranceProfile: none exists under `spec/`.

## Findings

| ID      | Severity | Summary | Refs |
| ------- | -------- | ------- | ---- |
| FND-001 | medium   | The `cancelled` row covers a request cancelled while queued or running, but AC-8 asks for one request ending in `cancelled`. A scheduler that increments the counter only when a lease is released passes AC-8 with a running cancel and never counts a queued-to-cancelled request; AC-1 does not require a queued cancel either. Require one cancel of each kind. | spec/functional/FR-015-build-metrics-export.md:72, spec/functional/FR-015-build-metrics-export.md:49 |
| FND-002 | low      | "Only the resource-limit aborts begin with `aborted_`" uses an undefined term. `rss_cap` is also a termination for exceeding a resource limit and does not begin with `aborted_`, so a consumer author can read `aborted_.*` as covering RSS kills and miss them. Say the `abort_above` aborts. | spec/functional/FR-015-build-metrics-export.md:59 |

## Dispositions

Round 1, checked at beed47004ea594ad6363e714dfad886f0ae56a5d.

| FND     | outcome | reason |
| ------- | ------- | ------ |
| FND-001 | fixed   | FR-015-AC-8 now requires one queued cancel and one running cancel, each counted once under `cancelled`. |
| FND-002 | fixed   | The sentence names the `abort_above` aborts and says the regex does not select `rss_cap`. |
