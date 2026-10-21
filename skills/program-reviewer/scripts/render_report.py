#!/usr/bin/env python3
"""Render an HTML program review from captured command JSON and judgments."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_ROOT / "references" / "report-template.html"
PROJECT_NAME = re.compile(r"\s+")
TEMPLATE_TOKEN = re.compile(r"\{\{[^{}]*\}\}")


def h(value: Any) -> str:
    return html.escape(str(value), quote=True)


def valid_time(value: Any) -> tuple[str, str]:
    if not isinstance(value, str):
        raise ValueError("observed_at must be an ISO-8601 string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("observed_at must include a timezone")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"), value


def table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return '<p class="empty">No records in the captured command output.</p>'
    head = "".join(f"<th scope=\"col\">{h(label)}</th>" for label in headers)
    body = "".join(
        "<tr>" + "".join(
            f'<td data-label="{h(label)}">{cell}</td>'
            for label, cell in zip(headers, row, strict=True)
        ) + "</tr>"
        for row in rows
    )
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def json_block(value: Any) -> str:
    return f"<pre>{h(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))}</pre>"


def command_sources(doc: dict[str, Any], section: str) -> list[dict[str, Any]]:
    commands = doc.get("commands")
    if not isinstance(commands, list):
        raise ValueError("commands must be an array of captured command outputs")
    found = []
    for command in commands:
        if not isinstance(command, dict) or not isinstance(command.get("name"), str):
            raise ValueError("each command needs a name, section, and output")
        if command.get("section") == section:
            if "output" not in command:
                raise ValueError(f"command {command['name']!r} has no captured output")
            found.append(command)
    return found


def roadmap_html(doc: dict[str, Any]) -> str:
    sources = command_sources(doc, "roadmap")
    if len(sources) != 1:
        raise ValueError("exactly one roadmap command output is required")
    output = sources[0]["output"]
    if not isinstance(output, dict) or not isinstance(output.get("initiatives"), list) or not isinstance(output.get("unplaced_projects"), list):
        raise ValueError("roadmap output must contain initiatives and unplaced_projects arrays")

    seen: set[str] = set()
    rows: list[list[str]] = []

    def add(project: Any, initiative: str) -> None:
        if not isinstance(project, dict) or not isinstance(project.get("name"), str):
            raise ValueError("each roadmap project must have a name")
        name = project["name"]
        key = PROJECT_NAME.sub(" ", name.strip()).casefold()
        if key in seen:
            return
        seen.add(key)
        also_in = project.get("also_in", [])
        note = ""
        if also_in:
            if not isinstance(also_in, list):
                raise ValueError(f"also_in for {name!r} must be an array")
            note = "<br><span class=\"meta\">Also in: " + h(", ".join(map(str, also_in))) + "</span>"
        rows.append([
            h(initiative), h(name) + note, h(project.get("status", "Unavailable")),
            h(project.get("progress_percent", "Unavailable")), h(project.get("open", "Unavailable")),
            h(project.get("done", "Unavailable")), h(project.get("canceled", "Unavailable")),
            h(project.get("last_activity") or "Unavailable"),
        ])

    for initiative in output["initiatives"]:
        if not isinstance(initiative, dict) or not isinstance(initiative.get("projects"), list):
            raise ValueError("each roadmap initiative must contain a projects array")
        for project in initiative["projects"]:
            add(project, str(initiative.get("name", "Unavailable")))
    for project in output["unplaced_projects"]:
        add(project, "Unplaced")

    finding = ""
    if output.get("projects_in_multiple_initiatives"):
        finding += "<p class=\"meta\">Multiple initiative membership reported for: " + h(", ".join(map(str, output["projects_in_multiple_initiatives"]))) + ". Primary placement remains the canonical row.</p>"
    return finding + table(["Primary initiative", "Project", "Status", "Progress %", "Open", "Done", "Canceled", "Last activity"], rows)


def blocker_html(doc: dict[str, Any]) -> str:
    sources = command_sources(doc, "blockers")
    reconcile_sources = command_sources(doc, "reconcile")
    if not sources and not reconcile_sources:
        return '<p class="empty">Unavailable: no blocker-chain or reconcile command output was captured.</p>'
    nodes: OrderedDict[str, dict[str, Any]] = OrderedDict()
    chains: dict[str, set[str]] = {}
    reconcile_evidence: dict[str, set[str]] = {}
    reconcile_warnings: list[str] = []
    for source in sources:
        output = source["output"]
        if not isinstance(output, dict) or not isinstance(output.get("nodes"), list) or not isinstance(output.get("paths", []), list):
            raise ValueError(f"blocker output from {source['name']!r} must contain nodes and paths arrays")
        for node in output["nodes"]:
            if not isinstance(node, dict) or not isinstance(node.get("identifier"), str) or not node["identifier"].strip():
                raise ValueError("each blocker node must have an identifier")
            ident = node["identifier"]
            # Merge repeated command evidence by the canonical issue identifier.
            prior = nodes.setdefault(ident, node.copy())
            if prior is not node:
                prior["blocked_by"] = sorted(set(prior.get("blocked_by", [])) | set(node.get("blocked_by", [])))
                for key in ("root_blocker", "unowned_root_blocker"):
                    prior[key] = bool(prior.get(key)) or bool(node.get(key))
                for key in ("owner_lane", "assignee_name", "state", "title"):
                    if not prior.get(key) and node.get(key):
                        prior[key] = node[key]
        for path in output.get("paths", []):
            if isinstance(path, dict) and isinstance(path.get("issues"), list):
                chain = " → ".join(map(str, path["issues"]))
                for ident in path["issues"]:
                    chains.setdefault(str(ident), set()).add(chain)

    ticket_groups = (
        ("merged PR, ticket remains open", "merged_pr_open_ticket"),
        ("done without merged PR", "done_without_merged_pr"),
        ("in progress without PR or branch", "in_progress_without_pr_or_branch"),
        ("stale open PR", "stale_open_pr"),
        ("draft PR on closed ticket", "draft_pr_closed_ticket"),
    )
    for source in reconcile_sources:
        output = source["output"]
        if not isinstance(output, dict):
            reconcile_warnings.append(f"{source['name']}: output is not a JSON object")
            continue
        findings = output.get("findings")
        if not isinstance(findings, dict):
            reconcile_warnings.append(f"{source['name']}: missing findings object")
            continue
        for label, group_name in ticket_groups:
            if group_name not in findings:
                reconcile_warnings.append(f"{source['name']}: missing finding group {group_name}")
                continue
            records = findings[group_name]
            if not isinstance(records, list):
                reconcile_warnings.append(f"{source['name']}: finding group {group_name} is not an array")
                continue
            for record in records:
                if not isinstance(record, dict) or not isinstance(record.get("identifier"), str) or not record["identifier"].strip():
                    reconcile_warnings.append(f"{source['name']}: ignored finding with missing or blank ticket identifier in {group_name}")
                    continue
                ident = record["identifier"]
                title = record.get("title", "")
                state = record.get("state", "Unavailable")
                node = nodes.setdefault(ident, {
                    "identifier": ident, "title": title, "state": state,
                    "owner_lane": None, "assignee_name": None, "assignee_id": None, "blocked_by": [],
                    "root_blocker": False, "unowned_root_blocker": False,
                })
                if not node.get("title") and title:
                    node["title"] = title
                if node.get("state") == "Unavailable" and state:
                    node["state"] = state
                detail = label
                pull_requests = record.get("pull_requests", [])
                if pull_requests:
                    detail += ": " + ", ".join(map(str, pull_requests))
                if record.get("url"):
                    detail += ": " + str(record["url"])
                if record.get("age_days") is not None:
                    detail += f" ({record['age_days']} days)"
                reconcile_evidence.setdefault(ident, set()).add(detail)

    rows = []
    for ident, node in nodes.items():
        blockers = node.get("blocked_by", [])
        if not blockers and not node.get("root_blocker") and not node.get("unowned_root_blocker") and not reconcile_evidence.get(ident):
            continue
        owner = node.get("owner_lane") or node.get("assignee_name")
        if not owner:
            owner = "Unassigned" if "assignee_id" in node and node.get("assignee_id") is None else "Owner unavailable"
        chain_text = "<br>".join(h(chain) for chain in sorted(chains.get(ident, set()))) or "Unavailable"
        if reconcile_evidence.get(ident):
            chain_text += "<br><span class=\"meta\">Reconcile: " + "; ".join(h(item) for item in sorted(reconcile_evidence[ident])) + "</span>"
        if blockers:
            chain_text += "<br><span class=\"meta\">Blocked by: " + h(", ".join(map(str, blockers))) + "</span>"
        if node.get("unowned_root_blocker"):
            chain_text += "<br><span class=\"status\">Unowned root blocker</span>"
        rows.append([h(owner), h(ident) + " — " + h(node.get("title", "")), h(node.get("state", "Unavailable")), chain_text])
    warnings_html = "".join(f'<p class="incomplete" role="status">Incomplete reconcile output: {h(warning)}. Missing values remain undetermined.</p>' for warning in reconcile_warnings)
    return warnings_html + table(["Owner", "Ticket", "State", "Blocker chain"], rows)


def sources_html(commands: list[dict[str, Any]], section: str, empty: str) -> str:
    sources = command_sources({"commands": commands}, section)
    if not sources:
        return f'<p class="empty">{h(empty)}</p>'
    return "".join(
        f"<details><summary>{h(command['name'])}</summary>{json_block(command['output'])}</details>"
        for command in sources
    )


def judgment_rows(value: Any, required: tuple[str, ...], label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    for index, record in enumerate(value):
        if not isinstance(record, dict) or any(not isinstance(record.get(key), str) for key in required):
            raise ValueError(f"{label}[{index}] must contain string fields: {', '.join(required)}")
    return value


def render(doc: dict[str, Any]) -> str:
    if not isinstance(doc, dict):
        raise ValueError("input must be a JSON object")
    title = doc.get("title")
    scope = doc.get("scope")
    verdict = doc.get("verdict")
    if not all(isinstance(value, str) and value.strip() for value in (title, scope, verdict)):
        raise ValueError("title, scope, and verdict must be non-empty strings")
    iso_time, display_time = valid_time(doc.get("observed_at"))
    commands = doc.get("commands", [])
    if not isinstance(commands, list):
        raise ValueError("commands must be an array")

    program_status = judgment_rows(doc.get("program_status", []), ("program", "assessment"), "program_status")
    status_rows = [[h(item["program"]), h(item["assessment"])] for item in program_status]
    decisions = judgment_rows(doc.get("owner_decisions", []), ("decision", "evidence"), "owner_decisions")
    decision_rows = [[h(item["decision"]), h(item["evidence"]), h(", ".join(item.get("options", [])) if isinstance(item.get("options", []), list) else "Unavailable")] for item in decisions]
    unavailable = doc.get("unavailable_sources", [])
    if not isinstance(unavailable, list) or any(not isinstance(item, str) for item in unavailable):
        raise ValueError("unavailable_sources must be an array of command names")

    replacements = {
        "{{report_title}}": h(title), "{{observed_at_iso}}": h(iso_time),
        "{{observed_at}}": h(display_time), "{{scope_name}}": h(scope),
        "{{verdict_html}}": "<p>" + h(verdict) + "</p>",
        "{{roadmap_html}}": roadmap_html(doc),
        "{{program_status_html}}": table(["Program", "Assessment"], status_rows),
        "{{blockers_html}}": blocker_html(doc),
        "{{allocation_html}}": sources_html(commands, "allocation", "Unavailable: lane focus or server capacity command output was not captured."),
        "{{lead_reports_html}}": sources_html(commands, "leads", "Unavailable: no structured lead response command output was captured."),
        "{{linear_changes_html}}": sources_html(commands, "linear_changes", "No confirmed Linear changes were recorded from command output."),
        "{{owner_decisions_html}}": table(["Decision", "Evidence", "Options"], decision_rows),
        "{{source_commands_html}}": h("; ".join(command["name"] for command in commands) or "None captured"),
        "{{unavailable_sources_html}}": h("; ".join(unavailable) or "None reported"),
    }
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    template_tokens = set(TEMPLATE_TOKEN.findall(template))
    missing = set(replacements) - template_tokens
    if missing:
        raise ValueError("template is missing required token(s): " + ", ".join(sorted(missing)))
    unresolved = template_tokens - set(replacements)
    if unresolved or "{{" in TEMPLATE_TOKEN.sub("", template) or "}}" in TEMPLATE_TOKEN.sub("", template):
        raise ValueError("template contains an unresolved token")
    return TEMPLATE_TOKEN.sub(lambda match: replacements[match.group(0)], template)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON containing captured command outputs and reviewer judgments")
    parser.add_argument("--output", type=Path, required=True, help="path for the generated HTML artifact")
    args = parser.parse_args()
    try:
        document = json.loads(args.input.read_text(encoding="utf-8"))
        html_page = render(document)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(html_page, encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as error:
        print(f"program-review renderer: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
