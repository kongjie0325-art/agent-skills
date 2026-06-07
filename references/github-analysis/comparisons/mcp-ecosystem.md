# MCP 生态 — 协议版本、传输层、热门 Servers

## 目录
- [一、协议版本演进](#一协议版本演进)
- [二、传输层详解](#二传输层详解)
- [三、热门 MCP Servers](#三热门-mcp-servers)
- [四、各框架 MCP 支持深度](#四各框架-mcp-支持深度)
- [五、MCP 开发框架](#五mcp-开发框架)

---

## 一、协议版本演进

| 时间 | 版本 | 关键更新 |
|------|------|----------|
| 2024-11 | v1.0 | 初始发布（stdio 传输）|
| 2025-03 | v2025-03-26 | Streamable HTTP 替代 SSE |
| 2025-03 | - | Tool call batching |
| 2025-12 | - | 捐赠给 Linux Foundation AAIF |
| 2026-01 | - | MCP Apps（Tools 返回 UI 组件）|
| 2026-06 | - | Stateless 协议支持（计划中）|
| 2026-06 | - | 97M+ 月 SDK 下载，10K+ 活跃 Server |

---

## 二、传输层详解

### stdio（本地进程）
```
Agent ←→ MCP Client ←→ stdio ←→ MCP Server（本地进程）
```
- 低延迟，无需网络
- 适合：Filesystem、本地数据库、本地工具

### Streamable HTTP（远程服务器）
```
Agent ←→ MCP Client ←→ HTTP/2 ←→ MCP Server（远程）
```
- 支持 OAuth 2.1 + PKCE
- 多用户共享
- 适合：SaaS 集成、团队协作

### 传输层选择决策
```
需要远程访问？
├─ 是 → Streamable HTTP
│   ├─ 需要多用户？ → 托管 Server + OAuth
│   └─ 单用户？ → 远程 Server + API Key
│
└─ 否 → stdio
    ├─ 需要低延迟？ → stdio
    └─ 需要隔离？ → stdio + 独立进程
```

---

## 三、热门 MCP Servers

**开发工具类**
| Server | Stars | 说明 |
|--------|-------|------|
| GitHub MCP | 15K+ | GitHub 操作（PR/Issue/CI）|
| GitLab MCP | 3K+ | GitLab 操作 |
| Docker MCP | 3K+ | Docker 容器管理 |
| Database MCP | 5K+ | PostgreSQL/MySQL 操作 |

**文件系统类**
| Server | Stars | 说明 |
|--------|-------|------|
| Filesystem MCP | 10K+ | 本地文件系统读写 |
| Google Drive MCP | 2K+ | Google Drive 文件 |
| S3 MCP | 1K+ | AWS S3 操作 |

**浏览器类**
| Server | Stars | 说明 |
|--------|-------|------|
| Browser MCP | 8K+ | 浏览器自动化 |
| Playwright MCP | 5K+ | Playwright 自动化测试 |

**通信类**
| Server | Stars | 说明 |
|--------|-------|------|
| Slack MCP | 4K+ | Slack 消息 |
| Discord MCP | 2K+ | Discord 消息 |
| Email MCP | 1K+ | 邮件收发 |

**AI/ML 类**
| Server | Stars | 说明 |
|--------|-------|------|
| Memory MCP | 2K+ | 向量记忆存储 |
| Qdrant MCP | 1K+ | Qdrant 向量数据库 |
| Tavily MCP | 1K+ | Tavily 搜索 |

---

## 四、各框架 MCP 支持深度

### Claude Code（最深）
```
✅ 200+ 内置 MCP Servers
✅ Deferred Tool Loading（按需加载 schema）
✅ 远程 Server + OAuth 2.1
✅ MCP Apps（UI 组件）
✅ 单行配置
✅ Tool Search（减少 token 开销）
```

### OpenAI Agents SDK
```
✅ Hosted MCP（OpenAI 托管）
✅ Tool Search（延迟加载）
✅ 内置 Web Search / File Search / Code Interpreter
✅ 自定义 MCP Server
❌ MCP Apps 支持有限
```

### Cursor
```
✅ 原生 MCP 集成
✅ 工具栏 UI 集成
✅ 远程 Server
❌ Deferred Loading 有限
```

### Cline
```
✅ 基础 MCP 支持
✅ 自动发现
✅ stdio 传输
❌ 远程 Server 支持有限
❌ 无 Deferred Loading
```

### Codex CLI
```
✅ 基础 MCP 支持
✅ Streamable HTTP
✅ OAuth 2.1
❌ 内置 Server 较少
```

---

## 五、MCP 开发框架

| 框架 | 语言 | Stars | 说明 |
|------|------|-------|------|
| MCP SDK (Anthropic) | Python/TS | 10K+ | 官方 SDK |
| MCP SDK (OpenAI) | Python | 5K+ | OpenAI 维护 |
| Spring AI MCP | Java | 3K+ | Spring 生态 |
| Go-MCP | Go | 2K+ | Go 实现 |
| Rust-MCP | Rust | 1K+ | Rust 实现 |

---

**下一节 →** [../comparisons/plugin-ecosystem.md](../comparisons/plugin-ecosystem.md) — Plugin 生态
