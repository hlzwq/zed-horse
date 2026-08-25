#!/usr/bin/env python3
"""
Seamless Vertical Long Poster Stitching Tool
Continuous Long Poster (连续长海报无缝拼接工具)

Features:
- Automatic width normalization across all segment slices
- Configurable top/bottom cropping per slice
- Smooth vertical alpha gradient feather blending on overlap regions
- High-resolution export (PNG/JPEG)
"""

import os
import sys
import argparse
from typing import List, Optional, Tuple, Dict, Any
from PIL import Image, ImageChops

def normalize_width(images: List[Image.Image], target_width: Optional[int] = None) -> List[Image.Image]:
    """Resize all images to have the exact same pixel width while preserving aspect ratio."""
    if not images:
        return []
    if target_width is None:
        target_width = max(img.width for img in images)
    
    resized = []
    for img in images:
        if img.width != target_width:
            new_height = int(round(img.height * (target_width / img.width)))
            resized.append(img.resize((target_width, new_height), Image.Resampling.LANCZOS))
        else:
            resized.append(img.copy())
    return resized

def blend_vertical_seam(top_img: Image.Image, bottom_img: Image.Image, overlap_height: int) -> Image.Image:
    """
    Blends two vertical image slices over an overlap region of specified height using linear alpha feathering.
    """
    if overlap_height <= 0:
        # Direct concatenation
        w = top_img.width
        h = top_img.height + bottom_img.height
        out = Image.new("RGBA", (w, h))
        out.paste(top_img, (0, 0))
        out.paste(bottom_img, (0, top_img.height))
        return out

    w = top_img.width
    top_h = top_img.height
    bot_h = bottom_img.height

    overlap_height = min(overlap_height, top_h, bot_h)

    # Convert to RGBA
    top_rgba = top_img.convert("RGBA")
    bot_rgba = bottom_img.convert("RGBA")

    total_h = top_h + bot_h - overlap_height
    out = Image.new("RGBA", (w, total_h))

    # Paste top non-overlapping part
    top_clean_h = top_h - overlap_height
    out.paste(top_rgba.crop((0, 0, w, top_clean_h)), (0, 0))

    # Overlap blend region
    top_overlap_strip = top_rgba.crop((0, top_clean_h, w, top_h))
    bot_overlap_strip = bot_rgba.crop((0, 0, w, overlap_height))

    # Create linear gradient mask from 1.0 (top) to 0.0 (bottom) for top strip,
    # or from 0.0 (top) to 1.0 (bottom) for bottom strip
    mask_bot = Image.new("L", (w, overlap_height))
    mask_data = []
    for y in range(overlap_height):
        alpha = int(255 * (y / max(1, overlap_height - 1)))
        mask_data.extend([alpha] * w)
    mask_bot.putdata(mask_data)

    blended_strip = Image.composite(bot_overlap_strip, top_overlap_strip, mask_bot)
    out.paste(blended_strip, (0, top_clean_h))

    # Paste bottom non-overlapping part
    bot_clean_h = bot_h - overlap_height
    out.paste(bot_rgba.crop((0, overlap_height, w, bot_h)), (0, top_h))

    return out

def stitch_segments(
    image_paths: List[str],
    output_path: str,
    overlap_ratio: float = 0.08,
    overlap_px: Optional[int] = None,
    crop_top_px: int = 0,
    crop_bottom_px: int = 0,
    target_width: Optional[int] = None,
    export_format: str = "PNG"
) -> str:
    """
    Main stitching pipeline.
    """
    if not image_paths:
        raise ValueError("No input images provided.")

    print(f"[Continuous Poster Stitcher] Loading {len(image_paths)} segments...")
    raw_images = [Image.open(p).convert("RGBA") for p in image_paths]

    # Crop if specified
    processed_images = []
    for i, img in enumerate(raw_images):
        w, h = img.size
        # Apply crop (crop_top for segment > 0, crop_bottom for segment < last)
        ct = crop_top_px if i > 0 else 0
        cb = crop_bottom_px if i < len(raw_images) - 1 else 0
        
        if ct > 0 or cb > 0:
            new_h = h - ct - cb
            if new_h > 10:
                img = img.crop((0, ct, w, h - cb))
        processed_images.append(img)

    # Normalize width
    normalized = normalize_width(processed_images, target_width=target_width)
    base_w = normalized[0].width

    current = normalized[0]
    for i in range(1, len(normalized)):
        next_img = normalized[i]
        ov_h = overlap_px if overlap_px is not None else int(round(next_img.height * overlap_ratio))
        print(f"  -> Merging Segment {i} with Segment {i+1} (Overlap: {ov_h}px)...")
        current = blend_vertical_seam(current, next_img, overlap_height=ov_h)

    # Convert to RGB if saving as JPEG
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    if output_path.lower().endswith((".jpg", ".jpeg")) or export_format.upper() == "JPEG":
        rgb_out = Image.new("RGB", current.size, (255, 255, 255))
        rgb_out.paste(current, mask=current.split()[3]) # paste with alpha
        rgb_out.save(output_path, "JPEG", quality=95)
    else:
        current.save(output_path, "PNG")

    print(f"[Continuous Poster Stitcher] Success! Long poster exported to: {output_path}")
    print(f"  Final Canvas Dimensions: {current.width} x {current.height} px")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Stitch vertical poster segments into a continuous long poster.")
    parser.add_argument("images", nargs="+", help="Paths to segment images in top-to-bottom order")
    parser.add_argument("-o", "--output", required=True, help="Output file path (e.g. poster_full.png)")
    parser.add_argument("--overlap-ratio", type=float, default=0.08, help="Overlap ratio between adjacent slices (default 0.08 / 8%%)")
    parser.add_argument("--overlap-px", type=int, default=None, help="Fixed overlap pixel height (overrides ratio)")
    parser.add_argument("--crop-top", type=int, default=0, help="Pixels to crop from top of middle/bottom slices")
    parser.add_argument("--crop-bottom", type=int, default=0, help="Pixels to crop from bottom of top/middle slices")
    parser.add_argument("--target-width", type=int, default=None, help="Target pixel width for all slices")
    args = parser.parse_args()

    stitch_segments(
        image_paths=args.images,
        output_path=args.output,
        overlap_ratio=args.overlap_ratio,
        overlap_px=args.overlap_px,
        crop_top_px=args.crop_top,
        crop_bottom_px=args.crop_bottom,
        target_width=args.target_width
    )

if __name__ == "__main__":
    main()
