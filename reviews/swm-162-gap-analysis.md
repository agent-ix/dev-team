---
id: SR-015
title: bounded acceptance inspection of department role skills
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/dev-team; SWM-162; PR dev-team#25 at f97ca523a4f0f85fda7aa6e2566dfb5a24acbe95; changed skills, metadata and external local-rule proposal"
review_set: subset
---

## Summary

Ticket: SWM-162. Reviewed source head: f97ca523a4f0f85fda7aa6e2566dfb5a24acbe95. Review of department role safeguards, deterministic interpretation, packaging, and the separately proposed local coder rules.

## Verdict

**PASS** for the requested instruction-level acceptance scope at the frozen source head and revised external proposal. Every FR-003 inspection scenario is supported: remote/login/worker reconciliation; acknowledgement/confirmation; planner pre-send/end-tick audit; focused gate/capacity/scoped routing; pin/window/current review policy; and deterministic retro/health with explicit unavailable output. This is not a repository assurance verdict.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | low | No findings (placeholder) | - |

## Examined Scope

```yaml
{
  "scope": [
    {
      "id": "FR-003-AC-1",
      "path": "spec/functional/FR-003-role-safeguards.md",
      "role": "examined",
      "excerpt": "A minder scenario with a login screen, an omitted remote lane, recently finished nested workers and queued mail requires pane lifecycle/PR-worktree/token reconciliation; neither live_subagents nor relay seen is accepted as liveness proof."
    },
    {
      "id": "FR-003-AC-2",
      "path": "spec/functional/FR-003-role-safeguards.md",
      "role": "examined",
      "excerpt": "An order unacknowledged beyond its configured acknowledgement deadline receives an owned escalation in the current observation tick; each order records confirmed by pane, PR head or SHA, or explicitly unconfirmed. Queued messages are not blindly resent."
    },
    {
      "id": "FR-003-AC-3",
      "path": "spec/functional/FR-003-role-safeguards.md",
      "role": "examined",
      "excerpt": "Planner instructions require pre-send evidence, authorized scope, plan membership, prior-order/changed-evidence and batch checks; end-tick audit records ad hoc assignments, out-of-scope conscription and excess messages. The planner rubric consumes their deterministic counts with cited judgment."
    },
    {
      "id": "FR-003-AC-4",
      "path": "spec/functional/FR-003-role-safeguards.md",
      "role": "examined",
      "excerpt": "Lead/coder guidance requires focused crate checks during iteration, one lead-run aggregate gate at final head, capacity from config/live state, scoped spec-gap routing and no stale toolchain notice. Gated or stale claims are reconciled to the team's configured ready state when active work is absent."
    },
    {
      "id": "FR-003-AC-5",
      "path": "spec/functional/FR-003-role-safeguards.md",
      "role": "examined",
      "excerpt": "Lead pin guidance folds required dependency pins into the consuming PR, names a pin owner/window and forbids repin-only PRs; review rounds use explicit current policy rather than an invented cap or automatic unsafe merge."
    },
    {
      "id": "FR-003-AC-6",
      "path": "spec/functional/FR-003-role-safeguards.md",
      "role": "examined",
      "excerpt": "Retro and department-health instructions interpret ix-board values and route actions; no prose asks the agent to invent deterministic metrics, infer unavailable evidence as zero, hardcode slots, or conscript another lane. Unshipped commands are reported unavailable."
    },
    {
      "id": "local-coder-rules-revised",
      "path": "/tmp/swm-162-coder-rules.md",
      "role": "examined",
      "excerpt": "The lead runs the final gate in that same ticket directory with the same ticket target directory; no separate integration or gate directory is created or used."
    }
  ]
}
```

## Coverage

Independent metadata/path assertions passed: all release manifests 0.4.0, fourteen indexed skill paths resolve, lifecycle WAITING/RECENT/unknown guidance retained. Claude plugin validation and git diff --check passed; existing missing-icon warning is unchanged. Supplied focused pytest log records eleven tests passing. No new mirror-the-prose tests or test suppression. Docs structure/Vale logs match the inherited eight prose findings; no new diff-level docs finding. No aggregate gate ran.

Computed quire matrix --scope /Users/peter/dev/worktrees/dev-team-swm-162 --strict --format json exits 1: 26 untagged criteria and six design gaps across the new cross-repository contract, plus the reported optional NFR-section diagnostic. These include unimplemented collectors/TUI/scheduler owned by other tickets. FR-003 is six Inspection criteria; this brief requests bounded instruction acceptance inspection, not repository-wide test assurance. The changed instruction behavior is inspected below; no full-repository gap PASS, test coverage completeness or historical incident replay is claimed. Optional semantic audit was not run. Plan completion: not assessed.

Sanitized pilot and independent team identifiers were walked through as instruction inspections, not runtime corpus replay. The revised local proposal removes fixed slot/job/checkout-floor claims, stale lane routing and duplicate workspace sweeps while retaining legacy admission until explicit reviewed activation. Revised proposal SHA256 c00a3a22fd79831e88d31c237583672fa774d64ac820a47c7db941636edd6ec2. The initial separate gate-directory exception is recorded in SR-014 and its disposition, not hidden here.
