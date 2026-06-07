# Roo Code 完整架构分析

## 目录
- [一、架构总览](#一架构总览)
- [二、自定义模式](#二自定义模式)
- [三、MCP 支持](#三mcp-支持)
- [四、与 Cline 的差异](#四与-cline-的差异)

---

## 一、架构总览

```
┌──────────────────────────────────────────┐
│           Roo Code (VS Code 扩展)         │
│                                          │
│  [Chat/Agent Mode] → [Tool Execution]    │
│        ↕                  ↕               │
│    .roo/rules           MCP Servers      │
│    Custom Modes        外部工具           │
│                                          │
│  安全: VS Code 沙箱 + 权限确认            │
└──────────────────────────────────────────┘
```

**Roo Code 特色**: 22.5K stars，高度可定制的 AI 编码助手。

---

## 二、自定义模式

### .roo/rules 目录
- 项目级规则（类似 CLAUDE.md）
- 支持多个自定义模式
- 每个模式可以有独立的：
  - 系统提示
  - 工具权限
  - 模型选择

### 自定义模式示例
```markdown
# .roo/rules/frontend-dev.md
---
name: frontend-dev
description: 前端开发模式
model: claude-sonnet-4
tools: Read, Write, Edit, Bash, Grep
---
你是前端开发专家。专注于 React + TypeScript 开发。
遵循项目的设计系统规范。
```

---

## 三、MCP 支持

- ✅ 基础 MCP 集成
- ✅ stdio 传输
- ⚠️ 远程 Server 支持有限
- ⚠️ 无 Deferred Loading

---

## 四、与 Cline 的差异

| 维度 | Cline | Roo Code |
|------|-------|----------|
| **Stars** | 58.6K | 22.5K |
| **Skills** | SKILL.md 标准 | 自定义规则 |
| **MCP** | 深度 | 中等 |
| **自定义模式** | 有限 | 强大 |
| **自动模式** | ✅ | 部分 |
| **模型支持** | 多模型 | 多模型 |

---

**下一节 →** [../frameworks/openhands.md](../frameworks/openhands.md) — OpenHands 完整架构
