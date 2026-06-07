# Memory + Hooks — 记忆与安全门卫

## 目录
- [一、Memory（记忆）](#一memory记忆)
- [二、Hooks（钩子）](#二hooks钩子)
- [三、Memory vs Hooks 的关系](#三memory-vs-hooks-的关系)

---

## 一、Memory（记忆）

### 什么是 Agent Memory？

Memory 是 Agent 的持久化上下文——让 Agent 记住之前发生过的事。

### 层次结构

```
┌─────────────────────────────────────────────┐
│              Memory 层次                      │
├─────────────────────────────────────────────┤
│                                             │
│  L1: Context Window（上下文窗口）              │
│     当前对话的 token 窗口                      │
│     容量：1M tokens（Claude Code）             │
│     生命周期：单次会话                          │
│                                             │
│  L2: Project Memory（项目记忆）                │
│     CLAUDE.md / AGENTS.md                    │
│     每次会话自动加载                           │
│     生命周期：持久（文件）                       │
│                                             │
│  L3: Session Memory（会话记忆）                │
│     跨会话的持久化存储                          │
│     Hermes: SQLite + FTS5                    │
│     生命周期：跨会话                            │
│                                             │
│  L4: External Memory（外部记忆）               │
│     Vector DB / RAG / Knowledge Base          │
│     Qdrant / pgvector / Redis                 │
│     生命周期：永久                              │
│                                             │
└─────────────────────────────────────────────┘
```

### CLAUDE.md — 项目记忆

```markdown
# CLAUDE.md

## 项目概览
Alexander Opalic 的个人博客，基于 AstroPaper
**技术栈**: Astro 5, TypeScript, React, TailwindCSS

## 开发命令
npm run dev    # 本地开发
npm run build  # 生产构建
npm run lint   # ESLint

## 编码规范
- 使用函数式组件，不用 class 组件
- 所有组件必须有 TypeScript 类型
- CSS 使用 TailwindCSS，不用内联样式
```

### CLAUDE.md 加载层级
```
Enterprise CLAUDE.md (组织级)
  → User ~/.claude/CLAUDE.md (用户级)
    → Project ./CLAUDE.md (项目级)
      → Subdirectory ./src/components/CLAUDE.md (目录级)
```

### AGENTS.md — 开放标准
- 由 Linux Foundation AAIF 维护
- 被 Codex、Cursor、Copilot、Windsurf、Gemini CLI 共同支持
- 与 CLAUDE.md 独立，两者可共存

---

## 二、Hooks（钩子）

### 什么是 Hooks？

Hooks 是**确定性的事件拦截器**——在 Agent 生命周期的特定点自动执行。

> Hooks 是安全/治理层的核心——在 Agent 行动前检查，在行动后审计。

### Claude Code 的 26 个生命周期事件

| 阶段 | Hook | 说明 |
|------|------|------|
| **PreToolUse** | `Bash`, `Read`, `Write`, `Edit`, `Grep`, `Glob`, `WebFetch`, `WebSearch` | 工具执行前 |
| **PostToolUse** | 同上所有工具 | 工具执行后 |
| **Notification** | - | Agent 发出通知时 |
| **Stop** | - | Agent 完成任务时 |
| **SubagentStop** | - | 子代理完成时 |
| **PreCompact** | - | 上下文压缩前 |
| **PostCompact** | - | 上下文压缩后 |

### Hook 配置示例
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "check-dangerous-commands.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "run-linter.sh"
          }
        ]
      }
    ]
  }
}
```

### Codex 的安全模型（内核级 vs 应用级）

| 维度 | Codex CLI | Claude Code |
|------|-----------|-------------|
| **隔离层** | OS 内核（Seatbelt/Landlock/seccomp） | 应用层 Hooks |
| **权限模式** | read-only / workspace-write / danger-full-access | 正则匹配 per-tool |
| **逃逸阻力** | 高（OS 层阻止） | 中（同进程边界） |
| **可编程性** | 低（二进制开关） | 高（任意脚本） |

---

## 三、Memory vs Hooks 的关系

| 维度 | Memory | Hooks |
|------|--------|-------|
| **本质** | 记住什么 | 拦截什么 |
| **作用时机** | 会话开始时加载 | 工具执行前后 |
| **目的** | 提供上下文和知识 | 强制安全和治理 |
| **实现** | Markdown 文件 / Vector DB | Shell 脚本 / 命令 |
| **Token 消耗** | 是（进入上下文） | 否（独立执行） |
| **可配置性** | 低（写文件） | 高（任意逻辑） |

---

**下一节 →** [05-anatomy-comparison.md](./05-anatomy-comparison.md) — 横向对比全维度
