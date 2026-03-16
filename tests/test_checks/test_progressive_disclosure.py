"""Tests for progressive disclosure check."""

from chealth.checks.progressive_disclosure import ProgressiveDisclosure
from chealth.models import CheckContext, Severity


def test_pass_short_file(make_claude_md, project):
    f = make_claude_md("# Short\n- just a few lines\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = ProgressiveDisclosure().run(ctx)
    assert results[0].severity == Severity.PASS


def test_warn_large_no_modularization(make_claude_md, project):
    content = "\n".join(f"- Rule {i}" for i in range(120))
    f = make_claude_md(content)
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = ProgressiveDisclosure().run(ctx)
    assert results[0].severity == Severity.WARN


def test_pass_large_with_imports(make_claude_md, project):
    content = "\n".join(f"- Rule {i}" for i in range(120))
    f = make_claude_md(content)
    extra = make_claude_md("# Extra", "docs/extra.md")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    ctx.import_targets[f] = [extra]
    results = ProgressiveDisclosure().run(ctx)
    assert results[0].severity == Severity.PASS


def test_pass_large_with_subdir(make_claude_md, project):
    content = "\n".join(f"- Rule {i}" for i in range(120))
    f = make_claude_md(content)
    sub = make_claude_md("# Sub", "src/CLAUDE.md")
    ctx = CheckContext(project_root=project, discovered_files=[f, sub])
    results = ProgressiveDisclosure().run(ctx)
    assert results[0].severity == Severity.PASS


def test_pass_large_with_rules(make_claude_md, project):
    content = "\n".join(f"- Rule {i}" for i in range(120))
    f = make_claude_md(content)
    rules = make_claude_md("# Rules", ".claude/rules/testing.md")
    ctx = CheckContext(project_root=project, discovered_files=[f, rules])
    results = ProgressiveDisclosure().run(ctx)
    assert results[0].severity == Severity.PASS
