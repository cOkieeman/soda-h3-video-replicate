# H3 视频复刻

基于参考图片与参考视频，生成 MiniMax H3 的分段复刻提示词。你负责**准确描述**和**合法编排**，不承诺文字提示能保证逐帧一致。

两条总原则：

1. **忠实**：只写看得见的。不补全遮挡后的动作和未展示的部位，不为生成方便新增准备动作、删事件、改镜头或重排时间。
2. **合法**：帧数、重叠、媒体编号必须在节点上可执行。算术交给 `scripts/plan_segments.py`，不要心算。

## 模式

| 模式 | 触发 | 说明 |
|---|---|---|
| **A 忠实复刻**（默认） | 给了参考图 + 参考视频 | 保留动作、分镜、节奏、表情、运镜；只替换用户指定的人物/服装/场景 |
| **B 电影化重拍** | 用户明确要改风格、光影、镜头语言，同时保留动作与时序 | 在 A 的基础上用 `references/cinematic-layer.md` 第 5 节改写风格锚点 |
| **C 参考静帧** | 复刻前要做场景图、关键帧、风格锚点图 | 用 `references/cinematic-layer.md` 第 7 节出图片提示词；身份参考板不走这里 |

用户措辞能判断模式就直接定，不用问。判断不了，或用户只是叫出插件，就出 `references/00-menu.md` 的开场菜单，让用户选编号。

## 读取纪律

按步骤读取对应文件，不读就进入该步骤属于跳步。文件里有该步骤的规则、模板和检查项。下文的 `references/`、`scripts/` 路径都相对于本 SKILL.md 所在的目录。

| 步骤 | 必读 |
|---|---|
| 开场、发素材清单、提问格式、交付后的下一步 | `references/00-menu.md` |
| 收素材、读片、首次回复、提问 | `references/01-intake.md`、`references/cinematic-layer.md` 第 2 节 |
| 填槽位 | `references/02-slots.md` |
| 算分段、写重叠区 | `references/03-timeline.md`，并**运行** `scripts/plan_segments.py` |
| 写动作、情绪、镜头 | `references/04-grammar.md`，按事件从 `references/phrases/core.md` 取句 |
| 原片含光标/换装/鞋袜/生成物/线框建模 | 另读 `references/phrases/cursor-edit.md` |
| 组装与输出 | `references/05-assembly-output.md` |
| 输出前自检、用户反馈问题 | `references/06-checklist.md` |
| 对接 ComfyUI 节点、带用户设导演台（菜单 7 / 下一步“导演台怎么设”） | `references/07-comfyui-wiring.md`（第 2 节是给用户的操作步骤） |

## 执行顺序（不得跳步，不得先写提示词）

0. **开场**：没说方向就出 00 第 2 节的菜单；选了方向就按 00 第 3 节发**一份**素材清单（必需项 + 带默认值的选择题）；方向和素材都齐了就跳过这一步。
1. **识别素材**：图片、视频、当前要求、工作流设置各自的用途。已核实的信息不重复向用户索取。
2. **读片**：实际查看图片；读视频时长、帧率、尺寸、时间戳；检查第一帧和紧随画面，再覆盖全片的镜头、动作、表情；关键事件、切镜、接缝附近加密查看。抽样就称抽样。看不了视频就说明并索取可用素材，不按文件名编时间轴。抽帧命令见 `references/01-intake.md` 的读片命令。
3. **建时间轴**：用读片会记录，填 S10 镜头表、S11 事件表。拿不准的地方标出来，不写成事实。
4. **首次回复**：向用户说明读到了什么、保留什么、替换什么、怎么分段、哪些还不能确定。缺项影响执行就问并等待，问法用 00 第 4 节的选择题格式（编号、字母选项、推荐项在前）；资料完整就在同一条回复里先给方案、再接着给全部提示词。**不得上来就直接输出提示词。**
5. **填槽位 + 算分段**：按 02 填槽位；运行脚本得到 N、各段范围、E、P，以及事件在各段的局部时间。
6. **组装**：按 05 的组装表，从句库取适用的句子，删掉不适用的模块。任何槽位都要填完，内部 Q/S/R 编号不得泄漏进最终提示词。
7. **自检**：逐条跑 06。按 05 第 2 节输出：逐段提示词在前（每段一个独立代码块），导演台设置表在后，最后附上 00 第 5 节的下一步菜单。
8. **迭代**：用户反馈问题时，按症状定位到具体镜头、规则、素材或节点参数；最小修改，贴出受影响分段的完整六字段。改动交接区要同步更新相邻段，时间框有变化就重跑脚本。

## 冲突裁决

1. 用户当前明确要求决定保留与替换的范围。技术上做不到就说明原因，不假装已实现。
2. 当前素材的实际观察决定内容与时序；当前工作流的代码/保存参数决定帧数、接缝和媒体编号是否可执行。
3. 槽位（02）记录取值，脚本和 03 是时间计算的唯一依据，05 是组装的唯一流程。
4. 句库是条件措辞库，**不是剧情来源**：句子里默认的颜色、侧别、身体部位、时长不得覆盖当前视频。
5. 摄影层的偏好（克制、不看镜头等）只在模式 B 且用户授权范围内生效；模式 A 一律以原片为准。
6. 对同一事件有冲突，先修正源数据，再同步所有引用；不靠优先级把矛盾原样留在成品里。

## 配置块（换节点或换配置只改这里和脚本的默认值）

| 项 | 当前值 |
|---|---|
| 节点 | MiniMax H3 Timeline Director 0.8.0，时间框模式 |
| 时基 | 24fps |
| 合法段长 | `5 + 17n` |
| 常规段长 L | 107 帧（4.458333 s；用户单段上限 4.5 s） |
| 常规重叠 O | 39 帧（1.625 s） |
| 步长 D | 68 帧（2.833333 s） |
| 合法接缝 | 0、1、5、22、39、56… |
| 段数上限 | 64 |
| 提示词语言 | 默认英文提示词、中文解释；用户明确要求才切换 |

## 最容易出错的七条

1. 不继承上一期的段数、时长、鼠标、鞋袜、猫耳、尾巴、灰色网格、脸红或收尾动作。
2. 首帧来自视频，不从图片站姿过渡。
3. 重叠区是**同一次**过程，不是新剧情容量；新内容从局部第 39 帧开始。
4. 提示词不能执行裁剪：P > 0 要另有实际裁剪步骤，未执行就标“待裁”。
5. 只要任意一段有本段提示词，全局提示词就失效，每段都要完整写。
6. 左右分别说明画面左右与解剖左右；不写互相矛盾的锁定（抬脚 + 双脚钉地）。
7. 六字段固定顺序，每段一个独立代码块；放图、声音、裁剪等导演台设置统一放在文末设置表，不夹在提示词中间。


---

> **单文件版**：各章已全部内联在下面，文中“读取某文件 / 某节”即查阅对应章节。
> 这个环境不能运行脚本：开始前请先在本机运行 `python scripts/plan_segments.py --seconds <时长> --events <事件秒数>`，
> 把输出的分段表贴进对话，分段数字以该表为准，不要心算。


---

<!-- references/00-menu.md -->
## 00 · 开场菜单、素材清单与提问格式

目标：用户不用知道流程，只要**选编号、照清单交东西、做选择题**。

### 1. 什么时候出菜单

