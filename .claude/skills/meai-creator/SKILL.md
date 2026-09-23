---
name: meai-creator
description: |
  使用 ME AI API 生成图片和视频。
  触发词：生图、生成图片、AI画图、文生图、图生图、生视频、生成视频、文生视频、图生视频、ME AI、meai
  支持模型：sd-2-fast / sd-2-c1 / sd-2.5-c1 等（视频，meaicc，默认 sd-2-fast）
---

# ME AI 图片视频创作 Skill

## 环境要求

- Python 3.8+
- 环境变量 `MEAI_API_KEY`：你的 API Key（sk-xxxx 格式）
- 环境变量 `MEAI_BASE_URL`：可选，默认 `https://api.meaicc.com`（2026-09-24 用户定为准则；旧 `api.meai.cloud` 仍可用此变量覆盖）

## 脚本位置

所有脚本在 `~/.claude/skills/meai-creator/scripts/` 目录下：

- `meai_api.py` — 核心 API 调用脚本，支持所有功能

## 功能一览

| 功能 | 命令 | 模型 |
|------|------|------|
| 文生图 | `python meai_api.py image --prompt "描述"` | seedream-5.0 |
| 图生图 | `python meai_api.py image --prompt "描述" --image "url"` | seedream-5.0 |
| 文生视频 | `python meai_api.py video --prompt "描述"` | seedance-2.0 |
| 图生视频 | `python meai_api.py video --prompt "描述" --first-frame "url"` | seedance-2.0 |
| 首尾帧视频 | `python meai_api.py video --prompt "描述" --first-frame "url" --last-frame "url"` | wan2.7 |
| 参考生视频 | `python meai_api.py video --prompt "描述" --ref-images "url1,url2"` | seedance-2.0 |

## 使用流程

### 1. 文生图

```bash
python ~/.claude/skills/meai-creator/scripts/meai_api.py image \
  --prompt "一只可爱的橘猫坐在窗台上晒太阳" \
  --size "2048*2048" \
  --output "./output.png"
```

### 2. 图生图

```bash
python ~/.claude/skills/meai-creator/scripts/meai_api.py image \
  --prompt "将人物换成白色衣服" \
  --image "https://example.com/source.jpg" \
  --output "./output.png"
```

### 3. 文生视频

```bash
python ~/.claude/skills/meai-creator/scripts/meai_api.py video \
  --prompt "小猫在草地上奔跑" \
  --resolution "1080P" \
  --ratio "16:9" \
  --duration 15 \
  --output "./output.mp4"
```

### 4. 图生视频（首帧）

```bash
python ~/.claude/skills/meai-creator/scripts/meai_api.py video \
  --prompt "图片中的人物开始跳舞" \
  --first-frame "https://example.com/frame.jpg" \
  --output "./output.mp4"
```

### 5. 首尾帧视频（仅 wan2.7）

```bash
python ~/.claude/skills/meai-creator/scripts/meai_api.py video \
  --prompt "人物从站立到奔跑" \
  --first-frame "https://example.com/start.jpg" \
  --last-frame "https://example.com/end.jpg" \
  --model "wan2.7" \
  --output "./output.mp4"
```

### 6. 参考生视频

```bash
python ~/.claude/skills/meai-creator/scripts/meai_api.py video \
  --prompt "图1中的人物穿上图2的装饰" \
  --ref-images "https://example.com/img1.jpg,https://example.com/img2.jpg" \
  --output "./output.mp4"
```

## 参数说明

### 图片参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--prompt` | 必填 | 文本描述 |
| `--image` | 无 | 图生图的源图片 URL |
| `--model` | seedream-5.0 | 可选 seedream-4.5 |
| `--size` | 2048*2048 | 分辨率，支持 2048*2048、4096*2304 等 |
| `--n` | 1 | 生成数量 |
| `--output` | ./meai_output.png | 输出路径 |

### 视频参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--prompt` | 必填 | 文本描述 |
| `--first-frame` | 无 | 首帧图片 URL |
| `--last-frame` | 无 | 尾帧图片 URL（仅 wan2.7） |
| `--ref-images` | 无 | 参考图片 URL，逗号分隔 |
| `--model` | sd-2-fast | 视频模型，见 meaicc 模型广场（sd-2-fast / sd-2-c1~c8 / sd-2.5-c1 等） |
| `--resolution` | 1080P | 分辨率 |
| `--ratio` | 16:9 | 宽高比 |
| `--duration` | 15 | 时长（秒），**范围 5–15** |
| `--prompt-extend` | false | 是否扩展提示词 |
| `--output` | ./meai_output.mp4 | 输出路径 |

## 分辨率参考

| 宽高比 | 4K | 2K | 1K |
|--------|-----|-----|-----|
| 1:1 | 4096*4096 | 2048*2048 | 1280*1280 |
| 16:9 | 4096*2304 | 2688*1536 | 1696*960 |
| 9:16 | 2304*4096 | 1536*2688 | 960*1696 |
| 4:3 | 4096*3072 | 2368*1728 | 1472*1104 |
| 3:4 | 3072*4096 | 1728*2368 | 1104*1472 |

## 注意事项

1. **时长边界**：`duration` 只能 **5–15 秒**；参考生视频另有「输入视频 + 输出视频合计 ≤ 25 秒」限制
2. **首尾帧**：sd-2 家族支持（与旧站 wan2.7-only 不同），`--first-frame` + `--last-frame` 同传
3. **图片上传**：图生图、首帧等需要 HTTP/HTTPS 地址，本地文件需先上传到图床；图片分辨率需 ≥300×300
4. **任务轮询**：异步任务会自动轮询（每 20 秒），生成完成自动下载
5. **内容审核**：避免违规、敏感内容，生成失败可能仍扣费
6. **缓存时效**：网页生成的内容仅缓存 10 小时，及时下载

## 当用户请求时

1. 理解用户要生成什么（图片/视频、文生/图生）
2. 选择合适的模型和参数
3. 用 `python` 运行 `meai_api.py` 对应子命令
4. 等待生成完成，展示结果给用户
5. 提示用户输出文件位置

如果用户只说了"帮我画一个xxx"，默认用文生图（seedream-5.0）。
如果用户说"把这个图片变成视频"，用图生视频（seedance-2.0）。
