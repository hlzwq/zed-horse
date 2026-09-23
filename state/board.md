# Zed Horse · AI 自主视觉创作系统 · 状态板（给 AI · 跨会话唯一接续点）

> 开工先读 `CLAUDE.md` + **`.42cog/` 四份**（`intent` · `real` · `cog` · `meta`）+ 本文件 + `state/memory/MEMORY.md`。
> **非轮规则：每轮有效工作必更新本文件**（倒序追加，新的在上，带日期与 commit hash）。
> 每完成一个可命名的逻辑单元存一次；破坏性操作之前也存一次。这是给你自己留的后路，不是给别人看的历史。

> ## 2026-09-24 · meai-creator 默认配置改为 meaicc（用户拍板）（AI：Claude Code / step-5-preview）
> **决定（用户指示）**：**`https://api.meaicc.com` 定为视频 API 准则 base**——原来 meai.cloud 那套不对；key 用 meaicc 对应的那把。
> **已改（4 处）**：① `meai_api.py:26` 默认 `MEAI_BASE_URL` → `https://api.meaicc.com`（不改 env 覆盖能力，旧站仍可 `$env:MEAI_BASE_URL="https://api.meai.cloud"` 指回）② 视频默认模型 `seedance-2.0` → **`sd-2-fast`**（用户 2026-09-24 指定；`sd-2-c1` 只是文档示例模型）③ SKILL.md 同步（env 说明/默认模型表/缓存 10 小时）④ **用户级环境变量 `MEAI_API_KEY` = meaicc 令牌**（`sk-aszx9…`，与 ccSwitch「MEAI」provider 同一把——**两处存放，任一处轮换记得同步**）。
> **生效面**：新开会话/新终端自动生效；当前会话内 PowerShell 仍持旧值，须先 `$env:MEAI_API_KEY="sk-…"` 或重开终端。
> **待实测（未动，计费）**：该 key 在 `/v1/videos` 上是否有视频额度——`python meai_api.py video --prompt "测试" --duration 5 --output out.mp4`（默认 sd-2-fast）提交一条即知，用户点头再跑。
> **★ ccSwitch 正交结论（2026-09-24 用户问过，记此防再绕）**：**做视频不需要切 ccSwitch**——ccSwitch 只换 Claude Code 自身跑的模型（大脑，当前 StepFun）；视频调用由 `meai_api.py` 带 `MEAI_API_KEY` 直连 meaicc，两条链路互不经过。只有想换掉 Claude Code 这个大脑本身时才在 ccSwitch 切「MEAI」。已同步 memory（`meai-video-pipeline`）。
> **参数边界（2026-09-24 从 `api.meaicc.com/create/sd-2.html` 全文提取，官方文档实证）**：`duration` **5–15 秒**；参考生视频「输入视频+输出视频」合计 ≤25 秒，参考媒体最多 9 图+3 视频+3 音频；宽高比仅 **1:1 / 16:9 / 9:16**（旧站 4:3 表在 meaicc 不适用）；图片 ≥300×300；**首尾帧 sd-2 家族直接支持**（旧站是 wan2.7-only，别混）；结果缓存 10 小时。文档全文存 `_tmp/20260924-meaicc-probe/sd2-doc-full.txt`。

> ## 2026-09-24 · LLM 中转 URL 配置定位：api.meaicc.com 在 ccSwitch（AI：Claude Code / step-5-preview）
> **已查明**：`https://api.meaicc.com` 的配置在 **ccSwitch**，不在本仓、不在任何 skill。位置：`C:\Users\webfox\.cc-switch\cc-switch.db` 的 `providers` 表，provider「**MEAI**」（id `260a3b8b-a9a5-4f7d-bcf0-816e4c20eee1`，claude 类）：
> - `ANTHROPIC_BASE_URL=https://api.meaicc.com`；模型映射 Opus=`sd-2-fast` · Sonnet=`mx-h3[1M]` · Haiku=`sd-2.5-c1` · Fable=`sd-2-c1[1M]`；**当前未激活**（`is_current=0`）。
> - **当前激活**：provider「StepFun」（`cff4f4e9…`，`api.stepfun.com/step_plan`）——与 `~/.claude/settings.json` 的 env 块一致，ccSwitch 切换即自动改写该文件。
> **已排除**：① 完整 URL `https://api.meaicc.com/create/sd-2.html` 在 cc-switch.db 与全仓**均无此值**——看形态是中转站网页后台页，非配置项，仓里只存裸域名；② MEAI 另有「MEAI real / MEAI copy / MEAI copy 国产」三个变体，base_url 全是 `api.meai.cloud`（claude-opus-* / kimi / deepseek / qwen 系）。
> **⚠️ 两套 MEAI 别混**：ccSwitch 的「MEAI」= `api.meaicc.com`，**只给 Claude Code 对话用**（sd-2-* 是文本模型，生不了图/视频，见下方 2026-09-23 渠道冒烟记录）；**生图/生视频**走另一套——环境变量 `MEAI_API_KEY` + 默认 `https://api.meai.cloud`（`.claude/skills/meai-creator/scripts/meai_api.py:26`），与 ccSwitch 无关。
> **下一步（未动）**：若要在 Claude Code 里切到该中转，在 ccSwitch 界面激活「MEAI」即可，无需改本仓任何文件。排查脚本在 `_tmp/20260924-cc-switch-probe/`（一次性，可删）。**（本条「sd-2-* 是文本模型/生不了视频」的判断已被下方同日两条推翻，以新者为凭。）**