- 用户只是叫出插件、没说要做什么，或说“开始”“怎么用” → 原样输出第 2 节的菜单，等用户选。
- 用户已经说清方向，素材也给齐了 → 跳过菜单和清单，直接按 SKILL.md 的执行顺序走。
- 方向说清了但素材不全 → 跳过菜单，只发第 3 节的清单，已给的不再要。
- 用户中途换方向 → 重发新方向的清单，已给的素材沿用。

### 2. 菜单

```text
这个插件能做下面几种，回复编号就行。1–4 可以组合，例如“1+2”。

1. 换人复刻：动作、镜头、节奏照原片，把人换成你的角色
2. 换装：动作照原片，换服装或造型
3. 换场景：人和动作照原片，背景换成别的地方
4. 电影化重拍：动作和时序照原片，重做画风、光影和镜头质感
5. 参考静帧：先出场景图、关键帧的生图提示词，给复刻当参考图
6. 只算分段：告诉我视频多长，我给出每段的帧范围（不写提示词）
7. 导演台设置：已经有提示词，带你把分段、放图、声音在导演台里设好

拿不准就回复“不知道”，把视频路径发给我，我看完推荐一个。
```

编号与 SKILL.md 模式的对应：1–3 = 模式 A；4 = 模式 B（可与 1–3 组合）；5 = 模式 C；6 = 只运行 `scripts/plan_segments.py`，不读片、不写提示词；7 = 只按 `07-comfyui-wiring.md` 第 2 节带用户设导演台，不读片、不写提示词。

### 3. 选了之后：按方向拼出清单

把用户选中的方向各自的“必需”和“顺便选”合并成**一份**清单发出，去掉重复项。每个选择题都给默认值，用户不选就用默认。

| 方向 | 必需 | 顺便选（默认值在前） |
|---|---|---|
| 1 换人 | 参考视频的完整路径；角色图的完整路径（脸要清楚，多视图拼图可以） | 声音：保留原声 / 静音 / 另配 |
| 2 换装 | 服装或造型图的完整路径；说明取哪些部分（例如“只要外套”） | 换装时机：全程就是新衣服 / 原片里有换装过程，照原片换 |
| 3 换场景 | 场景图的完整路径，或一两句场景描述 | 换的时机：全程 / 从某一秒开始 |
| 4 电影化重拍 | 参考视频的完整路径；想要的风格（一句话或一张参考图） | 机位和运镜：照原片 / 允许按新风格调整 |
| 5 参考静帧 | 要几张、分别是什么（场景图、某个瞬间的关键帧）；用在哪一段 | 生图模型：支持负向提示词 / 不支持（如即梦、豆包），决定排除语怎么写 |
| 6 只算分段 | 视频时长（秒）或总帧数 | 想知道落在哪段的事件时刻（秒），可不填 |
| 7 导演台设置 | 之前这个插件给出的导演台设置表；没有就给视频时长和每段要放的图 | 声音：保留原声 / 静音 |

清单里不提分段帧数和导演台设置：默认按 107 帧 / 重叠 39 帧，用户主动说要 90/5 才改；导演台的设置统一放在交付的最后。

清单的样子（以“1+2”为例）：

```text
好，做「1 换人 + 2 换装」。请发给我：

必需
- 参考视频：完整路径
- 角色图：完整路径（脸要清楚）
- 服装图：完整路径，并说一下要取哪些部分

顺便选（不选就用默认）
1. 声音：A 保留原声（默认）  B 静音  C 另配
2. 换装时机：A 全程就是新衣服（默认）  B 原片里有换装过程，照原片换

可以一次全发，例如：“视频 D:\素材\dance.mp4，角色 D:\素材\girl.png，服装 D:\素材\coat.png 只要外套，1A 2A”。
文件路径在资源管理器里右键“复制为路径”就能拿到。
```

### 4. 首次回复里的提问格式

读完片还有拿不准的地方时，在首次回复的末尾这样问（触发条件见 `01-intake.md` 第 5 节问答键）：

- 每题编号，选项用字母，**推荐项放第一个并标“（推荐）”**，最后一项是“其他：直接写”。
- 每题后面用一句话写依据，例如“3.2 秒左手被身体挡住，看不出有没有拿东西”。
- 一次最多 4 题，只问会改变结果的。
- 让用户一行回复，例如“1A 2C”。没回答的题按推荐项处理，并在下一条回复里说明用了哪个。

```text
还有两处要你定：
1. 3.2 秒左手被挡住，看不出有没有拿东西。
   A 当作空手（推荐）  B 拿着手机  C 其他：直接写
2. 结尾 9.6 秒画面变暗，可能是转场。
   A 照原片变暗（推荐）  B 不要变暗，停在最后一个动作
回复例如“1A 2A”。
```

### 5. 交付后的下一步菜单

全部分段输出完后，最后附上：

```text
接下来可以：
1. 生成后有问题：告诉我第几段、第几秒、什么现象，我只改受影响的段
2. 换一个设定重出：例如换声音、换角色图、换风格
3. 用同一套设定做下一个视频
4. 导演台怎么设：一步步带你把这几段设好（第一次用建议选）
```

用户回复“1”却没说细节时，追问“第几段、第几秒、看到了什么”，不要猜。

---

<!-- references/01-intake.md -->
## 01 · 接收素材、读片与首次回复

### 1. 适用范围与前提

- 用户提供参考图片和参考视频。图片定义人物、服装、道具、场景或风格；视频定义这一期的首帧、动作、分镜、节奏、表情和运镜。用户明确指定的替换项优先。
- 总时长与内容每期重新读取。不得继承上一期的段数、固定时长、鼠标、鞋袜、猫耳、尾巴、灰色网格、脸红或收尾动作。
- 首帧姿态、身体朝向、人物画面位置和摄像机来自视频；身份与明确指定的外观来自图片。多视图图片里的不同视角表示同一个角色，不代表多人或分屏。
- 看不见的部位、遮挡后的动作、未展示的服装背面不凭空补全。不能观看或解码视频时，说明限制并索取可用素材，不按文件名或旧案例编时间轴。
- 默认忠实复刻可观察的内容：不为生成方便新增准备动作、减掉事件、改换镜头或重排时间。素材确有冲突时先指出并确认；技术补帧放在原片终点之后，并标明需要裁除。

### 2. 输入清单

| # | 项目 | 记什么 |
|---|---|---|
| 1 | 参考视频 | 文件名、实际时长 T、原始帧率（是否可变帧率）、尺寸、首尾画面、音频情况。可变帧率按展示时间戳分析。生成时基是节点的 24fps，不能拿源视频 fps 直接算重叠。 |
| 2 | 角色参考图 | 身份锚点：脸、发型、比例、初始服装、可辨认部件。可单图或多视图。图片不能自动覆盖视频里的姿态与构图。 |
| 3 | 服装/变化目标图（可选） | 仅当用户要求替换，或原片确有状态变化时使用。逐项说明取用与排除范围，不自动排除或保留鞋、腿、配饰，以本期要求为准。 |
| 4 | 场景/道具/风格/关键帧图（可选） | 说明各自作用和参与区间。场景图放在确实需要它的那一段，不固定只接最后一段。 |
| 5 | 当前工作流配置 | 时间框范围、分段图片/音频分配、视频用途、视频原声、二采设置。常规参数已知（见 SKILL.md 配置块）就不反复问。 |
| 6 | 用户修改说明 | 人物、服装、场景、画风、声音、表情等哪些要改。没要求改的可观察动作与镜头按视频保留。 |

**稳定别名**：先给原始素材起全片稳定的别名（“角色初始图 A”“目标造型图 B”“场景图 C”），再为每一段按实际分配顺序映射本段局部的 `<Picture 1>`…。别名全片稳定，局部编号可随分段变化。

