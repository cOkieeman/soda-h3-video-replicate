# Soda H3 视频复刻

根据实际素材，把原片的镜头、动作和事件整理成可以逐段使用的生成说明。默认中文解释、英文提示词。工作止于观察、规划和提示词交付；生成质量需要实际运行与画面检查验证。

## 任务范围

- **忠实复刻**：保留原片可观察的时序、动作和镜头，只改变用户指定的人物、服装或环境。
- **电影化重拍**：用户明确希望改变影像风格时，调整获准的光色、构图或运镜，保留约定的事件顺序。
- **参考静帧**：为已有复刻计划准备场景或关键时刻的图片提示词。
- **只算分段 / 设置导演台**：只完成用户要求的计算或参数核对，不扩展成整套创作。

已有方向和素材就直接开始。用户只说“开始”时，可简要列出换人、换装、换场景、电影化重拍、参考静帧、只算分段和导演台设置七个方向。需要补充资料时，一次只问会影响结果的内容。

## 工作顺序与参考文档

| 环节 | 做法 | 参考 |
|---|---|---|
| 确认素材 | 明确视频、图片和修改要求分别约束什么；检查能否实际读取 | `references/intake.md` |
| 观察原片 | 读元数据并覆盖全片观察，记录镜头、事件、物件状态和不确定处 | `references/intake.md` |
| 规划窗口 | 运行 `scripts/plan_segments.py`，使用实际输出的帧范围和事件映射 | `references/timeline.md` |
| 编写提示词 | 将当前段的观察、替换范围、动作因果和媒体编号写成完整六字段 | `references/prompt-writing.md` |
| 选用动作句 | 只读取当前事件需要的通用模块或光标、服装与物件变化模块 | `references/phrases/core.md`、`references/phrases/cursor-edit.md` |
| 可选影像改写 | 只在电影化重拍或参考静帧任务中应用获准的摄影决策 | `references/cinematography.md` |
| 交付 | 分段代码块与导演台设置表分别给出，标明声音和尾裁的执行状态 | `references/delivery.md` |
| 对接节点 | 按实际时间框、素材分配和节点版本核对设置 | `references/director.md` |
| 检查与修订 | 检查事实、数字、跨段状态和交付完整性；只改受影响部分 | `references/quality-check.md` |

先向用户简要说明观察结果、替换范围和分段方案，再给提示词。资料完整时可在同一回复完成，无须额外等待确认。无法观看或解码视频时说明具体限制，不把文件名、旧案例或猜测写成已观察事实。

## 当前适配参数

| 项目 | 值 |
|---|---|
| 对接方式 | MiniMax H3 Timeline Director 0.8.0 时间框模式 |
| 生成时基 | 24 fps；源视频帧率用于观察，不替代生成时基 |
| 段长 | `5 + 17n`，每段最多 3592 帧 |
| 常规窗口 | 107 帧；相邻窗口重叠 39 帧；步长 68 帧 |
| 可用重叠 | 0、1、5、22、39、56…，小于段长 |
| 段数上限 | 64 |

这些数值用于当前适配，不代表所有节点版本。用户要求其他参数时，先核对脚本与当前节点是否支持；不直接套用旧工作流的默认段数。

## 必须保持的约束

1. 原片决定可观察事件与时间，参考图只约束它实际承担的身份、外观或场景。用户的明确修改要求决定替换范围。
2. 窗口重叠描述同一次过程。相邻段不能把重叠中的事件再发生一次，交接处的人物、物件和运动状态要一致。
3. 每段使用当前实际分配的 `<Picture 1>`、`<Video 1>` 等编号。编号在段内解释，不把内部 Latent 当成额外视频。
4. 每段独立包含 `subject_definitions`、`summary`、`retention_analysis`、`detailed_description`、`overall_soundscape`、`non_diegetic_music` 六个字段。
5. 提示词不能代替节点设置、裁尾或音轨处理。未实际执行的操作标为待执行，不宣称已经完成。
6. 不继承其他案例中的光标、换装、鞋袜、特效、表情或结尾动作；只描述当前素材和本期授权的内容。
7. 不主动启动 ComfyUI、提交 GPU 生成或改写工作流文件。需要这些工作时，按用户新的明确要求处理。

第三方作者称呼和方法出处集中在文末“致谢”（`references/acknowledgements.md`）。操作说明与生成提示词不附带作者账号、宣传标识或署名。

---

> 单文件版：参考章节已全部内联，文中的文件路径对应下方章节。
> 若当前聊天环境无法运行 Python，请从配套技能包在本机运行分段计算器，再把结果贴入聊天。
> 没有计算结果时不要编造帧范围；本文件不会自动执行裁尾、节点设置或视频生成。

---

<!-- references/intake.md -->
## 识别任务与读取素材

本页处理开始写分段之前的工作：弄清每份素材的作用，真实观察视频，留下可供后续核对的记录。帧数计算见 [timeline.md](timeline.md)，具体字段写法见 [prompt-writing.md](prompt-writing.md)。

### 直接识别用户要改什么

用户已经说清“用这张图换掉视频里的人”“衣服改成图中的款式”等要求时，直接进入对应任务，不再展示菜单。把要求整理为两句话：哪些内容需要替换，哪些内容需要保留。没有任务方向时才给出简短选择：换人、换装、换场景、电影化重拍、参考静帧、只算分段、导演台设置。可以组合选择，但不要让菜单代替对现有素材的理解。

逐份确认素材用途。视频通常提供动作、镜头、节奏和声音；人物图通常提供身份与外观；服装图提供衣物结构；场景图提供环境。参考图中的姿势不自动成为视频动作，背景也不自动替换原片。角色图同时含有服装和背景时，按用户的替换范围使用。用户只要求换人而没有指定服装处理方式，先检查上下文是否已有答案；只有该选择会实质改变结果时才补问。

一份素材兼有多种用途时分别写清。只要求长视频中的一段时，确认起止范围。

### 先核实文件，再观察内容

读取时长、宽高、显示方向、视频流帧率信息和音轨情况。这里的源帧率用于理解素材，生成仍按 24 fps 规划。旋转元数据可能使文件宽高与实际观看方向不同；先按正常显示方向看过，再决定横竖画面。可变帧率素材以展示时间戳定位，不用“源第几帧除以平均帧率”代替时间。

以下示例使用 PATH 中的工具；也可将命令名换成用户配置的可执行文件变量。路径变量在运行前设为实际素材，禁止把示例文件名当成已找到的文件。

```powershell
$SourceVideo = 'reference.mp4'
ffprobe -v error -show_entries format=duration:stream=index,codec_type,width,height,r_frame_rate,avg_frame_rate,duration:stream_tags=rotate -of json $SourceVideo
$ReviewDir = Join-Path ([IO.Path]::GetTempPath()) ('h3-review-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $ReviewDir | Out-Null
ffmpeg -hide_banner -i $SourceVideo -vf 'fps=1/2' -q:v 3 (Join-Path $ReviewDir 'overview-%05d.jpg')
```

每两秒一张只是建立全片概览的起点，短片或动作密集片段应缩短间隔。抽帧必须覆盖实际开头、内部和结尾；等间隔导出可能漏掉最后一瞬，另取尾部画面补齐。帧图序号并不证明精确源时间。需要对齐动作时，在目标时间前后连续检查，并记录对应展示时间戳。

有可用视频查看工具时实际播放或分段查看；只有图片工具时，查看覆盖全片的抽帧及加密帧。不能只读取元数据、文件名或一张封面就声称已经看过动作。若只能看到部分素材，明确哪些范围有证据、哪些尚未观察，不把未见部分写成确定事实。

### 建立一份全局记录

先做全片观察记录，再切分窗口。记录应包括：源时间、镜头景别和运动、主体位置、动作起点与结果、物件状态、接触关系、可见文字，以及声音事件。描述观察到的变化，例如“手从桌面移向杯柄，握住后抬离桌面”，比只记“拿杯子”更利于判断接缝。

特别加密检查转身、遮挡、伸手接触、物件交接、服装状态变化、镜头切换和声音起落。先后关系必须来自视频。两张间隔帧之间无法证明的细节记为不确定；可以继续观察，也可以用较宽的真实动作描述，不能补造一个看似合理的中间事件。首尾动作只写实际可见范围，画外事件不补写发生过程。

规划后回到接缝附近加密观察。窗口或重叠改变时，更新事件对应关系，不改写原片事实。

### 何时需要询问

