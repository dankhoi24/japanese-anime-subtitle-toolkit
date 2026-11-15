"""Helpers to split multi-episode ASS subtitles and export Japanese SRT."""
from __future__ import annotations
from dataclasses import dataclass
from statistics import median
import re

OVERRIDE_RE = re.compile(r"\{\\[^}]*\}")
ASS_TIME_RE = re.compile(r"^(\d+):(\d\d):(\d\d)\.(\d{1,2})$")

@dataclass(frozen=True)
class Cue:
    start_cs: int
    end_cs: int
    style: str
    text: str

def time_to_cs(raw: str) -> int:
    match = ASS_TIME_RE.fullmatch(raw.strip())
    if not match:
        raise ValueError(f"Invalid ASS timestamp: {raw!r}")
    hours, minutes, seconds, fraction = match.groups()
    if not (0 <= int(minutes) < 60 and 0 <= int(seconds) < 60):
        raise ValueError(f"Invalid ASS timestamp: {raw!r}")
    return (int(hours) * 3600 + int(minutes) * 60 + int(seconds)) * 100 + int(fraction.ljust(2, "0"))

def cs_to_srt(cs: int) -> str:
    if cs < 0:
        raise ValueError("Timestamp must be nonnegative")
    ms = cs * 10
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1_000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def clean_ass_text(value: str) -> str:
    value = OVERRIDE_RE.sub("", value)
    value = value.replace(r"\N", "\n").replace(r"\n", "\n").replace(r"\h", " ")
    return "\n".join(line.strip() for line in value.splitlines()).strip()

def parse_ass(content: str) -> list[Cue]:
    result = []
    for line in content.lstrip("\ufeff").splitlines():
        if not line.startswith("Dialogue:"):
            continue
        parts = line.partition(":")[2].strip().split(",", 9)
        if len(parts) != 10:
            continue
        try:
            start, end = time_to_cs(parts[1]), time_to_cs(parts[2])
        except ValueError:
            continue
        if end > start:
            result.append(Cue(start, end, parts[3].strip(), clean_ass_text(parts[9])))
    return result

def split_episodes(cues: list[Cue], *, episode_numbers: list[int],
                   japanese_styles: set[str], opening_line: str) -> dict[int, list[Cue]]:
    anchors = sorted(c.start_cs for c in cues if c.style in japanese_styles and c.text == opening_line)
    if len(anchors) != len(episode_numbers):
        raise ValueError(f"Expected {len(episode_numbers)} opening anchors, got {len(anchors)}")
    gaps = [b - a for a, b in zip(anchors, anchors[1:])]
    if not gaps or any(not 17_000 <= gap <= 18_000 for gap in gaps):
        raise ValueError("Opening positions are irregular; refusing to guess episode boundaries")
    base = anchors[0]
    starts = [a - base for a in anchors]
    bounds = [*starts, starts[-1] + round(median(gaps))]
    result = {}
    for index, episode in enumerate(episode_numbers):
        begin, end = bounds[index:index+2]
        segment = []
        for cue in cues:
            if cue.style not in japanese_styles or not cue.text or cue.end_cs <= begin or cue.start_cs >= end:
                continue
            start = max(0, cue.start_cs - begin)
            stop = min(end - begin, cue.end_cs - begin)
            if stop > start:
                segment.append(Cue(start, stop, cue.style, cue.text))
        segment.sort(key=lambda x: (x.start_cs, x.end_cs))
        if len(segment) < 10:
            raise ValueError(f"Episode {episode:03} has only {len(segment)} cues")
        result[episode] = segment
    return result

def render_srt(cues: list[Cue]) -> str:
    return "\n\n".join(
        f"{i}\n{cs_to_srt(c.start_cs)} --> {cs_to_srt(c.end_cs)}\n{c.text}"
        for i, c in enumerate(cues, 1)
    ) + "\n"

def validate_srt(content: str, *, max_duration_cs: int = 19_000) -> list[str]:
    issues = []
    blocks = [x for x in content.strip().split("\n\n") if x.strip()]
    if not blocks:
        return ["No subtitles found"]
    previous = -1
    for number, block in enumerate(blocks, 1):
        lines = block.splitlines()
        if len(lines) < 3 or lines[0] != str(number):
            issues.append(f"Cue {number}: missing index or text")
            continue
        match = re.fullmatch(r"(\d\d):(\d\d):(\d\d),(\d{3}) --> (\d\d):(\d\d):(\d\d),(\d{3})", lines[1])
        if not match:
            issues.append(f"Cue {number}: invalid timestamp")
            continue
        fields = list(map(int, match.groups()))
        start = (fields[0] * 3600 + fields[1] * 60 + fields[2]) * 100 + fields[3] // 10
        end = (fields[4] * 3600 + fields[5] * 60 + fields[6]) * 100 + fields[7] // 10
        if start < previous or end <= start or end > max_duration_cs:
            issues.append(f"Cue {number}: disordered, invalid, or too long")
        previous = start
    return issues
