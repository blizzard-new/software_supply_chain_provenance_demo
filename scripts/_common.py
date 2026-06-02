from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DEMO = ROOT / ".demo"


def sha256sum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def latest_artifact() -> Path:
    candidates = sorted(DIST.glob("*.whl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        candidates = sorted(DIST.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise SystemExit("No artifact found in dist/. Run: python -m build")
    return candidates[0].resolve()


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def git_value(args: list[str], default: str) -> str:
    command = ["git", *args]
    result = subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    if result.returncode != 0:
        return default
    value = result.stdout.strip()
    return value or default


def relative_to_root(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path.resolve())
