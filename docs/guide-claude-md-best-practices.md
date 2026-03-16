# Synthesised Guide to Claude Best Practice

Top 20 Rules for a Great CLAUDE.md File

> A practical guide synthesised from Anthropic's official documentation, engineering blog, and community best practices.

---

## Structure & Size

### 1. Keep it under 200 lines
*(Source: Anthropic official docs)*

Target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence. If your instructions are growing large, split them using imports or `.claude/rules/` files.

### 2. Include only universally applicable content
*(Source: HumanLayer)*

Since CLAUDE.md goes into every single session, ensure that its contents are as universally applicable as possible. Avoid instructions that won't matter across all tasks — they distract the model when working on something unrelated.

**Example of what NOT to include:**
- Instructions on how to structure a specific database schema (irrelevant when working on unrelated tasks)

### 3. Use markdown structure — not dense prose
*(Source: Anthropic official docs)*

Use markdown headers and bullets to group related instructions. Claude scans structure the same way readers do: organised sections are easier to follow than dense paragraphs.

### 4. Modularise with imports
*(Source: Anthropic official docs)*

CLAUDE.md files can import additional files using `@path/to/import` syntax. Both relative and absolute paths are allowed. This keeps your root file lean while preserving detail where needed.

```markdown
# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Individual preferences: @~/.claude/my-project-instructions.md
```

---

## What to Include

### 5. Document your build and test commands
*(Source: Anthropic engineering blog)*

CLAUDE.md is the ideal place for documenting common bash commands, core files and utility functions, code style guidelines, testing instructions, and developer environment setup.

**Example:**
```markdown
# Bash Commands
- npm run build: Build the project
- npm run typecheck: Run the typechecker
- npm run test: Run the test suite
```

### 6. State architectural decisions and key file locations
*(Source: Anthropic engineering blog)*

Include key files or architectural patterns so Claude knows where to look.

**Example:**
```markdown
# Architecture
- State management is handled by Zustand; see src/stores for examples
- API handlers live in src/api/handlers/
- Shared utilities are in src/lib/
```

### 7. Document repo etiquette
*(Source: Anthropic engineering blog)*

Include repository etiquette such as branch naming conventions, merge vs. rebase preferences, and any unexpected behaviours or warnings particular to the project.

**Example:**
```markdown
# Repo Etiquette
- Branch naming: feature/short-description or fix/issue-number
- Always rebase onto main before raising a PR
- Do not force-push to shared branches
```

### 8. Use the WHAT / WHY / HOW framework
*(Source: HumanLayer)*

Structure your CLAUDE.md around three questions:

| Section | What to Cover |
|---|---|
| **WHAT** | The tech stack, project structure, codebase map |
| **WHY** | The purpose and function of different parts of the repo |
| **HOW** | Tools to use, how to run tests, how to verify changes |

---

## Writing Style

### 9. Be concrete, not vague
*(Source: Anthropic official docs)*

Write instructions that are concrete enough to verify.

| Instead of... | Write... |
|---|---|
| "Format code properly" | "Use 2-space indentation" |
| "Test your changes" | "Run `npm test` before committing" |
| "Keep files organised" | "API handlers live in `src/api/handlers/`" |

### 10. Use emphasis keywords for critical rules
*(Source: Anthropic engineering blog)*

At Anthropic, instructions are tuned by adding emphasis with **"IMPORTANT"** or **"YOU MUST"** to improve adherence. Run your CLAUDE.md through the [Anthropic Prompt Improver](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-improver) periodically.

**Example:**
```markdown
# Testing
- IMPORTANT: Always run tests before committing
- YOU MUST run the typechecker after any series of code changes
```

### 11. Avoid contradictions
*(Source: Anthropic official docs)*

If two rules contradict each other, Claude may pick one arbitrarily. Review your CLAUDE.md files — including nested subdirectory files and `.claude/rules/` — periodically to remove outdated or conflicting instructions.

---

## Workflow Instructions

### 12. Encode the Explore > Plan > Code > Commit workflow
*(Source: Anthropic engineering blog)*

Instruct Claude to follow this proven sequence for complex tasks:

1. **Explore** - Read relevant files without writing code yet
2. **Plan** - Use "think" or "think hard" to trigger extended thinking
3. **Code** - Implement the solution with inline verification
4. **Commit** - Commit the result and create a PR

**Thinking keyword hierarchy:**
`think` < `think hard` < `think harder` < `ultrathink`

Each level allocates progressively more thinking budget.

### 13. Instruct Claude to commit incrementally
*(Source: Community, informed by Anthropic practices)*

Instruct Claude to write commits as it goes for each task step. This way either Claude or you can revert to a previous state if something goes wrong.