优先自行解决可读取的时长、比例、音轨、主体数量和明显动作。需要询问的是会改变交付内容的缺项，例如多人片中替换谁、是否保留原对白、是否允许重构场景布局，或用户只给人物图却要求复刻未提供的视频。一次提出最少的关键问题，并继续整理不依赖答案的观察记录。

只要分段或设置表时，不顺带写整套提示词。完整复刻说明的交付顺序见 [delivery.md](delivery.md)。

---

<!-- references/timeline.md -->
## 按帧规划分段与接缝

本页只负责生成时间轴。所有窗口、段数、末尾补齐和事件归属以 `scripts/plan_segments.py` 的实际输出为准。不要凭视频秒数心算一张正式分段表，再把脚本当作事后装饰。

### 统一计时单位

适配 MiniMax H3 Timeline Director 0.8.0 时间框模式，生成 24 fps；当前安装是否通过验证需另有证据。源 fps 不改变生成 fps，源动作仍按实际展示时间定位。

使用下列符号记录脚本结果：`F` 为目标保留帧数，`L` 为常规段长，`O` 为重叠帧数，`D` 为相邻常规窗口的起点间隔，`N` 为段数，`E` 为最终输出的排他末帧，`P` 为待裁尾帧数。正式交付直接使用输出中的数值，不用另一套公式覆盖脚本对尾段和边界的处理。

段长遵循 `5 + 17n`，其中 n 为非负整数，最大段长为 3592 帧。重叠可取 0、1、5、22、39、56……，且必须小于所属段长。默认使用 `L=107`、`O=39`、`D=68`，最多 64 段。不要把某个保存模板中的段数、采样步数或尾段长度升级为通用规则。

### 调用 planner

以下命令在技能目录运行；解释器名称可按实际环境调整。秒数来自已核实的视频范围，事件时间来自全局观察记录。只有用户明确给定帧数或任务确实以帧数为准时，才直接使用 `--frames`。

```text
python scripts/plan_segments.py --seconds 10 --events 2.9,5.7
python scripts/plan_segments.py --frames 240 --json
python scripts/plan_segments.py --seconds 10 --length 90 --overlap 5
```

需要保存结构化结果时加 `--json`。实际调用后检查错误和输出；参数被拒绝时应修正参数或报告适配问题，不绕过校验继续编表。时长与帧数出现差异时，先查清源展示时长、截取范围及量化方式，交付中同时保留原时长和最终 `F`。

已运行的 10 秒样例为：`F=240, L=107, O=39, D=68, N=3, E=243, P=3`，窗口为 `[0,107)`、`[68,175)`、`[136,243)`。包含起帧、不包含末帧，最后窗口不含第 243 帧。样例用于解释结果，不能替代本次调用。

### 把真实事件映射到窗口

全局事件先记录在源时间上，再让 planner 量化到生成帧并标出所属窗口。正式说明保留全局时间和局部时间，避免把某段的第 1 秒误说成整片第 1 秒。局部帧由全局帧相对该窗口起点确定；如果窗口规划改变，事件局部位置必须随之更新。

上述样例中，2.9 秒被映射为全局帧 70，出现在第一段局部帧 70 和第二段局部帧 2，分别属于尾部重叠和头部重叠。5.7 秒被映射为全局帧 137，出现在第二段局部帧 69 和第三段局部帧 1。这里是同一个源事件在两个观察窗口中出现，不是事件需要表演两次。

对每个接缝写一条连续性记录：重叠开始时身体与物件的状态、重叠中正在继续的动作、重叠结束时应到达的状态，以及后段从何处开始新增内容。后段头部可以继续叙述已经开始的动作，但不能让手重新伸出、杯子重新被拿起、人物重新转身。新的事件应落在重叠结束之后；如果原片事件本来就在重叠区，就按同一次事件保持两段一致。

动作跨窗口时保持原事件时间。只有用户允许改变节奏，才能讨论重定时。

### 尾部与超长任务

短尾段和长尾段都要满足合法长度。选择何种尾段策略，应服从请求的固定长度、当前脚本支持的选项和实际结果。不能手工截出一个非法尾段，也不能让生成文案承担视频裁切工作。

如果 `E` 超过 `F`，超出部分只是技术补齐。可延续最后可见状态或结束运动的自然惯性，但不能新加挥手、换姿势、说话、物件出现等尾部事件。交付明确列出 `P`，并提供保留原 `F` 帧和原音轨时长的实际裁尾办法，见 [delivery.md](delivery.md)。写一句“视频到此结束”不会把文件裁短。

超过 64 段时，停止扩大单次表格。向用户说明需要拆为多个规划批次，并在批次边界保留动作状态与时间对应。没有获得新的生成操作授权时，规划可以完成，实际执行保持待进行。

---

<!-- references/prompt-writing.md -->
## 撰写每段的六字段提示词

默认用自然中文解释素材用途与设置，生成提示词使用英文。每段都是可独立粘贴的一整份提示词。不要用“同前”“延续上一段设置”替代主体、动作、声音或约束，也不要指望全局提示词补全局部字段。

### 六个字段各管什么

| 固定字段 | 应写内容 |
| --- | --- |
| `subject_definitions` | 本段主体、身份和外观来源，参考素材分工，人物与物件的稳定特征。 |
| `summary` | 本段发生的主要动作、画面关系和镜头目标，概括实际窗口。 |
| `retention_analysis` | 保留哪些原片事实、替换哪些内容，以及接缝、文字和声音的处理范围。 |
| `detailed_description` | 按局部时间推进的动作、接触、轨迹、物件状态、视线、情绪和镜头变化。 |
| `overall_soundscape` | 本段实际环境声、动作声、对白及其保留或静音要求。 |
| `non_diegetic_music` | 画外配乐的来源、保留范围、进入退出；没有配乐时明确不新增。 |

字段名保持原样，不能用中文标题或另造近义字段替换。可以按导演台支持的输入形式交付，但字段内容必须一一对应。若用户只需要这些文字，不额外创建工作流文件。

### 先分清每份参考的权限

本段实际分配的媒体决定 `Picture 1`、`Video 1` 等编号。共享素材库里有一张图，不代表本段已经分配该图；上一段的第二张图在本段也可能变成第一张。先为每段列出实际媒体槽位，再写编号。没有分配的视频不能写成 `Video 1`，继续生成使用的 Latent 也不能被命名为额外图片或视频。

引用时说清用途，例如人物图只约束身份，视频约束身体运动和摄影。用角色图换人时，不把图中站姿、视线或手势移植到视频里；用服装图换装时，不把静态服装参考写成源视频发生过换装。多个人物或相似服装并存时，用稳定可识别的称呼指代，避免在相邻句子里换名称造成主体漂移。

使用 `<Subject 1>` 等标签时，在本段 `subject_definitions` 中定义其含义，再在动作描述中一致引用；不存在的主体不创建。`[Shot 1]` 等镜头标签只在真实切镜时递增，生成分段边界本身不构成切镜。

Ref2VA 的视觉保留标记可使用 `fully_preserved`、`partially_preserved`、`attribute_transfer`、`weak_reference`，音频标记可使用 `fully_copy`、`partially_copy`、`reference`、`weak_reference`。在 `retention_analysis` 中按实际取用的属性解释选择；换人不意味着把原片动作也降为弱参考。视频承担编辑源、动作结构参考或连续生成依据时，各自说明关系，不虚构额外媒体编号。

### 用动作因果写清楚画面

动作句需要回答谁对谁做了什么，以及结果如何出现。接触前写接近路径，接触时写接触部位和方向，接触后写物件或身体状态。能够观察到的加速度、停顿、回弹和重心变化可以写入；看不清的细节用范围描述，不能补成确定的手指结构或隐蔽动作。

左右必须明确参照系。`her left hand` 指身体左手，`screen-left` 指画面左侧，二者不一定一致。镜像、转身和越过画面中线时尤其注意。位置变化应连成轨迹，例如从胸前斜向画面右下移动，而不只是给起点终点两个静态姿势。视线跟随什么、情绪何时改变，也要与可见证据对应。

物件要维护状态：在哪只手中、是否被放下、是否仍在视野内、遮挡前后是否连续。人物走到遮挡物后面时，描述进入遮挡与重新可见的范围；不要给不可见区编造完整表演。首帧已在进行的动作从当前状态接着写，末帧未完成的动作不要强行收束。

