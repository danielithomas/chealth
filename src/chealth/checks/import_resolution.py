"""Import resolution check — verify @path references resolve to existing files."""

from __future__ import annotations

import re
from pathlib import Path

from chealth.checks import read_file_safe, register
from chealth.models import CheckContext, CheckResult, Severity

# Match @path references that contain / or end with .md (avoid matching emails/@mentions)
IMPORT_PATTERN = re.compile(r"@((?:[^\s@]+/[^\s@]*)|(?:[^\s@]+\.md))")


class ImportResolution:
    name = "import-resolution"
    description = "Verify @path/to/import targets exist on disk"
    rule_reference = "Rule 4"

    def run(self, ctx: CheckContext) -> list[CheckResult]:
        results: list[CheckResult] = []
        visited: set[Path] = set()

        for file_path in list(ctx.discovered_files):
            self._check_file(file_path, ctx, results, visited)

        return results

    def _check_file(
        self,
        file_path: Path,
        ctx: CheckContext,
        results: list[CheckResult],
        visited: set[Path],
    ) -> None:
        resolved = file_path.resolve()
        if resolved in visited:
            return
        visited.add(resolved)

        content = read_file_safe(file_path)
        if content is None:
            return

        imports = IMPORT_PATTERN.findall(content)
        if not imports:
            return

        missing: list[str] = []
        resolved_targets: list[Path] = []

        for imp in imports:
            # Resolve relative to file's directory
            target = (file_path.parent / imp).resolve()
            if target.is_file():
                resolved_targets.append(target)
                # Deep check: add resolved targets to discovered files
                if target not in ctx.discovered_files:
                    ctx.discovered_files.append(target)
                # Recursively check the imported file
                self._check_file(target, ctx, results, visited)
            else:
                missing.append(imp)

        # Track imports in context
        ctx.import_targets[file_path] = resolved_targets

        if missing:
            results.append(
                CheckResult(
                    check_name=self.name,
                    severity=Severity.DANGER,
                    message=f"Broken import(s): {', '.join(missing)}",
                    file_path=file_path,
                    rule_reference=self.rule_reference,
                    details={"missing": missing},
                )
            )
        else:
            results.append(
                CheckResult(
                    check_name=self.name,
                    severity=Severity.PASS,
                    message=f"All {len(imports)} import(s) resolved",
                    file_path=file_path,
                    rule_reference=self.rule_reference,
                )
            )


register(ImportResolution())
