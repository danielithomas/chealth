"""Tests for the check runner."""

from pathlib import Path

from chealth.models import Severity
from chealth.runner import compute_exit_code, run_checks


def test_run_checks_empty_project(tmp_path):
    results = run_checks(tmp_path)
    assert len(results) >= 1  # At least file-discovery result


def test_run_checks_with_filter(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("# Project\n- Item\n")
    results = run_checks(tmp_path, selected_checks=["line-count"])
    check_names = {r.check_name for r in results}
    assert "line-count" in check_names
    assert "emphasis-keywords" not in check_names


def test_priority_checks_populate_context(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("# Project\n- Item\n")
    # Even with a filter that excludes priority checks, they still run
    results = run_checks(tmp_path, selected_checks=["line-count"])
    # line-count should have results since file-discovery populated discovered_files
    assert any(r.check_name == "line-count" for r in results)


def test_compute_exit_code_pass():
    from chealth.models import CheckResult

    results = [
        CheckResult(check_name="test", severity=Severity.PASS, message="ok")
    ]
    assert compute_exit_code(results) == 0


def test_compute_exit_code_warn():
    from chealth.models import CheckResult

    results = [
        CheckResult(check_name="test", severity=Severity.WARN, message="warning")
    ]
    assert compute_exit_code(results) == 1


def test_compute_exit_code_danger():
    from chealth.models import CheckResult

    results = [
        CheckResult(check_name="test", severity=Severity.DANGER, message="danger"),
        CheckResult(check_name="test2", severity=Severity.PASS, message="ok"),
    ]
    assert compute_exit_code(results) == 2


def test_compute_exit_code_empty():
    assert compute_exit_code([]) == 0
