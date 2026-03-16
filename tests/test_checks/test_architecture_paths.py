"""Tests for architecture paths check."""

from chealth.checks.architecture_paths import ArchitecturePaths
from chealth.models import CheckContext, Severity


def test_pass_has_paths(make_claude_md, project):
    f = make_claude_md("# Arch\n\n- API handlers in `src/api/handlers/`\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = ArchitecturePaths().run(ctx)
    assert results[0].severity == Severity.PASS


def test_warn_no_paths(make_claude_md, project):
    f = make_claude_md("# Project\n\n- This is a project\n- It does things\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = ArchitecturePaths().run(ctx)
    assert results[0].severity == Severity.WARN


def test_ignores_urls(make_claude_md, project):
    f = make_claude_md("# Project\n\n- See https://example.com/api/docs\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = ArchitecturePaths().run(ctx)
    assert results[0].severity == Severity.WARN
