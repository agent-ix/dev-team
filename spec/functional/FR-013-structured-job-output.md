---
id: FR-013
title: Return a structured job summary and index logs by job id
type: FR
relationships:
  - target: ix://agent-ix/dev-team/US-003
    type: satisfies
  - target: ix://agent-ix/dev-team/FR-005
    type: depends_on
---
# FR-013: Return a structured job summary and index logs by job id

## Description

The scheduler SHALL return a bounded structured summary to the caller for every job, identified by a job id equal to the FR-005 request id. Full logs are stored and indexed by job id and read through bounded queries, so an agent does not tail raw logs.

## Behavior

On completion `run` prints one JSON summary and exits with the child's status per FR-005. The summary is defined here, not by any script. Fields: `job_id`, `host`, `repo`, `commit`, `class`, `lane`, `ticket`, `queue_wait_s`, `run_s`, `paused_s`, `slot`, `outcome`, `exit_code` or `signal`, `termination_reason`, `log_path`, `truncated`, `parse` (`ok` or `unavailable`), and for cargo commands a `cargo` object:

| Field | Extraction rule on the job's combined output |
|---|---|
| `test_results[]` | Every line matching `test result: (ok\|FAILED). N passed; M failed; K ignored` yields counts and status |
| `failing_tests[]` | Names from lines matching `test <name> ... FAILED`, first 12, in output order |
| `first_panic` | First `thread '<thread>' panicked at <file>:<line>:<col>:` and the following message line |
| `first_error` | First rustc diagnostic `error[<code>]: <message>` or `error: <message>` (excluding `error: could not compile` and `error: test failed` summary lines) with the `--> <file>:<line>:<col>` line that follows |
| `warnings` | Count of lines matching `warning: ` diagnostics |
| `watchdog_kills[]` | Abort or `rss_cap` terminations in this job from [FR-010](FR-010-scheduler-owned-throttling.md) |

The summary is at most 4 KiB; excess content is dropped from lists with `truncated` set. It contains no environment values or command secrets. A parity fixture set committed with the tool holds captured cargo outputs, including one captured from the retired remote runner's logs, each with its expected summary JSON; these fixtures remain the oracle after any script is deleted.

Logs are kept per job under the state directory with an index (job id, time, size, outcome). `log <job>` returns a bounded excerpt: `--failing`, `--test NAME`, `--grep`, `--range`, each with a line limit (default 80). The raw log is streamed only with `--raw`. Retention is by age and total size; pruning removes logs but keeps the index row and summary. A job still running reports `running` with elapsed time. When parsing fails the summary has `parse: unavailable` with the exit code and log path, never a guessed result.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-013-AC-1 | For each committed parity fixture (cargo test with failures, a panic, a compile error, a clean run, and the captured retired-runner log), the summary equals the fixture's expected JSON field by field using the extraction rules above. | Test |
| FR-013-AC-2 | A run with 100 000 log lines yields a summary of at most 4 KiB with `truncated` set when needed and no raw log text beyond `first_panic` and `first_error`. | Test |
| FR-013-AC-3 | `log <job> --test NAME` returns only that test's section within the line limit; an unknown job id returns a request error naming the id. | Test |
| FR-013-AC-4 | After log pruning, `result <job>` still returns the stored summary and the index row; `log <job>` reports `pruned`. | Test |
| FR-013-AC-5 | A non-cargo command or unparsable output yields exit code, outcome and `parse: unavailable`; a child killed by signal reports the signal. | Test |
| FR-013-AC-6 | A fixture whose environment holds a secret value produces no occurrence of that value in the summary, index or event output. | Test |

## Dependencies

- [FR-005](FR-005-fair-build-scheduler.md), request id, outcomes, redaction.
