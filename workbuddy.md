# workbuddy.md — WorkBuddy 开发对话上下文

> 本项目全程在腾讯 WorkBuddy 智能体中完成开发，符合麦当劳程序员创意开发大赛 WorkBuddy 专项奖励的提交要求。
> 记录形式：按开发时间线整理的关键会话节点（含用户原始指令与我方的执行动作）。
> 如需原始流水，可从 WorkBuddy 会话菜单「导出对话（Markdown）」追加至本文件末尾。

---

## 📌 项目信息

| 项 | 内容 |
|---|---|
| 项目名称 | 麦麦治愈食堂（mcd-comfort-canteen） |
| 开发平台 | 腾讯 WorkBuddy |
| 仓库 | https://github.com/SCY-hub123/mcd-comfort-canteen |
| MCP Server | mcd-mcp @ `https://mcp.mcd.cn`（Streamable HTTP） |
| 主用 MCP 工具 | `list-nutrition-foods`、`now-time-info`、`available-coupons` |

---

## 🗓 开发会话记录

### 【10-09】前置：赛事调研与 MCP 接入

**User**：（附麦当劳中国 Skill 开发比赛流程图）我想要参加这个比赛，我需要准备什么。

**Assistant**：抓取官方仓库 `M-China/mcd-developer-innovation-challenge` 真实规则（`activityGuidelines.md` / `README.md`），整理参赛准备清单：赛期 10-09~10-25、排名依据为 GitHub 公开 Star 数、前 100 名进榜、必需文件 5 项（README / CONTEST_DECLARATION / MCP_INTEGRATION / 源代码 / workbuddy.md）；并实测 40+ 已参赛项目，识别出「省钱薅券 / 热量营养 / 点餐流程」三大红海方向。

**User**：（提供麦当劳 MCP Token）

**Assistant**：直连验证 Token 有效（Server mcd-mcp v1.0.0），`tools/list` 返回 **35 个工具**（远超官方文档的 13 个），发现积分抽奖 / 麦麦商城 / 派对预订 / 企业团餐等无人涉足的能力域；真实调用 5 个核心工具（now-time-info / campaign-calendar / query-my-account / available-coupons / list-nutrition-foods）验证连通。

---

### 【10-10】第一项目实测：麦门海报工坊

**User**：配置好了，可以验证一下，选主题「麦门海报工坊」。

**Assistant**：搭建 `mcd-poster-studio`，封装 `scripts/mcd_client.py`（initialize → tools/call，兼容 SSE 与纯 JSON 响应），产出复古美式风海报与 9.9 早餐物料包。

**User**：给最近的麦当劳活动做个海报。

**Assistant**：按 SKILL.md 工作流 A 跑通：campaign-calendar 抓活动 → 提卖点 → 输出双风格文案 + AI 绘图 Prompt + 排版说明 + 发布时段建议。

**User**：差异化补充：给 skill 加一个「GD 联名」专属模板（潮酷黑金风海报）。

**Assistant**：从活动日历识别出联名是**三弹连发**（棒球帽 10-08 → 徽章 10-15 → 丝巾 10-22），产出黑金风联名物料包，提炼「收集线叙事」。

**User**：把「活动日历前瞻排期」写进 SKILL.md，并整理 10 月剩余追热点日历。

**Assistant**：新增「工作流 B：未来 7 日预热排期」，含 S/A/B 三级优先级与 T-7/T-1/T-0/T+1 倒计时逻辑；输出 12 个事件的追热点日历表。

---

### 【10-13】主推项目立项：麦麦治愈食堂

**User**：⭐ 麦麦治愈食堂：输入情绪 → 治愈套餐 + 治愈卡片（直接复用你心答小匣「先共情再解题」的产品逻辑）。

**Assistant**：立项后先做安全论证，再动手：

1. **核实热线（不凭记忆）**：检索确认 **12356** 为国家卫健委设立的全国统一心理援助热线（2025-05-01 开通，7×24，免费保密，已处理近 1 万起危机干预）；**12355** 为共青团中央青少年服务热线（14-35 岁）。
2. **识别合规张力**：大赛规则禁止「宣扬不健康饮食方式」，而情绪化进食本身踩线。据此设计——**吃饭仅为三个方案之一**，另两个方案必须是非进食的（一件小事 + 一句承认处境的话），且每次推荐必带热量与份量锚点，深夜 22:00 后自动降为 ≤300 kcal 轻食。
3. **工程化安全闸门**：编写 `scripts/safety_guard.py`，硬性规定其在**调用任何 MCP 工具之前**执行，命中危机词即短路返回、只输出热线卡片、绝不产生点餐动作。
4. **拉真实数据**：`list-nutrition-foods` 返回 160 项餐品营养数据（猪柳麦满分 308 kcal、板烧鸡腿麦满分 246 kcal、迷你薯条 106 kcal、玉米杯小 53 kcal 等），据此建立「情绪 → 方案映射表」（疲惫 / 低落 / 焦虑 / 孤独 / 烦躁 / 失眠深夜 / 需要被哄）。

**实测验证**：三档分流测试通过——普通情绪 `ALL_CLEAR` 放行、危机词「不想活 / 撑不下去」命中 `CRISIS` 并中止、软信号附加提示。

**完整演示**：用真实数据跑通「今天加班到十点，整个人都空了」场景，输出 ①猪柳麦满分 308 + 玉米杯 53（合计 361 kcal，带份量说明）②设 25 分钟倒计时，什么都不做 ③「今天剩下的部分，及格就行。」，附 8 项合规自检全过。

---

### 【10-14】主推策略与参赛准备

**User**：（在「合并 / 二选一主推 / 分两个号」中）选 2。

**Assistant**：主推治愈食堂，海报工坊转为技术展示。两项目 README 完成定位互链；补齐本项目 `workbuddy.md` 与 `.gitignore`；全文件 Token 扫描确认为零泄露。

### 【10-16】上线与报名

**User**：（提供 GitHub Token）

**Assistant**：代办建仓、上传、发报名 Issue 全流程。两个仓库均 PUBLIC 且必需文件齐全，报名 Issue #778（治愈食堂）、#779（海报工坊）提交并审核通过。

---

## 🧩 关键技术与产品产出

| 类别 | 产出 |
|------|------|
| 安全工程 | `scripts/safety_guard.py`（三档分流 CRISIS / SOFT / ALL_CLEAR，MCP 调用前短路） |
| 合规文档 | `SAFETY.md`（五条红线：危机词触发热线、禁诊断、禁鸡汤、反情绪性进食、数据本地） |
| 产品逻辑 | `SKILL.md`（四步不可跳步：接住情绪 → 弹窗询问 → 三方案 → 才问下单） |
| 数据支撑 | 160 项真实营养数据驱动的「情绪 → 方案映射表」 |
| 视觉 | 治愈卡片示例图（暖色调一人食特写，3:4） |

## 🔒 Token 安全

仓库内所有配置文件仅使用 `YOUR_MCP_TOKEN` 占位符，`.gitignore` 已屏蔽敏感文件，提交前经扫描确认无真实 Token。

## ✅ 参赛核验清单

- [x] 项目使用腾讯 WorkBuddy 智能体开发
- [x] 真实使用麦当劳 MCP 能力（`list-nutrition-foods` 等）
- [x] 含 README.md / CONTEST_DECLARATION.md / MCP_INTEGRATION.md / 源代码 / workbuddy.md
- [x] 仓库公开可访问
- [x] 报名 Issue 审核通过（#778）
