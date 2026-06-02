from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from _common import DEMO, latest_artifact, relative_to_root, sha256sum


def tamper_file(source: Path) -> tuple[Path, int]:
    data = bytearray(source.read_bytes())
    if not data:
        raise SystemExit("Artifact is empty; cannot tamper with it.")

    offset = min(len(data) // 2, len(data) - 1)
    data[offset] ^= 0x01

    output_dir = DEMO / "tampered"
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / f"{source.stem}.tampered{source.suffix}"
    target.write_bytes(data)
    return target.resolve(), offset


def run_verify(artifact: Path, mode: str, repo: str | None) -> int:
    script = Path(__file__).resolve().parent / "verify_artifact.py"
    command = [sys.executable, str(script), str(artifact), "--mode", mode]
    if repo:
        command.extend(["--repo", repo])

    print(f"[tamper] running = {' '.join(command)}")
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    print(result.stdout.rstrip())
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy an artifact, flip one byte, and show verification failure."
    )
    parser.add_argument("artifact", nargs="?", help="Artifact path. Defaults to latest dist/*.whl.")
    parser.add_argument(
        "--mode",
        choices=["auto", "local", "github"],
        default="auto",
        help="Use github after the GitHub Actions attestation exists; local is for rehearsal.",
    )
    parser.add_argument("--repo", help="GitHub repository in OWNER/REPO form.")
    args = parser.parse_args()

    artifact = Path(args.artifact).resolve() if args.artifact else latest_artifact()
    mode = args.mode
    if mode == "auto":
        mode = "github" if args.repo else "local"

    tampered, offset = tamper_file(artifact)
    print(f"[tamper] original = {relative_to_root(artifact)}")
    print(f"[tamper] tampered = {relative_to_root(tampered)}")
    print(f"[tamper] offset   = {offset}")
    print(f"[tamper] original sha256 = {sha256sum(artifact)}")
    print(f"[tamper] tampered sha256 = {sha256sum(tampered)}")

    print("\n[tamper] Step 1: verify original artifact. Expected: PASS")
    original_status = run_verify(artifact, mode, args.repo)
    if original_status != 0:
        print("[tamper] original artifact did not verify; fix the setup before presenting tamper.")
        return 2

    print("\n[tamper] Step 2: verify tampered artifact. Expected: FAIL")
    tampered_status = run_verify(tampered, mode, args.repo)
    if tampered_status == 0:
        print("[tamper] unexpected PASS: tampered artifact verified")
        return 3

    print("[tamper] expected result: tampered artifact failed verification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
