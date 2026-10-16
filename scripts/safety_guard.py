#!/usr/bin/env python3
"""
safety_guard.py — 危机信号检测（麦麦治愈食堂第一道闸门）

设计原则：
1. 在调用任何 MCP 工具【之前】执行，命中即短路，绝不产生点餐动作；
2. 宁可误报，不可漏报 —— 情绪陪伴产品的安全边界应当保守；
3. 只做"是否命中"判断，绝不做心理诊断或性质判定。

用法:
    python3 safety_guard.py "今天加班到十点，整个人都空了"
    → ALL_CLEAR  （放行，进入常规流程）

    python3 safety_guard.py "真的撑不下去了，不想活了"
    → CRISIS     （输出热线卡片，中止流程）

退出码: 0 = 放行, 1 = 命中危机信号
"""
import sys, re

# ── 危机信号词表（持续维护） ──────────────────────────────
CRISIS_PATTERNS = [
    # 自杀 / 自伤
    r"不想活", r"活不下去", r"活够了", r"想死", r"自杀", r"轻生",
    r"结束一切", r"了结(自己|生命)?", r"结束生命", r"去死",
    r"割腕", r"自残", r"自伤", r"伤害自己", r"想让自己疼", r"扎自己",
    # 绝望 / 告别暗示
    r"撑不下去", r"撑不住了", r"扛不住了", r"没意义了", r"活着没意思",
    r"消失就好了", r"消失算了", r"没有人会在意", r"没人会在乎",
    r"再也见不到", r"最后一次", r"想一直睡下去", r"睡过去算了",
    r"不想醒来", r"放弃自己", r"不要我了也没关系",
]

# ── 高危但需结合语境的软信号（命中仅提示，不强制中止）──────
SOFT_SIGNALS = [
    r"好累.*活着", r"好想消失", r"太痛苦了", r"崩溃了.*(好|想)",
    r"哭了一整", r"整夜没睡", r"一个人.*(很久|好几年)",
]

HOTLINE_CARD = """
🆘 先停一下，你现在的感受值得被认真对待。

请现在就拨打（免费、保密、7×24 小时）：
📞 12356 — 全国统一心理援助热线（国家卫生健康委设立）
      情绪疏导 / 心理危机干预 / 支持匿名通话
📞 12355 — 青少年服务热线（14-35 岁，成长·学业·家庭困扰）

如果你身边有人能陪你，请现在告诉他/她。
如果你正处于医疗急难中，请拨打 120。

麦麦可以等，你不用。
"""

SOFT_HINT = "\n（如果你是认真地在说这件事，也可以拨打 12356，有人会听你说。）"


def check(text: str) -> tuple[str, list]:
    """返回 (状态, 命中模式列表)；状态为 CRISIS / SOFT / ALL_CLEAR"""
    hits = [p for p in CRISIS_PATTERNS if re.search(p, text)]
    if hits:
        return "CRISIS", hits
    soft = [p for p in SOFT_SIGNALS if re.search(p, text)]
    if soft:
        return "SOFT", soft
    return "ALL_CLEAR", []


def main():
    if len(sys.argv) < 2:
        print("用法: python3 safety_guard.py \"用户输入的原话\"")
        sys.exit(2)
    user_text = sys.argv[1]
    status, hits = check(user_text)

    if status == "CRISIS":
        print("[CRISIS] 命中危机信号，已中止常规流程，输出热线卡片：")
        print(HOTLINE_CARD)
        print(f"（命中模式：{hits}）")
        sys.exit(1)
    elif status == "SOFT":
        print("[SOFT] 检测到需关注的表达，正常输出方案，并附软提示：")
        print(SOFT_HINT)
        sys.exit(0)
    else:
        print("[ALL_CLEAR] 未检测到危机信号，进入常规流程。")
        sys.exit(0)


if __name__ == "__main__":
    main()
