"""Tests for universal applicability check."""

from chealth.checks.universal_applicability import UniversalApplicability
from chealth.models import CheckContext, Severity


def test_pass_clean(make_claude_md, project):
    f = make_claude_md("# Project\n\n- Use consistent formatting\n- Run tests\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = UniversalApplicability().run(ctx)
    assert results[0].severity == Severity.PASS


def test_warn_sql(make_claude_md, project):
    f = make_claude_md("# DB\n\nSELECT * FROM users WHERE active = true\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = UniversalApplicability().run(ctx)
    assert results[0].severity == Severity.WARN


def test_danger_multiple_patterns(make_claude_md, project):
    content = (
        "# Config\n\n"
        "SELECT * FROM users\n"
        "Connect to postgres://localhost:5432/db\n"
        "Set PORT = 8080\n"
    )
    f = make_claude_md(content)
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = UniversalApplicability().run(ctx)
    assert results[0].severity == Severity.DANGER


def test_code_blocks_stripped(make_claude_md, project):
    content = "# Project\n\n```sql\nSELECT * FROM users\n```\n"
    f = make_claude_md(content)
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = UniversalApplicability().run(ctx)
    assert results[0].severity == Severity.PASS
