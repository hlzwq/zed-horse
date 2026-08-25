# Gemini 连续长海报生成提示词模版库 (Prompt Templates)

在使用 Gemini 的 `generate_image` 工具生成分段切片时，提示词的核心在于**「视觉连续性约束」**与**「过渡区留白规范」**。

---

## 模版一：第一段（顶部开场 / Segment 01: Top & Opening）

### 结构特点
- 拥有整张长图**唯一的总大标题**与主视觉入口。
- 中间承载第一部分核心内容/背景介绍。
- **底部严禁闭合**：背景、中轴线、光流、纹理必须以开放式姿态向下延伸，底部预留 10-15% 安全过渡区（无文字、无人物面部、无裁切卡片）。

### Gemini 提示词模版
```text
Professional vertical infographic poster segment, PART 1 of a continuous long scroll poster.
[Visual Identity & Style]: High-tech futuristic editorial style, dark navy blue background (#070B19) with subtle glowing cyber grid lines and cyan/electric purple neon lighting accents. Clean modern typography, high contrast, 8k resolution design aesthetics.

[Layout & Structure]:
1. TOP HEADER (Upper 20%): Large prominent master title: "【总标题】", subtitle: "【副标题】", sleek metallic/neon typography badge.
2. MAIN CONTENT (Middle 60%): Segment 1 content cards focusing on "【第1段核心内容：如背景/起点/痛点】", containing clear structured text blocks, elegant circular milestone icons, and crisp typography.
3. CONTINUOUS VISUAL THREAD: A central vertical glowing energy conduit / roadmap line running down the center of the canvas.
4. BOTTOM TRANSITION (Lower 20%): OPEN-ENDED CONTINUATION. The central energy conduit, particle stream, and dark gradient background extend naturally past the bottom frame edge. NO page numbers, NO footer badges, NO closed borders. Top & bottom margins clean of critical text.
Ratio: 9:16, ultra-sharp vector graphic style, crisp clean legible Chinese text.
```

---

## 模版二：中间段（承接与推进 / Segment 02..N-1: Middle Sections）

### 结构特点
- 必须传入**上一段图片**作为参考图（`ImagePaths: ["path/to/segment_01.png"]`）。
- **顶部承接**：严格对齐上一张底部的颜色、亮度、纹理与中轴线。
- **中间内容**：展示当前小节核心内容（如小节 02、03、核心方法、数据对比），使用同一卡片与图标语言。
- **底部开放**：继续向下延伸中轴线与背景，预留过渡区。
- **绝对禁忌**：不得重复总标题，不得放“下一页/Part N/翻页”标记，不得闭合边框。

### Gemini 提示词模版
```text
Professional vertical infographic poster segment, PART 2 (Continuous Middle Slice) of a seamless long vertical scroll poster.
[Reference & Continuity Directive]: DIRECT VISUAL CONTINUATION of the provided reference image. Perfectly match the background color palette (#070B19 navy gradient), grid texture density, lighting temperature, and typography hierarchy of the reference image.

[Layout & Structure]:
1. TOP TRANSITION (Upper 15%): SEAMLESS ENTRY. Directly receive and continue the vertical central glowing energy conduit and background ambient glow from the reference image. NO repeated main title, NO top header decoration.
2. SECTION CONTENT (Middle 70%): Section subtitle: "【小节标题：02 核心突破/阶段演进】". Structured information layout with 2-3 translucent glassmorphism cards, glowing data icons, and clean bullet points for "【第2段具体文案与数据】".
3. CONTINUOUS VISUAL THREAD: The vertical central glowing conduit flows continuously through the center of this slice from top to bottom.
4. BOTTOM TRANSITION (Lower 15%): OPEN-ENDED CONTINUATION. The glowing conduit and dark background continue smoothly past the bottom edge into the next section.
Ratio: 9:16, strict visual consistency with reference, crisp typography, no standalone page borders.
```

---

## 模版三：最后一段（收尾与总结 / Segment N: Final & Conclusion）

### 结构特点
- 传入上一张图片作为参考（`ImagePaths: ["path/to/segment_N-1.png"]`）。
- **顶部承接**：与上一段无缝衔接。
- **中间内容**：最终结论、行动指南（CTA）、核心金句。
- **底部闭合**：整张长图唯一的完整底部收束（Logo、版权落款、二维码占位区、优雅渐隐底边）。

### Gemini 提示词模版
```text
Professional vertical infographic poster segment, FINAL PART (Conclusion & CTA) of a seamless long vertical scroll poster.
[Reference & Continuity Directive]: DIRECT VISUAL CONTINUATION of the previous poster segment. Inherit exact background gradient (#070B19), typography style, card shapes, and the central glowing conduit from the reference image.

[Layout & Structure]:
1. TOP TRANSITION (Upper 15%): Smoothly receive the vertical energy conduit and background glow flowing from the previous slice.
2. CORE CONCLUSION (Middle 60%): Section title "【总结/行动倡议/核心结论】". Key takeaway callout box with golden accent glow, bullet points, and inspiring summary message.
3. FOOTER CLOSURE (Lower 25%): The FINAL CLOSURE of the entire long poster. The central energy conduit converges into a glowing brand badge / anchor emblem. Bottom includes brand signature "【品牌/作者签名】", slogan, and clean bottom frame gradient fade.
Ratio: 9:16, consistent aesthetic, polished grand finale composition.
```

---

## 提示词调优技巧（Gemini Image Best Practices）

1. **白名单文字原则（Strict Text Whitelist）**：
   在提示词中明确要求："Only render the exact Chinese text specified in quotation marks: '...' - do not generate gibberish or unrelated decorative English."
2. **多模态参考图绑定（Reference Image Conditioning）**：
   调用 `generate_image` 时，将前一张切片的文件绝对路径传入 `ImagePaths`，并配合提示词 `"Match the exact lighting, chromatic values, and line coordinates of the reference image"`，可使相邻切片的接缝色差低于 3%。
3. **安全过渡带预留（Safety Bleed Zones）**：
   提示词中始终强调 `"Keep top 10% and bottom 10% areas free of text, faces, and critical icons, dedicated exclusively to ambient background and flowing connecting paths"`。
