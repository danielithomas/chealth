"""Shared pytest fixtures for chealth tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from chealth.models import CheckContext


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """Return a temporary project root directory."""
    return tmp_path


@pytest.fixture
def make_claude_md(tmp_path: Path):
    """Factory fixture to create CLAUDE.md files in the project."""

    def _make(content: str, path: str = "CLAUDE.md") -> Path:
        file_path = tmp_path / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return file_path

    return _make


@pytest.fixture
def make_context(tmp_path: Path):
    """Factory fixture to create a CheckContext with discovered files."""

    def _make(
        files: list[Path] | None = None,
        max_lines: int = 200,
    ) -> CheckContext:
        ctx = CheckContext(project_root=tmp_path, max_lines=max_lines)
        if files is not None:
            ctx.discovered_files = files
        return ctx

    return _make
