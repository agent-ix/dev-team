---
id: SR-019
title: "gap-analysis of SWM-175 cache lifecycle instructions"
type: SpecReview
analysis: gap-analysis
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
      "id": "FR-001-AC-1",
      "path": "spec/functional/FR-001-evidence-contract.md",
      "role": "context_only",
      "excerpt": "A report from two configured teams contains their separate populations and one deduplicated department rollup; no out-of-scope issue or remote lane is silently included."
    },
    {
      "id": "FR-001-AC-2",
      "path": "spec/functional/FR-001-evidence-contract.md",
      "role": "context_only",
      "excerpt": "Removing a required page, host, source timestamp or capacity config makes dependent values null/unavailable with source and reason; unaffected values remain visible and no unavailable class is green."
    },
    {
      "id": "FR-001-AC-3",
      "path": "spec/functional/FR-001-evidence-contract.md",
      "role": "context_only",
      "excerpt": "Every value exposes metric ID/version, scope, observation/window timestamps, unit, population/denominator, source references, query/config identity and status; classified events also expose attribution and classification version."
    },
    {
      "id": "FR-001-AC-4",
      "path": "spec/functional/FR-001-evidence-contract.md",
      "role": "context_only",
      "excerpt": "A relay enqueue does not count as delivery or acknowledgement; an ambiguous pane/session association is unknown rather than assigned to the focused pane."
    },
    {
      "id": "FR-001-AC-5",
      "path": "spec/functional/FR-001-evidence-contract.md",
      "role": "context_only",
      "excerpt": "An existing metric fixture produces unchanged values after catalog extension; changed formulas use a new metric ID."
    },
    {
      "id": "FR-002-AC-1",
      "path": "spec/functional/FR-002-deterministic-metrics.md",
      "role": "context_only",
      "excerpt": "Fixed fixtures compute every catalog entry with exact expected count, age, ratio or nearest-rank duration percentile; replaying the same evidence and clock yields identical metric payloads."
    },
    {
      "id": "FR-002-AC-2",
      "path": "spec/functional/FR-002-deterministic-metrics.md",
      "role": "context_only",
      "excerpt": "Boundary fixtures on either side of configured stale, repin-window, WIP, wait, hold, refusal and message thresholds produce the documented assessment; absent thresholds produce unassessed values, never green."
    },
    {
      "id": "FR-002-AC-3",
      "path": "spec/functional/FR-002-deterministic-metrics.md",
      "role": "context_only",
      "excerpt": "Tag→repin, state-bounce and reversed-order fixtures emit the exact matching event IDs and participants once per qualifying sequence; duplicate events, legitimate new evidence and unrelated entities do not create a loop."
    },
    {
      "id": "FR-002-AC-4",
      "path": "spec/functional/FR-002-deterministic-metrics.md",
      "role": "context_only",
      "excerpt": "Missing state history, truncated relations, unknown message classification and an unavailable remote host make the corresponding metrics unavailable without lowering counts or denominators."
    },
    {
      "id": "FR-002-AC-5",
      "path": "spec/functional/FR-002-deterministic-metrics.md",
      "role": "context_only",
      "excerpt": "Previous/baseline comparisons include absolute changes and direction; incompatible query/config/catalog identity emits query_changed. Empty and singleton duration populations follow the catalog rules."
    },
    {
      "id": "FR-002-AC-6",
      "path": "spec/functional/FR-002-deterministic-metrics.md",
      "role": "context_only",
      "excerpt": "A department scorecard lists all ten problem classes, source age, available trend, threshold and one configured owner/action for each red; missing owner configuration is visible as unrouted rather than guessed."
    },
    {
      "id": "FR-002-AC-7",
      "path": "spec/functional/FR-002-deterministic-metrics.md",
      "role": "context_only",
      "excerpt": "A newly started claim without movement is excluded from claims_without_movement until its latest start/claim age exceeds the configured stale interval. An older claim without subsequent movement counts; recent movement or a restarted claim excludes it; missing claim history makes the metric unavailable."
    },
    {
      "id": "FR-002-AC-8",
      "path": "spec/functional/FR-002-deterministic-metrics.md",
      "role": "context_only",
      "excerpt": "Required metric mixes red+unknown and amber+unknown produce red and amber with complete=false and missing IDs; green+unknown produces unknown; all-green produces green with complete=true; an empty required set produces unknown. Optional metric statuses do not alter these results."
    },
    {
      "id": "FR-003-AC-1",
      "path": "spec/functional/FR-003-role-safeguards.md",
      "role": "context_only",
      "excerpt": "A minder scenario with a login screen, an omitted remote lane, recently finished nested workers and queued mail requires pane lifecycle/PR-worktree/token reconciliation; neither live_subagents nor relay seen is accepted as liveness proof."
    },
    {
      "id": "FR-003-AC-2",
      "path": "spec/functional/FR-003-role-safeguards.md",
      "role": "context_only",
      "excerpt": "An order unacknowledged beyond its configured acknowledgement deadline receives an owned escalation in the current observation tick; each order records confirmed by pane, PR head or SHA, or explicitly unconfirmed. Queued messages are not blindly resent."
    },
    {
      "id": "FR-003-AC-3",
      "path": "spec/functional/FR-003-role-safeguards.md",
      "role": "context_only",
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
      "role": "context_only",
      "excerpt": "Retro and department-health instructions interpret ix-board values and route actions; no prose asks the agent to invent deterministic metrics, infer unavailable evidence as zero, hardcode slots, or conscript another lane. Unshipped commands are reported unavailable."
    },
    {
      "id": "FR-004-AC-1",
      "path": "spec/functional/FR-004-terminal-views.md",
      "role": "context_only",
      "excerpt": "Given the same versioned model, TUI and JSON show matching statuses, values, evidence and actions; the model can be rendered without terminal initialization for a later plugin/desktop consumer."
    },
    {
      "id": "FR-004-AC-2",
      "path": "spec/functional/FR-004-terminal-views.md",
      "role": "context_only",
      "excerpt": "Status/health/retro switch by keyboard, preserve selected scope and show source age/unavailable diagnostics within an 80×24 terminal without hidden fatal errors; quit restores the terminal."
    },
    {
      "id": "FR-004-AC-3",
      "path": "spec/functional/FR-004-terminal-views.md",
      "role": "context_only",
      "excerpt": "With LINEAR_API_KEY unset and a valid saved credential, a scoped TUI starts without exposing credentials; missing auth produces an actionable diagnostic and a nonzero live-collection status, while a supplied offline report remains readable."
    },
    {
      "id": "FR-004-AC-4",
      "path": "spec/functional/FR-004-terminal-views.md",
      "role": "context_only",
      "excerpt": "Missing or ambiguous native pane identity permits an explicit project/team/offline report; no nearby session is guessed. An unreachable host and relation-page failure remain visible partial results."
    },
    {
      "id": "FR-004-AC-5",
      "path": "spec/functional/FR-004-terminal-views.md",
      "role": "context_only",
      "excerpt": "Existing dashboard startup/binding/credential tickets are linked and reused; reported-only failures are labeled reported until independently reproduced."
    },
    {
      "id": "FR-005-AC-1",
      "path": "spec/functional/FR-005-fair-build-scheduler.md",
      "role": "context_only",
      "excerpt": "Equal-priority eligible requests run in enqueue order; repeated high-priority arrivals cannot pass an eligible request after its configured reservation threshold. A deterministic-clock test proves this under sustained arrivals."
    },
    {
      "id": "FR-005-AC-2",
      "path": "spec/functional/FR-005-fair-build-scheduler.md",
      "role": "context_only",
      "excerpt": "Higher-priority waiting work gets the next available capacity before aging reservation, while an already running child continues; no new grant exceeds current capacity or duplicates leased units. If capacity shrinks from two units to one while two units are running, both continue, overcommit is reported, and new admission waits for sufficient release."
    },
    {
      "id": "FR-005-AC-3",
      "path": "spec/functional/FR-005-fair-build-scheduler.md",
      "role": "context_only",
      "excerpt": "Capacity shrink/growth, unavailable/stale host telemetry, insufficient disk reserve and oversized requests follow the defined admission behavior without a hardcoded slot count."
    },
    {
      "id": "FR-005-AC-4",
      "path": "spec/functional/FR-005-fair-build-scheduler.md",
      "role": "context_only",
      "excerpt": "Timeout, cancellation, child crash, scheduler restart, stale heartbeat and PID-reuse fixtures reclaim leases only after verified termination of the owned child group; unrelated children are never terminated."
    },
    {
      "id": "FR-005-AC-5",
      "path": "spec/functional/FR-005-fair-build-scheduler.md",
      "role": "context_only",
      "excerpt": "Each queued/running request exposes wait/hold age, owner, resource units, host capacity and termination reason through JSON events consumed by ix-board; enqueue/start/end calculations match the actual transitions."
    },
    {
      "id": "FR-005-AC-6",
      "path": "spec/functional/FR-005-fair-build-scheduler.md",
      "role": "context_only",
      "excerpt": "Logic is Rust in a shared tool with a thin Make invocation; consumers migrate from project wrappers rather than copying shell/Python arbitration into Rust repositories."
    },
    {
      "id": "FR-005-AC-7",
      "path": "spec/functional/FR-005-fair-build-scheduler.md",
      "role": "context_only",
      "excerpt": "A child returning 75 is invoked once and its status is propagated; a signaled child returns non-success. Neither outcome re-enters acquisition contention or silently reruns the build."
    },
    {
      "id": "FR-005-AC-8",
      "path": "spec/functional/FR-005-fair-build-scheduler.md",
      "role": "context_only",
      "excerpt": "On a host with total capacity two units, a queued two-unit request reaches the reservation threshold while one-unit jobs keep arriving. The request is reservation-eligible even with fewer than two free units; no newer job consumes subsequently released units, and the reserved request starts after both units are free."
    }
  ]
}
```

## Verification

Independent git diff --check against the supplied base passed (exit 0), and sh skills/code-lead/tests/team-gate-test.sh passed all 21 checks (exit 0). Logs: /Users/peter/dev/.dev-dept-recovery/swm-175/code-review/diff-check.log and /Users/peter/dev/.dev-dept-recovery/swm-175/code-review/team-gate-test.log. Three Markdown instruction files changed, 47 additions and 11 deletions; all 14 role skills remain. Spec, tests, reviewer guidance, versions and metadata are unchanged. No new test merely mirrors prose.

## Coverage

Actual quoin:gap-analysis procedures ran: target selection, computed matrix, coverage diagnostics, reverse behavior inventory, stub/test-oracle inspection, artifact authoring and validation. No invented quoin gap-analysis command was used. Repository root is the worktree above; spec root is spec/; the root has org agent-ix, name dev-team, and no document ID. URI prefix: ix://agent-ix/dev-team. Mode: planless.

Reconciliation: quoin matrix (quoin 0.36.7; quire 0.52.0 / engine 0.62.2), exit 0. Counts: tagged 0, untagged 26, tagged-by-ignored-test 0, method-without-symbol 9, qualified-record 0, retired 0. All 35 criteria have no run evidence. FR-003-AC-4 and AC-5 are Inspection and correctly require no source-test symbol. No source-test binding for those criteria is claimed. quire coverage also exited 0; untracked_symbols is empty.

The repository baseline cannot receive a full gap-audit PASS: FR-001 AC1–5, FR-002 AC1–8, FR-004 AC1–4, FR-005 AC1–5/7/8 and NFR-001 M1–2 are untagged. These are unchanged cross-repository collector, metric, terminal and scheduler obligations, not newly missing SWM-175 tests. Coverage additionally reports the inherited NFR Acceptance Criteria selector mismatch, absent StR/TestMatrix archetypes, Python pytest-marker-only binding with 11 examined/zero bound symbols despite legacy Trace docstrings, and hollow-denominator diagnostics. No green coverage ratio is inferred. Spec, module configuration, legacy renderer and tests are unchanged from base; these existing limitations are disclosed here rather than expanded into out-of-scope repairs.

Reverse inventory: 14 role skill entry points, one program-review HTML renderer CLI (input plus --output), and the existing team-gate gate/repin wrapper. Role behavior maps to FR-003 and the role contract; new cache/admission instructions refine existing FR-003-AC-4 and capacity/resources ownership. The legacy renderer and wrapper predate the department spec and are not fully bound to its current model. Their legacy source/test obligations remain a repository assurance limitation, not a newly introduced untraced SWM-175 surface. Source/test stub inspection found zero new source stubs, test stubs or coverage suppression; the existing 11 renderer tests contain behavioral assertions and the gate-wrapper suite checks observable exit/log behavior. No runtime source or tests changed, and no runtime-wide correctness claim is made.

Plan completion: not assessed

Semantic review: skipped; optional repository-wide semantic audit was not requested. Acceptance instruction inspection is recorded above, not represented as that optional audit.

Rust/React/Python language review lanes are inapplicable to this Markdown-only diff. Spec-review/sub-analyses are inapplicable: no spec or plan changes. Final aggregate gate and merge remain lead-owned.
