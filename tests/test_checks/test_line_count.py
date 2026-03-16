"""Tests for line count check."""

from chealth.checks.line_count import LineCount
from chealth.models import CheckContext, Severity


def test_pass_under_limit(make_claude_md, project):
    f = make_claude_md("# Short\n- line\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = LineCount().run(ctx)
    assert results[0].severity == Severity.PASS


def test_warn_over_limit(make_claude_md, project):
    content = "\n".join(f"- line {i}" for i in range(210))
    f = make_claude_md(content)
    ctx = CheckContext(project_root=project, max_lines=200, discovered_files=[f])
    results = LineCount().run(ctx)
    assert results[0].severity == Severity.WARN


def test_danger_far_over_limit(make_claude_md, project):
    content = "\n".join(f"- line {i}" for i in range(300))
    f = make_claude_md(content)
    ctx = CheckContext(project_root=project, max_lines=200, discovered_files=[f])
    results = LineCount().run(ctx)
    assert results[0].severity == Severity.DANGER


def test_custom_max_lines(make_claude_md, project):
    content = "\n".join(f"- line {i}" for i in range(50))
    f = make_claude_md(content)
    ctx = CheckContext(project_root=project, max_lines=100, discovered_files=[f])
    results = LineCount().run(ctx)
    assert results[0].severity == Severity.PASS


def test_checks_all_discovered_files(make_claude_md, project):
    f1 = make_claude_md("# Short", "CLAUDE.md")
    f2 = make_claude_md("# Also short", "src/CLAUDE.md")
    ctx = CheckContext(project_root=project, discovered_files=[f1, f2])
    results = LineCount().run(ctx)
    assert len(results) == 2
