# Plugin 深度解析

## 什么是 Plugin

**Plugin（插件）** 是封装好的功能模块，安装即用。

与 MCP 和 Skills 不同，Plugin 是 **平台绑定的** — 每个 Agent 框架有自己的插件系统和 API。

> Plugin = 平台特定的功能扩展包

---

## 各框架的 Plugin 实现

### Claude Code Plugin

Claude Code 的 Plugin 是最完善的插件体系之一。

一个 Claude Code Plugin 可以包含：

```
my-plugin/
├── SKILL.md          # 核心 Skill 文件（必选）
├── commands/         # 自定义斜杠命令
│   └── my-command.md
├── agents/           # 子 Agent 定义
│   └── my-agent.md
├── hooks/            # 事件钩子
│   ├── pre-tool-execution.md
│   └── post-response.md
└── mcp.json          # MCP 服务器配置
```

**支持的组件：**

| 组件 | 说明 |
|------|------|
| **Skills** | 工作流和流程模板 |
| **Slash Commands** | `deploy`、`/review` 等自定义命令 |
| **Subagents** | 专门化的子 Agent |
| **Hooks** | 事件触发脚本（29 种钩子） |
| **MCP Servers** | 内置的 MCP Server 配置 |

**Plugin Marketplace：**

Claude Code 有官方的插件市场，通过 `/plugin marketplace` 命令安装。

### Codex CLI

Codex CLI 不支持传统意义上的 "Plugin"。它的扩展方式：

| 机制 | 说明 |
|------|------|
| **AGENTS.md** | 全局 + 项目级指令文件 |
| **MCP 服务器** | 通过 Codex 的 MCP 客户端加载 |
| **Shell 脚本** | 自定义辅助脚本 |
| **Prompt 模板** | `.codex/` 目录下的预设提示 |

### Cline (VS Code Extension)

| 机制 | 说明 |
|------|------|
| **MCP Servers** | 第一等支持，专门 UI 管理 |
| **.clinerules** | 项目级规则文件 |
| **自定义模式** | 通过 Mode 配置文件 |

### Roo Code

| 机制 | 说明 |
|------|------|
| **MCP Servers** | 类 Cline，但更好（多模式支持） |
| **自定义 Mode** | 多 Agent 人格模式 |
| **Modes Marketplace** | 社区模式市场 |

### OpenHands

| 机制 | 说明 |
|------|------|
| **SDK 插件** | Python SDK 扩展 |
| **MCP 兼容** | 2025 年后添加 MCP 支持 |
| **多 Agent 编排** | 内置多 Agent 协调 |

---

## Plugin 的优点

| 优点 | 说明 |
|------|------|
| **📦 开箱即用** | 安装即用，无需配置 |
| **👤 用户门槛低** | 不需要懂编程也能用 |
| **🎯 特定场景体验好** | Jira/Notion/Slack 等插件一键集成 |
| **🏪 有市场** | 官方/社区市场方便发现 |

---

## Plugin 的缺点

| 缺点 | 说明 |
|------|------|
| **🔗 平台绑定** | Claude Code 的 Plugin 不能在 Codex 上用 |
| **🧠 Agent 理解较弱** | 通常是简单的 输入→输出 模式 |
| **🧩 难组合** | 插件之间互相不知道对方存在 |
| **🔄 更新负担** | 平台升级可能需要插件适配 |
| **🔍 质量不一** | 社区插件缺少审核机制 |

---

## Plugin vs MCP vs Skills

| 维度 | Plugin | MCP | Skills |
|------|--------|-----|-------|
| 平台绑定 | ✅ 强 | ❌ 开放标准 | ❌ 跨平台 |
| 安装复杂度 | 极低 | 中 | 极低 |
| 复杂逻辑 | 有限 | 高 | 高 |
| 组件组合 | 差 | 好 | 好 |
| 生态规模 | 中等 | 3000+ | 1000+ |
| 生命力 | 平台决定 | 社区驱动 | 社区驱动 |

---

## Plugin 开发指南

### Claude Code Plugin 开发

```bash
# 创建插件骨架
mkdir my-plugin
cd my-plugin

# 核心文件：SKILL.md
code SKILL.md

# 测试安装
# 在 Claude Code 中:
/plugin install /path/to/my-plugin

# 发布到市场
# 需要满足 ClaudePluginHub 规范
```

### SKILL.md 插件格式示例

```yaml
---
name: vps-manager
description: VPS 管理插件：SSH 连接、服务状态、日志查看
trigger: user
---
# VPS Manager

## 命令
- `/vps list` — 列出所有 VPS
- `/vps status <name>` — 查看服务状态
- `/vps logs <name>` — 查看最近日志

## 流程
当用户执行 `/vps status nginx`:
1. 通过 SSH MCP 连接到目标 VPS
2. 执行 `systemctl status nginx`
3. 返回状态摘要

## 依赖
- SSH MCP Server 必须已安装
