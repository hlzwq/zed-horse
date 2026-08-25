# Zed Horse · AI 自主视觉创作系统 · 状态板（给 AI · 跨会话唯一接续点）

> 开工先读 `CLAUDE.md` + **`.42cog/` 四份**（`intent` · `real` · `cog` · `meta`）+ 本文件 + `state/memory/MEMORY.md`。
> **非轮规则：每轮有效工作必更新本文件**（倒序追加，新的在上，带日期与 commit hash）。
> 每完成一个可命名的逻辑单元存一次；破坏性操作之前也存一次。这是给你自己留的后路，不是给别人看的历史。

> ## 2026-08-23 · 外部工具输出去向立规（AI：Claude Code / glm-5.3）
> **发现**：Antigravity+Gemini 跑 editorial-vision-studio 等会话的约 18 张成品（寻羊塔 zine ×2 · Moderna 漫画四格 + 白板卡 ×3 + lead · photo-abstract 水库 · pagoda 五风格系列 ×5 + 明信片 · granularity lead）埋在 `C:\Users\webfox\.gemini\antigravity-cli\brain\<会话id>\`，仓内无副本。
> **已立规**：外部工具成品与提示词显式落仓（已写进 `CLAUDE.md` 约定节）；工具状态区留仓外不动。
> **已收编**（2026-08-23 用户拍板「全部收编」）：18 张成品（11.9 MB）按 5 个作品单元落 `content/`——`xunyang-tower-zine-poster`（2）· `granularity-control-lead`（1）· `moderna-mrna-explainer-series`（8）· `reservoir-photo-abstract`（1）· `pagoda-poster-series`（6），各带 readme（来源指针+清单）；原件未动。提示词未随图落盘（scratch 全空），回溯走 `conversations/`——**下次用外部工具，成品与提示词当场落仓**。

> ## 2026-08-23 · 图片线并入（AI：Claude Code / glm-5.3）
> **已决定**：平面图像创作/优化并进本系统（用户拍板）——方向句放宽为「作品（成片·图像）」，作品区加第四类；系统更名「AI 自主视觉创作系统」。
> **已完成**：intent.md 四处修订（方向 / 度量 / 作品区 / 验证闭环）；meta.md 定位更新；changelog 已记；全仓名字统一替换（含 plugin.json）。
> **下一步**：`zed-research` 从「口播片产线不可妥协的三条」起步。

> ## 2026-08-23 · 初始化收尾（AI：Claude Code / glm-5.3）
> **已完成**：① 六组骨架落地（系统码 `zed`，作品区 `content/`；现有 CLAUDE.md 保留，开工协议已并入其下半部）② `.42cog/intent.md` 已按本仓实况起草——收敛方向/真难题/排除清单/真相源/验证闭环，**待人过目拍板** ③ `meta.md` 事实填齐（定位/上下游/依赖表）④ 工具链检查通过（仅缺 scoop/gitleaks，不挡事）。
> **已决定**：存量目录（`Design/` `remotion_video/` `PIC/` 等）= 事实的真相源，不迁移不删除；新作品一律进 `content/`。成片 MP4/音轨走仓外或 LFS，仓里留路径+哈希。
> **待办**：① 用户过目 intent.md 收敛方向 ② **远程仓库：用户确认暂无，记此待办**——`_build/_tmp/_archive` 等忽略件没有远端副本，不能一直欠着 ③ `real.md`/`cog.md` 还是模板占位 ④ 下一步走 `zed-research`（第二步系统分析）。
> **放权边界（用户已定）**：探查与 `content/`、`_tmp/` 内创作免确认；环境变更、提交推送须确认——已写进 `CLAUDE.md` 约定节。

> ## 🌱 系统开仓（2026-08-23 第一轮）
> `aias-meta-init` 生成六组骨架：① `README.md` `CLAUDE.md` `.42cog/` `specs/` ② `vault/` `notes/` `resources/` ③ `skills/` `scripts/` `plugin.json` ④ `content/` ⑤ `state/` `docs/` ⑥ `_build/` `_tmp/` `_archive/`（忽略）。
> **收敛方向**（草稿，待人确认）：见 `.42cog/intent.md`——**那句话只有一份，别抄到这里来**。
> **下一步**：确认收敛方向 → `zed-research` 找依据、排真相源权重 → 回来改这一句。方向第一版粗是正常的，四步是循环。
