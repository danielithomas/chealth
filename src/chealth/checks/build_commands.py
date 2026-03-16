"""Build commands check — presence of common command patterns in root CLAUDE.md."""

from __future__ import annotations

import re

from chealth.checks import read_file_safe, register
from chealth.models import CheckContext, CheckResult, Severity

# Patterns for common build/test commands
COMMAND_PATTERNS = [
    re.compile(r"`[^`]*(?:npm|pip|uv|make|cargo|pytest|python|yarn|pnpm|go|gradle|mvn|dotnet)\b[^`]*`"),
    re.compile(r"```[^\n]*\n[^`]*(?:npm|pip|uv|make|cargo|pytest|python|yarn|pnpm|go|gradle|mvn|dotnet)\b", re.DOTALL),
]


class BuildCommands:
    name = "build-commands"
    description = "Check for build/test command documentation"
    rule_reference = "Rule 5"

    def run(self, ctx: CheckContext) -> list[CheckResult]:
        root_claude = ctx.project_root / "CLAUDE.md"
        if root_claude not in ctx.discovered_files:
            return []

        content = read_file_safe(root_claude)
        if content is None:
            return []

        found = any(p.search(content) for p in COMMAND_PATTERNS)

        if found:
            return [
                CheckResult(
                    check_name=self.name,
                    severity=Severity.PASS,
                    message="Build/test commands documented",
                    file_path=root_claude,
                    rule_reference=self.rule_reference,
                )
            ]
        else:
            return [
                CheckResult(
                    check_name=self.name,
                    severity=Severity.WARN,
                    message="No build/test commands found in root CLAUDE.md",
                    file_path=root_claude,
                    rule_reference=self.rule_reference,
                )
            ]


register(BuildCommands())
