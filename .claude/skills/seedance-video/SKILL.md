---
name: seedance-video
description: |
  以本地图片作参考图 + 提示词, 调用 seedance 级视频模型 (shiping.djpsd.com 平台, model=video-v1) 生成视频。原生支持本地图上传, 内置慢节奏静谧审美。
  触发词: 图生视频、seedance、seedance 2、参考图视频、把图片变成视频、seedance-video
---

# seedance-video Skill

以**本地参考图 + 提示词**生成视频。区别于 `meai-creator`(那是 ME AI 平台, 图片需 HTTP URL), 本 skill 走 `shiping.djpsd.com` 平台, **原生支持本地图片上传**, 且**内置"缓慢运动"审美默认**。

## 环境要求

- Python 3.8+
- `httpx`(已随项目使用)
- API Key: 写在本 skill 目录下 `.env` 的 `SHIPING_API_KEY=xxx`(或环境变量同名)

## 脚本位置

`scripts/seedance_api.py` —— 核心 CLI, 子命令: `video` / `image` / `models` / `status` / `retry`

## 功能一览

| 功能 | 命令 | 模型 |
|------|------|------|
| 图生视频(主) | `... video --prompt "..." --image 本地图` | video-v1 |
| 文生视频 | `... video --prompt "..."` (不带 --image) | video-v1 |
| 多参考图视频 | `... video --prompt "..." --image a.jpg --image b.jpg` | video-v1 |
| 图生图 | `... image --prompt "..." --image 本地图` | image-v1-2k |
| 查模型 | `... models` | — |
| 查状态 | `... status --task-id N` | — |
| 重试失败 | `... retry --task-id N` | — |

## 使用流程

> 以下 `SCRIPT` = `D:\zed horse\.claude\skills\seedance-video\scripts\seedance_api.py`

### 1. 图生视频(核心: 传入本地参考图)

```bash
python "SCRIPT" video \
  --prompt "湖面上小船随微波轻轻起伏, 晨雾弥漫" \
  --image "D:\path\to\ref.jpg" \
  --duration 15 \
  --ratio 16:9 \
  --output ".\out.mp4"
```

`--image` 自动上传到平台再建任务; 也支持 http URL(直接用)。多图用多个 `--image` 或逗号分隔。

### 2. 文生视频(无参考图)

```bash
python "SCRIPT" video --prompt "雪山脚下的湖泊, 云影缓慢掠过水面" --duration 10
```

### 3. 先 dry-run 检查 payload(省积分, 推荐)

```bash
python "SCRIPT" video --prompt "..." --image "ref.jpg" --duration 5 --dry-run
```

### 4. 查询 / 重试

```bash
python "SCRIPT" status --task-id 123
python "SCRIPT" retry  --task-id 123
```

## 参数说明

### video 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--prompt` | 必填 | 文本描述 |
| `--image` | 无 | 参考图, 本地路径或 http URL, 可重复/逗号分隔 |
| `--duration` | **15** | 时长(秒), 推荐 5/10/15 |
| `--ratio` | **16:9** | 宽高比, 如 16:9 / 9:16 / 1:1 |
| `--model` | video-v1 | 模型 ID |
| `--calm` / `--no-calm` | **开** | 自动补"缓慢/近乎静止"修饰(见下) |
| `--output` | seedance_{task_id}.mp4 | 输出路径 |
| `--dry-run` | 关 | 只打印 payload 不提交 |

## 慢节奏提示词指南(内置审美)

本 skill **默认开启 `--calm`**: 若 `--prompt` 未含任何运动/节奏词, 脚本会自动追加

> 缓慢、近乎静止、静谧氛围、镜头缓缓推进、无快速运动

以确保生成结果符合**"运动必须缓慢/近乎静止, 禁止快移"**的审美(船不能像公路汽车那样飞驰)。调用时:
- 想要更精确控制, 自己在 prompt 里写明运动方式(脚本检测到运动词就不会重复追加)
- 确要快节奏, 加 `--no-calm` 并在 prompt 里写清

**提示词书写要点**: 主体几乎不动 + 环境的缓慢变化(光影、水波、云、雾、风) + 电影感运镜(缓缓推/摇/拉)。

## 模型映射说明

该平台当前视频模型 ID 为 **`video-v1`**(即 seedance 级后端, 用户口中的 "seedance 2")。脚本默认 `video-v1`。可用 `models` 命令查 `GET /v1/models` 实际列表; 若日后出现 seedance 专属 ID, 用 `--model` 覆盖即可。

## 注意事项

1. **⚠️ 真实人脸不可作参考图**: Seedance 2.0 出于肖像保护, **拒绝真实人脸素材**作参考(任务会 failed, 报"出于肖像保护考虑, Seedance 2.0 暂不支持上传真实人脸素材")。人物视频请改用**文生视频**(不带 `--image`)或换非人脸参考图。实测已确认 video-v1 后端即 **Seedance 2.0**。
2. **异步轮询**: 建任务后自动轮询(首查 10s, 之后每 15s, 最长 ~10 分钟超时), 成功自动下载
3. **URL 兼容**: 结果地址可能是相对路径(脚本自动拼平台域名)或带 http 的全链接, 已自动判断
4. **结果时效**: 平台缓存约 24 小时, 生成后及时取用本地 `--output`
5. **扣费**: 5s≈7 积分; 内容审核失败仍扣费, prompt 避免违规敏感内容
6. **去水印**: 优先下载 `video_url`(去水印地址), 回退 `result_url`

## 当用户请求时

1. 判断要生成什么: 图片变视频 → `video`(带 `--image`); 纯文字 → `video`(不带 `--image`)
2. **默认用慢节奏**: 直接写好静谧的 prompt, 让 `--calm` 兜底; duration 默认 15、ratio 默认 16:9
3. 不确定参数是否正确时, 先 `--dry-run` 看 payload
4. 用 `python` 运行 `seedance_api.py` 对应子命令, 等轮询完成展示结果, 告知输出文件位置
5. 失败时读 `error`, 用 `retry --task-id` 重试

如果用户说"把这张图变成视频"/"用这张图做视频" → 用图生视频(`video --image`)。
如果只说"生成一段...的视频" → 用文生视频(`video`, 无 `--image`)。
