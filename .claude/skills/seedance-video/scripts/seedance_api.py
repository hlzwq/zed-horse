#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seedance-video skill 核心 CLI
平台: https://shiping.djpsd.com/  (视频模型 video-v1 = seedance 级后端)
功能: 本地参考图上传 + 提示词 → 视频(图生视频), 附带文生视频 / 图生图 / 查模型 / 查状态 / 重试
蓝本: D:\\zed horse\\src\\测试apikey.py
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import httpx

# Windows 控制台默认 GBK, 强制 stdout/stderr 用 UTF-8, 避免中文乱码
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_URL = "https://shiping.djpsd.com/"
SKILL_DIR = Path(__file__).resolve().parent.parent  # .claude/skills/seedance-video/
ENV_FILE = SKILL_DIR / ".env"

DEFAULT_MODEL_VIDEO = "video-v1"
DEFAULT_MODEL_IMAGE = "image-v1-2k"

# 慢节奏静谧修饰 —— 内置用户审美偏好([[video-motion-pace-preference]])
CALM_SUFFIX = "缓慢、近乎静止、静谧氛围、镜头缓缓推进、无快速运动"
# 运动关键词 —— prompt 已含则不重复追加慢节奏修饰
MOTION_KEYWORDS = [
    "缓慢", "慢", "静止", "静静", "缓缓", "慢慢", "轻微", "微微", "渐渐",
    "calm", "slow", "still", "gentle", "gradual", "cinematic",
]


# ============ 配置 / 鉴权 ============

def load_api_key():
    """读 key 顺序: 环境变量 SHIPING_API_KEY > skill 目录 .env"""
    key = os.environ.get("SHIPING_API_KEY", "").strip()
    if key:
        return key
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == "SHIPING_API_KEY":
                v = v.strip().strip('"').strip("'")
                if v:
                    return v
    sys.exit(f"[错误] 未找到 API Key。请在环境变量 SHIPING_API_KEY 或\n  {ENV_FILE}\n中配置。")


def auth_headers(key):
    return {"Authorization": f"Bearer {key}"}


# ============ 提示词增强(内置慢节奏) ============

def enhance_prompt(prompt, calm):
    if not calm:
        return prompt
    low = prompt.lower()
    if any(kw in prompt or kw in low for kw in MOTION_KEYWORDS):
        return prompt  # 已含运动/节奏描述, 尊重用户原意
    return f"{prompt}。{CALM_SUFFIX}"


# ============ 图片处理 ============

def upload_image(client, key, image_path):
    """上传本地图片, 返回平台相对 URL。蓝本: 中转上传参考图列表"""
    p = Path(image_path)
    if not p.exists():
        sys.exit(f"[错误] 图片不存在: {image_path}")
    suffix = p.suffix.lower()
    if suffix == ".png":
        mime = "image/png"
    else:
        mime = "image/jpeg"  # .jpg/.jpeg 及其它一律按 jpeg
    with p.open("rb") as fp:
        files = {"file": (p.name, fp, mime)}
        resp = client.post(f"{BASE_URL}v1/media/upload", files=files, headers=auth_headers(key))
    data = _parse(resp, f"上传参考图 {p.name}")
    url = data.get("url") or ""
    if not url:
        sys.exit(f"[错误] 上传失败, 响应: {data}")
    return url


def resolve_images(client, key, image_args):
    """混合处理本地路径与 http URL, 返回平台 images 数组"""
    urls = []
    for item in image_args:
        for one in item.split(","):
            one = one.strip()
            if not one:
                continue
            if one.lower().startswith(("http://", "https://")):
                urls.append(one)
            else:
                print(f"[上传] {one}")
                urls.append(upload_image(client, key, one))
    return urls


# ============ 任务创建 / 轮询 / 下载 ============

def create_task(client, key, payload):
    resp = client.post(f"{BASE_URL}v1/media/generate", json=payload, headers=auth_headers(key))
    data = _parse(resp, "创建任务")
    task_id = data.get("task_id")
    if task_id is None:
        sys.exit(f"[错误] 创建任务失败, 响应: {data}")
    return task_id


