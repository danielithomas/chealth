"""Integration tests for the CLI entry point."""

import json
from pathlib import Path

from chealth.cli import main


def test_help(capsys):
    try:
        main(["--help"])
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert "CLAUDE.md health" in captured.out


def test_version(capsys):
    try:
        main(["--version"])
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert "0.1.1" in captured.out


def test_nonexistent_path(capsys):
    code = main(["/nonexistent/path"])
    assert code == 2


def test_empty_project(tmp_path, capsys):
    code = main([str(tmp_path)])
    captured = capsys.readouterr()
    assert code == 2  # DANGER: no files found
    assert "DANGER" in captured.out or "No CLAUDE.md" in captured.out


def test_healthy_fixture(capsys):
    fixture = str(Path(__file__).parent / "fixtures" / "healthy")
    code = main([fixture])
    captured = capsys.readouterr()
    assert code in (0, 1)  # PASS or WARN
    assert "file-discovery" in captured.out


def test_json_output(tmp_path, capsys):
    (tmp_path / "CLAUDE.md").write_text("# Project\n- Item\n")
    code = main(["--format", "json", str(tmp_path)])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "version" in data
    assert "results" in data
    assert "summary" in data


def test_check_filter(tmp_path, capsys):
    (tmp_path / "CLAUDE.md").write_text("# Project\n- Item\n")
    code = main(["--check", "line-count", str(tmp_path)])
    captured = capsys.readouterr()
    assert "line-count" in captured.out
    # Should not have other check names (except priority checks populate context silently)
    assert "emphasis-keywords" not in captured.out


def test_max_lines_flag(tmp_path, capsys):
    content = "\n".join(f"- line {i}" for i in range(50))
    (tmp_path / "CLAUDE.md").write_text(content)
    code = main(["--max-lines", "30", str(tmp_path)])
    captured = capsys.readouterr()
    assert code >= 1  # Should warn or danger since 50 > 30


def test_exit_zero_flag(tmp_path, capsys):
    """--exit-zero should return 0 even when findings have WARN/DANGER severity."""
    (tmp_path / "CLAUDE.md").write_text("# Project\n- Item\n")
    code = main(["--exit-zero", str(tmp_path)])
    assert code == 0


def test_exit_zero_json_still_has_severity(tmp_path, capsys):
    """--exit-zero returns 0 but JSON output still reports severity."""
    (tmp_path / "CLAUDE.md").write_text("# Project\n- Item\n")
    code = main(["--exit-zero", "--format", "json", str(tmp_path)])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert code == 0
    assert data["summary"]["warn"] >= 0 or data["summary"]["danger"] >= 0


def test_exit_code_0_all_pass(tmp_path, capsys):
    content = (
        "# Project Overview\n\n"
        "The purpose of this Python framework is to build APIs.\n\n"
        "## Architecture\n\n"
        "- API handlers in `src/api/handlers/`\n\n"
        "## Build\n\n"
        "- `uv run pytest` to test\n\n"
        "## Workflow\n\n"
        "- Branch from main for features\n"
        "- Write conventional commits\n"
        "- Open a PR for review\n\n"
        "IMPORTANT: Always run tests before committing.\n"
    )
    (tmp_path / "CLAUDE.md").write_text(content)
    code = main([str(tmp_path)])
    assert code == 0
