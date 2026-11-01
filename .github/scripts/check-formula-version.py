#!/usr/bin/env python3
"""Fail when Formula/omega.rb does not match the latest omega release tag."""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

REPO = "lcajigasm/omega"
FORMULA = Path("Formula/omega.rb")
ASSETS = ("darwin_arm64", "darwin_amd64", "linux_arm64", "linux_amd64")
USER_AGENT = "homebrew-omega-formula-updater"


def fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def main() -> int:
    payload = json.loads(fetch(f"https://api.github.com/repos/{REPO}/releases/latest"))
    tag = payload["tag_name"]
    latest = tag[1:] if tag.startswith("v") else tag
    text = FORMULA.read_text()
    found = re.findall(
        r'url "https://github\.com/lcajigasm/omega/releases/download/v([^"/]+)/'
        r'omega_([^"_]+)_(darwin_arm64|darwin_amd64|linux_arm64|linux_amd64)\.tar\.gz"',
        text,
    )
    suffixes = [suffix for _, _, suffix in found]
    if sorted(suffixes) != sorted(ASSETS) or len(found) != len(ASSETS):
        print(f"formula is missing stable release URLs for {tag}: {found}", file=sys.stderr)
        return 1
    mismatched = [item for item in found if item[0] != latest or item[1] != latest]
    if mismatched:
        print(f"formula version does not match latest tag {tag}: {found}", file=sys.stderr)
        return 1
    print(f"formula version {latest} matches {tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
