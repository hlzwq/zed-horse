#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
film-creator 拍摄编排器
读 screenplay.json → 逐幕生成(可选先生关键帧图) → ffmpeg 拼接成片。

设计要点:
- 生成环节委托兄弟 skill 的脚本(seedance-video / meai-creator), 本脚本只做编排, 不碰 API 细节
- 断点续跑: 已存在且 >10KB 的 scene 文件自动跳过(长任务每条即时落盘, 重跑跳过已完成)
- 单幕失败不终止: 跳过继续, 最后拼接成功幕(>=2 幕才拼)
- 拼接策略: 各幕编码参数一致 → concat 无损 copy; 不一致 → 统一重编码(scale+fps+去音轨, 默片)

用法:
  python shoot_film.py screenplay.json                     # 全流程
  python shoot_film.py screenplay.json --dry-run           # 只打印将执行的命令
  python shoot_film.py screenplay.json --assemble-only     # 只拼接已有 scene 文件
  python shoot_film.py screenplay.json --backend meai      # 切 ME AI 后端(纯文生视频)
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent  # .claude/skills/film-creator/
SEEDANCE_SCRIPT = SKILL_DIR.parent / "seedance-video" / "scripts" / "seedance_api.py"
MEAI_SCRIPT = SKILL_DIR.parent / "meai-creator" / "scripts" / "meai_api.py"

# ffmpeg 兜底路径(不在 PATH 时试 winget 安装位置)
FFMPEG_FALLBACK = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages"
MIN_SCENE_BYTES = 10 * 1024  # 小于 10KB 视为坏文件, 重新生成

BEATS = ["establishing", "introduction", "development", "climax", "resolution", "closing"]


def find_tool(name):
    p = shutil.which(name)
    if p:
        return p
    if FFMPEG_FALLBACK.exists():
        for hit in FFMPEG_FALLBACK.glob(f"*/ffmpeg-*/bin/{name}.exe"):
            return str(hit)
    return None


def run(cmd, dry):
    print("  $ " + " ".join(str(c) for c in cmd))
    if dry:
        return True
    r = subprocess.run([str(c) for c in cmd])
    return r.returncode == 0


def scene_files(out_dir, n, has_key):
    tag = f"{n:02d}"
    key = out_dir / f"scene_{tag}_key.png" if has_key else None
    return key, out_dir / f"scene_{tag}.mp4"


def ok_file(p):
    return p.exists() and p.stat().st_size > MIN_SCENE_BYTES


def build_scene_cmd(backend, sp, scene, key_path, video_out):
    """构造单幕生成命令(返回参数列表, 首元素为脚本路径)。"""
    style = sp.get("style_bible", "").strip()
    vp = f"{style}。{scene['video_prompt']}" if style else scene["video_prompt"]
    dur = scene.get("duration", sp.get("duration_per_scene", 5))
    ratio = sp.get("ratio", "16:9")

    if backend == "seedance":
        cmd = [sys.executable, SEEDANCE_SCRIPT, "video", "--prompt", vp,
               "--duration", dur, "--ratio", ratio, "--output", video_out]
        if key_path and ok_file(key_path):
            cmd += ["--image", key_path]
        return cmd

    # meai 后端: 关键帧需 HTTP URL, 不支持本地图, 故只做纯文生视频
    return [sys.executable, MEAI_SCRIPT, "video", "--prompt", vp,
            "--duration", dur, "--ratio", ratio, "--resolution", "1080P",
            "--output", video_out]


def build_keyframe_cmd(sp, scene, key_out):
    style = sp.get("style_bible", "").strip()
    ip = f"{style}。{scene['image_prompt']}" if style else scene["image_prompt"]
    return [sys.executable, SEEDANCE_SCRIPT, "image", "--prompt", ip,
            "--ratio", sp.get("ratio", "16:9"), "--output", key_out]


def probe(p, ffprobe):
    r = subprocess.run(
        [ffprobe, "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=codec_name,width,height,r_frame_rate",
         "-of", "json", str(p)],
        capture_output=True, text=True)
    try:
        s = json.loads(r.stdout)["streams"][0]
        return (s["codec_name"], s["width"], s["height"], s["r_frame_rate"])
    except Exception:
        return None


