# -*- coding: utf-8 -*-
"""清除 face1.png 天空区域的孤立小点(疑似远景飞机/飞鸟), 地景建筑风车完全不动。
对天空上45%做 size=3 中值滤波, 抹掉孤立1-2像素点, 几乎不影响AI生成的柔和天空渐变。"""
from PIL import Image, ImageFilter
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = r"D:\zed horse\PIC\face1.png"
DST = r"D:\zed horse\PIC\face1_clean.png"

img = Image.open(SRC).convert("RGB")
W, H = img.size
sky_h = int(H * 0.45)  # 天空区域
sky = img.crop((0, 0, W, sky_h))
sky_clean = sky.filter(ImageFilter.MedianFilter(size=3))
img.paste(sky_clean, (0, 0))
img.save(DST, "PNG")
print(f"原图 {W}x{H}, 天空区域 0..{sky_h}px 已中值滤波(去孤立点), 地景完整保留")
print(f"已存: {DST}")
