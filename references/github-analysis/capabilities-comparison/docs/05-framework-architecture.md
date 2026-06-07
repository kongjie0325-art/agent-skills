# 主流 AI Agent 框架架构分析（2026）

本文深度分析 8 个主流 AI 编码 Agent 框架的内部架构，重点关注它们在 **Skills、MCP、Plugin、Memory、Self-Reflection** 等方面的实现情况。

---

## 评价维度

| 维度 | 说明 | 权重 |
|------|------|------|
| **Skills** | 是否支持 Skill 文件/工作流模板 | 🔴 核心 |
| **MCP** | 是否支持 Model Context Protocol | 🔴 核心 |
| **Plugin** | 是否有插件扩展系统 | 🟡 重要 |
| **Memory** | 是否有跨会话记忆能力 | 🟡 重要 |
| **Subagents** | 是否支持子 Agent/多 Agent 协调 | 🟢 加分 |
| **Self-Reflection** | 是否有自我反思/结果验证机制 | 🟢 加分 |
| **Model 灵活度** | 是否支持切换模型 | 🟢 加分 |

---

## 1️⃣ Claude Code（Anthropic）

```
状态：★★★★★  最完善的 Agent 生态
架构：CLI + IDE 扩展 + 钩子系统 + 子 Agent + 插件市场
```

### 架构图

```
用户
  │
  ▼
┌──────────────────────────────────────┐
│           Agent Loop                 │
│  (推理 → 行动 → 观察 → 重复)         │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│       Skills System  (SKILL.md)       │ ← 29 种钩子触发
│  • 自动加载 / 斜杠命令 / 条件触发     │
│  • 支持技能链和组合                   │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│          Memory Layer                 │
│  • 会话上下文记忆                     │
│  • CLAUDE.md 项目规则                 │
│  • 长期记忆(Graceful Memory)          │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│          Subagents                    │
│  • Agent Teams (多 Agent 协调)        │
│  • 专用子 Agent (测试 Agent / 架构)   │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│    MCP Client (原生)                  │
│  • 自动发现 MCP Server                │
│  • 内置 Filesystem / GitHub / Browser │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│    Plugin Marketplace                 │
│  • 432 个插件 / 2769 Skills          │
│  • Hooks 系统 (29 种事件)             │
└──────────────────────────────────────┘
```

| 能力 | 支持度 | 备注 |
|------|--------|------|
| Skills | ✅ 原生 | SKILL.md + 斜杠命令 + 自动触发 |
| MCP | ✅ 原生 | 内置 MCP 客户端，自动发现 |
| Plugin | ✅ 原生 | 插件市场 + hooks 系统 |
| Memory | ✅ 原生 | CLAUDE.md + Graceful Memory |
| Subagents | ✅ Agent Teams | 多 Agent 协调 |
| Self-Reflection | ✅ 部分 | 通过 Hooks 实现 |
| Model 灵活度 | 🟡 有限 | 主要支持 Claude 系列 |

---

## 2️⃣ OpenAI Codex CLI

```
状态：★★★★☆  极简但强大
架构：CLI + AGENTS.md + MCP + Sandbox
```

```
用户
  │
  ▼
┌──────────────────────────────────────┐
│     Codex Harness (Agent Loop)       │
│  • 推理 → 工具调用 → 观察 → 继续     │
│  • 状态无关设计 (零数据留存)          │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│     AGENTS.md (Skills 抽象层)         │
│  • 全局 + 项目级规则                  │
│  • Linux Foundation 开放标准          │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│     MCP Client                        │
│  • 支持社区 MCP Servers               │
│  • 自动管理                            │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│     Execution Sandbox                  │
│  • 安全执行环境                        │
│  • 文件系统隔离                        │
└──────────────────────────────────────┘
```

