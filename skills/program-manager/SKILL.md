---
name: program-manager
description: Start or attach to a program team and coordinate its recurring checks with ix-board cadence and the existing team skills.
version: 0.1.0
---

# Program Manager

Start with `/program-manager <program>`. Resolve its Linear team, attach to the
planner, code lead, and minder, and use `/team-minder <team>` for lane work.
Run `ix-board cadence due --program <program> --team <team>` at each wake.

- **Exit 0:** nothing is due. Check current program status and finish this wake.
- **Exit 1:** run each listed due job with `ix-board cadence run <job-id>`.
- **Exit 2:** run each listed due or overdue job the same way, and call out
  overdue jobs or a missing cadence checker as blockers.

Use `/team-retro <team>` for the retro review and `/department-health <team>`
for the health review. Keep the program's next wake externally scheduled; this
skill does not create a session loop.