鼠标、换装、脱鞋、尾巴出现或变化都不是默认事件。原片没有就不加入；原片确有这些动作时，按同一套“起始状态—接触或运动—可见结果”的方法客观记录，不套固定情节，不加入性感化或挑逗性的解释。普通整理衣服和实际更换服装也不能混为一谈。

### 写时间与接缝

`detailed_description` 使用本段局部时间；分段标题另列全局窗口。时间点来自 planner 与全局记录，不凭语言段落平均分配。段内可以使用少量时间区间，边界落在真实动作转折处，不必每秒写一条。遇到快速接触或镜头切换，再加密关键时刻。

重叠头部描述的是前段已发生或正在发生的同一次动作。先写本段入场状态，再写连续推进；重叠结束后才进入后段独有的新内容。两段在重叠范围内的方向、物件归属、接触时刻和摄影位置应一致。如果前段说手已经握住把手，后段就不能从松手重新伸向把手开始。

不要靠大量否定句代替动作。一句“保持连续”仍需补充握持对象、手的位置与运动状态。

### 文字、标志与声音

先记录源片是否有字幕、界面字、标志或水印，再根据用户保留范围写约束。有原生文字且用户要求保留时，不能同时加笼统的 `no text`；源片有标志且需要保留时，不能同时写 `no logo`。只有源片本就没有相关内容，且不希望额外产生时，才使用对应的泛化限制。

声音与可见动作分别核实。有音轨并不代表有对白，有音乐也不代表需要重新创作。能听清时记录真实声源和出现时点；无法读取或试听时说明声音尚未核实，不能杜撰台词、情绪声或乐器。用户要求沿用原音轨时，提示词中明确避免额外生成相冲突的声音，交付另注明保留或重新合并原音轨的操作。

`overall_soundscape` 与 `non_diegetic_music` 不能互相代替。环境声和配乐都不要默认添加；需要静音时两处各写清范围，同时在导演台设置表核对声音相关选项。字段里写“silent”只表达意图，不证明采样器、合并节点或导出文件已静音。

### 按需使用原文句库

需要动作措辞时，按事件查阅[通用句库](phrases/core.md)；原片存在光标操作、服装或物件变化、线框生成等事件时，再查阅[交互与变化句库](phrases/cursor-edit.md)。句库中的 R 编号只用于内部检索，不进入最终提示词，也不要求每段使用固定数量的句子。

选中条目后逐项对照当前素材，替换所有占位符和不适用的固定颜色、侧别、次数、时长。局部占位符按句意解释，例如填充持续时间不能误用成 planner 的步长 `D`。不同策略的源句选项不能全部拼接；原片没有对应事件时，不调用模块。句库只是措辞素材，最终六字段、媒体编号和时间仍由本次规划决定。

### 提交前自查

逐段独立检查外观来源、镜头、动作起止和声音，再成对检查接缝是否重复触发事件。对照原片核实具体动词，新增动作必须有证据或授权。字段完整不保证模型逐帧复现。

---

<!-- references/cinematography.md -->
## 电影化重拍与参考静帧

本页用于用户明确要求电影化重拍、摄影调整或参考静帧的任务。默认复刻仍以原片动作、镜头和节奏为准。不能因为素材是动漫人物或竖屏短片，就自动增加景深、运镜、慢动作、对白或配乐。

### 先写清授权改变的内容

电影化可以包含光线、色彩、镜头语言、材质和环境氛围，但应由用户要求决定。把本次允许改变的项目列明，并注明哪些仍遵循源片。用户只说“电影感”时，先给与素材相符的简短方向；如果可以采用保守的光色调整，就按该范围推进。只有镜头重构、场景布局或节奏变化会影响核心任务时才追问。

摄影可以重新解释同一事件，却不能任意改变事件顺序。原片先接触物件再转头，不能为了制造悬念倒置成先转头再接触。源视频没有的跌倒、拥抱、服装变化或画外事件，也不能通过“戏剧性”包装成授权范围。慢动作和插入镜头会改变原时间轴，应先获得相应节奏修改意图，再重新规划。

写明具体改动；仍按真实观察与 planner 编写完整六字段，声音遵从原片与用户要求。

### 根据动作选择摄影变化

先判断动作需要观众看清什么。手与物件的接触是重点时，保留接触区域和前后空间关系；全身重心变化是重点时，避免裁掉脚部；两人互动需要明确谁看着谁，不用过浅景深抹去关键对象。保持空间方向，除非用户要求改动且相邻镜头已重新建立位置关系。

镜头运动要有动作依据。跟随主体移动时交代摄影机相对位置和移动方向，不让摄影机运动与人物运动相互抵消到无法辨认动作。源片固定镜头且只授权光色处理时，保持机位。用户允许重新设计镜头时，也要维护重叠区内相机位置与速度的一致，避免每段开头都重新推近一次。

统一色彩、反差和主光方向，避免冲突的风格词。高反差遮住关键手部动作时减弱暗部压缩，逆光影响身份辨识时调整补光；摄影选择应服务动作可读性。

替换背景时检查地面高度、主体落脚点、接触道具的位置和运动可用空间。新场景应能容纳原动作；不能把原片扶桌边的动作放进没有桌子的环境，又靠提示词让手悬空完成。需要新增对应支撑物时先把它作为场景替换的一部分说明，仍不新增动作事件。

### 为生成准备参考静帧

参考静帧可以用于锁定人物外观、服装、场景关系或某个关键动作状态。先写用途，再选时刻。身份图未必需要复制视频姿势；动作状态图则必须来自对应源时间。不要把多个时间点中各自最漂亮的手、脚和表情拼成源片从未出现的一帧。

优先选择信息明确的时刻：接触前能看清对象位置、接触时能看清手与物件关系、重叠边界能看清入场状态。没有必要为每一帧写图像提示词。用户只要求一张正面身份参考时就交付一张；不要自动追加多角度套图。用户已给可用参考时先复用，不默认要求重新生成。

每张图的中文说明应包含用途、对应源时间或事件、镜头构图、主体状态和替换范围。英文提示词描述该瞬间的可见画面：人物外观来源、身体朝向、接触关系、道具位置、摄影机位置、景别、光色和需要保留的文字。静帧不需要装入完整时间段的连续动作，也不必强行使用视频六字段结构。

如果提示词将用于支持参考图的图像工具，媒体编号遵循该次真实分配；不知道工具是否支持同一引用方式时，用明确文字说明参考用途，不编造 `Picture` 槽位。比例来自用户目标或已确定的视频设置，不能从一张横版人物图推断目标视频也应横版。

### 把静帧接回视频规划

静帧只是局部画面依据，视频动作仍来自真实观察记录。将静帧放入某段时，在媒体表中写明用途：身份约束、场景约束或该段起始状态。不要因为静帧画面漂亮，就把它的姿势强塞进所有段落，造成每段都回到同一个站姿。

若静帧用于接缝，检查它与前后窗口相应时刻是否一致，尤其是手中物件、遮挡、视线和摄影方向。生成静帧发生外观或姿势偏差时，先修正该图或减少其权限；不要把视频观察记录改成跟随错误图片。文档只准备了静帧提示词时，报告尚未生成或验看实际图片。

完成后按 [quality-check.md](quality-check.md) 检查动作顺序、接缝与授权范围，实际生成后再验看动作。

---

<!-- references/delivery.md -->
## 组织可使用的交付

### 完整复刻说明的顺序

先用简短中文说明复刻范围：哪段源视频、替换对象、保留内容、生成比例与声音要求。随后给出已观察到的全局动作和摄影记录，区分未确定的局部细节。不要长篇复述全部分析过程，但重要的未知项要能让用户看见。

用一两句摘要说明 planner 的实际结果，包括源时长、生成帧率、段数和尾裁。完整的 `F/L/O/D/N/E/P`、各段帧与秒区间、重叠范围和素材分配统一放在文末的导演台设置表，避免在代码块之间插入操作说明。若用户只要分段表，就直接交付计算结果，不必生成未请求的提示词。

逐段内容按相同顺序排列：标题注明段号和全局窗口，然后给出一个独立代码块，完整包含六字段英文提示词。入场、出场状态及本段局部媒体编号在相应字段内解释。段号只是识别标签；需要几个时间框由 planner 决定。不要复用某份示例的固定段数，也不要因篇幅较长而省略后段字段。

结构示意如下，交付前用本段实际观察与规划替换全部占位符：

```text
subject_definitions:
{{subjects and assigned reference roles}}
summary:
{{this segment's visible event}}
retention_analysis:
{{retained facts and authorized replacements}}
detailed_description:
{{local timing, motion, contacts, camera and carried state}}
overall_soundscape:
{{verified sound plan}}
non_diegetic_music:
{{verified music plan or no added music}}
```

