"""Tests for build commands check."""

from chealth.checks.build_commands import BuildCommands
from chealth.models import CheckContext, Severity


def test_pass_has_commands(make_claude_md, project):
    f = make_claude_md("# Build\n\n- `npm run build` to build\n- `pytest` to test\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = BuildCommands().run(ctx)
    assert results[0].severity == Severity.PASS


def test_warn_no_commands(make_claude_md, project):
    f = make_claude_md("# Project\n\n- This is a web app\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = BuildCommands().run(ctx)
    assert results[0].severity == Severity.WARN


def test_detects_code_block_commands(make_claude_md, project):
    content = "# Build\n\n```bash\nuv run pytest\n```\n"
    f = make_claude_md(content)
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = BuildCommands().run(ctx)
    assert results[0].severity == Severity.PASS
