#!/usr/bin/env python3
"""
AI 编程工具人格配置 - 交互式向导
通过 11 个关键问题，帮你生成一份完全个性化的配置文件，
自动适配 Claude Code、Cursor、Windsurf、Copilot 等工具。
"""

import os
import sys
from datetime import datetime

# ── 工具路径映射 ──────────────────────────────────────────

TOOL_PATHS = {
    "1": {"name": "Claude Code", "path": "~/CLAUDE.md"},
    "2": {"name": "Cursor", "path": ".cursorrules"},
    "3": {"name": "Windsurf", "path": ".windsurfrules"},
    "4": {"name": "GitHub Copilot", "path": ".github/copilot-instructions.md"},
    "5": {"name": "Codex / OpenAI Codex CLI", "path": "AGENTS.md"},
    "6": {"name": "Cline / Roo Code", "path": ".clinerules"},
}

# ── 问题定义 ──────────────────────────────────────────────

QUESTIONS = [
    {
        "id": "tool",
        "text": "你主要用哪个 AI 编程工具？\n"
                "  1) Claude Code  2) Cursor  3) Windsurf\n"
                "  4) GitHub Copilot  5) Codex / Codex CLI  6) Cline / Roo Code",
        "example": "如果不在上面，输入你的工具名和配置文件路径，例如：Aider=.aider.conf.yml",
    },
    {
        "id": "name",
        "text": "怎么称呼你？（名字 / 昵称）",
        "example": "例如：老王、小明、强哥",
    },
    {
        "id": "background",
        "text": "用一句话描述你的职业背景",
        "example": "例如：前大厂运营，现在转型创业 + 自媒体",
    },
    {
        "id": "focus",
        "text": "你目前最关注的方向是什么？（2-3 个关键词，逗号分隔）",
        "example": "例如：AI+增长、一人公司、自媒体变现",
    },
    {
        "id": "usage",
        "text": "你每天用 AI 编程工具主要做什么？（多选，逗号分隔）\n"
                "  a) 写代码  b) 写文案/内容  c) 做调研分析\n"
                "  d) 面试准备  e) 商业决策  f) 学习研究  g) 日常杂务",
        "example": "例如：b,d,e 或 b,c,f",
    },
    {
        "id": "role",
        "text": "你希望 AI 在你面前是什么角色？\n"
                "  a) 导师 — 挑战我的想法，推我深入思考\n"
                "  b) 战友 — 平等讨论，互相启发\n"
                "  c) 执行者 — 我说什么做什么，别废话\n"
                "  d) 混搭 — 决策时像导师，执行时像工具",
        "example": "例如：d",
    },
    {
        "id": "pet_peeves",
        "text": "你最受不了 AI 什么毛病？（多选，逗号分隔）\n"
                "  a) 说废话绕圈子  b) 讨好我，从不说不对\n"
                "  c) 从不质疑我  d) 记不住前面说的话\n"
                "  e) 太啰嗦，输出太长",
        "example": "例如：b,c 或 a,b,c",
    },
    {
        "id": "pitfalls",
        "text": "你有什么反复踩的坑，希望 AI 帮你盯着？\n（可以是任何事——工作习惯、决策模式、内容创作...）",
        "example": "例如：面试准备时总是准备太多不会考的 / 做视频时容易陷进工具选型 / 情绪低落时容易冲动做决定",
    },
    {
        "id": "content_prefs",
        "text": "你写内容时有什么偏好？\n（语言、风格、平台、输出格式...）",
        "example": "例如：中文为主，口播风格，小红书+公众号，不要 emoji，写口播稿时直接给可录版本",
    },
    {
        "id": "paths",
        "text": "你有哪些常用路径想让 AI 记住？\n（知识库、项目目录、常用文件...）格式：名称=路径，逗号分隔",
        "example": "例如：Obsidian=~/Documents/知识库, 项目=~/my-project",
    },
    {
        "id": "extra",
        "text": "还有什么特别想让 AI 知道的吗？\n（自由补充，直接回车跳过）",
        "example": "",
    },
]

# ── 人格规则生成 ──────────────────────────────────────────

def generate_dont_rules(peeves):
    """根据用户的痛点，生成对应的'不要做的'规则"""
    rules = [
        "不要为了挑战而挑战（变成杠精）",
        "不要事事都先质疑（让人觉得烦）",
        "不要接受错误的前提就直接执行（这是失职）",
    ]
    extras = {
        "a": "不要说废话和绕圈子。如果回答可以 50 字说清楚，不要写 200 字。先给结论，再给解释。",
        "b": "不要在关键决定上迎合我。我有问题的时候直接指出，不要附和。",
        "c": "我让你'看看'或'复盘'时，先讲问题再讲方案。不要先说'我觉得你做得挺好的'。",
        "d": "跨会话时要主动回溯之前的结论。如果某个东西之前聊过，先确认'上次我们讨论的结果是XX，要不要参照这个继续？'",
        "e": "控制输出长度。执行型任务不要加总结或建议，信息型不要延展。",
    }
    for code in peeves:
        rule = extras.get(code.strip())
        if rule:
            rules.append(rule)
    return rules


def generate_triggers(pitfalls):
    """根据用户反复踩的坑，生成特殊触发规则"""
    if not pitfalls.strip():
        return ""
    lines = [
        "\n**特别触发（基于你反复踩的坑）：**",
        pitfalls.strip(),
        "",
    ]
    return "\n".join(lines)


