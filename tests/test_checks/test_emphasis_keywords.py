"""Tests for emphasis keywords check."""

from chealth.checks.emphasis_keywords import EmphasisKeywords
from chealth.models import CheckContext, Severity


def test_pass_has_keywords(make_claude_md, project):
    f = make_claude_md("# Rules\n\nIMPORTANT: Always run tests\nYOU MUST check types\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = EmphasisKeywords().run(ctx)
    assert results[0].severity == Severity.PASS
    assert "IMPORTANT" in results[0].message


def test_warn_no_keywords(make_claude_md, project):
    f = make_claude_md("# Rules\n\n- Run tests before committing\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = EmphasisKeywords().run(ctx)
    assert results[0].severity == Severity.WARN


def test_ignores_code_blocks(make_claude_md, project):
    f = make_claude_md("# Rules\n\n```\nIMPORTANT: this is in a code block\n```\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = EmphasisKeywords().run(ctx)
    assert results[0].severity == Severity.WARN


def test_only_checks_root(make_claude_md, project):
    make_claude_md("IMPORTANT: sub rule", "src/CLAUDE.md")
    # No root CLAUDE.md
    sub = project / "src" / "CLAUDE.md"
    ctx = CheckContext(project_root=project, discovered_files=[sub])
    results = EmphasisKeywords().run(ctx)
    assert len(results) == 0
