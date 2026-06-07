# MCP 深度解析

## 什么是 MCP

**MCP** = **Model Context Protocol**（模型上下文协议）

Anthropic 在 2024 年底推出，现在是 **Linux Foundation Agentic AI Foundation** 下的开放标准。

> MCP 解决的问题：**怎么执行**

它定义了 Agent 如何：
- 发现工具
- 调用工具
- 接收工具返回值
- 处理工具错误

---

## MCP 架构

```
┌──────────────────────────────┐
│       AI Agent (Client)      │  ← Claude Code / Codex / Cursor
│       (MCP Client SDK)       │
└──────────┬───────────────────┘
           │ JSON-RPC (stdio / SSE / Streamable HTTP)
           │
┌──────────▼───────────────────┐
│     MCP Server (你写的)       │  ← 运行在本机或远端
│  tools/list → 暴露工具列表    │
│  tools/call → 执行工具        │
│  resources/ → 暴露资源        │
│  prompts/  → 暴露提示模板     │
└──────────────────────────────┘
```

### 核心概念

| 概念 | 说明 |
|------|------|
| **Tools** | Agent 可调用的函数（读文件、提交代码、搜索网页） |
| **Resources** | 外部数据源暴露给 Agent（文件、数据库记录、API 响应） |
| **Prompts** | 预设模板，引导 Agent 如何与工具交互 |
| **Transport** | stdio（本地）、SSE（远程）、Streamable HTTP（新标准） |

---

## MCP Server 生态（2026 年）

### 官方参考实现

| Server | 说明 |
|--------|------|
| [Filesystem](https://github.com/modelcontextprotocol/servers) | 安全文件系统访问 |
| [GitHub](https://github.com/modelcontextprotocol/servers) | 仓库、Issues、PRs、Code 操作 |
| [PostgreSQL](https://github.com/modelcontextprotocol/servers) | 数据库查询、Schema 探索 |
| [SQLite](https://github.com/modelcontextprotocol/servers) | 轻量级数据库 |
| [Puppeteer/Playwright](https://github.com/modelcontextprotocol/servers) | 浏览器自动化 |
| [Slack](https://github.com/modelcontextprotocol/servers) | 消息、频道、搜索 |
| [Brave Search](https://github.com/modelcontextprotocol/servers) | Web + 本地搜索 |

### 社区流行 MCP Server Top 10

| Server | 用途 | Stars |
|--------|------|-------|
| **GitHub** | 代码、PR、Issue 管理 | ⭐ 官⽅ |
| **Filesystem** | 本地文件读写 | ⭐ 官⽅ |
| **Playwright** | 浏览器自动化 | ⭐ 官⽅ |
| **Docker** | 容器管理 | 高 |
| **PostgreSQL** | 数据库查询 | ⭐ 官⽅ |
| **Linear** | 项目管理 | 高 |
| **Notion** | 知识库集成 | 高 |
| **Google Workspace** | Gmail、Calendar、Drive | 高 |
| **Jira** | 任务管理 | 高 |
| **Slack** | 团队沟通 | ⭐ 官⽅ |

### 按类别

| 类别 | MCP Servers |
|------|------------|
| 🔧 **开发** | GitHub, GitLab, Filesystem, Docker, SSH, PostgreSQL |
| 🌐 **网络** | Browser (Playwright/Puppeteer), Fetch, Search |
| ☁️ **云平台** | AWS, GCP, Cloudflare, Vercel |
| 💬 **通讯** | Slack, Discord, Telegram, Email |
| 🗄️ **数据** | MySQL, PostgreSQL, SQLite, Redis, Elasticsearch |
| 📊 **监控** | Prometheus, Grafana, Sentry, Datadog |
| 🧠 **AI 服务** | HuggingFace, OpenAI, Anthropic |
| 🎵 **多媒体** | Spotify, YouTube, ImageGen |

---

## MCP 的优点

| 优点 | 说明 |
|------|------|
| **🌍 通用** | 一次开发，所有 Agent（Claude Code / Codex / Cursor / Cline / etc.）都能用 |
| **🧰 工具丰富** | 3000+ 社区 MCP Server，覆盖几乎所有常见服务 |
| **🤖 自主闭环** | Agent 可以独立完成 计划 → 执行 → 验证 → 修复 闭环 |
| **📐 标准化** | Linux Foundation 背书，生态持续扩大 |
| **🔌 可组合** | 多个 MCP Server 可以同时工作 |

---

## MCP 的缺点

| 缺点 | 说明 |
|------|------|
| **🚧 需要部署** | Node.js / Python / Docker 环境通常需要 |
| **🔐 权限管理复杂** | Filesystem MCP 可能接触敏感文件 |
| **⚖️ 质量参差不齐** | 有些 MCP Server 写得很好，有些问题很多 |
| **📏 有学习曲线** | 理解 JSON-RPC 协议和 MCP 规格需要时间 |
| **🐌 远程延迟** | 网络式传输比本地 stdio 慢 |

---

## 如何选择 MCP Server

### 新手 Starter Pack

1. **GitHub MCP** — 代码仓库操作（必装）
2. **Filesystem MCP** — 安全文件访问（必装）
3. **Playwright MCP** — 浏览器自动化（高频）
4. **Brave Search MCP** — 网页搜索（随身）

### 进阶配置（开发/VPS/自动化场景）

```
GitHub MCP       → 代码、PR、Issue
Filesystem MCP   → 本地文件操作
Browser MCP      → 网页交互测试
Docker MCP       → 容器管理
SSH MCP          → 远程 VPS 管理
Search MCP       → 在线搜索
PostgreSQL MCP   → 数据库操作
```

---

## MCP vs Function Calling

| 维度 | OpenAI Function Calling | MCP |
|------|------------------------|-----|
| 标准 | 专有（OpenAI 独有） | 开放（Linux Foundation） |
| 工具发现 | 开发者手动注册 | 服务端自动暴露 tools/list |
| 传输 | HTTP + JSON Schema | stdio / SSE / Streamable HTTP |
| 生态 | 仅限于 OpenAI | 跨 Agent 平台 |
| 动态性 | 静态 Schema | 工具列表可动态变化 |
