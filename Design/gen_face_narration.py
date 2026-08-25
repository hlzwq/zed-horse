# -*- coding: utf-8 -*-
"""为 face.mp4 生成中文旁白。MiniMax speech-02-hd, Chinese_calm_streamer_vv1 男声, hex 解码。
视频 face.mp4 = 10.04s, 旁白需压在 10s 内。speed 自适应。"""
import json, os, re, sys, subprocess, base64, urllib.request, ssl

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

API_KEY = os.environ.get("MINIMAX_API_KEY", "")
VOICE_ID = "Chinese_calm_streamer_vv1"
MODEL = "speech-02-hd"
BASE_URL = "https://api.minimaxi.com/v1/t2a_v2"
OUT_DIR = r"D:\zed horse\Design"
FINAL = os.path.join(OUT_DIR, "face_narration.mp3")
VIDEO_DUR = 10.04  # face.mp4

FFMPEG = r"C:\Users\webfox\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
FFPROBE = r"C:\Users\webfox\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffprobe.exe"

TEXT = "当古老的海上丝绸之路延伸至现代航线，我们连接了两座城市，架起了一座文化的桥梁。"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def call_tts(text, speed):
    body = json.dumps({
        "model": MODEL, "text": text, "stream": False,
        "voice_setting": {"voice_id": VOICE_ID, "speed": speed, "vol": 1.0, "pitch": 0},
        "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3"},
    }).encode("utf-8")
    req = urllib.request.Request(BASE_URL, data=body,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        if "data" in result and "audio" in result["data"]:
            return result["data"]["audio"], result.get("extra_info", {})
        print(f"  API error: {json.dumps(result, ensure_ascii=False)[:300]}", file=sys.stderr)
        return None, {}


def decode_audio(s):
    if len(s) % 2 == 0 and re.fullmatch(r'[0-9a-fA-F]+', s):
        return bytes.fromhex(s), "hex"
    return base64.b64decode(s), "base64"


def ffprobe_dur(path):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def render(speed):
    audio_str, extra = call_tts(TEXT, speed)
    if audio_str is None:
        return None, None
    data, fmt = decode_audio(audio_str)
    tmp = os.path.join(OUT_DIR, "face_narr_tmp.mp3")
    with open(tmp, "wb") as f:
        f.write(data)
    r = subprocess.run([FFMPEG, "-y", "-i", tmp, "-c:a", "libmp3lame", "-b:a", "128k", FINAL],
                       capture_output=True, text=True)
    if os.path.exists(tmp):
        os.remove(tmp)
    if r.returncode != 0:
        print(f"ffmpeg FAIL: {r.stderr[-200:]}", file=sys.stderr)
        return None, None
    d = extra.get("audio_length", 0) / 1000 if extra.get("audio_length") else ffprobe_dur(FINAL)
    return d, fmt


if __name__ == "__main__":
    if not API_KEY:
        print("Error: MINIMAX_API_KEY not set", file=sys.stderr); sys.exit(1)
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Voice={VOICE_ID}  Model={MODEL}  视频={VIDEO_DUR}s  文本={len(TEXT)}字\n")
    print(f"文本: {TEXT}\n")

    # 先 speed=1.0, 看权威时长; 若 >9.6s 略提速以适配 10.04s 视频
    chosen_speed, chosen_dur = 1.0, None
    for sp in [1.0, 1.08, 1.15]:
        d, fmt = render(sp)
        if d is None:
            print(f"speed={sp}: FAIL"); continue
        status = "适配✓" if d <= 9.8 else f"偏长(>9.8s)"
        print(f"speed={sp}: {fmt} {d:.2f}s  ({len(TEXT)/d:.1f}字/秒)  {status}")
        chosen_speed, chosen_dur = sp, d
        if d <= 9.8:
            break  # 拿到适配版就停
    if chosen_dur is None:
        print("全部失败", file=sys.stderr); sys.exit(1)

    print(f"\n✓ 最终: speed={chosen_speed}  时长={chosen_dur:.2f}s  输出={FINAL}")
    slack = VIDEO_DUR - chosen_dur
    print(f"  视频 {VIDEO_DUR}s - 旁白 {chosen_dur:.2f}s = 富余 {slack:.2f}s (可前后留白)")
