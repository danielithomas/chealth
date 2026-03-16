"""Line count check — CLAUDE.md under max_lines threshold."""

from __future__ import annotations

from chealth.checks import read_file_safe, register
from chealth.models import CheckContext, CheckResult, Severity


class LineCount:
    name = "line-count"
    description = "Check line count against threshold"
    rule_reference = "Rule 1"

    def run(self, ctx: CheckContext) -> list[CheckResult]:
        results: list[CheckResult] = []

        for file_path in ctx.discovered_files:
            content = read_file_safe(file_path)
            if content is None:
                continue

            lines = content.count("\n") + (1 if content and not content.endswith("\n") else 0)
            warn_threshold = int(ctx.max_lines * 1.2)

            if lines <= ctx.max_lines:
                severity = Severity.PASS
                message = f"{lines} lines (limit: {ctx.max_lines})"
            elif lines <= warn_threshold:
                severity = Severity.WARN
                message = f"{lines} lines exceeds {ctx.max_lines} limit (within 20% tolerance)"
            else:
                severity = Severity.DANGER
                message = f"{lines} lines far exceeds {ctx.max_lines} limit"

            results.append(
                CheckResult(
                    check_name=self.name,
                    severity=severity,
                    message=message,
                    file_path=file_path,
                    rule_reference=self.rule_reference,
                    details={"lines": lines, "max_lines": ctx.max_lines},
                )
            )

        return results


register(LineCount())
