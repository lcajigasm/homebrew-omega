#!/usr/bin/env python3
"""Point Formula/omega.rb at the latest public lcajigasm/omega release.

Rewrites the version embedded in each stable URL and the sha256 that follows
it. Checksums are taken from the release SHA256SUMS file and checked against
the downloaded archives. Exits 0 when the formula already matches.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

REPO = "lcajigasm/omega"
FORMULA = Path("Formula/omega.rb")
ASSETS = (
    "darwin_arm64",
    "darwin_amd64",
    "linux_arm64",
    "linux_amd64",
)
USER_AGENT = "homebrew-omega-formula-updater"


def fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def latest_release() -> tuple[str, str]:
    payload = json.loads(fetch(f"https://api.github.com/repos/{REPO}/releases/latest"))
    if payload.get("draft") or payload.get("prerelease"):
        raise SystemExit(f"latest release is not a final release: {payload.get('tag_name')}")
    tag = payload["tag_name"]
    version = tag[1:] if tag.startswith("v") else tag
    if not re.fullmatch(r"\d+\.\d+(?:\.\d+)*", version):
        raise SystemExit(f"refusing unexpected version {tag}")
    return tag, version


def verified_checksums(tag: str, version: str) -> dict[str, str]:
    sums_url = f"https://github.com/{REPO}/releases/download/{tag}/SHA256SUMS"
    checksums: dict[str, str] = {}
    for line in fetch(sums_url).decode().splitlines():
        line = line.strip()
        if not line:
            continue
        digest, name = line.split()
        checksums[name] = digest.lower()

    verified: dict[str, str] = {}
    for suffix in ASSETS:
        name = f"omega_{version}_{suffix}.tar.gz"
        expected = checksums.get(name)
        if expected is None:
            raise SystemExit(f"SHA256SUMS has no entry for {name}")
        url = f"https://github.com/{REPO}/releases/download/{tag}/{name}"
        actual = hashlib.sha256(fetch(url)).hexdigest()
        if actual != expected:
            raise SystemExit(f"checksum mismatch for {name}: downloaded {actual}, SHA256SUMS {expected}")
        print(f"verified {name} {actual}")
        verified[suffix] = actual
    return verified


def rewrite(text: str, version: str, checksums: dict[str, str]) -> str:
    updated = text
    for suffix, digest in checksums.items():
        pattern = re.compile(
            rf'(url "https://github\.com/{re.escape(REPO)}/releases/download/v)'
            rf'[^"/]+'
            rf'(/omega_)'
            rf'[^"_]+'
            rf'(_{re.escape(suffix)}\.tar\.gz"\n\s*sha256 ")'
            rf'[0-9a-fA-F]+'
            rf'(")'
        )
        replacement = rf"\g<1>{version}\g<2>{version}\g<3>{digest}\g<4>"
        updated, count = pattern.subn(replacement, updated, count=1)
        if count != 1:
            raise SystemExit(f"could not rewrite the {suffix} URL and sha256 in {FORMULA}")
    return updated


def main() -> int:
    tag, version = latest_release()
    checksums = verified_checksums(tag, version)
    original = FORMULA.read_text()
    updated = rewrite(original, version, checksums)
    if updated == original:
        print(f"formula already matches {tag}")
        return 0
    FORMULA.write_text(updated)
    print(f"updated formula to {tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
