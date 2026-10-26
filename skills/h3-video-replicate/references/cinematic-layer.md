# 摄影层（吸收自小优 cinematic-director，按视频复刻改写）

小优的方法是“摄影团队先开会做视觉决策，再写提示词”。这里只取对复刻有用的部分，并改成**先观察、后决定**。方法来源见文末。

## 0. 三个接入点

| 接入点 | 何时用 | 做什么 |
|---|---|---|
| 读片（模式 A，默认） | 每次复刻 | 用第 2 节的读片会把原片按摄影语言记下来，落到 S10/S11/S08/S16 |
| 电影化重拍（模式 B） | 用户明确要求改风格、光影或镜头语言，同时保留动作与时序 | 第 3–6 节的克制规则改写风格锚点与镜头描述 |
| 参考静帧（模式 C） | 复刻前要做场景图、关键帧、风格锚点图 | 第 7 节的静帧提示词骨架 |

## 1. 优先级：忠实复刻压过小优的默认偏好

小优的方法默认追求“克制的电影感”。复刻时原片说了算：

| 小优默认 | 模式 A（复刻）怎么办 |
|---|---|
| 人物永远不看镜头 | 原片看镜头、对镜头 wink 或比心，就照做 |
| 低对比、克制高光、不要 HDR | 原片是高饱和、霓虹、卡通硬光，就照原片 |
| 不居中、留白、不拍碰撞 | 原片居中、拍了碰撞，就照原片 |
| 摄影师笔记、导演观察那类抽象收尾句 | 视频提示词里不加：它们没有可见内容，只会稀释动作描述 |
| 七维注意力权重（20/25/20…） | 不采用：是经验估计，没有验证依据 |

模式 B 才把这些默认偏好当作可选的改写方向，而且只在用户授权的范围内。

## 2. 读片会（记录原片，不替原片做决定）

每个原片镜头一份，或整片一份。写给用户看的中文记录，**不进最终提示词**：

```text
读片会
导演    这一镜真正在讲什么（情绪/关系，不是物件清单）
刚发生  这一秒之前刚发生了什么、此刻正在进行什么（相位，不写静态姿势）
摄影    景别 · 机位高度与角度 · 焦段感（广角/标准/长焦压缩）· 主体占比（尽量百分比）· 运镜方向与速度
美术    主导色（≤5 种）· 色彩来自光还是来自物件 · 光源（数量/方向/软硬/色温）
注意力  角色此刻看哪里（具体对象；看镜头也要如实记）
视线路径 观众的第一眼 → 第二眼 → 第三眼
情绪    2–3 个词 + 它们的可见载体
不确定  看不清 / 被遮挡 / 需要用户确认的地方
```

对应关系：摄影 → S10；刚发生、注意力 → S11；情绪 → S08；美术 → S16；不确定 → 首次回复里的提问。

## 3. 瞬间写法

- 写“刚发生/正在发生”，不写静态状态：`has just stopped walking` 比 `stands` 多出一个相位。
- 注意力要落在具体对象上：`her eyes follow the blade` 比 `looks away` 强；动机只暗示，不解释。
- 这两条用于首帧（R06）、段首（R29/R67）、段尾（R28）。原片没有的蓄势、停顿、凝视不要加。

## 4. 光与视线锚点

- 光有唯一可信的来源时，先写光源，再写它照到什么；光先落在空间或注意力对象上，不一定先照脸。
- 视线落点、最亮处、观众的第一眼，如果原片里是同一个东西，就让提示词保持一致，不要三者各说各的。
- 色彩来自光和空气，不来自一堆物件各带一种颜色。主导色控制在 3–5 种。
- 深度来自空气和层次，不靠加模糊。

## 5. 模式 B：电影化重拍

前提：用户明确要改风格、光影或镜头语言。**可以变**：风格、光色、色板、空气感、镜头质感，以及用户授权的机位和运镜。**不可变**：事件、顺序、时序、施动者与接触的因果、物件状态。镜头变动要在首次回复里列出并取得同意，且在重叠区保持物理连续。

风格锚点（替换 R01）按“意图 → 层级 → 光色 → 克制”写成 80–120 词的英文，不堆关键词：

