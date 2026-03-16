"""Check protocol, registry, and shared utilities."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Protocol

from chealth.models import CheckContext, CheckResult


class Check(Protocol):
    """Protocol that all checks must implement."""

    name: str
    description: str
    rule_reference: str

    def run(self, ctx: CheckContext) -> list[CheckResult]: ...


# Global check registry
_registry: dict[str, Check] = {}


def register(check: Check) -> Check:
    """Register a check instance in the global registry."""
    _registry[check.name] = check
    return check


def get_all() -> dict[str, Check]:
    """Return all registered checks."""
    return dict(_registry)


def get(name: str) -> Check | None:
    """Return a check by name."""
    return _registry.get(name)


def read_file_safe(path: Path) -> str | None:
    """Read a file trying multiple encodings. Returns None on failure."""
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except (UnicodeDecodeError, ValueError):
            continue
        except OSError:
            return None
    return None


def strip_code_blocks(content: str) -> str:
    """Remove fenced code block content to prevent false positives."""
    return re.sub(r"```[^\n]*\n.*?```", "", content, flags=re.DOTALL)
