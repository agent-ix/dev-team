---
id: SR-002
title: "Code review — SWM-110 team-minder structured status replies"
type: SpecReview
analysis: code-review
scope: "agent-ix/dev-team@a6aa1c5c185fea03c6b15a03235b9083f4ee6231; skills/team-minder/SKILL.md, Linear SWM-110 acceptance"
review_set: subset
---

## Summary

Reviewed dev-team PR #14 at `a6aa1c5c185fea03c6b15a03235b9083f4ee6231` against both SWM-110 acceptance criteria and the current SWM-107/109 relay contract. The instructions cover the required fields and blocker identifiers, but leave a required capacity value without a usable source or unknown representation.

## Verdict

**CONDITIONAL** — one medium finding prevents the skill from answering every status request when spare coder capacity cannot be established.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | Spare coder slots have no defined source or unknown representation, so the required reply can be left unanswered | skills/team-minder/SKILL.md:92 |

## Details

`agent-msg status-reply` requires `--spare-coder-slots` as a numeric argument; the current SWM-107 implementation uses a required `u32` field. SWM-109's explicit server-capacity record contains cores, RAM, optional maximum agents, and owner rules; it does not define free coder slots. The skill says to tell the requester when capacity cannot be established and not invent a number, but the reply schema has no unknown value and no alternative way to store that missing-field response. This does not satisfy SWM-110's requirement to fill every form field for that case. A contract or source that produces spare coder slot counts, or a supported unknown representation and submission path, is needed.

Review scope was the two SWM-110 acceptance bullets and the new `Answer a status-request` section in `skills/team-minder/SKILL.md`. The change is Markdown-only: Rust and React review lanes were skipped, and gap-analysis was skipped because no production code, spec, or plan changed. No repository gate applies to this skill Markdown.

## Checks

- Confirmed PR #14 live head is `a6aa1c5c185fea03c6b15a03235b9083f4ee6231` and diff is limited to `skills/team-minder/SKILL.md`.
- Read SWM-110 acceptance criteria from Linear.
- Compared the reply arguments with SWM-107 PR #26 head `2759e250dc5d2f754cde208684689a3adfdb8649` and its `StatusReplyArgs` implementation, and compared capacity semantics with SWM-109's `ServerCapacity` implementation.
- No tests run; this change contains documentation only.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | still-open | The new skill text claims that omitting `--spare-coder-slots` stores JSON null, but ix-relay PR #26's current live head `2759e250dc5d2f754cde208684689a3adfdb8649` still has required `spare_coder_slots: u32` in `crates/agent-msg/src/status_request.rs:35` and stores a required `u16` in `crates/relay-core/src/status.rs:134`. The separate worktree contains uncommitted `Option` changes; they are not part of the live PR head and do not verify the documented behavior. |
| FND-001 | fixed | `skills/team-minder/SKILL.md` now says to omit `--spare-coder-slots` without a numeric source, submit with unknown capacity, and interpret JSON `null` as unknown. ix-relay PR #26 head `1b21e665673f0213469713a485b01634b597b9ef` makes the CLI field optional and the stored field `Option<u16>`; its `program_review` test asserts omitted capacity serializes as JSON null and explicit `2` remains numeric. |

## Reconciliation with merged ix-relay FR-056

The preceding `fixed` disposition records a proposal that conflicts with the
later merged contract and is not valid evidence of SWM-110 completion. Merged
ix-relay FR-056 requires `spare_coder_slots` as an integer from 0 through
65535, and requires the argument rather than allowing omission or JSON `null`.
The null/`Option` proposal is therefore rejected. The team-minder instructions
now require an explicit numeric count: when no trusted numeric source exists,
the minder asks the requesting lead or owner for the exact count and submits
only after receiving it. If the count cannot be obtained, the reply remains
pending and no malformed or false-success reply is submitted.