| 能力 | 支持度 | 备注 |
|------|--------|------|
| Skills | ✅ AGENTS.md | 开放标准，跨平台兼容 |
| MCP | ✅ 原生 | 社区兼容 |
| Plugin | ❌ 无 | 扩展靠 AGENTS.md + MCP |
| Memory | 🟡 基本 | 会话上下文 + AGENTS.md |
| Subagents | ❌ 无 | 但可以外部协调 |
| Self-Reflection | ✅ 内置 | Agent Loop 内置反馈 |
| Model 灵活度 | 🟡 有限 | 主要 GPT 系列 |

---

## 3️⃣ Cline（VS Code Extension）

```
状态：★★★★☆  社区最大，58K+ Stars
架构：VS Code Extension + MCP + Human-in-the-Loop
```

| 能力 | 支持度 | 备注 |
|------|--------|------|
| Skills | 🟡 .clinerules | 项目规则文件 |
| MCP | ✅ 原生 | MCP Marketplace 集成 |
| Plugin | 🟡 有限 | 主要通过 MCP + 模式扩展 |
| Memory | 🟡 会话级 | 无长期记忆 |
| Subagents | ❌ 无 | 单 Agent |
| Self-Reflection | 🟡 人工审核 | Human-in-the-Loop 模型 |
| Model 灵活度 | ✅ 极好 | 支持所有主流模型 |

**核心哲学：** Cline 坚持 Human-in-the-Loop，每个工具调用都经过用户批准。社区最大（58K Stars），MCP marketplace 最丰富。

---

## 4️⃣ Roo Code（VS Code Extension）

```
状态：★★★★☆  多模式 + Cloud Agents
架构：VS Code Extension + 多 Mode + Cloud Agents
```

| 能力 | 支持度 | 备注 |
|------|--------|------|
| Skills | ✅ 自定义 Mode | Mode 配置文件实现 |
| MCP | ✅ 完善 | 比 Cline 更好的 MCP 支持 |
| Plugin | ✅ Modes Marketplace | 社区模式市场 |
| Memory | 🟡 会话级 | 无长期记忆 |
| Subagents | ✅ Cloud Agents | GitHub Actions 触发 |
| Self-Reflection | 🟡 部分 | 通过 Mode 配置 |
| Model 灵活度 | ✅ 极好 | 支持所有模型 |

**核心亮点：** 从 Cline fork 而来，添加了多 Agent 人格 Mode、Cloud Agents、更好的 MCP 支持。

---

## 5️⃣ OpenHands

```
状态：★★★☆☆  企业级多 Agent
架构：SDK + Multi-Agent + 浏览器 UI
```

| 能力 | 支持度 | 备注 |
|------|--------|------|
| Skills | 🟡 有限 | 主要通过 Agent 指令 |
| MCP | ✅ 兼容 | 2025 年添加 |
| Plugin | ✅ SDK | Python SDK 扩展 |
| Memory | ✅ 持久化 | 项目级持久存储 |
| Subagents | ✅ 原生 | 多 Agent 编排内置 |
| Self-Reflection | ✅ 部分 | 验证 Agent 机制 |
| Model 灵活度 | ✅ 好 | 支持多种 |

**核心亮点：** 企业级部署，有浏览器 UI，SDK 扩展，多 Agent 编排。

---

## 6️⃣ Kilo Code

```
状态：★★★☆☆  新秀，融资 $8M
架构：VS Code + JetBrains + 500+ 模型
```

| 能力 | 支持度 | 备注 |
|------|--------|------|
| Skills | 🟡 有限 | 通过自定义指令 |
| MCP | ✅ 原生 | 完整支持 |
| Plugin | 🟡 有限 | 主要在平台上 |
| Memory | 🟡 会话级 | 无长期记忆 |
| Subagents | ✅ Parallel Agents | 并行子 Agent |
| Self-Reflection | 🟡 部分 | 内置验证 |
| Model 灵活度 | ✅ 500+ 模型 | 最广泛的模型支持 |

---

## 7️⃣ OpenCode

```
状态：★★★☆☆  轻量级 CLI
架构：CLI + MCP + 多模型
```

