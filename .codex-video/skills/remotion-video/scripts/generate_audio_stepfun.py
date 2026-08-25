#!/usr/bin/env python3
"""
StepFun Step Audio 2.5 TTS (Contextual TTS) -- non-streaming.

Unique capabilities vs other TTS scripts in this skill:
  - Global `instruction` (max 200 chars) sets the overall tone.
  - Inline `()` in the scene text becomes a per-phrase directing note
    (emotion, pause, breath) and is NOT spoken.
  - Voice cloning: pass a cloned voice id via STEP_VOICE_ID.

API:  POST https://api.stepfun.com/v1/audio/speech
Auth: env STEP_API_KEY  (required)
Voice: env STEP_VOICE_ID (optional, default: cixingnansheng)
Model: env STEP_MODEL (default: stepaudio-2.5-tts)

Per-scene `instruction` overrides DEFAULT_INSTRUCTION.
Run from the project root. Resume is automatic (existing files are skipped).
After generation, src/audioConfig.ts is rewritten with measured durations.

Usage:
    export STEP_API_KEY=...
    export STEP_VOICE_ID=...           # optional
    python scripts/generate_audio_stepfun.py
"""

import os
import sys
import time
import json
import requests
import subprocess
from pathlib import Path

# Hardcoded for local testing. Override by setting STEP_API_KEY in the environment.
API_KEY = os.environ.get("STEP_API_KEY") or "58Qtik5K5LO9ZSV4GrHf6gdkiYHWoZPw6vCZJFQfDdr0w0XSQVA5Bq5bdUicnvrPy"
VOICE_ID = os.environ.get("STEP_VOICE_ID", "cixingnansheng")
MODEL = os.environ.get("STEP_MODEL", "stepaudio-2.5-tts")
API_URL = "https://api.stepfun.com/v1/audio/speech"
SAMPLE_RATE = 24000  # 8000 / 16000 / 22050 / 24000 / 48000
FPS = 30

if not API_KEY:
    print("ERROR: please set STEP_API_KEY in your environment.")
    print("       Get a key at https://platform.stepfun.com")
    sys.exit(1)

# Fallback instruction when a scene does not specify one.
# 200-char limit for stepaudio-2.5-tts; ignored for other models.
DEFAULT_INSTRUCTION = ""  # e.g. "语气专业，节奏平稳"

# Per-scene config. `text` may contain () inline direction (e.g.
# "（压低声音）嗨，你好。" -- the part
# inside () is not spoken).  Optional `instruction` overrides the default.
SCENES = [
    {"id": "01-intro",   "title": "开场",         "text": "欢迎观看本期视频。"},
    {"id": "02-concept", "title": "核心概念", "text": "今天我们来讲..."},
    {"id": "03-demo",    "title": "演示",         "text": "让我们看一个例子。"},
    {"id": "04-summary", "title": "总结",         "text": "感谢观看，下期见！"},
]

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "public" / "audio"
CONFIG_FILE = Path(__file__).resolve().parent.parent / "src" / "audioConfig.ts"


def ffprobe_duration(path: Path) -> float:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, timeout=10,
        )
        return float(r.stdout.strip()) if r.stdout.strip() else 0.0
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        return 0.0


def generate(scene: dict) -> tuple[Path, float]:
    text = scene["text"]
    if len(text) > 1000:
        print(f"  WARN: scene '{scene['id']}' is {len(text)} chars, truncating to 1000")
        text = text[:1000]

    instruction = scene.get("instruction") or DEFAULT_INSTRUCTION
    if len(instruction) > 200:
        print(f"  WARN: instruction for '{scene['id']}' truncated to 200 chars")
        instruction = instruction[:200]

    payload = {
        "model": MODEL,
        "input": text,
        "voice": VOICE_ID,
        "response_format": "mp3",
        "sample_rate": SAMPLE_RATE,
    }
    # `instruction` is only valid for stepaudio-2.5-tts -- other models error on it.
    if MODEL == "stepaudio-2.5-tts" and instruction:
        payload["instruction"] = instruction

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    last_err = None
    for attempt in range(3):
        try:
            r = requests.post(API_URL, json=payload, headers=headers, timeout=120)
            if r.status_code == 429 or r.status_code >= 500:
                raise RuntimeError(f"transient HTTP {r.status_code}: {r.text[:200]}")
            if r.status_code >= 400:
                # 4xx (non-429) is not retriable
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
            out = OUTPUT_DIR / f"{scene['id']}.mp3"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(r.content)
            dur = ffprobe_duration(out)
            if dur <= 0:
                # Fallback estimate: ~4.5 chars/sec for Chinese narration
                dur = max(0.5, len(text) / 4.5)
            return out, dur
        except Exception as e:
            last_err = e
            wait = 2 ** attempt
            print(f"  attempt {attempt+1} failed: {e}; retry in {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"failed after 3 attempts: {last_err}")


def write_config(scenes_with_dur: list[dict]) -> None:
    # Build line by line -- NEVER use ",\n".join() inside an f-string.
    lines = [
        "// Auto-generated by scripts/generate_audio_stepfun.py -- do not hand-edit durations.",
        "export interface SceneConfig {",
        "  id: string;",
        "  title: string;",
        "  durationInFrames: number;",
        "  audioFile: string;",
        "}",
        "",
        "export const SCENES: SceneConfig[] = [",
    ]
    for s in scenes_with_dur:
        title_json = json.dumps(s["title"], ensure_ascii=False)  # safe string escaping
        lines.append(
            f'  {{ id: {json.dumps(s["id"])}, '
            f'title: {title_json}, '
            f'durationInFrames: {s["frames"]}, '
            f'audioFile: {json.dumps(s["id"] + ".mp3")} }},'
        )
    lines.append("];")
    lines.append("")
    lines.append("export const getSceneStart = (i: number): number =>")
    lines.append("  SCENES.slice(0, i).reduce((sum, s) => sum + s.durationInFrames, 0);")
    lines.append("")
    lines.append("export const TOTAL_FRAMES = SCENES.reduce((sum, s) => sum + s.durationInFrames, 0) + 60;")
    lines.append(f"export const FPS = {FPS};")
    lines.append("")
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote {CONFIG_FILE}")


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"model={MODEL} voice={VOICE_ID}")
    results = []
    for s in SCENES:
        out = OUTPUT_DIR / f"{s['id']}.mp3"
        if out.exists() and out.stat().st_size > 0:
            dur = ffprobe_duration(out)
            print(f"[skip] {s['id']}  ({dur:.2f}s, {out.stat().st_size} bytes)")
        else:
            print(f"[gen ] {s['id']} ...", end="", flush=True)
            try:
                _, dur = generate(s)
                print(f" done ({dur:.2f}s)")
            except Exception as e:
                print(f" FAILED: {e}")
                return 1
        results.append({**s, "frames": max(30, int(round(dur * FPS)))})
    write_config(results)
    print(f"all done. {len(results)} scenes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
