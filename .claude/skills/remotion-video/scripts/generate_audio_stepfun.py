#!/usr/bin/env python3
"""
StepFun StepAudio 2.5 TTS 音频生成脚本

特性：
- 使用阶跃星辰 StepAudio 2.5 TTS API
- 支持 35 种音色（含中英文）
- 支持全局语气指令 (instruction) 和行内情感控制
- 断点续作：已存在的音频文件自动跳过
- 自动更新 Remotion 配置文件

用法：
    python scripts/generate_audio_stepfun.py

环境变量：
    STEP_API_KEY: 阶跃星辰 API 密钥

依赖：
    pip install requests
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

# ──────────────────────────────────────────────
# 配置
# ──────────────────────────────────────────────

API_KEY = os.environ.get("STEP_API_KEY")

if not API_KEY:
    print("❌ 错误: 请设置 STEP_API_KEY 环境变量")
    print("   export STEP_API_KEY=\"your-api-key\"")
    sys.exit(1)

# API 端点
API_URL = "https://api.stepfun.com/v1/audio/speech"

# 模型
MODEL = "stepaudio-2.5-tts"

# 默认音色（可在场景中覆盖）
DEFAULT_VOICE = "cixingnansheng"  # 磁性男声

# 默认全局语气指令
DEFAULT_INSTRUCTION = "语气自然，语速适中，适合教程讲解"

# 推荐音色速查
# ┌─────────────────────────┬──────────────┬──────┬──────────────────────────────┐
# │ voice_id                │ 名称         │ 性别 │ 适合场景                     │
# ├─────────────────────────┼──────────────┼──────┼──────────────────────────────┤
# │ cixingnansheng          │ 磁性男声     │ 男   │ 有声书、情感陪伴             │
# │ boyinnansheng           │ 播音男声     │ 男   │ 有声书、旁白（专业播音腔）   │
# │ zixinnansheng           │ 自信男声     │ 男   │ 有声书、教育、营销           │
# │ wenrounansheng          │ 温柔男声     │ 男   │ 旁白、情感陪伴、客服         │
# │ yuanqinansheng          │ 元气男声     │ 男   │ 有声书、旁白                 │
# │ ruyananshi              │ 儒雅男士     │ 男   │ 有声书、旁白、语音助手       │
# │ shenchennanyin          │ 深沉男音     │ 男   │ 情感陪伴、有声书             │
# │ vibrant-youth           │ Vibrant Youth│ 男   │ 英文有声书、视频配音         │
# │ magnetic-voiced-male    │ 磁性男声EN   │ 男   │ 英文有声书、视频配音         │
# │ elegantgentle-female    │ 气质温婉     │ 女   │ 客服、旁白、教育             │
# │ livelybreezy-female     │ 活力轻快     │ 女   │ 情感陪伴、客服、教育、营销   │
# │ jingdiannvsheng         │ 经典女声     │ 女   │ 客服、情感陪伴               │
# │ tianmeinvsheng          │ 甜美女声     │ 女   │ 情感陪伴、客服               │
# │ linjiajiejie            │ 邻家姐姐     │ 女   │ 旁白、语音助手、视频配音     │
# │ ruanmengnvsheng         │ 软萌女声     │ 女   │ 情感陪伴、语音助手、视频配音 │
# │ youyanvsheng            │ 优雅女声     │ 女   │ 视频配音                     │
# └─────────────────────────┴──────────────┴──────┴──────────────────────────────┘

# 场景配置
# 每个场景包含:
#   id:           场景标识
#   title:        场景标题
#   text:         合成文本（支持行内指令，用括号包裹，不会被朗读）
#   voice:        可选，覆盖默认音色
#   instruction:  可选，覆盖默认全局语气
SCENES = [
    {
        "id": "01-intro",
        "title": "开场",
        "text": "（热情）欢迎来到本期视频！今天我们要聊一个非常有趣的话题。",
        "instruction": "热情洋溢，语速稍快，像朋友打招呼",
    },
    {
        "id": "02-content",
        "title": "正文",
        "text": "（沉稳）让我们先从基础概念讲起。（停顿）请看这个例子。",
        "instruction": "沉稳专业，语速适中，适合教学讲解",
    },
    {
        "id": "03-summary",
        "title": "总结",
        "text": "（温和）好的，今天的内容就到这里。（微笑）如果觉得有帮助，别忘了点赞关注。我们下期见！",
        "instruction": "温和亲切，结尾稍慢，带感谢感",
    },
]

# 输出目录
OUTPUT_DIR = Path(__file__).parent.parent / "public" / "audio"

# Remotion 配置文件
CONFIG_FILE = Path(__file__).parent.parent / "src" / "audioConfig.ts"

# 帧率
FPS = 30


# ──────────────────────────────────────────────
# 核心函数
# ──────────────────────────────────────────────

def get_audio_duration(file_path: Path) -> float:
    """用 ffprobe 获取音频时长（秒）"""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(file_path),
            ],
            capture_output=True, text=True, timeout=10,
        )
        return float(result.stdout.strip()) if result.stdout.strip() else 0
    except (subprocess.TimeoutExpired, ValueError):
        return 0


def generate_audio(scene: dict) -> dict:
    """调用 StepFun TTS API 生成音频"""
    voice = scene.get("voice", DEFAULT_VOICE)
    instruction = scene.get("instruction", DEFAULT_INSTRUCTION)
    text = scene["text"]

    # 检查文本长度（API 限制 1000 字符）
    if len(text) > 1000:
        print(f"⚠️  文本超过 1000 字符（{len(text)}），将被截断")
        text = text[:1000]

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "voice": voice,
        "input": text,
        "instruction": instruction[:200],  # API 限制 200 字符
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=120)

    if response.status_code != 200:
        error_msg = response.text[:200]
        raise Exception(f"API 返回 {response.status_code}: {error_msg}")

    # 检查是否返回了音频数据
    content_type = response.headers.get("content-type", "")
    if "audio" not in content_type and len(response.content) < 1000:
        raise Exception(f"API 未返回音频数据: {response.text[:200]}")

    # 保存音频文件
    output_file = OUTPUT_DIR / f"{scene['id']}.mp3"
    output_file.write_bytes(response.content)

    # 获取时长
    duration = get_audio_duration(output_file)
    frames = round(duration * FPS)

    return {
        "id": scene["id"],
        "title": scene.get("title", scene["id"]),
        "file": f"{scene['id']}.mp3",
        "duration": duration,
        "frames": frames,
    }


def update_config(results: list):
    """更新 audioConfig.ts"""
    scenes_lines = []
    for r in results:
        scene_block = f'''  {{
    id: "{r['id']}",
    title: "{r['title']}",
    durationInFrames: {r['frames']},
    audioFile: "{r['file']}",
  }}'''
        scenes_lines.append(scene_block)

    scenes_content = ",\n".join(scenes_lines)

    content = f'''// 场景配置（StepFun TTS 生成）
// 自动生成，请勿手动修改

export interface SceneConfig {{
  id: string;
  title: string;
  durationInFrames: number;
  audioFile: string;
}}

export const SCENES: SceneConfig[] = [
{scenes_content},
];

// 计算场景起始帧
export function getSceneStart(sceneIndex: number): number {{
  return SCENES.slice(0, sceneIndex).reduce((sum, s) => sum + s.durationInFrames, 0);
}}

// 总帧数（加上片头片尾缓冲）
export const TOTAL_FRAMES = SCENES.reduce((sum, s) => sum + s.durationInFrames, 0) + 60;

// 帧率
export const FPS = {FPS};
'''
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(content)


# ──────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"🎙️  StepFun StepAudio 2.5 TTS")
    print(f"🔊  默认音色: {DEFAULT_VOICE}")
    print(f"📁  输出目录: {OUTPUT_DIR}")
    print(f"📝  场景数量: {len(SCENES)}")
    print("=" * 60)

    results = []
    skipped = 0
    generated = 0

    for i, scene in enumerate(SCENES, 1):
        output_file = OUTPUT_DIR / f"{scene['id']}.mp3"
        prefix = f"[{i}/{len(SCENES)}] {scene['id']}"

        # 断点续作：跳过已存在的文件
        if output_file.exists() and output_file.stat().st_size > 0:
            duration = get_audio_duration(output_file)
            frames = round(duration * FPS)
            results.append({
                "id": scene["id"],
                "title": scene.get("title", scene["id"]),
                "file": f"{scene['id']}.mp3",
                "duration": duration,
                "frames": frames,
            })
            print(f"{prefix}: ⏭️  已存在，跳过 ({duration:.2f}s)")
            skipped += 1
            continue

        # 生成音频
        voice = scene.get("voice", DEFAULT_VOICE)
        print(f"{prefix}: 生成中 (音色: {voice})...", end=" ", flush=True)
        try:
            result = generate_audio(scene)
            results.append(result)
            print(f"✅ {result['duration']:.2f}s ({result['frames']} frames)")
            generated += 1
        except Exception as e:
            print(f"❌ {e}")
            print("\n⚠️  生成中断，已完成的音频已保存，可重新运行继续")
            sys.exit(1)

    print("=" * 60)
    print(f"✅ 完成: {generated} 新生成, {skipped} 跳过")

    # 更新 audioConfig.ts
    update_config(results)
    print(f"📝 audioConfig.ts 已更新")

    # 输出摘要
    total_duration = sum(r["duration"] for r in results)
    total_frames = sum(r["frames"] for r in results)
    print(f"⏱️  总时长: {total_duration:.1f}s ({total_frames} frames @ {FPS}fps)")


if __name__ == "__main__":
    main()
