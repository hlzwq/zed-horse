# 连续长海报视觉风格体系 (Visual Identities)

在生成连续长海报时，首选确立一个**贯穿始终的连续视觉线索（Continuous Visual Thread）**，例如中央光流、纵向时间轨道、河流山川、几何网格或渐变中轴线，使各分段无缝融合。

---

## 1. 科技全景图解 (Tech Blueprint / Roadmap)
- **基调**：深空蓝/深灰黑底、冷光青蓝、明亮电光金、赛博网格。
- **贯穿视觉线索**：纵向发光光缆/数据流管道（Central Data Conduit）、流动发光粒子。
- **卡片/排版**：半透明磨砂卡片（Glassmorphism）、发光细描边（0.5px cyan border）、等宽数字标号。
- **适用场景**：AI 技术路线图、系统架构长图、产品发布全景、技术白皮书图解。

## 2. 商业战略画卷 (Executive Canvas)
- **基调**：极夜黑 / 藏青底、哑光香槟金、钛白高对比。
- **贯穿视觉线索**：纵向优雅金线轴、微光粒子台阶、连续上升曲线。
- **卡片/排版**：高级衬线大标题、大留白、精致胶囊标签、结构化对比矩阵。
- **适用场景**：年度商业总结、投资人 Pitch 长图、个人经历里程碑、高管思想长文。

## 3. 爆款知识图解 (Infographic Explainer)
- **基调**：米白纸质底 / 柔和暖灰、克莱因蓝 / 活力橙重点。
- **贯穿视觉线索**：纵向路线地图（Roadmap Path）、步进序号节点、连贯的连接虚线。
- **卡片/排版**：圆角卡片、生动 3D/扁平拟物图标、清晰的大字号核心结论、高亮加粗。
- **适用场景**：技能干货教学、书单/方法论图解、操作指南、保姆级教程长图。

## 4. 艺术 Zine 杂志卷轴 (Editorial Zine Scroll)
- **基调**：复古粗糙报纸纹理、暖黄牛皮纸色、单色网点、高对比红黑墨水。
- **贯穿视觉线索**：手撕纸边、纵向胶带贴条（Tape）、连续墨水飞溅、红黑引线。
- **卡片/排版**：粗犷无衬线黑体、倾斜张力标题、印章印记、排版拼贴画风（Collage）。
- **适用场景**：个人经历自述、独立创作者宣言、青年文化长图、品牌态度海报。

## 5. 极简极净画卷 (Minimalist Clean Flow)
- **基调**：纯白 / 浅灰底、单色灰阶搭配单强调色（如亮绿、钴蓝）。
- **贯穿视觉线索**：中央细线对齐中轴、渐变轻阴影、极简几何分界。
- **卡片/排版**：瑞士平面风格（Swiss Style）、巨大网格对比、精密对齐、极宽行距。
- **适用场景**：产品设计规范、极简思维导图、哲学/概念梳理。

## 6. 故事叙事长轴 (Storytelling Scroll)
- **基调**：插画风、日漫/绘本色调、温暖自然光影。
- **贯穿视觉线索**：纵向蜿蜒小路、天际线昼夜渐变（晨曦→正午→黄昏→星空）、主人公行进路线。
- **卡片/排版**：对话气泡、分镜感框架、手写体小标题。
- **适用场景**：个人成长故事、品牌创业历程、用户旅程地图、儿童绘本长图。

---

## 视觉基准锁（Visual Baseline Lock）

在生成 Segment 1 时，必须确立并固化以下参数并在后续各段提示词中显式约束：
```yaml
canvas:
  ratio: "9:16"
  bleed_margin: "12% safety margin at top and bottom"
color_system:
  bg_gradient: "e.g. Deep navy (#0A0F24) to dark obsidian (#050711)"
  primary_text: "#FFFFFF"
  accent_glow: "#00E5FF (Electric Cyan)"
  divider_thread: "Vertical cyan energy stream centered at X=50%"
typography:
  headline_font: "Bold geometric sans-serif"
  body_font: "Clean modern sans-serif"
continuity_element: "Continuous central glowing road spanning across top and bottom edges without termination"
```
