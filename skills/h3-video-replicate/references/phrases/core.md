# 通用句库（R 编号沿用原稿）

按需读取：只在组装某一镜、需要对应控制句时才打开本文件，不要整份贴进提示词。

用法：

1. 先选事件，再核实句子里的每一项事实，用当前素材的值替换全部 `{{...}}`。
2. 每条都是**条件句**：原片没有对应事件就不用，不补位。
3. 示范句里写死的左右、颜色、身体部位、次数、时长，只有与当前原片一致才能原样保留；否则保留“因果与连续性”的目的，改写其余部分。
4. 同一条下的“源句选项”是互斥用途，挑适用的，不要全拼。
5. R/S/Q 内部编号不得泄漏进最终提示词。R40、R49 原稿未定义，不补造。
6. 涉及光标、换装、鞋袜、生成物、线框建模的句子在 `cursor-edit.md`。

## 风格、环境与光照

### R01 · 风格与场景锚点

```text
Style: {{current visual style}}. The scene is {{current environment and layout}}, with {{observed lighting and material treatment}}. Preserve these established properties except where the source video or the requested edit explicitly changes them.
```

### R02 · 未发生变化的背景保持

```text
Throughout {{interval}}, the background retains {{established scene state}}. Only {{observed changes, if any}} occur at their specified times.
```

### R03 · 曝光与光照连续

```text
During {{interval}}, exposure, white balance, light direction and skin tone follow {{observed lighting progression}}. Removing or replacing {{item}} does not introduce an unrelated lighting change.
```

## 首帧、切镜与段间衔接

### R06 · 原片开场状态

```text
[Shot 1] <Subject 1> is already in {{source first-frame pose, position and orientation}}, with {{hand positions, gaze and expression}}. The camera has {{source framing and movement}}. Continue {{motion already in progress}} without adding a preparatory pose.
```

### R27 · 切镜状态继承

```text
At this cut, {{visible carried state}} continues from the preceding shot, including {{expression, gaze and item states}}. {{observed changes after the cut}} occur at their specified times.
```

### R28 · 段尾运动状态交接

```text
During {{tail interval}}, {{visible subjects and objects}} continue {{exact observed motion phases and emotional progression}} with {{camera movement, framing, environment and active sound}}. At the final frame, {{end state}}. This interval continues into the next segment without restarting.
```

### R29 · 段首重叠接续

```text
During 00:00.000–{{overlap end}}, this segment carries the preceding segment’s final {{actual overlap frames}} frames: {{the same observed action phases, expression changes, positions, objects, camera and sound}}. This is the same occurrence, not a repeated action. After {{overlap end}}, continue the source-aligned timeline.
```

### R67 · 段首动作相位保持

```text
The opening continues the preceding tail at the same movement phase and speed. Preserve {{motion already in progress}} without resetting the pose or inserting a pause.
```

### R30 · 静止待机，仅原片静止区间用

```text
During {{interval}}, <Subject 1> maintains {{observed stance}}. Only {{observed breathing or small movements}} occur.
```

### R32 · 固定机位，仅原片对应区间用

```text
The camera holds the source framing without moving during {{interval}}.
```

### R22 · 相机环绕

```text
During {{interval}}, the camera moves around <Subject 1> along {{source direction and arc}}, from {{start view}} to {{end view}}, with {{observed speed profile}}. {{character movement or stationary stance}}. Preserve any source cut separately; do not substitute a body turn for a camera orbit.
```

### R31 · 环绕时人物不动，仅符合原片时用

```text
During {{orbit interval}}, {{observed stationary body parts}} remain in place while the camera moves. {{observed independent movement}} continues.
```

### R66 · 局部支撑锁定

```text
During {{interval}}, {{actual support foot or stationary body part}} remains at {{observed support position}} while {{moving part}} performs {{source action}}.
```

## 动作因果与接触

### R60 · 施动者语法

```text
{{actual actor}} {{contact verb}} {{item}} at {{contact point}} and moves it along {{observed path}}. {{observed response of the body or object}} follows this cause.
```

