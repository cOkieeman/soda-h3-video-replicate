"""插件清单、skill 结构与清洁检查。"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "h3-video-replicate"

MANIFESTS = [
    "plugin.json",
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".agents/plugins/marketplace.json",
]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class Manifests(unittest.TestCase):
    def test_all_parse_and_agree(self):
        seen = set()
        for rel in MANIFESTS:
            d = load(rel)
            seen.add((d["name"], d["version"], d["description"]))
            for item in d.get("plugins", []):
                seen.add((item["name"], item["version"], item["description"]))
        self.assertEqual(len(seen), 1, seen)
        name, version, _ = seen.pop()
        self.assertEqual((name, version), ("h3-video-replicate", "0.3.0"))

    def test_codex_overlay_points_at_skills(self):
        self.assertEqual(load(".codex-plugin/plugin.json")["skills"], "./skills/")

    def test_local_marketplace_source(self):
        entry = load(".agents/plugins/marketplace.json")["plugins"][0]
        self.assertEqual(entry["source"], {"source": "local", "path": "./"})

    def test_prompts_only_wording(self):
        for rel in MANIFESTS + ["skills/h3-video-replicate/agents/openai.yaml"]:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotRegex(text, "工作流副本|联动工作流|写入工作流", rel)


class Skill(unittest.TestCase):
    def setUp(self):
        self.text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    def test_frontmatter(self):
        m = re.match(r"---\n(.*?)\n---\n", self.text, re.S)
        self.assertIsNotNone(m)
        self.assertRegex(m.group(1), r"(?m)^name: h3-video-replicate$")
        self.assertRegex(m.group(1), r"(?m)^description: \S")

    def test_referenced_files_exist(self):
        refs = set(re.findall(r"(?:references|scripts)/[\w./-]+\.(?:md|py)", self.text))
        self.assertTrue(refs)
        missing = [r for r in sorted(refs) if not (SKILL / r).is_file()]
        self.assertEqual(missing, [])

    def test_single_file_is_current(self):
        single = (SKILL / "dist" / "h3-video-replicate.single.md").read_text(encoding="utf-8")
        for marker in ("模板默认分段", "读片命令", "开场菜单", "给用户的导演台操作步骤"):
            self.assertIn(marker, single)


class Clean(unittest.TestCase):
    SECRET = re.compile(r"sk-[A-Za-z0-9]{10,}|Bearer |api[_-]?key\s*[:=]|password\s*[:=]", re.I)
    PRIVATE = re.compile(r"ScreenRecording|ChatGPT 图像")

    def files(self):
        return [p for p in ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts]

    def test_no_leftovers(self):
        self.assertFalse((SKILL / "assets").exists())
        self.assertFalse((ROOT / "validation").exists())
        bundled = [p for p in self.files() if p.suffix == ".json" and p.relative_to(ROOT).as_posix() not in MANIFESTS]
        self.assertEqual(bundled, [])

    def test_no_secrets_or_private_names(self):
        for p in self.files():
            if p.suffix not in (".md", ".py", ".json", ".yaml"):
                continue
            text = p.read_text(encoding="utf-8")
            if p.name == "test_plugin.py":
                continue  # 本文件里有用来匹配的模式本身
            self.assertIsNone(self.SECRET.search(text), p)
            self.assertIsNone(self.PRIVATE.search(text), p)


if __name__ == "__main__":
    unittest.main()
