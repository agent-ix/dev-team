---
id: SR-060
title: "EARS conformance review of SWM-252 ORCH-R17 and ORCH-R20"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/dev-team@bcbaf7fc20497e47aa7b99b4b1ba2a05b6363786; spec/roles/orchestrator.md (ORCH-R17, ORCH-R20, Valid window)"
review_set: subset
---

## Summary

Ticket: SWM-252. The two edited requirement statements and the Valid window bullet, read for one meaning, against the minder decision and ix-board FR-041-AC-11 in the ix-board#102 worktree.

## Verdict

**CONDITIONAL**. Both statements keep the subject and SHALL form and quire reports no grammar finding. The window condition is stated twice with an undefined term.

## Findings

| ID      | Severity | Summary | Refs |
| ------- | -------- | ------- | ---- |
| FND-001 | medium   | "Usable sample" is undefined, and ORCH-R17 (90% sample coverage) and the Valid window bullet (90% span of demand-covering samples) word the test differently. A window of 24 samples with 23 covering and 1 without ready-buffer evidence is valid if that sample is unusable and skipped, and is invalid (deficit_coverage) under ix-board FR-041-AC-11 and its implementation in ix-board#102. | spec/roles/orchestrator.md:267, spec/roles/orchestrator.md:146 |

## New findings (disposition pass 2)

| ID | Severity | Summary | Refs |
| -- | -------- | ------- | ---- |
| FND-002 | high | The SHALL sentence of ORCH-R20 no longer requires covered demand; the following sentences define coverage and the zero-lane gate but nothing makes either a condition of the start. An unrecorded host with 4 idle lanes, an empty ready buffer and a current lease must be put into discovery as written, against the Start bullet, both skill files and the rubric. faf8cfa had the condition. | spec/roles/orchestrator.md:289 |

## Dispositions

Round 1, checked at faf8cfa0fc545c689d87cbc3b169f3af6b41cdc0.

| FND     | outcome | reason |
| ------- | ------- | ------ |
| FND-001 | fixed   | "Usable sample" is gone; ORCH-R17 and the Valid window bullet both require every sample to carry evidence and cover demand, with covering samples spanning at least 90%. |

Round 2, checked at fc263a5c55fe5f1e8c4befb348ddac4ddd34b886: no earlier finding was open.
