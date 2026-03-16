# Project Overview

This project uses Python with uv as the package manager.

## Architecture

- API handlers live in `src/api/handlers/`
- Shared utilities are in `src/lib/`
- Database models in `src/models/`

## Build & Test

- `uv run pytest` — run the test suite
- `uv run build` — build the project

## Git Workflow

- `main` is the primary branch
- Branch from `dev` for feature work
- Always rebase onto main before raising a PR

IMPORTANT: Always run tests before committing.
