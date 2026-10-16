# MCP_INTEGRATION.md — 麦当劳 MCP 接入说明

## 一、使用的 MCP Server

| 项目 | 值 |
|------|-----|
| Server | mcd-mcp（麦当劳中国官方 MCP Server） |
| 地址 | `https://mcp.mcd.cn` |
| 协议 | MCP Streamable HTTP，版本 2025-03-26 |
| 鉴权 | `Authorization: Bearer <Token>`，Token 于 [open.mcd.cn](https://open.mcd.cn/mcp) 免费激活 |

## 二、实际使用的 Tool

| Tool | 作用 | 调用时机 |
|------|------|---------|
| `list-nutrition-foods` | 获取 160 项餐品的能量/蛋白/脂肪/碳水/钠/钙 | **核心**：推荐与份量锚点的数据基础 |
| `now-time-info` | 获取当前时段 | 判断是否为深夜（22:00+），触发轻食规则 |
| `available-coupons` | 可领优惠券 | 用户主动问价后才查 |
| `query-meals` | 餐品列表 | 需精确到门店可售时才调 |
| `calculate-price` | 算价（含券） | 用户明确要下单时才调 |

> **克制的调用设计**：情绪陪伴场景里，任何过早出现的商品信息都会把「被接住」变成「被推销」。因此本 Skill 把商品类工具（`query-meals` / `calculate-price` / `available-coupons`）严格放在**用户点头之后**，且默认不主动提券。

## 三、调用流程

```
① safety_guard.py（本地，先于一切）
   └─ CRISIS → 输出 12356/12355 热线卡片，终止，不触达 MCP
   └─ SOFT / ALL_CLEAR → 继续

② now-time-info（MCP）
   └─ 判断时段 → 22:00+ 启用「深夜轻食 ≤300 kcal」规则

③ 情绪命名 + 承认式共情（不调用 MCP，纯对话层）

④ 弹窗询问「需要我帮你安排点什么吗？」

⑤ 用户同意后：
   list-nutrition-foods（MCP）→ 按情绪映射筛选 → 组餐 → 输出热量与份量锚点
   同时输出：一件非进食的小事 + 一句承认处境的话

⑥ 用户问价才调：available-coupons → query-meals → calculate-price
```

## 四、业务价值

1. **把营养数据用在情绪场景**：`list-nutrition-foods` 通常用于减脂控卡，本项目把它用作「照顾自己的刻度」——推荐的不只是吃什么，而是「吃多少刚刚好」；
2. **合规即产品**：`safety_guard.py` 是把情绪陪伴产品的安全边界工程化的尝试（危机词短路 + 禁诊断 + 禁鸡汤 + 反情绪性进食），可直接被同类产品复用；
3. **差异化**：场上同类 Skill 解决「怎么点得更快/更省/更健康」，本 Skill 解决「今天很糟的时候，怎么照顾自己一顿」——服务的是情绪时刻，不是交易环节。

## 五、隐私

情绪输入与点餐偏好仅存本地，不上传、不做云端画像、不设社区与分享。