def generate_usage_context(usage_codes):
    """根据使用场景生成使用模式描述"""
    usage_map = {
        "a": "写代码",
        "b": "写文案和内容创作",
        "c": "做调研分析",
        "d": "面试准备",
        "e": "商业决策",
        "f": "学习研究",
        "g": "日常杂务",
    }
    contexts = [usage_map.get(c.strip(), c.strip()) for c in usage_codes]
    return "、".join(contexts)


def resolve_output_path(tool_answer, name):
    """根据用户选择或输入，解析最终输出路径"""
    # 检查是否是预设编号
    tool = TOOL_PATHS.get(tool_answer.strip())

    if tool:
        path = os.path.expanduser(tool["path"])
        tool_name = tool["name"]
        return path, tool_name

    # 否则用户输入的是自定义路径
    custom = tool_answer.strip()
    if "=" in custom:
        tool_name, path = custom.split("=", 1)
        path = os.path.expanduser(path.strip())
        return path, tool_name.strip()
    else:
        # 默认当作文件路径
        path = os.path.expanduser(custom)
        return path, "自定义"


def generate(claude_md_template_path, answers):
    """用答案填充模板"""
    name = answers.get("name", "我")
    background = answers.get("background", "")
    focus = answers.get("focus", "")
    usage = answers.get("usage", "")
    role = answers.get("role", "d")
    peeves = [p.strip() for p in answers.get("pet_peeves", "").split(",") if p.strip()]
    pitfalls = answers.get("pitfalls", "")
    content_prefs = answers.get("content_prefs", "")
    paths_raw = answers.get("paths", "")
    extra = answers.get("extra", "")

    # 解析路径
    path_lines = []
    if paths_raw.strip():
        for item in paths_raw.split(","):
            item = item.strip()
            if "=" in item:
                label, p = item.split("=", 1)
                path_lines.append(f"- {label.strip()}：`{p.strip()}`")

    # 解析研究方向
    focus_items = [f.strip() for f in focus.split(",") if f.strip()]

    # 生成不要做的规则
    dont_rules = generate_dont_rules(peeves)

    # 读取模板
    with open(claude_md_template_path, "r") as f:
        template = f.read()

    # 替换基础占位符
    template = template.replace("[你的称呼]", name)

    # 替换背景区域
    background_section = (
        f"- 跟我差不多：理性、务实、不矫情。\n"
        f"- {background}\n"
    )
    if focus_items:
        background_section += f"- 核心研究方向：\n"
        for i, item in enumerate(focus_items, 1):
            background_section += f"  {i}. {item}\n"

    # 替换 "[用 3-5 句话描述你自己" 标记
    old_content_marker = "- [用 3-5 句话描述你自己"
    template = template.replace(
        old_content_marker,
        background_section.strip()
    )

    # 清理可选注释
    import re
    pattern = r'\[可选：.*?\]\n'
    template = re.sub(pattern, '', template, flags=re.DOTALL)

    # 如果用户提供了 pitfalls，插入特殊触发
    if pitfalls.strip():
        trigger_insert = (
            f"\n**特别触发（基于你反复踩的坑）：**\n"
            f"当涉及以下情况时，先提醒再行动：\n"
            f"{pitfalls}\n"
        )
        template = template.replace(
            "**不要做的：**",
            f"**不要做的：**\n{trigger_insert}"
        )

    return template


# ── 主流程 ──────────────────────────────────────────────────

def main():
    print("\n" + "=" * 60)
    print("  AI 编程工具人格配置 - 交互式向导")
    print("  回答 11 个问题，生成你专属的配置文件")
    print("=" * 60)
    print("\n提示：直接回车 = 保留默认值；输入 skip = 跳过此题\n")

    answers = {}
    for q in QUESTIONS:
        print(f"\n── 问题 {QUESTIONS.index(q)+1}/{len(QUESTIONS)} ──")
        print(f"  {q['text']}")
        if q["example"]:
            print(f"    {q['example']}")

        answer = input("   > ").strip()
        if answer.lower() == "skip":
            answer = ""
        answers[q["id"]] = answer

    # 找到模板路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "..", "template", "CLAUDE.md.template")

    if not os.path.exists(template_path):
        print("\n  template/CLAUDE.md.template   ")
        sys.exit(1)

    # 解析工具和输出路径
    tool_answer = answers.get("tool", "1")
    output_path, tool_name = resolve_output_path(tool_answer, answers.get("name", ""))

    # 生成内容
    result = generate(template_path, answers)

    # 处理 Copilot 的特殊路径
    if tool_answer.strip() == "4":
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 备份旧配置
    if os.path.exists(output_path):
        backup = output_path + f".backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename(output_path, backup)
        print(f"\n 旧配置已备份到: {backup}")

    # 写入
    with open(output_path, "w") as f:
        f.write(result)

    print(f"\n  已生成: {output_path}")
    print(f"  适配工具: {tool_name}")
    print("\n" + "=" * 60)
    print("  下一步：")
    print(f"  1. 打开 {output_path}，检查内容是否符合预期")
    print("  2. 重启你的 AI 编程工具，新人格生效")
    print("  3. 不满意？随时重新运行本脚本，旧配置会自动备份")
    print("=" * 60)

    # 如果用户用多个工具，提醒
    print(f"\n   如果你也同时用其他工具，把同一份内容复制到对应路径：")
    for key, tool in TOOL_PATHS.items():
        if tool["name"] != tool_name:
            print(f"    {tool['name']}: {tool['path']}")
    print()


if __name__ == "__main__":
    main()
