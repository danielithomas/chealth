"""Universal applicability check — flag overly specific patterns in root CLAUDE.md."""

from __future__ import annotations

import re

from chealth.checks import read_file_safe, strip_code_blocks, register
from chealth.models import CheckContext, CheckResult, Severity

# Patterns that indicate overly specific content in root CLAUDE.md
SPECIFIC_PATTERNS = {
    "SQL statements": re.compile(
        r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE TABLE|ALTER TABLE|DROP TABLE)\s",
        re.IGNORECASE,
    ),
    "API URLs": re.compile(
        r"https?://(?:localhost|127\.0\.0\.1|api\.|staging\.|prod\.)\S+"
    ),
    "IP addresses": re.compile(
        r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    ),
    "API key patterns": re.compile(
        r"\b(?:api[_-]?key|secret[_-]?key|access[_-]?token)\s*[=:]\s*['\"][^'\"]+['\"]",
        re.IGNORECASE,
    ),
    "Hardcoded ports": re.compile(
        r"(?:port|PORT)\s*[=:]\s*\d{4,5}\b"
    ),
    "Database connection strings": re.compile(
        r"(?:postgres|mysql|mongodb|redis)://\S+", re.IGNORECASE
    ),
}


class UniversalApplicability:
    name = "universal-applicability"
    description = "Flag overly specific patterns in root CLAUDE.md"
    rule_reference = "Rule 2"

    def run(self, ctx: CheckContext) -> list[CheckResult]:
        root_claude = ctx.project_root / "CLAUDE.md"
        if root_claude not in ctx.discovered_files:
            return []

        content = read_file_safe(root_claude)
        if content is None:
            return []

        stripped = strip_code_blocks(content)
        found = [
            name
            for name, pattern in SPECIFIC_PATTERNS.items()
            if pattern.search(stripped)
        ]

        if not found:
            severity = Severity.PASS
            message = "Content appears universally applicable"
        elif len(found) <= 2:
            severity = Severity.WARN
            message = f"Potentially overly specific content: {', '.join(found)}"
        else:
            severity = Severity.DANGER
            message = f"Multiple overly specific patterns: {', '.join(found)}"

        return [
            CheckResult(
                check_name=self.name,
                severity=severity,
                message=message,
                file_path=root_claude,
                rule_reference=self.rule_reference,
                details={"patterns_found": found},
            )
        ]


register(UniversalApplicability())
