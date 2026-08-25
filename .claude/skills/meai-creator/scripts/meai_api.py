#!/usr/bin/env python3
"""
ME AI 图片视频 API 调用工具
支持：文生图、图生图、文生视频、图生视频、首尾帧视频、参考生视频

环境变量：
  MEAI_API_KEY — API Key (sk-xxxx 格式)
  MEAI_BASE_URL — 可选，默认 https://api.meai.cloud
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
import ssl

# Windows 终端 UTF-8 支持
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── 配置 ──────────────────────────────────────────────
BASE_URL = os.environ.get("MEAI_BASE_URL", "https://api.meai.cloud")
API_KEY = os.environ.get("MEAI_API_KEY", "")
POLL_INTERVAL = 20  # 秒
MAX_POLL_TIME = 600  # 最长等待 10 分钟

# 忽略 SSL 验证（某些网络环境需要）
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE


def api_request(method, path, body=None):
    """发送 API 请求"""
    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"✗ HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"✗ 网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)


def download_file(url, output_path):
    """下载文件到本地"""
    print(f"⬇ 下载中: {url}")
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=120) as resp:
        with open(output_path, "wb") as f:
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                f.write(chunk)
    print(f"✓ 已保存: {output_path}")


def poll_task(task_type, task_id):
    """轮询异步任务状态"""
    path_prefix = "/v1/images" if task_type == "image" else "/v1/videos"
    start = time.time()

    while True:
        elapsed = time.time() - start
        if elapsed > MAX_POLL_TIME:
            print(f"✗ 超时（已等待 {int(elapsed)} 秒）", file=sys.stderr)
            sys.exit(1)

        result = api_request("GET", f"{path_prefix}/{task_id}")
        status = result.get("status", "")

        if status == "SUCCEEDED":
            print(f"✓ 生成完成（耗时 {int(elapsed)} 秒）")
            return result.get("object", "")
        elif status == "FAILED" or status.startswith("FAILED"):
            print(f"✗ 生成失败: {status}", file=sys.stderr)
            sys.exit(1)
        else:
            progress = result.get("progress", "")
            prog_str = f" ({progress}%)" if progress else ""
            print(f"⏳ 状态: {status}{prog_str}，已等待 {int(elapsed)}s...")
            time.sleep(POLL_INTERVAL)


# ── 图片生成 ──────────────────────────────────────────
def generate_image(args):
    """文生图 / 图生图"""
    content = [{"text": args.prompt}]
    if args.image:
        content.insert(0, {"image": args.image})

    body = {
        "model": args.model,
        "input": {"messages": [{"role": "user", "content": content}]},
        "parameters": {
            "size": args.size,
            "n": args.n,
            "watermark": False,
            "thinking_mode": False,
        },
    }

    print(f"🎨 提交图片任务 (模型: {args.model})")
    result = api_request("POST", "/v1/images/generations/async", body)
    task_id = result.get("task_id") or result.get("id")
    print(f"📋 任务 ID: {task_id}")

    image_url = poll_task("image", task_id)
    if image_url:
        download_file(image_url, args.output)


# ── 视频生成 ──────────────────────────────────────────
def generate_video(args):
    """文生视频 / 图生视频 / 首尾帧视频 / 参考生视频"""
    input_data = {"prompt": args.prompt}
    media = []

    # 首帧
    if args.first_frame:
        media.append({"type": "first_frame", "url": args.first_frame})

    # 尾帧（仅 wan2.7）
    if args.last_frame:
        media.append({"type": "last_frame", "url": args.last_frame})

    # 参考图片
    if args.ref_images:
        for url in args.ref_images.split(","):
            url = url.strip()
            if url:
                media.append({"type": "reference_image", "url": url})

    if media:
        input_data["media"] = media

    params = {
        "resolution": args.resolution,
        "prompt_extend": args.prompt_extend,
        "watermark": False,
    }

    # ratio 只在非首尾帧模式下设置
    if not args.last_frame:
        params["ratio"] = args.ratio

    params["duration"] = args.duration

    body = {
        "model": args.model,
        "input": input_data,
        "parameters": params,
    }

    print(f"🎬 提交视频任务 (模型: {args.model})")
    result = api_request("POST", "/v1/videos", body)
    task_id = result.get("task_id") or result.get("id")
    print(f"📋 任务 ID: {task_id}")

    video_url = poll_task("video", task_id)
    if video_url:
        download_file(video_url, args.output)


# ── CLI ───────────────────────────────────────────────
def main():
    if not API_KEY:
        print("✗ 请设置环境变量 MEAI_API_KEY", file=sys.stderr)
        print("  Windows: set MEAI_API_KEY=sk-xxxx", file=sys.stderr)
        print("  Linux:   export MEAI_API_KEY=sk-xxxx", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="ME AI 图片视频生成工具")
    sub = parser.add_subparsers(dest="command", required=True)

    # ── image 子命令 ──
    img = sub.add_parser("image", help="生成图片")
    img.add_argument("--prompt", required=True, help="文本描述")
    img.add_argument("--image", help="图生图的源图片 URL")
    img.add_argument("--model", default="seedream-5.0", help="模型 (seedream-5.0 / seedream-4.5)")
    img.add_argument("--size", default="2048*2048", help="分辨率")
    img.add_argument("--n", type=int, default=1, help="生成数量")
    img.add_argument("--output", default="./meai_output.png", help="输出路径")

    # ── video 子命令 ──
    vid = sub.add_parser("video", help="生成视频")
    vid.add_argument("--prompt", required=True, help="文本描述")
    vid.add_argument("--first-frame", help="首帧图片 URL")
    vid.add_argument("--last-frame", help="尾帧图片 URL (仅 wan2.7)")
    vid.add_argument("--ref-images", help="参考图片 URL，逗号分隔")
    vid.add_argument("--model", default="seedance-2.0", help="模型 (seedance-2.0 / happyhorse-1.0 / wan2.7)")
    vid.add_argument("--resolution", default="1080P", help="分辨率")
    vid.add_argument("--ratio", default="16:9", help="宽高比")
    vid.add_argument("--duration", type=int, default=15, help="时长(秒)")
    vid.add_argument("--prompt-extend", action="store_true", help="扩展提示词")
    vid.add_argument("--output", default="./meai_output.mp4", help="输出路径")

    args = parser.parse_args()

    if args.command == "image":
        generate_image(args)
    elif args.command == "video":
        generate_video(args)


if __name__ == "__main__":
    main()
