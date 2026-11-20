---
id: SR-018
title: "code-review of SWM-175 cache lifecycle instructions"
type: SpecReview
analysis: code-review
scope: "agent-ix/dev-team; SWM-175; skills/coder/SKILL.md; skills/code-lead/SKILL.md; skills/code-lead/references/briefs.md; spec/; legacy source/test context"
review_set: subset
---

## Summary

Frozen source head: 96ed27bbd4e7a051d1f585dfd68d275dcc74dec7. Base: f6cc3fe00e343df6d47cedc0fd1245c7b465b1da. Ticket: SWM-175; PR: dev-team#26. Sole worktree: /Users/peter/dev/worktrees/dev-team-swm-175.

No applicable AssuranceProfile exists. Exact model ID is unavailable to this harness; recorded as unavailable, without guessing. No source edits, commits, pushes, cache cleanup or aggregate gate were performed by this reviewer.

## Verdict

**PASS for the bounded SWM-175 instruction acceptance scope.** No changed-behavior defect found. This is not a whole-repository assurance PASS.

Freeze → review → fix → disposition → final gate retains the same named private worktree cache. The coder and fix brief reuse it and report its path; lead closeout owns destruction after merge or an explicit recorded abandonment/resource-policy decision. Priority-goal worker retention remains in force. Disk checks use the build filesystem and configured reserve/source/age; unknown policy blocks dependent admission while independent work continues under the existing brief. No new user-permission flow or manual ledger is introduced. Focused checks, exact-head aggregate ownership, current review policy, scoped spec-gap routing, pin discipline and merge safeguards are retained. No second requirement definition, runtime helper, gate, package or release change is introduced.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |

## Examined Scope

