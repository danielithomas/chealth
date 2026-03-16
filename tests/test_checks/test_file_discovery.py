"""Tests for file discovery check."""

from pathlib import Path

from chealth.checks.file_discovery import FileDiscovery
from chealth.models import CheckContext, Severity


def test_finds_root_claude_md(make_claude_md, project):
    make_claude_md("# Hello")
    ctx = CheckContext(project_root=project)
    results = FileDiscovery().run(ctx)
    assert len(results) == 1
    assert results[0].severity == Severity.PASS
    assert project / "CLAUDE.md" in ctx.discovered_files


def test_finds_subdirectory_files(make_claude_md, project):
    make_claude_md("# Root", "CLAUDE.md")
    make_claude_md("# Sub", "src/api/CLAUDE.md")
    ctx = CheckContext(project_root=project)
    results = FileDiscovery().run(ctx)
    assert results[0].severity == Severity.PASS
    assert len(ctx.discovered_files) == 2


def test_finds_rules_files(make_claude_md, project):
    make_claude_md("# Root", "CLAUDE.md")
    make_claude_md("# Testing", ".claude/rules/testing.md")
    ctx = CheckContext(project_root=project)
    results = FileDiscovery().run(ctx)
    assert results[0].severity == Severity.PASS
    assert len(ctx.discovered_files) == 2


def test_warns_no_root(make_claude_md, project):
    make_claude_md("# Sub only", "src/CLAUDE.md")
    ctx = CheckContext(project_root=project)
    results = FileDiscovery().run(ctx)
    assert results[0].severity == Severity.WARN


def test_danger_no_files(project):
    ctx = CheckContext(project_root=project)
    results = FileDiscovery().run(ctx)
    assert results[0].severity == Severity.DANGER


def test_finds_local_md(make_claude_md, project):
    make_claude_md("# Root", "CLAUDE.md")
    make_claude_md("# Local", "CLAUDE.local.md")
    ctx = CheckContext(project_root=project)
    results = FileDiscovery().run(ctx)
    assert any(f.name == "CLAUDE.local.md" for f in ctx.discovered_files)


def test_skips_git_directory(make_claude_md, project):
    make_claude_md("# Root", "CLAUDE.md")
    make_claude_md("# Git", ".git/CLAUDE.md")
    ctx = CheckContext(project_root=project)
    FileDiscovery().run(ctx)
    assert not any(".git" in str(f) and "rules" not in str(f) for f in ctx.discovered_files if f.name == "CLAUDE.md" and f.parent.name == ".git")
