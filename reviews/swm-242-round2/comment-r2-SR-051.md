<!-- reviewer-dispositions repo=agent-ix/dev-team visibility=public quoin=0.36.10 module=spec-artifacts-process@v0.29.2 id=SR-051 round=2 model=claude-sonnet-5-5 run=E3197189-E9ED-4055-BF94-14E39A754DE9 -->

Head reviewed: `d1023710e636c65dcabf7f7235edc8d1215bd05b`. SR-051 was SR-043 (renumbered; SR-042 is now SR-050) to clear a collision with dev-team main. 1 fixed, 6 new (2 high, 4 medium). Not mergeable.

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Source conflict resolved by the transitional read |
| FND-002 | still-open | New (high): pause series deleted while FR-010-AC-10 still requires pause seconds |
| FND-003 | still-open | New (high): closed reason set forbids reasons FR-010 still produces |
| FND-004 | still-open | New (medium): abort outcome coverage removed from every criterion |
| FND-005 | still-open | New (medium): AC-1 "applicable" is untestable and conflicts with zero-valued outcomes |
| FND-006 | still-open | New (medium): configured slots undefined after SWM-239 |
| FND-007 | still-open | New (medium): FR-009-AC-8 mixes interim and post-profile states |

+++ [reviewer data]

```yaml
head: d1023710e636c65dcabf7f7235edc8d1215bd05b
dispositions:
  - fnd: FND-001
    outcome: fixed
    after_excerpt: |-
      The TOML profile is the target source of host limits. Until the SWM-239 TOML profile exists, `ix_build_slots_configured` is read from the `capacity_units` field in the locked-build per-host JSON host policy. This is a metrics-only transitional read: it does not supply or derive a sustainable slot value.
  - fnd: FND-002
    outcome: still-open
    reason: "Found in round 2; no fix yet."
  - fnd: FND-003
    outcome: still-open
    reason: "Found in round 2; no fix yet."
  - fnd: FND-004
    outcome: still-open
    reason: "Found in round 2; no fix yet."
  - fnd: FND-005
    outcome: still-open
    reason: "Found in round 2; no fix yet."
  - fnd: FND-006
    outcome: still-open
    reason: "Found in round 2; no fix yet."
  - fnd: FND-007
    outcome: still-open
    reason: "Found in round 2; no fix yet."
new_findings:
  - fnd: FND-002
    severity: high
    confidence: high
    method: spec-review-base
    check: soundness
    artifact_id: FR-010-AC-10
    related_ids: [FR-015, FR-010, FR-041]
    path: spec/functional/FR-010-scheduler-owned-throttling.md
    lines: "60"
    excerpt: |-
      `hold` blocks admission with reason `operator` and a stored note until `resume`; running leases continue unless `--pause` is given; held seconds appear as pause seconds with reason `operator`; queued requests keep their age.
    finding: "The diff deletes ix_build_pause_seconds_total from FR-015 while unchanged FR-010 and FR-010-AC-10 still require held and paused time as pause seconds, and the orchestrator role, its rubric and ix-board FR-041 still name the series (ix-board: absent until its producer exists). FR-010-AC-10 held seconds have no exported series, and pause-blocked admission is measured by nothing."
  - fnd: FND-003
    severity: high
    confidence: high
    method: spec-review-base
    check: soundness
    artifact_id: FR-015-AC-12
    related_ids: [FR-015, FR-010, FR-009-AC-11]
    path: spec/functional/FR-015-build-metrics-export.md
    lines: "77"
    excerpt: |-
      Unsupported `operator`, `swap`, and `compressor` sources produce no series rather than zero-valued series.
    finding: "FR-015 closes the blocked reason set to four values and AC-12 requires no operator, swap or compressor series, while FR-010 requires operator holds and swap and compressor block_above refusals. The reason given is that this build has no producer, which states build state as a permanent requirement."
  - fnd: FND-004
    severity: medium
    confidence: high
    method: spec-review-base
    check: coverage
    artifact_id: FR-015-AC-8
    related_ids: [FR-015-AC-9, FR-015-AC-10, FR-041]
    path: spec/functional/FR-015-build-metrics-export.md
    lines: "73-75"
    excerpt: |-
      Abort outcomes are not exercised or claimed by this criterion.
    finding: "AC-8, AC-9 and AC-10 drop all abort coverage while the outcome table and mapping sentence still require aborted outcomes, so no criterion verifies the aborted_ values that ix-board FR-041 consumes. The remaining non-abort termination members include pause_exceeded."
  - fnd: FND-005
    severity: medium
    confidence: high
    method: spec-review-base
    check: untestable-ac
    artifact_id: FR-015-AC-1
    related_ids: [FR-015]
    path: spec/functional/FR-015-build-metrics-export.md
    lines: "66"
    excerpt: |-
      After a scripted sequence of queued, running and finished requests, every applicable series in the table appears with the expected value and labels, and `promtool check metrics` accepts the output. A metric with no source is omitted rather than exported as zero.
    finding: "AC-1 asks for every applicable series without defining applicable, so omitting any series can pass. Its rule that a metric with no source is omitted conflicts with the requirement to export every outcome from 0, including aborted values that have no producer."
  - fnd: FND-006
    severity: medium
    confidence: medium
    method: spec-review-base
    check: ambiguous
    artifact_id: FR-015-AC-2
    related_ids: [FR-015, FR-015-AC-12, FR-009]
    path: spec/functional/FR-015-build-metrics-export.md
    lines: "67"
    excerpt: |-
      `ix_build_slots_busy`, `ix_build_slots_configured` and `ix_build_slots_sustainable` match the snapshot's occupied units, the interim JSON host policy's `capacity_units` value until the SWM-239 TOML profile exists, and computed sustainable slot count at the same sample.
    finding: "ix_build_slots_configured is defined only until SWM-239. No TOML key or meaning replaces it (FR-009 has max_slots and computed sustainable slots), and AC-2 also requires a computed sustainable count that does not exist in the interim."
  - fnd: FND-007
    severity: medium
    confidence: medium
    method: spec-review-base
    check: compound
    artifact_id: FR-009-AC-8
    related_ids: [FR-009]
    path: spec/functional/FR-009-host-profile-sustainable-slots.md
    lines: "59"
    excerpt: |-
      A JSON host policy present at the legacy path does not affect sustainable slot calculation: the metric-only `ix_build_slots_configured` value is read from its `capacity_units` field until the SWM-239 TOML profile exists, while sustainable capacity is computed from TOML profile inputs and probes only. The legacy file is warned about, and no code path converts it.
    finding: "Rewritten FR-009-AC-8 mixes the interim and post-profile states: it computes sustainable capacity from a TOML profile while that profile does not exist, warns about the file that is in use, and no longer verifies that the JSON file stops being read once the profile exists."
```

+++
