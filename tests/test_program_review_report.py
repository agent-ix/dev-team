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
