# OpenAI Codex 完整架构分析

## 目录
- [一、架构总览](#一架构总览)
- [二、Skills 系统](#二skills-系统)
- [三、Plugin 系统](#三plugin-系统)
- [四、安全模型](#四安全模型)
- [五、配置系统](#五配置系统)
- [六、与 Claude Code 的关键差异](#六与-claude-code-的关键差异)

---

## 一、架构总览

```
┌──────────────────────────────────────────────────┐
│                  OpenAI Codex                     │
│                                                  │
│  [Goal Loop] → [Planner] → [Executor] → [Output] │
│                    ↕            ↕                 │
│                 Skills      Plugins/MCP           │
│                    ↕            ↕                 │
│                AGENTS.md    外部工具              │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │ 安全层: Seatbelt (macOS) / Landlock (Linux)│   │
│  │ + seccomp + 沙箱                          │   │
│  └──────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```

---

## 二、Skills 系统

### Skills 仓库
- **GitHub**: [openai/skills](https://github.com/openai/skills)
- **安装器**: `$skill-installer`
- **自动安装**: `.system/` 目录的 Skills 自动安装

### 安装方式
```bash
# 安装官方 Skill
$skill-installer install create-plan

# 安装实验性 Skill
$skill-installer install skills/.experimental/create-plan

# 从 GitHub 安装
$skill-installer install https://github.com/openai/skills/...
```

### Skills 分类
- **system/**: 自动安装（Codex 内置）
- **curated/**: 精选 Skills（按名称安装）
- **experimental/**: 实验性 Skills

### 调用方式
```
$user-input          # 选择 Skill
$skill-name args     # 执行 Skill
```

### 与 Claude Code Skills 的差异

| 维度 | Claude Code | OpenAI Codex |
|------|-------------|--------------|
| **格式** | SKILL.md + YAML frontmatter | SKILL.md + YAML frontmatter |
| **Progressive Disclosure** | ✅ 三层 | ✅ |
| **脚本执行** | ✅ bash 沙箱 | ✅ |
| **API 上传** | ✅ /v1/skills | ✅ openai/skills 仓库 |
| **安装方式** | `/plugin` + marketplace | `$skill-installer` |
| **社区生态** | 400K+ 安装 | 快速增长 |

---

## 三、Plugin 系统

### 定义
> "Plugins help Codex connect to other tools and sources of information."

### 与 Skills 的关系
```
Plugin = 连接外部工具（Google Drive、邮箱、日历等）
Skill  = 遵循你的流程（团队规范、工作流）
Both   = 用外部工具 + 你的流程完成任务
```

### 使用场景
- 需要从 Google Drive 获取文件 → **Plugin**
- 需要按团队格式写周报 → **Skill**
- 需要从 Drive 获取数据 + 按格式写周报 → **Both**

### 创建 Plugin
- 需要技术知识
- 无标准格式
- 通过 UI 或手动配置

---

## 四、安全模型

### 内核级安全（vs Claude Code 的应用层）

| 维度 | Codex CLI | Claude Code |
|------|-----------|-------------|
| **隔离层** | OS 内核 | 应用层 Hooks |
| **macOS** | Seatbelt | - |
| **Linux** | Landlock + seccomp | - |
| **权限模式** | 3 种（read-only/workspace-write/danger-full-access）| 正则 per-tool |
| **可编程性** | 低（开关式）| 高（任意脚本）|
| **逃逸阻力** | 高 | 中 |

### 沙箱模式
```
read-only       → 只读，不能修改文件
workspace-write → 只能写工作区
danger-full-access → 完全访问（需明确批准）
```

---

## 五、配置系统

### AGENTS.md — 开放标准
- **维护方**: Linux Foundation AAIF
- **采纳**: Codex/Cursor/Copilot/Gemini CLI/Windsurf
- **与 CLAUDE.md 共存**: 两者独立，可同时存在

### Profiles（TOML）
```toml
[profile.careful]
approval_policy = "untrusted"

[profile.fast]
approval_policy = "on-request"
```

### 配置层级
```
Profile (--profile flag)
  → AGENTS.md (项目级)
    → AGENTS.md (用户级)
```

---

## 六、与 Claude Code 的关键差异

### 设计哲学差异

| 维度 | Claude Code | OpenAI Codex |
|------|-------------|--------------|
| **治理层** | 应用层（可编程） | 内核层（不可绕过）|
| **灵活性** | 极高 | 较低 |
| **安全性** | 中（同进程） | 高（OS 层）|
| **适用场景** | 深度开发、重构 | 安全审查、不可信代码 |
| **记忆** | CLAUDE.md | AGENTS.md |
| **Skills** | 自定义为主 | 官方仓库为主 |
| **Plugin** | 打包分享 | 工具连接 |
| **子代理** | 内置多种 | Handoffs |
| **上下文窗口** | 1M tokens | 1.05M tokens |

### 何时用哪个？

```
需要深度编程和重构？ → Claude Code
需要审查不可信代码？ → Codex CLI（内核安全）
需要两者都要？ → 同时使用，不冲突
```

---

**下一节 →** [../frameworks/cline.md](../frameworks/cline.md) — Cline 完整架构
