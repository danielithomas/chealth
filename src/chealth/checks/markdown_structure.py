"""Markdown structure check — headers and bullets present, not dense prose."""

from __future__ import annotations

import re

from chealth.checks import read_file_safe, register
from chealth.models import CheckContext, CheckResult, Severity

HEADER_PATTERN = re.compile(r"^#{1,6}\s", re.MULTILINE)
BULLET_PATTERN = re.compile(r"^\s*[-*+]\s", re.MULTILINE)
CODE_FENCE_PATTERN = re.compile(r"```[^\n]*\n.*?```", re.DOTALL)

# Threshold for consecutive non-structural lines indicating dense prose
DENSE_PROSE_THRESHOLD = 5


class MarkdownStructure:
    name = "markdown-structure"
    description = "Check for markdown headers, bullets, and detect dense prose"
    rule_reference = "Rule 3"

    def run(self, ctx: CheckContext) -> list[CheckResult]:
        results: list[CheckResult] = []

        for file_path in ctx.discovered_files:
            content = read_file_safe(file_path)
            if content is None:
                continue

            # Strip code blocks to avoid false positives
            stripped = CODE_FENCE_PATTERN.sub("", content)

            has_headers = bool(HEADER_PATTERN.search(stripped))
            has_bullets = bool(BULLET_PATTERN.search(stripped))
            has_dense_prose = self._detect_dense_prose(stripped)

            if has_headers and has_bullets and not has_dense_prose:
                severity = Severity.PASS
                message = "Well-structured with headers and bullets"
            elif has_headers or has_bullets:
                severity = Severity.WARN
                parts = []
                if not has_headers:
                    parts.append("no headers")
                if not has_bullets:
                    parts.append("no bullet points")
                if has_dense_prose:
                    parts.append("dense prose blocks detected")
                message = f"Partial structure: {', '.join(parts)}"
            else:
                severity = Severity.DANGER
                message = "No markdown structure (no headers or bullets)"

            results.append(
                CheckResult(
                    check_name=self.name,
                    severity=severity,
                    message=message,
                    file_path=file_path,
                    rule_reference=self.rule_reference,
                )
            )

        return results

    def _detect_dense_prose(self, content: str) -> bool:
        """Detect blocks of 5+ consecutive non-structural lines."""
        consecutive = 0
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped:
                consecutive = 0
                continue
            is_structural = (
                HEADER_PATTERN.match(line) is not None
                or BULLET_PATTERN.match(line) is not None
                or stripped.startswith("|")  # table rows
                or stripped.startswith("---")  # horizontal rules
                or stripped.startswith(">")  # blockquotes
            )
            if is_structural:
                consecutive = 0
            else:
                consecutive += 1
                if consecutive >= DENSE_PROSE_THRESHOLD:
                    return True
        return False


register(MarkdownStructure())
