"""CLI entry point for chealth."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from chealth import __version__
from chealth.formatters import format_json, format_text
from chealth.runner import compute_exit_code, run_checks


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chealth",
        description="Check CLAUDE.md health against Anthropic best practices",
    )
    parser.add_argument(
        "--version", action="version", version=f"chealth {__version__}"
    )
    parser.add_argument(
        "--check",
        action="append",
        dest="checks",
        metavar="NAME",
        help="Run only the named check (repeatable)",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        dest="output_format",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=200,
        metavar="N",
        help="Line count threshold (default: 200)",
    )
    parser.add_argument(
        "--exit-zero",
        action="store_true",
        default=False,
        help="Always exit 0 (report severity in output only)",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Project root to check (default: current directory)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point. Returns exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    project_root = Path(args.path).resolve()
    if not project_root.is_dir():
        print(f"chealth: not a directory: {args.path}", file=sys.stderr)
        return 2

    # Import all check modules to trigger registration
    _load_checks()

    results = run_checks(
        project_root=project_root,
        max_lines=args.max_lines,
        selected_checks=args.checks,
    )

    if args.output_format == "json":
        output = format_json(results, project_root)
    else:
        output = format_text(results, project_root)

    print(output, end="")
    return 0 if args.exit_zero else compute_exit_code(results)


def _load_checks() -> None:
    """Import all check modules to trigger registration."""
    import chealth.checks.file_discovery  # noqa: F401
    import chealth.checks.import_resolution  # noqa: F401
    import chealth.checks.line_count  # noqa: F401
    import chealth.checks.markdown_structure  # noqa: F401
    import chealth.checks.gitignore_check  # noqa: F401
    import chealth.checks.build_commands  # noqa: F401
    import chealth.checks.emphasis_keywords  # noqa: F401
    import chealth.checks.architecture_paths  # noqa: F401
    import chealth.checks.repo_etiquette  # noqa: F401
    import chealth.checks.what_why_how  # noqa: F401
    import chealth.checks.progressive_disclosure  # noqa: F401
    import chealth.checks.universal_applicability  # noqa: F401
