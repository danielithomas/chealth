"""Tests for gitignore check."""

from chealth.checks.gitignore_check import GitignoreCheck
from chealth.models import CheckContext, Severity


def test_no_local_no_results(make_claude_md, project):
    f = make_claude_md("# Root")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = GitignoreCheck().run(ctx)
    assert len(results) == 0


def test_pass_local_is_gitignored(make_claude_md, project):
    f = make_claude_md("# Root")
    local = make_claude_md("# Local", "CLAUDE.local.md")
    gitignore = project / ".gitignore"
    gitignore.write_text("CLAUDE.local.md\n")
    ctx = CheckContext(project_root=project, discovered_files=[f, local])
    results = GitignoreCheck().run(ctx)
    assert results[0].severity == Severity.PASS


def test_warn_local_not_gitignored(make_claude_md, project):
    f = make_claude_md("# Root")
    local = make_claude_md("# Local", "CLAUDE.local.md")
    ctx = CheckContext(project_root=project, discovered_files=[f, local])
    results = GitignoreCheck().run(ctx)
    assert results[0].severity == Severity.WARN


def test_wildcard_pattern_matches(make_claude_md, project):
    f = make_claude_md("# Root")
    local = make_claude_md("# Local", "CLAUDE.local.md")
    gitignore = project / ".gitignore"
    gitignore.write_text("*.local.md\n")
    ctx = CheckContext(project_root=project, discovered_files=[f, local])
    results = GitignoreCheck().run(ctx)
    assert results[0].severity == Severity.PASS
