<!-- reviewer repo=agent-ix/dev-team visibility=public quoin=0.36.10 module=spec-artifacts-process@v0.29.2 id=SR-060 method=spec-review/ears-conformance lang=spec pr=dev-team#44 head=bcbaf7fc20497e47aa7b99b4b1ba2a05b6363786 model=claude-sonnet-5-5 run=F6E0DDBD-15F0-4124-9B44-74919A6C0E91 -->

Head reviewed bcbaf7f. Verdict CONDITIONAL. Not mergeable.

| ID      | Severity | Summary |
| ------- | -------- | ------- |
| FND-001 | medium   | "Usable sample" is undefined, and ORCH-R17 (90% sample coverage) and the Valid window bullet (90% span of demand-covering samples) word the test differently. A window of 24 samples with 23 covering and 1 without ready-buffer evidence is valid if that sample is unusable and skipped, and is invalid (deficit_coverage) under ix-board FR-041-AC-11 and its implementation in ix-board#102. |

+++ [reviewer data]

```yaml
clean: false
scope:
  - {id: ORCH-R17, path: spec/roles/orchestrator.md, role: examined, excerpt: "A discovery step SHALL be judged only on a window with at least 90% saturation-sample coverage and ready-buffer tickets at least equal to the step's lane count in every usable sample; a positive target-buffer deficit does not invalidate demand coverage, and an inconclusive window SHALL be repeated."}
  - {id: ORCH-R20, path: spec/roles/orchestrator.md, role: examined, excerpt: "A host with no recorded level SHALL be put into discovery when its registry lease is current, its ready buffer is at least the greater of one ticket or its current reachable lane count, and the capacity history is available to record the run; a positive target-buffer deficit does not prevent discovery."}
  - {id: FR-041-AC-11, path: "agent-ix/ix-board spec/functional/FR-041-fleet-saturation.md", role: context_only, excerpt: "A window with demand-covered samples spanning under 90%, no samples, or unavailable ready-buffer evidence is invalid with `deficit_coverage`"}
findings:
  - fnd: FND-001
    severity: medium
    confidence: high
    method: spec-review/ears-conformance
    check: ambiguous
    artifact_id: ORCH-R17
    related_ids: [ORCH-R28, FR-041-AC-11]
    path: spec/roles/orchestrator.md
    lines: "267"
    excerpt: |-
      A discovery step SHALL be judged only on a window with at least 90% saturation-sample coverage and ready-buffer tickets at least equal to the step's lane count in every usable sample; a positive target-buffer deficit does not invalidate demand coverage, and an inconclusive window SHALL be repeated.
    finding: "'Usable sample' is undefined and this rule (90% sample coverage) and the Valid window bullet (90% span of demand-covering samples) word the test differently. 24 samples, 23 covering and 1 without ready-buffer evidence: valid if the one is unusable and skipped, invalid (deficit_coverage) under FR-041-AC-11 and the ix-board#102 implementation."
bindings: []
```

+++
