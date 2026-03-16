"""File discovery check — find all CLAUDE.md, CLAUDE.local.md, .claude/rules/*.md files."""

from __future__ import annotations

from pathlib import Path

from chealth.checks import register
from chealth.models import CheckContext, CheckResult, Severity

# Directories to skip during traversal
SKIP_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".env",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "dist",
    "build",
    ".eggs",
}

CLAUDE_FILENAMES = {"CLAUDE.md", "CLAUDE.local.md"}


class FileDiscovery:
    name = "file-discovery"
    description = "Inventory all CLAUDE.md, CLAUDE.local.md, and .claude/rules/*.md files"
    rule_reference = "Rules 15, 17"

    def run(self, ctx: CheckContext) -> list[CheckResult]:
        results: list[CheckResult] = []
        discovered: list[Path] = []

        # Walk project tree
        for path in self._walk(ctx.project_root):
            discovered.append(path)

        # Also check .claude/rules/*.md
        rules_dir = ctx.project_root / ".claude" / "rules"
        if rules_dir.is_dir():
            for md in sorted(rules_dir.glob("*.md")):
                if md.is_file() and md not in discovered:
                    discovered.append(md)

        # Populate context for other checks
        ctx.discovered_files = sorted(discovered)

        # Evaluate
        root_claude = ctx.project_root / "CLAUDE.md"
        has_root = root_claude in discovered
        has_any = len(discovered) > 0

        if has_root:
            results.append(
                CheckResult(
                    check_name=self.name,
                    severity=Severity.PASS,
                    message=f"Found {len(discovered)} file(s)",
                    file_path=root_claude,
                    rule_reference=self.rule_reference,
                    details={"files": [str(f) for f in discovered]},
                )
            )
        elif has_any:
            results.append(
                CheckResult(
                    check_name=self.name,
                    severity=Severity.WARN,
                    message=f"No root CLAUDE.md found, but {len(discovered)} file(s) in subdirectories",
                    rule_reference=self.rule_reference,
                    details={"files": [str(f) for f in discovered]},
                )
            )
        else:
            results.append(
                CheckResult(
                    check_name=self.name,
                    severity=Severity.DANGER,
                    message="No CLAUDE.md files found in project",
                    rule_reference=self.rule_reference,
                )
            )

        return results

    def _walk(self, root: Path) -> list[Path]:
        """Walk directory tree finding CLAUDE.md and CLAUDE.local.md files."""
        found: list[Path] = []
        try:
            entries = sorted(root.iterdir())
        except PermissionError:
            return found

        for entry in entries:
            if entry.is_file() and entry.name in CLAUDE_FILENAMES:
                found.append(entry)
            elif entry.is_dir() and entry.name not in SKIP_DIRS:
                found.extend(self._walk(entry))
        return found


register(FileDiscovery())