最后给出导演台设置表，详细检查项目见 [director.md](director.md)。若用户只要设置，使用现有规划和素材信息直接填表；缺少当前保存参数时将该项标为待核对，不凭经验填采样步数或按钮状态。

### 素材与提示词对应

媒体分配表要逐段写，至少包含局部编号、实际素材、承担的作用。例如某张图提供身份，另一张图提供服装；不要只写“参考图都放进去”。同一素材在不同时间框中的编号可以变化，提示词必须随实际分配一起检查。

可以用显示名称或用户给出的文件名帮助识别；文档模板不包含作者账号、个人目录或固定盘符。没有实际找到文件时，写“待提供的角色正面图”等明确状态，不把建议素材当成已存在的资源。用于接续的 Latent 单独说明连接用途，不放入图片或视频编号序列。

参考静帧任务按每张图交付：对应用途、源时间或事件、需要保持的构图和动作状态、允许替换的内容、完整英文图像提示词。只为后续生成准备静帧提示词时，不声称已经产出图片。具体写法见 [cinematography.md](cinematography.md)。

### 给出真正可执行的裁尾办法

当 planner 返回 `P > 0` 时，在说明中写出“预计合并输出 E 帧，最终保留 F 帧，裁去 P 帧”，并标明动作内容只覆盖源片范围。后段重叠去重和最终尾裁是两项工作；完成前者不能证明后者已完成。

下面是交付命令的写法。交付时必须把变量设置为本次实际文件、planner 的 `F` 和核实后的原音轨时长 `T`，不能只给占位词就称裁尾已解决。例中的 240 帧、10 秒仅对应 10 秒规划样例；其他任务必须替换。

```powershell
$MergedVideo = 'merged.mp4'
$TrimmedVideo = 'trimmed.mp4'
$KeepFrames = 240
$KeepSeconds = 10
```

若合并文件中已有需要保留的音轨，可在 PATH 中的 FFmpeg 执行：

```powershell
ffmpeg -hide_banner -i $MergedVideo -map 0:v:0 -map 0:a:0 -vf "trim=end_frame=$KeepFrames,setpts=PTS-STARTPTS" -af "atrim=end=$KeepSeconds,asetpts=PTS-STARTPTS" -r 24 -frames:v $KeepFrames -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac $TrimmedVideo
```

若要求用原片音轨替换生成声音，先给出适用于实际文件的重新合并方案，再裁尾。源视频只取中间一段时，按已确认的起点截取对应音轨，不能直接从整片零点对齐。

没有音轨或明确静音时，不映射音频，也不套用音频滤镜：

```powershell
ffmpeg -hide_banner -i $MergedVideo -map 0:v:0 -vf "trim=end_frame=$KeepFrames,setpts=PTS-STARTPTS" -r 24 -frames:v $KeepFrames -an -c:v libx264 -crf 18 -pix_fmt yuv420p $TrimmedVideo
```

这些命令会重新编码视频，输出文件名应与输入不同。FFmpeg 不在 PATH 时使用已配置的可执行文件变量。只有获得执行授权并实际运行后，才能报告裁切完成；否则明确写“裁尾命令已备好，尚未执行”。执行后还要检查视频帧数、时长、音轨和末尾画面，而不是凭进程退出成功认定视觉通过。

### 结尾状态说明

分别报告素材观察、帧规划、提示词、界面核对、生成和尾裁的状态。已实际完成的项目附对应证据，不把静态文档检查概括为全流程验证。

---

<!-- references/director.md -->
## 导演台时间框设置与接线核对

本页按 MiniMax H3 Timeline Director 0.8.0 时间框模式适配，未证明每个本地安装均通过实测。命名、接口或控件不同时，以当前保存参数和代码为准，说明差异。

### 核对数据如何流动

基础关系是：素材规划台的“分段规划”输出，连接有限分段采样的“有限分段规划”输入；采样得到的分段结果按对应接口合并视频和音频，再以 `CreateVideo` 按 24 fps 封装，交给 `SaveVideo` 保存。核对实际端口类型与节点版本，不仅看画布上节点摆放顺序。

一个可读的说明可以写成：

```text
素材规划台：分段规划
    → 有限分段采样：有限分段规划
    → 合并视频 / 合并音频
    → CreateVideo（24 fps）
    → SaveVideo
```

优先按表核对时间框。未看过当前界面时注明操作顺序未验证；不自动启动 ComfyUI、提交 GPU 生成或写工作流文件。

### 共享库与每段分配分开核对

共享素材库表示素材可用，不表示已经进入全部时间框。每一段都核对实际分配的图片、视频和用途，再核对本段提示词中的编号。界面若在每个时间框内重新排列媒体编号，文案也必须按本段重新排列，不能沿用共享库的全局顺序。

为每段附一张小表：本段序号、全局窗口、局部媒体编号、文件或显示名称、用途。人物身份图、服装参考图和动作视频各自说明作用；不需要某张图的段落可以不分配，但提示词不能继续引用它。把继续生成的 Latent 作为接续数据核对，它不占用 `Picture` 或 `Video` 编号。

只要任意一段填写局部提示词，全局提示词就不再生效，所有时间框都要填写完整内容。因此不要把人物定义放全局、动作放局部后就认为每段完整。每个时间框都应带完整六字段，且与本段媒体分配对应。修改全局提示词后，要逐段检查实际生效内容；不能推定所有局部字段已同步变化。

### 交付用设置表

下表给出项目与取值依据。正式交付应填本次实际值；只能从当前工作流确认的项目保留“待核对”，不要把样例数字填成实测参数。

| 项目 | 取值依据 | 核对重点 |
| --- | --- | --- |
| 工作模式与版本 | 当前节点保存信息；本说明按 0.8.0 时间框模式适配 | 实际模式一致，版本差异已标出。 |
| 目标时长与保留帧数 | 源范围、planner 的 `F` | 不把源 fps 当生成 fps，不混用整片与截取段。 |
| 段数与段窗口 | planner 的 `N` 及逐段范围 | 时间框数量对应实际规划，最多 64 段。 |
| 段长、重叠、起点间隔 | planner 的 `L/O/D` 与各段实际值 | 尾段单独核对，不能全段照抄默认值。 |
| 图片和视频分配 | 各时间框实际媒体列表 | 局部编号与提示词一致，文件已找到。 |
| 局部提示词 | 本段完整六字段 | 没有依赖失效的全局补充内容。 |
| 接续数据与重叠处理 | 当前节点支持的连接方式 | 后段承接同一次动作，合并没有再拼入一份重叠。 |
| 宽高与显示比例 | 用户要求、实际源画面和当前支持参数 | 角色与场景参考没有被误当成输出比例。 |
| 采样步数及其他生成参数 | 当前保存值和代码 | 不把别人的固定值或旧模板值列为通用要求。 |
| 声音相关选项 | 原片实有声音、用户保留方案、实际节点参数 | 提示词、采样、合并、封装的声音意图一致。 |
| 封装 fps | `CreateVideo` | 24 fps，与 planner 相同。 |
| 最终尾裁 | planner 的 `E/P` 与原音轨时长 | 节点去重后仍需按 `F` 和音轨时长处理多余尾部。 |
| 保存位置与文件名 | 用户指定或当前明确配置 | 交付中说明位置，不植入模板作者的个人目录。 |

分段表与界面数量不一致时，先找出漏段、尾段或时间框重复，不能删减动作文字掩盖差异。

### 合并与尾裁各自确认

后段头部有重叠，是为同一动作提供接续范围。按此版本约定，节点合并时处理后段重叠去重；不要再手工把全部窗口逐段首尾相接，否则重叠事件会重复，时长也会增加。实际节点行为与约定不一致时，检查当前代码和结果，不先修改 planner 的窗口补偿。

去重后预计结束位置看 planner 的 `E`。若仍超过 `F`，按 [delivery.md](delivery.md) 的尾裁方案处理。不要拿“已设置重叠”作为尾部帧数正确的证据，也不要将正常重叠重复误诊为原片有两次动作。

---

<!-- references/quality-check.md -->
## 按证据检查交付质量

提交说明或分析失败结果时，分别记录文档检查、界面核对、视频验看和声音试听的证据。

### 先检查是否理解了任务

