<!-- reviewer repo=agent-ix/dev-team visibility=public quoin=0.36.10 module=spec-artifacts-process@v0.29.2 id=SR-061 method=spec-review/integrity lang=spec pr=dev-team#44 head=bcbaf7fc20497e47aa7b99b4b1ba2a05b6363786 model=claude-sonnet-5-5 run=F6E0DDBD-15F0-4124-9B44-74919A6C0E91 -->

Head reviewed bcbaf7f. Verdict CONDITIONAL. Not mergeable.

| ID      | Severity | Summary |
| ------- | -------- | ------- |
| FND-001 | medium   | "Its ready buffer" has no definition: FR-041 defines one global buffer. Read as global, 3 hosts of 10 lanes with 12 ready tickets are all covered (30 lanes, 12 tickets); read as a share of 4 each, none is. ix-board#102 does both: a zero-lane host gets the global count and other hosts a share proportional to their target, so a host with unavailable duty gets no share and is never covered. |

+++ [reviewer data]

```yaml
clean: false
scope:
  - {id: ORCH-R20, path: spec/roles/orchestrator.md, role: examined, excerpt: "A host with no recorded level SHALL be put into discovery when its registry lease is current, its ready buffer is at least the greater of one ticket or its current reachable lane count"}
  - {id: rubric-orchestrator, path: spec/rubrics/rubric-orchestrator.md, role: examined, excerpt: "every usable sample had ready-buffer tickets at least equal to the step's lane count"}
  - {id: skills/fleet-orchestrator/references/capacity-discovery.md, path: skills/fleet-orchestrator/references/capacity-discovery.md, role: examined, excerpt: "A zero-lane host uses bootstrap ready-buffer evidence and needs one ready ticket for its first lane."}
  - {id: FR-041, path: "agent-ix/ix-board spec/functional/FR-041-fleet-saturation.md", role: context_only, excerpt: "**Ready buffer**: the count of ready, unassigned and unstarted tickets"}
findings:
  - fnd: FND-001
    severity: medium
    confidence: high
    method: spec-review/integrity
    check: ambiguous
    artifact_id: ORCH-R20
    related_ids: [ORCH-R17, FR-041]
    path: spec/roles/orchestrator.md
    lines: "270"
    excerpt: |-
      its ready buffer is at least the greater of one ticket or its current reachable lane count
    finding: "FR-041 defines one global ready buffer and nothing defines a host's. Read as global, 3 hosts of 10 lanes with 12 ready tickets are all covered; read as a share of 4 each, none is. ix-board#102 gives a zero-lane host the global count and other hosts a share proportional to their target, so a host with unavailable duty gets no share and is never covered."
bindings: []
```

+++
