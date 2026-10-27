# Soda H3 视频复刻

把参考视频里的动作、镜头和节奏整理成 MiniMax H3 的分段提示词。提供参考视频和角色、服装或场景图后，插件会分析素材、计算时间框，并逐段给出六字段英文提示词与导演台设置。

适用于 ComfyUI Timeline Director 的时间框模式。插件负责规划和写提示词；生成仍由你在 ComfyUI 中执行。

## 可以做什么

- **换人、换装、换场景**：保留原片可观察的动作和时序，替换指定外观。
- **电影化重拍**：在明确授权的范围内调整光影、画风和镜头语言。
- **参考静帧**：为场景或关键瞬间写生图提示词。
- **分段与设置**：按整数帧计算段长、重叠和尾裁，说明每段如何放图、设声音。

每段提示词使用固定六字段：`subject_definitions`、`summary`、`retention_analysis`、`detailed_description`、`overall_soundscape`、`non_diegetic_music`。解释默认用中文，提示词默认用英文。

## 使用前准备

- 可读取本地文件并运行命令的桌面环境。
- Python 3.9 或更高版本；分段、测试与打包脚本只依赖标准库。
- FFmpeg 与 ffprobe，用于读取视频信息、抽帧和必要的尾裁。放进 PATH，或在执行时提供实际路径。
- 已配置 MiniMax H3 与 Timeline Director 节点的 ComfyUI。节点版本和模型由使用者自行安装，插件不附带模型或工作流。

节点的合法帧数与可用选项可能随版本变化。执行前应核对当前节点，不能用提示词代替实际的声音开关、图片分配或裁剪。

## 在 Codex 中安装

从 GitHub 添加插件来源：

```powershell
codex plugin marketplace add https://github.com/cOkieeman/soda-h3-video-replicate.git
```

需要本地副本时，也可以克隆后从仓库目录注册：

```powershell
git clone https://github.com/cOkieeman/soda-h3-video-replicate.git
cd soda-h3-video-replicate
codex plugin marketplace add .
```

刷新或重启桌面客户端，在插件目录里选择 **Soda H3 视频复刻** 来源，安装同名插件。若环境不支持该命令，可在客户端添加本地 marketplace；入口文件是 `.agents/plugins/marketplace.json`。

更新本地仓库后可运行：

```powershell
codex plugin marketplace upgrade soda-h3-video-replicate
```

随后在客户端刷新插件，并在新聊天中确认新版本。仓库改名和插件改名不会自动替换旧安装；使用旧名称的用户需要安装新插件，再移除不再使用的旧版本。

## 开始使用

可以先打开菜单：

```text
用 $soda-h3-video-replicate，先列出可选方向，再告诉我要准备哪些素材。
```

也可以直接交代任务：

```text
参考视频是 D:\素材\dance.mp4，角色图是 D:\素材\character.png。
保留视频里的动作、镜头和节奏，把人物换成参考图角色，保留原声。
请先分析素材，再给出分段提示词和导演台设置。
```

插件会先说明观察到的镜头与事件。影响结果的不确定项会单独提出；素材完整时继续输出逐段提示词，最后汇总时间框、放图顺序、声音与尾裁设置。无法读取的视频需要先转换或提供可查看的素材，不能只凭文件名编写时间轴。

## Claude Code 与单文件使用

仓库保留 `.claude-plugin/plugin.json` 和 `.claude-plugin/marketplace.json` 兼容入口。可在 Claude Code 的插件管理中添加本仓库目录，安装 `soda-h3-video-replicate`。这只提供相同的技能内容，素材读取和命令执行仍取决于宿主环境。

没有插件安装能力时，可把 `skills/soda-h3-video-replicate/dist/soda-h3-video-replicate.single.md` 中的完整内容交给聊天模型。单文件版不能替你在本机运行 Python 或读取视频；应先在本机生成分段表，并提供实际抽帧或其他可查看素材。

## 分段计算器

```powershell
python skills\soda-h3-video-replicate\scripts\plan_segments.py --seconds 10 --events 2.9,5.7
python skills\soda-h3-video-replicate\scripts\plan_segments.py --frames 240 --json
python skills\soda-h3-video-replicate\scripts\plan_segments.py --seconds 10 --length 90 --overlap 5
```

默认时基为 24 fps，每段 107 帧、重叠 39 帧，步长 68 帧。段长遵循 `5 + 17n`；其他限制以当前节点和计算器校验为准。若原片末尾需要补齐合法段长，必须在合并后实际裁掉补帧及对应声音。

## 验证与打包

在仓库根目录执行：

```powershell
python -I -m unittest discover -s tests
python -I skills\soda-h3-video-replicate\scripts\build_single.py
python scripts\package_release.py
```

测试用于检查计算、清单、文件引用和打包一致性。它们不能证明生成视频的视觉质量。本版本尚未完成重命名后插件的跨客户端安装测试，也未用默认 107/39 配置完成真实视频的端到端生成与视觉验收。FFmpeg 抽帧属于抽样观察，提示词也不能保证逐帧一致。

## 文件与许可

`skills/soda-h3-video-replicate/` 是技能本体，包含重组后的规则、模板与按事件选用的条件句库。根目录清单和 marketplace 用于插件分发，`assets/` 为原创插件图标，`tests/` 为验证代码。

本项目已获得原教程作者的公开发布授权，发行内容保留获授权的条件句库。Soda 工程代码与自编内容适用 [Apache License 2.0](LICENSE)，教程内容保留原作者权利；具体授权范围见 [NOTICE](NOTICE)。

第三方方法与项目参考统一列在[致谢](skills/soda-h3-video-replicate/references/acknowledgements.md)。