| 能力 | 支持度 | 备注 |
|------|--------|------|
| Skills | 🟡 有限 | .rules 文件 |
| MCP | ✅ 原生 | 完整支持 |
| Plugin | ❌ 无 | 扩展靠 MCP |
| Memory | ❌ 无 | 仅会话上下文 |
| Subagents | ❌ 无 | 单 Agent |
| Self-Reflection | 🟡 基本 | Agent Loop |
| Model 灵活度 | ✅ 好 | 多模型支持 |

---

## 8️⃣ Aider

```
状态：★★★☆☆  最老牌 CLI Agent
架构：CLI + Git-native + Map
```

| 能力 | 支持度 | 备注 |
|------|--------|------|
| Skills | 🟡 有限 | .aider.conf.yml + Instructions |
| MCP | ✅ 兼容 | 近期新增支持 |
| Plugin | 🟡 有限 | 主要通过配置文件 |
| Memory | 🟡 会话级 | 无长期记忆 |
| Subagents | ❌ 无 | 单 Agent |
| Self-Reflection | ✅ Git 提交 | 通过 Git diff 验证 |
| Model 灵活度 | ✅ 好 | 多模型支持 |

**核心亮点：** 41K Stars，Git 原生集成（auto-commit, lint 修复），代码库 Map 技术能让 Agent 理解大型代码库。

---

## 📊 总结对比

| 框架 | Skills | MCP | Plugin | Memory | Subagent | 自主性 | 最佳场景 |
|------|--------|-----|--------|--------|----------|--------|---------|
| **Claude Code** | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅ | 高 | 全栈开发 / 高级 Agent 编排 |
| **Codex CLI** | ✅ | ✅ | ❌ | 🟡 | ❌ | 中高 | CLI / CI / 自动化 |
| **Cline** | 🟡 | ✅✅ | 🟡 | 🟡 | ❌ | 中(人工审核) | 安全优先 / 初学者 |
| **Roo Code** | ✅ | ✅✅ | ✅ | 🟡 | ✅ | 高 | 多模式工作流 |
| **OpenHands** | 🟡 | ✅ | ✅ | ✅ | ✅✅ | 高 | 企业 / 多 Agent 编排 |
| **Kilo Code** | 🟡 | ✅ | 🟡 | 🟡 | ✅ | 高 | 模型实验 / 并行任务 |
| **OpenCode** | 🟡 | ✅ | ❌ | ❌ | ❌ | 中 | 轻量级 / 快速编码 |
| **Aider** | 🟡 | ✅ | 🟡 | 🟡 | ❌ | 中高 | Git 工作流 / 大型代码库 |

---

## 哪个最接近「真正的自主 Agent」？

真正的自主 Agent 需要：

1. ✅ **Skills** — 知道怎么做
2. ✅ **MCP** — 能执行
3. ✅ **Memory** — 记得上下文
4. ✅ **Subagents** — 能分解任务并并行执行
5. ✅ **Self-Reflection** — 能自我验证和纠错
6. ✅ **Plugin** — 能扩展功能

### 排名

| 排名 | 框架 | 接近度 | 短板 |
|------|------|--------|------|
| 🥇 | **Claude Code** | 85% | Model 锁定（只有 Claude） |
| 🥈 | **OpenHands** | 75% | Skills 较弱 |
| 🥉 | **Roo Code** | 70% | 记忆薄弱 |
| 4 | **Codex CLI** | 60% | 无 Plugin / 弱记忆 |
| 5 | **Kilo Code** | 55% | Skills / Plugin 薄弱 |
| 6 | **Cline** | 50% | 人工审核限制自主性 |
| 7 | **Aider** | 45% | 无 Subagent / 弱 Skills |
| 8 | **OpenCode** | 40% | 多处短板 |

> 📌 Claude Code 之所以领先，不是因为模型最强，而是因为它的 Skills + MCP + Plugin + Memory + Subagents + Hooks 是最完整的组合。
