---
name: media-processing
description: 使用 FFmpeg（视频/音频编码、转换、流媒体、过滤、硬件加速）和 ImageMagick（图像处理、格式转换、批处理、效果、合成）处理多媒体文件。在转换媒体格式、使用特定编解码器（H.264、H.265、VP9）编码视频、调整/裁剪图像、从视频中提取音频、应用过滤器和效果、优化文件大小、创建流媒体清单（HLS/DASH）、生成缩略图、批量处理图像、创建复合图像或实现媒体处理管道时使用。支持 100 多种格式、硬件加速（NVENC、QSV）和复杂的过滤图。
license: MIT
---

# 媒体处理 Skill

使用 FFmpeg 和 ImageMagick 命令行工具处理视频、音频和图像，以进行转换、优化、流媒体和操作任务。

## 何时使用此 Skill

在以下情况下使用：
- 转换媒体格式（视频、音频、图像）
- 使用编解码器编码视频（H.264、H.265、VP9、AV1）
- 处理图像（调整大小、裁剪、效果、水印）
- 从视频中提取音频
- 创建流媒体清单（HLS/DASH）
- 生成缩略图和预览
- 批量处理媒体文件
- 优化文件大小和质量
- 应用过滤器和效果
- 创建复合图像或视频

## 工具选择指南

### FFmpeg：视频/音频处理
使用 FFmpeg 进行：
- 视频编码、转换、转码
- 音频提取、转换、混合
- 直播流媒体（RTMP、HLS、DASH）
- 视频过滤器（缩放、裁剪、旋转、叠加）
- 硬件加速编码
- 媒体文件检查（ffprobe）
- 帧提取、拼接
- 编解码器选择和优化

### ImageMagick：图像处理
使用 ImageMagick 进行：
- 图像格式转换（PNG、JPEG、WebP、GIF）
- 调整大小、裁剪、变换
- 批量图像处理（mogrify）
- 视觉效果（模糊、锐化、怀旧）
- 文本叠加和水印
- 图像合成和蒙太奇
- 颜色调整、过滤器
- 缩略图生成

### 决策矩阵

| 任务 | 工具 | 原因 |
|------|------|-----|
| 视频编码 | FFmpeg | 原生视频编解码器支持 |
| 音频提取 | FFmpeg | 直接流操作 |
| 图像调整大小 | ImageMagick | 针对静态图像优化 |
| 批量图像 | ImageMagick | 使用 mogrify 进行就地编辑 |
| 视频缩略图 | FFmpeg | 内置帧提取 |
| GIF 创建 | FFmpeg 或 ImageMagick | FFmpeg 用于视频源，ImageMagick 用于图像 |
| 流媒体 | FFmpeg | 直播流媒体协议 |
| 图像效果 | ImageMagick | 丰富的过滤器库 |

## 安装

### macOS
```bash
brew install ffmpeg imagemagick
```

### Ubuntu/Debian
```bash
sudo apt-get install ffmpeg imagemagick
```

### Windows
```bash
# 使用 winget
winget install ffmpeg
winget install ImageMagick.ImageMagick

# 或下载二进制文件
# FFmpeg: https://ffmpeg.org/download.html
# ImageMagick: https://imagemagick.org/script/download.php
```

### 验证安装
```bash
ffmpeg -version
ffprobe -version
magick -version
# 或
convert -version
```

## 快速入门示例

### 视频转换
```bash
# 转换格式（复制流，快速）
ffmpeg -i input.mkv -c copy output.mp4

# 使用 H.264 重新编码
ffmpeg -i input.avi -c:v libx264 -crf 22 -c:a aac output.mp4

# 将视频调整为 720p
ffmpeg -i input.mp4 -vf scale=-1:720 -c:a copy output.mp4
```

### 音频提取
```bash
# 提取音频（不重新编码）
ffmpeg -i video.mp4 -vn -c:a copy audio.m4a

# 转换为 MP3
ffmpeg -i video.mp4 -vn -q:a 0 audio.mp3
```

### 图像处理
```bash
# 转换格式
magick input.png output.jpg

# 按比例调整大小
magick input.jpg -resize 800x600 output.jpg

# 创建正方形缩略图
magick input.jpg -resize 200x200^ -gravity center -extent 200x200 thumb.jpg
```

### 批量图像调整大小
```bash
# 将所有 JPEG 调整为 800px 宽
mogrify -resize 800x -quality 85 *.jpg

# 输出到单独目录
mogrify -path ./output -resize 800x600 *.jpg
```

### 视频缩略图
```bash
# 提取 5 秒处的帧
ffmpeg -ss 00:00:05 -i video.mp4 -vframes 1 -vf scale=320:-1 thumb.jpg
```

### HLS 流媒体
```bash
# 生成 HLS 播放列表
ffmpeg -i input.mp4 \
  -c:v libx264 -preset fast -crf 22 -g 48 \
  -c:a aac -b:a 128k \
  -f hls -hls_time 6 -hls_playlist_type vod \
  playlist.m3u8
```

### 图像水印
```bash
# 在角落添加水印
magick input.jpg watermark.png -gravity southeast \
  -geometry +10+10 -composite output.jpg
```

## 常见工作流程

### 优化视频以适应网络
```bash
# H.264 具有良好的压缩
ffmpeg -i input.mp4 \
  -c:v libx264 -preset slow -crf 23 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  output.mp4
```

### 创建响应式图像
```bash
# 生成多个尺寸
for size in 320 640 1024 1920; do
  magick input.jpg -resize ${size}x -quality 85 "output-${size}w.jpg"
done
```

