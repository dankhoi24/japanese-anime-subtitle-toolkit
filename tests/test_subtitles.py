import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from subtitles import Cue, time_to_cs, cs_to_srt, clean_ass_text, parse_ass, split_episodes, render_srt, validate_srt

def sample_event(start, end, text, style="日文对话"):
    return f"Dialogue: 0,{start},{end},{style},NTP,0000,0000,0000,,{text}"

def timestamp(seconds):
    minutes, rem = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02}:{rem:02}.00"

class SubtitleTests(unittest.TestCase):
    def test_time_conversion(self):
        self.assertEqual(time_to_cs("0:01:54.12"), 11412)
        self.assertEqual(cs_to_srt(11412), "00:01:54,120")
    def test_clean(self):
        self.assertEqual(clean_ass_text(r"{\pos(3,4)}おなか\Nすいた"), "おなか\nすいた")
    def test_parse_commas(self):
        row = sample_event("0:00:02.00", "0:00:03.00", "ママ、どっち？")
        self.assertEqual(parse_ass(row)[0].text, "ママ、どっち？")
    def test_split_japanese_rebase_and_validate(self):
        lines = []
        for ep in range(3):
            base = ep * 176
            lines.append(sample_event(timestamp(base+1), timestamp(base+3), "ご機嫌で～す"))
            for i in range(11):
                lines.append(sample_event(timestamp(base+10+i*4),timestamp(base+12+i*4),f"例文{i}"))
            lines.append(sample_event(timestamp(base+10),timestamp(base+12),"中文","繁体对话"))
        parts = split_episodes(parse_ass("\n".join(lines)),episode_numbers=[1,2,3],
                               japanese_styles={"日文对话"},opening_line="ご機嫌で～す")
        for ep in (1,2,3):
            self.assertEqual(len(parts[ep]),12)
            self.assertEqual(parts[ep][0].start_cs,100)
            output = render_srt(parts[ep])
            self.assertNotIn("中文",output)
            self.assertEqual(validate_srt(output),[])
    def test_anchor_count_rejected(self):
        with self.assertRaisesRegex(ValueError, "opening anchors"):
            split_episodes([Cue(100,300,"日文对话","ご機嫌で～す")],
                           episode_numbers=[1,2],japanese_styles={"日文对话"},
                           opening_line="ご機嫌で～す")
    def test_invalid_srt(self):
        self.assertTrue(validate_srt("1\n00:00:03,000 --> 00:00:02,000\nbad\n"))

if __name__ == "__main__":
    unittest.main()