> ## 2026-09-24 · meaicc 定位：视频 API 与对话 API 同域并存，sd-2 家族即视频模型（AI：Claude Code / step-5-preview）
> **实证（页面即文档）**：`https://api.meaicc.com/create/sd-2.html` 就是该中转的**视频 API 对接文档**：`POST /v1/videos` 创建任务 → `GET /v1/videos/{task_id}` 轮询（≥20s）→ `SUCCEEDED` 后下 `object`，**结果缓存 10 小时**。文档示例的 model 就是 **`sd-2-c1`**——**sd-2 家族（c1~c8 · sd-2-fast · sd-2.5-c1 · mx-h3 · w3-c1）是视频模型，sd 即 seedance 家族**（用户 2026-09-24 指出，页面实证无误）。支持文生视频 / 图生视频 / 首尾帧 / 参考生视频（`@图1` 指代）。页面另提供「字字动画」插件包 `video_plugin_meaicc.zip`。
> **⚠️ 已纠错的错判（首轮下错，记此防再犯）**：曾据 `/v1/models` 与 `/api/pricing` 只有 10 个模型且 `supported_endpoint` 全为 `openai`（对话端点），断言「该中转无视频模型」——**错**。这两个接口只反映**对话侧**，视频端点在文档站单独成页，**不能用对话端点清单推视频能力**。同理，2026-09-23 那条「sd-2-c1 是文本模型」的结论也存疑（当时用 image 端点打 sd-2-c1，本就打不对端点），待用 `/v1/videos` 复测。
> **坑**：python urllib 裸请求 meaicc 被 Cloudflare 挡（`403 error code: 1010`），带浏览器 UA 即通。
> **待实测（未动）**：拿 ccSwitch「MEAI」令牌 POST `/v1/videos`（`model=sd-2-c1`）提交一条 5s 试跑，确认该 key 是否有视频额度——**会真实计费，待用户点头**。脚本在 `_tmp/20260924-meaicc-probe/`（一次性）。

> ## 2026-09-23（晚）· v2 提示词重写完成 · meai 渠道实测未开通（AI：Claude Code / step-5-preview）
> **用户指令**：改用 meai-creator 重做，重做之前先用 `seedance-prompt-en` 优化提示词，依据是一份新的 8 镜头 75 秒分镜。
> **已完成**：`content/jade-rabbit-hometown-moon/storyboard.md` **整份重写为 v2**（旧即梦版在提交链里，未删）。要点：
> ① **8 场拆成 14 个生成单元**——本地管线「一次生成 = 一张首帧 + 一条连续运动，段内不能切镜头」，所以镜头 02（尾翼特写插入）、03（外景→内景）、05（结尾天井）、06（特写→特写→中景）、07（特写→大远景）全部拆开；
> ② **14 条英文提示词按公式重写**：主体 / 场景 / 时间轴连续运动 / 运镜 / 声音 / 风格 / **运动铁律段** / **反向约束段**。末两段删了就会跑偏；
> ③ **玉兔一致性靠描述子锚定**——`pearly translucent fur … crimson-red scarf` 一段在 4 个出镜单元里一字不改照抄；剪影版单列。本地没有角色参考图输入位，描述子漂移比图参考更容易崩；
> ④ **慢节奏铁律落到具体镜头**：原文镜头 04「玉兔奔跑」改为**站桥栏一动不动**；「最燃」「全片最高潮」改为靠**月亮变大、海面变阔**实现，运动速度一分不提；
> ⑤ **提示词物化陷阱**（记忆既有教训）配了反向约束；U05b 人群只写 soft-blurred silhouettes 不写脸，U06b 只写 elderly hands 不写 figure；
> ⑥ **中文书法字幕与厦航 Logo 明确划给后期**（§7），不让模型编造品牌标识。
> **⚠️ 渠道冒烟（有界实验，打不出不计费）**：`MEAI_API_KEY` 的 `/v1/models` 回来 35 个模型**全是文本模型**；`video --model seedance-2.0` 报 **503 `No available channel for model seedance-2.0 under group default (distributor)`**；`image --model sd-2-c1` 提交过但轮询 404（`sd-*` 是文本模型）。**结论：该 key 今天既不能生图也不能生视频，只能对话——与 2026-07-19 记录一致，两个月未变。**
> **用户提供新 key 复测**：`sk-BErxl…` 后用户给 `sk-BErxlnnHRfulpnQm8OTj9ULQvwORGAXjR1cBRRpc61HK9xjN`，复测后 **同样 503**——`GET /v1/models` 35 个文本模型，`video --model seedance-2.0` 报 `No available channel for model seedance-2.0 under group default (distributor)`。**确认问题不在 key 有效性，而在 meai 后台未给该 key 开通图像/视频分组。**
> **首帧图盘点**：上周 6 张里 `s01`/`s03`/`s05`/`s06` 四张构图仍可用（`s05` 需裁成微距、`s06` 需重搭礁石构图），`s02` 报废（原为地面登机，新设计是云海登机廊桥）。**需新建 9 张**——同样卡在渠道上。
> **待用户定**：① 去 meai 后台给该 key 开通图像/视频分组，还是换已开通的 key（脚本读环境变量，直接 `MEAI_API_KEY=sk-xxx` 即可）② 画幅 2.35:1 / 16:9（提示词已按 2.35:1 写死，改要动 14 条）③ 有没有真实厦航 Logo 素材，没有就不合成、不自己画 ④ 要不要 BGM。
> **v1 未删**：`hometown-moon.mp4`（58.0s / 720p）留在盘上作 v2 对照基线，哈希已记在 `readme.md`。

