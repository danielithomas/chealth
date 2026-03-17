"""Tests for output formatters."""

import json
from pathlib import Path

from chealth.formatters import format_json, format_text
from chealth.models import CheckResult, Severity


def _make_results(project_root: Path) -> list[CheckResult]:
    return [
        CheckResult(
            check_name="line-count",
            severity=Severity.PASS,
            message="50 lines (limit: 200)",
            file_path=project_root / "CLAUDE.md",
            rule_reference="Rule 1",
        ),
        CheckResult(
            check_name="emphasis-keywords",
            severity=Severity.WARN,
            message="No emphasis keywords found",
            file_path=project_root / "CLAUDE.md",
            rule_reference="Rule 10",
        ),
    ]


def test_text_format_empty():
    output = format_text([], Path("/project"))
    assert "all checks passed" in output


def test_text_format_grouped(tmp_path):
    results = _make_results(tmp_path)
    output = format_text(results, tmp_path)
    assert "[PASS]" in output
    assert "[WARN]" in output
    assert "Summary:" in output
    assert "CLAUDE.md" in output


def test_text_format_relative_paths(tmp_path):
    results = _make_results(tmp_path)
    output = format_text(results, tmp_path)
    # Should use relative paths, not absolute
    assert str(tmp_path) not in output


def test_json_format_valid(tmp_path):
    results = _make_results(tmp_path)
    output = format_json(results, tmp_path)
    data = json.loads(output)
    assert data["version"] == "0.1.1"
    assert len(data["results"]) == 2
    assert data["summary"]["total"] == 2
    assert data["summary"]["pass"] == 1
    assert data["summary"]["warn"] == 1


def test_json_format_empty(tmp_path):
    output = format_json([], tmp_path)
    data = json.loads(output)
    assert data["summary"]["total"] == 0


def test_json_relative_paths(tmp_path):
    results = _make_results(tmp_path)
    output = format_json(results, tmp_path)
    data = json.loads(output)
    for r in data["results"]:
        if r["file_path"]:
            assert not r["file_path"].startswith(str(tmp_path))
