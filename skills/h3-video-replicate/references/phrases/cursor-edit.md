# 光标交互与物件变化句库（条件模块，R 编号沿用原稿）

**只在原片确实出现这类事件时读取**：鼠标/光标操作、外层衣物或鞋袜被移除、物件沿轨迹或点选生成/替换、线框填充开场、场景线框建模。原片没有的事件、物件与配饰不出现、不补位。

这些句子来自最初那个案例，里面有不少写死的画面内容（青色线框、浅灰背景和地面网格、粒子颜色、半秒消散、粉色脸红等）。**只有当前原片吻合时才能原样使用**，否则改写或删除。

## 主体编号沿用约定

仅在使用本模块时沿用，其余场景按首次出现顺序给主体编号，全片保持稳定：

| Subject | 含义 |
|---|---|
| 1 | 角色 |
| 3 | 光标 / 操作者 |
| 5 | 角色部件 |
| 7 | 腿部 |
| 8 / 9 | 生成物（沿轨迹生成 / 点选生成） |

不存在的主体不强行创建；每段只引用本段有定义的主体与实际分配的媒体。

## 策略互斥提醒

- R42（画外脱）、R43（同步后分侧）、R44（袜圈落地 + 抬脚）、R45（相机下摇）是四套互斥的处理策略，一次只选一套，且必须与原片一致或经用户授权。
- R44 存在抬脚时，禁止同时使用“双脚钉地”之类的静止锁定（见 R62s / R66）。
- R44 的整体环（选项 1）与两个独立环（选项 5）不能同用。

## 开场建模与线框填充

### R53 · 开场线框 + 一次填充

仅当前视频确有线框填充开场时用。图像身份和本期实际线框外观分别核对。

```text
At 00:00.000 there is no finished body yet: <Subject 1> is a cyan wireframe over a grey mannequin, only edges and construction lines, no skin, no hair colour, no garment surface and no face detail. The tip of <Subject 3> taps once on the wireframe chest, a dashed halo closes there, there is one brief flash, and the form fills in one continuous pass from the feet up to the head in under {{D}} seconds, the surfaces appearing behind the travelling fill line.
```

### R53b · 形态锁定

Picture 编号按本段分配重映射；不可脱部件仅列确实不变的部分。

```text
The wireframe is the silhouette of <Picture 1> and nothing else: when the fill is finished, <Subject 1> is exactly <Picture 1> - the same face, the same hair, the same proportions, with every {{不可脱部件}} in place - and the worn outfit is exactly {{图1 服装清单}}.
```

### R53c · 一次填充 + 无线框残留

仅当前原片是一次完整填充且没有残留时用。

```text
The fill happens once, in one pass, with no second pass and no half-filled body: no wire line, no construction line, no grey mannequin and no bare edge remains anywhere on the body after the fill, and the fill changes nothing else in frame - the background colour, the floor grid, the light direction and the exposure stay exactly as they were.
```

### R53d · 填充粒子

粒子与配色必须来自本期视频/用户指定；无粒子删此模块。

```text
The fill is not quiet: as the fill line travels up the body, small cyan particles run along the wire lines just ahead of it and settle into the surfaces behind it, and every wire edge brightens where the line passes. The particles are cyan and grey only, they are gone within half a second after the fill reaches the head, and the light grey background, the floor grid, the light direction and the exposure stay exactly as they were.
```

### R53e · 填充完成的第一反应 + 光标去向

原片第一反应与光标去向不同则相应改写；不自动恢复疑惑待机。

源句选项 1：

```text
The instant the fill reaches the head, <Subject 1> takes one breath, the eyes come onto the pointer tip and stay there, the head tilts to one side and reads it, and the mouth presses into a small puzzled line; <Subject 3> stays in frame at chest height, still, in front of <Subject 1>.
```

源句选项 2：

```text
the arrow moves away from the chest and slides back in from screen-{{SIDE}}
```

## 光标：入场、数量、可见性、选中