### 3. 读片方法

1. 读取时长、帧率、尺寸与时间戳。先看第一帧和紧随的画面，再覆盖全片检查镜头、动作与表情变化。
2. 关键事件、切镜和接缝附近（尤其是每个重叠区）加密查看。抽样检查就如实称为抽样，不声称逐帧看完。
3. 用 `cinematic-layer.md` 第 2 节的读片会模板做记录，落到 S10（镜头表）、S11（事件表）、S08（情绪线）、S16（风格与光色）。
4. 建立原片分镜与事件时间轴：所有真实切镜、事件时刻、动作轨迹、情绪进程、摄像机运动、物件状态、结尾。**尚不能确定的地方标明，不把猜测写成事实。**
5. 区分“原片镜头”和“GEN 分段”，不要混称“第几个镜头”和“第几段”。

#### 读片命令（Windows / PowerShell）

ffmpeg 不在 PATH 里，用 Codex 自带的（本机路径，换机器时改这两行）。抽出的图片放进新建的临时目录，不要写进素材目录。

```powershell
$ff  = 'C:\Users\Administrator\.codex\tools\bin\ffmpeg.exe'
$fp  = 'C:\Users\Administrator\.codex\tools\bin\ffprobe.exe'
$src = '参考视频的完整路径'
$out = '新建的临时目录'

# 1. 时长、帧率、分辨率、有无音轨
& $fp -v error -show_entries 'format=duration:stream=codec_type,width,height,r_frame_rate,avg_frame_rate' -of json $src

# 2. 首帧
& $ff -v error -i $src -frames:v 1 "$out\first.png"

# 3. 全片接触表：每秒 2 张，每张表 4×3 格
& $ff -v error -i $src -vf 'fps=2,scale=320:-2,tile=4x3' "$out\sheet_%02d.png"

# 4. 找真实切镜：输出的每个 pts_time 是一个候选切镜时刻（秒）
& $ff -hide_banner -i $src -vf "select='gt(scene,0.3)',showinfo" -an -f null - 2>&1 | ForEach-Object { "$_" } | Select-String 'pts_time:([0-9.]+)' | ForEach-Object { $_.Matches[0].Groups[1].Value }

# 5. 某段时间加密抽帧：从 1.0 秒起取 1.0 秒，每秒 12 张
& $ff -v error -ss 1.0 -i $src -t 1.0 -vf 'fps=12' "$out\t_%03d.png"
```

怎么读：

- 第 1 条：`r_frame_rate` 与 `avg_frame_rate` 不一致时可能是可变帧率，按展示时间戳分析。`codec_type` 里没有 `audio` 就是无音轨。
- 第 3 条：第 s 张表（从 1 数）的第 c 格（从 0 数，先左右后上下）约在 `((s−1)×12 + c) ÷ 2` 秒。
- 第 4 条：阈值 0.3 漏掉切镜就调低，误报就调高；结果只是候选，仍要对照画面确认。
- 第 5 条：第 k 张（从 001 数）约在 `起点 + (k−1) ÷ 12` 秒。用于每个切镜前后各 0.5 秒、每个重叠区（全局时间来自 `plan_segments.py` 的分段表）、关键动作前后。
- 汇报时如实写“每秒 2 张抽样，切镜、接缝和关键动作附近每秒 12 张”，不写“逐帧看完”。
- 没有 ffmpeg 时，可用 ComfyUI 内嵌 Python（`F:\soda comfyui\ComfyUI_windows_portable\python_embeded\python.exe`，带 `cv2` 和 `av`）读帧率、帧数并按时间取帧；可变帧率素材用 cv2 读出的时长不可靠。

### 4. 首次回复（必须先于任何提示词）

收到素材后先主动回复：读到了什么、保留什么、替换什么、怎么分段、哪些地方还不能确定。用普通语言写给用户，按当前素材填入，不得把示例当成当期观察结果：

```text
我已查看这次的参考图与参考视频。视频时长为【实际时长】，原片有【已核实镜头数/检查范围】。

这期内容按原视频是：
【按原片时间顺序描述开场、动作、表情、运镜和结尾；不限制段数或桥段数】。

参考关系：
【人物/服装/场景分别来自哪张图；视频中哪些内容保留；哪些按你的要求替换】。

生成安排：
预计分【N】段，每段约 4.5 秒，相邻两段有约 1.6 秒重叠（同一个动作，节点会自动去重）。
各段范围、放图和声音设置放在提示词之后的“导演台设置表”里。

【仅在有缺项时】还需要明确：【具体问题及读图/读视频依据】。
【资料完整时】下面按这个时间轴生成各段英文提示词。
```

- 分段数字一律来自 `scripts/plan_segments.py`，不要心算（见 `03-timeline.md`）。
- 缺项会影响执行 → 提问并等待回答；资料完整、没有实质歧义 → 同一条回复里先给方案，再接着给全部分段提示词，不额外要求一句“确认”。
- 用户已经明确的信息直接沿用，不重复询问。

### 5. 问答键（按本期触发，不强制全问）

能从视频、图片和用户指示确定的先给初判，只问不确定项。需要选项时推荐项放前面，“自定义”用来接收实际要求。

| 键 | 触发条件与确认内容 |
|---|---|
| Q0 | 开场：首帧姿态、构图，以及原片是否有建模过程。只有存在冲突/遮挡才问，不默认青色线框。 |
| Q1 | 物件变化：原片具体改变哪些物件、什么顺序；是否按用户要求替换。没有变化不问。 |
| Q1a | 腿部/鞋袜确实参与事件：逐侧初判类型、材质、覆盖范围、不可见处；不确定才确认。 |
| Q1b | 原片的脱除路径无法直接用于替换物件：提出画外、可见路径等处理差异；未经用户授权不改原片运镜。 |
| Q1d | 原片物件在新角色图中不存在等实质冲突：先说明，再问保留事件还是授权改编；不默认删除整个生成段。 |
| Q1e | 变化后的观察/展示动作：以原片为准，不自动添加抬脚、摸腿或特写。 |
| Q2 | 原片有沿轨迹生成的物件：保留原物还是用户指定替换。 |
| Q3 | 原片有点选生成/替换：物件、位置、数量与原有部件的关系。 |
| Q3b | 事件瞬间的表情与转变：默认逐项复刻；看不清或用户要求改变时再问。 |
| Q3c | 桥段收尾动作：直接读原片，不默认比心、wink 或 pout。 |
| Q4 | 全片情绪：默认原片，不默认害羞/脸红；用户修改情绪时，确认只改表情还是连身体反应一起改。 |
| Q5 | 原片结尾及是否保留：默认原样结束，不强制三个动作加定格。 |
| Q6 | 场景来源、何时出现/变化、是否用场景图；不按角色属性擅自推荐新剧情。 |
| Q7 | 音频：依据已知要求和开关说明保留原声、静音或另配；未指定且会影响交付时才问。 |
| Q8（新增） | 模式：用户是否同时要求改风格/光影/镜头语言（模式 B），或需要先做参考静帧（模式 C）。从措辞能判断就不问；判断不了就出 `00-menu.md` 的开场菜单。 |

真正发给用户的问题，一律用 `00-menu.md` 第 4 节的选择题格式。

---

<!-- references/02-slots.md -->
## 02 · 槽位

槽位只能来自当前素材、用户要求和实际节点。没有对应事件的槽位留空，不编造。