### R61 · 可见抓握接触

```text
At {{TS}}, {{actor contact point}} meets {{item contact point}}. {{material-appropriate deformation or rigid contact}} remains consistent as the item follows {{observed motion}}.
```

### R62 · 身体跟随物件

```text
During {{event}}, <Subject 1> responds with {{observed limb, hip, head and secondary motion}}. The hands stay at {{actual hand positions}} unless the source shows a hand action.
```

## 视线、情绪与反应

### R04 · 事件反应的运动层次

```text
The reaction follows the timing in the source: {{observed anticipation, response and settling}}. {{secondary part}} follows with {{observed delay and amplitude}}.
```

### R05 · 跨镜表情连续

```text
At each cut, preserve the expression and emotional intensity reached immediately before it, then follow the next observed expression change at its source-aligned time.
```

### R08 · 好奇反应，原片存在时用

```text
At {{TS}}, the eyes track {{observed target}}, while {{observed head, brow, mouth and shoulder response}} conveys curiosity at {{observed intensity}}.
```

### R09 · 情绪区分

```text
The expression during {{interval}} is {{observed emotion}}, carried by {{visible facial and body cues}}; it does not restart as a different reaction at the segment boundary.
```

### R11 · 事件第一反应

```text
The reaction begins at {{TS}} relative to {{trigger event}}: {{observed eye, mouth, head, shoulder and hand response}}.
```

### R11b · 已有情绪上的再次反应

```text
At {{TS}}, {{observed response to the new event}} develops from the expression already present. {{Existing facial colour or other visible emotional cue}} follows {{observed change}}, without resetting the face first.
```

### R12 · 脸红，原片或用户要求时用

```text
At {{TS}}, a {{observed colour and intensity}} flush {{appears or deepens}} on {{observed facial areas}}, following {{observed onset and fading progression}}.
```

### R13 · 手部反应与次级运动

```text
At {{TS}}, {{hand action and contact position}} follows the event. {{visible clothing or attached-part response}} settles according to the observed motion, while the gaze remains on {{target}}.
```

### R14 · 视线跟随离场物

```text
The eyes follow {{item}} along {{observed path}} toward {{exit edge}}. The head follows by {{observed amount}}, and the gaze next moves to {{next observed target}} at {{TS}}.
```

### R20 · 操作过程视线

```text
During {{event interval}}, the eyes of <Subject 1> follow {{pointer or held item}} along {{observed trajectory}}. At {{TS}}, the gaze shifts to {{next observed focus}}.
```

### R72 · 事件与视线反应对应

```text
For each observed interaction, the gaze follows {{actual focus}} and the response begins at {{source-aligned time relative to the event}}. Pointer travel alone does not create an additional reaction unless the source shows one.
```

### R73 · 重复事件的反应强度

```text
The response to this repeated event is {{observed intensity relative to the first}}, with {{visible expression and body response}} at {{TS}}. It does not automatically repeat the first surprise.
```

### R75 · 展示动作的情绪与时长

```text
During {{display interval}}, {{observed action}} accompanies {{observed expression and gaze}}. The movement uses {{observed amplitude and count}}, with {{observed hold and return timing}}. Preserve the source timing without adding repetitions.
```

### R48 · 视线环顾

```text
During {{interval}}, the gaze moves through {{ordered visible targets}}. The eyes and head follow {{observed lead or delay}}, with {{observed turning amplitude and settling}}. {{torso, shoulder, hair and foot behaviour}} matches the source.
```

### R48b · 视线扫描次数

```text
There are {{observed count}} looks during {{interval}}, toward {{ordered targets}} at {{source-aligned times}}.
```

### R48c · 转头幅度

```text
Each head turn follows {{observed angular or screen-relative range}} toward {{target}}. Preserve the source relationship between eye movement, head rotation and any torso turn.
```

## 身体动作（仅原片存在时）

### R21 · 观察脚部，原片存在时用

