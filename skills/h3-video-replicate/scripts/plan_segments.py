#!/usr/bin/env python3
"""MiniMax H3 Timeline Director 分段计算器。

按整数帧和精确分数计算，避免模型心算 ceil / 取整出错。
规则来源：本机 ComfyUI-MiniMaxH3-TimelineDirector 0.8.0（长度 5+17*n，接缝 0/1/5/22/39/56…，最多 64 段）。

用法：
  python plan_segments.py --seconds 10
  python plan_segments.py --frames 240 --events 3.2,7.5,9.9
  python plan_segments.py --seconds 10 --length 90 --overlap 5      # 旧配置
  python plan_segments.py --seconds 10 --json

--events 给的是原片时间（秒），会映射到每个包含它的分段的局部时间；落在重叠区的事件
会标出，那是同一次事件，两段都要写，不是两次动作。
"""
import argparse
import json
import sys
from fractions import Fraction
from math import ceil

DEFAULT_FPS = 24
DEFAULT_LENGTH = 107  # 4.4583 s，用户单段上限 4.5 s 内最大的合法长度
DEFAULT_OVERLAP = 39  # 1.625 s
MAX_SEGMENTS = 64


def legal_length(n: int) -> bool:
    return n >= 5 and (n - 5) % 17 == 0


def legal_overlap(n: int) -> bool:
    return n in (0, 1) or legal_length(n)


