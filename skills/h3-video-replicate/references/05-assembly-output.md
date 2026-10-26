# 05 · 组装与输出格式

填完槽位（02）→ 算完分段（03）→ 按本表逐镜组装 → 跑自检（06）→ 输出完整分段。不要把原案例的固定镜数和 R 调用链复制到新的参考视频。R 句在 `phrases/core.md`（通用）和 `phrases/cursor-edit.md`（光标/换装/生成/建模，仅原片存在时读取）。

## 1. 逐镜组装表

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

## 2. 每段输出格式（先中文配置，再英文提示词）

先输出本期总表：段号 / 全局帧范围 / 对应原片时间 / 本段实际时长 / 重叠 / 新增内容 / 参考图片（总表来自脚本）。然后逐段：

````text
### GEN i
时长：[实际帧数] 帧 / [实际秒数] 秒；全局范围：[start,end)；本段开头重叠：[O] 帧。
本段放图（按顺序）：
  <Picture 1> = [文件名/稳定别名]；取用：[具体属性]；不取：[必要排除属性]。
  <Picture 2> = [确实需要的第二张图；没有则删此行]；取用：[具体属性]。
视频：[本段实际参考视频及全局交集范围]；用途：[可编辑参考/其他已确认模式]。
音频：[实际开关与素材配置]。
衔接：[首段无前段；后续说明与前段同一重叠过程]。
尾部裁剪：[仅末段需要时写：合并后保留 F 帧，去掉末尾 P 帧及对应音频；未执行标“待裁”]。

（紧接一个独立代码块，里面只有本段完整六字段英文提示词）
````

规则：

- 图片分配、生成范围、设置、裁剪操作写在代码块**外**，不让用户把它们当成六字段正文粘贴。
- 每段一个独立完整的代码块，不只给摘要或差异。用户可直接复制六字段到本段提示词框。
- 默认英文提示词、中文说明。用户明确要求中文时只切换正文语言，字段名与标签仍用英文。对白、歌词、画面文字按需保留原语言。
- 逐段输入框不需要分隔符。只有用户要求支持批量解析的入口时，才另提供 `--- SEGMENT ---` 格式，且不得取代逐段放图说明。

## 3. 六字段（顺序固定）

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

## 4. Ref2VA 保留标记

- 视觉：`fully_preserved` / `partially_preserved` / `attribute_transfer` / `weak_reference`；音频：`fully_copy` / `partially_copy` / `reference` / `weak_reference`。
- 按实际取用的属性写清楚。不能因为换了人物就把动作也降成弱参考；忠实复刻不写成只保留概念的 `weak_reference`。
- 使用参考视频编辑时说明其编辑源关系；只取动作结构时说明 reference generation；后续段可说明 video continuation，但**不虚构新的媒体编号**（内部 Latent 不占 Picture/Video 编号）。

## 5. 排除句与硬约束镜像

六字段里没有负向字段。约束写成正向锁定句；用户的每条“不出现 / 不可见”的硬设定，在 `detailed_description` 末尾补一句对应的排除句。通用做法和镜像表见 `cinematic-layer.md` 第 6 节。
