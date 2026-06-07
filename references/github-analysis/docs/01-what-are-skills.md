# Skills 深度解析 — 大脑经验

## 目录
- [一、Skills 是什么](#一skills-是什么)
- [二、Skills 的结构](#二skills-的结构)
- [三、Progressive Disclosure（渐进披露）](#三progressive-disclosure渐进披露)
- [四、Skills 的类型](#四skills-的类型)
- [五、Skills 能做什么 vs 不能做什么](#五skills-能做什么-vs-不能做什么)
- [六、Skills 的优缺点](#六skills-的优缺点)
- [七、Skills 生态数据](#七skills-生态数据)

---

## 一、Skills 是什么

**Skills 本质 = Prompt + Workflow + Best Practice + 经验**

Skills 是文件夹，包含一个 `SKILL.md` 文件（YAML frontmatter + Markdown 指令）+ 可选的脚本/资源。
当用户的请求匹配某个 Skill 的 description 时，Agent 自动加载该 Skill 的完整指令。

> Anthropic 官方描述：Skills 是"入职指南"——你给新员工看的那种文档。

### 最简结构
```
my-skill/
└── SKILL.md          # 唯一必需文件
```

### 完整结构
```
my-skill/
├── SKILL.md          # 主指令文件
├── FORMS.md          # 参考文档（按需加载）
├── REFERENCE.md      # API 参考
├── templates/
│   └── report.md     # 模板文件
└── scripts/
    └── validate.py   # 可执行脚本（不进入上下文，只执行）
```

---

## 二、Skills 的结构

### SKILL.md 文件格式

```yaml
---
name: deploy-checklist
description: 部署前检查清单。当用户提到部署、发布、上线、rollout 时使用。
allowed-tools: Read, Bash, Grep
context: fork          # 在隔离的子代理上下文中运行
agent: general-purpose  # 指定子代理类型
model: sonnet          # 模型覆盖
disable-model-invocation: true  # 仅手动触发
user-invocable: false          # 隐藏（仅自动触发）
paths: "src/**/*.ts"           # 仅在匹配路径时自动加载
argument-hint: "[environment]"
---

# 部署检查清单

## 步骤
1. 运行 `git status` 确认无未提交的敏感文件
2. 检查 `.env` 不含硬编码密钥
3. 运行完整测试套件
4. 验证数据库迁移可回滚
5. 确认监控告警已配置
6. 执行部署
7. 部署后验证健康检查

## 回滚方案
如果健康检查失败，执行 `kubectl rollout undo deployment/main`
```

### Frontmatter 字段详解

| 字段 | 用途 | 默认值 |
|------|------|--------|
| `name` | 显示名 → `/slash-command` | 必填 |
| `description` | Agent 用来判断相关性 | 必填 |
| `allowed-tools` | Agent 可免确认使用的工具 | 全部工具 |
| `disable-model-invocation` | `true` = 仅手动触发 | `false` |
| `user-invocable` | `false` = 隐藏（仅自动触发） | `true` |
| `context` | `fork` = 在隔离子代理中运行 | 主上下文 |
| `agent` | 子代理类型（Explore/Plan/general-purpose） | - |
| `model` | 模型覆盖（haiku/sonnet/opus） | 默认模型 |
| `argument-hint` | 参数提示 | - |
| `paths` | Glob 模式限制自动加载范围 | 全项目 |

---

## 三、Progressive Disclosure（渐进披露）

这是 Skills 最核心的设计创新——**三层加载机制**：

| 层级 | 加载时机 | Token 开销 | 内容 |
|------|----------|-----------|------|
| **L1: Metadata** | 始终（启动时） | ~100 tokens/Skill | `name` + `description` |
| **L2: Instructions** | Skill 被触发时 | <5K tokens | SKILL.md 正文 |
| **L3: Resources** | 按需 | 无限制 | 参考文件、脚本（脚本代码不进上下文，只执行） |

### 为什么重要？

- 安装 100 个 Skill 也不会爆上下文窗口
- 每个 Skill 启动时只占 ~100 tokens
- 只有被触发的 Skill 才加载完整指令
- 脚本通过 bash 执行，代码本身不进上下文，只有输出进入

---

## 四、Skills 的类型

### 类型一：Capability Uplift（能力提升）
给 Agent 它**原本没有**的能力。

例如：
- **Web Scraping Skill** — 让 Agent 能抓取网页
- **PDF Processing Skill** — 让 Agent 能处理 PDF
- **Browser Testing Skill** — 让 Agent 能做端到端测试

### 类型二：Encoded Preference（偏好编码）
告诉 Agent **你的团队**怎么做某件事。

例如：
- **Code Review Checklist** — 你团队的代码审查标准
- **Commit Message Format** — 你团队的提交信息规范
- **Brand Guidelines** — 品牌设计方向

> "如果 Claude 对某个它技术上'知道'的任务反复产出通用输出，缺的可能就是一个 Encoded Preference Skill。"

### 类型三：Workflow Orchestration（工作流编排）
定义复杂的多步骤流程。

例如：
- **Deploy Workflow** — 分析→构建→测试→部署→验证
- **Incident Response** — 告警→诊断→修复→验证→复盘

---

## 五、Skills 能做什么 vs 不能做什么

### ✅ 能做
- 提供领域知识和最佳实践
- 定义标准化的工作流程
- 包含可执行脚本（在沙箱中运行）
- 自动触发（基于 description 匹配）
- 手动触发（通过 `/skill-name`）
- 跨项目/团队共享

### ❌ 不能做
- **不能直接执行外部 API 调用**（除非通过 MCP）
- **不能安装运行时包**（只能使用预装的库）
- **不能访问外部网络**（在 API 模式下）
- **不能持久化状态**（每次触发都是全新的）

---

## 六、Skills 的优缺点

### 优点
1. **提升推理质量** — 有 Skill 的 Agent 像高级工程师，没 Skill 的像实习生
2. **成本极低** — 几乎不用资源，只是 Prompt
3. **易迁移** — 可以给 GPT、Claude、Gemini、GLM 全部使用
4. **渐进披露** — 安装 100 个也不会浪费 token
5. **可执行代码** — 脚本直接运行，不进入上下文

### 缺点
1. **不能执行外部操作** — 只会说"应该这样做"，不会"真的去做"（需要 MCP 配合）
2. **容易过时** — Kubernetes 2024 教程到 2026 可能过期
3. **Prompt 污染** — Skill 太多会冲突、覆盖、遗忘
4. **触发不精准** — description 写得不好会误触发或漏触发

---

## 七、Skills 生态数据

### 采用情况（2026-06）
- **Claude Code**: 官方 Skills（pptx/xlsx/docx/pdf/frontend-design）+ 数千社区 Skills
- **OpenAI Codex**: `openai/skills` 官方仓库 + `$skill-installer` 安装器
- **Cursor / Gemini CLI / GitHub Copilot**: 全部支持 SKILL.md 格式
- **Superpowers**: 40.9K GitHub stars，最完整的 multi-agent Skill 集
- **Frontend Design Skill**: 277,000+ 次安装（截至 2026-03）
- **Agent Skills 标准**: 由 Anthropic 发布，已被 OpenAI/Google/Microsoft 采纳

### 关键 Skills 列表
| Skill | Stars | 类型 | 说明 |
|-------|-------|------|------|
| Superpowers | 40.9K | 能力提升 | 完整 multi-agent 开发工作流 |
| Frontend Design | 277K+ 安装 | 偏好编码 | 前端设计规范 |
| Karpathy's Guidelines | 144K | 偏好编码 | 4 条 LLM 编码原则 |
| Agent Skills for Context Engineering | 16.1K | 工作流 | 基础+架构+操作 Skills |
| Vercel Web Design | - | 偏好编码 | 100+ 规则审计 |
| Firecrawl | - | 能力提升 | 网页抓取/搜索 |

---

**下一节 →** [02-what-is-mcp.md](./02-what-is-mcp.md) — MCP 深度解析
