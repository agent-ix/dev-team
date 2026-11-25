<!-- reviewer-dispositions repo=agent-ix/dev-team visibility=public quoin=0.36.10 module=spec-artifacts-process@v0.29.2 id=SR-045 round=2 model=claude-sonnet-5-5 run=E3197189-E9ED-4055-BF94-14E39A754DE9 -->

Head reviewed: `d1023710e636c65dcabf7f7235edc8d1215bd05b`.

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | FR-009 now permits the transitional capacity_units read; residual defects are in SR-051 |

+++ [reviewer data]

```yaml
head: d1023710e636c65dcabf7f7235edc8d1215bd05b
dispositions:
  - fnd: FND-001
    outcome: fixed
    after_excerpt: |-
      The TOML profile is the target source of host limits. Until the SWM-239 TOML profile exists, `ix_build_slots_configured` is read from the `capacity_units` field in the locked-build per-host JSON host policy. This is a metrics-only transitional read: it does not supply or derive a sustainable slot value.
```

+++