def poll_status(client, key, task_id, timeout=600, first_wait=10, interval=15):
    """轮询任务状态, 仅用 state + is_final 判断(文档第八节)。返回最终状态 dict"""
    deadline = time.time() + timeout
    time.sleep(first_wait)
    last = {}
    while time.time() < deadline:
        resp = client.get(f"{BASE_URL}v1/media/status",
                          params={"task_id": task_id}, headers=auth_headers(key))
        data = _parse(resp, f"查询任务 {task_id}", exit_on_error=False)
        if not data:
            time.sleep(interval)
            continue
        last = data
        state = data.get("state", "")
        progress = data.get("progress", "")
        status_cn = data.get("status", "")
        print(f"[轮询] state={state}  progress={progress}  ({status_cn})")
        if data.get("is_final"):
            return data
        time.sleep(interval)
    sys.exit(f"[超时] 任务 {task_id} 在 {timeout}s 内未完成。最后状态: {last}")


def download(client, url, output):
    if not url:
        sys.exit("[错误] 无可下载的结果 URL(任务未成功?)")
    # 文档注明 result_url 后期可能由相对路径改为带 http 的全链接, 需判断后再下载
    if not url.lower().startswith(("http://", "https://")):
        url = BASE_URL.rstrip("/") + "/" + url.lstrip("/")
    print(f"[下载] {url}")
    with client.stream("GET", url) as r:
        r.raise_for_status()
        with open(output, "wb") as f:
            for chunk in r.iter_bytes():
                f.write(chunk)
    print(f"[完成] 已保存: {output}")


def _parse(resp, title, exit_on_error=True):
    print(f"\n=== {title} ===")
    print(f"status={resp.status_code}")
    try:
        data = resp.json()
    except Exception:
        print(resp.text[:500])
        if exit_on_error:
            sys.exit(1)
        return {}
    print(json.dumps(data, ensure_ascii=False, indent=2))
    if resp.status_code >= 400:
        detail = data.get("detail") if isinstance(data, dict) else None
        msg = f"[错误] HTTP {resp.status_code}: {detail or data}"
        if exit_on_error:
            sys.exit(msg)
        print(msg)
        return {}
    return data


# ============ 子命令 ============

def cmd_video(args):
    prompt = enhance_prompt(args.prompt, args.calm)
    if args.dry_run:
        # dry-run: 不上传、不建任务、不需要 key —— 仅检查 payload 结构
        images = []
        for item in args.image:
            for one in item.split(","):
                one = one.strip()
                if not one:
                    continue
                if one.lower().startswith(("http://", "https://")):
                    images.append(one)
                else:
                    images.append(f"[本地未上传] {one}")
        payload = {
            "model": args.model,
            "prompt": prompt,
            "params": {
                "duration": args.duration,
                "aspect_ratio": args.ratio,
                "images": images,
            },
        }
        print("\n[Payload (dry-run, 参考图未实际上传)]")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print("\n[dry-run] 未提交任务。去掉 --dry-run 真正生成。")
        return
    key = load_api_key()
    with httpx.Client(timeout=30) as client:
        images = resolve_images(client, key, args.image)
        payload = {
            "model": args.model,
            "prompt": prompt,
            "params": {
                "duration": args.duration,
                "aspect_ratio": args.ratio,
                "images": images,
            },
        }
        print("\n[Payload]")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        task_id = create_task(client, key, payload)
        print(f"\n[任务] task_id={task_id}")
        final = poll_status(client, key, task_id)
        if final.get("state") == "success":
            url = final.get("video_url") or final.get("result_url")  # video_url 为去水印地址, 优先
            out = args.output or f"seedance_{task_id}.mp4"
            with httpx.Client(timeout=300) as dl:  # 下载单独长超时
                download(dl, url, out)
        else:
            err = final.get("error", "")
            print(f"\n[失败] {err}")
            print(f"可用重试:  python {sys.argv[0]} retry --task-id {task_id}")
            sys.exit(1)