**Example:**
```markdown
# Git Workflow
- Commit after completing each discrete task step
- Use conventional commit format: feat:, fix:, chore:, docs:
- Write descriptive commit messages explaining the why, not just the what
```

### 14. Specify test-run preferences
*(Source: Anthropic engineering blog)*

Be explicit about how tests should be run to avoid costly full test suite runs during iteration.

**Example:**
```markdown
# Testing
- Prefer running single tests rather than the whole test suite for performance
- Run: `npm test -- --testPathPattern=<filename>` for targeted testing
- Only run the full suite before committing
```

---

## Scoping & Hierarchy

### 15. Use subdirectory CLAUDE.md files for local rules
*(Source: Anthropic official docs)*

CLAUDE.md files in subdirectories load on demand when Claude reads files in those directories. Use this for rules scoped to specific parts of the codebase.

```
repo/
├── CLAUDE.md              # Project-wide rules
├── src/
│   └── api/
│       └── CLAUDE.md      # API-specific conventions
└── docs/
    └── CLAUDE.md          # Documentation conventions
```

### 16. Use `~/.claude/CLAUDE.md` for personal preferences
*(Source: Anthropic engineering blog)*

Place personal preferences in your home folder to apply them to all Claude sessions, separate from project-level conventions that are checked into git.

**Good candidates for `~/.claude/CLAUDE.md`:**
- Preferred coding style
- Personal tool aliases and shortcuts
- Communication style preferences (e.g. "Always explain your reasoning")

### 17. Check project-level CLAUDE.md into version control
*(Source: Anthropic engineering blog)*

| File | Purpose |
|---|---|
| `CLAUDE.md` | Shared project standards — commit to git |
| `CLAUDE.local.md` | Personal overrides — add to `.gitignore` |

This ensures the whole team benefits from accumulated CLAUDE.md improvements.

---

## Maintenance

### 18. Treat it like a prompt — iterate on it
*(Source: Anthropic engineering blog)*

CLAUDE.md files become part of Claude's prompts, so they should be refined like any frequently used prompt. A common mistake is adding extensive content without iterating on its effectiveness.

**Tips:**
- Run it through the [Anthropic Prompt Improver](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-improver)
- Test whether Claude actually follows each instruction
- Remove instructions Claude consistently ignores

### 19. Use the `#` shortcut to build it as you work
*(Source: Anthropic engineering blog)*

The fastest way to build up your CLAUDE.md is to press `#` during a session to give Claude an instruction it will automatically incorporate. Many engineers do this continuously while coding, then include CLAUDE.md changes in commits so the whole team benefits.

**Quick memory shortcut:**
```
# Always use functional components with hooks, never class components
```

### 20. Use progressive disclosure — link out rather than bloat
*(Source: HumanLayer)*

Instead of cramming everything into one file, use separate markdown files with self-descriptive names and reference them from your root CLAUDE.md. This keeps task-specific instructions out of every session unless they are actually needed.

**Example structure:**
```
.claude/
├── CLAUDE.md              # Root — short, universally applicable
└── rules/
    ├── database.md        # DB-specific conventions
    ├── testing.md         # Testing standards
    └── deployment.md      # Deployment checklist
```

---

## Quick Reference Checklist

Before committing your CLAUDE.md, run through this checklist:

- [ ] Under 200 lines in the root file
- [ ] Every instruction is universally applicable to all tasks
- [ ] Structured with markdown headers and bullets
- [ ] Build/test commands documented
- [ ] Key file locations and architecture noted
- [ ] Repo etiquette covered (branching, commits, PRs)
- [ ] Instructions are concrete and verifiable — not vague
- [ ] No contradictions between rules
- [ ] Critical rules emphasised with IMPORTANT or YOU MUST
- [ ] Committed to version control (project-level)
- [ ] Personal preferences separated into `~/.claude/CLAUDE.md`
- [ ] Task-specific content moved to subdirectory files or imports

---

## Key Sources

| Source | Type | URL |
|---|---|---|
| Claude Code: Best Practices for Agentic Coding | Anthropic Engineering Blog | https://www.anthropic.com/engineering/claude-code-best-practices |
| How Claude Remembers Your Project | Anthropic Official Docs | https://docs.anthropic.com/en/docs/claude-code/memory |
| How Anthropic Teams Use Claude Code | Anthropic Internal Insights | https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf |
| Writing a Good CLAUDE.md | HumanLayer Blog | https://www.humanlayer.dev/blog/writing-a-good-claude-md |

---

*Guide compiled March 2026. Sources biased towards Anthropic employees and official documentation.*