### R07 · 光标入场或在场移动

只在当前视频此时确有光标入场时调用；已在场就描述实际移动，不再写入场。

```text
At {{TS}}, <Subject 3> {{enters from the observed screen edge or moves from its already-established position}} along {{source trajectory}}.
```

### R35 · 光标数量

```text
<Subject 3> is the {{observed cursor appearance}}. Exactly {{observed count}} cursor is present during {{observed visibility intervals}}, following the source trajectory and interaction order.
```

### R46 · 光标可见性

```text
During {{operation interval}}, the pointer remains {{source visibility and contact relationship}} and follows {{item or stroke}}. It exits or becomes occluded only at {{observed time and cause}}, without an unexplained disappearance.
```

### R76 · 点选生成的光标在场

仅原片光标点选可见时用；遮挡、出入画与接触时长取原片。

```text
<Subject 3> is visible in every frame of this beat: its tip travels from inside the frame onto {{target_part}}, the halo closes there, there is one click, the tip stays on that spot through the flash, and it leaves only after the particle ring is gone.
```

### R10 · 选中框

仅原片有选中框；框形、选中范围、情绪与时间按实际记录。

```text
The arrow stops in front of the {{部位}} and a dashed selection box closes on it, from {{上界}} to {{下界}}; the head tilt grows a little, the eyes drop down the box, still reading it, and one shoulder lifts slightly.
```

## 外层衣物、鞋袜与织物移除

### R15 · 光标拖走外层，仅该事件适用

```text
The tip of <Subject 3> hooks {{garment}} at {{contact point}} and travels along {{observed path}}. The garment follows the tip out through {{exit edge}} as an empty garment, with {{observed motion blur}}. The removal lasts {{observed duration}}, and the pointer follows its recorded exit timing.
```

### R16 · 已有内层与表面分离

```text
Throughout this removal, {{retained outfit}} is already worn underneath and remains in place. Only {{removed garment}} separates from the body; the character and retained outfit stay continuous. {{observed hand behaviour}}.
```

### R17 · 物件先后顺序与次数

```text
{{actor}} removes {{ordered item list}} in the order {{observed order}}, each exactly {{observed count}} time. Each item retains its recorded state afterward until another specified event changes it.
```

### R18 · 鞋被带动脱除

```text
The tip of <Subject 3> takes hold of {{side and shoe}} at {{contact point}} and carries it along {{source path}}. The foot follows with {{observed lift, ankle response and landing}}, while the shoe separates according to {{observed contact and coverage sequence}}.
```

### R19 · 软织物协同脱除

```text
<Subject 3> takes hold of {{observed contact point}} and draws {{specified garment or garments}} along {{observed removal path}}. {{per-side timing and separate-or-connected garment structure}}. The recorded operation occurs once; the resulting state is {{observed final state}}.
```

### R50 · 逐侧不对称状态

```text
At {{TS}}, the left leg has {{left state}} and the right leg has {{right state}}. Preserve these different states throughout {{interval}}, changing only {{specified item}} at {{specified event time}}.
```

### R51 · 单侧织物动作

```text
<Subject 3> takes hold of {{garment}} on {{specified side}} at {{contact point}} and draws it along {{observed path}} during {{interval}}. The other side retains {{actual other-side state and motion}}.
```

### R52 · 硬筒靴或机械壳体

```text
{{actor}} takes hold of {{rigid item}} at {{contact point}} and moves the shell as one piece along {{observed path}}. {{observed foot or limb response}} accompanies the removal, leaving {{actual remaining parts}}.
```

### R41 · 覆盖状态时间线

```text
During {{interval}}, {{garment construction and coverage}} follows the observed removal. At {{each relevant time}}, {{per-side visible and still-covered areas}}. Uncovering occurs only as the corresponding part of the garment clears that area.
```

### R42 · 策略 A 画外脱

仅原片已有画外脱除，或用户明确授权这种调整时选用；后续可见镜头的实际位置按原片改写。

