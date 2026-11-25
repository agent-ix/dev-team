<!-- reviewer repo=agent-ix/dev-team visibility=public quoin=0.36.10 module=spec-artifacts-process@v0.29.2 id=SR-059 method=spec-review/base lang=spec pr=dev-team#44 head=bcbaf7fc20497e47aa7b99b4b1ba2a05b6363786 model=claude-sonnet-5-5 run=F6E0DDBD-15F0-4124-9B44-74919A6C0E91 -->

Head reviewed bcbaf7f. Verdict CONDITIONAL. Not mergeable.

| ID      | Severity | Summary |
| ------- | -------- | ------- |
| FND-001 | medium   | ORCH-R20 requires discovery whenever demand covers an unrecorded host, with no exception for an open run or the daily cap. A host whose 2 runs today ended inconclusive_no_demand still has no level and has demand, so ORCH-R20 requires a third run that ORCH-R24 forbids. ORCH-R20-E1 (value 0) also counts samples taken during a run opened more than 10 minutes earlier, which demand coverage now makes the normal case. |
| FND-002 | low      | The ORCH-R27 note says an unrecorded host waits for demand "to cover its current lanes". It omits the one-ticket floor and the registry lease, so a zero-lane host reads as covered with an empty buffer. |

+++ [reviewer data]

```yaml
clean: false
scope:
  - {id: ORCH-R20, path: spec/roles/orchestrator.md, role: examined, excerpt: "A host with no recorded level SHALL be put into discovery when its registry lease is current, its ready buffer is at least the greater of one ticket or its current reachable lane count, and the capacity history is available to record the run; a positive target-buffer deficit does not prevent discovery."}
  - {id: ORCH-R20-E1, path: spec/roles/orchestrator.md, role: examined, excerpt: "| ORCH-R20-E1 | ORCH-R20 | ledger | ledger.unrecorded_hosts_with_demand | deterministic | ledger.unrecorded_hosts_without_discovery_run | evaluator | = | 0 | hosts | daily |"}
  - {id: ORCH-R27, path: spec/roles/orchestrator.md, role: examined, excerpt: "ORCH-R27 is `n.a.` for a host until its level is recorded: before that the host waits for ready-buffer demand to cover its current lanes or is in discovery (ORCH-R20)"}
  - {id: rubric-orchestrator, path: spec/rubrics/rubric-orchestrator.md, role: examined, excerpt: "A judgement evaluation cites one check as `rubric-orchestrator@2#<check-slug>`."}
  - {id: ORCH-R24, path: spec/roles/orchestrator.md, role: context_only, excerpt: "The orchestrator SHALL NOT start more than 2 discovery runs of one host per day, first runs and re-discoveries counted together."}
findings:
  - fnd: FND-001
    severity: medium
    confidence: high
    method: spec-review/base
    check: soundness
    artifact_id: ORCH-R20
    related_ids: [ORCH-R24, ORCH-R28, ORCH-R20-E1, FR-041]
    path: spec/roles/orchestrator.md
    lines: "270"
    excerpt: |-
      A host with no recorded level SHALL be put into discovery when its registry lease is current, its ready buffer is at least the greater of one ticket or its current reachable lane count, and the capacity history is available to record the run; a positive target-buffer deficit does not prevent discovery.
    finding: "No exception for an open run or the daily cap: a host whose 2 runs today ended inconclusive_no_demand has no level and has demand, so R20 requires a third run that R24 forbids. ORCH-R20-E1 (value 0) also counts samples taken during a run opened over 10 minutes earlier (ix-board#102 view requires started_at within [sample, sample+600000 ms]), which demand coverage now makes the normal case."
  - fnd: FND-002
    severity: low
    confidence: high
    method: spec-review/base
    check: ambiguous
    artifact_id: ORCH-R27
    related_ids: [ORCH-R20]
    path: spec/roles/orchestrator.md
    lines: "389-391"
    excerpt: |-
      host waits for ready-buffer demand to cover its current lanes or is in discovery (ORCH-R20), and `fleet
    finding: "The note omits the one-ticket floor and the registry lease, so a zero-lane host reads as covered with an empty buffer."
bindings: []
```

+++