def cmd_image(args):
    key = load_api_key()
    with httpx.Client(timeout=30) as client:
        images = resolve_images(client, key, args.image)
        payload = {
            "model": args.model,
            "prompt": args.prompt,
            "params": {"aspect_ratio": args.ratio, "images": images},
        }
        print("\n[Payload]")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        task_id = create_task(client, key, payload)
        print(f"\n[任务] task_id={task_id}")
        final = poll_status(client, key, task_id)
        if final.get("state") == "success":
            url = final.get("result_url")
            out = args.output or f"seedance_{task_id}.png"
            with httpx.Client(timeout=300) as dl:
                download(dl, url, out)
        else:
            print(f"\n[失败] {final.get('error', '')}")
            sys.exit(1)


def cmd_models(args):
    key = load_api_key()
    with httpx.Client(timeout=30) as client:
        resp = client.get(f"{BASE_URL}v1/models", headers=auth_headers(key))
        data = _parse(resp, "模型列表")
        for m in data.get("data", []):
            print(f"- {m.get('id')}\t{m.get('type')}\t{m.get('display_name', '')}")


def cmd_status(args):
    key = load_api_key()
    with httpx.Client(timeout=30) as client:
        resp = client.get(f"{BASE_URL}v1/media/status",
                          params={"task_id": args.task_id}, headers=auth_headers(key))
        _parse(resp, f"查询任务 {args.task_id}")


def cmd_retry(args):
    key = load_api_key()
    with httpx.Client(timeout=30) as client:
        resp = client.post(f"{BASE_URL}v1/media/retry",
                           json={"task_id": args.task_id}, headers=auth_headers(key))
        _parse(resp, f"重试任务 {args.task_id}")
        print(f"\n继续查询:  python {sys.argv[0]} status --task-id {args.task_id}")


# ============ argparse ============

def build_parser():
    p = argparse.ArgumentParser(
        prog="seedance_api.py",
        description="seedance-video: 本地参考图 + 提示词 → 视频  (shiping.djpsd.com / video-v1)",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    pv = sub.add_parser("video", help="图生/文生视频 (主命令)")
    pv.add_argument("--prompt", required=True, help="文本描述")
    pv.add_argument("--image", action="append", default=[],
                    help="参考图, 本地路径或 http URL, 可重复 / 逗号分隔")
    pv.add_argument("--duration", type=int, default=15, help="时长(秒), 推荐 5/10/15")
    pv.add_argument("--ratio", default="16:9", help="宽高比, 如 16:9 / 9:16 / 1:1")
    pv.add_argument("--model", default=DEFAULT_MODEL_VIDEO, help="模型 ID")
    pv.add_argument("--calm", dest="calm", action="store_true", default=True,
                    help="自动补慢节奏修饰(默认开, 符合静谧审美)")
    pv.add_argument("--no-calm", dest="calm", action="store_false", help="关闭慢节奏修饰")
    pv.add_argument("--output", help="输出路径, 默认 seedance_{task_id}.mp4")
    pv.add_argument("--dry-run", action="store_true", help="只打印 payload 不提交")
    pv.set_defaults(func=cmd_video)

    pi = sub.add_parser("image", help="图生/文生图")
    pi.add_argument("--prompt", required=True)
    pi.add_argument("--image", action="append", default=[])
    pi.add_argument("--ratio", default="16:9")
    pi.add_argument("--model", default=DEFAULT_MODEL_IMAGE, help="image-v1 / image-v1-2k / image-v1-4k")
    pi.add_argument("--output")
    pi.set_defaults(func=cmd_image)

    pm = sub.add_parser("models", help="列出可用模型")
    pm.set_defaults(func=cmd_models)

    ps = sub.add_parser("status", help="查询单个任务状态")
    ps.add_argument("--task-id", required=True, type=int)
    ps.set_defaults(func=cmd_status)

    pr = sub.add_parser("retry", help="重试失败任务")
    pr.add_argument("--task-id", required=True, type=int)
    pr.set_defaults(func=cmd_retry)

    return p


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
