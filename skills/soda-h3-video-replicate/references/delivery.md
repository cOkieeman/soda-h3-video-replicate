# 组织可使用的交付

## 完整复刻说明的顺序

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

## 素材与提示词对应

媒体分配表要逐段写，至少包含局部编号、实际素材、承担的作用。例如某张图提供身份，另一张图提供服装；不要只写“参考图都放进去”。同一素材在不同时间框中的编号可以变化，提示词必须随实际分配一起检查。

可以用显示名称或用户给出的文件名帮助识别；文档模板不包含作者账号、个人目录或固定盘符。没有实际找到文件时，写“待提供的角色正面图”等明确状态，不把建议素材当成已存在的资源。用于接续的 Latent 单独说明连接用途，不放入图片或视频编号序列。

参考静帧任务按每张图交付：对应用途、源时间或事件、需要保持的构图和动作状态、允许替换的内容、完整英文图像提示词。只为后续生成准备静帧提示词时，不声称已经产出图片。具体写法见 [cinematography.md](cinematography.md)。

## 给出真正可执行的裁尾办法

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

## 结尾状态说明

分别报告素材观察、帧规划、提示词、界面核对、生成和尾裁的状态。已实际完成的项目附对应证据，不把静态文档检查概括为全流程验证。