| 槽位 | 填什么 |
|---|---|
| S00 | 段数 N、生成 fps=24、目标保留帧数 F、常规长度 L、常规重叠 O、末段实际长度、输出末帧 E、尾部待裁帧数 P。**来自 `plan_segments.py`。** |
| S01 | 身份锚点、图像来源、不可改变的角色特征。本期会被替换的部件不要同时定义为“永不改变”。 |
| S01a | 原片首帧成立的姿态、位置、朝向、手位、表情、构图和正在进行的动作。只有原片存在建模时才填建模过程。 |
| S02 | 当前与目标服装/状态、变化时刻、来源。没有换装填“保持”，不编造内层或目标图。 |
| S03 | 光标/操作者的外观、数量、位置、轨迹；原片没有就不建立光标主体。 |
| S04 | 每个被改变物件的前态、触发者、接触点、路径、后态、在场范围。可用于衣物或其他道具。 |
| S05 | 鞋/硬壳物件（仅有关时）：侧别、顺序、结构、动作路径。左右不固定先左后右。 |
| S05a | 腿部状态逐侧记录及时间变化；无该事件留空，不把被服装遮挡的部位宣称为裸露。 |
| S05b | 适用的动作呈现策略；只来自原片或用户授权的调整，不自动遮挡/切镜来掩盖动作。 |
| S05d | 原片实际的观察/展示动作：主体侧别、持续时间、幅度、次数；无则留空。 |
| S06 | 沿轨迹生成的部件 A：物件、根部、路径、数量、材质、效果、时间。仅用于物件，不再当情绪槽位。 |
| S07 / S07a / S07b | 点选生成部件 B / 实际生成位置 / 原片后续动作；无则留空。 |
| S08 | **独立情绪时间轴**：事件前表情、触发时间、第一反应、转向、强度、眼神与身体载体、消退/持续时间。所有情绪引用只指向本槽位。 |
| S09 | 场景与结尾：来源、布局、变化时刻、灯光、原片最后状态。没有建模就不调用建模规则。 |
| S10 | 原片镜头表：全局镜号、起止时间、景别、构图、**机位高度/角度、焦段感、主体占比（尽量用百分比）、运镜方向与速度**、切镜方式、主体与物件状态。 |
| S11 | 事件表：全局起止、动作阶段（刚发生/进行中）、触发关系、数量、侧别、接触、**视线落点**、表情；附观察依据和不确定项。 |
| S12 | 分段表：每段 [startFrame,endFrame)、长度、重叠、新增区间、覆盖的原片镜头、局部时间映射。 |
| S13 | 逐段素材表：原始文件别名 → 实际局部 Picture/Video/Audio 编号、取用属性、排除属性、使用时间。 |
| S14 | 交接表：上一段最后 O 帧与下一段前 O 帧的同一运动过程，含人物、物件、表情、相机、环境、声音。 |
| S15 | 实际视频用途、视频原声/音频锁定、二采、最终裁剪要求。提示词不得与设置相反。 |
| S16（新增） | 风格与光色：画风、主导色（≤5 种）、光源（数量/方向/软硬/色温）、空气感、材质处理。模式 A 为原片观察值，模式 B 为用户授权的改写目标。 |

### 主体编号

- `<Subject N>` 在全片内保持身份稳定。默认按首次出现顺序编号：Subject 1 为主角，其余按需要定义。
- 使用 `phrases/cursor-edit.md` 时沿用它的约定（1 角色、3 光标、5 角色部件、7 腿部、8/9 生成物）。
- 不存在的主体不强行创建。每段只引用本段有定义的主体和实际分配的媒体。
- 图片的局部 `<Picture N>` 会随分段重新编号，Subject 编号不因此改动。

---

<!-- references/03-timeline.md -->
## 03 · 分镜、分段与重叠（唯一的时间依据）

**先跑脚本，再写文字。** 分段数、每段范围、补尾和事件的局部时间一律由 `scripts/plan_segments.py` 给出，不要心算 ceil 和取整：

```bash
python scripts/plan_segments.py --seconds 10 --events 2.9,5.7
python scripts/plan_segments.py --frames 240
python scripts/plan_segments.py --seconds 10 --length 90 --overlap 5   # 旧配置
```

脚本会校验：长度为 5+17n、接缝合法、窗口无空白且向前推进、新增帧之和等于 E、不超过 64 段。输出表格直接对应 S00 / S12。

### 1. 原片时间轴与生成时间轴分开

- **原片分镜**：以真实切镜为边界，保留数量、时点和镜头运动。没有切镜，动作变化也不新建 Shot。
- **生成分段**：以节点合法帧数为边界，可以跨原片镜头，也可以把一个长镜头分到多个 GEN。
- 原片事件在全局 t 秒发生，在第 i 段的局部时间为 `t − startFrame_i / 24`。同一事件落进两段重叠区时，两处描述**同一次**事件，不产生第二次动作。
- 时间码可以显示到毫秒，底层一律保留整数帧与精确分数。不得每段把 4.458 四舍五入回 4.5 再累计。
- 24fps 表示不了的原始切镜时刻映射到最近的输出帧，并说明存在帧级量化；不声称不同帧率能逐帧一一相等。

### 2. 常规参数（当前配置，换配置只改这一处）

| 参数 | 值与含义 |
|---|---|
| 输出时基 | 24fps，与已核对节点一致。 |
| 用户单段上限 | 4.5 秒。108 帧不在合法长度网格内。注意这是用户给的上限，不是节点上限（节点允许到 3592 帧）。 |
| 合法片段长度 | `5 + 17n`：5、22、39、56、73、90、**107**、… |
| 常规长度 L | 107 帧 = 4.458333 秒。 |
| 常规重叠 O | 39 帧 = 1.625 秒。36 帧（1.5 秒）不是合法重叠。 |
| 常规步长 D | L − O = 68 帧 = 2.833333 秒。 |
| 合法接缝 | 0、1、5、22、39、56…。0 表示独立生成，不保留自动 Latent 续接。 |
| 段数上限 | 64 段。 |

39 帧是已确认配置的默认值，不是所有工作流固有的常数。用户换了节点或配置，就读取实际合法帧数后重算，不要拿旧秒数硬套。常规段**包含**重叠，不是在 107 帧之外再加 39 帧。

旧配置（90 帧 / 重叠 5 帧 / 步长 85）仍可用脚本的 `--length 90 --overlap 5` 复现。

### 3. 段数与尾段

设有效时长 T 秒，默认保留到原片终点：`F = ceil(T × 24)`。用精确分数算，避免浮点把整数帧多算一帧；用户指定了准确输出帧数则以其为准。

```text
F <= L 时：N = 1
F >  L 时：N = 1 + ceil((F - L) / D)

startFrame_i = (i - 1) * D                       # i 从 1 开始
前 N-1 段 length_i = L
tail_required = F - startFrame_N
length_N = 5 + 17 * max(0, ceil((tail_required - 5) / 17))
endFrame_i = startFrame_i + length_i
E = endFrame_N        # 输出末帧
P = E - F             # 尾部待裁帧数
```

