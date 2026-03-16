"""Gitignore check — CLAUDE.local.md should be in .gitignore if it exists."""

from __future__ import annotations

from pathlib import Path

from chealth.checks import read_file_safe, register
from chealth.models import CheckContext, CheckResult, Severity


class GitignoreCheck:
    name = "gitignore-check"
    description = "Check that CLAUDE.local.md is gitignored"
    rule_reference = "Rule 17"

    def run(self, ctx: CheckContext) -> list[CheckResult]:
        results: list[CheckResult] = []

        # Find all CLAUDE.local.md files
        local_files = [f for f in ctx.discovered_files if f.name == "CLAUDE.local.md"]
        if not local_files:
            return results

        # Read .gitignore
        gitignore_path = ctx.project_root / ".gitignore"
        gitignore_content = read_file_safe(gitignore_path) if gitignore_path.is_file() else None
        gitignore_patterns = self._parse_gitignore(gitignore_content) if gitignore_content else []

        for local_file in local_files:
            rel_path = str(local_file.relative_to(ctx.project_root)).replace("\\", "/")
            if self._is_ignored(rel_path, gitignore_patterns):
                results.append(
                    CheckResult(
                        check_name=self.name,
                        severity=Severity.PASS,
                        message="CLAUDE.local.md is gitignored",
                        file_path=local_file,
                        rule_reference=self.rule_reference,
                    )
                )
            else:
                results.append(
                    CheckResult(
                        check_name=self.name,
                        severity=Severity.WARN,
                        message="CLAUDE.local.md exists but is not in .gitignore",
                        file_path=local_file,
                        rule_reference=self.rule_reference,
                    )
                )

        return results

    def _parse_gitignore(self, content: str) -> list[str]:
        """Parse .gitignore into a list of patterns."""
        patterns = []
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
        return patterns

    def _is_ignored(self, rel_path: str, patterns: list[str]) -> bool:
        """Simple fnmatch-style check against gitignore patterns."""
        from fnmatch import fnmatch

        filename = rel_path.split("/")[-1]
        for pattern in patterns:
            # Direct filename match
            if fnmatch(filename, pattern):
                return True
            # Path match
            if fnmatch(rel_path, pattern):
                return True
            # Pattern with leading slash means root-relative
            if pattern.startswith("/") and fnmatch(rel_path, pattern.lstrip("/")):
                return True
        return False


register(GitignoreCheck())
