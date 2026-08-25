# 特雷勒复古纸板长海报提示词工程 (Prompt Engineering · 强化版)

本指南针对 **Gemini (`generate_image`)** 生成粗糙纸板、折痕纤维、旧材料感、铅笔排线与剪影布告栏长海报提供精准提示词模版。

---

## 核心风格公式 (Master Style Prompt)

```text
[Style & Texture]: Authentic Bill Traylor inspired naive folk-art infographic poster on weathered rough corrugated cardboard (visible coarse brown kraft pulp fibers, dark wood flecks, natural paper creases, distressed raw edges, vintage scrap cardboard warmth). Flat no-perspective collage composition, naive graphite pencil contour outlines with visible hand-drawn pencil cross-hatching and shading. Flat gouache/poster paint coloring in muted 5-color palette: vintage navy blue (#243B53), warm ochre red / sienna (#8B3A2B), earthy mustard yellow (#C58B35), charcoal pencil black (#1F1E1C), and kraft cardboard tan. Minimalist silhouette figures with stick-thin limbs, top hats or flat caps, highly expressive gestures, accompanied by playful silhouette dogs, birds, and vintage everyday objects.
[Negative Constraints]: No 3D render, no realism, no photorealistic human anatomy, no neon colors, no glowing lights, no smooth gradients, no slick digital corporate vector art.
```

---

## 模版：标准 6 格读书笔记布告栏海报 (6-Grid Bulletin Poster)

```text
Detailed infographic poster in Bill Traylor naive folk-art silhouette style, matching the exact surface texture, color tone, and layout of weathered rough found cardboard.
[Material & Background]: Authentic weathered rough corrugated cardboard ground, coarse brown kraft pulp fibers, visible dark wood flecks, natural paper creases, distressed raw edges, vintage scrap cardboard warmth. Naive graphite pencil outlines with rich hand-drawn cross-hatching and pencil shading.
[Color Palette]: Muted 5-color gouache poster paint on raw cardboard: vintage navy blue (#243B53), warm ochre red / sienna (#8B3A2B), earthy mustard yellow (#C58B35), charcoal pencil black (#1F1E1C), and kraft cardboard tan.

[Layout & Content]:
- HEADER (Top): Retro bold headline '【大标题】', subtitle in stars '★ 【副标题/导语】 ★', numbered badge '01/03' at top right.
- ICON ROW: Naive flat doodle icons (e.g. hourglass, teapot, walking man with hat, little black dog, weighing scale, bird, old radio).
- GRID CARDS (6 Naive Panels with hand-drawn pencil borders and light yellow/blue backgrounds):
  1. '❶ 【要点1标题】': Silhouette stick-figures demonstrating 【要点1隐喻】. Text: '【要点1金句】 / 【简要说明】'.
  2. '❷ 【要点2标题】': Silhouette figure demonstrating 【要点2隐喻】. Text: '【要点2金句】 / 【简要说明】'.
  3. '❸ 【要点3标题】': Silhouette figure demonstrating 【要点3隐喻】. Text: '【要点3金句】 / 【简要说明】'.
  4. '❹ 【要点4标题】': Silhouette figure demonstrating 【要点4隐喻】. Text: '【要点4金句】 / 【简要说明】'.
  5. '❺ 【要点5标题】': Silhouette figure demonstrating 【要点5隐喻】. Text: '【要点5金句】 / 【简要说明】'.
  6. '❻ 【要点6标题/总结】': Silhouette figure demonstrating 【要点6隐喻】. Text: '【要点6金句】 / 【简要说明】'.
- BOTTOM BARS: '★ 核心清单 ★' with naive icons (木桶、沙漏、长椅) and '★ 认知金句 ★': '【总结金句】'
Ratio: 9:16, crisp Chinese text, authentic found-cardboard texture, pencil shading, naive warmth.
```
