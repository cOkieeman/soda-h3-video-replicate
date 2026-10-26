# H3 视频复刻（Codex 插件）

给参考视频和参考图，输出 MiniMax H3（ComfyUI Timeline Director 时间框模式）逐段复刻用的放图说明和六字段英文提示词。只出提示词，不读写工作流文件，不运行 ComfyUI。

## 目录

```text
plugin.json                      插件清单（Agent Plugins 格式）
.codex-plugin/plugin.json        Codex 兼容清单
.claude-plugin/                  Claude 兼容清单与 marketplace
.agents/plugins/marketplace.json 本地 marketplace（source 指向本目录）
skills/h3-video-replicate/       skill 本体
  SKILL.md                       入口
  agents/openai.yaml             Codex 界面信息
  references/                    各步骤的规则、模板、句库
  scripts/plan_segments.py       分段计算器
  scripts/build_single.py        生成单文件版
  dist/                          单文件版（贴进聊天模型用）
tests/                           单元测试
LICENSE / NOTICE                 许可证与授权范围
```

## 注册（手动，尚未执行）

```powershell
codex plugin marketplace add E:\个人开发项目\minimaxH3\h3-video-replicate-plugin
```

注册后重启 Codex，在插件列表里启用 `h3-video-replicate`。

## 用法

在 Codex 里附上参考视频和参考图，说：

```text
用 $h3-video-replicate 看这个参考视频和参考图，先告诉我分段方案，再逐段给出提示词。
```

它会先说明读到了什么、保留和替换什么、分几段，缺信息就问你；然后逐段给出“时长 / 全局范围 / 放图 / 视频与音频设置”和一个只装六字段提示词的代码块。拿到后在素材规划台里把各段范围改成分段表上的值，把图拖进对应段，再逐段粘贴提示词。

## 分段计算器

```powershell
python skills\h3-video-replicate\scripts\plan_segments.py --seconds 10 --events 2.9,5.7
python skills\h3-video-replicate\scripts\plan_segments.py --frames 240 --json
python skills\h3-video-replicate\scripts\plan_segments.py --seconds 10 --length 90 --overlap 5
```

默认每段 107 帧、重叠 39 帧（24fps）。只用 Python 标准库。

## 测试与单文件版

```powershell
python -I -m unittest discover -s tests
python -I skills\h3-video-replicate\scripts\build_single.py
```

## 已知限制

- 还没有在真实 Codex 会话里用真实视频端到端试过。
- 默认的 107/39 还没在本机生成过；本机实测过的是 90 帧/重叠 5 帧。“更新分段”不保证得到 107/39，要按分段表手动改各段范围。
- 读视频靠 ffmpeg 抽帧，是抽样观察，不是逐帧。
- 读片命令里的 ffmpeg 路径是本机路径（`C:\Users\Administrator\.codex\tools\bin\`），换机器要改 `references/01-intake.md`。

## 来源与许可

skill 合并自《视频复刻工作书-通用版Skill》与 <https://github.com/cOkieeman/xiaoyou-aigc-cinematic-director>。

- 本人编写的部分（脚本、测试、插件清单、README、摄影层）按 Apache License 2.0 授权，见 `LICENSE`。
- R 句库和源自原版说明书的规则来自 MiniMax H3 教程作者，**不在 Apache-2.0 范围内**，权利归原作者；取得授权前仅供私人使用、不得再分发。逐项范围见 `NOTICE`。
- 因此本仓库保持私有。要公开，需先取得教程作者同意，或把逐字搬来的句库重写。
