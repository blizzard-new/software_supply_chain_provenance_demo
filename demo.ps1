param(
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"

if (-not $SkipInstall) {
    python -m pip install -q build
    python -m pip install -q -e .
}

python -m unittest discover -s tests
python -m build
python scripts/create_local_manifest.py
python scripts/verify_artifact.py --mode local
python scripts/tamper_demo.py --mode local