def assemble(videos, final, ffmpeg, ffprobe, dry):
    """编码参数一致 → copy 拼接; 否则统一重编码。返回是否成功。"""
    infos = [probe(v, ffprobe) for v in videos]
    uniform = all(i == infos[0] for i in infos) and infos[0] is not None
    lst = final.parent / "concat_list.txt"
    body = "".join("file '{}'\n".format(str(v).replace("'", "'\\''").replace("\\", "/"))
                   for v in videos)

    if uniform:
        print(f"  各幕编码一致({infos[0]}) → 无损 copy 拼接")
        cmd = [ffmpeg, "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-y", final]
    else:
        print(f"  各幕编码不一致 {infos} → 统一重编码(scale={infos[0][1]}x{infos[0][2]})")
        w, h, fps = infos[0][1], infos[0][2], infos[0][3]
        vf = f"scale={w}:{h},fps={fps},format=yuv420p"
        cmd = [ffmpeg, "-f", "concat", "-safe", "0", "-i", lst,
               "-vf", vf, "-an", "-c:v", "libx264", "-crf", "18", "-y", final]

    if dry:
        print(f"  [concat_list.txt]\n{body}")
        return True
    lst.write_text(body, encoding="utf-8")
    ok = run(cmd, dry)
    if ok:
        lst.unlink(missing_ok=True)
    return ok


def main():
    ap = argparse.ArgumentParser(description="film-creator 拍摄编排器")
    ap.add_argument("screenplay", help="screenplay.json 路径")
    ap.add_argument("--backend", choices=["seedance", "meai"], help="覆盖剧本里的 backend")
    ap.add_argument("--no-keyframes", action="store_true", help="跳过关键帧, 直接文生视频")
    ap.add_argument("--assemble-only", action="store_true", help="只拼接已有 scene, 不再生成")
    ap.add_argument("--dry-run", action="store_true", help="只打印命令, 不执行")
    ap.add_argument("--final", default="final_film.mp4", help="成片文件名")
    args = ap.parse_args()

    sp_path = Path(args.screenplay)
    sp = json.loads(sp_path.read_text(encoding="utf-8-sig"))  # 容忍 PowerShell 写出的 BOM
    out_dir = sp_path.parent
    backend = args.backend or sp.get("backend", "seedance")
    use_key = backend == "seedance" and not args.no_keyframes and sp.get("keyframes", True)

    script = SEEDANCE_SCRIPT if backend == "seedance" else MEAI_SCRIPT
    if not script.exists():
        sys.exit(f"✗ 后端脚本不存在: {script} (需要先安装对应的兄弟 skill)")

    if not args.assemble_only:
        print(f"🎬 开拍: {sp.get('title', 'untitled')}  [{backend} 后端"
              f"{' + 关键帧' if use_key else ''}]")
        print(f"   剧本: {sp_path}  幕数: {len(sp['scenes'])}\n")

    videos, failed = [], []
    for sc in sp["scenes"]:
        n = sc["number"]
        beat = sc.get("beat", BEATS[min(n - 1, len(BEATS) - 1)])
        key_p, vid_p = scene_files(out_dir, n, use_key)
        videos.append(vid_p)

        if args.assemble_only or ok_file(vid_p):
            if not args.assemble_only:
                print(f"✓ 幕{n} [{beat}] 已存在, 跳过: {vid_p.name}")
            continue

        print(f"🎥 幕{n} [{beat}]")

        # 1) 关键帧(seedance 后端才有本地图生视频)
        if use_key:
            if ok_file(key_p):
                print(f"  ✓ 关键帧已存在, 跳过")
            else:
                print(f"  🖼️  生成关键帧…")
                if not run(build_keyframe_cmd(sp, sc, key_p), args.dry_run) and not args.dry_run:
                    print(f"  ! 关键帧失败, 改走纯文生视频")
                    key_p = None

        # 2) 本幕视频
        print(f"  🎬 生成视频…")
        cmd = build_scene_cmd(backend, sp, sc, key_p, vid_p)
        if run(cmd, args.dry_run):
            if args.dry_run or ok_file(vid_p):
                print(f"  ✓ 完成: {vid_p.name}")
                continue
        failed.append(n)
        print(f"  ✗ 幕{n} 失败, 继续后面的幕")

    if args.dry_run:
        print("\n[dry-run] 以上为将执行的命令, 未实际生成。")
        return

    good = [v for v in videos if ok_file(v)]
    print(f"\n📊 成功 {len(good)}/{len(videos)} 幕" + (f", 失败幕: {failed}" if failed else ""))
    if len(good) < 2:
        sys.exit("✗ 成功幕不足 2, 无法拼接。修复失败幕后重跑本命令即可续接。")

    ffmpeg = find_tool("ffmpeg")
    ffprobe = find_tool("ffprobe")
    if not ffmpeg or not ffprobe:
        sys.exit("✗ 找不到 ffmpeg/ffprobe")

    final = out_dir / args.final
    print(f"📼 拼接成片 → {final}")
    if assemble(good, final, ffmpeg, ffprobe, False):
        mb = final.stat().st_size / 1048576
        print(f"\n🎉 成片: {final}  ({mb:.1f} MB)")
    else:
        sys.exit("✗ 拼接失败, 可用 --assemble-only 单独重试拼接")


if __name__ == "__main__":
    main()
