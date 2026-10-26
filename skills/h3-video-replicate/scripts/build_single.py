#!/usr/bin/env python3
"""把 SKILL.md + references 合并成单文件，输出到 dist/h3-video-replicate.single.md。

用途：不装 Agent 时，把这一个文件贴进聊天模型当系统提示词。单文件版不能运行脚本，
所以分段数字需要先在本机跑 plan_segments.py，再把结果贴给模型。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "h3-video-replicate.single.md"

ORDER = [
    "references/01-intake.md",
    "references/02-slots.md",
    "references/03-timeline.md",
    "references/04-grammar.md",
    "references/05-assembly-output.md",
    "references/06-checklist.md",
    "references/07-comfyui-wiring.md",
    "references/cinematic-layer.md",
    "references/phrases/core.md",
    "references/phrases/cursor-edit.md",
]

BANNER = """> **单文件版**：各章已全部内联在下面，文中“读取某文件 / 某节”即查阅对应章节。
> 这个环境不能运行脚本：开始前请先在本机运行 `python scripts/plan_segments.py --seconds <时长> --events <事件秒数>`，
> 把输出的分段表贴进对话，分段数字以该表为准，不要心算。
"""


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8").replace("\r\n", "\n").strip()


def strip_frontmatter(text: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S).strip()


def demote(text: str) -> str:
    """章节里的标题整体下降一级，避免多个 H1 并列。"""
    out, fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
        if not fence and line.startswith("#"):
            line = "#" + line
        out.append(line)
    return "\n".join(out)


def main():
    parts = [strip_frontmatter(read("SKILL.md")), BANNER]
    for rel in ORDER:
        parts.append(f"<!-- {rel} -->\n" + demote(read(rel)))
    # 单文件里没有 scripts/ 与 references/ 目录，去掉文件清单一节
    text = "\n\n---\n\n".join(parts)
    text = re.sub(r"\n## 文件\n.*?(?=\n\n---\n\n)", "", text, count=1, flags=re.S)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(text + "\n", encoding="utf-8")
    if not sys.stdout.isatty():
        sys.stdout.reconfigure(encoding="utf-8")
    print(f"{OUT}  {len(text.encode('utf-8')) / 1024:.1f} KB  {text.count(chr(10)) + 1} lines")


if __name__ == "__main__":
    sys.exit(main())
