# ME AI 视频创作可复用清单

> 基于 meai-creator skill / seedance-2.0 图生视频的实战参数与提示词模板。
> 全部参数来自实际跑通的命令，非文档示例。每次创作照此填空即可。

---

## 一、固定参数（每次直接套用）

| 参数 | 值 | 说明 |
|---|---|---|
| `--model` | `seedance-2.0` | 图生视频主力模型 |
| `--resolution` | `1080P` | 全程 1080P（需更高可改 `2K`/`4K`）|
| `--ratio` | `16:9` | 横屏（竖屏改 `9:16`，方屏 `1:1`）|
| `--duration` | `15` | 默认 15s（范围 4–15s）|
| `--first-frame` | `<图床直链>` | **必须有首帧** |
| `--prompt-extend` | 省略 | 默认不开；需要更丰富运镜时可加 |
| `--output` | `D:\zed horse\NN.mp4` | 命名规律：`01.mp4 / 02.mp4 …` |

**首尾帧 / 参考图模式**（按需切换）：
- 首尾帧：`--first-frame <A> --last-frame <B> --model wan2.7`
- 多参考图：`--ref-images "url1,url2"`（seedance-2.0）

---

## 二、提示词模板（公式）

```
[景别+主体+场景], [运镜英文术语], [光线], [色调/风格], [画质+稳定性], [强调细节]
```

### 运镜术语库

| 英文术语 | 中文 | 适用场景 |
|---|---|---|
| `Slow Cinematic Pan + Subtle Zoom In` | 缓慢横移 + 微推 | 建筑/风景特写 |
| `Smooth Dolly Forward` | 平滑推进 | 街景、由远及近 |
| `Crane Up + Slow Pan` | 升起 + 慢摇 | 全景、节日场面 |
| `Tracking Shot` | 跟随 | 人物/动物行走 |
| `Dolly Zoom` | 拉伸（眩晕感）| 情绪强调 |
| `Orbit` | 环绕 | 物体 360° 展示 |
| `Low Angle` | 仰拍 | 宏伟、压迫感 |
| `Top-down / Bird's Eye` | 俯拍 | 地理、布局 |

### 风格词库（高频词）

`《天使爱美丽》温馨色调` · `治愈系风格` · `温暖午后阳光` · `清新自然光` · `明亮欢快色调` · `4K高清/超清` · `画面稳定无闪烁` · `画面流畅` · `人物面部清晰稳定` · `细节丰富`

---

## 三、4 个真实示例（照抄级参考）

```
① 中景特写一座绿色木制风车,巨大的风车叶片在蓝天白云下缓慢旋转,运河水面倒映着风车的完整影像,
   镜头从侧面缓慢横移至正面, Slow Cinematic Pan + Subtle Zoom In, 清新自然光, 治愈系风格,
   4K高清, 画面稳定, 展现风车叶片的机械美感和木质纹理细节

② 赞丹风车村街景,传统绿色木制风车、彩色木屋和石板路,游客穿着传统荷兰服饰在木鞋作坊前拍照,
   镜头从全景缓慢推进至中景, Smooth Dolly Forward, 温暖午后阳光, 《天使爱美丽》的温馨色调,
   4K高清, 画面流畅, 人物面部清晰稳定, 服装细节丰富, 充满生活气息

③ 赞丹风车村街景,……镜头继续从中景缓慢推进至近景特写, Smooth Dolly Forward,
   温暖午后阳光, 《天使爱美丽》的温馨色调, 4K高清, 画面流畅, 人物面部清晰稳定, 服装细节丰富

④ 风车挂满荷兰国旗和鲜花花环,橙色、白色、蓝色旗帜在风中飘扬,人群聚集在风车下庆祝,
   镜头从低角度仰拍缓慢升起, Crane Up + Slow Pan, 节日氛围浓厚, 明亮欢快色调,
   4K超清, 画面稳定无闪烁, 展现荷兰人对传统文化的热爱和自豪
```

---

## 四、完整流程（5 步）

```
① 首帧图   → 自备图片，或 seedream-5.0 文生图（--size 2048*2048 或 2688*1536）
② 首帧传递 → ★推荐 base64 data URI 直传 meai（国内直连、零依赖，已验证可用）
             压图到 ≤1280px JPEG(q88) → base64 → 塞进 input.media[].url
             参考 `gen_video_05.py`（PIL 压图 + urllib，结构镜像 meai_api.py）
             ⚠ 海外图床 catbox/litterbox/0x0.st 从国内被稳定拦截，弃用
③ 图生视频 → POST https://api.meai.cloud/v1/videos（参数见第一节，首帧可走 base64）
④ 旁白 TTS → _windmill_build/gen_narration.py（可选）
⑤ 合成     → ffmpeg concat 多镜头 + BGM（_windmill_build/compose.sh）
```

---

## 五、命令骨架（复制即用 · PowerShell）

```powershell
python "D:\zed horse\.claude\skills\meai-creator\scripts\meai_api.py" video `
  --prompt  "[景别+场景], [运镜], [光线], [色调], 4K高清, 画面稳定, [细节]" `
  --first-frame "https://litter.catbox.moe/xxxxxx.png" `
  --model "seedance-2.0" --resolution "1080P" --ratio "16:9" --duration 15 `
  --output "D:\zed horse\05.mp4"
```

文生图首帧（可选第一步）：

```powershell
python "D:\zed horse\.claude\skills\meai-creator\scripts\meai_api.py" image `
  --prompt "[首帧画面描述]" `
  --model "seedream-5.0" --size "2688*1536" `
  --output "D:\zed horse\PIC\05.png"
```

---

## 六、踩坑备忘

1. **海外图床（catbox/litterbox/0x0.st）从国内被稳定拦截**：litterbox 返回 `412 No file!`（数据已发全仍被拒）、catbox 主站连接失败。→ **改用 base64 data URI 直传 meai**，国内直连零依赖，2026-06-13 实测生成 05.mp4 成功。
2. **base64 注意**：原图先压到 ≤1280px、JPEG q88（base64 ≈ 300–450KB），别直接传 2MB+ 原图。meai_api.py 目前只支持 URL，base64 用 `gen_video_05.py` 这类小封装。
3. **异步轮询**：脚本每 20s 轮询，最长等 10 分钟；终端会打印 `任务 ID` 和进度。
4. **内容审核**：避免真人正脸、敏感内容；审核失败可能仍扣费。
5. **环境变量**：需先设 `MEAI_API_KEY`（`sk-xxxx`），否则脚本直接退出。

---

## 七、相关文件位置

- Skill 脚本：`D:\zed horse\.claude\skills\meai-creator\scripts\meai_api.py`
- 首帧图库：`D:\zed horse\PIC\`（`01.png`–`04.png` 为已用过的风车村首帧）
- 视频片段：`D:\zed horse\01.mp4` … `04.mp4`
- 旁白 + 合成：`D:\zed horse\_windmill_build\`（`gen_narration.py`、`compose.sh`、`narration/*.mp3`）
- API 对接教程：`D:\zed horse\Design\ME_AI_图片视频api对接教程.md`
