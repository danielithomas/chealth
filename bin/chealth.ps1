# Thin wrapper to invoke chealth CLI via uv, falling back to python3/python.
$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent (Split-Path -Parent $PSCommandPath)

if (Get-Command uv -ErrorAction SilentlyContinue) {
    & uv run --project $ScriptDir chealth @args
    exit $LASTEXITCODE
}
elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    & python3 -m chealth @args
    exit $LASTEXITCODE
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python -m chealth @args
    exit $LASTEXITCODE
}
else {
    Write-Error "chealth: Python not found. Install Python 3.10+ or uv."
    exit 1
}
