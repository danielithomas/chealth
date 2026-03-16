"""Tests for import resolution check."""

from chealth.checks.import_resolution import ImportResolution
from chealth.models import CheckContext, Severity


def test_pass_valid_import(make_claude_md, project):
    make_claude_md("# Extra rules", "docs/extra.md")
    f = make_claude_md("# Root\n- See @docs/extra.md")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = ImportResolution().run(ctx)
    assert any(r.severity == Severity.PASS for r in results)


def test_danger_broken_import(make_claude_md, project):
    f = make_claude_md("# Root\n- See @docs/nonexistent.md")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = ImportResolution().run(ctx)
    assert any(r.severity == Severity.DANGER for r in results)


def test_no_results_for_no_imports(make_claude_md, project):
    f = make_claude_md("# Root\n- No imports here")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = ImportResolution().run(ctx)
    assert len(results) == 0


def test_deep_import_adds_to_discovered(make_claude_md, project):
    make_claude_md("# Extra", "docs/extra.md")
    f = make_claude_md("# Root\n- @docs/extra.md")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    ImportResolution().run(ctx)
    assert any(f.name == "extra.md" for f in ctx.discovered_files)


def test_ignores_email_addresses(make_claude_md, project):
    f = make_claude_md("# Root\nContact user@example.com for help")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = ImportResolution().run(ctx)
    assert len(results) == 0


def test_circular_import_handled(make_claude_md, project):
    make_claude_md("# A\n- See @b.md", "a.md")
    make_claude_md("# B\n- See @a.md", "b.md")
    f = make_claude_md("# Root\n- @a.md")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    # Should not infinite loop
    results = ImportResolution().run(ctx)
    assert len(results) >= 1