> ## 2026-09-23 · 本地管线跑通 + 一个脚本坑（AI：Claude Code / step-5-preview）
> **已确认能跑**：`seedance-video` skill（shiping 平台）本机直连，key 在 `skills/seedance-video/.env`。实测：`image`(2K, 2 分) → `video`(video-v1, 10s, 11 分)。S1 全链路跑完。
> **已完成**：`content/jade-rabbit-hometown-moon/frames/s01_moon-palace_first-frame.png`（2K 2560×1440，兼玉兔定妆图）+ `clips/s01_moon-palace.mp4`（1280×720 / 24fps / 10.05s / h264+aac / 6.0MB / 无水印）。抽帧 1s·5s·9s 三帧查过：玉兔无漂移、无变形，红围巾与玉质完整，仅极缓慢推镜——慢节奏铁律过关。
> **⚠️ 脚本坑（首犯，记此备查）**：`seedance_api.py` 的 `download()` 用 `open(output,"wb")` 直接写，**不会创建输出子目录**。任务已 success、11 分已扣、URL 已打印，却因 `clips/` 不存在抛 `FileNotFoundError` 退出码 1，后台任务显示 "failed"——**视频其实生成了**。**规避：调用前先 `New-Item -ItemType Directory -Force` 建好目录**；若已中招，直接从日志里那条 `video_url`（`lr=unwatermarked` 去水印）用 Invoke-WebRequest 重下，不重复扣费。
> **落点定位**：`--output` 里 `~` 和相对路径在当前工作目录下解析，别依赖它。

> **待办**：~~S2–S6 首帧图生成~~ ~~六段视频~~ **全部完成**。成片已合成：`content/jade-rabbit-hometown-moon/hometown-moon.mp4`（58.0s / 1280×720 / 24fps / 28.9MB / 无水印）。四道验证闸：规格 ✅、音画对齐 ✅、慢节奏 ✅（抽帧玉兔无漂移）、中文字形 ✅（五字全对）。**首版→定稿返工 0 轮，人工介入 0 次。**
> **结构**：6 场 × 10.05s + 0.5s 交叉溶解 + 片头 1.2s 淡入 + 片尾 2.3s 淡出；「月是故乡明」落版 52.5–54.5s 淡入（华文行楷）。
> **已沉淀进 memory**（`seedance-video-skill` 2026-09-23 条）：① `download()` 不建子目录 → success 也报 failed ② drawtext 本机不可用（无 fontconfig）+ `filter_complex_script` 转义规则不同 → 中文落版最稳走 PIL 渲染 PNG + overlay alpha 淡入 ③ 本地无角色参考输入，一致性靠图生图链式传递 ④ shiping 上限 720p（此前记的 1080P 有误）。
> **仍悬而未决**（用户未答）：① 画幅 16:9 是否认（2.35:1 需后期加黑边）② 船政文化是否单独一场 ③ 要不要修 `seedance_api.py` 的 mkdir 坑（第三方 skill 文件，须先问）。
> **可选下一步**：配乐（现为平台自动环境音）· 1080p 超分。

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