```text
{{shot}} is approached as {{observation type}} rather than {{what to avoid}}.
{{protagonist}} occupies roughly {{percent}} of the frame; {{environment}} carries the rest.
The only light is {{source}} from {{direction}}, {{quality}}; it reaches {{attention object}} before {{secondary}}.
The palette stays within {{3–5 hues}}, with colour following light and distance. Depth comes from air and layering, not blur.
Avoid {{x}}. Leave {{y}}. Highlights stay restrained.
```

- 数字要具体：占比、距离、焦段、高度都写成数。
- 不写没有内容的质量标签：`8K, 4K, masterpiece, best quality, ultra detailed, hyper detailed, HDR, epic, stunning, breathtaking, award winning, trending on artstation, sharp focus, insane detail, high resolution`。这些词把模型推向宣传图，所有模式都不要用。
- 提示词写成完整的句子，每句一个决定；不写成逗号分隔的关键词流。

## 6. 排除句与硬约束镜像

六字段里没有负向字段（以你工作流里实际有没有负向输入为准，有就放那里）。做法：

1. **先写正向锁定**：`Exactly one character is in frame`、`the camera holds the source framing`。
2. **硬设定镜像**：用户每说一条“不出现/不可见/没有”，就在 `detailed_description` 末尾补一句对应的排除句。
3. **通用防崩句**（原片没有这些元素时）：`No on-screen text, subtitles, watermark or logo. No duplicated characters, extra limbs or extra fingers. No morphing between shots.` 原片本来就有字幕或文字，就不加。
4. **正向决策配一个负向保险**：

| 正向决策 | 镜像排除 |
|---|---|
| 主体占画面约 5% | no close-up, no oversized figure filling the frame |
| 只有一个光源 | no additional light sources, no fake rim light |
| 看不到天空 | no visible sky, no visible moon disc |
| 只有一个光标 | no second pointer |
| 单一尾巴 | no second tail beside it |

排除句要短。长串否定词容易把被否定的东西带进画面，能用正向锁定表达的就不用排除。

## 7. 模式 C：参考静帧提示词

用于场景图、环境关键帧、风格锚点图、构图参考。**不用于身份参考板**（三视图、多视图、定妆照）：那类图需要中性背景、均匀布光和精确形制，走技术一致性写法，不加氛围。

英文散文，按顺序组装：

1. **意图**：`This image is approached as … rather than …`
2. **层级**：谁是主角，占比多少（具体百分比）
3. **注意力**：人物（若有）看向什么
4. **摄影**：焦段、距离、机位高度和角度、光源
5. **视线路径**：第一眼是什么
6. **场景五要素**，每个一句：Location / Time / Weather / Moment / Human Scale（写“世界正在发生什么”，不写“有什么”）
7. **克制句**：`Avoid … Leave … Trust …`，3 句以内

模型支持独立负向提示词就按四类写：AI 味（CGI、塑料皮肤、游戏渲染）、非电影（居中英雄构图）、光影（过曝、假体积光）、色彩（过饱和、霓虹）；有人物时加解剖类，收尾加 `text, watermark, logo`。不支持负向的模型，压成 2–4 句自然语言接在正向末尾。

## 8. 迭代

某一块不好，只重写那一块再重新组装，不要推翻全部：

- 构图或镜头问题 → S10 与镜头描述
- 画面像 CG → 第 5 节的克制规则与质量标签
- 角色不吸引人或脸漂 → 身份锚点（S01）与该段 Picture 分配
- 视线不对 → S11 的视线落点

## 来源与说明

- 方法来自 <https://github.com/cOkieeman/xiaoyou-aigc-cinematic-director>（fork 自 wubo0927/xiaoyou-aigc-cinematic-director，抖音“小优AIGC”）。
- 本文件是改写，不是搬运。写作时看到的仓库页面上没有 LICENSE 文件；若要把更多原文并入并公开发布，建议先征得原作者同意。
- 没有吸收的部分：编剧和分镜两个 Skill（不公开）；固定的人物原型库和题材模板（面向生图，不适用于复刻）；七维权重百分比；摄影师笔记与导演观察的固定句式（见第 1 节）。