def round_half_up(x: Fraction) -> int:
    return int((x * 2 + 1) // 2)


def timecode(frames: int, fps: int) -> str:
    """整数帧 -> MM:SS.mmm（毫秒四舍五入，底层仍是整数帧）。"""
    ms = round_half_up(Fraction(frames * 1000, fps))
    m, rem = divmod(ms, 60000)
    s, ms = divmod(rem, 1000)
    return f"{m:02d}:{s:02d}.{ms:03d}"


def plan(total_frames: int, length: int, overlap: int, fps: int):
    step = length - overlap
    if total_frames <= length:
        n = 1
    else:
        n = 1 + ceil((total_frames - length) / step)
    if n > MAX_SEGMENTS:
        reach = length + (MAX_SEGMENTS - 1) * step
        raise ValueError(
            f"需要 {n} 段，超过时间框上限 {MAX_SEGMENTS} 段（该配置最多覆盖 {reach} 帧 ≈ {reach / fps:.3f} 秒）。"
            "请先制定分批续接/合并方案，不要截断视频。"
        )
    segs = []
    for i in range(1, n + 1):
        start = (i - 1) * step
        if i < n:
            ln = length
        else:
            tail = total_frames - start
            ln = 5 + 17 * max(0, ceil((tail - 5) / 17))
        segs.append(
            {
                "gen": i,
                "start": start,
                "end": start + ln,
                "length": ln,
                "overlap_in": 0 if i == 1 else overlap,
                "new_frames": ln if i == 1 else ln - overlap,
            }
        )
    end = segs[-1]["end"]
    return segs, end, end - total_frames


def check(segs, total_frames, end, pad, length, overlap):
    assert segs[0]["start"] == 0
    for a, b in zip(segs, segs[1:]):
        assert b["start"] < a["end"], "相邻窗口出现空白"
        assert a["end"] - b["start"] == overlap, "重叠与设定不符"
        assert b["start"] > a["start"], "窗口未向前推进"
    for s in segs:
        assert legal_length(s["length"]) and s["length"] <= length, f"GEN{s['gen']} 长度不合法"
    assert sum(s["new_frames"] for s in segs) == end, "新增帧数之和 != 输出末帧"
    assert end >= total_frames and 0 <= pad <= 16, "补尾帧数异常"
    if len(segs) > 1:
        assert segs[-1]["length"] > overlap, "末段长度必须大于重叠"


def map_event(t_sec: Fraction, segs, fps: int, total_frames: int, overlap: int):
    g = round_half_up(t_sec * fps)  # 量化到最近的输出帧
    hits = []
    for idx, s in enumerate(segs):
        if s["start"] <= g < s["end"]:
            local = g - s["start"]
            in_head_overlap = idx > 0 and local < overlap
            in_tail_overlap = idx < len(segs) - 1 and g >= segs[idx + 1]["start"]
            hits.append(
                {
                    "gen": s["gen"],
                    "local_frame": local,
                    "local_time": timecode(local, fps),
                    "head_overlap": in_head_overlap,
                    "tail_overlap": in_tail_overlap,
                }
            )
    return {
        "source_time": float(t_sec),
        "global_frame": g,
        "beyond_target": g >= total_frames,
        "segments": hits,
    }


def main():
    # 管道/重定向时 Windows 默认按 GBK 编码，强制 UTF-8；交互终端由 Python 自行处理。
    for stream in (sys.stdout, sys.stderr):
        if not stream.isatty():
            stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--seconds", type=str, help="原片有效时长（秒，可写小数，按精确分数计算）")
    src.add_argument("--frames", type=int, help="目标保留帧数 F")
    ap.add_argument("--fps", type=int, default=DEFAULT_FPS)
    ap.add_argument("--length", type=int, default=DEFAULT_LENGTH, help="常规段长 L，须为 5+17n")
    ap.add_argument("--overlap", type=int, default=DEFAULT_OVERLAP, help="常规重叠 O，须为 0/1/5+17n")
    ap.add_argument("--events", type=str, default="", help="原片事件时间（秒），逗号分隔")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if not legal_length(a.length):
        sys.exit(f"错误：常规段长 {a.length} 不是 5+17n（可用 5,22,39,56,73,90,107,…）")
    if not legal_overlap(a.overlap):
        sys.exit(f"错误：重叠 {a.overlap} 不是合法接缝（0,1,5,22,39,56,…）")
    if a.overlap >= a.length:
        sys.exit("错误：重叠必须小于段长")

    if a.frames is not None:
        total = a.frames
        seconds = Fraction(total, a.fps)
    else:
        seconds = Fraction(a.seconds)
        total = ceil(seconds * a.fps)
    if total < 1:
        sys.exit("错误：帧数必须 >= 1")

    try:
        segs, end, pad = plan(total, a.length, a.overlap, a.fps)
    except ValueError as e:
        sys.exit(f"错误：{e}")
    check(segs, total, end, pad, a.length, a.overlap)

    events = []
    if a.events.strip():
        for tok in a.events.split(","):
            events.append(map_event(Fraction(tok.strip()), segs, a.fps, total, a.overlap))

    result = {
        "fps": a.fps,
        "L": a.length,
        "O": a.overlap,
        "D": a.length - a.overlap,
        "target_seconds": float(seconds),
        "F": total,
        "N": len(segs),
        "E": end,
        "P": pad,
        "segments": segs,
        "events": events,
    }
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"时基 {a.fps}fps | 常规 L={a.length} 帧 ({a.length / a.fps:.6f}s)  O={a.overlap} 帧 ({a.overlap / a.fps:.6f}s)  D={a.length - a.overlap} 帧")
    print(f"目标保留 F={total} 帧 ({float(seconds):.6f}s) → 分 N={len(segs)} 段，输出末帧 E={end}，尾部待裁 P={pad} 帧")
    print()
    print("| GEN | 全局帧 [start,end) | 全局时间 | 长度(帧/秒) | 开头重叠 | 新增帧 |")
    print("|---|---|---|---|---|---|")
    for s in segs:
        print(
            f"| {s['gen']} | [{s['start']},{s['end']}) | {timecode(s['start'], a.fps)}–{timecode(s['end'], a.fps)} "
            f"| {s['length']} / {s['length'] / a.fps:.6f} | {s['overlap_in']} | {s['new_frames']} |"
        )
    print()
    if pad:
        print(f"裁剪：合并后保留前 {total} 帧，裁掉末尾 {pad} 帧及对应音频。提示词不能执行裁剪，必须另有实际裁剪步骤，未执行则标“待裁”。")
    else:
        print("裁剪：无需裁剪（E == F）。")
    if events:
        print()
        print("事件映射（量化到最近输出帧；落在重叠区的事件是同一次发生，相邻两段都要写，不得写成两次）：")
        for ev in events:
            flag = "  ⚠ 超出目标保留范围（落在补尾区）" if ev["beyond_target"] else ""
            print(f"- 原片 {ev['source_time']}s → 全局帧 {ev['global_frame']}{flag}")
            for h in ev["segments"]:
                tag = []
                if h["head_overlap"]:
                    tag.append("本段开头重叠区")
                if h["tail_overlap"]:
                    tag.append("本段结尾重叠区(下一段重复描述)")
                extra = f"（{'；'.join(tag)}）" if tag else ""
                print(f"    GEN{h['gen']}: 局部第 {h['local_frame']} 帧 = {h['local_time']}{extra}")


if __name__ == "__main__":
    main()