- 区间一律左闭右开 `[start,end)`，长度即 end − start。
- 保证：每段 ≤ L，多段时末段长度 > O，相邻窗口向前推进且无空白；末段可能短于常规段。
- 原片不足一常规段时只生成一段，不加重叠。极短素材按合法最短长度补尾后裁剪，不拉长原有动作。
- 原片终点落在末段中间时，后面 P 帧是技术补尾：保持已有状态和运动自然延续，**不发明新事件**；提示词写明补尾的局部范围，输出说明写明最终保留 F 帧。
- **提示词不能执行裁剪。** 时间框路径最终输出 E 帧（最后一个 GEN 的结束帧），不会自己知道原片目标 F。P > 0 时必须另有实际裁剪步骤，裁掉合并后的最后 P 帧及对应声音；没有实际步骤就标“待裁”，不能报告已得到精确时长。
- 不能为了省掉补尾而删原片最后的动作，也不能把动作等比压缩到合法长度。
- 超过 64 段（该配置最多覆盖 4391 帧，约 182.958 秒）：先说明节点上限并制定分批续接/合并方案，不得截断视频，不得输出无法运行的第 65 段。跨批续接必须实际可用，不能假定节点会跨执行保存状态。

### 4. 重叠区怎么写

常规段末尾局部 `[68,107)`（2.833333–4.458333 秒）是下一段局部 `[0,39)`（0–1.625 秒）的**同一过程**。后续常规段的新内容从局部第 39 帧开始。

交接表（S14）要记录整个重叠区的运动轨迹与情绪进程，而不是只复制末帧姿势：

1. 人物身份、位置、朝向、手位、动作相位；
2. 服装/道具逐项状态，生成物是否已存在；
3. 操作者/光标的位置、轨迹、是否在场；
4. 视线、表情、情绪强度和正在发生的转变；
5. 相机景别、位置、运动方向/速度，以及区间内的真实切镜；
6. 背景、光照、特效及其变化；
7. 已启用声音的当前进度。

重叠区有真实切镜时，在两段中对齐复现，不为迎合“一个 Guide 镜头”抹掉原片剪切。原片在动就连续动，不默认定格，也不默认把动作延后到重叠结束。新事件若已发生在重叠区，下一段只描述它原有的发生过程，不再执行一次。

### 5. 计算示例（仅示例，不得写进每一期剧情）

原片恰好 10 秒，F = 240（脚本：`--seconds 10`）：

| GEN | 全局帧 | 全局秒 | 长度 | 开头重叠 | 新增 |
|---|---|---|---|---|---|
| 1 | [0,107) | 0–4.458333 | 107 | 0 | 107 |
| 2 | [68,175) | 2.833333–7.291667 | 107 | 39 | 68 |
| 3 | [136,243) | 5.666667–10.125 | 107 | 39 | 68 |

先合并成 243 帧，再裁掉末尾 3 帧，保留 240 帧。不能把原片 10 秒写成三段共 13.375 秒，也不能把这个三段例子固定到下一期。

---

<!-- references/04-grammar.md -->
## 04 · 镜头与动作语法

具体值一律以当前视频为准。

1. **镜头来自原片。** 不固定长全景、近景次数、环绕角度、静止机位或“相机前 1/3 到位”。景别、取景范围、切镜和运镜按原片记录。
2. **因果明确。** 施动者、接触点、目标、运动路径和状态变化写清。确由光标控制才用光标作主语；角色主动动作、重力或其他外力不得硬改成光标操作。
3. **视线与反应对应。** 事件引起的反应按 S08 的实际时点开始：原片同步就同步，有延迟就保留延迟，不强制所有反应同帧。
4. **情绪是一条连续状态线。** 从原片读出，用眉、眼、嘴、头肩和手部动作落地；不默认脸红、捂胸、害羞、妩媚。第二次操作是否减弱反应由原片决定。
5. **动作数量与可见过程准确。** 记录可核实的次数、顺序、侧别、方向、接触、幅度和停留。不擅自把一次改三次；不为数值化而编造厘米/角度，无法测量时用有依据的画面相对描述。
6. **时间预算容纳动作。** 重复动作的次数/频率加上停留、准备、回落，必须落在观察到的区间内；不把“每秒一次共三次”塞进 1.8 秒。动作跨段时延续相位，不加速完成。
7. **物件状态连续。** 出现、消失、替换和遮挡按原片。生成物可以被身体正常遮挡，不用“永不隐藏”逼模型透视显示。没有新事件就不凭空复原。
8. **左右定义清晰。** 画面左右与解剖左右分别说明，不把 screen-left 自动当成人物左侧。原片镜像或方向不明时先核实。
9. **运动锁定只用于不动的部分。** 脚抬起时不同时写双脚钉地；相机移动时不写全段静止；光照确实在变化时不写曝光/背景绝对不变。
10. **防崩规则条件启用。** 单光标、重复事件排他、逐腿不对称、覆盖时间线、粒子和场景退场等，只在当前视频确实需要时调用。没有粒子不强制加粒子，没有原位幻化不编造幻化。
11. **配乐、声音和对白独立核实。** 原片无声/用户静音时据实际开关写静音；保留原声时不再默认写 `No words and no music`。不为每个动作发明音效。

### 写“相位”，不写“姿势”

事件描述写成“刚发生 / 正在进行 / 即将发生”，而不是静态状态（“站着”“拿着”）。这在三个位置最有用：

- **首帧**：写成原片首帧已经成立的姿态加正在进行的动作，不从图片站姿过渡，不补准备动作。
- **段尾**：写最后一个重叠区内的动作相位、速度和下一步走向，而不是一个定格姿势。
- **段首**：写与上一段同一次运动的延续，不重置姿态，不先停住。

“前一秒”式的蓄势停顿只在原片本来就是蓄势或停顿时保留；不得为了美感把原片已经发生的碰撞改成蓄势。

### 复刻时容易出的错

| 错误 | 正确 |
|---|---|
| 沿用上一期的段数、时长、物件 | 每期重新读取 |
| 按图片站姿写首帧 | 按视频首帧 |
| 为“更稳”减掉事件或加准备动作 | 事件、顺序、速度不变 |
| 把重叠区写成新剧情容量 | 重叠区是同一次过程，新内容从局部第 39 帧起 |
| 每个反应都和事件同帧 | 按原片的实际延迟 |
| 模板句里的颜色/侧别/次数原样照抄 | 与当前原片逐项核对后再用 |

---

<!-- references/05-assembly-output.md -->
## 05 · 组装与输出格式

填完槽位（02）→ 算完分段（03）→ 按本表逐镜组装 → 跑自检（06）→ 输出完整分段。不要把原案例的固定镜数和 R 调用链复制到新的参考视频。R 句在 `phrases/core.md`（通用）和 `phrases/cursor-edit.md`（光标/换装/生成/建模，仅原片存在时读取）。

### 1. 逐镜组装表

