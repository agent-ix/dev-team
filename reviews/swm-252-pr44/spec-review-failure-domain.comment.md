<!-- reviewer repo=agent-ix/dev-team visibility=public quoin=0.36.10 module=spec-artifacts-process@v0.29.2 id=SR-062 method=spec-review/failure-domain lang=spec pr=dev-team#44 head=bcbaf7fc20497e47aa7b99b4b1ba2a05b6363786 model=claude-sonnet-5-5 run=F6E0DDBD-15F0-4124-9B44-74919A6C0E91 -->

Head reviewed bcbaf7f. Verdict FAIL. Not mergeable.

| ID      | Severity | Summary |
| ------- | -------- | ------- |
| FND-001 | high     | The ready buffer counts ready tickets in no reachable assignment, which is what plan-coverage reports as unowned_ready and ORCH-R06 closes each cycle by assigning them. A host with 4 lanes and 8 ready tickets, 2 assigned to each lane (ORCH-R03), has ready work for every lane and a buffer of 0, so no run starts and every window is demand_short. The gate passes mainly while ORCH-R06 gaps are left open, so SWM-189 stays blocked for a compliant orchestrator. |

+++ [reviewer data]

```yaml
clean: false
scope:
  - {id: ORCH-R17, path: spec/roles/orchestrator.md, role: examined, excerpt: "A discovery step SHALL be judged only on a window with at least 90% saturation-sample coverage and ready-buffer tickets at least equal to the step's lane count in every usable sample"}
  - {id: ORCH-R20, path: spec/roles/orchestrator.md, role: examined, excerpt: "A host with no recorded level SHALL be put into discovery when its registry lease is current, its ready buffer is at least the greater of one ticket or its current reachable lane count"}
  - {id: ORCH-R06, path: spec/roles/orchestrator.md, role: context_only, excerpt: "Every gap `fleet plan-coverage` reports (unowned ready ticket, short queue, stale assignment) SHALL be closed in the cycle it appears"}
  - {id: FR-036-AC-1, path: "agent-ix/ix-board spec/functional/FR-036-fleet-plan-coverage.md", role: context_only, excerpt: "A ready ticket in no assignment appears in `unowned_ready` with queue position; one present in any assignment does not."}
findings:
  - fnd: FND-001
    severity: high
    confidence: high
    method: spec-review/failure-domain
    check: soundness
    artifact_id: ORCH-R17
    related_ids: [ORCH-R06, ORCH-R03, ORCH-R20, ORCH-R28, FR-041, FR-036-AC-1]
    path: spec/roles/orchestrator.md
    lines: "267"
    excerpt: |-
      A discovery step SHALL be judged only on a window with at least 90% saturation-sample coverage and ready-buffer tickets at least equal to the step's lane count in every usable sample; a positive target-buffer deficit does not invalidate demand coverage, and an inconclusive window SHALL be repeated.
    finding: "Hole in the decision: the buffer counts ready tickets in no reachable assignment, which plan-coverage reports as unowned_ready and ORCH-R06 closes each cycle by assigning. 4 lanes, 8 ready tickets, 2 assigned per lane (ORCH-R03): every lane has ready work, buffer is 0, no run starts and every window is demand_short. The gate passes mainly while R06 gaps are left open."
bindings: []
```

+++
