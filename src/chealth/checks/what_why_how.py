"""WHAT/WHY/HOW coverage check — keyword clusters for tech stack, purpose, workflow."""

from __future__ import annotations

import re

from chealth.checks import read_file_safe, strip_code_blocks, register
from chealth.models import CheckContext, CheckResult, Severity

CLUSTERS = {
    "WHAT": re.compile(
        r"\b(stack|framework|language|architecture|structure|typescript|python|react|"
        r"database|api|frontend|backend|monorepo)\b",
        re.IGNORECASE,
    ),
    "WHY": re.compile(
        r"\b(purpose|goal|overview|context|mission|motivation|objective|"
        r"responsible for|designed to)\b",
        re.IGNORECASE,
    ),
    "HOW": re.compile(
        r"\b(run|build|test|deploy|command|workflow|install|setup|start|"
        r"execute|invoke|compile)\b",
        re.IGNORECASE,
    ),
}


class WhatWhyHow:
    name = "what-why-how"
    description = "Check for WHAT/WHY/HOW framework coverage"
    rule_reference = "Rule 8"

    def run(self, ctx: CheckContext) -> list[CheckResult]:
        root_claude = ctx.project_root / "CLAUDE.md"
        if root_claude not in ctx.discovered_files:
            return []

        content = read_file_safe(root_claude)
        if content is None:
            return []

        stripped = strip_code_blocks(content)
        matched = [name for name, pattern in CLUSTERS.items() if pattern.search(stripped)]
        missing = [name for name in CLUSTERS if name not in matched]

        if len(missing) == 0:
            severity = Severity.PASS
            message = "WHAT/WHY/HOW framework covered"
        elif len(missing) <= 2:
            severity = Severity.WARN
            message = f"Missing coverage: {', '.join(missing)}"
        else:
            severity = Severity.DANGER
            message = "No WHAT/WHY/HOW coverage found"

        return [
            CheckResult(
                check_name=self.name,
                severity=severity,
                message=message,
                file_path=root_claude,
                rule_reference=self.rule_reference,
                details={"matched": matched, "missing": missing},
            )
        ]


register(WhatWhyHow())