对照用户原话检查替换范围。只换人时，衣服、场景、摄影和声音是否按约定保留；换装时是否误换身份；电影化重拍是否越过授权改了动作。出现多个主体时，替换目标必须能明确识别。用户已有的素材、限制和选择应沿用，不能重新发菜单或反复索取。

逐个具体动作对照源视频观察记录。参考图只证明外观时，不应用它证明视频中的站姿或手势。未见的首尾、遮挡中的过程、不可读的文字、未试听的对白都不能写成已确认。若实质信息仍未知，交付中标出影响，或补充有针对性的观察；不通过增加形容词掩盖缺失证据。

### 检查时间轴是否能落地

确认本次实际运行过 planner，保留其输出或准确摘要。检查生成 fps 为 24，目标 `F` 对应所选源范围，`N` 不超过 64，各段范围和 `N/E/P` 没有被手工改写。段长满足 `5+17n` 且不超过 3592，重叠是允许值且小于对应段长；尾段也必须合法。

全局时间、全局帧和局部时间要采用同一套起点。排他末帧不应被写成最后一个包含帧。可变帧率素材以展示时间定位，不能只根据平均帧率猜源动作发生位置。对临近取整边界的事件，必要时保留原时间与量化后帧号，便于解释一帧级差异。

重点成对检查接缝。前段重叠尾与后段重叠头应指向同一次抓握、转身、移动或镜头变化。比较两端身体朝向、接触对象、物件归属、运动方向、视线和摄影位置。后段新内容如果被写入头部重叠，可能造成事件重演；先调整叙述时间和入场状态，不凭空增加过渡动作。

确认尾部有明确方案：`P=0` 时没有额外补齐可裁；`P>0` 时说明保留原 `F` 帧与原音轨时长，提供已填实际值的命令或明确待执行步骤。提示词里的停止描述不算裁尾。若裁尾已实际执行，检查最终帧数、末尾画面、音轨与音画结束位置。

### 检查提示词与媒体引用

每段应完整包含六字段，且脱离其他段仍能理解主体、镜头、动作和声音。英文提示词中的人物称呼稳定；身体左右与画面左右没有混淆；关键轨迹和接触关系写清；状态变化有前因后果。删掉无来源的道具、动作、对白和情绪解释。

逐段对照实际媒体分配检查所有 `Picture`、`Video` 编号，不能按共享库顺序推测。Latent 不在媒体编号内。局部提示词已填写的时间框，不依赖全局字段补全。原生文字或标志的保留要求与负向限制不冲突。

声音至少检查三层：原片有什么、文案要求什么、实际声音相关设置是什么。无法试听时只报告未核实，不把“有音轨”写成“有对白”。用户要求静音时检查环境声、配乐、采样和导出；用户要求原音时检查是否仍混入生成声音。仅有字段文本不能证明最终音轨正确。

### 用户给出失败结果时

先读取结果本身，获取真实时长和音轨，再抽取出问题前后与相邻接缝的画面。将结果与同一源时间对照，区分外观漂移、动作顺序错误、重复触发、媒体引用错误、镜头变化、声音问题或尾部未裁。不要只根据一张失败截图判断整段运动。

外观错误先查素材分配和主体定义；动作重复查重叠状态与合并；尾部过长查 `E/P` 和尾裁；镜头偏移查有无额外摄影指令。保留用户已接受的部分。

### 报告检查边界

可以报告“已核对所有分段字段与 planner 结果”或“已观察该接缝的源片和生成片”。只有实际播放并听过，才报告视觉与声音的验看范围。未经当前界面验证的设置表要注明；没有运行 GPU 就不说生成通过。即使一次结果可用，也不承诺模型以后每次逐帧一致。

---

<!-- references/phrases/core.md -->
## 通用句库（R 编号沿用原稿）

按需读取：只在组装某一镜、需要对应控制句时才打开本文件，不要整份贴进提示词。

用法：

1. 先选事件，再核实句子里的每一项事实，用当前素材的值替换全部 `{{...}}`。
2. 每条都是**条件句**：原片没有对应事件就不用，不补位。
3. 示范句里写死的左右、颜色、身体部位、次数、时长，只有与当前原片一致才能原样保留；否则保留“因果与连续性”的目的，改写其余部分。
4. 同一条下的“源句选项”是互斥用途，挑适用的，不要全拼。
5. R/S/Q 内部编号不得泄漏进最终提示词。R40、R49 原稿未定义，不补造。
6. 涉及光标、换装、鞋袜、生成物、线框建模的句子在 `cursor-edit.md`。

### 风格、环境与光照

#### R01 · 风格与场景锚点

```text
Style: {{current visual style}}. The scene is {{current environment and layout}}, with {{observed lighting and material treatment}}. Preserve these established properties except where the source video or the requested edit explicitly changes them.
```

#### R02 · 未发生变化的背景保持

```text
Throughout {{interval}}, the background retains {{established scene state}}. Only {{observed changes, if any}} occur at their specified times.
```

#### R03 · 曝光与光照连续

```text
During {{interval}}, exposure, white balance, light direction and skin tone follow {{observed lighting progression}}. Removing or replacing {{item}} does not introduce an unrelated lighting change.
```

### 首帧、切镜与段间衔接

#### R06 · 原片开场状态

```text
[Shot 1] <Subject 1> is already in {{source first-frame pose, position and orientation}}, with {{hand positions, gaze and expression}}. The camera has {{source framing and movement}}. Continue {{motion already in progress}} without adding a preparatory pose.
```

#### R27 · 切镜状态继承

```text
At this cut, {{visible carried state}} continues from the preceding shot, including {{expression, gaze and item states}}. {{observed changes after the cut}} occur at their specified times.
```

#### R28 · 段尾运动状态交接

```text
During {{tail interval}}, {{visible subjects and objects}} continue {{exact observed motion phases and emotional progression}} with {{camera movement, framing, environment and active sound}}. At the final frame, {{end state}}. This interval continues into the next segment without restarting.
```

#### R29 · 段首重叠接续

```text
During 00:00.000–{{overlap end}}, this segment carries the preceding segment’s final {{actual overlap frames}} frames: {{the same observed action phases, expression changes, positions, objects, camera and sound}}. This is the same occurrence, not a repeated action. After {{overlap end}}, continue the source-aligned timeline.
```

#### R67 · 段首动作相位保持

```text
The opening continues the preceding tail at the same movement phase and speed. Preserve {{motion already in progress}} without resetting the pose or inserting a pause.
```

#### R30 · 静止待机，仅原片静止区间用

```text
During {{interval}}, <Subject 1> maintains {{observed stance}}. Only {{observed breathing or small movements}} occur.
```

#### R32 · 固定机位，仅原片对应区间用

```text
The camera holds the source framing without moving during {{interval}}.
```

#### R22 · 相机环绕

```text
During {{interval}}, the camera moves around <Subject 1> along {{source direction and arc}}, from {{start view}} to {{end view}}, with {{observed speed profile}}. {{character movement or stationary stance}}. Preserve any source cut separately; do not substitute a body turn for a camera orbit.
```

#### R31 · 环绕时人物不动，仅符合原片时用

```text
During {{orbit interval}}, {{observed stationary body parts}} remain in place while the camera moves. {{observed independent movement}} continues.
```

#### R66 · 局部支撑锁定

```text
During {{interval}}, {{actual support foot or stationary body part}} remains at {{observed support position}} while {{moving part}} performs {{source action}}.
```

### 动作因果与接触

#### R60 · 施动者语法

```text
{{actual actor}} {{contact verb}} {{item}} at {{contact point}} and moves it along {{observed path}}. {{observed response of the body or object}} follows this cause.
```

#### R61 · 可见抓握接触

```text
At {{TS}}, {{actor contact point}} meets {{item contact point}}. {{material-appropriate deformation or rigid contact}} remains consistent as the item follows {{observed motion}}.
```

#### R62 · 身体跟随物件

```text
During {{event}}, <Subject 1> responds with {{observed limb, hip, head and secondary motion}}. The hands stay at {{actual hand positions}} unless the source shows a hand action.
```

### 视线、情绪与反应

#### R04 · 事件反应的运动层次

```text
The reaction follows the timing in the source: {{observed anticipation, response and settling}}. {{secondary part}} follows with {{observed delay and amplitude}}.
```

#### R05 · 跨镜表情连续

```text
At each cut, preserve the expression and emotional intensity reached immediately before it, then follow the next observed expression change at its source-aligned time.
```

#### R08 · 好奇反应，原片存在时用

```text
At {{TS}}, the eyes track {{observed target}}, while {{observed head, brow, mouth and shoulder response}} conveys curiosity at {{observed intensity}}.
```