### 提取视频片段
```bash
# 从 1:30 到 3:00（重新编码以确保精度）
ffmpeg -i input.mp4 -ss 00:01:30 -to 00:03:00 \
  -c:v libx264 -c:a aac output.mp4
```

### 批量图像优化
```bash
# 将 PNG 转换为优化的 JPEG
mogrify -path ./optimized -format jpg -quality 85 -strip *.png
```

### 视频 GIF 创建
```bash
# 高质量 GIF 生成调色板
ffmpeg -i input.mp4 -vf "fps=15,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

### 图像模糊效果
```bash
# 高斯模糊
magick input.jpg -gaussian-blur 0x8 output.jpg
```

## 高级技术

### 多遍视频编码
```bash
# 第 1 遍（分析）
ffmpeg -y -i input.mkv -c:v libx264 -b:v 2600k -pass 1 -an -f null /dev/null

# 第 2 遍（编码）
ffmpeg -i input.mkv -c:v libx264 -b:v 2600k -pass 2 -c:a aac output.mp4
```

### 硬件加速编码
```bash
# NVIDIA NVENC
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc -preset fast -crf 22 output.mp4

# Intel QuickSync
ffmpeg -hwaccel qsv -c:v h264_qsv -i input.mp4 -c:v h264_qsv output.mp4
```

### 复杂图像管道
```bash
# 调整大小、裁剪、边框、调整
magick input.jpg \
  -resize 1000x1000^ \
  -gravity center \
  -crop 1000x1000+0+0 +repage \
  -bordercolor black -border 5x5 \
  -brightness-contrast 5x10 \
  -quality 90 \
  output.jpg
```

### 视频过滤链
```bash
# 缩放、去噪、水印
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[0:v]scale=1280:720,hqdn3d[v];[v][1:v]overlay=10:10" \
  -c:a copy output.mp4
```

### 从图像创建动画 GIF
```bash
# 创建带延迟的 GIF
magick -delay 100 -loop 0 frame*.png animated.gif

# 优化大小
magick animated.gif -fuzz 5% -layers Optimize optimized.gif
```

## 媒体分析

### 检查视频属性
```bash
# 详细的 JSON 输出
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# 获取分辨率
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height \
  -of csv=s=x:p=0 input.mp4
```

### 图像信息
```bash
# 基本信息
identify image.jpg

# 详细格式
identify -verbose image.jpg

# 自定义格式
identify -format "%f: %wx%h %b\n" image.jpg
```

## 性能提示

1. **使用 CRF 进行质量控制** - 比比特率更好
2. **尽可能复制流** - 使用 `-c copy` 避免重新编码
3. **硬件加速** - GPU 编码速度快 5-10 倍
4. **适当的预设** - 平衡速度与压缩
5. **使用 mogrify 批量处理** - 就地图像处理
6. **剥离元数据** - 使用 `-strip` 减少文件大小
7. **渐进式 JPEG** - 使用 `-interlace Plane` 更好地加载网页
8. **限制内存** - 防止大批量处理时崩溃
9. **在样本上测试** - 在批量处理前验证设置
10. **并行处理** - 使用 GNU Parallel 处理多个文件

## 参考文档

`references/` 中的详细指南：

- **ffmpeg-encoding.md** - 视频/音频编解码器、质量优化、硬件加速
- **ffmpeg-streaming.md** - HLS/DASH、直播流媒体、自适应比特率
- **ffmpeg-filters.md** - 视频/音频过滤器、复杂过滤图
- **imagemagick-editing.md** - 格式转换、效果、变换
- **imagemagick-batch.md** - 批量处理、mogrify、并行操作
- **format-compatibility.md** - 格式支持、编解码器推荐

## 常见参数

### FFmpeg 视频
- `-c:v` - 视频编解码器（libx264、libx265、libvpx-vp9）
- `-crf` - 质量（0-51，数值越低越好，23=默认）
- `-preset` - 速度/压缩（ultrafast 到 veryslow）
- `-b:v` - 视频比特率（例如，2M、2500k）
- `-vf` - 视频过滤器

### FFmpeg 音频
- `-c:a` - 音频编解码器（aac、mp3、opus）
- `-b:a` - 音频比特率（例如，128k、192k）
- `-ar` - 采样率（44100、48000）

### ImageMagick 几何
- `800x600` - 适应范围内（保持比例）
- `800x600!` - 强制精确大小
- `800x600^` - 填充（可能裁剪）
- `800x` - 仅宽度
- `x600` - 仅高度
- `50%` - 缩放百分比

## 故障排除

**FFmpeg "未知编码器"**
```bash
# 检查可用编码器
ffmpeg -encoders | grep h264

# 安装编解码器库
sudo apt-get install libx264-dev libx265-dev
```

**ImageMagick "未授权"**
```bash
# 编辑策略文件
sudo nano /etc/ImageMagick-7/policy.xml
# 将 <policy domain="coder" rights="none" pattern="PDF" />
# 更改为 <policy domain="coder" rights="read|write" pattern="PDF" />
```

**内存错误**
```bash
# 限制内存使用
ffmpeg -threads 4 input.mp4 output.mp4
magick -limit memory 2GB -limit map 4GB input.jpg output.jpg
```

## 资源

- FFmpeg: https://ffmpeg.org/documentation.html
- FFmpeg Wiki: https://trac.ffmpeg.org/
- ImageMagick: https://imagemagick.org/
- ImageMagick 使用: https://imagemagick.org/Usage/