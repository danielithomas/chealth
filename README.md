# chealth

CLI tool and Claude Code plugin to check CLAUDE.md health against [Anthropic best practices](docs/guide-claude-md-best-practices.md).

## Installation

### Claude Code Plugin (recommended)

From within a Claude Code session, add the marketplace and install:

```
/plugin marketplace add danielithomas/chealth
/plugin install chealth@danielithomas-chealth
```

Or use the interactive plugin browser:

```
/plugin
```

Navigate to the **Discover** tab after adding the marketplace.

Then run `/chealth` inside any Claude Code session. The plugin runs deterministic CLI checks followed by semantic analysis powered by Claude.

### CLI (standalone)

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/danielithomas/chealth.git
cd chealth
uv sync
```

## Usage

### CLI

```bash
# Check current directory
uv run chealth .

# Check a specific path
uv run chealth /path/to/project

# JSON output (for automation)
uv run chealth --format json .

# Run a specific check
uv run chealth --check line-count .
```

### Shell Wrappers

Platform wrappers are provided in `bin/`:

```bash
# Bash
./bin/chealth.sh .

# PowerShell
.\bin\chealth.ps1 .
```

## Checks

| # | Rule | Severity |
|---|------|----------|
| 1 | Keep it under 200 lines | WARN/DANGER |
| 2 | Include only universally applicable content | Semantic |
| 3 | Use markdown structure | WARN |
| 4 | Modularise with imports | Semantic |
| 5 | Document build and test commands | WARN |
| 6 | State architectural decisions and key file locations | Semantic |
| 7 | Document repo etiquette | Semantic |
| 8 | Use WHAT/WHY/HOW framework | Semantic |
| 9 | Be concrete, not vague | Semantic |
| 10 | Use emphasis keywords | INFO |
| 11 | Avoid contradictions | Semantic |
| 12 | Encode Explore > Plan > Code > Commit | Semantic |
| 13 | Instruct incremental commits | Semantic |
| 14 | Specify test-run preferences | Semantic |
| 15 | Use subdirectory CLAUDE.md files | Semantic |
| 16 | Use ~/.claude/CLAUDE.md for personal preferences | Semantic |
| 17 | Check project CLAUDE.md into version control | WARN |
| 18 | Treat it like a prompt — iterate | Semantic |
| 19 | Use # shortcut to build as you work | Semantic |
| 20 | Progressive disclosure | Semantic |

Checks marked **Semantic** are evaluated by Claude during plugin use, not by the CLI.

## License

MIT