#### R09 · 情绪区分

```text
The expression during {{interval}} is {{observed emotion}}, carried by {{visible facial and body cues}}; it does not restart as a different reaction at the segment boundary.
```

#### R11 · 事件第一反应

```text
The reaction begins at {{TS}} relative to {{trigger event}}: {{observed eye, mouth, head, shoulder and hand response}}.
```

#### R11b · 已有情绪上的再次反应

```text
At {{TS}}, {{observed response to the new event}} develops from the expression already present. {{Existing facial colour or other visible emotional cue}} follows {{observed change}}, without resetting the face first.
```

#### R12 · 脸红，原片或用户要求时用

```text
At {{TS}}, a {{observed colour and intensity}} flush {{appears or deepens}} on {{observed facial areas}}, following {{observed onset and fading progression}}.
```

#### R13 · 手部反应与次级运动

```text
At {{TS}}, {{hand action and contact position}} follows the event. {{visible clothing or attached-part response}} settles according to the observed motion, while the gaze remains on {{target}}.
```

#### R14 · 视线跟随离场物

```text
The eyes follow {{item}} along {{observed path}} toward {{exit edge}}. The head follows by {{observed amount}}, and the gaze next moves to {{next observed target}} at {{TS}}.
```

#### R20 · 操作过程视线

```text
During {{event interval}}, the eyes of <Subject 1> follow {{pointer or held item}} along {{observed trajectory}}. At {{TS}}, the gaze shifts to {{next observed focus}}.
```

#### R72 · 事件与视线反应对应

```text
For each observed interaction, the gaze follows {{actual focus}} and the response begins at {{source-aligned time relative to the event}}. Pointer travel alone does not create an additional reaction unless the source shows one.
```

#### R73 · 重复事件的反应强度

```text
The response to this repeated event is {{observed intensity relative to the first}}, with {{visible expression and body response}} at {{TS}}. It does not automatically repeat the first surprise.
```

#### R75 · 展示动作的情绪与时长

```text
During {{display interval}}, {{observed action}} accompanies {{observed expression and gaze}}. The movement uses {{observed amplitude and count}}, with {{observed hold and return timing}}. Preserve the source timing without adding repetitions.
```

#### R48 · 视线环顾

```text
During {{interval}}, the gaze moves through {{ordered visible targets}}. The eyes and head follow {{observed lead or delay}}, with {{observed turning amplitude and settling}}. {{torso, shoulder, hair and foot behaviour}} matches the source.
```

#### R48b · 视线扫描次数

```text
There are {{observed count}} looks during {{interval}}, toward {{ordered targets}} at {{source-aligned times}}.
```

#### R48c · 转头幅度

```text
Each head turn follows {{observed angular or screen-relative range}} toward {{target}}. Preserve the source relationship between eye movement, head rotation and any torso turn.
```

### 身体动作（仅原片存在时）

#### R21 · 观察脚部，原片存在时用

```text
At {{TS}}, <Subject 1> looks toward {{observed side and target}} with {{observed head and eye motion}}. {{actual foot placement or movement}}. The look lasts {{observed duration}} and proceeds to {{next observed focus}}.
```

#### R36 · 弯腰与相机关系

```text
At {{TS}}, <Subject 1> bends toward {{observed target}} with {{head, shoulders and waist motion}}. The camera {{observed stationary or moving behaviour}}, maintaining {{source composition}}.
```

#### R37 · 伸手动作

```text
At {{TS}}, {{observed hand}} reaches toward {{target}}, with {{palm orientation, fingers and elbow pose}}, and holds or withdraws according to {{observed timing}}.
```

#### R38 · wink 与眨眼计数

```text
At {{TS}}, {{observed eye}} closes in {{observed wink duration}} while {{other eye and mouth expression}}. Preserve {{observed wink and blink counts}} during this interval.
```

#### R68 · 抬脚展示，仅原片存在时用

```text
During {{interval}}, <Subject 1> lifts {{observed foot}} with {{knee and hip motion}}, reaching {{observed height or angle}}. The camera uses {{source view}}. {{observed hold or ankle movement}} lasts {{duration}} before {{observed lowering or continued lift}}. The face and gaze follow {{source expression and focus}}.
```

#### R69 · 弯腰触腿，仅原片存在时用

```text
At {{TS}}, <Subject 1> bends with {{observed body motion}} and {{hand}} touches {{actual contact area}}, moving along {{path}} for {{observed count and duration}}. {{observed recovery or continuing pose}} follows.
```

#### R70 · 脚部细节，仅原片存在时用

```text
During {{interval}}, the camera frames {{observed area}}. {{observed foot and toe action}} occurs with {{actual count, amplitude and duration}}, while {{support and other-side state}} remains consistent.
```

#### R71 · 面部细节

```text
During {{interval}}, {{source face framing}} shows {{observed eyes, brows, mouth, head and colour progression}}. Preserve the expression carried from the preceding view and its source-timed changes.
```

#### R57 · 卧姿腿脚运动，仅原片存在时用

```text
During {{interval}}, the legs and feet follow {{observed alternating or simultaneous movement}}, with {{observed amplitude, rate and count}}. This movement continues with {{concurrent upper-body action}} according to the source timing.
```

### 结尾与手势

#### R39 · 原片结尾

```text
From {{TS}} until the source ending, {{observed final action or held pose}}, with {{remaining movement, expression and camera behaviour}}. Do not append a new closing gesture.
```

#### R54 · 比心

仅原片有比心；手势保持与回收时点按原片，不自动加入收尾。

```text
Both hands come up in front of the chest and the two hands form one small heart aimed at the lens, held for one beat, then the two hands come apart and drop back to the sides.
```

#### R55 · 上半身特写 wink 收尾

仅原片对应 wink/上半身镜头适用；删去与原片不符的脸红、变焦和消退动作，时间来自本期。

源句选项 1：

```text
At {{TS}}, upper-body close-up, framing the body from the mid-chest to above the top of the ears, both ears and both shoulders inside frame: there is no cut, the camera pulls back slightly in one continuous 0.3 second move and then locks. Both hands come away from {{头部部件}} and drop to the sides in one small move. The head lifts and the eyes come up to the lens, and in that same instant a pink flush spreads across the cheeks, the bridge of the nose and the tops of the ears, the flush on the face only. The head tilts to one side by about ten degrees, one eye closes in a clean wink while the other stays open on the lens, and the mouth presses into a small playful smile. The wink is held for a quarter of a second, then both eyes are open on the lens and the head comes back level, and the flush fades out completely as the head levels.
```

源句选项 2：

```text
The face carries no colour from one second into this clip until the last shot; in the last shot only the face may take colour, and it is gone before that shot ends; the neck, the chest and the décolletage never take colour.
```

### 声音

#### R33 · 环境声音

```text
{{verified ambient sound and its continuity across the interval}}.
```

#### R34 · 无对白无音乐，仅实际静音设置适用

```text
Silent. No dialogue, environmental sound or music is requested; the workflow audio configuration is set to silence.
```

---

<!-- references/phrases/cursor-edit.md -->
## 光标交互与物件变化句库（条件模块，R 编号沿用原稿）

**只在原片确实出现这类事件时读取**：鼠标/光标操作、外层衣物或鞋袜被移除、物件沿轨迹或点选生成/替换、线框填充开场、场景线框建模。原片没有的事件、物件与配饰不出现、不补位。

这些句子来自最初那个案例，里面有不少写死的画面内容（青色线框、浅灰背景和地面网格、粒子颜色、半秒消散、粉色脸红等）。**只有当前原片吻合时才能原样使用**，否则改写或删除。

### 主体编号沿用约定

仅在使用本模块时沿用，其余场景按首次出现顺序给主体编号，全片保持稳定：

| Subject | 含义 |
|---|---|
| 1 | 角色 |
| 3 | 光标 / 操作者 |
| 5 | 角色部件 |
| 7 | 腿部 |
| 8 / 9 | 生成物（沿轨迹生成 / 点选生成） |

不存在的主体不强行创建；每段只引用本段有定义的主体与实际分配的媒体。

### 策略互斥提醒

- R42（画外脱）、R43（同步后分侧）、R44（袜圈落地 + 抬脚）、R45（相机下摇）是四套互斥的处理策略，一次只选一套，且必须与原片一致或经用户授权。
- R44 存在抬脚时，禁止同时使用“双脚钉地”之类的静止锁定（见 R62s / R66）。
- R44 的整体环（选项 1）与两个独立环（选项 5）不能同用。

