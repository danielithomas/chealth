"""Core data models for chealth."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path


class Severity(IntEnum):
    """Check result severity levels. IntEnum so max() gives the worst."""

    PASS = 0
    INFO = 0
    WARN = 1
    DANGER = 2


@dataclass(frozen=True)
class CheckResult:
    """Result of a single check against a single file."""

    check_name: str
    severity: Severity
    message: str
    file_path: Path | None = None
    rule_reference: str = ""
    details: dict = field(default_factory=dict)


@dataclass
class CheckContext:
    """Shared context populated by priority checks and consumed by all checks."""

    project_root: Path = field(default_factory=Path)
    max_lines: int = 200
    discovered_files: list[Path] = field(default_factory=list)
    import_targets: dict[Path, list[Path]] = field(default_factory=dict)
