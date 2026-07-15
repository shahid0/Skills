#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import shlex
import subprocess
import tempfile


def main() -> int:
    parser = argparse.ArgumentParser(description="Run devicectl with stable JSON output to a file.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments to pass after devicectl")
    parser.add_argument("--json-output", dest="json_output")
    ns = parser.parse_args()

    output = pathlib.Path(ns.json_output).expanduser().resolve() if ns.json_output else pathlib.Path(
        tempfile.mkstemp(prefix="devicectl-", suffix=".json")[1]
    )
    cmd = ["xcrun", "devicectl", "--json-output", str(output), *ns.args]
    print(" ".join(shlex.quote(part) for part in cmd))
    print(f"json-output:{output}")
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())