### 开场建模与线框填充

#### R53 · 开场线框 + 一次填充

仅当前视频确有线框填充开场时用。图像身份和本期实际线框外观分别核对。

```text
At 00:00.000 there is no finished body yet: <Subject 1> is a cyan wireframe over a grey mannequin, only edges and construction lines, no skin, no hair colour, no garment surface and no face detail. The tip of <Subject 3> taps once on the wireframe chest, a dashed halo closes there, there is one brief flash, and the form fills in one continuous pass from the feet up to the head in under {{D}} seconds, the surfaces appearing behind the travelling fill line.
```

#### R53b · 形态锁定

Picture 编号按本段分配重映射；不可脱部件仅列确实不变的部分。

```text
The wireframe is the silhouette of <Picture 1> and nothing else: when the fill is finished, <Subject 1> is exactly <Picture 1> - the same face, the same hair, the same proportions, with every {{不可脱部件}} in place - and the worn outfit is exactly {{图1 服装清单}}.
```

#### R53c · 一次填充 + 无线框残留

仅当前原片是一次完整填充且没有残留时用。

```text
The fill happens once, in one pass, with no second pass and no half-filled body: no wire line, no construction line, no grey mannequin and no bare edge remains anywhere on the body after the fill, and the fill changes nothing else in frame - the background colour, the floor grid, the light direction and the exposure stay exactly as they were.
```

#### R53d · 填充粒子

粒子与配色必须来自本期视频/用户指定；无粒子删此模块。

```text
The fill is not quiet: as the fill line travels up the body, small cyan particles run along the wire lines just ahead of it and settle into the surfaces behind it, and every wire edge brightens where the line passes. The particles are cyan and grey only, they are gone within half a second after the fill reaches the head, and the light grey background, the floor grid, the light direction and the exposure stay exactly as they were.
```

#### R53e · 填充完成的第一反应 + 光标去向

原片第一反应与光标去向不同则相应改写；不自动恢复疑惑待机。

源句选项 1：

```text
The instant the fill reaches the head, <Subject 1> takes one breath, the eyes come onto the pointer tip and stay there, the head tilts to one side and reads it, and the mouth presses into a small puzzled line; <Subject 3> stays in frame at chest height, still, in front of <Subject 1>.
```

源句选项 2：

```text
the arrow moves away from the chest and slides back in from screen-{{SIDE}}
```

### 光标：入场、数量、可见性、选中

#### R07 · 光标入场或在场移动

只在当前视频此时确有光标入场时调用；已在场就描述实际移动，不再写入场。

```text
At {{TS}}, <Subject 3> {{enters from the observed screen edge or moves from its already-established position}} along {{source trajectory}}.
```

#### R35 · 光标数量

```text
<Subject 3> is the {{observed cursor appearance}}. Exactly {{observed count}} cursor is present during {{observed visibility intervals}}, following the source trajectory and interaction order.
```

#### R46 · 光标可见性

```text
During {{operation interval}}, the pointer remains {{source visibility and contact relationship}} and follows {{item or stroke}}. It exits or becomes occluded only at {{observed time and cause}}, without an unexplained disappearance.
```

#### R76 · 点选生成的光标在场

仅原片光标点选可见时用；遮挡、出入画与接触时长取原片。

```text
<Subject 3> is visible in every frame of this beat: its tip travels from inside the frame onto {{target_part}}, the halo closes there, there is one click, the tip stays on that spot through the flash, and it leaves only after the particle ring is gone.
```

#### R10 · 选中框

仅原片有选中框；框形、选中范围、情绪与时间按实际记录。

```text
The arrow stops in front of the {{部位}} and a dashed selection box closes on it, from {{上界}} to {{下界}}; the head tilt grows a little, the eyes drop down the box, still reading it, and one shoulder lifts slightly.
```

### 外层衣物、鞋袜与织物移除

#### R15 · 光标拖走外层，仅该事件适用

```text
The tip of <Subject 3> hooks {{garment}} at {{contact point}} and travels along {{observed path}}. The garment follows the tip out through {{exit edge}} as an empty garment, with {{observed motion blur}}. The removal lasts {{observed duration}}, and the pointer follows its recorded exit timing.
```

#### R16 · 已有内层与表面分离

```text
Throughout this removal, {{retained outfit}} is already worn underneath and remains in place. Only {{removed garment}} separates from the body; the character and retained outfit stay continuous. {{observed hand behaviour}}.
```

#### R17 · 物件先后顺序与次数

```text
{{actor}} removes {{ordered item list}} in the order {{observed order}}, each exactly {{observed count}} time. Each item retains its recorded state afterward until another specified event changes it.
```

#### R18 · 鞋被带动脱除

```text
The tip of <Subject 3> takes hold of {{side and shoe}} at {{contact point}} and carries it along {{source path}}. The foot follows with {{observed lift, ankle response and landing}}, while the shoe separates according to {{observed contact and coverage sequence}}.
```

#### R19 · 软织物协同脱除

```text
<Subject 3> takes hold of {{observed contact point}} and draws {{specified garment or garments}} along {{observed removal path}}. {{per-side timing and separate-or-connected garment structure}}. The recorded operation occurs once; the resulting state is {{observed final state}}.
```

#### R50 · 逐侧不对称状态

```text
At {{TS}}, the left leg has {{left state}} and the right leg has {{right state}}. Preserve these different states throughout {{interval}}, changing only {{specified item}} at {{specified event time}}.
```

#### R51 · 单侧织物动作

```text
<Subject 3> takes hold of {{garment}} on {{specified side}} at {{contact point}} and draws it along {{observed path}} during {{interval}}. The other side retains {{actual other-side state and motion}}.
```

#### R52 · 硬筒靴或机械壳体

```text
{{actor}} takes hold of {{rigid item}} at {{contact point}} and moves the shell as one piece along {{observed path}}. {{observed foot or limb response}} accompanies the removal, leaving {{actual remaining parts}}.
```

#### R41 · 覆盖状态时间线

```text
During {{interval}}, {{garment construction and coverage}} follows the observed removal. At {{each relevant time}}, {{per-side visible and still-covered areas}}. Uncovering occurs only as the corresponding part of the garment clears that area.
```

#### R42 · 策略 A 画外脱

仅原片已有画外脱除，或用户明确授权这种调整时选用；后续可见镜头的实际位置按原片改写。

源句选项 1：

```text
framing the body from the hips to mid-shin, the feet below the bottom edge of frame
```

源句选项 2：

```text
The feet are never in frame while any part of the {{袜}} is still on the legs. The arrow pulls the rolled edge down and out of the bottom edge of frame, and the arrow leaves last. The bare feet appear only in the next shot, in the full shot, after the {{袜}} are gone.
```

#### R43 · 策略 B 混合节奏

仅原片确有同步后分侧的动作；时长与侧别按观察改写。不可与另一套同步时序同时使用。

```text
The arrow pulls both leg tubes down together in one continuous move to just below the knees, and there the two tubes separate: the arrow frees the left foot first and then the right, each foot out in under four tenths of a second with motion blur, the toes coming out last, and each rolled band keeps moving down in the same continuous move and never stops at the ankle.
```

#### R44 · 策略 C 袜圈落地 + 抬脚抽出

按物件结构选择整体环或两个独立环；两种不能同用。存在抬脚，禁止同时使用双脚钉地规则。

源句选项 1：

```text
the arrow pulls the whole garment down both legs in one continuous move and it gathers into one loose ring hanging around both ankles
```

源句选项 2：

```text
above the rolled edge the legs are bare skin; below it the fabric stays closed over the feet, and both feet stay inside the ring while it hangs at the ankles
```

源句选项 3：

```text
the left leg lifts straight up out of the ring in under half a second, the ring slides down off the left foot and stays hanging on the right ankle, and the left foot comes down bare on the floor beside the ring; then the right leg lifts the same way and the ring lands flat on the floor
```

源句选项 4：

```text
the arrow hooks the ring and drags it out of the bottom edge of frame in one short flick, the ring following the tip with motion blur, and the ring never reappears
```

源句选项 5：

```text
each stocking gathers into its own loose ring around its own ankle, two separate rings, one per leg
```

源句选项 6：

```text
the right rolled edge stays above the left rolled edge by at least a hand-length the whole way down: the two edges are never at the same height, never side by side, and never join into one band
```

源句选项 7：

