---
name: film-creator
description: |
  一句话或一张图 → 30 秒电影短片。六幕节拍剧本(由 Claude 现写, 非模板) → 逐幕关键帧+视频生成(委托 seedance-video / meai-creator) → ffmpeg 拼接成片。
  触发词：创作电影、拍电影、做一部短片、30秒短片、电影感短片、film creator、make a film
---

# Film Creator — 一句话拍成 30 秒电影

## 分工

| 环节 | 谁做 |
|------|------|
| 剧意分析 + 六幕剧本写作 | **Claude 现写**（本 skill 的核心价值，不用模板） |
| 逐幕关键帧图 + 视频生成 | 委托兄弟 skill 脚本（seedance-video 主 / meai-creator 备） |
| 拼接成片 | `scripts/shoot_film.py` 调 ffmpeg |

## 流程

### 1️⃣ 建工作目录
```
Films/<片名slug>/
  screenplay.json   ← Claude 写
  scene_0N_key.png  ← 编排器生成(关键帧)
  scene_0N.mp4      ← 编排器生成
  final_film.mp4    ← 成片
```

### 2️⃣ Claude 写六幕剧本 → screenplay.json

30 秒 = **6 幕 × 5 秒**（5s 恰好是 seedance 平台的时长档位）。固定节拍：

| 幕 | 节拍 | 镜头语言 |
|----|------|----------|
| 1 | establishing | 大远景定场，镜头缓推 |
| 2 | introduction | 中景 → 特写，引入主体 |
| 3 | development | 跟随/侧移，情节推进 |
| 4 | climax | 特写或戏剧角度，关键瞬间 |
| 5 | resolution | 中景稳定镜头，情绪落地 |
| 6 | closing | 大远景缓拉，收束余韵 |

**schema**（scenes 长度可 5-6，duration_per_scene 保持 5）：

```json
{
  "title": "最后一朵花",
  "backend": "seedance",
  "ratio": "16:9",
  "duration_per_scene": 5,
  "keyframes": true,
  "style_bible": "废土世界, 锈蚀混凝土, 暖橘夕照与青灰阴影, 电影感写实, 2.39:1 压暗气质",
  "scenes": [
    {
      "number": 1,
      "beat": "establishing",
      "shot": "EXT. 废弃城市 - 黎明 / 大远景",
      "action": "荒芜城市全貌, 藤蔓爬满断墙(给人看的剧情注记)",
      "image_prompt": "静态构图描述: 荒芜城市全景, 锈蚀高楼, 藤蔓覆墙, 晨光斜照, 一只小车机器人居于画面下三分之一",
      "video_prompt": "运动描述: 晨雾极缓慢流动, 镜头缓缓推进, 机器人几乎静止地停在原地"
    }
  ]
}
```

**剧本写作铁律：**
- **慢节奏审美（最高优先）**：运动物体必须缓慢/近乎静止；动感来自光影、水波、云雾、风的缓慢变化 + 缓慢运镜。禁止快移（船不能像公路汽车）。
- `image_prompt` 写**静态画面**（构图/光线/主体位置）；`video_prompt` 写**运动与运镜**。两者分开，关键帧才稳。
- **连续性靠 style_bible + 人物措辞一致**：每幕 prompt 都会自动拼上 `style_bible`；跨幕提到同一主体时用完全相同的外貌描述句。
- 每幕 prompt 控制在 80 字内，堆细节不如挑重点。

### 3️⃣ 先 dry-run 再实拍

```powershell
python "D:\zed horse\.claude\skills\film-creator\scripts\shoot_film.py" .\Films\<slug>\screenplay.json --dry-run
```

确认命令无误后去掉 `--dry-run` 正式开拍。**断点续跑**：某幕失败直接重跑同一命令，已生成的幕自动跳过；单独重拼用 `--assemble-only`。

## 后端选择

| 后端 | 命令参数 | 关键帧 | 特点 |
|------|----------|--------|------|
| `seedance`（默认） | `--backend seedance` | ✅ 本地图生视频 | shiping 平台，5s≈7 积分，内置 --calm 慢节奏修饰 |
| `meai` | `--backend meai` | ❌（首帧需 HTTP URL） | ME AI 平台 seedance-2.0，纯文生视频 |

⚠️ **真实人脸不能作 seedance 参考图**（平台肖像保护会拒绝）。用户给真人照片时：改文生视频，或换 meai 后端。AI 生成的关键帧图不受限。

## 费用预估（seedance）

6 幕 × 5s ≈ 42 积分 + 关键帧图 6 张。审核失败仍扣费，prompt 避免敏感内容。拿不准先 `--dry-run`。

## 与其他 skill 的边界

- 只做「剧本 → 逐幕生成 → 拼接」这条线；成片要**字幕/配乐/包装** → 接 hyperframes；要**单段图生视频** → 直接用 seedance-video / meai-creator，别绕道本 skill。
- 用户提供了参考图：本地文件直接喂 seedance 关键帧链路；此时可把幕 1 的 image_prompt 换成对参考图的转述以锁定画风。
