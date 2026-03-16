"""Repo etiquette check — branching, commits, PRs keywords present."""

from __future__ import annotations

import re

from chealth.checks import read_file_safe, strip_code_blocks, register
from chealth.models import CheckContext, CheckResult, Severity

# Three keyword clusters (case-insensitive)
CLUSTERS = {
    "branching": re.compile(
        r"\b(branch|feature/|fix/|main|master|develop|release)\b", re.IGNORECASE
    ),
    "commits": re.compile(
        r"\b(commit|squash|conventional|amend|cherry.pick)\b", re.IGNORECASE
    ),
    "pull_requests": re.compile(
        r"\b(pull\s*request|PR\b|merge|rebase|review)", re.IGNORECASE
    ),
}


class RepoEtiquette:
    name = "repo-etiquette"
    description = "Check for branching, commit, and PR conventions"
    rule_reference = "Rule 7"

    def run(self, ctx: CheckContext) -> list[CheckResult]:
        root_claude = ctx.project_root / "CLAUDE.md"
        if root_claude not in ctx.discovered_files:
            return []

        content = read_file_safe(root_claude)
        if content is None:
            return []

        stripped = strip_code_blocks(content)
        matched_clusters = [
            name for name, pattern in CLUSTERS.items() if pattern.search(stripped)
        ]

        if len(matched_clusters) >= 2:
            return [
                CheckResult(
                    check_name=self.name,
                    severity=Severity.PASS,
                    message=f"Repo etiquette covered: {', '.join(matched_clusters)}",
                    file_path=root_claude,
                    rule_reference=self.rule_reference,
                )
            ]
        else:
            missing = [n for n in CLUSTERS if n not in matched_clusters]
            return [
                CheckResult(
                    check_name=self.name,
                    severity=Severity.WARN,
                    message=f"Missing repo etiquette topics: {', '.join(missing)}",
                    file_path=root_claude,
                    rule_reference=self.rule_reference,
                )
            ]


register(RepoEtiquette())
