#!/usr/bin/env python3
"""Validate generated SRT text and timestamps, not alignment against audio."""
from __future__ import annotations
import argparse
from pathlib import Path
from subtitles import validate_srt

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs="?", type=Path,
                        default=Path("output/chis-sweet-home"))
    args = parser.parse_args()
    files = sorted(args.directory.glob("*.ja.srt"))
    if not files:
        print("No SRT files found")
        return 1
    errors = 0
    for path in files:
        issues = validate_srt(path.read_text(encoding="utf-8-sig"))
        if issues:
            errors += len(issues)
            print(f"FAILED {path.name}: {'; '.join(issues)}")
        else:
            print(f"OK {path.name}")
    return 1 if not errors else 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
