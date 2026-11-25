<!-- reviewer repo=agent-ix/dev-team visibility=public quoin=0.36.10 module=spec-artifacts-process@v0.29.2 id=SR-058 method=code-review lang=spec pr=dev-team#44 head=bcbaf7fc20497e47aa7b99b4b1ba2a05b6363786 model=claude-sonnet-5-5 run=F6E0DDBD-15F0-4124-9B44-74919A6C0E91 -->

Head reviewed bcbaf7f. Verdict CONDITIONAL. Not mergeable.

| ID      | Severity | Summary |
| ------- | -------- | ------- |
| FND-001 | medium   | Both skill files dropped, or never state, the start condition "the capacity history is available to record the run" that ORCH-R20 requires; the reference removed it in this diff. Only the not-installed case remains, so with fleet capacity installed and the ledger unwritable a run is started that cannot be recorded, breaching ORCH-R19. |
| FND-002 | low      | The skill and the reference say "current lane count" where the role spec and ORCH-R20 say "current reachable lane count". With 2 reachable and 2 unreachable lanes and 3 ready tickets the spec starts discovery and the skill reading does not. |
| FND-003 | low      | The frontmatter moved to role_spec_version 6 while the body still says the skill is the role "version 5". |
| FND-004 | low      | The ownership reference still names role spec version 5 after the spec moved to 6. |

+++ [reviewer data]

```yaml
clean: false
scope:
  - {id: skills/fleet-orchestrator/SKILL.md, path: skills/fleet-orchestrator/SKILL.md, role: examined, excerpt: "- A host with no recorded level enters discovery when its registry lease is current and its ready buffer is at least the greater of one ticket or its current lane count; a positive target-buffer deficit does not prevent discovery (ORCH-R20)."}
  - {id: skills/fleet-orchestrator/references/capacity-discovery.md, path: skills/fleet-orchestrator/references/capacity-discovery.md, role: examined, excerpt: "4. **Demand gate.** Judge a step only when demand-covering saturation samples span at least 90% of the window and every usable sample has ready-buffer tickets at least equal to the step's lane count."}
  - {id: rubric-orchestrator, path: spec/rubrics/rubric-orchestrator.md, role: examined, excerpt: "A judgement evaluation cites one check as `rubric-orchestrator@2#<check-slug>`."}
  - {id: skills/fleet-orchestrator/references/ownership.md, path: skills/fleet-orchestrator/references/ownership.md, role: examined, excerpt: "Source: the Ownership section of the orchestrator role spec, version 5."}
  - {id: ORCH-R14, path: spec/roles/orchestrator.md, role: context_only, excerpt: "A positive ready-buffer deficit SHALL be sent to each owning planner as a request for the stated number of ready tickets in the cycle it appears."}
findings:
  - fnd: FND-001
    severity: medium
    confidence: high
    method: code-review
    check: code-bug
    artifact_id: skills/fleet-orchestrator/references/capacity-discovery.md
    related_ids: [ORCH-R19, ORCH-R20, skills/fleet-orchestrator/SKILL.md]
    path: skills/fleet-orchestrator/references/capacity-discovery.md
    lines: "7"
    excerpt: |-
      1. **Start.** A host with no recorded level starts a run when its registry lease is current and its ready buffer is at least the greater of one ticket or its current lane count (ORCH-R20).
    finding: "The diff removed 'and the capacity history is available to record the run', and SKILL.md:142 does not state it either. Only the not-installed case remains, so with fleet capacity installed and the ledger unwritable a run is started that cannot be recorded, breaching ORCH-R19."
  - fnd: FND-002
    severity: low
    confidence: high
    method: code-review
    check: ambiguous
    artifact_id: skills/fleet-orchestrator/SKILL.md
    related_ids: [ORCH-R20, skills/fleet-orchestrator/references/capacity-discovery.md]
    path: skills/fleet-orchestrator/SKILL.md
    lines: "142"
    excerpt: |-
      its ready buffer is at least the greater of one ticket or its current lane count
    finding: "ORCH-R20 and the Start bullet say 'current reachable lane count'. With 2 reachable and 2 unreachable lanes and 3 ready tickets the spec starts discovery and the skill reading (4 lanes) does not."
  - fnd: FND-003
    severity: low
    confidence: high
    method: code-review
    check: code-bug
    artifact_id: skills/fleet-orchestrator/SKILL.md
    related_ids: [ORCH]
    path: skills/fleet-orchestrator/SKILL.md
    lines: "11"
    excerpt: |-
      fleet-orchestrator is the orchestrator role of the [orchestrator role spec](https://github.com/agent-ix/dev-team/blob/main/spec/roles/orchestrator.md), version 5.
    finding: "Frontmatter says role_spec_version 6 and the body says version 5, so a reader or evaluator gets two versions for one skill."
  - fnd: FND-004
    severity: low
    confidence: high
    method: code-review
    check: code-bug
    artifact_id: skills/fleet-orchestrator/references/ownership.md
    related_ids: [ORCH]
    path: skills/fleet-orchestrator/references/ownership.md
    lines: "19"
    excerpt: |-
      Source: the Ownership section of the orchestrator role spec, version 5.
    finding: "The spec is at version 6 after this PR and this reference still names version 5."
    outside_diff_failure: "At head bcbaf7f, grep 'version 5' returns ownership.md:19 while spec/roles/orchestrator.md frontmatter reads version: 6."
bindings: []
```

+++
