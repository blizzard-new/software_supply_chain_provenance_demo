from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

from _common import DEMO, command_exists, latest_artifact, relative_to_root, sha256sum


def verify_local(artifact: Path, manifest_path: Path) -> int:
    if not manifest_path.exists():
        print(f"[local] manifest not found: {manifest_path}")
        print("[local] create one first: python scripts/create_local_manifest.py")
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = manifest["subject"]["sha256"]
    actual = sha256sum(artifact)

    print("[local] WARNING: this is a classroom checksum policy, not a signed attestation.")
    print(f"[local] artifact = {relative_to_root(artifact)}")
    print(f"[local] expected = {expected}")
    print(f"[local] actual   = {actual}")

    if actual != expected:
        print("[local] verification FAILED: artifact digest does not match manifest")
        return 1

    print("[local] verification PASSED: artifact digest matches manifest")
    return 0


def verify_github(artifact: Path, repo: str | None) -> int:
    if not repo:
        print("[github] missing repository. Use --repo OWNER/REPO or set GITHUB_REPOSITORY.")
        return 2
    if not command_exists("gh"):
        print("[github] GitHub CLI was not found. Install gh and run: gh auth login")
        return 2

    command = [
        "gh",
        "attestation",
        "verify",
        str(artifact),
        "-R",
        repo,
        "--format",
        "json",
    ]
    print(f"[github] artifact = {relative_to_root(artifact)}")
    print(f"[github] sha256   = {sha256sum(artifact)}")
    print(f"[github] running  = {' '.join(command)}")
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    output = result.stdout.rstrip()
    if result.returncode != 0:
        print(output)
        print("[github] verification FAILED")
        return result.returncode

    try:
        records = json.loads(output)
    except json.JSONDecodeError:
        if output:
            print(output)
        print("[github] verification PASSED")
        return 0

    if records:
        verification = records[0].get("verificationResult", {})
        statement = verification.get("statement", {})
        predicate = statement.get("predicate", {})
        subject = statement.get("subject", [{}])[0]
        certificate = verification.get("signature", {}).get("certificate", {})
        timestamps = verification.get("verifiedTimestamps", [])
        builder = (
            predicate.get("runDetails", {}).get("builder", {}).get("id")
            or predicate.get("builder", {}).get("id")
            or "unknown"
        )
        print("[github] verification PASSED")
        print(f"[github] subject  = {subject.get('name', 'unknown')}")
        print(f"[github] digest   = {subject.get('digest', {}).get('sha256', 'unknown')}")
        print(f"[github] builder  = {builder}")
        print(f"[github] workflow = {certificate.get('githubWorkflowName', 'unknown')}")
        print(f"[github] commit   = {certificate.get('sourceRepositoryDigest', 'unknown')}")
        if timestamps:
            print(f"[github] tlog     = {timestamps[0].get('uri', 'unknown')}")
    else:
        print("[github] verification PASSED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify a build artifact with GitHub attestation or a local rehearsal manifest."
    )
    parser.add_argument("artifact", nargs="?", help="Artifact path. Defaults to latest dist/*.whl.")
    parser.add_argument(
        "--mode",
        choices=["auto", "local", "github"],
        default="auto",
        help="auto uses github when --repo is set, otherwise local.",
    )
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"))
    parser.add_argument(
        "--local-manifest",
        default=str(DEMO / "local_provenance.json"),
        help="Local rehearsal manifest path.",
    )
    args = parser.parse_args()

    artifact = Path(args.artifact).resolve() if args.artifact else latest_artifact()
    mode = args.mode
    if mode == "auto":
        mode = "github" if args.repo else "local"

    if mode == "github":
        return verify_github(artifact, args.repo)
    return verify_local(artifact, Path(args.local_manifest).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
