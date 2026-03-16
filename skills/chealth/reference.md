# Best Practice Rules Reference

Condensed reference for the /chealth skill. Full guide: @docs/guide-claude-md-best-practices.md

## Structure & Size

1. **Keep it under 200 lines** — Longer files consume more context and reduce adherence. Split using imports or `.claude/rules/`.
2. **Include only universally applicable content** — Avoid instructions that won't matter across all tasks.
3. **Use markdown structure** — Headers and bullets, not dense prose. Claude scans structure like readers do.
4. **Modularise with imports** — Use `@path/to/import` syntax to keep root file lean.

## What to Include

5. **Document build and test commands** — Common bash commands, core files, code style, testing instructions.
6. **State architectural decisions and key file locations** — Key files, patterns, directory structure.
7. **Document repo etiquette** — Branch naming, merge/rebase preferences, project warnings.
8. **Use WHAT/WHY/HOW framework** — Tech stack (WHAT), purpose (WHY), workflows (HOW).

## Writing Style

9. **Be concrete, not vague** — Write instructions concrete enough to verify. "Use 2-space indentation" not "format code properly".
10. **Use emphasis keywords** — IMPORTANT, YOU MUST for critical rules. Improves adherence.
11. **Avoid contradictions** — Conflicting rules cause arbitrary behaviour. Review periodically across all files.

## Workflow

12. **Encode Explore > Plan > Code > Commit** — Proven sequence for complex tasks.
13. **Instruct incremental commits** — Commit after each discrete step for easy rollback.
14. **Specify test-run preferences** — Avoid costly full test suite runs during iteration.

## Scoping & Hierarchy

15. **Use subdirectory CLAUDE.md files** — Load on demand for rules scoped to specific parts.
16. **Use ~/.claude/CLAUDE.md for personal preferences** — Separate from project conventions.
17. **Check project CLAUDE.md into version control** — CLAUDE.local.md goes in .gitignore.

## Maintenance

18. **Treat it like a prompt — iterate** — Refine like any frequently used prompt. Remove ignored instructions.
19. **Use # shortcut to build as you work** — Press # during sessions to add instructions incrementally.
20. **Progressive disclosure** — Link out rather than bloat. Use separate files with self-descriptive names.
