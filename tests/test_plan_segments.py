"""plan_segments.py 的命令行行为。"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "soda-h3-video-replicate" / "scripts" / "plan_segments.py"


def run(*args):
    return subprocess.run(
        [sys.executable, "-I", str(SCRIPT), *args],
        capture_output=True, text=True, encoding="utf-8",
    )


def plan(*args):
    r = run(*args, "--json")
    if r.returncode:
        raise AssertionError(r.stderr)
    return json.loads(r.stdout)


def windows(d):
    return [(s["start"], s["end"]) for s in d["segments"]]


class DefaultConfig(unittest.TestCase):
    def test_ten_seconds(self):
        d = plan("--seconds", "10")
        self.assertEqual((d["F"], d["N"], d["E"], d["P"]), (240, 3, 243, 3))
        self.assertEqual(windows(d), [(0, 107), (68, 175), (136, 243)])

    def test_single_segment_needs_no_overlap(self):
        d = plan("--frames", "107")
        self.assertEqual(windows(d), [(0, 107)])
        self.assertEqual(d["segments"][0]["overlap_in"], 0)

    def test_one_frame_over_adds_short_tail(self):
        d = plan("--frames", "108")
        self.assertEqual(windows(d), [(0, 107), (68, 124)])
        self.assertEqual(d["P"], 16)

    def test_events_in_overlap_map_to_both_segments(self):
        d = plan("--seconds", "10", "--events", "2.9")
        hits = d["events"][0]["segments"]
        self.assertEqual([h["gen"] for h in hits], [1, 2])
        self.assertTrue(hits[0]["tail_overlap"])
        self.assertTrue(hits[1]["head_overlap"])

    def test_zero_overlap_windows_meet_without_repeating_boundary_event(self):
        d = plan("--frames", "214", "--overlap", "0", "--events", "107/24")
        self.assertEqual(windows(d), [(0, 107), (107, 214)])
        self.assertEqual((d["E"], d["P"]), (214, 0))
        hits = d["events"][0]["segments"]
        self.assertEqual([(h["gen"], h["local_frame"]) for h in hits], [(2, 0)])
        self.assertFalse(hits[0]["head_overlap"])
        self.assertFalse(hits[0]["tail_overlap"])

    def test_maximum_segment_length_is_accepted(self):
        d = plan("--frames", "3592", "--length", "3592")
        self.assertEqual(windows(d), [(0, 3592)])
        self.assertEqual(d["P"], 0)


class LegacyConfig(unittest.TestCase):
    def test_ninety_five(self):
        d = plan("--seconds", "10", "--length", "90", "--overlap", "5")
        self.assertEqual(windows(d), [(0, 90), (85, 175), (170, 243)])


class Invariants(unittest.TestCase):
    def test_sweep(self):
        for f in range(1, 400):
            d = plan("--frames", str(f))
            segs = d["segments"]
            self.assertGreaterEqual(d["E"], f)
            self.assertLessEqual(d["E"] - f, 16)
            for s in segs:
                self.assertLessEqual(s["length"], 107)
                self.assertEqual((s["length"] - 5) % 17, 0)
            self.assertEqual(sum(s["new_frames"] for s in segs), d["E"])


class Rejects(unittest.TestCase):
    def assert_friendly_error(self, *args):
        result = run(*args)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("错误：", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_illegal_overlap(self):
        self.assertEqual(run("--seconds", "5", "--overlap", "36").returncode, 1)

    def test_illegal_length(self):
        self.assertEqual(run("--seconds", "5", "--length", "108").returncode, 1)

    def test_length_above_node_limit(self):
        self.assert_friendly_error("--frames", "240", "--length", "3609")

    def test_non_positive_fps(self):
        for fps in ("0", "-1"):
            with self.subTest(fps=fps):
                self.assert_friendly_error("--frames", "240", "--fps", fps)

    def test_invalid_seconds(self):
        for seconds in ("invalid", "1/0"):
            with self.subTest(seconds=seconds):
                self.assert_friendly_error("--seconds", seconds)

    def test_invalid_events(self):
        for events in ("invalid", "1/0", "1,,2"):
            with self.subTest(events=events):
                self.assert_friendly_error("--frames", "240", "--events", events)

    def test_negative_event(self):
        self.assert_friendly_error("--frames", "240", "--events", "-0.1")

    def test_more_than_64_segments(self):
        r = run("--frames", "4392")
        self.assertEqual(r.returncode, 1)
        self.assertIn("64", r.stderr)

    def test_64_segments_fit(self):
        self.assertEqual(plan("--frames", "4391")["N"], 64)


if __name__ == "__main__":
    unittest.main()
