# 分层架构图 — Agent 能力蛋糕

## 文本版分层架构

```
╔══════════════════════════════════════════════════════════════════╗
║                        用户交互层                                  ║
║  CLI / IDE / Web / Telegram / Discord / Slack                     ║
╠══════════════════════════════════════════════════════════════════╣
║                        编排层                                     ║
║  Planner → Executor → Validator → Reporter                       ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                     ║
║  ┌─────────────────────┐  ┌─────────────────────┐                 ║
║  │    Skills 层         │  │    MCP 层            │                 ║
║  │  (知识/流程)         │  │  (工具/数据)         │                 ║
║  │                     │  │                     │                 ║
║  │  • SKILL.md         │  │  • Tools            │                 ║
║  │  • Instructions     │  │  • Resources        │                 ║
║  │  • Scripts          │  │  • Prompts          │                 ║
║  │  • Templates        │  │  • MCP Servers      │                 ║
║  │                     │  │                     │                 ║
║  │  告诉 Agent 怎么做    │  │  让 Agent 能做       │                 ║
║  └─────────────────────┘  └─────────────────────┘                 ║
║                                                                     ║
╠══════════════════════════════════════════════════════════════════╣
║                        记忆层                                     ║
║  CLAUDE.md / AGENTS.md / Vector DB / Session Memory               ║
╠══════════════════════════════════════════════════════════════════╣
║                        安全层                                     ║
║  Hooks / Seatbelt / Landlock / Docker 沙箱 / Permissions           ║
╠══════════════════════════════════════════════════════════════════╣
║                        模型层                                     ║
║  Claude / GPT / Gemini / Local Models                              ║
╚══════════════════════════════════════════════════════════════════╝
```

## 数据流

```
用户请求
  ↓
[Skills 匹配] → 加载相关 Skill 指令
  ↓
[Memory 加载] → CLAUDE.md / AGENTS.md / Vector DB
  ↓
[LLM 推理] → 决定调用哪些 Tools
  ↓
[MCP 调用] → 执行外部工具/API
  ↓
[Hook 拦截] → 安全检查/审计日志
  ↓
[结果返回] → 用户
```

## 各层的关键设计

### Skills 层（知识）
- **Progressive Disclosure**: 启动时只加载 metadata（~100 tokens），触发时才加载完整指令
- **脚本执行**: 代码不进上下文，只执行，只有输出进入
- **自动触发**: 基于 description 的语义匹配

### MCP 层（工具）
- **标准协议**: JSON-RPC 2.0，跨模型、跨 Agent 平台
- **两种传输**: stdio（本地）+ Streamable HTTP（远程）
- **三大原语**: Tools + Resources + Prompts
- **Deferred Loading**: 启动时只加载名称，使用时才获取完整 schema

### 记忆层（连续性）
- **4 层记忆**: Context Window → Project Memory → Session Memory → External Memory
- **CLAUDE.md**: Anthropic 专有，5 层级联
- **AGENTS.md**: Linux Foundation 开放标准，多框架支持

### 安全层（治理）
- **应用层 Hooks** (Claude Code): 26 个生命周期事件，任意脚本
- **内核层隔离** (Codex): Seatbelt/Landlock/seccomp，OS 级阻止
- **容器隔离** (OpenHands): Docker 沙箱，完全隔离
