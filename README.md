# Japanese Anime Subtitle Toolkit 🇯🇵

Python tools for preparing Japanese subtitles to study anime with **asbplayer** and **Yomitan**.

**First anime:** *Chi's Sweet Home (2008)* (104 episodes). Start by generating episodes **001–010**.

> This repository contains **scripts, configuration, and synthetic tests only**, not copyrighted video or fan-subtitle dialogue. Check redistribution rights before uploading generated subtitles to Jimaku, GitHub, or elsewhere.

## Quick start (Windows, Python 3)

Clone this repository and open PowerShell in its folder:

```powershell
python scripts/build.py --start 1 --end 10
python scripts/validate.py output/chis-sweet-home
```

Alternatively, double-click `run_windows.bat`. The script downloads a combined Japanese ASS file from the [Kitsunekko mirror](https://github.com/Ajatt-Tools/kitsunekko-mirror), splits episodes, filters Japanese subtitle styles, and creates one UTF-8 `.ja.srt` per episode in `output/chis-sweet-home/`.

If download fails, obtain the matching `[Kamigami][Chi’s Sweet Home][01-16][JPN].ass` file from [Jimaku](https://jimaku.cc/entry/1004), save it in `sources/` under the same filename, and run:

```powershell
python scripts/build.py --start 1 --end 10 --no-download
```

**Important:** Generated timing has **not** been verified against AnimeVietSub. Test the exported files against the video in asbplayer; releases/encodes may have different offsets.

## Using subtitles with asbplayer

1. Open the video in a compatible web player.
2. In asbplayer, select **Load Subtitles** and choose the episode's `.ja.srt`.
3. Check sync and adjust Subtitle Offset if necessary.
4. Replay dialogue and use Yomitan to look up unfamiliar words.

## Project structure

```text
config/chis-sweet-home.json   Anime and source-group configuration
scripts/build.py              Download combined ASS and export per-episode SRT
scripts/subtitles.py          ASS parsing, splitting, conversion and validation
scripts/validate.py           Check exported files
tests/test_subtitles.py       Synthetic offline unit tests
metadata/episodes.csv         Tracking for episodes 001–104
.github/workflows/ci.yml     CI on push and pull request
docs/architecture.md         Processing design and limits
sources/                     Download cache, excluded from Git
output/                      Generated subtitles, excluded from Git
```

## Next milestones

- [ ] Generate SRTs for episodes 1–10.
- [ ] Check text and timing against the playback video.
- [ ] Verify source structure for episodes 17–104 before expanding.
- [ ] Review redistribution permissions before any public upload.
- [ ] Explore Jimaku integration only after confirming an upload API.

## Limitations

- Uses Python standard library; no `pip install` needed.
- Episode boundaries rely on a repeated opening line; unexpected input fails explicitly.
- CI tests code with synthetic fixtures; it does not download subtitles.
- No automated Jimaku upload or account-token storage is included.