| 当前内容 | 组装顺序与条件 |
|---|---|
| 首段首镜 | 风格/场景与人物定义 → R06 首帧状态 → 原片动作与视线/情绪。只有原片有建模时才选 R53 及适用变体。 |
| 后续段开头 | R29 同一重叠过程 → R67 相位不重置 → 按原片继续。已有动作继续，不先停住。 |
| 普通动作 | S11 时间与动作 → 明确主体/接触/方向/过程 → S08 表情与视线 → 结束状态。 |
| 原片光标交互 | S03 数量与轨迹 → R60/R61 实际接触 → 对应物件动作 → R20/R72 视线与反应 → R46 可见性。移动与状态变化分开写。 |
| 原片外层拖除 | R15/R16（仅内层确实已在时）→ R11/R12/R13 中与原片相符者 → R14；不自动新增脸红与遮挡动作。 |
| 鞋/硬件移除 | R17 实际顺序 → R18 或 R52 → R62 身体响应 → 更新逐件状态；不同时钉住正在抬起的脚。 |
| 织物变化 | R50（仅不对称）→ R19 或 R51 → R41 覆盖 → 适用的 R42/43/44/45 策略 → 实际反应。策略不得改变原片，除非用户已授权。R44 抬脚时不套双脚静止。 |
| 原片观察/展示 | 适用的 R21/R68/R69/R70/R71 → S08 → R75 实际时长；没有对应动作不调用。 |
| 原片沿轨迹生成 | R23 或 R23b → 原片确有特效才加 R23c → R24 → R25；运镜按原片，不默认配 R22。 |
| 原片点选生成 | R26 或 R26b → 实际取景/光标可见性 → 原片确有特效才加 R26c → R47 → R59；不强制近景、不强制移到脸。 |
| 原片环境建模 | R63/R63b → R64/R65 与 R74 中符合原片者；普通场景转换不套线框建模。 |
| 原片环顾 | R48/R48b/R48c 的实际目标、次数、幅度与身体关系；不强加 20–30 度或固定扫描次数。 |
| 真实切镜 | 新 Shot 与段内时间戳 → 新构图 → R27 状态继承 → 本镜原片内容。 |
| 非最终段尾 | R28 记录最后重叠区的全过程，并生成 S14；不额外增加停顿或强制半秒定格。 |
| 最终段尾 | R39 原片真实结束 → 如有技术补尾，区分补尾区间并说明待裁帧数；不新增收尾表演。 |

### 2. 输出格式：提示词在前，导演台设置在后

用户要的是提示词。导演台的设置统一放到最后一张表里，不夹在每段中间。顺序：

1. 一句话回顾方案：分几段、每段约几秒。
2. 逐段提示词：每段一个小标题，紧跟一个独立代码块，代码块里只有本段完整六字段英文提示词。

````text
### GEN 2 · 原片 2.833–7.292 秒
```
subject_definitions:
...
non_diegetic_music:
...
```
````

3. 最后一节“导演台设置表”，每段一行，数字来自 `plan_segments.py`：

| GEN | 选区起点（秒） | 生成时长（秒 / 帧） | 放图顺序 | 参考视频 | 声音 |
|---|---|---|---|---|---|
| 1 | 0 | 4.458 / 107 | P1 = 角色图 A（取脸、发型、服装；不取旧鞋） | 原片 0–4.458 秒，可编辑参考 | 保留原声 |

   表下写两句：开头重叠由节点自动去重，不用手动裁接缝；末段有补尾帧时写“合并后保留 F 帧，裁掉末尾 P 帧及对应声音”，没有实际裁剪步骤就标“待裁”。

4. 00 第 5 节的下一步菜单。用户选“导演台怎么设”或开场就选了菜单 7，按 07 第 2 节一步步带。

规则：

- 放图顺序要写清 Picture 编号对应哪张图、取用和排除什么。这是提示词里的 `<Picture N>` 能对上图的前提，不能省。
- 设置、放图、裁剪写在代码块**外**，不让用户把它们当成六字段正文粘贴。
- 每段一个独立完整的代码块，不只给摘要或差异。用户可直接复制到本段提示词框。
- 默认英文提示词、中文说明。用户明确要求中文时只切换正文语言，字段名与标签仍用英文。对白、歌词、画面文字按需保留原语言。
- 逐段输入框不需要分隔符。只有用户要求支持批量解析的入口时，才另提供 `--- SEGMENT ---` 格式，且不得取代逐段放图说明。

### 3. 六字段（顺序固定）

```text
subject_definitions:
[Actual subjects and the references assigned to this segment; calibrate inherited identity without reintroducing a new person.]

summary:
[Actual task types] [This segment's source-aligned action chain and replacement scope.]

retention_analysis:
[Actual reference relationships, preserving motion, expression and camera structure as requested while replacing only specified attributes.]

detailed_description:
[Current style and environment.]
[Shot 1] [Actual opening state; for later segments, describe the same carried overlap and then the source-aligned continuation.]
[Shot 2] At [local cut time], [Only if the source actually cuts.]

overall_soundscape:
[Verified audio plan matching the workflow settings.]

non_diegetic_music:
[Actual music treatment; N/A only when applicable.]
```

- `subject_definitions` 与 `detailed_description` 优先使用明确的 Subject 标签，避免代词歧义；不为满足机械的词数检查而破坏用户原语言的对白。
- 段内时间戳从本段 0 秒开始，**长度包含开头重叠区**。
- 只在真实切镜处新建 Shot；区间跨段不制造切镜；原片已有的切镜不删。
- 方括号只用于说明模板，正式结果不得留下；任何槽位都必须填完；内部 Q/S/R 编号、占位符、文件接线说明、裁剪指令不得出现在英文提示词里。
- 不设固定字符数；保持足够的动作细节，删掉重复约束和不适用的段落，不为凑字数堆砌。

### 4. Ref2VA 保留标记

- 视觉：`fully_preserved` / `partially_preserved` / `attribute_transfer` / `weak_reference`；音频：`fully_copy` / `partially_copy` / `reference` / `weak_reference`。
- 按实际取用的属性写清楚。不能因为换了人物就把动作也降成弱参考；忠实复刻不写成只保留概念的 `weak_reference`。
- 使用参考视频编辑时说明其编辑源关系；只取动作结构时说明 reference generation；后续段可说明 video continuation，但**不虚构新的媒体编号**（内部 Latent 不占 Picture/Video 编号）。

### 5. 排除句与硬约束镜像

六字段里没有负向字段。约束写成正向锁定句；用户的每条“不出现 / 不可见”的硬设定，在 `detailed_description` 末尾补一句对应的排除句。通用做法和镜像表见 `cinematic-layer.md` 第 6 节。

---

<!-- references/06-checklist.md -->
## 06 · 自检清单与问题定位

### 1. 输出前逐条自检

**流程**

- [ ] 已先向用户说明当前视频流程与分段方案；必要缺项已问，已有指示没有被重复询问。
- [ ] 确实读取了当前素材；没有沿用旧案例的人物、场景、动作、时长或镜头。分析范围如实说明（抽样就说抽样）。
- [ ] 尚不能确定的内容已标明，没有把猜测写成事实。

**时间与分段**（先对照脚本输出）

- [ ] 所有生成段 ≤ 107 帧，长度满足 5+17n；常规接缝 39 帧；首段起点 0；后续窗口无空白、向前推进；重叠小于相邻两段长度。
- [ ] N、每段 start/end/length、重叠、新增帧、F/E/P 相互一致；短尾段的提示词没有仍写 107 帧。
- [ ] 原片时间、输出全局帧、段内局部时间明确区分；时间戳在段内且不超长；重叠不是新增剧情容量。
- [ ] 重叠两处描述的是同一动作、同一表情进程：没有动作重启、重复点击、重复台词、突然回到中性脸。
- [ ] 原片镜头与 GEN 区分；只在真实切镜时新建 Shot；跨段区间不制造切镜；原片已有的切镜没被删。
- [ ] P > 0 已明确需要另行裁剪（同时裁音频）；未执行的裁剪没有说成已完成。

**内容**

- [ ] 首帧来自视频的当时姿态，不从图片站姿过渡；动作时间轴覆盖原片首尾，不删事件、不补准备/复位。
- [ ] 每个施动者、接触点、视线与反应合理；没有“脚抬起”与“双脚全程钉地”之类的矛盾。
- [ ] 左右、物件数量、服装前后态、遮挡、生成物持续性一致；不存在的物件没有被硬塞进模板。
- [ ] S08 是情绪的唯一来源；段间保留情绪，原片有表情变化时允许按时间变化。
- [ ] 模板句里写死的颜色、侧别、次数、时长都已与当前原片核对。

