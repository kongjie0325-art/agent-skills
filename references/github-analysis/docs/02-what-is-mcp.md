# MCP 深度解析 — 手和脚

## 目录
- [一、MCP 是什么](#一mcp-是什么)
- [二、MCP 的架构](#二mcp-的架构)
- [三、MCP 协议核心](#三mcp-协议核心)
- [四、传输层](#四传输层)
- [五、MCP 的能力](#五mcp-的能力)
- [六、MCP 的优缺点](#六mcp-的优缺点)
- [七、MCP 生态数据](#七mcp-生态数据)

---

## 一、MCP 是什么

**MCP（Model Context Protocol）= Agent 的万能插头**

MCP 是一个开放协议，标准化了 LLM 与外部工具/数据源的连接方式。
由 Anthropic 在 2024-11 发布，2025-12 捐赠给 Linux Foundation 的 Agentic AI Foundation (AAIF)。

> 类比：MCP 是 AI 世界的 USB-C 接口。

### 核心思想
```
以前：每个 Agent 为每个工具写一个集成 → N×M 个集成
现在：工具实现一次 MCP Server，所有支持 MCP 的 Agent 都能用 → N+M 个集成
```

---

## 二、MCP 的架构

```
┌─────────────────────────────────────────┐
│              Host Application           │
│    (Claude Desktop / Cursor / VS Code)  │
│                                         │
│  ┌──────────┐    JSON-RPC 2.0    ┌─────┴──────┐
│  │ MCP Client│ ◄────────────────► │ MCP Server │
│  └──────────┘                     └────────────┘
│                                     │  Tools     │
│                                     │  Resources │
│                                     │  Prompts   │
└─────────────────────────────────────┴────────────┘
         ▲                           ▲
         │                           │
    ┌────┴────┐               ┌──────┴──────┐
    │  stdio   │               │Streamable HTTP│
    │ (本地进程)│               │ (远程服务器)   │
    └─────────┘               └─────────────┘
```

### 三大角色
1. **Host** — 运行 AI 模型的应用（Claude Desktop、Cursor、VS Code）
2. **Client** — Host 内的 MCP 协议客户端
3. **Server** — 暴露工具/数据/能力的外部服务

---

## 三、MCP 协议核心

### 三大原语

| 原语 | 说明 | 示例 |
|------|------|------|
| **Tools** | Agent 可以调用的函数 | `web_search`, `read_file`, `create_issue` |
| **Resources** | Agent 可以读取的数据 | 文件内容、数据库记录、API 响应 |
| **Prompts** | 预定义的提示模板 | 代码审查模板、分析报告模板 |

### Tools 定义示例
```json
{
  "name": "create_issue",
  "description": "Create a GitHub issue",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": { "type": "string", "description": "Issue title" },
      "body": { "type": "string", "description": "Issue body" },
      "labels": { "type": "array", "items": { "type": "string" } }
    },
    "required": ["title", "body"]
  }
}
```

### Agent 使用 MCP Tools 的流程
```
1. 启动时：Client 连接所有 MCP Server，获取可用 Tools 列表
2. 用户提问：Agent 判断需要调用哪个 Tool
3. Agent 输出：JSON 格式的 tool_call（函数名 + 参数）
4. Client 执行：调用对应 MCP Server 的 Tool
5. 结果返回：Tool 执行结果注入到 Agent 上下文
6. 循环：Agent 继续推理，可能调用更多 Tools
```

---

## 四、传输层

### 两种传输方式

| 方式 | 适用场景 | 特点 |
|------|----------|------|
| **stdio** | 本地进程 | 低延迟，无需网络，适合本地工具 |
| **Streamable HTTP** | 远程服务器 | 支持 OAuth 2.1，多用户，可托管 |

### 协议演进
| 时间 | 更新 |
|------|------|
| 2024-11 | MCP 协议发布（stdio 传输） |
| 2025-03 | **Streamable HTTP** 传输（替代 HTTP+SSE）|
| 2025-03 | Tool call batching |
| 2026-01 | **MCP Apps** — Tools 可返回交互式 UI 组件 |
| 2026-06 | Stateless 协议支持（计划中）|

---

## 五、MCP 的能力

### ✅ 能做
- **标准化工具接入** — 一次开发，全 Agent 使用
- **通用性** — 跨模型、跨 Agent 平台
- **丰富的生态** — GitHub/Docker/PostgreSQL/Redis/Browser/Slack 等
- **自主闭环** — 计划→执行→验证→修复
- **OAuth 安全认证** — 标准化的权限管理
- **远程托管** — 多用户共享同一个 Server

### ❌ 不能做
- **不能提供领域知识**（这是 Skills 的事）
- **不能自动触发**（需要 Agent 主动调用）
- **高 Token 成本** — 大型 MCP Server 的定义可能消耗数万 tokens
- **不能组合复杂工作流**（需要 Skills 编排）

---

## 六、MCP 的优缺点

### 优点
1. **通用** — 一次开发，全 Agent 使用（真正的 USB-C）
2. **工具丰富** — 200+ 官方和社区 MCP Servers
3. **自主能力强** — 形成"计划→执行→验证→修复"闭环
4. **安全标准化** — OAuth 2.1 + PKCE
5. **远程托管** — Streamable HTTP 支持多用户

### 缺点
1. **需要部署** — 经常需要 Node/Python/Docker
2. **高 Token 成本** — 大型 Server 的工具定义消耗大量 tokens
3. **权限管理复杂** — Filesystem MCP 可能接触敏感文件
4. **工具质量参差不齐**
5. **安全风险** — 远程代码执行漏洞（2025 年多次被发现）

---

## 七、MCP 生态数据

### 采用情况（2026-06）
- **97M+** 月 SDK 下载量
- **10,000+** 活跃 MCP Servers
- **协议采纳**: Anthropic → OpenAI (2025-03) → Google (2025-04) → Microsoft → Linux Foundation AAIF

### 主流框架的 MCP 支持深度

| 框架 | MCP 支持 | 深度 |
|------|----------|------|
| Claude Code | ★★★★★ | 最深：200+ 服务器，Deferred Tool Loading |
| Cursor | ★★★★ | 原生支持，工具栏集成 |
| Windsurf | ★★★★ | 原生支持 |
| VS Code / Copilot | ★★★ | 通过扩展支持 |
| Cline | ★★★ | 支持，VS Code 扩展层面 |
| OpenAI Agents SDK | ★★★ | Hosted MCP + Tool Search |
| Codex CLI | ★★ | 基础支持 |

### 热门 MCP Servers
| Server | 用途 | Stars |
|--------|------|-------|
| GitHub MCP | GitHub 操作 | 15K+ |
| Filesystem MCP | 文件系统 | 10K+ |
| Browser MCP | 浏览器自动化 | 8K+ |
| PostgreSQL MCP | 数据库操作 | 5K+ |
| Slack MCP | Slack 消息 | 4K+ |
| Docker MCP | Docker 管理 | 3K+ |

---

**下一节 →** [03-what-are-plugins.md](./03-what-are-plugins.md) — Plugin 深度解析
