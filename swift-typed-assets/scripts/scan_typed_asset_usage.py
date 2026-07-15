#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import re
import sys


PATTERNS = {
    "swiftui-image": re.compile(r'Image\(\s*"([^"]+)"\s*\)'),
    "uiimage-named": re.compile(r'UIImage\s*\(\s*named:\s*"([^"]+)"\s*\)'),
    "nsimage-named": re.compile(r'NSImage\s*\(\s*named:\s*"([^"]+)"\s*\)'),
    "uicolor-named": re.compile(r'UIColor\s*\(\s*named:\s*"([^"]+)"\s*\)'),
    "nscolor-named": re.compile(r'NSColor\s*\(\s*named:\s*"([^"]+)"\s*\)'),
}


def asset_inventory(root: pathlib.Path) -> set[str]:
    names: set[str] = set()
    for path in root.rglob("*.xcassets"):
        for child in path.rglob("Contents.json"):
            parent = child.parent.name
            for suffix in (".imageset", ".colorset", ".symbolset"):
                if parent.endswith(suffix):
                    names.add(parent[: -len(suffix)])
    return names


def scan_file(path: pathlib.Path, known_assets: set[str]) -> list[str]:
    findings: list[str] = []
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        return findings

    for kind, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            name = match.group(1)
            status = "known-asset" if name in known_assets else "unknown-asset"
            findings.append(f"{path}:{match.start()}:{kind}:{name}:{status}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Find string-based asset lookups that can be migrated to generated asset symbols.")
    parser.add_argument("root", help="Project root to scan")
    args = parser.parse_args()

    root = pathlib.Path(args.root).expanduser().resolve()
    if not root.exists():
        print(f"root not found: {root}", file=sys.stderr)
        return 1

    known_assets = asset_inventory(root)
    print(f"known-asset-count:{len(known_assets)}")

    file_globs = ("*.swift", "*.m", "*.mm", "*.h")
    findings: list[str] = []
    for glob in file_globs:
        for path in root.rglob(glob):
            findings.extend(scan_file(path, known_assets))

    for finding in findings:
        print(finding)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