**素材与设置**

- [ ] 每段素材表完整：每张图的别名/文件名、局部编号、取用范围；提示词里每个引用都能在该段分配里找到。
- [ ] 内部 Latent 没占用媒体编号，没有写成虚构的 `<Video 2>`；视频参考按该段实际交集说明。
- [ ] 图像与视频的保留关系具体：身份/服装/背景谁提供，动作/表情/镜头谁提供。
- [ ] 视频原声、音频锁定与提示词一致；二采和采样参数属于设置，不写成剧情，也不能被提示词覆盖。

**格式**

- [ ] 六字段齐全，顺序为 `subject_definitions` / `summary` / `retention_analysis` / `detailed_description` / `overall_soundscape` / `non_diegetic_music`。
- [ ] 每段一个独立完整的代码块；放图、参考视频、声音、裁剪写在文末导演台设置表，每段一行。
- [ ] 没有 R/S/Q 编号、占位符、接线说明、裁剪指令混进英文提示词；默认英文提示词，中文仅用于说明。
- [ ] 没有无内容的质量标签（8K、4K、masterpiece、best quality、ultra detailed、hyper detailed、HDR、epic、stunning、breathtaking、award winning、trending on artstation、sharp focus、insane detail、high resolution）。
- [ ] 用户的每条“不出现/不可见”硬设定都有对应的排除句。

### 2. 用户反馈问题时：先定位，再最小修改

按症状定位，只重写受影响的那一块，再贴出受影响分段的**完整**六字段。改动交接区时同步更新相邻段对同一重叠内容的描述；时间框有变化就重新跑脚本，别让旧时间轴留在别的段里。

| 症状 | 先查哪里 |
|---|---|
| 重叠区动作重复 / 重启 | S14 交接表；相邻两段是否描述了同一次过程（R29、R67）；事件是否被写成了两次 |
| 段首表情突然回到中性 | S08 是否覆盖重叠区；R09 / R11b；段首是否写了表情进程 |
| 物件在段间凭空出现或消失 | S04 状态表；R59；目标图是否过早出现在前段 |
| 人脸 / 服装漂移 | 该段 Picture 分配与 retention_analysis 的取用范围；身份校准图是否排除了旧服装 |
| 镜头自己变了或被“稳住” | 是否写了固定机位但原片在动（R32）；运动锁定是否用在了会动的部分 |
| 动作变快 / 被压缩 | 时间预算（04 第 6 条）；动作跨段时是否延续了相位 |
| 左右反了 | 04 第 8 条；原片是否镜像 |
| 补尾区出现新动作 | P 区只能延续状态，不发明事件（03 第 3 节） |
| 声音与设置冲突 | S15；静音必须在设置里关，不能只写在提示词里 |
| 画面发塑料 / 过曝 / 像 CG（模式 B） | `cinematic-layer.md` 第 5 节的克制规则；是否混入了质量标签 |
| 有的段没吃到风格 | 是否有段提示词为空，导致全局提示词失效（见 07） |
| 最终时长比原片长 | 是否漏做 P 帧裁剪 |

---

<!-- references/07-comfyui-wiring.md -->
## 07 · ComfyUI 接线与连续生成（Timeline Director 时间框模式）

主链：**MiniMax H3 素材规划台「分段规划」→ MiniMax H3 有限分段采样「有限分段规划」→ 合并画面/合并音频 → CreateVideo（24fps）→ SaveVideo**。

不使用旧版的 8 秒四段、手动 Load/Save Latent、context_length 22 等接线方案；不需要「有限分段展开」节点（已标为废弃兼容入口）。

**已对照本机源码核实**（ComfyUI-MiniMaxH3-TimelineDirector 0.8.0）：段长必须是 `5 + 17n` 且不超过 3592 帧；时间框段数 1–64；接缝吸附为 0、1、5、22、39、56…；自动连续性 Guide 不占 Picture/Video 编号。节点升级后以本机实际代码和保存的参数再核对一次。

### 1. 接线与设置要求

| 配置 | 执行要求 |
|---|---|
| 分段模式 | 使用 timeline 时间框；数量与 03 的计算一致，每段 startFrame/endFrame 填实际计算值。 |
| 批量入口 | 连接“分段规划”。批量生成时 Prompt Index 不接，否则只会生成当前选中的 GEN。 |
| 时长显示 | 顶部生成时长跟随当前段，尾段可以短于 4.458 秒；别把当前选中尾段的时长当成全片每段的长度。 |
| 模板默认分段 | 本机工作流模板保存的是 5 段、90 帧、重叠 5 帧，生成时长显示 3.8 秒。“更新分段”会尽量保留已有段长与合法接缝，设成 4.5 秒再点它**不保证**得到 107/39。出提示词前以分段表为准，让用户在素材规划台里把各段范围改成表里的值，再逐段粘贴提示词。 |
| 参考视频 | 人物/外观替换通常用可编辑参考（edit）。固定 Guide 会约束原画面，不默认用于替换原人物。实际用途要与提示词一致。 |
| 视频取段 | 节点按 GEN 与时间线视频的交集取参考；超出原片的补尾区不能声称仍有完整视频参考。 |
| 图片 | 共享素材库不等于每段已分配。每段按放图顺序实际分配，局部编号从 1 开始。 |
| 人物与目标图 | 按本段实际需要分配。身份校准图只取稳定身份时，明确排除旧服装；目标状态图是否参与前段要防止目标提前出现。不强制全片固定两图，也不宣称 Latent 必然完全替代身份参考。 |
| 场景图 | 只在本段需要场景锚定时分配，不固定放末段。没有图片就明确该段图片分配为空，并核实任务允许。 |
| 局部提示词 | 只要任意一段填了本段提示词，全局提示词就**完全不生效**，每一段都必须完整填写；不能只在全局写风格再假定局部自动继承。 |
| 连续性 | 采样器内部处理上一段 AV Latent 尾部、Drift-Control、解码和去重。重叠区取上一段对应尾部作连续性 Guide，不额外分配 Picture/Video 标签。0 帧重叠则两段独立生成。 |
| 去重 | 后一段开头的重复画面由节点去掉，保留前一段对应画面，不要再手动裁接缝。最终补尾裁剪与接缝去重是两件事。 |
| 音频 | 原声开关、独立音频、锁定策略要与要求一致。开启“视频原声”会让每段拿到对应的时间线切片并锁定，最终输出为连续原声；关闭则 AV 音频流与最终成品固定为静音。静音不能只写在提示词里。需要保留音频时核对音频编号和最终裁剪。 |
| 二采 | 沿用实际设置：总步数取 BasicScheduler 的 steps，高清步数取素材规划台的 `secondPassHighSteps`（须 ≥1 且小于总步数），低清步数 = 总步数 − 高清步数（已对照节点源码核实）。本机三个工作流：V1 为 6 / 2 / 4，V2 与逻辑修订版为 8 / 2 / 6。二采是同一片段的采样阶段，不产生额外片段/时长，不把高低清各算一段。 |
| 种子 | 同一次有限分段采样内部各段使用同一个 seed；界面 randomize 影响下一次执行，不代表同次每段随机换种。 |
| 输出长度 | 时间框路径的输出是最后一个 GEN 的 endFrame。要回到原片 F 帧，必须落实额外尾裁，不能只在文字里写“自动删除补尾”。 |

