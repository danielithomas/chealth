"""Emphasis keywords check — IMPORTANT/YOU MUST/CRITICAL/etc. present for critical rules."""

from __future__ import annotations

import re

from chealth.checks import read_file_safe, strip_code_blocks, register
from chealth.models import CheckContext, CheckResult, Severity

EMPHASIS_PATTERN = re.compile(
    r"\b(IMPORTANT|YOU MUST|CRITICAL|NEVER|ALWAYS|REQUIRED)\b"
)


class EmphasisKeywords:
    name = "emphasis-keywords"
    description = "Check for emphasis keywords (IMPORTANT, YOU MUST, etc.)"
    rule_reference = "Rule 10"

    def run(self, ctx: CheckContext) -> list[CheckResult]:
        root_claude = ctx.project_root / "CLAUDE.md"
        if root_claude not in ctx.discovered_files:
            return []

        content = read_file_safe(root_claude)
        if content is None:
            return []

        stripped = strip_code_blocks(content)
        matches = EMPHASIS_PATTERN.findall(stripped)

        if matches:
            unique = sorted(set(matches))
            return [
                CheckResult(
                    check_name=self.name,
                    severity=Severity.PASS,
                    message=f"Emphasis keywords found: {', '.join(unique)}",
                    file_path=root_claude,
                    rule_reference=self.rule_reference,
                )
            ]
        else:
            return [
                CheckResult(
                    check_name=self.name,
                    severity=Severity.WARN,
                    message="No emphasis keywords (IMPORTANT, YOU MUST, etc.) found",
                    file_path=root_claude,
                    rule_reference=self.rule_reference,
                )
            ]


register(EmphasisKeywords())
