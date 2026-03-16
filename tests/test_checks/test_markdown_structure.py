"""Tests for markdown structure check."""

from chealth.checks.markdown_structure import MarkdownStructure
from chealth.models import CheckContext, Severity


def test_pass_well_structured(make_claude_md, project):
    f = make_claude_md("# Project\n\n- Item 1\n- Item 2\n\n## Section\n\n- More items\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = MarkdownStructure().run(ctx)
    assert results[0].severity == Severity.PASS


def test_warn_no_bullets(make_claude_md, project):
    f = make_claude_md("# Project\n\nSome text here\n\n## Section\n\nMore text\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = MarkdownStructure().run(ctx)
    assert results[0].severity == Severity.WARN


def test_warn_no_headers(make_claude_md, project):
    f = make_claude_md("- Item 1\n- Item 2\n- Item 3\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = MarkdownStructure().run(ctx)
    assert results[0].severity == Severity.WARN


def test_danger_no_structure(make_claude_md, project):
    content = "\n".join(f"Line {i} of dense prose content." for i in range(10))
    f = make_claude_md(content)
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = MarkdownStructure().run(ctx)
    assert results[0].severity == Severity.DANGER


def test_code_blocks_not_counted(make_claude_md, project):
    content = "# Project\n\n- Item\n\n```\nline1\nline2\nline3\nline4\nline5\nline6\n```\n"
    f = make_claude_md(content)
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = MarkdownStructure().run(ctx)
    assert results[0].severity == Severity.PASS