源句选项 1：

```text
framing the body from the hips to mid-shin, the feet below the bottom edge of frame
```

源句选项 2：

```text
The feet are never in frame while any part of the {{袜}} is still on the legs. The arrow pulls the rolled edge down and out of the bottom edge of frame, and the arrow leaves last. The bare feet appear only in the next shot, in the full shot, after the {{袜}} are gone.
```

### R43 · 策略 B 混合节奏

仅原片确有同步后分侧的动作；时长与侧别按观察改写。不可与另一套同步时序同时使用。

```text
The arrow pulls both leg tubes down together in one continuous move to just below the knees, and there the two tubes separate: the arrow frees the left foot first and then the right, each foot out in under four tenths of a second with motion blur, the toes coming out last, and each rolled band keeps moving down in the same continuous move and never stops at the ankle.
```

### R44 · 策略 C 袜圈落地 + 抬脚抽出

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

### R45 · 策略 D 相机下摇跟随

仅原片已有下摇或用户明确授权时用；不凭模板改变摄影机。

```text
The camera tilts down slowly, keeping the rolled edge of the {{袜}} in the middle of frame, so the feet stay at the very bottom edge of frame and out of frame until the fabric has cleared the toes. The tilt is one slow continuous move inside the removal, it stops the instant the fabric leaves frame, and after that the camera is locked.
```

### R62s · 织物运动与身体关系

```text
During {{removal interval}}, {{garment motion}} occurs while {{observed leg, foot, hip and hand behaviour}} is preserved. Use stationary support only for the limbs that actually remain still.
```

## 沿轨迹生成（尾巴等）

### R23 · 顺轨迹生成

```text
The pointer travels along {{source path}}, and <Subject 8> is drawn behind its tip from {{attachment or starting point}} toward {{endpoint}} with {{observed formation sequence and timing}}.
```

### R23b · 尾巴原位幻化

只有原片确有原位替换时用；根部、数量、材质与粒子均按当前素材。

```text
At {{TS}} the {{old_tail}} already on <Subject 1> does not stay: at its base at the base of the spine there is one brief particle flare, the old tail breaks into particles and drifts away along the pointer path, and <Subject 8> is drawn out of that same base behind the pointer tip along that path - root first, then the thickness, then the tip last - as if the cursor were repainting it in one stroke. There is one tail in frame at every moment: the old tail never returns and no second tail appears beside it.
```

### R23c · 绘制粒子

仅原片有粒子轨迹；颜色、强度与消散时间取实际值，不固定半秒。

```text
The stroke is not invisible: small self-lit {{角色配色}} particles run directly behind the pointer tip along the whole curve, and <Subject 8> solidifies out of them one step behind the tip, brightest where the tip is and thinner behind it. The particles sit on the pointer path only - the light grey background, the floor grid, the exposure and the colour grade stay exactly as they were. The trail stops when the stroke stops and is gone within 0.5 seconds after the tip stops: no glow, no smoke and no loose particles remain around <Subject 8> after that.
```

### R24 · 生成次数与在场范围

```text
<Subject 8> begins appearing at {{TS}} and develops through {{observed phases}}. There are {{observed number}} strokes. Its state afterward is {{observed persistent state}}.
```

### R25 · 观察生成与情绪过程

```text
While {{item}} forms during {{interval}}, the gaze follows {{observed focus}}. The expression changes from {{preceding emotion}} to {{observed response}} at {{source-aligned reaction time}} and develops into {{following emotion}}.
```

## 点选生成（头饰等）

### R26 · 瞬时生成 + 同镜表情翻转

点选次数、闪光与物件出现时点取原片，不强制一次或成对。

```text
the tip of <Subject 3> arrives at {{target_part}} from inside the frame, the halo closes on it, there is one click and one brief flash, and <Subject 9> appears in that instant.
```

### R26b · 头饰原位幻化

只有原片有原位替换时用；旧部件同时从不可变化清单中移出。

