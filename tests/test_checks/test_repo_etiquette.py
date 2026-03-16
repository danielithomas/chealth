"""Tests for repo etiquette check."""

from chealth.checks.repo_etiquette import RepoEtiquette
from chealth.models import CheckContext, Severity


def test_pass_all_clusters(make_claude_md, project):
    content = (
        "# Workflow\n\n"
        "- Branch from main for features\n"
        "- Write conventional commits\n"
        "- Open a PR for review\n"
    )
    f = make_claude_md(content)
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = RepoEtiquette().run(ctx)
    assert results[0].severity == Severity.PASS


def test_warn_missing_clusters(make_claude_md, project):
    f = make_claude_md("# Project\n\n- This is a Python project\n")
    ctx = CheckContext(project_root=project, discovered_files=[f])
    results = RepoEtiquette().run(ctx)
    assert results[0].severity == Severity.WARN
