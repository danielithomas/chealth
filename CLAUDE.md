# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

chealth is a CLI tool and Claude Code plugin that checks CLAUDE.md files against Anthropic best practices (20 rules). The CLI runs deterministic checks; the plugin skill adds semantic analysis powered by Claude.

## Language & Tooling

- **Language:** Python 3.10+
- **Package manager:** uv
- **Build backend:** hatchling

## Build & Test

- `uv run chealth .` — check this project's CLAUDE.md
- `uv run chealth --format json .` — JSON output for automation
- `uv run chealth --check line-count .` — run a specific check only
- `uv run pytest` — run all tests
- `uv run pytest tests/test_checks/test_line_count.py` — run a single test file

## Architecture

### Check System

Checks implement a `Check` Protocol (structural typing, no inheritance) with `name`, `description`, `rule_reference` attributes and a `run(ctx: CheckContext) -> list[CheckResult]` method. Each check lives in its own module under `src/chealth/checks/` and self-registers via `@register()` at import time. All check modules must be imported in `cli.py:_load_checks()` to trigger registration.

### Two-Phase Execution (`runner.py`)

1. **Priority checks** always run first regardless of `--check` filters: `file-discovery` populates `ctx.discovered_files`, `import-resolution` populates `ctx.import_targets`. These hydrate `CheckContext` for all subsequent checks.
2. **Standard checks** run after context is populated, respecting any `--check` filter.

Exit codes: 0 = all pass, 1 = worst is WARN, 2 = worst is DANGER. `Severity` is an IntEnum enabling `max()` to compute the worst result.

### Key Utilities (`checks/__init__.py`)

- `read_file_safe(path)` — tries utf-8, utf-8-sig, latin-1 encodings
- `strip_code_blocks(content)` — removes fenced code blocks to prevent false positives in pattern-matching checks

### Plugin Integration

`.claude-plugin/plugin.json` declares the skill. `skills/chealth/SKILL.md` defines the plugin workflow: run deterministic CLI checks (JSON), then perform semantic analysis using `skills/chealth/reference.md` (the 20-rule guide). Each check's `rule_reference` traces back to a specific best-practice rule.

## Adding a New Check

1. Create `src/chealth/checks/your_check.py` with a class implementing the Check protocol
2. Call `register(YourCheck())` at module level
3. Import the module in `cli.py:_load_checks()`
4. Add tests in `tests/test_checks/test_your_check.py`

## Version Management

Version `0.1.0` is defined in 4 places that MUST be kept in sync:

1. `pyproject.toml` — `version`
2. `.claude-plugin/plugin.json` — `version`
3. `skills/chealth/SKILL.md` — frontmatter `version`
4. `src/chealth/__init__.py` — `__version__`

When bumping the version, update all 4 files.

## Git Workflow

- `main` is the primary branch
- Branch from `main` for feature work
