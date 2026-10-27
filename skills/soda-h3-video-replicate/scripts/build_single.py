#!/usr/bin/env python3
"""Build the chat-friendly edition from the maintained skill documents."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist" / "soda-h3-video-replicate.single.md"
SECTIONS = (
    "intake.md",
    "timeline.md",
    "prompt-writing.md",
    "cinematography.md",
    "delivery.md",
    "director.md",
    "quality-check.md",
    "phrases/core.md",
    "phrases/cursor-edit.md",
    "acknowledgements.md",
)
BANNER = """> 单文件版：参考章节已全部内联，文中的文件路径对应下方章节。
> 若当前聊天环境无法运行 Python，请从配套技能包在本机运行分段计算器，再把结果贴入聊天。
> 没有计算结果时不要编造帧范围；本文件不会自动执行裁尾、节点设置或视频生成。"""


def demote_headings(text: str) -> str:
    """Keep fenced examples intact while making reference headings subordinate."""
    result = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)[0]
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
        if fence is None and line.startswith("#"):
            line = "#" + line
        result.append(line)
    return "\n".join(result)


def build_text(root: Path = ROOT) -> str:
    entry = (root / "SKILL.md").read_text(encoding="utf-8")
    entry = re.sub(r"\A---\r?\n.*?\r?\n---\r?\n", "", entry, count=1, flags=re.S).strip()
    parts = [entry, BANNER]
    for name in SECTIONS:
        path = root / "references" / name
        parts.append(f"<!-- references/{name} -->\n" + demote_headings(path.read_text(encoding="utf-8").strip()))
    return "\n\n---\n\n".join(parts) + "\n"


def main() -> None:
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_bytes(build_text().encode("utf-8"))
    print(f"Built {OUTPUT.name} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
