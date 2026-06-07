# Plugin 深度解析 — 封装好的功能

## 目录
- [一、Plugin 是什么](#一plugin-是什么)
- [二、Plugin 的结构](#二plugin-的结构)
- [三、Plugin vs Skill vs MCP 的关系](#三plugin-vs-skill-vs-mcp-的关系)
- [四、Plugin 的类型](#四plugin-的类型)
- [五、Claude Code Plugin 详解](#五claude-code-plugin-详解)
- [六、OpenAI Codex Plugin 详解](#六openai-codex-plugin-详解)
- [七、IDE 插件（VS Code / JetBrains）](#七ide-插件-vs-code--jetbrains)
- [八、Plugin 的优缺点](#八plugin-的优缺点)

---

## 一、Plugin 是什么

**Plugin = Skills + MCP + Hooks + Slash Commands 的打包单元**

如果说 Skills 是入职指南、MCP 是管道，那 Plugin 就是你交给团队的成品工具。

> "Skills are onboarding guides and MCP is plumbing, Plugins are the finished product you hand to a team."
> — Aaron Ott

### 核心定位
- **Skills** 告诉 Agent 怎么做
- **MCP** 让 Agent 能操作外部系统
- **Plugin** 把以上两者打包成一个开箱即用的产品

---

## 二、Plugin 的结构

### Claude Code Plugin 结构
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # 插件清单（必需）
├── skills/                  # 包含的 Skills
│   └── code-review/
│       └── SKILL.md
├── agents/                  # 包含的 Sub-agents
│   └── security-reviewer/
│       └── AGENT.md
├── hooks/                   # 包含的 Hooks
│   └── pre-commit.sh
├── commands/                # 包含的 Slash Commands
│   └── deploy.md
└── mcp.json                 # MCP Server 配置（可选）
```

### plugin.json 清单
```json
{
  "name": "engineering-team-pack",
  "description": "Complete engineering workflow: code review, deployment, security scanning",
  "version": "1.0.0",
  "skills": ["./skills/code-review", "./skills/deploy-checklist"],
  "agents": ["./agents/security-reviewer"],
  "hooks": {
    "PreToolUse": ["./hooks/block-dangerous-commands.sh"],
    "PostToolUse": ["./hooks/run-linter.sh"]
  },
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

---

## 三、Plugin vs Skill vs MCP 的关系

```
┌──────────────────────────────────────────────────┐
│                    Plugin                         │
│  ┌──────────┐  ┌──────────┐  ┌────────────────┐ │
│  │  Skill 1  │  │  Skill 2  │  │   MCP Config   │ │
│  │(知识)     │  │(流程)     │  │  (工具连接)     │ │
│  └──────────┘  └──────────┘  └────────────────┘ │
│  ┌──────────┐  ┌──────────┐                      │
│  │  Hook 1   │  │  Agent 1  │                     │
│  │(安全拦截) │  │(子代理)    │                     │
│  └──────────┘  └──────────┘                      │
└──────────────────────────────────────────────────┘
```

**关键关系**：
- Plugin **包含** Skills（一个 Plugin 可以有多个 Skill）
- Plugin **引用** MCP Servers（通过 mcp.json 配置）
- Plugin **配置** Hooks（生命周期拦截器）
- Skills **可以独立于** Plugin 存在
- MCP **可以独立于** Plugin 存在
- 但 Plugin 是最终的"交付物"

---

## 四、Plugin 的类型

### 按功能分

| 类型 | 说明 | 示例 |
|------|------|------|
| **工作流 Plugin** | 完整的工作流编排 | 部署流水线、事件响应 |
| **领域 Plugin** | 特定领域的全套能力 | 法律（NDA审查）、销售（CRM集成）|
| **安全 Plugin** | 安全检查和合规 | SAST扫描、密钥检测 |
| **集成 Plugin** | 第三方服务集成 | Jira/Notion/Slack 集成 |

### 按范围分

| 类型 | 说明 |
|------|------|
| **个人 Plugin** | 个人的工作习惯和工具 |
| **团队 Plugin** | 团队共享的流程和标准 |
| **组织 Plugin** | 组织级别的合规和治理 |

---

## 五、Claude Code Plugin 详解

### Plugin Marketplace
Claude Code 2026-01 引入了 Plugin 市场：

```bash
# 浏览 Plugin 市场
/plugin marketplace add <source>

# 安装 Plugin
/plugin install my-plugin

# 查看已安装 Plugin
/plugin list
```

### 安装方式
1. **Plugin Marketplace** — 通过 `/plugin marketplace` 命令
2. **直接安装** — 手动将文件放到 `.claude/plugins/`
3. **Git 仓库** — 从 GitHub 安装

### 配置层级
Claude Code 的配置是 5 层级联：
```
Managed Settings (组织)     ← 最高优先级
  → Command Line (命令行)
    → Local Project (.claude/)
      → Shared Project (.claude/)
        → User Defaults (~/.claude/)  ← 最低优先级
```

---

## 六、OpenAI Codex Plugin 详解

### Codex 的 Plugin 定义
> "Plugins help Codex connect to other tools and sources of information."
> — OpenAI 官方

### 与 Claude Code 的区别

| 维度 | Claude Code Plugin | OpenAI Codex Plugin |
|------|-------------------|-------------------|
| **核心定位** | 打包 Skills+Hooks+MCP | 连接外部工具和信息源 |
| **安装方式** | `/plugin` 命令 + Marketplace | UI 选择 + 手动创建 |
| **技术门槛** | 中等（需要写 JSON） | 较高（需要技术知识） |
| **核心文件** | `plugin.json` | 无标准格式 |
| **开源** | 是（GitHub 可查） | 部分 |

### Codex 的 Skills vs Plugins
| 场景 | 使用 |
|------|------|
| Codex 需要从某工具获取信息 | **Plugin**（连接 Google Drive、邮箱等）|
| Codex 需要遵循你的流程 | **Skill**（团队规范、工作流）|
| 两者都要 | **Both** |

---

## 七、IDE 插件（VS Code / JetBrains）

### VS Code 扩展 vs MCP vs Skills

| 机制 | 说明 | 示例 |
|------|------|------|
| **VS Code 扩展** | 完整的 IDE 功能扩展 | Cline、Roo Code、GitHub Copilot |
| **MCP Server** | 工具接入（被扩展调用） | GitHub MCP、Filesystem MCP |
| **SKILL.md** | 指令文档（被扩展读取） | Cline 的 `.cline/skills/` |
| **.cursorrules** | Cursor 的项目规则 | 编码规范、架构约束 |

### 各 IDE 的"Plugin"叫法

| IDE/工具 | 扩展机制 | 说明 |
|----------|----------|------|
| VS Code | Extensions | 完整的扩展 API |
| Cursor | .cursorrules + Extensions | 规则文件 + 扩展 |
| Cline | .cline/skills/ + MCP | Skills + MCP |
| Roo Code | .roo/ + Extensions | 类似 Cline |
| JetBrains | Plugins | 传统插件系统 |

---

## 八、Plugin 的优缺点

### 优点
1. **开箱即用** — 安装即可使用
2. **用户门槛低** — 适合非技术团队
3. **打包完整** — Skills + MCP + Hooks 一体化
4. **某些场景体验好** — Jira/Notion/Slack 集成

### 缺点
1. **不通用** — 很多只能在某个平台使用
2. **Agent 理解较弱** — 通常只是输入→输出模式
3. **难组合** — 插件之间互相不知道存在
4. **锁定效应** — 依赖特定平台/框架

---

**下一节 →** [04-memory-and-hooks.md](./04-memory-and-hooks.md) — Memory + Hooks 机制
