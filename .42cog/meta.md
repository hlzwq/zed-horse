# Zed Horse · AI 自主视觉创作系统 — 项目身份

<meta>
  <document-id>zed-meta</document-id>
  <version>1.0.0</version>
  <project>Zed Horse · AI 自主视觉创作系统</project>
  <type>Project Metadata</type>
  <created>2026-08-23</created>
</meta>

## Document Purpose

这个系统的**项目身份**：它是什么、归谁、在哪、跟谁交接。

**这里只描述事实，不定规矩。** 怎么干看 `CLAUDE.md`，产出该长什么样（含命名）看 `specs/`，
朝哪儿使劲看 `intent.md`，有哪些改不了的现实看 `real.md`。

---

<project-info>

## 身份

- **系统名**：Zed Horse · AI 自主视觉创作系统 ｜ **系统码**：`zed` ｜ **开仓**：2026-08-23
- **一句话定位**：用 AI 把一句想法做成能直接发布的作品——电影感短片、口播讲解片、教学动画、平面图像（海报 / zine）
- **负责人**：本人（用户）
- **状态**：在建

## 位置

- **作品区**：`content/` —— 装成片及其全套工程（脚本 · 分镜 · 音轨 · 可复渲工程）
- **远程仓库**：待配
- **与默认六组的差异**：本仓在六组骨架之外**已有大量在用存量**——`Design/`（用户风格规范）、`remotion_video/`（Remotion 旧作）、`PIC/`、`src/`、`.codex-video/`、`.agents/`、`.claude/`（skill 生态）。存量目录 = **事实**的真相源，不迁移、不删除、不改写；新作品一律进 `content/`，按新规约执行（旧实践迁就新理念）。

## 交接

这个系统在更大的链条里是哪一环：

```
（AI 平台与模型服务）──给我──▶  Zed Horse · AI 自主视觉创作系统  ──我给出──▶（发布渠道）
```

| | 是谁 | 交接什么 | 怎么交 |
|---|---|---|---|
| 上游 | ME AI 平台（seedream/seedance）· shiping（video-v1）· TTS（StepFun/MiMo/MiniMax）· HyperFrames CLI · Remotion | 生成能力：图 / 视频 / 语音 / 渲染 | API，key 在 `.env`（不入库） |
| 下游 | 用户自定的发布渠道 | 成片 MP4（+ 字幕/封面） | 人审后人发——发布动作不自动化 |

**没有上下游就写「独立系统」**——但先想一想，多数系统都有。

## 依赖

| 依赖 | 版本 | 缺了会怎样 |
|---|---|---|
| Node.js | 22+（本机 v24 ✓） | HyperFrames / Remotion 全跑不了 |
| npm | 随 Node | 装不了依赖；ECOMPROMISED 时用 node 直调 cli.js |
| Python | 3.8+ | TTS 脚本（StepFun/MiniMax/Edge）跑不了 |
| ffmpeg / ffprobe | 本机已装，**不在 Bash PATH，用全路径** | 探片、合流、转码全部停摆 |
| git | ✓ | 状态持久化无从谈起 |
| ME AI 平台账号（图片/视频生成） | key 在 `.env` | 电影感短片产线停 |
| shiping 平台（seedance video-v1） | key：`.env` 的 `SHIPING_API_KEY` | 本地图生视频停 |
| TTS：StepFun / MiMo / MiniMax | StepFun 有限流，重试 | 口播与教学片的解说音轨停 |
| HyperFrames CLI | `npx hyperframes` | HTML 渲 MP4 的成片 author 停 |

**换台机器能不能跑起来，看这张表填得全不全。**

</project-info>

---

元数据变了就地改，不留历史——**历史在提交链里**。