```text
the left edge reaches the left ankle first and gathers into a ring around the left ankle only, while the right edge is still running down the right calf
```

源句选项 8：

```text
the legs lift only because the fabric has pooled at the ankles, and no hand of <Subject 1> ever touches it
```

#### R45 · 策略 D 相机下摇跟随

仅原片已有下摇或用户明确授权时用；不凭模板改变摄影机。

```text
The camera tilts down slowly, keeping the rolled edge of the {{袜}} in the middle of frame, so the feet stay at the very bottom edge of frame and out of frame until the fabric has cleared the toes. The tilt is one slow continuous move inside the removal, it stops the instant the fabric leaves frame, and after that the camera is locked.
```

#### R62s · 织物运动与身体关系

```text
During {{removal interval}}, {{garment motion}} occurs while {{observed leg, foot, hip and hand behaviour}} is preserved. Use stationary support only for the limbs that actually remain still.
```

### 沿轨迹生成（尾巴等）

#### R23 · 顺轨迹生成

```text
The pointer travels along {{source path}}, and <Subject 8> is drawn behind its tip from {{attachment or starting point}} toward {{endpoint}} with {{observed formation sequence and timing}}.
```

#### R23b · 尾巴原位幻化

只有原片确有原位替换时用；根部、数量、材质与粒子均按当前素材。

```text
At {{TS}} the {{old_tail}} already on <Subject 1> does not stay: at its base at the base of the spine there is one brief particle flare, the old tail breaks into particles and drifts away along the pointer path, and <Subject 8> is drawn out of that same base behind the pointer tip along that path - root first, then the thickness, then the tip last - as if the cursor were repainting it in one stroke. There is one tail in frame at every moment: the old tail never returns and no second tail appears beside it.
```

#### R23c · 绘制粒子

仅原片有粒子轨迹；颜色、强度与消散时间取实际值，不固定半秒。

```text
The stroke is not invisible: small self-lit {{角色配色}} particles run directly behind the pointer tip along the whole curve, and <Subject 8> solidifies out of them one step behind the tip, brightest where the tip is and thinner behind it. The particles sit on the pointer path only - the light grey background, the floor grid, the exposure and the colour grade stay exactly as they were. The trail stops when the stroke stops and is gone within 0.5 seconds after the tip stops: no glow, no smoke and no loose particles remain around <Subject 8> after that.
```

#### R24 · 生成次数与在场范围

```text
<Subject 8> begins appearing at {{TS}} and develops through {{observed phases}}. There are {{observed number}} strokes. Its state afterward is {{observed persistent state}}.
```

#### R25 · 观察生成与情绪过程

```text
While {{item}} forms during {{interval}}, the gaze follows {{observed focus}}. The expression changes from {{preceding emotion}} to {{observed response}} at {{source-aligned reaction time}} and develops into {{following emotion}}.
```

### 点选生成（头饰等）

#### R26 · 瞬时生成 + 同镜表情翻转

点选次数、闪光与物件出现时点取原片，不强制一次或成对。

```text
the tip of <Subject 3> arrives at {{target_part}} from inside the frame, the halo closes on it, there is one click and one brief flash, and <Subject 9> appears in that instant.
```

#### R26b · 头饰原位幻化

只有原片有原位替换时用；旧部件同时从不可变化清单中移出。

```text
the tip of <Subject 3> arrives at the {{old_headwear}} already on the head, the halo closes on it, there is one click and one brief flash, and in that instant the {{old_headwear}} is gone and <Subject 9> appears at the same place on the head, same anchor point, same height, in one step with no second flash.
```

#### R26c · 生成粒子

仅原片有粒子环；环数、颜色与消散时长以原片为准。

```text
The flash is not empty: at the instant of the flash one ring of small {{角色配色}} particles opens around {{target_part}} and closes inward onto <Subject 9>, which is already solid in the first frame after the flash. There is one ring only, it dissipates within 0.4 seconds, and no glow, smoke or loose particles remain on or around <Subject 9> after that - the light grey background, the floor grid and the exposure stay exactly as they were.
```

#### R58 · 点出部件的近景

生成事件不强制特写；仅原片确有这种取景时用，0.3 秒等数值按原片改写。

```text
At {{TS}}, close-up, the camera moving in from the previous framing in one continuous 0.3 second move and then locking, framing {{target_part}} with the hands at rest and the tip of <Subject 3> in frame, pointing at {{target_part}}.
```

#### R58b · 生成部位离脸远时，同一镜内一次上移到脸

仅原片确有同镜上移到脸时用，不为看到表情新增运镜。

```text
At {{TS2}} the camera tilts up along the body in one continuous 0.4 second move with no cut and comes to rest on the face, still a close-up.
```

#### R47 · 生成瞬间表情变化

```text
At {{event time}}, <Subject 1> shows {{first visible reaction}}. After {{observed delay}}, this develops into {{following emotion}}, expressed through {{specific eyes, mouth, head, shoulders and hands}}.
```

#### R59 · 生成物持续在场与正常遮挡

```text
From {{appearance time}} onward, <Subject 9> retains {{shape, colour, attachment and state}} until {{next observed change or ending}}. Normal source occlusion is preserved. Any confirming touch acts on the already-existing object and does not generate it again.
```

### 场景线框建模

#### R63 · 场景框选 + 场景排他

仅原片确有框选与场景建模；原背景不是空网格时替换背景描述。

```text
At 00:00.000 the arrow tip draws a rectangle around <Subject 1>: four corner brackets appear and the rectangle closes once around the whole body, the arrow resting on the lower-right corner. While it closes, the light grey background and the floor grid are still exactly what they were - an empty viewport, nothing built anywhere in it.
```

#### R63b · 框选时她的反应

实际表情按本次观察记录，不能因框选默认疑惑。

```text
While the rectangle closes, the head tilts to one side and the eyes track the corner bracket nearest the face, the brows lift a little, the mouth presses into a small curious line, and both hands stay loose at the sides.
```

#### R74 · 场景生成时的视线与反应

按原片看向实际生成位置，表情按本次观察记录，不自动惊喜。

```text
The eyes of <Subject 1> stay on the travelling wire: as the lines run out across the ground and rise into the {{场景结构}}, the head follows them at half the angle, and the reaction runs with the build rather than after it - the mouth opens in a small breath as the first wall rises, then the eyes brighten and the head lifts as the {{招牌与灯具}} light one at a time.
```

#### R64 · 场景线框生成 + 粒子

场景结构、线框、粒子颜色和消散时间均以本期原片为准。

```text
The empty viewport builds into {{场景}} in one continuous pass: cyan wire lines run out across the ground from the rectangle and rise into the {{场景结构：墙面 / 屋顶 / 栏杆 / 树干}}, and the surfaces fill behind the travelling wire in the same move. Small cyan and grey particles ride along the wire lines and settle into the surfaces, brightest where the fill is travelling, and they are gone within one second after the build finishes.
```

#### R65 · 招牌依次点亮 + 网格退场

仅原片有灯具依次亮起/旧背景退场时用；无招牌不得编造招牌。

```text
the {{招牌与灯具}} light one at a time in a short row, each with one small flare of the same particles, and the grey floor grid fades out under the built ground and stays gone for the rest of the clip.
```

---

<!-- references/acknowledgements.md -->
## 致谢

感谢视频复刻教程与摄影方法分享者对本项目早期探索的帮助。

### 方法与工程参考

- **小优**：早期摄影分析与影像风格探索参考了[摄影方法参考项目](https://github.com/cOkieeman/xiaoyou-aigc-cinematic-director)及其[上游项目](https://github.com/wubo0927/xiaoyou-aigc-cinematic-director)。
- **ComfyUI-MiniMaxH3-TimelineDirector 项目**：时间框、合法帧长、分段素材与续接机制的工程参考，见[项目仓库](https://github.com/Songssx/ComfyUI-MiniMaxH3-TimelineDirector)。
- **《视频复刻工作书》及相关教程的作者**：提供动作、镜头与连续性写法的参考，并授权本项目公开发布相关技能内容及原文句库。

### 当前版本的取用范围

0.4.0 重新组织了使用说明，按需保留获授权的原文句库；句库集中在 `references/phrases/`，只作为当前素材适用时的措辞参考。当前发行包不附带上游节点代码或示例人物素材。

教程内容按原作者授予的公开发布授权提供，其权利仍归原作者；其他项目的来源链接仅用于说明参考关系，不代表替其授予许可。发行文件的授权范围见随包提供的 `NOTICE` 和 `LICENSE`。
