#!/usr/bin/env python3
"""Build per-episode Japanese SRT files, using only Python's standard library."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen
from subtitles import parse_ass, split_episodes, render_srt, validate_srt

ROOT = Path(__file__).resolve().parents[1]

def source_url(path: str, repository: str) -> str:
    return ("https://raw.githubusercontent.com/" + repository + "/main/"
            + "/".join(quote(piece, safe="") for piece in path.split("/")))

def get_source(group: dict, config: dict, source_dir: Path, no_download: bool) -> tuple[Path, str]:
    rel = config["source_path_template"].format(first=group["first"], last=group["last"])
    dest = source_dir / Path(rel).name
    url = source_url(rel, config["source_repository"])
    if not dest.is_file():
        if no_download:
            raise FileNotFoundError(f"Missing {dest}; save original ASS locally or remove --no-download")
        source_dir.mkdir(parents=True, exist_ok=True)
        print(f"Downloading source {group['first']}-{group['last']}: {url}")
        with urlopen(Request(url, headers={"User-Agent": "anime-subtitle-toolkit/0.1"}), timeout=35) as response:
            binary = response.read()
        if not binary.lstrip(b"\xef\xbb\xbf").startswith(b"[Script Info]"):
            raise ValueError("Downloaded source is not ASS")
        dest.write_bytes(binary)
    return dest, url

def main() -> int:
    parser = argparse.ArgumentParser(description="Convert combined ASS to individual Japanese SRT files")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=10)
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--source-dir", type=Path, default=ROOT / "sources")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "output" / "chis-sweet-home")
    args = parser.parse_args()
    config = json.loads((ROOT / "config" / "chis-sweet-home.json").read_text(encoding="utf-8"))
    if not 1 <= args.start <= args.end <= config["total_episodes"]:
        parser.error("Episode range must be within 1..104")
    files, records = [], []
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for group in config["groups"]:
        if group["last"] < args.start or group["first"] > args.end:
            continue
        source, url = get_source(group, config, args.source_dir, args.no_download)
        binary = source.read_bytes()
        cues = parse_ass(binary.decode("utf-8-sig"))
        episodes = list(range(group["first"], group["last"] + 1))
        segmented = split_episodes(cues, episode_numbers=episodes,
                                   japanese_styles=set(config["japanese_styles"]),
                                   opening_line=config["opening_anchor"])
        for episode, segment in sorted(segmented.items()):
            if not args.start <= episode <= args.end:
                continue
            filename = args.output_dir / f"Chi's Sweet Home - {episode:03}.ja.srt"
            content = render_srt(segment)
            issues = validate_srt(content)
            if issues:
                raise ValueError(f"Invalid episode {episode}: {issues}")
            filename.write_text(content, encoding="utf-8", newline="\n")
            files.append(filename)
            records.append(dict(episode=f"{episode:03}", cues=len(segment),
                                source_url=url, source_sha256=hashlib.sha256(binary).hexdigest(),
                                status="generated_not_audio_verified"))
            print(f"{episode:03}: {len(segment)} cues -> {filename.name}")
    if len(files) != args.end - args.start + 1:
        raise RuntimeError(f"Generated {len(files)} files but expected {args.end - args.start + 1}")
    with (args.output_dir / "build-manifest.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print("Export completed. Verify audio alignment and redistribution rights before sharing.")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
