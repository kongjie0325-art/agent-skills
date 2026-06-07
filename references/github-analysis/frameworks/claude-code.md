# Claude Code 完整架构分析

## 目录
- [一、架构总览](#一架构总览)
- [二、七层扩展模型](#二七层扩展模型)
- [三、配置层级](#三配置层级)
- [四、Skills 系统](#四skills-系统)
- [五、MCP 系统](#五mcp-系统)
- [六、Hooks 系统](#六hooks-系统)
- [七、子代理系统](#七子代理系统)
- [八、Plugin 系统](#八plugin-系统)

---

## 一、架构总览

```
┌──────────────────────────────────────────────────────────┐
│                     Claude Code                           │
│                                                          │
│  用户输入 → [Planner] → [Executor] → [Validator] → 输出  │
│                ↕            ↕            ↕               │
│              Skills       MCP/Tools     Hooks             │
│                ↕            ↕            ↕               │
│              Memory     外部系统      安全/审计            │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │ 扩展层: Skills + MCP + Hooks + Subagents + Plugins│   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ 记忆层: CLAUDE.md + Session Memory + Vector DB    │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ 配置层: 5 层级联（组织→用户→项目→本地→命令行）    │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

---

## 二、七层扩展模型

Claude Code 有 7 个核心扩展机制（按依赖顺序）：

| 层级 | 机制 | 说明 |
|------|------|------|
| 1 | **MCP** | 基础工具连接层 |
| 2 | **Memory (CLAUDE.md)** | 项目记忆和上下文 |
| 3 | **Skills** | 按需加载的知识 |
| 4 | **Subagents** | 隔离的工作代理 |
| 5 | **Agent Teams** | 协作的多代理 |
| 6 | **Hooks** | 生命周期拦截器 |
| 7 | **Plugins** | 打包分享层 |

> "Skills are knowledge. Subagents are workers. Agent Teams are workers that talk to each other."
> — Dean Blank

---

## 三、配置层级

```
Managed Settings (组织级)     ← 管理员控制，不可覆盖
  ↓
Command Line (命令行)         ← 每次启动指定
  ↓
Local Project (.claude/)      ← 项目级配置
  ↓
Shared Project (.claude/)     ← 团队共享
  ↓
User Defaults (~/.claude/)    ← 用户级配置
```

---

## 四、Skills 系统

### 位置
- **个人**: `~/.claude/skills/`
- **项目**: `.claude/skills/`

### 触发方式
1. **自动触发**: Agent 根据 description 判断相关性
2. **手动触发**: `/skill-name`
3. **路径限制**: `paths` 字段限制文件匹配

### 执行方式
1. **主上下文**: 直接在当前对话中执行
2. **Fork 上下文**: `context: fork` 在隔离子代理中执行
3. **指定子代理**: `agent: Explore` 使用特定子代理

### 脚本执行
```bash
# Skill 中的脚本通过 bash 执行
# 脚本代码不进上下文，只有输出进入
python ${CLAUDE_SKILL_DIR}/scripts/validate.py
```

---

## 五、MCP 系统

### 配置
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

### Deferred Tool Loading (2026)
- 启动时只加载工具名称列表
- 使用时才获取完整 schema
- 50+ 工具时减少 ~10% token 开销

### 远程 MCP
- Streamable HTTP 传输
- OAuth 2.1 + PKCE 认证
- 无需本地 stdio 进程

---

## 六、Hooks 系统

### 26 个生命周期事件
```
PreToolUse → Tool Execution → PostToolUse → Notification → Stop
                                      ↓
                              SubagentStop
                                      ↓
                              PreCompact → PostCompact
```

### Hook 类型
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "check-dangerous-commands.sh"
      }]
    }]
  }
}
```

### 安全模型
- **应用层 Hooks**（非内核级）
- 任意脚本（Bash/Python）
- Per-tool 正则匹配
- 3 级审批策略

---

## 七、子代理系统

### 内置子代理
| 子代理 | 模型 | 说明 |
|--------|------|------|
| **Explore** | Haiku | 快速只读搜索 |
| **Plan** | Sonnet | 研究-only |
| **General-purpose** | 默认 | 全功能 |
| **Claude Code Guide** | Sonnet | 文档专家 |

### 自定义子代理
```yaml
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: Reviews code for quality
tools: Read, Grep, Glob, Bash
model: sonnet
---
You are a senior code reviewer...
```

### Agent Teams（实验性）
- Lead agent + 多个 teammate
- 共享任务列表
- 直接互相通信
- 需要 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

---

## 八、Plugin 系统

### 安装
```bash
/plugin marketplace add <source>
/plugin install my-plugin
```

### 结构
```
my-plugin/
├── .claude-plugin/plugin.json
├── skills/
├── agents/
├── hooks/
├── commands/
└── mcp.json
```

### Plugin Marketplace
- 官方 + 社区 Plugin
- 一键安装
- 版本管理

---

**下一节 →** [../frameworks/openai-codex.md](../frameworks/openai-codex.md) — OpenAI Codex 完整架构
