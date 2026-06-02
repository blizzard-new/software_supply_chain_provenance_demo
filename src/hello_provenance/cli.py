from __future__ import annotations

import argparse
import json
import platform
import sys
from typing import Sequence

from . import __version__


def build_payload(name: str) -> dict[str, str]:
    return {
        "app": "hello-provenance-demo",
        "version": __version__,
        "message": f"Hello, {name}. This artifact was built for a provenance demo.",
        "python": platform.python_version(),
        "platform": platform.platform(),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Print a small message from an attested build artifact."
    )
    parser.add_argument("--name", default="supply-chain reviewer")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable runtime metadata.",
    )
    args = parser.parse_args(argv)

    payload = build_payload(args.name)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(payload["message"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
