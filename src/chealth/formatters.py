"""Text and JSON output formatters."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from chealth import __version__
from chealth.models import CheckResult, Severity

SEVERITY_BADGES = {
    Severity.PASS: "PASS",
    Severity.WARN: "WARN",
    Severity.DANGER: "DANGER",
}


def _relative_path(file_path: Path | None, project_root: Path) -> str | None:
    if file_path is None:
        return None
    try:
        return str(file_path.relative_to(project_root))
    except ValueError:
        return str(file_path)


def format_text(results: list[CheckResult], project_root: Path) -> str:
    """Format results as human-readable text grouped by file."""
    if not results:
        return "chealth: all checks passed.\n"

    # Group by file
    by_file: dict[str | None, list[CheckResult]] = defaultdict(list)
    for r in results:
        key = _relative_path(r.file_path, project_root)
        by_file[key].append(r)

    lines: list[str] = []
    for file_key, file_results in by_file.items():
        header = file_key or "(project-level)"
        lines.append(f"\n{header}")
        for r in file_results:
            badge = SEVERITY_BADGES.get(r.severity, "PASS")
            ref = f" [{r.rule_reference}]" if r.rule_reference else ""
            lines.append(f"  [{badge}] {r.check_name}: {r.message}{ref}")

    # Summary
    counts = defaultdict(int)
    for r in results:
        counts[r.severity] += 1
    summary_parts = []
    for sev in (Severity.DANGER, Severity.WARN, Severity.PASS):
        if counts[sev]:
            summary_parts.append(f"{counts[sev]} {SEVERITY_BADGES[sev]}")
    lines.append(f"\nSummary: {', '.join(summary_parts)}")
    return "\n".join(lines) + "\n"


def format_json(results: list[CheckResult], project_root: Path) -> str:
    """Format results as JSON."""
    output = {
        "version": __version__,
        "project_root": str(project_root),
        "results": [
            {
                "check_name": r.check_name,
                "severity": SEVERITY_BADGES.get(r.severity, "PASS"),
                "message": r.message,
                "file_path": _relative_path(r.file_path, project_root),
                "rule_reference": r.rule_reference,
                "details": r.details,
            }
            for r in results
        ],
        "summary": {
            "total": len(results),
            "pass": sum(1 for r in results if r.severity == Severity.PASS),
            "warn": sum(1 for r in results if r.severity == Severity.WARN),
            "danger": sum(1 for r in results if r.severity == Severity.DANGER),
        },
    }
    return json.dumps(output, indent=2) + "\n"
