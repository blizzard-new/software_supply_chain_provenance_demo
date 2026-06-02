from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from _common import DEMO, ROOT, git_value, latest_artifact, relative_to_root, sha256sum


def build_manifest(artifact: Path) -> dict[str, object]:
    return {
        "schema_version": "teaching-local-provenance-v1",
        "warning": (
            "This local manifest is only for classroom rehearsal. "
            "Real provenance should be cryptographically signed and verified "
            "with GitHub artifact attestations or another Sigstore/in-toto flow."
        ),
        "subject": {
            "name": artifact.name,
            "path": relative_to_root(artifact),
            "sha256": sha256sum(artifact),
        },
        "source": {
            "repository": git_value(["config", "--get", "remote.origin.url"], str(ROOT)),
            "commit": git_value(["rev-parse", "HEAD"], "not-a-git-repository"),
        },
        "builder": {
            "kind": "local-python-build",
            "command": "python -m build",
            "workflow_equivalent": ".github/workflows/build-and-attest.yml",
        },
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a local teaching manifest for the latest dist artifact."
    )
    parser.add_argument("artifact", nargs="?", help="Artifact path. Defaults to latest dist/*.whl.")
    parser.add_argument(
        "--output",
        default=str(DEMO / "local_provenance.json"),
        help="Manifest output path.",
    )
    args = parser.parse_args()

    artifact = Path(args.artifact).resolve() if args.artifact else latest_artifact()
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(build_manifest(artifact), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"[manifest] artifact = {relative_to_root(artifact)}")
    print(f"[manifest] sha256   = {sha256sum(artifact)}")
    print(f"[manifest] wrote    = {relative_to_root(output)}")
    print("[manifest] note     = local rehearsal only; use GitHub attestation for real provenance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
