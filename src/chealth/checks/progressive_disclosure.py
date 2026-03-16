"""Progressive disclosure check — large root file with no modularization."""

from __future__ import annotations

from chealth.checks import read_file_safe, register
from chealth.models import CheckContext, CheckResult, Severity

DISCLOSURE_THRESHOLD = 100  # lines


class ProgressiveDisclosure:
    name = "progressive-disclosure"
    description = "Check if large root files use imports or subdirectory files"
    rule_reference = "Rule 20"

    def run(self, ctx: CheckContext) -> list[CheckResult]:
        root_claude = ctx.project_root / "CLAUDE.md"
        if root_claude not in ctx.discovered_files:
            return []

        content = read_file_safe(root_claude)
        if content is None:
            return []

        line_count = content.count("\n") + (1 if content and not content.endswith("\n") else 0)
        if line_count <= DISCLOSURE_THRESHOLD:
            return [
                CheckResult(
                    check_name=self.name,
                    severity=Severity.PASS,
                    message=f"Root file is {line_count} lines — no modularization needed",
                    file_path=root_claude,
                    rule_reference=self.rule_reference,
                )
            ]

        has_imports = bool(ctx.import_targets.get(root_claude))
        has_subdir_files = any(
            f != root_claude and f.name == "CLAUDE.md"
            for f in ctx.discovered_files
        )
        has_rules_files = any(
            ".claude" in str(f) and "rules" in str(f)
            for f in ctx.discovered_files
        )

        if has_imports or has_subdir_files or has_rules_files:
            return [
                CheckResult(
                    check_name=self.name,
                    severity=Severity.PASS,
                    message=f"Root file is {line_count} lines but uses modularization",
                    file_path=root_claude,
                    rule_reference=self.rule_reference,
                )
            ]
        else:
            return [
                CheckResult(
                    check_name=self.name,
                    severity=Severity.WARN,
                    message=f"Root file is {line_count} lines with no imports, subdirectory files, or .claude/rules/ — consider splitting",
                    file_path=root_claude,
                    rule_reference=self.rule_reference,
                )
            ]


register(ProgressiveDisclosure())
