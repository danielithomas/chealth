#!/usr/bin/env bash
# Thin wrapper to invoke chealth CLI via uv, falling back to python3/python.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if command -v uv &>/dev/null; then
    exec uv run --project "$SCRIPT_DIR" chealth "$@"
elif command -v python3 &>/dev/null; then
    exec python3 -m chealth "$@"
elif command -v python &>/dev/null; then
    exec python -m chealth "$@"
else
    echo "chealth: Python not found. Install Python 3.10+ or uv." >&2
    exit 1
fi