```yaml
{
  "scope": [
    {
      "id": "coder-admission",
      "path": "skills/coder/SKILL.md",
      "role": "examined",
      "excerpt": "5. Before build admission, measure free space on the build dir's filesystem\n   (`df -h <worktree>`) and compare it with the current configured host disk\n   reserve. Record the measurement and policy source and age from the brief or\n   verified host config. Missing or stale reserve policy stays unknown: report\n   it to the leader; do not invent a universal floor or assume admission. If\n   space is below reserve, tell the leader for an explicit cleanup/admission\n   decision. Never delete another lane's cache."
    },
    {
      "id": "coder-cache-retention",
      "path": "skills/coder/SKILL.md",
      "role": "examined",
      "excerpt": "3. Retain the worktree and its named private build cache (`target/`,\n   `*-target/`, or `node_modules/`) through review, fix rounds and the leader's\n   final aggregate gate. PR freeze and review handback are not ticket\n   completion. Reuse this one cache; do not create another target directory.\n   The leader owns cleanup after merge, or after an explicit abandonment or\n   resource-policy decision recorded for this ticket. Never delete another\n   lane's cache."
    },
    {
      "id": "coder-cache-handoff",
      "path": "skills/coder/SKILL.md",
      "role": "examined",
      "excerpt": "- Retained worktree and private build-cache path (or no cache needed)"
    },
    {
      "id": "coder-fix-cache",
      "path": "skills/coder/SKILL.md",
      "role": "examined",
      "excerpt": "- Reuse the retained private cache in the same worktree. Freeze and report\n  again after the fix; leave cleanup to the leader under step 4."
    },
    {
      "id": "lead-freeze",
      "path": "skills/code-lead/SKILL.md",
      "role": "examined",
      "excerpt": "4. **Freeze:** the coder opens the PR. Nothing changes on the branch until\n   review returns. Retain its sole worktree and named private cache through\n   review, fix rounds and the final aggregate gate; freeze is not completion."
    },
    {
      "id": "lead-closeout",
      "path": "skills/code-lead/SKILL.md",
      "role": "examined",
      "excerpt": "After merge, the lead owns\n    removing this ticket's worktree and private build cache. Earlier cleanup\n    requires an explicit abandonment or resource-policy decision recorded for\n    this ticket; compare measured free space with the current configured host\n    reserve and record its source and age. Missing or stale policy stays\n    unknown; do not invent a universal floor. Never delete another lane's\n    cache. Update the state record. Report the merged slice to the planner."
    },
    {
      "id": "lead-efficiency-cache",
      "path": "skills/code-lead/SKILL.md",
      "role": "examined",
      "excerpt": "- **One target dir per worktree** (`<worktree>/target`, named in every brief);\n  a shared dir gives false failures. Retain that cache through review, fixes\n  and the lead's final gate, including for retained priority-goal workers.\n  The lead owns cleanup under closeout; a coder's handback is not cleanup."
    },
    {
      "id": "brief-admission",
      "path": "skills/code-lead/references/briefs.md",
      "role": "examined",
      "excerpt": "- Current lane/build capacity source and age, applicable admission policy,\n  configured host disk reserve and its source and age, and spec-gap owner\n  route. Compare measured free space on the build dir's filesystem with that\n  reserve before admission; missing or stale policy stays unknown and goes to\n  the lead for a decision. Do not invent a universal disk floor or paste a\n  fixed slot count, old toolchain notice\n  or another team's tracker destination from stale `coder-rules.md`."
    },
    {
      "id": "brief-cache-final-gate",
      "path": "skills/code-lead/references/briefs.md",
      "role": "examined",
      "excerpt": "- Its own build dir inside the worktree, never a shared one (for Rust,\n  `CARGO_TARGET_DIR=<worktree>/target`, covered by the repo's `.gitignore`). A\n  gate log built on a shared target dir is not evidence. Retain this same\n  private cache through freeze, review, fix rounds and the lead's final gate;\n  do not create a second target. The lead checks measured free space against\n  the current configured reserve before the final gate too."
    },
    {
      "id": "brief-cache-handoff",
      "path": "skills/code-lead/references/briefs.md",
      "role": "examined",
      "excerpt": "- PR freeze, review handback and a fix-round report are not ticket completion.\n  Leave the worktree and private cache for the lead, including while retained\n  on a priority-goal PR. The lead owns cleanup after merge or an explicit\n  abandonment/resource-policy decision recorded for this ticket. Never delete\n  another lane's cache. End with a report in this shape:"
    },
    {
      "id": "brief-fix-cache",
      "path": "skills/code-lead/references/briefs.md",
      "role": "examined",
      "excerpt": "- Reuse the ticket's retained private cache in its sole worktree; retain it\n  again at handback for disposition and the lead's final gate."
    },
    {
      "id": "independent-work",
      "path": "skills/code-lead/references/briefs.md",
      "role": "examined",
      "excerpt": "- If something is missing or unclear, say so in the report instead of guessing.\n  Questions go in the report too; keep working on everything that doesn't\n  depend on the answer."
    },
    {
      "id": "capacity-resources",
      "path": "docs/department-monitoring.md",
      "role": "context_only",
      "excerpt": "| Capacity/resources | `host_slots_used`, `host_slots_free`: occupied units and max(0, capacity-used) per host at end; `host_overcommit_units`: max(0, used-capacity); `queue_wait_minutes`: request start-enqueue for starts in window plus current ages for queued requests, separately labeled; `lock_hold_minutes`: end-start for finishes in window plus current ages for running requests, separately labeled | Scheduler events/verified live/config capacity; no wrapper-count heuristic is presented as a lease count | Build-tool/host owner: fair queue, bound holds and recover suspect leases |"
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
    }
  ]
}
```

## Verification

Independent git diff --check against the supplied base passed (exit 0), and sh skills/code-lead/tests/team-gate-test.sh passed all 21 checks (exit 0). Logs: /Users/peter/dev/.dev-dept-recovery/swm-175/code-review/diff-check.log and /Users/peter/dev/.dev-dept-recovery/swm-175/code-review/team-gate-test.log. Three Markdown instruction files changed, 47 additions and 11 deletions; all 14 role skills remain. Spec, tests, reviewer guidance, versions and metadata are unchanged. No new test merely mirrors prose.

## Coverage

Language-independent duplication, integrity, spec-code faithfulness and test-alignment checks ran over the changed instructions. No applicable Rust/React/Python lane; no spec/plan change. The gap-analysis companion records the actual computed repository baseline and its limits. No aggregate gate ran.
