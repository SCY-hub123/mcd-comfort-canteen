# workbuddy.md — WorkBuddy 开发对话记录

> 本项目使用腾讯 WorkBuddy 智能体开发，符合麦当劳程序员创意开发大赛 WorkBuddy 专项奖励要求。

## 📋 开发过程摘要

| 阶段 | 内容 |
|------|------|
| 选题 | 确定「麦麦治愈食堂」为主推项目（情绪陪伴 × 麦当劳），海报工坊为同源技术展示 |
| 环境 | WorkBuddy 自定义连接器接入麦当劳 MCP（`https://mcp.mcd.cn`），实测 35 个工具 |
| 安全设计 | 危机词检测脚本（`scripts/safety_guard.py`）在 MCP 调用前短路执行，热线信息经核实（12356 国家卫健委 7×24） |
| 数据 | `list-nutrition-foods` 拉取 160 项餐品真实营养数据，用于情绪配餐与份量锚点 |
| 演示 | 完整跑通「加班到十点」场景，产出 8 项合规自检全过的物料包 |
| 视觉 | 治愈卡片示例图（暖色调一人食特写，AI 绘图） |

## 🔒 Token 安全

本项目所有提交文件中**不含任何真实 MCP Token**——配置示例（`mcp-config.example.json`）仅使用 `YOUR_MCP_TOKEN` 占位符。请从 WorkBuddy 导出本项目的完整开发对话时，注意其中可能包含的敏感信息。

## 📎 导出说明

正式参赛前，请在 WorkBuddy 中导出本项目的完整开发对话上下文（Markdown 格式），替换/追加到本文件：

> 会话右上角菜单 → 导出对话（Markdown）

建议包含的对话片段：选题讨论 → MCP 连通性验证 → SAFETY.md 红线设计 → safety_guard.py 开发与三档测试 → 情绪映射表设计 → 「加班到十点」演示跑通 → 治愈卡片 Prompt 调优。
