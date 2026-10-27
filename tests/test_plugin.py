"""Validate installable paths, generated instructions, and release round trips."""

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = "soda-h3-video-replicate"
SKILL = ROOT / "skills" / NAME
MANIFESTS = ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json",
             ".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json")


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def builder():
    spec = importlib.util.spec_from_file_location("single_builder", SKILL / "scripts" / "build_single.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script(script, *args):
    return subprocess.run([sys.executable, "-I", str(script), *map(str, args)],
                          capture_output=True, text=True, encoding="utf-8")


class InstallablePlugin(unittest.TestCase):
    def test_identities_and_install_paths(self):
        expected = load("plugin.json")
        for rel in MANIFESTS:
            data = load(rel)
            for item in [data, *data.get("plugins", [])]:
                self.assertEqual((item["name"], item["version"], item["description"]),
                                 (NAME, expected["version"], expected["description"]), rel)
        self.assertEqual(load(".codex-plugin/plugin.json")["skills"], "./skills/")
        for rel in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
            source = load(rel)["plugins"][0]["source"]
            self.assertEqual((ROOT / (source["path"] if isinstance(source, dict) else source)).resolve(), ROOT)

    def test_ui_assets_resolve_and_match(self):
        ui = load("plugin.json")["extensions"]["com.openai"]["interface"]
        self.assertEqual(ui, load(".codex-plugin/plugin.json")["interface"])
        for field in ("logo", "composerIcon"):
            path = (ROOT / ui[field]).resolve()
            self.assertTrue(path.is_relative_to(ROOT))
            box = [float(value) for value in ET.parse(path).getroot().attrib["viewBox"].split()]
            self.assertEqual(box[2], box[3])
            self.assertGreaterEqual(box[2], 48)


class MaintainedSkill(unittest.TestCase):
    def test_entry_and_references(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(text, rf"(?m)^name: {NAME}$")
        refs = set(re.findall(r"(?:references|scripts)/[\w./-]+\.(?:md|py)", text))
        self.assertTrue(refs)
        self.assertEqual([rel for rel in refs if not (SKILL / rel).is_file()], [])
        for name in ("core.md", "cursor-edit.md"):
            self.assertTrue((SKILL / "references" / "phrases" / name).is_file())
        self.assertEqual([p.name for p in (ROOT / "skills").iterdir() if p.is_dir()], [NAME])

    def test_single_edition_and_credit_boundary(self):
        module = builder()
        single = (SKILL / "dist" / f"{NAME}.single.md").read_text(encoding="utf-8")
        self.assertEqual(single, module.build_text())
        self.assertEqual(module.SECTIONS[-1], "acknowledgements.md")
        main, credits = single.split("<!-- references/acknowledgements.md -->")
        self.assertNotRegex(main, r"小优|Songssx|cOkieeman|wubo0927|xiaoyou")
        self.assertNotRegex(single, r"Administrator|个人开发项目|soda comfyui")
        visible = re.sub(r"https?://[^\s)<>]+", "", credits)
        self.assertNotRegex(visible, r"Songssx|cOkieeman|wubo0927")

    def test_fenced_headings_are_preserved(self):
        source = "# Section\n```text\n# literal\n```\n## Part"
        self.assertEqual(builder().demote_headings(source),
                         "## Section\n```text\n# literal\n```\n### Part")


class ReleaseRoundTrip(unittest.TestCase):
    def test_reproducible_standalone_archives(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            for attempt in range(2):
                result = run_script(ROOT / "scripts" / "package_release.py", "--output-dir", output)
                self.assertEqual(result.returncode, 0, result.stderr)
                hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir()}
                if attempt == 0:
                    first = hashes
                else:
                    self.assertEqual(first, hashes)
            for path in output.glob("*.zip"):
                with zipfile.ZipFile(path) as archive:
                    self.assertIsNone(archive.testzip())
                    self.assertFalse(any(".git" in Path(n).parts or "__pycache__" in Path(n).parts
                                         or "/h3-video-replicate/" in n for n in archive.namelist()))
                    if path.name.endswith("-plugin.zip"):
                        extracted = output / "plugin"
                        archive.extractall(extracted)
                        generated = extracted / "skills" / NAME / "dist" / f"{NAME}.single.md"
                        self.assertEqual(generated.read_bytes(), (output / f"{NAME}.single.md").read_bytes())
                        rebuilt = run_script(extracted / "scripts" / "package_release.py",
                                             "--output-dir", output / "rebuilt")
                        self.assertEqual(rebuilt.returncode, 0, rebuilt.stderr)
                    else:
                        self.assertIn(f"{NAME}/LICENSE", archive.namelist())
                        self.assertIn(f"{NAME}/NOTICE", archive.namelist())
                        archive.extractall(output / "skill")
                        planned = run_script(output / "skill" / NAME / "scripts" / "plan_segments.py",
                                             "--frames", "240", "--json")
                        self.assertEqual(planned.returncode, 0, planned.stderr)
                        self.assertEqual(json.loads(planned.stdout)["F"], 240)


if __name__ == "__main__":
    unittest.main()
