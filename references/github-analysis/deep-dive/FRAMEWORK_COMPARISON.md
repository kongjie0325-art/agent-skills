# 主流 Agent 框架内部架构对比

> Claude Code vs Codex vs Gemini CLI vs OpenHands vs Cline vs Roo Code

## 架构总览

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户交互层                                │
│  CLI (Terminal)  |  IDE (VS Code)  |  Web UI  |  API           │
└────────────┬────────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                      Agent Core（核心引擎）                      │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Planner    │  │   Context    │  │    Tool Executor     │  │
│  │  (规划决策)   │  │  Engine      │  │    (工具执行)         │  │
│  │              │  │  (上下文管理) │  │                      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                 │                      │               │
│  ┌──────▼─────────────────▼──────────────────────▼───────────┐  │
│  │                    Memory / RAG                           │  │
│  │         (CLAUDE.md / AGENTS.md / GEMINI.md)               │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Skills Layer（技能层）                         │  │
│  │    渐进式披露 → 按需加载 → 工作流编排 → 错误处理             │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Tools Layer（工具层）                          │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │  │
│  │  │   MCP    │  │   CLI    │  │  Plugin  │  │  Native  │ │  │
│  │  │  Server  │  │  Tools   │  │  Tools   │  │  Tools   │ │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 框架对比

### Claude Code (Anthropic)

```
.claude/
├── settings.json          # 全局配置
├── skills/                # 用户级 Skills
│   └── my-skill/SKILL.md
└── CLAUDE.md              # 项目记忆

.claude-plugin/
└── plugin.json            # Plugin 清单

.github/
└── skills/                # 仓库级 Skills
    └── code-review/SKILL.md
```

**特点**：
- Skills 最成熟，.claude/skills/ + .github/skills/ 双级别
- MCP 原生支持（stdio + HTTP）
- CLAUDE.md 作为 Memory 层
- Plugin 系统支持 .claude-plugin/manifest.json

### Codex CLI (OpenAI)

```
.agents/
├── skills/                # 仓库级 Skills
│   └── deploy/SKILL.md
└── AGENTS.md              # 项目记忆
```

**特点**：
- 仅支持 Skills，无 MCP
- .agents/skills/ 单级别
- AGENTS.md 作为 Memory
- 轻量级，专注编码

### Gemini CLI (Google)

```
.gemini/
├── skills/                # 用户级 Skills
│   └── testing/SKILL.md
├── GEMINI.md              # 项目记忆
└── settings.json          # 配置
```

**特点**：
- Skills + MCP 双支持
- .gemini/skills/ 单级别
- GEMINI.md 作为 Memory
- Extensions 系统（类似 Plugin）

### GitHub Copilot

```
.github/
├── copilot-instructions.md  # 自定义指令（Always-on）
├── skills/                  # Agent Skills（On-demand）
│   └── deploy/SKILL.md
├── instructions/            # Prompt 文件
│   └── api-design.instructions.md
└── plugin/                  # Plugin 系统
    ├── marketplace.json     # Marketplace 注册
    └── my-plugin/           # 已安装 Plugin
        ├── plugin.json
        ├── skills/
        ├── agents/
        └── hooks.json
```

**特点**：
- 最完整的 Skills + Agents + Plugins + Marketplace 四层体系
- Skills 和 Instructions 分离（Always-on vs On-demand）
- Plugin 可以包含 Skills + MCP + Hooks + LSP
- Marketplace 支持版本管理和分发

### Cursor

```
.cursor/
├── rules/                   # 规则（类似 Skills）
│   └── code-style.md
└── .cursorrules            # 全局规则
```

**特点**：
- 以 IDE 为中心
- Rules 系统（类似 Always-on Skills）
- MCP 支持
- 无独立 Plugin 系统

### OpenHands

```
skills/                      # 仓库级 Skills
└── debug/SKILL.md
```

**特点**：
- 开源自主编码框架
- Skills + MCP 支持
- 完整的 Agent 生命周期管理
- Docker 沙箱隔离

## 核心能力对比

| 能力 | Claude Code | Codex CLI | Gemini CLI | Copilot | Cursor | OpenHands |
|------|------------|-----------|------------|---------|--------|-----------|
| **Skills** | ✅ 双级别 | ✅ 单级别 | ✅ 单级别 | ✅ + Instructions | ✅ Rules | ✅ 单级别 |
| **MCP** | ✅ stdio+HTTP | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Memory** | CLAUDE.md | AGENTS.md | GEMINI.md | copilot-instructions.md | .cursorrules | - |
| **Plugin** | ✅ | ❌ | Extensions | ✅ Marketplace | ❌ | ❌ |
| **Custom Agents** | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ |
| **Hooks** | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Sandbox** | ✅ | ❌ | ❌ | ✅ Codespaces | ❌ | ✅ Docker |
| **PTY 模式** | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Web UI** | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |

## Skills 路径对比

| 工具 | 仓库级 | 用户级 | 全局 |
|------|--------|--------|------|
| Claude Code | .github/skills/ | .claude/skills/ | ~/.claude/skills/ |
| Codex CLI | .agents/skills/ | - | ~/.agents/skills/ |
| Gemini CLI | .gemini/skills/ | - | ~/.gemini/skills/ |
| Copilot CLI | .github/skills/ | - | ~/.copilot/skills/ |
| Cursor | .cursor/rules/ | - | ~/.cursor/rules/ |
| OpenHands | skills/ | - | - |

## 演进趋势

### 2024 → 2025 → 2026

```
2024: MCP 元年
  → 所有工具都走 MCP
  → Context 爆炸问题

2025: Skills 崛起
  → Agent Skills 开放标准
  → 渐进式披露解决 Context 问题
  → Skills ≠ MCP 成为共识

2026: 三层融合
  → Skills + MCP + Plugin 各司其职
  → CLI + Skills 模式兴起（Zilliz、Lark）
  → MCP over HTTP 留存企业场景
  → MCP over stdio 被 CLI+Skills 替代
```

### 关键事件

| 时间 | 事件 | 影响 |
|------|------|------|
| 2024.11 | Anthropic 发布 MCP | 工具调用标准化 |
| 2025.12 | GitHub Copilot 支持 Agent Skills | Skills 成为主流 |
| 2025.12 | Anthropic 开放 Skills 标准 | 跨平台 Skill 成为可能 |
| 2026.01 | VoltAgent/awesome-agent-skills 合集 | 1424+ Skills 生态 |
| 2026.04 | OX Security 披露 MCP RCE 漏洞 | MCP 安全性受到关注 |
| 2026.04 | MCP 捐赠给 Linux Foundation AAIF | MCP 进入成熟治理 |
| 2026.05 | Perplexity 公开弃用 MCP (stdio) | CLI+Skills 模式受关注 |
| 2026.05 | 14,000+ MCP Server，月下载 9700 万 | MCP 生态仍在增长 |

---

*最后更新：2026-07-07*