### 2. 给用户的导演台操作步骤（菜单 7 / 下一步“导演台怎么设”）

按下面顺序带用户，数字填本期导演台设置表里的值。依据是节点前端代码：“更新分段”保留已有段的长度和接缝，只有新增的段才用当前选区时长和默认 39 帧重叠；改某段的生成时长或起点，后面的段整体顺移、各自长度和接缝不变；段数最少 1（`js/segment_windows.mjs` 的 `createWindows`、`editWindow`，`js/minimax_h3_timeline_director.js` 的 `applySegmentCount`）。**这套步骤是按代码推出来的，尚未在界面上实测，按钮名称以用户看到的为准。**

1. 双击 `E:\个人开发项目\minimaxH3\启动MiniMaxH3导演台.bat`，在工作流列表的 `MiniMaxH3` 文件夹里打开“MiniMaxH3-导演台-V2-本机版”。
2. 加入参考视频；换人时设为“可编辑参考”。
3. 先设分段范围，再放图和贴词（减少段数会清掉被删段的素材分配和提示词）：
    1. “素材分段数量”填 1，点“更新分段”。
    2. 选中 GEN1，“生成时长”填 4.5，吸附为 107 帧。
    3. “素材分段数量”填设置表的段数，点“更新分段”。新增的段都是 107 帧、重叠 39 帧。
    4. 末段短于 107 帧时，选中最后一个 GEN，把“生成时长”改成表上的秒数。
    5. 逐个 GEN 核对“选区起点”和“生成时长”与表一致。
4. 每段按“放图顺序”拖图，第一张就是 Picture 1。
5. 每段把对应代码块贴进“本段提示词”。每一段都要贴，否则全局提示词失效、漏贴的段没有提示词。
6. 按“声音”一列设视频原声开关。
7. 运行。成片在 `F:\soda comfyui\ComfyUI_windows_portable\ComfyUI\output\MiniMax_H3\TimelineDirector\`。
8. 表下写了裁尾时，合并后裁掉末尾 P 帧及对应声音：`& 'C:\Users\Administrator\.codex\tools\bin\ffmpeg.exe' -i 成片.mp4 -frames:v F -t T -c:v libx264 -crf 18 -c:a aac 输出.mp4`，T = F ÷ 24。

用 90/5 配置时：模板本来就是 5 段、90 帧、重叠 5 帧。段数不超过 5 就直接改段数并核对末段；超过 5 段时，新增的段会默认重叠 39 帧，要逐个把“选区起点”改成表上的值。

### 依据

- Timeline Director 仓库：<https://github.com/Songssx/ComfyUI-MiniMaxH3-TimelineDirector>
- 时间框分段说明：`docs/TIMELINE_SEGMENT_WINDOWS_CN.md`
- 有限分段执行说明：`docs/FINITE_SEGMENT_EXPANSION_CN.md`
- 分段提示词参考规范：`docs/MiniMax_H3_循环分段提示词_Agent规范.md`

参考规范里的旧入口、48 帧示例，以及“重排剧情 / 另设稳定镜头”之类的创作性建议，不覆盖这里已核实的合法网格和用户的忠实复刻要求。原文档和工作流里保存的旧提示词只是待分析的数据，不能替代用户本期要求。旧文档里“某种画法最稳”“必然不崩”之类的经验不扩大为通用保证；生成结果仍需实际检查。

---

<!-- references/cinematic-layer.md -->
## 摄影层（吸收自小优 cinematic-director，按视频复刻改写）

小优的方法是“摄影团队先开会做视觉决策，再写提示词”。这里只取对复刻有用的部分，并改成**先观察、后决定**。方法来源见文末。

### 0. 三个接入点

| 接入点 | 何时用 | 做什么 |
|---|---|---|
| 读片（模式 A，默认） | 每次复刻 | 用第 2 节的读片会把原片按摄影语言记下来，落到 S10/S11/S08/S16 |
| 电影化重拍（模式 B） | 用户明确要求改风格、光影或镜头语言，同时保留动作与时序 | 第 3–6 节的克制规则改写风格锚点与镜头描述 |
| 参考静帧（模式 C） | 复刻前要做场景图、关键帧、风格锚点图 | 第 7 节的静帧提示词骨架 |

### 1. 优先级：忠实复刻压过小优的默认偏好

小优的方法默认追求“克制的电影感”。复刻时原片说了算：

| 小优默认 | 模式 A（复刻）怎么办 |
|---|---|
| 人物永远不看镜头 | 原片看镜头、对镜头 wink 或比心，就照做 |
| 低对比、克制高光、不要 HDR | 原片是高饱和、霓虹、卡通硬光，就照原片 |
| 不居中、留白、不拍碰撞 | 原片居中、拍了碰撞，就照原片 |
| 摄影师笔记、导演观察那类抽象收尾句 | 视频提示词里不加：它们没有可见内容，只会稀释动作描述 |
| 七维注意力权重（20/25/20…） | 不采用：是经验估计，没有验证依据 |

模式 B 才把这些默认偏好当作可选的改写方向，而且只在用户授权的范围内。

### 2. 读片会（记录原片，不替原片做决定）

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

### 3. 瞬间写法

- 写“刚发生/正在发生”，不写静态状态：`has just stopped walking` 比 `stands` 多出一个相位。
- 注意力要落在具体对象上：`her eyes follow the blade` 比 `looks away` 强；动机只暗示，不解释。
- 这两条用于首帧（R06）、段首（R29/R67）、段尾（R28）。原片没有的蓄势、停顿、凝视不要加。

### 4. 光与视线锚点

- 光有唯一可信的来源时，先写光源，再写它照到什么；光先落在空间或注意力对象上，不一定先照脸。
- 视线落点、最亮处、观众的第一眼，如果原片里是同一个东西，就让提示词保持一致，不要三者各说各的。
- 色彩来自光和空气，不来自一堆物件各带一种颜色。主导色控制在 3–5 种。
- 深度来自空气和层次，不靠加模糊。

### 5. 模式 B：电影化重拍

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

### 6. 排除句与硬约束镜像

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

### 7. 模式 C：参考静帧提示词

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

### 8. 迭代

某一块不好，只重写那一块再重新组装，不要推翻全部：

- 构图或镜头问题 → S10 与镜头描述
- 画面像 CG → 第 5 节的克制规则与质量标签
- 角色不吸引人或脸漂 → 身份锚点（S01）与该段 Picture 分配
- 视线不对 → S11 的视线落点

### 来源与说明

- 方法来自 <https://github.com/cOkieeman/xiaoyou-aigc-cinematic-director>（fork 自 wubo0927/xiaoyou-aigc-cinematic-director，抖音“小优AIGC”）。
- 本文件是改写，不是搬运。写作时看到的仓库页面上没有 LICENSE 文件；若要把更多原文并入并公开发布，建议先征得原作者同意。
- 没有吸收的部分：编剧和分镜两个 Skill（不公开）；固定的人物原型库和题材模板（面向生图，不适用于复刻）；七维权重百分比；摄影师笔记与导演观察的固定句式（见第 1 节）。

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

实际表情按 S08，不能因框选默认疑惑。

```text
While the rectangle closes, the head tilts to one side and the eyes track the corner bracket nearest the face, the brows lift a little, the mouth presses into a small curious line, and both hands stay loose at the sides.
```

#### R74 · 场景生成时的视线与反应

按原片看向实际生成位置，表情按 S08，不自动惊喜。

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
