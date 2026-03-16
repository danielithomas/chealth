"""Architecture paths check — path-like references present in root CLAUDE.md."""

from __future__ import annotations

import re

from chealth.checks import read_file_safe, strip_code_blocks, register
from chealth.models import CheckContext, CheckResult, Severity

# Match path-like references (e.g. src/, lib/utils.ts, ./config)
# Filter out URLs by requiring no :// before the path
PATH_PATTERN = re.compile(
    r"(?<!\w://)(?<!\w://\w)"  # negative lookbehind for URLs
    r"(?:`[^`]*(?:\./|[\w-]+/[\w.-]+)[^`]*`"  # paths in backticks
    r"|(?:^|\s)(?:\./|[\w-]+/[\w.-]+))"  # bare paths
)

# URL pattern to filter false positives
URL_PATTERN = re.compile(r"https?://\S+")


class ArchitecturePaths:
    name = "architecture-paths"
    description = "Check for file path references documenting project structure"
    rule_reference = "Rule 6"

    def run(self, ctx: CheckContext) -> list[CheckResult]:
        root_claude = ctx.project_root / "CLAUDE.md"
        if root_claude not in ctx.discovered_files:
            return []

        content = read_file_safe(root_claude)
        if content is None:
            return []

        # Remove URLs first, then strip code blocks
        no_urls = URL_PATTERN.sub("", content)
        stripped = strip_code_blocks(no_urls)

        matches = PATH_PATTERN.findall(stripped)

        if matches:
            return [
                CheckResult(
                    check_name=self.name,
                    severity=Severity.PASS,
                    message="File path references found documenting project structure",
                    file_path=root_claude,
                    rule_reference=self.rule_reference,
                )
            ]
        else:
            return [
                CheckResult(
                    check_name=self.name,
                    severity=Severity.WARN,
                    message="No file path references found — consider documenting key file locations",
                    file_path=root_claude,
                    rule_reference=self.rule_reference,
                )
            ]


register(ArchitecturePaths())
