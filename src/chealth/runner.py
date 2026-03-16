"""Check orchestration and priority ordering."""

from __future__ import annotations

from pathlib import Path

from chealth.checks import get_all
from chealth.models import CheckContext, CheckResult, Severity

# These checks always run first to populate context
PRIORITY_CHECKS = ("file-discovery", "import-resolution")


def run_checks(
    project_root: Path,
    max_lines: int = 200,
    selected_checks: list[str] | None = None,
) -> list[CheckResult]:
    """Run all (or selected) checks and return results."""
    ctx = CheckContext(project_root=project_root.resolve(), max_lines=max_lines)
    all_checks = get_all()
    results: list[CheckResult] = []

    # Priority checks always run first to populate context
    for name in PRIORITY_CHECKS:
        check = all_checks.get(name)
        if check:
            findings = check.run(ctx)
            # Only include findings if check is selected (or no filter)
            if selected_checks is None or name in selected_checks:
                results.extend(findings)

    # Run remaining checks
    for name, check in all_checks.items():
        if name in PRIORITY_CHECKS:
            continue
        if selected_checks is not None and name not in selected_checks:
            continue
        results.extend(check.run(ctx))

    return results


def compute_exit_code(results: list[CheckResult]) -> int:
    """Compute exit code from results: 0=pass, 1=warn, 2=danger."""
    if not results:
        return 0
    worst = max(r.severity for r in results)
    return int(worst)