```text
At {{TS}}, <Subject 1> looks toward {{observed side and target}} with {{observed head and eye motion}}. {{actual foot placement or movement}}. The look lasts {{observed duration}} and proceeds to {{next observed focus}}.
```

### R36 · 弯腰与相机关系

```text
At {{TS}}, <Subject 1> bends toward {{observed target}} with {{head, shoulders and waist motion}}. The camera {{observed stationary or moving behaviour}}, maintaining {{source composition}}.
```

### R37 · 伸手动作

```text
At {{TS}}, {{observed hand}} reaches toward {{target}}, with {{palm orientation, fingers and elbow pose}}, and holds or withdraws according to {{observed timing}}.
```

### R38 · wink 与眨眼计数

```text
At {{TS}}, {{observed eye}} closes in {{observed wink duration}} while {{other eye and mouth expression}}. Preserve {{observed wink and blink counts}} during this interval.
```

### R68 · 抬脚展示，仅原片存在时用

```text
During {{interval}}, <Subject 1> lifts {{observed foot}} with {{knee and hip motion}}, reaching {{observed height or angle}}. The camera uses {{source view}}. {{observed hold or ankle movement}} lasts {{duration}} before {{observed lowering or continued lift}}. The face and gaze follow {{source expression and focus}}.
```

### R69 · 弯腰触腿，仅原片存在时用

```text
At {{TS}}, <Subject 1> bends with {{observed body motion}} and {{hand}} touches {{actual contact area}}, moving along {{path}} for {{observed count and duration}}. {{observed recovery or continuing pose}} follows.
```

### R70 · 脚部细节，仅原片存在时用

```text
During {{interval}}, the camera frames {{observed area}}. {{observed foot and toe action}} occurs with {{actual count, amplitude and duration}}, while {{support and other-side state}} remains consistent.
```

### R71 · 面部细节

```text
During {{interval}}, {{source face framing}} shows {{observed eyes, brows, mouth, head and colour progression}}. Preserve the expression carried from the preceding view and its source-timed changes.
```

### R57 · 卧姿腿脚运动，仅原片存在时用

```text
During {{interval}}, the legs and feet follow {{observed alternating or simultaneous movement}}, with {{observed amplitude, rate and count}}. This movement continues with {{concurrent upper-body action}} according to the source timing.
```

## 结尾与手势

### R39 · 原片结尾

```text
From {{TS}} until the source ending, {{observed final action or held pose}}, with {{remaining movement, expression and camera behaviour}}. Do not append a new closing gesture.
```

### R54 · 比心

仅原片有比心；手势保持与回收时点按原片，不自动加入收尾。

```text
Both hands come up in front of the chest and the two hands form one small heart aimed at the lens, held for one beat, then the two hands come apart and drop back to the sides.
```

### R55 · 上半身特写 wink 收尾

仅原片对应 wink/上半身镜头适用；删去与原片不符的脸红、变焦和消退动作，时间来自本期。

源句选项 1：

```text
At {{TS}}, upper-body close-up, framing the body from the mid-chest to above the top of the ears, both ears and both shoulders inside frame: there is no cut, the camera pulls back slightly in one continuous 0.3 second move and then locks. Both hands come away from {{头部部件}} and drop to the sides in one small move. The head lifts and the eyes come up to the lens, and in that same instant a pink flush spreads across the cheeks, the bridge of the nose and the tops of the ears, the flush on the face only. The head tilts to one side by about ten degrees, one eye closes in a clean wink while the other stays open on the lens, and the mouth presses into a small playful smile. The wink is held for a quarter of a second, then both eyes are open on the lens and the head comes back level, and the flush fades out completely as the head levels.
```

源句选项 2：

```text
The face carries no colour from one second into this clip until the last shot; in the last shot only the face may take colour, and it is gone before that shot ends; the neck, the chest and the décolletage never take colour.
```

## 声音

### R33 · 环境声音

```text
{{verified ambient sound and its continuity across the interval}}.
```

### R34 · 无对白无音乐，仅实际静音设置适用

```text
Silent. No dialogue, environmental sound or music is requested; the workflow audio configuration is set to silence.
```
