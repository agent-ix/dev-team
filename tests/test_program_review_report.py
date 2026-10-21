"""Acceptance tests for the program-review HTML renderer."""

import json
import sys
from pathlib import Path

import pytest

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills" / "program-reviewer" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from render_report import render  # noqa: E402


FIXTURE = Path(__file__).parent / "fixtures" / "program-review-input.json"


class TestProgramReviewReport:
    """Tests that command evidence becomes one safe, responsive review artifact."""

    def test_renders_source_data_once_and_escapes_untrusted_values(self):
        """
        Description:
            Render a report from roadmap, chain, allocation, lead, and Linear JSON.
        Assumptions:
            The fixture contains duplicate project names and repeated ticket evidence.
        Criteria:
            The report has one row per project and blocking issue, includes command data,
            escapes source text, and resolves every template token.

        Trace: SWM-106-AC-1, SWM-106-AC-2
        """
        document = json.loads(FIXTURE.read_text(encoding="utf-8"))
        result = render(document)

        assert result.count('data-label="Project">Repeatable Program Review') == 1
        assert result.count('data-label="Ticket">SWM-102') == 1
        assert result.count('data-label="Ticket">SWM-104') == 1
        assert "SWM-103 → SWM-102 → SWM-104" in result
        assert "&lt;script&gt;alert(1)&lt;/script&gt;" in result
        assert "<script>alert(1)</script>" not in result
        assert "agent-msg status-request --json" in result
        assert "{{" not in result and "}}" not in result

    def test_roadmap_and_blocker_sections_use_mobile_table_labels(self):
        """
        Description:
            Check responsive table and phone-width labeling in the generated page.
        Assumptions:
            The checked-in template is used by the report renderer.
        Criteria:
            Each data cell exposes its column heading and the narrow-screen layout stacks rows.

        Trace: SWM-106-AC-3
        """
        result = render(json.loads(FIXTURE.read_text(encoding="utf-8")))

        assert 'data-label="Primary initiative"' in result
        assert 'data-label="Blocker chain"' in result
        assert "@media (max-width: 42rem)" in result
        assert "tbody tr { background" in result

    def test_rejects_missing_or_invalid_roadmap_output(self):
        """
        Description:
            Reject incomplete source data instead of inventing roadmap values.
        Assumptions:
            The valid fixture is modified only in its roadmap command output.
        Criteria:
            Missing and malformed roadmap command output cause a clear ValueError.

        Trace: SWM-106-AC-1
        """
        document = json.loads(FIXTURE.read_text(encoding="utf-8"))
        document["commands"] = [item for item in document["commands"] if item["section"] != "roadmap"]
        with pytest.raises(ValueError, match="exactly one roadmap"):
            render(document)

        document["commands"] = [{"name": "roadmap", "section": "roadmap", "output": {"projects": []}}]
        with pytest.raises(ValueError, match="initiatives and unplaced_projects"):
            render(document)

    def test_reports_duplicate_normalized_project_names_without_source_finding(self):
        """
        Description:
            Detect duplicate normalized project rows directly from the roadmap source.
        Assumptions:
            Two entries normalize to the same project name and the optional duplicate
            membership field is absent.
        Criteria:
            The project appears once and the duplicate is identified as a data-quality finding.

        Trace: SWM-106-AC-2
        """
        document = json.loads(FIXTURE.read_text(encoding="utf-8"))
        roadmap = document["commands"][0]["output"]
        roadmap.pop("projects_in_multiple_initiatives")

        result = render(document)

        assert result.count('data-label="Project">Repeatable Program Review') == 1
        assert "Data-quality finding: duplicate normalized project name(s) in roadmap" in result
        assert "repeatable   program review" in result

    def test_reconcile_findings_appear_once_in_canonical_ticket_rows(self):
        """
        Description:
            Merge reconcile-only tickets and repeated findings into blocker rows.
        Assumptions:
            Reconcile output uses ix-board's ReconcileReport and ReconcileFindings fields.
        Criteria:
            A ticket absent from chain nodes appears once, and repeated reconcile evidence
            is merged into the same canonical row.

        Trace: SWM-106-AC-1, SWM-106-AC-2
        """
        document = json.loads(FIXTURE.read_text(encoding="utf-8"))
        document["commands"].append({
            "name": "ix-board reconcile Project --json",
            "section": "reconcile",
            "output": {
                "project": "Review Project",
                "project_id": "project-1",
                "stale_days": 14,
                "searched_repositories": [],
                "warnings": [],
                "findings": {
                    "merged_pr_open_ticket": [{"identifier": " SWM-999 ", "title": "Reconcile only", "state": "In Progress", "age_days": None, "pull_requests": ["https://github.com/example/repo/pull/99"]}],
                    "done_without_merged_pr": [
                        {"identifier": "SWM-999", "title": "Reconcile only", "state": "Done", "age_days": None, "pull_requests": []},
                        {"identifier": " SWM-102 ", "title": "Padded duplicate of chain ticket", "state": "Blocked", "age_days": None, "pull_requests": []}
                    ],
                    "in_progress_without_pr_or_branch": [],
                    "stale_open_pr": [],
                    "draft_pr_closed_ticket": []
                }
            }
        })

        result = render(document)

        assert result.count('data-label="Ticket">SWM-999') == 1
        assert result.count('data-label="Ticket">SWM-102') == 1
        assert 'data-label="Ticket"> SWM-102' not in result
        assert "Owner unavailable" in result
        assert "merged PR, ticket remains open" in result
        assert "done without merged PR" in result
        assert "https://github.com/example/repo/pull/99" in result

    def test_source_project_name_matching_template_token_is_not_replaced(self):
        """
        Description:
            Preserve template-like braces inside an escaped roadmap project name.
        Assumptions:
            The source value exactly matches another template interpolation token.
        Criteria:
            Source text stays literal while the real allocation token is independently rendered.

        Trace: SWM-106-AC-1, SWM-106-AC-2
        """
        document = json.loads(FIXTURE.read_text(encoding="utf-8"))
        document["commands"][0]["output"]["unplaced_projects"].append({
            "name": "{{allocation_html}}", "status": "Planned", "progress_percent": 0,
            "open": 1, "done": 0, "canceled": 0, "last_activity": None
        })

        result = render(document)

        assert '<td data-label="Project">{{allocation_html}}</td>' in result
        assert result.count("<details><summary>ix-board agents SWM --json</summary>") == 1
        assert "<pre>{" in result

    def test_missing_reconcile_groups_are_reported_as_incomplete(self):
        """
        Description:
            Report omitted or malformed reconcile groups instead of treating them as empty.
        Assumptions:
            The reconcile command returns only a partial findings object.
        Criteria:
            Valid findings remain visible and every missing or unusable group is identified.

        Trace: SWM-106-AC-1
        """
        document = json.loads(FIXTURE.read_text(encoding="utf-8"))
        document["commands"].append({
            "name": "ix-board reconcile Partial Project --json",
            "section": "reconcile",
            "output": {
                "project": "Partial Project",
                "project_id": "project-2",
                "stale_days": 14,
                "searched_repositories": [],
                "warnings": [],
                "findings": {
                    "merged_pr_open_ticket": [
                        {"identifier": "SWM-888", "title": "Visible finding", "state": "In Progress", "age_days": None, "pull_requests": []},
                        {"title": "Incomplete record"},
                        {"identifier": "  ", "title": "Blank identifier", "state": "In Progress", "age_days": None, "pull_requests": []}
                    ],
                    "done_without_merged_pr": [],
                    "stale_open_pr": "not-an-array"
                }
            }
        })

        result = render(document)

        assert result.count('data-label="Ticket">SWM-888') == 1
        assert "missing finding group in_progress_without_pr_or_branch" in result
        assert "missing finding group draft_pr_closed_ticket" in result
        assert "finding group stale_open_pr is not an array" in result
        assert "ignored finding with missing or blank ticket identifier in merged_pr_open_ticket" in result
        assert 'data-label="Ticket">  ' not in result
        assert "Missing values remain undetermined." in result

    def test_whitespace_only_reconcile_identifier_is_incomplete_evidence(self):
        """
        Description:
            Mark a whitespace-only issue identifier as incomplete reconcile evidence.
        Assumptions:
            The reconcile source otherwise contains all expected finding groups.
        Criteria:
            No blank ticket row is rendered and the report names the omitted identifier.

        Trace: SWM-106-AC-1, SWM-106-AC-2
        """
        document = json.loads(FIXTURE.read_text(encoding="utf-8"))
        document["commands"].append({
            "name": "ix-board reconcile Whitespace Project --json",
            "section": "reconcile",
            "output": {
                "findings": {
                    "merged_pr_open_ticket": [{"identifier": " \t ", "title": "No ticket ID"}],
                    "done_without_merged_pr": [],
                    "in_progress_without_pr_or_branch": [],
                    "stale_open_pr": [],
                    "draft_pr_closed_ticket": []
                }
            }
        })

        result = render(document)

        assert "ignored finding with missing or blank ticket identifier" in result
        assert 'data-label="Ticket"> \t ' not in result

    def test_blocker_path_issues_must_be_ticket_identifier_array(self):
        """
        Description:
            Reject a blocker path whose issue chain is encoded as a string.
        Assumptions:
            ix-board ChainPath.issues is an array of issue identifiers.
        Criteria:
            Malformed path data fails rendering instead of being silently omitted.

        Trace: SWM-106-AC-1
        """
        document = json.loads(FIXTURE.read_text(encoding="utf-8"))
        blocker = next(item for item in document["commands"] if item["section"] == "blockers")
        blocker["output"]["paths"][0]["issues"] = "SWM-102"

        with pytest.raises(ValueError, match="blocker path issues field must be an array"):
            render(document)

    def test_blocked_by_must_be_ticket_identifier_array(self):
        """
        Description:
            Reject a blocker node whose blockers are encoded as a string.
        Assumptions:
            ix-board ChainNode.blocked_by is an array of issue identifiers.
        Criteria:
            A malformed string is not interpreted as one ID per character.

        Trace: SWM-106-AC-1
        """
        document = json.loads(FIXTURE.read_text(encoding="utf-8"))
        blocker = next(item for item in document["commands"] if item["section"] == "blockers")
        blocker["output"]["nodes"][0]["blocked_by"] = "SWM-104"

        with pytest.raises(ValueError, match="blocked_by field must be an array"):
            render(document)

    def test_cli_writes_self_contained_html_artifact(self, tmp_path):
        """
        Description:
            Exercise the user-facing renderer command and its output path.
        Assumptions:
            Python 3 is available and the JSON fixture is readable.
        Criteria:
            The CLI exits successfully and writes a complete HTML page at the requested path.

        Trace: SWM-106-AC-1, SWM-106-AC-3
        """
        import subprocess

        output = tmp_path / "artifact" / "review.html"
        process = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "render_report.py"), str(FIXTURE), "--output", str(output)],
            check=False,
            capture_output=True,
            text=True,
        )

        assert process.returncode == 0, process.stderr
        artifact = output.read_text(encoding="utf-8")
        assert artifact.startswith("<!doctype html>")
        assert "Decisions needed from the owner" in artifact
