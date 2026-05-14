# 各工具适配说明

这段 Markdown 模板是一段通用的系统指令。放到不同工具的不同位置就能用。内容完全相同，只需放到正确的文件路径或配置字段。

## 快速对照表

| 工具 | 配置文件路径 | 如何生效 | 对话效果 |
|------|------------|---------|:---:|
| **Claude Code** | `~/CLAUDE.md` | 重启 Claude Code 自动加载 | ⭐⭐⭐ 完整 |
| **Cursor** | 项目根目录 `.cursorrules` | 打开项目自动加载；也可以在 Settings → Rules for AI 粘贴 | ⭐⭐⭐ 完整 |
| **Windsurf** | 项目根目录 `.windsurfrules` | 启动时自动加载 | ⭐⭐⭐ 完整 |
| **GitHub Copilot** | 项目根目录 `.github/copilot-instructions.md` | 每次对话请求时注入 | ⭐⭐ 对话中生效，Tab 补全不触发 |
| **Codex CLI** | 项目根目录 `AGENTS.md` 或 `CODEBUDDY.md` | 启动时加载 | ⭐⭐⭐ 完整 |
| **Cline / Roo Code** | 项目根目录 `.clinerules` | 启动时加载 | ⭐⭐⭐ 完整 |
| **Aider** | `.aider.conf.yml` 中的 `system_prompt` 字段，或项目根目录 `CONVENTIONS.md` | 启动时加载 | ⭐⭐ 取决于模式 |
| **Amazon Q Developer** | Settings → Custom Instructions | 请求时注入 | ⭐⭐ 可用 |

## 详细操作步骤

### Claude Code

```bash
cp template/CLAUDE.md.template ~/CLAUDE.md
# 编辑 ~/CLAUDE.md，填入你的信息
# 重启 Claude Code 即生效
```

### Cursor

**方式 A：项目级配置**
```bash
cp template/CLAUDE.md.template .cursorrules
```

**方式 B：全局配置**
Cursor → Settings → Cursor Settings → Rules for AI → 粘贴模板内容

### Windsurf

```bash
cp template/CLAUDE.md.template .windsurfrules
```

### GitHub Copilot

```bash
mkdir -p .github
cp template/CLAUDE.md.template .github/copilot-instructions.md
```

注意：Copilot 在代码补全（Tab）时不读取此文件，仅在对话模式（Chat）中生效。

### Codex / OpenAI Codex CLI

```bash
cp template/CLAUDE.md.template AGENTS.md
# 或
cp template/CLAUDE.md.template CODEBUDDY.md
```

### Cline / Roo Code (VS Code 插件)

```bash
cp template/CLAUDE.md.template .clinerules
```

### 其他工具

几乎所有 AI 编程工具都支持自定义系统指令。在 Settings 搜索以下关键词找到对应字段：

- `instructions`
- `system prompt`
- `rules`
- `custom prompt`
- `personality`

找到后粘贴模板全部内容即可。

## 多个工具一起用

如果你同时用 Claude Code + Cursor，在两个工具里放同一份内容即可：

```bash
cp template/CLAUDE.md.template ~/CLAUDE.md        # Claude Code
cp template/CLAUDE.md.template .cursorrules       # Cursor
```

两份内容一样。改了其中一份后，手动同步另一份。或者用 symlink：

```bash
ln -sf ~/CLAUDE.md .cursorrules
```

## 内存系统路径说明

模板中引用的记忆系统路径 `~/.ai-memory/pending_review.md` 和 `~/.claude/scheduler-status/` 是建议路径。你可以改到任何地方——只要修改模板中对应的路径即可。

不同工具对文件系统访问权限不同：
- Claude Code、Cline、Codex 支持完整的文件读写
- Cursor Agent 模式下可以访问文件
- Copilot Chat 模式文件访问受限

如果你的工具不支持文件读写，记忆系统那一段（第三层）的效果会打折，但前两层（灵魂设定 + Mentor Mode）仍然完整生效。
