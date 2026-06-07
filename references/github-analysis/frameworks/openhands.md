# OpenHands 完整架构分析

## 目录
- [一、架构总览](#一架构总览)
- [二、Skills 系统](#二skills-系统)
- [三、MCP 支持](#三mcp-支持)
- [四、沙箱安全](#四沙箱安全)

---

## 一、架构总览

```
┌──────────────────────────────────────────┐
│              OpenHands                    │
│                                          │
│  [Agent Loop] → [Planner] → [Executor]   │
│        ↕            ↕           ↕        │
│    Skills      Conventions   MCP Servers  │
│        ↕            ↕           ↕        │
│    Memory      沙箱安全      外部工具     │
│                                          │
│  CLI + IDE + Web 多入口                   │
└──────────────────────────────────────────┘
```

**OpenHands 特色**: 8K+ stars，完全开源，多入口（CLI/IDE/Web），强沙箱安全。

---

## 二、Skills 系统

### 位置
- `~/.openhands/skills/` — 个人
- `.openhands/skills/` — 项目

### 格式
- 自定义格式（非 SKILL.md）
- 基于 Markdown 指令
- 支持脚本执行

### 内置 Skills
- 代码分析
- 测试运行
- 代码搜索
- 文件操作

---

## 三、MCP 支持

- ✅ 基础 MCP 集成
- ✅ stdio + Streamable HTTP
- ✅ OAuth 2.1
- ⚠️ 无 Deferred Loading
- ⚠️ 内置 Server 较少

---

## 四、沙箱安全

### Docker 沙箱
- 所有代码执行在 Docker 容器中
- 网络隔离
- 文件系统隔离
- 资源限制

### 安全层次
```
Docker 沙箱（最外层）
  → 文件系统隔离
    → 网络隔离
      → 资源限制（CPU/内存）
```

### 与 Claude Code 的差异
| 维度 | Claude Code | OpenHands |
|------|-------------|----------|
| **沙箱** | 应用层 Hooks | Docker 容器 |
| **隔离** | 同进程 | 独立容器 |
| **安全性** | 中 | 高 |
| **灵活性** | 高 | 中 |

---

**下一节 →** [../diagrams/architecture-layer-cake.md](../diagrams/architecture-layer-cake.md) — 分层架构图