```text
the tip of <Subject 3> arrives at the {{old_headwear}} already on the head, the halo closes on it, there is one click and one brief flash, and in that instant the {{old_headwear}} is gone and <Subject 9> appears at the same place on the head, same anchor point, same height, in one step with no second flash.
```

### R26c · 生成粒子

仅原片有粒子环；环数、颜色与消散时长以原片为准。

```text
The flash is not empty: at the instant of the flash one ring of small {{角色配色}} particles opens around {{target_part}} and closes inward onto <Subject 9>, which is already solid in the first frame after the flash. There is one ring only, it dissipates within 0.4 seconds, and no glow, smoke or loose particles remain on or around <Subject 9> after that - the light grey background, the floor grid and the exposure stay exactly as they were.
```

### R58 · 点出部件的近景

生成事件不强制特写；仅原片确有这种取景时用，0.3 秒等数值按原片改写。

```text
At {{TS}}, close-up, the camera moving in from the previous framing in one continuous 0.3 second move and then locking, framing {{target_part}} with the hands at rest and the tip of <Subject 3> in frame, pointing at {{target_part}}.
```

### R58b · 生成部位离脸远时，同一镜内一次上移到脸

仅原片确有同镜上移到脸时用，不为看到表情新增运镜。

```text
At {{TS2}} the camera tilts up along the body in one continuous 0.4 second move with no cut and comes to rest on the face, still a close-up.
```

### R47 · 生成瞬间表情变化

```text
At {{event time}}, <Subject 1> shows {{first visible reaction}}. After {{observed delay}}, this develops into {{following emotion}}, expressed through {{specific eyes, mouth, head, shoulders and hands}}.
```

### R59 · 生成物持续在场与正常遮挡

```text
From {{appearance time}} onward, <Subject 9> retains {{shape, colour, attachment and state}} until {{next observed change or ending}}. Normal source occlusion is preserved. Any confirming touch acts on the already-existing object and does not generate it again.
```

## 场景线框建模

### R63 · 场景框选 + 场景排他

仅原片确有框选与场景建模；原背景不是空网格时替换背景描述。

```text
At 00:00.000 the arrow tip draws a rectangle around <Subject 1>: four corner brackets appear and the rectangle closes once around the whole body, the arrow resting on the lower-right corner. While it closes, the light grey background and the floor grid are still exactly what they were - an empty viewport, nothing built anywhere in it.
```

### R63b · 框选时她的反应

实际表情按 S08，不能因框选默认疑惑。

```text
While the rectangle closes, the head tilts to one side and the eyes track the corner bracket nearest the face, the brows lift a little, the mouth presses into a small curious line, and both hands stay loose at the sides.
```

### R74 · 场景生成时的视线与反应

按原片看向实际生成位置，表情按 S08，不自动惊喜。

```text
The eyes of <Subject 1> stay on the travelling wire: as the lines run out across the ground and rise into the {{场景结构}}, the head follows them at half the angle, and the reaction runs with the build rather than after it - the mouth opens in a small breath as the first wall rises, then the eyes brighten and the head lifts as the {{招牌与灯具}} light one at a time.
```

### R64 · 场景线框生成 + 粒子

场景结构、线框、粒子颜色和消散时间均以本期原片为准。

```text
The empty viewport builds into {{场景}} in one continuous pass: cyan wire lines run out across the ground from the rectangle and rise into the {{场景结构：墙面 / 屋顶 / 栏杆 / 树干}}, and the surfaces fill behind the travelling wire in the same move. Small cyan and grey particles ride along the wire lines and settle into the surfaces, brightest where the fill is travelling, and they are gone within one second after the build finishes.
```

### R65 · 招牌依次点亮 + 网格退场

仅原片有灯具依次亮起/旧背景退场时用；无招牌不得编造招牌。

```text
the {{招牌与灯具}} light one at a time in a short row, each with one small flare of the same particles, and the grey floor grid fades out under the built ground and stays gone for the rest of the clip.
```
